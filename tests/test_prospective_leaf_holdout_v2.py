"""Regression for panel-aware holdout v2; no manuscript text or EXP ID."""
import json
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import prepare_prospective_leaf_holdout as v1
import prepare_prospective_leaf_holdout_v2 as v2

V1_MANIFEST = (ROOT / "research/decipherment/"
               "2026-10-23-prospective-leaf-holdout/manifest.json")
MISSING_V1 = {67, 68, 70, 72, 85, 86, 89, 90, 95, 102}


class PanelAwareHoldout(unittest.TestCase):
    def test_multi_panel_folio_identifiers(self):
        raw = (b"<f67r1> metadata\n<f67r1.1,@P0> abc\n"
               b"<f67v2> metadata\n<f67v2.2,+P0> def\n"
               b"<f68r2> metadata\n<f68r2.1> ghi\n"
               b"<f69r> metadata\n<f69r.1> jkl\n")
        self.assertEqual(v1.leaves_from_bytes(raw), {69})
        self.assertEqual(v2.leaves_from_bytes(raw), {67, 68, 69})

    def test_only_page_headers_qualify(self):
        # The previous broad pattern admitted record IDs, damaged page
        # boundaries and impossible panels as if they were valid headers.
        raw = (b"<f1r.1,@P0> orphan locus\n"
               b"<f2r7> invalid panel\n"
               b"<f3r,> damaged page\n"
               b"<f4r> real page\n"
               b"<f4r.1,@P0> record\n"
               b"<fRos> named page excluded\n")
        self.assertEqual(v2.leaves_from_bytes(raw), {4})

    def test_page_tag_requires_boundary_after_closing_bracket(self):
        # Prefix matching previously admitted malformed glued suffixes as
        # valid page headers, creating phantom eligible leaves.
        raw = (b"<f67r1>garbage\n"
               b"<f68r><! $L=B>\n"
               b"<f69r> <! $L=A>\n"
               b"<f70r>\n"
               b"<f71r.1,@P0> orphan locus\n")
        self.assertEqual(v2.leaves_from_bytes(raw), {69, 70})
        with self.assertRaisesRegex(ValueError, "No folio headers"):
            v2.leaves_from_bytes(b"<f67r>garbage\n<f68r><!comment>\n")

    def test_orphan_loci_cannot_create_holdout_leaf(self):
        with self.assertRaisesRegex(ValueError, "No folio headers"):
            v2.leaves_from_bytes(b"<f67r1.1,@P0> orphan\n<f69r.2,@P0> orphan\n")

    def test_unicode_digit_page_cannot_create_leaf(self):
        raw = "<f١r> invalid\n<f4r> valid\n".encode("utf-8")
        self.assertEqual(v2.leaves_from_bytes(raw), {4})

    def test_no_reassignment_of_v1_folios(self):
        old = json.loads(V1_MANIFEST.read_text(encoding="utf-8"))
        old_leaves = set().union(*(set(x) for x in old["partitions"].values()))
        self.assertEqual(len(old_leaves), 92)
        regular = [f"<f{n}r> sample" for n in sorted(old_leaves)]
        panels = [f"<f{n}r1> sample" for n in sorted(MISSING_V1)]
        raw = ("\n".join(regular + panels) + "\n").encode()
        new = v2.build_manifest({name: raw for name in v2.SOURCE_NAMES})
        self.assertEqual(new["eligible_count"], 102)
        for group, old_members in old["partitions"].items():
            self.assertEqual(set(old_members) & set(new["partitions"][group]),
                             set(old_members))
        all_new = set().union(*(set(x) for x in new["partitions"].values()))
        self.assertEqual(all_new - old_leaves, MISSING_V1)
        self.assertEqual(sum(new["counts"].values()), 102)
        self.assertEqual(new["salt"], old["salt"])

    def test_reject_missing_source(self):
        with self.assertRaises(ValueError):
            v2.build_manifest({"eva_zl3b.txt": b"<f67r1.1> abc\n"})


if __name__ == "__main__":
    unittest.main()
