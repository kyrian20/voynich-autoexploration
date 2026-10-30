import unittest
from count_loci import scan

class CountsTests(unittest.TestCase):
    def test_records_are_not_tokens(self):
        x=scan('<f68r1.1,@Ls> two.words\n<f68r1.2,@La> three.other.words\n<f68r1.3,@Ri> text\n')['pages'][0]
        self.assertEqual(x['label_records'],2)
        self.assertEqual(x['locus_counts'],{'La':1,'Ls':1,'Ri':1})

    def test_twelve_is_only_count_condition(self):
        rows='\n'.join(f'<f68r1.{i},@Ls> arbitrary' for i in range(1,13))
        x=scan(rows)['pages'][0]
        self.assertTrue(x['Z12_literal_complete_bijection_count_condition'])
        self.assertFalse(x['C28_literal_complete_bijection_count_condition'])
        self.assertNotIn('meaning',x)

    def test_duplicate_refused(self):
        with self.assertRaises(ValueError):scan('<f68r1.1,@Ls> a\n<f68r1.1,@La> b')

    def test_non_numeric_exclusion_visible(self):
        x=scan('<f68r1.X,@Ls> a')
        self.assertEqual(len(x['unparsed_target_records']),1)

if __name__=='__main__':unittest.main()
