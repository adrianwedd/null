#!/usr/bin/env python3

import re
import datetime
import os
import argparse
import base64
import sys

# Directory for storing log files
ARCHIVE_DIR = "archive"

def ensure_directory_exists(dir_path):
    """Ensures the specified directory exists."""
    os.makedirs(dir_path, exist_ok=True)

def get_log_file_path_base():
    """Constructs the base log file path (without extension) based on the current date."""
    current_date = datetime.date.today()
    return os.path.join(ARCHIVE_DIR, f"THOUGHTLOG_{current_date.isoformat()}")

def log_thoughts(text_to_log, log_file_path_base, encrypt_mode, redact_mode): # Modified for V3
    """
    Finds thought blocks in the input text, logs them (raw/encrypted) to a file,
    and constructs a simulated STDOUT string with optional redaction.
    Returns a tuple: (number_of_thoughts_logged, simulated_stdout_string)
    """
    thoughts_found_for_logging = 0

    file_extension = ".enc" if encrypt_mode else ".md"
    log_file_path = log_file_path_base + file_extension

    # For simulated STDOUT
    stdout_parts = []

    # Split the text by thought blocks, keeping the delimiters (thought blocks themselves)
    # This allows us to process text and thoughts in order
    parts = re.split(r"(<think>.*?</think>)", text_to_log, flags=re.DOTALL)

    for part in parts:
        if not part: # Skip empty strings that can result from split
            continue

        is_thought_block = re.fullmatch(r"<think>.*?</think>", part, flags=re.DOTALL)

        if is_thought_block:
            # Extract raw thought text for logging
            match = re.search(r"<think>(.*?)</think>", part, flags=re.DOTALL)
            if match: # Should always match if is_thought_block is true
                raw_thought_text = match.group(1).strip()

                if raw_thought_text: # Log only if there's content
                    thoughts_found_for_logging += 1
                    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
                    source = "JULES_CORE"

                    thought_text_to_log_file = raw_thought_text
                    if encrypt_mode:
                        thought_text_to_log_file = base64.b64encode(raw_thought_text.encode('utf-8')).decode('utf-8')

                    log_entry = f"{timestamp} - {source}:\n---\n{thought_text_to_log_file}\n---\n\n"
                    try:
                        with open(log_file_path, 'a', encoding='utf-8') as f:
                            f.write(log_entry)
                    except IOError as e:
                        print(f"Error: Could not write to log file {log_file_path}. Exception: {e}", file=sys.stderr)
                        # In case of write error, we might not want to proceed or affect stdout simulation
                        # For now, we'll let stdout simulation continue but flag that logging might be incomplete.
                        thoughts_found_for_logging = -1 # Indicate error

            # Handle STDOUT part
            if redact_mode:
                stdout_parts.append(re.sub(r"<think>(.*?)</think>", r"<think>[redacted]</think>", part, flags=re.DOTALL))
            else:
                stdout_parts.append(part)
        else: # It's a non-thought part
            stdout_parts.append(part)

    simulated_stdout_string = "".join(stdout_parts)
    return thoughts_found_for_logging, simulated_stdout_string


def main():
    ensure_directory_exists(ARCHIVE_DIR)

    parser = argparse.ArgumentParser(
        description="Log thoughts from an input string to a dated file and simulate STDOUT with redaction."
    )
    parser.add_argument("input_string", type=str, help="The input string containing <think>...</think> blocks.")
    parser.add_argument("--encrypt", action='store_true', help="Enable encryption mode (Base64 encode thoughts in log file).")
    parser.add_argument("--redact-think", action='store_true', help="Redact thought content in the simulated STDOUT.") # Added for V3

    args = parser.parse_args()

    log_file_path_base = get_log_file_path_base()

    num_logged, simulated_stdout = log_thoughts(
        args.input_string,
        log_file_path_base,
        args.encrypt,
        args.redact_think  # Added for V3
    )

    # Print simulated STDOUT to actual stdout
    print(simulated_stdout, end='') # end='' if simulated_stdout might have its own trailing newline

    # Determine full log_file_path for the stderr message
    final_log_file_path = log_file_path_base + ('.enc' if args.encrypt else '.md')

    if num_logged > 0:
        print(f"\n[{num_logged} thought(s) processed. Logged {'(encrypted)' if args.encrypt else ''} to {final_log_file_path}]", file=sys.stderr)
    elif num_logged == 0: # No thoughts found or logged
        message = f"\n[No new thoughts found in input to log. Log file is {final_log_file_path}]"
        if not os.path.exists(final_log_file_path):
            message = f"\n[No thoughts found in input. Log file {final_log_file_path} was not created/appended to.]"
        print(message, file=sys.stderr)
    # If num_logged is -1 (error), an error message was already printed by log_thoughts

if __name__ == "__main__":
    main()
