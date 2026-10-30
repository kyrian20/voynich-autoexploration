"""Read-only provenance classification of LIB-EXP-624's curated Library JSON."""
import hashlib
import json
import unittest
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from scripts import audit_library_exp624_archive_format as audit


SCRIPT = b'''def main():\n    results = {"experiment": "exp624_position_conditioned_character_model", "method": {}, "datasets": {}}\n'''


def summary():
    def row(n, tokenizer):
        return {"tokenizer": tokenizer, "split_deltas": [0.5] * n,
                "splits_total": n, "split_delta_min": 0.5, "split_delta_max": 0.5,
                "mean_real_holdout_bits_per_unit": 1.5,
                "mean_null_holdout_bits_per_unit": 2.0,
                "mean_null_minus_real_bits_per_unit": 0.5,
                "relative_real_loss_reduction_percent": 25.0}
    return {"experiment": "exp624_position_conditioned_character_model",
            "date": "2026-10-20", "source_data": {}, "method": {},
            "ZL3b": {"parsed_folios_with_body": 203,
                      "results": [row(8, "raw EVA letters"), row(8, "EVA units with ch/sh collapsed")],
                      "currier_strata": [dict(row(6, mode), currier=lang)
                                         for lang in ("A", "B") for mode in ("raw", "glyph")]},
            "IT2a": {"parsed_folios_with_body": 203,
                      "results": [row(8, "raw EVA letters"), row(8, "EVA units with ch/sh collapsed")]},
            "interpretation": "Exploratory only"}


