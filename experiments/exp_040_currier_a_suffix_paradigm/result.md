# Experiment exp_040: Currier A Suffix Paradigm
Date: 2026-04-09

## Question (H040)
Does Currier A have a structural parallel to B's 9-form suffix paradigm?

## Results

### 1. Currier A HAS a Suffix Paradigm — Same Scale as B

| Metric | Currier A | Currier B |
|--------|-----------|-----------|
| Total tokens | 9,807 | 21,605 |
| Stems with 2+ suffix variants | **349** | 639 |
| Stems with 2+ core-suffix variants | **226** | 455 |
| Most productive stem | d (803 tokens, 13 forms) | qok (1895 tokens, 15 forms) |
| 2nd most productive | ch (660 tokens, 16 forms) | ch (1149 tokens, 15 forms) |

Currier A has a productive suffix paradigm with 349 multi-suffix stems — essentially the same structural phenomenon as B, just with fewer total tokens.

### 2. The SUFFIX DISTRIBUTIONS Are Qualitatively Different

| Suffix | A% | B% | B/A ratio |
|--------|-----|-----|----------|
| -ol | **17.0%** | 6.1% | 0.4x (A dominant) |
| -or | **12.1%** | 3.3% | 0.3x (A dominant) |
| -chy | **5.1%** | 1.5% | 0.3x (A dominant) |
| -aiin | 14.6% | 11.3% | 0.8x (similar) |
| -edy | 0.2% | **15.1%** | **75x (B dominant)** |
| -eedy | 0.1% | **6.3%** | **62x (B dominant)** |
| -ain | 2.7% | **7.0%** | 2.6x (B dominant) |

**A's dominant suffixes are -ol/-or/-chy; B's dominant suffixes are -edy/-eedy/-ain.**  
-edy is 75× more common in B than A; -ol is 2.8× more common in A than B.

### 3. The Same Core Stems Appear in Both Dialects — With Opposite Suffix Preferences

**Stem 'ch':**
- In A: -ol(225), -or(146), -y(80), -ey(73) dominate → **chol, chor, chy, chey**
- In B: -edy(430), -ey(208), -dy(114), -eey(113) dominate → **chedy, chey, chdy, cheey**

**Stem 'sh':**
- In A: -ol(99), -or(56), -ey(50), -y(44) → **shol, shor, shey, shy**
- In B: -edy(367), -ey(173), -eey(88), -eedy(73) → **shedy, shey, sheey, sheedy**

**Stem 'ot':**
- In A: -ol(33), -y(33), -chy(25), -aiin(25) → **otol, oty, otchy, otaiin**
- In B: -edy(134), -aiin(107), -ar(94), -ain(89) → **otedy, otaiin, otar, otain**

The same stems are present in both dialects, but suffix preferences are nearly inverted: what A selects with -ol, B selects with -edy.

### 4. cth- Functions as a Prefix Morpheme in A — Parallel to qo- in B

| Metric | cth- in A | qo- in B (exp_031) |
|--------|-----------|---------------------|
| % of dialect tokens | 3.9% | 16.8% |
| Stems in free vocabulary | 37.3% | 52.6% |
| H_initial of stripped stems | **1.966 bits** | **1.931 bits** |
| H_initial of free words | 3.061 bits | 3.027 bits |
| KL (stem initials ∥ free words) | **2.281 bits** | **2.960 bits** |
| Stem onset concentration | o(43.5%), y(24.3%), e(20.3%) | k(60.5%), t(21.2%) |

cth- in A behaves almost identically to qo- in B as a morphological prefix:
- Dramatically reduced H_initial after stripping (1.966 vs 3.061 bits — near-identical to qo-)
- KL is high (2.281 bits) — cth-stems are a constrained vowel/y-initial class
- But different onset class: cth- selects o/y/e-initial stems; qo- selects k/t-initial stems

cth- is A's dialect-specific prefix morpheme, functioning structurally parallel to B's qo-.

## Finding (F047)
**Currier A has a suffix paradigm parallel to B's in STRUCTURE but opposite in SUFFIX PREFERENCES:**
- A: 349 multi-suffix stems dominated by -ol (17.0%) and -or (12.1%); -edy is near-absent (0.2%)
- B: 639 multi-suffix stems dominated by -edy (15.1%) and -eedy (6.3%); -ol is muted (6.1%)
- Same core stems (ch, sh, ot, ok, qok, d, s) appear in both dialects but take different suffixes: A's "chol/chor" = B's "chedy/cheedy" — the same stem, different suffix paradigm
- **cth- in A is a morphological prefix parallel to qo- in B**: H_initial of cth-stripped stems = 1.966 bits (vs 3.061 for free words), KL = 2.281 bits, selecting o/y/e-initial stems (while qo- selects k/t-initial stems)

## Implications
1. **A and B share a morphological system** — same productive stems, same paradigm STRUCTURE — but each dialect selects different suffix paradigms (-ol/-or for A; -edy/-eedy for B)
2. **Both dialects have a dialect-specific prefix morpheme**: cth- (A) and qo- (B) are structurally parallel but phonologically distinct and select different stem classes
3. This is consistent with A and B being two REGISTERS or SECTIONS of a single language, not two independent systems
4. The "vocabulary divergence" (Jaccard=0.148, exp_035) is now partly explained: A's chol/chor and B's chedy/cheedy are the SAME semantic content (same stem 'ch') in different grammatical dress

## H040 Verdict: STRONGLY SUPPORTED
Currier A has a structural parallel to B's suffix paradigm. The key finding is not just parallel structure, but that the SAME STEMS take DIFFERENT SUFFIX DISTRIBUTIONS in the two dialects — suggesting dialect-level suffix selection (case system? tense? register?) rather than two independent lexicons.
