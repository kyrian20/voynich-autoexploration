import unittest
import gzip
import json
from pathlib import Path
from scripts.prepare_visual_annotation_queue import build, validate_annotation
from scripts.select_visual_pilot_v2 import build as build_pilot

class VisualQueueTests(unittest.TestCase):
    def record(self, edition):
        return {'id':'f65r.1','folio':'f65r','occurrence_id':edition+':1',
                'edition':edition,'source_line':1,'source_sha256':'f'*64,
                'image_source_archived':None,'raw_body':'SECRET_EVA'}

    def test_pair_editions_without_exposing_text(self):
        queue, mapping = build({'records':[self.record('ZL3b'),self.record('IT2a')]})
        self.assertEqual(len(queue['tasks']), 1)
        self.assertFalse(queue['tasks'][0]['annotation_ready'])
        self.assertEqual(len(mapping['tasks'][0]['source_rows']), 2)
        self.assertNotIn('SECRET_EVA',str(queue))
        self.assertNotIn('f65r',str(queue))
        self.assertEqual(build({'records':[self.record('IT2a'),self.record('ZL3b')]})[0],queue)

    def task_and_annotation(self):
        task={'annotation_ready':True,'status':'READY','masked_image_path':'masked.png',
              'masked_image_sha256':'a'*64,'mask_reviewed_by':'masker'}
        row={'task_id':'x','annotator_id':'reader1','round':'independent_initial',
             'category':'uncertain','confidence':'low','image_sha256':'a'*64,
             'timestamp':'2026-10-25T12:00:00+01:00','saw_eva':False,
             'saw_prior_hypotheses':False,'external_referent':None,
             'external_source':None,'notes':''}
        return {'x':task},row

    def test_block_unprepared_images_and_bad_hashes(self):
        tasks,row=self.task_and_annotation()
        self.assertTrue(validate_annotation(row,tasks))
        tasks['x']['annotation_ready']=False
        with self.assertRaises(ValueError): validate_annotation(row,tasks)
        tasks['x']['annotation_ready']=True
        row['image_sha256']='b'*64
        with self.assertRaises(ValueError): validate_annotation(row,tasks)

    def test_exposure_and_unsourced_names_rejected(self):
        tasks,row=self.task_and_annotation()
        for field in ('saw_eva','saw_prior_hypotheses'):
            row[field]=True
            with self.assertRaises(ValueError): validate_annotation(row,tasks)
            row[field]=False
        row['external_referent']='invented name'
        with self.assertRaises(ValueError): validate_annotation(row,tasks)


class VisualPilotIntegrityTests(unittest.TestCase):
    @staticmethod
    def fixture():
        manifest = {
            'partitions': {'train': [2], 'development': [3], 'test': [70]},
            'counts': {'train': 1, 'development': 1, 'test': 1},
            'eligible_count': 3,
        }
        inventory = {'records': [
            {'folio': 'f2r', 'id': 'f2r.14', 'image_source_archived': None},
            {'folio': 'f70r', 'id': 'f70r.1', 'image_source_archived': None},
        ]}
        return inventory, manifest

    def test_valid_pilot_does_not_include_test_or_approve_annotations(self):
        inventory, manifest = self.fixture()
        report = build_pilot(inventory, manifest)
        self.assertEqual(report['selected_leaves'], [2])
        self.assertEqual(report['leaves'][0]['locators'], ['f2r.14'])
        self.assertFalse(report['leaves'][0]['annotation_ready'])

    def test_reject_development_test_overlap(self):
        inventory, manifest = self.fixture()
        manifest['partitions']['test'] = [3]
        manifest['eligible_count'] = 2
        with self.assertRaisesRegex(ValueError, 'Partition overlap'):
            build_pilot(inventory, manifest)

    def test_reject_duplicate_and_invalid_leaf_identifiers(self):
        inventory, manifest = self.fixture()
        manifest['partitions']['train'] = [2, 2]
        manifest['counts']['train'] = 2
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            build_pilot(inventory, manifest)
        manifest['partitions']['train'] = [2, True]
        with self.assertRaisesRegex(ValueError, 'Invalid physical leaf'):
            build_pilot(inventory, manifest)

    def test_reject_mismatched_train_locator(self):
        inventory, manifest = self.fixture()
        inventory['records'][0]['id'] = 'f70r.14'
        with self.assertRaisesRegex(ValueError, 'locator/folio mismatch'):
            build_pilot(inventory, manifest)

    def test_reject_inconsistent_manifest_counts(self):
        inventory, manifest = self.fixture()
        manifest['counts']['train'] = 2
        with self.assertRaisesRegex(ValueError, 'count mismatch'):
            build_pilot(inventory, manifest)

    def test_archived_pilot_selection_is_unchanged(self):
        root = Path(__file__).resolve().parents[1]
        folder = root / 'research/decipherment/2026-10-25-visual-annotation'
        inventory = json.loads(gzip.decompress(
            (root / 'research/decipherment/2026-10-25-label-inventory/inventory.json.gz').read_bytes()))
        manifest = json.loads((root / 'research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json').read_text())
        archived = json.loads((folder / 'pilot-selection-v2.json').read_text())
        archived.pop('input_sha256')
        self.assertEqual(build_pilot(inventory, manifest), archived)


if __name__=='__main__': unittest.main()
