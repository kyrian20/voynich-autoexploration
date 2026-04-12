# exp_477: A/B t-LF pos1 Inversion Verification

**Question:** Does A dialect route t-LF → o-gallows (ot/ol) at pos1 while B dialect routes t-LF → template class (qok) at pos1? (H_new_AN)

---

## Results

### Corpus sizes (t-LF lines available)

| Section | Total lines | t-LF lines |
|---------|-------------|------------|
| A herbal_a | 975 | 28 |
| A cosmo | 336 | 7 |
| A stars | 130 | 1 |
| B herbal | 269 | 4 |
| B astro | 700 | 3 |
| B cosmo | 119 | 5 |
| B pharma | 799 | 11 |

**Critical finding:** B herbal has only N=4 t-LF lines in this corpus — prior experiment (exp_472) appeared to find N=37 using different corpus parsing or dialect classification. The hypothesis was based on evidence that cannot be reproduced at current parsing standards. Most B sections are below directional threshold (N≥5).

---

### A herbal_a t-LF pos1 routing (N=28)

| onset | obs | exp | E |
|-------|-----|-----|---|
| o | 5 | 2.4 | 2.12× (dir) |
| sh | 4 | 2.4 | 1.66× |
| d | 5 | 4.7 | 1.06× |
| ot | 0 | 1.5 | 0.00× |
| ol | 1 | 0.4 | 2.49× (N=1) |
| qok | 1 | 1.8 | 0.54× |

**o-class (broad) elevated at pos1: E=2.12×/N=5 (dir).** The A herbal_a t-LF pos1 elevation is for bare `o`-onset words (or/ol/etc. classified as `o` after priority stripping), not specifically ot or ol individually. ot is depleted (0/28). qok is depleted.

---

### B pharma t-LF pos1 routing (N=10 with ≥2 words)

| onset | obs | exp | E |
|-------|-----|-----|---|
| **t** | **3** | **0.4** | **7.99× (dir)** |
| ok | 2 | 0.6 | 3.63× |
| ch | 1 | 0.6 | 1.74× |
| qok | 0 | 0.6 | 0.00× |
| ot | 0 | 0.2 | 0.00× |
| ol | 0 | 0.5 | 0.00× |

**NEW(dir): B pharma t-LF → t at pos1 (E=7.99×/N=3).** t-chains appear in B pharma t-LF lines: the first word of the line also begins with t-onset. qok depleted. LF words: teor, teedaram, tchodaiin, tar, tarairy, teedu, teedar, taram, toky, tainary, teeodaiin — diverse B pharma t-words across 11 folios (f103v–f115v).

---

### B astro t-LF (N=3 — too small)

qok at pos1: E=3.13×/N=2. Too small to interpret.

---

### B herbal/cosmo t-LF (N=4 and N=5 — too small)

No testable signal. N below directional threshold.

---

## Interpretation

**H_new_AN ANSWERED (insufficient N, hypothesis not confirmed):**

The A/B t-LF pos1 inversion hypothesis (A→ot/ol, B→qok) is not supported at current corpus parsing standards:

1. **A herbal_a (N=28):** broad o-class elevated (E=2.12×/N=5, dir), NOT specifically ot/ol. ot is depleted (0/28). The prior evidence for A→ot/ol came from exp_471 (A herbal_a t-LF→ol 4.51×/dir, N=1) and exp_472 (A cosmo→ot/ol, dir) with small N that do not survive the current analysis.

2. **B herbal (N=4):** too small. exp_472's N=37 cannot be reproduced — the N discrepancy is large and likely reflects different dialect classification (some B-herbal folios classified as A in current parsing due to folio-level edy-rate boundary effects).

3. **B pharma (N=11, best B section available):** t-self at pos1 (E=7.99×/N=3, dir) — NOT qok, NOT ot/ol. A t-chain structure dominates in pharma t-LF lines.

**The hypothesis as stated is NOT reproducible** at N≥5 directional threshold for the A→ot/ol direction, and the B data does not support the qok→pos1 claim at any testable N.

**NEW directional finding (not threshold-crossing):** B pharma t-LF → t at pos1 (E=7.99×/N=3, dir). This extends the t-chain observation to B pharma t-LF lines: when a B pharma line ends with t, it often begins with t as well. This may link to t-chain structures in pharma (parallel to l-chain F423).

---

## Self-Audit

**Target-awareness:** No target-aware elements identified. Baselines are section-specific corpus frequency distributions, not calibrated to any VMS metric target.

**Feature-destroying implementation:** Onset priority list applied correctly; `o` is positioned after `ok`/`ot`/`ol`/`ol` in priority, so words classified as `o` are genuinely bare-o words. The 5 `o`-onset words at pos1 in A herbal_a t-LF lines are genuine o-class, not misclassified ot/ol. No feature-destroying implementation details identified.

**Extrapolation:** All claims are within tested range. "Cannot be confirmed" and "not supported" refer to the current corpus/parsing — not to all possible parsings or corpus definitions. The N discrepancy between exp_472 (B herbal t-LF N=37) and current (N=4) is acknowledged explicitly in result. No "structural/cannot/impossible/fundamental" claims made about the hypothesis itself.

**Negative-result scope:** The negative conclusion ("H_new_AN not confirmed") is scoped to: current parsing standards (folio-level dialect classification with edy-rate ≥5% threshold), current corpus (ZL3B eva_zl3b.txt with P-line filtering), and current N levels. The hypothesis COULD be re-tested with a different dialect classifier that correctly includes all B-herbal folios. The result says "cannot be confirmed at current N levels" — not "the inversion does not exist."

**Control behavior:** No control distributions used. This is a within-corpus frequency analysis. N/A.

---

## Conclusion

**H_new_AN ANSWERED (negative/insufficient):** A/B t-LF pos1 inversion cannot be confirmed at current N levels. A herbal_a shows broad o-class at pos1 (E=2.12×/N=5, dir) but NOT specifically ot/ol. B sections have N≤5 except pharma (N=11) which shows t-self at pos1 (E=7.99×/N=3, dir) rather than qok. **No finding ID assigned.** NEW(dir): B pharma t-LF → t at pos1 (E=7.99×/N=3).
