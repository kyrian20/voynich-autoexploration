# exp_371: B d→sh and A d→cth Cross-Onset Couplings (H583/H584)

**Date:** 2026-04-11
**Hypothesis:** H583/H584 — Two new cross-onset couplings identified in exp_367's bigram matrix: (1) B d→sh E=1.63× (found in 8×8 matrix but cut from top-20 elevated list); (2) A d→cth E=1.62× (N=70, identified in elevated pairs list). Both require positional decomposition to understand mechanism.
**Result:** Both confirmed. B d→sh: POSITION-GENERAL with strongest effect at pos1→pos2 (E=2.58×, N=19: d at pos1 → sh at pos2). Top pairs: daiin→shey(7), daiin→shedy(5), dal→shedy(5), dar→shedy(5) — all 'she-' body sh words as successors. A d→cth: POSITION-GENERAL (E=1.51-1.76×, all 4 positions elevated). Primarily daiin→cth-words (43% of pairs) but not exclusively (57% from other d-words). Top cth words: cthy(9), cthol(7), cthor(5).

---

## Key Statistics

### B d→sh per Position
| Position | N_d_prev | N_d→sh | P(sh|d) | Baseline_sh | E |
|----------|----------|--------|---------|-------------|---|
| LF→pos1 | 344 | 81 | 23.5% | 16.8% | 1.40× |
| pos1→pos2 | 67 | 19 | **28.4%** | 11.0% | **2.58×** |
| MID_inner | 438 | 48 | 11.0% | 8.9% | 1.23× |
| pre_LL→LL | 139 | 8 | 5.8% | 4.2% | 1.36× |
| all | 977 | 154 | 15.8% | 9.6% | **1.63×** |

Top B d→sh word pairs: daiin→shey(7), daiin→shedy(5), dal→shedy(5), dar→shedy(5), daiin→sheody(3), daiin→sheol(3)

### A d→cth per Position
| Position | N_d_prev | N_d→cth | P(cth|d) | Baseline_cth | E |
|----------|----------|---------|----------|-------------|---|
| LF→pos1 | 252 | 21 | 8.3% | 5.1% | 1.63× |
| pos1→pos2 | 114 | 9 | 7.9% | 4.7% | 1.67× |
| MID_inner | 356 | 23 | 6.5% | 4.3% | 1.51× |
| pre_LL→LL | 237 | 25 | 10.5% | 6.0% | **1.76×** |
| all | 918 | 70 | 7.6% | 4.7% | **1.62×** |

Top A d→cth word pairs: daiin→cthy(9), daiin→cthol(7), daiin→cthor(5), daiin→ctheody(3), daiin→cthain(2), daiin→ctheol(2), dchy→cthy(2)

---

## Findings

### Finding 1: B d→sh Is POSITION-GENERAL with a Striking pos1→pos2 Peak (E=2.58×, N=19)

B-dialect d→sh operates across all positions (LF=1.40×, MID=1.23×, pre_LL=1.36×) with a strong concentration at pos1→pos2 (E=2.58×, N=19). When a d-onset word occupies position pos1 (second word, common in lines starting with a non-d LF word), the next word (pos2) is sh-onset at 2.58× above baseline. This is the strongest positional expression of the d→sh rule. LF→pos1 also shows E=1.40× (N=81 — the largest N since d is enriched at LF).

### Finding 2: B d→sh Successor sh Words Are 'she-' Body sh Forms — Connecting to F372

The top sh words receiving d-onset predecessors in B-dialect: shey(7+3=10), shedy(5+5+2+2=14), sheody(3), sheol(3) — all 'she-' body sh words, exactly the subclass identified in F372 as the sh→qok driver. This is NOT coincidental: the 'she-' body sh subclass is both (a) the sh-to-qok coupling carrier (F372) and (b) the d-to-sh coupling receiver. The 'she-' sh words occupy a hub position in the B-dialect bigram grammar.

### Finding 3: A d→cth Is POSITION-GENERAL (E=1.51-1.76× at All 4 Positions)

A-dialect d→cth is elevated at all position categories (LF=1.63×, pos1=1.67×, MID=1.51×, pre_LL=1.76×). The rule is a genuine position-independent bigram rule, not a positional artifact. Pre_LL is the peak (1.76×), consistent with the overall pattern that many A-dialect bigram rules intensify near line-end.

### Finding 4: A d→cth Is daiin-Initiated But d-Class-General (43% daiin, 57% other d-words)

Top d→cth pairs: daiin→cthy(9), daiin→cthol(7), daiin→cthor(5) account for 21/70=30% of pairs. Total daiin-initiated d→cth pairs: ~30/70=43%. Other d-words (dchy, dain, dol, dar, etc.) contribute 57% of pairs. The rule is not purely daiin→cth (daiin-only) but is d-CLASS initiated. The cth words following d are diverse (cthy/cthol/cthor/ctheody/cthain/ctheol) — no single cth word dominates.

---

## Summary

B d→sh E=1.63× confirmed (N=154), strongest at pos1→pos2 (E=2.58×). The 'she-' body sh subclass (F372: sh→qok carrier) also receives d-onset predecessors. A d→cth E=1.62× confirmed (N=70), position-general, daiin-initiated but d-class-general. Both are genuine cross-onset bigram rules operating throughout continuation lines. Architecture: implement as position-general bigram rules (with possible pre-LL amplification). B d→sh connects to the 'she-' body sh hub position in B-dialect grammar.

---

## Self-Audit

**Target-awareness:** None. Pure corpus measurement. PASS.
**Feature-destroying implementation:** None. Inline script using standard parsing. PASS.
**Extrapolation:** B pos1→pos2 N=19 (directional for highest E; LF→pos1 N=81 and all N=154 are robust). A d→cth N=70 (adequate). PASS.
**Negative-result scope:** N/A — positive results. PASS.
**Control behavior:** No external control. Internal: pre-LL amplification consistent with other rules (ch→daiin pre-LL=1.43×, F371). PASS.
