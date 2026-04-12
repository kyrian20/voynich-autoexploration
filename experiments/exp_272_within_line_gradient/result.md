# exp_272: Within-Line Word Length Gradient

**Hypothesis**: H481 — VMS B-dialect shows a within-line word length gradient: words at high word-index within long lines are shorter than words at low word-index. This gradient is not captured by the simulation's position-agnostic buffer.

**Date**: 2026-04-11

---

## Results

### Gradient Coefficient Summary (linlen ≥ 8 lines, all words)

| Dialect | VMS slope | Sim slope | Gap | VMS r | Sim r |
|---------|-----------|-----------|-----|-------|-------|
| A | -0.0105 | -0.0014 | -0.0090 | -0.022 | -0.002 |
| B | **-0.0859** | -0.0161 | **-0.0698** | **-0.152** | -0.031 |

**H481 CONFIRMED for B-dialect**: B-dialect VMS shows a within-line word length gradient of -0.086 chars per word-index step. Over 10 words, this accumulates to -0.86 chars total gradient. The simulation slope is -0.016 (5× weaker), driven by LF/LL structure, not genuine within-line MID gradient.

**A-dialect shows no meaningful gradient**: VMS A slope = -0.011, and the MID-only slope is actually slightly POSITIVE (+0.016), indicating no within-line gradient in A-dialect MID words. This explains why A-dialect Menzerath r is captured by the simulation (A: sim r=-0.189 ≈ VMS r=-0.190) while B is not.

### MID-Only Gradient (excluding LF and LL, linlen ≥ 8)

| Dialect | VMS MID slope | Sim MID slope | Gap | VMS r | Sim r |
|---------|--------------|--------------|-----|-------|-------|
| A | +0.0155 | -0.0048 | +0.020 | +0.028 | -0.006 |
| B | **-0.0527** | -0.0009 | **-0.0516** | **-0.078** | -0.001 |

The MID-only analysis is decisive: Sim B MID slope = -0.001 (essentially zero, confirming position-agnostic buffer design). VMS B MID slope = -0.053 (58× larger). A-dialect shows no gradient in MID words.

### VMS B-Dialect Linlen 11+ Staircase (word-index × mean word length)

| idx | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|-----|---|---|---|---|---|---|---|---|---|---|----|----|
| VMS | 5.59 | 5.18 | 5.28 | 5.12 | 5.17 | 5.13 | 5.04 | 5.05 | 4.88 | 4.87 | 4.57 | 4.35 |
| Sim | 5.86 | 5.41 | 5.40 | 5.44 | 5.39 | 5.43 | 5.41 | 5.39 | 5.40 | 5.44 | 5.46 | 5.43 |

VMS B shows a clear monotone decline from idx1 onward (5.18 → 4.35, a drop of 0.83 chars). Simulation is essentially flat at 5.40–5.46 from idx1 onward.

### Normalized Position Quintile Means (excludes single-word and two-word lines)

| Quintile | VMS-A | Sim-A | VMS-B | Sim-B |
|----------|-------|-------|-------|-------|
| 0-20% | 5.229 | 5.539 | 5.557 | 5.643 |
| 20-40% | 5.084 | 5.075 | 5.494 | 5.415 |
| 40-60% | 5.208 | 5.062 | 5.460 | 5.420 |
| 60-80% | 5.327 | 5.046 | 5.366 | 5.417 |
| 80-100% | 5.324 | 5.665 | **5.125** | 5.491 |

VMS-B: monotone decline from 5.557 (first 20%) to 5.125 (last 20%) — total 0.432 char drop. Sim-B: last quintile goes UP (5.491) due to LL words being longer than MID (midfix adds +0.55 chars for B-LL). The gradient is opposite in direction for the last quintile: VMS-B ends shorter, Sim-B ends longer.

### Onset Composition by Word Index (VMS-B MID, linlen ≥ 8)

| Word idx | N | short_onset | other |
|----------|---|------------|-------|
| 1 | 1370 | 0.208 | 0.066 |
| 2 | 1370 | 0.223 | 0.054 |
| 3 | 1370 | 0.226 | 0.042 |
| 4 | 1370 | 0.239 | 0.056 |
| 5 | 1370 | 0.255 | 0.049 |
| 6 | 1370 | 0.242 | 0.061 |
| 7 | 1024 | 0.248 | 0.065 |
| 8 | 666 | 0.270 | 0.105 |
| 9 | 329 | 0.252 | 0.140 |
| 10 | 104 | 0.327 | 0.125 |

(short_onset = d, s, y, k, t, l, r, p, f, o — single-character onsets with shorter mean word length)

VMS B-dialect: short-onset fraction increases from 20.8% at idx1 to 32.7% at idx10 — a 57% relative increase. Simulation B: short-onset fraction is flat at 23.3-24.0% across all indices.

This onset composition shift is a key mechanistic contributor to the within-line gradient: words with shorter (single-char) onsets are more frequent at high word-index positions in VMS B-dialect.

