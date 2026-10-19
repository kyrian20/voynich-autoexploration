# exp_599 — Results: marginal successor distributions at offsets +1 and +2

**Execution date:** 2026-10-19  
**Workflow:** https://github.com/kyrian20/voynich-autoexploration/actions/runs/39258941188  
**Machine-readable output:** `results.json`

## Question
After excluding exp_598's uninformative joint-pair collapse, do the marginal token distributions at the first and second successor positions differ after initial `daiin`, `dain`, or `saiin`?

## Sample
Both ZL3b and ZL3a yielded the same 169 eligible Currier-B P0 starter lines: 89 `daiin`, 34 `dain`, and 46 `saiin`. The filter requires at least three cleaned tokens, so offsets +1 and +2 use exactly the same lines.

## Main tests

| Token offset | Pair | JSD (bits) | Mean null JSD | Raw p | Holm-adjusted p |
|---|---|---:|---:|---:|---:|
| +1 | `daiin` vs `dain` | 0.682 | 0.710 | 0.733 | 1.000 |
| +1 | `daiin` vs `saiin` | 0.632 | 0.690 | 0.946 | 1.000 |
| +1 | `dain` vs `saiin` | 0.655 | 0.706 | 0.865 | 1.000 |
| +2 | `daiin` vs `dain` | 0.814 | 0.828 | 0.643 | 1.000 |
| +2 | `daiin` vs `saiin` | 0.768 | 0.777 | 0.602 | 1.000 |
| +2 | `dain` vs `saiin` | 0.843 | 0.872 | 0.842 | 1.000 |

Each p-value is from 5,000 pooled-label permutations, and Holm correction is applied across all six planned pairwise tests per transcription. ZL3a values repeat the same observed JSDs to six decimals; adjusted p-values are likewise 1.0 across all six comparisons.

## Descriptive context
At offset +1, the most frequent successors include `shey` (6/89 after `daiin`, 4/46 after `saiin`) and `chey` (4/89 after `daiin`, 4/34 after `dain`). The second successor position is even more diverse: 74 unique tokens in 89 `daiin` contexts, 33 in 34 `dain` contexts, and 41 in 46 `saiin` contexts. The data are sparse relative to the number of possible token types.

## Conclusion
No pair of starter forms has a successor-token distribution that is unusually distinct under this test at either offset. This is a **non-significant result**, not proof that the contexts are equivalent. The empirical successor distributions are highly diverse, and the sample sizes—especially for `dain`—are modest.

The same result in both transcription versions is best treated as **transcription-version robustness**, not two independent samples: these files have the same eligible line and starter counts, with very similar underlying transcription data.

## Link to exp_598
Exp_598 tested joint two-token pairs but collapsed 97.1%–100% of contexts into one rare-pair bucket. Its joint-pair inference is marked **uninformative due to sparsity**, and is not evidence for context equivalence. Exp_599 keeps each successor position marginal and avoids this collapse.

## Limitations
- The permutation null does not stratify by folio or section.
- Sparse token distributions lower power; nonsignificance does not establish equivalence.
- EVA strings are transcription tokens; no semantics, synonymy, or decipherment is inferred.

## Next step
Pause the expanding `daiin` positional family and consolidate the analyses in a cross-experiment synthesis: distinguish replicated observations, annotation-sensitive findings, negative results, and experiments that were methodologically uninformative. Identify what evidence would be needed before moving from positional distribution to any linguistic hypothesis.
