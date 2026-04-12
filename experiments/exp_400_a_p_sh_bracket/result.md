# exp_400: A p-Formula sh-Bracket Structure (H622)

**Date:** 2026-04-11
**Hypothesis tested:** H622 — Does A p-formula have sh at both pos1 AND LL (bracketing grammar)?
**Outcome:** PARTIAL SUPPORT — sh-bracket enrichment = 1.80×(N=3/40 observed vs 1.67 expected under independence). Both marginals are significant: A p→sh at pos1=1.66×(N=10/41); A p→sh at LL=3.52×(N=7/41). B p-lines are ANTI-bracket: 0.44×.

---

## 1. Setup

A p-formula lines (continuation, LF=p). Corpus: EVA ZL3B, A-dialect folios only (edy+eedy rate <5%).

Marginal enrichment tests:
- p→sh at pos1: P(pos1=sh | LF=p) vs P(pos1=sh | any LF)
- p→sh at LL: P(LL=sh | LF=p) vs P(LL=sh | any LF)

Bracket test: For lines with both pos1 and LL extractable (n≥3), count lines with sh at BOTH positions. Expected under independence = P(sh|pos1) × P(sh|LL) × N_lines. Enrichment = observed / expected.

---

## 2. Results

### A Dialect

| Metric | Observed | Expected / Baseline | E |
|--------|----------|--------------------|----|
| p→sh at pos1 | 10/41 (24.4%) | ~14.7% baseline | **1.66×** |
| p→sh at LL | 7/41 (17.1%) | ~4.9% baseline | **3.52×** |
| sh-bracket (both) | 3/40 | 1.67 | **1.80×** |

### B Dialect (comparison)

| Metric | E |
|--------|---|
| p→sh at pos1 | 1.56× (B p→sh known; B p→sh→qot=2.11× F396) |
| p→sh at LL | 0.67× (depleted) |
| sh-bracket | **0.44×** (anti-bracket) |

---

## 3. Actual A Bracket Lines

Three A lines with sh at both pos1 and LL:
- f1/5: `potoy shol... shoshy`
- f3/11: `pcheol shol sols sheol shey`
- f42/16: `pydaiin sheor shaiin tsh olchy sholy`

All three show recognizable A p-formula structure: p[LF] → sh[pos1] → [MID content] → sh[LL].

---

## 4. Interpretation

A p-formula lines have a structural asymmetry relative to B:
- **A**: p at LF → sh at pos1 (1.66×) AND sh at LL (3.52×). The sh-bracket is enriched (1.80×) above what the two marginals predict independently.
- **B**: p at LF → sh at pos1 (known), but LL is ch-avoidant (F403: p→ch LL=0.47×) and sh-depleted at LL. Anti-bracket (0.44×).

The cross-dialectal contrast is:
- **A p-formula grammar**: sh brackets the line [sh...sh]
- **B p-formula grammar**: sh at pos1, but line ends with s/qo/k/o (not sh)

This is consistent with the broader A/B cross-dialectal inversion pattern (F400: A sh-pos1 inverts B; F401: A/B y inversion). The A p-formula appears to use sh as both an opening and closing marker, while B p-formula uses sh only as an opener.

**Caveat**: N=3 bracket instances. The 1.80× enrichment is suggestive but not conclusive on its own. The result depends on both marginals being independently established (which they are: 10/41 and 7/41). The independence test is the weakest part — it assumes pos1 and LL are uncorrelated given LF=p.

---

## 5. Limitations

- N=3 sh-bracket lines. 1.80× with N=3 is borderline — the enrichment could arise by chance.
- The bracket test assumes independence of pos1 and LL choices given LF. If the sh-bracket is a fixed formula template, the actual mechanism is template-selection, not two independent draws.
- A dialect corpus is smaller than B; A p-formula lines (N=41) may not be representative of all p-formula lines if some A folios are missing or misclassified.
- B comparison uses different N and different baseline rates; the anti-bracket conclusion for B is consistent with F396/F403 but not computed from an independent test here.

---

## Self-Audit

**Target-awareness**: No target-aware elements. The bracket test is a within-corpus structure test, not compared against any VMS cipher target metric.

**Feature-destroying implementation**: No feature-destroying elements. The sh-bracket counts sh at positions pos1 and LL — these are exactly the positions the hypothesis predicts.

**Extrapolation**: Bracket enrichment 1.80×(N=3) — labeled as suggestive, not definitive. "A p-formula brackets with sh" is stated as consistent with evidence, not as a proven structural rule. PASS.

**Negative-result scope**: N/A — positive (partial support) result.

**Control behavior**: No shuffle control used. Baseline is unconditional pos1=sh rate and unconditional LL=sh rate, computed from A continuation lines. These baselines are the correct null. Expected bracket count under independence (1.67) is small, making the 1.80× enrichment weak as an isolated test — but the two strong marginals (1.66×, 3.52×) are the primary evidence. The bracket test is confirmatory, not primary.

## Finding: F404

**See findings.md F404**
