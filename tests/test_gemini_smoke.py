"""Execute the actual inline workflow script with a mocked, offline transport."""
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
import urllib.request

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/gemini-smoke-test.yml"
SENTINEL = "private-key-and-remote-content"


class GeminiSmokeTests(unittest.TestCase):
    def setUp(self):
        self.workflow = yaml.safe_load(WORKFLOW.read_text())
        self.step = self.workflow["jobs"]["connection"]["steps"][0]
        self.script = self.step["run"].split("python3 - <<'PY'\n", 1)[1].rsplit("\nPY", 1)[0]

    def run_script(self, *, error=None, body=b'{"candidates":[{"content":{"parts":[{"text":"OK"}]}}]}', key=SENTINEL):
        response = unittest.mock.MagicMock()
        response.__enter__.return_value = response
        response.status = 200
        response.read.return_value = body
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as tmp:
            with patch.dict(os.environ, {"GEMINI_API_KEY": key, "RUNNER_TEMP": tmp}, clear=True), \
                 patch.object(urllib.request.OpenerDirector, "open", side_effect=error, return_value=response) as transport, \
                 contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                with self.assertRaises(SystemExit) as exit_result:
                    exec(compile(self.script, str(WORKFLOW), "exec"), {"__name__": "__main__"})
            raw = Path(tmp, "gemini-smoke-status.json").read_text()
        self.assertNotIn(SENTINEL, output.getvalue() + raw)
        return exit_result.exception.code, json.loads(raw), output.getvalue(), transport

    def test_http_errors_have_only_safe_diagnostics_and_one_attempt(self):
        cases = {
            400: "bad_request", 401: "authentication_error", 403: "permission_denied",
            404: "not_found", 408: "request_timeout", 429: "rate_limit_or_quota",
            418: "client_error", 500: "server_error", 502: "server_error",
            503: "server_error", 504: "server_error", 302: "redirect_blocked",
            307: "redirect_blocked", 600: "unexpected_http_status",
        }
        for status, category in cases.items():
            with self.subTest(status=status):
                body = io.BytesIO(SENTINEL.encode())
                error = urllib.error.HTTPError(
                    "https://user:" + SENTINEL + "@example.invalid/?key=" + SENTINEL,
                    status, SENTINEL, {"Authorization": SENTINEL}, body)
                with patch.object(error, "read", side_effect=AssertionError("must not read errors")):
                    code, report, output, transport = self.run_script(error=error)
                self.assertEqual(code, 1)
                self.assertEqual(report, {
                    "status": "http_error", "attempts": 1, "model": "gemini-2.5-flash",
                    "manuscript_data_sent": False, "http_status": status,
                    "error_category": category,
                })
                self.assertEqual(output, f"Gemini connection test status: http_error; http_status={status}; error_category={category}\n")
                transport.assert_called_once()
                self.assertTrue(body.closed)

    def test_success_uses_fixed_synthetic_request(self):
        code, report, output, transport = self.run_script()
        self.assertEqual((code, report["status"], report["attempts"]), (0, "connected", 1))
        request = transport.call_args.args[0]
        self.assertEqual(request.full_url, "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent")
        self.assertEqual(request.method, "POST")
        self.assertEqual(transport.call_args.kwargs, {"timeout": 30})
        self.assertEqual(json.loads(request.data), {
            "contents": [{"role": "user", "parts": [{"text": "Reply with exactly OK."}]}],
            "generationConfig": {"candidateCount": 1, "maxOutputTokens": 32,
                                 "thinkingConfig": {"thinkingBudget": 0}},
        })
        transport.assert_called_once()

    def test_other_failures_do_not_leak_or_retry(self):
        for error, body, status in [
            (TimeoutError(SENTINEL), b"", "request_or_response_error"),
            (urllib.error.URLError(SENTINEL), b"", "request_or_response_error"),
            (None, SENTINEL.encode(), "request_or_response_error"),
            (None, json.dumps({"candidates": [{"content": {"parts": [{"text": SENTINEL}]}}]}).encode(), "unexpected_response"),
        ]:
            with self.subTest(status=status, error=type(error).__name__):
                code, report, output, transport = self.run_script(error=error, body=body)
                self.assertEqual((code, report["status"], report["attempts"]), (1, status, 1))
                transport.assert_called_once()

    def test_missing_secret_sends_nothing(self):
        code, report, output, transport = self.run_script(key="")
        self.assertEqual((code, report["status"], report["attempts"]), (1, "missing_secret", 0))
        transport.assert_not_called()

    def test_manual_only_no_checkout_and_redirects_blocked(self):
        # BaseLoader avoids YAML 1.1 treating "on" as a boolean.
        workflow = yaml.load(WORKFLOW.read_text(), Loader=yaml.BaseLoader)
        self.assertEqual(workflow["on"], {"workflow_dispatch": ""})
        self.assertEqual(workflow["jobs"]["connection"]["if"], "github.event_name == 'workflow_dispatch'")
        self.assertFalse(any("checkout" in step.get("uses", "") for step in workflow["jobs"]["connection"]["steps"]))
        namespace = {}
        exec(compile(self.script.rsplit("sys.exit(main())", 1)[0], str(WORKFLOW), "exec"), namespace)
        self.assertIsNone(namespace["NoRedirect"]().redirect_request(None, None, 302, SENTINEL, {}, "https://example.invalid"))


if __name__ == "__main__":
    unittest.main()
