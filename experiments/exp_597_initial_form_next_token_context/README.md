# exp_597 — Next-token context after initial daiin/dain/saiin

After exp_596 found strong Currier-B P0 line-initial enrichment for `daiin`, `dain`, and `saiin`, this experiment compares the token immediately following each line-initial form.

## Protocol
- Transcriptions: ZL3b and ZL3a; Currier B, exact locus P0, lines with at least two cleaned tokens.
- Groups: lines whose first token equals `daiin`, `dain`, or `saiin`; the context token is the second token.
- Report top successor tokens and Shannon entropy for each group.
- Primary comparisons: pairwise Jensen–Shannon divergence (bits) for daiin-vs-dain, daiin-vs-saiin, and dain-vs-saiin.
- Permutation null: shuffle pooled successor labels between each pair while preserving group sizes; 5,000 draws, fixed seeds; Holm correction across three comparisons in each transcription.
- The comparison with all other line starters is descriptive only and is not in the corrected primary family.

## Limitations
The null assumes successor tokens are exchangeable across the two starter groups and does not stratify by folio. A significant difference would establish a distributional difference only; nonsignificance does not prove equivalence. No semantic interpretation or decipherment is claimed.
