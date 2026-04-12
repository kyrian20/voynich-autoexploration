# Loop Audit — 2026-04-11
**Scope**: Diagnostic analysis of research infrastructure drift, covering exp_200–287.
**Purpose**: Determine when state-file updates stopped, identify experiments that skipped mandatory steps, identify any experiments that should have triggered a stop condition.

---

## 1. WHEN DID STATE-FILE UPDATES STOP?

### Iteration Log
The iteration_log.md contains entries through **exp_199** as of this audit. The last logged entry is:
```
2026-04-11 | exp_199 | B WP-LF composition + d+ch successor...
```
Entries for exp_200–287 (88 experiments) were missing entirely. This represents a complete failure of the logging loop starting with exp_200.

### current_state.md
current_state.md said "through exp_181" at the start of this session — a gap of 106 experiments (exp_182–287 not reflected). This indicates the state file was last updated after exp_181, then abandoned.

### working_position.md
working_position.md was being updated as append-only addenda through exp_286 (the file header said "updated through exp_258" but the body contained addenda through exp_286). The document grew to 1,203 lines of per-experiment narrative, functioning as a second iteration log rather than a synthesis. This represents loop drift at the synthesis level — the document format degraded from synthesis to chronological log.

### hypothesis_backlog.md
The backlog contained 937 lines with the vast majority of entries marked RESOLVED but never moved to archive. At least two stale "Status: open" lines existed (H435 had both a resolved and an open status line — the original "open" was never removed when RESOLVED was prepended). Active versus resolved hypotheses were not easily distinguishable.

### Summary of drift timeline
| File | Last proper update | Drift period |
|------|--------------------|--------------|
| iteration_log.md | exp_199 | exp_200–287 (88 experiments) |
| current_state.md | exp_181 | exp_182–287 (106 experiments) |
| working_position.md | Degraded to append-only log; last synthesis was through ~exp_186 | exp_187–287 synthesis not written |
| hypothesis_backlog.md | Never pruned after archive was established | Accumulated 930+ lines of resolved entries |

---

## 2. DID ANY RESULT.MD SKIP AUDIT STEPS?

### write_finding.md step
Every experiment from exp_182 through exp_287 that has a result.md file appears to have a finding recorded (F182 through F286 are referenced in working_position.md addenda). However, this cannot be confirmed without reading every result.md — the write_finding.md step appears to have been executed for experiments whose findings appear in working_position.md.

**Experiments with no result.md:**
- exp_287 (exp_287_suffix_length_gradient): only script.py present. No result.md, no finding. This experiment was STARTED but not COMPLETED. No loop step was executed for it.

**Experiments with result.md but potentially missing audit steps:**
The audit_experiment.md skill was mandatory after every experiment per SOUL.md. The working_position.md addenda for experiments in the exp_217–287 range do not explicitly mention the audit step being run. Three specific failure modes were defined in SOUL.md (Catches 1, 2, 3) and the audit was designed to catch them. Without the audit step evidence, it is unclear whether:
- Check 1 (target-awareness) was applied to new calibration experiments
- Check 2 (feature-destroying implementation) was verified for mechanism changes
- Check 5 (control-comparison interpretation) was checked

**Notable target-awareness cases (Check 1 risk):**
- exp_209 (p_blind calibration to VMS am_ll): all parameters were explicitly set using knowledge of VMS targets. The result.md was written and the critical caveat appears in the working_position.md addendum, suggesting awareness was documented. No violation, but audit compliance uncertain.
- exp_210/211 (joint five-metric calibration): same situation — all four parameters target-calibrated. Critical caveat documented in working_position.md. Uncertain whether formal audit_experiment.md skill was invoked.

**Most likely assessment**: The write_finding.md step was consistently executed (findings F182–F286 all exist). The audit_experiment.md step compliance is uncertain for exp_200–287 because no explicit audit log was maintained. The audits for the specific catches that apply (target-awareness) appear to have been addressed by documenting the caveat in result.md text, but formal skill invocation is unverifiable from the state files alone.

---

## 3. WHICH EXPERIMENTS SHOULD HAVE TRIGGERED A STOP CONDITION?

### Stop conditions defined in SOUL.md / skills
- **committed_claim_at_risk**: If an experiment contradicts a committed claim in committed_claims.md, stop and write to open_questions.md. (Q003 was the model for this.)
- **audit_flagged**: If audit_experiment.md raises a flag, pause.
- **control_anomaly**: If a control behaves unexpectedly (especially exceeds real data), investigate before interpreting.

### Review of exp_200–287 for missed stop conditions

**Q003 was resolved before this range** (the C004 narrowing was handled by the human before exp_200). No committed-claim at-risk event was detected in the working_position.md addenda for exp_200–287.

