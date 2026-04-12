# exp_531 result — B-dialect CL grammar: pooled B herbal+pharma + B astro survey

## Audit

**Target-awareness**: None. Standard CL methodology.

**Feature-destroying implementation**: Within-folio consecutive CL pairs. Section-wide LF distributions as baselines. Pooling B herbal+pharma: combined baseline from 26 folios, 1071 lines. B astro: 10 folios, 700 lines, 690 pairs.

**Extrapolation**: None.

---

## Part 1: Pooled B herbal + B pharma CL Grammar — Multiple CONF Signals

Pooled dataset: 26 folios, 1071 lines, 1045 pairs.

| Sender | Receiver | N_cond | obs | exp | E | flag |
|--------|----------|--------|-----|-----|---|------|
| d | ok | 70 | 13 | 5.75 | **2.26×** | **CONF** |
| d | d | 70 | 10 | 4.64 | **2.15×** | **CONF** |
| ol | qok | 53 | 10 | 3.46 | **2.89×** | **CONF** |
| ot | ot | 83 | 13 | 6.51 | **2.00×** | **CONF** |
| ot | a | 83 | 13 | 7.75 | **1.68×** | **CONF** |

The exp_530 candidate CONF (d→ok: E=1.79× estimate) is **confirmed** at E=2.26× with the explicit pooled analysis. Pooling is justified: B herbal d→ok E=1.75×/obs=9 and B pharma d→ok E=1.90×/obs=4 are same direction and comparable magnitude.

Additional CONF signals not anticipated in exp_530:
- **ol→qok** (E=2.89×/obs=10): ol-LF followed by qok-LF at 2.89× baseline. CONF with N=10.
- **ot→ot** (E=2.00×/obs=13): ot-LF self-succession at CONF level in pooled B.
- **ot→a** (E=1.68×/obs=13): ot-LF followed by a-LF at CONF level.

### B herbal vs B pharma d→ok breakdown:
- B herbal only: N_cond=35, obs=9, exp=5.15, E=1.75× (below CONF alone)
- B pharma only: N_cond=35, obs=4, exp=2.10, E=1.90× (below CONF alone)
- Pooled: N_cond=70, obs=13, exp=5.75, E=2.26× (CONF)

### Summary of Part 1 CONF signals:
**F527**: d→ok CONF and d→d CONF — d-LF lines are followed by ok-LF and d-self at elevated rates in B herbal+pharma.
**F528**: ol→qok CONF, ot→ot CONF, ot→a CONF — ol/ot coupling signals specific to B herbal+pharma pool.

---

## Part 2: B Astro CL Grammar Survey

B astro: 10 folios, 700 lines, 690 pairs — highest-power B-dialect CL dataset.

B astro dominant LF classes: ol=14.9%, ch=12.1%, l=11.9%, d=11.3%, qok=10.7% (very different from B herbal/pharma).

### Signals above threshold:

| Sender | Receiver | N_cond | obs | exp | E | flag |
|--------|----------|--------|-----|-----|---|------|
| a | a | 20 | 3 | 0.57 | **5.25×** | **(dir)** |
| ot | o | 29 | 3 | 0.87 | **3.45×** | **(dir)** |
| d | qo | 79 | 8 | 2.60 | **3.08×** | **dir** |
| ot | s | 29 | 3 | 1.04 | **2.90×** | **(dir)** |
| sh | qot | 33 | 3 | 1.04 | **2.89×** | **(dir)** |
| k | qok | 10 | 3 | 1.07 | **2.80×** | **(dir)** |
| d | y | 79 | 4 | 1.47 | **2.73×** | **(dir)** |
| qok | qok | 75 | 14 | 8.04 | **1.74×** | **CONF** |
| ol | o | 104 | 7 | 3.12 | **2.24×** | **dir** |

Note: ol→o (dir, E=2.24×/obs=7) meets `dir` threshold (obs≥5, E≥2.0×) but was below the E≥2.5× filter in the summary — included here manually.

