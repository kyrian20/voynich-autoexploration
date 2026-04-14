# Proposed Amendment: C007

**Written by:** Cryptanalyst agent  
**Date:** 2026-04-12  
**Based on:** exp_573 (C007 reconciliation)  
**Status:** Proposed — awaiting human review and approval before any update to committed_claims.md

---

## Current C007 Text

> **C007: Onset self-succession ranges from 1.24× to 2.05× and survives position control**
> **Claim**: Onset self-succession (the tendency for consecutive words to share an onset class) ranges from 1.24× (qok, B-dialect) to 2.05× (ok, A-dialect) across six class-by-dialect combinations. This self-succession survives position control (within-stratum analysis controlling for line-position effects), with residuals ≥ 1.2× across all tested onset-by-dialect combinations.
> **Supporting experiments**: exp_164, exp_174
> **Contradiction condition**: A re-analysis showing that position control reduces self-succession residuals to < 1.1× for the majority of onset-by-dialect combinations would contradict this claim.

---

## Issues Identified (exp_573)

### Issue 1: Range is incorrect (both bounds wrong)

**Lower bound "1.24× (qok, B-dialect)"**: Under canonical methodology (exp_565), B qok self-succession = 1.03× (flat, no significant self-succession signal). The 1.239× in exp_174 was computed with folio-level dialect assignment and the old formula (E = obs/(total×rate²)); canonical per-line dialect assignment + canonical formula gives 1.03×.

**Upper bound "2.05× (ok, A-dialect)"**: This is a misattribution. In exp_174's own table, A ok = 1.930× and B qo = 2.047×. The stated "2.05×" appears to conflate B qo (2.047) with A ok. Under canonical methodology, the highest CONF self-succession values (obs≥10) are A ol=3.20×, A ot=2.23×, B y=3.16×, B l=2.62×.

### Issue 2: "Residuals ≥1.2× across all tested combinations" is false

Under canonical methodology, the following combinations are below 1.2×:
- B qok: 1.028× (flat)
- B ch: 0.906× (near-DEPL)
- B sh: 0.781× (near-DEPL)
- A qok: 1.270× (sub-threshold but above 1.2)
- A ok: 1.421×, A sh: 1.212× (flat)

The claim "residuals ≥1.2× across all tested combinations" fails for at least three class-by-dialect combinations under canonical methodology.

### Issue 3: What remains valid

The positive core of C007 is valid: many onset classes DO show robust self-succession that survives position control. Specifically, y, l, ot, qo, qot show CONF self-succession in both dialects (E=1.69–3.86×). The mechanism class evidence (C002: substitution alone produces ss≈1.0) depends on self-succession being present, which it clearly is for the strongest classes. These findings remain unchallenged.

---

## Proposed Corrected Language

> **C007 (REVISED): Onset self-succession exists in many onset classes but is class-specific, not universal**
> 
> **Claim**: Onset self-succession (the tendency for consecutive words to share an onset class) varies substantially across onset classes and dialects under canonical methodology. Classes with confirmed (CONF) self-succession in both A and B dialects: y (A:1.88×, B:3.16×), l (A:3.86×, B:2.62×), ot (A:2.23×, B:2.10×), qo (A:1.76×, B:1.82×), qot (A:3.16×, B:1.69×). Classes with flat or depleted self-succession: B qok (1.03× — flat), B ch (0.91×), B sh (0.78×). The overall range across onset-class-by-dialect combinations (obs≥10) is approximately 0.78× – 3.86×, compared to the original claim of 1.24–2.05×.
>
> The position-control finding (exp_174) remains valid for CONF self-succession classes: the enrichment is not explained by positional co-occurrence. However, B qok's 1.03× flatness means it is not a CONF self-succession class under canonical methodology, contradicting the original claim that B qok falls within the self-succession range.
>
> The original C007's upper bound "2.05× (ok, A-dialect)" was a misattribution; in exp_174 the value 2.047 belongs to B-dialect qo, not A-dialect ok.
>
> **Supporting experiments (original)**: exp_164, exp_174  
> **Reconciling experiments**: exp_565 (B qok=1.03×), exp_567 (A ok=1.42×), exp_573 (reconciliation)  
> **Revised contradiction condition**: A re-analysis showing that position control reduces self-succession residuals to <1.1× for the majority of **CONF** onset-by-dialect combinations (y, l, ot, qo, qot in both dialects) would contradict this revised claim.

---

## Implications for Dependent Claims and Findings

**C002 (substitution alone gives ss≈1.0)**: Not affected. C002's claim compares VMS ss_mean (~1.465) against substitution-only ss≈1.0. The revised C007 confirms that strong self-succession classes (y, l, ot etc.) pull ss_mean well above 1.0, supporting C002. If anything, the broader range under canonical (up to 3.86×) makes C002's contrast stronger.

**The 19/19 architecture (C003, C004)**: The architecture uses ss_mean as one of 19 metrics. The revision doesn't affect the architecture's performance, since ss_mean aggregates across all classes and the CONF classes (which dominate ss_mean) remain valid.

**exp_174's position-control claim**: Remains valid as a general finding for CONF classes. Recommend citing it as "onset self-succession survives position control for classes with confirmed self-succession (y, l, ot, qo, qot)" rather than "for all tested classes."

**F171 (qot→qot diverse pairs)** and related findings: Not affected — individual class characterizations are not dependent on C007's universal range claim.

---

## Recommendation

1. Update C007 in committed_claims.md with the revised language above.
2. Note: The contradiction condition from original C007 has been met for B qok (1.03× < 1.1×), but this is the expected outcome of the reconciliation rather than a discovery in new data.
3. If any papers or preprints have been submitted citing "onset self-succession 1.24–2.05×," the corrected range should be stated as "0.78–3.86× across onset-class-by-dialect combinations" with the caveat that only a subset of classes shows CONF (≥1.5×/obs≥10) self-succession.
