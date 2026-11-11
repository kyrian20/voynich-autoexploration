#!/usr/bin/env python3
"""Regression: failed atomic receipt replacement must not corrupt prior data."""
import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import audit_ivtff_minimum_format as auditor


class IvtffAtomicFailureTests(unittest.TestCase):
    def test_replace_failure_preserves_previous_receipt_and_removes_temp(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            source = folder / "source.ivtff"
            original = b"#=IVTFF Eva- 2.0 M optional header extension\n<f1r>\n"
            source.write_bytes(original)
            receipt = folder / "receipt.json"
            previous = b"PREVIOUS RECEIPT MUST SURVIVE\n"
            receipt.write_bytes(previous)
            stderr, stdout = io.StringIO(), io.StringIO()
            argv = ["audit_ivtff_minimum_format.py", "--out", str(receipt), str(source)]
            with patch.object(sys, "argv", argv), \
                 patch.object(auditor.os, "replace", side_effect=OSError("injected replace failure")) as replace, \
                 contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(stdout):
                status = auditor.main()
            self.assertEqual(status, 2)
            replace.assert_called_once()
            self.assertIn("Cannot write IVTFF receipt", stderr.getvalue())
            self.assertEqual(stdout.getvalue(), "")
            self.assertEqual(receipt.read_bytes(), previous)
            self.assertEqual(source.read_bytes(), original)
            self.assertEqual(list(folder.glob(".ivtff-receipt-*.tmp")), [])


    def test_fsync_failure_preserves_previous_receipt_and_removes_temp(self):
        # Failure occurs after temporary content is written but before replace.
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            source = folder / "source.ivtff"
            original = b"#=IVTFF Eva- 2.0 M optional header extension\\n<f1r>\\n"
            source.write_bytes(original)
            receipt = folder / "receipt.json"
            previous = b"PREVIOUS RECEIPT MUST SURVIVE\\n"
            receipt.write_bytes(previous)
            stderr, stdout = io.StringIO(), io.StringIO()
            argv = ["audit_ivtff_minimum_format.py", "--out", str(receipt), str(source)]
            with patch.object(sys, "argv", argv), \\
                 patch.object(auditor.os, "fsync", side_effect=OSError("injected fsync failure")) as fsync, \\
                 patch.object(auditor.os, "replace") as replace, \\
                 contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(stdout):
                status = auditor.main()
            self.assertEqual(status, 2)
            fsync.assert_called_once()
            replace.assert_not_called()
            self.assertIn("Cannot write IVTFF receipt", stderr.getvalue())
            self.assertEqual(stdout.getvalue(), "")
            self.assertEqual(receipt.read_bytes(), previous)
            self.assertEqual(source.read_bytes(), original)
            self.assertEqual(list(folder.glob(".ivtff-receipt-*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
