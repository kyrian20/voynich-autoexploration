"""Regression: IVTFF slash continuation must not become a line boundary.

The conservative policy is to exclude affected words as barriers, not to
claim to have reconstructed the full joined word across physical rows.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = (Path(__file__).resolve().parents[1] / "research" / "analysis" /
          "2026-10-28-line-boundary-reproduction" / "line_boundary_replication.py")
spec = importlib.util.spec_from_file_location("line_boundary_replication_slash", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SlashContinuationContract(unittest.TestCase):
    def test_slash_affects_whole_word_in_both_policies(self):
        for policy in ("primary", "drop_uncertain_word"):
            with self.subTest(policy=policy):
                self.assertEqual(module.tokens("ab/", policy, preserve_gaps=True), [None])
                self.assertEqual(module.tokens("/cd", policy, preserve_gaps=True), [None])
                self.assertEqual(module.tokens("ab/cd", policy, preserve_gaps=True), [None])
                self.assertEqual(module.tokens("ab/", policy), [])

    def test_slash_only_marker_is_a_barrier(self):
        self.assertEqual(module.tokens("alpha./.beta", "primary",
                                       preserve_gaps=True), ["alpha", None, "beta"])
        self.assertEqual(module.tokens("alpha./.beta", "primary"), ["alpha", "beta"])

    def test_continued_word_does_not_forge_positive_line_break(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "synthetic.ivtff"
            source.write_text("<f1r.P.1,P0> ab/\n"
                              "<f1r.P.2,P0> /cd\n",
                              encoding="latin-1")
            pages = module.parse(source)
        # A page with no usable words is intentionally absent.
        self.assertNotIn("f1r", pages)
        self.assertEqual(module.candidates(pages, list(pages)), [])

    def test_continuation_does_not_bridge_neighbouring_words(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "synthetic.ivtff"
            source.write_text("<f1r.P.1,P0> safe.ab/\n"
                              "<f1r.P.2,P0> /cd.clean\n",
                              encoding="latin-1")
            pages = module.parse(source)
        self.assertEqual([row["words"] for row in pages["f1r"]],
                         [["safe", None], [None, "clean"]])
        self.assertEqual(module.candidates(pages, ["f1r"]), [])

    def test_ordinary_boundary_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "synthetic.ivtff"
            source.write_text("<f1r.P.1,P0> safe.other\n"
                              "<f1r.P.2,P0> clean\n",
                              encoding="latin-1")
            pages = module.parse(source)
        self.assertEqual([row["y"] for row in module.candidates(pages, ["f1r"])],
                         [0, 1])


if __name__ == "__main__":
    unittest.main()
