# exp_152: cthor Section Profile & cthol@Second Analysis
**Date**: 2026-04-10
**Hypotheses**: H301 (cthor section-specificity), H302 (cthol@second drivers)
**Status**: H301 METHODOLOGICAL FAILURE (section-map key mismatch: folio_base='f1r' vs key='f1'; cthor shows n=0 in A-herbal/pharma — spurious); H302 PARTIALLY CONFIRMED (cthol@second is NOT dominated by chol/chor openers; ch-onset openers=40%, d=20%, sh=13%; daiin→cthol is 20%); BONUS: daiin is the most common penultimate word before cthy-at-LL (4/21=19%), directly confirming [daiin][cthy→LL] line-closing construction.

---

## H301: cthor SECTION ANALYSIS — METHODOLOGICAL FAILURE

The section mapping `SECTION_MAP['f1'] = 'herbal'` failed because folio_base values in the corpus are 'f1r', 'f1v', etc. (recto/verso suffix included). The key 'f1r' ≠ 'f1' → SECTION_MAP returns 'other'. All A-herbal lines were classified as section 'other', giving cthor n=0 in A-herbal and A-pharma.

**Valid data from A-all** (n=32 cthor tokens, all A-dialect P-type):
- LF=31.2% (1.76×), second=15.6% (0.97×), MID=46.9% (0.98×), LL=6.2% (0.35×)
- Confirms F158's cthor positional profile; no section breakdown available from this run.

**cthor at LF → second word** (n=10):
- chol=2, chpcheos=1, otal=1, chor=1, y+kaiiin=1, daiin=1, okaiin=1, oty=1, okol=1
- No dominant second word (diverse: ch-class, ot-class, ok-class, d-class)

Section analysis for H301 requires fixing the folio_base → section key to strip r/v suffix. Deferred.

---

## H302: cthol AT SECOND — LF WORD DISTRIBUTION

**cthol at second total: 15 cases**

LF word when cthol is at second:

| LF word    | n  | % |
|------------ |-----|---|
| chol        | 3   | 20.0% |
| daiin       | 3   | 20.0% |
| chor        | 2   | 13.3% |
| kchor       | 1   | 6.7%  |
| otchor      | 1   | 6.7%  |
| shor        | 1   | 6.7%  |
| she         | 1   | 6.7%  |
| choror      | 1   | 6.7%  |
| chees       | 1   | 6.7%  |
| qotshy      | 1   | 6.7%  |

LF onset distribution (when cthol is at second):

| Onset | n  | % |
|-------|-----|---|
| ch    | 6   | 40.0% |
| d     | 3   | 20.0% |
| sh    | 2   | 13.3% |
| k     | 1   | 6.7%  |
| ot    | 1   | 6.7%  |
| ch_e  | 1   | 6.7%  |
| qot   | 1   | 6.7%  |

**H302 PARTIALLY CONFIRMED**: cthol at second is NOT dominated by the Type 2 [chol/chor][cthol] construction alone. ch-onset openers at LF account for 40% (6/15), d-onset (daiin) for 20%, sh-onset for 13%. Specific chol/chor (the Type 2 participants) account for 5/15 (33%). The remaining 10/15 cases come from diverse LF words (kchor, otchor, shor, she, daiin, choror, chees, qotshy).

**Conclusion**: cthol's second-position enrichment (1.94×) reflects BOTH:
1. The Type 2 [chol/chor at LF][cthol at second] construction (~33% of cthol@second)
2. A more general tendency for cthol to appear at second after ANY ch/sh line-opener (~53% from ch+sh combined)

cthol's second-position affinity is driven by ch/sh-opening lines generally, not exclusively by the specific [chol/chor][cthol] pair.

---

## BONUS: daiin IS THE MOST COMMON PENULTIMATE WORD BEFORE cthy AT LL

**cthy at LL: n=21 cases**

Penultimate word (word before cthy at LL):

| Word     | n  | % |
|----------|-----|---|
| **daiin** | **4** | **19.0%** |
| dchy     | 2   | 9.5%  |
| chor     | 2   | 9.5%  |
| chy      | 1   | 4.8%  |
| qokam    | 1   | 4.8%  |
| others   | 11  | 52.4% |

**daiin is the dominant penultimate word before line-final cthy (4/21=19%)**, directly confirming the [daiin→cthy→LL] sub-construction from exp_151. daiin's enrichment as cthy's preceder: baseline daiin rate ~3.8% of words → 19% of penultimate positions before cthy-at-LL = enrichment ~5×. The daiin→cthy line-closing construction is real and substantial.

LF word when cthy is at LL: highly diverse (chol=2/21, then all singletons). No single line-opening word is concentrated in cthy-closing lines.

---

## Summary of New Findings (F159)

1. **cthol@second driven by ch/sh line-openers broadly (40%+13%), not exclusively Type 2 [chol/chor][cthol]**: ch-onset LF words account for 40% of cthol@second; specific chol/chor account for ~33%. cthol's second-position affinity is a general feature of ch-opening lines, not restricted to chol/chor.

2. **daiin→cthy→LL is the dominant specific cthy-closing construction (4/21=~5× enrichment of penultimate daiin)**: daiin is penultimate before cthy-at-LL 19% of the time (4/21 cases), vs ~3.8% baseline. This is the clearest evidence for the [daiin][cthy] line-closing nominal phrase as a specific A-grammar construction.

3. **H301 failed due to section-mapping bug** (folio_base 'f1r' ≠ section_map key 'f1'). Deferred.

---

## Hypotheses Spawned
- **H303** (H301 retry with bug fix): Compute cthor positional profile by section (herbal/pharma/astro) in A-dialect using correct folio_num extraction. Expected: cthor is concentrated in herbal-A (F147 established cthor is A-herbal specific); cthor's LF=1.76× enrichment may be herbal-specific.
- **H304**: Is [daiin][cthy] a two-word fixed phrase (appearing only in this exact form), or does daiin precede other cth-words before them at LL with similar enrichment? Compute penultimate word for cthol-at-LL and cthor-at-LL — is daiin equally enriched before all cth-words at LL, or specifically before cthy?
