# Experiment exp_047: Quire Structure vs Section as Morphological Grouping Variable
Date: 2026-04-09

## Question (H051)
Does quire grouping explain morphological variation better than section grouping? Are folios in the same quire more morphologically similar than folios in the same section?

## Results

### Variance Decomposition: F-ratios (Between/Within)

| Feature | Quire F | Section F | Winner |
|---------|---------|-----------|--------|
| qo-rate | 0.99 | **1.35** | Section |
| -edy rate | 1.34 | **2.07** | Section |
| -ol rate | 0.67 | **0.86** | Section |
| -aiin rate | 0.32 | **0.40** | Section |

**Section explains more morphological variance than quire for all four features.**

### Quire-Level Summary (Notable Outliers)

| Quire | Folios | Tokens | qo% | -edy% | -ol% | -aiin% |
|-------|--------|--------|-----|-------|------|--------|
| M | 20 | 6241 | **25.8%** | **20.5%** | 7.2% | 5.9% |
| T | 23 | 9991 | 18.0% | 9.9% | 4.6% | 11.5% |
| N | 6 | 1574 | 14.7% | 8.5% | 3.8% | 12.9% |
| A | 16 | 1294 | 7.7% | 0.0% | 13.2% | 13.6% |
| J | 2 | 125 | 5.3% | 0.0% | 7.3% | 11.9% |
| I | 7 | 346 | 5.9% | 0.6% | 8.8% | 6.0% |

Quire M stands out dramatically: qo=25.8%, -edy=20.5% — these are extreme B-type markers. Quire M corresponds to the bio section (folio 75r–84v, known bio folios). Quire A, J, I cluster with low qo/edy, high -ol — A-type markers.

### Within-Quire Variation

Quire-level standard deviations for qo-rate are substantial (std=0.04–0.06), meaning individual folios within a single quire can vary ±5-6% around the quire mean. This is driven by mixed-section quires: some quires span multiple sections with different Currier dialects.

### Section-Level Summary

| Section | Folios | Tokens | qo% | -edy% | -ol% | -aiin% |
|---------|--------|--------|-----|-------|------|--------|
| B (bio) | 19 | 5727 | 26.1% | 20.6% | 7.4% | 5.9% |
| S (text) | 25 | 10676 | 17.8% | 9.2% | 4.7% | 11.2% |
| T (text/special) | 6 | 2109 | 13.2% | 9.1% | 5.5% | 10.9% |
| P (pharma) | 16 | 2110 | 13.8% | 0.3% | 18.5% | 10.0% |
| H (herbal) | 128 | 9881 | 10.7% | 3.0% | 10.4% | 12.4% |
| C (cosmo) | 7 | 647 | 8.9% | 4.7% | 8.2% | 10.5% |
| A (astro) | 5 | 262 | 7.1% | 0.0% | 6.2% | 5.7% |

Pharma stands out: -ol=18.5% (highest of any section), -edy=0.3% (near-zero despite having tokens). This is a P-section specific signature. Bio continues to show the extreme B-type profile.

## Finding (F054)
Section grouping explains morphological variance better than quire grouping for all four morphological features tested (qo-rate, -edy, -ol, -aiin). Section F-ratios range from 1.25–1.54× quire F-ratios. The strongest case is -edy (Section F=2.07 vs Quire F=1.34). Quire M is a statistical outlier — it maps almost entirely to the bio section — so the apparent "quire" signal is actually a section signal. Within-quire variance (std≈0.05) is high, confirming that quires are heterogeneous. The pharma section shows a distinctive -ol=18.5% signature not seen in other sections.

## H051 Verdict: NOT SUPPORTED
Quire structure does not explain morphological variation better than section assignment. Section is the primary organizing variable for morphological features in the manuscript. The codicological unit (quire) does not predict morphological behavior independently of the section/content type. This is consistent with the scribe producing morphologically consistent text within content sections across quire boundaries, rather than quire-level scribal behavior.
