# Experiment 617 — high-support matched-cell sensitivity (corrected parser)

Terminal `ch`/`sh` occurrences without a following character are excluded. Restrict to IVTFF `$Q=T`; a cell is folio × exact token length × digraph position and contains both digraphs. Retain cells with at least 3 occurrences of each digraph, then repeat at a stricter threshold of 5 each. Outcome: next character in `aeiouy`. Folio bootstrap: 20,000 replicates, equal-weight mean of per-folio differences.

| Transcription | Min each | Retained / matched cells | Folios | ch rate | sh rate | Pooled sh−ch | Bootstrap 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|
| ZL3b | 3 | 109 / 280 | 23 | 83.17% | 88.49% | 5.32 pp | 3.24 to 12.26 pp |
| IT2a | 3 | 105 / 283 | 23 | 82.54% | 88.40% | 5.86 pp | 4.63 to 12.36 pp |
| ZL3b | 5 | 63 / 280 | 23 | 83.42% | 88.07% | 4.64 pp | 3.07 to 12.42 pp |
| IT2a | 5 | 62 / 283 | 22 | 82.38% | 87.99% | 5.61 pp | 2.51 to 12.13 pp |

The direction remains positive in both sources at both support thresholds. This is a sensitivity check, not an independent replication; repeated word templates and the conditional cell selection remain limitations.
