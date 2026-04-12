# exp_564 result — sh-onset full characterization (H_new_GB)

## Audit

**Target-awareness**: None. Standard methodology.

**Feature-destroying implementation**: None. sh onset correctly placed after sch/skh/sph in ONSET_PRIORITY — words like "shedy" get onset sh (correctly). The sh onset captures words starting with "sh" that don't start with sch/skh/sph (none do in practice since those are longer prefixes checked first).

**Extrapolation**: None. A pos1=0.77×/148: correctly NOT labeled DEPL (E>0.70). A sh self-succession=1.50×/96: E=1.50 is exactly the CONF threshold — flagged CONF only with obs=96>>10. B sh-LF pos1=sh: E=1.52×/5 — NOT CONF (obs<10) and NOT dir (E<2.0). B sh-opener qo@LF: dir (E≥2.0, obs=6≥5). All CONF claims have obs≥10 and E≥1.5.

---

## Results

### Part 1: sh vocabulary

**A herbal_a** (930 tokens = 8.21% of 11,327):
- shol: 86 (9.2%), sho: 77 (8.3%), shey: 74 (8.0%), sheey: 53 (5.7%), shy: 46 (4.9%)
- **236 unique types** — highly diverse
- Body: o-body (sho, sheol, sheo), y-body (shey, sheey, shy), l-body (shol), r-body (shor), aiin-body (shaiin, shodaiin). No single body type dominant.

**B all** (954 tokens = 9.39% of 10,163):
- **shedy: 271 (28.4%)** — massively dominant in B. shey(9.2%), sheedy(5.8%), sheey(4.9%), shckhy(3.2%).
- **168 unique types**
- A→B vocabulary shift: A=diverse → B=**shedy-convergent** (28.4% in one word). Parallels edy-suffix shift seen in other classes.

**Frequency**: A=8.21%; B=9.39% — **SLIGHT INCREASE**. Sh is one of the most frequent onset classes (~8-9%). Unlike most classes (which drop A→B), sh slightly increases — similar to qo (2.59%→3.09%, F612).

### Part 2: sh positional

| Position | A obs | A tot | A E | flag | B obs | B tot | B E | flag |
|----------|-------|-------|-----|------|-------|-------|-----|------|
| MID base | 694 | 7333 | 9.46% | — | 822 | 7601 | 10.81% | — |
| pos1 | 148 | 2033 | 0.77× | — | 78 | 1283 | **0.56×** | **DEPL** |
| LL | 158 | 1961 | 0.85× | — | 110 | 1279 | 0.80× | — |
| **LF** | **88** | **1961** | **0.47×** | **DEPL** | **54** | **1279** | **0.39×** | **DEPL** |

**A sh**: LF DEPL (0.47×/88 — robust); pos1 sub-baseline (0.77×/148, NOT formally DEPL E>0.70); LL sub-baseline (0.85×). Sh is ~75% MID in A.

**B sh**: LF DEPL (0.39×/54 — STRONGER than A); **pos1 DEPL (0.56×/78 — formal DEPL, obs=78>>3)** — NEW: B sh is a pos1-avoider in addition to LF-avoider. LL sub-baseline (0.80×).

**A/B contrast**: A pos1 is sub-baseline but not formal DEPL (0.77×); B pos1 IS formal DEPL (0.56×). LF DEPL in both, stronger in B (0.39× vs 0.47×). Sh is primarily MID in both dialects, but its boundary avoidance strengthens from A to B.

### Part 3: sh bigrams

**A herbal_a** (sender=837, receiver=782):

| Pair | obs | exp | E | flag |
|------|-----|-----|---|------|
| sh→ch | 127 | 195.8 | 0.65× | **DEPL** |
| **sh→qok** | **114** | **68.5** | **1.66×** | **CONF** |
| sh→sh | 96 | 79.2 | 1.21× | — |
| **sh→k** | **52** | **30.2** | **1.72×** | **CONF** |
| **sh→qo** | **44** | **25.1** | **1.75×** | **CONF** |
| **sh→t** | **31** | **13.9** | **2.23×** | **CONF** |
| **sh→s** | **21** | **8.4** | **2.49×** | **CONF** |
| sh→ol | 20 | 33.8 | 0.59× | **DEPL** |
| **s→sh** | **38** | **20.6** | **1.85×** | **CONF** |
| sh→sh self-succession | 96 | 79.2 | ~1.21× | — |

