# exp_469: B Astro q-bench Triplet — qot-LF and qo-LF Formula Structure (H_new_AJ)

**H_new_AJ:** B astro has qok(1.78×)+qot(1.94×/N=29)+qo(1.60×/N=34) all elevated at LF (F447). Do they have distinct within-line formula routing?

---

## Results

**B astro lines: N=678** (695 total; 678 with ≥2 words)

### B astro LF-class distribution (confirmation of F447)
qok=22.0%(N=149), s=18.1%(N=123), d=14.7%(N=100), y=6.0%(N=41), sh=5.8%(N=39), qo=5.0%(N=34), t=4.4%(N=30), qot=4.3%(N=29)

### q-bench formula routing (within B astro, using astro-specific pos1/pos2/LL baseline)

**qot-LF (N=29):**
- pos1: ch=E1.56×(N=7), qok=E1.28×(N=7), qot=E1.51×(N=2)
- pos2: **ot=E2.82×(N=3)**, l=E1.96×(N=3), sh=E1.55×(N=6)
- LL: **ot=E3.12×(N=4)**, d=E1.23×(N=4), ch=E1.13×(N=4)

**qo-LF (N=34):**
- pos1: **ol=E2.18×(N=7)**, ch=E1.52×(N=8), qo=E1.66×(N=3)
- pos2: ok=E2.16×(N=4), ch=E1.67×(N=7)
- LL: **ch=E1.68×(N=7)**, qok=E1.33×(N=5), ol=E1.16×(N=6)

**qok-LF (N=149):**
- pos1: **ok=E2.00×(N=11)**, ch=E1.34×(N=31), qok=E0.92×(N=26)
- pos2: qok=E1.05×(N=32) — near-baseline; diverse
- LL: l=E1.32×(N=24) — mild elevation

**s-LF (N=123) for comparison:**
- pos1: sh=E1.63×(N=37) — the s→sh formula from F426 confirmed in astro
- LL: diverse, no strong elevation

**d-LF (N=100):**
- pos2: **qot=E1.99×(N=9)** — qot elevated at pos2 in d-LF lines
- LL: diverse

---

## Interpretation

**H_new_AJ CONFIRMED: B astro q-bench classes have distinct within-line formula routing.**

**qot-LF → ot at LL (E=3.12×/N=4)**: NEW directional finding. When B astro opens with qot (LF), the line ends with ot onset (E=3.12×). qot also predicts ot at pos2 (E=2.82×/N=3). This is a B astro within-line spatial pair: qot-LF → ot-LL. This PARALLELS A-dialect's qot/ot spatial pair (F378: A qot is LF-enriched, ot is LL-enriched, they form a mirror-image pair). The B astro qot-LF → ot-LL rule suggests the same qot/ot pairing operates in B astro at the section level, even though B overall has qot as MID/LL-enriched (not LF-enriched), not LF-enriched.

**qo-LF → ol at pos1 (E=2.18×/N=7)**: qo-LF in B astro is followed by ol-onset words at pos1. qo (the A-dialect functional analog of qok, exp_454) routes to ol (the compound terminal class) at pos1. qo-LF → ch at LL (E=1.68×/N=7) — qo-opened lines end with ch onset. Together: qo[LF] → ol[pos1] → ... → ch[LL].

**qok-LF → ok at pos1 (E=2.00×/N=11)**: qok-LF predicts ok at pos1 (the "bare gallows" onset). qok[LF] → ok[pos1] is a B astro pairing — the two high-frequency gallows compound classes (qok, ok) appear as LF-pos1 pairs.

**Summary — B astro q-bench within-line grammar:**
| LF class | pos1 | pos2 | LL |
|----------|------|------|-----|
| qok (22%) | ok(2.0×/11) | diverse | l(1.3×/24) |
| qot (4.3%) | ch(1.6×/7) | ot(2.8×/3,dir) | **ot(3.1×/4,dir)** |
| qo (5.0%) | **ol(2.2×/7)** | ch(1.7×/7) | ch(1.7×/7) |

Each q-bench class has a different within-line routing signature. B astro qot and qo are distinct grammar classes despite both being "q-compound" onsets.

**d-LF → qot at pos2 (E=1.99×/N=9)**: When B astro opens with d (14.7% of lines), qot appears at pos2 with E=1.99×. This creates a cross-class connection: d[LF] → ... → qot[pos2]. Combined with B astro qot-LF → ot[LL], there may be a d[LF] → qot[pos2] → ot[LL] sequence — a B astro within-line 3-word pattern.

---

## Self-Audit

**Target-awareness**: None. Onset-class counts with astro-specific baselines (the correct procedure — using B-overall as baseline would be wrong given B astro's very different LF distribution).

**Feature-destroying implementation**: None. Using astro-specific pos1/pos2/LL distributions as baselines (parallel to exp_466/467's section-specific base rates).

**Extrapolation**: qot-LF → ot LL (E=3.12×/N=4) is directional. qo-LF → ol pos1 (E=2.18×/N=7) is borderline (N≥5 but below standard formula-type threshold). d-LF → qot pos2 (E=1.99×/N=9) is directional. All findings are directional — no formal finding ID.

**Negative-result scope**: qok-LF → qok self-succession at pos1 is NEAR-BASELINE (0.92×) — qok-opened lines do NOT preferentially continue with qok. The qok chain structure in B astro is therefore not a pos1-level rule.

**Control behavior**: B astro-specific pos1/pos2/LL distributions used throughout. These correctly control for section-specific onset class frequencies.

---

## Conclusion

**H_new_AJ CONFIRMED (directional): B astro q-bench triplet classes have distinct within-line formula routing.** Key findings:
- qot-LF → ot at LL: E=3.12×(N=4, dir) — B astro qot/ot spatial pair
- qo-LF → ol at pos1: E=2.18×(N=7, dir)  
- qok-LF → ok at pos1: E=2.00×(N=11)

No formal finding ID (all directional). The B astro q-bench triplet operates as three distinct grammar modes at LF: qok(heavy-traffic, 22%), qot(light, 4.3%) and qo(5.0%) each with different pos1/LL routing. NEW for follow-up: B astro qot-LF → ot-LL parallels A qot/ot spatial pair (F378) — could be worth testing with A astro section if sufficient data.
