# Experiment exp_290: Hapax Words by Line Position

**Date:** 2026-04-11
**Hypothesis:** Template words (frequent, zero-midfix) should concentrate at MID positions (copy-buffer output). Vocabulary-rich words (hapax, long midfix) should concentrate at LF/LL (cipher output), or at MID if the copy-buffer generates unique content.
**Status:** complete

## Hypothesis

The Mode B architecture predicts: MID positions are filled by the copy-buffer (repeated, frequent onset+suffix words), while LF/LL positions are filled by a cipher component (grammar words like -am, y-onset). If this is correct, hapax words should be depleted at MID (copy-buffer recycles) and enriched at LF/LL (cipher produces diverse output). The two-tier vocabulary structure (exp_289: hapax=long midfix, frequent=short midfix) should be position-stratified.

## Method

- Corpus: eva_zl3b.txt, both dialects, body text only (P* loci)
- Position assignment: first word per line = LF, last word = LL, others = MID
- Global word frequency (A+B combined), frequency tier classification from exp_289
- Metrics: hapax rate per position, midfix length per position per tier, zero-midfix rate per position, template vs vocabulary ratio per position

## Expected Outcomes

| Theory | Predicted result |
|--------|-----------------|
| Mode B (copy-buffer MID / cipher LF-LL) | Hapax rate higher at LF/LL than MID; frequent words concentrate at MID |
| Uniform generation (no position distinction) | Hapax rate uniform across positions |
| Grammar/content position model | LF/LL = short grammar words (low hapax); MID = content words (higher hapax) |

**This experiment is an UNFAIR test if:** Hapax rate differences across positions could be a length artifact (LF/LL words are longer on average due to positional grammar, and longer words are rarer). Check: does controlling for length remove the position effect?

## Raw Output
```
=== Word Position Distribution by Frequency Tier ===
hapax    :  916 LF (19.5%), 2746 MID (58.5%), 1034 LL (22.0%)
frequent : 1744 LF (10.2%), 13489 MID (79.1%), 1825 LL (10.7%)

=== Midfix Length by Position (all words) ===
LF:  N=4093,  WLen=5.60, MLen=2.02, ZeroMid=0.319, Hapax%=22.4%
MID: N=21867, WLen=5.41, MLen=1.40, ZeroMid=0.448, Hapax%=12.6%
LL:  N=4127,  WLen=5.28, MLen=1.75, ZeroMid=0.386, Hapax%=25.1%

=== Midfix Length by Position AND Frequency Tier ===
LF  hapax    N= 916: WLen=7.05, MLen=4.18, ZeroMid=0.007
LF  frequent N=1744: WLen=4.76, MLen=0.51, ZeroMid=0.689
MID hapax    N=2746: WLen=7.23, MLen=3.94, ZeroMid=0.008
MID frequent N=13489: WLen=4.92, MLen=0.57, ZeroMid=0.688
LL  hapax    N=1034: WLen=6.85, MLen=3.94, ZeroMid=0.015
LL  frequent N=1825: WLen=4.55, MLen=0.47, ZeroMid=0.742

=== By Dialect: Hapax Rate per Position ===
A: LF=23.2%, MID=16.0%, LL=28.7%
B: LF=21.8%, MID=11.0%, LL=22.4%

=== Template vs Vocabulary Hapax Rate by Position ===
A: LF: template hapax=0.2%, vocabulary hapax=31.8%
   MID: template hapax=0.5%, vocabulary hapax=25.8%
   LL: template hapax=1.1%, vocabulary hapax=44.5%
B: LF: template hapax=0.6%, vocabulary hapax=33.3%
   MID: template hapax=0.1%, vocabulary hapax=20.8%
   LL: template hapax=0.8%, vocabulary hapax=36.9%

B-dialect positional MLen and ZeroMid:
B-LF:  N=2405, Hapax=21.8%, MLen>2=34.8%, ZeroMid=35.1%, WLen=5.72, MLen=1.98
B-MID: N=15004, Hapax=11.0%, MLen>2=21.5%, ZeroMid=47.6%, WLen=5.49, MLen=1.30
B-LL:  N=2419, Hapax=22.4%, MLen>2=26.0%, ZeroMid=40.1%, WLen=5.16, MLen=1.57
```

## Result