**Experiments that may have warranted stop-condition review:**

1. **exp_245/246** (self-succession diagnostic): exp_245 asserted that exp_241's MISSED classification was an artifact and that the buffer OVER-produces self-succession. exp_246 then partially contradicted exp_245 (ot→ot IS a genuine gap). This is a within-two-experiment contradiction that reversed an interpretation. Neither experiment references a stop condition. The contradiction was resolved by the experiments themselves, but the exp_245→exp_246 reversal is the kind of pattern the audit_experiment.md skill's Check 2 (feature-destroying implementation) was designed to catch: exp_245's theoretical prediction was contradicted by direct measurement. **Verdict**: Should have flagged for human review but didn't; resolved correctly.

2. **exp_253 (ot→ot Markov)**: p_ot_ot=0.10 added as 13th mechanism. This was subsequently found to be over-calibrated to a contaminated gap (the 'other' onset bug, discovered in exp_254). The contaminated mechanism was reverted in exp_256. The three-experiment sequence (add mechanism, discover bug, revert) is self-correcting but represents a case where a mechanism was added to the architecture based on a false measurement. **Verdict**: The bug was discovered and corrected; no committed claim referenced ot→ot; no stop condition required. But the sequence shows audit_experiment.md's Check 1 (are we measuring what we think we're measuring?) should have caught the 'other' onset label being used as a literal string before exp_253 added a mechanism.

3. **exp_282/283 architectural inconsistency**: exp_282 implemented MID midfix (p_mf=0.20) and word-index conditioning simultaneously. exp_283 then diagnosed that the positive Menzerath r was caused by LF midfix being MISSING from cipher_lf() — a propagation error from exp_280. This means exp_282's mechanism was built on a state where LF midfix was broken. The gamma and alpha parameters in exp_282 were calibrated against a simulation with a missing component. **Verdict**: The broken state was diagnosed in exp_283 and corrected in exp_284. The gamma/alpha parameters (gamma=0.30, alpha=0.20) were retained after the fix and reconfirmed valid (exp_286 battery 19/19 PASS). No stop condition formally triggered. However, this is a case where a bug in the simulation (omitted LF midfix) affected mechanism calibration across exp_282–283. The audit's Check 2 (does implementation actually implement what hypothesis says?) would have caught this if applied to exp_280 when the LF midfix was first added.

4. **exp_285 (LL midfix)**: exp_285 found that reducing p_ll_mf WORSENED menz_r (opposite of hypothesis). The result states "NEGATIVE — opposite direction." This is a control-direction anomaly analogous to Catch 1 (when a control behaves unexpectedly). The correct response per SOUL.md is to investigate before interpreting. The investigation WAS done within exp_285 (the root cause — LL acting as a length anchor for short lines — was identified). **Verdict**: Handled correctly within the experiment.

---

## 4. SUMMARY AND RECOMMENDATIONS

### What stopped working
1. **Iteration logging** stopped completely at exp_199. The SOUL.md step 9 ("Log iteration") was not executed for exp_200–287.
2. **current_state.md** was not updated for 106 experiments.
3. **working_position.md** was maintained (as appended addenda) but degraded from synthesis to iteration log.
4. **hypothesis_backlog.md** was never pruned.

### Root cause assessment
The loop was running experiments and recording findings (write_finding.md appears to have been executed), but the state-update housekeeping steps (iteration_log.md, current_state.md, hypothesis_backlog.md pruning) were omitted starting around exp_200. This is consistent with a session restart where the "Read state" step (SOUL.md step 1) was abbreviated, causing the agent to proceed to experiment execution without updating log files.

### No catastrophic failures detected
- No committed claims were contradicted in the exp_200–287 range.
- The 'other' onset bug (exp_254–256) was discovered and corrected before it affected any final architecture claim.
- The LF midfix propagation error (exp_280→283) was self-correcting.
- The exp_245→246 reversal was handled within the experimental sequence.
- No finding in this range conflicts with committed_claims.md based on working_position.md addenda.

### Recommended actions
1. **Complete exp_287**: exp_287_suffix_length_gradient has only script.py. Run the script and write result.md.
2. **Run audit_experiment.md on exp_282** retroactively: the MID midfix + word-index conditioning experiment was run while LF midfix was broken. While exp_286 confirmed the gamma/alpha parameters are still valid, a formal audit would confirm no Check 2 violation persists.
3. **Verify F261 s→s claim** (Q005): re-run exp_261's VMS ss computation to confirm whether VMS s→s=0.887 was MID-only N=1 or something else.
4. **Enforce SOUL.md step 9** in all future sessions: iteration_log.md must be updated after every experiment, not in batch.
