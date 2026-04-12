# exp_437: Suffix Entropy vs Hapax Rate per Onset Class (H497 + H_new_B)

**H497:** Is onset-class suffix entropy correlated with hapax rate?
**H_new_B:** Is B-qok unusually edy-class suffix concentrated compared to other onset classes?

---

## Results

### A-dialect: suffix entropy vs hapax rate

| Onset | Tokens | Types | Hapax% | SufH | Type/Token |
|-------|--------|-------|--------|------|-----------|
| qok | 462 | 98 | 55.1% | 3.75 | 0.212 |
| cth | 295 | 56 | 60.7% | 3.10 | 0.190 |
| ch | 1556 | 350 | 62.3% | 3.69 | 0.225 |
| sh | 638 | 179 | 67.6% | 3.57 | 0.281 |
| d | 1134 | 216 | 72.2% | 3.56 | 0.190 |
| y | 504 | 214 | 64.0% | **4.25** | 0.425 |
| s | 210 | 97 | **77.3%** | **4.03** | 0.462 |
| ol | 186 | 76 | **73.7%** | 3.13 | 0.409 |

**A Spearman(SufH, hapax_rate) = 0.071** (no correlation)
**A Spearman(SufH, type/token) = 0.554** (moderate)

### B-dialect: suffix entropy vs hapax rate

| Onset | Tokens | Types | Hapax% | SufH | Type/Token |
|-------|--------|-------|--------|------|-----------|
| qok | 1916 | 142 | 56.3% | 3.77 | 0.074 |
| ch | 2391 | 427 | 60.0% | 3.93 | 0.179 |
| sh | 1258 | 221 | 60.6% | 3.71 | 0.176 |
| d | 988 | 208 | 70.2% | 3.81 | 0.211 |
| y | 503 | 215 | 68.8% | 4.17 | 0.427 |
| l | 828 | 231 | **61.9%** | **4.36** | 0.279 |
| ot | 908 | 158 | 69.6% | 4.00 | 0.174 |
| ok | 1026 | 148 | 60.1% | 3.91 | 0.144 |

**B Spearman(SufH, hapax_rate) = 0.242** (weak, not significant given N~18)
**B Spearman(SufH, type/token) = -0.035** (no correlation)

### H_new_B: B-dialect edy-class suffix fraction by onset class

| Onset | edy-class tokens | Total tokens | Fraction |
|-------|-----------------|-------------|---------|
| sh | 576 | 1258 | **45.8%** (HIGHEST) |
| qok | 775 | 1916 | **40.4%** |
| ch | 863 | 2391 | 36.1% |
| ok | 313 | 1026 | 30.5% |
| ot | 259 | 908 | 28.5% |
| y | 142 | 503 | 28.2% |
| ol | 130 | 820 | 15.9% |
| s | 20 | 409 | 4.9% |
| **d** | **42** | **988** | **4.3%** (LOWEST) |

---

## Interpretation

**H497 ANSWERED: Suffix entropy is NOT correlated with hapax rate (rho<0.25 in both dialects).** Onset classes with more diverse suffix inventories do not have proportionally more hapax word types. In A-dialect, SufH shows moderate correlation with type/token ratio (rho=0.554) but not hapax rate — suggesting that suffix diversity generates more word types per token (wider vocabulary spread) but not necessarily more unique-occurrence words. In B, the type/token correlation disappears entirely. No finding ID assigned.

**H_new_B ANSWERED: B-qok is NOT unusually edy-class concentrated.** sh (45.8%) is MORE edy-concentrated than qok (40.4%), and ch (36.1%) is similar. The edy-class suffix fraction reveals a structural split:
- **High-edy onset classes (template/gallows class)**: sh(45.8%), qok(40.4%), ch(36.1%), ok(30.5%), ot(28.5%), y(28.2%) — all use edy-class suffixes at 28-46%
- **Low-edy onset classes (content/rare class)**: d(4.3%), s(4.9%), ol(15.9%) — strongly prefer non-edy suffixes

The d-onset class is the MOST ANTI-EDY (4.3% vs expected ~35%). d words predominantly end in -aiin/-in/-ar (d+aiin=daiin, the most common B word). This structural split (template onsets prefer edy-class; content onsets prefer aiin/ar-class) is a pre-existing pattern in the literature but now quantified.

The sh-onset being the MOST edy-concentrated onset (45.8%) is notable: sh is the dominant "template/interface" class in B (F326: sh→qok bigram, sh at pos1 in many formula lines), and its suffix choices are dominated by edy-class (shedy=F326 driver).

**No new finding ID for H497 (null result). H_new_B answered: B-qok edy fraction is unremarkable; d-anti-edy (4.3%) is the most distinctive value. Assign F436 for the edy-class split finding.**

---

## Self-Audit

**Target-awareness**: No target-aware elements.
**Feature-destroying implementation**: No issues.
**Extrapolation**: "No correlation" claim qualified by small N (~15-18 onset classes). rho=0.07/0.24 not tested for significance.
**Negative-result scope**: H497 null result is within tested scope. Does not claim suffix entropy is never correlated with hapax rate — only that no strong correlation found in this data.
**Control behavior**: No control comparison. N/A.

---

## Conclusion

H497: Suffix entropy NOT correlated with hapax rate (rho<0.25). No finding ID.
H_new_B: B-qok edy fraction (40.4%) NOT unusual — sh=45.8% is higher; d=4.3% is lowest. Structural split: template onsets (sh/qok/ch/ok/ot) prefer edy-class; content onsets (d/s) prefer aiin/ar-class. **Assign F436.**
