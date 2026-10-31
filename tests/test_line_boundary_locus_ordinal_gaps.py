"""Do not invent P-to-P boundaries across missing IVTFF locus numbers.

This is a code defect and frozen-corpus candidate-count audit, NOT a new
predictive evaluation. No model is fitted and no reserved-leaf score is read.
"""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = (Path(__file__).resolve().parents[1] / "research" / "analysis" /
          "2026-10-28-line-boundary-reproduction" / "line_boundary_replication.py")
spec = importlib.util.spec_from_file_location("line_boundary_locus_gaps", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture(text, policy="primary"):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "synthetic.ivtff"
        path.write_text(text, encoding="latin-1")
        return module.parse(path, policy)


class MissingLocusOrdinalContract(unittest.TestCase):
    def test_missing_number_blocks_false_positive_not_within_row_negatives(self):
        for policy in ("primary", "drop_uncertain_word"):
            with self.subTest(policy=policy):
                pages = fixture("<f1r.1,@P0> alpha.beta\n"
                                "<f1r.3,+P0> gamma.delta\n", policy)
                self.assertEqual([r["locus_number"] for r in pages["f1r"]],
                                 [1, 3])
                self.assertEqual([r["y"] for r in module.candidates(pages, ["f1r"])],
                                 [0, 0])

    def test_consecutive_loci_still_have_positive_candidate(self):
        pages = fixture("<f1r.1,@P0> alpha.beta\n"
                        "<f1r.2,+P0> gamma.delta\n")
        self.assertEqual([r["y"] for r in module.candidates(pages, ["f1r"])],
                         [0, 1, 0])

    def test_repeated_reversed_and_unreadable_ordinals_fail_closed(self):
        for second in ("<f1r.1,+P0>", "<f1r.0,+P0>",
                       "<f1r.P.foo,+P0>"):
            with self.subTest(second=second):
                pages = fixture("<f1r.1,@P0> alpha\n" + second + " beta\n")
                self.assertEqual(module.candidates(pages, ["f1r"]), [])

    def test_non_p_and_paragraph_guards_still_apply(self):
        pages = fixture("<f1r.1,@P0> alpha\n"
                        "<f1r.2,*L0> label\n"
                        "<f1r.3,+P0> beta\n")
        self.assertEqual(module.candidates(pages, ["f1r"]), [])
        pages = fixture("<f1r.1,@P0> alpha<$>\n"
                        "<f1r.3,+P0> <%>beta\n")
        self.assertEqual(module.candidates(pages, ["f1r"]), [])

    def test_frozen_corpus_delta_against_previous_constructor(self):
        # Authenticate bytes before inspection; the counterfactual removes
        # ONLY the new ordinal field and retains the previous non-P and
        # paragraph guards. No model, holdout metric or result is recomputed.
        expected = {"ZL3b": {"jumps": 76, "removed": 0},
                    "IT2a": {"jumps": 76, "removed": 2}}
        for label, path in module.INPUTS.items():
            self.assertEqual(module.sha(path), module.EXPECTED_SHA256[label])
            for policy in ("primary", "drop_uncertain_word"):
                with self.subTest(label=label, policy=policy):
                    pages = module.parse(path, policy)
                    jumps = sum(
                        a["locus_number"] is not None
                        and b["locus_number"] is not None
                        and b["locus_number"] != a["locus_number"] + 1
                        for rows in pages.values()
                        for a, b in zip(rows, rows[1:])
                    )
                    self.assertEqual(jumps, expected[label]["jumps"])
                    corrected = module.candidates(pages, sorted(pages))
                    legacy_pages = copy.deepcopy(pages)
                    for rows in legacy_pages.values():
                        for row in rows:
                            row.pop("locus_number", None)
                    previous = module.candidates(legacy_pages, sorted(legacy_pages))
                    removed = len(previous) - len(corrected)
                    self.assertEqual(removed, expected[label]["removed"])
                    self.assertEqual(
                        sum(r["y"] == 0 for r in previous),
                        sum(r["y"] == 0 for r in corrected))
                    self.assertEqual(
                        sum(r["y"] == 1 for r in previous)
                        - sum(r["y"] == 1 for r in corrected), removed)
                    print(f"{label} {policy}: SHA256 OK; P ordinal gaps={jumps}; "
                          f"positive candidates excluded={removed}")


if __name__ == "__main__":
    unittest.main()
