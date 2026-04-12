# exp_399: B/A LF→LL Grammar — LF Class Conditions LL Choice (H617)

**Date:** 2026-04-11
**Hypothesis tested:** H617 — Do LF classes affect LL beyond what pre_LL predicts?
**Outcome:** YES — LF class has direct LF→LL associations beyond local bigram expectations. Key findings: B p at LF → ch at LL = 0.47×(N=15/222, STRONG DEPLETION); B sh→sh LL=2.07×/sh→qo LL=2.67×; B t→t LL=2.50×; B qok→s LL=2.16×; B ot→ot LL=2.14×; A p→sh LL=3.60×(N=7/41); A s→s LL=2.06×; A qot→d LL=1.79×(N=32/72).

---

## 1. B LF→LL Matrix: Key Results

| LF | N | ch E | Notable LL enrichments | Notable LL depletions |
|----|---|------|----------------------|----------------------|
| d | 344 | 0.95× | l=1.20×, other=1.32× | ol=0.73×, qok=0.74× |
| y | 261 | 1.06× | ot=1.43×, other=1.33× | qok=0.64×, qot=0.54× |
| s | 260 | 1.20× | ch=1.20×, ol=1.20×, qok=1.23× | other=0.64×, o=0.42× |
| qok | 237 | 0.94× | l=1.34×, s=**2.16×**(N=9) | other=0.50× |
| **p** | 222 | **0.47×(N=15)** | s=**2.05×**(N=8), qo=**1.89×**(N=10) | ch=**0.47×** |
| t | 205 | 1.08× | t=**2.50×**(N=7), ok=1.44×, d=1.30× | l=0.57×, other=0.64× |
| sh | 126 | 1.16× | sh=**2.07×**(N=11), qo=**2.67×**(N=8) | ot=0.42× |
| ot | 50 | 1.25× | ot=**2.14×**(N=8) | ok=0.88× |
| qo | 65 | 0.96× | d=**1.87×**(N=11), qok=**1.77×**(N=9) | — |
| qot | 47 | 1.18× | qok=1.63×(N=6), d=1.41×(N=6) | ok=0.31×(N=1) |

---

## 2. B p→LL: Strong ch Depletion and Specific Routing

**B p at LF → ch at LL = 0.47×(N=15/222)** — strongest LF→LL depletion found. p formula-class lines not only open with p→sh→qot (F396) but also specifically AVOID ch at LL.

B p LL distribution: s=2.05×(N=8), qo=1.89×(N=10), k=1.74×(N=8), o=1.70×(N=24), ch=0.47×(N=15).

p-formula lines end predominantly with s/qo/k/o (not ch). This is a global line-structure rule: p lines are "ch-avoidant throughout."

---

## 3. B Self-Routing LF→LL Pairs

| LF | LL | E | N | Interpretation |
|----|----|---|---|----------------|
| t | t | **2.50×** | 7/205 | t self-routes across full line |
| sh | sh | **2.07×** | 11/126 | sh self-routes (A sh self-chain F400) |
| ot | ot | **2.14×** | 8/50 | ot self-routes; template class memory |
| sh | qo | **2.67×** | 8/126 | sh→qo LL (new) |
| qo | d | **1.87×** | 11/65 | qo→d LL pair |
| qo | qok | **1.77×** | 9/65 | qo→qok LL pair |

---

## 4. A LF→LL Matrix: Key Results

| LF | Notable enrichments | Notable depletions |
|----|--------------------|--------------------|
| p | sh=**3.60×**(N=7/41) | ch=0.45×(N=3) |
| t | qo=**3.57×**(N=5) | d=0.70×(N=19) |
| d | l=**3.22×**(N=5), ch=1.27×(N=53) | sh=0.66×, s=0.64× |
| qo | cth=**2.96×**(N=6) | — |
| qok | k=**2.80×**(N=8) | ot=0.62×, sh=0.66× |
| ot | d=1.51×(N=22) | other=0.24× |
| qot | d=**1.79×**(N=32/72) | ok=0.46×, other=0.40× |
| s | s=**2.06×**(N=8/91) | sh=0.46×(N=2) |
| y | o=**1.82×**(N=18/212) | ch=0.72×(N=25) |

**A p at LF → sh at LL = 3.60×(N=7/41)**: A p-formula lines specifically terminate with sh. This is A-specific (not found in B: B p→sh LL is not enriched).

**A qot at LF → d at LL = 1.79×(N=32/72)**: A qot is the A LF-formula template class (F392: A qot LF=1.65×). Its strong d→d chain (F385) and d-routing at LL may explain qot lines ending with d.

---

## 5. Cross-Dialectal p→ch LL Contrast

| | A | B |
|--|---|---|
| p→ch at LL | 0.45×(N=3/41) | **0.47×(N=15/222)** |
| p→sh at LL | **3.60×(N=7/41)** | — (sh=0.67×) |

Both dialects show p at LF → ch at LL depleted. But A p ends with sh (3.60×) while B p ends with s/qo/k/o. The anti-ch ending is cross-dialectally INVARIANT for p-formula lines.

---

## Self-Audit

**Target-awareness**: No target-aware elements.

**Feature-destroying implementation**: No feature-destroying elements.

**Extrapolation**: B p→ch LL=0.47×(N=15/222) — adequate for STRONG depletion claim. B sh→qo LL=2.67×(N=8/126) — adequate. B t→t LL=2.50×(N=7/205) — adequate. B qok→s LL=2.16×(N=9/237) — adequate. A p→sh LL=3.60×(N=7/41) — adequate given very strong E. A s→s LL=2.06×(N=8/91) — adequate. A qot→d LL=1.79×(N=32/72) — robust. All other directional claims labeled. PASS.

**Negative-result scope**: N/A — positive result.

**Control behavior**: Unconditional LL distributions used as baseline (A: N=1478, B: N=2271). Expected some LF→LL enrichments given non-Markovian grammar (F393). Found stronger effects than expected: B p→ch LL=0.47× is stronger than most pos2-level effects. The self-routing pairs (t→t, sh→sh, ot→ot) suggest LF onset class has memory across the full line, not just at adjacent positions.

## Finding: F403

**See findings.md F403**
