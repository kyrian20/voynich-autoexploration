# Synthesis Audit: working_position.md vs. exp_170–175 Results
**Date**: 2026-04-10
**Method**: Line-by-line comparison of working_position.md against each experiment's result.md. All numbers verified against the actual script output or result tables.

---

## VERDICT: One significant overstatement, three minor issues, two understated findings.

---

## SIGNIFICANT OVERSTATEMENT

### 1. Long-range MI (lags 10-12) presented as "genuine long-range structure" — NOT supported by the within-line shuffle comparison

**What the synthesis says** (Section 2, exp_175 block):
> "then above Timm at lags 10-12 (genuine long-range structure in long lines)"

**What the synthesis says** (Section 4, structured grammar block):
> "long-range MI (lags 10-12) is above Timm (consistent with within-line structural coherence in long lines)"

**What exp_175 actually shows**:
At lags 11-12, the within-line shuffled VMS produces **higher MI than real VMS**:
- Lag 11: VMS/Within = 0.825 (shuffle > real)
- Lag 12: VMS/Within = 0.873 (shuffle > real)

This directly contradicts the "genuine long-range structure" characterization. If real VMS has less MI at lags 11-12 than a within-line shuffle of the same corpus, the excess over Timm cannot be attributed to sequential structure in the VMS — it is more likely a sampling artifact (only the longest lines contribute lag-10+ pairs, and Timm's line-length distribution may differ from VMS at the extremes).

exp_175's own Finding 5 states: "most sequential structure in B-dialect is concentrated at lag 1" and "most sequential structure in B-dialect is concentrated at lag 1 (nearest neighbors). The mid-range structure (lags 2-7) is NOT higher than shuffle baseline." The synthesis does not include this finding. The exp_175 caveat ("the sample is biased toward long lines") is also absent from the synthesis.

**Correct characterization**: VMS MI at lags 10-12 is above Timm CI, but is simultaneously below the within-line shuffle at lags 11-12. The net interpretation is that VMS lacks long-range sequential structure beyond lag 1-2, and the lags 10-12 Timm discrepancy is more plausibly a sampling artifact than evidence of genuine long-range grammar. The synthesis should present the MI finding primarily as the lag-1 ABOVE and lags 2-7 BELOW results, which are the internally consistent findings. The lags 10-12 ABOVE Timm result should be flagged as uncertain.

**Severity**: Significant. The synthesis uses the lags 10-12 result to support the structured-grammar verdict in Section 4. That support is not valid given the shuffle comparison.

---

## MINOR OVERSTATEMENTS

### 2. "14/16 metrics ABOVE or BELOW" for Naibbe cipher

**What the synthesis says**:
> "14/16 metrics are ABOVE or BELOW the cipher CI (only 2 informatively inside, both trivially)"

**What exp_170 actually shows**:
The INSIDE/OUTSIDE COUNTS table in exp_170 shows:
- Ital-A: 3 INSIDE, 13 outside (10 ABOVE + 3 BELOW)
- Ital-B: 4 INSIDE, 12 outside
- Lat-A: 4 INSIDE, 12 outside
- Lat-B: 4 INSIDE, 12 outside

The raw count is **12-13/16 outside**, not 14/16. The "14/16" figure is derived by subtracting the 2 non-informative INSIDEs that exp_170 identifies (daiin→cth: both VMS-B and Naibbe are ~0 because this is an A-dialect finding; k@para-start: parsing issue producing 94% para-start rate). After removing those, the informative-INSIDE count is 2, giving 14/16 informatively outside.

The synthesis correctly cites "only 2 informatively inside, both trivially" as the qualifier — so the logic is right — but the summary "14/16 ABOVE or BELOW" reads as the raw count, which it is not. A careful reader would not infer the qualification from the sentence structure.

**Correct phrasing**: "12-13/16 raw OUTSIDE; 14-15/16 after removing 2 non-informative INSIDE cases" or "only 2 informative INSIDEs (of 16 metrics)."

**Severity**: Minor. The underlying logic is accurate, just the presentation conflates informative-only with raw counts.

### 3. Naibbe self-succession range "~0.84-0.89" omits ok≈0.96

**What the synthesis says**:
> "Onset self-succession: VMS enriched (qok=1.24×, ok=1.46×, ch=1.69×), Naibbe depleted (~0.84-0.89×)"

**What exp_170 actually shows** (Lat-B condition):
- qok self-succession: Naibbe=0.886 ✓ (within range)
- ok self-succession: Naibbe=0.964 (near-baseline, not ~0.84-0.89)
- ch self-succession: Naibbe=0.867 ✓ (within range)
- d self-succession: Naibbe=1.046 (INSIDE, not depleted)

The "~0.84-0.89" range accurately describes qok and ch but excludes ok (0.964) and d (1.046). The exp_170 summary table confirms ok self-succession is ABOVE in all 4 conditions — meaning VMS is enriched relative to Naibbe — but Naibbe's ok value is close to baseline (0.96), not depleted to 0.84-0.89. Describing all onset self-succession as "~0.84-0.89" misrepresents Naibbe's performance on ok specifically.

**Correct phrasing**: "Naibbe self-succession range: qok≈0.84-0.89×, ch≈0.81-0.89×, ok≈0.96× (near-baseline), d≈1.0-1.05× (INSIDE in most conditions)."

**Severity**: Minor. The directional conclusion (VMS self-succession ABOVE Naibbe for all three onset classes) is correct. The numeric range misrepresents the variation.

### 4. "d self-succession varies 9-fold" — actually ~8.6-fold

**What the synthesis says** (exp_174 block):
> "d: 2.1% (LF→second) → 18.0% (MID→LL)"

The ratio is 18.0/2.1 = 8.57×, presented as "9-fold" in the table and "9-fold" in the structured grammar discussion. The underlying numbers are correctly cited (2.1% and 18.0%); the summary description as "9-fold" rounds up. This is trivially minor but included for completeness.

---

## UNDERSTATED FINDINGS

### 5. exp_175 Finding 5 not in synthesis: "most sequential structure concentrated at lag 1"

**What exp_175 says** (Finding 5):
> "most sequential structure in B-dialect is concentrated at lag 1 (nearest neighbors). The mid-range structure (lags 2-7) is NOT higher than shuffle baseline. This is inconsistent with long-range dependencies from syntax."

This is a significant interpretive result: VMS B-dialect does NOT show the slowly-decaying MI of natural language syntax. Most of its sequential signal is nearest-neighbor only. The synthesis presents the MI results as evidence for "strong local onset-class grammar" (accurate) but does not include the observation that this means VMS B-dialect lacks long-range dependency structure characteristic of natural language syntax. This is relevant to the "what cannot yet be determined" section (whether VMS encodes language) and weakens the natural-language interpretation relative to an artificial structured system.

**Why it matters**: If VMS is a natural language, we might expect multi-lag MI decay, not near-total concentration at lag 1. The rapid decay is more consistent with an artificial structured system with adjacent-word rules than with natural language syntax.

### 6. A-dialect cth LF depletion (0.145×) not cited in structured grammar evidence

**What exp_174 shows** (H4, A-dialect):
| cth | LF rate 0.0055 | Global rate 0.0377 | Enrichment **0.145** |

The A-dialect cth LF depletion (0.145×) is one of the strongest positional onset effects in the entire dataset — cth words are nearly seven times LESS common at line-first positions than their overall frequency would predict. This appears in exp_174's H4 analysis but is not cited in the synthesis's evidence for structured grammar. The synthesis mentions "cth LF depletion" in the summary of exp_170/173 but does not connect it to the exp_174 position-control result showing this depletion survives position control.

---

## ACCURATE CLAIMS (VERIFIED)

The following key claims were checked against experiment outputs and are accurate:

- exp_171: Timm identical adjacent word rate=0.037, VMS=0.009 ✓ (4.1× ratio)
- exp_171: qok self-succession Timm=1.532, VMS=1.239; ch Timm=2.410, VMS=1.694 ✓
- exp_171: TTR Timm=0.203, VMS=0.284 ✓; mean word length Timm=5.039, VMS=5.768 ✓
- exp_172: Random 80/20 A=18/19 PASS, B=14/19 PASS ✓; leave-cosmo=10/19 FAIL at n=32 ✓
- exp_173: 24/30 Bonferroni survivors, 26/30 BH-FDR ✓; all key positional metrics survive ✓
- exp_173: -am LL (B) p=6.27e-161, y-onset LF (A) p=8.38e-40, y-onset LF (B) p=2.86e-90 ✓
- exp_174: -am LL B-dialect enrichment=6.856× ✓; al=0.913, edy=0.346, ol=0.593 all <1 ✓
- exp_174: B-dialect LF y=3.478×, s=4.389×, t=2.749×; ch=0.291×, ch_e=0.320× ✓
- exp_174: d self-succession B LF→second=0.021 (2.1%), MID→LL=0.180 (18.0%) ✓
- exp_174: qok→ch position-controlled A=1.242, B=1.248 ✓
- exp_174: Position-controlled self-succession all ≥1.2× across onsets and dialects ✓
- exp_175: VMS B lag-1 MI=0.085, Timm mean=0.063, ABOVE CI ✓
- exp_175: VMS B lags 2-7 all BELOW Timm CI ✓
- exp_175: Within-line shuffle ratio at lag 1: B=2.705 (63% MI destroyed) ✓
- Naibbe correctly reproduces vocabulary composition (edy rate, l-onset) — by design ✓

---

## SUMMARY TABLE

| Issue | Type | Severity | Location in synthesis |
|-------|------|----------|-----------------------|
| Lags 10-12 "genuine long-range structure" — shuffle comparison contradicts | Overstatement | **Significant** | Sec. 2 (exp_175), Sec. 4 (structured grammar) |
| "14/16 outside" conflates informative with raw count | Minor overstatement | Minor | Sec. 4 (cipher verdict) |
| Naibbe self-succession "~0.84-0.89" omits ok≈0.96 | Minor overstatement | Minor | Sec. 2 (exp_170) |
| "9-fold" should be ~8.6-fold | Rounding | Trivial | Sec. 2 (exp_174) |
| Finding 5 (lag-1 concentration) absent from synthesis | Understatement | Moderate | Missing from MI interpretation |
| A-dialect cth LF depletion (0.145×) not cited | Understatement | Minor | Missing from structured grammar evidence |

---

## RECOMMENDED CORRECTIONS

1. **For the synthesis document**: Revise the lags 10-12 MI interpretation to note that the within-line shuffle exceeds real VMS at lags 11-12, making the "ABOVE Timm" result ambiguous as evidence for long-range structure. The MI finding should be characterized primarily as: (a) VMS lag-1 MI is above Timm (strongest finding), and (b) VMS lags 2-7 MI is below Timm (key negative result for self-citation). The lags 10-12 result should be presented as uncertain.

2. **For the synthesis document**: Add a note to "What Cannot Yet Be Determined" that VMS B-dialect MI concentrates at lag 1 with rapid decay — which is inconsistent with natural language long-range syntactic dependency, weakening (though not ruling out) the natural-language interpretation.

3. **Minor number corrections** can be noted but do not affect the theory discrimination verdicts.
