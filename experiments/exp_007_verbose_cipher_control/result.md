# Experiment exp_007: Verbose Cipher Control Test

**Date:** 2026-04-09
**Hypothesis:** Control for exp_006 — does adjacent-pair grouping always overshoot natural-language h2, and what would a genuine verbose cipher look like after pairing?
**Status:** complete

## Hypothesis
If adjacent-pair grouping always overshoots natural-language h2 as a mathematical property of the operation, then Voynich's paired h2 = 3.836 is unremarkable. But if pairing a genuine verbose cipher produces paired h2 = source language h2 (a theoretically motivated prediction), then we can compare Voynich's paired h2 against known language h2 values to test the model.

## Method
Apply adjacent-pair grouping to: (1) Voynich, (2) Latin, (3) Italian, (4) Italian with a fixed-filler verbose cipher (every char + 'x'), (5) Italian with a random-filler verbose cipher. Compare baseline h2, paired h2, and gain across all corpora.

## Raw Output
```
Corpus                          H2_base   H2_pair    Gain
Voynich (EVA)                    2.3413    3.8355  +1.4941
Latin (Virgil+Caesar)            3.5093    5.1373  +1.6280
Italian (Dante)                  3.4108    4.9489  +1.5381
Italian verbose-x (sim)          2.0135    3.4108  +1.3973
Italian verbose-rand(sim)        3.6242    6.1328  +2.5086
```

## Result

**The Italian fixed-filler verbose cipher simulation gives paired h2 EXACTLY equal to the original Italian h2 (3.4108).** This is mathematically exact — pairing a fixed-filler cipher perfectly recovers the source language's entropy. This validates adjacent-pair grouping as a verbose cipher detector: if Voynich were a fixed-filler pair cipher on a known language, its paired h2 would equal that language's h2.

**Voynich paired h2 = 3.836 does not match any tested natural language's baseline h2.** Italian h2 = 3.411 (too low), Latin h2 = 3.509 (too low). If Voynich is a fixed-filler verbose cipher, the source language must have h2 ≈ 3.836 — which is above both Latin and Italian. No candidate language with this property has been identified.

**The gain from pairing (+1.49 for Voynich) is similar to natural language gains (+1.54 for Italian, +1.63 for Latin).** This means the gain is largely a mathematical property of increasing token diversity through grouping, not a property specific to Voynich. The gain does NOT distinguish Voynich from natural language in this respect.

**Natural languages, when paired, give h2 values substantially HIGHER than Voynich paired h2 (Latin: 5.137, Italian: 4.949 vs Voynich: 3.836).** This means Voynich's paired-token sequence is actually LESS diverse than natural language paired sequences — Voynich has more constrained adjacent-character pairs than natural language does.

## Interpretation

**Fixed-filler adjacent-pair verbose cipher on Italian or Latin is ruled out.** If such a cipher were in use, paired Voynich h2 should equal Italian h2 (3.411) or Latin h2 (3.509). The observed value (3.836) is inconsistent with both.

**The gain from pairing is a generic mathematical property, not a Voynich-specific signal.** This retroactively confirms that exp_006's adjacent-pair result (h2 = 3.836) was not evidence for or against anything specific — the gain of ~1.5 bits occurs for all corpora tested.

**An important diagnostic has been established:** if any grouping scheme produces paired h2 exactly matching a known natural language's baseline h2, that is specific evidence for a fixed-filler verbose cipher on that language. This gives us a falsifiable test: for any candidate grouping scheme G and source language L, the test is: H2(Voynich after G) ≈ H2(L). The adjacent-pair scheme with Italian and Latin fails this test.

## Limitations
- Only two natural languages tested as cipher targets. The search should be extended to German, Arabic, Hebrew (if natural-language corpora can be obtained).
- Fixed-filler verbose cipher is the simplest case. Variable-filler schemes would produce different diagnostics; the control test only establishes the fixed-filler case.

## Follow-up Questions
- What is h2 for Arabic (unvoweled) or Hebrew? If either is ~3.836, it becomes a candidate source language for a fixed-filler verbose cipher interpretation.
- The "random-filler" verbose cipher gives extremely high paired h2 (6.13) — so variability in the filler character is immediately detectable. If Voynich has a specific filler character, its paired h2 should cluster around the source language's h2.
