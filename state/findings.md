# Findings
# Cryptanalyst — Voynich Manuscript Investigation
# Facts about the text that survived methodological scrutiny.
# Format: see skills/write_finding.md for the entry template.

---

## F001: Voynich Word-Initial Entropy Is Elevated Above h2 but Below Natural-Language Levels
**Experiment:** exp_001_word_initial_entropy
**Date:** 2026-04-09
**Finding:** Voynich word-initial character entropy (H_init = 3.137 bits, ZL3b EVA corpus, 32,866 words) is substantially elevated above the overall bigram conditional entropy (H2 = 2.341 bits), with a gap of +0.796 bits. This gap is larger than the analogous gap in natural languages (Latin Virgil: +0.50 approximate, Italian Dante: +0.62). However, H_init is substantially lower than natural-language word-initial entropy (Italian Dante: 4.037 bits), and the Voynich onset distribution is more constrained relative to its own unigram distribution than natural languages (shuffled-actual gap: Voynich +0.734 bits vs. Dante ~0.00 bits). Four characters (o, c, q, s) account for 69.3% of all word onsets.
**Limitation:** Label text was not successfully extracted (locus code parser bug — fix needed). Latin comparison baseline was mistakenly an English Bible; replaced with Virgil/Caesar Latin for subsequent experiments.

## F003: Voynich Positional Entropy Has a U-Shape — Middle Positions Are Freest
**Experiment:** exp_002_positional_entropy
**Date:** 2026-04-09
**Finding:** Voynich character entropy by word position forms a U-shape: onset (pos 0: 3.137 bits) and suffix (pos 5-6: 3.272-3.402) are lower entropy than middle positions (pos 3-4: 3.606-3.612). The positional bias index (shuffled_H - actual_H) confirms: pos 3-4 bias is +0.237 vs pos 0 bias of +0.729. Natural languages show the OPPOSITE at onset (Latin pos 0 bias = -0.118, Italian = -0.077 — onset is freer than the shuffled control). This U-shape directly matches the Stolfi/Zattera slot grammar's prediction (constrained outer crust, freer inner core/mantle).
**Limitation:** Computed over all words regardless of length; short words distort endpoint statistics.

## F004: Voynich Word-Final Positions Are the Most Constrained Characters in the Text
**Experiment:** exp_002_positional_entropy
**Date:** 2026-04-09
**Finding:** H(-1) = 2.456 bits (final character) is the single lowest-entropy positional measurement in Voynich, lower even than the overall h2 (2.341) when computed from the full stream. H(-2) = 2.933. Compare: Latin H(-1) = 3.248, Italian H(-1) = 3.062. The final position in Voynich is dramatically more constrained than natural-language word finals and than Voynich's own interior positions.
**Limitation:** Latin end-positional entropy from Virgil+Caesar Latin; not yet verified against medieval Latin.

## F005: Voynich H2 by Word Length Is Flat — No Information Rise with Length
**Experiment:** exp_002_positional_entropy
**Date:** 2026-04-09
**Finding:** For word lengths 4-13, Voynich h2 ranges only from 2.194 to 2.341 bits — essentially flat. In Latin (Virgil+Caesar), h2 rises from 2.1 (length 2) to 3.47 (length 5) then plateaus. In Italian (Dante), a similar rise-then-plateau is observed. The absence of a rise in Voynich means additional word length does not carry additional information per character — consistent with templated affixal material being added without adding content.
**Limitation:** H2 computed using flat-stream bigrams within length classes; does not account for positional structure within word-length groups.

## F006: Q-Initial Words Do NOT Drive Word-Initial Entropy Upward
**Experiment:** exp_002_positional_entropy
**Date:** 2026-04-09
**Finding:** Removing q-initial words (15.5% of corpus) LOWERS H_initial from 3.137 to 2.976 bits. Q is followed by 'o' in 97.7% of cases (4976/5091), making "qo" a nearly invariant word-initial bigram. Rather than inflating entropy via a constrained sub-slot, q contributes a unique onset category that adds diversity. Stripping it concentrates the remaining distribution further on o and c.
**Limitation:** This refutes H010 as stated but does not rule out q functioning as a grammatical marker; it establishes only that q is not suppressing H_initial.

