# exp_404: A vs B LF→pos1 Matrix Comparison (H629)

**Date:** 2026-04-11
**Hypothesis tested:** H629 — What causes A pos1=ch=28.2% vs B=19.0%? Which LF classes drive the A/B pos1 divergence?
**Outcome:** Four LF-class dominant pos1 inversions identified: s-LF (A→ch, B→sh), sh-LF (A→ch, B→qok), ok-LF (A→ch, B→qok), ot-LF (A→ch/d, B→qok). A routes template-class and formula-terminal LFs to ch; B routes them to sh/qok. The A/B ch-at-pos1 elevation (A=28.2% vs B=19.0%) is broadly distributed across LF classes, not driven by a single class. B's qok-at-pos1 advantage (B=12.4% vs A=4.5%) reflects B's higher qok frequency overall AND B-specific routing from template-class LFs (ok/ot/qot→qok at pos1).

---

## 1. Dominant pos1 Inversions (LF classes with different dominant pos1 in A vs B)

| LF class | A dominant pos1 | A rate | B dominant pos1 | B rate | Inversion? |
|---|---|---|---|---|---|
| d | ch | 64/250=26% | ch | 83/352=24% | No (both ch) |
| y | ch | 49/206=24% | ch | 53/273=19% | No (both ch) |
| **s** | **ch** | **31/89=35%** | **sh** | **63/264=24%** | **YES** |
| qok | ch | 34/96=35% | ch | 55/239=23% | No (both ch) |
| p | sh | 10/39=26% | sh | 52/229=23% | No (both sh) |
| t | ch | 20/108=19% | ch | 38/208=18% | No (both ch) |
| **sh** | **ch** | **37/107=35%** | **qok** | **22/128=17%** | **YES** |
| ch | ch | 39/111=35% | ch | 14/88=16% | No (ch) but rate differs |
| o | ch | 30/106=28% | ch | 20/72=28% | No (both ch) |
| ok | ch | 25/75=33% | **qok** | **15/76=20%** | **YES** |
| qot | ch | 28/72=39% | ch | 14/47=30% | No (both ch) |
| **ot** | **ch/d** | **14/58=24%** | **qok** | **11/51=22%** | **YES** |
| k | sh | 17/46=37% | ch/sh (tie) | 5/34 each | (minor diff) |

**Four clear inversions: s/sh/ok/ot LF classes.**

---

## 2. Source of A ch=28.2% vs B=19.0% at pos1

The A elevation of ch-at-pos1 is BROADLY distributed: most LF classes route more often to ch in A than B (or approximately the same). The biggest A>B ch routing gaps:
- sh-LF: A ch=1.23× vs B ch=0.74× (gap=0.49×)
- ch-LF: A ch=1.24× vs B ch=0.84× (gap=0.41×)
- ok-LF: A ch=1.18× vs B ch=0.83× (gap=0.35×)
- s-LF: A ch=1.23× vs B ch=0.99× (gap=0.24×)

The only LF classes where B routes MORE to ch than A are:
- d-LF: A ch=0.91× vs B ch=1.24× (B>A by 0.33)
- t-LF: A ch=0.66× vs B ch=0.96× (B>A by 0.30)
- o-LF: A ch=1.00× vs B ch=1.46× (B>A by 0.46)

**The A ch-at-pos1 elevation is not driven by a single LF class but is a global property: most A LF classes route to ch at pos1 more often than B (with exceptions for d/t/o LF classes).**

---

## 3. Source of B qok=12.4% vs A=4.5% at pos1

The B qok-at-pos1 advantage is driven by specific template-class LFs:
- B qot→qok=1.89×(N=11) vs A qot→qok=0.93×(N=3) — B qot routes to qok
- B ok→qok=1.59×(N=15) vs A ok→qok=0.90×(N=3) — B ok routes to qok
- B ot→qok=dominant(N=11/51) vs A ot→ch(N=14/58) — the main inversion
- B p→qok=0.77×(N=22) vs A p→qok=0.00×(N=0) — p NEVER routes to qok in A

The interpretation: in B, template-class LFs (ok/ot/qot) tend to continue with qok at pos1 (intra-template-class continuation). In A, these same LFs route to ch at pos1 (cross-class transition). This suggests B's MID grammar has stronger template-class clustering at the line opening, while A's LF grammar routes through ch more generically.

---

## 4. s-LF Inversion: Key Finding

The clearest single inversion: **A s-LF dominant pos1 = ch; B s-LF dominant pos1 = sh**.

This connects directly to the formula-type taxonomy:
- B s-formula type: s→sh→l=2.06×(F398) — B s-LF lines use sh as pos1 opener
- A s-LF: no sh-formula type; routes to ch generically

In B, s is a "formula-terminal" LF class (F398: opens with sh, terminates with l/qok). In A, s is a "near-Markovian ch-routing" LF class. This is another A/B formula-type inversion: B has s→sh formula, A does not.

---

## 5. sh-LF Inversion: Mechanism

B sh-LF → qok(dominant) connects to B's sh→qok global bigram rule (F326: sh→qok=1.97×). When sh appears at LF in B, the next word tends to be qok (via the global sh→qok bigram rule). In A, sh→qok is present (F326: A sh→qok=1.74×) but A sh-LF routes to ch first (sh→ch→sh interleaving: F406 A sh→ch→sh=2.69×(N=8)). So A sh-opening lines use ch as the intermediate, not qok.

---

## 6. Implications

The A/B pos1 divergence decomposes as:
1. **A global ch routing** — most A LF classes (sh/ch/ok/s/qok) route to ch at pos1 more than B
2. **B formula routing** — B s-LF→sh, B sh-LF→qok, B ok/ot-LF→qok (specific formula types); A lacks these formula routing types
3. **B template-class clustering** — B template-class LFs (ok/ot/qot) tend to stay in the qok/template class zone at pos1; A routes them to ch

This means the A/B pos1 difference is not a single mechanism but the sum of (a) A global ch-routing bias, (b) B-specific formula types (s→sh, sh→qok, ok→qok, ot→qok), and (c) B template-class clustering. All three work in the same direction: pushing A ch up and B qok up.

---

## Self-Audit

**Target-awareness**: No target-aware elements.

**Feature-destroying implementation**: No feature-destroying elements.

**Extrapolation**: "Four clear inversions" (s/sh/ok/ot) are based on N=39-128 per LF class — adequate. Directional claims (B p→qok=0.00×: N=0/39 in A) are adequate for categorical characterization. PASS.

**Negative-result scope**: "A/B ch elevation broadly distributed" is not a negative result. PASS.

**Control behavior**: No shuffle control. Baseline is dialectal pos1 class distribution (A=28.2% ch, B=19.0% ch). These baselines are computed from the same corpus — correct reference. PASS.

## Finding: F408

**See findings.md F408**
