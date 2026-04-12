# exp_387: A-Dialect r-Onset Positional Census (H601)

**Date:** 2026-04-11
**Hypothesis tested:** H601 — Is A-dialect r approximately LL-exclusive?
**Outcome:** PARTIAL FALSIFICATION — A r is LL-enriched (2.95×) and pos1-absent (0.00×) but NOT LL-exclusive; A r appears at MID_inner at BASELINE rates (1.09×)

---

## 1. A Dialect r Positional Distribution (Continuation Lines, N=21 r tokens)

| Position  | r count | pos total | r rate | E vs baseline |
|-----------|---------|-----------|--------|---------------|
| LF        | 1       | 1507      | 0.066% | 0.27×         |
| pos1      | 0       | 1478      | 0.000% | 0.00×         |
| MID_inner | 8       | 2993      | 0.267% | **1.09×**     |
| pre_LL    | 2       | 1206      | 0.166% | 0.68×         |
| LL        | 10      | 1382      | 0.724% | **2.95×**     |

Overall A r rate in continuation lines: 0.245% (21/8566 words).

---

## 2. Key Finding: A r Is LL-Enriched and MID-Baseline, NOT LL-Exclusive

H601's prediction (A r ≈ LL-exclusive) is REFUTED. The actual profile:
- **LL: 2.95× enriched** (10/21 tokens = 48% at LL)
- **MID_inner: 1.09× = baseline** (8/21 tokens = 38% at MID)
- **pos1: 0.00× = categorical absence** (0/21 tokens — confirms F390)
- **LF: 0.27× depleted** (1/21 tokens)
- **pre_LL: 0.68× mildly depleted** (2/21 tokens)

A r is a bimodal class: strongly enriched at LL and baseline-distributed at MID, while categorically excluded from pos1 and strongly depleted at LF. This parallels B r's positional profile but with A r much smaller and less structured (A=21 tokens vs B=r a major class).

---

## 3. A r Word Inventory (Continuation Lines)

17 word types for 21 tokens (81% hapax — consistent with F382's 88% hapax):
- raiin: 4 tokens (LL×2, MID×1, pre_LL×1) — the only repeated A r word; note raiin is the dominant B r word (18.4%, F382) but only 19% of A r
- ry: 2 tokens (LL×2)
- All others: 1 token each

**LL tokens**: ry(2), raiin(2), rchealcham(1), ram(1), rokyddaly(1), rchody(1), rchy(1), rodaiin(1) — highly heterogeneous, no dominant LL r word

**MID tokens**: rol(1), raiin(1), roiry(1), rcheey(1), rchseesy(1), ror(1), rcheodal(1), ro(1) — all different words, all hapax except raiin

**LF token**: roar(1) — single LF token
**pre_LL tokens**: raiin(1), rar(1)

---

## 4. Extended to All Lines

| Position  | r count | E vs baseline |
|-----------|---------|---------------|
| LF        | 1       | 0.25×         |
| pos1      | 1       | 0.25×         |
| MID_inner | 8       | 1.00×         |
| pre_LL    | 3       | 0.93×         |
| LL        | 10      | 2.68×         |

In ALL lines (including openers/closers): pos1 = 1/1675 (0.25×, not categorical zero). The continuation-line pos1=0 is consistent with strong depletion but the single all-lines pos1 token reduces it from categorical to near-categorical.

---

## 5. Interpretation

A r is not LL-exclusive — it is LL-enriched. The pattern is:
1. A r is excluded from pos1 (categorical in continuation lines)
2. A r is strongly depleted at LF (0.27×)
3. A r appears at MID at baseline rates
4. A r is strongly enriched at LL (2.95×)

This means A r is produced by whatever MID processes generate words there (baseline rate), but is also specifically enriched at LL via the A ch→r pre_LL=6.39× routing rule (F383). The MID r tokens are scattered hapax words; the LL r tokens are also highly heterogeneous (no dominant LL r word despite raiin appearing twice).

Compared to B r (F382): B r shows MID self-succession (1.96×) and more systematic vocabulary (raiin=18.4%). A r lacks both — A r is grammatically marginal at MID but not absent.

---

## Self-Audit

**Target-awareness**: No target-aware elements. Direct corpus census with no calibrated parameters.

**Feature-destroying implementation**: No feature-destroying elements. Standard continuation-line filter and onset detection used.

**Extrapolation**: All claims within tested data. "Near-categorical" accurately characterizes pos1=0 in continuation lines; the full-lines result (1/1675 = 0.25×) confirms strong depletion rather than categorical exclusion.

**Negative-result scope**: H601's LL-exclusive prediction is refuted: A r has 8/21 tokens at MID at baseline rates. Valid conclusion: "A r is LL-enriched and pos1-absent but not LL-exclusive; MID distribution is at baseline."

**Control behavior**: No external control used. Baseline is A-dialect position-averaged r rate (0.245% of 8566 words). E=1.09× at MID_inner confirms baseline behavior.

## Finding: F391

**See findings.md F391**
