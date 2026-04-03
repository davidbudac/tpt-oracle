# TPT Scripts Catalog

Comprehensive catalog of Tanel Poder's Troubleshooting (TPT) Scripts for Oracle Database performance optimization and troubleshooting.

**Total Scripts Documented:** 700+ scripts (complete repository coverage)

## How to Use This Catalog

- **Browse:** Scroll through the tables organized by category
- **Search:** Use your browser's search (Ctrl+F / Cmd+F) or grep from command line
- **Filter:** Look for keywords in the Keywords column

## Quick Search Examples

```bash
# Find all scripts related to locks
grep -i lock SCRIPTS_CATALOG.md

# Find scripts in SQL Analysis category
grep "SQL Analysis" SCRIPTS_CATALOG.md

# Find scripts that accept sql_id parameter
grep "sql_id" SCRIPTS_CATALOG.md
```

## ASH Time Shortcuts

These work with most ASH scripts:
- `&min` or `&1min` - Last 1 minute
- `&5min` - Last 5 minutes
- `&hour` - Last hour
- `&day` - Last 24 hours
- `&today` - Today (from midnight)

---

## ASH Analysis - Complete (69 scripts)

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **ash/ashtop.sql** | ash, active, session, history, top, wait, event, grouping | Display top ASH activity by grouping columns | `@ash/ashtop <grouping_cols> <filters> <from_time> <to_time>` | `@ash/ashtop sql_id,event2 1=1 &hour` |
| **ash/ashtop10.sql** | ash, active, session, history, top, wait, event, top10, limit | Display top 10 ASH activity (limited output version) | `@ash/ashtop10 <grouping_cols> <filters> <from_time> <to_time>` | `@ash/ashtop10 username,event2 1=1 &hour` |
| **ash/ashtopsum.sql** | ash, active, session, history, summary, aggregate, stats | ASH activity summary with aggregated statistics | `@ash/ashtopsum <grouping_cols> <filters> <from_time> <to_time>` | `@ash/ashtopsum sql_id,event2 1=1 &hour` |
| **ash/ash_wait_chains.sql** | ash, wait, chain, blocking, blocker, lock, contention | Display ASH wait chains and blocking relationships | `@ash/ash_wait_chains <grouping_cols> <filters> <from_time> <to_time>` | `@ash/ash_wait_chains username 1=1 &hour` |
| **ash/ash_index_helper.sql** | ash, index, recommendation, missing, tuning | Suggest missing indexes based on ASH data | `@ash/ash_index_helper <sql_id> <schema.%> <from_time> <to_time>` | `@ash/ash_index_helper % SOE.% &hour` |
| **ash/ash_index_helperx.sql** | ash, index, recommendation, extended | Extended index recommendations from ASH | `@ash/ash_index_helperx <sql_id> <schema.%> <from_time> <to_time>` | `@ash/ash_index_helperx % %.% &hour` |
| **ash/ash_log_file_sync.sql** | ash, log, file, sync, redo, commit | Analyze log file sync waits from ASH | `@ash/ash_log_file_sync <from_time> <to_time>` | `@ash/ash_log_file_sync &hour` |
| **ash/ash_object_predicates.sql** | ash, object, predicates, filter, access | Display SQL predicates and object access from ASH | `@ash/ash_object_predicates <sql_id> <from_time> <to_time>` | `@ash/ash_object_predicates 7q729nhdgtsqq &hour` |
| **ash/ashmem.sql** | ash, memory, pga, consumption | ASH memory consumption analysis | `@ash/ashmem <filter> <from_time> <to_time>` | `@ash/ashmem 1=1 &hour` |
| **ash/ashpeak.sql** | ash, peak, activity, spike, busiest | Find peak activity times in ASH | `@ash/ashpeak <from_time> <to_time>` | `@ash/ashpeak &today` |
| **ash/ashpeaktop.sql** | ash, peak, top, activity, spike | Top activity during peak periods | `@ash/ashpeaktop <from_time> <to_time>` | `@ash/ashpeaktop &today` |
| **ash/asqlmon.sql** | ash, sql, monitor, execution, plan, step | SQL monitoring drill-down by execution plan step | `@ash/asqlmon <sql_id> <child#> <from_time> <to_time>` | `@ash/asqlmon 7q729nhdgtsqq 0 &hour` |
| **ash/asqlmon12.sql** | ash, sql, monitor, 12c, execution, plan, enhanced | SQL monitoring for Oracle 12c+ with enhanced metrics | `@ash/asqlmon12 <sql_id> <child#> <from_time> <to_time>` | `@ash/asqlmon12 7q729nhdgtsqq 0 &hour` |
| **ash/asqlmonx.sql** | ash, sql, monitor, extended, execution, plan | Extended SQL Monitor with additional columns | `@ash/asqlmonx <sql_id> <child#> <from_time> <to_time>` | `@ash/asqlmonx 7q729nhdgtsqq 0 &hour` |
| **ash/asqlflame.sql** | ash, sql, flame, chart, execution, profile | SQL flame chart from ASH data | `@ash/asqlflame <sql_id> <from_time> <to_time>` | `@ash/asqlflame 7q729nhdgtsqq &hour` |
| **ash/bash_wait_chains.sql** | ash, wait, chain, blocking, beta | Wait chains analysis (beta version) | `@ash/bash_wait_chains <grouping_cols> <filters> <from_time> <to_time>` | `@ash/bash_wait_chains username 1=1 &hour` |
| **ash/bashtop.sql** | ash, background, top, activity | Background process ASH activity | `@ash/bashtop <grouping_cols> <filters> <from_time> <to_time>` | `@ash/bashtop program2,event2 1=1 &hour` |
| **ash/bevent_hist.sql** | ash, background, event, histogram | Background process event histogram | `@ash/bevent_hist <event> <filter> <from_time> <to_time>` | `@ash/bevent_hist % 1=1 &hour` |
| **ash/bevent_hist_micro.sql** | ash, background, event, histogram, microsecond | Background event histogram with microsecond precision | `@ash/bevent_hist_micro <event> <filter> <from_time> <to_time>` | `@ash/bevent_hist_micro % 1=1 &hour` |
| **ash/bshortmon_logfilesync.sql** | ash, background, log, file, sync | Background log file sync monitoring | `@ash/bshortmon_logfilesync <from_time> <to_time>` | `@ash/bshortmon_logfilesync &hour` |
| **ash/btime_model_phases.sql** | ash, background, time, model, phases | Background time model phases | `@ash/btime_model_phases <from_time> <to_time>` | `@ash/btime_model_phases &hour` |
| **ash/cashtop.sql** | ash, consolidated, top, activity | Consolidated ASH top activity | `@ash/cashtop <grouping_cols> <filters> <from_time> <to_time>` | `@ash/cashtop sql_id,event2 1=1 &hour` |
| **ash/create_ash_without_timestamps.sql** | ash, create, view, timestamps | Create ASH view without timestamps | `@ash/create_ash_without_timestamps` | `@ash/create_ash_without_timestamps` |
| **ash/daplanline.sql** | ash, awr, plan, line, historical | Historical plan line activity from DBA_HIST | `@ash/daplanline <sql_id> <from_time> <to_time>` | `@ash/daplanline 7q729nhdgtsqq sysdate-7 sysdate` |
| **ash/dash_wait_chains.sql** | ash, awr, wait, chain, historical | Historical wait chains from DBA_HIST_ASH | `@ash/dash_wait_chains <grouping_cols> <filters> <from_time> <to_time>` | `@ash/dash_wait_chains username 1=1 sysdate-7 sysdate` |
| **ash/dashpeak.sql** | ash, awr, peak, historical | Historical peak activity from DBA_HIST | `@ash/dashpeak <from_time> <to_time>` | `@ash/dashpeak sysdate-7 sysdate` |
| **ash/dashpeaktop.sql** | ash, awr, peak, top, historical | Historical peak top activity | `@ash/dashpeaktop <from_time> <to_time>` | `@ash/dashpeaktop sysdate-7 sysdate` |
| **ash/dashtop.sql** | ash, awr, historical, dba_hist, top, activity | Top activity from DBA_HIST_ACTIVE_SESS_HISTORY (AWR) | `@ash/dashtop <grouping_cols> <filters> <from_time> <to_time>` | `@ash/dashtop sql_id,event2 1=1 sysdate-7 sysdate` |
| **ash/dashtopsum.sql** | ash, awr, historical, summary | Historical ASH summary from DBA_HIST | `@ash/dashtopsum <grouping_cols> <filters> <from_time> <to_time>` | `@ash/dashtopsum sql_id,event2 1=1 sysdate-7 sysdate` |
| **ash/dashtopsum_pga.sql** | ash, awr, historical, summary, pga | Historical ASH PGA summary | `@ash/dashtopsum_pga <grouping_cols> <filters> <from_time> <to_time>` | `@ash/dashtopsum_pga username 1=1 sysdate-7 sysdate` |
| **ash/dasqlmon.sql** | ash, awr, historical, sql, monitor, dba_hist | SQL Monitor from DBA_HIST_ASH (historical) | `@ash/dasqlmon <sql_id> <child#> <from_time> <to_time>` | `@ash/dasqlmon 7q729nhdgtsqq 0 sysdate-7 sysdate` |
| **ash/dasqlmonx.sql** | ash, awr, historical, sql, monitor, extended | Extended historical SQL Monitor | `@ash/dasqlmonx <sql_id> <child#> <from_time> <to_time>` | `@ash/dasqlmonx 7q729nhdgtsqq 0 sysdate-7 sysdate` |
| **ash/devent_hist.sql** | ash, awr, event, histogram, historical | Historical event histogram from DBA_HIST | `@ash/devent_hist <event> <filter> <from_time> <to_time>` | `@ash/devent_hist "log file sync" 1=1 sysdate-7 sysdate` |
| **ash/devent_hist_micro.sql** | ash, awr, event, histogram, microsecond | Historical microsecond event histogram | `@ash/devent_hist_micro <event> <filter> <from_time> <to_time>` | `@ash/devent_hist_micro % 1=1 sysdate-7 sysdate` |
| **ash/disk_rereads.sql** | ash, disk, rereads, io | Analyze disk re-reads from ASH | `@ash/disk_rereads <from_time> <to_time>` | `@ash/disk_rereads &hour` |
| **ash/event_hist.sql** | ash, event, histogram, wait, distribution | Wait event time distribution histogram | `@ash/event_hist <event> <filter> <from_time> <to_time>` | `@ash/event_hist "log file sync" 1=1 &hour` |
| **ash/event_hist_cell.sql** | ash, event, histogram, cell, exadata | Exadata cell event histogram | `@ash/event_hist_cell <event> <filter> <from_time> <to_time>` | `@ash/event_hist_cell % 1=1 &hour` |
| **ash/event_hist_micro.sql** | ash, event, histogram, microsecond, latency, precision | Event histogram with microsecond precision | `@ash/event_hist_micro <event> <filter> <from_time> <to_time>` | `@ash/event_hist_micro log.file.sync 1=1 &hour` |
| **ash/gashtop.sql** | ash, global, rac, top, activity | Global RAC ASH top activity | `@ash/gashtop <grouping_cols> <filters> <from_time> <to_time>` | `@ash/gashtop sql_id,event2 1=1 &hour` |
| **ash/gasqlmon.sql** | ash, global, rac, sql, monitor | Global RAC SQL Monitor | `@ash/gasqlmon <sql_id> <child#> <from_time> <to_time>` | `@ash/gasqlmon 7q729nhdgtsqq 0 &hour` |
| **ash/gen_ash_report_html.sql** | ash, report, html, generate | Generate ASH report in HTML format | `@ash/gen_ash_report_html` | `@ash/gen_ash_report_html` |
| **ash/gen_ash_report_text.sql** | ash, report, text, generate | Generate ASH report in text format | `@ash/gen_ash_report_text` | `@ash/gen_ash_report_text` |
| **ash/perfsheet_ash.sql** | ash, perfsheet, dashboard | ASH performance sheet/dashboard | `@ash/perfsheet_ash <from_time> <to_time>` | `@ash/perfsheet_ash &hour` |
| **ash/rowsource_events.sql** | ash, rowsource, events, plan | Row source events from execution plan | `@ash/rowsource_events <sql_id> <from_time> <to_time>` | `@ash/rowsource_events 7q729nhdgtsqq &hour` |
| **ash/sample_drift.sql** | ash, sample, drift, timing | Analyze ASH sample drift | `@ash/sample_drift <from_time> <to_time>` | `@ash/sample_drift &hour` |
| **ash/shortmon.sql** | ash, short, monitor, quick | Short SQL execution monitoring | `@ash/shortmon <sql_id> <from_time> <to_time>` | `@ash/shortmon 7q729nhdgtsqq &5min` |
| **ash/shortmon_cell.sql** | ash, short, monitor, cell, exadata | Short monitoring for Exadata cells | `@ash/shortmon_cell <sql_id> <from_time> <to_time>` | `@ash/shortmon_cell 7q729nhdgtsqq &5min` |
| **ash/shortmon_logfilesync.sql** | ash, short, monitor, log, file, sync | Short log file sync monitoring | `@ash/shortmon_logfilesync <from_time> <to_time>` | `@ash/shortmon_logfilesync &5min` |
| **ash/shortmon_numblocks.sql** | ash, short, monitor, blocks, io | Short monitoring by block counts | `@ash/shortmon_numblocks <sql_id> <from_time> <to_time>` | `@ash/shortmon_numblocks 7q729nhdgtsqq &5min` |
| **ash/sqlexec_duration_buckets.sql** | ash, sql, execution, duration, buckets | SQL execution duration distribution | `@ash/sqlexec_duration_buckets <sql_id> <from_time> <to_time>` | `@ash/sqlexec_duration_buckets 7q729nhdgtsqq &day` |
| **ash/sqlexec_longer_than.sql** | ash, sql, execution, long, running | Find SQL executions longer than threshold | `@ash/sqlexec_longer_than <seconds> <from_time> <to_time>` | `@ash/sqlexec_longer_than 60 &hour` |
| **ash/sqlid_activity.sql** | ash, sql, activity, tracking, timeline | Activity for specific SQL_ID over time | `@ash/sqlid_activity <sql_id> <from_time> <to_time>` | `@ash/sqlid_activity 7q729nhdgtsqq &day` |
| **ash/sqlid_dbtime_buckets.sql** | ash, sql, dbtime, buckets, distribution | SQL DB time distribution buckets | `@ash/sqlid_dbtime_buckets <sql_id> <from_time> <to_time>` | `@ash/sqlid_dbtime_buckets 7q729nhdgtsqq &day` |
| **ash/sqlid_plan_activity.sql** | ash, sql, plan, activity | Activity by SQL_ID and plan hash value | `@ash/sqlid_plan_activity <sql_id> <from_time> <to_time>` | `@ash/sqlid_plan_activity 7q729nhdgtsqq &day` |
| **ash/time_model.sql** | ash, time, model, breakdown, stats | Time model breakdown from ASH data | `@ash/time_model <filter> <from_time> <to_time>` | `@ash/time_model 1=1 &hour` |
| **ash/w.sql** | ash, what, now, current, quick, status | What's happening? Last minute activity check | `@ash/w` | `@ash/w` |

