# exp_232: H432 — LF/MID -am Suffix Suppression

**Date**: 2026-04-11  
**Hypothesis**: H432 — Does suppressing -am in LF and MID fresh-word suffix distributions fix am_lf_enr (332.7%→PASS) and am_mid_enr (144.0%→PASS) without regressing 15 currently passing metrics?  
**Status**: H432 NEGATIVE — uniform suppression overshoots both targets below VMS, regresses ss_d, net **14/18 FAIL (−1 from exp_231)**. Root cause: copy buffer modification erodes -am further, causing MID am rate to collapse well below LF am rate. GENERATES H433 (differential suppression: r_lf ≠ r_mid).

---

## Design

Apply a suppression factor r to the -am weight in the fresh LF and fresh MID suffix distributions. All other parameters identical to exp_231 (cp=0.55, mp=0.90, p_blind=0.30, p_lf=1.0, p_qokch=0.12, p_stutter=0.009, d_boost=9.13%, VMS LL onset for non-blind LL).

`suffix_suppressed[am] = r × suffix_global[am]`, other weights renormalized to sum to 1.

Used for: (a) fresh LF words via `cipher_lf_vms`, (b) fresh MID words via `random_eva_word`, (c) `timm_modify` fresh-fallback for MID. LL non-blind fraction still uses global suffix unchanged.

Sweep r ∈ {0.05, 0.08, 0.10, 0.15, 0.20} at N=5 each. Best r determined by: smallest r that still gives am_lf_enr ≤ 1.20 × VMS (if any), else r minimizing |am_lf_enr − VMS|. Full N=30 at best r=0.20.

---

## Sweep Results

```
r     am_lf_enr  %VMS  P?  am_mid_enr  %VMS  P?   am_ll    %VMS  P?  ss_mean  P?
0.05      0.028  22.7%  F       0.033  16.9%  F    8.181  124.9%  F    1.346   P
0.08      0.039  31.8%  F       0.051  26.2%  F    8.002  122.2%  F    1.389   P
0.10      0.053  43.3%  F       0.055  28.2%  F    8.046  122.8%  F    1.376   P
0.15      0.076  62.2%  F       0.065  33.5%  F    7.955  121.5%  F    1.371   P
0.20      0.086  70.2%  F       0.070  35.7%  F    7.871  120.2%  F    1.341   P
```

**No r value achieves am_lf_enr ≤ 0.147 (pass zone upper bound)**. At r=0.20, am_lf_enr = 0.086 (70.2% of VMS, below pass zone lower bound 0.098). All r values overshoot: am_lf_enr falls BELOW VMS rather than reaching it. am_mid_enr also collapses below VMS across all tested r.

---

## Full Run Results (N=30, r=0.20)

```
Metric           VMS    E232       %  P?    E231    delta
am_ll           6.550   7.786  118.9% P    6.203   +1.583  ← increases as global am drops
d_ll            1.362   1.421  104.3% P    1.420   +0.001
y_lf            3.324   3.349  100.8% P    3.493   -0.144
ss_mean         1.164   1.363  117.1% P    1.354   +0.009
adj_rate        0.009   0.010  109.8% P    0.010   -0.000
qok_lf          0.778   0.802  103.1% P    0.771   +0.031
d_lf            2.211   2.310  104.5% P    2.265   +0.045
s_lf            4.638   4.841  104.4% P    4.851   -0.010
ch_ll           0.939   0.851   90.7% P    0.858   -0.007
ok_ll           0.975   0.998  102.4% P    0.988   +0.010
qok_ll          0.595   0.598  100.5% P    0.593   +0.005
ss_d            1.291   1.562  121.0% F    1.505   +0.057  ← NEW FAILURE
ss_y            1.955   1.853   94.8% P    1.858   -0.005
am_lf_enr       0.122   0.096   78.7% F    0.407   -0.311  ← overshoots below VMS
am_mid_enr      0.195   0.084   42.9% F    0.281   -0.197  ← collapsed below VMS
edy_rate        0.194   0.191   98.4% P    0.187   +0.004
word_len_mean   5.400   6.637  122.9% F    6.628   +0.009
qok_ch          1.267   1.203   95.0% P    1.189   +0.014

Pass count:  E232=14/18  |  E231 (baseline)=15/18
```

