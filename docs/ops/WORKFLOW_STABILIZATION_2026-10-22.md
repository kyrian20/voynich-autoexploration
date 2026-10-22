# GitHub Actions stabilization — 2026-10-22

## Scope
Reduce self-triggering runs for experiments 604–611 without deleting or rewriting scientific outputs.

## Change applied
For each workflow `.github/workflows/voynich-exp604.yml` through `voynich-exp611.yml`, the `push.paths` trigger was narrowed from the whole experiment directory (`experiments/<experiment>/**`) to the experiment's `script.py`, required input transcription files, and the workflow file itself. This prevents commits that update generated `results.json` / `result.md` from retriggering that same workflow.

- EXP-604: `experiments/exp_604_independent_transcription_replication/script.py`, `data/transcriptions/eva_it2a.txt`, workflow.
- EXP-605: script, `data/transcriptions/eva_zl3b.txt`, `data/transcriptions/eva_it2a.txt`, workflow.
- EXP-606: script, both transcription files, `scripts/audit_ivtff_metadata.py`, workflow.
- EXP-607–611: each experiment's `script.py`, both transcription files, workflow.

## Evidence and limits
- A failed EXP-606 run (run ID `39673613865`, commit `65f6b4cbe52c46cb23a0946994d4f95dfcb64660`) logged `ModuleNotFoundError: No module named 'scripts'`. The current EXP-606 script explicitly adds the repository root to `sys.path`; this stabilization change does not alter its scientific calculations.
- A failed EXP-611 run (run ID `39673446318`) occurred during a YAML indentation fix. Check the latest run before considering the workflow fully validated.
- At audit time, the latest 100 repository runs contained 93 successes, 2 failures, and 5 in-progress runs. This is a rolling page, not a complete accounting of all 73 email notifications.
- No historical result files were deleted or renumbered.
- Follow-up required: verify post-change runs for each workflow and inspect any remaining failed or “No jobs were run” notifications individually. Do not interpret “No jobs were run” alone as evidence that the scientific script failed.

## Commit references
- EXP-604: `a338e0ef96ac0086e19e478ab81629feccccd87e`
- EXP-605: `d26ff00887259a8c814392d7e914cc0bb9598074`
- EXP-606: `4387d1b823baf2a4608f52746b1174f376f63d7b`
- EXP-607: `6bf91e64484609e4f6157ad7efeb72ead7331d81`
- EXP-608: `49b8e2e8a3753358bd77a20a567d5cfae77e00c7`
- EXP-609: `bc1cf136fd5222fc99718093e3ae79b9101b72d8`
- EXP-610: `0a1fe1d75691e4e6e7661945b60147db5b480f73`
- EXP-611: `bdd9115fc6ee8468a8c81e1cb1a13195f32400c1`


## Follow-up audit — 2026-10-22

Extended the trigger audit to four more workflows: EXP-603, EXP-601 folio-clustered confirmation, EXP-592 folio influence, and EXP-602 held-out prediction. Their push filters now target the script and input files rather than the whole experiment directory, and their write concurrency groups use `voynich-master-writes`.

During validation, the first edits exposed duplicated path entries; EXP-602 had a malformed trailing quote that caused its workflow run to fail. This was corrected immediately by replacing each complete `push.paths` block rather than editing a partial line. Follow-up commits:
- EXP-603: `6bcd3c65dacdd7731555da36cc93cf0cb2536f53`
- EXP-601: `c68113ab86e3a2d6110003eab2c8970dc2319d61`
- EXP-592: `e70a20812f992edc8d8441c1f91a4f8f96c1d708`
- EXP-602: `6ce6a864d4c3432cfe335b73ba99a21b54953c8a`

The trigger files have been re-fetched after correction. Their new post-fix workflow runs must complete before marking all four fully validated. No scientific result files were deleted or modified as part of this workflow cleanup.


## EXP-602 follow-up — verified 2026-10-22

The apparent EXP-602 failures at runs `39714457080`, `39714486884`, `39714490804`, and `39714495615` had no jobs started; they corresponded to workflow YAML/configuration revisions during the rapid stabilization commits, not failures inside the scientific Python test. The corrected workflow run `39714499934` completed successfully: compile-check, held-out prediction, artifact upload, and generated-result commit all passed. General repository check `39714508491` also passed.

The scientific result itself is negative for the predeclared primary claim. On the 528 held-out Currier B P0 lines across 21 held-out folios, the train-only global start probability for `daiin` has log-loss gain `-0.0813` versus the conditional inventory baseline; the folio-cluster bootstrap 95% interval is `[-0.1117, -0.0564]`, with bootstrap probability of positive gain 0.0. Brier gain is `-0.0080`. The declared decision rule is therefore not met: this simple model does not demonstrate predictive improvement. Important limitation: the comparison baseline uses each held-out line's token inventory and is a conditional null, not a deployable prediction system. This is not evidence for a semantic decipherment.

No scientific outputs were changed during this documentation update.
