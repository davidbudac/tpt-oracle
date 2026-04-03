# TPT Oracle Scripts - Documentation Gap Analysis

**Analysis Date:** 2026-01-12

## Executive Summary

This analysis identifies all TPT Oracle scripts that are NOT yet documented in `SCRIPTS_CATALOG.md` and related QUICKREF guides.

### Key Statistics

- **Total Scripts in Repository:** 794 (root + ash/ + awr/ directories)
- **Currently Documented:** 88 scripts
- **Undocumented:** 706 scripts
- **Documentation Coverage:** 11%

## Breakdown by Category

### High-Priority Categories (Most Useful for Users)

| Category | Count | Priority | Notes |
|----------|-------|----------|-------|
| **ASH Analysis** | 69 | HIGH | Many variants of ashtop, asqlmon, event histograms, wait chains |
| **Execution Plans** | 42 | HIGH | Multiple xplan variants (xm, xb, xp, xph, xpi, etc.) |
| **SQL Analysis & Cursors** | 26 | HIGH | SQL memory, optimization, execution tracking |
| **AWR Analysis** | 21 | MEDIUM | AWR event histograms, sysmetrics, sqlstats variants |
| **Object Information** | 24 | MEDIUM | Table/index/partition details, constraints, dependencies |
| **Parameters & Configuration** | 29 | MEDIUM | Parameter search, validation, system configuration |

### Specialized Categories

| Category | Count | Notes |
|----------|-------|-------|
| **Memory & Buffer Management** | 18 | Buffer cache analysis (bh_by_ts, bhla, bufprof) |
| **Tracing & Diagnostics** | 17 | Event tracing (10046, 10053), dumps, ostack profiling |
| **Space & Storage** | 22 | Tablespace usage, segment analysis |
| **System Statistics** | 10 | System-level statistics and monitoring |
| **ASM Management** | 5 | ASM diskgroups, files, dump utilities |
| **Lock/Latch/Mutex** | 5 | Latch profiling, mutex profiling |
| **Performance Profiling** | 4 | waitprof, bufprof, latchprof variants |
| **Session Monitoring** | 5 | Active session monitoring (a.sql, as.sql, asql.sql) |
| **Transaction & Undo** | 2 | Transaction and undo monitoring |
| **Redo & Archive Logs** | 4 | Redo log analysis |
| **Wait/Event Analysis** | 2 | Wait profiling tools |

### Utilities & Helper Scripts

| Category | Count | Notes |
|----------|-------|-------|
| **Utilities & Helpers** | 401 | Wide variety of small utility scripts |
| **Demo & Test Scripts** | 55 | aot/ directory examples and demos |

## Top Priority Scripts to Document

### 1. ASH Analysis Scripts (ash/ directory)

**High Value Scripts:**
- `ash/ashtop10.sql` - Top 10 ASH activity
- `ash/ashtopsum.sql` - ASH activity summary
- `ash/asqlmon12.sql` - SQL Monitor for 12c+
- `ash/asqlmonx.sql` - Extended SQL Monitor
- `ash/bash_wait_chains.sql` - Wait chains from ASH (beta)
- `ash/dashtop.sql` - DBA_HIST_ACTIVE_SESS_HISTORY top activity
- `ash/dasqlmon.sql` - SQL Monitor from DBA_HIST_ASH
- `ash/event_hist.sql` - Event histogram from ASH
- `ash/event_hist_micro.sql` - Microsecond event histogram
- `ash/shortmon.sql` - Short SQL execution monitoring
- `ash/sqlid_activity.sql` - Activity analysis by SQL_ID
- `ash/time_model.sql` - Time model analysis from ASH

### 2. Execution Plan Scripts

**High Value Scripts:**
- `xb.sql` - eXplain Better (enhanced execution plan)
- `xm.sql` - eXplain from Memory
- `xp.sql` - eXplain with Profile (SQL Monitor)
- `xph.sql` - eXplain with Profile HTML
- `xpi.sql` - eXplain with Profile by SQL_ID
- `xms.sql` - eXplain from Memory with Statistics
- `xmai.sql` - eXplain from Memory with aliases by SQL_ID
- `xplto.sql` - Show execution plan operations

### 3. SQL Analysis Scripts

**High Value Scripts:**
- `sql.sql` - Show SQL by hash value
- `sqlmemh.sql` - SQL shared pool memory by hash
- `sqlmemx.sql` - SQL shared pool memory by SQL_ID
- `sqlopt.sql` - Show cursor compilation environment
- `sqlflame.sql` - Flame chart for SQL execution
- `sqlfh.sql` - SQL Feature Hierarchy
- `sqlmon_restarts.sql` - SQL with restart issues
- `curheaps.sql` - Cursor heap analysis

### 4. AWR Analysis Scripts

**High Value Scripts:**
- `awr/dstat.sql` - System metrics with per-minute granularity
- `awr/awr_evh.sql` - AWR event histogram
- `awr/awr_sqlid.sql` - AWR SQL analysis by SQL_ID
- `awr/awr_sqlid_binds.sql` - AWR bind variable values
- `awr/awr_sqlstats_unstable.sql` - Detect unstable execution times
- `awr/awr_sysmetric_history.sql` - System metric history
- `awr/awr_sysstat.sql` - System statistics from AWR
- `awr/gen_awr_report.sql` - Generate AWR report

### 5. Session & Performance Monitoring

**High Value Scripts:**
- `a.sql` - Display CURRENT active sessions
- `as.sql` - Active sessions grouped by column
- `asql.sql` - Active sessions with current SQL
- `waitprof.sql` - Session Wait Profiler
- `bufprof.sql` - Buffer Get Profiler
- `latchprofx.sql` - Extended latch profiling

