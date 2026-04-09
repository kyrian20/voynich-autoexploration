# Experiment exp_037: Label 'o'-Initial Morpheme Analysis
Date: 2026-04-09

## Hypothesis Tested
H033: Is 'o' at label-word initials a grammatical label-marker prefix (similar to how qo- marks Currier B vocabulary)?

## Results

### 1. Label o-Initial Bigram Distribution
The 157 o-initial label tokens have a specific second-character distribution:

| Bigram | Label % | Body % | Delta |
|--------|---------|--------|-------|
| ot- | 36.3% | 26.0% | **+10.3%** |
| ok- | 28.0% | 29.2% | -1.2% |
| ol- | 13.4% | 21.7% | -8.3% |
| op- | 6.4% | 4.3% | +2.1% |
| or- | 4.5% | 7.6% | -3.1% |

KL(label-o-bigrams || body-o-bigrams) = **0.154 bits** — relatively small. The o-initial bigram distributions are SIMILAR between labels and body text (both dominated by ot/ok/ol).

### 2. Section-Level o-Initial Rates

| Section | Label o-initial | Body o-initial | Ratio |
|---------|----------------|----------------|-------|
| Astro | 60.5% | 18.2% | 3.3× |
| Bio | 60.2% | 21.4% | 2.8× |
| Pharma | 54.4% | 21.6% | 2.5× |

Labels are 2.5-3.3× more o-initial than body text IN THE SAME SECTIONS. This section-invariant elevation rules out section-specific vocabulary as the explanation.

### 3. 64.3% of o-Stripped Stems Appear in Body Text
101/157 o-initial label words have their stem (word-minus-'o') in the body vocabulary:
- otar → tar (body freq: 41×)
- otol → tol (body freq: 39×)
- olor → lor (body freq: 39×)
- ockhy → ckhy (body freq: 36×)
- octhey → cthey (body freq: 43×)

This is analogous to the qo-prefix situation: otar = o + tar (known body word), just as qokeedy = qo + keedy.

## Verdict

**H033: SUPPORTED — 'o' Functions as a Label-Form Prefix**

Evidence for 'o' as a label-marker:
1. 3× higher o-initial rate in labels vs body text (same sections)
2. 64.3% of o-stripped stems appear in body vocabulary (real words with 'o' prepended)
3. Section-invariant elevation (all three sections at 54-60%)
4. Similar o-initial bigram distribution to body text (KL=0.154 bits) — the stems after 'o' are body-text-like

Evidence against:
- 35.7% of o-stripped stems are NOT in body vocabulary (label-unique items)
- Body text has many o-initial words (20.5%) — 'o' is not exclusively a label marker

**Interpretation:** 'o' functions as a LABEL-FORM MORPHEME that transforms body-text vocabulary items into their "labeled object" forms — similar structurally to how 'qo' marks Currier B vocabulary. Labels use both "native" o-forms (35.7%) and prefixed-body-stems (64.3%). This is the third morphological prefix pattern identified: qo- (Currier B k/t-stems), and o- (label forms of body-text words).

## New Finding (F044)
o-prefix labels: 64.3% of o-initial label words can be analyzed as o + body-text-word. Labels across all sections show 2.5-3.3× the body-text o-initial rate. The ot-/ok- dominant pattern (64.3% of o-labels) uses body-text second characters. 'o' appears to be a label-form morpheme — structurally parallel to the qo- prefix in Currier B.

## Updated Hypothesis H033 Implication
A label corpus that strips leading 'o' from object labels would produce stems with better body-text vocabulary overlap. This could improve cross-reference analysis between label vocabulary and body text.
