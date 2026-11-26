# EXP-620 — panel-subtype CI result (2026-11-15)

Status: **DESCRIPTIVE ONLY; not an IVTFF adjudication, historical reproduction, or translation.**

## Exact provenance

- PR #284, head before this report: `d9f8eb5c8e81c72c8559b4d66fd848682f4b71a5`.
- Workflow run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/43670619214 — completed, conclusion success; job 132679614052.
- Output artifact: https://github.com/kyrian20/voynich-autoexploration/actions/runs/43670619214/artifacts/14143669605 (JSON + SHA-256 manifest; retention 90 days). ZIP SHA-256 as reported by upload action: `d2b0ff9e4ef2962ccc45e40791098463d7c6c63f3a7c1b94713d6b722bfa1b4f`.
- Command: `python -m py_compile research/maintenance/exp620_angle_record_subtypes.py`; `python research/maintenance/exp620_angle_record_subtypes.py | tee exp620-angle-subtypes.json`; `python -m json.tool exp620-angle-subtypes.json`; `sha256sum exp620-angle-subtypes.json > exp620-angle-subtypes.sha256`.
- Deterministic lexical classification; no RNG or seed. Input files and historical scripts unchanged.

## Counts from CI job stdout

| Corpus | Panel headers | Panel loci | Other f-prefixed | Total excluded angular records |
|---|---:|---:|---:|---:|
| ZL3b | 42 | 1,028 | 161 | 1,231 |
| IT2a | 42 | 1,024 | 0 | 1,066 |
| Total | 84 | 2,052 | 161 | 2,297 |

- ZL3b: `data/transcriptions/eva_zl3b.txt`; 411671 bytes; SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- IT2a: `data/transcriptions/eva_it2a.txt`; 342104 bytes; SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- Example physical lines: ZL3b panel header 2815, panel locus 2823, other f-prefixed 5253; IT2a panel header 1767, panel locus 1768.

## Scope and limitations

This resolves the previous runtime `NameError` at the CI-tested head and partitions the formerly residual 2,297 angular records by lexical shape. It **does not** establish that panel loci are eligible text under IVTFF, that they contribute ch/sh events, or that EXP-613–617 conclusions should change. The 161 residual ZL3b records require literal inspection and independent IVTFF adjudication. CI log and artifact listing were checked, but the downloaded ZIP contents were **not** independently decompressed and hash-verified here. No frozen corpus, historical output, committed claim, or semantic label was modified.

Next bounded repair: examine exact literal tags at ZL3b physical lines beginning 5253, document their IVTFF role, then write a parser regression with explicit inclusion policy and held-out folio check **only after** the policy is independently justified. Do not repeat the census as an experiment.
