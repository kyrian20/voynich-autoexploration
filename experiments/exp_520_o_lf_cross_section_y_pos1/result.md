# exp_520 result — o-LF pos1=y cross-section survey + ol-LF scope + ot-LF pos2=y scope

## H_new_EB: o-LF pos1=y complete cross-section survey

| Section | N_elig | obs | exp | E | base_y | threshold |
|---------|--------|-----|-----|---|--------|-----------|
| A herbal_a (1-56) | 28 | 9 | 3.98 | 2.26× | 0.142 | dir |
| A stars (57-72) | 13 | 6 | 2.60 | 2.31× | 0.200 | **dir NEW** |
| A cosmo (85-102) | 15 | 4 | 2.67 | 1.50× | 0.178 | below-CONF |
| B herbal (1-72 B) | 17 | 4 | 3.43 | 1.17× | 0.201 | flat |
| B astro (73-84 B) | 19 | 3 | 1.14 | 2.63× | 0.060 | (dir) |
| B pharma (103-116 B) | 40 | 7 | 6.94 | 1.01× | 0.174 | flat |
| B cosmo (85-102 B) | 14 | 2 | 2.50 | 0.80× | 0.178 | depleted |

**Key findings:**
- **A herbal_a**: E=2.26×/obs=9 (dir) — confirmed, consistent with F502 inline result (E=2.17×)
- **A stars**: E=2.31×/obs=6 (dir) — **NEW**. A stars (57-72 A-dialect) has y specifically elevated for o-LF. This is the first confirmed pos1 signal found in A stars (exp_501 found no confirmed pos1 rules in A stars). Note: A stars y@pos1 baseline is elevated (20%) vs A herbal_a (14.2%), yet E=2.31× is genuine.
- **B astro**: E=2.63×/obs=3 ((dir)) — consistent with H_new_EA inline test (E=2.55×). Confirmed as genuine.
- **B pharma**: E=1.01×/obs=7 — conclusively FLAT. The largest B section tested.
- **B herbal**: E=1.17×/obs=4 — flat.
- **B cosmo**: E=0.80×/obs=2 — flat/depleted.

**Scope pattern**: o-LF pos1=y is confirmed in A herbal_a, A stars, B astro — but absent in B herbal, B pharma, B cosmo. The pattern does NOT split cleanly by A/B dialect. Within A-dialect: confirmed in herbal AND stars but absent in cosmo. Within B-dialect: confirmed only in astro. This suggests a **content-type dependency**: the rule appears to be active in *herbal* (A herbal_a) and *astronomical/stars* (A stars, B astro) content, but absent from pharmaceutical (B pharma) and pharmacological-adjacent sections.

**Control check**: ok-LF pos1=y in A stars (BONUS table): obs=1/N_elig=9, E=0.56× — DEPLETED. This confirms that A stars is not simply a high-y-opening section for all LF classes. The o-LF enrichment is class-specific.

---

## H_new_EC: ol-LF pos1=y cross-section survey

| Section | N_elig | obs | exp | E | threshold |
|---------|--------|-----|-----|---|-----------|
| A herbal_a | 20 | 5 | 2.84 | 1.76× | below dir (E<2.0) |
| A stars | 6 | 2 | 1.20 | 1.67× | below threshold |
| A cosmo | 10 | 1 | 1.78 | 0.56× | depleted |
| B herbal | 13 | 3 | 2.62 | 1.15× | flat |
| B astro | 101 | 7 | 6.06 | 1.15× | flat |
| B pharma | 40 | 6 | 6.94 | 0.86× | flat |
| B cosmo | 16 | 2 | 2.85 | 0.70× | flat |

**ol-LF pos1=y conclusion**: The prior borderline reading (E=1.68×/obs=5 in inline test) is approximately consistent with E=1.76×/obs=5 here (different A herbal_a boundary definition affects baseline slightly). Neither meets dir (E<2.0) or (dir) (E<2.5) threshold. **ol-LF pos1=y is not confirmed at any threshold in any section.** All other sections are flat.

