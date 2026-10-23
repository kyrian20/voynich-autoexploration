from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_exp173_paragraph_strata import marked_end, stratum, metric
from audit_exp173_reader_bridge import historical_tokens
from ivtff_lossless import lex, tokens


class ParagraphStrata(unittest.TestCase):
    def test_fixed_fixture_partition_and_counts(self):
        fixture = [('P0', 'y.xam<$>'), ('P0', 'y.xam'), ('Pb', 'y.xam')]
        observed = []
        names = []
        for locus, body in fixture:
            p = lex(body)
            names.append(stratum({'locus': locus, 'payload': p}))
            observed.append([metric([historical_tokens(body)])['am_final']['observed'],
                             metric([tokens([p])])['am_final']['observed']])
        self.assertEqual(names, ['P0/marked_end', 'P0/no_marked_end', 'other_P/no_marked_end'])
        self.assertEqual(observed, [[0, 1], [1, 1], [1, 1]])
        self.assertEqual([sum(x[i] for x in observed) for i in (0, 1)], [2, 3])

    def test_no_marker_does_not_infer_end(self):
        self.assertFalse(marked_end(lex('am')))
        self.assertFalse(marked_end(lex('am<!end>')))

    def test_nested_marker_rejected(self):
        with self.assertRaises(ValueError):
            marked_end(lex('[x<$>:y]'))

    def test_unresolved_rejected(self):
        with self.assertRaises(ValueError):
            marked_end(lex('am<$'))

    def test_singleton_fixed_endpoint(self):
        result = metric([['am']])
        self.assertEqual(result['singleton_lines'], 1)
        self.assertEqual(result['am_final']['ratio_within_line'], 1)


if __name__ == '__main__':
    unittest.main()
