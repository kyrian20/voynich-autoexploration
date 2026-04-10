# exp_139: A-Herbal cth Breakpoint & l-Gradient Dialect Analysis
**Date**: 2026-04-09
**Hypotheses**: H275 (A-herbal cth gradient: smooth vs breakpoint), H276 (A-herbal l-gradient: B-vocabulary contamination?)
**Status**: H275 CONFIRMED (SMOOTH GRADIENT), H276 NOT CONFIRMED (INSUFFICIENT DATA)

---

## H275: A-HERBAL cth DECLINE — SMOOTH GRADIENT (CONFIRMED)

The A-herbal cth decline is a **smooth, monotonic gradient** across folio sequence, not a step-change at a specific breakpoint.

### Tertile Analysis
| Tertile | Folios | n words | cth% | l% |
|---------|--------|---------|------|-----|
| T1 (early) | f1-f16 | 2048 | **5.957%** | 0.391% |
| T2 (mid) | f16-f32 | 2056 | **4.815%** | 0.438% |
| T3 (late) | f35-f56 | 2184 | **3.663%** | 0.916% |
| Ratio T3/T1 | | | **0.615×** | **2.34×** |

cth declines by roughly equal amounts at each stage: T1→T2: −1.14 pp; T2→T3: −1.15 pp. This equal-interval decline is consistent with a **continuous content or scribal drift**, not a discrete scribe change.

### 5-Folio Window Progression
| Window | cth% | l% |
|--------|------|----|
| f1-f3 | 5.870% | 0.839% |
| f3-f5 | 5.923% | 0.000% |
| f6-f8 | 5.897% | 0.737% |
| f8-f10 | 7.670% | 0.284% |
| f11-f14 | 2.593% | 0.000% |
| f14-f16 | 6.522% | 0.000% |
| f17-f19 | 5.419% | 0.000% |
| f19-f21 | 4.336% | 1.084% |
| f22-f24 | 5.412% | 0.706% |
| f24-f27 | 3.448% | 0.345% |
| f28-f30 | 5.128% | 0.000% |
| f30-f35 | 4.348% | 1.449% |
| f36-f38 | 5.300% | 0.353% |
| f38-f44 | 5.610% | 0.976% |
| f45-f49 | 3.183% | 1.326% |
| f49-f52 | 3.101% | 0.517% |
| f53-f55 | 1.970% | 0.739% |
| f56-f56 | 3.067% | 0.613% |

High within-window variance (f11-f14: 2.6% vs f15: ~10-11%) makes it impossible to identify a single breakpoint. The change-point scan best breakpoint is **f54** (mean-cth difference = 0.0297) — the very last A-herbal folios (f53-f56) have the lowest cth (~2%). But this "breakpoint" captures the endpoint of a continuous trend, not a discrete scribal transition.

### Spearman Correlations (A-herbal folio-sides, n=87)
- cth: **ρ=-0.269** (weaker than exp_138 ρ=-0.353 because recto/verso treated separately, adding within-folio noise)
- l: **ρ=+0.627** (STRONGER — l-increase is more consistent than cth-decrease)

**The l-gradient (ρ=+0.627) is STRONGER than the cth-gradient (ρ=-0.269) within A-herbal.** Later A-herbal folios show a more consistent shift toward l-onset words than they show cth depletion.

### Interpretation
The equal-interval decline across tertiles (not a step) rules out a single scribal hand change at a specific folio. Possible mechanisms:
1. **Content gradient**: Herbal folios are organized by botanical type; later plants have different vocabulary that intrinsically uses fewer cth-nominal forms
2. **Continuous scribal drift**: The same scribe gradually changed writing habits across the herbal section
3. **Dialect-creep**: Later A-herbal folios, approaching the A/B boundary (B-herbal insertions, B-cosmo section at f75+), show gradual vocabulary drift toward B-like patterns (less cth, more l)

---

## H276: A-HERBAL l-GRADIENT — NOT CONFIRMED (INSUFFICIENT DATA)

The A-herbal l-gradient exists (ρ=+0.627) but the individual l-onset word sample is too small to characterize the B-contamination hypothesis.

