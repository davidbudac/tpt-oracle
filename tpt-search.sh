#!/usr/bin/env bash
################################################################################
# TPT Script Catalog Search Tool
#
# Search through Tanel Poder's TPT scripts catalog with multiple options
#
# Author: Created for TPT Scripts Repository
# Usage: tpt-search.sh [options] <search_term>
################################################################################

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CATALOG="$SCRIPT_DIR/SCRIPTS_CATALOG.txt"

# Colors for output (if terminal supports it)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    MAGENTA='\033[0;35m'
    CYAN='\033[0;36m'
    BOLD='\033[1m'
    NC='\033[0m' # No Color
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    MAGENTA=''
    CYAN=''
    BOLD=''
    NC=''
fi

# Check if catalog exists
if [ ! -f "$CATALOG" ]; then
    echo -e "${RED}Error: Catalog file not found at $CATALOG${NC}"
    exit 1
fi

################################################################################
# Helper Functions
################################################################################

show_help() {
    cat << EOF
${BOLD}TPT Script Catalog Search Tool${NC}

${BOLD}USAGE:${NC}
    $(basename $0) [options] <search_term>

${BOLD}OPTIONS:${NC}
    ${GREEN}-s, --script${NC} <name>        Search by script name (default)
    ${GREEN}-k, --keyword${NC} <term>       Search by keyword
    ${GREEN}-c, --category${NC} <cat>       Search by category
    ${GREEN}-p, --purpose${NC} <text>       Search by purpose/description
    ${GREEN}-e, --example${NC} <text>       Search in examples
    ${GREEN}-l, --list${NC}                 List all scripts
    ${GREEN}-lc, --list-categories${NC}     List all categories
    ${GREEN}-i, --ignore-case${NC}          Case-insensitive search (default)
    ${GREEN}-h, --help${NC}                 Show this help message

${BOLD}EXAMPLES:${NC}
    # Find a specific script
    $(basename $0) snapper.sql
    $(basename $0) -s sqlid

    # Search by keyword
    $(basename $0) -k lock
    $(basename $0) -k "wait chain"
    $(basename $0) --keyword performance

    # Search by category
    $(basename $0) -c "SQL Analysis"
    $(basename $0) --category ash

    # Search by purpose
    $(basename $0) -p "execution plan"

    # Search in examples
    $(basename $0) -e "sysdate-1/24"

    # List all scripts or categories
    $(basename $0) -l
    $(basename $0) --list-categories

${BOLD}TIPS:${NC}
    - Use quotes for multi-word search terms
    - Partial matches are supported
    - Case-insensitive by default
    - Use | in script directory for quick access: alias tpt='$SCRIPT_DIR/$(basename $0)'

EOF
}

list_all_scripts() {
    echo -e "${BOLD}All TPT Scripts in Catalog:${NC}\n"
    grep "^SCRIPT:" "$CATALOG" | sed 's/SCRIPT: /  /' | sort | nl -w2 -s'. '
    echo ""
    local count=$(grep -c "^SCRIPT:" "$CATALOG")
    echo -e "${CYAN}Total: $count scripts${NC}"
}

list_categories() {
    echo -e "${BOLD}All Categories:${NC}\n"
    grep "^CATEGORY:" "$CATALOG" | sed 's/CATEGORY: //' | sort -u | while read cat; do
        local count=$(grep -c "^CATEGORY: $cat" "$CATALOG")
        echo -e "  ${YELLOW}$cat${NC} ($count scripts)"
    done
}

