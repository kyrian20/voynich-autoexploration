import copy
import gzip
import json
import unittest
from pathlib import Path
from scripts.audit_label_partition_coverage import (
    build, partition_map, leaf_id, load_verified_coverage_inputs
)

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

class FrozenLabelCoverageInputTests(unittest.TestCase):
    """Adversarial copies; the archived inventory and manifest stay unchanged."""

    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.inventory_bytes = (cls.root / 'research/decipherment/2026-10-25-label-inventory/inventory.json.gz').read_bytes()
        cls.manifest_bytes = (cls.root / 'research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json').read_bytes()

    @staticmethod
    def encode_inventory(value):
        return gzip.compress(json.dumps(value).encode('utf-8'), mtime=0)

    def test_archived_coverage_unchanged_after_full_input_verification(self):
        inventory, manifest = load_verified_coverage_inputs(
            self.inventory_bytes, self.manifest_bytes, self.root)
        report = build(inventory, manifest)
        expected = json.loads((self.root / 'research/decipherment/2026-10-25-label-coverage/coverage.json').read_text())
        expected.pop('inputs_sha256', None)
        self.assertEqual(report, expected)

    def test_same_size_train_test_swap_is_rejected(self):
        manifest = json.loads(self.manifest_bytes)
        train, test = manifest['partitions']['train'], manifest['partitions']['test']
        train[0], test[0] = test[0], train[0]
        train.sort()
        test.sort()
        self.assertEqual(len(train), manifest['counts']['train'])
        self.assertEqual(len(test), manifest['counts']['test'])
        with self.assertRaisesRegex(ValueError, 'Partition hash assignment mismatch'):
            load_verified_coverage_inputs(self.inventory_bytes, json.dumps(manifest).encode(), self.root)

    def test_duplicate_manifest_keys_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate holdout manifest JSON key'):
            load_verified_coverage_inputs(
                self.inventory_bytes, b'{"salt":"first","salt":"second"}', self.root)

    def test_forged_inventory_source_row_is_rejected(self):
        inventory = json.loads(gzip.decompress(self.inventory_bytes))
        inventory['records'][0]['raw_line'] = 'forged source text'
        with self.assertRaisesRegex(ValueError, 'raw_line differs from original'):
            load_verified_coverage_inputs(
                self.encode_inventory(inventory), self.manifest_bytes, self.root)

    def test_omitted_inventory_row_is_rejected(self):
        inventory = json.loads(gzip.decompress(self.inventory_bytes))
        inventory['records'].pop()
        with self.assertRaisesRegex(ValueError, 'L/R selection mismatch'):
            load_verified_coverage_inputs(
                self.encode_inventory(inventory), self.manifest_bytes, self.root)


if __name__=='__main__':unittest.main()
