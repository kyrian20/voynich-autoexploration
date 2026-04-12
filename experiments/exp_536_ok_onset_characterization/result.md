# exp_536 result — ok-onset full characterization (H589_archived)

## Audit

**Target-awareness**: None. Standard characterization methodology.

**Feature-destroying implementation**: Standard corpus parsing. A herbal_a = n≤56 A-dialect. B all = all B-dialect lines. qok/ok priority ordering in ONSET_PRIORITY is correct (qok priority 1, ok priority 8).

**Extrapolation**: None.

---

## Part 1: ok Vocabulary

### A herbal_a: 227 tokens, 71 types
Top words: okaiin(12.3%), oky(10.6%), okol(7.0%), okal(6.2%), okchy(4.4%), okor(4.0%), okchor(4.0%), okeey(3.5%), okchey(3.5%), okar(3.1%), okeol(2.2%), okshy(2.2%).

**A vocabulary pattern**: aiin body: okaiin (12.3%) — dominant single word. y-body: oky (10.6%). ol/or: okol+okor = 11.0%. al/ar: okal+okar = 9.3%. ch-mediated: okchy+okchor+okchey ≈ 12% — MUCH lower than ot/qot (~30%). ok has a strong aiin-body affinity absent in ot/qot.

### B all: 1040 tokens, 149 types
Top words: okaiin(13.1%), okain(10.5%), okeey(9.0%), okedy(8.3%), okeedy(7.3%), okar(7.1%), okal(6.4%), oky(3.0%), okey(2.6%), okam(1.6%).

**B vocabulary pattern**: aiin/ain: okaiin+okain = 23.6% — highest aiin-body proportion of any template class. edy/eedy: 15.6% (similar to ot 17.1%, lower than qot 22.2%). al/ar: 13.5%.

### ok vs ot/qot vocabulary divergence:
| Feature | A ok | A ot | A qot | B ok | B ot | B qot |
|---------|------|------|-------|------|------|-------|
| aiin body | **12.3%** | 6.2% | 5.2% | **23.6%** | 17.9% | 17.2% |
| ch-mediated | ~12% | ~30% | ~36% | minor | minor | minor |
| edy/eedy | — | — | — | 15.6% | 17.1% | 22.2% |
| al/ar | 9.3% | 3.1% | — | 13.5% | 15.5% | 16.4% |

