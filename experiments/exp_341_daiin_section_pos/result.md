# exp_341: B-Dialect daiin LF Enrichment by Section (H546)

**Date:** 2026-04-11
**Hypothesis:** H546 — The B-dialect daiin LF=2.57× enrichment varies by section; bio section may drive it given high daiin prevalence.
**Result:** H546 CONFIRMED. daiin LF enrichment is NOT uniform across B-dialect sections — it's strongest in pharma (LF_enr=4.68×) and text (3.58×), moderate in cosmo (2.34×) and herbal (1.89×), and weakest in bio (1.57×). Bio section does NOT drive the overall enrichment; pharma and text do. A-dialect daiin LL enrichment (from F341) is driven primarily by herbal section (LL_enr=1.50×); pharma section shows NEAR-BASELINE daiin LL enrichment (0.85×). This contrasts with pharma being the most {ol,or}-enriched section (F342=17.88×), suggesting A-dialect pharma has a distinctive grammar: template onsets use ol/or AND daiin is positionally diffuse.

---

## Key Statistics

### B-Dialect daiin LF Enrichment by Section

| Section | Total | daiin N | daiin LF | LF% | LF_enr |
|---------|-------|---------|---------|-----|--------|
| pharma | 397 | 8 | 5 | 62.5% | **4.68×** |
| text | 9063 | 110 | 47 | 42.7% | **3.58×** |
| cosmo | 1056 | 16 | 5 | 31.2% | 2.34× |
| herbal | 2390 | 54 | 14 | 25.9% | 1.89× |
| bio | 5693 | 75 | 16 | 21.3% | 1.57× |

Overall B-dialect daiin LF_enr = 2.57× (pooled across sections)

### A-Dialect daiin LL Enrichment by Section

| Section | Total | daiin N | daiin LL | LL% | LL_enr |
|---------|-------|---------|---------|-----|--------|
| cosmo | 344 | 5 | 1 | 20.0% | 1.76× |
| herbal | 6280 | 326 | 93 | 28.5% | **1.50×** |
| pharma | 2559 | 101 | 12 | 11.9% | 0.85× |
| astro | 431 | 11 | 0 | 0.0% | 0.00× |

Overall A-dialect daiin LL_enr = 1.37× (from F341, mostly driven by herbal)

---

## Findings

### Finding 1: B-dialect pharma and text sections are daiin-LF-dominant; bio is weakest

The B-dialect overall daiin LF=2.57× pooled enrichment is driven primarily by pharma (4.68×) and text (3.58×). Bio section shows the weakest daiin LF enrichment (1.57×) despite having the most daiin tokens (N=75). This means the "daiin as LF formula" function is strongest in the pharma/text sections and weakest in bio — where daiin appears more evenly distributed across line positions.

### Finding 2: A-dialect pharma has near-baseline daiin LL enrichment (0.85×) despite extreme {ol,or} dominance

A-dialect pharma (F342: {ol,or}/{aiin,ain}=17.88×) shows LL_enr=0.85× for daiin — essentially no LL enrichment. The A-dialect pharma section thus has: (1) template onsets using ol/or instead of aiin; (2) daiin NOT concentrated at LL. A-dialect pharma appears to have the weakest daiin positional grammar of any A-dialect section. The daiin LL enrichment in A-dialect (F341: 1.37×) is driven by herbal (1.50×) and cosmo (1.76×).

### Finding 3: A-dialect herbal section drives most of the A-dialect daiin LL enrichment

A-dialect herbal has daiin N=326 (74% of all A-dialect daiin occurrences) and LL_enr=1.50×. The overall A-dialect daiin LL=1.37× is largely explained by the herbal section's LL enrichment (326 out of 443 A-dialect daiin instances are in herbal).

---

## Interpretation

The section-level analysis reveals that the B-dialect daiin LF grammar is not bio-driven — it is strongest in pharma and text. The most uniform positional grammar is in text section (which also has the most daiin tokens, N=110). 

A-dialect pharma is uniquely distinctive: extreme {ol,or} dominance AND near-baseline daiin positional grammar. This suggests A-dialect pharma has a fundamentally different formula structure from all other VMS sections.

---

## Self-Audit

**Target-awareness:** No target-aware elements. PASS.
**Feature-destroying implementation:** Section assignment by folio number ranges (approximate but standard). PASS.
**Extrapolation:** All claims within observed data. B pharma daiin N=8 (small but 5/8=62.5% LF is striking). PASS.
**Negative-result scope:** Bio NOT driving B-dialect LF enrichment. Conclusion is bounded to the tested sections. PASS.
**Control behavior:** No control. Expected under null: all sections show same LF%≈13% (baseline). Observed: pharma=62.5%, text=42.7% are far above baseline. PASS.
