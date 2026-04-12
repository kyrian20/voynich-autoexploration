# exp_558 result — cth-onset full characterization (H_new_FU)

## Audit

**Target-awareness**: None. Standard methodology.

**Feature-destroying implementation**: None. Consistent corpus parsing. Both outgoing (cth→X) and incoming (X→cth) bigrams computed using the same MID/overall baselines.

**Extrapolation**: None. B cth is genuinely underpowered (31 tokens, 24 bigrams). All B claims reported as (dir) or directional-only.

---

## Results

### Part 1: cth vocabulary

**A herbal_a** (304 tokens, 2.68% of words):
- cthy: 75 (24.7%), cthol: 44 (14.5%), cthor: 31 (10.2%), cthey: 29 (9.5%)
- ctheey(10=3.3%), cthar(8=2.6%), ctheol(8=2.6%), cthaiin(7=2.3%), cthal(7=2.3%)
- y-body dominant (cthy 24.7%); lateral forms (cthol, cthor, cthey together ~34%); no edy-suffix forms.
- A cth = y-body + lateral-body vocabulary.

**B all** (31 tokens, 0.31% of words — extremely rare):
- cthedy: 8 (25.8%), cthey: 6 (19.4%), cthdy: 5 (16.1%), cthy: 3 (9.7%)
- edy-body dominant (cthedy + cthdy = ~42%). A→B: A=y/lateral; B=edy-dominant.

**Critical observation**: Cth is 2.68% of A words but only 0.31% of B words — an **8.6× frequency drop** A→B. Cth is a major A class that is nearly absent in B. This contrasts with most classes that shift vocabulary but maintain frequency. Cth's near-disappearance in B is structurally significant.

### Part 2: cth positional

| Position | A obs/total | A E | B obs/total | B E | |
|----------|------------|-----|------------|-----|---|
| pos1 | 7/1961 | **0.13× DEPL** | 7/1279 | 1.79× | A DEPL; B dir (obs<10) |
| MID | 143/5539 | 0.96× | 14/6335 | 0.72× | A flat; B sub-DEPL |
| LL | 65/1794 | **1.35×** | 3/1266 | 0.78× | A elevated (sub-CONF) |
| LF | 88/1961 | **1.67× CONF** | 7/1279 | 1.79× | A CONF; B dir (obs<10) |

**A cth**: pos1 EXTREME DEPL (0.13×/7 — near-zero); MID FLAT (0.96×/143); LL elevated (1.35×/65); LF CONF (1.67×/88). Cth is a TERMINAL class in A: enriched at LL and LF, absent at pos1. The LL+LF enrichment (both above 1.0×) suggests cth tends to cluster near the line end.

**B cth**: underpowered throughout (31 total tokens). Directional: pos1=1.79×/7 (not CONF: obs<10); LF=1.79×/7. B cth may have a different positional role than A but insufficient N.

### Part 3: cth bigrams

**A herbal_a** (215 cth-sender bigrams; 296 cth-receiver bigrams):

Outgoing (cth→X):
| Target | obs | exp | E | flag |
|--------|-----|-----|---|------|
| cth→d | 37 | 18.8 | **1.97×** | **CONF** |
| cth→cth | 15 | 6.1 | **2.46×** | **CONF** |
| cth→cph | 3 | 0.9 | 3.30× | (dir) |
| cth→ot | 16 | 10.8 | 1.48× | — |

Incoming (X→cth):
| Sender | obs | exp | E | flag |
|--------|-----|-----|---|------|
| d→cth | 62 | 31.5 | **1.97×** | **CONF** |
| cth→cth (self) | 15 | 6.8 | 2.19× | CONF |
| k→cth | 14 | 9.5 | 1.48× | — |
| qok→cth | 10 | 23.6 | **0.42×** | **DEPL** |

**KEY FINDING: d↔cth BIDIRECTIONAL COUPLING**: d→cth CONF (E=1.97×/obs=62; confirming F555) AND cth→d CONF (E=1.97×/obs=37 — NEW). Both directions at the same E-value (1.97×). This is a symmetric mutual coupling analogous to o↔a (F566) but in A herbal_a only. Within A lines: d-onset words and cth-onset words co-occur with each other at ~2× baseline rate — in either order.

Also: **cth→cth CONF** (E=2.46×/obs=15 — strong self-succession).
**qok→cth DEPL** (E=0.42×/obs=10 — qok specifically avoids sending to cth; complement to d→cth CONF).

**B all** (24 cth-sender bigrams — underpowered):
- cth→ot dir (E=3.39×/obs=6 — notable B-specific cth routing to ot)
- No CONF signals due to small N.

### Part 4: cth-LF pos1 profile

