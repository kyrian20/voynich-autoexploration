"""Safety-contract tests; never execute the historical 400-run simulator."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import run_exp170_isolated_reconstruction as runner


class Exp170ReconstructionRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.naibbe = self.base / "naibbe"
        (self.naibbe / "references").mkdir(parents=True)
        (self.naibbe / "naibbe_v2.py").write_text("print('fixture only')\n")
        (self.naibbe / "references/naibbe_tables.csv").write_text("code,glyphs\na,b\n")
        self.italian = self.base / "italian.txt"
        self.italian.write_text("testo sintetico\n")
        self.hashes = {
            "naibbe_code": runner.sha256(self.naibbe / "naibbe_v2.py"),
            "naibbe_tables": runner.sha256(self.naibbe / "references/naibbe_tables.csv"),
            "italian": runner.sha256(self.italian),
        }
        self.out = self.base / "output"
        self.original_sha = runner.sha256(
            ROOT / runner.EXP / "data/simulation_results.json")

    def invoke(self, execute=False):
        return runner.run_reconstruction(
            ROOT, self.naibbe, self.italian, self.hashes, self.out, execute)

    def test_preflight_does_not_run_or_write(self):
        with patch.object(runner.subprocess, "run",
                          side_effect=AssertionError("simulator must not run")):
            receipt = self.invoke()
        self.assertEqual(receipt["status"], "PREFLIGHT_ONLY")
        self.assertFalse(receipt["historical_reproduction"])
        self.assertFalse(self.out.exists())

    def test_rejects_existing_output_before_execution(self):
        self.out.mkdir()
        with self.assertRaises(FileExistsError):
            self.invoke(execute=True)
        self.assertEqual(list(self.out.iterdir()), [])

    def test_rejects_hash_mismatch_and_symlink(self):
        self.hashes["italian"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            self.invoke()
        self.hashes["italian"] = runner.sha256(self.italian)
        link = self.naibbe / "references/naibbe_tables.csv"
        link.unlink()
        try:
            link.symlink_to(self.italian)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")
        self.hashes["naibbe_tables"] = runner.sha256(self.italian)
        with self.assertRaisesRegex(ValueError, "symlinked"):
            self.invoke()

    def test_rejects_output_inside_checkout(self):
        inside = ROOT / "research" / "never-create-exp170-output"
        with self.assertRaisesRegex(ValueError, "outside"):
            runner.preflight(ROOT, self.naibbe, self.italian, self.hashes, inside)
        self.assertFalse(inside.exists())

    def test_output_reserved_before_simulation_rejects_second_caller(self):
        def synthetic_failure(args, **kwargs):
            self.assertTrue(self.out.is_dir())
            self.assertEqual(list(self.out.iterdir()), [])
            with self.assertRaises(FileExistsError):
                self.invoke(execute=True)
            return SimpleNamespace(stdout="single caller", stderr="", returncode=3)

        with patch.object(runner.subprocess, "run", side_effect=synthetic_failure) as mock:
            with self.assertRaisesRegex(RuntimeError, r"failed \(3\)"):
                self.invoke(execute=True)
        self.assertEqual(mock.call_count, 1)
        self.assertEqual((self.out / "stdout.log").read_text(), "single caller")
        self.assertEqual(json.loads((self.out / "receipt.json").read_text())["status"],
                         "FAILED")
        self.assertEqual(runner.sha256(ROOT / runner.EXP / "data/simulation_results.json"),
                         self.original_sha)

    def test_destination_created_by_concurrent_caller_prevents_subprocess(self):
        real_stage = runner.stage_inputs

        def concurrent_reservation(stage, root, naibbe_dir, italian, hashes):
            staged = real_stage(stage, root, naibbe_dir, italian, hashes)
            self.out.mkdir()
            (self.out / "other-run.marker").write_text("concurrent")
            return staged

        with patch.object(runner, "stage_inputs", side_effect=concurrent_reservation):
            with patch.object(runner.subprocess, "run",
                              side_effect=AssertionError("must not run")) as mock:
                with self.assertRaises(FileExistsError):
                    self.invoke(execute=True)
                mock.assert_not_called()
        self.assertEqual((self.out / "other-run.marker").read_text(), "concurrent")
        self.assertEqual(runner.sha256(ROOT / runner.EXP / "data/simulation_results.json"),
                         self.original_sha)

    def test_staged_input_drift_is_rejected_against_locked_hash(self):
        stage = self.base / "staging"
        stage.mkdir()
        real_copy = shutil.copyfile

        def copy_then_mutate(source, target):
            real_copy(source, target)
            if Path(target) == stage / runner.DESTINATIONS["italian"]:
                Path(target).write_text("modified after preflight")

        with patch.object(runner.shutil, "copyfile", side_effect=copy_then_mutate):
            with self.assertRaisesRegex(ValueError, "Staged input SHA-256 mismatch: italian"):
                runner.stage_inputs(stage, ROOT, self.naibbe, self.italian, self.hashes)
        self.assertEqual(self.italian.read_text(), "testo sintetico\n")

    def test_staged_success_uses_disposable_paths_and_new_output(self):
        def synthetic_simulator(args, **kwargs):
            stage = Path(kwargs["cwd"])
            self.assertNotEqual(stage, ROOT)
            self.assertTrue((stage / runner.EXP / "script.py").exists())
            self.assertFalse((stage / runner.EXP / "data/simulation_results.json").exists())
            self.assertTrue((stage / "data/derived/naibbe-cipher/naibbe_v2.py").exists())
            destination = stage / runner.EXP / "data/simulation_results.json"
            shutil.copyfile(ROOT / runner.EXP / "data/simulation_results.json", destination)
            return SimpleNamespace(stdout="synthetic test\n", stderr="", returncode=0)

        with patch.object(runner.subprocess, "run", side_effect=synthetic_simulator) as mock:
            receipt = self.invoke(execute=True)
        self.assertEqual(mock.call_count, 1)
        self.assertEqual(receipt["status"], "MODERN_RECONSTRUCTION_UNVALIDATED")
        self.assertFalse(receipt["historical_reproduction"])
        self.assertEqual((self.out / "stdout.log").read_text(), "synthetic test\n")
        self.assertEqual(runner.sha256(self.out / "simulation_results.json"), self.original_sha)
        self.assertEqual(runner.sha256(ROOT / runner.EXP / "data/simulation_results.json"),
                         self.original_sha)
        self.assertEqual(json.loads((self.out / "receipt.json").read_text())["status"],
                         "MODERN_RECONSTRUCTION_UNVALIDATED")

    def test_failed_simulation_keeps_logs_but_not_output(self):
        with patch.object(runner.subprocess, "run", return_value=SimpleNamespace(
                stdout="partial", stderr="synthetic error", returncode=3)):
            with self.assertRaisesRegex(RuntimeError, "failed"):
                self.invoke(execute=True)
        self.assertEqual((self.out / "stderr.log").read_text(), "synthetic error")
        self.assertEqual(json.loads((self.out / "receipt.json").read_text())["status"], "FAILED")
        self.assertFalse((self.out / "simulation_results.json").exists())
        self.assertEqual(runner.sha256(ROOT / runner.EXP / "data/simulation_results.json"),
                         self.original_sha)

    def test_invalid_generated_json_keeps_validation_receipt(self):
        def invalid_simulator(args, **kwargs):
            path = Path(kwargs["cwd"]) / runner.EXP / "data/simulation_results.json"
            path.write_text('{"italian_A": []}')
            return SimpleNamespace(stdout="", stderr="", returncode=0)

        with patch.object(runner.subprocess, "run", side_effect=invalid_simulator):
            with self.assertRaisesRegex(RuntimeError, "failed"):
                self.invoke(execute=True)
        receipt = json.loads((self.out / "receipt.json").read_text())
        self.assertEqual(receipt["returncode"], 65)
        self.assertIn("validation_error", receipt)
        self.assertFalse((self.out / "simulation_results.json").exists())


    def test_subprocess_launch_error_keeps_receipt_and_logs(self):
        with patch.object(runner.subprocess, "run",
                          side_effect=OSError("synthetic interpreter launch failure")):
            with self.assertRaisesRegex(RuntimeError, r"failed \(126\)"):
                self.invoke(execute=True)
        receipt = json.loads((self.out / "receipt.json").read_text())
        self.assertEqual(receipt["returncode"], 126)
        self.assertEqual(receipt["status"], "FAILED")
        self.assertIn("OSError: synthetic interpreter launch failure",
                      (self.out / "stderr.log").read_text())
        self.assertFalse((self.out / "simulation_results.json").exists())
        self.assertEqual(runner.sha256(ROOT / runner.EXP / "data/simulation_results.json"),
                         self.original_sha)

    def test_timeout_with_bytes_keeps_decoded_logs(self):
        error = runner.subprocess.TimeoutExpired(
            cmd=["synthetic"], timeout=1, output=b"partial\xff", stderr=b"problem\xfe")
        with patch.object(runner.subprocess, "run", side_effect=error):
            with self.assertRaisesRegex(RuntimeError, r"failed \(124\)"):
                self.invoke(execute=True)
        receipt = json.loads((self.out / "receipt.json").read_text())
        self.assertEqual(receipt["returncode"], 124)
        self.assertEqual(receipt["status"], "FAILED")
        self.assertIn("partial", (self.out / "stdout.log").read_text())
        self.assertIn("problem", (self.out / "stderr.log").read_text())
        self.assertIn("TIMEOUT", (self.out / "stderr.log").read_text())
        self.assertFalse((self.out / "simulation_results.json").exists())


if __name__ == "__main__":
    unittest.main()
