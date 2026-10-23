"""Pure fixture tests for EXP-173 metadata-B folio sensitivity; no corpus needed."""
import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/audit_exp173_folio_sensitivity.py"
spec = importlib.util.spec_from_file_location("folio", SCRIPT)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class FolioSensitivityTests(unittest.TestCase):
    def test_within_line_expected(self):
        self.assertEqual(audit.line_counts(["yam", "xam", "y"]), {
            "lines": 1, "words": 3, "am": 2, "amLL": 0,
            "y": 2, "yLF": 1, "amExp": 2/3, "yExp": 2/3})

    def test_single_token_is_eligible(self):
        c = audit.line_counts(["yam"])
        self.assertEqual((c["amLL"], c["yLF"], c["amExp"], c["yExp"]), (1, 1, 1, 1))

    def test_no_empty_line(self):
        with self.assertRaises(ValueError):
            audit.line_counts([])

    def test_metadata_selection_and_signs(self):
        rows = [
            {"page": "f1r", "tokens": ["yam", "xam", "y"]},
            {"page": "f2r", "tokens": ["y", "xam"]},
            {"page": "f3r", "tokens": ["yam", "y", "xam"]},
            {"page": "f4r", "tokens": ["y", "yam"]},
            {"page": "f5r", "tokens": ["xam", "y"]},
        ]
        out = audit.analyze(rows, {"f1r": "B", "f2r": "B", "f3r": "B", "f4r": "B", "f5r": "A"})
        self.assertEqual(out["metadata_B_physical_folios"], 4)
        self.assertEqual(out["metadata_B"]["lines"], 4)
        self.assertEqual(out["metadata_B"]["amLL"], 3)
        self.assertEqual(out["metadata_B"]["yLF"], 4)
        self.assertEqual(out["metrics"]["am"]["folio_excess_positive"], 3)
        self.assertEqual(out["metrics"]["am"]["folio_excess_negative"], 1)
        self.assertGreater(out["metrics"]["am"]["jackknife_se"], 0)

    def test_recto_verso_clustered_together(self):
        rows = [{"page": "f1r", "tokens": ["yam", "y"]},
                {"page": "f1v", "tokens": ["y", "xam"]},
                {"page": "f2r", "tokens": ["yam", "xam"]},
                {"page": "f3r", "tokens": ["yam", "xam"]}]
        result = audit.analyze(rows, {"f1r": "B", "f1v": "B", "f2r": "B", "f3r": "B"})
        self.assertEqual(result["metadata_B_physical_folios"], 3)
        self.assertEqual(result["metadata_B_page_loci"], 4)
        self.assertEqual(result["folios"]["f1"]["lines"], 2)

    def test_leave_one_out_requires_folios(self):
        with self.assertRaises(ValueError):
            audit.analyze([{"page": "f1r", "tokens": ["yam"]}], {"f1r": "B"})

    def test_zero_denominator_fails(self):
        with self.assertRaises(ValueError):
            audit.enrichment({"lines": 1, "words": 1, "am": 0, "amLL": 0}, "am")

    def test_git_blob(self):
        self.assertEqual(audit.blob_sha(b"test\n"), "9daeafb9864cf43055ae93beb0afd6c7d144bfa4")


if __name__ == "__main__":
    unittest.main()
