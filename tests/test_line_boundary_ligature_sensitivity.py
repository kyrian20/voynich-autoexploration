"""Scoped IVTFF ligature sensitivity for the draft line-boundary predictor.

No model fit, no held-out metric, no modification of historical outputs.
The default policy remains quarantine; only ASCII-letter-only ligatures are
expanded in the explicit alternative view. Other glyph codes remain barriers.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest

SCRIPT = (Path(__file__).resolve().parents[1] / "research" / "analysis" /
          "2026-10-28-line-boundary-reproduction" / "line_boundary_replication.py")
spec = importlib.util.spec_from_file_location("line_boundary_ligature_sensitivity", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture(text, ligature_policy="quarantine"):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "synthetic.ivtff"
        path.write_text(text, encoding="latin-1")
        return module.parse(path, ligature_policy=ligature_policy)


def census(path):
    """Count braced spans in admitted P bodies, not metadata or comments."""
    total = ascii_only = 0
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
        if not re.fullmatch(r"f([0-9]+)[rv][1-6]?", page) and page != "fRos":
            continue
        if not re.fullmatch(r"P(?:0|1|b|c|r|t)", loc):
            continue
        body = re.sub(r"<![^>]*>", "", m["body"] or "")
        for span in re.finditer(r"\{([^{}]*)\}", body):
            total += 1
            ascii_only += bool(re.fullmatch(r"[A-Za-z]+", span.group(1)))
    return total, ascii_only


class LineBoundaryLigatureSensitivity(unittest.TestCase):
    def test_explicit_ascii_expansion_preserves_word_identity(self):
        self.assertEqual(module.tokens("al{ck}or.beta", preserve_gaps=True),
                         [None, "beta"])
        self.assertEqual(module.tokens("al{ck}or.beta", preserve_gaps=True,
                                       ligature_policy="expand_ascii"),
                         ["alckor", "beta"])
        self.assertEqual(module.tokens("alpha.{ck}.beta", preserve_gaps=True,
                                       ligature_policy="expand_ascii"),
                         ["alpha", "ck", "beta"])

    def test_non_ascii_opaque_or_malformed_braces_never_become_words(self):
        for body in ("al{c'h}or", "al{@209;h}or", "al{c.d}or",
                     "al{ck", "al{{ck}}or", "al{ck}}or"):
            with self.subTest(body=body):
                self.assertEqual(module.tokens(body, preserve_gaps=True,
                                               ligature_policy="expand_ascii"),
                                 [None])
        with self.assertRaisesRegex(ValueError, "unsupported ligature"):
            module.tokens("alpha", ligature_policy="guess")

    def test_candidates_are_added_only_when_a_ligature_is_unambiguous(self):
        text = ("<f1r.1,@P0> al{ck}or.beta\n"
                "<f1r.2,+P0> gamma.delta\n")
        before = fixture(text)
        after = fixture(text, "expand_ascii")
        self.assertEqual([r["y"] for r in module.candidates(before, ["f1r"])],
                         [1, 0])
        self.assertEqual([r["y"] for r in module.candidates(after, ["f1r"])],
                         [0, 1, 0])

    def test_frozen_corpus_candidate_census_without_fitting(self):
        for label, path in module.INPUTS.items():
            self.assertEqual(module.sha(path), module.EXPECTED_SHA256[label])
            counts = census(path)
            self.assertEqual(counts, {"ZL3b": (394, 283), "IT2a": (0, 0)}[label])
            for policy in ("primary", "drop_uncertain_word"):
                with self.subTest(label=label, policy=policy):
                    before = module.parse(path, policy)
                    after = module.parse(path, policy, ligature_policy="expand_ascii")
                    old = module.candidates(before, sorted(before))
                    new = module.candidates(after, sorted(after))
                    bpos = sum(r["y"] for r in old)
                    npos = sum(r["y"] for r in new)
                    bneg = len(old) - bpos
                    nneg = len(new) - npos
                    self.assertGreaterEqual(npos, bpos)
                    self.assertGreaterEqual(nneg, bneg)
                    if label == "IT2a":
                        self.assertEqual((npos, nneg), (bpos, bneg))
                    print("LIGATURE_CENSUS " + json.dumps({
                        "source": label, "policy": policy,
                        "sha256": module.EXPECTED_SHA256[label],
                        "ligatures_P": counts[0], "ascii_only_P": counts[1],
                        "quarantine": {"positive": bpos, "negative": bneg},
                        "expand_ascii": {"positive": npos, "negative": nneg},
                        "delta_positive": npos - bpos,
                        "delta_negative": nneg - bneg,
                    }, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
