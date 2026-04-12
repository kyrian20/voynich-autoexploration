# exp_300: A-Dialect Onset Class Characterization
**Date:** 2026-04-11
**Hypothesis:** Phase 6 parallel — does A-dialect have the same three-tier onset class taxonomy as B? What are A-dialect closed paradigm sizes?
**Script:** script.py
**Data:** eva_zl3b.txt

---

## Result: A-DIALECT SHARES SAME DIRECTIONAL TAXONOMY BUT WITH MUCH LARGER CLOSED PARADIGMS

A-dialect onset classes fall into the same directional categories as B (LF grammar-words, LL-terminal, MID-enriched template classes), but A's template-onset classes have 3-4× LARGER closed paradigm percentages. A-dialect lacks B's extreme template concentration: no A-dialect onset class achieves <25% hapax rate (B-qok: 57%), and A-qok requires 71 types for 90% token coverage vs B-qok's 32 types.

---

## Key Findings

### 1. I(onset;position): Consistent with exp_293

| Dialect | I(onset;pos) | Z-score | % of H(pos) |
|---------|-------------|---------|-------------|
| A       | 0.097 bits  | 153     | 7.8%        |
| B       | 0.137 bits  | 450     | 13.1%       |

A-dialect value exactly matches exp_293's 0.096 bits (confirming the measurement). B remains 1.4× higher onset-position coupling.

### 2. Grammar-word LF classes (cross-dialect consistency)

| Onset | A LF-enr | B LF-enr | In A? | In B? |
|-------|----------|----------|-------|-------|
| p     | 4.02×    | 6.03×    | yes   | yes   |
| f     | 2.70×    | 1.82×    | yes   | border|
| t     | 2.45×    | 3.51×    | yes   | yes   |
| y     | 2.28×    | 3.49×    | yes   | yes   |
| s     | 2.23×    | 4.79×    | yes   | yes   |
| d     | 1.10×    | **2.29×**| no    | **yes** |

Core grammar-word LF classes {p, t, y, s} are consistent across dialects. **d-onset is the major cross-dialect divergence**: LF-enriched in B (2.29×) but nearly neutral in A (1.10×). This matches F060 (d-onset lines in A mark line endings rather than beginnings).

### 3. Line-terminal LL classes (cross-dialect differences)

| Onset | A LL-enr | B LL-enr | In A? | In B? |
|-------|----------|----------|-------|-------|
| r     | 2.39×    | 2.37×    | yes   | yes   |
| d     | **1.72×**| 1.36×    | **yes**| border |
| ol    | 1.60×    | 1.93×    | yes   | yes   |
| o     | 1.14×    | 1.69×    | border| yes   |
| l     | 0.95×    | **1.62×**| no    | **yes** |
| cth   | 1.45×    | **1.53×**| border| **yes** |

**r** and **ol** are consistently LL-terminal in both dialects. **d** is more LL-enriched in A (1.72×) than B (1.36×) — d-onset words mark line endings in A-dialect (F060: -dy, -al, -am words LL-enriched in A). **l** is LL-terminal only in B. **cth** borderline in both.

### 4. Template-onset classes — CROSS-DIALECT PARADIGM SIZE DIVERGENCE (critical)

| Onset | A ZeroMid | B ZeroMid | A CP90% | B CP90% | A Hapax | B Hapax |
|-------|-----------|-----------|---------|---------|---------|---------|
| qok   | 44.1%     | **78.4%** | **57.3%** | **18.2%** | 61.3% | 56.8% |
| ok    | 47.4%     | **68.2%** | **58.9%** | **33.8%** | 61.7% | 64.1% |
| ot    | 46.4%     | **66.7%** | **67.6%** | **39.0%** | 72.1% | 68.5% |
| qot   | 40.0%     | **69.7%** | **66.3%** | **39.3%** | 62.8% | 55.6% |
| ch    | 40.0%     | 39.8%     | **58.4%** | **46.8%** | 67.5% | 66.7% |
| sh    | 40.4%     | 51.4%     | **60.6%** | **43.3%** | 69.7% | 66.3% |

