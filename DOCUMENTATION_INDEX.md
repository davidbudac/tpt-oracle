# TPT Scripts Documentation Index

**Complete guide to all TPT documentation files**

---

## 📚 Main Documentation

### Core References

| File | Purpose | When to Use |
|------|---------|-------------|
| **README_TPT_SEARCH.md** | Complete search tool documentation | Learning the search tool |
| **SEARCH_GUIDE.md** | Extended usage guide with examples | Detailed search examples |
| **CLAUDE.md** | AI assistant guidance for repository | AI context about TPT |

---

## 🔍 Script Catalogs

### All Formats Available

| File | Format | Best For | Scripts |
|------|--------|----------|---------|
| **SCRIPTS_CATALOG.txt** | Structured text | Command-line grep | 135+ |
| **SCRIPTS_CATALOG.md** | Markdown tables | Reading in browser/GitHub | 135+ |
| **SCRIPTS_CATALOG.csv** | Pipe-delimited CSV | Excel/Google Sheets | 135+ |

**Total Scripts Documented:** 135+ (expanded from initial 50)

### How to Use Each Format

#### SCRIPTS_CATALOG.txt (Best for grep)
```bash
# Find lock-related scripts
grep -i "KEYWORDS.*lock" SCRIPTS_CATALOG.txt

# Find script with full details
grep -A 15 "^SCRIPT: snapper" SCRIPTS_CATALOG.txt

# Find all SQL tuning scripts
grep "CATEGORY:.*SQL Tuning" SCRIPTS_CATALOG.txt
```

#### SCRIPTS_CATALOG.md (Best for reading)
- Open in GitHub (auto-renders)
- View in VS Code with markdown preview
- Use browser search (Ctrl+F/Cmd+F)
- Organized by category with tables

#### SCRIPTS_CATALOG.csv (Best for analysis)
- Import into Excel (delimiter: `|`)
- Import into Google Sheets
- Sort, filter, create custom views
- Command line: `column -t -s'|' SCRIPTS_CATALOG.csv | less -S`

---

## 🎯 Quick Reference Cards

### General Quick Reference

| File | Coverage | Pages |
|------|----------|-------|
| **TPT_QUICK_REF.md** | All essentials | 1-page |

**Contains:**
- Setup instructions
- Common searches
- Top 10 most used scripts
- All categories
- Emergency quick checks
- Typical workflows

**Print this and keep at your desk!**

### Category-Specific Quick References

| File | Category | Focus |
|------|----------|-------|
| **QUICKREF_ASH_ANALYSIS.md** | ASH Analysis | Active Session History troubleshooting |
| **QUICKREF_SQL_TUNING.md** | SQL Tuning | SQL optimization and plan management |
| **QUICKREF_PERFORMANCE_MONITORING.md** | Performance | Snapper, profiling, real-time monitoring |
| **QUICKREF_MEMORY_SPACE.md** | Memory & Space | SGA, PGA, tablespace management |

---

## 📖 Quick Reference Details

### 1. TPT_QUICK_REF.md - General Reference

**Use this when:** You need a quick lookup for any TPT script

**Includes:**
- Setup (alias creation)
- Basic usage table
- Common searches by scenario
- Top 10 most used scripts with usage
- All categories list
- Typical workflows
- Emergency diagnostics
- File locations

**Example scenarios:**
- Performance issues
- SQL problems
- Session issues
- Locks & blocking
- Memory issues
- Space issues
- Wait events

---

### 2. QUICKREF_ASH_ANALYSIS.md - ASH Deep Dive

**Use this when:** Working with Active Session History data

**Includes:**
- What ASH is and why use it
- Essential ASH scripts table
- Quick start examples for each script
- Time range shortcuts
- Common filters
- 5 common troubleshooting workflows
- Pro tips
- ASH vs AWR vs Snapper comparison

**Workflows covered:**
1. General performance issue
2. Lock/blocking investigation
3. Slow SQL investigation
4. I/O performance issue
5. Finding performance spikes

**Key scripts documented:**
- ash/ashtop.sql
- ash/ash_wait_chains.sql
- ash/asqlmon.sql
- ash/ashpeak.sql
- ash/ash_index_helper.sql
- ash/event_hist.sql

---

### 3. QUICKREF_SQL_TUNING.md - SQL Optimization

**Use this when:** Tuning SQL statements or managing execution plans

**Includes:**
- 4-step tuning workflow (Identify → Analyze → Fix → Verify)
- Scripts for each phase
- How to create patches, profiles, baselines
- Common tuning scenarios with step-by-step instructions
- Hint reference
- Execution plan interpretation guide
- SQL tuning checklist

**Fix methods covered:**
- SQL Patches (inject hints)
- SQL Profiles (guide optimizer)
- SQL Plan Baselines (lock plans)
- Statistics gathering
- Index creation

