# exp_593 — daiin and IVTFF line metadata

This is a cautious follow-up to exp_589–592. It asks whether the line-initial `daiin` effect varies across explicit IVTFF prefix modifier categories, within Currier A/B and P0 only.

**Important:** the modifier symbols `@`, `+`, `*`, and absence of a modifier are preserved as metadata categories. Without a verified specification for this exact transcription version, we do not relabel them “paragraph-start” or “continuation”. This test is therefore a metadata-stratified sensitivity analysis, not an assertion about paragraph-opening semantics.

- Corpus: ZL3b IVTFF, source digest recorded in `results.json`.
- Filters: Currier A/B separately, locus P0, lines with at least two cleaned tokens.
- Statistics: observed first `daiin`, line-composition expectation, enrichment, 5,000 Monte Carlo position draws, one-sided p-value, Holm correction within A and B category families.
- Minimum stratum size: 50 lines; smaller modifier/locus subtypes are omitted from inference, not declared null.
- No paid API required. Every category and result is retained for interpretation after execution.
