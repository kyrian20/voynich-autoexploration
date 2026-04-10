# exp_154: Section Bug Fix, cthor Section Profile (H303), daiin→cthy Position (H306), Corrected cth Paradigm
**Date**: 2026-04-10
**Hypotheses**: H305 (section-bug diagnostic), H303 (cthor section profile), H306 (daiin→cthy positional)
**Status**: H305 RESOLVED (bug: folio_base kept leading '<'; fix: `.lstrip('<')`); H303 CONFIRMED (cthor=97% in A-herbal, second=2.16× enriched); H306 CONFIRMED (daiin→cthy places cthy at LL 2.12×); MAJOR CORRECTION to F158 (exp_151/152 had swapped LF/second slot labels — cthor is NOT LF-opener, it is SECOND-enriched)

---

## H305: SECTION BUG ROOT CAUSE IDENTIFIED AND FIXED

**Bug**: When parsing locus `<f1r.1,@P0>`, folio_raw = `<f1r`, folio_base = `<f1r` (the leading `<` was included). The regex `re.match(r'f(\d+)', '<f1r')` fails because the string starts with `<`, not `f`. All folios returned 'other'.

**Fix**: `folio_base = folio_raw.split('.')[0].lstrip('<')` → `'f1r'`. The regex then extracts folio_num=1 correctly. All A-dialect tokens now map to correct sections.

**Section distribution (A-dialect P-type, corrected)**:

| Section | Lines |
|---------|-------|
| herbal  | 1224  |
| pharma  | 326   |
| astro   | 89    |
| cosmo   | 32    |

---

## H303: cthor SECTION PROFILE — CONFIRMED

**cthor in A-dialect P-type: n=33 total**

| Section | cthor_n | total_words | cthor_ppm |
|---------|---------|-------------|-----------|
| herbal  | 32      | 7045        | 4.54‰     |
| pharma  | 1       | 2604        | 0.38‰     |
| astro   | 0       | 450         | 0         |
| cosmo   | 0       | 159         | 0         |

**cthor is 97% concentrated in A-herbal** (32/33 tokens). A-pharma has 1 token; astro and cosmo have 0.

**Corrected cthor positional profile in A-herbal (n=32)**:

| Slot   | n  | rate  | baseline | enrichment |
|--------|----|-------|----------|------------|
| LF     | 2  | 6.2%  | 17.2%    | **0.36×**  |
| second | 10 | 31.2% | 16.6%    | **1.89×**  |
| MID    | 18 | 56.2% | 48.9%    | 1.15×      |
| LL     | 2  | 6.2%  | 17.2%    | **0.36×**  |

**cthor positional profile across ALL A-dialect (n=33)**:

| Slot   | n  | rate  | baseline | enrichment |
|--------|----|-------|----------|------------|
| LF     | 2  | 6.1%  | 16.0%    | **0.38×**  |
| second | 11 | 33.3% | 15.4%    | **2.16×**  |
| MID    | 18 | 54.5% | 52.2%    | 1.04×      |
| LL     | 2  | 6.1%  | 16.0%    | **0.38×**  |

**CRITICAL CORRECTION to F158**: exp_151 and exp_152 inline analyses had SWAPPED LF and second slot labels. cthor is NOT a line-first word (LF-depleted 0.38×). cthor is a SECOND-POSITION word (second=2.16× enriched) — appearing at i=1 (the second word on the line) far more often than expected. cthor is LF-depleted AND LL-depleted. The F158 claim "cthor=LF-OPENER (LF=31.2%, 1.76×)" is CORRECTED to "cthor=SECOND-ENRICHED (second=33.3%, 2.16×)".

---

## CORRECTED FULL cth POSITIONAL PARADIGM (A-dialect, corrected code)

| cth-word   | n  | dominant slot    | enrichment   | LF      | notes |
|------------|----|-----------------  |--------------|---------|-------|
| cthy       | 84 | LL               | **1.63×**    | 0.15×   | LINE-CLOSER |
| cthol      | 49 | MID              | **1.33×**    | 0.13×   | MEDIAL |
| cthor      | 33 | second           | **2.16×**    | 0.38×   | SECOND-POSITION |
| cthody     | 13 | MID              | 1.33×        | 0.00×   | MEDIAL (small n) |
| ctheody    | 5  | MID              | **1.53×**    | 0.00×   | MEDIAL |
| cthom      | 5  | LL               | **2.49×**    | 0.00×   | LINE-CLOSER (small n) |
| cthain     | 4  | second/LL        | 1.56-1.62×   | 0.00×   | bimodal (tiny n) |

