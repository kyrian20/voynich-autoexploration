# EXP-620 — named composite folio subtype: exact-head CI result (2026-11-15)

Status: **LEXICAL CENSUS VERIFIED IN CI; IVTFF ADJUDICATION OPEN**. This note records a new result, not a translation or rehabilitation of frozen EXP-612–619 claims.

## Provenance
- PR #284 head before this report: `6e07226d69eb18de9b7623332c46ffa372db38ae`; base `master` observed at `19439462f661a7443c54db163f6d7de9b0a99253`.
- Exact-head successful workflow run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/43679504917 (job 132706835653). Python syntax check, embedded self-tests, corpus hash checks, JSON formatting and artifact upload succeeded.
- Artifact: https://github.com/kyrian20/voynich-autoexploration/actions/runs/43679504917/artifacts/14148045945 ; archive digest reported by GitHub: `sha256:b502cc18c5224bd305fdcaf0b42ee8fab36c840c4bea7a909d9e1420075e4dab`. ZIP contents were **not** independently downloaded and hashed. Log confirms `exp620-angle-subtypes.json` and `exp620-angle-subtypes.sha256` uploaded, retention 90 days.
- Script: `research/maintenance/exp620_angle_record_subtypes.py`, blob SHA `b549508417d65ca774f6215c098f57960c4a17fd` at checked head. Command: `python research/maintenance/exp620_angle_record_subtypes.py | tee exp620-angle-subtypes.json`; `python -m json.tool exp620-angle-subtypes.json`; `sha256sum exp620-angle-subtypes.json`. Deterministic, seed not applicable.

## New observed counts (CI stdout)

| Corpus | named header | named locus | panel header | panel locus | total excluded angle records |
|---|---:|---:|---:|---:|---:|
| ZL3b | 1 | 160 | 42 | 1028 | 1231 |
| IT2a | 0 | 0 | 42 | 1024 | 1066 |

Source SHA-256: ZL3b `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` (411671 bytes); IT2a `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`. ZL3b physical line 5253 is the sampled named header; sampled named loci begin at 5262. The 161 previously unclassified ZL3b records are now **lexically** assigned to named header/locus categories. This is a partition of the same 1231 records, **not** an increase in analyzed tokens.

## Limits and next decision
- The regexes identify `fRos` and its numbered loci as candidates; they do **not** establish normative IVTFF eligibility, independent semantic anchors, or valid `ch/sh` events.
- No corpus or frozen output changed. No EXP-612–619 scientific rerun is authorized by this result. The historical exclusion policy and cross-edition comparability remain open.
- Next: inspect literal named-locus content and IVTFF grammar with independent adjudication; quantify eligible follower events only after documented policy approval, preferably on reserved physical folios without training leakage.
