## Voynich Cryptanalyst

Read SOUL.md before doing anything. It defines your identity, methodology, behavioral constraints, and the mandatory audit_experiment skill.

Key files:
- SOUL.md — identity and loop definition
- skills/ — five skill files (run_experiment, audit_experiment, write_finding, generate_hypotheses, query_kb)
- state/ — live working memory:
  - working_position.md — theory discrimination synthesis (the live document; read every iteration)
  - hypothesis_backlog.md — active untested hypotheses only (resolved hypotheses archived)
  - committed_claims.md — claims in public outputs (check before updating findings/failures)
  - findings.md — 284 established facts (grep by ID, don't read cover-to-cover)
  - working_model.md — characterization reference organized by topic (consult when needed, not every iteration)
  - failed_approaches.md, open_questions.md, iteration_log.md, current_state.md
- state/archive/ — Opus reviews, paper materials, resolved hypotheses (reference, not read during normal iterations)
- experiments/ — 287 experiment directories with scripts, results, and data

Constraints that must never be skipped:
1. Run skills/audit_experiment.md after every experiment, before updating state files.
2. Check state/committed_claims.md before writing to findings.md or failed_approaches.md. If a contradiction exists, STOP and write to open_questions.md instead.
3. Do not edit committed_claims.md — only the human updates it. You may propose new commitments in state/proposed_commitments.md.

## Housekeeping

- Every 10 experiments, move resolved hypotheses from hypothesis_backlog.md to state/archive/hypothesis_backlog_resolved.md.
- Every 30 experiments, append a dated 1-paragraph summary to current_state.md.
- If you've run 5+ experiments on the same narrow topic, switch to a different category: word-internal structure, cross-unit patterns (folio/section level), anomalies, or simulation implications.
