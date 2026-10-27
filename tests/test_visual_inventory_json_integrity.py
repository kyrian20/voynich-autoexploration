"""Fail closed on ambiguous JSON in the frozen L/R inventory, at every depth.

These are operational input-integrity tests, not an IVTFF or semantic audit.
The archived gzip and source transcriptions are never rewritten.
"""
import gzip
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.audit_label_partition_coverage import load_verified_coverage_inputs
from scripts.audit_visual_inventory_source_rows import main as source_rows_main
from scripts.audit_visual_inventory_completeness import main as completeness_main
from scripts.audit_visual_inventory_projections import main as projections_main
from scripts.prepare_visual_annotation_queue import prepare_verified_queue
from scripts.select_visual_pilot_v2 import load_unique_inventory, main as pilot_main


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json"
INVENTORY = ROOT / "research/decipherment/2026-10-25-label-inventory/inventory.json.gz"


class VisualInventoryJsonIntegrityTests(unittest.TestCase):
    @staticmethod
    def pack(text):
        return gzip.compress(text.encode("utf-8"), mtime=0)

    def test_valid_json_and_archived_inventory_unchanged(self):
        self.assertEqual(load_unique_inventory(self.pack('{"sources":[],"records":[]}')),
                         {"sources": [], "records": []})
        archived = INVENTORY.read_bytes()
        decoded = json.loads(gzip.decompress(archived))
        strict = load_unique_inventory(archived)
        self.assertEqual(len(strict["records"]), len(decoded["records"]))
        self.assertEqual(strict, decoded)

    def test_duplicate_top_level_key_rejected_instead_of_last_value_wins(self):
        text = '{"sources":[],"sources":[{"edition":"forged"}],"records":[]}'
        self.assertEqual(json.loads(text)["sources"], [{"edition": "forged"}])
        with self.assertRaisesRegex(ValueError, "Duplicate visual inventory JSON key: sources"):
            load_unique_inventory(self.pack(text))

    def test_duplicate_nested_row_and_projection_key_rejected(self):
        for text, key in (
            ('{"records":[{"folio":"f2r","folio":"f99r"}]}', "folio"),
            ('{"records":[{"views":{"split/primary/expand":{"tokens":["ok"],"tokens":["fake"]}}}]}',
             "tokens"),
            ('{"sources":[{"sha256":"real","sha256":"fake"}]}', "sha256"),
        ):
            with self.subTest(key=key):
                with self.assertRaisesRegex(ValueError, "Duplicate visual inventory JSON key: " + key):
                    load_unique_inventory(self.pack(text))

    def test_coverage_and_queue_reject_ambiguous_inventory_before_export(self):
        ambiguous = self.pack('{"sources":[],"sources":[],"records":[]}')
        manifest_bytes = MANIFEST.read_bytes()
        with self.assertRaisesRegex(ValueError, "Duplicate visual inventory JSON key"):
            load_verified_coverage_inputs(ambiguous, manifest_bytes, ROOT)
        with self.assertRaisesRegex(ValueError, "Duplicate visual inventory JSON key"):
            prepare_verified_queue(ambiguous, manifest_bytes, ROOT)

    def test_pilot_cli_rejects_ambiguous_archive_without_creating_output(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "ambiguous.json.gz"
            output = Path(temp) / "selection.json"
            source.write_bytes(self.pack('{"records":[],"records":[]}'))
            argv = ["select_visual_pilot_v2.py", "--inventory", str(source),
                    "--manifest", str(MANIFEST), "--out", str(output)]
            with patch("sys.argv", argv):
                with self.assertRaisesRegex(ValueError, "Duplicate visual inventory JSON key"):
                    pilot_main()
            self.assertFalse(output.exists())


    def test_audit_clis_reject_duplicate_manifest_keys_before_reporting(self):
        with tempfile.TemporaryDirectory() as temp:
            manifest = Path(temp) / "ambiguous-manifest.json"
            manifest.write_text('{"corpora":{},"corpora":{}}', encoding="utf-8")
            for name, entrypoint in (
                ("source_rows", source_rows_main),
                ("completeness", completeness_main),
                ("projections", projections_main),
            ):
                with self.subTest(entrypoint=name):
                    output = Path(temp) / (name + ".json")
                    argv = [name, "--root", str(ROOT), "--manifest", str(manifest),
                            "--out", str(output)]
                    with patch("sys.argv", argv):
                        with self.assertRaisesRegex(ValueError, "Duplicate holdout manifest JSON key"):
                            entrypoint()
                    self.assertFalse(output.exists())

    def test_audit_cli_rejects_same_size_train_test_swap(self):
        manifest = json.loads(MANIFEST.read_bytes())
        train, test = manifest["partitions"]["train"], manifest["partitions"]["test"]
        train[0], test[0] = test[0], train[0]
        train.sort()
        test.sort()
        with tempfile.TemporaryDirectory() as temp:
            altered = Path(temp) / "swapped-manifest.json"
            output = Path(temp) / "report.json"
            altered.write_text(json.dumps(manifest), encoding="utf-8")
            argv = ["source_rows", "--root", str(ROOT), "--manifest", str(altered),
                    "--out", str(output)]
            with patch("sys.argv", argv):
                with self.assertRaisesRegex(ValueError, "Partition hash assignment mismatch"):
                    source_rows_main()
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
