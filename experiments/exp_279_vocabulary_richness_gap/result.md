# exp_279: VMS Vocabulary Richness Gap (H482)
**Hypothesis:** H482
**Date:** 2026-04-11
**Status:** CONFIRMED — gap is caused by missing midfix in MID words; onset+suffix model generates 10-15× fewer types than VMS

---

## Summary

The simulation's pure onset+suffix model for MID words generates only 194-223 unique types (A and B respectively), while VMS has 2036-2929 unique MID types — a 10-15× gap. The root cause is that 61-71% of VMS MID words contain a midfix region between the onset and suffix, which the simulation does not model for MID words. The midfix creates exponential vocabulary expansion: each onset+suffix pair spawns multiple word types via midfix variation.

---

## Key Results

### Vocabulary Size

| Corpus | Tokens | Unique Types | Types≥5 | TTR |
|--------|--------|-------------|---------|-----|
| VMS A MID | 6,264 | 2,036 | 214 | 0.325 |
| VMS B MID | 13,849 | 2,929 | 397 | 0.211 |
| Sim A (onset+suf only) | 6,264 | 194 | 140 | 0.031 |
| Sim B (onset+suf only) | 13,849 | 223 | 193 | 0.016 |

**Gap: VMS has 10-15× more unique types than the pure onset+suffix simulation model.**

### Onset-Suffix Pair Coverage

| Corpus | Onset types | Suffix types | Max pairs | Observed pairs | Fill rate | HHI/null |
|--------|------------|--------------|-----------|---------------|-----------|----------|
| VMS A MID | 19 | 12 | 228 | 195 | 85.5% | 4.25× |
| VMS B MID | 19 | 12 | 228 | 221 | 96.9% | 2.94× |

Both dialects fill nearly all onset-suffix pair slots (85-97%). The HHI/null ratio (4.25× A, 2.94× B) shows concentration: a subset of pairs dominates probability mass.

**Top-5 B-dialect pairs by frequency**: ch+other (602), ch+edy (438), ch+ey (388), sh+other (374), sh+edy (348). "other" suffix is the most common — masking words with non-standard midfixes.

### Word Internal Structure

| Corpus | Exact onset+suffix (no midfix) | Has midfix |
|--------|-------------------------------|-----------|
| VMS A MID | 29.1% | **70.9%** |
| VMS B MID | 38.3% | **61.7%** |

**The majority of VMS MID words (62-71%) contain a midfix region.** The onset+suffix model classifies these as "suffix=other" (because the characters between onset and suffix don't match a SUFFIX_PATTERN), which is why 'other' dominates the pair counts.

---

## Interpretation

**H482 CONFIRMED.** The vocabulary richness gap is caused by missing midfix in the simulation's MID word generation.

**Root cause decomposition:**

1. **Onset+suffix combination space** (19 onsets × 12 suffix patterns) = 228 theoretical pairs. Simulation uses this as its entire vocabulary — 194-223 unique types (some pairs very low probability). VMS also has 195-221 unique onset+suffix pairs — the same combinatorial space — but VMS's actual vocabulary is 10-15× larger.

2. **The midfix is the vocabulary expander.** Each onset+suffix pair spawns multiple word types via midfix variation (e.g., "ch" + "ol" yields "chol", "cheol", "chaol", "cholol", etc.). Since 62-71% of VMS MID words have a midfix, the effective vocabulary is onset × midfix-variants × suffix — potentially thousands of combinations.

3. **The simulation TTR gap** (Sim 0.016-0.031 vs VMS 0.211-0.325) is primarily caused by the missing midfix, not by r_mid parameter tuning. Even with r_mid=0, the pure onset+suffix model would only have ~200 types, capping TTR at ~0.03.

**Implication for simulation architecture:**

Adding midfix sampling to MID words (analogous to what was done for LF/LL in exp_270) would:
1. Expand MID vocabulary toward VMS levels (from ~200 to potentially ~1000+ types)
2. Extend word repetition distances (more types → less frequent repetition)
3. Increase TTR toward VMS levels
4. Possibly improve Menzerath r for B-dialect (longer MID words with midfixes at specific positions)
5. May require word_len_mean recalibration (midfix adds chars)

**New hypothesis generated:** H484 — Add midfix sampling to MID words using VMS MID midfix distribution; verify vocabulary expansion and repetition distance improvement.

---

## Self-Audit

**Target-awareness**: No calibration. Pure measurement study comparing VMS corpus to a simple simulation baseline.

**Feature-destroying implementation**: N/A — analysis only.

**Extrapolation**: The claim "midfix is the vocabulary expander" is confirmed by the 70.9% midfix rate in VMS MID words and the 10× vocabulary size gap. No parameter-extrapolation claims.

**Negative-result scope**: N/A — positive characterization.

**Control behavior**: The simulation baseline (pure onset+suffix) behaves exactly as expected (194-223 unique types). No surprises — the model is intentionally simplified. The gap from VMS is the finding.
