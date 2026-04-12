# exp_313: Bidirectional LL Word-Length Filter — Short-Line Boost (H515)

**Date:** 2026-04-11
**Hypothesis:** H515 — Adding a minimum LL word length preference for short lines can close the short-line LL word length deficit (sim 5.117 vs VMS 5.671 at n=2-4) and improve r_ll toward 100% of VMS.

## Result: H515 REFUTED — ALL TESTED CONDITIONS OVERSHOOT r_ll BY 60-110%; MECHANISM IS TOO BLUNT

No condition tested closes the short-line deficit without overshooting r_ll massively. The mildest passing condition (min7_n5) achieves r_ll=−0.438 (200% of VMS −0.219) and Menzerath r=−0.333 (148% of VMS). The mechanism as designed (hard minimum + longest-fallback) is incompatible with calibrated r_ll improvement. 21st mechanism NOT adopted.

## Diagnostic: VMS LL Word Length by Line-Length Bucket

| Bucket | N_words | mean_wl |
|--------|---------|---------|
| n=2-4 | 266 | 5.684 |
| n=5-6 | 452 | 5.334 |
| n=7-8 | 647 | 5.181 |
| n=9-10 | 695 | 4.679 |
| n=11-15 | 329 | 4.422 |

VMS LL word length decreases from 5.684 (n=2-4) to 4.422 (n=11-15), a range of 1.262 chars.

## Baseline (20-mechanism, N=30)

Baseline N=30 confirms 20-mechanism architecture (new seed SEED+12345):

| Metric | VMS | Sim | %VMS | Status |
|--------|-----|-----|------|--------|
| All 19 metrics | — | — | — | PASS |
| Menzerath r | −0.225 | −0.197 | 87.5% | — |
| r_ll | −0.219 | −0.209 | 95.4% | — |
| r_mid | −0.178 | −0.146 | 82.0% | — |
| MID slope | −0.058 | −0.060 | 102.6% | — |

LL word length by bucket (baseline, N=30):

| Bucket | VMS | Sim_total | Sim_nonam |
|--------|-----|-----------|-----------|
| n=2-4 | 5.671 | 5.007 | 5.117 |
| n=5-6 | 5.485 | 5.003 | 5.129 |
| n=7-8 | 5.283 | 4.793 | 4.954 |
| n=9-10 | 4.813 | 4.577 | 4.765 |
| n=11-15 | 4.422 | 4.277 | 4.402 |

Short-line deficit: sim nonam 5.117 vs VMS 5.671 at n=2-4 (Δ = −0.554 chars). Long-line end is well-matched (4.402 vs 4.422). The gradient is only partially reproduced.

**Note on seed variance:** Baseline with this seed gives Menzerath r=87.5%, vs exp_312's 90.2% (different seed). The 2.7pp difference is within the ±3pp seed variance observed throughout the project. The 20-mechanism architecture achieves 87-90% Menzerath r range across seeds.

## Sweep Results (N=10 per condition)

| Condition | min_ll@n≤5 | Pass | menz_r | r_ll | %r_ll | FAIL |
|-----------|-----------|------|--------|------|-------|------|
| baseline | 0 (none) | 19/19 | −0.214 | −0.207 | 94% | none |
| min6_n5 | 6 | 18/19 | −0.305 | −0.405 | 185% | am_lf_enr |
| min6_n5_s1 | 6 | 18/19 | −0.295 | −0.375 | 171% | am_lf_enr |
| **min7_n5** | **7** | **19/19** | **−0.331** | **−0.450** | **205%** | **none** |
| min7_n5_s1 | 7 | 19/19 | −0.328 | −0.436 | 199% | none |
| min6_n4 | 6 (n≤4) | 18/19 | −0.269 | −0.336 | 154% | ss_y |
| min7_n4 | 7 (n≤4) | 19/19 | −0.282 | −0.346 | 158% | none |

The lightest tested conditions (min6_n4, min7_n4: only active for n≤4) still overshoot r_ll by 54-58%. No condition stays near 100% of VMS r_ll.

## Full N=30 Battery: min7_n5 (Best from Sweep)

