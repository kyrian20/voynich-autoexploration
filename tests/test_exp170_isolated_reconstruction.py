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

    def test_preflight_receipt_pins_runtime_and_declared_seed_recipe(self):
        # This describes the prospective runtime; it is not a 400-run receipt.
        def versions(package):
            return {"pandas": "99.1-test", "numpy": "99.2-test"}[package]

        with patch.object(runner.metadata, "version", side_effect=versions):
            receipt = self.invoke()
        runtime = receipt["runtime_provenance"]
        self.assertEqual(runtime["python"]["executable"], sys.executable)
        self.assertEqual(runtime["python"]["version"], sys.version)
        self.assertEqual(runtime["python"]["implementation"], sys.implementation.name)
        self.assertEqual(runtime["dependencies"],
                         {"pandas": "99.1-test", "numpy": "99.2-test"})
        self.assertEqual(runtime["timeout_seconds"], 3600)
        self.assertEqual(runtime["historical_script"],
                         runner.DESTINATIONS["historical_script"].as_posix())
        lineage = runtime["script_lineage"]
        self.assertEqual(lineage["variant_for_optional_execution"],
                         "PATH_PORTED_2026_10_22")
        self.assertEqual(lineage["path"],
                         runner.DESTINATIONS["historical_script"].as_posix())
        self.assertEqual(lineage["portable_script_sha256"],
                         runner.sha256(ROOT / runner.DESTINATIONS["historical_script"]))
        self.assertEqual(lineage["april_original_commit"],
                         "bfa786767d61a2c52bfb7a34a10d8b81ab777230")
        self.assertEqual(lineage["april_original_git_blob_sha1"],
                         "26553a194c67fa82dd02a4d3e39b8f4fb12898ce")
        self.assertEqual(lineage["portability_edit_commit"],
                         "83b0875841b3cbdb83c4ffa661e55abfb5b98fa4")
        self.assertFalse(lineage["april_original_used_for_execution"])
        self.assertIn("external input identity", lineage["observed_diff_scope"])
        seeds = runtime["seed_schedule_declared_by_frozen_script"]
        self.assertEqual(seeds["simulation_indices_inclusive"], [0, 99])
        self.assertEqual(seeds["corpus_offsets"], {"italian": 0, "latin": 500})
        self.assertEqual(seeds["protocol_offsets"], {"A": 0, "B": 250})
        self.assertIn("not a per-simulation", runtime["scope"])
        self.assertFalse(self.out.exists())

    def test_missing_dependency_version_is_recorded_as_unknown(self):
        with patch.object(runner.metadata, "version",
                          side_effect=runner.metadata.PackageNotFoundError):
            receipt = self.invoke()
        self.assertEqual(receipt["runtime_provenance"]["dependencies"],
                         {"pandas": None, "numpy": None})
        self.assertFalse(self.out.exists())

    def test_direct_api_rejects_invalid_timeouts_without_side_effects(self):
        # CLI already rejects nonpositive integers; the callable API must too.
        for invalid in (0, -1, True, 1.5, "2"):
            with self.subTest(timeout=repr(invalid)):
                with patch.object(runner, "preflight",
                                  side_effect=AssertionError("must not preflight")) as pre:
                    with patch.object(runner.subprocess, "run",
                                      side_effect=AssertionError("must not launch")) as proc:
                        with self.assertRaisesRegex(
                                ValueError, "timeout must be a positive integer"):
                            runner.run_reconstruction(
                                ROOT, self.naibbe, self.italian, self.hashes,
                                self.out, execute=True, timeout=invalid)
                        pre.assert_not_called()
                        proc.assert_not_called()
                self.assertFalse(self.out.exists())
        self.assertEqual(
            runner.sha256(ROOT / runner.EXP / "data/simulation_results.json"),
            self.original_sha)

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
        self.assertEqual(receipt["returncode"], 0)
        self.assertEqual(receipt["child_returncode"], 0)
        self.assertEqual(json.loads((self.out / "receipt.json").read_text())["child_returncode"], 0)
        self.assertFalse(receipt["historical_reproduction"])
        self.assertEqual(receipt["runtime_provenance"]["timeout_seconds"], 3600)
        self.assertEqual(
            json.loads((self.out / "receipt.json").read_text())["runtime_provenance"],
            receipt["runtime_provenance"])
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

    def test_failed_run_quarantines_exact_partial_output(self):
        # Synthetic failing child only: preserve negative output, never run Naibbe.
        payload = b'{"partial": true}' + bytes([0xff])
        # The former fixture encoded literal backslash-xff, not byte 0xff.
        with self.assertRaises(UnicodeDecodeError):
            payload.decode("utf-8")

        def synthetic_failure(args, **kwargs):
            generated = Path(kwargs["cwd"]) / runner.EXP / "data/simulation_results.json"
            generated.write_bytes(payload)
            return SimpleNamespace(stdout=b"partial", stderr=b"failure", returncode=3)

        with patch.object(runner.subprocess, "run", side_effect=synthetic_failure):
            with self.assertRaisesRegex(RuntimeError, r"failed"):
                self.invoke(execute=True)
        receipt = json.loads((self.out / "receipt.json").read_text())
        self.assertEqual(receipt["status"], "FAILED")
        self.assertEqual(receipt["returncode"], 3)
        self.assertEqual(receipt["child_returncode"], 3)
        quarantined = self.out / "simulation_results.failed.bin"
        self.assertEqual(quarantined.read_bytes(), payload)
        self.assertEqual(receipt["quarantined_output"]["status"],
                         "UNVALIDATED_FAILED_OUTPUT")
        self.assertEqual(receipt["quarantined_output"]["name"], quarantined.name)
        self.assertEqual(receipt["quarantined_output"]["size_bytes"], len(payload))
        self.assertEqual(receipt["quarantined_output"]["sha256"],
                         hashlib.sha256(payload).hexdigest())
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
        # The simulator exited successfully; the *runner* rejected its data.
        self.assertEqual(receipt["child_returncode"], 0)
        self.assertIn("validation_error", receipt)
        self.assertEqual((self.out / "simulation_results.failed.bin").read_bytes(),
                         b'{"italian_A": []}')
        self.assertEqual(receipt["quarantined_output"]["sha256"],
                         hashlib.sha256(b'{"italian_A": []}').hexdigest())
        self.assertFalse((self.out / "simulation_results.json").exists())


    def test_success_exit_with_null_required_metric_is_quarantined(self):
        # A successful child exit is not sufficient when a required metric
        # is missing. Preserve the synthetic invalid payload, never publish
        # it as a modern reconstruction and never touch the frozen original.
        def invalid_simulator(args, **kwargs):
            path = Path(kwargs["cwd"]) / runner.EXP / "data/simulation_results.json"
            data = json.loads((ROOT / runner.EXP / "data/simulation_results.json").read_text())
            data["italian_A"][0]["edy_rate"] = None
            path.write_text(json.dumps(data), encoding="utf-8")
            return SimpleNamespace(stdout=b"", stderr=b"", returncode=0)

        with patch.object(runner.subprocess, "run", side_effect=invalid_simulator):
            with self.assertRaisesRegex(RuntimeError, r"failed \(65\)"):
                self.invoke(execute=True)
        receipt = json.loads((self.out / "receipt.json").read_text())
        self.assertEqual(receipt["status"], "FAILED")
        self.assertEqual(receipt["returncode"], 65)
        self.assertEqual(receipt["child_returncode"], 0)
        self.assertIn("Unexpected null", receipt["validation_error"])
        self.assertFalse((self.out / "simulation_results.json").exists())
        quarantined = self.out / "simulation_results.failed.bin"
        self.assertEqual(receipt["quarantined_output"]["sha256"],
                         hashlib.sha256(quarantined.read_bytes()).hexdigest())
        self.assertEqual(runner.sha256(ROOT / runner.EXP / "data/simulation_results.json"),
                         self.original_sha)

    def test_subprocess_launch_error_keeps_receipt_and_logs(self):
        with patch.object(runner.subprocess, "run",
                          side_effect=OSError("synthetic interpreter launch failure")):
            with self.assertRaisesRegex(RuntimeError, r"failed \(126\)"):
                self.invoke(execute=True)
        receipt = json.loads((self.out / "receipt.json").read_text())
        self.assertEqual(receipt["returncode"], 126)
        self.assertIsNone(receipt["child_returncode"])
        self.assertEqual(receipt["status"], "FAILED")
        self.assertIn("OSError: synthetic interpreter launch failure",
                      (self.out / "stderr.log").read_text())
        self.assertFalse((self.out / "simulation_results.json").exists())
        self.assertEqual(runner.sha256(ROOT / runner.EXP / "data/simulation_results.json"),
                         self.original_sha)

    def test_non_utf8_subprocess_output_preserves_failure_receipt(self):
        # Run a tiny synthetic child, never the historical 400-run simulator.
        real_run = runner.subprocess.run

        def synthetic_bytes_process(args, **kwargs):
            self.assertTrue(str(args[1]).endswith("script.py"))
            code = ("import sys\n"
                    "sys.stdout.buffer.write(b'partial\\xff')\n"
                    "sys.stderr.buffer.write(b'problem\\xfe')\n"
                    "raise SystemExit(3)\n")
            return real_run([sys.executable, "-c", code], **kwargs)

        with patch.object(runner.subprocess, "run", side_effect=synthetic_bytes_process):
            with self.assertRaisesRegex(RuntimeError, r"failed \(3\)"):
                self.invoke(execute=True)
        receipt = json.loads((self.out / "receipt.json").read_text())
        self.assertEqual(receipt["returncode"], 3)
        self.assertEqual(receipt["status"], "FAILED")
        self.assertIn(r"\xff", (self.out / "stdout.log").read_text())
        self.assertIn(r"\xfe", (self.out / "stderr.log").read_text())
        self.assertFalse((self.out / "simulation_results.json").exists())
        self.assertEqual(runner.sha256(ROOT / runner.EXP / "data/simulation_results.json"),
                         self.original_sha)

    def test_raw_binary_logs_distinguish_literal_escape_from_invalid_byte(self):
        # Synthetic child only. Escaped text is ambiguous; binary logs are not.
        real_run = runner.subprocess.run
        expected_stdout = bytes([92, 120, 102, 102, 124, 255])
        expected_stderr = bytes([92, 120, 102, 101, 124, 254])

        def synthetic_process(args, **kwargs):
            self.assertNotIn("text", kwargs)
            self.assertNotIn("encoding", kwargs)
            code = (
                "import sys; "
                "sys.stdout.buffer.write(bytes([92,120,102,102,124,255])); "
                "sys.stderr.buffer.write(bytes([92,120,102,101,124,254])); "
                "sys.exit(3)"
            )
            return real_run([sys.executable, "-c", code], **kwargs)

        with patch.object(runner.subprocess, "run", side_effect=synthetic_process):
            with self.assertRaisesRegex(RuntimeError, r"failed \(3\)"):
                self.invoke(execute=True)
        receipt = json.loads((self.out / "receipt.json").read_text())
        self.assertEqual(receipt["status"], "FAILED")
        self.assertEqual((self.out / "stdout.bin").read_bytes(), expected_stdout)
        self.assertEqual((self.out / "stderr.bin").read_bytes(), expected_stderr)
        for name, expected in (("stdout", expected_stdout), ("stderr", expected_stderr)):
            self.assertEqual(receipt["raw_logs"][name]["size_bytes"], len(expected))
            self.assertEqual(receipt["raw_logs"][name]["sha256"],
                             hashlib.sha256(expected).hexdigest())
        self.assertEqual((self.out / "stdout.log").read_text(),
                         expected_stdout.decode("utf-8", errors="backslashreplace"))
        self.assertEqual((self.out / "stderr.log").read_text(),
                         expected_stderr.decode("utf-8", errors="backslashreplace"))
        self.assertFalse((self.out / "simulation_results.json").exists())
        self.assertEqual(runner.sha256(ROOT / runner.EXP / "data/simulation_results.json"),
                         self.original_sha)

    def test_child_exit_124_is_not_a_timeout(self):
        # Exit status 124 is not proof that subprocess.run timed out.
        with patch.object(runner.subprocess, "run", return_value=SimpleNamespace(
                stdout=b"ordinary exit", stderr=b"child exit", returncode=124)):
            with self.assertRaisesRegex(RuntimeError, r"failed \(124\)"):
                self.invoke(execute=True)
        receipt = json.loads((self.out / "receipt.json").read_text())
        self.assertEqual(receipt["returncode"], 124)
        self.assertEqual(receipt["child_returncode"], 124)
        self.assertFalse(receipt["timed_out"])
        self.assertEqual(receipt["status"], "FAILED")
        self.assertEqual((self.out / "stderr.log").read_text(), "child exit")
        self.assertNotIn("TIMEOUT", (self.out / "stderr.log").read_text())
        self.assertEqual((self.out / "stderr.bin").read_bytes(), b"child exit")
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
        self.assertIsNone(receipt["child_returncode"])
        self.assertTrue(receipt["timed_out"])
        self.assertEqual(receipt["status"], "FAILED")
        stdout_log = (self.out / "stdout.log").read_text(encoding="utf-8")
        stderr_log = (self.out / "stderr.log").read_text(encoding="utf-8")
        # TimeoutExpired carries bytes even when subprocess.run(text=True).
        # Replacement characters would destroy the identity of invalid bytes.
        self.assertIn(r"\xff", stdout_log)
        self.assertIn(r"\xfe", stderr_log)
        self.assertNotIn("\ufffd", stdout_log + stderr_log)
        self.assertIn("TIMEOUT", stderr_log)
        self.assertEqual((self.out / "stdout.bin").read_bytes(), b"partial\xff")
        self.assertEqual((self.out / "stderr.bin").read_bytes(), b"problem\xfe")
        self.assertEqual(receipt["raw_logs"]["stdout"]["sha256"],
                         hashlib.sha256(b"partial\xff").hexdigest())
        self.assertEqual(receipt["raw_logs"]["stderr"]["sha256"],
                         hashlib.sha256(b"problem\xfe").hexdigest())
        self.assertFalse((self.out / "simulation_results.json").exists())
        self.assertEqual(runner.sha256(ROOT / runner.EXP / "data/simulation_results.json"),
                         self.original_sha)


    def test_preapril_external_candidate_temporal_identity_is_not_historical_replay(self):
        # This is an offline regression for independently inspected GitHub
        # commit/tree metadata. It does not authenticate the April run inputs.
        from datetime import datetime

        registry = json.loads((ROOT / "research/external/2026-10-22-professional-sources/registry.json")
                              .read_text(encoding="utf-8"))
        entry = next(x for x in registry["external_repositories"]
                     if x["repository"] == "greshko/naibbe-cipher")
        evidence = entry["pre_experiment_candidate"]
        self.assertEqual(evidence["status"], "TEMPORALLY_AVAILABLE_NOT_PROVEN_HISTORICAL")
        self.assertIs(evidence["historical_identity_proven"], False)
        self.assertIs(evidence["execution_performed"], False)
        self.assertIs(evidence["tree_listing_complete_both"], True)
        self.assertEqual(evidence["experiment_commit"], runner.ORIGINAL_EXP170_COMMIT)
        self.assertEqual(evidence["source_commit"], "d9cab18fafaca29610515753193806652cb019f2")
        self.assertEqual(evidence["source_tree_sha1"], "263896a7b28ce5b7cf501d389cc3ec5908d9e099")
        self.assertEqual(evidence["later_commit"], entry["commit"])
        self.assertEqual(evidence["later_tree_sha1"], "be16bb4cdd327769c3c19addee401195cff7a8f2")
        before = datetime.fromisoformat(evidence["source_commit_utc"].replace("Z", "+00:00"))
        experiment = datetime.fromisoformat(evidence["experiment_commit_utc"].replace("Z", "+00:00"))
        later = datetime.fromisoformat(evidence["later_commit_utc"].replace("Z", "+00:00"))
        self.assertLess(before, experiment)
        self.assertLess(experiment, later)
        expected = {
            "naibbe_v2.py": ("b566ad82e4b6ff0782ecdddebf77718dac44f292", 11626),
            "references/naibbe_tables.csv": ("5cd34fb81d80faf3b4d57dbf1719c05ffde25302", 8913),
            "input/examples/divina_commedia.txt": ("2f57181cca66ab61d8719e35778d6b06688ee8be", 1112569),
        }
        observed = {x["path"]: (x["git_blob_sha1"], x["bytes"])
                    for x in evidence["matching_blob_paths"]}
        self.assertEqual(observed, expected)
        latest = {x["path"]: (x["git_blob_sha1"], x["bytes"])
                  for x in entry["files"] if x["path"] in expected}
        self.assertEqual(latest, expected)
        self.assertIn("no evidence", evidence["verification_scope"])


if __name__ == "__main__":
    unittest.main()