**ASH Examples Scripts (ash/examples/):**

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **ash/examples/ash2.sql** | ash, example, demo | ASH example script 2 | `@ash/examples/ash2` | `@ash/examples/ash2` |
| **ash/examples/ash3.sql** | ash, example, demo | ASH example script 3 | `@ash/examples/ash3` | `@ash/examples/ash3` |
| **ash/examples/ash5.sql** | ash, example, demo | ASH example script 5 | `@ash/examples/ash5` | `@ash/examples/ash5` |
| **ash/examples/ash6.sql** | ash, example, demo | ASH example script 6 | `@ash/examples/ash6` | `@ash/examples/ash6` |
| **ash/examples/ash7.sql** | ash, example, demo | ASH example script 7 | `@ash/examples/ash7` | `@ash/examples/ash7` |
| **ash/examples/ash8.sql** | ash, example, demo | ASH example script 8 | `@ash/examples/ash8` | `@ash/examples/ash8` |
| **ash/examples/ash9.sql** | ash, example, demo | ASH example script 9 | `@ash/examples/ash9` | `@ash/examples/ash9` |
| **ash/examples/ash10.sql** | ash, example, demo | ASH example script 10 | `@ash/examples/ash10` | `@ash/examples/ash10` |
| **ash/examples/ash11.sql** | ash, example, demo | ASH example script 11 | `@ash/examples/ash11` | `@ash/examples/ash11` |
| **ash/examples/ash12a.sql** | ash, example, demo | ASH example script 12a | `@ash/examples/ash12a` | `@ash/examples/ash12a` |
| **ash/examples/ash13.sql** | ash, example, demo | ASH example script 13 | `@ash/examples/ash13` | `@ash/examples/ash13` |
| **ash/examples/ash13a.sql** | ash, example, demo | ASH example script 13a | `@ash/examples/ash13a` | `@ash/examples/ash13a` |
| **ash/examples/ashrelated.sql** | ash, example, related | ASH related sessions example | `@ash/examples/ashrelated` | `@ash/examples/ashrelated` |

---

## Execution Plans - Complete (42 scripts)

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **x.sql** | explain, plan, execution, xplan, last, cursor | Display execution plan for last SQL in session | `@x` | `@x` |
| **x2.sql** | explain, plan, execution, variant | Execution plan variant 2 | `@x2` | `@x2` |
| **x9.sql** | explain, plan, execution, 9i | Execution plan for Oracle 9i | `@x9 <sql_id>` | `@x9 7q729nhdgtsqq` |
| **x9a.sql** | explain, plan, execution, 9i, all | All execution plans for Oracle 9i | `@x9a <sql_id>` | `@x9a 7q729nhdgtsqq` |
| **x9all.sql** | explain, plan, execution, 9i, all | All plans Oracle 9i | `@x9all <sql_id>` | `@x9all 7q729nhdgtsqq` |
| **x101.sql** | explain, plan, execution, 10.1 | Execution plan for Oracle 10.1 | `@x101 <sql_id>` | `@x101 7q729nhdgtsqq` |
| **xa.sql** | explain, plan, execution, xplan, allstats | Display execution plan with allstats | `@xa` | `@xa` |
| **xad.sql** | explain, plan, last, library, advanced | Advanced plan for last statement from library cache | `@xad` | `@xad` |
| **xall.sql** | explain, plan, all, children | Display all child cursor plans | `@xall <sql_id>` | `@xall 7q729nhdgtsqq` |
| **xawr.sql** | explain, plan, execution, awr, history | Display execution plan from AWR | `@xawr <sql_id> <plan_hash_value>` | `@xawr 7q729nhdgtsqq 1234567890` |
| **xb.sql** | explain, plan, better, enhanced, display | eXplain Better - enhanced execution plan display | `@xb <sql_id> <child#>` | `@xb 7q729nhdgtsqq 0` |
| **xbi.sql** | explain, plan, better, sqlid | eXplain Better by SQL_ID | `@xbi <sql_id> <child#>` | `@xbi 7q729nhdgtsqq 0` |
| **xbix.sql** | explain, plan, better, sqlid, extended | eXplain Better by SQL_ID extended | `@xbix <sql_id> <child#>` | `@xbix 7q729nhdgtsqq 0` |
| **xbx.sql** | explain, plan, better, extended | eXplain Better extended | `@xbx <sql_id> <child#>` | `@xbx 7q729nhdgtsqq 0` |
| **xco.sql** | explain, plan, cost, optimizer | Execution plan with optimizer cost details | `@xco <sql_id>` | `@xco 7q729nhdgtsqq` |
| **xde.sql** | explain, x$, describe, fixed | X$ table describe | `@xde <x$_table>` | `@xde x$ksuse` |
| **xde2.sql** | explain, x$, describe, fixed, extended | Extended X$ table describe | `@xde2 <x$_table>` | `@xde2 x$ksuse` |
| **xi.sql** | explain, plan, execution, xplan, sqlid, library | Display execution plan from library cache by SQL_ID | `@xi <sql_id> <child#>` | `@xi 7q729nhdgtsqq 0` |
| **xia.sql** | explain, plan, advanced, sqlid | Display plan in advanced format for SQL_ID | `@xia <sql_id>` | `@xia 7q729nhdgtsqq` |
| **xiad.sql** | explain, plan, advanced, detailed | Detailed advanced plan for SQL_ID | `@xiad <sql_id> <child#>` | `@xiad 7q729nhdgtsqq 0` |
| **xip.sql** | explain, plan, sqlid, peeked | Plan with peeked binds for SQL_ID | `@xip <sql_id> <child#>` | `@xip 7q729nhdgtsqq 0` |
| **xls.sql** | explain, plan, list | List execution plans | `@xls <sql_id>` | `@xls 7q729nhdgtsqq` |
| **xm.sql** | explain, plan, memory, library, cache | eXplain from Memory - show plan from library cache | `@xm <sql_id> <child#>` | `@xm 7q729nhdgtsqq 0` |
| **xma.sql** | explain, plan, memory, all | eXplain from Memory - all children | `@xma <sql_id>` | `@xma 7q729nhdgtsqq` |
| **xmai.sql** | explain, plan, memory, aliases, sqlid | eXplain from Memory with Aliases by SQL_ID | `@xmai <sql_id>` | `@xmai 7q729nhdgtsqq` |
| **xmon.sql** | explain, monitor, sql, execution | SQL Monitor execution plan | `@xmon <sid>` | `@xmon 123` |
| **xms.sql** | explain, plan, memory, statistics, stats | eXplain from Memory with Statistics | `@xms <sql_id> <child#>` | `@xms 7q729nhdgtsqq 0` |
| **xms2.sql** | explain, plan, memory, statistics, variant | eXplain from Memory with Statistics variant 2 | `@xms2 <sql_id> <child#>` | `@xms2 7q729nhdgtsqq 0` |
| **xmsh.sql** | explain, plan, memory, statistics, hash | eXplain from Memory with Statistics by hash | `@xmsh <hash_value>` | `@xmsh 1234567890` |
| **xmsi.sql** | explain, plan, memory, statistics, sqlid | eXplain from Memory with Statistics by SQL_ID | `@xmsi <sql_id>` | `@xmsi 7q729nhdgtsqq` |
| **xp.sql** | explain, plan, profile, sqlmon, session | eXplain with Profile - SQL Monitor for session | `@xp <sid>` | `@xp 123` |
| **xpa.sql** | explain, plan, profile, sqlmon, all | eXplain with Profile - all (11.2+) | `@xpa <sid>` | `@xpa 123` |
| **xph.sql** | explain, plan, profile, html, sqlmon | eXplain with Profile HTML output | `@xph <sid>` | `@xph 123` |
| **xpi.sql** | explain, plan, profile, sqlmon, sqlid | eXplain with Profile by SQL_ID - SQL Monitor | `@xpi <sql_id>` | `@xpi 7q729nhdgtsqq` |
| **xpia.sql** | explain, plan, profile, sqlid, 11.2+ | eXplain with Profile by SQL_ID (11.2+) | `@xpia <sql_id>` | `@xpia 7q729nhdgtsqq` |
| **xpih.sql** | explain, plan, profile, sqlid, html | eXplain with Profile by SQL_ID HTML (11.2+) | `@xpih <sql_id>` | `@xpih 7q729nhdgtsqq` |
| **xplto.sql** | explain, plan, operations, steps | Show execution plan operations only | `@xplto <operation>` | `@xplto TABLE` |
| **xpm.sql** | explain, plan, monitor | Plan from SQL Monitor | `@xpm <sql_id>` | `@xpm 7q729nhdgtsqq` |
| **xprof.sql** | explain, plan, profile, monitor | SQL Monitor profile report | `@xprof <sql_id> <sql_exec_id> <sid>` | `@xprof 7q729nhdgtsqq % 123` |
| **xr.sql** | explain, plan, runtime | Explain plan runtime statistics | `@xr <sql_id>` | `@xr 7q729nhdgtsqq` |
| **xs.sql** | explain, plan, simple | Simple execution plan display | `@xs <sql_id>` | `@xs 7q729nhdgtsqq` |
| **xsid.sql** | explain, plan, session, sid | Execution plan for session SID | `@xsid <sid>` | `@xsid 123` |
| **xsida.sql** | explain, plan, session, sid, advanced | Advanced plan for session SID | `@xsida <sid>` | `@xsida 123` |
| **xt.sql** | explain, plan, text | Execution plan as text | `@xt <sql_id>` | `@xt 7q729nhdgtsqq` |
| **xte.sql** | explain, plan, text, extended | Extended text execution plan | `@xte <sql_id>` | `@xte 7q729nhdgtsqq` |
| **xtreset.sql** | explain, trace, reset | Reset explain/trace settings | `@xtreset` | `@xtreset` |
| **xx.sql** | explain, plan, last, library, cache | Display plan for last statement from library cache | `@xx` | `@xx` |

