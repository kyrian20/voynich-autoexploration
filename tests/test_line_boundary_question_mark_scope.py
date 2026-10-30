"""Frozen-source census for literal IVTFF '?' in the line-boundary reader.

This is a source-scope and regression audit, NOT a rerun of the historical
predictor, a candidate-level effect estimate, or a semantic experiment.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import unittest

SCRIPT = (Path(__file__).resolve().parents[1] / "research" / "analysis" /
          "2026-10-28-line-boundary-reproduction" / "line_boundary_replication.py")
spec = importlib.util.spec_from_file_location("line_boundary_question_scope", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Independently counted on the exact frozen source bytes; both corpora are
# alternative transcriptions of one manuscript, not independent samples.
EXPECTED = {
    "ZL3b": (4130, 155, 201, 90, 132),
    "IT2a": (4118, 67, 129, 67, 129),
}


def census(path):
    counts = dict(p_rows=0, raw_rows=0, raw_marks=0,
                  primary_rows=0, primary_marks=0)
    for _number, raw in module.checked_physical_lines(
            path.read_text(encoding="latin-1")):
        match = module.ROW.match(raw.strip())
        if not match or "," not in match["ident"]:
            continue
        ident, locus = match["ident"].split(",", 1)
        page = ident.split(".")[0]
        if not (re.fullmatch(r"f[0-9]+[rv][1-6]?", page) or page == "fRos"):
            continue
        loc = re.sub(r"^[+*@=~&!/]+", "", locus.strip())
        if not re.fullmatch(r"P(?:0|1|b|c|r|t)", loc):
            continue
        counts["p_rows"] += 1
        # Only literal unknown-glyph question marks outside free-text
        # comments are counted. Comments may themselves contain '?'.
        body = re.sub(r"<![^>]*>", "", match["body"] or "")
        n = body.count("?")
        if n:
            counts["raw_rows"] += 1
            counts["raw_marks"] += n
        # The primary-reading policy discards non-primary alternatives:
        # raw '?' inside an unselected option must not be called a primary
        # unknown glyph. Match the reader's exact bracket projection.
        primary = re.sub(r"\[([^:\]]*):[^\]]*\]", r"\1", body)
        primary = re.sub(r"\[([^\]]*)\]", r"\1", primary)
        selected = primary.count("?")
        if selected:
            counts["primary_rows"] += 1
            counts["primary_marks"] += selected
            # A selected '?' cannot silently become a certain word or a
            # new adjacency: at least one barrier must survive projection.
            if None not in module.tokens(match["body"] or "", "primary",
                                         preserve_gaps=True):
                raise AssertionError(("selected primary '?' lacks barrier", ident, raw))
        if n:
            # Excluding uncertain words must not promote an unknown glyph.
            if None not in module.tokens(match["body"] or "",
                                         "drop_uncertain_word",
                                         preserve_gaps=True):
                raise AssertionError(("excluded '?' lacks barrier", ident, raw))
    return counts



def literal_question_deletion_counterfactual(path, parsed, policy):
    """Delete literal '?' only; retain every other current parser/guard.

    This deliberately does NOT reconstruct the historical reader. It measures
    a named sensitivity of the current candidate population, not AUC.
    """
    import copy

    changed = copy.deepcopy(parsed)
    raw_by_line = dict(module.checked_physical_lines(
        path.read_text(encoding="latin-1")))
    for page, rows in changed.items():
        for row in rows:
            source = module.ROW.match(raw_by_line[row["line"]].strip())
            if source is None:
                raise AssertionError(("missing source row", page, row["line"]))
            body = source["body"] or ""
            row["words"] = module.tokens(
                body.replace("?", ""), policy, preserve_gaps=True)
            row["text"] = " ".join(
                word if word is not None else "<UNCERTAIN>"
                for word in row["words"])
    return changed


def candidate_totals(parsed):
    candidates = module.candidates(parsed, sorted(parsed))
    return (sum(item["y"] == 0 for item in candidates),
            sum(item["y"] == 1 for item in candidates))


class FrozenUnknownGlyphScope(unittest.TestCase):
    def test_question_deletion_counterfactual_synthetic_control(self):
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "control.ivtff"
            path.write_text("<f1r.P.1,P0> alpha.?\\n"
                            "<f1r.P.2,P0> beta\\n", encoding="latin-1")
            for policy in ("primary", "drop_uncertain_word"):
                with self.subTest(policy=policy):
                    parsed = module.parse(path, policy)
                    counterfactual = literal_question_deletion_counterfactual(
                        path, parsed, policy)
                    self.assertEqual(candidate_totals(parsed), (0, 0))
                    self.assertEqual(candidate_totals(counterfactual), (0, 1))
        # A question mark in the unselected option must not change primary.
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "unselected.ivtff"
            path.write_text("<f1r.P.1,P0> safe.[ch:?].clean\\n",
                            encoding="latin-1")
            parsed = module.parse(path, "primary")
            counterfactual = literal_question_deletion_counterfactual(
                path, parsed, "primary")
            self.assertEqual(candidate_totals(parsed),
                             candidate_totals(counterfactual))

    def test_frozen_candidate_sensitivity_to_literal_question_deletion(self):
        # Descriptive paired counterfactual, NOT a historical replay or
        # a model fit. Other IVTFF guards and physical-row identifiers
        # remain in force in both arms.
        for label, path in module.INPUTS.items():
            with self.subTest(label=label):
                self.assertEqual(module.sha(path), module.EXPECTED_SHA256[label])
                for policy in ("primary", "drop_uncertain_word"):
                    parsed = module.parse(path, policy)
                    counterfactual = literal_question_deletion_counterfactual(
                        path, parsed, policy)
                    self.assertEqual(set(parsed), set(counterfactual))
                    for page in parsed:
                        self.assertEqual(
                            [(row["line"], row["loc"], row["locus_number"])
                             for row in parsed[page]],
                            [(row["line"], row["loc"], row["locus_number"])
                             for row in counterfactual[page]])
                    corrected = candidate_totals(parsed)
                    deleted = candidate_totals(counterfactual)
                    delta = tuple(b - a for a, b in zip(corrected, deleted))
                    print(
                        f"QUESTION_CANDIDATES {label} {policy}: "
                        f"sha256={module.EXPECTED_SHA256[label]} "
                        f"corrected_neg={corrected[0]} corrected_pos={corrected[1]} "
                        f"delete_question_neg={deleted[0]} "
                        f"delete_question_pos={deleted[1]} "
                        f"delta_neg={delta[0]} delta_pos={delta[1]}")
                    # No expectation is fitted to the observed delta;
                    # both arms must remain valid nonnegative populations.
                    self.assertTrue(all(v >= 0 for v in corrected + deleted))

    def test_alternative_selection_does_not_invent_unknown_glyphs(self):
        self.assertEqual(module.tokens("safe.[ch:?].clean", "primary", True),
                         ["safe", "ch", "clean"])
        self.assertEqual(module.tokens("safe.[ch:?].clean",
                                       "drop_uncertain_word", True),
                         ["safe", None, "clean"])
        self.assertEqual(module.tokens("safe.[?:ch].clean", "primary", True),
                         ["safe", None, "clean"])

    def test_frozen_census_and_barriers(self):
        for label, path in module.INPUTS.items():
            with self.subTest(label=label):
                self.assertEqual(module.sha(path), module.EXPECTED_SHA256[label])
                actual = census(path)
                self.assertEqual(tuple(actual.values()), EXPECTED[label])
                print(f"{label}: sha256={module.EXPECTED_SHA256[label]} "
                      f"P={actual['p_rows']} raw_question_rows={actual['raw_rows']} "
                      f"raw_question_marks={actual['raw_marks']} "
                      f"primary_selected_rows={actual['primary_rows']} "
                      f"primary_selected_marks={actual['primary_marks']} "
                      f"barriers=checked")


if __name__ == "__main__":
    unittest.main()