**-am rate diagnostics (r=0.20)**:
```
Global am = 4.03%  (VMS global = 2.03%)
LF am     = 0.388% (VMS LF ≈ 0.249%)
MID am    = 0.338%
LL am     = 31.39%
Derived am_lf_enr = 0.096  (VMS = 0.122)
Derived am_mid_enr = 0.084 (VMS = 0.195)
ss_mean safety: 1.363 (upper bound = 1.397, margin = 0.033)
```

---

## Interpretation

### Finding 1: Uniform suppression overshoots — am_lf_enr and am_mid_enr both fall BELOW VMS

At every tested r value, am_lf_enr falls below VMS 0.122 (to 0.028-0.086). The suppression is too effective. At r=0.20:
- LF am = 0.388% vs VMS LF 0.249% — sim LF am still too high for VMS, but the global am has also dropped significantly
- am_lf_enr = LF_am / global_am = 0.388 / 4.03 = 0.096 — BELOW pass zone lower bound (0.098)

Similarly, am_mid_enr = 0.084 (42.9%) — grossly below VMS 0.195.

**Root cause**: The suppression propagates through the copy buffer. Fresh MID words are suppressed to r × global_am. Modified buffer copies lose -am via modification erosion. The equilibrium MID am rate is much lower than just r × global_am_fresh. Specifically, at r=0.20, fresh MID am = 0.406% but equilibrium MID am = 0.338% (16% lower from buffer erosion). The buffer erosion compounds the suppression.

### Finding 2: am_lf_enr and am_mid_enr overshoot in opposite ways under uniform r

At r=0.20: am_lf_enr = 0.096 (just below pass zone [0.098, 0.146]), am_mid_enr = 0.084 (far below pass zone [0.156, 0.234]). The two metrics cannot simultaneously be in their pass zones under uniform r:
- To fix am_lf_enr: need am_lf_enr ≥ 0.098, meaning less suppression of LF (larger r_lf)
- But at larger r, MID also gets less suppressed, and am_mid_enr would still remain above its pass zone upper bound (0.234) since exp_231 gives 0.281

This means the two metrics require different suppression factors: am_lf_enr needs a specific suppression of LF, while am_mid_enr needs a specific suppression of MID. Uniform r cannot satisfy both simultaneously.

### Finding 3: ss_d regresses to FAIL (1.505→1.562, 121.0%)

ss_d = 1.562 vs VMS 1.291, pass zone [1.033, 1.549]. This is at 121.0% — just above the upper bound. The 0.057 increase from exp_231 is consistent with random variance (ss_d has high variance across simulations), but represents a genuine regression. Mechanism: when MID am is suppressed, the fresh word pool changes composition, which alters buffer word frequencies, which slightly affects d-onset self-succession through buffer copy patterns. This is a weak indirect mechanism. The failure is borderline.

### Finding 4: am_ll increases as global am decreases (6.203→7.786)

Suppressing LF and MID -am reduces global am from ~5.5% to 4.03%. With LL am unchanged (31.39%), am_ll = 31.39/4.03 = 7.79 (118.9%). Still within pass zone [5.24, 7.86] but increased significantly. This confirms that global am reduction does increase am_ll — an important constraint for calibrating any fix.

### Finding 5: Root cause diagnosis — why uniform suppression fails

The fundamental problem: at r=1.0 (exp_231), LF_am ≈ 2.03% and MID_am ≈ 1.55% (from buffer erosion). With global_am ≈ 5.5%:
- am_lf_enr = 2.03/5.5 = 0.369 (not matching observed 0.407, but close — discrepancy from buffer MID contribution to global)
- am_mid_enr = 1.55/5.5 = 0.282 (matches observed 0.281) ✓

For am_lf_enr to reach pass zone (≤ 0.146) while am_mid_enr reaches pass zone (≤ 0.234):
- Need LF_am / global_am ≤ 0.146
- Need MID_am / global_am ≤ 0.234
- But both share the same global_am denominator

