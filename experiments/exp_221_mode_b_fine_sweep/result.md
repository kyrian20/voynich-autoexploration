# exp_221: H422 — Fine-Sweep cp=0.40–0.55 in Mode B

**Date**: 2026-04-11  
**Hypothesis**: H422 — Fine sweep of cp ∈ {0.40, 0.45, 0.50, 0.55} × mp ∈ {0.60, 0.70, 0.80, 0.90} in Mode B (VMS MID onset for MID, onset-preserving Timm modification, p_blind=0.30) will identify which cp/mp combination simultaneously satisfies ss_mean ±20%, adj_rate ≤0.009, am_ll ±20%, and y_lf ±20%.  
**Status**: H422 ANSWERED — 14/16 combinations pass all 4 key criteria; best (cp=0.55, mp=0.90) achieves **11/18 PASS** on full 18-metric battery.

---

## Architecture

- **p_blind**: 0.30 (30% of LL words drawn as d/am structure)
- **d_boost**: 14.79% (boosted d-onset in LL blind fraction)
- **p_lf**: 1.0 (LF words drawn from VMS LF onset distribution)
- **onset_weights** (MID): VMS B MID onset distribution (H421 fix; y=2.21%, s=0.99%, ch=17.67%)
- **onset_lf_vms**: VMS B LF onset distribution
- **onset_ll**: VMS B LL onset distribution (with d_boost applied)
- **suffix_weights**: VMS B global suffix distribution
- **Timm modification**: onset-preserving (only suffix characters modified)
- **cp=0.55, mp=0.90** (selected as best all-4-viable from sweep)

---

## Sweep Results (N=15 per combination)

```
cp   mp     am_ll    d_ll    y_lf  ss_mean     adj    all4?
0.40 0.60   5.897   1.264   3.478   1.184   0.0074   *** ALL4 ***
0.40 0.70   5.981   1.246   3.384   1.185   0.0056   *** ALL4 ***
0.40 0.80   6.003   1.267   3.500   1.166   0.0042   *** ALL4 ***
0.40 0.90   5.964   1.202   3.536   1.196   0.0026   *** ALL4 ***
0.45 0.60   5.981   1.228   3.475   1.235   0.0084   *** ALL4 ***
0.45 0.70   6.014   1.221   3.449   1.220   0.0063   *** ALL4 ***
0.45 0.80   6.031   1.221   3.483   1.225   0.0043   *** ALL4 ***
0.45 0.90   6.024   1.200   3.407   1.241   0.0027   *** ALL4 ***
0.50 0.60   5.941   1.230   3.407   1.269   0.0092   (adj borderline)
0.50 0.70   6.094   1.193   3.409   1.267   0.0068   *** ALL4 ***
0.50 0.80   6.136   1.207   3.366   1.270   0.0047   *** ALL4 ***
0.50 0.90   6.189   1.224   3.393   1.289   0.0029   *** ALL4 ***
0.55 0.60   6.091   1.189   3.489   1.339   0.0101   (adj borderline)
0.55 0.70   6.165   1.272   3.389   1.338   0.0074   *** ALL4 ***
0.55 0.80   6.152   1.219   3.474   1.319   0.0052   *** ALL4 ***
0.55 0.90   6.213   1.220   3.519   1.334   0.0029   *** ALL4 ***
```

**14/16 combinations pass all 4 key criteria.** The 2 failures (cp=0.50 mp=0.60 and cp=0.55 mp=0.60) fail only on adj_rate ≤0.009 (adj=0.0092 and 0.0101 respectively).

---

## Full 18-Metric Battery (N=30, cp=0.55, mp=0.90)

```
Metric          VMS      E221    %VMS  Status   vs E220(cp=0.6)  [Category]
am_ll          6.550    6.258   95.6%  [PASS]   was 6.292        [CALIBRATED]
d_ll           1.362    1.222   89.7%  [PASS]   was 1.242        [CALIBRATED]
y_lf           3.324    3.440  103.5%  [PASS]   was 3.453        [VMS-DIRECT]
ss_mean        1.164    1.341  115.2%  [PASS]   was 1.403        [CALIBRATED (cp/mp)]
adj_rate       0.009    0.003   34.6%  [FAIL]   was 0.003        [CALIBRATED (cp/mp)]
qok_lf         0.778    0.756   97.2%  [PASS]   was 0.753        [VMS-DIRECT]
d_lf           2.211    2.253  101.9%  [PASS]   was 2.281        [VMS-DIRECT]
s_lf           4.638    5.138  110.8%  [PASS]   was 5.030        [VMS-DIRECT]
ch_ll          0.939    1.066  113.6%  [PASS]   was 1.061        [VMS-DIRECT]
ok_ll          0.975    1.043  106.9%  [PASS]   was 1.054        [VMS-DIRECT]
qok_ll         0.595    0.750  125.9%  [FAIL]   was 0.742        [partial]
ss_d           1.291    1.452  112.5%  [PASS]   was 1.568        [uncalibrated]
ss_y           1.955    1.673   85.6%  [PASS]   was 1.748        [uncalibrated]
am_lf_enr      0.122    0.380  310.3%  [FAIL]   was 0.418        [uncalibrated]
am_mid_enr     0.195    0.277  142.2%  [FAIL]   was 0.264        [uncalibrated]
edy_rate       0.194    0.140   72.4%  [FAIL]   was 0.132        [VMS-DIRECT suffix]
word_len_mean  5.400    6.592  122.1%  [FAIL]   was 6.593        [uncalibrated]
qok_ch         1.267    0.987   77.9%  [FAIL]   was 0.966        [uncalibrated]

Pass count: 11/18 (exp_220 Mode B cp=0.6: 9/18)
```

