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
                                 "from_time", "to_time", "dropping",
                                 "notes:", "note:", "todo", "warning", "prompt ",
                                 "this script uses", "running ", "attaching ",
                                 "for unix", "bug ", "experimental"))
            or d_lower.endswith((" from", " where", " and", " or", ",", "(", ";"))
            or re.search(r"&\w+|\|\||\bput_line\b|^\w+\.\w+,", desc)
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


VIEW_DESCRIPTIONS = {
    # V$ views
    "session": "active session information",
    "sql": "SQL statements in shared pool",
    "sqlstats": "SQL execution statistics",
    "sql_plan": "execution plans",
    "sql_plan_statistics_all": "execution plan runtime statistics",
    "sql_monitor": "SQL monitor data",
    "sql_shared_cursor": "child cursor sharing reasons",
    "sql_bind_capture": "captured bind variable values",
    "sql_workarea": "SQL workarea memory usage",
    "sql_workarea_active": "active SQL workareas",
    "process": "Oracle processes",
    "lock": "lock and enqueue information",
    "locked_object": "locked objects",
    "latch": "latch statistics",
    "latchholder": "current latch holders",
    "latch_children": "per-child latch statistics",
    "mutex_sleep": "mutex sleep events",
    "mutex_sleep_history": "mutex sleep history",
    "active_session_history": "active session history (ASH) samples",
    "event_name": "wait event definitions",
    "event_histogram": "wait event time histograms",
    "system_event": "system-wide wait event totals",
    "session_event": "per-session wait events",
    "session_wait": "current session waits",
    "sysstat": "system-wide statistics",
    "sesstat": "per-session statistics",
    "mystat": "current session statistics",
    "sysmetric": "system metrics",
    "sysmetric_summary": "system metric summary",
    "parameter": "database initialization parameters",
    "parameter2": "database parameters (expanded)",
    "spparameter": "spfile parameters",
    "sga": "SGA summary",
    "sga_dynamic_components": "dynamic SGA components",
    "sgastat": "detailed SGA memory breakdown",
    "pgastat": "PGA memory statistics",
    "pga_target_advice": "PGA target advisor",
    "db_cache_advice": "buffer cache advisor",
    "shared_pool_advice": "shared pool advisor",
    "diag_info": "diagnostic repository info",
    "db_object_cache": "cached library cache objects",
    "transaction": "active transactions",
    "tempseg_usage": "temp segment usage",
    "temp_space_header": "temporary tablespace space",
    "temporary_lobs": "temporary LOBs per session",
    "tablespace": "tablespaces",
    "datafile": "datafiles",
    "log": "online redo logs",
    "logfile": "redo log files",
    "archived_log": "archived redo logs",
    "open_cursor": "open cursors",
    "result_cache_objects": "result cache objects",
    "qmon_tasks": "queuing monitor tasks",
    "buffered_queues": "buffered queue stats",
    "aq": "advanced queuing",
    "asm_diskgroup": "ASM disk groups",
    "asm_disk": "ASM disks",
    "segment_statistics": "per-segment statistics",
    "filestat": "datafile I/O statistics",
    "filemetric": "datafile metrics",
    "iostat_file": "file I/O stats",
    "bh": "buffer headers",
    "instance": "instance info",
    "instance_cache_transfer": "RAC cache transfer stats",
    "cell_state": "Exadata cell state",
    "cell_config": "Exadata cell config",
    "px_session": "parallel execution sessions",
    "px_process": "parallel slave processes",
    "undostat": "undo statistics",
    "rollstat": "rollback segment statistics",
    "rollname": "rollback segment names",
    "cache_transfer": "block cache transfer stats",
    "fixed_table": "fixed tables (X$)",
    "database": "database info",
    "version": "Oracle version info",
    "license": "licensing info",
    "option": "installed options",
    "nls_parameters": "NLS session parameters",
    "nls_database_parameters": "NLS database parameters",
    "services": "database services",
    "active_services": "active services",
    "containers": "pluggable containers",
    "pdbs": "pluggable databases",
    "encrypted_tablespaces": "encrypted tablespaces",
    "log_history": "redo log switch history",
}

DBA_DESCRIPTIONS = {
    "tables": "table metadata",
    "tab_columns": "column metadata",
    "tab_cols": "column metadata",
    "indexes": "index metadata",
    "ind_columns": "index columns",
    "constraints": "table constraints",
    "segments": "segment storage",
    "extents": "segment extents",
    "data_files": "data file metadata",
    "tablespaces": "tablespace metadata",
    "users": "database users",
    "roles": "roles",
    "role_privs": "role grants",
    "sys_privs": "system privileges",
    "tab_privs": "object privileges",
    "objects": "database objects",
    "procedures": "procedures and functions",
    "triggers": "triggers",
    "views": "views",
    "synonyms": "synonyms",
    "sequences": "sequences",
    "directories": "directory objects",
    "db_links": "database links",
    "dependencies": "object dependencies",
    "tab_partitions": "table partitions",
    "tab_subpartitions": "table subpartitions",
    "ind_partitions": "index partitions",
    "tab_histograms": "column histograms",
    "tab_stats_history": "statistics history",
    "sql_plan_baselines": "SQL plan baselines",
    "sql_patches": "SQL patches",
    "sql_profiles": "SQL profiles",
    "sql_translations": "SQL translations",
    "hist_snapshot": "AWR snapshots",
    "hist_active_sess_history": "historical ASH samples",
    "hist_sql_plan": "historical execution plans",
    "hist_sqlstat": "historical SQL statistics",
    "hist_sqltext": "historical SQL text",
    "hist_sysstat": "historical system statistics",
    "hist_system_event": "historical wait events",
    "scheduler_jobs": "scheduled jobs",
    "jobs": "legacy DBMS_JOB jobs",
    "audit_trail": "audit trail entries",
    "lobs": "LOB segment metadata",
    "mviews": "materialized views",
    "recyclebin": "recycled objects",
}


