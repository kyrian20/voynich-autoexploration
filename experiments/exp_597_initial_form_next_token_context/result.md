# exp_597 — Results: next-token context after initial daiin/dain/saiin

**Execution date:** 2026-10-19  
**Workflow:** https://github.com/kyrian20/voynich-autoexploration/actions/runs/39258573517  
**Machine-readable output:** `results.json`

## Question
Do Currier-B P0 lines beginning with `daiin`, `dain`, and `saiin` have distinguishable distributions of the immediately following token?

## Sample sizes and diversity

| First token | Lines | Unique next tokens | Next-token entropy (bits) |
|---|---:|---:|---:|
| `daiin` | 89 | 67 | 5.872 |
| `dain` | 34 | 28 | 4.676 |
| `saiin` | 46 | 39 | 5.176 |

The 2,354-line Currier-B P0 set is the same in each transcription; starter counts are 89 `daiin`, 34 `dain`, and 46 `saiin`.

## Pairwise context-distribution tests

Jensen–Shannon divergence (JSD) measures how different the empirical next-token distributions are; the permutation test shuffles the pooled successor labels between each pair while keeping sample sizes.

| Pair | Observed JSD (bits) | Mean null JSD | Upper-tail p | Holm-adjusted p |
|---|---:|---:|---:|---:|
| `daiin` vs `dain` | 0.682 | 0.711 | 0.7457 | 1.000 |
| `daiin` vs `saiin` | 0.632 | 0.690 | 0.9430 | 1.000 |
| `dain` vs `saiin` | 0.655 | 0.705 | 0.8540 | 1.000 |

These JSD statistics were **not unusually large** relative to the permutation null. This analysis therefore does not find a statistically detectable distinction between these three successor distributions, at the resolution and sample sizes tested. It also does not establish equivalence: the groups are modest in size, especially the 34 `dain` starters.

The same pattern is recovered in ZL3a. The observed JSD values match those in ZL3b to six decimals; all Holm-adjusted pairwise p-values are 1.0. This near identity is expected given the very similar token/locus rows in the two files, so it should be described as version robustness, not two fully independent manuscript samples.

## Common immediate successors

The most frequent successors overlap:
- After `daiin`: `shey` (6/89, 6.7%), `chey` (4/89, 4.5%), then `sheol`, `chedy`, and `shody` (3 each).
- After `dain`: `chey` (4/34, 11.8%), then `cheky`, `shey`, and `ar` (2 each).
- After `saiin`: `shey` (4/46, 8.7%), followed by `shedy`, `or`, and `al` (2 each).

The shared presence of `shey`, `chey`, `ar`, and other successors is descriptive. Sparse counts and a high number of unique types mean the apparent ranks should not be treated as stable grammatical categories.

## Interpretation
Combined with exp_596, all three forms show Currier-B P0 initial-position enrichment, but their successor distributions were not distinguishable by this exploratory JSD/permutation test. This is compatible with overlapping local contexts; it is not evidence that the forms are synonyms, related morphemes, or have any particular meaning.

## Limitations
- One-token context only; no longer-range or neighboring-line context.
- Permutation assumes successor labels exchangeable between starter groups and does not stratify by folio/section.
- Pairwise tests use 5,000 permutations; the report's null result is not a proof of equality.
- EVA strings are transcription tokens, not confirmed words in a known language. No decipherment claim.

## Next test
Test whether the three initial forms differ in broader local context using a predeclared window of two following tokens and a robust sparse-category treatment (e.g., Jensen–Shannon smoothing or permutation on paired two-token sequences). Because the sample sizes are small and sparse, retain a distinct "other/rare" category and avoid overfitting top-token lists.
