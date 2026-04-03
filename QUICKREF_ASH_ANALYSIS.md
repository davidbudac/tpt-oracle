# ASH Analysis - Quick Reference

**Active Session History troubleshooting at your fingertips**

---

## What is ASH?

ASH (Active Session History) samples V$SESSION every second showing what sessions are doing. TPT's ASH scripts provide Diagnostics Pack-like functionality **WITHOUT requiring expensive licenses** (they query V$ACTIVE_SESSION_HISTORY which is always available, not the AWR repository).

---

## Essential ASH Scripts

| Script | Purpose | When to Use |
|--------|---------|-------------|
| **ash/ashtop.sql** | Top activity by any dimension | Finding what's consuming resources |
| **ash/ashtop10.sql** | Top 10 activity (limited output) | Quick overview with less detail |
| **ash/ashtopsum.sql** | Activity summary with aggregated stats | Getting summary statistics |
| **ash/ash_wait_chains.sql** | Blocking session chains | Lock/blocking investigations |
| **ash/asqlmon.sql** | SQL execution breakdown by plan step | Slow SQL analysis (11g) |
| **ash/asqlmon12.sql** | SQL Monitor for 12c+ with enhanced metrics | Slow SQL analysis (12c+) |
| **ash/asqlmonx.sql** | Extended SQL Monitor with additional columns | Deep SQL execution analysis |
| **ash/dashtop.sql** | Top activity from AWR ASH (historical) | Historical analysis (requires Diag Pack) |
| **ash/dasqlmon.sql** | SQL Monitor from AWR ASH (historical) | Historical SQL analysis (requires Diag Pack) |
| **ash/ashpeak.sql** | Find peak activity times | Identifying performance spikes |
| **ash/ashpeaktop.sql** | Top activity during peak periods | Analyzing spike causes |
| **ash/ash_index_helper.sql** | Suggest missing indexes | SQL tuning |
| **ash/event_hist.sql** | Wait event time distribution | Latency analysis |
| **ash/event_hist_micro.sql** | Event histogram with microsecond precision | Precise latency analysis |
| **ash/time_model.sql** | Time model breakdown from ASH | Understanding time distribution |
| **ash/sqlid_activity.sql** | Activity for specific SQL_ID over time | Tracking SQL performance |
| **ash/w.sql** | What's happening? Last minute activity | Quick current status check |

---

## Quick Start Examples

### 1. What's Consuming Resources? (ash/ashtop.sql)

```sql
-- Top activity by SQL_ID and event
@ash/ashtop sql_id,event2 1=1 sysdate-1/24 sysdate

-- Top activity by username and program
@ash/ashtop username,program2 1=1 sysdate-1/24 sysdate

-- Top activity by wait class
@ash/ashtop wait_class,event2 1=1 &hour

-- Top activity with SQL operations
@ash/ashtop sql_opname,event2,sql_plan_operation||' '||sql_plan_options 1=1 sysdate-1/24 sysdate
```

**Grouping column examples:**
- `sql_id` - By SQL statement
- `username` - By database user
- `event2` - By wait event
- `wait_class` - By wait class
- `program2` - By client program
- `machine` - By client machine
- `sql_opname` - By SQL operation (SELECT, INSERT, etc.)
- `session_state` - ON CPU vs WAITING
- `blocking_session` - Who is blocking

### 2. Finding Blocking Sessions (ash/ash_wait_chains.sql)

```sql
-- Show blocking chains
@ash/ash_wait_chains username||'-'||program2 1=1 sysdate-1/24 sysdate

-- Focus on application waits only
@ash/ash_wait_chains username "wait_class='Application'" sysdate-1/24 sysdate

-- See who's blocking whom
@ash/ash_wait_chains blocking_session,event2 1=1 &hour
```

### 3. Slow SQL Deep Dive (ash/asqlmon.sql)

```sql
-- Where is SQL spending time in execution plan?
@ash/asqlmon <sql_id> 0 sysdate-1/24 sysdate

-- Example:
@ash/asqlmon 7q729nhdgtsqq 0 sysdate-1/24 sysdate

-- All children of SQL
@ash/asqlmon 7q729nhdgtsqq % sysdate-1 sysdate
```

**Shows:** Which plan steps consume the most time!

### 4. Find Peak Activity (ash/ashpeak.sql)

```sql
-- When was database busiest today?
@ash/ashpeak &today

-- Peak activity last 7 days
@ash/ashpeak sysdate-7 sysdate

-- Peak activity specific timeframe
@ash/ashpeak "timestamp'2026-01-08 00:00:00'" "timestamp'2026-01-08 23:59:59'"
```

