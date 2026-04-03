# TPT Catalog Search Script

A powerful command-line search tool for Tanel Poder's TPT (Troubleshooting & Performance Tools) scripts catalog. Quickly find the right Oracle database troubleshooting script with intelligent search and filtering.

## Features

- 🔍 **Multiple Search Modes** - Search by script name, keyword, category, purpose, or examples
- 🎨 **Color-Coded Output** - Easy-to-read, highlighted results
- ⚡ **Fast & Lightweight** - Pure bash, no dependencies
- 📚 **Comprehensive Catalog** - 50+ most important TPT scripts documented
- 💡 **Smart Matching** - Case-insensitive, partial matching supported
- 📋 **List & Browse** - View all scripts and categories at a glance

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Search Modes](#search-modes)
- [Examples](#examples)
- [Options Reference](#options-reference)
- [Integration with SQL*Plus](#integration-with-sqlplus)
- [Tips & Tricks](#tips--tricks)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Installation

### Prerequisites

- Bash shell (Linux, macOS, WSL, Git Bash)
- The TPT scripts repository cloned locally
- The catalog files (SCRIPTS_CATALOG.txt, .md, .csv)

### Method 1: Direct Usage (No Setup)

Simply run the script from its location:

```bash
cd /path/to/tpt-oracle
./tpt-search.sh snapper.sql
```

### Method 2: Create an Alias (Recommended)

Add to your `~/.bashrc`, `~/.bash_profile`, or `~/.zshrc`:

```bash
alias tpt='/path/to/tpt-oracle/tpt-search.sh'
```

Reload your shell configuration:

```bash
source ~/.bashrc  # or source ~/.zshrc
```

Now use from anywhere:

```bash
tpt snapper.sql
tpt -k lock
```

### Method 3: Add to PATH

```bash
# Create ~/bin directory if it doesn't exist
mkdir -p ~/bin

# Create a symlink
ln -s /path/to/tpt-oracle/tpt-search.sh ~/bin/tpt

# Add ~/bin to PATH (add this to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/bin:$PATH"

# Reload your shell
source ~/.bashrc
```

Now use `tpt` command globally:

```bash
tpt snapper.sql
```

### Verify Installation

```bash
./tpt-search.sh --help
```

You should see the help message with all available options.

## Quick Start

```bash
# Find a specific script
./tpt-search.sh snapper.sql

# Search for scripts about locks
./tpt-search.sh -k lock

# View all SQL Analysis scripts
./tpt-search.sh -c "SQL Analysis"

# List all available scripts
./tpt-search.sh -l

# Get help
./tpt-search.sh --help
```

## Usage

```
tpt-search.sh [options] <search_term>
```

### Basic Syntax

```bash
# Search by script name (default behavior)
tpt-search.sh <script_name>

# Search with specific mode
tpt-search.sh -k <keyword>
tpt-search.sh -c <category>
tpt-search.sh -p <purpose>
```

## Search Modes

### 1. Script Name Search (Default)

Find a script by its name. Partial matches work!

```bash
./tpt-search.sh snapper.sql
./tpt-search.sh snapper          # Partial match works
./tpt-search.sh ash/ashtop.sql
./tpt-search.sh ashtop           # Partial match works
```

**Output includes:**
- Script name and category
- Complete list of keywords
- Purpose/description
- Full syntax with parameter explanations
- Multiple usage examples

### 2. Keyword Search

Find all scripts related to a specific topic or functionality.

```bash
./tpt-search.sh -k lock           # Find lock-related scripts
./tpt-search.sh -k performance    # Find performance monitoring scripts
./tpt-search.sh -k "wait chain"   # Multi-word search
./tpt-search.sh --keyword ash     # Long form option
```

**Use keywords like:**
- `lock`, `blocking`, `contention`
- `performance`, `monitoring`, `profiling`
- `sql`, `execution`, `plan`
- `memory`, `sga`, `pga`
- `session`, `wait`, `event`

### 3. Category Search

Browse scripts by functional category.

```bash
./tpt-search.sh -c "SQL Analysis"
./tpt-search.sh -c ash
./tpt-search.sh -c memory
./tpt-search.sh --category "Execution Plans"
```

**Available categories:**
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
- And more... (use `-lc` to see all)

### 4. Purpose Search

Find scripts by what they do.

```bash
./tpt-search.sh -p "execution plan"
./tpt-search.sh -p monitoring
./tpt-search.sh -p "session statistics"
./tpt-search.sh --purpose "wait events"
```

### 5. Example Search

Find scripts by looking at their usage examples.

```bash
./tpt-search.sh -e "sysdate-1/24"    # Scripts with time ranges
./tpt-search.sh -e sql_id            # Scripts using sql_id
./tpt-search.sh -e "@snapper"        # Scripts showing snapper usage
./tpt-search.sh --example ash        # Scripts with ASH examples
```

### 6. List & Browse

View all scripts or categories in the catalog.

```bash
./tpt-search.sh -l      # List all scripts (numbered)
./tpt-search.sh -lc     # List all categories with counts
./tpt-search.sh --list
./tpt-search.sh --list-categories
```

## Examples

### Example 1: Finding a Script to Monitor Sessions

```bash
$ ./tpt-search.sh -k session
```

**Result:** Shows all session-related scripts (s.sql, ses.sql, ses2.sql, etc.)

### Example 2: Analyzing Slow SQL

**Problem:** You have a slow SQL statement with SQL_ID: `7q729nhdgtsqq`

```bash
# Step 1: Find relevant scripts
$ ./tpt-search.sh -k sql

# Step 2: Get details on a specific script
$ ./tpt-search.sh sqlid.sql
```

**Output shows:**
```
SYNTAX: @sqlid <sql_id> <child_number>
EXAMPLES:
  @sqlid 7q729nhdgtsqq 0
  @sqlid 7q729nhdgtsqq %
```

**Now use in SQL*Plus:**
```sql
SQL> @sqlid 7q729nhdgtsqq 0
```

### Example 3: Investigating Blocking Sessions

```bash
# Find lock-related scripts
$ ./tpt-search.sh -k blocking

# Get details on lock analysis
$ ./tpt-search.sh lock.sql
```

**Shows you can use:**
```sql
@lock 1=1
@lock type='TM'
@lock sid=123
```

### Example 4: Viewing Execution Plans

```bash
# Find execution plan scripts
$ ./tpt-search.sh -c "Execution Plans"
```

**Shows:** x.sql, xa.sql, xi.sql, xawr.sql with their differences

### Example 5: Memory Analysis

```bash
# List all memory-related scripts
$ ./tpt-search.sh -c "Memory Management"
```

**Result:** sga.sql, pga.sql, sgastat.sql, mem.sql

### Example 6: Using ASH for Performance Analysis

```bash
# Find ASH scripts
$ ./tpt-search.sh -k ash

# Get details on ASH top activity
$ ./tpt-search.sh ash/ashtop.sql
```

**Syntax shown:**
```
@ash/ashtop <grouping_cols> <filters> <from_time> <to_time>
```

**Example usage:**
```sql
@ash/ashtop username,event2 1=1 sysdate-1/24 sysdate
```

## Options Reference

| Short | Long | Description | Example |
|-------|------|-------------|---------|
| `-s` | `--script` | Search by script name (default) | `tpt -s sqlid` |
| `-k` | `--keyword` | Search by keyword | `tpt -k lock` |
| `-c` | `--category` | Search by category | `tpt -c "SQL Analysis"` |
| `-p` | `--purpose` | Search by purpose/description | `tpt -p "execution plan"` |
| `-e` | `--example` | Search in examples | `tpt -e sysdate` |
| `-l` | `--list` | List all scripts | `tpt -l` |
| `-lc` | `--list-categories` | List all categories | `tpt -lc` |
| `-i` | `--ignore-case` | Case-insensitive (default) | `tpt -i LOCK` |
| `-h` | `--help` | Show help message | `tpt -h` |

## Integration with SQL*Plus

The search script is designed to work seamlessly with SQL*Plus:

### Workflow

1. **Find the script** you need:
   ```bash
   tpt -k "execution plan"
   ```

2. **View syntax** and examples:
   ```bash
   tpt xi.sql
   ```

3. **Use in SQL*Plus**:
   ```bash
   sqlplus user/pass@database
   SQL> @xi 7q729nhdgtsqq 0
   ```

### Setting Up TPT Scripts in SQL*Plus

Make sure your `SQLPATH` points to the TPT directory:

```bash
# In your shell (add to ~/.bashrc or ~/.bash_profile)
export SQLPATH=/path/to/tpt-oracle

# Or in SQL*Plus
SQL> define _editor=vi
SQL> @login.sql
```

## Tips & Tricks

### 1. Partial Matches Work Everywhere

```bash
tpt snap           # Finds snapper.sql
tpt sqlid          # Finds sqlid.sql
tpt ash/ash        # Finds ash/ashtop.sql, ash/asqlmon.sql, etc.
```

### 2. Case Doesn't Matter

```bash
tpt SNAPPER.SQL    # Works!
tpt -k LOCK        # Works!
tpt -c "sql analysis"  # Works!
```

### 3. Use Quotes for Multi-Word Searches

```bash
tpt -k "wait chain"         # Correct
tpt -k wait chain           # Wrong - only searches "wait"

tpt -c "SQL Analysis"       # Correct
tpt -c SQL Analysis         # Wrong
```

### 4. Combine with Unix Tools

```bash
# Page through results
tpt -k lock | less

# Count matching scripts
tpt -k performance | grep "^SCRIPT:" | wc -l

# Save results
tpt -c "ASH Analysis" > ash_scripts.txt

# Search within results
tpt -l | grep -i sql
```

### 5. Quick Category Browse

```bash
# See all categories
tpt -lc

# Then search specific category
tpt -c "Memory Management"
```

### 6. Find Scripts by Parameter Type

```bash
# Find scripts that use sql_id
tpt -e sql_id

# Find scripts with time ranges
tpt -e "sysdate-1/24"

# Find scripts using SID
tpt -e "sid="
```

### 7. Common Search Patterns

```bash
# Performance troubleshooting
tpt -k performance
tpt snapper.sql

# SQL tuning
tpt -c "SQL Tuning"
tpt -k hint

# Wait events
tpt -k wait
tpt -p "wait event"

# Locks and blocking
tpt -k lock
tpt -k blocking

# Memory issues
tpt -c "Memory Management"
tpt -k memory

# Space issues
tpt -k space
tpt df.sql
```

## Troubleshooting

### Script Not Found Error

**Problem:**
```bash
./tpt-search.sh: command not found
```

**Solution:**
```bash
# Make sure you're in the correct directory
cd /path/to/tpt-oracle

# Or use full path
/path/to/tpt-oracle/tpt-search.sh snapper.sql
```

### Permission Denied

**Problem:**
```bash
bash: ./tpt-search.sh: Permission denied
```

**Solution:**
```bash
# Make script executable
chmod +x /path/to/tpt-oracle/tpt-search.sh
```

### Catalog File Not Found

**Problem:**
```bash
Error: Catalog file not found at /path/to/SCRIPTS_CATALOG.txt
```

**Solution:**
```bash
# Ensure SCRIPTS_CATALOG.txt exists in the same directory as the script
ls -la /path/to/tpt-oracle/SCRIPTS_CATALOG.txt

# If missing, regenerate catalog files
```

### Alias Not Working

**Problem:**
```bash
tpt: command not found
```

**Solution:**
```bash
# Make sure you added alias to correct file
# For bash: ~/.bashrc or ~/.bash_profile
# For zsh: ~/.zshrc

# Add this line:
alias tpt='/path/to/tpt-oracle/tpt-search.sh'

# Reload configuration
source ~/.bashrc  # or source ~/.zshrc

# Or open a new terminal window
```

### No Output or Blank Results

**Problem:** Script runs but shows no results

**Solution:**
```bash
# Check if search term matches anything
tpt -l | grep -i <your_search_term>

# Try broader search
tpt -k sql     # Instead of -k "specific thing"

# List all categories to see what's available
tpt -lc
```

### Line Ending Issues (Windows)

**Problem:**
```bash
/usr/bin/env: 'bash\r': No such file or directory
```

**Solution:**
```bash
# Convert line endings from Windows (CRLF) to Unix (LF)
dos2unix tpt-search.sh

# Or use sed
sed -i 's/\r$//' tpt-search.sh
```

## File Structure

```
tpt-oracle/
├── tpt-search.sh              # Main search script
├── SCRIPTS_CATALOG.txt        # Text catalog (used by script)
├── SCRIPTS_CATALOG.md         # Markdown catalog (for reading)
├── SCRIPTS_CATALOG.csv        # CSV catalog (for spreadsheets)
├── README_TPT_SEARCH.md       # This file
├── SEARCH_GUIDE.md            # Detailed usage guide
├── CLAUDE.md                  # AI assistant guidance
└── [700+ .sql scripts...]     # TPT scripts
```

## Catalog Coverage

Currently catalogs **50+ most important TPT scripts** including:

- **Performance Monitoring:** snapper.sql, aw.sql
- **Session Analysis:** s.sql, ses.sql, long.sql
- **SQL Analysis:** sqlid.sql, sqlmon.sql, hash.sql
- **Execution Plans:** x.sql, xi.sql, xawr.sql
- **ASH Analysis:** ashtop.sql, ash_wait_chains.sql, asqlmon.sql
- **AWR Analysis:** awr_sqlstats.sql
- **SQL Tuning:** create_sql_baseline.sql, create_sql_patch.sql
- **Lock Analysis:** lock.sql, trans.sql
- **Wait Analysis:** evh.sql, sed.sql
- **Object Info:** tab.sql, ind.sql, seg.sql
- **Space Management:** df.sql, topseg.sql
- **Memory Management:** sga.sql, pga.sql, sgastat.sql
- **And more...**

## Related Files

- **SCRIPTS_CATALOG.txt** - Structured text format (best for grep, used by this script)
- **SCRIPTS_CATALOG.md** - Markdown tables (best for reading on GitHub)
- **SCRIPTS_CATALOG.csv** - CSV format (best for Excel/Google Sheets)
- **SEARCH_GUIDE.md** - Extended usage guide with more examples
- **CLAUDE.md** - Repository guidance for AI assistants

## Contributing

### Adding More Scripts

To add more scripts to the catalog:

1. Edit `SCRIPTS_CATALOG.txt`
2. Follow the existing format:
   ```
   ================================================================================
   SCRIPT: scriptname.sql
   CATEGORY: Category Name
   KEYWORDS: keyword1, keyword2, keyword3
   PURPOSE: What the script does
   SYNTAX: @scriptname <param1> <param2>
   PARAMETERS:
     - param1: Description
     - param2: Description
   EXAMPLES:
     @scriptname example1
     @scriptname example2
   ================================================================================
   ```
3. Test with the search script
4. Update corresponding .md and .csv files

### Reporting Issues

If you find bugs or have suggestions:

1. Check existing documentation
2. Try the troubleshooting section
3. Open an issue on the repository (if applicable)

## Credits

- **TPT Scripts:** Created by Tanel Poder (https://tanelpoder.com)
- **Search Script:** Created for TPT repository organization
- **Catalog:** Compiled from TPT script headers and help.sql

## License

This search tool follows the same license as the TPT scripts repository (Apache License 2.0).

The TPT scripts themselves are:
- Copyright: Tanel Poder
- License: Apache License 2.0
- Website: https://tanelpoder.com
- More info: See LICENSE.txt in repository

## Version History

- **v1.0** - Initial release
  - Script name search
  - Keyword search
  - Category search
  - Purpose search
  - Example search
  - List functionality
  - Color-coded output
  - 50+ scripts cataloged

## See Also

- **TPT Scripts Repository:** https://github.com/tanelpoder/tpt-oracle
- **Tanel Poder's Blog:** https://tanelpoder.com
- **Oracle Database Documentation:** https://docs.oracle.com
- **help.sql:** Built-in help within TPT: `@help <keyword>`

---

**Quick Links:**
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

**Last Updated:** 2026-01-08
