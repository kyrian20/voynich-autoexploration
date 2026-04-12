# Commitments Audit — 2026-04-12

**Auditor:** Cryptanalyst loop (housekeeping session)
**Scope:** All committed claims C001–C009 as of 2026-04-12

---

## Audit Procedure

Each claim's headline number was verified against its supporting experiment's result.md. Three new claims (C008, C009, and the C003 scope qualification) were applied from proposed_commitments/ to committed_claims.md in this session. Proposal files moved to state/proposed_commitments/applied/.

---

## C001: Position-blind mechanisms fail — max 1.1× am_ll

**Status:** MINOR IMPRECISION  
**Check:** exp_170 result.md shows max Naibbe am_ll ≈ 1.062×. The committed "1.1×" is a rounded upper bound.  
**Verdict:** Acceptable rounding. No amendment needed. The claim's contradiction condition (≥3.0×) is unaffected.

---

## C002: Substitution alone produces ss_mean ≈ 1.00

**Status:** VERIFIED  
**Check:** exp_177 result.md confirms ss_mean ≈ 0.999.  
**Verdict:** Exact match. No issues.

---

## C003: Onset-replacing modification → 0/18 viable

**Status:** VERIFIED  
**Check:** exp_180 result.md confirms 0/18 viable combinations.  
**Verdict:** Exact match. No issues.  
**Note:** The "proposed_c003_qualification.md" from exp_579 was NOT applied to this entry. committed_claims.md C003 concerns onset-replacing modification (exp_180) — it is not the "19/19 PASS" claim that the qualification was written for. The section-heterogeneity qualification is instead incorporated as the Scope Qualification subfield of C008. This numbering mismatch arises because working_position.md uses an informal "C003 = 19/19 PASS" convention from the architecture phase, while committed_claims.md C003 = onset-replacing modification from the discrimination phase. This mapping is documented here; future readers should treat working_position.md C003 references as pointing to committed_claims.md C008.

---

## C004: Onset-preserving modification → 4/36 viable (lenient)

**Status:** VERIFIED  
**Check:** exp_181 result.md confirms 4/36 lenient viable, best cp=0.6/mp=0.8.  
**Verdict:** Exact match. No issues.

---

## C005: -am LL enrichment 6.811× (p < 10^-161)

**Status:** VERIFIED  
**Check:** exp_173 result.md confirms 6.811× at p=6.27e-161.  
**Verdict:** Exact match. No issues.

---

## C006: y-onset LF enrichment 3.506× (p < 10^-90)

**Status:** VERIFIED  
**Check:** exp_173 result.md confirms 3.506× at p=2.86e-90.  
**Verdict:** Exact match. No issues.

---

## C007: Self-succession range 1.24–2.05× — KNOWN ERRORS

**Status:** REQUIRES AMENDMENT (pending human approval)  
**Check:** exp_164 result.md shows B ot→ot=2.05× and B l→l=2.13×. The committed claim attributes 2.05× to "ok, A-dialect" — this is a misattribution. The stated maximum is also exceeded by 2.13×.  
**Three confirmed errors:**
1. Range "1.24–2.05×" wrong — canonical range is 0.78–3.86×
2. "2.05× (ok, A-dialect)" misattributed — belongs to B ot→ot (not A ok)
3. "residuals ≥1.2× for all" fails for B qok/ch/sh (lower residuals confirmed in exp_164/exp_174)

**Status in committed_claims.md:** Known-issue note added to C007 entry pointing to proposed_c007_amendment.md. Amendment text is in state/proposed_commitments/proposed_c007_amendment.md — awaiting separate human approval. This audit does NOT apply the amendment; it documents the issue.

---

## C008: 19/19 PASS + Architecture Specificity (NEW — applied this session)

**Status:** APPLIED (from proposed_c008_arch_specificity.md)  
**Supporting experiments:** exp_314, exp_574, exp_575, exp_576, exp_579  
**Key numbers verified:** 19/19 PASS (exp_314 N=30); 10/19 on fixed-param shuffled (exp_574); 16/19 intra best (exp_575); 14/19 inter best (exp_575); Section composition 97–107% of gradient (exp_579).  
**Scope qualification incorporated:** The proposed_c003_qualification.md (section heterogeneity, exp_579) is embedded as the "Scope qualification" subfield of C008. Not applied to committed_claims.md C003 (wrong entry; see C003 note above).

---

## C009: adj_rate Structure — Near-Random / Zero / Copy-Buffer Overproduction (NEW — applied this session)

**Status:** APPLIED (from proposed_c009_q007_adj_rate.md)  
**Supporting experiments:** exp_577, exp_578  
**Key numbers verified:** sh 1.11×/d 0.70×/ch 1.91× vs random; s: 0/452; t: 0/466; baseline sim overproduces sh 1.41×/ch 1.55×/d 1.79× (exp_578 N=5).  
**Scope note (preserved from proposal):** B-dialect only; exp_578 N=5 is low statistical power; ch is "above random" not "near-random" due to self-succession structure.

---

## Summary

| Claim | Audit Result |
|-------|-------------|
| C001 | Minor rounding, no amendment needed |
| C002 | Exact match ✓ |
| C003 | Exact match ✓ (C003 qualification → incorporated into C008) |
| C004 | Exact match ✓ |
| C005 | Exact match ✓ |
| C006 | Exact match ✓ |
| C007 | **ERRORS DOCUMENTED** — amendment in proposed_c007_amendment.md, awaiting human approval |
| C008 | Applied from proposal. Numbers verified. Scope qualification incorporated. |
| C009 | Applied from proposal. Numbers verified. B-dialect scope preserved. |

**Numbering note:** working_position.md section 8.1 uses an informal claim numbering (C001–C008) derived from the architecture phase. This numbering does NOT correspond 1:1 to committed_claims.md. Specifically: working_position.md "C003 = 19/19 PASS" maps to committed_claims.md **C008**. Future state updates should use committed_claims.md numbering (C001–C009) as canonical.
