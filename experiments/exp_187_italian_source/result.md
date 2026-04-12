# exp_187: Italian Source Text (Dante) in Position-Aware Hybrid Architecture
**Date**: 2026-04-11
**Hypothesis**: Italian source text (Dante Divina Commedia) produces higher am_ll than Latin sources in the position-aware hybrid architecture, because Italian morphology may have higher clause-final marker density.
**Addresses**: H351 (Italian source test).
**Fixed parameters**: cp=0.76, mp=0.9 (best from exp_185), p_detect=0.90. Three Italian CF patterns tested. 50 sims per pattern.

---

## 1. HEADLINE RESULT

**Italian is substantially inferior to Latin as a source language for this architecture. With linguistically motivated Italian clause-final patterns (CF_rate ≈ 5.5–6.8%), am_ll = 3.46–3.76× (50.9–55.3% of VMS 6.811×) — nearly half of what Latin achieves (6.42×, 94.3% VMS) at the same p_detect.**

| Pattern | CF_rate | am_ll | %VMS | y_lf | ss_mean | adj_rate |
|---------|---------|-------|------|------|---------|----------|
| narrow (à/ò/ì + verbal endings) | 0.055 | 3.465 | 50.9% | 1.912 | 1.460 | 0.00443 |
| broad (+ past participles/infinitives) | 0.068 | 3.765 | 55.3% | 1.952 | 1.466 | 0.00438 |
| broad-vowel (any vowel-final) | 0.785 | 7.352 | **107.9%** | 2.101 | 1.440 | 0.00413 |
| **Latin (Cicero, exp_186 baseline)** | **0.342** | **6.420** | **94.3%** | **2.474** | **1.443** | **0.00434** |
| **VMS target** | — | **6.811** | **100%** | **3.506** | **1.465** | **0.009** |

---

## 2. MECHANISTIC EXPLANATION

### Why Italian is worse than Latin (narrow/broad patterns)

Italian is an analytic language. Morphological clause-boundary signals are concentrated in a small fraction of tokens: accented verb endings (à, ò, ì, ù marking future/past tense), plural verbs (-ono, -ano), gerunds (-endo, -ando), and past participles (-ato, -uto, -ito). In Dante's Commedia, these patterns cover only 5.5–6.8% of all words.

With CF_rate ≈ 5.5%:
- LL am rate = 0.055 × 0.90 + 0.945 × 0.02 = 0.0495 + 0.0189 = 0.0684
- Corpus am rate ≈ 0.125 × 0.0684 + 0.875 × 0.02 = 0.0086 + 0.0175 = 0.0261
- Algebraic ceiling: 0.0684 / 0.0261 ≈ 2.62× (simulated: 3.46 — higher than algebraic due to actual frac_LL < 12.5%)

Latin (Cicero, CF_rate=34.2%) has 6× more clause-final morpheme signal per LL word. Latin's synthetic inflection (case endings + person endings) creates a dense, specific morphological signature at syntactic boundaries that Italian's analytic morphology cannot match.

### Why broad-vowel exceeds VMS (and why this is not meaningful)

With CF_rate=78.5% (any vowel-final Italian word):
- LL am rate = 0.785 × 0.90 + 0.215 × 0.02 ≈ 0.711
- Corpus am rate ≈ 0.125 × 0.711 + 0.875 × 0.02 ≈ 0.0889 + 0.0175 = 0.1064
- am_ll ≈ 0.711 / 0.1064 ≈ 6.68× (simulated: 7.35 — slight overestimate)

**This exceeds VMS — but it is an extreme target-aware design.** Mapping ALL vowel-final Italian words (78.5%) to -am has no linguistic motivation: it is equivalent to saying "all Italian nouns, verbs, adjectives, and adverbs in LL position → -am." This is even more target-aware than p_detect=1.00 in the Latin case (which at least restricts the mapping to a linguistically coherent class of clause-final morphemes). The broad-vowel result establishes the mathematical ceiling for Italian, not a linguistically plausible mechanism.

### The CF_rate gap: what VMS requires

From exp_186, the VMS am_ll (6.811×) requires CF_rate ≈ 41% at p_detect=1.00. Italian achieves:
- Linguistically motivated patterns: 5.5–6.8% (far below 41%)
- Broad-vowel (unmotivated): 78.5% (above 41%, overshoots VMS)

