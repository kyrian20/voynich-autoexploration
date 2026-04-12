# exp_566 result — ch-onset full characterization (H_new_GD)

## Audit

**Target-awareness**: None. Standard methodology.

**Feature-destroying implementation**: None. ch onset correctly placed after cth/ckh/cph in ONSET_PRIORITY — words starting with "cth", "ckh", "cph" are captured by higher-priority onsets. ch captures all remaining ch-starting words. Verified: chol, chey correctly get onset ch; cthy would get onset cth (correct).

**Extrapolation**: None. ch→d A: E=1.46×/238 — correctly labeled sub-CONF (E<1.5×, below threshold). B ch→d: 1.45×/107 — similarly sub-CONF. A qo@LL in ch-LF: E=1.66×/12 — CONF (E≥1.5, obs=12≥10). B ch→l: E=1.56×/135 — CONF. B ch→t: E=1.67×/35 — CONF. Ch-LF pos1: no flags assigned (all below thresholds). 

**Note on dual-perspective sh↔ch**: sh→ch outgoing (exp_564, MID baseline) gives E=0.65×/0.54×; ch incoming sh→ch (exp_566, overall baseline) gives 0.74×/0.60×. Both confirm DEPL direction; exp_564's MID-baseline measure is the definitive outgoing bigram result. No contradiction.

---

## Results

### Part 1: ch vocabulary

**A herbal_a** (2242 tokens = 19.79% of 11,327): **MOST FREQUENT onset class in A**
- chol: 243 (10.8%), chey: 137 (6.1%), chor: 130 (5.8%), chy: 74 (3.3%), cheey: 74 (3.3%)
- **457 unique types** — second-highest diversity after sh (236) due to extremely high frequency
- Body: l-body (chol), y-body (chey, cheey, chy), r-body (chor), compound forms (chckhy, chcthy)

**B all** (1695 tokens = 16.68% of 10,163):
- **chedy: 376 (22.2%)** — edy-dominant in B. chey(6.8%), cheey(3.5%), chckhy(3.5%)
- 337 unique types
- A→B vocabulary shift: A=diverse → B=chedy-convergent

**Frequency DROPS A→B** (19.79%→16.68%) — a moderate drop (~1.2×). Unlike qok (doubles), sh/qo (increases), and stable classes; ch slightly decreases. Ch is the dominant class in A but slightly less dominant in B.

### Part 2: ch positional

| Position | A obs | A E | flag | B obs | B E | flag |
|----------|-------|-----|------|-------|-----|------|
| MID base | 1715/7333 | 23.39% | — | 1448/7601 | 19.05% | — |
| **pos1** | **154/2033** | **0.32×** | **DEPL** | **53/1283** | **0.22×** | **DEPL** |
| LL | 445/1961 | 0.97× | — | 224/1279 | 0.92× | — |
| LF | 373/1961 | 0.81× | — | 194/1279 | 0.80× | — |

**A ch**: pos1 EXTREME DEPL (0.32×/154 — robust, obs=154>>3); LL near-flat (0.97×/445); LF sub-baseline (0.81×/373, NOT DEPL).

**B ch**: pos1 EXTREME DEPL (0.22×/53 — the MOST EXTREME pos1 DEPL characterized in B); LL near-flat (0.92×/224); LF sub-baseline (0.80×/194, NOT DEPL).

**Cross-dialectal pattern**: Ch pos1 is extremely depleted in both dialects (A:0.32×; B:0.22×). LF is sub-baseline in both (0.80-0.81×) but NOT formally DEPL (E>0.70). LL is near-flat. Ch is a MID class: it occupies interior positions but avoids line openings and is mildly sub-baseline at line endings.

**Updated pos1-avoider ranking by E-value**: B k(near-zero obs=4 from prior data) > B ch(0.22×/53) > A a(0.16×/14) > B a(0.26×/12) > A k(0.52×/32) > A ch(0.32×/154). With robust obs, B ch (0.22×/53) is the most reliably extreme pos1-avoider characterized in B.

