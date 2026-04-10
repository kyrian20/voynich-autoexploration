# exp_156: chol/chor Positional Profiles, chol→cth Bigram Positions (H310), chol@LF Analysis (H311), Bigram Verification (H312)
**Date**: 2026-04-10
**Hypotheses**: H310 (chol→cth bigram positional context), H311 (chol@LF second-word), H312 (verified bigram enrichments)
**Status**: H310 CONFIRMED (chol→cth from chol@second/MID only, 0 from chol@LF); H311 CONFIRMED (chol@LF second=ch-onset 54.5%); H312 CONFIRMED (chol→cth=2.35×, chor→cth=2.22×)

---

## chol AND chor POSITIONAL PROFILES IN A-DIALECT

| Word | n   | LF enrichment | second enrichment | MID enrichment | LL enrichment |
|------|-----|---------------|-------------------|----------------|---------------|
| chol | 228 | **0.30×**     | **1.87×**         | 1.25×          | **0.03×**     |
| chor | 147 | 0.64×         | **2.33×**         | 0.98×          | **0.13×**     |

**chol is SECOND-enriched (1.87×), LF-depleted (0.30×)**. chol is NOT a line-opener. It appears after some other word, predominantly at second (29%) or MID (65%). LL is essentially absent (n=1, 0.03×).

**chor is SECOND-enriched (2.33×), MID-neutral (0.98×)**. chor also avoids LF (0.64×) and LL (0.13×). chor is predominantly a second-position word.

This directly contradicts F157's claim that "chol at LF=50%" when preceding cth-words. F157's positional analysis had swapped LF/second labels (same bug as exp_150/151/152 analyses).

---

## H310: chol→cth BIGRAMS — POSITIONAL CONTEXT (CONFIRMED)

**chol→cth bigrams: n=20**

| chol position | n  | % |
|---------------|-----|---|
| second (i=1)  | 11  | 55.0% |
| MID (i>1)     | 9   | 45.0% |
| LF (i=0)      | 0   | 0.0%  |
| LL (i=n-1)    | 0   | 0.0%  |

**cth-words introduced by chol→cth bigrams**:
- chol→cthol: 6 cases (4 at chol@second, 2 at chol@MID)
- chol→cthy: 5 cases (2 at chol@second, 3 at chol@MID)
- chol→cthor: 2 cases (1 second, 1 MID)
- chol→cthaiin: 2 cases
- chol→other-cth: 5 cases

**chol→cth bigrams occur exclusively when chol is at second or MID positions**. The corrected "chol→cth construction" is a within-line medial sequence: [some-LF-word][chol@second][cth@MID/LL] or [...][chol@MID][cth@subsequent].

---

## chor→cth BIGRAMS — POSITIONAL CONTEXT

**chor→cth bigrams: n=12**

| chor position | n  | % |
|---------------|-----|---|
| second (i=1)  | 7   | 58.3% |
| MID (i>1)     | 5   | 41.7% |
| LF (i=0)      | 0   | 0.0%  |

**cth-words introduced by chor→cth bigrams**:
- chor→cthom: 3 cases (2 second, 1 MID)
- chor→cthol: 2 cases (1 second, 1 MID)
- chor→cthy: 2 cases (1 second, 1 MID)
- chor→cthor: 2 cases (both at MID)
- chor→cthaiin: 1 case, chor→cthoiin: 1 case, chor→ctheey: 1 case

---

## H311: chol@LF — SECOND-POSITION WORDS (CONFIRMED)

**chol@LF lines: n=11**

Second-position words after chol@LF:

| Word    | n | % |
|---------|---|---|
| chol    | 2 | 18.2% |
| chor    | 1 | 9.1% |
| chok    | 1 | 9.1% |
| chcthal | 1 | 9.1% |
| cheol   | 1 | 9.1% |
| dchy    | 1 | 9.1% |
| or      | 1 | 9.1% |
| shy     | 1 | 9.1% |
| daiiin  | 1 | 9.1% |
| shotol  | 1 | 9.1% |

