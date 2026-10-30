"""Adversarial and real-source checks for high-ASCII code adjacency census."""
import unittest

from scripts import audit_exp590_high_ascii_adjacency as audit
from scripts.ivtff_lossless import lex


class HighAsciiAdjacencyTests(unittest.TestCase):
    def test_direct_ascii_neighbors_are_not_decoded(self):
        source = (
            "<f1r.1,@P0> qo@140;dy.daiin\n"
            "<f1r.2,@P0> @140;dy\n"
            "<f1r.3,@P0> qo@140;\n"
            "<f1r.4,@P0> @140;\n"
            "<f1r.5,@P0> {c@132;h}\n"
        )
        report = audit.analyze_text(source)
        self.assertEqual(report["rows_with_primary_high_ascii"], 5)
        self.assertEqual(report["primary_high_ascii_codes"], 5)
        self.assertEqual(report["codes_with_ascii_left"], 3)
        self.assertEqual(report["codes_with_ascii_right"], 3)
        self.assertEqual(report["codes_with_ascii_both_sides"], 2)
        self.assertEqual(report["codes_with_no_direct_ascii_neighbor"], 1)
        self.assertEqual(report["rows_with_at_least_one_ascii_neighbor"], 4)
        self.assertEqual(report["affected_rows"][0]["locus"], "f1r.1")
        self.assertEqual(report["affected_rows"][0]["adjacent_codes"][0]["code"], "@140;")

    def test_comments_and_unselected_alternatives_are_not_counted(self):
        source = (
            "<f1r.1,@P0> a<!@140;>b.[a:@190;].@140;\n"
            "<f1r.2,@P0> [@140;:b].a@142;b\n"
        )
        report = audit.analyze_text(source)
        self.assertEqual(report["primary_high_ascii_codes"], 2)
        self.assertEqual(report["codes_with_ascii_both_sides"], 1)
        self.assertEqual(report["codes_with_no_direct_ascii_neighbor"], 1)

    def test_nonascii_and_out_of_range_codes_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "Non-ASCII"):
            list(audit.primary_codes(lex("@١٤٠;").spans))
        with self.assertRaisesRegex(ValueError, "outside 128"):
            list(audit.primary_codes(lex("@999;").spans))
        with self.assertRaisesRegex(ValueError, "Non-physical"):
            audit.analyze_text("# comment\u2028<f1r.1,@P0> qo@140;dy\n")

    def test_frozen_corpora_have_expected_inventory(self):
        result = audit.audit()
        self.assertEqual(result["status"], "DESCRIPTIVE_SOURCE_ADJACENCY_ONLY")
        self.assertFalse(result["historical_exp590_reexecuted"])
        self.assertFalse(result["heldout_evaluation_performed"])
        for label, expected in audit.EXPECTED_CODE_COUNTS.items():
            source = result["sources"][label]
            self.assertEqual((source["rows_with_primary_high_ascii"],
                              source["primary_high_ascii_codes"]), expected)
            self.assertEqual(
                source["codes_with_at_least_one_ascii_neighbor"] +
                source["codes_with_no_direct_ascii_neighbor"],
                source["primary_high_ascii_codes"],
            )
            self.assertLessEqual(source["codes_with_ascii_both_sides"],
                                 source["codes_with_at_least_one_ascii_neighbor"])


if __name__ == "__main__":
    unittest.main()
