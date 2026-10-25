#!/usr/bin/env python3
"""EXP-593 output preservation regression; never reruns 5,000 permutations."""
from __future__ import annotations

import json
import runpy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
MODULE = runpy.run_path(str(ROOT / "scripts/exp593_daiin_variants.py"),
                        run_name="exp593_archive_guard_test")
DATE = "2026-10-25"
SOURCE_SHA = "a" * 64


class Exp593ArchiveGuardTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name)
        scope = patch.dict(MODULE["archive_paths"].__globals__, {"OUT": self.out})
        scope.start()
        self.addCleanup(scope.stop)
        self.paths = MODULE["archive_paths"](DATE)

    def payload(self, *, seed=None):
        return {"experiment": "EXP-593", "date_utc": DATE,
                "source": "data/transcriptions/eva_zl3b.txt",
                "source_sha256": SOURCE_SHA,
                "seed": MODULE["SEED"] if seed is None else seed,
                "permutations": MODULE["N_PERM"],
                "variants": list(MODULE["VARIANTS"])}

    def report(self, *, source_sha=SOURCE_SHA):
        return (f"# EXP-593\n\n- Fecha UTC: {DATE}\n"
                f"- SHA-256: {source_sha}\n"
                f"- Permutaciones: {MODULE['N_PERM']:,}\n"
                f"- Semilla: {MODULE['SEED']}\n")

    def store(self, *, payload=None, report=None):
        self.paths[0].write_text(json.dumps(self.payload() if payload is None else payload),
                                 encoding="utf-8")
        self.paths[1].write_text(self.report() if report is None else report,
                                 encoding="utf-8")

    def test_fresh_destination_can_be_created(self):
        self.assertEqual(MODULE["archive_status"](self.paths, DATE, SOURCE_SHA), "new")
        MODULE["write_archive_pair"](self.paths, "new-json", "new-report")
        self.assertEqual(self.paths[0].read_text(), "new-json")
        self.assertEqual(self.paths[1].read_text(), "new-report")

    def test_complete_matching_archive_skips_without_mutation(self):
        self.store()
        before = [path.read_bytes() for path in self.paths]
        self.assertEqual(MODULE["archive_status"](self.paths, DATE, SOURCE_SHA), "existing")
        self.assertEqual([path.read_bytes() for path in self.paths], before)

    def test_partial_archive_fails_closed(self):
        self.paths[0].write_text("historic-json", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "incomplete"):
            MODULE["archive_status"](self.paths, DATE, SOURCE_SHA)
        self.assertEqual(self.paths[0].read_text(), "historic-json")

    def test_mismatched_seed_is_not_accepted_as_reproduction(self):
        self.store(payload=self.payload(seed=123))
        with self.assertRaisesRegex(RuntimeError, "provenance differs"):
            MODULE["archive_status"](self.paths, DATE, SOURCE_SHA)

    def test_mismatched_report_is_not_accepted(self):
        self.store(report=self.report(source_sha="b" * 64))
        with self.assertRaisesRegex(RuntimeError, "report provenance differs"):
            MODULE["archive_status"](self.paths, DATE, SOURCE_SHA)

    def test_unreadable_json_is_not_silently_replaced(self):
        self.store()
        self.paths[0].write_text("{invalid", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "cannot be read"):
            MODULE["archive_status"](self.paths, DATE, SOURCE_SHA)

    def test_symlink_destination_rejected(self):
        target = self.out / "outside.txt"
        target.write_text("do-not-touch", encoding="utf-8")
        self.paths[0].symlink_to(target)
        with self.assertRaisesRegex(RuntimeError, "symlink"):
            MODULE["archive_status"](self.paths, DATE, SOURCE_SHA)
        self.assertEqual(target.read_text(), "do-not-touch")

    def test_exclusive_write_cannot_replace_existing_json(self):
        self.paths[0].write_text("historic-json", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            MODULE["write_archive_pair"](self.paths, "new-json", "new-report")
        self.assertEqual(self.paths[0].read_text(), "historic-json")
        self.assertFalse(self.paths[1].exists())


if __name__ == "__main__":
    unittest.main()
