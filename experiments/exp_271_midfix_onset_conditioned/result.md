# exp_271: Onset-Conditioned Midfix Sampling

**Hypothesis**: H480 — Onset-conditioned midfix sampling will prevent B-LL over-correction and improve B-dialect Menzerath toward -0.206.

**Date**: 2026-04-11

---

## Results

### Menzerath r and Position Lengths (Three-Way Comparison)

| Dialect | Metric | exp_268 (no midfix) | exp_270 (pos midfix) | exp_271 (onset-cond) | VMS |
|---------|--------|--------------------|-----------------------|----------------------|----|
| A | r | +0.078 | -0.189 | **-0.183** | -0.190 |
| A | LF | 4.708 | 5.839 | 5.831 | 5.447 |
| A | LL | 4.775 | 5.933 | 5.940 | 5.403 |
| B | r | +0.097 | -0.052 | **-0.055** | -0.206 |
| B | LF | 4.857 | 5.867 | 5.912 | 5.732 |
| B | LL | 4.947 | 5.561 | 5.529 | 5.015 |

**H480 DISCONFIRMED**: Onset conditioning does not substantially improve over position-agnostic midfix (exp_270). B-LL: 5.529 (onset-cond) vs 5.561 (pos-agnostic) vs 5.015 (VMS) — the over-correction of +0.51 chars is nearly identical. B-dialect Menzerath r = -0.055 (onset-cond) vs -0.052 (pos-agnostic) — essentially identical.

A-dialect remains essentially perfect (r=-0.183 vs VMS=-0.190). Battery word_len_mean: A=101.4%, B=101.1% — both PASS.

---

## Why Onset-Conditioning Doesn't Help

The B-LL onset-conditioned expected additions per onset class:

| Onset | N | Non-empty | Mean_ne | Expected_add |
|-------|---|-----------|---------|--------------|
| d | 158 | 0.253 | 2.70 | 0.684 |
| ch | 181 | 0.757 | 2.44 | 1.845 |
| ol | 109 | 0.413 | 1.69 | 0.697 |
| ok | 104 | 0.423 | 2.25 | 0.952 |
| o | 95 | 0.789 | 2.00 | 1.579 |
| ot | 111 | 0.441 | 2.27 | 1.000 |

Even d-onset B-LL (the shortest onset class with mean word length 4.1 in VMS) gets +0.684 chars, far more than needed. The ch-onset midfix is very large (+1.845 chars). The onset-conditioned B-LL midfix distribution correctly models VMS B-LL words WITH complex midfixes, but the simulation draws these midfixes and applies them at a rate that over-inflates mean word length.

The key insight: even with onset conditioning, the midfix distribution is too aggressive for B-LL because B-LL needs LESS midfix correction than the data suggests. VMS B-LL is already SHORT (5.015 chars, the shortest position in B-dialect), and the no-midfix simulation is already close (4.947 chars, Δ=0.068). The midfix correction overshoots by 7-8× what is needed.

---

## Root Cause of B-Dialect Menzerath Under-Magnitude

The deeper issue (not solved by onset conditioning): VMS B-dialect shows within-line word length gradient that the simulation cannot reproduce.

From the bucket data: VMS shows steep decline at long lines (linlen 9–14: mean drops to 4.3–5.2 chars). Simulation stays nearly flat (5.4–5.6 chars). This within-line gradient is NOT captured by the position-agnostic buffer:
- In VMS: words at positions 10, 11, 12 within a 14-word line are shorter than words at position 3
- In simulation: all MID words drawn from the same buffer with same mean; no word-index-within-line gradient

This within-line gradient (possibly reflecting discourse structure, rhythmic patterns, or frequency effects where common short words fill the ends of long lines) is a new architectural gap. It produces stronger Menzerath correlation in VMS than the simulation's position-agnostic MID generation can match.

**New hypothesis generated**: H481 — VMS B-dialect shows a within-line word length gradient: words at high word-index within long lines are shorter than words at low word-index. This within-line gradient (measured from VMS corpus) is not captured by the simulation's position-agnostic buffer.

---

## Conclusions

1. **A-dialect midfix works**: r=-0.183 (vs VMS -0.190), essentially perfect, consistent across exp_270 and exp_271.
2. **B-dialect midfix achieves correct direction**: r=-0.055 (vs VMS -0.206); 30/30 runs negative. Magnitude gap is architectural, not calibration-related.
3. **Onset conditioning does not help for B-dialect**: the over-correction is not onset-specific; it's a general B-LL issue.
4. **Preferred implementation**: exp_270's position-agnostic midfix (simpler code, essentially same result).

---

## Self-Audit

**Target-awareness**: No target-aware elements. Midfix distributions are empirical from VMS.

**Feature-destroying implementation**: No feature-destroying details. The onset-conditioned midfix correctly conditions on the same onset sampled by cipher_lf/cipher_ll, preserving the onset distribution.

**Extrapolation**: No extrapolation. "Onset conditioning does not help for B-dialect" applies specifically to B-LL under these conditions. A-dialect is not affected.

**Negative-result scope**: H480 is DISCONFIRMED: onset-conditioned midfix does NOT improve B-dialect Menzerath relative to position-agnostic midfix (exp_270). The valid conclusion is: "onset conditioning of midfix does not close the B-LL word length gap; the over-correction is not onset-class-specific."

**Control behavior**: A-dialect serves as a control (unchanged from exp_270), confirming the onset-conditioning doesn't break what already worked.

---

## Conclusion

**H480 DISCONFIRMED**: Onset-conditioned midfix gives essentially the same B-dialect results as position-agnostic midfix (exp_270). The B-LL over-correction is not onset-dependent. Preferred implementation: exp_270's approach (simpler, same result). The B-dialect Menzerath magnitude gap (sim -0.055 vs VMS -0.206) is an architectural limitation — the simulation's position-agnostic buffer doesn't produce within-line word length gradients present in VMS B-dialect. New architectural gap identified: within-line word length gradient (H481).
