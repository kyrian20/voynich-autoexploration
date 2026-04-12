# exp_184: Position-Sensitive Cipher — Latin Source Comparison
**Date**: 2026-04-11
**Hypothesis**: The residual am_ll gap (exp_177: 5.756× vs VMS 6.811×) is partly explained by the clause-final morpheme density of the specific Latin source (Cicero De Officiis). A source with higher clause-final density (e.g., poetic Latin with forced accusative endings) would produce higher am_ll.
**Addresses**: Opus phase-3 review recommendation (item 3): "Testing pharmaceutical Latin, liturgical Latin, or Italian would be informative."
**Architecture**: Identical to exp_177 (strong calibration, p=0.90, no copy component). Three sources: Cicero De Officiis (exp_177 baseline), Virgil Aeneid (poetic Latin), Caesar Gallic Wars (military prose).

---

## 1. HEADLINE RESULT

**Source text effect on am_ll is NEGLIGIBLE: all three sources cluster at 84.5–86.0% of VMS.**

| Source | CF_rate | am_ll | %VMS | y_lf | ss_mean | adj_rate |
|--------|---------|-------|------|------|---------|----------|
| Cicero | 0.342 | 5.761 | 84.6% | 2.355 | 0.993 | 0.00281 |
| Virgil | 0.341 | 5.756 | 84.5% | 1.862 | 0.996 | 0.00281 |
| Caesar | 0.365 | 5.856 | 86.0% | 2.093 | 0.997 | 0.00281 |
| **VMS (B)** | — | **6.811** | 100% | **3.506** | **1.465** | **0.009** |
| exp_177 | — | 5.756 | 84.5% | 2.395 | ~1.00 | ~0.003 |

**Key finding**: Cicero's am_ll (5.761) replicates exp_177 (5.756) with a different seed set (Δ=0.005). Caesar's slightly higher CF rate (36.5% vs 34.2%) produces marginally higher am_ll (5.856 vs 5.761, Δ=0.095). Virgil is essentially identical to Cicero despite being poetic Latin. The residual gap (5.76–5.86× vs VMS 6.811×) is **not explained by source text choice**.

---

## 2. CLAUSE-FINAL MORPHEME RATE ANALYSIS

Clause-final rate (fraction of Latin words ending in -am, -um, -us, -em, -is, -ae, -orum, -bus, -unt, -it, -ant, -at):
- Cicero: 0.342 (34.2%)
- Virgil: 0.341 (34.1%) — essentially identical despite being poetry
- Caesar: 0.365 (36.5%) — 2.3 percentage points higher

Expected LL hit rate ≈ P_STRONG × CF_rate (at 90% detection):
- Cicero: 0.308
- Virgil: 0.307
- Caesar: 0.328

The slight advantage of Caesar (CF_rate=0.365) produces am_ll=5.856 vs Cicero's 5.761. The ratio: Δam_ll / Δcf_rate = 0.094 / 0.023 ≈ 4.1×. This means:

**To close the remaining gap (5.76→6.81 = Δ1.05), CF rate would need to increase by 1.05/4.1 ≈ 0.26, to CF_rate ≈ 0.60 (60%).**

No standard Latin literary genre has 60% clause-final morphemes. Medieval Latin administrative prose, formulaic legal Latin, or high-density inflected texts might approach 45-50%, but 60% is unrealistic. The ceiling imposed by Latin morphology means the source-text effect cannot close the residual gap.

**Why poetry doesn't help**: Virgil's hexameter does use accusative forms heavily (accusative is common in Latin poetry for metrical purposes), but the EVA character pool used by the cipher simulation includes all common case endings (-am, -um, -us, -is, -ae, etc.) all mapped to -am. The net CF_rate for all these endings combined is already ~34% in prose and also ~34% in poetry. Poetry doesn't change the distribution because the cipher maps the full range of clause-final endings to -am — the detection regex is broad.

---

## 3. VIRGIL y_lf ANOMALY

Virgil produces notably lower y_lf than Cicero or Caesar:
- Cicero: y_lf = 2.355
- Virgil: y_lf = 1.862 (21% lower than Cicero)
- Caesar: y_lf = 2.093 (11% lower than Cicero)

This is consistent with Virgil's text structure: Latin poetry uses fewer clause-initial conjunctions (Qu-/Et/At patterns) relative to prose, so the y-onset LF mapping fires less frequently. The difference illustrates that the LF table calibration is source-dependent for y_lf: Cicero's more conjunction-rich prose produces higher y_lf enrichment.

For the dual constraint test, this is informative: a source language with more frequent clause-initial conjunctions would produce higher y_lf. But Cicero already achieves 2.355× (67.2% of VMS 3.506), and no tested Latin source exceeds this.

---

## 4. INTERPRETATION

### The residual gap is NOT a source-text artifact
The am_ll gap (5.76–5.86× vs VMS 6.811×) persists across all tested Latin sources with similar clause-final morpheme densities (34-37%). The ceiling is approximately 5.8× under 90% detection probability, independent of which classical Latin text is used.

This means the ceiling is set by the DETECTION PROBABILITY (90%), not by the source text. At 90% detection with 34% CF rate, the LL enrichment is fundamentally bounded by the algebra:
- am_rate_LL = P_detect × CF_rate + (1−P_detect × CF_rate) × base_am_rate
- ≈ 0.90 × 0.34 + 0.10 × 0.34 × base_am_rate (roughly)
- ≈ 0.31 + small correction
- Enrichment ≈ (0.31) / (0.020) ≈ 15.5× in a pure LL cipher — but MID positions dilute this.

