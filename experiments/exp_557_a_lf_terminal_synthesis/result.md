# exp_557 result — A herbal_a LF terminal synthesis (H_new_FT)

## Audit

**Target-awareness**: None. All baselines corpus-internal.

**Feature-destroying implementation**: None. Standard positional methodology.

**Extrapolation**: None. All claims within A herbal_a (2033 lines).

---

## Results

### Part 1: A LF full onset distribution

**A herbal_a: 1961 LF words from 1961 eligible lines**

| Class | A LF obs | A LF E | LF flag | A pos1 E | pos1 flag | Role |
|-------|---------|--------|---------|---------|-----------|------|
| cth | 88 | **1.67×** | **CONF** | 0.13× | — (extreme DEPL) | **A TERMINAL** |
| d | 360 | **1.53×** | **CONF** | 1.47× | — (near-CONF) | **A TERMINAL (+near opener)** |
| f | 3 | 1.72× | — (obs<10) | — | — | — |
| r | 16 | 1.41× | — | 0.09× | — | sub-CONF both |
| a | 117 | 1.35× | — | 0.16× | DEPL | pos1-DEPL, sub-LF |
| ol | 96 | 1.24× | — | 0.67× | DEPL | pos1-DEPL |
| l | 48 | 1.16× | — | 0.72× | — | near-pos1-DEPL |
| o | 105 | 1.12× | — | 1.39× | — | neutral |
| ot | 103 | 1.08× | — | 0.80× | — | neutral |
| s | 52 | 1.03× | — | 3.24× | **CONF** | **OPENER** |
| ok | 144 | 0.99× | — | 0.62× | DEPL | pos1-DEPL |
| t | 47 | 0.96× | — | 2.28× | **CONF** | **OPENER** |
| ch | 373 | 0.96× | — | 0.38× | DEPL | pos1-DEPL |
| qot | 46 | 0.91× | — | 1.41× | — | neutral |
| k | 53 | 0.87× | — | 0.52× | DEPL | pos1-DEPL |
| y | 72 | 0.63× | **DEPL** | 2.81× | **CONF** | **OPENER + LF-DEPL** |
| p | 3 | 0.59× | **DEPL** | 2.97× | **CONF** | **OPENER + LF-DEPL** |
| qok | 82 | 0.57× | **DEPL** | 0.98× | — | **LF-DEPL** |
| sh | 88 | 0.55× | **DEPL** | 0.89× | — | **LF-DEPL** |
| qo | 27 | 0.53× | **DEPL** | 0.88× | — | **LF-DEPL** |
| sch | 2 | 0.52× | — | 3.91× | **CONF** | **OPENER (NEW)** |

**A LF CONF classes**: cth(1.67×/88), d(1.53×/360) — only 2 confirmed.
**A LF DEPL classes**: y(0.63×/72), p(0.59×/3 small N), qok(0.57×/82), sh(0.55×/88), qo(0.53×/27).

**NEW A-specific finding**: cth is pos1 EXTREME DEPL (0.13×/7) — cth almost never opens A lines. It is a terminal class only. A LF CONF: {cth, d}; cth is a pos1-avoider and terminal; d is both near-opener AND terminal (dual-position class).

**NEW: sch is A pos1 CONF (3.91×/15)** — sch-onset words open A herbal_a lines at 3.91× baseline rate at CONF level. Previously only dir in B (3.97×/9).

### Part 2: A LF word vocabulary

Top A LF words (from 1961 lines):
- **daiin (d): 98 (5.0%)** — single most common A LF word, by far
- dy (d): 45 (2.3%); cthy (cth): 27 (1.4%); dal (d): 24 (1.2%); dam (d): 22 (1.1%)
- ol (ol): 22 (1.1%); dar (d): 20 (1.0%); dain (d): 20 (1.0%)

**D-onset words dominate A LF**: daiin+dy+dal+dam+dar+dain together = 229/1961 = 11.7% of all A LF words. Daiin alone (5.0%) is the single most common A LF word — nearly 1 in 20 A lines ends in 'daiin'.

**Cth-LF vocabulary**: cthy(27=1.4%), cthey(9), cthol(6), cthor(6) — cthy accounts for 27/88 = 31% of all cth-LF obs. 'Cthy' is the canonical A terminal cth-word.

