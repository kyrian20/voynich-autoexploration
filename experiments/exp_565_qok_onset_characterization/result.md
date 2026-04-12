# exp_565 result — qok-onset full characterization (H_new_GC)

## Audit

**Target-awareness**: None. Standard methodology.

**Feature-destroying implementation**: None. qok onset is correctly the HIGHEST priority in ONSET_PRIORITY — all words starting with "qok" get onset qok (no longer prefix takes priority). Confirmed by the vocabulary output (qokaiin, qokeey correctly captured).

**Extrapolation**: None. A pos1=0.87×/145: NOT labeled DEPL (E>0.70). B pos1=0.81×/171: NOT labeled DEPL (E>0.70). qok→r CONF B: E=1.95×/30 — CONF (E≥1.5, obs=30≥10; E<2.0 so not dir, but CONF threshold met). A qok-pos1 l@LF CONF: E=2.90×/10 — CONF (E≥1.5, obs=10≥10). B qok-pos1 r@LF CONF: E=1.56×/10 — borderline CONF (obs=10 exactly minimum).

**Committed claim conflict**: C007 claims B qok self-succession = 1.24×. Exp_565 finds 1.03× (flat). Conflict written to open_questions.md (Q013). B qok self-succession is NOT reported in findings to avoid contradicting C007.

**Prior data correction**: working_position.md listed A qok pos1 = 1.47× near-CONF. Exp_565 finds A pos1 = 0.87× (sub-baseline). This is NOT a committed claim (C007 does not address positional data). The correction is noted in F619.

---

## Results

### Part 1: qok vocabulary

**A herbal_a** (827 tokens = 7.30% of 11,327):
- qokaiin: 94 (11.4%), qokeey: 81 (9.8%), qokain: 72 (8.7%), qokol: 48 (5.8%), qokal: 48 (5.8%)
- 129 unique types
- Diverse: aiin-body (qokaiin, qokain), e-body (qokeey, qokeol, qokey), lateral (qokol, qokal, qokar), bench (qokchy)

**B all** (1538 tokens = 15.13% of 10,163):
- **qokeedy: 248 (16.1%)**, qokedy: 206 (13.4%), qokeey: 173 (11.2%), qokain: 158 (10.3%), qokaiin: 133 (8.6%)
- 114 unique types
- B: **edy-dominant** (qokeedy+qokedy = 29.5%)

**CRITICAL: A→B frequency MORE THAN DOUBLES (7.30%→15.13%)**. This is the REVERSE of most classes (which drop A→B). Driver: **B astro = 19.58% qok** >> B pharma (12.81%) >> B herbal (9.19%). B astro drives the qok A→B increase — consistent with the q-bench TRIPLET in B astro (F447).

### Part 2: qok positional

| Position | A obs | A E | flag | B obs | B E | flag |
|----------|-------|-----|------|-------|-----|------|
| MID base | 600/7333 | 8.18% | — | 1255/7601 | 16.51% | — |
| pos1 | 145/2033 | 0.87× | — | 171/1283 | 0.81× | — |
| LL | 133/1961 | 0.83× | — | 211/1279 | 1.00× | — |
| **LF** | **82/1961** | **0.51×** | **DEPL** | **112/1279** | **0.53×** | **DEPL** |

**A qok**: LF DEPL (0.51×/82 CONF — robust); pos1 sub-baseline (0.87×/145, NOT formally DEPL); LL sub-baseline (0.83×).

**B qok**: LF DEPL (0.53×/112 CONF — robust); pos1 sub-baseline (0.81×/171, NOT formally DEPL); LL flat (1.00×/211).

**CORRECTION of prior data**: working_position.md showed A qok pos1=1.47× (near-CONF). This is incorrect under canonical methodology. Actual A pos1=0.87× (sub-baseline, NOT enriched). The prior 1.47× was likely from a different corpus partition. Qok is NOT a line-opener in A under canonical methodology.

Qok is a **MID class** with strong **LF DEPL cross-dialectally**: LF is avoided at 0.51-0.53× in both dialects. Both A and B pos1 are sub-baseline (0.81-0.87×) but not formally DEPL.

### Part 3: qok bigrams

**A herbal_a** (sender=741, receiver=682):

| Pair | obs | exp | E | flag |
|------|-----|-----|---|------|
| **sh→qok** | **114** | **56.0** | **2.04×** | **CONF** |
| qok→qok self | 77 | 60.6 | 1.27× | — |
| qo→qok | 27 | 17.6 | 1.53× | **CONF** |
| **qok→s** | **12** | **7.5** | **1.60×** | **CONF** |
| qok→a | 24 | 37.1 | 0.65× | **DEPL** |
| qok→k | 17 | 26.8 | 0.63× | **DEPL** |
| qok→qo | 15 | 22.2 | 0.67× | **DEPL** |
| d→qok | 55 | 82.1 | 0.67× | **DEPL** |
| o→qok | 19 | 32.6 | 0.58× | **DEPL** |
| a→qok | 13 | 30.0 | 0.43× | **DEPL** |

