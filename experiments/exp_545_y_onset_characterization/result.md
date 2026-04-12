# exp_545 result — y-onset full characterization (H_new_FG)

## Audit

**Target-awareness**: None. Standard characterization methodology.

**Feature-destroying implementation**: y onset (priority 17 in ONSET_PRIORITY, after sh/ok/ot/ol/d/s, before k/t) correctly extracted. No bare 'y' word exists in either corpus sample (single-char 'y' proportion = 0.0 in both) — all y-onset words are compound forms at least 2 chars.

**Extrapolation**: None.

---

## Part 1: y Vocabulary

### A herbal_a: 671 tokens, 274 types
Top words: ykeey(4.6%), ykaiin(3.7%), ykar(2.7%), ytaiin(2.4%), ychor(2.1%), ykchy(1.9%), ytchy(1.9%), ytar(1.8%), yty(1.6%), ycheey(1.5%), ychey(1.5%).

**A y vocabulary**: Diverse (274 types / 671 tokens — highest type/token ratio of any characterized class). All forms are y+[gallows/bench+body] compound structures. Top forms: k-gallows+body (ykeey, ykar, ykaiin, ykchy), t-gallows+body (ytaiin, ytchy, ytar, yty, ytor), ch-bench+body (ychor, ycheey, ychey). No bare 'y' — y-onset words always carry additional structure.

### B all: 330 tokens, 140 types
Top words: yteedy(6.4%), ykeedy(6.1%), ytedy(3.9%), ykeey(3.6%), ykedy(3.3%), ykaiin(3.3%), ychedy(3.0%), ykar(2.7%), ytaiin(2.7%), ytchedy(2.4%).

**B y vocabulary**: edy-body forms dominant in B (yteedy, ykeedy, ytedy, ykedy, ychedy, etc.). A→B vocabulary shift in y-class: A y-words are gallows+aiin/al/ol-body; B y-words adopt edy-body while retaining gallows onset (y+gallows+edy). The y-class vocabulary follows the dialect shift (A=complex compound; B=edy-dominated) but with y always providing the onset prefix.

---

## Part 2: y Positional Distribution

| Position | A obs/N | A rate | A E | B obs/N | B rate | B E |
|---------|---------|--------|-----|---------|--------|-----|
| pos1 | 323/1961 | 16.5% | **2.78× CONF** | 147/1279 | 11.5% | **3.54× CONF** |
| MID | 265/7333 | 3.6% | **0.61× DEPL** | 158/7601 | 2.1% | **0.64× DEPL** |
| LL | 62/1794 | 3.5% | **0.58× DEPL** | 24/1266 | 1.9% | **0.58× DEPL** |
| LF | 72/1961 | 3.7% | **0.62× DEPL** | 25/1279 | 2.0% | **0.60× DEPL** |

Baselines: A=5.9%, B=3.2%.

**Y is the most pos1-exclusive class in VMS grammar**: pos1 STRONGLY CONF in BOTH dialects (A: E=2.78×; B: E=3.54×) — the highest cross-dialectal pos1 enrichment of any characterized class. All other positions (MID, LL, LF) are DEPLETED in both dialects (~0.58-0.64×). Y uniquely occupies the pos1 slot only — it opens lines and appears nowhere else at elevated rates.

**Comparison to all characterized classes at pos1:**
| Class | A pos1 E | B pos1 E | Nature |
|-------|----------|----------|--------|
| **y** | **2.78× CONF** | **3.54× CONF** | **STRONGEST line-opener, both dialects** |
| d | 1.47× near-CONF | 2.64× CONF | A: LF-primary; B: pos1-primary |
| qot | 1.79× CONF | 0.60× DEPL | A-only opener |
| qok | 1.47× | 0.88× | A-only sub-opener |
| ch | 0.38× DEPL | 0.25× DEPL | pos1-avoider |
| sh | 1.03× neutral | 0.70× DEPL | MID class |

Y is the dominant pos1 class in A herbal_a (16.5% of line starts, second only to d). In B, y at 11.5% and d at 19.2% together account for 30.7% of all B line starts.

---

## Part 3: y Within-line Bigrams (y→X)

### A herbal_a (588 y sender bigrams):
| y→X | obs | E | flag |
|-----|-----|---|------|
| y→y | 40 | **1.88×** | **CONF** |
| y→ckh | 13 | **1.73×** | **CONF** |
| y→k | 25 | 1.24× | sub-CONF |
| y→l | 16 | 1.22× | sub-CONF |
| y→ch | 125 | 0.95× | ~baseline |
| y→qok | 29 | 0.67× | DEPL |

**A: TWO CONF signals.** y→y self-succession CONF (E=1.88×/obs=40). y→ckh CONF (E=1.73×/obs=13) — y routes specifically to compound gallows. y→ch is ~baseline (0.95×). y→qok DEPLETED (0.67×).

### B all (305 y sender bigrams):
| y→X | obs | E | flag |
|-----|-----|---|------|
| y→y | 20 | **3.18×** | **CONF** |
| y→k | 11 | **1.68×** | **CONF** |
| y→t | 7 | 1.74× | sub-CONF |
| y→ch | 57 | 1.01× | baseline |
| y→qok | 43 | 0.92× | ~baseline |
| y→ot | 16 | 0.71× | DEPL |

