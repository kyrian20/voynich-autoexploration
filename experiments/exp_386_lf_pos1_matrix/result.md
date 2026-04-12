# exp_386: LF-Formula Class → pos1 Response Matrix (H600)

**Date:** 2026-04-11
**Hypothesis tested:** H600 — what pos1 class follows each LF-formula class?
**Outcome:** ANSWERED with partial falsification of expected routing architecture

---

## 1. Corpus Statistics

- A dialect continuation LF→pos1 pairs: **1478**
- B dialect continuation LF→pos1 pairs: **2271**

---

## 2. Key Structural Finding: A Dialect pos1 r = 0 (Categorical)

A dialect pos1 baseline: r = 0/1478 (0.0%). **r never appears at pos1 in A dialect.** This extends the A r-exclusion pattern beyond specific producing-class rules (sh→r=0, y→r=0, cth→r=0 from F384/F387/F388) to a categorical positional rule: A r is LL-only. r cannot occupy pos1 in A-dialect continuation lines.

---

## 3. LF-Formula Classes (d, s, y) — Routing to ch/sh at pos1

### A dialect:
| LF class | N   | ch (E)   | sh (E)   |
|----------|-----|----------|----------|
| d        | 255 | 0.91×    | 1.08×    |
| s        | 91  | 1.22×    | 1.18×    |
| y        | 212 | 0.83×    | 0.76×    |

**A LF-formula classes do NOT specifically route to ch/sh.** All three produce ch/sh at near-baseline or below-baseline rates. The dominance of ch/sh at A pos1 (27.9% and 15.0% respectively) is a property of ch/sh's positional concentration, not driven by specific LF-formula class routing.

### B dialect:
| LF class | N   | ch (E)   | sh (E)   | primary elevated routes |
|----------|-----|----------|----------|-------------------------|
| d        | 344 | 1.24×    | 1.40×    | sh(N=81), ch(N=82), s(2.20×/N=6) |
| s        | 260 | 1.00×    | 1.42×    | sh(N=62), ol(1.43×/N=23) |
| y        | 261 | 1.03×    | 0.57×    | y(2.13×/N=12), r(2.30×/N=10) |

**B y is the exception**: y AVOIDS sh at pos1 (0.57×), unlike d(1.40×) and s(1.42×). B y at LF primarily routes to same-class y(2.13×) and r(2.30×), not to ch/sh. The B s→sh (1.42×) and B d→sh (1.40×) are the clearest LF-formula → ch/sh routing rules, but both are mild (not the strong directed routing that was hypothesized).

---

## 4. Template Classes at LF: Self-Routing Pattern

qot and qok at LF show onset-class self-routing to pos1:
- A qot at LF: qot→qot=3.00×(N=6), qot→ch=1.40×; ot=0.00×/ol=0.00×
- A qok at LF: qok→qok=2.17×(N=9), qok→ch=1.23×; sh=0.56×(depleted)
- B qot at LF: qot→qot=2.01×(N=3), qot→y=2.96×(N=3), qot→r=3.20×(N=6), qot→qok=1.85×(N=11)
- B qok at LF: qok→qok=1.27×(N=38), qok→r=3.20×(N=12)

**B template classes at LF route to r at pos1 (qot=3.20×/N=6, qok=3.20×/N=12).** This is a new cross-dialect-specific rule: in B, template classes at LF produce r at pos1 — a pattern absent from A (where pos1 r=0).

B ok at LF avoids ch/sh (ch=0.82×, sh=0.70×) and prefers template successors: d(2.13×), qok(1.56×), ok(1.61×), ot(1.76×), qot(1.66×). Template classes at LF produce template classes at pos1.

---

## 5. y Self-Routing at LF→pos1

y at LF shows cross-dialectal self-routing:
- A y→y: E=1.78×(N=12) — moderate, directional
- B y→y: E=2.13×(N=12) — moderate

