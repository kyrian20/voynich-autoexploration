# exp_427: Gallows-Class Generalization of LF-Onset MID Embedding

**Hypothesis (H647):** If the p-LF → 'opch' MID enrichment (F427: E=5.28×) is a general gallows LF→embedded-gallows-in-MID rule, then f-LF lines should show 'ofch' compound enrichment, and t/k-LF should show analogous enrichment for their respective embedded compound prefixes.

**Method:** For each gallows LF class (p, f, k, t), compute rate of words starting with the embedded-gallows prefix ('opch', 'ofch', 'okch', 'otch') at MID positions in that-gallows-LF lines vs all-other-gallows-LF B continuation lines. Also test the broader 'op', 'of', 'ok', 'ot' prefixes. Compare to F427 baseline (p→opch E=5.28×/N=39).

---

## Results

### Embedded compound enrichment by gallows LF class

| LF | Embed prefix | N_LF_lines | LF cnt | LF rate | NLF rate | E |
|----|-------------|-----------|--------|---------|----------|---|
| p | opch | 219 | 39 | 2.70% | 0.51% | **5.28×** |
| f | ofch | 9 | 0 | 0.00% | 0.008% | 0.00× |
| k | okch | 33 | 1 | 0.52% | 0.50% | 1.03× |
| t | otch | 201 | 10 | 0.79% | 0.59% | 1.34× |

### Broader 'o+gallows' prefix embedding

| LF | Prefix | N_LF_lines | LF cnt | LF rate | NLF rate | E |
|----|--------|-----------|--------|---------|----------|---|
| p | op | 219 | 59 | 4.08% | 0.67% | **6.06×** |
| f | of | 9 | 1 | 1.41% | 0.11% | 12.30×* |
| k | ok | 33 | 8 | 4.12% | 7.72% | 0.53× |
| t | ot | 201 | 78 | 6.15% | 7.25% | 0.85× |

*f→'of': N=1 (ofar, 1 occurrence in 9 f-LF lines / 71 MID tokens) — completely directional, uninformative.

### 'ofch' corpus survey

| Compound | N (B cont lines) |
|---------|-----------------|
| opch-prefix total | 111 |
| ofch-prefix total | 14 |
| ofchedy | 5 |
| ofchdy | 3 |
| ofchy | 2 |

'ofch' compounds exist in the corpus (N=14) but are not concentrated in f-LF lines.

---

## Interpretation

**H647 REFUTED for k and t; inconclusive for f (N too small).**

The p→opch self-referential enrichment (5.28×) does NOT generalize to other gallows classes:

- **t (N_lines=201)**: otch MID in t-LF = E=1.34×/N=10 — below the 2.0× threshold. With N=201 t-LF lines, the signal is measurable and is clearly below formula-type threshold. The broader 'ot' prefix is DEPLETED in t-LF MID (0.85×), consistent with t-LF lines not pulling ot-class words.
- **k (N_lines=33)**: okch MID in k-LF = E=1.03×/N=1 — near-baseline. The broader 'ok' prefix is DEPLETED in k-LF MID (0.53×).
- **f (N_lines=9)**: ofch count=0 in f-LF MID (9 lines, 71 MID tokens) — completely directional, no enrichment. The 'ofch' compound vocabulary exists (N=14 in full B corpus) but does not appear in f-LF lines, though the sample is too small to conclude.

**p-specificity confirmed:** The self-referential structure (p-gallows embedded in MID compound words in p-LF lines) is specific to the p-formula line type. This distinguishes p from other gallows classes at a third level of analysis: p is the strongest gallows LF class (F412), p-formula lines have pan-positional ch-avoidance and o-enrichment (F409, F417), and now p-formula lines specifically accumulate p-embedded 'opch' compound words at MID (F427). No analogous multi-scale structure exists for f/k/t.

The p→'op' broader prefix enrichment (E=6.06×/N=59) shows that ALL o-gallows-compound words (not just 'opch' variants) are enriched in p-LF MID. This extends F427: it is the presence of the p-gallows character within any o-onset compound word that is enriched, not just the 'opch' specific compound type.

---

## Limitations

- f-LF N=9 lines is too small for any conclusion; 'ofch' corpus total is only 14.
- k-LF N=33 is modest but sufficient to rule out large enrichment (0.53× is well below 1.0).
- The broader 'of'/'ok'/'ot' prefix analysis is confounded: 'ok' and 'ot' are their own onset classes, so the 'ok' and 'ot' prefix rates mostly reflect onset-class distributions, not gallows-embedding specifically.
- Mechanism unknown: why does p specifically have this self-referential embedding structure?

---

## Self-Audit

**Target-awareness**: No target-aware elements.

**Feature-destroying implementation**: No feature-destroying elements. MID word extraction and prefix matching are transparent operations that preserve the feature under test.

**Extrapolation**: The f-LF conclusion is explicitly stated as "inconclusive (N too small)." The k and t conclusions are stated as "below threshold for the tested corpus." No extrapolation to untested parameter ranges.

**Negative-result scope**: The conclusion for k and t is "below formula-type threshold in B continuation lines under this test." This is appropriately scoped to the tested sample and threshold.

**Control behavior**: Non-LF-gallows lines serve as baseline. Expected: opch enrichment at 5.28× (from F427, reproduced exactly). Actual: reproduced exactly. Other gallows classes produce E near 1.0 or below (k=1.03×, t=1.34×), consistent with absence of the self-referential structure. Controls behaved as expected.

---

## Conclusion

H647 REFUTED (k/t), inconclusive (f). p→opch self-referential enrichment (E=5.28×) does NOT generalize to other gallows LF classes. k-LF: okch=1.03×(N=1), ok-MID DEPLETED(0.53×). t-LF: otch=1.34×(N=10), below threshold. f-LF: N=9 too small. The p-formula line type uniquely concentrates p-gallows embedded compound words (opch/op-prefix) at MID — a third scale at which p distinguishes itself from other gallows classes.
