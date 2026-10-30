"""Regression for the real nine/eight IVTFF high-ASCII-only record omissions."""
import unittest

from scripts import audit_ivtff_high_ascii_coverage as audit
from scripts.ivtff_lossless import lex
from scripts.ivtff_rows import tokens_rows


class HighAsciiCoverageTests(unittest.TestCase):
    def test_opaque_codes_are_tokens_not_empty_rows(self):
        source = (
            "<f1r.1,@P0> @140;\n"
            "<f1r.2,@P0> @172;<!cf f57v?>\n"
            "<f1r.3,@P0> qo@140;dy.daiin\n"
            "<f1r.4,@P0> daiin.[x:@192;].{c@132;h}od\n"
            "<f1r.5,@P0> ?\n"
        )
        result = audit.analyze_text(source)
        self.assertEqual(result["nonempty_text_records"], 5)
        self.assertEqual(result["ascii_tokenized_records"], 2)
        self.assertEqual(result["records_with_selected_high_ascii"], 4)
        self.assertEqual(result["selected_high_ascii_codes"], 4)
        self.assertEqual(result["high_ascii_only_records"], 2)
        self.assertEqual(result["unreadable_only_records"], 1)
        self.assertEqual([r["locus"] for r in result["ascii_omitted_but_opaque_nonempty"]],
                         ["f1r.1", "f1r.2", "f1r.5"])
        self.assertEqual([r["opaque_tokens"] for r in result["ascii_omitted_but_opaque_nonempty"]],
                         [["@140;"], ["@172;"], ["?"]])
        self.assertEqual(tokens_rows([lex("qo@140;dy.daiin")]),
                         ["qo@140;dy", "daiin"])

    def test_comments_and_unselected_alternatives_are_not_evidence(self):
        spans = lex("a<!@140;>.[x:@190;].{c@132;h}").spans
        self.assertEqual(audit.selected_codes(spans), ["@132;"])
        with self.assertRaisesRegex(ValueError, "Unadjudicated ASCII-empty"):
            audit.analyze_text("<f1r.1,@P0> [x:@190;]\n")

    def test_fail_closed_invalid_high_ascii_and_physical_rows(self):
        with self.assertRaisesRegex(ValueError, "Non-ASCII"):
            audit.selected_codes(lex("@١٤٠;").spans)
        with self.assertRaisesRegex(ValueError, "outside 128"):
            audit.selected_codes(lex("@999;").spans)
        with self.assertRaisesRegex(ValueError, "Non-physical"):
            audit.analyze_text("# comment\u2028<f1r.1,@P0> @140;\n")

    def test_malformed_primary_code_cannot_be_silently_counted_as_zero(self):
        # Prior to the guard, a mixed ASCII row passed with zero codes
        # because the lossless lexer's diagnostic was not inspected.
        for body in ("qo@12;dy", "a.@12;", "{c@12;h}.a"):
            with self.subTest(body=body):
                with self.assertRaisesRegex(ValueError, "Malformed primary"):
                    audit.analyze_text(f"<f1r.1,@P0> {body}\n")
        # This inventory deliberately excludes unselected alternatives
        # and free-text comments; neither contributes a primary code.
        result = audit.analyze_text(
            "<f1r.1,@P0> a.[@12;:b].<!@12;>c\n"
        )
        self.assertEqual(result["selected_high_ascii_codes"], 0)

    def test_unclosed_primary_containers_cannot_hide_high_ascii_codes(self):
        # Previously these rows passed with zero selected codes despite a
        # visible @140; inside an unterminated primary container.
        for body in ("{c@140;h", "a.[b:@140;", "a.<!@140;"):
            with self.subTest(body=body):
                with self.assertRaisesRegex(ValueError, "Unclosed primary"):
                    audit.analyze_text(f"<f1r.1,@P0> {body}\\n".replace("\\n", "\n"))

    def test_frozen_corpus_reconciliation(self):
        report = audit.audit()
        self.assertEqual(report["status"], "REPRODUCED_SCOPE_ONLY")
        self.assertFalse(report["historical_experiment_reexecuted"])
        for label, expected in audit.EXPECTED.items():
            result = report["sources"][label]
            actual = (result["nonempty_text_records"],
                      result["ascii_tokenized_records"],
                      result["records_with_selected_high_ascii"],
                      result["selected_high_ascii_codes"],
                      result["high_ascii_only_records"],
                      result["unreadable_only_records"],
                      tuple(r["locus"] for r in result["ascii_omitted_but_opaque_nonempty"]))
            self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
