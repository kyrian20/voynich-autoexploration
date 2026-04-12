# exp_402: A Continuation Line Opening Trigram Inventory (H627)

**Date:** 2026-04-11
**Hypothesis tested:** H627 — What is A's formula-typed fraction? Are A's formula trigrams different from B's?
**Outcome:** A formula-typed fraction=7.6%(N=103/1360) — slightly BELOW B's 9.3%(N=211/2276). A top trigrams are ch-pos1 dominated (d→ch→ch N=16 top) vs B sh-pos1 dominated (d→sh→qok N=24 top). A-specific formula types: sh→ch→sh=2.69×(N=8); t→ch→sh=3.27×(N=5); o→sh→cth=4.33×(N=4); qok→ch→qok=3.10×(N=5). y→sh→ch NOT in A formula list — A/B inversion confirmed. A pos1=ch=28.6% vs B=19.0%.

---

## 1. Corpus

A continuation lines (≥3 words): **N=1360**.

LF class breakdown: d=17.1%, y=14.4%, t=7.6%, o=7.4%, sh=7.4%, ch=6.9%, qok=6.5%, s=6.4%, ok=4.9%, qot=4.9%, ot=3.9%, k=3.4%, p=2.8%.

pos1 class breakdown: **ch=28.6%** (vs B=19.0%), sh=15.6% (vs B=16.9%), d=8.5% (vs B=3.0%), other=7.6%, ok=5.0%, cth=4.8% (vs B=tiny), o=4.8%, qok=4.6% (vs B=12.3%).

**Key A vs B pos1 differences:**
- A ch at pos1 = 28.6% (much higher than B 19.0%)
- A qok at pos1 = 4.6% (much lower than B 12.3%)
- A d at pos1 = 8.5% (much higher than B 3.0%)
- A cth at pos1 = 4.8% (vs B ~0.1% — A-specific)

---

## 2. Top Trigrams by Frequency (A)

| LF | pos1 | pos2 | N | E_cond |
|---|---|---|---|---|
| d | ch | ch | 16 | 0.90× (near-Markovian) |
| d | ch | d | 13 | 1.43× (mild) |
| s | ch | ch | 13 | 1.43× (mild) |
| y | ch | ch | 13 | 1.01× (near-Markovian) |
| sh | ch | ch | 12 | 1.17× (near-Markovian) |
| ch | ch | ch | 11 | 1.04× (near-Markovian) |
| qot | ch | ch | 10 | 1.31× (mild) |
| o | ch | ch | 9 | 1.06× (near-Markovian) |
| **sh** | **ch** | **sh** | **8** | **2.69×** (formula-typed) |
| y | ch | d | 8 | 1.22× (near-Markovian) |

The top 8 most frequent A trigrams are all near-Markovian with pos1=ch. The first formula-typed trigram appears at rank 9: sh→ch→sh=2.69×(N=8).

**B comparison for the same 9th slot:** y→sh→ch=2.88×(N=8) — B's first formula type has y→sh while A's has sh→ch. Different LF classes and pos1 classes.

---

## 3. Formula-Type Classification

**Formula-typed lines (E_cond≥2.0, N≥3): 103 (7.6%)**
**Near-Markovian lines: 1257 (92.4%)**
**Distinct formula trigrams: 27** (vs B: 55)

### A-specific formula types (not seen in B):

| LF | pos1 | pos2 | N | E_cond | Interpretation |
|---|---|---|---|---|---|
| y | ol | ol | 3 | 6.40× | y-LF → ol self-routing (directional) |
| ok | ok | sh | 3 | 6.38× | ok self-succession then sh (directional) |
| o | sh | cth | 4 | **4.33×** | o-LF → sh → cth continuation (A cth-dominant) |
| **t** | **ch** | **sh** | **5** | **3.27×** | t→ch→sh interleaving (= F399: 3.28×) CONFIRMED |
| d | ch | t | 4 | 3.19× | d→ch→t continuation |
| **sh** | **ch** | **sh** | **8** | **2.69×** | sh-LF → ch → sh return (A sh↔ch interleaving) |
| t | ol | d | 3 | 2.67× | t-LF → ol → d routing (directional) |
| qot | ch | cth | 4 | 2.60× | A qot → ch → cth (cth routing specific to A) |

### A formula types shared with B (overlap):

| Trigram | A E | B E | Status |
|---|---|---|---|
| qok→ch→qok | 3.10×(N=5) | 1.61×(N=15) | Stronger in A |
| y→d→ok | 3×(N=3,dir) | from F401 t→d→ok | Different LF class |

