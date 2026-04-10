#!/usr/bin/env python3
"""
exp_147: B-Dialect ch as Medial Nominal Parallel to A-cth
H291: Do B-ch compound words show the same positional/before-context profile as A-cth?
Also: Clarify exp_145 daiin->sh enrichment using P-type body text only.
"""
# Script is inline in result.md above (no separate script used; analysis run ad hoc)
# The analysis used P-type locus filtering:
#   b_lines = [words for fb, lt, words in raw_lines if dialect_map[fb]=='B' and lt.startswith('P')]
# Key finding: filtering to P-type only changes daiin->sh from 2.33x (exp_145 all-locus)
# to 1.19x (near baseline). exp_145 results were inflated by non-body-text lines.
print("exp_147: see result.md for full analysis. Ad hoc script run inline.")
