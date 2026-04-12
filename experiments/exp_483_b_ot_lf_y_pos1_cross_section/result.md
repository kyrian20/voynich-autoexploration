# exp_483: Cross-Section ot-LF → y@pos1 and ok-LF → a@pen Tests

**Question:** H_new_AZ — (1) Does B pharma/astro ot-LF → y at pos1 (confirming cross-dialectal ot/y opener from F456+exp_482)? (2) Is ok-LF → a at pen a B-dialect-wide rule (B herbal + B pharma)?

---

## Results: ot-LF → y at pos1 Across B Sections

| Section | N_ot | y@pos1 obs | y@pos1 exp | E | flag |
|---------|------|-----------|-----------|---|------|
| A herbal_a | 43 | 11 | 6.0 | 1.83× | **CONFIRMED (F456)** |
| B herbal | 11 | 6 | 2.2 | 2.67× | dir (exp_482) |
| B pharma | 79 | 16 | 13.7 | 1.16× | flat |
| B astro | 30 | 1 | 1.9 | 0.52× | depleted |
| B cosmo | 9 | 3 | 1.4 | 2.20× | (dir, N=9 total) |
| **B combined** | **129** | **26** | **17.6** | **1.48×** | **below threshold** |

**ot-LF → y at pos1 is herbal-section-specific, not B-dialect-wide.**

B pharma ot-LF (N=79) is FLAT for y at pos1 (E=1.16×). B astro ot-LF (N=30) shows y DEPLETED (E=0.52×). B combined gives E=1.48×/N=26 — below the E≥1.5× threshold for confirmation. The cross-dialectal evidence from exp_482 (B herbal dir) reflects the shared HERBAL content, not the B-dialect grammar per se. 

**Revised scope of F456/exp_482 finding**: ot-LF → y at pos1 is:
- Confirmed in A herbal_a (F456)
- Directional in B herbal (exp_482)
- Absent in B pharma and B astro

This is a **herbal-content-specific rule**: both herbal sections (A and B) use y to open ot-terminal lines, while non-herbal sections do not. The rule is governed by content domain (herbal), not dialect boundary (A/B).

B pharma ot-LF pos1 top signal: **t at pos1 (E=2.02×/N=6, dir)**. B pharma ot-LF has different pos1 routing than herbal — t rather than y. This further supports content-conditional grammar routing.

---

## Results: ok-LF → a at pen Across B Sections

| Section | N_pen_elig | a@pen obs | a@pen exp | E | flag |
|---------|-----------|----------|----------|---|------|
| B herbal | 35 | 6 | 2.2 | 2.73× | dir |
| B pharma | 49 | 11 | 4.0 | 2.75× | **CONFIRMED** (F452) |
| B astro | 35 | 2 | 0.7 | 2.70× | (dir) |
| B cosmo | 6 | 0 | 0.3 | 0.00× | (too small) |
| **B combined** | **125** | **19** | **6.8** | **2.79×** | **CONFIRMED** |

**F459: B-dialect ok-LF → a at pen (E=2.79×/N=19, CONFIRMED).** The ok→a-pen rule is B-dialect-wide. Herbal (dir), pharma (CONF), and astro (dir) all show E≈2.7×. Combined gives N=19, E=2.79×. This extends F452 (B pharma-specific) to a B-dialect finding. a-onset words (a-suffix forms: am, ain, aiin) appear at the penultimate position in ok-ending lines at 2.79× baseline across all B sections with ok-LF representation.

Note: B pharma E in this experiment (2.75×) is higher than in F452 (E=2.04×). The difference arises from baseline choice: F452 computed the a-rate from the overall section distribution (11.0% baseline) while this experiment uses the pen-specific baseline (8.2% for a at pen in B pharma). Both confirm the finding; the E values differ by baseline convention. The underlying obs/N are identical (11/49).

---

## Results: ot-LF → ot at pen (F450 Cross-Section Replication)

