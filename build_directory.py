#!/usr/bin/env python3
"""Extract script metadata from TPT Oracle repo and build JSON for the directory page."""

import os
import re
import json
import glob

REPO = os.path.dirname(os.path.abspath(__file__))

# Stop words to exclude from keywords — common English + SQL noise
STOP_WORDS = {
    "the", "and", "for", "from", "with", "that", "this", "are", "was", "not",
    "but", "use", "can", "has", "its", "will", "all", "any", "may", "etc",
    "like", "into", "each", "also", "just", "than", "then", "them", "been",
    "have", "only", "when", "where", "what", "which", "who", "how", "more",
    "some", "such", "very", "most", "other", "about", "these", "those",
    "your", "their", "could", "would", "should", "does", "did", "get",
    "got", "set", "let", "put", "run", "see", "show", "display", "list",
    "print", "output", "using", "based", "given", "specified", "matching",
    "current", "information", "details", "data", "report", "query", "file",
    "name", "value", "number", "type", "used", "available", "still",
    "whether", "including", "specified", "both", "same", "last", "first",
    "new", "old", "one", "two", "need", "make", "take", "give", "work",
    "select", "column", "head", "format", "prompt", "define", "col",
    "break", "compute", "order", "group", "having", "distinct", "case",
    "decode", "null", "true", "false", "none",
    # Apache license noise
    "copyright", "licensed", "apache", "license", "terms", "conditions",
    "tanel", "poder", "tanelpoder", "http", "www", "com",
}

# Oracle-specific technical terms to boost in keywords
ORACLE_TERMS = {
    "ash", "awr", "sga", "pga", "uga", "redo", "undo", "temp", "lob",
    "clob", "blob", "index", "table", "tablespace", "datafile", "segment",
    "partition", "subpartition", "cursor", "latch", "mutex", "enqueue",
    "lock", "wait", "event", "session", "process", "sql_id", "plan",
    "optimizer", "hint", "baseline", "profile", "patch", "bind", "parse",
    "execute", "fetch", "commit", "rollback", "transaction", "rac",
    "instance", "cluster", "exadata", "cellsrv", "iorm", "flashcache",
    "snapper", "parallel", "workarea", "sort", "hash", "join",
    "nested", "full", "scan", "buffer", "cache", "pool", "shared",
    "library", "dictionary", "fixed", "object", "privilege", "role",
    "grant", "synonym", "sequence", "trigger", "procedure", "function",
    "package", "view", "materialized", "dblink", "directory",
    "scheduler", "job", "dbms_monitor", "dbms_system", "oradebug",
    "trace", "tkprof", "sql_trace", "xplan", "dbms_xplan",
    "histogram", "statistics", "cardinality", "selectivity",
    "blocking", "blocker", "deadlock", "contention",
    "spid", "sid", "serial", "pid", "ospid",
    "v$session", "v$sql", "v$lock", "v$process", "v$sysstat",
    "v$sesstat", "v$active_session_history", "gv$session",
    "dba_objects", "dba_tables", "dba_indexes", "dba_segments",
    "x$kcbwh", "x$ksppi", "x$ksmsp",
    "memory", "allocation", "resize", "advisor",
    "physical_read", "logical_read",
    "cpu", "elapsed", "time_waited", "wait_class",
    "metric", "sysmetric", "ossstat",
    "parameter", "spfile", "pfile", "init",
    "datapump", "rman", "backup", "recovery",
    "flashback", "logfile", "archive",
}


def parse_catalog(path):
    """Parse SCRIPTS_CATALOG.txt into structured entries."""
    entries = {}
    with open(path) as f:
        text = f.read()

    blocks = text.split("=" * 80)
    for block in blocks:
        block = block.strip()
        if not block or not block.startswith("SCRIPT:"):
            continue
        entry = {}
        lines = block.split("\n")
        current_key = None
        current_val = []

        for line in lines:
            m = re.match(r'^(SCRIPT|CATEGORY|KEYWORDS|PURPOSE|SYNTAX|PARAMETERS|EXAMPLES):\s*(.*)', line)
            if m:
                if current_key:
                    entry[current_key] = "\n".join(current_val).strip()
                current_key = m.group(1).lower()
                current_val = [m.group(2)]
            else:
                if current_key:
                    current_val.append(line)

        if current_key:
            entry[current_key] = "\n".join(current_val).strip()

        if "script" in entry:
            entries[entry["script"]] = entry

    return entries


