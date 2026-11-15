#!/usr/bin/env python3
"""Regression tests for historical EXP-580 inventory exporter (no semantic claims)."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/export_exp580_label_inventory.py"
spec = importlib.util.spec_from_file_location("exp580_inventory", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class HistoricalInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = module.build()

    def test_counts_and_order(self):
        report = self.report
        self.assertEqual(report["summary"]["exclusive_types"], 547)
        self.assertEqual(len(report["inventory"]), 547)
        words = [x["eva"] for x in report["inventory"]]
        self.assertEqual(words, sorted(words))
        self.assertEqual(len(words), len(set(words)))

    def test_occurrence_consistency(self):
        report = self.report
        inventory = report["inventory"]
        self.assertEqual(sum(x["count"] for x in inventory), report["summary"]["exclusive_tokens"])
        for row in inventory:
            self.assertGreater(row["count"], 0)
            self.assertEqual(row["count"], len(row["occurrences"]))
            self.assertTrue(row["eva"].isascii() and row["eva"].isalpha() and row["eva"].islower())
            for occurrence in row["occurrences"]:
                self.assertTrue(occurrence["folio"].startswith("f"))
                self.assertTrue(occurrence["locus"])

    def test_provenance_and_scope(self):
        report = self.report
        self.assertEqual(report["status"], "HISTORICAL_PARSER_REPLAY_NOT_INDEPENDENT")
        self.assertEqual(len(report["source_script_sha256"]), 64)
        self.assertEqual(len(report["source_corpus_sha256"]), 64)
        self.assertTrue(report["limitations"])


if __name__ == "__main__":
    unittest.main()