def describe_view(view_name):
    """Map a V$/X$/DBA_ view to a short human description."""
    v = view_name.lower()
    if v.startswith(("gv$", "v$")):
        base = v.split("$", 1)[1]
        if base in VIEW_DESCRIPTIONS:
            return f"`{view_name}` ({VIEW_DESCRIPTIONS[base]})"
        return f"`{view_name}`"
    if v.startswith("dba_"):
        base = v[4:]
        if base in DBA_DESCRIPTIONS:
            return f"`{view_name}` ({DBA_DESCRIPTIONS[base]})"
        return f"`{view_name}` (data dictionary)"
    if v.startswith(("all_", "user_")):
        return f"`{view_name}` (data dictionary)"
    if v.startswith("x$"):
        return f"`{view_name}` (internal fixed table)"
    return f"`{view_name}`"


def strip_sql_comments(text):
    """Remove -- and /* */ comments and single-quoted strings from SQL.

    Preserves double-quoted identifiers (e.g. "_serial_direct_read"), which
    are not strings in Oracle SQL.
    """
    text = re.sub(r'/\*.*?\*/', ' ', text, flags=re.DOTALL)
    text = re.sub(r'--[^\n]*', ' ', text)
    text = re.sub(r"'[^']*'", " '' ", text)
    return text


