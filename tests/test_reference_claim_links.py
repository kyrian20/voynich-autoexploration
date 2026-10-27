"""Pure regression controls for reference claim adjudication (stdlib only)."""
import importlib.util
from copy import deepcopy
import json
import tempfile
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

    def test_position_table_rejects_duplicate_even_if_identical(self):
        rows = '\n'.join(f'| {d} | {p} | 12 | 5.2 | 5 |'
                         for d in 'AB' for p in ('LF', 'MID', 'LL'))
        with self.assertRaisesRegex(ValueError, 'exactly one row'):
            audit.parse_position_table(rows + '\n| B | LL | 12 | 5.2 | 5 |')

    def test_position_table_rejects_conflicting_duplicate(self):
        rows = '\n'.join(f'| {d} | {p} | 12 | 5.2 | 5 |'
                         for d in 'AB' for p in ('LF', 'MID', 'LL'))
        with self.assertRaisesRegex(ValueError, 'exactly one row'):
            audit.parse_position_table(rows + '\n| B | LL | 12 | 999.0 | 5 |')



    def test_position_table_rejects_malformed_duplicate_rows(self):
        rows = '\n'.join(f'| {d} | {p} | 12 | 5.2 | 5 |'
                         for d in 'AB' for p in ('LF', 'MID', 'LL'))
        # Previously the numeric-only findall ignored these rows and
        # incorrectly returned a complete six-cell table.
        for bad in ('| B | LL | 12 | n/a | 5 |',
                    '| B | LL | ? | 999.0 | 5 |'):
            with self.subTest(bad=bad), self.assertRaisesRegex(ValueError, 'Malformed EXP-267 position row'):
                audit.parse_position_table(rows + '\n' + bad)

    def test_position_table_rejects_empty_sample(self):
        rows = '\n'.join(f'| {d} | {p} | {0 if (d, p) == ("B", "LL") else 12} | 5.2 | 5 |'
                         for d in 'AB' for p in ('LF', 'MID', 'LL'))
        with self.assertRaisesRegex(ValueError, 'Empty EXP-267 position row'):
            audit.parse_position_table(rows)

    def test_unique_index_accepts_distinct_identifiers(self):
        rows = [{'experiment_path': 'a', 'value': 1}, {'experiment_path': 'b', 'value': 2}]
        self.assertEqual(audit.unique_index(rows, 'experiment_path', 'Reader replay')['b']['value'], 2)

    def test_unique_index_rejects_malformed_or_missing_identifiers(self):
        for rows in (None, {}, [None], [{}], [{'path': ''}], [{'path': 12}]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                audit.unique_index(rows, 'path', 'Corpus identity')

    def run_with_metadata(self, readers, identities):
        # No original corpus or historical script is required: duplicate
        # metadata must be rejected before any corpus/script reads occur.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / 'research/maintenance/2026-10-22-remaining-readers'
            folder.mkdir(parents=True)
            (folder / 'results.json').write_text(json.dumps({
                'source_commit': 'aa9ec5399e7a5cdf8d1b2890fa657f1358825b41',
                'cases': readers,
            }), encoding='utf-8')
            (root / 'research/CORPUS_IDENTITY_REVIEW.json').write_text(json.dumps({
                'excluded_from_new_language_baselines': identities,
            }), encoding='utf-8')
            return audit.audit(root)

    def test_audit_rejects_duplicate_reader_even_when_same(self):
        row = {'experiment_path': 'experiments/exp_267_word_length_position/script.py'}
        with self.assertRaisesRegex(ValueError, 'Reader replay: duplicate experiment_path'):
            self.run_with_metadata([row, dict(row)], [])

    def test_audit_rejects_conflicting_corpus_identity_duplicates(self):
        path = 'data/reference_corpora/latin/cicero_de_officiis_latin.txt'
        with self.assertRaisesRegex(ValueError, 'Corpus identity: duplicate path'):
            self.run_with_metadata([], [{'path': path, 'adjudicated_language': 'Latin'},
                                        {'path': path, 'adjudicated_language': 'English'}])

    def test_audit_rejects_duplicate_reader_json_member(self):
        # The last source_commit is valid, but a conflicting first member
        # must not be silently overwritten by json.loads.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / 'research/maintenance/2026-10-22-remaining-readers'
            folder.mkdir(parents=True)
            (folder / 'results.json').write_text(
                '{"source_commit":"wrong","source_commit":"aa9ec5399e7a5cdf8d1b2890fa657f1358825b41","cases":[]}',
                encoding='utf-8')
            (root / 'research/CORPUS_IDENTITY_REVIEW.json').write_text(
                '{"excluded_from_new_language_baselines":[]}', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Duplicate JSON object key: source_commit'):
                audit.audit(root)

    def test_audit_rejects_duplicate_nested_identity_json_member(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / 'research/maintenance/2026-10-22-remaining-readers'
            folder.mkdir(parents=True)
            (folder / 'results.json').write_text(
                '{"source_commit":"aa9ec5399e7a5cdf8d1b2890fa657f1358825b41","cases":[]}',
                encoding='utf-8')
            (root / 'research/CORPUS_IDENTITY_REVIEW.json').write_text(
                '{"excluded_from_new_language_baselines":[{"path":"wrong","path":"valid"}]}',
                encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Duplicate JSON object key: path'):
                audit.audit(root)

    def test_strict_snapshot_loader_rejects_duplicate_members(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'snapshot.json'
            path.write_text('{"schema_version":0,"schema_version":1}', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Duplicate JSON object key: schema_version'):
                audit.load_json_strict(path)
            path.write_text('{"schema_version":1,"checks":{}}', encoding='utf-8')
            self.assertEqual(audit.load_json_strict(path)['schema_version'], 1)


    def test_claim_provenance_gate_accepts_frozen_corpus_identities(self):
        root = MODULE.parents[1]
        identities = audit.load_json_strict(root / 'research/CORPUS_IDENTITY_REVIEW.json')
        self.assertIsNone(audit.verify_corpus_identity(root, identities))

    def test_claim_provenance_gate_rejects_jointly_forged_work_label(self):
        # Previously a reader snapshot and overlay could agree on a fabricated
        # language/work without checking the separate adjudication.
        root = MODULE.parents[1]
        identities = deepcopy(audit.load_json_strict(root / 'research/CORPUS_IDENTITY_REVIEW.json'))
        target = next(row for row in identities['excluded_from_new_language_baselines']
                      if row['path'] == 'data/reference_corpora/latin/vulgate.txt')
        target['adjudicated_work'] = 'Latin Vulgate (fabricated)'
        with self.assertRaisesRegex(ValueError, 'Historical adjudicated work changed'):
            audit.verify_corpus_identity(root, identities)

    def test_claim_provenance_gate_rejects_frozen_manifest_drift(self):
        root = MODULE.parents[1]
        identities = audit.load_json_strict(root / 'research/CORPUS_IDENTITY_REVIEW.json')
        manifest = deepcopy(audit.load_json_strict(root / 'research/CORPUS_INPUT_MANIFEST.json'))
        target = next(row for row in manifest['files']
                      if row['path'] == 'data/reference_corpora/latin/vulgate.txt')
        target['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Overlay hash/size disagrees with frozen manifest'):
            audit.verify_corpus_identity(root, identities, manifest)

    def test_claim_provenance_gate_rejects_missing_exclusion(self):
        root = MODULE.parents[1]
        identities = deepcopy(audit.load_json_strict(root / 'research/CORPUS_IDENTITY_REVIEW.json'))
        identities['excluded_from_new_language_baselines'] = [
            row for row in identities['excluded_from_new_language_baselines']
            if row['path'] != 'data/reference_corpora/latin/vulgate.txt'
        ]
        with self.assertRaisesRegex(ValueError, 'Historical exclusion silently removed'):
            audit.verify_corpus_identity(root, identities)


if __name__ == '__main__':
    unittest.main()