**B: TWO CONF signals.** y→y self-succession CONF (E=3.18×/obs=20) — STRONGER than A (3.18× vs 1.88×). y→k CONF (E=1.68×/obs=11) — y routes to simple gallows k in B. y→ch baseline (1.01×). y→t elevated (1.74×/obs=7) — approaching CONF but N insufficient.

### A/B y bigram comparison:
| Target | A E×(obs) | B E×(obs) |
|--------|-----------|-----------|
| y→y | CONF (1.88×/40) | **CONF (3.18×/20)** |
| y→ckh | CONF (1.73×/13) | (ckh rare in B) |
| y→k | 1.24×(25) sub-CONF | **CONF (1.68×/11)** |
| y→ch | ~baseline (0.95×/125) | baseline (1.01×/57) |
| y→qok | DEPL (0.67×/29) | ~baseline (0.92×/43) |

**Cross-dialectal conserved**: y→y CONF in BOTH dialects (stronger in B). y routes to gallows class: compound gallows (ckh) in A; simple gallows (k) in B. Y→ch is baseline in both — no ch avoidance (unlike sh→ch F328). Y→qok DEPLETED in A (0.67×).

**Gallows affinity**: y consistently routes to gallows-type classes after appearing at pos1 or as self-successor: ckh (compound gallows) in A; k in B. The gallows-after-y pattern is structurally consistent cross-dialectally.

---

## Part 4: y-LF Lines Pos1 Profile

### A herbal_a y-LF (72 lines, 3.7%):
**NO CONF signals.** Best: k at pos1 (dir): E=2.55×/obs=3 (barely dir-threshold, insufficient). y-self: E=1.35×/obs=16 (sub-CONF). ot: E=1.79×/obs=5 (sub-CONF). Flat overall.

### B all y-LF (25 lines, 2.0%):
**Insufficient N for analysis** — N=25 lines, only obs=1-4 per pos1 class. Highest E: sch (5.68×/obs=1) — single observation, not meaningful.

**Y-LF pos1 is flat** (consistent with underpowering: y-LF is only 3.7% of A lines / 2.0% of B lines). Y-LF is too rare for pos1 grammar characterization.

---

## Self-Audit

**Target-awareness**: None.

**Feature-destroying implementation**: y onset correctly excludes 'y' as a standalone word (not present in corpus as a single-char word). y priority (17) correctly places it after s/d/ol etc. y→y self-succession within-line is genuine (consecutive y-onset words in same line, not cross-line).

**Extrapolation**: None.

**Negative-result scope**: y-LF pos1 flat is an N-limited result (72 A lines, 25 B lines) — not a clean null but an underpowered test. Cannot claim y-LF grammar is absent; only that it is undetected.

---

## Summary: y Characterization

| Feature | A herbal_a | B all |
|---------|-----------|-------|
| Vocabulary | gallows+body compounds (yk-, yt-, ych-); no bare 'y' | edy-body dominant (yteedy, ykeedy); same gallows onset |
| Positional role | **pos1 CONF (2.78×/323)** — strong opener; MID/LL/LF DEPL (~0.60×) | **pos1 CONF (3.54×/147)** — strongest opener; MID/LL/LF DEPL (~0.60×) |
| Within-line self-succession | **CONF (1.88×/obs=40)** | **CONF (3.18×/obs=20)** |
| Key within-line targets | **y→ckh CONF (1.73×/13)** — compound gallows | **y→k CONF (1.68×/11)** — simple gallows |
| y→ch | ~baseline (0.95×) | baseline (1.01×) |
| y-LF pos1 | flat (underpowered, N=72) | flat (underpowered, N=25) |

**F557 (y vocabulary)**: A y = gallows+body compounds (yk, yt, ych forms); B y = edy-body dominant (yteedy, ykeedy). Vocabulary follows dialect shift like template classes but maintains y-prefix gallows affinity. Y-vocabulary is the most type-diverse class (A: 274/671 = 0.41 type-token ratio).

**F558 (y positional)**: Y is pos1-STRONGLY-CONF in BOTH dialects (A: E=2.78×/obs=323; B: E=3.54×/obs=147) — the highest cross-dialectal pos1 enrichment of any characterized class. ALL other positions DEPLETED in both dialects (MID/LL/LF ~0.58-0.64×). Y is the definitive **line-opener class** in VMS: it opens lines universally and avoids all other positions cross-dialectally.

**F559 (y within-line)**: y→y CONF cross-dialectally (A: 1.88×/40; B: 3.18×/20). Y routes to gallows: y→ckh CONF in A (1.73×/13); y→k CONF in B (1.68×/11). Gallows routing after y-pos1 words is a dialect-dependent but structurally consistent pattern (compound gallows in A; simple gallows in B). Y→ch is baseline in both dialects (no avoidance, unlike sh→ch).

**New findings: F557, F558, F559**
**H_new_FG CLOSED.**
