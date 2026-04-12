# exp_526 result — A stars a-LF grammar (H_new_ER) + full A stars grammar survey

## Audit

**Target-awareness**: No target-aware elements. All measurements are corpus observations with standard methodology.

**Feature-destroying implementation**: Standard positional grammar methodology: pos1 uses len≥2 eligibility; pos2 and pen use len≥3 eligibility. Section definitions: A stars = 57≤n≤72, not is_b_dialect (5 folios, 136 lines); A herbal_a = n≤56, not is_b_dialect; B herbal = n≤72, is_b_dialect. is_b_dialect = endswith edy/eedy threshold 5%.

**Extrapolation**: None. Direct corpus measurements.

**Data quality flag**: One of 2 t-LF lines in A stars contains English words ("stars one less than") with LF word "than" onset=t. This is a corpus artifact — the ZL3b transcription includes some non-EVA text (likely researcher annotations or folio headings) that passes the `re.match(r'^[a-z]+$', w)` filter. This does not affect Part 1-3 results meaningfully but is relevant to Q011.

**F470 contamination flag**: F470 (B herbal a→a@pos2 dir, E=3.60×/N=6, exp_489) used N_elig=19; exp_526 uses N_elig=16. The 3-line difference is due to exp_489 likely using len≥2 for pos2 eligibility, including 2-word a-LF lines where pos2=LF trivially (same bug as Q009/F458). With len≥3 eligibility: a@pos2 obs=2, E=1.54× (below any threshold). Q012 raised.

---

## H_new_ER: A stars a-LF grammar — NEGATIVE (all positions flat)

**A stars a-LF (N=15 lines, 11.0% of A stars LF)**

### pos1 (N_elig=14):
No class meets any threshold. Highest-E classes:
- sh: obs=2, E=2.65× (below (dir), N<3)
- t: obs=3, E=1.74× (below (dir), E<2.5)
- y: DEPLETED (E=0.71×/obs=2)
- d: DEPLETED (E=0.34×/obs=1)
- ch: ZERO (obs=0)

**a-self at pos1: obs=1, E=9.29× (single obs, N=1 — noise only)**

### pos2 (N_elig=13):
No class meets any threshold:
- ol: obs=2, E=3.13× (below (dir), N<3)
- o: obs=2, E=2.09× (below any threshold)
- **a-self at pos2: obs=2, E=1.04× — BASELINE. a-LF does NOT self-chain at pos2.**
- sh, ok, y, ot, s: all ZERO

### pen (N_elig=13):
No class meets any threshold:
- ot: obs=2, E=3.75× (below (dir), N<3)
- o: obs=2, E=2.68× (below (dir))
- ch: DEPLETED (E=0.35×/obs=1)

**H_new_ER CONCLUSION: NEGATIVE. A stars a-LF grammar is FLAT at all positions. No confirmed, dir, or (dir) rules. The a-self@pos2 E=1.04× is notable: a-LF is the only major LF class in A stars that does NOT show pos2 self-chaining enrichment. a-LF appears grammatically inert in the within-line positional slot.**

Why is a-LF so prominent in A stars (11%) but grammatically flat? This may indicate that a-LF is a section-specific topic marker rather than a grammatical class with internal structure. The high frequency of a-LF in A stars may reflect lexical/semantic content (zodiac/calendar imagery) rather than grammatical patterning.

---

## F503 and F504 Reproduced

- A stars o-LF pos1=y: E=2.50×/obs=7 (dir) ✓ **F503 confirmed**
- A stars o-LF pos2=o-self: E=4.17×/obs=4 ((dir)) ✓ **F504 confirmed**

---

## Part 2: Cross-Section a-LF Comparison

### A herbal_a a-LF (N=16 lines):
All positions below threshold. Notable near-signals:
- pos1: y E=1.76×/obs=4 (below dir)
- pos2: ch E=1.46×/obs=7 (below CONF)
- pen: a-self E=11.84×/obs=2 (N=2, below (dir) threshold) — borderline self-chaining at pen

### B herbal a-LF (N=20 lines):
**NEW signals at pen (not pos2):**
- **pen=ok: E=2.85×/obs=5 (dir)** — B herbal a-LF → ok@pen (F522)
- **pen=o: E=4.10×/obs=4 ((dir))** — B herbal a-LF → o@pen (F522)

pos2: a-self E=1.54×/obs=2 — **F470 NOT REPRODUCED**. F470 claimed E=3.60×/N=6 with N_elig=19; exp_526 with len≥3 finds obs=2, E=1.54×. Discrepancy consistent with Q009-type 2-word line contamination (3 extra eligibles in exp_489 are likely 2-word a-LF lines). Q012 raised.

---

## Part 3: A Stars Full Grammar Survey — New Findings

