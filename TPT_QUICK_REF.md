# TPT Quick Reference

Short cheat sheet for finding scripts and running the most common TPT workflows.

## Setup

```bash
alias tpt='/path/to/tpt-oracle/tpt-search.sh'
source ~/.zshrc
```

## Shell Lookup

| What You Want | Command |
|---------------|---------|
| Find a script by name | `tpt snapper.sql` |
| Search by keyword | `tpt -k lock` |
| Search by category | `tpt -c "SQL Analysis"` |
| List cataloged scripts | `tpt -l` |
| List categories | `tpt -lc` |
| Show help | `tpt -h` |

## SQL*Plus Essentials

```sql
@help sql
@help lock
@help snapper
@init
```

## Common Lookups

```bash
tpt snapper.sql
tpt sqlid.sql
tpt xi.sql
tpt ash/ashtop.sql
tpt -k blocking
tpt -c "Memory Management"
```

## Common TPT Commands

### Slow SQL

```sql
@sqlid <sql_id> 0
@xi <sql_id> 0
@ash/asqlmon <sql_id> 0 sysdate-1/24 sysdate
```

### Blocking or Locks

```sql
@lock 1=1
@ash/ash_wait_chains username 1=1 sysdate-1/24 sysdate
```

### Live Performance Triage

```sql
@aw 1=1
@snapper ash 5 12 all
@ash/ashtop sql_id,event2 1=1 &hour
```

### Memory and Space

```sql
@sga
@pga
@df
```

## Useful Syntax Reminders

### Time Ranges

```sql
sysdate-1/24 sysdate
sysdate-1 sysdate
&hour
&5min
```

### SID Patterns

```sql
123
123,456,789
all
"select sid from v$session where username='APP'"
```

### Wildcards

```sql
%
soe.%
%.orders
```

## Pick the Right Reference

- Use [README_TPT_SEARCH.md](README_TPT_SEARCH.md) for the full search-tool guide
- Use [SEARCH_GUIDE.md](SEARCH_GUIDE.md) for task-oriented examples
- Use [QUICKREF_ASH_ANALYSIS.md](QUICKREF_ASH_ANALYSIS.md) for ASH workflows
- Use [QUICKREF_SQL_TUNING.md](QUICKREF_SQL_TUNING.md) for SQL tuning
- Use [QUICKREF_PERFORMANCE_MONITORING.md](QUICKREF_PERFORMANCE_MONITORING.md) for live monitoring
- Use [QUICKREF_MEMORY_SPACE.md](QUICKREF_MEMORY_SPACE.md) for memory and storage
