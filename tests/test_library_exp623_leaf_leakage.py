"""Synthetic metadata-only regressions for archived Library EXP-623 split audit."""
import hashlib
import unittest
from unittest.mock import patch
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import audit_library_exp623_leaf_leakage as audit


class LibraryExp623LeakageTests(unittest.TestCase):
    def test_archived_rng_vectors(self):
        lcg = audit.LCG(623101)
        self.assertAlmostEqual(lcg.random(), 0.7203728687018156, places=10)
        mulberry = audit.Mulberry32(623)
        self.assertAlmostEqual(mulberry.random(), 0.21315328311175108, places=10)

    def test_eligibility_and_side_level_split(self):
        text = (
            "<f1r> $L=A\n<f1r.1,@P0> ab.cd.ef.gh\n"
            "<f1v> $L=A\n<f1v.1,@P0> ab.cd.ef.gh\n"
            "<f2r> $L=B\n<f2r.1,@P0> ab.cd.ef.gh\n"
            "<f2v> $L=B\n<f2v.1,@P0> ab.cd.ef.gh\n"
        )
        self.assertEqual(audit.eligible_a(text), ["f1r", "f1v", "f2r", "f2v"])
        folios, labels = audit.eligible_b(text)
        self.assertEqual(folios, ["f1r", "f1v", "f2r", "f2v"])
        self.assertEqual(labels, {"f1r": "A", "f1v": "A", "f2r": "B", "f2v": "B"})
        self.assertEqual(audit.overlap({"f1r", "f2v"}, {"f1v", "f2r"}), [1, 2])
        self.assertEqual(audit.overlap({"f1r", "f1v"}, {"f2r", "f2v"}), [])

    def test_panels_collapse_to_same_leaf_and_named_excluded(self):
        self.assertEqual(audit.overlap({"f67r1", "fRos"}, {"f67v", "f68r"}), [67])
        self.assertEqual(audit.physical_leaf("fRos"), None)

    def test_source_hash_guard(self):
        raw = b"<f1r> $L=A\n<f1r.1,@P0> aa.bb.cc\n"
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            audit.analyze("ZL3b", raw)
        with patch.dict(audit.CORPORA, {"ZL3b": ("fixture", hashlib.sha256(raw).hexdigest(), 623101)}):
            result = audit.analyze("ZL3b", raw)
        self.assertEqual(result["A_eligible_page_ids"], 1)
        self.assertEqual(result["B_eligible_page_ids"], 1)

    def test_frozen_count_guard(self):
        baseline = {name: {method: [{"shared_physical_leaves": list(range(n))} for n in values]
                           for method, values in methods.items()}
                    for name, methods in audit.EXPECTED_OVERLAP.items()}
        audit.check_expected(baseline)
        baseline["ZL3b"]["B_interior_tokens"][0]["shared_physical_leaves"].pop()
        with self.assertRaisesRegex(ValueError, "overlap counts drift"):
            audit.check_expected(baseline)


if __name__ == "__main__":
    unittest.main()
