# exp_401: B Continuation Line Opening Trigram Inventory (H618)

**Date:** 2026-04-11
**Hypothesis tested:** H618 — What are the most common B continuation line (LF, pos1, pos2) trigrams? What fraction of lines are formula-typed vs near-Markovian?
**Outcome:** 9.3% of B continuation lines are formula-typed (E_cond≥2.0, N≥3). 90.7% are near-Markovian. The most frequent trigrams (d→sh→qok N=24, s→sh→qok N=21) are near-Markovian (E_cond≈1.1×). Known formula types confirmed (y→sh→ch=2.88×; p→sh→qot=2.04×; qok→sh→k=4.16×; s→sh→l=2.06×; p→ch→ot=5.33×). New: d→ot→ot=4.13×(N=5); qok→ch→qo=2.62×(N=8); d→qok→ol=2.51×(N=6).

---

## 1. Corpus

B continuation lines (≥3 words): **N=2276**.

LF class breakdown: d=15.2%, y=11.7%, s=11.5%, qok=10.3%, p=10.1%, t=9.0%, sh=5.4%, ch=3.8%, o=3.2%, ok=3.1%, ol=3.1%, qo=2.9%, l=2.7%, ot=2.2%, qot=2.0%, k=1.4%.

pos1 class breakdown: ch=19.0%, sh=16.9%, qok=12.3%, ok=7.3%, other=6.6%, ol=6.2%, l=5.1%, qo=4.3%, o=4.2%, ot=3.8%.

---

## 2. Top Trigrams by Frequency

| LF | pos1 | pos2 | N | E_cond |
|---|---|---|---|---|
| d | sh | qok | 24 | 1.12× (near-Markovian) |
| s | sh | qok | 21 | 1.28× (near-Markovian) |
| d | ch | ch | 15 | 1.04× (near-Markovian) |
| qok | ch | qok | 15 | 1.61× (mild) |
| d | ch | qok | 14 | 1.04× (near-Markovian) |
| y | ch | ch | 13 | 1.44× (mild) |
| d | ch | l | 12 | 1.75× (mild) |
| s | ch | qok | 11 | 1.30× (near-Markovian) |
| qok | sh | qok | 10 | 1.14× (near-Markovian) |
| y | sh | ch | 8 | **2.88×** (formula-typed) |
| p | sh | qot | 8 | **2.04×** (formula-typed) |
| qok | ch | qo | 8 | **2.62×** (formula-typed) |

The top 9 most frequent trigrams are all near-Markovian (E_cond < 2.0). The first formula-typed trigrams appear at ranks 10-12 (y→sh→ch, p→sh→qot, qok→ch→qo).

---

## 3. Formula-Type Classification

**Formula-typed lines (E_cond≥2.0, N≥3): 211 (9.3%)**  
**Near-Markovian lines: 2065 (90.7%)**  
**Distinct formula trigrams: 55**

### Strongest formula-typed trigrams (E_cond≥4.0, N≥3):

| LF | pos1 | pos2 | N | E_cond | Status |
|---|---|---|---|---|---|
| t | d | ok | 3 | 6.80× | NEW (directional) |
| qot | qok | qot | 3 | 6.48× | NEW (directional) |
| p | ch | ot | 4 | 5.33× | = F398 (5.28×, confirmed) |
| sh | o | ot | 3 | 5.28× | NEW (directional) |
| ok | ch | qo | 3 | 4.91× | NEW (directional) |
| qok | sh | k | 5 | 4.16× | = F398 (4.08×, confirmed) |
| d | ot | ot | 5 | **4.13×** | NEW (adequate) |
| y | sh | ch | 8 | 2.88× | = F398 (2.94×, confirmed) |

### Notable formula-typed trigrams (E_cond 2.0-4.0, N≥5):

| LF | pos1 | pos2 | N | E_cond | Notes |
|---|---|---|---|---|---|
| qok | ch | qo | 8 | 2.62× | qo after qok→ch (connects to qok→qo grammar) |
| d | qok | ol | 6 | 2.51× | d→qok body with ol at pos2 |
| l | ch | qok | 5 | 2.96× | l LF formula type (new) |
| qok | l | qok | 5 | 2.09× | qok self-routing at pos2 via l |
| qok | ch | ol | 5 | 2.31× | qok→ch→ol |
| s | sh | l | 6 | 2.06× | = F398 (s→sh→l=2.06×, confirmed) |
| p | sh | qot | 8 | 2.04× | = F396 (p→sh→qot=2.11×, confirmed) |

---

## 4. Key Interpretations

### 4.1 B Grammar is Predominantly Near-Markovian

