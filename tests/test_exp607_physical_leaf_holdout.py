"""Synthetic, metadata-only regressions for the frozen EXP-607 split audit."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import audit_exp607_physical_leaf_holdout as audit


class Exp607PhysicalLeafTests(unittest.TestCase):
    def test_opposite_sides_are_not_independent(self):
        pages = {"f5r": 2, "f5v": 3, "f1r": 1, "f1v": 1}
        result = audit.allocation(pages)
        self.assertEqual(result["shared_physical_leaves"], [5])
        self.assertEqual(result["test_leaves_exposed_to_train"], 1)
        self.assertEqual(result["test_leaves_unseen_in_train"], 0)
        self.assertEqual(result["train_lines"] + result["test_lines"], 7)

    def test_same_leaf_stays_independent_if_grouped(self):
        pages = {"f1r": 1, "f1v": 2}
        self.assertEqual(audit.allocation(pages)["shared_physical_leaves"], [])

    def test_historical_eligibility_is_explicit(self):
        raw = (b"<f5r> $L=A\n<f5r.1,@P0> ab.cd.ef\n"
               b"<f5v.1,@P0> ab.cd\n<f5v.2,@P0> x\n"
               b"<f1r.1,@L0> {bad}.ab.cd\n")
        self.assertEqual(audit.eligible_pages(raw), {"f5r": 1, "f5v": 1, "f1r": 1})

    def test_reject_drift_and_symlink_before_reading(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            good = root / "good"
            good.write_bytes(b"source")
            expected = __import__("hashlib").sha256(b"source").hexdigest()
            self.assertEqual(audit.verify_bytes(good, expected), b"source")
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                audit.verify_bytes(good, "0" * 64)
            link = root / "alias"
            link.symlink_to(good)
            with self.assertRaisesRegex(ValueError, "symlinked"):
                audit.verify_bytes(link, expected)

    def test_invalid_folio_rejected(self):
        with self.assertRaisesRegex(ValueError, "Invalid historical"):
            audit.leaf("f67r1")


if __name__ == "__main__":
    unittest.main()
