# exp_446: Suffix Type Positional Distribution (H_new_H)

**Hypothesis (H_new_H):** Specific suffix types show position-specific enrichment at LF/MID/LL. F436 documents template/content onset split in suffix class preferences; this tests whether the suffix-level differentiation extends to positional grammar.

**Method:** ZL3B continuation lines, Stolfi decomposition. Count suffix-type rates at LF/MID/LL. E = (suffix_rate_at_pos) / (suffix_rate_global). Require global N≥50 for individual suffixes; N≥50 for suffix class analysis.

---

## Results

### Individual suffix positional enrichment (E≥1.4, global N≥50)

**A-dialect:**

| Suffix | Global% | LF E | MID E | LL E | Global N |
|--------|---------|------|-------|------|----------|
| 'iin' | 1.2% | 0.69× | 0.88× | **2.23×** | 71 |
| 'cthy' | 0.9% | 1.11× | 0.92× | **1.46×** | 51 |
| 'am' | 1.8% | **1.41×** | 1.00× | 0.51× | 109 |
| 'al' | 4.6% | **0.59×** | 1.08× | 0.88× | 274 |

**B-dialect:**

| Suffix | Global% | LF E | MID E | LL E | Global N |
|--------|---------|------|-------|------|----------|
| 'dy' | 5.5% | **1.86×** | 0.94× | 1.28× | 678 |
| 'shey' | 0.6% | 0.81× | 0.96× | **2.17×** | 78 |
| 'r' | 1.2% | 0.88× | 0.97× | **1.85×** | 144 |
| 'shedy' | 1.1% | **1.42×** | 0.99× | 0.73× | 133 |
| 'l' | 1.3% | **0.40×** | 1.05× | 0.62× | 157 |

### Suffix class positional enrichment

| Class | A LF E | A LL E | B LF E | B LL E |
|-------|--------|--------|--------|--------|
| edy-class | 0.82× | 1.00× | 0.95× | **0.87×** |
| aiin-class | 1.05× | 0.97× | 0.83× | **1.10×** |
| ol-class | 0.88× | 1.02× | 0.99× | 0.97× |
| am-class | 1.28× | 0.59× | 1.23× | 1.09× |
| dy-class | 1.23× | 1.02× | **1.52×** | 1.11× |
| no-suffix | 0.90× | 0.98× | 1.03× | 1.13× |

---

## Interpretation

**H_new_H ANSWERED (WEAK EFFECT): Suffix types show mild positional preferences, but the effects are much weaker (E mostly 0.8-1.9×) than onset-level positional grammar (E=3-7×). The B 'dy' suffix is the strongest individual finding.**

Key findings:

1. **B 'dy' suffix LF-enriched (E=1.86×/N=60)**: Words ending in -dy are enriched at LF in B. The -dy suffix at LF includes words like dshedy, qokchdy, orchdy at line-first position. This is a B-specific positional preference for the -dy terminal marker at line openings. The overall dy-class (dy+y) is LF-enriched E=1.52×/N=107 at B-LF — the second-largest class-level positional effect.

2. **B 'shey' and 'r' suffixes LL-enriched (B shey E=2.17×/N=11; r E=1.85×/N=11)**: Small-N but notable. B words ending in -shey and -r appear disproportionately at LL. This extends B's LL suffix grammar (F1-F2 documented -am LL enrichment) to -shey and -r suffixes. N=11 makes these directional.

3. **A 'iin' suffix LL-enriched (E=2.23×/N=17)**: A standalone '-iin' suffix (distinct from 'aiin', 'ain') appears at LL at 2.23× rate. This is A-specific; B iin is LL-depleted (E=0.58×). Consistent with A's LL grammar selecting terminal markers including '-iin' endings.

4. **Suffix CLASS effects are weak**: The strongest class-level effect is B dy-class at LF (E=1.52×). All other classes are E=0.83-1.31×. For comparison, onset-level positional grammar operates at E=3-7×. Suffix selection is primarily governed by onset class and dialect (F436: edy-class vs aiin-class by onset), not by line position.

5. **A 'al' suffix LF-depleted (E=0.59×/N=274)**: Words ending in -al appear at LF at 60% of their expected rate in A. This is a depletion finding — -al-ending words (qokal, chal, shal, etc.) are not LF words in A. These are MID/LL-favored. N=274 makes this reliable.

6. **B 'l' suffix LF-depleted (E=0.40×/N=3 at LF)**: B words ending in '-l' (standalone l suffix) are strongly LF-depleted, but N=3. The l-suffix is primarily MID-distributed in B.

7. **No strong suffix class/position coupling in A**: A-dialect suffix classes show E=0.82-1.28× across all positions — essentially flat. A's positional grammar is primarily mediated by onset class, not suffix type.

---

## Self-Audit

**Target-awareness**: No target-aware elements.

**Feature-destroying implementation**: Suffix decomposition identical to exp_438/exp_443 (same SUFFIXES list). Position detection same as exp_443. No issues.

**Extrapolation**: N thresholds stated. Small-N findings (N=11 for shey/r) explicitly flagged as directional.

**Negative-result scope**: The weak effects are properly scoped: "suffix types show mild preferences" does not mean "no suffix positional grammar." The finding is that suffix-level grammar is WEAKER than onset-level grammar (E=1.5-2.2× vs onset E=3-7×).

**Control behavior**: N/A.

---

## Conclusion

H_new_H ANSWERED: Suffix types have mild positional preferences. **B 'dy' suffix LF E=1.86×(N=60)** is the strongest confirmed result. **B 'shey'(LL E=2.17×) and 'r'(LL E=1.85×)** are directional LL-enriched suffixes. **A 'iin' LL E=2.23×(N=17)** is A-specific. Suffix CLASS effects are weak (E=0.8-1.5×) vs onset-level grammar (E=3-7×). Suffix positional grammar is SECONDARY to onset positional grammar — the same onset-driven positional rules documented in F1-F433 operate at the word level, with suffix selection primarily determined by onset class (F436), not by position. **No new finding ID** (weak/directional results only; B 'dy' LF result extends F436 direction but doesn't warrant a separate finding).
