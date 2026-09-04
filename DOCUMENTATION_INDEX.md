# TPT Documentation Index

This repository contains two different documentation layers:

- Human-oriented quick references and guides for common TPT workflows
- Catalog and metadata artifacts that help you search the script library

The important distinction is scope:

- `tpt-search.sh` searches the curated reference catalog in `SCRIPTS_CATALOG.txt`
- The repository itself contains far more SQL scripts than that curated CLI catalog
- `scripts_data.js` is a broader machine-readable metadata export than the CLI catalog

## Start Here

| If You Want To... | Open This |
|-------------------|-----------|
| Understand the repository and basic setup | [README.md](README.md) |
| Find the right script quickly | [TPT_QUICK_REF.md](TPT_QUICK_REF.md) |
| Learn the search tool properly | [README_TPT_SEARCH.md](README_TPT_SEARCH.md) |
| See task-oriented search examples | [SEARCH_GUIDE.md](SEARCH_GUIDE.md) |
| Work with ASH | [QUICKREF_ASH_ANALYSIS.md](QUICKREF_ASH_ANALYSIS.md) |
| Tune SQL | [QUICKREF_SQL_TUNING.md](QUICKREF_SQL_TUNING.md) |
| Monitor live performance | [QUICKREF_PERFORMANCE_MONITORING.md](QUICKREF_PERFORMANCE_MONITORING.md) |
| Check memory or space | [QUICKREF_MEMORY_SPACE.md](QUICKREF_MEMORY_SPACE.md) |

## Search and Catalog Artifacts

| File | Purpose | Scope |
|------|---------|-------|
| [tpt-search.sh](tpt-search.sh) | CLI search tool | Searches the curated text catalog |
| [SCRIPTS_CATALOG.txt](SCRIPTS_CATALOG.txt) | Canonical catalog for `tpt-search.sh` | Documented subset used by the CLI |
| [SCRIPTS_CATALOG.csv](SCRIPTS_CATALOG.csv) | Spreadsheet-friendly export | Companion export for the curated catalog |
| [SCRIPTS_CATALOG.md](SCRIPTS_CATALOG.md) | Browser-friendly catalog view | Large browsable catalog artifact |
| [scripts_data.js](scripts_data.js) | Machine-readable metadata | Broader metadata export than the CLI catalog |

## Quick References

| File | Focus |
|------|-------|
| [TPT_QUICK_REF.md](TPT_QUICK_REF.md) | Short operator cheat sheet |
| [QUICKREF_ASH_ANALYSIS.md](QUICKREF_ASH_ANALYSIS.md) | ASH and wait analysis workflows |
| [QUICKREF_SQL_TUNING.md](QUICKREF_SQL_TUNING.md) | SQL tuning and plan management |
| [QUICKREF_PERFORMANCE_MONITORING.md](QUICKREF_PERFORMANCE_MONITORING.md) | Live performance triage |
| [QUICKREF_MEMORY_SPACE.md](QUICKREF_MEMORY_SPACE.md) | SGA, PGA, tablespace, and segment checks |

## Actual Repository Layout

This is the structure that exists in the repository today:

```text
tpt-oracle/
├── README.md
├── DOCUMENTATION_INDEX.md
├── README_TPT_SEARCH.md
├── SEARCH_GUIDE.md
├── TPT_QUICK_REF.md
├── QUICKREF_*.md
├── SCRIPTS_CATALOG.*
├── scripts_data.js
├── tpt-search.sh
├── ash/
├── awr/
├── setup/
├── tools/
└── *.sql
```

## Recommended Reading Order

### New to TPT

1. [README.md](README.md)
2. [TPT_QUICK_REF.md](TPT_QUICK_REF.md)
3. [README_TPT_SEARCH.md](README_TPT_SEARCH.md)
4. One category quick reference relevant to your task

### Already Familiar With TPT

1. Use `@help <keyword>` inside SQL*Plus
2. Use `tpt-search.sh` when you want shell-side lookup
3. Jump straight to the category quick reference for the problem at hand

## Choosing the Right Lookup Method

| Situation | Best Tool |
|-----------|-----------|
| You are already inside SQL*Plus | `@help <keyword>` |
| You want shell-side lookup before connecting | `tpt-search.sh` |
| You want a compact cheat sheet | `TPT_QUICK_REF.md` |
| You want step-by-step workflows | `QUICKREF_*.md` |
| You want broad inventory-style browsing | `SCRIPTS_CATALOG.md` |

## Maintenance Notes

- Do not assume all catalog artifacts have identical coverage
- The CLI search experience is defined by [SCRIPTS_CATALOG.txt](SCRIPTS_CATALOG.txt)
- If you update search-tool documentation, keep it aligned with `tpt-search.sh`
- If you update curated catalog entries, regenerate [SCRIPTS_CATALOG.csv](SCRIPTS_CATALOG.csv) with `python3 tools/generate_search_catalog_csv.py`