### 5. Index Recommendations (ash/ash_index_helper.sql)

```sql
-- Suggest indexes for slow SQL
@ash/ash_index_helper 8zz6y2yzdqjp0 %.% sysdate-1/24 sysdate

-- Suggest indexes for specific schema
@ash/ash_index_helper % SOE.% sysdate-1/24 sysdate

-- Analyze all recent SQL for index opportunities
@ash/ash_index_helper % %.% &hour
```

### 6. Wait Event Latency Distribution (ash/event_hist.sql)

```sql
-- How long do log file syncs take?
@ash/event_hist log.file 1=1 sysdate-1/24 sysdate

-- I/O wait times for user sessions
@ash/event_hist "log.file|db.file" "wait_class='User I/O' AND session_type='FOREGROUND'" sysdate-1/24 sysdate

-- All wait event distribution
@ash/event_hist % 1=1 &hour

-- Microsecond precision histogram
@ash/event_hist_micro log.file.sync 1=1 &hour
```

### 7. Quick Activity Check (ash/w.sql)

```sql
-- What's happening RIGHT NOW? (last minute)
@ash/w

-- Quick status check without parameters
@ash/w
```

### 8. Activity Summary (ash/ashtopsum.sql)

```sql
-- Get aggregated summary instead of detailed rows
@ash/ashtopsum sql_id,event2 1=1 &hour

-- Summary by user and wait class
@ash/ashtopsum username,wait_class 1=1 sysdate-1/24 sysdate
```

### 9. Top 10 Quick View (ash/ashtop10.sql)

```sql
-- Quick top 10 view (faster than full ashtop)
@ash/ashtop10 sql_id,event2 1=1 &5min

-- Top 10 by username
@ash/ashtop10 username,program2 1=1 &hour
```

### 10. Historical ASH Analysis (ash/dashtop.sql & ash/dasqlmon.sql)

**Note: Requires Diagnostics Pack license**

```sql
-- Historical top activity from AWR
@ash/dashtop sql_id,event2 1=1 sysdate-7 sysdate

-- Historical SQL Monitor from AWR
@ash/dasqlmon 7q729nhdgtsqq 0 sysdate-7 sysdate
```

### 11. Time Model Analysis (ash/time_model.sql)

```sql
-- See time model breakdown from ASH
@ash/time_model 1=1 sysdate-1/24 sysdate

-- Time model for specific SQL
@ash/time_model "sql_id='7q729nhdgtsqq'" &hour
```

### 12. SQL Activity Tracking (ash/sqlid_activity.sql)

```sql
-- Track specific SQL_ID activity over time
@ash/sqlid_activity 7q729nhdgtsqq sysdate-1/24 sysdate

-- See when SQL was active
@ash/sqlid_activity abc123def456 &day
```

---

## Time Range Shortcuts

Instead of typing dates, use these shortcuts:

| Shortcut | Expands to |
|----------|------------|
| `&min` or `&1min` | sysdate-1/1440 sysdate |
| `&5min` | sysdate-5/1440 sysdate |
| `&hour` | sysdate-1/24 sysdate |
| `&day` | sysdate-1 sysdate |
| `&today` | trunc(sysdate) sysdate |

**Usage:**
```sql
@ash/ashtop sql_id,event2 1=1 &hour
@ash/ashpeak &today
@ash/event_hist log.file 1=1 &5min
```

---

## Common Filters

### Filter by User
```sql
@ash/ashtop sql_id 1=1 "username='SOE'" sysdate-1/24 sysdate
```

### Filter by Wait Class
```sql
@ash/ashtop sql_id "wait_class='User I/O'" sysdate-1/24 sysdate
```

### Filter by Session Type
```sql
@ash/ashtop sql_id "session_type='FOREGROUND'" sysdate-1/24 sysdate
```

### Filter by Program
```sql
@ash/ashtop sql_id "program like 'sqlplus%'" sysdate-1/24 sysdate
```

### Multiple Conditions
```sql
@ash/ashtop sql_id "username='APP' AND wait_class='Application'" sysdate-1/24 sysdate
```

---

## Common Troubleshooting Workflows

### Workflow 1: General Performance Issue

```sql
-- 1. What's consuming resources?
@ash/ashtop sql_id,event2 1=1 sysdate-1/24 sysdate

-- 2. Deep dive into top SQL
@ash/asqlmon <sql_id_from_step1> 0 sysdate-1/24 sysdate

-- 3. Check for blocking
@ash/ash_wait_chains username 1=1 sysdate-1/24 sysdate
```

