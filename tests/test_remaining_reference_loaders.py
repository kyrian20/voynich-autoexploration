#!/usr/bin/env python3
import ast
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('remaining', ROOT/'scripts/audit_remaining_reference_loaders.py')
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

class RemainingReaderTests(unittest.TestCase):
    def fixture(self, experiment, text):
        source=(ROOT/'experiments'/experiment/'script.py').read_text()
        # A module-level exception proves that importing the experiment is forbidden.
        with tempfile.TemporaryDirectory() as directory:
            directory=Path(directory)
            path=directory/'script.py'
            corpus=directory/'fixture.txt'
            path.write_text("raise RuntimeError('whole module executed')\n"+source)
            corpus.write_text(text)
            original=audit.ROOT
            try:
                audit.ROOT=directory
                return audit.replay(experiment,path,corpus)
            finally:
                audit.ROOT=original

    def test_inline_minimum_two_preserves_case_and_english(self):
        r=self.fixture('exp_267_word_length_position','I am Latin. The book. Arma virumque.')
        self.assertEqual(r['selected_units'],6)
        self.assertEqual(r['first_units'],['am','Latin','The','book','Arma'])

    def test_inline_onset_loop_matches_and_keeps_english(self):
        r=self.fixture('exp_288_stolfi_onset_decomp','I am arma. The book. rhythm.')
        self.assertEqual(r['selected_units'],4)
        self.assertEqual(r['first_units'][0],{'onset':'rm','wlen':4,'blen':1,'mlen':0})
        self.assertEqual(r['last_units'][-1]['blen'],0)

    def test_line_filter_counts_unicode_letters_and_retains_headers(self):
        r=self.fixture('exp_170_naibbe_simulation','12\nab\nABC\nééé\nThe book\n')
        self.assertEqual(r['first_units'],['ABC','ééé','The book'])

    def test_gutenberg_coordinate_bug_exposed(self):
        r=self.fixture('exp_001_word_initial_entropy','header\n*** START OF title ***\narma cano\n*** END OF title ***\nenglish footer retained')
        c=r['gutenberg_coordinate_check']
        self.assertGreater(c['token_delta'],0)
        self.assertGreater(c['historical_selected_characters'],c['coordinate_corrected_characters'])

    def test_no_markers_plain_ascii(self):
        r=self.fixture('exp_001_word_initial_entropy','Arma virumque cano')
        self.assertEqual(r['first_units'],['arma','virumque','cano'])
        self.assertEqual(r['gutenberg_coordinate_check']['token_delta'],0)

    def test_missing_reader_fails(self):
        with self.assertRaises(ValueError):
            audit.select(ast.parse('x=1'), 'exp_267_word_length_position')

if __name__=='__main__': unittest.main()
