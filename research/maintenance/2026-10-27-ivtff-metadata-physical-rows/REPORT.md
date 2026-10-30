# IVTFF physical-row metadata preflight — 2026-10-27

**Status:** proposed repair pending remote CI verification. No new EXP.

## Reproducible defect and boundary

At base commit `176f5479ed3a60d8ba0c9bd2637eaab39670fcbb`, the two additive metadata audits
`scripts/audit_ivtff_metadata_strict.py` and
`scripts/audit_ivtff_unique_page_headers.py` iterate over
`str.splitlines()`. Python treats VT, FF, FS, GS, RS, NEL, U+2028 and U+2029 as
line boundaries, whereas these are not physical IVTFF CR/LF/CRLF row delimiters.
A crafted row such as `<!editor<U+2028><f2r> <! $L=B>` was therefore
interpreted as a second folio header by those audits. This is a parser
preflight defect, **not evidence that the frozen transcription contains it**.
The independent structural auditor already rejects these separators, but
the other metadata gates must not silently reinterpret them.

## Change

Introduce `scripts/ivtff_physical_rows.py` with a strict iterator: normalize
CRLF and CR into LF for record enumeration, reject the eight nonphysical
separators with original physical line number and Unicode codepoint, and
never turn a contaminated comment into a valid header. Route both additive
metadata audits through this iterator. Preserve
`scripts/audit_ivtff_metadata.py` unchanged because archived EXP-173
depends on its frozen SHA-256.

Extend both existing test modules with eight adversarial separator cases
and positive CR/LF/CRLF controls. Their test modules are already invoked by
the canonical `.github/workflows/voynich-check.yml`; no duplicate CI
workflow or new scientific experiment is required.

## Verification plan

- `python tests/test_ivtff_metadata_strict.py`
- `python -m unittest discover -s tests -p 'test_ivtff_unique_page_headers.py' -v`
- `python scripts/audit_ivtff_metadata_strict.py`
- `python scripts/audit_ivtff_unique_page_headers.py`
- Canonical `Voynich Check` on the PR head; check each run's SHA, jobs,
  result and artifacts before merging.
- After merge, verify fresh `master` CI for the merge SHA.

## Scientific and archival limits

No corpus, historical script, EXP result, negative outcome, seed, reserved
folio assignment or committed claim is changed. No language meaning is
inferred. This gate does not establish full IVTFF 2.0.2 conformity or
historical reproducibility; independent adjudication and corpus provenance
remain open. The initial observation is a synthetic adversarial case,
not a detected source-file corruption.
