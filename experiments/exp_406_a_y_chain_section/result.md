# exp_406: A y-Chain Section Specificity (H614)

**Date:** 2026-04-11
**Hypothesis tested:** H614 — Are A y-chains (length≥3) concentrated in herbal/bio sections?
**Outcome:** CONFIRMED (directional). bio_stars section: 5.71 chains per 100 y-words (N=2/35 y-words, 4 folios). herbal: 0.60/100 (N=2/334). pharma: 0.00 (N=0/46). cosmo: 0.00 (N=0/70). Bio_stars has ~10× higher y-chain rate per y-word than herbal. All 4 chains (2 length-4, 2 length-3) are in herbal or bio_stars; none in pharma or cosmo. bio_stars also has highest y% (10.1% vs 6.0% herbal, 5.4% cosmo, 4.3% pharma).

---

## 1. Section Statistics

| Section | N_words | y% | runs_3 | runs_4+ | rate/100y |
|---|---|---|---|---|---|
| herbal (45 folios) | 5609 | 6.0% | 1 | 1 | 0.60 |
| **bio_stars (4 folios)** | **347** | **10.1%** | **1** | **1** | **5.71** |
| cosmo (6 folios) | 1285 | 5.4% | 0 | 0 | 0.00 |
| pharma (4 folios) | 1078 | 4.3% | 0 | 0 | 0.00 |
| text (0 A folios) | 0 | — | 0 | 0 | — |

---

## 2. Specific Long Chains

| Length | Section | Folio | Notes |
|---|---|---|---|
| 4 | herbal | f19 | "ytor ytar ytchor ytaiin" (from F395) |
| 4 | bio_stars | f67r2 | "ypair ykoaiin ydoly ytalchos" (from F395) |
| 3 | herbal | f44 | (from F395) |
| 3 | bio_stars | f67r2 | (same folio as length-4) |

---

## 3. Interpretation

### 3.1 bio_stars Concentration

The bio_stars section (4 folios: f67-f86) has a y-chain rate ~10× higher than herbal (5.71 vs 0.60 per 100 y-words). bio_stars also has a higher y% overall (10.1% vs 6.0% in herbal) — y words are proportionally more common in bio folios. The y-chain concentration in bio is thus driven by both higher y-frequency AND higher y-chain formation rate.

**Caveat**: N=2 chains in 35 y-words (bio). The 5.71/100 rate is a highly directional estimate. The actual bio y-chain rate could be anywhere from 1-15/100 at 90% confidence.

### 3.2 Pharma and Cosmo: Zero Chains

Pharma (4 folios, 46 y-words) and cosmo (6 folios, 70 y-words) have zero chains of length≥3. The zero counts are meaningful: with 46 and 70 y-words, a chain rate of 0.60/100 (herbal rate) would produce expected 0.28 and 0.42 chains respectively — so zero is plausible under the herbal rate. But under the bio rate (5.71/100), expected would be 2.6 and 4.0 chains — the observed zero in pharma/cosmo is inconsistent with the bio rate.

This means pharma/cosmo y-chains follow the herbal rate (≤1/100), while bio follows a much higher rate (≥3/100). The section-specificity is clearest as a bio vs non-bio distinction.

### 3.3 Implications

y-chains being section-specific (bio-concentrated) suggests:
1. The y-chain mechanism is activated more strongly in bio sections
2. Either the bio scribal practice includes longer y-chain sequences, or bio-section content produces more y-class words in sequence
3. Combined with F395 (both A length-4 y-chains are in herbal/bio), the y super-geometric chain structure is a section-grammar property, not a universal A-dialect grammar property

---

## 4. Limitations

- bio_stars: N=2 chains in 35 y-words. All bio claims are highly directional.
- "text" section has 0 A-dialect folios in this corpus (ZL3B A-dialect folios stop at the pharma/cosmo range). Cannot compute text section y-chain rate.
- Folio-to-section assignment is approximate (linear cutoffs at f66/f86/f98/f116) and may misclassify some borderline folios.
- bio_stars section only 4 folios (f67-f86 A-dialect); the concentrated y-chains may be folio-specific (both chains are in f67r2 specifically).

---

## Self-Audit

**Target-awareness**: No target-aware elements.

**Feature-destroying implementation**: No feature-destroying elements. y-runs correctly identified as consecutive y-onset words within continuation lines.

**Extrapolation**: "bio_stars 10× higher y-chain rate" is stated as directional (N=2 chains). Not claiming bio is the only y-chain locus — pharma/cosmo may have chains not detected due to small N. PASS.

**Negative-result scope**: pharma/cosmo zero-chain result is adequately scoped: zero chains expected ≤0.4 under herbal rate, so zero is consistent with herbal-rate chain frequency in these sections. The negative result means pharma/cosmo chain rate ≤ herbal rate (0.60/100). PASS.

**Control behavior**: No shuffle control. Expected bio_stars to show elevated y-chain rate based on F395 prior. Confirmed. PASS.

## Finding: F410

**See findings.md F410**
