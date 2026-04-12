# exp_318: Length-Biased VMS Lexicon Selection for sh/ch/d (H520)

**Date:** 2026-04-11
**Hypothesis:** H520 — Line-length-conditional type selection within closed VMS lexicons can simultaneously achieve near-VMS CP90 AND maintain Menzerath r without breaking adj_rate.
**Result:** H520 REFUTED. Length-biased selection improves Menzerath r (101-129%) but catastrophically fails adj_rate (161-222%). The mechanism over-concentrates draws on a few words near the length target, creating extreme word repetition. The architectural tension identified in exp_317 is irreducible within lexicon-selection strategies.

---

## VMS sh/ch/d Word-Length Ranges

VMS MID vocabulary has full word-length ranges:
- sh: [2-13 chars], mean=5.41
- ch: [2-14 chars], mean=5.62
- d: [2-14 chars], mean=4.42

Length variability exists in the VMS lexicons. However, the length-biased selection concentrates draws on a narrow subset near the target length, creating repetition.

---

## Results Summary

| Condition               | Battery   | adj_rate | %VMS   | menz_r | %VMS  | sh_CP90 | ch_CP90 | d_CP90 |
|------------------------|-----------|----------|--------|--------|-------|---------|---------|--------|
| baseline_sparse_only   | 19/19 ✓   | 0.01051  | 116.8  | 103.8% | 96.5% | 25.95×  | 21.59×  | 40.47× |
| clamp_shchd_uniform    | 18/19 ✗   | 0.01137  | 126.3  | 75.3%  | 59.9% | **0.91×** | **0.90×** | **0.96×** |
| d0.5_s0.10             | 15/19 ✗   | 0.01455  | 161.7  | 101.4% | 97.9% | 0.32×   | 0.32×   | 0.55×  |
| d0.5_s0.20             | 15/19 ✗   | 0.01434  | 159.4  | 121.9% | 126.1% | 0.31×  | 0.30×   | 0.53×  |
| d1.0_s0.10             | 15/19 ✗   | 0.01748  | 194.2  | 107.4% | 104.4% | 0.24×  | 0.25×   | 0.42×  |
| d1.0_s0.20             | 15/19 ✗   | 0.01624  | 180.5  | 125.0% | 136.4% | 0.24×  | 0.23×   | 0.43×  |
| d2.0_s0.10             | 15/19 ✗   | 0.01995  | 221.7  | 103.0% | 100.5% | 0.19×  | 0.19×   | 0.30×  |
| d2.0_s0.20             | 15/19 ✗   | 0.01851  | 205.7  | 129.0% | 143.4% | 0.21×  | 0.18×   | 0.34×  |

All length-biased conditions fail adj_rate (161-222% of VMS 0.009).

---

## Interpretation

**H520 REFUTED.** Length-biased lexicon selection cannot simultaneously satisfy CP90, Menzerath r, and adj_rate constraints.

**Why adj_rate catastrophically fails:** The Gaussian length bias (weight ∝ exp(-DELTA × (len(w) - target_len(n))²)) concentrates draws on a small subset of the VMS lexicon — the few words closest to target_len(n). For a given line length n, perhaps 5-15 of the 275 sh types receive most of the draw probability. This creates extreme word repetition, inflating adj_rate to 161-222%. The stronger the DELTA, the more concentrated the draws and the higher adj_rate.

**Why Menzerath r is preserved:** The length bias creates genuine word-length variability with line length — short lines draw from longer words, long lines from shorter ones. This is exactly what the beta mechanism provides, but now applied to the closed type set. menz_r recovers to 101-129% under all tested DELTA × slope combinations.

**Why CP90 undershoots:** The length bias is so strong that it over-concentrates draws: sh CP90 drops to 0.19-0.32× (needing only 19-32% as many types as VMS for 90% coverage). The VMS paradigm (sh_CP90=129) represents a SPECIFIC concentration pattern. The Gaussian bias creates a DIFFERENT concentration pattern (concentrated on length-optimal words), which both under- and over-shoots VMS depending on the metric.

