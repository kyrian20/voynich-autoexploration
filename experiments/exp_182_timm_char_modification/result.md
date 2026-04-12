# exp_182: Character-Level Timm Modification — Position-Aware Hybrid
**Date**: 2026-04-11
**Hypothesis**: Character-level Timm modification (single-char replace/insert/delete) in the position-aware hybrid produces ss_mean/adj_rate values intermediate between exp_180 (onset-replacing, 0/18 viable) and exp_181 (onset-preserving, 4/36 viable), falling closer to exp_181 because ~79% of single-char modifications fall outside the onset region.
**Addresses**: Opus review exp_180 Section D3; exp_181 Limitation 3.
**Status**: PRE-REGISTRATION RESULT — 8/36 VIABLE. Timm character-level modification produces MORE viable combinations than both exp_180 (0) and exp_181 (4). The primary reason: character-level modification has ~2% collision rate (new char matches old by chance: 1/16 × 1/3 ≈ 2% per modification) vs suffix modification's ~17% collision rate (new suffix matches old). This lower collision rate means adj_rate decreases faster with MODIFY_PROB under Timm modification. Three combinations achieve adj_rate ≤ VMS level (0.009) while maintaining ss_mean ≥ 1.2 and am_ll ≥ 5.0 — the first such result in the experimental program.

**COMMITTED CLAIM CHECK REQUIRED**: See Section 7. C004 contradiction condition is triggered.

**Configuration**: 36 combinations (COPY_PROB ∈ {0.2, 0.3, 0.4, 0.5, 0.6, 0.7} × MODIFY_PROB ∈ {0.3, 0.4, 0.5, 0.6, 0.7, 0.8}). 50 simulations per combination. 1800 total runs. MID-only buffer: WINDOW=20. Seed base: 182000.

**Viability thresholds**: am_ll ≥ 5.0× AND ss_mean ∈ [1.2, 1.7] AND adj_rate ≤ 0.015.

**VMS targets**: am_ll=6.811, y_lf=3.506, ss_mean=1.465, adj_rate=0.009.

---

## 1. HEADLINE RESULT

**8 / 36 combinations are viable** (lenient threshold: am_ll ≥ 5.0, ss_mean ∈ [1.2, 1.7], adj_rate ≤ 0.015).

**3 / 36 combinations achieve adj_rate ≤ 0.009 (VMS level) while maintaining ss_mean ≥ 1.2 and am_ll ≥ 5.0** — the first such result in the experimental program.

### Best combination by joint score (am_ll × ss_mean): cp=0.7, mp=0.4
*(Not viable by lenient threshold — adj_rate=0.0245 > 0.015. Listed for reference.)*
- am_ll = 6.122 — passes threshold ✓
- ss_mean = 1.476 — passes threshold ✓ (extremely close to VMS 1.465)
- adj_rate = 0.0245 — fails adj threshold ✗

### Best viable combination by joint score: cp=0.7, mp=0.6
- am_ll = 6.190 [5.931, 6.579] — passes threshold ✓ (90.9% of VMS)
- y_lf = 2.432 [2.092, 2.718]
- ss_mean = 1.424 [1.322, 1.519] — passes threshold ✓ (97.2% of VMS)
- ss_mean_mid = 1.742 [1.641, 1.858]
- adj_rate = 0.0140 [0.0124, 0.0156] — passes threshold ✓

### Combinations achieving VMS-level adj_rate (≤ 0.009) with ss_mean ≥ 1.2 and am_ll ≥ 5.0:

| combination | am_ll | ss_mean | adj_rate | %VMS_am | %VMS_ss | vs VMS_adj |
|-------------|-------|---------|----------|---------|---------|-----------|
| cp=0.6, mp=0.7 | 6.093 | 1.279 | **0.0085** | 89.5% | 87.3% | ≤ VMS |
| cp=0.6, mp=0.8 | 6.099 | 1.266 | **0.0060** | 89.6% | 86.4% | < VMS |
| cp=0.7, mp=0.8 | 6.308 | 1.368 | **0.0069** | 92.6% | 93.4% | < VMS |

VMS values: am_ll=6.811, ss_mean=1.465, adj_rate=0.009. None of the three fully reproduce VMS am_ll or ss_mean, but the best (cp=0.7, mp=0.8) is at 92.6% and 93.4% respectively. adj_rate is below VMS on all three.

