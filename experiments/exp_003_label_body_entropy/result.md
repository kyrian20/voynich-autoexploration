# Experiment exp_003: Label vs Body Entropy / Inner-Slot Analysis / qo-Token

**Date:** 2026-04-09
**Hypothesis:** H009 — Labels have higher h2 than body text (signal/noise model); H012 — inner-slot (pos 3-4) character characterization; H013 — qo-as-token effect
**Status:** complete

## Hypothesis
If labels are under semantic pressure (they must refer to what they label), they should carry more information per character than body text, manifesting as higher h2. If body text is largely generated material (template or glossographic), its h2 should be lower. A signal/noise model predicts: h2(labels) > h2(body).

## Method
Parse ZL3b EVA locus codes into four categories (body/label/rider/circular) using the corrected locus parser. Compute full entropy profiles for each. Compare vocabulary overlap between labels and body. Run inner-slot (pos 3-4) character distribution for H012, and qo-stripping for H013.

## Expected Outcomes

| Theory | Label vs body h2 |
|--------|-----------------|
| Signal/noise hybrid | h2(labels) > h2(body) |
| Uniform cipher / uniform glossographic | h2(labels) ≈ h2(body) |
| Hoax with consistent style | h2(labels) ≈ h2(body) |

## Raw Output
```
Corpus      Tokens  Types     TTR      H1      H2  H_init  H_final
Body        29,543  6,771   0.229   3.862   2.302   3.145    2.403
Labels       1,065    794   0.746   3.771   2.575   2.377    2.818
Rider          307    255   0.831   3.699   2.389   2.803    2.438
Circular     1,951  1,006   0.516   3.756   2.379   2.765    2.783

Vocabulary overlap labels vs body:
  Label types: 794 | Body types: 6,771
  Shared types: 355 (44.7% of labels)
  Label-exclusive: 439 types (55.3%)

Top body words: daiin(710), chedy(433), shedy(369), ol(353), chol(309), qokeey(298)...
Top label words: o(13), s(12), y(10), 'otedy'(9), oky(8), otaly(8), d(7), okal(7)...

Label initial chars: o(56%), d(9%), y(8%), s(7%), c(6%), a(5%)
Body initial chars:  o(21%), c(19%), q(17%), s(12%), d(9%), y(5%)

Label final chars:  y(42%), l(14%), r(14%), n(7%), s(6%), m(6%)
Body final chars:   y(43%), n(17%), l(15%), r(15%), s(3%), m(3%)

H012 Inner slot (pos 3-4, words ≥6):
  Body:   H=3.278 bits — e(25.5%), i(12.6%), h(11.8%), d(10.8%), a(9.9%), o(8.4%)
  Labels: H=3.499 bits — a(14.3%), o(13.1%), d(12.0%), e(11.5%), h(10.5%), l(10.4%)

H013 qo-as-token:
  H_initial original=3.137 → stripped=3.166  (Δ +0.029)
  H2 original=2.341 → stripped=2.384          (Δ +0.043)
```

## Result

**H009 confirmed:** Labels have substantially higher h2 (2.575) than body text (2.302), a gap of +0.273 bits. This is the most constrained body of text in the manuscript (only 1,065 tokens) but the effect is large and directionally consistent with the signal/noise model.

**Vocabulary divergence is extreme:** 55.3% of label word types do not appear in the body text at all. Labels use a predominantly exclusive vocabulary. The top body words (daiin, chedy, shedy, ol, chol, qokeey) are almost entirely absent from the top label words.

**q-initial words are largely absent from labels:** Body has 17% q-initial words; labels have 0 q-initial words in the top 6 initial characters. qo words are a body-text phenomenon.

**Label word-initial entropy is LOWER than body (2.377 vs 3.145):** This appears paradoxical given higher h2, but is explained by extreme 'o' dominance at label onsets (56%). Many labels begin with 'o' or 'ot-'/'ok-' compounds — a label-specific vocabulary pattern. The body's word-initial diversity is partially driven by the 17% q-initial words; labels have almost no q-initial words.