Combined with y's MID self-succession (A=3.15×, F387) and pre_LL self-succession (B=6.37×, F387), y is the onset class with strongest self-routing across all line positions.

---

## 6. Additional Observations

- **A s→s at LF: 3.75×(N=3)** — directional (tiny N), but consistent with A s self-succession (N=6 overall from F386)
- **A d→y at LF: 1.60×(N=13)** — moderate (d leads to y at pos1 slightly above baseline)
- **A d→cth at LF: 1.60×(N=5, dir)** — consistent with A d→cth pan-positional rule (F385)
- **B d→ol depleted at pos1: 0.47×** — B d at LF specifically avoids ol at pos1
- **A qot→ot=0.00×, qot→ol=0.00×** — A qot at LF avoids ot/ol class at pos1

---

## 7. Synthesis: LF→pos1 Architecture Revised

The expected architecture (LF-formula class → ch/sh response at pos1) is partially falsified:
1. In A dialect, there is NO specific LF-formula → ch/sh routing: d/s/y all produce ch/sh at near-baseline.
2. In B dialect, the routing is mild (1.4-1.42×) for d and s; **y breaks the pattern** (avoids sh, prefers y/r).
3. The dominant architecture at LF→pos1 is:
   - **Template-class self-routing**: qot→qot, qok→qok (cross-dialect)
   - **B template classes → r**: qot/qok at LF → r at pos1 (B-specific)
   - **y self-routing**: y at LF → y at pos1 (cross-dialect, moderate)
   - **LF-formula class d/s → sh mild elevation** (B-only, E≈1.40-1.42×)

The ch/sh dominance at pos1 is a consequence of ch/sh being pos1-enriched classes, not of specific LF-formula routing.

---

## 8. Methodology Notes

- Baseline uses pos1-conditional frequencies (same denominator = total LF→pos1 pairs per dialect)
- Continuation lines only (ln != min_ln AND ln != max_ln)
- A pos1 r=0.0% means all A cells in the r column are "nan" (undefined baseline) — r is categorically absent from A pos1

---

## Self-Audit

**Target-awareness**: No target-aware elements identified. The experiment computes corpus-internal bigram frequencies and enrichment ratios. No parameter was calibrated against any VMS target metric.

**Feature-destroying implementation**: No feature-destroying implementation details identified. The LF→pos1 extraction uses the standard continuation-line filter (ln != min_ln AND ln != max_ln), which is the appropriate scope for testing LF→pos1 bigrams in non-opener/non-closer contexts. The onset priority order correctly disambiguates overlapping onsets (qok/qot/qo before ch/sh before single-letter classes).

**Extrapolation**: All claims are within the tested parameter range. The finding that "A LF-formula classes do NOT specifically route to ch/sh" is bounded to the continuation-line LF→pos1 context; no claim is made about other position pairs or about folio-opener/closer lines.

**Negative-result scope**: The partial falsification of the expected LF-formula → ch/sh routing is scoped to: (1) A-dialect, where the routing does not materialize at all; (2) B-dialect y, which avoids sh. The B d/s → sh mild elevation (1.40-1.42×) is not refuted — it is confirmed but recharacterized as mild rather than strongly directed. Valid conclusion: "Under continuation-line LF→pos1 context, d/s do not strongly route to ch/sh; A shows no routing preference; B shows mild sh-elevation for d/s but y breaks the pattern."

**Control behavior**: No external control distributions used. The baseline is the corpus-internal pos1 distribution (all LF→pos1 pairs regardless of LF class). Expected behavior: if no LF-class-specific routing exists, all LF classes should produce the pos1 baseline distribution (E≈1.0× for all pos1 classes). For most A LF-formula classes, this is what was observed — A d/s/y produced ch/sh at E=0.76-1.22×, all within baseline range. The B template classes at LF routing to r (E=3.2×) is a clear departure from baseline, consistent with strong routing.

## Finding: F390

**See findings.md F390**
