#!/usr/bin/env python3
"""Fail-closed regressions for unsafe or unresolvable IVTFF receipt paths."""
import contextlib
import io
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import audit_ivtff_minimum_format as auditor


class OutputAliasErrorsTests(unittest.TestCase):
    def test_symlink_cycle_is_rejected_without_touching_source(self):
        if not hasattr(os, "symlink"):
            self.skipTest("symlinks unavailable")
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            source = folder / "source.ivtff"
            original = b"#=IVTFF Eva- 2.0 M optional header extension\n<f1r>\n"
            source.write_bytes(original)
            first, second = folder / "cycle-a.json", folder / "cycle-b.json"
            try:
                first.symlink_to(second)
                second.symlink_to(first)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")
            stderr, stdout = io.StringIO(), io.StringIO()
            argv = ["audit_ivtff_minimum_format.py", "--out", str(first), str(source)]
            with patch.object(sys, "argv", argv), \
                 contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(stdout):
                status = auditor.main()
            self.assertEqual(status, 2)
            self.assertIn("Cannot verify IVTFF receipt path safety", stderr.getvalue())
            self.assertEqual(stdout.getvalue(), "")
            self.assertEqual(source.read_bytes(), original)
            self.assertTrue(first.is_symlink())
            self.assertTrue(second.is_symlink())
            self.assertEqual(list(folder.glob(".ivtff-receipt-*.tmp")), [])

    def test_resolution_oserror_is_reported_without_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            source = folder / "source.ivtff"
            original = b"#=IVTFF Eva- 2.0 M optional header extension\n<f1r>\n"
            source.write_bytes(original)
            output = folder / "receipt.json"
            argv = ["audit_ivtff_minimum_format.py", "--out", str(output), str(source)]
            original_resolve = Path.resolve

            def reject_output(path, *args, **kwargs):
                if path == output:
                    raise PermissionError("injected resolution denial")
                return original_resolve(path, *args, **kwargs)

            stderr, stdout = io.StringIO(), io.StringIO()
            with patch.object(sys, "argv", argv), \
                 patch.object(Path, "resolve", autospec=True, side_effect=reject_output), \
                 contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(stdout):
                status = auditor.main()
            self.assertEqual(status, 2)
            self.assertIn("injected resolution denial", stderr.getvalue())
            self.assertEqual(stdout.getvalue(), "")
            self.assertFalse(output.exists())
            self.assertEqual(source.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
