from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from analyze_two_token_residual import TwoToken, score, synthetic, triples


class TwoTokenTests(unittest.TestCase):
    def test_known_sensitivity_and_negative(self):
        self.assertGreater(synthetic(True)['score']['older_identity_gain'], .5)
        self.assertLess(abs(synthetic(False)['score']['older_identity_gain']), 1e-10)

    def test_normalization_seen_and_unseen(self):
        train = [{'group': 'train', 'tokens': ['aba', 'mid', 'xx']},
                 {'group': 'train', 'tokens': ['aca', 'mid', 'yy']}]*30
        dev = [{**r, 'group': 'dev'} for r in train]
        model = TwoToken(train, dev)
        for z, a in (('aba', 'mid'), ('aca', 'mid'), ('new', 'unseen')):
            probs = [model.probabilities(z, a, b) for b in model.base.events]
            for layer in range(3):
                self.assertAlmostEqual(sum(p[layer] for p in probs), 1.0, places=12)

    def test_group_leak_rejected(self):
        rows = [{'group': 'same', 'tokens': ['a', 'b', 'c']}]
        with self.assertRaises(ValueError):
            TwoToken(rows, rows)

    def test_no_gain_from_proportional_unequal_identity_counts(self):
        pairs = [('aba', 'xx')]*2+[('aba', 'yy')]+[('aca', 'xx')]*4+[('aca', 'yy')]*2
        train = [{'group': 'train', 'tokens': [z, 'mid', b]} for z, b in pairs]*10
        dev = [{**r, 'group': 'dev'} for r in train]
        test = [{**r, 'group': 'test'} for r in train]
        self.assertLess(abs(score(TwoToken(train, dev), test)['older_identity_gain']), 1e-10)

    def test_no_cross_line_triplets(self):
        self.assertEqual(triples([{'tokens': ['a', 'b']}, {'tokens': ['c', 'd']}]), {})

    def test_no_evaluation_triplets_rejected(self):
        train = [{'group': 'train', 'tokens': ['a', 'b', 'c']}]
        dev = [{'group': 'dev', 'tokens': ['a', 'b', 'c']}]
        with self.assertRaises(ValueError):
            score(TwoToken(train, dev), [{'group': 'test', 'tokens': ['a']}])


if __name__ == '__main__':
    unittest.main()
