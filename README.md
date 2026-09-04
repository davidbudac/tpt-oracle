# Tanel Poder's Troubleshooting Scripts (TPT)

TPT is a large collection of Oracle Database troubleshooting and performance scripts designed to run directly from SQL*Plus or SQL Developer.

The core design constraints are deliberate:

- No database objects need to be created for normal use
- Most work is done with SQL*Plus commands and anonymous PL/SQL
- Scripts read dynamic performance views directly
- The toolkit is usable even in restrictive change-management environments

## Quick Start

Set `SQLPATH` to the repository root so SQL*Plus can find the scripts:

```bash
export SQLPATH=/path/to/tpt-oracle
sqlplus user/pass@db
```

Once connected, start with:

```sql
@help sql
@help lock
@help snapper
```

If you want TPT-style SQL*Plus defaults for line width, formatting, and helper variables:

```sql
@init
```

## Start Here

| Task | Script | Example |
|------|--------|---------|
| Find the right script | `help.sql` | `@help explain` |
| Profile live activity | `snapper.sql` | `@snapper ash 5 12 all` |
| Check current activity | `aw.sql` | `@aw 1=1` |
| Inspect a session | `s.sql` | `@s 123` |
| Inspect a SQL statement | `sqlid.sql` | `@sqlid 7q729nhdgtsqq 0` |
| Show an execution plan | `xi.sql` | `@xi 7q729nhdgtsqq 0` |
| Analyze recent ASH activity | `ash/ashtop.sql` | `@ash/ashtop sql_id,event2 1=1 &hour` |
| Check locks and blocking | `lock.sql` | `@lock 1=1` |

## Common Workflows

### Slow SQL

```sql
@sqlid <sql_id> 0
@xi <sql_id> 0
@ash/asqlmon <sql_id> 0 sysdate-1/24 sysdate
```

### Blocking or Lock Contention

```sql
@lock 1=1
@ash/ash_wait_chains username 1=1 sysdate-1/24 sysdate
```

### General Performance Triage

```sql
@aw 1=1
@snapper ash 5 12 all
@ash/ashtop sql_id,event2 1=1 &hour
```

### Memory and Space Checks

```sql
@sga
@pga
@df
```

## Documentation

Start with these files:

- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md): overview of the docs set
- [TPT_QUICK_REF.md](TPT_QUICK_REF.md): short operator cheat sheet
- [README_TPT_SEARCH.md](README_TPT_SEARCH.md): canonical guide for `tpt-search.sh`
- [SEARCH_GUIDE.md](SEARCH_GUIDE.md): task-oriented search examples
- [QUICKREF_ASH_ANALYSIS.md](QUICKREF_ASH_ANALYSIS.md): ASH workflows
- [QUICKREF_SQL_TUNING.md](QUICKREF_SQL_TUNING.md): SQL tuning workflows
- [QUICKREF_PERFORMANCE_MONITORING.md](QUICKREF_PERFORMANCE_MONITORING.md): live monitoring workflows
- [QUICKREF_MEMORY_SPACE.md](QUICKREF_MEMORY_SPACE.md): memory and storage workflows

## Repository Layout

- `ash/`: ASH-based analysis scripts
- `awr/`: AWR-based analysis scripts
- `setup/`: setup, grants, and helper files
- `tools/`: helper tools and utilities
- repository root: the main SQL*Plus script library

## Notes

- Many scripts require access to `V$` or `GV$` views
- Some advanced scripts also depend on `X$` access or additional privileges
- TPT ASH scripts sample live session state; they are distinct from querying licensed AWR history

## References

- Website: <https://tanelpoder.com>
- YouTube: <https://www.youtube.com/tanelpoder>
- Twitter/X: <https://twitter.com/tanelpoder>
- License: [LICENSE.txt](LICENSE.txt)
