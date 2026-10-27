"""Reject ambiguous JSON in the frozen physical-leaf holdout manifest.

Synthetic fixtures only; no corpus, holdout split, or historical result changes.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_holdout_locus_coverage import FROZEN_SALT, load_manifest


class HoldoutManifestJsonIntegrity(unittest.TestCase):
    def load_fixture(self, source):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.json"
            path.write_text(source, encoding="utf-8")
            return load_manifest(path)

    def test_duplicate_top_level_salt_rejected(self):
        source = '{"salt":"wrong","salt":"correct"}'
        # The previous json.loads() silently selected the last assignment.
        self.assertEqual(json.loads(source)["salt"], "correct")
        with self.assertRaisesRegex(ValueError, "Duplicate holdout manifest JSON key: salt"):
            self.load_fixture(source)

    def test_duplicate_partition_group_rejected(self):
        source = '{"partitions":{"train":[1],"train":[3]}}'
        with self.assertRaisesRegex(ValueError, "Duplicate holdout manifest JSON key: train"):
            self.load_fixture(source)

    def test_duplicate_nested_source_hash_rejected(self):
        source = '{"corpora":{"eva_zl3b.txt":{"sha256":"old","sha256":"new"}}}'
        with self.assertRaisesRegex(ValueError, "Duplicate holdout manifest JSON key: sha256"):
            self.load_fixture(source)

    def test_duplicate_identical_member_still_rejected(self):
        source = '{"counts":{"test":18,"test":18}}'
        with self.assertRaisesRegex(ValueError, "Duplicate holdout manifest JSON key: test"):
            self.load_fixture(source)

    def test_unambiguous_json_and_frozen_manifest_accepted(self):
        self.assertEqual(self.load_fixture('{"salt":"s","counts":{"test":18}}'),
                         {"salt": "s", "counts": {"test": 18}})
        frozen = load_manifest()
        self.assertEqual(frozen["schema_version"], 2)
        self.assertEqual(frozen["salt"], FROZEN_SALT)
        self.assertEqual(frozen["eligible_count"], 102)
        self.assertEqual(set(frozen["partitions"]), {"train", "development", "test"})


if __name__ == "__main__":
    unittest.main()