def read_lines(filepath, max_lines=80):
    """Read first N lines of a file."""
    try:
        with open(filepath, "r", errors="replace") as f:
            lines = []
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                lines.append(line)
            return lines
    except:
        return []


def is_license_line(line):
    """Check if a line is part of the Apache license boilerplate."""
    s = line.strip().lstrip("-").lstrip("/").strip().lower()
    return any(kw in s for kw in [
        "copyright", "licensed under", "apache license", "license.txt",
        "terms & conditions", "all rights reserved", "more info at",
        "http://tanelpoder", "https://tanelpoder",
        "(c) http://", "(c) https://",
    ])


def extract_header(filepath):
    """Extract description, author, usage, examples from a SQL file's header."""
    lines = read_lines(filepath, 80)
    if not lines:
        return "", "", "", ""

    desc = ""
    author = ""
    usage = ""
    example = ""

    text = "".join(lines)

    # --- Purpose / Description ---
    # Pattern 1: "-- Purpose:" or "-- Description:" header field
    m = re.search(
        r'--\s*(?:Purpose|Description)\s*[:\-]\s*(.+?)(?:\n\s*--\s*$|\n\s*--\s*(?:Author|Usage|Other|Copyright|Example))',
        text, re.IGNORECASE | re.DOTALL
    )
    if m:
        desc = re.sub(r'\n\s*--\s*', ' ', m.group(1)).strip()

    # Pattern 2: "-- File name:" block (common in TPT)
    if not desc:
        m = re.search(
            r'--\s*File\s+name:\s*.+?\n\s*--\s*Purpose:\s*(.+?)(?:\n\s*--\s*$|\n\s*--\s*(?:Author|Usage|Other))',
            text, re.IGNORECASE | re.DOTALL
        )
        if m:
            desc = re.sub(r'\n\s*--\s*', ' ', m.group(1)).strip()

    # Pattern 3: PROMPT line that describes the script
    if not desc:
        for line in lines[:25]:
            s = line.strip()
            if s.upper().startswith("PROMPT") and len(s) > 10:
                prompt_text = s[6:].strip().lstrip("-").strip()
                # Skip prompts that are just parameter echoes or dashes
                if (prompt_text and len(prompt_text) > 10
                    and not prompt_text.startswith("---")
                    and not prompt_text.startswith("===")
                    and not prompt_text.startswith("***")
                    and "&" not in prompt_text[:5]):  # Allow & later in string
                    desc = prompt_text.rstrip(".")
                    break

    # Pattern 4: First substantive comment line after license
    if not desc:
        past_license = False
        for line in lines[:30]:
            s = line.strip()
            if not s or is_license_line(line):
                if is_license_line(line):
                    past_license = True
                continue
            if re.match(r'^-{4,}$|^={4,}$|^\*{4,}$', s):
                continue

            if s.startswith("--"):
                comment = s.lstrip("-").strip()
                if re.match(r'^(File\s+name|Author|Usage|Other|Copyright|Example|REM|SET|COL|DEF)', comment, re.IGNORECASE):
                    continue
                if comment and len(comment) > 10 and past_license:
                    desc = comment
                    break

    # Final cleanup: reject descriptions that are clearly SQL fragments, not descriptions
    if desc:
        d_lower = desc.lower().strip()
        if (d_lower.startswith(("select ", "from ", "where ", "drop ", "create ",
                                 "alter ", "insert ", "update ", "delete ", "grant ",
                                 "begin ", "declare ", "exec ", "set ", "col ",
                                 "v$", "dba_", "all_", "user_", "sys.", "....",
                                 "from_time", "to_time", "dropping"))
            or d_lower.endswith((" from", " where", " and", " or"))
            or len(desc) < 12
            or re.match(r'^[\.\-\*=\s]+$', desc)
            or re.match(r'^[A-Z_]+=&', desc)):
            desc = ""

    # --- Author ---
    m = re.search(r'--\s*Author\s*[:\-]\s*(.+)', text, re.IGNORECASE)
    if m:
        author = m.group(1).strip().lstrip("-").strip()

    # --- Usage / Syntax ---
    # Pattern 1: "-- Usage:" header field
    m = re.search(r'--\s*Usage\s*[:\-]\s*(.+)', text, re.IGNORECASE)
    if m:
        usage = m.group(1).strip().lstrip("-").strip()
        # Collect continuation lines
        idx = text.index(m.group(0)) + len(m.group(0))
        rest = text[idx:]
        for uline in rest.split("\n"):
            us = uline.strip()
            if us.startswith("--") and ("@" in us or us.strip("- ").startswith("@")):
                extra = us.lstrip("-").strip()
                usage += "\n" + extra
            else:
                break

    # Pattern 2: Infer from PROMPT that contains @
    if not usage:
        for line in lines[:25]:
            s = line.strip()
            if s.upper().startswith("PROMPT") and "@" in s:
                prompt_text = s[6:].strip()
                if "@" in prompt_text:
                    usage = prompt_text
                    break

    # --- Examples ---
    m = re.search(r'--\s*Example[s]?\s*[:\-]\s*(.+?)(?:\n\s*--\s*$|\n\s*--\s*(?:Other|Author|\-{4,}))', text, re.IGNORECASE | re.DOTALL)
    if m:
        example = re.sub(r'\n\s*--\s*', '\n', m.group(1)).strip()

    return desc.strip(), author.strip(), usage.strip(), example.strip()


