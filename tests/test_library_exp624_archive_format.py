"""Read-only provenance classification of LIB-EXP-624's curated Library JSON."""
import hashlib
import json
import unittest
from pathlib import Path
from scripts import audit_library_exp624_archive_format as audit


SCRIPT = b'''def main():\n    results = {"experiment": "exp624_position_conditioned_character_model", "method": {}, "datasets": {}}\n'''


def summary():
    def row(n, tokenizer):
        return {"tokenizer": tokenizer, "split_deltas": [0.5] * n,
                "splits_total": n, "split_delta_min": 0.5, "split_delta_max": 0.5,
                "mean_real_holdout_bits_per_unit": 1.5,
                "mean_null_holdout_bits_per_unit": 2.0,
                "mean_null_minus_real_bits_per_unit": 0.5}
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


if __name__ == "__main__":
    unittest.main()
