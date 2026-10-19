# exp_599 — Marginal successor distributions at offsets +1 and +2

This corrective follow-up avoids exp_598's uninformative joint-pair collapse, which pooled nearly every context into one rare category.

## Protocol
- Sources: ZL3b and ZL3a.
- Filter: Currier B, exact IVTFF locus P0, at least three cleaned tokens per line, and line starter equal to `daiin`, `dain`, or `saiin`.
- Use the same line set for both successor positions: offset +1 (immediate next token) and offset +2 (the token after that).
- Analyze each offset as a **marginal** token distribution; do not collapse rare tokens.
- For each offset, compare each of the three starter pairs using Jensen–Shannon divergence and 5,000 pooled-successor-label permutations, preserving group sizes.
- Holm correction across the six predeclared comparisons (three starter pairs x two offsets) within each transcription.
- Record source hashes, sample sizes, entropy, top tokens, null means, raw and adjusted p-values.

## Interpretation
This measures whether the observed successor-token distributions differ beyond the sample-size-driven divergence under the permutation null. Nonsignificance does not prove equality, and any difference would not establish semantics. Results use literal EVA tokens and are not a decipherment.