search_exact_script() {
    local script_name="$1"
    local found=0

    # Use awk to extract complete entry
    local result=$(awk -v script="$script_name" '
        /^========/ {
            if (found) {
                print separator
                exit
            }
            separator = $0
            next
        }
        /^SCRIPT:/ {
            if (tolower($0) ~ tolower(script)) {
                found=1
                print $0
                next
            }
        }
        found { print }
    ' "$CATALOG")

    if [ -n "$result" ]; then
        echo -e "${GREEN}Found script:${NC}\n"
        echo "$result" | highlight_output "$script_name"
        return 0
    else
        echo -e "${RED}No script found matching: $script_name${NC}"
        echo -e "\n${YELLOW}Suggestions:${NC}"
        grep -i "^SCRIPT:.*$script_name" "$CATALOG" | head -5 | sed 's/SCRIPT: /  - /'
        return 1
    fi
}

search_by_field() {
    local search_term="$1"
    local field="$2"
    local field_label="$3"

    local matches=$(grep -i "^$field.*$search_term" "$CATALOG" -B 2 -A 12)

    if [ -z "$matches" ]; then
        echo -e "${RED}No scripts found with $field_label matching: $search_term${NC}"
        return 1
    fi

    echo -e "${GREEN}Scripts matching $field_label '$search_term':${NC}\n"

    # Extract and display each matching entry
    echo "$matches" | awk -v field="$field" '
        /^SCRIPT:/ {
            if (script != "") print separator
            script = $0
            separator = "----------------------------------------"
            print script
            next
        }
        /^CATEGORY:|^KEYWORDS:|^PURPOSE:|^SYNTAX:|^EXAMPLES:/ { print; next }
        /^  / { print; next }
    '

    # Count matches
    local count=$(echo "$matches" | grep -c "^SCRIPT:")
    echo -e "\n${CYAN}Found $count matching script(s)${NC}"
}

search_in_examples() {
    local search_term="$1"

    echo -e "${GREEN}Scripts with examples containing '$search_term':${NC}\n"

    # Find scripts where examples contain the search term
    awk -v term="$search_term" '
        BEGIN { IGNORECASE=1; found=0 }
        /^========/ {
            if (found && script != "") {
                print script
                print category
                print syntax
                print examples
                print "----------------------------------------"
            }
            script = ""
            category = ""
            syntax = ""
            examples = ""
            found = 0
            next
        }
        /^SCRIPT:/ { script = $0; next }
        /^CATEGORY:/ { category = $0; next }
        /^SYNTAX:/ { syntax = $0; next }
        /^EXAMPLES:/ {
            in_examples = 1
            examples = $0
            next
        }
        in_examples && /^[A-Z]+:/ { in_examples = 0 }
        in_examples {
            examples = examples "\n" $0
            if ($0 ~ term) found = 1
        }
    ' "$CATALOG"
}

highlight_output() {
    local term="$1"
    if [ -t 1 ] && [ -n "$term" ]; then
        # Highlight search term in output
        sed "s/\($term\)/${YELLOW}\1${NC}/gi"
    else
        cat
    fi
}

################################################################################
# Main Script Logic
################################################################################

# Default mode is script search
MODE="script"
SEARCH_TERM=""

# Parse command line arguments
while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help)
            show_help
            exit 0
            ;;
        -l|--list)
            list_all_scripts
            exit 0
            ;;
        -lc|--list-categories)
            list_categories
            exit 0
            ;;
        -s|--script)
            MODE="script"
            shift
            SEARCH_TERM="$1"
            ;;
        -k|--keyword)
            MODE="keyword"
            shift
            SEARCH_TERM="$1"
            ;;
        -c|--category)
            MODE="category"
            shift
            SEARCH_TERM="$1"
            ;;
        -p|--purpose)
            MODE="purpose"
            shift
            SEARCH_TERM="$1"
            ;;
        -e|--example)
            MODE="example"
            shift
            SEARCH_TERM="$1"
            ;;
        -i|--ignore-case)
            # Already default, but accept flag
            shift
            continue
            ;;
        -*)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
        *)
            # No flag specified, treat as script name search
            SEARCH_TERM="$1"
            ;;
    esac
    shift
done

# Check if search term provided
if [ -z "$SEARCH_TERM" ]; then
    echo -e "${RED}Error: No search term provided${NC}"
    echo ""
    show_help
    exit 1
fi

# Execute search based on mode
case "$MODE" in
    script)
        search_exact_script "$SEARCH_TERM"
        ;;
    keyword)
        search_by_field "$SEARCH_TERM" "KEYWORDS:" "keywords"
        ;;
    category)
        search_by_field "$SEARCH_TERM" "CATEGORY:" "category"
        ;;
    purpose)
        search_by_field "$SEARCH_TERM" "PURPOSE:" "purpose"
        ;;
    example)
        search_in_examples "$SEARCH_TERM"
        ;;
    *)
        echo -e "${RED}Unknown mode: $MODE${NC}"
        exit 1
        ;;
esac

exit 0