def extract_parameters(filepath):
    """Infer parameter semantics from &1, &2 etc usage in the script."""
    lines = read_lines(filepath, 120)
    if not lines:
        return ""

    text = "".join(lines)

    # Find max parameter number used
    param_nums = set(int(m) for m in re.findall(r'&(\d+)', text))
    if not param_nums:
        return ""

    max_param = max(param_nums)
    params = {}

    for n in range(1, max_param + 1):
        params[n] = None

    # Strategy 1: DEF/DEFINE lines that assign &N to a named variable
    # e.g., DEF _lhp_sid="&2"  or  DEF num_samples=&2
    for line in lines:
        m = re.match(r'^\s*(?:DEF|DEFINE)\s+(\w+)\s*=\s*["\']?&(\d+)["\']?', line, re.IGNORECASE)
        if m:
            varname = m.group(1).strip("_").replace("_", " ")
            num = int(m.group(2))
            if num in params:
                params[num] = varname

    # Strategy 2: PROMPT lines that reference &N
    # e.g., "prompt Show SQL for SQLID &1 child &2"
    for line in lines:
        s = line.strip()
        if s.upper().startswith("PROMPT") and "&" in s:
            prompt = s[6:].strip()
            # Find words immediately before &N
            for m in re.finditer(r'(\w+)\s+&(\d+)', prompt):
                word = m.group(1).lower()
                num = int(m.group(2))
                if num in params and params[num] is None:
                    params[num] = word

    # Strategy 3: WHERE clause context
    # e.g., "where sid in (&1)" -> &1 is sid
    #        "and sql_id = ('&1')" -> &1 is sql_id
    #        "like lower('%&1%')" -> &1 is name pattern
    for line in lines:
        s = line.strip().lower()
        for m in re.finditer(r"(\w+)\s*(?:=|like|in\s*\()\s*[('\s]*(?:%?)&(\d+)", s):
            col = m.group(1)
            num = int(m.group(2))
            if num in params and params[num] is None:
                # Clean up column name
                col = col.strip("_").replace("lower(", "").replace("upper(", "")
                if col not in ("and", "or", "where", "having", "on"):
                    params[num] = col

    # Strategy 4: Column alias patterns near &N
    # e.g., "@@tab2 '%&1%'" -> &1 is table name pattern
    for line in lines:
        s = line.strip()
        m = re.match(r'^@@(\w+)\s+["\']?%?&(\d+)', s, re.IGNORECASE)
        if m:
            script_called = m.group(1).lower()
            num = int(m.group(2))
            if num in params and params[num] is None:
                # Infer from the wrapper script name
                name_hints = {
                    "tab": "table_name", "ind": "index_or_table",
                    "seg": "segment_name", "o": "object_name",
                    "col": "column_name",
                }
                for prefix, hint in name_hints.items():
                    if script_called.startswith(prefix):
                        params[num] = hint
                        break
                else:
                    params[num] = "pattern"

    # Strategy 5: ACCEPT statements
    # e.g., ACCEPT sid PROMPT "Enter SID: "
    for line in lines:
        m = re.match(r'^\s*ACCEPT\s+(\w+)', line, re.IGNORECASE)
        if m:
            varname = m.group(1).lower()
            # Match ACCEPT variable to &N if the variable is later used as &N
            # This is a heuristic - just note the accept var name
            for n in params:
                if params[n] is None:
                    params[n] = varname
                    break

    # Build parameter string
    parts = []
    for n in sorted(params.keys()):
        name = params[n]
        if name:
            # Clean up parameter name
            name = name.strip("_").replace("_", " ")
        else:
            name = f"param{n}"
        parts.append(f"&{n}: {name}")

    return ", ".join(parts) if parts else ""


