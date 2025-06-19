#!/bin/bash
# Script to rehydrate the repository to its Genesis state (v0.0.1-genesis-corrected).

# Refined Safety Guard: Check for existing files/dirs other than .git and the build directory itself
# This assumes the script is run from the intended repository root.
FOUND_ITEMS=$(ls -A | grep -v -E '^\.git$|^build$' | wc -l)
if [ "$FOUND_ITEMS" -gt 0 ]; then
    echo "ERROR: Current directory is not empty (besides .git and build/). Contains:"
    ls -A | grep -v -E '^\.git$|^build$'
    echo "Rehydration aborted to prevent data loss."
    echo "Please run this script in an empty directory."
    # Removed exit 1
else
    echo "Safety check passed. Proceeding with rehydration..."
    echo "Rehydrating repository to Genesis state (v0.0.1-genesis-corrected)..."

    # Create Directories
    echo "Creating directories..."
    mkdir -p src tests prompts build archive

    # Create .gitkeep Files
    echo "Creating .gitkeep files..."
    touch src/.gitkeep
    touch tests/.gitkeep
    touch prompts/.gitkeep
    touch build/.gitkeep # This script is in build/, so build/ will exist.
    touch archive/.gitkeep

    # Create .gitignore File
    echo "Creating .gitignore..."
    printf "archive/**\n!archive/.gitkeep\n\n# Ignore any future prompt archive markdown files in any location\n*_ARCHIVE*.md\n" > .gitignore

    echo ""
    echo "Repository rehydrated to Genesis state (v0.0.1-genesis-corrected)."
    echo "To version this state, run the following commands in this directory:"
    echo "  git init"
    echo "  git add ."
    echo "  git commit -m \"feat: Initial repository structure from rehydration (v0.0.1-genesis-corrected)\""
    echo "  git tag v0.0.1-genesis-rehydrated"
    echo ""
    echo "To verify against the original corrected genesis commit (e.g., 9a43eb6...):"
    echo "  # First, ensure your rehydrated repo is committed and HEAD points to that commit."
    echo "  # Then, in another clone or detached worktree of the main Jules repo:"
    echo "  git ls-tree -r --name-only 9a43eb6ffc41d7f1dc9bcb57aff7edf817b5446c | sort > /tmp/expected_genesis_files.txt"
    echo "  # Back in your rehydrated repo:"
    echo "  git ls-files | sort > /tmp/current_rehydrated_files.txt"
    echo "  diff /tmp/expected_genesis_files.txt /tmp/current_rehydrated_files.txt && echo 'Verification successful!'"
    echo "  rm /tmp/expected_genesis_files.txt /tmp/current_rehydrated_files.txt"
fi
