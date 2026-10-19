# exp_596 — ZL3a/ZL3b line-level annotation audit

Before treating exp_595 as robustness, compare the two local transcriptions directly.

- Match rows by folio header and complete IVTFF locus identifier.
- Report unmatched and duplicate keys rather than silently forcing alignment.
- Count token-sequence, paragraph-marker, Currier-label, and line-initial `daiin` status disagreements.
- Save source byte sizes and SHA-256 digests plus a bounded sample of disagreement rows.
- Recompute descriptive `daiin` enrichment for the same paragraph-marker strata.

This is a version-comparison audit, not independent replication. Tokenizer differences can reflect transcription conventions as well as lexical readings. No semantic claim is made.
