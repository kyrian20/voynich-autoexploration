import hashlib
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_holdout_page_crosswalk import crosswalk
from audit_holdout_locus_coverage import SOURCE_NAMES


def fixture(text):
    sources = {name: text.encode() for name in SOURCE_NAMES}
    manifest = {'schema_version': 2,
                'corpora': {name: {'path': f'data/transcriptions/{name}',
                                  'sha256': hashlib.sha256(raw).hexdigest(), 'leaf_count': 1}
                            for name, raw in sources.items()},
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


if __name__ == '__main__':
    unittest.main()
