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

    def test_nonphysical_separators_cannot_forge_folio_headers(self):
        # A phantom page must never be promoted from a comment or locus body.
        for separator in "\v\f\x1c\x1d\x1e\x85\u2028\u2029":
            text = (
                "<f1r> $L=A\n<f1r.1,@P0> ab.cd.ef"
                + separator + "<f2r> $L=B\n<f2r.1,@P0> ab.cd.ef\n"
            )
            for reader in (audit.eligible_a, audit.eligible_b):
                with self.subTest(separator=ord(separator), reader=reader.__name__):
                    with self.assertRaisesRegex(ValueError, "Non-physical IVTFF line separator"):
                        reader(text)

    def test_only_cr_lf_and_crlf_delimit_physical_rows(self):
        for newline in ("\n", "\r", "\r\n"):
            with self.subTest(newline=repr(newline)):
                text = newline.join((
                    "<f1r> $L=A", "<f1r.1,@P0> ab.cd.ef",
                    "<f2r> $L=B", "<f2r.1,@P0> ab.cd.ef", "",
                ))
                self.assertEqual(audit.eligible_a(text), ["f1r", "f2r"])
                folios, labels = audit.eligible_b(text)
                self.assertEqual(folios, ["f1r", "f2r"])
                self.assertEqual(labels, {"f1r": "A", "f2r": "B"})

    def test_panels_collapse_to_same_leaf_and_named_excluded(self):
        self.assertEqual(audit.overlap({"f67r1", "fRos"}, {"f67v", "f68r"}), [67])
        self.assertEqual(audit.physical_leaf("fRos"), None)

    def test_currier_unknown_stratum_is_not_silently_assigned_to_a_or_b(self):
        folios = ["f1r", "f2r", "f3r"]
        counts, unknown = audit.currier_strata(folios, {"f1r": "A", "f2r": "B"})
        self.assertEqual(counts, {"A": 1, "B": 1, "?": 1})
        self.assertEqual(unknown, ["f3r"])

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
        for name in baseline:
            baseline[name]["B_currier_group_counts"] = dict(audit.EXPECTED_B_STRATA[name]["counts"])
            baseline[name]["B_unclassified_folios"] = list(audit.EXPECTED_B_STRATA[name]["unclassified"])
        frozen = {name: {method: audit.split_sha256(rows) for method, rows in methods.items()
                         if method in ("A_all_tokens", "B_interior_tokens")}
                  for name, methods in baseline.items()}
        with patch.dict(audit.EXPECTED_SPLIT_SHA256, frozen, clear=True):
            audit.check_expected(baseline)
            baseline["ZL3b"]["B_interior_tokens"][0]["shared_physical_leaves"].pop()
            with self.assertRaisesRegex(ValueError, "overlap counts drift"):
                audit.check_expected(baseline)

    def test_same_count_membership_and_seed_drift_are_rejected(self):
        baseline = {name: {method: [{"seed": index, "train_page_ids": 7,
                                    "test_page_ids": 3,
                                    "shared_physical_leaves": list(range(n))}
                                   for index, n in enumerate(values)]
                           for method, values in methods.items()}
                    for name, methods in audit.EXPECTED_OVERLAP.items()}
        for name in baseline:
            baseline[name]["B_currier_group_counts"] = dict(audit.EXPECTED_B_STRATA[name]["counts"])
            baseline[name]["B_unclassified_folios"] = list(audit.EXPECTED_B_STRATA[name]["unclassified"])
        frozen = {name: {method: audit.split_sha256(rows) for method, rows in methods.items()
                         if method in ("A_all_tokens", "B_interior_tokens")}
                  for name, methods in baseline.items()}
        with patch.dict(audit.EXPECTED_SPLIT_SHA256, frozen, clear=True):
            audit.check_expected(baseline)
            row = baseline["ZL3b"]["A_all_tokens"][0]
            original = row["shared_physical_leaves"][0]
            row["shared_physical_leaves"][0] = 999
            with self.assertRaisesRegex(ValueError, "split evidence drift"):
                audit.check_expected(baseline)
            row["shared_physical_leaves"][0] = original
            row["seed"] += 1
            with self.assertRaisesRegex(ValueError, "split evidence drift"):
                audit.check_expected(baseline)
            row["seed"] -= 1
            row["train_page_ids"] += 1
            with self.assertRaisesRegex(ValueError, "split evidence drift"):
                audit.check_expected(baseline)
            row["train_page_ids"] -= 1
            baseline["ZL3b"]["B_unclassified_folios"].pop()
            with self.assertRaisesRegex(ValueError, "Currier stratum drift"):
                audit.check_expected(baseline)


if __name__ == "__main__":
    unittest.main()
