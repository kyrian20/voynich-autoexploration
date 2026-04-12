# exp_413: B p-Formula pos3 Grammar

**Hypothesis (H623):** After p→sh→qot at pos0-pos1-pos2, what comes at pos3? Does the formula continue into pos3, or does it decay to near-Markovian?

**Method:** For B cont lines with p at LF (N=229, len≥4: N=228): compute pos3 onset distribution vs B baseline; compute pos2→pos3 routing conditioned on pos2 class in p-LF lines; compute specific p→sh→qot→pos3 routing; compute p→o pos2 distribution.

---

## Results

### B p-LF pos3 distribution vs baseline (N=228 lines with len≥4):

| onset | n  | E      | note |
|-------|----|--------|------|
| qo    | 14 | 1.86×  | ELEVATED — o-class continues |
| other | 15 | 1.63×  | elevated |
| ot    | 21 | 1.39×  | moderate |
| o     | 11 | 1.37×  | elevated |
| ch    | 32 | **0.75×** | DEPLETED — ch-avoidance continues |
| qok   | 34 | 0.93×  | near-baseline |
| ol    | 9  | 0.66×  | depleted |
| d     | 8  | 0.73×  | depleted |

**The global ch-avoidance in p-formula lines extends to pos3 (ch=0.75×).** The o-class enrichment (qo=1.86×, o=1.37×) also extends to pos3, consistent with F409 (MID: qo=1.50×, o=1.73×).

### B p-LF pos2=sh → pos3 routing (N=33 p-LF lines with sh at pos2):

| onset | n | E       |
|-------|---|---------|
| qo    | 6 | 2.55×   |
| y     | 3 | 5.41× (dir) |
| k     | 2 | 2.88× (dir) |
| ot    | 4 | 2.06×   |
| qok   | 6 | **0.66×** (depleted) |

Given sh at pos2 in p-LF lines, pos3 routes to qo (2.55×, N=6) and ot (2.06×, N=4). qok is depleted (0.66×) — contrast with unconditional sh→qok in B (the strong sh→qok bigram is SUPPRESSED in p-formula lines at pos3).

### B p→sh→qot → pos3 (N=8, all directional):

N=8 lines exist; 6 have ≥4 words. Results: ot=1.68×(N=2), qok=1.68×(N=2), ch=0.57×(depleted, N=1). All directional — no reliable routing signal.

### B p-LF pos2=qot → pos3 (N=17):

Near-Markovian. d=2.23×(N=3, dir), ch=1.08×(N=4, baseline). No strong formula continuation.

### B p-LF pos2=ch → pos3 (N=19 p-LF lines):

ch→pos3: ch=1.80×(N=6), sh=2.70×(N=3, dir). Near-Markovian overall — but ch tends to self-repeat (ch=1.80×, N=6).

---

## Interpretation

**The p-formula grammar at pos3 is near-Markovian, with ch-avoidance continuing.** The two established formula effects (ch-avoidance and o-class enrichment) persist through pos3:

1. **ch-avoidance at pos3=0.75×(N=32)**: The global ch-avoidance (F409: pos1=0.42×, MID=0.69×, LL=0.47×) now extends to pos3=0.75×. ch is depleted at ALL positions in p-formula lines.

2. **qo enrichment at pos3=1.86×(N=14)**: Consistent with F409's qo enrichment at MID (1.50×). The qo class (onset qo: words starting "qo...") is enriched throughout p-formula lines.

3. **pos2=sh → pos3=qo 2.55×(N=6)**: When pos2=sh in p-LF lines, pos3 routes to qo more than baseline (2.55×). This continues the o/qo enrichment chain: p[LF] → sh[pos2] → qo[pos3]. The sh→qok bigram (strong in B unconditionally) is SUPPRESSED in p-formula lines (0.66× at pos3 given pos2=sh) — the p-formula context overrides the general sh→qok bigram.

4. **p→sh→qot→pos3 is near-Markovian (N=8 directional)**: The specific formula type (p→sh→qot, F396) does not have strong pos3 routing. The formula effect is concentrated at pos2 (qot at pos2 given p→sh), not extending to pos3.

**Extended p-formula characterization:**
```
p[LF] → sh/o[pos1] → qot/ch/sh/o[pos2] → [qo/o enriched, ch-avoided, qok suppressed at pos3]
        → [o/qo/qot-rich MID] → [o/qot/r LL]
```
The ch-avoidance is global (all positions 1 through LL). The o-class enrichment is global. The specific formula routing (p→sh→qot, p→sh→qo, p→o→sh) is concentrated in the first 3 positions.

---

## Limitations

- p→sh→qot→pos3: N=8 total lines, only 6 with ≥4 words. All directional.
- pos2=sh→pos3=y: E=5.41×(N=3) — extreme but tiny N.
- B p-LF pos2=qot→pos3: N=17, most effects directional (d=2.23×, N=3).
- pos3 analysis limited to lines with ≥4 words (N=228/229); pre-LL and LL not analyzed here (already in F409).

---

## Self-Audit

**Target-awareness**: No target-aware elements.

**Feature-destroying implementation**: Not applicable.

**Extrapolation**: All directional findings (N<5) labeled explicitly. The ch-avoidance at pos3 (N=32, E=0.75×) is adequate. The qo enrichment (N=14, E=1.86×) is moderate. No "structural" or "cannot" claims.

**Negative-result scope**: "p→sh→qot→pos3 routing is near-Markovian (N=8 directional)" — does not claim "no formula at pos3 possible for larger N."

**Control behavior**: B baseline pos3 distribution serves as control. No surprises — baseline rates are stable.

---

## Conclusion

H623 ANSWERED. B p-formula pos3 grammar:
1. **ch-avoidance extends to pos3** (0.75×, N=32) — the global ch-avoidance is pan-positional in p-lines.
2. **qo enrichment extends to pos3** (1.86×, N=14) — consistent with o-class MID/LL enrichment (F409).
3. **pos2=sh → pos3=qo 2.55×(N=6)**: specific sh→qo routing in p-lines (overrides general sh→qok bigram).
4. **p→sh→qot→pos3 near-Markovian** (N=8, directional). Formula effect is at pos2 only for the p→sh→qot path.