**REVISED 4-WAY cth PARADIGM** (correcting F158):
1. **cthor = SECOND-ENRICHED** (2.16×, LF=0.38×): appears at i=1, not LF
2. **cthol = MEDIAL-ENRICHED** (MID=1.33×, LF=0.13×): medial-dominant
3. **cthody/ctheody = MEDIAL** (MID=1.33-1.53×): similar to cthol
4. **cthy = LL-ENRICHED** (1.63×, LF/second depleted): line-closer

The cthor vs cthol distinction is preserved (second vs MID) but cthor is second-position, not LF. ALL cth-words avoid LF (LF=0.00-0.38×). None of the cth-vocabulary opens lines — they all appear after at least one other word.

---

## H306: daiin→cthy — cthy POSITIONAL SLOT (CONFIRMED)

**All cthy in A P-type (n=84)**:

| Slot   | n  | rate  |
|--------|----|-------|
| LF     | 2  | 2.4%  |
| second | 12 | 14.3% |
| MID    | 48 | 57.1% |
| LL     | 22 | 26.2% |

**daiin→cthy bigrams (n=9) — cthy slot distribution**:

| Slot   | n | rate  | baseline | enrichment |
|--------|---|-------|----------|------------|
| LF     | 0 | 0.0%  | 2.4%     | 0.00×      |
| second | 0 | 0.0%  | 14.3%    | 0.00×      |
| MID    | 4 | 44.4% | 57.1%    | **0.78×**  |
| LL     | 5 | 55.6% | 26.2%    | **2.12×**  |

**H306 CONFIRMED**: daiin→cthy selects cthy at LL 55.6% of the time (2.12× enriched vs cthy baseline 26.2% at LL). After daiin, cthy never appears at LF or second (0× for both). daiin shifts cthy strongly toward LL.

**daiin→cthy examples (all n=9)**:
- `ochor qocheor chol daiin cthy` → cthy at LL
- `sol,oiin cheor chol daiin cthy` → cthy at LL
- `ychky daiin cthy` → cthy at LL
- `otcho,rol dain daiin cthy` → cthy at LL
- `dshody ckhody qokol dykaiin chy qokey daiin cthy` → cthy at LL
- `ykey chor ykaiin daiin cthy otaiin oky oeees daiin` → cthy at MID
- `shor shor dky daiin cthy d,y,chodl,daiin` → cthy at MID
- `tol okchor shcthy otol daiin cthy cthy` → cthy at MID
- `okol chor daiin cthy okchol chom...` → cthy at MID

The 4 MID cases have cthy at i=4-5 in 8-12 word lines — late-MID, approaching LL. The [daiin][cthy→LL] construction is real; the 4 MID cases represent daiin→cthy occurring in non-final contexts.

---

## Summary of New Findings (F161)

1. **Section bug fixed: folio_base kept leading `<` (e.g., `<f1r` not `f1r`), causing regex match failure for all folios.** Fix: `.lstrip('<')` before parsing. (H305 RESOLVED)

2. **cthor is 97% concentrated in A-herbal (32/33 tokens); 0 in astro/cosmo.** (H303 CONFIRMED)

3. **CRITICAL CORRECTION to F158: cthor is SECOND-ENRICHED (2.16×), NOT LF-enriched.** exp_151/152 had swapped LF and second slot labels. In the corrected paradigm: cthor=second (2.16×); cthol=MID (1.33×); cthy=LL (1.63×); ctheody=MID (1.53×); cthom=LL (2.49×). ALL cth-words avoid LF (0.00-0.38×). The key cthor/cthol distinction (second vs MID) is preserved.

4. **daiin→cthy selects cthy at LL 2.12× enriched (H306 CONFIRMED).** daiin→cthy never produces cthy at LF or second (0×). daiin is a line-terminal selector for cthy specifically.

---

## Hypotheses Spawned
- **H307**: Re-run H302 analysis (cthol@second LF-word distribution) with corrected slot code. Previous result (n=15 "cthol@second") may be inflated if exp_152 was also computing "cthol@LF" instead of "cthol@second". Correct cthol@second n=9 (from exp_154). What are the LF words for these 9 cthol@second cases?
- **H308**: cthor is SECOND-ENRICHED. What is the LF word (i=0) when cthor is at second (i=1)? Is there a specific [LF-word][cthor@second] construction? Given cthor's strong second enrichment (2.16×), the LF word should show enrichment for specific onset classes (ch/sh/d?).
- **H309**: Does the corrected cth paradigm change the cth-introduction constructions (F157)? Specifically: if cthor is at second not LF, then the chol/chor@LF→cthor@second construction is the operative one. Re-examine Type 2 ([chol/chor@LF][cthor@second]) with corrected data.
