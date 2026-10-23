"""Pure tests for read-only AST detection; no experiment imports or writes."""
import importlib.util
from pathlib import Path
import unittest

PATH = Path(__file__).resolve().parents[1] / 'scripts' / 'audit_exp177_rng_provenance.py'
spec = importlib.util.spec_from_file_location('audit_exp177_rng_provenance', PATH)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class TestExp177RngAudit(unittest.TestCase):
    def test_detects_three_separate_issues(self):
        fixture = '''
import random

def make_word(onset, suffix):
    return onset + random.choice(['a', 'e']) + suffix

def generate_cipher_corpus(sentences, rng):
    all_words = list(sentences)
    rng.shuffle(all_words)
    return all_words

random.seed(42)
for cal in ['strong']:
    rng = random.Random(1 + hash(cal) % 1000)
'''
        self.assertEqual(audit.audit_source(fixture), {
            'python_hash_used_in_simulation_seed': True,
            'word_core_uses_global_random_not_local_rng': True,
            'plaintext_word_order_shuffled_before_encoding': True,
            'global_random_seed_42_present': True,
        })

    def test_no_false_positive_when_local_rng_used(self):
        fixture = '''
import random

def make_word(onset, suffix, rng):
    return onset + rng.choice(['a', 'e']) + suffix

def generate_cipher_corpus(sentences, rng):
    all_words = list(sentences)
    return all_words

random.seed(42)
rng = random.Random(1000)
'''
        flags = audit.audit_source(fixture)
        self.assertFalse(flags['python_hash_used_in_simulation_seed'])
        self.assertFalse(flags['word_core_uses_global_random_not_local_rng'])
        self.assertFalse(flags['plaintext_word_order_shuffled_before_encoding'])
        self.assertTrue(flags['global_random_seed_42_present'])

    def test_unrelated_hash_and_shuffle_not_flagged(self):
        fixture = '''
import random

def make_word(onset, suffix):
    return onset + suffix

def generate_cipher_corpus(sentences, rng):
    tmp = list(sentences)
    rng.shuffle(tmp)
    return tmp

h = hash('other')
'''
        flags = audit.audit_source(fixture)
        self.assertFalse(flags['python_hash_used_in_simulation_seed'])
        self.assertFalse(flags['plaintext_word_order_shuffled_before_encoding'])

    def test_missing_function_fails_closed(self):
        with self.assertRaises(ValueError):
            audit.audit_source('import random\n')


if __name__ == '__main__':
    unittest.main()
