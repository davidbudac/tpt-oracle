# Priority Scripts to Document - Quick Reference

This is a curated list of the most important undocumented TPT scripts that should be added to SCRIPTS_CATALOG.md.

## Priority 1: Essential Scripts (Immediate Documentation)

### ASH Analysis - Most Used

| Script | Purpose | Similar To |
|--------|---------|------------|
| **ash/ashtop10.sql** | Show top 10 ASH activity (shorter output than ashtop) | ash/ashtop.sql (documented) |
| **ash/ashtopsum.sql** | ASH activity summary with aggregated stats | ash/ashtop.sql (documented) |
| **ash/asqlmon12.sql** | SQL Monitor for Oracle 12c+ with enhanced metrics | ash/asqlmon.sql (documented) |
| **ash/asqlmonx.sql** | Extended SQL Monitor with additional columns | ash/asqlmon.sql (documented) |
| **ash/dashtop.sql** | Top activity from DBA_HIST_ACTIVE_SESS_HISTORY (AWR ASH) | ash/ashtop.sql (documented) |
| **ash/dasqlmon.sql** | SQL Monitor analysis from DBA_HIST_ASH (historical) | ash/asqlmon.sql (documented) |
| **ash/event_hist.sql** | Event histogram showing wait distribution | - |
| **ash/sqlid_activity.sql** | Analyze activity for specific SQL_ID over time | - |
| **ash/time_model.sql** | Time model breakdown from ASH | - |

### Execution Plans - Enhanced Variants

| Script | Purpose | Similar To |
|--------|---------|------------|
| **xb.sql** | eXplain Better - enhanced execution plan display | x.sql (documented) |
| **xm.sql** | eXplain from Memory - show plan from library cache | xi.sql (documented) |
| **xp.sql** | eXplain with Profile - SQL Monitor report for session | sqlmon.sql (documented) |
| **xpi.sql** | eXplain with Profile by SQL_ID - SQL Monitor by SQL_ID | sqlmon.sql (documented) |
| **xms.sql** | eXplain from Memory with Statistics - plan + stats | xi.sql (documented) |
| **xmai.sql** | eXplain from Memory with aliases by SQL_ID | xi.sql (documented) |

### SQL Analysis - Core Scripts

| Script | Purpose | Similar To |
|--------|---------|------------|
| **sql.sql** | Show SQL text, children, stats by hash value | sqlid.sql (documented) |
| **sqlmemh.sql** | Show shared pool memory usage by hash value | sqlmem.sql (documented) |
| **sqlmemx.sql** | Show shared pool memory usage by SQL_ID | sqlmem.sql (documented) |
| **sqlopt.sql** | Show cursor compilation environment/parameters | - |
| **curheaps.sql** | Show cursor heap sizes and contents | - |

### AWR Analysis - Key Scripts

| Script | Purpose | Similar To |
|--------|---------|------------|
| **awr/dstat.sql** | System metrics per-minute from AWR | - |
| **awr/awr_evh.sql** | Event histogram from AWR | - |
| **awr/awr_sqlid.sql** | SQL analysis from AWR by SQL_ID | awr/awr_sqlstats.sql (documented) |
| **awr/awr_sqlstats_unstable.sql** | Detect SQLs with varying execution times | awr/awr_sqlstats_unstable.sql (documented) |

### Session Monitoring - Active Sessions

| Script | Purpose | Similar To |
|--------|---------|------------|
| **a.sql** | Display CURRENT active sessions with counts | s.sql (documented) |
| **as.sql** | Active sessions grouped by specified column | s.sql (documented) |
| **asql.sql** | Active sessions with their current SQL_IDs | s.sql (documented) |

## Priority 2: High-Value Scripts

### ASH Analysis - Specialized

| Script | Purpose |
|--------|---------|
| **ash/bash_wait_chains.sql** | Wait chains analysis using ASH (beta version) |
| **ash/ashpeak.sql** | Find peak activity periods in ASH |
| **ash/ashpeaktop.sql** | Top activity during peak periods |
| **ash/event_hist_micro.sql** | Event histogram with microsecond precision |
| **ash/shortmon.sql** | Short SQL execution monitoring |
| **ash/sqlid_plan_activity.sql** | Activity by SQL_ID and plan hash value |
| **ash/w.sql** | What's going on? Last minute activity from ASH |

