"""Adversarial full-line exclusion: preserve authentic repeats, lengths and order."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.audit_duplicate_leakage import exclude_shared, grouped
class DuplicateControl(unittest.TestCase):
    def test_full_sequence_only_and_repeated_test_rows(self):
        train=[('a','f1r',('ab','c'))]
        test=[('b','f2r',('ab','c')),('c','f2r',('a','bc')),
              ('d','f2r',('c','ab')),('e','f2r',('x','y')),('f','f2r',('x','y'))]
        kept,removed=exclude_shared(train,test)
        self.assertEqual([r[0] for r in removed],['b'])
        self.assertEqual([r[0] for r in kept],['c','d','e','f'])
        self.assertEqual(grouped(kept)[0][1][-2:],[['x','y'],['x','y']])
        self.assertEqual(len(train),1)
    def test_no_test_remains(self):
        row=('a','f1r',('x','y'))
        self.assertEqual(exclude_shared([row],[('b','f2r',row[2])])[0],[])
if __name__=='__main__': unittest.main()
