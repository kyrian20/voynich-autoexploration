import hashlib
import json
import sys
import tempfile
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.check_corpus_integrity import verify, unique_keys
class CorpusIntegrity(unittest.TestCase):
    def test_mutation_missing_and_unregistered_input_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); folder=root/'data/transcriptions'; folder.mkdir(parents=True)
            p=folder/'test.txt'; p.write_bytes(b'abc')
            manifest={'files':[{'path':'data/transcriptions/test.txt','bytes':3,'sha256':hashlib.sha256(b'abc').hexdigest(),'status':'FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED'}]}
            self.assertEqual(verify(root,manifest),[])
            p.write_bytes(b'abd'); self.assertTrue(verify(root,manifest))
            p.unlink(); self.assertTrue(verify(root,manifest))
            p.write_bytes(b'abc'); (folder/'extra.txt').write_bytes(b'abc')
            self.assertTrue(verify(root,manifest))
    def test_empty_input_needs_explicit_quarantine(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); p=root/'data/transcriptions/x.txt'; p.parent.mkdir(parents=True); p.touch()
            entry={'path':'data/transcriptions/x.txt','bytes':0,'sha256':hashlib.sha256(b'').hexdigest()}
            self.assertTrue(verify(root,{'files':[entry]}))
            entry['status']='BLOCKED_EMPTY_DO_NOT_USE'
            self.assertEqual(verify(root,{'files':[entry]}),[])
    def test_matching_checksum_does_not_authorize_file_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            root = base / 'checkout'
            folder = root / 'data/transcriptions'
            folder.mkdir(parents=True)
            external = base / 'outside.txt'
            external.write_bytes(b'abc')
            (folder / 'x.txt').symlink_to(external)
            entry = {'path': 'data/transcriptions/x.txt', 'bytes': 3,
                     'sha256': hashlib.sha256(b'abc').hexdigest(),
                     'status': 'FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED'}
            errors = verify(root, {'files': [entry]})
            self.assertIn('Symlink corpus path forbidden: data/transcriptions/x.txt', errors)

    def test_matching_checksum_does_not_authorize_parent_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            root = base / 'checkout'
            outside = base / 'outside-folder'
            outside.mkdir()
            (outside / 'x.txt').write_bytes(b'abc')
            (root / 'data').mkdir(parents=True)
            (root / 'data/transcriptions').symlink_to(outside, target_is_directory=True)
            entry = {'path': 'data/transcriptions/x.txt', 'bytes': 3,
                     'sha256': hashlib.sha256(b'abc').hexdigest(),
                     'status': 'FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED'}
            errors = verify(root, {'files': [entry]})
            self.assertIn('Symlink corpus path forbidden: data/transcriptions/x.txt', errors)

    def test_duplicate_manifest_paths_rejected(self):
        entry={'path':'data/transcriptions/x.txt','bytes':0,'sha256':hashlib.sha256(b'').hexdigest(),'status':'BLOCKED_EMPTY_DO_NOT_USE'}
        with tempfile.TemporaryDirectory() as d:
            errors=verify(Path(d),{'files':[entry,dict(entry)]})
            self.assertTrue(any('Duplicate manifest path' in e for e in errors))
    def test_invalid_manifest_fields_rejected(self):
        entry={'path':'data/transcriptions/x.txt','bytes':0,'sha256':hashlib.sha256(b'').hexdigest(),'status':'BLOCKED_EMPTY_DO_NOT_USE'}
        cases=[('bytes',True),('bytes',-1),('sha256','bad'),('status','VALIDATED'),('path','data/transcriptions/../x.txt')]
        with tempfile.TemporaryDirectory() as d:
            for key,value in cases:
                with self.subTest(field=key,value=value):
                    changed=dict(entry);changed[key]=value
                    self.assertTrue(verify(Path(d),{'files':[changed]}))
    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(ValueError):
            json.loads('{"files": [], "files": []}',object_pairs_hook=unique_keys)
if __name__=='__main__': unittest.main()
