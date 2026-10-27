# Guard against IVTFF structural tags hidden behind a continuation slash — 2026-10-27

Status: **CODE CHANGE PROPOSED; remote CI not yet verified** at initial commit. No new EXP, no semantic hypothesis, and no change to any corpus or historical scientific output.

## Bounded defect and falsifiable regression

At base `master` `a192f1b14b282a8e34e2f2aad87e31e7f43612da`, `scripts/audit_ivtff_page_locus_ids.py` counted **every** physical row starting with `/` as a continuation and skipped its content. Thus a damaged page boundary such as `/<f2r>` could be silently ignored: `f1r` stayed active and a later `<f1r.2,@P0>` was accepted without a page mismatch. A damaged locus `/<f1r.2,@P0>` was similarly lost. These are **synthetic adversarial fixtures**, not observed corruptions in the three original transcriptions.

The new guard diagnoses slash-prefixed page tags (including Rosettes, foldout, Unicode digit lookalikes and truncated tags), clears active-page scope, and diagnoses slash-prefixed locus tags. It still counts ordinary slash continuations and inline comments. The guard does not normalize or accept malformed tags as valid.

## Code and test contract

- Implementation: `scripts/audit_ivtff_page_locus_ids.py`.
- Regression fixtures: `tests/test_ivtff_page_locus_ids.py` (five damaged page variants, two damaged locus variants, two ordinary slash controls).
- Test command: `python tests/test_ivtff_page_locus_ids.py`.
- Original-source audit command: `python scripts/audit_ivtff_page_locus_ids.py`.
- CI: `.github/workflows/voynich-check.yml` already runs both commands, so no duplicate workflow is added.
- Input policy: no corpus modifications; no random sampling or seed. Synthetic test strings are embedded in the test source; commit SHA fixes exact bytes. No scientific metrics or p-values are produced.

## Scientific scope and limitations

This closes only a parser *fail-closed* hole. It is not a full IVTFF conformance adjudication, not a reproduction of historical EXP outputs, and not a validated decipherment. Historical results, original transcription bytes, manifest partitions and negative results must remain unchanged. The physical source audit must be inspected before claiming the real corpus passes. The prospective holdout remains scientifically restricted; no semantic confirmatory cycle is authorized by this change.

## Verification record

Record the exact PR head SHA, GitHub Actions run ID, conclusion, job steps and any failure before changing this status to verified. Do not infer CI success from the existence of this document.
