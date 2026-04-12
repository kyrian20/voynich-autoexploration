# exp_525 result — A stars per-page reclassification (H_new_EN) + F446 audit

## Audit

**Target-awareness**: No target-aware elements. All measurements are corpus observations.

**Feature-destroying implementation**: Per-page edy-rate computation is applied per page name (e.g., f57v separately from f57r). The is_b_dialect threshold (≥5%) is the same as standard methodology. This is a methodological alternative to folio-number grouping, not a modification.

**Extrapolation**: No extrapolation. Results are direct corpus measurements.

**Critical finding — F446 contradicted**: This experiment finds t-LF in A stars (per-page and folio-number) at N=2/136 = 1.5%, giving E=0.51× relative to A herbal_a (2.9%). F446 claimed E=2.12×/N=15. Both methodologies confirm t-LF is DEPLETED in A stars at current corpus, not elevated. See Section 3 for discussion.

**Control behavior**: Folio-number vs per-page comparison is the internal control. Both give identical results (136 lines each, same pages), confirming the methodology equivalence for the 57-72 range in this corpus.

---

## H_new_EN: Per-page A stars reclassification

### Part 1: Methodology comparison

**Per-page A stars (57-72, not B-dialect): 12 pages, 136 lines** — IDENTICAL to folio-number A stars.

Reason: The folio numbers that were previously excluded from A stars (n=57, 60-66 range etc.) are excluded because their B-dialect pages are classified as B-dialect by both methods. The pages in 57-72 range that are A-dialect happen to already be on folio numbers where the combined grouping also gives A-dialect classification (low edy rate).

**B-dialect pages in 57-72 range**: f57r, f65v, f66r, f66v. These are the pages that render certain folio numbers B-dialect.

**Per-page recovered pages**: NONE beyond what folio-number grouping already includes. The per-page reclassification does NOT expand A stars.

**H_new_EN conclusion**: The per-page reclassification produces the identical A stars section as folio-number grouping for the 57-72 range in the ZL3b corpus. H_new_EJ's blocking is not due to the folio-number methodology — t-LF is simply not present in A stars at elevated rates (see Part 3).

---

## Part 2: t-LF in A stars (H_new_EJ reconsidered)

A stars t-LF: **N=2 lines** (out of 136 total, 1.5%). Both methodologies agree.

With N=2, no positional grammar can be meaningfully assessed. H_new_EJ is confirmed UNANSWERABLE at current corpus, regardless of methodology.

### F503 verification (o-LF pos1=y in A stars)

Per-page A stars o-LF pos1=y: E=2.50×/obs=7/N_elig=14 → **dir** (confirmed). F503 reproduced. o-LF pos2=o-self also reproduced: E=4.17×/obs=4 ((dir)) ✓ F504.

---

## Part 3: F446 CONTRADICTED — t-LF is NOT elevated in A stars

**F446 claimed**: A stars t-LF elevation E=2.12×/N=15 (from exp_466).
**This experiment finds**: A stars t-LF N=2/136 = 1.5% vs A herbal_a 28/966 = 2.9% → **E=0.51× (DEPLETED)**.

The discrepancy is not a subtle E-value correction but a complete directional reversal: F446 claimed 2.12× elevation; current finding is 0.51× depletion. Both folio-number and per-page methodologies give identical results (N=2, E=0.51×).

**Possible sources of F446 discrepancy:**
1. Different corpus file used in exp_466 (the corpus may have been updated between exp_466 and current experiments)
2. Different A stars section definition in exp_466 (perhaps A stars included more pages)
3. Different methodology for computing E (perhaps using global baseline vs section-specific)
4. Script error in exp_466

**Action required:** F446 should be **FLAGGED for investigation** (Q011). t-LF is NOT elevated in A stars under current corpus and methodology. H_new_EJ is not "blocked" by methodology — it is closed by the finding that t-LF is not a dominant LF class in A stars.

**Updated A stars characterization:**
- LF distribution: d(18.4%), ch(16.9%), a(11.0%), o(10.3%), sh/ok(7.4% each), ot(6.6%), ol(5.1%), y(4.4%), s(3.7%)
- t-LF: 1.5% (DEPLETED vs A herbal_a's 2.9%, E=0.51×)
- a-LF is the most notable difference from A herbal_a: a is 11% in A stars vs ~1.4% in A herbal_a

**A stars dominant LF classes are d, ch, a, o — not t.**

---

## Summary

| Hypothesis | Result |
|-----------|--------|
| H_new_EN: per-page A stars | Per-page = folio-number (136 lines both). NO expansion. |
| H_new_EJ: t-LF in A stars | CLOSED (NOT "blocked"): t-LF N=2 in A stars (1.5%, DEPLETED 0.51×). |
| F446 (t-LF elevation A stars) | **CONTRADICTED**: E=0.51× (DEPLETED) vs claimed E=2.12×. Q011 raised. |
| F503 (o-LF pos1=y A stars) | **REPRODUCED**: E=2.50×/obs=7 dir ✓ |
| F504 (o-LF pos2=o-self A stars) | **REPRODUCED**: E=4.17×/obs=4 (dir) ✓ |

**New open question:** Q011 — F446 (t-LF elevation in A stars) is contradicted by current corpus/methodology. Investigate exp_466 script and methodology to determine source of discrepancy.

**New hypothesis generated:** H_new_ER — characterize A stars a-LF grammar. a-LF is the 3rd most common LF class in A stars (11%), but has no confirmed within-line grammar rules anywhere (a-LF in B herbal has F470: a→a@pos2 dir). What is the positional grammar of a-LF in A stars?
