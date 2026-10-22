// Curated "start here" troubleshooting workflows for directory.html.
// Hand-edited. Each step's `file` must be a repo-relative path of an existing script.
// Examples assume SQLPATH is the repo root; subfolder scripts are called as @ash/ashtop etc.
// Licensing reminders: V$ACTIVE_SESSION_HISTORY and DBA_HIST_* need the Diagnostics Pack,
// SQL Monitor / DBMS_SQLTUNE need the Tuning Pack, snapper.sql samples V$SESSION (no pack).
const WORKFLOWS = [
  {
    id: "slow-session",
    title: "A session is slow or hung",
    blurb: "Find what one session is waiting on or burning CPU for, right now.",
    steps: [
      { file: "s.sql", why: "Wait event, SQL_ID, state and blocker of the session right now", example: "@s 123" },
      { file: "snapper.sql", why: "Sample one session for 5s: waits, SQL_IDs and statistic deltas", example: "@snapper all 5 1 123",
        note: "Samples V$SESSION/V$SESSTAT only, no Diagnostics Pack needed. Use more snapshots (e.g. 5 12) for a longer view." },
      { file: "long.sql", why: "Is it inside a long operation? Progress and time left (V$SESSION_LONGOPS)", example: "@long sid=123" },
      { file: "ash/ashtop.sql", why: "What the session spent the last hour on, by event and SQL_ID", example: "@ash/ashtop event2,sql_id session_id=123 sysdate-1/24 sysdate",
        note: "Needs Diagnostics Pack license (queries GV$ACTIVE_SESSION_HISTORY). The snapper step above is the license-free equivalent." },
      { file: "usid.sql", why: "Map the session to its OS process (SPID), program and machine", example: "@usid 123" }
    ]
  },
  {
    id: "db-slow-now",
    title: "The whole database is slow right now",
    blurb: "Get the load picture first, then see which waits and SQL account for the active sessions.",
    steps: [
      { file: "aw.sql", why: "Key load metrics (V$SYSMETRIC) plus the last minute of ASH top events", example: "@aw 1=1",
        note: "The metrics part needs no pack; the ASH part queries GV$ACTIVE_SESSION_HISTORY (Diagnostics Pack license)." },
      { file: "vstat.sql", why: "Per-minute AAS, CPU, IOPS, latency trend from V$SYSMETRIC_HISTORY", example: "@vstat sysdate-1/24 sysdate",
        note: "In-memory history only covers about the last hour; use awr/dstat.sql for older data." },
      { file: "ash/ashtop.sql", why: "Top wait classes and events of foreground sessions, last 15 minutes", example: "@ash/ashtop wait_class,event2 session_type='FOREGROUND' sysdate-15/1440 sysdate",
        note: "Needs Diagnostics Pack license (queries GV$ACTIVE_SESSION_HISTORY)." },
      { file: "ash/ashtop.sql", why: "Top SQL_IDs and what they wait for, last 15 minutes", example: "@ash/ashtop sql_id,event2 1=1 sysdate-15/1440 sysdate",
        note: "Needs Diagnostics Pack license (queries GV$ACTIVE_SESSION_HISTORY)." },
      { file: "snapper.sql", why: "License-free alternative: sample all sessions for 5s x 3 (V$SESSION)", example: "@snapper ash=sql_id+event 5 3 all",
        note: "No Diagnostics Pack needed; samples V$SESSION directly. Run it when ashtop is not licensed or ASH is unavailable." }
    ]
  },
  {
    id: "slow-sql",
    title: "A specific SQL statement is slow",
    blurb: "Know the SQL_ID? See its cursors and plan, then where in the plan the time goes.",
    steps: [
      { file: "sqlid.sql", why: "SQL text, child cursors, executions and per-exec timings (V$SQL)", example: "@sqlid 7q729nhdgtsqq %",
        note: "Second argument is the child cursor number; % shows all children." },
      { file: "xi.sql", why: "Execution plan of a cached cursor with cost, rows and peeked binds", example: "@xi 7q729nhdgtsqq 0",
        note: "Actual rows and times (A-Rows, A-Time) appear only if the statement ran with the GATHER_PLAN_STATISTICS hint or statistics_level=ALL." },
      { file: "ash/asqlmon.sql", why: "SQL-monitor-style view: time per plan line, from ASH samples", example: "@ash/asqlmon 7q729nhdgtsqq % sysdate-1/24 sysdate",
        note: "Needs Diagnostics Pack license (queries GV$ACTIVE_SESSION_HISTORY). Second argument is the child number; % means all." },
      { file: "xpi.sql", why: "Real SQL Monitor text report for a SQL_ID (rows, time, waits per line)", example: "@xpi 7q729nhdgtsqq",
        note: "Needs Tuning Pack license (V$SQL_MONITOR, DBMS_SQLTUNE). Only works for statements Oracle monitored (long-running or parallel)." },
      { file: "sqlbinds.sql", why: "Captured bind values: is it slow only for certain inputs?", example: "@sqlbinds 7q729nhdgtsqq 0 %",
        note: "Args: sql_id, child number (% = all), bind name pattern." },
      { file: "nonshared.sql", why: "Why there are many child cursors (reasons from V$SQL_SHARED_CURSOR)", example: "@nonshared 7q729nhdgtsqq" }
    ]
  },
  {
    id: "locking-blocking",
    title: "Sessions are blocking or waiting on each other",
    blurb: "Find who waits for whom, what the root blocker is doing, and what it holds.",
    steps: [
      { file: "swc.sql", why: "Current wait chains from GV$SESSION: who waits for whom (no pack)", example: "@swc program2||event2 1=1",
        note: "License-free: reads GV$SESSION only. Shows idle blockers at the end of each chain." },
      { file: "lock.sql", why: "Held and requested locks; blockers have BLOCK > 0 (V$LOCK)", example: "@lock \"block > 0 OR request > 0\"" },
      { file: "s.sql", why: "What the root blocker is doing and waiting on right now", example: "@s 456",
        note: "Use the blocker SID found in the previous steps." },
      { file: "trans.sql", why: "Open transactions with start time and undo used (V$TRANSACTION)", example: "@trans",
        note: "An idle blocker is usually a session with an uncommitted transaction listed here." },
      { file: "ash/ash_wait_chains.sql", why: "Wait chains over the last hour, to catch blocking that already ended", example: "@ash/ash_wait_chains username||'-'||program2 \"wait_class='Application'\" sysdate-1/24 sysdate",
        note: "Needs Diagnostics Pack license (queries GV$ACTIVE_SESSION_HISTORY). Use ash/dash_wait_chains.sql for older (AWR) data." },
      { file: "kill.sql", why: "Generate ALTER SYSTEM KILL SESSION commands for chosen sessions", example: "@kill sid=456",
        note: "Only prints the commands; running them is destructive, so verify the SID and serial# first." }
    ]
  },
  {
    id: "history",
    title: "What happened earlier (yesterday, last week)?",
    blurb: "Use AWR and ASH history to find when load peaked and what ran then.",
    steps: [
      { file: "awr/dbload.sql", why: "Last 7 days of AAS, CPU, IO, redo, parse metrics per AWR snapshot", example: "@awr/dbload",
        note: "Needs Diagnostics Pack license (DBA_HIST_*). Takes no arguments." },
      { file: "ash/dashpeak.sql", why: "AAS per hour bucket from AWR ASH: when was the busiest period?", example: "@ash/dashpeak hh 1=1 sysdate-2 sysdate",
        note: "Needs Diagnostics Pack license (DBA_HIST_ACTIVE_SESS_HISTORY). Group by dd, hh or mi for day, hour or minute buckets." },
      { file: "ash/dashtop.sql", why: "Top SQL_IDs and events inside the problem window (AWR ASH)", example: "@ash/dashtop sql_id,event2 1=1 \"timestamp'2026-10-21 14:00:00'\" \"timestamp'2026-10-21 15:00:00'\"",
        note: "Needs Diagnostics Pack license. AWR keeps about 1 in 10 ASH samples, so counts are approximate." },
      { file: "ash/dasqlmon.sql", why: "Time per plan line for a SQL_ID in that window (AWR ASH)", example: "@ash/dasqlmon 7q729nhdgtsqq % \"timestamp'2026-10-21 14:00:00'\" \"timestamp'2026-10-21 15:00:00'\"",
        note: "Needs Diagnostics Pack license. Second argument is the plan hash value; % means all plans." },
      { file: "awr/awr_sqlstats_per_exec.sql", why: "Per-execution elapsed, CPU, IO and rows per snapshot and plan", example: "@awr/awr_sqlstats_per_exec 7q729nhdgtsqq % sysdate-7 sysdate",
        note: "Needs Diagnostics Pack license (DBA_HIST_SQLSTAT). Second argument is the plan hash value; % means all." },
      { file: "awr/gen_awr_report.sql", why: "Generate the standard AWR HTML report for two snapshots you choose", example: "@awr/gen_awr_report",
        note: "Needs Diagnostics Pack license. Prompts for begin and end snapshot ids and writes awr_local_inst_1.html in the current directory." }
    ]
  },
  {
    id: "latch-mutex-shared-pool",
    title: "Latch, mutex or shared pool contention",
    blurb: "Library cache, cursor and latch waits: find the holders, the hot objects and whether it is a parse storm.",
    steps: [
      { file: "ash/ashtop.sql", why: "Which latch, mutex and library cache waits dominate, and for which SQL", example: "@ash/ashtop event2,sql_id \"(event like 'latch%' or event like 'cursor:%' or event like 'library cache%')\" sysdate-1/24 sysdate",
        note: "Needs Diagnostics Pack license (queries GV$ACTIVE_SESSION_HISTORY). The snapper step below is the license-free alternative." },
      { file: "snapper.sql", why: "License-free: sample all sessions, grouped by SQL_ID and wait event", example: "@snapper ash=sql_id+event 5 3 all",
        note: "No Diagnostics Pack needed; samples V$SESSION directly." },
      { file: "latchprof.sql", why: "Sample V$LATCHHOLDER to see which sessions hold the shared pool latch", example: "@latchprof sid,name,sqlid % \"shared pool\" 10000",
        note: "High-frequency sampling of a fixed view; run as a privileged user, and try it on a quiet system first." },
      { file: "mutexprof.sql", why: "Top mutex sleeps by code location, from V$MUTEX_SLEEP_HISTORY", example: "@mutexprof loc 1=1",
        note: "Add id,req,blk to the first argument to see the object hash and requesting/blocking SIDs." },
      { file: "nonsharedsum.sql", why: "Cursors with 10+ children and the reasons they were not shared", example: "@nonsharedsum %",
        note: "High version counts are a classic cause of cursor: mutex and library cache waits." },
      { file: "topcur.sql", why: "Plans reused by 100+ different SQL_IDs: literals instead of binds", example: "@topcur 100",
        note: "The argument is the minimum number of distinct SQL_IDs per plan hash value." }
    ]
  },
  {
    id: "memory",
    title: "Memory: SGA and PGA usage",
    blurb: "See how the SGA is divided, who uses PGA and workarea memory, and whether resizing is churning.",
    steps: [
      { file: "sga.sql", why: "SGA components: current, min, max sizes and last resize op", example: "@sga" },
      { file: "sgastat.sql", why: "Breakdown of SGA pools (V$SGASTAT), e.g. shared pool free memory", example: "@sgastat \"free memory\"",
        note: "Argument matches component name or pool name, e.g. \"shared pool\" or \"large pool\"." },
      { file: "sgares.sql", why: "Recent automatic SGA resize operations: is memory being shuffled?", example: "@sgares" },
      { file: "pga.sql", why: "PGA target vs allocated, cache hit %, over-allocation (V$PGASTAT)", example: "@pga" },
      { file: "wrka.sql", why: "Active workareas per session: PGA and TEMP used by sorts and hashes", example: "@wrka 1=1",
        note: "Filter on any column, e.g. @wrka sid=123 or @wrka username='APPUSER'." },
      { file: "smem.sql", why: "One session's process memory by category (V$PROCESS_MEMORY)", example: "@smem 123" }
    ]
  },
  {
    id: "space",
    title: "Space: tablespaces, segments, TEMP and undo",
    blurb: "Find which tablespace is filling up, what fills it, and who is using TEMP or undo.",
    steps: [
      { file: "df.sql", why: "Tablespace usage in GB, df-style, including TEMP", example: "@df",
        note: "Percent used is based on current file sizes, not autoextend limits; check the next step for MAXSIZE." },
      { file: "ls.sql", why: "Datafiles of a tablespace with size, autoextend and max size", example: "@ls USERS" },
      { file: "topseg.sql", why: "Biggest segments in a tablespace, partitions rolled up to table or index", example: "@topseg USERS" },
      { file: "seg.sql", why: "Size, type, tablespace and header block of a segment (wildcards allowed)", example: "@seg soe.orders" },
      { file: "temp.sql", why: "Who uses TEMP right now: session, SQL_ID, MB (GV$TEMPSEG_USAGE)", example: "@temp" },
      { file: "uds.sql", why: "Undo usage per interval, longest query, ORA-1555 and no-space counts", example: "@uds" }
    ]
  },
  {
    id: "plan-regression",
    title: "A plan changed and got slower; pin or patch the plan",
    blurb: "Compare plans over time, then (optionally) lock in the good plan with a baseline or a SQL patch.",
    steps: [
      { file: "awr/awr_sqlstats_unstable.sql", why: "Find SQL_IDs whose time per execution varies between plans", example: "@awr/awr_sqlstats_unstable sql_id plan_hash_value sysdate-14 sysdate",
        note: "Needs Diagnostics Pack license (DBA_HIST_SQLSTAT). Skip this step if you already know the SQL_ID." },
      { file: "awr/awr_sqlstats_per_exec.sql", why: "Elapsed per execution by plan and snapshot: which plan was good?", example: "@awr/awr_sqlstats_per_exec 7q729nhdgtsqq % sysdate-14 sysdate",
        note: "Needs Diagnostics Pack license (DBA_HIST_SQLSTAT). Second argument is the plan hash value; % means all." },
      { file: "xawr.sql", why: "Display the old (good) plan from AWR by plan hash value", example: "@xawr 7q729nhdgtsqq 1541789278",
        note: "Needs Diagnostics Pack license (DBA_HIST_SQL_PLAN). Use % as plan hash value to list all plans." },
      { file: "xi.sql", why: "Display the current plan(s) from the cursor cache to compare", example: "@xi 7q729nhdgtsqq %" },
      { file: "create_sql_baseline.sql", why: "Load the good cached plan into a SQL plan baseline for the bad SQL", example: "@create_sql_baseline 7q729nhdgtsqq 1541789278 7q729nhdgtsqq",
        note: "CHANGES THE DATABASE (DBMS_SPM). Args: good sql_id, good plan hash value, bad sql_id. The good plan must still be in the cursor cache; otherwise use create_sql_baseline_awr.sql with the same arguments. Undo: @drop_sql_baseline <sql_handle>. Test outside production first." },
      { file: "create_sql_patch.sql", why: "Alternative: attach hints to a SQL_ID without changing the application", example: "@create_sql_patch 7q729nhdgtsqq \"FULL(@SEL$1 T@SEL$1)\"",
        note: "CHANGES THE DATABASE (DBMS_SQLDIAG). Creates SQL_PATCH_<sql_id>. Wrap hints containing spaces in double quotes. Prefer hints copied from the plan OUTLINE section (see otherxml.sql). Undo: @drop_sql_patch SQL_PATCH_7q729nhdgtsqq. Test outside production first." }
    ]
  },
  {
    id: "parallel-query",
    title: "Parallel query (PX) is slow or misbehaving",
    blurb: "Check requested vs granted DOP, what the slaves wait for, and where in the plan the time goes.",
    steps: [
      { file: "px.sql", why: "Running parallel queries cluster-wide: QC SID, requested vs actual DOP", example: "@px" },
      { file: "pxs.sql", why: "Slaves of one query coordinator: state, wait event and blocker per slave", example: "@pxs 123",
        note: "The argument is the query coordinator (QC) SID listed by px.sql." },
      { file: "ash/ashtop.sql", why: "Where do QC and slaves wait? Split by DOP, program and event", example: "@ash/ashtop dop,program2,event2 sql_id='7q729nhdgtsqq' sysdate-1/24 sysdate",
        note: "Needs Diagnostics Pack license (queries GV$ACTIVE_SESSION_HISTORY). Slaves show up as (Pnnn) in program2." },
      { file: "ash/asqlmon.sql", why: "Which plan lines the slaves spent their time on, from ASH", example: "@ash/asqlmon 7q729nhdgtsqq % sysdate-1/24 sysdate",
        note: "Needs Diagnostics Pack license (queries GV$ACTIVE_SESSION_HISTORY)." },
      { file: "xpi.sql", why: "SQL Monitor text report: per-line rows and time, incl. PX details", example: "@xpi 7q729nhdgtsqq",
        note: "Needs Tuning Pack license (V$SQL_MONITOR, DBMS_SQLTUNE). Parallel statements are monitored automatically." },
      { file: "ash/rowsource_events.sql", why: "Last hour of ASH: are parallel slaves doing buffered full table scans?", example: "@ash/rowsource_events \"TABLE ACCESS\" FULL",
        note: "Needs Diagnostics Pack license. Args are LIKE patterns for plan operation and options; looks at the last hour only." }
    ]
  }
];
