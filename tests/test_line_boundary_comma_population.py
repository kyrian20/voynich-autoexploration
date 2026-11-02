#!/usr/bin/env python3
"""Regressions for the non-predictive comma population census."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "research/analysis/2026-10-28-line-boundary-reproduction/audit_comma_population.py"
spec = importlib.util.spec_from_file_location("audit_comma_population", SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError("Missing census script")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class PopulationCensusTests(unittest.TestCase):
    def test_comma_counterfactual_keeps_uncertainty_explicit(self):
        t = audit.reader.tokens
        self.assertEqual(
            t("aa,bb.cc", preserve_gaps=True, uncertain_space_policy="quarantine"),
            [None, "cc"],
        )
        self.assertEqual(
            t("aa,bb.cc", preserve_gaps=True, uncertain_space_policy="split"),
            ["aa", "bb", "cc"],
        )
        self.assertEqual(
            t("aa.bb", preserve_gaps=True, uncertain_space_policy="quarantine"),
            ["aa", "bb"],
        )

    def test_frozen_source_census_and_historical_scope(self):
        result = audit.compute()
        self.assertEqual(result["status"], "DESCRIPTIVE_NOT_HISTORICAL_REPLAY")
        self.assertFalse(result["reads_heldout_labels_or_predictor_scores"])
        self.assertIsNone(result["random_seed"])
        for label, expected in audit.EXPECTED.items():
            observed = result["sources"][label]
            for key, value in expected.items():
                self.assertEqual(observed[key], value, f"{label}.{key}")
            self.assertEqual(
                observed["archived_reported_not_reproduced"],
                audit.ARCHIVED_REPORTED_COUNTS[label],
            )
            self.assertEqual(
                observed["split"]["accepted"] - observed["quarantine"]["accepted"],
                observed["accepted_delta_split_minus_quarantine"],
            )

    def test_source_mutation_rejected_before_census(self):
        with tempfile.TemporaryDirectory() as td:
            altered = Path(td) / "altered.ivtff"
            altered.write_text("<f1r>\n<f1r.1,@P0> aa,bb\n", encoding="latin-1")
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                audit.census("ZL3b", altered)


if __name__ == "__main__":
    unittest.main()
