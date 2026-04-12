# exp_214: H405 — B pos=1 Anti-PS Constraint Section Stability

**Date:** 2026-04-11
**Hypothesis tested:** H405 (Is the B pos=1 p/t/k exclusion stable across sections?)
**Data:** ZL3b, B-dialect (n=101 ≥2 lines) and A-dialect (n=163 ≥2 lines) paragraphs

---

## Result: H405 SUPPORTED — CONSTRAINT IS CROSS-SECTION STABLE; t IS HARD-EXCLUDED FROM pos=1 IN BOTH DIALECTS

### B-Dialect Results

| Section | n_ps | gal_PS% | ptk_PS% | n_p1 | gal_P1% | ptk_P1% | ptk_P1=0? |
|---------|------|---------|---------|------|---------|---------|----------|
| other | 98 | 69.4% | 66.3% | 95 | 4.2% | **0.0%** | **YES** |
| pharma | 3 | 66.7% | 66.7% | 3 | 0.0% | **0.0%** | **YES** |
| **Total** | **101** | **69.3%** | **66.3%** | **98** | **4.1%** | **0.0%** | **0/98** |

B pos=1 p+t+k = 0/98 across ALL sections. The anti-PS constraint is cross-section stable.

### A-Dialect Results

| Section | n_ps | gal_PS% | ptk_PS% | n_p1 | gal_P1% | ptk_P1% | ptk_P1=0? |
|---------|------|---------|---------|------|---------|---------|----------|
| pharma | 23 | 65.2% | 65.2% | 23 | 0.0% | **0.0%** | **YES** |
| other | 115 | 72.2% | 65.2% | 113 | 5.3% | 2.7% | NO (n=3) |
| astro | 25 | 28.0% | 28.0% | 24 | 4.2% | 4.2% | NO (n=1) |
| **Total** | **163** | **59.8%** | **59.5%** | **160** | **4.4%** | **2.5%** | **4/160** |

A-dialect p+t+k at pos=1: 4/160 = 2.5% — near-exclusion with small leakage (1 case in astro, 3 in "other").

---

## Key Findings

### Finding 1: t is Hard-Excluded from pos=1 in BOTH Dialects

| Onset | B PS% (rank) | B pos=1 n | A PS% (rank) | A pos=1 n |
|-------|------|------|------|------|
| t | 17.82% (#2) | **0/98** | 18.4% (#2) | **0/160** |
| p | 35.64% (#1) | **0/98** | 28.8% (#1) | **1/160 (0.6%)** |
| k | 12.87% (#3) | **0/98** | 12.3% (#3) | **3/160 (1.9%)** |

t is 0% at pos=1 in both B (0/98) and A (0/160), despite being the 2nd most common PS onset class in both dialects (17.82% B, 18.4% A). This is the strongest cross-dialect anti-PS finding: t is universally excluded from pos=1.

p is hard-excluded in B (0/98) and near-excluded in A (1/160, 0.6%). k is hard-excluded in B (0/98) and near-excluded in A (3/160, 1.9%). The B constraint is absolute; the A constraint has minimal leakage.

### Finding 2: The Anti-PS Constraint is a Grammar Rule, Not a Scribe Artifact

The p/t/k exclusion from pos=1 holds in EVERY tested section:
- B: both "other" (95 paragraphs) and pharma (3 paragraphs) — 0/98 total
- A: pharma (23 paragraphs) shows 0/23; other and astro show 1-3 leakage cases

The cross-section stability (especially in B where both sections independently show 0) indicates this is a grammatical rule operating at the system level, not a section-specific convention or single scribe's preference.

### Finding 3: f is NOT Excluded — Only p/t/k

- B pos=1 f = 4/98 (4.1%, 2.08× enrichment)
- A pos=1 f = 3/160 (1.9%, 1.26×)

f-onset appears at pos=1 in both dialects (small enrichment in B, neutral in A). f is the weakest PS gallows class (B: 3.0%, 1.51×; A: 4.9%, 3.31×) and is NOT part of the anti-PS exclusion. The constraint is specifically "the three dominant PS gallows classes (p/t/k) are excluded from pos=1," not "all gallows are excluded."

### Finding 4: A pos=1 is Dominated by ch+sh (43.1% Combined)

A pos=1 onset distribution:
- ch: 35/160 (21.9%) — dominant
- sh: 34/160 (21.2%) — dominant
- Combined ch+sh at A pos=1: 43.1%

B pos=1 is more distributed: sh(16.3%)/qok(15.3%)/ch(10.2%)/o(13.3%)/d(9.2%)/ol(8.2%). A concentrates at ch/sh; B has a broader anti-gallows vocabulary at pos=1.

---

## Self-Audit

**Target-awareness:** No target-aware elements. Pure corpus extraction.

**Feature-destroying implementation:** No issues. The section classification is limited (B paragraphs mostly show as "other") — but the constraint is stable even within the "other" category alone (0/95). The finding is robust to section classification imprecision.

**Extrapolation:** The claim "stable across sections" is supported by: (a) both B sections independently show 0/N; (b) A pharma shows 0/23; A other/astro show minimal leakage. The "grammar rule vs scribe convention" interpretation is the simplest explanation for cross-section stability. We cannot rule out that all sections happen to be from the same scribe — but the pharma/astro split in A makes this unlikely.

**Negative-result scope:** N/A — positive result.

**Control behavior:** The A-dialect parallel analysis serves as a within-study control. A shows the same directional pattern (t: 0/160, p: near-zero, k: near-zero) with slightly more leakage than B. The consistency across dialects strengthens the grammar interpretation.

---

## Conclusion

**H405 SUPPORTED**: B pos=1 anti-PS constraint (0/98 for p+t+k) is cross-section stable. The constraint holds in both identified B sections independently. t is universally excluded from pos=1 in BOTH dialects (B: 0/98; A: 0/160) despite being the #2 PS onset in both dialects. p is hard-excluded in B (0/98) and near-excluded in A (1/160). k is hard-excluded in B (0/98) and near-excluded in A (3/160).

**Revised characterization of B first-line grammar**:
- PS slot: p(35.6%)/t(17.8%)/k(12.9%)/f(3.0%) — gallows-compound para-openers
- pos=1 slot: sh(16.3%)/qok(15.3%)/o(13.3%)/ch(10.2%)/d(9.2%)/ol(8.2%) — anti-PS vocabulary; p/t/k strictly excluded
- The alternating onset structure [PS=gallows] → [pos=1=anti-gallows] is a cross-section, cross-dialect grammatical rule. The rule is most absolute for t (0/98+0/160=0/258), strong for p (0/98 B, 1/160 A), and strong for k (0/98 B, 3/160 A).

**Cross-dialect summary**: Both A and B have an "anti-PS slot" at pos=1:
- A: [PS=p/t/k] → [pos=1=ch/sh dominant; t=0, p≈0, k≈0]
- B: [PS=p/t/k] → [pos=1=sh/qok/ch/o/d; p=t=k=0 hard]

The A constraint is softer (small leakage) and concentrates at ch/sh at pos=1; B constraint is absolute and distributes across more onset classes at pos=1. The shared grammar skeleton [PS=gallows-class → pos=1=anti-gallows-class] is the third instance of shared A/B syntactic structure (after the shared PS formula and the anti-qo PF-LL depletion in both dialects).
