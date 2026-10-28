"""Regression tests for frozen page-side splits; no held-out targets are scored."""
import hashlib
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import audit_exp602_exp603_physical_leaf_holdout as audit


class PhysicalLeafHoldoutTests(unittest.TestCase):
    def test_opposite_sides_share_a_physical_leaf(self):
        rows = [("f34r", "B"), ("f34v", "B"),
                ("f46r", "B"), ("f46v", "B")]
        got = audit.allocation(rows, ("B",))
        self.assertEqual(got["shared"], [34])
        self.assertEqual(got["unseen_test_leaves"], [46])
        self.assertEqual((got["train_lines"], got["test_lines"]), (1, 3))
        self.assertEqual((got["train_pages"], got["test_pages"]), (1, 3))

    def test_panels_are_part_of_the_same_numbered_leaf(self):
        self.assertEqual(audit.physical_leaf("f86v3"), 86)
        self.assertEqual(audit.physical_leaf("f95r2"), 95)
        self.assertEqual(audit.physical_leaf("f102v1"), 102)
        self.assertEqual(audit.physical_leaf("f102r2"), 102)

    def test_historical_eligibility_and_dialects(self):
        raw = (b"<f34r> <! $L=B>\n"
               b"<f34r.1,@P0> ab.cd\n"
               b"<f34r.2,@L0> ab.cd\n"
               b"<f34v> <! $L=A>\n"
               b"<f34v.1,@P0> ab.cd.ef\n"
               b"<f34v.2,@P0> ab\n"
               b"<f46r> <! $L=?>\n"
               b"<f46r.1,@P0> ab.cd\n")
        rows = audit.eligible_rows(raw)
        self.assertEqual(rows, [("f34r", "B"), ("f34v", "A")])
        self.assertEqual(audit.allocation(rows, ("B",))["train_lines"], 1)
        self.assertEqual(audit.allocation(rows, ("A", "B"))["test_lines"], 1)

    def test_reject_invalid_physical_identifier(self):
        for page in ("f67", "f67rX", "f67v2extra", "f-1r", "f٦r"):
            with self.subTest(page=page), self.assertRaises(ValueError):
                audit.physical_leaf(page)

    def test_frozen_hash_and_symlink_fail_closed(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            source.write_bytes(b"unchanged")
            expected = hashlib.sha256(b"unchanged").hexdigest()
            self.assertEqual(audit.verify_bytes(source, expected), b"unchanged")
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                audit.verify_bytes(source, "0" * 64)
            alias = root / "alias"
            alias.symlink_to(source)
            with self.assertRaisesRegex(ValueError, "symlinked"):
                audit.verify_bytes(alias, expected)

    def test_shared_identity_drift_even_with_same_count(self):
        expected = {"train_lines": 1, "test_lines": 1,
                    "train_pages": 1, "test_pages": 1,
                    "train_leaves": 1, "test_leaves": 1,
                    "shared": [34]}
        changed = dict(expected, shared=[35])
        with self.assertRaisesRegex(ValueError, "shared drift"):
            audit.check_snapshot(changed, expected)
        audit.check_snapshot(expected, expected)


if __name__ == "__main__":
    unittest.main()