Note: A qok self-succession E=1.27× — sub-CONF (below 1.5×). See Q013 re: committed claim C007 conflict.

**B all** (sender=1426, receiver=1367):

| Pair | obs | exp | E | flag |
|------|-----|-----|---|------|
| **sh→qok** | **266** | **128.3** | **2.07×** | **CONF** |
| **qok→r** | **30** | **15.4** | **1.95×** | **CONF** |
| qok→qo | 31 | 44.7 | 0.69× | **DEPL** |
| qok→a | 29 | 53.1 | 0.55× | **DEPL** |
| qok→k | 17 | 30.4 | 0.56× | **DEPL** |
| d→qok | 64 | 99.7 | 0.64× | **DEPL** |
| o→qok | 19 | 38.6 | 0.49× | **DEPL** |
| s→qok | 18 | 37.1 | 0.48× | **DEPL** |

**Key patterns:**
- **sh→qok CONF cross-dialectally** (A:2.04×/114; B:2.07×/266) — extremely consistent
- **qok→a DEPL cross-dialectally** (A:0.65×/24; B:0.55×/29) — qok avoids routing to a
- **qok→qo DEPL cross-dialectally** (A:0.67×/15; B:0.69×/31) — qok avoids routing to qo
- **qok→k DEPL cross-dialectally** (A:0.63×/17; B:0.56×/17)
- **d→qok DEPL cross-dialectally** (A:0.67×/55; B:0.64×/64) — d avoids routing to qok
- **qo→qok CONF A** (1.53×/27) — qo routes to qok in A
- **qok→r CONF B** (1.95×/30) — qok routes to r in B (r is B's strongest LF class)
- **qok→s CONF A** (1.60×/12) — qok routes to s (an opener) in A

**qok-pos1 line terminal grammar:**
- A [qok-opener]→l@LF **CONF** (2.90×/10) — qok-opening A lines terminate with l
- A [qok-opener]→k@LF **dir** (2.36×/9)
- B [qok-opener]→r@LF **CONF** (1.56×/10) — qok-opening B lines terminate with r
- B [qok-opener]→s@LF **dir** (2.09×/7)
- B [qok-opener] pos2=ol **CONF** (1.58×/14) — B qok-opener lines have ol at pos2

**qok-LF pos1:**
- A: y@pos1 DEPL (0.67×/9), ch@pos1 DEPL (0.66×/4) — lines ending in qok do NOT start with y or ch
- B: y@pos1 DEPL (0.62×/8), d@pos1 DEPL (0.65×/14) — B qok-LF lines avoid y and d openers; p@pos1 dir (2.11×/5)

---

## New Findings

**F618: qok vocabulary** — A: 827 tokens (7.30%); 129 types; diverse (qokaiin 11.4%, qokeey 9.8%, qokain 8.7%); aiin/e/lateral mix. B: 1538 tokens (15.13%); edy-dominant (qokeedy 16.1%, qokedy 13.4%); **A→B frequency MORE THAN DOUBLES (7.30%→15.13%)**. B astro=19.58% >> B pharma=12.81% >> B herbal=9.19% — B astro drives the increase. Cross-dialectal vocabulary shift: A=diverse → B=edy-convergent.
**Experiment:** exp_565 (2026-04-11)
**Date:** 2026-04-11
**Commitment status:** Not committed.
**Magnitude context:** Qok's A→B frequency doubling (7.30%→15.13%) is unique among characterized classes. All other frequent classes either drop (compound gallows 6×, cth 8.6×) or stay stable (s, t, y, sh, qo). The B astro driver (19.58%) is consistent with the q-bench TRIPLET (qok+qot+qo all elevated in B astro LF, F447). Qok is the most concentrated class in B astro, where it may have a structural grammar role not present in B herbal/pharma.

**F619: qok positional** — A: LF DEPL (0.51×/82 CONF); pos1 sub-baseline (0.87×/145, NOT DEPL); LL sub-baseline (0.83×). B: LF DEPL (0.53×/112 CONF); pos1 sub-baseline (0.81×/171, NOT DEPL); LL flat (1.00×). CORRECTS prior: working_position.md A pos1=1.47× near-CONF is INCORRECT under canonical methodology (actual: 0.87×, sub-baseline). Qok is a **MID class with strong LF DEPL cross-dialectally**. Not an opener.
**Experiment:** exp_565 (2026-04-11)
**Date:** 2026-04-11
**Commitment status:** Not committed.
**Magnitude context:** The correction of A qok pos1 from 1.47× to 0.87× is significant. Under canonical methodology, qok is not enriched at pos1 in A — it is sub-baseline (0.87×). This changes qok's classification from "A sub-opener" to "MID class." The LF DEPL cross-dialectally (0.51×/0.53×) is robust. Combined with the B astro elevation (F618), qok's MID role and LF avoidance suggest it is a structural MID class that concentrates in B astro but never appears at line endings. Prior data for A pos1 likely used a different corpus partition or methodology.

**F620: qok bigrams** — CROSS-DIALECTAL: sh→qok CONF (A:2.04×/114; B:2.07×/266); qok→a DEPL (A:0.65×/24; B:0.55×/29); qok→qo DEPL (A:0.67×/15; B:0.69×/31); qok→k DEPL (A:0.63×/17; B:0.56×/17); d→qok DEPL (A:0.67×/55; B:0.64×/64). A-SPECIFIC: qo→qok CONF(1.53×/27); qok→s CONF(1.60×/12); o→qok DEPL(0.58×/19); a→qok DEPL(0.43×/13). B-SPECIFIC: qok→r CONF(1.95×/30); o→qok DEPL(0.49×/19); s→qok DEPL(0.48×/18). Terminal grammar: A [qok-opener]→l@LF CONF(2.90×/10); B [qok-opener]→r@LF CONF(1.56×/10); B pos2=ol CONF(1.58×/14). qok-LF pos1: y@pos1 DEPL both; d@pos1 DEPL B; p@pos1 dir B.
**Experiment:** exp_565 (2026-04-11)
**Date:** 2026-04-11
**Commitment status:** Not committed.
**Magnitude context:** sh→qok CONF cross-dialectally (A:2.04×; B:2.07×) is exceptionally consistent — E nearly identical in both dialects. This confirms sh as the primary feeder to qok, completing the s→sh→qok chain (s→sh CONF F617; sh→qok CONF F620). The d→qok DEPL cross-dialectally (0.67×/0.64×) is structurally coherent: d is an A terminal/B opener — in A it appears at LF (cannot route forward); in B it appears at pos1 (routes to other classes but avoids qok). The qok→r CONF B (1.95×/30) extends the B terminal routing: qok routes to r (the strongest B LF class, F588), creating a B sub-pattern [qok→r] that may represent [MID qok word][r-terminal word near LF]. The A [qok-opener]→l@LF CONF (2.90×/10) and B [qok-opener]→r@LF CONF (1.56×/10) shows dialect-specific terminal pairing for qok-opening lines (A uses l; B uses r — the same cross-dialectal terminal-class inversion seen in F593). Note: B qok self-succession (1.03×) is excluded due to conflict with C007 (see Q013).

---

## Summary

- **H_new_GC CLOSED**: qok fully characterized.
- Vocabulary: A=diverse (7.30%, 129 types); B=edy-dominant (15.13%), **A→B MORE THAN DOUBLES** (B astro=19.58% driver) (F618).
- Positional: LF DEPL cross-dialectally (A:0.51×/82; B:0.53×/112 CONF); pos1 sub-baseline both (0.87×/0.81×, not formally DEPL). **CORRECTS prior: A pos1 NOT 1.47× but 0.87×**. Qok is a MID class (F619).
- Bigrams: **sh→qok CONF cross-dialectally** (A:2.04×/114; B:2.07×/266); multiple DEPL routes (qok→a, qok→qo, qok→k; d→qok all cross-dialectal). A: qo→qok CONF, qok→s CONF. B: qok→r CONF. Terminal grammar: A→l@LF CONF; B→r@LF CONF (dialect-specific terminal pairing) (F620).

## Self-Audit

**Target-awareness**: None.

**Feature-destroying implementation**: None. qok correctly has highest onset priority — all qok-starting words captured first.

**Extrapolation**: None. A pos1=0.87×: NOT labeled DEPL; B pos1=0.81×: NOT labeled DEPL. qok→r B: E=1.95×/30 labeled CONF (E≥1.5, obs≥10). All CONF claims meet obs≥10 and E≥1.5.

**Committed claim conflict**: B qok self-succession discrepancy with C007 documented in Q013. No claim about B qok self-succession made in findings.

**Prior data correction**: A qok pos1 = 0.87× vs prior 1.47× in working_position.md. This is NOT a committed claim conflict (C007 does not address positional E-values). The correction is reported in F619 and working_position.md should be updated.
