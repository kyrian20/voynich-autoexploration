# exp_302: Simulation Per-Onset Closed Paradigm Diagnostic (Q007)

**Date:** 2026-04-11
**Hypothesis:** Q007 — vocabulary over-production: simulation generates 2.2× too many MID types

## Result: DIAGNOSTIC COMPLETE — modified path is primary source; qok paradigm 17× over-produced

### VMS Per-Onset Closed Paradigm (MID words only)

| Onset | MID N | Types | CP90 | CP90% |
|-------|-------|-------|------|-------|
| qok   | 1965  | 150   |  32  | 21.3% |
| ok    | 1041  | 151   |  67  | 44.4% |
| ot    |  999  | 156   |  83  | 53.2% |
| sh    | 1461  | 275   | 145  | 52.7% |
| ch    | 2447  | 467   | 284  | 60.8% |
| qot   |  613  |  88   |  46  | 52.3% |
| d     |  674  | 150   | 149  | 99.3% |

### Simulation Per-Onset Over-Production (N=10 trials, R_MID=0.20)

| Onset | Sim Types/trial | Sim CP90 | VMS CP90 | Ratio |
|-------|----------------|----------|----------|-------|
| qok   | 794            | 553      | 32       | 17.28× |
| qot   | 286            | 217      | 46       |  4.71× |
| ok    | 455            | 348      | 67       |  5.19× |
| ot    | 435            | 333      | 83       |  4.01× |
| sh    | 583            | 438      | 145      |  3.02× |
| ch    | 1002           | 735      | 284      |  2.59× |
| d     | 428            | 328      | 149      |  2.20× |

**Overall vocabulary:** 3,888 unique MID types/trial vs VMS 2,929 — ratio **1.33×** (previously estimated 2.2× from different architecture; current architecture improved with beta=0.30 and R_MID=0.20).

### Origin Analysis for qok-Onset MID Words (all 10 trials)

| Path     | Tokens | Unique types | Type/Token ratio |
|----------|--------|-------------|-----------------|
| modified | 13,447 (55.6%) | 3,498 | 26.0% |
| cipher   |  9,131 (37.7%) |   764 |  8.4% |
| copy     |  1,476 (6.1%)  |   482 | 32.7% |
| stutter  |    151 (0.6%)  |     0 |  0% |

## Key Findings

### F1: qok paradigm is the most over-produced (17×) due to VMS concentration

The VMS qok-onset vocabulary is extremely concentrated: 32 types cover 90% of 1,965 MID tokens. The simulation generates 553 types for 90% coverage — a 17× over-production. This is the largest discrepancy of any onset class. The VMS qok slot behaves like a closed register of ~32 canonical forms used repeatedly; the simulation treats qok as a freely-generated onset class.

### F2: Modified path generates 73% of unique qok types despite producing 56% of tokens

The `modified` path produces 3,498 unique qok types from 13,447 tokens (type/token=26%). This is the dominant source of vocabulary explosion. Each modification of a qok buffer word generates a near-unique new form because the modification step changes one character in the midfix region, producing a word that has likely never appeared before. For onset classes with sparse midfixes (qok ZeroMid=66%), modifications either destroy the word's validity or generate rare combinations.

### F3: Cipher path also over-produces for qok (764 types from 9,131 tokens = 8.4% TTR)

Even the cipher component generates qok words with 8.4% type/token ratio (764 unique types). VMS qok has 150/1965 = 7.6% TTR — so the cipher path alone is nearly VMS-calibrated for qok TTR! The over-production comes from the *number* of cipher draws, not the diversity of each draw. However, in terms of CP90 concentration, the cipher draws are still spread across too many types.

### F4: d-onset shows tightest simulation/VMS paradigm gap (2.20×)

d-onset has the smallest ratio (2.20×) and the VMS d-onset has d=149 types for CP90 (99.3% of all 150 d-types). In the VMS, essentially every d-type is needed for 90% coverage — the d-onset has almost no dominant forms (flat distribution). The simulation's 2.20× over-production is therefore due to more types, not more concentration.

