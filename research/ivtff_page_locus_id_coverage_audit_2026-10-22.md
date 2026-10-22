# IVTFF page/locus identifier coverage audit — 2026-10-22

## Status

**Structural audit passed in GitHub Actions run 575**: [Voynich Check run 575](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39740049037). Regression fixtures also passed in [run 574](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39740031613).

The audit is deliberately non-destructive. It does not edit transcription files or regenerate historical experiment outputs.

## Results

| Source | Bytes | SHA-256 | Page headers / distinct | Locus records | Malformed headers | Malformed records | Page/header mismatches | Locus numbers outside 1–160 |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| ZL3b | 411,671 | `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` | 227 / 227 | 5,385 | 0 | 0 | 0 | 0 |
| ZL3a | 411,710 | `56419297682d338ff1a0a17f5ae251e3ee3e2c5bf05a62db04c5385ef30b36a2` | 227 / 227 | 5,389 | 0 | 0 | 0 | 0 |
| IT2a | 342,104 | `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5` | 225 / 225 | 5,215 | 0 | 0 | 0 | 0 |

All three files include the special page names needed by the corpus, including subdivided folios such as `f67r1` and the combined Rosettes page `fRos`. The regression fixtures explicitly test `f67r1.5`, `f86v4.160`, and `fRos.23`, as well as malformed and mismatched identifiers.

The record totals differ between transcriptions. This audit confirms structural coverage and active-page agreement, **not** that ZL3a/ZL3b/IT2a have identical locus populations or independent evidential status. In particular, ZL3a and ZL3b are alternative transcriptions of the same manuscript.

## Method and limitations

The script checks:
- recognizable page-header names under the corpus's standard folio/subdivision conventions, including `fRos`;
- locus-ID shape, numeric field syntax, and the three-character locator/type code;
- whether each locus refers to the active page header;
- whether the locus number is within the current corpus sanity range 1–160.

Reference: [IVTFF format definition 2.0.2, issue 08-07-2025](https://www.voynich.nu/software/ivtt/IVTFF_format.pdf), especially §§4.2, 5.4, 6.3–6.5. The specification defines the page name and locus-ID fields, the optional transcriber ID, and the special Rosettes page. This script is a structural audit, not a full IVTFF validator; additional semantic constraints and the content of every locus are outside its scope.

## Files added

- `scripts/audit_ivtff_page_locus_ids.py` — non-destructive inventory and source hashes.
- `tests/test_ivtff_page_locus_ids.py` — valid/invalid regression fixtures.
- `.github/workflows/voynich-check.yml` — runs both test and audit on CI.

## Consequence for the research

The previous concern that simple line-ID patterns may silently omit valid records remains material for legacy experiments such as EXP-590. This audit establishes that the three selected source files have structurally parseable page/locus identifiers under the declared checks; it does **not** automatically repair or invalidate any historical analysis. Before regenerating a result, each experiment must explicitly choose and document its source population and tokenizer, then be rerun with its own saved output and hash.
