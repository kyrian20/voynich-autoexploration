#!/usr/bin/env python3
"""Adversarial tests for the read-only historical EXP alias triage."""
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_ambiguous_exp_references import PATTERN, collisions, scan


class AmbiguousReferenceAuditTests(unittest.TestCase):
    def setUp(self):
        self.registry = {
            "entries": [
                {"legacy_numeric_id": 177, "path": "experiments/exp_177_a"},
                {"legacy_numeric_id": 177, "path": "experiments/exp_177_b"},
                {"legacy_numeric_id": 200, "path": "experiments/exp_200_c"},
            ],
            "numeric_collisions": {
                "177": ["GH:experiments/exp_177_a", "GH:experiments/exp_177_b"]
            },
        }

    def test_collision_validation(self):
        self.assertEqual(len(collisions(self.registry)["177"]), 2)
        broken = dict(self.registry, numeric_collisions={})
        with self.assertRaises(ValueError):
            collisions(broken)

    def test_boundary_and_case(self):
        text = "EXP-177 exp_177 EXP 177 EXP177 EXP-1777 XEXP-177 EXP-200"
        self.assertEqual([int(m.group(1)) for m in PATTERN.finditer(text)], [177, 177, 177, 177, 1777, 200])

    def test_scan_flags_bare_but_not_explicit_path(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "note.md").write_text(
                "EXP-177 is ambiguous.\nEXP-177 experiments/exp_177_a\nEXP-200 is unique.\n",
                encoding="utf-8",
            )
            (root / "ignore.py").write_text("EXP-177\n", encoding="utf-8")
            result = scan(root, self.registry)
            self.assertEqual(result["occurrences"], 2)
            self.assertEqual(result["review_required"], 1)
            self.assertEqual(result["hits"][1]["classification"], "EXPLICIT_PATH_NEARBY")
            self.assertEqual(result["files_with_hits"], 1)


if __name__ == "__main__":
    unittest.main()
