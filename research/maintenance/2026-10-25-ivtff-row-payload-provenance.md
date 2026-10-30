# IVTFF row payload provenance guard — 2026-10-25

**Status:** proposed operational correction on a review branch; no new EXP and no claim of decipherment.

## Reproducible defect and scope

`scripts/ivtff_lossless.py` exposes mutable `Payload` and `Span` dataclasses. The additive `tokens_rows` adapter previously checked only the object type and CR/LF in `payload.raw`, then passed the original spans and diagnostics to `tokens()`. Consequently a caller could accidentally supply a payload whose `raw` had changed after lexing, whose spans had been modified, or whose diagnostics had been lost. The projected tokens could then differ from the claimed source row, or unresolved input could be silently truncated. This is a synthetic integrity defect, **not evidence that any archived manuscript run was affected**.

The regression fixtures exercise (a) a stale `raw` value, (b) an altered `Span.raw`, (c) a cleared diagnostic from an unclosed alternative, and (d) a non-text raw value. Both `tokens_rows` and `tokens_scoped_rows` must reject the first three; the unscoped adapter rejects the fourth.

## Repair

Before projecting a physical row, `tokens_rows` now re-lexes its exact raw text using the unchanged `lex()` and requires the original span tree and diagnostics to match the recomputed values. It also retains the CR/LF guard. This adds a linear re-lex cost per physical row; no caching or experimental output was changed. The frozen historical `tokens()` API and callers bypassing this adapter are **not** protected by this fix.

## Verification contract

- Exact command: `python tests/test_ivtff_lossless.py`.
- CI: `Voynich Check` on the exact PR head, then a separate push run on the merge SHA if integrated.
- Fixtures are synthetic and deterministic: no random seeds, corpus files or holdout leaves are read.
- Original transcriptions, historical results, scripts, source hashes, snapshots, and EXP identifiers are untouched.
- Before a passing run is inspected, the correction is **proposed**, not CI-verified.
- This does not adjudicate the full IVTFF specification or validate any semantic interpretation.

## Next work

Inventory consumers that still call the frozen `tokens()` directly; do not rewrite them without checking their archived input/script hashes. Continue independent parser conformance and corpus provenance adjudication before any confirmatory held-out test.