---

## 2. FULL PARAMETER GRID

| cp  | mp  | am_ll               | y_lf  | ss_full             | ss_mid              | adj_rate              | viable |
|-----|-----|---------------------|-------|---------------------|---------------------|-----------------------|--------|
| 0.2 | 0.3 | 5.819 | 2.392 | 1.056 | 1.095 | 0.0079 | no |
| 0.2 | 0.4 | 5.806 | 2.396 | 1.052 | 1.089 | 0.0068 | no |
| 0.2 | 0.5 | 5.805 | 2.417 | 1.058 | 1.085 | 0.0061 | no |
| 0.2 | 0.6 | 5.827 | 2.394 | 1.064 | 1.096 | 0.0052 | no |
| 0.2 | 0.7 | 5.816 | 2.398 | 1.049 | 1.079 | 0.0044 | no |
| 0.2 | 0.8 | 5.840 | 2.385 | 1.055 | 1.091 | 0.0036 | no |
| 0.3 | 0.3 | 5.806 | 2.384 | 1.110 | 1.172 | 0.0109 | no |
| 0.3 | 0.4 | 5.786 | 2.397 | 1.102 | 1.160 | 0.0094 | no |
| 0.3 | 0.5 | 5.855 | 2.420 | 1.096 | 1.149 | 0.0079 | no |
| 0.3 | 0.6 | 5.880 | 2.410 | 1.088 | 1.144 | 0.0065 | no |
| 0.3 | 0.7 | 5.874 | 2.400 | 1.077 | 1.124 | 0.0052 | no |
| 0.3 | 0.8 | 5.865 | 2.419 | 1.067 | 1.110 | 0.0039 | no |
| 0.4 | 0.3 | 5.828 | 2.389 | 1.166 | 1.252 | 0.0145 | no |
| 0.4 | 0.4 | 5.833 | 2.381 | 1.144 | 1.240 | 0.0123 | no |
| 0.4 | 0.5 | 5.873 | 2.438 | 1.146 | 1.239 | 0.0101 | no |
| 0.4 | 0.6 | 5.895 | 2.398 | 1.130 | 1.215 | 0.0081 | no |
| 0.4 | 0.7 | 5.901 | 2.387 | 1.128 | 1.208 | 0.0063 | no |
| 0.4 | 0.8 | 5.957 | 2.390 | 1.132 | 1.213 | 0.0047 | no |
| 0.5 | 0.3 | 5.852 | 2.411 | 1.226 | 1.366 | 0.0191 | no |
| 0.5 | 0.4 | 5.865 | 2.419 | 1.238 | 1.367 | 0.0158 | no |
| **0.5** | **0.5** | **5.938** | **2.394** | **1.214** | **1.353** | **0.0128** | **YES** |
| **0.5** | **0.6** | **5.967** | **2.415** | **1.200** | **1.337** | **0.0098** | **YES** |
| 0.5 | 0.7 | 5.972 | 2.423 | 1.189 | 1.319 | 0.0074 | no (ss<1.2) |
| 0.5 | 0.8 | 5.977 | 2.448 | 1.175 | 1.291 | 0.0053 | no (ss<1.2) |
| 0.6 | 0.3 | 5.926 | 2.435 | 1.325 | 1.525 | 0.0249 | no |
| 0.6 | 0.4 | 5.989 | 2.475 | 1.322 | 1.521 | 0.0198 | no |
| 0.6 | 0.5 | 6.015 | 2.448 | 1.305 | 1.504 | 0.0157 | no |
| **0.6** | **0.6** | **6.018** | **2.450** | **1.277** | **1.474** | **0.0118** | **YES** |
| **0.6** | **0.7** | **6.093** | **2.503** | **1.279** | **1.480** | **0.0085** | **YES** (adj ≤ VMS) |
| **0.6** | **0.8** | **6.099** | **2.444** | **1.266** | **1.465** | **0.0060** | **YES** (adj < VMS) |
| 0.7 | 0.3 | 6.059 | 2.436 | 1.480 | 1.796 | 0.0317 | no |
| 0.7 | 0.4 | 6.122 | 2.477 | 1.476 | 1.804 | 0.0245 | no |
| 0.7 | 0.5 | 6.149 | 2.477 | 1.451 | 1.763 | 0.0189 | no |
| **0.7** | **0.6** | **6.190** | **2.432** | **1.424** | **1.742** | **0.0140** | **YES** |
| **0.7** | **0.7** | **6.205** | **2.454** | **1.406** | **1.725** | **0.0101** | **YES** |
| **0.7** | **0.8** | **6.308** | **2.499** | **1.368** | **1.677** | **0.0069** | **YES** (adj < VMS) |

