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

    def test_unreadable_candidate_is_reported_not_silently_ignored(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "broken.md").write_bytes(bytes([0xFF, 0xFE]) + b"EXP-177")
            with self.assertRaises(UnicodeDecodeError):
                (root / "broken.md").read_text(encoding="utf-8")
            result = scan(root, self.registry)
            self.assertFalse(result["coverage_complete_for_selected_files"])
            self.assertEqual(result["unreadable_files"], [
                {"path": "broken.md", "error_type": "UnicodeDecodeError"}
            ])

    def test_raw_corpora_are_excluded_not_mislabeled_as_broken_reports(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            corpus = root / "data" / "transcriptions" / "v101_claston.txt"
            corpus.parent.mkdir(parents=True)
            corpus.write_bytes(bytes([0xFF, 0xFE]) + b"EXP-177")
            reference = root / "data" / "reference_corpora" / "latin" / "caesar.txt"
            reference.parent.mkdir(parents=True)
            reference.write_bytes(bytes([0xFF]) + b"EXP-177")
            (root / "report.md").write_text("EXP-177", encoding="utf-8")
            result = scan(root, self.registry)
            self.assertEqual(result["occurrences"], 1)
            self.assertEqual(result["unreadable_files"], [])
            self.assertEqual(result["excluded_raw_corpora"], [
                "data/reference_corpora/latin/caesar.txt",
                "data/transcriptions/v101_claston.txt",
            ])
            self.assertTrue(result["coverage_complete_for_selected_files"])

    def test_symlink_cannot_leak_outside_checkout(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "checkout"
            root.mkdir()
            outside = Path(temp) / "outside.txt"
            outside.write_text("EXP-177", encoding="utf-8")
            (root / "link.txt").symlink_to(outside)
            result = scan(root, self.registry)
            self.assertEqual(result["occurrences"], 0)
            self.assertEqual(result["skipped_symlinks"], ["link.txt"])
            self.assertFalse(result["coverage_complete_for_selected_files"])

    def test_symlinked_directory_does_not_falsely_certify_coverage(self):
        # pathlib.rglob does not traverse directory symlinks in Python 3.12.
        # The old suffix-first filter missed the extensionless link itself.
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp)
            root = parent / "checkout"
            root.mkdir()
            outside = parent / "reports"
            outside.mkdir()
            (outside / "archived.md").write_text("EXP-177", encoding="utf-8")
            (root / "linked_reports").symlink_to(outside, target_is_directory=True)
            result = scan(root, self.registry)
            self.assertEqual(result["occurrences"], 0)
            self.assertEqual(result["skipped_symlinks"], ["linked_reports"])
            self.assertFalse(result["coverage_complete_for_selected_files"])

    def test_broken_extensionless_link_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "missing_reports").symlink_to(root / "absent", target_is_directory=True)
            result = scan(root, self.registry)
            self.assertEqual(result["skipped_symlinks"], ["missing_reports"])
            self.assertFalse(result["coverage_complete_for_selected_files"])

    def test_nonreport_file_symlink_does_not_change_selected_coverage(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "script.py"
            target.write_text("EXP-177", encoding="utf-8")
            (root / "link.py").symlink_to(target)
            result = scan(root, self.registry)
            self.assertEqual(result["skipped_symlinks"], [])
            self.assertTrue(result["coverage_complete_for_selected_files"])

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
