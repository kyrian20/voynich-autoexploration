#!/usr/bin/env python3
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('sensitivity',ROOT/'scripts/audit_reference_entropy_sensitivity.py')
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

class EntropyControls(unittest.TestCase):
    def test_deterministic_transition_has_zero_conditional_entropy(self):
        rows=audit.direct_profile(['ab','ba']*3,2)
        self.assertAlmostEqual(rows[1]['marginal_bits'],1)
        self.assertAlmostEqual(rows[1]['conditional_bits'],0)

    def test_independent_balanced_transition_has_one_bit(self):
        rows=audit.direct_profile(['aa','ab','ba','bb'],2)
        self.assertAlmostEqual(rows[1]['conditional_bits'],1)

    def test_tail_counts_condition_on_surviving_words(self):
        rows=audit.direct_profile(['a','ab','abc'],4)
        self.assertEqual([r['n'] for r in rows],[3,2,1,0])
        self.assertIsNone(rows[-1]['conditional_bits'])

    def test_original_and_independent_formulas_agree(self):
        original,_=audit.isolated_historical()
        audit.verified_profile(['a','ab','ba','cabbage','aba','ba','abc'],original)

if __name__=='__main__':unittest.main()
