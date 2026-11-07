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


    def test_opaque_ivtff_glyph_units(self):
        # Match the frozen wordpair reader's opaque-code segmentation.
        self.assertEqual(eva_glyphs('ch@123;sh'), ('ch', '@123;', 'sh'))
        self.assertEqual(eva_glyphs('@123;@456;'), ('@123;', '@456;'))
        self.assertEqual(eva_glyphs('@12;'), ('@', '1', '2', ';'))
        self.assertTrue(near('a@123;c', 'a@456;c'))
        self.assertFalse(near('a@123;c', 'a@123;cd'))

    def test_tokenizer_parity_with_frozen_reader(self):
        """Regression: v2 must use the same EVA units as the frozen audit."""
        from itertools import product
        from wordpair_audit import eva_glyphs as frozen_eva_glyphs

        units = ('a', 'ch', 'sh', 'cth', '@123;', '@456;', '@12;')
        words = [''] + [''.join(seq) for n in range(1, 4)
                        for seq in product(units, repeat=n)]
        self.assertEqual(len(words), 400)
        for word in words:
            with self.subTest(word=word):
                self.assertEqual(eva_glyphs(word), tuple(frozen_eva_glyphs(word)))


    def test_exhaustive_small_glyph_alphabet(self):
        """Independent nested-loop oracle over 85 words / 7,225 ordered pairs."""
        from itertools import product

        alphabet = ('a', 'b', 'ch', 'sh')
        words = [''] + [''.join(glyphs) for n in range(1, 4)
                        for glyphs in product(alphabet, repeat=n)]
        self.assertEqual(len(words), 85)
        for a in words:
            for b in words:
                x, y = eva_glyphs(a), eva_glyphs(b)
                expected = False
                if len(x) == len(y) and len(x) > 0:
                    for i in range(len(x)):
                        for j in range(len(y)):
                            if x[:i] + x[i+1:] == y[:j] + y[j+1:]:
                                expected = True
                self.assertEqual(near(a, b), expected, (a, b))


if __name__ == '__main__':
    unittest.main()
