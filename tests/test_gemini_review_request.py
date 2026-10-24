"""Offline tests for the opt-in Gemini review request boundary."""
import sys
import subprocess
from pathlib import Path
import unittest
from unittest.mock import patch

from scripts.request_gemini_review import build_request, extract_text, main


class GeminiReviewRequestTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
