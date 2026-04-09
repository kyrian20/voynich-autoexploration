# Experiment exp_024: Lingua Ignota Phonotactic Comparison
Date: 2026-04-09

## Hypothesis Tested
H005: Does Voynichese phonotactically resemble Hildegard's Lingua Ignota more than it resembles natural languages (Latin, German)?

## Data Limitation

**Only 35/1011 Lingua Ignota words were publicly available.** The first 30 entries of the glossary are on Wikipedia/HandWiki; 5 additional words appear in Hildegard's documented sentence usage. The complete 1011-word glossary is only in Higley (2007) print edition. The first 30 words cover the theological/family hierarchy semantic domain (God → angel → patriarch → father → grandfather → boy...) — a morphologically regularized domain with heavy suffix derivation (-iz, -onz compounds). This likely overrepresents suffix rigidity relative to the full vocabulary.

**All results must be treated as preliminary.**

## Comparison Table

| Metric | Lingua Ignota (n=35) | Voynich (n=32,469) | Latin (n=66,528) | German (n=34,433) |
|---|---|---|---|---|
| **Initial char entropy** | 3.829 bits | 3.176 bits | 4.138 bits | 4.263 bits |
| **Final char entropy** | 2.567 bits | 2.455 bits | 3.306 bits | 3.567 bits |
| Bigram entropy | 6.156 bits | 5.712 bits | 7.349 bits | 7.160 bits |
| Mean word length | 7.26 chars | 5.21 chars | 5.75 chars | 4.60 chars |
| **Top-4 initials coverage** | 42.9% | **67.4%** | 35.6% | 35.5% |

## Key Findings

### 1. Onset Constraint: Voynich Is FAR More Constrained Than Lingua Ignota

| | Top-4 Initials | Coverage |
|---|---|---|
| Voynich | o, c, q, s | **67.4%** |
| Lingua Ignota | z, l, p, h | 42.9% |
| Latin | — | 35.6% |
| German | — | 35.5% |

Voynich's onset constraint (top-4 initials = 67.4%) is nearly double the Lingua Ignota (42.9%) and twice the natural languages (35-36%). Lingua Ignota onsets are only marginally more concentrated than Latin/German — **Lingua Ignota has free onset choice comparable to natural languages**.

Initial char entropy: Lingua Ignota (3.829) sits between natural languages (Latin 4.138, German 4.263) and Voynich (3.176). Lingua Ignota shows mild onset preference but is 0.65 bits ABOVE Voynich's constrained onset distribution.

**Conclusion:** Voynich's onset constraint has NO analog in Lingua Ignota. The slot-grammar structure that forces 67% of Voynich words to start with o/c/q/s is absent from Lingua Ignota.

### 2. Word-Final Entropy: The One Similarity

Both Voynich (2.455) and Lingua Ignota (2.567) have substantially lower word-final entropy than Latin (3.306) or German (3.567). This is the most striking phonotactic similarity between the two.

Lingua Ignota final characters: z (dominant, 40% of words), l, r, a, s — the '-iz/-onz' ending pattern drives this.
Voynich final characters: y (41%), n (17%), l (16%), r (15%) — similar dominance by ~4 chars.

**Caveat:** The Lingua Ignota sample is from the first 30 glossary entries which are heavily suffixed derivational forms (the -iz, -onz, -riz endings repeat within the theological hierarchy). With the full 1011 words, final entropy would likely rise toward natural-language levels as diverse vocabulary semantic domains are included.

### 3. Bigram Entropy: Both Below Natural Languages

Voynich (5.712) and Lingua Ignota (6.156) are both below Latin (7.349) and German (7.160). However:
- The gap to natural languages is much larger for Voynich (-1.6 bits below Latin)
- Lingua Ignota is intermediate (-1.2 bits below Latin)
- With more words (less repetitive suffix tokens), Lingua Ignota bigram entropy would likely rise toward natural-language levels

### 4. Word Length: Lingua Ignota Is Longer

Lingua Ignota mean = 7.26 chars vs Voynich 5.21. The sample includes many long derivational compounds (kulzphazur=10, hilzscifriz=11, hilzpeueriz=11). With the full lexicon (including shorter animal/plant names), mean length would likely decrease toward natural-language levels (Latin=5.75, German=4.60). **Not a reliable comparison from this sample.**

## Verdict

**H005 NOT SUPPORTED (from available data).**

Voynichese does NOT more closely resemble Lingua Ignota than natural languages. The measured differences point in the opposite direction: Lingua Ignota phonotactics are much closer to Latin and German than to Voynich:

- Lingua Ignota has natural-language-like onset freedom (H_init = 3.83 ≈ Latin 4.14, far above Voynich 3.18)
- The only phonotactic similarity (low final entropy) is likely a sample artifact — the first 30 words are systematically derived forms with the same -iz/-onz endings

**Confidence level: LOW.** This is 35/1011 words. The theological hierarchy domain with its systematic -iz derivation is the single most morphologically predictable section of the vocabulary. Any conclusion from this sample could be reversed by the full word list.

**Recommended follow-up:** Obtain Higley (2007) word list or a digitized version from a research library. With 200+ words from diverse semantic domains (plants, animals, objects), the comparison would be definitive.

## Updated H005 Status

PARTIALLY TESTED — result is "not supported" but confidence is low due to very limited Lingua Ignota sample (35/1011 words, morphologically biased domain).