ch-onset total at second after chol@LF: 6/11 = **54.5%** (baseline ch=6.9% → 7.9× enriched!). chol at LF consistently leads into another ch-word at second. The chol@LF construction is: **[chol@LF][ch-word@second]** — a ch-reduplication opening. chol self-succession: 2/11 cases (18.2%).

**Full chol@LF lines**:
- `chol chok choty chotey` → chok at second (ch-onset)
- `chol dchy qokar chl aiin chean char chaiin` → dchy at second (d-onset)
- `chol chol dar otchar etaiin cthol dar` → chol at second (ch-onset; cthol at i=5 MID)
- `chol or chy qodam okor chor okchom` → or at second (other)
- `chol chcthal okshal chykald` → chcthal at second (ch-onset)
- `chol shy keol chol chy shol chy daiin chey dam` → shy at second (sh-onset)
- `chol daiiin chees chos dan` → daiiin at second (d-onset)
- `chol chol kor shey odaiin qotchy taiin s she otey sy` → chol at second (ch-onset)
- `chol shotol oteol okee[a:y] s chor d aiin,d` → shotol at second (sh-onset)
- `chol chor ches chkalchy chokeeoky chokoran` → chor at second (ch-onset)
- `chol cheol cho chckheody otolchey` → cheol at second (ch_e-onset)

**H311 CONFIRMED**: chol@LF is a ch-opening pattern. After chol@LF, the second word is overwhelmingly a ch-class word (54.5%, ~8× enriched). Note: chol@LF lines that also have cthol later (e.g., "chol chol dar otchar etaiin cthol dar") have cthol at MID (position 5), not at second — consistent with H310's finding that chol@LF never has cth at second.

---

## H312: VERIFIED chol/chor→cth BIGRAM ENRICHMENTS

**Baseline cth rate in A (corrected corpus)**: 3.77%

| Bigram   | count | total bigrams | rate  | enrichment |
|----------|-------|---------------|-------|------------|
| chol→cth | 20    | 226           | 8.85% | **2.35×**  |
| chor→cth | 12    | 143           | 8.39% | **2.22×**  |

**H312 CONFIRMED**: chol→cth=2.35× and chor→cth=2.22× are genuine bigram enrichments (correctly computed from P-type body text). These are real syntactic relationships — chol and chor consistently introduce cth-words at higher than baseline rate, but from second and MID positions (not LF).

---

## Summary of New Findings (F163)

1. **chol is SECOND-enriched (1.87×) and LF-depleted (0.30×)**: NOT a line-opener. Same for chor (second=2.33×, LF=0.64×). F157's "chol at LF=50%" was an artifact of the swapped-slot bug.

2. **chol→cth bigrams occur exclusively at chol@second (55%) or chol@MID (45%); 0 from chol@LF**: The corrected chol→cth construction is [LF-word][chol@second][cth@MID/LL] — chol is the second word introducing a subsequent cth-word. The dominant cth-words after chol: cthol (6), cthy (5), cthor (2).

3. **chol@LF → ch-word@second (54.5%, ~8× enriched)**: When chol IS at LF (n=11), it consistently leads into another ch-class word at second. [chol@LF][ch@second] is the chol-opening construction. None of these lines have cth at second.

4. **Verified bigram enrichments: chol→cth=2.35×, chor→cth=2.22× (corrected corpus)**: Real enrichments from within-line (non-LF) positions.

---

## Hypotheses Spawned
- **H313**: What is the LF word when chol is at second? (In the corrected [LF][chol@second][cth@MID] construction, what opens the line?) Is there a specific LF word class that opens lines with chol@second?
- **H314**: Verify daiin→cth bigram positional context with corrected code. daiin→cth was described in F157 as "daiin at MID(61%) → cth at MID/LL" — but exp_150 may have had slot errors. Re-run with corrected code: where is daiin when it precedes cth-words?
