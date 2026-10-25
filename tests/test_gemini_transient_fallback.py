import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import MagicMock, patch
import urllib.error

from scripts.request_gemini_review import main, FALLBACK_MODEL
from scripts.validate_gemini_review import DESIGN_FIELDS, PREREG_FIELDS


def response(value):
    manager = MagicMock()
    manager.__enter__.return_value.read.return_value = json.dumps(value).encode()
    return manager


def good_review():
    return {'limitations': ['limit']*5,
            'competing_hypotheses': [{'name':'n','prediction':'p','falsifier':'f'}]*3,
            'proposed_design': dict.fromkeys(DESIGN_FIELDS, 'needs_data'),
            'pre_registration': dict.fromkeys(PREREG_FIELDS, 'needs_data'),
            'required_inputs':['hashes'], 'unresolved_questions':['question']}


class TransientFallback(unittest.TestCase):
    def run_case(self, sequence):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        with patch.dict(os.environ, {'GEMINI_API_KEY':'synthetic-secret'}):
            with patch('scripts.request_gemini_review.urllib.request.build_opener') as factory:
                factory.return_value.open.side_effect = sequence
                code = main(['--model','gemini-3.8-flash','--output-dir',tmp.name,'--execute'])
                calls = factory.return_value.open.call_args_list
        receipt = json.loads((Path(tmp.name)/'receipt.json').read_text())
        self.assertNotIn('synthetic-secret', json.dumps(receipt))
        return code, receipt, calls

    def test_transient_fallback_verifies_model_then_preserves_real_model_and_history(self):
        metadata = {'name':'models/'+FALLBACK_MODEL,
                    'supportedGenerationMethods':['generateContent'], 'outputTokenLimit':8192}
        envelope = {'candidates':[{'content':{'parts':[{'text':json.dumps(good_review())}]}}]}
        for error in [TimeoutError(), urllib.error.HTTPError('https://invalid',503,'',{},None)]:
            with self.subTest(error=type(error).__name__):
                code, r, calls = self.run_case([error, response(metadata), response(envelope)])
                self.assertEqual(code,0)
                self.assertEqual(r['model'],FALLBACK_MODEL)
                self.assertEqual(r['requested_model'],'gemini-3.8-flash')
                self.assertEqual(r['api_attempts'],2)
                self.assertEqual(r['fallback_discovery'],'VERIFIED')
                self.assertEqual(r['status'],'SCHEMA_VALID_ONLY')
                self.assertEqual([c.args[0].get_method() for c in calls],['POST','GET','POST'])
                self.assertEqual([c.kwargs['timeout'] for c in calls],[180,15,90])
                self.assertIn(FALLBACK_MODEL,calls[-1].args[0].full_url)

    def test_permission_failure_is_not_retried(self):
        code,r,calls=self.run_case([urllib.error.HTTPError('https://invalid',403,'',{},None)])
        self.assertEqual(code,1)
        self.assertEqual(len(calls),1)
        self.assertEqual(r['api_attempts'],1)

    def test_incompatible_metadata_blocks_fallback_generation(self):
        code,r,calls=self.run_case([TimeoutError(),response({'name':'models/wrong'})])
        self.assertEqual(code,1)
        self.assertEqual(len(calls),2)
        self.assertEqual(r['api_attempts'],1)
        self.assertEqual(r['fallback_discovery'],'INCOMPATIBLE_METADATA')

    def test_second_failure_stops_after_two_generations(self):
        metadata={'name':'models/'+FALLBACK_MODEL,'supportedGenerationMethods':['generateContent'],'outputTokenLimit':8192}
        code,r,calls=self.run_case([TimeoutError(),response(metadata),TimeoutError()])
        self.assertEqual(code,1)
        self.assertEqual(len(calls),3)
        self.assertEqual(r['api_attempts'],2)
        self.assertEqual(r['model'],FALLBACK_MODEL)


if __name__=='__main__':
    unittest.main()
