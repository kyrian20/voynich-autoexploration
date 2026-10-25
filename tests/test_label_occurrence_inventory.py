import unittest
from scripts.build_label_occurrence_inventory import extract, digest, build

class LabelInventoryTests(unittest.TestCase):
    def parse(self, text):
        return extract(text, 'fixture', digest(text.encode()), {})

    def test_selection_includes_special_markers_and_nonnumeric_ids(self):
        text = '<fRos> <! $L=A>\n<fRos.0a,/L0> daiin\n<fRos.2,!Lf> qok\n<fRos.3,+P0> ignored\n'
        records, excluded, unknown = self.parse(text)
        self.assertEqual([r['id'] for r in records], ['fRos.0a', 'fRos.2'])
        self.assertEqual(len(excluded), 1)
        self.assertEqual(unknown, [])
        self.assertIn('special_record_marker_requires_adjudication', records[0]['exclusion_reasons'])

    def test_variants_and_source_line_are_retained(self):
        text = '<f65r> <! $L=B>\n<f65r.1,@Lp> otaim,dam.alam\n'
        row = self.parse(text)[0][0]
        self.assertEqual(row['source_line'], 2)
        self.assertEqual(row['raw_line_sha256'], digest(text.splitlines()[1].encode()))
        self.assertEqual(row['views']['split/primary/expand']['tokens'], ['otaim','dam','alam'])
        self.assertEqual(row['views']['join/primary/expand']['tokens'], ['otaimdam','alam'])
        self.assertFalse(row['eligible_for_semantic_evaluation'])
        self.assertIsNone(row['external_referent'])

    def test_unresolved_reading_is_visible_not_dropped(self):
        rows = self.parse('<f1r>\n<f1r.1,@L0> [unclosed\n')[0]
        self.assertEqual(len(rows), 1)
        self.assertTrue(all(v['error'] for v in rows[0]['views'].values()))
        self.assertTrue(rows[0]['lexer_diagnostics'])

    def test_coverage_errors_remain_explicit(self):
        text = '<f1r>\n<f2r.1,@Lp> x\n<f2r.1,@Lp> y\nbroken\n'
        records, _, unknown = self.parse(text)
        self.assertIn('page_header_mismatch', records[0]['exclusion_reasons'])
        self.assertIn('duplicate_locus_id_in_source', records[1]['exclusion_reasons'])
        self.assertEqual(unknown[0]['raw_line'], 'broken')

    def test_real_sources_are_complete_for_selected_rows(self):
        report = build()
        self.assertEqual(report['summary']['unparsed_lines'], 0)
        self.assertEqual(report['summary']['source_rows'], 2196)
        self.assertEqual(len({r['occurrence_id'] for r in report['records']}), 2196)
        self.assertEqual(report['summary']['semantic_eligible_rows'], 0)
        missing = report['cross_source_coverage']['IT2a']['missing_ids']
        self.assertIn('f2r.14', missing)
        row = next(r for r in report['records'] if r['edition']=='ZL3b' and r['id']=='f41v.1')
        self.assertIn('[e:o]', row['raw_body'])
        self.assertEqual(len(row['views']), 8)
        self.assertTrue(row['image_source_archived']['sha256'])

if __name__ == '__main__':
    unittest.main()