def generate_description(filepath):
    """Analyze SQL content and synthesize a one-sentence description.

    Returns (description, True) if generated successfully, or (None, False).
    """
    lines = read_lines(filepath, 200)
    if not lines:
        return None

    # Keep only non-blank, non-comment lines for structural analysis
    code_lines = []
    for line in lines:
        s = line.strip()
        if not s or s.startswith("--") or s.startswith("/*"):
            continue
        code_lines.append(s)

    if not code_lines:
        return "Empty or placeholder script (header comments only)."

    raw = "\n".join(code_lines)
    sql = strip_sql_comments(raw).lower()

    # --- Early check: demo/lab script (CREATE TABLE + multiple ops) ---
    # If script creates test tables and also has DML or ALTER SYSTEM,
    # describe as a demo first, since the admin commands are incidental.
    has_ct = bool(re.search(r'\bcreate\s+table\b', sql))
    has_dml = bool(re.search(r'\binsert\s+into\b|\bupdate\s+\w+\s+set\b|\bdelete\s+from\b', sql))
    if has_ct and has_dml:
        return "Creates and populates test tables for a demonstration scenario."

    # --- Pattern: wrapper script @@other or @$SQLPATH/... ---
    first = code_lines[0].lstrip()
    m = re.match(r'^@@?([\w/]+)', first)
    if m and len(code_lines) <= 3:
        wrapped = m.group(1)
        return f"Thin wrapper that calls `@{wrapped}` with formatted parameters."
    m = re.match(r'^@[&\$]?[\w/_]*?/([\w_]+)', first)
    if m and len(code_lines) <= 3:
        wrapped = m.group(1)
        return f"Thin wrapper that calls the external `{wrapped}` script under SQLPATH."

    # --- Pattern: oradebug command ---
    m = re.search(r'\boradebug\s+([a-z_]+(?:\s+[a-z_$]+)?)', sql)
    if m:
        cmd = m.group(1).strip()
        return f"Runs `oradebug {cmd}` for diagnostic output."

    # --- Pattern: ALTER SESSION SET ... ---
    m = re.search(r'alter\s+session\s+set\s+"?([\w_]+)"?\s*=', sql)
    if m:
        param = m.group(1)
        return f"Alters current session parameter `{param}`."

    m = re.search(r'alter\s+session\s+set\s+events\b', sql)
    if m:
        return "Enables or disables a diagnostic event at the session level."

    # --- Pattern: ALTER SYSTEM SET ---
    m = re.search(r'alter\s+system\s+set\s+"?([\w_]+)"?\s*=', sql)
    if m:
        return f"Alters instance parameter `{m.group(1)}`."

    if re.search(r'alter\s+system\s+(kill|cancel|disconnect|flush|checkpoint|switch)', sql):
        m = re.search(r'alter\s+system\s+(kill|cancel|disconnect|flush|checkpoint|switch)\s+(\w+)?', sql)
        action = m.group(1) if m else "admin"
        tail = m.group(2) if m and m.group(2) else ""
        return f"Runs `ALTER SYSTEM {action}{' ' + tail if tail else ''}` command."

    # --- Pattern: DBMS package call ---
    m = re.search(r'\b(?:exec(?:ute)?\s+|begin\s+)?(dbms_\w+(?:\.\w+)?)', sql)
    if m and ("exec" in sql or "begin" in sql or "call" in sql):
        proc = m.group(1)
        return f"Calls `{proc}` procedure."

    # --- Pattern: pure SQL*Plus configuration ---
    config_prefixes = ("set ", "col ", "column ", "break ", "compute ", "ttitle ",
                        "btitle ", "repheader ", "define ", "def ", "spool ",
                        "clear ", "prompt", "pause", "accept ", "host ")
    if all(cl.lower().startswith(config_prefixes) for cl in code_lines):
        return "SQL*Plus configuration and formatting commands."

    # --- Pattern: ALTER SESSION FORCE PARALLEL / ENABLE/DISABLE ---
    m = re.search(r'alter\s+session\s+(force|enable|disable)\s+([^\n;]{1,80})', sql)
    if m:
        mode = m.group(1)
        target = re.sub(r'\s+', ' ', m.group(2)).strip()[:50]
        return f"Runs `ALTER SESSION {mode.upper()} {target.upper()}`."

    # --- Pattern: CREATE/REPLACE PROCEDURE / FUNCTION / PACKAGE / TRIGGER ---
    m = re.search(r'create\s+(?:or\s+replace\s+)?(procedure|function|package|trigger|type)\s+(\w+)', sql)
    if m:
        kind = m.group(1)
        name = m.group(2)
        return f"Creates the `{name}` {kind} used in demonstrations."

    # --- Pattern: DML-heavy script (demo / lab) ---
    has_delete = bool(re.search(r'\bdelete\s+from\b', sql))
    has_update = bool(re.search(r'\bupdate\s+\w+\s+set\b', sql))
    has_lock_table = bool(re.search(r'\block\s+table\b', sql))
    has_commit = bool(re.search(r'\bcommit\b', sql))
    if sum([has_delete, has_update, has_lock_table]) >= 1 and not re.search(r'\bselect\b', sql):
        parts = []
        if has_lock_table:
            parts.append("locks")
        if has_delete:
            parts.append("deletes")
        if has_update:
            parts.append("updates")
        action = "/".join(parts)
        return f"DML demo script that {action} rows (often paired with hang/lock scenarios)."

    # --- Pattern: SQL fragment / continuation snippet ---
    first_line = code_lines[0].strip().lower()
    if first_line.startswith(("and ", "or ", "where ", "having ", "order by ", ",")):
        return "SQL fragment appended to another query at runtime."

    # --- Pattern: SELECT aggregate from dynamic table (&N) ---
    m = re.search(r'select\s+(count|sum|avg|min|max)\s*\(', sql)
    if m and re.search(r'from\s+&\d', sql):
        fn = m.group(1).upper()
        return f"Runs `SELECT {fn}(...)` against a user-supplied table name."

    # --- Pattern: SELECT * FROM &1 ---
    if re.search(r'select\s+\*\s+from\s+&\d', sql):
        return "Dumps all rows from a user-supplied table name."

    # --- Pattern: DESCRIBE &1 ---
    if re.search(r'^\s*describe\s+&\d', sql, re.MULTILINE):
        return "Describes the structure of a user-supplied object."

    # --- Pattern: HTML/markup wrapper (SQL*Plus output to HTML) ---
    if "markup html" in sql and "spool" in sql:
        return "SQL*Plus wrapper that spools query output to a formatted HTML file."

    # --- Pattern: store set / saved set ---
    if "store set" in sql:
        return "Saves current SQL*Plus session settings for later restore."
    m = re.search(r'@\s*"?&?_?tpt_tempdir/set_', raw)
    if m or re.search(r'@["\']?[^"\'\n]*?/set_&', raw):
        return "Restores previously saved SQL*Plus session settings."

    # --- Pattern: HOST shell wrapper ---
    if code_lines and code_lines[0].upper().startswith("HOST "):
        return "Shell helper that generates and runs a temporary SQL fragment."

    # --- Pattern: UNDEFINE substitution variables ---
    if re.search(r'\bundef(?:ine)?\s+\d', sql):
        return "Undefines SQL*Plus substitution variables (numeric positional params)."

    # --- Pattern: runs a user-supplied script (@&N alone) ---
    if re.match(r'^\s*@&\d\s*$', raw.strip()):
        return "Runs a user-supplied script file (simple @ pass-through)."

    # --- Pattern: spool + execute + spool off ---
    if "spool" in sql and re.search(r'@\s*&\d', raw):
        return "Spools the output of a user-supplied script to a file and opens it."

    # --- Pattern: DISTINCT / GROUP BY on user table ---
    if re.search(r'select\s+distinct\s+&\d', sql, re.DOTALL):
        return "Shows distinct values of a user-supplied column from a user-supplied table."
    if re.search(r'select\s+&\d.*count\s*\(.*from\s+&\d.*group\s+by', sql, re.DOTALL):
        return "Counts rows in a user-supplied table grouped by a user-supplied column."

    # --- Pattern: incomplete/stub SQL (SELECT without real FROM) ---
    if re.search(r'\bselect\b', sql) and not re.search(r'from\s+\S', sql):
        return "Incomplete or stub SELECT statement (work-in-progress)."

    # --- Pattern: uses DBMS_ROWID / rowid math ---
    if "dbms_rowid" in sql:
        return "Decodes ROWIDs into file#/block#/row# for physical block lookup."

    # --- Pattern: Snapper measurement wrapper ---
    if "@snapper" in sql:
        return "Measures session activity around a user-supplied command using Snapper."

    # Oracle hint names that look like views but aren't
    HINT_NAMES = {
        "all_rows", "first_rows", "rule", "choose", "cpu_costing",
    }

    # --- Pattern: SELECT from view(s) ---
    views = re.findall(r'from\s+((?:sys\.)?(?:g?v\$|x\$|dba_|all_|user_)[\w_$]+)', sql)
    views = [v for v in views if v.lower() not in HINT_NAMES]
    views = list(dict.fromkeys(views))

    # Also find joined views (after comma or join keyword)
    joined = re.findall(r'[,\n]\s*((?:sys\.)?(?:g?v\$|x\$|dba_|all_|user_)[\w_$]+)', sql)
    for v in joined:
        if v.lower() not in HINT_NAMES and v not in views:
            views.append(v)

    has_where_param = bool(re.search(r'where[^;(]*&\d', sql))
    has_group_by = bool(re.search(r'\bgroup\s+by\b', sql))
    has_order_by = bool(re.search(r'\border\s+by\b', sql))
    has_top_n = bool(re.search(r'(rownum\s*<=|fetch\s+first|top\s+\d)', sql))
    has_aggregate = bool(re.search(r'\b(count|sum|avg|max|min)\s*\(', sql))

    # --- Pattern: DDL/DML demo scripts ---
    has_create_table = bool(re.search(r'\bcreate\s+table\b', sql))
    has_insert = bool(re.search(r'\binsert\s+into\b', sql))
    has_drop_table = bool(re.search(r'\bdrop\s+table\b', sql))
    has_create_user = bool(re.search(r'\bcreate\s+user\b', sql))
    has_drop_user = bool(re.search(r'\bdrop\s+user\b', sql))

    if has_create_user or has_drop_user:
        return "Creates or drops test users (demo setup/cleanup)."

    if has_create_table and has_insert:
        return "Creates and populates test tables for a demonstration scenario."

    if has_create_table:
        return "Creates test tables for a demonstration scenario."

    if has_drop_table and not views:
        return "Drops test objects (demo cleanup script)."

    # --- Build description from views ---
    if views:
        main = views[0]
        main_desc = describe_view(main)

        action = "Queries"
        if has_top_n:
            action = "Shows top rows from"
        elif has_aggregate and has_group_by:
            action = "Aggregates"

        suffix_parts = []
        if has_where_param:
            suffix_parts.append("filtered by user-supplied value")
        if has_group_by and not (has_aggregate and "aggregat" in action.lower()):
            suffix_parts.append("grouped")
        if has_order_by and has_top_n:
            suffix_parts.append("ordered")

        if len(views) > 1:
            others = ", ".join(f"`{v}`" for v in views[1:4])
            suffix_parts.insert(0, f"joined with {others}")

        suffix = (", " + "; ".join(suffix_parts)) if suffix_parts else ""
        return f"{action} {main_desc}{suffix}."

    # --- Pattern: SELECT against regular tables (demo/lab scripts) ---
    # Look for FROM <identifier> that isn't a system view
    sel_count = len(re.findall(r'\bselect\b', sql))
    if sel_count >= 1:
        # Find regular (non-system) tables referenced in FROM
        tables = re.findall(r'from\s+([a-z_][\w]*)', sql)
        tables = [t for t in tables if not t.startswith(("v$", "gv$", "x$", "dba_", "all_", "user_", "dual"))]
        tables = list(dict.fromkeys(tables))[:3]
        has_hint = bool(re.search(r'/\*\+', sql))
        has_xplan = bool(re.search(r'@xall|@xb|@xi\b', raw))

        if tables:
            table_str = ", ".join(f"`{t}`" for t in tables)
            if has_xplan and has_hint:
                return f"Demo script: runs hinted queries against {table_str} and displays execution plans."
            if has_xplan:
                return f"Demo script: runs queries against {table_str} and displays execution plans."
            if has_hint:
                return f"Demo script: runs hinted SQL against {table_str}."
            return f"Demo or test script: queries {table_str}."

    # --- Pattern: single SELECT from dual (utility) ---
    if re.search(r'from\s+dual\b', sql):
        if re.search(r'to_char\s*\(.*date', sql) or re.search(r'sysdate', sql):
            return "Calculates or formats a date/time value."
        if re.search(r'dbms_utility\.', sql):
            return "Calls a DBMS_UTILITY function from dual."
        return "Computes a value using SELECT FROM dual."

    # --- Pattern: PL/SQL anonymous block with heavy loop ---
    if re.search(r'^\s*(declare|begin)\b', sql):
        if re.search(r'\bloop\b|\bfor\s+\w+\s+in\b', sql):
            return "Anonymous PL/SQL block running a loop for benchmarking or load generation."
        return "Anonymous PL/SQL block."

    # --- Pattern: empty/stub file (license only) ---
    if not code_lines:
        return "Empty placeholder script (header only)."

    # --- Fallback: couldn't determine ---
    return None


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


