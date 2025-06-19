#!/usr/bin/env python3

import unittest
import subprocess
import os
import datetime
import base64
import re
import shutil
import sys

# Constants
ARCHIVE_DIR = "archive"
# Assuming the test script is run from the repository root,
# or that the paths are relative to the repo root.
LOGGER_SCRIPT = os.path.join("tools", "thought_logger.py")

class TestThoughtLogger(unittest.TestCase):

    def setUp(self):
        """Clean and recreate the archive directory before each test."""
        if os.path.exists(ARCHIVE_DIR):
            shutil.rmtree(ARCHIVE_DIR)
        os.makedirs(ARCHIVE_DIR, exist_ok=True)

    def tearDown(self):
        """Clean up the archive directory after each test."""
        if os.path.exists(ARCHIVE_DIR):
            shutil.rmtree(ARCHIVE_DIR)

    def _run_logger(self, input_str, options=None):
        """Helper method to run the logger script."""
        cmd = [sys.executable, LOGGER_SCRIPT] + (options or []) + [input_str]
        # Using check=False to inspect stderr and stdout even on non-zero exit codes
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return result

    def _read_log_file(self, filename_part_with_date_and_ext):
        """Helper method to read a log file from the archive directory."""
        full_path = os.path.join(ARCHIVE_DIR, filename_part_with_date_and_ext)
        if not os.path.exists(full_path):
            return None
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError:
            return None # Or raise an error

    def _get_expected_log_filename(self, encrypted=False):
        """Generates the expected log filename for today."""
        date_str = datetime.date.today().isoformat()
        ext = ".enc" if encrypted else ".md"
        return f"THOUGHTLOG_{date_str}{ext}"

    def test_plain_logging_single_thought(self):
        input_str = "Hello <think>thought one</think> world"
        result = self._run_logger(input_str)

        self.assertEqual(result.returncode, 0, f"Script exited with error: {result.stderr}")
        self.assertEqual(result.stdout.strip(), "Hello <think>thought one</think> world")

        log_filename = self._get_expected_log_filename()
        log_content = self._read_log_file(log_filename)

        self.assertIsNotNone(log_content, f"Log file {log_filename} not found.")
        self.assertRegex(log_content, r"JULES_CORE:\n---\nthought one\n---")
        self.assertRegex(log_content, r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+([+-]\d{2}:\d{2}|Z) - JULES_CORE:")

    def test_encrypted_logging(self):
        input_str = "Encrypt <think>secret data</think>"
        result = self._run_logger(input_str, options=['--encrypt'])

        self.assertEqual(result.returncode, 0, f"Script exited with error: {result.stderr}")
        self.assertEqual(result.stdout.strip(), "Encrypt <think>secret data</think>")

        log_filename = self._get_expected_log_filename(encrypted=True)
        log_content = self._read_log_file(log_filename)
        self.assertIsNotNone(log_content, f"Log file {log_filename} not found.")

        match = re.search(r"---\n(.*?)\n---", log_content, re.DOTALL)
        self.assertTrue(match, "Could not find thought block in log content.")
        encoded_secret = match.group(1).strip()

        self.assertEqual(base64.b64decode(encoded_secret.encode('utf-8')).decode('utf-8'), "secret data")

    def test_redaction(self):
        input_str = "Redact <think>sensitive info</think> now"
        result = self._run_logger(input_str, options=['--redact-think'])

        self.assertEqual(result.returncode, 0, f"Script exited with error: {result.stderr}")
        self.assertEqual(result.stdout.strip(), "Redact <think>[redacted]</think> now")

        log_filename = self._get_expected_log_filename() # Logs to .md
        log_content = self._read_log_file(log_filename)
        self.assertIsNotNone(log_content, f"Log file {log_filename} not found.")
        self.assertRegex(log_content, r"JULES_CORE:\n---\nsensitive info\n---") # Raw thought in log

    def test_encrypt_and_redact(self):
        input_str = "Mix encrypt <think>very secret</think> and redact"
        result = self._run_logger(input_str, options=['--encrypt', '--redact-think'])

        self.assertEqual(result.returncode, 0, f"Script exited with error: {result.stderr}")
        self.assertEqual(result.stdout.strip(), "Mix encrypt <think>[redacted]</think> and redact")

        log_filename = self._get_expected_log_filename(encrypted=True)
        log_content = self._read_log_file(log_filename)
        self.assertIsNotNone(log_content, f"Log file {log_filename} not found.")

        match = re.search(r"---\n(.*?)\n---", log_content, re.DOTALL)
        self.assertTrue(match, "Could not find thought block in log content.")
        encoded_secret = match.group(1).strip()
        self.assertEqual(base64.b64decode(encoded_secret.encode('utf-8')).decode('utf-8'), "very secret")

    def test_no_thoughts_logged(self):
        input_str = "Plain text only."
        result = self._run_logger(input_str)

        self.assertEqual(result.returncode, 0, f"Script exited with error: {result.stderr}")
        self.assertEqual(result.stdout.strip(), "Plain text only.")

        log_filename = self._get_expected_log_filename()
        # The logger script might still create an empty log file or a log file by virtue of being called.
        # The important part is that no JULES_CORE entry for a thought is present.
        log_content = self._read_log_file(log_filename)

        if log_content: # Log file might exist and have been touched
            self.assertNotRegex(log_content, r"JULES_CORE:")
        else:
            self.assertIsNone(log_content, "Log file should not exist or be empty if no thoughts logged and file wasn't touched.")

        # Check stderr for the specific message from the logger script
        # Example: "[No new thoughts found in input to log. Log file is archive/THOUGHTLOG_YYYY-MM-DD.md]"
        # Or: "[No thoughts found in input. Log file archive/THOUGHTLOG_YYYY-MM-DD.md was not created/appended to.]"
        self.assertTrue(
            "No new thoughts found" in result.stderr or \
            "No thoughts found in input" in result.stderr,
            f"Unexpected stderr message: {result.stderr}"
        )

    def test_multiple_thoughts_mixed_options(self):
        input_str = "First <think>thought A</think> then <think>thought B</think> and finally <think>thought C</think>."
        result = self._run_logger(input_str, options=['--encrypt', '--redact-think'])

        self.assertEqual(result.returncode, 0, f"Script exited with error: {result.stderr}")
        self.assertEqual(result.stdout.strip(), "First <think>[redacted]</think> then <think>[redacted]</think> and finally <think>[redacted]</think>.")

        log_filename = self._get_expected_log_filename(encrypted=True)
        log_content = self._read_log_file(log_filename)
        self.assertIsNotNone(log_content, f"Log file {log_filename} not found.")

        # Verify all thoughts are logged and encrypted
        decoded_thoughts = []
        for match_obj in re.finditer(r"---\n(.*?)\n---", log_content, re.DOTALL):
            encoded_text = match_obj.group(1).strip()
            decoded_thoughts.append(base64.b64decode(encoded_text.encode('utf-8')).decode('utf-8'))

        self.assertListEqual(decoded_thoughts, ["thought A", "thought B", "thought C"])

if __name__ == '__main__':
    # Running with verbosity and not exiting allows test runner integration if needed
    unittest.main(argv=[sys.argv[0], '-v'], exit=False)
