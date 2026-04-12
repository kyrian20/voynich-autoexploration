# exp_570: B q-bench → r routing universality (H_new_GH)

**Date:** 2026-04-11
**Hypothesis tested:** H_new_GH — B q-bench → r routing universality
**Status:** RESOLVED PARTIAL — F633

---

## RESULTS

### Per-class q-bench → r routing in B

| Sender | →r (E×/obs) | →l (E×/obs) | →ol (E×/obs) | →o (E×/obs) | Note |
|--------|-------------|-------------|--------------|-------------|------|
| qok | **1.57×/30 CONF** | 1.03×/90 flat | 1.09×/85 flat | 0.87×/35 | qok routes to r only |
| qot | **1.97×/10 CONF** | 0.86×/20 flat | 0.77×/16 flat | 0.84×/9 | qot routes to r only |
| qo | 1.33×/5 (sub-CONF) | 1.04×/18 flat | **1.70×/26 CONF** | **1.51×/12 CONF** | qo routes to ol+o, NOT r |

**Combined q-bench → r**: obs=45, exp=27.9, E=1.61× **CONF**
**Non-q-bench → r**: obs=85, exp=90.9, E=0.94× (baseline)

### Qo routing in B (from this experiment, confirming F614)

- qo→ol CONF (1.70×/26) — confirms F614 (1.78×/26)
- qo→qo CONF (1.84×/16) — confirms F614 (1.82×/16)
- qo→o CONF (1.51×/12) — confirms F614 (1.68×/12)
- qo→d DEPL (0.34×/7)
- qo→ot DEPL (0.69×/13)
- qo→qot DEPL (0.68×/12)

---

## INTERPRETATION

**H_new_GH is PARTIALLY confirmed**: The combined q-bench → r is CONF (1.61×/45), but the class-level pattern shows a **structural dichotomy within q-bench**:

**Group 1 (qok/qot)**: Both route to r CONF individually; both avoid y, a, s; both have concentrated routing to few targets. Pattern: [qok or qot][r-word] is enriched 1.57-1.97×.

**Group 2 (qo)**: Routes to ol/o/self CONF; does NOT route to r CONF individually (1.33×/5 sub-CONF). Qo has completely different B routing targets from qok/qot.

The hypothesis "q-bench universally routes to r" is **FALSE for qo specifically**. The qok/qot → r coupling is real and CONF, but qo decouples from this pattern, routing instead to the ol/o lateral-vowel cluster.

**Structural interpretation**: B has two sub-groups within q-bench:
- **qok/qot**: "deep-q" classes that route to r (the strongest B terminal)
- **qo**: "shallow-q" class that routes to ol/o (lateral-vowel group)

This dichotomy may reflect a word-structural distinction: qo-onset words have different body class distribution (qo+l-body: qol, qolchedy) compared to qok/qot (which have more compound body forms). The routing target reflects the word-class semantics rather than a pure onset-class rule.

---

**→ F633**

---

## SUMMARY

H_new_GH RESOLVED PARTIAL.

**F633**: B q-bench routing dichotomy:
- qok→r CONF (1.57×/30); qot→r CONF (1.97×/10); combined CONF (1.61×/45)
- qo→r sub-CONF (1.33×/5); qo routes to ol/o/self instead
- B q-bench splits into [qok/qot → r] vs [qo → ol/o/self]
- Non-q-bench → r = baseline (0.94×) — the enrichment is q-bench specific
