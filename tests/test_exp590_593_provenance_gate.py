"""Synthetic regression tests; never substitute these for historical reproduction."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from research.maintenance.check_exp590_593_reproduction import FILES, inspect

class ProvenanceGateTests(unittest.TestCase):
    def test_missing_attestations_and_mutated_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.txt"
            source.write_bytes(b"original")
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            for name in FILES:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps({"source": "source.txt", "source_sha256": digest}), encoding="utf-8")
            issues = inspect(root)
            self.assertEqual(len(issues), 12)
            self.assertEqual(sum("no attested" in issue for issue in issues), 12)
            source.write_bytes(b"altered")
            issues = inspect(root)
            self.assertEqual(sum("source SHA-256 mismatch" in issue for issue in issues), 2)

    def test_malformed_record_and_digest_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.txt"
            source.write_bytes(b"original")
            for name, payload in zip(FILES, ([], {"source": "source.txt", "source_sha256": []})):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(payload), encoding="utf-8")
            issues = inspect(root)
            self.assertTrue(any("must be an object" in issue for issue in issues))
            self.assertTrue(any("source path or SHA-256 absent" in issue for issue in issues))

    def test_two_unhashable_digests_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.txt").write_bytes(b"original")
            for name in FILES:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps({"source": "source.txt", "source_sha256": []}), encoding="utf-8")
            issues = inspect(root)
            self.assertEqual(sum("source path or SHA-256 absent" in issue for issue in issues), 2)

    def test_forged_attestation_paths_and_generator_digest_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.txt"
            source.write_bytes(b"original")
            generator = root / "generator.py"
            generator.write_bytes(b"print('old')")
            record = {
                "source": "source.txt",
                "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "generator_path": "generator.py",
                "generator_sha256": hashlib.sha256(b"print('different')").hexdigest(),
                "reproduction_command": "python generator.py",
                "reproduction_log_path": "missing.log",
                "reproduced_output_sha256": "a" * 64,
                "reproduction_status": "REPRODUCED",
            }
            for name in FILES:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(record), encoding="utf-8")
            issues = inspect(root)
            self.assertEqual(sum("generator SHA-256 mismatch" in x for x in issues), 2)
            self.assertEqual(sum("reproduction_log_path file unavailable" in x for x in issues), 2)
            record["generator_path"] = "../outside.py"
            record["reproduction_log_path"] = "../outside.log"
            for name in FILES:
                (root / name).write_text(json.dumps(record), encoding="utf-8")
            issues = inspect(root)
            self.assertEqual(sum("file unavailable or outside root" in x for x in issues), 4)

    def test_reproduced_output_requires_archived_matching_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.txt").write_bytes(b"source")
            (root / "generator.py").write_bytes(b"generator")
            (root / "run.log").write_bytes(b"log")
            (root / "output.json").write_bytes(b"output")
            record = {
                "source": "source.txt",
                "source_sha256": hashlib.sha256(b"source").hexdigest(),
                "generator_path": "generator.py",
                "generator_sha256": hashlib.sha256(b"generator").hexdigest(),
                "reproduction_command": "python generator.py",
                "reproduction_log_path": "run.log",
                "reproduction_log_sha256": hashlib.sha256(b"log").hexdigest(),
                "reproduced_output_sha256": hashlib.sha256(b"output").hexdigest(),
                "reproduction_status": "REPRODUCED",
            }
            for name in FILES:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(record), encoding="utf-8")
            self.assertEqual(sum("no attested reproduced_output_path" in x for x in inspect(root)), 2)
            record["reproduced_output_path"] = "output.json"
            for name in FILES:
                (root / name).write_text(json.dumps(record), encoding="utf-8")
            self.assertEqual(sum("reused reproduced output path" in x for x in inspect(root)), 1)
            (root / "run.log").write_bytes(b"altered log")
            self.assertEqual(sum("reproduction log SHA-256 mismatch" in x for x in inspect(root)), 2)
            (root / "run.log").write_bytes(b"log")
            record["reproduction_log_sha256"] = "not-a-digest"
            for name in FILES:
                (root / name).write_text(json.dumps(record), encoding="utf-8")
            self.assertEqual(sum("invalid or missing reproduction log SHA-256" in x for x in inspect(root)), 2)
            record["reproduction_log_sha256"] = hashlib.sha256(b"log").hexdigest()
            for name in FILES:
                (root / name).write_text(json.dumps(record), encoding="utf-8")
            self.assertEqual(sum("reused reproduced output path" in x for x in inspect(root)), 1)
            (root / "output.json").write_bytes(b"tampered")
            self.assertEqual(sum("reproduced output SHA-256 mismatch" in x for x in inspect(root)), 2)
            record["reproduced_output_path"] = "../outside.json"
            for name in FILES:
                (root / name).write_text(json.dumps(record), encoding="utf-8")
            self.assertEqual(sum("reproduced output unavailable or outside root" in x for x in inspect(root)), 2)

    def test_distinct_outputs_are_required_for_distinct_results(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, data in (("source.txt", b"source"), ("generator.py", b"generator"),
                               ("run.log", b"log"), ("output1.json", b"one"),
                               ("output2.json", b"two")):
                (root / name).write_bytes(data)
            base = {
                "source": "source.txt", "source_sha256": hashlib.sha256(b"source").hexdigest(),
                "generator_path": "generator.py", "generator_sha256": hashlib.sha256(b"generator").hexdigest(),
                "reproduction_command": "python generator.py", "reproduction_log_path": "run.log",
                "reproduction_log_sha256": hashlib.sha256(b"log").hexdigest(),
                "reproduction_status": "REPRODUCED",
            }
            for name in FILES:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps({**base, "reproduced_output_path": "output1.json",
                    "reproduced_output_sha256": hashlib.sha256(b"one").hexdigest()}), encoding="utf-8")
            self.assertTrue(any("reused reproduced output path" in x for x in inspect(root)))
            second = root / FILES[1]
            second.write_text(json.dumps({**base, "reproduced_output_path": "output2.json",
                "reproduced_output_sha256": hashlib.sha256(b"two").hexdigest()}), encoding="utf-8")
            self.assertEqual(inspect(root), [])

    def test_output_alias_paths_cannot_attest_two_results(self):
        # Different strings can point to the same file; compare canonical paths.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, data in (("source.txt", b"source"), ("generator.py", b"generator"),
                               ("run.log", b"log"), ("output.json", b"result")):
                (root / name).write_bytes(data)
            base = {
                "source": "source.txt", "source_sha256": hashlib.sha256(b"source").hexdigest(),
                "generator_path": "generator.py",
                "generator_sha256": hashlib.sha256(b"generator").hexdigest(),
                "reproduction_command": "python generator.py",
                "reproduction_log_path": "run.log",
                "reproduction_log_sha256": hashlib.sha256(b"log").hexdigest(),
                "reproduced_output_sha256": hashlib.sha256(b"result").hexdigest(),
                "reproduction_status": "REPRODUCED",
            }
            for name, output in zip(FILES, ("output.json", "./output.json")):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps({**base, "reproduced_output_path": output}),
                                encoding="utf-8")
            self.assertEqual(sum("reused reproduced output path" in x for x in inspect(root)), 1)

    def test_missing_json_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(len(inspect(Path(directory))), 2)

if __name__ == "__main__":
    unittest.main()
