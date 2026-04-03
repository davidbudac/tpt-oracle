# Memory & Space Management - Quick Reference

**Managing Oracle memory and storage**

---

## Memory Quick Checks

| What | Script | Example |
|------|--------|---------|
| SGA overview | `sga.sql` | `@sga` |
| PGA overview | `pga.sql` | `@pga` |
| Space overview | `df.sql` | `@df` |
| Tablespace list | `ts.sql` | `@ts %` |

---

## Part 1: Memory Management

### SGA (System Global Area)

#### View SGA Components

```sql
-- SGA overview with dynamic components
@sga

-- Detailed breakdown
@sgastat %

-- Specific component
@sgastat "shared pool"
@sgastat "buffer cache"
@sgastat "free memory"

-- By subpool (X$ version)
@sgastatx "free memory"
```

#### SGA Resize Operations

```sql
-- Recent resize operations
@sgares

-- All memory resize operations
@memres
```

#### Shared Pool Analysis

```sql
-- Free memory in shared pool
@sgastat "free memory"

-- Shared pool stats by subpool
@sgastatx %

-- Extended SGA statistics (X$ tables)
@sgastatx "free memory"

-- Top SQL by memory usage
@topcur
@topcurmem

-- Memory for specific SQL
@sqlmem <sql_id>

-- Memory by hash value
@sqlmemh <hash_value>

-- Memory by SQL_ID
@sqlmemx <sql_id>

-- Row cache (dictionary cache)
@rowcache %
```

### PGA (Program Global Area)

#### View PGA Usage

```sql
-- PGA statistics overview
@pga

-- PGA by session
@wrka 1=1
@wrka sid=123

-- Workarea summary by operation
@wrkasum 1=1
@wrkasum sql_id='7q729nhdgtsqq'
```

#### Session Memory

```sql
-- Session memory (PGA+UGA)
@smem <sid>
@smem 123

-- Process memory detail
@pmem <spid>
@pmem 12345

-- Session+process info
@usid <sid>
```

### Memory Troubleshooting

#### Issue: Out of Memory Errors

```sql
-- 1. Check SGA free space
@sgastat "free memory"

-- 2. Check PGA usage
@pga

-- 3. Top memory consumers
@wrka 1=1
@topcurmem

-- 4. Session memory usage
@smem <sid>
```

#### Issue: Shared Pool Exhaustion

```sql
-- 1. Free memory in shared pool
@sgastat "shared pool"

-- 2. Top cursors
@topcur

-- 3. SQL using most memory
@sqlmem <sql_id>

-- 4. Flush shared pool (if necessary)
-- ALTER SYSTEM FLUSH SHARED_POOL;
```

#### Issue: PGA/TEMP Space Issues

```sql
-- 1. Who's using PGA/TEMP?
@wrka 1=1

-- 2. Workarea operations
@wrkasum 1=1

-- 3. Session detail
@smem <sid>

-- 4. Temp tablespace usage
@temp
@df
```

---

## Part 2: Space Management

### Quick Space Checks

```sql
-- All tablespaces (GB)
@df

-- All tablespaces (MB)
@dfm

-- Specific tablespace
@ts USERS
@ts %

-- Tablespace with datafiles
@ls USERS
@ls %
```

### Segment Space Usage

```sql
-- Top segments by size
@topseg %
@topseg USERS

-- Specific segment info
@seg soe.orders
@seg soe.%

-- Segment with extents
@segext soe.orders

-- Table info with storage
@tab soe.orders
@tab soe.%
```

### Table Space Analysis

```sql
-- Table storage
@tab soe.orders

-- Table partitions
@tabpart soe.orders

-- Table subpartitions
@tabsubpart soe.orders

-- Partition keys
@partkeys soe.orders
```

### Index Space

```sql
-- Index storage
@ind soe.ord_customer_ix
@ind soe.%

-- Indexes on table
@ind orders

-- Extended index info
@ind2 soe.ord_customer_ix
@indf soe.ord_customer_ix
```

### LOB Space

```sql
-- LOB segment info
@lob soe.customers
@lob soe.%
```

### Extended Object Information

```sql
-- Extended table info
@tab2 soe.orders

-- Constraint information
@cons soe.orders
@cons2 soe.orders

-- Object dependencies
@dep soe.orders

-- Partition monitoring
@partmon soe.orders

-- Segment statistics
@segstat soe.orders
@segstat2 soe.orders
```

### Object-Level I/O

```sql
-- Top segments by reads
@topsegstat reads

-- Top segments by writes
@topsegstat writes

-- Top segments by physical I/O
@topsegstat physical%

-- Blocks in buffer cache
@segcached soe.orders

-- Extended cached info
@segcachedx soe.orders
```

---

## Space Troubleshooting

### Issue: Tablespace Almost Full

```sql
-- 1. Check space
@df

-- 2. Find big segments
@topseg <tablespace_name>

-- 3. Check segment details
@seg <owner>.<segment>

-- 4. Options:
--    - Add datafile
--    - Resize datafile
--    - Enable autoextend
--    - Purge/archive data
--    - Reorganize segments
```

### Issue: Table Growing Too Fast

```sql
-- 1. Current size
@tab soe.orders

-- 2. Segment extents
@segext soe.orders

-- 3. Check I/O activity
@topsegstat writes

-- 4. Partition info (if partitioned)
@tabpart soe.orders

-- 5. LOBs (if applicable)
@lob soe.orders
```

### Issue: Need to Identify Space Hogs

```sql
-- Top tables
SELECT owner, segment_name, bytes/1024/1024 mb
FROM dba_segments
WHERE segment_type = 'TABLE'
ORDER BY bytes DESC
FETCH FIRST 20 ROWS ONLY;

-- Or use:
@topseg %
```

