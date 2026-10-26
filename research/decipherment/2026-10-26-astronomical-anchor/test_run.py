import hashlib,json,os,tempfile,unittest
from pathlib import Path
import run

class AnchorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import sys,os
        sys.path.insert(0,os.environ.get('ANCHOR_REPO_ROOT','.'))
        from scripts.ivtff_lossless import lex,tokens
        cls.lex=staticmethod(lex);cls.tokens=staticmethod(tokens)

    def scan(self,raw):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'fixture.txt';p.write_text(raw)
            run.EXPECTED[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
            try:return run.inventory(p,self.lex,self.tokens)
            finally:del run.EXPECTED[p.name]

    def test_exact_tokens_not_substrings(self):
        s=self.scan('<f68r3.11,@Ls> doaro.adoary.doaryx.dary\n')
        self.assertEqual(s['views']['split']['doary']['count'],0)
        self.assertEqual(s['views']['split']['doaro']['count'],1)
        self.assertEqual(s['views']['split']['dary']['count'],1)

    def test_alternative_and_uncertain_space_explicit(self):
        s=self.scan('<f68r3.11,@Ls> [doaro:doary].doa,ry\n')
        self.assertEqual(s['views']['split']['doaro']['count'],1)
        self.assertEqual(s['views']['split']['doary']['count'],0)
        self.assertEqual(s['views']['join']['doary']['count'],1)

    def test_excluded_non_numeric_locus_is_reported(self):
        s=self.scan('<f68r3.11,@Ls> doaro\n<f68r3.X,@Ls> doary\n')
        self.assertEqual(len(s['unparsed_target_bearing_lines']),1)
        self.assertEqual(s['numeric_records'],1)

    def test_named_page_is_not_a_numeric_page(self):
        s=self.scan('<f68r3> header\n<f68r3.11,@Ls> doaro\n<fRos> header\n<fRos.1,@L0> dary\n')
        self.assertEqual(s['parsed_records'],2)
        self.assertEqual(s['numeric_records'],1)
        self.assertEqual(s['named_records'],1)
        self.assertEqual(s['parsed_records'],s['numeric_records']+s['named_records'])
        self.assertEqual(s['views']['split']['dary']['matches'][0]['page'],'fRos')

    def test_non_ascii_decimal_identifiers_fail_closed(self):
        # The source hashes are frozen, but the reader must reject bad future
        # IVTFF IDs instead of silently excluding them from exact-token counts.
        bad_rows = (
            '<f٦٨r3.12,@Ls> doary\\n',
            '<f68r3.١٢,@Ls> doary\\n',
            '<fRos.١,@L0> doary\\n',
        )
        for bad in bad_rows:
            with self.subTest(row=bad):
                with self.assertRaisesRegex(ValueError, 'Non-ASCII decimal digit'):
                    self.scan('<f68r3.11,@Ls> doaro\\n' + bad)

    def test_missing_target_locus_refused(self):
        with self.assertRaisesRegex(ValueError,'target locus'):
            self.scan('<fRos.1,@L0> dary\n')

    def test_duplicate_refused(self):
        with self.assertRaises(ValueError):self.scan('<f68r3.11,@Ls> doaro\n<f68r3.11,@Ls> doary\n')

    def test_raw_glyph_positions_preserved(self):
        s=self.scan('<f68r3.11,@Ls> doaro\n')
        spans=s['target_locus']['payload_spans']
        self.assertEqual(''.join(x['raw'] for x in spans),'doaro')
        self.assertEqual(spans[-1],{'kind':'glyph','raw':'o','start':4,'end':5})

    def test_frozen_corpora_preserve_historical_matches_and_split_counts(self):
        root=Path(os.environ.get('ANCHOR_REPO_ROOT','.')).resolve()
        historical=json.loads(Path(__file__).with_name('inventory.json').read_text())
        expected_counts={'eva_zl3b.txt':(5385,5225,160),'eva_it2a.txt':(5215,5215,0)}
        for old in historical['sources']:
            with self.subTest(source=old['file']):
                current=run.inventory(root/'data/transcriptions'/old['file'],self.lex,self.tokens)
                self.assertEqual((current['parsed_records'],current['numeric_records'],current['named_records']),expected_counts[old['file']])
                self.assertEqual(current['parsed_records'],old['numeric_records'])
                for key in ('file','sha256','target_locus','unparsed_target_bearing_lines','views'):
                    self.assertEqual(current[key],old[key])

if __name__=='__main__':unittest.main()
