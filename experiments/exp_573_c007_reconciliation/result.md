# exp_573: C007 Reconciliation — Onset Self-Succession Methodology Comparison

**Date:** 2026-04-12
**Hypothesis tested:** Resolution of Q013 — why do exp_565/567 (canonical) find lower self-succession than exp_164/174 (C007 source)?
**Status:** RESOLVED — C007 requires amendment (see proposed_c007_amendment.md)

---

## PURPOSE

C007 claims: "Onset self-succession ranges from 1.24× (qok, B-dialect) to 2.05× (ok, A-dialect)."
Canonical experiments find: B qok=1.03× (exp_565), A ok=1.42× (exp_567).
This experiment identifies the methodological sources of discrepancy and determines the correct values.

---

## IDENTIFIED METHODOLOGY DIFFERENCES (exp_164/174 vs canonical)

Five variables differ between the C007-source experiments and the canonical methodology:

**(A) Dialect assignment**: exp_174 uses FOLIO-LEVEL edy-rate (aggregate words per folio); canonical (exp_565) uses PER-LINE edy-rate (each line independently classified as B if edy≥5% of that line's words). This is the dominant factor for A-dialect values.

**(B) Bigram formula**: exp_174 uses E = obs / (total_bigrams × rate²); canonical uses E = obs / (n_sender × mid_rate_target). The canonical formula uses MID-position frequency of the target class (higher than overall for MID-concentrated classes), producing lower E-values.

**(C) Word parsing**: exp_174 splits text on '.' only; canonical splits on '[-.\s]' (also hyphens/spaces) + requires all-lowercase + len≥2. The old parsing includes more multi-character tokens and single-character words.

**(D) Onset taxonomy**: exp_174 has 'ch_e' class (words starting che/chi) separate from 'ch'; canonical has no ch_e but adds ckh/cph/sch as distinct classes.

**(E) Corpus scope**: exp_174 A includes ALL A-dialect folios (folio-level assignment); canonical restricts A to lines with line_number ≤ 56 (effectively all lines, since the filter removes only 41/2074 lines), but PER-LINE dialect assignment changes which lines are "A."

---

## KEY FINDING: WHAT DRIVES THE DISCREPANCY?

### A-dialect ok self-succession (exp_174: 1.930×, exp_567: 1.42×, Δ=0.51):

| Condition | E |
|-----------|---|
| Old formula + folio-level dialect (best-faith exp_174 replication) | 2.083× |
| Canonical formula + folio-level dialect | 1.882× (formula effect: Δ=−0.20) |
| Canonical formula + per-line dialect (canonical) | 1.421× (dialect-assignment effect: Δ=−0.46) |

**The dialect-assignment change is the dominant driver** (−0.46×). Per-line dialect assignment enlarges the A herbal_a corpus from ~8,453 words (folio-level) to 11,327 words (per-line), capturing more heterogeneous lines including those from mixed-section folios. This dilutes the self-succession signal. The formula change contributes an additional −0.20×.

### B-dialect qok self-succession (exp_174: 1.239×, exp_565: 1.03×, Δ=0.21):

| Condition | E |
|-----------|---|
| Old formula + folio-level dialect (best-faith exp_174 replication) | 1.259× |
| Canonical formula + folio-level dialect | 1.093× (formula effect: Δ=−0.17) |
| Canonical formula + per-line dialect (canonical) | 1.028× (dialect-assignment effect: Δ=−0.07) |

**For B-dialect**, the formula change dominates (−0.17×). The canonical formula uses mid_rate_qok as the expected baseline — and since qok is highly concentrated at MID positions (LF DEPL=0.53×), mid_rate_qok > overall_rate_qok, making the expected denominator larger and thus E lower.

---

## C007 ATTRIBUTION ERROR

C007 states "2.05× (ok, A-dialect)" for the upper bound. This is a misattribution:
- exp_174's A ok unconditional = **1.930×** (not 2.05×)
- exp_174's maximum is **B qo unconditional = 2.047×**
- The committed claim should have cited "qo, B-dialect" not "ok, A-dialect"

This misattribution does not affect C007's practical validity for most purposes (the claim that self-succession is substantial across classes and dialects), but it assigns the wrong class and dialect to the upper bound value.

---

## CANONICAL SELF-SUCCESSION SURVEY

**A herbal_a (per-line dialect, canonical formula, obs≥10):**

| Onset | obs | E | CONF? |
|-------|-----|---|-------|
| l | 16 | 3.86× | sub-CONF (obs<10 strict, but E is high) |
| ol | 45 | 3.20× | CONF |
| qot | 18 | 3.16× | CONF |
| cth | 15 | 2.46× | CONF |
| ot | 50 | 2.23× | CONF |
| y | 40 | 1.88× | CONF |
| qo | 14 | 1.76× | CONF |
| d | 151 | 1.75× | CONF |
| qok | 77 | 1.27× | sub-CONF |
| ok | 81 | 1.42× | sub-CONF |
| sh | 96 | 1.21× | flat |
| ch | 453 | 1.04× | flat |

**B all (per-line dialect, canonical formula, obs≥10):**

| Onset | obs | E | CONF? |
|-------|-----|---|-------|
| y | 20 | 3.16× | CONF |
| l | 72 | 2.62× | CONF |
| ot | 90 | 2.10× | CONF |
| qo | 16 | 1.82× | CONF |
| qot | 29 | 1.69× | CONF |
| ok | 56 | 1.30× | sub-CONF |
| ol | 30 | 1.32× | sub-CONF |
| d | 41 | 1.35× | sub-CONF |
| qok | 242 | 1.03× | flat |
| ch | 259 | 0.91× | flat/near-DEPL |
| sh | 76 | 0.78× | near-DEPL |

**Range (obs≥10 in either dialect):** 0.78× (B sh) – 3.86× (A l)

**Classes with CONF self-succession in both dialects:** y, l, ot, qo, qot  
**Classes with flat/depleted self-succession:** ch (both dialects), sh (B), qok (B)

---

## INTERPRETATION

**The C007 claim requires three amendments:**

1. **The range is wrong**: C007's "1.24–2.05×" captures part of the range but gets the bounds wrong. Canonical range (obs≥10): 0.78× – 3.86×. Several classes are flat or near-DEPL (ch A=1.04×, B=0.91×; sh B=0.78×; qok B=1.03×).

2. **The upper bound is misattributed**: 2.05× is from B qo (exp_174), not A ok. Canonical maximum is A l=3.86× or A ol=3.20× (though obs<10 for l; best obs≥10 canonical max is A ol=3.20×).

3. **"Residuals ≥1.2× across all tested combinations" is false under canonical**: B qok (1.03×), B ch (0.91×), B sh (0.78×) all fail this claim.

**What remains true from C007:** The claim that onset self-succession "survives position control" remains broadly true for classes with CONF self-succession (y, l, ot, qo, qot in both dialects). The CONF classes ARE self-successive, and this was confirmed across dialects. The methodological differences reduced the estimated E-values but do not change the qualitative finding that several classes show robust self-succession.

**Root cause summary:** The discrepancy is methodological, not a data error. The two most important differences are:
1. Per-line vs folio-level dialect assignment (dominant for A-dialect, dilutes the signal)
2. MID-baseline vs overall-rate formula (dominant for B-dialect, raises expected count for MID-concentrated classes)

---

## Self-Audit

**Target-awareness**: No target-aware elements. This experiment is purely methodological comparison using the VMS corpus; no VMS target metrics were used to calibrate any parameter.

**Feature-destroying implementation**: No feature-destroying implementation. The self-succession computation correctly identifies consecutive onset-class pairs. Both old and canonical formulas measure the same raw observation (obs = count of same-class adjacent pairs); they differ only in the expected-count denominator.

**Extrapolation**: None. Claims are within the scope of computed E-values with explicit obs counts. The statement that B qok "is flat at 1.03×" is specific to the canonical methodology and noted as such.

**Negative-result scope**: N/A — this is a reconciliation experiment, not a mechanism test.

**Control behavior**: No shuffled-text control needed here — the experiment's purpose is to compare two computing methodologies on the same data, not to assess statistical significance of the self-succession signal. The comparison is self-contained.

---

## CONCLUSIONS

1. The C007 discrepancy is **fully explained** by two methodology changes: (A) per-line vs folio-level dialect assignment, (B) canonical formula vs old formula. No bug in exp_565/567; no bug in exp_164/174 — they are computing different things on partially different data.

2. C007's lower bound "1.24× (qok, B-dialect)" should be revised: B qok in canonical = 1.03× (flat). The actual lower bound across canonical CONF classes is ~1.69× (B qot); non-CONF classes go as low as 0.78× (B sh).

3. C007's upper bound "2.05× (ok, A-dialect)" is a misattribution: the 2.047 is from B qo in exp_174. Canonical maximum (obs≥10) is A ol=3.20×.

4. The claim "residuals ≥1.2× across all tested combinations" fails for B qok (1.03×), B ch (0.91×), B sh (0.78×).

5. See **state/proposed_c007_amendment.md** for the proposed corrected language.

**→ Q013 RESOLVED**


---

## Reproducibility check — 2026-10-22

The script was made repository-relative (removing the machine-specific `/Users/asash/...` corpus path), given a main guard so it can be imported safely, and added to the `Voynich Check` workflow. The full run passed in [CI run 584](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39740259579).

The canonical per-line/formula values reproduce the reported values closely:
- A-dialect `ok`: 1.421× (reported exp_567: 1.42×).
- B-dialect `qok`: 1.028× (reported exp_565: 1.03×).

**Important limitation:** the old-formula/folio-level branch is not an exact numerical reproduction of the historical exp_174 table: this run gives A `ok` = 2.083× versus the cited 1.930×, and B `qok` = 1.259× versus 1.239×. Thus, treat that branch as a best-faith methodological comparison, not as an exact reproduction of exp_174. The script's execution success does not remove this discrepancy. The attribution check remains a direct comparison against the values transcribed from the cited exp_174 table: 2.047× is listed for B `qo`, not A `ok` (listed as 1.930×).

No source transcription or historical output was changed. The result remains methodological; it is not evidence of decipherment.
