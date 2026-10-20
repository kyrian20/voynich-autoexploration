# EXP-622 and external comparison: ch/sh context specificity

Date: 2026-10-20

## External lead

Christophe Parisel, “A Quantitative Confirmation of the Currier Language Distinction” (arXiv:2604.25979, v2 revised 2026-05-05): https://arxiv.org/abs/2604.25979

The preprint reports (as its author's claims) that a Beta-Binomial mixture over character-pair ratios predicts held-out Currier A/B folio labels at 89% accuracy and proposes a folio-level switch involving vowels after ch/sh. It further reports that word-template identity accounts for a large share of the modeled variance. These are not established facts until the exact analysis is independently reproduced; the preprint is not a decipherment.

## Our EXP-622 diagnostic

Source: ZL3b IVTFF, SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.

- 5,162 ch/sh occurrences had a character on both sides.
- 472 matched folio × token-length × digraph-position strata across 144 folios contained both ch and sh.
- Equal-weight mean next-character vowel-rate contrast (sh−ch): +4.38 percentage points.
- Equal-weight mean preceding-character vowel-rate contrast (sh−ch): +3.85 percentage points.
- Difference of those contrasts (following minus preceding): +0.53 percentage points.
- Within-stratum label-permutation test, 10,000 replicates: two-sided p=0.82342.

## Interpretation

This does not support the claim that the observed ch/sh separation is specifically stronger after the digraph than before it under this particular matched-cell null. It does not refute Parisel's different folio-level mixture model: the estimands, conditioning, and null hypotheses differ. It does reinforce the need to test a proposed switch with a folio-held-out design, verified $L Currier labels, transcription sensitivity, and a fixed feature family.

## Next tests

1. EXP-623 runs the same specificity interaction on IT2a as a transcription-sensitivity check; ZL3b and IT2a are alternative transcriptions of the same manuscript, not independent manuscript samples.
2. If the sign and scale are interpretable across transcriptions, implement a separate, preregistered folio-held-out test of whether the ch/sh post-digraph feature predicts verified Currier $L labels beyond baseline rates, hand, section, and word-template/position controls.
3. Preserve null and adverse results; do not infer phonetic values, semantic content, or decipherment from these distributional statistics.