# The 12 canonical categories (shared with tools/ai_describe.py).
CATEGORIES = [
    "Session & Process", "SQL & Execution Plans", "Waits, Locks & Latches",
    "ASH Analysis", "AWR & History", "Memory", "Objects & Storage",
    "Instance & Configuration", "Tracing & Diagnostics", "Exadata",
    "Demos & Experiments", "SQL*Plus Utilities",
]

# Legacy category names (from SCRIPTS_CATALOG.txt and infer_category) -> canonical.
# Matched on the part before " / " so sub-categories collapse too.
CATEGORY_MAP = {
    "ash analysis": "ASH Analysis",
    "awr analysis": "AWR & History", "awr": "AWR & History", "statspack": "AWR & History",
    "memory management": "Memory",
    "object information": "Objects & Storage", "space management": "Objects & Storage",
    "statistics": "Objects & Storage",
    "performance monitoring": "Session & Process", "performance profiling": "Session & Process",
    "session monitoring": "Session & Process", "session management": "Session & Process",
    "transaction monitoring": "Session & Process", "system monitoring": "Session & Process",
    "parallel execution": "Session & Process",
    "sql analysis": "SQL & Execution Plans", "sql monitoring": "SQL & Execution Plans",
    "sql tuning": "SQL & Execution Plans", "execution plans": "SQL & Execution Plans",
    "advanced sql tuning": "SQL & Execution Plans", "in-memory": "SQL & Execution Plans",
    "lock analysis": "Waits, Locks & Latches", "wait analysis": "Waits, Locks & Latches",
    "system configuration": "Instance & Configuration", "rac / cluster": "Instance & Configuration",
    "scheduler / jobs": "Instance & Configuration", "user management": "Instance & Configuration",
    "setup / configuration": "Instance & Configuration",
    "tracing / diagnostics": "Tracing & Diagnostics", "tracing & diagnostics": "Tracing & Diagnostics",
    "advanced oracle troubleshooting": "Tracing & Diagnostics",
    "exadata": "Exadata",
    "demos": "Demos & Experiments", "experiments": "Demos & Experiments",
    "bug test cases": "Demos & Experiments",
    "utility": "SQL*Plus Utilities", "tools / utilities": "SQL*Plus Utilities",
    "error handling": "SQL*Plus Utilities", "deprecated": "SQL*Plus Utilities",
}


