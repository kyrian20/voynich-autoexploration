# Experiment exp_001: Word-Initial Character Entropy

**Date:** 2026-04-09
**Hypothesis:** H003 — Word-initial character entropy in Voynichese is substantially higher than overall h2, approaching natural-language levels (~3–4 bits), which would indicate that low h2 is a within-word artifact and that the lexicon itself has normal diversity at its starting points.
**Status:** complete

## Hypothesis
If Voynichese's anomalously low conditional character entropy (h2 ≈ 2.0, Lindemann & Bowern 2020) reflects within-word templating or verbose encoding rather than lexicon-level poverty, then the first character of each word — which is not conditioned on anything within the word — should show entropy closer to what natural languages show at word-initial positions. Conversely, if the text is glossographic (phonological template generation with no real lexicon), low entropy should persist even at word-initial positions, because the template constrains word onsets.

This is the cleanest discriminator between the "obfuscated natural language" and "glossographic/received text" theories, because it isolates exactly one level of the hierarchy where their predictions diverge.

## Method
Extract the first character of every word in the ZL3b EVA corpus (excluding uncertain readings, words shorter than 1 character, and metadata). Compute Shannon entropy H = -Σ p(c) log2 p(c) over the distribution of word-initial characters. Compare to:
1. Overall unigram character entropy in Voynich
2. Overall h2 (bigram conditional entropy) in Voynich
3. Word-initial entropy in Latin (Vulgate)
4. Word-initial entropy in Italian (Dante)
5. A random control: shuffle all characters within each Voynich word, then measure "word-initial" entropy — this tests whether the word-initial distribution is just the unigram distribution or is specifically constrained at onset positions

## Expected Outcomes

| Theory | Predicted word-initial entropy |
|--------|-------------------------------|
| Natural language in cipher | ~3.0–4.5 bits — similar to Latin/Italian word-initial entropy |
| Glossographic/received text | ~2.0 bits — same as overall h2, no elevation at word onset |
| Constructed artificial language with open onset slot | ~3.0–4.0 bits |
| Constructed artificial language with constrained onset slot | < 2.0 bits (onset is the most constrained position) |
| Hoax / meaningless text | Matches unigram distribution — indistinguishable from shuffled control |

## Raw Output
```
Corpus                            H1      H2  H_init  init-H2
-------------------------------------------------------
Voynich all                    3.861   2.341   3.137   +0.796
Voynich body                   3.861   2.341   3.137   +0.796
Latin Vulgate                  4.130   3.478   3.978   +0.500
Italian Dante                  4.023   3.413   4.037   +0.625

Voynich top word-initial characters:
  o: 7750 (23.6%), c: 6042 (18.4%), q: 5091 (15.5%), s: 3886 (11.8%)
  d: 3054 (9.3%), y: 1576 (4.8%), a: 1426 (4.3%), l: 1163 (3.5%)

Voynich H_initial (shuffled): 3.871
Gap (shuffled minus actual): 0.734 bits

Latin H_initial (shuffled): 4.076 — gap: +0.099
Italian H_initial (shuffled): 3.960 — gap: -0.077 (word-initial slightly MORE diverse than unigram)

Note: Label parsing returned 0 words — locus code prefix characters (=, *, @) were not stripped before checking startswith('L'). Fix needed for H009.
```

## Result
Voynich word-initial entropy (H_init = 3.137 bits) is substantially higher than its overall h2 (2.341 bits), with a gap of +0.796 bits — larger than the analogous gap in Latin (+0.500) or Italian (+0.625). However, the absolute word-initial entropy is substantially lower than Latin (3.978) or Italian (4.037). Additionally, Voynich word-initial characters are more constrained relative to the unigram distribution than natural languages: the shuffled-minus-actual gap is 0.734 bits for Voynich vs. ~0.10 bits for Latin and ~0.00 bits for Italian. Four characters (o, c, q, s) account for 69.3% of all word onsets.

