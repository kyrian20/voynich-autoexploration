# Experiment exp_002: Positional Entropy Analysis

**Date:** 2026-04-09
**Hypothesis:** H001 — h2 conditioned on position within word; also covers H002 (length-conditioned entropy) and H010/H011 (q-initial removal, positional bias index)
**Status:** complete

## Hypothesis
If Voynichese has a rigid prefix-midfix-suffix template (Stolfi/Zattera slot grammar), positional entropy should be NON-UNIFORM: high at some positions (the content/root slots) and low at others (the template/affix slots). If entropy is uniformly ~2.3 across all positions, a systemic transformation (verbose cipher, substitution) affecting all positions equally is more likely. Natural languages should show moderate, relatively flat entropy profiles. For H002: if longer Voynich words add predictable affixal material, h2 should decrease with word length; flat would argue against templating as the sole explanation.

## Method
Compute Shannon entropy of the character distribution at each word position (position 0 = first char, 1 = second, etc., from both start and end), for Voynich vs. Latin (Virgil + Caesar De Bello Gallico) vs. Italian (Dante). Also compute positional bias index (shuffled_H - actual_H at each position) and h2 by word length. Run q-initial analysis from H010 as a sub-experiment.

## Expected Outcomes

| Theory | Predicted positional entropy profile |
|--------|--------------------------------------|
| Natural language in cipher | Varies by position but non-dramatically; no sharp spikes or valleys |
| Slot grammar (constructed language) | Sharp contrast: low H at slot boundaries, higher H at slot centers |
| Glossographic/received text | Uniformly low H across all positions (template dominates everywhere) |
| Verbose cipher (systemic) | Uniformly constrained but slightly higher at grouped-unit boundaries |

## Raw Output
```
Positional H from start:       Voynich    Latin   Italian
  Pos 0 (onset):                 3.137    4.120     4.037
  Pos 1:                         3.237    3.628     3.400
  Pos 2:                         3.454    4.117     3.865
  Pos 3 (near root):             3.612    3.805     3.919
  Pos 4:                         3.606    3.813     3.623
  Pos 5:                         3.402    3.755     3.675
  Pos 6:                         3.272    3.610     3.586

Positional H from end:
  Pos -1 (final):      Voynich 2.456  Latin 3.248  Italian 3.062
  Pos -2:              Voynich 2.933  Latin 3.376  Italian 4.018
  Pos -3:              Voynich 3.286  Latin 4.043  Italian 4.009

Positional bias index (shuffled_H - actual_H), Voynich:
  Pos 0: +0.729  Pos 1: +0.627  Pos 2: +0.407  Pos 3: +0.237
  Pos 4: +0.236  Pos 5: +0.419  Pos 6: +0.561

Latin pos 0: -0.118 (onset is FREER than shuffled), Pos 2: -0.089
Italian pos 0: -0.077

H2 by word length (Voynich): 1→2.68, 2→1.98, 3→2.45, 4→2.34, 5→2.24, 6→2.21, 7→2.19, 8→2.23, 9→2.28... (roughly flat 2.19-2.34 for lengths 4-13)
H2 by word length (Latin):   2→2.10, 3→3.08, 4→3.37, 5→3.47 (rises then plateaus)

Q-initial: 5,091 words (15.5%), 97.7% followed by 'o'
H_initial (all): 3.137 — H_initial (no-q words): 2.976 (LOWER after removal)
```

## Result

**Three distinct structural findings:**

**Finding A — U-shaped positional bias profile.** The positional bias index (constraint relative to unigram distribution) forms a U-shape across word positions: highest at onset (pos 0: +0.729 bits) and suffix (pos 6: +0.561 bits), lowest at the middle positions (pos 3-4: +0.237 bits). Natural languages show the OPPOSITE at onset: Latin pos 0 bias = -0.118 (onset is FREER than shuffled), Italian pos 0 = -0.077. This U-shape directly matches the Stolfi/Zattera slot grammar prediction where crust (outer layer) constrains, core/mantle (inner) is freer.

