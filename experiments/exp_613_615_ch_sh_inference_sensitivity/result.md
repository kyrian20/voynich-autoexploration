# Experiments 613–615 — corrected ch/sh inference and sensitivity

Terminal `ch`/`sh` occurrences without a following character are excluded. This correction aligns the implementation with the stated outcome definition and makes ZL3b counts agree with experiment 612.

Method: IVTFF `$Q=T`; letter-run tokenization after markup removal; matched cells are folio × exact token length × zero-based digraph position and contain both digraphs. Outcome is whether the next character is in the vowel set. Bootstrap resamples folios (20,000 replicates) for the equal-weight mean of per-folio differences. Conditional permutation shuffles binary outcomes within matched cells while preserving ch/sh counts (20,000 replicates; two-sided plus-one p).

| Transcription | Inventory | Cells | Folios | ch rate | sh rate | Pooled sh−ch | Folio bootstrap 95% CI | Permutation p |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| ZL3b | aeiouy | 280 | 23 | 83.63% | 89.15% | 5.52 pp | 3.79 to 10.88 pp | 0.00005 |
| IT2a | aeiouy | 283 | 23 | 83.03% | 88.91% | 5.88 pp | 3.75 to 10.71 pp | 0.00005 |
| ZL3b | aeiou | 280 | 23 | 81.24% | 85.63% | 4.39 pp | 3.34 to 10.42 pp | 0.00795 |
| IT2a | aeiou | 283 | 23 | 80.44% | 85.53% | 5.09 pp | 3.78 to 10.53 pp | 0.00310 |

Leave-one-folio-out pooled differences remain positive for both transcriptions under both inventories. A Monte Carlo p of 0.00005 means zero exceedances in 20,000 draws (simulation floor), not an exact zero. ZL3b and IT2a are alternative transcriptions of the same manuscript, not independent historical samples. Word templates, section composition, and transcription decisions remain possible dependencies. No translation or decipherment is established.
