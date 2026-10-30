"""Deterministic regression for Library EXP-624 physical-leaf split audit."""
import unittest

from scripts import audit_library_exp624_leaf_leakage as audit


class LibraryExp624LeakageTests(unittest.TestCase):
    def test_lcg_and_split_fixture(self):
        pages = [{"id": p, "lang": "A", "words": ["ab"]}
                 for p in ("f1r", "f1v", "f2r", "f2v", "f3r", "f3v")]
        first = audit.splits(pages, 624010, 1)[0]
        self.assertEqual(first["train_pages"], 4)
        self.assertEqual(first["test_pages"], 2)
        self.assertEqual(len(first["shared_physical_leaves"]),
                         len(set(first["shared_physical_leaves"])))
        self.assertTrue(all(p in {"f1r", "f1v", "f2r", "f2v", "f3r", "f3v"}
                            for p in first["leaked_test_page_ids"]))

    def test_parser_eligibility_and_language(self):
        text = ("<f1r> <! $L=A>\n<f1r.P.1,P0> a.ab.cd\n"
                "<f1v> <! $L=B>\n<f1v.P.1,P0> aa.bb\n"
                "<f2r> <! $L=A>\n<f2r.L.1,L0> aa.bb\n").encode()
        pages = audit.parse_pages(text)
        self.assertEqual([(p["id"], p["lang"]) for p in pages],
                         [("f1r", "A"), ("f1v", "B")])

    def test_frozen_corpus_split_regressions(self):
        results = {label: audit.analyze(label, (audit.ROOT / "data/transcriptions" / source[0]).read_bytes())
                   for label, source in audit.SOURCES.items()}
        audit.check(results)
        self.assertEqual([len(r["shared_physical_leaves"]) for r in results["ZL3b"]["groups"]["all"]],
                         list(audit.EXPECTED["ZL3b"]["all"]))

    def test_wrong_corpus_rejected(self):
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            audit.analyze("ZL3b", b"not the historical corpus")

    def test_changed_expected_series_rejected(self):
        # Adversarial mutation of a reconstructed split must fail checkpoints.
        results = {label: audit.analyze(label, (audit.ROOT / "data/transcriptions" / source[0]).read_bytes())
                   for label, source in audit.SOURCES.items()}
        results["ZL3b"]["groups"]["all"][0]["shared_physical_leaves"].pop()
        with self.assertRaisesRegex(ValueError, "split drift"):
            audit.check(results)


if __name__ == "__main__":
    unittest.main()