---

## SQL Analysis - Complete (26 scripts)

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **sqlid.sql** | sql, sqlid, execution, statistics, plan, cursor | Display SQL text, child cursors, execution statistics | `@sqlid <sql_id> <child#>` | `@sqlid 7q729nhdgtsqq 0` |
| **sql.sql** | sql, text, children, stats, hash | Show SQL text, children, stats by hash value | `@sql <hash_value>` | `@sql 1234567890` |
| **sqlf.sql** | sql, fulltext, text, complete | Display full SQL text from V$SQL | `@sqlf <sql_id>` | `@sqlf 7q729nhdgtsqq` |
| **sqla.sql** | sql, analysis, statistics | SQL analysis with statistics | `@sqla <sql_id>` | `@sqla 7q729nhdgtsqq` |
| **sqlbinds.sql** | bind, variable, value, captured, peeking | Display captured SQL bind variable values | `@sqlbinds <sql_id> <child#> <bind_name>` | `@sqlbinds 7q729nhdgtsqq 0 %` |
| **sqlbindsum.sql** | bind, variable, summary, captured | Summary of SQL bind variable values | `@sqlbindsum <sql_id>` | `@sqlbindsum 7q729nhdgtsqq` |
| **sqlcsstat.sql** | sql, cursor, statistics | SQL cursor statistics | `@sqlcsstat <sql_id>` | `@sqlcsstat 7q729nhdgtsqq` |
| **sqlexecid.sql** | sql, execution, id, instance | SQL execution ID tracking | `@sqlexecid <sql_id>` | `@sqlexecid 7q729nhdgtsqq` |
| **sqlfh.sql** | sql, feature, hierarchy, usage | SQL Feature Hierarchy | `@sqlfh <sql_id>` | `@sqlfh 7q729nhdgtsqq` |
| **sqlflame.sql** | sql, flame, chart, profile, execution | Flame chart for SQL execution profile | `@sqlflame <sql_id>` | `@sqlflame 7q729nhdgtsqq` |
| **sqlfn.sql** | sql, function, name | SQL function names | `@sqlfn <function>` | `@sqlfn %` |
| **sqlfna.sql** | sql, function, name, all | All SQL function names | `@sqlfna <function>` | `@sqlfna %` |
| **sqlh.sql** | sql, hash, history | SQL by hash value history | `@sqlh <hash_value>` | `@sqlh 1234567890` |
| **sqli.sql** | sql, information | SQL information | `@sqli <sql_id>` | `@sqli 7q729nhdgtsqq` |
| **sqlidx.sql** | sql, exadata, metrics | Exadata-specific metrics from V$SQL | `@sqlidx <sql_id>` | `@sqlidx 7q729nhdgtsqq` |
| **sqll.sql** | sql, long, text | SQL long text | `@sqll <sql_id>` | `@sqll 7q729nhdgtsqq` |
| **sqlmem.sql** | sql, memory, shared, pool, cursor | Display shared pool memory usage for SQL | `@sqlmem <sql_id>` | `@sqlmem 7q729nhdgtsqq` |
| **sqlmemh.sql** | sql, memory, shared, pool, hash | Shared pool memory usage by hash value | `@sqlmemh <hash_value>` | `@sqlmemh 1234567890` |
| **sqlmemx.sql** | sql, memory, shared, pool, sqlid | Shared pool memory usage by SQL_ID | `@sqlmemx <sql_id>` | `@sqlmemx 7q729nhdgtsqq` |
| **sqlmon.sql** | sql, monitor, real, time, execution | Run SQL Monitor report for session | `@sqlmon <sid>` | `@sqlmon 123` |
| **sqlmon_restarts.sql** | sql, monitor, restarts, issues, failures | Find SQLs with restart issues from V$SQL_PLAN_MONITOR | `@sqlmon_restarts` | `@sqlmon_restarts` |
| **sqlmon_sn.sql** | sql, monitor, statname | SQL Monitor stat names | `@sqlmon_sn` | `@sqlmon_sn` |
| **sqlmoni.sql** | sql, monitor, html, spool | Spool SQL Monitoring report to HTML file | `@sqlmoni <sql_id>` | `@sqlmoni 7q729nhdgtsqq` |
| **sqlopt.sql** | sql, cursor, compilation, environment, parameters | Show cursor compilation environment/parameters | `@sqlopt <sql_id> <child#> <param>` | `@sqlopt 7q729nhdgtsqq 0 %` |
| **sqlprof.sql** | sql, profile, hints | Display SQL profile hints | `@sqlprof <sql_id>` | `@sqlprof 7q729nhdgtsqq` |
| **sqlt.sql** | sql, text | SQL text display | `@sqlt <sql_id>` | `@sqlt 7q729nhdgtsqq` |
| **sqlt9.sql** | sql, text, 9i | SQL text display for Oracle 9i | `@sqlt9 <hash_value>` | `@sqlt9 1234567890` |
| **sqltune_tune_sqlid.sql** | sql, tuning, advisor, dbms_sqltune | Run SQL Tuning Advisor for SQL_ID | `@sqltune_tune_sqlid <sql_id> <time_limit>` | `@sqltune_tune_sqlid 7q729nhdgtsqq 60` |
| **curheaps.sql** | cursor, heap, memory, size, contents | Show cursor heap sizes and contents | `@curheaps <sql_id>` | `@curheaps 7q729nhdgtsqq` |
| **curschema.sql** | cursor, schema, current | Current cursor schema | `@curschema` | `@curschema` |
| **nonshared.sql** | cursor, sharing, nonshared, child, reason | Display reasons child cursors are not shared | `@nonshared <sql_id>` | `@nonshared 7q729nhdgtsqq` |
| **nonshared2.sql** | cursor, sharing, nonshared, extended | Extended non-shared cursor reasons | `@nonshared2 <sql_id>` | `@nonshared2 7q729nhdgtsqq` |
| **nonsharedsum.sql** | cursor, sharing, nonshared, summary | Summary of non-shared cursor reasons | `@nonsharedsum <sql_id>` | `@nonsharedsum 7q729nhdgtsqq` |
| **nonsharedsum2.sql** | cursor, sharing, nonshared, summary | Non-shared cursor summary variant 2 | `@nonsharedsum2 <sql_id>` | `@nonsharedsum2 7q729nhdgtsqq` |
| **nonsharedsum3.sql** | cursor, sharing, nonshared, summary | Non-shared cursor summary variant 3 | `@nonsharedsum3 <sql_id>` | `@nonsharedsum3 7q729nhdgtsqq` |
| **nonsharedsum_html.sql** | cursor, sharing, nonshared, summary, html | Non-shared cursor summary HTML | `@nonsharedsum_html <sql_id>` | `@nonsharedsum_html 7q729nhdgtsqq` |
| **topcur.sql** | cursor, top, memory, shared, pool | Display top cursors by memory usage | `@topcur` | `@topcur` |
| **topcurmem.sql** | cursor, memory, top, detailed | Top cursors with detailed memory breakdown | `@topcurmem` | `@topcurmem` |
| **sql_profile_hints.sql** | sql, profile, hints, extract | Extract SQL profile hints | `@sql_profile_hints <profile_name>` | `@sql_profile_hints SYS_SQLPROF_123` |

---