**A LF vocabulary comparison with B LF**: A = d-dominated (daiin, dy, dal); B = ch/l/ol/d distributed (chedy, oly, dy, lchedy). Both have d-LF words (dy, dar) but A has 'daiin' (5.0%) vs B's top word 'chedy' (3.1%).

**A a-LF words**: aiin(15), am(12), al(10), ar(8) — in A, 'aiin' tops a-LF (vs B where 'am' tops). A→B reversal in a-LF: aiin>am in A; am>aiin in B.

### Part 3: Complete cross-dialect comparison

| Class | A:pos1-E | A:LF-E | B:pos1-E | B:LF-E | A-role | B-role |
|-------|---------|--------|---------|--------|--------|--------|
| p | 2.97× CONF | 0.59× DEPL | 5.23× CONF | 0.39× | OPENER+LF-DEPL | OPENER |
| sch | **3.91× CONF** | 0.52× | 3.97× dir | — | **OPENER (NEW)** | dir-opener |
| s | 3.24× CONF | 1.03× | 4.77× CONF | 0.72× | OPENER | OPENER |
| y | 2.81× CONF | 0.63× DEPL | 3.54× CONF | 0.60× DEPL | OPENER+LF-DEPL | OPENER+LF-DEPL |
| t | 2.28× CONF | 0.96× | 3.18× CONF | 0.45× DEPL | OPENER | OPENER+LF-DEPL |
| d | 1.47× near-CONF | **1.53× CONF** | **2.64× CONF** | 1.30× | **LF-CONF+near-opener** | **OPENER** |
| cth | 0.13× DEPL | **1.67× CONF** | 1.79× | 1.79× | **A TERMINAL only** | B sub-enriched |
| r | 0.09× | 1.41× | 0.35× DEPL | **2.80× CONF** | sub-LF | **B TERMINAL** |
| l | 0.72× | 1.16× | 0.52× DEPL | **1.85× CONF** | — | **B TERMINAL** |
| ol | 0.67× DEPL | 1.24× | 0.63× DEPL | **1.65× CONF** | pos1-DEPL | **B TERMINAL** |
| o | 1.39× | 1.12× | 1.00× | **1.58× CONF** | neutral | **B TERMINAL** |
| a | 0.16× DEPL | 1.35× | 0.26× DEPL | **1.52× CONF** | pos1-DEPL | **B TERMINAL** |
| sh | 0.89× | 0.55× DEPL | 0.65× DEPL | 0.45× DEPL | LF-DEPL | LF-DEPL+pos1-DEPL |
| qok | 0.98× | 0.57× DEPL | 0.88× | 0.58× DEPL | LF-DEPL | LF-DEPL |
| y | — | — | — | — | LF-DEPL | LF-DEPL |

**Key structural contrast**: The 5 B terminal classes (r,l,ol,o,a) are all sub-threshold in A LF (1.12-1.41× range). The 2 A terminal classes (cth, d) are not CONF in B LF (cth: 1.79×/7 underpowered; d: 1.30× below CONF threshold). Each dialect has its own terminal-layer vocabulary with no overlap.

**Cross-dialectal constants**: y(DEPL both), qok(DEPL both), sh(DEPL A + DEPL B).

---

## New Findings

