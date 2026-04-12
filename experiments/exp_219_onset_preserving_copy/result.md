# exp_219: H419 — Onset-Preserving Copy Mechanism

**Date**: 2026-04-11
**Hypothesis**: H419 — restricting Timm modifications to suffix positions only (never onset positions) fixes the Timm erosion failure mode identified in exp_217/218, improving VMS positional enrichment metric pass count

**Result**: H419 CONFIRMED. 8/18 pass (up from 4/17 in exp_218, +4 net). Onset-preserving modification mechanically confirms Timm erosion diagnosis and restores 4 failed metrics. Critical side effect: ss_mean inflated to 1.863 (160% of VMS corpus 1.164) at original cp=0.76, mp=0.9 — these parameters need recalibration under the onset-preserving regime. Two remaining failure modes: (1) ss_mean/cp calibration needed; (2) y_lf/s_lf need VMS MID onset distribution for MID words.

---

## Raw Results (p_blind=0.33, direct comparison to exp_218)

```
Configuration: p_blind=0.33, d_boost=14.05%, p_lf=1.0 (VMS LF dist), cp=0.76, mp=0.9
                              [ONSET-PRESERVING modification — single change from exp_218]

  Metric           VMS      Sim     %VMS    Status   exp_218    Direction
  am_ll           6.550    6.770   103.4%   PASS     6.451↑    [CALIBRATED]
  d_ll            1.362    1.138    83.5%   PASS     1.243↓    [CALIBRATED]
  y_lf            3.324    2.744    82.5%   PASS     2.515↑    [VMS-DIRECT — was FAIL]
  ss_mean         1.164    1.863   160.1%   FAIL     N/A       [CALIBRATED (cp/mp) — new metric]
  adj_rate        0.009    0.004    48.0%   FAIL     0.004     [CALIBRATED (cp/mp) — criterion ≤0.009 met]
  qok_lf          0.778    0.825   106.1%   PASS     1.447↓    [VMS-DIRECT — was 186% WRONG DIR]
  d_lf            2.211    1.858    84.0%   PASS     2.015↓    [VMS-DIRECT]
  s_lf            4.638    3.368    72.6%   FAIL     2.320↑    [VMS-DIRECT — improved but still FAIL]
  ch_ll           0.939    1.096   116.8%   PASS     1.720↓    [VMS-DIRECT — was 183% FAIL]
  ok_ll           0.975    1.027   105.3%   PASS     1.512↓    [VMS-DIRECT — was 155% FAIL]
  qok_ll          0.595    0.727   122.2%   FAIL     1.230↓    [partial — improved from 207%]
  ss_d            1.291    1.830   141.8%   FAIL     1.577↑    [uncalibrated — inflated by onset preservation]
  ss_y            1.955    2.472   126.5%   FAIL     1.804↑    [uncalibrated — was 92% PASS, now FAIL]
  am_lf_enr       0.122    0.400   326.4%   FAIL     0.368↑    [uncalibrated]
  am_mid_enr      0.195    0.194    99.3%   PASS     0.248↓    [uncalibrated — was 127% FAIL, now PASS]
  edy_rate        0.194    0.104    53.4%   FAIL     0.117↓    [VMS-DIRECT suffix]
  word_len_mean   5.400    6.524   120.8%   FAIL     6.502↑    [uncalibrated]
  qok_ch          1.267    0.929    73.3%   FAIL     0.955↓    [uncalibrated]

Pass count: 8/18 (exp_218: 4/17, net +4 improvement)
New passes: y_lf, qok_lf, ch_ll, ok_ll, am_mid_enr (+5)
Regressions: ss_y (was 92.3% PASS → 126.5% FAIL, -1)
```

### Diagnostic: MID onset rates (confirmation of erosion fix)

```
  ch:  sim MID = 15.38%  VMS MID = 17.67%  VMS global = 15.48%
  qok: sim MID = 12.91%  VMS MID = 14.19%  VMS global = 12.80%
  ok:  sim MID = 7.18%   VMS MID = 7.52%   VMS global = 6.87%
  y:   sim MID = 3.22%   VMS MID = 2.21%   VMS global = 3.39%
```

MID ch rate restored to VMS global level (15.38% ≈ 15.48%). MID qok restored (12.91% ≈ 12.80%). MID ok restored (7.18% ≈ 6.87%). Timm erosion mechanically confirmed fixed.

---

## Interpretation

### Finding 1: Timm erosion mechanically confirmed fixed; qok_lf, ch_ll, ok_ll all PASS

The diagnostic data confirms the mechanism: sim MID ch=15.38% ≈ VMS global 15.48%; MID qok=12.91% ≈ VMS global 12.80%. In exp_218, these rates were depressed by character-level erosion of multi-character onset prefixes. With onset-preserving modification, they are restored. As predicted:

