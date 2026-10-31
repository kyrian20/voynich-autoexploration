# IVTFF: closed but invalid inline metadata tags — 2026-10-29

**Scope:** technical repair of the independent line-boundary reader in draft PR #138. No new EXP ID, no new predictive run, no prospective held-out leaves inspected, no translation claim. This document is a linked correction, not a replacement for frozen `results.json`.

## Falsifiable defect and correction

The parser recognizes valid single-character IVTFF inline metadata tags such as `<@H=2>` and removes them at zero width. Previously, a closed but malformed tag such as `<@H=22>` failed that match, then fell through to the generic `<...>` drawing-gap substitution. As a result, `ab<@H=22>cd` became two apparently certain words `ab` and `cd`, potentially forging a within-line negative candidate or a line-boundary positive. This contradicted the code comment that malformed metadata is not silently erased.

The patch detects residual closed `<@...>` tags **after** removing well-formed zero-width metadata and free-text comments, but **before** generic tag substitution. Such a row is quarantined as a single `None` sentinel for candidate construction (or omitted in the token-only API). Valid single-character metadata remains zero width. Unclosed markup retains its earlier fail-closed path. This is conservative: malformed metadata is not guessed to be a word separator or an intended valid tag.

## Frozen-input scope and non-reproduction

Original source identities, unchanged:

- ZL3b: `data/transcriptions/eva_zl3b.txt`, SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- IT2a: `data/transcriptions/eva_it2a.txt`, SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.

Read-only inspection of the versioned files via GitHub before patch publication found **two valid inline `<@H=n>` tagged P records in each transcription and zero malformed closed `<@...>` tags** in those records. The new automated test repeats the SHA-locked admission and tag check on all **4,130** ZL3b and **4,118** IT2a P rows. This defect therefore has **no observed impact in the currently admitted P-row populations**; it is not evidence of improved predictive performance. Other forms of IVTFF uncertainty and historical modeling discrepancies remain unresolved.

## Regression and commands

New `tests/test_line_boundary_invalid_inline_tags.py` covers:

1. Valid single-character metadata and free comments retain zero-width semantics.
2. Five malformed closed metadata forms are rejected under both reading policies, including the previous `ab<@L=AB>cd` false split.
3. A malformed tag quarantines the complete row, not merely the tag.
4. The quarantined row cannot forge a cross-row positive while valid neighboring rows retain their within-line negative.
5. Read-only source scope checks exact SHA-256, admitted P-row counts and valid/malformed metadata tags.

Commands: `python -m unittest discover -s tests -p 'test_line_boundary_invalid_inline_tags.py' -v` and `python -O -m unittest discover -s tests -p 'test_line_boundary_invalid_inline_tags.py' -v`. Both are wired into `.github/workflows/voynich-check.yml`. These are deterministic fixtures and source counts; no random seed is used, no model is fit, and no historical artifact is overwritten. Verify the exact PR-head CI and its logs before declaring these commands successful.

## Integrity disposition

**Defect:** repaired in proposed code, subject to CI verification and integration into PR #138. **Historical scores:** unchanged and still `INVALID_FOR_CLAIM` as outputs of the *corrected* reader because of previously documented real candidate-population and probability-model defects; no new retraction is attributed to this zero-impact malformed-tag subset. **Global IVTFF compliance:** not established. **Next:** prioritize an independently adjudicated reader/physical-page continuity contract before re-running metrics, and do not conflate successful unit tests with scientific validation.