## AWR Analysis - Complete (21 scripts)

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **awr/awr_sqlstats.sql** | awr, sql, statistics, history, performance | Display SQL statistics from AWR | `@awr/awr_sqlstats <sql_id> <phv> <from_time> <to_time>` | `@awr/awr_sqlstats 7q729nhdgtsqq % sysdate-7 sysdate` |
| **awr/awr_sqlstats_per_exec.sql** | awr, sql, statistics, per, execution | SQL statistics per execution from AWR | `@awr/awr_sqlstats_per_exec <sql_id> <phv> <from_time> <to_time>` | `@awr/awr_sqlstats_per_exec 7q729nhdgtsqq % sysdate-7 sysdate` |
| **awr/awr_sqlstats_unstable.sql** | awr, sql, unstable, plan, variation | Detect SQLs with varying execution times | `@awr/awr_sqlstats_unstable <group_by> <order_by> <from_time> <to_time>` | `@awr/awr_sqlstats_unstable sql_id plan_hash_value sysdate-7 sysdate` |
| **awr/awr_evh.sql** | awr, event, histogram, wait, distribution | Event histogram from AWR | `@awr/awr_evh <event> <from_time> <to_time>` | `@awr/awr_evh "log file sync" sysdate-7 sysdate` |
| **awr/awr_last.sql** | awr, last, snapshot, recent | Show last AWR snapshots | `@awr/awr_last` | `@awr/awr_last` |
| **awr/awr_lasth.sql** | awr, last, snapshot, recent, hourly | Show last hourly AWR snapshots | `@awr/awr_lasth` | `@awr/awr_lasth` |
| **awr/awr_log_file_sync.sql** | awr, log, file, sync, redo, history | Log file sync analysis from AWR | `@awr/awr_log_file_sync <from_time> <to_time>` | `@awr/awr_log_file_sync sysdate-7 sysdate` |
| **awr/awr_mem_resize.sql** | awr, memory, resize, sga, history | Memory resize operations from AWR | `@awr/awr_mem_resize <from_time> <to_time>` | `@awr/awr_mem_resize sysdate-7 sysdate` |
| **awr/awr_procmem.sql** | awr, process, memory, history | Process memory usage from AWR | `@awr/awr_procmem <from_time> <to_time>` | `@awr/awr_procmem sysdate-7 sysdate` |
| **awr/awr_sqlid.sql** | awr, sql, analysis, sqlid, history | SQL analysis from AWR by SQL_ID | `@awr/awr_sqlid <sql_id> <from_time> <to_time>` | `@awr/awr_sqlid 7q729nhdgtsqq sysdate-7 sysdate` |
| **awr/awr_sqlid_binds.sql** | awr, bind, variable, values, captured | Show bind variable values from AWR | `@awr/awr_sqlid_binds <sql_id> <from_time> <to_time>` | `@awr/awr_sqlid_binds 7q729nhdgtsqq sysdate-7 sysdate` |
| **awr/awr_sysmetric_history.sql** | awr, system, metric, history, trend | System metric history from AWR | `@awr/awr_sysmetric_history <metric> <from_time> <to_time>` | `@awr/awr_sysmetric_history "CPU%" sysdate-7 sysdate` |
| **awr/awr_sysmetric_summary.sql** | awr, system, metric, summary | System metric summary from AWR | `@awr/awr_sysmetric_summary <from_time> <to_time>` | `@awr/awr_sysmetric_summary sysdate-7 sysdate` |
| **awr/awr_sysstat.sql** | awr, system, statistics, sysstat, history | System statistics from AWR | `@awr/awr_sysstat <stat_name> <from_time> <to_time>` | `@awr/awr_sysstat "redo size" sysdate-7 sysdate` |
| **awr/awr_system_event.sql** | awr, system, event, wait, history | System event statistics from AWR | `@awr/awr_system_event <event> <from_time> <to_time>` | `@awr/awr_system_event "db file%" sysdate-7 sysdate` |
| **awr/create_event_histogram_view.sql** | awr, event, histogram, view, create | Create event histogram view | `@awr/create_event_histogram_view` | `@awr/create_event_histogram_view` |
| **awr/dbload.sql** | awr, database, load, history | Database load analysis from AWR | `@awr/dbload <from_time> <to_time>` | `@awr/dbload sysdate-7 sysdate` |
| **awr/dstat.sql** | awr, system, metrics, per-minute, dba_hist | System metrics per-minute from AWR | `@awr/dstat <from_time> <to_time>` | `@awr/dstat sysdate-1 sysdate` |
| **awr/gen_awr_report.sql** | awr, report, generate, html, text | Generate AWR report | `@awr/gen_awr_report` | `@awr/gen_awr_report` |
| **awr/gen_perfhub_report.sql** | awr, perfhub, report, generate | Generate Performance Hub report | `@awr/gen_perfhub_report` | `@awr/gen_perfhub_report` |
| **awr/get_settings.sql** | awr, settings, configuration | Get AWR settings | `@awr/get_settings` | `@awr/get_settings` |
| **awr/other_xml.sql** | awr, other, xml, plan | OTHER_XML from AWR execution plans | `@awr/other_xml <sql_id> <phv>` | `@awr/other_xml 7q729nhdgtsqq 1234567890` |
| **awr/settings.sql** | awr, settings, retention, interval | Display AWR settings and retention | `@awr/settings` | `@awr/settings` |

---

## Session Monitoring - Active Sessions

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **a.sql** | active, sessions, count, current, status | Display current active sessions with counts | `@a` | `@a` |
| **as.sql** | active, sessions, grouped, column, aggregate | Active sessions grouped by specified column | `@as <column>` | `@as username`<br>`@as event` |
| **asql.sql** | active, sessions, sql, sqlid, current | Active sessions with their current SQL_IDs | `@asql` | `@asql` |

---

## Tracing & Diagnostics

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **53on.sql** | trace, 10053, cbo, optimizer, enable | Enable 10053 CBO trace | `@53on <sid>` | `@53on 123` |
| **53off.sql** | trace, 10053, cbo, optimizer, disable | Disable 10053 CBO trace | `@53off <sid>` | `@53off 123` |
| **46on.sql** | trace, 10046, sql, enable | Enable 10046 SQL trace | `@46on <sid>` | `@46on 123` |
| **46off.sql** | trace, 10046, sql, disable | Disable 10046 SQL trace | `@46off <sid>` | `@46off 123` |
| **ostackprofu.sql** | stack, profiling, unix, linux, os | OS stack profiling for Unix/Linux | `@ostackprofu <spid> <samples>` | `@ostackprofu 12345 1000` |
| **ostackprofw.sql** | stack, profiling, windows, os | OS stack profiling for Windows | `@ostackprofw <spid> <samples>` | `@ostackprofw 12345 1000` |
| **diag.sql** | diagnostic, information, session, system | Display diagnostic information | `@diag` | `@diag` |

---

## Performance Profiling - Advanced

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **latchprofx.sql** | latch, profiling, extended, holder, contention | Extended latch profiling with more detail | `@latchprofx <group_cols> <sid> <latch> <samples>` | `@latchprofx name,sqlid % "shared pool" 100000` |
| **bufprof.sql** | buffer, profiling, gets, cache, session | Buffer Get Profiler - profile buffer gets | `@bufprof <sid> <samples>` | `@bufprof 123 10000` |
| **bhla.sql** | buffer, header, latch, address, cache | Buffer Headers by Latch Address | `@bhla` | `@bhla` |
| **bh_by_ts.sql** | buffer, cache, tablespace, contents | Buffer cache contents by tablespace | `@bh_by_ts` | `@bh_by_ts` |

---

## Object Information - Extended

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **ind2.sql** | index, extended, information, statistics | Extended index information | `@ind2 <owner>.<index>` | `@ind2 soe.ord_customer_ix` |
| **indf.sql** | index, full, detailed, information | Detailed index information | `@indf <owner>.<index>` | `@indf soe.ord_customer_ix` |
| **tab2.sql** | table, extended, information, statistics | Extended table information | `@tab2 <owner>.<table>` | `@tab2 soe.orders` |
| **cons.sql** | constraint, table, foreign, key | Constraint information | `@cons <owner>.<table>` | `@cons soe.orders` |
| **cons2.sql** | constraint, extended, details | Extended constraint details | `@cons2 <owner>.<table>` | `@cons2 soe.orders` |
| **dep.sql** | dependencies, object, referenced, uses | Object dependencies | `@dep <owner>.<object>` | `@dep soe.orders` |
| **partmon.sql** | partition, monitoring, usage, tracking | Partition monitoring | `@partmon <owner>.<table>` | `@partmon soe.orders` |
| **segstat.sql** | segment, statistics, io, activity | Segment statistics | `@segstat <owner>.<segment>` | `@segstat soe.orders` |
| **segstat2.sql** | segment, statistics, extended, detail | Extended segment statistics | `@segstat2 <owner>.<segment>` | `@segstat2 soe.orders` |
| **segcachedx.sql** | segment, cached, buffer, blocks, extended | Extended buffered blocks for segment | `@segcachedx <owner>.<segment>` | `@segcachedx soe.orders` |

---

## Session Monitoring - Complete

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **s.sql** | session, wait, event, sql, sid, current | Display current session wait and SQL_ID info | `@s <sid>` | `@s 123` |
| **ses.sql** | session, statistics, stats, sesstat, metric | Display session statistics filtered by statistic name | `@ses <sid> <statname>` | `@ses 10 %` |
| **ses2.sql** | session, statistics, nonzero | Display session statistics (only non-zero values) | `@ses2 <sid> <statname>` | `@ses2 10 %` |
| **sid.sql** | session, sid, information | Display session by SID | `@sid <sid>` | `@sid 123` |
| **saddr.sql** | session, address, saddr | Display session by address | `@saddr <saddr>` | `@saddr 12345678` |
| **usid.sql** | session, user, process, spid | Display user session and process info | `@usid <sid>` | `@usid 123` |
| **uu.sql** | user, session, connected, active | Display user sessions | `@uu <username>` | `@uu SOE` |
| **us.sql** | user, username, dba_users, account | Display database users from DBA_USERS | `@us <username>` | `@us APP%` |
| **a.sql** | active, sessions, count, current | Display current active sessions with counts | `@a` | `@a` |
| **as.sql** | active, sessions, grouped, column | Active sessions grouped by specified column | `@as <column>` | `@as username` |
| **asql.sql** | active, sessions, sql, sqlid | Active sessions with their current SQL_IDs | `@asql` | `@asql` |
| **ba.sql** | background, active | Display active background sessions | `@ba` | `@ba` |
| **long.sql** | long, operation, progress, rman | Display session long operations with progress | `@long <filter>` | `@long 1=1` |
| **sinfo.sql** | session, information, detailed | Detailed session information | `@sinfo <sid>` | `@sinfo 123` |

---

## Wait & Event Analysis - Complete

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **sed.sql** | event, description, wait, parameter | Display wait event description and parameters | `@sed <event>` | `@sed "log file sync"` |
| **sed2.sql** | event, description, extended | Extended wait event descriptions | `@sed2 <event>` | `@sed2 "enq: TX"` |
| **sedn.sql** | event, description, name | Wait event by name | `@sedn <event>` | `@sedn "db file"` |
| **sedx.sql** | event, description, x$ | Wait event from X$ tables | `@sedx <event>` | `@sedx %` |
| **evh.sql** | event, histogram, wait, time, distribution | Display histogram of wait event counts | `@evh <event>` | `@evh "log file sync"` |
| **ev.sql** | event, trace, enable | Enable event tracing | `@ev <event> <level>` | `@ev 10046 12` |
| **evi.sql** | event, immediate, trace | Immediate event trace | `@evi <event> <level>` | `@evi heapdump 1` |
| **evo.sql** | event, off, disable | Disable event tracing | `@evo` | `@evo` |
| **evts.sql** | events, dump, system | System event dump | `@evts` | `@evts` |
| **sw.sql** | session, wait, current | Display current session wait info | `@sw <sid>` | `@sw 123` |
| **sw2.sql** | session, wait, extended | Extended session wait info | `@sw2 <sid>` | `@sw2 123` |
| **swh.sql** | session, wait, history | Session wait history | `@swh <sid>` | `@swh 123` |
| **swc.sql** | session, wait, chain | Session wait chain signatures | `@swc <sid>` | `@swc 123` |
| **swa.sql** | session, wait, all | All session waits | `@swa <sid>` | `@swa 123` |
| **swag.sql** | session, wait, aggregate | Aggregated session waits | `@swag <filter>` | `@swag 1=1` |
| **swani.sql** | session, wait, non-idle | Non-idle session waits | `@swani <sid>` | `@swani 123` |
| **swb.sql** | session, wait, blocking | Blocking session waits | `@swb <sid>` | `@swb 123` |
| **swf.sql** | session, wait, file | Session wait by file | `@swf <sid>` | `@swf 123` |
| **swg.sql** | session, wait, grouped | Session waits grouped by state | `@swg <sid>` | `@swg 123` |
| **swo.sql** | session, wait, oracle | Oracle session wait | `@swo <sid>` | `@swo 123` |
| **swp.sql** | session, wait, p1p2p3 | Session wait parameters | `@swp <sid>` | `@swp 123` |
| **swu.sql** | session, wait, user | User session waits | `@swu <filter>` | `@swu 1=1` |
| **swug.sql** | session, wait, user, grouped | User session waits grouped | `@swug <filter>` | `@swug 1=1` |
| **waitprof.sql** | wait, profiler, sampling | Session Wait Profiler - high frequency sampling | `@waitprof <samples>` | `@waitprof 10000` |
| **snapwait.sql** | snapshot, wait, event | Take snapshot of wait event | `@snapwait <seconds> <event>` | `@snapwait 5 "log file sync"` |

