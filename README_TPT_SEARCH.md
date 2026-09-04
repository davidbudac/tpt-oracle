# TPT Search Tool

`tpt-search.sh` is a shell-side helper for finding commonly used TPT scripts before you open SQL*Plus or while you are browsing the repository.

## Scope

The search tool does not scan the repository dynamically. It reads the curated catalog in [SCRIPTS_CATALOG.txt](SCRIPTS_CATALOG.txt).

That means:

- It is fast and predictable
- It returns documented reference entries with syntax and examples
- It covers a curated subset, not every SQL file in the repository

If you are already inside SQL*Plus, use `@help <keyword>` first. If you want broader metadata outside the CLI catalog, inspect [SCRIPTS_CATALOG.md](SCRIPTS_CATALOG.md) or [scripts_data.js](scripts_data.js).

## Installation

### Direct Usage

```bash
cd /path/to/tpt-oracle
./tpt-search.sh snapper.sql
```

### Alias

```bash
alias tpt='/path/to/tpt-oracle/tpt-search.sh'
source ~/.zshrc
```

### Add to PATH

```bash
mkdir -p ~/bin
ln -s /path/to/tpt-oracle/tpt-search.sh ~/bin/tpt
export PATH="$HOME/bin:$PATH"
source ~/.zshrc
```

## Usage

```text
tpt-search.sh [options] <search_term>
```

| Option | Meaning |
|--------|---------|
| `-s`, `--script` | Search by script name |
| `-k`, `--keyword` | Search by keyword |
| `-c`, `--category` | Search by category |
| `-p`, `--purpose` | Search by purpose text |
| `-e`, `--example` | Search inside examples |
| `-l`, `--list` | List all cataloged scripts |
| `-lc`, `--list-categories` | List all categories |
| `-h`, `--help` | Show help |

## Common Examples

### Find a Specific Script

```bash
tpt snapper.sql
tpt sqlid.sql
tpt ash/ashtop.sql
```

### Search by Keyword

```bash
tpt -k lock
tpt -k "wait chain"
tpt -k performance
```

### Search by Category

```bash
tpt -c "SQL Analysis"
tpt -c "ASH Analysis"
tpt -c "Memory Management"
```

### Search by Purpose or Example

```bash
tpt -p "execution plan"
tpt -e "sysdate-1/24"
tpt -e sql_id
```

### Browse the Catalog

```bash
tpt -l
tpt -lc
```

## Typical Flow

Use the search tool in the shell:

```bash
tpt sqlid.sql
```

Then run the actual script in SQL*Plus:

```sql
@sqlid 7q729nhdgtsqq 0
```

Another example:

```bash
tpt -k lock
```

```sql
@lock 1=1
@ash/ash_wait_chains username 1=1 sysdate-1/24 sysdate
```

## Troubleshooting

### Script Not Found

```bash
cd /path/to/tpt-oracle
./tpt-search.sh snapper.sql
```

### Permission Denied

```bash
chmod +x /path/to/tpt-oracle/tpt-search.sh
```

### Alias Not Working

```bash
source ~/.zshrc
```

## Related Files

- [SEARCH_GUIDE.md](SEARCH_GUIDE.md): task-oriented example searches
- [TPT_QUICK_REF.md](TPT_QUICK_REF.md): short cheat sheet
- [SCRIPTS_CATALOG.txt](SCRIPTS_CATALOG.txt): canonical CLI catalog
- [SCRIPTS_CATALOG.csv](SCRIPTS_CATALOG.csv): spreadsheet export of the curated catalog
- [SCRIPTS_CATALOG.md](SCRIPTS_CATALOG.md): larger browsable catalog artifact
- [tools/generate_search_catalog_csv.py](tools/generate_search_catalog_csv.py): regenerate the curated CSV export

## Maintenance

- Keep this document aligned with the actual options in [tpt-search.sh](tpt-search.sh)
- Treat [SCRIPTS_CATALOG.txt](SCRIPTS_CATALOG.txt) as the search tool's canonical input
- If you change curated catalog entries, regenerate [SCRIPTS_CATALOG.csv](SCRIPTS_CATALOG.csv) with `python3 tools/generate_search_catalog_csv.py`
