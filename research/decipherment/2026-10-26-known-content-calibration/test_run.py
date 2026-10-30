import unittest
from run import rotate,transform,recover,unigram,plain_loss

class RecoveryTests(unittest.TestCase):
    def test_alphabet_roundtrip(self):
        s='abcdefghijklmnopqrstuvwxyz àéö?'
        for shift in range(26):self.assertEqual(rotate(rotate(s,shift),-shift),s)

    def test_period_and_line_reset(self):
        rows=[{'group':'g','tokens':['abc']*9},{'group':'h','tokens':['abc']*2}]
        encoded=transform(rows,7,11)
        self.assertEqual(encoded[0]['tokens'][0],encoded[0]['tokens'][7])
        self.assertEqual(encoded[0]['tokens'][0],encoded[1]['tokens'][0])
        self.assertEqual(transform(encoded,7,11,True),rows)

    def test_selector_without_ground_truth(self):
        train=[{'group':'train','tokens':['aaaaa','aaba','aaac']*20}]
        dev=[{'group':'dev','tokens':['aaaaa']*30}]
        selected=recover(transform(dev,7,11),unigram(train))['selected']
        self.assertEqual((selected['period'],selected['offset']),(7,11))

    def test_unigram_cannot_certify_word_order(self):
        rows=[{'group':'g','tokens':['alpha','beta','gamma']}]
        reversed_rows=[{'group':'g','tokens':list(reversed(rows[0]['tokens']))}]
        cost=unigram(rows)
        self.assertEqual(plain_loss(rows,cost),plain_loss(reversed_rows,cost))

    def test_reject_outside_family(self):
        with self.assertRaises(ValueError):transform([],13,0)

if __name__=='__main__':unittest.main()