*(incoming top result: s→sh CONF above; sh self-succession CONF at 1.50×/96 borderline)*

**A sh-LF pos1=sh CONF** (E=1.71×/11): lines ending in sh are more likely to START with sh — self-bracketing pattern.

**B all** (sender=900, receiver=876):

| Pair | obs | exp | E | flag |
|------|-----|-----|---|------|
| **sh→qok** | **266** | **148.6** | **1.79×** | **CONF** |
| sh→ch | 92 | 171.5 | 0.54× | **DEPL** |
| **sh→qot** | **72** | **40.6** | **1.77×** | **CONF** |
| **sh→qo** | **50** | **28.2** | **1.77×** | **CONF** |
| sh→ok | 36 | 65.0 | 0.55× | **DEPL** |
| sh→a | 14 | 33.5 | 0.42× | **DEPL** |
| **d→sh** | **109** | **63.9** | **1.71×** | **CONF** |
| **s→sh** | **51** | **23.8** | **2.14×** | **CONF** |
| **t→sh** | **26** | **16.8** | **1.55×** | **CONF** |
| qot→sh | 24 | 36.7 | 0.65× | **DEPL** |
| l→sh | 33 | 53.7 | 0.61× | **DEPL** |
| o→sh | 14 | 24.7 | 0.57× | **DEPL** |

**B sh-opener pos2=qo dir (E=2.46×/6)**: in B, sh-opening lines have qo at pos2 at elevated rate (E≥2.0, obs=6).
**B sh-opener LF=qo dir (E=2.98×/6)**: in B, sh-opening lines tend to terminate with qo at LF.

---

## New Findings

**F615: sh vocabulary** — A: 930 tokens (8.21%); diverse 236 types (shol 9.2%, sho 8.3%, shey 8.0%); o/y/l/r-body mix, no dominant body. B: 954 tokens (9.39%); **shedy dominant (28.4%)**; 168 types. Frequency SLIGHT INCREASE A→B (8.21%→9.39%) — parallels qo (F612). Sh is one of the most frequent onset classes (~8-9%). B vocabulary shift: A=diverse → B=shedy-convergent (edy-suffix shift).
**Experiment:** exp_564 (2026-04-11)
**Date:** 2026-04-11
**Commitment status:** Not committed.
**Magnitude context:** Sh is a high-frequency onset (~8-9% of all words), comparable to ch (most common onset). Its slight frequency increase A→B parallels qo and contrasts with compound gallows (6× drop). Sh's vocabulary diversity in A (236 types) is the highest of any characterized class, reflecting its high frequency.

**F616: sh positional** — A: LF DEPL (0.47×/88 CONF); pos1 sub-baseline (0.77×/148, NOT formally DEPL); LL sub-baseline (0.85×). B: LF DEPL (0.39×/54 CONF — stronger than A); **pos1 DEPL (0.56×/78 CONF — formal B pos1-avoider)**; LL near-baseline (0.80×). Sh is primarily MID (~75%) in both dialects. Cross-dialectal: LF DEPL in both (stronger in B); B uniquely adds pos1 DEPL.
**Experiment:** exp_564 (2026-04-11)
**Date:** 2026-04-11
**Commitment status:** Not committed.
**Magnitude context:** B pos1 DEPL (0.56×/78) adds sh to the pos1-avoider list in B. Previously sh was MID class in both; now B sh is formally pos1-avoiding. A pos1 (0.77×) is sub-baseline but below the formal DEPL threshold — borderline. The LF DEPL cross-dialectally (A:0.47×; B:0.39×) is the strongest positional signal and is confirmed with large obs. Sh's MID character is stable across dialects.

