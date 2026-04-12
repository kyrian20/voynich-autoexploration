# exp_268: Menzerath's Law in Simulation

**Hypothesis**: H473 — The existing copy-buffer simulation reproduces VMS Menzerath's Law (r(line_length, mean_word_length) < 0) without parameter adjustment, as a byproduct of buffer dynamics.

**Date**: 2026-04-11

---

## Results

### Menzerath Correlation

| Dialect | VMS r | Sim r (mean ± sd) | Runs with r<0 |
|---------|-------|-------------------|---------------|
| A | -0.189 (N=1675 lines) | +0.078 ± 0.026 | 0/30 |
| B | -0.206 (N=2389 lines) | +0.097 ± 0.021 | 0/30 |

**H473 DISCONFIRMED**: The simulation produces POSITIVE Menzerath correlation in 30/30 runs for both dialects — the opposite of VMS. This is not noise: the gap from VMS is 0/30 overlap.

### Position-Stratified Word Length

| Dialect | Position | VMS mean | Sim mean | Δ |
|---------|----------|----------|----------|---|
| A | LF | 5.447 | 4.708 | +0.739 |
| A | MID | 5.171 | 5.068 | +0.103 |
| A | LL | 5.403 | 4.775 | +0.628 |
| B | LF | 5.732 | 4.857 | +0.875 |
| B | MID | 5.409 | 5.413 | -0.005 |
| B | LL | 5.015 | 4.947 | +0.068 |

**Critical pattern**: Simulation MID words match VMS closely (Δ ≈ 0.1 chars A, 0.0 chars B). Simulation LF and LL words are substantially shorter than VMS (Δ ≈ 0.6–0.9 chars).

In VMS: LF > MID and LL ≈ MID (A-dialect), LF > MID > LL (B-dialect). Longer lines → more MID words → mean pulled toward shorter MID → **r < 0**.

In simulation: LF < MID and LL < MID. Longer lines → more MID words → mean pulled toward longer MID → **r > 0**.

### Bucket-Level Comparison (A-dialect)

| LinLen | VMS_N | VMS_mean | SIM_N | SIM_mean |
|--------|-------|----------|-------|----------|
| 2 | 111 | 5.937 | 175 | 4.683 |
| 5 | 271 | 5.335 | 265 | 5.002 |
| 9 | 108 | 4.928 | 99 | 5.015 |
| 11 | 21 | 4.537 | 27 | 5.172 |

VMS shows clear decrease from bucket 2 (5.937) to bucket 11 (4.537). Simulation shows nearly FLAT pattern, with slight increase at long lines (4.683 → 5.172).

---

## Root Cause Analysis

The simulation uses the **onset+suffix word construction model**:

```
word = onset + suffix                  [for most suffixes]
word = onset + vowel_bridge + edy/eedy [for -edy/-eedy suffixes]
```

This model correctly calibrates MID word length (because MID onset and suffix distributions are derived directly from VMS MID words and the construction matches their structure). However, VMS LF/LL words are longer than what onset+suffix produces because:

1. **LF words in VMS have longer midfix regions**: content-word LF positions (y, s, t, d enriched onset classes at LF per F263) combine with longer vowel sequences (e.g., 'daiin' = d + aiin, but only 'ain' is in SUFFIX_PATTERNS; words like 'dain' vs 'daiin' differ by midfix).

2. **LL words with -am**: VMS LL -am words are built as onset + 'am', which gives SHORT words (e.g., 'dam' = 3 chars, 'cham' = 4 chars). The p_blind mechanism draws onset from ll_onsets + 'am', producing very short -am words. But VMS LL MEAN is 5.4 chars — the LL mean in VMS is pulled up by NON-am words that are apparently longer than the simulation produces.

3. **LF words in simulation use cipher_lf**, which samples from onset_lf and suffix_lf_sup distributions derived from VMS LF words. But the suffix distribution has many 'other' suffix cases that map to short words — when a VMS LF word has complex midfix structure not captured by SUFFIX_PATTERNS, the suffix is 'other' and the simulation produces a short word without midfix.

**Core gap**: VMS LF/LL words have richer midfix structure (vowel sequences between onset and suffix) than the onset+suffix model captures. The model was optimized for MID words (which dominate the corpus) and the battery's word_len_mean metric calibrates the global mean, masking this positional gap.

---

## Implications

This is a new structural finding that is NOT in the 19-metric battery. The battery passes word_len_mean as a global metric; the positional decomposition reveals that LF/LL words are systematically too short in the simulation, while MID words are correctly calibrated.

The Menzerath correlation in VMS (r ≈ -0.19 to -0.21 in exp_268; -0.25 to -0.29 in exp_267, slightly different parsing) is driven by VMS LF/LL words being longer than MID. This property of VMS is NOT reproduced by the simulation — the opposite direction emerges.

**New hypothesis generated**: H478 — Can the simulation's LF/LL word length be corrected by a position-aware word construction that models the midfix vowel region? If VMS LF/LL words are systematically longer due to richer midfix structure, can adding a vowel bridge (analogous to the -edy bridge) to LF/LL word construction close the gap?

---

## Limitations

1. VMS Menzerath r differs between exp_267 (-0.249/-0.293) and exp_268 (-0.189/-0.206). The difference likely reflects parsing differences (exp_267 used the `lpos` field from the corpus; exp_268 uses first/last position within parsed lines). The DIRECTION is consistent: both show r < 0.
2. Exp_268 uses the same Latin corpus for all 30 runs (shuffled differently each run) — not varied across texts. This does not affect conclusions since the mechanism is in cipher_lf/cipher_ll, not Latin.
3. Root cause hypothesis (midfix region gap) is proposed but not yet tested.

---

## Self-Audit

**Target-awareness**: No target-aware elements. The simulation parameters are from the finalized 13/12-mechanism architectures (exp_264/257). No parameters were tuned for Menzerath.

**Feature-destroying implementation**: No feature-destroying elements. The Menzerath test measures line-level mean word length vs line length — directly measured from simulation output. The implementation faithfully runs the simulation and measures the correlation.

**Extrapolation**: No claims beyond tested grid. The result "simulation does not reproduce Menzerath" applies to these specific simulation architectures. A modified simulation with longer LF/LL words could potentially produce r < 0 — this is proposed as H478, not claimed as a result.

**Negative-result scope**: The conclusion is: "The existing simulation (with MID-calibrated word construction and cipher_lf/cipher_ll) does not reproduce VMS Menzerath's Law. The root cause is that simulation LF/LL words are too short by 0.6–0.9 chars." This does not imply "copy-buffer architectures cannot produce Menzerath's Law" — it implies this specific implementation fails.

**Control behavior**: No control distribution used. Simulation serves as the model to compare to VMS. No unexpected control behavior.

---

## Conclusion

**H473 DISCONFIRMED**: Simulation produces r = +0.078 (A) and +0.097 (B) — positive Menzerath (longer lines → longer mean word length), opposite of VMS. Root cause: simulation LF/LL words are 0.6–0.9 chars shorter than VMS LF/LL words, while MID word length matches well. This is a new structural gap NOT captured by the 19-metric battery.

F268 added. H473 RESOLVED (disconfirmed). H478 generated (midfix correction for LF/LL word construction).
