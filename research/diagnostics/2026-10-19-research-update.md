# Research update — 2026-10-19

## Current authoritative files
- Current state: `state/current_state.md`.
- Synthesis: `research/synthesis/2026-10-19-daiin-position-synthesis.md`.
- Historical checkpoint: `state/working_position.md` is marked as an archived April 2026 snapshot.

## Repository work through exp_601
- exp_589–599 record the daiin position/context investigation, including a non-significant successor test and exp_598's explicitly uninformative rare-pair collapse.
- exp_600 aligns ZL3a/ZL3b by IVTFF line identifiers: 5,385 matched rows, 49 (0.91%) differing cleaned token sequences, four IDs only in ZL3a, no duplicate/skipped keys after compound/Rosettes IDs were included.
- exp_601 pairs the exact B/P0 line records across both versions and compares counts/initial-position statistics for daiin and common-word controls. See its result report and JSON before using its values.
- These files are alternative transcriptions of one manuscript, not independent corpora.

## API workflow
The separate OpenAI-API LLM workflow returned HTTP 429 because API funds were unavailable, as reported by the maintainer; it has not been retried. The corpus analysis workflows use Python/GitHub Actions and require no OpenAI API credit.

## Next priority
Independent parser conformance review against the IVTFF specification: validate folio headers, compound page IDs, text locus IDs, locator parsing, Currier labels, and token cleanup against a separately implemented extractor. Do not add more lexical hypotheses until this audit is documented.
