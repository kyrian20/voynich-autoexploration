"""Frozen visual-pilot partition gate: exact historical inputs, no semantic test.

Regression fixtures mutate only temporary manifest copies. Corpus and frozen
manifest in the repository are read-only; no EXP identifier is assigned.
"""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.audit_holdout_locus_coverage import MANIFEST, ROOT
from scripts.select_visual_pilot_v2 import load_verified_frozen_manifest


class FrozenVisualPilotManifestTests(unittest.TestCase):
    def test_committed_manifest_passes_independent_frozen_split_audit(self):
        manifest = load_verified_frozen_manifest(MANIFEST, ROOT)
        self.assertEqual(manifest["schema_version"], 2)
        self.assertEqual(manifest["eligible_count"], 102)

    def test_same_size_train_test_swap_fails_even_when_counts_stay_valid(self):
        manifest = copy.deepcopy(json.loads(MANIFEST.read_text(encoding="utf-8")))
        train = manifest["partitions"]["train"]
        test = manifest["partitions"]["test"]
        self.assertTrue(train and test)
        train[0], test[0] = test[0], train[0]
        train.sort()
        test.sort()
        self.assertEqual(len(train), manifest["counts"]["train"])
        self.assertEqual(len(test), manifest["counts"]["test"])
        self.assertEqual(len(set(train) & set(test)), 0)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "swapped.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Partition hash assignment mismatch"):
                load_verified_frozen_manifest(path, ROOT)

    def test_duplicate_manifest_keys_fail_before_pilot_selection(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.json"
            path.write_text('{"salt":"first","salt":"second"}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Duplicate holdout manifest JSON key"):
                load_verified_frozen_manifest(path, ROOT)

    def test_false_source_hash_fails_before_pilot_selection(self):
        manifest = copy.deepcopy(json.loads(MANIFEST.read_text(encoding="utf-8")))
        source = next(iter(manifest["corpora"].values()))
        source["sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "forged-source.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Source provenance mismatch"):
                load_verified_frozen_manifest(path, ROOT)


if __name__ == "__main__":
    unittest.main()