**ok vocabulary DIVERGES from ot/qot**: While ot and qot share ch-mediated dominance in A and edy-dominance in B, ok has a distinctive aiin-body emphasis across both dialects (12-24% vs ot/qot's 5-17%). The ch-mediated architecture (~30%) seen in ot/qot is largely absent in ok (~12%). ok is NOT a vocabulary-parallel to ot/qot — it has its own vocabulary structure.

---

## Part 2: ok and qok Positional Distribution

### ok positional:
| Position | A obs/N | A rate | A E | B obs/N | B rate | B E |
|---------|---------|--------|-----|---------|--------|-----|
| pos1 | 53/928 | 5.7% | 1.10× | 67/1903 | 3.5% | **0.49×** |
| MID | 119/2481 | 4.8% | 0.92× | 839/10610 | 7.9% | 1.10× |
| LL | 35/829 | 4.2% | 0.81× | 154/1846 | 8.3% | 1.16× |
| LF | 55/966 | 5.7% | 1.10× | 134/1930 | 6.9% | 0.96× |

Baselines: A=5.19%, B=7.20%.

**A ok: NEUTRAL** — no position elevated to CONF. pos1 and LF both at 1.10× (slightly elevated but sub-CONF). LF slightly elevated unlike ot/qot which had LF near-baseline.
**B ok: pos1 DEPLETED (E=0.49×)** — excluded from pos1 but not as severely as B ot (E=0.34×). MID/LL slightly elevated.

### qok positional (comparison):
| Position | A obs/N | A rate | A E | B obs/N | B rate | B E |
|---------|---------|--------|-----|---------|--------|-----|
| pos1 | 62/928 | 6.7% | **1.47×** | 224/1903 | 11.8% | 0.88× |
| MID | 112/2481 | 4.5% | 0.99× | 1555/10610 | 14.7% | 1.10× |
| LL | 38/829 | 4.6% | 1.01× | 248/1846 | 13.4% | 1.01× |
| LF | 25/966 | 2.6% | **0.57×** | 150/1930 | 7.8% | **0.58×** |

**A qok: pos1 near-CONF (E=1.47×/obs=62)** — line-opener tendency (just below CONF threshold of E=1.5×). LF DEPLETED (E=0.57×). A qok avoids LF positions while preferring pos1 — partial opener profile.
**B qok: pos1 near-baseline (E=0.88×)**, LF DEPLETED (E=0.58×). B qok avoids LF more than pos1.

### Template class positional hierarchy in A:
| Class | A pos1 E | A LF E |
|-------|----------|--------|
| qot | 1.79× **CONF** | 1.01× |
| qok | 1.47× (near-CONF) | 0.57× DEPL |
| ot | 1.29× (sub-CONF) | 1.01× |
| ok | 1.10× (neutral) | 1.10× |

The qo-prefixed classes (qot, qok) are pos1-elevated; non-prefixed (ot, ok) are pos1-neutral. qot is the strongest opener (CONF), qok shows a weaker but similar tendency (near-CONF). The positional gradient: qot > qok > ot > ok at pos1. In LF: qok DEPL while others near-baseline.

**H589_archived assessment**: qok/ok do NOT form a mirror-image spatial pair analogous to qot/ot. A qot is strongly pos1-elevated (CONF) while A ot is neutral — a clear positional contrast. But qok is only near-CONF and ok is neutral — too close together to constitute a mirror. The pattern is better described as: qo-prefix confers line-opener tendency (qot>qok), while non-prefixed template classes are neutral (ot, ok).

F539: Template class positional hierarchy (A herbal_a): qot=CONF opener (E=1.79×/F533) > qok=near-CONF opener (E=1.47×/obs=62) > ot=neutral (E=1.29×) > ok=neutral (E=1.10×). B-dialect: all four depleted at pos1 (ot=0.34×, ok=0.49×, qot=0.60×, qok=0.88×). qo-prefix confers line-opener tendency in A; qok LF-depleted in BOTH dialects (A: E=0.57×; B: E=0.58×).

---

## Part 3: ok Within-Line Bigrams

### A herbal_a (172 ok sender bigrams):
| ok→X | obs | E | flag |
|------|-----|---|------|
| ok→ok | 18 | 2.10× | **CONF** |
| ok→ch | 50 | 1.11× | baseline |
| ok→qo | 6 | 1.67× | 1.67× |
| ok→d | 21 | 0.70× | DEPL |

**A ok→ok CONF** (E=2.10×/obs=18) — strong A-specific self-succession. ok→ch is BASELINE (E=1.11×) — unlike ot→ch which was DEPLETED (E=0.77×, F537). ok does NOT avoid ch.

### B all (906 ok sender bigrams):
| ok→X | obs | E | flag |
|------|-----|---|------|
| ok→ch | 189 | 1.12× | baseline |
| ok→ok | 87 | 1.24× | 1.24× |
| ok→ot | 78 | 1.20× | 1.20× |
| ok→qok | 116 | 0.94× | DEPL |
| ok→a | 39 | 0.78× | DEPL |

**B: NO CONF signals for ok**. ok→ok = 1.24×/obs=87 — below CONF (need E≥1.5×). This contrasts with B ot→ot CONF (E=2.12×, F537). B ok self-succession is NOT confirmed. ok→ch baseline (E=1.12×) — same as A.

### ok vs ot within-line key distinction:
| | A ok | A ot | B ok | B ot |
|--|------|------|------|------|
| Self-succession | CONF (2.10×) | CONF (1.79×) | 1.24× (sub-CONF) | **CONF (2.12×)** |
| →ch | baseline (1.11×) | **DEPL (0.77×)** | baseline (1.12×) | **DEPL (0.85×)** |

A ok self-succession CONF but B ok sub-CONF. ot self-succession CONF in BOTH dialects. ok→ch baseline vs ot→ch depleted — ok is more ch-neutral than ot.

---

## Part 4: ok-LF Lines

### A herbal_a ok-LF (51 lines, 5.3%):
- y: E=1.52×/obs=11 → **CONF** — re-confirms F455 (A ok-LF pos1=y CONF)
- s: E=2.22×/obs=5 → dir (NEW — not previously documented)

### B all ok-LF (132 lines, 6.8%):
- t: E=1.95×/obs=16 → **CONF** (NEW — B ok-LF opens with t-class at CONF level)
- y: E=1.22×/obs=22 — below CONF

**F455 re-confirmed** (A ok-LF pos1=y: E=1.52×/obs=11, exactly at CONF threshold).
**NEW F540**: B ok-LF pos1=t CONF (E=1.95×/obs=16). B ok-terminal lines open with t-onset at CONF level. This is unexpected — t is a line-opener in B (via s-class words sh/s), and ok-LF lines specifically recruit t-onset at CONF.

---

## Self-Audit

**Target-awareness**: No target-aware elements identified.

**Feature-destroying implementation**: ONSET_PRIORITY places qok (priority 1) before ok (priority 8), correctly partitioning the two classes. No word starting with 'ok' can be classified as 'qok'. Standard methodology.

**Extrapolation**: All claims within tested parameter range.

**Negative-result scope**: H589_archived's spatial pair hypothesis receives a nuanced negative: the pair structure is real but weak. qo-prefix confers opener tendency (qot>qok both pos1-elevated) while non-prefixed (ot>ok) are neutral. The spatial PAIR framing overstates the structural contrast.

**Control behavior**: No controls used. Within-corpus baselines used throughout.

---

## Summary: ok Characterization and H589_archived Assessment

| Feature | A herbal_a ok | B all ok |
|---------|--------------|---------|
| Dominant words | okaiin (12.3%), oky (10.6%) | okaiin+okain (23.6%), okeey+edy (15.6%) |
| Positional role | NEUTRAL (pos1=1.10×, LF=1.10×) | MID/LL class (pos1 DEPL E=0.49×) |
| Self-succession within-line | **CONF (E=2.10×/obs=18)** | sub-CONF (E=1.24×/obs=87) |
| ok→ch | baseline (E=1.11×) | baseline (E=1.12×) |
| ok-LF pos1 | y CONF (F455); s dir (NEW) | **t CONF (E=1.95×/obs=16, NEW)** |
| Vocab parallel to ot/qot? | **NO** — aiin-dominated, ch-mediated ~12% | **NO** — higher aiin, different structure |

**qok/ok spatial pair: WEAKLY SUPPORTED.** A qok is pos1 near-CONF (E=1.47×) and ok is neutral (E=1.10×). This is a real gradient (qot>qok>ot>ok at pos1) but not a mirror-image pair. H589_archived's spatial pair hypothesis is CLOSED NEGATIVE — the pattern is a qo-prefix gradient, not a discrete spatial pair.

**New findings: F539 (template class hierarchy), F540 (B ok-LF pos1=t CONF)**
**F455 and Q010 status**: A ok-LF pos1=y exactly CONF (E=1.52×/obs=11). Q010 was about whether E≥1.5× is achieved. Current result: E=1.52×, exactly at CONF — consistent with Q010 resolution (CONF restored).
**H589_archived CLOSED.**
