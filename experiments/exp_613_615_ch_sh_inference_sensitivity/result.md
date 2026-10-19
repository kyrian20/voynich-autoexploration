# Experiments 613–615 — ch/sh follow-up

## Status
Calculated in this session from the repository's current ZL3b and IT2a transcription files. This is a conditional distributional analysis, not a decipherment or causal result.

## Shared method
IVTFF line headers provide folio and $Q metadata. The exploratory parser strips IVTFF markup from line bodies, tokenizes letter runs, and records each `ch` or `sh` occurrence that has a following character. Outcome: whether that next character belongs to the selected vowel set. Analysis is restricted to IVTFF `$Q=T` and matched cells containing both digraphs, defined as folio × exact token length × zero-based digraph position. Counts below are from this implementation and need not exactly match older reports using different tokenization or filters.

## 613 — Folio-clustered bootstrap
Bootstrap resamples folios with replacement (20,000 replicates; percentile 95% CI). The estimate is the unweighted mean of per-folio differences (sh vowel rate minus ch vowel rate); pooled rates are shown separately.

| Transcription | Matched cells | Folios | ch rate | sh rate | Pooled sh−ch | Mean folio sh−ch | Bootstrap 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|
| ZL3b | 286 | 23 | 83.69% | 89.21% | 5.53 pp | 7.58 pp | 3.77 to 10.86 pp |
| IT2a | 283 | 23 | 83.03% | 88.91% | 5.88 pp | 7.49 pp | 3.75 to 10.71 pp |

The percentile intervals are above zero in both transcriptions under this folio-equal-weight estimand. Leave-one-folio-out pooled differences range from 5.01 to 6.94 pp (ZL3b) and 5.48 to 6.93 pp (IT2a); the pooled direction survives omission of any single included folio.

## 614 — Within-cell permutation
Within each matched cell, the binary vowel/non-vowel outcomes were shuffled while preserving the number of `ch` and `sh` occurrences. Two-sided plus-one Monte Carlo p-values (20,000 replicates): ZL3b **0.00005**; IT2a **0.00005**. Zero exceedances in 20,000 draws means the Monte Carlo estimate is bounded by the simulation resolution; it does not mean the exact p-value is zero. This is conditional on exchangeability of outcomes within each matched cell and does not control all word-template or transcription dependencies.

## 615 — Vowel-inventory sensitivity
Changing the vowel inventory from `aeiouy` to `aeiou`:

| Transcription | ch rate | sh rate | Pooled sh−ch | Folio-bootstrap 95% CI | Within-cell permutation p |
|---|---:|---:|---:|---:|---:|
| ZL3b | 81.30% | 85.71% | 4.41 pp | 3.33 to 10.40 pp | 0.00575 |
| IT2a | 80.44% | 85.53% | 5.09 pp | 3.78 to 10.53 pp | 0.00310 |

The direction remains positive with the narrower vowel inventory. This is a sensitivity check, not an independent replication because the source tokens are the same.

## Interpretation and caveats
- There is a repeatable local distributional contrast: within the selected metadata class and matched length/position contexts, `sh` is followed by a member of the tested vowel set more often than `ch` in both transcriptions.
- The transcriptions are not independent manuscripts; ZL3b and IT2a are alternative transcription sources for the same artifact, so agreement tests transcription robustness rather than independent historical replication.
- Folios are resampled as clusters, but repeated word types, line structure, sections, and transcriber decisions can still induce dependence. The permutation's exchangeability assumption is not guaranteed.
- No semantic value, translation, phonetic value, or decipherment is established. Next: audit tokenization against an independent parser and run preregistered negative controls/multiple-testing review.
