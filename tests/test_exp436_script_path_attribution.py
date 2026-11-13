"""Regression for EXP-436 source-path attribution; no corpus or historical replay.

Run: python -m unittest tests.test_exp436_script_path_attribution
The historical English source identity is a documented archival fact, not
proof that the present script generated the frozen result.
"""
import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments" / "exp_436_latin_hapax_length"
ARCHIVED_ENGLISH_NAME = "caesar_gallic_wars.txt"
CURRENT_SCRIPT_NAME = "caesar_de_bello_gallico_latin.txt"


class Exp436PathAttributionTests(unittest.TestCase):
    def test_current_script_is_not_archived_english_input_path(self):
        source = (EXP / "script.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        # Inspect string literals only: never import/execute the frozen script.
        literals = {node.value for node in ast.walk(tree)
                    if isinstance(node, ast.Constant) and isinstance(node.value, str)}
        self.assertIn("data/reference_corpora/latin/" + CURRENT_SCRIPT_NAME, literals)
        self.assertNotIn("data/reference_corpora/latin/" + ARCHIVED_ENGLISH_NAME, literals)

    def test_errata_preserves_both_distinct_source_names_and_claim_scope(self):
        correction = (EXP / "CORRECTION.md").read_text(encoding="utf-8")
        self.assertIn(ARCHIVED_ENGLISH_NAME, correction)
        self.assertIn(CURRENT_SCRIPT_NAME, correction)
        self.assertIn("INVALID_FOR_CLAIM", correction)
        self.assertIn("no demuestra que el script actualmente consultado", correction)


if __name__ == "__main__":
    unittest.main()
