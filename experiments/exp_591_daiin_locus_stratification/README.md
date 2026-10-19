# exp_591 — daiin by exact IVTFF body-locus subtype

**Question:** does the Currier-B line-initial excess from exp_589 remain in the dominant P0 locus, or is it explained by mixing IVTFF body-locus subtypes?

## Protocol
- ZL3b only; this is a sensitivity test, not a second-transcription replication.
- Uses the same conservative token cleanup and body-locus rule as exp_589/590, but keeps the exact locus code (P0, P1, Pb, Pc, Pr) after stripping IVTFF prefix modifiers.
- Lines must contain at least two clean tokens.
- 2,000 fixed-seed within-line random-position draws; the expected first count conditions on every line's own token inventory and length.
- Primary test family: Currier-B locus strata with at least 50 lines, corrected using Holm's method. Currier-A loci are separately corrected as a secondary family. Smaller strata remain descriptive.
- Output reports first/last counts, conditional expectations and effect ratios; locus codes are not assigned grammatical meanings.

## Status
GitHub Actions generates and commits `results.json` and uploads an artifact. Results should be interpreted alongside exp_589 and exp_590, with null and small-sample outcomes kept visible.
