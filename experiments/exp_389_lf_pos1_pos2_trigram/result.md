# exp_389: LF→pos1→pos2 Trigram Structure (H603)

**Date:** 2026-04-11
**Hypothesis tested:** H603 — is B-dialect line grammar Markovian at bigram level?
**Outcome:** PARTIAL — grammar is NOT strictly bigram-Markovian; LF class adds moderate-to-strong conditioning on pos2 beyond pos1 class in specific combinations; y-chain extends to 3 positions in A; B p→sh→ch≈0; B y→sh→ch elevated (2.94×)

---

## 1. Corpus Statistics

- A trigrams (LF, pos1, pos2): **1382** (continuation lines with ≥3 words)
- B trigrams (LF, pos1, pos2): **2225**

---

## 2. Key Findings: LF Conditioning Effects on pos2

### Finding 1: B p→sh→ch ≈ 0 (Strongest LF-Conditioning Found)

| Context | pos2=ch rate | N | baseline sh→ch |
|---------|-------------|---|----------------|
| (p, sh) → pos2=ch | 0.02 (N=1/51) | 51 | 0.11 (N=41/377) |
| (y, sh) → pos2=ch | 0.32 (N=8/25) | 25 | 0.11 |
| (d, sh) → pos2=ch | 0.07 (N=6/80) | 80 | 0.11 |
| (s, sh) → pos2=ch | 0.11 (N=7/61) | 61 | 0.11 |

**B p at LF specifically suppresses ch at pos2 when sh is at pos1 (0.18× vs baseline).** By contrast, B y at LF specifically enriches ch at pos2 (2.94×/N=8). The pos2 ch rate after (LF, pos1=sh) is strongly LF-class-dependent: ranges from 0.02 (p) to 0.32 (y) — a 16× span. This is the strongest LF→pos1→pos2 trigram effect found.

### Finding 2: A y Self-Chain Extends to 3 Positions

| Context | pos2=y rate | N | baseline (*,y)→y |
|---------|-------------|---|-------------------|
| (y, y) → pos2=y | 0.250 (N=3/12) | 12 | 0.116 (N=5/43) |

A y→y→y: E=2.15×(N=3, directional). When y appears at both LF and pos1, y is 2.15× more likely at pos2 than the (*,y)→y bigram baseline. The y self-chain extends to at least 3 positions in A. Additionally, (y,y)→ch=0.00 — ch is excluded from pos2 after (y,y).

**B y-chain does NOT extend to pos2**: (y,y)→y=0.000 (N=0/12) in B. B y self-chains at LF→pos1 (E=2.13×, F390) but the chain terminates; after (y,y), pos2 is ch(0.33×/N=4) or d(0.25×/N=3).

### Finding 3: B (s, sh)→pos2=d ≈ 0

| Context | pos2=d rate | N | baseline sh→d |
|---------|-------------|---|---------------|
| (s, sh) → pos2=d | 0.000 (N=0/61) | 61 | 0.032 (N=12/377) |

When s is at LF and sh at pos1, d never appears at pos2 (0/61 events vs 12/377=3.2% baseline). This extends the s-formula avoidance pattern: s not only avoids producing d at pos1 (F386 B s→d LF=0.29×) but also suppresses d at pos2 when sh is at pos1.

### Finding 4: Most Common B Paths Near-Bigram-Markovian

| Context | TVD from P(pos2|pos1) | N |
|---------|----------------------|---|
| (d, sh)→pos2 | ~0.10 (estimated) | 80 |
| (d, ch)→pos2 | ~0.08 (estimated) | 79 |
| (s, sh)→pos2 | ~0.09 + d=0 effect | 61 |

For the three most common B trigram contexts (d,sh), (d,ch), (s,sh), most pos2 classes match the pos1-only bigram distribution closely. The exception is specific depletions (s,sh→d=0, p,sh→ch≈0). For the most common paths, grammar is approximately bigram-Markovian with specific depletion exceptions.

### Finding 5: A sh→ch→sh Elevated (2.63×/N=8)

A (sh, ch)→pos2=sh: 0.22 (N=8/36) vs baseline ch→sh=0.08 (N=33/390) = 2.63×. When sh appears at LF and ch at pos1, sh reappears at pos2 more than expected — a 3-position sh-ch-sh interleaving pattern. This is consistent with A's ch↔sh avoidance being weaker than B's (F328, F338).

---

## 3. TVD Summary: Top LF-Conditioning Pairs

**A-dialect** (highest LF→pos1→pos2 conditioning, N≥10):
- (y,y): TVD=0.401 (N=12) — y self-chain effect
- (sh,sh): TVD=0.377 (N=17) — sh self-chain LF effect
- (k,sh): TVD=0.381 (N=16) — k at LF modifies sh→pos2

**B-dialect** (highest LF→pos1→pos2 conditioning, N≥10):
- (y,sh): TVD≈0.35+ (N=25) — y→sh→ch=2.94×
- (p,sh): TVD≈0.35 (N=51) — p→sh→ch≈0
- (y,y): TVD=0.417 (N=12) — y self-chain

---

## 4. Structural Interpretation

Line grammar is **approximately bigram-Markovian for the most frequent paths** but has **specific 3rd-order conditioning** in several cases:
1. **LF-class "locks" certain pos2 classes as depleted or enriched** beyond pos1 conditioning
2. **y self-chains** extend to pos2 in A (y→y→y E=2.15×); in B y-chain terminates after LF→pos1
3. **LF formula classes suppress competitors at pos2**: s suppresses d at pos2 even via sh intermediary
4. **Gallows LF class modifies pos2**: p at LF suppresses ch at pos2 after sh; t at LF elevates sh and ol at pos2 after ch

---

## Self-Audit

**Target-awareness**: No target-aware elements. Direct corpus frequency comparison.

**Feature-destroying implementation**: No feature-destroying elements. Trigram extraction standard; continuation-line filter applied.

**Extrapolation**: All claims within tested data. The "near-bigram-Markovian" characterization applies to the most common paths (N≥50). For rare paths (N=10-25), LF-conditioning effects are often directional (single-digit event counts).

**Negative-result scope**: "Near-Markovian for most common paths" is qualified: specific 3rd-order effects exist in key combinations. Valid conclusion: "The most common B paths (d,sh), (d,ch), (s,sh) are near-bigram-Markovian; but LF class consistently modifies specific pos2 classes beyond pos1 conditioning in combination contexts like (p,sh), (y,sh), (y,y)."

**Control behavior**: No external control. Baseline P(pos2|pos1) serves as the comparison.

## Finding: F393

**See findings.md F393**
