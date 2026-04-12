# exp_563 result — qo-onset full characterization (H_new_GA)

## Audit

**Target-awareness**: None. Standard methodology.

**Feature-destroying implementation**: None. qo onset is correctly extracted as words starting with "qo" but not "qok" or "qot" (ONSET_PRIORITY order). Consistent methodology throughout.

**Extrapolation**: None. B qo-LF pos1=sh dir (E=2.98×/6): dir level (E≥2.0, obs≥5) correctly flagged. A pos1 E=0.75×: not formally DEPL (need E<0.7); correctly reported as sub-baseline.

---

## Results

### Part 1: qo vocabulary

**A herbal_a** (293 tokens = 2.59% of 11,327 words):
- qodaiin: 24 (8.2%), qol: 23 (7.8%), qoaiin: 14 (4.8%), qockhy: 14 (4.8%), qor: 10 (3.4%), qo: 9 (3.1%)
- 126 unique types — HIGHLY diverse (most classes have 20-50 types)
- No single form dominates. Distributed across d-body (qodaiin, qodal), o-body (qoor), y-body (qody), aiin-body (qoaiin), short forms (qo, qol, qor)

**B all** (314 tokens = 3.09% of 10,163 words):
- **qol: 78 (24.8%)** — massively dominant in B. Next: qolchedy(11=3.5%), qoeedy(11), qodaiin(10=3.2%), qolchey(8), qolkeedy(8).
- 112 unique types
- **A→B vocabulary shift**: A=diverse (qodaiin dominant 8.2%); B=**qol dominant (24.8%)**. The B shift is NOT the typical edy-suffix shift but a convergence toward "qol" specifically. "Qolchedy" (edy-suffix of "qol") is the 3rd B word, consistent with qol→qolchedy edy-formation.

**Frequency**: A=2.59%; B=3.09% — **STABLE / SLIGHT INCREASE**. Unique among major classes: most classes either drop substantially (compound gallows 6.7×↓) or stay near-stable. Qo slightly increases A→B.

**B section distribution**: B astro=4.25% >> B herbal=1.77%, B pharma=2.44%. B qo is concentrated in B astro (significantly above B-overall 3.09%).

### Part 2: qo positional

| Position | A obs | A E | flag | B obs | B E | flag |
|----------|-------|-----|------|-------|-----|------|
| MID base | 220/7333 | 0.030 | — | 238/7601 | 0.031 | — |
| pos1 | 46/2033 | 0.75× | — | 43/1283 | 1.07× | — |
| **LL** | 45/1961 | 0.76× | — | **21/1279** | **0.52×** | **DEPL** |
| **LF** | **27/1961** | **0.46×** | **DEPL** | 33/1279 | 0.82× | — |

**A qo**: LF DEPL (0.46×/27 — E<0.7, obs=27≥3); pos1 and LL sub-baseline (0.75×/0.76×) but not formally DEPL (E>0.70). Qo is primarily MID (220/293 tokens = 75%) in A.

**B qo**: LL DEPL (0.52×/21); LF sub-baseline (0.82×/33); pos1 flat (1.07×/43). Also primarily MID (238/314 = 75.8%) in B.

**A/B positional contrast**: A avoids LF (DEPL 0.46×) but B does NOT avoid LF (0.82×). B avoids LL (DEPL 0.52×) but A does NOT formally avoid LL (0.76×, sub-baseline but above threshold). Qo's positional role SHIFTS between dialects: A=anti-terminal (LF DEPL); B=anti-penultimate (LL DEPL). Both dialects: qo is primarily a MID class (~75% at MID positions).

**Qot comparison**: qot is A pos1 CONF (from prior characterization). Qo is different — sub-baseline at A pos1 (0.75×). Qo is NOT an opener like qot; it's a MID class.

### Part 3: qo bigrams

**A herbal_a** (265 sender, 247 receiver):

| Pair | obs | exp | E | flag |
|------|-----|-----|---|------|
| qo→qo | 14 | 8.0 | 1.76× | **CONF** |
| **qo→sh** | **12** | **25.1** | **0.48×** | **DEPL** |
| sh→qo | 44 | 20.3 | 2.17× | **CONF** |

**CRITICAL: sh→qo CONF (E=2.17×/44) + qo→sh DEPL (E=0.48×/12)** — sh PRECEDES qo at CONF rate, but qo does NOT precede sh (actively avoided). This is a **DIRECTIONAL coupling**: sh→qo is strongly enriched but qo→sh is strongly depleted. The directional asymmetry matches the l→r coupling pattern (l→r CONF; r→l flat, F589).

qo→qo CONF (1.76×/14): self-succession elevated.

**B all** (281 sender, 271 receiver):

