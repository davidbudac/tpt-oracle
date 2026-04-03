# Performance Monitoring - Quick Reference

**Real-time performance analysis and profiling**

---

## The Big Three Monitoring Tools

| Tool | Data Source | Best For | License Required |
|------|-------------|---------|------------------|
| **Snapper** | Direct V$ sampling | Live session profiling | NO - Free |
| **ASH** | V$ACTIVE_SESSION_HISTORY | Recent activity (last hour) | NO - Free |
| **AWR** | DBA_HIST_* tables | Historical (days/weeks) | YES - Diagnostics Pack |

---

## 1. Snapper - The Swiss Army Knife

### Basic Usage

```sql
-- Profile all sessions for 60 seconds (12 x 5-second snapshots)
@snapper ash 5 12 all

-- Profile specific session
@snapper ash 5 12 123

-- Profile multiple sessions
@snapper ash 5 12 123,456,789

-- Profile with statistics (not just ASH)
@snapper stats 5 12 all

-- Both ASH and stats
@snapper ash,stats 5 12 all
```

### Snapper Syntax

```
@snapper [options] <seconds> <snapshots> <sid>
```

**Options:**
- `ash` - Sample session activity (default)
- `stats` - Capture session statistics
- `all` - Both ASH and stats
- `gather=[s][t][w][l][e]` - What to gather
  - `s` = sessions
  - `t` = time model
  - `w` = waits
  - `l` = latches
  - `e` = enqueues

### Common Snapper Patterns

```sql
-- Quick 30-second sample of all activity
@snapper ash 5 6 all

-- Detailed 2-minute profile with stats
@snapper ash,stats 10 12 all

-- Focus on specific SQL execution
@snapper ash=sql_id+event 5 12 123

-- Profile just time and waits
@snapper ash,stats,gather=stw 5 12 all

-- Long-term monitoring (5 minutes)
@snapper ash 10 30 all
```

### Snapper Output Interpretation

**Look for:**
1. **Top Wait Events** - What's the session waiting on?
2. **SQL_ID** - Which SQL statements are active?
3. **% Activity** - How much time in each state?
4. **ON CPU vs WAITING** - CPU-bound or I/O-bound?

---

## 2. Current Activity - What's Happening Now?

### Quick Status Check

```sql
-- What's the database doing RIGHT NOW?
@aw 1=1

-- Current session activity
@s <sid>

-- All user sessions
@uu %

-- Active sessions with SQL
@ash/ashtop sql_id,event2 1=1 &5min
```

### Session Monitoring

```sql
-- Detailed session info
@s 123

-- Active sessions count
@a

-- Active sessions grouped by column
@as <column>

-- Active sessions with SQL_IDs
@asql

-- Session statistics
@ses 123 %
@ses 123 parse
@ses 123 redo

-- Only non-zero stats
@ses2 123 %

-- Session memory usage
@smem 123

-- Process memory detail
@pmem <spid>

-- Session+process info
@usid 123
```

### System-Wide Monitoring

```sql
-- System statistics
@sys redo
@sys parse
@sys %commit%

-- System metrics
@aw 1=1

-- Background processes
@bg %
@bg dbw
```

---

## 3. Memory Monitoring

### SGA Monitoring

```sql
-- SGA overview
@sga

-- SGA detailed
@sgastat %
@sgastat "free memory"

-- Shared pool by subpool
@sgastatx "free memory"

-- SGA resize history
@sgares
@memres
```

### PGA Monitoring

```sql
-- PGA overview
@pga

-- Session PGA usage
@smem <sid>

-- Process PGA detail
@pmem <spid>

-- PGA+TEMP by session
@wrka 1=1
@wrka sid=123

-- Workarea summary
@wrkasum 1=1
@wrkasum sql_id='7q729nhdgtsqq'
```

### SQL Memory Usage

```sql
-- Top cursors by memory
@topcur
@topcurmem

-- Memory for specific SQL
@sqlmem <sql_id>
```

