# exp_308: Menzerath r Component Decomposition — LF/LL vs MID Contribution (H510)

**Date:** 2026-04-11
**Hypothesis:** H510 — VMS Menzerath r has a component from LF/LL word length scaling with line length, creating additional r beyond what the MID slope accounts for. The simulation's cipher_lf/cipher_ll generate words independently of line length, missing this component.

## Result: H510 CONFIRMED — LL word length is the DOMINANT driver of VMS Menzerath r; r_ll = −0.219 (VMS) vs −0.016 (sim), 92% gap; simulation missing the line-length-conditional LL mechanism

### Component Correlations: r(line_len, position_word_len)

| Section | N | r_total | r_lf | r_mid | r_ll | MID_slope |
|---------|---|---------|------|-------|------|-----------|
| overall VMS | 2338 | −0.2249 | −0.002 | −0.178 | −0.219 | −0.058 |
| stars VMS | 1068 | −0.2909 | −0.009 | −0.206 | −0.294 | −0.063 |
| bio VMS | 759 | −0.2075 | −0.027 | −0.170 | −0.208 | −0.046 |
| herbal VMS | 270 | −0.3293 | −0.049 | −0.321 | −0.157 | −0.111 |
| astro VMS | 50 | −0.3281 | +0.243 | −0.421 | −0.298 | −0.125 |
| simulation | 24110 | −0.134 | −0.010 | −0.108 | −0.016 | −0.051 |

### VMS Word Length by Line-Length Bucket (all B-dialect)

| Line_len | N_lines | LF_wl | MID_wl | LL_wl | Mean_wl |
|----------|---------|-------|--------|-------|---------|
| 2-4 | 215 | 5.642 | 5.530 | **5.730** | 5.614 |
| 5-6 | 452 | 5.699 | 5.658 | **5.334** | 5.607 |
| 7-8 | 647 | 5.802 | 5.609 | **5.181** | 5.576 |
| 9-10 | 695 | 5.799 | 5.392 | **4.679** | 5.360 |
| 11-15 | 329 | 5.587 | 5.075 | **4.422** | 5.063 |

VMS LL_wl drops **1.31 chars** (from 5.730 to 4.422) as line length increases from 2-4 to 11-15 words.

### Simulation Word Length by Line-Length Bucket

| Line_len | N_lines | LF_wl | MID_wl | LL_wl | Mean_wl |
|----------|---------|-------|--------|-------|---------|
| 2-4 | 1741 | 6.141 | 5.471 | **5.024** | 5.532 |
| 5-6 | 4022 | 6.132 | 5.340 | **4.972** | 5.416 |
| 7-8 | 6051 | 6.137 | 5.264 | **4.954** | 5.339 |
| 9-10 | 5898 | 6.146 | 5.239 | **4.958** | 5.305 |
| 11-15 | 5607 | 6.084 | 5.185 | **4.926** | 5.239 |

Simulation LL_wl nearly flat: only **0.098 chars** decrease (2-4 → 11-15). **13× weaker than VMS.**

## Key Findings

### F1: LL word length is the DOMINANT driver of VMS Menzerath r

Decomposing the overall VMS Menzerath r = −0.225:
- **r_lf = −0.002** (LF component): negligible contribution
- **r_mid = −0.178** (MID component): substantial
- **r_ll = −0.219** (LL component): dominant — as strong as the global r itself

The LL component contributes ~equal weight to the global Menzerath r as the MID component. The simulation captures the MID component at 61% (−0.108 vs −0.178) but misses the LL component at 7.3% (−0.016 vs −0.219).

### F2: VMS LL word length is strongly line-length conditional (1.31 chars decrease)

VMS LL_wl decreases from 5.730 (2-4 word lines) to 4.422 (11-15 word lines) — a 1.31 char decrease. The simulation's LL_wl decreases by only 0.098 chars (13× weaker). This means the simulation's cipher_ll, which generates LL words independently of line length, is missing a fundamental VMS structural property.

### F3: The LL mechanism is the highest-leverage architectural improvement

Gap analysis:
- LL component gap: r_ll = −0.219 (VMS) vs −0.016 (sim) → gap = 0.203
- MID component gap: r_mid = −0.178 (VMS) vs −0.108 (sim) → gap = 0.070

Closing the LL gap (gap = 0.203) would contribute ~3× more to Menzerath r recovery than closing the MID gap (gap = 0.070). A mechanism that makes p_blind line-length-conditional (H511) would directly address this.

### F4: Line-length-conditional LL mechanism is architecturally feasible

The simulation knows the line length (n) before generating LL words (the chunk length n is determined first). A new 18th mechanism: scale p_blind with line length. In long lines (n≥10), p_blind increases toward ~0.25-0.35, producing more short -am words; in short lines (n≤5), p_blind decreases to ~0.05-0.08, producing longer LL words. Average p_blind must remain calibrated to maintain am_ll target.

Approximate calibration: current p_blind=0.115 gives am_ll=6.55 (target). If p_blind scales linearly with line length, the mean p_blind (weighted by line length distribution) must equal 0.115. Line length distribution: 40% of lines have LL≤6, 35% have LL=7-9, 25% have LL=10+. A formula: p_blind(n) = 0.115 × (n/mean_n)^k for some k>0 would achieve this.

### F5: MID word length also has structured section-level differences

Stars and bio sections: r_mid ≈ −0.17 to −0.21 (simulation at 64-67% closure)
Herbal and astro: r_mid ≈ −0.32 to −0.42 (simulation at 26-34% closure)
The herbal/astro MID component gap is larger than their section r_ll, unlike bio/stars where r_ll dominates.

## Architecture Implications

The Menzerath r residual gap decomposes into:
1. **LL component (primary gap)**: r_ll = −0.016 (sim) vs −0.219 (VMS) — line-length-conditional LL mechanism missing. This is the dominant driver of the Menzerath r gap and is architecturally addressable (H511).
2. **MID component (secondary gap)**: r_mid = −0.108 vs −0.178 — 61% achieved; beta mechanism partially closes this; herbal/astro sections have steeper MID gradients than bio/stars (exp_307 F2).

## Self-Audit

**Target-awareness:** No calibration performed in this experiment — pure corpus analysis + simulation comparison. The simulation runs with exp_306 architecture parameters unchanged.

**Feature-destroying implementation:** Simulation computes LL words via cipher_ll which does not condition on line length. This is the identified gap, not an implementation error — it's an architectural feature of the cipher component.

**Extrapolation:** The claim "a line-length-conditional p_blind would close the LL gap" is speculative (H511, untested). The measured gap (r_ll = −0.016 vs −0.219) is a direct observation.

**Negative-result scope:** H510 CONFIRMED (not a negative result). The LF component hypothesis (LF word length scales with line length) is partially refuted: r_lf ≈ 0 in both VMS and simulation for most sections. Astro section shows r_lf = +0.243 but N=50 (noisy).

**Control behavior:** Simulation r_lf matches VMS r_lf (both near 0): ✓. Simulation r_mid is 61% of VMS — expected given beta mechanism achieves ~85% of VMS MID slope but full Menzerath r decomposition differs. Simulation r_ll is ~7% of VMS — confirms the cipher_ll architectural gap.
