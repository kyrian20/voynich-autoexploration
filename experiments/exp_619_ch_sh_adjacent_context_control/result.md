# Experiment 619 — adjacent-context control for ch/sh

## Purpose and limitation
Test whether the ch/sh difference is specific to the following-character vowel outcome or whether a similar contrast appears in the preceding-character context. This is a diagnostic negative-control outcome, not a guaranteed null: orthographic templates may influence both sides.

## Method
Restrict to IVTFF `$Q=T`, tokens with a character before and after the digraph, and matched folio × exact token length × digraph-position cells containing both `ch` and `sh`. Outcomes are whether the preceding (control) or following (primary) character is in `aeiouy`. Bootstrap resamples folios (20,000 replicates); conditional permutation shuffles binary outcomes within matched cells (20,000 replicates).

| Transcription | Outcome | Matched cells | Folios | ch rate | sh rate | sh−ch | Folio bootstrap 95% CI | Permutation p |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| ZL3b | preceding control | 151 | 22 | 14.25% | 21.66% | 7.41 pp | -1.86 to 17.49 pp | 0.08320 |
| ZL3b | following primary | 151 | 22 | 87.25% | 93.50% | 6.26 pp | 4.64 to 11.56 pp | 0.00220 |
| IT2a | preceding control | 153 | 22 | 15.97% | 24.13% | 8.16 pp | -1.04 to 16.80 pp | 0.01835 |
| IT2a | following primary | 153 | 22 | 87.58% | 92.31% | 4.73 pp | 0.86 to 8.73 pp | 0.03535 |

## Interpretation
The preceding-character contrast is not uniformly smaller; this warns that general token-template/context effects may contribute. Do not treat this single exploratory control as a multiple-testing correction or proof that confounding is absent. ZL3b and IT2a are alternate transcriptions of the same manuscript.
