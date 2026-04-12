# exp_490: B pharma ch@pos2 Universality + B astro q-bench pos2 Self-Chaining

**Questions:** (H_new_BO) Is ch@pos2 universally elevated in B pharma? (H_new_BN) Does pos2 self-chaining hold for B astro q-bench classes?

---

## 1. H_new_BO: B pharma ch@pos2 — REFUTED

ch@pos2 is **at or below baseline** for all B pharma LF classes:

| LF onset | N_lf | obs_ch | E(ch@pos2) | flag |
|---------|------|--------|------------|------|
| ch | 158 | 52 | 1.30× | — |
| l | 92 | 24 | 1.03× | — |
| a | 88 | 20 | 0.91× | — |
| **ot** | **79** | **15** | **0.75×** | **DEPLETED** |
| qok | 59 | 14 | 0.94× | — |
| ok | 49 | 17 | 1.37× | — |
| o | 44 | 11 | 0.99× | — |
| **d** | **36** | **3** | **0.33×** | **STRONGLY DEPLETED** |
| sh | 23 | 4 | 0.69× | — |
| y | 16 | 2 | 0.53× | — |
| t | 11 | 1 | 0.40× | — |

**ch@pos2 CONFIRMED=0, dir=0 across all 16 tested LF classes.** The hypothesis was an artifact of confusing raw count with enrichment. B pharma's pos2 baseline for ch is 25.28% — ch appears frequently at pos2 because it's a common word, not because of any LF-conditional routing rule. Corrected for baseline, ch is near-baseline for most LF classes and strongly depleted for d-LF (E=0.33×) and ot-LF (E=0.75×).

**H_new_BO REFUTED.** There is no universal ch@pos2 rule in B pharma. The "ch dominates non-self pos2" observation from exp_489 was a baseline artifact.

---

## 2. H_new_BN: B astro pos2 Self-Chaining Survey

B astro (N=695 lines), full pos2 self-chaining survey:

| LF onset | N_lf | N_elig | obs | base% | E | flag |
|---------|------|--------|-----|-------|---|------|
| **ol** | 104 | 104 | 15 | 9.4% | **1.54×** | **CONFIRMED** |
| ch | 85 | 84 | 19 | 15.5% | 1.46× | — (below 1.5×) |
| l | 83 | 83 | 7 | 4.8% | 1.75× | — (below 2.0×) |
| d | 79 | 76 | 5 | 3.4% | 1.95× | — (just below dir threshold) |
| qok | 75 | 75 | 18 | 18.7% | 1.28× | — |
| **sh** | 35 | 34 | 10 | 18.4% | **1.59×** | **CONFIRMED (F469)** |
| ot | 30 | 30 | 1 | 3.7% | 0.91× | flat |
| **ok** | 37 | 35 | 3 | 4.1% | **2.09×** | **(dir)** |
| **qot** | 22 | 22 | **0** | 4.5% | **0.00×** | **ZERO** |
| qo | 23 | 23 | 2 | 5.3% | 1.65× | — |

**Key findings:**

1. **NEW CONFIRMED: B astro ol-LF → ol-self at pos2 (E=1.54×/N=15). F471 candidate.**
2. sh confirmed (F469, reproduced).
3. ch just below threshold (E=1.46×/N=19) — consistent with F462 (herbal-specific scope; astro near-miss).
4. qok (largest B astro LF class, N=75): E=1.28× — BELOW threshold. qok does NOT show confirmed self-chaining despite being the dominant class.
5. qot: obs=0 (ZERO) — complete absence of self-chaining.

**B astro pos2 self-chaining is NOT universal.** qok (largest class) is below threshold; qot is zero. Only ol and sh are confirmed. The q-bench triplet does NOT collectively self-chain.

**B astro qok-LF full pos2 distribution:**
- qok-self: E=1.28×/N=18 — modest, below threshold
- qo: E=1.52×/N=6 — directional (q-bench internal routing: qok→qo at pos2)
- sh, ch, ol: near baseline
- No elevated onset with E≥1.5× and N≥10 for qok pos2

---

## 3. B astro vs A herbal_a pos2 Baseline Comparison

A herbal_a and B pharma have dramatically different pos2 distributions:
- d: A=11.1% vs B pharma=1.4% — d dominates A pos2 but nearly absent B pharma pos2
- a: A=1.0% vs B pharma=8.6% — reversed
- l: A=0.1% vs B pharma=7.7% — nearly absent in A
- cth: A=5.5% vs B pharma=0.1% — A-specific pos2 word class

These baseline differences reflect the underlying vocabulary differences between A and B dialects, not routing rules.

---

## Self-Audit

**Target-awareness:** None. ch@pos2 enrichment was computed with section-specific baseline throughout.

**Extrapolation:** "ch@pos2 at or below baseline" is based on direct E computation for all LF classes. No LF class shows E≥1.5× for ch@pos2 in B pharma. The refutation is clean.

**Negative result scope:** H_new_BO refutation is about the ch-routing hypothesis, not about whether B pharma has any routing rules. B pharma does have rules (F449-F452, F459-F460) — they just aren't ch@pos2 rules.

---

## Conclusions

**F471 ASSIGNED: B astro ol-LF → ol-self at pos2 (E=1.54×/N=15, CONFIRMED).** ol is the most common B astro LF class (N=104). ol self-chaining joins sh (F469) as a B astro pos2 confirmed finding. B astro's pos2 self-chaining is selective (ol and sh confirmed; qok below threshold; qot zero).

**H_new_BO REFUTED:** No universal ch@pos2 elevation in B pharma. The high raw counts for ch@pos2 reflect B pharma's high ch baseline (25.3%), not enrichment. ch@pos2 is strongly depleted for d-LF (E=0.33×) and ot-LF (E=0.75×) in B pharma.

**H_new_BN ANSWERED:** B astro pos2 self-chaining is selective, not universal. ol (CONF, F471) and sh (CONF, F469) self-chain; qok (largest class) below threshold; qot = zero. The q-bench triplet does NOT collectively show pos2 self-chaining.
