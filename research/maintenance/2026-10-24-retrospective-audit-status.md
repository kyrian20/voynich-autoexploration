# Retrospective audit status — 2026-10-24

## Scope and limitation

This is a repository-document and open-PR inventory, NOT an exhaustive re-execution or certification of every historical experiment. Reviewed: README, OPERATIONAL_STATUS, CI_VERIFICATION, 2026-10-23 history-status review, 2026-10-22 anchor protocol/candidates, and current open-PR inventory. Historical reports cited below are existing audit findings, not newly reproduced results.

## Confirmed historical problems and dispositions

1. Seven reused numeric experiment aliases (177, 594, 596, 597, 600, 601, 602). Existing canonical path registry distinguishes 624 paths / 617 numeric aliases. Historical unqualified numeric references remain potentially ambiguous. Do not renumber frozen artifacts.
2. EXP-170: existing audit corrected 50 numeric components and two classifications; original simulation and inputs have not been fully reproduced. Use the corrected audit, never treat it as full replay.
3. IVTFF conformity: reader agreement does not certify compliance. Extended codes, uncertain spaces, ligatures and alternatives remain an open adjudication requirement.
4. CI: success of specified earlier runs does not certify the current master SHA or all historical analyses. The commit-workflow-runs connector can omit push events; absence there is not proof of no CI run.
5. Three PRs remain open at time of review: #5 (validation/coordination), #7 (long-range dependencies), #13 (semantic-anchor preregistration). #13 potentially overlaps the newly merged semantic-anchor outline; compare designs before merging to avoid duplicate or contradictory protocols.
6. The three Lp candidate labels f2r/f41v/f65r are exploratory; f65r segmentation unresolved. User screenshot observation is not a calibrated independent transcription. No verified translation.

## Immediate safeguards

- Treat EXP numeric IDs as ambiguous unless resolved to full paths.
- Require source hashes, reader policy, corpus identity, and full selection rule for each historical claim being readmitted.
- Preserve negative results, source files, original reports and correction history.
- Review PR #13 against `research/protocols/semantic-anchor-study.md` before merging either methodology into an executable experiment.
- Do not claim repository-wide green CI or scientific validation without commit-specific evidence.

## Outstanding verification work

Full corpus/Library provenance reconciliation; independent IVTFF parser tests; historical experiment-by-experiment claim audit; external dependencies for EXP-170; review of open PRs; current-master CI inspection through complete Actions API; folio-level held-out semantic-anchor experiment. None is marked completed by this note.
