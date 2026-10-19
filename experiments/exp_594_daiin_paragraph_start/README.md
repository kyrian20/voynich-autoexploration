# exp_594 — Actual paragraph-opening marker audit

Question: within the checked-in ZL3b transcription, does line-initial `daiin` differ between lines carrying the literal IVTFF `<%>` paragraph-start marker and other P0 body lines?

The script records `<%>` from the raw line body **before** token cleaning. It does not use `@`, `+`, or `*` as paragraph proxies. IVTFF describes `<%>` as paragraph start and `<$>` as paragraph end (format §6.9).

Primary reporting:
- counts, target-token frequency, observed initial hits, within-line expected hits, enrichment, upper/lower-tail Monte Carlo p-values within Currier A and B;
- direct difference between Currier-B paragraph-start and continuation initial-token rates, with a permutation test preserving group sizes;
- source SHA-256 and marker counts.

Limitations: marker placement is a transcription decision; only ZL3b is tested; line inventory/length null does not model all layout or paragraph dependencies; findings do not reveal word meaning.
