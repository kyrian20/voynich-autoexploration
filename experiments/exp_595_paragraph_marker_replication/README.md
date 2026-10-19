# exp_595 — Replicate paragraph-marker findings in ZL3a

This experiment repeats the explicit IVTFF paragraph-start marker analysis (exp_594) in both checked-in EVA transcriptions, ZL3b and ZL3a, with the same parser and thresholds.

## Protocol
- Paragraph start is identified only by `<%>` at the beginning of the raw transliterated line; paragraph end by `<$>` at the end.
- Generic P-locus rows, separate Currier A/B, at least two cleaned tokens per line.
- Each transcription receives 5,000 within-line random-position draws per eligible category and Holm correction for upper/lower tails within dialect.
- Reports bytes, SHA-256, counts, marker coverage, and enrichment differences between versions.
- A row without `<%>` is termed `no_start_marker`; it is not assumed to be a continuation because marker coverage can be incomplete.

Official format reference: https://voynich.nu/software/ivtt/IVTFF_format.pdf, §6.9.

## Decision rule
Treat the exp_594 pattern as replicated only if direction and material effect size agree across both versions and the marker counts/coverage are comparable. If they differ, report transcription sensitivity and do not pool counts or claim a general paragraph-level rule.