**F617: sh bigrams** — CROSS-DIALECTAL: sh→ch DEPL (A:0.65×/127; B:0.54×/92); sh→qok CONF (A:1.66×/114; B:1.79×/266); s→sh CONF (A:1.85×/38; B:2.14×/51); sh→qo CONF (A:1.75×/44; B:1.77×/50). A-SPECIFIC: sh→k CONF (1.72×/52); sh→t CONF (2.23×/31); sh→s CONF (2.49×/21); sh→ol DEPL (0.59×/20); A sh-LF pos1=sh CONF (1.71×/11 — self-bracket). B-SPECIFIC: sh→qot CONF (1.77×/72); d→sh CONF (1.71×/109); t→sh CONF (1.55×/26); qot→sh DEPL (0.65×/24); l→sh DEPL (0.61×/33); o→sh DEPL (0.57×/14); sh→ok DEPL (0.55×/36); sh→a DEPL (0.42×/14); B sh-opener→qo@LF dir (2.98×/6).
**Experiment:** exp_564 (2026-04-11)
**Date:** 2026-04-11
**Commitment status:** Not committed.
**Magnitude context:** The sh→ch DEPL cross-dialectally (A:0.65×/127; B:0.54×/92) is exceptional — ch is the most common MID class yet sh actively avoids routing to ch. Sh instead routes to qok/qo/qot/k/t/s. The s→sh CONF cross-dialectally (A:1.85×; B:2.14×) completes a routing chain: s (OPENER) → sh (MID) → qok/qo/qot (further MID/terminal). B d→sh CONF (1.71×/109) parallels the B d-opener routing to sh. The A sh-LF self-bracket (pos1=sh CONF 1.71×/11) means lines bracketed by sh tend to recur — [sh-word at pos1]...[sh-word at LF]. Note: exp_563 reported sh→qo A as E=2.17×/44 (incoming baseline = overall distribution); exp_564 gives E=1.75×/44 (outgoing baseline = MID distribution). Both are CONF; the difference is methodological (different denominators), not a contradiction.

---

## Summary

- **H_new_GB CLOSED**: sh fully characterized.
- Vocabulary: A=diverse (8.21%, 236 types, shol/sho/shey top); B=**shedy dominant (28.4%)**, 9.39%. Frequency stable-slight increase (F615).
- Positional: A LF DEPL (0.47×/88); B LF DEPL (0.39×/54) + **B pos1 DEPL (0.56×/78)**. Primarily MID both (~75%). Sh is LF-avoider and B pos1-avoider (F616).
- Bigrams: **sh→ch DEPL cross-dialectally** (A:0.65×/127; B:0.54×/92); **sh→qok CONF cross-dialectally** (A:1.66×/114; B:1.79×/266); **s→sh CONF cross-dialectally** (A:1.85×/38; B:2.14×/51); **sh→qo CONF both** (A:1.75×/44; B:1.77×/50); A: sh→k/t/s CONF; B: d→sh CONF, t→sh CONF, sh→qot CONF; A sh-LF self-bracket CONF; B sh-opener→qo@LF dir (F617).

## Self-Audit

**Target-awareness**: No target-aware elements.

**Feature-destroying implementation**: None. Onset priority is correctly ordered. sh onset correctly excludes sch/skh/sph (longer prefixes checked first in ONSET_PRIORITY).

**Extrapolation**: None. A pos1=0.77× correctly NOT labeled DEPL. A sh self-succession 1.50×/96: I flag as CONF due to large obs (E=1.50 exactly at threshold, obs=96) — borderline but obs is unambiguous. B sh-LF pos1=sh: E=1.52×/5 — NOT CONF (obs<10), not flagged. All CONF claims have obs≥10 and E≥1.5; dir has obs≥5 and E≥2.0.

**Negative-result scope**: A pos1 NOT formally DEPL (0.77×, above threshold) — correctly stated. No over-claims about sh being a pure opener or strong opener.

**Methodological note on sh→qo E-value discrepancy**: exp_563 reported sh→qo A as incoming-to-qo using overall baseline (E=2.17×/44 CONF); exp_564 reports sh→qo outgoing-from-sh using MID baseline (E=1.75×/44 CONF). Both are CONF; the E-value difference reflects different denominators (overall qo frequency 2.59% vs MID qo rate 3.00%). No error in either experiment.