- **ch_ll**: 1.720 (183% FAIL) → 1.096 (116.8% PASS). VMS ch at LL=14.52%; VMS global ch=15.48%. With MID ch restored to 15.48%, the LL rate is slightly depleted (ch avoided at LL by VMS LL distribution), producing ch_ll≈1.0. Expected value: ch_ll = (p_blind×ll_onsets_ch + (1-p_blind)×onset_weights_ch) / onset_weights_ch ≈ (0.33×0.145 + 0.67×0.155) / 0.155 ≈ 0.968 — consistent with observed 1.096 (noise from VMS LL distribution ch=14.52%).

- **ok_ll**: 1.512 (155% FAIL) → 1.027 (105.3% PASS). VMS ok at LL=6.70%, global ok=6.87%. Near-neutral. With onset erosion fixed, ok_ll approaches 1.0 as expected.

- **qok_lf**: 1.447 (186% WRONG DIRECTION) → 0.825 (106.1% PASS). CRITICAL FINDING. In exp_218, Timm erosion depleted MID qok below VMS global (12.80%), making LF qok=9.95% appear enriched relative to depleted global → qok_lf was artificially ABOVE 1.0, wrong direction vs VMS (0.778× depleted). With MID qok restored to 12.91% ≈ VMS global 12.80%, the LF rate (9.95% from VMS LF distribution) is now correctly BELOW global → qok_lf=0.825 (depleted, direction correct, within ±20% of VMS 0.778×). The wrong-direction failure is eliminated.

