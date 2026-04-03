# SQL Tuning - Quick Reference

**Oracle SQL tuning and plan management scripts reference**

---

## SQL Tuning Workflow

```
1. IDENTIFY → 2. ANALYZE → 3. FIX → 4. VERIFY
```

---

## 1. IDENTIFY Problem SQL

### Find Slow/Resource-Intensive SQL

| Method | Script | Usage |
|--------|--------|-------|
| **Current activity** | ash/ashtop.sql | `@ash/ashtop sql_id,event2 1=1 &hour` |
| **Top SQL by CPU** | (snapper or AWR) | `@snapper ash 5 12 all` |
| **Long-running ops** | long.sql | `@long 1=1` |
| **Top cursors by memory** | topcur.sql | `@topcur` |

```sql
-- Most active SQL right now
@ash/ashtop sql_id,event2 1=1 &hour

-- SQL with high parse counts
@ses <sid> parse
```

---

## 2. ANALYZE SQL Performance

### Get SQL Details

```sql
-- Full SQL text
@sqlf <sql_id>

-- SQL with execution statistics
@sqlid <sql_id> 0

-- SQL by hash value
@sql <hash_value>

-- All child cursors
@sqlid <sql_id> %

-- Bind variable values
@sqlbinds <sql_id> 0 %

-- Why child cursors not shared
@nonshared <sql_id>

-- Cursor compilation environment
@sqlopt <sql_id>

-- Cursor heap sizes
@curheaps <sql_id>

-- Shared pool memory by hash value
@sqlmemh <hash_value>

-- Shared pool memory by SQL_ID
@sqlmemx <sql_id>

-- SQL flame chart/profile
@sqlflame <sql_id>

-- SQL feature hierarchy
@sqlfh <sql_id>

-- Find SQLs with restart issues
@sqlmon_restarts
```

### View Execution Plans

```sql
-- Plan from library cache
@xi <sql_id> 0

-- Plan with runtime statistics (if available)
@xbi <sql_id> 0

-- Plan from memory (alternative to xi)
@xm <sql_id> 0

-- Better plan display (enhanced format)
@xb <sql_id> 0

-- Plan with statistics from memory
@xms <sql_id> 0

-- Plan with aliases from memory
@xmai <sql_id>

-- Advanced plan with outline hints
@xia <sql_id>

-- Plan from AWR (historical)
@xawr <sql_id> <plan_hash_value>

-- ALL plans for SQL from AWR
@xawr <sql_id> %

-- SQL Monitor report for session
@xp <sid>

-- SQL Monitor by SQL_ID
@xpi <sql_id>

-- SQL Monitor with HTML output
@xph <sid>

-- SQL Monitor by SQL_ID (11.2+)
@xpia <sql_id>

-- Show plan operations only
@xplto <sql_id>

-- Last statement from library cache
@xx
```

### Analyze Execution

```sql
-- Where is time spent in execution plan? (ASH-based)
@ash/asqlmon <sql_id> 0 sysdate-1/24 sysdate

-- SQL Monitor report (if monitoring enabled)
@sqlmon <sid>

-- Execution statistics from AWR
@awr/awr_sqlstats <sql_id> % sysdate-7 sysdate

-- Per-execution stats from AWR
@awr/awr_sqlstats_per_exec <sql_id> % sysdate-7 sysdate

-- SQL analysis from AWR by SQL_ID
@awr/awr_sqlid <sql_id> sysdate-7 sysdate

-- Bind values from AWR
@awr/awr_sqlid_binds <sql_id> sysdate-7 sysdate

-- Event histogram from AWR
@awr/awr_evh <event_name> sysdate-7 sysdate

-- System metrics from AWR
@awr/dstat sysdate-1 sysdate

-- System statistics from AWR
@awr/awr_sysstat sysdate-7 sysdate

-- Generate AWR report
@awr/gen_awr_report
```

### Find Missing Indexes

```sql
-- ASH-based index recommendations
@ash/ash_index_helper <sql_id> %.% sysdate-1/24 sysdate

-- For specific schema
@ash/ash_index_helper <sql_id> SOE.% sysdate-1/24 sysdate
```

---

## 3. FIX the Problem

### Option A: Create SQL Patch (Inject Hints)

**When:** You want to add hints without changing application code

```sql
-- Add single hint
@create_sql_patch g4pkmrqrgxg3b GATHER_PLAN_STATISTICS

-- Add multiple hints (use quotes)
@create_sql_patch b9dmj0ahu6xgc 'NO_INDEX_SS(@"SEL$1" "T1") FULL(@"SEL$1" "T2")'

-- Common hints to inject:
-- GATHER_PLAN_STATISTICS - Enable SQL monitoring
-- FULL(table_alias) - Force full table scan
-- INDEX(table_alias index_name) - Force index usage
-- NO_INDEX(table_alias index_name) - Prevent index usage
-- PARALLEL(table_alias 4) - Force parallel execution
-- NO_PARALLEL(table_alias) - Disable parallel
```