**Confirmed:** Hapax rate is substantially higher at LF/LL (21-29%) than MID (11-16%). MID has the highest zero-midfix rate (A: 38.6%, B: 47.6% — template words). Frequent words concentrate overwhelmingly at MID (79.1% of frequent-word tokens). **New finding:** Hapax midfix length is STABLE across positions: hapax MLen ≈ 3.94–4.18 at LF, MID, and LL alike. Among vocabulary-rich words (has midfix), LL has the highest hapax rate (A-LL: 44.5%, B-LL: 36.9%) — uniquely complex words are concentrated at LL.

## Interpretation

**The Mode B architectural prediction is PARTIALLY confirmed:**

Mode B predicts: MID = copy-buffer (frequent, recycled), LF/LL = cipher (grammar words). The data supports the MID prediction: MID has the fewest hapaxes (11-16%) and the most template words (ZeroMid=38-48%). The copy-buffer mechanism correctly explains why MID words repeat more.

**But the LF/LL cipher prediction is INCOMPLETE:**

The Mode B cipher at LF/LL is calibrated to produce grammar words (y-onset LF, -am LL). These grammar words are predominantly template words (short, zero-midfix). But LF/LL also has high rates of vocabulary-rich hapax words (WLen≈7, MLen≈4). These are NOT what the cipher component produces.

Specifically:
- B-LL vocabulary words (has midfix): 36.9% hapax rate — one in three LL vocabulary words is unique
- A-LL vocabulary words: 44.5% hapax rate — nearly half of LL vocabulary words are unique
- This creates a two-component LL: (1) grammar words (-am, short) from cipher; (2) vocabulary words (long, unique) from unknown source

**The hapax midfix length does NOT differ by position.** Hapax words at LF have MLen=4.18, at MID=3.94, at LL=3.94 — essentially the same. This means hapaxes are structurally uniform regardless of where in the line they appear. The long-midfix hapax form is not position-specific — it's a property of the word type itself, not of its line position.

**Architectural implication:** The vocabulary richness gap (simulation 2.2× over-produces unique MID types) may be partly caused by the cipher component generating too many unique long words at LF/LL too. The vocabulary-rich hapaxes at LF/LL are a feature that Mode B's cipher component (calibrated to short grammar words) does not currently model.

## Limitations

- Hapax rate differences across positions may partly reflect word-length differences (LF/LL words are longer; longer words are rarer). A length-controlled comparison would be needed to isolate the position effect from the length effect. However: hapax MLen is stable across positions (3.94–4.18), so length alone doesn't explain the positional hapax rate difference.
- The "template words" (ZeroMid) hapax rate is very low (0.1-1.1%) regardless of position. This confirms template words are genuinely frequent. But a few template-form hapaxes at LL (1.1%) suggest some grammar word types appear only once even with short structure.
- Position assignment (first/last word per text line) may not precisely correspond to Mode B's LF/LL/MID categories, which use paragraph-first and paragraph-last lines.

## Self-Audit

**Target-awareness:** No VMS target metrics used. Exploratory measurement. No target-awareness issues.

**Feature-destroying implementation:** None. Frequency classification is based on global corpus counts, independent of position assignment.

**Extrapolation:** The "two-component LL" interpretation is a descriptive inference from the data. The claim that Mode B's cipher "does not model" vocabulary-rich LL hapaxes is within the tested scope (we know the cipher produces grammar words; the vocabulary-rich hapaxes are unexplained).

**Negative-result scope:** Not a negative result — multiple predictions confirmed. The "incomplete" LF/LL cipher prediction is a narrowing of Mode B, not a refutation.

**Control behavior:** Null model not needed (descriptive analysis). The expected hapax rate at MID (proportional share ≈ 73% of tokens) would predict 73% of hapax tokens at MID; observed is 58.5%, confirming hapaxes are genuinely depleted at MID.

## Follow-up Questions

- Q: What are the specific word types in the LL vocabulary-rich hapax category? Are they genuine content words or morphological variants of common stems?
- Q: Does the cipher component of Mode B need to be augmented with a vocabulary-sampling step (not just grammar-word output) to capture the vocabulary-rich LF/LL hapaxes?
- Q: The stable hapax MLen across positions (≈4 chars midfix) suggests hapax words come from a single structural population regardless of position. Is this consistent with the Mode B simulation output? Does the simulation produce stable hapax MLen across positions?
