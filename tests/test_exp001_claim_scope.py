"""Pure regression tests for EXP-001 scope auditor (no corpus needed)."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / 'scripts/audit_exp001_claim_scope.py'
spec = importlib.util.spec_from_file_location('audit_exp001_claim_scope', MODULE)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class TestExp001ClaimScope(unittest.TestCase):
    def test_entropy_and_h2(self):
        self.assertEqual(audit.entropy('aabb'), 1.0)
        self.assertEqual(audit.entropy([]), 0.0)
        self.assertEqual(audit.historical_h2(['zz', 'zz']), 0.0)

    def test_synthetic_nonsemantic_control(self):
        x = audit.synthetic_control()
        self.assertEqual(x['h_initial_bits'], 2.0)
        self.assertGreater(x['gap_bits'], 1.0)
        self.assertEqual(x['words'], 512)
        self.assertEqual(x, audit.synthetic_control())

    def test_changed_generator_changes_fingerprint(self):
        self.assertNotEqual(audit.synthetic_control(suffix_length=4)['input_sha256'],
                            audit.synthetic_control(suffix_length=8)['input_sha256'])

    def test_frozen_reader_rejects_missing_corpus(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            p = root / audit.READERS
            p.parent.mkdir(parents=True)
            p.write_text(json.dumps({'source_commit': 'aa9ec5399e7a5cdf8d1b2890fa657f1358825b41',
                                     'cases': [{'experiment_path': audit.SCRIPT,
                                                'corpus': audit.CORPUS, 'selected_units': 991553,
                                                'unit': 'tokens', 'adjudicated_language': 'English',
                                                'status': 'ISOLATED_READER_REPLAY_MATCHED',
                                                'script_sha256': 'dummy', 'corpus_sha256': 'dummy'}]}))
            with self.assertRaises(FileNotFoundError):
                audit.audit(root)

    def test_reader_provenance_gate(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            p = root / audit.READERS
            p.parent.mkdir(parents=True)
            p.write_text(json.dumps({'source_commit': 'unknown', 'cases': []}))
            with self.assertRaisesRegex(ValueError, 'provenance'):
                audit.audit(root)


if __name__ == '__main__':
    unittest.main()