**Drop SQL patch:**
```sql
@drop_sql_patch SQL_PATCH_<sql_id>
```

### Option B: Create SQL Profile (From Good Plan)

**When:** You have a good plan and want optimizer to use it

```sql
-- Create profile with hints
@create_sql_profile <sql_id> 'hint1 hint2 hint3'

-- Example
@create_sql_profile 7q729nhdgtsqq 'FULL(@SEL$1 T1) USE_HASH(@SEL$1 T2)'
```

**Extract existing profile hints:**
```sql
@sql_profile_hints <sql_id>
```

**Drop SQL profile:**
```sql
@drop_sql_profile <profile_name>
```

### Option C: Create SQL Plan Baseline (Fix the Plan)

**When:** You want to lock in a specific good execution plan

```sql
-- Copy good plan from one SQL to another
@create_sql_baseline <good_sql_id> <good_plan_hash_value> <bad_sql_id>

-- Example: SQL abc123 has plan 12345 (good), apply to xyz789 (bad)
@create_sql_baseline abc123 12345 xyz789
```

**Drop SQL baseline:**
```sql
-- Get sql_handle from DBA_SQL_PLAN_BASELINES
@drop_sql_baseline SQL_52cb74b7097edbbd
```

### Option D: Gather Statistics

```sql
-- Table statistics
EXEC DBMS_STATS.GATHER_TABLE_STATS('owner','table_name');

-- Schema statistics
EXEC DBMS_STATS.GATHER_SCHEMA_STATS('schema_name');

-- System statistics
EXEC DBMS_STATS.GATHER_SYSTEM_STATS('START');
-- (wait for representative workload)
EXEC DBMS_STATS.GATHER_SYSTEM_STATS('STOP');
```

### Option E: Create Index

```sql
-- Get index recommendations
@ash/ash_index_helper <sql_id> <schema>.% sysdate-1/24 sysdate

-- Create index based on recommendations
CREATE INDEX idx_name ON table_name(column1, column2);

-- Verify index is used
@xi <sql_id> 0
```

---

## 4. VERIFY the Fix

### Compare Before/After

```sql
-- Check new plan
@xi <sql_id> 0

-- Check execution stats
@sqlid <sql_id> 0

-- Verify with ASH
@ash/ashtop sql_id,event2 "sql_id='<sql_id>'" &hour

-- Monitor execution
@sqlmon <sid>
```

### Verify Plan Stability

```sql
-- Check for plan changes over time (AWR)
@awr/awr_sqlstats_unstable force_matching_signature plan_hash_value sysdate-7 sysdate

-- Look for specific SQL
@awr/awr_sqlstats <sql_id> % sysdate-7 sysdate
```

---

## Common SQL Tuning Scenarios

### Scenario 1: SQL Doing Full Table Scan (Need Index)

```sql
# 1. Identify the issue
@xi <sql_id> 0
# Look for: TABLE ACCESS FULL

# 2. Get index recommendations
@ash/ash_index_helper <sql_id> %.% &hour

# 3. Check existing indexes
@ind <table_name>

# 4. Create index if missing
CREATE INDEX idx_name ON table(col1, col2);

# 5. Verify new plan
@xi <sql_id> 0
```

### Scenario 2: Wrong Index Being Used

```sql
# 1. See current plan
@xi <sql_id> 0

# 2. Force different index
@create_sql_patch <sql_id> 'INDEX(@SEL$1 TABLE_NAME INDEX_NAME)'

# 3. Verify
@xi <sql_id> 0
```

### Scenario 3: SQL Needs Parallel Execution

```sql
# 1. Check current plan (no parallel?)
@xi <sql_id> 0

# 2. Force parallel
@create_sql_patch <sql_id> 'PARALLEL(TABLE_ALIAS 4)'

# 3. Monitor parallel execution
@px 1=1
@pxs
```

### Scenario 4: Plan Changed and Now Slow

```sql
# 1. Find old good plan hash value
@awr/awr_sqlstats <sql_id> % sysdate-7 sysdate

# 2. See old plan
@xawr <sql_id> <old_good_plan_hash>

# 3. Create baseline to lock good plan
@create_sql_baseline <sql_id> <good_plan_hash> <sql_id>

# 4. Verify baseline is used
@xi <sql_id> 0
# Look for "SQL plan baseline" in notes
```

### Scenario 5: Join Order is Wrong

```sql
# 1. View current plan
@xi <sql_id> 0

# 2. See join order in OTHER_XML
@otherxml <sql_id> 0

# 3. Force different join order/method
@create_sql_patch <sql_id> 'LEADING(T1 T2 T3) USE_HASH(T2) USE_NL(T3)'

# 4. Verify
@xi <sql_id> 0
```

### Scenario 6: Cursor Sharing Issues

