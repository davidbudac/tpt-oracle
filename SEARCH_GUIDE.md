# TPT Catalog Search Script Guide

## Quick Start

The `tpt-search.sh` script helps you quickly find and view TPT scripts from the catalog.

## Installation

### Option 1: Use Directly (No Setup Required)
```bash
cd /Users/davidbudac/github/tpt-oracle
./tpt-search.sh snapper.sql
```

### Option 2: Create an Alias (Recommended)
Add this to your `~/.bashrc` or `~/.zshrc`:

```bash
alias tpt='/Users/davidbudac/github/tpt-oracle/tpt-search.sh'
```

Then reload your shell:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

Now you can use it anywhere:
```bash
tpt snapper.sql
tpt -k lock
```

### Option 3: Add to PATH
```bash
# Create ~/bin if it doesn't exist
mkdir -p ~/bin

# Create a symlink
ln -s /Users/davidbudac/github/tpt-oracle/tpt-search.sh ~/bin/tpt

# Add ~/bin to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/bin:$PATH"
```

## Usage Examples

### 1. Find a Specific Script
```bash
./tpt-search.sh snapper.sql
./tpt-search.sh sqlid.sql
./tpt-search.sh ash/ashtop.sql
```

**Partial matches work:**
```bash
./tpt-search.sh snapper     # Finds snapper.sql
./tpt-search.sh ashtop      # Finds ash/ashtop.sql
```

### 2. Search by Keyword
```bash
# Find all scripts related to locks
./tpt-search.sh -k lock

# Find performance monitoring scripts
./tpt-search.sh -k performance

# Find scripts about wait chains
./tpt-search.sh -k "wait chain"

# Find ASH-related scripts
./tpt-search.sh --keyword ash
```

### 3. Search by Category
```bash
# Find all SQL Analysis scripts
./tpt-search.sh -c "SQL Analysis"

# Find all ASH scripts
./tpt-search.sh -c ash

# Find memory management scripts
./tpt-search.sh --category memory
```

### 4. Search by Purpose
```bash
# Find scripts that work with execution plans
./tpt-search.sh -p "execution plan"

# Find scripts for monitoring
./tpt-search.sh -p monitoring
```

### 5. Search in Examples
```bash
# Find scripts with examples using time ranges
./tpt-search.sh -e "sysdate-1/24"

# Find scripts with sql_id parameter
./tpt-search.sh -e sql_id
```

### 6. List All Scripts
```bash
# List all documented scripts
./tpt-search.sh -l

# List all categories
./tpt-search.sh -lc
```

### 7. Get Help
```bash
./tpt-search.sh --help
./tpt-search.sh -h
```

## Output Features

- **Color-coded output** (when terminal supports colors)
- **Highlighted search terms** for easy spotting
- **Complete script entries** with all parameters and examples
- **Multiple matches** shown when searching by keyword/category

## Real-World Examples

### Example 1: I need to analyze a slow SQL
```bash
$ tpt -k "sql analysis"
# Shows: sqlid.sql, sqlmon.sql, ash/asqlmon.sql, etc.

$ tpt sqlid.sql
# Shows full syntax: @sqlid <sql_id> <child_number>
```

### Example 2: Sessions are blocking each other
```bash
$ tpt -k lock
# Shows: lock.sql, ash/ash_wait_chains.sql

$ tpt lock.sql
# Shows: @lock <filter_expression>
# Example: @lock type='TM'
```

### Example 3: I need to see execution plans
```bash
$ tpt -c "execution plans"
# Shows: x.sql, xi.sql, xawr.sql, xa.sql

$ tpt xi.sql
# Shows: @xi <sql_id> <child_number>
```

### Example 4: Looking for ASH analysis tools
```bash
$ tpt -k ash
# Shows all ASH-related scripts

$ tpt -c "ASH Analysis"
# Shows specifically categorized ASH scripts
```

### Example 5: Finding memory management scripts
```bash
$ tpt -lc
# Browse all categories

$ tpt -c "Memory Management"
# Shows: sga.sql, pga.sql, sgastat.sql, mem.sql
```

## Tips & Tricks

1. **Use quotes for multi-word searches:**
   ```bash
   tpt -k "wait chain"
   tpt -c "SQL Analysis"
   ```

2. **Partial matches work everywhere:**
   ```bash
   tpt snap        # Finds snapper.sql
   tpt ash/ash     # Finds ash/ashtop.sql, ash/asqlmon.sql, etc.
   ```

3. **Case doesn't matter:**
   ```bash
   tpt SNAPPER.SQL    # Works!
   tpt -k LOCK        # Works!
   ```

4. **Combine with other tools:**
   ```bash
   # Search and page through results
   tpt -k lock | less

   # Count how many scripts match
   tpt -k performance | grep "^SCRIPT:" | wc -l

   # Save results to file
   tpt -k ash > ash_scripts.txt
   ```

5. **Quick reference:**
   ```bash
   tpt -l | grep -i sql     # Find all SQL-related scripts
   tpt -lc                  # See all categories at a glance
   ```

## Troubleshooting

### Script not found
```bash
# Make sure you're in the correct directory
cd /Users/davidbudac/github/tpt-oracle

# Or use full path
/Users/davidbudac/github/tpt-oracle/tpt-search.sh snapper.sql
```

### Permission denied
```bash
# Make sure script is executable
chmod +x /Users/davidbudac/github/tpt-oracle/tpt-search.sh
```

### Alias not working
```bash
# Make sure you reloaded your shell config
source ~/.bashrc   # or source ~/.zshrc

# Or open a new terminal window
```

## Integration with SQL*Plus

Once you find the script you need, use it in SQL*Plus:

```bash
# 1. Find the script
tpt snapper.sql
# Shows: @snapper [options] <seconds> <snapshots> <sid>

# 2. Copy the syntax and use in SQL*Plus
sqlplus user/pass@db
SQL> @snapper ash 5 12 all
```

## See Also

- **SCRIPTS_CATALOG.txt** - Raw catalog (for direct grep)
- **SCRIPTS_CATALOG.md** - Markdown version (for browsing)
- **SCRIPTS_CATALOG.csv** - Spreadsheet version
- **help.sql** - Built-in help in SQL*Plus: `@help <keyword>`

## Feedback & Issues

If you find any issues with the search script or want to suggest improvements, check the repository for the latest version.