**Note on B astro**: B astro has N_elig=101 ol-LF lines — the largest ol-LF sample in the corpus. E=1.15×/obs=7 is a well-powered negative (with 101 lines, we'd expect about 6 obs under baseline; 7 observed is near-perfect null). This is a strong confirmation that ol-LF has no pos1=y rule in B astro despite o-LF having one.

---

## H_new_ED: t-LF positional profile in A stars

A stars (57-72 A-dialect) contains only N_elig=2 t-LF lines (len≥3). This is insufficient to test the hypothesis. The "t-LF dominant A stars section" (F446) must refer to a broader definition of A stars that captures more folios (possibly including folios currently classified as B-dialect or not yet fully parsed). **H_new_ED is unanswerable with the current corpus definition of A stars.** No findings.

---

## H_new_EE: ot-LF pos2=y cross-section scope

| Section | N_elig | obs | E | threshold |
|---------|--------|-----|---|-----------|
| A herbal_a | 40 | 4 | 3.60× | (dir) |
| A stars | 9 | 1 | 2.71× | below (obs<3) |
| A cosmo | 14 | 0 | 0.00× | absent |
| B herbal | 11 | 1 | 2.24× | below (obs<3) |
| B astro | 30 | 0 | 0.32× | absent |
| B pharma | 72 | 2 | 1.67× | below (dir) |
| B cosmo | 15 | 1 | 1.03× | flat |

**ot-LF pos2=y conclusion**: Remains A herbal_a-specific at (dir) level (E=3.60×/obs=4). N=4 is one below dir threshold (obs≥5). In all other sections, obs is 0-2 — too small for any threshold. The rule does not extend broadly. A herbal_a remains the only confirmed location of this signal.

**A herbal_a ot-LF pos2 distribution** (most elevated classes):
- ch: 11/40 = 27.5%, E=0.80× (depleted — consistent with F498)
- k: 5/40, E=2.07× (dir — consistent with F498)
- y: 4/40, E=3.60× ((dir) — consistent with exp_519)
- a: 4/40, E=3.23× (new signal? N=4 meets (dir) if E≥2.5)

**New observation**: ot-LF pos2=a appears elevated (E=3.23×/obs=4 → (dir) threshold: E≥2.5×/obs≥3). Not previously noted. 'a' is a rare onset class. This might be a genuine signal or a small-N artifact. Flag for follow-up.

---

## Methodological note: A herbal_a definition

This experiment used A herbal_a = folios 1-56 A-dialect (exp_511/519 methodology). Some prior findings (F455, F456) were established with experiments that may have used different A herbal_a boundaries. The ok-LF pos1=y result in exp_520 (E=1.38×/obs=9/N_elig=46) is lower than F455's value (E=1.62×/obs=12/N_elig=53). The discrepancy is consistent with F455 having included A stars folios (57-72) in "A herbal_a." This is an open methodological question that should be addressed in a dedicated audit experiment, but does not affect the current experiment's findings.

---

## Self-Audit

**Target-awareness**: No target-aware elements identified. The o-LF pos1=y signal is a corpus measurement, not a simulation parameter.

**Feature-destroying implementation**: The is_b_dialect bug (originally using `re.match(r'^(e+dy|e+edy)$')` instead of `w.endswith('edy')`) would have misclassified B-dialect folios as A-dialect, inflating A sections with B content. Fixed before analysis. No feature-destroying implementation in the corrected script.

**Extrapolation**: A stars finding (E=2.31×/obs=6 dir) is within threshold. No extrapolation beyond measured values. The content-type dependency interpretation ("herbal and astronomical sections") is a descriptive summary of the observed pattern, not a causal claim.

**Negative-result scope**: B pharma flat at E=1.01×/obs=7 is a well-powered negative. B herbal (obs=4, E=1.17×) and B cosmo (obs=2, E=0.80×) are lower-powered negatives. The claim is "o-LF pos1=y is absent in B pharma and B herbal" — this is within scope given the observed data.

**Control behavior**: Null model = E≈1.0× (uniform baseline). B pharma achieves E=1.01× — within 1% of null. A cosmo (E=1.50×/obs=4) is near-threshold — consistent with a borderline borderline null (marginally elevated but not confirmed).

## Summary

| Hypothesis | Result |
|-----------|--------|
| H_new_EB: o-LF pos1=y cross-section | dir in A herbal_a + A stars (NEW) + (dir) in B astro. FLAT in B herbal, B pharma, B cosmo. A cosmo borderline (1.50×). Pattern: content-type (herbal+astronomical) not dialect. |
| H_new_EC: ol-LF pos1=y cross-section | NOT confirmed anywhere. A herbal_a E=1.76×/obs=5 (below dir). B astro N=101 ol-LF lines flat (E=1.15×) — strong null. ol-LF pos1=y is a borderline signal in A herbal_a only. |
| H_new_ED: t-LF A stars profile | UNANSWERABLE: A stars (57-72) has only N_elig=2 t-LF lines. |
| H_new_EE: ot-LF pos2=y scope | A herbal_a-specific at (dir) E=3.60×/obs=4. Absent elsewhere. NEW: pos2=a also elevated (E=3.23×/obs=4, (dir)). |
