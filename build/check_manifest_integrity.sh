#!/bin/bash
# Script to check repository integrity against the GENESIS_MANIFEST.md

MANIFEST_FILE="prompts/GENESIS_MANIFEST.md"
PASSED=true

if [ ! -f "$MANIFEST_FILE" ]; then
    echo "ERROR: Genesis Manifest file not found at $MANIFEST_FILE"
    PASSED=false
else
    echo "Reading expected files from $MANIFEST_FILE..."
    # Extract lines between the triple backticks, then extract the file paths
    EXPECTED_FILES=$(sed -n '/```/,/```/{ /100644 blob/p; }' "$MANIFEST_FILE" | awk -F'\t' '{print $2}' | sort)

    if [ -z "$EXPECTED_FILES" ]; then
        echo "ERROR: Could not parse expected files from $MANIFEST_FILE, or manifest is empty/corrupt."
        PASSED=false
    else
        echo "Getting current tracked files from git..."
        CURRENT_FILES=$(git ls-files | sort)

        echo ""
        echo "Expected files (from ):"
        echo "$EXPECTED_FILES"
        echo ""
        echo "Current tracked files (from git ls-files):"
        echo "$CURRENT_FILES"
        echo ""

        MISSING_FILES_COUNT=0
        echo "Checking for missing files (files in manifest but not in current repo state)..."
        for expected_file in $EXPECTED_FILES; do
            if ! echo "$CURRENT_FILES" | grep -qx "$expected_file"; then
                echo "Integrity check FAILED: Manifest file '$expected_file' is MISSING from current repository state."
                MISSING_FILES_COUNT=$((MISSING_FILES_COUNT + 1))
                PASSED=false
            fi
        done

        if [ "$MISSING_FILES_COUNT" -gt 0 ]; then
            echo "Total missing files: $MISSING_FILES_COUNT"
        fi
    fi
fi

if [ "$PASSED" = true ]; then
    echo "All files listed in $MANIFEST_FILE are present in the current repository."
    echo "Integrity check passed (basic check for deletions)."
else
    echo "Integrity check FAILED."
fi