class LibraryExp624ArchiveFormatTests(unittest.TestCase):
    def test_curated_summary_is_not_native_output(self):
        raw = json.dumps(summary()).encode()
        report = b"archived report"
        hashes = {name: hashlib.sha256(value).hexdigest()
                  for name, value in (("script", SCRIPT), ("results", raw), ("report", report))}
        result = audit.audit(SCRIPT, raw, report, hashes)
        self.assertEqual(result["status"], "ARCHIVED_CURATED_SUMMARY_NOT_NATIVE_SCRIPT_OUTPUT")
        self.assertFalse(result["historical_reproduction"])
        self.assertEqual(result["checked_rows"]["ZL3b"]["split_deltas_checked"], 40)
        self.assertEqual(result["checked_rows"]["IT2a"]["split_deltas_checked"], 16)
        self.assertEqual(result["relative_percentage_audit"]["rows_checked"], 8)
        self.assertEqual(result["relative_percentage_audit"]["discrepancies"], [])

    def test_hash_gate(self):
        raw = json.dumps(summary()).encode()
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            audit.audit(SCRIPT, raw, b"report")

    def test_duplicate_keys_and_nonfinite_rejected(self):
        for data in (b'{"a": 1, "a": 2}', b'{"a": NaN}', b'{"a": Infinity}'):
            with self.subTest(data=data), self.assertRaises(ValueError):
                audit.strict_json(data)

    def test_overflowed_json_exponents_fail_closed(self):
        # parse_constant alone does not catch overflow in JSON's number grammar.
        for raw in (b'{"x": 1e400}', b'{"x": -1e400}',
                    b'{"nested": {"x": 1e400}}'):
            with self.subTest(raw=raw), self.assertRaisesRegex(ValueError, "Non-finite JSON float"):
                audit.strict_json(raw)
        self.assertEqual(audit.strict_json(b'{"x": 1.5e2}')["x"], 150.0)

    def test_nonfinite_or_nonnumeric_means_fail_closed(self):
        fields = ("mean_real_holdout_bits_per_unit",
                  "mean_null_holdout_bits_per_unit",
                  "mean_null_minus_real_bits_per_unit",
                  "split_delta_min", "split_delta_max")
        for field in fields:
            for value in (float("inf"), -float("inf"), float("nan"), "0.5", True):
                with self.subTest(field=field, value=repr(value)):
                    data = summary()
                    data["IT2a"]["results"][0][field] = value
                    with self.assertRaisesRegex(ValueError, "invalid " + field):
                        audit.validate_summary(data)

    def test_malformed_delta_and_wrong_shape_fail_closed(self):
        data = summary()
        data["IT2a"]["results"][0]["split_deltas"][0] = 2.0
        with self.assertRaisesRegex(ValueError, "delta mean inconsistent"):
            audit.validate_summary(data)
        data = summary()
        data["IT2a"]["results"].pop()
        with self.assertRaisesRegex(ValueError, "two overall tokenizers"):
            audit.validate_summary(data)

    def test_overall_tokenizer_identities_cannot_be_duplicated_or_relabelled(self):
        # Previously a two-row summary with two identical tokenizers passed
        # validation. The auditor must preserve the identity of both views.
        for edition in ("ZL3b", "IT2a"):
            for replacement in ("raw EVA letters", "unverified tokenizer", None):
                with self.subTest(edition=edition, replacement=replacement):
                    data = summary()
                    data[edition]["results"][1]["tokenizer"] = replacement
                    with self.assertRaisesRegex(ValueError, "identities missing or duplicated"):
                        audit.validate_summary(data)
        # Order is not scientifically meaningful: identity, not position, matters.
        data = summary()
        data["ZL3b"]["results"].reverse()
        data["IT2a"]["results"].reverse()
        self.assertEqual(audit.validate_summary(data)["ZL3b"]["overall_rows"], 2)

    def test_ast_not_executed_and_dynamic_schema_rejected(self):
        self.assertEqual(audit.native_root_keys(SCRIPT.decode()), {"experiment", "method", "datasets"})
        with self.assertRaisesRegex(ValueError, "Dynamic native output key"):
            audit.native_root_keys('def main():\n    results = {get_key(): 1, "datasets": {}}\n')

    def test_saved_receipt_matches_pinned_source_hashes(self):
        root = Path(__file__).resolve().parents[1]
        receipt = audit.strict_json(
            (root / "research/maintenance/2026-10-30-lib-exp624-library-native-format-evidence.json").read_bytes()
        )
        self.assertEqual(receipt["sha256"], audit.EXPECTED_SHA256)
        self.assertEqual(receipt["status"], "ARCHIVED_CURATED_SUMMARY_NOT_NATIVE_SCRIPT_OUTPUT")
        self.assertFalse(receipt["historical_reproduction"])
        self.assertEqual(sum(x["split_deltas_checked"] for x in receipt["checked_rows"].values()), 56)


    def test_relative_percentage_rounding_discrepancy_is_not_silenced(self):
        # Real archived IT2a glyph mean fields, but a synthetic complete row:
        # this test does not access the private Library JSON in CI.
        data = summary()
        row = data["IT2a"]["results"][1]
        row["mean_null_holdout_bits_per_unit"] = 3.8357742633
        row["mean_null_minus_real_bits_per_unit"] = 0.9498638385
        row["mean_real_holdout_bits_per_unit"] = 2.8859104248
        row["split_deltas"] = [0.9498638385] * 8
        row["split_delta_min"] = row["split_delta_max"] = 0.9498638385
        row["relative_real_loss_reduction_percent"] = 24.77
        audit.validate_summary(data)  # All pre-existing numeric checks pass.
        result = audit.audit_relative_percentages(data)
        self.assertEqual(result["rows_checked"], 8)
        self.assertEqual(len(result["discrepancies"]), 1)
        discrepancy = result["discrepancies"][0]
        self.assertEqual((discrepancy["edition"], discrepancy["stratum"]),
                         ("IT2a", "all"))
        self.assertEqual(discrepancy["expected_percent_2dp"], "24.76")
        self.assertEqual(discrepancy["reported_percent"], "24.77")

    def test_relative_percentage_invalid_type_fails_closed(self):
        for value in (True, "25.00", float("nan"), float("inf")):
            with self.subTest(value=repr(value)):
                data = summary()
                data["IT2a"]["results"][0]["relative_real_loss_reduction_percent"] = value
                with self.assertRaisesRegex(ValueError, "invalid relative_real_loss_reduction_percent"):
                    audit.audit_relative_percentages(data)

    def test_archived_percentage_receipt_is_self_consistent(self):
        # This frozen derived receipt is NOT a substitute for Library bytes.
        root = Path(__file__).resolve().parents[1]
        receipt = json.loads((root / "research/maintenance" /
            "2026-10-30-lib-exp624-percentage-evidence.json").read_text(encoding="utf-8"))
        self.assertEqual(receipt["source_sha256"], audit.EXPECTED_SHA256["results"])
        self.assertEqual(receipt["source_bytes"], 8141)
        self.assertEqual(len(receipt["rows"]), 8)
        discrepancies = []
        for row in receipt["rows"]:
            calculated = Decimal(100) * Decimal(row["mean_delta"]) / Decimal(row["mean_null"])
            expected = calculated.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if expected != Decimal(row["reported_percent"]):
                discrepancies.append((row["edition"], row["stratum"], row["tokenizer"],
                                      str(expected), row["reported_percent"]))
        self.assertEqual(len(discrepancies), receipt["expected_discrepancy_count"])
        self.assertEqual(discrepancies, [("IT2a", "all", "EVA units with ch/sh collapsed",
                                          "24.76", "24.77")])


if __name__ == "__main__":
    unittest.main()