def infer_syntax(filepath, usage, params_str):
    """Build a syntax string from usage line or filename + params."""
    if usage and "@" in usage:
        return usage.split("\n")[0]  # First line of usage

    relpath = os.path.relpath(filepath, REPO)
    base = f"@{relpath}"

    if not params_str:
        return base

    # Build from params
    param_parts = []
    for p in params_str.split(", "):
        m = re.match(r'&\d+:\s*(.+)', p)
        if m:
            param_parts.append(f"<{m.group(1)}>")
    if param_parts:
        return f"{base} {' '.join(param_parts)}"
    return base


def infer_category(filepath, desc=""):
    """Infer category from filepath and description."""
    name = os.path.basename(filepath).lower()
    dirname = os.path.dirname(filepath).replace(REPO, "").strip("/").lower()

    if dirname.startswith("ash"):
        return "ASH Analysis"
    if dirname.startswith("awr"):
        return "AWR Analysis"
    if dirname.startswith("aot"):
        return "Advanced Oracle Troubleshooting"
    if dirname.startswith("demos"):
        return "Demos"
    if dirname.startswith("exadata"):
        return "Exadata"
    if dirname.startswith("tools"):
        return "Tools / Utilities"
    if dirname.startswith("ast"):
        return "Advanced SQL Tuning"
    if dirname.startswith("setup"):
        return "Setup / Configuration"
    if dirname.startswith("ppx"):
        return "Performance Profiling"
    if dirname.startswith("experiments"):
        return "Experiments"
    if dirname.startswith("im"):
        return "In-Memory"
    if dirname.startswith("bugs"):
        return "Bug Test Cases"
    if dirname.startswith("statspack"):
        return "Statspack"
    if dirname.startswith("deprecated"):
        return "Deprecated"

    dl = (desc or "").lower() + " " + name
    if any(w in dl for w in ["snapper", "profil", "latchprof", "mutexprof"]):
        return "Performance Monitoring"
    if any(w in dl for w in ["ash", "active session"]):
        return "ASH Analysis"
    if any(w in dl for w in ["awr", "workload"]):
        return "AWR Analysis"
    if any(w in dl for w in ["lock", "enqueue", "blocking"]):
        return "Lock Analysis"
    if any(w in dl for w in ["wait", "event"]):
        return "Wait Analysis"
    if any(w in dl for w in ["session", "sid", "ses"]) and "sql" not in dl:
        return "Session Monitoring"
    if any(w in dl for w in ["explain", "xplan"]) or (name.startswith("x") and "plan" in dl):
        return "Execution Plans"
    if any(w in dl for w in ["sql_id", "sqlid", "cursor", "bind", "sql_text"]):
        return "SQL Analysis"
    if any(w in dl for w in ["baseline", "patch", "profile", "hint", "tuning"]):
        return "SQL Tuning"
    if any(w in dl for w in ["table", "index", "column", "partition", "lob", "segment",
                              "object", "synonym", "sequence", "trigger", "procedure",
                              "ddl", "describe"]):
        return "Object Information"
    if any(w in dl for w in ["sga", "pga", "memory", "buffer", "cache"]):
        return "Memory Management"
    if any(w in dl for w in ["tablespace", "datafile", "space", "storage"]):
        return "Space Management"
    if any(w in dl for w in ["parameter", "init", "config", "setting", "directory",
                              "dblink", "redo", "log"]):
        return "System Configuration"
    if any(w in dl for w in ["trace", "diagnostic", "oradebug"]):
        return "Tracing / Diagnostics"
    if any(w in dl for w in ["kill", "cancel", "disconnect"]):
        return "Session Management"
    if any(w in dl for w in ["job", "scheduler"]):
        return "Scheduler / Jobs"
    if any(w in dl for w in ["user", "username", "grant", "privilege", "role"]):
        return "User Management"
    if any(w in dl for w in ["rac", "cluster", "instance"]):
        return "RAC / Cluster"
    if any(w in dl for w in ["help", "init.sql", "login.sql", "calc", "ascii"]):
        return "Utility"
    if any(w in name for w in ["stat", "metric", "sys"]):
        return "System Monitoring"

    return "Other"