def normalize_category(cat):
    if cat in CATEGORIES:
        return cat
    key = (cat or "").lower().split(" / ")[0].strip()
    return CATEGORY_MAP.get(key) or CATEGORY_MAP.get((cat or "").lower().strip()) or "SQL*Plus Utilities"


def load_ai_cache():
    path = os.path.join(REPO, ".ai_descriptions.json")
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)


def file_hash(filepath):
    import hashlib
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def params_from_ai(params):
    return ", ".join(
        f"&{p['n']}: {p['name']}" + (f" ({p['desc']})" if p.get("desc") else "")
        for p in params
    )


def syntax_from_ai(relpath, params):
    base = f"@{relpath}"
    if not params:
        return base
    return base + " " + " ".join(f"<{p['name']}>" for p in params)


NONE_VALUES = {"none", "n/a", "-", "na"}
FIX_STATS = {"syntax": 0, "examples": 0, "wrapper_skipped": 0, "samples": []}
INVOKE_RE = re.compile(r"^(@@?)([A-Za-z0-9_$./\\-]+)")


def clean_text_field(val):
    """Normalize placeholder values to '' and strip common leading indentation."""
    val = (val or "").strip("\n")
    if val.strip().lower() in NONE_VALUES:
        return ""
    lines = val.rstrip().split("\n")
    if len(lines) > 1:
        def ind(l):
            return len(l) - len(l.lstrip())
        rest = [l for l in lines[1:] if l.strip()]
        if rest:
            m = min(ind(l) for l in rest)
            if ind(lines[0]) == 0 and m > 0:
                first = lines[0].lstrip()[:1]
                if first and all(l.lstrip()[:1] == first for l in rest if ind(l) == m):
                    lines = [lines[0]] + [l[m:] if l.strip() else l for l in lines[1:]]
            elif ind(lines[0]) > 0:
                m = min(ind(l) for l in lines if l.strip())
                lines = [l[m:] if l.strip() else l for l in lines]
    return "\n".join(l.rstrip() for l in lines).strip()


def correct_token(entry, token, allow_rename):
    """Return the corrected invocation token for this script, or None."""
    own_dir = os.path.dirname(entry["file"])
    own_base = entry["name"][:-4] if entry["name"].lower().endswith(".sql") else entry["name"]
    ext = ".sql" if token.lower().endswith(".sql") else ""
    t = token[:-4] if ext else token
    tdir, tbase = os.path.split(t)
    tdir = tdir[2:] if tdir.startswith("./") else tdir
    if tbase.lower() != own_base.lower():
        if not allow_rename or not re.fullmatch(r"[A-Za-z0-9_$]+", tbase or ""):
            return None
    elif tdir == own_dir and tbase == own_base:
        return None
    new = (own_dir + "/" if own_dir else "") + own_base + ext
    return new if new != token else None


def fix_invocations(entry):
    """Rewrite wrong @script invocations in syntax/examples (deterministic)."""
    for f in ("purpose", "syntax", "parameters", "examples"):
        entry[f] = clean_text_field(entry.get(f, ""))
    is_wrapper = entry.get("kind") == "wrapper"
    own_base = entry["name"][:-4]
    m = INVOKE_RE.match(entry["syntax"])
    if m:
        tok = m.group(2)
        tb = os.path.basename(tok[:-4] if tok.lower().endswith(".sql") else tok)
        new = correct_token(entry, tok, True)
        rest = entry["syntax"][m.end():]
        if new and is_wrapper and tb.lower() != own_base.lower() and (
                re.search(r"&\d", rest) or not re.search(r"<\w", rest)):
            # Syntax is the wrapped call copied from the body, not this script's
            # usage: rebuild it from the parameter names instead.
            names = re.findall(r"^\s*(?:-\s*|&\d+:\s*)(\w+)", entry["parameters"], re.M)
            names += re.findall(r",\s*&\d+:\s*(\w+)", entry["parameters"])
            old = entry["syntax"]
            entry["syntax"] = " ".join(["@" + new.removesuffix(".sql")] + [f"<{n}>" for n in names])
            FIX_STATS["wrapper_rebuilt"] = FIX_STATS.get("wrapper_rebuilt", 0) + 1
            FIX_STATS["samples"].append((entry["file"], old, entry["syntax"]))
            new = None
        if new:
            old = entry["syntax"]
            entry["syntax"] = m.group(1) + new + old[m.end():]
            FIX_STATS["syntax"] += 1
            FIX_STATS["samples"].append((entry["file"], old, entry["syntax"]))
    out = []
    for line in entry["examples"].split("\n"):
        mm = re.match(r"^(\s*(?:--+\s*)?)(@@?)([A-Za-z0-9_$./\\-]+)", line)
        if mm:
            tok = mm.group(3)
            tb = os.path.basename(tok[:-4] if tok.lower().endswith(".sql") else tok)
            if tb.lower() == own_base.lower():
                new = correct_token(entry, tok, False)
                if new:
                    old = line
                    line = mm.group(1) + mm.group(2) + new + line[mm.end():]
                    FIX_STATS["examples"] += 1
                    FIX_STATS["samples"].append((entry["file"], old.strip(), line.strip()))
        out.append(line)
    entry["examples"] = "\n".join(out)


