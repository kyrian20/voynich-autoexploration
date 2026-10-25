"""Guard against silent omission of nonnumeric loci in a numeric-leaf holdout.

Synthetic fixtures only: original corpus and frozen v2 manifest are never edited.
"""
import hashlib
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_holdout_locus_coverage import audit, inspect_source


class HoldoutLocusCoverageTests(unittest.TestCase):
    def setUp(self):
        self.sources = {
            "eva_zl3b.txt": b"<f1r.1> a\n<f2v1.2> b\n<f3r.1> c\n<fRos> metadata\n<fRos.1,@L0> d\n",
            "eva_it2a.txt": b"<f1r.1> a\n<f2v1.2> b\n<f3r.1> c\n",
        }
        self.manifest = {
            "schema_version": 2,
            "corpora": {
                name: {
                    "path": f"data/transcriptions/{name}",
                    "sha256": hashlib.sha256(raw).hexdigest(),
                    "leaf_count": 3,
                }
                for name, raw in self.sources.items()
            },
            "partitions": {"train": [1], "development": [2], "test": [3]},
            "counts": {"train": 1, "development": 1, "test": 1},
            "eligible_count": 3,
            "source_only_leaves": {"eva_zl3b.txt": [], "eva_it2a.txt": []},
        }

    def test_named_rosettes_excluded_and_explicit(self):
        result = audit(self.sources, self.manifest)
        self.assertEqual(result["eligible_numeric_physical_leaves"], 3)
        self.assertEqual(result["source_coverage"]["eva_zl3b.txt"]["named_locus_records"], {"Ros": 2})
        self.assertEqual(result["source_coverage"]["eva_it2a.txt"]["named_locus_record_count"], 0)
        self.assertIn("EXCLUDED", result["named_loci_holdout_status"])

    def test_numeric_header_must_parse(self):
        with self.assertRaisesRegex(ValueError, "Unparsed numeric"):
            inspect_source(b"<f1r.1> a\n<f2x.1> invalid\n")

    def test_named_header_must_parse(self):
        with self.assertRaisesRegex(ValueError, "Unparsed named"):
            inspect_source(b"<f1r.1> a\n<fRos broken\n")

    def test_nonpositive_leaf_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Nonpositive"):
            inspect_source(b"<f0r.1> invalid\n<f1r.1> a\n")

    def test_source_provenance_cannot_be_substituted(self):
        tampered = dict(self.sources, **{"eva_zl3b.txt": self.sources["eva_zl3b.txt"] + b"x"})
        with self.assertRaisesRegex(ValueError, "provenance mismatch"):
            audit(tampered, self.manifest)

    def test_missing_leaf_or_duplicate_assignment_fails(self):
        self.manifest["partitions"]["test"] = [1]
        with self.assertRaisesRegex(ValueError, "Assigned leaves differ"):
            audit(self.sources, self.manifest)

    def test_named_loci_never_become_numeric_partitions(self):
        self.manifest["partitions"]["test"] = [3, 4]
        self.manifest["counts"]["test"] = 2
        with self.assertRaisesRegex(ValueError, "Assigned leaves differ"):
            audit(self.sources, self.manifest)


if __name__ == "__main__":
    unittest.main()
