import os
import re
from datetime import datetime
import sys
import base64
from typing import Optional

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


class ThoughtLogger:
    """Intercepts writes to a stream, logging <think>...</think> blocks."""

    def __init__(self, stream, module: str = "main", redact: bool = False, log_dir: str = "archive"):
        self.stream = stream
        self.module = module
        self.redact = redact
        self.log_dir = log_dir
        self.encrypt = os.getenv("THOUGHTLOG_ENCRYPT") == "1"
        key_b64 = os.getenv("THOUGHTLOG_KEY")
        if self.encrypt:
            if key_b64:
                self.key = base64.b64decode(key_b64)
            else:
                # fallback deterministic key for tests/demo (32 bytes)
                self.key = b"0" * 32
        else:
            self.key = None
        os.makedirs(self.log_dir, exist_ok=True)

    def _log_path(self) -> str:
        date_str = datetime.now().strftime("%Y-%m-%d")
        ext = "enc" if self.encrypt else "md"
        return os.path.join(self.log_dir, f"THOUGHTLOG_{date_str}.{ext}")

    def _encrypt(self, plaintext: str) -> bytes:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded = padder.update(plaintext.encode("utf-8")) + padder.finalize()
        ciphertext = encryptor.update(padded) + encryptor.finalize()
        return iv + ciphertext

    def _append_log(self, text: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"{timestamp} [{self.module}] {text}\n"
        path = self._log_path()
        if self.encrypt:
            data = self._encrypt(line)
            mode = "ab"
            with open(path, mode) as f:
                f.write(data)
        else:
            with open(path, "a", encoding="utf-8") as f:
                f.write(line)

    def write(self, text: str) -> None:
        pattern = re.compile(r"<think>(.*?)</think>", re.DOTALL)
        pos = 0
        output_parts = []
        for match in pattern.finditer(text):
            start, end = match.span()
            output_parts.append(text[pos:start])
            inner = match.group(1)
            self._append_log(inner)
            if self.redact:
                output_parts.append("<think>[redacted]</think>")
            else:
                output_parts.append(match.group(0))
            pos = end
        output_parts.append(text[pos:])
        output = "".join(output_parts)
        self.stream.write(output)
        self.stream.flush()

    def flush(self) -> None:
        self.stream.flush()


def install(redact: bool = False, module: str = "main", log_dir: str = "archive") -> None:
    """Install thought logging on stdout and stderr."""
    sys.stdout = ThoughtLogger(sys.stdout, module=module, redact=redact, log_dir=log_dir)
    sys.stderr = ThoughtLogger(sys.stderr, module=module, redact=redact, log_dir=log_dir)
