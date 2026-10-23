"""Pure fixture checks for read-only EXP-173 metadata crosswalk."""
from pathlib import Path
import importlib.util
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/audit_exp173_currier_crosswalk.py"
spec = importlib.util.spec_from_file_location("crosswalk", SCRIPT)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class CrosswalkTests(unittest.TestCase):
    def test_historical_threshold_and_page_metadata(self):
        corpus = """<f1r> <! $Q=B $L=A>\n<f1r.1,@P0> xedy.yam.a.b.c\n<f1r.2,+P0> yy.x.a.b.c\n<f1v> <! $Q=A $L=B>\n<f1v.1,@P0> yedy.xam.a.b.c\n<f1v.2,+P0> y.x.a.b.c\n"""
        rows, legacy, labels = audit.read_legacy_population(corpus)
        self.assertEqual(len(rows), 4)
        self.assertEqual(legacy, {1: "B"})
        self.assertEqual(labels, {"f1r": "A", "f1v": "B"})
        result = audit.crosswalk(corpus)
        self.assertEqual(result["confusion_lines"], {"B->A": 2, "B->B": 2})
        self.assertEqual(result["mismatch_lines"], 2)
        self.assertEqual(result["metadata_B"]["lines"], 2)

    def test_missing_metadata_is_not_imputed(self):
        corpus = """<f2r> <! $Q=A>\n<f2r.1,@P0> yedy.am\n<f2r.2,+P0> aa.bb.cc.dd.ee.ff.gg.hh.ii.jj\n"""
        result = audit.crosswalk(corpus)
        self.assertEqual(result["confusion_lines"], {"B->unknown": 2})
        self.assertEqual(result["metadata_classified_rows"], 0)
        self.assertEqual(result["metadata_unknown_pages"], {"f2r": 2})

    def test_non_p_and_short_line_excluded(self):
        corpus = """<f3r> <! $L=B>\n<f3r.1,@P0> x.y\n<f3r.2,@Lx> yy.zz\n<f3r.3,@P0> <tag>.<more>\n"""
        rows, legacy, _ = audit.read_legacy_population(corpus)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["tokens"], ["x", "y"])
        self.assertEqual(legacy, {})

    def test_conflicting_L_rejected(self):
        with self.assertRaises(ValueError):
            audit.read_legacy_population("<f4r> <! $L=A $L=B>\n")

    def test_metrics_exact(self):
        rows = [{"tokens": ["yam", "xam"]}, {"tokens": ["y", "xx"]}]
        r = audit.metrics(rows)
        self.assertEqual((r["lines"], r["words"], r["am"], r["amLL"], r["y"], r["yLF"]), (2, 4, 2, 1, 2, 2))
        self.assertEqual(r["amLLenrichment"], 1.0)
        self.assertEqual(r["yLFenrichment"], 2.0)

    def test_git_blob_sha1(self):
        self.assertEqual(audit.git_blob_sha1(b"test\n"), "9daeafb9864cf43055ae93beb0afd6c7d144bfa4")


if __name__ == "__main__":
    unittest.main()