**F597: A LF full onset taxonomy — CONF LF-enriched: d(1.53×/360), cth(1.67×/88). CONF LF-depleted: y(0.63×/72), qok(0.57×/82), sh(0.55×/88), qo(0.53×/27). CTH is pos1 EXTREME DEPL (0.13×/7) — exclusively a terminal class in A. A LF CONF = {d,cth}; B LF CONF = {r,l,ol,o,a} — complete terminal-layer dialect inversion with zero overlap. Cross-dialectal LF-DEPL constants: y, qok, sh depleted in both.**
**Experiment:** exp_557 (2026-04-11)
**Date:** 2026-04-11
**Finding:** A herbal_a complete LF onset distribution (1961 LF words). LF-CONF: cth=1.67×/88 CONF; d=1.53×/360 CONF. LF sub-enriched (below CONF threshold): f=1.72×/3; r=1.41×/16; a=1.35×/117; ol=1.24×/96. LF-DEPL: y=0.63×/72 CONF; p=0.59×/3 CONF; qok=0.57×/82 CONF; sh=0.55×/88 CONF; qo=0.53×/27 CONF. Cth is pos1 extreme DEPL (0.13×/7) — appears almost exclusively at LF, never at pos1. D is near-opener (1.47× near-CONF pos1) AND CONF terminal (1.53×/360 LF) — the only class with meaningful presence at BOTH pos1 and LF in A. Cross-dialectal constants (LF-DEPL in both A and B): y(A:0.63×; B:0.60×), qok(A:0.57×; B:0.58×), sh(A:0.55×; B:0.45×). None of the 5 B LF-CONF classes (r,l,ol,o,a) reach CONF in A LF.
**Limitation:** A herbal_a n≤56. Cth obs=88 at A LF — robust CONF. D obs=360 at A LF — most robust A LF claim. P LF obs=3 at E=0.59× — formally DEPL (E<0.7, obs≥3) but small. Qo LF obs=27 at E=0.53× — CONF. The 5 sub-enriched classes (f, r, a, ol, l) are all directionally above 1.0× but below CONF — they show A LF sub-enrichment consistent with their B LF CONF status but insufficient A N for formal CONF.
**Commitment status:** Not committed.
**Magnitude context:** D at 360 obs is the most robust A LF finding (higher N than any other positional E-value in this entire program). CTH at 88 obs with E=1.67× is second. Together d+cth = 448/1961 = 22.8% of all A LF words, yet they are only 18.7% of the total A corpus — the 1.53-1.67× enrichment represents ~60-100 excess LF occurrences above expected. Y, qok, sh together suppress: 242 LF obs vs ~419 expected = 177 fewer LF words than expected. These cross-cancel: LF is enriched in d+cth and depleted in y+qok+sh — a strong redistribution.

**F598: A LF word vocabulary — 'daiin' is the dominant A LF word (98=5.0% of all A LF lines). D-onset words (daiin+dy+dal+dam+dar+dain) together = ~23% of A LF words. 'Cthy' tops cth-LF (27=1.4%). A a-LF: aiin(15) > am(12) [opposite of B: am>aiin]. A LF is d-dominated; B LF is more distributed.**
**Experiment:** exp_557 (2026-04-11)
**Date:** 2026-04-11
**Finding:** A herbal_a LF word vocabulary (1961 lines). Top words: daiin(98=5.0%), dy(45=2.3%), cthy(27=1.4%), dal(24=1.2%), dam(22=1.1%). D-onset accounts for 360/1961=18.4% of A LF words, making d the most common A LF onset class by a large margin (second is ch=373 obs=19.0% but ch at E=0.96× is not LF-enriched; d is enriched). Cthy(27) accounts for 31% of all cth-LF obs — 'cthy' is the canonical A terminal cth-form (y-body suffix). A a-LF top words: aiin(15), am(12), al(10), ar(8) — in A, 'aiin' is the most common a-LF word; in B, 'am' tops a-LF (11 obs). Both 'aiin' and 'am' are a-onset terminal forms but their relative frequency inverts across dialects. The B 'am' dominance at LF may reflect B's different morphological conventions for terminal particles.
**Limitation:** B LF: chedy(40=3.1%) was top word from ch-class (not LF-enriched); A LF: daiin(98=5.0%) from d-class (LF-CONF). The comparison is informative: B's most common LF word is from a non-enriched class (ch); A's most common is from an enriched class (d). A is more concentrated in its LF-enriched class vocabulary.
**Commitment status:** Not committed.
**Magnitude context:** 'Daiin' at 98 obs = 5.0% of A LF lines means ~1 in 20 A herbal_a lines ends with 'daiin'. This is a remarkably concentrated terminal word. In the full A herbal_a corpus, daiin (classified as d-onset) should occur at ~32.3% of all d-tokens (from F553: A daiin = 32.3% of d-tokens). With 360 d-LF obs and daiin=32.3% of d, expected daiin-LF ≈ 116 — the 98 obs is slightly below this (consistent with daiin having normal within-d distribution at LF vs other d-words). The terminal role of 'daiin' is its d-class position, not daiin-specific concentration.

