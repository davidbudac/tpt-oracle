#!/bin/bash
# Extract documentation from TPT scripts

echo "Script|First_Line_Doc"
echo "------|---------------"

# Root directory scripts
for file in $(find . -maxdepth 1 -name "*.sql" -type f | sort); do
    basename_file=$(basename "$file")
    doc=$(head -10 "$file" 2>/dev/null | grep -i "prompt\|--.*purpose\|--.*usage" | head -1 | sed 's/^[Pp][Rr][Oo][Mm][Pp][Tt][ ]*//' | sed 's/^-- *//')
    if [ -n "$doc" ]; then
        echo "$basename_file|$doc"
    else
        echo "$basename_file|No documentation found"
    fi
done

# ASH scripts
for file in $(find ash/ -name "*.sql" -type f 2>/dev/null | sort); do
    doc=$(head -10 "$file" 2>/dev/null | grep -i "prompt\|--.*purpose\|--.*usage" | head -1 | sed 's/^[Pp][Rr][Oo][Mm][Pp][Tt][ ]*//' | sed 's/^-- *//')
    if [ -n "$doc" ]; then
        echo "$file|$doc"
    else
        echo "$file|No documentation found"
    fi
done

# AWR scripts
for file in $(find awr/ -name "*.sql" -type f 2>/dev/null | sort); do
    doc=$(head -10 "$file" 2>/dev/null | grep -i "prompt\|--.*purpose\|--.*usage" | head -1 | sed 's/^[Pp][Rr][Oo][Mm][Pp][Tt][ ]*//' | sed 's/^-- *//')
    if [ -n "$doc" ]; then
        echo "$file|$doc"
    else
        echo "$file|No documentation found"
    fi
done
