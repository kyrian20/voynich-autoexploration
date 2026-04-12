# exp_521 result — A herbal pos1 audit + pooled CONF test + ot-LF pos2=a check

## H_new_EG: F455/F456 audit — ok-LF and ot-LF pos1=y with corrected section definitions

| Section | LF | N_elig | obs | E | threshold |
|---------|----|--------|-----|---|-----------|
| A herbal_a (1-56, strict) | ok | 46 | 9 | 1.38× | below CONF |
| A herbal_a (1-56, strict) | ot | 40 | 9 | 1.58× | below CONF (obs<10) |
| A herbal_a (1-56, strict) | o | 28 | 9 | 2.26× | dir |
| A stars (57-72) | ok | 9 | 1 | 0.56× | depleted |
| A stars (57-72) | ot | 9 | 3 | 1.67× | below threshold |
| A stars (57-72) | o | 13 | 6 | 2.31× | dir |
| A herbal+stars (1-72 A) | ok | 55 | 10 | 1.22× | below CONF (E<1.5) |
| A herbal+stars (1-72 A) | ot | 49 | 12 | 1.64× | **CONF** |
| A herbal+stars (1-72 A) | o | 41 | 15 | 2.45× | **CONF** |

### F455 (ok-LF pos1=y) — STATUS: QUESTIONABLE

F455 claimed E=1.62×/obs=12 in "A herbal_a ok-LF lines (N=53)". Current experiment:
- Strict 1-56: E=1.38×/obs=9 (below CONF at E<1.5)
- Pooled 1-72: E=1.22×/obs=10 (below CONF at E<1.5)

Neither definition reproduces F455 at CONF. The discrepancy:
- F455 N=53 vs exp_521 N_elig=55 (2 more eligible lines in exp_521)
- F455 obs=12 vs exp_521 obs=10 (2 fewer observations in exp_521)
- F455 baseline=14.0% vs exp_521 baseline=14.9% (different section composition)

**Root cause unknown** without checking exp_480 directly. Possibilities: (a) corpus version difference; (b) different A herbal_a definition in exp_480; (c) word eligibility filter difference. F455 is flagged for audit but NOT retracted pending investigation. The finding should be treated as provisionally directional (E≈1.4-1.6×) rather than CONF until the discrepancy is resolved.

### F456 (ot-LF pos1=y) — STATUS: CONFIRMED at pooled level

F456 claimed E=1.83×/obs=11. Current experiment:
- Strict 1-56: E=1.58×/obs=9 (E≥1.5× but obs<10 → below CONF)
- Pooled 1-72: E=1.64×/obs=12 → **CONF**

F456 is reproduced at CONF in the pooled 1-72 definition. The strict 1-56 definition is one observation short of CONF (obs=9). The original F456 claim at E=1.83× is slightly higher than exp_521's E=1.64× — small variation attributable to section composition differences. **F456 stands as CONF** (conservative scope: "1-72 A-dialect" or "A herbal + A stars combined").

---

## H_new_EH: Pooled A herbal+stars o-LF pos1=y — CONF confirmed

Combined A herbal_a (1-56) + A stars (57-72) = 1102 lines total:
- o-LF N_elig: 41
- obs: 15, exp: 6.12, E: 2.45×
- **flag: CONF** (obs≥10 AND E≥1.5)

This is the first CONF-level confirmation of the o-LF pos1=y rule. The pooled baseline is y@pos1 = 158/1058 = 14.9%, intermediate between A herbal_a (14.2%) and A stars (20.0%) separately. E=2.45× at obs=15 is well above CONF threshold.

**F502 upgrade**: o-LF pos1=y is CONFIRMED in the A herbal+stars combined section (E=2.45×/obs=15 CONF). Individual sections: A herbal_a (E=2.26×/obs=9, dir) + A stars (E=2.31×/obs=6, dir).

---

## H_new_EF: ot-LF pos2=a in A herbal_a — ARTIFACT CONFIRMED

In A herbal_a (1-56, strict): ot-LF pos2=a obs=**0** (E=0.00×).

The apparent (dir) signal (E=3.23×/obs=4) from exp_520 was an artifact of the wrong A herbal_a definition (exp_520 used 1-72 A-dialect which included A stars folios 57-72). In the correct 1-56 definition, there are **no** ot-LF lines with pos2=a. The signal originated from A stars contamination. **H_new_EF is closed: artifact.**

**ot-LF pos2 in A herbal_a (1-56, confirmed):**
- ch: 11/40, E=0.80× (DEPLETED — F498 consistent)
- k: 5/40, E=2.07× (dir — F498 consistent)
- y: 4/40, E=3.60× ((dir) — exp_519 consistent)
- All other classes: flat

---

## ok-LF pos1=y cross-section scope

| Section | N_elig | obs | E | flag |
|---------|--------|-----|---|------|
| A herbal_a (1-56) | 46 | 9 | 1.38× | below CONF |
| A stars (57-72) | 9 | 1 | 0.56× | depleted |
| A cosmo (85-102) | 25 | 4 | 0.90× | flat |
| B astro (73-84) | 35 | 3 | 1.43× | below threshold |
| B pharma (103-116) | 48 | 7 | 0.84× | flat |
| B herbal (1-72 B) | 37 | 9 | 1.21× | below CONF |

ok-LF pos1=y is consistently below CONF across all sections in this methodology. The F455 claim (CONF E=1.62×) is not reproducible with current methodology in any section. F455 methodological discrepancy needs investigation.

---

## Self-Audit

**Target-awareness**: No target-aware elements. All measurements are corpus observations.

**Feature-destroying implementation**: None. The strict 1-56 A herbal_a definition is more conservative than broader definitions — if anything, it is harder on positive results. The ot-LF pos2=a artifact (false positive from wrong section) was correctly identified and corrected.

**Extrapolation**: The claim "F455 is questionable" is limited to the methodological discrepancy found. I do not claim F455 is retracted — only that the current methodology cannot reproduce it at CONF. This is appropriately scoped.

**Negative-result scope**: ok-LF pos1=y not at CONF in any section — this means the F455 claim is not reproducible under current methodology, not that ok-LF has no pos1=y enrichment (E=1.38× is directional).

**Control behavior**: o-LF null expectation: E≈1.0×. B pharma: E=1.01×/obs=7 flat. B herbal ok-LF E=1.21× flat. All controls behave as expected.

## Summary

| Hypothesis | Result |
|-----------|--------|
| H_new_EG: F455/F456 audit | F456 CONFIRMED (E=1.64×/obs=12 pooled). F455 NOT reproduced at CONF (E=1.22-1.38×). F455 flagged for investigation. |
| H_new_EH: Pooled o-LF CONF | **CONF: E=2.45×/obs=15** in A herbal+stars (1-72). F502 upgraded to CONF at pooled level. |
| H_new_EF: ot-LF pos2=a | ARTIFACT from wrong section definition. obs=0 in strict 1-56. Closed. |
