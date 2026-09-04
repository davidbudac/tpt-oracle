#!/usr/bin/env bash
# Rebuild the directory index and catalogs after pulling new scripts.
#
# Usage:
#   ./rebuild.sh                   # rebuild everything (rule-based descriptions only)
#   ./rebuild.sh --ai              # …first classify new/changed scripts via `claude` CLI
#   ./rebuild.sh --ai --api        # …use the Anthropic API instead (ANTHROPIC_API_KEY)
#   ./rebuild.sh --ai --force      # regenerate every AI record from scratch
#   ./rebuild.sh --ai --limit 20   # cap calls (good for testing)
#   ./rebuild.sh --serve           # rebuild, then start a local web server
#   ./rebuild.sh --check           # rebuild into a tmp file and diff vs. current
#
# Outputs (overwritten in place):
#   .ai_descriptions.json    — cache of AI classifications (commit this)
#   scripts_data.js          — curated catalog + AI cache + heuristics, consumed by directory.html
#   SCRIPTS_CATALOG.csv      — CSV export of the curated catalog
#
# Environment:
#   ANTHROPIC_API_KEY   required for --ai --api
#   ANTHROPIC_MODEL     override model (default: claude-haiku-4-5)
#   PORT                --serve port (default: 8000)
#   PYTHON              python interpreter (default: python3)

set -euo pipefail

cd "$(dirname "$0")"

PY=${PYTHON:-python3}
SERVE=0
CHECK=0
AI=0
FORCE=0
API=0
LIMIT=
PORT=${PORT:-8000}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --serve) SERVE=1 ;;
    --check) CHECK=1 ;;
    --ai)    AI=1 ;;
    --force) FORCE=1 ;;
    --api)   API=1 ;;
    --limit) LIMIT="$2"; shift ;;
    --limit=*) LIMIT="${1#--limit=}" ;;
    -h|--help)
      sed -n '2,22p' "$0"; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
  shift
done

log() { printf '\033[1;36m▌\033[0m %s\n' "$*"; }
ok()  { printf '\033[1;32m✓\033[0m %s\n' "$*"; }

# --- 1. AI classification cache (optional) --------------------------------
if [[ $AI -eq 1 && $CHECK -eq 0 ]]; then
  log "Classifying new/changed scripts via Claude…"
  ai_args=()
  [[ $API -eq 1 ]] && ai_args+=(--backend api)
  [[ $FORCE -eq 1 ]] && ai_args+=(--force)
  [[ -n "$LIMIT" ]] && ai_args+=(--limit "$LIMIT")
  "$PY" tools/ai_describe.py "${ai_args[@]}"
fi

# --- 2. scripts_data.js ---------------------------------------------------
TARGET=scripts_data.js
TMP=$(mktemp -t scripts_data.XXXXXX.js)
trap 'rm -f "$TMP"' EXIT

log "Building $TARGET from $(find . -name '*.sql' -not -path './.git/*' | wc -l | tr -d ' ') SQL files…"
{
  printf 'const SCRIPTS_DATA = '
  "$PY" build_directory.py
  printf ';\n'
} > "$TMP"

if [[ $CHECK -eq 1 ]]; then
  if diff -q "$TARGET" "$TMP" >/dev/null 2>&1; then
    ok "$TARGET is up to date"
  else
    echo "DIFFERS: $TARGET would change. Run without --check to apply."
    "$PY" - "$TARGET" "$TMP" <<'PYEOF' || true
import json, re, sys
def load(p):
    t = open(p).read()
    return {e["file"]: e for e in json.loads(re.match(r"\s*const SCRIPTS_DATA\s*=\s*(.*?);?\s*$", t, re.S).group(1))}
a, b = load(sys.argv[1]), load(sys.argv[2])
added, removed = sorted(set(b) - set(a)), sorted(set(a) - set(b))
changed = [f for f in a if f in b and a[f] != b[f]]
print(f"  added {len(added)}, removed {len(removed)}, changed {len(changed)}")
for f in (added + removed + changed)[:20]:
    fields = [k for k in set(a.get(f, {})) | set(b.get(f, {})) if a.get(f, {}).get(k) != b.get(f, {}).get(k)]
    print(f"    {f}: {', '.join(sorted(fields))}")
PYEOF
    exit 1
  fi
else
  mv "$TMP" "$TARGET"
  trap - EXIT
  ok "wrote $TARGET ($(wc -c < "$TARGET" | tr -d ' ') bytes)"
fi

# --- 3. SCRIPTS_CATALOG.csv ----------------------------------------------
if [[ -f tools/generate_search_catalog_csv.py ]]; then
  log "Regenerating SCRIPTS_CATALOG.csv…"
  "$PY" tools/generate_search_catalog_csv.py
  ok "wrote SCRIPTS_CATALOG.csv"
fi

# --- 5. summary -----------------------------------------------------------
COUNT=$(grep -o '"file":' "$TARGET" | wc -l | tr -d ' ')
ok "indexed $COUNT scripts"

if [[ $SERVE -eq 1 ]]; then
  log "serving at http://localhost:$PORT/directory.html  (Ctrl-C to stop)"
  exec "$PY" -m http.server "$PORT"
fi
