# exp_600 — ZL3b/ZL3a transcription concordance audit

**Goal:** quantify how independent (or closely aligned) the two EVA transcription files are for line-level analyses. Prior experiment reports treat agreement between versions as robustness; it must not be described as independent-sample replication.

## Matching and extraction
- Match text records by exact IVTFF identifier before the comma (e.g. `f1r.22`).
- Preserve raw locus/locator codes for comparison; do not discard a locus mismatch.
- Record Currier A/B from the folio header `$L=` field.
- Compare raw payload equality and cleaned token-sequence equality separately.
- Token cleanup: remove comments/markup, keep the first `[a:b]` alternative, remove uncertain `{...}` spans and `@NNN` glyph codes, split on period/comma/whitespace, and keep ASCII-letter tokens. This is a declared comparison parser, not an authoritative interpretation of all IVTFF constructs.
- Report unmatched keys, duplicate keys, marker differences, raw locator disagreements, token-difference counts and example lines.

## Interpretation rules
- Equal cleaned tokens do not mean identical annotation or transcription conventions.
- Different cleaned tokens show where alternative readings can affect downstream counts.
- ZL3a/ZL3b are transcriptions of the same manuscript, not independent corpora.
- No semantic/decipherment interpretation follows from line concordance.
