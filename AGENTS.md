# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project Overview

This is **Tanel Poder's Troubleshooting Scripts (TPT)** - a comprehensive collection of Oracle Database performance optimization and troubleshooting scripts. These are SQL*Plus scripts designed to work directly from SQL*Plus or SQL Developer without requiring any database changes or creation of database objects.

**Key Design Principles:**
- No database changes required (no tables, packages, or objects created)
- All processing done via SQL*Plus commands and anonymous PL/SQL blocks
- Queries V$ views (and X$ fixed tables in advanced mode)
- No traces enabled, no oradebug usage required
- Designed for restrictive change management environments

**Author:** Tanel Poder (tanel@tanelpoder.com)
**License:** Apache License 2.0
**Website:** https://tanelpoder.com

## Repository Structure

The repository contains a large SQL*Plus script library plus a small documentation and catalog layer.

### Core Directories

- **`/ash/`** - Active Session History (ASH) analysis scripts that sample GV$SESSION
  - `ashtop.sql` - Top activity by grouping ASH columns
  - `ash_wait_chains.sql` - Multi-session wait chains analysis
  - `asqlmon.sql` - SQL monitoring style execution plan drill-down
  - Note: These scripts do NOT require Diagnostics Pack licenses

- **`/awr/`** - Automatic Workload Repository (AWR) analysis scripts
  - `awr_sqlstats.sql` - SQL statistics from AWR
  - `awr_sqlstats_per_exec.sql` - SQL statistics per execution
  - `awr_sqlstats_unstable.sql` - Identify unstable execution plans

- **`/setup/`** - Installation and configuration scripts
  - `create_xviews.sql` - Create X$ table views for advanced analysis
  - `grant_snapper_privs.sql` - Grant necessary privileges for Snapper
  - `wordfile_*.txt` - SQL*Plus wordfiles for tab completion (11gR2, 12cR1, 18c)

- **`/tools/`** - Unix/Linux helper tools and utilities

- **Root directory** - 600+ individual SQL troubleshooting scripts

### Documentation and Catalog Files

- **`README.md`** - Main repository overview and getting-started page
- **`DOCUMENTATION_INDEX.md`** - Entry point for the docs set
- **`TPT_QUICK_REF.md`** - Short operator cheat sheet
- **`README_TPT_SEARCH.md`** - Canonical guide for `tpt-search.sh`
- **`SEARCH_GUIDE.md`** - Task-oriented search examples
- **`QUICKREF_*.md`** - Workflow-oriented reference guides

### Search and Directory Artifacts

There are two separate catalog layers in this repository. Do not treat them as interchangeable.

- **Curated CLI catalog**:
  - `tpt-search.sh` reads `SCRIPTS_CATALOG.txt`
  - `SCRIPTS_CATALOG.csv` is the spreadsheet export of that curated catalog
  - At the time of writing, `SCRIPTS_CATALOG.txt` contains 137 curated `SCRIPT:` entries
- **Interactive directory catalog**:
  - `directory.html` is the standalone interactive catalog UI
  - `scripts_data.js` is the dataset that powers `directory.html`, covering every `.sql` file in the repo
  - `build_directory.py` builds it by merging three sources, highest priority first:
    1. `SCRIPTS_CATALOG.txt` (curated purpose/syntax/examples)
    2. `.ai_descriptions.json` (Claude-generated purpose, category, kind, tags, params; committed cache keyed by file content hash)
    3. header comments and rule-based heuristics (offline fallback)
  - `tools/ai_describe.py` fills `.ai_descriptions.json` for new or changed scripts
  - Categories are a fixed list of 12 shared by `build_directory.py` and `tools/ai_describe.py`; `kind` is one of tool/wrapper/demo/fragment/setup/stub

If a task touches search, documentation, or catalog data, first determine which layer is being changed:

- `@help` and `tpt-search.sh` flow: curated CLI catalog
- `directory.html` interactive browsing flow: `scripts_data.js` + `build_directory.py`

## Key Scripts

### Essential Scripts

- **`snapper.sql`** - The flagship Session Snapper tool (v4.x)
  - Session-level performance measurement without requiring any DB changes
  - Supports ASH-style sampling, statistics, and RAC environments
  - Requires Oracle 10.1+ (v3.5 works on 9.2+)

