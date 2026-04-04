#!/usr/bin/env python3
"""Extract script metadata from TPT Oracle repo and build JSON for the directory page."""

import os
import re
import json
import glob

REPO = os.path.dirname(os.path.abspath(__file__))

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


def extract_header(filepath):
    """Extract description, author, usage from a SQL file's header comments."""
    desc = ""
    author = ""
    usage = ""
    example = ""
    try:
        with open(filepath, "r", errors="replace") as f:
            lines = []
            for i, line in enumerate(f):
                if i >= 50:
                    break
                lines.append(line)
    except:
        return desc, author, usage, example

    text = "".join(lines)

    # Try to find description
    m = re.search(r'(?:Description|PURPOSE)\s*[:\-]?\s*(.+?)(?:\n\s*\n|\n\s*--\s*(?:Author|Usage|Other))', text, re.IGNORECASE | re.DOTALL)
    if m:
        desc = re.sub(r'\s*--\s*', ' ', m.group(1)).strip()
    else:
        # Try simpler patterns
        for line in lines[:20]:
            stripped = line.strip().lstrip("-").lstrip("/").strip()
            if stripped and not stripped.startswith("@") and not stripped.startswith("SET ") and not stripped.startswith("COL ") and not stripped.startswith("DEF ") and not stripped.startswith("DEFINE ") and len(stripped) > 15 and not stripped.startswith("Copyright") and not stripped.startswith("http"):
                # Check if it looks like a description
                if re.match(r'^[A-Z].*', stripped) and not re.match(r'^(REM|PROMPT|SELECT|FROM|WHERE|AND|OR |WITH |CREATE|DROP|ALTER|GRANT|EXEC|BEGIN|DECLARE|SET |COLUMN|BREAK|COMPUTE|TTITLE|BTITLE|SPOOL|ACCEPT)', stripped):
                    desc = stripped
                    break

    m = re.search(r'Author\s*[:\-]?\s*(.+)', text, re.IGNORECASE)
    if m:
        author = m.group(1).strip().lstrip("-").strip()

    m = re.search(r'Usage\s*[:\-]?\s*(.+)', text, re.IGNORECASE)
    if m:
        usage = m.group(1).strip().lstrip("-").strip()

    m = re.search(r'Example[s]?\s*[:\-]?\s*(.+)', text, re.IGNORECASE)
    if m:
        example = m.group(1).strip().lstrip("-").strip()

    return desc, author, usage, example


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

    dl = desc.lower() + " " + name
    # Root directory - infer from name/desc
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
    if any(w in dl for w in ["session", "sid", "ses"]) and not any(w in dl for w in ["sql"]):
        return "Session Monitoring"
    if any(w in dl for w in ["explain", "xplan", "plan"]) and "sql" not in name:
        return "Execution Plans"
    if any(w in dl for w in ["sql_id", "sqlid", "cursor", "bind", "sql_text"]):
        return "SQL Analysis"
    if any(w in dl for w in ["baseline", "patch", "profile", "hint", "tuning"]):
        return "SQL Tuning"
    if any(w in dl for w in ["table", "index", "column", "partition", "lob", "segment", "object", "synonym", "sequence", "trigger", "procedure", "ddl", "describe"]):
        return "Object Information"
    if any(w in dl for w in ["sga", "pga", "memory", "buffer", "cache"]):
        return "Memory Management"
    if any(w in dl for w in ["tablespace", "datafile", "space", "storage"]):
        return "Space Management"
    if any(w in dl for w in ["parameter", "init", "config", "setting", "directory", "dblink", "redo", "log"]):
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


def infer_keywords(name, desc, category):
    """Generate keywords from script name, description, and category."""
    words = set()
    # From filename
    base = os.path.splitext(os.path.basename(name))[0]
    words.update(re.findall(r'[a-z]+', base.lower()))
    # From description
    if desc:
        words.update(w.lower() for w in re.findall(r'\b[a-z]{3,}\b', desc.lower())
                      if w not in {"the", "and", "for", "from", "with", "that", "this", "are", "was", "not", "but", "use", "can", "has", "its", "will", "all", "any", "may", "etc"})
    # From category
    words.update(w.lower() for w in re.findall(r'[a-z]+', category.lower()))
    return ", ".join(sorted(words))


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
    # Parse the well-documented catalog
    catalog_path = os.path.join(REPO, "SCRIPTS_CATALOG.txt")
    catalog = parse_catalog(catalog_path) if os.path.exists(catalog_path) else {}

    # Find all .sql files
    all_sql = []
    for pattern in ["*.sql", "**/*.sql"]:
        all_sql.extend(glob.glob(os.path.join(REPO, pattern), recursive=True))

    all_sql = sorted(set(all_sql))

    scripts = []
    seen = set()

    for filepath in all_sql:
        relpath = os.path.relpath(filepath, REPO)

        # Skip some non-script files
        if relpath.startswith("."):
            continue

        if relpath in seen:
            continue
        seen.add(relpath)

        # Check if in catalog
        cat_entry = catalog.get(relpath)
        if not cat_entry:
            # Try without path
            cat_entry = catalog.get(os.path.basename(relpath))

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
            category = normalize_category(infer_category(filepath, desc))
            entry = {
                "file": relpath,
                "name": os.path.basename(relpath),
                "category": category,
                "keywords": infer_keywords(relpath, desc, category),
                "purpose": desc,
                "syntax": usage if usage else f"@{relpath}",
                "parameters": "",
                "examples": example,
                "documented": False,
            }

        # Add directory info
        dirname = os.path.dirname(relpath)
        entry["directory"] = dirname if dirname else "root"

        scripts.append(entry)

    # Sort: documented first, then alphabetically
    scripts.sort(key=lambda s: (not s["documented"], s["category"], s["name"]))

    print(json.dumps(scripts, indent=2))


if __name__ == "__main__":
    main()