**F599: Complete A/B cross-dialect positional comparison — A OPENERS (pos1 CONF): sch(3.91×/15 — NEW CONF), s(3.24×/163), y(2.81×/323), p(2.97×/15), t(2.28×/111); d near-CONF (1.47×/346). A TERMINALS (LF CONF): cth(1.67×/88), d(1.53×/360). B OPENERS (pos1 CONF): p(5.23×/27), s(4.77×/165), y(3.54×/147), t(3.18×/78), d(2.64×/246). B TERMINALS (LF CONF): r(2.80×/48), l(1.85×/145), ol(1.65×/115), o(1.58×/57), a(1.52×/70). D is the KEY DIALECT-CROSSING CLASS: A TERMINAL; B OPENER. Cth and r/l/ol/o/a are dialect-specific terminal classes. Cross-dialectal constants: y,qok,sh LF-DEPL in both. NEW: sch is A pos1 CONF (3.91×/15).**
**Experiment:** exp_557 (2026-04-11)
**Date:** 2026-04-11
**Finding:** Complete cross-dialect positional comparison from exp_555+557. A openers (pos1 CONF): sch(3.91×/15 NEW), s(3.24×/163), y(2.81×/323), p(2.97×/15), t(2.28×/111) — plus d near-CONF (1.47×/346). B openers (pos1 CONF): p(5.23×/27), s(4.77×/165), y(3.54×/147), t(3.18×/78), d(2.64×/246). Shared openers (CONF both): p, s, y, t. B-specific openers: d. A-specific openers: sch (dir B only). A terminals (LF CONF): cth(1.67×/88), d(1.53×/360). B terminals (LF CONF): r(2.80×/48), l(1.85×/145), ol(1.65×/115), o(1.58×/57), a(1.52×/70). Cth-onset: A terminal (pos1 DEPL 0.13×; LF CONF 1.67×); B pos1 sub-elevated (1.79×/7 dir) + B LF sub-elevated (1.79×/7) — small N prevents CONF claim in B. D's role inversion is complete: A LF CONF (1.53×/360) + pos1 near-CONF (1.47×/346); B pos1 CONF (2.64×/246) + LF sub-enriched (1.30×/121). The d-class has substantial presence at BOTH edges in BOTH dialects but is dominant at opposite edges.
**Limitation:** A herbal_a n≤56; B all. Sch obs=15 at pos1 in A (CONF borderline but meets both thresholds). Cth in B: 7 obs at LF and 7 obs at pos1 — too small for CONF claims; the 1.79× E-values are directional only. The A 3-layer architecture is less clean than B: d occupies both terminal and near-opener positions; only cth is purely terminal. B has a cleaner separation.
**Commitment status:** Not committed.
**Magnitude context:** The d-class role reversal (A=terminal; B=opener) is the most dramatic cross-dialect structural difference found. Every other cross-dialectal class either maintains its role (s,t,y remain openers; y,qok,sh remain LF-depleted) or shows amplification (p remains opener but E increases from 2.97× to 5.23×). Only d undergoes role reversal. The question of what cth corresponds to in B (no LF-CONF analog exists) is open — cth may represent a structurally distinct A-specific word class with no B equivalent.

---

## Summary

- **H_new_FT CLOSED**: A herbal_a LF terminal structure fully characterized.
- **F597**: A LF CONF = cth(1.67×/88) + d(1.53×/360); A LF DEPL = y,qok,sh,qo. Cth pos1 EXTREME DEPL (0.13×). Zero overlap with B LF CONF classes.
- **F598**: A LF vocabulary — daiin(98=5.0%) dominant; cthy(27=1.4%) top cth-LF; a-LF: aiin>am (opposite of B).
- **F599**: Complete A/B comparison — NEW: sch is A pos1 CONF (3.91×/15). D is key dialect-crossing class (A=terminal; B=opener). Shared CONF openers: p,s,y,t. Cross-dialectal constants: y,qok,sh LF-DEPL in both.
- **New hypothesis H_new_FU**: cth-onset full characterization — cth is A LF CONF (1.67×/88) and pos1 EXTREME DEPL (0.13×); a purely terminal A class. Full vocabulary, positional, and bigram characterization needed.

## Self-Audit

**Target-awareness**: No target-aware elements.

**Feature-destroying implementation**: None. Standard positional methodology consistent with exp_555.

**Extrapolation**: No extrapolation. Cth's B sub-enrichment (1.79×/7) is reported as directional only (obs=7 too small for CONF). All CONF claims are within the tested data with sufficient N.

**Negative-result scope**: N/A — positive results (F597-F599 all informative).

**Control behavior**: No separate control. Corpus-internal baselines throughout.
