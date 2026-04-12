# exp_408: A/B t-onset Full Positional Characterization

**Hypothesis (H613):** t is the second most frequent B gallows LF class (3.59×, F392) after p. We know p's full profile (LF-dominant, pos1=0.18×, MID/LL depleted). Does t share p's extreme LF concentration, or is it more broadly distributed? What are t's MID→successor and pre_LL→LL rules?

**Method:** For both A and B continuation lines, compute t positional distribution (LF/pos1/pos2/pos3/MID/pre_LL/LL) with enrichment vs global rate. For LF=t, compute pos1 routing with E values vs dialect baseline. For MID=t, compute successor onset distribution. For pre_LL=t, compute LL routing. Compare to p profile.

**N:** A=1487 cont lines; B=2341 cont lines.

---

## Results

### B t positional profile (cont lines):

| Position | n    | total | rate  | E     |
|----------|------|-------|-------|-------|
| LF       | 208  | 2322  | 0.090 | 3.90× |
| pos1     | 31   | 2322  | 0.013 | 0.58× |
| pos2     | 34   | 2276  | 0.015 | 0.65× |
| pos3     | 26   | 2211  | 0.012 | 0.51× |
| MID      | 135  | 9132  | 0.015 | 0.64× |
| pre_LL   | 56   | 2211  | 0.025 | 1.10× |
| LL       | 33   | 2322  | 0.014 | 0.62× |

**B t is strongly LF-concentrated and depleted everywhere else.** pre_LL is near-baseline (1.10×), which contrasts with p's pre_LL=0.26×. B t has a less extreme concentration than p (LF=3.90× vs p=6.98×; pos1=0.58× vs p=0.18×).

### B t LF→pos1 routing (N=208): NEAR-MARKOVIAN

| onset | n  | E    |
|-------|----|------|
| ch    | 38 | 0.96× |
| sh    | 35 | 1.00× |
| qok   | 25 | 0.97× |
| ok    | 16 | 1.04× |
| ol    | 16 | 1.23× |
| o     | 13 | 1.51× |

Confirms F399: B t→pos1 is near-baseline. No formula routing at pos1.

### B t MID→successor (N=135):

| onset | n  | E     |
|-------|----|-------|
| ot    | 22 | 1.95× |
| sh    | 18 | 1.50× |
| l     | 11 | 1.51× |
| ch    | 23 | 0.97× |
| qok   | 14 | 0.74× |

**B t in MID position is followed by ot at 1.95× (N=22).** t→ot in MID is the strongest successor signal. sh and l also moderately elevated. ch (the dominant B MID class) is at baseline.

### B t pre_LL → LL (N=56):

| onset | n | E     |
|-------|---|-------|
| t     | 4 | 5.03× (dir) |
| ot    | 9 | 2.12× |
| qot   | 4 | 2.07× (dir) |
| ch    | 4 | 0.50× |

**B t at pre_LL routes to ot at LL (2.12×, N=9) and shows t-self-succession (5.03×, N=4 — directional).** ch depleted at LL given t at pre_LL (0.50×). The {t, ot, qot} cluster at LL after t pre_LL suggests a terminal gallows-adjacent affinity.

---

### A t positional profile (cont lines):

| Position | n   | total | rate  | E     |
|----------|-----|-------|-------|-------|
| LF       | 108 | 1456  | 0.074 | 2.63× |
| pos1     | 19  | 1456  | 0.013 | 0.46× |
| pos2     | 31  | 1360  | 0.023 | 0.81× |
| pos3     | 32  | 1182  | 0.027 | 0.96× |
| MID      | 54  | 2834  | 0.019 | 0.68× |
| pre_LL   | 28  | 1182  | 0.024 | 0.84× |
| LL       | 36  | 1456  | 0.025 | 0.88× |

A t is also LF-concentrated (2.63×) but with weaker positional exclusion than B. pos3 and LL are near-baseline (0.96×, 0.88×) in A, whereas B's are more strongly depleted (pos3=0.51×, LL=0.62×). A t has broader positional footprint than B t.

### A t LF→pos1 routing (N=108):

| onset | n  | E     |
|-------|----|-------|
| ot    | 9  | 2.82× |
| ol    | 6  | 2.45× |
| ch    | 20 | 0.66× |
| sh    | 19 | 1.19× |

Confirms F399: A t→ot elevated (2.77→2.82×), A t→ch depleted (0.66×). A t→ol=2.45×(N=6) is a new detail.

### A t MID→successor (N=54): near-Markovian

ch=1.29×(N=15), qot=2.28×(N=3, dir). Broadly near-Markovian.

### A t pre_LL → LL (N=28): sparse

No dominant routing — directional signals only (N<6 per onset class).

---

