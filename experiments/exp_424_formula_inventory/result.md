# exp_424: Updated B Formula Type Inventory

**Hypothesis (H646):** Compile the current confirmed B formula type inventory after exp_415-423 refinements.

**Method:** Standard E_cond = P(pos2|LF,pos1) / P(pos2|pos1), with 'other' onset filtering (consistent with exp_418 methodology). Report all trigrams with N≥5, E≥2.0, plus formula-typed fraction.

---

## Results

### Candidate trigrams — E_cond with standard pos1-conditional baseline

| Trigram | N_tri | N_lf_p1 | E_cond | Status |
|---------|-------|---------|--------|--------|
| qok→sh→k | 5 | 34 | **3.90×** | CONFIRMED(N≥5) |
| d→ot→ot | 5 | 13 | **3.69×** | CONFIRMED(N≥5) |
| l→ch→qok | 5 | 11 | **2.72×** | CONFIRMED(N≥5) |
| d→qok→ol | 6 | 42 | **2.61×** | CONFIRMED(N≥5) |
| y→sh→ch | 8 | 30 | **2.53×** | CONFIRMED(N≥5) |
| y→o→ch | 6 | 14 | **2.45×** | CONFIRMED(N≥5) |
| qok→ch→qo | 8 | 56 | **2.35×** | CONFIRMED(N≥5) |
| d→ch→y | 5 | 86 | **2.23×** | CONFIRMED(N≥5, 'other'-filtered) |
| qok→ch→ol | 5 | 56 | **2.06×** | CONFIRMED(N≥5) |
| p→sh→ok | 6 | 56 | **2.03×** | CONFIRMED(N≥5) |
| **d→ch→l** | **12** | 86 | **1.57×** | BELOW THRESHOLD |
| p→sh→qot | 8 | 56 | 1.78× | BELOW THRESHOLD |
| s→sh→l | 6 | 64 | 1.87× | BELOW THRESHOLD |
| s→sh→qok | 21 | 64 | 1.26× | BELOW THRESHOLD |

### Formula-typed fraction
**10 formula types at N≥5, E≥2.0**. Formula-typed lines: 59/2265 = **2.6%** (consistent with F416).

### Full confirmed inventory (N≥5, E≥2.0)
1. qok→sh→k: E=3.90×/N=5
2. d→ot→ot: E=3.69×/N=5
3. l→ch→qok: E=2.72×/N=5
4. d→qok→ol: E=2.61×/N=6
5. y→sh→ch: E=2.53×/N=8
6. y→o→ch: E=2.45×/N=6
7. qok→ch→qo: E=2.35×/N=8
8. d→ch→y: E=2.23×/N=5 (with 'other' filtering)
9. qok→ch→ol: E=2.06×/N=5
10. p→sh→ok: E=2.03×/N=6

---

## Methodological Notes

**'Other' filtering vs strict positions**: The exp_424 methodology filters 'other' onset tokens from the onset sequence before computing trigrams. This differs from a strict word[0]/word[1]/word[2] approach. For d→ch→y: with 'other' filtering N=5, E=2.23×; with strict positions N=3 (exp_421). The 'other'-filtered approach is consistent with exp_418 (which established the N≥5 threshold baseline in F416), so we use it here.

**F424 correction**: d→ch→l was reported as E=2.16×(N=12) in F424, but that used the d-LF baseline (not pos1-conditional). Under the standard pos1-conditional baseline, d→ch→l = E=1.57×(N=12) — BELOW threshold. F424's d→ch→l claim should be downgraded: d→ch→l is NOT a confirmed formula type under the standard methodology.

**p→sh→qot status**: E=1.78×/N=8 in this analysis (BELOW threshold). But exp_392 found E=2.11×/N=8 using a slightly different method. The discrepancy may reflect the 'other'-filtering changing the effective N_lf_p1 denominator. p→sh→qot should be treated as borderline (1.78-2.11×/N=8).

**s→sh→qok**: N=21 but E=1.26× — large sample, confirmed near-baseline routing. s→sh→qok is NOT a formula type (E<2.0), despite s routing to sh at pos1.

---

## Limitations

- 'Other' filtering methodology may slightly miscount trigrams at corpus boundaries.
- d→ch→y status depends on methodology choice.
- p→sh→qot borderline status requires a dedicated recount with consistent methodology.
- PASS.

---

## Conclusion

H646 ANSWERED. VMS B confirmed formula type inventory (N≥5, E≥2.0, 'other'-filtered): 10 types. Formula-typed fraction = 2.6% (consistent with F416). KEY CORRECTIONS: d→ch→l BELOW threshold (E=1.57×, not a formula type despite N=12); p→sh→qot borderline (E=1.78-2.11×/N=8). s→sh→qok large N but low E (1.26×) — confirmed non-formula. The 10-type inventory supersedes prior partial lists.
