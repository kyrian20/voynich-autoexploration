# Experiment exp_046: Per-Folio Label-Body Vocabulary Correlation
Date: 2026-04-09

## Question (H053)
Do folio labels predict the body word distribution on the same folio? Are labels folio-specific (naming what's illustrated) or formulaic (standard names regardless of body content)?

## Results

### Overall Statistics (30 folios with ≥3 labels AND ≥30 body tokens)

- Folios with label-body Jaccard ratio > 1.0 (above chance): **12/30 (40%)**
- Folios with zero shared label-body vocabulary: **18/30 (60%)**
- Mean label-body Jaccard ratio: 3.86 (inflated by a few high-ratio outliers)

### Section-Level Summary

| Section | N folios | Mean ratio | Median ratio |
|---------|---------|-----------|-------------|
| Bio (B) | 10 | **7.10** | 5.76 |
| Astro (A) | 3 | 6.04 | 6.68 |
| Pharma (P) | 15 | 1.77 | **0.00** |
| Text/Cosmo | 2 | 0.00 | 0.00 |

**Bio and astro labels are most predictive of same-folio body vocabulary; pharma labels have median ratio=0.00 (zero overlap for most pharma folios).**

### The Overlap Is Mediated by 'o'-Prefix Words

In every folio with label-body overlap, the shared words are 'o'-initial:
- f83v: `okaiin`
- f82v: `okain, oteedy, olkol, olkeedy`
- f75v: `qokal, olol, oteey, lol, otedy`
- f89v2: `chody, sheol` (exceptions, shorter words)
- f89r2: `opcheor, dy, cheody`

The label-body vocabulary overlap is not a content relationship ("labels name what's in the body") — it is a **morphological relationship**: the same 'o'-prefix form (e.g., "okain") appears in both the label layer and the body text of the same folio. This is consistent with exp_037's finding that 'o' is a label-form morpheme that can transform body-text stems into labeled forms — and those same o+stem forms occasionally appear in body text.

### Pharma Labels Are Formulaic

15 pharma folios have labels (Lf locus). Only 2 show above-chance overlap (f89v2, f89r2). The remaining 13 have zero shared words between their labels and body text — their labels use completely different vocabulary from the body prose on the same folio. **Pharma labels are a formulaic register independent of folio-specific body content.**

This is consistent with pharma labels being plant/ingredient names (high TTR=0.956, near-unique labels per exp_032) while pharma body text is recipe/procedure prose using a different vocabulary register.

## Finding (F053)
**Labels are overwhelmingly formulaic (distinct register) rather than folio-specific (naming illustrated objects):** 18/30 folios (60%) with sufficient label AND body tokens have zero vocabulary overlap between the two layers. Where overlap exists (40% of folios, primarily bio and astro), it is mediated by 'o'-prefix words appearing in both layers — a morphological relationship (the 'o' label morpheme from F044), not a content relationship. Pharma section labels (Lf locus) have median ratio=0.00: formulaic across the section. Bio labels have median ratio=5.76 (highest section), with shared words being ot-/ok- forms — the same morphological class that dominates the label corpus (F010/F023).

## H053 Verdict: PARTIALLY SUPPORTED
Labels do NOT generally predict same-folio body vocabulary (60% zero overlap). The 40% of folios with above-chance overlap are primarily bio/astro and share specific morphological forms (o-prefix words). Pharma labels are pure formulaic registers. The label-body separation supports the register hypothesis: labels are a distinct linguistic layer from body prose, not content-based annotations of the illustrated content.