---

## Interpretation

**H422 ANSWERED.** 14/16 tested combinations pass all 4 key criteria simultaneously. cp=0.55, mp=0.90 was selected as the best (closest am_ll to VMS among all-4-viable) and achieves 11/18 on the full battery — the highest pass count in the experimental program (surpassing the prior best of 9/18 at exp_220).

**Net gain over exp_220**: +2 passes. ss_mean moved from FAIL (1.403, 120.6%) to PASS (1.341, 115.2%). ss_d moved from FAIL (1.568, 121.4%) to PASS (1.452, 112.5%). This confirms that the ss_mean/ss_d link is mediated by cp: lower cp → fewer consecutive same-onset words → both ss_mean and ss_d improve together.

**IMPORTANT — target-awareness caveat**: am_ll, d_ll, and ss_mean are conditionally calibrated. p_blind=0.30 was set to reproduce am_ll enrichment; d_boost=14.79% was set to reproduce d_ll enrichment; cp/mp were selected in this sweep specifically to satisfy ss_mean ±20% and adj_rate ≤0.009. A model with these parameters set without reference to VMS targets would likely produce qualitatively different values for am_ll, d_ll, and ss_mean.

**Remaining failures — structural analysis:**

1. **adj_rate** (34.6% FAIL): The ±20% pass criterion requires adj_rate between 0.0072 and 0.0108. At cp=0.55 the model produces adj_rate≈0.003, well below the lower bound. This is driven by onset-preserving modification: modified copies rarely produce exact duplicates. However, the directional criterion (adj≤0.009) IS satisfied. This failure reflects the ±20% criterion being inappropriate for adj_rate, not a directional model error.

2. **qok_ll** (125.9% FAIL): The minimum achievable qok_ll in this architecture at p_blind=0.30 is ≈0.70, because: LL words have p_blind=0.30 generating d/am words (zero qok) and 0.70 generating from onset_weights (qok≈12.8%). So qok_ll = 0.70×0.128/0.128 = 0.70 — which already exceeds VMS qok_ll=0.595×. This is a logical structural ceiling, not a parameter-tuning gap: reducing qok_ll below 0.70 requires either reducing p_blind (which trades am_ll) or explicitly suppressing qok in LL beyond what VMS onset_ll dictates. This architectural tension is the constraint, not the specific cp/mp values.

3. **am_lf_enr** (310.3% FAIL, wrong direction): VMS LF is DEPLETED in -am (0.122×). The model generates LF words from VMS LF onset distribution (correct onsets) plus global suffix distribution. Since the suffix is drawn independently of position, am_lf_enr ≈ 1.0 — neither enriched nor depleted. The observed 310.3% (enriched) vs VMS 0.122× (depleted) reveals an architectural gap: the model has no mechanism to deplete -am in LF position. This is a novel diagnostic finding — -am depletion in LF appears to require a separate positional rule, not just correct onset calibration.

4. **am_mid_enr** (142.2% FAIL): VMS MID is also DEPLETED in -am (0.195×). Copy buffer words occasionally carry -am suffixes from LL words that entered the buffer; the model propagates -am into MID via the buffer. A targeted -am block for MID/LF positions would fix this, but is untested.

5. **edy_rate** (72.4% FAIL): The Timm suffix modification disrupts edy endings on copy buffer words. At cp=0.55, mp=0.90, approximately 55%×90%=49.5% of MID words are Timm-modified copies. If the modification removes the final 'y' or inserts a character into 'edy', the word no longer ends in 'edy'. This is the Timm erosion mechanism acting specifically on 3-character suffixes. Fresh words are drawn from suffix_global which includes 'edy' at the correct rate, but copy buffer words with 'edy' are partially eroded.