### l-Word Sample Sizes
- Early A-herbal (f1-f28): **16 tokens, 14 types**
- Late A-herbal (f29-f57): **21 tokens, 21 types**

With only 37 total l-onset tokens across all A-herbal, each l-word is essentially a hapax (21 types in 21 late tokens). Statistical inference is unreliable.

### Suffix Paradigm Split of l-Onset Words
| Period | A-suffix% | B-suffix% | other% | n tokens |
|--------|-----------|-----------|--------|---------|
| Early (f1-f28) | 50.0% | **0.0%** | 50.0% | 16 |
| Late (f29-f57) | 42.9% | **28.6%** | 28.6% | 21 |

Late A-herbal has 28.6% B-suffix l-words (6/21) vs 0% in early. The B-suffix forms in late A-herbal:
- `l,dy<->dain` (transcription artifact with comma and `<->` line-continuation)
- `l,chaiin` (comma artifact)
- `lodaly<->oteey` (line-continuation artifact)
- `loldaiin` (clean B-form: l+ol+daiin compound, aiin suffix)
- `lkeedy` (clean B-form: lk-prefixed with -eedy suffix)
- `lkeey` (clean B-form: lk-prefixed with -eey suffix)

Of the 6 "B-suffix" l-words, **4 are transcription artifacts** (comma-separated multi-part tokens). Only `loldaiin`, `lkeedy`, `lkeey` are clean l-onset words with B-paradigm suffixes (3/21 tokens = 14.3%).

### Corpus-Wide Dialect Distribution of Late A-Herbal l-Words
Top late A-herbal l-words by corpus-wide dialect:
| Word | A corpus | B corpus | B% | Appears in late A-herbal |
|------|----------|----------|-----|------------------------|
| lor | 3 | 31 | 91.2% | 1 token |
| lo | 1 | 11 | 91.7% | 1 token |
| lchor | 1 | 2 | 66.7% | 1 token |
| lshy | 2 | 1 | 33.3% | 1 token |

The most frequent late A-herbal l-words (`lor`, `lo`) are predominantly B-dialect corpus-wide. This is **weak evidence** that the l-gradient in A-herbal involves B-dialect vocabulary appearing in otherwise A-dialect folios — but the sample (1 occurrence each) is far too small for confidence.

### Bottom Line
H276 cannot be confirmed or refuted with current data. The l-gradient (ρ=+0.627) is real, but the absolute number of l-onset words in A-herbal is too small (37 total tokens across all A-herbal) and too contaminated by transcription artifacts to characterize the mechanism. A larger analysis combining all l-onset words across dialect boundaries would be needed.

---

## Summary of New Findings (F146)

1. **A-herbal cth decline is SMOOTH (equal-interval across tertiles, not step-change)**: T1=5.96%→T2=4.82%→T3=3.66% (−1.14 pp, −1.15 pp). Best change-point at f54 (diff=0.030) is endpoint of continuous trend. Rules out single scribal hand-change; supports content gradient or continuous scribal drift.
2. **l-gradient in A-herbal is STRONGER than cth-gradient**: l Spearman ρ=+0.627 vs cth ρ=-0.269 within A-herbal. Later A-herbal shows more consistent shift toward l-onset words than cth depletion.
3. **A-herbal l-words are too sparse to characterize dialect origin**: Only 37 total l-tokens in all A-herbal (16 early, 21 late). Many are transcription artifacts. Clean B-form l-words in late A-herbal: lkeedy(1), lkeey(1), loldaiin(1) — 3 tokens. Insufficient for statistical inference on B-vocabulary contamination.

---

## Hypotheses Spawned
- **H277**: Is the A-herbal cth smooth gradient explained by plant-type content organization? If later herbal folios contain plants whose names/descriptions inherently use fewer cth-nominal forms (cthy/cthol/cthey), the gradient would reflect content, not scribal drift. Test: identify which cth-words disappear in late A-herbal.
- **H278**: What is the l-onset vocabulary in B-dialect sections (cosmo, stars, pharma)? The 37 l-tokens in all A-herbal contrast with presumably many more in B sections. Characterizing the full B-dialect l-vocabulary would provide a reference for comparing the 3 clean l-forms found in late A-herbal.
