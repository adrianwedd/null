#!/usr/bin/env python3

import hashlib
import sys
import os

def calculate_sha256(filepath):
    """Calculates the SHA-256 hash of a file's content."""
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
            sha256_hash = hashlib.sha256(content).hexdigest()
        return sha256_hash
    except FileNotFoundError:
        print(f"ERROR: File not found: {filepath}", file=sys.stderr)
        sys.exit(2)
    except IOError:
        print(f"ERROR: Could not read file: {filepath}", file=sys.stderr)
        sys.exit(3)

def main():
    # Determine the root directory of the repository assuming the script is in scripts/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir) # This should be /app

    preprompt_file = os.path.join(root_dir, "PREPROMPT.md")
    hash_file_path = os.path.join(root_dir, "archive", "PREPROMPT_HASH.txt")

    # Read the reference hash
    try:
        with open(hash_file_path, 'r') as hf:
            line = hf.readline().strip()
            if not line:
                print(f"ERROR: Reference hash file is empty: {hash_file_path}", file=sys.stderr)
                sys.exit(4)
            # Expected format: "hash  filename"
            parts = line.split('  ', 1)
            if len(parts) < 1 or not parts[0]: # Check if hash part is empty or not present
                print(f"ERROR: Invalid format in hash file: {hash_file_path}. Expected 'hash  filename'. Got '{line}'", file=sys.stderr)
                sys.exit(5)
            reference_hash = parts[0]
    except FileNotFoundError:
        print(f"ERROR: Reference hash file not found: {hash_file_path}", file=sys.stderr)
        sys.exit(6)
    except IOError:
        print(f"ERROR: Could not read reference hash file: {hash_file_path}", file=sys.stderr)
        sys.exit(7)

    # Calculate the hash of the current PREPROMPT.md
    current_hash = calculate_sha256(preprompt_file)
    if current_hash is None: # calculate_sha256 handles its own exit for file errors
        sys.exit(8) # Should not happen if calculate_sha256 exits

    # Compare the hashes
    if current_hash == reference_hash:
        print("SUCCESS: PREPROMPT.md content is consistent with the reference hash.")
        sys.exit(0)
    else:
        print("ERROR: PREPROMPT.md content has changed! Hash mismatch.", file=sys.stderr)
        print(f"  Reference hash: {reference_hash}", file=sys.stderr)
        print(f"  Current hash:   {current_hash}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
