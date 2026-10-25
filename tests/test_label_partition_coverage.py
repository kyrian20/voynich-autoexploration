import copy
import unittest
from scripts.audit_label_partition_coverage import build, partition_map, leaf_id

class LabelCoverageTests(unittest.TestCase):
    def fixture(self):
        manifest={'partitions':{'train':[1],'development':[2],'test':[3]},
                  'corpora':{'a.txt':{'sha256':'a'},'b.txt':{'sha256':'b'}}}
        inv={'sources':[{'edition':'A','path':'a.txt','sha256':'a','excluded_rows':[]},
                        {'edition':'B','path':'b.txt','sha256':'b','excluded_rows':[]}],
             'records':[]}
        for e,folio,key in [('A','f1r','f1r.1'),('A','f1v2','f1v2.1'),('B','f1r','f1r.1')]:
            inv['records'].append({'edition':e,'folio':folio,'id':key,'locus':'Lp',
                'source_sha256':e.lower(),'occurrence_id':e+key})
        return inv,manifest

    def test_panels_and_recto_verso_share_leaf(self):
        inv,m=self.fixture();r=build(inv,m)
        cell=next(c for c in r['strata'] if c['edition']=='A' and c['partition']=='train')
        self.assertEqual(cell['source_rows'],2);self.assertEqual(cell['numeric_leaves'],1)
        test=next(c for c in r['strata'] if c['edition']=='A' and c['partition']=='test')
        self.assertEqual(test['source_rows'],0)
        self.assertEqual(r['common_locus_ids'],1)

    def test_overlap_missing_leaf_and_identity_fail_closed(self):
        inv,m=self.fixture();m['partitions']['test']=[1]
        with self.assertRaises(ValueError):build(inv,m)
        inv,m=self.fixture();inv['records'][0]['folio']='f99r'
        with self.assertRaises(ValueError):build(inv,m)
        inv,m=self.fixture();inv['sources'][0]['sha256']='changed'
        with self.assertRaises(ValueError):build(inv,m)

    def test_duplicate_record_rejected_and_ros_unassigned(self):
        inv,m=self.fixture();inv['records'].append(copy.deepcopy(inv['records'][0]))
        with self.assertRaises(ValueError):build(inv,m)
        inv,m=self.fixture();inv['records'][0]['folio']='fRos'
        r=build(inv,m);self.assertEqual(r['per_source']['A']['unassigned_rows'],1)
        self.assertIsNone(leaf_id('fRos'))
        with self.assertRaises(ValueError):leaf_id('f1v99')

    def test_outside_selection_distinguished_from_absent(self):
        inv,m=self.fixture()
        inv['sources'][1]['excluded_rows']=[{'id':'f1v2.1','locus':'P0'}]
        r=build(inv,m)
        self.assertEqual(r['unmatched'][0]['counterpart_status'],'PRESENT_OUTSIDE_SELECTION')
        self.assertEqual(r['unmatched'][0]['counterpart_excluded_rows'][0]['locus'],'P0')

    def test_type_disagreement_retained(self):
        inv,m=self.fixture();inv['records'][-1]['locus']='L0'
        self.assertEqual(len(build(inv,m)['type_mismatches']),1)

if __name__=='__main__':unittest.main()
