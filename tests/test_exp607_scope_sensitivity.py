#!/usr/bin/env python3
import collections
import copy
import hashlib
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import audit_exp607_scope_sensitivity as audit


class ScopeControls(unittest.TestCase):
    def test_locus_partition_and_unknown_rejected(self):
        expected = {'P0':'P0','P1':'other_paragraph','Pb':'other_paragraph',
                    'Lz':'labels','Cc':'circular_radial','Ri':'circular_radial'}
        for locus, category in expected.items():
            self.assertEqual(audit.locus_class(locus), category)
        with self.assertRaises(ValueError):
            audit.locus_class('UNKNOWN')

    def test_selection_preserves_physical_order_and_split(self):
        folios = [f'f{i}r' for i in range(1, 30)]
        train = next(f for f in folios if not audit.is_test(f))
        test = next(f for f in folios if audit.is_test(f))
        records = {
            'last': {'source_line': 3,'folio':train,'locus':'P0'},
            'first': {'source_line':1,'folio':train,'locus':'P0'},
            'label': {'source_line':2,'folio':train,'locus':'Lf'},
            'test': {'source_line':4,'folio':test,'locus':'P0'}}
        words = {key:[key,'end'] for key in records}
        groups, meta = audit.select(records,words,sorted(records),'P0',False)
        self.assertEqual(groups, [(train,[['first','end'],['last','end']])])
        self.assertEqual(meta['lines'],2)
        self.assertEqual(meta['locus_counts'],{'P0':2})
        testing,_ = audit.select(records,words,sorted(records),'P0',True)
        self.assertEqual({f for f,_ in groups} & {f for f,_ in testing},set())

    def test_shuffling_preserves_units_and_does_not_mutate(self):
        groups=[('f1r',[['a','b','a','c'],['d','e','f']]),
                ('f2r',[['g','h','i']])]
        original=copy.deepcopy(groups)
        shuffled=audit.shuffle_groups(groups,11)
        self.assertEqual(groups,original)
        self.assertEqual(shuffled,audit.shuffle_groups(groups,11))
        self.assertNotEqual(shuffled,original)
        for (fa,la),(fb,lb) in zip(original,shuffled):
            self.assertEqual(fa,fb)
            for a,b in zip(la,lb):
                self.assertEqual(collections.Counter(a),collections.Counter(b))

    def test_first_seed_matches_native_control_exactly(self):
        train=[('f1r',[['a','b','a','c'],['b','c','d']]),
               ('f2r',[['a','d','b']])]
        test=[('f3r',[['a','b','c'],['d','a','b']])]
        a=audit.native.score(train,test,shuffled=True)
        b=audit.native.score(audit.shuffle_groups(train,6072026),test)
        self.assertEqual(a,b)

    def test_empty_scope_never_reports_zero_as_success(self):
        self.assertFalse(audit.evaluate([], [('f1r',[['a','b']])])['available'])
        self.assertFalse(audit.evaluate([('f1r',[['a','b']])],
                                       [('f2r',[['a']])])['available'])
        with self.assertRaises(ValueError):
            audit.evaluate([('f1r',[['a','b']])],[('f1r',[['b','a']])])

    def test_seeds_and_quantiles_frozen(self):
        self.assertEqual(len(audit.SEEDS),64)
        self.assertEqual(len(set(audit.SEEDS)),64)
        self.assertEqual(audit.SEEDS[1],int(hashlib.sha256(
            b'EXP607-scope-control-v1:0').hexdigest()[:16],16))
        self.assertAlmostEqual(audit.linear_quantile([0,10],.95),9.5)
        self.assertEqual(audit.linear_quantile([3],.95),3)
        with self.assertRaises(ValueError):
            audit.linear_quantile([],.95)


if __name__ == '__main__':
    unittest.main()