## p vs t Comparison (B cont lines):

| Profile point        | p       | t       |
|----------------------|---------|---------|
| LF E                 | 6.98×   | 3.90×   |
| pos1 E               | 0.18×   | 0.58×   |
| MID E                | 0.41×   | 0.64×   |
| LL E                 | 0.27×   | 0.62×   |
| LF→pos1 formula?     | sh=1.36×, o=2.22× | near-baseline |
| MID→succ top         | o=2.90×, k=3.05× | ot=1.95× |
| pre_LL→LL top        | o=5.88×, t=17.59× (dir) | t=5.03×(dir), ot=2.12× |

p is far more LF-concentrated and more depleted at non-LF positions. Both show strong LF enrichment; t is the "weak" version of p's gallows-LF pattern.

---

## Interpretation

**B t = LF-dominant, non-formula gallows.** t appears strongly at LF (3.90×) and is depleted everywhere else (MID=0.64×, LL=0.62×). But unlike p (which routes strongly to sh at pos1, 1.36×, with formula pos2 routing), t's LF→pos1 is near-Markovian. This confirms the gallows taxonomy from F411: STRONG-FORMULA {p} → WEAK-FORMULA {f} → NON-FORMULA {t, k (folio-level)}.

**New finding: B t MID→ot=1.95×(N=22).** When t appears in MID position (rare: E=0.64×), it is followed by ot class at nearly 2×. This may reflect t-ot adjacency in compound forms (e.g., t-onset word followed by ot-onset word as a habitual pair).

**New finding: B t pre_LL→ot=2.12×(N=9) and pre_LL→t=5.03×(N=4, dir).** Terminal t chains: t at pre_LL routes to ot or t at LL. The {t, ot, qot} gallows-terminal affinity at line-end (given t at pre_LL) mirrors t's LF-dominant behavior — t clusters at line boundaries.

**A t = moderately LF-dominant, broader distribution.** A t has weaker LF concentration (2.63× vs B's 3.90×) and weaker non-LF depletion. A t pos3/LL are near-baseline in A but depleted in B. A t shows A-specific pos1 routing: ot=2.82×, ol=2.45× (both A-dominant classes), ch=0.66× (depleted, unlike A's normal ch-dominant pos1).

**A/B t distinction:** B t is more sharply LF-concentrated than A t. This adds to the A/B grammar inversion set: in A, t-onset is somewhat broadly distributed; in B, t-onset is almost exclusively a line-first word class.

---

## Limitations

- B t pre_LL→t self-succession (N=4) is directional only.
- A t pre_LL→LL N=28 with no class reaching N≥6 — all directional.
- A t MID→qot=2.28×(N=3) directional only.
- Global E values use all-position baseline; position-specific baselines would be cleaner but consistent with prior experiments.

---

## Self-Audit

**Target-awareness**: No target-aware elements identified. E values computed from corpus-derived baselines with no external VMS metric knowledge.

**Feature-destroying implementation**: Not applicable — observational positional study, no mechanism implementation.

**Extrapolation**: No "structural" or "cannot" claims made. Pre_LL t-self-succession and A t pre_LL routing explicitly flagged as directional only (N<6). Gallows taxonomy claim ("NON-FORMULA {t}") is supported by N=208 near-Markovian pos1 routing, sufficient to establish absence of formula routing.

**Negative-result scope**: B t→pos1 is near-Markovian (no formula routing). Conclusion: "B t LF→pos1 routing does not show the formula-type enrichment seen in p." Does not claim "t cannot have formula routing" — only that none was detected (N=208).

**Control behavior**: No external control corpus used. Dialect-specific baseline rates serve as internal control. No surprises in baseline rates.

---

## Conclusion

B t is a **LF-dominant non-formula gallows**: strongly LF-enriched (3.90×), near-Markovian at LF→pos1, depleted at all other positions. In MID (rare), t routes to ot at 1.95×(N=22). At pre_LL, t routes to ot (2.12×, N=9) and self-succession t=5.03×(N=4, dir). A t is LF-dominant but less concentrated, with A-specific pos1 routing (ot=2.82×, ch=0.66×). The gallows taxonomy is: STRONG-FORMULA {p} → WEAK-FORMULA {f} → NON-FORMULA/LF-ONLY {t} → FOLIO-LEVEL {k}.

## Follow-up Questions

1. **H613b**: B t MID→ot=1.95×(N=22) — is this a t-ot compound construction, or independent t and ot words in sequence? (Check vocabulary of the t-onset and ot-onset words in these bigrams.)
2. **H624**: A bracket grammar for other LF classes (t at LF may show t-bracket: pos1=ot/ol and LL routing?).
3. **H631**: Reference corpus comparison of formula-typed fraction.
