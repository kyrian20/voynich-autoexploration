"""Regression tests for the non-decoding EXP-590 high-ASCII token policy."""
import unittest

from scripts import audit_exp590_opaque_token_sensitivity as audit


class OpaqueTokenSensitivityTests(unittest.TestCase):
    def test_synthetic_split_and_final_position(self):
        source = (
            "<f1r.1,@P0> a@140;b.daiin\n"
            "<f1r.2,@P0> daiin.@140;\n"
            "<f1r.3,@P0> {c@132;h}.a<!@150;>b.[@155;:a].@141;\n"
            "<f1r.4,@P0> @140;\n"
            "<f1r.5,@P0> x{c@140;h}y.[@141;:a].<!@142;>z\n"
        )
        result = audit.analyze_text(source)
        self.assertEqual(result["physical_locus_records"], 5)
        self.assertEqual(result["historical"], {
            "lines_with_tokens": 4, "tokens": 9, "exact_daiin": 2,
            "initial_daiin_lines": 1, "final_daiin_lines": 2,
        })
        self.assertEqual(result["opaque_marker"], {
            "lines_with_tokens": 5, "tokens": 11, "exact_daiin": 2,
            "initial_daiin_lines": 1, "final_daiin_lines": 1,
        })
        self.assertEqual(result["changed_records"], 4)
        self.assertEqual(result["previously_ascii_empty_now_opaque"], 1)
        self.assertEqual(result["changed_initial_daiin_records"], 0)
        self.assertEqual(result["changed_final_daiin_records"], 1)
        self.assertEqual(result["changed_rows"][0]["opaque_tokens"], ["a¤b", "daiin"])

    def test_no_decoding_and_excluded_markup(self):
        old, new = audit.views("qo@140;dy.[@141;:a].{c@142;h}.<!@143;>daiin")
        self.assertEqual(old, ["qo", "dy", "daiin"])
        self.assertEqual(new, ["qo¤dy", "daiin"])
        self.assertEqual(audit.views("a?b"), (["a", "b"], ["a", "b"]))
        with self.assertRaisesRegex(ValueError, "sentinel"):
            audit.views("a¤b")

    def test_reject_nonphysical_line_break(self):
        with self.assertRaisesRegex(ValueError, "Non-physical"):
            audit.analyze_text("# comment\u2028<f1r.1,@P0> daiin\n")

    def test_frozen_sources_and_exact_target_endpoint_delta(self):
        result = audit.audit()
        self.assertEqual(result["status"], "DESCRIPTIVE_OPAQUE_TOKEN_SENSITIVITY_ONLY")
        self.assertFalse(result["historical_exp590_reexecuted"])
        self.assertFalse(result["heldout_evaluation_performed"])
        expected = {
            "ZL3b": (5385, 5376, 5385, 39594, 39610, 853, 161, 134, 133, 85, 9),
            "ZL3a": (5389, 5380, 5388, 39596, 39614, 853, 161, 134, 133, 81, 8),
            "IT2a": (5215, 5207, 5207, 37945, 37945, 865, 157, 134, 134, 0, 0),
        }
        for label, e in expected.items():
            with self.subTest(label=label):
                row = result["sources"][label]
                h, o = row["historical"], row["opaque_marker"]
                self.assertEqual((
                    row["physical_locus_records"],
                    h["lines_with_tokens"], o["lines_with_tokens"],
                    h["tokens"], o["tokens"],
                    h["exact_daiin"], h["initial_daiin_lines"],
                    h["final_daiin_lines"], o["final_daiin_lines"],
                    row["changed_records"], row["previously_ascii_empty_now_opaque"],
                ), e)
                self.assertEqual(h["exact_daiin"], o["exact_daiin"])
                self.assertEqual(h["initial_daiin_lines"], o["initial_daiin_lines"])
                self.assertEqual(row["changed_initial_daiin_records"], 0)
                self.assertEqual(row["changed_final_daiin_records"], int(label != "IT2a"))
                self.assertEqual(
                    sum(x["delta_token_count"] for x in row["changed_rows"]),
                    o["tokens"] - h["tokens"],
                )


if __name__ == "__main__":
    unittest.main()
