# exp_186: Detection Probability Sweep — Hard am_ll Ceiling of Position-Aware Hybrid Architecture
**Date**: 2026-04-11
**Hypothesis**: Higher detection probability (p_detect > 0.90) for the LL cipher table closes the am_ll gap. At p_detect=1.00 (all clause-final words → -am), am_ll approaches VMS target (6.811×).
**Addresses**: H352 (can p_detect increase close am_ll gap?).
**Fixed parameters**: cp=0.76, mp=0.9 (best joint approximation from exp_185). p_ll ∈ {0.90, 0.95, 1.00}, p_lf ∈ {0.90, 1.00}. 6 combinations × 50 sims = 300 runs.

---

## 1. HEADLINE RESULT

**The architecture has a hard am_ll ceiling of approximately 6.61× (97.1% of VMS 6.811), reached at p_ll=1.00, p_lf=1.00. Increasing detection probability above 0.90 cannot close the residual gap.**

| p_ll | p_lf | am_ll | %VMS  | y_lf  | %VMS  | ss_mean | adj_rate |
|------|------|-------|-------|-------|-------|---------|----------|
| 0.90 | 0.90 | 6.420 | 94.3% | 2.474 | 70.6% | 1.443   | 0.00434  |
| 0.90 | 1.00 | 6.417 | 94.2% | 2.651 | 75.6% | 1.463   | 0.00430  |
| 0.95 | 0.90 | 6.550 | 96.2% | 2.555 | 72.9% | 1.448   | 0.00423  |
| 0.95 | 1.00 | 6.570 | 96.5% | 2.634 | 75.1% | 1.466   | 0.00423  |
| **1.00** | **0.90** | **6.579** | **96.6%** | **2.507** | **71.5%** | **1.468** | **0.00418** |
| **1.00** | **1.00** | **6.608** | **97.0%** | **2.620** | **74.7%** | **1.449** | **0.00426** |
| VMS target | — | **6.811** | **100%** | **3.506** | **100%** | **1.465** | **0.009** |

**am_ll gain from p_detect increase** (p_lf=0.90, varying p_ll):
- 0.90 → 0.95: +0.130× (gain: 1.9% VMS)
- 0.95 → 1.00: +0.029× (gain: 0.4% VMS — strongly diminishing returns)
- Total gain 0.90 → 1.00: +0.159× (2.3% VMS)

The remaining gap at p_detect=1.00 is **0.203× (3.0% of VMS)** — structural to the architecture.

---

## 2. WHY THE CEILING IS STRUCTURAL

At p_ll=1.00, ALL clause-final Latin words at LL positions are mapped to -am. With the Cicero source (CF_rate=34.2%), the LL am rate = CF_rate × 1.00 + (1−CF_rate) × base_am_rate ≈ 0.342 + 0.658 × 0.020 ≈ 0.355.

The 65.8% of LL words that lack clause-final morphemes get the base distribution (am rate ≈ 2%), permanently limiting how high the LL am rate can go. Even at 100% detection, LL am rate ≈ 35.5%, not 100%. The enrichment (LL am rate / corpus am rate) is then bounded by the Latin source's CF_rate.

**To close the remaining 3% gap at p_detect=1.00**: would require CF_rate ≈ 41% (from the linear extrapolation of the gain curve). Caesar Gallic Wars has CF_rate=36.5% (exp_184) — likely to push am_ll to ~6.67 at p_detect=1.00. A hypothetical text with CF_rate=41% would close the gap. No tested classical Latin source achieves this.

---

## 3. SS_MEAN IS STABLE ACROSS ALL P_DETECT VALUES

ss_mean ranges 1.443–1.468 across all 6 combinations (within 1.5% of VMS 1.465). The copy component drives ss_mean, not the cipher table calibration. This confirms that the cipher tables (LF/LL) and the copy component (cp/mp) are structurally independent: adjusting detection probability does not affect self-succession.

---

## 4. Y_LF HAS A SEPARATE CEILING

y_lf ranges 2.474–2.651 (70.6–75.6% of VMS 3.506). At p_lf=1.00, y_lf = 2.620–2.651. This ceiling (~75% of VMS) is driven by the fraction of LF Latin words matching the clause-initial patterns (Qu-/et/at + s/t-initial). Even at 100% detection of these patterns, ~25% of VMS y_lf remains unaccounted for. This y_lf gap is separate from the am_ll gap and has not been systematically addressed in the hybrid architecture.

---

## 5. INTERPRETATION