90.7% of B continuation lines fall into "near-Markovian" trigrams (E_cond < 2.0 or N < 3). The most common trigrams (d→sh→qok, s→sh→qok) are near-Markovian, meaning the most frequent lines do NOT show strong LF-conditional pos2 effects. The B grammar rule is: **most lines follow the local bigram chain (pos1→pos2 given only pos1), and a minority (~10%) are formula-typed (LF-conditional at pos2)**.

This is consistent with the bigram succession matrix (F326): most bigram enrichments are present regardless of LF class (e.g., sh→qok=1.97× is a global rule, not LF-conditional). The formula-typed lines represent an overlay structure on top of the dominant near-Markovian grammar.

### 4.2 All Previously Characterized Formula Types Confirmed

- y→sh→ch=2.88× (F398: 2.94×) ✓
- p→sh→qot=2.04× (F396: 2.11×) ✓
- qok→sh→k=4.16× (F398: 4.08×) ✓
- s→sh→l=2.06× (F398: 2.06×) ✓
- p→ch→ot=5.33× (F398: 5.28×) ✓

All five previously characterized formula types are reproduced in this larger-scope inventory.

### 4.3 New Formula-Typed Trigrams

**d→ot→ot=4.13×(N=5):** d at LF followed by ot→ot continuation. d is the most common B LF class (15.2%), but d→ot at pos1 is uncommon (ot pos1 = 3.8%). When d→ot occurs, ot self-routes at pos2 (ot→ot=4.13×). This connects to F383 (ot→ot self-succession in MID) and suggests d-opening lines with ot at pos1 are template-class lines that maintain ot throughout.

**qok→ch→qo=2.62×(N=8):** qok at LF followed by ch→qo continuation. qo is depleted at pos1 (4.3%) and qok→ch is the most common qok pos1 routing (15/234 qok-LF lines go to ch). qo specifically enriched at pos2 after qok→ch (connects to F383 ch→qok→qo grammar).

**l→ch→qok=2.96×(N=5):** l at LF followed by ch→qok continuation. l is a LL-enriched class (F392: l LF-depleted) but when it appears at LF, it routes to ch→qok. This suggests l-LF lines are "misplaced" LL-class lines that function like template-class continuation.

### 4.4 LF→pos1 Bigrams Are Mostly Near-Markovian

The top LF→pos1 bigrams by E are dominated by low-N combinations (f→k=9.03×, N=2; d→cth=6.58×, N=2). High-frequency p→sh is only 1.32× at the joint LF→pos1 level (P(pos1=sh|LF=p) ≈ 22% vs baseline 17% — mild enrichment). This confirms that the primary grammar rule for p is NOT "p always goes to sh at pos1" but rather "given p→sh, pos2 is strongly formula-typed (qot=2.04×; ch≈0)". The LF class primarily controls pos2 conditioning, not pos1 choice.

---

## 5. Limitations

- Formula classification threshold E_cond≥2.0 is arbitrary. At E_cond≥1.5, more lines would qualify. At E_cond≥3.0, ~5% would qualify. The 9.3% figure is threshold-dependent.
- N≥3 minimum excludes many directional E values (e.g., sh→o→ot=5.28× with N=3 is at the margin). Many directional-N formula trigrams exist but aren't counted in the 9.3%.
- The pos2 measurement is restricted to lines with ≥3 words; shorter lines are excluded.
- "Near-Markovian" does not mean independent — the bigram succession matrix (F326) shows many pos1→pos2 enrichments (e.g., sh→qok=1.97×) that apply regardless of LF. These near-Markovian effects are not captured by this LF-conditional analysis.

---

## Self-Audit

**Target-awareness**: No target-aware elements. This is a within-corpus structure analysis.

**Feature-destroying implementation**: No feature-destroying elements. The E_cond computation correctly conditions on (LF, pos1) vs (pos1) baseline.

**Extrapolation**: "90.7% of B lines are near-Markovian" is threshold-dependent (E_cond<2.0, N≥3). The correct statement is "most frequent B trigrams are near-Markovian at the LF-conditional pos2 level." Not claiming this means the grammar is random — just that LF→pos2 conditioning is weak for most line types. PASS.

**Negative-result scope**: The 9.3% formula-typed fraction does not imply "only 9.3% of lines have grammar effects" — the bigram succession rules (pos1→pos2 unconditionally) account for additional structured grammar not captured here. PASS.

**Control behavior**: No shuffle control used. Baseline is unconditional pos1→pos2 rates (same corpus). Expected that most trigrams would have E_cond near 1.0× — confirmed (top 9 most frequent trigrams all have E_cond 1.0-1.75×). The strong formula-typed trigrams (E≥4×) are few and mostly low-N. No unexpected control behavior. PASS.

## Finding: F405

**See findings.md F405**
