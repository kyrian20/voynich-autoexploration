# exp_497: B herbal pos2 Full Survey

**Question:** (H_new_BX) Does B herbal have confirmed pos2 routing rules beyond F457/F458?

---

## Corpus

B herbal: 269 lines. pos2 baseline (len≥3 lines, N=239): ch=23.0%, sh=18.0%, a=7.9%, qok=7.1%, d=7.1%, ok=6.7%, k=5.4%, o=5.0%.

---

## Results

### Confirmed findings

| LF | pos2 onset | obs/N_elig | E | flag | note |
|----|-----------|-----------|---|------|------|
| d | sh | 10/32 | 1.74× | **CONFIRMED** | F457 reproduced |

F457 (d-LF → sh@pos2) is confirmed with len≥3 eligibility.

### FLAG: F458 (ch-LF → ch@pos2) Discrepancy

F458 claimed E=1.74×/N=19 CONFIRMED (exp_482). Current result with len≥3 eligibility:
- obs=13/41, E=1.38× — **BELOW confirmation threshold**

The discrepancy is 19 vs 13 observations, with N_elig=48 (if len≥2) vs N_elig=41 (if len≥3). 7 B herbal ch-LF lines have len=2; in 2-word lines, ws[1]=ws[-1]=LF word. If exp_482 used len≥2 eligibility, 2-word ch-LF lines would trivially have ch at "pos2" (which equals the LF word). This inflates the ch→ch@pos2 count: estimated +7 trivial self-chain observations, producing 20/48 ≈ 1.81×, close to the claimed 1.74×.

**F458 is flagged for re-examination.** With len≥3 (correct, avoiding LF-as-pos2 contamination), B herbal ch→ch@pos2 = E=1.38×/N=13 — below confirmation threshold.

### New directional findings

| LF | pos2 onset | obs/N_elig | E | flag |
|----|-----------|-----------|---|------|
| ok | o | 6/35 | 3.41× | **dir** |
| ol | qok | 4/13 | 4.33× | **(dir)** |
| ot | sh | 4/11 | 2.02× | **(dir)** |

**ok-LF → o@pos2 (dir, E=3.41×/N=6):** New. B herbal ok-LF lines have o-onset words at pos2 at 3.41× the pos2-specific baseline. ok-self@pos2 is DEPLETED (E=0.43×/N=1). Compare: B herbal ok-LF pos1 has o@pos1 (dir, E=5.17×/N=3); A herbal_a ok-LF has y at pos1 (F455) + ok-self at pos2 (F467, A-herbal_a). B herbal ok-LF routing is to o-class at both pos1 and pos2.

**ol-LF → qok@pos2 ((dir), E=4.33×/N=4):** New. B herbal ol-LF lines have qok-onset words at pos2 at 4.33× baseline. N=4 only.

**ot-LF → sh@pos2 ((dir), E=2.02×/N=4):** New. B herbal ot-LF has sh at pos2. Note: sh is the 18.0% baseline onset (dominant pos2 onset in B herbal), so this enrichment is against that already-elevated baseline.

### B herbal pos2 self-chaining: NOT universal

| LF | self@pos2 | N_elig | E |
|----|----------|--------|---|
| ch | 13 | 41 | 1.38× |
| d | 3 | 32 | 1.32× |
| sh | 4 | 16 | 1.39× |
| ok | 1 | 35 | 0.43× (DEPLETED) |
| ot | 0 | 11 | 0.00× (ZERO) |
| ol | 0 | 13 | 0.00× (ZERO) |
| a | 2 | 15 | 1.68× |
| o | 1 | 16 | 1.24× |

No B herbal LF class shows confirmed pos2 self-chaining. ot and ol have ZERO. ok is DEPLETED. The A herbal_a universal self-chaining (F468) does NOT hold in B herbal (consistent with exp_489 which showed ot/ol/l obs=0 in B herbal — now confirmed also with correct len≥3 eligibility).

**The B herbal pos2 baseline is dominated by ch (23.0%)** — ch-onset words are the most common pos2 words in B herbal regardless of LF class. Compare to A herbal_a where self-chaining drives the pos2 distribution. B herbal has a default "ch filler" at pos2 rather than LF-class-specific self-chaining.

---

## Interpretation

**B herbal pos2 grammar (exp_497 summary):**
- **Confirmed:** d→sh@pos2 (F457 reproduced, E=1.74×/N=10)
- **Flagged:** ch→ch@pos2 (F458): with correct len≥3, E=1.38×/N=13 — below threshold. The 2-word line contamination bug likely inflated exp_482's result.
- **New dir:** ok→o@pos2 (E=3.41×/N=6); ol→qok@pos2 ((dir), N=4); ot→sh@pos2 ((dir), N=4)

B herbal pos2 grammar is SELECTIVE (one confirmed cross-class rule: d→sh), NOT universal self-chaining. This contrasts sharply with A herbal_a (universal self-chaining, F468). B herbal's dominant pos2 word is ch-onset regardless of LF class, suggesting ch-onset words serve a body-position filler role in B herbal.

---

## Self-Audit

**Target-awareness:** No target-aware elements. pos2 baseline uses B herbal pos2 distribution with len≥3 eligibility.

**Feature-destroying implementation:** N/A — survey.

**Extrapolation:** F458 flag is clearly within scope: the discrepancy between 19 (exp_482) and 13 (exp_497) observations for ch→ch@pos2 matches the expected inflation from 7 two-word line inclusions. The mechanism (2-word line adds LF word as pos2 word trivially) is explicit.

**Negative-result scope:** "B herbal pos2 self-chaining is not universal" — stated as observed zero/depleted rates for ot/ol/ok; the confirmed absence for ot and ol (N_elig=11 and 13) is well-powered.

**Control behavior:** No controls. N/A.

---

## Conclusions

**H_new_BX ANSWERED:**
- B herbal pos2 has ONE confirmed rule: d→sh@pos2 (F457 reproduced)
- F458 (ch→ch@pos2) is FLAGGED: with correct len≥3, E=1.38×/N=13 — likely a 2-word line contamination artifact in exp_482
- New directional: ok→o@pos2 (dir, E=3.41×/N=6)
- B herbal pos2 self-chaining is NOT universal; most classes near or below baseline

**Q009 OPENED:** F458 potentially needs correction (2-word line eligibility bug in exp_482). Need to re-run B herbal ch-LF pos2 with exp_482's exact methodology to confirm bug.
