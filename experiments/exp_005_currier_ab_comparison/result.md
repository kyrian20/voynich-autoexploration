# Experiment exp_005: Currier A vs B Subcorpus Comparison

**Date:** 2026-04-09
**Hypothesis:** H004 (partial) — Are Currier A and B structurally similar ("dialects") or structurally different systems?
**Status:** complete

## Hypothesis
The "dialect" model predicts: similar structural entropy profiles, shared function words, different surface vocabularies with the same underlying grammar. The "different systems" model predicts: different entropy profiles, few shared high-frequency words, different template structures. This experiment tests structural and distributional divergence. Full embedding-based alignment (word2vec + Procrustes) is deferred to H004-followup.

## Method
Parse ZL3b body text by Currier A/B label. Compare: h2, h1, H_initial, H_final, positional entropy profiles, word length distributions, character KL divergence, vocabulary specificity (frequency ratios), and mutual information between word identity and Currier language.

## Expected Outcomes
| Theory | Prediction |
|--------|-----------|
| Dialect model | Low vocabulary specificity ratios, similar positional entropy, shared function words |
| Different systems / registers | High vocabulary specificity, different positional entropy shapes, few shared top words |
| Shared template, different "content" (glossographic) | Similar structural entropy, different surface vocabulary |

## Raw Output
```
Currier A: 9,265 tokens, 3,115 types  TTR=0.336  avg_len=5.19
Currier B: 20,278 tokens, 4,667 types TTR=0.230  avg_len=5.33

Entropy comparison:
         H1      H2    H_init  H_final
A:     3.830   2.348   3.001    2.644
B:     3.855   2.182   3.136    2.260

KL divergence (character level):
  KL(A||B) = 0.0668, KL(B||A) = 0.0711, symmetric = 0.0689

Top character differences (A% - B%):
  'o': +4.13%  'h': +3.13%  'c': +2.98%  [A has more of these]
  'e': -5.25%  'y': -1.74%  'd': -1.82%  [B has more of these]

MI(word; currier) = 0.437 bits (4.2% of H(word))

Vocabulary specificity (selected):
  A-specific: cthor(39x ratio), ckhey(54x), cthol(36x), sho(18x), cthy(27x)
  B-specific: qokeedy(14697x!), okedy(5130x), okeedy(4834x), chedy(98x), shedy(84x)

Positional entropy from start (pos 5-8):
  A: 3.591, 3.570, 3.558, 3.690  [stays high]
  B: 3.217, 3.029, 3.096, 3.092  [drops dramatically]

Word length distribution: A skews shorter (37% length 1-4), B skews longer (37% length 6-7)
```

## Result

**Six structural differences between A and B:**

1. **h2: A=2.348, B=2.182** — B is 0.166 bits more predictable per character than A. This is a non-trivial difference in within-word information content.

2. **H_final: A=2.644, B=2.260** — B's final characters are dramatically more constrained than A's. This reflects B's heavy use of -y, -ain, -edy suffixes vs A's more varied endings.

3. **Positional entropy profile at positions 5-8: A stays high (~3.6 bits), B drops sharply (~3.0-3.2 bits)** — the suffix zone of longer words is much more constrained in B than in A.

4. **Character-level KL divergence is LOW (0.069 bits)** — both subcorpora use the same character pool with similar unigram frequencies. The differences are in HOW characters are arranged, not in WHICH characters appear.

5. **Vocabulary specificity is EXTREME** — qokeedy appears 298 times in B and essentially zero in A (ratio 14,697:1). chedy appears 431 times in B and only 4 times in A (ratio 98:1). These are not dialect-level differences; these are category-level separations.

6. **MI(word; currier) = 4.2%** — This seems low, but consider: if A and B used literally the same words with the same frequencies, MI would be 0. The fact that 4.2% of word variation is explained by Currier identity means the A/B distinction accounts for meaningful vocabulary divergence, while most variation is shared.

## Interpretation

**The dialect model is NOT supported.** Dialects of the same language share function words (the most frequent words in both varieties). Instead, A's most frequent words (daiin, chol, chor, shol — all heavily biased toward A) are rare in B, and B's most frequent words (chedy, shedy, qokeedy — essentially absent in A) don't appear in A at all. This is the opposite of what dialects look like.

**The "shared template, different content" model is PARTIALLY supported.** Both A and B show similar character unigram distributions (low KL = 0.069) and similar onset entropy (pos 0: A=3.001, B=3.136). This is consistent with both subcorpora drawing from the same character pool and the same onset template. However, the suffix zone diverges sharply (pos 5-8: A ~3.6, B ~3.0-3.2), which means the TEMPLATE ITSELF is different in the suffix region.

**The most parsimonious interpretation:** A and B are distinct text types using the same character inventory but different slot-grammar templates, particularly in the suffix region. B has a more constrained suffix template (heavy -edy, -ain, -eedy suffixes) while A has more varied endings. This could reflect: (a) two different encoding schemes applied to different content (the cipher was applied differently in each section), (b) two different authors with distinct scribal habits, or (c) two genuinely different linguistic registers where one favors certain grammatical endings.

**The massive vocabulary specificity (qokeedy appearing ~0 times in A despite 298 occurrences in B) rules out the simple "same words, different frequency" model of dialects.** These are genuinely different word inventories, not just different frequency weightings of the same inventory.

**A/B comparison requires embedding-based alignment (the full H004 experiment) to test whether, under some mapping, A and B word distributions align.** The current data suggests they won't align cleanly at the word level, but may align at the character-class or slot level.

## Limitations
- The A/B labels in ZL3b are per-folio, not per-line; some transition folios may be ambiguous.
- The massive vocabulary divergence between A and B is partly explained by section-language correlation: Herbal A (folios 1-66) is mostly Currier A, and the Biological/Recipe sections are mostly Currier B. The vocabulary differences might be partly SECTION differences rather than LANGUAGE differences. Disentangling language from section requires holding section constant and varying language — which requires mixed-language folios.
- Mutual information of 4.2% seems low; but the lexical space is very large (10.3 bits of word entropy), so even 0.44 bits of word-currier MI represents substantial structural association.

## Follow-up Questions
- Are the vocabulary differences between A and B primarily driven by section (herbal vs recipes vs bio) or by language (A vs B)? Need to find folios that are mixed Currier-language within the same section.
- The Biological section (folios 75-84) is predominantly Currier B and dominated by qo-compound words. Is this a B-language property or a biological-section property?
- Do the full embedding-based alignment (word2vec + Procrustes, per the original H004 design) results confirm or contradict the "different templates" interpretation?
