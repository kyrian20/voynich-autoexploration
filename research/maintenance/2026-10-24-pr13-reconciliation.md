# PR #13 reconciliation audit — 2026-10-24

Scope: static review of open draft PR #13 against current master; no execution or merge. PR #13 was 131 commits behind master when compared. Its changed paths include the shared CI workflow; direct merge is not authorized by this review.

## Findings

- The PR proposes an EXP-580 historical label inventory exporter and replay script, plus tests and a prospective semantic protocol.
- `scripts/export_exp580_label_inventory.py` invokes the historical EXP-580 script through `runpy.run_path`, reads its `label_lines` and `body_lines` globals and checks expected headline counts `(1087, 4113, 1036, 7030, 489, 547)`. This is a replay of the historical parser, NOT independent IVTFF verification. Its own status string correctly says so.
- The inventory stores `folio` and `locus` but no unique line identifier. These fields cannot by themselves locate every occurrence unambiguously. An implementation intended for blind annotation must add stable source-line/record IDs and original raw bodies before use.
- `tests/test_exp580_label_inventory.py` tests ordering, counts, formatting and internal consistency; these tests cannot establish correct folio/locus attribution or parser independence.
- `scripts/replay_exp580_label_counts.py` checks archived counts by executing the historical script. Agreement validates replay in the tested environment, not source classification or semantics.
- The prospective protocol refers to `research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json`, which is present on master and explicitly says its 102 leaves (68 train, 16 development, 18 test) are NOT historically untouched. Preserve that caveat.
- The existing `research/protocols/semantic-anchor-study.md` is a brief outline, whereas PR #13 adds operational criteria and controls. They overlap conceptually but are not interchangeable. Do not declare either confirmed.

## Disposition

PR #13: KEEP DRAFT; DO NOT MERGE stale workflow changes. Salvage candidate scripts only on a fresh branch from master, with unique source IDs, independent reader checks and tests for adversarial/ambiguous IVTFF cases. No counts or scientific outcomes from this static inspection are newly verified. PRs #5 and #7 also remain divergent and require separate content review.