### Memory & Buffer Profiling

| Script | Purpose |
|--------|---------|
| **bufprof.sql** | Buffer Get Profiler - profile buffer gets by session |
| **bhla.sql** | Buffer Headers by Latch Address |
| **bh_by_ts.sql** | Buffer cache contents by tablespace |
| **sgastatx.sql** | Extended SGA statistics from X$ tables |

### Performance Profiling

| Script | Purpose |
|--------|---------|
| **waitprof.sql** | Session Wait Profiler - sample session waits |
| **latchprofx.sql** | Extended latch profiling with more detail |

### Tracing & Diagnostics

| Script | Purpose |
|--------|---------|
| **53on.sql** / **53off.sql** | Enable/disable 10053 CBO trace |
| **46on.sql** / **46off.sql** | Enable/disable 10046 SQL trace |
| **ostackprofu.sql** | OS stack profiling for Unix/Linux |
| **ostackprofw.sql** | OS stack profiling for Windows |
| **diag.sql** | Display diagnostic information |

## Priority 3: Medium-Value Scripts

### AWR Analysis - Extended

| Script | Purpose |
|--------|---------|
| **awr/awr_sqlid_binds.sql** | Show bind variable values from AWR |
| **awr/awr_sysmetric_history.sql** | System metric history from AWR |
| **awr/awr_sysstat.sql** | System statistics from AWR |
| **awr/gen_awr_report.sql** | Generate AWR report |

### Object Information - Extended

| Script | Purpose |
|--------|---------|
| **ind2.sql** / **indf.sql** | Extended index information |
| **tab2.sql** | Extended table information |
| **cons.sql** / **cons2.sql** | Constraint information |
| **dep.sql** | Object dependencies |
| **partmon.sql** | Partition monitoring |
| **segstat.sql** | Segment statistics |

### Execution Plans - Additional Variants

| Script | Purpose |
|--------|---------|
| **xph.sql** | eXplain with Profile HTML output |
| **xpia.sql** | eXplain with Profile by SQL_ID (11.2+) |
| **xplto.sql** | Show execution plan operations |
| **xx.sql** | Display plan for last statement from library cache |

### SQL Analysis - Additional Tools

| Script | Purpose |
|--------|---------|
| **sqlflame.sql** | Flame chart for SQL execution profile |
| **sqlfh.sql** | SQL Feature Hierarchy |
| **sqlmon_restarts.sql** | Find SQLs with restart issues |

## Documentation Template

For each script, include:

```markdown
| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **script.sql** | keyword1, keyword2, keyword3 | Brief description of what it does | `@script param1 param2` | `@script example1`<br>`@script example2` |
```

### Example Entry

```markdown
| **ash/ashtop10.sql** | ash, active, session, history, top, wait, event, top10, limit | Display top 10 ASH activity by grouping columns (limited output version of ashtop) | `@ash/ashtop10 <grouping_cols> <filters> <from_time> <to_time>` | `@ash/ashtop10 username,event2 1=1 &hour`<br>`@ash/ashtop10 sql_id,wait_class 1=1 sysdate-1/24 sysdate` |
```

## Cross-Reference Strategy

When documenting, add notes like:

- "See also: **ash/ashtopsum.sql** for aggregated summary view"
- "Similar to **ash/ashtop.sql** but limits output to top 10 entries"
- "Historical version: **ash/dashtop.sql** queries DBA_HIST_ACTIVE_SESS_HISTORY"
- "12c+ version: **ash/asqlmon12.sql** includes additional metrics"

## Suggested Documentation Workflow

1. **Phase 1** (Priority 1 - ~25 scripts): Core ASH, SQL, Plan analysis
2. **Phase 2** (Priority 2 - ~20 scripts): Profiling, memory, tracing
3. **Phase 3** (Priority 3 - ~50 scripts): Extended AWR, objects, utilities
4. **Phase 4** (Remaining): Specialized and utility scripts

---

**Total Priority 1 Scripts:** ~25
**Total Priority 2 Scripts:** ~20  
**Total Priority 3 Scripts:** ~50

**For complete analysis, see:**
- UNDOCUMENTED_SCRIPTS_SUMMARY.md
- UNDOCUMENTED_SCRIPTS_ANALYSIS.md
