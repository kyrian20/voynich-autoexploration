"""Non-P IVTFF loci must not be silently skipped when making P-to-P gaps.

This is a code/corpus-impact audit, not a fresh predictive experiment.
All frozen sources are checked by SHA-256 before reading. The historical
results.json is not regenerated or overwritten.
"""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = (Path(__file__).resolve().parents[1] / "research" / "analysis" /
          "2026-10-28-line-boundary-reproduction" / "line_boundary_replication.py")
spec = importlib.util.spec_from_file_location("line_boundary_interposed", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture(text, policy="primary"):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "fixture.ivtff"
        path.write_text(text, encoding="latin-1")
        return module.parse(path, policy)


class InterposedLocusContract(unittest.TestCase):
    def test_label_between_body_rows_blocks_forged_positive(self):
        pages = fixture("<f1r.P.1,P0> alpha.beta\n"
                        "<f1r.L.1,*L0> label\n"
                        "<f1r.P.2,P0> gamma.delta\n")
        self.assertEqual(
            pages["f1r"][0]["intervening_non_p"], [{"line": 2, "loc": "L0"}])
        # Genuine within-row negative gaps remain; the cross-locus
        # positive candidate is excluded.
        self.assertEqual(
            [row["y"] for row in module.candidates(pages, ["f1r"])], [0, 0])

    def test_multiple_non_body_loci_are_traceable(self):
        pages = fixture("<f1r.P.1,P0> alpha\n"
                        "<f1r.L.1,*L0> label\n"
                        "<f1r.C.1,*Cc> circle\n"
                        "<f1r.P.2,P0> beta\n")
        self.assertEqual(pages["f1r"][0]["intervening_non_p"],
                         [{"line": 2, "loc": "L0"}, {"line": 3, "loc": "Cc"}])
        self.assertEqual(module.candidates(pages, ["f1r"]), [])

    def test_non_body_locus_before_first_body_row_does_not_block(self):
        pages = fixture("<f1r.L.1,*L0> label\n"
                        "<f1r.P.1,P0> alpha\n"
                        "<f1r.P.2,P0> beta\n")
        self.assertNotIn("intervening_non_p", pages["f1r"][0])
        self.assertEqual(
            [row["y"] for row in module.candidates(pages, ["f1r"])], [1])

    def test_comment_without_locus_is_not_a_non_body_record(self):
        pages = fixture("<f1r.P.1,P0> alpha\n"
                        "# metadata without a locus\n"
                        "<f1r.P.2,P0> beta\n")
        self.assertEqual(
            [row["y"] for row in module.candidates(pages, ["f1r"])], [1])

    def test_unparsed_same_page_locus_blocks_false_positive(self):
        # An invalid row is still physical evidence of an intervening locus.
        # Before the guard it vanished, yielding a false P.1 -> P.2 break.
        for invalid in ("<f1r.P.2> unknown",
                        "<f1r.P.2 unknown",
                        "<f1r.P.2,P0 unknown"):
            with self.subTest(invalid=invalid):
                pages = fixture("<f1r.P.1,P0> alpha.beta\n"
                                + invalid + "\n"
                                + "<f1r.P.2,P0> gamma.delta\n")
                self.assertEqual(pages["f1r"][0]["intervening_non_p"],
                                 [{"line": 2, "loc": "UNPARSED_LOCUS"}])
                self.assertEqual([r["y"] for r in module.candidates(pages, ["f1r"])],
                                 [0, 0])

    def test_valid_header_comment_and_other_page_are_not_barriers(self):
        pages = fixture("<f1r.P.1,P0> alpha\n"
                        "<f1r>\n"
                        "# ordinary comment\n"
                        "<f2r.P.2> malformed other page\n"
                        "<f1r.P.2,P0> beta\n")
        self.assertNotIn("intervening_non_p", pages["f1r"][0])
        self.assertEqual([r["y"] for r in module.candidates(pages, ["f1r"])], [1])

    def test_comma_without_locus_component_blocks_forged_positive(self):
        # Before this fix ROW matched these records, but len(parts)<2
        # silently dropped them and forged a P.1 -> P.2 positive.
        for invalid in ("<f1r,P0> orphan",
                        "<f1r,> orphan",
                        "<f1r,garbage> orphan"):
            with self.subTest(invalid=invalid):
                pages = fixture("<f1r.P.1,P0> alpha.beta\n"
                                + invalid + "\n"
                                + "<f1r.P.2,P0> gamma.delta\n")
                self.assertEqual(pages["f1r"][0]["intervening_non_p"],
                                 [{"line": 2, "loc": "UNPARSED_LOCUS"}])
                self.assertEqual([r["y"] for r in module.candidates(pages, ["f1r"])],
                                 [0, 0])

    def test_other_page_comma_without_locus_is_not_a_barrier(self):
        pages = fixture("<f1r.P.1,P0> alpha\n"
                        "<f2r,P0> orphan\n"
                        "<f1r.P.2,P0> beta\n")
        self.assertNotIn("intervening_non_p", pages["f1r"][0])
        self.assertEqual([r["y"] for r in module.candidates(pages, ["f1r"])], [1])

    def test_frozen_sources_have_no_comma_only_page_identifiers(self):
        # Authenticate immutable source bytes before asserting the scope.
        import re
        for label, path in module.INPUTS.items():
            with self.subTest(label=label):
                self.assertEqual(module.sha(path), module.EXPECTED_SHA256[label])
                suspect = []
                for lineno, raw in module.checked_physical_lines(
                        path.read_text(encoding="latin-1")):
                    parsed = module.ROW.match(raw.strip())
                    if not parsed or "," not in parsed["ident"]:
                        continue
                    ident = parsed["ident"].split(",", 1)[0]
                    if re.fullmatch(r"f(?:[0-9]+[rv][1-6]?|Ros)", ident):
                        suspect.append(lineno)
                self.assertEqual(suspect, [],
                                 f"{label}: comma without locus at {suspect}")

    def test_frozen_sources_have_no_unparsed_locus_rows(self):
        # Independently census the precise malformed-locus class; authenticate
        # both immutable source bytes before interpreting the result.
        import re
        for label, path in module.INPUTS.items():
            with self.subTest(label=label):
                self.assertEqual(module.sha(path), module.EXPECTED_SHA256[label])
                suspect = []
                for lineno, raw in module.checked_physical_lines(
                        path.read_text(encoding="latin-1")):
                    stripped = raw.strip()
                    if not re.match(r"^<(?:f[0-9]+[rv][1-6]?|fRos)\.", stripped):
                        continue
                    parsed = module.ROW.match(stripped)
                    if not parsed or "," not in parsed["ident"]:
                        suspect.append(lineno)
                self.assertEqual(suspect, [], f"{label}: unparsed loci at {suspect}")

    def test_frozen_corpus_scope_and_candidate_delta(self):
        # The legacy counterfactual is identical except that it removes
        # the new annotation, reproducing the previous candidate logic.
        # Historical deltas (71/64 and 72/72) were measured before
        # paragraph-marker barriers were introduced. Those numbers remain
        # archived in the original PR #148 report, but overlap with the
        # newly blocked paragraph transitions and must not be reasserted
        # against the corrected combined reader. CI 40898321137 exposed
        # the changed conditional deltas on the frozen source hashes.
        # The unsupported-symbol repair overlaps one ZL3b transition in
        # each policy: the earlier combined-reader conditional 37/33 is
        # preserved in PR #150; the CURRENT combined-reader delta is 36/32.
        # Failure evidence: CI run 40918868325. The 76 raw loci do not change.
        expected = {
            "ZL3b": {"raw_interposed": 76,
                      "primary": 36, "drop_uncertain_word": 32},
            "IT2a": {"raw_interposed": 73,
                      "primary": 37, "drop_uncertain_word": 37},
        }
        for label, path in module.INPUTS.items():
            self.assertEqual(module.sha(path), module.EXPECTED_SHA256[label])
            for policy in ("primary", "drop_uncertain_word"):
                with self.subTest(label=label, policy=policy):
                    # Historical conditional delta predates comma quarantine.
                    # Pin the old split policy to preserve that audit's scope.
                    pages = module.parse(path, policy, uncertain_space_policy="split")
                    interposed = sum(
                        bool(row.get("intervening_non_p"))
                        for lines in pages.values() for row in lines[:-1])
                    self.assertEqual(interposed, expected[label]["raw_interposed"])
                    # Preserve the historical conditional delta for PR #148:
                    # compare with and without the non-P guard under the
                    # PRE-ordinal reader. Otherwise the new locus-number
                    # check already blocks those gaps and makes this
                    # counterfactual falsely report zero. The separate
                    # ordinal-gap test measures the incremental new delta.
                    preordinal = copy.deepcopy(pages)
                    for lines in preordinal.values():
                        for row in lines:
                            row.pop("locus_number", None)
                    baseline = module.candidates(preordinal, sorted(preordinal))
                    legacy_pages = copy.deepcopy(preordinal)
                    for lines in legacy_pages.values():
                        for row in lines:
                            row.pop("intervening_non_p", None)
                    legacy = module.candidates(legacy_pages, sorted(legacy_pages))
                    removed = len(legacy) - len(baseline)
                    self.assertEqual(removed, expected[label][policy])
                    self.assertEqual(
                        sum(row["y"] for row in legacy) -
                        sum(row["y"] for row in baseline), removed)
                    print(f"{label} {policy}: {interposed} P-to-P transitions "
                          f"with intervening loci; {removed} legacy positive "
                          "candidates excluded; frozen source SHA-256 OK")


    def test_indented_page_and_locus_are_rejected(self):
        # The old raw.strip() silently promoted malformed physical rows.
        # Do not infer a line boundary from an indented source tag.
        for damaged in (" <f1r.P.2,P0> beta", "\t<f2r> page"):
            with self.subTest(damaged=damaged):
                with self.assertRaisesRegex(
                        ValueError, "Indented IVTFF structural row at source line 2"):
                    fixture("<f1r.P.1,P0> alpha\n" + damaged + "\n")

    def test_frozen_sources_have_no_indented_folio_rows(self):
        # Impact census only: hash-check originals; do not fit any model.
        for label, path in module.INPUTS.items():
            with self.subTest(label=label):
                self.assertEqual(module.sha(path), module.EXPECTED_SHA256[label])
                suspects = [
                    number for number, row in module.checked_physical_lines(
                        path.read_text(encoding="latin-1"))
                    if row.lstrip(" \t") != row and
                    row.lstrip(" \t").startswith("<f")
                ]
                self.assertEqual(suspects, [], f"{label}: indented folio rows {suspects}")


if __name__ == "__main__":
    unittest.main()
