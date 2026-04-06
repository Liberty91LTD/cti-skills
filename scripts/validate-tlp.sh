#!/bin/bash
# Hook script: validates that files being exported have a TLP marking
# Used as a PreToolUse hook on export operations

FILE="$1"

if [ -z "$FILE" ]; then
    exit 0
fi

if [ -f "$FILE" ]; then
    if grep -q "^tlp:" "$FILE" || grep -q "\"tlp\":" "$FILE"; then
        exit 0
    else
        echo "ERROR: File $FILE has no TLP marking. All exports must include a TLP designation."
        echo "Add 'tlp: CLEAR|GREEN|AMBER|AMBER+STRICT|RED' to the file frontmatter."
        exit 1
    fi
fi

exit 0
