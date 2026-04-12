# exp_429: Astro-Section qok-LF Grammar

**Hypothesis (H651):** Is qok-LF more common in the astro section (driving formula-type concentration from F430), or is only the specific formula-type routing astro-specific?

**Method:** B continuation lines. Section classification by folio number (herbal ≤72, astro 73-84, bio 85-102, pharma 103-116). Compute qok-LF rate by section. For qok-LF lines, compute pos1 distribution by section. Compare section-specific rates to global qok-LF baseline.

---

## Results

### qok-LF rate by section

| Section | qok-LF lines | Total lines | Rate | E vs global (10.2%) |
|---------|-------------|-------------|------|---------------------|
| herbal | 16 | 277 | 5.8% | **0.56×** |
| **astro** | **147** | **750** | **19.6%** | **1.91×** |
| bio | 13 | 219 | 5.9% | **0.58×** |
| pharma | 58 | 1038 | 5.6% | **0.55×** |
| **Global** | **235** | **2293** | **10.2%** | — |

The astro section has **1.91× the global qok-LF rate**, while all other sections are at 0.55-0.58× (collectively depleted). Every astro folio (f75-f84) contributes qok-LF lines (6-12 per folio, uniform distribution across all 20 astro folios).

### qok-LF pos1 routing by section

| Pos1 onset | herbal (N=16) | astro (N=147) | bio (N=13) | pharma (N=58) |
|-----------|---------------|---------------|------------|---------------|
| sh | 12.5% | 16.3% | 0.0% | 12.1% |
| ch | 25.0% | 20.4% | 15.4% | **29.3%** |
| qok | 12.5% | 18.4% | 7.7% | 13.8% |
| qo | 6.2% | 4.1% | **23.1%** | 0.0% |
| d | 12.5% | 4.8% | 0.0% | 1.7% |
| o | 6.2% | 2.0% | 15.4% | 0.0% |

**E(pos1|qok-LF, section) vs global qok-LF pos1 baseline:**
- sh: astro=1.16× (mild elevation), others near baseline
- ch: pharma=1.29× (mild elevation), astro=0.90× (mild depletion)
- k: astro=1.59×(N=2, directional)
- qo: bio=5.40×(N=3, directional)

**No dramatic section-specific routing**: qok-LF pos1 distribution is broadly similar across sections (sh 12-16%, ch 15-29%, qok 8-18%). The mild differences do not reach formula-type thresholds.

---

## Interpretation

**H651 ANSWERED.** The astro section formula-type concentration (F430: qok-LF formula types E=1.7-2.5× in astro) is driven primarily by **the 1.91× elevated qok-LF rate in astro**, NOT by section-specific formula routing.

**Mechanism**: The astro section has ~19.6% qok-LF lines vs ~5.8% elsewhere. Since formula types like qok→sh→k/qok→ch→qo/qok→ch→ol require qok at LF, the elevated LF rate mechanically produces more formula-type instances in astro. The pos1 routing after qok-LF is relatively uniform across sections (~12-16% sh, ~15-29% ch).

**Implication**: The astro section is characterized by **qok-class LF selection**, not qok-specific formula routing grammar. Something about the astro content systematically produces qok-onset words as line-first words (at nearly 2× the rate of other sections). This could reflect the content (astronomical labels, planet names, zodiac terms → qok-class word shapes) or scribal convention for this section type.

All 20 astro folios (f75-f84) contribute uniformly — this is not driven by 1-2 outlier folios.

---

## Limitations

- Section classification by folio number is approximate.
- qok-LF pos1 routing differences are small (N per section modest for some cells).
- The mechanism by which astro content generates qok-LF words is not identified by this analysis.

---

## Self-Audit

**Target-awareness**: No target-aware elements.

**Feature-destroying implementation**: No feature-destroying elements.

**Extrapolation**: The mechanism claim (elevated qok-LF rate drives formula-type concentration) is supported by the data: 1.91× qok-LF rate in astro, pos1 routing near-uniform. This is within the tested parameter range.

**Negative-result scope**: The conclusion "no dramatic section-specific pos1 routing" is stated for this section×pos1 grid only.

**Control behavior**: No explicit control. The global qok-LF rate (10.2%) serves as baseline. Expected (from F430): astro-concentrated formula types. Actual: confirmed, driven by 1.91× qok-LF rate. Control behaved as expected.

---

## Conclusion

H651 ANSWERED. qok-LF rate is 1.91× elevated in astro (19.6% vs 5.6-5.9% in herbal/bio/pharma). Astro formula-type concentration (F430) is driven by elevated qok-LF RATE, not section-specific routing. All 20 astro folios (f75-f84) contribute uniformly (6-12 qok-LF lines each). Astro section is characterized by qok-class LF selection at nearly 2× global rate.
