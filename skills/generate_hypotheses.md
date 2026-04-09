# Skill: Generate Hypotheses

## Purpose
Evolve the hypothesis backlog. This skill covers: deriving follow-up hypotheses from completed experiments, recognizing when a finding opens a new direction, injecting novelty when the backlog is stale, and phrasing a hypothesis so it is actually testable.

## When to Use This Skill

Use after every completed experiment (to generate 1-3 follow-ups) and whenever the backlog feels depleted or the remaining hypotheses are all expensive or blocked on prerequisites.

## Part 1: Deriving Follow-Ups from a Completed Experiment

After any experiment, ask three questions:

**Question 1: What did the result not explain?**
If positional entropy is low at suffix positions but high at midfix positions, the natural follow-up is not "entropy is interesting" — it is "what is the character distribution in high-entropy midfix positions, and does it resemble any known language's consonant inventory?" Every result leaves a residue of unexplained variance. Chase it.

**Question 2: What would falsify the interpretation?**
If you interpreted a result as evidence for glossographic production, what result would change that interpretation? That falsifying test is usually the next experiment. Make it explicit: "We'd need to see X to rule out Y."

**Question 3: What did the control corpora reveal?**
Unexpected behavior in the control corpora is often more valuable than the Voynich result itself. If Latin shows a pattern you didn't anticipate, that's a hypothesis about Latin phonotactics — and the question of whether Voynich resembles that pattern is immediately testable.

## Part 2: Recognizing New Directions

Some findings don't just extend the current line of inquiry — they open a genuinely new one. Signs that a finding implies a new direction:

- The result contradicts the assumptions behind multiple backlog hypotheses simultaneously (e.g., if word boundaries turn out to be unreliable, all word-based entropy metrics need to be reconsidered)
- The result matches a pattern characteristic of a specific language family or cipher type not previously on the list
- The Botanist phase has produced a high-confidence plant anchor that creates a potential ciphertext-plaintext pair — any cipher hypothesis must now explain that pair, which is a new constraint
- The result is surprising enough that the most parsimonious explanation invokes a mechanism not yet represented in the backlog

When this happens, add the new direction to `open_questions.md` with a note explaining why the old agenda needs to shift. Do not silently reprioritize without logging the reason.

## Part 3: Injecting Novelty

When the backlog contains only expensive or blocked hypotheses, use these heuristics to generate new ideas:

**Decompose further.** If you've measured h2 at the character level, measure it at the glyph-class level (gallows / bench / vowel-like / other). If you've measured it on whole words, measure it on word-initial trigrams only. Every decomposition is a new hypothesis.

**Swap the unit of analysis.** Character → word → line → paragraph → section. Measurement → comparison → alignment → transformation. Absolute entropy → conditional entropy → mutual information → transfer entropy.

**Import a method from a neighboring field.** The Voynich literature tends to recycle the same methods. Areas that have undercontributed: corpus linguistics (collocations, mutual information between distant words), information theory (Kolmogorov complexity estimates), typology (universals of natural language phonotactics), and historical cryptography (specific 15th-century cipher types actually in use — nomenclators, polyalphabetic systems, steganography).

**Check the seeds.** Read `seeds/llm_conversation_2026_04.md` again. The conversation contains more suggestions than are currently in the backlog. Some of them may have become relevant after experiments that weren't yet done when the seeds were written.

**Check the Librarian's open_questions.md.** ~/voynich-kb/state/open_questions.md contains questions the Librarian flagged as unresolved. Some of them are directly testable with the methods you have.

## Part 4: Phrasing a Testable Hypothesis

A hypothesis is testable if it satisfies all of:
1. **Specific:** it names a measurable quantity (not "the text is language-like" but "h2 conditioned on word-initial position is ≥ 3.0 bits")
2. **Falsifiable:** there is a possible result that would refute it (not "Voynich might be a cipher" but "if verbose cipher grouping scheme G recovers h2 ≥ 3.5, the verbose cipher hypothesis is supported")
3. **Discriminating:** the result would favor one theory over others (not "entropy is interesting" but "entropy at this level of analysis would be expected under theory A but not theory B")
4. **Bounded:** the test can be completed in one experiment session, not an open-ended research program

Bad hypothesis: "The Voynich text is an artificial language."
Good hypothesis: "Voynich word-initial character entropy, measured over the full EVA corpus, is ≥ 3.0 bits — which would be consistent with a real lexicon and inconsistent with pure glossographic production."

## Part 5: Writing the Backlog Entry

```markdown
## HNNN: [Brief Title]

**Priority:** high | medium | low
**Status:** open
**Source:** [experiment ID that generated this, or "seeds/llm_conversation_2026_04.md", or "generate_hypotheses skill"]
**Description:** [1-2 sentences: what is being tested and what the test is]
**Expected outcome under competing theories:**
- Natural language in cipher: [prediction]
- Glossographic/received text: [prediction]
- Constructed artificial language: [prediction]
- Hoax / meaningless text: [prediction]
**Cost estimate:** trivial | small | medium | large
**Prerequisites:** [experiment IDs that must complete first, or "none"]
```

**Priority assignment:**
- **high:** cheap test that discriminates strongly (ideally rules out a whole class of theories)
- **medium:** moderate cost or moderate discrimination
- **low:** expensive, weak signal, or depends on many prerequisites

When in doubt, break a medium hypothesis into two smaller high-priority hypotheses.