# ---------------------------------------------------------------------------
# Call graph (calls / called_by) and requirement tags (requires)
# ---------------------------------------------------------------------------

def _read_text(filepath):
    try:
        with open(filepath, "r", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


_LINE_CMT_RE = re.compile(r"^[ \t]*(?:rem(?:ark)?|prompt|pro)(?:[ \t].*|)$", re.I)


def _drop_sqlplus_comment_lines(text):
    """Blank out SQL*Plus REM / PROMPT lines (prompt may continue with a trailing '-')."""
    out = []
    cont = False
    for line in text.split("\n"):
        if cont:
            cont = line.rstrip().endswith("-")
            out.append("")
            continue
        if _LINE_CMT_RE.match(line):
            cont = line.rstrip().endswith("-") and re.match(r"^[ \t]*(prompt|pro)\b", line, re.I) is not None
            out.append("")
        else:
            out.append(line)
    return "\n".join(out)


def _tokenize_sql(text, keep_strings, multiline_strings):
    """Strip -- and /* */ comments (and optionally string literals) from SQL.

    Newlines are preserved so line structure survives.  With
    multiline_strings=False an unterminated quote ends at end of line, which
    keeps a stray apostrophe in a SQL*Plus command line from swallowing the
    rest of the file.
    """
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        two = text[i:i + 2]
        if two == "--":
            j = text.find("\n", i)
            i = n if j < 0 else j
        elif two == "/*":
            j = text.find("*/", i + 2)
            seg = text[i:] if j < 0 else text[i:j + 2]
            out.append("\n" * seg.count("\n") + " ")
            i = n if j < 0 else j + 2
        elif c in "qQ" and text[i + 1:i + 2] == "'" and i + 2 < n and text[i + 2] in "[{(<!|/#~^" \
                and (i == 0 or not (text[i - 1].isalnum() or text[i - 1] in "_$#")):
            op = text[i + 2]
            cl = {"[": "]", "{": "}", "(": ")", "<": ">"}.get(op, op)
            j = text.find(cl + "'", i + 3)
            end = n if j < 0 else j + 2
            seg = text[i:end]
            out.append(seg if keep_strings else "'' " + "\n" * seg.count("\n"))
            i = end
        elif c == "'":
            j = i + 1
            while j < n:
                if text[j] == "'":
                    if text[j + 1:j + 2] == "'":
                        j += 2
                        continue
                    break
                if text[j] == "\n" and not multiline_strings:
                    j -= 1
                    break
                j += 1
            end = min(j + 1, n)
            seg = text[i:end]
            out.append(seg if keep_strings else "'' " + "\n" * seg.count("\n"))
            i = end
        else:
            out.append(c)
            i += 1
    return "".join(out)


_MAYBE_CALL_RE = re.compile(r"^[ \t]*(@@?)[ \t]*(\S+)|^[ \t]*(?:start|sta)[ \t]+(?!with\b)()(\S+)", re.I | re.M)
_ADMIN_DIAG_RE = re.compile(r"^[ \t]*@@?[ \t]*\?[/\\]rdbms[/\\]admin[/\\](?:awr|ash|addm)\w*", re.I | re.M)

# Hard-coded requirement patterns (applied to lowercase, comment-stripped text)
_REQ_DIAG = re.compile(
    r"\bg?v\$active_session_history\b|\b(?:dba|cdb)_hist_\w+|\bdbms_workload_repository\b|"
    r"\bdbms_addm\b|\bdba_addm_\w+")
_REQ_TUNING = re.compile(
    r"\bdbms_sqltune\b|\bdbms_sql_monitor\b|\bg?v\$sql_monitor\w*|\bg?v\$sql_plan_monitor\b|\bdba_sqltune_\w+")
_REQ_X = re.compile(r"\bx\$\w+")
_REQ_SYSDBA = re.compile(r"\boradebug\b")

_TBL = r"[\w.$\"@]+"
_CHANGES = [
    ("alter system", re.compile(r"\balter\s+system\b")),
    ("kill/disconnect session", re.compile(r"\b(?:kill|disconnect)\s+session\b")),
    ("ddl", re.compile(
        r"\b(?:create|drop|truncate|alter)\s+(?:or\s+replace\s+)?(?:(?:unique|bitmap|public|global\s+temporary|"
        r"private\s+temporary|materialized|force|editionable|noneditionable)\s+)*"
        r"(?:table|index|user|procedure|package|view|trigger|directory|sequence|synonym)\b")),
    ("insert", re.compile(r"\binsert\s+(?:all\s+)?into\s+(" + _TBL + r")")),
    ("update", re.compile(r"\bupdate\s+(" + _TBL + r")\s+(?:\w+\s+)?set\b")),
    ("delete", re.compile(r"\bdelete\s+from\s+(" + _TBL + r")|^\s*delete\s+(" + _TBL + r")\s*(?:where\b|;)", re.M)),
    ("merge", re.compile(r"\bmerge\s+into\s+(" + _TBL + r")")),
    ("grant/revoke", re.compile(r"(?:^|;)[ \t]*(?:grant|revoke)\s+[\w ,$]+?\s+(?:on|to|from)\b", re.M)),
    ("dbms_spm/sqldiag", re.compile(
        r"\bdbms_spm\.(?!display)\w+|"
        r"\bdbms_sqldiag(?:_internal)?\.\w*(?:create|drop|alter|import|load|pack|unpack|evolve|accept|configure|set)\w*")),
    ("dbms_sqltune change", re.compile(
        r"\bdbms_sqltune\.\w*(?:create|drop|alter|import|accept|execute_tuning|set_|update_|load|unpack|pack|remove|reset|cancel|resume)\w*")),
    ("dbms_stats", re.compile(
        r"\bdbms_stats\.(?:gather|set_|delete|lock|unlock|export|import|restore|copy|create|drop|publish|flush|"
        r"purge|reset|alter|transfer|prepare)\w*")),
    ("dbms_scheduler", re.compile(r"\bdbms_scheduler\.(?:create|drop)\w*")),
]
_EXEC_IMM = re.compile(r"\bexecute\s+immediate\b")
_TEMP_TARGET = re.compile(r"temp|tmp|gtt|plan_table|^:|^table\($|^\(")


def _requires_own(clean_str, clean_nostr, with_str_raw):
    """Own (non-propagated) requirement tags from comment-stripped lowercase text."""
    tags = set()
    why = {}
    for tag, rx in (("diag_pack", _REQ_DIAG), ("tuning_pack", _REQ_TUNING),
                    ("x$", _REQ_X), ("sysdba", _REQ_SYSDBA)):
        m = rx.search(clean_str)
        if m:
            tags.add(tag)
            why[tag] = m.group(0)
    # TPT scripts that wrap Oracle's own AWR/ASH/ADDM report scripts
    if _ADMIN_DIAG_RE.search(with_str_raw):
        tags.add("diag_pack")
        why.setdefault("diag_pack", "@?/rdbms/admin/awr|ash|addm*")
    for label, rx in _CHANGES:
        for m in rx.finditer(clean_nostr):
            if label in ("insert", "update", "delete", "merge"):
                target = next((g for g in m.groups() if g), "")
                if _TEMP_TARGET.search(target):
                    continue
            tags.add("changes")
            why.setdefault("changes", m.group(0).strip()[:60])
            break
        if "changes" in tags:
            break
    if "changes" not in tags:
        for m in _EXEC_IMM.finditer(clean_nostr):
            # ignore EXECUTE IMMEDIATE 'alter session ...' (session-local); the string
            # literal is only visible in the string-preserving text
            tags.add("changes")
            why["changes"] = "execute immediate"
            break
    return tags, why


def _exec_imm_only_session(clean_str):
    """True if every EXECUTE IMMEDIATE targets a literal ALTER SESSION / SELECT / SET ROLE."""
    found = False
    for m in re.finditer(r"\bexecute\s+immediate\s*(.{0,40})", clean_str, re.S):
        found = True
        if not re.match(r"\(?\s*(?:q?'\s*(?:alter\s+session|select\b|set\s+role)\b)", m.group(1)):
            return False
    return found


def compute_call_graph_and_requires(scripts):
    """Annotate each script record with calls, called_by and requires."""
    by_path = {s["file"]: s for s in scripts}
    lower_map = {p.lower(): p for p in by_path}
    unresolved = {}
    own_tags, own_why = {}, {}

    def lookup(rel):
        rel = os.path.normpath(rel).replace(os.sep, "/")
        if rel in by_path:
            return rel
        return lower_map.get(rel.lower())

    for s in scripts:
        rel = s["file"]
        sdir = os.path.dirname(rel)
        raw = _drop_sqlplus_comment_lines(_read_text(os.path.join(REPO, rel)))
        for_calls = _tokenize_sql(raw, True, False)
        calls = []
        for m in _MAYBE_CALL_RE.finditer(for_calls):
            at, tok = (m.group(1), m.group(2)) if m.group(1) else ("@", m.group(4))
            if not tok or "&" in tok:
                continue
            tok = tok.strip("\"'")
            tok = re.sub(r"^(?:\$SQLPATH|\$\{SQLPATH\}|%SQLPATH%)[/\\]", "", tok, flags=re.I)
            tok = tok.rstrip(";").replace("\\", "/")
            if not tok or tok.startswith(("?", "$", "%", "http")) or "&" in tok:
                continue
            base = tok if re.search(r"\.\w+$", os.path.basename(tok)) else tok + ".sql"
            cands = []
            if at == "@@":
                cands = [os.path.join(sdir, base), base]
            else:
                cands = [base, os.path.join(sdir, base)]
            hit = None
            for c in cands:
                hit = lookup(c)
                if not hit and not c.lower().endswith(".sql"):
                    hit = lookup(c + ".sql")
                if hit:
                    break
            if hit:
                if hit != rel and hit not in calls:
                    calls.append(hit)
            else:
                unresolved.setdefault(tok, set()).add(rel)
        s["calls"] = calls

        low = raw.lower()
        clean_str = _tokenize_sql(low, True, True)
        clean_nostr = _tokenize_sql(low, False, True)
        tags, why = _requires_own(clean_str, clean_nostr, _tokenize_sql(raw, True, False))
        if "changes" in tags and why.get("changes") == "execute immediate" and _exec_imm_only_session(clean_str):
            tags.discard("changes")
            why.pop("changes", None)
        own_tags[rel], own_why[rel] = tags, why

    called_by = {p: [] for p in by_path}
    for s in scripts:
        for c in s["calls"]:
            called_by[c].append(s["file"])
    for s in scripts:
        s["called_by"] = sorted(called_by[s["file"]])

    # Transitive propagation (fixpoint => cycle-safe).  "changes" only flows
    # into wrapper callers.
    eff = {p: set(t) for p, t in own_tags.items()}
    changed = True
    while changed:
        changed = False
        for s in scripts:
            cur = eff[s["file"]]
            for c in s["calls"]:
                add = eff[c] if s["kind"] == "wrapper" else eff[c] - {"changes"}
                if not add <= cur:
                    cur |= add
                    changed = True
    for s in scripts:
        s["requires"] = sorted(eff[s["file"]])

    return unresolved, own_tags, own_why


def validate_workflows(scripts):
    """Warn (stderr) about workflows.js steps whose `file` is not in the index."""
    import sys
    path = os.path.join(REPO, "workflows.js")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r"^\s*//.*$", "", text, flags=re.M)
    known = {s["file"] for s in scripts}
    missing = [m for m in re.findall(r"\bfile\s*:\s*\"([^\"]+)\"", text) if m not in known]
    for m in missing:
        print(f"WARNING: workflows.js references {m!r}, which is not in the script index", file=sys.stderr)


