# exp_598 — Two-token successor context

This extends exp_597's single-successor analysis to the next two EVA tokens after line-initial `daiin`, `dain`, and `saiin`.

## Predeclared protocol
- Transcriptions: ZL3b and ZL3a; Currier B, exact IVTFF locus P0, at least three cleaned tokens per line.
- Context: ordered pair of the second and third cleaned tokens.
- Rare-pair rule: count ordered pairs across the pooled three starter groups; if a pair occurs only once, replace it with a shared `<RARE_PAIR>` category. The threshold is fixed at pooled count <2 before looking at results.
- Metric: Jensen–Shannon divergence in bits for each of three pairwise starter-group comparisons.
- Null: shuffle the pooled context-pair labels between groups while preserving sample sizes; 5,000 draws; Holm correction across the three pairs within each transcription.
- Report raw and collapsed pair counts, fraction collapsed, entropy, top contexts, both source-file SHA-256 hashes, and results.

## Interpretation
A significant difference would mean the two-token successor distributions differ under this sampling null. A nonsignificant result is not proof of equivalence. These are literal EVA context strings, not translated words. No semantic or decipherment conclusion follows.
