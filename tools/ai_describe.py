#!/usr/bin/env python3
"""Classify TPT scripts with Claude and cache the results in .ai_descriptions.json.

For every .sql file in the repo, one model call returns a small JSON record:

    purpose   one-sentence DBA-facing description
    category  one of CATEGORIES (fixed list shared with build_directory.py)
    kind      tool | wrapper | demo | fragment | setup | stub
    tags      3-8 short search tags
    params    [{"n": 1, "name": "sql_id", "desc": "..."}, ...]

Results are cached by file path + content hash, so re-runs only touch new or
changed scripts. build_directory.py reads the cache and merges it with the
curated SCRIPTS_CATALOG.txt (curated purpose/syntax/examples always win; AI
supplies category/kind/tags/params where the catalog has none).

Backends:
  --backend claude-code   (default) shells out to the `claude` CLI, billed to
                          your Claude subscription. ~3-6 s per call.
  --backend api           anthropic SDK, needs ANTHROPIC_API_KEY.

Usage:
  python3 tools/ai_describe.py --dry-run          # what would run
  python3 tools/ai_describe.py --limit 5          # smoke test
  python3 tools/ai_describe.py                    # fill missing / changed
  python3 tools/ai_describe.py --force            # regenerate everything
  python3 tools/ai_describe.py --only ash/ashtop.sql --force
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".ai_descriptions.json"
MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5")
MAX_CHARS = 8000
CLI_TIMEOUT = 180
SCHEMA_VERSION = 2  # bump when the record shape or prompt changes materially

CATEGORIES = [
    "Session & Process",
    "SQL & Execution Plans",
    "Waits, Locks & Latches",
    "ASH Analysis",
    "AWR & History",
    "Memory",
    "Objects & Storage",
    "Instance & Configuration",
    "Tracing & Diagnostics",
    "Exadata",
    "Demos & Experiments",
    "SQL*Plus Utilities",
]

KINDS = ["tool", "wrapper", "demo", "fragment", "setup", "stub"]

SYSTEM_PROMPT = f"""You classify Oracle DBA troubleshooting scripts from Tanel Poder's TPT library (SQL*Plus scripts).

Return ONLY a JSON object, no markdown, no prose, with these keys:

"purpose": ONE sentence, max 18 words, from a DBA's perspective. Start with a verb
   (Shows, Samples, Profiles, Dumps, Lists, Compares, Enables, ...). Do not start with
   "This script". State what it is for, not how it is implemented. If it is a thin
   wrapper, say what it wraps. If empty / comments only, say "Placeholder or stub script".

"category": exactly one of:
{chr(10).join('   - ' + c for c in CATEGORIES)}
   Guidance: ASH Analysis = anything sampling GV$SESSION or reading ASH/DBA_HIST_ACTIVE_SESS_HISTORY.
   AWR & History = DBA_HIST_* / statspack. Waits, Locks & Latches = wait events, enqueues,
   blockers, latches, mutexes. Memory = SGA/PGA/shared pool/buffer cache. Objects & Storage =
   tables, indexes, segments, partitions, tablespaces, datafiles, ASM, stats. Instance &
   Configuration = parameters, users/privs, jobs, services, redo, RAC, PDBs, licensing.
   Tracing & Diagnostics = 10046/10053, oradebug, dumps, X$ internals, stack sampling.
   SQL*Plus Utilities = login/init, formatting, set/restore, spool helpers, calculators.
   Demos & Experiments = scripts whose purpose is to create a scenario for a talk or test,
   not to troubleshoot.

"kind": exactly one of {KINDS}.
   tool = a usable troubleshooting/query script. wrapper = mostly calls another script.
   demo = creates load, test tables or a scenario. fragment = an incomplete SQL snippet
   meant to be included by another script. setup = install/grant/create views.
   stub = empty, TODO, or broken.

"tags": 3 to 8 lowercase search tags: Oracle concepts and the main V$/X$/DBA_ views used
   (e.g. "sql_id", "v$session", "latch", "10046", "shared pool"). No generic words.

"params": list of positional parameters the script takes (&1, &2 ...), each
   {{"n": 1, "name": "short_snake_name", "desc": "what to pass, max 10 words"}}.
   Use [] if the script takes none. Infer names from DEFINE/PROMPT/WHERE usage.