### F5: Sparse-midfix onsets have highest over-production; rich-midfix onsets have lowest

Over-production ratios: qok=17×, qot=4.71×, ok=5.19×, ot=4.01× vs ch=2.59×, sh=3.02×, d=2.20×. The sparse-midfix onsets (which have ZeroMid≥60%) show the worst vocabulary explosion. This is mechanistically coherent: in the VMS, sparse-midfix words are highly repetitive (using the same canonical ZeroMid forms repeatedly), but the simulation's modification and cipher paths generate varied midfixes even for sparse-midfix onset classes.

## Interpretation

The core problem is a mismatch between the **VMS qok paradigm structure** (32 canonical forms, heavily repeated) and the **simulation generation model** (freely generates new onset×midfix×suffix combinations). The 17× over-production for qok is because:

1. VMS has a closed lexical slot for qok: ~32 forms function as recurrent grammatical elements
2. The simulation's `modified` path treats qok as a productive slot (any onset + any modification = valid word)
3. The simulation's `cipher` path generates qok from the cipher component, which has no paradigm memory

**Overall vocabulary ratio (1.33×) is less alarming than the per-onset CP90 ratios (2.20–17×)** because the overall ratio measures total unique types (many hapaxes), while CP90 measures concentration of frequent types. The VMS is much more concentrated at the top of each onset class than the simulation — even though the total type counts may not differ drastically.

## Mechanism proposal

To match per-onset closed paradigm sizes, the simulation needs onset-class-specific vocabulary pools:
- For sparse-midfix onsets (qok, ok, ot, qot): draw from a finite pool of N canonical types (e.g., 50 for qok, 100 for ok/ot). This constrains the paradigm.
- For rich-midfix onsets (ch, sh): allow free generation as currently (CP90 ratio already 2.59-3.02×, closer to acceptable).
- Alternative: increase onset-specific copy probability for sparse-midfix classes (rather than sending to modified or cipher paths).

The copy path has 32.7% type/token ratio for qok — paradoxically *higher* than modified (26%) because copy draws from whatever is in the buffer. A pre-populated buffer dominated by canonical qok forms would be self-reinforcing.

## Self-Audit

**Target-awareness:** VMS_CP90 targets (qok=32, ok=67, etc.) are used as comparison benchmarks, not calibration targets. All simulation parameters (R_MID=0.20, beta=0.30, cp=0.55, mp=0.90, etc.) were fixed from prior experiments calibrated against different metrics (am_mid_enr, edy_rate, MID slope, etc.). No parameter in this experiment was tuned to match closed paradigm sizes. No target-aware elements identified.

**Feature-destroying implementation:** This is a passive diagnostic — measuring what the existing simulation produces, not testing a new mechanism. Onset-preservation (from exp_181) is intact. The `run_sim_tracked()` extension adds origin tagging without modifying the generation process. No feature-destroying implementation details identified.

**Extrapolation:** All claims are within the tested parameter range (R_MID=0.20, beta=0.30, 10 trials). "Behaves like a closed register" language is observational and appropriately hedged. The mechanism proposals in Next Steps are explicitly labeled as proposals, not conclusions. No "structural/cannot/impossible" language used.

**Negative-result scope:** N/A — this is a diagnostic measurement rather than a pass/fail hypothesis test.

**Control behavior:** No explicit null model or control distribution was used. The comparison is simulation-generated CP90 vs VMS-measured CP90, both computed using the same `closed_paradigm_size()` function on analogous token streams. No control-comparison issues.

## Next steps

- **exp_303 (H505):** Test finite vocabulary pool for sparse-midfix onsets: pre-build a qok lexicon of N=50-100 canonical types and draw from it for all MID qok words. Measure: does CP90 ratio drop from 17× toward 1×? Does 19/19 battery hold?
- Alternatively: test onset-conditional copy probability: p_copy_qok = 0.85 (vs current 0.55) for MID qok words.
