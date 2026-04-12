# exp_199: B WP-LF Composition + d+ch Successor + Gallows+ch Folio Distribution
**Date**: 2026-04-11
**Method**: ZL3b paragraph-aware parser; A=163 paragraphs, B=101 paragraphs.

---

## 1. H359: B Within-Para LF Composition — What Fills Where k-Onset Is Absent?

**B vs A enrichment at within-para LF position:**
| Onset | B WP-LF% | A WP-LF% | B/A ratio |
|-------|---------|---------|---------|
| p | 9.61% | 2.32% | **4.14×** |
| l | 2.86% | 0.58% | **4.92×** |
| s | 11.60% | 6.78% | **1.71×** |
| qok | 10.30% | 6.20% | **1.66×** |
| ol | 3.25% | 1.68% | **1.93×** |
| t | 8.70% | 6.78% | 1.28× |
| k | 1.30% | 2.84% | **0.46×** |
| o | 2.94% | 7.36% | **0.40×** |
| ch | 3.90% | 8.13% | **0.48×** |
| qot | 1.99% | 4.84% | **0.41×** |
| d | 15.37% | 17.56% | 0.88× |

**B WP-LF absolute rates (n=2,310):** d=15.4%, s=11.6%, y=11.7%, qok=10.3%, p=9.6%, t=8.7%, sh=5.6%

**H359 SUPPORTED**: The k-onset gap at B WP-LF is filled by p-onset (B=9.61% vs A=2.32%, 4.14×) and l-onset (B=2.86% vs A=0.58%, 4.92×). B WP-LF is also enriched for s (1.71×) and qok (1.66×). The dramatic enrichment of p-onset at B WP-LF (from 2.32% in A to 9.61% in B) explains why k has a paradoxically high PS enrichment in B (9.91×) despite similar absolute PS rates: in B, p-onset floods into WP-LF positions (9.6%), competing with k there (reducing k's WP-LF rate to 1.30%), so k remains confined to PS. In A, p-onset stays at WP-LF = 2.32%, but k appears more often at WP-LF (2.84%). The B grammar has a stronger PARA-tier concentration at PS because p and k BOTH avoid within-para LF positions (p at WP-LF is still only 9.6% vs 36% at PS; k at WP-LF is only 1.3% vs 13% at PS).

---

## 2. H360: d+ch → sh Successor — Which sh-Words?

**After d+ch lines (A-dialect), next-line first word = sh-onset in 12/94 cases (12.8% = 1.77×).**

**sh-onset words following d+ch lines:**
| Word | After d+ch | Rate | Baseline | Baseline% | Enrichment |
|------|-----------|------|----------|-----------|-----------|
| shol | 4 | 33.3% | 14 | 12.5% | **2.7×** |
| sho | 2 | 16.7% | 30 | 26.8% | 0.6× |
| shok | 1 | 8.3% | 1 | 0.9% | 9.3× |
| shochy | 1 | 8.3% | 1 | 0.9% | 9.3× |
| (others) | 4 | 33.3% | — | — | variable |

**Top specific next words after d+ch lines (n=94):**
shol(4.7×), qotcho(9.9×), ytchy(9.9×), sol(8.2×), qor(11.0×), chol(3.1×), otchol(3.7×)

**H360 PARTIALLY SUPPORTED**: The d+ch → sh enrichment (1.77×) is driven primarily by `shol` (33.3% of sh-followers, 2.7× enriched). However, the sample is small (n=12 sh-onset followers) and diverse — 8 distinct sh-words appear, with only shol appearing more than once. The d+ch successor pattern overall is distributed: no single word dominates (max 4 instances each for shol, chol, qotcho, ytchy, sol). The sh enrichment after d+ch is real but not driven by a single formulaic word — it reflects a structural preference for shol (a common sh-word) as the opener of lines following d+ch lines.

---

## 3. H361: Gallows+ch Para-Starter Distribution — Cannot Test by Folio

**Key finding**: Herbal A has 87 paragraphs, with exactly 1 paragraph per folio. This means the gallows+ch distribution at PS (overall: p+ch=12.6%, t+ch=8.0%, k+ch=5.7%, f+ch=4.6%) is spread across 87 individual folios, with no folio having more than 1 PS word. Folio-level variation in gallows+ch hierarchy is untestable with n=1 per folio.

**H361 NOT TESTABLE with current paragraph structure**: Herbal A's 1-paragraph-per-folio structure prevents within-folio variation analysis. The overall gallows+ch rates (p+ch=12.6% > t+ch=8.0% > k+ch=5.7% > f+ch=4.6%) are consistent with F196/F198 but cannot be tested for folio clustering. A different framing would be required (e.g., do early quire folios use p+ch more often than late quire folios?), but with n=1 data point per folio, this test has zero power.

---

## Self-Audit

**Target-awareness**: No target-aware elements. All metrics are corpus-internal positional rates.

**Feature-destroying implementation**: H360 d+ch detection uses `w.startswith('d') and len(w)>=3 and w[1:3] in ('ch','sh')`. This is correct. The "next word" is the first word of the next line in the same paragraph — correctly defined. The sample is small (n=12 sh-followers of n=94 d+ch next-line words).

**Extrapolation**: H359: The "p-onset floods into WP-LF in B" interpretation is supported by the 4.14× enrichment. This is a descriptive finding, not extrapolated. H360: Small n (n=12 sh-followers) means all specific-word enrichments are directional only.

**Negative-result scope**: H361 not testable (1-per-folio structure). This does not mean the hierarchy is uniform across folios — it means we cannot test folio variation with 1 PS word per folio.

**Control behavior**: No external controls. All comparisons are corpus-internal (B vs A WP-LF, d+ch vs baseline).

---

## CONCLUSION

| H | Result | Key Finding |
|---|--------|-------------|
| H359 | SUPPORTED | B WP-LF: p(4.14×) and l(4.92×) enriched vs A; k(0.46×) depleted; p-onset at B WP-LF=9.61% (vs A=2.32%) fills where k is absent — explains B's high k PS-enrichment (9.91×) |
| H360 | PARTIALLY SUPPORTED | d+ch→sh: primarily shol (33.3%, 2.7×); diverse sh-words follow d+ch (8 distinct types); no single formulaic sh-word dominates |
| H361 | NOT TESTABLE | 1-paragraph-per-folio structure in herbal A prevents folio-level variation analysis |
