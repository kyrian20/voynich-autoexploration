# IVTFF physical-row scope guard — 2026-10-25

**Status:** proposed operational guard; no scientific experiment, no new EXP ID.

## Concrete risk and falsifiable regression

The existing additive `tokens_rows([Payload, ...])` has no source or folio metadata. It correctly joins `lex("a/")` followed by `lex("/b")` to `["ab"]` but cannot distinguish a legitimate continuation from a cross-folio or cross-transcription pair. A caller that inadvertently concatenates ZL3b and IT2a rows, or f1r and f1v rows, could silently create a fictitious word. The pre-existing API is intentionally preserved because historical users may depend on its exact behavior.

## Implemented safeguard

`scripts/ivtff_rows.py::tokens_scoped_rows` accepts tuples `(source_id, folio_id, lexed_payload)`. It splits processing into contiguous scope blocks and delegates each block to the unchanged `tokens_rows`. Thus an unfinished continuation at a scope boundary raises `ValueError` rather than joining two different sources or folios. A repeated non-contiguous scope is also rejected to flag unordered or interleaved input. Empty/missing IDs, non-Payload inputs, and invalid policy values are rejected.

The existing `tests/test_ivtff_lossless.py` (already called by the canonical CI workflow) now checks valid within-folio joins, independent rows across folios and sources, both cross-boundary slash cases, noncontiguous repeated scopes, invalid IDs, non-Payload input, and invalid empty-input policies. These are synthetic adversarial fixtures, not manuscript measurements.

## Preservation and limitations

No original transcriptions, existing tokenizer, historical results, experiment snapshots, seeds, or holdout manifests are changed. The new labels are supplied by the caller: they are **not independently authenticated**, do not validate IVTFF page metadata or the source SHA-256, and do not enforce whether a folio is eligible for a held-out partition. The guard is not a replacement for independent IVTFF 2.0.2 conformance tests. It prevents a specific boundary error only for consumers that explicitly call the new API.

## Verification gate

A passing `Voynich Check` on the exact PR head is required before this change can be described as tested in CI; a subsequent passing push run on the merge commit is required for post-merge validation. Until then, status is **PROPOSED**.
