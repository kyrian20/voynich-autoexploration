"""Regression: bracketed IVTFF uncertainty must not survive exclusion policy."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


SCRIPT = (Path(__file__).resolve().parents[1] / "research" / "analysis" /
          "2026-10-28-line-boundary-reproduction" / "line_boundary_replication.py")
spec = importlib.util.spec_from_file_location("line_boundary_replication", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class UncertaintyPolicyContract(unittest.TestCase):
    def test_primary_reading_unchanged(self):
        self.assertEqual(module.tokens("ab[cd:ef]gh", "primary"), ["abcdgh"])

    def test_bracket_alternative_embedded_word_excluded(self):
        self.assertEqual(module.tokens("ab[cd:ef]gh", "drop_uncertain_word"), [])

    def test_bracket_only_word_excluded(self):
        self.assertEqual(module.tokens("[cd:ef]", "drop_uncertain_word"), [])

    def test_bracket_without_alternative_excluded(self):
        self.assertEqual(module.tokens("ab[cd]gh", "drop_uncertain_word"), [])

    def test_neighbouring_certain_words_preserved(self):
        self.assertEqual(module.tokens("safe.ab[cd:ef]gh.clean", "drop_uncertain_word"),
                         ["safe", "clean"])

    def test_ligature_and_question_mark_still_excluded(self):
        self.assertEqual(module.tokens("ab{cd}gh", "drop_uncertain_word"), [])
        self.assertEqual(module.tokens("ab?gh", "drop_uncertain_word"), [])

    def test_certain_words_unchanged(self):
        self.assertEqual(module.tokens("safe.clean", "drop_uncertain_word"),
                         ["safe", "clean"])


if __name__ == "__main__":
    unittest.main()
