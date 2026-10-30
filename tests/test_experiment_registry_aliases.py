#!/usr/bin/env python3
"""Regression guard for ambiguous historical experiment aliases.

Checks registry consistency without renaming experiments or interpreting results.
"""
import json
import re
import unittest
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "research/EXPERIMENT_PATH_REGISTRY.json"


class ExperimentAliasRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    def test_canonical_paths_and_numeric_aliases(self):
        entries = self.registry["entries"]
        self.assertEqual(len(entries), len({e["canonical_id"] for e in entries}))
        self.assertEqual(len(entries), len({e["path"] for e in entries}))
        for e in entries:
            self.assertEqual(e["canonical_id"], "GH:" + e["path"])
            match = re.fullmatch(r"experiments/exp_(\d+)_.+", e["path"])
            self.assertIsNotNone(match, e["path"])
            self.assertEqual(e["legacy_numeric_id"], int(match.group(1)))

    def test_all_collisions_are_explicit_and_unambiguous(self):
        by_number = defaultdict(list)
        for entry in self.registry["entries"]:
            by_number[str(entry["legacy_numeric_id"])].append(entry["canonical_id"])
        computed = {number: paths for number, paths in by_number.items() if len(paths) > 1}
        self.assertEqual(self.registry["numeric_collisions"], computed)
        for number, paths in computed.items():
            self.assertGreater(len(paths), 1, number)
            self.assertEqual(len(paths), len(set(paths)))

    def test_registry_matches_directories(self):
        expected = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "experiments").iterdir()
            if path.is_dir() and re.fullmatch(r"exp_\d+_.+", path.name)
        }
        actual = {entry["path"] for entry in self.registry["entries"]}
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
