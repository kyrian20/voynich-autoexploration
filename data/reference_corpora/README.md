# Reference Corpora Manifest

Reference corpora for use as natural-language baselines in entropy and statistical experiments. All are plain text (UTF-8 unless noted). The goal is not comprehensiveness but representativeness — a few thousand words per language is enough for the entropy tests in H001-H009.

---

## latin/vulgate.txt
**Source:** Project Gutenberg #8300
**Language:** Latin (Vulgate Bible, medieval/late antique)
**Size:** ~5.6 MB
**Notes:** Primary Latin baseline. Vulgate Latin is appropriate for the Voynich historical context (early 15th century, Central Europe, likely literate-clerical production). Contains Gutenberg header/footer — strip before use.

## latin/caesar_gallic_wars.txt
**Source:** Project Gutenberg #10657
**Language:** Latin (Classical — 1st century BCE)
**Size:** ~965 KB
**Notes:** Classical Latin for comparison with medieval Vulgate. Register differences may be informative. Contains Gutenberg header/footer — strip before use.

## italian/dante_divina_commedia.txt
**Source:** Project Gutenberg #1012
**Language:** Italian (medieval — early 14th century, Tuscan)
**Size:** ~626 KB
**Notes:** Dante's Italian is the best available medieval Italian baseline — geographically and temporally close to the Voynich's likely production context. Contains Gutenberg header/footer — strip before use.

## english/kjv_bible.txt
**Source:** Project Gutenberg #17
**Language:** English (early modern — King James Version, 1611)
**Size:** ~1.5 MB
**Notes:** Included as a control in a language with well-characterized entropy properties. Not a primary comparison target for Voynich (wrong language family and period) but useful for sanity-checking that entropy measurements behave as expected on a known corpus.

---

## Languages Still Needed

The following reference corpora are listed in SOUL.md but not yet downloaded:
- **Hebrew** (Tanakh): needed for H005 and any Semitic-language hypotheses. Source: sefaria.org or wikisource.
- **Arabic** (Quran): same motivation. Source: corpus.quran.com or any plain-text Quran.
- **German** (medieval): useful if phonotactic comparison to Germanic L1 is needed. Source: Gutenberg (MHD texts).

Add these if an experiment requires them. Do not download proactively.

---

## Preprocessing Notes

For entropy experiments, preprocessing should:
1. Remove Gutenberg headers/footers (lines before/after the actual text)
2. Strip punctuation and numerals
3. Lowercase
4. Tokenize into words (split on whitespace and punctuation)
5. Optionally: strip diacritics for character-level entropy (or keep them — document the choice)

For character-level entropy analysis (H001-H003), work with individual characters; for word-level analysis (H004), work with space-separated tokens. Always document which preprocessing was applied in the experiment's result.md.