---

## 3. THREE-WAY COMPARISON: exp_180 vs exp_182 vs exp_181 AT mp=0.5

| cp  | E180 ss | E182 ss | E181 ss | E180 adj | E182 adj | E181 adj |
|-----|---------|---------|---------|----------|----------|----------|
| 0.3 | 1.045   | 1.096   | 1.114   | 0.0092   | 0.0079   | 0.0097   |
| 0.5 | 1.094   | 1.214   | 1.264   | 0.0156   | 0.0128   | 0.0171   |
| 0.6 | 1.108   | 1.305   | 1.401   | 0.0198   | 0.0157   | 0.0220   |
| 0.7 | 1.148   | 1.451   | 1.574   | 0.0248   | 0.0189   | 0.0283   |

**Key pattern**: exp_182 (Timm) has intermediate ss_mean (between E180 and E181) but LOWER adj_rate than E181. At matched adj_rate ≈ 0.016, E182 achieves ss_mean ≈ 1.35 vs E181 ≈ 1.26.

**Interpolation fraction** (f = (ss_182 − ss_180) / (ss_181 − ss_180)):
- cp=0.3, mp=0.5: f = 0.740
- cp=0.5, mp=0.5: f = 0.708
- cp=0.6, mp=0.5: f = 0.673
- cp=0.7, mp=0.5: f = 0.710

Mean f ≈ 0.71. This is consistent with the theoretical estimate: ~79% onset preservation from Timm character-level modification at mean EVA word length, slightly above the 71% empirical interpolation fraction (some non-linearity expected).

---

## 4. THE ADJ_RATE ADVANTAGE OF TIMM MODIFICATION

**Why does Timm modification achieve lower adj_rate than suffix modification at matched MODIFY_PROB?**

Under **suffix modification (exp_181)**: A modified copy produces the same word when the new suffix matches the original suffix. The most common suffix is 'edy' (weight 0.183), giving an 18.3% collision rate for that suffix; overall expected collision rate ~17%. This is the residual coupling that prevented adj_rate from reaching VMS level in exp_181.

Under **Timm single-character modification (exp_182)**: A modified copy produces the same word when the replacement character happens to equal the character it replaced (probability 1/16 ≈ 6.25% for replacements), or when the modified word happens to be identical (negligible for inserts/deletes). Only 1/3 of modifications are replacements, so overall expected collision rate: 1/3 × 6.25% + 1/3 × 0 + 1/3 × 0 ≈ 2%. This is ~8× lower than the suffix modification collision rate.

The lower collision rate means: increasing MODIFY_PROB reduces adj_rate more aggressively under Timm modification, allowing adj_rate to cross below the VMS threshold (0.009) while maintaining viable ss_mean.

At cp=0.7, each 0.1 increment in MODIFY_PROB reduces adj_rate by approximately 0.025 (0.0317 → 0.0245 → 0.0189 → 0.0140 → 0.0101 → 0.0069 from mp=0.3 to mp=0.8). The linear trend continues below VMS level.

**IMPORTANT CAVEAT (target-awareness check)**: This adj_rate advantage is mechanistically genuine, but the specific parameter combination that achieves VMS-level adj_rate (cp=0.7, mp=0.8) was not predicted in advance. The experiment was pre-registered as testing whether 0-4 viable combinations would appear. The discovery that 3 combinations achieve VMS-level adj_rate is a finding, not a prediction — and it should be interpreted as such.

---

## 5. WHY exp_182 IS MORE VIABLE THAN exp_181

exp_181 (suffix-replacing) achieved 4/36 viable at lenient threshold and 0/36 at VMS adj_rate threshold, due to ~17% suffix collision.

