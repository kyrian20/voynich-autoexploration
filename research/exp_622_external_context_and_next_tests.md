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


## EXP-623 result and decision update (2026-10-20)

GitHub Actions completed successfully for commit `119598765165c0b795d21500d89053ad24bdb024`: [run 39486630716](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39486630716).

EXP-623 uses IT2a, SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`:
- 5,374 occurrences with two neighbors; 485 matched strata; 149 folios.
- Following-character contrast (sh−ch): +4.50 percentage points.
- Preceding-character contrast (sh−ch): +5.41 percentage points.
- Interaction (following minus preceding): −0.91 percentage points.
- Two-sided within-stratum permutation p=0.69003 (10,000 replicates).

EXP-622 (ZL3b) gave +0.53 pp, p=0.82342. The interaction changes sign across transcription files and is non-significant in both. This is a transcription-sensitivity check, not an independent replication on another manuscript. The evidence does **not** support a claim that the ch/sh contrast is specific to the following character. Keep the broader descriptive ch/sh contrast separate from any claim about its mechanism.

## Decision for next work

Do not create another near-duplicate ch/sh interaction test. The next defensible step is a new, explicitly preregistered held-out Currier A/B prediction study only after:
1. verify $L labels from folio headers, never substitute $Q (quire) or $I;
2. independently audit parsing against IVTFF fixtures and edge cases;
3. freeze a small feature set and controls before scoring;
4. split by folio (preferably externally grounded sections where source boundaries are documented), keeping all tokens from a folio in one partition;
5. compare against a majority-class baseline and simple metadata-only baseline, report balanced accuracy, confusion matrix, and uncertainty;
6. test transcription sensitivity (ZL3b and IT2a) without treating the files as independent samples.

Until those checks are implemented, do not report a predictive result.

## Additional gate discovered during 2026-10-20 review

The existing `experiments/exp_602_independent_ivtff_parser_audit/results.json` has identical record IDs but substantial token-list disagreement: 1,466 rows for ZL3b and 1,472 for ZL3a. Thus this is not yet a successful tokenization-conformance audit. Also, EXP-602's held-out test predicts line-initial token positions in Currier B/P0; it is not a held-out Currier A/B classifier. See [EXP-624 parser disagreement and prediction gate](exp_624_parser_disagreement_and_prediction_gate.md). The Currier A/B prediction study remains unrun until tokenization policy and $L metadata handling are validated.
