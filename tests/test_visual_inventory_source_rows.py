"""Synthetic regression tests for exact row-to-source provenance binding."""
import copy
import hashlib
import tempfile
import unittest
from pathlib import Path

from scripts.audit_visual_inventory_source_rows import audit, sha256


class VisualInventorySourceRowsTests(unittest.TestCase):
    def fixture(self, root):
        path = "data/transcriptions/eva_zl3b.txt"
        raw = b"<f2r> <! $L=A>\n<f2r.14,@Lp> daiin\n"
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        source_hash = sha256(raw)
        line = raw.decode().splitlines()[1]
        record = {
            "edition": "ZL3b", "source_sha256": source_hash,
            "source_line": 2, "occurrence_id": "ZL3b:2",
            "raw_line": line, "raw_line_sha256": sha256(line.encode()),
            "folio": "f2r", "locus_id": "14", "id": "f2r.14",
            "raw_body": "daiin", "locus": "Lp",
        }
        inventory = {"sources": [{"edition": "ZL3b", "path": path,
                                  "sha256": source_hash}],
                     "records": [record]}
        manifest = {"corpora": {target.name: {"path": path,
                                               "sha256": source_hash}}}
        return inventory, manifest

    def test_exact_line_binding_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            inventory, manifest = self.fixture(Path(temp))
            result = audit(inventory, manifest, Path(temp))
            self.assertEqual(result["record_count"], 1)
            self.assertEqual(result["records_by_edition"], {"ZL3b": 1})

    def test_reject_wrong_line_even_with_valid_source_hash(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inventory, manifest = self.fixture(root)
            inventory["records"][0]["source_line"] = 1
            inventory["records"][0]["occurrence_id"] = "ZL3b:1"
            with self.assertRaisesRegex(ValueError, "raw_line differs"):
                audit(inventory, manifest, root)

    def test_reject_forged_body_and_locator(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inventory, manifest = self.fixture(root)
            inventory["records"][0]["raw_body"] = "fake"
            with self.assertRaisesRegex(ValueError, "fields differ"):
                audit(inventory, manifest, root)
            inventory, manifest = self.fixture(root)
            inventory["records"][0]["id"] = "f2r.99"
            with self.assertRaisesRegex(ValueError, "fields differ"):
                audit(inventory, manifest, root)

    def test_reject_wrong_line_hash(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inventory, manifest = self.fixture(root)
            inventory["records"][0]["raw_line_sha256"] = "0" * 64
            with self.assertRaisesRegex(ValueError, "raw_line_sha256 mismatch"):
                audit(inventory, manifest, root)

    def test_reject_duplicate_physical_line_with_distinct_occurrence(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inventory, manifest = self.fixture(root)
            other = copy.deepcopy(inventory["records"][0])
            other["id"] = "f2r.99"
            other["occurrence_id"] = "ZL3b:other"
            inventory["records"].append(other)
            with self.assertRaisesRegex(ValueError, "Duplicate physical source line"):
                audit(inventory, manifest, root)

    def test_reject_non_integer_line_and_wrong_occurrence(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inventory, manifest = self.fixture(root)
            inventory["records"][0]["source_line"] = True
            with self.assertRaisesRegex(ValueError, "Invalid inventory source_line"):
                audit(inventory, manifest, root)
            inventory, manifest = self.fixture(root)
            inventory["records"][0]["occurrence_id"] = "ZL3b:1"
            with self.assertRaisesRegex(ValueError, "occurrence/source_line mismatch"):
                audit(inventory, manifest, root)

    def test_reject_modified_original_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inventory, manifest = self.fixture(root)
            (root / inventory["sources"][0]["path"]).write_bytes(b"tampered")
            with self.assertRaisesRegex(ValueError, "Source bytes differ"):
                audit(inventory, manifest, root)


if __name__ == "__main__":
    unittest.main()
