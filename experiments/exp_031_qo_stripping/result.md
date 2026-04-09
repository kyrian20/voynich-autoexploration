# Experiment exp_031: qo-Stripping Analysis
Date: 2026-04-09

## Hypothesis Tested
H013: If "qo" is a grammatical article/particle prefixed to content words, stripping "qo" should reveal higher-entropy word stems underneath.

## Results

### 1. Initial Entropy After Stripping — OPPOSITE OF HYPOTHESIS
| Corpus | H_initial (bits) |
|--------|-----------------|
| Full corpus | 3.144 |
| Non-qo words | 3.027 |
| **qo-stripped stems** | **1.931** |
| Hybrid (non-qo + qo-stems) | 3.194 |

**qo-stripped stems are MORE constrained than the corpus average** (delta = -1.095 bits vs non-qo words). The article/particle hypothesis predicted higher entropy after stripping; the opposite is observed.

### 2. qo-Stripped Stems Are Dominated by k/t Initials
| Initial char | % of qo-stems |
|-------------|---------------|
| 'k' | 60.5% |
| 't' | 21.2% |
| 'l' | 4.3% |
| 'p' | 3.2% |
| (all others) | 10.8% |

Compare to non-qo words: 'o'=25.1%, 'c'=23.0%, 's'=14.6%, 'd'=11.2%, 'k'=3.4%.

**KL(qo-stems || non-qo words) = 2.96 bits** — the qo-stem initial distribution is extremely different from the free-word distribution. qo does NOT prefix arbitrary words; it attaches to a specific structural class (k/t-initial stems).

### 3. 52.6% of qo-Stems Exist as Free Words
384/730 qo-stripped stem types appear independently in non-qo vocabulary. Top examples:
- qokeey → keey (exists as free word)
- qokeedy → keedy (exists as free word)
- qokain → kain (exists as free word)
- qokedy → kedy (exists as free word)

The stems are real vocabulary items. qo is a genuine morphological affix, not a cipher artifact.

### 4. Currier A vs B
| Section | qo-words fraction |
|---------|------------------|
| Currier A | 11.1% |
| Currier B | 19.4% |

qo-words are nearly twice as frequent in B. B's top qo-words (qokeedy, qokain, qokedy, qokeey, qokaiin) are all k-initial stems, confirming this paradigm is especially dominant in Currier B.

### 5. Bigram Entropy
| Corpus | H2 (bits) |
|--------|----------|
| Full corpus | 2.060 |
| qo-stripped stems | 1.818 |
| Non-qo words | 2.137 |

qo-stripped stems have the LOWEST within-sequence predictability in the corpus — they are more templated than free words.

## Verdict

**H013 REFUTED (as article/particle hypothesis)**

The qo-particle hypothesis predicted: stripping qo → higher-entropy stems (arbitrary content words). The data shows: stripping qo → LOWER-entropy stems dominated by 'k' (60.5%) and 't' (21.2%).

**Better characterization:** qo is a MORPHOLOGICAL PREFIX that marks a specific grammatical form of k/t-initial word stems. The qo-prefix does not float freely across the vocabulary — it selects a structurally-determined subclass. This is consistent with Stolfi's "crust" model where qo-words form a distinct word class with a fixed "qo" onset slot.

The fact that 52.6% of qo-stems appear as free words suggests qo marks a PARADIGMATIC VARIANT (e.g., an inflected form) of base words, not a semantic particle. If "keedy" is a base word and "qokeedy" is an inflected form, the morphological system has at least two forms per stem type in this paradigm.

**New finding:** The "qo+k" onset (qok-) should be investigated as a compound onset element. The near-invariance of qo→k (60.5%) suggests "qok" may function as a single onset unit analogous to "ch" or "sh" in EVA.

## New Hypothesis Generated
**H032:** qo-words and their stem-equivalents (qokeedy/keedy, qokain/kain, etc.) appear in complementary distribution by position-in-line or section — testing whether they are truly grammatical alternants (inflected forms of the same lexical item).

**F037** to be added: qo-stripped stems have H_initial=1.931 bits (1.1 bits below non-qo words); 60.5% begin with 'k', 21.2% with 't'. qo is a morphological prefix selecting k/t-initial stems, not an article. 52.6% of qo-stems appear as free words (real vocabulary items).