### The Position-Aware Hybrid Architecture Is Fully Characterized

After exp_180–186, the position-aware hybrid with Timm character modification has been exhaustively explored:

**What it achieves (at optimal parameters cp=0.74–0.76, mp=0.8–0.9, p_detect=0.90–1.00)**:
- ss_mean: 1.443–1.468 (98.5–100.2% of VMS) ✓ — reproducible within 1.5%
- adj_rate: 0.004–0.007 (well below VMS 0.009) ✓ — consistently satisfied
- am_ll: 6.42–6.61 (94.3–97.1% of VMS) — **3–5.7% below VMS ceiling**
- y_lf: 2.47–2.65 (70.6–75.6% of VMS) — **24–29% below VMS ceiling**

**What it cannot achieve without architectural change**:
- am_ll ≥ 6.81× (would require CF_rate ≥ 41% or a different LL cipher design)
- y_lf ≥ 3.51× (would require clause-initial Latin frequency ≥ actual VMS y-onset LF frequency)

### Target-awareness statement (mandatory)
p_ll=1.00 means ALL clause-final Latin words → -am deterministically. This is the maximally target-aware design — the LL table is 100% calibrated to the VMS target. The am_ll metric at p_ll=1.00 is **fully conditional on this calibration**. A non-calibrated cipher table would produce am_ll ≈ 1.0×. The experiment establishes the ceiling of maximum calibration, not a result achievable from a naive cipher.

---

## 6. LIMITATIONS

1. **Only Cicero tested at p_detect=1.00**: Caesar (CF_rate=36.5%) might push am_ll to ~6.67 at p_detect=1.00. This would narrow the gap from 3.0% to ~2.1%.

2. **CF_rate definition includes broad pattern**: The regex includes common verb endings (at, it, unt) that appear in many syntactic positions, not just clause-final. True syntactic clause-final rate may differ.

3. **y_lf gap not explained**: The y_lf ceiling (~75% of VMS at p_lf=1.00) means LF clause-initial patterns in Latin account for only 75% of VMS y-onset LF enrichment. The remaining 25% is unexplained by the cipher architecture.

---

## Self-Audit

**Target-awareness**: p_ll=1.00 is maximally target-aware (LL table 100% calibrated to -am). This is stated prominently. ss_mean is NOT target-aware (driven by copy component). The experiment explicitly tests the LIMIT of target calibration. Result stated as "ceiling under maximum calibration" — correctly conditional.

**Feature-destroying implementation**: No feature-destroying elements. The Timm modification continues to preserve onset ~79%.

**Extrapolation**: The claim "hard ceiling at ~97% of VMS" is supported by algebraic analysis (CF_rate × p_detect + non-CF_rate × base_rate) and confirmed empirically (p_detect=1.00 gives 97%). No "cannot" language without supporting argument.

**Negative-result scope**: The result is that the architecture cannot produce am_ll ≥ 6.81× within this design. The scope is: this specific architecture (position-sensitive cipher + MID-only copy buffer + Timm modification + Cicero Latin source). Different architectures (e.g., MID position also enriched for -am, or different source text) are untested.

**Control behavior**: ss_mean ≈ 1.45–1.47 across all 6 combinations (expected: copy component drives ss_mean, cipher tables don't). adj_rate ≈ 0.00418–0.00434 (expected: copy parameters fixed, slight variation from different cipher tables creating different buffer content). Both are internally consistent.

---

## CONCLUSION

The position-aware hybrid architecture has a hard am_ll ceiling of ~6.61× (97.1% of VMS 6.811) at maximum detection probability (p_ll=1.00, Cicero Latin source). This ceiling cannot be broken within the current architecture. The remaining 3% gap is structural — driven by the 65.8% of LL Latin words lacking clause-final morphemes even in the best-case source text. The mechanism is fully characterized: it reproduces VMS ss_mean to within 1.5% and adj_rate well below VMS at optimal cp/mp settings, but cannot reach VMS am_ll by parameter tuning alone. **The architecture is the closest any tested mechanism has come to joint VMS constraint satisfaction, but is not fully ruled IN as the VMS mechanism without explaining the am_ll gap.**

The natural next steps are: (a) a different LL cipher architecture (e.g., one that maps a broader class of LL Latin patterns to -am), (b) Italian or medieval Latin source text (H351), or (c) a fundamentally different generation model.

---

## FILES
- `script.py`: p_detect sweep at fixed cp=0.76, mp=0.9 (6 combinations × 50 sims)
- `data/pdetect_results.json`: Raw results
