# Cryptanalyst Phase Closure
**Date:** 2026-04-12
**Experiment count:** 579
**Audience:** Future investigator picking this up cold.

---

## What Was Done

The Cryptanalyst loop investigated the structural properties of the Voynich Manuscript (VMS) through statistical characterization, theory discrimination, and generative architecture construction. The work proceeded in twelve phases from exp_001 to exp_579.

---

## Primary Result

**A 21-mechanism position-aware copy-buffer architecture achieves 19/19 PASS on a B-dialect 19-metric battery (exp_314, N=30, C008).**

The architecture is VMS-specific: applying the same fixed parameters to shuffled VMS text yields 10/19. A free grid-search re-optimizing to each shuffled corpus's own targets achieves at best 16/19 (within-line shuffle) and 14/19 (word-to-line shuffle). The failures are mechanistically explained: fixed constants (CP=0.55, MP=0.90, P_STUTTER=0.006) create structural minima for ss_y, ss_d, adj_rate, and am_ll that exceed any shuffled corpus target — these are not parameter-space gaps.

**Architecture parameters (exp_314):** CP=0.55, MP=0.90, P_STUTTER=0.006, beta_scale=1.8, p_blind=0.115, r_lf=0.12, r_mid=0.20. Fixed constants are not searchable.

**Scope:** The 19/19 is a full-corpus average over four B-dialect sections (B_herbal ~14%, B_bio ~33%, B_astro ~15%, B_pharma ~39%) with systematically different positional grammar profiles. Section composition explains 97–107% of the document-order metric gradient. A-dialect extension (exp_239) achieves 19/19 but was not the primary calibration target.

---

## What Was Ruled Out

| Mechanism | Status | Key result |
|-----------|--------|-----------|
| Position-blind ciphers (Naibbe, Timm) | **RULED OUT** (C001) | Max am_ll ≈ 1.06×; VMS requires 6.8× |
| Pure self-citation (Timm alone) | **RULED OUT** | Joint ss_mean/adj_rate constraint unsatisfiable across 75-combination parameter space |
| Onset-replacing position-aware hybrid | **RULED OUT** (C003) | 0/18 viable — modification destroys onset self-succession |
| Position-sensitive substitution alone | **RULED OUT** (C002) | ss_mean ≈ 1.00×; VMS requires 1.47× |

---

## What Was NOT Ruled Out

The architecture reproduces the statistics of VMS but does not identify the underlying process. The following interpretations remain open:
- Natural language with position-sensitive writing conventions
- Artificial/constructed language with compact grammar rules
- Glossographic or domain-specific notation (section-specific grammar is consistent with this)

No decipherment was attempted. The architecture is a statistical generative model, not a cipher key.

---

## Key Structural Findings

**Dual constraint** (Sections 2–3 of working_position.md): VMS requires BOTH position-sensitive onset-class grammar (am_ll 6.8×, y_lf 3.5× enrichment) AND sequential word-class memory (ss_mean 1.47×, ss_d/ss_y/ss_qok elevated). No single mechanism satisfies both. The copy-buffer hybrid is the only tested class that does.

**Copy-buffer + self-succession → adj_rate overproduction** (C009): The architecture generates adjacent identical word pairs 1.4–1.8× above VMS for sh/ch/d because the copy-buffer amplifies same-onset self-succession (sh→sh=9%, ch→ch=15%). This is a known residual gap. VMS adj_rate for sh/ch/d is near-random expectation from finite vocabulary pools; s/t adj_rate = 0 from positional constraint.

**B-dialect section heterogeneity** (F639, C008 scope qualification): Four B-dialect sections have systematically different positional grammar profiles (am_ll: bio=0.053 to pharma=0.192). Document-order metric gradients are explained by section composition, not scribal hand transitions or linguistic drift.

**Grammar beyond the word level** (Sections 6–7 of working_position.md): Three-register line grammar, section-specific LF taxonomies, A herbal_a directed cross-line network (d→qot→ch→…), B-dialect section CL patterns, B pharma penultimate grammar. These are characterized but not yet incorporated into a generative grammar specification.

---

## Committed Claims (C001–C009)

See state/committed_claims.md for full claim text, supporting experiments, and contradiction conditions.

**Known issue:** C007 (onset self-succession range 1.24–2.05×) has three documented errors — wrong range, attribution error, and "residuals ≥1.2× for all" fails. Amendment in state/proposed_commitments/proposed_c007_amendment.md, awaiting human approval.

---

## Open Questions at Closure

- **Q007 (partial):** Copy-buffer adj_rate overproduction is diagnosed but not resolved architecturally. Any copy-buffer with ≥8% same-onset self-succession will exhibit this. Resolution requires architectural change (adjustable CP/MP).
- **Q012:** k-onset is not LF-enriched unlike p/t/f (gallows anomaly). Unresolved.
- **Q016:** B p→sh→{pos2} grammar extension. Unresolved.
- **F455/Q010/Q015:** A herbal_a ok-LF → y at pos1: provisionally directional, cannot confirm at CONF with strict section boundaries.

---

## How to Resume

1. Read SOUL.md (identity and loop definition)
2. Read state/working_position.md (full synthesis, theory state, all findings)
3. Read state/committed_claims.md (what is committed in public outputs)
4. Consult state/hypothesis_backlog.md for untested hypotheses
5. Do NOT run new Cryptanalyst experiments without explicit direction — the loop is at closure point
6. Next phase directed by human: Grammar Spec consolidation

---

## Files and Directories

```
experiments/exp_001–exp_579/   — all experiment scripts, results, data
state/committed_claims.md      — canonical public commitments (C001–C009)
state/working_position.md      — full synthesis (read cold)
state/findings.md              — 639 established facts (grep by ID)
state/working_model.md         — characterization reference by topic
state/failed_approaches.md     — ruled-out directions
state/open_questions.md        — unresolved questions
state/hypothesis_backlog.md    — untested hypotheses
state/iteration_log.md         — one-line experiment log
state/proposed_commitments/    — pending C007 amendment
state/proposed_commitments/applied/ — applied proposals (C008, C009, C003 qualification)
state/commitments_audit_2026_04_12.md — this session's audit record
state/archive/                 — Opus reviews, resolved hypotheses, paper materials
```
