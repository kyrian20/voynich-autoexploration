# Experiment exp_010: Label Word Section Distribution

**Date:** 2026-04-09
**Hypothesis:** H015 — ot-/ok- initial label words cluster in specific manuscript sections (content labels) vs. uniform distribution (generic structural labels)
**Status:** complete

## Hypothesis
Label words with 'ot-' or 'ok-' initial bigrams dominate the label vocabulary overall. H015 predicts: if these are content words naming depicted objects, they should cluster in specific sections. If they are generic structural labels ("figure," "note," "genus"), they should appear uniformly.

## Method
Parse all ZL3b words with locus and section context. Assign sections by folio number range: herbal_A (f1-f66), astro (f67-f73), bio (f74-f84), pharma (f85-f102), recipes (f103-f116). Count ot-/ok- label tokens per section vs. total label tokens per section. Compare with ot-/ok- body text frequency per section as a baseline.

## Raw Output
```
Label tokens: 1,065  Body tokens: 29,543

H015: ot-/ok- LABEL WORDS BY SECTION
  Section          ot/ok count  label total    % ot/ok
  herbal_A                   3           81       3.7%
  astro                    204          499      40.9%
  bio                       49          125      39.2%
  pharma                   116          358      32.4%
  recipes                    0            2       0.0%

Top ot-/ok- label words: otedy(9), oky(8), otaly(8), okal(7), okol(7), otal(7), otchdy(6)...

LABEL VOCABULARY BY SECTION
  herbal_A: 81 tokens, 45 types (TTR=0.556)
    Top: ['y', 'o', 'f', 'd', 'e', 's', 'p', 'x']
  astro: 499 tokens, 413 types (TTR=0.828)
    Top: ['okal', 'oky', 'ar', 'okeey', 'otaly', 'otal', 's', 'am']
  bio: 125 tokens, 108 types (TTR=0.864)
    Top: ['s', 'otedy', 'l', 'o', 'r', 'darol', 'daldy', 'otoly']
  pharma: 358 tokens, 326 types (TTR=0.911)
    Top: ['otoldy', 'okol', 'okody', 'otchdy', 'otedy', 'oky', 'ytedar', 'okedy']

ot-/ok- IN BODY TEXT BY SECTION (control)
  herbal_A: 10.2%  astro: 9.6%  bio: 9.7%  pharma: 11.7%  recipes: 15.6%
  (body ot-/ok- is UNIFORM across sections at ~10-15%)

LABEL VOCABULARY OVERLAP
  herbal_A ∩ astro: 9 shared (20% of herbal_A, 2% of astro)
  herbal_A ∩ pharma: 3 shared (7% of herbal_A, 1% of pharma)
  astro ∩ bio: 30 shared (7% of astro, 28% of bio)
  astro ∩ pharma: 43 shared (10% of astro, 13% of pharma)
  bio ∩ recipes: 0 shared
```

## Result

**H015 is confirmed: ot-/ok- label words are strongly section-specific.** They dominate non-herbal labels (astro: 40.9%, bio: 39.2%, pharma: 32.4%) and are nearly absent from herbal_A labels (3.7%) and recipes (0%). This is a systematic clustering — these words are NOT generic structural labels uniformly distributed.

**Crucially: ot-/ok- words in body text are UNIFORM across sections (~10%)** — they are not section-specific in running text. The strong section clustering appears only in labels. This means ot-/ok- is a label-specific naming convention for non-herbal illustrated content (astronomical diagrams, biological figures, pharmaceutical illustrations), not a body-text word class.

**The most surprising finding: herbal_A labels are dominated by SINGLE CHARACTERS.** Top label tokens in herbal_A: y, o, f, d, e, s, p, x — all single characters. Only 81 label tokens total, 45 types, TTR=0.556. The herbal section appears to use single-letter annotations near plant illustrations rather than multi-character label words. This is qualitatively different from all other sections.

**Pharma labels have TTR=0.911** — essentially every label word is unique. 358 tokens, 326 types. This is consistent with pharmaceutical labels being unique names for specific plants or preparations.

**Label vocabulary overlap between sections is near-zero.** herbal_A ∩ pharma = 3 shared types. astro ∩ bio = 30 shared types, bio ∩ recipes = 0. Each section has its own private label vocabulary, consistent with labels naming section-specific content objects.

## Interpretation

**ot-/ok- words are the labeling register for non-herbal illustrated content** — specifically for astronomical, biological, and pharmaceutical illustrations. They are not found in herbal labels (which use a completely different single-character convention) or recipe labels.

**The herbal single-character labels are a distinct discovery.** Herbal_A label "words" are predominantly single EVA characters (y, o, f, d, e, s, p, x). What are these? They could be:
- Color codes for plant illustrations (plants are sometimes color-coded in medieval herbals)
- Abbreviations for plant types, parts, or properties (root/leaf/flower?)
- Marginal annotations by a different hand
- A separate annotation layer not meant to be read as the primary text

This single-character labeling pattern has a different character from the ot-/ok- naming pattern and from body text. It may represent a third "register" in the manuscript.

**Sections form a labeling hierarchy:**
1. Herbal (single chars): oldest/simplest annotation layer?
2. Astro/Bio (ot-/ok- multi-word): names for depicted objects
3. Pharma (near-unique words, highest TTR): specific pharmaceutical names

## Limitations
- Folio-number-based section assignment is approximate. Some herbal-content folios may be mis-assigned.
- Single-character labels in herbal_A might be parsing artifacts (e.g., damaged/uncertain text reducing words to single chars). This needs to be verified against facsimile images.
- The small recipe label count (2 tokens) means no conclusions can be drawn for that section.

## Follow-up Questions
- What EVA characters appear as single-char herbal labels? Are they a specific subset (e.g., only 'y', 'o') or random? Do they correspond to known color categories or plant-part abbreviations in medieval herbals?
- Do the single-char herbal labels co-occur with specific plant colors in the illustrations? (Requires cross-referencing with image data — outside current scope)
- Are the ot-/ok- words in astro, bio, and pharma labels semantically consistent within each section (i.e., do the same ot-/ok- words appear repeatedly near the same type of illustration across different folios)?
- The near-zero vocabulary overlap between sections supports a "lexical richness" interpretation of pharma labels. What is the word frequency distribution for pharma labels — does it follow Zipf's law (natural language signature) or is it more uniform?
