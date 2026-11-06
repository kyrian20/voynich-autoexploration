"""IVTFF paragraph tags are barriers, not ordinary word separators.

Synthetic counterexamples and a hash-locked frozen-corpus scope audit.
No historical metrics or prospective held-out folios are recalculated.
"""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = (Path(__file__).resolve().parents[1] / "research" / "analysis" /
          "2026-10-28-line-boundary-reproduction" / "line_boundary_replication.py")
spec = importlib.util.spec_from_file_location("line_boundary_paragraph", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture(source, policy="primary"):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "synthetic.ivtff"
        path.write_text(source, encoding="latin-1")
        return module.parse(path, policy)


class ParagraphBoundaryContract(unittest.TestCase):
    def test_explicit_paragraph_end_is_a_barrier(self):
        for policy in ("primary", "drop_uncertain_word"):
            with self.subTest(policy=policy):
                self.assertEqual(module.tokens("alpha<$>", policy, True),
                                 ["alpha", None])
                pages = fixture("<f1r.P.1,P0> alpha<$>\n"
                                "<f1r.P.2,P0> beta\n", policy)
                self.assertEqual(module.candidates(pages, ["f1r"]), [])

    def test_explicit_paragraph_start_is_a_barrier(self):
        for policy in ("primary", "drop_uncertain_word"):
            with self.subTest(policy=policy):
                self.assertEqual(module.tokens("<%>beta", policy, True),
                                 [None, "beta"])
                pages = fixture("<f1r.P.1,P0> alpha\n"
                                "<f1r.P.2,P0> <%>beta\n", policy)
                self.assertEqual(module.candidates(pages, ["f1r"]), [])

    def test_inline_paragraph_transition_cannot_forge_negative(self):
        for marker in ("<%>", "<$>"):
            with self.subTest(marker=marker):
                self.assertEqual(module.tokens("alpha" + marker + "beta",
                                               "primary", True),
                                 ["alpha", None, "beta"])
                pages = fixture("<f1r.P.1,P0> alpha" + marker + "beta\n")
                self.assertEqual(module.candidates(pages, ["f1r"]), [])

    def test_regular_gaps_and_free_comments_remain_unchanged(self):
        self.assertEqual(module.tokens("alpha.beta", "primary", True),
                         ["alpha", "beta"])
        self.assertEqual(module.tokens("alpha<!note>beta", "primary", True),
                         ["alphabeta"])
        self.assertEqual(module.tokens("alpha<->beta", "primary", True),
                         ["alpha", "beta"])
        pages = fixture("<f1r.P.1,P0> alpha.beta\n"
                        "<f1r.P.2,P0> gamma.delta\n")
        self.assertEqual([x["y"] for x in module.candidates(pages, ["f1r"])],
                         [0, 1, 0])

    def test_frozen_corpus_scope_and_counterfactual(self):
        # Compare against the prior behavior *only* by removing the two
        # paragraph tags with spaces (the exact old reader behavior), not by rerunning the model.
        # All input bytes are authenticated before any analysis.
        for label, path in module.INPUTS.items():
            with self.subTest(label=label):
                self.assertEqual(module.sha(path), module.EXPECTED_SHA256[label])
                marked = {}
                for lineno, raw in module.checked_physical_lines(
                        path.read_text(encoding="latin-1")):
                    m = module.ROW.match(raw.strip())
                    if m and m["body"] and ("<%>" in m["body"] or
                                            "<$>" in m["body"]):
                        marked[lineno] = m["body"]
                for policy in ("primary", "drop_uncertain_word"):
                    pages = module.parse(path, policy)
                    legacy = copy.deepcopy(pages)
                    impacted = 0
                    for lines in legacy.values():
                        for row in lines:
                            if row["line"] in marked:
                                body = marked[row["line"]]
                                before = module.tokens(body.replace("<%>", " ")
                                                        .replace("<$>", " "),
                                                       policy, True)
                                if before != row["words"]:
                                    impacted += 1
                                row["words"] = before
                    names = sorted(pages)
                    corrected = module.candidates(pages, names)
                    previous = module.candidates(legacy, names)
                    removed = len(previous) - len(corrected)
                    self.assertGreaterEqual(removed, 0)
                    self.assertEqual(removed,
                                     sum(x["y"] for x in previous) -
                                     sum(x["y"] for x in corrected) +
                                     (sum(x["y"] == 0 for x in previous) -
                                      sum(x["y"] == 0 for x in corrected)))
                    print(f"{label} {policy}: frozen_sha256_ok; "
                          f"raw_rows_with_paragraph_tags={len(marked)}; "
                          f"admitted_rows_changed={impacted}; "
                          f"candidate_delta_legacy_minus_corrected={removed}")


if __name__ == "__main__":
    unittest.main()
