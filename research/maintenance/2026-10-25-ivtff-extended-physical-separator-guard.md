# IVTFF: physical line separators beyond CR/LF — 2026-10-25

**Type:** bounded integrity repair, no new EXP, no new semantic claim. **Status:** proposed until branch CI is verified.

## Reproducible defect in the previous adapter

At `master` commit `bb1ca922a93cd9641a0cfeae3a00dce057695502`, `scripts/ivtff_rows.py` rejects only CR and LF inside a physical-row `Payload.raw`. Python's `str.splitlines()`, used by the project's corpus readers, also recognizes VT (U+000B), FF (U+000C), U+001C–U+001E, NEL (U+0085), line separator (U+2028) and paragraph separator (U+2029). The frozen lexer may consume such a character inside an angle-bracket comment, or classify it as layout whitespace, without a physical-newline diagnostic. A row adapter can therefore project text that the upstream reader would treat as multiple physical lines. This is a synthetic interface inconsistency; it is **not** evidence that any historical corpus contains these characters.

## Repair and regression

- `scripts/ivtff_rows.py`: reject all ten individual physical separator characters recognized by Python `splitlines()` before projecting a row. CRLF is also covered. Preserve the frozen `scripts/ivtff_lossless.py` byte-for-byte.
- `tests/test_ivtff_lossless.py`: exercise eleven separator forms (including CRLF), both hidden inside an inline comment and visible between glyphs: 22 negative fixtures. Each must be recognized by `splitlines()` and rejected by both `tokens_rows` and `tokens_scoped_rows`.
- Test command: `python tests/test_ivtff_lossless.py`. GitHub gate: `Voynich Check` on the exact PR head, followed by a separate push run on the merge commit if merged.
- No random seeds or statistical tests: fixtures are deterministic strings. No manuscript source, historical script, output, holdout split, or committed claim is changed.

## Limits

This is a **row-projection guard**, not independent IVTFF conformance certification. The original single-row `tokens()` API remains frozen and unprotected; downstream callers bypassing the adapter are not audited by this patch. Source/folio IDs supplied to the scoped adapter are still caller assertions, not authenticated provenance. No claim of translation or global integrity is made.

## Next action

Confirm exact-head CI and inspect the diff; merge only after success, then check the resulting `master` SHA and push CI. Continue normative IVTFF adjudication and the historical corpus-identity inventory without repeating archived scientific experiments.
