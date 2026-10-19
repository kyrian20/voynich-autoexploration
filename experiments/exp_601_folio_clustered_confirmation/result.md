# exp_601 — Folio-clustered confirmation results

**Workflow:** https://github.com/kyrian20/voynich-autoexploration/actions/runs/39259869279  
**Machine-readable output:** `results.json`  
**Source SHA-256:** `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`

## Result

Frozen primary test: Currier B, P0, at least two cleaned EVA tokens, first token exactly `daiin`.

- Eligible lines: 2325
- Represented folios: 81
- Observed initial hits: 88
- Within-line inventory expectation: 31.279224
- Enrichment ratio: **2.813369×**
- Folio-cluster bootstrap 95% percentile interval: **2.115596–3.59317×** (20,000 folio resamples)
- Conditional within-line randomization: mean 31.30515; one-sided Monte Carlo p=0.00005 (20,000 replicates)
- Leave-one-folio-out enrichment range: **2.640358–2.930637×**.

## Interpretation

The preregistered decision rule is met: the cluster-bootstrap interval is entirely above 1 and every leave-one-folio-out estimate remains above 1. The positional excess is therefore robust to resampling the represented folios under this specification.

The randomization p-value addresses a different null: uniform token position conditional on each line's observed inventory and length. It should not be read as a test of natural language or as a semantic result.

## Limitations

- Cluster bootstrap quantifies folio-sampling sensitivity; it does not prove folios are identically distributed.
- The conditional randomization does not model all dependencies in the manuscript.
- ZL3a and ZL3b are related transcriptions, not independent samples.
- `daiin` is not unique in line-initial enrichment: earlier controls found `dain` and `saiin` enrichments too.
- This confirms a positional statistic only. It does not establish meaning, grammar, language family, or decipherment.

## Next decision

Do not extend the family with more hand-picked word tests. The next high-value step is a held-out prediction experiment: fit a simple positional model on a preregistered subset of folios and evaluate it on untouched folios, with negative controls and a baseline that preserves each line's token inventory.