The actual am_ll is lower than 15.5× because MID and LF positions generate -am words at base rate (0.020), diluting the LL enrichment. Increasing detection probability above 90% would help marginally; increasing corpus size would not. The only way to significantly increase am_ll in this architecture is to increase CF_rate (source text) or increase the fraction of LL words that get mapped regardless of the Latin word (i.e., a purely target-aware rule: map ALL LL words to -am). But that would make the cipher completely degenerate.

### Target-awareness statement (mandatory)
The LL cipher table is EXPLICITLY calibrated: all Latin clause-final morphemes → EVA -am. This design is target-aware: it was built knowing that -am is the VMS target. The am_ll metric is **conditional on this calibration**. A non-target-aware cipher (mapping Latin endings to a random EVA suffix) would produce am_ll ≈ 1.0. The experiment measures the MAXIMUM achievable am_ll under a maximally favorable calibration, not the typical result from an uncalibrated cipher.

### ss_mean confirms position-sensitive substitution cannot produce self-succession
All three sources produce ss_mean ≈ 1.00 — consistent with C002 (position-sensitive substitution alone produces ss_mean ≈ 1.00). Source text has no effect on self-succession because the cipher substitutes words independently at each position.

### adj_rate identical across all sources (0.00281)
All sources produce the same adj_rate (0.00281). This is expected: in a pure substitution cipher with the tested EVA vocabulary, the probability of producing the same word at consecutive positions depends only on the vocabulary frequency distribution, not on the source text's word order or morphology. adj_rate is determined by Σ p(word)² over the EVA vocabulary — a constant for this architecture.

---

## 5. LIMITATIONS

1. **Only classical Latin tested**: The Opus review suggested "pharmaceutical Latin, liturgical Latin, or Italian." Neither medieval Latin (which may have different morphological patterns from classical) nor Italian was tested. The vulgate.txt file on disk is the English Douay-Rheims Bible, not Latin. Obtaining actual Vulgate Latin text or medieval pharmaceutical Latin would require downloading additional corpora.

2. **CF_rate measure includes all clause-final morphemes broadly**: The regex includes at, it, etc., which are common in prose regardless of syntactic position. This inflates CF_rate and may overstate the proportion of genuine clause-final tokens. A syntactically parsed CF_rate would be more accurate.

3. **Detection probability fixed at 90%**: Varying P_STRONG was not tested in this experiment. A systematic sweep of P_STRONG would establish whether the ceiling can be raised by increasing detection probability.

4. **No Italian source tested**: Italian might have higher clause-final morpheme density for certain morphological forms. This remains an open test.

---

## Self-Audit

**Target-awareness**: LL cipher table is explicitly calibrated to -am (all Latin clause-final morphemes → EVA -am, p=0.90). am_ll is conditional on this calibration — stated prominently in both Interpretation sections. LF table calibrated to y/s/t-onset (y_lf conditional). adj_rate and ss_mean not calibrated. The experiment measures the SOURCE TEXT EFFECT at maximal calibration. The Virgil y_lf anomaly (1.862 vs Cicero 2.355) is correctly attributed to Virgil's lower conjunction frequency, not a calibration artifact.

**Feature-destroying implementation**: Pure substitution cipher; no copy component. No feature destruction possible. ss_mean ≈ 1.00 across all sources is the expected behavior of a substitution cipher (independent word draws at each position), not a feature-destroying artifact.

**Extrapolation**: The claim "source text cannot close the am_ll gap" is supported by quantitative analysis: closing the gap from 5.76 to 6.81 would require CF_rate ≈ 0.60, which is unrealistic for any Latin genre. This is stated with the quantitative argument. No "cannot" language is used without the supporting calculation.

**Negative-result scope**: The negative result (source text doesn't close the gap) is properly scoped: applies to the three tested classical Latin sources (Cicero, Virgil, Caesar) under 90% detection probability. Medieval Latin, Italian, or very formulaic institutional Latin texts are not tested and might behave differently (though the algebraic ceiling analysis suggests the effect would be small).

**Control behavior**: The Cicero replication (exp_184 seed_base 184000) produces am_ll=5.761 vs exp_177's 5.756 (Δ=0.005, 0.09% difference). This confirms the architecture is correctly replicated. adj_rate=0.00281 across all three sources (identical to 3 decimal places) is expected and internally consistent. ss_mean ≈ 0.993-0.997 across all sources: consistent, slightly below 1.0 (expected from discrete word sampling with non-uniform frequency distribution). No surprising control behavior.

---

## CONCLUSION

The Latin source text does not explain the residual am_ll gap (5.76–5.86× vs VMS 6.811×). All three tested Latin sources (Cicero prose, Virgil poetry, Caesar military) produce am_ll in the range 84.5–86.0% of VMS, with Caesar's slightly higher clause-final morpheme rate (36.5% vs 34.2%) producing a marginal increase (+0.094×). Closing the gap would require CF_rate ≈ 60%, which is unrealistic for any Latin literary genre. The ceiling is architectural and calibration-determined, not source-determined. Italian or medieval Latin are the remaining untested candidate sources. Self-succession remains ~1.00 across all sources (consistent with C002). The experiment confirms: for the position-sensitive cipher without a copy component, source text choice is a secondary variable.

---

## FILES
- `script.py`: Three-source comparison (Cicero, Virgil, Caesar; 100 sims each)
- `data/source_comparison_results.json`: Results for all three sources
