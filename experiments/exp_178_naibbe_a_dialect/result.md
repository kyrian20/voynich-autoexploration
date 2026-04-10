# exp_178: Naibbe A-Dialect Coverage Analysis
**Date**: 2026-04-10
**Hypothesis**: Does the exp_170 Naibbe falsification extend to A-dialect metrics, or is the null simulation coverage limited to B-dialect?
**Status**: A-DIALECT GAP DOCUMENTED; POSITIONAL FAILURE CONFIRMED. Naibbe fails on 7/8 A-dialect positional/sequential metrics across all 4 conditions. The one partial exception (cth LF depletion, Latin A condition) is a wide-CI artifact. The positional grammar failure is dialect-independent.

**Method**: Re-analysis of existing exp_170 simulation results (400 runs across 4 conditions). No new simulations run. Compares Naibbe output against VMS A-dialect metric targets (exp_173 candidate findings, A-dialect values).

---

## CAVEAT: VOCABULARY MISMATCH

Naibbe is calibrated to Currier B vocabulary statistics: high edy-suffix rate, qok-prefix frequency, l-onset bias. Comparing Naibbe against A-dialect targets is inherently a mismatch on vocabulary metrics — Naibbe was not designed to reproduce A-dialect vocabulary. This comparison is therefore:

- **Informative on positional/sequential metrics**: Position-blind failure is mechanism-inherent, not vocabulary-dependent.
- **Not informative on vocabulary metrics**: edy_rate and edy_ol_ratio failures against A-dialect targets are expected artifacts of dialect calibration mismatch, not evidence against Naibbe for A-dialect.

**The correct null simulation for A-dialect would require a cipher calibrated to Currier A vocabulary statistics.** No such published cipher exists; the Greshko/Naibbe mechanism targets B-dialect by design. This gap is documented as a limitation of the current null simulation coverage.

---

## RESULTS

### Positional/Sequential Metrics (Primary Test)

| Metric | VMS A | Ital-A | Ital-B | Lat-A | Lat-B |
|--------|-------|--------|--------|-------|-------|
| -am LL enrichment | **3.562** | 1.062 [0.755,1.380] **ABOVE** | 0.999 [0.820,1.227] **ABOVE** | 0.625 [0.362,0.903] **ABOVE** | 1.008 [0.816,1.196] **ABOVE** |
| y-onset LF enrichment | **2.459** | 0.724 [0.504,0.899] **ABOVE** | 1.011 [0.838,1.152] **ABOVE** | 1.117 [0.766,1.631] **ABOVE** | 1.011 [0.835,1.233] **ABOVE** |
| d-onset LL enrichment | **1.667** | 0.879 [0.733,1.024] **ABOVE** | 1.000 [0.857,1.143] **ABOVE** | 1.063 [0.867,1.246] **ABOVE** | 0.988 [0.874,1.111] **ABOVE** |
| cth LF depletion | **0.159** | 0.961 [0.533,1.492] BELOW | 0.995 [0.634,1.378] BELOW | 0.332 [0.000,0.834] inside* | 1.023 [0.600,1.435] BELOW |
| ok self-succession | **1.930** | 0.846 [0.639,1.055] **ABOVE** | 0.858 [0.636,1.112] **ABOVE** | 0.958 [0.754,1.158] **ABOVE** | 0.964 [0.768,1.143] **ABOVE** |
| ch self-succession | **1.427** | 0.813 [0.485,1.198] **ABOVE** | 0.793 [0.544,1.113] **ABOVE** | 0.888 [0.581,1.105] **ABOVE** | 0.867 [0.618,1.168] **ABOVE** |
| qok self-succession | **1.623** | 0.843 [0.725,0.982] **ABOVE** | 0.848 [0.710,1.012] **ABOVE** | 0.880 [0.788,0.987] **ABOVE** | 0.886 [0.786,0.997] **ABOVE** |
| daiin→cth enrichment | **2.839** | 0.410 [0.000,1.555] **ABOVE** | 0.423 [0.000,1.613] **ABOVE** | 0.144 [0.000,0.729] **ABOVE** | 0.141 [0.000,0.787] **ABOVE** |

**Legend**: ABOVE = VMS value exceeds cipher CI (cipher underproduces); BELOW = VMS value below cipher CI (cipher overproduces); inside = VMS within cipher CI.

*cth LF Latin-A: Mean 0.332 vs VMS 0.159; "inside" only because the Latin-A CI is wide ([0.000, 0.834]) due to rare cth words. The cipher mean (0.332) is more than twice the VMS value (0.159) — Naibbe substantially underproduces the A-dialect cth depletion, but with insufficient precision to reject it.

### Summary Counts (8 positional/sequential metrics)

| Condition | ABOVE | BELOW | inside |
|-----------|-------|-------|--------|
| Italian-A | 7 | 1 | 0 |
| Italian-B | 7 | 1 | 0 |
| Latin-A | 7 | 0 | 1* |
| Latin-B | 7 | 1 | 0 |

