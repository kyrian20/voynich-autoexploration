# Experiment 616 — folio-block holdout sensitivity (partial)

## Scope
This is an exploratory substitute for a true section holdout, **not** a completed codicological section analysis. We use coarse contiguous numeric folio blocks only because authoritative section boundaries have not yet been established for this filter. The blocks are heuristic: 103–106, 107–108, 111–113, and 114–116.

## Method
For each transcription, select IVTFF `$Q=T` matched cells defined as folio × exact token length × digraph position, with both `ch` and `sh`; terminal digraphs lacking a following character are excluded. Recompute pooled next-character vowel rates after removing each numeric block. This is a stability diagnostic, not an inferential test.

| Transcription | Omitted block | Cells remaining | Folios remaining | ch rate | sh rate | sh−ch |
|---|---|---:|---:|---:|---:|---:|
| ZL3b | 103–106 | 171 | 15 | 83.73% | 90.85% | 7.12 pp |
| ZL3b | 107–108 | 236 | 19 | 83.59% | 88.02% | 4.43 pp |
| ZL3b | 111–113 | 204 | 17 | 83.16% | 89.28% | 6.11 pp |
| ZL3b | 114–116 | 229 | 18 | 84.02% | 89.03% | 5.01 pp |
| IT2a | 103–106 | 173 | 15 | 82.96% | 90.32% | 7.36 pp |
| IT2a | 107–108 | 239 | 19 | 82.87% | 87.88% | 5.02 pp |
| IT2a | 111–113 | 208 | 17 | 82.79% | 88.86% | 6.07 pp |
| IT2a | 114–116 | 229 | 18 | 83.51% | 89.03% | 5.52 pp |

## Interpretation
The pooled direction remains positive when any one of these heuristic blocks is omitted in both transcription sources. Because the blocks are not verified manuscript sections and no cluster inference is performed at block level, this result must not be described as section-independent. Full section holdout remains open.
