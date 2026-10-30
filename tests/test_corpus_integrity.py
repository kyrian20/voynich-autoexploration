import hashlib
import json
import sys
import tempfile
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.check_corpus_integrity import verify, unique_keys, verify_frozen_manifest, FROZEN_CORPUS
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

    def test_unregistered_dangling_file_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            folder = root / 'data/transcriptions'
            folder.mkdir(parents=True)
            (folder / 'known.txt').write_bytes(b'abc')
            entry = {'path': 'data/transcriptions/known.txt', 'bytes': 3,
                     'sha256': hashlib.sha256(b'abc').hexdigest(),
                     'status': 'FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED'}
            manifest = {'files': [entry]}
            self.assertEqual(verify(root, manifest), [])
            (folder / 'dangling.txt').symlink_to(root / 'missing.txt')
            errors = verify(root, manifest)
            self.assertIn(
                'Unregistered symlink in corpus tree: data/transcriptions/dangling.txt',
                errors,
            )
            self.assertFalse((folder / 'dangling.txt').is_file())

    def test_unregistered_symlink_directory_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            folder = root / 'data/reference_corpora'
            folder.mkdir(parents=True)
            (folder / 'known.txt').write_bytes(b'abc')
            entry = {'path': 'data/reference_corpora/known.txt', 'bytes': 3,
                     'sha256': hashlib.sha256(b'abc').hexdigest(),
                     'status': 'FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED'}
            manifest = {'files': [entry]}
            self.assertEqual(verify(root, manifest), [])
            (folder / 'external').symlink_to(root / 'missing-directory',
                                            target_is_directory=True)
            errors = verify(root, manifest)
            self.assertIn(
                'Unregistered symlink in corpus tree: data/reference_corpora/external',
                errors,
            )

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
    def test_independent_frozen_lock_accepts_original_manifest(self):
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root/'research/CORPUS_INPUT_MANIFEST.json').read_text(encoding='utf-8'), object_pairs_hook=unique_keys)
        self.assertEqual(len(FROZEN_CORPUS), 14)
        self.assertEqual(verify_frozen_manifest(manifest), [])

    def test_coordinated_manifest_and_corpus_digest_change_cannot_pass_lock(self):
        # Even if the edited bytes matched the edited manifest, the independent
        # reviewed digest remains different. No real corpus bytes are modified.
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root/'research/CORPUS_INPUT_MANIFEST.json').read_text(encoding='utf-8'), object_pairs_hook=unique_keys)
        name = 'data/reference_corpora/latin/vulgate.txt'
        row = next(r for r in manifest['files'] if r['path'] == name)
        row['sha256'] = '0'*64
        row['bytes'] += 1
        self.assertIn('Frozen corpus metadata changed without review: '+name, verify_frozen_manifest(manifest))

    def test_frozen_lock_rejects_quarantine_relabel_and_missing_file(self):
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root/'research/CORPUS_INPUT_MANIFEST.json').read_text(encoding='utf-8'), object_pairs_hook=unique_keys)
        name = 'data/reference_corpora/latin/cicero_caesar_latin.txt'
        row = next(r for r in manifest['files'] if r['path'] == name)
        row['status'] = 'FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED'
        self.assertIn('Frozen corpus metadata changed without review: '+name, verify_frozen_manifest(manifest))
        manifest['files'].remove(row)
        self.assertIn('Frozen corpus removed from manifest: '+name, verify_frozen_manifest(manifest))

    def test_frozen_lock_rejects_unreviewed_addition_and_source_change(self):
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root/'research/CORPUS_INPUT_MANIFEST.json').read_text(encoding='utf-8'), object_pairs_hook=unique_keys)
        manifest['source_commit'] = '0'*40
        manifest['files'].append(dict(manifest['files'][0], path='data/reference_corpora/latin/extra.txt'))
        errors = verify_frozen_manifest(manifest)
        self.assertIn('Frozen manifest version/source changed without review', errors)
        self.assertIn('Unreviewed corpus added to frozen manifest: data/reference_corpora/latin/extra.txt', errors)

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(ValueError):
            json.loads('{"files": [], "files": []}',object_pairs_hook=unique_keys)
if __name__=='__main__': unittest.main()
