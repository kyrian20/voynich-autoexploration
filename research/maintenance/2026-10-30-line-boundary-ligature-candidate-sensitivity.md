# IVTFF ligatures: candidate-population sensitivity in draft line-boundary replication

**Date:** 2026-10-30. **Scope:** bounded parser adjudication, **not a new EXP** and not a predictive or semantic experiment. **Status:** scoped audit **REPRODUCED** by exact-commit CI #40994826986 (SHA `a2add2fab0064557c68ddc57c6a2a3e493dd3af8`); pending review of final documentation-only commit and integration into draft PR #138. Parent: draft PR #138 at `0765dcf55e4a70718ef8555e42aa63b587c493c2`; master at initial review `342b4dd0eaf36e4b2ee94cc2628378b0ae47320b`. Historical `results.json` is **INVALID_FOR_CLAIM** for corrected code and remains frozen.

## Question and predeclared decision

IVTFF issue 2.0.2 §6.6, Table 10 specifies `{...}` as a ligature of transliterated characters, **not a generic editorial comment**. The draft predictor currently quarantines every braced span as an unknown token. For spans containing exclusively ASCII letters, this discards recoverable letter sequences. Does an explicit expansion of only those unambiguous spans change the *candidate population* of the corrected line-boundary reader?

Null/negative control: in IT2a, which has no P-body brace spans in the scoped inspection, expansion must leave candidate counts unchanged. In ZL3b, counts may increase or remain unchanged because adjacent comma/unknown barriers can still exclude the reconstructed word. We will report both outcomes; **no selection by AUC**. Criteria: (a) defaults unchanged; (b) `{ck}` expands only under named `expand_ascii`; (c) braces with apostrophes, `@nnn;`, punctuation, or malformed nesting remain barriers; (d) no positive or negative candidates are lost when the explicit view is enabled; (e) frozen source SHA-256 checks and exact CI logs; (f) no fitting, bootstrap or held-out metrics.

## Inputs and method

- ZL3b: `data/transcriptions/eva_zl3b.txt`, SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- IT2a: `data/transcriptions/eva_it2a.txt`, SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- Source script: `research/analysis/2026-10-28-line-boundary-reproduction/line_boundary_replication.py`. New named argument `ligature_policy` defaults to `quarantine`; alternative `expand_ascii` expands only `\\{[A-Za-z]+\\}` after square-alternative selection, leaving all other brace spans unresolved. This does **not** assign phonetic or semantic values to ligatures.
- Audit/test: `tests/test_line_boundary_ligature_sensitivity.py`. Python 3.12 standard library; no stochastic steps or seed. Candidate unit is an adjacent pair of accepted tokens within P rows or a permitted P-to-P boundary on one page. No classifier is trained.
- Scope: `primary` and `drop_uncertain_word` reading policies; existing comma, non-P, ordinal, paragraph and unknown-character guards unchanged. Full manuscript files are read solely for **input/candidate integrity**; no reserved-leaf outcomes are scored, and this is not a prospective confirmatory test.

The scoped pre-CI text census of P-body brace spans was **394 ZL3b, of which 283 are ASCII letters only; 0 IT2a**. The Python regression authenticated both sources and reproduced this census in CI. Some of the 283 spans may lie inside excluded readings or words blocked by other markup; they are **not** predicted to add 283 candidates.

Commands:

```sh
python -m unittest discover -s tests -p 'test_line_boundary_ligature_sensitivity.py' -v
python -O -m unittest discover -s tests -p 'test_line_boundary_ligature_sensitivity.py' -v
```

The canonical CI runs both and emits `LIGATURE_CENSUS` JSON lines with source hashes, policies, positive/negative counts and deltas. No new file is written by the audit; the GitHub Actions job log is the raw receipt. Existing `results.json`, corpus bytes, other historical results, manifests, committed claims and seeds must not be changed.

## Interpretation and self-audit

- **Target awareness:** the alternative is defined by IVTFF syntax and ASCII validity, not by any Voynich statistic or predictive score. No parameters are calibrated to a target.
- **Feature preservation:** the conservative default suppresses some valid ligature words. The explicit alternative restores only the subset whose character sequence is unambiguous under this limited policy. Other ligatures remain excluded, so a negative delta would not show the full ligature impact.
- **Extrapolation:** no claims about all IVTFF ligatures or a full conformant tokenizer. No extrapolation to all manuscript pages from the P-body subset.
- **Negative result scope:** a zero candidate delta would mean only that the tested expansion does not change these candidate counts under existing guards; it would not validate the default lexer.
- **Control behavior:** IT2a has zero P-body brace spans, so expected delta = 0; actual counts pending CI. ZL3b may gain candidate pairs but a gain is not evidence of language or a translation.

## Observed result and evidence (2026-10-30)

The GitHub Actions run [#40994826986](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40994826986) completed with **success** for commit `a2add2fab0064557c68ddc57c6a2a3e493dd3af8`. The new regression passed **4/4 tests in normal Python and 4/4 in optimized Python**. All eight `LIGATURE_CENSUS` log records were inspected: each of the four source/policy results was byte-equivalent across the two Python invocations. The run had 120 completed steps, none failed, and 22 nonempty uploaded artifacts (their individual internal contents were not audited). The raw run/job logs, not this prose, are the execution receipt.

| Corpus/policy | Quarantine positives | Expanded positives | Δ positives | Quarantine negatives | Expanded negatives | Δ negatives |
|---|---:|---:|---:|---:|---:|---:|
| ZL3b primary | 2,554 | 2,596 | **+42** | 24,270 | 24,698 | **+428** |
| ZL3b drop_uncertain_word | 2,417 | 2,451 | **+34** | 23,534 | 23,919 | **+385** |
| IT2a primary | 3,291 | 3,291 | 0 | 30,244 | 30,244 | 0 |
| IT2a drop_uncertain_word | 3,291 | 3,291 | 0 | 30,244 | 30,244 | 0 |

The independent source inspection also located **33** of the 283 ASCII-only ZL3b P-body ligatures inside square-bracket uncertain readings; this helps explain why not every span necessarily contributes a candidate. The test does not assert 33 as a frozen invariant.

**Interpretation:** the decision to quarantine all ligatures suppresses hundreds of potential candidate pairs in ZL3b, even after the earlier comma/paragraph/non-P guards. The new explicit view exposes a measurable, falsifiable **population sensitivity**, not a demonstrated predictive gain or a language feature. A candidate added under ASCII expansion may still be affected by unresolved readings or manuscript layout. IT2a's zero change is the expected negative control; it is an alternate transcription of the same manuscript, not independent linguistic replication. The model was not fitted, the historical scores remain **INVALID_FOR_CLAIM**, and no reserved-leaf outcome was consulted.

Structured snapshot: `research/maintenance/2026-10-30-line-boundary-ligature-candidate-sensitivity-results.json` (added after the first successful run). Recheck CI for the final documentation commit before integration.

**Next step:** verify the final SHA CI and integrate only into the draft scientific branch if unchanged; continue independent IVTFF adjudication for non-ASCII glyph codes and folio-layout continuity before any predictor rerun. Do not promote historical AUC/gain, claim translation or global cleanup.
