import io
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import urllib.error

from scripts.request_gemini_review import main, REQUEST_TIMEOUT


class FailureDiagnostics(unittest.TestCase):
    def test_distinguishes_errors_without_leaking_details_or_retrying(self):
        secret = 'synthetic-secret-never-persist'
        cases = [
            (TimeoutError(secret), 'TIMEOUT', None),
            (urllib.error.URLError(TimeoutError(secret)), 'TIMEOUT', None),
            (urllib.error.URLError(secret), 'TRANSPORT_ERROR', None),
            (urllib.error.HTTPError('https://example.invalid/'+secret, 429, secret, {}, io.BytesIO(secret.encode())), 'HTTP_ERROR', 429),
            (json.JSONDecodeError(secret, secret, 0), 'INVALID_JSON', None),
        ]
        for error, category, status in cases:
            with self.subTest(category=category), TemporaryDirectory() as tmp:
                with patch.dict(os.environ, {'GEMINI_API_KEY': secret}):
                    with patch('scripts.request_gemini_review.urllib.request.build_opener') as opener:
                        opener.return_value.open.side_effect = error
                        self.assertEqual(main(['--model', 'gemini-3.8-flash', '--output-dir', tmp, '--execute', '--no-fallback']), 1)
                        opener.return_value.open.assert_called_once()
                        self.assertEqual(opener.return_value.open.call_args.kwargs['timeout'], REQUEST_TIMEOUT)
                raw = (Path(tmp)/'receipt.json').read_text()
                result = json.loads(raw)
                self.assertEqual(result['error_category'], category)
                self.assertEqual(result['http_status'], status)
                self.assertEqual(result['api_attempts'], 1)
                self.assertEqual(result['timeout_seconds'], 180)
                self.assertNotIn(secret, raw)
                self.assertNotIn('example.invalid', raw)
                self.assertEqual([p.name for p in Path(tmp).iterdir()], ['receipt.json'])


if __name__ == '__main__':
    unittest.main()
