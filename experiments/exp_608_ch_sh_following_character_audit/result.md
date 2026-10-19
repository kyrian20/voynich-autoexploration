# exp608 — ch/sh following-character audit

## Question
Do cleaned EVA tokens show folio-level variation in the character following ch/sh, as suggested by Parisel (2026)?

## Method and limitations
- Count each within-word occurrence of ch or sh with a following character; summarize by folio and transcription.
- Report next-character frequencies and vowel/e/a rates overall; omit Currier breakdown because labels are not parsed authoritatively.
- Folio e-rate range uses folios with at least five contexts.
- This is a descriptive proxy, not a replication of Parisel's template-conditioned Beta-Binomial mixture. No significance or decipherment claim follows.
- ZL3b and IT2a are related transcriptions, not independent physical witnesses.

## ZL3b
- Source SHA-256: bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc
- Folios with contexts: 183; occurrences: 13083
- Next-character counts: {"a": 573, "c": 518, "d": 783, "e": 6552, "f": 7, "g": 6, "h": 5, "i": 3, "k": 186, "l": 62, "o": 3081, "p": 26, "r": 15, "s": 87, "t": 88, "x": 4, "y": 1087}
- Vowel rate: 0.8634; e rate: 0.5008; a rate: 0.0438
- Folio e-rate range (n≥5): [0.0, 0.853448275862069]

## IT2a
- Source SHA-256: 7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5
- Folios with contexts: 182; occurrences: 13258
- Next-character counts: {"a": 570, "c": 565, "d": 796, "e": 6553, "f": 7, "g": 3, "h": 3, "i": 2, "k": 192, "l": 62, "m": 2, "n": 1, "o": 3141, "p": 26, "r": 19, "s": 102, "t": 90, "x": 5, "y": 1119}
- Vowel rate: 0.8587; e rate: 0.4943; a rate: 0.0430
- Folio e-rate range (n≥5): [0.0, 0.8571428571428571]

## Interpretation guardrail
Folio variation would be compatible with the published claim but would not establish a discrete switch: word templates, section composition, transcription conventions and small counts can create apparent differences. Proper replication requires exact extraction rules, template-conditioned modeling and held-out validation.