### A stars ch-LF (N=23 lines):
- **pos2=ot: E=3.81×/obs=5 (dir)** — NEW F517
- pos1: y DEPLETED (E=0.45×/obs=2); no pos1 rule
- pen: ch-self E=1.81×/obs=8 (below CONF)

### A stars d-LF (N=25 lines):
- **pos2=d-self: E=2.54×/obs=4 ((dir))** — NEW F518a
- **pen=s: E=5.08×/obs=4 ((dir))** — NEW F518b
- pos1: y DEPLETED (E=0.42×/obs=2); d-self E=1.60×/obs=8 (below CONF)

### A stars sh-LF (N=10 lines):
- **pos2=sh-self: E=3.49×/obs=4 ((dir))** — NEW F519a (self-chaining at pos2 confirmed in A stars)
- **pen=a: E=3.05×/obs=3 ((dir))** — NEW F519b (sh-LF pen routes to a-onset in A stars)
- pos1: y E=2.00×/obs=4 (borderline dir — obs≥5 needed; BELOW dir)

### A stars ot-LF (N=9 lines):
- **pos2=a: E=3.01×/obs=4 ((dir))** — NEW F520
- Note: ot-LF pos2=a was ARTIFACT in A herbal_a (exp_521: obs=0 in strict 1-56). This is section-specific: ot-LF uses a at pos2 in A stars but has zero signal in A herbal_a. A cosmo: not tested.

### A stars ol-LF (N=7 lines):
- **pos1=s: E=4.64×/obs=3 ((dir))** — NEW F521
- pos2: all below threshold

### A stars ok-LF (N=10 lines):
- No positions meet threshold. Highest: ok pos2=a E=2.26×/obs=3 (E<2.5×, below (dir))

### A stars o-LF (N=14 lines):
- pos1=y: E=2.50×/obs=7 (dir) — F503 reproduced ✓
- pos2=o-self: E=4.17×/obs=4 ((dir)) — F504 reproduced ✓

---

## Q011 Investigation: F446 Range Test

No section definition puts t-LF at the level F446 claimed (N=15, 11.7% rate):
- A stars 57-72 (current): N=2/136 = 1.5%
- A stars 57-84 (extended): N=2/136 = 1.5%
- A stars 57-102 (widened): N=8/432 = 1.9%
- A stars 57-116 (maximal): N=8/432 = 1.9%

None approaches 11.7%. The discrepancy cannot be explained by section range changes alone. Most likely cause remains corpus update or different parsing methodology in exp_466. Additional note: one t-LF line in current A stars is a corpus artifact (contains English words). With N=2 total and one being garbage, actual clean t-LF in A stars may be N=1.

---

## Summary

| Hypothesis/Question | Result |
|-------------------|--------|
| H_new_ER: A stars a-LF grammar | NEGATIVE: flat at all positions; no (dir)+ rules; a-self@pos2 baseline (E=1.04×) |
| F503 (o-LF pos1=y A stars) | REPRODUCED: dir ✓ |
| F504 (o-LF pos2=o-self A stars) | REPRODUCED: (dir) ✓ |
| F470 (B herbal a→a@pos2 dir) | NOT REPRODUCED (E=1.54×/obs=2 with len≥3). Q012 raised. |
| Q011: F446 range test | Range changes cannot explain F446's N=15. Corpus/parsing most likely. |

**New findings:**
- F517: A stars ch-LF → ot@pos2 dir (E=3.81×/obs=5)
- F518: A stars d-LF → d-self@pos2 (dir) (E=2.54×/obs=4); d-LF → s@pen (dir) (E=5.08×/obs=4)
- F519: A stars sh-LF → sh-self@pos2 (dir) (E=3.49×/obs=4); sh-LF → a@pen (dir) (E=3.05×/obs=3)
- F520: A stars ot-LF → a@pos2 (dir) (E=3.01×/obs=4) — A stars-specific (zero in A herbal_a)
- F521: A stars ol-LF → s@pos1 (dir) (E=4.64×/obs=3)
- F522: B herbal a-LF pen: ok@pen dir (E=2.85×/obs=5), o@pen (dir) (E=4.10×/obs=4)

**New open questions:**
- Q012: F470 (B herbal a→a@pos2 dir) not reproduced with len≥3. Possible 2-word contamination in exp_489 (same bug as Q009/F458).

**New hypothesis generated:** H_new_ES — A stars has 6 new positional grammar rules across ch/d/sh/ot/ol LF classes. Pattern: A stars grammar is section-specific and differs from A herbal_a (e.g., ot→a@pos2 is zero in A herbal_a but (dir) in A stars; sh→a@pen has no A herbal_a parallel). Is there a systematic cross-LF-class a-onset role in A stars internal grammar (a appears at pen of sh, pos2 of ot)?