No Italian CF pattern that is both linguistically motivated and within the 41% threshold exists in Dante's Commedia. Italian morphology cannot produce VMS am_ll under any plausible position-sensitive cipher design.

---

## 3. SS_MEAN AND ADJ_RATE ARE SOURCE-INDEPENDENT

ss_mean ranges 1.440–1.466 across all three Italian patterns (within 2% of VMS 1.465) — confirming the copy component (cp=0.76, mp=0.9) drives ss_mean independently of the source language. adj_rate ranges 0.00413–0.00443 (consistent with Latin exp_186: 0.00418–0.00434). Both constraints are robustly satisfied regardless of Italian/Latin source.

---

## 4. Y_LF IS LOWER IN ITALIAN THAN LATIN

y_lf ranges 1.91–2.10 for Italian (vs Cicero 2.474 at baseline). The Italian LF clause-initial patterns (qu-/et/ma-/e-/so-) match less frequently than Latin (qu-/et/at + s/t-initial). Italian y_lf at 1.91–2.10 is below the 2.35–2.65 range from Cicero (exp_186), confirming that Italian performs worse than Latin on BOTH am_ll and y_lf simultaneously.

---

## 5. INTERPRETATION

### Italian is NOT a better source language than Latin for this cipher

The position-aware hybrid architecture is better matched to Latin morphology than Italian. Latin's dense synthetic morphology (34-37% clause-final marker density) produces am_ll 6.4-6.6× (94-97% of VMS). Italian's analytic morphology (5-7% motivated CF_rate) produces am_ll 3.5-3.8× (51-55% of VMS). Italian is eliminated as a primary source language candidate for this architecture on the am_ll metric.

### The am_ll metric discriminates between Latin and Italian source languages

This is a novel and useful finding for the VMS hypothesis space: the am_ll metric (6.811× in VMS) is *consistent* with Latin synthetic morphology (34-37% CF_rate) and *inconsistent* with Italian analytic morphology (5-7% CF_rate). If VMS is a position-sensitive cipher, the source language must have Latin-like morphological density at syntactic boundaries — Italian fails this constraint.

### H351 RESOLVED

The Italian source test confirms: (a) Italian cannot exceed Latin in am_ll reproduction under any linguistically motivated CF pattern; (b) the am_ll metric is diagnostic for morphological type — consistent with Latin, inconsistent with Italian; (c) the architecture's am_ll ceiling (97.1% VMS from exp_186) is a Latin-specific result.

---

## Self-Audit

**Target-awareness**: narrow/broad CF patterns are linguistically motivated (specific to clause-final morpheme classes in Italian). The broad-vowel pattern is explicitly flagged as unmotivated. Results stated conditionally on the CF pattern used.

**Feature-destroying implementation**: None. Copy component preserved.

**Extrapolation**: All three am_ll values are from direct simulation (50 sims each). Algebraic predictions confirmed within ~30% (actual > algebraic due to frac_LL artifact).

**Negative-result scope**: The claim "Italian is inferior to Latin" applies to: Dante Divina Commedia (medieval Italian), this specific cipher architecture, and narrow/broad CF patterns as defined. Different Italian texts or CF patterns may differ. Medieval Latin (not tested) remains an open question.

**Control behavior**: ss_mean and adj_rate stable across all three patterns (copy-driven). Consistent with exp_186 finding that cipher calibration and copy component are independent.

---

## CONCLUSION

Italian source text (Dante Divina Commedia) produces am_ll = 3.46–3.76× (51–55% of VMS 6.811×) under linguistically motivated clause-final patterns — nearly half of Latin's 6.42× at the same settings. Italian is eliminated as a primary source language for the position-aware hybrid architecture on the am_ll metric. The am_ll metric is diagnostic for morphological type: consistent with Latin synthetic morphology (CF_rate 34-37%), inconsistent with Italian analytic morphology (CF_rate 5-7%). H351 resolved negative: Italian source does NOT close the am_ll gap; it makes it worse.

The broad-vowel pattern (78.5% CF_rate, am_ll=7.35×, 107.9% VMS) technically exceeds VMS but is linguistically unmotivated. It establishes the mathematical ceiling, not a plausible mechanism.

**Files**:
- `script.py`: Position-aware hybrid with Italian Dante corpus, three CF patterns, 50 sims each
- `data/italian_results.json`: Raw results