**Finding B — Word-final positions are dramatically more constrained than any natural language.** H(-1) = 2.456 bits for Voynich vs. Latin 3.248, Italian 3.062. H(-2) = 2.933 vs. Latin 3.376, Italian 4.018. The final character of Voynich words is the most constrained position in the text — more constrained than word onset, and far more constrained than natural-language finals.

**Finding C — H2 by word length is flat for Voynich but rises-then-plateaus for natural languages.** Voynich h2 stabilizes at ~2.2 for lengths 4-13, with no upward trend. Latin rises from 2.1 (length 2) to 3.47 (length 5) and then plateaus. This means: in Voynich, additional word length does NOT carry additional information per character — consistent with template slots that add predictable structure rather than content.

**Q-initial (H010):** Removing q-initial words lowers H_initial from 3.137 to 2.976. q is almost exclusively followed by 'o' (97.7%). H010 was refuted: q-initial words are NOT a constrained slot whose removal reveals underlying lexical diversity; rather, q itself contributes entropy as a unique category.

## Interpretation

**The slot grammar hypothesis (Stolfi/Zattera) is strongly supported.** Three independent measurements all point to the same underlying structure:

1. The U-shaped positional bias exactly matches a grammar where outer slots (crust) are constrained and inner slots (core/mantle) are freer. Positions 3-4 from word start have the lowest bias — this is where Stolfi's "core" (gallows characters) typically sits in words of length 5-6. The crust (dealers: d, l, r, s, n, y, etc.) dominates at positions 0 and 5-6.

2. Word-final extreme constraint (H(-1) = 2.456) is consistent with a small set of word-final "dealer" characters: y, n, m, in, etc. The Stolfi grammar predicts that the suffix position is drawn from an extremely small set (m almost exclusively word-final, for example).

3. Flat H2-by-length is incompatible with natural language phonology (where longer words have root material that adds information). It is compatible with templated generation where additional length comes from adding more crust/mantle material with predictable entropy.

**The "uniform glossographic" hypothesis is additionally constrained.** Glossolalia/automatic writing produces roughly uniform entropy across positions (the template applies everywhere). The U-shaped profile, with positions 3-4 genuinely freer than edges, is not what uniform template generation would produce — it requires specifically structured slots.

**What this does NOT settle:** The slot grammar is consistent with (a) a constructed artificial language, (b) a cipher that maps a natural language through a templated encoding, and (c) an elaborate fraud constructed with a consistent rule. It discriminates against (a) pure random hoax, (b) simple glossolalia, (c) unstructured cipher (where all positions would be roughly equally constrained or unconstrained).

**The middle positions (3-4) are the most informative region.** If there is linguistic signal in Voynich, it is most likely to be found in the characters at positions 3-4 from word start — the innermost slots with the highest entropy. This is where the Stolfi core (gallows characters + their bench combinations) sits. Any experiment targeting the "content-carrying" part of Voynich words should focus on these positions.

## Limitations
- The U-shaped profile is computed over ALL words regardless of length. Short words (length 2-3) have no "inner" positions and will distort the endpoint measurements.
- The locus code parser fix is now working (1,065 labels extracted). Latin reference is now correct (Virgil + Caesar Latin, not English translations).
- H2 by word length uses flat-stream bigrams within words of each length — this ignores within-word positional structure and treats characters as exchangeable. A more rigorous analysis would compute h2 position-conditionally within each length class.
- The bias index is sensitive to the shuffling randomness; reported values are from seed 42 and may vary slightly across runs.

## Follow-up Questions
- What are the character distributions specifically at positions 3-4 (the freest slots)? Do they match any known language's root consonant inventory?
- The word-final H(-1) = 2.456 implies ~6-8 characters dominate the final position. Which ones, and do they form a grammatical category in the Stolfi grammar?
- H002 (length-conditioned entropy) is now tested: the result (flat Voynich, rising-then-flat natural language) should be added to findings.

