"""Regression: future line-boundary artifacts must be strict JSON and fail closed.

No historical results.json, corpus, holdout manifest or scientific metric is
modified or recomputed by these synthetic writer tests.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = (Path(__file__).resolve().parents[1] / "research" / "analysis" /
          "2026-10-28-line-boundary-reproduction" / "line_boundary_replication.py")
spec = importlib.util.spec_from_file_location("line_boundary_strict_json", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class StrictJsonArtifactContract(unittest.TestCase):
    def test_valid_payload_round_trips_and_ends_with_newline(self):
        payload = {"source_sha256": "f" * 64, "score": 0.125,
                   "folds": [0, 1], "note": "revisión"}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "new.json"
            module.write_new_result(path, payload)
            raw = path.read_text(encoding="utf-8")
            self.assertTrue(raw.endswith("\n"))
            self.assertEqual(json.loads(raw), payload)
            self.assertNotIn("NaN", raw)
            self.assertNotIn("Infinity", raw)

    def test_nonfinite_values_fail_before_file_creation(self):
        for value in (float("nan"), float("inf"), -float("inf")):
            with self.subTest(value=str(value)):
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "new.json"
                    with self.assertRaises(ValueError):
                        module.write_new_result(path, {"nested": [1, {"auc": value}]})
                    self.assertFalse(path.exists())
                    self.assertEqual(list(Path(directory).iterdir()), [])

    def test_unserializable_object_fails_before_file_creation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "new.json"
            with self.assertRaises(TypeError):
                module.write_new_result(path, {"bad": {1, 2}})
            self.assertFalse(path.exists())

    def test_existing_artifact_remains_untouched(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "results.json"
            path.write_bytes(b"frozen historical output\\n")
            with self.assertRaises(FileExistsError):
                module.write_new_result(path, {"valid": True})
            self.assertEqual(path.read_bytes(), b"frozen historical output\\n")

    def test_symlink_target_remains_untouched(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "historical.json"
            target.write_text("historical\n", encoding="utf-8")
            link = Path(directory) / "new.json"
            link.symlink_to(target)
            with self.assertRaises(FileExistsError):
                module.write_new_result(link, {"valid": True})
            self.assertTrue(link.is_symlink())
            self.assertEqual(target.read_text(encoding="utf-8"), "historical\n")


if __name__ == "__main__":
    unittest.main()
