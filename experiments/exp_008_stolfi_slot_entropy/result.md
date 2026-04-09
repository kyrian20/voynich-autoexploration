# Experiment exp_008: Stolfi Slot Entropy Analysis

**Date:** 2026-04-09
**Hypothesis:** H006 — Crust stripping reveals higher h2 in the inner-slot (core/mantle) region, approaching natural-language h2 levels
**Status:** complete

## Hypothesis
H006: If the Stolfi slot grammar correctly models Voynich word structure, then the low h2 of the full corpus (2.341) is inflated downward by constrained outer-crust characters (d, l, r, s, n, y, g, q) and terminal suffixes (y, n, m, d). Stripping the crust should reveal the informational core of words, which under this model should have h2 approaching natural-language levels (~3.4-3.5 bits). Specifically: if the crust characters are "grammatical" affixes and the core contains the lexical content, the core h2 should be substantially higher than the full corpus h2.

## Method
Strip Voynich words in stages following a simplified Stolfi crust model:
1. Baseline (full corpus)
2. Strip terminal y/n/m (most constrained suffix characters)
3. Strip leading q (most constrained onset, nearly always followed by 'o')
4. Strip both ends (core region): leading chars in {d,l,r,s,n,y,g,q} and trailing chars in {y,n,m,d,l,r,s}

For each stage, compute H1 (unigram entropy of remaining characters) and H2 (bigram conditional entropy). Compare against natural language target (~3.4-3.5 bits). Also: characterize gallows character density in core region.

## Raw Output
```
Entropy Ladder:
Full corpus:                        H1=3.861  H2=2.341
Strip final y/n/m:                  H1=3.710  H2=2.462
Strip leading q:                    H1=3.783  H2=2.338
Core region (both ends stripped):   H1=3.312  H2=2.389

Core region h2: 2.389 bits (vs NL target ~3.4-3.5 bits)
Core region top chars: o(19.4%), e(15.6%), h(13.4%), a(10.9%), c(10.0%)
Gallows words: 51.9% of all words
Gallows context h2: 2.271 bits
```

## Result

**H006 is not supported.** Core region h2 = 2.389 bits — only 0.048 bits above full corpus h2 (2.341). The prediction required a substantial rise toward natural-language h2 (~3.4-3.5 bits); the actual rise is negligible.

**Stripping terminal y/n/m raises h2 to 2.462** — a modest +0.121 bit gain. This confirms that terminal y/n/m are constrained (consistent with prior findings), but removing them does not expose a higher-entropy core.

**Stripping leading q actually LOWERS h2 from 2.341 to 2.338** — a negligible change consistent with F006 (q contributes entropy by providing a unique onset category; removing it concentrates the remaining onset distribution).

**Core region characters are still dominated by o, e, h, a, c** — the same characters that dominate the full corpus. There is no distinctive "inner lexicon" with a different character distribution.

**Gallows context h2 = 2.271** — words containing gallows characters (51.9% of all words) have LOWER h2 than the full corpus average (2.341), not higher. This is the opposite of what the H006 model predicts: if gallows mark the high-information core, gallows-containing words should be more diverse, not less.

## Interpretation

**The Stolfi crust is not a low-information wrapper over a high-information core.** Removing the outer crust characters does not expose natural-language-like entropy. The information distribution is relatively flat across word positions — the core is not more informative than the crust.

**This is compatible with two very different models:**
1. The text has uniformly low per-character information throughout — consistent with a highly templated or generated text (e.g., glossolalia, constrained combinatorial system, or very narrow vocabulary).
2. The Stolfi slot grammar correctly identifies structural positions, but all positions are constrained (not just the outer crust). The low h2 is intrinsic to the text, not a result of an outer "grammatical" wrapper hiding a richer inner core.

**The finding does NOT rule out the Stolfi grammar as a structural description.** The slot grammar may be a correct characterization of word formation rules while still being consistent with uniformly low entropy — the grammar constrains ALL slots, not just the outer ones.

**Gallows words being LESS diverse than non-gallows words** (h2 = 2.271 vs 2.341) suggests gallows characters mark a particularly constrained word class, not a particularly informative one.

## Limitations
- The crust-stripping algorithm is a simplified approximation of the Stolfi grammar. A proper Stolfi parser would use the full slot grammar (crust → mantle → bench → core) rather than a character-class approach. Some non-crust characters may be stripped, and some crust characters may be missed.
- H2 computed on the concatenated stripped-word stream may create artificial bigrams across word boundaries (though word-internal bigrams dominate in a large corpus).
- Only two crust positions tested (leading, trailing). A position-conditional strip (Stolfi's actual grammar uses specific characters in specific slots, not just character class) might give different results.

## Follow-up Questions
- Does the positional entropy at pos 2-3 (the bench/core slots by position) actually differ from pos 0-1 (crust slots) in a way that the stripping analysis missed? The U-shaped positional entropy (F003) shows pos 3-4 have HIGHER entropy — this is consistent with a freer core — but stripping doesn't recover NL levels.
- The gallows h2 = 2.271 (lower than average) suggests gallows words are a constrained sub-vocabulary. What ARE these words? Are gallows words concentrated in specific sections or locus types?
- Since stripping doesn't work, the low h2 must be intrinsic. What combinatorial structures produce h2 ≈ 2.34 with the observed character distribution? Can a constrained grammar model reproduce this?
