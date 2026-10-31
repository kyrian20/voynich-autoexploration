"""Fail-closed IVTFF malformed markup regression for line-boundary candidates.

Synthetic fixtures are not historical source reconstructions. Corpus coverage
uses the exact frozen SHA-256 before inspecting physical P rows.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import tempfile
import unittest

SCRIPT = (Path(__file__).resolve().parents[1] / "research" / "analysis" /
          "2026-10-28-line-boundary-reproduction" / "line_boundary_replication.py")
spec = importlib.util.spec_from_file_location("line_boundary_malformed_markup", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class MalformedMarkupContract(unittest.TestCase):
    def test_unclosed_inline_comment_cannot_become_words(self):
        # Previously: ['alpha', 'unfinished', 'note'].
        self.assertEqual(module.tokens("alpha<!unfinished.note", "primary"), [])
        self.assertEqual(module.tokens("alpha<!unfinished.note", "primary",
                                       preserve_gaps=True), [None])

    def test_unclosed_text_tag_and_stray_closer(self):
        for body in ("alpha<@X=unfinished.beta", "alpha>beta"):
            with self.subTest(body=body):
                self.assertEqual(module.tokens(body, "primary",
                                               preserve_gaps=True), [None])

    def test_unclosed_or_stray_square_bracket_both_policies(self):
        for body in ("alpha[cd.ef", "alpha]beta", "alpha[cd:ef"):
            for policy in ("primary", "drop_uncertain_word"):
                with self.subTest(body=body, policy=policy):
                    self.assertEqual(module.tokens(body, policy,
                                                   preserve_gaps=True), [None])

    def test_well_formed_annotations_still_follow_existing_policy(self):
        self.assertEqual(module.tokens("alpha<!note>beta", "primary"), ["alphabeta"])
        self.assertEqual(module.tokens("alpha[cd:ef]beta", "primary"),
                         ["alphacdbeta"])
        self.assertEqual(module.tokens("alpha[cd:ef]beta",
                                       "drop_uncertain_word", preserve_gaps=True),
                         [None])

    def test_malformed_row_blocks_cross_line_gap_but_preserves_next_row(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.ivtff"
            path.write_text("<f1r.1,+P0> alpha<!unfinished.note\n"
                            "<f1r.2,+P0> gamma.delta\n", encoding="latin-1")
            pages = module.parse(path)
        self.assertEqual(pages["f1r"][0]["words"], [None])
        self.assertEqual(pages["f1r"][1]["words"], ["gamma", "delta"])
        self.assertEqual([row["y"] for row in module.candidates(pages, ["f1r"])],
                         [0])

    def test_frozen_p_row_scope_is_zero_for_this_new_guard(self):
        expected = {"ZL3b": 4130, "IT2a": 4118}
        for label, path in module.INPUTS.items():
            with self.subTest(corpus=label):
                self.assertEqual(module.sha(path), module.EXPECTED_SHA256[label])
                checked = 0
                malformed = 0
                for _, raw in module.checked_physical_lines(
                        path.read_text(encoding="latin-1")):
                    m = module.ROW.match(raw.strip())
                    if not m or "," not in m["ident"]:
                        continue
                    ident, locus = m["ident"].split(",", 1)
                    parts = ident.split(".")
                    if len(parts) < 2:
                        continue
                    page = parts[0]
                    if not (re.fullmatch(r"f\d+[rv][1-6]?", page) or page == "fRos"):
                        continue
                    loc = re.sub(r"^[+*@=~&!/]+", "", locus.strip())
                    if not re.fullmatch(r"P(?:0|1|b|c|r|t)", loc):
                        continue
                    checked += 1
                    body = m["body"] or ""
                    body = re.sub(r"<![^>]*>", "", body)
                    body = re.sub(r"<[^>]*>", " ", body)
                    if "<" in body or ">" in body:
                        malformed += 1
                        continue
                    for policy in ("primary", "drop_uncertain_word"):
                        if policy == "drop_uncertain_word":
                            normalized = re.sub(r"\[[^\]]*\]", "?", body)
                        else:
                            normalized = re.sub(
                                r"\[([^:\]]*):[^\]]*\]", r"\1", body)
                            normalized = re.sub(
                                r"\[([^\]]*)\]", r"\1", normalized)
                        if "[" in normalized or "]" in normalized:
                            malformed += 1
                            break
                self.assertEqual(checked, expected[label])
                self.assertEqual(malformed, 0)


if __name__ == "__main__":
    unittest.main()
