#!/usr/bin/env python3
"""EXP-259: provenance and reader-scope regression tests."""
import tempfile
import unittest
from pathlib import Path
from scripts import audit_exp259_latin_claim as scope


class Exp259ComparatorScopeTests(unittest.TestCase):
    def test_historical_reader_does_not_filter_language(self):
        reader = scope.load_historical_reader((scope.ROOT / scope.SCRIPT).read_bytes())
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "mixed.txt"
            path.write_text("AMO ET\nTHE AND\n", encoding="utf-8")
            self.assertEqual(reader(str(path)), ["amo", "et", "the", "and"])

    def test_bilingual_adjudication_cannot_be_relabelled(self):
        row = {"issue": "BILINGUAL_REQUIRES_FILTER_AUDIT",
               "adjudicated_language": "Latin and English",
               "adjudicated_work": "De Officiis #47001",
               "evidence": ["WITH AN ENGLISH TRANSLATION BY"]}
        scope.check_bilingual_adjudication(row)
        with self.assertRaisesRegex(ValueError, "not adjudicated as bilingual"):
            scope.check_bilingual_adjudication(dict(row, adjudicated_language="Latin"))
        with self.assertRaisesRegex(ValueError, "evidence missing"):
            scope.check_bilingual_adjudication(dict(row, evidence=[]))

    def test_duplicate_identity_entries_rejected(self):
        rows = [{"path": scope.CORPUS}, {"path": scope.CORPUS}]
        with self.assertRaisesRegex(ValueError, "exactly one entry"):
            scope.require_unique_path(rows, scope.CORPUS, "test")

    def test_duplicate_json_members_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate JSON key"):
            scope.json.loads('{"issue":"a","issue":"b"}',
                             object_pairs_hook=scope.strict_object)

    def test_linked_erratum_is_required_and_scope_is_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            correction = root / scope.CORRECTION
            with self.assertRaisesRegex(ValueError, "adjacent CORRECTION.md missing"):
                scope.check_linked_correction(root)
            correction.parent.mkdir(parents=True)
            correction.write_text("\\n".join(scope.CORRECTION_MARKERS), encoding="utf-8")
            self.assertEqual(len(scope.check_linked_correction(root)), 64)
            correction.write_text("\\n".join(scope.CORRECTION_MARKERS[:-1]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing required marker"):
                scope.check_linked_correction(root)

    def test_actual_frozen_reference_and_claims(self):
        result = scope.audit()
        self.assertEqual(result["status"], "INVALID_FOR_CLAIM")
        self.assertEqual(result["historical_reference_tokens_replayed"], 112081)
        self.assertEqual(result["reference_sha256"], scope.CORPUS_SHA256)
        self.assertEqual(result["source_script_git_blob"], scope.SCRIPT_BLOB)
        self.assertEqual(result["linked_correction_path"], scope.CORRECTION)
        self.assertEqual(len(result["linked_correction_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