### 6. Object Information Scripts

**High Value Scripts:**
- `ind2.sql`, `indf.sql` - Extended index information
- `tab2.sql` - Extended table information
- `partmon.sql` - Partition monitoring
- `partpruning.sql` - Partition pruning analysis
- `segstat.sql`, `segstat2.sql` - Segment statistics
- `cons.sql`, `cons2.sql` - Constraint information
- `dep.sql` - Object dependencies

### 7. Memory & Buffer Analysis

**High Value Scripts:**
- `bufprof.sql` - Buffer Get Profiler
- `bhla.sql` - Buffer Headers by Latch Address
- `bh_by_ts.sql` - Buffer cache by tablespace
- `sgastatx.sql` - Extended SGA statistics
- `heap6.sql` - Heap analysis

### 8. Tracing & Diagnostics

**High Value Scripts:**
- `53on.sql` / `53off.sql` - Enable/disable 10053 trace
- `46on.sql` / `46off.sql` - Enable/disable 10046 trace
- `ostackprofu.sql` / `ostackprofw.sql` - OS stack profiling (Unix/Windows)
- `dumptrc.sql` - Dump trace files
- `diag.sql`, `diag_sid.sql` - Diagnostics information

## Recommendations

### Documentation Priority Levels

**Priority 1 - Immediate (Next 20-30 scripts):**
1. All main ASH variants (ashtop10, ashtopsum, dashtop, dasqlmon)
2. Most-used execution plan scripts (xb, xm, xp, xpi, xms)
3. Key SQL analysis scripts (sql.sql, sqlmemh, sqlmemx, sqlopt)
4. Top AWR scripts (dstat, awr_sqlstats_unstable, awr_evh)
5. Session monitoring scripts (a.sql, as.sql, asql.sql)

**Priority 2 - High Value (Next 50 scripts):**
1. Remaining ASH analysis variants
2. Memory/buffer profiling tools
3. Extended object information scripts
4. Tracing and diagnostic tools
5. Performance profiling scripts

**Priority 3 - Medium Value (Next 100 scripts):**
1. Specialized AWR analysis
2. Parameter and configuration scripts
3. Space and storage scripts
4. Remaining execution plan variants
5. Utility scripts with clear use cases

**Priority 4 - Low Priority:**
1. Demo and test scripts (aot/ directory)
2. Highly specialized or rarely used utilities
3. Legacy/deprecated script versions

### Documentation Strategy

1. **Start with High-Impact Categories:**
   - Focus on ASH, SQL Analysis, and Execution Plans first
   - These have the most user-facing value

2. **Group Similar Scripts:**
   - Document variants together (e.g., all xplan variants in one section)
   - Show progression from basic to advanced

3. **Include Usage Examples:**
   - Every script should have at least 1-2 examples
   - Show real troubleshooting scenarios

4. **Add Cross-References:**
   - Link related scripts (e.g., ash/ashtop → ash/ashtopsum)
   - Reference from documented to undocumented variants

5. **Create Category Guides:**
   - Expand QUICKREF guides for ASH, AWR, Memory, etc.
   - Add "script decision tree" for choosing right tool

## Quick Reference by Use Case

### "I need to analyze SQL performance"
**Undocumented scripts to add:**
- `sql.sql` - SQL details by hash
- `sqlmemh.sql`, `sqlmemx.sql` - Memory usage
- `sqlopt.sql` - Compilation environment
- `ash/sqlid_activity.sql` - ASH analysis by SQL_ID
- `ash/asqlmon12.sql` - Modern SQL Monitor

### "I need to explain execution plans"
**Undocumented scripts to add:**
- `xb.sql` - Better explain plan
- `xm.sql` - From memory
- `xms.sql` - With statistics
- `xp.sql`, `xpi.sql` - With SQL Monitor

### "I need to analyze ASH data"
**Undocumented scripts to add:**
- `ash/ashtop10.sql` - Top 10 activity
- `ash/ashtopsum.sql` - Summary view
- `ash/event_hist.sql` - Event histograms
- `ash/time_model.sql` - Time model breakdown

### "I need to check memory/buffer usage"
**Undocumented scripts to add:**
- `bufprof.sql` - Buffer profiler
- `bhla.sql` - Buffer headers
- `bh_by_ts.sql` - By tablespace

### "I need to trace/diagnose issues"
**Undocumented scripts to add:**
- `53on.sql`/`53off.sql` - CBO trace
- `ostackprofu.sql` - Stack profiling
- `diag.sql` - Diagnostics

## Files Generated by This Analysis

1. **UNDOCUMENTED_SCRIPTS_ANALYSIS.md** (790 lines)
   - Complete categorized list of all 706 undocumented scripts
   - With descriptions extracted from script headers
   - Organized into 20 categories

2. **UNDOCUMENTED_SCRIPTS_SUMMARY.md** (this file)
   - Executive summary and recommendations
   - Priority-based documentation roadmap
   - Quick reference by use case

## Next Steps

1. Review Priority 1 scripts (20-30 scripts)
2. Create detailed documentation entries for each
3. Add to SCRIPTS_CATALOG.md with:
   - Keywords
   - Purpose
   - Syntax
   - Examples (2-3 per script)
4. Update relevant QUICKREF_*.md guides
5. Add cross-references between related scripts
6. Consider consolidating very similar variants

---

**For complete detailed listing, see:** `UNDOCUMENTED_SCRIPTS_ANALYSIS.md`
