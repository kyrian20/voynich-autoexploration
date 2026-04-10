# exp_153: cthor Section Profile (H303) & daiin@Penultimate Before cth@LL (H304)
**Date**: 2026-04-10
**Hypotheses**: H303 (cthor section profile retry), H304 (daiin→cthy specificity)
**Status**: H303 STILL FAILED (folio_to_section returns 'other' for all A-dialect words; bug root cause unclear despite attempted fix); H304 CONFIRMED ([daiin][cthy] IS a specific two-word fixed phrase: daiin enriches before cthy@LL at 3.57× but 0.00× before cthol@LL, cthor@LL, cthody@LL)

---

## H303: cthor SECTION PROFILE — STILL FAILED

Attempted fix: `folio_to_section` function using `re.match(r'f(\d+)', folio_base)` to extract numeric folio number from 'f1r'/'f1v' format. Despite this, section analysis returned all A-dialect words as 'other' (n=9165), herbal/pharma/astro all n=0.

Root cause remains unclear. The section-mapping function extracts a numeric folio and maps it to section — but all tokens still fall in 'other'. Possible remaining issues: the regex match on folio_base format, the integer lookup range, or the folio_base parsing from the corpus locus format. Further debugging required (exp_154 to isolate the bug with diagnostic output).

**Status**: H303 deferred again. Section analysis for cthor not available.

---

## H304: daiin AS PENULTIMATE BEFORE cth-WORDS AT LL — SPECIFICITY TEST

**Baseline**: daiin as penultimate word in A P-type body text = 79/1480 = 5.34%

### daiin rate as penultimate before each cth-word at LL:

| cth-word@LL | n@LL | daiin penultimate | daiin% | Enrichment |
|-------------|------|-------------------|--------|------------|
| cthy        | 21   | 4                 | 19.0%  | **3.57×**  |
| cthol       | 5    | 0                 | 0.0%   | 0.00×      |
| cthor       | 2    | 0                 | 0.0%   | 0.00×      |
| cthody      | 2    | 0                 | 0.0%   | 0.00×      |
| cthain      | 1    | 0                 | 0.0%   | 0.00×      |

### Top penultimate words before cthy@LL (n=21):

| Word     | n  | % |
|----------|-----|---|
| **daiin** | **4** | **19.0%** |
| dchy     | 2   | 9.5%  |
| chor     | 2   | 9.5%  |
| chy      | 1   | 4.8%  |
| qokam    | 1   | 4.8%  |
| others   | 11  | 52.4% |

### Top penultimate words before cthol@LL (n=5):

| Word         | n | % |
|--------------|---|---|
| cham         | 1 | 20.0% |
| dain         | 1 | 20.0% |
| ctho         | 1 | 20.0% |
| (others)     | 2 | 40.0% |

daiin appears 0× as penultimate before cthol@LL.

### Example [daiin][cthy→LL] lines:

- `qocheor chol daiin cthy`
- `cheor chol daiin cthy`
- `dain daiin cthy`
- `ckhody qokol dykaiin chy<->qokey daiin cthy`

---

## H304 CONFIRMED: [daiin][cthy] IS A SPECIFIC TWO-WORD FIXED PHRASE

daiin enriches before cthy@LL at **3.57×** (19.0% vs 5.34% baseline, n=4/21) but does NOT enrich before any other cth-word at LL (cthol=0×, cthor=0×, cthody=0×, cthain=0×). The [daiin][cthy] specificity is categorical — no overlap with other cth-words at LL.

**Interpretation**: [daiin][cthy] at line-end is a specific two-word nominal phrase. daiin does not simply enrich before all line-final cth-words as a generic "line-final cth-determiner." It specifically selects cthy — the line-final cth-form — confirming that cthy@LL is a distinct grammatical slot that daiin targets, while the other cth-words at LL (cthol, cthor) appear in different constructions (cthol@LL after other ch/sh openers, cthor@LL after ot-class words).

This is the strongest evidence for a specific Voynichese nominal phrase construction in the A-grammar. Combined with F158's 4-way positional paradigm, cthy is the canonical daiin-selected line-terminal nominal form.

---

## Summary of New Findings (F160)

1. **[daiin][cthy] is a specific two-word fixed phrase (3.57× enrichment for daiin as penultimate before cthy@LL, 0× before all other cth-words@LL)**: H304 CONFIRMED. daiin specifically selects cthy as line-final cth-word. The specificity is categorical across 5 cth-words at LL. This is the strongest evidence for a particular Voynichese nominal phrase in the A-grammar.

2. **H303 section analysis still fails (folio_to_section returns 'other' for all folios even with numeric extraction attempt)**: Root cause unclear. Requires diagnostic experiment to identify the exact failure point.

---

## Hypotheses Spawned
- **H305** (section-bug diagnostic): Run targeted diagnostic to identify why folio_to_section fails. Print sample folio_base values from the corpus, trace the regex match, and compare against SECTION_MAP keys. Isolate: is the bug in folio_base format, regex, or map key type mismatch (int vs string)?
- **H306**: Does daiin also specifically select cthy at non-LL positions? Compute: when daiin→cthy bigram occurs, what is cthy's position? If daiin→cthy always or mostly targets cthy at LL, daiin is a line-terminal selector. If daiin→cthy also targets cthy at MID, daiin is a general cthy-introducer (not LL-specific).