## F007: Labels Have Substantially Higher h2 Than Body Text (+0.273 bits)
**Experiment:** exp_003_label_body_entropy
**Date:** 2026-04-09
**Finding:** Label text h2 = 2.575 bits vs body text h2 = 2.302 bits — labels are 0.273 bits less predictable per character within words. Labels also have dramatically higher type/token ratio (0.746 vs 0.229) and 55.3% exclusive vocabulary (439/794 label word types never appear in body text). Inner-slot entropy (pos 3-4) is higher in labels (3.499 vs 3.278 bits). All measurements are consistent with labels being informationally denser than body text.
**Limitation:** Label corpus is small (1,065 tokens). TTR comparison is not size-controlled.

## F008: qo-Words Are Largely Absent from Label Text (0% vs 17% in body)
**Experiment:** exp_003_label_body_entropy
**Date:** 2026-04-09
**Finding:** Body text has ~17% q-initial words (nearly always 'qo'); labels have effectively zero q-initial words (q does not appear in the top 6 initial characters for labels). The 'qo' construction is a body-text-specific feature. This is consistent with qo functioning as a grammatical particle (article/preposition) in body prose, absent from short label noun-phrases.
**Limitation:** Quantitative q-initial count for labels not directly measured; inferred from top initial char table.

## F009: daiin (Body Text's Most Frequent Word) Is Not Found in Label Vocabulary
**Experiment:** exp_003_label_body_entropy
**Date:** 2026-04-09
**Finding:** 'daiin' appears 710 times in body text (2.4% of tokens, most frequent word). It does not appear in the top 10 label words. If daiin were a ubiquitous function word, it would appear in labels; its apparent absence suggests it is either body-specific grammatical material or a body-text filler/padding element. Similarly, the top body words chedy, shedy, chol, qokeey, qokeedy are absent from label top-10. Label top words (o, s, y, otedy, oky) are structurally different from body top words.
**Limitation:** 'daiin' may appear in labels at low frequency but not rank in top-10; direct count not extracted.

## F010: Labels Have a Distinctive 'ot-'/'ok-' Vocabulary Pattern
**Experiment:** exp_003_label_body_entropy
**Date:** 2026-04-09
**Finding:** Among the top label words are otedy, oky, otaly, okal, okol, otal — all sharing an 'ot-' or 'ok-' initial bigram. These words are frequent in labels and largely absent from the top body vocabulary. 56% of label onsets are 'o' (vs 21% in body), driven largely by these words plus single-char 'o' tokens. This pattern is consistent with labels using a semantically distinct vocabulary register for describing/naming illustrated objects.
**Limitation:** Not verified whether ot-/ok- words appear in body text at low frequency.

## F011: H013 Refuted — qo Stripping Has Negligible Effect on Entropy
**Experiment:** exp_003_label_body_entropy
**Date:** 2026-04-09
**Finding:** Stripping the 'qo' prefix from q-initial words changes H_initial by +0.029 bits and H2 by +0.043 bits — negligible. qo is a tightly integrated word component, not a separable grammatical particle with content words underneath. The qo-stripping approach does not reveal latent lexical structure.
**Limitation:** Analysis on all words combined; result might differ if tested only on body text (where qo is concentrated).

## F012: daiin Concentrates Massively in Currier A / Herbal A (4.11-4.58% vs 1.28-1.41%)
**Experiment:** exp_004_daiin_distribution
**Date:** 2026-04-09
**Finding:** 'daiin' frequency: Herbal A = 4.11%, Currier A body = 4.58%, vs Bio = 1.28%, Recipes = 1.18%, Currier B body = 1.41%. daiin is the single most frequent word in Herbal A (382 occurrences). In labels, daiin appears only once (0.09%). daiin is not a universal function word — it is a Currier A / Herbal A specific feature.
**Limitation:** Section boundaries are approximate; overlap between sections and Currier languages possible.

