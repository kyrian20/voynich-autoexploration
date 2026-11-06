"""Fail closed on malformed *closed* IVTFF metadata tags.

Read-only source scope: both original transcriptions SHA-locked. This is a
parser regression, NOT a new statistical experiment or a reproduction of
historical scores. No holdout labels or reserved-leaf outcomes are read.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import tempfile
import unittest

SCRIPT = (Path(__file__).resolve().parents[1] / "research" / "analysis" /
          "2026-10-28-line-boundary-reproduction" / "line_boundary_replication.py")
spec = importlib.util.spec_from_file_location("line_boundary_invalid_inline_tags", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

TAG = re.compile(r"<@[^>]*>")
VALID = re.compile(r"^<@[A-Z]=[^<>]>$")


class InvalidInlineTagContract(unittest.TestCase):
    def test_valid_single_character_tags_remain_zero_width(self):
        for policy in ("primary", "drop_uncertain_word"):
            with self.subTest(policy=policy):
                self.assertEqual(module.tokens("ab<@H=2>cd", policy, True), ["abcd"])
                self.assertEqual(module.tokens("<@L=A>ab.cd", policy, True),
                                 ["ab", "cd"])
                self.assertEqual(module.tokens("ab<@L=@><!note>cd", policy, True),
                                 ["abcd"])

    def test_closed_malformed_metadata_cannot_create_certain_gaps(self):
        # Previously the generic <...> replacement forged ["ab", "cd"].
        for tag in ("<@L=AB>", "<@L=>", "<@x=A>", "<@L=12>", "<@L=XYZ>"):
            for policy in ("primary", "drop_uncertain_word"):
                with self.subTest(tag=tag, policy=policy):
                    self.assertEqual(module.tokens("ab" + tag + "cd", policy, True),
                                     [None])
                    self.assertEqual(module.tokens("ab" + tag + "cd", policy), [])

    def test_malformed_metadata_quarantines_whole_row(self):
        for policy in ("primary", "drop_uncertain_word"):
            with self.subTest(policy=policy):
                self.assertEqual(module.tokens("safe.ab<@H=22>cd.clean", policy, True),
                                 [None])

    def test_malformed_row_cannot_generate_cross_row_positive(self):
        source = ("<f1r.P.1,P0> alpha<@H=22>beta.gamma\n"
                  "<f1r.P.2,P0> delta.epsilon\n")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "synthetic.ivtff"
            path.write_text(source, encoding="latin-1")
            for policy in ("primary", "drop_uncertain_word"):
                with self.subTest(policy=policy):
                    pages = module.parse(path, policy)
                    self.assertEqual([r["words"] for r in pages["f1r"]],
                                     [[None], ["delta", "epsilon"]])
                    self.assertEqual([r["y"] for r in
                                      module.candidates(pages, ["f1r"])], [0])

    def test_source_scope_sha_locked_without_model_reexecution(self):
        # Two valid <@H=n> tags per frozen corpus in admitted P rows.
        # No malformed closed metadata tags are present in those rows.
        for label, path in module.INPUTS.items():
            with self.subTest(corpus=label):
                self.assertEqual(module.sha(path), module.EXPECTED_SHA256[label])
                checked = 0
                tagged = 0
                malformed = 0
                for _, raw in module.checked_physical_lines(
                        path.read_text(encoding="latin-1")):
                    m = module.ROW.match(raw.strip())
                    if not m or "," not in m["ident"]:
                        continue
                    ident, loc = m["ident"].split(",", 1)
                    page = ident.split(".")[0]
                    if not (re.fullmatch(r"f\d+[rv][1-6]?", page)
                            or page == "fRos"):
                        continue
                    loc = re.sub(r"^[+*@=~&!/]+", "", loc.strip())
                    if not re.fullmatch(r"P(?:0|1|b|c|r|t)", loc):
                        continue
                    checked += 1
                    body = re.sub(r"<![^>]*>", "", m["body"] or "")
                    tags = TAG.findall(body)
                    if tags:
                        tagged += 1
                    malformed += sum(not VALID.fullmatch(t) for t in tags)
                self.assertEqual(checked, {"ZL3b": 4130, "IT2a": 4118}[label])
                self.assertEqual(tagged, 2)
                self.assertEqual(malformed, 0)


if __name__ == "__main__":
    unittest.main()
