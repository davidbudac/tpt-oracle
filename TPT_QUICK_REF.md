# TPT Search - Quick Reference Card

**One-page cheat sheet for tpt-search.sh**

---

## Setup (One Time)

```bash
# Add to ~/.bashrc or ~/.zshrc
alias tpt='/path/to/tpt-oracle/tpt-search.sh'
source ~/.bashrc
```

---

## Basic Usage

| What You Want | Command | Example |
|---------------|---------|---------|
| Find a script | `tpt <name>` | `tpt snapper.sql` |
| Search by keyword | `tpt -k <keyword>` | `tpt -k lock` |
| Search by category | `tpt -c <category>` | `tpt -c "SQL Analysis"` |
| List all scripts | `tpt -l` | `tpt -l` |
| List categories | `tpt -lc` | `tpt -lc` |
| Get help | `tpt -h` | `tpt -h` |

---

## Common Searches

```bash
# Performance Issues
tpt snapper.sql          # Session profiler
tpt aw.sql               # What's happening now
tpt -k performance       # All performance scripts

# SQL Problems
tpt sqlid.sql            # SQL details by ID
tpt -k "execution plan"  # Plan analysis
tpt xi.sql               # Explain plan from cache

# Session Issues
tpt s.sql                # Current session status
tpt ses.sql              # Session statistics
tpt -k session           # All session scripts

# Locks & Blocking
tpt lock.sql             # Current locks
tpt -k blocking          # Blocking scripts
tpt ash/ash_wait_chains.sql  # Wait chains

# Memory Issues
tpt -c "Memory Management"   # All memory scripts
tpt sga.sql              # SGA breakdown
tpt pga.sql              # PGA statistics

# Space Issues
tpt df.sql               # Tablespace usage (GB)
tpt dfm.sql              # Tablespace usage (MB)
tpt -k space             # All space scripts

# Wait Events
tpt -k wait              # Wait-related scripts
tpt sed.sql              # Event description
tpt evh.sql              # Event histogram

# ASH Analysis
tpt -c "ASH Analysis"    # All ASH scripts
tpt ash/ashtop.sql       # Top ASH activity
tpt ash/asqlmon.sql      # SQL monitor (ASH)
```

---

## All Options

| Short | Long | What It Does |
|-------|------|--------------|
| `-s` | `--script` | Search by name (default) |
| `-k` | `--keyword` | Search by keyword |
| `-c` | `--category` | Search by category |
| `-p` | `--purpose` | Search by description |
| `-e` | `--example` | Search in examples |
| `-l` | `--list` | List all scripts |
| `-lc` | `--list-categories` | List all categories |
| `-h` | `--help` | Show help |

---

## Quick Tips

✅ **Partial matches work**: `tpt snap` finds `snapper.sql`
✅ **Case insensitive**: `tpt SNAPPER` works fine
✅ **Use quotes**: `tpt -k "wait chain"` for multi-word
✅ **Pipe results**: `tpt -k lock | less`
✅ **Save output**: `tpt snapper.sql > ~/snapper_help.txt`

---

## Top 10 Most Used Scripts

| Script | What It Does | Basic Usage |
|--------|--------------|-------------|
| `snapper.sql` | Session profiler | `@snapper ash 5 12 all` |
| `s.sql` | Session status | `@s 123` |
| `sqlid.sql` | SQL details | `@sqlid <sql_id> 0` |
| `x.sql` | Explain last SQL | `@x` |
| `xi.sql` | Explain by SQL_ID | `@xi <sql_id> 0` |
| `ash/ashtop.sql` | Top ASH activity | `@ash/ashtop event2 1=1 sysdate-1/24 sysdate` |
| `lock.sql` | Current locks | `@lock 1=1` |
| `ses.sql` | Session stats | `@ses 123 %` |
| `aw.sql` | Current activity | `@aw 1=1` |
| `df.sql` | Space usage | `@df` |

---

## Categories at a Glance

- Performance Monitoring / Profiling
- Session Monitoring
- SQL Analysis
- Execution Plans
- ASH Analysis
- AWR Analysis
- SQL Tuning
- Lock Analysis
- Wait Analysis
- Memory Management
- Space Management
- Object Information
- Tracing / Diagnostics
- Transaction Monitoring
- Session Management
- User Management
- Scheduler / Jobs
- System Monitoring
- Utility

---

## Typical Workflows

### 1. Slow SQL Investigation
```bash
tpt sqlid.sql              # Get syntax
# In SQL*Plus:
@sqlid <sql_id> 0          # View SQL & stats
@xi <sql_id> 0             # View execution plan
@ash/asqlmon <sql_id> 0 sysdate-1/24 sysdate  # ASH analysis
```

### 2. Session Blocking
```bash
tpt -k lock                # Find lock scripts
@lock 1=1                  # See all locks
@ash/ash_wait_chains username 1=1 sysdate-1/24 sysdate  # Wait chains
```

### 3. Performance Baseline
```bash
@snapper ash 5 12 all      # Sample all sessions
@aw 1=1                    # Current metrics
@ses <sid> %               # Session stats
```

### 4. Memory Issues
```bash
@sga                       # SGA breakdown
@pga                       # PGA stats
@sgastat %                 # Detailed SGA
```

---

## Quick Syntax Reminders

### Time Ranges (ASH/AWR scripts)
```bash
sysdate-1/24 sysdate       # Last hour
sysdate-1 sysdate          # Last day
&hour                      # Shortcut: last hour
&5min                      # Shortcut: last 5 min
```

### SID Patterns
```bash
123                        # Single SID
123,456,789                # Multiple SIDs
all                        # All sessions
"select sid from v$session where username='APP'"  # Subquery
```

### Wildcards
```bash
%                          # Match anything
soe.%                      # All in schema
%.orders                   # Object in any schema
```

---

## Emergency Quick Checks

```bash
# What's happening RIGHT NOW?
@aw 1=1

# Who's connected?
@uu %

# Top SQL by activity
@ash/ashtop sql_id,event2 1=1 sysdate-1/24 sysdate

# Space running out?
@df

# Memory pressure?
@sga
@pga

# Lock issues?
@lock 1=1
```

---

## File Locations

```
~/github/tpt-oracle/
├── tpt-search.sh              # This script
├── SCRIPTS_CATALOG.txt        # Full catalog
├── SCRIPTS_CATALOG.md         # Markdown version
├── SCRIPTS_CATALOG.csv        # CSV version
├── README_TPT_SEARCH.md       # Full README
└── TPT_QUICK_REF.md          # This file
```

---

## Need More Help?

```bash
tpt -h                     # Script help
tpt -l                     # List all scripts
tpt -lc                    # List categories
cat README_TPT_SEARCH.md   # Full documentation
```

**In SQL*Plus:**
```sql
@help <keyword>            # Built-in TPT help
```

---

**Print This Page** | **Keep at Desk** | **Share with Team**

*Quick Reference v1.0 - TPT Search Tool - Last Updated: 2026-01-08*
