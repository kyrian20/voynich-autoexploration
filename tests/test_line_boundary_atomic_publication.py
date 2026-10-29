"""Atomic, exclusive publication of line-boundary JSON (synthetic I/O faults).

No model fitting, holdout access, corpus mutation or historical-result rewrite.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

SCRIPT = (Path(__file__).resolve().parents[1] / "research" / "analysis" /
          "2026-10-28-line-boundary-reproduction" / "line_boundary_replication.py")
spec = importlib.util.spec_from_file_location("line_boundary_atomic", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class AtomicPublicationContract(unittest.TestCase):
    def test_staged_bytes_are_complete_before_destination_appears(self):
        payload = {"metric": 0.25, "observations": [1, 2, 3]}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / "result.json"
            real_link = module.os.link
            observed = []

            def inspect_then_link(source, target):
                self.assertEqual(Path(target), destination)
                self.assertFalse(destination.exists())
                self.assertEqual(json.loads(Path(source).read_text(encoding="utf-8")),
                                 payload)
                observed.append(True)
                return real_link(source, target)

            with mock.patch.object(module.os, "link", side_effect=inspect_then_link):
                module.write_new_result(destination, payload)
            self.assertEqual(observed, [True])
            self.assertEqual(json.loads(destination.read_text(encoding="utf-8")),
                             payload)
            self.assertEqual(list(root.iterdir()), [destination])

    def test_failed_publication_does_not_leave_partial_final_or_temp(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / "result.json"
            with mock.patch.object(module.os, "link",
                                   side_effect=OSError("simulated link failure")):
                with self.assertRaisesRegex(OSError, "simulated link failure"):
                    module.write_new_result(destination, {"ok": True})
            self.assertEqual(list(root.iterdir()), [])

    def test_failed_staging_flush_does_not_publish_or_leave_temp(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / "result.json"
            with mock.patch.object(module.os, "fsync",
                                   side_effect=OSError("simulated disk failure")):
                with self.assertRaisesRegex(OSError, "simulated disk failure"):
                    module.write_new_result(destination, {"ok": True})
            self.assertEqual(list(root.iterdir()), [])

    def test_concurrent_winner_is_never_replaced(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / "result.json"

            def competitor_wins(source, target):
                Path(target).write_text('{"winner": true}\\n', encoding="utf-8")
                raise FileExistsError("concurrent writer already published")

            with mock.patch.object(module.os, "link", side_effect=competitor_wins):
                with self.assertRaises(FileExistsError):
                    module.write_new_result(destination, {"winner": False})
            self.assertEqual(json.loads(destination.read_text(encoding="utf-8")),
                             {"winner": True})
            self.assertEqual(list(root.iterdir()), [destination])

    def test_existing_symlink_is_not_followed_or_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            frozen = root / "frozen.json"
            frozen.write_text("frozen", encoding="utf-8")
            destination = root / "result.json"
            destination.symlink_to(frozen)
            with self.assertRaises(FileExistsError):
                module.write_new_result(destination, {"overwrite": True})
            self.assertEqual(frozen.read_text(encoding="utf-8"), "frozen")
            self.assertEqual(sorted(p.name for p in root.iterdir()),
                             ["frozen.json", "result.json"])

    def test_invalid_json_fails_before_any_file_is_created(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                module.write_new_result(root / "result.json",
                                        {"auc": float("nan")})
            self.assertEqual(list(root.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
