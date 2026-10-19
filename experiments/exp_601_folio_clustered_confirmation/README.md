# exp_601 — Folio-clustered confirmation of Currier-B/P0 initial `daiin`

## Confirmatory question
Does the previously observed excess of literal EVA `daiin` at the start of Currier-B P0 lines remain robust when uncertainty is summarized by resampling whole folios rather than treating every line as an independent cluster?

## Frozen primary specification
- Corpus: `data/transcriptions/eva_zl3b.txt`; SHA-256 recorded in results.
- Currier class: `$L=B` folio header metadata.
- Locus: exact P0 after removing one leading IVTFF locator character.
- Eligible line: at least two cleaned alphabetic EVA tokens.
- Target: literal token `daiin` as first cleaned token.
- Effect: observed line-initial count divided by the line-inventory expectation, where each line contributes its `daiin` count divided by token length.
- Cluster uncertainty: percentile 95% bootstrap interval resampling folios, 20,000 replicates.
- Conditional randomization: one uniformly sampled token position per eligible line, 20,000 replicates; tests within-line positional exchangeability, separately from cluster uncertainty.
- Random seed: 60120261019.

## Decision rule
Call the effect robust to folio sampling only if the cluster-bootstrap 95% interval excludes 1 and all leave-one-folio-out enrichment ratios exceed 1. Report randomization p-value separately. If these criteria disagree, call the inference mixed.

## Important limitation
This tests a positional statistic, not semantics or decipherment. The conditional null preserves each line's inventory and length but not every linguistic or scribal dependency. ZL3a/ZL3b are related transcriptions, not independent samples.
