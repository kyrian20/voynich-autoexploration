# Experiment 617 — high-support matched-cell sensitivity

## Method
Restrict to IVTFF `$Q=T`. A cell is folio × exact token length × zero-based digraph position and must contain both `ch` and `sh`. Unlike the main analysis, retain only cells with at least 3 occurrences of each digraph, then repeat at a stricter threshold of 5 each. Outcome is whether the following character belongs to `aeiouy`. Bootstrap resamples folios (20,000 replicates); its estimand is the unweighted mean of per-folio differences. This tests sensitivity to sparse cells, not an independent replication.

## Results
| Transcription | Minimum each | Cells retained / matched | Folios | ch rate | sh rate | Pooled sh−ch | Mean folio sh−ch | Bootstrap 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ZL3b | 3 | 109 / 286 | 23 | 83.17% | 88.49% | 5.32 pp | 7.91 pp | 3.24 to 12.26 pp |
| IT2a | 3 | 105 / 283 | 23 | 82.54% | 88.40% | 5.86 pp | 8.38 pp | 4.63 to 12.36 pp |
| ZL3b | 5 | 63 / 286 | 23 | 83.42% | 88.07% | 4.64 pp | 7.92 pp | 3.07 to 12.42 pp |
| IT2a | 5 | 62 / 283 | 22 | 82.38% | 87.99% | 5.61 pp | 7.45 pp | 2.51 to 12.13 pp |

## Interpretation
The pooled contrast remains positive in both transcriptions under both support thresholds. Bootstrap intervals should be read alongside small retained folio counts and the known dependencies among repeated word templates. No semantic or phonetic decoding follows from this result.