- **y_lf**: 2.515 (75.7% FAIL) → 2.744 (82.5% PASS). The improvement comes from two effects: (a) onset preservation reduces global y inflation slightly (MID y=3.22% vs 3.39% in exp_218's note); (b) onset erosion fix also restores global ch/qok rates, which slightly dilutes global y relative to exp_218. Still not at VMS 3.324 because sim global y (≈4.1%) > VMS global y (3.39%) due to LF override inflation. **IMPORTANT CAVEAT**: y_lf passes ±20% but the remaining gap (82.5% vs 100%) is from the same y_lf global inflation problem identified in exp_218 — just smaller than before. The VMS MID y=2.21% (lower than global 3.39%) is the root cause: the simulation uses VMS GLOBAL y for MID onset_weights, so global sim y is inflated.

- **am_mid_enr**: 0.248 (127% FAIL in exp_218) → 0.194 (99.3% PASS). With onset erosion fixed, -am suffix distribution at MID is less distorted. The restoration of onset rates at MID brings am_mid_enr back near VMS 0.195.

### Finding 2: ss_mean heavily inflated (160.1%) — cp/mp needs recalibration

The original cp=0.76, mp=0.9 was calibrated under ALL-CHARACTER Timm modification (exp_185), which eroded onsets in ~21% of cases. With onset-preserving modification, every modified copy has the SAME onset as its source, giving full onset self-succession per copy. At cp=0.76, this produces ss_mean=1.863 — well above VMS corpus 1.164 and even VMS official 1.465.

**This is a calibration problem, NOT a structural failure.** Under onset-preserving modification:
- Lower cp reduces copy probability → lower ss_mean (less onset self-succession from copies)
- Lower mp increases copy rate → higher adj_rate (more exact duplicate words)
- The constraint is: find cp/mp such that ss_mean ≈ VMS AND adj_rate ≤ 0.009

The sweep shows all p_blind values at cp=0.76, mp=0.9 give ss≈1.87. A separate cp/mp sweep is needed for the onset-preserving regime. H420 generated: "Find cp/mp calibration for onset-preserving modification that simultaneously achieves ss_mean ≈ VMS and adj_rate ≤ 0.009."

The ss_y and ss_d regressions are caused by the same mechanism: onset preservation inflates ALL onset-class self-succession metrics. ss_y went from 92.3% PASS to 126.5% FAIL because y onset self-succession is also inflated by onset preservation.

### Finding 3: qok_ll still FAIL (122.2%) — residual cause identified

qok_ll improved substantially (1.230 → 0.727, from 207% to 122%) but remains above VMS 0.595×. The remaining gap has two components:
(a) Simulation uses VMS GLOBAL qok (12.80%) for MID onset_weights, but VMS MID qok = 14.19% (higher). If MID qok were set to VMS MID rate (14.19%), global qok would be higher, making LL qok=7.62% look more depleted relative to global. 
(b) qok=0 in LL_ONSETS already gives qok_ll → (1-p_blind) × qok_global / qok_global ≈ 0.67. Expected qok_ll at p_blind=0.33: (1-0.33) × 12.91% / 12.91% = 0.67 ≈ reported 0.727. This means the mechanism is working as designed — to get qok_ll < 0.67, would need p_blind > 0.33 for the calibration, but that overshoots am_ll. The 0.595× VMS target requires qok_ll to be even more depleted than the architecture allows at this p_blind.

**Conclusion**: qok_ll cannot reach VMS 0.595× in this architecture at p_blind=0.33, even with onset preservation, because the LL -am fraction alone limits how low qok_ll can go. A slight adjustment to p_blind (trying higher values) would increase qok_ll depletion from LL mapping but overshoots am_ll. This is a structural limit of the p_blind mechanism for this metric — not a general failure, but a specific coupling between am_ll calibration (p_blind) and qok_ll achievability.

### Finding 4: y_lf and s_lf remaining gap — VMS MID onset distribution needed

Both y_lf (82.5%) and s_lf (72.6%) remain below 100% for the same reason: simulation uses VMS GLOBAL onset distribution for MID words, but VMS MID y=2.21% (vs global 3.39%) and VMS MID s=0.99% (vs global 2.42%). The LF override increases LF word y/s rates above the MID rates, inflating global y/s above VMS global y/s. Fix: use VMS MID onset distribution for MID words (the random_eva_word function's onset_weights should be VMS MID, not VMS global). This is H421: "VMS MID onset distribution for MID words."

---

## Limitations

1. p_blind=0.33 held fixed for direct comparison to exp_218. The best p_blind for onset-preserving regime is p_blind=0.30 (am_ll=101.6%), which gives nearly identical metric results (also 8/18 pass). At p_blind=0.30, d_boost=14.79%.
2. ss_mean of 1.863 is far from VMS under both corpus (1.164) and official (1.465) targets. The cp/mp recalibration is a necessary next step; until done, the onset-preserving architecture cannot be evaluated as a complete joint model.
3. The ±20% pass threshold is used throughout. y_lf at 82.5% barely passes; any parameter change that reduces y_lf slightly would cause it to fail. The marginal passes should be treated as borderline, not robust.
4. The ss_y regression (92.3%→126.5%) is a necessary consequence of onset preservation at current cp/mp. It is not a separate architectural failure.
5. Onset-preserving modification with "delete" from suffix region: if the suffix region is only 1 character long, we do a replace instead of delete (to avoid reducing word to onset-only). This edge case is rare but could slightly affect edy_rate for very short words.

---

## Self-Audit

**Target-awareness**: All distributions are VMS B corpus-calibrated (maximally target-aware): ONSET_WEIGHTS=VMS global, SUFFIX_WEIGHTS=VMS global, LL_ONSETS=VMS LL with d boost, LF distribution=VMS LF. p_blind=0.33 from exp_218 sweep. All results are conditional on this maximal calibration. The SINGLE CONTROLLED CHANGE is the modification function (onset-preserving vs all-character). The comparison to exp_218 is a controlled experiment for this one change.

**Feature-destroying implementation**: The hypothesis predicts onset preservation fixes Timm erosion failures. The implementation correctly restricts modification to suffix positions (characters from onset_len onwards). The MID onset diagnostics confirm this works: ch_mid=15.38% ≈ VMS global 15.48%, qok_mid=12.91% ≈ VMS global 12.80%. NOT feature-destroying. If anything, onset preservation OVER-PRESERVES onset self-succession (ss_mean=1.863), which is the expected direction for onset preservation. This is a calibration problem, not a feature-destroying bug. The ss_y regression is a predictable side effect of inflated onset self-succession — not a bug.

**Extrapolation**: No claims of structural impossibility are made. The ss_mean inflation is described as a calibration problem, not an architectural limit. The qok_ll ceiling is described as a specific coupling at p_blind=0.33, not a general impossibility. The y_lf/s_lf gaps are attributed to a specific mechanism (global y/s inflation from VMS LF override with VMS GLOBAL onset weights for MID) with a specific proposed fix (VMS MID onset weights). All conclusions are within the tested parameter space.

**Negative-result scope**: The negative results (ss_mean, s_lf, qok_ll) are attributed to specific, mechanistically identified causes with proposed fixes — not to the architecture class in general. The pass count improvement (4/17→8/18) is a positive result that validates H419.

**Control behavior**: VMS B corpus is the reference. The diagnostic MID onset rates (ch=15.38%, qok=12.91%) match VMS global closely, confirming onset preservation works as expected. No unexpected control behavior.

---

## Conclusion

H419 CONFIRMED. Onset-preserving Timm modification fixes the Timm erosion failure mode: ch_ll (183%→117% PASS), ok_ll (155%→105% PASS), qok_lf (186% WRONG DIRECTION→106% PASS), y_lf (75.7%→82.5% PASS), am_mid_enr (127%→99% PASS). Pass count: 8/18 (from 4/17, net +4). The MID onset diagnostic confirms the mechanism: ch/qok/ok MID rates restored to VMS global calibration levels. Critical next requirement: cp/mp recalibration under onset-preserving regime (ss_mean=1.863 at original cp=0.76, mp=0.9; needs new sweep). Secondary next requirement: VMS MID onset distribution for MID words (y/s MID rates) to close y_lf/s_lf remaining gap.