### Dictionary Cache

```sql
-- Row cache statistics
@rowcache %
@rowcache dc_users
```

---

## 4. Advanced Profiling

### Latch Profiling

```sql
-- Profile latch holders (100k samples)
@latchprof name,sqlid 123 % 100000

-- Which SIDs hold shared pool latches?
@latchprof sid,name % "shared pool" 100000

-- Drill down to latch address
@latchprof sid,name,laddr % % 100000

-- Extended latch profiling
@latchprofx name,sqlid 123 % 100000
```

### Mutex Profiling

```sql
-- Profile cursor pin mutex (10k samples)
@mutexprof sid,sql_id 1=1 10000
```

### Wait Event Profiling

```sql
-- High-frequency wait sampling (10k samples)
@waitprof 10000
```

### Buffer Cache Profiling

```sql
-- Profile buffer cache activity
@bufprof

-- Buffer headers by latch address
@bhla

-- Buffer cache by tablespace
@bh_by_ts
```

### OS Stack Profiling

```sql
-- Unix/Linux stack profiling
@ostackprofu <spid> <samples>

-- Windows stack profiling
@ostackprofw <spid> <samples>

-- General stack profiling
@ostackprof <spid> <samples>
```

### Tracing & Diagnostics

```sql
-- Enable 10046 SQL trace
@46on <sid>

-- Disable 10046 trace
@46off <sid>

-- Enable 10053 CBO trace
@53on <sid>

-- Disable 10053 trace
@53off <sid>

-- Display diagnostic information
@diag
```

---

## 5. Monitoring Workflows

### Workflow 1: General Performance Check

```sql
-- 1. What's active right now?
@aw 1=1

-- 2. Top sessions
@uu %

-- 3. Recent activity
@ash/ashtop sql_id,event2 1=1 &5min

-- 4. Profile active sessions
@snapper ash 5 12 all
```

### Workflow 2: Slow Session Investigation

```sql
-- 1. Session details
@s 123

-- 2. Session statistics
@ses 123 %

-- 3. What SQL is running?
@usid 123

-- 4. Profile the session
@snapper ash,stats 10 12 123

-- 5. Memory usage
@smem 123
```

### Workflow 3: System Performance Issue

```sql
-- 1. System overview
@aw 1=1

-- 2. Top activity (last 5 min)
@ash/ashtop sql_id,event2 1=1 &5min

-- 3. System statistics
@sys %

-- 4. Memory status
@sga
@pga

-- 5. Profile all sessions
@snapper ash 5 12 all
```

### Workflow 4: CPU Saturation

```sql
-- 1. Find CPU-consuming sessions
@ash/ashtop sql_id "session_state='ON CPU'" &5min

-- 2. Top SQL by activity
@snapper ash=sql_id 5 12 all

-- 3. Profile specific session
@snapper ash,stats 10 12 <sid_from_step1>

-- 4. Check system stats
@sys "CPU used"
```

### Workflow 5: I/O Performance Issue

```sql
-- 1. Top I/O waits
@ash/ashtop event2,sql_id "wait_class='User I/O'" &5min

-- 2. Wait event distribution
@ash/event_hist "db.file|direct" 1=1 &hour

-- 3. Top segments by I/O
@topsegstat reads

-- 4. Profile sessions doing I/O
@snapper ash 5 12 all
```

---

## 6. Monitoring Cheat Sheet

### CPU Issues

```sql
@ash/ashtop sql_id "session_state='ON CPU'" &5min
@sys "CPU used"
@snapper ash 5 12 all
```

### Memory Issues

```sql
@sga
@pga
@wrka 1=1
@topcur
@sgastat %
```

### I/O Issues

```sql
@ash/ashtop event2 "wait_class='User I/O'" &5min
@ash/event_hist "db.file" 1=1 &hour
@topsegstat reads
```

### Lock/Blocking Issues

```sql
@ash/ash_wait_chains username 1=1 &hour
@lock 1=1
@trans 1=1
```

