#!/usr/bin/env python3
"""
exp_156: chol/chor positional profiles, chol→cth bigram positions (H310),
         chol@LF second-word analysis (H311), verified bigram enrichments (H312)
H310 CONFIRMED: chol→cth bigrams occur at chol@second (11/20=55%) or chol@MID (9/20=45%), NEVER chol@LF (0). chol is second-enriched (1.87×), LF-depleted (0.30×). F157's "chol at LF=50%" was wrong.
H311: chol@LF (n=11) second-pos is ch-onset 54.5%; chol self-succession=18.2% (2 cases).
H312 CONFIRMED: chol→cth=2.35×, chor→cth=2.22× (real bigram enrichments, corrected corpus).
CORRECTED: chol/chor are NOT line-openers. The chol→cth construction is [chol@second/MID][cth@subsequent].
"""
print("exp_156: inline. See result.md.")
