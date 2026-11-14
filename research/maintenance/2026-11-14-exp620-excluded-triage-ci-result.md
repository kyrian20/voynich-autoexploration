# EXP-620: excluded-record lexical triage — exact-head CI evidence (2026-11-14)

## Scope and provenance
This is a **lexical shape census**, not IVTFF grammar adjudication, a corrected historical replay, or decipherment. The source is the unmodified `research/maintenance/exp620_excluded_record_triage.py` at commit `324a93e18aa91895f319f32d9db70d6d88baa4cc` (blob `95813442a13c8ef71dcdaf68bc2e0f5fc4351734`). Its self-test, compilation, JSON parse and execution passed in [exact-head CI run 43640914605](https://github.com/kyrian20/voynich-autoexploration/actions/runs/43640914605), job `132588064756`. The CI logs include the JSON output; [artifact 14132048056](https://github.com/kyrian20/voynich-autoexploration/actions/runs/43640914605/artifacts/14132048056) stores JSON and SHA-256 manifest (ZIP digest `sha256:d9bdab204bd2320f9db30df679b8c05a2f1c1588dca8cadb71189ab92e0891ee`). ZIP contents have **not** been independently extracted and hashed.

| Corpus | Input SHA-256 | Physical lines | Recognized headers | Recognized lines | Comments | Other angle records | Excluded nonblank |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| ZL3b | `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` | 8510 | 184 | 4197 | 2898 | 1231 | 4129 |
| IT2a | `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5` | 5444 | 183 | 4191 | 4 | 1066 | 1070 |

Checks: ZL3b 184+4197+2898+1231=8510; IT2a 183+4191+4+1066=5444. All 5,199 excluded nonblank lines partition as **2,902 comments** and **2,297 other angle records**. No malformed-folio, unclosed-angle, or other-text categories appeared under this particular first-match classifier. This **does not** establish that the 2,297 angle records are valid or invalid IVTFF; nor that the current parser should ingest them.

## Reproduction and interpretation
```sh
python -m py_compile research/maintenance/exp620_excluded_record_triage.py
python research/maintenance/exp620_excluded_record_triage.py > exp620-excluded-triage.json
python -m json.tool exp620-excluded-triage.json >/dev/null
sha256sum exp620-excluded-triage.json > exp620-excluded-triage.sha256
```
No random seed (deterministic). The historical parsers, source corpora, and frozen results remain unchanged. The zero header/line folio mismatches in the prior recognized-line census cannot be extended to the 2,297 angle records. There is no evidence here for a `ch/sh` effect, held-out folio generalization, or a validated translation.

## Next actionable issue
Adjudicate the 2,297 `other_angle_record` shapes against the exact IVTFF specification and original line identifiers, preserving examples, denominators, and source hashes; only then assess whether any eligible `ch/sh` event was excluded. Avoid re-running the same census without a new policy or source. This report is a scoped CI-result receipt, not an independent scientific audit or approval to merge PR #284.
