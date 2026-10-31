"""Regression tests for strict JSON input to the generic snapshot comparator.

All files are synthetic; no archived snapshot or corpus is modified.
"""
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_audit_snapshot as checker


class GenericSnapshotJsonIntegrityTests(unittest.TestCase):
    def compare_files(self, expected, actual):
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "expected.json"
            second = Path(tmp) / "actual.json"
            first.write_text(expected, encoding="utf-8")
            second.write_text(actual, encoding="utf-8")
            with patch.object(sys, "argv", ["check_audit_snapshot.py", str(first), str(second)]):
                with redirect_stdout(io.StringIO()) as captured:
                    checker.main()
            return captured.getvalue()

    def test_duplicate_expected_key_is_rejected_even_if_values_equal(self):
        with self.assertRaisesRegex(ValueError, "Duplicate audit snapshot JSON key: n"):
            self.compare_files('{"n": 1, "n": 1}', '{"n": 1}')

    def test_duplicate_actual_nested_key_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate audit snapshot JSON key: score"):
            self.compare_files('{"result": {"score": 1}}',
                               '{"result": {"score": 0, "score": 1}}')

    def test_duplicate_array_member_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate audit snapshot JSON key: x"):
            self.compare_files('{"rows": [{"x": 1}]}',
                               '{"rows": [{"x": 2, "x": 1}]}')

    def test_nonstandard_nan_is_rejected_before_comparison(self):
        with self.assertRaisesRegex(ValueError, "Non-standard audit snapshot JSON constant: NaN"):
            self.compare_files('{"n": NaN}', '{"n": NaN}')

    def test_nonstandard_infinity_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Non-standard audit snapshot JSON constant: Infinity"):
            self.compare_files('{"n": 1.0}', '{"n": Infinity}')

    def test_valid_structured_snapshot_still_matches(self):
        output = self.compare_files(
            '{"rows": [{"n": 12, "score": 0.125}], "status": "REPRODUCED"}',
            '{"status": "REPRODUCED", "rows": [{"score": 0.125, "n": 12}]}')
        self.assertIn("Audit snapshot reproduced", output)

    def test_type_mismatch_still_rejected(self):
        with self.assertRaisesRegex(ValueError, "types differ"):
            self.compare_files('{"n": true}', '{"n": 1}')


if __name__ == "__main__":
    unittest.main()
