# EXP-622 — ch/sh context-specificity interaction

## Question
Is the observed ch/sh vowel-rate contrast larger for the character after the digraph than for the character before it, after matching folio, exact token length, and digraph position?

## Method
Source: `data/transcriptions/eva_zl3b.txt` (SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`). A simple parser extracts text rows and alphabetic tokens, then retains ch/sh occurrences with a character on both sides. Matched strata contain both digraphs. The statistic is the equally weighted mean across strata of [(sh−ch) following-vowel rate] − [(sh−ch) preceding-vowel rate]. The two-sided permutation test shuffles ch/sh labels within strata for 10,000 replicates, preserving the label count per stratum.

## Results
- Occurrences with both neighbors: 5,162
- Matched strata: 472
- Folios represented: 144
- Mean following-character contrast (sh−ch): 4.38 percentage points
- Mean preceding-character contrast (sh−ch): 3.85 percentage points
- Interaction (following minus preceding): 0.53 percentage points
- Two-sided permutation p: 0.82342 (8234 exceedances / 10,000)

## Interpretation and limits
This is a diagnostic specificity test motivated by EXP-619, where the preceding-character control was not uniformly smaller than the primary contrast. A positive interaction supports a larger contrast after than before the digraph under this null; a non-positive or uncertain result does not support an outcome-specific claim. This remains exploratory, not a phonetic, semantic, language-identification, or decipherment result. ZL3b and IT2a are alternative transcriptions of the same manuscript; this experiment uses ZL3b only. The simple parser and the conditioning strategy leave possible lexical-template confounding.

See `results.json` for machine-readable details.