### Part 3: ch bigrams

**A herbal_a** (sender=1861, receiver=2088):

| Pair | obs | exp | E | flag |
|------|-----|-----|---|------|
| ch→ch | 453 | 435.2 | 1.04× | — |
| ch→d | 238 | 162.9 | 1.46× | — *(sub-CONF)* |
| **ch→sh** | **117** | **176.1** | **0.66×** | **DEPL** |
| ch→l | 57 | 40.6 | 1.40× | — *(sub-CONF)* |
| ch→cth | 68 | 52.8 | 1.29× | — |
| ch→k | 86 | 67.3 | 1.28× | — |

Top incoming (overall baseline): no CONF signals. qok→ch: 1.22×/186; sh→ch: 0.74×/127 (near-DEPL but above threshold).

**ch-LF LL-analysis (A)**: **qo@LL CONF** (E=1.66×/12, obs≥10 ✓) in ch-LF lines; **sh@LL DEPL** (0.62×/17, E<0.70, obs≥3) — [qo@LL][ch@LF] is a terminal pair enriched in A (parallel to [c-gallows@LL][d@LF] in F611).

**B all** (sender=1501, receiver=1642):

| Pair | obs | exp | E | flag |
|------|-----|-----|---|------|
| **ch→l** | **135** | **86.3** | **1.56×** | **CONF** |
| **ch→t** | **35** | **20.9** | **1.67×** | **CONF** |
| ch→d | 107 | 73.7 | 1.45× | — *(sub-CONF)* |
| **ch→sh** | **86** | **162.3** | **0.53×** | **DEPL** |
| sh→ch | 92 | 154.1 | 0.60× | **DEPL** |

**ch-LF pos1 grammar**: FLAT in both A (373 lines) and B (194 lines) — no CONF opener preference for ch-terminal lines.

**ch-LF LL-analysis (B)**: No CONF signals. Near-flat for all classes.

---

## New Findings

**F623: ch bigrams** — CROSS-DIALECTAL: ch→sh DEPL (A:0.66×/117; B:0.53×/86); ch→d sub-CONF near-threshold (A:1.46×/238; B:1.45×/107). B-SPECIFIC: ch→l CONF(1.56×/135); ch→t CONF(1.67×/35). A-SPECIFIC: A ch-LF qo@LL CONF(1.66×/12); A ch-LF sh@LL DEPL(0.62×/17). Ch-LF pos1 grammar: FLAT both dialects (no CONF opener preference). No CONF incoming routes to ch in either dialect (qok→ch A:1.22×/186; B:1.22×/302 — both sub-CONF).
**Experiment:** exp_566 (2026-04-11)
**Date:** 2026-04-11
**Commitment status:** Not committed.
**Magnitude context:** Ch→sh DEPL cross-dialectally (A:0.66×/117; B:0.53×/86) is symmetric to sh→ch DEPL from F617 — the mutual avoidance between ch and sh is confirmed from both directions. Ch→d sub-CONF (A:1.46×; B:1.45×) is consistently just below threshold across both dialects and large obs — the near-threshold consistency suggests a real but weak routing tendency from ch to d. B ch→l CONF (1.56×/135) extends the B terminal routing: ch routes to l (the second-strongest B LF class, F585). B ch→t CONF (1.67×/35): ch routes to t (an OPENER); this likely represents ch appearing in MID positions immediately before a re-opener at the next line or within specific B constructions. A [qo@LL][ch@LF] terminal pair (1.66×/12 CONF) mirrors the A [c-gallows@LL][d@LF] enrichment from F611 — A lines ending in ch tend to have qo at LL.

