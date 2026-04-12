# exp_393: k-Onset Positional Census — Continuation vs Folio-Opener Lines (H606)

**Date:** 2026-04-11
**Hypothesis tested:** H606 — Why is k not LF-enriched in continuation lines despite being a folio-opener gallows class?
**Outcome:** ANSWERED — k is LF-concentrated in opener lines (A=4.32×/B=3.88×) but POSITION-GENERAL in continuation lines (A=0.79×/B=0.66× at LF), contrasting sharply with p/t/f which remain LF-enriched in BOTH line types. k is a folio-level formula class, not a line-level formula class.

---

## 1. k Positional Profile in Continuation Lines

| Dialect | LF E | pos1 E | MID E | pre_LL E | LL E | N |
|---------|------|--------|-------|----------|------|---|
| A | 0.79×(N=43) | 1.22×(N=62) | 1.08×(N=119) | 1.02×(N=45) | 0.81×(N=45) | 314 |
| B | 0.66×(N=34) | 1.04×(N=53) | 1.07×(N=219) | 1.11×(N=55) | 0.90×(N=47) | 408 |

k is essentially position-general in continuation lines — all E values are 0.66×–1.22×, close to baseline. No position is strongly enriched. In B, k is particularly MID-dominant (54% of k tokens at MID, vs ~48% baseline).

---

## 2. p/t/f Positional Profile in Continuation Lines (Comparison)

| Onset | Dial | LF E | pos1 E | MID E | LF% |
|-------|------|------|--------|-------|-----|
| p | A | 3.60×(N=41) | 0.00× | 0.56× | 62% |
| p | B | 5.90×(N=222) | 0.16× | 0.35× | 75% |
| t | A | 2.48×(N=109) | 0.41× | 0.68× | 43% |
| t | B | 3.59×(N=205) | 0.54× | 0.57× | 46% |
| f | A | 2.75×(N=9) | 1.63× | 0.60× | 47% |
| f | B | 1.69×(N=9) | 0.57× | 0.72× | 21% |

p/t remain strongly LF-enriched in continuation lines. f is also LF-enriched (A=2.75×, though N small).

---

## 3. k Positional Profile in Folio-Opener Lines

| Dialect | LF E | pos1 E | MID E | LF% |
|---------|------|--------|-------|-----|
| A | 4.32×(N=16) | 0.54× | 0.43× | 67% |
| B | 3.88×(N=8) | 0.00× | 0.64× | 50% |

In opener lines, k IS LF-enriched — comparable to p/t in those lines. A k opener LF=4.32× matches t opener LF=4.32× exactly (same E). B k opener LF=3.88× is somewhat lower than p opener (7.09×) or t opener (5.68×) but still strongly elevated.

---

## 4. Comparison: k vs p/t at LF — Opener vs Continuation

| Onset | Dial | Opener LF E | Cont LF E | Contrast |
|-------|------|------------|-----------|---------|
| k | A | 4.32× | 0.79× | 5.5× drop |
| k | B | 3.88× | 0.66× | 5.9× drop |
| p | A | 5.34× | 3.60× | 1.5× drop |
| p | B | 7.09× | 5.90× | 1.2× drop |
| t | A | 4.32× | 2.48× | 1.7× drop |
| t | B | 5.68× | 3.59× | 1.6× drop |

k shows a 5.5–5.9× drop in LF enrichment from opener to continuation lines. p and t show only 1.2–1.7× drop — they remain LF-enriched in both contexts. k is a folio-opener LF gallows class that loses its LF affinity in continuation lines.

---

## 5. Interpretation

k is structurally distinct from p/t/f within continuation lines:

**p/t/f**: "line-level formula classes" — LF-enriched in both folio-opener AND continuation lines. These onset classes mark the beginning of almost any line.

**k**: "folio-level formula class" — LF-enriched in folio-opener lines but position-general (flat) in continuation lines. k appears at folio-first positions in the same way as p/t, but within the body of folios it disperses across all line positions.

In B continuation lines, k is MID-dominant (54% of k tokens), consistent with F364's finding that k is ch-biased at MID/pre_LL in B. In A continuation lines, k disperses more evenly (pos1=20%, MID=38%, pre_LL=14%, LL=14%).

The k anomaly (F392: k=0.80×/0.65× at LF in continuation lines) is now explained: k does not function as a "line-opening" formula in continuation lines because it is not a line-formula class — it is a folio-formula class. The folio-first line uses k as a gallows opener, but subsequent lines do not preferentially start with k.

---

## Self-Audit

**Target-awareness**: No target-aware elements. Corpus analysis only.

**Feature-destroying implementation**: No feature-destroying elements.

**Extrapolation**: All E values are within the tested data. The claim that k is "position-general" in continuation lines is supported by E values spanning 0.79–1.22× in A and 0.66–1.11× in B — all within ±35% of baseline, with no single dominant position. The claim that p/t are "line-level formula classes" is supported by continuation-line LF E ≥ 2.48× in both dialects. The k vs p/t distinction is robust to sample size: k continuation N=314 (A) / N=408 (B) — both adequate.

**Negative-result scope**: N/A — descriptive characterization.

**Control behavior**: No external control. Baseline is positional distribution of all words in continuation/opener lines (denominator for E calculation). Expected k E at LF in continuation lines to be ≤1.0× based on F392 (A=0.80×/B=0.65×); confirmed (A=0.79×/B=0.66×). Expected k E at LF in opener lines to be elevated based on F345 (67-70% gallows at folio-first); confirmed (A=4.32×/B=3.88×). No surprises.

## Finding: F397

**See findings.md F397**
