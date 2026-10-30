# IVTFF — unclosed primary containers can hide high-ASCII codes

**Date:** 2026-10-31. **Status:** proposed software-integrity correction; do not declare reproduced until exact branch CI, logs, and evidence artifacts have been checked. **Scope:** two read-only derived censuses, not historical EXP-590, no new EXP or scientific inference.

## Concrete defect and falsifiable acceptance

The lossless IVTFF lexer represents an unterminated primary `{ligature`, `[alternative`, or `<!comment` as an `unresolved` span containing the remaining raw characters. The two downstream high-ASCII censuses previously rejected malformed `@12;` only when the lexer emitted a standalone unresolved `@` span. They did **not** reject an unresolved container that swallowed a valid-looking `@140;`. Thus `<f1r.1,@P0> {c@140;h` could silently be counted as **zero** selected codes. This is a reproducible code-path defect on a synthetic malformed input, not evidence that the three frozen transcriptions contain this defect.

The correction rejects unresolved primary spans beginning `{`, `[`, or an unclosed `<`, before publishing any count. It leaves well-formed free-text comments and **closed** unselected square alternatives outside the selected-code census. It does not assign any meaning to high-ASCII glyphs or change the historical ASCII tokenizer. Unrelated unsupported tags remain outside the scope of this repair; full IVTFF 2.0.2 adjudication remains blocked.

## Regression and source invariants

Files changed: `scripts/audit_ivtff_high_ascii_coverage.py`, `scripts/audit_exp590_high_ascii_adjacency.py`, and their two dedicated test files. New adversarial rows have the bodies `{c@140;h`, `a.[b:@140;`, and `a.<!@140;`; each must raise `ValueError` containing `Unclosed primary`. Existing tests retain the excluded-comment/alternative controls and frozen-source hash gates.

Expected unchanged source identities: ZL3b SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; ZL3a `56419297682d338ff1a0a17f5ae251e3ee3e2c5bf05a62db04c5385ef30b36a2`; IT2a `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`. The previous census expectations remain 122/168, 117/160, 0/0 code-bearing rows/codes respectively. A CI run must confirm that these gates still pass; the hashes above are previously frozen expectations, **not** newly measured hashes.

## Reproduction

From the repository root, with Python 3.12:

```sh
python -m unittest discover -s tests -p 'test_ivtff_high_ascii_coverage.py' -v
python -O -m unittest discover -s tests -p 'test_ivtff_high_ascii_coverage.py' -v
python -m unittest discover -s tests -p 'test_exp590_high_ascii_adjacency.py' -v
python -O -m unittest discover -s tests -p 'test_exp590_high_ascii_adjacency.py' -v
python scripts/audit_ivtff_high_ascii_coverage.py --out /tmp/new-ivtff-coverage.json
python scripts/audit_exp590_high_ascii_adjacency.py --out /tmp/new-exp590-adjacency.json
sha256sum /tmp/new-ivtff-coverage.json /tmp/new-exp590-adjacency.json
```

The existing `.github/workflows/voynich-check.yml` runs both tests in normal and optimized mode, regenerates the two JSONs and stores SHA-256 evidence. No new random draws, seeds, holdout access, or statistical experiments are involved.

## Integrity self-audit

No target-aware fitting, linguistic mechanism, parameter search, interpretation of positive/negative scientific effects, or changes to committed claims. The three malformed rows are synthetic **parser failure controls**, not independent linguistic samples. Frozen corpora, original experimental outputs, seeds, prospective partitions, and `state/committed_claims.md` are untouched. This is not a reproduction of historical EXP-590 or proof of full IVTFF conformance.

**Pending:** verify branch CI run and both artifacts; inspect concurrent PRs and the current `master` SHA before any merge; verify push CI on the merge SHA. Remaining blockers include EXP-170 original-input provenance, complete IVTFF adjudication, and global artifact reconciliation.