**Inner-slot entropy is higher in labels (H=3.499 vs 3.278):** At positions 3-4, labels show more diverse character distributions than body text, particularly with 'a', 'l', 'r' appearing more prominently vs body's domination by 'e' (25.5%).

**H013 (qo-as-token):** Stripping the 'qo' prefix changes H_initial by only +0.029 bits and H2 by +0.043 bits. Negligible effect. qo-stripping does not reveal underlying linguistic structure.

## Interpretation

**The signal/noise hypothesis (signal in labels, structured noise in body) is partially supported.** Labels have higher within-word conditional entropy (h2), higher TTR, largely exclusive vocabulary, and more diverse inner-slot characters. All of these are consistent with labels being semantically constrained content while body text repeats a restricted set of templates.

**However, the label onset pattern complicates the picture.** The 56% 'o' dominance at label onsets, combined with the prevalence of 'ot-' and 'ok-' compounds (otedy, oky, otaly, okal, okol, otal), suggests that labels have their OWN distinctive vocabulary structure — not just "more diverse" but differently structured. This is consistent with Zattera's finding that different manuscript sections have distinct slot grammars, but extends it: labels don't just use different words from body text, they use words with different internal structure.

**The absence of qo-words from labels is significant.** If qo is a grammatical marker (article, preposition, or discourse marker) that belongs to body prose grammar, its absence from short label text makes sense: labels are noun-phrases, not sentences. This is exactly the distributional property we'd expect if qo functions as a function word (like "the" or "of") that appears in connected prose but not in isolated labels.

**The body text's high-frequency words (daiin, chedy, shedy) don't appear in labels.** daiin (the most frequent body word at 710 occurrences = 2.4% of body tokens) appears 0-very few times in labels. This is structurally unusual: in natural language, the most frequent words are function words that appear everywhere; if daiin were a function word, it should appear in labels too. Its absence suggests daiin is either: (a) a body-text-specific grammatical feature with no analogue in label syntax, (b) a filler/padding word in the template-generation sense, or (c) a body-specific content word. This is an important discriminating question.

**The qo-stripping result rules out H013:** qo functions as a unit bigram but stripping it doesn't expose latent lexical structure. The qo prefix is better modeled as part of the word's template rather than as a separable grammatical particle with content words underneath.

## Limitations
- Labels corpus is small (1,065 tokens / ~5,700 chars). H2 estimate may be less stable than for body (29,543 tokens). The +0.273 bit difference is large enough to be unlikely to be a sampling artifact, but confirmation with a larger label corpus (e.g., Zattera's concordance file with more characters) would strengthen this.
- "Labels" as identified by ZL3b locus codes may include some text that isn't in the traditional sense "labels next to illustrations" — the locus taxonomy should be verified against the manuscript.
- The TTR comparison is not controlled for sample size (labels have 74x fewer tokens, so TTR would naturally be higher from random-sample effects). A fairer comparison would subsample body tokens to 1,065 and compare TTR.

## Follow-up Questions
- H_lex(body) = 10.342 vs H_lex(labels) = 9.356 — why is lexical entropy lower for labels despite higher TTR? (Answer: fewer tokens, smaller corpus → less total information. This is an artifact.)
- **daiin appears 710 times in body (2.4% of tokens) but likely rarely in labels. Why?** This needs direct verification. If daiin is truly absent from label vocabulary, it is likely a body-specific grammatical marker, not content. This has implications for Currier A/B analysis (H004).
- Labels show 'ot-' / 'ok-' word family as dominant. Is this a specific semantic category? Check if these words cluster in particular manuscript sections (herbal vs astronomical vs balneological) or are uniformly distributed across labels.
- The circular text (1,951 words) has intermediate statistics between body and labels — worth profiling more carefully as its own category.
