# exp_428: Section Distribution of 10 Confirmed B Formula Types

**Hypothesis (H650):** Are any of the 10 confirmed B formula types section-concentrated, like y→o→ch (pharma+bio, F425)?

**Method:** B continuation lines with section classification by folio number (herbal ≤72, astro 73-84, bio 85-102, pharma 103-116). 'Other' onset filtering (consistent with exp_424). For each formula type, count occurrences per section and compute E = (observed fraction) / (baseline fraction). Baseline: B continuation line distribution by section.

---

## Results

### Baseline B continuation line section distribution

| Section | N cont lines | Fraction |
|---------|-------------|----------|
| herbal (≤72) | 277 | 12.1% |
| astro (73-84) | 750 | 32.7% |
| bio (85-102) | 219 | 9.6% |
| pharma (103-116) | 1038 | 45.3% |
| other | 9 | 0.4% |
| **Total** | **2293** | |

### Formula type section enrichment (E = obs/baseline fraction)

| Formula type | N | herbal | astro | bio | pharma | Max section |
|-------------|---|--------|-------|-----|--------|------------|
| qok→sh→k | 5 | 1.7× | **2.4×** | 0.0× | 0.0× | astro(2.4×) |
| d→ot→ot | 5 | 0.0× | 0.6× | 0.0× | **1.8×** | pharma(1.8×) |
| l→ch→qok | 4* | **2.1×** | 0.0× | 0.0× | 1.7× | herbal(2.1×) |
| d→qok→ol | 6 | 0.0× | **2.5×** | 0.0× | 0.4× | astro(2.5×) |
| y→sh→ch | 8 | **3.1×** | 0.0× | 1.3× | 1.1× | herbal(3.1×) |
| y→o→ch | 4* | 0.0× | 0.0× | **2.6×** | 1.7× | bio(2.6×) |
| qok→ch→qo | 7 | 0.0× | **1.7×** | 0.0× | 0.9× | astro(1.7×) |
| d→ch→y | 5 | **5.0×** | 0.0× | 0.0× | 0.9× | herbal(5.0×) |
| qok→ch→ol | 5 | 0.0× | **2.4×** | 0.0× | 0.4× | astro(2.4×) |
| p→sh→ok | 6 | **2.8×** | 1.0× | 0.0× | 0.7× | herbal(2.8×) |

*N discrepancy from exp_424 (N=5 for l→ch→qok, N=6 for y→o→ch) due to minor corpus boundary differences in locus filtering.

---

## Interpretation

**H650 CONFIRMED (directional).** All 10 formula types show section skew; none is uniformly distributed. Three section-specific clusters emerge:

### Cluster 1: Astro-section formula types (qok-LF class)
**qok→sh→k (E=2.4×), d→qok→ol (E=2.5×), qok→ch→qo (E=1.7×), qok→ch→ol (E=2.4×)** — all concentrated in the astro section (folios 73-84, including zodiac and astrological charts). The qok-LF formula types and the d→qok routing formula are astro-grammar features. d→ot→ot is the exception (pharma-concentrated, E=1.8×). The astro section may have a qok-template dominant grammar that drives these formula types.

### Cluster 2: Herbal-section formula types
**d→ch→y (E=5.0×!), y→sh→ch (E=3.1×), p→sh→ok (E=2.8×)** — all concentrated in the herbal section (folios ≤72) despite herbal being only 12.1% of B continuation lines. The herbal section has a grammar characterized by: d-LF routing to ch→y, y-LF routing via sh to ch, and p-LF routing to sh→ok. These are the three "content routing" formula types (ch/y/ok at pos2), distinct from the astro template-class formula types (qok/qo/ol at pos2).

### Cluster 3: Pharma+bio section formula types
**y→o→ch (herbal=0, bio=2.6×, pharma=1.7×)** — consistent with F425. l→ch→qok also pharma-present (3/4 in pharma) consistent with F423.

### Cross-cluster pattern
The three LF classes' formula types cluster by section:
- **y-LF**: herbal path (y→sh→ch) vs pharma+bio path (y→o→ch) — cross-section inversion within same LF class
- **d-LF**: astro path (d→qok→ol, E=2.5×) vs herbal path (d→ch→y, E=5.0×) — d-formula splits by section
- **qok-LF**: astro-concentrated (all 3 qok formula types in astro)
- **p-LF**: herbal-concentrated (p→sh→ok, E=2.8×)

This suggests VMS B section-grammar: the same formula LF class uses different routing depending on section, producing section-specific formula types.

---

## Limitations

- ALL counts are N=4-8 per formula type — directional only, not statistically robust.
- Section boundaries (folio-number-based) are approximate.
- N discrepancies from exp_424 (l→ch→qok N=4 vs 5, y→o→ch N=4 vs 6) due to minor corpus differences.
- d→ch→y E=5.0× in herbal (3/5 lines) is striking but N=5.

---

## Self-Audit

**Target-awareness**: No target-aware elements.

**Feature-destroying implementation**: No feature-destroying elements. Section classification by folio number is an external metadata assignment, not dependent on the text features under test.

**Extrapolation**: All claims qualified as "directional" given N=4-8 per formula type. No claims about what "must" happen in specific sections.

**Negative-result scope**: N/A — positive result.

**Control behavior**: No explicit control. Section baselines computed from the full B continuation line corpus. Expected: y→o→ch shows herbal=0 (consistent with F425, reproduced). Actual: herbal=0 reproduced. The astro cluster was unexpected (expected d-related formula types to be more distributed); the discovery of qok-LF astro-concentration is a new finding.

---

## Conclusion

H650 CONFIRMED (directional). Three section clusters: (1) **Astro**: qok-LF formula types (qok→sh→k/d→qok→ol/qok→ch→qo/qok→ch→ol, E=1.7-2.5×); (2) **Herbal**: content-routing formula types (d→ch→y=5.0×/y→sh→ch=3.1×/p→sh→ok=2.8×); (3) **Pharma+bio**: y→o→ch (herbal=0, consistent F425). d-LF and y-LF formula types SPLIT between sections: same LF class uses different routing in different sections. All findings directional (N=4-8 per type).
