"""Independent checks of committed prospective holdout manifests.

Does not import the partition generator or inspect Voynich text.
These checks complement, not replace, the CI byte-for-byte replay.
"""
import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "research/decipherment/2026-10-23-prospective-leaf-holdout"
GROUPS = ("train", "development", "test")
ADDED = {67, 68, 70, 72, 85, 86, 89, 90, 95, 102}


def load(name):
    return json.loads((BASE / name).read_text(encoding="utf-8"))


def assert_consistent(testcase, manifest):
    parts = manifest["partitions"]
    testcase.assertEqual(set(parts), set(GROUPS))
    all_leaves = []
    for group in GROUPS:
        leaves = parts[group]
        testcase.assertTrue(all(type(n) is int and n > 0 for n in leaves))
        testcase.assertEqual(leaves, sorted(leaves))
        testcase.assertEqual(len(leaves), len(set(leaves)))
        testcase.assertEqual(manifest["counts"][group], len(leaves))
        all_leaves.extend(leaves)
    testcase.assertEqual(len(all_leaves), len(set(all_leaves)),
                         "Physical leaf appears in multiple groups")
    testcase.assertEqual(manifest["eligible_count"], len(all_leaves))
    testcase.assertEqual(
        set(all_leaves),
        set(range(1, 117)) - {
            12, 59, 60, 61, 62, 63, 64, 74, 91, 92, 97, 98, 109, 110
        } if manifest["schema_version"] == 2 else set(all_leaves),
    )


class CommittedManifestInvariants(unittest.TestCase):
    def test_v1_and_v2_are_disjoint_and_complete(self):
        for name in ("manifest.json", "manifest-v2.json"):
            with self.subTest(name=name):
                assert_consistent(self, load(name))

    def test_v2_preserves_all_v1_assignments(self):
        old, new = load("manifest.json"), load("manifest-v2.json")
        self.assertEqual(old["schema_version"], 1)
        self.assertEqual(new["schema_version"], 2)
        self.assertEqual(old["salt"], new["salt"])
        self.assertEqual(old["eligible_count"], 92)
        self.assertEqual(new["eligible_count"], 102)
        for group in GROUPS:
            self.assertLessEqual(set(old["partitions"][group]),
                                 set(new["partitions"][group]))
        old_leaves = set().union(*(set(old["partitions"][g]) for g in GROUPS))
        new_leaves = set().union(*(set(new["partitions"][g]) for g in GROUPS))
        self.assertEqual(new_leaves - old_leaves, ADDED)
        self.assertEqual(old_leaves - new_leaves, set())


if __name__ == "__main__":
    unittest.main()
