# exp_466: A Stars Section t-LF Grammar (H_new_AF)

**Hypothesis (H_new_AF):** Is the A stars section t-LF elevation (3.3× vs herbal_a baseline in exp_465) confirmed vs A-dialect overall baseline? What are the dominant t-words? Is there a t→pos2 routing rule?

---

## Results

### A-dialect LF-class section distribution (A-overall baseline)

| onset | herbal_a(N=969) | stars(N=128) | cosmo(N=332) | A_overall |
|-------|-----------------|--------------|--------------|-----------|
| d | 0.91x(165) | 1.08x(26) | 1.24x(77) | 18.8% |
| y | 0.89x(136) | 1.29x(26) | 1.21x(63) | 15.7% |
| ch | **1.21x↑(101)** | **0.54x↓(6)** | 0.56x↓(16) | 8.6% |
| sh | 1.13x(84) | 0.71x(7) | 0.74x(19) | 7.7% |
| s | 0.82x(58) | **1.50x↑(14)** | 1.32x(32) | 7.3% |
| qok | 1.00x(64) | **0.59x↓(5)** | 1.14x(25) | 6.6% |
| **t** | **0.63x↓(34)** | **2.12x↑(15)** | **1.63x↑(30)** | 5.5% |
| ok | 1.15x(57) | 0.92x(6) | 0.59x↓(10) | 5.1% |
| **qot** | **1.43x↑(68)** | **0.16x↓(1)** | **0.06x↓(1)** | 4.9% |
| **ot** | 1.35x(53) | **0.19x↓(1)** | 0.30x↓(4) | 4.1% |
| qo | 1.01x(22) | 1.74x↑(5) | 0.67x(5) | 2.2% |

**Formal A stars t-LF: obs=15, exp=7.08 (A-overall baseline), E=2.12×**

Sharp contrast:
- herbal_a t-LF: E=0.63×(N=34) — DEPLETED
- cosmo t-LF: E=1.63×(N=30) — elevated (intermediate)
- stars t-LF: E=2.12×(N=15) — highest elevation

**A stars qot-LF: obs=1, E=0.16×** — massively depleted
**A stars ot-LF: obs=1, E=0.19×** — massively depleted

### t-word inventory in A stars (N=15, 11 unique words)
tal(2), todal(2), tcheos(2), taiin(2), torchey(1), toleeshal(1), tazain(1), tor(1), tolain(1), tcheor(1), tcheody(1)

Compare A herbal_a t-LF (top words): tol(5), tchor(3), tor(3), todaiin(2), tar(2) — different distribution, overlapping vocabulary.

### A stars t-LF → pos2 routing (N=15)
- ot: 20.0%, E=4.93×(N=3) — ot elevated at pos2 after t-LF
- ch: 20.0%, E=2.32×(N=3)
- qot: 13.3%, E=2.72×(N=2)
- ol: 6.7%, E=3.66×(N=1)
- y: 6.7%, E=0.42×(N=1)

(All N≤3, directional)

### A stars vs B astro comparison

| metric | A stars | B astro |
|--------|---------|---------|
| t-LF E | **2.12×(N=15)** | 0.70×(N=30) — depleted |
| qok-LF E | 0.59×(N=5) — depleted | **1.78×(N=149)** — elevated (F431) |
| qot-LF E | 0.16×(N=1) — nearly absent | (not in F431 focus; B astro herbal) |
| ch-LF E | 0.54×(N=6) — depleted | (moderate in B herbal) |

**Full A/B inversion at "astronomical" section LF grammar:**
- A stars: t elevated (2.12×), qok depleted (0.59×)
- B astro: qok elevated (1.78×, F431), t depleted (0.70×)

---

## Interpretation

**H_new_AF CONFIRMED: A stars section has t-LF grammar elevated E=2.12×(N=15) vs A-overall baseline.**

This is the A-dialect analog of B astro's qok-LF elevation (F431: 1.91× in exp_429). Both the A "astronomical" section (stars, f57-72) and B "astronomical" section (astro, f73-84) have a specific onset class elevated at line-first position, but they use DIFFERENT onset classes:
- B astro: qok (E=1.78-1.91×, N=149) — the template-class gallows+bench compound
- A stars: t (E=2.12×, N=15) — a different, rare gallows onset

**Triple LF-class inversion between A stars and B astro:**
1. t-LF: A stars 2.12× vs B astro 0.70× — opposite
2. qok-LF: A stars 0.59× vs B astro 1.78× — opposite
3. qot-LF: A stars 0.16× vs herbal_a 1.43× — stars-specific depletion

**A stars LF profile summary:** {d(1.08×), y(1.29×), s(1.50×), t(2.12×)} elevated; {qot(0.16×), ot(0.19×), ch(0.54×), qok(0.59×)} depleted. The "astronomical" content in A-dialect uses t-onset words as frequent line-openers — a formula-starting onset class not predicted by the within-line grammar seen in herbal_a.

**t-word vocabulary**: 11 unique words for 15 occurrences — class-level (not one dominant word). Different distribution from herbal_a t-words (herbal_a: tol/tchor/tor dominant; stars: tal/todal/tcheos/taiin).

**t-LF → pos2 routing** (directional, N≤3): ot(E=4.93×), ch(2.32×), qot(2.72×) — all elevated. If confirmed, t-LF may predict ot/ch at pos2 (formula-type routing). This would make t→ot a stars formula pair.

**A stars additional grammar features** (descriptive):
- s-LF: elevated 1.50×(N=14) in stars alongside t — s is also elevated
- qo-LF: elevated 1.74×(N=5,dir) in stars — qo may also be a stars LF class
- qot+ot combined depleted ~0.17× — these two "bench" onset classes nearly absent at stars LF

---

## Self-Audit

**Target-awareness**: No target-aware elements. E computed from corpus frequencies (A-overall LF base rate) without calibration to any committed metric.

**Feature-destroying implementation**: No feature-destroying details. Same parsing and dialect classifier as all prior CL experiments.

**Extrapolation**: A stars t-LF E=2.12×(N=15): formal enrichment vs A-overall baseline. This is a frequency ratio with N=15 observed vs 7.08 expected — not overextrapolated. t→pos2 routing is directional only (N≤3 per target). The "A/B inversion" comparison is descriptive (A stars vs B astro in different corpus regions) — not a formal test of inversion.

**Negative-result scope**: herbal_a t-LF E=0.63× (N=34) is an informative negative — t is actively depleted in herbal_a. This contrast sharpens the stars finding.

**Control behavior**: No explicit control. A-overall LF base rate (N=1429 A-dialect lines) serves as baseline. B astro qok-LF comparison reproduces F431 at E=1.78× (consistent with published 1.91×, small difference due to different line counting method).

---

## Conclusion

**H_new_AF CONFIRMED: A stars t-LF E=2.12×(N=15) vs A-overall.** A stars section LF grammar uses t-onset as a marked line-opening class (2.12×) while depleting qot (0.16×) and ot (0.19×). This is the A-dialect parallel of B astro's qok-LF elevation (F431) but uses a DIFFERENT onset class (t vs qok) — an A/B inversion in "astronomical section" LF grammar.

**F446 assigned**: A Stars Section Has t-LF Grammar (E=2.12×/N=15 vs A-overall; qot/ot depleted to E≈0.17×); Parallel to B Astro qok-LF (F431) but with t Instead of qok.
