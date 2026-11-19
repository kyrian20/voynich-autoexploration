#!/usr/bin/env python3
"""Regression: samefile inspection errors must fail closed before receipt output."""
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


class SamefileDenialTests(unittest.TestCase):
    def test_existing_output_samefile_permission_error_preserves_both_files(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            source = folder / "source.ivtff"
            output = folder / "receipt.json"
            original_source = b"#=IVTFF Eva- 2.0 M optional header extension\n<f1r>\n"
            original_output = b"previous receipt must survive\n"
            source.write_bytes(original_source)
            output.write_bytes(original_output)
            argv = ["audit_ivtff_minimum_format.py", "--out", str(output), str(source)]
            stderr, stdout = io.StringIO(), io.StringIO()
            original_samefile = Path.samefile

            def deny_output_comparison(path, other):
                if path == output:
                    raise PermissionError("injected samefile denial")
                return original_samefile(path, other)

            with patch.object(sys, "argv", argv), \
                 patch.object(Path, "samefile", autospec=True, side_effect=deny_output_comparison), \
                 contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(stdout):
                status = auditor.main()
            self.assertEqual(status, 2)
            self.assertIn("Cannot verify IVTFF receipt path safety", stderr.getvalue())
            self.assertIn("injected samefile denial", stderr.getvalue())
            self.assertEqual(stdout.getvalue(), "")
            self.assertEqual(source.read_bytes(), original_source)
            self.assertEqual(output.read_bytes(), original_output)
            self.assertEqual(list(folder.glob(".ivtff-receipt-*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