---

## Memory Best Practices

### 1. Regular Monitoring

```sql
-- Daily checks
@sga
@pga
@sgastat "free memory"
@wrka 1=1
```

### 2. Set Appropriate Parameters

```sql
-- Check current settings
@p sga_target
@p pga_aggregate_target
@p memory_target
@p memory_max_target

-- For ASMM (Automatic Shared Memory Management)
-- Set SGA_TARGET and PGA_AGGREGATE_TARGET

-- For AMM (Automatic Memory Management)
-- Set MEMORY_TARGET and MEMORY_MAX_TARGET
```

### 3. Monitor Resize Operations

```sql
-- Check if automatic resizing is working
@sgares
@memres

-- Look for failed resize operations
```

### 4. Identify Memory Hogs

```sql
-- Top SQL by memory
@topcur
@topcurmem

-- Sessions using most PGA
@wrka 1=1
```

---

## Space Best Practices

### 1. Regular Space Monitoring

```sql
-- Weekly checks
@df
@topseg %

-- Monitor growth trends
```

### 2. Proactive Management

```sql
-- Set datafiles to autoextend
ALTER DATABASE DATAFILE '/path/to/file' AUTOEXTEND ON NEXT 100M MAXSIZE 10G;

-- Monitor autoextend files approaching maxsize
```

### 3. Segment Management

```sql
-- Enable automatic segment space management
-- CREATE TABLESPACE ... SEGMENT SPACE MANAGEMENT AUTO;

-- Monitor fragmentation
-- Consider reorganization for heavily fragmented segments
```

### 4. Archive/Purge Old Data

```sql
-- Identify old data
-- Implement archiving strategy
-- Use partitioning for easier management
```

---

## Common Commands Cheat Sheet

### Memory

```sql
# SGA
@sga                          # Overview
@sgastat %                    # Detailed
@sgastat "free memory"        # Free space
@sgares                       # Resize history

# PGA
@pga                          # Overview
@wrka 1=1                     # By session
@wrkasum 1=1                  # By operation

# Session
@smem <sid>                   # Session memory
@pmem <spid>                  # Process memory

# SQL Memory
@topcur                       # Top cursors
@sqlmem <sql_id>             # SQL memory
```

### Space

```sql
# Tablespace
@df                           # All tablespaces (GB)
@dfm                          # All tablespaces (MB)
@ts %                         # List tablespaces
@ls USERS                     # Tablespace detail

# Segments
@topseg %                     # Top segments
@seg soe.orders              # Segment info
@segcached soe.orders        # In buffer cache

# Tables
@tab soe.orders              # Table info
@tabpart soe.orders          # Partitions

# Indexes
@ind orders                   # Indexes on table
@ind soe.ord_ix              # Index info
```

---

## Emergency Space Actions

### Immediate Actions When Tablespace Full

```sql
-- 1. Check current usage
@df

-- 2. Identify largest segments
@topseg <tablespace_name>

-- 3. Quick fixes (choose one):

-- Option A: Add datafile
ALTER TABLESPACE <name> ADD DATAFILE '/path/to/new/file.dbf' SIZE 1G;

-- Option B: Resize existing datafile
ALTER DATABASE DATAFILE '/path/to/file.dbf' RESIZE 5G;

-- Option C: Enable autoextend
ALTER DATABASE DATAFILE '/path/to/file.dbf' AUTOEXTEND ON NEXT 100M MAXSIZE 10G;

-- 4. Verify
@df
```

---

## Memory Monitoring Script

```bash
#!/bin/bash
# Save as: check_memory.sh

echo "=== Memory Status Check ==="
echo ""

sqlplus -S / as sysdba << EOF
set pagesize 50
@sga
@pga
@sgastat "free memory"
@wrka 1=1
EOF
```

## Space Monitoring Script

```bash
#!/bin/bash
# Save as: check_space.sh

echo "=== Space Status Check ==="
echo ""

sqlplus -S / as sysdba << EOF
set pagesize 100
@df
@topseg %
EOF
```

---

## Search for Memory/Space Scripts

```bash
# Memory scripts
tpt -c "Memory Management"
tpt -k sga
tpt -k pga
tpt -k memory

# Space scripts
tpt -c "Space Management"
tpt -k tablespace
tpt -k segment
tpt -k storage
```

---

## Key Thresholds to Monitor

### Memory Thresholds

| Metric | Threshold | Action |
|--------|-----------|--------|
| SGA free memory | < 10% | Investigate memory consumers |
| PGA allocated | > 80% of target | Check session memory usage |
| Shared pool free | < 10% | Consider flushing or increasing |
| Parse count (hard) | High | Check cursor sharing |

### Space Thresholds

| Metric | Threshold | Action |
|--------|-----------|--------|
| Tablespace free | < 15% | Add space or purge data |
| Datafile at maxsize | > 90% | Increase maxsize or add datafile |
| Segment growth | Unexpected | Investigate application |
| TEMP usage | Consistently high | Tune SQL, increase TEMP |

---

## Pro Tips

1. **Automate Monitoring**
   - Set up daily/hourly checks
   - Alert on thresholds
   - Track trends over time

2. **Use Appropriate Units**
   - `@df` for GB (easier to read)
   - `@dfm` for MB (more precision)

3. **Know Your Baselines**
   - What's normal for your system?
   - Compare current to baseline
   - Investigate deviations

4. **Plan for Growth**
   - Monitor growth rates
   - Project future needs
   - Add space proactively

5. **Document Changes**
   - When you add space, document why
   - Track resize operations
   - Note unusual events

---

*Memory & Space Management Quick Reference - TPT Scripts - v1.0*
