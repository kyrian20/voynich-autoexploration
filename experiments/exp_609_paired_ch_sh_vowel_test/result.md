# exp609 — Paired per-folio ch/sh vowel test

## Question
Do folio-level vowel rates after ch and sh differ, and do they co-vary?

## Method and caveats
- Count the next character after each within-word ch/sh occurrence, if one exists; vowels are a/e/i/o/u/y.
- Compare folio-level rates only for folios with both contexts; bootstrap folios and perform a paired sign-flip test on ch-minus-sh vowel-rate differences.
- This is not a reproduction of Parisel's template-conditioned Beta-Binomial mixture. Equal folio weighting, tokenization, word-template composition and section effects limit interpretation.

## ZL3b
- Source SHA-256: bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc
- Overall raw counts: {"ch": {"a": 446, "e": 4322, "n": 9288, "vowel": 7868}, "sh": {"a": 127, "e": 2224, "n": 3783, "vowel": 3422}}
- Folios paired: 181
- Mean folio vowel rate after ch: 0.85815; after sh: 0.92055
- Mean paired difference (ch−sh): -0.06240; folio bootstrap 95% CI [-0.07807659062562528, -0.0467715704375914]
- Paired sign-flip two-sided p: 0.00005
- Correlation of folio rates (ch, sh): 0.5039

## IT2a
- Source SHA-256: 7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5
- Overall raw counts: {"ch": {"a": 448, "e": 4324, "n": 9433, "vowel": 7945}, "sh": {"a": 122, "e": 2229, "n": 3825, "vowel": 3440}}
- Folios paired: 182
- Mean folio vowel rate after ch: 0.85208; after sh: 0.90698
- Mean paired difference (ch−sh): -0.05489; folio bootstrap 95% CI [-0.07338408555917515, -0.035321545136600414]
- Paired sign-flip two-sided p: 0.00005
- Correlation of folio rates (ch, sh): 0.4143

## Interpretation
A difference or correlation is descriptive, not proof of a discrete folio switch or a decipherment. Proper replication requires the paper's exact template-conditioned extraction and held-out comparison against composition-matched controls.
