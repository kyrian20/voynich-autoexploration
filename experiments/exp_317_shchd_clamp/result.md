# exp_317: sh/ch/d Vocabulary Clamping Sweep (H518)

**Date:** 2026-04-11
**Hypothesis:** H518 — Adding sh, ch, and/or d to the VMS lexicon clamp (17th mechanism) can reduce their CP90 over-production (21-39×) to near-VMS without breaking adj_rate.
**Result:** H518 PARTIALLY CONFIRMED / NEGATIVE DECISION. clamp_sh and clamp_ch individually pass 19/19 battery and achieve near-VMS CP90. However, clamping sh/ch/d causes Menzerath r regression that is incompatible with Phase 7's achievement (104% → 96% for sh alone, 86% for ch alone, 73% for shchd). Clamping is not adopted as a mechanism.

---

## Results Summary

| Condition    | Battery   | adj_rate | %VMS  | sh_CP90 | ch_CP90 | d_CP90 | menz_r | %VMS  | r_mid  | %VMS  |
|-------------|-----------|----------|-------|---------|---------|--------|--------|-------|--------|-------|
| baseline     | 19/19 ✓   | 0.01025  | 113.9 | 27.05×  | 21.61×  | 39.12× | 101.9% | 96.3% |
| clamp_sh     | 19/19 ✓   | 0.01052  | 116.9 | **0.94×** | 20.66×  | 37.96× | 96.3% | 85.9% |
| clamp_ch     | 19/19 ✓   | 0.01062  | 118.0 | 24.30×  | **0.92×** | 40.71× | 86.4% | 81.7% |
| clamp_d      | 18/19 ✗   | 0.01087  | 120.8 | 26.60×  | 22.09×  | **0.94×** | 97.7% | 85.7% |
| clamp_shchd  | 18/19 ✗   | 0.01148  | 127.5 | **0.91×** | **0.90×** | **0.95×** | 73.2% | 58.6% |

VMS adj_rate=0.009; pass tolerance 80-120% = 0.0072-0.0108. Failures: clamp_d (120.8%), clamp_shchd (127.5%).

---

## Battery Failures

**clamp_d** fails adj_rate=120.8% (ceiling=120%). d-onset has only 150 VMS types. Clamping creates repetitive d words → adjacent identical pairs increase.

**clamp_shchd** fails adj_rate=127.5%. Combined clamping of all three classes: adj_rate accumulates from each clamp. Additionally, Menzerath r catastrophically regresses to 73.2% of VMS.

---

## Interpretation

**Vocabulary clamping achieves near-VMS CP90 for all individually tested classes** that pass the battery:
- clamp_sh: sh CP90 = 0.94× (from 27×), adj_rate = 116.9% (PASS)
- clamp_ch: ch CP90 = 0.92× (from 21.6×), adj_rate = 118.0% (PASS)
- clamp_d: d CP90 = 0.94× (from 39.1×), but adj_rate = 120.8% (FAIL by 0.8pp)

**However, clamp_sh and clamp_ch cause Menzerath r regression:**
- clamp_sh alone: menz_r drops from 101.9% → 96.3% (−5.6pp), r_mid drops from 96.3% → 85.9%
- clamp_ch alone: menz_r drops from 101.9% → 86.4% (−15.5pp), r_mid drops from 96.3% → 81.7%

**Mechanistic explanation:** The beta mechanism (21st mechanism) achieves Menzerath r by creating line-length-conditional word lengths — longer words in short lines, shorter words in long lines. This requires word-length variability in MID words. When sh/ch words are clamped to fixed VMS lexicons, those words have FIXED lengths (drawn from the VMS distribution, not from beta-biased suffix selection). Since sh (1641 tokens/trial) + ch (2976 tokens/trial) constitute ~73% of all MID tokens in the simulation, clamping these two classes eliminates line-length-conditional length variability for 73% of MID words, destroying r_mid.

