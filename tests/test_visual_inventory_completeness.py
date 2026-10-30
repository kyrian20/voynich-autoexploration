"""Regression tests: archived inventory must include exactly every explicit L/R row."""
import tempfile
import unittest
from pathlib import Path

from scripts.audit_visual_inventory_completeness import audit, census, digest
from scripts.audit_visual_inventory_source_rows import audit as audit_binding


class CompletenessTests(unittest.TestCase):
    def fixture(self, root):
        path = 'data/transcriptions/eva_zl3b.txt'
        raw = (b'<f2r> <! $L=A>\n'
               b'<f2r.14,@Lp> daiin\n'
               b'<f2r.15,+P0> excluded\n'
               b'<f2r.16,/R0> otol\n')
        file = root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_bytes(raw)
        source_hash = digest(raw)
        lines = raw.decode().splitlines()

        def row(number, locus_id, code, body):
            line = lines[number - 1]
            return {'edition': 'ZL3b', 'source_sha256': source_hash,
                    'source_line': number, 'occurrence_id': f'ZL3b:{number}',
                    'raw_line': line, 'raw_line_sha256': digest(line.encode()),
                    'folio': 'f2r', 'locus_id': locus_id, 'id': f'f2r.{locus_id}',
                    'raw_body': body, 'locus': code[1:]}

        inventory = {'sources': [{'edition': 'ZL3b', 'path': path,
                                  'sha256': source_hash, 'selected_rows': 2}],
                     'records': [row(2, '14', '@Lp', 'daiin'),
                                 row(4, '16', '/R0', 'otol')]}
        manifest = {'corpora': {file.name: {'path': path, 'sha256': source_hash}}}
        return inventory, manifest, row

    def test_complete_selection_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inventory, manifest, _ = self.fixture(root)
            result = audit(inventory, manifest, root)
            self.assertEqual(result['selected_total'], 2)
            self.assertEqual(result['selected_by_edition'], {'ZL3b': 2})

    def test_missing_row_is_detected_even_if_prior_binding_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inventory, manifest, _ = self.fixture(root)
            inventory['records'].pop()
            self.assertEqual(audit_binding(inventory, manifest, root)['record_count'], 1)
            with self.assertRaisesRegex(ValueError, r'missing=\[4\]'):
                audit(inventory, manifest, root)

    def test_extra_non_lr_row_is_detected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inventory, manifest, row = self.fixture(root)
            inventory['records'].append(row(3, '15', '+P0', 'excluded'))
            with self.assertRaisesRegex(ValueError, r'extra=\[3\]'):
                audit(inventory, manifest, root)

    def test_tampered_selected_rows_count_is_detected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inventory, manifest, _ = self.fixture(root)
            inventory['sources'][0]['selected_rows'] = 1
            with self.assertRaisesRegex(ValueError, 'selected_rows disagrees'):
                audit(inventory, manifest, root)

    def test_undecidable_physical_line_blocks(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inventory, manifest, _ = self.fixture(root)
            path = root / inventory['sources'][0]['path']
            raw = path.read_bytes() + b'<f2r.17,@L0 no-terminator\n'
            path.write_bytes(raw)
            h = digest(raw)
            inventory['sources'][0]['sha256'] = h
            manifest['corpora'][path.name]['sha256'] = h
            for record in inventory['records']:
                record['source_sha256'] = h
            with self.assertRaisesRegex(ValueError, 'Undecidable physical lines'):
                audit(inventory, manifest, root)

    def test_census_handles_comments_headers_and_nonnumeric_loci(self):
        raw = b'# comment\n<fRos> <! $L=A>\n<fRos.0a,/L0> x\n<fRos.0b,+P0> y\n'
        self.assertEqual(census(raw), ({3}, []))


if __name__ == '__main__':
    unittest.main()