**B-dialect has dramatically smaller closed paradigms for qok/ok/ot/qot**: B needs only 18-39% of vocabulary types for 90% coverage; A needs 58-68%. For qok: A requires 71 types vs B's 32 types — A needs 2.2× more types for the same coverage fraction.

The A-B ZeroMid difference is clearest for qok (A=44.1% vs B=78.4%) and ok (A=47.4% vs B=68.2%) — B has dramatically more ZeroMid (onset+suffix) templates than A.

**Interpretation**: B-dialect is more template-standardized. B qok/ok/ot/qot classes converge on a small set of onset+suffix combinations (mostly ZeroMid); A retains more midfix diversity spreading token mass across more word types.

### 5. Top suffix cross-dialect (template classes)

| Onset | A top suffix | B top suffix |
|-------|-------------|-------------|
| qok   | ol (19.4%)  | edy (13.4%) |
| ch    | ol (18.8%)  | edy (17.0%) |
| ok    | ol (17.9%)  | aiin (12.8%)|
| d     | aiin (34.6%)| aiin (22.5%)|

A-dialect template classes predominantly use **-ol/-or** suffix; B uses **-edy/-eedy** suffix. This is the fundamental suffix paradigm shift that defines the A/B distinction (exp_023, F035).

### 6. A-dialect taxonomy FAILS template threshold

The B-dialect definition of "template-copying" (MID>1× AND hapax<25%) finds **no A-dialect onset class**. A's MID-enriched classes (ch=1.19×, sh=1.18×, qo=1.23×) all have 60-80% hapax rates. A-dialect template-onset classes exist directionally but with much higher hapax rates — A's "templates" are less concentrated, requiring more types.

**Revised cross-dialect taxonomy:**
- "Template-copying" classes are those with MID-enrichment (ch/sh/ok/ot/qok/cth) in BOTH dialects — the defining feature is positional preference (MID), not hapax rate
- B-dialect adds an extra layer of type-concentration onto the same positional structure
- A-dialect = same positional grammar, broader vocabulary per onset class

### 7. l-onset: highest hapax rate in A

A-dialect l-onset: hapax=89.3%, CP90=89.3%, N=64 tokens. This is the most hapax-dense onset class in A-dialect. l-onset in A is essentially entirely hapax words — each occurrence is a novel word. This matches F296's finding for B (B-l hapax=67.7%) but A is even more extreme.

---

## Summary Table

| Feature | A-dialect | B-dialect |
|---------|-----------|-----------|
| I(onset;pos) | 0.097 bits (7.8%) | 0.137 bits (13.1%) |
| Grammar-word LF | p/f/t/y/s | p/s/t/y/d |
| LL-terminal | r/d/ol | r/ol/o/l/cth |
| Template-onset classes | ch/sh/ok/qok (MID>1×) | ch/sh/ok/qok/ot (MID>1×) |
| qok CP90% | 57.3% (71 types) | **18.2% (32 types)** |
| Top suffix (qok) | ol/19.4% | edy/13.4% |
| Template hapax floor | >60% (no class <25%) | qok=57% (still high) |

---

## Self-Audit

1. **Validity**: Same script as B-dialect Phase 6 analysis, applied to A-dialect folios. I(onset;pos) matches prior measurement. Three-category taxonomy thresholds are the same as for B. ✓
2. **Surprising**: A-dialect's three-category taxonomy finds NO template-copying class by the strict threshold (MID>1× AND hapax<25%). The MID-enriched classes in A have 60-80% hapax — comparable to B's grammar-word classes. B's low-hapax template classes (qok=57%) are NOT present in A at the same concentration level.
3. **Battery impact**: None — descriptive characterization.
4. **Committed claims**: No committed claims reference A-dialect closed paradigm sizes. ✓
5. **New hypotheses**: None needed — this completes the Phase 6 cross-dialect parallel.

---

## Finding

See F302 in findings.md.