---

## Interpretation

**H481 CONFIRMED**: The within-line word length gradient is real and B-dialect-specific.

Key numbers:
- VMS B MID slope: -0.053 chars/word-idx; Sim B MID slope: -0.001. Gap = 58×.
- VMS A MID slope: +0.016 (no gradient); A-dialect Menzerath r already matched by simulation.
- VMS B linlen 11+ staircase: 5.18 (idx1) → 4.35 (idx11), a drop of 0.83 chars across 10 positions.

**Why A-dialect doesn't need this**: A-dialect MID slope = +0.016 (slightly positive, near zero). The absence of a within-line gradient in A-dialect MID means the position-agnostic buffer is sufficient for Menzerath reproduction in A. B-dialect requires word-index-aware generation.

**Why the simulation has a non-zero slope for all words**: The all-words slope for sim B is -0.016, not zero. This comes from: LF words (idx0, ~5.86 chars) are always longer; as idx increases, LF words are replaced by MID (~5.42) and eventually LL (~5.56) in the mix. For very long lines, LL appears at high idx and is longer than MID. The MID-only slope of -0.001 confirms the buffer has essentially no within-line gradient.

**Onset composition gradient**: VMS B-dialect shows systematically more short-onset words at high word-index positions. This is an onset composition gradient, not just a word-length gradient. It suggests the underlying grammatical/lexical property is word-index-dependent onset selection — possibly related to how the VMS scribe selected function words (short onset, short word) to fill the ends of long lines, or a discourse structure where the ends of long lines use more common/short words.

**Architectural implication**: The simulation's position-agnostic buffer cannot reproduce this gradient by construction. The buffer draws from the same pool regardless of word index. Reproducing the gradient would require one of:
1. Word-index-aware buffer sampling (sample different onset classes at different positions within a line)
2. Onset-specific line-length targeting (short-onset words preferentially generated when line is long)
3. A word-frequency-gradient mechanism (common words shorter on average; common words placed at end of long lines)

The B-dialect Menzerath magnitude gap (-0.055 vs VMS -0.206) follows directly from the missing within-line gradient: the simulation produces lines with flat MID word length, while VMS B shows shortening toward line ends.

---

## Limitations

1. Onset composition gradient at idx ≥ 8 in linlen ≥ 8 lines: small N (N=329 at idx9, N=104 at idx10) — short-onset fraction at high indices may have noise.
2. The within-line gradient in VMS B could reflect a composition effect (long B-dialect lines appear in particular sections with shorter words) rather than genuine within-line grammar. Section stratification not done.
3. The mechanism that produces the onset composition gradient is unknown — whether it's discourse structure, lexical frequency, rhythmic constraint, or grammatical rule is unresolved.
4. Full 19-metric battery not updated in this experiment.

---

## Self-Audit

**Target-awareness**: No target-aware elements. This is a pure corpus measurement experiment. No parameters were calibrated to a VMS gradient target. The simulation parameters are from exp_270/exp_257 architectures, calibrated to different metrics.

**Feature-destroying implementation**: Not applicable. This is a characterization study, not a mechanism test. The simulation's position-agnostic buffer is by design — we're measuring the gap, not attempting to reproduce it. No implementation detail destroys the feature under analysis.

**Extrapolation**: The statement "the position-agnostic buffer cannot reproduce the within-line gradient" is a logical claim, not extrapolation from a parameter sweep. The MID buffer samples from a fixed distribution regardless of word index — this is a structural property of the design, and the MID-only slope of -0.001 confirms it empirically. No parameter tuning of the current architecture could produce word-index-dependent length gradients without fundamentally changing how MID words are generated.

**Negative-result scope**: N/A — H481 is a positive result (gradient confirmed). No negative results about mechanisms in this experiment.

**Control behavior**: The simulation serves as a position-agnostic null model. Expected: essentially flat MID word length across all word indices (by construction of the buffer). Actual: MID slope = -0.001 (Sim B) and -0.005 (Sim A) — consistent with expectation. The simulation behaves exactly as expected; the VMS deviation from this flat baseline is the signal.

---

## Conclusion

**H481 CONFIRMED**: VMS B-dialect shows a robust within-line word length gradient. MID words at high word-index positions are shorter (slope = -0.053 chars/word-idx; over 10 positions: -0.53 chars total). A-dialect shows no gradient (MID slope = +0.016). The simulation is flat for both dialects (MID slope ≈ -0.001). The onset composition gradient is a secondary finding: short-onset words (single-char onsets) increase from 20.8% to 32.7% across word indices 1–10 in VMS B-dialect MID, while the simulation stays flat at 23–24%. This confirms H481 and explains why B-dialect Menzerath magnitude gap (-0.055 vs VMS -0.206) is architectural — the simulation's position-agnostic buffer cannot produce position-dependent MID word length gradients by construction.
