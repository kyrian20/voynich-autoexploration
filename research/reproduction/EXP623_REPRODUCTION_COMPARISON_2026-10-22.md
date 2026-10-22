# EXP-623 pilot reproduction comparison — 2026-10-22

## Scope and provenance

The two Library EXP-623 word-order pilots were reproduced in GitHub Actions against the exact transcription blobs recorded by the pilots. This is a reproduction of two distinct exploratory protocols, not a new experiment ID and not a decipherment test.

- Reproduction workflow run: [39729111827](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39729111827)
- Workflow commit: `40e636cd7815f0b2de5d10d5ea6b7a47f1ad645d`
- Immutable Actions artifact: `exp623-reproduction-40e636cd7815f0b2de5d10d5ea6b7a47f1ad645d` (artifact ID 12404740024; SHA-256 of ZIP: `12a286d6cd47646957f52966621a1036e46187c7c2452a63f47e6203e34c56eb`)
- Source transcription Git blobs verified by the workflow:
  - ZL3b `data/transcriptions/eva_zl3b.txt`: `2a4533ab9bdfa85db9bad602d590978953055df1`, 411,671 bytes.
  - IT2a `data/transcriptions/eva_it2a.txt`: `4d6d3f2537b1f507a257529b49c94af7d6e03446`, 342,104 bytes.
- Both reproduction scripts compiled and both analysis steps completed successfully. Outputs are retained as the run artifact, separate from historical pilot JSON.

## Comparison A — endpoint-preserving interior shuffle

Script: `research/reproduction/exp623_order_null.py`. Ten folio-stratified 70/30 splits, 39 null permutations per split; each locus keeps its first and last token, length, token multiset, and folio assignment, while interior positions are shuffled. The model is refit for each shuffled training/test corpus.

| Metric | ZL3b pilot | ZL3b reproduced | IT2a pilot | IT2a reproduced |
|---|---:|---:|---:|---:|
| Eligible P0 loci | 3,879 | 3,879 | 3,881 | 3,881 |
| Clean tokens | 32,959 | 32,959 | 33,380 | 33,380 |
| Mean observed-minus-null gain (bits/token) | 0.05416632725281336 | 0.054166327252813375 | 0.045747563548623846 | 0.045747563548623874 |
| Median gain | 0.05419924778424624 | 0.05419924778424623 | 0.04640161866417089 | 0.04640161866417089 |
| Positive splits | 10/10 | 10/10 | 10/10 | 10/10 |
| Observed above null 95th percentile | 10/10 | 10/10 | 10/10 | 10/10 |
| Observed above every null draw | 10/10 | 10/10 | 10/10 | 10/10 |

Differences are only floating-point rounding at approximately machine precision; counts and split-level categorical outcomes agree. Under this particular model and endpoint-preserving null, observed word order yields greater held-out predictive gain than the shuffled interiors in all ten overlapping sensitivity splits.

## Comparison B — all-token within-locus shuffle

Script: `research/reproduction/exp623_shuffle_holdout.py`. Twenty 70/30 folio-level splits and 50 test shuffles per split. This protocol scores shuffled test sequences using a model trained on the original training sequence; it is not the same null or refitting procedure as Comparison A.

| Metric | ZL3b pilot | ZL3b reproduced | IT2a pilot | IT2a reproduced |
|---|---:|---:|---:|---:|
| Loci | 5,376 | 5,376 | 5,207 | 5,207 |
| Tokens | 39,298 | 39,298 | 37,945 | 37,945 |
| Mean shuffled-minus-original loss (bits/token) | -0.0068360668085217565 | -0.006836066808522201 | -0.019098027742836622 | -0.01909802774283529 |
| Splits where original loss is lower | 3/20 | 3/20 | 0/20 | 0/20 |
| Fraction of random shuffles with lower loss than original | 0.769 | 0.769 | 0.988 | 0.988 |

Counts and categorical outcomes match exactly; the mean-loss differences are around (10^{-15}) bits/token, consistent with floating-point rounding. For this alternative test, random shuffles often have lower test loss than the original sequence. This is a real protocol-dependent contrast, not something to average away or call a direct replication of Comparison A.

## Interpretation and limits

1. **Execution provenance is now closed for these two scripts:** the exact recorded source blobs were verified, both scripts ran in Actions, and the reproduced summary metrics match the saved pilot values within floating-point rounding.
2. **The two null models are not interchangeable.** Comparison A refits the model on shuffled corpora and preserves endpoints; Comparison B shuffles test sequences against a model trained on original data. Their differing outcomes are expected to require separate interpretation.
3. Ten overlapping splits in Comparison A are descriptive robustness checks, not ten independent replications. ZL3b and IT2a are alternate transcriptions of the same manuscript, not independent manuscripts.
4. These results concern predictive behavior under specified tokenization/model/null choices. They do not identify a generating mechanism, prove natural language, reveal semantics, or decipher the manuscript.
5. The reproduced JSON files are retained in the Actions artifact, not committed as canonical scientific results. The historical Library originals were not overwritten, renamed, merged, or deleted.

## Output integrity

SHA-256 of the JSON files extracted from the immutable Actions artifact:

- `exp623_order_null_reproduced.json`: `1f991a79a5d3fe6a2dbcf5d689327031580341b3943de2f2d15a66b4193c2051`
- `exp623_shuffle_holdout_reproduced.json`: `7397660f9df7a5a5e048e1ce2aa382ce76b9517e88f993e1ded0b94a306a12b0`

## Remaining work

This closes only the execution/reproduction gap for the two Library EXP-623 pilots. It does not close full Library↔GitHub byte-level reconciliation, the seven internal duplicate GitHub experiment-folder IDs, or the independent IVTFF parser audit.
