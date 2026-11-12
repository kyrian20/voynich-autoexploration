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
            original = b"#=IVTFF Eva- 2.0 M optional header extension\n<f1r>\n"
            source.write_bytes(original)
            receipt = folder / "receipt.json"
            previous = b"PREVIOUS RECEIPT MUST SURVIVE\n"
            receipt.write_bytes(previous)
            stderr, stdout = io.StringIO(), io.StringIO()
            argv = ["audit_ivtff_minimum_format.py", "--out", str(receipt), str(source)]
            with patch.object(sys, "argv", argv), \
                 patch.object(auditor.os, "fsync", side_effect=OSError("injected fsync failure")) as fsync, \
                 patch.object(auditor.os, "replace") as replace, \
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


    def test_cleanup_failure_does_not_mask_primary_replace_error(self):
        # If unlink also fails, the CLI must still report the write failure.
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
            real_unlink = Path.unlink
            leaked = []

            def fail_temp_cleanup(path, *args, **kwargs):
                if path.name.startswith(".ivtff-receipt-"):
                    leaked.append(path)
                    raise PermissionError("injected cleanup failure")
                return real_unlink(path, *args, **kwargs)

            with patch.object(sys, "argv", argv), \
                 patch.object(auditor.os, "replace", side_effect=OSError("injected replace failure")), \
                 patch.object(Path, "unlink", autospec=True, side_effect=fail_temp_cleanup), \
                 contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(stdout):
                status = auditor.main()
            self.assertEqual(status, 2)
            self.assertEqual(stdout.getvalue(), "")
            self.assertIn("injected replace failure", stderr.getvalue())
            self.assertIn("Cannot remove temporary IVTFF receipt", stderr.getvalue())
            self.assertEqual(receipt.read_bytes(), previous)
            self.assertEqual(source.read_bytes(), original)
            self.assertEqual(len(leaked), 1)
            # Simulated unlink denial leaves a named file; caller is informed.
            self.assertTrue(leaked[0].exists())


    def test_successful_replace_does_not_attempt_stale_temp_cleanup(self):
        # os.replace consumes the temporary pathname. A subsequent unlink is
        # unnecessary and may falsely report a failed operation.
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            source = folder / "source.ivtff"
            original = b"#=IVTFF Eva- 2.0 M optional header extension\n<f1r>\n"
            source.write_bytes(original)
            receipt = folder / "receipt.json"
            stderr, stdout = io.StringIO(), io.StringIO()
            argv = ["audit_ivtff_minimum_format.py", "--out", str(receipt), str(source)]
            real_unlink = Path.unlink

            def reject_temp_unlink(path, *args, **kwargs):
                if path.name.startswith(".ivtff-receipt-"):
                    raise AssertionError("stale temporary cleanup after successful replace")
                return real_unlink(path, *args, **kwargs)

            with patch.object(sys, "argv", argv), \
                 patch.object(Path, "unlink", autospec=True, side_effect=reject_temp_unlink), \
                 contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(stdout):
                status = auditor.main()
            self.assertEqual(status, 0)
            self.assertEqual(stderr.getvalue(), "")
            self.assertIn('"status": "PASS"', stdout.getvalue())
            self.assertEqual(source.read_bytes(), original)
            self.assertEqual(list(folder.glob(".ivtff-receipt-*.tmp")), [])
            self.assertEqual(receipt.read_text(encoding="utf-8"), stdout.getvalue())


    def test_directory_destination_fails_without_leaking_temporary_receipt(self):
        # os.replace cannot replace a nonempty directory with a file.
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            source = folder / "source.ivtff"
            original = b"#=IVTFF Eva- 2.0 M optional header extension\n<f1r>\n"
            source.write_bytes(original)
            destination = folder / "receipt.json"
            destination.mkdir()
            sentinel = destination / "keep.txt"
            sentinel.write_bytes(b"DO NOT MODIFY")
            stderr, stdout = io.StringIO(), io.StringIO()
            argv = ["audit_ivtff_minimum_format.py", "--out", str(destination), str(source)]
            with patch.object(sys, "argv", argv), \
                 contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(stdout):
                status = auditor.main()
            self.assertEqual(status, 2)
            self.assertIn("Cannot write IVTFF receipt", stderr.getvalue())
            self.assertEqual(stdout.getvalue(), "")
            self.assertEqual(source.read_bytes(), original)
            self.assertEqual(sentinel.read_bytes(), b"DO NOT MODIFY")
            self.assertEqual(list(folder.glob(".ivtff-receipt-*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
