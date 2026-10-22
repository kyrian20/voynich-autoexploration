#!/usr/bin/env python3
"""Adversarial controls on the original loader, isolated from module execution."""
import ast
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('loader_audit', ROOT/'scripts/audit_historical_latin_loaders.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

class LoaderAuditTests(unittest.TestCase):
    def replay(self, fixture, experiment='exp_180_position_aware_hybrid'):
        source = (ROOT/'experiments'/experiment/'script.py').read_text()
        name = 'parse_latin' if experiment.startswith('exp_259') else 'extract_latin_sentences'
        function = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == name)
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            script = temporary/'script.py'
            # This must never execute: proves the whole experiment is not imported.
            script.write_text("raise RuntimeError('module body ran')\n"+ast.unparse(function))
            corpus = temporary/'fixture.txt'
            corpus.write_text(fixture)
            original = audit.ROOT
            try:
                audit.ROOT = temporary
                return audit.replay(script, corpus)
            finally:
                audit.ROOT = original

    def test_english_heading_survives_historical_filter(self):
        row = self.replay('CONTENTS\n\nCORRECTIONS:\n\nBibliography')
        self.assertEqual(row['selected_tokens'], 3)
        self.assertEqual(row['chunking']['returned_tokens'], 0)
        self.assertEqual(row['chunking']['omitted_tail_tokens'], 3)

    def test_english_prose_rejected_but_metadata_retained(self):
        row = self.replay('The book is in the house and it is for him.\n\nCONTENTS')
        self.assertEqual(row['selected_tokens'], 1)
        self.assertEqual(row['retained_paragraphs'], 1)

    def test_latin_homographs_can_trigger_rejection(self):
        row = self.replay('in in in arma virumque cano')
        self.assertEqual(row['selected_tokens'], 0)

    def test_unfiltered_reader_retains_both_languages(self):
        row = self.replay('The book is here.\n\nArma virumque cano.', 'exp_259_char_positional_entropy')
        self.assertEqual(row['selected_tokens'], 7)
        self.assertEqual(row['filter'], 'NONE')

if __name__ == '__main__':
    unittest.main()
