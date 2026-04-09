# Experiment exp_061: Paragraph Structure by Section + k vs t Onset Classes
Date: 2026-04-09

## H071: Paragraph Structure by Section

### Results: Content Sections Are Single-Paragraph; Technical Sections Are Multi-Paragraph

| Section | Folios | Avg PS/folio | Single-para% | Multi-para% | Max PS |
|---------|--------|-------------|-------------|-----------|--------|
| Herbal (H) | 128 | 0.98 | **100%** | 0% | 1 |
| Special (S) | 25 | 1.00 | **100%** | 0% | 1 |
| Text (T) | 6 | 1.00 | **100%** | 0% | 1 |
| Bio (B) | 19 | 1.63 | 63.2% | **36.8%** | 4 |
| Pharma (P) | 16 | 2.25 | 25.0% | **75.0%** | 4 |
| Astro (A) | 4 | 4.25 | 50.0% | **50.0%** | 13 |
| Cosmo (C) | 7 | 3.00 | 28.6% | **71.4%** | 5 |

**Pattern: Content sections (Herbal, Special, Text) are uniformly single-paragraph. Technical sections (Pharma, Astro, Cosmo, Bio) have multi-paragraph folios.**

### Multi-Paragraph Folios by Section

**Bio (7 multi-para folios)**: f83r (4 PS, 51 lines), f84v (4 PS, 51 lines), f75v (3 PS, 37 lines), f75r, f82r, f83v, f84r. These are predominantly the **bathing pool folios** (f75v, f82r, f83r, f83v, f84r, f84v — the pool section). Pool folios have multiple illustrated scenes per page, each with its own text block.

**Pharma (12 multi-para folios)**: f99r (4 PS), f99v (4 PS), f88r (3 PS), etc. Consistent with recipe-book structure where multiple items appear per page.

**Astro**: f67r2 has **13 para-starts** in 35 lines — this is an astronomical folio with many labeled sections/items.

**Cosmo**: f86v3 (5 PS), f85r2 (4 PS), fRos (4 PS) — cosmological folios have complex multi-section layout.

### H071 Verdict: SUPPORTED

Single-paragraph structure is not herbal-specific — it's a property of **content sections** (Herbal=100%, Special=100%, Text=100%). Technical/reference sections (Pharma=75% multi-para, Cosmo=71%, Astro=50%) have multi-paragraph folios reflecting multiple items per page. Bio's 37% multi-paragraph rate corresponds to the bathing pool sub-section (multiple scenes per folio), while single-figure bio folios are single-paragraph. The paragraph count is a direct structural indicator of page content complexity.

## H070: k vs t Onset Classes (Currier B)

### KL Divergence Between Onset Classes

| Onset pair | KL bits | Interpretation |
|-----------|---------|---------------|
| sh vs ch | **0.062** | Nearly identical — same class |
| **k vs t** | **0.082** | Nearly identical — same class |
| p vs t | 0.111 | Similar |
| k vs qo | 0.157 | Different |
| t vs qo | 0.193 | Different |
| k vs sh | 0.329 | Very different |
| s vs t | 0.247 | Different |
| s vs k | 0.339 | Very different |
| k vs d | 0.345 | Very different |
| t vs sh | 0.312 | Different |

**k and t have nearly identical suffix distributions (KL=0.082 bits)** — they are the same onset class. Similarly, sh and ch form one class (KL=0.062 bits).

### Suffix Distribution: k vs t vs Other Classes

The near-identical suffix profiles of k and t:
- -dy: k=13.9%, t=8.5% (small difference)
- -edy: k=11.0%, t=14.7%
- -ar: k=11.0%, t=11.0% (identical)
- -aiin: k=8.0%, t=9.9%

The `s` class is distinctively aiin-dominant (s: -aiin=20.6%, -ain=11.6%) — closer to d (d: -aiin=20.8%) than to k/t.

### Onset Class Hierarchy in Currier B

Based on KL analysis, Currier B has **3-4 onset classes**, not the 8 originally tested:
1. **{ch, sh}**: KL=0.062 — one class (ch/sh-initial stem class)
2. **{k, t, p}**: KL 0.082-0.111 — one class (k/t-initial stem class, extends to p)
3. **{d, s}**: both aiin-dominant — one class (d/s-stem class; aiin-selecting)
4. **{qo}**: distinctive extended-form preference (-eedy/-eey/-ain; KL 0.157-0.193 from k/t)

`o` was not disaggregated in this analysis but was the largest single class (23.2% of B tokens).

### H070 Verdict: SUPPORTED

k-initial and t-initial words have nearly identical suffix distributions (KL=0.082 bits) in Currier B — they are the same morphological onset class. sh and ch are also nearly identical (KL=0.062 bits). The 8-class onset taxonomy from exp_056 can be reduced to ~4 classes in B: {ch/sh}, {k/t/p}, {d/s}, {qo}. This is consistent with the qo-stripping finding (exp_040) that qo-stems are k/t-initial — the qo- prefix selects the k/t class (the same class identified here as highly coherent). The `s` class is unexpectedly aiin-dominant (similar to d), suggesting a different morphological role for s-initial words.

## Combined Finding (F068)

**H071 SUPPORTED**: Single-paragraph structure is a cross-section property of content-organized folios (Herbal=100%, Special=100%, Text=100%) — not herbal-specific. Multi-paragraph structure characterizes technical/reference sections (Pharma=75%, Cosmo=71%, Astro=50%, Bio=37%). In Bio, multi-paragraph folios are specifically the bathing pool sub-section (f75v, f82r, f83r, f83v, f84r, f84v), where multiple scenes per folio require multiple text blocks.

**H070 SUPPORTED**: k-initial and t-initial words in Currier B are the same onset class (KL=0.082 bits from each other). sh and ch are also one class (KL=0.062 bits). Currier B's effective onset class structure is ~4 classes: {ch/sh} (high -y/-ey/-edy), {k/t/p} (balanced, moderate -dy), {d/s} (aiin-dominant), {qo} (extended-form dominant: -eedy/-eey/-ain). This reduces the complexity of the word template (exp_056): the 8-onset cross-tabulation can be collapsed to 4 onset classes without significant information loss. The qo- prefix selects the {k/t} class — consistent across multiple experiments.
