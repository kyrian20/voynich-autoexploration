# exp_596 — Compare daiin with predeclared common-word controls

Does Currier-B P0 `daiin` show a stronger line-initial affinity than other predeclared high-frequency EVA strings? The control list is frozen from the existing exp_589 script: `aiin`, `chedy`, `dain`, `saiin`, and `qokaiin`.

## Protocol
- Corpus variants: ZL3b and ZL3a.
- Filters: exact body locus P0, Currier A/B separately, at least two cleaned tokens per line.
- Null model: draw one uniform token position per line, independently, preserving that line's token inventory and length.
- 5,000 fixed-seed Monte Carlo replicates; report observed first count, inventory/length expectation, enrichment, upper/lower p-values.
- Holm correction across the six terms separately within each transcription/dialect/tail family.
- Compare enrichment and observed first counts across ZL3b/ZL3a; do not pool source versions.

## Decision rule
If `daiin` remains strongly enriched after correction in Currier B across both versions and its enrichment is materially larger than the controls, that supports a relatively distinctive positional profile (not a decipherment). If multiple controls are also enriched, interpret `daiin` as part of a broader positional pattern. A failure to reject for a control does not prove it has no positional preference.