### Key B astro findings:

**qok→qok CONF (F495, cross-confirmed)**: B astro qok-LF lines self-chain at CONF level (E=1.74×/obs=14). Previously documented as F495 (exp_516, E=1.77×/obs=14). This experiment confirms F495 with identical N and comparable E-value.

**d→qo dir and ol→o dir (F495 directionals, cross-confirmed)**: B astro d→qo E=3.08×/obs=8 (dir) and ol→o E=2.24×/obs=7 (dir). Both previously noted as directionals in F495's limitation text (E=3.13×/obs=8 and E=2.28×/obs=7). Minor value differences due to baseline calculation.

**ot CL profile and other new (dir) signals (F531)**: ot-LF sends to o (E=3.45×) and s (E=2.90×) at (dir) level. Additional new (dir) signals not in F495: a→a (5.25×/obs=3), sh→qot (2.89×/obs=3), d→y (2.73×/obs=4), k→qok (2.80×/obs=3). These six signals are the genuinely new B astro findings of this experiment.

---

## Cross-Section Comparisons

| Signal | A herbal_a | B herbal | B pharma | Pooled B_hp | B astro |
|--------|-----------|---------|---------|------------|---------|
| d→qot | CONF (F491) | ZERO | — | — | E=1.21×/obs=3 (below) |
| d→qo | — | — | — | E=0.55×/obs=3 (DEPL) | **dir** (E=3.08×) |
| d→ok | — | 1.75× (near-CONF) | 1.90× | **CONF** E=2.26× | E=0.72× (DEPL) |
| qok→qok | — | — | — | E=0.87× (DEPL) | **CONF** E=1.74× |
| ot→ch | — | **dir** (F526) | DEPL | DEPL | E=0.85×/obs=3 (DEPL) |

The B dialects are NOT uniform in CL structure:
- B astro qok→qok CONF but DEPLETED in B herbal+pharma pooled
- Pooled B herbal+pharma d→ok CONF but DEPLETED in B astro
- B herbal ot→ch (F526) not present in B pharma or B astro

---

## New Hypotheses

**H_new_EV**: B astro d→qo (dir) vs A herbal_a d→qot (CONF) — is qo the B-astro functional equivalent of qot in the CL chain sender role? Test: does B astro have a d→qo→? chain (analogous to A herbal_a's d→qot→ch)?

**H_new_EW**: B astro qok→qok CONF: why does qok self-succeed? Is qok a "topic continuation" class in B astro (similar to d-LF self-succession in A herbal_a)? Check: does B astro qok have grammar analogous to A herbal_a's d-LF (multi-link chain)?

---

## Summary

| Finding | Resolution |
|---------|-----------|
| Pooled B herbal+pharma d→ok | CONF confirmed: E=2.26×/obs=13 (F527) |
| Pooled B herbal+pharma d→d | CONF: E=2.15×/obs=10 (F527) |
| Pooled B herbal+pharma ol→qok | CONF: E=2.89×/obs=10 (F528) |
| Pooled B herbal+pharma ot→ot | CONF: E=2.00×/obs=13 (F528) |
| Pooled B herbal+pharma ot→a | CONF: E=1.68×/obs=13 (F528) |
| B astro qok→qok | CONF: E=1.74×/obs=14 (cross-confirms F495) |
| B astro d→qo | dir: E=3.08×/obs=8 (cross-confirms F495 directional) |
| B astro ol→o | dir: E=2.24×/obs=7 (cross-confirms F495 directional) |
| B astro (dir) signals: ot→o, ot→s, sh→qot, a→a, d→y, k→qok | (dir) level (F531) — genuinely new |
| B-dialect CL homogeneity | **HETEROGENEOUS**: each B section has different CL grammar |

**New findings: F527, F528, F531** (3 new findings; F495/F496 cross-confirmed)
**New hypotheses: H_new_EV, H_new_EW**
