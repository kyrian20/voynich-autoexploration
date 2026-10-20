# EXP-623 — IT2a replication of ch/sh context-specificity interaction

## Question
Is the observed ch/sh vowel-rate contrast larger for the character after the digraph than for the character before it, after matching folio, exact token length, and digraph position?

## Method
Source: `data/transcriptions/eva_it2a.txt` (SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`). A simple parser extracts text rows and alphabetic tokens, then retains ch/sh occurrences with a character on both sides. Matched strata contain both digraphs. The statistic is the equally weighted mean across strata of [(sh−ch) following-vowel rate] − [(sh−ch) preceding-vowel rate]. The two-sided permutation test shuffles ch/sh labels within strata for 10,000 replicates, preserving the label count per stratum.

## Results
- Occurrences with both neighbors: 5,374
- Matched strata: 485
- Folios represented: 149
- Mean following-character contrast (sh−ch): 4.50 percentage points
- Mean preceding-character contrast (sh−ch): 5.41 percentage points
- Interaction (following minus preceding): -0.91 percentage points
- Two-sided permutation p: 0.69003 (6900 exceedances / 10,000)

## Interpretation and limits
This is a transcription-sensitivity replication of the diagnostic specificity test motivated by EXP-619, where the preceding-character control was not uniformly smaller than the primary contrast. A positive interaction supports a larger contrast after than before the digraph under this null; a non-positive or uncertain result does not support an outcome-specific claim. This remains exploratory, not a phonetic, semantic, language-identification, or decipherment result. ZL3b and IT2a are alternative transcriptions of the same manuscript; this experiment uses ZL3b only. The simple parser and the conditioning strategy leave possible lexical-template confounding.

See `results.json` for machine-readable details.
