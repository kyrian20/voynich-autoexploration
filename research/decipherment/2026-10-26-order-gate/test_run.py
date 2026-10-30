from collections import Counter
import math,unittest
from run import OrderModel,choose,shuffle,transform
from support import support

class GateTests(unittest.TestCase):
    def test_probability_normalization_seen_unseen(self):
        train=[{'group':'train','tokens':['a','b','a','c']*20}];dev=[{'group':'dev','tokens':['a','b','a','c']}]
        m=OrderModel(train,dev)
        for previous in ('a','missing'):
            self.assertAlmostEqual(sum(m.probabilities(previous,b)[1] for b in m.events),1,places=12)

    def test_no_identity_signal_selects_zero_weight(self):
        train=[{'group':'train','tokens':[a,b]} for a in ('aa','bb') for b in ('aa','bb') for _ in range(20)]
        m=OrderModel(train,[{**r,'group':'dev'} for r in train])
        self.assertEqual(m.weight,0)
        self.assertEqual(m.score(train)['gain'],0)

    def test_ambiguity_abstains(self):
        rows=[{'group':'dev','tokens':['abcdef']*3}];cost={chr(i+97):math.log2(26) for i in range(26)}
        result=choose(rows,{'a':cost,'b':cost})
        self.assertEqual(result['status'],'NO_IDENTIFICABLE')
        self.assertEqual(len(result['candidates']),624)

    def test_shuffle_preserves_inventory_and_groups(self):
        rows=[{'group':'g','tokens':['a','b','c','d']}];new=shuffle(rows,12)
        self.assertEqual(Counter(rows[0]['tokens']),Counter(new[0]['tokens']))
        self.assertEqual(new[0]['group'],'g')
        self.assertEqual(rows[0]['tokens'],['a','b','c','d'])

    def test_no_vocabulary_leakage_and_roundtrip(self):
        train=[{'group':'train','tokens':['a','b']*20}];dev=[{'group':'dev','tokens':['new','words']}]
        m=OrderModel(train,dev);self.assertNotIn('new',m.vocab)
        self.assertEqual(transform(transform(dev,7,11),7,11,True),dev)

    def test_positive_dependency(self):
        train=[{'group':'train','tokens':['aa','bb']*200}]
        dev=[{'group':'dev','tokens':['aa','bb']*30}]
        m=OrderModel(train,dev)
        self.assertGreater(m.score(dev)['gain'],.5)

    def test_exact_position_support(self):
        rows=[{'group':'g','tokens':['word']*12}]
        self.assertTrue(support(rows,12,13)['mapping_identical_on_all_observed_tokens'])
        rows[0]['tokens'].append('word')
        self.assertEqual(support(rows,12,13)['positions0'],[12])
        self.assertTrue(support(rows,13,14)['mapping_identical_on_all_observed_tokens'])

if __name__=='__main__':unittest.main()
