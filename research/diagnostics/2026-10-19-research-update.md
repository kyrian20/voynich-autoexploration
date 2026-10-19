# Research update — 2026-10-19

## Canonical pointers
- Current state: `state/current_state.md` (updated through exp_599; latest verified write commit is expected to be checked after this update).
- Synthesis: `research/synthesis/2026-10-19-daiin-position-synthesis.md`.
- Historical checkpoint: `state/working_position.md` is explicitly marked as an archived April 2026 snapshot and does not reflect work after exp_579.

## API workflow
The scheduled LLM agent workflow failed with HTTP 429 because the OpenAI API has no funds available, as reported by the maintainer. It was not retried. Corpus experiments exp_589–599 ran with standard Python in GitHub Actions and required no OpenAI API credit.

## Research through exp_599
Experiments exp_589–599 each have protocol/code, results JSON, a result report and a run link (see the synthesis). The key result is a Currier-B/P0 initial-position excess for literal EVA `daiin`; this is robust to the tested transcription versions and folio omission, but is not unique because `dain` and `saiin` show stronger initial enrichment under the same test.

Exp_594–595 found paragraph-marker associations in the transcriptions; these are annotation-sensitive because IVTFF paragraph segmentation is a transcriber decision. Exp_597 and exp_599 did not distinguish successor-context distributions; this is not proof of equivalence. Exp_598's joint pair analysis is specifically marked uninformative because its rare-pair collapse removed nearly all context information.

## Next work
Prioritize an independent IVTFF parser/provenance and paired ZL3a/ZL3b concordance audit before further hypotheses or lexical interpretations. Keep the API-based LLM workflow disabled until the maintainer chooses to fund the API.