def main():
    catalog_path = os.path.join(REPO, "SCRIPTS_CATALOG.txt")
    catalog = parse_catalog(catalog_path) if os.path.exists(catalog_path) else {}
    ai_cache = load_ai_cache()

    all_sql = glob.glob(os.path.join(REPO, "**", "*.sql"), recursive=True)
    all_sql = sorted(set(all_sql))

    scripts = []
    for filepath in all_sql:
        relpath = os.path.relpath(filepath, REPO)
        if any(part.startswith(".") for part in relpath.split(os.sep)):
            continue

        cat_entry = catalog.get(relpath)
        base = os.path.basename(relpath)
        # Bare-name catalog entries refer to the root script when one exists.
        if not cat_entry and not os.path.exists(os.path.join(REPO, base)):
            cat_entry = catalog.get(base)
        ai = ai_cache.get(relpath)
        if ai and (ai.get("hash") != file_hash(filepath) or "category" not in ai):
            ai = None  # stale (script changed) or old-schema record; ignore

        desc, author, usage, example = extract_header(filepath)
        rule_desc = None
        if not desc:
            rule_desc = generate_description(filepath)
        params_str = extract_parameters(filepath)

        entry = {
            "file": relpath,
            "name": os.path.basename(relpath),
            "documented": bool(cat_entry),
            "ai_generated": False,
            "generated": False,
        }

        # --- purpose / syntax / params / examples: curated > AI > header > rules
        if cat_entry:
            entry["purpose"] = cat_entry.get("purpose", "")
            entry["syntax"] = cat_entry.get("syntax", "")
            entry["parameters"] = cat_entry.get("parameters", "")
            entry["examples"] = cat_entry.get("examples", "")
        elif ai:
            entry["purpose"] = ai["purpose"]
            entry["ai_generated"] = True
            entry["parameters"] = params_from_ai(ai.get("params", [])) or params_str
            entry["syntax"] = (usage.split("\n")[0] if usage and "@" in usage
                               else syntax_from_ai(relpath, ai.get("params", [])))
            entry["examples"] = example
        else:
            entry["purpose"] = desc or rule_desc or ""
            entry["generated"] = bool(not desc and rule_desc)
            entry["parameters"] = params_str
            entry["syntax"] = infer_syntax(filepath, usage, params_str)
            entry["examples"] = example

        # --- category / kind: AI > curated > inferred
        if ai:
            entry["category"] = ai["category"]
            entry["kind"] = ai["kind"]
        elif cat_entry:
            entry["category"] = normalize_category(cat_entry.get("category", ""))
            entry["kind"] = "tool"
        else:
            entry["category"] = normalize_category(infer_category(filepath, entry["purpose"]))
            entry["kind"] = "tool"

        # --- keywords: curated + AI tags + extracted, deduped
        kws = []
        if cat_entry:
            kws += [k.strip() for k in cat_entry.get("keywords", "").split(",")]
        if ai:
            kws += ai.get("tags", [])
        kws += [k.strip() for k in extract_keywords(filepath, entry["purpose"], entry["category"]).split(",")]
        seen = set()
        entry["keywords"] = ", ".join(k for k in kws if k and not (k.lower() in seen or seen.add(k.lower())))[:400]

        dirname = os.path.dirname(relpath)
        entry["directory"] = dirname if dirname else "root"
        fix_invocations(entry)
        scripts.append(entry)

    unresolved, _own_tags, _own_why = compute_call_graph_and_requires(scripts)
    if os.environ.get("CALL_DEBUG_FILE"):
        with open(os.environ["CALL_DEBUG_FILE"], "w") as f:
            json.dump({"unresolved": {k: sorted(v) for k, v in unresolved.items()},
                       "own": {k: sorted(v) for k, v in _own_tags.items()},
                       "why": _own_why}, f)
    scripts.sort(key=lambda s: (not s["documented"], s["category"], s["name"]))
    import sys
    validate_workflows(scripts)
    print(f"fixed {FIX_STATS['syntax']} syntax lines, {FIX_STATS['examples']} example lines "
          f"(wrapper syntax rebuilt from params: {FIX_STATS.get('wrapper_rebuilt', 0)})", file=sys.stderr)
    if os.environ.get("FIX_VERBOSE"):
        for f, a, b in FIX_STATS["samples"]:
            print(f"  {f}: {a!r} -> {b!r}", file=sys.stderr)
    print(json.dumps(scripts, separators=(",", ":"), ensure_ascii=False))


if __name__ == "__main__":
    main()