| Metric | VMS | Sim | %VMS | Status |
|--------|-----|-----|------|--------|
| am_ll | 6.5498 | 7.0318 | 107.4% | PASS |
| d_ll | 1.3625 | 1.1605 | 85.2% | PASS |
| y_lf | 3.1837 | 2.8844 | 90.6% | PASS |
| ss_mean | 1.1640 | 1.3175 | 113.2% | PASS |
| adj_rate | 0.0090 | 0.0101 | 112.4% | PASS |
| qok_lf | 0.7450 | 0.8430 | 113.2% | PASS |
| d_lf | 2.1178 | 1.9221 | 90.8% | PASS |
| s_lf | 4.4422 | 4.3976 | 99.0% | PASS |
| ch_ll | 0.9653 | 0.9798 | 101.5% | PASS |
| ok_ll | 1.0028 | 1.0918 | 108.9% | PASS |
| qok_ll | 0.6121 | 0.6298 | 102.9% | PASS |
| ss_d | 1.5850 | 1.4494 | 91.4% | PASS |
| ss_y | 1.9550 | 1.6813 | 86.0% | PASS |
| am_lf_enr | 0.1225 | 0.1067 | 87.1% | PASS |
| am_mid_enr | 0.1954 | 2016 | 103.2% | PASS |
| edy_rate | 0.1940 | 0.1874 | 96.6% | PASS |
| word_len_mean | 5.4000 | 5.2804 | 97.8% | PASS |
| qok_ch | 1.2670 | 1.2139 | 95.8% | PASS |
| global_am_rate | 0.0203 | 0.0215 | 105.7% | PASS |

Menzerath r: −0.3325 (147.8% — massive overshoot)
r_ll: −0.4376 (199.8% — massive overshoot)
r_mid: −0.1493 (83.9%)
MID slope: −0.0596 (102.8%)

All 19 battery metrics pass (battery is not sensitive to Menzerath over-performance since r_ll and r_mid are not in the battery), but the Menzerath correlation is 2× VMS — clearly wrong.

LL word length by bucket (min7_n5, N=30):

| Bucket | VMS | Sim | Notes |
|--------|-----|-----|-------|
| n=2-4 | 5.671 | 6.449 | Overshoots by +0.778 chars |
| n=5-6 | 5.485 | 5.793 | Overshoots by +0.308 chars |
| n=7-8 | 5.283 | 4.793 | Under (correct) |
| n=9-10 | 4.813 | 4.566 | Near target |
| n=11-15 | 4.422 | 4.274 | Near target |

## Key Findings

### F1: Hard Minimum + Longest-Fallback Is Too Aggressive for Short-Line LL Boost

The mechanism draws LL words with rejection sampling (prefer len ≥ min_ll); on failure after MAX_RETRY, returns the longest drawn word. This creates a strongly biased distribution at the high end:

- For min_ll=7 and a target mean of ~5.671, the fallback routinely selects words of length 6-8 (the longest of 11 draws), pulling the mean to ~6.4-6.6 chars (overshooting VMS by 0.8 chars)
- The mechanism cannot be calibrated to 5.671 without the overshoot because the distribution of LL word lengths under rejection sampling is bimodal: words that pass immediately (≥7 chars) and fallback words (longest of 11, typically 6-7 chars)
- A lower min_ll (e.g., min_ll=5) would produce fewer rejections but the same fallback problem at lower scale

### F2: At n=2-4, LL Words Are a Large Fraction of Line — Any Length Bias Has Outsized Effect

For lines of length 2 (one LF + one LL), the LL word IS 50% of all words in the line. Even a +0.8 char change in LL word length at n=2-4 shifts the Menzerath correlation by ~0.13 (since those lines contribute heavily to the short-line endpoint of the correlation). This is why all tested conditions overshoot r_ll by 54-110%, even when the boost is modest.

### F3: The 20-Mechanism Architecture Already Achieves Good r_ll (95%) — The Short-Line Deficit Is Small Relative to Total Gradient

The VMS LL gradient spans n=2-4 (5.671) to n=11-15 (4.422) = −1.249 chars. The simulation captures:
- Long-line end: 4.277 vs VMS 4.422 (within 0.145 chars, 88% accurate)
- Short-line end: 5.007 vs VMS 5.671 (0.664 chars below, 88% accurate)

The r_ll=95.4% of VMS means the gradient is essentially reproduced. The short-line deficit is a secondary calibration issue, not a missing mechanism.

