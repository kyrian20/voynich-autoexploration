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


def latin_corpus_literal(source):
    """Extract only the unique top-level LATIN_CORPUS path expression.

    This is a static attribution guard, not a historical execution replay.
    Fail closed if the declaration becomes ambiguous or dynamic.
    """
    tree = ast.parse(source)
    assignments = [
        node.value for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "LATIN_CORPUS"
                for target in node.targets)
    ]
    if len(assignments) != 1:
        raise ValueError("expected exactly one top-level LATIN_CORPUS assignment")
    value = assignments[0]
    if isinstance(value, ast.Constant) and isinstance(value.value, str):
        return value.value
    # Recognize only the actual static repository-relative construction.
    # A single string buried inside an arbitrary call is not sufficient.
    if (isinstance(value, ast.Call) and isinstance(value.func, ast.Name)
            and value.func.id == "str" and len(value.args) == 1
            and not value.keywords):
        path = value.args[0]
        if (isinstance(path, ast.BinOp) and isinstance(path.op, ast.Div)
                and ast.unparse(path.left) ==
                "_RepositoryPath(__file__).resolve().parents[2]"
                and isinstance(path.right, ast.Constant)
                and isinstance(path.right.value, str)):
            return path.right.value
    raise ValueError("LATIN_CORPUS must be a static repository-relative path")


class Exp436PathAttributionTests(unittest.TestCase):
    def test_current_script_is_not_archived_english_input_path(self):
        source = (EXP / "script.py").read_text(encoding="utf-8")
        literal = latin_corpus_literal(source)
        self.assertEqual(literal, "data/reference_corpora/latin/" + CURRENT_SCRIPT_NAME)
        self.assertNotEqual(literal, "data/reference_corpora/latin/" + ARCHIVED_ENGLISH_NAME)

    def test_unrelated_literal_cannot_mask_wrong_assignment(self):
        source = (
            'LATIN_CORPUS = "data/reference_corpora/latin/wrong.txt"\\n'
            'NOTE = "data/reference_corpora/latin/' + CURRENT_SCRIPT_NAME + '"\\n'
        ).replace("\\n", "\n")
        # Exercise the SAME extractor as the production regression, rather
        # than repeating a separate AST walk that could pass tautologically.
        self.assertEqual(latin_corpus_literal(source),
                         "data/reference_corpora/latin/wrong.txt")
        self.assertNotEqual(latin_corpus_literal(source),
                            "data/reference_corpora/latin/" + CURRENT_SCRIPT_NAME)

    def test_missing_or_ambiguous_assignment_fails_closed(self):
        with self.assertRaises(ValueError):
            latin_corpus_literal('NOTE = "data/reference_corpora/latin/' +
                                 CURRENT_SCRIPT_NAME + '"')
        with self.assertRaises(ValueError):
            latin_corpus_literal('LATIN_CORPUS = "a"\nLATIN_CORPUS = "b"')
        with self.assertRaises(ValueError):
            latin_corpus_literal('LATIN_CORPUS = choose("a", "b")')
        with self.assertRaises(ValueError):
            latin_corpus_literal('LATIN_CORPUS = choose("data/reference_corpora/latin/' +
                                 CURRENT_SCRIPT_NAME + '")')
        with self.assertRaises(ValueError):
            latin_corpus_literal('LATIN_CORPUS = str(other_root / "data/reference_corpora/latin/' +
                                 CURRENT_SCRIPT_NAME + '")')

    def test_errata_preserves_both_distinct_source_names_and_claim_scope(self):
        correction = (EXP / "CORRECTION.md").read_text(encoding="utf-8")
        self.assertIn(ARCHIVED_ENGLISH_NAME, correction)
        self.assertIn(CURRENT_SCRIPT_NAME, correction)
        self.assertIn("INVALID_FOR_CLAIM", correction)
        # Markdown emphasis must not change the semantic scope of the errata.
        self.assertIn("no demuestra que el script actualmente consultado",
                      correction.casefold().replace("**", ""))


if __name__ == "__main__":
    unittest.main()
