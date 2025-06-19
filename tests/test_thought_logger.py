import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import os
import unittest
import tempfile
import base64
from io import StringIO

import thought_logger


class ThoughtLoggerTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)

    def read_log(self, encrypt=False):
        date_str = thought_logger.datetime.now().strftime("%Y-%m-%d")
        ext = 'enc' if encrypt else 'md'
        path = os.path.join(self.tmpdir.name, f"THOUGHTLOG_{date_str}.{ext}")
        with open(path, 'rb' if encrypt else 'r') as f:
            return f.read()

    def test_plain_log(self):
        os.environ.pop('THOUGHTLOG_ENCRYPT', None)
        out = StringIO()
        logger = thought_logger.ThoughtLogger(out, log_dir=self.tmpdir.name)
        logger.write("<think>secret chain</think> hello")
        log = self.read_log(encrypt=False)
        self.assertIn('secret chain', log)
        self.assertTrue(out.getvalue().startswith('<think>secret chain</think>'))

    def test_encrypted_roundtrip(self):
        os.environ['THOUGHTLOG_ENCRYPT'] = '1'
        key = b'a' * 32
        os.environ['THOUGHTLOG_KEY'] = base64.b64encode(key).decode()
        out = StringIO()
        logger = thought_logger.ThoughtLogger(out, log_dir=self.tmpdir.name)
        logger.write("<think>encrypt me</think>")
        data = self.read_log(encrypt=True)
        iv = data[:16]
        cipher = thought_logger.Cipher(thought_logger.algorithms.AES(key),
                                       thought_logger.modes.CBC(iv),
                                       backend=thought_logger.default_backend())
        decryptor = cipher.decryptor()
        unpadder = thought_logger.padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(decryptor.update(data[16:]) + decryptor.finalize()) + unpadder.finalize()
        self.assertIn('encrypt me', plaintext.decode())

    def test_redact_flag(self):
        os.environ.pop('THOUGHTLOG_ENCRYPT', None)
        out = StringIO()
        logger = thought_logger.ThoughtLogger(out, log_dir=self.tmpdir.name, redact=True)
        logger.write("<think>redact this</think>")
        log = self.read_log(encrypt=False)
        self.assertIn('redact this', log)
        self.assertEqual(out.getvalue().strip(), '<think>[redacted]</think>')


if __name__ == '__main__':
    unittest.main()
