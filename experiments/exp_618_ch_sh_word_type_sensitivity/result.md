# Experiment 618 — word-type versus token-frequency sensitivity

## Method
Within IVTFF `$Q=T`, cells are matched by folio × exact token length × zero-based digraph position. For each cell, each distinct token type contributes at most once to the `ch` or `sh` group, regardless of how often that token repeats. Compare whether the next character is in `aeiouy`. Bootstrap resamples folios (20,000 replicates); the interval applies to the equal-weight mean of per-folio differences. This is a weighting sensitivity, not an independent replication.

| Transcription | Matched cells | Folios | Distinct ch types | ch vowel rate | Distinct sh types | sh vowel rate | Pooled sh−ch | Mean folio sh−ch | Bootstrap 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ZL3b | 280 | 23 | 1526 | 80.47% | 747 | 87.82% | 7.35 pp | 9.13 pp | 4.40 to 13.23 pp |
| IT2a | 283 | 23 | 1587 | 80.09% | 756 | 87.17% | 7.08 pp | 8.77 pp | 4.32 to 12.79 pp |

## Interpretation
The contrast remains positive after downweighting repeated tokens to unique word types within matched cells, with folio-bootstrap intervals above zero in both transcription sources. Caveat: a word type appearing on multiple folios can still contribute once on each folio, and exact word types may share templates. No linguistic meaning or phonetic interpretation is established.