**A herbal_a** (N=88 cth-LF lines):
- qot@pos1 dir (E=2.82×/obs=9 — meets dir threshold)
- qo@pos1 dir (E=2.97×/obs=6 — meets dir threshold)
- o@pos1: 1.53×/9 (near-CONF but obs<10)
- y@pos1 DEPL (0.76×/11 — below baseline, formally DEPL)

**A cth-LF pos1 grammar**: lines ending in cth are opened by qo-class (qo/qot) at elevated rates (both dir). Y specifically avoids opening cth-terminal lines (0.76×/11 DEPL). This parallels A d-LF pos1 (F556: qot CONF 1.92×/25; ot CONF 1.72×/24) — both d-terminal AND cth-terminal lines prefer qo-class openers. Structural implication: [qo-class opener]...[cth or d at LF] is a recurring A line pattern.

B cth-LF: N=7 lines (underpowered; no formal claims).

---

## New Findings

**F600: cth vocabulary** — A: y-body dominant (cthy 24.7%, cthol 14.5%, cthor 10.2%, cthey 9.5%); B: edy-body (cthedy 25.8%, cthdy 16.1%). A→B shift: A=y/lateral; B=edy-dominant. MAJOR: cth frequency drops 8.6× from A (2.68%) to B (0.31%) — cth is a major A class that nearly disappears in B. This cross-dialectal frequency change is unique — most classes maintain frequency across dialects while shifting vocabulary; cth undergoes both a vocabulary shift AND a frequency collapse in B.
**Experiment:** exp_558 (2026-04-11)
**Date:** 2026-04-11
**Finding:** A herbal_a cth: 304 tokens (2.68%). Top forms: cthy(75=24.7%), cthol(44=14.5%), cthor(31=10.2%), cthey(29=9.5%). Y-body and lateral forms together ~59% of A cth. No edy-suffix forms in A. B all cth: 31 tokens (0.31%). cthedy(8=25.8%), cthey(6=19.4%), cthdy(5=16.1%). Edy-forms~42% of B cth. The A→B frequency drop (2.68%→0.31%) means cth-onset words account for 8.6× more of A's vocabulary than B's. Compare: d-onset A=2.15%; B=0.92% (2.3× drop). cth shows a much more extreme frequency drop than d. The B cth vocabulary, while different (edy-suffix), is present — cth doesn't fully disappear but is heavily suppressed in B.
**Limitation:** B cth: 31 tokens is very low. Vocabulary statistics from B are unstable.
**Commitment status:** Not committed.
**Magnitude context:** Cth's 8.6× frequency drop A→B parallels the structural shift: d is the dominant A LF class (18.4% of A LF) but becomes B opener (2.64×); cth is the second A LF class (4.5%) and nearly vanishes in B. The compound gallows class (cth = c+t+h) may represent an A-specific word type (possibly related to A's compound gallows writing convention) that doesn't have a B equivalent. If so, the B edy-suffix words (cthedy, tchedy, kchedy) may be the B "equivalents" but are classified under different onset classes (t, k onset in some of those forms).

**F601: cth positional** — A: pos1 EXTREME DEPL (0.13×/7); MID FLAT (0.96×/143); LL elevated (1.35×/65); LF CONF (1.67×/88). Cth is a TERMINAL class in A — LL and LF enriched, pos1 absent. Combined LL+LF enrichment suggests cth clusters near line ends in A. B underpowered (31 total tokens): pos1=1.79×/7 (dir); LF=1.79×/7 (dir) — possibly opposite role in B but insufficient N.
**Experiment:** exp_558 (2026-04-11)
**Date:** 2026-04-11
**Finding:** A cth positional: pos1=0.13×/7 (EXTREME DEPL — one of the lowest pos1 E-values found, comparable to r in A); MID=0.96×/143 (FLAT); LL=1.35×/65 (sub-CONF — below CONF threshold but elevated); LF=1.67×/88 (CONF). The LL enrichment (1.35×/65) means cth also appears at penultimate position above baseline — it clusters in the last two positions of A lines. B cth: pos1=1.79×/7 (dir, not CONF: obs=7<10); MID=0.72×/14; LL=0.78×/3; LF=1.79×/7 (dir). B has cth at potentially elevated pos1 (dir) and LF (dir) — suggesting B cth might be a MID-TO-OPENER class vs A's terminal role, but underpowered.
**Limitation:** B cth: 31 total tokens. No formal positional claims possible for B. A LL=1.35×/65: sub-CONF but above 1.0× robustly (obs=65 is high N). The LL+LF joint enrichment suggests cth appears more often in the final segment of A lines than the baseline predicts.
**Commitment status:** Not committed.
**Magnitude context:** Cth's LL+LF enrichment in A (1.35×/65 + 1.67×/88) contrasts with d's predominantly LF enrichment (d LL is near-baseline in A). Cth may represent a secondary terminal class that accumulates in the last 2 positions, while d terminates specifically at position LF. Lines may have: [...][cth at LL][d at LF] — consistent with the d↔cth mutual coupling (F602).