def extract_keywords(filepath, desc, category):
    """Generate relevant technical keywords only — no common words."""
    lines = read_lines(filepath, 60)
    text = "".join(lines).lower()
    words = set()

    # Extract Oracle-specific terms found in the file (whole word match only)
    for term in ORACLE_TERMS:
        # Use word boundary matching to avoid partial matches like "io" in "information"
        if re.search(r'\b' + re.escape(term) + r'\b', text):
            words.add(term)

    # Extract V$ view references
    for m in re.finditer(r'(g?v\$\w+|x\$\w+|dba_\w+|all_\w+|user_\w+)', text):
        words.add(m.group(1))

    # Add terms from the description (only technical/meaningful ones)
    if desc:
        for w in re.findall(r'\b[a-z_]{3,}\b', desc.lower()):
            if w in ORACLE_TERMS:
                words.add(w)
            elif w not in STOP_WORDS and len(w) >= 4:
                # Only add if it looks technical (contains underscore or is known)
                if "_" in w:
                    words.add(w)

    # Add from category
    for w in re.findall(r'[a-z]+', category.lower()):
        if w not in STOP_WORDS and len(w) >= 3:
            words.add(w)

    # Limit to most relevant (max 12)
    # Prioritize Oracle terms, then V$ views, then others
    oracle = sorted(w for w in words if w in ORACLE_TERMS)
    views = sorted(w for w in words if w.startswith(("v$", "gv$", "x$", "dba_", "all_", "user_")))
    others = sorted(w for w in words if w not in oracle and w not in views)

    result = []
    result.extend(oracle[:8])
    result.extend(views[:3])
    result.extend(others[:3])

    # Deduplicate while preserving order
    seen = set()
    final = []
    for w in result:
        if w not in seen:
            seen.add(w)
            final.append(w)

    return ", ".join(final[:12])