exp_182 (Timm, char-level) achieves 8/36 viable at lenient threshold and **3/36 at VMS adj_rate threshold** (cp=0.6/mp=0.7, cp=0.6/mp=0.8, cp=0.7/mp=0.8), due to ~2% character collision.

This reversal of the "exp_182 should have fewer viable combinations than exp_181" prediction illustrates that the adj_rate is driven primarily by the collision rate of the modification, not by the onset preservation rate. Onset preservation drives ss_mean; collision rate drives adj_rate. Timm modification has both moderate onset preservation (~79%) AND very low collision rate (~2%), giving the best of both properties.

---

## 6. WITHIN-MID-ONLY SELF-SUCCESSION

ss_mid is consistently 8–19% higher than ss_full at the same parameter combination — consistent with exp_181's boundary dilution finding.

At cp=0.6, mp=0.8: ss_mid = 1.465, equal to VMS ss_mean target. This shows the copy buffer is generating VMS-level onset clustering within its operating domain; the full-corpus dilution reduces it to 1.266. At cp=0.7, mp=0.8: ss_mid = 1.677, above VMS level.

---

## 7. COMMITTED CLAIM CHECK — C004 CONTRADICTION

**THIS SECTION MUST BE FLAGGED. DO NOT UPDATE findings.md.**

C004 states: "Under VMS-level adj_rate (≤ 0.009), 0/36 combinations are viable." (Referring to exp_181 architecture.)

The C004 contradiction condition reads: "Any tested mechanism (copy-buffer hybrid or otherwise) producing joint viability at VMS-level adj_rate (≤ 0.009), ss_mean ≥ 1.2, and am_ll ≥ 5.0 would contradict this claim's residual gap statement and trigger the contradiction rule."

In exp_182, three combinations achieve adj_rate ≤ 0.009 simultaneously with ss_mean ≥ 1.2 and am_ll ≥ 5.0:
- cp=0.6, mp=0.7: adj=0.0085, ss=1.279, am_ll=6.093 — all three conditions met
- cp=0.6, mp=0.8: adj=0.0060, ss=1.266, am_ll=6.099 — all three conditions met
- cp=0.7, mp=0.8: adj=0.0069, ss=1.368, am_ll=6.308 — all three conditions met

**This satisfies the literal contradiction condition in C004.**

Note: C004 specifically refers to the exp_181 architecture (onset-preserving suffix modification). exp_182 uses a different modification operation (Timm character-level). The "residual gap statement" in C004 says the best viable combination is at 160% of VMS adj_rate — but that is now superseded for exp_182, which achieves adj_rate below VMS level. A nuanced reading of C004 is that it was meant to characterize the exp_181 result, not preclude all future mechanisms. However, the contradiction condition text is written broadly ("any tested mechanism"), so it is triggered.

**Per SOUL.md behavioral constraints**: Writing to open_questions.md instead of findings.md or failed_approaches.md. Looping to human.

---

## 8. HONESTY CHECK (TARGET-AWARENESS)

**Target-aware elements**:

1. **LL cipher table (explicitly target-aware, inherited from exp_177)**: All Latin clause-final morphemes → EVA -am. The am_ll metric is conditional on this calibration. A blind cipher would not reproduce am_ll ≥ 5.0.

2. **LF cipher table (partially target-aware, inherited from exp_177)**: y-onset mapping. y_lf metric is conditional.

3. **MID cipher table**: Not target-calibrated.

4. **Buffer filtering (MID-only)**: Architecturally target-motivated (designed knowing the dual constraint), not numerically calibrated.

5. **EVA character pool for Timm modification**: The 16-character EVA pool {a,c,d,e,h,i,k,l,m,n,o,q,r,s,t,y} is derived from the vocabulary generation structure. Is this target-aware? Each character has equal probability of replacement (1/16). The pool does not specifically increase the probability of -am suffixes or y-onset prefixes. The pool selection is not calibrated to any VMS positional metric. **Not a target-awareness concern.**