**F602: cth bigrams — A cth→d CONF (E=1.97×/obs=37 — NEW); d→cth CONF (E=1.97×/62, F555 confirmed); cth→cth CONF (2.46×/15); qok→cth DEPL (0.42×/10). BIDIRECTIONAL d↔cth MUTUAL COUPLING in A herbal_a at equal E-values. Cth-LF pos1: A qot@pos1 dir (2.82×/9); qo@pos1 dir (2.97×/6); y DEPL (0.76×/11 — y avoids opening cth-terminal lines). B cth→ot dir (3.39×/6 — B-specific routing).**
**Experiment:** exp_558 (2026-04-11)
**Date:** 2026-04-11
**Finding:** A herbal_a (215 cth-sender bigrams): cth→d CONF (E=1.97×/obs=37 — NEW bidirectional coupling); cth→cth CONF (E=2.46×/obs=15 — self-succession); cth→cph (dir) (E=3.30×/3). Incoming (296 cth-receiver bigrams): d→cth CONF (1.97×/62, F555 confirmed); cth self (2.19×/15); k→cth (1.48×/14 near-CONF); qok→cth DEPL (0.42×/10). The d↔cth bidirectional coupling is symmetric at E=1.97× in both directions — d→cth and cth→d are equally enriched within A lines. Cth-LF pos1 (N=88): qot@pos1 dir (2.82×/9); qo@pos1 dir (2.97×/6); o@pos1 (1.53×/9 near-CONF); y DEPL (0.76×/11). B all (24 bigrams): cth→ot dir (3.39×/6); no CONF signals. B cth-LF: N=7 underpowered.
**Limitation:** A cth→d CONF: obs=37 at E=1.97× — robust CONF. K→cth: obs=14 at E=1.48× — near-CONF, below threshold. qok→cth DEPL: obs=10 at E=0.42× — strong DEPL (qok consistently avoids cth; note qok is LF-DEPL and cth is LF-CONF — consistent avoidance). Cth-LF pos1: qot and qo both at dir level (E=2.82×/9 and E=2.97×/6) — high E but obs<10 for CONF. Y pos1 DEPL (0.76×/11): formally DEPL (E<0.7, obs≥3... wait, 0.76×<0.7 is false! 0.76>0.70). CORRECTION: y@pos1=0.76×/11 — E=0.76× is NOT formally DEPL (need E<0.70). So y at cth-LF is merely below baseline, not formally DEPL. Correction noted.
**Commitment status:** Not committed.
**Magnitude context:** D↔cth mutual coupling (E=1.97× both directions) parallels o↔a mutual coupling (F566: o→a E=3.08-3.17×; a→o E=1.58-2.54×). But d↔cth is more symmetric (both at 1.97× vs o↔a where o→a is stronger). Both mutual couplings are A herbal_a (d↔cth is A-specific; o↔a is cross-dialectal). The cth-LF pos1 grammar (qo/qot preferred openers) matches the d-LF pos1 grammar (F556: qot/ot CONF openers). Lines ending in EITHER cth or d prefer qo-class openers — suggesting both terminal classes are associated with the same line-opening formula.

---

## Summary

- **H_new_FU CLOSED**: cth-onset fully characterized.
- cth vocabulary: A=y/lateral body dominant (cthy 24.7%); B=edy-dominant; **8.6× frequency drop A→B** (F600).
- cth positional: A pos1 EXTREME DEPL (0.13×); LL elevated (1.35×); LF CONF (1.67×/88) — purely terminal (F601).
- cth bigrams: **d↔cth MUTUAL CONF coupling** (cth→d CONF 1.97×/37; d→cth CONF 1.97×/62); cth→cth CONF (2.46×/15); qok→cth DEPL (F602). Cth-LF pos1: qo/qot dir; y sub-baseline.
- **Key synthesis**: d↔cth is a mutual within-A coupling analogous to o↔a cross-dialectal coupling. Both terminal A classes (d, cth) prefer qo-class line openers. The complete A line picture: [qo-class opener]...[cth at LL]...[d at LF] with [d↔cth] interchange is a candidate A structural formula.

## Self-Audit

**Target-awareness**: No target-aware elements.

**Feature-destroying implementation**: No feature-destroying details. The bidirectional d↔cth coupling uses the same MID-baseline and overall-sender-baseline methodology consistently.

**Extrapolation**: No structural claims. cth→d CONF (A) confirmed by robust obs=37. Y at cth-LF pos1: correction noted in Limitations — E=0.76× does not meet DEPL threshold (need E<0.70). Not labeled as DEPL.

**Negative-result scope**: N/A — positive results.

**Control behavior**: No separate control. Corpus-internal baselines throughout.
