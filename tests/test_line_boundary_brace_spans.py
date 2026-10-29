"""Fail closed on IVTFF braced spans before splitting apparent words.

A synthetic regression of a real parser defect, plus a SHA-locked source
census. This does not run the classifier or consume reserved folios.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import tempfile
import unittest

SCRIPT = (Path(__file__).resolve().parents[1] / "research" / "analysis" /
          "2026-10-28-line-boundary-reproduction" / "line_boundary_replication.py")
spec = importlib.util.spec_from_file_location("line_boundary_braces", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def parse_fixture(source, policy="primary"):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "synthetic.ivtff"
        path.write_text(source, encoding="latin-1")
        return module.parse(path, policy)


class BraceSpanContract(unittest.TestCase):
    def test_dotted_and_spaced_braces_do_not_create_internal_words(self):
        for policy in ("primary", "drop_uncertain_word"):
            for span in ("{a.b.c.d}", "{a b c d}", "{a,b,c,d}"):
                with self.subTest(policy=policy, span=span):
                    self.assertEqual(
                        module.tokens("alpha." + span + ".omega",
                                      policy, preserve_gaps=True),
                        ["alpha", None, "omega"])
                    self.assertEqual(
                        module.tokens("alpha." + span + ".omega", policy),
                        ["alpha", "omega"])

    def test_glued_and_multiple_braces_preserve_barriers(self):
        for policy in ("primary", "drop_uncertain_word"):
            self.assertEqual(module.tokens("ab{a.b.c}cd", policy, True), [None])
            self.assertEqual(module.tokens("a.{x}.{y}.b", policy, True),
                             ["a", None, None, "b"])
            self.assertEqual(module.tokens("a.b", policy, True), ["a", "b"])

    def test_unbalanced_or_nested_braces_quarantine_whole_row(self):
        for body in ("alpha.{a.b.c", "alpha.a.b.c}", "alpha.{a{b.c}d}.omega",
                     "alpha.{a.b}c}.omega", "alpha.{a.b}{c.d"):
            for policy in ("primary", "drop_uncertain_word"):
                with self.subTest(body=body, policy=policy):
                    self.assertEqual(module.tokens(body, policy, True), [None])
                    self.assertEqual(module.tokens(body, policy), [])

    def test_no_fabricated_within_or_cross_row_candidates(self):
        source = ("<f1r.P.1,P0> alpha.{a.b.c.d}\n"
                  "<f1r.P.2,P0> beta.gamma\n")
        for policy in ("primary", "drop_uncertain_word"):
            with self.subTest(policy=policy):
                pages = parse_fixture(source, policy)
                self.assertEqual(pages["f1r"][0]["words"], ["alpha", None])
                self.assertEqual(pages["f1r"][1]["words"], ["beta", "gamma"])
                self.assertEqual([r["y"] for r in module.candidates(pages, ["f1r"])],
                                 [0])

    def test_frozen_census_is_authenticated_and_scope_limited(self):
        expected = {"ZL3b": (4130, 394, 0), "IT2a": (4118, 0, 0)}
        for label, path in module.INPUTS.items():
            with self.subTest(label=label):
                self.assertEqual(module.sha(path), module.EXPECTED_SHA256[label])
                rows = spans = separated_spans = 0
                for _, raw in module.checked_physical_lines(
                        path.read_text(encoding="latin-1")):
                    match = module.ROW.match(raw.strip())
                    if not match or "," not in match["ident"]:
                        continue
                    ident, loc = match["ident"].split(",", 1)
                    page = ident.split(".")[0]
                    if not (re.fullmatch(r"f\d+[rv][1-6]?", page)
                            or page == "fRos"):
                        continue
                    loc = re.sub(r"^[+*@=~&!/]+", "", loc.strip())
                    if not re.fullmatch(r"P(?:0|1|b|c|r|t)", loc):
                        continue
                    rows += 1
                    for span in re.findall(r"\{[^{}]*\}", match["body"] or ""):
                        spans += 1
                        separated_spans += bool(re.search(r"[.,\s]", span))
                self.assertEqual((rows, spans, separated_spans), expected[label])
                print(f"{label}: source SHA256 OK; P rows={rows}; "
                      f"braced spans={spans}; with separators={separated_spans}")


if __name__ == "__main__":
    unittest.main()
