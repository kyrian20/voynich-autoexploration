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

    def run_script(self, *, error=None, body=b'{"candidates":[{"content":{"parts":[{"text":"OK"}]}}]}', key=SENTINEL, catalog=None, metadata=None, discovery_error=None, pages=None):
        response = unittest.mock.MagicMock()
        response.__enter__.return_value = response
        response.status = 200
        response.read.return_value = body
        model = {"name": "models/gemini-3.8-flash", "supportedGenerationMethods": ["generateContent"],
                 "inputTokenLimit": 10000, "outputTokenLimit": 8192}
        def reply(value):
            result = unittest.mock.MagicMock()
            result.__enter__.return_value = result
            result.status = 200
            result.read.return_value = json.dumps(value).encode()
            return result
        replies = [reply(catalog if catalog is not None else {"models": [model]}),
                   reply(metadata if metadata is not None else model), error or response]
        if pages is not None:
            replies = [reply(page) for page in pages] + replies[1:]
        if discovery_error:
            replies = [discovery_error]
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as tmp:
            with patch.dict(os.environ, {"GEMINI_API_KEY": key, "RUNNER_TEMP": tmp}, clear=True), \
                 patch.object(urllib.request.OpenerDirector, "open", side_effect=replies) as transport, \
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
                self.assertEqual(report["status"], "http_error")
                self.assertEqual(report["attempts"], 1)
                self.assertEqual(report["http_status"], status)
                self.assertEqual(report["error_category"], category)
                self.assertEqual(report["stage"], "generate_content")
                self.assertEqual(output, f"Gemini connection test status: http_error; http_status={status}; error_category={category}\n")
                self.assertEqual(transport.call_count, 3)
                self.assertTrue(body.closed)

    def test_success_uses_fixed_synthetic_request(self):
        code, report, output, transport = self.run_script()
        self.assertEqual((code, report["status"], report["attempts"]), (0, "connected", 1))
        request = transport.call_args.args[0]
        self.assertEqual(request.full_url, "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent")
        self.assertEqual(request.method, "POST")
        self.assertEqual(transport.call_args.kwargs, {"timeout": 30})
        self.assertEqual(json.loads(request.data), {
            "contents": [{"role": "user", "parts": [{"text": "Reply with exactly OK."}]}],
            "generationConfig": {"maxOutputTokens": 1024},
        })
        self.assertEqual(transport.call_count, 3)

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
                self.assertEqual(transport.call_count, 3)

    def test_discovery_errors_never_generate_or_leak(self):
        for status in (400, 401, 403, 404, 429, 503, 302):
            error = urllib.error.HTTPError("https://example.invalid/" + SENTINEL,
                                           status, SENTINEL, {}, io.BytesIO(SENTINEL.encode()))
            code, report, output, transport = self.run_script(discovery_error=error)
            self.assertEqual((code, report["attempts"], report["stage"]), (1, 0, "models_list"))
            transport.assert_called_once()

    def test_no_compatible_model_does_not_generate(self):
        for models in ([], [{"name": "models/gemini-3.8-flash", "supportedGenerationMethods": ["embedContent"]}],
                       [{"name": SENTINEL, "supportedGenerationMethods": ["generateContent"]}]):
            code, report, output, transport = self.run_script(catalog={"models": models})
            self.assertEqual((code, report["status"], report["attempts"]), (1, "no_compatible_model", 0))
            transport.assert_called_once()

    def test_invalid_metadata_stops_before_post(self):
        for metadata in ({}, {"name": SENTINEL},
                         {"name": "models/gemini-3.8-flash", "supportedGenerationMethods": ["generateContent"],
                          "inputTokenLimit": 10000, "outputTokenLimit": 32}):
            code, report, output, transport = self.run_script(metadata=metadata)
            self.assertEqual((code, report["status"], report["attempts"]), (1, "incompatible_parameters", 0))
            self.assertEqual(transport.call_count, 2)
            self.assertTrue(all(c.args[0].method == "GET" for c in transport.call_args_list))

    def test_catalog_pagination_and_preference(self):
        model = {"name": "models/gemini-3.8-flash", "supportedGenerationMethods": ["generateContent"]}
        code, report, output, transport = self.run_script(pages=[
            {"models": [], "nextPageToken": "page + /?"}, {"models": [model]}])
        self.assertEqual((code, report["status"], report["discovery_requests"]), (0, "connected", 3))
        self.assertIn("pageToken=page+%2B+%2F%3F", transport.call_args_list[1].args[0].full_url)
        self.assertEqual([c.args[0].method for c in transport.call_args_list], ["GET", "GET", "GET", "POST"])

    def test_repeated_page_token_stops_before_generation(self):
        code, report, output, transport = self.run_script(pages=[
            {"models": [], "nextPageToken": "repeat"}, {"models": [], "nextPageToken": "repeat"}])
        self.assertEqual((code, report["status"], report["attempts"]), (1, "incomplete_catalog", 0))
        self.assertEqual(transport.call_count, 2)

    def test_selects_available_older_text_model_before_any_post(self):
        model = {"name": "models/gemini-2.5-flash", "supportedGenerationMethods": ["generateContent"],
                 "inputTokenLimit": 10000, "outputTokenLimit": 8192}
        code, report, output, transport = self.run_script(catalog={"models": [model]}, metadata=model)
        self.assertEqual((code, report["model"]), (0, "gemini-2.5-flash"))
        self.assertTrue(transport.call_args.args[0].full_url.endswith("gemini-2.5-flash:generateContent"))

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
