# exp_390: B r at pos1 — Word-Level Analysis (H602)

**Date:** 2026-04-11
**Hypothesis tested:** H602 — what r words appear at pos1 in B, and which LF classes produce them?
**Outcome:** ANSWERED — raiin dominates B pos1 r (40%); qok(3.19×)/qot(3.22×)/y(2.32×) produce r at pos1; B pos1 r and B LL r have DIFFERENT vocabulary profiles

---

## 1. Corpus Statistics

- B continuation lines: 2271
- B lines with r at pos1: **15** (0.66% = baseline r@pos1 rate)

---

## 2. LF Onset Classes Producing B r at pos1

| LF onset | r@pos1 N | LF total N | rate  | E       |
|----------|----------|------------|-------|---------|
| qok      | 5        | 237        | 2.1%  | **3.19×** |
| qot      | 1        | 47         | 2.1%  | **3.22×** |
| y        | 4        | 261        | 1.5%  | **2.32×** |
| ol       | 1        | 70         | 1.4%  | **2.16×** (new) |
| t        | 1        | 205        | 0.5%  | 0.74×   |
| p        | 1        | 222        | 0.5%  | 0.68×   |
| s        | 1        | 260        | 0.4%  | 0.58×   |
| d        | 1        | 344        | 0.3%  | 0.44×   |
| sh       | 0        | 126        | 0.0%  | 0.00×   |
| ch       | 0        | 88         | 0.0%  | 0.00×   |
| ok       | 0        | 76         | 0.0%  | 0.00×   |
| ot       | 0        | 50         | 0.0%  | 0.00×   |
| k        | 0        | 34         | 0.0%  | 0.00×   |

Key: qok(E=3.19×) and qot(E=3.22×) are the primary r-pos1 producers (confirmed from F390). y(E=2.32×) is the third. ch/sh/ok/ot/k all produce 0 r at pos1. New finding: ol(E=2.16×/N=1, directional) also slightly elevated.

---

## 3. B r Word Inventory at pos1 (N=15)

- **raiin**: 6/15 = **40%** — overwhelmingly dominant
- rshey: 1 (6.7%)
- rol: 1 (6.7%)
- rshedy: 1 (6.7%)
- rchey: 1 (6.7%)
- rsheal: 1 (6.7%)
- rchs: 1 (6.7%)
- ror: 1 (6.7%)
- rcheey: 1 (6.7%)
- rain: 1 (6.7%)

raiin is the dominant B r word (F382: 18.4% of all B r tokens). At pos1 specifically, raiin = 40% of r appearances (vs 18.4% overall). **r at pos1 is biased toward raiin** relative to the general B r vocabulary.

---

## 4. B r Vocabulary: pos1 vs LL Comparison

| Word   | pos1 N | LL N | Total |
|--------|--------|------|-------|
| raiin  | 6      | 6    | 12    |
| ram    | 0      | 10   | 10    |
| ry     | 0      | 6    | 6     |
| ror    | 1      | 5    | 6     |
| rol    | 1      | 5    | 6     |
| ral    | 0      | 5    | 5     |
| rain   | 1      | 4    | 5     |
| ro     | 0      | 4    | 4     |
| rar    | 0      | 3    | 3     |
| raram  | 0      | 3    | 3     |

**B pos1 r and B LL r use different vocabulary profiles.** LL is dominated by ram(10)/ry(6)/raiin(6)/ror(5)/rol(5)/ral(5) — more diverse, with ram as the single most common LL r word. pos1 r is dominated by raiin(6/15=40%), with most LL-dominant words (ram/ry/ral/ro/rar/raram) absent from pos1 entirely.

---

## 5. Representative Lines with r at pos1

Lines where LF ∈ {qok, qot, y} and pos1 = r:

```
[f75/12]  qokedy rshey qol chey ol chey...   (qok → rshey)
[f77/40]  qokeey rol chdor cheey qokaiin...  (qok → rol)
[f79/3]   yshealdy rshedy qoteedy...         (y → rshedy)
[f80/36]  qokeey rchey tain oteey qokain...  (qok → rchey)
[f82/30]  qoteey raiin cheol qoteey...       (qot → raiin)
[f95v1/9] qokeeod raiin qokeey qoko skchdy  (qok → raiin; 5-word line)
[f108/13] ykeey raiin                        (y → raiin; 2-word line!)
[f111/41] ycheey raiin cheody qokechy...    (y → raiin)
[f115/42] yair rcheey lkchdy qokchey...     (y → rcheey)
[f116/36] qokeey rain shey okeey...         (qok → rain)
```

**Pattern**: After (qok/qot/y at LF, r at pos1), the line typically continues with ch/qok/s/sh class words. The r word (usually raiin) does NOT terminate the line — it is a MID word that leads into the rest of the line grammar. One short line: `ykeey raiin` = 2-word line with y at LF, raiin = LL (pos1 = LL in this case).

---

## 6. Key Structural Finding

B r at pos1 is primarily **raiin** (40%), produced by **template classes qok and qot** and **formula class y** at LF. The pattern qok/qot/y → raiin → {ch/qok/sh continuation} is a recognizable B-dialect trigram. This differs from B r at LL (where ram, ry, rol, ral dominate, not raiin).

**raiin is a position-polymorphic word**: it appears as the dominant B r word at pos1 AND as a LL r word (6 LL occurrences) AND in MID positions. raiin does not have a fixed positional assignment unlike some LL-exclusive words.

---

## Self-Audit

**Target-awareness**: No target-aware elements. Direct corpus frequency analysis.

**Feature-destroying implementation**: No feature-destroying elements.

**Extrapolation**: All claims within tested data. N=15 total for pos1 r; most LF onset claims are directional (N=1-5). The qok(N=5) and y(N=4) claims are the most reliable. ol(N=1) is directional only.

**Negative-result scope**: N/A — descriptive analysis.

**Control behavior**: Baseline r@pos1 rate = 0.66%. LF onset classes producing 0 r at pos1 (ch/sh/ok/ot/k) are adequately supported by total LF N (76-237) combined with zero events.

## Finding: F394

**See findings.md F394**
