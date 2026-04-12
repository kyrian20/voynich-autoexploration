# exp_398: B raiin Line Continuation Grammar (H612)

**Date:** 2026-04-11
**Hypothesis tested:** H612 — Full line structure after B pos1=raiin
**Outcome:** ANSWERED (directional, N=6) — B raiin-pos1 lines strongly route to ch at pos2 (4.67×/N=4/5). Canonical formula: LF(y/qok/qot/s/t)-word → raiin → ch → qok → [MID continuation] → LL. r appears at LL in 2/6 lines (9.46×, directional) — lines with raiin at pos1 may also terminate with r at LL.

---

## Corpus Statistics

- B continuation lines with raiin at pos1: **6** (of 15 total B pos1 r lines; 40% are raiin, F394)

---

## LF Distribution

y=2, qot=1, qok=1, s=1, t=1. Consistent with F394 (template classes qot/qok/y/s produce r at pos1).

---

## pos2 Distribution (N=5 lines with ≥3 words)

| pos2 | N | % | E |
|------|---|---|---|
| ch | 4 | 80.0% | **4.67×** |
| qok | 1 | 20.0% | 1.19× |

ch is the dominant pos2 after raiin (4.67×/N=4). **The raiin formula: LF → raiin → ch.**

---

## LL Distribution (N=6)

| LL | N | % | E |
|----|---|---|---|
| r | 2 | 33.3% | **9.46×** (directional) |
| s | 1 | 16.7% | 9.46× (directional) |
| ot | 1 | 16.7% | 2.23× |
| ch | 1 | 16.7% | 1.16× |

r at LL (9.46×, N=2): lines with raiin at pos1 may also terminate with r at LL — r appears twice in these lines (pos1=raiin + LL=r-word).

---

## Actual Line Examples

```
f82/30: qoteey raiin cheol qoteey shedy qokeey lshedy qokeedy rag
  qot → r(raiin) → ch → qot → sh → qok → l → qok → r(rag=LL)

f111/41: ycheey raiin cheody qokechy qokeey okedy lchedy qokeeal daiin otaral
  y → r(raiin) → ch → qok → qok → ok → l → qok → d → ot(LL)

f115/42: tcheodl raiin chkar qokol lchdy qorshy qokain qokain chep chotchdy
  t → r(raiin) → ch → qok → l → qo → qok → qok → ch → ch(LL)
```

The canonical structure is clear: **LF(template/formula) → raiin → ch → qok → [qok-dominated MID] → LL**.

---

## Interpretation

The raiin formula is: template-class LF word → raiin at pos1 → ch at pos2 → qok continuation. This connects to:
- F394 (raiin=40% of B pos1 r; qok/y/qot LF produce r at pos1)
- F383 (B ch→qok MID=1.21×)
- F370 (sh→qok rule)

The raiin-pos1 line uses r as a "bridging" word class between the formula-class LF opener and the ch/qok content body. The r word at LL in 2/6 lines suggests some raiin-pos1 lines have r-terminal endings (via the B pre_LL→r routing rule, F382/F389).

---

## Self-Audit

**Target-awareness**: No target-aware elements.

**Feature-destroying implementation**: No feature-destroying elements.

**Extrapolation**: N=6 total, N=5 with pos2. All claims are directional. pos2=ch 4.67×(N=4/5) is the most robust finding. LL=r 9.46×(N=2/6) and LL=s 9.46×(N=1/6) are highly directional. No claims beyond the tested N.

**Negative-result scope**: N/A — descriptive.

**Control behavior**: B cont line pos2 baseline (N=total_b_pos2) and LL baseline used. Expected pos2=ch elevated based on F394's actual line examples showing ch continuation; confirmed (4.67×). No surprises.

## Finding: F402

**See findings.md F402**
