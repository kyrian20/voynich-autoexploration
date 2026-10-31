"""Fail closed if a frozen holdout manifest misstates scientific-use rules.

These are synthetic metadata mutations. The two source transcriptions are
read-only and their original SHA-256 values are verified by audit().
No manuscript tokens are used to select or test a rule.
"""
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_holdout_locus_coverage import ROOT as SOURCE_ROOT, SOURCE_NAMES, audit, load_manifest


class FrozenHoldoutContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = {
            name: (SOURCE_ROOT / "data/transcriptions" / name).read_bytes()
            for name in SOURCE_NAMES
        }
        cls.original = load_manifest()

    def setUp(self):
        self.manifest = copy.deepcopy(self.original)

    def test_unmodified_manifest_and_original_sources_pass(self):
        result = audit(self.sources, self.manifest)
        self.assertEqual(result["eligible_numeric_physical_leaves"], 102)
        self.assertEqual(result["status"], "COVERAGE_VERIFIED_NOT_IVTFF_OR_SEMANTIC_VALIDATION")

    def test_false_validated_status_rejected(self):
        self.manifest["status"] = "VALIDATED"
        with self.assertRaisesRegex(ValueError, "contract mismatch: status"):
            audit(self.sources, self.manifest)

    def test_prior_exposure_caveat_cannot_be_removed(self):
        del self.manifest["caveat"]
        with self.assertRaisesRegex(ValueError, "manifest fields mismatch"):
            audit(self.sources, self.manifest)

    def test_prior_exposure_caveat_cannot_be_reworded_as_blind(self):
        self.manifest["caveat"] = "Historically blind semantic validation"
        with self.assertRaisesRegex(ValueError, "contract mismatch: caveat"):
            audit(self.sources, self.manifest)

    def test_test_folio_restrictions_cannot_be_removed(self):
        self.manifest["forbidden"].remove("tuning on test outcomes")
        with self.assertRaisesRegex(ValueError, "contract mismatch: forbidden"):
            audit(self.sources, self.manifest)

    def test_allocation_thresholds_cannot_be_misreported(self):
        self.manifest["allocation"]["train"] = 0.8
        with self.assertRaisesRegex(ValueError, "contract mismatch: allocation"):
            audit(self.sources, self.manifest)

    def test_unit_cannot_be_relabelled_as_lines(self):
        self.manifest["unit"] = "random line split"
        with self.assertRaisesRegex(ValueError, "contract mismatch: unit"):
            audit(self.sources, self.manifest)

    def test_selection_policy_cannot_be_relabelled(self):
        self.manifest["selection"] = "random token selection"
        with self.assertRaisesRegex(ValueError, "contract mismatch: selection"):
            audit(self.sources, self.manifest)

    def test_unknown_scientific_claim_field_rejected(self):
        self.manifest["semantic_validation"] = True
        with self.assertRaisesRegex(ValueError, "manifest fields mismatch"):
            audit(self.sources, self.manifest)

    def test_extra_nested_corpus_claim_rejected(self):
        # Before this guard, top-level fields were frozen but a nested
        # corpus record could assert semantic validation and still pass.
        self.manifest["corpora"][SOURCE_NAMES[0]]["semantic_validation"] = True
        with self.assertRaisesRegex(ValueError, "Frozen source metadata fields mismatch"):
            audit(self.sources, self.manifest)

    def test_missing_nested_corpus_provenance_field_rejected(self):
        del self.manifest["corpora"][SOURCE_NAMES[0]]["sha256"]
        with self.assertRaisesRegex(ValueError, "Frozen source metadata fields mismatch"):
            audit(self.sources, self.manifest)

    def test_nonmapping_nested_corpus_record_rejected(self):
        self.manifest["corpora"][SOURCE_NAMES[0]] = []
        with self.assertRaisesRegex(ValueError, "Frozen source metadata fields mismatch"):
            audit(self.sources, self.manifest)

    def test_extra_count_field_rejected(self):
        self.manifest["counts"]["blind_test"] = 102
        with self.assertRaisesRegex(ValueError, "count fields mismatch"):
            audit(self.sources, self.manifest)

    def test_extra_source_only_edition_rejected(self):
        self.manifest["source_only_leaves"]["invented.txt"] = []
        with self.assertRaisesRegex(ValueError, "source-only edition fields mismatch"):
            audit(self.sources, self.manifest)


if __name__ == "__main__":
    unittest.main()