**6 common scenarios:**
- Full table scan (need index)
- Wrong index being used
- SQL needs parallel execution
- Plan changed and now slow
- Join order is wrong
- Cursor sharing issues

---

### 4. QUICKREF_PERFORMANCE_MONITORING.md - Live Monitoring

**Use this when:** Profiling live systems or investigating performance

**Includes:**
- The "Big Three" monitoring tools comparison
- Snapper comprehensive guide
- Current activity monitoring
- Memory monitoring (SGA/PGA)
- Advanced profiling (latch, mutex, wait, buffer)
- 5 complete monitoring workflows
- Monitoring cheat sheets
- Key metrics reference

**Tools covered:**
- Snapper (the Swiss Army knife)
- ASH (recent activity)
- AWR (historical)
- Session monitoring
- System monitoring

**5 workflows:**
1. General performance check
2. Slow session investigation
3. System performance issue
4. CPU saturation
5. I/O performance issue

---

### 5. QUICKREF_MEMORY_SPACE.md - Resource Management

**Use this when:** Managing memory or storage

**Includes:**
- Memory management (SGA/PGA)
- Space management (tablespaces/segments)
- Quick checks table
- Troubleshooting guides
- Best practices
- Emergency actions
- Monitoring scripts
- Key thresholds

**Covers:**
- SGA components and analysis
- PGA usage and workareas
- Session memory
- Tablespace space checks
- Segment space analysis
- LOB space
- Object-level I/O

**Troubleshooting:**
- Out of memory errors
- Shared pool exhaustion
- PGA/TEMP issues
- Tablespace almost full
- Table growing too fast
- Space hog identification

---

## 🔧 Search Tool

### tpt-search.sh

**Location:** `/path/to/tpt-oracle/tpt-search.sh`

**Features:**
- Search by script name, keyword, category, purpose, or examples
- List all scripts or categories
- Color-coded output
- Case-insensitive
- Partial matching

**Quick setup:**
```bash
# Add to ~/.bashrc or ~/.zshrc
alias tpt='/path/to/tpt-oracle/tpt-search.sh'
```

**Usage:**
```bash
tpt snapper.sql               # Find specific script
tpt -k lock                   # Search by keyword
tpt -c "SQL Analysis"         # Search by category
tpt -l                        # List all scripts
tpt -lc                       # List categories
```

---

## 📂 File Organization

```
tpt-oracle/
├── Documentation/
│   ├── README_TPT_SEARCH.md              # Search tool README
│   ├── SEARCH_GUIDE.md                   # Extended guide
│   ├── CLAUDE.md                         # AI guidance
│   ├── DOCUMENTATION_INDEX.md            # This file
│   │
│   ├── Catalogs/
│   │   ├── SCRIPTS_CATALOG.txt           # Greppable
│   │   ├── SCRIPTS_CATALOG.md            # Markdown
│   │   └── SCRIPTS_CATALOG.csv           # Spreadsheet
│   │
│   └── Quick References/
│       ├── TPT_QUICK_REF.md              # General
│       ├── QUICKREF_ASH_ANALYSIS.md      # ASH
│       ├── QUICKREF_SQL_TUNING.md        # SQL Tuning
│       ├── QUICKREF_PERFORMANCE_MONITORING.md  # Performance
│       └── QUICKREF_MEMORY_SPACE.md      # Memory/Space
│
├── Scripts/ (700+ .sql files)
└── tpt-search.sh                         # Search tool
```

---

## 🚀 Getting Started Guide

### For New Users

1. **Start with:** TPT_QUICK_REF.md
   - Get overview of most important scripts
   - Learn basic usage patterns

2. **Set up search:**
   ```bash
   alias tpt='/path/to/tpt-oracle/tpt-search.sh'
   ```

3. **Try searches:**
   ```bash
   tpt -l              # See all scripts
   tpt snapper.sql     # Learn about Snapper
   tpt -k lock         # Find lock scripts
   ```

4. **Deep dive:** Read category-specific quick references for your needs
   - Performance issues? → QUICKREF_PERFORMANCE_MONITORING.md
   - Slow SQL? → QUICKREF_SQL_TUNING.md
   - ASH analysis? → QUICKREF_ASH_ANALYSIS.md
   - Memory/space? → QUICKREF_MEMORY_SPACE.md

### For Experienced Users

1. **Quick lookup:** Use `tpt` command for instant script reference
2. **Grep catalog:** `grep` SCRIPTS_CATALOG.txt for detailed info
3. **Reference cards:** Keep quick references handy for specific domains
4. **Contribute:** Add more scripts to catalog as you discover them

---

## 📊 Catalog Statistics

- **Total Scripts Documented:** 135+
- **Categories:** 25+
- **Coverage:** ~20% of all 700+ TPT scripts
- **Focus:** Most important and commonly used scripts

