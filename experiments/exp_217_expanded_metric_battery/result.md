# exp_217: H410 — Expanded Metric Battery for exp_211 Best Configuration

**Date**: 2026-04-11
**Hypothesis**: H410 — does exp_211's best config reproduce VMS metrics it was NOT calibrated to?

**Result**: H410 ANSWERED (NEGATIVE): 1/13 uncalibrated metrics pass; 12/13 fail, with systematic architectural failures. Additionally, 2/5 calibrated metrics fail when evaluated against corpus-computed VMS values (discrepancy between "official" targets and corpus parser output).

---

## Raw Results

```
Calibrated metrics (3/5 pass vs corpus-computed VMS):
  am_ll      VMS=6.550  Sim=6.801  103.8%  PASS
  d_ll       VMS=1.362  Sim=1.481  108.7%  PASS
  y_lf       VMS=3.324  Sim=3.530  106.2%  PASS
  ss_mean    VMS=1.164  Sim=1.442  124.0%  FAIL (calibrated to target 1.465, not corpus 1.164)
  adj_rate   VMS=0.009  Sim=0.004   44.7%  FAIL (calibrated as ≤ 0.009; far below VMS)

Uncalibrated metrics (1/13 pass):
  qok_lf     VMS=0.778  Sim=1.309  168.4%  FAIL (WRONG DIRECTION — enriched vs depleted)
  d_lf       VMS=2.211  Sim=0.898   40.6%  FAIL (underproduces — architecture doesn't privilege d at LF)
  s_lf       VMS=4.638  Sim=0.606   13.1%  FAIL (severely underproduces)
  ch_ll      VMS=0.939  Sim=1.838  195.8%  FAIL (LL_ONSETS enriches ch, VMS ch near-neutral)
  ok_ll      VMS=0.975  Sim=1.992  204.3%  FAIL (LL_ONSETS enriches ok, VMS ok near-neutral)
  qok_ll     VMS=0.595  Sim=1.846  310.2%  FAIL (LL_ONSETS enriches qok, VMS qok depleted)
  ss_d       VMS=1.291  Sim=1.562  121.0%  FAIL (overproduces d self-succession)
  ss_y       VMS=1.955  Sim=1.295   66.2%  FAIL (underproduces y self-succession)
  am_lf_enr  VMS=0.122  Sim=0.330  269.8%  FAIL (random EVA generates -am at LF at base rate)
  am_mid_enr VMS=0.195  Sim=0.198  101.6%  PASS (correct — MID am rate matches VMS)
  edy_rate   VMS=0.194  Sim=0.105   54.2%  FAIL (simulation generates half the expected edy suffix)
  word_len   VMS=5.400  Sim=7.176  132.9%  FAIL (simulation words 33% too long)
  qok_ch     VMS=1.267  Sim=0.966   76.3%  FAIL (near-pass but outside 20% threshold)
```

---

## Interpretation

### Critical finding 1: The calibration targeted different VMS values than the corpus parser produces

The "official" B-targets (am_ll=6.811, ss_mean=1.465, adj_rate=0.009) were established in earlier experiments. The current ZL3b B-dialect corpus parser produces: am_ll=6.550, ss_mean=1.164, adj_rate=0.009. The simulation was calibrated to 6.811 and 1.465; it achieves those targets precisely but overshots the corpus-computed values (am_ll 103.8%, ss_mean 124%). The ss_mean discrepancy (official 1.465 vs corpus 1.164) was flagged in F216 and confirmed here: the simulation's ss_mean calibration is against a target that exceeds the corpus-measured VMS value by 26%.

For adj_rate: simulation achieves 0.004 (BELOW VMS 0.009). The original calibration criterion was "≤ 0.009", which the simulation satisfies. But the absolute deviation is large (44.7% of VMS). The calibration was one-sided (upper bound), not a precise match.

### Critical finding 2: 12/13 uncalibrated metrics fail — systematic architectural failures

The failures are not random — they reveal three structural problems with the exp_211 architecture:

**Problem A: LF override is y-only (d_lf=40.6%, s_lf=13.1%)**
The p_lf_blind parameter sends 22% of LF words to y-onset, depleting d and s at LF. VMS B LF is dominated by d (14.8%), y (11.3%), s (11.2%), p (10.7%) — four onset classes are enriched at LF. The architecture only privileges y. The simulation therefore underproduces d, s, p at LF by 4–8×.

**Problem B: LL_ONSETS enriches ch, ok, qok — VMS has these near-neutral (ch_ll=196%, ok_ll=204%, qok_ll=310%)**
LL_ONSETS = {ok:0.21, qok:0.21, ch:0.14, other:0.28, d:0.16}. These weights heavily enrich ok, qok, ch at LL. VMS B LL shows ch≈0.94× (near-neutral), ok≈0.975× (near-neutral), qok≈0.595× (depleted). The architecture is pulling LL onset distribution in exactly the wrong direction for ch/ok/qok.

**Problem C: Copy buffer Timm erosion causes wrong-direction qok_lf (qok_lf=168.4%, WRONG DIRECTION)**
VMS qok is depleted at LF (0.778×). The simulation ENRICHES qok at LF (1.309×). Mechanism: Timm character modifications in MID positions gradually erode qok words from the copy buffer (replacing 'q' or 'o' or 'k' destroys the qok prefix; rebuilding qok by modification is very unlikely). MID positions accumulate non-qok words. Since LF uses cipher_lf_blind (78% random_eva_word with qok=12.1%), qok is elevated at LF relative to the qok-depleted MID pool. This is a previously undetected side effect of the copy buffer mechanism.

