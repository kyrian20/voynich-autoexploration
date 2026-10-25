import unittest
from scripts.prepare_visual_annotation_queue import build, validate_annotation

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

if __name__=='__main__': unittest.main()