### Workflow 2: Lock/Blocking Investigation

```sql
-- 1. Find blocking chains
@ash/ash_wait_chains blocking_session,event2 1=1 sysdate-1/24 sysdate

-- 2. Top application waits
@ash/ashtop sql_id,event2 "wait_class='Application'" sysdate-1/24 sysdate

-- 3. See current locks
@lock 1=1
```

### Workflow 3: Slow SQL Investigation

```sql
-- 1. Identify slow SQL
@ash/ashtop sql_id,event2 1=1 sysdate-1/24 sysdate

-- 2. Execution plan analysis
@ash/asqlmon <sql_id> 0 sysdate-1/24 sysdate

-- 3. Check for missing indexes
@ash/ash_index_helper <sql_id> %.% sysdate-1/24 sysdate

-- 4. Get SQL details
@sqlid <sql_id> 0
```

### Workflow 4: I/O Performance Issue

```sql
-- 1. Top I/O events
@ash/ashtop event2,sql_id "wait_class='User I/O'" sysdate-1/24 sysdate

-- 2. I/O wait time distribution
@ash/event_hist "db.file" 1=1 sysdate-1/24 sysdate

-- 3. Top segments by I/O
@topsegstat reads
```

### Workflow 5: Finding Performance Spikes

```sql
-- 1. When did spikes occur?
@ash/ashpeak sysdate-1 sysdate

-- 2. What was active during spike?
@ash/ashtop sql_id,event2 1=1 <spike_start> <spike_end>

-- 3. Deep dive into top SQL from spike
@ash/asqlmon <sql_id> 0 <spike_start> <spike_end>
```

---

## Pro Tips

1. **Start Broad, Then Narrow**
   ```sql
   -- Start: What's happening?
   @ash/ashtop event2 1=1 sysdate-1/24 sysdate

   -- Narrow: Focus on top event
   @ash/ashtop sql_id,event2 "event like 'enq: TX%'" sysdate-1/24 sysdate
   ```

2. **Combine Multiple Dimensions**
   ```sql
   -- See SQL, event, and plan operation together
   @ash/ashtop sql_id,event2,sql_plan_operation 1=1 &hour
   ```

3. **Use Meaningful Time Windows**
   ```sql
   -- Match your monitoring/alerting timeframe
   @ash/ashtop sql_id 1=1 sysdate-15/1440 sysdate  -- Last 15 minutes
   ```

4. **Filter Out Noise**
   ```sql
   -- Exclude background processes
   @ash/ashtop sql_id "session_type='FOREGROUND'" &hour

   -- Exclude specific users
   @ash/ashtop sql_id "username not in ('SYS','SYSTEM')" &hour
   ```

5. **Save Output for Analysis**
   ```sql
   SQL> spool ash_analysis.txt
   SQL> @ash/ashtop sql_id,event2 1=1 &hour
   SQL> spool off
   ```

---

## ASH vs AWR vs Snapper

| Tool | Data Source | License | Retention | Best For |
|------|-------------|---------|-----------|----------|
| **ASH Scripts** | V$ACTIVE_SESSION_HISTORY | Free | ~1 hour | Real-time, recent issues |
| **AWR Scripts** | DBA_HIST_* tables | Diagnostics Pack | Days/Weeks | Historical analysis |
| **Snapper** | Direct V$ sampling | Free | Session duration | Live profiling |

**Rule of Thumb:**
- **Last hour:** Use ASH scripts
- **Historical (days/weeks):** Use AWR scripts (if licensed)
- **Right now (live):** Use Snapper

---

## Quick Diagnostics

```sql
-- Database slow RIGHT NOW?
@ash/ashtop sql_id,event2 1=1 &5min

-- Was database slow earlier today?
@ash/ashpeak &today

-- Blocking issues?
@ash/ash_wait_chains username 1=1 &hour

-- Which SQL is slow?
@ash/ashtop sql_id,event2 1=1 &hour

-- Where in execution plan is time spent?
@ash/asqlmon <sql_id> 0 &hour
```

---

## Search for ASH Scripts

```bash
# Find all ASH scripts
tpt -c "ASH Analysis"

# Find specific ASH functionality
tpt -k "ash wait"
tpt -k "ash index"
tpt -k "ash peak"
```

---

**Remember:** ASH data is typically retained for ~1 hour in memory. For older data, use AWR scripts (requires Diagnostics Pack license).

---

*ASH Analysis Quick Reference - TPT Scripts - v1.0*
