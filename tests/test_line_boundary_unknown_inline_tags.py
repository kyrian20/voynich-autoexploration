"""IVTFF unsupported angle tags must not fabricate line-boundary candidates.

Synthetic parser regressions plus a SHA-locked, read-only census of the two
frozen transcriptions. No predictive rerun, holdout outcomes, or EXP ID.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import tempfile
import unittest

SCRIPT = (Path(__file__).resolve().parents[1] / "research" / "analysis" /
          "2026-10-28-line-boundary-reproduction" / "line_boundary_replication.py")
spec = importlib.util.spec_from_file_location("line_boundary_unknown_tags", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class UnknownAngleTagContract(unittest.TestCase):
    def test_only_documented_drawing_interruptions_are_spaces(self):
        for policy in ("primary", "drop_uncertain_word"):
            with self.subTest(policy=policy):
                self.assertEqual(module.tokens("alpha<->beta<~>gamma", policy, True),
                                 ["alpha", "beta", "gamma"])
                self.assertEqual(module.tokens("ab<!comment>cd", policy, True),
                                 ["abcd"])
                self.assertEqual(module.tokens("ab<@H=2>cd", policy, True),
                                 ["abcd"])

    def test_unknown_closed_tags_quarantine_entire_row(self):
        for tag in ("<foo>", "<+>", "<-->", "<>", "<@L=AB>", "<#>"):
            for policy in ("primary", "drop_uncertain_word"):
                with self.subTest(tag=tag, policy=policy):
                    self.assertEqual(module.tokens("safe.ab" + tag + "cd.tail",
                                                   policy, True), [None])
                    self.assertEqual(module.tokens("ab" + tag + "cd",
                                                   policy), [])

    def test_stray_or_unclosed_angle_markers_still_quarantine(self):
        for body in ("alpha<unknown.beta", "alpha>beta", "alpha<->beta<bogus>"):
            self.assertEqual(module.tokens(body, "primary", True), [None])

    def test_unknown_tag_cannot_create_within_or_cross_row_pair(self):
        source = ("<f1r.P.1,P0> alpha<unknown>beta.gamma\n"
                  "<f1r.P.2,P0> delta.epsilon\n")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.ivtff"
            path.write_text(source, encoding="latin-1")
            for policy in ("primary", "drop_uncertain_word"):
                pages = module.parse(path, policy)
                self.assertEqual(pages["f1r"][0]["words"], [None])
                self.assertEqual(pages["f1r"][1]["words"], ["delta", "epsilon"])
                self.assertEqual([r["y"] for r in module.candidates(pages, ["f1r"])],
                                 [0])

    def test_frozen_sources_are_sha_locked_and_scope_is_explicit(self):
        # Source census of accepted P payloads, not a score or full IVTFF audit.
        for label, path in module.INPUTS.items():
            with self.subTest(corpus=label):
                self.assertEqual(module.sha(path), module.EXPECTED_SHA256[label])
                rows = 0
                unknown_tags = 0
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
                    body = match["body"] or ""
                    body = re.sub(r"<![^>]*>", "", body)
                    body = body.replace("<%>", "").replace("<$>", "")
                    body = re.sub(r"<@[A-Z]=[^<>]>", "", body)
                    body = re.sub(r"<(?:-|~)>", "", body)
                    unknown_tags += len(re.findall(r"<[^>]*>", body))
                self.assertEqual(rows, {"ZL3b": 4130, "IT2a": 4118}[label])
                # Initial independent source scan found none. If this changes,
                # investigate the raw examples rather than relaxing the guard.
                self.assertEqual(unknown_tags, 0)


if __name__ == "__main__":
    unittest.main()
