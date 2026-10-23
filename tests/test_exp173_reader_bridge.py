from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_exp173_reader_bridge import historical_tokens, metrics, paired_leave_one_out, POLICIES
from ivtff_lossless import lex, tokens


class ReaderBridgeTests(unittest.TestCase):
    def test_paragraph_end_not_part_of_word(self):
        body = 'y.xam<$>'
        old = historical_tokens(body)
        new = tokens([lex(body)])
        self.assertEqual(old, ['y', 'xam<$>'])
        self.assertEqual(new, ['y', 'xam'])
        self.assertEqual(metrics([old])['am_final']['observed'], 0)
        self.assertEqual(metrics([new])['am_final']['observed'], 1)

    def test_alternative_exclusion_moves_first_token(self):
        payload = lex('[x:y].yam.z')
        self.assertEqual(tokens([payload]), ['x', 'yam', 'z'])
        self.assertEqual(tokens([payload], alternatives='exclude_word'), ['yam', 'z'])

    def test_uncertain_boundary_changes_both_endpoints(self):
        payload = lex('x,yam')
        split, join = tokens([payload]), tokens([payload], uncertain_space='join')
        self.assertEqual(split, ['x', 'yam'])
        self.assertEqual(join, ['xyam'])
        self.assertNotEqual(metrics([split])['am_final']['ratio_within_line'],
                            metrics([join])['am_final']['ratio_within_line'])

    def test_opaque_glyph_not_fragmented(self):
        self.assertEqual(tokens([lex('@180;yam.?am')]), ['@180;yam', '?am'])

    def test_ligature_views_are_explicit(self):
        payload = lex('y.x{am}')
        self.assertEqual(tokens([payload]), ['y', 'xam'])
        self.assertEqual(tokens([payload], ligatures='opaque'), ['y', 'x{am}'])

    def test_all_eight_policies_and_empty_tokens(self):
        self.assertEqual(len(POLICIES), 8)
        self.assertEqual(tokens([lex('[am:y]')], alternatives='exclude_word'), [])
        self.assertEqual(metrics([[]])['lines'], 0)
        self.assertIsNone(metrics([[]])['am_final'])

    def test_leave_one_out_removes_both_sides(self):
        rows = [{'id': 'f1r.1', 'number': 1}, {'id': 'f1v.1', 'number': 1}, {'id': 'f2r.1', 'number': 2}]
        old = {r['id']: ['yam', 'xam'] for r in rows}
        new = {r['id']: ['y', 'xam'] for r in rows}
        result = paired_leave_one_out(rows, old, new)
        self.assertEqual([r['removed_lines'] for r in result], [2, 1])
        self.assertEqual(result[0]['effects']['am_final']['historical'], 1)
        self.assertEqual(result[0]['effects']['am_final']['candidate'], 2)

    def test_unresolved_payload_refused(self):
        with self.assertRaises(ValueError):
            tokens([lex('y.[am')])


if __name__ == '__main__':
    unittest.main()