- **`help.sql`** - Search and display help for TPT scripts
  - Usage: `@help <search_pattern>`
  - Example: `@help explain` or `@help lock|latch`

- **`init.sql`** - Initialize SQL*Plus environment with TPT settings
  - Sets linesize, pagesize, date formats, arraysize
  - Configures SQLPATH and temporary directories
  - Platform-specific settings (Unix/Mac/Windows)

- **`login.sql`** - Auto-executed on SQL*Plus login
  - Calls init.sql and i.sql for session setup

### Common Script Categories

1. **Session Monitoring:**
   - `s.sql` - Display current session wait and SQL_ID info
   - `ses.sql` - Session statistics filtered by statistic name
   - `usid.sql` - User session and process information

2. **SQL Analysis:**
   - `sqlid.sql` - Display SQL text, child cursors, execution stats
   - `sqlmon.sql` - Run SQL Monitor report
   - `x.sql`, `xa.sql`, `xi.sql` - Explain plan variants
   - `xawr.sql` - Explain plan from AWR

3. **Wait Analysis:**
   - `aw.sql` - Display last minute database activity
   - `sed.sql` - Wait events description
   - `evh.sql` - Histogram of wait counts
   - `lock.sql` - Display current locks

4. **Performance Profiling:**
   - `latchprof.sql` - Profile top latch holders
   - `mutexprof.sql` - Mutex profiling
   - `ostackprofu.sql` / `ostackprofw.sql` - Oracle process stack sampling (Unix/Windows)

5. **Object Information:**
   - `tab.sql` - Table information
   - `ind.sql` - Index information
   - `seg.sql` - Segment information
   - `descxx.sql` - Extended table column info
   - `o.sql` - Database objects by owner and name

6. **Space Management:**
   - `df.sql` / `dfm.sql` - Tablespace usage (GB/MB)
   - `topseg.sql` - Top space users per tablespace

7. **Memory & Performance:**
   - `sga.sql`, `sgastat.sql` - SGA information
   - `pga.sql` - PGA memory usage
   - `mem.sql` - Dynamic SGA components

8. **SQL Tuning:**
   - `create_sql_baseline.sql` - Create SQL Plan Baseline
   - `create_sql_patch.sql` - Create SQL patch with hints
   - `create_sql_profile.sql` - Create SQL profile

## Usage Patterns

### Environment Setup

The scripts expect the `SQLPATH` environment variable to be set to the TPT directory:

```bash
export SQLPATH=/path/to/tpt-oracle
sqlplus user/pass@db
```

On Windows:
```cmd
set SQLPATH=C:\path\to\tpt-oracle
sqlplus user/pass@db
```

### Script Invocation

Scripts are invoked with the `@` operator in SQL*Plus:

```sql
@scriptname parameter1 parameter2
```

Examples:
```sql
@help sql
@s 123
@sqlid 7q729nhdgtsqq 0
@ash/ashtop username,event2 1=1 sysdate-1/24 sysdate
@snapper ash=sql_id+event 5 12 all
```

### Common Parameters

- **SID filtering:** Many scripts accept SID parameters or filter expressions
  - Single: `123`
  - Multiple: `123,456,789`
  - Subquery: `"select sid from v$session where username='SOE'"`
  - Special: `all` for all sessions, `&mysid` for current session

- **Time ranges:** ASH/AWR scripts use Oracle date expressions
  - Predefined: `&min`, `&5min`, `&hour`, `&day`, `&today`
  - Explicit: `sysdate-1/24 sysdate` (last hour)
  - Timestamp: `"timestamp'2025-01-08 07:00:00'"`

- **Wildcards:** Object name patterns support `%` wildcard
  - `@tab soe.%` - All tables in SOE schema
  - `@o %.%files` - All objects ending with "files"

### Snapper Usage

The Session Snapper is the flagship tool with this syntax:

```sql
@snapper [ash|stats|all][,options] <seconds> <snapshots> <sid>
```

Options:
- `ash` - Sample session activity (default)
- `stats` - Capture statistics
- `all` - Both ASH and stats
- `gather=[s][t][w][l][e][b][a]` - What to gather (sessions, time, waits, latches, etc.)
- `pagesize=X` - Set page size
- `out` - Output formatting
- `trace` - Enable tracing

