# exp_594 — Explicit IVTFF paragraph-start marker audit

**Question:** does line-initial `daiin` behave differently on lines explicitly marked as paragraph beginnings in the checked-in ZL3b IVTFF transcription?

## Format definition
The official IVTFF format defines paragraph boundaries using dedicated in-text comments: `<%>` marks the beginning of a paragraph and must appear at the start of that line; `<$>` marks paragraph end. Paragraph segmentation decisions are made by the transcriber. See the official [IVTFF format specification](https://voynich.nu/software/ivtt/IVTFF_format.pdf), §6.9 (version 2.0.2, 2025-07-08).

## Protocol
- Use all generic P-locus types, preserving Currier A/B separately.
- Capture `<%>` and `<$>` from the raw text before markup cleanup; use same cleaned-token rules as exp_589–593.
- Require at least two clean tokens per line.
- Compare explicit paragraph-start-marked lines with lines lacking the start marker. Because absence may reflect incomplete annotation, call the latter “no-start-marker” rather than definitely “continuation”.
- Compute observed first `daiin`, expected count from each line's own token inventory/length, enrichment, and 5,000 within-line random-position draws.
- Report one-sided upper/lower tails with Holm adjustment within each Currier dialect. Small marker groups below 30 lines are descriptive/omitted from inference.

## Limitations
This is a transcription-annotation sensitivity check, not a semantic test. Different transcription files may mark paragraph divisions differently. A marker association can only describe the chosen transliteration's segmentation, not prove punctuation, grammar, or meaning.