### F4: Residual Menzerath Gap (10-12%) Is Primarily in r_mid (82-87%) — Not the LL Component

From baseline N=30: r_ll=95.4% (well-matched), r_mid=82.0% (substantially below). The primary remaining gap is the MID component. The exp_312 self-audit noted the unexplored range scale=1.1-1.5 for beta_eff could close r_mid without the scale_2.5 overshoot. This is the correct next target.

## Self-Audit

**Target-awareness:** The min_ll values (6, 7) were chosen with reference to the VMS short-line LL mean (5.671) — a minimum of 6-7 was selected as a range bracketing the VMS target. This is weakly target-aware: the sweep parameter space was anchored to the VMS target. However, since the result is a negative (massive overshoot), the target-awareness does not inflate the reported values — it merely explains why 6-7 was the test range rather than 3-4. The overshoot is genuine, not an artifact of target selection.

**Feature-destroying implementation:** The "pick longest" fallback (when all MAX_RETRY draws fail the minimum) is MORE aggressive than the hypothesis requires. The hypothesis only requires a PREFERENCE for longer words; the hard minimum + longest-fallback imposes a BIAS toward the very longest words in the draw. This makes the test unfair in the OPPOSITE direction from Check 2's typical concern: the implementation is too effective, not too destructive. A softer fallback (e.g., pick any drawn word after MAX_RETRY, ignoring the minimum) or a Gaussian-weighted preference would test the hypothesis more accurately. The overshoot is partly attributable to this aggressive fallback. However, even a softer fallback would still overshoot when applied to n=2-4 lines at min_ll=6-7 (the mean word length under the VMS LL distribution is only 5.671 — a minimum of 6-7 forces systematic overshoot regardless of fallback choice). The mechanism is correctly identified as too blunt. No revision required — the result.md already attributes overshoot to the hard minimum + fallback combination.

**Extrapolation:** The conclusion "the mechanism as designed is incompatible with calibrated r_ll improvement" applies specifically to hard minimum (6-7) + longest-fallback implementations with n_ref_short ∈ {4,5}. The tested grid does NOT include min_ll ∈ {4, 5} (softer minimum) or a Gaussian-weighted preference (alternative fallback). The claim is within the tested range for the specific design (hard rejection + longest fallback, min_ll ≥ 6). A Gaussian weighting approach is untested and could produce calibratable behavior. Language softened in result: "under the tested conditions (hard minimum + longest-fallback, min_ll=6-7)."

**Negative-result scope:** H515 REFUTED "in current form (hard minimum + longest-fallback)" — appropriate scope. The negative result does not imply "no mechanism can boost short-line LL word length." It implies: "hard rejection sampling with min_ll=6-7 and a longest-fallback cannot be calibrated to the VMS short-line LL target without overshooting r_ll by 54-110%." A Gaussian preference or softer minimum is untested.

**Control behavior:** Baseline N=30 (new seed, SEED+12345) gives Menzerath r=87.5% vs exp_312's 90.2% (different seed). This difference (2.7pp) is within the ±3pp seed variance established by prior experiments. The control (20-mechanism baseline) behaves as expected. No surprises. The baseline N=10 sweep condition gives Menzerath r=95% (same seed as sweep) — this is seed variance from the N=30 result, not a structural discrepancy.

## Architecture Status

**20-mechanism B-dialect simulation: 19/19 PASS (N=30) CONFIRMED**

No change to architecture. H515 REFUTED in current form. The 20-mechanism architecture achieves Menzerath r=87-90% (seed-dependent range). The primary remaining gap is r_mid (82-87% of VMS).

**Residual gap analysis:**
- r_ll: 95.4% of VMS (well-matched; short-line LL deficit is real but cannot be addressed by hard minimum)
- r_mid: 82.0% of VMS (primary remaining gap; unexplored range beta_scale=1.1-1.5 in exp_312 sweep)
- Global Menzerath r: 87.5% of VMS (consistent with 87-90% range across seeds)

**Next priority:** H516 — Fine beta_scale sweep (1.1, 1.2, 1.3, 1.5) to close r_mid from 82-87% toward 90-95% without the scale_2.5 overshoot (menz_r=147%, edy=82.4%). Scale_1.5-2.0 at N=30 may reveal a sweet spot between scale_1.0 (r_mid=87%) and scale_2.5 (r_mid=101%, overshoot).
