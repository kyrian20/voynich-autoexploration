import hashlib
import copy
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_holdout_page_crosswalk import crosswalk
from audit_holdout_locus_coverage import SOURCE_NAMES, FROZEN_CONTRACT
import audit_holdout_locus_coverage as coverage_module
import audit_holdout_page_crosswalk as crosswalk_module


def fixture(text):
    sources = {name: text.encode() for name in SOURCE_NAMES}
    manifest = {**copy.deepcopy(FROZEN_CONTRACT), 'schema_version': 2,
                'corpora': {name: {'path': f'data/transcriptions/{name}',
                                  'sha256': hashlib.sha256(raw).hexdigest(), 'leaf_count': 1}
                            for name, raw in sources.items()},
                'salt': 'VOYNICH-FUTURE-RULES-2026-10-23-v1',
                'partitions': {'train': [67], 'development': [], 'test': []},
                'counts': {'train': 1, 'development': 0, 'test': 0},
                'eligible_count': 1, 'source_only_leaves': {name: [] for name in SOURCE_NAMES}}
    return sources, manifest


class PageCrosswalkTests(unittest.TestCase):
    def test_panels_and_named_page(self):
        result = crosswalk(*fixture('<f67r1>\n<f67r1.1,@P0> a\n<f67v2>\n<f67v2.1,@P0> b\n<fRos>\n<fRos.1,@P0> c\n'))
        pages = result['editions'][SOURCE_NAMES[0]]['pages']
        self.assertEqual(pages['f67r1'], pages['f67v2'])
        self.assertEqual(pages['f67r1']['partition'], 'train')
        self.assertEqual(pages['fRos'], {'physical_leaf': None, 'partition': 'excluded_unassigned'})

    def test_wrong_active_page_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Orphan or mismatched locus'):
            crosswalk(*fixture('<f67r1>\n<f67v2.1,@P0> a\n'))

    def test_broad_numeric_panel_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Unparsed numeric folio header'):
            crosswalk(*fixture('<f67r12>\n<f67r12.1,@P0> a\n'))

    def test_substituted_source_is_rejected(self):
        sources, manifest = fixture('<f67r1>\n<f67r1.1,@P0> a\n')
        sources[SOURCE_NAMES[0]] += b'# replaced\n'
        with self.assertRaisesRegex(ValueError, 'provenance'):
            crosswalk(sources, manifest)


    def test_same_leaf_but_wrong_panel_id_is_rejected(self):
        # Fault injection: a strict reader returning a different panel ID
        # would have passed the old leaf-only equality gate.
        sources, manifest = fixture(
            '<f67r1>\n<f67r1.1,@P0> a\n'
            '<f67v2>\n<f67v2.1,@P0> b\n'
        )
        real_audit = crosswalk_module.audit_text

        def corrupted_audit(text, **kwargs):
            report = real_audit(text, **kwargs)
            report['page_names'] = ['f67r1', 'f67v1']
            return report

        with patch.object(crosswalk_module, 'audit_text', side_effect=corrupted_audit):
            with self.assertRaisesRegex(ValueError, 'page identifiers disagree'):
                crosswalk(sources, manifest)

    def test_same_leaf_but_missing_locus_count_is_rejected(self):
        # Fault injection: page/leaf sets remain identical but the strict
        # reader silently undercounts a record.
        sources, manifest = fixture(
            '<f67r1>\n<f67r1.1,@P0> a\n<f67r1.2,@P0> b\n'
        )
        real_audit = crosswalk_module.audit_text

        def corrupted_audit(text, **kwargs):
            report = real_audit(text, **kwargs)
            report['record_count'] -= 1
            return report

        with patch.object(crosswalk_module, 'audit_text', side_effect=corrupted_audit):
            with self.assertRaisesRegex(ValueError, 'physical row counts disagree'):
                crosswalk(sources, manifest)


    def test_same_page_and_count_but_different_locus_id_is_rejected(self):
        # Fault injection: the strict reader silently substitutes a locus tag.
        # Page names, leaf assignment, header count and record count agree.
        sources, manifest = fixture(
            '<f67r1>\n<f67r1.1,@P0> a\n<f67r1.2,@P0> b\n'
        )
        real_audit = crosswalk_module.audit_text

        def corrupted_audit(text, **kwargs):
            report = real_audit(text, **kwargs)
            report['locus_ids'] = [
                tag.replace('f67r1.2,@P0', 'f67r1.3,@P0')
                for tag in report['locus_ids']
            ]
            return report

        with patch.object(crosswalk_module, 'audit_text', side_effect=corrupted_audit):
            with self.assertRaisesRegex(ValueError, 'locus identifiers disagree'):
                crosswalk(sources, manifest)

    def test_optional_locus_inventory_does_not_change_default_reports(self):
        raw = '<f67r1>\n<f67r1.1,@P0> a\n'.encode()
        strict = crosswalk_module.audit_text(raw.decode())
        extended = crosswalk_module.audit_text(raw.decode(), include_locus_ids=True)
        self.assertEqual(strict, {k: v for k, v in extended.items() if k != 'locus_ids'})
        independent = coverage_module.inspect_source(raw)
        expanded = coverage_module.inspect_source(raw, include_locus_ids=True)
        self.assertEqual(independent, {k: v for k, v in expanded.items() if k != 'locus_ids'})
        self.assertEqual(extended['locus_ids'], expanded['locus_ids'])

    def test_both_audit_clis_refuse_existing_outputs_and_symlinks(self):
        # Exercise the real CLI main() paths with tiny, hash-matched synthetic
        # transcriptions. No frozen source, manifest or archived result is touched.
        for module in (coverage_module, crosswalk_module):
            with self.subTest(module=module.__name__):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    inputs = root / 'data' / 'transcriptions'
                    inputs.mkdir(parents=True)
                    sources, manifest = fixture(
                        '<f67r> metadata\n<f67r.1,@P0> a\n'
                    )
                    for name, raw in sources.items():
                        (inputs / name).write_bytes(raw)
                    output = root / 'audit.json'
                    with patch.object(module, 'ROOT', root), \
                            patch.object(module, 'load_manifest', return_value=manifest):
                        with patch.object(sys, 'argv', ['audit', '--out', str(output)]):
                            with redirect_stdout(io.StringIO()):
                                module.main()
                            original = output.read_bytes()
                            self.assertTrue(original.endswith(b'\n'))
                            self.assertIn(b'"status"', original)
                            with self.assertRaises(FileExistsError):
                                module.main()
                            self.assertEqual(output.read_bytes(), original)

                        frozen = root / 'frozen.json'
                        frozen.write_bytes(b'FROZEN_EVIDENCE')
                        link = root / 'linked.json'
                        link.symlink_to(frozen)
                        with patch.object(sys, 'argv', ['audit', '--out', str(link)]):
                            with self.assertRaises(FileExistsError):
                                module.main()
                        self.assertEqual(frozen.read_bytes(), b'FROZEN_EVIDENCE')
                        self.assertTrue(link.is_symlink())


if __name__ == '__main__':
    unittest.main()
