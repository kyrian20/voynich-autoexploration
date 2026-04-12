# exp_298: Text-Section Paradigm Expansion — Register Mixing vs Genuine Lexical Diversity (H502)
**Date:** 2026-04-11
**Hypothesis:** H502 — The text section's larger paradigm (2.6× bio for qok) is due to register mixing across folios, not genuine within-folio lexical diversity
**Script:** script.py
**Data:** data/transcriptions/eva_zl3b.txt

---

## Result: H502 REFUTED

Text sub-sections (f103-109 early, f110-116 late) individually require 32-38 qok types for 90% coverage — essentially the same as the combined text section (39 types). Bio sub-sections each require 14-15 types. The paradigm expansion is WITHIN-FOLIO, confirmed by per-folio TTR: text qok TTR = 0.350 vs bio = 0.218.

---

## Key Findings

### qok-onset: text vs bio sub-section paradigm sizes

| Section        | N tokens | 90%-coverage set | % of local types |
|----------------|----------|------------------|-----------------|
| bio early      | 559      | **14 types**     | 26.9%           |
| bio late       | 506      | **15 types**     | 26.8%           |
| text early     | 604      | 32 types         | 36.4%           |
| text late      | 480      | 38 types         | 48.7%           |

- Bio intra-section Jaccard: **0.611** (highly consistent between early/late)
- Text intra-section Jaccard: **0.522** (also consistent, but larger sets)

Bio sub-sections need ~14-15 types; text sub-sections need ~32-38 types. If mixing across folios explained the expansion, each sub-section should be bio-sized. They are not.

### Per-folio TTR confirms within-folio diversity

| Onset | Mean text TTR | Mean bio TTR | Ratio |
|-------|---------------|--------------|-------|
| qok   | 0.350         | 0.218        | 1.6×  |
| ok    | 0.501         | 0.473        | 1.06× |
| ot    | 0.488         | 0.507        | 0.96× |
| ch    | 0.500         | 0.422        | 1.18× |
| sh    | 0.588         | 0.346        | 1.70× |

- qok and sh show the largest within-folio diversity gap (1.6-1.7×)
- ok and ot show near-identical TTR between sections — their paradigm expansion in text (exp_297) is due to larger section size (more accumulation), not higher per-folio diversity

### Interpretation by onset class

**qok/sh (genuine text diversity):** Higher per-folio TTR means individual text folios use more distinct word types than bio folios. This is genuine lexical diversity, not register mixing.

**ok/ot (size-driven expansion):** Per-folio TTR is similar between text and bio (~0.49-0.51). The larger paradigm sets in text (exp_297) reflect the larger section token count accumulating more rare types — Zipfian accumulation, not genuine diversity.

**ch (intermediate):** Text TTR 1.18× higher — modest but real within-folio diversity.

---

## Structural Conclusion

The text section (f103-f116) is genuinely more lexically diverse per folio than bio for qok/sh onset classes. This is not an artifact of mixing different registers across folios. The most likely explanation:

> The text section (recipes, zodiac, diverse content) uses a broader vocabulary WITHIN each folio, consistent with a more complex or varied underlying text content. Bio section pages repeat a smaller, more formulaic vocabulary within each folio.

This reinforces the finding that bio section = tightest closed paradigm in the manuscript. The bio paradigm (15 qok types for 90% coverage) is the most concentrated word-class vocabulary observed anywhere in B-dialect. Text sections use the same word-class structure but with higher within-folio entropy.

---

## Self-Audit

1. **Validity**: Sub-section split is clean (two halves by folio number). Per-folio TTR is computed with N≥5 filter. ✓
2. **Surprising**: ok and ot show no TTR difference between text and bio — their larger paradigm sets in exp_297 are Zipfian accumulation artifacts of section size, not genuine diversity. qok and sh are genuinely more diverse in text.
3. **Battery impact**: None — descriptive characterization.
4. **Committed claims**: None affected. ✓
5. **New hypotheses**: None needed — H502 resolved cleanly. The within-folio diversity explanation is sufficient for the text section's expanded paradigm.

---

## Finding

See F300 in findings.md.