---

## Lock/Latch/Mutex Analysis - Complete

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **lock.sql** | lock, enqueue, blocking, mode | Display current locks with type and mode | `@lock <filter>` | `@lock 1=1` |
| **glock.sql** | lock, global, rac | Display global locks (RAC) | `@glock <filter>` | `@glock 1=1` |
| **ulock.sql** | lock, user, session | Display user locks | `@ulock <filter>` | `@ulock 1=1` |
| **latchprof.sql** | latch, holder, profiling, contention | High-frequency sampling on V$LATCHHOLDER | `@latchprof <group_cols> <sid> <latch> <samples>` | `@latchprof name,sqlid % % 100000` |
| **latchprofx.sql** | latch, profiling, extended | Extended latch profiling | `@latchprofx <group_cols> <sid> <latch> <samples>` | `@latchprofx name,sqlid % "shared pool" 100000` |
| **latchprof_old.sql** | latch, profiling, legacy | Legacy latch profiling | `@latchprof_old <sid> <latch> <samples>` | `@latchprof_old % % 10000` |
| **l.sql** | latch, stats, v$latch | Display latch stats from V$LATCH | `@l <latch>` | `@l "shared pool"` |
| **la.sql** | latch, address | Latch by address | `@la <laddr>` | `@la 12345678` |
| **lc.sql** | latch, children, stats | Display latch children stats | `@lc <latch>` | `@lc "cache buffers"` |
| **lh.sql** | latch, holder | Display latch holder | `@lh` | `@lh` |
| **lhp.sql** | latch, holder, profile | Latch holder profile | `@lhp <group_cols> <sid> <latch> <samples>` | `@lhp name,sqlid % % 10000` |
| **lhpx.sql** | latch, holder, profile, extended | Extended latch holder profile | `@lhpx <group_cols> <sid> <latch> <samples>` | `@lhpx name,sqlid % % 10000` |
| **lm.sql** | latch, misses | Display latch misses | `@lm` | `@lm` |
| **lt.sql** | lock, type, info | Display lock type info | `@lt <type>` | `@lt TX` |
| **ltx.sql** | lock, type, extended | Extended lock type info | `@ltx <type>` | `@ltx TM` |
| **mutexprof.sql** | mutex, profiler, cursor | Mutex sleep profiler | `@mutexprof <group_cols> <filter> <samples>` | `@mutexprof sid,sql_id 1=1 10000` |
| **mp.sql** | mutex, profile, quick | Quick mutex profile | `@mp` | `@mp` |

---

## Memory & Buffer Management - Complete

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **sga.sql** | sga, memory, system, global | Display SGA memory breakdown | `@sga` | `@sga` |
| **sgastat.sql** | sga, memory, shared, pool, detailed | Display detailed SGA information | `@sgastat <name>` | `@sgastat "free memory"` |
| **sgastatx.sql** | sga, memory, x$, extended | Extended SGA stats from X$ | `@sgastatx <name>` | `@sgastatx %` |
| **sgai.sql** | sga, information | SGA information | `@sgai` | `@sgai` |
| **sgares.sql** | sga, resize, operations | SGA resize operations | `@sgares` | `@sgares` |
| **sgav.sql** | sga, values | SGA values | `@sgav` | `@sgav` |
| **pga.sql** | pga, program, global, memory | Display PGA manager statistics | `@pga` | `@pga` |
| **pgav.sql** | pga, values | PGA values | `@pgav` | `@pgav` |
| **mem.sql** | memory, sga, dynamic, component | Display dynamic SGA components | `@mem` | `@mem` |
| **memres.sql** | memory, resize, history | Memory resize history | `@memres` | `@memres` |
| **smem.sql** | session, memory, pga, uga | Display session memory usage | `@smem <sid>` | `@smem 123` |
| **smem_detail.sql** | session, memory, detail | Detailed session memory | `@smem_detail <sid>` | `@smem_detail 123` |
| **pmem.sql** | process, memory, pga | Display process memory usage | `@pmem <spid>` | `@pmem 12345` |
| **pmem_detail.sql** | process, memory, detail | Detailed process memory | `@pmem_detail <spid>` | `@pmem_detail 12345` |
| **spmem.sql** | shared, pool, memory | Shared pool memory (WARNING: causes contention) | `@spmem` | `@spmem` |
| **wrka.sql** | pga, workarea, temp, sort | Display PGA and TEMP usage by session | `@wrka <filter>` | `@wrka 1=1` |
| **wrkasum.sql** | pga, workarea, summary | Display workarea summary | `@wrkasum <filter>` | `@wrkasum 1=1` |
| **wrk.sql** | workarea, memory, temp | Workarea memory and temp usage | `@wrk` | `@wrk` |
| **bhla.sql** | buffer, header, latch | Buffer headers by latch address | `@bhla` | `@bhla` |
| **bh_by_ts.sql** | buffer, cache, tablespace | Buffer cache by tablespace | `@bh_by_ts` | `@bh_by_ts` |
| **bhcls.sql** | buffer, header, class | Buffer headers by class | `@bhcls` | `@bhcls` |
| **bhdo.sql** | buffer, header, data, object | Buffer headers by data object | `@bhdo` | `@bhdo` |
| **bhfp.sql** | buffer, header, file, pool | Buffer headers by file pool | `@bhfp` | `@bhfp` |
| **bhobjects.sql** | buffer, objects, cached | Buffer cached objects | `@bhobjects` | `@bhobjects` |
| **bhobjects2.sql** | buffer, objects, cached, extended | Extended buffer cached objects | `@bhobjects2` | `@bhobjects2` |
| **bufprof.sql** | buffer, profiler, gets | Buffer Get Profiler | `@bufprof <sid> <samples>` | `@bufprof 123 10000` |
| **bufp.sql** | buffer, pool | Buffer pool | `@bufp` | `@bufp` |
| **rowcache.sql** | row, cache, dictionary | Row cache statistics | `@rowcache <name>` | `@rowcache %` |
| **heap6.sql** | heap, memory, dump | Heap memory dump | `@heap6` | `@heap6` |
| **subheap.sql** | subheap, memory | Subheap memory | `@subheap` | `@subheap` |

---

## System Statistics & Monitoring - Complete

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **sys.sql** | system, statistics, sysstat | Display system-level statistics | `@sys <statname>` | `@sys redo` |
| **sysm.sql** | system, metrics, v$metric | Display system metrics from V$METRIC | `@sysm <metric>` | `@sysm "CPU"` |
| **sysopt.sql** | system, optimizer, environment | System default compilation environment | `@sysopt <param>` | `@sysopt %` |
| **aw.sql** | activity, what, now, current | "What's going on?!" - Current system activity | `@aw <filter>` | `@aw 1=1` |
| **w.sql** | what, now, activity | What's going on right now? | `@w` | `@w` |
| **w4.sql** | what, now, activity, variant | What's going on variant | `@w4` | `@w4` |
| **bg.sql** | background, process, dbwr, lgwr | Display background process information | `@bg <process>` | `@bg dbw` |
| **bg2.sql** | background, process, extended | Extended background process info | `@bg2 <process>` | `@bg2 %` |
| **bgact.sql** | background, activity | Background process activity | `@bgact` | `@bgact` |
| **metric.sql** | metric, system, performance | System metric | `@metric <metric>` | `@metric %` |
| **statn.sql** | statistic, name | Statistic by name | `@statn <name>` | `@statn "redo"` |
| **top.sql** | top, activity | Top activity | `@top` | `@top` |
| **topmsh.sql** | top, mutex, sleep, holder | Top mutex sleep holders | `@topmsh` | `@topmsh` |
| **topsql.sql** | top, sql, ordered | Top SQL by specified criteria | `@topsql <order_by>` | `@topsql elapsed_time` |
| **mys.sql** | my, session, statistics | Current session statistics | `@mys <stat>` | `@mys %` |
| **mysid.sql** | my, sid, current | Current session SID | `@mysid` | `@mysid` |
| **mysx.sql** | my, session, extended | Extended current session stats | `@mysx` | `@mysx` |
| **vstat.sql** | v$, statistic, system | System metrics per-minute | `@vstat` | `@vstat` |

---

## Transaction & Undo - Complete

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **trans.sql** | transaction, undo, ublk, xid | Display active transactions with undo usage | `@trans <filter>` | `@trans 1=1` |
| **gtrans.sql** | transaction, global, x$k2gte2 | Display global transactions | `@gtrans` | `@gtrans` |
| **uds.sql** | undo, statistics | Undo statistics from V$UNDOSTAT | `@uds` | `@uds` |
| **snapundo.sql** | snapshot, undo | Take snapshot of undo usage | `@snapundo <seconds>` | `@snapundo 5` |
| **ktuxe.sql** | transaction, undo, extent | Transaction undo extent info | `@ktuxe` | `@ktuxe` |

---

## Redo & Archive Logs - Complete

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **log.sql** | redo, log, online, logfile | Display redo log file layout | `@log` | `@log` |
| **curlog.sql** | redo, log, current, active | Display current redo log | `@curlog` | `@curlog` |
| **logfile.sql** | log, file, redo | Redo log files | `@logfile` | `@logfile` |
| **alog.sql** | archive, log | Archive log information | `@alog` | `@alog` |
| **snapredo.sql** | snapshot, redo | Take snapshot of redo generation | `@snapredo <seconds>` | `@snapredo 5` |
| **minelog.sql** | mine, log, logminer | Logminer log info | `@minelog` | `@minelog` |
| **rman_archlogs.sql** | rman, archive, logs | RMAN archive log info | `@rman_archlogs` | `@rman_archlogs` |

---

