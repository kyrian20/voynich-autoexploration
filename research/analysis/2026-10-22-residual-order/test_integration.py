import copy
import hashlib
from pathlib import Path
import tempfile
import unittest
from run_integrated import scientific_compare,validate_source_reuse
class IntegrationContracts(unittest.TestCase):
    def test_only_interpreter_metadata_may_differ(self):
        a={'python':'3.11','results':[{'gain':.01}],'sha256':{'input':'abc'}}
        b=copy.deepcopy(a);b['python']='3.12';scientific_compare(a,b)
        b['results'][0]['gain']=.02
        with self.assertRaises(ValueError):scientific_compare(a,b)
        b=copy.deepcopy(a);b['sha256']['input']='changed'
        with self.assertRaises(ValueError):scientific_compare(a,b)
    def test_quarantined_baseline_rejected_even_if_hash_matches(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/'data/bad.txt';p.parent.mkdir();p.write_bytes(b'unchanged')
            inputs={'raw_sources':[{'path':'data/bad.txt','sha256':hashlib.sha256(p.read_bytes()).hexdigest()}]}
            review={'excluded_from_new_language_baselines':[{'path':'data/bad.txt'}]}
            with self.assertRaises(ValueError):validate_source_reuse(root,inputs,review)
    def test_source_drift_rejected_and_original_not_changed(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/'data/good.txt';p.parent.mkdir();p.write_bytes(b'good')
            inputs={'raw_sources':[{'path':'data/good.txt','sha256':hashlib.sha256(b'good').hexdigest()}]}
            review={'excluded_from_new_language_baselines':[]}
            validate_source_reuse(root,inputs,review);p.write_bytes(b'drift')
            with self.assertRaises(ValueError):validate_source_reuse(root,inputs,review)
            self.assertEqual(p.read_bytes(),b'drift')
    def test_duplicate_review_path_rejected(self):
        with self.assertRaises(ValueError):
            validate_source_reuse(Path('/tmp'),{'raw_sources':[]},
                                 {'excluded_from_new_language_baselines':[{'path':'data/x'},{'path':'data/x'}]})
if __name__=='__main__':unittest.main()
