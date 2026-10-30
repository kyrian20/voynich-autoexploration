"""Offline tests for the opt-in Gemini review request boundary."""
import sys
import subprocess
from pathlib import Path
import unittest
from unittest.mock import patch

from scripts.request_gemini_review import PROMPT_PATH, build_request, extract_text, main


class GeminiReviewRequestTests(unittest.TestCase):
    def test_v2_prompt_defines_quire_currier_and_fixed_holdout(self):
        prompt = PROMPT_PATH.read_text(encoding="utf-8")
        self.assertIn("$Q=T", prompt)
        self.assertIn("cuaderno", prompt)
        self.assertIn("NO", prompt)
        self.assertIn("$L=A/B", prompt)
        self.assertIn("$I", prompt)
        self.assertIn("train/development/test", prompt)
        self.assertIn("needs_data", prompt)
        # The original prompt is immutable provenance for the earlier Gemini run.
        previous = PROMPT_PATH.with_name("2026-10-24-gemini-ch-sh-review-prompt.md")
        self.assertTrue(previous.is_file())
        self.assertNotEqual(previous.read_bytes(), PROMPT_PATH.read_bytes())

    def test_workflow_checks_out_the_same_versioned_prompt(self):
        root = Path(__file__).resolve().parents[1]
        selected = PROMPT_PATH.relative_to(root).as_posix()
        workflow = (root / ".github/workflows/gemini-methodological-review.yml").read_text(encoding="utf-8")
        self.assertEqual(workflow.count(selected), 2)
        self.assertNotIn("2026-10-24-gemini-ch-sh-review-prompt.md", workflow)

    def test_requires_explicit_execute(self):
        with patch.object(sys, "argv", ["request_gemini_review.py", "--model", "gemini-3.8-flash", "--output-dir", "unused"]):
            self.assertEqual(main(), 0)

    def test_direct_cli_dry_run_without_network_or_secret(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, str(root / "scripts/request_gemini_review.py"),
             "--model", "gemini-3.8-flash", "--output-dir", "unused"],
            cwd=root, capture_output=True, text=True, timeout=10,
            env={"PATH": "/usr/bin:/bin"},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("DRY_RUN_ONLY", result.stdout)

    def test_module_cli_dry_run_without_network_or_secret(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, "-m", "scripts.request_gemini_review",
             "--model", "gemini-3.8-flash", "--output-dir", "unused"],
            cwd=root, capture_output=True, text=True, timeout=10,
            env={"PATH": "/usr/bin:/bin"},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("DRY_RUN_ONLY", result.stdout)

    def test_provenance_serialization_is_parseable_json(self):
        import json
        from tempfile import TemporaryDirectory
        sample = {"candidates": [{"content": {"parts": [{"text": "{}"}]}}]}
        with TemporaryDirectory() as directory:
            output = Path(directory) / "api-response-untrusted.json"
            output.write_text(json.dumps(sample, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), sample)

    def test_failed_api_attempt_preserves_sanitized_receipt(self):
        # A failed manual review must leave verifiable provenance even when
        # there is no valid Gemini response to upload. No network call occurs.
        import hashlib
        import json
        import os
        import urllib.error
        from tempfile import TemporaryDirectory

        for failure in ("offline", "invalid_json"):
            with self.subTest(failure=failure), TemporaryDirectory() as tmp:
                destination = Path(tmp) / "review"
                with patch.dict(os.environ, {"GEMINI_API_KEY": "synthetic-test-key"}):
                    with patch("scripts.request_gemini_review.urllib.request.build_opener") as opener:
                        if failure == "offline":
                            opener.return_value.open.side_effect = urllib.error.URLError(
                                "synthetic network failure"
                            )
                        else:
                            response = opener.return_value.open.return_value.__enter__.return_value
                            response.read.return_value = b"not-json"
                        status = main([
                            "--model", "gemini-3.8-flash",
                            "--output-dir", str(destination), "--execute",
                        ])
                self.assertEqual(status, 1)
                opener.return_value.open.assert_called_once()
                self.assertEqual(sorted(p.name for p in destination.iterdir()), ["receipt.json"])
                raw = (destination / "receipt.json").read_text(encoding="utf-8")
                receipt = json.loads(raw)
                self.assertEqual(receipt["status"], "API_OR_RESPONSE_ERROR")
                self.assertEqual(receipt["scientific_status"], "BLOCKED")
                self.assertEqual(receipt["api_attempts"], 1)
                self.assertEqual(receipt["model"], "gemini-3.8-flash")
                self.assertFalse(receipt["manuscript_corpus_sent"])
                self.assertIsNone(receipt["response_sha256"])
                self.assertIsNone(receipt["api_envelope_sha256"])
                self.assertEqual(
                    receipt["prompt_sha256"],
                    hashlib.sha256(PROMPT_PATH.read_bytes()).hexdigest(),
                )
                self.assertNotIn("synthetic-test-key", raw)
                self.assertNotIn("synthetic network failure", raw)

    def test_rejects_missing_secret(self):
        with self.assertRaises(ValueError):
            build_request("gemini-3.8-flash", "", "public text")

    def test_rejects_path_in_model(self):
        with self.assertRaises(ValueError):
            build_request("../models/private", "placeholder", "public text")

    def test_only_public_prompt_is_transmitted(self):
        req = build_request("gemini-3.8-flash", "placeholder", "public-methodology-only")
        self.assertEqual(req.get_method(), "POST")
        self.assertIn(b"public-methodology-only", req.data)
        self.assertNotIn(b"placeholder", req.data)
        self.assertEqual(req.full_url, "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent")

    def test_extract_ignores_thought_parts(self):
        payload = {"candidates": [{"content": {"parts": [
            {"text": "internal", "thought": True}, {"text": '{"limitations":[]}'}
        ]}}]}
        self.assertEqual(extract_text(payload), '{"limitations":[]}')

    def test_empty_candidates_rejected(self):
        with self.assertRaises(ValueError):
            extract_text({"candidates": []})

    def test_malformed_envelopes_leave_sanitized_receipt_without_retry(self):
        import json
        import os
        from tempfile import TemporaryDirectory
        payloads = [[], {"candidates": [None]}, {"candidates": {}},
                    {"candidates": [{"content": []}]},
                    {"candidates": [{"content": {"parts": [None]}}]},
                    {"candidates": [{"content": {"parts": [{"text": 7}]}}]}]
        for payload in payloads:
            with self.subTest(payload=payload), TemporaryDirectory() as tmp:
                with patch.dict(os.environ, {"GEMINI_API_KEY": "synthetic-secret"}):
                    with patch("scripts.request_gemini_review.urllib.request.build_opener") as opener:
                        response = opener.return_value.open.return_value.__enter__.return_value
                        response.read.return_value = json.dumps(payload).encode()
                        self.assertEqual(main(["--model", "gemini-3.8-flash", "--output-dir", tmp, "--execute"]), 1)
                        opener.return_value.open.assert_called_once()
                receipt = json.loads((Path(tmp)/"receipt.json").read_text())
                self.assertEqual(receipt["api_attempts"], 1)
                self.assertEqual(receipt["scientific_status"], "BLOCKED")
                self.assertNotIn("synthetic-secret", json.dumps(receipt))


if __name__ == "__main__":
    unittest.main()