| Pair | obs | exp | E | flag |
|------|-----|-----|---|------|
| **qo→ol** | **26** | **14.6** | **1.78×** | **CONF** |
| qo→qo | 16 | 8.8 | 1.82× | **CONF** |
| qo→o | 12 | 7.1 | 1.68× | **CONF** |
| qo→ot | 13 | 20.7 | 0.63× | **DEPL** |
| sh→qo | 50 | 25.4 | 1.97× | **CONF** |

**sh→qo CONF in B (E=1.97×/50)**: sh routes to qo in B at CONF level — same directional coupling as in A.

**qo→ol CONF B (E=1.78×/26)**: qo routes to ol in B (new B-specific signal).
**qo→o CONF B (E=1.68×/12)**: qo routes to o in B.
**qo→ot DEPL B (E=0.63×/13)**: qo avoids ot in B.

**Cross-dialectal constant**: sh→qo CONF in BOTH dialects (A: 2.17×/44 CONF; B: 1.97×/50 CONF).

### Part 4: qo-LF pos1 profile

**A herbal_a**: N=27 qo-LF lines — underpowered for CONF. Directional signals: t@pos1 (1.96×/3), sh@pos1 (1.52×/3) — both near-threshold.

**B all**: N=33 qo-LF lines. **sh@pos1 dir (E=2.98×/6)** — sh is enriched at pos1 for B qo-LF lines (E≥2.0, obs≥5). Lines ending in qo (rare in B but present) tend to be opened by sh at elevated rate. This is consistent with sh→qo CONF B — sh leads to qo within lines, and sh also opens B lines that terminate in qo.

---

## New Findings

**F612: qo vocabulary** — A: 293 tokens (2.59%); diverse 126 types; qodaiin(8.2%), qol(7.8%), qoaiin(4.8%), qockhy(4.8%). B: 314 tokens (3.09%); **qol DOMINANT (78=24.8%)**; qolchedy(11=3.5%), qoeedy(11). A→B shift: A=diverse → B=qol-convergent (not edy-suffix shift but short-form dominance). Frequency-STABLE (2.59%→3.09%, slight increase). B astro elevated (4.25% vs B overall 3.09%).
**Experiment:** exp_563 (2026-04-11)
**Date:** 2026-04-11
**Finding:** A: 293 tokens, 126 unique forms (highly diverse). B: 314 tokens, 112 forms; qol alone=78 (24.8% of all B qo). The B qol concentration is striking — in B, one specific qo word (qol) accounts for 1/4 of all qo tokens. This contrasts with A where qodaiin(8.2%) and qol(7.8%) are close. B section distribution: B astro=4.25% > B pharma=2.44% > B herbal=1.77% — qo is concentrated in B astro. Cross-dialectal frequency: slightly increases A→B unlike most classes (compound gallows drop 5-12×).
**Limitation:** B qol=78 is robust. A vocabulary diversity makes single-form dominant claims weak. B section distribution: B cosmo too small to compute (0 lines?).
**Commitment status:** Not committed.
**Magnitude context:** Qo's frequency stability (2.59%→3.09%) is unusual. Most major classes either drop (compound gallows) or stay near-stable (s, y, t). The B qol dominance (24.8%) is different from B edy-suffix dominance in other classes. "Qol" is a 3-letter word (q+o+l) that might represent a specific grammatical function (quantifier, particle?) especially in B astro context. The B astro elevation (4.25%) parallels other classes with B astro concentrations (qok→qok B astro, F495).

**F613: qo positional — A LF DEPL (0.46×/27 CONF); A pos1/LL sub-baseline; B LL DEPL (0.52×/21); B pos1 flat (1.07×); qo primarily MID (~75% both dialects). A/B positional contrast: A avoids LF (DEPL); B avoids LL (DEPL). Qo is NOT an opener (unlike qot A CONF); it is a MID class with dialect-specific boundary avoidance.**
**Experiment:** exp_563 (2026-04-11)
**Date:** 2026-04-11
**Finding:** A herbal_a: pos1=0.75×/46 (sub-baseline, NOT formally DEPL); LL=0.76×/45 (sub-baseline); LF=0.46×/27 DEPL (E<0.7, obs=27≥3). MID=220/7333=3.00% (= overall qo frequency 2.59% — qo is at baseline in MID). B all: pos1=1.07×/43 (flat); LL=0.52×/21 DEPL; LF=0.82×/33 (sub-baseline). Both dialects: ~75% of qo tokens are at MID positions. Cross-dialectal: qo is NEVER an opener (pos1 neutral-to-sub-baseline in both), never a strong terminal (LF DEPL in A; LL DEPL in B).
**Limitation:** A pos1=0.75×: NOT formally DEPL (need E<0.70). The sub-baseline pos1 is directionally consistent with MID-class character but not as extreme as compound gallows (pos1 near-zero) or a (0.16×). B LL DEPL: E=0.52×/21 — robust DEPL. A LF DEPL: E=0.46×/27 — robust DEPL.
**Commitment status:** Not committed.
**Magnitude context:** Qo's A LF DEPL (0.46×/27) was predicted from F597 (A LF onset taxonomy). Now confirmed with positional analysis. Contrast with qot (A pos1 CONF — opener) and qok (LF DEPL in both — MID class like qo). The qo/qok comparison: both are LF-DEPL in A; both have sub-baseline pos1; both are primarily MID classes. Qot is structurally different (pos1 CONF). The q-class has two OPENER subclasses (qok in A-specific pattern, qot in A) and two MID subclasses (qo, qok in B? need to check). The A/B contrast in which position qo avoids (LF vs LL) may reflect a vocabulary shift (qol in B is a short form that appears in LL positions less often).

