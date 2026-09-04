# TPT Search Guide

This is the task-oriented companion to [README_TPT_SEARCH.md](README_TPT_SEARCH.md). Use it when you already know what kind of problem you are solving and want a fast way to locate the right TPT script.

## Before You Start

- For installation and option details, read [README_TPT_SEARCH.md](README_TPT_SEARCH.md)
- If you are already inside SQL*Plus, try `@help <keyword>` before using the shell tool

## Common Scenarios

### I Need to Inspect a SQL Statement

```bash
tpt sqlid.sql
tpt -k "execution plan"
tpt -k sql
```

Then in SQL*Plus:

```sql
@sqlid <sql_id> 0
@xi <sql_id> 0
```

### Sessions Are Blocking Each Other

```bash
tpt -k lock
tpt -k blocking
tpt ash/ash_wait_chains.sql
```

Then in SQL*Plus:

```sql
@lock 1=1
@ash/ash_wait_chains username 1=1 sysdate-1/24 sysdate
```

### I Need Live Performance Triage

```bash
tpt snapper.sql
tpt aw.sql
tpt -c "ASH Analysis"
```

Then in SQL*Plus:

```sql
@aw 1=1
@snapper ash 5 12 all
@ash/ashtop sql_id,event2 1=1 &hour
```

### I Need Historical Analysis

```bash
tpt -c "AWR Analysis"
tpt awr/awr_sqlstats.sql
tpt xawr.sql
```

Then in SQL*Plus:

```sql
@awr/awr_sqlstats <sql_id> % sysdate-7 sysdate
@xawr <sql_id> <plan_hash_value>
```

### I Need Memory or Space Scripts

```bash
tpt -c "Memory Management"
tpt -k tablespace
tpt df.sql
```

Then in SQL*Plus:

```sql
@sga
@pga
@df
```

## Useful Patterns

### Partial Name Search

```bash
tpt snap
tpt ashtop
```

### Multi-Word Search

```bash
tpt -k "wait chain"
tpt -p "execution plan"
```

### Category Discovery

```bash
tpt -lc
tpt -c "SQL Analysis"
```

### Example-Based Discovery

```bash
tpt -e sql_id
tpt -e "sysdate-1/24"
```

## Choosing Between Search Methods

| Use This | When |
|----------|------|
| `tpt-search.sh` | You want shell-side lookup with syntax/examples |
| `@help <keyword>` | You are already in SQL*Plus |
| `TPT_QUICK_REF.md` | You want a compact operator cheat sheet |
| `QUICKREF_*.md` | You want a workflow, not just script lookup |

## Quick Troubleshooting

```bash
cd /path/to/tpt-oracle
./tpt-search.sh --help
chmod +x ./tpt-search.sh
```