```sql
# 1. Too many child cursors?
@sqlid <sql_id> %

# 2. Why not sharing?
@nonshared <sql_id>

# 3. Check bind peeking
@sqlbinds <sql_id> % %

# 4. Possible fixes:
# - CURSOR_SHARING=FORCE (session level)
# - Create SQL profile
# - Fix application to use proper binds
```

---

## Hint Reference

### Common Optimizer Hints

```sql
-- Access Path Hints
FULL(table_alias)              -- Full table scan
INDEX(table_alias index_name)  -- Use specific index
NO_INDEX(table_alias)          -- Don't use indexes

-- Join Hints
USE_NL(table_alias)           -- Nested loops join
USE_HASH(table_alias)         -- Hash join
USE_MERGE(table_alias)        -- Sort-merge join
LEADING(t1 t2 t3)            -- Join order

-- Parallel Hints
PARALLEL(table_alias degree)  -- Parallel execution
NO_PARALLEL(table_alias)      -- No parallel

-- Other Common Hints
GATHER_PLAN_STATISTICS        -- Enable SQL monitoring
FIRST_ROWS(n)                 -- Optimize for first N rows
ALL_ROWS                      -- Optimize for throughput
NO_QUERY_TRANSFORMATION       -- Disable transformations
```

### View All Available Hints

```sql
@hint %                       -- List all hints
@hint full                    -- Search for specific hint
@hintclass merge             -- Hints by class
```

---

## Understanding Execution Plans

### Key Things to Look For

```sql
@xi <sql_id> 0
```

**Look for:**

1. **High Cardinality Estimates** (E-Rows vs A-Rows)
   - Large difference? → Stale/missing statistics

2. **TABLE ACCESS FULL on large tables**
   - Missing index?
   - Use: `@ash/ash_index_helper`

3. **Nested Loops with high A-Rows**
   - Should be hash join?
   - Hint: `USE_HASH(table)`

4. **No Parallel on large scans**
   - Could benefit from parallel?
   - Hint: `PARALLEL(table 4)`

5. **Note section**
   - SQL profile applied?
   - SQL plan baseline used?
   - Dynamic sampling used?

---

## SQL Tuning Checklist

### Before Tuning

- [ ] Get baseline metrics (executions, elapsed time, CPU time)
- [ ] Capture current plan: `@xi <sql_id> 0`
- [ ] Check ASH activity: `@ash/ashtop sql_id 1=1 &hour`
- [ ] Check bind variables: `@sqlbinds <sql_id> 0 %`

### During Analysis

- [ ] Verify statistics are current
- [ ] Check for missing indexes: `@ash/ash_index_helper`
- [ ] Review execution plan operations
- [ ] Look for cardinality misestimates
- [ ] Check for plan instability: `@awr/awr_sqlstats_unstable`

### After Tuning

- [ ] Verify new plan: `@xi <sql_id> 0`
- [ ] Compare metrics (before vs after)
- [ ] Monitor with ASH: `@ash/ashtop sql_id "sql_id='...'"`
- [ ] Test thoroughly in non-prod first!

---

## Quick Commands

```bash
# Find SQL tuning scripts
tpt -c "SQL Tuning"
tpt -k hint
tpt -k baseline
tpt -k profile

# Find SQL analysis scripts
tpt -c "SQL Analysis"
tpt -k execution
tpt -k plan
```

---

## Pro Tips

1. **Always Capture Before State**
   ```sql
   @sqlid <sql_id> 0 > before.txt
   @xi <sql_id> 0 >> before.txt
   ```

2. **Test in Non-Prod First**
   - Patches/profiles can sometimes make things worse
   - Always have a rollback plan

3. **One Change at a Time**
   - Don't create patch AND profile together
   - Change one thing, test, measure

4. **Monitor After Changes**
   ```sql
   -- Keep checking ASH
   @ash/ashtop sql_id,event2 "sql_id='...'" &hour
   ```

5. **Document Everything**
   - What was the problem?
   - What fix was applied?
   - What were the results?

---

## Troubleshooting Tuning Changes

### Patch/Profile Not Being Used?

```sql
-- Check if patch exists
SELECT name, status FROM dba_sql_patches WHERE name LIKE '%<sql_id>%';

-- Check if profile exists
SELECT name, status FROM dba_sql_profiles WHERE name LIKE '%<sql_id>%';

-- Check baseline exists
SELECT sql_handle, plan_name, enabled, accepted
FROM dba_sql_plan_baselines
WHERE sql_text LIKE '%<some_unique_text>%';

-- Flush shared pool to force reparse
ALTER SYSTEM FLUSH SHARED_POOL;
```

### Plan Still Bad After Fix?

- Hard parse may be needed: `ALTER SYSTEM FLUSH SHARED_POOL;`
- Check ENABLED/ACCEPTED status of baseline/profile
- Verify SQL text exactly matches (whitespace sensitive!)
- Check for conflicting profiles/baselines

---

*SQL Tuning Quick Reference - TPT Scripts - v1.0*