## F622: ch positional — A pos1 EXTREME DEPL (0.32×/154 CONF); B pos1 EXTREME DEPL (0.22×/53 CONF — most extreme reliable B pos1-avoider); LF sub-baseline (A:0.81×/373; B:0.80×/194 — NOT DEPL); LL near-flat both. Ch is a MID class with extreme pos1 avoidance. LF sub-baseline (NOT DEPL) distinguishes ch from sh (which is LF DEPL).
**Experiment:** exp_566 (2026-04-11)
**Date:** 2026-04-11
**Commitment status:** Not committed.
**Magnitude context:** B ch pos1=0.22×/53 is the most statistically reliable extreme pos1-avoider in B (large obs=53 confirms E=0.22×). Working_position.md previously listed B ch pos1=0.25× — now corrected to 0.22×. Ch's LF sub-baseline (0.80-0.81×) is distinct from sh's LF DEPL (0.47×/0.39×): ch is less extreme at LF than sh. Ch is a broader MID class that spreads across MID/LL/LF sub-positions without strong avoidance of LF specifically (only pos1 avoided). This places ch as a true MID class with no terminal-avoidance behavior, whereas sh has strong terminal-avoidance.

## F621: ch vocabulary — A: 2242 tokens (19.79%); MOST FREQUENT onset class in A; 457 types; chol(10.8%), chey(6.1%), chor(5.8%); diverse l/y/r-body mix. B: 1695 tokens (16.68%); chedy dominant (22.2%); 337 types. Frequency DROPS A→B (19.79%→16.68%). A→B shift: A=diverse → B=chedy-convergent.
**Experiment:** exp_566 (2026-04-11)
**Date:** 2026-04-11
**Commitment status:** Not committed.
**Magnitude context:** Ch is the most frequent onset class in A (19.79% of all A words are ch-onset). In B, it drops slightly (16.68%) — one of the few classes that DECREASES from A to B (qok doubles; sh/qo increase; s/t/y stable; ch decreases by ~1.2×). The B chedy dominance (22.2%) is the highest single-word fraction for any class. Ch vocabulary diversity (457 types in A) reflects its extremely high frequency. The frequency drop A→B (19.79%→16.68%) is mild compared to cth (8.6×) or compound gallows (6×) drops — ch is a structurally stable class across dialects.

---

## Summary

- **H_new_GD CLOSED**: ch fully characterized.
- Vocabulary: A=19.79%/457types (most frequent class); diverse; chol/chey/chor top. B=16.68%/337types; chedy dominant (22.2%). Frequency drops mildly A→B (F621).
- Positional: pos1 EXTREME DEPL (A:0.32×/154; B:0.22×/53 — most extreme B pos1-avoider); LF sub-baseline NOT DEPL both (0.80-0.81×); LL near-flat. Ch is a MID class (F622).
- Bigrams: **ch→sh DEPL cross-dialectally** (A:0.66×/117; B:0.53×/86 — mutual avoidance confirmed); ch→d sub-CONF both (1.46×/1.45×); B ch→l CONF(1.56×/135); B ch→t CONF(1.67×/35); A ch-LF [qo@LL][ch@LF] CONF(1.66×/12); ch-LF pos1 FLAT both. No CONF incoming signals (F623).

## Self-Audit

**Target-awareness**: None.

**Feature-destroying implementation**: None. Onset order correct; cth/ckh/cph words correctly captured by higher-priority onsets.

**Extrapolation**: None. ch→d 1.46×/238: correctly NOT labeled CONF (below 1.5×). A qo@LL ch-LF: E=1.66×/12 — CONF (≥1.5, ≥10). B ch→l/t: correctly labeled CONF (obs≥10, E≥1.5). Ch-LF pos1: no CONF signals — not over-interpreted.

**Negative result**: Ch-LF pos1 grammar is FLAT (no enriched opener class). This is in contrast to most other LF classes which have opener preferences (e.g., sh-LF pos1=sh CONF, r-LF pos1=qok CONF, d-LF pos1=qot CONF). Ch-terminal lines have no preferred opener type.
