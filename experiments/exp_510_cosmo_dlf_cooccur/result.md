# exp_510: Three-Position Co-occurrence Test + F465 Bug Discovery

**Question H_new_CR:** Do A cosmo d-LF's confirmed pos1 and pen rules (y@pos1 F479 + ok@pen F487) co-occur in the same lines more than expected?

**Incidental:** F465 (A herbal_a d-LF → d-self@pos2, CONF E=1.56×/N=44) may be a 2-word-line artifact.

---

## Co-occurrence Results

### PART 1: A cosmo d-LF — y@pos1 AND ok@pen

| metric | value |
|--------|-------|
| N_lf | 63 |
| N_elig | 60 |
| y@pos1: obs/N_elig | 18/60 (30.0%) vs 17.8% base, E=1.60× CONF (F479 reproduced) |
| ok@pen: obs/N_elig | 11/60 (18.3%) vs 10.7% base, E=1.71× CONF (F487 reproduced) |
| co-occurrence obs | 5/60 |
| co-occurrence expected | 3.30 |
| E_cooccur | **1.52×** |

**H_new_CR ANSWERED: A cosmo d-LF y@pos1 AND ok@pen co-occurrence is above baseline (E=1.52×/N=5) but does not meet confirmation thresholds (need N≥10 for CONF or E≥2.0×/N≥5 for dir).** The two rules show a suggestive positive correlation (5 vs 3.3 expected) without statistical confirmation. Result is consistent with INDEPENDENCE — the rules may operate somewhat independently with slight positive correlation.

F479 and F487 are confirmed individually. Their co-occurrence is not confirmed but not depleted. The three-position grammar y[pos1]→ok[pen]→d[LF] is a suggestive but unconfirmed template.

### PART 2: A herbal_a d-LF — ot@pos1 AND d-self@pos2 (DEPLETED)

| metric | value |
|--------|-------|
| N_elig | 261 |
| ot@pos1: obs | 20/261 (7.7%), E=1.44× (near-threshold) |
| d@pos2: obs | 28/261 (10.7%), E=1.12× (below threshold — see F465 note below) |
| co-occurrence obs | 1/261 |
| co-occurrence expected | 2.15 |
| E_cooccur | **0.47× (DEPLETED)** |

Lines where ot appears at pos1 tend NOT to have d at pos2 (E=0.47×). Even though both rules individually show above-baseline enrichment, they are ANTI-CORRELATED at the line level. This is consistent with two d-LF line subtypes: (1) ot-opener lines and (2) d-self-at-pos2 lines, which rarely co-occur.

### PART 3: A herbal_a ch-LF — ch@pos1 AND ch@pos2 (INDEPENDENT)

E_cooccur = 1.33×/N=12. Near-baseline. ch-LF self-chains independently at pos1 and pos2 in A herbal_a.

### PART 4: A herbal_a cth-LF — cth@pos2 AND d@pen (INDEPENDENT, control)

E_cooccur = 0.76×/N=1. Replicates exp_493 result (INDEPENDENT). Consistent cross-session replication.

---

## F465 BUG DISCOVERY

**F465 (A herbal_a d-LF → d-self at pos2, E=1.56×/N=44) is a 2-word-line artifact.**

Direct verification:
- d-LF lines total: 290
- Two-word d-LF lines: 18 — all trivially have d at ws[1] (ws[1] = LF word = d-onset)
- With len>=2 (old method): d at pos2 = 46/279, E=1.61×/N=46
- With len>=3 (correct method): d at pos2 = 28/261, E=1.12×/N=28

**With len>=3 (correct baseline): E=1.12×/N=28 — NOT confirmed.** The apparent enrichment in F465 was driven entirely by 18 two-word lines where ws[1] is trivially the LF word (d-onset). This is the same bug that affected F458 (B herbal ch-self@pos2), corrected in exp_497.

**F465 must be retracted.** With correct methodology, A herbal_a d-LF does NOT have a confirmed d-self@pos2 rule. The corrected d-LF pos2 distribution is flat (E=1.12× below threshold).

This also corrects the A herbal_a formula grammar matrix: d-LF pos2 column should show "below threshold" not "CONF E=1.56×/N=44".

---

## Self-Audit

**Target-awareness:** None. Pure structural co-occurrence analysis.

**Feature-destroying implementation:** None. len>=3 requirement correctly applied. The F465 discovery is a FEATURE of proper implementation (len>=3), not a bug.

**Extrapolation:** "A cosmo d-LF co-occurrence: INDEPENDENT" — E=1.52×/N=5 below both CONF and dir thresholds. Stated as "above baseline but not confirmed." "A herbal_a d-LF ot/d-self DEPLETED" — E=0.47×/N=1 from 261 eligible lines. Both individual rules are near-threshold but the anti-correlation is clear. "F465 is artifact" — verified by counting: 18 two-word lines + len>=2 gives E=1.61×/N=46; len>=3 gives E=1.12×/N=28. Causal mechanism is clear.

**Negative-result scope:** F465 retraction is definitive — the mechanism (2-word-line contamination) is identified and quantified. This is not a "negative result" but a methodological correction.

**Control behavior:** No controls. N/A.

---

## Conclusions

**H_new_CR:** A cosmo d-LF y@pos1 AND ok@pen co-occur at 1.52×/N=5 — suggestive but not confirmed. The three-position grammar y[pos1]→ok[pen]→d[LF] is a template hypothesis that remains unconfirmed.

**A herbal_a d-LF subtypes:** ot@pos1 and d-self@pos2 are ANTI-CORRELATED (E=0.47×). d-LF lines appear to come in subtypes: ot-opener type (F453) and otherwise. These subtypes rarely co-occur.

**F465 RETRACTED (ARTIFACT):** A herbal_a d-LF → d-self at pos2 was inflated by 2-word-line contamination. Corrected value: E=1.12×/N=28 (not confirmed). A herbal_a d-LF pos2 grammar is flat.

The A herbal_a d-LF formula grammar matrix must be updated: d-LF pos2 = FLAT (not CONF). The d-LF confirmed rule in A herbal_a is pos1→ot ONLY (F453).
