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
               b"<f67v2.2,+P0> def\n<f68r2.1> ghi\n"
               b"<f69r.1> jkl\n")
        self.assertEqual(v1.leaves_from_bytes(raw), {69})
        self.assertEqual(v2.leaves_from_bytes(raw), {67, 68, 69})

    def test_no_reassignment_of_v1_folios(self):
        old = json.loads(V1_MANIFEST.read_text(encoding="utf-8"))
        old_leaves = set().union(*(set(x) for x in old["partitions"].values()))
        self.assertEqual(len(old_leaves), 92)
        regular = [f"<f{n}r.1> sample" for n in sorted(old_leaves)]
        panels = [f"<f{n}r1.1> sample" for n in sorted(MISSING_V1)]
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
