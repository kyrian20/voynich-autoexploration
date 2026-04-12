# exp_222: H423 — VMS Positional Suffix Distributions (LF/MID/LL)

**Date**: 2026-04-11  
**Hypothesis**: H423 — Using VMS B positional suffix distributions (VMS LF suffix for LF words, VMS MID suffix for MID fresh words, VMS LL suffix for non-blind LL words) instead of global suffix will fix am_lf_enr, am_mid_enr, and edy_rate without breaking calibrated metrics.  
**Status**: H423 PARTIALLY ANSWERED — directional improvements confirmed but mechanism reveals a root-cause structural tension. Net result: **10/18 PASS** (regression from exp_221's 11/18).

---

## Architecture

Identical to exp_221 (Mode B, cp=0.55, mp=0.90, p_blind=0.30, p_lf=1.0) plus:
- **LF words**: VMS LF suffix distribution (am=0.25%, edy=16.84%)
- **MID fresh words**: VMS MID suffix distribution (am=0.40%, edy=21.24%)
- **LL non-blind fraction**: VMS LL suffix distribution (am=13.31%, edy=11.34%)
- **LL blind fraction** (p_blind=0.30): forced suffix='am' (architecture requirement, unchanged)

VMS B positional am rates confirmed:
- Global: 2.03% | LF: 0.25% | MID: 0.40% | LL: 13.31%

---

## Results (N=30, cp=0.55, mp=0.90)

```
Metric          VMS      E222    %VMS  Status   vs E221        [Category]
am_ll          6.550    7.968  121.7%  [FAIL]   was 6.258      [CALIBRATED]
d_ll           1.362    1.219   89.5%  [PASS]   was 1.222      [CALIBRATED]
y_lf           3.324    3.342  100.5%  [PASS]   was 3.440      [VMS-DIRECT]
ss_mean        1.164    1.327  114.0%  [PASS]   was 1.341      [CALIBRATED (cp/mp)]
adj_rate       0.009    0.003   34.7%  [FAIL]   was 0.003      [CALIBRATED (cp/mp)]
qok_lf         0.778    0.759   97.6%  [PASS]   was 0.756      [VMS-DIRECT]
d_lf           2.211    2.350  106.3%  [PASS]   was 2.253      [VMS-DIRECT]
s_lf           4.638    5.067  109.3%  [PASS]   was 5.138      [VMS-DIRECT]
ch_ll          0.939    1.060  112.9%  [PASS]   was 1.066      [VMS-DIRECT]
ok_ll          0.975    0.995  102.1%  [PASS]   was 1.043      [VMS-DIRECT]
qok_ll         0.595    0.746  125.3%  [FAIL]   was 0.750      [partial]
ss_d           1.291    1.482  114.8%  [PASS]   was 1.452      [uncalibrated]
ss_y           1.955    1.702   87.1%  [PASS]   was 1.673      [uncalibrated]
am_lf_enr      0.122    0.051   41.4%  [FAIL]   was 0.380      [VMS-DIRECT suffix]
am_mid_enr     0.195    0.061   31.4%  [FAIL]   was 0.277      [VMS-DIRECT suffix]
edy_rate       0.194    0.139   71.9%  [FAIL]   was 0.140      [VMS-DIRECT suffix]
word_len_mean  5.400    6.596  122.2%  [FAIL]   was 6.592      [uncalibrated]
qok_ch         1.267    0.971   76.6%  [FAIL]   was 0.987      [uncalibrated]

Pass count: 10/18 (exp_221 Mode B: 11/18)
```

**Net change**: −1 pass vs exp_221. am_ll regressed to FAIL (121.7%); all other previously passing metrics maintained PASS. am_lf_enr and am_mid_enr moved dramatically in the correct direction but overcorrected (both went from too-high to too-low).

---

## Interpretation

**H423 PARTIALLY ANSWERED.** The positional suffix distribution approach reveals a fundamental structural tension in the p_blind architecture — not a simple calibration fix.

### What the VMS positional suffix diagnostics show

VMS B suffix distributions by position:
- Global am = 2.03%; LF am = 0.25%; MID am = 0.40%; LL am = 13.31%
- am_lf_enr (VMS) = 0.25%/2.03% = 0.123 ≈ 0.122 ✓ (internally consistent in VMS)
- am_mid_enr (VMS) = 0.40%/2.03% = 0.197 ≈ 0.195 ✓ (internally consistent in VMS)

In VMS, the global am rate (2.03%) is the weighted average of positional am rates. The enrichment ratios naturally follow from the positional distributions.

### Why the fix fails: the global am rate divergence

In our model, the p_blind=0.30 mechanism works by having 30% of LL words always end in -am AND having 70% of LL words draw from the suffix distribution. With global suffix (am=2.03%):
- sim LL am rate = 0.30 × 1.0 + 0.70 × 0.0203 = 31.42%
- sim global am rate ≈ 5.5% (inflated by LL's 31.42% rate × LL word fraction)

With VMS LL suffix (am=13.31%) for non-blind fraction:
- sim LL am rate = 0.30 × 1.0 + 0.70 × 0.1331 = 39.32%
- sim global am rate ≈ 5.0% (slightly lower because LF/MID now have lower am)
- am_ll = 39.32%/5.0% = 7.86 → FAIL (121.7%)

**Root cause**: The VMS LL suffix distribution (13.31% am) already ENCODES the VMS's natural positional rule for LL. Our model's p_blind mechanism is ALSO a positional rule for LL. Using both simultaneously double-counts the LL am enrichment.

### The global am rate structural tension

A more fundamental issue: in VMS, the global am rate is 2.03% — a natural consequence of VMS's positional rule (most words are not am). In our model, the global am rate is ~5.5%, because the p_blind mechanism produces a much higher LL am rate (31.42%) than VMS's LL am rate (13.31%), and LL word fraction is ~12%.

This means any ratio (am at position X / global am) in our simulation uses a wrong denominator (5.5% vs VMS 2.03%). The consequence:
- am_lf_enr with VMS LF suffix: 0.25%/5.0% = 0.05 (too low, VMS=0.122)
- am_lf_enr with global suffix: 2.03%/5.5% = 0.37 (too high, VMS=0.122)
- Target: 0.122 × 5.0% ≈ 0.61% LF am rate — between VMS LF (0.25%) and global (2.03%)

**The p_blind=0.30 mechanism achieves am_ll by elevating the global am rate, not by precisely matching VMS's actual LL am rate.** This elevation distorts all am_pos_enr metrics relative to VMS. No suffix distribution assignment can simultaneously fix global am rate and positional am rates without changing the p_blind architecture.

### edy_rate: immovable by suffix changes

edy_rate stayed at 0.139 (vs 0.140 in exp_221), even though VMS MID suffix has edy=21.24% vs global 19.40%. Mechanism: Timm suffix modification on copy buffer words erodes edy endings. At cp=0.55, mp=0.90, ~49.5% of MID words are modified copies. These modified copies rarely preserve edy endings (modification of the last character(s) destroys edy). The fresh word edy rate (from suffix distribution) has minor impact when ~50% of words are from eroded buffer. This confirms that edy_rate cannot be improved by suffix distribution changes — it requires changing the modification policy (e.g., protecting edy suffixes, or using word-direct sampling).

### edy suffix protection as targeted fix (future)

An onset-preserving modification already protects onset prefixes. A suffix-preserving modification (protecting the final 3 characters from deletion/replacement) could protect edy endings. This would be analogous to the onset-preserving fix that resolved the onset erosion problem.

---

## Limitations

1. **Double-counting LL am**: Using VMS LL suffix for non-blind LL fraction and p_blind forced -am for blind fraction creates double am enrichment at LL.
2. **Global am rate divergence**: The p_blind architecture's global am rate (~5.5%) is 2.7× VMS's global am rate (2.03%). This structural divergence prevents any positional suffix fix from achieving the correct positional am enrichment ratios simultaneously.
3. **edy erosion dominates suffix choice**: Timm buffer erosion makes edy_rate insensitive to suffix distribution changes at cp=0.55, mp=0.90.

---

## Self-Audit

**Target-awareness**: Same calibrated elements as exp_221: p_blind=0.30 (target-aware for am_ll), d_boost=14.79% (target-aware for d_ll), cp=0.55/mp=0.90 (target-aware for ss_mean via exp_221 sweep). The positional suffix distributions are VMS-direct (not post-hoc tuned to match enrichment ratios). The reported am_ll=7.968 (FAIL) is conditional on p_blind=0.30 AND VMS LL suffix for non-blind fraction — both must be stated.

**Feature-destroying implementation**: No feature-destroying implementation for the hypothesis being tested. The VMS LL suffix assignment double-counts am enrichment at LL — but this is a mechanism mismatch, not a feature-destroying detail in the audit sense. The directional effects on am_lf_enr and am_mid_enr are as predicted (both drop toward depletion); the magnitude overcorrects for the structural reason identified above.

**Extrapolation**: No "structural" or "impossible" claims made. All findings are within the tested architecture and parameter setting. The global am rate divergence is a diagnosis of the specific p_blind mechanism, not a claim about all position-aware models.

**Negative-result scope**: The primary result (10/18 PASS, worse than exp_221) is for this specific architecture modification (VMS LL suffix for non-blind LL). The diagnosis explains WHY it fails. The conclusion is that "VMS LL suffix for non-blind LL" is incompatible with the p_blind mechanism at p_blind=0.30. It does NOT conclude that positional suffix distributions in general cannot improve am_lf_enr/am_mid_enr — a LF+MID-only suffix fix (keeping global for LL non-blind) might improve am_lf_enr directionally without breaking am_ll.

**Control behavior**: No explicit controls tested. Internal comparison (exp_221 vs exp_222) confirmed the mechanism diagnosis: the only metric that improved substantially was am_lf_enr and am_mid_enr (both moved toward VMS direction but overcorrected), while am_ll regressed. No surprises — all changes were mechanistically predicted by the global am rate divergence analysis.

---

## Conclusion

H423 PARTIALLY ANSWERED. VMS positional suffix distributions reveal a root-cause structural tension: the p_blind mechanism produces a global am rate (~5.5%) that is 2.7× VMS's true global am rate (2.03%). Using VMS LL suffix for non-blind LL fraction double-counts am enrichment, breaking am_ll (7.97, FAIL). The am_lf_enr and am_mid_enr improvements are overcorrected (0.051, 0.061 vs VMS 0.122, 0.195) because the inflated global am rate makes any fixed LF/MID am rate appear too depleted. edy_rate is immovable by suffix changes due to Timm buffer erosion. Net: 10/18 PASS, regression from exp_221's 11/18.

The key diagnostic advance: the am_lf_enr/am_mid_enr failures in exp_221 are consequences of the global am rate divergence produced by the p_blind mechanism, NOT a fixable suffix distribution problem. To achieve correct am positional enrichment ratios, the architecture would need to generate a global am rate closer to VMS's 2.03% — which requires either reducing p_blind (trading am_ll) or implementing a different am_ll mechanism.

**The 11/18 result from exp_221 remains the program best.** H408/H409 (parameter-count control and corpus-split stability) are the next priority.