If r_lf=0.33 (LF only, MID unchanged): LF_am = 0.67%, MID_am = 1.55%, global_am ≈ 5.29% (LF contribution reduced by 0.129 × (2.03-0.67)% = 0.18%). Then am_lf_enr = 0.67/5.29 = 0.127 (PASS) but am_mid_enr = 1.55/5.29 = 0.293 (FAIL — above upper bound 0.234).

For am_mid_enr to also pass, need to suppress MID am. If r_lf=0.33 and r_mid=0.70: fresh MID am = 1.42%, buffer equilibrium MID am ≈ ~1.0% (estimated from proportional reduction), net MID am ≈ 1.05%. New global_am ≈ 0.129 × 0.67 + 0.742 × 1.05 + 0.129 × 31.39 = 0.086 + 0.779 + 4.049 = 4.91%. Then: am_lf_enr = 0.67/4.91 = 0.136 (PASS), am_mid_enr = 1.05/4.91 = 0.214 (PASS), am_ll = 31.39/4.91 = 6.39 (97.6% — PASS). This is the theoretical basis for H433.

---

## Limitations

1. **N=5 for sweep**: Small sample per r value; sweep results are rough estimates. Full run at r=0.20 confirms the sweep trend (am_lf_enr=0.086 sweep vs 0.096 full; both below pass zone).
2. **ss_d regression**: At 121.0%, just above the 120% upper bound. May be statistical noise (single-run variance) but represents a genuine regression risk.
3. **Buffer equilibration modeling**: The exact relationship between r and equilibrium MID am rate is complex. The suppression propagates through the buffer in a way that simple linear scaling cannot predict.

---

## Self-Audit

**Target-awareness**: r=0.20 was chosen to minimize distance to VMS am_lf_enr target. This is target-calibrated — the result is conditional on this choice. The mechanism direction is architecturally motivated (VMS grammar: -am avoided at LF/MID), but the specific r value is target-calibrated.

**Feature-destroying implementation**: None. The mechanism suppresses -am in fresh suffix distributions, which does not destroy any onset-class or bigram feature.

**Extrapolation**: The claim that "uniform r cannot fix both metrics" is supported by the analytical argument in Finding 5. The argument shows that for am_mid_enr to pass (≤ 0.234), MID_am must be ≤ 0.234 × global_am. With LF-only suppression giving global_am ≈ 5.29%, MID_am ≤ 1.237% is needed, but exp_231 shows MID_am ≈ 1.55% (unchanged from buffer equilibration). This gap requires independent MID suppression — i.e., separate r_lf and r_mid parameters. The tested grid (uniform r for both) was the wrong parameter space.

**Negative-result scope**: H432 (uniform suppression) fails. This does NOT mean all -am suppression mechanisms fail. Specifically, H433 (differential suppression with r_lf ≠ r_mid) is untested and analytically motivated by the Finding 5 derivation.

**Control behavior**: The diagnostic confirms the mechanism behaves as expected: at r=0.20, LF_am=0.388% (≈ 0.2 × 2.03% = 0.406%, close ✓). Global am dropped from ~5.5% to 4.03% as expected. The discrepancy is from the buffer-erosion MID effect compounding with the fresh suppression.

---

## Conclusion

H432 NEGATIVE. Uniform -am suppression (same r for LF and MID) overshoots both targets below VMS and introduces a new ss_d failure. Net: 14/18 (−1 from exp_231). The root cause: copy buffer modification erosion causes MID am rate to drop further than LF am rate, making joint calibration impossible with a single suppression factor.

**Generates H433**: Differential -am suppression with separate factors r_lf (for LF) and r_mid (for MID fresh words). Analytical prediction (Finding 5): r_lf ≈ 0.33, r_mid ≈ 0.70 should give am_lf_enr ≈ 0.136 (PASS), am_mid_enr ≈ 0.214 (PASS), am_ll ≈ 6.39 (PASS). This would give 17/18 if ss_d doesn't regress. To be confirmed empirically.

**Structural note**: The three remaining failures (am_lf_enr, am_mid_enr, word_len_mean) require different levels of architectural intervention. The -am suppression approach continues to be the most tractable path for am_lf_enr and am_mid_enr.