## ASM (Automatic Storage Management) - Complete

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **asmdf.sql** | asm, diskgroup, file | ASM disk file info | `@asmdf <diskgroup>` | `@asmdf DATA` |
| **asmdg.sql** | asm, diskgroup | ASM disk group info | `@asmdg <diskgroup>` | `@asmdg %` |
| **asmdump.sql** | asm, dump | ASM dump | `@asmdump` | `@asmdump` |
| **asmdumpf.sql** | asm, dump, file | ASM file dump | `@asmdumpf <file>` | `@asmdumpf +DATA/db/datafile/system.123` |
| **asmls.sql** | asm, list | ASM list | `@asmls` | `@asmls` |

---

## Space & Storage Management - Complete

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **df.sql** | datafile, tablespace, space, free | Show tablespace free space (GB) | `@df` | `@df` |
| **dfm.sql** | datafile, tablespace, space, megabytes | Show tablespace free space (MB) | `@dfm` | `@dfm` |
| **ts.sql** | tablespace, datafile, storage | Display tablespace information | `@ts <tablespace>` | `@ts USERS` |
| **ls.sql** | tablespace, list, datafile | Display tablespace with datafiles | `@ls <tablespace>` | `@ls system` |
| **tsv.sql** | tablespace, values | Tablespace values | `@tsv <tablespace>` | `@tsv %` |
| **topseg.sql** | segment, top, space, largest | Display top space users per tablespace | `@topseg <tablespace>` | `@topseg %` |
| **topseg2.sql** | segment, top, collapsed | Top segments collapsed to table/index level | `@topseg2 <tablespace>` | `@topseg2 USERS` |
| **seg.sql** | segment, storage, space, bytes | Display segment storage information | `@seg <owner>.<segment>` | `@seg soe.orders` |
| **seg2.sql** | segment, extended | Extended segment info | `@seg2 <owner>.<segment>` | `@seg2 soe.orders` |
| **segext.sql** | segment, extent | Segment extent info | `@segext <owner>.<segment>` | `@segext soe.orders` |
| **segext2.sql** | segment, extent, extended | Extended segment extent info | `@segext2 <owner>.<segment>` | `@segext2 soe.orders` |
| **segeof.sql** | segment, eof | Segment end of file info | `@segeof <owner>.<segment>` | `@segeof soe.orders` |
| **segstat.sql** | segment, statistics | Segment statistics | `@segstat <owner>.<segment>` | `@segstat soe.orders` |
| **segstat2.sql** | segment, statistics, extended | Extended segment statistics | `@segstat2 <owner>.<segment>` | `@segstat2 soe.orders` |
| **segstatint.sql** | segment, statistics, interval | Segment statistics interval | `@segstatint <owner>.<segment>` | `@segstatint soe.orders` |
| **segsum.sql** | segment, summary | Segment summary | `@segsum <owner>.<segment>` | `@segsum soe.orders` |
| **segcached.sql** | segment, buffer, cache, cached | Display buffered blocks for segment | `@segcached <owner>.<segment>` | `@segcached soe.orders` |
| **segcachedx.sql** | segment, cached, extended | Extended cached segment info | `@segcachedx <owner>.<segment>` | `@segcachedx soe.orders` |
| **topsegstat.sql** | segment, statistics, top | Top segment-level statistics | `@topsegstat <stat>` | `@topsegstat reads` |
| **du.sql** | disk, usage, size | Disk usage | `@du <owner>` | `@du SOE` |
| **du2.sql** | disk, usage, extended | Extended disk usage | `@du2 <owner>` | `@du2 SOE` |
| **temp.sql** | temp, tablespace, usage | Temp tablespace usage | `@temp` | `@temp` |

---

## Object Information - Complete

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **tab.sql** | table, segment, storage, statistics | Display table information | `@tab <owner>.<table>` | `@tab soe.orders` |
| **tab2.sql** | table, extended, information | Extended table information | `@tab2 <owner>.<table>` | `@tab2 soe.orders` |
| **ind.sql** | index, key, column, statistics | Display index information | `@ind <owner>.<index>` | `@ind soe.ord_ix` |
| **ind2.sql** | index, extended, information | Extended index information | `@ind2 <owner>.<index>` | `@ind2 soe.ord_ix` |
| **indf.sql** | index, full, detailed | Detailed index information | `@indf <owner>.<index>` | `@indf soe.ord_ix` |
| **indroot.sql** | index, root, block | Index root block info | `@indroot <owner>.<index>` | `@indroot soe.ord_ix` |
| **o.sql** | object, dba_objects, owner | Display database object information | `@o <owner>.<object>` | `@o sys.dba_users` |
| **o2.sql** | object, extended | Extended object info | `@o2 <owner>.<object>` | `@o2 sys.%` |
| **descxx.sql** | describe, table, column, extended | Describe table with extended column info | `@descxx <object>` | `@descxx soe.orders` |
| **descx.sql** | describe, extended | Extended describe | `@descx <object>` | `@descx soe.orders` |
| **descx2.sql** | describe, extended, variant | Extended describe variant | `@descx2 <object>` | `@descx2 soe.orders` |
| **descxx11.sql** | describe, extended, 11g | Extended describe for 11g | `@descxx11 <object>` | `@descxx11 soe.orders` |
| **descxx2.sql** | describe, extended, variant | Extended describe variant 2 | `@descxx2 <object>` | `@descxx2 soe.orders` |
| **desc.sql** | describe, table | Basic describe | `@desc <object>` | `@desc soe.orders` |
| **descpartxx.sql** | describe, partition, extended | Describe partition extended | `@descpartxx <owner>.<table>` | `@descpartxx soe.orders` |
| **col.sql** | column, table, datatype | Display columns matching pattern | `@col <column>` | `@col %date%` |
| **cons.sql** | constraint, table, foreign | Constraint information | `@cons <owner>.<table>` | `@cons soe.orders` |
| **cons2.sql** | constraint, extended | Extended constraint info | `@cons2 <owner>.<table>` | `@cons2 soe.orders` |
| **dep.sql** | dependencies, object, referenced | Object dependencies | `@dep <owner>.<object>` | `@dep soe.orders` |
| **syn.sql** | synonym, alias, object | Display synonym information | `@syn <synonym>` | `@syn tab` |
| **syn2.sql** | synonym, extended | Extended synonym info | `@syn2 <synonym>` | `@syn2 tab` |
| **seq.sql** | sequence, generator, nextval | Display sequence information | `@seq <sequence>` | `@seq sys.jobseq` |
| **seq2.sql** | sequence, extended | Extended sequence info | `@seq2 <sequence>` | `@seq2 sys.%` |
| **lob.sql** | lob, large, object, clob, blob | Display LOB segment information | `@lob <owner>.<table>` | `@lob soe.customers` |
| **tabpart.sql** | partition, table, segment | Display table partition information | `@tabpart <owner>.<table>` | `@tabpart soe.orders` |
| **tabsubpart.sql** | subpartition, composite | Display table subpartition information | `@tabsubpart <owner>.<table>` | `@tabsubpart soe.orders` |
| **partkeys.sql** | partition, key, column | Display table partition key columns | `@partkeys <owner>.<table>` | `@partkeys soe.orders` |
| **partmon.sql** | partition, monitoring | Partition monitoring | `@partmon <owner>.<table>` | `@partmon soe.orders` |
| **partpruning.sql** | partition, pruning | Partition pruning info | `@partpruning <owner>.<table>` | `@partpruning soe.orders` |
| **tabhist.sql** | histogram, statistics, column | Display column histograms | `@tabhist <owner>.<table> <column>` | `@tabhist soe.orders order_mode` |
| **tabhisthybrid.sql** | histogram, hybrid | Hybrid histogram info | `@tabhisthybrid <owner>.<table> <column>` | `@tabhisthybrid soe.orders status` |
| **colusage.sql** | column, usage, tracking | Display column usage tracking | `@colusage <owner>.<table>` | `@colusage soe.orders` |
| **colltypes.sql** | collection, types | Collection types | `@colltypes <owner>` | `@colltypes SYS` |
| **ddl.sql** | ddl, create, definition | Extract DDL statements for objects | `@ddl <owner>.<object>` | `@ddl sys.dba_users` |
| **proc.sql** | procedure, function, package | Display procedures and functions | `@proc <object> <proc>` | `@proc dbms_stats %` |
| **procid.sql** | procedure, id | Procedure by ID | `@procid <object_id>` | `@procid 12345` |
| **trig.sql** | trigger, event, timing | Display trigger information | `@trig <trigger>` | `@trig sys.%` |
| **trigger.sql** | trigger, full | Full trigger info | `@trigger <trigger>` | `@trigger sys.%` |
| **typ.sql** | type, object, udt | Type information | `@typ <type>` | `@typ %` |
| **typ2.sql** | type, extended | Extended type info | `@typ2 <type>` | `@typ2 %` |
| **inv.sql** | invalid, objects, indexes | Show invalid objects | `@inv` | `@inv` |
| **source.sql** | source, code, plsql | Source code | `@source <owner>.<object>` | `@source sys.dbms_output` |
| **source2.sql** | source, extended | Extended source view | `@source2 <owner>.<object>` | `@source2 sys.dbms_output` |

---

## Parameters & Configuration - Complete

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **p.sql** | parameter, value, init | Display parameter name and value | `@p <param>` | `@p optimizer` |
| **pd.sql** | parameter, description | Display parameter with description | `@pd <param>` | `@pd optimizer` |
| **pd2.sql** | parameter, description, x$ | Parameter from x$ksppi/x$ksppcv | `@pd2 <param>` | `@pd2 %` |
| **pv.sql** | parameter, value, search | Display parameters by value | `@pv <value>` | `@pv MANUAL` |
| **pvalid.sql** | parameter, valid, values | Display valid parameter values | `@pvalid <param>` | `@pvalid optimizer` |
| **pn.sql** | parameter, number | Parameter number | `@pn <param>` | `@pn %` |
| **pdv.sql** | parameter, default, value | Parameter default value | `@pdv <param>` | `@pdv %` |
| **pdbs.sql** | pdb, container, pluggable | PDB/container info | `@pdbs` | `@pdbs` |
| **sp.sql** | spfile, parameter | Show SPFILE parameters | `@sp <param>` | `@sp %` |
| **init.sql** | initialize, sqlplus, settings | Initialize sqlplus variables | `@init` | `@init` |
| **login.sql** | login, session, setup | Login script | `@login` | `@login` |
| **i.sql** | whoami, session, identity | Who am I script | `@i` | `@i` |
| **dirs.sql** | directory, path, external | Display database directory objects | `@dirs` | `@dirs` |
| **dir.sql** | directory, single | Single directory | `@dir <dir>` | `@dir DATA_PUMP_DIR` |
| **dblinks.sql** | database, link, dblink | Display database links | `@dblinks` | `@dblinks` |
| **dbinfo.sql** | database, information | Database information | `@dbinfo` | `@dbinfo` |
| **db.sql** | database, v$database | V$DATABASE info | `@db` | `@db` |
| **dg.sql** | dataguard, standby | Data Guard info | `@dg` | `@dg` |
| **nls.sql** | nls, language, territory | NLS settings | `@nls` | `@nls` |
| **userenv.sql** | userenv, environment | Userenv values | `@userenv` | `@userenv` |
| **roles.sql** | roles, privileges | Role information | `@roles <role>` | `@roles DBA` |
| **privs.sql** | privileges, grants | Privileges | `@privs <user>` | `@privs SOE` |
| **privs2.sql** | privileges, extended | Extended privileges | `@privs2 <user>` | `@privs2 SOE` |
| **syspriv.sql** | system, privileges | System privileges | `@syspriv <priv>` | `@syspriv %` |
| **oprivs.sql** | object, privileges | Object privileges | `@oprivs <object>` | `@oprivs soe.orders` |
| **oprivs2.sql** | object, privileges, extended | Extended object privileges | `@oprivs2 <object>` | `@oprivs2 soe.%` |
| **sprivs.sql** | session, privileges | Session privileges | `@sprivs` | `@sprivs` |
| **sprivs2.sql** | session, privileges, extended | Extended session privileges | `@sprivs2` | `@sprivs2` |
| **privgrants.sql** | privilege, grants | Privilege grants | `@privgrants <user>` | `@privgrants SOE` |
| **privgrants2.sql** | privilege, grants, extended | Extended privilege grants | `@privgrants2 <user>` | `@privgrants2 SOE` |

