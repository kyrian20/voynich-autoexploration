# exp_478: B pharma LF-class Self-Succession at pos1

**Question:** Is B pharma t-LF → t at pos1 (E=7.99×/N=3 from exp_477) part of a general LF-class self-succession rule in B pharma, or specific to t? Compare to B herbal. (H_new_AR)

---

## Results

### B pharma LF distribution (N=799 total lines)

Top LF classes: ch(19.8%), l(11.5%), a(11.0%), ot(9.9%), qok(7.4%), ok(6.1%), o(5.5%), ol(5.1%), d(4.5%), r(4.1%)

ch is the dominant pharma LF class (158 lines, 19.8%). B herbal by comparison: ch=17.8%, ok=14.5%, d=12.6%.

---

### B pharma LF-class self-succession at pos1

| LF | N_lf | self_obs | E | flag |
|----|------|----------|---|------|
| **ch** | **158** | **15** | **1.64×** | **CONFIRMED** |
| **sh** | **23** | **6** | **3.99×** | **dir** |
| **t** | **10** | **3** | **8.22×** | **(dir)** |
| l | 92 | 3 | 1.23× | — |
| ok | 49 | 3 | 1.11× | — |
| o | 44 | 2 | 1.00× | — |
| qok | 59 | 4 | 1.10× | — |
| d | 36 | 6 | 0.82× | — |
| qot | 29 | 0 | 0.00× | depleted |

**CONFIRMED: B pharma ch-LF → ch at pos1 (E=1.64×/N=15).** Ch-class lines in B pharma begin with ch-class words at elevated rate (9.5% vs 5.7% baseline). Self-succession is confirmed at N=15/E≥1.5×.

**dir: B pharma sh-LF → sh at pos1 (E=3.99×/N=6).** Sh-class lines similarly self-chain.

**dir: B pharma t-LF → t at pos1 (E=8.22×/N=3).** Confirms exp_477 finding.

**NOT GENERAL:** Self-succession does NOT hold for template/gallows classes l(1.23×), ok(1.11×), o(1.00×), qok(1.10×), or d(0.82×). The rule is class-selective: ch and sh (gallows/quasi-gallows) show self-succession; template classes do not.

---

### B herbal comparison: ch self-succession absent

| LF | B pharma E | B herbal E |
|----|-----------|-----------|
| ch | 1.64×/N=15 (CONFIRMED) | 0.00×/N=0 (DEPLETED) |
| sh | 3.99×/N=6 (dir) | 1.38×/N=2 |
| l | 1.23×/N=3 | 0.00×/N=0 |
| d | 0.82×/N=6 | 0.64×/N=4 |

**B herbal ch-LF → ch at pos1 is DEPLETED (0/47 ch-LF lines start with ch).** This is a B pharma-specific ch self-succession — absent in B herbal. 

---

### B pharma additional pos1 routing (directional)

From full pos1 routing analysis of major LF classes:
- **d-LF → l at pos1: E=4.21×/N=4 (dir)** — connects to F423 pharma l-chain; d-LF lines start with l-onset words
- **ok-LF → t at pos1: E=2.24×/N=4 (dir)** — t-onset elevation for ok-LF lines
- **ch-LF → t at pos1: E=1.56×/N=9** — ch-LF also elevated for t at pos1 (below dir threshold)
- **ch-LF → qot at pos1: E=2.16×/N=3 (dir)** — qot elevation in ch-LF lines
- **sh-LF → d at pos1: E=1.50×/N=7** — sh-LF lines also show d at pos1 (moderate)

---

## Interpretation

**F449 assigned: B pharma ch-LF → ch at pos1 (E=1.64×/N=15, Confirmed); pharma-specific ch self-succession absent in B herbal.**

The H_new_AR hypothesis is partially confirmed: B pharma has selective LF-class self-succession at pos1, but only for ch and sh (gallows-class LF markers), not for template classes (l, ok, o, qok). The rule is class-specific, not general.

**Selective self-succession taxonomy:**
- ch-LF → ch at pos1: CONFIRMED in B pharma (F449), DEPLETED in B herbal (0/47)
- sh-LF → sh at pos1: DIRECTIONAL in B pharma (E=3.99×/N=6)
- t-LF → t at pos1: DIRECTIONAL in B pharma (E=8.22×/N=3, confirmed exp_477)
- l-LF → l at pos1: NO elevation (1.23×/N=3)
- ok/o/qok-LF → self at pos1: NO elevation

**Interpretation:** In B pharma, gallows-class lines (ch, sh as final onsets) tend to begin with the same gallows class. This creates a within-line onset class persistence for ch/sh specifically. This is distinct from F423 (l-chain = sequential l succession within MID positions) and from F430 (formula types = specific 3-word triplet structures). The ch self-succession rule is a 2-position onset class persistence (LF → pos1) that is pharma-concentrated.

**Connection to prior findings:**
- F447: ch is NOT a marker of B pharma LF elevation (ch-LF is at baseline vs sections); but ch IS the dominant B pharma LF class (19.8%), and its self-succession at pos1 is a pharma-specific grammar feature.
- F423: pharma l-chain involves l at MID positions. B pharma d-LF → l at pos1 (E=4.21×/N=4, dir) extends this — d-closing lines begin with l, consistent with d being an "opener for l-content".
- F408: B has qok-self-succession at pos1 (pos1 distribution inversion); this is different from the ch self-succession, which is LF-conditional.

**A/B comparison for ch self-succession:**
- A herbal_a: ch self-succession at pos1 exists (exp_449 showed A ch→ch within-line is elevated ~1.3×), but this is not LF-conditional.
- B pharma: ch self-succession is specifically elevated in ch-LF lines (LF-conditional) and absent in B herbal ch-LF lines.
- The B pharma self-succession is a LF-class conditional rule, not a general sequential rule.

---

## Self-Audit

**Target-awareness:** No target-aware elements identified. Self-succession E computed from section-specific baselines, no calibration to VMS metrics.

**Feature-destroying implementation:** Onset priority list applied; ch before sh; ok/ot/ol before o — classification is correct. The self-succession test correctly measures whether the LF onset class appears at pos1. No implementation issues.

**Extrapolation:** All claims within tested range. "CONFIRMED" threshold (N≥10, E≥1.5×) correctly applied to ch result (N=15). "dir" for sh (N=6≥5, E≥2×). "(dir)" for t (N=3, E≥2×) correctly parenthesized. "NOT GENERAL" is based on 7 LF classes tested; there could be other rare classes not tested.

**Negative-result scope:** The conclusion "self-succession is selective (ch/sh), not general" is scoped to the 9 LF classes with N_lf≥5 tested in B pharma. Classes with N<5 (e.g., r) could not be tested reliably.

**Control behavior:** No control distributions. N/A.

---

## Conclusion

**F449 ASSIGNED: B pharma ch-LF → ch at pos1 (E=1.64×/N=15, Confirmed); pharma-specific.** B pharma has selective LF-class self-succession at pos1 for gallows classes (ch CONFIRMED, sh dir, t dir) but NOT for template classes (l, ok, o, qok, d). **B pharma vs B herbal inversion:** B herbal ch-LF → ch at pos1 is DEPLETED (0/47 = 0.0% vs 9.5% in pharma). Additional directional findings: d-LF → l at pos1 (E=4.21×/N=4, pharma l-chain connection); ok-LF → t at pos1 (E=2.24×/N=4).