### Parse Issues

```sql
@sys parse
@ses <sid> parse
@ash/ashtop event2 "event like 'latch%'" &5min
@latchprof name,sqlid % "shared pool" 100000
```

---

## 7. Key Metrics to Monitor

### Session-Level

| Metric | Script | Interpretation |
|--------|--------|----------------|
| Wait events | `@s <sid>` | What's blocking the session? |
| CPU time | `@ses <sid> "CPU used"` | CPU consumption |
| Parse count | `@ses <sid> parse` | Parse activity |
| PGA memory | `@smem <sid>` | Memory usage |
| SQL_ID | `@s <sid>` | Which SQL is running |

### System-Level

| Metric | Script | Interpretation |
|--------|--------|----------------|
| Database activity | `@aw 1=1` | Overall load |
| Redo generation | `@sys redo` | Write activity |
| Parse count | `@sys parse` | Hard vs soft parses |
| SGA free memory | `@sgastat "free"` | Memory pressure? |
| Active sessions | `@ash/ashtop` | Who's consuming resources |

---

## 8. Profiling Best Practices

### 1. Choose Right Tool

- **Snapper** → Live profiling, specific sessions
- **ASH** → Recent activity, multiple sessions
- **AWR** → Historical analysis, trends

### 2. Sample Duration

```sql
-- Quick check (30 seconds)
@snapper ash 5 6 all

-- Normal analysis (1-2 minutes)
@snapper ash 10 12 all

-- Deep analysis (5 minutes)
@snapper ash 10 30 all
```

### 3. Save Output

```sql
SQL> spool snapshot_2026-01-08.txt
SQL> @snapper ash,stats 10 12 all
SQL> spool off
```

### 4. Compare Before/After

```sql
-- Before change
@snapper ash,stats 10 12 all > before.txt

-- Make change...

-- After change
@snapper ash,stats 10 12 all > after.txt

-- Compare files
```

---

## 9. Real-Time Monitoring Commands

### Every DBA Should Know

```sql
-- What's happening now?
@aw 1=1

-- Who's connected?
@uu %

-- What are they doing?
@ash/ashtop sql_id,event2 1=1 &5min

-- Profile everything
@snapper ash 5 12 all

-- Top SQL
@ash/ashtop sql_id 1=1 &hour

-- Memory status
@sga
@pga

-- Space status
@df

-- Current locks
@lock 1=1
```

---

## 10. Emergency Quick Diagnostics

```sql
-- DATABASE SLOW? Run these in order:

-- 1. What's active?
@aw 1=1

-- 2. Top wait events?
@ash/ashtop event2 1=1 &5min

-- 3. Top SQL?
@ash/ashtop sql_id 1=1 &5min

-- 4. Blocking?
@ash/ash_wait_chains username 1=1 &5min

-- 5. Profile 1 minute
@snapper ash 5 12 all

-- 6. Check resources
@sga
@pga
@df
```

---

## Search for Monitoring Scripts

```bash
# Find performance monitoring scripts
tpt -c "Performance Monitoring"

# Find profiling tools
tpt -k profiling

# Find memory scripts
tpt -c "Memory Management"

# Find specific monitoring tool
tpt snapper.sql
tpt waitprof.sql
```

---

## Pro Tips

1. **Always capture baseline** before tuning
   ```sql
   @snapper ash,stats 10 12 all > baseline.txt
   ```

2. **Use appropriate sample duration**
   - Quick issue: 30-60 seconds
   - Intermittent: 2-5 minutes
   - Long-running: Multiple snapshots

3. **Focus on top consumers**
   - Snapper shows top events/SQL
   - Start with #1, not #10

4. **Combine tools**
   ```sql
   @snapper ash 5 12 all          -- What's active
   @ash/ashtop sql_id 1=1 &hour  -- Recent history
   ```

5. **Save everything**
   - Spool to files
   - Compare over time
   - Share with others

---

*Performance Monitoring Quick Reference - TPT Scripts - v1.0*