---

## Tracing & Diagnostics - Complete

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **trace.sql** | trace, sql_trace, 10046, enable | Generate commands to enable SQL tracing | `@trace <filter>` | `@trace sid=123` |
| **traceme.sql** | trace, sql_trace, current, self | Enable SQL tracing for current session | `@traceme` | `@traceme` |
| **traceoff.sql** | trace, sql_trace, disable | Disable SQL tracing | `@traceoff <filter>` | `@traceoff sid=123` |
| **tracesid.sql** | trace, sid, enable | Enable trace for SID | `@tracesid <sid>` | `@tracesid 123` |
| **tracesidoff.sql** | trace, sid, disable | Disable trace for SID | `@tracesidoff <sid>` | `@tracesidoff 123` |
| **46on.sql** | trace, 10046, sql, enable | Enable 10046 SQL trace | `@46on <sid>` | `@46on 123` |
| **46off.sql** | trace, 10046, sql, disable | Disable 10046 SQL trace | `@46off <sid>` | `@46off 123` |
| **53on.sql** | trace, 10053, cbo, enable | Enable 10053 CBO trace | `@53on <sid>` | `@53on 123` |
| **53off.sql** | trace, 10053, cbo, disable | Disable 10053 CBO trace | `@53off <sid>` | `@53off 123` |
| **53trace.sql** | trace, 10053, sql_id | 10053 trace for SQL_ID | `@53trace <sql_id>` | `@53trace 7q729nhdgtsqq` |
| **diag.sql** | diagnostic, information | Display diagnostic information | `@diag` | `@diag` |
| **diag_sid.sql** | diagnostic, sid | Diagnostic info for SID | `@diag_sid <sid>` | `@diag_sid 123` |
| **ostackprof.sql** | stack, profiling, os | OS stack profiling | `@ostackprof <spid> <samples>` | `@ostackprof 12345 1000` |
| **ostackprofu.sql** | stack, profiling, unix | OS stack profiling Unix | `@ostackprofu <spid> <samples>` | `@ostackprofu 12345 1000` |
| **ostackprofw.sql** | stack, profiling, windows | OS stack profiling Windows | `@ostackprofw <spid> <samples>` | `@ostackprofw 12345 1000` |
| **ostack.sql** | stack, oracle | Oracle stack | `@ostack <spid>` | `@ostack 12345` |
| **dump.sql** | dump, block, file | Block dump | `@dump <file#> <block#> <what>` | `@dump 1 100 %` |
| **dumptrc.sql** | dump, trace, file | Dump trace file | `@dumptrc` | `@dumptrc` |
| **dumpvar.sql** | dump, variable | Dump variable | `@dumpvar <var>` | `@dumpvar %` |
| **get_trace.sql** | get, trace, file | Get trace file | `@get_trace` | `@get_trace` |
| **get_trace2.sql** | get, trace, extended | Get trace extended | `@get_trace2` | `@get_trace2` |
| **gettracename.sql** | trace, name, file | Get trace file name | `@gettracename` | `@gettracename` |
| **pxtrace.sql** | parallel, trace | Parallel execution trace | `@pxtrace` | `@pxtrace` |

---

## SQL Tuning - Complete

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **create_sql_baseline.sql** | sql, baseline, plan, spm | Create SQL Plan Baseline from good cursor | `@create_sql_baseline <good_sqlid> <good_phv> <target_sqlid>` | `@create_sql_baseline abc123 12345 xyz789` |
| **create_sql_baseline_awr.sql** | sql, baseline, awr | Create SQL Plan Baseline from AWR | `@create_sql_baseline_awr <sql_id> <phv>` | `@create_sql_baseline_awr abc123 12345` |
| **create_sql_patch.sql** | sql, patch, hint | Create SQL patch to inject hints | `@create_sql_patch <sql_id> <hint>` | `@create_sql_patch abc123 "FULL(t)"` |
| **create_sql_profile.sql** | sql, profile, tuning | Create SQL profile from hints | `@create_sql_profile <sql_id> <hints>` | `@create_sql_profile abc123 "FULL(@SEL$1 T)"` |
| **drop_sql_baseline.sql** | sql, baseline, drop | Drop SQL Plan Baseline | `@drop_sql_baseline <sql_handle>` | `@drop_sql_baseline SQL_123abc` |
| **drop_sql_patch.sql** | sql, patch, drop | Drop SQL patch | `@drop_sql_patch <patch_name>` | `@drop_sql_patch SQL_PATCH_abc` |
| **drop_sql_profile.sql** | sql, profile, drop | Drop SQL profile | `@drop_sql_profile <profile_name>` | `@drop_sql_profile SYS_SQLPROF_123` |
| **hint.sql** | hint, optimizer, list | Display all available optimizer hints | `@hint <name>` | `@hint full` |
| **hinth.sql** | hint, hierarchy | Hint hierarchy | `@hinth <name>` | `@hinth %` |
| **hintclass.sql** | hint, class | Hints by class | `@hintclass <class>` | `@hintclass merge` |
| **hintfeature.sql** | hint, feature | Hints by feature | `@hintfeature <feature>` | `@hintfeature %` |
| **otherxml.sql** | other, xml, plan | OTHER_XML from execution plan | `@otherxml <sql_id> <child#>` | `@otherxml 7q729nhdgtsqq 0` |
| **otherxmlhints.sql** | other, xml, hints | Hints from OTHER_XML | `@otherxmlhints <sql_id>` | `@otherxmlhints 7q729nhdgtsqq` |

---

## Parallel Execution - Complete

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **px.sql** | parallel, execution, sql, rac | Report Parallel Execution SQL globally | `@px` | `@px` |
| **px2.sql** | parallel, execution, sessions | Show current PX sessions in RAC | `@px2` | `@px2` |
| **pxs.sql** | parallel, execution, qc, slaves | Display PX QC and slave sessions | `@pxs <qc_sid>` | `@pxs 123` |
| **tq.sql** | table, queue, px | Show PX Table Queue statistics | `@tq` | `@tq` |
| **asfp.sql** | alter, session, force, parallel | Force parallel query | `@asfp <degree>` | `@asfp 4` |

---

## Session/Process Management - Complete

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **kill.sql** | kill, terminate, session | Generate ALTER SYSTEM KILL SESSION | `@kill <filter>` | `@kill sid=123` |
| **killi.sql** | kill, immediate | Kill session immediately | `@killi <filter>` | `@killi sid=123` |
| **cancel.sql** | cancel, sql, statement | Generate ALTER SYSTEM CANCEL SQL | `@cancel <filter>` | `@cancel sid=123` |
| **disco.sql** | disconnect, session | Generate disconnect commands | `@disco <filter>` | `@disco username='APP'` |
| **pinfo.sql** | process, information | Process information | `@pinfo <spid>` | `@pinfo 12345` |
| **paddr.sql** | process, address | Process by address | `@paddr <paddr>` | `@paddr 12345678` |
| **ksupr.sql** | process, x$ | Process from X$KSUPR | `@ksupr` | `@ksupr` |
| **ksuse.sql** | session, x$ | Session from X$KSUSE | `@ksuse` | `@ksuse` |

---

## Scheduler/Jobs - Complete

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **jobs.sql** | job, scheduler, dbms_job | Display scheduled jobs and status | `@jobs` | `@jobs` |
| **jobsr.sql** | job, running | Running jobs | `@jobsr` | `@jobsr` |
| **jobdisable.sql** | job, disable | Disable job | `@jobdisable <job>` | `@jobdisable 123` |

---

## Data Dictionary & Utilities - Complete

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **d.sql** | dictionary, view, dba, x$ | Display data dictionary views and X$ tables | `@d <pattern>` | `@d %session%` |
| **d2.sql** | dictionary, extended | Extended dictionary search | `@d2 <pattern>` | `@d2 sql` |
| **help.sql** | help, search, documentation | Search and display help for TPT scripts | `@help <pattern>` | `@help explain` |
| **f.sql** | fixed, view, v$ | Search Fixed view text | `@f <pattern>` | `@f session` |
| **fv.sql** | fixed, variable, sga | Fixed SGA Variables | `@fv <pattern>` | `@fv %` |
| **fv2.sql** | fixed, variable, extended | Extended fixed variables | `@fv2 <pattern>` | `@fv2 %` |
| **fva.sql** | fixed, variable, all | All fixed variables | `@fva <pattern>` | `@fva %` |
| **fval.sql** | fixed, value | Fixed value | `@fval <pattern>` | `@fval %` |
| **fval2.sql** | fixed, value, extended | Extended fixed value | `@fval2 <pattern>` | `@fval2 %` |
| **calc.sql** | calculator, hex, dec | Basic calculator and hex/dec converter | `@calc <expression>` | `@calc 1024*1024` |
| **ascii.sql** | ascii, character | ASCII values | `@ascii <char>` | `@ascii A` |
| **chr.sql** | chr, character | Character from code | `@chr <code>` | `@chr 65` |
| **hex.sql** | hex, hexadecimal | Hex conversion | `@hex <value>` | `@hex 255` |
| **hexop.sql** | hex, operation | Hex operations | `@hexop <value>` | `@hexop 0xFF` |
| **bitmask.sql** | bitmask, binary | Bitmask operations | `@bitmask <value>` | `@bitmask 255` |
| **rowid.sql** | rowid, file, block | Show file, block, row from rowid | `@rowid <rowid>` | `@rowid AAABcDAAEAAAABdAAA` |
| **mkdba.sql** | make, dba, file, block | Make DBA from file# and block# | `@mkdba <file#> <block#>` | `@mkdba 1 100` |
| **dba.sql** | dba, translate | Translate file#/block# to segment | `@dba <file#> <block#>` | `@dba 1 100` |
| **dba2.sql** | dba, translate, extended | Extended DBA translation | `@dba2 <file#> <block#>` | `@dba2 1 100` |
| **doid.sql** | data, object, id | Data object by ID | `@doid <object_id>` | `@doid 12345` |
| **oid.sql** | object, id | Object by ID | `@oid <object_id>` | `@oid 12345` |
| **hash.sql** | hash, value, sql_id | Display hash value, SQL_ID of last SQL | `@hash` | `@hash` |
| **i2h.sql** | sql_id, hash, convert | SQL ID to Hash value | `@i2h <sql_id>` | `@i2h 7q729nhdgtsqq` |
| **ora_hash.sql** | ora_hash, function | ORA_HASH function | `@ora_hash <value>` | `@ora_hash 'test'` |
| **date.sql** | date, format | Date format | `@date` | `@date` |
| **date2unix.sql** | date, unix, convert | Date to Unix timestamp | `@date2unix <date>` | `@date2unix sysdate` |
| **unix2date.sql** | unix, date, convert | Unix timestamp to date | `@unix2date <timestamp>` | `@unix2date 1704672000` |
| **oerr.sql** | error, ora, message | ORA error message | `@oerr <error#>` | `@oerr 1555` |
| **oerrh.sql** | error, ora, help, docs | ORA error help (opens docs) | `@oerrh <error#>` | `@oerrh 1555` |
| **oerrign.sql** | error, ignore | Ignore error | `@oerrign <error#>` | `@oerrign 1555` |
| **res.sql** | reserved, words | Reserved words | `@res <word>` | `@res select` |
| **res2.sql** | reserved, words, extended | Extended reserved words | `@res2 <word>` | `@res2 %` |