**7/8 or 8/8 positional metrics fail (ABOVE or BELOW) in all four conditions.** The one "inside" (cth LF, Latin-A) is a precision artifact, not a genuine cipher success.

### Vocabulary Metrics (Mismatch by Design)

| Metric | VMS A | Ital-A | Ital-B | Lat-A | Lat-B |
|--------|-------|--------|--------|-------|-------|
| edy rate | **0.043** | 0.151 [0.148,0.155] BELOW | 0.151 [0.146,0.156] BELOW | 0.151 [0.147,0.155] BELOW | 0.151 [0.147,0.156] BELOW |
| edy/ol ratio | **0.650** | 1.965 [1.880,2.057] BELOW | 1.959 [1.863,2.070] BELOW | 2.282 [2.159,2.410] BELOW | 2.286 [2.146,2.437] BELOW |

Naibbe overproduces edy in all conditions (15.1% vs VMS A 4.3%). This is by design: the Naibbe cipher tables target B-dialect vocabulary. These failures do not count against Naibbe as an A-dialect cipher model because Naibbe was never proposed for A-dialect. They are documented for completeness.

---

## INTERPRETATION

### The positional grammar failure is dialect-independent

The core positional metrics (-am LL, y-onset LF, d LL) fail identically against A-dialect and B-dialect targets. Naibbe produces -am LL enrichment of 0.625–1.062× against an A-dialect target of 3.562×. This is the same structural gap as for B-dialect (0.999–1.062× vs B-dialect target 6.811×). The failure is not specific to the B-dialect comparison — it is a property of the position-blind mechanism.

### daiin→cth is an A-dialect finding; Naibbe fails

The daiin→cth enrichment (2.839×) is an A-dialect sequential bigram. Exp_170 explicitly noted this was not a B-dialect finding and treated it as uninformative when VMS-B = 0 and Naibbe ≈ 0. Against the A-dialect target, Naibbe produces 0.14–0.41× (VMS: 2.839×) — clearly ABOVE (underproduces) across all four conditions. Naibbe fails to reproduce the A-dialect daiin→cth sequential preference.

### Onset self-succession fails on A-dialect too

Onset self-succession was already shown to fail in B-dialect (exp_170). The A-dialect comparison confirms: Naibbe produces depleted self-succession (~0.85–0.96×) for qok, ok, and ch, while VMS A-dialect shows enriched self-succession (1.42–1.93×). The cipher mechanism cannot produce word-class clustering.

---

## LIMITATION DOCUMENTATION: A-DIALECT NULL SIMULATION GAP

The current null simulation coverage has the following A-dialect gap:

1. **No A-calibrated Naibbe**: The Naibbe/Greshko cipher is a B-dialect model. No published homophonic cipher has been calibrated to Currier A vocabulary statistics.

2. **What an A-dialect null simulation would require**: A cipher with tables calibrated to A-dialect statistics — lower edy rate (~4%), higher -ol suffix rate, lower qok frequency, higher d-onset frequency, without the edy-dominated suffix paradigm. Testing whether such a cipher (if it existed) could also fail to reproduce positional grammar is theoretically important but not feasible without a published A-dialect cipher model.

3. **Working assumption**: Given that position-blind failure is mechanism-inherent rather than vocabulary-dependent, and given that exp_170 shows the same positional failure pattern for both Italian and Latin plaintext (different vocabulary statistics), the position-blind failure is expected to hold for any A-calibrated cipher as well. This assumption is supported by:
   - The position-sensitive cipher (exp_177) demonstrating that only position-sensitive mechanisms can approach the positional metrics
   - The Timm parameter sweep (exp_176) showing that positional metrics near baseline across 75 parameter combinations that vary vocabulary-level statistics

4. **Documentation in synthesis**: working_position.md will note that A-dialect null simulation coverage is limited to this exploratory cross-dialect comparison, and that a definitive A-dialect falsification would require an A-calibrated cipher model.

---

## CONCLUSION

**The Naibbe positional grammar failure extends to A-dialect metrics.** On 7/8 A-dialect positional and sequential metrics, Naibbe output falls outside the VMS A-dialect value in all four conditions. The failure is consistent with the B-dialect result from exp_170 and with the theoretical expectation that position-blind substitution cannot produce position-sensitive structure regardless of vocabulary calibration.

**The A-dialect null simulation gap is acknowledged as a limitation.** No published cipher exists that targets Currier A, making a fully symmetric A-dialect null simulation infeasible with current tools. The exploratory cross-dialect comparison in this experiment partially fills this gap, showing that the position-blind failure is not dialect-specific.

---

## FILES

- `script.py`: Re-analysis of exp_170 data against A-dialect targets (no new simulations)
- `data/a_dialect_comparison.json`: Per-metric comparison results for all 4 conditions