Examples:
```sql
@snapper ash 5 12 all
@snapper ash=sql_id+event 5 6 123,456
@snapper stats,gather=st 1 60 all
```

## Platform-Specific Notes

### Unix/Mac/Linux
- Uses `rm -f` for file deletion
- Uses `open` (Mac) or `xdg-open` (Linux) to open files
- Stack profiling: `@ostackprofu.sql`

### Windows
- Uses `del` for file deletion
- Uses `start` to open files
- Stack profiling: `@ostackprofw.sql`

Configure these in `init.sql` by uncommenting appropriate lines.

## Important Conventions

1. **No Database Modifications:** Scripts are read-only and make no schema changes
2. **Requires System Privileges:** Many scripts query V$ views and require appropriate grants
3. **License-Free ASH:** TPT's ASH functionality only samples GV$SESSION, not the licensed AWR repository
4. **Case Sensitivity:** Object names in filters typically need proper case or wildcards
5. **Output Format:** Scripts output is designed for Unix text tools and spreadsheet import

## Development Workflow

This is a script library, not an application to build. Typical workflow:

1. **Adding Scripts:** Create new .sql files following existing naming conventions
2. **Testing:** Test scripts directly in SQL*Plus against Oracle database
3. **Documentation:** Update `help.sql` with script descriptions and usage
4. **Platform Support:** Consider Unix/Mac/Windows compatibility

### Documentation Workflow

If you change repository docs:

1. Keep `README.md` and `DOCUMENTATION_INDEX.md` aligned with the actual repo layout
2. Use `/path/to/tpt-oracle` in user-facing shell examples, not machine-specific local paths
3. Keep shell examples in `bash` fences and SQL*Plus examples in `sql` fences

### Catalog Workflow

If you change the curated CLI catalog:

1. Edit `SCRIPTS_CATALOG.txt`
2. Keep `tpt-search.sh` help text aligned with the supported options
3. Regenerate `SCRIPTS_CATALOG.csv` with:

```bash
python3 tools/generate_search_catalog_csv.py
```

If you change the interactive directory:

1. Update `directory.html` for UI behavior or presentation
2. Update `build_directory.py` if merge or fallback rules change; update `tools/ai_describe.py` if the AI prompt or record shape changes (bump `SCHEMA_VERSION`)
3. Regenerate with `./rebuild.sh` (heuristics + cache only) or `./rebuild.sh --ai` (also classify new/changed scripts via the `claude` CLI). `./rebuild.sh --check` verifies `scripts_data.js` is current.
4. Commit `.ai_descriptions.json` together with `scripts_data.js`
5. Do not assume `SCRIPTS_CATALOG.txt` and `scripts_data.js` should have the same scope

## Common Tasks

### Finding the Right Script

```sql
@help <search_term>
```

### Analyzing Session Performance

```sql
-- Current session info
@s <sid>

-- Session statistics over time
@snapper ash 5 12 <sid>

-- Wait chains
@ash/ash_wait_chains username 1=1 sysdate-1/24 sysdate
```

### SQL Performance Analysis

```sql
-- Find SQL details
@sqlid <sql_id> 0

-- Explain plan
@xi <sql_id> 0

-- ASH-based execution breakdown
@ash/asqlmon <sql_id> 0 sysdate-1/24 sysdate
```

### Historical Analysis (AWR)

```sql
-- SQL stats from AWR
@awr/awr_sqlstats <sql_id> % sysdate-7 sysdate

-- System metrics
@awr/dstat sysdate-1 sysdate
```

## References

- YouTube: https://www.youtube.com/tanelpoder
- Twitter: https://twitter.com/tanelpoder
- Website: https://tanelpoder.com

## Technical Notes

- **Oracle Versions:** Most scripts work on Oracle 10g+, some on 9i+
- **RAC Support:** Snapper v4+ and many scripts support RAC (query GV$ views)
- **Privileges:** Requires SELECT on V$ views, possibly X$ tables for advanced features
- **DBMS_SYSTEM:** Some trace scripts require EXECUTE on DBMS_SYSTEM
- **Array Size:** Configured to 100 to avoid DBMS_OUTPUT 32k fetch limits
- **Long Datatype:** Set to 1MB for querying DBA_VIEWS, DBA_TRIGGERS
