"""Guard against silent omission of nonnumeric loci in a numeric-leaf holdout.

Synthetic fixtures only: original corpus and frozen v2 manifest are never edited.
"""
import hashlib
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_holdout_locus_coverage import audit, inspect_source, FROZEN_SALT


class HoldoutLocusCoverageTests(unittest.TestCase):
    def setUp(self):
        self.sources = {
            "eva_zl3b.txt": b"<f1r> metadata\n<f1r.1,@P0> a\n<f4v1> metadata\n<f4v1.2,@P0> b\n<f3r> metadata\n<f3r.1,@P0> c\n<fRos> metadata\n<fRos.1,@L0> d\n",
            "eva_it2a.txt": b"<f1r> metadata\n<f1r.1,@P0> a\n<f4v1> metadata\n<f4v1.2,@P0> b\n<f3r> metadata\n<f3r.1,@P0> c\n",
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
            "salt": FROZEN_SALT,
            "partitions": {"train": [1], "development": [4], "test": [3]},
            "counts": {"train": 1, "development": 1, "test": 1},
            "eligible_count": 3,
            "source_only_leaves": {"eva_zl3b.txt": [], "eva_it2a.txt": []},
        }

    def test_named_rosettes_excluded_and_explicit(self):
        result = audit(self.sources, self.manifest)
        self.assertEqual(result["eligible_numeric_physical_leaves"], 3)
        self.assertEqual(result["source_coverage"]["eva_zl3b.txt"]["named_locus_records"], {"Ros": 1})
        self.assertEqual(result["source_coverage"]["eva_zl3b.txt"]["named_page_headers"], {"Ros": 1})
        self.assertEqual(result["source_coverage"]["eva_zl3b.txt"]["named_tag_count"], 2)
        self.assertEqual(result["source_coverage"]["eva_zl3b.txt"]["named_page_header_count"], 1)
        self.assertEqual(result["source_coverage"]["eva_zl3b.txt"]["named_locus_record_count"], 1)
        for source in self.sources:
            counts = result["source_coverage"][source]
            self.assertEqual(counts["numeric_tag_count"], 6)
            self.assertEqual(counts["numeric_page_header_count"], 3)
            self.assertEqual(counts["numeric_locus_record_count"], 3)
            self.assertEqual(counts["numeric_tag_count"], counts["numeric_page_header_count"] + counts["numeric_locus_record_count"])
        self.assertEqual(result["source_coverage"]["eva_it2a.txt"]["named_locus_record_count"], 0)
        self.assertIn("EXCLUDED", result["named_loci_holdout_status"])

    def test_repeated_page_header_does_not_inflate_locus_records(self):
        record = inspect_source(
            b"<f1r> first\n<f1r> repeated\n<f1r.1,@P0> a\n"
            b"<fRos> header\n<fRos.1,@L0> b\n"
        )
        self.assertEqual(record["numeric_tag_count"], 3)
        self.assertEqual(record["numeric_page_header_count"], 2)
        self.assertEqual(record["numeric_locus_record_count"], 1)
        self.assertEqual(record["named_tag_count"], 2)
        self.assertEqual(record["named_page_headers"], {"Ros": 1})
        self.assertEqual(record["named_locus_records"], {"Ros": 1})

    def test_numeric_header_must_parse(self):
        with self.assertRaisesRegex(ValueError, "Unparsed numeric"):
            inspect_source(b"<f1r> page\n<f2x.1> invalid\n")

    def test_named_header_must_parse(self):
        with self.assertRaisesRegex(ValueError, "Unparsed named"):
            inspect_source(b"<f1r> page\n<fRosx> invalid\n")

    def test_nonpositive_leaf_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Nonpositive"):
            inspect_source(b"<f0r> invalid\n<f1r.1,@P0> a\n")

    def test_orphan_and_cross_page_loci_rejected(self):
        # A locus alone must never manufacture an eligible physical leaf.
        with self.assertRaisesRegex(ValueError, "Orphan or mismatched"):
            inspect_source(b"<f9r.1,@P0> orphan\n")
        with self.assertRaisesRegex(ValueError, "Orphan or mismatched"):
            inspect_source(b"<f1r> page\n<f2r.1,@P0> wrong page\n")

    def test_glued_suffix_and_malformed_page_tags_rejected(self):
        # The former prefix-matching regex counted each of these as a page.
        for broken in (b"<f9r>garbage", b"<f9r><!comment>",
                       b"<f9r7> bad panel", b"<f9r,> bad header",
                       b"<f9r.1> missing locus metadata"):
            with self.subTest(broken=broken):
                with self.assertRaisesRegex(ValueError, "Malformed|Unparsed"):
                    inspect_source(b"<f1r> good\n" + broken + b"\n")

    def test_valid_header_and_locus_control(self):
        result = inspect_source(
            b"<f1r> metadata\n<f1r.1,@P0> body\n"
            b"<f2v1> metadata\n<f2v1.2,+P0> body\n"
            b"<fRos> metadata\n<fRos.1,@L0> label\n"
        )
        self.assertEqual(result["numeric_leaves"], [1, 2])
        self.assertEqual(result["numeric_page_header_count"], 2)
        self.assertEqual(result["numeric_locus_record_count"], 2)
        self.assertEqual(result["named_locus_record_count"], 1)

    def test_same_size_train_test_swap_is_rejected(self):
        # Previously passed every count/union/provenance check, but changes
        # which folio is held out and invalidates the locked evaluation.
        self.manifest["partitions"]["train"] = [3]
        self.manifest["partitions"]["test"] = [1]
        with self.assertRaisesRegex(ValueError, "Partition hash assignment mismatch"):
            audit(self.sources, self.manifest)

    def test_frozen_salt_cannot_be_changed_or_removed(self):
        for salt in ("different-salt", None):
            with self.subTest(salt=salt):
                self.manifest["salt"] = salt
                with self.assertRaisesRegex(ValueError, "Frozen partition salt mismatch"):
                    audit(self.sources, self.manifest)

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