**Problem D: Word length overproduction (132.9%)**
The simulation generates words averaging 7.18 chars vs VMS 5.40 chars. The word generation model (onset + 'a/ai/o/oi/e/ei' + suffix) produces words longer than actual VMS vocabulary. This is a fundamental mismatch in the word-generation model, not the positional mapping.

**Problem E: edy-suffix underproduction (54.2%)**
VMS B edy-suffix rate is 19.4% (F206); simulation produces 10.5%. SUFFIX_WEIGHTS has 'edy': 0.183, which should give 18.3%. The shortfall is explained by Timm modifications: modifying edy-suffix words changes their suffix (cp=0.76, mp=0.9 means 68% of MID words are modified copies, often changing the suffix). The Timm character modification erodes edy just as it erodes qok.

### Architectural significance

The architecture calibrated to 5 primary metrics is NOT capturing a broad VMS structural signal. It is fitting a 5-dimensional slice of VMS structure while failing on 12 of 13 independent structural metrics. More importantly, several failures are in the WRONG DIRECTION (qok_lf enriched when VMS depletes it; ch_ll enriched when VMS is near-neutral). These wrong-direction failures indicate the architecture is ANTI-predictive for those metrics — it would give confidently wrong predictions.

The one passing uncalibrated metric (am_mid_enr=101.6%) passes because -am in MID positions is determined by the background copy distribution (which preserves some -am words), and VMS MID -am is also at a moderate background rate. This is a trivially expected pass given the architecture.

### Implications for discrimination

exp_217 establishes that the exp_211 architecture:
1. Reproduces 3/5 primary metrics against corpus-computed VMS (not 5/5, due to calibration target discrepancy and one-sided adj_rate criterion)
2. Reproduces 1/13 uncalibrated structural metrics
3. Fails in the wrong direction on qok_lf, ch_ll, ok_ll, qok_ll — confidently anti-predictive
4. Has two unrecognized failure modes: (a) Timm erosion distorts onset distributions in MID vs LF positions; (b) LL_ONSETS architecture enriches onsets that VMS does not enrich at LL

The architecture is not a comprehensive model of VMS structure — it is a narrow 5-parameter fit that happens to match the calibration targets.

---

## Limitations

1. The ±20% pass threshold is arbitrary. qok_ch at 76.3% fails by this criterion but is directionally correct (enriched in both VMS and simulation).
2. The calibrated metric discrepancy (official targets vs corpus-computed values) does not invalidate exp_211's calibration result — it reveals that different parsers/corpora give different values for the same text. The consistency issue was flagged in F216.
3. N=50 simulations — sufficient for mean estimates but CIs are moderate.
4. The "wrong direction" failures (qok_lf, LL onset enrichments) are mechanistically predicted and expected, not surprising. They confirm expected failure modes of the architecture.

---

## Self-Audit

**Target-awareness**: No new target-calibrated elements in this experiment. The simulation uses exactly exp_211's best-config parameters (p_blind=0.40, d_am=0.16, p_lf_blind=0.22, cp=0.76, mp=0.9), all of which are documented as target-calibrated. The 13 ADDITIONAL metrics are evaluated against corpus-computed VMS values (no calibration to these metrics). The exp_211 calibration caveat fully applies: the architecture was tuned to 5 specific signals, not to the broader structural picture tested here.

**Feature-destroying implementation**: No hypothesis predicts the simulation should pass the additional metrics (H410 is asking whether it does, not claiming it will). The experiment is a fair test of H410.

**Extrapolation**: The negative result (12/13 uncalibrated metrics fail) is interpreted within scope. The conclusion is: "exp_211's architecture fails 12/13 uncalibrated VMS structural metrics under the tested configuration." The claim that this is "systematic" is supported by the mechanistic explanation of three distinct failure modes, not extrapolation beyond the grid.

**Negative-result scope**: The experiment shows this specific architecture (blind LF y-override + blind LL -am mapping + Timm copy buffer) fails on uncalibrated metrics. The conclusion is NOT "no copy-buffer architecture can reproduce VMS structure." An architecture with (a) multi-onset LF distribution, (b) onset-neutral LL mapping, and (c) onset-preserving copy mechanism might reproduce more metrics. H410's result narrows the class of viable architectures, not the class of mechanisms.

**Control behavior**: VMS B corpus is the reference (not a shuffled control). The B corpus values were computed fresh using the same parser as exp_216 — consistent internal calibration. The calibrated metric discrepancy (corpus ss_mean=1.164 vs target 1.465) is the most significant control-behavior surprise, and its cause is understood (different parsers/populations for the "official" targets).

---

## Conclusion

H410 ANSWERED: exp_211's best configuration achieves 3/5 calibrated primary metrics (against corpus VMS) and 1/13 uncalibrated structural metrics. The architecture is a narrow 5-parameter fit to specific signals, not a comprehensive VMS structural model. Key failure modes: (1) LF override is y-only, missing d/s/p LF enrichment; (2) LL_ONSETS enriches ch/ok/qok while VMS has these near-neutral; (3) Timm copy buffer erosion causes wrong-direction qok_lf enrichment; (4) word length overproduction (+33%). The architecture's discrimination value lies in demonstrating joint achievability of the 5 primary metrics — not in providing a comprehensive structural account.
