import hashlib
import sys
import tempfile
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.check_corpus_integrity import verify
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
if __name__=='__main__': unittest.main()
