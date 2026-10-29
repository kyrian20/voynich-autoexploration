"""IVTFF uncertain comma gaps: quarantine, not fabricated certain words.

Synthetic regressions plus frozen-source candidate census. This is NOT a
predictor rerun, a holdout evaluation, or a reproduction of frozen results.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import tempfile
import unittest

SCRIPT = (Path(__file__).resolve().parents[1] / "research" / "analysis" /
          "2026-10-28-line-boundary-reproduction" / "line_boundary_replication.py")
spec = importlib.util.spec_from_file_location("line_boundary_uncertain_comma", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture(text, policy="primary", uncertain_space_policy="quarantine"):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "synthetic.ivtff"
        path.write_text(text, encoding="latin-1")
        return module.parse(path, policy, uncertain_space_policy)


def frozen_comma_census(path):
    """Count comma marks only in accepted P payloads, never in locus IDs."""
    rows = marks = 0
    for _, raw in module.checked_physical_lines(path.read_text(encoding="latin-1")):
        m = module.ROW.match(raw.strip())
        if not m or "," not in m["ident"]:
            continue
        ident, locus = m["ident"].split(",", 1)
        parts = ident.split(".")
        if len(parts) < 2:
            continue
        page = parts[0]
        loc = re.sub(r"^[+*@=~&!/]+", "", locus.strip())
        if not re.fullmatch(r"f(\\d+)[rv][1-6]?", page) and page != "fRos":
            continue
        if not re.fullmatch(r"P(?:0|1|b|c|r|t)", loc):
            continue
        body = re.sub(r"<![^>]*>", "", m["body"] or "")
        n = body.count(",")
        rows += bool(n)
        marks += n
    return rows, marks


class UncertainCommaBoundary(unittest.TestCase):
    def test_comma_quarantines_both_fragments_in_both_reading_policies(self):
        for policy in ("primary", "drop_uncertain_word"):
            with self.subTest(policy=policy):
                self.assertEqual(module.tokens("alpha,beta", policy, True), [None])
                self.assertEqual(module.tokens("alpha,beta", policy), [])
                self.assertEqual(module.tokens("alpha, beta", policy, True), [None])
                self.assertEqual(module.tokens("alpha ,beta", policy, True), [None])
                self.assertEqual(module.tokens("alpha,beta,gamma", policy, True),
                                 [None])
                self.assertEqual(module.tokens("alpha,beta", policy, True, "split"),
                                 ["alpha", "beta"])

    def test_known_dots_and_drawing_gaps_still_produce_candidates(self):
        for gap in (".", "<->", "<~>"):
            with self.subTest(gap=gap):
                self.assertEqual(module.tokens("alpha" + gap + "beta",
                                               preserve_gaps=True),
                                 ["alpha", "beta"])
        self.assertEqual(module.tokens("alpha.beta,gamma.delta.epsilon",
                                       preserve_gaps=True),
                         ["alpha", None, "delta", "epsilon"])
        self.assertEqual(module.tokens("alpha<!note>beta",
                                       preserve_gaps=True), ["alphabeta"])

    def test_comma_fragments_do_not_forge_cross_line_break(self):
        source = ("<f1r.P.1,P0> alpha,beta\\n"
                  "<f1r.P.2,P0> gamma.delta\\n")
        for policy in ("primary", "drop_uncertain_word"):
            with self.subTest(policy=policy):
                quarantined = fixture(source, policy)
                split = fixture(source, policy, "split")
                self.assertEqual([r["words"] for r in quarantined["f1r"]],
                                 [[None], ["gamma", "delta"]])
                self.assertEqual([r["y"] for r in module.candidates(
                    quarantined, ["f1r"])], [0])
                self.assertEqual([r["y"] for r in module.candidates(
                    split, ["f1r"])], [0, 1, 0])

    def test_unsupported_space_policy_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "unsupported uncertain-space"):
            module.tokens("alpha,beta", uncertain_space_policy="guess")

    def test_authenticated_corpus_impact_without_model_fit(self):
        expected = {"ZL3b": (1700, 2463), "IT2a": (0, 0)}
        for label, path in module.INPUTS.items():
            self.assertEqual(module.sha(path), module.EXPECTED_SHA256[label])
            self.assertEqual(frozen_comma_census(path), expected[label])
            for policy in ("primary", "drop_uncertain_word"):
                with self.subTest(label=label, policy=policy):
                    before = module.parse(path, policy, "split")
                    after = module.parse(path, policy, "quarantine")
                    previous = module.candidates(before, sorted(before))
                    corrected = module.candidates(after, sorted(after))
                    pos = sum(r["y"] for r in previous) - sum(
                        r["y"] for r in corrected)
                    neg = sum(r["y"] == 0 for r in previous) - sum(
                        r["y"] == 0 for r in corrected)
                    self.assertEqual(len(previous) - len(corrected), pos + neg)
                    if label == "ZL3b":
                        self.assertGreater(neg, 0)
                        self.assertGreaterEqual(pos, 0)
                    else:
                        self.assertEqual((pos, neg), (0, 0))
                    print(f"{label} {policy}: SHA256 OK; comma rows/marks="
                          f"{expected[label]}; removed positive={pos}; "
                          f"removed negative={neg}")


if __name__ == "__main__":
    unittest.main()
