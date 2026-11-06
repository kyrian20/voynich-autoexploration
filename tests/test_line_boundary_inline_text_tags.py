"""IVTFF text tags are metadata, not word spaces (IVTFF 2.0.2 §6.8).

Synthetic regressions plus read-only SHA-locked scope audit. No model fitting,
reserved-leaf evaluation, historical result replacement or EXP allocation.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import tempfile
import unittest

SCRIPT = (Path(__file__).resolve().parents[1] / "research" / "analysis" /
          "2026-10-28-line-boundary-reproduction" / "line_boundary_replication.py")
spec = importlib.util.spec_from_file_location("line_boundary_inline_tags", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

TAG = re.compile(r"<@[A-Z]=[^<>]>")


class InlineTextTagContract(unittest.TestCase):
    def test_tag_inside_word_is_zero_width_under_both_policies(self):
        for policy in ("primary", "drop_uncertain_word"):
            with self.subTest(policy=policy):
                self.assertEqual(module.tokens("ab<@L=A>cd", policy, True),
                                 ["abcd"])
                self.assertEqual(module.tokens("ab<@L=@><!note>cd", policy, True),
                                 ["abcd"])
                self.assertEqual(module.tokens("<@L=A>ab", policy, True), ["ab"])
                self.assertEqual(module.tokens("ab<@L=A>cd", policy), ["abcd"])

    def test_certain_spaces_and_drawing_gaps_still_split(self):
        # A comma is an uncertain IVTFF word boundary (§6.7), not a
        # certain gap. Keep the old comma-split expectation only as an
        # explicitly named counterfactual; the default must fail closed.
        for gap in (".", "<->", "<~>"):
            with self.subTest(gap=gap):
                self.assertEqual(module.tokens("ab<@L=A>" + gap + "cd",
                                               "primary", True), ["ab", "cd"])
        for policy in ("primary", "drop_uncertain_word"):
            with self.subTest(policy=policy, gap="uncertain comma"):
                self.assertEqual(module.tokens("ab<@L=A>,cd", policy, True),
                                 [None])
                self.assertEqual(module.tokens("ab<@L=A>,cd", policy, True,
                                               uncertain_space_policy="split"),
                                 ["ab", "cd"])

    def test_paragraph_markers_remain_barriers(self):
        for marker in ("<%>", "<$>"):
            with self.subTest(marker=marker):
                self.assertEqual(module.tokens("ab<@L=A>" + marker + "cd",
                                               "primary", True),
                                 ["ab", None, "cd"])

    def test_candidate_population_does_not_gain_fake_within_line_gap(self):
        source = ("<f1r.P.1,P0> ab<@L=A>cd.ef\n"
                  "<f1r.P.2,P0> gh\n")
        for policy in ("primary", "drop_uncertain_word"):
            with self.subTest(policy=policy):
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "synthetic.ivtff"
                    path.write_text(source, encoding="latin-1")
                    pages = module.parse(path, policy)
                    self.assertEqual(pages["f1r"][0]["words"], ["abcd", "ef"])
                    self.assertEqual([x["y"] for x in
                                      module.candidates(pages, ["f1r"])],
                                     [0, 1])

    def test_frozen_sources_scope_without_model_reexecution(self):
        for label, path in module.INPUTS.items():
            with self.subTest(label=label):
                self.assertEqual(module.sha(path), module.EXPECTED_SHA256[label])
                tagged = {}
                for lineno, raw in module.checked_physical_lines(
                        path.read_text(encoding="latin-1")):
                    match = module.ROW.match(raw.strip())
                    if match and match["body"] and TAG.search(match["body"]):
                        tagged[lineno] = match["body"]
                for policy in ("primary", "drop_uncertain_word"):
                    pages = module.parse(path, policy)
                    admitted = [row for lines in pages.values() for row in lines
                                if row["line"] in tagged]
                    changed = 0
                    for row in admitted:
                        body = tagged[row["line"]]
                        self.assertEqual(row["words"],
                                         module.tokens(body, policy, True))
                        # Exact prior behavior: each metadata tag became a
                        # whitespace separator, not a zero-width annotation.
                        old = module.tokens(TAG.sub(" ", body), policy, True)
                        changed += old != row["words"]
                    print(f"{label} {policy}: SHA256 verified; "
                          f"raw tagged records={len(tagged)}; "
                          f"admitted P records={len(admitted)}; "
                          f"changed token lists={changed}")


if __name__ == "__main__":
    unittest.main()