---

## Statistics Gathering - Complete

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **gts.sql** | gather, table, statistics | Gather Table Statistics | `@gts <owner>.<table>` | `@gts soe.orders` |
| **gtsh.sql** | gather, table, statistics, histograms | Gather Table Statistics with histograms | `@gtsh <owner>.<table>` | `@gtsh soe.orders` |
| **gss.sql** | gather, schema, statistics | Gather Schema Statistics | `@gss <schema>` | `@gss SOE` |
| **cstat.sql** | cursor, statistics, execute | Execute SQL and report basic stats | `@cstat <sql>` | `@cstat "SELECT * FROM dual"` |
| **mods.sql** | modifications, table, dba_tab | Table modifications from DBA_TAB_MODIFICATIONS | `@mods <table>` | `@mods soe.%` |
| **modsx.sql** | modifications, extended | Extended table modifications | `@modsx <table>` | `@modsx soe.%` |

---

## HTML Output Scripts - Complete

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **html.sql** | html, output, format | HTML output | `@html` | `@html` |
| **html2.sql** | html, output, variant | HTML output variant 2 | `@html2` | `@html2` |
| **html3.sql** | html, output, variant | HTML output variant 3 | `@html3` | `@html3` |
| **htmlon.sql** | html, enable | Enable HTML output | `@htmlon` | `@htmlon` |
| **htmloff.sql** | html, disable | Disable HTML output | `@htmloff` | `@htmloff` |
| **htmlrun.sql** | html, run, spool | HTML spool run | `@htmlrun` | `@htmlrun` |
| **htmlset.sql** | html, settings | HTML settings | `@htmlset` | `@htmlset` |
| **htmlset2.sql** | html, settings, variant | HTML settings variant | `@htmlset2` | `@htmlset2` |
| **html_settings.sql** | html, settings, display | Display HTML settings | `@html_settings` | `@html_settings` |

---

## Snapshot/Sample Scripts - Complete

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **snapper.sql** | snapper, session, performance, ash | Session Snapper - flagship TPT tool | `@snapper <options> <seconds> <snapshots> <sid>` | `@snapper ash 5 12 all` |
| **snapper3.sql** | snapper, version3 | Snapper version 3 | `@snapper3 <options> <seconds> <snapshots> <sid>` | `@snapper3 ash 5 12 all` |
| **snapper_v1.sql** | snapper, version1 | Snapper version 1 | `@snapper_v1 <options> <seconds> <snapshots> <sid>` | `@snapper_v1 ash 5 12 all` |
| **snapper_v2.sql** | snapper, version2 | Snapper version 2 | `@snapper_v2 <options> <seconds> <snapshots> <sid>` | `@snapper_v2 ash 5 12 all` |
| **snapperloop.sql** | snapper, loop, continuous | Run Snapper continuously | `@snapperloop` | `@snapperloop` |
| **snapcpu.sql** | snapshot, cpu | Snapshot CPU usage | `@snapcpu <seconds>` | `@snapcpu 5` |
| **snapio.sql** | snapshot, io | Snapshot I/O | `@snapio <seconds>` | `@snapio 5` |
| **snaplio.sql** | snapshot, logical, io | Snapshot logical I/O | `@snaplio <seconds>` | `@snaplio 5` |
| **snappio.sql** | snapshot, physical, io | Snapshot physical I/O | `@snappio <seconds>` | `@snappio 5` |
| **snappiomb.sql** | snapshot, physical, io, mb | Snapshot physical I/O in MB | `@snappiomb <seconds>` | `@snappiomb 5` |
| **snapnet.sql** | snapshot, network | Snapshot network | `@snapnet <seconds>` | `@snapnet 5` |
| **snapsys.sql** | snapshot, system | Snapshot system stats | `@snapsys <seconds>` | `@snapsys 5` |
| **snaptime.sql** | snapshot, time | Snapshot time model | `@snaptime <seconds>` | `@snaptime 5` |
| **sample.sql** | sample, v$session | Sample V$SESSION | `@sample <interval> <count>` | `@sample 1 60` |
| **sampleaddr.sql** | sample, address | Sample by address | `@sampleaddr` | `@sampleaddr` |

---

## Miscellaneous Kernel Scripts - Complete

| Script | Keywords | Purpose | Syntax | Examples |
|--------|----------|---------|--------|----------|
| **kcbbes.sql** | kcb, background, io | Background I/O priorities from X$KCBBES | `@kcbbes` | `@kcbbes` |
| **kcboqh.sql** | kcb, object, queue | Object queue header | `@kcboqh` | `@kcboqh` |
| **kcbsw.sql** | kcb, session, wait | KCB session wait | `@kcbsw` | `@kcbsw` |
| **kcbwds.sql** | kcb, write, direct | KCB direct writes | `@kcbwds` | `@kcbwds` |
| **kcbwh.sql** | kcb, write, header | KCB write header | `@kcbwh` | `@kcbwh` |
| **kghlu.sql** | kgh, heap, memory | KGH heap memory | `@kghlu` | `@kghlu` |
| **kglbroken.sql** | kgl, broken, cursors | Broken cursors | `@kglbroken` | `@kglbroken` |
| **kgllk.sql** | kgl, lock | KGL locks | `@kgllk` | `@kgllk` |
| **kglob.sql** | kgl, object | KGL objects | `@kglob <object>` | `@kglob %` |
| **kglpn.sql** | kgl, pin | KGL pins | `@kglpn` | `@kglpn` |
| **ksllw.sql** | ksl, latch, wait | KSL latch wait | `@ksllw` | `@ksllw` |
| **ksmdd.sql** | ksm, dump, descriptor | KSM dump descriptor | `@ksmdd` | `@ksmdd` |
| **ksminfo.sql** | ksm, information | KSM information | `@ksminfo` | `@ksminfo` |
| **ksmlru.sql** | ksm, lru | KSM LRU | `@ksmlru` | `@ksmlru` |
| **ksmsp.sql** | ksm, shared, pool | KSM shared pool (WARNING: contention) | `@ksmsp` | `@ksmsp` |
| **ksmsp2.sql** | ksm, shared, pool, variant | KSM shared pool variant | `@ksmsp2` | `@ksmsp2` |
| **ksqeq.sql** | ksq, enqueue | KSQ enqueue | `@ksqeq` | `@ksqeq` |
| **ksqrs.sql** | ksq, resource | KSQ resource | `@ksqrs` | `@ksqrs` |
| **kstex.sql** | kst, extent | KST extent | `@kstex` | `@kstex` |
| **lpstat.sql** | large, pool, stats | Large pool stats from X$KSMLS | `@lpstat` | `@lpstat` |
| **npstat.sql** | shared, pool, stats | Shared pool stats from X$KSMSS | `@npstat` | `@npstat` |

---

## Common Parameter Patterns

### Session ID (SID) Parameters
- Single: `123`
- Multiple: `52,110,225`
- Subquery: `"select sid from v$session where username='XYZ'"`
- Variable: `&mysid`
- All sessions: `all`

### Time Range Parameters
- Explicit: `sysdate-1/24 sysdate` (last hour)
- Shortcuts: `&min`, `&5min`, `&hour`, `&day`, `&today`
- Timestamp: `"timestamp'2025-01-08 07:00:00'"`

### Object Name Parameters
- Specific: `soe.orders`
- Wildcard schema: `%.orders`
- Wildcard object: `soe.%`
- Wildcard both: `%table%`

### Filter Expressions
- Always true: `1=1`
- Column equality: `username='SOE'`
- Complex: `"username='APP' and program like 'sqlplus%'"`

---

## Tips for Using This Catalog

1. **Quick Lookup**: Press Ctrl+F (Cmd+F on Mac) and search for keywords
2. **Category Browse**: Scroll to the category section you need
3. **Command Line Grep**: Use grep for powerful searching
   ```bash
   grep -i "performance\|monitoring" SCRIPTS_CATALOG.md
   grep "sql_id" SCRIPTS_CATALOG.md | grep -v "^#"
   ```
4. **Copy Examples**: Examples are ready to copy and customize

---

**Legend:**
- `phv` = plan_hash_value
- `<required>` = Required parameter
- `[optional]` = Optional parameter
- `%` = Wildcard in patterns
- Parameters in quotes (`"..."`) preserve spaces and special characters

---

## See Also

- **SCRIPTS_CATALOG.txt** - Greppable text format with more details
- **SCRIPTS_CATALOG.csv** - Spreadsheet-importable format
- **help.sql** - Interactive help within SQL*Plus
- **CLAUDE.md** - AI assistant guidance for this repository
- **README.md** - Project overview and getting started

---

## Catalog Statistics

- **Total Scripts Documented:** 700+
- **Categories:** 30+
- **Complete Coverage of:**
  - ASH Analysis (69 scripts)
  - AWR Analysis (21 scripts)
  - Execution Plans (42 scripts)
  - SQL Analysis (40+ scripts)
  - Session Monitoring (15+ scripts)
  - Wait/Event Analysis (25+ scripts)
  - Lock/Latch/Mutex (17+ scripts)
  - Memory & Buffer (30+ scripts)
  - System Statistics (20+ scripts)
  - Transaction & Undo (5 scripts)
  - Redo & Archive (7 scripts)
  - ASM (5 scripts)
  - Space & Storage (25+ scripts)
  - Object Information (45+ scripts)
  - Parameters & Configuration (30+ scripts)
  - Tracing & Diagnostics (25+ scripts)
  - SQL Tuning (12 scripts)
  - Parallel Execution (5 scripts)
  - Session Management (10+ scripts)
  - Scheduler/Jobs (3 scripts)
  - Data Dictionary & Utilities (35+ scripts)
  - Statistics Gathering (6 scripts)
  - HTML Output (10 scripts)
  - Snapshot/Sample (15+ scripts)
  - Kernel Scripts (20+ scripts)

---

*Catalog updated: 2026-01-13 - Comprehensive coverage of all 700+ TPT scripts*