CATEGORY_NORMALIZE = {
    "ASH Analysis / Lock Analysis": "ASH Analysis",
    "ASH Analysis / SQL Analysis": "ASH Analysis",
    "ASH Analysis / SQL Tuning": "ASH Analysis",
    "ASH Analysis / Wait Analysis": "ASH Analysis",
    "AWR / SQL Analysis": "AWR Analysis",
    "AWR / SQL Tuning": "AWR Analysis",
    "AWR / System Monitoring": "AWR Analysis",
    "AWR / Wait Analysis": "AWR Analysis",
    "Memory Management / Workarea": "Memory Management",
    "Memory Management / Dictionary Cache": "Memory Management",
    "Object Information / Buffer Cache": "Object Information",
    "Object Information / DDL": "Object Information",
    "Object Information / Performance": "Object Information",
    "Object Information / PL/SQL": "Object Information",
    "Object Information / Statistics": "Object Information",
    "Performance Monitoring / Buffer Cache": "Performance Monitoring",
    "Performance Monitoring / Latch Analysis": "Performance Monitoring",
    "Performance Monitoring / Profiling": "Performance Monitoring",
    "Performance Monitoring / Wait Analysis": "Performance Monitoring",
    "SQL Analysis / Cursor": "SQL Analysis",
    "SQL Analysis / Memory": "SQL Analysis",
    "SQL Monitoring": "SQL Analysis",
    "SQL Tuning / Execution Plans": "SQL Tuning",
    "Session Management / Tracing": "Session Management",
    "Session Monitoring / Events": "Session Monitoring",
    "Session Monitoring / Security": "Session Monitoring",
    "Statistics / Object Information": "Object Information",
    "System Configuration / Database Info": "System Configuration",
    "System Configuration / Globalization": "System Configuration",
    "System Configuration / Multitenant": "System Configuration",
    "System Configuration / Redo": "System Configuration",
    "System Configuration / Services": "System Configuration",
    "System Monitoring / Background Processes": "System Monitoring",
    "Transaction Monitoring": "Session Monitoring",
    "Transaction Monitoring / Undo": "Session Monitoring",
    "Parallel Execution": "Performance Monitoring",
    "RAC / Cluster": "System Configuration",
    "Error Handling": "Utility",
    "Utility / Search": "Utility",
    "Tracing / Diagnostics": "Tracing & Diagnostics",
    "Scheduler / Jobs": "System Configuration",
    "User Management": "System Configuration",
    "Bug Test Cases": "Experiments",
    "Statspack": "AWR Analysis",
    "Deprecated": "Other",
}


def normalize_category(cat):
    return CATEGORY_NORMALIZE.get(cat, cat)


def main():
    catalog_path = os.path.join(REPO, "SCRIPTS_CATALOG.txt")
    catalog = parse_catalog(catalog_path) if os.path.exists(catalog_path) else {}

    all_sql = []
    for pattern in ["*.sql", "**/*.sql"]:
        all_sql.extend(glob.glob(os.path.join(REPO, pattern), recursive=True))
    all_sql = sorted(set(all_sql))

    scripts = []
    seen = set()

    for filepath in all_sql:
        relpath = os.path.relpath(filepath, REPO)
        if relpath.startswith("."):
            continue
        if relpath in seen:
            continue
        seen.add(relpath)

        cat_entry = catalog.get(relpath) or catalog.get(os.path.basename(relpath))

        if cat_entry:
            entry = {
                "file": relpath,
                "name": os.path.basename(relpath),
                "category": normalize_category(cat_entry.get("category", "Other")),
                "keywords": cat_entry.get("keywords", ""),
                "purpose": cat_entry.get("purpose", ""),
                "syntax": cat_entry.get("syntax", ""),
                "parameters": cat_entry.get("parameters", ""),
                "examples": cat_entry.get("examples", ""),
                "documented": True,
            }
        else:
            desc, author, usage, example = extract_header(filepath)
            params_str = extract_parameters(filepath)
            category = normalize_category(infer_category(filepath, desc))
            syntax = infer_syntax(filepath, usage, params_str)
            keywords = extract_keywords(filepath, desc, category)

            entry = {
                "file": relpath,
                "name": os.path.basename(relpath),
                "category": category,
                "keywords": keywords,
                "purpose": desc,
                "syntax": syntax,
                "parameters": params_str,
                "examples": example,
                "documented": False,
            }

        dirname = os.path.dirname(relpath)
        entry["directory"] = dirname if dirname else "root"
        scripts.append(entry)

    scripts.sort(key=lambda s: (not s["documented"], s["category"], s["name"]))
    print(json.dumps(scripts, indent=2))


if __name__ == "__main__":
    main()
