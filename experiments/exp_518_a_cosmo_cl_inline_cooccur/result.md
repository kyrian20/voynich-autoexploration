# exp_518 result — A cosmo CL survey (proper dialect filter) + inline co-occurrence tests

## Section sizes
- A cosmo (A-dialect only, n=85-102): **10 folios, 296 lines, 286 pairs**
- A herbal_a (A-dialect only, n≤56): **44 folios, 966 lines**

Note: exp_512 used n=85-102 WITHOUT is_b_dialect filter → included B-dialect folios 85, 86, 94, 95 in "A cosmo". This experiment corrects that.

---

## Part 1: F492 validation (ch→ok A cosmo CL)

| Pair | obs | exp | E | flag |
|------|-----|-----|---|------|
| ch→ok | 9 | 5.26 | 1.71× | — |
| ok→ch | 6 | 5.26 | 1.14× | — |
| ch→ch | 9 | 12.55 | 0.72× | — |

**F492 survives but weakened**: E drops from 2.01× (exp_512, contaminated) to 1.71× (corrected, A-dialect only). N drops from 12 to 9. Does not meet CONF threshold (E≥1.5 AND N≥10). Directional but below standard thresholds.

## Part 2: New A cosmo CL findings

Top enriched pairs (proper A-dialect filter):

| A→B | obs | exp | E | flag |
|-----|-----|-----|---|------|
| cth→cth | 4 | 0.55 | 7.25× | (dir) |
| cth→ol | 3 | 0.51 | 5.89× | (dir) |
| ok→a | 3 | 0.76 | 3.93× | (dir) |
| qok→qok | 3 | 0.84 | 3.59× | (dir) |
| t→d | 3 | 0.94 | 3.19× | (dir) |
| s→sh | 4 | 1.28 | 3.13× | (dir) |
| ch→ol | 5 | 2.43 | 2.06× | dir |

cth→cth and cth→ol are very strong (E≥5×) despite small N. qok→qok in A cosmo mirrors the B astro qok→qok (F495).

---

## Part 3: H_new_DA — ot-LF pos1+pos2=y co-occurrence (A herbal_a)

- ot-LF lines (len≥3): N_elig=40
- pos1=y baseline: 0.148; pos2=y baseline: 0.028
- ot-LF pos1=y: obs=9, E=1.52×
- ot-LF pos2=y: obs=4, E=3.60×
- ot-LF BOTH pos1=y AND pos2=y: obs=2, exp=0.90, **E_cooccur=2.22×**

**POSITIVE but weak**: Individual rules confirmed (pos2=y strongly enriched at 3.60×). Co-occurrence is above 1 (E=2.22×) but N=2 is very small — insufficient to confirm. H_new_DA: directional co-occurrence, N too small for confirmation.

---

## Part 4: H_new_DB — cth-LF pos2=qot AND pen=d co-occurrence (A herbal_a)

- cth-LF lines (len≥3): N_elig=64
- pos2=qot: obs=5, E=2.59×
- pen=d: obs=18, E=1.60×
- BOTH pos2=qot AND pen=d: obs=1, exp=1.41, **E_cooccur=0.71×**

**NEGATIVE**: pos2=qot and pen=d are NOT co-occurring in cth-LF lines — they are slightly anti-correlated (E=0.71×). Consistent with exp_493 (cth pos2+pen independent, E=0.76×). H_new_DB **CLOSED NEGATIVE**.

---

## Summary

| Question | Result |
|----------|--------|
| F492 (ch→ok A cosmo CL) | Weakened: E=1.71×/N=9 (was E=2.01×/N=12); below CONF; directional |
| cth→cth A cosmo CL | NEW: E=7.25×/N=4 (dir) |
| cth→ol A cosmo CL | NEW: E=5.89×/N=3 (dir) |
| qok→qok A cosmo CL | NEW: E=3.59×/N=3 (dir) |
| H_new_DA (ot-LF pos1+pos2=y) | Directional E=2.22×, N=2 — too small to confirm |
| H_new_DB (cth-LF pos2+pen co-occur) | NEGATIVE: E=0.71× (independent, consistent with exp_493) |

## Self-Audit

**Target-awareness**: No target-aware elements identified. This experiment is a purely statistical survey of corpus co-occurrence patterns with no calibration to VMS target metrics.

**Feature-destroying implementation**: No feature-destroying implementation details identified. The B-dialect filter correction is the key design element — it ensures "A cosmo" is actually A-dialect only, which is what the experiment is designed to test.

**Extrapolation**: All claims are within the tested parameter range. H_new_DB is closed as "NEGATIVE" scoped specifically to cth-LF lines in A herbal_a with the tested co-occurrence definition. No "structural" or "impossible" language used.

**Negative-result scope**: H_new_DB: "pos2=qot and pen=d do not co-occur above baseline in cth-LF lines in A herbal_a (E=0.71×)." Scoped to this section and this test. F492: "ch→ok is directional (E=1.71×/N=9) but below CONF threshold after contaminated folios removed." Not claimed as disproven — correctly stated as weakened.

**Control behavior**: No external controls used. Null model is base_A × base_B × N (independence baseline). Expected behavior under independence: E=1.0×. cth-LF BOTH: E=0.71× (slightly below independence, consistent with independent rules). No surprises.