### Most Comprehensive Categories

1. **Object Information** - 20+ scripts
2. **SQL Analysis** - 15+ scripts
3. **ASH Analysis** - 10+ scripts
4. **Session Monitoring** - 10+ scripts
5. **Memory Management** - 10+ scripts
6. **System Configuration** - 10+ scripts
7. **AWR Analysis** - 8+ scripts
8. **SQL Tuning** - 8+ scripts
9. **Execution Plans** - 8+ scripts

---

## 💡 Tips for Using Documentation

### 1. Print Quick References

Print and laminate these for desk reference:
- TPT_QUICK_REF.md
- Your most-used category quick reference

### 2. Create Bookmarks

Bookmark in your browser:
- SCRIPTS_CATALOG.md (for searchable web view)
- Category quick references

### 3. Keep Local Copies

```bash
# Create docs directory
mkdir -p ~/oracle_docs

# Copy quick references
cp QUICKREF_*.md ~/oracle_docs/
cp TPT_QUICK_REF.md ~/oracle_docs/
```

### 4. Integration with Tools

```bash
# Create function to open docs
oracle_docs() {
    case "$1" in
        ash) less ~/oracle_docs/QUICKREF_ASH_ANALYSIS.md ;;
        sql) less ~/oracle_docs/QUICKREF_SQL_TUNING.md ;;
        perf) less ~/oracle_docs/QUICKREF_PERFORMANCE_MONITORING.md ;;
        mem) less ~/oracle_docs/QUICKREF_MEMORY_SPACE.md ;;
        *) less ~/oracle_docs/TPT_QUICK_REF.md ;;
    esac
}
```

### 5. Share with Team

- Email quick references to team members
- Add to internal wiki
- Include in onboarding documentation

---

## 🔄 Keeping Documentation Updated

### When New Scripts Added

1. Update SCRIPTS_CATALOG.txt (use existing format)
2. Run tpt-search.sh to verify
3. Regenerate CSV/MD if needed
4. Update relevant quick references

### Format for New Entries

```
================================================================================
SCRIPT: script_name.sql
CATEGORY: Category Name
KEYWORDS: keyword1, keyword2, keyword3
PURPOSE: What the script does
SYNTAX: @script_name <param1> <param2>
PARAMETERS:
  - param1: Description
  - param2: Description
EXAMPLES:
  @script_name example1
  @script_name example2
================================================================================
```

---

## 🎓 Learning Path

### Week 1: Basics
- Read: TPT_QUICK_REF.md
- Practice: Top 10 scripts
- Learn: tpt search tool

### Week 2: Performance
- Read: QUICKREF_PERFORMANCE_MONITORING.md
- Master: Snapper, ASH basics
- Practice: Live monitoring scenarios

### Week 3: SQL Tuning
- Read: QUICKREF_SQL_TUNING.md
- Learn: Execution plans, hints
- Practice: SQL tuning workflows

### Week 4: ASH Deep Dive
- Read: QUICKREF_ASH_ANALYSIS.md
- Master: All ASH scripts
- Practice: Complex troubleshooting

### Week 5: Advanced
- Read: QUICKREF_MEMORY_SPACE.md
- Explore: All catalogs
- Master: Category-specific scripts

---

## 📞 Quick Help

```bash
# Lost? Start here:
tpt -h                        # Search tool help
cat TPT_QUICK_REF.md         # General reference

# Find scripts:
tpt -l                        # List all
tpt -lc                       # List categories
tpt -k <keyword>              # Search

# Get script details:
tpt <script_name>             # Full info

# Category help:
cat QUICKREF_ASH_ANALYSIS.md          # ASH help
cat QUICKREF_SQL_TUNING.md            # SQL help
cat QUICKREF_PERFORMANCE_MONITORING.md # Performance help
cat QUICKREF_MEMORY_SPACE.md          # Memory/Space help
```

---

## 🎯 Most Useful Documents by Scenario

| Scenario | Document |
|----------|----------|
| **General lookup** | TPT_QUICK_REF.md |
| **Performance issue** | QUICKREF_PERFORMANCE_MONITORING.md |
| **Slow SQL** | QUICKREF_SQL_TUNING.md |
| **Blocking/locks** | QUICKREF_ASH_ANALYSIS.md |
| **Out of space** | QUICKREF_MEMORY_SPACE.md |
| **Out of memory** | QUICKREF_MEMORY_SPACE.md |
| **Learning** | README_TPT_SEARCH.md |
| **Advanced search** | SEARCH_GUIDE.md |
| **Complete reference** | SCRIPTS_CATALOG.md |

---

**Documentation Version:** 1.0
**Last Updated:** 2026-01-08
**Total Documentation Files:** 11
**Total Scripts Cataloged:** 135+

---

*Complete Documentation Index - TPT Scripts Collection - v1.0*
