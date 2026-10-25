import hashlib,tempfile,unittest
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

    def test_duplicate_refused(self):
        with self.assertRaises(ValueError):self.scan('<f68r3.11,@Ls> doaro\n<f68r3.11,@Ls> doary\n')

    def test_raw_glyph_positions_preserved(self):
        s=self.scan('<f68r3.11,@Ls> doaro\n')
        spans=s['target_locus']['payload_spans']
        self.assertEqual(''.join(x['raw'] for x in spans),'doaro')
        self.assertEqual(spans[-1],{'kind':'glyph','raw':'o','start':4,'end':5})

if __name__=='__main__':unittest.main()
