"""Regression: unsupported compression with *consistent* local/central ZIP headers.

The earlier PR #306 test only exercises the header-mismatch gate, not the
NotImplementedError boundary. Synthetic ZIP bytes; no historical artifact.
"""
from contextlib import redirect_stderr
import hashlib
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "research/maintenance/verify_pr287_ivtff_artifact.py"
spec = importlib.util.spec_from_file_location("ivtff_consistent_method_verifier", SCRIPT)
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class UnsupportedCompressionConsistentHeaders(unittest.TestCase):
    def test_cli_rejects_consistent_unsupported_method_without_traceback(self):
        # Generate real ZIP bytes first, then mutate *both* method fields.
        # Method 99 is not supported by Python's zipfile decompressor.
        stream = io.BytesIO()
        payload = b'{"audit":"IVTFF file-level minimums","status":"PASS","files":[]}'
        manifest = hashlib.sha256(payload).hexdigest().encode("ascii") + b"  ivtff-minimum-format.json\n"
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("ivtff-minimum-format.json", payload)
            archive.writestr("ivtff-minimum-format.sha256", manifest)
        data = bytearray(stream.getvalue())
        local = data.find(b"PK\x03\x04")
        central = data.find(b"PK\x01\x02")
        self.assertGreaterEqual(local, 0)
        self.assertGreaterEqual(central, 0)
        method = (99).to_bytes(2, "little")
        data[local + 8:local + 10] = method
        data[central + 10:central + 12] = method
        data = bytes(data)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "unsupported-consistent.zip"
            path.write_bytes(data)
            stderr = io.StringIO()
            with patch.object(verifier, "ZIP_SHA", hashlib.sha256(data).hexdigest()), \
                 patch.object(sys, "argv", ["verify_pr287_ivtff_artifact.py", str(path)]), \
                 redirect_stderr(stderr):
                self.assertEqual(verifier.main(), 1)
            self.assertIn("REJECTED:", stderr.getvalue())
            self.assertIn("compression method is not supported", stderr.getvalue())
            self.assertNotIn("header mismatch", stderr.getvalue())
            self.assertNotIn("Traceback", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
