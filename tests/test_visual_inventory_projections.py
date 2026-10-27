"""Synthetic regressions for archived L/R token-view replay; no semantic scoring."""
import copy
import hashlib
import tempfile
import unittest
from pathlib import Path

from scripts.audit_visual_inventory_projections import replay
from scripts.build_label_occurrence_inventory import extract


class ArchivedVisualProjectionTests(unittest.TestCase):
    def fixture(self, root, body="otaim,dam.alam"):
        path = "data/transcriptions/eva_zl3b.txt"
        raw = ("<f2r> <! $L=A>\n<f2r.14,@Lp> " + body + "\n").encode()
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        source_sha = hashlib.sha256(raw).hexdigest()
        rows, excluded, unparsed = extract(raw.decode(), "ZL3b", source_sha, {})
        self.assertEqual((len(rows), len(excluded), len(unparsed)), (1, 0, 0))
        inventory = {
            "sources": [{"edition": "ZL3b", "path": path, "sha256": source_sha,
                         "selected_rows": 1, "excluded_rows": []}],
            "records": rows,
        }
        manifest = {"corpora": {target.name: {"path": path, "sha256": source_sha}}}
        return inventory, manifest

    def test_eight_policies_replay_on_exact_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            inv, manifest = self.fixture(root)
            result = replay(inv, manifest, root)
            self.assertEqual(result["rows_checked"], 1)
            self.assertEqual(result["views_checked"], 8)
            self.assertEqual(result["views_with_errors"], 0)

    def test_changed_token_projection_rejected_even_with_correct_source_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            inv, manifest = self.fixture(root)
            inv["records"][0]["views"]["split/primary/expand"]["tokens"] = ["fabricated"]
            with self.assertRaisesRegex(ValueError, "Archived projection differs"):
                replay(inv, manifest, root)

    def test_missing_and_extra_policy_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            inv, manifest = self.fixture(root)
            inv["records"][0]["views"].pop("join/primary/opaque")
            with self.assertRaisesRegex(ValueError, "policy set differs"):
                replay(inv, manifest, root)
            inv, manifest = self.fixture(root)
            inv["records"][0]["views"]["unregistered"] = {"tokens": [], "error": None}
            with self.assertRaisesRegex(ValueError, "policy set differs"):
                replay(inv, manifest, root)

    def test_changed_diagnostics_and_error_projection_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            inv, manifest = self.fixture(root, "[unclosed")
            self.assertEqual(replay(inv, manifest, root)["views_with_errors"], 8)
            inv["records"][0]["lexer_diagnostics"] = []
            with self.assertRaisesRegex(ValueError, "lexer diagnostics differ"):
                replay(inv, manifest, root)
            inv, manifest = self.fixture(root, "[unclosed")
            inv["records"][0]["views"]["split/primary/expand"]["error"] = None
            with self.assertRaisesRegex(ValueError, "Archived projection differs"):
                replay(inv, manifest, root)

    def test_unreviewed_row_cannot_be_promoted_to_semantic_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            inv, manifest = self.fixture(root)
            inv["records"][0]["eligible_for_semantic_evaluation"] = True
            with self.assertRaisesRegex(ValueError, "promoted to semantic evidence"):
                replay(inv, manifest, root)
            inv, manifest = self.fixture(root)
            inv["records"][0]["external_referent"] = "invented"
            with self.assertRaisesRegex(ValueError, "promoted to semantic evidence"):
                replay(inv, manifest, root)

    def test_source_line_forgery_still_blocked_before_projection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            inv, manifest = self.fixture(root)
            inv["records"][0]["raw_line"] = "<f2r.14,@Lp> forged"
            with self.assertRaisesRegex(ValueError, "raw_line differs"):
                replay(inv, manifest, root)

    def test_omitted_selected_row_still_blocked_before_projection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            inv, manifest = self.fixture(root)
            inv["records"].clear()
            with self.assertRaises(ValueError):
                replay(inv, manifest, root)


if __name__ == "__main__":
    unittest.main()
