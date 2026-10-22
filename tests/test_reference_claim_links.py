"""Pure regression controls for reference claim adjudication (stdlib only)."""
import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / 'scripts/audit_reference_claim_links.py'
spec = importlib.util.spec_from_file_location('audit_reference_claim_links', MODULE)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class TestReferenceClaimLinks(unittest.TestCase):
    def test_git_blob_sha(self):
        self.assertEqual(audit.git_blob_sha(b'test\n'), '9daeafb9864cf43055ae93beb0afd6c7d144bfa4')

    def test_entropy_counterexample(self):
        self.assertEqual(audit.entropy(['x', 'x', 'y', 'y']), 1.0)
        self.assertEqual(audit.entropy(['x', 'x']), 0.0)
        self.assertEqual(audit.entropy(['y', 'y']), 0.0)

    def test_position_table(self):
        example = '\n'.join(f'| {d} | {p} | 12 | {v} | 5 |' for d, p, v in [
            ('A', 'LF', 5.5), ('A', 'MID', 5.2), ('A', 'LL', 5.7),
            ('B', 'LF', 5.8), ('B', 'MID', 5.456), ('B', 'LL', 5.275)])
        table = audit.parse_position_table(example)
        self.assertGreater(table['B', 'MID'], table['B', 'LL'])

    def test_position_table_rejects_incomplete(self):
        with self.assertRaises(ValueError):
            audit.parse_position_table('| A | LF | 10 | 5.2 | 5 |')


if __name__ == '__main__':
    unittest.main()
