"""Guard against silent omission of nonnumeric loci in a numeric-leaf holdout.

Synthetic fixtures only: original corpus and frozen v2 manifest are never edited.
"""
import hashlib
import copy
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_holdout_locus_coverage import (
    audit as frozen_audit, inspect_source, FROZEN_SALT, FROZEN_CONTRACT,
    FROZEN_SOURCE_SHA256,
)


def audit(sources, manifest):
    """Existing synthetic fixtures explicitly bypass only the original-byte lock."""
    return frozen_audit(sources, manifest, enforce_frozen_source_hashes=False)


class HoldoutLocusCoverageTests(unittest.TestCase):
    def setUp(self):
        self.sources = {
            "eva_zl3b.txt": b"<f1r> metadata\n<f1r.1,@P0> a\n<f4v1> metadata\n<f4v1.2,@P0> b\n<f3r> metadata\n<f3r.1,@P0> c\n<fRos> metadata\n<fRos.1,@L0> d\n",
            "eva_it2a.txt": b"<f1r> metadata\n<f1r.1,@P0> a\n<f4v1> metadata\n<f4v1.2,@P0> b\n<f3r> metadata\n<f3r.1,@P0> c\n",
        }
        self.manifest = {
            **copy.deepcopy(FROZEN_CONTRACT),
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

    def test_duplicate_physical_headers_fail_closed(self):
        # Previously the coverage reader counted both headers while its
        # set of page IDs and physical-leaf allocation remained unchanged.
        for page, locus in (
            ("f1r", "f1r.1,@P0"),
            ("f4v1", "f4v1.2,@P0"),
            ("fRos", "fRos.1,@L0"),
        ):
            with self.subTest(page=page):
                raw = (f"<{page}> first\n<{locus}> word\n"
                       f"<{page}> duplicate\n").encode("utf-8")
                with self.assertRaisesRegex(
                    ValueError, f"Duplicate physical folio header {page} at source line 3"
                ):
                    inspect_source(raw)

    def test_duplicate_locus_identifiers_fail_closed(self):
        # A second physical row with the same full locator used to inflate
        # record counts in this standalone reader; strict IVTFF rejects it.
        for tag in ("f1r.1,@P0", "f4v1.2,@P0", "fRos.1,@L0"):
            with self.subTest(tag=tag):
                page = tag.split(".", 1)[0]
                raw = (f"<{page}> page\n<{tag}> first\n"
                       f"<{tag}> duplicate\n").encode("utf-8")
                with self.assertRaisesRegex(ValueError, "Duplicate locus identifier"):
                    inspect_source(raw)

    def test_locus_number_bounds_match_strict_census(self):
        # The regex accepts three ASCII digits; IVTFF census additionally
        # requires physical record indices in the inclusive range 1..160.
        for number in (0, 161, 999):
            with self.subTest(number=number):
                raw = f"<f1r> page\n<f1r.{number},@P0> body\n".encode()
                with self.assertRaisesRegex(ValueError, "Locus number outside 1..160"):
                    inspect_source(raw)
        valid = inspect_source(b"<f1r> page\n<f1r.160,@P0> body\n")
        self.assertEqual(valid["numeric_locus_record_count"], 1)

    def test_matching_hash_cannot_hide_duplicate_locus(self):
        name = "eva_zl3b.txt"
        self.sources[name] += b"<f3r.1,@P0> duplicate\n"
        self.manifest["corpora"][name]["sha256"] = hashlib.sha256(
            self.sources[name]
        ).hexdigest()
        with self.assertRaisesRegex(ValueError, "Duplicate locus identifier"):
            audit(self.sources, self.manifest)

    def test_rehashed_manifest_cannot_hide_duplicate_header(self):
        # Adding a second header for the same page does not alter the
        # leaf intersection, salt, partitions, or manifest leaf counts.
        # A matching synthetic source SHA must not make this acceptable.
        name = "eva_zl3b.txt"
        self.sources[name] += b"<f1r> duplicate\n"
        self.manifest["corpora"][name]["sha256"] = hashlib.sha256(
            self.sources[name]
        ).hexdigest()
        with self.assertRaisesRegex(ValueError, "Duplicate physical folio header f1r"):
            audit(self.sources, self.manifest)

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

    def test_nonphysical_separator_cannot_forge_a_folio(self):
        # Before this guard, splitlines() treated these eight characters as
        # line endings and counted a fake <f2r> inside a physical comment.
        for separator in ("\v", "\f", "\x1c", "\x1d", "\x1e",
                          "\x85", "\u2028", "\u2029"):
            with self.subTest(codepoint=f"U+{ord(separator):04X}"):
                raw = (
                    "<f1r> metadata\n<f1r.1,@P0> a\n"
                    "# comment" + separator + "<f2r> forged\n"
                    "<f2r.1,@P0> b\n"
                ).encode("utf-8")
                with self.assertRaisesRegex(
                    ValueError, "Non-physical IVTFF line separator"
                ):
                    inspect_source(raw)

    def test_physical_cr_lf_crlf_are_accepted(self):
        for ending in ("\n", "\r", "\r\n"):
            with self.subTest(ending=repr(ending)):
                raw = ending.join((
                    "<f1r> metadata", "<f1r.1,@P0> a",
                    "<f2v1> metadata", "<f2v1.1,@P0> b",
                )).encode("utf-8")
                result = inspect_source(raw)
                self.assertEqual(result["numeric_leaves"], [1, 2])
                self.assertEqual(result["numeric_page_header_count"], 2)
                self.assertEqual(result["numeric_locus_record_count"], 2)

    def test_indented_structural_tags_are_rejected(self):
        # Before this repair, the coverage-only reader silently ignored
        # indented page and locus tags, undercounting physical source rows.
        for damaged in (
            b" <f2r> extra page\n",
            b"\t<f1r.2,@P0> extra locus\n",
        ):
            with self.subTest(damaged=damaged):
                with self.assertRaisesRegex(ValueError, "Indented folio tag"):
                    inspect_source(b"<f1r> page\n<f1r.1,@P0> body\n" + damaged)

    def test_slash_prefixed_structural_tags_are_rejected(self):
        # The coverage reader formerly skipped every slash continuation,
        # including a damaged page or locus tag. The strict IVTFF census
        # already diagnoses this; holdout coverage must reject it itself.
        for damaged in (
            b"/<f2r> hidden page\n",
            b"/ <f1r.2,@P0> hidden locus\n",
            b" \t/<fRos> hidden named page\n",
        ):
            with self.subTest(damaged=damaged):
                with self.assertRaisesRegex(
                    ValueError, "Folio tag hidden behind continuation slash"
                ):
                    inspect_source(b"<f1r> page\n<f1r.1,@P0> body\n" + damaged)

    def test_matching_hash_cannot_hide_slash_prefixed_locus(self):
        # A matching, synthetically rehashed manifest cannot make the
        # missing record count trustworthy.
        name = "eva_zl3b.txt"
        self.sources[name] = self.sources[name].replace(
            b"<f1r.1,@P0> a", b"/<f1r.1,@P0> a"
        )
        self.manifest["corpora"][name]["sha256"] = hashlib.sha256(
            self.sources[name]
        ).hexdigest()
        with self.assertRaisesRegex(
            ValueError, "Folio tag hidden behind continuation slash"
        ):
            audit(self.sources, self.manifest)

    def test_nonstructural_slash_continuations_remain_ignored(self):
        record = inspect_source(
            b"<f1r> page\n/<note> continuation\n/ ordinary text\n"
            b"<f1r.1,@P0> body\n"
        )
        self.assertEqual(record["numeric_page_header_count"], 1)
        self.assertEqual(record["numeric_locus_record_count"], 1)

    def test_matching_hash_cannot_hide_indented_locus(self):
        # The source checksum may match a synthetically modified manifest;
        # this does not make an omitted physical locus acceptable.
        name = "eva_zl3b.txt"
        self.sources[name] = self.sources[name].replace(
            b"<f1r.1,@P0>", b" <f1r.1,@P0>"
        )
        self.manifest["corpora"][name]["sha256"] = hashlib.sha256(
            self.sources[name]
        ).hexdigest()
        with self.assertRaisesRegex(ValueError, "Indented folio tag"):
            audit(self.sources, self.manifest)

    def test_non_ascii_whitespace_and_delimiter_locator_codes_are_rejected(self):
        # Former [^;>] accepted these malformed three-character locator
        # fields (and Unicode transcriber IDs) as valid holdout records.
        # They are synthetic structural controls, not manuscript data.
        for tag in (
            "f1r.1,éP0", "f1r.1,<P0", "f1r.1, P0",
            "f1r.1,@P0;é",
        ):
            with self.subTest(tag=tag):
                raw = ("<f1r> page\n<" + tag + "> body\n").encode("utf-8")
                with self.assertRaisesRegex(ValueError, "Unparsed numeric"):
                    inspect_source(raw)

    def test_audit_rejects_invalid_locator_even_with_matching_source_hash(self):
        # A source digest match alone must not certify a malformed record.
        name = "eva_zl3b.txt"
        self.sources[name] = self.sources[name].replace(
            b"<f1r.1,@P0>", b"<f1r.1,<P0>")
        self.manifest["corpora"][name]["sha256"] = hashlib.sha256(
            self.sources[name]).hexdigest()
        with self.assertRaisesRegex(ValueError, "Unparsed numeric"):
            audit(self.sources, self.manifest)

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

    def test_rehashed_source_and_manifest_cannot_redefine_frozen_holdout(self):
        # Prior to this fix, modifying the source AND its manifest SHA passed:
        # leaf membership and the partition salt remained unchanged.
        original_hashes = {name: hashlib.sha256(raw).hexdigest()
                           for name, raw in self.sources.items()}
        with patch.dict(FROZEN_SOURCE_SHA256, original_hashes):
            frozen_audit(self.sources, self.manifest)
            name = "eva_zl3b.txt"
            self.sources[name] += b"# synthetic changed source bytes\n"
            self.manifest["corpora"][name]["sha256"] = hashlib.sha256(
                self.sources[name]).hexdigest()
            # Demonstrate that the old, manifest-only gate would still accept.
            audit(self.sources, self.manifest)
            with self.assertRaisesRegex(ValueError, "Frozen source SHA-256 mismatch"):
                frozen_audit(self.sources, self.manifest)

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
