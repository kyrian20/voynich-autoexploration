# exp_602 — Independent IVTFF parser/tokenizer audit

This experiment implements a second, differently structured parser to check whether the central Currier-B/P0 first-position statistics depend on a single parser implementation.

## Parser comparison
- Parser A: regex-based record extraction and token cleanup patterned after the exp_600 concordance audit.
- Parser B: stateful delimiter parsing and character-by-character tokenization, separately implemented.
- Both extract line IDs, active folio/Currier metadata, raw/normalized locus codes, paragraph markers, body payloads, and cleaned EVA tokens.
- Compare keys and fields for ZL3b and ZL3a; retain up to 100 mismatch examples per file.
- Recompute the primary six-token Currier-B/P0 statistic using each parser, with the same minimum line length.

## What this can establish
Agreement of the two parsers supports implementation consistency under these declared parsing rules. It does not prove that the cleaned-token conventions or all transcription annotations are authoritative. Discrepancies must be resolved before new linguistic hypotheses.
