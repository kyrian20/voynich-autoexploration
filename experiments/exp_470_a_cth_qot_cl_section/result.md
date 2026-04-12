# exp_470: A cth→qot CL Section-Specificity and Body-Conditional Driver

**Question (H_new_AI):** Is the A cth→qot CL (E=2.07×/N=7 in exp_465) section-specific like cth→sh (herbal_a-concentrated)? What is the body-class driver?

---

## Results

**A-dialect total CL pairs: 1,314. A cth-class LL pairs: N=105** (cth+ckh+cph combined).

### A cth-LL → next LF onset profile (N=105)

| onset | obs | exp | E |
|-------|-----|-----|---|
| sh | 12 | 8.31 | 1.44× |
| qot | 9 | 5.11 | 1.76× |
| ok | 8 | 5.19 | 1.54× |
| ol | 3 | 1.92 | 1.56× |
| l | 2 | 0.72 | 2.78× (dir, N=2) |
| ch | 11 | 9.35 | 1.18× |
| d | 16 | 18.14 | 0.88× |
| y | 12 | 16.38 | 0.73× |

Most elevated (excluding trivial N=1-2): qot(1.76×/N=9), sh(1.44×/N=12), ok(1.54×/N=8).

### cth→qot CL section breakdown

| section | cth_N | →qot | section qot% | E |
|---------|-------|------|--------------|---|
| herbal_a | 87 | 9 | 7.0% | **1.48×** |
| cosmo | 18 | 0 | 0.3% | 0.00× |
| stars | 0 | 0 | 0.8% | — |
| herbal_b | 0 | 0 | — | — |

**cth-class LL words are 83% herbal_a (87/105). All 9 qot cases are in herbal_a.** Within herbal_a, the section-specific E = 1.48× (9/(87×0.070) = 1.48×) — **below confirmation threshold**.

### cth→qot word inventory (N=9)

All 9 cases from distinct folios (f4r, f10r, f15v, f29v, f30v, f35r, f36r, f37v, f56r) — 9 unique word pairs:
- LL words: cth, cthy(×2), cthod, cthor, cthory, cthols, cphey, cphaiin
- LF words: qotchor(×2), qotchey, qotcho, qotchy, qotol(×2), qotchoiin
- All LF words are qot-onset (expected — these are the LF words in qot-LF herbal_a lines)

### Body-class driver (cth→qot)

Overall cth→qot rate: 8.6% (9/105)

| body | total | →qot | rate | E |
|------|-------|------|------|---|
| aiin | 7 | 1 | 14.3% | 1.67× (dir) |
| ol | 9 | 0 | 0% | 0.00× |
| edy | 1 | 0 | — | — |
| other | 88 | 8 | 9.1% | 1.06× |

**No body-class driver** for cth→qot. The "other" class (no special suffix) carries 8/9 cases at baseline.

### cth→sh comparison

| section | cth_N | →sh | section sh% | E |
|---------|-------|-----|-------------|---|
| herbal_a | 87 | 9 | 8.9% | 1.16× |
| cosmo | 18 | 3 | 5.8% | 2.85× (dir) |

Note: Including ckh/cph in cth-class (N=105) slightly dilutes the cth-specific signal vs exp_465's cth-only analysis (N smaller). The cosmo sh-directional finding from exp_465 (N=3, E=4.0×) is replicated (E=2.85×, N=3).

---

## Interpretation

**H_new_AI ANSWERED (section composition artifact, not selective coupling):**

The apparent A cth→qot CL enrichment (E=1.76× overall) is explained by:
1. **cth-class is a herbal_a phenomenon**: 87/105 = 83% of cth LL pairs are from herbal_a
2. **herbal_a has elevated qot-LF rate**: 7.0% qot at LF in herbal_a vs ~4.9% A-overall
3. **Within herbal_a, cth→qot is NOT selectively elevated**: section-specific E = 1.48× (below 1.5× directional threshold relative to N=9)

The **cth→qot is a section-composition effect**, not a genuine selective coupling. The prior E=2.07×/N=7 in exp_465 reflected using the A-overall qot-LF baseline against what is effectively a herbal_a subsample.

**No body-class driver**: Unlike cth→sh (which has an o-body elevation from exp_465: E=2.31×/N=6), cth→qot shows no body-class specificity.

**Diversity confirms real data**: 9 unique folios, 9 unique word pairs, 8 unique LL words — this is not a single-phrase repeat. The qot-LF words are the normal herbal_a qot vocabulary (qotchor, qotchey, qotcho).

**cth-class geographical summary**: cth-onset words appear almost exclusively in A herbal_a. Stars, cosmo (except for the 18 pairs = folio boundary effects), herbal_b, and other_a have near-zero cth-LL contributions. This confirms cth as a herbal_a-specific onset class, consistent with prior work (exp_449, exp_465).

---

## Self-Audit

**Target-awareness**: None. Section-specific baselines computed from corpus without reference to expected outcomes.

**Feature-destroying implementation**: Locus stripping corrected (vs initial buggy version) using `lstrip('+*=/~&')` matching exp_465's working implementation. Onset priority list includes cth+ckh+cph as the cth-class.

**Extrapolation**: cth→qot herbal_a E=1.48×/N=9 — correctly characterized as below threshold. No claim of confirmation.

**Negative-result scope**: "cth→qot is not a selective CL coupling" is specific to the CL level. Within-line cth usage in herbal_a remains valid. The herbal_a qot-LF elevation (F445) is real — cth just inherits it by concentration.

**Control behavior**: Section-specific baselines (herbal_a qot-LF = 7.0%) vs A-overall (4.87%) both computed from corpus. The difference explains the apparent elevation.

---

## Conclusion

**H_new_AI ANSWERED (section-composition artifact):** A cth→qot CL (apparent E=1.76×/N=9) is not a genuine selective coupling — it reflects cth being an 83% herbal_a class (which has elevated qot-LF baseline). Within herbal_a, cth→qot E=1.48× (below threshold). No body-class driver found. No new finding ID.

**F445 stands as written** — it included cth→sh as a herbal_a coupling (exp_465 E=1.5×/N=9), not cth→qot. The current result confirms cth→qot should NOT be added to F445.

**Follow-up**: The cosmo cth→sh directional (N=3, E=2.85×) is consistent across exp_465 and exp_470 — remains directional (N too small for confirmation, and cosmo has very few cth-LL pairs total).