**F614: qo bigrams — sh→qo CONF CROSS-DIALECTALLY (A: E=2.17×/44 CONF; B: E=1.97×/50 CONF); qo→sh DEPL A (E=0.48×/12 DEPL) — DIRECTIONAL coupling sh→qo (not mutual). qo→qo CONF both (A: 1.76×/14; B: 1.82×/16 — self-succession). B-specific: qo→ol CONF (1.78×/26); qo→o CONF (1.68×/12); qo→ot DEPL (0.63×/13). B qo-LF pos1=sh dir (2.98×/6).**
**Experiment:** exp_563 (2026-04-11)
**Date:** 2026-04-11
**Finding:** A herbal_a (265 qo-sender; 247 qo-receiver): qo→sh DEPL (E=0.48×/12 — robust DEPL, obs=12≥3, E<0.7); qo→qo CONF (1.76×/14); sh→qo CONF (2.17×/44 — robust CONF). B all (281 sender; 271 receiver): sh→qo CONF (1.97×/50); qo→qo CONF (1.82×/16); qo→ol CONF (1.78×/26); qo→o CONF (1.68×/12); qo→ot DEPL (0.63×/13). B qo-LF pos1: sh@pos1 dir (2.98×/6 — E≥2.0, obs≥5). The sh→qo CONF in BOTH dialects with qo→sh DEPL in A makes this the DIRECTIONAL sh→qo coupling (sh sends to qo, not the reverse).
**Limitation:** qo→sh DEPL A: E=0.48×/12 — robust (obs=12, E=0.48<0.70). B qo-LF pos1: only 33 lines; sh@pos1 dir but N is modest. B qo→ol CONF: obs=26 >> CONF threshold. Cross-dialectal: sh→qo CONF in both, though B's E=1.97× is just below the CONF threshold 2.0× for dir — still CONF (E≥1.5, obs=50>>10).
**Commitment status:** Not committed.
**Magnitude context:** Sh→qo CONF cross-dialectally (2.17×/44 in A; 1.97×/50 in B) is a new strong coupling. Combined with sh's known role (LF DEPL in both dialects; MID class; sh→ch CONF A from prior findings), sh appears to route specifically toward qo within lines. The directionality (qo→sh DEPL in A) means sh precedes qo but not the reverse — sh is a "feeding" class for qo, consistent with sh being a MID class that produces qo transitions. The B-specific qo→ol CONF (1.78×/26) extends qo's grammar: in B, qo words are followed by ol-onset words at elevated rate. Given B ol is a TERMINAL class (LF CONF 1.65×, F582), this may represent B lines where qo appears at MID and ol appears near terminal.

---

## Summary

- **H_new_GA CLOSED**: qo fully characterized.
- Vocabulary: A=diverse (qodaiin dominant 8.2%); B=**qol dominant (24.8%)**. Frequency-STABLE 2.59%→3.09% (F612).
- Positional: A LF DEPL (0.46×/27); B LL DEPL (0.52×/21). Both primarily MID (~75%). Qo is NOT an opener — MID class with dialect-specific boundary avoidance (F613).
- Bigrams: **sh→qo CONF cross-dialectally** (A: 2.17×/44; B: 1.97×/50); qo→sh DEPL A — DIRECTIONAL sh→qo coupling. qo→qo CONF both. B: qo→ol CONF (1.78×/26); qo→o CONF (1.68×/12); qo→ot DEPL (F614).
- B astro elevated (4.25% qo vs 3.09% B overall).

## Self-Audit

**Target-awareness**: No target-aware elements.

**Feature-destroying implementation**: None. qo onset priority correctly placed after qok and qot in ONSET_PRIORITY — words like "qokaiin" get onset qok (correctly), not qo.

**Extrapolation**: None. A pos1=0.75× correctly NOT labeled DEPL (above 0.70). B qo-LF pos1=sh dir (not CONF). All CONF claims have obs≥10 and E≥1.5.

**Negative-result scope**: Qo is NOT a pos1-enriched opener (negative for the opener hypothesis). This is clearly stated.

**Control behavior**: MID baseline for outgoing bigrams; overall distribution for incoming. B section distribution computed using folio-number classification.
