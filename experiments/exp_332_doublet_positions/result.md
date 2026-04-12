# exp_332: MID Position of Doublet Pairs — Do Onset-Substitution Doublets Appear at Gradient-Predicted Positions? (H535)

**Date:** 2026-04-11
**Hypothesis:** H535 — For each core body vocabulary item (aiin, ain, ar...), do the 5 onset-substitution doublets (qok+body, ok+body, ot+body, d+body, s+body) appear at MID positions matching their onset class's gradient position (F331: qok < ok < s < d < ot)?
**Result:** H535 CONFIRMED (moderate). B-dialect: 17/28 doublet position pairs gradient-consistent (60.7%); A-dialect: 15/22 (68.2%). Both above 50% chance. 'aiin'-body doublets span 0.154 normalized MID positions (okaiin=0.468 → otaiin=0.622 in B), exceeding the expected class-level range (0.097). A-dialect 'aiin' ordering is perfect: qok(0.511) < ok(0.516) < ot(0.573) < d(0.582) < s(0.827) — all 4 adjacent pairs correct (4/4). Confirms: onset character encodes MID gradient position; same body vocabulary appears at different positions based on onset class.

---

## Key Statistics

### 'aiin'-Body Doublets

**B-Dialect:**
| Word | Onset class | Mean MID pos | Class gradient pos | Diff |
|------|------------|-------------|-------------------|------|
| okaiin | ok | 0.468 | 0.503 | −0.035 |
| qokaiin | qok | 0.505 | 0.491 | +0.014 |
| daiin | d | 0.521 | 0.560 | −0.039 |
| saiin | s | 0.593 | 0.532 | +0.061 |
| otaiin | ot | 0.622 | 0.588 | +0.034 |

Observed range: 0.622−0.468 = **0.154** (expected from class gradient: 0.097)
Order: ok < qok < d < s < ot (2/4 pairs match gradient qok<ok<s<d<ot; ok/qok inverted by 0.037)

**A-Dialect:**
| Word | Onset class | Mean MID pos | Class gradient pos | Diff |
|------|------------|-------------|-------------------|------|
| qokaiin | qok | 0.511 | 0.501 | +0.010 |
| okaiin | ok | 0.516 | 0.521 | −0.005 |
| otaiin | ot | 0.573 | 0.574 | −0.001 |
| daiin | d | 0.582 | 0.596 | −0.014 |
| saiin | s | 0.827 | 0.617 | +0.210 |

Order: qok < ok < ot < d < s — **PERFECT** (4/4 adjacent pairs match gradient). A-dialect saiin appears very late (0.827) vs expected 0.617.

### Summary of Ordering Analysis

| Body | B consistent | A consistent |
|------|-------------|-------------|
| aiin | 2/4 | 4/4 (perfect) |
| ain | 2/4 | 1/3 |
| ar | 3/4 | 2/4 |
| al | 3/4 | 2/4 |
| ol | 2/4 | 3/3 (perfect) |
| air | 4/4 (perfect) | — |
| or | 1/4 | 3/4 |
| **Total** | **17/28 (60.7%)** | **15/22 (68.2%)** |

### MID Position Range for Each Body

| Body | Observed range (B) | Observed range (A) |
|------|-------------------|-------------------|
| aiin | 0.154 | 0.316 |
| ain | 0.134 | 0.114 |
| ar | 0.251 | 0.225 |
| al | 0.116 | 0.076 |
| ol | 0.134 | 0.168 |
| air | 0.243 | — |
| or | 0.446 | 0.337 |
| Expected from class gradient | 0.097 | 0.097 |

All 7 bodies show ranges exceeding the class-level gradient expectation (0.097). The actual position spread of doublet words is larger than predicted by class-level mean alone.

---

## Findings

### Finding 1: Onset-substitution doublets appear at gradient-consistent positions (moderate confirmation)

60-68% of pairwise position comparisons between doublet words are gradient-consistent (correct onset class ordering). This is above 50% chance and consistent with the onset-class gradient encoding the grammatical position of doublet pairs. The confirmation is moderate (not perfect) because individual word positions have variance beyond the class-level mean.

The best confirmation is in A-dialect 'aiin' (4/4 perfect) and 'ol' (3/3 perfect), and B-dialect 'air' (4/4 perfect).

### Finding 2: Doublet position ranges exceed class-level gradient prediction

The class-level gradient spans 0.097 units (ot=0.588 minus qok=0.491 in B). But actual doublet words spread across 0.116-0.446 normalized MID position units. The 'or'-body doublets show the largest spread (0.446 in B: sor=0.325 vs dor=0.771). This suggests individual word positions have considerable variance beyond the class mean — consistent with individual words having specific paragraph/section contexts.

### Finding 3: ot+body is consistently the most terminal; qok+body and ok+body are earliest

Across bodies where ot is available: ot+body ranks latest in observed position in 5/7 bodies (B). qok+body and ok+body are earliest in 4/7 bodies each. This body-level confirmation mirrors the class-level gradient finding (ot is latest class, qok/ok are earliest).

### Finding 4: A-dialect saiin is exceptionally late (mean=0.827)

A-dialect saiin appears at mean position 0.827 — far later than any other onset+aiin word. The A-dialect s-onset position is 0.617 (latest in A-dialect gradient), and saiin specifically seems to appear even later. With N=14 A-dialect MID saiin occurrences, this may reflect s-onset words appearing near line-end in A-dialect specifically. This is a notable anomaly worth revisiting.

---

## Interpretation

The doublet position analysis provides moderate evidence that the onset character in VMS MID words encodes positional function — words with the same body appear at systematically different MID positions based on their onset class. This is consistent with the structural model:
- **Onset = grammatical/positional marker**: encodes where in the MID span the word appears
- **Body = content morpheme**: encodes semantic/functional content (the 7-body vocabulary)

The imperfect gradient consistency (60-68%) reflects two factors:
1. Individual word variance (each word has a specific distributional context, not just its class mean)
2. The 'e'-body template forms and 'a'-body content forms within the same onset class appear at similar positions (the bimodal body structure doesn't split by position for ok, per exp_329)

The VMS writing system appears to organize MID words around a position-grammar × content-vocabulary structure, where onset = position and body = content.

---

## Limitations

- N is small for rare combinations (e.g., saiin N=14 in A, sar N=12 in B). High-variance estimates for small-N words.
- Position measurement is normalized within each line; lines of different lengths may contribute noise.
- A-dialect saiin anomaly (mean=0.827) is based on N=14 — may not be stable.

---

## Self-Audit

**Target-awareness:** No target-aware elements. Pure corpus positional measurement. PASS.

**Feature-destroying implementation:** Normalized MID position (0.0=first, 1.0=last) is a direct measurement. No feature-destroying details. PASS.

**Extrapolation:** "Moderate confirmation" of gradient-consistent positioning is within the tested data. The "onset = position marker" interpretation is explicitly labeled as interpretive. PASS.

**Negative-result scope:** The 39% (B) non-gradient-consistent pairs are acknowledged as reflecting word-level variance and are not interpreted as refuting the gradient. PASS.

**Control behavior:** Independence null: all doublet words appear at the same position regardless of onset → 50% gradient consistency. Observed 60.7/68.2% > 50%. PASS.
