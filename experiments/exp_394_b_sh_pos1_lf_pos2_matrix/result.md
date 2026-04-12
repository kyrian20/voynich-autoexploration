# exp_394: Complete B sh-pos1 LF×pos2 Matrix (H611)

**Date:** 2026-04-11
**Hypothesis tested:** H611 — Full pos2 distribution for all LF classes in B sh-pos1 lines
**Outcome:** ANSWERED — Four B sh-pos1 LF grammar types identified; d→sh near-Markovian; s→sh→qot=0.00× (new categorical); qok→sh→k=4.08× (new template path); B ch-pos1 grammar: p→ch→ot=5.28×

---

## 1. sh-pos1 Baseline

B continuation lines with sh at pos1: **377** (with ≥3 words for pos2 analysis).
Baseline pos2 distribution: qok=27.1%, sh=11.4%, ch=10.9%, qot=7.4%, qo=6.6%, l=4.8%, ok=4.5%, ot=4.2%, o=4.2%, k=3.7%.

---

## 2. Full LF×pos2 Matrix for B sh-pos1 Lines

| LF | N | qok | ch | qot | l | k | other notes |
|----|---|-----|-----|-----|---|---|-------------|
| d | 80 | 1.11×(24) | 0.69×(6) | 1.01×(6) | 1.31×(5) | 1.01×(3) | Near-Markovian throughout |
| s | 61 | 1.27×(21) | 1.06×(7) | **0.00×(0)** | **2.06×(6)** | 0.44×(1) | qot categorical depletion; l routing |
| p | 51 | 0.58×(8) | **0.18×(1)** | **2.11×(8)** | 0.00×(0) | 1.06×(2) | gallows-formula (F396) confirmed |
| t | 35 | 0.53×(5) | 1.31×(5) | 1.54×(4) | 1.80×(3) | 0.77×(1) | o=2.02×(3); distributed |
| qok | 33 | 1.12×(10) | 1.11×(4) | 1.63×(4) | 0.63×(1) | **4.08×(5)** | k=4.08× very strong template path |
| y | 25 | 0.59×(4) | **2.94×(8)** | 1.08×(2) | 0.84×(1) | 0.00×(0) | content-formula (F396) confirmed |
| sh | 16 | 1.16×(5) | 1.72×(3) | 0.00×(0) | 0.00×(0) | 1.68×(1) | self-chain: ch/sh mild enrichment |

---

## 3. Four B sh-pos1 LF Grammar Types

**Type 1 — Content-formula (y):** y→sh→ch=2.94×(N=8/25). ch strongly enriched, qok/y depleted.

**Type 2 — Gallows-formula (p):** p→sh→qot=2.11×(N=8/51), ch≈0(0.18×). qot enriched, ch/qok depleted.

**Type 3 — Template-class (qok):** qok→sh→k=4.08×(N=5/33). k strongly enriched. This is a new finding: qok at LF specifically routes to k-onset at pos2 after sh.

**Type 4 — Formula-terminal (s):** s→sh→l=2.06×(N=6/61). l-onset enriched at pos2. s→sh→qot=0.00×(N=0/61) categorical depletion (extends F393's s→sh→d=0.00× to include qot). s→sh lines avoid both d and qot at pos2.

**Type 5 — Near-Markovian (d, t):** d→sh (N=80) shows no strong pos2 routing; all E values 0.59–1.39×. t→sh (N=35) also distributed (o/l/qot/ch all 1.3-2.0× but small N).

The cross-LF pos2=ch rate spans 0.18×(p) to 2.94×(y). The cross-LF pos2=qot rate spans 0.00×(s/sh) to 2.11×(p) to 1.63×(qok). Grammar type at the trigram level is determined by the LF class, not by pos1 class alone.

---

## 4. B ch-pos1 LF×pos2 Matrix (for Comparison)

B continuation lines with ch at pos1: **428** (with ≥3 words).
Baseline pos2: ch=18.2%, qok=16.8%, ok=9.8%, l=8.6%, sh=7.0%, qot=6.1%, qo=5.6%, other=4.9%.

Key LF-conditional results for B ch-pos1:
- **p (N=18)**: ot=**5.28×(N=4)** — strongly enriched; p→ch→ot is the dominant p-ch path
- **y (N=49)**: ok=1.87×(N=9), ch=1.46×(N=13) — y→ch→ok and y→ch→ch enriched
- **qok (N=55)**: qo=2.59×(N=8), ol=2.29×(N=5) — qok→ch routes to qo/ol classes
- **d (N=79)**: l=1.76×(N=12), qo=0.23×(N=1) depleted
- **t (N=38)**: other=2.15×(N=4), ol=1.99×(N=3), sh=0.38×(N=1) depleted

The B ch-pos1 grammar is less strongly LF-conditioned than sh-pos1 (most E values 1.0-2.0× vs sh's 2-4× range), except for p→ch→ot=5.28×.

---

## 5. Summary of New Findings

**New:** qok→sh→k=4.08×(N=5/33) — template class at LF routes to k at pos2 via sh (not previously documented)
**New:** s→sh→qot=0.00×(N=0/61) — s suppresses qot at pos2 after sh (extends F393's s→sh→d=0.00× to a two-class depletion: {d, qot})
**New:** p→ch→ot=5.28×(N=4/18) — when p at LF pairs with ch at pos1 (not sh), ot at pos2 is strongly enriched
**Confirmed:** y→sh→ch=2.94× (F396), p→sh→qot=2.11× (F396), d→sh near-Markovian (F393 established d as near-baseline)

---

## Self-Audit

**Target-awareness**: No target-aware elements. Corpus analysis only.

**Feature-destroying implementation**: No feature-destroying elements.

**Extrapolation**: All E values within tested data. qok→sh→k=4.08× N=5/33 (adequate for strong enrichment characterization, but specific word-level details would require N>10). s→sh→qot=0.00× N=0/61 (adequate for categorical characterization). p→ch→ot=5.28× N=4/18 (adequate for enrichment characterization given the very strong E). d→sh near-Markovian: N=80, adequate. t→sh distributed: N=35, each individual pos2 E value directional (N=2-5 per cell). All claims labeled with N.

**Negative-result scope**: N/A — descriptive analysis.

**Control behavior**: sh-pos1 baseline (N=377) and ch-pos1 baseline (N=428) serve as controls. Expected d→sh to be near-Markovian (F393 established most common B paths as near-baseline); confirmed (all d→sh E values 0.59–1.39×). Expected y→sh→ch=2.94× and p→sh→qot=2.11× from F396; confirmed exactly.

## Finding: F398

**See findings.md F398**