### B formula types ABSENT in A:

| B formula | B E | A E | Interpretation |
|---|---|---|---|
| y→sh→ch | 2.88×(N=8) | 0.62×(N≈2, depleted) | A/B inversion confirmed (F400) |
| p→sh→qot | 2.04×(N=8) | not in A formula list | p→sh grammar different in A |
| qok→sh→k | 4.16×(N=5) | not in A formula list | A qok very different at pos1 |
| s→sh→l | 2.06×(N=6) | not in A formula list | s formula type B-specific |

---

## 4. Key Interpretations

### 4.1 A Grammar is Also Predominantly Near-Markovian

A formula-typed fraction (7.6%) is nearly equal to B (9.3%). Both dialects have overwhelmingly near-Markovian trigram grammar. The structural grammar operates primarily at the pos1→pos2 bigram level (ch→ch, ch→d), not the LF-conditional pos2 level.

### 4.2 A Top Trigrams Are ch-Dominated; B Top Trigrams Are sh-Dominated

A's top 8 most frequent trigrams all have pos1=ch. B's top 3 most frequent trigrams have pos1=sh (d→sh→qok, s→sh→qok) or pos1=ch (d→ch→ch). This reflects:
- A ch at pos1 = 28.6% (vs B = 19.0%) — A is more ch-pos1-concentrated
- B qok at pos1 = 12.3% (vs A = 4.6%) — B has more qok at pos1 (from sh→qok enrichment, F326)
- A d at pos1 = 8.5% (vs B = 3.0%) — A has more d self-routing at pos1

This is a major pos1 distribution difference, not captured by onset-class-level analysis before.

### 4.3 y→sh→ch Inversion Directly Confirmed

In B: y→sh→ch=2.88×(N=8) — top formula type.
In A: y→sh→ch is NOT in A's formula list. In exp_396 (F400), A y→sh→ch=0.62×(depleted, N=2). The exp_402 trigram inventory directly confirms: when we search for formula-typed trigrams in A, y→sh→ch does NOT appear. The A/B inversion (F400) is structurally confirmed in the full trigram space: y→sh routing in A does not produce ch at pos2.

### 4.4 A sh↔ch Interleaving Visible as LF-Formula

A sh→ch→sh=2.69×(N=8) is the first formula-typed trigram in A by frequency. This connects to:
- F393: A sh→ch→sh=2.63× (from MID context)
- F400: A sh self-chain extends to 3 positions (1.72×)
- F338: A ch→sh unidirectionality is genuine

When sh appears at LF in A, it tends to alternate ch→sh at positions 1 and 2. This is an A-specific LF-opening formula: the sh-opening line interleaves with ch.

### 4.5 A Fewer Distinct Formula Trigrams (27 vs B 55)

A has 27 distinct formula trigrams vs B's 55. Given A has 60% of B's line count (1360 vs 2276), we'd expect ~33 by scaling. The 27 vs 33 expected suggests A may have slightly fewer formula trigrams per line count, but the difference is small and could reflect corpus size effects.

---

## 5. Limitations

- Same thresholding caveat as exp_401: E_cond≥2.0, N≥3.
- A corpus smaller (1360 vs 2276 B cont lines), so many A trigrams are directional (N=3-4) where B had N=5-8 for the corresponding formula types.
- The A/B comparison uses the same threshold; A's smaller N means some formula effects may not reach N≥3 and appear to be "absent" when they are actually rare.
- "Not in A formula list" ≠ "depleted in A" for low-N cases.

---

## Self-Audit

**Target-awareness**: No target-aware elements. Within-corpus structure analysis.

**Feature-destroying implementation**: No feature-destroying elements.

**Extrapolation**: "y→sh→ch not in A formula list" is consistent with F400 (A y→sh→ch=0.62×, depleted). Not claiming the absence proves the depletion — just confirms that when searching A's full trigram space, y→sh→ch does not emerge as formula-typed. PASS.

**Negative-result scope**: A/B formula-typed fraction difference (7.6% vs 9.3%) is a small difference; not claiming A is "less formula-typed" — the two fractions are close and the difference may be corpus-size or threshold dependent. PASS.

**Control behavior**: No shuffle control. Baselines are A unconditional pos1→pos2 rates. Expected that A's top trigrams would be ch-dominated (given A ch pos1=28.6%); confirmed. PASS.

## Finding: F406

**See findings.md F406**