## F013: Currier A and B Have Dramatically Different Top Vocabularies
**Experiment:** exp_004_daiin_distribution
**Date:** 2026-04-09
**Finding:** Currier A top words: daiin(424), chol(227), chor(147), s(100), shol(99), cthy(85). Currier B top words: chedy(431), shedy(367), qokeedy(298), ol(287), daiin(286), qokedy(264), qokeey(258). The A and B vocabularies share almost no top words. qo- words dominate Currier B body text (qokeedy, qokedy, qokeey, qokaiin, qokain) while being rare in Currier A. h2: Currier A = 2.348, Currier B = 2.182 (B is slightly more predictable per character).
**Limitation:** Currier language labels in ZL3b are per-folio, not per-line; some folios may contain mixed language.

## F014: Inner-Slot Characters Differ Between Currier A and B
**Experiment:** exp_004_daiin_distribution
**Date:** 2026-04-09
**Finding:** At positions 3-4 (inner/core slots, words ≥6): Currier A shows balanced e(15.7%)/o(15.7%) distribution, H=3.465. Currier B shows 'e' dominance at 29.3%, H=3.152. The inner-slot character distributions are structurally different between the two languages — B is more constrained at the informational core of words.
**Limitation:** Inner-slot positions are relative to word start; words of different lengths contribute differently to each position.

## F015: Bio Section is Dominated by qo- Words; Herbal A by Short Words with daiin
**Experiment:** exp_004_daiin_distribution
**Date:** 2026-04-09
**Finding:** Bio section top words: shedy, chedy, qokain, qokedy, ol, qokeedy, qokal, qokaiin — heavily qo-compound. Herbal A top words: daiin, chol, chor, shol, dar, or, chy, cthy — shorter, fewer qo-compounds. The manuscript sections have strongly section-specific vocabularies. The Bio section qo- word frequency is dramatically higher than other sections, while Herbal A's daiin concentration is the most distinctive feature of the herbal vocabulary.
**Limitation:** Section boundary classification is approximate (folio number ranges).

## F016: Currier A and B Have Different Suffix Templates (Positional Entropy Diverges at Pos 5-8)
**Experiment:** exp_005_currier_ab_comparison
**Date:** 2026-04-09
**Finding:** Currier A positional entropy from word start stays high at positions 5-8 (range 3.557-3.690 bits). Currier B drops sharply at the same positions (range 3.029-3.217 bits). H_final: A=2.644, B=2.260. The character distributions are similar at the unigram level (KL = 0.069 bits) and at onset positions, but diverge strongly at word suffixes. B's suffix zone is substantially more constrained than A's.
**Limitation:** Positional differences partly confounded with section differences (most B text is in Biological/Recipe sections).

## F017: Currier A/B Vocabulary Divergence is Near-Total for High-Frequency Words
**Experiment:** exp_005_currier_ab_comparison
**Date:** 2026-04-09
**Finding:** Words specific to B: qokeedy (298 occurrences in B, ~0 in A, ratio 14,697:1), chedy (431 in B, 4 in A, ratio 98:1), shedy (367 in B, 4 in A, 84:1). Words specific to A: cthor (36:1), cthol (36:1), cthy (27:1), sho (18:1). The A/B split is not a frequency-weighted dialect relationship — entire word categories exist in one subcorpus and are essentially absent from the other. MI(word; currier) = 0.437 bits (4.2% of word entropy).
**Limitation:** Cannot fully disentangle section effects from language effects without finding mixed-language folios within the same section.

## F002: Pure Glossographic Model (Uniform Template Across All Positions) is Contradicted
**Experiment:** exp_001_word_initial_entropy
**Date:** 2026-04-09
**Finding:** The substantial elevation of word-initial entropy (+0.796 bits) above within-word conditional entropy in Voynichese is incompatible with a text-generation process that constrains all character positions equivalently (pure phonological template / glossolalia model). Under such a model, H_initial ≈ H2; instead H_initial > H2 by a margin larger than seen in natural languages.
**Limitation:** This rules out the uniform-template variant of the glossographic hypothesis only. A model with a specifically constrained onset slot (low H_initial) and constrained continuation positions (low H2) could still produce a structured text without a real lexicon.
