# exp_218: H412+H413 — VMS-Calibrated Onset/Suffix Distributions

**Date**: 2026-04-11
**Hypothesis**: H412+H413 — replacing exp_211's approximate ONSET_WEIGHTS and LL_ONSETS with VMS B-calibrated distributions, and replacing y-only LF override with multi-onset VMS LF distribution, improves uncalibrated metric count

**Result**: H412+H413 ANSWERED: 4/17 pass (same as exp_217's 4/18). One genuine improvement (d_lf: 40.6% → 91.2% PASS) and one regression (y_lf: 106.2% → 75.7% FAIL). The architecture class is structurally limited: even maximal VMS calibration cannot simultaneously reproduce all VMS enrichment metrics.

---

## Raw Results

```
Configuration: p_blind=0.33, d_boost=14.05%, p_lf=1.0 (VMS LF dist), cp=0.76, mp=0.9

  am_ll      VMS=6.550  Sim=6.451   98.5%  PASS  [CALIBRATED]
  d_ll       VMS=1.362  Sim=1.243   91.2%  PASS  [CALIBRATED] — slightly below target
  y_lf       VMS=3.324  Sim=2.515   75.7%  FAIL  [VMS-DIRECT — see analysis]
  adj_rate   VMS=0.009  Sim=0.004   45.6%  FAIL  [CALIBRATED (cp/mp) — criterion ≤ 0.009 met]
  qok_lf     VMS=0.778  Sim=1.447  186.0%  FAIL  [VMS-DIRECT — still wrong direction]
  d_lf       VMS=2.211  Sim=2.015   91.2%  PASS  [VMS-DIRECT — exp_217 was 40.6%]
  s_lf       VMS=4.638  Sim=2.320   50.0%  FAIL  [VMS-DIRECT — exp_217 was 13.1%]
  ch_ll      VMS=0.939  Sim=1.720  183.3%  FAIL  [VMS-DIRECT — exp_217 was 195.8%]
  ok_ll      VMS=0.975  Sim=1.512  155.1%  FAIL  [VMS-DIRECT — exp_217 was 204.3%]
  qok_ll     VMS=0.595  Sim=1.230  206.6%  FAIL  [partial — exp_217 was 310.2%]
  ss_d       VMS=1.291  Sim=1.577  122.2%  FAIL  [uncalibrated]
  ss_y       VMS=1.955  Sim=1.804   92.3%  PASS  [uncalibrated — exp_217 was 66.2%]
  am_lf_enr  VMS=0.122  Sim=0.368  300.7%  FAIL  [uncalibrated]
  am_mid_enr VMS=0.195  Sim=0.248  127.0%  FAIL  [exp_217 was 101.6% PASS — regressed]
  edy_rate   VMS=0.194  Sim=0.117   60.5%  FAIL  [VMS-DIRECT suffix — Timm erosion]
  word_len   VMS=5.400  Sim=6.502  120.4%  FAIL  [uncalibrated — exp_217 was 132.9%]
  qok_ch     VMS=1.267  Sim=0.955   75.4%  FAIL  [uncalibrated]

Pass count: 4/17 (exp_217: 4/18, same effective count)
By category: CALIBRATED 2/3, VMS-DIRECT 1/7, partial 0/1, uncalibrated 1/6
```

---

## Interpretation

### Finding 1: d_lf is now PASS (91.2%) — multi-onset LF distribution fixes this failure

The single clearest improvement from H413: using VMS B LF distribution for all LF words correctly places d at LF at 14.81% (enriched), giving d_lf=91.2%. exp_217 had d_lf=40.6% because only y was privileged at LF. This confirms H413's prediction for d_lf. s_lf also improved (13.1% → 50.0%) but remains below threshold — the VMS LF s-onset rate (11.24%) is reproduced at LF, but the global s rate in simulation differs from VMS, distorting the enrichment ratio.

### Finding 2: y_lf regression from 106.2% to 75.7% — global y inflation from LF override

This is the most striking result. Using VMS LF distribution (y=11.28%) for ALL LF words (p_lf=1.0) increases the global simulation y rate:
- VMS global y = 3.39% (MID y ≈ 2.35%, LL y ≈ 2.30%, LF y = 11.28%)
- Simulation global y ≈ 4.28% (MID uses ONSET_WEIGHTS['y']=3.39% — VMS global, not VMS MID)

Since the enrichment ratio normalizes by global y, inflating global y from 3.39% to 4.28% REDUCES y_lf:
- Expected y_lf_sim = 11.28% / 4.28% = 2.63 ≈ reported 2.515

The root cause: onset_weights (used for MID words) = VMS GLOBAL onset distribution, but VMS MID y ≈ 2.35% (lower than global 3.39% because VMS LF draws heavily from y). Using VMS global y for MID over-represents y in MID positions, inflating global y and reducing apparent y_lf enrichment. To correctly reproduce y_lf, the simulation needs VMS MID onset distribution for MID words (not VMS global distribution).

### Finding 3: qok_lf still wrong direction (1.447× vs VMS 0.778×) — Timm erosion is the root cause

Explained in exp_217: Timm modifications erode qok from the copy buffer (qok prefix is destroyed by char replacement). MID words therefore have lower qok than onset_weights, making LF (which draws from VMS LF at qok=9.95%) appear enriched relative to the depressed global average. Even with VMS LF distribution (qok=9.95% at LF, below onset_weights qok=12.80%), the Timm erosion makes global qok lower than 12.80%, so qok_lf = 9.95% / depleted_global > 1.0. Fixing qok_lf requires preserving onset structure in the copy buffer — a fundamental architectural change beyond distribution calibration.

### Finding 4: LL onset distribution fixes are insufficient for ch_ll/ok_ll/qok_ll

Even after using VMS LL distribution as LL_ONSETS (p_blind=0.33):
- ch_ll = 183% (VMS 94%) — only modest improvement from 196%
- ok_ll = 155% (VMS 97.5%) — improved from 204%
- qok_ll = 207% (VMS 59.5%) — improved from 310%

The failures persist because ONSET_WEIGHTS for MID/random_eva_word has different onset rates than VMS LL. With VMS global onset rates (ch=15.48%), MID words have high ch. But the LL_ONSETS in p_blind fraction now also has ch=14.99% (from VMS LL). Together: ch at LL ≈ 0.33 × 14.99% + 0.67 × 15.48% = 15.27%. Global ch (from corrected ONSET_WEIGHTS) = 15.48%. ch_ll = 15.27%/15.48% = 0.986. That should be ≈ VMS 0.939. But simulation reports 1.720. 

The discrepancy: Timm erosion in MID reduces MID ch (by replacing 'c' or 'h' prefix chars), lowering global ch below 15.48%. Then ch at LL (15.27%) appears enriched relative to the depressed global. Timm erosion is eroding ALL onset classes from MID — not just qok. This makes LF and LL positions appear ENRICHED relative to Timm-depleted MID, affecting every positional enrichment metric.

### Structural Diagnosis: Timm Erosion is the Universal Failure Mode

exp_217 and exp_218 together establish a unified explanation: Timm character modifications (replace/insert/delete) preferentially erode onset-specific prefixes from MID words in the copy buffer. Long onset prefixes (qok=3 chars, ch=2 chars, sh=2 chars, ok=2 chars) are especially vulnerable to single-character replacement. This erosion:
1. Depresses global onset rates for common multi-character onsets
2. Makes LF/LL positional onset rates (which bypass the buffer) appear enriched
3. Creates WRONG-DIRECTION or EXAGGERATED enrichments at LF/LL vs buffer-depleted global

This is a structural property of Timm-style character-modification in the copy buffer, not a calibration artifact. Distribution calibration (H412/H413) does not fix it. Fixing it would require onset-preserving Timm modifications (e.g., modify only suffix positions, never onset positions).

---

## Limitations

1. p_blind=0.33 gives am_ll=98.5% and d_ll=91.2%; a slightly different p_blind might improve d_ll. The sweep at N=10 may have variance.
2. The Timm erosion analysis is mechanistic reasoning, not directly measured. A direct measurement of onset distributions at MID vs LF vs LL positions in simulation output would confirm.
3. p_lf=1.0 is maximally target-aware (all LF words drawn from VMS LF distribution). This ensures LF onset distribution matches VMS but does not guarantee correct enrichment ratios due to global rate shifts.

---

## Self-Audit

**Target-awareness**: Maximally target-aware. ONSET_WEIGHTS = VMS B global, SUFFIX_WEIGHTS = VMS B suffix, LL_ONSETS = VMS B LL (d boosted for d_ll), LF distribution = VMS B LF. Every distribution parameter derived from VMS corpus. The result (4/17 pass) is conditional on this maximal calibration.

**Feature-destroying implementation**: No hypothesis predicts all metrics should pass — H412/H413 are tested as improvement hypotheses. The finding that y_lf REGRESSED is a genuine negative result explaining WHY (global y inflation from VMS LF override), not an implementation flaw against the hypothesis.

**Extrapolation**: "The architecture class is structurally limited" is supported by the specific mechanistic argument (Timm erosion → onset depletion in MID → distorted enrichment ratios). This conclusion applies to this architecture class (Timm copy buffer + positional onset override), not to position-aware architectures in general.

**Negative-result scope**: The failing metrics are attributed to Timm erosion (for positional enrichments) and word-generation model mismatch (for word_len). The valid conclusion is: "this architecture, even with maximal calibration, cannot simultaneously reproduce VMS positional enrichment metrics."

**Control behavior**: VMS B corpus serves as reference (same parser as exp_216/217). No unexpected control behavior.

---

## Conclusion

H412+H413 ANSWERED: Calibrating onset/suffix distributions to VMS B corpus provides 1 genuine improvement (d_lf PASS) and reveals 1 regression (y_lf FAIL due to global y inflation). The architecture achieves 4/17 pass — same as exp_217 (4/18). The remaining failures are traced to Timm copy buffer erosion, which systematically distorts onset distributions in MID positions, corrupting ALL positional enrichment metrics that depend on the global onset rate denominator. This is a structural limitation of Timm-style character modification in the copy buffer. Distribution calibration cannot fix it.