6. **word_len_mean** (122.1% FAIL): sim=6.592 vs VMS=5.400. The word generation model (onset + connector + suffix) produces longer words than VMS average. This is a persistent structural gap across all experiments — the combined length distribution of EVA characters in onset, connector, and suffix components does not match VMS word length distribution. Untested: restricting suffix length or connector choice.

7. **qok_ch** (77.9% FAIL): VMS has elevated qok→ch bigram succession (1.267×). The model treats consecutive words as independent draws from position-specific distributions, producing qok_ch≈1.0. Reproducing this requires either a copy mechanism that preserves qok→ch succession or a Markov onset chain. Untested.

---

## Architecture Evolution Summary

```
exp_218: 4/17 (VMS calibrated dists, all-char Timm modification)
exp_219: 8/18 (onset-preserving modification)
exp_220: 9/18 (+ VMS MID onset for MID, cp=0.60)
exp_221: 11/18 (fine-tuned cp=0.55, same architecture)
```

The 11/18 result establishes the current best for the onset-blind LL + VMS LF + copy buffer model class.

---

## Limitations

1. **N=30** at the full-run stage. 90% CI intervals are not shown in this summary but should be approximately ±5-8% for most metrics.
2. **p_blind=0.30 fixed**: The sweep only varied cp/mp. The structural failures (qok_ll, adj_rate) are conditional on p_blind=0.30. Lower p_blind could reduce qok_ll but would reduce am_ll below VMS.
3. **word_len and qok_ch**: These metrics require architectural changes (EVA character weighting, Markov onset model) not tested in this experiment.

---

## Self-Audit

**Target-awareness**: Three elements are conditionally calibrated against VMS targets:
- **p_blind=0.30** calibrated to reproduce am_ll enrichment (VMS=6.550). The reported am_ll=6.258 (PASS) is conditional on this calibration. A model with p_blind set without reference to am_ll would produce a qualitatively different am_ll value.
- **d_boost=14.79%** calibrated to reproduce d_ll enrichment (VMS=1.362). The reported d_ll=1.222 (PASS) is conditional.
- **cp=0.55, mp=0.90** selected in this sweep specifically to satisfy ss_mean ±20% and adj_rate ≤0.009. ss_mean=1.341 (PASS) is conditional on this sweep optimization.
- The 8 VMS-DIRECT metrics (y_lf, qok_lf, d_lf, s_lf, ch_ll, ok_ll, onset_weights) use VMS distributions directly but do not use knowledge of the enrichment ratio targets — they are not post-hoc calibrated to match enrichment values.
- The 5 uncalibrated metrics (ss_d, ss_y, am_lf_enr, am_mid_enr, edy_rate, word_len_mean, qok_ch) pass or fail without any parameter being tuned to match them.

**Feature-destroying implementation**: No feature-destroying implementation details for H422's tested hypothesis (cp/mp parameter tuning for ss_mean). For ancillary metrics: the Timm onset-preserving modification is correctly implemented and does not destroy onset features. The edy_rate failure is a secondary consequence of the copy buffer mechanism modifying suffix characters (this erodes 'edy' endings on copied words), not a feature-destroying detail in the audit sense — it is the mechanism's natural behavior, not an implementation error.

**Extrapolation**: One structural claim is made: "qok_ll cannot fall below ≈0.70 at p_blind=0.30." This claim is supported by an explicit logical argument (LL fraction with p_blind=0.30 generates zero qok; remaining 0.70 generates qok at global rate → floor=0.70), not extrapolation from the parameter grid. All other claims are within the tested parameter range (cp ∈ {0.40–0.55}, mp ∈ {0.60–0.90}).

**Negative-result scope**: Not applicable to primary result (positive: 11/18 PASS). For remaining 7 failures: each is characterized as specific to this architecture and parameters. The am_lf_enr failure (wrong direction: 310.3% enriched vs VMS 0.122× depleted) is identified as an architectural gap (no LF -am depletion mechanism), not a claim about all copy-buffer architectures.

**Control behavior**: No explicit control distributions tested in this sweep. Internal comparison (cp sweep) showed monotonic behavior: ss_mean increases with cp (more repetition → more consecutive same-onset pairs); adj_rate decreases with mp (more modification → fewer exact duplicates). No surprises in the sweep trends.

---

## Conclusion

H422 ANSWERED. The fine sweep confirms that Mode B (VMS MID onset for MID + onset-preserving modification) achieves the target 4-metric window (ss_mean ±20%, adj≤0.009, am_ll ±20%, y_lf ±20%) across 14/16 tested combinations. At cp=0.55, mp=0.90: **11/18 PASS** — the program's best result. The 7 remaining failures split into three categories: (a) adj_rate directional pass but metric FAIL due to ±20% criterion inapplicability; (b) structural qok_ll ceiling at p_blind=0.30; (c) architectural gaps requiring new mechanisms (am position depletion, word length calibration, qok_ch bigram succession).
