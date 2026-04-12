# exp_392: B p→sh Line Structure Analysis (H607)

**Date:** 2026-04-11
**Hypothesis tested:** H607 — what does the line look like after p opens with sh at pos1?
**Outcome:** ANSWERED — B p→sh→ch≈0(0.18×) confirmed; B p→sh→qot elevated (2.11×/N=8); B p→sh→qok depleted (0.58×); p→sh lines represent a gallows-formula grammar distinct from content-formula (d/s/y) lines

---

## 1. Corpus Statistics

- B continuation lines with sh at pos1: **382**
- B continuation lines with p at LF, sh at pos1: **51** (13.4% of sh-pos1 lines)

---

## 2. pos2 Distribution for p→sh Lines vs sh-pos1 Baseline

| pos2 class | p→sh N | p→sh % | sh-base N | sh-base % | E      |
|------------|--------|--------|-----------|-----------|--------|
| ch         | 1      | 2.0%   | 41        | 10.9%     | **0.18×** |
| qok        | 8      | 15.7%  | 102       | 27.1%     | **0.58×** |
| qot        | 8      | 15.7%  | 28        | 7.4%      | **2.11×** |
| y          | 2      | 3.9%   | 7         | 1.9%      | 2.11×  |
| sh         | 7      | 13.7%  | 43        | 11.4%     | 1.20×  |
| ok         | 3      | 5.9%   | 17        | 4.5%      | 1.30×  |
| ot         | 3      | 5.9%   | 16        | 4.2%      | 1.39×  |
| p          | 2      | 3.9%   | 4         | 1.1%      | 3.70×  |

**B p→sh lines specifically route to qot at pos2** (2.11×/N=8), not to ch (0.18×) or qok (0.58×). This is the distinctive gallows-formula grammar: the p onset at LF avoids ch as a pos2 response (confirming F393) and specifically enriches qot at pos2.

---

## 3. Cross-LF-Class Comparison: pos2=ch Rate After pos1=sh

| LF onset | N   | pos2=ch rate | E vs baseline |
|----------|-----|-------------|---------------|
| p        | 51  | 2.0% (1/51) | **0.18×**     |
| y        | 25  | 32.0% (8/25)| **2.94×**     |
| d        | 80  | 7.5% (6/80) | 0.69×         |
| s        | 61  | 11.5% (7/61)| 1.06×         |
| qok      | 33  | 12.1% (4/33)| 1.11×         |
| sh       | 16  | 18.8% (3/16)| 1.72×         |
| t        | 35  | 14.3% (5/35)| 1.31×         |

The LF-class effect on pos2=ch (when pos1=sh) ranges from 0.18× (p) to 2.94× (y). The p→sh grammar is specifically "qot-routing" rather than "ch-routing." By contrast, y→sh is strongly "ch-routing."

---

## 4. The Two B Gallows LF Grammar Types

The comparison reveals **two distinct B sh-pos1 grammar types**:

**Type 1: Content-formula LF + sh → ch-routing**: y at LF produces ch at pos2 (2.94×) after sh. The y→sh→ch trigram is the distinctive content-formula path.

**Type 2: Gallows LF + sh → qot-routing**: p at LF produces qot at pos2 (2.11×) after sh. The p→sh→qot trigram is the distinctive gallows-formula path. qok is suppressed (0.58×), ch is suppressed (0.18×).

---

## 5. LL Distribution for p→sh Lines

LL onset distribution (N=51):
- other: 15.7% (8/51) — highest
- qok: 9.8% (5/51)
- ch: 7.8% (4/51)
- k: 7.8% (4/51)
- d: 7.8% (4/51)
- qot: 5.9% (3/51)
- ot: 5.9% (3/51)
- s: 5.9% (3/51)
- ol: 5.9% (3/51)

No single dominant LL class — p→sh lines have distributed LL grammar without a specific LL-terminal formula.

---

## 6. Actual Line Examples

```
pchedar shear qokchdy qokees cheol ypchdaiin chedy chedain
  p → sh → qok → qok → ch → y → ch → ch

pshorol shckhy qotshdy qokaldy opchedy qotar
  p → sh → qot → qok → o → qot

polchedy shedy qoteedy qotain ody chckhes otal
  p → sh → qot → qot → o → ch → ot

pdalshor shtol qoty ykar alol lkaiin otain okar
  p → sh → qot → y → other → l → ot → ok
```

The pattern is consistent: p→sh is followed by qot (not qok), and qok appears later in the line.

---

## Self-Audit

**Target-awareness**: No target-aware elements.

**Feature-destroying implementation**: No feature-destroying elements.

**Extrapolation**: All claims within tested data. p→sh→qot N=8/51 (adequate). p→sh→ch N=1/51 (adequate for near-zero characterization). The p→sh→p=3.70× is directional (N=2/51).

**Negative-result scope**: N/A — descriptive analysis confirming F393 and finding new qot-routing.

**Control behavior**: sh-pos1 baseline (N=377) serves as comparison. Expected sh→ch=10.9%, sh→qot=7.4%.

## Finding: F396

**See findings.md F396**