| Section | N_pen_elig | ot@pen obs | ot@pen exp | E | flag |
|---------|-----------|-----------|----------|---|------|
| B pharma | 78 | 15 | 8.6 | 1.75× | **CONFIRMED** (F450) |
| B herbal | 11 | 3 | 0.6 | 5.43× | (dir) |
| **B combined** | **128** | **25** | **11.2** | **2.24×** | **CONFIRMED** |

**F460: B-dialect ot-LF → ot at pen (E=2.24×/N=25, CONFIRMED).** F450 (B pharma-specific, E=1.94×/N=15) extends to B-dialect combined. B herbal also shows the ot-pen doublet (dir, 5.43×/N=3). Combined N=25 at E=2.24× is strongly confirmed. The ot-at-pen pattern is B-dialect-wide, not pharma-specific.

(Note: B pharma E here is 1.75× vs F450's 1.94× — small baseline difference due to how exp_479 vs exp_483 compute the section baseline. The N=15 and obs/N are identical; the E discrepancy is a methodological artifact, not a data discrepancy.)

---

## Synthesis

**Content-conditional vs dialect-conditional rules:**

| Rule | A herbal_a | B herbal | B pharma | B astro | Conclusion |
|------|-----------|---------|---------|--------|------------|
| ot-LF → y@pos1 | CONF (F456) | dir | flat | depleted | Herbal-content-specific |
| ok-LF → a@pen | — | dir | CONF (F452) | dir | B-dialect-wide (F459) |
| ot-LF → ot@pen | dir (exp_481) | dir | CONF (F450) | — | B-dialect-wide (F460) |

The ot/y opener rule is **content-conditional** (herbal sections only). The ok→a-pen and ot→ot-pen rules are **dialect-conditional** (all B sections). This supports the §17.4 four-level grammar taxonomy: LF-class grammar rules operate at different scopes — some are section-specific, others are dialect-wide.

---

## Self-Audit

**Target-awareness:** None. All enrichment calculations use section-specific baselines derived from the corpus itself. No VMS target metric informed parameter choices.

**Feature-destroying implementation:** Onset priority list correct (cth before ch; qok/qot/qo before ok/ot/ol). pen = ws[-2]. B dialect classifier: edy+eedy rate ≥5% at folio level. locus stripping: locus.lstrip('+*=/~&'). No feature-destroying details.

**Extrapolation:** ot-LF → y at pos1 "herbal-content-specific" claim based on: A herbal CONF + B herbal dir (N=6) vs B pharma flat (N=16) + B astro depleted (N=1). The B herbal N is small (N=11 total ot-LF lines); the "herbal-content-specific" label is directional. Stated as "herbal-section-specific" (not "confirmed" as a cross-section rule).

E discrepancy for F452/F450 replication noted: the E values differ between exp_479 and exp_483 due to different baseline construction (pos-specific vs overall). Both confirm the finding. The discrepancy is a documented methodological choice, not a data inconsistency.

**Negative-result scope:** ot-LF → y at pos1: "absent from B pharma and B astro" is stated correctly at section scope. B pharma N=79 is adequate to detect a 1.5× enrichment if present. B astro N=30 has E=0.52× — y is depleted, not just flat.

**Control behavior:** N/A — no explicit control distribution. Section-specific baselines are section-internal.

---

## Conclusion

**F459 ASSIGNED: B-dialect ok-LF → a at pen (E=2.79×/N=19, CONFIRMED).** Extends F452 from pharma-specific to B-dialect-wide. ok-terminal lines close with a-suffix words at penultimate across all B sections.

**F460 ASSIGNED: B-dialect ot-LF → ot at pen (E=2.24×/N=25, CONFIRMED).** Extends F450 from pharma-specific to B-dialect-wide. ot-terminal lines have ot-class penultimate words at 2.24× baseline across B.

**H_new_AZ ANSWERED:** ot-LF → y at pos1 is herbal-content-specific (A+B herbal both show it; B pharma/astro do not). ok-LF → a at pen and ot-LF → ot at pen are B-dialect-wide features.
