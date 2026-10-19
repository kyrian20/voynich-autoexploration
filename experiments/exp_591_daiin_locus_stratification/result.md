# exp_591 — Results: daiin by exact IVTFF body-locus subtype

**Execution date:** 2026-10-19  
**Status:** completed successfully in GitHub Actions  
**Machine-readable output:** `results.json`; source SHA-256 is recorded inside it.  
**Workflow run:** https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256723800

## Question
Does the Currier-B initial-position effect persist in the dominant P0 locus, or does it arise from combining different IVTFF body-locus subtypes?

## Results

| Currier / locus | Lines (minimum 2 tokens) | `daiin` tokens | Observed first | Expected first | Enrichment | Nominal p | Holm-adjusted p |
|---|---:|---:|---:|---:|---:|---:|---:|
| B / P0 | 2,345 | 298 | 89 | 31.53 | 2.823× | 0.0005 | 0.0015 |
| B / P1 | 62 | 7 | 4 | 1.11 | 3.609× | 0.0125 | 0.0250 |
| B / Pb | 116 | 12 | 4 | 2.47 | 1.621× | 0.2104 | 0.2104 |
| A / P0 | 1,501 | 485 | 59 | 67.85 | 0.870× | 0.9020 | 0.9020 |
| A / P1 | 10 | 4 | 1 | 0.98 | 1.017× | — | descriptive only |
| A / Pc | 8 | 0 | 0 | 0.00 | — | — | descriptive only |
| B / Pc | 8 | 0 | 0 | 0.00 | — | — | descriptive only |
| A / Pr | 5 | 1 | 1 | 0.50 | 2.000× | — | descriptive only |
| B / Pr | 7 | 0 | 0 | 0.00 | — | — | descriptive only |

The B primary family is the three locus subtypes with at least 50 lines, adjusted with Holm's method. The A family is adjusted separately. The p=0.0005 result is the Monte Carlo resolution floor from 2,000 replicates, not an exact p-value.

## Interpretation

**The Currier-B effect is present in P0**, the dominant body-locus code: 89 observed initial `daiin` tokens versus 31.53 expected under within-line exchangeability, an approximately 2.82× enrichment; Holm-adjusted p=0.0015. P0 accounts for 3,846 of 4,062 parsed body lines overall (about 94.7%).

P1 also shows an elevated rate (4 vs 1.11 expected, Holm-adjusted p=0.025), but it has only 62 B lines and seven target tokens, so the magnitude is less stable. Pb is positive descriptively but not statistically distinguished from the null in this run (Holm-adjusted p=0.210). Small Pc/Pr groups do not support reliable inference.

Currier-A P0 has no evidence of first-position enrichment under this test (0.87×, adjusted p=0.902). That agrees with the overall A/B contrast in exp_589. This argues against a result caused solely by mixing the main P0 locus with rare body-locus subtypes.

## Limitations
- The null preserves each line's token inventory and length but treats positions as exchangeable within a line.
- Locus codes P0/P1/Pb/Pc/Pr are reported as IVTFF codes only; this report does not assign them grammatical meanings.
- P-values are one-sided tests for initial-position excess. Sparse groups are descriptive, not negative evidence.
- This is still one transcription (ZL3b); the independent ZL3a replication belongs to exp_589.
- A positional effect is not a decipherment and does not determine the meaning of `daiin`.

## Next test
Assess whether the B/P0 result is spread across folios or depends on one/few high-leverage folios. Run leave-one-folio-out influence analysis and summarize folio-level contributions before developing semantic hypotheses.
