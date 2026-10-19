# exp_601 — Paired sensitivity of the primary first-position statistic

This experiment measures whether the small ZL3a/ZL3b token differences change the core exp_591/596 statistics, using line IDs to pair the versions rather than treating them as independent samples.

## Protocol
- Parse both IVTFF files, including simple, compound and nonnumeric folio identifiers.
- Filter each transcription independently to Currier B, normalized locus P0, at least two cleaned tokens per line.
- Report full-version token counts, observed first-position counts, line-inventory/length expectations, and enrichment for `daiin` plus the five exp_596 controls.
- Pair exact line IDs; on matched eligible rows, count token-occurrence differences, first-position status changes and changes in total/expected counts for every target.
- Report any eligible lines that appear only in one version. Do not calculate a p-value for the difference between versions: these are paired alternative transcriptions of the same manuscript.
- Token cleanup and locus normalization are explicitly documented in `script.py`; independent parser conformance remains a follow-up.

## Interpretation
If total token counts differ slightly but first-position flags and enrichment remain stable, the main positional result is insensitive to the observed version-specific readings. If first-position status changes appear, their loci and net contribution must be reported. Either outcome concerns transcription sensitivity, not independent replication, meaning, or decipherment.
