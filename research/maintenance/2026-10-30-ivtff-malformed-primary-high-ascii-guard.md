# IVTFF — malformed primary @ codes in high-ASCII inventories

**Date:** 2026-10-30. **Scope:** software-integrity repair; no new EXP, no decipherment claim. **Status:** proposed on a separate branch; CI and post-merge verification required before closing.

## Concrete defect and falsifiable regression

The frozen `scripts/ivtff_lossless.py` lexer marks a malformed `@12;` as `unresolved` with a `malformed_high_ascii` diagnostic. Two derived primary-reading censuses, `scripts/audit_ivtff_high_ascii_coverage.py` and `scripts/audit_exp590_high_ascii_adjacency.py`, traversed only recognized `high_ascii` spans and silently ignored the unresolved `@` when a row also contained ordinary ASCII words. For example, `<f1r.1,@P0> qo@12;dy` could be reported as having **zero** high-ASCII codes rather than being rejected. This is a demonstrated code-path defect on a synthetic adversarial row, **not evidence that the frozen sources contain this malformed code**.

The correction fails closed for unresolved primary `@` spans, including those inside primary ligatures. It deliberately does not interpret comments or discarded square-bracket alternatives as primary readings. The frozen lexer and corpus are unchanged. This is an input-validation repair, not a new transliteration or a historical EXP-590 reproduction.

## Evidence and acceptance

Changed scripts: `scripts/audit_ivtff_high_ascii_coverage.py`, `scripts/audit_exp590_high_ascii_adjacency.py`. New cases in `tests/test_ivtff_high_ascii_coverage.py` and `tests/test_exp590_high_ascii_adjacency.py` reject `qo@12;dy`, `a.@12;` and `{c@12;h}.a`, while leaving comment and unselected alternative content out of primary counts. Existing frozen-source regression tests must continue to pass and preserve ZL3b 122/168, ZL3a 117/160 and IT2a 0/0 code-row/code counts.

Run on Python 3.12 from repository root:

```sh
python -m unittest discover -s tests -p 'test_ivtff_high_ascii_coverage.py' -v
python -O -m unittest discover -s tests -p 'test_ivtff_high_ascii_coverage.py' -v
python -m unittest discover -s tests -p 'test_exp590_high_ascii_adjacency.py' -v
python -O -m unittest discover -s tests -p 'test_exp590_high_ascii_adjacency.py' -v
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

CI in `.github/workflows/voynich-check.yml` is the authoritative remote verification for the branch. Do not claim the repair reproduced until checking the exact run, its logs and relevant artifact if produced. The two auditors already have full frozen-source regressions, so the original corpus hashes and their expected counts are also checked. No randomization, seeds or reserved folios are used.

## Scientific integrity and limitations

This change prevents **silent acceptance of one class of malformed primary glyph code**; it does not certify full IVTFF grammar, adjudicate glyph identity, or restore historical claims. The alternative transcriptions are not independent manuscript samples. No source files, historical output, hypotheses, `state/committed_claims.md` or prospective holdout manifests are changed.

Self-audit: no parameters calibrated to Voynich metrics; no linguistic feature tested or destroyed; no inference outside the synthetic malformed-code fixtures and the three frozen-source regression gates; no negative scientific result; no stochastic control. The comments/alternative fixture is a **scope control**, not a language baseline.

**Next step:** check branch CI and frozen-source counts, then inspect current `master` and concurrent PRs before merging. If green, verify push CI on the resulting merge SHA. EXP-170 original-input provenance and full IVTFF adjudication remain separate blockers.
