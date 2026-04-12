# exp_544 result — B d→sh section scope; A d→cth/ckh scope (H_new_FH)

## Audit

**Target-awareness**: None. All sections tested systematically.

**Feature-destroying implementation**: Same folio-number B-section classification as exp_542. d-onset correctly identified (ONSET_PRIORITY priority 15, after compound gallows cth/ckh/cph). d→sh and d→cth/d→ckh computed as within-line bigrams separately per section.

**Extrapolation**: None.

---

## B d→sh Section Breakdown

| Section | N_sender | sh obs | sh E | sh flag |
|---------|----------|--------|------|---------|
| B herbal | 97 | 21 | 2.14× | **CONF** |
| B astro | 266 | 48 | 1.40× | sub-CONF |
| B pharma | 205 | 34 | 2.23× | **CONF** |
| B cosmo | 51 | 6 | 1.70× | underpowered |
| B all pooled | 619 | 109 | 1.79× | **CONF** |

**B d→sh is B-HERBAL and B-PHARMA CONF**: Both B herbal (E=2.14×/obs=21) and B pharma (E=2.23×/obs=34) independently show CONF d→sh. B astro has large N (N_sender=266, obs=48) but E=1.40× — genuinely sub-CONF within B astro (baseline sh rate is higher in B astro, reducing relative E). B cosmo underpowered (obs=6). The pooled B CONF is driven by herbal+pharma, not astro.

**Scope update for F555**: B d→sh CONF = B-herbal CONF + B-pharma CONF (both independently). B astro sub-CONF despite large obs — d→sh is not a B-astro rule.

---

## A d→cth, d→ckh Scope: Compound Gallows in B

| Section | N_sender | cth obs | cth E | ckh obs | ckh E |
|---------|----------|---------|-------|---------|-------|
| A herbal_a | 988 | 62 | 1.97× CONF | 20 | 1.58× CONF |
| B herbal | 97 | 1 | 1.12× | 0 | 0.00× |
| B astro | 266 | 1 | 2.65× | 0 | 0.00× |
| B pharma | 205 | 1 | 2.31× | 0 | 0.00× |
| B cosmo | 51 | 1 | 5.68× | 0 | 0.00× |

**Compound gallows (cth, ckh) are EFFECTIVELY ABSENT from B-dialect sections**: All B sections have cth=1 obs (single occurrence each) and ckh=0 obs. A d→cth CONF (E=1.97×/obs=62) and A d→ckh CONF (E=1.58×/obs=20) are A-herbal-a-specific by necessity — compound gallows are A-dialect-dominant features not testable in B. This is consistent with the known cth/ckh frequency differential between A and B dialects.

---

## Summary

- **B d→sh CONF** (F555) is B-HERBAL + B-PHARMA-specific (each independently CONF); B astro sub-CONF. F555 scope updated: "B all pooled CONF, driven by B herbal and B pharma."
- **A d→cth/ckh CONF** (F555) are A-herbal-a-specific — compound gallows are near-absent in B (obs≤1 per section), making B comparison impossible.
- No new findings beyond scope clarification.

**H_new_FH CLOSED (scope clarification only, no new CONF signals).**
