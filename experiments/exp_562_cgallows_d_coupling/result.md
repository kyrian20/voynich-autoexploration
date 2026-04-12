# exp_562 result — Compound gallows → d universal coupling analysis (H_new_FY)

## Audit

**Target-awareness**: None. Standard methodology.

**Feature-destroying implementation**: None. Co-occurrence directionality analysis is straightforward positional comparison. Position enrichment uses all-bigram baseline.

**Extrapolation**: None. [o][ckh][d] triplet: E=3.43×/obs=3 = (dir) level — correctly flagged. Directionality result (d before c-gallows) is a negative finding correctly reported.

---

## Results

### Part 1: Combined compound gallows → d bigram strength

| Class | obs→d | sender total | E | flag |
|-------|-------|-------------|---|------|
| cth→d | 37 | 215 | 1.97× | **CONF** |
| ckh→d | 18 | 103 | 2.00× | **CONF** |
| cph→d | 7 | 32 | 2.50× | dir |
| sch→d | 6 | 20 | 3.43× | dir |
| **COMBINED** | **68** | **370** | **2.10×** | **CONF** |

MID baseline d-rate: 0.0875 (8.75% of MID words are d-onset).

**Combined compound gallows → d CONF (E=2.10×/68)** — the most robust confirmation of the universal coupling. Across 370 c-gallows sender bigrams, 68 (18.4%) lead to d vs expected 8.75% (baseline). This is 2.10× enrichment with high N.

### Part 2: Directionality — within co-occurring lines

Lines with both c-gallows and d: **211** (10.8% of A lines).

| Ordering | count | fraction |
|----------|-------|---------|
| c-gallows BEFORE d (exclusively) | 62 | 29.4% |
| d BEFORE c-gallows (exclusively) | 91 | **43.1%** |
| Mixed (both orderings present) | 58 | 27.5% |

Directional ratio: 62/(62+91) = **0.405** (c-gallows before d in 40.5% of ordered co-occurrences).

**NEGATIVE FINDING: d tends to appear BEFORE c-gallows in A co-occurrence lines (43.1% > 29.4%).** This is the opposite of what a "c-gallows before d" formula would predict. However, this is explained by d's extremely high frequency at BOTH line boundaries in A: d is LF CONF (1.53×/360 = 18.4% of line endings) AND pos1-enriched (1.47× near-CONF). D words appear throughout A lines, often both before and after c-gallows words at MID positions.

**Structural interpretation**: The directional co-occurrence measure cannot distinguish the specific [c-gallows at LL][d at LF] sub-pattern from random mixing. See Part 4 for position-specific analysis.

### Part 3: [y][ckh][d] and [o][ckh][d] triplets

| Triplet | obs | [y/o][ckh] pairs | E | flag |
|---------|-----|-----------------|---|------|
| [y][ckh][d] | 1 | 12 | 0.95× | FLAT |
| **[o][ckh][d]** | **3** | **10** | **3.43×** | **(dir)** |

[y][ckh][d]: flat (E=0.95×/1). The y→ckh→d chain does not form a specific triplet sequence.

**[o][ckh][d] triplet (dir) (E=3.43×/3)**: among the 10 [o][ckh] consecutive pairs, 3 (30%) are followed by d at 3.43× the baseline rate (expected 0.875). This is a (dir)-level signal suggesting o→ckh→d is a recurring A sub-sequence. However obs=3 — minimum for (dir) threshold.

### Part 4: Position of compound gallows → d consecutive bigrams

| Position pair | obs | fraction | baseline | E |
|---------------|-----|---------|---------|---|
| pos1→pos2 | 4 | 5.9% | 21.1% | **0.28× DEPL** |
| MID→MID+1 | 36 | 52.9% | 59.6% | 0.89× (flat) |
| **LL→LF** | **28** | **41.2%** | **19.3%** | **2.13×** |

**KEY FINDING: Compound gallows → d bigrams are 2.13× enriched at LL→LF position.** 28/68 c-gallows→d bigrams (41.2%) occur at LL→LF, while only 19.3% of all bigrams are at LL→LF. This is significantly elevated. The coupling is predominantly a TERMINAL pattern: compound gallows at LL, d at LF.

Compound gallows → d bigrams are DEPLETED at pos1→pos2 (E=0.28×) and flat at MID→MID+1 (E=0.89×). The signal is concentrated at LL→LF.

**Revised interpretation**: The compound gallows → d coupling is primarily a **[c-gallows at LL][d at LF]** structural pattern. This is a terminal sub-pattern: lines that end in d (LF CONF) frequently have a compound gallows word immediately preceding the d-terminal word. The apparent co-occurrence of d appearing "before" c-gallows (Part 2) is due to d appearing multiple times in a line (at both earlier and LF positions), not because c-gallows genuinely precedes d.

