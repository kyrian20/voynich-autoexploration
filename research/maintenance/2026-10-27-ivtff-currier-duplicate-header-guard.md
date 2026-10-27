# IVTFF Currier metadata: repeated folio header guard — 2026-10-27

**Scope:** bounded operational defect in `scripts/audit_ivtff_metadata.py`, not a new EXP or a decipherment result. Based on `master` `03a069ff3818440510c28d8a597353e3146cf306`. CI and post-merge status must be checked at the exact corresponding SHAs.

## Defect and falsifiable regression

The existing Currier metadata audit stored `pages[folio] = lang` without checking whether the same physical folio header had already occurred. A duplicate `<f1r>` header with a later contradictory `$L=B` silently replaced an earlier `$L=A`; repeated headers without `$L` were also silently counted. Thus the reported A/B counts depended on source order rather than a unique mapping of physical pages.

The repair adds `collect_folio_languages(text)`, which rejects any repeated header before assigning Currier metadata and returns the page count from the same pass. The CLI uses that helper. It does **not** infer Currier from `$Q` or `$I`, change the existing treatment of unknown `$L`, or assert full IVTFF conformance.

The regression in `tests/test_ivtff_metadata.py` exercises identical and conflicting duplicate `$L` values, missing-first-language headers, a numbered panel (`f67r1`) and the named Rosettes page (`fRos`). A unique three-header control must pass. The archived ZL3b source must still contain exactly 227 distinct headers. The CI already executes this test file under the step **IVTFF metadata**; no workflow mutation or new job is needed.

## Input provenance and preservation

- Source: `data/transcriptions/eva_zl3b.txt`; previously archived SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`. This value is a historical provenance claim, not a newly computed hash in this change.
- Repository read of the current source before editing: 8,511 physical rows; 227 header matches, 227 distinct IDs, **zero repeated headers** under the metadata auditor's existing header regex. IT2a had 225 matches, 225 distinct IDs; it is not read by this CLI.
- The existing `master` run [40486187317](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40486187317) was observed as completed/success for its check job before creating the branch. That run does not certify this change.
- No original transcription, manifest, experimental output, seed, model parameter, frozen negative result or committed claim is edited.

## Reproduction and acceptance

```sh
python tests/test_ivtff_metadata.py
python scripts/audit_ivtff_metadata.py
python tests/test_ivtff_lossless.py
python scripts/check_corpus_integrity.py
```

The first command must reject the synthetic duplicate headers and accept the unchanged archived census. A clean CI run on the PR head and a separate successful run on the merged `master` SHA are required before marking the repair integrated. Preserve failures and logs; do not call a failed run successful.

## Limits

This is a preventive guard, **not evidence that the original ZL3b source contained duplicate folio headers**. The metadata regex is not a complete IVTFF parser; missing/malformed headers, ambiguous alternative glyphs, external corpus provenance and independent semantic anchors remain open. The reserved-leaf split is historically exposed; no test-folio evaluation or semantic hypothesis is performed. No experiment ID, RNG seed or p-value applies to these deterministic adversarial fixtures.