Example:
{{"purpose":"Shows top ASH activity grouped by the columns you specify for a time range","category":"ASH Analysis","kind":"tool","tags":["ash","gv$session","top activity","wait event","sql_id"],"params":[{{"n":1,"name":"group_by","desc":"comma-separated columns to group by"}},{{"n":2,"name":"filter","desc":"WHERE predicate, 1=1 for all"}},{{"n":3,"name":"from_time","desc":"start timestamp expression"}},{{"n":4,"name":"to_time","desc":"end timestamp expression"}}]}}"""


def load_cache() -> dict:
    if CACHE.exists():
        return json.loads(CACHE.read_text())
    return {}


def save_cache(c: dict) -> None:
    CACHE.write_text(json.dumps(c, indent=1, sort_keys=True, ensure_ascii=False) + "\n")


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def read_truncated(path: Path) -> str:
    text = path.read_text(errors="replace")
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + f"\n\n[... truncated, full file is {len(text)} chars ...]"
    return text


def user_message(rel: str, content: str) -> str:
    return f"FILE: {rel}\n\n---\n{content}\n---\n\nReturn the JSON object only."


def describe_via_api(client, rel: str, content: str) -> dict:
    resp = client.messages.create(
        model=MODEL,
        max_tokens=600,
        system=[{"type": "text", "text": SYSTEM_PROMPT,
                 "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user_message(rel, content)}],
    )
    return parse_record(resp.content[0].text)


_CLI_CWD = tempfile.mkdtemp(prefix="tpt_ai_")  # neutral cwd: don't load repo CLAUDE.md


def describe_via_cli(rel: str, content: str) -> dict:
    proc = subprocess.run(
        ["claude", "-p", "--output-format", "json", "--model", MODEL,
         "--system-prompt", SYSTEM_PROMPT],
        input=user_message(rel, content),
        capture_output=True, text=True, timeout=CLI_TIMEOUT, cwd=_CLI_CWD,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"claude CLI exited {proc.returncode}: {proc.stderr.strip()[:400]}")
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"claude CLI returned non-JSON: {proc.stdout[:200]!r}") from e
    if data.get("is_error"):
        raise RuntimeError(f"claude CLI reported error: {data.get('result') or data}")
    return parse_record(data.get("result", ""))


def parse_record(text: str) -> dict:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.S)
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError(f"no JSON object in response: {text[:160]!r}")
    rec = json.loads(m.group(0))
    return normalize(rec)


def normalize(rec: dict) -> dict:
    purpose = str(rec.get("purpose", "")).strip().strip('"').rstrip(".")
    purpose = purpose.splitlines()[0] if purpose else ""
    if not purpose:
        raise ValueError("empty purpose")

    category = str(rec.get("category", "")).strip()
    if category not in CATEGORIES:
        low = category.lower()
        category = next((c for c in CATEGORIES if c.lower() == low), None) or \
            next((c for c in CATEGORIES if low and low.split()[0] in c.lower()), None)
        if category is None:
            raise ValueError(f"bad category {rec.get('category')!r}")

    kind = str(rec.get("kind", "tool")).strip().lower()
    if kind not in KINDS:
        kind = "tool"

    tags = rec.get("tags") or []
    tags = [str(t).strip().lower() for t in tags if str(t).strip()][:8]

    params = []
    for p in rec.get("params") or []:
        try:
            n = int(p.get("n"))
        except (TypeError, ValueError, AttributeError):
            continue
        name = re.sub(r"\W+", "_", str(p.get("name", f"param{n}")).strip().lower()).strip("_") or f"param{n}"
        params.append({"n": n, "name": name, "desc": str(p.get("desc", "")).strip()})
    params.sort(key=lambda p: p["n"])

    return {"purpose": purpose, "category": category, "kind": kind,
            "tags": tags, "params": params}


def all_scripts() -> list[Path]:
    out = []
    for p in ROOT.rglob("*.sql"):
        rel = p.relative_to(ROOT)
        if any(part.startswith(".") for part in rel.parts):
            continue
        out.append(p)
    return sorted(out)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--backend", choices=("api", "claude-code"), default="claude-code")
    p.add_argument("--force", action="store_true", help="ignore cache, regenerate all")
    p.add_argument("--limit", type=int, default=0, help="cap calls (0 = unlimited)")
    p.add_argument("--only", action="append", default=[], help="restrict to these relative paths")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def main():
    args = parse_args()

    if not args.dry_run:
        if args.backend == "api" and not os.environ.get("ANTHROPIC_API_KEY"):
            sys.exit("ERROR: ANTHROPIC_API_KEY not set (or use --backend claude-code).")
        if args.backend == "claude-code" and not shutil.which("claude"):
            sys.exit("ERROR: `claude` CLI not found on PATH (or use --backend api).")

    cache = load_cache()
    files = all_scripts()
    if args.only:
        wanted = set(args.only)
        files = [f for f in files if str(f.relative_to(ROOT)) in wanted]

    todo = []
    for f in files:
        rel = str(f.relative_to(ROOT))
        h = file_hash(f)
        c = cache.get(rel)
        fresh = c and c.get("hash") == h and c.get("schema") == SCHEMA_VERSION
        if fresh and not args.force:
            continue
        todo.append((rel, f, h))

    # Drop cache entries for files that no longer exist
    live = {str(f.relative_to(ROOT)) for f in all_scripts()}
    for stale in [k for k in cache if k not in live]:
        del cache[stale]

    print(f"→ {len(files)} scripts, {len(files) - len(todo)} cached, {len(todo)} to generate"
          f"  (backend={args.backend} model={MODEL} workers={args.workers})")
    if args.dry_run:
        return
    if args.limit:
        todo = todo[:args.limit]

    if args.backend == "api":
        try:
            from anthropic import Anthropic
        except ImportError:
            sys.exit("ERROR: pip install anthropic (or use --backend claude-code).")
        client = Anthropic()
        describe = lambda rel, content: describe_via_api(client, rel, content)
    else:
        describe = describe_via_cli

    def work(item):
        rel, path, h = item
        content = read_truncated(path)
        last = None
        for attempt in range(3):
            try:
                rec = describe(rel, content)
                rec.update({"hash": h, "model": MODEL, "schema": SCHEMA_VERSION})
                return rel, rec, None
            except Exception as e:  # noqa: BLE001
                last = e
                time.sleep(2 * (attempt + 1))
        return rel, None, last

    done = errors = 0
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = [ex.submit(work, it) for it in todo]
        for fut in as_completed(futures):
            rel, rec, err = fut.result()
            if rec:
                cache[rel] = rec
                done += 1
                print(f"  [{done + errors:4d}/{len(todo)}] {rel}: [{rec['category']}/{rec['kind']}] {rec['purpose'][:70]}")
            else:
                errors += 1
                print(f"  ! {rel}: {err}", file=sys.stderr)
            if (done + errors) % 25 == 0:
                save_cache(cache)

    save_cache(cache)
    print(f"✓ done in {time.time() - t0:.0f}s — generated: {done}, errors: {errors}")
    print("  now run ./rebuild.sh to regenerate scripts_data.js")


if __name__ == "__main__":
    main()
