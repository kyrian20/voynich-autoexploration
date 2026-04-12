# exp_542 result — B ch→t CONF section scope (H_new_FE)

## Audit

**Target-awareness**: None. Tested all sections systematically; no cherry-picking.

**Feature-destroying implementation**: Corrected corpus parsing uses folio number extracted from folio_raw (not n-field) to classify B sections. B section definitions: herbal=folio≤72; astro=73-84; cosmo=85-102; pharma=103-116. N values confirmed against expected section sizes (B herbal=162, B astro=544, B pharma=498, B cosmo=79).

**Extrapolation**: None.

---

## Section Breakdown

| Section | N_sender | ch→t obs | ch→t E | ch→t flag | ch→k obs | ch→k E | ch→l obs | ch→l E |
|---------|----------|---------|--------|-----------|---------|--------|---------|--------|
| A herbal_a | 1861 | 42 | 1.24× | sub-CONF | 86 | 1.35× | 57 | 1.37× |
| B herbal | 190 | 4 | 1.29× | sub-CONF | 12 | 1.21× | 4 | 0.89× |
| B astro | 469 | 9 | 1.54× | near-CONF | 3 | 0.51× DEPL | 44 | **1.58× CONF** |
| B pharma | 732 | 18 | **2.17× CONF** | CONF | 27 | **1.79× CONF** | 82 | 1.28× |
| B cosmo | 110 | 4 | 1.50× | near-dir | 2 | 0.58× DEPL | 5 | 1.46× |
| B all pooled | 1501 | 35 | **1.77× CONF** | CONF | 44 | 1.36× | 135 | **1.37×** |

---

## Key Findings

### 1. B ch→t CONF is B-PHARMA-PRIMARY (not B-dialect-wide)

Pooled B ch→t CONF (E=1.77×/obs=35, F548) is driven by **B pharma** (E=2.17×/obs=18, CONF — the single largest contributor with 18/35 obs). B astro contributes 9 obs at E=1.54× (just below CONF threshold of obs≥10). B herbal is baseline (E=1.29×/obs=4). B cosmo is near-threshold (E=1.50×/obs=4).

**Scope update for F548**: B ch→t CONF is B-pharma-primary. B-all pooled is CONF but individual-section CONF only in B pharma.

### 2. B pharma ch→k CONF (E=1.79×/obs=27) — NEW

B pharma ch routes to BOTH t-onset (E=2.17×/obs=18 CONF) AND k-onset (E=1.79×/obs=27 CONF). B pharma ch→{t, k} — gallows routing in B pharma. B astro ch→k is DEPLETED (E=0.51×) — opposite direction.

**B pharma ch recruits gallows classes (k AND t) as within-line successors at CONF level.**

### 3. B astro ch→l CONF (E=1.58×/obs=44) — NEW

B astro ch routes to l-onset words at CONF (E=1.58×/obs=44). This is the ONLY CONF signal for B astro ch. B astro is also ch→k DEPLETED (0.51×). B pharma ch→l is sub-CONF (1.28×).

**B astro ch recruits l-onset as within-line successor at CONF level — a distinct routing pattern from B pharma gallows routing.**

### 4. A herbal_a ch within-line: all sub-CONF (confirmed flat)

A herbal_a: ch→t (E=1.24×/obs=42), ch→k (E=1.35×/obs=86), ch→l (E=1.37×/obs=57) — all consistently below CONF with large N. A herbal_a ch within-line is genuinely flat (F548 confirmed).

---

## A/B Section Ch Routing Summary

| Section | Ch within-line CONF routing |
|---------|----------------------------|
| A herbal_a | NONE (flat) |
| B herbal | NONE (flat) |
| **B astro** | **ch→l CONF (1.58×/obs=44)** |
| **B pharma** | **ch→t CONF (2.17×/obs=18); ch→k CONF (1.79×/obs=27)** |
| B cosmo | near-threshold (insufficient N) |

**Section-specific ch routing**: B pharma and B astro have entirely different ch routing targets. B pharma: gallows {t, k}. B astro: lateral class {l}. B herbal and A herbal_a are flat.

---

## Self-Audit

**Target-awareness**: None. The B astro ch→l CONF and B pharma ch→k CONF were unexpected.

**Feature-destroying implementation**: Folio number extraction from folio_raw confirmed against B-dialect folio distribution (26 distinct B folio numbers, total 1281 lines matching exp_541 count 1283 ≈ consistent within rounding).

**Extrapolation**: None. Claims within tested sections.

---

## Findings

**F548 SCOPE UPDATE**: B ch→t CONF (E=1.77×/obs=35 pooled) is B-PHARMA-PRIMARY: B pharma alone is CONF (E=2.17×/obs=18); B astro near-CONF (E=1.54×/obs=9); B herbal baseline. Not B-dialect-wide — it's pharma-section-specific at individual-section level.

**F551 (new): B pharma ch recruits gallows classes: ch→t CONF (E=2.17×/obs=18) AND ch→k CONF (E=1.79×/obs=27)** in B pharma. B pharma ch has dual gallows routing: both t-onset and k-onset are elevated within-line. B astro ch→k is DEPLETED (0.51×) — pharma-specific.

**F552 (new): B astro ch→l CONF (E=1.58×/obs=44)** — ch routes to l-onset words in B astro. B astro is ch→k DEPLETED. This is section-specific to B astro (B pharma ch→l sub-CONF 1.28×; B herbal 0.89×). The l-onset class is a B-astro-specific ch successor.

**H_new_FE CLOSED POSITIVE (with section structure).**