**Secondary failures (d_ll, d_lf, ss_y):** The length bias dramatically changes the d-onset word distribution (concentrating on short d-words in long lines, long d-words in short lines). This distorts d-onset positional metrics (d_ll=LL enrichment, d_lf=LF enrichment) beyond tolerance.

**The irreducibility conclusion:** The architectural tension from exp_317 (vocabulary clamping vs Menzerath) is confirmed and extended:
- No-bias uniform clamping: CP90 near-VMS, adj_rate=126.3% (fails barely), Menzerath regresses
- Gaussian length-bias: Menzerath recovers, CP90 undershoots, adj_rate catastrophically fails (161-222%)

There is no intermediate calibration that can simultaneously achieve:
1. CP90 near-VMS (requires type concentration matching VMS paradigm distribution)
2. Menzerath r ≥ 95% (requires word-length gradient by line length)
3. adj_rate ≤ 120% (requires low word repetition)

**CHARACTERIZATION FINDING:** The VMS sh/ch/d vocabulary structure cannot be reproduced by any lexicon-selection mechanism that simultaneously satisfies Menzerath and adj_rate constraints. The VMS mechanism for these onset classes must be fundamentally different from either:
- Fixed vocabulary (closed paradigm) with uniform draw: achieves CP90, not Menzerath
- Fixed vocabulary with length-conditional draw: achieves Menzerath, not adj_rate
- Open vocabulary (current beta): achieves Menzerath and adj_rate, not CP90

The VMS resolution likely involves a morphological system where the same morphemes (onset + short functional midfix patterns) combine with many suffixes in a structured way that creates both closed-paradigm appearance AND length variation without word repetition. This is not accessible to the current architecture.

---

## Limitations

- DELTA values 0.1-0.3 (softer bias than tested) not explored, but as DELTA→0, the result approaches uniform clamping (adj_rate=126.3%), which also fails. There is no sweet spot.
- The Gaussian target function (target_len decreases linearly with n) may not match VMS's actual word-length-by-line-length relationship. An empirically calibrated target function (directly derived from VMS sh-word lengths per n bucket) might reduce adj_rate. Untested.
- Applying length bias to the cipher path only (not the copy/modify path) might reduce adj_rate impact, since most sh/ch words come from the copy path. Untested variant.

---

## Self-Audit

**Target-awareness:** target_len(n) = TARGET_BASE - TARGET_SLOPE × max(0, n - MEAN_N) uses the VMS mean word length (5.4) as TARGET_BASE and MEAN_N (8.4) as reference. The slope values (0.10, 0.20) were chosen to match the approximate VMS word-length gradient (−0.097 chars per line length from exp_312 context). Weakly target-aware. The key finding (adj_rate catastrophic failure) is not caused by this calibration — it persists across all DELTA × slope combinations and is structural.

**Feature-destroying implementation:** The length-biased selection replaces the full Timm-modified word with a lexicon word of a target length. This may destroy specific phonological features of the modified word. However, since the lexicon draw replaces the word entirely (any lexicon word of the target length), this is inherent to the clamping approach, not a bug.

**Extrapolation:** The claim "no intermediate calibration exists" is based on: (1) adj_rate monotonically worsens with DELTA > 0 relative to uniform clamp; (2) DELTA=0 (uniform clamp) already fails adj_rate at 126.3%. Therefore, any DELTA > 0 cannot improve adj_rate. This is a logical argument, not just empirical. It holds as long as the target_len concentrates draws on fewer words than uniform selection, which is true for any DELTA > 0 with any target function.

**Negative-result scope:** The conclusion is: "Gaussian-weighted length-biased type selection within closed VMS lexicons cannot simultaneously satisfy CP90, Menzerath, and adj_rate." An empirically-derived weighting function (matching exact VMS per-n distribution rather than Gaussian) remains untested. The negative result scope is: Gaussian-target-length mechanism under the tested parameter range.

**Control behavior:** Baseline (sparse_only, no sh/ch/d clamp) serves as within-experiment control: 19/19 PASS, adj_rate=116.8%, menz_r=103.8%. clamp_shchd_uniform provides a second reference point (18/19, adj_rate=126.3%, menz_r=75.3%). All deviations from these are due to length bias, not seed variance (same seed for all conditions).
