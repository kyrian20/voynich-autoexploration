# exp_410: B Bracket Grammar

**Hypothesis (H634):** A has general bracket structure (F413: y/d/k/p same-onset brackets). B p is anti-bracket (F404). Does B show bracket structure for any LF class?

**Method:** Applied same exp_409 methodology to B cont lines (len≥4). For each B LF class with N≥10: compute (pos1=X, LL=Y) joint enrichment vs independence.

**N:** 2211 B cont lines (len≥4).

---

## Results: B same-onset brackets (pos1=LL=X) with E≥2.0, N≥3

| LF  | N_lf | pos1=LL=X | N_joint | Expected | E_bracket |
|-----|------|-----------|---------|----------|-----------|
| p   | 228  | ch→ch     | 4       | 1.2      | 3.38× (dir) |
| t   | 198  | sh→sh     | 4       | 1.2      | 3.33× (dir) |
| qok | 229  | sh→sh     | 3       | 1.0      | 2.97× (dir) |
| qok | 229  | ol→ol     | 4       | 1.4      | 2.84× (dir) |
| s   | 255  | qok→qok   | 6       | 2.2      | 2.78× |
| y   | 260  | ch→ch     | 13      | 7.0      | 1.85× |
| qok | 229  | ch→ch     | 12      | 7.5      | 1.59× |
| d   | 335  | sh→sh     | 4       | 3.2      | 1.24× (near-baseline) |

## A/B Contrast: Same-Onset Brackets for Key LF Classes

| LF | A E (same-onset onset) | B E (same-onset onset) | Contrast |
|----|------------------------|------------------------|---------|
| d  | sh: 3.78×(N=4)         | sh: 1.24×(N=4)         | A >> B: A d sh-bracket, B d no bracket |
| y  | y: 5.21×(N=3)          | y: — (not detectable)  | A >> B: A y self-bracket, B y absent |
| p  | sh: 2.06×(N=4)         | sh: 0.44×(anti,F404); ch: 3.38×(N=4) | OPPOSITE: A p sh-bracket / B p ch-corr |
| t  | sh: 2.76×(dir,N=2)     | sh: 3.33×(N=4)         | SHARED: t sh-bracket in both dialects |
| s  | — (no bracket)         | qok: 2.78×(N=6)        | B-specific: B s qok-bracket |
| k  | ch: 3.04×(N=4)         | — (N=32, no bracket at N≥3) | A-specific: A k ch-bracket |

## Key Findings

**B DOES have bracket structure but it is different from A's:**

1. **B s qok-bracket (E=2.78×, N=6):** B s-LF lines that open with qok at pos1 also close with qok at LL. This is the strongest N≥3 B same-onset bracket. In A, s-LF shows no bracket.

2. **B t sh-bracket (E=3.33×, N=4, dir):** B t-LF lines that open with sh at pos1 also close with sh at LL. Mirrors A t sh-bracket (E=2.76×, N=2, dir). The t sh-bracket may be shared across dialects.

3. **B p ch-correlation (E=3.38×, N=4, dir):** B p-LF lines have ch depleted at both pos1 (0.42×) and LL (0.47×). But when ch DOES appear at pos1, it correlates with ch at LL (E=3.38×). This is a conditional correlation among rare events — not a bracket in the same sense as A p sh-bracket (where sh is enriched at both positions).

4. **B d sh-bracket ABSENT (E=1.24×):** A d sh-bracket is strong (E=3.78×, F413). B d sh: near-baseline (E=1.24×). This is a clear A/B inversion.

5. **B y y-bracket ABSENT:** A y self-bracket is E=5.21×(N=3, F413). In B, y same-onset bracket for y: not detected (all B y same-onset brackets are for ch=1.85×, not y). This matches F401: A y-self-chains extend, B y-self-chains terminate.

---

## Interpretation

**B bracket grammar exists but is structurally different from A's.** The key distinction:

- **A bracket grammar**: sh-bracket shared by multiple classes (d, p, t), y-bracket, k ch-bracket. The sh-bracket is A's dominant bracket type (appears for the two most common A LF classes: d and p).

- **B bracket grammar**: No dominant sh-bracket. Instead: s qok-bracket (unique to B), t sh-bracket (possibly shared with A), p ch-correlation (a depletion-conditional pattern, not a full bracket). B's brackets are weaker, more varied, and involve different onset classes.

The **A/B bracket taxonomy** now has four discriminating differences:
1. A d sh-bracket (E=3.78×) vs B d no-sh-bracket (E=1.24×) — strongest A/B inversion
2. A y y-bracket (E=5.21×) vs B y no-y-bracket — consistent with A y-chain / B y-chain termination
3. A p sh-bracket (E=2.06×) vs B p sh-ANTI-bracket (0.44×) — established F404
4. B s qok-bracket (E=2.78×) — B-specific, not found in A

The t sh-bracket may be shared (A: 2.76×, N=2; B: 3.33×, N=4) — both directional, but consistently present.

---

## Limitations

- All B same-onset brackets: N=3-6, all directional.
- B p ch-correlation: N=4, dir. The ch-ch "bracket" is among rare events (ch depleted in p-lines), so it may reflect small-N variation rather than grammar.
- B s qok-bracket (E=2.78×, N=6): strongest B bracket. Still small N but matches the B s formula type (s→sh→qok is a B formula type, F398/F405 — s-LF lines have strong qok routing).
- Multiple testing: exploratory sweep.

---

## Self-Audit

**Target-awareness**: No target-aware elements.

**Feature-destroying implementation**: Not applicable — observational study.

**Extrapolation**: All results stated as directional where N<6. No "structural" or "cannot" claims. The B d sh-bracket absence (E=1.24×) is stated as "near-baseline," not "no bracket possible."

**Negative-result scope**: "B d sh-bracket not detected at E≥1.5, N≥3" — does not rule out a weaker bracket at larger N.

**Control behavior**: Independence model serves as null. No surprises in model behavior.

---

## Conclusion

B has bracket structure (s qok-bracket, t sh-bracket, p ch-correlation) but it is structurally different from A. A's dominant sh-bracket (d and p) is absent in B. A's y-bracket is absent in B. B has its own B-specific bracket (s→qok). The A/B bracket grammar distinction is a concrete grammar-level difference: A uses sh as a line-framing onset across multiple LF classes; B does not. This adds to the A/B discrimination taxonomy alongside the five pos1 inversions (F408/F413).

## Follow-up Questions

- **H635**: B s qok-bracket characterization — for B s-LF lines with qok at pos1 AND qok at LL (N=6), what is the MID content? Is this related to B s→sh→qok formula type (F398)?
- The t sh-bracket (shared A and B) may reflect a t-onset structural constraint: t at LF → sh opens and closes the bracketed content regardless of dialect.
