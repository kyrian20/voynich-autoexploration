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
        observed = {}
        tests = {}
        for word, n, initial, final in (("daiin", 3, 1, 1),
                                         ("dain", 2, 1, 0),
                                         ("daiiin", 0, 0, 0)):
            observed[word] = {
                "occurrences": n, "line_initial": initial, "line_final": final,
                "initial_fraction": initial / n if n else None,
                "by_currier": {"A": {"occurrences": n,
                                    "line_initial": initial, "line_final": final}},
            }
            tests[word] = {"null_mean_initial": 0.5, "null_sd_initial": 0.5,
                           "observed_standardized_statistic": 1.0,
                           "empirical_p": 0.2, "max_stat_adjusted_p": 0.3}
        return {"experiment": "EXP-593", "date_utc": DATE,
                "source": "data/transcriptions/eva_zl3b.txt",
                "source_sha256": SOURCE_SHA,
                "seed": MODULE["SEED"] if seed is None else seed,
                "permutations": MODULE["N_PERM"],
                "variants": list(MODULE["VARIANTS"]),
                "lines": 4188, "tokens": 32732, "observed": observed,
                "tests": tests, "null_model": "synthetic test fixture",
                "limitations": ["synthetic test fixture; no permutations run"]}

    def report(self, *, source_sha=SOURCE_SHA):
        payload = self.payload()
        lines = (f"# EXP-593\n\n- Fecha UTC: {DATE}\n"
                 f"- SHA-256: {source_sha}\n"
                 f"- Líneas: {payload['lines']:,}\n"
                 f"- Tokens: {payload['tokens']:,}\n"
                 f"- Permutaciones: {MODULE['N_PERM']:,}\n"
                 f"- Semilla: {MODULE['SEED']}\n\n")
        for word in MODULE["VARIANTS"]:
            o, t = payload["observed"][word], payload["tests"][word]
            lines += (f"| {word} | {o['occurrences']} | {o['line_initial']} | "
                      f"{o['line_final']} | {t['empirical_p']:.6f} | "
                      f"{t['max_stat_adjusted_p']:.6f} |\n")
        lines += "\n## Distribución por clase Currier\n\n"
        for word in MODULE["VARIANTS"]:
            lines += (f"### {word}\n\n| Clase | Ocurrencias | Inicio | Final |\n"
                      "|---|---:|---:|---:|\n")
            for name, values in payload["observed"][word]["by_currier"].items():
                lines += (f"| {name} | {values['occurrences']} | "
                          f"{values['line_initial']} | {values['line_final']} |\n")
            lines += "\n"
        return lines

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

    def test_metadata_only_archive_cannot_be_mistaken_for_complete(self):
        partial = self.payload()
        del partial["observed"]
        del partial["tests"]
        self.store(payload=partial)
        with self.assertRaisesRegex(RuntimeError, "result body is incomplete"):
            MODULE["archive_status"](self.paths, DATE, SOURCE_SHA)

    def test_missing_variant_statistics_rejected(self):
        partial = self.payload()
        del partial["tests"]["dain"]
        self.store(payload=partial)
        with self.assertRaisesRegex(RuntimeError, "result body is incomplete"):
            MODULE["archive_status"](self.paths, DATE, SOURCE_SHA)

    def test_invalid_probability_rejected(self):
        partial = self.payload()
        partial["tests"]["daiin"]["empirical_p"] = float("nan")
        self.store(payload=partial)
        with self.assertRaisesRegex(RuntimeError, "result body is incomplete"):
            MODULE["archive_status"](self.paths, DATE, SOURCE_SHA)

    def test_mismatched_currier_totals_rejected(self):
        partial = self.payload()
        partial["observed"]["daiin"]["by_currier"]["A"]["occurrences"] = 2
        self.store(payload=partial)
        with self.assertRaisesRegex(RuntimeError, "result body is incomplete"):
            MODULE["archive_status"](self.paths, DATE, SOURCE_SHA)

    def test_report_table_must_match_json(self):
        self.store(report=self.report().replace("| daiin | 3 |", "| daiin | 999 |"))
        with self.assertRaisesRegex(RuntimeError, "result body is incomplete"):
            MODULE["archive_status"](self.paths, DATE, SOURCE_SHA)

    def test_currier_label_mismatch_with_same_totals_rejected(self):
        # Before the repair, the report's A row could disagree with JSON's B
        # label while every aggregate and summary-table check still passed.
        altered = self.payload()
        by = altered["observed"]["daiin"]["by_currier"]
        by["B"] = by.pop("A")
        self.store(payload=altered)
        with self.assertRaisesRegex(RuntimeError, "result body is incomplete"):
            MODULE["archive_status"](self.paths, DATE, SOURCE_SHA)

    def test_missing_currier_report_row_rejected(self):
        self.store(report=self.report().replace("| A | 3 | 1 | 1 |\\n", "", 1))
        with self.assertRaisesRegex(RuntimeError, "result body is incomplete"):
            MODULE["archive_status"](self.paths, DATE, SOURCE_SHA)

    def test_duplicate_currier_report_row_rejected(self):
        row = "| A | 3 | 1 | 1 |\\n"
        self.store(report=self.report().replace(row, row + row, 1))
        with self.assertRaisesRegex(RuntimeError, "result body is incomplete"):
            MODULE["archive_status"](self.paths, DATE, SOURCE_SHA)

    def test_historical_oct21_archive_remains_compatible(self):
        paths = (ROOT / "research/experiments/2026-10-21-exp593-corrected-L-metadata.json",
                 ROOT / "research/experiments/2026-10-21-exp593-corrected-L-metadata.md")
        historical_sha = "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc"
        self.assertEqual(MODULE["archive_status"](paths, "2026-10-21", historical_sha), "existing")

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