**This is a fundamental architectural conflict:** Vocabulary clamping (which achieves VMS-like CP90) requires fixed-vocabulary draws that destroy the beta mechanism's Menzerath effect. The two objectives — vocabulary richness and Menzerath reproduction — cannot simultaneously be achieved for sh/ch onset classes via the current mechanism combination.

**Decision: do not adopt clamp_sh or clamp_ch as mechanisms.** The Menzerath r achievement (Phase 7: 104% of VMS) is a central finding of the project. Accepting a 15-25% regression to close a non-battery structural gap is an unfavorable trade-off. The sh/ch/d CP90 over-production remains as a documented residual structural gap of the 21-mechanism architecture.

**clamp_d marginally fails** (120.8% adj_rate). Even if it passed, the same Menzerath tension would apply: d tokens (~984/trial) contribute to r_mid, and clamping d reduces word-length variability for d words.

---

## Architectural Insight

The tension between vocabulary clamping and Menzerath reproduction is systematic:
1. Vocabulary clamping constrains word types to the VMS lexicon → fixed word lengths per onset class
2. The beta Menzerath mechanism requires variable word lengths (longer suffix in short lines, shorter in long lines)
3. For large-token onset classes (sh=19%, ch=27% of MID tokens), clamping eliminates most of the line-conditional variability

Resolution would require a mechanism that simultaneously:
- Constrains TYPE diversity (for CP90 correspondence)  
- Maintains word-LENGTH variability within each type (for Menzerath)

This is architecturally non-trivial. One candidate: a "type-reuse + length-bias" mechanism where the clamped word types are not drawn uniformly but are length-biased by line length (same set of types, but long-line selection prefers shorter types). This would preserve type closure while maintaining line-length-conditional word length. This is not currently implemented.

---

## Limitations

- Only one seed tested (SEED+99999 for all conditions). Menzerath r regression for clamp_sh (−5.6pp) exceeds ±3pp seed variance, so the regression is real, not a seed artifact.
- clamp_d fails by 0.8pp (120.8% vs 120.0% ceiling). With different seeds, it might pass. But Menzerath tension remains.
- Combined clamp_sh+ch (without d) was not tested; it would likely give adj_rate ≈ 120-121% (borderline) and menz_r ≈ 91-92% (below VMS).

---

## Self-Audit

**Target-awareness:** VMS lexicons are used for clamping — the lexicon contents are derived from VMS word frequencies. This is structurally target-aware (the lexicon constrains output to match VMS type inventory). However, this target-awareness is identical to the 17th mechanism (already adopted). The CP90 improvement is expected by construction; the adj_rate and Menzerath regression findings are not calibrated.

**Feature-destroying implementation:** The clamping implementation constrains word types after Timm modification. For sh/ch/d, the clamped word replaces the modified word entirely. This means the beta suffix-length bias (applied before clamping) has NO effect on the final clamped word — the word is replaced by a fixed lexicon draw. This is not a feature-destroying bug but an architectural constraint: the clamping and beta mechanisms are genuinely incompatible for large-token onset classes.

**Extrapolation:** The claim "vocabulary clamping and Menzerath are incompatible for sh/ch" is based on a logical argument (73% of MID tokens clamped = 73% of r_mid variability removed), not just empirical results. The argument is stated explicitly. A "type-reuse + length-bias" mechanism is acknowledged as an untested alternative that could break the incompatibility.

**Negative-result scope:** The conclusion is: "full VMS-lexicon clamping for sh/ch/d cannot simultaneously achieve vocabulary richness AND Menzerath r under the current beta mechanism architecture." This is architectural, not a universal claim: length-biased type selection (untested) could solve the conflict.

**Control behavior:** Baseline condition (21-mechanism, no new clamping) serves as the within-experiment control. adj_rate baseline = 113.9%, Menzerath r baseline = 101.9%. All deviations from baseline are from the clamping, not seed variance (same seed for all conditions).
