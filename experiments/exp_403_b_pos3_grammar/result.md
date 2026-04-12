# exp_403: B pos3 Grammar — After (LF, pos1, pos2), What Happens at pos3? (H628)

**Date:** 2026-04-11
**Hypothesis tested:** H628 — Do formula-typed lines (E_cond≥2.0) maintain LF-conditional structure at pos3?
**Outcome:** Formula effects do NOT strongly persist to pos3 as LF-conditional effects (all formula-trigram pos3 analyses have N=4-8, highly directional). The pos2→pos3 grammar is dominated by UNCONDITIONAL bigram enrichments (sh→qo=2.16×/N=17; qot→ot=2.25×/N=15; l→l=2.16×/N=13). pos1/pos2/pos3 distribution comparison confirms onset gradient: sh 17%→11%→10% (LF-concentrated, decreases); qok 12.5%→16.9%→16.1% (MID-concentrated, increases from pos1); ot 3.8%→5.9%→6.6% (MID-concentrated).

---

## 1. Corpus

B continuation lines (≥4 words): **N=2211**.

---

## 2. Unconditional pos2→pos3 Bigram Enrichments (Top, N≥3)

| pos2 | pos3 | N | E |
|---|---|---|---|
| o | other | 13 | 4.19× |
| l | r | 6 | 3.68× |
| sh | p | 3 | 3.48× |
| **y** | **y** | **5** | **3.41×** |
| **t** | **ot** | **7** | **3.12×** |
| other | o | 12 | 2.98× |
| s | ok | 4 | 2.92× |
| r | sh | 6 | 2.96× |
| k | qot | 6 | 2.55× |
| qot | s | 3 | 2.26× |
| **qot** | **ot** | **15** | **2.25×** |
| **l** | **l** | **13** | **2.16×** |
| **sh** | **qo** | **17** | **2.16×** |

**Most robust (N≥10)**: sh→qo=2.16×(N=17); qot→ot=2.25×(N=15); l→l=2.16×(N=13).

The sh→qo=2.16× at pos2→pos3 connects to F403 (B sh→qo LL=2.67×) and suggests sh→qo is a global bigram rule across MID positions, not just LF→LL. The qot→ot=2.25×(N=15) is a new MID bigram: qot routes to ot at the next MID position.

---

## 3. Formula-Typed Trigram pos3 Routing

All formula-typed trigram pos3 analyses have N=4-8 lines — highly directional. Summary of most interesting signals:

| Formula trigram | pos3 dominant | N/total | E | Notes |
|---|---|---|---|---|
| y→sh→ch | (dispersed) | — | <2.5× all | Formula effect decays at pos3 |
| p→sh→qot | p at pos3 | 1/8 | 12.62× | Highly directional (N=1); qot baseline→ot/qok mild |
| qok→ch→qo | qo self | 2/8 | 4.29× | qo→qo at pos3 (directional) |
| qok→ch→ol | sh | 3/5 | 4.39× | Directional |
| s→sh→l | qok | 3/6 | 3.33× | l→qok at pos3 (consistent with l→? chain) |
| qok→sh→k | cth | 1/5 | 10.60× | Highly directional |
| l→ch→qok | ch | 3/5 | 2.74× | qok→ch near-baseline but elevated here |
| d→ot→ot | (dispersed) | — | <4× all | Formula effect decays at pos3 |

**Interpretation**: For all formula-typed trigrams, pos3 routing is near-Markovian or directional-only. The strongest LF-conditional pos2 effects (y→sh→ch=2.88×, p→sh→qot=2.04×) do NOT produce correspondingly strong pos3 effects. The formula structure is primarily a 3-position effect (LF, pos1, pos2); by pos3, the local bigram grammar (pos2→pos3) takes over.

---

## 4. Onset Gradient at pos1/pos2/pos3

| Class | pos1% | pos2% | pos3% | Trend |
|---|---|---|---|---|
| sh | 17.0% | 10.8% | 10.1% | ↓↓ LF-concentrated |
| qok | 12.5% | 16.9% | 16.1% | ↑→ MID-concentrated |
| ot | 3.8% | 5.9% | 6.6% | ↑↑ MID-concentrated |
| ch | 19.1% | 17.0% | 18.7% | stable |
| d | 2.8% | 4.7% | 4.8% | ↑→ mild MID-lean |
| ok | 7.4% | 7.1% | 8.1% | stable-slight ↑ |
| l | 5.1% | 5.4% | 5.0% | stable |
| other | 6.6% | 5.2% | 4.0% | ↓↓ pos1-concentrated |

The sh gradient (pos1=17%→pos3=10%) confirms F380 (sh is pos1-concentrated in MID). The qok/ot gradient (increases from pos1→pos2/pos3) confirms F380 (qok/ot are MID-enriched). By pos3, the distribution has largely converged to the stable MID distribution — consistent with the "formula overlay" model where pos1→pos2 has LF-conditional effects but pos3→later is near-Markovian.

---

## 5. Implications for Grammar Model

The finding that formula effects primarily operate at positions 1-2 (trigram level) and decay by pos3 is consistent with the "near-Markovian grammar with formula overlays" model:

1. **Line opening (pos0-pos1-pos2)**: LF class conditionally routes pos2 for 9.3% of lines; 90.7% near-Markovian.
2. **pos3 onward**: Governed by unconditional pos2→pos3 bigram grammar (sh→qo, qot→ot, l→l, y→y). LF-conditional effects not detectable with current N.
3. **The sh gradient** (pos1=17%→pos3=10%) represents the transition from LF-sensitive opening to Markovian MID grammar.

---

## 6. Limitations

- All formula-typed trigram pos3 analyses have N=4-8 (highly directional). Cannot confirm or deny strong LF-conditional pos3 effects with current N.
- The pos2→pos3 unconditional bigram analysis (N=2211 lines) is more robust. The formula-conditional analysis (N=4-8 per formula type) is insufficient for definitive pos3 claims.
- The assertion "formula effects decay by pos3" is based on absence of strong signals in small-N analyses — not a positive finding.

---

## Self-Audit

**Target-awareness**: No target-aware elements.

**Feature-destroying implementation**: No feature-destroying elements. Pos3 is correctly extracted as words[3].

**Extrapolation**: "Formula effects do NOT persist to pos3" is stated as "not detectable given current N" rather than "formula effects are absent at pos3." The absence of large E values in N=4-8 analyses is acknowledged as insufficient. PASS.

**Negative-result scope**: The negative result at pos3 (no detectable LF-conditional effects) is correctly scoped to: formula-typed trigrams with N=4-8 lines. Not claiming pos3 is globally Markovian. PASS.

**Control behavior**: No shuffle control. Baseline is unconditional pos2→pos3 rates. Expected global bigram enrichments to persist (sh→qo, qot→ot confirmed). The pos1→pos2→pos3 distribution shift (sh: 17%→11%→10%) is exactly as expected from F380 onset gradient. PASS.

## Finding: F407

**See findings.md F407**