6. **Surprise check**: The best combination at cp=0.7, mp=0.4 achieves ss_mean=1.476, essentially matching VMS ss_mean (1.465). This is within natural simulation variance, but the proximity to VMS deserves scrutiny. At cp=0.7, mp=0.8, ss_mean=1.368 is 6.6% below VMS. The high-copying-probability + high-modification regime produces ss_mean values closely tracking VMS. Is this a coincidence? The mechanism is copying with ~71% onset preservation; the VMS ss_mean is ~1.465. The copy fraction at cp=0.7 means ~70% of MID tokens are copy-or-modified copies. The mathematical relationship: ss_mean grows approximately with sqrt(copy fraction × onset preservation). No numerical calibration was done — these are emerged properties of the parameter values tested.

---

## 9. LIMITATIONS

1. **Timm modification changes word length**: Insert/delete operations change word length by ±1 character. The EVA vocabulary distribution in this simulation was generated with make_word() having lengths roughly 5-9 chars. After a delete, some words will be shorter; after an insert, longer. This modestly affects get_onset() because the onset detection order checks multi-char prefixes first. A very short word (after multiple deletes through chain copying) might be mis-tokenized. This effect is small but not zero.

2. **No semantic content in EVA words**: The make_word() function generates phonetically plausible EVA strings but not the actual VMS vocabulary. The Timm modification on a generated EVA word may produce strings not in the VMS vocabulary at all. A more faithful test would operate on actual EVA word tokens from the VMS corpus.

3. **Character replacement distribution is uniform**: Real Timm/Schinner modification used substitutions from the same EVA alphabet frequency distribution, not uniform. If EVA character frequencies are non-uniform, the effective collision rate and onset-preservation rate would differ from the estimates here.

4. **Three VMS-viable combinations do not fully reproduce VMS values**: am_ll remains at 89.5–92.6% of VMS target; ss_mean at 86.4–93.4% of VMS. The mechanism enters the "not ruled out" zone under VMS-level adj_rate constraints but does not positively reproduce VMS measured values at any combination.

5. **A-dialect not tested**: Same limitation as exp_181.

---

## Self-Audit

**Target-awareness**: LL cipher table is explicitly calibrated to -am (inherited from exp_177); am_ll result is conditional on this calibration. LF cipher table is calibrated to y-onset. All three VMS-viable combinations still fall short of VMS am_ll and ss_mean targets. Result is stated as "not ruled out by this architecture" not as "positively reproduces VMS." The character pool for Timm modification is not calibrated to any VMS metric. No additional target-awareness concerns beyond the inherited LL/LF calibration already disclosed in exp_177 and carried forward.

**Feature-destroying implementation**: The Timm modification preserves onset class ~79% of the time (vs 0% in exp_180, 100% in exp_181). This is not feature-destroying. Insert-at-position-0 (~5.8% of all modifications) does destroy onset class; this is disclosed in the script docstring. The feature is not destroyed — it is partially degraded, which is the intended test.

**Extrapolation**: No "structural" or "cannot" claims are made. The result is stated as "8/36 combinations viable under tested parameter grid." The three VMS-viable combinations are stated as "the mechanism is not ruled out under these conditions" — no claim is made that the mechanism positively reproduces VMS or that the remaining gap (7.4–14% on am_ll, ss_mean) is bridgeable.

**Negative-result scope**: Positive result overall (8/36 viable). The three VMS-viable combinations make this a partially positive result for the specific adj_rate constraint, though am_ll and ss_mean remain below VMS values.

**Control behavior**: No external control corpus in this experiment. The "control" is the comparison to exp_180 (0/18) and exp_181 (4/36). Both behaved as expected based on theoretical predictions about onset preservation and collision rates. No surprising control behavior.

**Committed claim**: C004 contradiction condition is triggered. Writing to open_questions.md. Not updating findings.md.

---

## CONCLUSION (DEFERRED TO HUMAN)

exp_182 produces 8/36 viable combinations, with 3 achieving adj_rate at or below VMS level — the first such result in the experimental program. The mechanism is not ruled out by the VMS adj_rate constraint under Timm modification, though am_ll and ss_mean remain below VMS values at the VMS-viable adj_rate combinations.

This result triggers a C004 contradiction condition. **Loop stopped per SOUL.md behavioral constraints. See open_questions.md.**

---

## FILES

- `script.py`: Position-aware hybrid with Timm single-char modification (36 combinations × 50 sims = 1800 runs; 10-sim verification at best combo)
- `data/timm_char_results.json`: Raw results for all 1800 + 10 verification simulations
