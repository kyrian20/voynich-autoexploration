import unittest
from near_copy_v2 import eva_glyphs, equal_after_one_deletion_each as near


class NearCopyV2Tests(unittest.TestCase):
    def test_deletion_each_and_symmetry(self):
        for a, b, expected in [
            ('abc', 'adc', True),
            ('abc', 'abx', True),
            ('abc', 'abcd', False),  # Levenshtein insertion
            ('abc', 'ac', False),    # Levenshtein deletion
            ('ab', 'cd', False),
            ('a', 'b', True),
            ('', '', False),
            ('abc', 'abc', True),   # scorer separately excludes identical pairs
            ('chd', 'shd', True),
            ('ch', 'c', True),
            ('chd', 'cd', True),
        ]:
            with self.subTest(a=a, b=b):
                self.assertEqual(near(a, b), expected)
                self.assertEqual(near(b, a), expected)

    def test_eva_segmentation(self):
        self.assertEqual(eva_glyphs('cthckhcphcfhchsh'),
                         ('cth', 'ckh', 'cph', 'cfh', 'ch', 'sh'))


if __name__ == '__main__':
    unittest.main()