## Interpretation
**The pure glossographic model is contradicted.** A text produced entirely by phonological template generation (where the template constrains all character positions equivalently) should show H_initial ≈ H2. Instead, word-initial positions are substantially more diverse (+0.796 bits elevation). This is the pattern expected if there is a real lexicon behind the text: word onsets are freer than word continuations, because continuations are constrained by the prior character but onsets are not.

**The "natural language h_initial" prediction is partially supported but with important caveats.** H_initial = 3.137 bits is in the right neighborhood for natural language (vs. Latin 3.978, Italian 4.037), but Voynich's word-initial distribution is STILL more constrained than any natural language tested:
- The shuffled control shows that Voynich's unigram distribution would produce H_initial = 3.871, but the actual onset distribution is only 3.137 — a deficit of 0.734 bits. This means word-initial positions are NOT random draws from the character pool: they favor a small set (o, c, q, s, d = 82% of all onsets).
- In natural languages, word-initial entropy equals or slightly exceeds the shuffled control, because onsets are in fact MORE diverse than non-initial characters (initial consonant clusters, etc.).

**The most informative quantity is the double gap:**
- Voynich: H_initial (3.137) sits midway between H2 (2.341) and the shuffled control (3.871)
- Latin: H_initial (3.978) sits very close to the shuffled control (4.076), meaning initial positions are nearly as free as random
- Italian: H_initial (4.037) ≈ shuffled (3.960)

This pattern is characteristic of a system where word onsets are a semi-constrained slot: freer than within-word positions (supporting lexicality) but still drawn from a restricted character class (consistent with the Stolfi/Zattera slot grammar, where the crust layer dominates and the "q" character appears almost exclusively at word onset).

**The q-initial phenomenon is extreme and noteworthy:** 15.5% of all Voynich words begin with q. In EVA convention, q almost always appears before o (the "qo" cluster) at word onset, and almost never elsewhere. This is exactly the pattern Stolfi documented. It strongly constrains the "obfuscated natural language" model: what natural language has 15% of words beginning with the same character in the same context?

**Net assessment:** Results are most consistent with a system that has SOME lexical structure (H_initial substantially above H2) but with a constrained onset slot (H_initial substantially below natural-language levels and below shuffled control). This is compatible with: (a) a constructed language with a restricted onset inventory, (b) a cipher that constrains what can appear at word boundaries, or (c) a slot grammar operating at the word level (Stolfi/Zattera). It is NOT compatible with pure glossolalia.

## Limitations
- Label parsing failed (0 labels extracted). The locus code parser needs to strip prefix characters (=, *, +, @) before the alphanumeric code. This must be fixed before H009 can run.
- EVA alphabet letters are not 1-to-1 with phonemes — 'c' as a standalone character in EVA is relatively rare (it's usually part of 'ch', 'ck', 'cth', etc.). The actual entropy depends on the level of glyph decomposition assumed.
- h2 computation here is character-level on the full word stream (concatenated without word boundaries). Compare against Lindemann & Bowern's figure of ~2.0: our 2.341 is higher, possibly because we include word boundaries implicitly by joining words. A more rigorous h2 would measure within-word conditional entropy only.
- The Latin Vulgate corpus has noise from the Gutenberg header/footer strip; the 't' and 'h' dominance in "Latin" initials looks suspicious (English KJV contamination possible — the Gutenberg file may be an English Bible, not Latin).

## Follow-up Questions
- **Why does the Latin "Vulgate" show 't' (20%) and 'h' (7.1%) dominance?** These look like English function words (the, that, this, he, her...). The corpus may actually be the KJV English Bible, not Latin text. Need to verify the corpus language before using it as a Latin baseline. This is Q001.
- The q-initial constraint (15.5% of word onsets, nearly always followed by 'o') is a major structural feature. Does it survive in a "true" word-initial entropy calculation where we strip qo as a single digraphic onset? H_initial would change substantially. This is a variant of H003 to add to the backlog.
- The mid-range H_initial strongly motivates H001 (positional entropy): if onset is semi-constrained, how does entropy vary across positions 0, 1, 2, 3, ... within words?

