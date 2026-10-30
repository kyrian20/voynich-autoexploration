"""Regression tests for immutable, date-stamped EXP-590 archives.

The 2026-10-27 JSON/Markdown pair is a frozen fixture; tests do not run
permutations, edit historical data, or infer scientific validity.
"""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import exp590_daiin_position as exp590


FIXTURE_DATE = "2026-10-27"
FIXTURE_JSON, FIXTURE_MD = exp590.archive_paths(FIXTURE_DATE)


class Exp590ArchiveGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.paths = (root / "archive.json", root / "archive.md")
        for src, dest in zip((FIXTURE_JSON, FIXTURE_MD), self.paths):
            shutil.copyfile(src, dest)
        self.source_sha = json.loads(self.paths[0].read_text(encoding="utf-8"))["source_sha256"]

    def check(self):
        return exp590.archive_status(self.paths, FIXTURE_DATE, self.source_sha)

    def edit_json(self, edit):
        value = json.loads(self.paths[0].read_text(encoding="utf-8"))
        edit(value)
        self.paths[0].write_text(json.dumps(value), encoding="utf-8")

    def test_original_frozen_pair_is_recognized_without_reexecution(self):
        self.assertEqual(self.check(), "existing")

    def test_new_destination_is_recognized(self):
        for path in self.paths:
            path.unlink()
        self.assertEqual(self.check(), "new")

    def test_partial_pair_is_rejected(self):
        self.paths[1].unlink()
        with self.assertRaisesRegex(RuntimeError, "partial"):
            self.check()

    def test_source_hash_mismatch_is_rejected(self):
        self.edit_json(lambda data: data.__setitem__("source_sha256", "0" * 64))
        with self.assertRaisesRegex(RuntimeError, "provenance"):
            self.check()

    def test_duplicate_json_keys_are_rejected(self):
        raw = self.paths[0].read_text(encoding="utf-8")
        self.paths[0].write_text(raw.replace('  "experiment": "EXP-590",',
                                                '  "experiment": "EXP-590",\n  "experiment": "EXP-590",', 1),
                                     encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "ambiguous"):
            self.check()

    def test_currier_reassignment_is_rejected_even_if_totals_unchanged(self):
        def mutate(data):
            data["metrics"]["currier"]["A"]["line_initial_lines"] += 1
            data["metrics"]["currier"]["B"]["line_initial_lines"] -= 1
        self.edit_json(mutate)
        with self.assertRaisesRegex(RuntimeError, "report disagrees"):
            self.check()

    def test_truncated_report_is_rejected(self):
        self.paths[1].write_text("# incomplete\n", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "report disagrees"):
            self.check()

    def test_permutation_settings_mismatch_is_rejected(self):
        self.edit_json(lambda data: data["permutation_test"].__setitem__("seed", 0))
        with self.assertRaisesRegex(RuntimeError, "settings"):
            self.check()

    def test_impossible_counts_are_rejected(self):
        self.edit_json(lambda data: data["metrics"].__setitem__("line_initial_occurrences", 10000))
        with self.assertRaisesRegex(RuntimeError, "impossible"):
            self.check()

    def test_existing_destination_is_not_overwritten(self):
        before = [p.read_bytes() for p in self.paths]
        with self.assertRaises(FileExistsError):
            exp590.write_archive_pair(self.paths, "tampered", "tampered")
        self.assertEqual(before, [p.read_bytes() for p in self.paths])

    def test_symlink_destination_is_rejected(self):
        self.paths[0].unlink()
        self.paths[0].symlink_to(self.paths[1])
        with self.assertRaisesRegex(RuntimeError, "symlink"):
            self.check()


if __name__ == "__main__":
    unittest.main()