### Part 5: Reverse — d → compound gallows

| Pair | obs | exp | E | flag |
|------|-----|-----|---|------|
| d→cth | 62 | 28.0 | **2.21×** | **CONF** |
| d→ckh | 20 | 13.6 | 1.47× | — |
| d→sch | 3 | 0.7 | 4.45× | (dir) |
| d→cph | 4 | 4.2 | 0.96× | — |

**d→cth CONF (2.21×/62)**: confirms F602's d↔cth bidirectional coupling from both directions (cth→d CONF 1.97×/37 + d→cth CONF 2.21×/62). This is a symmetric mutual coupling.

d→ckh is sub-CONF (1.47×/20) — elevated but below 1.5× CONF threshold. d→sch (dir) (4.45×/3) — d precedes sch at elevated rate (obs=3).

---

## New Findings

**F611: Compound gallows → d coupling is LL→LF enriched (E=2.13×/28); combined c-gallows → d CONF (E=2.10×/68 CONF); [o][ckh][d] triplet (dir) (E=3.43×/3); d→cth CONF (E=2.21×/62 — d↔cth mutual coupling reconfirmed). The compound gallows → d coupling is primarily a [c-gallows at LL][d at LF] terminal pattern, not a general within-line ordering.**
**Experiment:** exp_562 (2026-04-11)
**Date:** 2026-04-11
**Finding:** Combined c-gallows → d bigrams: 68/370 sender = 18.4% vs MID baseline 8.75% → E=2.10× CONF (obs=68 >> threshold). Position distribution: LL→LF=28 (41.2%), E=2.13× vs baseline 19.3%; MID→MID+1=36 (52.9%), E=0.89× flat; pos1→pos2=4 (5.9%), E=0.28× DEPL. Directionality: 211 A lines have both c-gallows and d; 43.1% have d before c-gallows (exclusively), 29.4% have c-gallows before d. Directional ratio 0.405 — NOT c-gallows-before-d directional at the co-occurrence level (d is common at pos1 and LF in A, appearing on both sides of MID c-gallows words). [o][ckh][d] triplet (dir): E=3.43×/3. d→cth CONF (2.21×/62 — symmetric mutual coupling).
**Limitation:** [o][ckh][d] triplet: obs=3 at (dir) threshold (minimum). The LL→LF enrichment (2.13×/28) is robust given 28 obs. Directionality (Part 2) gives a negative result for a simple directional formula — correctly reported as negative. The LL→LF position finding reconciles the CONF bigram signal with the negative directionality result.
**Commitment status:** Not committed.
**Magnitude context:** The LL→LF E=2.13×/28 for compound gallows → d is the most specific positional signal found. Combined with cth's LL enrichment (1.35×/65, F601) and the joint LL+LF enrichment for cth (F601), the picture is: A lines with d at LF have compound gallows words preferentially at LL (immediately preceding d). This gives the A terminal structure: [...][c-gallows word at LL][d-word at LF], which is more specific than "c-gallows and d co-occur somewhere in a line." The [o][ckh][d] (dir) triplet (E=3.43×/3) suggests a specific A line sub-pattern: [o-word][ckh-word][d-word] appearing consecutively.

---

## Summary

- **H_new_FY CLOSED**: compound gallows → d coupling confirmed CONF, LL→LF concentrated.
- Combined c-gallows → d: E=2.10×/68 **CONF** (F611).
- LL→LF position 2.13× enriched (28/68 = 41% of c-gallows→d bigrams at terminal pair).
- Directionality NEGATIVE: d appears before c-gallows in 43% of co-occurrence lines (d's high A-LF frequency creates reverse appearances).
- [o][ckh][d] triplet (dir) (E=3.43×/3).
- d→cth CONF (2.21×/62) — d↔cth mutual coupling reconfirmed.
- **Revised interpretation**: c-gallows → d is a **terminal sub-pattern** ([c-gallows at LL][d at LF]), not a general line ordering.

## Self-Audit

**Target-awareness**: No target-aware elements.

**Feature-destroying implementation**: None. Directionality analysis: correctly counts lines with EXCLUSIVELY c-gallows-before-d vs d-before-c-gallows (mixed = both orderings present). The negative directionality finding is structural, not an artifact.

**Extrapolation**: None. [o][ckh][d]: (dir) level correctly flagged. LL→LF E=2.13×/28 is robust (28 obs).

**Negative-result scope**: Directionality negative is genuine — d frequently precedes c-gallows because d is high-frequency at both ends of A lines. This is an informative negative that refines the coupling interpretation.

**Control behavior**: All-bigram baseline for position distribution (not MID-only). This is appropriate for position comparisons.
