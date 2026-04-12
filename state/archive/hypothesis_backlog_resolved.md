# Hypothesis Backlog
# Cryptanalyst — Voynich Manuscript Investigation
# Format: see skills/generate_hypotheses.md for the entry template.
# Ordering within a priority tier is not significant; re-order as priorities shift.

---

## H490: MID Slope Improvement
**Priority:** high
**Status:** RESOLVED — exp_286 (2026-04-11) — PARTIALLY CONFIRMED (marginal). alpha=0.20 accepted (MID slope +0.002; menz_r +0.009). gamma ceiling at 0.30 confirmed. Architectural ceiling reached for gamma+alpha mechanism. H491 generated. See F286.

---

## H489: LL_wl Excess — Reduce LL Midfix Rate
**Priority:** high
**Status:** RESOLVED — exp_285 (2026-04-11) — NEGATIVE (opposite direction). Reducing p_ll_mf worsens menz_r (higher LL_wl → more negative r, not an artifact). VMS-accurate LL_wl (p_ll=0.00, LL_wl=4.948) gives menz_r=-0.043 (19% of target). True deficit: MID slope. Architecture: p_ll_mf=0.00. H490 generated. See F285.

---

## H488: Restore LF Midfix — Add LF Midfix Sampling Back to cipher_lf
**Priority:** high
**Status:** RESOLVED — exp_284 (2026-04-11) — CONFIRMED. LF midfix restored: LF_wl 4.854→5.889 (VMS=5.732). menz_r: +0.037→-0.108 (correct sign, 48% of target). 19/19 PASS at all p_lf_mf ∈ {0.00-0.50}. p_lf_mf=0.50 selected. Architecture: 15 mechanisms. New concern: LL_wl=5.697 vs VMS 5.015 → H489. See F284.

---

## H486: Restore Menzerath r by Reducing p_mf
**Priority:** medium
**Status:** RESOLVED — exp_283 (2026-04-11) — NEGATIVE (wrong root cause). p_mf reduction doesn't flip menz_r. LF midfix missing since exp_280 is the true cause. H488 generated. See F283.

---

## H483: Word-Index-Conditioned MID Generation
**Priority:** medium
**Status:** RESOLVED — exp_282 (2026-04-11) — PARTIALLY CONFIRMED. MID slope improved 28× (52% of target). Menzerath r positive (+0.037) — MID midfix interaction. gamma=0.30 + alpha=0.15 accepted as 13th/14th mechanisms. See F282.

---

## H485: Timm Modification Rate Sweep
**Priority:** medium
**Status:** RESOLVED — exp_281 (2026-04-11) — NEGATIVE. MP=0.90 is minimum viable (18/19 at lower values). Vocabulary over-production is structural. See F281.

---

## H484: Midfix Sampling for MID Words
**Priority:** high
**Status:** RESOLVED — exp_280 (2026-04-11) — PARTIALLY CONFIRMED (with architectural surprise). p_mf=0.20 maintains 19/19 PASS and improves word_len (102.9%). Surprise: full sim already over-produces vocabulary at p_mf=0 (5255 vs VMS 2929). Vocabulary gap from exp_279 was simplified-sim artifact. Timm mechanism (MP=0.90) over-generates unique word forms. H485 generated. See F280.

---

## H482: VMS Vocabulary Richness Gap
**Priority:** medium
**Status:** RESOLVED — exp_279 (2026-04-11) — CONFIRMED. Gap 10-15×. Root cause: 62-71% of VMS MID words have midfix. H484 generated. See F279.

---

## H472: VMS Word Length Distribution
**Priority:** low
**Status:** RESOLVED — exp_278 (2026-04-11) — CONFIRMED. Log-normal fit adequate. A std=1.918 (skewness=1.417), B std=1.681 (skewness=0.395). VMS narrower than Latin. See F278.

---

## H466: B-Dialect Fine-Grained p_sh_qok Sweep
**Priority:** low
**Status:** RESOLVED — exp_277 (2026-04-11) — NEGATIVE. p=0.02 maximum viable; +0.031 E improvement (3.2% gap closure). Not worth 13th mechanism. See F277.

---

## H477: Word Repetition Distance Distribution
**Priority:** medium
**Status:** RESOLVED — exp_276 (2026-04-11) — PARTIALLY CONFIRMED. Directionality correct (A<B in both VMS and sim, consistent with r_mid=0.87 vs 0.25). VMS 2× short-distance enrichment vs shuffled. Simulation over-produces by 2–41× (vocabulary size artifact). See F276.

---

## H476: ch→ch and sh→sh Depletion in MID Position
**Priority:** medium
**Status:** RESOLVED — exp_275 (2026-04-11) — PARTIALLY CONFIRMED (B-dialect specific). B ch→ch=0.943, sh→sh=0.937 (DEPLETED); A ch→ch=1.194, sh→sh=1.312 (ENRICHED). Sim over-produces for B: sh→sh gap+0.617 (substantial), ch→ch gap+0.199. Bio section most depleted. Mechanism unresolved — may be indirect effect of qok↔ch coupling. Architecture gap identified; not in battery; 19/19 PASS unaffected. See F275.

---

## H001: Positional Entropy Analysis
**Priority:** high
**Status:** tested
**Source:** seeds/llm_conversation_2026_04.md
**Description:** Compute second-order character entropy (h2) conditioned on position within the word (position 0, 1, 2, ..., from both start and end). If entropy varies strongly by position — high in the middle/root slot, low at edges — this implicates a rigid prefix-midfix-suffix template. If entropy is uniformly ~2 across all positions, a systemic transformation (verbose cipher, substitution cipher) is more likely.
**Expected outcome under competing theories:**
- Natural language in cipher: entropy should vary by position in a language-like way, with some high-entropy positions corresponding to root consonants
- Glossographic/received text: entropy should be low across all positions, with no clear "root" slot showing elevated entropy
- Constructed artificial language with templated morphology: entropy should be high at a bounded set of positions (the "content" slots) and low elsewhere
- Hoax / meaningless text: entropy should be roughly uniform or follow the character frequency distribution with no positional structure
**Cost estimate:** small
**Prerequisites:** none — requires only the EVA transcription and a working Python environment

---

## H002: Length-Conditioned Entropy
**Priority:** high
**Status:** tested
**Source:** seeds/llm_conversation_2026_04.md
**Description:** Compute h2 as a function of word length. Natural languages show roughly constant per-character entropy across word lengths (longer words don't get more predictable per character). If Voynich entropy drops sharply for longer words, this indicates that additional length comes from predictable affixal/padding material rather than additional information — evidence for templating or padding.
**Expected outcome under competing theories:**
- Natural language in cipher: relatively flat entropy vs. length curve, similar to reference corpora
- Glossographic/received text: could be flat (glossolalia templates scale) or could drop (longer words accumulate more template material)
- Constructed artificial language with templated morphology: strong drop in entropy for longer words as affixes accumulate
- Hoax / meaningless text: flat or erratic curve — no linguistic reason for length-entropy correlation
**Cost estimate:** small
**Prerequisites:** none — run simultaneously with H001

---

## H003: Word-Initial Character Entropy
**Priority:** high
**Status:** tested
**Source:** seeds/llm_conversation_2026_04.md
**Description:** Extract only the first character of each word token in the corpus and measure the entropy of this distribution. This strips away within-word sequential predictability and measures lexicon-level entropy — whether the vocabulary itself is diverse at its starting points. Word-initial entropy ~3-4 bits (similar to natural languages) while overall h2 ~2 bits would strongly indicate that low h2 is a within-word artifact of templating or verbose encoding, not a property of the lexicon. This is the cleanest discriminator between glossographic and obfuscated-natural-language theories.
**Expected outcome under competing theories:**
- Natural language in cipher: word-initial entropy should be 3–4 bits, similar to reference corpora
- Glossographic/received text: word-initial entropy should also be low (~2 bits), because the template constrains word beginnings as much as continuations
- Constructed artificial language with templated morphology: low word-initial entropy if the template fixes the initial character class; higher if the initial slot is free
- Hoax / meaningless text: could be either, depending on how the text was generated
**Cost estimate:** trivial
**Prerequisites:** none — this is the cheapest and most discriminating of the entropy tests

---

## H004: Currier A vs Currier B Unsupervised Alignment
**Priority:** medium
**Status:** tested (exp_023) — A/B are NOT same system: vocab Jaccard=0.148, context alignment 2/100 identical pairs (vs 21% null), rank ρ=0.337. A exclusive: cth- cluster. B exclusive: -edy/-ain paradigm. Shared: ~21 short function/template words.
**Source:** seeds/llm_conversation_2026_04.md
**Description:** Treat Currier A and Currier B subcorpora as separate texts. Train token embeddings (word2vec or simple co-occurrence vectors) separately on each. Attempt unsupervised cross-lingual alignment (e.g., Procrustes alignment of embedding spaces). If they align cleanly at the word level, A and B are one system and probably encode something. If function-word-like tokens align but content-word-like tokens don't, this is the fingerprint of shared phonological template with independent "content" generation (received-transcription model). If they don't align at all, A and B may be genuinely different systems.
**Expected outcome under competing theories:**
- Natural language in cipher: strong alignment, especially for high-frequency tokens (function words align well across dialects)
- Glossographic/received text: partial alignment — shared templates align, content tokens don't
- Two distinct languages or systems: no alignment
- One author with stylistic variation: high alignment at all token types
**Cost estimate:** medium
**Prerequisites:** EVA transcription with Currier A/B labels (need to verify these are present in the downloaded transcription)

---

## H005: Phonotactic Comparison to Hildegard's Lingua Ignota
**Priority:** medium
**Status:** partially tested (exp_024) — NOT supported from 35/1011 words: LI onset entropy=3.829 (≈Latin 4.138, far above Voynich 3.176); LI top-4 coverage 42.9% vs Voynich 67.4%; only similarity is low final entropy (likely sample artifact). Needs full Higley 2007 word list (200+ words) for definitive test.
**Source:** seeds/llm_conversation_2026_04.md
**Description:** Hildegard of Bingen's Lingua Ignota (12th century) is the closest known analog to Voynich: an invented language/script by a visionary author, with surviving vocabulary (~1000 words glossed into Latin and German). Compare phonotactic profiles of Voynichese and Lingua Ignota: permitted character bigrams, character class distributions, word-length distributions, and syllable template rigidity. If Voynichese resembles Lingua Ignota's relationship to its Latin/German base languages more than it resembles any natural language, that is meaningful. This comparison may not have been done rigorously before — check the KB first.
**Expected outcome under competing theories:**
- Glossographic/received text: Voynichese should resemble Lingua Ignota more than it resembles any natural language
- Natural language in cipher: Voynichese's underlying phonotactics should align with some natural language, not with invented languages
- Constructed artificial language: could go either way depending on the construction method
**Cost estimate:** medium — requires locating and digitizing Lingua Ignota word list
**Prerequisites:** Locate Lingua Ignota word list (available in published scholarly editions); check KB for any existing analysis

---

## H006: Stolfi Prefix-Midfix-Suffix Decomposition with Per-Slot Entropy
**Priority:** medium
**Status:** tested
**Source:** seeds/llm_conversation_2026_04.md
**Description:** Jorge Stolfi proposed that Voynich words decompose into three positional slots: prefix, midfix, and suffix, each drawing from a restricted character set. Replicate this decomposition on the EVA corpus, then measure entropy separately within each slot. The question: do the high-entropy slots show natural-language-like entropy? If stripping the template slots leaves residual content with h2 ~3–4, the template is adding redundancy to an underlying natural language. If per-slot entropy is uniformly low, the template is the generative mechanism.
**Expected outcome under competing theories:**
- Natural language with templated encoding: midfix (root) slot entropy should be substantially higher than prefix/suffix entropy
- Glossographic/received text: all slots should show low entropy, because the template is the generative process at every level
- Verbose cipher on top of a template: per-slot entropy after collapsing verbose units should approach natural-language levels
**Cost estimate:** medium — requires implementing the Stolfi decomposition heuristic
**Prerequisites:** H001 (positional entropy) recommended first to identify which positions correspond to which slots

---

## H007: Verbose Cipher Reversal — Systematic Grouping Search
**Priority:** medium
**Status:** tested
**Source:** seeds/llm_conversation_2026_04.md
**Description:** Systematically test whether any grouping of adjacent characters into units recovers natural-language-like h2. Test grouping schemes: adjacent pairs, adjacent triples, and class-based groupings (e.g., every gallows character + its following character as a unit). For each scheme, collapse the sequence and measure h2 on the result. A scheme that raises h2 from ~2 to ~3.5 is a candidate verbose cipher grouping. This test is large because the grouping space is combinatorial — start with the most motivated groupings (pairs and gallows-based) before exploring further.
**Expected outcome under competing theories:**
- Verbose cipher: some grouping scheme should substantially raise h2 toward natural-language range
- Templated natural language: no grouping scheme should raise h2 (the entropy is lost to template constraints, not character-level redundancy)
- Hoax: no grouping scheme should raise h2 in a systematic way
**Cost estimate:** medium — manageable if constrained to a small set of motivated groupings
**Prerequisites:** H001 and H003 should run first — if word-initial entropy is already high, verbose cipher is less likely

---

## H008: Gallows-as-Group-Initiator Hypothesis
**Priority:** medium
**Status:** tested
**Source:** seeds/llm_conversation_2026_04.md
**Description:** A specific variant of the verbose cipher hypothesis motivated by paleography. The "gallows" characters (t, k, p, f in EVA and their variants) behave structurally differently from other characters. Test whether treating each gallows character as the start of a bigram unit (gallows + next character → single token) raises h2 or produces a more natural-language-like character distribution. This is a single specific test within the broader grouping-search space of H007, motivated by independent evidence from the writing system itself.
**Expected outcome under competing theories:**
- Gallows-as-initiator: collapsing gallows bigrams should raise h2 and produce distributions resembling natural-language character frequencies
- Gallows as a distinct character class (not group initiator): collapsing gallows bigrams should not substantially change h2
**Cost estimate:** small — a single specific grouping scheme, not a search
**Prerequisites:** none — this is motivated by paleography, not by H007's results; can run before H007

---

## H009: Entropy Comparison — Label Text vs Running Body Text
**Priority:** high
**Status:** tested
**Source:** seeds/llm_conversation_2026_04.md
**Description:** Compare second-order entropy between the short label text (annotations next to illustrations) and the running body text. Labels are under semantic pressure — they must refer to the thing depicted — and should show higher entropy if any part of the manuscript encodes real content. If labels show substantially higher h2 than body text, this supports a "signal embedded in noise" model where labels carry real information and body text is largely generated. If they're the same, the distinction between labeled and unlabeled content may not be meaningful.
**Expected outcome under competing theories:**
- Signal/noise hybrid: label entropy should be higher than body text entropy
- Uniform system (cipher or glossographic): label and body text entropy should be similar
- Hoax: could go either way — hoaxer might vary register between labels and body, or might not
**Cost estimate:** small — requires only identifying label vs. body text regions in the transcription
**Prerequisites:** Verify that the EVA transcription marks label text separately from body text (likely yes — check transcription format)

---

## H010: Word-Initial Entropy Without q-initial Words
**Priority:** high
**Status:** tested
**Source:** exp_001_word_initial_entropy
**Description:** 15.5% of Voynich words begin with 'q', almost exclusively in the context 'qo' (q followed by o at word onset). This is a massively constrained sub-pattern. Test whether stripping all q-initial words from the corpus changes H_initial substantially. If H_initial rises to ~3.5–4.0 bits after removing q-initial words, then the q-initial slot is a structurally special marker that acts like punctuation or a grammatical prefix, and the underlying word-initial diversity is natural-language-like. If H_initial stays at ~3.1 after removal, the constraint is not explained by q-initial alone.
**Expected outcome under competing theories:**
- Slot grammar / constructed language: stripping q-initial words should raise H_initial substantially, because q is filling a special slot
- Natural language in cipher: same as above — 'q' maps to a high-frequency grammatical marker (article, preposition?) that happens to precede a specific set of words
- Hoax: q-initial frequency is arbitrary and removal should not produce a clean change
**Cost estimate:** trivial
**Prerequisites:** none — uses same corpus as exp_001

---

## H011: Onset Constraint Relative to Unigram (Positional Bias Index)
**Priority:** medium
**Status:** tested (exp_027) — CONFIRMED: final position bias=1.482 bits (most constrained), position 1 bias=0.774 > position 0 bias=0.751. Suffix gradient (1.48→0.99→0.61) steeper than prefix gradient (0.75→0.39→0.24). All positions more constrained than natural languages.
**Source:** exp_001_word_initial_entropy
**Description:** Voynich word-initial entropy (3.137) is 0.734 bits below the shuffled-within-word control (3.871), meaning onsets are substantially more constrained than a random draw from the character pool. Natural languages show little or no such bias (Latin: ~0.10 bits, Italian: ~0.00 bits). Define a "positional bias index" = shuffled_H_initial - actual_H_initial, and compute it for positions 0, 1, 2, ... within words. This extends H001 (positional entropy) with a normalized measure that controls for overall character distribution.
**Expected outcome under competing theories:**
- Slot grammar: high bias at onset (slot 0), sharp drop at positions 1-2 (mantle/core), then high again at suffix positions
- Natural language: low bias across all positions
- Glossographic: high bias across all positions
**Cost estimate:** small (extends exp_002 natural progression)
**Prerequisites:** H001 positional entropy (exp_002)

---

## H012: Character Distribution at Core/Inner Positions (3-4 from start)
**Priority:** high
**Status:** tested (exp_029 sub-test): pos 3: e(20.4%), i(10.4%), o(9.7%), a(9.4%), d(9.0%) — vowel-like chars dominate. Entropy 3.606 bits (vs Latin 3.842). pos-3 and pos-4 distributions distinct from suffix. No clear source language consonant pattern identified at these positions.
**Source:** exp_002_positional_entropy
**Description:** Positions 3-4 from word start are the freest slots in Voynich words (lowest positional bias: +0.237 bits) and are where the Stolfi core (gallows characters) typically sits. Characterize the full character distribution at these positions. Do the characters at positions 3-4 resemble any known language's consonant or vowel inventory? Compute the most common characters at pos 3, pos 4, and compare to root consonants of candidate languages (Latin, Italian, Arabic, Hebrew). If the inner-slot character set is small and language-like, this is the strongest constraint on what underlying language the cipher might encode.
**Expected outcome under competing theories:**
- Natural language in cipher: pos 3-4 characters form a language-like consonant/vowel set; comparison to candidate languages might identify the source language family
- Constructed artificial language: pos 3-4 characters are a deliberately chosen subset, possibly arbitrary
- Slot grammar without semantic content: pos 3-4 characters are drawn from whatever glyphs were assigned to the "core" slot
**Cost estimate:** trivial
**Prerequisites:** exp_002 (done)

---

## H013: "qo" as a Single Token — Bigram Onset Analysis
**Priority:** medium
**Status:** REFUTED as article/particle (exp_031): qo-stripped stems H_initial=1.931 bits (LOWER, not higher, than non-qo words at 3.027). Stems 60.5% k-initial, 21.2% t-initial (KL=2.96 bits from free words). qo is a morphological prefix selecting k/t-initial word class, not a free-floating article. 52.6% of stems exist as free words. H032 generated (complementary distribution test). F037 added.
**Source:** exp_002_positional_entropy
**Description:** Q is followed by 'o' in 97.7% of cases at word onset. If "qo" functions as a single onset unit (like a digraph), treating it as one token changes the effective word-initial distribution. Strip all leading "qo" from words (leaving the remainder), recompute H_initial and H2, and compare. If the "true" onset (after qo) has higher entropy, qo is a prefix particle or article that precedes content words. If entropy stays low, qo removal makes no fundamental difference.
**Expected outcome under competing theories:**
- Grammar particle/article: stripping qo should reveal higher-entropy word stems underneath
- Digraph onset slot: entropy should remain about the same after stripping
**Cost estimate:** trivial
**Prerequisites:** none

---

## H014: daiin Frequency and Distribution — Body-Specific Marker or Universal?
**Priority:** high
**Status:** tested
**Source:** exp_003_label_body_entropy
**Description:** 'daiin' is the most frequent body text word (710 occurrences, 2.4% of body tokens) but appears not to feature in label vocabulary. Test directly: count 'daiin' in labels, circular text, and rider text. If daiin appears ≤1% in non-body text, it is a body-specific feature. Then check: which manuscript sections does it concentrate in? Does it appear equally in Currier A and B? A word this frequent that is section/register-specific is either a grammar word specific to body prose syntax, or a filler/padding word, or carries body-specific content. This discriminates between the three models.
**Expected outcome under competing theories:**
- Body-specific grammar word: daiin appears in both A and B body text but rarely elsewhere
- Padding/filler: daiin appears uniformly across body text regardless of section
- Content word: daiin concentrates in specific sections (herbal only, or balneological only)
**Cost estimate:** trivial
**Prerequisites:** none

---

## H015: ot-/ok- Label Words — Section Distribution
**Priority:** medium
**Status:** tested
**Source:** exp_003_label_body_entropy
**Description:** Label words with 'ot-' or 'ok-' initial bigrams (otedy, oky, otaly, okal, okol, otal) dominate the label vocabulary. Test whether these words cluster in specific manuscript sections (herbal labels vs astronomical labels vs biological labels) or are uniformly distributed. Section-specific clustering would suggest these are content words naming section-specific objects; uniform distribution would suggest they are generic label words (like "genus," "figure," "note").
**Expected outcome under competing theories:**
- Content labels: strong section clustering
- Generic structural labels: uniform distribution
**Cost estimate:** small — requires locus codes parsed by section
**Prerequisites:** Section-level parsing of ZL3b (feasible — folio ranges are known)

---

## H021: ZL3b L0 Structural Audit — Classify All L0 Entries by Functional Type
**Priority:** high
**Status:** COMPLETE (exp_022 + exp_032): L0 audited (160 entries; 9 TRUE_LABEL, 43 LINE_MARKER, 108 LIST_ENTRY). Non-L0 label loci (Lf/Lz/Ls/Lc/Ln/Lt) are clean — 0% single-char, 100% section-specific, ~732 total true labels. Clean label corpus established. F038, F039 added.
**Source:** exp_011_single_char_validation
**Description:** ZL3b L0 locus code conflates at least three distinct structural types: (1) true object labels near illustrations, (2) line margin markers alternating with body text (discovered in f49v), (3) list/table column entries (discovered in f66r). This conflation invalidated 83% of exp_010's herbal label analysis. A systematic audit of all L0 entries across all folios is needed to: (a) determine what fraction of L0 entries fall into each category, (b) produce a cleaned label-only subcorpus for reliable analysis, (c) identify other folios with line-marker or list structures. Diagnostic criteria: line-marker pattern = L0 entry immediately precedes a P0 entry (alternating); list/table pattern = multiple consecutive L0 entries with no intervening P0; true label = L0 entry with no adjacent P0 (standalone or with illustration context).
**Expected outcome:** A classification of all ~1,065 L0 tokens that enables reliable label analysis. May also reveal other folios with unusual structural features (more f49v-like or f66r-like pages).
**Cost estimate:** medium — systematic pass through full ZL3b with pattern matching
**Prerequisites:** none

---

## H016: Verbose Cipher Source Language h2 Target — Arabic/Hebrew/German
**Priority:** medium
**Status:** tested
**Source:** exp_007_verbose_cipher_control
**Description:** The control test established that if Voynich is a fixed-filler adjacent-pair verbose cipher, its source language must have h2 ≈ 3.836 bits. Latin (3.509) and Italian (3.411) are both too low. Test: what is h2 for unvoweled Arabic and Hebrew? These are two natural language candidates that could plausibly have h2 in the 3.5-4.0 range (Arabic without diacritics, Hebrew without nikkud). If either matches 3.836 ± 0.1 bits, it becomes a candidate source language. This connects to the Reddy/Knight abjad hypothesis in the KB.
**Expected outcome:** If Arabic unvoweled h2 ≈ 3.836, the abjad hypothesis gains support. If not, the fixed-filler verbose cipher interpretation is further constrained.
**Cost estimate:** small — need Arabic/Hebrew corpora; computation is trivial
**Prerequisites:** Acquire Arabic/Hebrew text corpora (not yet downloaded)

---

## H022: f66r Column 2 Lists "Atomic" (Non-Compound-Forming) EVA Characters
**Priority:** medium
**Status:** tested (exp_025) — PARTIALLY SUPPORTED (p=0.063, marginal): compound-rate vs col2 anti-correlation in right direction but not significant. 'c' (compound_rate=0.995) is IN col2; 'k' (rate=0.084) is absent. Reformulation: col2 lists compound-INITIATING chars (c,s) + standalone chars, excluding compound-COMPLETING chars (h,n).
**Source:** exp_012_f66r_alphabet_test
**Description:** The characters present in f66r column 2 (o, y, d, c, l, r, s, t, f, p, x plus sh) are precisely those that typically stand alone or form bounded units. The characters absent (e, h, a, i, k, n, q) are precisely those that frequently fuse into compound clusters (ee, ch, sh, aiin, ck, etc.). This pattern is too clean to be coincidental. Test: does the set of "compound-forming" EVA characters have a statistically significant anti-correlation with column 2 membership? If so, column 2 may be a list of graphically atomic or compound-resistant glyphs — a subset of the writing system that represents simple, non-ligated forms.
**Expected outcome:** If compound-forming chars are systematically absent, column 2 is a sub-inventory (not a full alphabet) of non-compound-forming units. This would be structurally significant for understanding EVA compound formation rules.
**Cost estimate:** small — requires compound frequency computation per EVA character already done in exp_012
**Prerequisites:** exp_012 (done)

---

## H023: f57v Circular "Key-Like" Text and f66r Column 2 Share @169/@172 and Overlap in Standard Characters
**Priority:** medium
**Source:** exp_012_f66r_alphabet_test, exp_014_prior_work_check, exp_017_cluster_distinctiveness
**Status:** tested (exp_021) — SUPPORTED: overlap significant at p=0.003, Jaccard=0.667, f→@169 adjacency echo; but no positional ordering correspondence
**Reformulation note (exp_017):** The original H023 framing assumed f49v/f57v/f66r form a statistical cluster; exp_017 falsified this. H023 is reformulated to focus on the specific f57v↔f66r connection (shared @169/@172, ZL3b cross-reference) without implying a 3- or 4-folio statistical cluster.
**Description:** f57v's 17-token repeating sequence uses @169;v compound, @170, @171, @172 in fixed positions. f66r column 2 contains standalone @169 and @172 (not @170/@171). The two folios are by different scribes (Hand 1 vs Hand 5), in different sections, yet ZL3b transcribers explicitly cross-referenced them ("cf f57v?" on f66r L38). The shared standard characters between f57v's sequence (o, l, d, r, v, x, k, m, f/p, t, y, I/c) and f66r column 2 (o, y, s, sh, d, f, x, air, c, t, r, l, p) show substantial overlap but not identity. Sub-questions: (a) Does the character overlap between f57v's 17-token sequence and f66r column 2 exceed random expectation? (b) What is the immediate context of @169 and @172 in f66r column 2 compared to f57v's sequence? (c) Could f66r column 2 be a linear sampling from a circular structure exemplified by f57v?
**Expected outcome:** If the overlap significantly exceeds random, the two lists may be related. If at chance, the shared @169/@172 may be coincidental (same glyph ID used for visually similar but functionally unrelated manuscript marks).
**Cost estimate:** small — character overlap computation + context comparison already partially done
**Prerequisites:** exp_012 (done), exp_015 (done), exp_019 (done)

---

## H024: f49v @SPECIAL Glyphs in Line Markers Are the Same Physical Glyphs as f57v Circular Text
**Priority:** medium
**Status:** REFUTED (exp_034): f49v @NNN = {140,192,164,243}; f57v @NNN = {169,170,171,172,255}. Zero overlap. @140 is now identified as numeral "5" (later-hand annotation). f49v @NNN codes are a different physical layer (numerals) from f57v's original Voynich special characters. f49v↔f57v @NNN connection: none.
**Source:** exp_013_line_marker_structure
**Description:** f49v has 6/26 line markers as @SPECIAL glyphs (non-EVA characters). f57v circular text also uses @169, @170, @171, @172. Since f49v is Scribe 1 and f57v is also Scribe 1 (Hand 1, Currier A), these @SPECIAL glyphs may be the same physical glyphs. If the @SPECIAL glyphs in f49v margins correspond to @169/@172 from f57v, then the f49v line marker sequence contains BOTH EVA characters AND the special glyphs from the f57v "key" — making f49v the first discovered folio where the "key-like" glyph set appears in a structural role (margin markers).
**Expected outcome:** Visual comparison of f49v @SPECIAL margin glyphs with f57v @169/@172 would determine if they are the same. A positive identification would strongly link all three key-cluster folios.
**Cost estimate:** small — requires image inspection only
**Prerequisites:** exp_013 (done)

---

## H025: Gallows Characters in Line Markers Function as Section-Level Structural Indices
**Priority:** low
**Status:** cannot test as stated (exp_029 sub-test): f49v and f76r don't have paragraph/section boundaries in their body text — all lines are continuous. The 5 gallows markers (f,k,p,p,k on f49v) are distributed throughout the sequence, not at boundaries. H025 is not supported but also not falsifiable on the available data.
**Source:** exp_013_line_marker_structure
**Description:** f49v line markers show dramatic gallows overrepresentation (f: 16.5x, p: 9.1x corpus rate). f76r shows 's' overrepresentation (8.9x). Gallows characters (t, k, f, p) in the Voynich main text spike at word-position 1, consistent with a structural marking role. If gallows in margin markers serve as section-level labels (e.g., "f" = folio, "p" = paragraph, "k" = key entry), the marker sequence would encode a hierarchical structure invisible in body text statistics. Test: compare gallows marker identity with section-level features of the corresponding body text line (line length, topic, section boundary).
**Expected outcome:** If gallows markers cluster at body text boundaries (section starts, paragraph heads), they may be structural delimiters. If random relative to structure, the overrepresentation is a character-selection artifact.
**Cost estimate:** small — requires body text analysis per marker, mostly done in exp_013
**Prerequisites:** exp_013 (done)

---

## H026: The f57v Repeating Sequence Is 17 Units Per Cycle, with @169 Functioning as a Compound Glyph Including 'v'
**Priority:** medium
**Status:** tested (exp_019) — CONFIRMED: cycle is 4×17 tokens; @169;v is a single compound token bounded by IVTFF dots
**Source:** exp_015_f57v_characterization + exp_018_at_glyph_prior_work
**Description:** Voynich.nu describes the f57v repeating sequence as "4 × 17 characters," while ZL3b tokenization gives 18 tokens per cycle (because @169;v is split at the dot separator). The discrepancy is exactly 1 — consistent with @169 being a compound glyph that incorporates the following 'v' stroke, making the actual repeating unit 17 characters: `o l d r v x k m [f/p @169v] t r @170 @171 y [I/c] @172`. Test: (a) visually inspect the f57v manuscript image at the @169 position to determine if @169 and v are visually fused or separate; (b) check whether ZL3b's own description confirms compound treatment; (c) compare position counts from Zandbergen's folio page (4×17) against our tokenization. If @169 is compound, the cycle is: 8 standard chars, then @169v (1 compound), then 4 chars, then @170, @171, y, [I/c], @172 — a tight 17-unit ring.
**Expected outcome:** If @169;v is a compound, the repeating unit becomes 17, matching voynich.nu. This would mean @169 is a ligature (two-part glyph) and should be treated as a single structural unit.
**Cost estimate:** small — primarily visual inspection of manuscript image
**Prerequisites:** exp_015 (done), exp_018 (done)

---

## H027: The f68r2 Four-Consecutive-@Glyph Sequence (@231-@234) Is a Second Structured @Glyph Group
**Priority:** low
**Status:** FALSIFIED (exp_020)
**Source:** exp_016_at_glyph_census
**Falsification:** exp_020 shows f68r2's @231-@234 are a single concatenated terminus token (`@231;@232;@233;@234;` with no dot separators) at the end of the bottom circular text — structurally opposite to f57v's distributed @glyphs within a repeating cycle. f68r2 does NOT have a repeating structure. The f57v pattern is unique in the manuscript. See X009 in failed_approaches.md.

---

## H028: The Jim Reeds X1-X128 Rare Character Document Identifies the Physical Glyphs for @169, @172, @195
**Priority:** medium
**Status:** unresolved (exp_028) — document not publicly accessible; X1-X128 ≠ @NNN (different numbering systems). Reeds document exists in research community but not posted online. ZL3b cross-reference (cf f57v?) provides sufficient warrant for f57v↔f66r link without glyph ID verification. Visual inspection of f57v image is alternative route.
**Source:** exp_018_at_glyph_prior_work
**Description:** Jim Reeds produced a systematic document of rare Voynich characters, designated X1-X128, which covers the non-standard EVA glyphs. This document would identify what manuscript glyphs correspond to @NNN codes (ASCII values 130-255). If located, it would: (a) name the physical glyph @169 represents; (b) show whether @169 and @172 on f57v vs f66r are the same physical character or coincidentally assigned the same code; (c) clarify the @169;v compound question. Test: search voynich.nu, Reeds's archived papers (via Wayback Machine or university archives), and voynich community resources (voynich.ninja forum) for the Reeds X-character document or any equivalent enumeration.
**Expected outcome:** The document either exists and is findable (resolving the glyph identity question) or has been lost/unpublished (leaving the question open but quantifying the gap).
**Cost estimate:** small — web search and archive check
**Prerequisites:** exp_018 (done)

---

## H029: The f49v Margin Numerals 1-5 Are Latin-Script Digits That Were Added by a Different Hand
**Priority:** low
**Status:** RESOLVED (exp_030): ZL3b comment confirms "1 2 3 4 5" sequence at lines 2-6, encoded as L0 entries o=1, r=2, y=3, e=4, @140=5. These are later-hand Arabic numeral annotations, NOT original Voynich content. @140 = numeral "5". @NNN codes do NOT form a counting system (irregular gaps). Cross-paragraph L0 alignment 0/13. F036 added.
**Source:** exp_018_at_glyph_prior_work + exp_013_line_marker_structure
**Description:** Voynich.nu documents "numbers 1-5 written to the left of lines 2-6" on f49v alongside the Voynich character margin sequence.

---

## H030: f75v and f76r Line-Marker Sequences Are Parts of a Longer Hand 2 Sequence
**Priority:** medium
**Status:** FALSIFIED (exp_026 sub-test): only f75v and f76r among 46 Hand 2 folios have L0 markers. The two sequences are complete; no third folio extends them. Combined inventory {d,k,l,o,q,r,s} = 7 chars is the full Hand 2 marker vocabulary. Bonus finding: f75v|f76r are inner opening of a bifolium (f75v verso ↔ f76r recto).
**Source:** exp_026_f75v_line_markers
**Description:** f75v (6 markers: s,l,l,o,r,s) and f76r (9 markers: s,d,q,s,o,l,k,r,s) are both by Hand 2, biological section, Currier B. f75v's char set {l,o,r,s} is a proper subset of f76r's {d,k,l,o,q,r,s}. If the two sequences are parts of a longer single sequence, the combined char set {d,k,l,o,q,r,s} = 7 distinct characters. Test: (a) Are there other Hand 2 biological folios with L0 line markers? (b) If the sequences are concatenated or interleaved, does a pattern emerge? (c) Is there any 7-element inventory in the manuscript that matches {d,k,l,o,q,r,s}?
**Expected outcome:** Either a longer sequence is discoverable, or the two folios' sequences are independent (like f49v vs f76r). The 7-char combined set may or may not be meaningful.
**Cost estimate:** small — systematic L0 check for Hand 2 bio folios (f70-f84 range)
**Prerequisites:** exp_026 (done) These numerals are NOT captured as @SPECIAL in ZL3b's machine-readable content (the @SPECIAL markers in f49v are @140, @164, @192, @243 — not numerals). This suggests the numerals are either: (a) a separate extraneous annotation not in ZL3b (like the zodiac month names or Jacobus ex libris), (b) encoded as @NNN themselves (possibly @164 is the numeral sequence), or (c) visible in the manuscript image but not transcribed. Test: (a) inspect the f49v manuscript image for the numerals; (b) check if any @NNN code in f49v corresponds to numerals; (c) cross-reference with ZL3b's transcription metadata for f49v. If the numerals are a later addition by a different hand, they could be a reader's annotation rather than original text.
**Expected outcome:** Either the numerals are the @NNN markers (explaining some of the @SPECIAL tokens) or they're a separate layer. The former would resolve the @140/@192/@243 identity question for f49v.
**Cost estimate:** small — image inspection + ZL3b metadata check
**Prerequisites:** exp_013 (done), exp_016 (done)

---

## H032: qo-Words and Their Stem-Equivalents Are in Complementary Distribution by Line Position or Section
**Priority:** medium
**Status:** NOT SUPPORTED (exp_033): Distribution is NOT complementary. Both forms coexist in same dialects/sections. qo-forms are 2.3x more A-absent (88% B vs 11.6% A); bare forms 72.7% B vs 26.6% A. Section: qo=39% bio/14% herbal; bare=18% bio/37% herbal. Line position differences <3%. qo is a DIALECTAL MARKER for B/bio vocabulary, not a grammatical alternant. F040 added.
**Source:** exp_031_qo_stripping
**Description:** 52.6% of qo-stripped stem types appear as independent free words (e.g., both "qokeedy" and "keedy" exist). If qo marks a grammatical inflection (case, number, aspect), the qo-form and the bare form should appear in different syntactic positions (e.g., qo-form is line-medial, bare form is line-final) or in different sections. If they're randomly distributed, qo may be a cipher artifact or phonotactically determined variant rather than a grammatical marker.
**Expected outcome:**
- Grammatical inflection: complementary positional/sectional distribution
- Phonotactic conditioning: no distribution difference, qo-form appears wherever stem-form appears (cipher artifact possibility)
- Dialectal: one form dominates in A, other in B
**Test:** For the top 20 qo/bare stem pairs (e.g., qokeedy/keedy), compute: (a) position-in-line distribution (word-initial, medial, final), (b) Currier A/B frequency, (c) section (herbal/bio/pharma/astro/cosmo) frequency.
**Cost estimate:** medium — requires parsing positional data per token
**Prerequisites:** exp_031 (done)

---

## H033: Labels Are Dominated by an 'ot-/ok-' Prefix Morpheme — Is 'o' a Label-Specific Onset Marker?
**Priority:** medium
**Status:** SUPPORTED (exp_037): 'o' is a label-form morpheme. 64.3% of o-initial label words have their body (o-stripped) in body vocabulary. Section-invariant 2.5-3.3× higher o-initial rate than body text. KL of o-bigrams=0.154 bits (similar distribution). F044 added.
**Source:** inline analysis + F043 + exp_010
**Description:** 58.4% of object labels (Lf+Ls+Ln+Lt) begin with 'o', compared to 20.5% in body text. 'q'-initial words (16.3% of body) are nearly absent from labels (1.9%). The ot-/ok- subtype is known from exp_010 to concentrate in specific sections. H033 asks: is 'o' in label-initial position a GRAMMATICAL MORPHEME (a label-marker particle), or does it reflect the fact that labeled objects all start with 'o'-type vocabulary? Test: (a) check if label-initial 'o' is followed by specific characters (especially t/k/l), (b) compare ot-label initial distribution across sections, (c) check if body text o-initial words cluster in same sections as labels.
**Expected outcome:** If 'o' is a label prefix, it should appear before varied content (ot-, ok-, or-, ol- all common). If labels just happen to use o-type vocabulary, the o-initial rate should match the relevant section's body text.
**Cost estimate:** small
**Prerequisites:** exp_032 (done), F043 (done)

---

## H034: The -edy/-ain Paradigm in Currier B Is a Grammatical Inflectional System
**Priority:** medium
**Status:** PARTIALLY SUPPORTED (exp_038): 384 stems with 2+ suffix variants; 311 have edy/ain/aiin variants. qok stem alone has 9 forms (1559 tokens). -ain more line-final (8%, chi²=5.8 vs -edy 6%), -aiin more line-initial (14.2%). Section: -aiin in S-section (57%), -edy in bio (42%). Positional complementarity is weak (all forms ~80% medial). F045 added.
**Source:** exp_005_currier_ab_comparison, exp_023, F035
**Description:** Currier B's top vocabulary is dominated by -edy suffix words (chedy=478, shedy=411, qokeedy=293, qokedy=261) and -ain suffix words (qokain=270, qokaiin=238). Both paradigms use the same base words with different suffixes (-edy vs -ain vs -aiin). This looks like grammatical inflection. H034 tests whether -edy/-ain/-aiin are truly in complementary distribution (different syntactic environments) or freely alternating.
**Expected outcome:** If -edy/-ain are grammatical, they should show positional complementarity (e.g., -edy in medial position, -ain in final position). If arbitrary alternants, positions should be similar.
**Cost estimate:** medium
**Prerequisites:** exp_033 (qo complementary distribution, done — same methodology)

---

## H035: Folio-Level Vocabulary Diversity Shows Outlier Folios with Unusually Restricted or Diverse Vocabulary
**Priority:** low
**Status:** CONFIRMED (exp_039): Bio mean TTR=0.552 (lowest), herbal=0.835 (highest). f48r/f96v TTR=1.000 (all-unique). f76r TTR=0.466 (lowest in MS, z=-1.7). All high-TTR outliers are herbal; all low-TTR outliers are Currier B. F046 added.
**Source:** exp_017 + accumulated section findings
**Description:** Manuscript-wide vocabulary variation is documented at section level, but not at folio level. Some folios may be statistical outliers (very restricted vocabulary suggesting formulaic text, or very diverse suggesting unique content). Test: for each folio with sufficient tokens (>50), compute TTR and H2. Identify top outliers above/below the section mean.
**Cost estimate:** small
**Prerequisites:** none

---

## H040: Currier A Has a Structural Parallel to B's -edy/-ain Suffix Paradigm
**Priority:** high
**Status:** STRONGLY SUPPORTED (exp_040): A has 349 multi-suffix stems; same core stems (ch,sh,ot,ok) appear in both dialects with opposite suffix preferences (A: -ol/-or dominant; B: -edy/-eedy dominant). cth- in A is a prefix morpheme parallel to qo- in B (H_initial drops 3.061→1.966 after stripping; KL=2.281 bits). F047 added.
**Source:** working_model.md Phase 2 synthesis (2026-04-09)
**Description:** Currier B's 9-form suffix paradigm is the most striking morphological regularity found to date. Currier A has its own distinctive vocabulary (cthy, cthol, cthor, daiin, chor, chol) but no suffix analysis has been run on it. H040 tests whether A words also decompose into stem + suffix families, with a small set of high-productivity stems taking multiple suffix variants. The cth- cluster in A could be a prefix (parallel to B's qo-) or could be a stem class (c-gallows-h = a specific morpheme). Test: apply the same suffix_group() function from exp_038 to Currier A body text. Measure: (a) how many stems have 2+ suffix variants, (b) which suffixes are A-specific vs shared with B, (c) whether the cth- cluster distributes as a prefix morpheme (applies to varied stems) or a stem root (combines with varied prefixes/suffixes).
**Expected outcome under competing models:**
- If A has its own suffix paradigm: A morphology is parallel to B, same system different lexicon — suggests two dialects of one language
- If A vocabulary is morphologically unsystematic: A and B are genuinely different systems (not dialects)
- If A has the same suffixes as B (but different stems): surface vocabulary differs but morphological system is shared
**Cost estimate:** small (same methodology as exp_038)
**Prerequisites:** exp_038 (done)

---

## H041: The 9-Form Suffix Paradigm Is Productive — Rare Stems Predict Suffix Counts
**Priority:** high
**Status:** CONFIRMED (exp_041): Log-linear Pearson r=0.830(B)/0.891(A) between stem frequency and paradigm completeness. KL from marginal=0.2-1.1 bits (partially productive, consistent with NL inflection). Singletons are sparse samples, not fixed mono-suffix forms. F048 added.
**Source:** working_model.md Phase 2 synthesis (2026-04-09)
**Description:** The 384-stem paradigm discovered in exp_038 could reflect either (a) a productive generative grammar where any stem can take any suffix, with low-count stems just lacking evidence, or (b) a fixed lexical list where the 384 stems are the complete vocabulary and each suffix form is individually memorized. Distinguishing these has major implications: productive grammar suggests encoding of a natural language; fixed lexical list suggests a constructed vocabulary. Test: for stems with exactly 1 observed suffix variant (the "singleton" stems), measure the observed frequency distribution. Under productivity, their "missing" suffix forms should appear at very low frequency (1-2 tokens each), consistent with sparse sampling of a productive paradigm. Under the lexical-list model, missing forms should be completely absent (exactly 0 tokens). Also test: does stem frequency predict number-of-suffix-variants? Under productivity, more frequent stems will show more variants simply because sampling is deeper.
**Expected outcome:** Pearson r between stem frequency and suffix variant count > 0.5 would support productivity (frequency drives paradigm completeness, not intrinsic stem class). Near-zero r would suggest paradigm completeness is lexically fixed.
**Cost estimate:** small (use exp_038 data + additional pass on low-frequency stems)
**Prerequisites:** exp_038 (done)

---

## H042: The o-Label Morpheme Distribution Correlates with Section, but Not with qo-Distribution
**Priority:** medium
**Status:** tested — STRONGLY SUPPORTED (exp_048: 10/13 (77%) of o-stems are also qo-stems; both select k/t-initial stem class; parallel register morphemes confirmed)
**Source:** working_model.md Phase 2 synthesis (2026-04-09)
**Description:** Both 'o' (label morpheme) and 'qo' (Currier B body-text prefix) attach to shared stem vocabulary. H042 tests whether the same stems that appear as qo+stem in body text appear as o+stem in labels, and whether section mediates this relationship. The structural parallel (both are prefix + body-stem) could mean: (a) 'o' = "label register version of qo-" — the same underlying morpheme in two registers, (b) 'o' and 'qo' are independent morphemes that happen to attach to similar stems, or (c) they co-occur on the same folios (section governs both). Test: for the top-50 qo-stems (keedy, kain, kaiin, kal, etc.), check whether the label vocabulary contains o+same_stem (okeedy, okain, etc.). Measure co-occurrence rate. Also compare section distribution of 'o'-initial labels vs qo-words in body text.
**Expected outcome:** If 'o' and 'qo' attach to the same stems: stem class is shared; the morphemes select the same vocabulary base. If they attach to different stems: 'o' and 'qo' select different vocabulary registers, suggesting they're not parallel morphemes.
**Cost estimate:** small
**Prerequisites:** exp_031 (qo-stripping data), exp_037 (o-label data)

---

## H043: Word N-gram Repetition Rate Varies by Section — Bio Has Highest Cross-Folio Repetition
**Priority:** medium
**Status:** tested — SUPPORTED (exp_043: bio 6.0 bigrams/folio-pair vs herbal 0.2; bio 30× more formulaic; only 0.24% trigrams cross-folio)
**Source:** working_model.md Phase 2 synthesis (2026-04-09)
**Description:** The 9-form suffix paradigm and section-level TTR patterns suggest Bio section is structurally the most repetitive. H043 measures not just within-folio repetition (TTR) but CROSS-FOLIO repetition: what fraction of consecutive 2-gram (bigram) and 3-gram (trigram) word sequences on one folio also appear on a different folio in the same section? High cross-folio repetition suggests formulaic text (repeated phrases, templates, or reused passages). Low cross-folio repetition with low TTR could mean word repetition is single-word (the same individual words repeat) but phrases are unique. Test: for each section, compute the fraction of within-section folio pairs that share at least one word bigram, and the mean number of shared bigrams.
**Expected outcome:** If Bio is formulaic: Bio section will have the highest cross-folio bigram sharing rate. If labels are formulaic: astro/pharma labels may share phrase templates. The herbal section (highest folio TTR) should have the LOWEST cross-folio bigram overlap.
**Cost estimate:** medium (requires bigram extraction + pairwise folio comparison)
**Prerequisites:** none (direct from corpus)

---

## H044: Currier A cth- Cluster Functions as a Prefix Morpheme Parallel to B's qo-
**Priority:** medium
**Status:** tested — STRONGLY SUPPORTED (exp_040: H_initial drops 3.061→1.966 after stripping; KL=2.281 bits; selects o/y/e-initial stems; parallel structure to qo- confirmed)
**Source:** working_model.md Phase 2 synthesis (2026-04-09)
**Description:** The Currier A vocabulary is dominated by cth- initial words (cthy=85, cthol, cthor, qotchy) that are near-absent in Currier B. These structurally resemble the qo- prefix in B: they are a small cluster of heavily used words that all share an initial morpheme. H044 tests whether cth- is a morphological prefix in A. Test: (a) strip 'cth' from cth-initial A words and check if the resulting stems appear in A's free vocabulary, (b) measure KL divergence between cth-stripped stem initials and non-cth A word initials (parallel to exp_031's qo analysis), (c) check if cth-words avoid the same line positions that qo-words favor in B. If cth- is A's equivalent of B's qo- prefix, this would suggest both dialects share a "obligatory prefix class" mechanism even though the actual morphemes differ.
**Expected outcome:** If cth- is a prefix: stripped stems (hy, ol, or...) appear in A free vocabulary; KL between stem initials and free word initials is low. If cth- is a stem root: stripped residues are not valid free words; KL is high.
**Cost estimate:** small (same method as exp_031)
**Prerequisites:** exp_031 (done)

---

## H050: Scribal Hand Variation in qo-Morphology Rate — Do Hands 1–5 Differ Systematically?
**Priority:** high
**Status:** PARTIALLY SUPPORTED (exp_044): Hand 4 outlier: qo=5.9% (vs 18-21% for Hands 2-3), -edy=0.4%, -ol=8.3% — resembles Currier A. Hand-section confound is strong. Within-Hand 2 qo-rate std=0.090 (content-driven more than hand-driven). H056 generated. F051 added.
**Source:** working_model.md Phase 3 gap-hunting (2026-04-09)
**Description:** qo- prefix rate varies across sections (bio=19.4%, herbal=11.1%) and correlates with Currier B. But section and hand are confounded: Hand 1 writes primarily Currier A herbal; Hands 2-5 write primarily Currier B sections. H050 attempts to decompose: within the same section, do different hands show different qo- rates? ZL3b $H= field assigns a hand number (1-5) to each folio. For folios in the bio section written by the same Currier dialect, measure qo-rate per hand. If hands vary independently of section/dialect, qo- has a scribal component. If hands don't vary within section+dialect combinations, qo- is entirely explained by section or dialect.
**Expected outcome:** If qo-rate is a hand feature: Hand 2 and Hand 3 (both bio section) will have measurably different rates. If qo- is section-driven: hands within the same section will show no difference. The result constrains whether the morphological system is stable across different scribes (language feature) or variable (idiolect/scribal habit feature).
**Cost estimate:** medium (requires per-folio hand metadata join with token data)
**Prerequisites:** exp_031 (qo data), exp_033 (positional data)

---

## H051: Quire Structure Predicts Morphological Features Better Than Section Labels
**Priority:** high
**Status:** tested — NOT SUPPORTED (exp_047: Section F-ratios higher than Quire F-ratios for all features; section is primary organizing variable)
**Source:** working_model.md Phase 3 gap-hunting (2026-04-09)
**Description:** The manuscript is organized into physical quires (gatherings of folios, labeled A-R in ZL3b via $Q= field). Section labels (herbal, bio, astro, etc.) reflect content; quire labels reflect physical production order. If morphological features (qo-rate, suffix type, TTR) cluster by quire rather than by section, this would suggest the text was generated/copied in quire-sized batches with consistent scribal practice per quire. H051 measures: for each quire, compute (a) qo-rate, (b) mean suffix distribution (-edy vs -ain vs -aiin fractions), (c) mean folio TTR. Then test whether quire explains more variance than section in each measure. If quire > section: physical production order matters more than content category. If section > quire: content register drives morphology.
**Expected outcome:** Neither pure quire nor pure section effects — likely partial confound since quires and sections overlap. But if quire-level variation is substantial, this opens a line of evidence about manuscript production sequence.
**Cost estimate:** medium (requires $Q= field parsing + per-quire statistics)
**Prerequisites:** exp_033, exp_038, exp_039 data

---

## H052: Cross-Folio Exact-Phrase Repetition — "Parallel Passages" in Voynich
**Priority:** high
**Status:** SUPPORTED (exp_043): Bio section 6.0 shared bigrams/pair (30× herbal's rate). Only 0.24% of trigrams cross-folio (overwhelmingly unique at phrase level). bio↔special most cross-section connected (1,404 bigrams, 17 trigrams). Most widespread bigram: "chol daiin" on 24 folios. F050 added.
**Source:** working_model.md Phase 3 gap-hunting (2026-04-09)
**Description:** If Voynich text is formulaic (same templates repeated), we expect to find identical or near-identical sequences of words appearing on multiple folios. This is known as "parallel passages" in manuscript studies. Beyond 9-form suffix paradigm word repetition, H052 looks for repeated 3-gram and 4-gram word sequences that appear on 2+ distinct folios. Known parallel-passage candidates: f49v's L0 sequence (already shown to NOT align with f76r); zodiac folios may repeat structural formulas. Test: extract all word trigrams from body text; for each trigram appearing on 2+ folios, record the folio pairs and section context. Are the same-section trigrams the most repeated? Are any trigrams repeated across different sections (suggesting cross-section formulaic linking)?
**Expected outcome:** High within-section trigram repetition (especially bio section, highest cross-folio TTR expectation from exp_039). Low cross-section repetition. Any cross-section repetition is especially interesting.
**Cost estimate:** medium (trigram extraction + folio-pair matrix)
**Prerequisites:** exp_039 (done)

---

## H053: Per-Folio Label Vocabulary Correlates with Per-Folio Body Vocabulary
**Priority:** medium
**Status:** PARTIALLY SUPPORTED (exp_046): 60% of folios have zero label-body overlap (formulaic register). 40% with above-chance overlap use o-prefix words (morphological relationship, not content). Pharma labels completely formulaic (median ratio=0.00). F053 added.
**Source:** working_model.md Phase 3 gap-hunting (2026-04-09)
**Description:** For folios with both labels (Lf/Ln/Lt/Ls) and substantial body text, do the label words predict the body word distribution on the same folio? If labels name the illustrated objects and body text describes them, we'd expect label stem vocabulary to show elevated frequency in the body text of the same folio (co-occurrence). If labels are formulaic (standard names regardless of body content), label-body correlation per folio would be low. Test: for each folio with ≥5 label tokens AND ≥30 body tokens, compute the Jaccard similarity between label word types and body word types. Compare to the expected Jaccard given the folio's label size and body size (random null). Is there a per-folio correlation (label vocabulary predicts same-folio body vocabulary) that exceeds the manuscript-wide baseline?
**Expected outcome:** Pharma section (Lf labels, f88-f102) is the best candidate for high correlation if label = plant name and body = recipe/use. Astro labels (Ls) may show low correlation if labels are constellation names and body text is general astronomical prose.
**Cost estimate:** medium (per-folio label + body token extraction)
**Prerequisites:** exp_032 (clean label corpus)

---

## H054: The f76r "Key-Like Sequence" Has Higher Within-Sequence Bigram Repetition Than Normal Bio Text
**Priority:** medium
**Status:** NOT SUPPORTED (exp_042): f76r body text max ACF ratio=1.85 (below 2.0 threshold). Low TTR from high frequency of standard Currier B words (shedy/chedy/chey). "Key-like" refers to L0 line markers only. Bonus: f84v and f75v both peak at lag=13 (ratios 2.30/2.22***). F049 added.
**Source:** working_model.md Phase 3 gap-hunting (2026-04-09)
**Description:** f76r has the lowest TTR in the entire manuscript (TTR=0.466, exp_039). Its low TTR means its words repeat heavily — but WHY? Two models: (a) f76r contains a small vocabulary cycling through a fixed template (like f57v's 4×17 cycle), or (b) f76r contains normal Bio text that happens to use fewer word types because it repeats a fixed subject matter. H054 tests: does f76r have a periodic word-level structure (like f57v's 17-cycle)? Test: extract f76r body text word sequence; compute word autocorrelation at lags 1-20 (does word[i] predict word[i+k] for some k?). Also compute body line similarity (do consecutive lines share more words than expected by TTR alone?).
**Expected outcome:** If f76r has a cycle: autocorrelation will peak at the cycle period. If f76r is just repetitive Bio text: autocorrelation will be noise at all lags. Given that ZL3b already labeled f76r as "key-like sequence," some structure is expected.
**Cost estimate:** small (autocorrelation on word sequence)
**Prerequisites:** exp_039 (done)

---

## H055: Bio Section Prose Has a Lag-13 Autocorrelation Peak — Possible Paragraph Unit Structure
**Priority:** low
**Status:** tested — PARTIALLY SUPPORTED (exp_049: effect is folio-specific, not section-wide; 3/19 bio folios have ratio>2.0 but bio mean=1.00 at baseline)
**Source:** exp_042_f76r_autocorrelation (bonus finding in f84v and f75v)
**Description:** Both f84v (ratio=2.30***, p≈0.03) and f75v (ratio=2.22***, p≈0.04) show significant word-level autocorrelation at lag=13 in the bio section. This could reflect: (a) bio-section text organized in ~13-word "paragraph chunks" where the same theme word recurs every ~13 positions, (b) a systematic folio-level structural convention for bio pages (numbered items? plant descriptions?), or (c) a sampling artifact at these token counts. Test: compute word autocorrelation for all bio section folios with ≥200 tokens; check whether lag=13 is systematically elevated across the section (vs. random folios). If lag=13 is a bio-section feature, it may reflect the underlying content structure (e.g., each "paragraph" ~13 words, with the topic word appearing at start and end).
**Expected outcome:** If systematic: lag=13 peak appears in ≥5 of the 19 bio folios with sufficient tokens. If random artifact: lag=13 peaks in ~1-2 folios by chance (consistent with 5% alpha).
**Cost estimate:** small (loop the exp_042 analysis across bio section folios)
**Prerequisites:** exp_042 (done)

---

## H056: The Astro/Cosmo Section (Hand 4) Is Morphologically Intermediate Between Currier A and B
**Priority:** medium
**Status:** PARTIALLY SUPPORTED (exp_045): Astro is A-adjacent (qo=0.059 below A=0.110, -edy=0.7% near A=0.2%, -ol=13.8% intermediate). Jaccard: A↔Astro=0.046 > B↔Astro=0.033. But -ey/-eey anomalously above B. F052 added.
**Source:** exp_044_hand_qo_variation (F051)
**Description:** Hand 4 (astro/cosmo folios f67-f70) has Currier B designation but morphological features close to Currier A: qo=5.9% (vs B average 17-21%), -edy=0.4% (vs B average 10-16%), -ol=8.3% (highest of any B hand, approaching A's 17%). H056 tests whether the astro/cosmo section is statistically intermediate between A and B on multiple morphological measures. Test: for the Hand 4 folios, compute (a) vocabulary Jaccard with Currier A vs Currier B bodies, (b) suffix distribution distance to A vs B, (c) word-initial entropy and character distribution. Also test: is the A-like profile a consequence of circular text structure (ring diagrams constrain vocabulary), or is it present in all Hand 4 text regardless of locus type?
**Expected outcome:** If astro/cosmo is intermediate: Jaccard(Hand4, A) > Jaccard(Hand4, B) or approximately equal. If astro/cosmo is B: Jaccard(Hand4, B) > Jaccard(Hand4, A). The former would suggest a three-way dialect distinction (A, B, astro/cosmo).
**Cost estimate:** small (comparative vocabulary analysis on the 9 Hand 4 folios)
**Prerequisites:** exp_044 (done), exp_023 (A/B alignment data)

---

## H057: The Pharma Section's -ol Dominance Reflects Plant-Name/Ingredient Morphology
**Priority:** medium
**Status:** tested — PARTIALLY SUPPORTED (exp_051: pharma -ol driven by -eol suffix variant; NOT a label morpheme (labels show lower -ol than body). F058 added.)
**Source:** exp_047 (F054: pharma -ol=18.5%, highest of any section)
**Description:** The pharma section has -ol as its dominant suffix (18.5% vs herbal 10.4%, bio 7.4%). This section primarily contains labels (plant names, ingredient names: Lf locus TTR=0.956) and short recipe-like body text. H057: The -ol suffix in pharma encodes a "plant/ingredient name" function — the pharmacological register defaults to -ol-terminal words as naming forms. Test: (a) what fraction of pharma body text words end in -ol vs other sections? (b) Do pharma label words also prefer -ol endings (label corpus analysis)? (c) Is -ol elevation in pharma driven by a small set of highly frequent words or distributed across stems?
**Expected outcome:** If -ol is pharma's naming morpheme: pharma labels should also prefer -ol; the elevation should be distributed across many -ol-ending stems. If it's a small cluster: a few high-frequency pharma words (like "chol", "shol") explain the elevation.
**Cost estimate:** small (targeted pharma corpus analysis from existing parse)
**Prerequisites:** exp_047 (done), exp_038 (section suffix distributions)

---

## H058: The Three Prefix Morphemes (qo-, o-, cth-) Form a Morphological System Based on Stem-Initial Class
**Priority:** medium
**Status:** tested — NOT SUPPORTED (exp_052: stem-class suffix split (KL=4.726 bits) is between-dialect effect; within B all stem classes use B-type suffixes. cth- is a stem root, not a prefix. F059 added.)
**Source:** F055 (exp_048) + F047 (exp_040): qo- and o- both select k/t-initial stems; cth- selects o/y/e-initial stems
**Description:** The three confirmed prefix morphemes select complementary stem classes: qo- and o- both select k/t-initial stems (66-82% of their stems), while cth- selects o/y/e-initial stems (o=40%, y=24%, e=20%). H058: This division reflects a deeper phonological or semantic categorization — k/t-initial stems belong to one morphological class (nouns/objects?), and o/y/e-initial stems to another (verbs/actions? or a different noun class). Test: (a) Do qo-stems, o-stems, and bare k/t-initial words have similar suffix distributions (suggesting same grammatical category)? (b) Are cth-stems (o/y/e-initial) different in suffix distribution from qo-/o-stems (k/t-initial)?
**Expected outcome:** If the stem classes have distinct grammatical functions: cth-stems should have systematically different suffix distributions than qo-/o-stems. If the stem classes are arbitrary: suffix distributions will be similar.
**Cost estimate:** medium (requires cross-corpus suffix analysis by stem-initial class)
**Prerequisites:** exp_040 (cth- data), exp_048 (qo-/o- data)

---

## H059: The f75v/f82v/f84v Bathing-Pool Folios Share Distinctive Phrase Structures
**Priority:** low
**Status:** tested — NOT SUPPORTED (exp_055: lag=13 signal is statistical; cross-folio bigram sharing 2-8, indistinguishable from other bio pairs. F062 added.)
**Source:** exp_049 (F056): lag=13 word autocorrelation signal concentrated in these 3 folios
**Description:** The three bio folios with strongest lag=13 autocorrelation signal (f75v=2.22, f82v=2.17, f84v=2.30) all come from the bathing-pool content sequence (bio folios featuring pools of bathing women). H059: These three folios share a structural text pattern — possibly a repeated phrase template at 13-word intervals (e.g., a descriptive sentence about each woman/pool of fixed length) that doesn't appear in other bio folios. Test: extract the specific word sequences that repeat at lag=13 in each folio and check if the same sequences are shared across f75v, f82v, f84v.
**Expected outcome:** If a shared template: the same word sequence should appear at ~13-word intervals on all three folios. If coincidence: the lag=13 peaks reflect different structures in each folio.
**Cost estimate:** small (targeted analysis of those 3 folios)
**Prerequisites:** exp_049 (done)

---

## H060: Currier A daiin Is Morphologically Parallel to Currier B qokain/-ain Words
**Priority:** medium
**Status:** tested — PARTIALLY SUPPORTED (exp_050: daiin IS line-final elevated 1.41×; entire d-stem paradigm marks line endings in A; -ol/-or words excluded from line endings. B -ain is NOT line-final elevated. F057 added.)
**Source:** working_model.md (F012: daiin concentrates in Currier A/Herbal A at 4.11-4.58%); F047 (A has -aiin as irregular high-frequency form like a verb)
**Description:** In Currier A, 'daiin' is the single most frequent word (4-4.5% of tokens), with irregular paradigm behavior (KL=1.077, dominated by -aiin). In Currier B, the paradigm is -ain-terminal words at line-final position (exp_038: -ain 8.0% line-final). H060: 'd'+aiin in A is the functional parallel of qok+ain in B — both encode a high-frequency, potentially grammatical function word (verb? auxiliary? connective?). Test: (a) Is 'd+aiin' in A concentrated at line-final position (parallel to -ain in B being line-final dominant)? (b) What is the daiin positional profile (line-initial, medial, final)? (c) Does 'd' as a bare stem appear in A or only with -aiin suffix?
**Expected outcome:** If daiin is A's functional equivalent of B's qokain: daiin should show line-final preference (A's equivalent of B's -ain=8% line-final). If daiin is neutral: no positional preference.
**Cost estimate:** small (positional analysis of 'd' stem in Currier A)
**Prerequisites:** exp_038 (suffix positional data), exp_041 (productivity data for 'd' stem)

---

## H061: The 'y-' Prefix in Currier A Is a Line-Initial Particle (Analogous to a Definite Article or Sentence-Opener)
**Priority:** high
**Status:** tested — NOT SUPPORTED (exp_054: y-initial is 0% at para-starts; is a CONTINUATION line marker, not sentence-opener. -dy is para-start marker (4.39×). F061 added.)
**Source:** exp_053 (F060: y-initial words are 5-6× enriched at line beginnings; ychor, ycheor, ychol, ycheey all strongly line-initial)
**Description:** In Currier A, words beginning with 'y' followed by 'ch' (ychor, ycheor, ychol, ychey) are 5-6× over-represented at line beginnings. This parallels the EVA 'y' known to function as a word-initial element in many Voynichese words. H061: The prefix 'y-' in Currier A marks sentence-initial position (like a definite article, narrative opener, or quotative marker). Test: (a) What fraction of Currier A lines begin with a 'y-' initial word? (b) Is the 'y-' line-initial effect also present in Currier B? (c) Do 'y-' words cluster specifically at PARAGRAPH beginnings (@P0) vs line beginnings within a paragraph (+P0)?
**Expected outcome:** If 'y-' is a true paragraph/sentence opener: it should concentrate at @P0 lines (paragraph starts) more than +P0 lines. If it's simply a line-initial marker without paragraph-level structure: equal distribution across @P0 and +P0.
**Cost estimate:** small (targeted re-analysis of positional data from exp_053)
**Prerequisites:** exp_053 (done)

---

## H062: The -ain Suffix Is a Sentence-Boundary Marker, Appearing at Both Line-Initial and Line-Final Positions
**Priority:** medium
**Status:** tested — PARTIALLY SUPPORTED (exp_054: -ain is suppressed at para-starts (0.25× A, 0.30× B). -aiin marks para-ENDS (19.5% A, 10.5% B). The boundary marker function is -aiin not -ain. F061 added.)
**Source:** exp_053 (F060: -ain is 1.30× first AND 1.45× last in A; exp_038: -ain 8.0% line-final in B at chi²=5.8)
**Description:** The -ain suffix appears to mark sentence boundaries in both Currier A and B, appearing above baseline at both line edges. H062: -ain marks syntactic boundaries (sentence-initial or sentence-final position) rather than a specific grammatical category (like -edy marking medial content). Test: (a) Do -ain words concentrate at PARAGRAPH beginnings (@P0) and PARAGRAPH endings (=Pt) more than at mid-paragraph lines? (b) Does the line-initial vs line-final split change between @P0 and +P0 lines?
**Cost estimate:** small (re-parse with @P0 vs +P0 distinction)
**Prerequisites:** exp_053 (done)

---

## H063: The y-Initial Line-Opening Correlates with Specific Content/Section
**Priority:** low
**Status:** tested — PARTIALLY SUPPORTED (exp_055: astro=23.2%, pharma=17.9%, bio=7.5% — variation reflects paragraph length, not vocabulary preference. F062 added.)
**Source:** exp_053 (F060): 30% of A lines open with -ol/-or words; 'y-' words are highly enriched at line openings
**Description:** Are the 'y-' initial line openers concentrated in specific herbal sections (e.g., particular folio ranges)? Or are they manuscript-wide? If concentrated in specific sections, the 'y-' particle may be section-specific rather than a general A-dialect particle.
**Cost estimate:** small (per-section 'y-' analysis)
**Prerequisites:** exp_053 (done)

---

## H064: The -dy Paragraph-Start Marker in A Is Also Present in Currier B as a Paragraph Opener
**Priority:** medium
**Status:** tested — PARTIALLY SUPPORTED (exp_057: -dy is 3.36× in A, 1.53× in B; B has stronger markers -chy 2.94×, -ar 2.11×; y-initial completely suppressed in A, 0.28× in B; B suppresses -aiin 0.37× at para-starts unlike A. F064 added.)
**Source:** exp_054 (F061): -dy is 4.39× enriched at para-starts in A; is this also a B-dialect paragraph marker?
**Description:** In Currier A, -dy words appear 4.39× more at paragraph-start first positions than at continuation first positions. H064: Is the -dy paragraph-start function also present in Currier B? If yes: -dy is a cross-dialect paragraph marker. If no: it is A-dialect-specific.
**Cost estimate:** tiny (direct check in exp_054 data using B lines)
**Prerequisites:** exp_054 (done — has B data)

---

## H065: The f6v 38% y-Initial Folio Is Structurally Anomalous (Long Paragraphs or Unusual Text Format)
**Priority:** low
**Status:** tested — NOT SUPPORTED (exp_058: all 75 herbal A folios are single-paragraph; f6v is within normal range rank#2; zero-y-initial cluster of ~12 folios is the real anomaly. F065 added.)
**Source:** exp_055 (F062): f6v has 38.1% y-initial rate (far above A mean ~15%)
**Description:** f6v (herbal, Currier A) has 38.1% of lines starting with y-initial words — the highest rate found. This suggests either (a) f6v has very long paragraphs relative to other herbal folios, (b) the folio has an unusual text layout (e.g., list format where each item continues the previous), or (c) this is a scribal preference specific to the scribe who wrote f6v. Test: how many paragraphs does f6v have? What is its average paragraph length compared to other herbal folios?
**Cost estimate:** tiny
**Prerequisites:** exp_054/055 (done)

---

## H066: The Currier A Line Grammar (3-Tier) Is Disrupted in Specific Folios — Exceptions Reveal Content Boundaries
**Priority:** medium
**Status:** tested — SUPPORTED (exp_059: 6 herbal A folios violate y-initial grammar; violations exclusively in H section; two-register system: y-dominant vs aiin-dominant folios; f35r most extreme. F066 added.)
**Source:** F060-F061: Currier A has rigid 3-tier positional grammar. Folios that violate this grammar (e.g., -ol at line-final, no y-initial lines) may mark structurally different content.
**Description:** If the 3-tier Currier A line grammar (-dy para-open, y-initial continuation, -aiin para-close) is consistent, then folios that violate it strongly may have different scribal hands, damaged text, or content that doesn't follow the standard template. Test: identify Currier A folios where the y-initial, -dy, and -aiin positional biases are REVERSED or absent, and characterize what's different about those folios.
**Cost estimate:** small
**Prerequisites:** exp_053, exp_054 (done)

---

## H067: Voynichese Has a Three-Slot Word Template: [Onset Class] + [Root Class] + [Suffix Class]
**Priority:** high
**Status:** tested — PARTIALLY SUPPORTED (exp_056: onset × suffix KL=0.01-0.32 bits; probabilistic not categorical; d+aiin 2.69× most rigid; top 6×6 covers 48-54%. F063 added.)
**Source:** Synthesis of F060, F061, F047, F057, exp_052: the positional grammar and morphological prefix system together suggest a highly structured word-formation system
**Description:** Based on findings so far: qo-/o-/y- are onset-class markers; k/t vs o/y/e stems are root classes; -ol/-or/-edy/-aiin/-y are suffix classes. H067: Voynichese word formation can be described as: [ONSET: qo/o/y/cth/∅] + [ROOT: k/t vs c/s/o-initial stems] + [SUFFIX: paradigm class]. Test: (a) For each combination of onset × suffix class, what is the observed vs expected frequency? (b) Which onset-suffix combinations are systematically avoided? (c) What percentage of the corpus is accounted for by the top N onset × suffix combinations?
**Expected outcome:** If there is a true template: specific onset-suffix combinations will be dramatically over- or under-represented. If onsets and suffixes are independent: the observed = expected (multiplicative baseline).
**Cost estimate:** medium (requires full cross-tabulation of onset × suffix classes)
**Prerequisites:** exp_040 (qo-), exp_048 (o-), exp_052 (cth-), exp_053 (y-)

---

## H068: The Two-Register Herbal A Folios Differ in Vocabulary, Not Just Positional Grammar
**Priority:** high
**Status:** tested — STRONGLY SUPPORTED (exp_062: Jaccard=0.138 near A/B gap of 0.148; y-onset globally suppressed 0.21×; d/ch/sh enriched in aiin-dom; 447 aiin-exclusive types, 781 y-exclusive types. F069 added.)
**Source:** F066 (exp_059): six herbal A folios have 0% y-initial and elevated aiin-last, forming an "aiin-dominant" register. Are these folios lexically distinct from the y-dominant herbal folios?
**Description:** If the aiin-dominant herbal A folios (f49r, f32r, f8v, f42v, f35r) represent a different scribal hand or content sub-type, they should differ from y-dominant folios not just in positional grammar but in word choice. Specifically: (a) Do aiin-dominant folios use more daiin? More 'a'-initial words? Different suffix distributions overall? (b) What is the vocabulary overlap (Jaccard) between aiin-dominant and y-dominant herbal A folios? (c) Do aiin-dominant folios cluster around any shared high-frequency words not found in y-dominant folios?
**Expected outcome:** If same scribal hand but different grammar: vocabulary should overlap strongly. If different hand: vocabulary will differ, especially in the most common words.
**Cost estimate:** small
**Prerequisites:** exp_059 (done)

---

## H069: y-Initial Rate and daiin Frequency Are Negatively Correlated Across Herbal A Folios
**Priority:** medium
**Status:** tested — PARTIALLY SUPPORTED (exp_060: r=-0.297; aiin-dominant folios have 2× daiin=6.88% vs y-dominant=3.50%; daiin and y-initial appear to be competing continuation strategies. F067 added.)
**Source:** F066 (exp_059): some herbal A folios have 0% y-initial and elevated aiin; F012: daiin concentrates in Herbal A. Are high-daiin folios the same as low-y-initial folios?
**Description:** daiin is the most common Currier A/Herbal word. The y-initial continuation marker and the -aiin suffix may be in competition. Test: across herbal A folios, is the per-folio daiin frequency negatively correlated with the y-initial rate? If daiin concentrates in the aiin-dominant folios (those with 0% y@cont and high aiin-last), this would suggest that daiin is specifically the -aiin continuation marker rather than a general high-frequency word.
**Expected outcome:** Negative correlation if daiin and y-initial are competing strategies; no correlation if they're independent.
**Cost estimate:** tiny (compute per-folio daiin rate vs y-initial rate from existing data)
**Prerequisites:** exp_058, exp_059 (done)

---

## H070: The 'k' and 't' Onset Classes Have Different Suffix Preferences Within the Currier B 'Other' Category
**Priority:** high
**Status:** tested — REFUTED (exp_061: k vs t KL=0.082 bits, nearly identical — same onset class. sh vs ch=0.062 bits also same class. 4 effective onset classes in B: {ch/sh}, {k/t/p}, {d/s}, {qo}. F068 added.)
**Source:** F063 (exp_056): the 'other' onset class (25.6% of B tokens) is heterogeneous; KL=0.033 bits (very low). Disaggregating k-initial vs t-initial words (the two main stem classes identified in qo-stripping, exp_040) may reveal onset-specific suffix preferences invisible in the lumped 'other' category.
**Description:** exp_040 showed that qo-stems are dominated by 'k' (60.5%) and 't' (21.2%) initial stems. The free-word corpus contains many k-initial (keedy, kaiin, kal) and t-initial (taiin, tol, tcheey) words. If k-initial and t-initial words have the same suffix preferences, they're the same morphological class. If they differ (e.g., k-initial prefers -edy while t-initial prefers -aiin), they're distinct classes. This would extend the 3-slot template (exp_056) to include root-class specificity.
**Expected outcome:** If k and t are the same class: overlapping suffix distributions. If different: different suffix preferences that were averaged out in the 'other' category.
**Cost estimate:** small (extend exp_056 by disaggregating the 'other' onset category)
**Prerequisites:** exp_056 (done)

---

## H071: Multi-Paragraph Structure Is NOT Herbal-Specific — Bio and Pharma Folios Have Multiple Paragraphs
**Priority:** medium
**Status:** tested — SUPPORTED (exp_061: Herbal/Special/Text=100% single-para; Pharma=75% multi-para, Cosmo=71%, Astro=50%, Bio=37% multi-para; para count mirrors content complexity. F068 added.)
**Source:** F065 (exp_058): all 75 herbal A folios are single-paragraph. Is this herbal-specific? Or does the single-paragraph structure extend to all sections?
**Description:** If herbal A folios are universally single-paragraph (1 para-start per folio) but bio/pharma/special have multi-paragraph folios, this reveals a structural difference between sections: herbal text is continuous narrative (one plant = one paragraph = one folio), while bio/pharma use a different organizational scheme. Test: how many para-starts per folio across each section? Are some sections uniformly single-paragraph and others multi-paragraph?
**Expected outcome:** Expected herbal = single para (confirmed for A); bio = likely multi-paragraph (shorter formulaic units per exp_055/F062); pharma/special = uncertain.
**Cost estimate:** tiny (direct parse of para-start counts by section)
**Prerequisites:** exp_058 (done)

---

## H072: The Aiin-Dominant Herbal A Folios Cluster in Specific Quires
**Priority:** medium
**Status:** tested — PARTIALLY SUPPORTED (exp_060: Quire F=62% aiin-dominant, D=50%; Quires B/O/Q=0%. Scribal-hand explanation supported but imperfect. F067 added.)
**Source:** F066 (exp_059): f49r, f32r, f8v, f42v, f35r form the aiin-dominant cluster. These folio numbers span f8v, f32r, f35r, f42r, f42v, f49r — are they in the same quires?
**Description:** If the aiin-dominant herbal A folios cluster in specific quires (e.g., quires 3-4 or 6-7), this strongly suggests a scribal hand change: different quires were written by different scribes. Conversely, if they're scattered across many quires, the effect is more likely content-driven (a specific category of plants or botanical descriptions). The quire assignment can be determined from the $Q= field in the transcription header. Mapping the 6 violator folios to quires will test whether the two-register system has a structural (scribal) or semantic (content) origin.
**Expected outcome:** If clustered: scribal hand change hypothesis. If scattered: content sub-type hypothesis.
**Cost estimate:** tiny (look up $Q= field for the 6 violator folios)
**Prerequisites:** exp_059 (done)

---

## H073: B Para-Start p/t-Onset Words Are a Distinct Vocabulary Class with Their Own Morphology
**Priority:** medium
**Status:** tested — SUPPORTED (exp_063: pch=17×, tch=11× enriched at B para-starts; 0/781 in labels; line-last=0.1%; -edy preferred (19-25%); p-onset is B's paragraph-start marker class. F070 added.)
**Source:** F064 (exp_057): B para-start words cluster around p/t-onset forms (pchedar, tchedy, pchedal) that are rare in the general B corpus (0.4-0.9%). These look morphologically distinctive with 'pc-' and 'tc-' onset clusters.
**Description:** In Currier B, the most common para-start opener words are pchedar (×3), tchedy (×3), pchedal (×2). These start with the consonant clusters 'pch' and 'tch' — which are unusual onset combinations not found in the main onset classes (qo-, o-, ch-, sh-, d-, y-). Test: (a) What is the full frequency of 'pch' and 'tch' onset words in the B corpus? (b) Do these words concentrate at para-starts and line-starts, or are they evenly distributed? (c) Are 'pch' and 'tch' words absent from labels? (d) Do they take a distinct suffix distribution (e.g., prefer -ar/-al over -edy/-aiin)?
**Expected outcome:** If they are a dedicated structural vocabulary: concentration at para-starts, distinctive suffix distribution, label absence. If random coincidence: evenly distributed, no suffix specialization.
**Cost estimate:** small
**Prerequisites:** exp_057 (done)

---

## H074: The s-Initial Onset Class in Currier B Is Aiin-Dominant and Functions Like d-Initial
**Priority:** high
**Status:** tested — NOT SUPPORTED (exp_064: s is 4.61× line-FIRST biased; d is 2.43× first AND 1.42× last. Same suffix profile but different positional grammar. F071 added.)
**Source:** F068 (exp_061): s-initial words in B have -aiin=20.6% (KL from k/t is 0.339 bits) — similar to d-initial (-aiin=20.8%). Both s and d are aiin-dominant onset classes in B. Are s-words grammatically similar to d-words (e.g., both mark line endings, both suppress at line-initial positions)?
**Description:** If s-initial and d-initial words share both suffix distribution AND positional grammar (both appear at line-final positions, both avoided at line-initial), this confirms they form a single grammatical class. From exp_050, d-stem words are strongly line-final (dam=3.92×, dain, etc.). Test: (a) What is the positional distribution of s-initial words? (b) Do s-initial words prefer line-final positions? (c) Are s-initial and d-initial words mutually exclusive at specific positions (complementary distribution)?
**Expected outcome:** If same class: s-initial = line-final bias (similar to dam/dain). If different: different positional profile despite similar suffix distribution.
**Cost estimate:** small (extend exp_050 to include s-initial words)
**Prerequisites:** exp_050, exp_061 (done)

---

## H075: In Currier B, p-Onset Line-Opening and y-Onset Line-Continuation Are Symmetrical Systems
**Priority:** high
**Status:** tested — PARTIALLY SUPPORTED (exp_064: p-onset cross-dialect para-start marker (A:7.38×, B:2.80×); y-initial cross-dialect continuation marker (suppressed at PS); symmetrical but pan-Voynichese not B-specific. F071 added.)
**Source:** F061 (y-initial = continuation marker in A), F070 (p-onset = para-start marker in B). In Currier B: y-initial suppressed at B para-starts (0.28×) and p-onset is the para-start marker. Does y-initial in B serve as a continuation marker (like in A) while p-onset serves as the para-start marker? This would establish a two-marker positional system in B parallel to A's two-marker system.
**Description:** From exp_054/F061: y-initial is at 14.2% of B continuation lines but suppressed at B para-starts. From exp_063/F070: p-onset is 17-18× enriched at B para-starts. If these are symmetric: p-onset marks para-START, y-initial marks LINE-CONTINUATION. Test: (a) Is y-initial enriched at B CONTINUATION positions relative to all B lines? (b) Is the B continuation y-initial rate similar to A's (16.4%)? (c) Are B para-start p-onset words and B continuation y-initial words mutually exclusive (no para-start y-initial p-onset words)?
**Expected outcome:** If symmetric system: B continuation y-initial rate ~ 14-16%; B para-starts have p-onset but no y-initial.
**Cost estimate:** tiny (direct from exp_057 data)
**Prerequisites:** exp_057, exp_063 (done)

---

## H076: The 4-Class Onset Taxonomy in Currier B Maps Onto Grammatical Roles
**Priority:** medium
**Status:** tested — PARTIALLY SUPPORTED (exp_064: positional grammar confirmed but 4-class taxonomy is imperfect: {k/t/p} splits — k=neutral, t=3.38× first, p=6.34× first. {d/s} splits — s=4.61× first, d=2.43× first AND 1.42× last. {ch/sh/qo}=medial confirmed. F071 added.)
**Source:** F068 (exp_061): Currier B has 4 effective onset classes: {ch/sh}, {k/t/p}, {d/s}, {qo}. F069-F070 suggest these onset classes correspond to grammatical roles. Do the four onset classes have systematically different grammatical functions (positional distributions)?
**Description:** From the findings so far: qo-prefix selects k/t class (F037/F055); d/s are aiin-dominant (F068); p-onset marks para-starts (F070); ch/sh have high -y/-edy suffix. Test: do these four onset classes have systematically different LINE-POSITIONAL distributions? Specifically: (a) Is {d/s} class line-final biased? (b) Is {qo} class medial biased? (c) Is {ch/sh} class medial biased (since -edy and -ey are medial)? (d) Is {p} class specifically line-initial biased? Mapping onset classes to positional functions would unify F068 (suffix distributions) with the positional grammar findings (F057-F070).
**Expected outcome:** If onset maps onto positional grammar: {d/s} = line-final, {p} = line-initial, {qo}/{ch/sh} = medial.
**Cost estimate:** small
**Prerequisites:** exp_050, exp_061, exp_063 (done)

---

## H077: The Herbal A Aiin-Dominant Sub-Dialect Is Closer to Currier B Than to Standard Currier A
**Priority:** high
**Status:** tested — NOT SUPPORTED (exp_065: aiin-dom A Jaccard with y-dom A=0.138 > with all B=0.046; both A registers show A suffix profile -ol/-or dominant, -edy<0.2%; two-register system is intra-A. F072 added.)
**Source:** F069 (exp_062): aiin-dominant herbal A folios have vocabulary Jaccard=0.138 from y-dominant folios — near A/B inter-dialect gap. But aiin-dominant folios use d-onset (1.61×), ch-onset (1.50×) — which are also strong in B. If aiin-dominant folios are a B-like scribal tradition mislabeled as A, they should be closer to B in vocabulary and morphology.
**Description:** Compare the aiin-dominant herbal A folios to: (a) y-dominant herbal A folios, (b) Currier B herbal folios (if any), (c) Currier B overall. Measure Jaccard overlap and frequency-rank correlation. If aiin-dominant ≈ B: the Currier classification of these folios may be wrong, or these represent a B-type scribal tradition that was part of the Herbal A compilation.
**Expected outcome:** If mislabeled: aiin-dominant Jaccard with B > aiin-dominant Jaccard with y-dominant A. If genuine A sub-dialect: aiin-dominant Jaccard with B < aiin-dominant Jaccard with y-dominant.
**Cost estimate:** small
**Prerequisites:** exp_062 (done)

---

## H079: The Aiin-Dominant Herbal A Register Has Higher Entropy Than y-Dominant (Less Predictable Words)
**Priority:** medium
**Status:** tested — SUPPORTED (opposite direction): y-dom has HIGHER h1=9.180 vs aiin-dom=8.488; aiin-dom concentrated around daiin (6.48%). Same bigram h2~1.57. F073 added.
**Source:** F069 (exp_062): the two A registers have vocabulary Jaccard=0.138, suggesting different word inventories. The aiin-dominant register uses more diverse -aiin suffix words (chaiin, chey, chy) while y-dominant uses more y-initial compound words. Which register has higher vocabulary entropy?
**Description:** If the aiin-dominant register uses a more diverse (higher-entropy) vocabulary than y-dominant, this suggests the aiin-dominant scribal tradition encoded more information per token. If lower entropy, it's more formulaic. Test: compute h1 (unigram entropy), h2 (bigram conditional entropy), and TTR for each register.
**Expected outcome:** If aiin-dom is more formulaic (lower entropy): it uses a smaller set of words more repetitively. If higher entropy: it uses a more diverse vocabulary.
**Cost estimate:** tiny
**Prerequisites:** exp_062 (done)

---

## H080: The Currier B p-Onset Para-Start Words Have a Different Quire Distribution Than B Baseline (Are They Section-Specific?)
**Priority:** medium
**Status:** tested — NOT SUPPORTED (exp_067: pch/tch distributed across all B quires, range 0.58-2.36% combined; no strong clustering. F074 added.)
**Source:** F070 (exp_063): pch/tch onset words are concentrated in Special (1.01%), Herbal (0.85-0.91%), Bio (0.47-0.58%) sections of B and absent from Astro. Are pch/tch words also concentrated in specific quires of the B manuscript?
**Description:** If pch/tch words are uniformly distributed across all B quires, the para-start function is a manuscript-wide convention. If they cluster in specific quires (as the aiin-dominant A register clusters in Quires D/F), this suggests a B-side quire-level scribal variation. Test: compute pch/tch rates per B quire.
**Expected outcome:** If uniform: manuscript-wide B convention. If clustered: quire-specific scribal convention (parallel to aiin-dominant A).
**Cost estimate:** tiny
**Prerequisites:** exp_063 (done)

---

## H081: Voynichese Has a "Word Length Grammar" — Word Length Distribution Differs Systematically by Line Position
**Priority:** high
**Status:** tested — STRONGLY SUPPORTED (exp_066: A para_start=6.55, B para_start=7.15; B gradient para>cont>medial>last; para-start words are longest, last words shortest. F073 added.)
**Source:** Synthesis of F057-F071: line-initial words tend to be p-onset (long compound words like pchedar, tchedy) while medial words (ch/sh) and line-final words (o-onset) may have different length distributions. Does Voynichese use word LENGTH as an additional positional signal?
**Description:** The positional grammar findings so far focus on onset class and suffix class. But word length itself may be a positional signal: if line-initial words are systematically longer than line-final words, this adds another dimension to the positional grammar. Test: compute mean word length (in EVA characters) for (a) para-start first words, (b) continuation first words, (c) line-medial words, (d) line-last words, separately for Currier A and B. Compare with the positional onset class results.
**Expected outcome:** If length is a positional signal: para-start words are longer (p-onset compound words); line-final words are shorter (e.g., 'ol', 'or', 'al').
**Cost estimate:** small
**Prerequisites:** exp_057, exp_063, exp_064 (done)

---

## H082: The Bio Section Has a Two-Register System Analogous to Herbal A (Pool vs Non-Pool Folios)
**Priority:** medium
**Status:** tested — NOT SUPPORTED (exp_067: Jaccard=0.201 far above A register split=0.138; identical suffix profiles, qo-rates. Bio pool/non-pool is organizational not linguistic. F074 added.)
**Source:** F068 (exp_061): Bio multi-para folios are specifically pool/bathing folios. F069 (exp_062): two-register system in Herbal A. Does the Bio section also have two registers — pool folios (multi-paragraph, specialized vocabulary) vs non-pool folios (single-paragraph)?
**Description:** Pool folios (f75v, f82r, f83r, f83v, f84r, f84v) vs non-pool bio folios (the rest). Test: (a) Do pool vs non-pool bio folios differ in vocabulary (Jaccard)? (b) Do they differ in suffix distributions? (c) Do pool folios have higher qo-rates or different positional grammar? The pool/non-pool distinction in bio may be as significant as the aiin/y-dominant distinction in herbal A.
**Expected outcome:** Some vocabulary difference expected (pool scenes describe different content). Structural grammar differences would be more significant.
**Cost estimate:** small
**Prerequisites:** exp_061 (done)

---

## H083: Within Multi-Para Bio Folios, Paragraphs Are Independent Vocabulary Units
**Priority:** high
**Status:** tested — PARTIALLY SUPPORTED (exp_068: non-trivial para pairs Jaccard 0.075-0.156 ≈ cross-folio 0.155; tiny paras are marginal annotations; paragraphs share structural B vocabulary. F075 added.)
**Source:** F074 (exp_067): Bio pool/non-pool is organizational, not linguistic. F068 (exp_061): Bio has 37% multi-para folios. Within a single multi-paragraph bio folio, are the paragraphs independent vocabulary units (each paragraph describing a different figure/subject) or do they repeat the same high-frequency words?
**Description:** For each multi-para bio folio, split words by paragraph (para index 0, 1, 2, ...). Compute within-folio inter-paragraph Jaccard. If paragraphs are semantically independent units (each describes a different person), we expect low within-folio inter-paragraph Jaccard. If paragraphs are continuation of the same text, we expect high Jaccard. Compare to cross-folio Jaccard as a baseline.
**Expected outcome:** If bio paragraphs describe independent figures: Jaccard < overall bio Jaccard. If continuation: high Jaccard with same vocabulary.
**Cost estimate:** small
**Prerequisites:** exp_067 (done)

---

## H084: qo-Onset Words Have a Distinct Morphological Sub-Grammar (qo + restricted suffix set)
**Priority:** high
**Status:** tested — STRONGLY SUPPORTED (exp_068: qo attaches to gallows k/t/p/f in 86.5%; medial 1.12× enriched; para-start 0.12× suppressed; -eedy 2.05×; Bio=26%; F075 added.)
**Source:** F068 (exp_061): qo is a distinct onset class in Currier B. F071 (exp_064): qo is 0.64× line-first biased (slightly medial). Do qo-onset words have a restricted suffix grammar? The qo-prefix may function as a grammatical particle (determiner? negation? quantifier?) that combines with a limited set of stems.
**Description:** Extract all qo-initial words from Currier B. What follows 'qo'? Map the post-qo character distribution. Does qo consistently combine with a restricted set of stems/suffixes? Compare qo-suffix distribution to the overall B suffix distribution. Also test: is qo more common in specific sections (Herbal vs Bio vs Cosmo)?
**Expected outcome:** If qo is a grammatical particle: restricted suffix set, not just any word with qo prefix. If qo is a phonological coincidence: same suffix distribution as non-qo words.
**Cost estimate:** small
**Prerequisites:** none — corpus analysis

---

## H085: ch vs sh Discrimination — What Determines Which Allomorph Appears?
**Priority:** medium
**Status:** tested — SUPPORTED (exp_069: sh more line-initial A:11.2% vs ch:3.9%, B:5.0% vs 2.1%; ch more line-final; B ch+short suffix, sh+extended suffix; sh follows p-onset 4.1×; self-following repetition. F076 added.)
**Source:** F068 (exp_061): KL(ch vs sh) = 0.062 bits — nearly identical positional profiles. Both are strongly medial. But ch is far more frequent. Is there a phonological or positional context that distinguishes ch from sh? Are they in complementary distribution (one appears after certain words, the other after different words)?
**Description:** For all body-text lines in Currier B: (1) Compute the word immediately BEFORE ch-onset vs sh-onset words. Do different words precede ch vs sh? (2) Compute the character immediately before ch vs sh in the raw EVA (within-word context — are they ever word-medial after a prefix?). (3) Test whether ch and sh have different suffix preferences. (4) Check if one appears more in specific sections.
**Expected outcome:** If complementary distribution: ch appears after certain word classes, sh after others. If free variation: no predictable context.
**Cost estimate:** small
**Prerequisites:** none

---

## H086: The Voynich 'Gallows' Letters (k, t, f, p) Have Individual Positional Grammar Despite Being One Onset Class
**Priority:** medium
**Status:** tested — STRONGLY SUPPORTED (exp_069: p=17.76× para-start; t=7.64×; f=8.04×; k=medial 1.05× but 4.88× para-start; k has -dy suffix preference 2.14×. Revised taxonomy: {p}, {t/f}, {k}, {ch/sh}. F076 added.)
**Source:** F068 (exp_061): KL(k vs t) = 0.082 bits — same suffix class. F071 (exp_064): p is 6.34× line-first while k is only 0.66× line-first. The 4-class taxonomy groups k/t/p but they have very different positional behavior. Do k, t, f each have distinct positional signatures, or are k and t truly interchangeable while p is the outlier?
**Description:** Compute line-first%, line-last%, para-start% for each of k, t, f, p individually in Currier B. Also compute suffix distributions for each. Are k and t truly interchangeable (similar positional profiles)? Is f (a less common gallows) positionally distinct?
**Expected outcome:** If k/t interchangeable: similar line-first%, similar suffix profiles. If p is the sole outlier: k/t clustered, p separate. If 4-way distinct: all have different positional grammar.
**Cost estimate:** tiny
**Prerequisites:** exp_064 (done)

---

## H087: The k+-dy Combination Is a Specific Grammatical Morpheme (Medial Particle)
**Priority:** high
**Status:** tested — WEAKLY SUPPORTED (exp_070: k-dy forms are complex k+ch+dy compounds; slightly more line-final 1.43×; follows gallows 2.79×. Not a clear particle. F077 added.)
**Source:** F076 (exp_069): k is the medial gallows (1.05× medial) with -dy suffix preference (13.9% = 2.14× baseline). The most common k words are keedy, kar, kaiin, kedy, kain. k+-dy (kedy) is disproportionately common. Is this a specific grammatical morpheme — a medial particle or conjunction? Test: (1) Is 'kedy' more positionally restricted than random k words? (2) Does 'kedy' appear in a specific syntactic slot (e.g., always medial, always after qo- words)? (3) Do k+-dy words differ from k+-other-suffix words in positional grammar?
**Expected outcome:** If kedy is a particle: positionally restricted (exclusively medial), follows specific word classes. If kedy is a random form: same distribution as other k words.
**Cost estimate:** small
**Prerequisites:** exp_069 (done)

---

## H088: ch-ch and sh-sh Self-Following Sequences Form Bi-Word Constructions
**Priority:** medium
**Status:** tested — SUPPORTED FOR A, NOT B (exp_070: A ch-ch 1.34×, sh-sh 1.46×; dominant pair "chol chol"(20); B near-random 1.04-1.09×. New: qo+gallows→ch is dominant B word-order rule. F077 added.)
**Source:** F076 (exp_069): ch follows ch at 1.52-1.63×; sh follows sh at 2×. This self-following repetition suggests that ch-ch and sh-sh bigrams may be bi-word constructions (determiners + nouns, or compound phrases). Test: (1) What are the most common ch-ch and sh-sh word pairs? (2) Do they appear at specific positions (both medial)? (3) Is the second word of a ch-ch pair different from a random ch word?
**Expected outcome:** If bi-word constructions: specific high-frequency ch-ch pairs, restricted to medial position. If coincidental: random ch pairs with no structural binding.
**Cost estimate:** small
**Prerequisites:** exp_069 (done)

---

## H089: The Revised 5-Class Onset Taxonomy ({p}, {t/f}, {k}, {ch/sh}, {d/s}) Is Stable Across B Sections
**Priority:** medium
**Status:** tested — STRONGLY SUPPORTED (exp_071: ch/sh 0.00% para-first all sections; p 19-55× para-start all sections; qo medial all sections; k para-start varies Bio=12×, Herbal=3.77×. F078 added.)
**Source:** F076 (exp_069): revised 5-class taxonomy derived from B-wide data. F074 (exp_067): qo-rate varies by section (Bio=26%, Astro=6.5%). Does the positional specialization of each onset class hold within individual B sections, or does the taxonomy change by section?
**Description:** Compute the positional enrichment (first%, medial%, last%, para-first%) for each of the 5 onset classes separately within each B section (Herbal B, Bio, Special, Text, Cosmo, Astro). Is p still the dominant para-start marker in all sections? Is k still medial-dominant in all sections?
**Expected outcome:** If taxonomy is stable: same positional enrichment pattern in each section. If section-specific: some sections use different onset classes for structural positions.
**Cost estimate:** small
**Prerequisites:** exp_069 (done)

---

## H090: The qo+gallows→ch/sh Sequential Rule Holds Across All Currier B Sections
**Priority:** high
**Status:** tested — WEAKLY SUPPORTED (exp_071: qo→ch 1.13-1.70× by section; strongest Bio+Cosmo; weak Herbal/Special/Text. Serendipitous: sh→qo=36.6% is dominant B transition. F078 added.)
**Source:** F077 (exp_070): In B body text overall, qo+gallows words (qokain=86, qokaiin=78) are the most common predecessors of ch-onset words. Does this sequential rule hold within individual sections? If the rule is universal, it's a grammatical constraint; if section-specific, it's a content vocabulary effect.
**Description:** For each Currier B section (H=Herbal, B=Bio, S=Special, T=Text, C=Cosmo), compute the top words that precede ch-onset and sh-onset words. Is qo+gallows always the top predecessor? Also compute: P(ch after qo+gallows) vs P(ch after non-qo words). This yields the conditional probability of the sequential rule.
**Expected outcome:** If universal rule: qo+gallows precedes ch/sh in all sections. If content artifact: specific to Bio or Special section (where qo is most common).
**Cost estimate:** small
**Prerequisites:** exp_070 (done)

---

## H091: Currier A Has an Equivalent Sequential Grammar to B's qo+gallows→ch
**Priority:** medium
**Status:** tested — SUPPORTED (exp_072: A has NO dominant predecessor for ch; flat transitions max 1.34×; ch→ch self-following is only structure; A lacks qo-hinge function. F079 added.)
**Source:** F077 (exp_070): B has qo+gallows→ch/sh as dominant sequential rule. In A, the top predecessor of ch words is daiin(69) and chol(67) — the dominant A bi-gram. Is there a structural parallel in A? What are the most common A word-order pairs for ch-onset and sh-onset words?
**Description:** For Currier A, compute the top words before and after ch-onset and sh-onset words, by section. Identify the dominant A sequential grammar analogous to B's qo+gallows→ch rule. Compare: does A use the same predecessor class (daiin → ch?) systematically, and does this hold across sections?
**Expected outcome:** If A has a parallel grammar: one A-specific word class systematically precedes ch (daiin? or-initial?). If A is different: no dominant predecessor for ch words.
**Cost estimate:** small
**Prerequisites:** exp_070 (done)

---

## H092: The sh→qo Coupling (36.6%) Reflects a Tight Two-Word Construction: sh-word + qo-word Form a Bi-Word Unit
**Priority:** high
**Status:** tested — STRONGLY SUPPORTED (exp_072: sh→qo 1.44-2.20× in all B sections; dominant pair shedy→qok-forms; d suppresses qo 0.76×; A has weak parallel 1.56×. F079 added.)
**Source:** F078 (exp_071): sh→qo=36.6% is the largest single onset transition in Currier B (vs random baseline qo rate ~18.6%). sh is followed by qo at nearly 2× the baseline rate. Does this reflect a grammatically bound bi-word unit (sh-word + qo-word), or is it a serial correlation from shared section affinity?
**Description:** (1) What are the most common sh-word + qo-word adjacent pairs? (2) Is the sh→qo transition uniform across all sections or concentrated in specific sections? (3) Does sh appear before qo more than any other class across all sections? (4) Compare P(qo after sh) vs P(qo after ch) vs P(qo after d) to confirm sh→qo is a specific coupling.
**Expected outcome:** If grammatical coupling: specific high-frequency sh+qo pairs, uniform across sections. If coincidental: driven by specific section or folio.
**Cost estimate:** small
**Prerequisites:** exp_071 (done)

---

## H093: The Currier A Sequential Grammar: daiin Is the A-Analogue of B's qo+gallows Predecessor
**Priority:** high
**Status:** tested — NOT SUPPORTED (exp_072: A has flat transition matrix; ch→ch 1.34× is only notable; daiin not tested as onset class since daiin=d-class; A grammar is flatly distributed. F079 added.)
**Source:** F077 (exp_070): in A, daiin(69) precedes ch more than any other word. F078 (exp_071): in B, qo+gallows is the dominant ch predecessor. H091 proposed testing whether daiin is A's sequential grammar rule. Test this directly: (1) P(ch | daiin prev) vs P(ch | non-daiin prev) in Currier A, by section. (2) Compute A-wide onset transition matrix. (3) What is A's dominant sh predecessor?
**Expected outcome:** If daiin is A's dominant medial predecessor: P(ch|daiin) >> P(ch|non-daiin). If the A grammar is different: no clear dominant predecessor.
**Cost estimate:** small
**Prerequisites:** exp_071 (done)

---

## H094: The d→qo Suppression (0.76×) Reflects That d-onset Words and qo-onset Words Occupy Complementary Slots
**Priority:** high
**Status:** tested — STRONGLY SUPPORTED (exp_073: d→ch=1.27×, d→qo=0.76×; sh→ch=0.64×, sh→qo=1.97×. Perfect complements. Two paths to ch: sh→qo→ch and d→ch. F080 added.)
**Source:** F079 (exp_072): sh→qo=1.97× (enriched) while d→qo=0.76× (suppressed). d and qo are in opposite sequential relationships to sh: sh prefers qo, d avoids qo. Does d occupy a positional slot that is FOLLOWED by ch directly (bypassing qo)? Is there a d→ch coupling analogous to sh→qo?
**Description:** Compute P(ch|d), P(ch|sh), P(ch|qo), P(ch|o) directly and compare to baseline. Also: what does d follow most often? Is there a word class that systematically precedes d? If d and qo are in complementary sequential niches, the sequence around d would be: [something] → d → ch, while around qo it would be: sh → qo → ch.
**Expected outcome:** If d→ch coupling: P(ch|d) > P(ch|sh). If d is the "medial non-qo" class: d words appear in the same slot as qo but with different preceding and following words.
**Cost estimate:** tiny (uses existing transition matrix data from exp_072)
**Prerequisites:** exp_072 (done)

---

## H095: The B Grammar Has a Three-Slot Medial Structure: [qo-gallows] + [ch/sh] + [suffix-word]
**Priority:** high
**Status:** tested — REFUTED AT WORD LEVEL (exp_073: qo+ch trigrams 99.4% unique; grammar is onset-class level only, not word level. After qo+ch: qo=29.7%, confirming alternation loop. F080 added.)
**Source:** F078 (exp_071, transition matrix): the B medial sequence is qo→ch/sh→qo→ch/sh (alternation). F079 (exp_072): sh→qo coupling is specific to shedy/shey → qok-forms. Do three-word medial sequences (qo-word + ch/sh-word + closing-word) appear at elevated rates as specific trigram constructions?
**Description:** Extract all three-word sequences where word 1 is qo-onset, word 2 is ch/sh-onset, word 3 is any onset. What are the most common three-word medial sequences? Are specific trigrams (qo+ch/sh+suffix-word) highly repetitive across folios? Compare trigram diversity in B medial positions to A.
**Expected outcome:** If three-slot structure exists: specific qo+ch/sh+word trigrams appear repeatedly across folios. If not: medial words combine freely.
**Cost estimate:** small
**Prerequisites:** exp_071, exp_072 (done)

---

## H096: The A 'daiin' Word Encodes a Specific Sequential Role: It Precedes ch-onset Words More Than Expected When Controlling for Its Overall Frequency
**Priority:** medium
**Status:** tested — NOT SUPPORTED (exp_073: P(ch|daiin)=1.06×, P(ch|other-d)=1.10×; daiin not enriched vs d-class baseline. The d→ch enrichment is a class property. F080 added.)
**Source:** H093 tested onset classes in A; daiin is a d-class word. F079: A has flat transition matrix, with d→ch at 1.09× baseline. But daiin specifically (not all d-words) was the most common predecessor of ch in the raw word-count analysis (F070: daiin=74 occurrences before ch). Is daiin itself (not the d-class generally) enriched as a ch-predecessor?
**Description:** Compute P(ch|daiin) vs P(ch|other-d-words) in Currier A. Is daiin specifically enriched as a ch-predecessor, while other d-words (dar, dain, dy...) are not? This would show that daiin is NOT just a common word that happens to precede ch, but specifically enriched as a ch-predecessor.
**Expected outcome:** If daiin-specific: P(ch|daiin) >> P(ch|other-d). If coincidental: P(ch|daiin) ≈ P(ch|other-d) ≈ baseline.
**Cost estimate:** tiny
**Prerequisites:** exp_072 (done)

---

## H097: The d/sh Sequential Complementarity Exists in Currier A (Cross-Dialect Sequential Grammar)
**Priority:** high
**Status:** tested — SUPPORTED (exp_074: A has d/sh complementarity but weaker than B; sh→qo=1.58× vs B 1.97×, d→ch=1.09× vs B 1.27×. Critical: in A, s-onset is the true complement of sh — s→ch=1.36×, s→qo=0.63×. F081 added.)
**Source:** F080 (exp_073): d and sh are perfect sequential complements in B (sh→qo=1.97×, d→ch=1.27×, sh→ch=0.64×, d→qo=0.76×). F079: A has weak sh→qo (1.56×). Does A also have d/sh complementarity? In A, the qo-hinge is weaker — does d→ch still hold?
**Description:** Compute P(ch|d), P(qo|d), P(ch|sh), P(qo|sh) for Currier A. Compare to B values. Are d and sh in complementary roles in A too? Also: does A have a different complementary structure (perhaps y vs d instead of sh vs d)?
**Expected outcome:** If cross-dialect: A also shows d→ch enrichment and sh→ch suppression. If B-specific: A shows no complementarity or different pairs.
**Cost estimate:** tiny (reuse A transition matrix from exp_072)
**Prerequisites:** exp_073 (done)

---

## H098: The B Grammar Model Can Predict Onset Class Sequences: A Bigram Language Model at Onset Level Has Lower Perplexity Than Unigram
**Priority:** high
**Status:** tested — SUPPORTED (exp_074: B bigram model 13.3% improvement over unigram, 0.207 bits; A 9.1%, 0.138 bits. B's sequential grammar is 35% stronger. F081 added.)
**Source:** F078-F080: The B sequential grammar is encoded in onset-class bigram transition probabilities (sh→qo=1.97×, qo→ch=1.31×, d→ch=1.27×). This should be learnable as a bigram language model. Does a bigram model over onset classes have significantly lower perplexity than a unigram model? And does A have lower bigram perplexity than B (B's grammar is stronger)?
**Description:** Build unigram and bigram language models over onset classes (not words) for Currier A and B separately. Compute perplexity (average bits per onset class token). The difference in perplexity (bigram vs unigram) measures how much the sequential grammar helps prediction. Compare A vs B: which dialect has a stronger onset-class sequential grammar?
**Expected outcome:** B bigram model has significantly lower perplexity than B unigram (due to sh→qo coupling). A bigram model has smaller perplexity reduction (flatter transitions).
**Cost estimate:** small
**Prerequisites:** exp_073 (done)

---

## H099: Line-Final Words Are Determined by the Onset Class of the Preceding Word
**Priority:** medium
**Status:** tested — SUPPORTED (exp_074: B line-final: qo=0.61×, sh=0.42× suppressed; o=1.25×, d=1.50× enriched. sh-penult→qo-last: 28.0%. A line-final: d=1.73× dominant. F081 added.)
**Source:** F071 (exp_064): o-onset words are slightly line-final biased (1.24×). The B sequential grammar loop (sh→qo→ch→qo→...) must terminate with a line-final word. Is the line-final word class determined by the onset class of the word preceding it?
**Description:** For B body text: group line-final words by the onset class of the second-to-last word. Do specific onset classes (e.g., qo, ch) systematically precede line-final words with specific onset classes (e.g., o)? Also: what onset classes appear as second-to-last words in B lines?
**Expected outcome:** If line-final determination: specific onset classes reliably precede line-final words. If free: the second-to-last word has a flat distribution.
**Cost estimate:** small
**Prerequisites:** exp_073 (done)

---

## H100: The A {sh vs s} Complementarity Is Section-Sensitive (Like B's {sh vs d})
**Priority:** high
**Status:** tested — STRONGLY SUPPORTED (exp_075: Pharma A sh→qo=2.44× > B's 1.97×! sh→ch=0.36×. Herbal A weak: sh→qo=1.27×. Pharma A has B-strength sequential grammar. F082 added.)
**Source:** F081 (exp_074): In A, s→ch=1.36× and s→qo=0.63×, mirroring B's d→ch=1.27× and d→qo=0.76×. But the A s-onset role was measured globally. Does the s/sh complementarity in A vary by section (Herbal A vs Pharma A), as B's d/sh complementarity varies by section?
**Description:** Compute P(ch|s), P(qo|s), P(ch|sh), P(qo|sh) for each Currier A section separately (Herbal A, Pharma A). Are there sections where s plays the d-role more strongly? Also: does the two-register system (y-dominant vs aiin-dominant folios) affect the s/sh complementarity?
**Expected outcome:** If section-sensitive: one A section has stronger s/sh complementarity (analogous to B Astro being the strongest sh→qo section). If uniform: s/sh is cross-section in A.
**Cost estimate:** small
**Prerequisites:** exp_074 (done)

---

## H102: The B Trigram Grammar (qo→ch→qo) Has an A Equivalent (ch→ch→ch or s→ch→s)
**Priority:** medium
**Status:** tested — SUPPORTED (exp_075: A dominant trigram ch→ch→ch=2.05× (107 tokens); B dominant sh→qo→ch=3.35×. A=ch-repetition grammar; B=sh-qo oscillation. F082 added.)
**Source:** F081 (exp_074): A has ch→ch self-following (1.34×) and s plays the d role (s→ch=1.36×). F080: B has a confirmed qo→ch→qo alternation loop (after qo+ch, next is qo at 29.7%). Does A have an analogous alternation? Specifically: does A have ch→ch→ch triplets? Or s→ch→s? Or some other 3-slot onset sequence?
**Description:** Compute A onset-class trigrams (onset classes for consecutive triplets of words). Find the most enriched trigrams vs a unigram baseline. Compare to B's dominant trigram structure (qo→ch→qo: 29.7% after qo+ch). Does A have a comparable dominant trigram structure?
**Expected outcome:** If analogous: A has ch→ch→ch or s→ch→s as a dominant triplet (reflecting the ch→ch self-following). If not: A's grammar is truly flat at the trigram level.
**Cost estimate:** small
**Prerequisites:** exp_074 (done)

---

## H103: The sh→qo Coupling Differs in Strength Between y-Dominant and aiin-Dominant Herbal A Folios
**Priority:** medium
**Status:** tested — SUPPORTED (exp_075: aiin-dom bigram PPL 12.7% vs y-dom 10.2%; aiin-dom uses qo→ch (1.72×) and s→ch (1.76×) pathways; y-dom uses sh→qo (1.29×). Critical: aiin-dom d→qo=1.55× (opposite to B). F082 added.)
**Source:** F081 (exp_074): The A sequential grammar is weaker than B's (bigram PPL reduction: 9.1% vs B 13.3%). F066 (exp_059): Two-register Herbal A — y-dominant vs aiin-dominant folios have different onset profiles (y-dominant enriches o-onset 1.59×; aiin-dominant enriches d-onset 1.61×). Does the {sh vs s} complementarity differ between these A registers?
**Description:** Split Herbal A folios into y-dominant vs aiin-dominant registers (using the exp_059/exp_062 classification). Compute onset-class bigram transition matrices separately for each. Compare: (1) sh→qo coupling, (2) s→ch enrichment, (3) bigram vs unigram PPL reduction. Are the two registers of Herbal A as different in sequential grammar as A vs B?
**Expected outcome:** If register-sensitive: aiin-dominant A has stronger d-like grammar (d→ch enriched); y-dominant A has different structure. If uniform: the two registers share the same sequential grammar despite different onset-class frequencies.
**Cost estimate:** small
**Prerequisites:** exp_059, exp_074 (done)

---

## H104: The B Line-Final Onset Pattern Differs Systematically by Section (Bio vs Herbal B)
**Priority:** low
**Status:** tested — PARTIALLY SUPPORTED (exp_075: qo/sh suppression and o enrichment universal across all B sections; d enrichment 5/6 sections; Special section exception: no d enrichment, "other"=2.03×. F082 added.)
**Source:** F081 (exp_074): B line-final words are non-random (o=1.25×, d=1.50×, qo=0.61×, sh=0.42×) — measured globally. But B sections differ morphologically (F078: 5-class taxonomy stable; Bio enriches k at para-starts). Does the line-final onset distribution differ by section?
**Description:** For each B section (Herbal B, Bio B, Pharma B, Text B, Special B), compute the last-word onset distribution and enrichment. Does the d-onset line-final enrichment (1.50×) hold across all sections? Is the qo suppression at line-ends universal or section-specific?
**Expected outcome:** If universal: the line-final grammar is a section-independent property of Currier B. If section-sensitive: one section (e.g., Bio with its qo-dominated vocabulary) might show different line-final patterns.
**Cost estimate:** small
**Prerequisites:** exp_074 (done)

---

## H105: Pharma A Has a B-Like Sequential Grammar Because It Shares B's Onset-Class Vocabulary Distribution
**Priority:** high
**Status:** tested — PARADOX CONFIRMED (exp_076: Pharma A has B-strength sh→qo=2.44× but Jaccard with B=0.070 < Herbal A's 0.100; -edy=0.2%, -ol=18.2% pure A-type. Grammar and morphology dissociated. F083 added.)
**Source:** F082 (exp_075): Pharma A sh→qo=2.44× (stronger than B's 1.97×!). This is surprising because Pharma A should be Currier A in dialect. Is Pharma A actually closer to B in its onset-class vocabulary distribution, which would explain the stronger sh→qo coupling?
**Description:** (1) Compute onset-class frequency distribution for Pharma A vs Herbal A vs global B. Is Pharma A's qo-rate closer to B's? (2) Compute vocabulary Jaccard between Pharma A and Currier B. Is Pharma A closer to B than Herbal A is? (3) Check Pharma A suffix profile (-edy%, -ol%, -aiin%) — is Pharma A using B-type or A-type suffixes? (4) Is the Pharma A sh→qo coupling driven by specific high-frequency words (e.g., shedy → qok-forms)?
**Expected outcome:** If Pharma A is B-adjacent: onset-class distribution closer to B; Jaccard higher with B than Herbal A is; suffix profile mixed. If it's purely grammar-level: onset distribution matches A but transition matrix differs.
**Cost estimate:** small
**Prerequisites:** exp_075 (done)

---

## H106: The Aiin-Dominant A d→qo=1.55× Is Driven by Specific Word Pairs (daiin→qok-forms)
**Priority:** high
**Status:** tested — STRONGLY SUPPORTED (exp_076: daiin→qo=2.38× in aiin-dom; other-d→qo=1.24×; y-dom daiin→qo=0.81× (opposite!). Two A registers have opposite daiin-qo coupling. F083 added.)
**Source:** F082 (exp_075): Aiin-dominant Herbal A has d→qo=1.55× (opposite to B's d→qo=0.76×). This is unexpected — in aiin-dominant A, d-onset words lead to qo, not away from it. Is this coupling driven by specific word pairs? Particularly: does daiin specifically precede qo-onset words?
**Description:** In aiin-dominant Herbal A: (1) Compute P(qo next | daiin) vs P(qo next | other d-words). Is daiin specifically the qo-preceding word? (2) What are the actual word pairs driving d→qo in aiin-dom? (3) Compare: in B, d→qo is suppressed (0.76×). In y-dominant A, d→qo=0.81×. In aiin-dom, d→qo=1.55×. What explains this gradient?
**Expected outcome:** If daiin-specific: daiin→qo-words is a common construction in aiin-dom A. If general d-class: all d-words show elevated qo-following in aiin-dom. The mechanism might reveal an A-specific grammatical rule.
**Cost estimate:** small
**Prerequisites:** exp_075 (done)

---

## H107: The B Special Section "Other" Line-Final Dominance Reflects Specific Onset Classes Not Captured in the 10-Class Taxonomy
**Priority:** medium
**Status:** tested — CLARIFIED (exp_076: "other" = a/l/r-initial words, same as non-Special B. Anomaly is quantity: Special=28.7% "other" vs ~15-18% elsewhere. Special avoids d-onset at line-ends (0.85×). F083 added.)
**Source:** F082 (exp_075): B Special section has "other" onset enriched 2.03× at line-ends. All other B sections show d-enrichment and o-enrichment at line-ends; Special section doesn't. What specific onset classes are in the "other" category in Special section line-final words?
**Description:** For B Special section: (1) Decompose the "other" onset category — what specific characters start these words? (2) Are there specific B Special section words that dominate line-ends? (3) Compare Special section line-final vocabulary to the rest of B. Is this an anomalous scribal practice, vocabulary effect, or genuine grammar difference?
**Expected outcome:** If specific word type: Special section line-final "other" words are a specific class (e.g., words starting with f, l, or specific patterns). If random: "other" reflects miscellaneous unconstrained positions.
**Cost estimate:** small
**Prerequisites:** exp_075 (done)

---

## H108: The B para-Interior vs para-Final Line-Ending Onset Distribution Differs (Paragraph Boundary Marking)
**Priority:** medium
**Status:** tested — STRONGLY SUPPORTED (exp_076: B para-final: o=40.0% (1.72×) vs within-para 28.2% (1.22×); qo=0.17× at para-final vs 0.62× within. A para-final: ch=1.20× (vs 0.83× within). Both dialects suppress qo at para-final. F083 added.)
**Source:** H101 (pending), F082 (exp_075): B line-final grammar is section-universal. But is there a PARAGRAPH-level boundary marker in the line-final position? Para-start words are strongly marked (p-onset: 17.76×). Is the last word of a paragraph's last line also distinctively marked?
**Description:** For B: classify each record as (1) continuation line within paragraph, (2) last line of paragraph (next record is para-start or new paragraph). Compute last-word onset distribution for each. Also: for A, compare para-final last word to within-para last word onset distribution.
**Expected outcome:** If para-final marking: the last word of a paragraph's last line has a different onset distribution from within-para line-final words. If no distinction: the line-final grammar is line-level only.
**Cost estimate:** small
**Prerequisites:** exp_075 (done)

---

## H109: The B o-Onset Para-Final Pattern — Specific o-Words That Serve As Paragraph Closers
**Priority:** high
**Status:** tested — SUPPORTED (DISTRIBUTED) (exp_077: No single word dominates B para-finals; ary=49.86×, orol=41.55× but are rare. Para-closing is onset-class-level only. Within-para line-finals favor oly, otam, okam. F084 added.)
**Source:** F083 (exp_076): B paragraphs close with o-onset words (40.0%, 1.72×). This is much stronger than the general line-final o enrichment (1.25×). Are there specific o-onset words that function as paragraph closers? What is the vocabulary of B para-final last words?
**Description:** (1) List the most frequent o-onset words that appear as B para-final last words. Are a few words (e.g., "ol", "or", "o") disproportionately common? (2) Compare: are these same o-words also enriched at within-para line-finals, or specifically at para-finals? (3) Do the B para-closing o-words differ by section? (4) For A: what specific ch-words appear at A para-finals?
**Expected outcome:** If specific closers: a few o-words (e.g., "ol", "or") dominate para-finals. If distributed: many o-words appear. Either way, identifying the specific words would reveal the vocabulary of the para-boundary marker class.
**Cost estimate:** small
**Prerequisites:** exp_076 (done)

---

## H110: The Pharma A sh→qo Coupling Has a Different Character From Herbal A — Specific sh-Words Differ
**Priority:** medium
**Status:** tested — SUPPORTED (exp_077: Pharma A uses she- prefix forms (sheol, sheey, sheor) vs Herbal A short sh- forms (shol, sho, shor). Pharma A sh→qo=32.3% vs Herbal A 12.9%. she- forms drive the B-strength coupling. F084 added.)
**Source:** F083 (exp_076): Pharma A sh→qo=2.44× (stronger than B's 1.97×) despite using A-type vocabulary. The sh→qo pairs are diverse (sheey, sheol, sheody, shoy — many hapaxes). Does Pharma A use different sh-words than Herbal A? The Pharma A sh-words appear to include -eol, -eo, -ody suffixes — different from Herbal A's sh-words.
**Description:** (1) List the most frequent sh-words in Pharma A vs Herbal A. Are they different stems? (2) What suffixes do Pharma A sh-words take (vs Herbal A sh-words)? (3) In Herbal A, what follows sh-words (if not qo)? Compare the full sh→X transition distribution in Pharma A vs Herbal A.
**Expected outcome:** If different sh-words: Pharma A sh-words are distinct vocabulary items from Herbal A sh-words. If same stems but different grammar: the same sh-words (shedy, shey, shol) appear in both but follow different sequential rules.
**Cost estimate:** small
**Prerequisites:** exp_076 (done)

---

## H111: The daiin→qo Construction in Aiin-Dom Herbal A Has a Specific Successor Pattern (daiin → qo → X)
**Priority:** medium
**Status:** tested — SUGGESTIVE ONLY (exp_077: n=9 triplets; X=qo at 33.3% (4.20×), dominant triplet daiin→qotchy→qotor (2×); sh precedes daiin→qo in 3/9. Sample too small for firm conclusions. F084 added.)
**Source:** F083 (exp_076): In aiin-dominant Herbal A, daiin→qo=2.38× (enriched); top pairs include daiin→qotchy (2), daiin→qoky, daiin→qokcho. Does this create a three-word construction: daiin → qo-word → X, where X is a specific onset class?
**Description:** In aiin-dom Herbal A: (1) Compute P(X | daiin → qo-word) for each onset class X. Is the third word in the daiin→qo→X chain constrained? (2) Compare: in B, the three-word chain d→qo is suppressed (d avoids qo). In aiin-dom A, daiin→qo is enriched. Is there a preceding context that triggers the daiin→qo construction?
**Expected outcome:** If structured: the daiin→qo→X chain has a constrained third word (e.g., ch, or another d-word). If free: the third position is unconstrained (consistent with the onset-class grammar being the constraint, not word-level).
**Cost estimate:** small
**Prerequisites:** exp_076 (done)

---

## H112: The A ch Para-Final Pattern Is Driven by Specific ch-Words (chol, chor, chy, cthy)
**Priority:** medium
**Status:** tested — SUPPORTED (exp_077: daiin dominates A para-finals (12 occ, 2.08×); ch-onset para-finals distributed (chor=3, chory=2, then hapaxes). daiin is A's "para-closing particle." F084 added.)
**Source:** F083 (exp_076): In A, para-final last words show ch=23.9% (1.20×) enrichment, while within-para line-final ch is suppressed (0.83×). Which specific ch-onset words serve as A para-closers?
**Description:** List the most frequent ch-onset words at A para-final positions. Are they: (1) short ch-words (chol, chor, chy, ch) — suggesting a grammatical particle role? (2) The same as the most frequent A ch-words generally? (3) Different in section (Herbal A vs Pharma A para-closers)?
**Expected outcome:** If specific closers: cthy or chol may dominate (as these are high-frequency A ch-words). If distributed: any ch-word can close a paragraph. The specific words would constrain interpretations of A grammar.
**Cost estimate:** trivial
**Prerequisites:** exp_076 (done)

---

## H113: daiin Encodes Paragraph Position — Its Rate Varies Systematically From Para-Start to Para-End
**Priority:** high
**Status:** tested — STRONGLY SUPPORTED (exp_078: daiin rate rises 2.8× from para-first 2.44% to para-last 6.87%; last-token enrichment 6.11%. daiin is hierarchical boundary marker. F085 added.)
**Source:** F084 (exp_077): daiin accumulates multiple positional roles: line-final marker (1.41×), para-final marker (2.08×). It may encode paragraph POSITION — if daiin marks paragraph-ending positions specifically, its rate should rise toward the end of paragraphs.
**Description:** For Currier A paragraphs with 3+ lines: compute daiin rate by line position within paragraph (line 1=para-start, line 2, ..., last line=para-end). Does daiin become more frequent toward the end of paragraphs? Also: compute daiin rate by token position within a line (first word, middle words, last word). Are daiin's positional biases purely line-final, or does it accumulate toward paragraph end?
**Expected outcome:** If positional encoder: daiin rate rises toward para-end. If line-final marker only: daiin is enriched only at the last position of each line, uniformly across para-positions.
**Cost estimate:** small
**Prerequisites:** exp_077 (done)

---

## H114: The she- vs sh- Morphological Distinction in Currier A Generalizes Across Sections and Predicts qo-Following Rate
**Priority:** high
**Status:** tested — STRONGLY SUPPORTED (exp_078: she-→qo: A=2.41×, Pharma A=2.91×, B=2.19×; sh-other→qo: 1.18-1.45×. Cross-dialect and cross-section. F085 added.)
**Source:** F084 (exp_077): Pharma A she- forms (sheol, sheey, sheor) precede qo at 32.3% vs Herbal A short sh- forms (shol, sho, shor) at 12.9%. Is this a general rule: any she- prefix sh-word tends to precede qo, regardless of section?
**Description:** In all Currier A: split sh-words into she- prefix forms (words starting "she") vs short sh- forms (words starting "sho", "shy", "sha", etc.). For each group: (1) compute P(qo next); (2) compute P(ch next); (3) compare suffix distribution. Does the she- vs sh- distinction consistently predict qo-following rate across both Herbal A and Pharma A?
**Expected outcome:** If generalizes: she- forms precede qo more than sh- forms in all A sections. If Pharma-A-specific: she- forms only show elevated qo-following in Pharma A section.
**Cost estimate:** small
**Prerequisites:** exp_077 (done)

---

## H115: B Within-Para Line-Final Words (oly, otam, okam) Are Structurally Different From o-Onset Para-Final Words
**Priority:** medium
**Status:** tested — SUPPORTED (exp_078: oly=84.6%, okam=75.0%, oldy=80.0% line-final; never line-initial; preceded by o/ch. Form o→o→oly closing pattern. F085 added.)
**Source:** F084 (exp_077): Within-para B line-finals favor specific o-words: oly (7.27×), otam (5.57×), okam (6.21×), oldy (6.50×). Para-final B last words are diverse o-words with no dominant term. Are oly/otam/okam morphologically distinct from para-final o-words?
**Description:** (1) Compare suffix and stem distribution of oly/otam/okam/oldy vs the diverse para-final o-words. (2) Are oly/otam/okam also enriched in other positional slots (line-first, para-first)? (3) What precedes oly, otam, okam (onset class of the preceding word)?
**Expected outcome:** If structurally distinct: oly/otam/okam form a specific sub-class of o-words with a line-closing function (like function words). If coincidental: they appear frequently at line-ends because they're common words generally.
**Cost estimate:** small
**Prerequisites:** exp_077 (done)

---

## H116: The A Two-Register System (y-dom vs aiin-dom) Corresponds to Distinct "sh vs she-" Usage Patterns
**Priority:** medium
**Status:** tested — SUPPORTED (OPPOSITE DIRECTION) (exp_078: y-dom she-→qo=1.59× > aiin-dom she-→qo=1.18×. Aiin-dom uses qo→ch/s→ch pathways, not sh→qo. Two distinct grammar strategies. F085 added.)
**Source:** F084 (exp_077): Herbal A sh-words are dominated by short sh- forms (shol, sho, shor, shy). Pharma A uses she- prefix forms. F066/F069: A has two registers (y-dominant and aiin-dominant). Does the she-/sh- distinction extend to the register split within Herbal A? Does aiin-dominant Herbal A use more she- prefix sh-words than y-dominant Herbal A?
**Description:** Split Herbal A sh-words by register (aiin-dom vs y-dom folios). Compute: (1) fraction of sh-words that are she- prefix forms in each register; (2) sh→qo rate in each register; (3) whether the she-/sh- split predicts sequential coupling strength within Herbal A.
**Expected outcome:** If registers differ in sh-vocabulary: aiin-dom uses more she- forms and has stronger sh→qo; y-dom uses more short sh- forms. If vocabulary is consistent: the register split is driven by something other than sh-word morphology.
**Cost estimate:** small
**Prerequisites:** exp_077 (done)

---

## H117: The she-/sh- Distinction Corresponds to a Broader e-Vowel Infix Pattern in Voynichese (she-, che-, qoe-, oe-, de-)
**Priority:** high
**Status:** tested — STRONGLY SUPPORTED (exp_079: e-infix predicts higher qo-following in ALL onset classes in BOTH dialects. A: she-=2.41×, che-=0.93×, ke-=1.03×, oe-=1.02×, qoe-=1.62× (all > non-e forms). B: she-=2.19×, che-=1.36×, ke-=1.40×, oe-=1.54×, qoe-=1.60×. F086 added.)
**Source:** F085 (exp_078): she- prefix (she+stem) predicts higher qo-following rate vs sh+stem. This could be an instance of a general e-vowel infix in Voynichese: the difference between sh-forms and she-forms may reflect a broader morphological pattern where an internal 'e' vowel changes the sequential grammar of a word. Does the same pattern apply to other onsets? ch- vs che-? d- vs de-?
**Description:** For each major onset class (sh/sh-, ch/che-, d/de-, o/oe-, qo/qoe-), compare: (1) rate of qo-following for e-infixed vs non-e-infixed forms; (2) rate of ch-following; (3) frequency distribution by section. Does an e-vowel after the onset consistently shift the sequential behavior?
**Expected outcome:** If generalizes: she-, che-, de-, oe- forms all show different sequential behavior from sh-, ch-, d-, o- forms. If onset-specific: only she- shows the effect.
**Cost estimate:** small
**Prerequisites:** exp_078 (done)

---

## H118: The B o-Onset Line-Closers (oly, otam, okam) Have Currier A Equivalents (dal, daiin, or similar)
**Priority:** medium
**Status:** tested — SUPPORTED (exp_079: A has only 2 line-closers (sy: 90%, dam: 62.5%); B has 14. dam cross-dialect. B -am suffix forms a line-boundary class (6/14 words). F086 added.)
**Source:** F085 (exp_078): B has a class of o-onset line-closing words (oly, otam, okam, oldy: 65-85% line-final, preceded by o/ch). Does Currier A have equivalent line-closing words — specific words that are highly enriched at line-final positions and preceded by specific onset classes?
**Description:** For Currier A: identify words with ≥60% line-final rate and at least 10 occurrences. Compare their properties to B's oly/otam/okam. What onset class do A line-closers belong to? Are they d-onset (daiin is 1.41× line-final) or ch-onset, or another class?
**Expected outcome:** If A equivalents: A has a set of words analogous to B's o-onset line-closers, probably d-onset or ch-onset based on the general A line-final patterns. If no equivalents: A's line-final grammar is more diverse and doesn't concentrate in specific words.
**Cost estimate:** small
**Prerequisites:** exp_078 (done)

---

## H119: The Pharma A Section-Level qo Enrichment Is Driven by Specific Pharma Content (Measurement or Dosage Vocabulary)
**Priority:** medium
**Status:** tested — SUPPORTED (exp_079: Pharma A sh→qo elevation is sh-specific (2.44×); qo→qo suppressed (0.78×). Pharma A qo-vocabulary (qokeol, qokeey) resembles B's (qokeedy, qokedy) more than Herbal A's (qotchy). F086 added.)
**Source:** F085 (exp_078): In Pharma A, ALL sh-forms (including sh-other) precede qo at elevated rates (sh-other→qo=1.54× vs Herbal A 1.19×). This suggests a section-level grammar effect on top of morphological effect — the Pharma A grammatical context globally elevates qo-following. Does this reflect Pharma A having more qo-onset words generally, or a genuine sequential grammar change?
**Description:** (1) Compute qo-rate in Pharma A vs Herbal A vs other sections. (2) What follows qo in Pharma A (vs Herbal A)? (3) Are specific qo-words enriched in Pharma A? (4) Does the Pharma A sequential grammar differ in other ways besides sh→qo and she-→qo (e.g., o→qo, ch→qo)?
**Expected outcome:** If qo-enriched section: Pharma A has higher qo-rate which mechanically elevates all X→qo rates. If genuine grammar: qo-following rates are elevated even controlling for qo base-rate.
**Cost estimate:** small
**Prerequisites:** exp_078 (done)

---

## H120: The e-Infix Morphological Marker Co-Occurs with Specific Suffix Classes (e-Infix = Specific Syllable Template)
**Priority:** high
**Status:** tested — STRONGLY SUPPORTED (exp_080: B she-→-edy 29% vs sh-other→-dy 16%; A she-→-ey 20% vs sh-other→-aiin 9%. Complete syllable template {onset}+e+{stem}+{e-suffix} confirmed in both dialects. F087 added.)
**Source:** F086 (exp_079): e-vowel infix after onset universally predicts higher qo-following rate. Do e-infix words (she-, che-, ke-, oe-) also preferentially take specific suffixes? In B, she-forms (shedy, sheedy, sheey) take -edy/-eedy/-ey suffixes. Is there a coherent syllable template: {onset}+e+{suffix}?
**Description:** For each onset class, compare suffix distribution of e-infix vs non-e-infix forms. Do e-infix words take specific suffixes? Is the e-infix correlated with the -edy/-eedy suffix paradigm? If the template is {onset}+e+{edy/eedy/ey}, this would define a major morphological class of B words.
**Expected outcome:** If syllable template: e-infix words predominantly take -edy, -eedy, -ey suffixes, forming a coherent class. If uncorrelated: e-infix and suffix are independent dimensions.
**Cost estimate:** small
**Prerequisites:** exp_079 (done)

---

## H121: The B -am Suffix Class Is a Grammatical Line-Boundary Marker (Not Content Words)
**Priority:** high
**Status:** tested — STRONGLY SUPPORTED (exp_080: -am words 81.6% line-final vs 11.9% average; SUPPRESSED at para-final 7.7% vs within-para 14.0%; marks WITHIN-para line-boundaries NOT para-finals. B tripartite grammar: p-onset para-start → [-am line-ends] × N → o-onset para-end. F087 added.)
**Source:** F086 (exp_079): 6 of 14 B line-closers end in -am: am (81%), dam (77%), okam (75%), olkam (80%), qokam (86%), otam (66%). Is -am a grammatical suffix marking line-endings in B? Is -am also enriched at para-finals (B's o-onset para-closers)?
**Description:** (1) Compute line-final rate for ALL B words ending in -am vs corpus average. (2) Is -am enriched at para-final positions? (3) What precedes -am words? (4) Do -am words appear in labels? (5) Compare -am suffix distribution in A: does A have -am line-closers?
**Expected outcome:** If grammatical marker: -am words are systematically line-final, never line-initial, absent from labels, and preceded by specific onset classes. If coincidental: -am words are just common words that happen to appear at line-ends.
**Cost estimate:** small
**Prerequisites:** exp_079 (done)

---

## H122: Pharma A Is a Transitional Text — Closer to B Than to Herbal A in Sequential Grammar and qo-Vocabulary Despite A-Type Morphology
**Priority:** high
**Status:** tested — STRONGLY SUPPORTED (DISSOCIATION, NOT INTERPOLATION) (exp_080: Pharma A bigram PPL=12.9%≈B 13.3%; sh→qo=2.44×>B 1.97×; she-→qo=2.91×>B 2.19×; BUT -edy=0.47% vs B 18%; Jaccard with B=0.070 < Herbal A 0.100. NOT transitional — has B-strength grammar AND MORE DISTANT vocabulary than Herbal A. F087 added.)
**Source:** F083/F086 (exp_076/exp_079): Pharma A shows: (1) B-strength sh→qo coupling (2.44× vs B 1.97×); (2) B-like qo-vocabulary (qokeol, qokeey resembling qokeedy, qokedy); (3) she-→qo=2.91× (even stronger than B's 2.19×); (4) but pure A-type suffix morphology (-ol=18.2%, -edy=0.2%). Is Pharma A a "transitional" or "mixed" text — one that uses A-type words but B-type grammar?
**Description:** Systematically compare Pharma A to the spectrum from Herbal A to Currier B on multiple dimensions: (1) bigram onset-class PPL reduction; (2) specific B-diagnostic features (sh→qo coupling, qo-word vocabulary, e-infix prevalence); (3) suffix paradigm; (4) onset-class distribution. Where does Pharma A sit on the A-to-B gradient for each feature?
**Expected outcome:** If transitional: Pharma A sits between Herbal A and B on most sequential grammar features. If purely A with B-like qo: only the qo-handling differs, not the overall grammar.
**Cost estimate:** small
**Prerequisites:** exp_079 (done)

---

## H123: The e-Infix Syllable Template Defines a Complete Morphological Paradigm (e-Infix Defines Stem Class, Not Individual Words)
**Priority:** high
**Status:** tested — NOT SUPPORTED AS STATED (exp_081: e-infix is a vocabulary partition, not a productive morphological operation. 70-98% of stems are exclusive to e-infix or non-e contexts. In shared stems, suffix distributions identical (e-context 16-18% e-suffix ≈ non-e-context 14-22%). H120's e-infix→-edy correlation driven by MINIMAL WORDS (shedy=onset+e+suffix with no stem). F088 added.)
**Source:** F087 (exp_080): e-infix words take e-extended suffixes (B: -edy, -eedy, -ey, -eey; A: -ey, -eey) while non-e forms take -dy/-aiin. The co-occurrence suggests the e-infix is a CLASS marker. Do e-infix stems (the part between onset and suffix) appear consistently with ONLY e-extended suffixes? If shedy and sheedy share the same stem "sh" + e + d/dy, is there a systematic mapping from stem to suffix paradigm — i.e., given a stem, can you predict whether it takes e- or non-e suffixes?
**Description:** Extract stem from e-infix words by removing onset+e prefix and -edy/-ey/-eey/-eedy suffix. Do these stems ALSO appear in non-e contexts (sh+stem without e)? If shedy and shdy are both attested, do they use complementary suffixes? Or do certain stems appear exclusively in e-infix contexts? This tests whether the e-infix is a stem-class marker or a productive morphological operation.
**Expected outcome:** If stem-class: e-infix stems appear only in e-suffix contexts; non-e stems appear only in non-e contexts — two disjoint stem classes. If productive morphology: same stem appears in both e-infix and non-e contexts with different suffixes.
**Cost estimate:** medium
**Prerequisites:** exp_080 (done)

---

## H124: The B -am Suffix Suppression at Para-Final Reflects a Third-Person vs First/Second-Person Grammar (or Tense/Aspect Shift)
**Priority:** medium
**Status:** tested — PARTIALLY SUPPORTED (exp_081: B para-final suffix fingerprint is {-edy 16.2%, -aiin 11.8%, -eedy 7.4%}; within-para line-final fingerprint {-y 17.6%, -am 11.3%, -edy 12.0%}. -am modestly suppressed at para-final (10.3% vs 12.5%). Top B para-final word: chedy (5 occurrences). F088 added.)
**Source:** F087 (exp_080): -am words mark within-para line-ends (81.6%) but are SUPPRESSED at para-ends (7.7%). Para-ends use o-onset words (F083). What is the grammatical contrast between -am words and o-onset para-closers? Both are positional markers, but for different levels of structure. Does the -am suffix correspond to a specific grammatical feature (e.g., tense/aspect/person) that is appropriate for line-ends but not paragraph conclusions?
**Description:** (1) What suffixes do B para-final words actually take? Compare suffix distribution of para-final last words vs within-para line-final words. (2) Do o-onset para-final words take specific non-am suffixes? (3) Is there a COMBINATION of onset AND suffix that marks para-finals in B? (4) Does the -am suffix appear in A para-finals or only within-para?
**Expected outcome:** If grammatical contrast: para-final words take a different suffix class from within-para line-final words, suggesting -am and the para-final suffix encode different grammatical features. If positional only: the contrast is purely structural with no morphological parallel.
**Cost estimate:** small
**Prerequisites:** exp_080 (done)

---

## H125: The Pharma A Dissociation (Grammar-Morphology Independence) Extends to Aiin-Dominant Herbal A vs Y-Dominant Herbal A
**Priority:** high
**Status:** tested — STRONGLY SUPPORTED (exp_081: Aiin-dom: bigram PPL=5.8%, d→qo=1.90×, she-→qo=0.41× SUPPRESSED, -ol=13.6%, -or=12.2%, e-infix rate=7.54%. Y-dom: bigram PPL=4.0%, sh→qo=1.75×, she-→qo=2.23×, -ey=6.65%, -eey=5.99%, e-infix rate=12.59%. Grammar-morphology dissociation is GENERAL, not Pharma A anomaly. F088 added.)
**Source:** F087 (exp_080): Pharma A shows B-strength sequential grammar with A-type morphology. A similar dissociation might appear within Herbal A's two registers: aiin-dom has stronger overall bigram grammar (12.7% PPL reduction) vs y-dom (10.2%), while their suffix morphologies are similar (both use -aiin, -ol, -or, -y paradigm). Does aiin-dom have more B-like sequential grammar (higher sh→qo, stronger bigram coupling) independently of its suffix paradigm?
**Description:** (1) For aiin-dom vs y-dom Herbal A: compute the FULL onset-class transition matrix and compare each entry to B. (2) Compare suffix paradigm between aiin-dom and y-dom (are they actually the same morphologically, just different in daiin rate?). (3) Does the grammar-morphology dissociation pattern hold WITHIN Herbal A, not just in Pharma A? This would confirm that sequential grammar and morphological paradigm are independently varying throughout the corpus.
**Expected outcome:** If dissociation universal: aiin-dom's stronger sequential grammar is not accompanied by more B-like suffix morphology — grammar and morphology vary independently within A. If Pharma-A-specific: the dissociation is unique to Pharma A's section-level grammar, not a general feature.
**Cost estimate:** small
**Prerequisites:** exp_080 (done)

---

## H128: The Aiin-Dom Register's -ol/-or Suffix Dominance Reflects a Different Morphological Paradigm (Not Just More Liquid-Final Stems)
**Priority:** high
**Status:** tested — PARTIALLY SUPPORTED (exp_082: same top words (chol, shol, cthol, chor, shor) in both registers at higher rates in aiin-dom. Complementary substitution: -ol/-or replaces -ey/-eey for ch/sh stems (ch: aiin 37.2% vs y-dom 25.4% liquid; y-dom -ey=8.5%/-eey=4.0% vs aiin 5.0%/0%). Two sub-paradigms: liquid-final (aiin-dom) vs glide-final (y-dom). F089 added.)
**Source:** F088 (exp_081): Aiin-dom Herbal A has -ol=13.59% and -or=12.17% (25.76% combined), far above y-dom's -ol=6.45% and -or=5.88% (12.33% combined). This is a 2× difference in liquid-final suffix usage. Is aiin-dom using a different morphological paradigm where -ol/-or serve the role that -ey/-eey serve in y-dom? Or does aiin-dom have a different onset-class distribution that mechanically produces more -ol/-or?
**Description:** (1) Compute -ol/-or rate by onset class in aiin-dom vs y-dom. Are -ol/-or concentrated in specific onset classes in aiin-dom? (2) What words dominate aiin-dom's -ol/-or? Are they the same words as y-dom's top -ol/-or words? (3) Is the aiin-dom -ol/-or pattern driven by specific words (like daiin, daiin-followed words) or is it general? (4) Is there a complementary distribution: where y-dom uses -ey, aiin-dom uses -ol (same stems, different suffixes)?
**Expected outcome:** If different paradigm: -ol/-or in aiin-dom fills the grammatical role of -ey/-eey in y-dom; same stems appear with different suffixes in the two registers. If mechanical: aiin-dom just has more o-onset words (ol=short for o+l?), which take -ol suffix at higher rates.
**Cost estimate:** small
**Prerequisites:** exp_081 (done)

---

## H129: The she-→qo Suppression in Aiin-Dom (0.41×) Means e-Infix Words Mark NON-qo Transitions in Aiin-Dom (They Are ch-Predictors Instead)
**Priority:** high
**Status:** tested — SUPPORTED (exp_082: aiin-dom she-words are NEUTRAL for all classes (ch=1.02×, o=1.22×, sh=0.68×) — NOT ch-predictors, just qo-suppressors. Top aiin-dom she-words: shey(12), sheey(5), sheol(3) — minimal suffix forms. The e-infix carries zero qo-coupling information in aiin-dom. F089 added.)
**Source:** F088 (exp_081): In aiin-dom, she-prefix words suppress qo-following (0.41×, below base rate). If she-words don't predict qo, what DO they predict? The aiin-dom grammar uses qo→ch (1.23×) and d→qo (1.90×) — perhaps she-words in aiin-dom predict ch instead? Or d? This would mean the same morphological marker (she-) encodes OPPOSITE sequential information in the two registers — a fundamental inversion of the morphological grammar mapping.
**Description:** For aiin-dom: compute what follows she-prefix words. What onset class follows she- most often? Compare to: (1) what follows sh-other in aiin-dom; (2) what follows she- in y-dom; (3) what follows she- in B. Also: does the e-infix suppress qo in ALL onset classes in aiin-dom, or is it specific to sh-onset?
**Expected outcome:** If ch-predictor: she- in aiin-dom predicts ch-following (encoding the qo→ch grammatical pattern differently). If she- is neutral: she- in aiin-dom has no strong predictive bias for any onset class. Either way, the universal qo-coupling found in F086/H117 breaks down for aiin-dom.
**Cost estimate:** small
**Prerequisites:** exp_081 (done)

---

## H130: The B Paragraph Tripartite Grammar Is Detectable from Word Features Alone (Morphological Structure Parsing)
**Priority:** medium
**Status:** tested — FAILED (exp_082: para-boundary prediction F1<10% for all features. CRITICAL: p-onset is NOT B para-start marker — 0.0% rate at 101 B para-starts. B para-starts use o(36.6%)/qo(18.8%)/sh(14.9%). Revised model: -am suppressed 6.3× at para-final (2.0% vs 12.6%). F089 added.)
**Source:** F087/F088 (exp_080/exp_081): B has: p-onset para-starts, -am line-final markers (within-para), o-onset para-ends. The para-final suffix fingerprint is {-edy, -aiin, -eedy}. Can these markers be used to algorithmically parse paragraph structure from WORD FEATURES ALONE (without locus codes)?
**Description:** For each B line, code: first_word_p=(first word is p-onset?), last_word_am=(last word ends -am?), last_word_o=(last word is o-onset?). Train a simple rule: para_start predicted if previous line's last word was o-onset or -edy-suffix. Evaluate precision/recall using actual locus-code para-start markers. Also evaluate: how often does the tripartite structure BREAK (p-onset mid-para, -am at para-end, no marker at para-end)?
**Expected outcome:** If parseable: precision/recall >60% for para-boundary prediction from word features. If too noisy: the markers are probabilistic guides, not deterministic signals.
**Cost estimate:** small
**Prerequisites:** exp_081 (done)

---

## H132: The Liquid-Final (-ol/-or) vs Glide-Final (-ey/-eey) Suffix Substitution Involves Specific Stem Pairs (chol↔chey, chor↔cheor, shor↔sheor)
**Priority:** high
**Status:** tested — PARTIALLY SUPPORTED (exp_083: substitution is distributed, not concentrated. Best pair: o+k stem (aiin-dom 38% liquid vs y-dom 12%). No dominant word-pair alternation — it's a register-level paradigm shift across many stems. F090 added.)
**Source:** F089 (exp_082): Aiin-dom uses -ol/-or where y-dom uses -ey/-eey for ch/sh/cth stems. Top -ol words in aiin-dom: chol (53), shol (28), cthol (12); y-dom also has chol (70), shol (31) but uses more cheol, sheol. The substitution appears to be at the suffix level: chol in both registers (same word) + additional cheol/sheol variants in y-dom. Is there a true complementary pair: does chol appear MORE in aiin-dom while chey appears MORE in y-dom (using the same ch stem with different suffixes)?
**Description:** For key ch-stems (ch+ol, ch+ey, ch+or, ch+eor) and sh-stems (sh+ol, sh+ey, sh+or, sh+eor): compute rate in aiin-dom vs y-dom. Are chol and chey complementary across registers? Does shol substitute for shey? Create a "liquid-to-glide substitution table" showing which word pairs are register-complementary.
**Expected outcome:** If stem pairs: chol is enriched in aiin-dom; chey is enriched in y-dom; shol vs shey shows the same pattern; cthol vs cthey. If just rate: same words at different rates but no true complementary pair (chol high in BOTH but even higher in aiin-dom).
**Cost estimate:** small
**Prerequisites:** exp_082 (done)

---

## H133: B Para-Starts Are NOT Morphologically Marked — Paragraph Boundaries Are a Scribal/Layout Feature, Not Encoded in Word Grammar
**Priority:** medium
**Status:** tested — NOT SUPPORTED (OPPOSITE): B para-starts ARE marked: o-onset(2.42×), sh(1.72×), long words, -dy/-edy/-ey suffix (2.59×/1.68×/1.78×). -aiin(0.21×) and -eey(0.24×) suppressed. d/s/y/p/t suppressed. Top words: olfchedy(87.6×), olkey(58.4×). COMPLETE B MODEL: [o/sh+long-edy PARA-START] → [-am 12.6%] → [o+med-eedy PARA-END]. F090 added.)
**Source:** F089 (exp_082): B para-starts show no distinctive morphological marker: first-word onset is o (36.6%), qo (18.8%), sh (14.9%) — same as corpus base rates. p-onset is NOT enriched (0.0% at para-starts). Para-final lines also end with o-onset (32.7%) but many other onset classes too. The paragraph boundary appears to be a purely positional/scribal convention, not encoded in the word grammar.
**Description:** (1) Compare the FULL morphological profile of para-start first words vs non-para-start first words in B. Is there ANY feature (suffix, length, specific word) that distinguishes para-start lines? (2) Is the para-start word distribution indistinguishable from the general B word distribution? (3) If paragraph boundaries are purely scribal, should we expect the -am last-word marker to ALSO be purely positional (not grammatical)? (4) Compare A para-starts — does A show any morphological marking of para-starts?
**Expected outcome:** If no marking: B para-start words are statistically indistinguishable from general B words. If subtle marking: there exists some morphological feature (length, specific suffix, specific word) that is enriched at para-starts even if not dominant.
**Cost estimate:** small
**Prerequisites:** exp_082 (done)

---

## H135: The A Dialect Has a Para-Start Morphological Marker Analogous to B's -am Line-Final Marker
**Priority:** medium
**Status:** tested — STRONGLY SUPPORTED (exp_083: A para-starts use sh(2.54×)/ch(2.25×); d(0.21×)/y(0.38×)/t suppressed. daiin SUPPRESSED at A para-start(0.6%) and enriched at A para-final(8.6%). -am suppressed at A para-final(1.9% vs 6.4%) — cross-dialect finding. A model: [sh/ch PARA-START] → [-am 6.4%] → [daiin/ch PARA-END]. F090 added.)
**Source:** F089 (exp_082): B's -am is strongly suppressed at para-final (2.0% vs 12.6%). A has only 2 line-closing words (sy: 90%, dam: 62.5%). But what about A PARA-STARTS — is there a morphological marker for paragraph openings in A? daiin is a para-final marker in A (F084, exp_077); what marks para-starts?
**Description:** (1) For A para-start lines: what is the first-word onset distribution? (2) Are there specific words enriched at A para-starts? (3) Compare A para-start profile to B para-start profile. (4) Does daiin appear at different rates at A para-start vs para-mid vs para-final? (5) Is there a cross-dialect para-start marker (analogous to dam being cross-dialect)?
**Expected outcome:** If A marks para-starts: specific A words or onset classes are enriched at A para-start lines. If A doesn't mark para-starts: A para-start lines are indistinguishable from para-interior lines (unlike A para-finals where daiin is enriched).
**Cost estimate:** small
**Prerequisites:** exp_082 (done)

---

## H136: The B Para-Start ol-Prefix Word Class (olfchedy, olkey) Is a Distinct Morphological Class Marking Paragraph Openings
**Priority:** high
**Status:** tested — SUPPORTED (exp_084: ol-prefix splits into: (1) ol-line-closers (oly=88.6% line-last, oldy=78.6%) — pure line-final markers; (2) ol-para-starters (olkey=33.3% PSFirst, olkeeey=9.1%) — para-opening words. Two functional sub-classes based on stem after ol-. F091 added.)
**Source:** F090 (exp_083): Top B para-start first words are olfchedy (87.6× enrichment), olkey (58.4×), opchedy (7.6×) — all starting with o-onset + complex internal form + -edy/-ey suffix. The ol- prefix appears in both olfchedy and olkey. Is there a class of B words starting with "ol+" that are disproportionately paragraph-opening words? These words differ from the general o-onset words (otaiin, okeedy) that mark para-finals.
**Description:** (1) Extract all B words starting with 'ol': olkey, olfchedy, olkam, oly, oldy, etc. (2) Compute their positional statistics: line-final rate, para-start rate, para-final rate. (3) Are ol-prefix words specifically para-start markers (vs general o-onset words)? (4) What is the internal structure of ol-prefix words: onset=o + l + {complex stem} + {suffix}? (5) Do ol-prefix words and non-ol o-onset words have different positional roles?
**Expected outcome:** If ol-class: ol-prefix words are enriched at B para-starts AND line-finals (oly, olkam already known as line-final markers). The ol-prefix may mark BOTH line-starts and line-finals in different word types (oly/olkam for line-finals; olfchedy/olkey for para-starts).
**Cost estimate:** small
**Prerequisites:** exp_083 (done)

---

## H137: A Para-Start sh/ch-Onset Words Are Specifically the LONGER sh/che-Forms (sheol, shey) Not Short sh-Forms (shol, sho)
**Priority:** medium
**Status:** tested — STRONGLY SUPPORTED (exp_084: she-=4.74× at para-start vs sh-other=1.62×; she- is 3× more specifically a para-start marker. daiin=0.13× anti-para-start. FINAL A MODEL: [she-prefix PARA-START 4.74×] → [-am 6.4%] → [daiin/ch PARA-END 8.6%]. F091 added.)
**Source:** F090 (exp_083): A para-start top words: shey (4.4× enrichment), sheol (5.7×), shol (1.6×), shor (2.8×), chor (1.8×). The she-prefix forms (shey, sheol) have HIGHER enrichment than plain sh-forms (shol, shor). Does the she- prefix specifically mark A para-starts more than plain sh-forms? This would link the e-infix morphological class to positional marking.
**Description:** (1) Compare para-start rate for she-prefix sh-words vs plain sh-words in A. (2) Similarly: che-prefix vs plain ch-words at para-starts. (3) What is the para-final rate for she- vs sh-other? (daiin is para-final; are she-words NOT para-final?) (4) Is the e-infix's para-start enrichment related to its y-dom qo-coupling (she-→qo=2.23×)?
**Expected outcome:** If she-specific: she-words (shey, sheol) are more enriched at para-starts than plain sh-words (shol, sho). This would mean the e-infix marks paragraph openings in A, connecting morphological class to positional grammar.
**Cost estimate:** small
**Prerequisites:** exp_083 (done)

---

## H138: daiin Functions as a SENTENCE-FINAL (Not Just Para-Final) Marker in Currier A — It Marks the End of Syntactic Units at Multiple Levels
**Priority:** high
**Status:** tested — PARTIALLY SUPPORTED (exp_084: daiin shows binary-step pattern: first line=2.93% vs middle=4.83% vs last=6.50%. NOT smooth monotonic hierarchy — step function, not gradient. First-line avoidance is key (39% below middle). daiin-as-last-word: line 1=3.7%, later ordinals 3.7-11% (high variance). F091 added.)
**Source:** F090 (exp_083): daiin is enriched at A para-final (8.6%) but also appears as a line-final marker (1.41× enrichment from earlier experiments). The gradient from non-para-start first word (5.3%) to within-para last word (6.2%) to para-final last word (8.6%) suggests daiin marks hierarchical boundaries at increasing scales. If daiin marks multiple levels (line-end, para-end), it may be analogous to a sentence-final particle in natural language.
**Description:** (1) Within para-INTERIOR lines of A: compute daiin rate at different word positions (first word, middle, last word). (2) Compare daiin rate in short A paragraphs (2-3 lines) vs long paragraphs (5+ lines) at each line position. (3) Is daiin rate monotonically increasing as you approach para-final from para-start? (4) Does daiin appear preferentially at the end of the LAST WORD in lines that aren't para-final (i.e., as a within-para line-final marker too)?
**Expected outcome:** If hierarchical: daiin rate increases continuously from para-start (0.6%) → within-para lines → para-final (8.6%), with intermediate rates at para-interior line-ends. If binary: daiin only marks para-final, not intermediate positions.
**Cost estimate:** small
**Prerequisites:** exp_083 (done)

---

## H140: The she- Para-Start Function (4.74×) and the she-→qo Grammar Function (2.23×) Are the SAME Function — Paragraphs Opening with she- Develop sh→qo Sequences
**Priority:** high
**Status:** TESTED (exp_085) — REFUTED: The two functions are INDEPENDENT. she-→qo rates are nearly identical on para-start (27.5%) and non-para-start (24.1%) lines. qo-prediction is an INTRINSIC LEXICAL property of she-words, not a context-dependent para-start function. The two co-occur in she-lexemes but are not causally linked.
**Source:** F091 (exp_084): she-prefix words serve two roles: (1) para-start markers (4.74×); (2) qo-predictors in y-dom (2.23×). Are these the same phenomenon? Para-start lines that begin with she-words may subsequently contain more qo-onset words (because she-→qo and she-starts-para both predict qo following). Or are there two distinct she-functions that happen to co-occur?
**Description:** (1) For A para-start lines that begin with she-prefix words: what is the onset distribution of subsequent words ON THAT LINE? Is qo more frequent after she-para-start-words? (2) For A para-start lines that begin with sh-other words: what is the qo rate on that same line? (3) If she-→qo coupling operates both at line-start (she-opens-para) and mid-line (she-precedes-qo), then she- is a single grammatical category encoding "qo-transition topic/initiator". (4) For Pharma A: does she-→qo=2.91× track with a high para-start she-rate too?
**Expected outcome:** If unified: A paragraphs beginning with she-words have significantly more qo-onset words on the opening line and subsequent lines. If separate: the she-para-start function and she-→qo function operate independently in different syntactic positions.
**Cost estimate:** small
**Prerequisites:** exp_084 (done)

---

## H141: The B ol-Prefix Sub-Classes Reflect a Morphological Opposition Between "Line-Terminal" and "Line-Initiating" Stems
**Priority:** medium
**Status:** TESTED (exp_085) — PARTIALLY SUPPORTED: Stem complexity gradient exists (simple→line-closer 27.5% LLast; complex→para-starter 7.7% PSFirst) but weak. Specific lexical identity is a stronger predictor than stem structure. oly/oldy/olam (empty stems) are pure line-closers; olfchedy/olkair (complex stems) are para-starters. Gallows vs no-gallows does not cleanly separate roles.
**Source:** F091 (exp_084): B ol-prefix words divide into line-closers (oly=88.6% line-last, oldy=78.6%) and para-starters (olkey=33.3% PSFirst). The difference appears to be the stem AFTER 'ol': oly/oldy have simple stems (y, dy) while olkey/olfchedy have complex stems (key, fchedy). Is the morphological complexity of the ol-stem predictive of positional role?
**Description:** (1) For all B ol-prefix words: compute stem_complexity (length of the part between 'ol' and suffix). (2) Do shorter ol-stems (oly=stem+y, oldy=stem+dy) favor line-final positions while longer ol-stems favor line-initial? (3) More specifically: do ol+{short_stem} words favor line-ends; ol+{gallows_stem} (olkey, olfchedy — stems containing gallows letters k, f) favor line/para-starts? (4) Is the ol- prefix morphological class internally structured by stem type?
**Expected outcome:** If stem-structured: ol+{short/simple} → line-closer; ol+{gallows/complex} → para-starter. If lexically listed: the positional roles are determined by the specific words, not by the stem structure.
**Cost estimate:** small
**Prerequisites:** exp_084 (done)

---

## H142: The Complete Positional Grammar Models (A and B) Are Universal Across All Folio Sections — Not Section-Specific
**Priority:** medium
**Status:** TESTED (exp_086) — PARTIALLY SUPPORTED: Grammar models hold across herbal and pharma sections. she-para-start: herbal A=10.25×, pharma A=5.03×. B o-onset para-start: cosmo B=2.87×, herbal B=2.58×, pharma B=3.60×, stars B=1.56× (weakest). -am suppression at para-final: strong in B, weak in herbal A (1.75×). daiin para-final most specifically a Pharma A effect (2.87× vs herbal A 1.27×). Models break down in unclassified "other" sections.
**Source:** F090/F091 (exp_083/084): A model: [she-prefix PARA-START] → [-am line-ends] → [daiin PARA-END]. B model: [o/sh+long+edy PARA-START] → [-am line-ends] → [o+medium+eedy PARA-END]. Are these models consistent across all sections (Herbal A/Pharma A, Herbal B/Astro/Cosmo/Special) or section-specific?
**Description:** (1) Check if the -am within-para / para-final suppression holds for Pharma A, Astro B, and Special section separately. (2) Does the she-para-start model hold in Pharma A (which has different grammar from Herbal A)? (3) Does the B o-onset para-start model hold in all B sections (Bio/Pharma B/Special)? (4) Are there section-specific exceptions to the positional grammar?
**Expected outcome:** If universal: the positional grammar models hold across all sections, confirming they are grammar-level (not content-level) phenomena. If section-specific: some sections deviate, suggesting content drives positional word choice.
**Cost estimate:** small
**Prerequisites:** exp_084 (done)

---

## H143: The -am Suffix Has a Different Onset-Class Distribution Than Non-am Words — It Is Specifically a d-Onset and o-Onset Suffix
**Priority:** medium
**Status:** TESTED (exp_085) — STRONGLY SUPPORTED: -am is onset-structured. d-onset dominant in A (2.01×), d/t/o enriched in B (1.67×/1.55×/1.45×). sh-onset suppressed in BOTH dialects (A=0.56×, B=0.37×). p-onset completely absent in A (0.00%). Core cross-dialect -am vocabulary: dam, otam, qokam, okam. -am attaches predominantly to {t,k,d,r} short stems.
**Source:** F087/F090 (exp_080/083): Top -am words in B: otam (35), dam (31), qokam (22), okam (20), chdam (10), olkam (10), ram (10). Top A -am words: dam (32), cham (9), otam (7), okam (6). The -am suffix appears on words from diverse onset classes (d, o, qo, ch, r). Is there a pattern to WHICH onset classes take -am? Specifically: d-onset (dam, chdam) and o-onset (otam, okam, olkam) seem to dominate. Is -am more frequent after certain stems?
**Description:** (1) Compute -am suffix rate by onset class for B. (2) Compare: do d-onset and o-onset words have higher -am rates than qo/sh/ch-onset? (3) What is the internal structure of -am words: do they have specific stems (ot+am, ok+am, ol+k+am)? (4) Is the -am suffix productive (can be added to any stem) or lexically restricted?
**Expected outcome:** If onset-structured: -am is predominantly a d-onset and o-onset suffix class, reflecting a specific grammatical relationship between line-ending function and word onset. If general: -am attaches equally to any onset class stem.
**Cost estimate:** small
**Prerequisites:** exp_084 (done)

---

## H144: The -am Suffix Suppression in sh-Onset Is Related to sh-Onset Para-Start Enrichment — sh-Words Serve Opening Functions, Not Line-Ending Functions
**Priority:** medium
**Status:** TESTED (exp_086) — PARTIALLY REFUTED: sh-onset is NOT a pure line-opener (LFirst=20.7% A, 13% B; true line-openers are s=46%/61%, y=41%/44%). -am suppression for sh explained by sh's low LLast% (A=11%, B=6.8%) — mechanistic rather than grammatical incompatibility.
**Source:** F092 (exp_085): sh-onset is suppressed for -am in both A (0.56×) and B (0.37×). From F090/F091: sh-onset words are enriched at para-starts in both dialects (A=2.54×, B=1.72×). Hypothesis: sh-onset encodes an "opening/initiating" grammatical function; -am encodes "within-para line-ending"; these are functionally incompatible. sh-words cannot serve the line-ending role that -am marks.
**Description:** (1) Compute the positional profile of -am words vs non-am words by onset class: do -am words have suppressed line-first rates? (2) Does sh-onset have specifically SUPPRESSED line-last rates? (3) If sh-words never end lines (they start them), that explains zero -am rate. (4) Cross-validate: do sh-onset words have LOW LLast% in B? (from F089 data)
**Expected outcome:** If hypothesis correct: sh-onset words have very low LLast% AND very high LFirst% across both dialects — confirming sh-words are pure line-openers that cannot take -am (a line-ender marker).
**Cost estimate:** small
**Prerequisites:** F090 (exp_083), F092 (exp_085)

---

## H145: The core -am Vocabulary (dam, otam, qokam, okam) Represents a Closed Grammatical Class — a Small Set of High-Frequency Function Words That Mark Within-Para Line Endings
**Priority:** medium
**Status:** TESTED (exp_086) — STRONGLY SUPPORTED: {otam, qokam, dam, okam, cham, ram} all show LLast%=50-100%, WithinPara%=90-100%, PSFirst%=0%, PFLast%≈0% — confirmed closed class of within-para line-closers. daiin in B is LINE-OPENER (LFirst=34%), not line-closer — opposite from A.
**Source:** F092 (exp_085): Top B -am words: otam(27), dam(22), qokam(22), okam(19). Top A: dam(38), otam(13), cham(10). dam and otam appear in both dialects at high frequency. Hypothesis: these are FUNCTION WORDS from a small closed class, not open-class content words. Like daiin (para-closing) and oly (line-closing), dam/otam may be the core WITHIN-PARA line-ending function words.
**Description:** (1) Do dam/otam/qokam/okam show the characteristic function-word positional profile: high LLast%, low LFirst%, within-para enriched? (2) How do they compare to daiin (para-closing) and oly (line-closing)? (3) Are they contextually restricted (e.g. appear in specific folio sections or only with certain preceding words)? (4) Cross-dialect: in A, dam is 38× — is dam the primary within-para line-ending function word in A?
**Expected outcome:** If function words: dam/otam/okam have LLast% >>50%, LFirst%<<5%, and near-zero PSFirst rates. They would form a parallel paradigm to daiin (PSLast) and oly (LLast).
**Cost estimate:** small
**Prerequisites:** F092 (exp_085)

---

## H146: The Positional Grammar Models Are Falsifiable With a Held-Out Test Set — A Grammatical Parsing Attempt on New Sections
**Priority:** high
**Status:** TESTED (exp_090) — NOT FALSIFIED: she-prefix precision=45.7% (4.74×), astro A=100%. olfchedy/olkey/opchedy B precision=61.5% (14.72×). Cross-dialect combined: 1.95×. Daiin para-final weak (1.35×). Models are high-precision, low-recall on full corpus.
**Source:** F090/F091/F092 (exp_083/084/085): We have two full positional grammar models: A=[she-para-start → -am within-para → daiin/ch para-end]; B=[o/sh+long+edy para-start → -am within-para → o+med+eedy para-end]. Can these models PREDICT paragraph structure in new folios not used for model building?
**Description:** (1) Hold out a subset of folios (e.g., Pharma A, Astro B). (2) Use the positional grammar model to predict: which lines are para-starts, which are para-finals? (3) Evaluate precision/recall against the actual locus-code para-start markers. (4) What is the best predictor combination? Is it above chance?
**Expected outcome:** If grammar models are real: precision/recall for para-start prediction should exceed 30%/30% (far above the ~10% base rate). If over-fit to training data: prediction on held-out sections falls to chance.
**Cost estimate:** medium
**Prerequisites:** F090/F091 (exp_083/084)

---

## H148: daiin in Currier B Is a LINE-OPENER (34.0% LFirst, 9.5% LLast) — Completely Different Grammatical Role Than A (Where daiin Is a Line-Closer)
**Priority:** high
**Status:** TESTED (exp_087) — STRONGLY SUPPORTED: daiin-B pos0=33.2%, avg_position=0.387. daiin[0] in B followed by ch=37.9%/sh=35.6% (73.5% combined). Concentrated in Stars/Cosmo sections (70%). daiin-A: pos-last=25.2%, avg_position=0.558. Cross-dialect reversal confirmed.
**Source:** F093 (exp_086): In Currier B, daiin has LFirst%=34.0%, LLast%=9.5% — it functions as a LINE-OPENER, not a line-closer. In Currier A, daiin has LFirst%=19.4%, LLast%=25.9% — a line-closer/para-boundary marker. This is a fundamental cross-dialect reversal in daiin's grammatical role.
**Description:** (1) Verify the daiin-B line-opener finding: what words FOLLOW daiin on the same line in B? (2) What words PRECEDE daiin on the same line in B? (3) Is daiin predominantly the FIRST WORD of B lines (34% LFirst), or does it appear both first and mid-line? (4) Is the daiin-B line-opener consistent across all B sections, or concentrated in one section? (5) Can daiin's B role be described as a "line-initial discourse particle" (like how daiin marks line-endings in A)?
**Expected outcome:** If daiin is a B line-opener: most B daiin tokens should appear at line position 0 or 1 (first or second word), with specific following words. This would be a major grammatical discovery — the same word encoding opposite boundaries in two dialects.
**Cost estimate:** small
**Prerequisites:** F093 (exp_086)

---

## H149: The -am Function Words (otam, qokam, dam, okam) and the ol-Line-Closers (oly, oldy) Are Grammatical Synonyms — They Occupy the Same Syntactic Slot
**Priority:** medium
**Status:** TESTED (exp_087) — STRONGLY SUPPORTED: PERFECT complementary distribution — zero co-occurrence on same line (0/94, 0/42). Both uniformly distributed across para-positions. Section-level preference: -am dominates herbal B (7.2%)/stars B (4.5%); oly/oldy dominates cosmo B (3.8%).
**Source:** F093 (exp_086): Both -am core words and oly/oldy have LLast%=50-100%, WithinPara%=90-100%, PSFirst%=0%, PFLast%≈0%. They appear to be functionally synonymous. Do they occupy the same syntactic slot — i.e., are they in complementary distribution with each other ON THE SAME LINE?
**Description:** (1) On B lines that end with -am words: what other line-closing words appear? Do -am endings and oly/oldy endings alternate on different lines? (2) Are -am word endings and oly/oldy endings enriched in the same folio regions or different regions? (3) Do -am words and oly/oldy words share preceding contexts (same onset classes precede them)? (4) What is the overlap in preceding-word distributions?
**Expected outcome:** If synonymous slots: -am words and oly/oldy should be in near-perfect complementary distribution — any given line ends with EITHER an -am word OR oly/oldy, not both. If parallel: they might appear in different folio regions (section preference) while serving the same syntactic role.
**Cost estimate:** small
**Prerequisites:** F093 (exp_086)

---

## H150: The s-Onset and y-Onset (True Line-Openers by LFirst%) Have Complementary Grammatical Functions — s Marks One Line-Type, y Another
**Priority:** medium
**Status:** TESTED (exp_087) — PARTIALLY SUPPORTED: s-words → sh/ch following; y-words → qo/aiin following (distinct patterns). y-words are compound prefix forms (y+ch/k/sh/t+suffix). Top B s-opener: saiin(47). Top B y-opener: ycheey(9). Distinction confirmed but not fully characterized.
**Source:** F093 (exp_086): s-onset has LFirst%=45.9% (A) / 61.3% (B); y-onset has LFirst%=40.7% (A) / 44.4% (B). Both are strongly line-initial. But they have different LLast% and onset distributions. Are they grammatically distinct (s=topic opener, y=continuation/list) or synonymous?
**Description:** (1) Compare s-onset and y-onset positional profiles more finely: what words FOLLOW s-onset line-openers vs y-onset line-openers? (2) Do s-onset line-openers appear in different folio sections or paragraph positions than y-onset? (3) Are s-words and y-words in complementary distribution as LINE-OPENERS (one preferred over the other by section/position)? (4) What are the most common s-onset and y-onset line-first words?
**Expected outcome:** If complementary: s-onset and y-onset mark different line-types (e.g., s=standalone statement, y=continuation). If synonymous: they are interchangeable line-openers with no structural difference.
**Cost estimate:** small
**Prerequisites:** F093 (exp_086)

---

## H151: daiin-B as Line-Initial Connector Functions as a "Topic Continuation" Marker — The Preceding Line Always Ends With ch/sh-Onset Words
**Priority:** high
**Status:** TESTED (exp_088) — REFUTED: preceding line when daiin opens B ends with o-onset (35.2%, 1.27×); ch-onset SUPPRESSED (11.4%, 0.83×). Dominant 3-line pattern: [o-ending] → daiin-B → [o-ending]. daiin-B follows o-onset context, not ch/sh.
**Source:** F094 (exp_087): daiin-B at position 0 is followed by sh/ch-onset 73.5% of the time. Preceding daiin (within same line, mid-position): also ch-onset (chedy=10). Does the PRECEDING LINE (before daiin-opening line) end with ch/sh-onset words? If so, daiin is a CROSS-LINE CONNECTOR bridging two sh/ch-onset content sequences.
**Description:** (1) For each B line opening with daiin: what is the last word of the PRECEDING line? (2) Is the preceding line's last word predominantly ch- or sh-onset? (3) Does daiin-B line-opening predict that the NEXT line also opens with a ch/sh word? (4) What is the paragraph-position distribution of daiin-B openings? Do they appear at specific paragraph positions?
**Expected outcome:** If daiin-B is a cross-line connector: preceding lines should also end with ch/sh words at elevated rates. The pattern would be [ch/sh-ending line] → [daiin-B opener] → [ch/sh content], encoding a 3-line structural unit.
**Cost estimate:** small
**Prerequisites:** F094 (exp_087)

---

## H152: oly/oldy (Cosmo B) vs -am Words (Herbal B/Stars B) — Different Preceding-Word Distributions Reflect Content-Level vs Grammar-Level Line-Closing
**Priority:** medium
**Status:** TESTED (exp_088) — SUPPORTED: oly/oldy preceded by s-onset (6.88×), d-onset (3.06×), sh-onset (2.29×). -am preceded by ch-onset (inverse 0.57×), qo (0.76×). Perfect complementary distribution follows from selectional constraint on preceding onset class.
**Source:** F094 (exp_087): oly/oldy preferred in cosmo B (3.8% endings vs 2.0% for -am); -am preferred in herbal B (7.2% vs 0.7%). If these are functionally synonymous, why does section preference differ? Hypothesis: -am words are more "content-flexible" (can follow any onset class) while oly/oldy have specific preceding-word requirements that are more common in Cosmo.
**Description:** (1) For -am-ending lines: what is the SECOND-TO-LAST word (word preceding -am)? (2) For oly/oldy-ending lines: same analysis. (3) Is there an onset-class or morphological difference between words preceding -am vs oly/oldy? (4) Do oly/oldy endings always follow specific word classes (e.g., only after ch-onset words in cosmo B)?
**Expected outcome:** If content-driven: the words preceding oly/oldy should come from a restricted class specific to Cosmo vocabulary (e.g., only after specific plant/astrological terms). If grammar-driven: the difference is a section-level grammatical preference with no content explanation.
**Cost estimate:** small
**Prerequisites:** F094 (exp_087)

---

## H153: The y-Prefix System in B Is Parallel to the qo-Prefix System — y+[k/ch/sh/t] Are Line-Initial Compound Stems
**Priority:** medium
**Status:** TESTED (exp_088) — STRONGLY SUPPORTED (REVISED): y-compound is LINE-INITIAL (LFirst=47.3%, 3.75× enrichment in B; 40.3%, 2.24× in A). qo-prefix is MID-LINE (LFirst=11.3%, background). NOT parallel — they occupy opposite line positions. Both select k/t stems.
**Source:** F094 (exp_087): y-onset B line-first words are dominated by compound forms: ycheey, ykaiin, yshey, ychedy, yteey — all y+[onset]+suffix. y-prefix attaches to the same onset classes (k, ch, sh, t) as qo-prefix. Is y- a LINE-INITIAL morphological prefix parallel to qo-? The qo-prefix appears in body text positions; does y- appear specifically at line-initial positions?
**Description:** (1) Compare onset-class distribution of y-prefix stems vs qo-prefix stems. (2) Are y-compound words EXCLUSIVELY line-initial (LFirst%>>50%)? (3) Do y-compound words appear in the same folio sections as qo-compound words (B dialect throughout)? (4) Are there y-prefix stems that appear WITHOUT being line-initial (mid-line y-words)? (5) Does y- encode a different grammatical meaning than qo- (which is a body-text form in F037)?
**Expected outcome:** If y-prefix is a line-initial morpheme: y-compound words (ykaiin, ycheey, ychedy) should have LFirst% >>50% and appear only at line-starts. They would form a line-initial paradigm distinct from qo-prefix (which can appear mid-line).
**Cost estimate:** small
**Prerequisites:** F093/F094 (exp_086/087)

---

## H154: y+{Stem} and qo+{Stem} Are LINE-INITIAL vs MID-LINE Alternants of the SAME Stem — A Positional Morphological Paradigm
**Priority:** high
**Status:** TESTED (exp_089) — STRONGLY SUPPORTED: B shows 3.12× y/qo LFirst ratio across 81 shared stems (bare=8.9%, qo=11.6%, y=36.2%). Individual stems: tal=8.17×, tchedy=6.00×, tar=5.27×. A weaker (1.28×). Prefix-encoded positional paradigm confirmed for B.
**Source:** F095 (exp_088): y-compound selects k/t stems (ykaiin, ykeey, ytaiin, yteedy) — the same stem class as qo-prefix (qo-stems are 60.5% k-initial, 21.2% t-initial). y-compound LFirst=47.3% (line-initial); qo-prefix LFirst=11.3% (mid-line). Hypothesis: y+{stem} is the LINE-INITIAL form of the k/t-stem paradigm, while qo+{stem} is the MID-LINE form. Same content word appears with different position-marking prefix depending on where it falls in the line.
**Description:** (1) Take the top y-compound words (ykaiin, ykeey, ytaiin, yteedy). Strip y-prefix to get stem: kaiin, keey, taiin, teedy. (2) Do these stems also appear as qo+stem forms (qokaiin, qokeey, qotaiin, qoteedy)? (3) What are the positional profiles of ykaiin vs qokaiin, ykeey vs qokeey? Are they complementarily distributed by line position? (4) Compute: for stem X, what % of yX tokens are line-initial and what % of qoX tokens are line-initial? Is there a consistent y-initial/qo-mid pattern?
**Expected outcome:** If positional alternation: ykaiin should be predominantly line-initial and qokaiin predominantly mid-line; the two forms occupy complementary positions. This would establish a POSITIONAL PREFIX PARADIGM: LINE-START → y-{stem}; MID-LINE → qo-{stem}.
**Cost estimate:** small
**Prerequisites:** F095 (exp_088)

---

## H155: The Complete B Line Structure [y/s → qo → -am/oly] Can Be Verified as a Sequence Pattern — What Fraction of B Lines Follow This Template?
**Priority:** high
**Status:** TESTED (exp_089) — NOT SUPPORTED: Full template only 0.7% (chance=0.8%, enrichment=0.95×). Components are INDEPENDENT. qo-mid pervasive (65.4%); opener/closer optional (20.8%/5.6%). B line grammar is modular, not rigid sequence.
**Source:** F095 (exp_088): Proposed B line structure: [y-compound or s-onset LINE-OPENER] → [qo-prefix MID-LINE] → [-am or oly/oldy LINE-CLOSER]. Is this actually a common B line template? Or is the line structure more variable?
**Description:** (1) Classify each B line word-by-word: opener (y-compound or s-onset at pos0), mid (qo-prefix anywhere mid-line), closer (-am or oly/oldy at final). (2) Count how many B lines have the full [opener → qo-mid → closer] structure. (3) Count lines with partial matches (opener only, closer only, qo-mid only). (4) What fraction of B lines have NO opener/mid/closer — are there blank-template lines? (5) Compare: lines that DO follow the template — are they from specific sections?
**Expected outcome:** If template is real: 15-30% of B lines follow the full [opener → qo-mid → closer] pattern (much above the ~1-3% expected by chance). If template is just statistical: the overlap is at chance levels.
**Cost estimate:** small
**Prerequisites:** F093/F094/F095 (exp_086/087/088)

---

## H158: d+ch Compound Words in A (dchor, dchol, dchey) Are A's Line-Initial Opener System
**Priority:** high
**Status:** TESTED (exp_091) — STRONGLY SUPPORTED (REVISED): A has TWO line-initial systems: y+ch (LFirst=85.9%, 8.86× vs bare) and d+ch (LFirst=59.6%, 6.17× vs bare). Bare ch = background (9.7%). Three-tier paradigm: bare < d+ch < y+ch in LFirst%.

---

## H159: Three-Level Positional Paradigm for ch-Stems in A (Analogous to B's bare/qo/y Paradigm)
**Priority:** high
**Status:** TESTED (exp_091) — STRONGLY SUPPORTED: A ch paradigm: bare (9.7%) << d+ch (59.6%, 6.17×) ≤ y+ch (85.9%, 8.86×). No mid-line prefix identified in A (unlike B's qo-prefix). A has 2-tier prefix system (both d and y = line-initial) vs B's 3-tier (bare < qo-mid < y-initial).

---

## H160: A Mid-Line ch-Onset Words Form a Self-Continuing Sequence — ch→ch Is the Dominant A Line Interior
**Priority:** medium
**Status:** TESTED (exp_091) — CONFIRMED: ch→ch at pos2 = 28.4% (most common continuation). Bare ch-onset at pos1 dominated by chol(78), chor(50). A line structure is modular: [d+ch/y+ch opener] → [bare ch mid ×N] → [d-closer]. Template enrichment modest (1.29×).

---

## H161: The A Line-Initial y+ch System and the A Line-Initial d+ch System Have Different Preceding/Following Contexts
**Priority:** medium
**Status:** TESTED (exp_092) — CONFIRMED WITH EXTENSION: Both have 0% para-start rate (WITHIN-PARA line openers only, not para starters). y+ch→o-onset following (24.3%, 8.15× over d+ch); d+ch→qo-onset following (16.4%, 6.07× over y+ch). d+ch follows d-ending lines (35.7%); y+ch follows o-ending lines (23.0%). 10 shared ch-stems → prefix marks position, not lexicon. 17/87 paras have both forms (not complementary). d-chain identified: d-closer→d+ch opener.

---

## H162: sh-Stem Positional Paradigm in A
**Priority:** high
**Status:** TESTED (exp_092) — STRONGLY SUPPORTED: sh-stems show same 3-tier paradigm: bare sh(13.2%) << d+sh(68.8%, 5.21×) ≤ y+sh(85.7%, 6.49×). Nearly identical to ch-stem ratios (6.17×/8.86×). Universal in A: applies to both ch- and sh-stems. d+sh n=48, y+sh n=21.

---

## H163: A Para-Starts Are Dominated by p/t/k-Onset Words (NEW FINDING)
**Priority:** high
**Status:** TESTED (exp_092) — NEW FINDING CONFIRMED: A para-starts dominated by p-onset (12.41× enrichment, 28.8% of PS lines), k-onset (4.32×), t-onset (2.72×). y+ch and d+ch = 0.0% at para-starts (suppressed). Revised A grammar: Para-starter (p/k/t) > Line-opener (y+ch/d+ch/y+sh/d+sh) > Mid-line (bare ch/sh) > Line-closer (d+suffix).

---

## H164: A Para-Start p-Onset Words Are a Specific Closed Class
**Priority:** high
**Status:** TESTED (exp_093) — CONFIRMED WITH EXTENSION: p-onset enrichment real (12.41×) but OPEN CLASS (43 unique forms). p- PREFIX marks para-initial position; stems vary. p+ch/sh/o = A para-start morphemes. p- is A's THIRD POSITIONAL PREFIX. High-enrichment forms: pchor(9.5×), pcheol(9.5×), podaiin(19.0×).

---

## H165: d-Chain Pattern — d-Closer Triggers d+ch Opener
**Priority:** medium
**Status:** TESTED (exp_093) — CONFIRMED (MODEST): d+ch after d-closer = 1.76× (P=6.6% vs 3.7%). y+ch SUPPRESSED (0.61×) after d-closer. Chains mostly length=1 pairs. o→y+ch weaker (1.20×). Effect real but not dominant.

---

## H166: Cross-Dialect Para-Start Onset Comparison
**Priority:** high
**Status:** TESTED (exp_093) — STRONGLY CONFIRMED UNIVERSAL GRAMMAR: p-onset (A=12.41×, B=3.71×), k-onset (A=4.32×, B=9.91×), t-onset (A=2.72×, B=2.05×) ALL enriched at para-starts in BOTH dialects. y/d/qo/s/sh suppressed in BOTH. Gallows-onset words = PARAGRAPH-LEVEL POSITIONAL CLASS across manuscript. Complete 4-level grammar: Para(p/k/t) → Line-opener(y+/d+) → Mid-line(bare/qo) → Closer(-am/d+).

---

## H167: k-Onset A Para-Start Words
**Priority:** high
**Status:** TESTED (exp_094) — CONFIRMED: k-onset is OPEN CLASS para-start marker; all individual words are hapaxes. Same pattern as p-onset. Both k and p use onset character to encode para-start, with variable stems.

---

## H168: All Four Gallows Characters Are Para-Start Enriched
**Priority:** high
**Status:** TESTED (exp_094) — STRONGLY CONFIRMED: p(A=12.41×,B=3.71×), k(A=4.32×,B=9.91×), t(A=2.72×,B=2.05×), f(A=9.50×,B=7.62×) all enriched. Non-gallows all suppressed. Gallows glyph class = PARA-LEVEL positional morpheme class.

---

## H169: qo+Gallows and y+Gallows Suppressed at Para-Starts
**Priority:** high
**Status:** TESTED (exp_094) — STRONGLY CONFIRMED: qo+gallows = 0.27-0.32× PS suppressed; y+gallows = 0.19-0.40×. Prefix DEMOTES gallows from para-level to line-level. MASTER FINDING: morphological prefix = positional demotion mechanism.

---

## H170: Complete Gallows Positional Hierarchy
**Priority:** high
**Status:** TESTED (exp_094) — CONFIRMED: Same hierarchy in A and B. bare_p strongest para-starter (A=40.2%!, B=10.7%). y+gallows = within-para line-opener (LFirst=30%). qo+gallows = mid-line. bare_ch = mid-line/closing. Four-level grammar: bare gallows(para) > y/d+gallows(line-open) > qo+gallows(mid-line) > bare non-gallows(closing).

---

## H171: Internal Gallows Hierarchy — p > f > t > k for Para-Start Specialization
**Priority:** medium
**Status:** TESTED (exp_095) — SUPPORTED: Platform gallows (p,f) consistently > Regular gallows (t,k) for PS rate. Bare: p=40%>f=24%>t=10%>k=6%. +ch: p=27%>f=21%>t=4%>k=4%. Consistent across herbal and pharma A.

---

## H172: p+ch = A Para-Starter (Gallows-Demotion Model for ch-Stems)
**Priority:** high
**Status:** TESTED (exp_095) — STRONGLY CONFIRMED: p+ch=26.9% PS (61.5% LFirst); f+ch=21.4% PS. y/d+ch=0% PS (line-openers). bare_ch=0.3% PS (mid-line). Complete 5-level ch-stem hierarchy.

---

## H173: p+sh = A Para-Starter for sh-Stems
**Priority:** high
**Status:** TESTED (exp_095) — STRONGLY CONFIRMED: p+sh=33.3% PS; t+sh=28.6% PS; y/d+sh=0%; bare_sh=1%. IDENTICAL hierarchy to ch-stems. Universal prefix×stem positional system confirmed.

---

## H174: Complete Prefix × Stem Matrix
**Priority:** high
**Status:** TESTED (exp_095) — COMPLETE MATRIX: Para-level={p,f,t}+stem or bare_p/f (PS=20-56%); Line-opener={y,d}+stem (PS=0%, LFirst=55-86%); Mid-line=bare_ch/sh/qo+gallows (PS≈0%). Three clean tiers.

---

## H175: B Dialect Gallows+Stem Para-Start Hierarchy
**Priority:** high
**Status:** TESTED (exp_096) — STRONGLY CONFIRMED: p+ch=11.6% PS in B (para-level, same as A=26.9%); y+ch=0% PS (line-opener); d+ch=0% PS (line-opener); bare_ch=0.1% PS (mid-line). SAME role in both dialects.

---

## H176: B k-Onset Concentration Analysis
**Priority:** medium
**Status:** TESTED (exp_096) — CONFIRMED: B bare_k 9.91× enrichment is a contrast effect. bare_k is mostly mid-line (92%). Para-start count is only 8 tokens. The high ratio arises because k is very rare at within-para line-first (0.78%).

---

## H177: Unified Cross-Dialect Gallows Grammar
**Priority:** high
**Status:** TESTED (exp_096) — STRONGLY CONFIRMED (F103): Prefix = positional morpheme universally. {p,f}+stem=para; {y,d}+stem=line-opener; {qo}+gallows/bare_ch=mid-line. SAME class has SAME role in BOTH dialects. Stem = content; prefix = position.

---

## H178: Stem × Prefix Independence
**Priority:** high
**Status:** TESTED (exp_097) — PARTIALLY CONFIRMED: Core stems (chol, chor, cheey) appear with ALL prefix classes. 87.8% exclusivity is frequency-driven (rare stems don't have enough tokens to appear in all contexts). Consistent with productive morphology.

---

## H179: f+ch Cross-Dialect Asymmetry
**Priority:** medium
**Status:** TESTED (exp_097) — CONFIRMED: f+ch asymmetry is real and section-driven. A: f+ch in herbal (21% PS). B: f+ch in stars (0% PS, B-type suffixes). Genuine dialect difference in f-gallows para-start usage.

---

## H180: Stem Productivity Gradient
**Priority:** medium
**Status:** TESTED (exp_097) — CONFIRMED: 3 fully-productive stems (all 7 prefix classes): chol, cheey, cho. Zipfian distribution: ~16 productive stems = 47% of ch-stem tokens. Consistent with natural language morphology.

---

## H181: Positional Grammar Classifier Accuracy
**Priority:** high
**Status:** TESTED (exp_098) — CONFIRMED: LINE_OPEN tier is categorically excluded from para-starts (B=100% clean, A=98.6% clean). PARA tier: A=55.6% precision (11.8× enriched), B=14.8% precision (3.94× enriched). ~54% of para-starts have "OTHER" words — major classifier coverage gap. WEAK_PARA also enriched (2.6-3.4×).

---

## H182: Paragraph Internal Structure Template
**Priority:** high
**Status:** TESTED (exp_098) — CONFIRMED: Sharpest morphological transition in MS is para-boundary. PARA markers: 33%→0.6% (line 1→2, 55× drop). LINE_OPEN: 2.4%→29% (12× jump). Within-para structure is uniform (no distinct closing morphology). Para-final words are o-ending (27-35%) and d-ending (24% A). Canonical sequence: PARA-opener → LINE_OPEN on lines 2+.

---

## H183: Paragraph Length by Section
**Priority:** medium
**Status:** TESTED (exp_098) — CONFIRMED: Stars(B)=47 lines, cosmo(B)=25 lines, herbal(A/B)=12-13 lines, pharma(A)=7.7 lines, astro(A)=3.4 lines. Para length is section-determined.

---

## H184: "OTHER" Para-Start Investigation
**Priority:** high
**Status:** TESTED (exp_099) — CONFIRMED: "OTHER" PS words dominated by bare_k (9-12× enriched) and bare_t (3.25× A). These are bare gallows para-starters missing from classifier. Extended PARA tier = {p,f}+stem + bare_k + bare_t covers ~65-70% of para-starts.

---

## H185: Para-Final o-Onset Specialization
**Priority:** medium
**Status:** TESTED (exp_099) — PARTIALLY CONFIRMED: o-onset mildly enriched (A=1.52×, B=1.25×). B has stronger para-final specialization: sh-onset (2.88×) and words okeey (16.4×), orol (21.9×), shedy (6.25×). P-onset perfectly excluded from para-finals (0.00×).

---

## H188: Extended Positional Classifier
**Priority:** high
**Status:** TESTED (exp_100) — CONFIRMED: v2 classifier (PARA = {p,f}+stem + bare_k + bare_t) doubles PS coverage (33%→54% A, 39%→54% B). OTHER shrinks to 18-24%. Remaining OTHER is 52-63% o-onset. LINE_OPEN still 0/100% clean. PARA enrichment: 6.58× A, 3.48× B.

---

## H189: B Para-Final Closing Vocabulary
**Priority:** medium
**Status:** TESTED (exp_100) — PARTIALLY CONFIRMED: okeey/okeeey (∞), orol (21.9×), shedy (6.25×, cosmo-specific). Closing class covers only 22.8% of para-finals. No universal B para-final morphological class. Most B paragraphs end with hapax/section-specific words.

---

## H190: Astro Section Anomalous Para-Start Grammar
**Priority:** medium
**Status:** TESTED (exp_100) — CONFIRMED: Astro A has relaxed grammar: 50% OTHER, LINE_OPEN at para-starts (11.5%), t/o onset dominant. Short captions don't follow the strict positional grammar of long-paragraph sections.

---

## H191: o-Onset Para-Start Words
**Priority:** high
**Status:** TESTED (exp_101) — CONFIRMED (negative): o-onset is NOT a coherent para-start class (0.52× A suppressed, 1.28× B neutral). Only "op-" sub-onset (9.5×) is para-enriched — via internal p-gallows. olfchedy/olfchey are enriched via internal f+ch morphology. ~17-20% OTHER after v3 is genuinely diverse vocabulary beyond the grammar system.

---

## H192: Grammar Strength vs Paragraph Length
**Priority:** medium
**Status:** TESTED (exp_101) — STRONGLY CONFIRMED: Para-start grammar strictness scales with paragraph length. A long (10-15 lines): 70.7% PARA, 0% LINE_OPEN — strictest in manuscript. A short (2-4 lines): 31% PARA, 8.6% LINE_OPEN allowed. B monotonically increasing (22%→65%), never violates LINE_OPEN exclusion.

---

## H193: Section vs Length Grammar Separation
**Priority:** medium
**Status:** TESTED (exp_102) — PARTIALLY CONFIRMED: Grammar strictness is primarily section-driven. Within herbal A, shorter paras have HIGHER PARA% (reversed from H192). Within cosmo B, length has genuine positive effect. H192 cross-section gradient = section composition artifact.

---

## H194: Content Word Analysis
**Priority:** high
**Status:** TESTED (exp_102) — CONFIRMED: ch-stem content words show strong section-specific vocabulary. Herbal A: chain, chocthy, choiin exclusive; Pharma A: cheol (6.1×), cheeor (10.4×) enriched; Stars B: cho/cheo/cheeo exclusive; Cosmo B: chcthy/checthy enriched. Each section has distinctive ch-stem morphological signature. PARA+LO+WEAK tiers = only 10-20% of all tokens; ~80% are content words (MID+OTHER).

---

## H195: Section Classifier from ch-Stems
**Priority:** high
**Status:** TESTED (exp_103) — CONFIRMED: ch-words achieve 73% of full-vocabulary classification power. Most informative: herbal A = chaiin, char; pharma A = cheom, cheodal; stars B = cheeo, chokaiin; cosmo B = checthy.

---

## H196: Cross-Dialect ch-Stem Comparison
**Priority:** medium
**Status:** TESTED (exp_103) — CONFIRMED: Jaccard=0.181 (below independence expectation 0.62×). A and B ch-vocabularies are ANTI-CORRELATED — more distinct than random. B-exclusive: chedar, chdaiin, chdal (ch+d cluster). chedy is 43.9× more common in B than A.

---

## H197: B ch+d Cluster Pattern — Is "chd" a Morphological Unit in B?
**Priority:** medium
**Status:** TESTED (exp_104) — CONFIRMED (negative): "chd" is NOT a morphological unit. ch+d forms are ch-onset + B-type -edy/-dy suffix. Identical positional profile to bare_ch (mid-line). -edy enriched 2.97×; -y/-ey suppressed to 0.06×. The B-exclusive ch+d cluster from F110 is explained by B's suffix preference, not new morphology.
**Source:** F110: B-exclusive ch-words include chedar(25), chdaiin(17), chdal(16), chdar(15), chdam(10), chdor(9). These share a ch+d structure. Is "chd" a distinct B-morphological unit (ch-onset followed by d-element), or are these coincidental forms?
**Description:** Extract all B words starting with "chd". Compute their positional distribution (PS/LFirst/LLast). Are they mid-line content words (MID tier) or have different positional behavior? Compare suffix patterns of chd-words vs bare ch-words.
**Expected outcome:** chd-words are mid-line content words with B-type -aiin/-al/-or suffixes, confirming they are ch-stems followed by d-element (possibly a B-specific infix).
**Cost estimate:** small

---

## H198: Vocabulary Growth (Heaps' Law) by Section — Does Voynichese Vocabulary Grow at Natural Language Rates?
**Priority:** medium
**Status:** TESTED (exp_104) — CONFIRMED: Voynichese follows Heaps' law. Section-level β=0.661-0.744 (upper end of NL range 0.5-0.7). B cosmo=0.674 (most repetitive); A herbal=0.744, B stars=0.735. Overall A/B β=0.84 is artifact of cross-section vocabulary divergence. Consistent with natural language statistics.
**Source:** (new direction): In natural languages, vocabulary grows as V=K*N^β where β≈0.5-0.7. Does Voynichese follow Heaps' law? And do different sections follow the same law?
**Description:** Plot cumulative unique words vs cumulative word tokens for each section. Fit V=K*N^β. If β≈0.5-0.7: natural language-like growth. If β<0.3: repetitive/formulaic. If β>0.8: artificial/random.
**Expected outcome:** Heaps' β≈0.5-0.6 consistent with natural language, varying by section. Stars (B) may have lower β (more repetitive) than herbal (A).
**Cost estimate:** small

---

## H200: "OTHER" Vocabulary Tier — What Are the Mid-Line Words Not Classified by Positional Grammar?
**Priority:** high
**Status:** TESTED (exp_105, exp_106) — CONFIRMED: OTHER=43.8% of tokens. Sub-structure: o-prefix 37% (ok/ot/ol), d-onset 19%, particles 9%, s-openers 6%. exp_106 extended: o-prefix body=19% all tokens; 28.3% stem overlap with qo-body; o-prefix obeys A/B suffix paradigm (A:-ol/-or; B:-edy/-eedy). or-onset=closer (40.6%LL); ok/ot=mid-line (14-16%LL).
**Source:** exp_100-102 found that PARA+LINE_OPEN+WEAK_PARA+MID covers only ~50-60% of all tokens. The remaining "OTHER" 40-50% are mid-line content words with diverse vocabulary. What is the structural character of these words? Are they: (1) qo-onset words not yet classified? (2) o-onset content words? (3) Short 2-4 character words? (4) Section-specific unlabeled vocabulary?
**Description:** Extract all "OTHER" tier tokens from the v3 classifier (not PARA, LINE_OPEN, WEAK_PARA, or MID). Compute: onset distribution, length distribution, suffix distribution, section distribution, positional stats (PS/LFirst/LLast). Compare to MID tier (ch/sh onset) to understand how OTHER differs structurally. Look for sub-classes within OTHER that have consistent structural patterns.
**Expected outcome:** OTHER is dominated by (a) o-onset words without gallows (like ol, or, okey, okain — simple closers/openers), (b) short 2-3 char words (particles?), (c) rare hapax forms. These may represent function words, grammatical particles, or the actual content vocabulary of the manuscript.
**Cost estimate:** medium

---

## H201: Cross-Section Universal Vocabulary — Are There Words Appearing in ALL Sections With High Frequency?
**Priority:** medium
**Status:** TESTED (exp_105) — CONFIRMED: 44 universal words in all 5 sections (≥3 tokens). Universal tokens = 21-28% of each section. Universal words: OTHER (57%) + MID (41%). No PARA words are universal. B_stars=215 exclusive words (most diverse); B_herbal=12 (most shared). A_herbal exclusive: cth-cluster forms.
**Source:** F109-F111 established section-specific ch-vocabularies. But some words must be "universal" — appearing in all sections at significant rates. Identifying these could reveal grammatical function words (like "the", "of", "and" in English) vs content words.
**Description:** For each section (A herbal, A pharma, B cosmo, B stars, B herbal), compute the set of words appearing with rate > 0.5‰. Intersect these across all 5 sections. Words in the intersection are "universal" — appearing in all sections at non-trivial frequency. Then compute which of these universal words are also the highest-rank words overall. Compare: are universal words predominantly PARA tier (gallows-onset) or MID tier (ch/sh) or OTHER?
**Expected outcome:** Universal words are predominantly grammar words: daiin (line-connecting particle), aiin (B suffix pattern), qokeedy/qokeey (B function words), olkeedydy (formulaic). Section-specific words are content words. The split would strongly support a two-tier vocabulary model (grammar words + content words).
**Cost estimate:** small

---

## H202: o-Prefix Body Words (ok/ot/ol) as the Body-Text Counterpart to Label System — Does the o-Prefix System in Body Text Decode as Object-Naming Vocabulary?
**Priority:** high
**Status:** CONFIRMED PARTIAL (exp_130) — ok/ot body words are B-dialect medial content nouns (81-82%MID); stars/cosmo 38-45%; Jaccard=0.197(ok)/0.139(ot)/0.062(ol) with labels (low overlap); ok/ot body vocabulary DISTINCT from label vocabulary; line-closers: oly=81.2%LL, otam=62.8%LL; ok/ot body=B-dialect nominal class parallel to A-dialect cth-nouns (F137)
**Source:** F112: OTHER tier is dominated by ok+/ot+/ol+ words (37% of OTHER). F043: o-prefix in labels parallels qo-prefix in body text (three-prefix system). But ok/ot-onset OTHER words are NOT qo-words — they are SEPARATE body-text vocabulary. Do ok/ot words in body text correlate with labeled objects? Do ok-onset body words appear near illustrations, or do they show section-specific rates consistent with naming specific object types?
**Description:** Extract all ok+/ot+/ol+ body-text words. Compute: (1) section distribution vs what's expected from F112 (ok/ot words = universal content class or section-specific?); (2) compare ok-body words to ok-label words — are they the same vocabulary? (3) Do ok-body words appear with higher frequency in lines near paragraph boundaries (suggesting a naming or reference function)? (4) Do specific ok words co-occur with specific ch-words (suggesting noun-verb pairing)?
**Expected outcome:** ok/ot-body words are partially shared with label vocabulary, appear section-neutrally (universal content), and show mid-line distribution (content words, not line-boundary markers). This would confirm the three-prefix body parallel: qo=B-form, o-label=label-form, o-body=A-or-neutral-form of same semantic class.
**Cost estimate:** medium

---

## H203: d-Onset Words as LINE-BOUNDARY MORPHEME Class — Is There a Unified d-Onset Grammar?
**Priority:** high
**Status:** CONFIRMED (exp_130) — THREE sub-classes: (1) d+ch/sh OPENERS (dshedy=90.9%LF/B, dchor=59.1%LF/A); (2) d-CLOSERS (dan=100%LL, dam=67.9%LL, dy=40.3%LL); (3) medial FUNCTION words (daiin=61.5%MID, dol=80%MID); d+gallows=23 tokens only; d-chain WEAK (max 1.67×) (F137)
**Source:** F112: d-onset sub-class within OTHER is a line-boundary marker system: dal=30% LL, dam=70% LL, dy=46% LL (closers); dain=30% LF, dar=15% LF, dol=16% LF (openers). But this was also found in prior experiments (F097-F101: d+ch/sh = LINE_OPEN tier; daiin = line-closer in A, opener in B). Is the d-onset class unified? Are bare d-words (dal, dain) structurally parallel to prefixed d+ch words (dch- = LINE_OPEN tier)? Or are they different word classes?
**Description:** Systematically analyze all d-onset words: (1) classify as bare_d (no gallows following) vs d+gallows (LINE_OPEN tier); (2) compute LF/LL for each sub-type; (3) compare bare_d-closers (dal/dam/dy) vs bare_d-openers (dain/dar/dol) — are they morphologically distinct? (4) Do d-closers and d-openers complement each other (d-chain: d-closer → d+ch-opener on next line, as in F099)?
**Expected outcome:** Bare d-onset words have a clear two-way split: d-closers (dal/dam/dy/dar final) and d-openers (dain/dol/dor initial). The d-chain (d-closer on line N → d+ch on line N+1) from F099 may extend to bare_d: d-closer on line N → bare d-opener on line N+1 (without requiring the ch-prefix).
**Cost estimate:** small

---

## H204: Suffix-Onset Joint Distribution — Does Each Onset Class Have a Characteristic Suffix Profile That Distinguishes Content from Function Words?
**Priority:** medium
**Source:** F112 identified three sub-classes in OTHER: o-prefix (objects), d-onset (boundaries), particles (aiin/ain/ar/or/al). These should have different suffix distributions. Also from prior work: ch-MID words have -ol/-or/-edy suffixes (dialect-dependent); qo-words have -eedy/-eey. Test: does onset × suffix jointly predict the word's positional and semantic role?
**Description:** For each of the main onset classes (ch, sh, qo, ok/ot, da, s, bare_short), compute the suffix distribution (using the same suffix taxonomy from exp_104). Rank onset-classes by suffix entropy. Lowest entropy = most constrained suffix paradigm. Test: do onset-suffix combinations cluster into (1) high-entropy pairs (content words, many suffixes possible) vs (2) low-entropy pairs (grammatical words, one suffix dominant)?
**Expected outcome:** Grammar words: d+am (suffix: -am, 70% LL, 1 suffix), s+aiin (suffix: -aiin, 1 suffix), bare aiin (no suffix). Content words: ch-MID (multiple suffixes: -ol/-or/-ey/-edy, ~7 productive suffixes). The onset-suffix entropy would quantify the grammar/content distinction.
**Cost estimate:** small

---

## H205: A/B Suffix Paradigm Is Universal — Does Every Onset Class Follow the Same A:-ol/-or vs B:-edy/-eedy Split?
**Priority:** high
**Status:** TESTED (exp_107) — CONFIRMED: All 16 onset classes show same direction. bare_t=12.6× B-ratio (strongest), d+gallows=9.3×, bare_ch=5.7×. d/s-onset in A-dialect: ZERO -edy. Universal grammatical property of dialect.
**Source:** F113: o-prefix words show same A/B suffix split as ch-stems (F047). This suggests the paradigm is not stem-class-specific but a grammatical property of the entire dialect. Test: does EVERY onset class (ch, sh, ok, ot, d, s, qo+gallows, bare_gallows) show the same A/B suffix ratio pattern?
**Description:** For each onset class, compute suffix distribution in dialect A vs B. For each (onset class × dialect), compute the ratio of -edy/-eedy vs -ol/-or usage. If universal: all onset classes should show A preferring -ol/-or and B preferring -edy/-eedy, with similar ratio differences. If stem-class-specific: some onsets will not show the paradigm split.
**Expected outcome:** The paradigm split is UNIVERSAL across all onset classes, with MAGNITUDE varying by onset class (ch-stems show strongest split; bare gallows may show weaker split due to PARA-tier function). d-onset will show suppressed -edy in BOTH dialects (consistent with F113). qo-onset will show B-dominant -eedy (consistent with F043).
**Cost estimate:** small

---

## H206: s-Onset Is a Distinct Grammatical Class — Are saiin/sain True Line-Openers (Parallel to daiin)?
**Priority:** medium
**Status:** TESTED (exp_107) — CONFIRMED: s-onset (11.8%) is LINE-OPENER (LFirst=18.7%, LLast=9.9%). saiin=51%LF, sain=60%LF, sor=66%LF. SUFFIX OPPOSITE of d-onset: s enriches -edy (1.40×), suppresses -aiin (0.73×); d suppresses -edy (0.16×), enriches -aiin (3.08×). Both s/d-openers followed by qo at 2.2-2.5×. s=B-paradigm; d=A-paradigm aligned.
**Source:** F112: s-onset = 6% of OTHER tier; saiin=51%LF, sain=60%LF = line-openers. F105: s-words → sh/ch following (saiin-next-word: ch/sh dominant). saiin and sain are the s-onset parallels of daiin/dain. Are they SYMMETRIC with d-onset openers (d+aiin=24%LF vs s+aiin=51%LF)? Is s-onset an A-dialect or B-dialect feature?
**Description:** Full positional and suffix analysis of s-onset words: LFirst/LLast/PS, suffix distribution, dialect split (A vs B rate), section distribution, what follows them (next-word onset). Compare s-onset to d-onset: are they the same grammatical role in different dialects, or complementary sub-classes?
**Expected outcome:** s-onset is a dialect-specific line-opener: saiin/sain are predominantly B-section (B uses s-opening; A uses d-opening = daiin/dain). Or they may be universal but section-specific. s-onset likely has lower -edy rates than ch-onset but higher than d-onset.
**Cost estimate:** small

---

## H207: Parallel Passages — Are Any Word Sequences of Length ≥4 Repeated Verbatim Across Multiple Folios?
**Priority:** medium
**Source:** F050 found 0.24% of trigrams appear on 2+ folios, with bio section showing 30× more cross-folio repetition than herbal. 4-gram and 5-gram cross-folio repetition has not been tested. Verbatim repeated passages of length ≥4 words would be strong evidence of formulaic construction, copy from a source text, or a substitution cipher with fixed plaintext segments.
**Description:** Extract all 4-grams and 5-grams from body text. Find sequences appearing on 2+ distinct folios. Report: how many 4-grams repeat? What are they? Do they concentrate in specific sections (bio/cosmo, as with bigrams)? Are they grammatically structured (PARA-opener followed by specific sequence)?
**Expected outcome:** 4-gram repetition is very rare (< 0.1% of all 4-grams). Most repetitions will be found in bio/cosmo B sections (most formulaic). Some may represent fixed formulaic phrases like the para-start sequence (p+ch+edy + qo+k+edy + ch+edy...).
**Cost estimate:** small

---

## H208: s/d-Onset Complementary Distribution — Are They Mutually Exclusive Line-Openers on the Same Lines?
**Priority:** high
**Status:** TESTED (exp_108) — CONFIRMED (partial): Co-occurrence ratio=0.97× (near independence). NOT strict complementary. s-opener suppresses d (0.67×). B uses s-openers 1.78× more (cosmo B: 2.98×). pharma A slightly prefers d. Frequency-complementary by dialect/section, not grammatically exclusive.
**Source:** F114: s-onset and d-onset are both LINE-OPENER classes leading to qo at 2.2-2.5×. They have OPPOSITE suffix alignment (s=B-paradigm, d=A-paradigm). Are they in COMPLEMENTARY DISTRIBUTION — i.e., does the same line use EITHER s-onset opener OR d-onset opener, but not both? If so, they may be dialect/register variants of the same grammatical slot.
**Description:** Identify all lines with a line-initial s-onset or d-onset word. Compute: (1) co-occurrence on the SAME LINE — does s-line-initial predict d-absence (and vice versa)? (2) Does dialect determine which is used (A uses d-opener; B uses s-opener)? (3) Is there a section-level preference (cosmo B uses more s-openers; herbal A uses more d-openers)?
**Expected outcome:** s-openers and d-openers are NOT perfectly complementary (they can co-occur on long lines) but are frequency-complementary: lines with s-opener have lower d-content and vice versa. A-dialect predominantly uses d-openers; B-dialect uses both but s-opener at higher rate. This would confirm s and d are variant encodings of the same grammatical role (LINE-OPENER → qo-mid).
**Cost estimate:** small

---

## H209: Parallel Passages (4-gram Repetition) — Are There Verbatim 4-Word Sequences Repeated Across Folios?
**Priority:** medium
**Source:** F050 found 0.24% of trigrams repeat across folios; bio section has 30× more repetition. 4-gram cross-folio repetition untested. Verbatim repeated passages indicate formulaic construction.
**Description:** Extract all 4-grams from body text. Find 4-grams appearing on 2+ distinct folios. Report: how many? Which sections? Are they grammatically structured?
**Expected outcome:** Very few 4-gram repeats (<0.1% of all 4-grams); mostly in bio/cosmo B sections.
**Cost estimate:** small

---

## H210: Suffix Entropy by Onset Class — Do Grammar Words Have Lower Suffix Entropy Than Content Words?
**Priority:** medium
**Status:** TESTED (exp_108) — CONFIRMED: Grammar/content at STEM level (3+ bit gap), NOT onset-class level (0.55 bit range). Grammar particles (cham, otam, dam = -am class): H=0 bits. Content stems (ch, sh, qok): H=2.9-3.4 bits. Two-tier vocabulary confirmed.
**Source:** F114 found that d-onset is -aiin dominant (single suffix, low entropy) while s-onset is more diverse. F112: OTHER tier = particles (aiin/ain) have essentially ZERO suffix (they ARE suffixes). H204 proposed onset × suffix entropy analysis to quantify grammar/content distinction.
**Description:** For each onset class, compute Shannon entropy of suffix distribution. Low entropy = one dominant suffix (grammar word). High entropy = many possible suffixes (content word). Compare: bare_d entropy vs bare_ch entropy vs aiin (particle) entropy. Do the grammatical word classes (d-closers, s-openers) have lower suffix entropy than content words (ch-stems)?
**Expected outcome:** Grammar words: daiin-as-suffix (H=0 bits, one form), dam (H=0, one suffix), dy (H=0). Content words: ch-stem (H≈2-3 bits, 7+ productive suffixes). d-onset has high -aiin concentration but variable tail → medium entropy. This would quantify the grammar/content distinction from suffix entropy.
**Cost estimate:** small

---

## H211: Productivity of the -am Closed Class — Do cham/otam/dam Follow the Same A/B Paradigm as -edy/-ol Stems?
**Priority:** medium
**Status:** CONFIRMED (PARTIAL) — exp_109 (F116): -am class is dialect-neutral overall (A/B=1.00x) but dialect-split within: A-dominant -am (dam=3.1x, cham=3.5x, sam=11.6x) vs B-dominant (qokam=0.3x, ram=0.2x). Onset determines dialect identity; -am suffix is neutral. All -am are line-closers (LL=60-100%). cosmo B suppresses -am (6.83permill vs 22-41permill).
**Source:** F115: The -am closed class (cham, otam, dam, okam, ram, ytam) has H=0 bits (zero suffix variation). F093: -am words are within-para line-closers in PERFECT complementary distribution with oly/oldy (zero co-occurrence). But do -am words themselves follow A/B paradigm? In A, are the dominant -am words different from B?
**Description:** Compute -am word frequency and rates in A vs B: which -am words appear in A? Which in B? Is dam A-dominant? Is otam B-dominant? Are the section distributions of -am words different from oly/oldy? This tests whether the -am closed class is a universal function word (same in A and B) or a dialect-split function word.
**Expected outcome:** The -am class is partially dialect-split: dam (d-onset → A-paradigm aligned) is A-dominant; otam (o+t onset) may be B-neutral or B-dominant. This would show that even the grammar particle layer has dialect-specific variant selection.
**Cost estimate:** trivial

---

## H212: 4-gram Cross-Folio Repetition — Are There Verbatim 4-Word Sequences Shared Across Folios?
**Priority:** medium
**Status:** REFUTED — exp_109 (F116): Only 1 of 16,210 unique 4-grams repeats across 2 folios (0.006%). 5-grams: 0 cross-folio. Voynichese generates compositionally unique sequences per folio. No formulaic 4+ word repetition.
**Source:** H207 (open): F050 found 0.24% of trigrams repeat. 4-grams untested. Verbatim repeated passages indicate formulaic construction.
**Description:** Extract all 4-grams (length-4 word sequences). Count occurrences per folio. Find 4-grams appearing on 2+ distinct folios. Characterize: which sections? Are they grammatically structured (PARA-start + mid-line)?
**Expected outcome:** Very few 4-gram repeats (<20 unique 4-grams on 2+ folios). Most in bio/cosmo B (most formulaic per F050). Any that repeat will likely begin with a PARA-tier word (structural anchor).
**Cost estimate:** small

---

## H213: cth-Cluster Words — Is cth- a Morphological Prefix Parallel to qo- and o-?
**Priority:** medium
**Status:** CONFIRMED — exp_109 (F116): cth- is most A-exclusive onset class (14x A/B ratio), line-closer (LLast=25-26%), A-paradigm suffix dominant (enriches -y=2.16x, -or=2.24x, -ol=1.96x; suppresses -edy=0.33x). Concentrated in herbal/pharma (24-38permill), absent from stars/cosmo (~2permill). NOT a parallel to qo/o prefix systems (only 17-24% stem overlap). cth- = GALLOWS-EXTENDED A-DIALECT CLOSER.
**Source:** F043-F044: cth- is an A-dialect prefix morpheme parallel to qo- (B) and o- (labels). F113: A-exclusive o-prefix words include otchol, otchor (ot+ch+ol, ot+ch+or) — these contain cth-like structure. F115: A_herbal exclusive vocabulary is dominated by cth-cluster words (cthor=34, dchor=20, kchy=19, dchy=19, tchy=14). Is cth- a productive prefix on o/y/e stems (as suggested by F043), and do cth-words follow the A/B paradigm split?
**Description:** Extract all cth-onset words. Compute: (1) A vs B dialect distribution; (2) suffix distribution (A-paradigm or B-paradigm?); (3) stem overlap after stripping cth- — do cth-stripped stems appear as other-onset words? (4) Positional profile (PARA-tier? LINE_OPEN? MID?).
**Expected outcome:** cth- words are overwhelmingly A-dialect (cth- suppressed in B). After stripping cth-, stems are o/y/e initial (parallel to F043). Suffix distribution shows A-paradigm dominance (-ol/-or). Positional role: mid-line or para-level, not line-opening.
**Cost estimate:** small

---

## H214: Extreme B-Pole Onset Classes — Does the Dialect Polarity Axis Have a B-Extreme Counterpart to cth-?
**Priority:** high
**Status:** CONFIRMED UNEXPECTED — exp_110 (F117): B-extreme clusters (shed=78.8x, ched=45.5x, oked=inf) are -edy SUFFIX PRODUCTS, not morphological onset classes. NO B-exclusive onset morpheme parallel to cth- exists. A-extreme=ONSET-encoded (cth-=14x); B-extreme=SUFFIX-encoded (-edy). Dialect polarity axis is ASYMMETRIC. olk-cluster is closest B-structural class (B/A=9.5x, stars/cosmo).
**Source:** F116: The dialect polarity axis is cth- (14× A-extreme) → d-onset (moderate A) → ch/sh/qo (neutral) → s-onset (B-shifted). The B-extreme counterpart to cth- has not been identified. cth- is a gallows-extended A-closer — by analogy the B-extreme might be a gallows-extended B-opener (perhaps fch-/pch-onset, which are PARA-tier words already identified as para-start markers in A). Or perhaps the stars/cosmo-specific forms?
**Description:** Survey onset classes to find the most B-dominant (highest B/A rate ratio). Candidates: (1) fch/pch-onset (F-gallows extended); (2) stars/cosmo B-exclusive onset classes; (3) eee/ee-initial words (triple-vowel forms only in B cosmo). Compute B/A rate ratios for all multi-character onset clusters with n>30 tokens. Identify the B-extreme counterpart to cth-.
**Expected outcome:** Some onset class has B/A ratio ≥5× — likely fch-, pch-, or a stars/cosmo-specific form. If found, it will complete the dialect polarity axis.
**Cost estimate:** small

---

## H215: Paragraph-Internal Line Grammar — Do Lines Within a Paragraph Follow a Predictable Sequential Grammar?
**Priority:** high
**Status:** CONFIRMED (PARTIAL) — exp_110 (F117): Grammar is a STEP FUNCTION, not smooth arc. Lines 1-2 have 5.0%/3.7% PARA tier (3.5x average). From line 3+: PARA near-zero (0.2-1.9%). -am closers appear in last 3-5 lines, absent from first 2. Para-final words: A-paradigm content forms (chol, chor, ain). B-dialect has stronger grammar zone (6.0% at line+1 vs 4.1% A).
**Source:** F114: Line-openers (s/d-onset) → qo mid-line is a confirmed sequence. F108: Para-start words (PARA tier) appear at position 0 of paragraphs. But the grammar of lines 2, 3, 4... within a paragraph is unknown. Is there a predictable line-level sequence?
**Description:** Analyze the sequential grammar of paragraph-internal lines. For each paragraph, extract line-position (1=first, 2=second, ..., N=last). Compute the word-tier distribution at each position. Does line 1 differ from line 2? Does the last line consistently use -am words (line-closers from F093)? Is there a gradual transition from grammar-heavy (PARA-tier) openers to content-heavy lines to grammar-heavy closers?
**Expected outcome:** Para-internal lines follow a arc: strong grammar at first line (PARA-tier), content words dominate middle lines, grammar markers (-am, oly/oldy, dal/dam) concentrate at last line. If confirmed, Voynichese paragraphs have a paragraph-level positional grammar.
**Cost estimate:** medium

---

## H216: Suffix Co-Occurrence Within Single Words — Are Certain Suffix Combinations (e.g., -eedy vs -edy) Mutually Exclusive at the Stem Level?
**Priority:** medium
**Status:** CONFIRMED — exp_111 (F118): Secondary B-paradigm split: ch/sh prefer -edy (68-69%, Simple-B); qok/ok use all three B-suffixes equally (Complex-B, H=1.57-1.58 bits). Stars B systematically shifts to -eey (qok: 43% eey); cosmo B prefers -eedy. A-dialect has no secondary suffix split. The secondary B-split is a genuine stem-level morphological distinction within B-paradigm.
**Source:** F114: B-type suffixes (-edy/-eedy/-eey) are the paradigm markers. F115: The 3+ bit entropy gap separates grammar from content. But within content stems (ch, sh, qok), do all stems freely use both -edy and -eedy, or do some stems preferentially select one over the other?
**Description:** For the top 20 content stems (ch, sh, qok, ok, ot, etc.), compute the distribution of -edy vs -eedy vs -eey. Does ch prefer -edy while qok prefers -eedy? Is there a stem-level suffix specialization beyond the general A/B paradigm? Also test within dialects (B-dialect stem × suffix matrix).
**Expected outcome:** Some stems preferentially select -eedy over -edy (or vice versa). This would indicate a STEM-LEVEL morphological distinction within the B-paradigm suffix class — a secondary paradigm within the B-paradigm.
**Cost estimate:** small

---

## H217: Folio-Level Language Model — Can Each Folio's Vocabulary Distribution Predict Its Section?
**Priority:** medium
**Source:** F103: Section classifier achieves 96.6% accuracy (A) using all words. F109-F110: ch-stem vocabulary alone achieves 73% of full-vocabulary classification performance. F116: Each folio has essentially unique 4-gram sequences. These results imply folio-level vocabulary is strongly section-predictive.
**Description:** Build a per-folio unigram language model (word frequency vector). Use cosine similarity or KL-divergence between folio vectors to compute folio-to-folio distances. Cluster folios by vocabulary similarity. Do folios cluster by section? By dialect? Are there any folios that cluster with the wrong section (potential mis-classification candidates or transition folios)?
**Expected outcome:** Folios cluster strongly by section (A herbal, A pharma, B cosmo, B stars, B herbal separate clusters). Transition folios (e.g., f1r at herbal/astro boundary, f85 at herbal/cosmo boundary) may appear between clusters.
**Cost estimate:** medium

---

## H218: olk-Cluster Characterization — Is olk- the B-Structural Counterpart to cth-?
**Priority:** high
**Status:** CONFIRMED REVISED — exp_111 (F118): olk- is B-dominant (9.5x B/A), section-complement to cth- (olk-=cosmo/stars; cth-=herbal/pharma), suffix-complement (olk-=eedy/eey; cth-=or/ol/y). BUT olk- is MID-LINE content (LLast=11.7%), NOT a closer like cth- (LLast=20.2%). No B-exclusive onset-based closer morpheme exists. olk-= B-paradigm mid-line content class.
**Source:** F117: The olk- cluster (olkedy, olkaiin, olkam, olka) has B/A=9.5× — the strongest B-dominant structural class that is NOT a suffix artifact. It's concentrated in stars/cosmo. Is olk- a morphological prefix parallel to cth- (A-closer) but for the B-dialect?
**Description:** Extract all olk-onset words (starting with 'olk'). Compute: (1) A/B dialect distribution and section distribution; (2) positional profile (LFirst%, LLast%, PS%); (3) suffix distribution (A vs B paradigm); (4) stem overlap with qo-, ch-, sh-stems after stripping olk-; (5) Compare olk-/olka-/olke-/olkee- sub-classes. Is olk- a single morphological class or heterogeneous?
**Expected outcome:** olk- is B-dominant (9-10× B/A), stars/cosmo concentrated, with B-paradigm suffix dominance. Positional role: mid-line or line-closing. If confirmed, olk- is the B-paradigm closer counterpart to cth-.
**Cost estimate:** small

---

## H219: Suffix Paradigm Diachrony — Did the -edy Suffix Evolve From an Earlier Stem+Onset Combination?
**Priority:** medium
**Status:** CONFIRMED — exp_111 (F118): A-paradigm suffixes (-ol/-or/-aiin/-ar/-al) have abundant standalone free-word forms (100-500+ tokens); B-paradigm suffixes (-edy/-eedy/-eey) are near-zero standalone (2-8 tokens). standalone dy = A-dialect closer (LLast=42.9%, A-dominant). y standalone = 0. A=grammaticalized free morphemes; B=novel non-free suffix innovation.
**Source:** F117: B-dialect encodes identity through -edy suffix; A-dialect through onset morphemes (cth-). The asymmetry suggests B added -edy to existing onset classes. Could -edy represent an earlier word that grammaticalized into a suffix? If -edy is a grammaticalized free morpheme, there should be: (1) a free word 'edy' or 'dy' with similar distribution; (2) 'dy' as a standalone word that mirrors -edy semantics.
**Description:** Check if 'edy', 'eedy', 'dy', 'y' exist as standalone free words. Compute their section/dialect distribution and positional profiles. Compare standalone 'dy' with -dy suffix distribution. Does standalone 'dy' appear in similar sections and positions as -dy suffix words?
**Expected outcome:** 'dy' and 'y' exist as standalone words (~100-200 tokens). Their distribution mirrors -dy/-y suffix words in section and dialect. This would support that Voynichese suffixes are grammaticalized free morphemes (consistent with an agglutinative or analytic language).
**Cost estimate:** trivial

---

## H220: Secondary B-Suffix in Stars vs Cosmo — Is -eey a Stars-Specific B-Paradigm Marker and -eedy a Cosmo-Specific Marker?
**Priority:** high
**Status:** CONFIRMED (PARTIAL) — exp_112 (F119): Stars-B universally elevates -eey (highest rate across ALL onset classes; stars>cosmo>herbal). Cosmo-B elevates -eedy for qo-prefix stems (qok=35%, qot=41%) but NOT ch/sh. -edy remains dominant for ch/sh everywhere. GRADIENT not categorical switch. Stars exclusive: triple-vowel forms (oteeey=7, cheeey=6). Same vocabulary, different proportions.
**Source:** F118: Stars B shifts to -eey (qok: 43% eey vs 11% herbal); cosmo B prefers -eedy (qok: 35% eedy). H216 confirmed section-level B-suffix variation. Is there a systematic three-way B-suffix grammar: herbal-B=-edy; cosmo-B=-eedy; stars-B=-eey?
**Description:** For EACH B-dialect section (herbal B, cosmo B, stars B), compute the rate of -edy, -eedy, -eey separately for each major onset class (ch, sh, qok, ok, ot, qo). Test whether the three-way B-suffix partition is systematic (all onset classes show same direction in each section). Also: compute cross-section word overlap for -eedy vs -eey words — do sections share the same stems with different suffixes, or different stems?
**Expected outcome:** Systematic three-way partition: herbal-B→-edy, cosmo-B→-eedy, stars-B→-eey. Word-level evidence: qok+eey is stars-specific; qok+eedy is cosmo-specific; qok+edy is herbal-specific. This would make the secondary B-suffix a SECTION MARKER within B-dialect (third layer of linguistic structure below dialect, above individual word).
**Cost estimate:** small

---

## H221: Folio-Level Vocabulary Distance Clustering — Do Folios Cluster by Section? Are There Transition Folios?
**Priority:** medium
**Status:** CONFIRMED (exp_131) — 25/94 folios (27%) best-match ≠ assigned section. Herbal=LEAST cohesive (mean=0.914); cosmo=MOST (0.965). B-herbal bifolio insertions (f26/f31/f40/f48/f50) systematically mismatch; f40 most extreme (best=stars/0.860 vs self=0.755). f103 (first stars folio) best-matches cosmo. Many A-herbal folios best-match pharma (herbal-pharma onset continuum). Stars/cosmo most homogeneous; astro/herbal most heterogeneous. (F138)
**Source:** F117: H217 (folio clustering) proposes using cosine similarity on folio word-frequency vectors. F112: 72-79% of each section's vocabulary is section-specific. F116: Each folio has essentially unique 4-gram sequences.
**Description:** Build per-folio word frequency vectors (normalized). Compute pairwise cosine similarity between folio vectors. Cluster by similarity. Identify: (1) clusters that correspond to sections; (2) outlier folios; (3) transition folios between sections.
**Expected outcome:** Folios cluster into 5-6 clear groups corresponding to sections. Transition folios (f57, f85, f86, f103) may appear between clusters. Some star-section folios may cluster with herbal B if vocabulary overlaps.
**Cost estimate:** medium

---

## H222: Triple-Vowel Extended Forms — Are oteeey/cheeey/lkeeey Stars-Exclusive Suffix Paradigm Extensions?
**Priority:** high
**Status:** CONFIRMED — exp_113 (F120): Stars-B dominant (17.25permill vs cosmo 4.40permill). Vowel-length gradient monotonic stars-concentrated (edy→eedy→eeedy: stars=36%→48%→63%; eeey: stars=59%). eee words avoid ch/sh (0.37-0.46x), concentrate on ok/ol/qo (1.7-1.9x). Stars-only forms: oteeey(7), lkeeey(7), teeedy(4).
**Source:** F119: Stars B has exclusive triple-vowel forms (oteeey=7, cheeey=6, lkeeey=7, teeedy=4) not found in cosmo or herbal. These appear to be ot/ch/lk/t + eee + y/dy (triple-e vowel extension). Is this a systematic stars-specific sub-suffix paradigm?
**Description:** Extract all words with 3+ consecutive 'e' characters (eee) from body text. Compute: (1) section distribution; (2) onset class distribution; (3) whether eee forms are stars-exclusive or appear rarely elsewhere; (4) relationship to double-e forms (eey/eedy) — is eee a further extension of the ee pattern?
**Expected outcome:** eee forms are stars-dominant (80%+). The eee pattern extends the ee pattern: edy→eedy→eeedy; eey→eeey as a vowel-length gradient. Stars uses longer vowel strings than cosmo or herbal.
**Cost estimate:** trivial

---

## H223: A-Dialect Suffix Paradigm Completeness — Does A Have Any Suffix Variation by Section Analogous to B's Three-Tier System?
**Priority:** medium
**Status:** CONFIRMED (PARTIAL) — exp_113 (F120): A has mild section variation: herbal-A=-y dominant (ch=29%, qok=37%); pharma-A=-ol dominant (ch=28%, qok=41%). Consistent across all onset classes. Avg diff=8.9% (vs B 31%). Pharma-A elevates -dy/-ey. The A-section variation is 3.5x weaker than B 3-tier system.
**Source:** F118-F119: B-dialect has a 3-tier suffix system. A-dialect was assumed to be uniform (no secondary split). Is this actually true? Do A herbal/pharma/astro sections use different proportions of -ol/-or/-y/-aiin?
**Description:** Compute A-paradigm suffix (-ol/-or/-y/-aiin) rates by section for A-dialect onset classes (ch, sh, qok in A-dialect). Is pharma-A different from herbal-A in suffix use? Does astro-A have distinctive suffix choices? Test whether A has any section-level suffix variation comparable to B's section gradient.
**Expected outcome:** A has minimal or no section-level suffix variation (uniform paradigm). OR: A-pharma uses more -or/-aiin than herbal-A (which might use more -ol/-y). If variation is found, it would be a secondary A-paradigm structure parallel to B's secondary structure.
**Cost estimate:** small

---

## H224: Word-Level Entropy as Naturalness Test — Do the Four Levels of Suffix Hierarchy Predict Information Content Per Word?
**Priority:** high
**Status:** CONFIRMED (exp_114)
**Source:** F120: The four-level suffix hierarchy (dialect→stem class→section→vowel length) encodes layered information. If the hierarchy is genuine, then knowing the onset class + section should REDUCE the uncertainty about which suffix a word takes (lower conditional entropy). This is a formal test of whether the hierarchy is meaningful.
**Description:** Compute conditional entropy H(suffix | onset_class, section, dialect) and compare to marginal entropy H(suffix). How many bits of uncertainty are resolved by knowing onset class + section? Compare: A-dialect words in herbal vs pharma; B-dialect words by section and onset class. A genuine hierarchy reduces conditional entropy.
**Expected outcome:** H(suffix | onset_class, section, dialect) < H(suffix) by 0.5-1.0 bits. The hierarchy resolves substantial suffix uncertainty. This would formalize that the four-level structure is a genuine morphological system encoding about 0.5-1.0 bits of information per word.
**Cost estimate:** small

---

## H225: Folio-Level Vocabulary Distance Clustering
**Priority:** medium
**Status:** CONFIRMED PARTIAL (exp_115)
**Source:** F112: 72-79% of vocabulary is section-specific. H217 (unresolved). Now we have the four-level suffix model — do folios cluster by section AND by their suffix pattern tier?
**Description:** Build per-folio word frequency vectors. Compute cosine similarity between folio vectors. Cluster. Look for: (1) section clusters; (2) transition folios; (3) whether suffix pattern (stars-eey vs cosmo-eedy) aligns with folio clustering independent of section labels.
**Expected outcome:** Folios cluster into 5-6 section groups. Stars folios cluster tightly (highest eey rate, distinctive eee forms). Cosmo folios may be more spread (some folio-level variation in B-suffix preference from F119).
**Cost estimate:** medium

---

## H226: Herbal A/B Interleave Periodicity
**Status:** CONFIRMED (exp_116) — Is the Alternating Pattern Regular Enough to Imply Page-Pair or Quire-Based Assembly?
**Priority:** high
**Source:** F122: Herbal section has B-dialect folios alternating with A-dialect every 3-5 folios (f26/31/33-34/39-41/43/46/48/50/57). This appears regular. If the pattern has a period of ~4-5 folios, it may correspond to quire structure (quires are typically 4-8 folio gatherings). A strict periodicity test could support a "two-scribes interleaved during binding" theory vs. random variation.
**Description:** Map the dialect assignment (A or B) of each herbal folio and test for periodicity. Compute autocorrelation of the binary A/B sequence. Check whether B-folios cluster near quire boundaries (known quire structure: Q1=f1-8, Q2=f9-16, Q3=f17-24, Q4=f25-32, Q5=f33-40, Q6=f41-48, Q7=f49-57 approx). Does each quire tend to have a B-folio near its start or end?
**Expected outcome:** IF quire-aligned: each quire's last 1-2 folios are B-dialect, suggesting a systematic insertion pattern. IF random: the B-folios appear randomly within quires with no boundary preference.
**Cost estimate:** small

---

## H227: Line-Position Effect on Suffix Distribution
**Status:** CONFIRMED (exp_116) — Do First/Last Words Use Different Suffixes Than Mid-Line?
**Priority:** high
**Source:** F117: Para-internal grammar step function (PARA class concentrated at first 2 lines). F118: Free-morpheme asymmetry (A-paradigm suffixes are free words; ol/or/aiin appear as standalone words). The line-position effect on word TIER is known, but line-position effect on SUFFIX CHOICE within the same onset class is unexplored.
**Description:** For each onset class, compute suffix distribution conditioned on line-position: (1) line-first word, (2) line-last word, (3) mid-line word. Do A-dialect folios show ol/or enrichment at line-last position (consistent with standalone usage)? Do B-dialect folios show edy enrichment at specific positions? Compare to the positional entropy profile (F003).
**Expected outcome:** Line-last words enrich -ol/-or/-aiin (standalone-like suffixes); line-first words enrich -edy/-eedy (topic/theme markers?). This would add a fifth level to the suffix hierarchy: Dialect → Onset → Section → Vowel length → Line position.
**Cost estimate:** small

---

## H228: The "Other" 20.8%
**Status:** CONFIRMED (exp_117) — What Are Words With No Identified Suffix?
**Priority:** medium
**Source:** F121: 20.8% of tokens (6,878/33,066) fall into the 'other' suffix category (no recognized suffix pattern). This is the largest single "suffix class." Understanding what these words are could reveal an unmodeled morphological category.
**Description:** Extract all words falling into the 'other' category. Characterize: (1) length distribution vs. suffixed words; (2) onset class distribution; (3) section/dialect distribution; (4) frequency distribution (hapax vs. repeated); (5) whether they cluster into groups (e.g., short uninflected forms, long compound-like forms). Sample the top 50 'other' words and inspect manually.
**Expected outcome:** 'Other' consists of: (a) short function words (2-3 chars) with no suffix structure; (b) long compound-like forms with multiple suffix-like endings; (c) possible transcription errors or illegible words. Identifying the 'other' composition would tighten the entropy estimate.
**Cost estimate:** small

---

## H229: Paragraph-Internal Vocabulary Repetition
**Status:** CONFIRMED (exp_117) — Do Words Repeat Within Paragraphs More Than Across Paragraphs?
**Priority:** medium
**Source:** F112 (section vocabulary specificity). F117 (para grammar step function). Within a paragraph, is there word-level cohesion (same stems repeated with different suffixes)? This would be analogous to discourse coherence in natural language (pronoun/anaphora patterns).
**Description:** For each paragraph, compute: (1) within-para word repetition rate (how many unique words / total words); (2) cross-para word sharing rate for adjacent paragraphs vs. non-adjacent paragraphs; (3) whether the same ONSET (stem prefix) appears multiple times within a paragraph with different suffixes. Compare within-para repetition to within-section and cross-section repetition rates.
**Expected outcome:** IF natural language: within-para words should repeat more than cross-para (topic coherence). IF cipher or generated text: repetition is uniform across distances. Finding within-para cohesion would be strong evidence for discourse-level structure.
**Cost estimate:** medium

---

## H230: Extended Suffix List
**Status:** CONFIRMED REVISED (exp_118) With -am and -air — Does Adding These Suffixes Change the Hierarchy?
**Priority:** high
**Source:** F124: 'other' category contains -am words (dam=70, otam=34, qokam=24; ~570 tokens) and -air words (dair=75, qokair=15; ~450 tokens). These are legitimate suffix patterns. If -am and -air are bona fide A-paradigm suffixes (A-markers like -ol/-or), adding them to the analysis would change the conditional entropy estimates and the A-dialect section variation picture.
**Description:** Re-run the suffix analysis with -am and -air added to the suffix list. Test: (1) Are -am and -air A-dialect or B-dialect suffixes? (2) Do they show section-level variation like -ol/-or? (3) What onset classes prefer -am vs -air? (4) How does adding them change H(suffix) and conditional entropy levels? Compare to H224 baseline.
**Expected outcome:** -am and -air are A-paradigm suffixes (like -ol/-or/-y). They may show section-level preferences (e.g., -am=pharma-dominant or -air=astro-dominant). Adding them lowers 'other' from 20.6% to ~17% and raises H(suffix) slightly.
**Cost estimate:** small

---

## H231: daiin as a Syntactic Function Word
**Status:** CONFIRMED (exp_118) — Positional Profile, Bi-gram Context, and Semantic Slot
**Priority:** high
**Source:** F124: daiin appears 3+ times in 41% of all paragraphs (most ubiquitous repeated word). F117: d-onset words are line-openers. daiin = d-onset + -aiin suffix. F119: -aiin is an A-paradigm suffix.
**Description:** Characterize daiin as a syntactic unit: (1) Positional profile: is daiin a line-first word (like d-onset class)? (2) Bigram context: what words come before and after daiin? (3) Para-position: does daiin appear more at para-start or para-end? (4) Section distribution: is daiin evenly distributed or section-concentrated? (5) Co-occurrence: which words most often appear IN THE SAME LINE as daiin? This is a direct probe of daiin's syntactic role.
**Expected outcome:** daiin is a line-opening determiner or grammatical particle that precedes content words (ch/sh/qok-onset words). It may parallel the definite article in romance languages that preceded content nouns.
**Cost estimate:** small

---

## H232: Stars Section Catalog Structure — Do Stars Paragraphs Have a Repeating Template?
**Priority:** medium
**Status:** CONFIRMED (exp_131) — Stars has a line-ELEMENT template: [p/s/y/d/t OPENER (5-7× enriched at first position)][sh-word 2nd (2.25×)][B-content middle][r-closer (2.55×) or -am LAST (8.06×)]. The -am line-ending signal (8.06×) is the STRONGEST positional suffix enrichment in the manuscript. Line-openers dominated by 5 onset classes (p/s/y/d/t). Each folio has characteristic dominant opener (f112=s, f107/f113=p, f104/f106/f114=y, most others=d). Stars lines=8.7-10.9 words/line mean. No whole-line repeating template (consistent with H239/F128) but strong element-level positional grammar. (F138)
**Source:** F122: Stars paragraphs have within-para repetition rate 0.476 (nearly double other sections). The stars section contains star catalog entries. If each paragraph follows a template "star-name + descriptor + position", the same vocabulary template should recur with variable stem slots filled differently.
**Description:** Examine stars paragraphs at the level of paragraph-internal word sequences. Do all stars paragraphs follow a template like "X daiin Y ol Z"? Compute per-paragraph suffix sequence profiles. Look for repeated n-gram patterns within the stars section that suggest a catalog template.
**Expected outcome:** Stars paragraphs follow a repeating suffix template (e.g., most lines end in -ol or -or; most lines start with -eey or -eedy words). The template is consistent across the 25 stars paragraphs.
**Cost estimate:** medium

---

## H233: Other Pre-Nominal Determiners
**Status:** CONFIRMED (exp_119) — Do Other High-Frequency A-Paradigm Words Show Similar Directional Bigram Enrichment Toward cth- or ch-/sh-Nouns?
**Priority:** high
**Source:** F125: daiin→cth-onset enriched 4.89×. This is the strongest bigram found. If daiin is a determiner class, there may be other determiners (possibly dain, dy, ol, or similar) that also show directional enrichment before nominal onset classes.
**Description:** For each of the top 20 high-frequency words (daiin, ol, chedy, shedy, or, aiin, dy, dar, etc.): compute what onset class appears AFTER them (next-word onset) vs the baseline. Identify words with strong directional enrichment (>2×) toward specific onset classes. Build a bigram enrichment matrix: word → next_onset → enrichment_ratio. This would map out the functional word → content word syntactic patterns.
**Expected outcome:** A cluster of "determiner-like" words that precede cth- or ch-/sh-onset content words. Possible contrast: words that precede qok-onset vs words that precede ch-onset may be different functional categories.
**Cost estimate:** small

---

## H234: D-Onset as a Function-Word Class
**Status:** CONFIRMED (exp_119) — Are d-Onset Words Structurally Distinct From All Other Onset Classes?
**Priority:** high
**Source:** F125: d-onset words show extreme structural diversity: dshedy=93.1% line-first (topic marker), dam=68.6% line-last (closer), dy=43.1% line-last (closer), daiin=20.2% first/17.5% last (balanced determiner), dain=26.2% first. F116: d-onset is "moderate A-paradigm." This diversity suggests d-onset encodes function words (grammatical vocabulary) rather than content vocabulary.
**Description:** Compare the structural diversity of d-onset words vs all other onset classes: (1) positional entropy (do d-onset words span a wider range of positional roles?); (2) frequency distribution (do d-onset words have a flatter rank-frequency distribution?); (3) suffix entropy (do d-onset words have more diverse suffix distributions?); (4) collocational diversity (do different d-onset words follow different onset classes?). Compare to ch-onset (likely content words) and qok-onset (complex content).
**Expected outcome:** d-onset has the highest positional entropy and widest range of positional functions — consistent with function word class. ch-onset should be more content-word-like (lower positional variation, higher collocational consistency).
**Cost estimate:** small

---

## H235: Stars Section Catalog Structure — Repeating Template in Stars Paragraphs
**Priority:** medium
**Source:** F122: Stars paragraphs have within-para repetition rate 0.476 (highest). F119: stars B has highest -eey rate and distinctive triple-vowel forms. H232.
**Description:** Examine the 25 stars paragraphs. For each paragraph: (1) compute per-line suffix sequence (what suffix does each word take?); (2) look for a repeating structural template across lines within a paragraph; (3) compare template consistency across different stars paragraphs. Do all stars paragraphs follow a similar "X suffix_seq Y suffix_seq Z" pattern?
**Expected outcome:** Stars paragraphs show a star-entry template: each "entry" (1-2 lines) has a consistent suffix ordering — possibly "eey/eedy word + -ol/-or phrase + daiin cth-word". The template reuses the same suffix pattern across entries.
**Cost estimate:** medium

---

## H236: Dialect-Specific Bigram Rules
**Status:** CONFIRMED REVISED (exp_120) — Are [A-Suffix→cth] and [B-Suffix→qok] Patterns Dialect-Pure?
**Priority:** high
**Source:** F126: Pre-cth cluster = A-suffix words (chor, daiin, chol, shol); Pre-qok cluster = B-suffix words (shedy, chedy). But we tested on mixed-dialect body text. The pre-cth pattern should be STRONGER in A-dialect sections (herbal, pharma) and the pre-qok pattern STRONGER in B-dialect sections (cosmo, stars).
**Description:** Re-run bigram analysis separately for A-dialect folios and B-dialect folios. Test: (1) Does the chor→cth enrichment increase when restricted to A-dialect text? (2) Does shedy→qok enrichment increase in B-dialect text? (3) Are there DIFFERENT pre-nominal clusters in A vs B (i.e., A-dialect has daiin→cth but B-dialect has a different word preceding qok-nouns)? Also test: does the [A-suffix→cth] rule hold at the WORD level or at the FOLIO level?
**Expected outcome:** The cth-preceding pattern is 5-7× in A-dialect-only text (stronger than the 4.7× seen in mixed text). The qok-preceding pattern is 4-5× in B-dialect text. The patterns are dialect-pure and represent genuinely different clause structures in A vs B dialects.
**Cost estimate:** small

---

## H237: otaiin as Demonstrative
**Status:** CONFIRMED PARTIAL (exp_120)/Determiner for ot-Class Words — Parallel to daiin→cth
**Priority:** medium
**Source:** F126: otaiin→ot = 4.27× (third-strongest word→onset enrichment after chor→cth=4.73× and daiin→cth=4.38×). If daiin is a pre-nominal determiner for cth-nouns, otaiin may be a parallel determiner for ot-onset nouns. otaiin = ot + -aiin (parallel structure to daiin = d + -aiin).
**Description:** Characterize otaiin: (1) positional profile vs other ot-onset words; (2) section/dialect distribution; (3) bigram context: what comes after otaiin vs after other ot-onset words? (4) Is there a parallel pattern: [other-onset]-aiin words → [same-onset] words? Test okaiin→ok, qokaiin→qok, chaiin→ch enrichments.
**Expected outcome:** otaiin shows strong ot-onset enrichment in next-word (4.27× confirmed). A general pattern: [onset-aiin] → [onset-onset] suggests -aiin is a "cross-referential" suffix — marking the determiner of a subsequent noun from the same onset class.
**Cost estimate:** small

---

## H238: Trigram Phrase Structure — Do [A-suffix-word] [cth-word] pairs form consistent 3-grams with preceding words?
**Priority:** high
**Status:** CONFIRMED PARTIAL (exp_121) — W1 before [daiin][cth] is ch-onset (1.94×), -ol suffix (2.48×). Top W1: chol, shol, chor. d-onset depleted before daiin (0.60×). W0 shows no pattern — template is exactly 3 words [ch-word][daiin][cth-noun]. (F128)
**Source:** F127: A-dialect rule daiin→cth is strong. If daiin + cth-word forms a "determiner + noun" phrase, the word BEFORE daiin should be consistently different (e.g., a verb or adjective). Testing the trigram [X] [daiin] [cth-word] would reveal whether there's a consistent phrase-initial word class.
**Description:** Extract all trigrams [W1] [W2] [W3] where W2=daiin and get_onset(W3)=cth. What is the onset/suffix class distribution of W1? Compare to [W1] [daiin] [non-cth W3] — is W1 different depending on whether daiin is followed by cth or not? Also test trigrams [W1] [chol] [cth-word] and [W1] [shol] [cth-word].
**Expected outcome:** W1 (before daiin-before-cth) has a consistent onset profile — likely s-onset (topic opener) or d-onset. This would reveal a 3-word phrase template: [s-word/opener] [daiin] [cth-noun] = "topic determiner noun" in A-dialect.
**Cost estimate:** small

---

## H239: Stars Paragraph Template — Do Stars Entries Follow a Canonical Suffix Sequence?
**Priority:** medium
**Status:** CONFIRMED PARTIAL (exp_121) — All stars folios B-dialect. No repeating whole-line template (all 580 sequences unique). Positional structure: pos-0 constrained (H=-0.532: other/d/s), 2nd-half ot-enriched (1.75×), s-onset depleted in 2nd half (0.28×). Template: [d/s-opener][B-content][ot-nominal phrase][other-closer]. otaiin→ot=3.99× in stars. (F128)
**Source:** F122: Stars has highest within-para repetition (0.476). Stars likely contains catalog entries for individual stars. H232: stars paragraphs may follow a template. H235: untested.
**Description:** Extract all 25 stars paragraphs. For each paragraph, compute the suffix sequence of each line (what suffix does each word take, in order). Identify: (1) does each line follow a suffix template? (2) is there a consistent first-line vs non-first-line pattern? (3) do all paragraphs share a common suffix n-gram?
**Expected outcome:** Stars lines follow a template like "-eey/-eedy word + -ol/-or + daiin + cth-word", repeated for each star entry. The template is visible as a consistent suffix sequence.
**Cost estimate:** small

---

## H240: chol vs chor — Are -ol and -or Suffix Variants Context-Distinguishable?
**Priority:** high
**Status:** CONFIRMED (exp_122) — -ol=pre-determiner (d-onset 1.44-1.66×); -or=pre-nominal (cth 2.15×, sh 1.57×); chol→d=1.66× vs chor→d=0.75×; shor→sh=2.84×; full suffix matrix: aiin=2.24× cth, ey/dy/eey=pre-qok (1.57-2.48×), al=pre-d-particle (F129)
**Source:** F128: chol (31 pre-daiin occurrences) is 3.4× more common than chor (9) as pre-daiin word, but exp_119 showed chor→cth=4.73× (the strongest bigram in the mixed corpus). exp_120 revealed chor→cth=1.77× in A-dialect only while chol→cth was moderate. So chol and chor have different bigram profiles despite sharing the ch- onset. Are -ol and -or selecting for different subsequent word classes?
**Description:** Compute full bigram enrichment matrix for chol vs chor separately: what onset classes follow each? Test: chol→X vs chor→X for all onset classes X. Also test shol vs shor. Is -ol a "pre-determiner" suffix (precedes daiin/determiners) while -or is a "pre-noun" suffix (precedes cth directly)? Test positional distribution: chol vs chor at line-first/mid/last. Test section distribution.
**Expected outcome:** chol→daiin enriched; chor→cth enriched directly (without daiin). The -ol and -or suffix variants encode different syntactic positions within the A-paradigm NP — chol = A-paradigm adjective-like modifier; chor = A-paradigm that directly precedes the head noun.
**Cost estimate:** small

---

## H241: B-Dialect NP Template — What Precedes qok-Onset Words in B?
**Priority:** high
**Status:** CONFIRMED (exp_122) — B-NP template: [ot/ok-modifier][otaiin][ot-noun]; post-otaiin ot=4.08×; pre-otaiin ot=2.47×; A-daiin→cth=2.77× MIRRORS B-otaiin→ot=4.00×; perfect dialectal NP complementarity; pre-otaiin top word = okaiin (4×); [qok-word][shedy][qok-word]=1.79× (F129)
**Source:** F128: A-dialect has [chol/shol][daiin][cth-noun] as NP template. B-dialect has shedy/qokeedy→qok bigrams (F126/F127). Is there a parallel B-dialect NP template [W1][otaiin][ot-noun] or [W1][shedy][qok-word]? F128: otaiin→ot=3.99× in stars (B-dialect). Does otaiin serve as B's determiner in the same way daiin serves A's?
**Description:** In B-dialect text, extract: (1) trigrams [W1][shedy][qok-word] — what is W1 onset? (2) trigrams [W1][otaiin][ot-word] — what is W1 onset? (3) trigrams [W1][qokaiin][ch-word] (since qokaiin→ch=1.84×). Compare B-dialect NP structure to A-dialect [chol][daiin][cthy]. Also test: what precedes otaiin in stars? Is there a B-dialect formula [X][otaiin][otal/otedy]?
**Expected outcome:** B-dialect has a parallel NP template using otaiin as determiner: [B-onset-word][otaiin][ot-noun], analogous to A-dialect [ch-word][daiin][cth-noun]. This would confirm a symmetric NP grammar across dialects with different determiners (daiin vs otaiin) and different noun classes (cth vs ot).
**Cost estimate:** small

---

## H242: The "other" Onset Class in Stars — What Words Constitute It?
**Priority:** medium
**Status:** CONFIRMED (exp_123) — Stars "other" = (1) standalone particles aiin/ar/al/or/am (33%); (2) l-onset (lchedy/lkaiin/lkeedy=81% stars); (3) k-onset (kaiin/keedy/keey); (4) y-/p-prefixed line-starters; line-end "other" = am particles; lkaiin=81% stars-concentrated (F130)
**Source:** F128: In stars, pos-0 onset distribution is 48% "other" (vs ~27% overall baseline). Stars lines predominantly start with "other"-onset words. F117: 'other' top words are free morphemes (ol, aiin, or, ar, al). But in stars (B-dialect), the "other" words at line-start are likely different from A-dialect free morphemes. What specific words constitute the "other" class at stars line-starts?
**Description:** Extract all stars lines. Identify the specific words at pos-0 that classify as "other" onset. Build a frequency table. Compare to: (1) overall "other" class composition, (2) B-dialect "other" words more generally, (3) check if these are standalone particles (ol, ar, al), compound words, or genuinely unclassified new word types. Also: what "other"-onset words appear at stars line-final positions (where "other" also dominates)?
**Expected outcome:** Stars line-start "other" words are a specific set of B-dialect particles or formula words that function as paragraph/entry openers (like "Item", "The star", etc. in natural language catalogs). Stars line-final "other" words may be a different set (closing particles, possibly -am words).
**Cost estimate:** small

---

## H243: chol→daiin Bigram — Is -ol Suffix Specifically a "Pre-Determiner" Marker?
**Priority:** medium
**Status:** CONFIRMED (exp_122 / F129) — -ol=pre-determiner (d-onset 1.44-1.66×); -or=pre-nominal (cth 2.15×); full suffix matrix completed; see H240.
**Source:** F128: W1 in [W1][daiin][cth-noun] has -ol suffix at 2.48× enrichment. chol is the top W1 word (31 of 401 pre-daiin occurrences = 7.7%). Is this a general property of -ol suffix words? Test: all -ol suffix words: what onset follows each of them? Is -ol suffix systematically followed by daiin (or other d-onset determiners) more than other suffixes?
**Description:** Compute for each suffix (-ol, -or, -y, -ey, -aiin, -edy, -al, -ar) the bigram enrichment to next-onset class. Specifically test: [X-ol]→d-onset vs [X-or]→d-onset in A-dialect. Also test [X-ol]→cth vs [X-or]→cth. Build a full suffix→next-onset enrichment table analogous to the word-level bigram matrix.
**Expected outcome:** -ol suffix words are pre-determiner (enrich d-onset next); -or suffix words are pre-nominal (enrich cth-onset next directly). This would establish that suffix choice within A-paradigm encodes syntactic position, not just morphological slot — the -ol/-or distinction maps to adjective/modifier vs pre-nominal determiner positions.
**Cost estimate:** small

---

## H244: Onset-Class Transition Matrix — Is There a Full Markov Grammar?
**Priority:** high
**Status:** CONFIRMED PARTIAL (exp_123) — Grammar is probabilistic (no forbidden pairs); only mandatory: cth→cth=4.78×; dominant cycle: cth↔d (2.18-2.21×); sh→qok=1.99×; ot→ot=1.95×; s-onset most constrained (H=-0.169 bits); B-cth→cth=8.79× (F130)
**Source:** F129: -ol/-or encode syntactic position via next-onset enrichment. Multiple experiments have shown onset-class bigram enrichment rules. The accumulated evidence suggests a full Markov grammar over onset classes. What does the complete onset→onset transition matrix look like? Are there forbidden transitions (near-zero)? Is there a cyclic grammar: s→d→ch→cth→d→... ?
**Description:** Build the full N×N onset-class transition matrix (conditional probability of next onset given current onset) over the full corpus. Compute enrichment (obs/baseline) for every onset→onset pair. Identify: (1) forbidden pairs (enrichment <0.2); (2) mandatory pairs (enrichment >3×); (3) whether the matrix reveals a directed cycle (a grammar graph). Test A-dialect and B-dialect separately. Compare entropies: which onset class has lowest H(next) = most grammatically constrained?
**Expected outcome:** A-dialect reveals a grammar graph: some transitions are enriched (ch/sh→d→cth, s→ch, etc.) and others forbidden (cth→cth self-loop?, s→cth directly?). B-dialect shows a parallel grammar with different preferred transitions (qok→sh→ch→ot?). A full Markov grammar would be the strongest evidence yet for genuine syntactic structure.
**Cost estimate:** small

---

## H245: cth-Onset Vocabulary — Are cth-Words a Closed or Open Noun Class?
**Priority:** medium
**Status:** CONFIRMED PARTIAL (exp_126) — cth is a SEMI-CLOSED nominal class: top5=55.4% (vs ch=28.1%, sh=36.8%); herbal+pharma=90% of tokens; A-cth=85 types (71.6% hapax), B-cth=20 types (hybrid forms); A/B Jaccard=0.117; NOT a productive prefix — marks specialized herbal/pharma nominal vocabulary; high hapax at margins indicates large rare plant-name inventory (F133)
**Source:** F129: cth-onset is the target of the A-dialect NP template (daiin→cth=2.77×, chol→daiin→cth). If cth-words are nouns, they should form a relatively closed class (finite vocabulary). F114: cth- strips to reveal constrained stems. H222 (tested as exp_109): cth-onset hapax rate vs other onset classes?
**Description:** Characterize the cth-onset vocabulary: (1) how many distinct cth-types are there? (2) what is the hapax rate (types seen only once)? (3) what is the frequency distribution (Zipfian? Geometric? Evidence for open/closed class)? (4) compare to qok-onset (B-paradigm "noun" class). (5) are cth-words section-specific (different cth words in herbal vs pharma vs cosmo)? (6) what is the cth-word type-token ratio vs baseline? A closed class would show low hapax rate, high repetition, small type count. An open class would show high hapax rate, low repetition, Zipfian distribution.
**Expected outcome:** cth-onset is a semi-closed class (small vocabulary, moderate hapax, strong section specialization) consistent with a proper-noun or plant-name-like lexicon in herbal/pharma sections. This would support the "herbal glossary" interpretation where cth-words name plants.
**Cost estimate:** small

---

## H246: Suffix Sequence Within Lines — Is There a Positional Suffix Grammar?
**Priority:** medium
**Status:** CONFIRMED (exp_126) — Within-line suffix grammar confirmed in A-dialect: -or(0.371) < -ol(0.441) < -ey/-aiin(0.45-0.53) < -dy/-al(0.58-0.59) < -am(0.799); -or enriched at 0-20%(1.51×); -dy/-al enriched at 80-100%(1.51×/1.50×); aiin→am=4.62× strongest suffix bigram; -ol before -aiin=54.6% (p<0.01); B-dialect same directionality but flatter; full line grammar = line-level NP template (F133)
**Source:** F129: Suffix encodes syntactic position (aiin=cth-determiner, ol=pre-d, or=pre-noun). If suffixes encode syntactic position, then WITHIN a line, the suffix sequence should show systematic patterns: e.g., -ol words appear before -aiin words appear before content words. Is there a within-line suffix grammar?
**Description:** For each line, extract the sequence of suffixes. Compute: (1) suffix bigrams within lines (what suffix follows what suffix? constrained or free?); (2) suffix positional enrichment within lines by line-fraction (0=start, 1=end) rather than absolute position; (3) test whether -ol appears before -aiin within the same line; (4) entropy of suffix at each fractional position. Compare A-dialect and B-dialect. 
**Expected outcome:** Within A-dialect lines: -ol suffix appears at fraction 0.2-0.4 (modifier position); -aiin appears at 0.3-0.5 (determiner position); cth-onset at 0.4-0.6 (noun position); -y/-dy at 0.7-1.0 (closing position). This would confirm that the within-line suffix sequence is a positional grammar, not random.
**Cost estimate:** small

---

## H247: l-Onset Prefix Class — Is 'l' a B-Dialect Morphological Prefix?
**Priority:** high
**Status:** CONFIRMED (exp_124) — l is a B-dialect morphological prefix: stem recovery=91.3% (vs qo=54.8%); A/B=0.097 (10.3× B-dominant); stars=1.83×, cosmo=1.42×; -edy=2.32×; lk-subclass=80% stars; l-words 17.9% line-last; four prefix classes: o-/qo-/cth-/l- (F131)
**Source:** F130: Stars "other"-onset analysis revealed lchedy (52), lkaiin (39), lkeedy (30), lkeey (34), lkain (28) — words starting with 'l' that are heavily stars-concentrated (lkaiin=81% in stars). These appear to be l+[B-onset-word] compounds. If 'l' is a morphological prefix (like 'o-', 'qo-', 'cth-'), then l-stripped words should appear as standalone words in the vocabulary. This would add a fourth B-dialect prefix to the taxonomy.
**Description:** Extract all words starting with 'l' in the manuscript. Strip the 'l' and check if the remainder is in the vocabulary (l-stem rate). Compare to qo-prefix (qo-stripped stem recovery rate = 42%). Compute: (1) dialect distribution of l-initial words; (2) section distribution; (3) suffix distribution (do they take B-paradigm suffixes?); (4) l-stripped stems: what onset classes? (5) bigram behavior: what precedes and follows l-onset words? Compare to o-prefix structure.
**Expected outcome:** l-onset is a B-dialect prefix (B-enriched), stars-concentrated, that strips to reveal k-/ch-initial stems (similar to qo-prefix). l-stripped stems appear in the vocabulary. This would extend the onset taxonomy with 'l' as a fourth recognized prefix class.
**Cost estimate:** small

---

## H248: k-Onset Words — Are They a Separate Productive Class or l-stripped k-Stems?
**Priority:** medium
**Status:** CONFIRMED (exp_124) — k is a stem-initial segment (NOT independent prefix); generates 3-prefix paradigm: bare-k (A-herbal f1-56), qo+k (B-body), l+k (B-stars/cosmo f75-116); kaiin vs lkaiin are section-disjoint; qo-stripped qok-words = k-stems; k-suffix = mixed A+B (F131)
**Source:** F130: Stars "other"-onset analysis found kaiin (36), keedy (34), keey (21), kain (20), kedy (14) — k-initial words that are 47-55% stars-concentrated. These could be: (1) standalone k-onset words (k is a recognized onset in the inner structure but not in the onset taxonomy); (2) l-prefix stripped forms (lkaiin → kaiin = l-stripped form?); (3) a third prefix class.
**Description:** Characterize k-initial words: (1) frequency and section distribution; (2) suffix distribution (do they take B-paradigm suffixes?); (3) are k-initial words = l-stripped forms (does lkaiin → kaiin correspond?); (4) is 'k' a recognized stem-initial character in the EVA alphabet?; (5) co-occurrence: do kaiin and lkaiin appear in the same paragraphs? (6) bigram behavior: what precedes k-onset words?
**Expected outcome:** k-onset words are related to the l-prefix class (lkaiin is l + kaiin; kaiin alone also appears as a free form). This would reveal a k-onset sub-class that is either a stripped form of l-compounds or an independent onset class analogous to ch/sh.
**Cost estimate:** small

---

## H249: Full Prefix Paradigm Reconstruction — Do All Major Stem Classes Take (bare/qo-/l-) Prefixes?
**Priority:** high
**Status:** CONFIRMED (exp_125) — Four-prefix paradigm generalizes to all k/t stems: ok=o+k, ot=o+t, qok=qo+k, qot=qo+t; ch/sh-stems take ONLY l-prefix (lchedy=116, qochedy=1 absent); qo-prefix is exclusively k/t-stem selective; new prefix classes: r-(87% recovery, 8.4× B), p-(76%, B), y-(86%, balanced); full taxonomy: o-/qo-/l-/r-/p-/y-/cth-; onset taxonomy requires revision: ok/ot/qok/qot are derived (F132)
**Source:** F131: k-stems generate a three-prefix paradigm (bare-k/qo+k/l+k). Does this generalize? Do ch-stems have bare-ch vs qo+ch vs l+ch? (qokaiin=qo+kaiin; qochor=qo+chor?). Test: for each major stem class (ch-, sh-, k-, t-, ot-), compute what prefixes appear (bare vs qo vs l vs o) and what section/dialect each prefix form appears in.
**Description:** Build a systematic prefix paradigm table: for each stem class, count bare/qo-/l-/o- prefixed forms. Compute: (1) stem recovery rate for each prefix applied to each stem class; (2) section distribution of each prefix×stem combination; (3) is there a consistent pattern: bare=A-herbal, qo=B-body, l=B-stars/cosmo, o=labels? Test ch-stem: chedy(bare) vs qo+chedy=? vs l+chedy=lchedy. Also test t-stem (taiin, teedy) with l-prefix (ltaiin?, lteedy?).
**Expected outcome:** The prefix paradigm generalizes: ch-stems take l-prefix for B-stars/cosmo context (lchedy is the top l-word, n=116); qo+ch is a recognized form. t-stems may similarly have l+t forms (lteedy appears 6 times in stars). This would establish a complete FOUR-PREFIX system: o-[labels]/bare[A-herbal]/qo-[B-body]/l-[B-stars+cosmo].
**Cost estimate:** small

---

## H250: cth-Onset in B-Dialect — What ARE the 52 cth-Tokens in B-Text?
**Priority:** medium
**Status:** CONFIRMED (exp_125) — B-cth (n=55) = hybrid morphological forms: cthedy (B_frac=0.917) and cthdy (B_frac=1.000) are B-dialect-specific (B-paradigm suffix on cth-onset); other B-cth are A-vocabulary words in B-herbal folios (cthy/cthor/cthol B_frac≤0.05); concentrated in B-herbal folios f26/f48 (~20‰) and stars f113/f116; pre-B-cth: ch=2.03×; B-cth→cth=n=1 only (exp_123's 8.79× was single-token artifact); B-scribes applied -edy/-dy suffixes to cth-onset creating B-specific hybrid forms (F132)
**Source:** F127: cth appears only 52 times in 20,236 B-dialect tokens (2.57‰ vs 39.29‰ in A). F130: B-dialect cth→cth=8.79× (extreme self-clustering). These 52 B-dialect cth-tokens are anomalous — are they: (1) B-dialect folios that contain some A-dialect text (code-switching); (2) a specific set of formulaic cth-words repeated in B-text; (3) a specific section or folio localization?
**Description:** Extract all cth-onset tokens in B-dialect text. Characterize: (1) which specific words (cthy, cthor, cthol, etc.); (2) which folios and sections contain them; (3) are they in specific paragraphs or distributed evenly?; (4) do they appear next to A-paradigm words (daiin, chol) or B-paradigm words (shedy, qokeedy)?; (5) are these the same cth-words as in A-dialect or different cth-words?
**Expected outcome:** B-dialect cth-tokens are: (a) localized to specific folios with mixed A/B dialect content (folio-level misclassification), OR (b) a fixed set of cth-words used formulaically in B-dialect (e.g., as proper names or section headings), OR (c) A-dialect insertions into B-dialect folios. The cth→cth=8.79× self-clustering suggests they cluster in specific passages.
**Cost estimate:** small

---

## H251: y-Prefix Class Full Characterization — What Are the 1374 y-Prefix Words?
**Priority:** high
**Status:** CONFIRMED (exp_127) — y-prefix splits into A-y (y+A-paradigm: ycheor/ydaiin/ytchy, B%≤25%, herbal) and B-y (y+B-paradigm: yteedy/ykeedy/ykedy, B%=100%, herbal+stars); both select k/t-stems (65.4% = same as qo-/o-); A/B Jaccard=0.174; line-start=39.6% (grammatical position prefix); y= dialect-neutral k/t-stem prefix marking line-continuation (F134)
**Source:** F132: y-prefix was discovered as a new prefix class (1374 tokens, 85.6% stem recovery, A/B ratio=0.76 = balanced). Unlike r- (8.4× B) and p- (3.4× B), y- is nearly dialect-neutral. The y-prefix class appeared in stars line-start analysis (exp_123) and prefix recovery (exp_125). What are y-words? What stems do they attach to? What section/dialect/position profile do they have?
**Description:** Extract all y-initial words (≥2 chars) from body text. Characterize: (1) top y-words by frequency; (2) y-stripped stem distribution (what onset classes after stripping y?); (3) dialect distribution of y-words (A vs B); (4) section distribution (herbal/cosmo/stars/pharma); (5) positional behavior (line-start vs line-end vs medial); (6) do y-words appear in both A-dialect and B-dialect text or are there separate A-y and B-y vocabularies? Cross-reference with the known "y-initial = line-continuation particle" (F057) and "y-prefix = B-para-start" observations (F130).
**Expected outcome:** y-prefix shows two sub-types: (a) A-dialect y-words (y+ch/sh stems, appearing as continuation particles within A paragraphs) and (b) B-dialect y-words (y+k/t stems appearing at B-line-starts as formula openers). These may be homophonous y-prefixes with different grammatical functions. If the y-stem recovery is 85.6% for both, the underlying stems should be identifiable.
**Cost estimate:** small
**Prerequisites:** F132 (y-prefix identified in prefix taxonomy)

---

## H252: aiin→am Formulaic Construction — Is [daiin][am] a Recurrent A-Dialect Phrase?
**Priority:** medium
**Status:** CONFIRMED (exp_127) — NOT a fixed phrase; 67 bigrams span 57 unique pairs; [daiin][dam]=6 (herbal only); stars=36% of instances; aiin→am=4.62× is distributional artifact of -am as universal line-closer co-occurring with -aiin words in same lines (F134)
**Source:** F133: aiin→am suffix bigram = 4.62× (strongest suffix bigram in the corpus; after -aiin words, -am words follow at 4.62×). This could mean: (a) [daiin][dam] is a formulaic phrase closing determiner phrases; (b) [daiin][am] as a particle sequence; (c) any -aiin word is followed by a line-closing am-word at elevated rates.
**Description:** Test: (1) What are the specific word pairs that generate aiin→am=4.62×? Tabulate top [word_aiin][word_am] bigrams. (2) Is daiin specifically involved or is it any -aiin word? (3) Does [daiin][dam] appear as a fixed phrase? (4) What comes before and after this phrase? (5) How many times does this bigram appear and in which sections/folios?
**Expected outcome:** [daiin][dam] or [daiin][am] is a small recurrent phrase in A-dialect herbal (consistent with the NP template: [chol][daiin][cthy][dam] = complete A-dialect sentence). If confirmed, this would give us the full 4-word A-dialect sentence template.
**Cost estimate:** trivial
**Prerequisites:** F133

---

## H253: Full A-Dialect Line Template — Is [-or/-ol][daiin][cthy][-am] a Canonical 4-Word Sentence?
**Priority:** high
**Status:** CONFIRMED WEAK (exp_127) — 4-gram enriched 4.92× vs independence (3 observed/0.6 expected); all 3 in A-herbal; 3-gram has 23 matches; template is real but rare — cth-noun often ends phrase before closer; canonical A-clause is [chol/chor][daiin][cthy] ± closer (F134)
**Source:** F133: The within-line suffix grammar reveals [-or/-ol modifier] → [-aiin determiner] → [cth-noun] → [-am closer]. If these four elements constitute the canonical A-dialect line, we should see the 4-gram [chol/chor][daiin][cthy/cthol][dam/am] at enriched rates. F128: The 3-gram [chol][daiin][cth-noun] is confirmed (n=26). Can we extend to the full 4-gram?
**Description:** Search for 4-grams matching the template [W1=-ol/-or][W2=daiin/okaiin][W3=cth-onset][W4=-am/-dy/-al]. Compute: (1) how many 4-grams match; (2) what are the most common 4-gram instances; (3) what fraction of A-dialect lines contain this template; (4) is the 4-gram significantly enriched vs random onset sequence? Also test: does the -or word come BEFORE the -ol word (consistent with positional order)?
**Expected outcome:** The full 4-gram [chor][daiin][cthy][dam] appears at enriched rates. This would be the most complete grammatical template recovered from the manuscript: a full 4-word A-dialect clause. Even if only 5-10% of A-dialect lines contain this exact template, that would be structurally significant.
**Cost estimate:** small
**Prerequisites:** F128 (3-gram template), F133 (4th element -am identified)

---

## H254: p-Prefix Class Characterization — What Are the 528 p-Prefix Words?
**Priority:** high
**Status:** CONFIRMED (exp_128) — p-prefix is B-dialect LINE-OPENER on ch/sh-stems (ch=45.5%); line-start=71.1% (5.72×); stars=43.4%, cosmo=16.8%; A/B=0.31; Jaccard=0.095; pchedy=35 (100%B); stem recovery=76.9%; POSITIONAL PREFIX SYSTEM: p=OPENER, r=CLOSER bracket B-dialect lines (F135)
**Source:** F132: p-prefix discovered as new prefix class (528 tokens, 76.1% stem recovery, A/B=0.30 = 3.4× B-dominant, stars=43%). Similar to r-prefix (87% recovery, 8.4× B, stars). p-onset was already identified as a B-paragraph-START marker (pchedy/tchedy=B-para-starts, 17-18× enriched, F057). But F132 treats p as a PREFIX — is p-onset = p-prefix on ch/sh/k/t stems?
**Description:** Extract all p-initial words (≥2 chars). Characterize: (1) p-stripped stems: what onset classes? (stem recovery rate); (2) dialect distribution (A vs B); (3) section distribution; (4) positional behavior (para-start vs line-start vs medial); (5) suffix distribution; (6) is pchedy = p + chedy (B-paradigm stem) or an independent word? Cross-reference with F057 (pchedy=para-start) and F076 (p-onset=75.3% first = primary para-start).
**Expected outcome:** p-prefix on ch/sh/k/t stems — pchedy=p+chedy, pchy=p+chy. The para-start enrichment of p-onset (17-18×) reflects that the p-prefix marks paragraph-initial position — i.e., p is BOTH a morphological prefix AND a positional marker (like y- being a line-continuation marker). p- = B-dialect paragraph-start marker; y- = line-continuation opener; these are the two positional prefix types.
**Cost estimate:** small
**Prerequisites:** F132 (p-prefix in taxonomy), F134 (y-prefix as grammatical positional prefix)

---

## H255: r-Prefix Class Characterization — What Are the 346 r-Prefix Words?
**Priority:** medium
**Status:** CONFIRMED (exp_128) — r-prefix is B-dialect LINE-CLOSER on PARTICLE STEMS (64.5%: aiin/ain/ar/al/or/am); line-end=28.7%; stars=51.6%, cosmo=32.6%; A/B=0.12 (8.3×B); creates prefixed particles: raiin(61), rain(21), rar(17), ral(15), ror(14); stem recovery=84.8%; Jaccard=0.111 (F135)
**Source:** F132: r-prefix (346 tokens, 87.0% stem recovery = highest, A/B=0.12 = 8.4× B-dominant, stars=51%). r-onset words: raiin, rain, raram, roar. If r is a prefix: r+aiin=raiin, r+am=ram, r+ar=rar. But r-initial words are quite short — what stems do they strip to?
**Description:** Extract all r-initial words. (1) r-stripped stems (what are they?); (2) are the stems common vocabulary? (3) dialect and section distribution; (4) suffix distribution; (5) what precedes and follows r-words? Is r-prefix restricted to specific stem classes?
**Expected outcome:** r-stripped stems = mostly aiin/am/ar/al particles — r-prefix on particle stems creates r-particle forms. This would explain the 87.0% stem recovery (r+aiin=raiin; raiin→aiin is in vocabulary). The 8.4× B-dominance and stars concentration suggests r-prefix marks specific B-stars content.
**Cost estimate:** small
**Prerequisites:** F132

---

## H256: p and r Form a Complementary LINE-BRACKET Pair — Do B-Dialect Lines Template as [p-word][content][r-word]?
**Priority:** high
**Status:** NOT CONFIRMED (exp_129) — p+r co-occurrence=1.29× (13 observed/10.1 expected); p and r are independent positional markers, not a mandatory line-bracket pair; B-lines p-start=12%, r-end=3.5%, both=0.5% (near independence); p and r are each enriched at their individual positions but do not preferentially co-occur (F136)
**Source:** F135: p-prefix is a B-dialect line-opener (71.1% line-start) and r-prefix is a B-dialect line-closer (28.7% line-end). These form a positional complementary pair. Do they co-occur in the same lines? Is there a B-dialect line template [p-word][...content...][r-word]?
**Description:** (1) What fraction of B-dialect lines contain both a p-initial word (at start) AND an r-initial word (at end)? (2) What section shows highest p+r co-occurrence? (3) Compute enrichment: P(r-word at end | p-word at start) vs P(r-word at end | no p-word at start). (4) What are the most common p+r line combinations? (5) Is there a characteristic line length for lines with both p and r?
**Expected outcome:** B-dialect stars/cosmo lines frequently have p-word at start and r-word at end. The enrichment would confirm p and r as grammatical line-bracket markers. This would be the most complete structural template yet: [p-opener][content phrase][r-closer] = B-dialect line template.
**Cost estimate:** trivial
**Prerequisites:** F135

---

## H257: r-Prefix on Particles — Are raiin vs aiin in Different Syntactic Contexts?
**Priority:** medium
**Status:** CONFIRMED PARTIAL (exp_129) — raiin=B-stars/cosmo medial particle (63.9% stars, 93.4% B); pre-raiin s=3.25× (topic openers), ch=1.68×, NOT other (0.13×); post-raiin ot=2.36×, sh=1.81×; raiin≠daiin (no post-raiin cth enrichment); raiin pattern: [s-opener][content][raiin][ot/sh]; r-prefix creates B-stars specific particle forms (F136)
**Source:** F135: r-prefix creates "prefixed particle" forms (raiin=61, rain=21, rar=17, ral=15, ror=14, ram=11). If r-prefix is morphologically meaningful, raiin should appear in different syntactic contexts than aiin. What precedes raiin vs aiin? What follows raiin vs aiin?
**Description:** For raiin and aiin: (1) compute onset class of preceding word; (2) compute onset class of following word; (3) suffix distribution of raiin vs aiin; (4) section distribution (raiin=64% stars, aiin=?); (5) line-position distribution. Is raiin a B-stars determiner parallel to daiin in A-herbal?
**Expected outcome:** raiin appears in B-stars context where aiin appears in A-herbal context — they are dialectal/section counterparts (daiin=A-determiner, raiin=B-stars particle). Pre-raiin and pre-aiin should show different onset class enrichments.
**Cost estimate:** small
**Prerequisites:** F135

---

## H258: B-Herbal Folio Onset Profile Diagnostic — What Specific Onset Classes Make f40/f26/f31/f48/f50 Cluster with Stars/Pharma Rather Than Herbal?
**Priority:** high
**Status:** CONFIRMED (exp_132) — ALL B-herbal folios universally depleted in cth (mean_dev=-0.037) and d (mean_dev=-0.062). Most elevated in ok/qok/other. f40→stars because ok=16.1% (3.8× A-herbal). f26/f31/f50→pharma (pharma also has elevated qok vs A-herbal). f48→astro (elevated ot/t). f43/f46 B-dialect but herbal-best-match (less extreme B-vocabulary). (F139)
**Source:** F138: B-herbal bifolio insertions (f26/f31/f40/f48/f50) all best-match sections other than herbal by cosine similarity on onset-class profile vectors. f40→stars(0.860 vs self=0.755); f26/f31→pharma(0.966/0.959); f48→astro(0.890); f50→pharma(0.893). The onset-class DIFFERENCE between these B-herbal folios and the herbal centroid is the key diagnostic.
**Description:** For each B-herbal folio (f26, f31, f40, f48, f50): (1) compute onset-class profile; (2) subtract herbal centroid to get per-class deviation; (3) identify which onset classes are OVER- and UNDER-represented vs A-herbal; (4) compare deviation profile to the best-match section's centroid. Specifically: does f40 have elevated qok/ok/ot (B-paradigm classes) and depleted cth/ch-onset (A-paradigm classes)?
**Expected outcome:** B-herbal folios are elevated in qok/ok/ot/p onset classes (B-paradigm content words) and depleted in cth/ch (A-paradigm) relative to A-herbal. f40 specifically matches stars because it has stars-level qok/ot and depleted A-paradigm classes. f26/f31 match pharma because pharma also uses elevated qok relative to A-herbal.
**Cost estimate:** small
**Prerequisites:** F138 (exp_131 folio profile vectors); onset-class taxonomy from exp_131

---

## H259: s-Onset Characterization — Is s a SECTION MARKER and LINE-OPENING GRAMMATICAL PARTICLE? Sub-Classes of s-Onset Words?
**Priority:** high
**Status:** CONFIRMED (exp_132) — s=LINE-OPENER class (LF=48.9%). Two sub-classes: s-OPENERS (saiin/sain/sol/soiin=50-72%LF, sshedy/sshey=100%LF) and s-CLOSERS (sy=85%LL, sam=89%LL). Post-s sh=1.92× (s→sh sequential rule). Cosmo=1.52×, astro=2.15× concentrated; stars=0.67× depleted. Stars s-words are rare but 67.2% LF. (F139)
**Source:** F138: s=6.56× at stars line-start (strongest section-specific enrichment after p=6.84×). F126: s-onset is para-start marker (48.5% para-first position). F136: pre-raiin s=3.25× (s-words immediately precede raiin in B-stars). s appears to be a critical grammatical onset class that has NOT been characterized in depth (unlike d/p/r/y which have all been analyzed).
**Description:** Characterize all s-onset words: (1) total tokens, types, hapax rate; (2) positional profile (line-first/mid/last %); (3) section/dialect distribution; (4) top s-words and their positional profiles; (5) sub-classes: are there s-openers vs s-closers vs s-particles? (6) bigram context: what precedes s-words, what follows? (7) comparison to d-onset (which has three sub-classes): does s also have opener/closer/medial sub-classes?
**Expected outcome:** s-onset splits into at least two sub-classes: (1) s-openers (saiin, sar, sain = line-start, topic-opening function); (2) s-content words in stars (stars-specific s-vocabulary). s is a GRAMMATICAL OPENER (parallel to d-openers but perhaps more stars-specific). s-onset has lower vocabulary diversity than d-onset but higher positional concentration.
**Cost estimate:** small

---

## H261: Cosmo vs Stars Differentiation — What Onset Classes, Suffixes, and Positional Patterns Distinguish Cosmo from Stars? Why Is Cosmo the Most Internally Cohesive Section?
**Priority:** high
**Status:** CONFIRMED (exp_133) — Cosmo=ol-dominant (2.06×), qok-dominant (1.75×), s-line-opener (17.7%), -y line-closer (25.5%). Stars=ch-dominant (near baseline), ot-elevated (1.43×), -am line-closer (17.0%), ch+eo exclusive vocabulary. Jaccard=0.178. (F140)
**Source:** F138: Cosmo=most cohesive (0.965), Stars=second (0.954). Both are B-dialect sections (F139: s=1.52× in cosmo, but 0.67× in stars). F120: Stars uses -eey suffix more; cosmo prefers -eedy. F131: cosmo=75-84, stars=103-116 — these are non-contiguous sections. What structural differences make cosmo more cohesive than stars?
**Description:** For each onset class and suffix: compute cosmo vs stars rate comparison. Identify onset classes that are cosmo-enriched vs stars-enriched. Compute per-folio onset profiles for cosmo (n=10 folios) and stars (n=12 folios). Also compare: line-positional patterns, top words, vocabulary Jaccard between cosmo and stars. Is cosmo more homogeneous because it has fewer topics (one astronomical theme) or fewer scribes?
**Expected outcome:** Cosmo has specific onset classes elevated: s (1.52×), possibly ol or specific content classes. Stars has ok (0.704×) and l-onset (lchedy, lkaiin) elevated. The cosmo-stars vocabulary distinction is captured by 2-3 onset classes. Both sections share the same B-paradigm suffix system but with stars preferring -eey and cosmo preferring -eedy.
**Cost estimate:** small

---

## H262: ol-Onset Characterization — Is ol a Distinct Onset Class (Cosmo 2.06× Corpus) with Sub-Classes? What Are the ol-Stem Words and Their Positional Profiles?
**Priority:** high
**Status:** CONFIRMED (exp_134) — ol=MEDIAL class (MID=74.6%, LF=7.7%). Cosmo=2.06×. Standalone ol(n=474, 84%MID) + ol+k-stem B-cosmo compound words. ol self-chains (post-ol=ol 1.89×). ol-CLOSERS: oly=81.8%LL. ol = o-prefix + l-stem-word (olkeedy=36 ↔ lkeedy=36). (F141)
**Source:** F140: ol=9.08% in cosmo (2.06× corpus baseline, 2.61× vs stars). F137: oly=81.2%LL (B-cosmo line-closer). ol-onset is the most cosmo-enriched onset class but has not been characterized in depth (unlike d/s/p/r/y which have all been analyzed). From F139: ol onset classified separately from 'other'.
**Description:** Extract all ol-onset words. Compute: (1) tokens, types, hapax rate; (2) positional profile (LF/MID/LL %); (3) section/dialect distribution; (4) sub-classes: openers vs closers vs medials; (5) top words and their individual profiles; (6) bigram context (pre-ol and post-ol onset enrichment); (7) whether ol = o-prefix + l-stem (morphological derivation) or an independent onset class.
**Expected outcome:** ol-onset splits into: (1) ol-CLOSERS (oly=81.2%LL, oldy, olchedy? — confirmed from F137); (2) ol-medials (ol=the standalone word, most common?). ol is predominantly B-dialect and cosmo-concentrated. Pre-ol and post-ol show specific enrichments related to cosmo grammar.
**Cost estimate:** small

---

## H264: Cosmo Line-Element Template — Does Cosmo Have a Formal Line-Template Analogous to Stars' [OPENER][sh-2nd (2.25×)][-am LAST (8.06×)]?
**Priority:** high
**Status:** CONFIRMED (exp_135) — Cosmo template: [s/y/p/t/d OPENER (2.6-4.7×)][sh 2nd (1.75×)][l/r/ol CLOSER][−am(7.87×) or −y/−dy SUFFIX CLOSER]. -am CLOSER is pan-B-section (cosmo=7.87×, stars=7.48×). cth absent from cosmo first (consistent with B-dialect cth depletion). (F142)
**Source:** F138: Stars has a line-element template [p/s/y/d/t OPENER (5-7×)][sh-2nd (2.25×)][-am LAST (8.06×)]. F140: Cosmo line-first dominated by s(17.7%)+qok(16.9%); line-last =-y(25.5%); cosmo is the most internally cohesive section (0.965). F141: ol self-chains (post-ol=ol 1.89×) in cosmo lines. What is the complete cosmo line-element template?
**Description:** For cosmo body text: (1) compute line-position onset enrichment (first/second/mid/last) — how enriched is each onset class at each position? (2) compute line-position suffix enrichment (first/mid/last) — what suffix classes cluster at line-start vs line-end in cosmo? (3) compare cosmo enrichments to stars enrichments from F138 — are the same position classes used? (4) identify the cosmo line template analogous to the stars template.
**Expected outcome:** Cosmo line template: [s or qok OPENER][ol or sh-content MID][ol-chain][oly or -y CLOSER]. The cosmo template should have qok at line-start (16.9% LF from F140), ol self-chaining in the middle, and -y suffix at line-end. The template is distinct from stars but uses the same slot structure.
**Cost estimate:** small
**Prerequisites:** F138, F140, F141

---

## H265: Cross-Section Vocabulary Jaccard Matrix — What Is the Full Pairwise Similarity Between All 5 Sections?
**Priority:** medium
**Status:** CONFIRMED (exp_135) — Cosmo-stars=closest pair (J=0.1371); herbal-pharma=0.1209; herbal-stars=0.1199. Astro=most isolated (astro-stars=0.0434). 71-word universal vocabulary core dominated by d/ol onsets. Herbal=vocabulary superset (0 absent types when word is in all other 4). (F142)
**Source:** F140: cosmo-stars Jaccard=0.178; cosmo-herbal=0.134; stars-herbal=0.164. But the full 5×5 matrix (herbal/pharma/stars/cosmo/astro) has not been computed. Which section pairs share the most vocabulary?
**Description:** Compute pairwise Jaccard similarity (type overlap) for all 5 sections. Also compute overlap with A-dialect only and B-dialect only subcorpora. Do herbal-pharma share more vocabulary than herbal-stars? What is the "vocabulary distance tree" of the manuscript sections?
**Expected outcome:** Herbal-pharma Jaccard > herbal-stars Jaccard (A-dialect sections share more vocabulary). Stars-cosmo Jaccard > stars-herbal (B-dialect sections share more). A full distance matrix would allow dendrogram-style section clustering.
**Cost estimate:** trivial
**Prerequisites:** F140

---

## H271: Folio-Level Onset Gradient — Do Onset Classes Change Systematically Across Manuscript Folio Sequence?
**Priority:** high
**Status:** CONFIRMED (exp_137) — Six onset classes show folio gradient |ρ|>0.5: d(ρ=-0.641), cth(ρ=-0.613), l(ρ=+0.640), qok(ρ=+0.609), ol(ρ=+0.534), ch(ρ=-0.534). sh/s: ρ≈0. Within-herbal cth(ρ=-0.486), l(ρ=+0.476). Stars cth(ρ=+0.469, UNEXPECTED). 10-folio running means show clear phase transitions at section boundaries. (F144)
**Source:** New hypothesis arising from cross-section analysis; folio sequence as proxy for manuscript organization.

---

## H272: Is the Within-Herbal cth Gradient Driven by B-Herbal Insertions or a Genuine A-Herbal Scribal Shift?
**Priority:** high
**Status:** CONFIRMED PARTIAL (exp_138) — A-herbal-only ρ=-0.353 (44 folios): genuine A-herbal cth decline. B-insertions amplify (full-herbal ρ=-0.486) but don't create the gradient. Early A-herbal cth=5.4%, late=3.7% (0.69×). l-gradient also real in A-herbal (ρ=+0.457, later A-herbal has more l-onset words). (F145)
**Source:** F144: Within-herbal cth ρ=-0.486 (notable). cth=6-10% in f1-f20 → ~0% in f40-f57. Is this explained entirely by the 12 B-herbal folios (which have cth≈0 by B-dialect definition), or does A-herbal itself show a cth gradient?
**Description:** (1) Extract A-herbal-only folios (exclude all B-dialect folios from herbal section); (2) compute cth gradient within A-herbal alone; (3) compare A-herbal cth rate at early folios (f1-f25) vs late folios (f26-f57). If gradient disappears in A-herbal-only, the within-herbal trend is a B-insertion artifact. If gradient remains, there's a genuine A-herbal scribal shift in cth use.
**Expected outcome:** B-insertions fully explain the gradient (A-herbal-only gradient disappears or weakens to ρ<0.2). If residual gradient remains, it would suggest the A-herbal scribe also changed register toward the end of the herbal section.
**Cost estimate:** trivial (sub-analysis of existing data)
**Prerequisites:** F144, F139

---

## H273: Why Does cth INCREASE Within Stars (ρ=+0.469)? Is It Driven by Specific Later-Stars Folios?
**Priority:** medium
**Status:** NOT CONFIRMED (NOISE ARTIFACT) (exp_138) — Stars cth = 19 total tokens (0.25% rate across 7748 words). The ρ=+0.469 is entirely driven by f113 (7 tokens, 0.77%) and f116 (4 tokens, 0.79%); all other stars folios have 0-3 tokens. With only 19 total tokens, Spearman ρ is statistically unreliable — this is sampling noise, not a real gradient. F144's stars-cth ρ=+0.469 claim is RETRACTED by F145. (F145)
**Source:** F144: Stars cth ρ=+0.469 (unexpected positive correlation — cth/ch increase in later stars folios). Stars is supposed to be B-dialect (cth-depleted by F139). Later stars folios (f112-f116) may have unusual cth/ch vocabulary.
**Description:** (1) Compute per-folio cth rate in stars (f103-f116); (2) identify which folios drive the upward trend; (3) check whether these are B-cth hybrid forms (cthedy/cthdy from F132) or genuine cth-onset words; (4) check folio-level dialect assignment of later stars folios.
**Expected outcome:** Later stars folios (f113-f116) have slightly elevated cth from B-cth hybrid forms (cthedy at f113/f116 from F132). The ρ=+0.469 is driven by a handful of folios with unusual vocabulary.
**Cost estimate:** trivial
**Prerequisites:** F144, F132

---

## H274: What Is the Full Onset/Suffix Profile of f47 (Herbal/A, Most Deviant A-Herbal Folio)?
**Priority:** medium
**Status:** CONFIRMED (exp_138) — f47 is a sampling artifact (n=134 words). ch=35.1% (2.06×) explained by chol=11 (3.0×), chy=6 (4.6×), chdy=3 (34.9×) — small-sample chance over-representation. y=0% and qo=0% consistent with n=134 draws from 6.5%/2.5% rates. Cosine similarity: herbal=0.8473 (best match). f47 is a normal A-herbal folio with no scribal anomaly. (F145)
**Source:** F144: f47 (herbal/A) is the most deviant A-herbal folio (dev=0.2375) with ch:+20.0% above A-herbal centroid. This anomaly makes f47 potentially a mislabeled dialect or a scribal outlier.
**Description:** Compute f47's complete onset-class and suffix profile. Compare to: A-herbal centroid, B-herbal centroid, pharma centroid. Check: (1) Is f47's ch elevation driven by specific ch-words? (2) Does f47's vocabulary match any other section or folio more than A-herbal?
**Expected outcome:** f47 is genuinely unusual — likely an A-herbal folio with specific botanical content driving unusual ch-onset vocabulary. Its best-match section may be pharma or A-herbal-pharma.
**Cost estimate:** trivial
**Prerequisites:** F144

---

## H287: Is daiin a Determiner for cth-Nominals Specifically, or a General Particle?
**Priority:** high
**Status:** CONFIRMED (exp_145) — daiin→cth in A: 3.19× enrichment (43 cases). No other tested particle precedes cth-words at all (0.00×). daiin→cth is categorically unique. In B-dialect: daiin→cth=0.0%, but daiin→sh=2.33× and daiin→ch_e=2.11× — functional role preserved, target onset class shifts. daiin is a dialect-specific "category determiner" for the marked onset class (cth in A; sh/ch_e in B). (F152)
**Source:** F151: daiin precedes cth-words 43 times in A-dialect (daiin→cthy=9, daiin→cthol=6, daiin→cthor=6). But is daiin enriched SPECIFICALLY before cth-onset, or does it precede all onset classes equally?
**Description:** Compute daiin→[onset] transition matrix in A-dialect: (1) What is daiin's most common following onset? (2) Is cth-onset enriched after daiin vs baseline cth rate? (3) Compare to other high-frequency particles (aiin, ain, ar, or, al) — do they also precede cth at elevated rates? (4) Does the same daiin→cth enrichment appear in B-dialect (where cth is rare)?
**Expected outcome:** daiin is a general linker that precedes content words at baseline rates — not a cth-specific determiner. If daiin does show specific cth enrichment (>2×), it would suggest daiin is a grammatical determiner for the cth-nominal class specifically, the strongest evidence for functional word classes in Voynichese.
**Cost estimate:** small
**Prerequisites:** F151, F143 (universal core findings)

---

## H288: Does ot-Onset Have a Distinct Positional Profile (Quantity/Modifier Role)?
**Priority:** medium
**Source:** F151: ot-onset follows cthor at 6.18× enrichment; ot appears in "cthor→ot-word" nominal phrases. If ot-words are quantity/size modifiers, they should be more LL-enriched or second-position concentrated than typical medial content words.
**Description:** Compute positional distribution (LF/MID/LL) of ot-words in A-dialect (all sections). Compare: (1) A ot-words vs A baseline; (2) top ot-words (otol, oty, otaiin, otchy) individually; (3) B ot-words vs B baseline. Are ot-words distributed differently than ch/cth-onset words?
**Expected outcome:** ot-words are slightly LL-enriched (as modifiers appearing late in nominal phrases) or second-position concentrated. This would confirm ot as a "modifier/adjective" class distinct from the "nominal" cth/ch classes.
**Cost estimate:** small
**Prerequisites:** F151

---

## H289: Is daiin's B-Dialect Role (Preceding sh/ch_e at 2.33×/2.11×) the Functional Parallel to Its A-Dialect Role (Preceding cth at 3.19×)?
**Priority:** high
**Status:** NOT CONFIRMED (exp_146). B-sh is a LINE-OPENER (LF=1.90×), not a medial nominal like A-cth (LF≈0.94×). Before-sh in B: qok-enriched (1.42×), d near-baseline (1.20×); before-cth in A: d-enriched (1.30×), qok-suppressed. No self-succession for sh (0.93×) or ch_e (0.87×) in B; A-cth has 1.84×. The daiin→sh enrichment (2.33×) reflects both daiin and sh being LF-enriched in B sequential grammar, NOT a determiner-nominal construction. (F153)
**Source:** F152: daiin→sh=2.33× and daiin→ch_e=2.11× in B-dialect; all other B-particles depleted before sh/ch_e (0.31×–0.45×). If daiin's role as "category determiner" is preserved cross-dialect, then sh/ch_e-words in B should have the same positional profile that cth-words show in A.
**Description:** Compute for B-dialect sh-words and ch_e-words: (1) Positional distribution (LF/MID/LL) — are sh/ch_e-words LF-depleted and LL-enriched, like A-dialect cth-words? (2) Before-context enrichment — is d-onset enriched before sh/ch_e at ~1.5× in B (parallel to d before cthol=1.51× in A)? (3) Self-succession — do sh-words precede sh/ch_e-words at elevated rates (~1.5-2×), mirroring cth before cthol? If all three checks confirm, the grammatical parallel is complete: [daiin][sh-word] in B = [daiin][cth-word] in A syntactically.
**Expected outcome:** sh-words in B are somewhat LF-depleted (consistent with medial content words) and have d-enrichment at ~1.5×. If confirmed, this establishes that daiin encodes the same syntactic role cross-dialect, with sh/ch_e being the B-dialect functional equivalent of cth in A.
**Cost estimate:** small
**Prerequisites:** F152

---

## H290: What Particle (If Any) in B-Dialect Plays the cth-Determiner Role That daiin Plays in A?
**Priority:** medium
**Status:** NOT CONFIRMED (exp_146). No single B-particle is enriched before l-onset at 3×+. At onset-class level: ch_e=1.42×, ch=1.27× (modest). Individual -eey words (okeey=3.37×, qokey=2.96×, chey=2.94×) are enriched but small n. d is strongly DEPLETED before l in B (0.42×). The pre-l structure in B is a morphological pattern (l follows -eey suffix class), not a single determiner. No B-equivalent of daiin's categorical cth-determiner exists. (F153)
**Source:** F152: daiin is the UNIQUE cth-determiner in A (3.19×, all others 0.00×). In B-dialect, what precedes l-onset words (B's functional content-word class analogous to A's cth) at elevated enrichment? Is there a particle X such that X→l-onset is enriched at ~3× in B, while all other particles show near-zero?
**Description:** Compute transition matrix for B-dialect: (1) For high-frequency B particles (aiin, ar, ol, chol, shedy, qokedy), compute enrichment before l-onset words. (2) Are any B-particles enriched before l-onset at ≥2×? (3) What is daiin→l-onset enrichment in B? (If daiin→l is also enriched in B, daiin may be a cross-dialect "content-word determiner," not just cth-specific). (4) Compare lchedy-specific vs all l-onset enrichment.
**Expected outcome:** Either (a) daiin→l is enriched in B at ~2× (daiin is cross-dialect, onset-class-general determiner that shifts target per dialect); or (b) a different B-particle (e.g., aiin or chol) uniquely precedes l-words at elevated rates; or (c) l-onset words in B have no specific determiner (distributed across many particles at ~baseline). Most likely: no strong B-determiner for l, since B grammar organizes around the qo/sh hinge rather than a determiner-content word sequence.
**Cost estimate:** small
**Prerequisites:** F152

---

## H291: Is B-ch (Not sh or ch_e) the B-Dialect Medial Nominal Parallel to A-cth?
**Priority:** medium
**Status:** PARTIALLY CONFIRMED (exp_147). B-compound-ch words (chdy/chckhy/chcthy/chody) are MID-enriched (1.10-1.28×) and LF-depleted (0.52-0.68×). ch self-succession=1.57×. BUT d is DEPLETED before B-ch (0.79×) — opposite to A-cth where d=1.30×. Positional parallel holds; before-context parallel does NOT. B-ch and A-cth are "medial self-coherent" word classes but with different grammatical predecessors. (F154)
**Source:** F153: B-ch shows 1.57× self-succession (closer to A-cth's 1.84× than sh=0.93× or ch_e=0.87×). B-ch is LF-depleted (0.77×), MID-enriched (1.05×) — the positional profile closest to a medial nominal class. sh is a line-opener; ch_e is near-baseline.
**Description:** Examine B-ch in detail: (1) Positional profile of specific B-ch words (chedy, chaiin, chol, chor, chey) — do any show strong MID-enrichment and LF-depletion? (2) Before-context: is d-onset enriched before B-ch-words at ~1.5× (parallel to d before A-cthol)? (3) After-context: does B-ch follow qo at elevated rates (i.e., qo→ch bigram enrichment, part of B's qo↔ch/sh alternation grammar)? (4) What is daiin→ch enrichment in B? If B-ch is the medial nominal parallel, daiin should precede it at elevated rates.
**Expected outcome:** B-ch-words (especially chedy) show MID-enrichment (>70% MID) and d-enriched before-context (~1.5×), confirming B-ch as the medial nominal equivalent of A-cth. This would reframe daiin→ch_e (2.11×) as more relevant than daiin→sh (2.33×).
**Cost estimate:** small
**Prerequisites:** F153

---

## H293: Are B-Compound-ch Words (chckhy/chcthy) a Distinct Morphological Class From Simple ch-Words (chol/chdy)?
**Priority:** medium
**Source:** F154: Top B ch-words are compound-gallows forms (chckhy=102, chcthy=52, chckhey=25) containing embedded {ck} and {ct} digraphs. These are structurally different from simple ch-words (chol=70, chdy=103). Do they form a separate morphological subclass?
**Description:** (1) Compute suffix distribution of compound-ch (chck-/chct-) vs simple ch-words — do compound forms have a distinctive suffix paradigm? (2) Section distribution: are compound-ch words concentrated in specific B sections? (3) Positional: do compound-ch words differ from simple ch-words in LF/MID/LL rates? (4) Are compound-ch words precursors of any specific word class?
**Expected outcome:** Compound-ch words are more MID-concentrated (as found) and may be a B-specific "heavy morpheme" class. If they're section-specific (stars/cosmo B), they may be a specialized vocabulary class for those sections.
**Cost estimate:** small
**Prerequisites:** F154

---

## H294: B-daiin→d=2.70× — Is This daiin Self-Succession or True daiin→d Enrichment?
**Priority:** medium
**Status:** CONFIRMED (TRUE ENRICHMENT, exp_148). Only 3/24 daiin→d cases are daiin self-succession. Remaining 21 cases are diverse d-words at 2.85× enrichment. A-daiin→d=1.40× (weaker). A/B reversal on sh/ch_e confirmed: A-daiin→sh=0.64×/ch_e=0.42× (depleted); B-daiin→ch_e=1.77× (enriched). B-daiin is a d/ch_e introducer; A-daiin is a cth-specific gatekeeper. (F155)
**Source:** F154: In B P-type body text, daiin→d=2.70× enriched (24/160 cases). Top words after daiin: daiin(3), dam(2), dar(2). Is this enrichment driven by daiin→daiin self-succession, or does daiin precede all d-onset words at elevated rates?
**Description:** (1) Compute daiin→daiin separately vs daiin→dam vs daiin→dar vs daiin→(other d-words) in B. (2) If daiin→daiin is high (e.g., >5%), subtract it: does daiin→(non-self d-words) remain enriched? (3) Compare daiin→d in A-dialect vs B-dialect (A daiin→d may also be enriched). (4) What is the B baseline rate for daiin→daiin specifically (vs daiin rate = d rate = independent)?
**Expected outcome:** daiin self-succession (daiin→daiin) exists but contributes only a fraction of the daiin→d=2.70× signal. If daiin→dam and daiin→dar are both enriched independently, daiin precedes the d-onset class in general in B — potentially as a line-boundary connector before d-words. This would parallel A-cth's d-predecessor enrichment but in B-dialect with d as the "content class."
**Cost estimate:** trivial
**Prerequisites:** F154

---

## H295: In A-Dialect, Are sh/ch_e-Onset Words Introduced by a Different Particle (Not daiin)?
**Priority:** medium
**Status:** NOT CONFIRMED (exp_149). No A-particle introduces sh at ≥2.5× or ch_e at ≥2.5× systematically. sh is self-introduced (sh-succession 1.68×); ch_e is self-introduced (ch_e-succession 1.98×) with ok/qok enrichment (1.50-1.56×). The "cth-enriched particle cluster" (daiin/chol/chor/cthol) depletes sh/ch_e; aiin/ol/ar→cth=0.00× but →ch_e=1.43-1.97×. daiin's categorical cth-gatekeeping has no parallel for sh/ch_e. (F156)
**Source:** F155: A-daiin→sh=0.64× and A-daiin→ch_e=0.42× (depleted). daiin is a cth-gatekeeper that avoids sh/ch_e. What particle (if any) introduces sh/ch_e-words in A-dialect at elevated rates? If A has its own sh/ch_e introducer (parallel to daiin→cth), this would establish a complete A-dialect particle taxonomy: [daiin→cth] + [X→sh] + [Y→ch_e].
**Description:** Compute transition matrix for A-dialect: for each high-frequency A particle (aiin, or, ol, chol, chor, dain, saiin, ar), compute enrichment before sh-onset and before ch_e-onset. Is any A-particle enriched at ≥2× before sh or ch_e? Compare to daiin→sh (0.64×) as the depleted baseline.
**Expected outcome:** No single A-particle specifically introduces sh or ch_e at 3× (as daiin does for cth). Instead, sh/ch_e in A-dialect appear after diverse onset classes near baseline. If a specific A-particle does introduce sh at 2×, it reveals an A-dialect grammatical slot parallel to daiin's cth-gatekeeper role.
**Cost estimate:** small
**Prerequisites:** F155

---

## H296: Are the d-Words After B-daiin the Same as Those After A-daiin, or Dialect-Specific?
**Priority:** low
**Source:** F155: B-daiin→d=2.85× with top words dam(2), dar(2), dal(3). A-daiin→d=1.40× with top words daiin(8), dain(5), dar(4), dam(4). Both dialects show daiin→dam and daiin→dar, but enrichment is much stronger in B (2.85× vs 1.40×).
**Description:** Compute: (1) for each specific d-word (dam, dar, dal, dain, daiin, dor, dy, dol), what is its rate after daiin in A vs B? (2) Are there B-exclusive d-words that appear after B-daiin at high rates? (3) Is the A-daiin→d=1.40× driven by the same specific d-words as B-daiin→d=2.85×? This would reveal whether daiin→d is a cross-dialect construction (same d-words appear after daiin in both A and B) or a B-specific grammatical pattern.
**Expected outcome:** dam/dar appear after daiin in both A and B (cross-dialect construction). B has additionally enriched daiin→dal/dol/dady (B-specific d-words). The underlying daiin→dam/dar bigram is a pan-Voynichese construction; B augments it with additional d-followers that don't appear in A.
**Cost estimate:** trivial
**Prerequisites:** F155

---

## H297: Do the "cth-Introducer" Particles (daiin/chol/chor/cthol) Appear in Specific Positions Before cth-Words?
**Priority:** medium
**Status:** CONFIRMED WITH SURPRISE (exp_150). Two distinct cth-introduction constructions: Type 1=[daiin@MID→cth@MID/LL] (daiin=within-line medial determiner); Type 2=[chol/chor@LF→cth@second] (line-opener construction, not determiner). aiin/ol/ar/s→cth=0 bigrams (categorical). cthol→cth fully medial. Cluster=2.77× collective enrichment (22.9% of before-cth). (F157)
**Source:** F156: daiin/chol/chor/cthol all precede cth at 2.1-3.1× and deplete sh/ch_e. They form a cluster of "cth-nominal introducer" particles. Do they appear in specific positional contexts (LF vs second vs MID) when they precede cth-words?
**Description:** For each of daiin/chol/chor/cthol: (1) When it precedes a cth-onset word, what slot is it in? (LF, second, MID?) (2) Is the pattern that these particles appear at line-final (LL) position and the cth-word opens the NEXT line, or within the same line? (3) Compute: when the bigram [particle→cth] occurs, what is the positional slot of the particle? This reveals whether "cth-introduction" is within-line (particle at MID; cth-word at MID+1) or cross-line (particle at LL; cth-word at LF of next line).
**Expected outcome:** daiin precedes cth within the same line (both at MID positions). If confirmed, daiin is a within-line determiner. If particle is at LL and cth is at LF, these are line-boundary bigrams — counting line-boundary bigrams should be excluded for within-line grammar analysis.
**Cost estimate:** small
**Prerequisites:** F156

---

## H298: Is dy→sh=1.96× a Within-Line Construction or a Cross-Line Bigram Artifact?
**Priority:** low
**Status:** CONFIRMED NOT ARTIFACT (exp_150). All 6 dy→sh bigrams have dy at second/MID/LF (never LL). Among non-LL dy occurrences (~32), ~19% are followed by sh (vs ~10% baseline). Real within-line construction. (F157)
**Source:** F156: dy→sh=1.96× (n=6/32 transitions). dy is primarily a line-final short word in A; if dy appears at line-end (LL) and sh appears at LF of the next line, the bigram spans a line boundary and is not a syntactic construction.
**Description:** Check all 6 dy→sh bigrams: are they within the same parsed line (same locus P-type line) or cross-line (dy at end of line N, sh at start of line N+1)? If all 6 are within-line, dy→sh is a real construction. If most are cross-line, the enrichment is a line-boundary artifact.
**Expected outcome:** dy→sh is a cross-line artifact (dy ending one line, next line starting with sh). This would confirm that line-boundary bigrams inflate apparent enrichments for line-final words (dy) followed by line-initial onset classes (sh).
**Cost estimate:** trivial
**Prerequisites:** F156

---

## H299: In A-Dialect, What Fraction of Lines Beginning with chol or chor Have a cth-Word at Position 2?
**Priority:** medium
**Status:** CONFIRMED (exp_151). chol@LF → cth@second = 14.1% (3.11×); chor@LF → cth@second = 10.7% (2.37×); shol@LF = 9.7% (2.14×). Baseline = 4.53%. chol-opening lines have cth anywhere in 31.2%. (F158)
**Source:** F157: Type 2 cth-introduction = [chol/chor at LF] → [cth-word at second] (n=32 bigrams). chol/chor at LF are followed by cth at second in 45-50% of chol/chor→cth bigrams. But what fraction of ALL chol-at-LF lines have cth at second?
**Description:** (1) Count all A P-type lines where first word is chol or chor. (2) What fraction have a cth-onset word at second position? (3) Compare to baseline: what is the rate of cth at second across all A lines? (4) Is there a specific set of chol-starting or chor-starting lines that consistently produce cth at second (e.g., specific folios or sections)?
**Expected outcome:** ~10-20% of chol-at-LF lines have cth at second (elevated above baseline ~4-5%). If this holds, the Type 2 construction [chol at LF][cth at second] is a recurring A-herbal formula, not an artifact of the reverse selection (we found chol→cth bigrams and looked at chol's position).
**Cost estimate:** trivial
**Prerequisites:** F157

---

## H300: Do cth-Words at LL (Line-Final) Tend to Be Specific cth-Words (e.g., cthol/cthy vs cthor)?
**Priority:** medium
**Status:** CONFIRMED (exp_151). 4-way cth positional paradigm: cthor=LF(1.76×)/LL-depleted(0.35×); cthol=second(1.94×); cthody/ctheody=MID(1.29-1.68×); cthy=LL(1.39×). daiin→cthy→LL=5 cases (dominant); daiin→cthol→MID=6 cases. (F158)
**Source:** F157: daiin→cth places cth-word at LL 36.1% of the time (13/36 cases). Also, cth has overall mild LL-enrichment (1.20×). Are line-final cth-words from a specific subset of the cth vocabulary?
**Description:** (1) Compute positional distribution (LF/second/MID/LL) for each top cth-word: cthy, cthol, cthor, cthain, ctheol, cthody. (2) Are some cth-words LL-enriched (line-closers) while others are MID-enriched (medial nominals)? (3) Specifically: does cthol or cthy show strong LL-enrichment (closing role), while cthor remains MID/second (medial role)? This would reveal a positional paradigm split within the cth vocabulary.
**Expected outcome:** cthol (the most common medial cth-word per F148) is MID-enriched (confirmed from exp_141). cthy may be LL-enriched (closing role). cthor is MID/second (confirmed from exp_142). A LL-enriched cth-word (cthy or cthain) would be the "cth-closing particle" completing the daiin→cth-at-LL construction.
**Cost estimate:** small
**Prerequisites:** F157, F148

---

## H301: What is cthor's Full Positional Profile in A-Herbal vs A-Pharma? Is cthor's LF=1.76× Concentrated in Herbal?
**Priority:** medium
**Status:** FAILED (exp_152) — section-mapping bug: SECTION_MAP used 'f1' keys but folio_base values are 'f1r'/'f1v'. Fix: strip r/v suffix before lookup. H303 is the retry.
**Source:** F158: cthor is LF-enriched (1.76×) across all A-dialect. cthor was previously noted (F147/F149) to have anomalous positional behavior. Does cthor's LF-enrichment come specifically from A-herbal lines?
**Description:** (1) Compute cthor positional distribution (LF/second/MID/LL) separately for A-herbal vs A-pharma vs A-other sections. (2) In A-herbal specifically: what is cthor's LF% vs baseline? (3) What is the most common second word after cthor-at-LF? This reveals whether cthor is a line-opening nominal in herbal-specific constructions.
**Expected outcome:** cthor's LF=1.76× is driven by A-herbal (section where cth-words are concentrated). In A-pharma, cthor may be near-baseline. A-herbal cthor-at-LF is likely followed by cthol or cthy (the second-position/medial cth-words).
**Cost estimate:** trivial
**Prerequisites:** F158

---

## H302: Is cthol@Second Driven by the Type 2 [Line-Opener][cthol] Construction or Also Appears Second in Other Contexts?
**Priority:** medium
**Status:** PARTIALLY CONFIRMED (exp_152). cthol@second (n=15): ch-onset LF=40%, d(daiin)=20%, sh=13%. chol/chor specific=33%. General ch/sh-opening lines account for most cthol@second cases. Not exclusively Type 2. Also: daiin is penultimate before cthy@LL in 4/21=19% (~5× enriched) — confirming [daiin][cthy→LL] construction. (F159)
**Source:** F158: cthol appears at second position 31.2% (1.94×). This could be driven by the Type 2 [chol/chor at LF][cthol at second] construction, or cthol may independently appear at second in other contexts (e.g., after daiin at LF, or after other line-openers).
**Description:** For all A lines where cthol is at second position: (1) What word is at LF? Distribution across chol/chor/daiin/other. (2) What fraction of cthol@second come from chol/chor-opening lines vs other contexts? (3) Is cthol@second specifically a Type 2 phenomenon, or does it appear broadly at second across diverse LF words?
**Expected outcome:** ~30-50% of cthol@second cases come from chol/chor-opening lines (Type 2). The remaining 50-70% come from other line-openers (y+ch, d+ch type), showing cthol is independently enriched at second across diverse contexts.
**Cost estimate:** trivial
**Prerequisites:** F158

---

## H303: cthor Section Profile — RETRY WITH CORRECT FOLIO MAPPING (H301 BUG FIX)
**Priority:** medium
**Status:** STILL FAILED (exp_153) — folio_to_section returns 'other' for ALL A-dialect words (n=9165, herbal/pharma/astro all n=0) despite attempted fix with re.match(r'f(\d+)', folio_base). Root cause unclear. H305 is the diagnostic retry.
**Source:** F159: H301 failed due to section_map bug (folio_base 'f1r' ≠ key 'f1'). Fix: `folio_num = int(re.sub(r'[rv]$', '', folio_base[1:]))` to extract numeric folio, then look up section.
**Description:** Re-run cthor positional profile by section (herbal/pharma/astro/other) in A-dialect with correct folio→section mapping. (1) cthor count per section; (2) positional profile (LF/second/MID/LL) per section; (3) Is cthor's LF=1.76× concentration driven by A-herbal specifically?
**Expected outcome:** cthor is concentrated in A-herbal (consistent with F147 finding that cthor is an A-herbal specific word with T1>>T3 gradient). cthor's LF=1.76× will be confirmed or refined within A-herbal.
**Cost estimate:** trivial
**Prerequisites:** F159

---

## H304: Is [daiin][cthy] A Specific Two-Word Fixed Phrase, or Does daiin Enrich Before ALL cth-Words at LL?
**Priority:** medium
**Status:** CONFIRMED (exp_153) — daiin=3.57× enriched as penultimate before cthy@LL (4/21=19.0% vs 5.34% baseline); 0.00× before cthol@LL (0/5), cthor@LL (0/2), cthody@LL (0/2), cthain@LL (0/1). The enrichment is SPECIFIC to cthy — categorical 0× for all other cth-words at LL. (F160)
**Source:** F159: daiin is penultimate before cthy@LL 4/21=19% (~5× enriched). Is this enrichment specific to cthy, or does daiin also enrich before cthol@LL, cthor@LL, etc.?
**Description:** (1) For each cth-word at LL, compute penultimate word distribution. (2) Is daiin enriched specifically before cthy@LL or equally before all cth-words@LL? (3) Compute: baseline daiin rate as penultimate word vs daiin rate as penultimate before cthy@LL vs cthol@LL vs cthor@LL. If daiin enriches only before cthy@LL, [daiin][cthy] is a specific fixed phrase. If daiin enriches before all cth@LL equally, daiin→cth@LL is a general construction (daiin introduces line-final cth-words).
**Expected outcome:** daiin specifically enriches before cthy@LL (not equally before all cth@LL). This would confirm [daiin][cthy] as a two-word fixed phrase (nominal closing construction), analogous to a determined noun phrase where daiin=determiner and cthy=the specific nominal form used at line-ends.
**Cost estimate:** trivial
**Prerequisites:** F159

---

## H305: Diagnostic — Why Does folio_to_section Return 'other' for ALL A-Dialect Folios?
**Priority:** high
**Status:** RESOLVED (exp_154) — Bug: folio_base value was `<f1r` (locus `<f1r.1,@P0>` → folio_raw=`<f1r` → split('.')[0]=`<f1r` — leading '<' not stripped). Fix: `.lstrip('<')` → 'f1r' → regex matches correctly. (F161)
**Source:** F160: H303 section analysis failed in exp_152 AND exp_153 despite attempted folio_base→section fix. Both runs returned all A-dialect tokens as 'other' (herbal/pharma/astro all n=0). Root cause unknown.
**Description:** Run a targeted diagnostic: (1) Print 10 sample folio_base values from A-dialect P-type tokens. (2) Print the SECTION_MAP keys. (3) Trace the regex match step by step for a sample folio_base. (4) Check: is the section_map keyed by int or string? Is folio_num an int or string? Is the folio range in SECTION_MAP covering the right folios? Report the exact values at each step.
**Expected outcome:** Identify the exact failure point (e.g., type mismatch int vs string, wrong folio range, folio_base format different from expected, regex group() failure). Fix and re-run cthor section analysis (H303).
**Cost estimate:** trivial
**Prerequisites:** F160

---

## H306: When daiin→cthy Occurs, Is cthy Always at LL, or Also at MID?
**Priority:** medium
**Status:** CONFIRMED (exp_154) — daiin→cthy (n=9): cthy at LL=55.6% (2.12× enriched), cthy at MID=44.4% (0.78×), 0× at LF/second. daiin is an LL-specific selector for cthy. (F161)
**Source:** F160: [daiin][cthy] confirmed as specific two-word fixed phrase at LL. But does daiin→cthy also occur when cthy is at MID? If daiin→cthy is exclusively or predominantly LL-targeted, daiin is a line-terminal selector. If daiin→cthy also appears with cthy at MID frequently, daiin is a general cthy-introducer (not LL-specific).
**Description:** (1) For all daiin→cthy bigrams in A P-type body text, compute cthy's positional slot (LF/second/MID/LL). (2) What fraction of daiin→cthy bigrams have cthy at LL vs MID vs other? (3) Compare: baseline cthy positional distribution vs daiin-selected cthy positional distribution. Does daiin shift cthy toward LL?
**Expected outcome:** daiin→cthy bigrams have cthy at LL in majority (>50%), confirming daiin is a line-terminal selector for cthy. If cthy@MID is also common after daiin, the [daiin][cthy] fixed phrase is not LL-specific but a general determined-nominal phrase.
**Cost estimate:** trivial
**Prerequisites:** F160

---

## H307: Corrected cthol@Second Analysis — Which LF Words Precede cthol at Second (i=1)?
**Priority:** high
**Status:** CONFIRMED with surprise (exp_155) — cthol@second (n=9): qot=6.30×, y=2.16×, ch=0.00×. F159's "ch=40% before cthol@second" retracted. (F162)
**Source:** F161: corrected cthol@second n=9 (not 15 as in F159/exp_152 which had swapped LF/second). F159's H302 analysis of "cthol@second LF-word distribution" may be invalid. Need re-run with correct slot code.
**Description:** (1) Find all A P-type lines where cthol appears at i=1 (second, corrected definition). (2) What word appears at i=0 (LF) in these lines? (3) Compute onset distribution of LF words when cthol is at second. Is it ch-dominated (40%) as F159 claimed, or different? (4) Compare to cthol@MID LF-word distribution.
**Expected outcome:** If the F159 analysis was computing cthol@LF incorrectly, the LF-word distribution for true cthol@second will differ. We expect the Type 2 [chol/chor@LF][cthol@second] construction to still hold but possibly at different proportions.
**Cost estimate:** trivial
**Prerequisites:** F161

---

## H308: What Is the LF Word (i=0) When cthor Is at Second (i=1)? Is [chol/chor@LF][cthor@second] The Dominant Construction?
**Priority:** high
**Status:** CONFIRMED (exp_155) — cthor@second (n=11): d-onset=36.4% (2.25×), daiin 3/11=27.3% at LF. chol/chor at LF: 0 cases. (F162)
**Source:** F161: cthor=SECOND-enriched (2.16×). cthor appears at i=1 in 11/33 A-dialect cases. What is the i=0 (LF) word in these cases? The corrected Type 2 construction (F157) may specifically be [chol/chor@LF][cthor@second] rather than [chol/chor@LF][cthol@second].
**Description:** (1) Extract all A P-type lines where cthor is at i=1 (second). (2) What word is at i=0 (LF)? (3) Compute onset distribution — is ch-class dominant? Is chol specifically dominant? (4) Compare to the baseline LF word distribution. Is there a specific [LF-word][cthor@second] bigram pattern?
**Expected outcome:** chol/chor or more broadly ch-onset words dominate LF position when cthor is at second — consistent with the Type 2 line-opening construction ([chol/chor@LF][cthor@second]). This would pin down which cth-word the chol/chor opener specifically introduces.
**Cost estimate:** trivial
**Prerequisites:** F161

---

## H309: Is the Type 2 [chol/chor@LF][cth@second] Construction Specifically [chol@LF][cthor@second], or Is It Spread Across cthol/cthy/cthody@second Too?
**Priority:** medium
**Status:** RESOLVED BY H309 (exp_155) — chol/chor@LF → cth@second = 0/26 (0%). Type 2 construction does not exist. (F162)
**Source:** F161: cthor=SECOND-enriched (2.16×), cthol=MID-enriched. The F157 "Type 2 construction" was described as chol/chor at LF → cth at second/MID. Now with corrected data: is the specific second-position cth-word predominantly cthor (not cthol)? F157's analysis placed cth-word at second=45-50% after chol/chor — but which cth-word was it?
**Description:** (1) For all chol@LF bigrams with cth-word at second (i=1): which cth-words appear? Is cthor dominant? (2) For chor@LF bigrams with cth-word at second: which cth-words? (3) Compute: P(cthor@second | chol@LF) vs P(cthol@second | chol@LF) vs P(cthy@second | chol@LF). The dominant second-position cth-word after chol/chor defines the Type 2 construction.
**Expected outcome:** cthor dominates at second after chol/chor@LF (since cthor is the most second-enriched cth-word). This would make the Type 2 construction specifically [chol/chor@LF][cthor@second], with cthol appearing later at MID.
**Cost estimate:** trivial
**Prerequisites:** F161, H308

---

## H310: What Is the Actual Positional Context of chol→cth Bigrams? (chol@LF Never Precedes cth — Where Does chol→cth Occur?)
**Priority:** high
**Status:** CONFIRMED (exp_156) — chol→cth bigrams: chol@second=55%, chol@MID=45%, chol@LF=0%. chol=second-enriched (1.87×), LF-depleted (0.30×). (F163)
**Source:** F162: chol/chor at LF never have cth at second (0/26). But chol→cth bigram enrichment is real (F156). Where does chol appear when it precedes a cth-word? Is chol@MID → cth@subsequent MID the actual construction?
**Description:** (1) Extract all chol→cth bigrams in A P-type body text. (2) For each bigram, record chol's position (LF/second/MID/LL). (3) Compute position distribution — is chol predominantly at MID or second when it precedes cth? (4) Same for chor→cth bigrams. (5) Compare: chol's overall positional distribution vs chol's positional distribution specifically when preceding cth.
**Expected outcome:** chol→cth bigrams occur with chol at MID position (not LF). This would establish a within-line medial construction [chol@MID → cth@subsequent] as the actual basis of the chol→cth enrichment.
**Cost estimate:** trivial
**Prerequisites:** F162

---

## H311: After chol@LF, What Specific ch-Words Follow at Second? Is [chol@LF][chol/chor@second] a Reduplication Construction?
**Priority:** medium
**Status:** CONFIRMED (exp_156) — chol@LF → ch-onset at second = 54.5% (~8× enriched). Chol self-succession=18.2% (2/11). [chol@LF][ch@second] is the dominant chol-opening construction. (F163)
**Source:** F162: chol@LF → second-pos = ch-onset 45.5% (5/11 lines), sh 18.2%, d 18.2%. Which specific ch-words follow chol at LF?
**Description:** (1) List all second-position words after chol@LF. (2) Is chol→chol or chol→chor the dominant pattern? (3) Compute enrichment of specific ch-words at second after chol@LF vs baseline. (4) Is there a [chol@LF][chol@second] reduplication? Such reduplication could indicate a specific determiner/nominal pair construction where chol is both opener and a second-position word.
**Expected outcome:** chol→chor or chol→chol at second (ch-reduplication), suggesting lines with chol@LF have a ch-word phrase at the front before moving to medial content.
**Cost estimate:** trivial
**Prerequisites:** F162

---

## H312: Verify chol/chor→cth BIGRAM ENRICHMENT WITH CORRECTED POSITIONAL CODE
**Priority:** medium
**Status:** CONFIRMED (exp_156) — chol→cth=2.35×, chor→cth=2.22× (real, corrected corpus). (F163)
**Source:** F162: chol/chor→cth bigram enrichment was established in F156/exp_149 using inline code that may have had slot-swapping bugs. Verify the bigram enrichment is real (not positional artifact) using corrected parsing.
**Description:** (1) Re-run chol→cth and chor→cth bigram enrichment analysis with corrected corpus parser (lstrip '<', P-type only). (2) Compute: how many chol→cth and chor→cth bigrams exist? (3) Compare to F156's values (chol→cth n=20, chor→cth n=12). If counts match, enrichment is confirmed real. (4) For each bigram, record positions of both words.
**Expected outcome:** chol→cth and chor→cth bigrams are real (counts match F156), confirming the enrichment is a real syntactic relationship. The positional context (chol at MID) will be established from H310.
**Cost estimate:** trivial
**Prerequisites:** F162

---

## H313: What Is the LF Word When chol Is at Second? (In [LF][chol@second][cth@MID] Construction)
**Priority:** high
**Source:** F163: chol→cth bigrams occur at chol@second (55%) — so there's a LF word at i=0 before chol@second. What opens these lines?
**Description:** (1) Extract all A P-type lines where chol is at second (i=1). (2) What word is at LF (i=0)? (3) Compute onset distribution. Is any onset specifically enriched before chol@second? (4) Specifically: does daiin or another cth-enriched word appear at LF when chol is at second?
**Expected outcome:** A specific word class opens lines with chol@second. Possibly d-class/daiin (as daiin opens cthor@second lines), or a distinct class from the cthor@second case.
**Cost estimate:** trivial
**Prerequisites:** F163

---

## H314: Verify daiin→cth Bigram Positional Context With Corrected Code
**Priority:** high
**Source:** F157 described "daiin at MID(61%)" preceding cth-words — but exp_150 had slot-swapping bugs. Need corrected positional analysis of daiin→cth bigrams.
**Description:** (1) Extract all daiin→cth bigrams in A P-type body text. (2) For each bigram, record daiin's positional slot (LF/second/MID/LL). (3) daiin's overall positional distribution in A. (4) Is daiin predominantly at MID (as F157 claimed) or at second or other positions when preceding cth-words?
**Expected outcome:** daiin is MID-enriched when preceding cth-words (consistent with "daiin as medial determiner"). If daiin is actually second-enriched, the daiin→cth construction occurs at [LF-word][daiin@second][cth@MID] rather than from deep within the line.
**Cost estimate:** trivial
**Prerequisites:** F163

---

## H292: The -eey Suffix Class Precedes B l-Onset Words at 2.7-3.4×. Is This a Specific [-eey][l-word] Morphological Sequence or Section Artifact?
**Priority:** medium
**Source:** F153: -eey suffix words (okeey=3.37×, qokey=2.96×, chey=2.94×, oteey=2.66×, cheey=2.27×) are the dominant precursors of l-onset words in B-dialect. This appears across different onset classes (ok/qo/ch/ot all with -eey suffix) — the suffix, not the onset, drives the pattern.
**Description:** (1) What is the suffix distribution of words preceding l-onset in B? Specifically: what percentage end in -eey/-ey vs -edy/-aiin/-ain? (2) Is the [-eey word][l-word] construction section-concentrated (e.g., in stars B or cosmo B where l-words concentrate)? (3) Are the -eey+l collocations specific word pairs (e.g., always okeey+lchedy) or spread across diverse l-words? (4) Compute: baseline -eey rate in B vs -eey rate specifically before l-onset.
**Expected outcome:** The -eey→l construction is section-specific (likely stars B, which has many l-words and -eey vocabulary). If the enrichment disappears when controlling for section, it is an artifact. If it persists across sections, it may reflect a genuine morphological coupling: [-eey words form phrases ending in l-words].
**Cost estimate:** small
**Prerequisites:** F153

---

## H285: Is the "daiin cthor ot*" Construction Botanically Specific?
**Priority:** medium
**Status:** CONFIRMED (exp_144) — All 3 "daiin cthor ot*" are preceded by qo/ok-words (qoty, qotchy, okchor). Extended construction: [qo/ok][daiin][cthor][ot*]. daiin is a universal cth-preceder (43 cases, not cthor-specific). (F151)
**Source:** F150: "daiin cthor ot*" triple appears 3× (f10, f14, f19 — all early A-herbal). Is this a specific botanical description formula?
**Description:** Examine the context of all 3 "daiin cthor ot*" occurrences: (1) What follows the ot-word? (2) What precedes daiin in each case? (3) Are folios f10, f14, f19 botanically related (neighboring plants in the herbal sequence)? Compare to daiin usage in general A-herbal (is daiin commonly a preceding context for other cth-words?).
**Expected outcome:** "daiin cthor ot*" is a botanical nominal phrase (plant type + shape + quantity) appearing in specific folio clusters. daiin as a cth-word preceder suggests daiin functions as a determiner or classificatory particle.
**Cost estimate:** trivial
**Prerequisites:** F150, F149

---

## H286: Which Specific ch-Words Follow cthor? (cthor→ch is Most Common at 26.7%)
**Priority:** medium
**Status:** CONFIRMED (exp_144) — cthor→chol dominates (3/8, 37.5%). "daiin cthor chol" 2× (f15, f19). cthor also followed by chor(1), chaiin(1), cholchom(1). No B-paradigm ch-words (chedy) follow cthor. (F151)
**Source:** F150: cthor is followed by ch-onset in 26.7% of cases (8/30) — the most common after-cthor onset. Which ch-words specifically? If cthor is followed predominantly by chol/chor (the canonical ch-nominal forms), this would be a second "cthor→ch-nominal" bigram pattern parallel to cthor→ot.
**Description:** Extract all cthor→ch bigrams (A-herbal). Which ch-words follow cthor most often? Compute enrichment vs baseline ch-word frequency.
**Expected outcome:** cthor→chol or cthor→chor dominates, suggesting "cthor [ch-content-word]" is a second-position + medial nominal phrase formula. If cthor→chedy or cthor→cheey dominate, cthor may precede B-paradigm forms more than expected.
**Cost estimate:** trivial
**Prerequisites:** F150

---

## H283: What Is the cthor→ot Bigram? Which Specific ot-Words Follow cthor?
**Priority:** medium
**Status:** PARTIALLY CONFIRMED (exp_143) — cthor→ot: 21.9% of cthor usages (7/32). "daiin cthor ot*" triple recurrent 3×. Varied ot-words (otol/oty/otydy/otam/otal). Spread across f9-f52 (not early-specific). cthor decline not due to cthor→ot disappearing. (F150)
**Source:** F149: cthor at MID is followed by ot-onset at 6.18× (7/29 cases). ot-onset words include otal, otol, otaiin, otchol. Is this a specific botanical construction?
**Description:** Extract all cthor→[ot-word] bigrams from A-herbal. Compute: (1) Which ot-words follow cthor? (2) Are these cthor→ot bigrams concentrated in specific early A-herbal folios? (3) Does the cthor→ot pattern map to any botanical description pattern (e.g., "cth-form ot-quantity" or similar)?
**Expected outcome:** cthor→otal or cthor→otol dominates, appearing in specific early A-herbal folios. Their folio distribution would explain cthor's faster decline in late A-herbal.
**Cost estimate:** trivial
**Prerequisites:** F149, F147

---

## H284: Are There "cth-Runs" (2-3 Consecutive cth-Words) in A-Herbal?
**Priority:** medium
**Status:** NOT CONFIRMED (RARE) (exp_143) — 93.2% of cth-words are isolated; only 6.8% in 2+ runs (19 total runs). All 17 consecutive cth-bigrams are hapax. No dominant cth-cluster formula. cth self-succession enrichment (exp_142) is relative enrichment from a small base. (F150)
**Source:** F149: cth self-succession is enriched (cth before cthol=1.55×, cth after cthol=2.25×). This suggests cth-onset words appear in clusters.
**Description:** Extract all consecutive cth-onset word sequences (runs of 2+) from A-herbal. Compute: (1) How many runs of 2+ cth-words? (2) What are the top cth-bigrams and trigrams? (3) Are cth-runs concentrated in specific folios or periods?
**Expected outcome:** cth-runs of 2 are relatively common (perhaps 10-15% of cth-tokens appear in runs). Specific cth-bigrams like [cthy][cthol] or [cthol][cthey] dominate. This would confirm that cth-onset words form a "noun phrase cluster" in A-herbal.
**Cost estimate:** trivial
**Prerequisites:** F149

---

## H281: Is cthor Positionally Distinct from cthol? (cthor LF=39.4% vs cthol LF=20.4%)
**Priority:** medium
**Status:** CONFIRMED (exp_142) — F148 "cthor LF=39.4%" was measurement artifact (LF+second combined). True cthor LF=6.1%. cthor is SECOND-POSITION word (~33% at i=1). cthor→ot bigram 6.18×; cth never precedes cthor (0.00× vs cthol 1.55×). cthor is structurally distinct from cthol. (F149)
**Source:** F148: cthor has LF=39.4% (vs cthol=20.4%) — anomalously LF-present for a cth-word. cthor and cthol are the -or/-ol suffix forms of the same cth-stem. If cthor is a line-opener nominal (different grammatical role from medial cthol), this explains its faster decline in late A-herbal (F147): fewer line-opening constructions in later folios.
**Description:** (1) Compute bigram context for cthor specifically (what precedes cthor at LF vs MID positions?). (2) Compare cthor vs cthol bigram context at line-first, medial, and line-final positions separately. (3) Is cthor's LF usage followed by a specific grammatical pattern (like cthol-medial is followed by d/ch content words)?
**Expected outcome:** cthor at LF is a "topic-introducing" nominal (the subject of the botanical description), while cthol at MID is a "content particle." If cthor predominantly appears at LF followed by d-onset words (the typical A-herbal line structure), it marks a different grammatical role.
**Cost estimate:** small
**Prerequisites:** F148, F147

---

## H282: Are lchedy and cthol Bigram-Context-Equivalent After Dialect Normalization?
**Priority:** medium
**Status:** PARTIALLY CONFIRMED (exp_142) — d-enrichment before cthol=1.51× and before lchedy=1.45× — nearly identical baseline-normalized values. Self-succession: cth before cthol=1.55×, l before lchedy=2.10×. After-contexts differ by dialect vocabulary but similar enrichment magnitudes (~2×). Structural parallel confirmed at d-predecessor level. (F149)
**Source:** F148: lchedy and cthol have nearly identical positional profiles but completely different raw bigram contexts (qok/l before lchedy; d/ch before cthol). The difference in raw context reflects different dialect-level baseline frequencies. If we normalize by baseline onset frequencies in each dialect, do lchedy and cthol have similar RELATIVE bigram contexts?
**Description:** (1) Compute bigram context of cthol (what onsets appear before/after, relative to A-dialect baseline). (2) Compute bigram context of lchedy (what onsets appear before/after, relative to B-dialect baseline). (3) If d-onset before cthol has the same enrichment ratio as qok-onset before lchedy (e.g., both ~1.5× baseline), this confirms positional-grammatical equivalence. If enrichment patterns are different, the positional similarity is coincidental.
**Expected outcome:** After baseline normalization, both lchedy and cthol show similar enrichment patterns for their respective "preceding content word" onsets — confirming that both serve as medial content words following the dominant content words of their respective dialects.
**Cost estimate:** small
**Prerequisites:** F148

---

## H279: Is cthor Botanically Specific to Early A-Herbal Folios? Why Does cthor Decline 2.5× Faster Than cthol?
**Priority:** medium
**Source:** F147: cthor disproportionately declines in A-herbal (T3/T1=0.24 vs cthol T3/T1=0.78). cthor and cthol are parallel nominal forms (-or vs -ol suffix). What explains cthor's extra decline?
**Description:** (1) Which specific A-herbal folios have high cthor vs high cthol? (2) Is cthor concentrated in specific early folios (suggesting botanical specificity)? (3) Are cthor and cthol in complementary distribution (used for different types of botanical content)? Compute per-folio cthor/cthol ratio and Spearman ρ with folio number.
**Expected outcome:** cthor is concentrated in a specific subset of early A-herbal folios (perhaps root/bulb plant descriptions) and cthol in a more even distribution. The cthor decline reflects the specific botanical content of early folios, not a general scribal pattern.
**Cost estimate:** small
**Prerequisites:** F147

---

## H280: Is l-Onset (B-Dialect) the Morphological Parallel to cth-Onset (A-Dialect)? Do lch-Words Have the Same Positional Profile as cth-Words?
**Priority:** high
**Status:** PARTIALLY CONFIRMED (exp_141) — lchedy↔cthol positional equivalence (MID~67-69%, LF~21%, LL~11%). Both LF-depleted and LL-enriched. But bigram contexts completely different (d/ch before cth; qok/l before lch). cthor anomalously LF-present (39.4%). lk-words more medial than lch or cth (74.5%). (F148)
**Source:** F147: l is B-dialect parallel to A's cth (both are productive prefix morphemes on distinct stem classes). lchedy (l+ch+edy) parallels cthol (cth+ol). Both are suppressed in cross-dialect sections. If they are true grammatical parallels, lch-words should have similar positional profiles to cth-words in A.
**Description:** (1) Compute positional distribution (LF/MID/LL) of lch-words (lchedy, lchey, lshedy) in B-dialect sections. (2) Compare to cth-word positional distribution (cthy, cthol, cthey) in A-dialect sections. (3) If lch-words are ~90% MID (like cth-words are ~90% MID in A), this confirms the morphological parallel. (4) Check bigram context: do lch-words appear in similar contexts as cth-words?
**Expected outcome:** lch-words in B-dialect sections are predominantly medial (70-90% MID), mirroring cth-words in A-dialect. This would establish l-prefix as B's functional equivalent to A's cth-prefix, a key structural parallel between the two dialects.
**Cost estimate:** small
**Prerequisites:** F147, F143 (universal core positional data)

---

## H277: Is the A-Herbal cth Smooth Gradient Explained by CONTENT Shift (Which cth-Words Disappear in Late A-Herbal)?
**Priority:** high
**Status:** PARTIALLY CONFIRMED (exp_140) — cth decline is mixed: cthor 0.24× (2.5× faster than overall), cthaiin stable 1.03×, most words proportional ~0.46×. Many "disappearing" T3-absent words are hapax legomena. Not purely proportional, not purely selective. cthor specific decline is most notable deviation. (F147)
**Source:** F146: A-herbal cth decline is smooth (equal-interval −1.1 pp/tertile), consistent with content gradient. cth vocabulary is stable (cthy/cthol/cthey dominate both early and late — F145). But F145 says "fewer cth tokens, not different cth words." Is this literally true? Are the same cth-words present in both periods at different frequencies, or do some cth-words disappear entirely in late A-herbal?
**Description:** Extract all cth-onset words from early A-herbal (f1-f18) vs late A-herbal (f38-f56). Compute: (1) Which cth-words are present in early but absent in late? (2) Which cth-words maintain similar frequency ratios? (3) Does the decline reflect uniform proportional reduction of all cth-words (consistent with a scribe writing the same content less often) or selective disappearance of specific cth-words (consistent with content change)?
**Expected outcome:** If content gradient: specific botanical cth-words (ctholy, cthom — rare forms associated with specific plant types) disappear in late A-herbal while common forms (cthy, cthol, cthey) remain. If scribal drift: all cth-words decline proportionally.
**Cost estimate:** small
**Prerequisites:** F146, F145

---

## H278: What Is the Full l-Onset Vocabulary in B-Dialect Sections (Cosmo, Stars, Pharma)?
**Priority:** medium
**Status:** CONFIRMED (exp_140) — B l-vocabulary: 1120 tokens (stars=725, cosmo=349, herbal-B=40, pharma=6, astro=0) vs A 59 tokens. Top B l-words: lchedy(102,100%B), lkaiin(37,100%B), lkeey(33,97%B), lkeedy(32,97%B). lch- and lk-prefix forms dominate. B-suffix%: 42.3% B-dialect vs 11.9% A-dialect. 376 of 396 B l-types are B-exclusive. loldaiin corrected: A-exclusive (not B-form). (F147)
**Source:** F146: Only 37 l-tokens in all A-herbal. B-dialect sections (cosmo, stars, pharma) presumably have many more l-onset words. Characterizing B-dialect l-vocabulary would provide a reference for evaluating whether late A-herbal l-words are B-like.
**Description:** Extract all l-onset words from B-dialect folios in: cosmo, stars, pharma, herbal-B. Compute: (1) Top l-words by frequency in each B section; (2) suffix paradigm split (A-suffix vs B-suffix); (3) which l-words appear exclusively in B, which are shared with A. This establishes the "B l-vocabulary" profile that can be compared to the 3 clean B-form late A-herbal l-words (lkeedy, lkeey, loldaiin).
**Expected outcome:** B-dialect l-vocabulary is dominated by lk-prefixed forms (lkeedy, lkedy, lkeey — from F131/F134) with -edy/-eedy suffixes. A-dialect l-vocabulary (from early A-herbal) uses lor/lol/lar with -or/-ol/-ar suffixes. This would establish a clean A/B l-dichotomy for comparison.
**Cost estimate:** small
**Prerequisites:** F146, F131, F134

---

## H275: Is the A-Herbal cth Decline a Smooth Gradient or a Specific Breakpoint?
**Priority:** high
**Status:** CONFIRMED (SMOOTH GRADIENT) (exp_139) — A-herbal cth tertile decline is equal-interval: T1=5.96%, T2=4.82%, T3=3.66% (−1.14pp, −1.15pp per step). No discrete breakpoint. Best change-point at f54 is endpoint of continuous trend, not discrete transition. l-gradient (ρ=+0.627) stronger than cth-gradient (ρ=-0.269). (F146)
**Source:** F145: A-herbal-only cth ρ=-0.353 (genuine gradient). Early A-herbal (f1-f28): cth=5.4%; late (f29-f57): cth=3.7%. Is this a smooth monotonic decline or a step-change at a specific folio?
**Description:** Divide A-herbal folios into tertiles (f1-f18, f19-f37, f38-f57). Compute cth rate and l rate for each tertile. If tertile 1→2→3 shows a step-change at one boundary (e.g., f19 or f38) rather than a smooth decline, there may be a scribal hand change at that point. Also compute the within-A-herbal breakpoint using a simple change-point scan (slide a breakpoint across all A-herbal folios, find the folio that maximizes the difference in mean cth rate between before/after groups).
**Expected outcome:** If smooth gradient: evidence for content shift (botanical content changes across the herbal section). If step-change at a specific folio: evidence for scribal hand change (two A-scribes with different cth rates).
**Cost estimate:** small
**Prerequisites:** F145, F144

---

## H276: Does the A-Herbal l-Gradient Reflect B-Vocabulary Contamination in Later A-Herbal Folios?
**Priority:** medium
**Status:** NOT CONFIRMED (INSUFFICIENT DATA) (exp_139) — A-herbal l-words: only 37 total tokens (16 early, 21 late). Clean B-form late l-words: lkeedy(1), lkeey(1), loldaiin(1). Transcription artifacts contaminate 4/6 apparent B-suffix l-words. Sample too small for statistical inference. corpus-wide some late A-herbal l-words (lor=91%B, lo=92%B) are predominantly B-dialect but each appears only once. (F146)
**Source:** F145: A-herbal l-onset gradient (ρ=+0.457): later A-herbal folios (f29-f57) have l=0.8% vs early 0.4%. l-onset words are B-dialect markers (F131, F134). Do later A-herbal l-onset words look like B-vocabulary forms (lkeedy, lkedy, lkeey) or like A-vocabulary l-onset words (lar, lor, lol)?
**Description:** Extract all l-onset words from early A-herbal (f1-f28) vs late A-herbal (f29-f57). Compute: (1) Which l-words appear in early vs late A-herbal? (2) Are late A-herbal l-words predominantly A-dialect l forms (short, with -ol/-or suffixes) or B-dialect l forms (lkeedy/lkedy type, with -edy/-eedy)? (3) Compute dialect purity of late A-herbal l-words using the suffix paradigm split (A-suffix vs B-suffix).
**Expected outcome:** Late A-herbal l-words are dominated by A-dialect l forms (lar/lor/lol) rather than B-vocabulary l forms — the l-gradient is a content shift, not scribal cross-contamination. If B-dialect l forms (lkeedy) dominate in late A-herbal, it would suggest dialect mixing at the A/B boundary.
**Cost estimate:** small
**Prerequisites:** F145, F131, F134

---

## H266: Is -am a SENTENCE-FINAL (paragraph-final) Marker, Not Just a LINE-FINAL Marker?
**Priority:** high
**Status:** NOT CONFIRMED (REVERSED) (exp_136) — -am=0 occurrences at para-final positions (0.00×) across all 260 paragraphs and all sections. -am is SUPPRESSED even within para-final lines (0.33× internal rate). Para-final lines end with "other" (97.6%) — tail-type (=Pt) lines with transcription markers. -am is a within-paragraph line-final marker ONLY. (F143)
**Source:** F142: -am CLOSER is pan-B-section with ~7.8× line-end enrichment in both cosmo and stars. F138: stars -am=8.06×. The -am pattern may be even stronger at paragraph-final lines.
**Description:** Identify paragraph-final lines using locus code changes (new paragraph marker). Compute -am enrichment at paragraph-final lines vs all line-final positions vs non-final positions. Compare cosmo and stars. If -am is ~2× more common at paragraph-final than at regular line-final, it is a sentence/paragraph boundary marker, not just a line closer.
**Expected outcome:** -am is elevated at paragraph-final lines (>10× enrichment vs corpus baseline). This would make -am a discourse-level boundary marker, the strongest structural signal in the manuscript.
**Cost estimate:** small
**Prerequisites:** F142, F138

---

## H267: Does the 71-Word Universal Core Constitute a Closed Functional Vocabulary With Distinctive Positional Distribution?
**Priority:** medium
**Status:** CONFIRMED (exp_136) — Universal core (71 types) = 78.9% medial (vs section-exclusive 60.2%); LL=9.5% (vs exclusive 23.8%). Core contains both openers (saiin=53.5%LF, dain=29.9%LF) and closers (dy=41.9%LL) and medials (chey=95.7%MID). l/p/cth ABSENT from universal core. s/ot/ok overrepresented. After-universal bigram context ≈ baseline. (F143)
**Source:** F142: 71 word types appear in all 5 sections, dominated by d-onset (daiin, dain, dal, dar, dy) and ol/other particles (ol, aiin, ar, or, al). These are likely the manuscript's "function words."
**Description:** Extract the 71 universal words. Compute their: (1) positional distribution (LF/MID/LL) vs section-exclusive words; (2) onset-class composition vs section-exclusive vocabulary; (3) bigram context (what onset classes precede/follow universal words?). If these 71 words are more positionally variable (can appear at any position) but bigram-context-specific, they are function words in the linguistic sense.
**Expected outcome:** Universal words have balanced LF/MID/LL distribution (not position-constrained) unlike section-exclusive vocabulary. They appear in diverse bigram contexts, consistent with grammatical function words.
**Cost estimate:** small
**Prerequisites:** F142

---

## H268: What Is the Positional Distribution of the 31 Cosmo-Absent Words (chor, sho, cthy, cthol, cheo)?
**Priority:** medium
**Status:** CONFIRMED (exp_136) — 55% of 73 high-freq cosmo-absent words are A-dialect dominated (≥70%A). cth=10.90× in cosmo-absent (cthy=96.6%A, cthol=96.1%A). ol/s/l = 0.00× in cosmo-absent (these are cosmo's unique features). Cosmo absence is B-dialect cth suppression mechanism (same as F139). (F143)
**Source:** F142: 31 word types are in all sections except cosmo, including chor(167), sho(89), cthy(87), cthol(51), cheo(33). All are cth/ch-onset words. Are these concentrated in specific folio ranges suggesting scribe-specific vocabulary?
**Description:** Extract chor, sho, cthy, cthol, cheo, and the other 26 cosmo-absent words. For each: (1) compute folio-level frequency distribution; (2) check whether they cluster in A-dialect folios specifically; (3) compare their onset profiles to the ch/cth depletion confirmed for B-cosmo (F139). If chor/sho/cthy all concentrate in A-dialect herbal folios, the cosmo absence reflects dialect-level suppression of the A-nominal class (cth/ch).
**Expected outcome:** chor/sho/cthy/cthol cluster in A-herbal/A-pharma folios. Their absence from cosmo reflects the same B-dialect cth depletion mechanism identified in F139 (B-herbal universally depleted in cth). This would make the cosmo-absent set a near-perfect A-dialect vocabulary marker.
**Cost estimate:** small
**Prerequisites:** F142, F139

---

## H263: Stars-Exclusive ch+eo Vocabulary — Is ch+e+o a Morphological Sub-Class of Stars ch-Onset? What Are cheo/cheody/cheeo's Positional Profiles?
**Priority:** high
**Status:** CONFIRMED REVISED (exp_134) — ch+eo has VOWEL-GRADIENT not stars-exclusivity: ch+o=27% stars, ch+eo=40%, ch+eeo=55%, ch+eeeo=100%. Parallels suffix gradient edy→eedy→eeedy (36%→48%→63%). e-vowel extension = stars-specific marker at multiple structural levels. (F141)
**Source:** F140: Stars-exclusive top words include cheo(38), cheody(33), chody(22), cheeo(18), sheo(17), cho(17) — all ch+[e]+o or sh+eo forms. These appear to be ch-stem + e-vowel-extension + o/ody ending, distinct from ch-stem + -ol/-or/-edy. Are cheo/cheody/cheeo a stars-specific ch-sub-paradigm?
**Description:** Extract all body-text words matching the pattern ch+e*+o (cheo, cheeo, cheody, chody, chos, cheos, sheo, sheody, etc.). Compute: (1) section concentration; (2) positional profile (are these line-openers or line-closers?); (3) relationship to -ol suffix (chol vs cheo: same stem, different suffix pattern?); (4) prefix variation (cheo/cheeo/cheo/cheody — is this a vowel-length gradient similar to edy/eedy?).
**Expected outcome:** cheo/cheody/cheeo are stars-exclusive ch+eo forms concentrated at line-middle or specific positions. They represent a stars-specific suffix-zero or -o/-ody suffix on ch-stem (parallel to how stars uses -eey on other stems). sheo/sheody are parallel sh-stem forms.
**Cost estimate:** small

---

## H260: Astro Section Characterization — Why Is Astro the LEAST Cohesive Section (mean=0.886) and Why Does f87 (Pharma) Best-Match Astro?
**Priority:** medium
**Status:** CONFIRMED (exp_133) — Astro is heterogeneous: f67=true astro (y=2.36×, s=2.15×, other=1.87×, qok=0.33×, particle-heavy); f68/f70=A-herbal-like (sim=0.960/0.968 to herbal centroid, pairwise=0.953); f69=pharma-like. f67 vs f68 sim=0.558 explains low cohesion. f87 matches astro because s=12.35% and qok-depleted. (F140)
**Source:** F138: Astro has mean self-similarity=0.886 (lowest of all sections), n=4 folios. f87 (pharma, A-dialect) best-matches astro (0.885 vs self=0.884). The 4 astro folios (f67, f68, f69, f70 approx) are poorly internally consistent. What makes astro distinctive and low-cohesion?
**Description:** (1) Extract onset-class profiles for each astro folio (f67-f73); (2) compare astro centroid to all other section centroids — which onset classes distinguish astro from herbal/pharma/stars/cosmo? (3) Compute pairwise similarity between astro folios — are they more different from each other than within any other section? (4) Check f87 (pharma) onset profile vs astro centroid — which onset classes make f87 look astro-like?
**Expected outcome:** Astro has a mixed onset profile — perhaps intermediate between A-herbal and B-stars. The 4 astro folios are heterogeneous (different scribe conventions or subject matter). f87 looks astro-like because it shares an unusual onset class distribution (possibly elevated s or d-onset relative to pharma centroid).
**Cost estimate:** small
**Prerequisites:** F138

---

## H269: Is the Para-Final "other=97.6%" a Transcription Artifact? What Vocabulary Do Paragraph Tail Lines (=Pt) Actually Contain?
**Priority:** medium
**Source:** F143: Para-final lines end with "other" suffix at 97.6%. These are likely =Pt (paragraph tail) lines ending with `<$>` or similar transcription markers. Do paragraph-final lines have ANY systematic vocabulary? Are they short or long? Do they differ from mid-paragraph lines in onset or word-length profile?
**Description:** (1) Extract all lines with `=` prefix (paragraph tail type, =Pt); (2) compare their word count, onset profile, suffix profile, and ending tokens vs `+` (continuation) lines; (3) check whether `<$>` line-end markers cluster in para-tail lines; (4) identify what vocabulary actually closes paragraphs when `<$>` is excluded.
**Expected outcome:** =Pt lines are shorter than + continuation lines; their "other" suffix rate is driven by `<$>` or short words. When `<$>` is excluded, para-closing words may show an onset profile (o-onset or d-onset for para-final words per F106).
**Cost estimate:** small
**Prerequisites:** F143, F106

---

## H270: Among the 71 Universal Words, Which Are POSITIONAL CONNECTORS (High LF AND High LL) vs Pure Medials (High MID Only)?
**Priority:** low
**Source:** F143: Universal core = 78.9% medial, but contains both openers (saiin=53.5%LF, dain=29.9%LF) and closers (dy=41.9%LL, dal=26.9%LL). Some words like daiin (22.9%LF + 13.1%LL) appear at both edges.
**Description:** For each of the 71 universal words: classify as (1) CONNECTOR = high LF AND high LL; (2) OPENER = high LF only; (3) CLOSER = high LL only; (4) MEDIAL = low LF and low LL. Compare connector words to openers/closers — do connectors have more section-balanced distribution than edge-specialized words?
**Expected outcome:** A small set (~5-10) of universal words are true connectors (appear at any position). The majority are either openers (y-initial words, saiin) or closers (dy, dal) or pure medials (chey, cheey, aiin). Connectors would represent the most grammatically versatile function words.
**Cost estimate:** trivial
**Prerequisites:** F143

---

## H315: What Is the Full Sentence Context of [daiin@LF][cthor@second] Lines?
**Priority:** high
**Status:** CONFIRMED (exp_158) — 3 lines, all short (n=3-5 words), third word is chol or daiin. [daiin cthor chol chor] appears 2 times as formula. Lines have formula-like structure.
**Source:** F164: daiin@LF → cthor@second appears in 3 cases. Full-line contexts needed to confirm.
**Description:** Extract all 3 [daiin@LF][cthor@second] lines and tabulate third, fourth, fifth words.
**Expected outcome:** Specific formula structure; consistent pattern at third/fourth position.
**Cost estimate:** trivial
**Prerequisites:** F164

---

## H316: Corrected Onset Class Positional Profiles (Grammar Model)
**Priority:** high
**Status:** ESTABLISHED (exp_158) — y=LF 2.46× (strongest opener), d=LL 1.68×, cth=LF 0.15× (never opens lines), ch=second 1.45×, ch_e=second 1.46×. 5-construction grammar model for cth introduction. (F165)
**Source:** exp_155-158 corrected all prior inline slot-swapping bugs.
**Description:** Establish corrected onset class profiles from corrected slot function.
**Expected outcome:** Corrected values for all onset classes.
**Cost estimate:** small
**Prerequisites:** F161, F162, F163, F164

---

## H317: y-Onset Line-Opener Specificity — Which y-Words Drive the LF Enrichment?
**Priority:** high
**Status:** CONFIRMED (exp_159) — ychor=PURE LF-OPENER (13/13=6.24×); ycheor=5.35×; y-words open 40% of all lines in both A and B. B y-onset even more LF-enriched (3.48× vs A=2.46×). (F166)
**Source:** F165: y-onset LF=2.46× (strongest onset-class opener in A). What individual y-words drive this? Are all y-words LF-enriched or only a few?
**Description:** Extract top y-words by frequency and compute their individual LF/LL enrichment profiles.
**Expected outcome:** A few y-words (ychor, ycheor) are extreme LF-enriched; others (ytaiin, yty) are LL-enriched.
**Cost estimate:** small
**Prerequisites:** F165

---

## H318: d-Onset LL Drivers — Which d-Words Are Line-Closers?
**Priority:** high
**Status:** CONFIRMED (exp_159) — d internal split: LL-closers (dam=3.98×, dy=3.02×, daiiin=2.77×, dal=1.95×) vs LF-openers (dchol=3.74×, dchor=3.56×, dor=1.73×). daiin=near-baseline after corpus-artifact correction. (F166)
**Source:** F165: d-onset overall LL=1.68×. Which specific d-words drive LL? Is daiin itself a LL-closer?
**Description:** Compute positional profiles for top d-words (dam, dy, dal, dar, daiin, dchor, dchol).
**Expected outcome:** d has internal split between LL-closers and LF-openers.
**Cost estimate:** small
**Prerequisites:** F165

---

## H319: ot-cth Grammatical Parallelism — Does [cthor@second][ot-word] Appear at Bigram Level?
**Priority:** high
**Status:** CONFIRMED WITH SURPRISE (exp_161) — cthor→ot=5.57× (7/31 cthor bigrams); oty→cth=0.00× (oty never precedes cth); line-level co-occurrence=baseline (0.98×). Bigram-level not line-level relationship. (F168)
**Source:** F165: ot and cth have parallel 4-way positional paradigms. Do they co-occur specifically at bigram level?
**Description:** Compute cthor→ot enrichment; reverse ot→cth enrichment; line-level ot+cth co-occurrence.
**Expected outcome:** cthor followed by ot-word at moderate enrichment; line co-occurrence near-baseline.
**Cost estimate:** small
**Prerequisites:** F165

---

## H320: What Follows ychor@LF and ycheor@LF at Second Position?
**Priority:** high
**Status:** CONFIRMED (exp_160) — ychor@LF → cth@second=3.62×; [ychor][cthy@second]=2 cases. ycheor@LF → ch@second dominates (chor/chol, 2.40×). (F167)
**Source:** F166: ychor and ycheor are pure LF-openers. What is the second-position word?
**Description:** Extract all ychor@LF and ycheor@LF lines; tabulate second-position onset class and specific words.
**Expected outcome:** Specific formula words at second position after ychor/ycheor.
**Cost estimate:** small
**Prerequisites:** F166

---

## H322: Grammar of y-Opened Lines — Second-Position and LL Patterns After y@LF
**Priority:** high
**Status:** CONFIRMED (exp_160) — y-opened lines near-baseline at second (y-self=1.69×). ch depleted at LL (0.59×). ot/y mildly enriched at LL (1.49-1.50×). d@LF→cth@second=1.86× vs y@LF=1.02×. (F167)
**Source:** F166: y-words open 40% of all lines. What is the grammar of these lines?
**Description:** For all y-opened lines (n=254), compute second-position onset class distribution and LL onset class distribution. Compare to baseline.
**Expected outcome:** Some systematic enrichment at second or LL position after y@LF.
**Cost estimate:** small
**Prerequisites:** F166

---

## H352: Can the am_ll Gap (5–7%) Be Closed by Increasing Detection Probability Above 90%?
**Priority:** HIGH
**Status:** RESOLVED by exp_186 (2026-04-11). Hard ceiling confirmed: p_ll=1.00 → am_ll=6.608 (97.0% VMS); 3% gap is structural (CF_rate ≤ 37% means 65.8% of LL words lack clause-final morphemes). No parameter tuning closes the gap — architectural change required. See F181.
**Source:** F180 (exp_185): At cp=0.76, mp=0.9, am_ll=6.460 (94.8% VMS). The remaining 5.2% gap requires an increase in LL -am rate. Currently p_detect=0.90 (90% of clause-final Latin words → -am). What if p_detect=0.95 or 1.00 (100%)?
**Description:** Re-run exp_185 at cp=0.76, mp=0.9 with p_detect ∈ {0.90, 0.95, 1.00} for the LL cipher table. Hypothesis: at p_detect=1.00 (ALL clause-final words → -am), am_ll would increase to approximately 5.86/0.90 × 1.00 ≈ 6.51× (all of the 0.90-factor gain applied). But the gain is sublinear because am_ll enrichment is ratio-based (LL rate / corpus rate). Expected: p_detect=1.00 → am_ll ≈ 6.6-6.8 (95-100% VMS). If yes: the am_ll gap is closable by pushing detection probability to maximum — meaning ANY sufficiently formulaic LL morpheme mapping to -am could close the gap. If no: the gap requires a source text with genuinely higher clause-final density.
**Cost estimate:** tiny (3 parameter variations, 50 sims each = 150 runs)
**Prerequisites:** exp_185 (done)


---

## H350: Targeted cp=0.74–0.76 Grid to Localize VMS ss_mean Crossover in Timm Char Modification
**Priority:** HIGH
**Status:** RESOLVED by exp_185 (2026-04-11). Crossover confirmed at cp≈0.745–0.750 (mp=0.8), consistent with prediction. Best combination: cp=0.76, mp=0.9 → ss=1.454 (99.2% VMS), am_ll=6.460 (94.8%), adj=0.00425. See F180.
**Source:** F178 (exp_183): The VMS ss_mean crossover (cp=0.7 underproduces at 94%, cp=0.8 overproduces at 107%) implies optimal cp≈0.745. This is interpolated; direct measurement required.
**Description:** Run position-aware hybrid with Timm char modification at cp ∈ {0.70, 0.72, 0.74, 0.76, 0.78, 0.80} × mp ∈ {0.7, 0.8, 0.9} (18 combinations × 50 sims). Goal: find the cp value that produces ss_mean closest to VMS target (1.465) while maintaining adj_rate ≤ 0.009 and am_ll ≥ 5.0. Expected: ss_mean = 1.465 at cp≈0.745. Secondary question: does the fine-grained cp sweep show the am_ll also increasing linearly with cp (from 6.30 at cp=0.7 to 6.50 at cp=0.8)? If so, optimal cp ≈ 0.745 produces am_ll ≈ 6.40 (93.9% VMS), establishing the final residual gap in a single well-controlled measurement.
**Expected outcome:** One or two (cp, mp) combinations with ss_mean ∈ [1.42, 1.50] (within 3% of VMS) at adj_rate ≤ 0.009. If the gap in am_ll (≈6.4%) persists at optimal cp, this establishes the architecture's ceiling.
**Cost estimate:** small (18 × 50 = 900 simulations, <5 min)
**Prerequisites:** exp_183 (done)

---


---

## H351: Italian Source Text in Position-Sensitive Cipher — Does Higher Morphological Density Close am_ll Gap?
**Priority:** medium
**Status:** RESOLVED NEGATIVE by exp_187 (2026-04-11). Italian (Dante) produces am_ll=3.46–3.76× (51–55% VMS) — far below Latin's 6.42× (94.3% VMS). Italian analytic morphology has CF_rate only 5.5–6.8% (vs Latin 34–37%). Italian does NOT close the am_ll gap; it makes it worse. am_ll metric discriminates: consistent with Latin, inconsistent with Italian. See F182.
**Source:** F179 (exp_184): Latin sources (Cicero/Virgil/Caesar) all cluster at CF_rate 34-37%, producing am_ll 84-86% of VMS. Italian (a romance language with different clause-final patterns) and medieval Latin formulaic texts are untested. Closing the full gap would require CF_rate ≈ 60%, so Italian is unlikely to close it entirely — but the test would establish the Italian baseline and identify whether Italian morphology changes the mechanism at all.
**Description:** Run exp_177 architecture with Italian text from data/reference_corpora/italian/ at strong calibration (p=0.90). Measure am_ll, y_lf, ss_mean, adj_rate. Italian clause-final patterns differ from Latin (synthetic inflection → analytic, fewer -um/-us/-ae endings, but -à/-ò/-i may trigger different cipher patterns). The clause-final detection regex in exp_177 is Latin-specific — would need to be updated for Italian (Italian sentence-final verbs: -ò, -à, -ono; noun endings: -a, -e, -i, -o). Secondary: download actual Latin Vulgate text (not the Douay-Rheims English) if available.
**Expected outcome:** Italian am_ll either similar to Latin (CF detection regex fires less often → lower am_ll than Cicero) or different if Italian clause-final morphemes are more frequent. The key question is whether any Romance language source produces am_ll significantly above 5.85×.
**Cost estimate:** small-medium (requires adapting cipher tables for Italian morphology)
**Prerequisites:** exp_184 (done)

---


---

## H078: Bio Section Has Multiple Paragraphs Per Folio Because Pool Folios Have Multiple "Scenes"
**Priority:** medium
**Status:** RESOLVED by exp_194 (2026-04-11). SUPPORTED — multi-para folios (7) have shorter paragraphs (15.1 vs 38.7 lines); vocabulary Jaccard 0.004-0.156 between paragraphs (near-independent); each paragraph = independent scene. See F194.
**Source:** F068 (exp_061): Bio multi-para folios are f83r (4 PS), f84v (4 PS), f75v (3 PS), f75r, f82r, f83v, f84r — mostly pool/bathing folios. Do multi-paragraph bio folios have more words/lines per paragraph (longer scenes) or more paragraphs (more scenes)?
**Description:** In the bio section, some folios have 1 paragraph (single-scene bio illustrations) and some have 2-4 paragraphs (pool folios with multiple bathing scenes). Test: (a) Do multi-paragraph bio folios have the same word-per-paragraph count as single-paragraph bio folios, or longer paragraphs? (b) Are the paragraph texts in multi-para bio folios independent vocabulary (each scene described separately) or do they repeat the same words? (c) Does the text within each bio-folio paragraph use the same vocabulary as other bio paragraphs on the same folio?
**Expected outcome:** If each paragraph = independent scene description: different vocabulary per paragraph on the same folio.
**Cost estimate:** small
**Prerequisites:** exp_061 (done)

---


---

## H101: The Line-Final Onset Distribution Is Preserved Within Paragraphs vs Paragraph-Final Lines
**Priority:** medium
**Status:** RESOLVED by exp_194 (2026-04-11). SUPPORTED — A: para-final enriched ok(1.47×)/o(1.66×)/ot(1.31×); d-onset NEUTRAL (0.98×); p perfectly excluded (0.00×). B: ok(2.51×)/sh(2.69×)/ch(1.70×) enriched; d depleted (0.42×); p excluded (0.00×). See F194.
**Source:** F081 (exp_074): B last-word onsets are non-random (o=1.25×, d=1.50×, qo=0.61×, sh=0.42×). F064 (exp_057): para-start words have a distinct onset class. Is there a difference between line-final words on para-INTERIOR lines vs the line-FINAL of a paragraph?
**Description:** For B body text, classify lines as: (1) within-paragraph continuation lines, (2) last line of a paragraph. For each group, compute last-word onset distribution and enrichment. If the para-final last word has a different onset class than within-para last words, this would show paragraph-level boundary marking at the last word.
**Expected outcome:** If boundary marking: para-final last words have different onset distribution than mid-para last words (e.g., para-final avoids qo, prefers o or d). If no distinction: the line-final grammar is purely line-level, not paragraph-level.
**Cost estimate:** small
**Prerequisites:** exp_074 (done)

---


---

## H126: The B Paragraph Tripartite Structure (p-onset START → -am LINE-ENDs → o-onset PARA-END) Can Be Used to Parse Paragraph Structure Automatically
**Priority:** medium
**Status:** RESOLVED by exp_194 (2026-04-11). NOT SUPPORTED — PS PARA-tier=70.4% (strong), within-para -am=13.9% (moderate), but para-final o-onset (bare)=5.1% (weak); all 3 signals = only 2/98 paras; para-close is specific words not onset class. See F194.
**Source:** F087 (exp_080): B shows a tripartite positional grammar: p-onset marks para-starts; -am suffix marks within-para line-ends; o-onset marks para-ends. If this structure is consistent, it should be possible to use these markers to PREDICT where paragraph boundaries are — i.e., to parse paragraph structure from word features alone (without the locus codes). How accurately does the tripartite grammar predict the observed locus-code paragraph structure?
**Description:** (1) For each B line, compute: is the first word p-onset? is the last word -am? is the last word o-onset? (2) Train a simple classifier: predict is_para_start from previous-line's last word features (is it o-onset? is it -am?). (3) Evaluate precision/recall of -am words for identifying within-para line-ends vs para-final line-ends. (4) How often does the tripartite grammar break down (p-onset mid-paragraph, o-onset within-para, -am at para-end)?
**Expected outcome:** If parseable: -am predicts within-para line-end with high precision (>70%); o-onset last word predicts para-final with >50% precision; p-onset first word predicts para-start with >60% precision. If inconsistent: the grammar is more approximate than suggested.
**Cost estimate:** small
**Prerequisites:** exp_080 (done)

---


---

## H127: The d-Onset Words (dam, chdam) Forming Line-Closers in Both Dialects Are a Cross-Dialect Function Word Subclass
**Priority:** medium
**Status:** RESOLVED by exp_195 (2026-04-11). SUPPORTED — dam exclusively LL/MID in BOTH dialects (LF=0% in A and B). A=64.1% LL, B=79.2% LL. General d-onset shows dialect reversal (A LL-biased, B LF-biased) but dam resists this shift. dam is the clearest cross-dialect positional anchor. See F195.
**Source:** F086/F087 (exp_079/exp_080): dam is the only word appearing as a line-closer in BOTH A (62.5%) and B (77.4%). chdam is a B line-closer (60%). Both end in -am. Are there other d-onset words that bridge A and B in their positional behavior? d-onset is enriched at line-finals in BOTH dialects (A: d→1.73×, B: d→1.51×) — a cross-dialect positional grammar feature. Is d-onset the "cross-dialect bridge" onset class, appearing at line-finals in both systems?
**Description:** (1) Compute d-onset line-final rate for ALL d-onset words in both A and B. (2) Are there d-onset words that appear in both dialects with similar positional behavior? (3) Compare: dam in A vs B (line-final rate, what precedes it, what follows). (4) Does dam in A have the same positional role as dam in B, or are they the same orthographic form serving different grammatical functions?
**Expected outcome:** If cross-dialect bridge: d-onset words (especially dam and chdam) have similar line-final rates in both dialects, suggesting d-onset grammatical words are dialect-stable (unlike the sh→qo vs d→qo opposition). If dialect-specific: dam in A and dam in B have different distributional profiles despite the same form.
**Cost estimate:** small
**Prerequisites:** exp_080 (done)

---


---

## H131: The Two Herbal A Registers (Aiin-Dom vs Y-Dom) Are Written by Different Scribes or Represent Different Sections of the Herbal Content
**Priority:** medium
**Status:** PARTIALLY RESOLVED by exp_198 (2026-04-11). NOT SUPPORTED computationally — no f16/f17 folio boundary; f17+ has slightly higher daiin than f1-f16. Codicological question (quire/scribe) still requires manuscript access. See F198.
**Source:** F088 (exp_081): Aiin-dom and y-dom Herbal A show: (1) different suffix paradigms (-ol/-or vs -ey/-eey); (2) opposite she-→qo coupling; (3) different bigram grammar strength; (4) different e-infix word rates. These differences are as large as the A vs B dialect difference for some features. The AIIN_DOM_FOLIOS set (f1r-f16v) may correspond to a specific quire or scribe section in the physical manuscript.
**Description:** (1) Map the aiin-dom and y-dom folios to their physical quires in the manuscript. Do they fall into distinct quires? (2) Do the aiin-dom folios have different illustration styles (herbal A plant drawings vs y-dom plant drawings)? (3) Is the aiin-dom/y-dom split purely folio-based or does it appear within single folios? (4) Is the AIIN_DOM_FOLIOS set (f1r-f16v, 24 folios) physically contiguous in the manuscript?
**Expected outcome:** If scribe split: aiin-dom folios are all from one or two quires (suggesting different hands). If section split: aiin-dom represents a specific content subsection of Herbal A with different language register.
**Cost estimate:** small (reference-based)
**Prerequisites:** exp_081 (done)

---


---

## H147: The she- Lexical Class Has a Consistent Semantic Register — she-Words Appear With Specific Content Words That Suggest a Grammatical Function (Aspect/Topic Marker)
**Priority:** medium
**Status:** RESOLVED by exp_195 (2026-04-11). SUPPORTED — she-successor onsets in A: qo=3.33×, t=2.51×, qok=2.18× enriched; ch=0.49×, d=0.57× depleted. Top specific successors: qodar(17.1×), qokor(9.5×). PS enrichment 2.38×. she-words license qo-complex and gallows successors while avoiding ch/d. See F195.
**Source:** F091/F092 (exp_084/085): she-prefix is 4.74× enriched at para-starts, AND predicts qo-following (27.5% she-→qo vs 11.4% base). The she- function appears to be inherent to she-lexemes (not context-driven). What follows she-words? Do specific content words co-occur with she-words more than expected?
**Description:** (1) For each A record containing she-prefix words: what are the most over-represented following-words? (2) Is there a recurring {she-word} → {X} pattern where X is a specific content or function word? (3) Do she-words appear in specific topic/content contexts (e.g., only in Herbal sections, not Pharma)? (4) Compare she-para-start lines vs she-non-para-start lines: do they have different following-word profiles?
**Expected outcome:** If she- is a grammatical marker: the following-word distribution after she-words would be drawn from a restricted class (qo-onset words plus a few other common words). The co-occurrence pattern may reveal what grammatical role she- encodes.
**Cost estimate:** small
**Prerequisites:** F091/F092 (exp_084/085)

---


---

## H161: The A Line-Initial y+ch System and the A Line-Initial d+ch System Have Different Preceding/Following Contexts — They Are Not Interchangeable
**Priority:** medium
**Status:** RESOLVED by exp_196 (2026-04-11). SUPPORTED — both excluded from PS (0%); within-para: y+ch→next-line o(2.52×)/ok(2.04×); d+ch→next-line sh(1.77×), avoids ok(0.22×)/d(0.36×). Functionally distinct. See F196.
**Source:** F098 (exp_091): A has both y+ch (85.9% LFirst) and d+ch (59.6% LFirst) as line-initial prefix systems. But y+ch has HIGHER LFirst% than d+ch. Are they truly synonymous openers? Or do they appear in different contexts (e.g., y+ch at para-starts, d+ch at within-para line-starts)?
**Description:** (1) Compare y+ch vs d+ch: do they appear at para-start lines at different rates? (2) What FOLLOWS y+ch at pos1 vs what follows d+ch at pos1? (3) Are y+ch and d+ch in complementary distribution within paragraphs (e.g., y+ch opens first line, d+ch opens subsequent lines)? (4) Do y+ch words appear only in specific folio sections while d+ch appears in others?
**Expected outcome:** If distinct functions: y+ch opens para-start lines while d+ch opens within-para lines — the difference in LFirst% (85.9% vs 59.6%) reflects different para-level positions. If synonymous: both appear at similar para-position rates.
**Cost estimate:** small
**Prerequisites:** F098 (exp_091)

---


---

## H162: The Cross-Dialect Positional Grammar Paradigm Has a Universal Structure — Position-Encoding Prefix System Is Voynichese-Level, Not Dialect-Specific
**Priority:** high
**Status:** RESOLVED by exp_088-096 (2026-04-09). CONFIRMED — F103: PREFIX TYPE determines positional role cross-dialectally; p+ch=Para in A(27%) and B(12%); y/d+ch=Line-Opener in both (0% PS); the positional morpheme is the prefix. Universal three-position line grammar confirmed. See F095-F103.
**Source:** F095-F098 (exp_088-091): Both A and B implement: [PREFIXED LINE-OPENER] → [MID-LINE CONTENT] → [LINE-CLOSER]. B: y+k/t opener; qo+k/t mid; -am/oly closer. A: y+ch or d+ch opener; bare ch mid; d+suffix closer. The prefix-encoded positional paradigm is present in BOTH dialects. Hypothesis: this is a universal Voynichese grammatical property, not dialect-specific.
**Description:** (1) Test if the A positional paradigm extends to other stem classes (not just ch): do y+sh, d+sh compounds exist in A and show similar LFirst enrichment? (2) Do the A d+ch openers appear on the same lines as the B y+k/t openers in mixed-dialect sections? (3) Is there a universal line-grammar rule that applies across all Voynichese text?
**Expected outcome:** If universal: the same three-position line grammar should appear in all sections regardless of dialect assignment. This would be the strongest possible evidence for Voynichese as a rule-governed linguistic system.
**Cost estimate:** medium
**Prerequisites:** F095-F098 (exp_088-091)

---


---

## H164: A Para-Start p-Onset Words Are a Specific Closed Class — Identify Them and Their PSFirst Enrichment
**Priority:** high
**Status:** RESOLVED by exp_093 (2026-04-09). CONFIRMED — p-onset A para-starters: po- (22.17×), pc- (7.39×); F100: p/k/t are universal gallows para-starters; F101: MASTER — prefix-demoted gallows hierarchy. See F099-F101.
**Source:** F099 (exp_092): p-onset words dominate A para-starts at 12.41× enrichment (28.8% of PS openers). This is the STRONGEST para-start signal found in A (stronger than she-prefix at 4.74×). Need to identify which specific p-onset words are the para-starters.
**Description:** (1) List all p-onset words in A by frequency. (2) Compute PSFirst%, LFirst%, LLast% for each p-onset word with n≥3. (3) Are para-start p-onset words a specific closed class (like she-prefix, olfchedy)? (4) Are they concentrated in specific sections (astro, herbal, pharma)? (5) What FOLLOWS the p-onset para-starters at pos1?
**Expected outcome:** A small number of specific p-onset words (like "pchedy", "pchor", "pcho") will have very high PSFirst% (>50%) — they are the A paragraph markers analogous to B's olfchedy/olkey/opchedy (61.5% precision). This would complete the A para-start grammar.
**Cost estimate:** small
**Prerequisites:** F099 (exp_092)

---


---

## H165: d-Chain Pattern in A — d-Closer → d+ch Opener Sequence Is Systematically Above Chance
**Priority:** medium
**Status:** RESOLVED by exp_194 (2026-04-11). PARTIALLY SUPPORTED — d-final → d+ch opener: 1.47×; y+ch after d-final depleted (0.67×); 75 runs of 3-5 consecutive d-final lines. No o-chain. See F194.
**Source:** F099 (exp_092): When a line ends with a d-onset word (d-closer), the NEXT line opens with d+ch at 35.7% vs y+ch at 16.2% (ratio 2.20×). This suggests a d-chain continuity pattern: d-onset LINE-CLOSER triggers a d-onset LINE-OPENER on the following line. Test if this is statistically significant and if it creates multi-line d-chain runs.
**Description:** (1) Measure: P(d+ch opener | prev d-closer) vs P(d+ch opener | prev non-d-closer). (2) Is the 35.7% rate significantly above expected? (3) Do d-chains (d-closer → d+ch → d-closer → d+ch → ...) extend for 3+ lines? (4) Is there a complementary o-chain (o-ending → y+ch opener → o-ending)?
**Expected outcome:** d-chains appear at significantly above chance. This would establish a INTER-LINE CONTINUITY GRAMMAR: d-onset words create runs across consecutive lines.
**Cost estimate:** small
**Prerequisites:** F099 (exp_092)

---


---

## H167: k-Onset A Para-Start Words — Identify the Specific k-Onset Para-Start Vocabulary
**Priority:** high
**Status:** RESOLVED by exp_093-099 (2026-04-09). CONFIRMED — ko- (8.77× A, 38.12× B), k-onset A=4.32×; k is part of gallows para-start class; F101 MASTER finding establishes all four gallows (p/k/t/f). See F100-F101.
**Source:** F100 (exp_093): k-onset words are para-start enriched in A (4.32×) and VERY strongly in B (9.91×!). k-onset is the SECOND strongest gallows-initial para-start class. Need to identify which specific k-onset words (kol, kor, kaiin, kedy, etc.) drive the para-start enrichment.
**Description:** (1) List all k-onset A words by frequency. (2) Compute PSFirst% for k-onset A words with n≥3. (3) Compare: are k-onset A PS words the same structural forms as p-onset A PS words? (4) Check B k-onset PS words (9.91× — even stronger than p-onset!) — what specific B k-onset words open paragraphs? (5) Is there a "gallows-initial" closed class for k/p/t/f that marks discourse-level positions?
**Expected outcome:** A specific subset of k-onset words (like kol, kor — the same stems as ch-stems but with k-initial gallows) will show high PSFirst%. The gallows character (k gallows ≡ t/p gallows) systematically marks para-starts.
**Cost estimate:** small
**Prerequisites:** F100 (exp_093)

---


---

## H168: The Four-Level Positional Grammar Is Encode in the Gallows Character System — p/k = Para-Level; Non-Gallows = Line-Level
**Priority:** high
**Status:** RESOLVED by exp_094 (2026-04-09). CONFIRMED — F101 MASTER: all four gallows (p/k/t/f) are para-level; f-onset para-enriched; qok/qot suppressed at PS (0.54×/0.17×); y+k/t compounds are B line-openers. See F101.
**Source:** F100 (exp_093): p/k/t-onset (gallows characters) = para-starters; y/d/qo (non-gallows) = line-level. In EVA, k and t are the "regular gallows"; p and f are the "platform gallows". All four gallows characters should show para-start enrichment.
**Description:** (1) Check f-onset words — do f-onset words also show para-start enrichment? (2) Within gallows class: is p-gallows enrichment > k-gallows > t-gallows > f-gallows? (3) Are qo-prefix + gallows words (qok, qot) showing para-start SUPPRESSION? (4) Does the y-initial line-opener system ever use gallows stems (y+k, y+t)? This would explain y+k/t compounds in B as a way to "recruit" gallows stems into the WITHIN-LINE position.
**Expected outcome:** f-onset words are also para-start enriched. The four gallows characters (p/k/t/f) collectively mark paragraph-level positions; prefixes (y/d/q) recruit the same gallows stems for within-line positions.
**Cost estimate:** small
**Prerequisites:** F100 (exp_093)

---


---

## H171: Is the Gallows Hierarchy Consistent for ALL Gallows Characters Individually? (bare_p > bare_t > bare_k?)
**Priority:** medium
**Status:** RESOLVED by exp_196 (2026-04-11). PARTIALLY SUPPORTED — bare gallows NEVER at PS (all 0%); hierarchy exists only for +ch compounds: p+ch>t+ch>k+ch>f+ch. f+ch is weakest (not second to p). B amplifies p+ch. See F196.
**Source:** F101 (exp_094): bare_p is strongest (A=40.2% PS, B=10.7%); bare_t next (A=10.2%, B=3.9%); bare_k weakest (A=5.7%, B=3.0%). Is there a consistent internal hierarchy within the gallows class: p > f > t > k? And is this hierarchy consistent across sections?
**Description:** (1) Section-specific analysis: does herbal A show same gallows hierarchy as pharma A? (2) Does bare_t appear at para-starts more than bare_k in all sections? (3) What is the functional difference between bare_k and qo+k — if they have same LFirst% (~10%) but different PS rates (3% vs 0.1%), they may differ in discourse function but not line position. (4) Is p > f > t > k a consistent hierarchy across sections and dialects?
**Cost estimate:** small
**Prerequisites:** F101 (exp_094)

---


---

## H172: The Prefix-Demoted Gallows Grammar Applies to A's ch-Stems Analogously — p+ch = Para-Starter, y+ch/d+ch = Line-Opener, bare ch = Mid-Line
**Priority:** high
**Status:** RESOLVED by exp_095 (2026-04-09). CONFIRMED — F102: p+ch=26.9% PS (para-starter); platform gallows (p,f) > regular (t,k) for para-start; universal across ch AND sh stems; A p+sh also para-enriched. See F102.  
**Source:** F101 (exp_094): A's ch-stem system: bare_ch(7.1% LFirst) < d+ch(59.6%)/y+ch(85.9%) line-openers < p+ch(para-starters). This is exactly the gallows-demotion hierarchy! p+ch would be the "recruited gallows for ch-stem para-start". Test: (1) p+ch words in A — what are their PSFirst% rates? (2) If p+ch = para-starters and d+ch/y+ch = line-openers, this extends the gallows-demotion model to ch-stems in A. (3) Does A have p+sh, p+s, p+d forms as para-starters for sh-stems?
**Expected outcome:** p+ch words have high PSFirst% (para-starters), extending the gallows-demotion model to A's ch-stem paradigm. This would unify A's positional grammar with B's under a single framework: para-starters use gallows-initial prefix; line-openers use y/d-prefix; mid-line = bare.
**Cost estimate:** small
**Prerequisites:** F101 (exp_094)

---


---

## H175: Does the B Dialect Show the Same Gallows+Stem Para-Start Hierarchy? (pch/fch/tch in B)
**Priority:** high
**Status:** RESOLVED by exp_096 (2026-04-09). CONFIRMED — F103: p+ch para-start in B=12%; y/d+ch = line-openers in B (0% PS); prefix determines position cross-dialectally. f+ch exception in B (0% PS vs A 21%) documented. See F103.
**Source:** F102 (exp_095): In A, p+ch and f+ch are para-starters, y+ch/d+ch are line-openers. In B, the ch-stem system is used differently (ch is mid-line in B; B uses k/t stems not ch). But B also has gallows words at para-starts. Does B show p+ch = para-starter? Or p+t/p+k? Test the B-equivalent of the A gallows+stem hierarchy.
**Expected outcome:** In B, p+ch should also show elevated PS rate; but B's primary para-starters may be p+t or p+k (gallows+gallows compounds). The B answer will tell us if the A gallows-demotion model is universal.
**Cost estimate:** small
**Prerequisites:** F102 (exp_095)

---


---

## H176: The k-onset Words in A Are a DIFFERENT Positional Class Than k-onset in B — A's k-onset Is Line-Distributed; B's k-onset Is More Para-Concentrated
**Priority:** medium
**Status:** RESOLVED by exp_196 (2026-04-11). SUPPORTED — A k-onset: PS-enriched 4.32× (within-para 2.84%); B k-onset: PS-enriched 9.91× (within-para 1.30%). B k-onset more strictly confined to PS. See F196.
**Source:** F101-F102: In A, k+ch=3.5% PS (very weak); bare_k=5.7% PS (weak). In B, bare_k=3.0% PS but total B k-onset=9.91× — the B k enrichment is driven by k at line-first generally, not just para-starts. Test: is B k-onset concentrated at ANY line-first position (not just para-starts) more than A k-onset?
**Cost estimate:** small
**Prerequisites:** F101, F102

---


---

## H178: The Prefix Determines Position; Does the STEM AFFECT MEANING (Content vs Function Words)?
**Priority:** high
**Status:** RESOLVED by exp_097 (2026-04-09). CONFIRMED — F104: core ch-stems (chor/chol/chey) appear across ALL prefix classes; 87.8% stem exclusivity is frequency artifact; consistent with productive positional morphology. See F104.
**Source:** F103 (exp_096): Prefix determines position; stem determines content. But are some stems FUNCTION words (abstract) while others are CONTENT words (concrete)? Test: (1) Do para-start p+ch words use the SAME ch-stems as within-para y+ch and d+ch? (2) Are there "exclusive" stems that only appear with one prefix type? (3) If stem = content and prefix = position, then the same stem should appear with p-, y-, d-, and bare forms depending on context. Test this.
**Expected outcome:** The same ch-stems (chor, chol, chey) appear with all three prefixes (p+ch, y+ch, d+ch) — the stem is semantically stable and the prefix shifts position. If TRUE: Voynichese is a positional morphology system. If FALSE (stems are prefix-exclusive): the stem+prefix combination = lexical item with no stem reuse.
**Cost estimate:** small
**Prerequisites:** F103 (exp_096)

---


---

## H179: f+ch Cross-Dialect Asymmetry — Why Is f+ch Para-Level in A (21% PS) But Mid-Line in B (0% PS)?
**Priority:** medium
**Status:** RESOLVED by exp_196 (2026-04-11). SUPPORTED — A f+ch: herbal-dominant(83%), LF=44.4%, PS=2.45%; B f+ch: stars-dominant(57%), MID=75.7%, PS=0.99%; B uses fchedy with -edy suffix = MID vocabulary. See F196.
**Source:** F103 (exp_096): f+ch appears at para-starts 21.4% in A but 0% in B (n=34). This is the one major exception to the unified grammar model. Test: (1) In B, where do f+ch words appear? Are they truly mid-line? (2) Is the B f+ch distribution section-specific (only in specific B folios)? (3) Could the n=34 sample in B be too small? (4) Does B use other gallows+ch forms for para-starts instead of f+ch?
**Expected outcome:** The B f+ch distribution may be section-specific or folio-specific. Alternatively, B uses different gallows (k+sh=9% in B, which is stronger than k+sh in A) to compensate for f+ch's mid-line role. The exception may be real: A uses both p and f as para-starters; B uses primarily p (and less f).
**Cost estimate:** small
**Prerequisites:** F103 (exp_096)

---


---

## H181: Voynichese Positional Grammar Completeness Test — Can We Predict Line Position From Prefix With >80% Accuracy?
**Priority:** high
**Status:** RESOLVED by exp_098-101 (2026-04-09). CONFIRMED — F105-F108: LINE_OPEN categorically excluded from PS; v2 classifier 54% PS coverage (6.6×/3.5×); para length predicts grammar strictness; herbal A (10-15 line) = strictest (70.7% PARA, 0% LINE_OPEN). See F105-F108.
**Source:** F101-F104 (exp_093-097): We now have a complete positional grammar model: {p,f}+stem=para; {y,d}+stem=line-opener; {qo}+gallows=mid-line; bare_ch=mid-line. Test: given a word's morphological form (prefix + stem class), can we predict whether it's at (1) para-start, (2) within-para line-first, (3) mid-line, or (4) line-last with >80% accuracy?
**Description:** (1) Build a classifier: word → predict positional tier. (2) Use prefix type and stem class as features. (3) Compute confusion matrix: how often does the predicted tier match the actual position? (4) What are the most common misclassifications? (5) Does accuracy differ by section or dialect?
**Expected outcome:** High accuracy (>70%) for classifying words into positional tiers based on morphology alone. This would confirm the MORPHOLOGY-TO-POSITION MAPPING is the dominant grammatical rule in Voynichese. Misclassifications would identify edge cases.
**Cost estimate:** medium
**Prerequisites:** F101-F104 (exp_093-097)

---


---

## H182: Do Voynichese Paragraphs Have Consistent Internal Structure? (Para-Level Template Test)
**Priority:** high
**Status:** RESOLVED by exp_098 (2026-04-09). CONFIRMED — F105: LINE_OPEN tier categorically excluded from PS; sharp para-boundary transition; para-length section-determined; grammar step-function (F117: lines 1-2 grammar-strong, lines 3+ near-zero PARA). See F105, F117.
**Source:** F100-F104: We know individual words have strong positional grammar. But do paragraphs have consistent internal structure? Test: (1) What is the typical A/B paragraph length (in lines)? (2) Is there a consistent pattern within paragraphs: gallows-word first line, then multiple y/d+ch openers, then final d-onset closer? (3) Is the "paragraph" a coherent unit with observable internal structure?
**Description:** (1) Compute paragraph lengths (number of lines per paragraph) for A and B. (2) For each paragraph, track the sequence of line-opener types: para-start line (gallows opener), then line 2 (y/d+ch?), line 3... (3) Is there a modal paragraph template? (4) Do para-start gallows words always appear at line 1, or also mid-paragraph?
**Expected outcome:** Paragraphs have consistent structure with gallows word at line 1, followed by y/d+ch-type openers for internal lines, and possibly d+ch or d-onset words at para-final line. This would complete the multi-level grammar characterization.
**Cost estimate:** medium
**Prerequisites:** F100-F104

---


---

## H184: What Are the "OTHER" Para-Start Words? — Coverage Gap Investigation
**Priority:** high
**Status:** RESOLVED by exp_099 (2026-04-09). CONFIRMED — bare k (9.12×/11.92×) and bare t (3.25×/1.77×) dominate OTHER PS; o-onset/d-onset/s-onset SUPPRESSED at PS. PARA tier must be extended to {p,f,k,t}+anything. See F106.
**Source:** F105 (exp_098): ~54% of para-starts begin with "OTHER" words not captured by the PARA/LINE_OPEN/MID/WEAK_PARA classifier. This is the largest single category at para-starts. What onset classes do these words use? Are they: (1) o-onset words, (2) words beginning with specific vowel-onset patterns, (3) word-forms with specific suffixes, (4) section-specific vocabulary?
**Description:** Extract all para-start words classified as "OTHER" in A and B. Compute onset distribution (o, a, e, s, c, etc.). Compare to within-para OTHER words. Identify if specific word forms are para-start-enriched within the OTHER category.
**Expected outcome:** Likely find that o-onset words (like ol, or, or similar) are para-start enriched. These would be a FOURTH positional class beyond the gallows system — an "o-prefix para-start" class to complement p/k/t/f para-starters.
**Cost estimate:** small
**Prerequisites:** F105 (exp_098)

---


---

## H185: Para-Final o-Onset Specialization — Is o-Ending a Paragraph Closer Morpheme?
**Priority:** medium
**Status:** RESOLVED by exp_099 (2026-04-09). PARTIALLY CONFIRMED — o-onset mildly enriched at para-final (A=1.52×, B=1.25×); B sh-onset (2.88×) stronger; specific words okeey=16.4×, orol=21.9×, shedy=6.25× are para-final specialists; p-onset perfectly excluded (0.00×). See F106.
**Source:** F105 (exp_098): Para-final last words are 27.4% (A) / 35.3% (B) o-onset. Is this para-specialized or just a property of line-final words in general? Compare o-onset line-last rate at para-final lines vs within-para line-last positions.
**Description:** Test if o-onset words are SPECIFICALLY enriched at para-final positions vs within-para line-last positions. If para-final o-onset > within-para line-last o-onset, then o-onset is a paragraph-closer signal.
**Expected outcome:** o-onset words are somewhat enriched at para-final line-last positions but not dramatically so — the 27-35% rate may simply reflect the general distribution of line-final words ending in o-onset forms.
**Cost estimate:** small
**Prerequisites:** F105 (exp_098)

---


---

## H186: Stars (B) Paragraph Internal Structure — Are 47-Line Paragraphs Internally Structured Into Sub-Sections?
**Priority:** medium
**Status:** RESOLVED by exp_194 (2026-04-11). SUPPORTED — all 23 stars paras have PARA-tier words at non-PS positions (13-43% rate at lines 3+, vs ~0% in herbal A); mean 2.5 lines between PARA-tier words; no regular N-line cycle; no astronomical number match. See F194.
**Source:** F105/H183: Stars (B) paragraphs have mean 47 lines (range 37-54). These are massive structural units. Do they have sub-structure? Test: (1) Within-stars paragraphs, do PARA-tier markers appear mid-paragraph (creating internal "sub-paragraphs")? (2) Is there a repeating N-line cycle within stars paragraphs? (3) Do the ~47-line stars paragraphs correspond to known astronomical sub-structures (12 zodiac signs × 4 lines? 36 decans?)?
**Description:** Extract stars-section B paragraphs. Look at line position × opener-tier to find any mid-paragraph structure. Check if paragraph length = some astronomically meaningful number.
**Expected outcome:** Stars paragraphs may have internal structure corresponding to astronomical catalog format. The ~47-line length in stars may be 47 = some combination like 12+12+12+11 (seasonal months) or 36+N (decans).
**Cost estimate:** small
**Prerequisites:** F105/H183 (exp_098)

---


---

## H187: "OTHER" Para-Start Words — Do They Form Positional Bigrams With Line-2 Words?
**Priority:** medium
**Status:** RESOLVED by exp_194 (2026-04-11). PARTIALLY SUPPORTED — PARA PS → LINE_OPEN at line 2 = 33% (A)/24% (B); ok-onset OTHER → LINE_OPEN = 33%; d-onset OTHER → LINE_OPEN = 0%; B OTHER → OTHER dominant (67%). See F194.
**Source:** F105: 23.2% of A paragraphs start with "OTHER→OTHER" 2-line sequence. If OTHER para-start words have positional grammar, it should appear in their transition probabilities. Do specific OTHER para-starters predict specific line-2 continuations?
**Description:** Extract OTHER para-start words. For each, compute what tier appears on line 2. Does OTHER→LINE_OPEN rate differ by specific OTHER word type? Are some "OTHER" para-starters actually predictive of line-2 structure?
**Expected outcome:** Some OTHER para-start words behave like PARA-tier words (followed by LINE_OPEN at line 2). These would extend the PARA tier class.
**Cost estimate:** small
**Prerequisites:** F105 (exp_098)

---


---

## H188: Extended Positional Classifier — Add bare_k and bare_t to PARA Tier; Test Coverage Improvement
**Priority:** high
**Status:** RESOLVED by exp_100 (2026-04-09). CONFIRMED — v2 classifier PS coverage rises 33-39%→54%; OTHER drops 38%→18-24%; PARA enrichment 6.6×(A)/3.5×(B); remaining OTHER 52-63% o-onset. See F107.
**Source:** F106 (exp_099): bare_k and bare_t are para-starters (F101, 4-10× enriched) but were missing from the PARA-tier classifier. Adding them should improve classifier coverage from ~38-39% to ~65-70% of para-starts.
**Description:** Rebuild the classifier with bare_k and bare_t in PARA tier. Re-evaluate: (1) new precision/recall for PARA tier; (2) what fraction of para-starts are still "OTHER"? (3) Does adding bare_k/bare_t create false positives (within-para k/t words)?
**Expected outcome:** Coverage increases to ~65-70%, precision may decrease slightly (bare_k/bare_t appear within-para too), but enrichment should still be strong (4-12×).
**Cost estimate:** small
**Prerequisites:** F106 (exp_099)

---


---

## H189: B Para-Final Closing Words — okeey, orol, shedy, cheam as a Specialized Para-Closing Class
**Priority:** medium
**Status:** RESOLVED by exp_100 (2026-04-09). PARTIALLY CONFIRMED — okeey/okeeey (∞), orol (21.9×), shedy (6.25× cosmo-specific); covers only 22.8% of B para-finals; no universal B para-closing class. See F107.
**Source:** F106 (exp_099): B has para-final words okeey (16.4×), orol (21.9×), shedy (6.25×), cheam (10.9×). Do these form a coherent lexical class? Test: (1) Are they systematically distributed across all B sections or section-specific? (2) Do they share morphological features (all o-onset + -ey/-eey, or sh- + -edy)? (3) Is the para-final closing signal consistent within individual B folios?
**Description:** Extract all para-final last words in B. Cluster by onset class and suffix. Identify the core B para-closing vocabulary. Compare to B line-final words (which are separate from para-final).
**Expected outcome:** B para-closing words = {o-onset + -ey/-eey} + {sh-onset + -edy} — a closed class of 10-15 words that systematically end paragraphs in B. This would be the B equivalent of A's daiin para-closing function.
**Cost estimate:** small
**Prerequisites:** F106 (exp_099)

---


---

## H190: Astro Section Anomalous Para-Start Grammar — 69% OTHER — What Words Actually Start A Astro Paragraphs?
**Priority:** medium
**Status:** RESOLVED by exp_100 (2026-04-09). CONFIRMED — astro A: 50% OTHER even with v2, LINE_OPEN at PS=11.5% (violations), t/o onset dominant; short captions (3.4 lines) have relaxed grammar. See F107.
**Source:** F106/H186: A_astro has 69.2% OTHER para-starts — highest of any section. These are short captions/labels (~3.4 lines each). What vocabulary do they use? Are they using a completely different para-start system (perhaps image-specific labels)?
**Description:** Extract all astro-section A para-start words. Compute onset distribution. Identify top 20 para-start words. Compare to herbal A para-start vocabulary.
**Expected outcome:** Astro A para-starts use a diverse open-class vocabulary, possibly with more d-onset or o-onset words than other sections, reflecting the label-like nature of astro captions.
**Cost estimate:** very small
**Prerequisites:** F106 (exp_099)

---


---

## H191: o-Onset Para-Start Words — Which Specific o-Onset Words Are Para-Enriched?
**Priority:** high
**Status:** RESOLVED by exp_101 (2026-04-09). CONFIRMED (negative result) — o-onset NOT a coherent PS class (A=0.52×, B=1.28×); only op- sub-class (9.5×) enriched due to internal p-gallows; remaining OTHER (~17-20%) is genuinely diverse. See F108.
**Source:** F107 (exp_100): Remaining OTHER (52-63% o-onset) is the biggest gap in the classifier. But o-onset words are NOT uniformly enriched at para-starts (overall o-onset: A=0.52×, B=1.28×). ONLY SPECIFIC o-onset words are para-enriched. Need to identify which ones.
**Description:** Extract all o-onset words at para-starts and within-para positions. Compute per-word enrichment at para-start. Identify the specific o-onset words that are para-enriched (≥2×). Are they: (1) olfchedy/olkey-type (established from exp_090 as 87.6× para-starters); (2) o+gallows (ok-, ot-) prefix forms; (3) o+ch (och-onset)?
**Expected outcome:** A small set of specific o-onset words (olfchedy, olkey, opchedy, okar, oty, etc.) are strongly para-enriched, while the majority of o-onset words (otol, okaiin, or, etc.) are within-para. This will identify the "o-onset para-starter" class as a closed set of 10-20 specific words.
**Cost estimate:** small
**Prerequisites:** F107 (exp_100)

---


---

## H192: Positional Grammar Strength vs Paragraph Length — Short Paragraphs Have Relaxed Grammar?
**Priority:** medium
**Status:** RESOLVED by exp_101 (2026-04-09). STRONGLY CONFIRMED — A: long (10-15 lines) has strictest grammar (70.7% PARA, 0% LINE_OPEN); short (2-4) has 31% PARA, 8.6% LINE_OPEN violations; B monotonic with length. See F108.
**Source:** F107: Astro A (3.4 lines) has relaxed grammar; herbal A (12-13 lines) has strict grammar. Is there a systematic relationship between paragraph length and grammatical strictness?
**Description:** Bin all paragraphs by length (2-4 lines, 5-9 lines, 10-15 lines, 16+ lines). For each bin, compute PARA% and LINE_OPEN% at para-start and within-para. Test whether short paragraphs have lower PARA% and higher LINE_OPEN% at para-starts.
**Expected outcome:** There is a positive correlation between paragraph length and PARA% at para-start. Very short paragraphs (2-4 lines) have lower grammatical constraint.
**Cost estimate:** small
**Prerequisites:** F107 (exp_100)

---


---

## H193: Section vs Length Separation — Is Grammar Strictness Driven by Section or Length?
**Priority:** medium
**Status:** RESOLVED by exp_196 (2026-04-11). SUPPORTED — primarily section-driven: herbal=74.7%>pharma=63.8%>astro=30.8%; within-herbal length effect weak (80.77%→62.50%); pharma shows REVERSED length effect. See F196.
**Source:** F108: H192 finding conflates section (short=astro, long=herbal, very_long=cosmo+stars) with length. Need within-section analysis: within herbal A, do shorter paragraphs follow grammar less strictly than longer herbal paragraphs?
**Description:** Within each major section (herbal A, pharma A), split paragraphs by length and compute PARA% at PS. If within-section length still predicts grammar strictness, it's a genuine length effect, not a section effect.
**Expected outcome:** Within herbal A, there may be modest length effects (longer herbal paras have higher PARA%), but the main effect is section-level. The "very long" paragraphs in "other" (mean=39.7 lines) may have lower PARA% due to content differences.
**Cost estimate:** small
**Prerequisites:** F108 (exp_101)

---


---

## H194: Cross-Sectional Positional Grammar Summary — What Is the Final Model?
**Priority:** high
**Status:** RESOLVED by exp_198 (2026-04-11). SUPPORTED — A: PS=64.4% PARA; p(12.41×)>f(9.50×)>k(4.32×)>t(2.72×); B: PS=69.3% PARA; k(9.91×)>f(7.62×)>p(3.71×)>t(2.05×). PF-LL: p/f 0.00× both dialects. See F198.
**Source:** F101-F108: We now have a comprehensive positional grammar model. Time to synthesize into a unified, quantitative summary of the complete Voynichese positional grammar.
**Description:** Build a comprehensive table: For each morphological class × position combination, report the attested rates. Final classifier performance with v3. Summary of what fraction of the manuscript is "explained" by the positional grammar.
**Expected outcome:** A complete, coherent positional grammar model for Voynichese: PARA tier covers ~55% of para-starts in main text, LINE_OPEN tier is perfectly excluded from para-starts, the model correctly classifies ~70-75% of main-text (herbal/pharma/stars) para-start words.
**Cost estimate:** medium
**Prerequisites:** F101-F108

---


---

## H195: Section-Specific ch-Stem Vocabulary — Can We Build a ch-Stem Section Classifier?
**Priority:** high
**Status:** RESOLVED by exp_197 (2026-04-11). STRONGLY SUPPORTED — NB classifier 88.7% accuracy (vs 25% baseline); cosmo=96.4%, herbal=89%, stars=87%, pharma=85%. Distinctive: cth- (herbal), cthe- (pharma), ched- (stars), sh+cluster (cosmo). See F197.
**Source:** F109: ch-stem words are section-enriched. Can a ch-stem vocabulary-based classifier identify which section a fragment of text comes from? Test: given a set of ch-words from an unknown paragraph, predict its section (herbal/pharma/stars/cosmo). Baseline: random assignment. Performance: how well does ch-stem vocabulary predict section?
**Expected outcome:** The classifier achieves >50% accuracy on section prediction using only ch-stem words (vs 25% baseline for 4-way classification). The section-distinctive ch-words (chain, cheol, cheo) are the best features.
**Cost estimate:** medium

---


---

## H196: Cross-Dialect ch-Stem Comparison — Do the Same ch-Stems Appear in A-Herbal and B-Stars?
**Priority:** medium
**Status:** RESOLVED by exp_197 (2026-04-11). SUPPORTED — 39.7% shared (≥2 count); B-exclusive=shedy/sheedy/cheedy (all -edy); A-exclusive=cthy/cthor/cthar (cth-forms); 53 universal ch-words cross-section. See F197.
**Source:** F109: Stars B has exclusive ch-words (cheo, cheeo, chedam) not found in herbal B. Do these appear in herbal A? Are the "exclusive" words truly absent or just below detection threshold?
**Expected outcome:** Some ch-stems appear in herbal A but not in B dialect, and vice versa, reflecting genuine vocabulary differences between dialects.

---


---

## H199: Zipf's Law — Does Voynichese Word Frequency Follow a Power Law Rank-Frequency Distribution?
**Priority:** medium
**Status:** RESOLVED by exp_197 (2026-04-11). PARTIALLY SUPPORTED — α=1.021 at ranks 1-1000 (consistent with Zipf); flat head at top-100 (α=0.66); 69.2% hapax rate; Heaps'-Zipf relationship doesn't hold. See F197.
**Source:** F111 (Heaps' law confirmed). Heaps' law and Zipf's law are mathematically related (Heaps' β ≈ 1/Zipf's α for pure power law). Test whether Voynich word frequency rank-frequency distribution follows Zipf's law f(r) ∝ r^(-α), and whether the Zipf exponent α is consistent with the Heaps' β values found in F111.
**Description:** Compute word rank vs frequency for each section and overall. Fit f(r) = C × r^(-α) on log-log scale. Expected: Zipf's α ≈ 1.0-1.5 for natural language. Compare α to the theoretical prediction from Heaps' β (α ≈ 1/β). If α matches the Heaps' prediction, the two statistics are mutually consistent (as they should be for natural language). Also test: are the most frequent words (rank 1-10) the same across sections, or section-specific?
**Expected outcome:** α ≈ 1.3-1.5 (consistent with β≈0.66-0.74 via α≈1/β). Top-ranked words may be grammar/function words (daiin, chedy, qokeedy) universal across sections; lower-ranked words more section-specific.
**Cost estimate:** small

---


---

## H321: What Precedes dam@LL and dy@LL? Is [X][dam@LL] a Specific Bigram Construction?
**Priority:** high
**Status:** RESOLVED by exp_189 (2026-04-11). PARTIALLY SUPPORTED (different pattern than predicted). dam@LL penultimate: d-onset 2.05×, y-onset 2.77× (cth NOT enriched). dy@LL penultimate: cth 2.41×, qok 2.20×. [daiin][dam@LL] = 3 cases. dam/dy have complementary predecessor environments. See F184.
**Source:** F166: dam=3.98× LL-closer, dy=3.02× LL-closer in A. What precedes these terminal words? Is there a [cth-word][dam@LL] or [ot-word][dy@LL] construction?
**Description:** Extract all lines ending in dam@LL (n=23) and dy@LL (n=30). Tabulate penultimate words and onset classes. Compute enrichment of specific penultimate onset classes vs baseline.
**Expected outcome:** dam/dy are preceded by specific onset classes (possibly cth-words or ot-words), revealing a terminal construction [X][dam/dy@LL].
**Cost estimate:** small
**Prerequisites:** F166

---


---

## H323: The [ychor][cthy@second] Construction — Full Context and Folio Cluster
**Priority:** high
**Status:** RESOLVED by exp_189 (2026-04-11). SUPPORTED. cth enriched 4.1× at second position after ychor (2/13 cases). Both cases followed by ch-word at position 3 → potential 3-gram [ychor][cthy][ch-word]. Folios f17 and f45 (herbal A, not same folio). See F184.
**Source:** F167: [ychor][cthy@second]=2 cases. cthy normally LL-enriched (1.63×), but after ychor appears at second=atypical. What follows cthy in these lines? Specific section/folio?
**Description:** Extract full text of all 13 ychor lines. Identify the 2 [ychor cthy...] lines. Tabulate words at positions 2, 3, 4 (third, fourth, fifth). Check folio numbers — are they in same section? Compare third-position word to the typical [ychor][other-word@second] lines.
**Expected outcome:** The [ychor cthy ...] lines have a distinctive third-word or folio cluster (e.g., both in same folio range of herbal section).
**Cost estimate:** trivial
**Prerequisites:** F167

---


---

## H324: Decompose d@LF→cth@second: How Much Is Driven by daiin@LF vs Other d-LF Words?
**Priority:** medium
**Status:** RESOLVED by exp_190 (2026-04-11). daiin drives 38%; d+ch compounds (dchor/dchol/dchey) 4.42× each. Pure d-stems → 0% cth@second. See F185.
**Source:** F167: d@LF→cth@second=1.86× (21/266=7.9%). F164: daiin@LF→cth@second=6 cases. How much of the 21 cases are daiin@LF specifically?
**Description:** Among 266 d@LF lines, identify which d-word opened the line. Tabulate LF-word × second-onset. Focus: daiin@LF→cth@second (n=?), dchor@LF→cth@second (n=?), dchol@LF→cth@second (n=?).
**Expected outcome:** Most d@LF→cth@second cases are daiin@LF (6/21=29%); dchor/dchol may contribute a few.
**Cost estimate:** small
**Prerequisites:** F165, F166, F167

---


---

## H325: Are [cthor→ot-word] Bigrams Concentrated in Specific Herbal Folio Clusters?
**Priority:** medium
**Status:** RESOLVED by exp_190 (2026-04-11). 1-per-folio across 7 folios — structural, not formulaic. See F185.
**Source:** F168: cthor→ot=5.57× (7 bigrams). cthor is 97% herbal (F161). Are these 7 bigrams spread through herbal or clustered in specific folios?
**Description:** Extract folio locations of all 7 cthor→ot bigram occurrences. Check distribution across A-herbal folios. Compute whether they cluster (same folio ≥2) or are spread (1 per folio).
**Expected outcome:** The 7 bigrams are spread across herbal section (1-2 per folio cluster), consistent with a grammatical construction rather than a specific copied formula.
**Cost estimate:** trivial
**Prerequisites:** F168, F161

---


---

## H326: Does the Ordering Constraint [cth before ot-terminal] Generalize? Is [oty@LL][cth-word] Ever Observed?
**Priority:** medium
**Status:** RESOLVED by exp_190 (2026-04-11). [oty][cth]=0 confirmed (categorical). SURPRISE: [oty][l-onset]=15.78× in B-dialect Stars/Bio (f80,f103-f116). See F185.
**Source:** F168: cthor→oty appears (cth before ot-terminal allowed). oty→cth = 0.00× (ot-terminal never followed by cth). Is this asymmetry categorical?
**Description:** Search for all cases where an ot-terminal word (oty, otal, otam) is followed by any cth-word in the same line. Count instances. Compare to cthor/cthol→oty direction.
**Expected outcome:** [oty@LL][cth] = 0 cases (categorical absence), confirming one-directional ordering constraint.
**Cost estimate:** trivial
**Prerequisites:** F168

---


---

## H327: Is the [ot-word][ot-word] Bigram Enriched in A-dialect? (Sparked by f17: otor oteol)
**Priority:** medium
**Status:** RESOLVED by exp_190 (2026-04-11). SUPPORTED: ot→ot enriched 1.84× (26 cases vs expected 14.1). Diverse pairs. See F185.
**Source:** F169: f17 line `ychor cthy che'eky cheo otor oteol` ends with two consecutive ot-words. Is [ot-word][ot-word] a real bigram construction in A?
**Description:** Compute [ot-word][ot-word] bigram enrichment in A-dialect. Baseline: ot-onset rate in A = 4.1%. If baseline, P(ot after ot) = 4.1%. Count observed [ot][ot] consecutive pairs and compute enrichment.
**Expected outcome:** Moderate enrichment (1.5-3×) — ot-words in MID position tend to cluster, consistent with ot-word sequences in medial positions.
**Cost estimate:** trivial
**Prerequisites:** F165, F168, F169

---


---

## H328: What Are the Two [dchor@LF][cth@second] Full Lines? Is [dchor][cthor] a Specific Construction?
**Priority:** medium
**Status:** RESOLVED by exp_191 (2026-04-11). SUPPORTED (n=1 clean). f25: [dchor][cthor] — onset reduplication (d+ch+r → cth+r). f32: artifact token. [dchor][cthor] = 15.54× enrichment but n=1. See F186.
**Source:** F169: dchor@LF → cth@second = 2/12=16.7% (3.98×). Two full lines: f25 `dchor cthor chor daiin s okeeaiin daiin ckhey daiin` and f32 `dchor ctho,daiin`.
**Description:** Both lines identified in exp_162 output. Analyze: what is the cth-word at second in each line? Is it cthor both times? Is [dchor][cthor] a reduplication construction?
**Expected outcome:** Both dchor@LF lines have cthor at second — [dchor][cthor] would be a ch-reduplication formula. f32 `dchor ctho,daiin` has ctho (cth-stem fragment) — consistent with cthor-variant.
**Cost estimate:** trivial (already in exp_162 output)
**Prerequisites:** F169

---


---

## H329: Are [daiin ... dam@LL] Lines Short? Is [daiin][dam] an Immediate Bigram?
**Priority:** medium
**Status:** RESOLVED by exp_190 (2026-04-11). SUPPORTED. [daiin][dam] = 3 immediate cases; dam@LL lines are LONGER than average (7.4 vs 6.1 mean). See F185.
**Source:** F169: daiin appears as penultimate in 3/23 dam@LL lines (3.23×). Are these [daiin dam] immediate bigrams (2-word lines) or longer lines?
**Description:** Check the 3 lines ending `daiin dam`: (1) `qo,ar daiin dam` (f32), (2) `daiin okeey shoaiin otal shshy tal dam` (f70), (3) `qeaiin cheyl seey qotey qokeeol daiin daiin dam` (f89/pharma). How long are these lines? Is `daiin dam` immediate?
**Expected outcome:** Mixed — some short (3-word [X daiin dam]) and some longer. The [daiin][dam] pattern is the closest thing to a precursor construction for dam, but it is not dominant.
**Cost estimate:** trivial (already in exp_162 output)
**Prerequisites:** F169

---


---

## H330: qot→qot=2.22× (15 Cases) and qot→l=2.84× — Which Specific qot-Words Self-Chain or Precede l-Onset?
**Priority:** medium
**Status:** RESOLVED by exp_190 (2026-04-11). Class-level enrichments confirmed; diverse pairs, no word-pair formula. See F185.
**Source:** F170: qot self-succession=2.22× (15 cases, highest among large-n onset classes). Also qot→l=2.84× (4 cases). What specific qot-word pairs drive qot→qot? Are they specific reduplication formulas?
**Description:** Extract all 15 [qot-word][qot-word] consecutive pairs. Tabulate specific word pairs. Also extract all 4 [qot-word][l-word] pairs. Are these from specific folios or spread?
**Expected outcome:** A few dominant qot-word pairs (e.g., qotchy→qotchy, qotor→qotol) plus some diverse pairs. qot→l pairs may be from specific A-herbal folios where l-words appear.
**Cost estimate:** trivial
**Prerequisites:** F170

---


---

## H331: ok→ok=1.96× (54 Cases) — Which ok-Words Chain?
**Priority:** low
**Status:** RESOLVED by exp_190 (2026-04-11). 54 cases; 15% exact same-word self-repetition; diverse pairs, class-level enrichment. See F185.
**Source:** F170: ok self-succession=1.96× (54 cases — large n). Which specific ok-word pairs dominate?
**Description:** Extract all 54 [ok-word][ok-word] pairs and tabulate specific bigrams. Compute top-10 most common ok-ok pairs.
**Expected outcome:** oky→oky or oky→okchol are likely dominant pairs. ok-word chains may be a specific formula class.
**Cost estimate:** trivial
**Prerequisites:** F170

---


---

## H332: l→l=10.21× (n=3) — What Are the Three l→l Cases in A-Dialect?
**Priority:** high
**Status:** RESOLVED by exp_190 (2026-04-11). 3 cases in f35 (2×) and f89 (1×); all involve tokenization artifacts — likely partially artifactual. See F185.
**Source:** F170: l self-succession=10.21× from n=3. l-onset words are predominantly B-dialect — are these 3 l→l cases from B-contaminated A-herbal folios?
**Description:** Find all 3 [l-word][l-word] pairs in A-dialect. Tabulate folio, words, full line context. Are these late A-herbal folios (known B-contamination zone from F147)?
**Expected outcome:** 3 l→l cases are from late A-herbal (f29-f57 region), consistent with B-dialect l-word intrusion in late A-herbal.
**Cost estimate:** trivial
**Prerequisites:** F170, F147

---


---

## H333: ch_e↔r Bidirectional Enrichment (2.55×, n=6 Each) — What Are the Specific Pairs?
**Priority:** medium
**Status:** RESOLVED by exp_191 (2026-04-11). SUPPORTED. ch_e→r: cheol (2×), cheo (2×) → bare 'r' (2×), raiin/ro/rar. r→ch_e: bare 'r' (3×) → cheey (2×). 'r' single-char word specifically attracted to ch_e words bidirectionally. ~2-3 artifact cases per direction. See F187.
**Source:** F170: ch_e→r=2.55× (6 cases) and r→ch_e=2.55× (6 cases). ch_e words (che-, chi- forms) bidirectionally enriched with r-onset words. What specific pairs?
**Description:** Extract all 6 [ch_e][r] and 6 [r][ch_e] pairs. Are they the same words (e.g., [cheol][ral] and [ral][cheol] alternating)? Or different words?
**Expected outcome:** Some overlap — possibly [cheol][ral][cheol] or [cheo][ar] type sequences. If they are the same pairs reversed, this suggests a specific ch_e-r couplet formula.
**Cost estimate:** trivial
**Prerequisites:** F170

---


---

## H334: t→ot=1.85× (n=16) — Which t-Words Precede ot-Words?
**Priority:** medium
**Status:** RESOLVED by exp_191 (2026-04-11). SUPPORTED. 16 cases, tchy dominant (3/16). All pairs distinct — class-level enrichment. See F188.
**Source:** F171: t→ot=1.85× (16 cases) from A-dialect full bigram matrix. t-onset words (tor, taiin, tol, tchey, etc.) specifically precede ot-words. New unexplored pattern.
**Description:** Extract all 16 [t-word][ot-word] consecutive pairs. Tabulate specific word pairs. Which t-words drive this enrichment (taiin? tol? other)?
**Expected outcome:** A few dominant t-words (possibly taiin or tor) precede ot-words. This may connect to the [otaiin→ot] stars-section pattern from B-dialect.
**Cost estimate:** trivial
**Prerequisites:** F171

---


---

## H335: k→cth=1.60× (n=18) — Which k-Words Precede cth-Words?
**Priority:** high
**Status:** RESOLVED by exp_191 (2026-04-11). SUPPORTED. 18 cases (1.57×); kchor dominant (3/18); cthy dominant cth result (4/18). Class-level, no formula. See F188.
**Source:** F171: k→cth=1.60× (18 cases). k-onset words before cth-words are enriched. This is NOT in the existing 5-construction cth-introduction grammar model (F165). What specific k-words and what cth-words follow?
**Description:** Extract all 18 [k-word][cth-word] bigrams. Tabulate specific word pairs. Which k-words are involved (ky? kchol? kchy? kaiin?)? Does this represent a new 6th construction for cth introduction?
**Expected outcome:** Moderate variety — k-words are not dominant cth-introducers but form a real minor construction.
**Cost estimate:** trivial
**Prerequisites:** F165, F171

---


---

## H336: ch→r=2.34× (n=15) — Which ch-Words Precede r-Onset?
**Priority:** medium
**Status:** RESOLVED by exp_191 (2026-04-11). SUPPORTED. 21 total (15 clean, 6 artifact-inflated); cho dominant (4/21); ch_e⊂ch→r confirmed (6/21). See F187.
**Source:** F171: ch→r=2.34× (15 cases). ch_e→r=2.55× (6 cases). Are these overlapping patterns? Which ch-words precede r?
**Description:** Extract all 15 [ch-word][r-word] pairs. Is it predominantly chol→r, chor→r, or ch_e words? What r-words follow? Compare with the 6 ch_e→r pairs from H333/F171.
**Expected outcome:** The 15 ch→r pairs include both ch (non-e) and ch_e forms. ch_e→r is a subset of the broader ch→r pattern.
**Cost estimate:** trivial
**Prerequisites:** F171

---


---

## H337: B-Dialect ch→cth=2.75× (n=8) — What Are These 8 B ch→cth Bigrams?
**Priority:** high
**Status:** RESOLVED by exp_191 (2026-04-11). SUPPORTED. 14 total (8 clean), 1.96× enrichment. B-suffix co-selection: ch-edy/ody → cth-dy/ey/edy. Concentrated f46/f48/f113. See F189.
**Source:** F171: B-dialect ch→cth=2.75× (8 cases). B has very few cth occurrences (15× less than A from F035). When cth appears in B, it's specifically preceded by ch-onset. What sections are these 8 B-dialect ch→cth bigrams from?
**Description:** Extract all B-dialect lines containing cth-words. Find the 8 ch→cth bigrams. Tabulate: which ch-words, which cth-words, which folio/section. Are these from B-herbal (where some A-herbal-like vocabulary appears) or from other B sections?
**Expected outcome:** 8 B ch→cth bigrams concentrated in B-herbal folios where A-dialect vocabulary occasionally appears (dialect mixing zone). cth-words in B are likely cthor/cthol imports from A-herbal.
**Cost estimate:** small
**Prerequisites:** F171, F035

---


---

## H338: Is B-Dialect cthedy/cthdy Genuine B-Vocabulary or Scribal Adaptation?
**Priority:** high
**Status:** RESOLVED by exp_191 (2026-04-11). SUPPORTED — genuine B-vocabulary. cthedy(10), cthey(10), cthdy(6) spread across bio+stars (no pharma concentration). A has only 1 cthedy. F047 narrowed: cth appears in B at 0.25% with B-suffixes. See F189.
**Source:** F172: B-dialect has cthedy (10), cthey (10), cthdy (6) — cth- prefix with B-suffixes. Challenges F047's "cth=A-exclusive." Are these genuine B-vocabulary items or scribal errors/transcription artifacts?
**Description:** For each B-dialect cth-occurrence line: (1) what B-suffix cth-word appears? (2) What words precede/follow it? (3) Does it appear in standard bigram contexts like other B-words? Check if cthedy appears in B-herbal, B-bio, B-stars at similar rates. Check whether these lines are consistent B-dialect (high edy/eedy rate) or mixed.
**Expected outcome:** cthedy/cthdy are genuine B-vocabulary items (consistent B-bigram context, appear in high-edy-rate folios). This would establish cth- as a cross-dialect prefix morpheme with dialect-specific suffix paradigm.
**Cost estimate:** small
**Prerequisites:** F172, F047

---


---

## H339: qok DEPLETES Before cth (0.51×) — Is This Systematic Avoidance?
**Priority:** medium
**Status:** RESOLVED by exp_192 (2026-04-11). SUPPORTED. 0.54× in A (10 vs 18.5 expected); 0.17× in B. Genuine avoidance, not rarity. See F190.
**Source:** F172: qok→cth = 0.51× (10 observed vs expected 19.5). qok-words specifically do NOT introduce cth. Is this because qok is predominantly B-vocabulary (88% B from F037)?
**Description:** Compute qok→cth bigrams in A-dialect only. Does qok@A deplete before cth? Expected: qok is rare in A (12% of qok tokens) so few qok→cth bigrams regardless. Confirm whether the 0.51× depletion is significant given qok rarity in A.
**Expected outcome:** qok→cth depletion is partly explained by qok being rare in A-dialect (not enough qok-word opportunities). The avoidance may be structural (qok and cth are morphologically incompatible — qo selects k/t stems, cth selects o/y/e stems).
**Cost estimate:** trivial
**Prerequisites:** F172, F037

---


---

## H340: cth Self-Succession (1.62×, n=23) — Which [cth1][cth2] Pairs?
**Priority:** high
**Status:** RESOLVED by exp_192 (2026-04-11). SUPPORTED + SURPRISE. cthy dominant cth2 (7/23=30%); all 23 pairs distinct; [cthol][cthy]=1 case only; 3-consecutive cth confirmed in f6.16 and f7.2. See F190.
**Source:** F172: cth self-succession in A = 23 observed, 12.2 expected (1.62×). These are consecutive cth-word bigrams. What are the dominant cth→cth pairs?
**Description:** Extract all 23 A-dialect [cth-word][cth-word] consecutive pairs. Tabulate specific word pairs. Is [cthol][cthy] (MID→LL) the dominant pair? Or [cthor][cthol]? Are any pairs recurrent?
**Expected outcome:** [cthol][cthy] and [cthor][cthol] are the dominant pairs — matching the positional paradigm (cthor@second → cthol@MID → cthy@LL = a 3-cth sequence).
**Cost estimate:** trivial
**Prerequisites:** F172, F161

---


---

## H341: f46 (B-Herbal) Has Anomalous cth Concentration — Is It a Transition Folio?
**Priority:** medium
**Status:** RESOLVED by exp_192 (2026-04-11). NOT SUPPORTED (expected direction). f46 is firmly B (edy=17.1%); cth words use B-suffixes (cthy, cthdy, cthey). Not importing A-vocabulary. See F190.
**Source:** F172: f46 has 4 cth-word occurrences in 3 lines (highest B-herbal concentration). Is f46 at the A/B boundary in the herbal section?
**Description:** Check folio f46: (1) dialect classification (edy/eedy rate); (2) cth rate vs neighboring folios (f44, f45, f47); (3) is there evidence of mixed A/B content? Compare f46's vocabulary profile to adjacent A-herbal and B-herbal folios.
**Expected outcome:** f46 is consistently B-dialect (high edy/eedy rate) but has unusually high cth density, suggesting it may be a scribe-transition folio where A-herbal vocabulary (cth-words) appears in B-dialect text.
**Cost estimate:** trivial
**Prerequisites:** F172

---


---

## H342: Does B-Dialect cthedy Have the Same Positional Profile as Other B-Suffix Words (chedy, shedy)?
**Priority:** high
**Status:** RESOLVED by exp_192 (2026-04-11). NOT SUPPORTED (expected direction). cthedy/cthey are LF-enriched (20%, 1.68×); cthdy LL-enriched (33%, 2.77×) — NOT MID-dominant like chedy/shedy. See F191.
**Source:** F173: B cth is positionally neutral (LF=0.97×, LL=0.97×). Does cthedy specifically match the positional profile of other -edy suffix words like chedy, shedy, qokedy?
**Description:** For B-dialect: compute positional profiles (LF/second/MID/LL enrichments) for cthedy, chedy, shedy, qokedy. If cthedy matches chedy/shedy, it is grammatically equivalent. If it differs, B's cthedy occupies a unique grammatical position.
**Expected outcome:** cthedy~chedy~shedy positional profiles (all MID-enriched, LL-depleted for -edy class). This would confirm cthedy is grammatically equivalent to other B-edy nominals.
**Cost estimate:** small
**Prerequisites:** F173, F045

---


---

## H343: qok→l=2.44× in A — Which qok-Words? Which Folios?
**Priority:** medium
**Status:** RESOLVED by exp_192 (2026-04-11). SUPPORTED. 7 cases, 1/folio (f35/45/55/58/89/99/102), diverse word pairs — class-level, same as qot→l. See F190.
**Source:** F173: qok→l=2.44× is the HIGHEST qok successor enrichment in A-dialect. qok-words specifically introduce l-onset words in A late-herbal/pharma.
**Description:** Extract all A-dialect [qok-word][l-word] consecutive pairs. Tabulate specific words and folio numbers. Are specific qok-words (qokeol? qokar?) the ones that introduce l?
**Expected outcome:** The qok→l pairs are concentrated in late A-herbal (f29-f57) and A-pharma where B-type l-words appear (from F147). Specific qok-words like qokar→lchedy or qokol→lkeedy may dominate.
**Cost estimate:** trivial (from exp_164 data)
**Prerequisites:** F173, F147

---


---

## H344: Is [cthol][cthy] Part of a Longer [daiin cthol cthy] 3-Word Chain?
**Priority:** high
**Status:** RESOLVED by exp_192 (2026-04-11). PARTIALLY SUPPORTED. [daiin][cthol][cthy]=1 case (f7.2); [cthol][cthy]=1 total; [daiin][cthol] leads to diverse successors. See F190.
**Source:** F173: [cth-MID][cthy@LL] is dominant cth self-succession. F164/F165: daiin→cthol (6 cases) and daiin→cthy (9 cases). Is [daiin cthol cthy] a specific 3-word sequence?
**Description:** Search A-dialect for lines containing the trigram [daiin][cthol][cthy] in consecutive positions. Also search [daiin][cthol] where the next word is cthy. Are there any [daiin cthol cthy] 3-grams in the data?
**Expected outcome:** 1-2 cases of [daiin cthol cthy] trigram (combining daiin→cthol and cthol→cthy). This would establish a [determiner][medial-nominal][terminal-nominal] grammatical triplet.
**Cost estimate:** trivial
**Prerequisites:** F173, F160, F164

---


---

## H345: B-cthedy/cthey Are LF-Enriched (1.53×/1.69×) — What Are Their Line-Opening Formulas?
**Priority:** high
**Status:** RESOLVED by exp_192 (2026-04-11). SUPPORTED. cthedy@LF→l/ot (F183 pattern); cthey@LF→ch_e (2/2); distinct LF successor classes. See F191.
**Source:** F174: B-cthedy and cthey are LF-ENRICHED (line-openers), opposite of standard B-edy words. Does cthedy@LF have a distinctive second word?
**Description:** Extract all B-dialect lines where cthedy or cthey appears at LF position. For each, record the second word (position 1). Is there a recurring second word (analogous to A-dialect ychor@LF → cthor/cthol@second construction)? Do cthedy@LF lines have a shared structural formula?
**Expected outcome:** If cthedy is a grammatical line-opener (like a determiner or topic marker), it may consistently select a specific class of second words. If it is a regular content word that happens to appear line-initially sometimes, successors should be diverse.
**Cost estimate:** small
**Prerequisites:** F174

---


---

## H346: [d][cth][d]=16 Is 2nd Most Common cth Onset-Trigram — Are These All Literally [daiin][cth-word][daiin]?
**Priority:** high
**Status:** RESOLVED by exp_192 (2026-04-11). PARTIALLY SUPPORTED. cthol dominant (5/16); daiin left 50%; [daiin][cth][daiin]=2/16 (12.5%); right d-word is dam/dol not daiin. See F190.
**Source:** F174: onset-trigram [d][cth][d]=16 (2nd highest). The d-onset class includes daiin, dam, dy, dol, dain, etc. How many of the 16 cases are specifically daiin as both flanking words?
**Description:** Extract all 16 [d][cth][d] onset-trigrams and tabulate the specific d-words at positions 1 and 3 (flanking the cth-word). What fraction are literally [daiin][cth-word][daiin]? What other d-words flank cth-words?
**Expected outcome:** Majority of [d][cth][d] are [daiin][cth-word][daiin] (since daiin dominates the d-class). This would confirm the specific structural role of daiin as a bilateral cth-word bracket.
**Cost estimate:** trivial
**Prerequisites:** F174

---


---

## H347: B-cthdy Is LL-Enriched (2.41×) — Are All 7 Cases Literally at LL Position?
**Priority:** medium
**Status:** RESOLVED by exp_192 (2026-04-11). SUPPORTED. 2/6=33% at LL (2.77×); 4/6 MID. B-dialect line-terminal parallel to A-dialect cthy@LL. See F191.
**Source:** F174: B-cthdy LL-enrichment = 2.41× (2/7=28.6% at LL vs 12% baseline). Does cthdy specifically close lines?
**Description:** Extract all 7 B-dialect cthdy occurrences and check position in their lines (LL, MID, LF). Are the 2 LL cases truly at line-final position? Does cthdy have the same LL-closing role as A-dialect cthy (LL=1.81×)?
**Expected outcome:** 2/7 cthdy at LL is marginal enrichment (n=2). May confirm or may be noise. Also check: do cthdy lines end with cthdy or is there a following word?
**Cost estimate:** trivial
**Prerequisites:** F174

---


---

## H348: [ch][daiin][cth]=12/17 — Is [ch-word][daiin] a Stable Compound Precursor to cth-Words?
**Priority:** high
**Status:** RESOLVED by exp_192 (2026-04-11). SUPPORTED. 12/20 [ch][d][cth] are daiin-mediated; diverse ch-words (chol 3×, chor 2×, 7 others); daiin is universal bridge; cthy dominant result (4/12). See F190.
**Source:** F175: [ch][d][cth]=17 trigrams, daiin is d-word in 12/17 cases. [ch][daiin][cth] is the dominant form of the highest cth onset-trigram.
**Description:** Extract all 12 [ch][daiin][cth] specific cases. Are these the same ch-words each time (e.g., always chor/chol)? Is [ch-word][daiin] a compound phrase unit (comparable to [ychor][daiin] constructions from F162)? Does [ch][daiin] appear together as a pair at high enrichment, suggesting they function as a grammatical unit before cth?
**Expected outcome:** If [ch][daiin] is a compound unit, the same ch-words should appear before daiin in these cases. If random, diverse ch-words should appear.
**Cost estimate:** small
**Prerequisites:** F175, F162

---


---

## H349: cthol Appears in 5/16 [d][cth][d] Trigrams — Does cthol Have Asymmetric d-Word Preferences (daiin Left, non-daiin Right)?
**Priority:** medium
**Status:** RESOLVED by exp_192 (2026-04-11). NOT SUPPORTED. daiin left=54%, daiin right=43% — no asymmetry. cthol attracts daiin equally on both sides. See F190.
**Source:** F175: [d][cthol][d] = 5 cases — [daiin][cthol][dol], [daiin][cthol][doiin], [dchol][cthol][daiin], [dockhy][cthol][dam], [daiin][cthol][daiin]. daiin appears LEFT of cthol in 3/5; varied words appear RIGHT.
**Description:** Expand to ALL [d][cthol] bigrams (not just trigrams). Does daiin preferentially appear before cthol? And what d-words appear after cthol (from all [cthol][d] bigrams)? Is there an asymmetric preference: daiin→cthol but cthol→diverse-d?
**Expected outcome:** Based on F164/F167: [daiin][cthol]=6 cases (confirmed); [cthol][daiin] may be rarer. The right d-word after cthol may be dol/doiin/dam (shorter d-words) while the left is daiin.
**Cost estimate:** small
**Prerequisites:** F175, F164

---


---

## H350: cthey@LF → ch_e Second Word (2/2 Cases) — Is This a Genuine Pattern?
**Priority:** medium
**Status:** RESOLVED by exp_192 (2026-04-11). PARTIALLY SUPPORTED. 2/2 cthey@LF→ch_e confirmed; general cthey→ch enriched at 2.17× (3/9). n=2 too small for certainty. See F191.
**Source:** F175: both cthey@LF cases are followed by ch_e-onset second words (chey, chedain). n=2 — too small to confirm.
**Description:** Expand beyond LF: when cthey is at the front of a line (LF or second position), what onset does the NEXT word have? Also check cthedy's front-position successors. Does cthey specifically attract ch_e-type words as successors, or is the n=2 finding noise?
**Expected outcome:** If cthey has a genuine ch_e affinity, we'd expect enriched ch_e successor rate even at non-LF positions. If it's noise, successor distribution should be baseline.
**Cost estimate:** small
**Prerequisites:** F175

---


---

## H351: [chol/chor][daiin][cthy] — Is [chol][daiin] a Stable Bigram Unit Preceding cth?
**Priority:** high
**Status:** RESOLVED by exp_188 (2026-04-11). SUPPORTED. [chol/chor][daiin]→cth: 5.30× enrichment (vs 2.30× direct); daiin amplifies chol→cth by 2.3×. cthy dominant (4/12 cases). [chol][daiin][chol] also appears 2× (self-referential chain). See F183.
**Source:** F176: [ch][daiin]→cth=5.89×; chol (3×) and chor (2×) are the dominant ch-words before daiin-cth. Is [chol][daiin] itself a recurrent bigram?
**Description:** Extract all [chol][daiin][?] trigrams in A-dialect. What follows [chol][daiin]? Does cth dominate? Also compare: [chol][daiin] enrichment vs [chol] → cth directly (without daiin). Is daiin a necessary bridge, or does chol sometimes introduce cth directly?
**Expected outcome:** [chol][daiin][cthy] is likely the most common specific trigram (3 cases already found). [chol] without daiin may also precede cth at enriched rate, but daiin boosts the enrichment.
**Cost estimate:** small
**Prerequisites:** F176

---


---

## H352: cthedy → l (5.79×) and ot (5.07×) in B-Dialect — Specific Word Pairs?
**Priority:** high
**Status:** RESOLVED by exp_188 (2026-04-11). PARTIALLY SUPPORTED. l-onset 5.2×, ot-onset 4.5× confirmed; all 10 successors are different words — onset-class enrichment, no stable word-pair formula. See F183.
**Source:** F176: cthedy successor onset l=5.79×, ot=5.07×. What specific l-words and ot-words follow cthedy?
**Description:** Extract all B-dialect cthedy → [word] pairs and tabulate the specific successor words. Are the l-onset and ot-onset successors consistent (same words) or diverse? If specific l-words always follow cthedy, this would establish [cthedy][l-word] as a stable bigram formula in B-dialect.
**Expected outcome:** Given cthedy n=11 with 9 having successors, and l=3 and ot=3 successors, the specific words may be diverse (3 different l-words, 3 different ot-words) or may converge on 1-2 items.
**Cost estimate:** trivial (data already available from exp_169 full lines)
**Prerequisites:** F176

---


---

## H353: cthol Successor Enriched for cth (2.41×) — Are These All [cthol][cthy] Pairs?
**Priority:** medium
**Status:** RESOLVED by exp_188 (2026-04-11). NOT SUPPORTED. cthol→cthy only 1/44 (2.3%); cth enrichment (2.41×) is class-level — 4 different cth-words follow. [cthol][daiin][cthy] absent. cthol→daiin (6×) and cthol→chol (3×) are the dominant patterns. See F183.
**Source:** F176: cthol successor cth=2.41×. From F166: [cth-MID][cthy@LL] is the dominant cth self-succession. The 4 cthol→cth successor cases — are they specifically cthol→cthy?
**Description:** Extract all [cthol][cth-word] bigrams. Is cthy the dominant cthol successor among cth-words? Also: does [cthol][daiin]=6 lead to further cth-words (i.e., [cthol][daiin][cth] trigrams)? This would reveal whether daiin mediates between cthol and cthy: [cthol][daiin][cthy].
**Expected outcome:** Some cthol→cthy direct pairs, and possibly [cthol][daiin][cthy] trigrams where daiin intervenes. This would establish [cthol][cthy] and [cthol][daiin][cthy] as variants of the same [medial-nominal][terminal-nominal] construction.
**Cost estimate:** trivial
**Prerequisites:** F176, F166

---


---

## H354: Is 'r' a B-Dialect Function Word? What Is Its Full Positional and Bigram Profile?
**Priority:** medium
**Status:** RESOLVED by exp_193 (2026-04-11). SUPPORTED. Bare 'r'=strictly MID (0/26 at LF); ch→r=2.04×, r→ch=1.82×; r predominantly B (3.1× more common); non-bare r-words LL-enriched (2.78×). See F193.
**Source:** F187 (exp_191): The bare single-character word 'r' (n=53 in A-dialect) bidirectionally co-occurs with ch_e words at 2.55×. 'r' may function as a grammatical particle adjacent to ch_e words.
**Description:** (1) Compute the full positional profile of 'r': is it LF-, MID-, or LL-enriched? (2) Which onset classes most commonly precede and follow 'r'? (3) Is 'r' a word boundary marker (similar to how dam=LL marker or daiin=common MID word)? (4) What A-dialect lines contain 'r'? Are they clustered in specific folios? (5) Does 'r' appear in B-dialect at all?
**Expected outcome:** 'r' is a mid-line particle with specific attraction to ch_e words. It may mark a grammatical boundary (e.g., a preposition or article equivalent) that appears between ch_e words and their objects.
**Cost estimate:** small
**Prerequisites:** F187

---


---

## H355: [oty][l@LL] in B-Stars — Is This a Line-Closing Construction (oty Penultimate, l-word Terminal)?
**Priority:** medium
**Status:** RESOLVED by exp_193 (2026-04-11). SUPPORTED (marginal). 2.30× enrichment but same signal as general [oty][l] (2.37×); not a distinct sub-construction. See F192.
**Source:** F185 corrected (exp_191): [oty][l-onset] in B-dialect = 2.37× enrichment (6 cases). 3/6 cases have oty at penultimate position with l-word as LL. B-stars section (f103-f116) has 5/6 cases.
**Description:** Test whether the [oty][l@LL] construction is: (1) a penultimate-oty / l-word-terminal formula specific to B-stars, and (2) enriched beyond the overall [oty][l] rate when restricting to cases where oty is penultimate. Compute: among all B-stars lines ending in l-onset, how often is the penultimate word oty? Among all B-stars lines where oty is penultimate, how often does an l-word close the line?
**Expected outcome:** [oty][l@LL] is a genuine sub-construction — penultimate oty before l-word LL-closer — specific to B-stars. This would extend the LL closing-word grammar to include B-stars l-words as a new LL-enriched onset class.
**Cost estimate:** small
**Prerequisites:** F185, exp_191

---


---

## H356: Stars PARA-Tier Words as Zodiacal Entry Markers — Specific Word Analysis and Spacing
**Priority:** high
**Status:** RESOLVED by exp_195 (2026-04-11). SUPPORTED WITH CAVEAT — 246 non-PS markers, 202 unique words (open vocab), top-10=16.7%; only tchedy in 5+ paras (6/23). Onset: p=52%, t=34.6%. Spacing: mean=3.6, median=3.0 lines. No regular cycle. See F195.
**Source:** F194 (exp_194): Stars B paragraphs have PARA-tier words at 13-43% rate from line 3+ (vs ~0% in herbal A). These appear throughout 47-line paragraphs with irregular spacing (mean 2.5 lines between PARA markers). Are these a specific closed set of words? Do they appear at specific para-internal positions corresponding to zodiacal entry boundaries?
**Description:** (1) Extract all PARA-tier words appearing at non-PS positions (lines 3+) in stars paragraphs. What specific words are they? (2) Are they a closed set of ~12-15 words (one per zodiac sign) or diverse? (3) Do the same words appear in each paragraph at the same internal position? (4) Compute position-of-first-PARA-marker within each stars paragraph — is it always at line 4-5?
**Expected outcome:** A specific closed set of p/k/t-onset words appears repeatedly within stars paragraphs as entry markers (12 words for 12 zodiac signs?). Or: the words are diverse but appear at 3-5 line intervals, suggesting a catalog format.
**Cost estimate:** small
**Prerequisites:** F194

---


---

## H357: Full PARA-Tier (k/t/f) Exclusion from Para-Final — Are ALL Gallows Excluded?
**Priority:** medium
**Status:** RESOLVED by exp_195 (2026-04-11). PARTIALLY SUPPORTED — p=0.00× and f=0.00× (perfectly excluded both dialects); k=near-neutral (0.88-0.93×); t=0.50× A but 1.52× B. Only p/f are universally excluded, not k/t. See F195.
**Source:** F194 (exp_194): p-onset is perfectly excluded from para-final (0.00×) in both A and B. This extends the para-start/para-end polarity to the para-end side. Are k/t/f-onset also excluded from para-final (completing the PARA-tier exclusion from para-end)?
**Description:** Compute para-final vs within-para line-final enrichment for ALL gallows: p, k, t, f individually. If all four are excluded from para-final (0.00× or near-zero), this establishes that the PARA tier has perfect bidirectional polarity: ONLY at para-start, NEVER at para-end.
**Expected outcome:** k/t/f-onset are also excluded or depleted at para-final (0-0.3×), completing the PARA-tier exclusion pattern. This would establish that the positional grammar perfectly separates PARA-tier words to para-start boundaries, with no appearance at para-ends.
**Cost estimate:** trivial (reuse exp_194 data)
**Prerequisites:** F194

---


---

## H358: d-Chain Vocabulary Analysis — Do Consecutive d-Final Lines Share Vocabulary?
**Priority:** medium
**Status:** RESOLVED by exp_195 (2026-04-11). SUPPORTED — 29 runs of 3+ consecutive d-final lines in A; 20/29 (69%) have 3+ distinct words (diverse). Only 2/29 identical (daiin×3). d-chains are grammatical, not formulaic. See F195.
**Source:** F194 (exp_194): 75 runs of 3-5 consecutive d-final lines in A-dialect. Are these d-final lines using the SAME d-words repeatedly (formulaic repetition) or different d-words (structural grammatical pattern)?
**Description:** Extract all runs of 3+ consecutive d-final lines. Tabulate the specific d-words at LL for each line in the run. Are the words identical (copy-like repetition), similar (same stem, different suffix), or diverse?
**Expected outcome:** Diverse d-words in consecutive d-final lines would suggest a grammatical pattern (all lines in a passage use d-final words, different vocabulary). Identical d-words would suggest formulaic repetition.
**Cost estimate:** small
**Prerequisites:** F194

---


---

## H359: B Within-Para LF Composition — What Onset Classes Fill B WP-LF Positions Where A Uses k-Onset?
**Priority:** medium
**Status:** RESOLVED by exp_199 (2026-04-11). SUPPORTED — B WP-LF: p(4.14×), l(4.92×), s(1.71×), qok(1.66×) enriched vs A; k(0.46×) depleted. p floods B WP-LF (9.61% vs A 2.32%), pushing k to PS-only. See F199.
**Source:** F198 (exp_198): B within-para LF has k-onset at only 1.30% (vs A=2.84%). B PS has k-onset at 12.87% (PS enrichment 9.91×). In A, k-onset appears both at PS (12.27%) and within-para LF (2.84%), but in B it almost never appears at within-para LF (1.30%). What displaces k at B WP-LF? Is it displaced by more sh-onset words? More y-onset words? Or does the qo-complex vocabulary fill the within-para LF slot in B?
**Description:** Compute complete onset distribution at B WP-LF vs A WP-LF. Identify which onsets are elevated in B WP-LF that are not elevated in A WP-LF. Is B WP-LF dominated by different onset classes (qo-complex? sh? y?) than A WP-LF?
**Expected outcome:** qo-complex or sh-onset words displace k at B WP-LF, explaining why k appears almost exclusively at B para-starts.
**Cost estimate:** trivial (reuse existing parser)
**Prerequisites:** F198

---


---

## H360: d+ch → sh Successor — Which Specific sh-Words Follow d+ch Lines?
**Priority:** medium
**Status:** RESOLVED by exp_199 (2026-04-11). PARTIALLY SUPPORTED — d+ch→sh (12/94=12.8%, 1.77×); sh-words diverse (8 types); shol dominates (4/12=33.3%, 2.7×); no single formulaic word. See F199.
**Source:** F196 (exp_196): After d+ch lines (within-para), the next line's first word is sh-onset at 1.77× enrichment vs baseline. After y+ch lines, sh is depleted (0.34×). Are the sh-following words specific (shedy? sheey? shol?) or are they a diverse sh-class?
**Description:** Collect all within-para d+ch lines and their following lines. For cases where the next line starts with sh-onset: what specific sh-onset words appear? Compute the top-10 sh-words following d+ch, and compare to the baseline sh-word distribution. Is there a specific sh-word that drives the d+ch → sh enrichment?
**Expected outcome:** Specific sh-onset words (likely shedy or sheey, B-type suffix forms, or shol, a common sh-word) follow d+ch lines disproportionately, or the sh enrichment is spread across many sh-words.
**Cost estimate:** small
**Prerequisites:** F196

---


---

## H361: Gallows+ch Para-Starter Distribution — Is p+ch Concentrated in Specific Folios While k+ch Dominates Others?
**Priority:** medium
**Status:** RESOLVED by exp_199 (2026-04-11). NOT TESTABLE — herbal A has 1 para per folio (n=1 per folio), preventing folio-level variation analysis. Overall: p+ch=12.6% > t+ch=8.0% > k+ch=5.7% > f+ch=4.6%. See F199.
**Source:** F196 (exp_196): A PS hierarchy: p+ch(11.66%) > t+ch(7.36%) > k+ch(3.07%) > f+ch(2.45%); B: p+ch(21.78%) > t+ch(10.89%) > k+ch(4.95%) > f+ch(0.99%). Are these hierarchical positions consistent across all folios or are there folio clusters where k+ch dominates over p+ch?
**Description:** For each herbal A folio with ≥ 5 paragraphs, compute the fraction of PS lines starting with p+ch vs t+ch vs k+ch. Is the hierarchy p>t>k consistent within folios, or is there folio-level variation?
**Expected outcome:** The hierarchy is consistent across folios (p+ch dominant everywhere). OR: some folios prefer k+ch over p+ch, suggesting scribe-level or section-level differences.
**Cost estimate:** small
**Prerequisites:** F196, F198

---


---

## H362: daiin Cross-Dialect Positional Profile — Does daiin Show LL Stability Like dam?
**Priority:** high
**Status:** RESOLVED by exp_200 (2026-04-11). SUPPORTED — daiin PARTICIPATES in d-onset shift (A-LL=23.9%→B-LL=9.5%, A-LF=18.3%→B-LF=33.0%). dam uniquely invariant (LF=0% both dialects, LL increases from 64.1%→79.2%). See F200.
**Source:** F195 (exp_195): dam shows cross-dialect LL invariance (LF=0% in both A and B), despite the general d-onset positional reversal between dialects (A: d-onset LL-biased; B: d-onset LF-biased). daiin is the most frequent word overall (A: ~6% of tokens; B: ~4%). Does daiin also resist the d-onset positional shift, remaining LL-confined in both dialects? Or does daiin follow the general B shift toward LF/WP-LF?
**Description:** Compute the full positional profile (LF%, second%, MID%, LL%) for daiin in both A and B dialects. Also compute for dy, dol, dain (other common d-onset words). Compare to the general d-onset class distribution at each position. Identify which specific d-onset words drive the A LL→B LF positional reversal and which resist it (like dam).
**Expected outcome:** daiin may also be LL-biased in A (consistent with its common occurrence as a line-closer) but shows different B behavior than dam. Alternatively, daiin shifts to LF/MID in B, making it the driver of the d-onset reversal while dam stabilizes at LL.
**Cost estimate:** small (ZL3b parser reuse)
**Prerequisites:** F195, F198

---


---

## H363: B Para-Final Closing Vocabulary — What Specific Words Close B Paragraphs?
**Priority:** high
**Status:** RESOLVED by exp_200 (2026-04-11). PARTIALLY SUPPORTED — onset constraints confirmed (cth=6.98×, ok=2.71×, sh=2.66×, ch=1.81×; d=0.11× depleted); but B PF-LL is open vocabulary (no closed formula class); cosmo B: shedy(13.8%)/chedy(10.3%) = partial formula. See F200.
**Source:** F198 (exp_198): B PF-LL is enriched for ok(2.71×), sh(2.66×), ch(1.81×) vs within-para WP-LL. The specific words driving these onset-class enrichments are unknown. In A, okeey, orol (from F107) are para-final specialists. What specific words close B paragraphs?
**Description:** (1) Extract all B para-final last words. (2) Compute per-word enrichment at PF-LL vs WP-LL. (3) Identify the top-20 B PF-LL words. (4) Are there B-specific para-closing formulas analogous to A's daiin/okeey? (5) Do the specific B para-final words vary by section (herbal/pharma/stars)?
**Expected outcome:** A small closed set of B para-final words (shedy, okeey, cheam, okedy, or similar) drives the ok/sh/ch enrichment. These would be the B equivalents of A's para-final vocabulary (daiin, okeey, orol).
**Cost estimate:** small
**Prerequisites:** F198

---


---

## H364: p-Onset WP-LF Vocabulary in B — Which Specific p-Onset Words Flood B's Within-Para LF?
**Priority:** medium
**Status:** RESOLVED by exp_200 (2026-04-11). SUPPORTED — flooding driven by POL-prefix words (pol/polaiin/polchedy), not pch-para-starters; 141/174 (81%) B WP-LF p-onset words never appear at PS; two subclasses: POL (WP-LF) vs PCH (PS). See F200.
**Source:** F199 (exp_199): p-onset words at B WP-LF = 9.61% (vs A WP-LF = 2.32%, ratio 4.14×). This "flooding" of B WP-LF by p-onset displaces k-onset and concentrates k at PS. But which specific p-onset words appear at B WP-LF? Are they the same p+ch para-starters that appear at PS, appearing more broadly in B? Or are there distinct p-onset words that serve WP-LF but not PS roles?
**Description:** (1) Extract all p-onset words at B WP-LF. (2) Compute per-word frequency and compare to p-onset words at B PS. (3) Are the B WP-LF p-onset words the same as B PS p-onset words (just the para-start vocabulary appearing more broadly)? (4) Compute p-onset enrichment at B WP-LF vs B PS for individual words — are some words exclusively WP-LF-p while others are PS-p?
**Expected outcome:** Two possible outcomes: (a) B WP-LF p-onset words are the same set as B PS p-onset words but appearing at lower concentration at WP-LF (a single p-onset vocabulary used at both positions); or (b) distinct p-onset subsets for WP-LF vs PS — a genuine split between "true para-starters" and "within-para line-openers" within the p-onset class.
**Cost estimate:** small
**Prerequisites:** F199, F198

---


---

## H365: sh-Prefix Successor Profile — Is she-qo Affinity Shared by All sh-Prefix Words?
**Priority:** medium
**Status:** RESOLVED by exp_200 (2026-04-11). STRONGLY SUPPORTED — she-qo affinity is specific to she-prefix (qok: she=24.83% vs non-she=11.05%, 2.25×); non-she sh-words prefer ch/sh/d; cth enriched 4.3× MORE after non-she vs she. she-prefix = distinct grammatical morpheme. See F200.
**Source:** F195 (exp_195): she-prefix successor enrichments: qo(3.33×), t(2.51×), qok(2.18×); depleted ch(0.49×), d(0.57×). Is this qo affinity specific to she-prefix words (she-*, shee-*), or do all sh-prefix words (shol, shod, shok, etc.) show the same successor pattern?
**Description:** (1) Segment sh-prefix words into two groups: she-words (she*, shee*) and non-she sh-words (shol, shod, shok, sho, etc.). (2) Compute successor onset distributions for both groups. (3) Compare: does the she-specific qo enrichment appear in non-she sh-words? (4) Are non-she sh-words more likely to precede different successor classes?
**Expected outcome:** The qo-successor affinity is specific to she-prefix words (reflecting their grammatical role as described in F195). Non-she sh-words (shol, shod) have a different successor profile (possibly enriched for d or ch successors, consistent with their different grammatical function as LL-enriched words per F198).
**Cost estimate:** small
**Prerequisites:** F195

---


---

## H366: POL-Prefix Words in B — What Is the Full Positional Profile of pol/polaiin/polchedy?
**Priority:** high
**Status:** RESOLVED by exp_201 (2026-04-11). SUPPORTED — pol-prefix B: 87.1% LF, 0% LL (n=70); stars(52.9%)+cosmo(41.4%); A=9 tokens only. pol-onset is a B-specific LINE_OPEN class with hard LL exclusion. See F201.
**Source:** F200 (exp_200): B WP-LF p-onset flooding is driven by POL-prefix words (pol=11, polaiin=6, polchedy=5 at WP-LF). These are morphologically distinct from pch-para-starters. But what is the full positional profile of pol-prefix words? Are they exclusively WP-LF, or do they also appear at MID and LL positions? Are they A-dialect as well, or B-specific?
**Description:** (1) Extract all pol-prefix words in both A and B dialects. (2) Compute their positional distributions: LF (PS + WP-LF), MID, LL. (3) Compare to pch-prefix word positional distributions. (4) Are pol-prefix words exclusively B-dialect, or do they appear in A? (5) Section distribution: are pol-words concentrated in specific B sections?
**Expected outcome:** pol-prefix words in B are primarily WP-LF line-openers with some MID presence, low LL, nearly zero PS. In A, pol-prefix may be rarer or absent. This would confirm pol-onset as a B-specific LINE_OPEN subclass, extending the grammar model.
**Cost estimate:** small
**Prerequisites:** F200

---


---

## H367: daiin Predecessor/Successor Profile — What Precedes daiin@LL in A and What Follows daiin@LF in B?
**Priority:** medium
**Status:** RESOLVED by exp_201 (2026-04-11). SUPPORTED — A daiin@LL predecessor: ch(1.40×)/chol(10), qot(2.26×). B daiin@LF successor: sh(2.15×)+ch(2.00×)=73.6%; shey(5)/chedy(4)/chey(4). Bidirectional sh/ch adjacency. See F201.
**Source:** F200 (exp_200): daiin shifts from LL-biased in A (23.9% LL) to LF-biased in B (33.0% LF). The functional change suggests a grammatical role shift. In A: what is the penultimate onset before daiin@LL? In B: what follows daiin@LF (the second word)?
**Description:** (1) In A: extract all lines where daiin is at LL. Compute penultimate-word onset distribution vs baseline. (2) In B: extract all lines where daiin is at LF (first word). Compute second-word onset distribution vs baseline. (3) Compare: does daiin@LF-B have a characteristic second-word class that mirrors daiin@LL-A's predecessor class?
**Expected outcome:** In A, daiin@LL is preceded by diverse mid-line content. In B, daiin@LF may introduce ch or qok words (consistent with B's LINE_OPEN tier function). The role reversal would suggest daiin functions as a line-boundary marker in both dialects — just at different ends of the line.
**Cost estimate:** small
**Prerequisites:** F200, F195

---


---

## H368: Non-she sh-Prefix Words' cth Affinity — Which Specific sh-Words Precede cth?
**Priority:** medium
**Status:** RESOLVED by exp_201 (2026-04-11). SUPPORTED — sh→cth n=27: shol(5)+shor(3)+shaiin(3)+sho(3); cthy=30%; 22 folios; A-herbal=85%. sh-onset = 6th cth-introduction construction (1.72×). See F201.
**Source:** F200 (exp_200): Non-she sh-prefix words have cth-successor enrichment at 1.72× (2.76% vs baseline 1.60%), n=27 cases. she-prefix has cth at 0.39× (avoids cth). Which specific non-she-sh words drive the cth enrichment, and what cth-words follow?
**Description:** (1) Extract all [non-she-sh word][cth-word] bigrams (n≈27). (2) Which sh-words: shol, sho, shor, shy, shcthy? (3) Which cth-words follow: cthor, cthol, cthy? (4) Are these concentrated in specific sections? (5) Compare to F165's 5 cth-introduction constructions — is sh-onset a new 6th construction?
**Expected outcome:** The sh→cth enrichment involves 2-3 specific sh-words (likely shol or sho) and 1-2 specific cth-words (likely cthor/cthol). These spread across herbal A folios — a grammatical pattern, not a formulaic repetition. sh-onset may be a 6th cth-introduction construction.
**Cost estimate:** trivial
**Prerequisites:** F200, F165

---


---

## H369: cosmo B Para-Final shedy/chedy — Are These Spread Across Paragraphs or Concentrated?
**Priority:** medium
**Status:** RESOLVED by exp_201 (2026-04-11). SUPPORTED — shedy(14.72×)/chedy(5.15×) spread across 7 paragraphs in 6 folios (f75r-f84v); 21.9% coverage = section-level formula confirmed. See F201.
**Source:** F200 (exp_200): cosmo B PF-LL: shedy(4/29=13.8%), chedy(3/29=10.3%) — together 24% of cosmo B para-finals. Are these concentrated in specific cosmo paragraphs or spread across all 29 cosmo B paragraphs?
**Description:** (1) Extract all 29 cosmo B paragraph-final last words. (2) How many distinct cosmo B paragraphs end with shedy? With chedy? (3) What is the within-para LL rate for shedy/chedy in cosmo B vs PF-LL rate? (4) Are there other cosmo B sections (f75r-f84v) where shedy/chedy appear differently?
**Expected outcome:** shedy/chedy are spread across many cosmo B paragraphs (not concentrated in 1-2), confirming section-wide formula status. Their PF-LL rate (13.8%/10.3%) should be substantially higher than their WP-LL rate in cosmo B, confirming para-boundary enrichment.
**Cost estimate:** trivial (n=29)
**Prerequisites:** F200

---


---

## H370: pol-Prefix Word Successor Profile — What Follows pol/polaiin/polchedy at Line-First in B?
**Priority:** high
**Status:** RESOLVED by exp_202 (2026-04-11). SUPPORTED — pol@LF: ch DEPLETED (0.26×), sh weak (1.29×), ol(1.84×)/ot(2.20×); pol ≠ daiin (daiin→sh/ch 2.15×/2.00×). pol and daiin are distinct LINE_OPEN classes. See F202.
**Source:** F201 (exp_201): pol-prefix words in B are 87.1% LF with hard LL exclusion (0/70). They function as LINE_OPEN para-internal openers in stars/cosmo. But what do they open TO? What is the second word after pol/polaiin/polchedy at LF — is it a ch-onset word (consistent with daiin@LF's sh/ch successor profile), a qok word, or something distinct?
**Description:** (1) For each B pol-prefix word at LF (pos 0), extract the second word (pos 1). (2) Compute second-word onset distribution vs baseline. (3) Compare to daiin@LF B successor profile (sh=2.15×/ch=2.00×). (4) Do specific pol-words (pol vs polaiin vs polchedy) have different successor profiles? (5) Test by section (stars vs cosmo).
**Expected outcome:** pol-prefix words are followed by ch/sh-onset words (similar to daiin's B@LF successor profile), OR by qok words (consistent with LINE_OPEN function), OR by content-specific vocabulary. If pol@LF successors differ from daiin@LF successors, this distinguishes two LINE_OPEN subclasses by their characteristic "opening move."
**Cost estimate:** small
**Prerequisites:** F201

---


---

## H371: daiin@MID in A — What Is Its Predecessor and Successor Onset Profile?
**Priority:** medium
**Status:** RESOLVED by exp_202 (2026-04-11). SUPPORTED — daiin@MID predecessor: ch(1.18×, chol=17); daiin@MID successor: cth(3.05×)/cthy(9)/cthol(5). [daiin→cth] is a within-line (MID) construction. See F202.
**Source:** F201 (exp_201): In A, daiin is at LL=23.9% and LF=18.3%, so ~57.8% of A daiin tokens are at MID position. We know the predecessor of daiin@LL in A is ch-onset (1.40×). But in MID position, daiin is neither line-final nor line-initial — what precedes AND follows it? Is the ch adjacency specific to the LL position, or does daiin maintain ch-adjacency even at MID?
**Description:** (1) Extract all A-dialect lines where daiin appears at a MID position (not first, not last word). (2) Compute predecessor onset (word before daiin@MID) distribution vs baseline. (3) Compute successor onset (word after daiin@MID) distribution vs baseline. (4) Compare predecessor profile to daiin@LL predecessor profile (ch=1.40×). (5) Is daiin@MID surrounded by ch/sh vocabulary in both directions, or only in one direction?
**Expected outcome:** daiin@MID in A may still prefer ch-predecessors (consistent with ch-daiin being a collocational unit regardless of line position), while the successor at MID may differ from what follows daiin@LF in B. If the ch-predecessor is specific to daiin@LL (not daiin@MID), the ch adjacency is a line-final construction. If ch-predecessor appears at daiin@MID too, it's a lexical affinity independent of position.
**Cost estimate:** small
**Prerequisites:** F201

---


---

## H372: Unified Ranking of All 6 cth-Introduction Constructions by Enrichment Rate
**Priority:** medium
**Status:** RESOLVED by exp_202 (2026-04-11). SUPPORTED — Ranking (all A): ychor_stem(3.06×)>daiin(2.93×)>>d_onset(1.67×, daiin-driven)>k_onset(1.35×)>sh_nonshe(1.11×)≈ch_onset(1.10×). sh_nonshe NOT a genuine cth-constructor within A (1.02× in A-herbal). F201 sh claim narrowed. See F202.
**Source:** F165 (5 constructions: ychor→cth, daiin→cth, ch-word→cth, d+ch→cth, k→cth) + F201 (6th: sh-onset→cth, 1.72×). We have enrichment estimates for sh→cth from F201 (1.72×, n=27) but no systematic ranking table for all 6. Which predecessor class has the strongest cth-introduction enrichment? Is ychor→cth still the top, or has a quantitative ranking not been established in a single unified experiment?
**Description:** (1) For all bigrams [predecessor][cth-word] in A-herbal (the primary cth-construction section): extract all predecessor words/onsets. (2) For each of the 6 known predecessor classes (ychor-stem, daiin, ch-onset, d+ch-construction, k-onset, sh-onset non-she), compute enrichment rate = P(cth-successor|this predecessor) / P(cth-successor|all words). (3) Rank the 6 classes by enrichment magnitude. (4) Are there other predecessor classes with enrichment >1.5× not in the known 6?
**Expected outcome:** ychor→cth likely has the highest enrichment (F165 described it as strongest), followed by daiin→cth, then ch-word→cth, k→cth, sh-onset→cth (1.72×), with d+ch→cth possibly lowest. A unified ranking table would finalize the cth-introduction grammar model.
**Cost estimate:** small
**Prerequisites:** F165, F191, F201

---


---

## H373: cosmo B shedy/chedy — Restriction or Elevation? WP-LL vs PF-LL Rate
**Priority:** medium
**Status:** RESOLVED by exp_202 (2026-04-11). SUPPORTED — shedy: PF/WP=13.34× (genuine restriction); chedy: PF/WP=4.67× (general LL word, weak PF elevation). F201 overstated chedy as closing formula. See F202.
**Source:** F201 (exp_201): cosmo B PF-LL: shedy=14.72×, chedy=5.15× enriched vs corpus WP-LL baseline. But the WP-LL baseline is the WHOLE-CORPUS non-para-final LL rate. What is the cosmo B WITHIN-PARA (WP-LL) rate of shedy/chedy specifically? Is the para-final enrichment because shedy/chedy are RESTRICTED to PF-LL (rarely appearing at WP-LL in cosmo), or because they're ELEVATED at PF-LL while also appearing at WP-LL?
**Description:** (1) In cosmo B paragraphs: separate PF-LL (last word of last line) from WP-LL (last word of non-last lines). (2) Compute shedy rate and chedy rate at WP-LL in cosmo B. (3) Compare to PF-LL rates: shedy=4/29, chedy=3/29. (4) Enrichment = PF-rate/WP-rate within cosmo B only (not corpus-level). (5) If WP-LL cosmo B shedy rate ≈ PF-LL cosmo B shedy rate → elevation, not restriction. If WP-LL rate << PF-LL rate → restriction (shedy is specifically para-terminal).
**Expected outcome:** shedy/chedy in cosmo B have substantially lower WP-LL rates than PF-LL rates — they are preferentially para-final (restriction), not equally distributed across all LL positions. This would confirm them as genuine para-closing formulae, not just common cosmo B LL words.
**Cost estimate:** trivial
**Prerequisites:** F201

---


---

## H374: pol-Prefix PS Rate — Do pol-Words Ever Appear at Para-Starts (First Word of First Line)?
**Priority:** high
**Status:** RESOLVED by exp_203 (2026-04-11). SUPPORTED (nuanced) — pol@PS=5 (7.14%) but productive pol-words (pol/polchedy/polaiin/polshy) have PS=0; hapax pol-words only. pol is functionally WP-LF exclusive for productive vocabulary. See F203.
**Source:** F202 (exp_202): pol-prefix words are 87.1% LF in B, 12.9% MID, 0% LL. But F200 claims pol-words are "exclusively WP-LF" (within-para line openers, not para-starters). In exp_201, LF included both PS and WP-LF positions. Do any pol-prefix words appear at PS (first word of first line of a paragraph)?
**Description:** (1) Separate pol-prefix B occurrences into PS (first word of first line of paragraph) vs WP-LF (first word of non-first lines) vs MID vs LL. (2) Count PS occurrences of pol-prefix words. (3) Compare to pch-prefix PS vs WP-LF separation (pch should be predominantly PS). (4) If pol@PS = 0, the claim "pol is exclusively WP-LF" is confirmed. If pol@PS > 0, pol is partially a para-starter.
**Expected outcome:** pol-prefix words appear at PS=0 or very rarely (0-2%), confirming pol as a pure WP-LF opener. pch-prefix should show PS dominance (>70%). This separation would confirm the pol/pch functional split at sub-LF granularity.
**Cost estimate:** trivial
**Prerequisites:** F200, F201, F202

---


---

## H375: [ch-word][daiin][cth-word] Triple in A — Count and Enrichment
**Priority:** medium
**Status:** RESOLVED by exp_203 (2026-04-11). PARTIALLY SUPPORTED — triple n=12 (1.51× enriched vs expected 8.0); ch-pred and cth-succ affinities of daiin are independent; 22/34 daiin→cth lack ch-pred. Not a tight 3-word construction. See F203.
**Source:** F202 (exp_202): In A, daiin@MID predecessor is ch-onset (1.18×) and daiin@MID successor is cth-onset (3.05×). The combined construction [ch-word][daiin][cth-word] within a single line should be ~3.6× enriched (1.18×3.05×). Can we count actual triples where pos[j-1]=ch-onset, pos[j]=daiin, pos[j+1]=cth-onset?
**Description:** (1) Scan all A-dialect lines for the triple pattern: [ch-onset word][daiin][cth-onset word] (j-1, j, j+1 positions). (2) Count occurrences (expected ~20+ based on n=256 daiin@MID × 23% ch-pred × 13% cth-succ ≈ 7-8 triples). (3) Compute enrichment vs random triple occurrence rate. (4) What are the specific ch-words and cth-words in these triples? (5) Compare to [other-pred][daiin][cth-word] (non-ch predecessors) to confirm ch-specific enrichment.
**Expected outcome:** ~5-15 [ch-onset][daiin][cth-onset] triples, enriched ~3-4× vs random. Top triples likely: [chol][daiin][cthy], [chor][daiin][cthy], etc.
**Cost estimate:** trivial
**Prerequisites:** F202

---


---

## H376: daiin@LF Successor Profile in A-Dialect — Does Position Change the daiin→cth Pattern?
**Priority:** medium
**Status:** RESOLVED by exp_203 (2026-04-11). SUPPORTED — A daiin@LF: cth(2.42×), ch depleted(0.79×); A/B split is absolute — A daiin→cth always(LF:2.42×,MID:3.05×); B daiin→sh/ch, cth=0%. See F203.
**Source:** F202 (exp_202): daiin@MID in A is followed by cth(3.05×). We know daiin@LF in B is followed by sh+ch(2.15×+2.00×). But what is daiin's successor profile when at LF in A? In A, daiin@LF would be the first word of a line — its successor is the second word. Does daiin@LF in A also attract cth-successors (consistent with within-line construction), or does the line-initial position change the successor class?
**Description:** (1) Extract all A-dialect lines where daiin is at LF (pos 0). (2) Compute second-word onset distribution vs baseline. (3) Compare to: (a) daiin@MID A successor (cth=3.05×); (b) daiin@LF B successor (sh=2.15×, ch=2.00×). (4) Is daiin@LF in A a hybrid (both cth and ch enriched) or does it match the B profile?
**Expected outcome:** daiin@LF in A may show cth enrichment (consistent with daiin as cth-introducer regardless of line position) or may show neutral/different profile (suggesting daiin@MID→cth is specific to within-line position). If A daiin@LF also shows cth-successor enrichment, daiin is a general cth-attractor in A that operates at any line position.
**Cost estimate:** trivial
**Prerequisites:** F202, F201

---


---

## H377: pch-Prefix Successor Profile at PS — What Does pch Open Into?
**Priority:** medium
**Status:** RESOLVED by exp_203 (2026-04-11). SUPPORTED — B pch@PS: o(1.71×)/ol(1.67×)/d(1.48×); pol@WP-LF: ch depleted(0.28×) = "ch-isolator"; A pch@PS: qo(3.06×)/ch(1.68×) — opens into A-dialect core vocabulary. See F203.
**Source:** F202 (exp_202): pol@WP-LF opens into ot/ol/sh avoiding ch (0.26×). pch-prefix words are predominantly PS (para-starters). What is the second word after pch@PS? Is pch followed by ch-onset words (consistent with gallows+ch para-starting grammar) or by a different vocabulary?
**Description:** (1) Extract all pch-prefix words at PS (first word of first line of paragraph) in both A and B. (2) Compute second-word onset distribution vs baseline. (3) Compare to pol@WP-LF second-word profile (H370). (4) Are pch@PS and pol@WP-LF simply different line-opening words with similar successors, or do they open into different vocabulary classes?
**Expected outcome:** pch@PS is followed by diverse paragraph content (d-onset, ch-onset, qok) — possibly the same distribution as baseline paragraph openings. This would confirm that pch marks the paragraph boundary without constraining successor vocabulary, while pol constrains successor vocabulary (avoids ch). The contrast would establish that pol and pch differ not just in para vs WP-LF position but in their successor grammar.
**Cost estimate:** small
**Prerequisites:** F202, F200

---


---

# BATCH ARCHIVE: Hypotheses Resolved exp_204–286 (2026-04-11)
# The following hypotheses were resolved after the last archive update (through exp_203).
# Full hypothesis text was in the active backlog prior to 2026-04-11 cleanup.
# For experiment details, see experiments/expN/result.md for the resolving experiment.

## H378: -aiin Suffix Words as cth-Introduction Class in A
**Status:** RESOLVED by exp_204. SUPPORTED (nuanced) — -aiin class 1.92×; onset-class driven (shaiin=6.56×/okaiin=3.48×/daiin=2.93×); zero-cth: aiin/qokaiin/saiin. See F204.

## H379: cth-Word Successor Profile in A
**Status:** RESOLVED by exp_204. SUPPORTED — cth→d(1.33×)/cth(1.49×)/ot(1.48×)/qo(1.64×); sh depleted(0.57×); grammar cluster ch→daiin→cth→daiin/d confirmed. See F204.

## H356: Stars Section B Non-PS PARA-tier Markers
**Status:** RESOLVED by exp_195. SUPPORTED WITH CAVEAT — 246 non-PS PARA markers, 202 unique words; only tchedy in 5+ paras; mean spacing 3.6 lines, no cycle. See F195.

## H357: Para-Final LL Gallows Exclusion
**Status:** RESOLVED by exp_195. PARTIALLY SUPPORTED — ONLY p/f perfectly excluded (0.00× both); k near-neutral; t=0.50×A but 1.52×B. Refines F194. See F195.

## H358: d-Chain Vocabulary Diversity
**Status:** RESOLVED by exp_195. SUPPORTED — 20/29 runs have 3+ distinct words; daiin dominates but chains are grammatical. See F195.

## H359: B WP-LF Onset Composition
**Status:** RESOLVED by exp_199. SUPPORTED — B WP-LF: p 4.14×, l 4.92×, k 0.46×. p-flooding (9.61% vs A 2.32%) explains k PS-concentration. See F199.

## H360: d+ch Successor Profile
**Status:** RESOLVED by exp_199. PARTIALLY SUPPORTED — d+ch→sh primarily shol (33.3%/2.7×); diverse 8-word sh set; no formulaic word. See F199.

## H408: Parameter-Count Control
**Status:** RESOLVED by exp_224. ANSWERED — Architecture matters; each Mode B feature necessary. Mode B=11/18 > Alt B=10/18 > Alt A=9/18 >> Alt C=6/18. See F224.

## H409: Parameter Stability Under Corpus Split
**Status:** RESOLVED by exp_223. CONFIRMED STABLE — 11/18 PASS in FULL/ODD/EVEN identically. See F223.

## H410: Expanded Metric Audit
**Status:** RESOLVED by exp_217. NEGATIVE — 1/13 uncalibrated metrics pass; 12/13 fail including wrong-direction failures. See F217.

## H412: Fix LL_ONSETS Architecture
**Status:** RESOLVED by exp_218. MIXED — ch_ll/ok_ll/qok_ll reduced but still fail; Timm erosion is root cause. See F218.

## H413: Fix LF Override (Multi-Onset Distribution)
**Status:** RESOLVED by exp_218. MIXED — d_lf PASS; y_lf regression (VMS MID onset depletion). See F218.

## H419–H436 (architecture construction exp_219–236)
**Status:** All RESOLVED by exp_219 through exp_236 progressively. Key milestones: H419 onset-preserving (exp_219 8/18); H421 VMS MID onset (exp_220); H422 fine-sweep (exp_221 11/18); H425/H426 edy-preservation (exp_225/226 12/18); H428 qok→ch Markov (exp_228 13/18); H429 stutter (exp_229 14/18); H431 LL onset fix (exp_231 15/18); H433 differential -am (exp_233 17/18); H434 edy-conditional connector (exp_234); H435 p_stutter recal (exp_235 18/18 FIRST PERFECT); H436 global am (exp_236 19/19 MILESTONE). See F219–F236.

## H437–H440 (A-dialect generalization exp_237–240)
**Status:** All RESOLVED. H437 17/19 direct transfer (exp_237 F237); H438 erosion fix 18/19 (exp_238 F238); H439 y→y Markov 19/19 A-MILESTONE (exp_239 F239); H440 split stable 18/19 odd / 17/19 even (exp_240 F240). See F237–F240.

## H441: Erosion Factor Analytical Derivation
**Status:** open — see active backlog. (Not yet resolved.)

## H442–H460 (bigram structure exp_241–257)
**Status:** All RESOLVED. H442 bigram matrix (exp_241 F241); H443 p→sh refuted B-dialect (exp_242 F242); H444 self-succession (exp_245 overturned, F245); H445 position-filtered (exp_242 F242); H446 sh→qok Markov insufficient B (exp_243 F243); H447 ot→ot Markov superseded by bug discovery (exp_253/256); H448 ot→ot grammatical (exp_252 F252); H449 char entropy (exp_259 F259); H450 A-dialect mid bigrams (exp_254 F254); H451 section onset grammar (exp_252 F252); H452 onset trigrams (exp_247 F247); H453 trigram premise invalidated by bug (exp_248 F248); H454 p_chqok added (exp_249 F249); H455 A ch→qok NEGATIVE (exp_250 F250); H456 A qok→qok premise invalidated (exp_251 F251); H457 A ot→ot match after fix (exp_255 F255); H458 A o→o Markov (exp_258 F258); H459 B ot→ot true gap (exp_256 F256); H460 B battery with fix (exp_257 F257). See F241–F258.

## H461–H468 (character/bigram characterization exp_259–266)
**Status:** All RESOLVED. H461 A sh→qok partial closure (exp_262 F262); H462 unified persist NEGATIVE (exp_261 F261); H463 char PMI (exp_260 F260); H464 position-stratified entropy NEGATIVE (exp_263 F263); H465 A split stable (exp_264 F264); H466 B sh→qok fine sweep NEGATIVE (exp_277 F277); H467 vocabulary overlap (exp_265 F265); H468 sh→qok lag-1 only (exp_266 F266). See F260–F266.

## H471–H490 (Menzerath/word-structure exp_267–285)
**Status:** All RESOLVED. H471 Menzerath confirmed (exp_267 F267); H472 log-normal distribution (exp_278 F278); H473 sim does NOT reproduce Menzerath (exp_268 F268); H474 B split stable (exp_273 F273); H475 s→s not depleted (exp_274 F274); H476 ch/sh depletion B-specific (exp_275 F275); H477 repetition distance (exp_276 F276); H478 midfix root cause (exp_269 F269); H479 midfix LF/LL (exp_270 F270); H480 onset-conditioned midfix DISCONFIRMED (exp_271 F271); H481 within-line gradient (exp_272 F272); H482 vocabulary gap (exp_279 F279); H483 word-index conditioning (exp_282 F282); H484 MID midfix (exp_280 F280); H485 Timm rate NEGATIVE (exp_281 F281); H486 p_mf flip NEGATIVE (exp_283 F283); H487 ch/sh anti-succession OPEN; H488 LF midfix restored (exp_284 F284); H489 LL midfix NEGATIVE (exp_285 F285); H490 MID slope (exp_286 F286 ceiling reached). See F267–F286.

## H566: Gallows-Onset LF → pos1 sh Elevation — RESOLVED by exp_357
**Priority:** RESOLVED — exp_357 (F359): CONFIRMED. Gallows-LF→sh=1.72× (A) and 1.22× (B) in continuation lines. Folio-opener pos1 sh=25.6% largely explained by this rule. Also gallows→anti-ch=0.59×/0.63× discovered. k→sh=38.1% in A. New bigram rule beyond 7×7 matrix (F326).
**Status:** resolved — see F359

## H564: B-Dialect Folio-Closer pos1 Distribution — RESOLVED by exp_356
**Priority:** RESOLVED — exp_356 (F358): H564 CONFIRMED. B folio-closer pos1 sh=4.7% (E=0.49× vs cont 16.8%). Cross-dialectal anti-sh at closer pos1 confirmed. B sh "migrates" to LL (E=3.45×). B closer ch=18.6% (near-baseline, not elevated). A closer more extreme (ch E=1.34×, sh E=0.16×).
**Status:** resolved — see F358

## H563: Folio-Opener pos1 Distribution — What Onset Follows the Gallows LF Word at Folio-First Lines? — RESOLVED by exp_356
**Priority:** RESOLVED — exp_356 (F358): H563 CONFIRMED. t=0% at folio-opener pos1 (both dialects). B also p=0%, k=0% at opener pos1. A opener pos1: ch=sh=25.6% (balanced). B opener pos1: o=sh=15.1%, qok=13.7%, ch=12.3%, d=11% (diverse). Gallows excluded from pos1 (all gallows=5% A, 4% B). Cross-register ch/sh ratio gradient confirmed.
**Status:** resolved — see F358
## H562: A-Dialect Folio-Closer y→ch Onset Sequence — RESOLVED by exp_355
**Priority:** RESOLVED — exp_355 (F357): ANSWERED. ch at pos1 is general folio-closer property (E=1.34×, not y-specific). sh depleted (E=0.16×). cth=0%. ALL LF onset types show elevated ch at pos1 (y=36.8%, d=43.8%, s=45.5%). y→ch = 0.86× in continuation (below expectation). Folio-closer is anti-sh throughout.
**Status:** resolved — see F357
## H560: Folio-Closer LL Specifics — B-Dialect Folio-Last LL sh-Enrichment Driven by Formula Word? — RESOLVED by exp_354
**Priority:** RESOLVED — exp_354 (F356): ANSWERED. B folio-closer LL sh=14.6% (E=3.45×) is NOT driven by a specific formula word — all 48 LL tokens are hapax. Sh words: shckhdy, shckhar, shdy, shckhy (sh+ckhy compound class). No formula word; onset-class enrichment without lexical repetition.
**Status:** resolved — see F356

## H558: Folio-Closer Vocabulary — What Specific Words at Folio-Last LF? — RESOLVED by exp_354
**Priority:** RESOLVED — exp_354 (F356): ANSWERED. B top LF word: ol(3×), hapax=85.4%. A top LF word: ycheor(3×), ykeey(2×), hapax=80.7%. Both registers hapax-dominated (vs continuation LF=35-40%). B formula class: l/ol/ot=29.2% of LF. A formula class: y/s/ch=49.4%.
**Status:** resolved — see F356

## H557: A-Dialect Section-Specific Three-Register Grammar — RESOLVED by exp_353
**Priority:** RESOLVED — exp_353 (F355): CONFIRMED. A-dialect herbal (N=88): folio-first=75% (E=6.05×), folio-last=2.0% (E=0.16×), len_last=3.55. A-dialect pharma (N=23): 69.6% (E=3.83×), 9.1% (E=0.50×), 4.23 words. Cross-dialect distinction: A folio-closer LF = y/s/ch onset; B = ol/l/ot onset. A p-onset 0/83 confirmed.
**Status:** resolved — see F355

## H555: Does the Three-Register Line Grammar Apply Within All B-Dialect Sections Including Bio? — RESOLVED by exp_351
**Priority:** RESOLVED — exp_351 (F353): CONFIRMED. Three-register grammar section-invariant. Bio folio-first=73% gallows (E=5.35×). Folio-last SHORT (4-5 words) across all sections. Scribal layout constraint above section grammar.
**Status:** resolved — see F353
**Source:** F351 (exp_349): folio-first LF=74% gallows (both dialects). F350 (exp_348): bio section enforces ch/sh symmetry (balanced ratio). Question: within B-dialect bio folios specifically, is the folio-opener LF still gallows-enriched despite the section's balanced ch/sh structure?
**Description:** For B-dialect bio folios (f75-84), compute: (1) folio-first LF onset distribution vs bio continuation LF; (2) folio-last LF onset distribution vs bio continuation LF; (3) mean folio-last line length in bio vs herbal/cosmo. Is the folio-opener gallows formula section-independent, or does bio's ch/sh symmetry override it?
**Expected outcome:** If section-independent: bio folio-first LF still ~74% gallows. If section-modifies: bio folio-first LF has lower gallows% (bio's balanced formula prevails). The folio-opener may be a scribal/structural constraint that operates above section-level grammar.
**Cost estimate:** small — per-section folio-opener analysis
**Prerequisites:** F351, F350

## H556: y-Onset Positional Subtype Structure — RESOLVED by exp_352
**Priority:** RESOLVED — exp_352 (F354): CONFIRMED. y-onset cont-LF=yc- dominant (29-34%); cont-MID=yk-/yt- (80-85%); B folio-last LF=yk- (83%, N=6 directional); A folio-first y=0/75 (excluded). Anti-gallows constraint applies to ONSET class, not word-internal gallows.
**Status:** resolved — see F354
**Source:** F323 (exp_319): y-onset = y+gallows compound class (94% gallows at B0 in B-dialect). F326 (bigram matrix): y→y self-succession elevated (2.5-2.9×), y→d coupling elevated (1.37×). F351 (exp_349): y-onset 0.00% at folio-first LF in A-dialect (completely absent) but 22.9% at folio-LAST LF (E=1.60× vs 14.3% baseline). B-dialect folio-last: y=12.5% (E=3.17×) vs continuation 11.5%.
**Description:** For B and A dialect, compute: (1) y-onset word type frequency by position (LF/MID/LL) and compare to overall distribution; (2) y-onset word types at folio-first vs folio-last LF (is there a specific y-onset folio-closer formula?); (3) the top y+gallows compounds (ytaiin, ykaiin, etc.) — are there position-specific subtypes?
**Expected outcome:** y-onset = primarily MID/LF compound marker. At folio-last LF, y-words may function as the "anti-gallows" LF formula words — using y-onset (which is technically gallows-bearing y+gallows, but EVA 'y' is a weak gallows vs p/k/t/f). If y is not counted as "gallows" in the folio-last formula, the anti-gallows constraint may be "no p/k/t/f" rather than "no y."
**Cost estimate:** small — positional word-type analysis for y-onset
**Prerequisites:** F351, F323

## H553: Is Folio-Last Anti-Gallows LF a Line-Wide Constraint? — RESOLVED by inline analysis
**Priority:** RESOLVED: B-dialect folio-last: gallows depleted at ALL positions (LF=0.56×, MID=0.62×, LL=0.51×) — LINE-WIDE. A-dialect: LF depleted (0.33×), MID=baseline (0.95×), LL depleted (0.21×) — LF+LL constrained, MID free. B folio-last = global anti-gallows formula; A folio-last = positional (LF+LL). Added to F351 as supplemental finding.
**Status:** resolved (inline)

## H552: Bio Section sh+ckhy Compounds — RESOLVED by exp_350
**Priority:** RESOLVED — exp_350 (F352): ANSWERED. sh+ckhy pure MID (96-97%), bio+cosmo concentrated (not bio-exclusive). ch+ckhy widespread (herbal=36). bio ch/sh symmetry extends to ckhy carrier. herbal=ch+ckhy only.
**Status:** resolved — see F352
**Source:** F350 (exp_348): shckhy=4.1% and sheckhy=2.9% in bio-mixed sh-words; depleted 8.94×/6.35× outside bio. These sh+ckhy compound words are essentially bio-exclusive.
**Description:** For B-dialect bio section, characterize shckhy and sheckhy: (1) What positions (LF/MID/LL) do they appear in? (2) Are there parallel ch+ckhy words (chckhy/checkhy) in bio, and are ch+ckhy also bio-enriched? (3) What are the bigram successors of shckhy — is it sh-specific grammar? (4) Is there an A-dialect parallel?
**Expected outcome:** If bio is about bathing (balneological), sh+ckhy may be a formula for describing water or body-washing actions. shckhy may be MID-dominant (content word). Parallel: chckhy should also be bio-enriched if this is an edy-class symmetry.
**Cost estimate:** small — word-type positional analysis
**Prerequisites:** F350

## H551: Do Folio-LAST Lines Have a Different LF/LL Grammar? — RESOLVED by exp_349
**Priority:** RESOLVED — exp_349 (F351): CONFIRMED. Folio-last lines are SHORT (~4-5 words); anti-gallows LF (B=0.60×, A=0.44×); A p-onset 0/83=0.0% at folio-last LF (vs 37.3% at folio-first). B l/ol/ot LF enriched 3.4-3.9×. No LL formula. Three-register grammar confirmed.
**Status:** resolved — see F351
**Source:** F349 (exp_347): folio-first LF = gallows-onset; folio-first LL = no terminal formula. Symmetric question: does the LAST line of a folio (folio-last) show any different grammar? If the folio-opener formula is special, is there a folio-closer formula?
**Description:** For B and A dialect, classify lines as folio-last vs continuation. Compute LF onset distribution for folio-last vs continuation LF. Also compute LL onset distribution for folio-last vs continuation LL. Is folio-last LF depleted in gallows (the opposite of folio-first LF)? Does folio-last LL show the canonical LL-terminal formula more strongly (because it's the actual end of a folio)?
**Expected outcome under symmetric hypothesis:** Folio-last LF = similar to continuation LF (d/s/qok-onset). Folio-last LL = enhanced am/l-onset terminal formula (stronger LL termination to close the folio). If there's no distinction: folio-last = normal continuation line.
**Cost estimate:** small — positional analysis on folio-last-line classification
**Prerequisites:** F349, F345

## H548: Is the Folio-First Gallows Register Confined to the LF Position or Does the Entire Folio-First Line Use Gallows Words? — RESOLVED by exp_344
**Priority:** RESOLVED — exp_344 (F346): REFUTED (line-wide). LF-only one-word constraint. MID/LL at baseline gallows%. LL depleted (A: E=0.29×).
**Status:** resolved — see F346
**Source:** F345 (exp_343): folio-first LF = 67–70% gallows-onset. If the gallows bias extends to MID and LL positions of folio-first lines (not just the first word), it is a line-wide formula register. If it's LF-only, it's a single-word opener token.
**Description:** For B-dialect folio-first lines (N≈73), compute onset-class distribution at each position (LF/MID/LL). Compare gallows% at each position to the baseline continuation-line gallows%. If MID and LL on folio-first lines also show elevated gallows%, the entire first line is structurally distinct. If only LF is elevated, the formula is a one-word opener rule.
**Expected outcome:** If line-wide formula: folio-first MID gallows% > continuation MID gallows%. If one-word formula: folio-first MID ≈ continuation MID gallows% (baseline). The hapax-dominated vocabulary (F345) suggests complexity; a line-wide formula seems architecturally costly. Null: only LF position is constrained.
**Cost estimate:** small — per-position onset analysis on folio-first vs continuation lines
**Prerequisites:** F345

## H547: Is `pch-` (p+ch Compound) the Canonical Folio-Opener Word Class? — RESOLVED by exp_344
**Priority:** RESOLVED — exp_344 (F346): REFUTED. pch- B: 1.28× (mildly enriched); A: 0.59× (depleted). No specific p-subtype dominates folio-first LF. Gallows signal = p-onset class broadly.
**Status:** resolved — see F346
**Source:** F345 (exp_343): p-onset = 43.5% (B) / 37.3% (A) of folio-first LF. Top B-dialect folio-first words: pchedar, pdair, pchedain, pchedy, pcheodchy, pdsairy — majority are p+ch or p+d compound structures. A-dialect: pcheol, pchooiin, pdychoiin, pchroiin, pchodol — also p+ch dominant. The folio-opener formula may specifically require p+ch (EVA: pch = p-gallows + ch = double gallows compound).
**Description:** For B and A dialect folio-first LF words with p-onset, compute what fraction have p+ch (pch-) vs p+k (pk-) vs simple p+body (par, pol, etc.) structures. Compare to p-onset distribution in continuation-line LF. If pch- dominates folio-first p-onset words, the folio-opener formula is "pch-compound" not just "p-onset."
**Expected outcome:** Folio-first p-onset: pch- fraction >60%. Continuation p-onset: pch- fraction <40% (p-onset in continuation includes par, pol, pain, etc.). If pch- specializes for folio-opening, this is a finer-grained constraint than just "gallows-bearing."
**Cost estimate:** small — word-type analysis of p-onset folio-first tokens with substring classification
**Prerequisites:** F345

## H549: Folio-First LL Is Gallows-Depleted — RESOLVED by exp_347
**Priority:** RESOLVED — exp_347 (F349): ANSWERED (grammar-driven). B folio-first lines same length as continuation (7.67 vs 7.80). l-onset depleted at folio-first LL (E=0.15×). s/sh/y enriched (2.1-3.2×). No LL-terminal formula applied to folio-first lines. A daiin LL depleted (E=0.63×).
**Status:** resolved — see F349
**Source:** F346 (exp_344): folio-first LL gallows-depleted (B: E=0.68×, A: E=0.29×). This is the inverse of the LF enrichment. Two competing explanations: (1) folio-first lines are structurally long and end with a specific terminal formula (am, eedy) that is non-gallows; (2) folio-first lines happen to be longer on average so the LL position falls on a MID-class word rather than a true terminal.
**Description:** For B and A dialect folio-first lines: (a) compute mean and distribution of line length (word count) vs continuation lines; (b) identify top LL words on folio-first lines and compare onset-class distribution to continuation LL.
**Expected outcome:** If length-driven: folio-first lines average 8+ words, LL onset = same as MID onset profile (not true LL). If formula-driven: folio-first LL = specific words (e.g., am-class, eedy-class). The A-dialect E=0.29× is stronger than B=0.68× which may reflect A-dialect folio-first lines being consistently shorter.
**Cost estimate:** trivial — line length + LL word distribution
**Prerequisites:** F346

## H543: A-Dialect {ol,or} Body Vocabulary — Section-Specific? — RESOLVED by exp_340
**Priority:** RESOLVED — exp_340 (F342): CONFIRMED section-specific. pharma=17.88×, herbal=3.98×, cosmo=1.25× (balanced). Not uniform. Pharma most extreme. B-dialect bio=aiin-dominant (qokain=160). A-dialect bio absent (bio=B-dialect).
**Status:** resolved — see F342
**Source:** F340 (exp_338): universal template-onset shift from aiin to ol/or in A-dialect. qokol(4.72×), okol(6.96×), chol(4.74×), chor(8.98×).
**Description:** Two competing explanations: (1) A-dialect has shorter lines → fewer MID words → aiin-template words are displaced to LF and ol/or words fill MID; (2) Section-specific: A-dialect sections (herbal_A, bio) have specific ol/or formula usage. Test by checking which A-dialect sections drive the ol/or enrichment: is it uniform across sections or concentrated in bio/herbal_A?
**Expected outcome:** If section-specific: bio section drives chol enrichment (bio is consistently mixed ch+sh, F328). If line-length: A-dialect MID position gradient differs from B.
**Cost estimate:** small — per-section word type analysis
**Prerequisites:** F340

## H542: d-Onset Section Distribution — RESOLVED by exp_345
**Priority:** RESOLVED — exp_345 (F347): CONFIRMED. A d-onset aiin-dominant in all sections (herbal=37%, text=37%). ch-onset ol/or-dominant in herbal (23%) and text (14%). d/template divergence is section-invariant. B ch edy-dominant cross-section (0-4% ol+or).
**Status:** resolved — see F347
**Source:** F340: d-onset does not shift to ol/or; daiin is dominant in A-dialect. The contrast with template onsets (which DO shift) is a marker of the d-onset vs template-onset functional distinction.
**Description:** For A-dialect, compute d-onset top body forms per section. Compare to template onset (ch) body forms per section. Does d-onset show aiin-dominance consistently across all sections while ch shows ol/or dominance? Or is the divergence section-specific?
**Expected outcome:** d-onset: daiin dominant in all A-dialect sections. ch-onset: chol/chor dominant in bio/herbal; cheey dominant in other sections. Confirms: d-onset is functionally distinct (content-MID) while ch/sh are section-conditioned template words.
**Cost estimate:** small
**Prerequisites:** F340

## H541: A-Dialect d-Onset LL Enrichment — RESOLVED by exp_339
**Priority:** RESOLVED — exp_339 (F341): CONFIRMED. A daiin LL=1.37× (explains F339 aiin LL=1.225×). INVERSION: B daiin LF=2.57× (formula), A daiin LL=1.37× (content). A d-onset broadly LL-enriched (dar=1.67×, dal=2.30×, dam=3.68×). B d-onset: daiin/dain=LF-formula, dal/dam=LL-terminal only.
**Status:** resolved — see F341 — Does daiin Appear at LL in A-Dialect (aiin LL_enr=1.225×) Because A-Dialect d+aiin Serves Both MID and LL Functions?
## H546: B-Dialect daiin Section Distribution — RESOLVED by exp_341
**Priority:** RESOLVED — exp_341 (F343): CONFIRMED. B-dialect daiin LF NOT bio-driven: pharma=4.68×, text=3.58×, bio=1.57× (weakest). A-dialect herbal drives LL enrichment (1.50×, N=326). A pharma=near-baseline (0.85×) despite extreme ol/or dominance (F342). A-dialect pharma = most distinctive grammar section.
**Status:** resolved — see F343 — Is the daiin LF=2.57× Enrichment Driven by One Section (e.g., Bio) or Uniform?
## H545: A-Dialect Cosmo Section — RESOLVED by exp_346
**Priority:** RESOLVED — exp_346 (F348): ANSWERED. Cosmo = f86v5 (cosmological rosette, N=344). Diagram-label grammar: y=17.7% (2.97× herbal), ot=11.0%, ch=7.3% (0.35×). Balanced ratio = artifact of low-N template onsets + bare "aiin" words (onset=other). Not a genuine prose-section comparison.
**Status:** resolved — see F348
**Source:** F342 (exp_340): A-dialect cosmo ratio=1.25× vs pharma=17.88×, herbal=3.98×. Cosmo is the only balanced A-dialect section.
**Description:** Examine A-dialect cosmo section word vocabulary. Is it possible that cosmo uses a different onset class (not ch/sh/qok/ok) or that the section has unusual structural properties (circular text, astronomical glyphs)?
**Expected outcome:** Cosmo section may have fewer template-onset words overall and more gallows-onset words (consistent with astronomical context). The {ol,or}/{aiin,ain} balance may reflect low template-onset usage rather than specific {aiin,ain} preservation.
**Cost estimate:** trivial — word-type frequency for cosmo section
**Prerequisites:** F342

## H544: B-Dialect daiin as Paragraph-Opening Formula — RESOLVED by exp_342
**Priority:** RESOLVED — exp_342 (F344): REFUTED (folio opener). daiin AVOIDS folio-first lines (0/73=0%). Continuation-line LF formula (87/2316=3.8%, E≈2.97×). A-dialect same. daiin = mid-folio continuation formula, not opener.
**Status:** resolved — see F344
**Source:** F341 (exp_339): B-dialect daiin LF=33%, E=2.57×. Is this driven by paragraph-opening lines, where the first word of the paragraph (LF of first line) is more likely to be daiin?
**Description:** For B-dialect, classify lines as paragraph-first vs paragraph-continuation. For each class, compute daiin LF%. If daiin is enriched at paragraph-opening LF specifically (not just any LF), it's a paragraph opener. Compare P(daiin|para-LF) vs P(daiin|non-para-LF).
**Expected outcome:** If paragraph opener: daiin LF% in paragraph-first lines = 40-50%, vs daiin LF% in continuation lines = 20-25%. If uniform LF enrichment: both ~33%.
**Cost estimate:** small — requires paragraph boundary detection from locus codes
**Prerequisites:** F341

## H540: 'eey' Terminal Template — Is 'eey' LF/LL-Concentrated Relative to 'edy'/'eedy' in A-Dialect? — RESOLVED by exp_337
**Priority:** RESOLVED — exp_337 (F339): REFUTED. eey is the MOST LL-depleted (0.427×/0.346×). All e-body templates LL-depleted. am=sole LL-terminal. deey=100% LF in B (E=7.80×). A-dialect aiin LL-enriched (1.225×) = new finding. eey universality = MID distribution breadth, not terminal function.
**Status:** resolved — see F339
**Source:** exp_333 (F335): eey achieves 7/7 onset coverage in A-dialect (vs 6/7 in B). edy/eedy are the dominant template forms in B-dialect; A-dialect shifts toward eey/ey.
**Description:** For each onset class (qok, ok, ot, d, s, ch, sh), compare LF+LL fraction vs MID fraction for 'eey' vs 'edy'/'eedy'. If eey is a terminal template form, it should be concentrated at LF or LL relative to edy/eedy. Compute: P(LF|eey), P(MID|eey), P(LL|eey) for each onset class, contrasted with P(LF|edy), P(MID|edy), P(LL|edy). Cross-dialect: is the A-dialect 7/7 coverage of eey driven by eey appearing at different positions than B?
**Expected outcome under template-terminal hypothesis:** eey is LL-concentrated (LL > LF > MID); edy/eedy are MID-concentrated. This would explain A-dialect universal coverage: eey = template line terminal, every onset class uses it.
**Cost estimate:** small — positional analysis of template word types
**Prerequisites:** F335 (eey coverage); corpus parsing with position classification (LF/MID/LL)

## H539: ch→qok Enrichment — Is ch→qok Elevated Cross-Dialect Like sh→qok (E=1.97×/1.74×)? — RESOLVED by exp_334
**Priority:** RESOLVED — exp_334 (F336): REFUTED. ch→qok B=1.147×, A=0.877× (near-baseline/depleted). sh→qok=1.967×/1.741× is sh-specific. No general "TEMPLATE→qok" rule. A-dialect ch→qok actively depleted. d→qok=0.591× B (anti-gradient, confirmed). ch vs sh bigram profiles diverge fundamentally despite both being template-dominant.
**Status:** resolved — see F336
**Source:** F326 (bigram matrix): sh→qok elevated (1.97×/1.74×). ch is also a template class. If ch→qok is similarly elevated, both are covered by a single "TEMPLATE→qok" grammar rule, simplifying the architecture.
**Description:** From the exp_324 bigram matrix data, extract ch→qok enrichment values for B and A dialects. Compare to sh→qok. If ch→qok is also elevated (E>1.3×), the rule is "template-class → qok" not "sh → qok" specifically. Also check ch→sh and sh→ch asymmetry within the same matrix.
**Expected outcome under single-rule hypothesis:** ch→qok E=1.3-2.0× cross-dialect. If so, one rule covers both. If ch→qok is NOT elevated, sh→qok is a class-specific rule (requiring separate p_sh_qok parameter).
**Cost estimate:** trivial — data already in exp_324 output; this is a re-analysis
**Prerequisites:** exp_324 (bigram matrix)

## H538: ch-Onset Body-Class MID Position Split — Do chol/char/chor Appear Later in MID Span Than chedy/cheedy? — RESOLVED by exp_335
**Priority:** RESOLVED — exp_335 (F337): PARTIALLY CONFIRMED with reversal. A-dialect ch: 'a'-body LATER (z=+2.04, a_mean=0.557 vs e_mean=0.474). B-dialect ch: NS (z=−0.54, N=74 small). REVERSAL: B-dialect sh 'a'-body EARLIER (z=−2.19, shar=0.153 = early-formula). Body-class position split is gradient-dependent: early-MID onset (sh) → 'a'-body early; late-MID onset (ot) → 'a'-body late; ch = dialect-split (A: late-content, B: mixed).
**Status:** resolved — see F337
**Source:** F331 (exp_329): ot+'a'-body words significantly later than ot+'e'-body words (z=2.67σ). ok+'a'-body not significantly split (z=0.75). ch has bimodal body structure: 'e'-body (edy/eedy) vs 'a'-body (chol/char). The same split should be testable for ch.
**Description:** For B and A dialect, compute mean normalized MID position for ch+'e'-body words (chedy, cheedy, cheey) vs ch+'a'-body words (chol, char, chor, chaiin). Test z-score for the split. Compare to ot result (z=2.67σ). Also compute for sh. If ch+'a'-body is significantly later, this generalizes: template-onset 'a'-body words appear later in MID span than same-onset 'e'-body words.
**Expected outcome:** ch+'a'-body mean position ≈ 0.52-0.56 (between ok and d positions); ch+'e'-body mean position ≈ 0.47-0.49 (at ch class mean). z>2σ expected given larger N for ch (ch total=2447 vs ot=999).
**Cost estimate:** small — extends exp_329 analysis to ch/sh onset classes
**Prerequisites:** F331 (gradient), exp_329 (positional analysis framework)

## H537: ch+'ol'/'or' A-Dialect Enrichment — Are chol/chor Specifically Enriched Beyond Overall ch 'a'-Body Increase? — RESOLVED by exp_338
**Priority:** RESOLVED — exp_338 (F340): CONFIRMED and EXTENDED. chol(4.74×), chor(8.98×), but also universal: ALL template onsets shift from {aiin,ain} to {ol,or} in A-dialect. qokain=0.09×, okain=0.15× (extreme depletion). d-onset does not shift. Universal A-dialect body vocabulary reorganization: template onsets use ol/or; d-onset uses aiin.
**Status:** resolved — see F340
**Source:** F335 (exp_333): ch 'a'-body B=6.2%, A=28.0% (4.5× enrichment). But chol=65→209 (3.2×) and chor=25→126 (5×). Is the A-dialect enrichment uniform across all 'a'-body forms, or is {ol, or} specifically enriched?
**Description:** Compute per-body-form enrichment ratios: (A_count/A_total) / (B_count/B_total) for each ch+'a'-body form (chol, chor, char, chaiin, chain, char). Rank by enrichment ratio. Test whether {ol, or}-body forms are significantly more enriched than {aiin, ain, ar}-body forms in A-dialect. If yes, A-dialect ch specifically develops a ch+{ol,or} = content function distinct from B-dialect.
**Expected outcome:** chol: A=209/1458 vs B=65/2447 → rate ratio ≈ 5.4×. chor: 126/1458 vs 25/2447 → rate ratio ≈ 8.5×. chaiin: 24/1458 vs 7/2447 → rate ratio ≈ 5.8×. All ratios roughly similar → uniform enrichment. If ol/or are specifically elevated 3-5× above aiin/ar, there's a body-specific rule.
**Cost estimate:** small — rate-ratio analysis of F335 doublet table
**Prerequisites:** F335

---

## H536: ch/sh Body Doublets — Do ch and sh Fully Participate in the 7-Body Doublet System? — RESOLVED by exp_333
**Priority:** RESOLVED — exp_333 (F335): CONFIRMED. All 7 onset classes produce all 7 core body forms. ch/sh: 7/7 for aiin/ain/ar/al/ol/or in both dialects; 5-6/7 for air and am. ch/sh are template-dominant (B: 5-6% 'a'-body; A: 21-28%). d is content-dominant (64%). chol=65/209 B/A; chor=25/126 B/A. 'eey' achieves 7/7 onset coverage in A-dialect. The doublet system extends to a complete 7-onset × 7-body architecture.
**Status:** resolved — see F335
**Source:** F333 (5-onset doublet system); exp_333 (extends to ch/sh)

## H535: Onset-Substitution Doublets MID Position — RESOLVED by exp_332
**Priority:** RESOLVED — exp_332 (F334): CONFIRMED (moderate). B: 17/28 (60.7%) gradient-consistent; A: 15/22 (68.2%). Both above 50% chance. A-dialect 'aiin' 4/4 perfect. All 7 bodies show ranges exceeding class-level gradient prediction (0.097). ot+body consistently latest; qok+ok+body earliest. A-dialect saiin exceptionally late (0.827, N=14 — anomaly).
**Status:** resolved — see F334
**Source:** F331 (gradient), F333 (doublet system)

## H534: MID Position Gradient and Bigram Grammar Correspondence — RESOLVED by exp_330
**Priority:** RESOLVED — exp_330 (F332): CONFIRMED (moderate). 73% B-dialect / 68% A-dialect gradient-consistent vs 50% chance. Self-succession E positively correlates with gradient position. B-dialect s→s=0 (zero adjacent s-onset bigrams). ch↔sh avoidance overrides gradient (both directions depleted). Strong forward pairs: sh→qok (1.64×), qok→s (1.83×), sh→y (1.60×). Strong backward depletions: d→qok (0.49×).
**Status:** resolved — see F332
**Source:** F331 (onset gradient: sh<y/ch<qok<ok<d<ot); F326 (bigram matrix with sh→qok 1.97×, y→y 2.49×, ok→ok 1.32×).
**Description:** For each enriched bigram pair (sh→qok, sh→d, ok→ok, y→d, qok→s), check directionality: is the FORWARD direction (early→late in gradient) more enriched than BACKWARD? Compute E(o1→o2) vs E(o2→o1) for all pairs. If forward direction is systematically stronger, the gradient has directional grammar.
**Expected outcome:** sh→qok enriched, qok→sh depleted. y→d enriched (y is mid-MID, d is late-MID = forward). ok→ok is self-succession (no direction). The gradient encodes a general "left-to-right" directionality for onset class transitions.
**Cost estimate:** small — uses existing bigram data from exp_324; cross-reference with F331 gradient
**Prerequisites:** F326 (bigram matrix), F331 (position gradient)

## H533: Onset-Body Overlap Gradient — RESOLVED by exp_331 (F333)
**Priority:** RESOLVED — exp_331 (F333): CONFIRMED. Complete 5-onset × 7-body doublet system: qok/ok/ot/d/s ALL produce words for {aiin,ain,ar,al,ol,air,or} at 5/5 onset classes. Onset character encodes gradient position, not body vocabulary access. 'a'-body fraction gradient: d=73%, ok=43%, qok=36%.
**Status:** resolved — see F333
**Source:** F330 (ok+'a'=43.2%), F323 (qok B0='a'=36%, d B0='a'=73%), F327 (s B0='a'=63%).
**Description:** For each of the 5 "aiin-capable" onset classes (qok, ok, ot, d, s), extract top-20 MID word types. Construct the body inventory overlap table: for each body (aiin, ain, ar, al, ol, air, am), show which onset classes have the onset+body word in their top-20. Count how many onset classes share each body. Expected: the core body inventory (aiin, ain, ar, al) is shared by ALL 5 onset classes — every onset class has qok/ok/ot/d/s+aiin in its type inventory.
**Expected outcome:** All 5 onset classes share the 6-word body vocabulary {aiin, ain, ar, al, ol, air}. The onset character ('qok', 'ok', 'ot', 'd', 's') can substitute for any other in front of these bodies. The 'a'-body fraction varies by onset class (d=73%, qok=36%) due to different rates of 'e'-body template usage.
**Cost estimate:** small — cross-onset word-type table
**Prerequisites:** F323, F327, F330

## H532: ok+'e'-Body vs ok+'a'-Body MID Position Distribution — RESOLVED by exp_329
**Priority:** RESOLVED — exp_329 (F331): PARTIALLY CONFIRMED. ok sub-class split not significant in B-dialect (z=0.75); ot sub-class split significant (z=2.67σ, ot+'a' later than ot+'e'). MAJOR BONUS: onset-class MID position gradient discovered: sh(0.42)<y/ch/qok(0.48-0.49)<ok(0.50)<s/d(0.53-0.56)<ot(0.59). Three tiers: (1) early-MID: sh; (2) mid-MID: y/ch/qok/ok; (3) late-MID: d/ot/s. Cross-dialect invariant. ok+'e'≈qok position; ok (all) intermediate between qok and d.
**Status:** resolved — see F331
**Source:** F330 (ok compound class); prior findings on position-conditioned onset distributions (F293 I(onset;pos)=7.8%).
**Description:** For B-dialect MID words, classify ok words by B0 ('e' vs 'a') and compute mean MID position for each sub-class. Compare to: (a) qok mean MID position (expected: similar to ok+'e'), (b) d-onset mean MID position (expected: similar to ok+'a'). If the distributions are statistically different, ok is a position-differentiated compound class.
**Expected outcome:** ok+'e'-body mean position ≈ qok mean position; ok+'a'-body mean position ≈ d-onset mean position. The bimodal B0 corresponds to a bimodal position distribution.
**Cost estimate:** small
**Prerequisites:** F330

## H531: qok 'a'-Body Forms (qokain, qokaiin) — RESOLVED by exp_331
**Priority:** RESOLVED — exp_331 (F333): CONFIRMED. Complete 5-onset × 7-body doublet system: qok/ok/ot/d/s all produce words for {aiin,ain,ar,al,ol,air,or} (5/5 coverage for all 7 bodies, B and A). qok+'a' top doublets: qokain/dain, qokaiin/daiin, qokal/dal, qokar/dar. 10/15 top qok+'a' words have d-analogues. Onset character encodes gradient position; body vocabulary is universal.
**Status:** resolved — see F333
**Source:** F330 (ok+'a'=d-substitutes); F323 (qok B0='a'=36%, top qok 'a' words are qokaiin/qokain/qokal/qokar).
**Description:** Extract qok top-30 word types. Partition into 'e'-body and 'a'-body. For 'a'-body words: are they identical to d-onset body forms? (qokaiin body = 'aiin', daiin body = 'aiin' — YES by definition if they share bodies). Check if d-onset doublets appear at similar or different rates in qok vs d: is qok 'a'-body usage (36%) proportional to overall qok usage relative to d? Is qokaiin enriched or depleted at any specific sections/positions?
**Expected outcome:** qok+'a'-body words ARE the aiin-body paradigm with qok onset. qokaiin (197 B), qokain (221 B) are among the most frequent MID words overall — they're the qok-substituted aiin forms.
**Cost estimate:** very small — word-type table already in data from exp_324 context
**Prerequisites:** F323, F330

## H530: Folio/Paragraph ch-Heavy vs sh-Heavy Specialization — RESOLVED by exp_348
**Priority:** RESOLVED — exp_348 (F350): ANSWERED. Two mechanisms: (1) Bio section enforces ch/sh symmetry via ch+edy↔sh+edy parallel (10 folios 0.437-0.571); bio-specific shckhy/sheckhy compounds. (2) Ch-dominant sections: ch expands to ol/aiin body vocabulary (cheody, chol) while sh remains edy-class. Scribe hand not directly tested.
**Status:** resolved — see F350
**Source:** exp_326 (F328): 15 ch-dominant folios (herbal/pharma/stars_text); 0 sh-dominant; bio consistently mixed.
**Description:** For the 15 ch-dominant folios: (1) What are the most frequent MID words on ch-dominant vs mixed folios? (2) Is the ch-dominance driven by specific paragraph-opening ch-words (first MID position)? (3) Cross-check with known scribe hand assignments: do ch-dominant folios cluster in specific hand regions?
**Expected outcome:** ch-dominance may reflect hand/scribe preference (different scribes favor different template onset classes) or section-specific paragraph formulae.
**Cost estimate:** small-medium
**Prerequisites:** exp_326 (F328)

## H529: B-Dialect Bidirectional ch↔sh Avoidance — Is A-Dialect Asymmetry (sh→ch Only) Due to Lower sh Frequency? — RESOLVED by exp_336
**Priority:** RESOLVED — exp_336 (F338): CONFIRMED. A-dialect ch→sh E=0.954 is NOT a power artifact. Min detectable E=0.890 at 80% power; z(A vs B) = 2.1-2.4σ (significant). A-dialect unidirectional ch↔sh rule is genuine (sh→ch only, E=0.742). B-dialect bidirectional rule is B-specific. Ancestral rule: sh→ch. B-dialect adds ch→sh direction.
**Status:** resolved — see F338
**Source:** exp_326 (F328): A-dialect ch→sh mixed-line E=0.954 (near 1.0) vs sh→ch E=0.742.
**Description:** Power analysis: given 252 mixed A-dialect lines with ch+sh MID words, and the observed mixed-line counts, what is the minimum detectable E at 80% power for ch→sh? If the expected count is too small (<5-10), the near-1.0 result may simply reflect noise. Compare A-dialect sh→ch to B-dialect sh→ch (0.661×) — if both are ~0.67-0.74×, the mechanism is consistent. Then ch→sh difference (B=0.678, A=0.954) is the actual asymmetry to explain.
**Expected outcome:** Power analysis shows A-dialect ch→sh mixed-line obs=90 with exp=94.3 → near-1.0 may be genuine. If so, A-dialect truly lacks the ch→sh grammatical rule while B-dialect has it — B-dialect strengthened the avoidance to bidirectional.
**Cost estimate:** small — statistical power calculation + recheck
**Prerequisites:** exp_326 (F328)

## H528: ok-Onset Body Structure and A/B ok↔qok Coupling — RESOLVED by exp_328
**Priority:** RESOLVED — exp_328 (F330): CONFIRMED. ok = compound onset class: ok+'e'-body = qok-'q' substitutes (okeedy/qokeedy, okedy/qokedy, okeey/qokeey); ok+'a'-body = d-onset doublets (okaiin/daiin, okain/dain, okar/dar, okal/dal). B0 bimodal: 'e'=43.4%, 'a'=43.2%. ot-onset structurally isomorphic (e=42.6%, a=36.3%). A-dialect ok: 'a'-body shrinks (24.3%), 'o'-body grows (17.6%); ok↔qok coupling (2.03×/1.68×) is class-level, driven by ok+'e'-template words; absent in B (E≈1.0×).
**Status:** resolved — see F330
**Source:** exp_321 (F323): ok B0 bimodal ('e'=43.5%, 'a'=43.3%); exp_324 (F326): A-dialect ok↔qok coupling (2.03/1.68×).
**Description:** Extract top-30 ok-onset MID word types for B and A. Partition by B0 character: ok+'e'-body types vs ok+'a'-body types. Are they structurally different? In B-dialect, ok+e words could be okeedy/okeey (template-copying) and ok+a words could be okaiin/okain (aiin-body like d-onset). Are the B0='e' and B0='a' ok-onset words in different sections or positions? A-dialect: is the ok↔qok coupling explained by specific ok-word types that tend to precede qok-words?
**Expected outcome:** ok+'e' words: okeedy, okeey, okeol (template forms); ok+'a' words: okaiin, okain, okar, okal (aiin-body forms, doublets with daiin/dain/dar/dal). This would make ok a compound onset class: partly template-copying (ok+'e') and partly aiin-doublet (ok+'a').
**Cost estimate:** small — word-type analysis
**Prerequisites:** exp_321 (F323), exp_324 (F326)

## H527: ch↔sh Mutual Avoidance — Section-Level vs Grammar-Level Mechanism
**Priority:** RESOLVED — exp_326 (F328): ANSWERED. Dual mechanism. Section segregation: ch dominant in ALL sections (no sh-dominant section), not the primary explanation. Within-mixed-line B-dialect: E=0.67 (avoidance persists = GRAMMATICAL RULE). Global vs mixed-line decomposition: global E=0.47 → mixed-line E=0.67; folio clustering explains 0.47→0.67, sequential grammar accounts for E=0.67 residual. A-dialect asymmetric: ch→sh normalizes (E=0.954) but sh→ch persists (E=0.742). B-dialect = bidirectional grammatical avoidance; A-dialect = unidirectional (sh→ch only). B-dialect mixed lines: sh-before-ch arrangement most common (48.7% vs 29.3%).
**Status:** resolved — see F328
**Source:** exp_324 (F326): B-dialect ch→sh = 0.567×, sh→ch = 0.555× (bidirectional avoidance); A-dialect ch→sh = 0.731× (weaker but similar direction).
**Description:** (1) Compute section-level ch and sh onset frequencies: in which sections (herbal/pharma/astro/bio/cosmo/stars/text) does ch appear at high rate? Does sh? If they're in different sections, section clustering explains the avoidance. (2) For WITHIN-LINE analysis: among lines that contain at least one ch-onset AND at least one sh-onset word, compute the bigram enrichment within those lines. If the avoidance persists within mixed-onset lines, it's a grammar rule not a section artifact. (3) Compare ch→sh vs ch→other depletion: is it specifically sh that ch avoids, or does ch depleted towards all template classes? Similarly for sh.
**Expected outcome under section-clustering:** Lines that mix ch and sh onset words show no bigram depletion (E≈1.0×); the avoidance is entirely explained by section-level segregation. Under grammar rule: even in mixed lines, ch-words avoid following sh-words and vice versa.
**Cost estimate:** medium — requires section classification + within-line bigram extraction
**Prerequisites:** exp_324 (F326: bidirectional avoidance measured)

## H526: y→d Coupling — RESOLVED by exp_327
**Priority:** RESOLVED — exp_327 (F329): CONFIRMED class-level grammar rule. B=17 bigrams=17 unique pairs (T/T=1.0); A=37 bigrams=37 unique pairs (T/T=1.0); Jaccard=1.9%. d-words following y prefer variant forms (dar/dol/dain) over daiin (near baseline or depleted). A-dialect: y→ch/sh depleted (0.69×), y→d enriched (1.38×) — A shows asymmetric coupling profile (content vs template classes). Simple Markov p_y_d parameter adequate for simulation.
**Status:** resolved — see F329
**Source:** exp_324 (F326): y→d enriched 1.37/1.38× cross-dialect. N=17 (B), N=37 (A).
**Description:** Extract all y→d adjacent MID bigrams for B and A dialects. (1) Which y-words precede d-words? Are they y+k forms, y+t forms, or mixed? (2) Which d-words follow y-words? Are they daiin/dar/dal (top-3 d-words) or more diverse? (3) Compute per-y-word P(→d) vs class rate. (4) Cross-dialect: do A and B share the same y×d pairs?
**Expected outcome:** y→d follows the class-level pattern (not specific pairs), analogous to sh→qok. y+k and y+t words both transition to d-onset words in proportion to their frequency; daiin is the most common d-word following y-onset words.
**Cost estimate:** small — bigram analysis similar to exp_323
**Prerequisites:** exp_322 (y+gallows), exp_325 (d = daiin-dominated), exp_324 (y→d coupling measured)

## H525: Template Class Succession Matrix — RESOLVED by exp_324
**Priority:** RESOLVED — exp_324 (F326): ANSWERED. Five cross-dialect elevated invariants: y→y(2.49/2.85×), sh→qok(1.97/1.74×), ok→ok(1.32/1.96×), y→d(1.37/1.38×), qok→s(1.36/1.39×). One cross-dialect depletion: sh→ch(0.555/0.565×). B-dialect: ch→sh also depleted (0.567×) = bidirectional ch↔sh mutual avoidance. A-dialect: qok↔ok bidirectional coupling (2.03/1.68×), sh→sh elevated (1.31×), qok→qok elevated (1.75×).
**Status:** resolved — see F326
**Source:** exp_323 (F325): sh→ch depleted 0.555×/0.565× in both dialects — NEW structural invariant.
**Description:** For B and A dialect MID bigrams, compute E(onset1→onset2) = obs/exp for all major onset-class pairs (qok, ch, sh, d, y, ok, s as both onset1 and onset2). Compute expected under independence (P(onset1) × P(onset2) × N_bigrams). Generate a 7×7 matrix of enrichment values for each dialect. Identify: (a) systematically elevated pairs (E>1.3×, both dialects); (b) systematically depleted pairs (E<0.7×, both dialects); (c) cross-dialect differences (elevated in B not A, or vice versa). Focus on template classes (ch/sh/ok/ot/qok) — are there mutual avoidance rules between template classes?
**Expected outcome:** Known from prior experiments: qok↔ch enriched (~1.15-1.20× in both); sh→qok enriched (1.74-1.97×); sh→ch depleted (0.555-0.565×). Prediction: ch→sh also depleted (mutual avoidance); ch→ch self-succession depleted (VMS data, prior exp_299/F301 measured sim, not VMS); ok→qok and ot→qok may be enriched (template-class coupling); d→ch enriched or depleted?
**Cost estimate:** small — extends exp_323 to full bigram matrix
**Prerequisites:** exp_323 (F325: sh→ch depletion discovered)

## H524: s-Onset Body Structure — RESOLVED by exp_325
**Priority:** RESOLVED — exp_325 (F327): CONFIRMED. s-onset and d-onset are onset-substitution doublets (same body vocabulary). Top s-words: saiin(20.4%), sain(10.9%), sar(8.8%), sol(8.0%), sal(7.3%). 10/20 top s-words have d-analogues in top-20 d-words. d/s ratio: B=4.9×, A=7.5×. A-dialect s uses more 'o'-body forms. Jaccard A/B=0.095.
**Status:** resolved — see F327
**Source:** exp_321 (F323): s-onset B0='a'=62.8% (B), 37.1% (A); B1='i'=40.1% (B), 28.7% (A); similar pattern to d-onset.
**Description:** Extract top-30 s-onset MID word types for B and A dialects. Compute s-onset body character sequence B0-B3 (from exp_321 data: B: a=63%, i=40%, i=33%, n=41% — already measured). Compare to d-onset: are the body sequences statistically similar? Measure s-onset closed paradigm size (CP90 ratio). Cross-dialect: A-dialect s-onset has B0='a'=37% vs B=62.8% (less 'a'-concentrated); B1='i'=28.7% vs B=40% — does A-dialect s-onset show weaker aiin constraint? If s-onset ≈ d-onset in body structure, they represent parallel onset classes with the same body template but different onset characters.
**Expected outcome:** Top s-onset types: saiin, sein, sain, sal, sar, sol, sor, sedy. Saiin/sain dominant but less concentrated than daiin for d-onset (because s B0='a'=63% vs d B0='a'=73%). A-dialect s-onset less aiin-concentrated than B (consistent with weaker 'a' at B0 in A).
**Cost estimate:** small — word-type frequency analysis
**Prerequisites:** exp_321 (F323: s-onset B0='a' similarity to d-onset observed)

## H523: y+Gallows Compound Structure — RESOLVED by exp_322
**Priority:** RESOLVED — exp_322 (F324): CONFIRMED. 94.1% (B) / 92.7% (A) y-onset MID words are y+gallows compounds. Gallows rank: k(44%)>t(36%)>p(7%)>ch(5%)>f(2%). B0='c'=4.6% from exp_321 = entirely ch compound (bare c=0%). A/B suffix split: B uses -eedy/-edy; A uses -ol/-or/-al. y+ch concentrates at LF positions (13.6% all vs 4.6% MID). Triple compounds y+p/f+ch confirmed. Jaccard A/B=0.193.
**Status:** resolved — see F324
**Source:** exp_321 (F323): y-onset B0 = gallows discovery. Gallows rank at B0: k=44%, t=36%, p=7%, c=5%, f=2%.
**Description:** Extract top-30 y-onset MID word types for B and A dialects. For each, parse as y(onset)+body and identify: (a) whether body[0] is gallows; (b) full word structure. Compute: total y-onset MID token count vs words with gallows-body; fraction where body[0] ∈ {k,t,p,f} vs {ch} (c at B0 = ch or bare c?); y+gallows sub-inventory by gallows type (yk-words, yt-words, yp-words, ych-words). Cross-dialect: which y-words are shared A/B vs dialect-exclusive?
**Expected outcome:** Top y-onset word types are ykaiin, ytaiin, ykaiin variants, ychaiin, ychedy, etc. All have gallows at position 1. 'c' at B0 = 'ch' (compound gallows) for most occurrences. A and B dialects share the y+gallows structure but differ in specific gallows+body combinations (A: more yt-ol forms; B: more yk-aiin forms — speculative).
**Cost estimate:** small — word-type frequency analysis
**Prerequisites:** exp_321 (F323: y-onset B0 = gallows discovery)

## H522: sh→qok Bigram Word-Level Analysis — RESOLVED by exp_323
**Priority:** RESOLVED — exp_323 (F325): Q004 CLOSED. Class-level grammar rule (scenario b/a hybrid). Most sh-words cluster near class rate (0.267 B / 0.096 A). Top pair shedy→qokedy=16 occurrences (4.7% of bigrams). Cross-dialect pair overlap=5/257 pairs (2.4%) — proves class-level not lexical. NEW FINDING: sh→ch depleted 0.555×/0.565× in BOTH dialects (structural invariant). A-dialect sh→sh=1.312× (elevated) vs B 0.937×. B-dialect sh→qok enrichment is passive copy-buffer mechanism.
**Status:** resolved — see F325
## H521: Body Character Distribution by Onset Class — RESOLVED by exp_321
**Priority:** RESOLVED — exp_321 (F323): ANSWERED. Four structural discoveries: (1) d-onset body B0-B3 = a+i+i+n (daiin template character by character; a=73% at B0, i=40% at B1, i=42% at B2, n=49% at B3); (2) y-onset B0 = 80% gallows characters (k+t=79-81%): y-onset is y+gallows compound class, explaining its LF grammar-word role; (3) A-dialect ch/sh B0 = 'o'-primary (48%, 45%) vs B-dialect 'e'-primary (60%, 73%): character-level dialect marker; (4) No categorical character boundary — distributional not categorical onset separation.
**Status:** resolved — see F323
**Source:** exp_320 (F322): d-onset most constrained onset class at B0-B3; y-onset B1 entropy lowest in B-dialect at position B1.
**Description:** For each major onset class, compute full character frequency distribution at body positions 0-3 (not just entropy). (1) For d-onset: what is P(char | d-onset, B0), P(char | d-onset, B1), P(char | d-onset, B2), P(char | d-onset, B3)? (2) For y-onset: what dominates at B1 in B-dialect (where entropy=2.216)? (3) For ch-onset (highest entropy): what is the distribution at B0-B3 — is it truly flat? (4) Cross-onset comparison: which characters appear EXCLUSIVELY in one onset class's body at B0-B2 (would prove character-level morphological gating)? (5) A-dialect comparison: does d-onset show tighter character gating in A (consistent with lower entropy there)?
**Expected outcome:** d-onset B0 dominated by 'a' (from daiin structure → d + a + iin → body[0]='a'). y-onset B1 dominated by 'a' (y + a + iin → body[0]='a', body[1]='i' or 'o'?). ch-onset B0-B1 will have multiple frequent characters (e, a, o) with none dominant above ~30%.
**Cost estimate:** small — extends exp_320 with character frequency tables instead of entropy only
**Prerequisites:** exp_320 (F322: body entropy profile characterized; positions of interest identified)

## H502: Text-Section Paradigm Expansion — RESOLVED by exp_298
**Priority:** RESOLVED — exp_298 (F300): REFUTED (register mixing). Text sub-sections individually need 32-38 qok types (bio-sized 14-15 would confirm mixing); per-folio TTR text=0.350, bio=0.218 for qok (1.6×). qok/sh expansion is genuine within-folio diversity; ok/ot expansion is Zipfian accumulation.
**Status:** resolved — see F300

## H500: daiin Structural Dominance — RESOLVED by exp_296
**Priority:** RESOLVED — exp_296 (F297): daiin is position-neutral (LF/MID=0.96×), appears in 102/104 d-onset folios, concentrated in A-dialect (32.5% of A-d vs 21.7% of B-d). Dominance is mechanistic: convergence of d→-aiin constraint × ZeroMid template mode × d-onset frequency. Three-way sub-structure within d-onset (plain templates/gallows-compound LF-enriched/dam LL-specialized).
**Status:** resolved — see F297

## H501: B-Dialect Closed Paradigm Section Stability — RESOLVED by exp_297
**Priority:** RESOLVED — exp_297 (F298): PARTIALLY CONFIRMED. Stable universal core (bio: 100% overlap with global 90%-set) plus section-specific periphery (text: 64-74% overlap, 2.6× larger sets). Two-tier paradigm structure identified. H502 generated.
**Status:** resolved — see F298

## H499: Sparse-Template Onset Positional Grammar — Do qok/ok/ot (Sparse-Midfix) Show Stronger Positional Grammar Than ch/y (Rich-Midfix)?
**Priority:** RESOLVED — exp_293 (F294): Both sparse and rich onset classes show positional specificity, but in OPPOSITE DIRECTIONS. Sparse classes (qok/ok/ot) are MID-concentrated; rich classes (p/y/s/t) are LF-concentrated. All onset classes are position-specific. Zero-midfix rate does NOT predict direction of positional preference (d-onset: ZeroMid=59.8% but LF-enriched 3.1×).
**Status:** resolved — see F294
**Source:** exp_293

---

## H511: Line-Length-Conditional p_blind — RESOLVED by exp_309
**Priority:** RESOLVED — exp_309 (F311): PARTIALLY CONFIRMED. cond_mild (p_short=0.060/p_long=0.180) achieves 19/19 PASS, menz_r=−0.137 (61%, +26%), r_ll=−0.034 (15%). Battery fails at p_long≥0.25 (am_ll inflation). DIAGNOSTIC: non-am LL_wl decreases −1.244 chars with line length (nearly equal to total −1.262) — p_blind scaling captures only the -am rate component; a deeper mechanism is required. 18th mechanism adopted. H512 generated.
**Status:** resolved — see F311

## H512: Line-Length-Conditional Non-am LL Word Length — RESOLVED by exp_310
**Priority:** RESOLVED — exp_310 (F312): REFUTED as suffix-length mechanism. DIAGNOSTIC: VMS non-am LL_wl gradient driven by "other"-suffix words increasing 22.5%→42.6% in long lines; recognized suffix length stays flat (2.97→3.12). Beta_ll suffix bias achieves r_ll 36% but is mechanistically wrong. H513 generated for correct mechanism.
**Status:** resolved — see F312

## H513: Line-Length-Conditional LL Word-Length Filter — RESOLVED by exp_311
**Priority:** RESOLVED — exp_311 (F313): CONFIRMED. MAJOR RESULT. mild_s30 achieves 19/19 PASS (N=30), Menzerath r=-0.163 (73%), r_ll=-0.206 (94% of VMS). Largest Menzerath gain in project history (+12pp). 19th mechanism adopted.
**Status:** resolved — see F313

## H514: Line-Length-Conditional Beta for MID Words — RESOLVED by exp_312
**Priority:** RESOLVED — exp_312 (F314): CONFIRMED. MAJOR RESULT. scale_1.0 (beta_eff(n)=0.50×n/8.4) achieves 19/19 PASS (N=30), menz_r=−0.203 (90.2% of VMS, +17pp from 73%), r_mid=−0.155 (86.9% of VMS, up from 61%), r_ll=−0.208 (95.1% maintained). VMS MID suffix length confirms negative gradient (2.696→2.599, r=−0.178). 20th mechanism adopted.
**Status:** resolved — see F314

## H519: CP90 and Word-Length Component Diagnostic with 21-Mechanism Architecture — RESOLVED by exp_316
**Priority:** HIGH — The last CP90 measurement (exp_302) used the 16-mechanism architecture; the last word-length component analysis (H494, never run) predates any Menzerath mechanisms. With 21 mechanisms now active (beta_scale=1.8, vocabulary clamping for qok/ok/ot/qot, n-conditional beta, etc.), CP90 ratios for sh/ch/d may have changed. Also, H494 asks which component (onset/midfix/suffix) drives the 22% word-length overproduction — this is pure VMS corpus measurement and requires no simulation.
**Status:** resolved — see F318 (exp_316). qok/ok/ot/qot CP90=0.94-1.00×. sh/ch/d CP90=21-39× (aggregate). Suffix_len −20% from beta bias (structural). H494 closed: suffix length is primary word-length gap.

## H520: Length-Biased VMS Lexicon Selection for sh/ch/d — RESOLVED by exp_318 — Can Line-Length-Conditional Type Selection Within Closed VMS Lexicons Simultaneously Achieve Near-VMS CP90 AND Maintain Menzerath r?
**Priority:** HIGH — exp_317 (F319) identified the fundamental tension: vocabulary clamping (CP90) and beta Menzerath mechanism are incompatible for large-token onset classes (sh+ch=73% of MID). The "type-reuse + length-bias" mechanism resolves this by keeping the closed type set but weighting type selection by target word length conditional on line length. This is analogous to GAMMA weighting in draw_buf (word-index conditional) but applied to VMS lexicon selection conditioned on LINE length n.
**Status:** resolved — see F320 (exp_318). All 6 conditions fail adj_rate (161-222%). adj_rate worsens monotonically with DELTA (as DELTA→0 = uniform clamp = adj_rate=126.3%, also fails). sh/ch/d CP90 gap is irreducible by any lexicon-selection mechanism; three-way constraint (CP90+Menzerath+adj_rate) cannot be satisfied simultaneously for large-token onset classes.

## H518: sh/ch/d CP90 Clamping — RESOLVED by exp_317
**Priority:** RESOLVED — exp_317 (F319): NEGATIVE DECISION. clamp_sh and clamp_ch individually pass 19/19 but cause Menzerath r regression (menz_r: 101.9%→96.3% for sh, →86.4% for ch; r_mid: 96.3%→85.9% for sh, →81.7% for ch). Root cause: sh+ch = 73% of MID tokens; clamping destroys line-length-conditional word-length variability for these onsets → beta Menzerath mechanism ineffective. clamp_d fails adj_rate (120.8%). clamp_shchd fails adj_rate AND catastrophically regresses menz_r (73.2%). ARCHITECTURAL TENSION: vocabulary clamping (CP90) and beta Menzerath mechanism are incompatible for large-token onset classes. Resolution requires "type-reuse + length-bias" mechanism (H520 candidate).
**Status:** resolved — see F319

## H517: IDX_THRESH Sweep — RESOLVED by exp_315
**Priority:** RESOLVED — exp_315 (F317): REFUTED. IDX_THRESH ∈ {3, 4} increases MID slope (138.9%, 141.0%) vs baseline IDX_THRESH=2 (123.7%). Mechanism works in opposite direction from prediction: exempting early positions leaves them longer, making the gradient steeper. IDX_THRESH=2 remains optimal. 22nd mechanism NOT adopted. MID slope 123% accepted as architectural floor.
**Status:** resolved — see F317

## H516: Fine Beta_scale Sweep for MID Component — RESOLVED by exp_314
**Priority:** RESOLVED — exp_314 (F316): CONFIRMED. All scales 1.0-2.5 pass 19/19 at N=30. Scale_1.8 achieves r_mid=100.1% (exact VMS), menz_r=104.1%, edy=87.2%, all 19 PASS. 21st mechanism adopted (beta_scale 1.0→1.8).
**Status:** resolved — see F316

## H515: Short-Line LL Word Length Boost — RESOLVED by exp_313
**Priority:** RESOLVED — exp_313 (F315): REFUTED in current form. Hard minimum (min_ll=6-7) + longest-fallback rejection sampling massively overshoots r_ll (154-205%) for all tested conditions. The primary remaining Menzerath gap is r_mid (82% of VMS), not r_ll (95%). 21st mechanism NOT adopted.
**Status:** resolved — see F315

## H510: LF/LL Word Length vs Line Length Correlation — RESOLVED by exp_308
**Priority:** RESOLVED — exp_308 (F310): CONFIRMED. r_ll=−0.219 (VMS, dominant) vs r_ll=−0.016 (sim, 7.3%). r_lf≈0 in both (negligible). LL word length decreases 1.31 chars with line length in VMS vs 0.098 chars in simulation (13× weaker). H511 generated.
**Status:** resolved — see F310

## H509: Section-Level Menzerath Analysis — RESOLVED by exp_307
**Priority:** RESOLVED — exp_307 (F309): REFUTED (cross-section heterogeneity). ALL VMS sections have strong Menzerath r (stars=−0.291, bio=−0.208, herbal=−0.329). Weighted within-section r=−0.268 > global r=−0.225. Simulation gap is genuine within-section mechanism deficit. Herbal/astro MID slopes 2× simulation capability; bio MID slope already matched.
**Status:** resolved — see F309

## H508: Beta Re-Sweep with 17-Mechanism clamp_sparse Architecture — RESOLVED by exp_306
**Priority:** RESOLVED — exp_306 (F308): CONFIRMED. beta=0.50 achieves 19/19 PASS (N=30), menz_r=−0.1089 (48% of VMS, up from 40%), MID slope=−0.049 (85% of VMS). edy_rate stable 98% across all beta values. Architecture parameter updated beta=0.30→0.50.
**Status:** resolved — see F308

## H507: am_lf_enr Seed Sensitivity in 17-Mechanism clamp_sparse Architecture — RESOLVED by exp_305
**Priority:** RESOLVED — exp_305 (F307): CONFIRMED. 10/10 seeds give 19/19 PASS; am_lf_enr 84-111% of VMS. exp_304 failure was statistical artifact (unlucky sequential RNG at SEED=304000, N=30). R_LF=0.12 confirmed optimal. 17-mechanism architecture is 19/19 stable.
**Status:** resolved — see F307

## H506: Full-VMS-Lexicon Clamping with Canonical Battery — RESOLVED by exp_304
**Priority:** RESOLVED — exp_304 (F306): PARTIALLY CONFIRMED. Sparse clamp (qok/ok/ot/qot): CP90 ratios 0.77-0.91× (near-VMS), edy_rate fragility resolved (83%→100%), 18/19 battery (am_lf_enr borderline 125.3%). All-7 clamp: adj_rate genuine failure. Architecture: adopt clamp_sparse_only as 17th mechanism.
**Status:** resolved — see F306
**Source:** exp_303 (F305): N_qok=100 gives CP90 ratio=0.74-0.96×; target is 1.0× using all 150 VMS qok types.
**Description:** Modify lexicon construction: for each clamped onset class, lexicon = ALL VMS B-dialect MID types of that onset class (no N cap), weighted by their VMS frequency. This gives CP90 ratio = 1.0× by construction. Test:
- Condition A: clamp sparse only (qok/ok/ot/qot with full-VMS lexicon) — should give CP90≈1× for sparse, still high for sh/ch/d
- Condition B: clamp all 7 major onset classes — should give CP90≈1× for all
- Run FULL 19-metric canonical battery (from exp_287 architecture) on both conditions × N=30 trials
- Key metrics to verify: edy_rate (fragile at 83.5%), am_mid_enr (critical), qok_ch, am_ll, d_ll
- Also measure: total MID vocabulary, per-trial type count, CP90 ratios per trial (not aggregate)
**Cost estimate:** medium — requires copying canonical battery from exp_287, adding full-VMS lexicon construction
**Prerequisites:** exp_303 (done — mechanism confirmed, lexicon approach identified)

## H505: Finite Vocabulary Pool for Sparse-Midfix Onset Classes — RESOLVED by exp_303
**Priority:** RESOLVED — exp_303 (F305): CONFIRMED. Vocabulary clamping reduces qok CP90 from 67× to 0.42-0.96×. Under-clamping (ratios <1×) due to top-N frequency weighting. Fix: use all VMS types (N=150 for qok) as lexicon. Battery check unreliable. H506 generated.
**Status:** resolved — see F305
**Source:** exp_302 (F304): qok paradigm 17× over-produced; modified path is primary source.
**Description:** Test two approaches to constrain qok vocabulary:
- Approach A: Pre-build per-onset finite lexicons: qok_lex = top-N qok word types by corpus frequency (N=50, 100, 150). When generating a MID qok word via cipher or modified path, restrict output to qok_lex. Compare CP90 ratio before and after for qok/ok/ot. Also check if battery stays 19/19.
- Approach B: Onset-conditional copy: for MID words with sparse-midfix onsets (qok/ok/ot/qot), increase copy probability from cp=0.55 to cp_sparse=0.80. Measure: CP90 ratio reduction vs battery impact.
- Key metrics: qok CP90 ratio (target: from 17× toward 1-2×), ok/ot/qot CP90 ratios, total MID vocabulary (target: from 1.33× toward 1.0×), battery pass count (must maintain 19/19).
**Cost estimate:** medium — extends simulation with per-onset vocabulary restriction; requires careful onset identification in cipher path.
**Prerequisites:** exp_302 (done — baseline CP90 ratios established)

---

## H498: qok A vs B Internal Structure — RESOLVED by exp_319
**Status:** RESOLVED — exp_319 (F321): ANSWERED. A-qok midfix richness driven by (1) 'e' vowel midfix 2× more frequent (25.5% vs 13.7%) and (2) 'ch' compound midfix forms (qokchol, qokchor, qokchody). 50 A-only types. Suffix diversity: A uses ol/ey/dy/or/ar vs B's edy/eedy/ain/aiin dominance. Distributed across folios (not a scribal artifact). See F321.
 — Why Does A-qok Have 2.6× Longer Midfix Than B-qok?
## H497: Suffix Entropy vs Hapax Rate per Onset Class
**Status:** RESOLVED — exp_295 (F296): Confirmed in A (ρ=+0.682), not in B (ρ=+0.098). B has HIGHER suffix entropy than A in 18/20 onset classes — standardization is at word-type level. Template-copying/grammar-word/line-terminal three-way characterization established.
 — Does Higher Suffix Entropy Predict Higher Hapax Rate?
## H496: Cross-Position Word Identity vs Onset-Class Overlap
**Status:** RESOLVED — exp_292 (F293): (A)=55-67% identical words, (B)=33-45% same class, (C)=0%. Positional grammar is both word-level and onset-class level. C=0% means all onset classes appear at all positions (probabilistic not categorical grammar).
 — How Much of LF/MID/LL Vocabulary Overlap Is Identical Words vs Shared Onset Class?
## H495: Hapax Internal Structure
**Status:** RESOLVED — exp_289 (F290): Hapax MLen=3.9 vs frequent MLen=0.55 (7× difference). ZeroMid: hapax=1% vs frequent=67%. Two-tier vocabulary confirmed.
 — Are Hapax Words Morphologically Different from Frequent Words?
## H493: Positional Entropy Conditioned on Onset Class — RESOLVED by exp_320
**Status:** RESOLVED — exp_320 (F322): CONFIRMED. Onset classes show divergent body entropy profiles at B1-B3 in both dialects. B-dialect B1 range=1.086 bits (ch=3.301 high, y=2.216 low); B3 range=1.054 bits (ch=3.225 high, qok=2.171 low). A-dialect B1 range=1.244 bits, B3 range=1.280 bits (ch high, d low throughout B1-B3). d-onset is the most constrained class (B0-B3 all below average, especially in A-dialect); ch-onset has broadest combinatorial freedom. Morphological interpretation supported; pure glossographic template model refuted. Entropy divergence peaks at midfix zone (B1-B3) and weakens toward suffix.
**Priority:** high — exp_259 measured overall positional entropy. If qok-onset words have a different entropy profile from ch-onset words at positions 3-5 (post-onset), this means the onset class carries predictive information about internal structure. This would strengthen the morphological interpretation: onset class not only determines positional distribution (grammar) but also constrains internal character sequence.
**Status:** resolved — see F322
**Source:** exp_259 (overall positional entropy). User Phase 6 directive.
**Description:** For each major onset class (qok, ch, sh, d, y, o, cth), compute h(c_i) at each position i within words in that class. Use absolute position (from word start) and relative position (from onset end). Specifically: after stripping the onset prefix, compute entropy of body[0], body[1], ..., body[-1] for each onset class. Compare profiles: do onset classes converge (same body entropy = onset doesn't predict body structure) or diverge (onset class predicts body structure)? Reference: Latin word stems by initial consonant cluster.
**Expected outcome under morphological interpretation:** Different onset classes will have different body entropy profiles (e.g., qok words have longer/more constrained bodies than ch words). Under template/glossographic: all onset classes will have similar body entropy profiles (onset is interchangeable).
**Cost estimate:** small — extension of exp_259 analysis
**Prerequisites:** exp_259 (done — overall positional entropy framework)

---

## H492: Stolfi Decomposition by Onset Class
**Status:** RESOLVED — exp_288 (F287/F288/F289): Three-tier midfix structure, qok A/B asymmetry, d→-aiin constraint.
 — Do Different Onset Classes Have Different Suffix Inventories, Midfix Lengths, and Internal Structure?
## H491: Suffix Length Gradient — RESOLVED by exp_287
**Priority:** RESOLVED — exp_287 (F299): CONFIRMED — MAJOR IMPROVEMENT. beta=0.30: 19/19 PASS, MID slope=−0.050 (87% of VMS −0.058, up from 55%), menz_r=−0.101 (45% of VMS −0.225, up from 23%). beta=0.50 fails (edy_rate). 16-mechanism architecture. edy_rate fragile at 83.5%.
**Status:** resolved — see F299

---

## H504: am_mid_enr Metric Stabilization — RESOLVED by exp_301
**Priority:** RESOLVED — exp_301 (F303): CONFIRMED. R_MID=0.20 gives am_mid_enr=100% (exact VMS) with 19/19 PASS. Architecture updated: R_MID=0.25→R_MID=0.20.
**Status:** resolved — see F303

## H487: B-Dialect ch→ch and sh→sh Anti-Self-Succession — RESOLVED by exp_299
**Priority:** RESOLVED — exp_299 (F301): PARTIALLY CONFIRMED. Anti-succession mechanism works (p_anti=0.40: ch→ch MID E2=1.001, 78% closure) but battery reveals am_mid_enr stochastically at boundary. Decision: not added to canonical architecture. H504 generated.
**Status:** resolved — see F301
**Description:** Test an anti-Markov rule: after generating a ch-onset MID word, reduce probability of next MID word also having ch onset. Implementation: in draw_buf, if prev_onset == 'ch' (or 'sh' or 'd'), draw with reduced weight on words of same onset class. Alternatively: rejection sampling — draw and reject if same onset with probability p_anti. Measure: E2_MID for ch→ch, sh→sh, d→d. Check: does 19/19 battery still pass? ss_mean uses global ch bigrams — check this specifically.
**Expected outcome:** Partial reduction in ch→ch/sh→sh/d→d over-production while maintaining 19/19. This is a low-priority refinement since the metrics are not in the battery.
**Cost estimate:** small — extend draw_buf with onset-based rejection probability
**Prerequisites:** exp_275 (done — over-production confirmed and magnitude measured)

---



# Pruned from active backlog: 2026-04-12

## H_new_FJ: o→a CONF cross-dialectally (E≈3.1×, F563) — what is the nature of this coupling? Section scope, specific a-onset words, reverse coupling, and interpretive significance.
**Priority:** high
**Status:** RESOLVED (exp_548, 2026-04-11). POSITIVE with complete characterization: o→a is primarily [o-word][aiin] (A: 43%=29/67; B: 30%=8/27); MID-position coupling; MUTUAL (a→o CONF both dialects, F566); B-dialect-wide (all B sections ≥(dir), F567). NEW F568: a-onset bigram grammar rich and conserved (a→a CONF 3.15×/4.01×; a→ok CONF both; a→ol CONF A; a→o CONF both; DEPL: d, qok). H_new_FJ CLOSED.
**Source:** exp_547 (2026-04-11): o→a CONF in A herbal_a (E=3.08×/obs=67) and B all (E=3.17×/obs=27). This is the strongest cross-dialectally conserved within-line bigram found. o-onset is a word starting with 'o' (bare o without higher-priority prefix); a-onset is a word starting with 'a' (ar, al, am, ain, aiin, etc.). The coupling is ~3× baseline in both dialects — stronger than any other cross-dialectal bigram. What grammatical/structural role does this represent?
**Description:** (1) **Specific a-onset words**: which a-onset words specifically follow o? Break the 67 A obs and 27 B obs by target word — do most go to 'ar', 'al', or 'aiin'? Is the target distribution concentrated or spread? (2) **Reverse coupling a→o**: compute a-onset→o bigrams. Is this symmetric (mutual coupling) or directional (o→a only)? (3) **Section scope in B**: break B o→a by B section (B herbal, B astro, B pharma) — is this B-pharma-primary (like ch→t F551) or B-dialect-wide? (4) **A section scope**: test A stars and A cosmo for o→a. (5) **Positional context**: does o→a appear at specific positions within lines, or throughout? Do o-a pairs appear at MID positions or near LF?
**Expected outcome:** The coupling may represent o-class as a "quantifier" or "modifier" that precedes a-class nouns/roots. Or it could be a sequential formula. If the target is concentrated (mostly 'ar' after 'or'), this is a specific word collocation. If spread, it's a class-level grammar rule. If a→o is also elevated, this is a mutual affinity. Section scope: likely B-dialect-wide given both B herbal+pharma show d→ok CONF (F527) — broad patterns tend to be cross-section.
**Cost estimate:** small — extend exp_547 with breakdown of a-successor vocabulary and reverse bigram + section scope test
**Prerequisites:** none

## H_new_FK: a-onset full characterization — vocabulary, positional distribution, and LF pos1 profile
**Priority:** high
**Status:** RESOLVED (exp_549, 2026-04-11). F569: a vocabulary DIALECT-STABLE (aiin/ar/al dominant in both; no A→B shift — most stable characterized class). F570: pos1 STRONGLY DEPL (A: 0.16×/14; B: 0.26×/12 — most extreme pos1-avoider). B LF CONF (1.52×/70). a-LF pos1 FLAT (no CONF, parallels ch-LF). H_new_FK CLOSED.
**Source:** exp_548 (2026-04-11): a-onset has a rich bigram grammar (F568: a→a CONF 3.15×/4.01×; a→ok CONF both; a→ol CONF A; a→o CONF both). But no positional profile has been computed. a-onset is 4.3% of A herbal_a words and 4.2% of B all words — comparable to o-onset (4.8% A, 2.8% B). a-onset vocabulary includes: aiin, ar, al, ain, aiiin, am, etc. The complete characterization would close the a-onset gap and enable comparison with o-onset (both are late-onset-priority classes with mutual coupling).
**Description:** Same 4-part methodology as exp_540-547. A herbal_a and B all: (1) a vocabulary (top-20 a words by frequency); (2) positional distribution (pos1/MID/LL/LF) vs baseline; (3) a within-line bigrams (a→X — largely established F568, but confirm with positional baseline instead of MID baseline); (4) a-LF lines pos1 profile. Special focus: is a-onset positionally enriched or flat (like o in A)? Does a have an LF enrichment (like B o LF CONF)?
**Expected outcome:** a-onset positional distribution: possibly LF-enriched given aiin appears frequently at LF. Possibly MID-enriched given o→a coupling is predominantly MID. pos1 likely depleted (aiin-type words as articles/particles rarely open lines). Vocabulary: aiin and ar likely dominant. a-LF pos1: may show o-onset enrichment (given o↔a mutual coupling, F566).
**Cost estimate:** small — direct reuse of exp_547 methodology
**Prerequisites:** none

## H_new_FP: ol and l-onset characterization — positional distribution, bigrams, LF pos1 for both ol and l
**Priority:** high
**Status:** RESOLVED (exp_553, 2026-04-11). F581 (ol vocabulary: A=bare+mixed; B=edy-compounds ~18%). F582 (ol positional: pos1 DEPL both; B LF CONF 1.65×/115). F583 (ol bigrams: ol→ol CONF A 3.20×/45; ol→o CONF both; ol→l CONF A; B ol→k CONF; A ol-LF pos1=s CONF 2.13×/17). F584 (l vocabulary: A=mixed; B=lchedy dominant 15.4%). F585 (l positional: B LF CONF 1.85×/145 — strongest B LF enrichment; B pos1 DEPL 0.52×). F586 (l bigrams: l→l CONF both; l→r CONF B 3.30×/17 — new strong coupling; B l-LF pos1=ch CONF 1.66×/10 — pos1-avoider ch opens l-terminal B lines). H_new_FP CLOSED.
**Source:** 'ol' and 'l' onset classes appear in multiple CONF findings: B s→ol CONF (2.23×/29, F573); a→ol CONF A (1.95×/30, F568); B astro ol→qok CONF (F528/F496); CL ol→qok CONF (F528); B astro ol→o dir (F530). Also: B a→l DEPL (0.53×/9, F568); B t→l near-baseline; B ok→ol (dir) (F514). 'ol' onset words include olaiin, olchey, olol etc. 'l' onset = words starting with 'l' (not 'ol'): laiin, lar, etc. Both classes uncharacterized positionally.
**Description:** Same 4-part methodology for ol-onset AND l-onset. A herbal_a and B all: (1) vocabulary; (2) positional distribution; (3) bigrams; (4) LF pos1 profile. Focus: are ol and l positionally distinct? Does ol have the same positional role in A and B (given B s→ol CONF and a→ol CONF suggest ol is an important bigram target)?
**Expected outcome:** ol may be MID-enriched (since it's a bigram target for s and a at elevated rates in MID positions). l onset may have different profile from ol.
**Cost estimate:** small
**Prerequisites:** none

## H_new_FQ: r-onset full characterization — motivated by l→r CONF B (E=3.30×/obs=17, F586) and A l→r dir (4.02×/5). What is r-onset's positional profile? Is it LF-enriched (paralleling l)? Does r→l CONF (reverse coupling, mutual like o↔a)?
**Priority:** high
**Status:** RESOLVED (exp_554, 2026-04-11). F587 (vocabulary: aiin-body dominant both dialects; B adds edy-compounds ~8%). F588 (r positional: B LF CONF 2.80×/48 — STRONGEST B LF enrichment; B pos1 DEPL 0.35×/6; A underpowered). F589 (l→r CONF B 3.30×/17 confirmed; r→l FLAT B — directional not mutual; A r→a dir 3.26×/8; B r-LF pos1=qok CONF 1.56×/10). H_new_FQ CLOSED.
**Source:** exp_553 (2026-04-11): l→r CONF B (3.30×/17, F586) is a strong new within-line coupling. A l→r dir (4.02×/5) is directional. R-onset words include: or, ar, ror, rol, rar, etc. (words starting with 'r' not preceded by higher-priority prefix). R-onset is uncharacterized. Given that l is strongly LF-enriched in B (1.85×/145, F585) and l→r CONF B, r may also be LF-enriched (as a post-l word). Or r may be a MID-class target for l-onset lines.
**Description:** Same 4-part methodology. A herbal_a and B all: (1) r vocabulary (top-20 r words); (2) positional distribution (pos1/MID/LL/LF vs baseline); (3) r within-line bigrams (r→X; baseline=MID distribution); (4) r-LF pos1 profile. Special focus: (a) is r→l CONF (mutual coupling, like o↔a)? (b) is r positionally enriched at LF (would make l→r an LF-approach coupling, l as penultimate before r at LF)? (c) what is r-onset's pos1 profile — opener or avoider?
**Expected outcome:** R may be LF-enriched in B (paralleling l; both lateral-like classes). R may be a MID class (l→r is a within-line MID coupling, r does not need to be at LF). R vocabulary likely includes 'or', 'ar', 'ror', lateral+body forms. r→l coupling (reverse): likely CONF in A if A l→a CONF (1.79×/17) but A l→r only dir (4.02×/5) — A may be underpowered for r characterization. B is the main power corpus for r given l→r CONF B.
**Cost estimate:** small — same methodology as exp_547-553
**Prerequisites:** none

## H_new_FS: p-onset full characterization — p is B pos1 CONF (5.23×/27 — highest B opener E-value, F592). P has appeared in LF pos1 dir signals: B qok-LF p@pos1 dir (F543); B ol-LF p@pos1 dir (F583); A ol-LF p@pos1 dir (F583). P is entirely uncharacterized in vocabulary, positional profile, and bigrams.
**Priority:** high
**Status:** RESOLVED (exp_556, 2026-04-11). F594 (vocabulary: A=diverse pch-bench; B=pchedy dominant 34.1%). F595 (pos1 CONF cross-dialectally A:2.99×/15; B:5.23×/27; MID DEPL both; LF virtually absent; B-dialect-wide). F596 (bigrams: B p→qok CONF 1.55×/10; A p→sh dir; B p→ch DEPL). P is CROSS-DIALECTAL CONF opener — corrects prior "B-ONLY" label. H_new_FS CLOSED.
**Source:** exp_555 (2026-04-11): B pos1 analysis reveals p-onset at 5.23×/27 CONF — the highest pos1 E-value of any onset class in B (exceeding s=4.77×). P has obs=27 at pos1 (out of 1279 B lines = 2.1% of B line openings). P is never in the opening discussion because it is low frequency overall (~0.4% of B words) but concentrated at pos1. Previous signals: p@pos1 dir in qok-LF and ol-LF (suggesting p opens lines containing specific terminal classes). P-onset words would include: par, pol, pam, py, pchedy, etc.
**Description:** Same 4-part methodology. A herbal_a and B all: (1) p vocabulary; (2) positional distribution (pos1/MID/LL/LF); (3) p within-line bigrams; (4) p-LF pos1 profile. Special focus: (a) is p a B-only opener or also A-opener? (b) what are p-onset words — are they a coherent vocabulary class? (c) does p show LF-class-specific line opening (already seen for qok-LF and ol-LF)?
**Expected outcome:** P is likely B-specific or B-dominant (given no A characterization). P vocabulary may include pchedy, par, pam-type words. P-onset may be extremely pos1-concentrated (almost exclusively opener), similar to how t, s, y are pos1-enriched.
**Cost estimate:** small
**Prerequisites:** none

## H_new_FR: B LF terminal class synthesis — B LF is occupied by a structurally coherent cluster: r(2.80×/48), l(1.85×/145), ol(1.65×/115), o(1.58×/57), a(1.52×/70) — all lateral/vowel-initial classes. No opener or template class is B LF-enriched. What do B LF lines look like internally? Is there a B LF "terminal formula" and what specific words occupy LF most?
**Priority:** high
**Status:** RESOLVED (exp_555, 2026-04-11). F590 (B LF full taxonomy: 5 CONF LF-enriched + 4 CONF LF-DEPL). F591 (B LF word vocabulary: top words characterized). F592 (B pos1 full taxonomy: p is new CONF opener). F593 (complete B 3-layer architecture). H_new_FR CLOSED.
**Source:** exp_554 (2026-04-11): B LF ranking: r(2.80×)>l(1.85×)>ol(1.65×)>o(1.58×)>a(1.52×). All five B LF-enriched classes are lateral (r, l, ol) or vowel-initial (o, a). B pos1 profile for each B LF class: r-LF pos1=qok CONF; l-LF pos1=ch CONF (F586); ol-LF no strong pos1 signal; o-LF pos1=y CONF (F564); a-LF pos1 FLAT (F570). The B LF occupation by lateral+vowel classes is structurally coherent — this is a characterizable property of B dialect line structure. Additionally: the d-class is B pos1 CONF (opener) while the LF classes are all non-d. Structural picture: B lines open with d/s/t/y and terminate with r/l/ol/o/a.
**Description:** Two sub-questions: (1) Confirm B LF complement — what onset classes are DEPLETED at B LF? Compute full B LF onset distribution and compare all classes. (2) B LF word-level vocabulary — what are the most common B LF words (the actual last words of B lines), broken by onset class? Is there a concentration in specific words (like B LF=r words: raiin, rol dominant)? This would characterize the actual terminal vocabulary.
**Expected outcome:** B LF DEPL classes: s, t, y (the pos1-enriched openers) likely avoid LF in B — s and t were flagged as LF-near-depleted (F572, F575). Template classes (qot, ot) may be near-baseline at B LF. The B LF terminal vocabulary is likely: raiin, lchedy, ol, or, aiin, daiin — the highest-frequency words from the five LF-enriched classes. Confirming this would give a concrete picture of B line endings.
**Cost estimate:** small — compute B LF onset distribution comprehensively + top LF words
**Prerequisites:** none

## H_new_FV: A herbal_a line structure formula test — the d↔cth mutual coupling (F602) combined with d-LF CONF (F597) and cth-LF CONF (F601) and shared qo-class opener preference (F602 + F556) suggests an A line pattern: [qo/qot opener][...][cth word(s)][d word at LF]. Test directly: among A lines that end in d, what fraction contain a cth word before the d? Among A lines ending in cth, what fraction are followed by d-LF lines in CL?
**Priority:** medium
**Status:** RESOLVED NEGATIVE (exp_559, 2026-04-11). F603: [cth@LL][d@LF] exists (14 lines, 3.9% of d-LF) but E=1.37× sub-CONF. d-LF with any cth: E=1.29×/47. Inter-line cth-LF→d-LF: E=1.13× (flat). The d↔cth coupling is distributed word-adjacency (57% MID, 38% LL→LF), not a terminal formula. Dominant pairs: cthol→daiin (6), cthy→daiin (6). H_new_FV CLOSED.
**Source:** exp_558 (2026-04-11): d↔cth mutual CONF coupling (both directions 1.97×); cth LL+LF enriched; d LF CONF; both prefer qo-class openers at pos1. The within-line evidence strongly suggests [cth][d] ordering near line ends in A. If confirmed, this would be an A-specific line-terminal formula combining compound gallows and d-class words.
**Description:** (1) Among A lines with LF=d: what fraction contain at least one cth word? Expected ~1.96× overrepresentation (cth→d CONF). (2) Among A lines with LF=cth: what fraction are followed in CL by a d-LF line? (3) Is the [cth][d] sequence predominantly in the LL+LF positions (cth at LL, d at LF)? (4) What are the most common [cth-word][d-word] bigram pairs?
**Expected outcome:** If [cth at LL][d at LF] is a formula: ~20-30% of d-LF lines should contain a cth word in the penultimate position. The specific word pairs may be concentrated (e.g., [cthy][daiin] or [cthol][daiin] as dominant pairs).
**Cost estimate:** small
**Prerequisites:** none

## H_new_FU: cth-onset full characterization — cth is A LF CONF (1.67×/88, F597) and pos1 EXTREME DEPL (0.13×/7) — the most purely terminal onset class in A. Cth receives from d (d→cth CONF A, F555) and k (k→cth CONF A, F580). Full vocabulary, positional, and bigram profile needed.
**Priority:** high
**Status:** RESOLVED (exp_558, 2026-04-11). F600 (vocabulary: A=y/lateral; B=edy; 8.6× freq drop). F601 (pos1 DEPL 0.13×; LF CONF 1.67×/88; LL 1.35×). F602 (d↔cth mutual CONF; cth→cth CONF; qok→cth DEPL; cth-LF pos1=qo/qot dir). H_new_FU CLOSED.
**Source:** exp_557 (2026-04-11): cth is A LF CONF (1.67×/88) and pos1 extreme DEPL (0.13×/7). Cth is a pure terminal class in A — it receives from d and k (within-line), and appears at LF at above-baseline rate. In B: cth has obs=7 at LF (1.79×/7 dir) — underpowered but directional. Cth vocabulary: cthy(27=31% of cth-LF), cthey(9), cthol(6), cthor(6). But cth full vocabulary (all positions) and bigram profile are unknown.
**Description:** Same 4-part methodology: (1) cth vocabulary (top-20 words); (2) positional distribution (pos1/MID/LL/LF vs baseline); (3) cth within-line bigrams (cth→X; and X→cth bigram receivers); (4) cth-LF pos1 profile. Special focus: (a) what does cth route to after appearing (cth→X bigrams)? (b) is cth-LF pos1 grammar characterized (pos1 preference after cth terminal lines)?
**Expected outcome:** cth: pos1 DEPL cross-dialectally (confirmed 0.13×); LF CONF in A (confirmed 1.67×); possibly LF elevated in B (dir). Cth bigrams: likely receives from d (confirmed) and k (confirmed); cth→X: routes to other LF classes or ch. Cth vocabulary: cthy (~30%), cthey, cthol, cthor — aiin-body and lateral forms.
**Cost estimate:** small
**Prerequisites:** none

## H_new_FT: A herbal_a LF full onset synthesis — analogous to exp_555 (B LF synthesis). A LF CONF classes were identified as d(1.53×/360) and cth(1.67×/88) in exp_555. What is the complete A LF onset distribution? What are the A LF DEPL classes? What are the top A LF words?
**Priority:** high
**Status:** RESOLVED (exp_557, 2026-04-11). F597 (A LF taxonomy: cth+d CONF; y,qok,sh,qo DEPL). F598 (A LF vocabulary: daiin dominant). F599 (complete A/B comparison; sch NEW CONF A opener). H_new_FT CLOSED.
**Source:** exp_555 (2026-04-11): A LF partial data showed d=1.53×/360 CONF and cth=1.67×/88 CONF. These are completely different from B LF CONF classes (r,l,ol,o,a). The cross-dialectal LF inversion (A=d+cth; B=r+l+ol+o+a) is a major structural contrast (F593). But A LF has not been comprehensively tabulated — other classes may be LF-CONF or LF-DEPL in A. Full A LF distribution would complete the F593 contrast picture and potentially reveal additional A-specific terminal classes.
**Description:** Same approach as exp_555 Part 1-2 applied to A herbal_a. (1) Full A LF onset distribution — all onset classes with obs/exp/E/flag; (2) A LF word vocabulary — top words by onset class; (3) A pos1 full distribution for comparison; (4) A positional complementarity table (analogous to F593). This would give the complete A 3-layer architecture.
**Expected outcome:** A LF CONF: d (dominant, 1.53×/360 already established), cth (1.67×/88). A LF DEPL: y (0.63×/72 DEPL established F558), qok (0.57×/82 DEPL), sh (0.55×/88 DEPL). A pos1 CONF: qot, s, t, y, p. A MID classes: ch, ok, qok, ot, sh. Result would show A has a different 3-layer structure from B: A OPENERS = qot+s+t+y+p; A MID = ch/qok/ok/ot/sh; A TERMINALS = d+cth (dominant, not the lateral cluster). A TERMINALS are structurally different: d is both opener (B) and terminal (A); cth is compound-gallows — no analog in B LF.
**Cost estimate:** small — extend exp_555 approach to A
**Prerequisites:** none

## H_new_GA: qo-onset full characterization — RESOLVED (exp_563, 2026-04-11)
**Status:** RESOLVED — F612/F613/F614. qo is a MID class (NOT opener); A LF DEPL (0.46×/27); B LL DEPL (0.52×/21); B qol dominant (24.8%); sh→qo CONF cross-dialectally (2.17×/44 A; 1.97×/50 B).

## H_new_GB: sh-onset full characterization — RESOLVED (exp_564, 2026-04-11)
**Status:** RESOLVED — F615/F616/F617. sh: LF DEPL both (A:0.47×; B:0.39×); B pos1 DEPL(0.56×/78); sh→ch DEPL cross-dialectal; sh→qok CONF both; s→sh CONF both; sh→qo CONF both. H_new_GB CLOSED.

## H_new_GC: qok-onset full characterization — RESOLVED (exp_565, 2026-04-11)
**Status:** RESOLVED — F618/F619/F620. qok: A→B DOUBLES (7.30%→15.13%); LF DEPL CONF both (0.51×/0.53×); A pos1=0.87× (corrects prior 1.47×; NOT opener); sh→qok CONF cross-dialectal; s→sh→qok chain complete. Q013 raised re: B self-succession conflict with C007.

## H_new_GD: ch-onset full characterization — RESOLVED (exp_566, 2026-04-11)
**Status:** RESOLVED — F621/F622/F623. ch=19.79% A (most frequent); pos1 EXTREME DEPL (A:0.32×; B:0.22×); LF sub-baseline NOT DEPL; ch→sh DEPL both; B ch→l/t CONF; A [qo@LL][ch@LF] CONF. H_new_GD CLOSED.

## H_new_GE: ok-onset full characterization — RESOLVED (exp_567, 2026-04-11)
**Status:** RESOLVED — F624/F625/F626. ok: pos1 DEPL both (A:0.57×; B:0.50×); LF NOT DEPL (sub-baseline); MID class; a→ok CONF both; B ok-LF pos1=t CONF. Q013 extended (A ok self-succession 1.42× vs C007's 2.05×). H_new_GE CLOSED.

## H_new_GF: ot-onset full characterization — RESOLVED (exp_568, 2026-04-11)
**Status:** RESOLVED — F627/F628/F629. ot: A→B INCREASES (4.84%→6.69%); B pos1 EXTREME DEPL (0.26×/22); A pos1=0.77× sub-baseline NOT DEPL (CORRECTS prior 1.29×); LF NOT DEPL both; ot→ot CONF cross-dialectal (A:2.32×/50; B:2.31×/90); ot→a CONF cross-dialectal; B qot→ot CONF; A l→ot CONF; B l→ot DEPL (A↔B inversion); B ot-LF y@pos1 CONF; A ot-LF t@pos1 CONF. H_new_GF CLOSED.

## H_new_FY: Compound gallows → d universal coupling test — ALL 4 compound gallows (cth, ckh, cph, sch) route to d within A herbal_a lines at E=2.0-3.4× (F607-F610). Is this a compound-gallows-class property or a positional artifact? Test: control for positional co-occurrence. Among lines where a compound gallows word and a d-word co-occur, is there a directional ordering (c-gallows before d)?
**Priority:** medium
**Status:** RESOLVED (exp_562, 2026-04-11). F611: combined c-gallows→d CONF (E=2.10×/68 CONF); LL→LF enriched (E=2.13×/28); directionality NEGATIVE (d before c-gallows 43% > c-gallows before d 29%); [o][ckh][d] (dir) (E=3.43×/3); d→cth CONF (2.21×/62). Coupling is primarily [c-gallows@LL][d@LF] terminal pattern. H_new_FY CLOSED.
**Source:** exp_561 (2026-04-11): All 4 compound gallows route to d: cth→d CONF (1.97×/37); ckh→d CONF (2.00×/18); cph→d dir (2.50×/7); sch→d dir (3.43×/6). Together, compound gallows appear before d at ~2× baseline. This may be: (a) a word-class property (compound gallows words grammatically precede d-words); (b) a positional artifact (compound gallows tend toward MID/LL, which naturally precede LF=d); or (c) both. Distinguishing these would clarify whether compound gallows have a functional relationship to d.
**Description:** (1) Among A lines containing both a compound gallows word and a d-word: what fraction have [c-gallows before d] vs [d before c-gallows]? Expected: if directional property, [before] >> [after]. (2) Control for line length — longer lines give more MID positions before LF. (3) Combine all 4 compound gallows classes for power (total compound gallows → d bigrams: ~37+18+7+6 = 68). Compute combined E vs MID baseline.
**Expected outcome:** If directional: [c-gallows before d] / [d before c-gallows] >> 1. Combined E should be ~2.0× across all 4 classes.
**Cost estimate:** small
**Prerequisites:** none

## H_new_FX: ckh+cph onset characterization — compound gallows ckh (c+k+h) and cph (c+p+h) appear in ONSET_PRIORITY. Y→ckh CONF A (F559: 1.64×/obs=12); cth→cph (dir) A (F602: E=3.30×/3). Both are uncharacterized. Given sch is pos1 CONF (11.54×/16), do ckh and cph also show pos1 enrichment (compound gallows as a class of openers)?
**Priority:** high
**Status:** RESOLVED (exp_561, 2026-04-11). F607 (positional taxonomy: sch=opener; cth=terminal; ckh=MID pos1-near-zero/LF DEPL; cph=MID/LL; combined 6.7× A→B drop). F608 (ckh: MID class). F609 (ckh→d CONF 2.00×/18; y→ckh CONF 1.84×/13; o→ckh CONF 1.76×/10; compound gallows → d universal coupling). F610 (cph: cph→d dir 2.50×/7; cth→cph (dir) confirmed). H_new_FX CLOSED.
**Source:** exp_560 (2026-04-11): sch pos1 CONF 11.54×/16 — the compound gallows class (c+sh, c+ch, c+k, c+p) may be systematically pos1-enriched. Y→ckh CONF A (F559: y→ckh 1.64×/12 — wait, this was in a different context. Actually let me recall: in exp_545 (y characterization): y→ckh CONF A (E=1.64×/12? or is this right?). Also cth→cph (dir) A (E=3.30×/3 from F602). Ckh and cph are in ONSET_PRIORITY higher-priority than ch, sh. If compound gallows (cth, ckh, cph, sch) are all openers, this forms a structural class.
**Description:** Joint characterization: (1) ckh vocabulary (both dialects); (2) ckh positional (pos1/MID/LL/LF); (3) ckh bigrams; (4) cph vocabulary; (5) cph positional; (6) cph bigrams. Cross-compare with sch (pos1 CONF 11.54×) and cth (pos1 DEPL 0.13×). Expected to reveal whether compound gallows are systematically pos1-enriched or whether cth and sch represent different structural classes within compound gallows.
**Expected outcome:** ckh may be pos1-enriched (if compound gallows = openers). cph likely very rare. Cross-comparison with cth (pos1 DEPL) would clarify: is sch anomalous, or are ckh/cph also pos1-enriched? If cth is LF-enriched (terminal) and sch/ckh are pos1-enriched (opener), then compound gallows class splits into terminal (cth) vs opener (sch, ckh, cph) subclasses.
**Cost estimate:** small (rare classes; same methodology)
**Prerequisites:** none

## H_new_FW: sch-onset full characterization — sch is A pos1 CONF (3.91×/15, F599) — newly discovered as the 6th A CONF opener. Sch is uncharacterized in vocabulary, full positional profile, bigrams, and LF grammar. Is sch A-only or cross-dialectal? What do sch-onset words look like?
**Priority:** high
**Status:** RESOLVED (exp_560, 2026-04-11). F604 (vocabulary: A=y-body; B=edy; frequency-stable 0.20% both). F605 (A pos1 CONF 11.54×/16 — HIGHEST E-value; B pos1 dir 6.66×/9). F606 (sch→d dir both dialects; opener→terminal coupling). H_new_FW CLOSED.
**Source:** exp_557 (2026-04-11): A pos1 full distribution revealed sch at 3.91×/15 CONF — higher than t (2.27×/111) and s (3.16×/163) in terms of E-value, though lower N. Sch appears in ONSET_PRIORITY (after sph, before d). Sch words would include: shchy, shchey, etc. — compound sh+ch gallows. The A pos1 CONF for sch (E=3.91×/15) means sch is preferentially a line-opener in A, similar to p (2.99×/15). This was an unexpected discovery — sch was not in the prior CONF opener list. Full characterization needed.
**Description:** Same 4-part methodology: (1) sch vocabulary (top-20 sch words, both A and B); (2) positional distribution (pos1/MID/LL/LF vs baseline, both dialects); (3) sch within-line bigrams (sch→X; X→sch); (4) sch-LF pos1 profile. Special focus: (a) Is sch A-only opener or also B pos1-enriched? (b) What is B sch frequency (may be very low)? (c) What are sch-onset words — are they a coherent class?
**Expected outcome:** Sch pos1 in A: CONF (3.91×/15 confirmed). Sch in B: likely very low frequency (compound gallows absent in B, F600). Sch vocabulary: compound forms with sch-prefix. LF: likely DEPL (openers avoid LF).
**Cost estimate:** small
**Prerequisites:** none

## H_new_FN: k-onset full characterization — vocabulary, positional distribution, bigrams, k-LF pos1
**Priority:** medium
**Status:** RESOLVED (exp_552, 2026-04-11). F578 (vocabulary: A=mixed/ch-bench+e-body; B=edy-body). F579 (pos1 DEPL cross-dialectally A: 0.52×/32; B: 0.16×/4 — k is a MID-class pos1-avoider, opposite of s/t/y). F580 (bigrams: A k→cth CONF; B k→ok/d CONF; k→qok DEPL cross-dialectally). H_new_FN CLOSED.
**Source:** k-onset (simple gallows) appears in several findings: B a→k CONF (F568: 1.59×/10); t→k sub-CONF (B: 1.78×/7, exp_551); F559 (y→k CONF B: 1.68×/11). k is the simplest gallows class in EVA. No formal characterization exists. k frequency: estimated ~3-4% of words.
**Description:** Same 4-part methodology. A herbal_a and B all: (1) k vocabulary; (2) positional distribution; (3) k within-line bigrams; (4) k-LF pos1 profile. Focus: is k a line-opener (like t, s, y) or a MID/LF class?
**Expected outcome:** k may be pos1-enriched (gallows classes tend to be openers). Or k may be a MID class distinct from the t/s opener cluster.
**Cost estimate:** small
**Prerequisites:** none

## H_new_FM: t-onset full characterization — vocabulary, positional distribution, bigrams, t-LF pos1
**Priority:** high
**Status:** RESOLVED (exp_551, 2026-04-11). F574 (vocabulary: A=mixed/ch-bench; B=edy-body). F575 (pos1 CONF A: 2.27×/111; B: 3.18×/78 — THIRD LINE-OPENER; MID DEPL both; B LF DEPL). F576 (bigrams: A t→qot CONF; B t→ot CONF; ok DEPL both). F577 (t-LF pos1: y DEPL, o@pos1 dir). H_new_FM CLOSED.
**Source:** F523 (exp_527): A stars t-onset at pos1 CONF (E=3.67×/obs=16 vs A herbal_a baseline). t is a confirmed line-opener in A stars, alongside s (F524/F572). From exp_524 (CL analysis): t-LF is a CL relay in A herbal_a (receives from d CONF F508 and sh (dir) F510; routes to d near-CONF and y (dir)). From exp_535 (ot characterization): ot≠t (ot is template class with different grammar). Now that s is confirmed as pos1-CONF (3.16×/4.75×, F572), t is the natural next candidate for a pos1-enriched gallows class. Also: t-LF appears in multiple B findings as a pos1 opener for other LF classes (F540: B ok-LF pos1=t CONF; F548: B a-LF pos1=t sub-CONF).
**Description:** Same 4-part methodology. A herbal_a and B all: (1) t vocabulary; (2) positional distribution; (3) t within-line bigrams; (4) t-LF pos1 profile. Special focus: is t a pos1-enriched opener (like s, y) or a different positional class? Does t have a different profile in A herbal_a vs A stars?
**Expected outcome:** t may be pos1-enriched in A herbal_a (consistent with A stars CONF). Or t may be a MID/LF class in A herbal_a. t-LF pos1 grammar: likely y or s enriched (consistent with overall line-opening patterns).
**Cost estimate:** small
**Prerequisites:** none

## H_new_FL: s-onset full characterization — vocabulary, positional distribution, bigrams, s-LF pos1
**Priority:** high
**Status:** RESOLVED (exp_550, 2026-04-11). F571 (vocabulary: A=mixed, B=aiin+sol-dominated). F572 (pos1 CONF cross-dialectally A: 3.16×/163; B: 4.75×/165 — second definitive LINE-OPENER alongside y; MID/LL DEPL). F573 (bigrams: s→sh CONF both; s→a CONF both; B s→ol CONF; DEPL: q-class). s-LF pos1 FLAT. H_new_FL CLOSED.
**Source:** F524 (exp_527): A stars s-onset at pos1 CONF (E=2.10×/obs=13) — s is a confirmed line-opener in A stars alongside t (F523). s also appears in: F516 (ok-LF pos1=s dir, A herbal_a); F521 (A stars ol-LF pos1=s dir). No formal 4-part s-onset profile exists. s is approximately 4-5% of words in A herbal_a (estimated), making it comparable to o/a in frequency. Characterizing s-onset would complete the picture of all onset classes >2% frequency.
**Description:** Same 4-part methodology as exp_540-549. A herbal_a and B all: (1) s vocabulary (top-20 s words); (2) positional distribution (pos1/MID/LL/LF) vs baseline; (3) s within-line bigrams (s→X); (4) s-LF lines pos1 profile. Special focus: is s a pos1-CONF opener in A herbal_a (as in A stars)? Or is the A stars pattern section-specific?
**Expected outcome:** s may be pos1-enriched in A herbal_a (consistent with A stars CONF). Vocabulary: likely includes sor, saiin, sol-type words in A; s-edy forms in B. s bigrams may show s→ch or s→sh routing.
**Cost estimate:** small — direct reuse of exp_549 methodology
**Prerequisites:** none

## H_new_FD: sh-onset full characterization — vocabulary, positional distribution, bigrams, LF pos1
**Priority:** high
**Status:** RESOLVED → F544/F545/F546 (exp_540, 2026-04-11). ANSWERED: A sh o-body dominant (~40%); B sh edy-body dominant (25.2%). sh LF-DEPLETED both dialects (A: 0.51×; B: 0.47×). sh is MID-class (not opener: A pos1=1.03× neutral; B pos1=0.70× DEPLETED). A/B routing INVERSION: A→{sh-self CONF, k CONF, t CONF}; B→{qok CONF, qo CONF, qot CONF}. Cross-dialectal conserved: sh→ch DEPLETED (F328). B sh-LF pos1=sh CONF (E=2.00×/obs=10) — line-level bracket. H_new_FD CLOSED.
**Source:** exp_535-537 established complete template class quad (F536-F543). sh is the most important non-template onset class: it's the CL relay in A herbal_a (sh→ok dir F509, sh→t dir F510); it drives the sh→qok bigram (F372); it has the mutual ch↔sh avoidance (F328); and it's a pos1 opener in some sections (F524: A stars s-onset). Full positional characterization at same level as template classes would complete the "major onset class" picture.
**Description:** For A herbal_a and B all: (1) sh vocabulary (top-20 sh words by frequency); (2) positional distribution (pos1/MID/LL/LF) vs baseline; (3) sh within-line bigrams (sh→X); (4) sh-LF lines pos1 profile. Compare sh positional role to template classes (qot/qok/ot/ok, F539).
**Expected outcome:** sh is likely MID-biased (from the sh→qok MID bigram rule) or pos1-elevated (from formula openers). sh→qok should be elevated within-line. sh→ch should be DEPLETED (from ch↔sh avoidance F328). sh vocabulary: A dominated by sh-bench compounds (shey, shor, shol); B by shedy/sh-edy forms.
**Cost estimate:** small — direct reuse of exp_534/535/536/537 methodology
**Prerequisites:** none

## H_new_FC: ch-onset full characterization — vocabulary, positional distribution, bigrams, LF pos1
**Priority:** high
**Status:** RESOLVED → F547/F548/F549/F550 (exp_541, 2026-04-11). ANSWERED: ch pos1 STRONGLY DEPLETED (A: 0.38×; B: 0.25×) — most pos1-excluded major class. MID elevated (1.14-1.18×). LF near-baseline (0.91-0.96×) — ch/sh COMPLEMENTARITY (sh avoids LF; ch avoids pos1). A ch: NO CONF within-line signals (flat). B ch→t CONF (E=1.77×/obs=35, NEW). Ch→sh DEPLETED both dialects (F328 confirmed). Ch→ch sub-CONF (1.08×A, 0.93×B, F461/462 confirmed). Ch-LF pos1 FLAT both dialects (only major LF class with absent pos1 grammar, F550). Ch vocabulary y-body dominant in both dialects (F549). H_new_FC CLOSED. New hypothesis: H_new_FE (B ch→t section scope).
**Source:** ch is the most frequent onset class in A herbal_a (~18% of words) and the dominant MID class. ch→ch self-succession (below CONF after corrections), ch↔sh mutual avoidance (F328), ch→o CL CONF (F506), ch→daiin coupling (F362). A complete positional characterization would complete the "major onset class" picture alongside sh (H_new_FD).
**Description:** Same 4-part methodology as sh. Compare ch/sh/template-class profiles for onset grammar taxonomy.
**Expected outcome:** ch is likely MID-enriched and LF-enriched but depleted at pos1 (from various findings). ch→ch within-line sub-CONF (corrected F461/462). ch→daiin within-line elevated.
**Cost estimate:** small
**Prerequisites:** none

## H_new_FI: A d-LF paragraph structure — do qot-opener d-LF lines (F556) preferentially lead to ch-LF or qot-LF on next line (testing multi-level nesting of F491 + F556)?
**Priority:** medium
**Status:** RESOLVED NEGATIVE (exp_546, 2026-04-11). H_new_FI CLOSED NEGATIVE. No conditional enhancement of d→qot CL given qot/ot-opener at pos1. F556 (d-LF pos1=qot/ot CONF) and F491 (d→qot CL CONF) are INDEPENDENT structural patterns. SIDE FINDING: d→d CL CONF (E=1.77×/obs=101, F560) — d-LF self-chaining is the dominant CL signal, with template-opener d-LF lines showing enhanced d→d CL (directional, N insufficient).
**Source:** exp_543 (2026-04-11): A d-LF lines have qot at pos1 CONF (F556, E=1.92×/obs=25) and ot at pos1 CONF (E=1.72×/obs=24). F491: d-LF lines are followed by qot-LF on next line (CL CONF). F506: qot-LF lines are followed by ch-LF (CL CONF). So the proposed paragraph structure is: [qot/ot(pos1)...d(LF)] → [qot(LF)] → [ch(LF)]. If this nesting is real, qot-opener d-terminal lines should SPECIFICALLY lead to qot-terminal next lines at a higher rate than generic d-LF lines. This would be the first test of a within-line × cross-line interaction.
**Description:** Take A herbal_a d-LF lines. Split into two groups: (A) d-LF lines where pos1=qot; (B) d-LF lines where pos1≠qot. For each group, compute the CL target distribution (what LF class follows on next line). Does group A have stronger qot→LF signal than group B? If group A has higher qot-next-line rate, this confirms the multi-level nesting.
**Expected outcome:** If nesting is real: group A (d-LF with qot-pos1) should have qot as next-line LF at E≥1.5× MORE than group B. If this is coincidental: both groups should show same CL distribution.
**Cost estimate:** small — A herbal_a d-LF = 360 lines; qot-pos1 subset ≈ 25 lines; statistical test feasible
**Prerequisites:** none

## H_new_FG: y-onset full characterization — vocabulary, positional distribution, bigrams, LF pos1
**Priority:** medium
**Status:** RESOLVED → F557/F558/F559 (exp_545, 2026-04-11). y pos1 STRONGLY CONF in BOTH dialects (A: 2.78×; B: 3.54×) — highest cross-dialectal pos1 enrichment; MID/LL/LF DEPLETED. Y=definitive LINE-OPENER. Vocab: A=gallows+body; B=edy-body. y→y CONF cross-dialectal; y→ckh CONF A; y→k CONF B (gallows routing). H_new_FG CLOSED.
**Source:** exp_540-541 completed sh and ch characterizations. y-onset is the major LF class in B herbal (y CONF at LF, F447), elevated at pos1 for o/ok/ot LF lines (F455/F456/F502), and a key LF marker in A cosmo and B dialect sections. y-onset is the third most-characterized class based on incidental findings, but lacks a formal 4-part onset-class profile. The complete major-onset-class taxonomy (template quad + sh + ch + d + y) would give a comprehensive positional grammar map.
**Description:** Same 4-part methodology as exp_540-541 (sh, ch). A herbal_a and B all: (1) y vocabulary; (2) positional distribution (pos1/MID/LL/LF) vs baseline; (3) y within-line bigrams (y→X); (4) y-LF lines pos1 profile. Compare y to ch/sh profiles. Special focus: y LF rate (known elevated in B herbal), y pos1 rate (known elevated as LF-class opener rule), y→ch coupling (expected elevated from known patterns).
**Expected outcome:** y is likely LF-elevated in B (F447) and MID+LF distributed in A. y within-line bigrams may show y→ch or y→qot coupling. y-LF pos1 profile should be flat or show d/y-self elevation.
**Cost estimate:** small — direct reuse of exp_541 methodology
**Prerequisites:** none

## H_new_FH: B d→sh CONF (E=1.79×/obs=109, F555) — section scope; also A d→cth/ckh CONF scope
**Status:** RESOLVED (exp_544, 2026-04-11). B d→sh CONF is B-HERBAL (E=2.14×/obs=21 CONF) + B-PHARMA (E=2.23×/obs=34 CONF); B astro sub-CONF (E=1.40×/obs=48, genuine null); B cosmo underpowered. F555 scope = B-herbal+pharma. A d→cth/ckh: compound gallows absent from B (cth obs≤1, ckh obs=0 per B section) — A-herbal-a-specific by necessity. H_new_FH CLOSED.
**Priority:** medium
**Source:** exp_543 (2026-04-11): B all d→sh CONF (E=1.79×/obs=109, F555). B all pools B herbal (162 lines), B astro (544 lines), B pharma (498 lines), B cosmo (79 lines). Is d→sh B-dialect-wide or section-specific? Context: B d is the dominant pos1 class (E=2.64×, F554), and sh is a B MID class (E=1.15×, F545). Also: A d→cth CONF (E=1.97×/obs=62) and A d→ckh CONF (E=1.58×/obs=20) — are these A-herbal_a-specific?
**Description:** Break B all d→sh by section (B herbal, B astro, B pharma, B cosmo) using folio-number classification from exp_542. Also test A sections: A stars and A cosmo for d→cth, d→ckh scope.
**Expected outcome:** If B d→sh is B-pharma-primary (like ch→t was), scope narrows. If B-dialect-wide, F555 scope expands. A d→cth is likely A-herbal-a-specific given compound gallows frequency distribution.
**Cost estimate:** small — subset of exp_543 methodology with section classification from exp_542
**Prerequisites:** none

## H_new_FF: d-onset full characterization — vocabulary, positional distribution, bigrams, LF pos1
**Priority:** high
**Status:** RESOLVED → F553/F554/F555/F556 (exp_543, 2026-04-11). ANSWERED: d aiin-dominated (A: 40.4%; B: 32.4%), daiin dominant (F553). A/B POSITIONAL INVERSION: A d=LF CONF (E=1.52×/obs=360); B d=pos1 CONF (E=2.64×/obs=246). MID-DEPLETED both (A: 0.73×; B: 0.67×). D is structural EDGE class (F554). A d→cth CONF (1.97×/62) + d→ckh CONF (1.58×/20); B d→sh CONF (1.79×/109); d→qot within-line BASELINE (0.99×) confirming F491 exclusively inter-line (F555). A d-LF pos1=qot CONF (1.92×/25) + ot CONF (1.72×/24) (F556). H_new_FF CLOSED.
**Source:** exp_534-541 completed template class quad + sh + ch. d-onset is the remaining major uncharacterized class: d is the dominant LF class in A herbal_a (~18% of LF, exp_467 F447), the CL chain anchor (d→qot→ch→o→sh, F491/F508), and has known within-line sub-CONF signals (d→ch 1.19×, d→sh 0.67× DEPL from exp_541 ch→d reverse). A complete 4-part d characterization would close the major-onset-class characterization program (template quad + sh + ch + d).
**Description:** Same 4-part methodology as exp_540-541. A herbal_a and B all: (1) d vocabulary; (2) positional distribution; (3) d within-line bigrams (d→X); (4) d-LF lines pos1 profile. Special focus: d LF rate (dominant LF class in A), d pos1 rate, d→ch coupling, d→qot within-line (distinct from CL coupling). Cross-reference with F491 (d→qot CL CONF) and F508 (d→t CL CONF) — do these couplings appear within-line or only cross-line?
**Expected outcome:** d is likely LF-elevated in A herbal_a. d→qot within-line may be elevated (complementing the CL signal). d vocab: A dominated by d-suffix words (daiin, dain, dy, dam); B by d-edy forms.
**Cost estimate:** small — direct reuse of exp_541 methodology
**Prerequisites:** none

## H_new_FE: B ch→t CONF (E=1.77×/obs=35) — section scope and A analog
**Priority:** medium
**Status:** RESOLVED → F551/F552 + F548 scope update (exp_542, 2026-04-11). B ch→t pooled CONF is B-PHARMA-PRIMARY: B pharma CONF (E=2.17×/obs=18); B astro near-CONF (E=1.54×/obs=9); B herbal baseline. NEW: B pharma ch→k CONF (E=1.79×/obs=27) — dual gallows routing {t, k} in B pharma (F551). NEW: B astro ch→l CONF (E=1.58×/obs=44), ch→k DEPLETED (F552). Section ch routing: B pharma=gallows {t,k}; B astro=lateral {l}. A herbal_a: all sub-CONF (flat). H_new_FE CLOSED.
**Source:** exp_541 (2026-04-11): B all ch→t CONF (E=1.77×/obs=35, F548). B ok-LF pos1=t CONF (F540) and B ch→t CONF both recruit t-onset as a structural "partner" in B-dialect. Is B ch→t herbal-specific or B-dialect-wide? Does A herbal_a ch→t approach significance? Also: ch→k (A: 1.35×/86; B: 1.36×/44) and ch→l (A: 1.37×/57; B: 1.37×/135) are consistently elevated in both dialects (below CONF) — worth testing pooled significance.
**Description:** (1) Break B all ch→t by section: B herbal vs B astro vs B pharma. If section-specific, update F548 scope. (2) Test A herbal_a ch→t specifically: E= how much above threshold? (3) Pooled test: ch→k and ch→l — are these structurally consistent below-CONF signals or noise?
**Expected outcome:** If B ch→t is B-herbal-specific (like some other B signals), scope narrows. If B-dialect-wide, F548 scope expands. A ch→t may be at (dir) level in a section subset.
**Cost estimate:** small — subset of exp_541 methodology
**Prerequisites:** none

## H_new_FA: A qok→qot CONF within-line (F542, E=2.22×/obs=12) — triplet structure and section scope
**Priority:** medium
**Status:** RESOLVED (exp_538, 2026-04-11). POSITIVE with scope limit: qok→qot CONF directed coupling (qot→qok sub-CONF 1.42×). NO triplet chain (8 cases spread across 6 targets). A-HERBAL-A SPECIFIC: A stars ZERO (E=0.00×); A cosmo DEPLETED (E=0.53×). F542 scope updated to herbal_a-specific.
**Source:** exp_537 (2026-04-11): A herbal_a qok→qot CONF (E=2.22×/obs=12). This is a NEW within-line directed coupling not previously documented. Does this create a triplet? qok→qot→(qot or y or qo)? Is this signal A-herbal_a-specific or broader?
**Description:** (1) For A herbal_a: extract all within-line qok→qot pairs (N=12). What comes after qot in those lines? Compute qok→qot→X distribution (triplet). (2) Test A sections: is qok→qot elevated in A stars, A cosmo? (3) Check: is A qot→qok also elevated (from qot bigrams: E=1.42×/obs=8, below CONF — asymmetric or symmetric)?
**Expected outcome:** If triplet structure exists: qok→qot→qot or qok→qot→y would suggest a within-line template chain (qok-class word followed by qot-class word, then qot recurse or y-terminate). If section-general: broader A-dialect rule.
**Cost estimate:** small — extract qok→qot pairs, check successors
**Prerequisites:** none

## H_new_EX: qok-onset full characterization — completing template class quad
**Priority:** high
**Status:** RESOLVED → F541/F542/F543 (exp_537, 2026-04-11). ANSWERED: qok follows qot/ot vocabulary architecture (A=ch-mediated ~29%, B=edy+eedy 23.5%). qok LF-depleted cross-dialectally (A: E=0.57×; B: E=0.58×) — unique among template classes. A qok→qot CONF (E=2.22×/obs=12, NEW directed coupling), qok→qok CONF (2.16×/obs=15), qok→y CONF (1.57×/obs=11). B qok flat (no CONF). Complete template quad: two-tier self-succession (qot/ot=both-dialect CONF; qok/ok=A-only); ot=only ch-depleter; ok=vocabulary diverger (aiin-dominated).

## H_new_EW: B astro qok→qok CONF — qok self-succession role: is qok a "topic continuation" class in B astro?
**Priority:** medium
**Status:** resolved — exp_532 (2026-04-11). NEGATIVE: qok-LF has NO chain beyond self-succession. qok→qok is an isolated CONF self-succession, not a chain starter. qok→qok→? triplets show no concentrated target. B astro CL = self-succession terminus, not a relay hub.
**Source:** exp_531 (2026-04-11): B astro qok→qok CONF (E=1.74×/obs=14, F495 from exp_516; confirmed exp_531). qok is depleted in pooled B herbal+pharma qok self-succession (E=0.87×). qok self-succession is B astro-specific and ABSENT in B herbal+pharma.
**Description:** Does B astro qok-LF have a multi-step CL chain (analogous to A herbal_a d→qot→ch→...)? What does qok route to beyond self-succession? Specifically: qok→qok→? — does the chain extend? Check: qok-LF as sender for all non-self receivers at E≥1.5× in B astro. Also: does qok self-succession correlate with specific folios (folio clustering risk)?
**Expected outcome:** If qok is a "topic pacing" class, it should have a CL chain with specific targets after self-succession. If it's a local pattern, it may be folio-clustered.
**Cost estimate:** small (B astro CL code from exp_531)
**Prerequisites:** none

## H_new_EV: B astro d→qo (dir) vs A herbal_a d→qot (CONF) — is qo the B-astro functional analog of qot in d-LF CL?
**Priority:** medium
**Status:** resolved — exp_532 (2026-04-11). NEGATIVE: qo-LF has flat sender profile (no signal above threshold). d→qo→? triplets spread across 6 targets with no concentration. qo is a CL terminal, not a pivot. The qo/qot analog hypothesis REFUTED.
**Source:** exp_531 (2026-04-11): B astro d→qo dir (E=3.08×/obs=8, F495/exp_531). A herbal_a d→qot CONF (F491). In A herbal_a, qot is the CL "pivot" class receiving from d; in B astro, the elevated successor is qo not qot. qo and qot are structurally related onset classes (gallows consonant cluster).
**Description:** Test whether B astro has a d→qo→? CL chain (analogous to A herbal_a d→qot→ch). Specifically: what does qo-LF route to in B astro CL? Is qo→ch (as qot→ch in A herbal_a) or qo→[other class]? Also: is qo elevated as a CL RECEIVER for other senders in B astro, suggesting it plays a pivot role?
**Expected outcome:** If qo is the B-astro qot-analog, we'd expect qo→ch or qo→[dominant class] CL in B astro. B astro qo N_cond=23 (from exp_531 output) — borderline power.
**Cost estimate:** small (specific CL analysis of B astro qo-LF sender profile)
**Prerequisites:** none

## H_new_EU: ot→ch cross-section CL scope — is this a universal or section-specific coupling?
**Priority:** medium
**Status:** resolved — exp_530 (2026-04-11). B herbal-SPECIFIC. ot→ch is DEPLETED in A herbal_a (E=0.78×/obs=6) and B pharma (E=0.87×/obs=12, large N, strong null). A stars f58 signal was folio-local noise. ot→ch is NOT a cross-section rule — F526 scope = B herbal only.
**Source:** exp_529 (2026-04-11): ot→ch appears at dir level independently in B herbal (E=2.63×/obs=5, F526) and within f58/A stars (E=3.04×/obs=3 (dir)). This cross-section appearance suggests ot→ch may be a broader grammatical coupling rule.
**Description:** Test ot→ch CL in: A herbal_a (N_cond≈38 ot-LF pairs), A cosmo, B astro (large section), B pharma. If ot→ch appears in multiple sections independently, it may be a cross-dialect CL rule. Also: check B herbal d→ok near-CONF (obs=9, E=1.75×) — whether pooling B herbal + B pharma or additional data can push to CONF.
**Expected outcome:** A herbal_a ot-LF has N_cond≈38 pairs; if ot→ch is enriched at E=2.0×, expected obs ≈ 15 × 0.169 × 2 = 5 obs at dir level. B astro has large N — powerful test. If ot→ch is found CONF in A herbal_a or dir in B astro, this becomes a multi-section CL rule.
**Cost estimate:** small (subset of existing CL code from exp_511-528)
**Prerequisites:** none

## H_new_ET: Why is A stars CL grammar flat? Power issue vs true structural absence
**Priority:** medium
**Status:** resolved — exp_529 (2026-04-11). DUAL ANSWER: (1) POWER ISSUE: f58 (72 pairs) shows 3 (dir) signals (ok→ch, ot→ch, a→d) — A stars IS NOT flat, it's folio-local. Pooled 131 pairs cannot detect folio-local signals averaging across different folios. (2) STRUCTURAL DIFFERENCE: A stars lacks a shared section-wide CL chain. Individual folios have different CL patterns (f67: o→o; f68: d→d; f58: ot→ch, ok→ch, a→d). A herbal_a's chain is a section property; A stars patterns are folio-local.
**Source:** exp_528 (2026-04-11): A stars CL (131 pairs) shows NO signals at (dir) or above in pooled analysis. The A herbal_a chain does not replicate. Is this because A stars genuinely lacks CL coupling structure, or because 131 pairs is insufficient power?
**Description:** Power analysis: A herbal_a CL chain links have E=1.5-3.0× with obs=4-11 across 922 pairs. With 131 pairs (14% of A herbal_a), expected obs for the same E would be 14% as large — barely above threshold or below threshold. Additionally: folio 58 dominates (72/131 pairs), and within f58 the patterns are different from cross-folio pooling. Test: (a) compute what E would be needed for detection at 131 pairs; (b) check if f58 alone has CL patterns not visible in pooling.
**Expected outcome:** If A stars truly has no CL grammar: pooling more A stars data (if available) would still give flat results. If it's a power issue: within-folio analysis of f58 (largest folio) should show some directionality consistent with the A herbal_a chain.
**Cost estimate:** small (within-f58 CL analysis is ~50 lines)
**Prerequisites:** none

## H_new_ES: A stars cross-LF-class a-onset role — is a-onset a structured constituent in A stars grammar?
**Priority:** medium
**Status:** resolved — exp_533 (2026-04-11). CONFIRMED STRUCTURAL: a-onset is a cross-class "non-opener" in A stars. pos1 near-zero (0.8%, 1/130, E≈0.07×); pos2=14.8% (CONF vs A herbal_a); pen=9.8% (CONF). Within-class: only ot-LF pos2=a (dir, F520) and sh-LF pen=a (dir, F519) elevated; d/ch/y/s all depleted. F532: positional complementarity t/s=OPENERS (CONF), a=NON-OPENER (near-zero pos1).
**Source:** exp_526 (2026-04-11): Multiple A stars LF classes show a-onset enrichment in specific positions: sh-LF pen=a ((dir), F519); ot-LF pos2=a ((dir), F520). Also: a-LF itself is 11% of A stars LF (high frequency). Is a-onset playing a structured grammatical role within A stars lines — appearing at specific positions for multiple LF classes — rather than being random background frequency?
**Description:** Compute cross-LF-class a-onset rates at each position (pos1, pos2, pen) in A stars. Pool ALL a-onset appearances at each position regardless of LF class. Compare A stars a-onset rates at each position to A stars baseline (overall pos1/pos2/pen distributions). Also: does a-onset at pen correlate with specific LF classes beyond sh-LF? Does a-onset at pos2 correlate with ot-LF specifically or more broadly?
**Expected outcome:** If a-onset is structurally elevated at pen or pos2 across multiple LF classes, this suggests a-onset words have a specific syntactic/grammatical slot in A stars lines — consistent with A stars being a specialized section (zodiac/calendar) with section-specific vocabulary roles.
**Cost estimate:** small (A stars 136 lines; cross-class a-onset tallying)
**Prerequisites:** none

## H_new_ER: A stars a-LF grammar — what is the positional grammar of the 3rd-ranked LF class in A stars?
**Priority:** high
**Status:** resolved — exp_526 (2026-04-11). NEGATIVE: A stars a-LF grammar is FLAT at all positions. No confirmed/dir/(dir) rules. a-self@pos2 E=1.04× (baseline — no pos2 self-chaining, unlike all other A stars LF classes). y DEPLETED at pos1. a-LF appears grammatically inert within-line. The high frequency of a-LF in A stars (11%) is not accompanied by a detectable within-line grammar signature. a-LF is likely a topic/section marker rather than a grammatical class with internal structure in A stars.
**Source:** exp_525 (2026-04-11): A stars LF distribution shows a-LF is 11.0% of LF (3rd rank), behind d(18.4%) and ch(16.9%). a-LF has NO confirmed within-line grammar rules in ANY section. In B herbal, F470 claims a→a@pos2 dir; scope limited. In A herbal_a, a-LF is only ~1.4% of LF (rare), making A stars the best location to study a-LF grammar.
**Description:** For A stars a-LF lines (~15 estimated): compute full pos1, pos2 (len≥3), pen (len≥3) routing distributions with A-stars baselines. Key questions: (1) Does a-LF have a-self@pos2 self-chaining? (2) What class opens a-LF lines at pos1 — y-opening or a-self? (3) Any pen routing signal? Cross-section comparison with B herbal a-LF (F470: a→a@pos2 dir).
**Expected outcome:** With N≈15 a-LF lines, N_elig≈12-14 at pos1. At dir threshold (obs≥5, E≥2.0×), stable signals are findable. a-self@pos2 self-chaining is the primary candidate. a-LF is distinctive for being high-frequency in A stars (11%) but rare in A herbal_a (~1.4%).
**Cost estimate:** small (A stars corpus 136 lines; standard positional profile code)
**Prerequisites:** none

## H_new_EQ: A herbal_a t-LF CL role — what does t-LF route to? Is it a relay or terminal?
**Priority:** high
**Status:** resolved — exp_524 (2026-04-11). t is a RELAY: routes toward d (E=1.47×/obs=11, just below CONF), also →y ((dir), F512), →ot ((dir), F513). ch STRONGLY DEPLETED after t (E=0.19×/obs=1). t-LF pos1=o new dir (F515). ok@pen (dir). t is a content-switch relay that connects back toward d without going through the qot/ch chain.
**Source:** exp_523: t-LF receives from d (F508, CONF) and from sh (F510, (dir)). t is a multiply-fed downstream destination. But what does t-LF then send to? t-LF is not a very common LF class in A herbal_a (estimated ~3-5% from LF distribution). If t→qot or t→d, t would be a cycle-closing relay. If t has no elevated successors, it's a terminal sink.
**Description:** For A herbal_a t-LF CL: compute all X-receiver distributions (t-LF followed by X-LF). Focus: does t→d, t→qot, or t→ch (which would create partial cycles)? Also compute full within-line grammar for t-LF in A herbal_a (pos1, pos2, pen). Does t have any confirmed within-line rules?
**Expected outcome:** t-LF in A herbal_a is a minority class (estimated N_cond~30). Unlikely to find CONF signals unless E is very high. May find (dir) or directional signals. Key question is whether t routes back into the chain or diverges.
**Cost estimate:** small (same CL code as exp_523, additional within-line grammar)
**Prerequisites:** none

## H_new_EP: A herbal_a ok-LF CL routing — what follows ok-LF? (sh→ok dir established; does ok then route?)
**Priority:** medium
**Status:** resolved — exp_524 (2026-04-11). ok does NOT route back to d (DEPLETED 0.63×) or qot (flat). ok→ol NEW (dir, F514). sh→ok confirmed from receiver side. ok-LF pos1=s NEW dir (F516, E=2.22×/obs=5). No chain cyclicity via ok.
**Source:** exp_523 established sh→ok (F509, dir). ok-LF has confirmed within-line grammar (F485: ok-self@pen CONF; F455: ok→y@pos1 FLAGGED). But ok-LF's CL role as a SENDER is uncharacterized. Does ok route to d (beginning the chain anew), to qot, or to some other class?
**Description:** For A herbal_a ok-LF CL: compute all X-receiver distributions (ok-LF followed by X-LF). N_cond~52 (ok-LF ~5.6% of 922 pairs). Also: which classes PRECEDE ok-LF (receiver side) — we know sh→ok, but what else?
**Expected outcome:** With N_cond~52 and CONF threshold at obs≥10, any E≥1.5× rule with obs≥10 would be CONF. ok may route back to d (completing a partial cycle d→...→sh→ok→d?) or to ch or some other class.
**Cost estimate:** small (subset of exp_523 code)
**Prerequisites:** none

## H_new_EN: Per-page A stars section reclassification — enable H_new_EJ and expand A stars survey pool
**Priority:** high
**Status:** resolved — exp_525 (2026-04-11). NEGATIVE: Per-page classification produces IDENTICAL 136-line A stars set as folio-number grouping. The B-dialect pages in 57-72 (f57r, f65v, f66r, f66v) are already correctly excluded by folio-number methodology. No expansion. H_new_EJ is therefore NOT blocked by methodology — t-LF is simply not elevated in A stars (E=0.51× DEPLETED). F446 discrepancy traced to possible different corpus/script (Q011 raised).
**Source:** exp_522 blocked H_new_EJ: the folio-number grouping combines both sides of f57r/f57v etc. when one is B-dialect and one is A-dialect, causing those folios to exceed 5% edy threshold and be excluded from A stars. F446 found N=15 t-LF lines using per-page classification (each page name separately). Per-page classification would recover these pages and enable H_new_EJ + a comprehensive A stars grammar survey.
**Description:** Modify the corpus parser to use per-page names (e.g., "f57r", "f57v") as the grouping key instead of integer folio numbers. Compute is_b_dialect per page name. Then redefine A stars = pages with page-level name in 57-72 range AND not is_b_dialect. Compare resulting A stars size to current (136 lines, 5 folios). With per-page classification, A stars should recover the A-dialect pages that share folio numbers with B pages (f57v, f58r, f58v, etc.) and expand to match F446's N=15 t-LF count.
**Expected outcome:** A stars expands from 136 lines (5 folio-numbers) to ~180-220 lines, enabling t-LF pos1 grammar survey with N_elig≥10. F503 and other A stars findings should get corrected obs counts.
**Cost estimate:** small (modify one function in the corpus parser; rerun A stars surveys)
**Prerequisites:** none

## H_new_EM: A herbal_a CL chain cyclicity — does sh-LF route back to d or qot (completing the loop)?
**Priority:** high
**Status:** resolved — exp_523 (2026-04-11). NOT CYCLIC. sh→d DEPLETED (E=0.57×/obs=6); sh→qot ZERO (E=0.00×/obs=0). Chain d→qot→ch→o→sh is LINEAR. sh branches to ok (dir, F509) and t ((dir), F510). Also NEW: d→t CONF (F508) — d has two confirmed CL channels. t-LF is multiply-fed by both d and sh.
**Source:** exp_522 established d→qot→ch→o→sh (4 links, 3 CONF + 1 dir). The chain may be: (a) a terminal sequence ending at sh, (b) an open-ended chain that continues past sh, or (c) a cyclic structure where sh connects back to d or qot. Cyclicity would make this a grammatical "loop" — a recurring paragraph-level structure that repeatedly generates the same LF-class sequence.
**Description:** For A herbal_a sh-LF CL (sh as sender): compute all X-receiver distributions (sh-LF followed by X-LF). Focus: is d or qot elevated after sh? sh_N≈38, so within-folio CL pairs with sh as sender: ~38 pairs. Also compute sh as receiver from all classes (full X→sh survey) to see if sh is being "fed" by the chain at the rate predicted by o→sh (F507).
**Expected outcome:** If sh→d (E≥1.5×), the chain would be cyclic: d→qot→ch→o→sh→d. If sh→qot (E≥1.5×), the cycle would be shorter: sh→qot→ch→o→sh. If sh has no elevated successors, the chain is a 5-link open sequence ending at sh. Also expected: sh as a receiver — is sh elevated after o? (should confirm F507 from the receiver side)
**Cost estimate:** small (within-folio CL pairs for A herbal_a already computed in exp_511; sh-LF subset is tractable)
**Prerequisites:** none

## H_new_EL: A herbal_a sh-LF within-line grammar — pos1/pos2/pen routing for the 5th chain link
**Priority:** high
**Status:** resolved — exp_523 (2026-04-11). NO confirmed rules: pos1/pos2/pen all below CONF or dir. sh-self@pos1 E=1.83×/obs=6 (below dir); ok@pos1 E=1.84×/obs=4 (below dir); y DEPLETED 0.74×. pos2: cth DEPLETED (0.00×); d E=1.54×/obs=5 (below CONF). pen: d E=1.47×/obs=8 (below CONF). sh-LF is internally Markovian — its grammatical distinctiveness is CL-level, not within-line.
**Source:** sh-LF is now the 5th link in the A herbal_a CL chain. sh has no confirmed within-line grammar rules yet: sh-self@pos2 is BELOW CONF (F463 corrected E=1.53×/N=8); pen: d@pen E=1.48× below threshold; pos1: sh-self E=2.55×/N=9 dir. What is the within-line grammar of sh-LF? As the chain endpoint, does sh have distinctive internal grammar (like o-LF which has y@pos1 and o-self/cth at pos2)?
**Description:** For A herbal_a sh-LF (N=38): compute full pos1, pos2 (len≥3), pen (len≥3) routing distributions with proper baselines. Compare with o-LF grammar (the chain predecessor) and other chain members. Key: does sh-LF show y@pos1 (like o-LF and ot-LF)? Does sh-LF have any distinctive pen routing?
**Expected outcome:** sh-self@pos1 stays dir (E=2.55×/N=9). y@pos1 may be elevated for sh (cross-class). pen may show some ch or d enrichment. With N=38 total lines and len≥3 filter, N_elig≈30-35 for pos1.
**Cost estimate:** small (standard positional profile, same code as exp_522)
**Prerequisites:** none

## H_new_EJ: A stars t-LF pos1 routing — what is the positional grammar of A stars' dominant LF class?
**Priority:** high
**Status:** resolved — exp_522 (2026-04-11). CLOSED — exp_525 confirmed: per-page reclassification gives IDENTICAL A stars (136 lines). t-LF in A stars: N=2/136 (1.5%), E=0.51× DEPLETED vs A herbal_a (2.9%). t-LF is NOT elevated in A stars. H_new_EJ is definitively closed: not a methodology artifact, t-LF simply rare in A stars. F446 claim of N=15 t-LF is CONTRADICTED — Q011 raised.
**Source:** F446 (exp_466): A stars t-LF elevated at 2.12×/N=15. A stars has only one confirmed pos1 rule so far: F503 (o-LF→y, dir). But t-LF is the dominant LF class in A stars (much more common than o-LF). What is the pos1 routing for t-LF in A stars? H_new_AH (open) hints at pos2=ot (E=4.93×/N=3, dir) but pos1 is unknown. In A herbal_a, there is no t-LF confirmed pos1 rule; in B sections, t-LF pos1 is near-Markovian. A stars may have a t-LF pos1 signature consistent with its unique LF-class grammar.
**Description:** For A stars (57-72 A-dialect): compute full pos1 routing for t-LF lines (N_lf~15, len≥3). Check: is any class elevated at pos1 for t-LF? Also compute pos2 routing (to test H_new_AH: pos2=ot at E=4.93×/N=3). Additionally: compute pos1 routing for the other major A stars LF classes (d, s, y, ch) with N_lf≥5. This gives the first comprehensive A stars within-line grammar survey.
**Expected outcome:** t-LF may route through sh/y/ch at pos1 (consistent with A continuation grammar). Or t-LF may have a section-specific pos1 routing in A stars. H_new_AH's pos2=ot may upgrade from directional to dir if additional cases are found.
**Cost estimate:** small (A stars corpus is only 136 lines; full pos1/pos2 survey is tractable)
**Prerequisites:** none

## H_new_EI: o-LF pos2 and pen grammar — characterize full within-line structure of the broadest-scope LF rule
**Priority:** high
**Status:** resolved — exp_522 (2026-04-11). PARTIAL POSITIVE: A herbal_a o-LF pos2=o-self (E=3.06×/obs=3, (dir), F504); pos2=cth (E=2.75×/obs=4, (dir), F505). pen: no signal (sh E=1.97×/obs=5, below dir). y-opening subtype pen: fragmented N (max obs=2 per class). A stars o-LF pos2=o-self also (dir) (E=4.17×/obs=4). The o-LF within-line structure is primarily at pos2 (o-self and cth enrichment), not pen. This contrasts with ot-LF where pen has two confirmed routing rules. Hypothesis closed — further data not available without per-page section reclassification.
**Source:** F502 (CONF): o-LF pos1=y confirmed in pooled A herbal+stars. All three O-onset LF classes (ok, ot, o) have elevated pos1=y, but only ot-LF has characterized pos2/pen grammar. o-LF pos2 and pen are completely uncharacterized — we don't know if y at pos1 correlates with specific pos2 routing or pen routing (as seen with ot-LF: y-opening→ot-self@pen; standard→cth@pen).
**Description:** For A herbal_a o-LF (N_elig~28, len≥3): (1) compute full pos2 routing distribution; (2) compute full pen routing distribution; (3) test y-opening vs standard subtype split for pen routing (does y at pos1 predict different pen outcome for o-LF, as seen with ot-LF?). Also check A stars o-LF pos2/pen (N_elig=13, smaller). Cross-compare with ot-LF grammar to see if the template structure is parallel.
**Expected outcome:** o-LF pos2 may show y-self elevation (paralleling ot-LF pos2=y at E=3.60×). o-LF pen may show o-self or some other class. The y-opening subtype may have different pen routing from standard subtype (ot-LF precedent). With N_elig=28 in A herbal_a, expect directional rather than CONF findings.
**Cost estimate:** small (targeted survey, no new corpus parsing)
**Prerequisites:** none

## H_new_EF: ot-LF pos2=a elevated in A herbal_a (E=3.23×/obs=4, (dir)) — confirm or artifact?

**Priority:** medium
**Status:** resolved — exp_521 (2026-04-11). ARTIFACT. In strict A herbal_a (1-56): ot-LF pos2=a obs=0 (E=0.00×). The apparent (dir) signal from exp_520 was caused by wrong A herbal_a definition (1-72 included A stars). In the correct 1-56 definition, there are zero ot-LF lines with pos2=a. Closed negative.

## H_new_EG: o-LF pos1=y cross-section scope audit — do F455/F456 E-values shift with corrected A herbal_a definition?

**Priority:** high
**Status:** resolved — exp_521 (2026-04-11). KEY FINDING: F456 CONFIRMED at pooled level (ot-LF E=1.64×/obs=12 CONF in 1-72 A-dialect). F455 NOT REPRODUCIBLE at CONF — ok-LF: strict 1-56: E=1.38×/obs=9; pooled 1-72: E=1.22×/obs=10 — both below E=1.5 CONF threshold. F455 methodological discrepancy flagged → Q010 raised. ok-LF pos1=y is likely directional but not CONF under current methodology.

## H_new_EH: A stars o-LF pos1=y at CONF level — can we pool A herbal_a + A stars for CONF?

**Priority:** medium
**Status:** resolved — exp_521 (2026-04-11). POSITIVE: Pooled A herbal+stars (1-72 A-dialect): o-LF E=2.45×/obs=15/N_elig=41 → **CONF**. First CONF-level confirmation of o-LF pos1=y. F502 upgraded to CONF at pooled level.

## H_new_DK: A herbal_a ot-LF → y at pos2: Confirm or close (N currently=4, E=3.60×)

**Priority:** medium
**Status:** resolved — exp_519 (2026-04-11). STAYS (dir): ot-LF pos2=y remains E=3.60×/N=4 ((dir) threshold, E≥2.5×/N≥3). N=4 is one below dir. NEW: ot-LF pos2=k discovered at E=2.07×/N=5 (dir). pos2=ch DEPLETED (E=0.80×). F498 added for pos2=k dir + ch depletion. y at pos2 remains (dir) — insufficient N for dir confirmation without more data.
**Source:** exp_518 (2026-04-11) — inline pos2 survey found ot-LF pos2=y: obs=4/N_elig=40, E=3.60×. This is directional (E≥2.0×/N=4) but NOT dir (N<5). exp_513 also found E=3.25×/N=5. Combined evidence suggests this is real but underpowered. With N_elig=40, the E is stable; the question is whether a targeted test with all eligible lines produces N≥5 (needed for dir) or N≥10 (needed for CONF).
**Description:** Run a dedicated ot-LF pos2 survey in A herbal_a (A-dialect only, len≥3). Focus: ot-LF → y@pos2 enrichment. Compute exact obs/exp/E with full baseline. Also check ot-LF pos2 full distribution (what does pos2 look like for ot-LF? Multiple classes?).
**Expected outcome:** If obs=4 from N_elig=40 is stable: E=3.60×/N=4 stays just below dir. Need obs≥5 for dir or obs≥10 for CONF. At E=3.6×, need only N=5 for dir — this may be achievable with careful eligibility filter. The ot-LF paragraph role (pos1=y CONF, pos2=y dir, pos2=cth dir) would become clearer.
**Cost estimate:** trivial (targeted pos2 survey, no new corpus parsing)
**Prerequisites:** none

## H_new_DJ: Scope of A cosmo cth CL rules in A herbal_a

**Priority:** medium
**Status:** resolved — exp_519 (2026-04-11). FLAT in A herbal_a. cth→cth E=1.29×/N=7; cth→ol E=0.68×/N=1; ch→ol E=0.56×/N=2 — all near or below baseline. The A cosmo cth CL signals were f93-driven artifacts; they do not appear in A herbal_a. cth has no confirmed CL rules in any section.
**Source:** exp_518 (2026-04-11) — A cosmo cth→cth CL (E=7.25×/N=4) and cth→ol CL (E=5.89×/N=3) discovered with proper A-dialect filter. Are these A cosmo-specific, or do they appear in A herbal_a too? A herbal_a has N_pairs=1133 (much larger), so a test there would be higher power.
**Description:** In A herbal_a within-folio CL pairs: check cth→cth and cth→ol enrichment. Baseline is A herbal_a section-specific (exp_511 methodology). Also check ch→ol in A herbal_a (E=2.06×/N=5 in A cosmo — is ch also routing to ol in herbal_a?).
**Expected outcome:** cth-LF is ~5% of A herbal_a LF — N_pairs involving cth≈57. cth→cth: if E=7.25× holds, expected obs≈ 57×0.05×E = 3 × 7 = ~21? Actually E = obs / (base_cth × base_cth × N) = obs / (0.05×0.05×1133) = obs/2.83. For obs=21, E=7.4×. But more likely E is lower in herbal_a. If flat (E=1.0×), obs≈3. Testing whether cth→cth is A cosmo-specific or broader.
**Cost estimate:** trivial (inline addition to A herbal_a CL pairs already computed)
**Prerequisites:** none

## H_new_DI: A cosmo CL → ol: Multiple classes route to ol? Full ol-destination survey

**Priority:** medium
**Status:** resolved — exp_519 (2026-04-11). PARTIAL: Only ch→ol (E=2.06×/N=5, dir) survives as non-artifact sender. cth→ol is the f93 clustering artifact. ol→X receivers all N=1-2 (underpowered). ol is not a confirmed CL "relay" — just a moderate destination for ch in A cosmo.
**Source:** exp_518 — A cosmo CL survey shows TWO senders routing to ol: cth→ol (E=5.89×/N=3) and ch→ol (E=2.06×/N=5). This is unusual — ol-LF is a relatively rare destination class that is now the target of two independent senders. Is ol a special "sink" in A cosmo CL? What are ALL classes routing to ol, and what does ol then route to?
**Description:** In A cosmo (A-dialect only, N=286 pairs): compute all X→ol pairs and ol→X pairs. Compare with A herbal_a ol CL distribution. Does ol self-succeed? Is ol a terminal sink or a relay? Also: check ol's LF class rate in A cosmo vs A herbal_a (ol may be more prominent in A cosmo, explaining why senders route to it).
**Expected outcome:** ol-LF rate in A cosmo exp_518 top-LF: not in top 8 (top 8 = ch:62, d:48, ok:26, s:23, o:17, sh:17, qok:16, ot:14). So ol is below these. Expected low N. But the two-sender pattern (cth→ol + ch→ol) may still be revealing.
**Cost estimate:** trivial (subset of exp_518 CL survey already done)
**Prerequisites:** none

## H_new_DV: y-opening as grammar-mode switch — does pos1=y suppress LF-self@pen across all LF classes?

**Priority:** high
**Status:** resolved — inline (2026-04-11). PARTIAL: y-opening is NOT a uniform self-chain suppressor. LF-class-specific effects: ok-LF→ZERO self-chain (complete suppression); ot-LF→ENHANCED self-chain; ch-LF→weak suppression; d-LF→new y@pen signal. Pattern: y-opening changes pen grammar differently per LF class. Consistent with y-opening being a "grammar mode" but the mode is class-specific. F485 note added: ok-self@pen is standard-subtype-only. New H_new_DW for d-LF y-bracket template.

## H_new_EA: B astro o-LF pos1=y (E=2.55×/N=3, (dir)) — unexpected cross-dialect signal, verify

**Priority:** medium
**Status:** resolved — inline (2026-04-11). GENUINE (dir): B astro baseline y@pos1 = 6.2% (41/662) — much lower than A herbal_a's 14.8%. With this lower baseline, E=2.55×/N=3 is not a baseline artifact. Cross-section check: B astro pos1=y enrichment is class-specific — o-LF E=2.55× (dir), k-LF E=3.23×, d-LF E=1.72× — y is not generally inflated for all B astro LF classes. o-LF pos1=y in B astro is genuine. F502 scope extended: A herbal_a (dir) + A herbal_b (dir) + B astro ((dir)). The o-LF y-opening rule has cross-dialect reach.
**Source:** inline H_new_DZ (2026-04-11) — B astro o-LF has pos1=y at E=2.55×/N=3. This is unexpected: the y-opens-o-onset rule was found in A herbal_a and confirmed in A herbal_b. Finding it in B astro suggests it may be a manuscript-wide (or at least A+B astro shared) rule for o-LF, not herbal-specific. With N=3 it meets (dir) threshold.
**Description:** For B astro o-LF lines (N_elig=19, len≥3): compute exact E for pos1=y using B astro section baseline (not A herbal_a baseline). Compare with B astro's overall pos1 grammar (F430: qok-formula). Is y specifically elevated for o-LF in B astro, or is y elevated for many B astro LF classes?
**Expected outcome:** If B astro's baseline has low y at pos1 for all LF classes, then E=2.55× is a genuine o-LF signal. If B astro has high y@pos1 generally (for all classes), then it may be a baseline artifact.
**Cost estimate:** trivial
**Prerequisites:** none

## H_new_DZ: O-onset LF cluster y-opening scope — does the pattern extend beyond A herbal_a?

**Priority:** medium
**Status:** resolved — inline (2026-04-11). POSITIVE: o-LF pos1=y extends to A herbal_b (E=2.25×/N=6, dir). Combined herbal A obs=15/N=41, E≈2.47×/N=15 (dir). A cosmo: E=1.50×/N=4 (near-threshold). B astro: E=2.55×/N=3 ((dir) — unexpected). Scope of o-LF pos1=y is HERBAL-WIDE (both A herbal_a and herbal_b). Contrasts with ok-LF (herbal_a-specific: herbal_b E=0.54×) and ot-LF (herbal_a-specific). F502 confirmed as herbal-wide.
**Source:** F502 (inline 2026-04-11) — all four o-onset LF classes (ok,ot,o,ol) have elevated pos1=y in A herbal_a. F455 and F456 (ok,ot) were already tested for herbal-section-specificity. F476 (ot-LF pos1=y) is confirmed herbal-section-specific (A cosmo: ot-LF pos1=y DEPLETED). Does o-LF also follow this pattern? Is the "y-opens-o-onset-LF" rule herbal-specific or A-dialect-wide?
**Description:** For A cosmo, A stars, B herbal o-LF lines (len≥3): compute E for pos1=y. A cosmo has small o-LF N (~10-15 lines). A stars has different LF class distribution. B herbal may have o-LF lines too. This extends the scope testing of F455/F456 to the o-LF class.
**Expected outcome:** Given that F455/F456 are herbal-specific, o-LF pos1=y is likely also herbal-specific. But this needs verification.
**Cost estimate:** trivial
**Prerequisites:** none

## H_new_DY: A herbal_a o-LF → y at pos1 (E=2.17×/N=9) — confirm new directional finding

**Priority:** high
**Status:** resolved — inline (2026-04-11). CONFIRMED dir: o-LF pos1=y E=2.17×/N=9 (dir threshold met: E≥2.0×/N≥5). o-LF pos1 full dist: y(9), sh(4), d(3), t(2), ot(2), o(2), qok(2). y is the top pos1 class for o-LF lines. O-onset cluster: all four o-onset LF classes (ok,ot,o,ol) have elevated pos1=y. F502 added.
**Source:** inline H_new_DX (2026-04-11) — o-LF has y-opening rate 9/28 = 32.1%, pos1_y_E=2.17×/N=9. This exceeds the dir threshold (E≥2.0×/N≥5) and was not previously established. F455 (ok-LF pos1=y CONF) and F456 (ot-LF pos1=y CONF) are known. o-LF pos1=y is a new dir signal that may be worth CONF-testing.
**Description:** For A herbal_a o-LF lines (N_elig=28, len≥3): compute exact E for pos1=y using the section-wide pos1 baseline. Check: is E≥2.0×/N≥5 confirmed? o-LF pos1 full distribution (what other classes appear at pos1 for o-LF lines). Compare with ok-LF and ot-LF pos1 profiles — do all three "o-onset" LF classes (ok, ot, o) share y at pos1 grammar?
**Expected outcome:** E=2.17×/N=9 from H_new_DX: this is computed as yo_rate/y_base_p1, which is correct for the dir calculation. If the exact calculation matches, this is a new dir finding. The key question: does o-LF join ok and ot in having a confirmed pos1=y rule?
**Cost estimate:** trivial
**Prerequisites:** none

## H_new_DW: d-LF y-opening subtype: y[pos1]→...→y[pen]→d[LF] — confirm y-bracket template

**Priority:** medium
**Status:** resolved — inline (2026-04-11). POSITIVE: Not a 3-word artifact. d-LF y-opening y@pen with len≥4: E=3.23×/N=3 ((dir): E≥2.5×/N≥3). Standard: E=1.05×. All 3 lines have y distributed at multiple positions: y[1],y[3],y[5]=pen in 6-word line; y[1],y[5]=pen in 6-word line; y[1],y[3]=pen in 4-word line. y-bracket d-LF template confirmed. F501 added.
**Source:** inline H_new_DV (2026-04-11) — d-LF y-opening (pos1=y, N=27): y@pen obs=3, E=2.63× ((dir): E≥2.5×/N≥3). Standard d-LF: y@pen E=1.14×. The y-bracket template y[pos1]→...→y[pen]→d[LF] would be a striking symmetric structure. With N=3, this is at the threshold but just barely meets (dir).
**Description:** For A herbal_a d-LF y-opening lines (pos1=y, N=27): compute exact E for pen=y. Record the 3 lines that have y@pos1 AND y@pen. Are they all short (2-word or 3-word lines)? If yes, this might be pos1=y AND pen=y for 3-word lines where pos2=pen, not a genuine independent finding. Check: for d-LF y-opening lines with len≥4 (excluding cases where pos2=pen), does y@pen survive?
**Expected outcome:** If the y-bracket signal is genuine: y appears at pen in more than baseline rate specifically in y-opening d-LF lines. If it's a 3-word artifact: the 3 lines might all be len=3 (pos1=y, pos2=y/d, LF=d, and pen=pos2=y).
**Cost estimate:** trivial (check line lengths and word-level detail of the 3 matching lines)
**Prerequisites:** none

## H_new_DX: y-opening subtype rate by LF class — does rate correlate with confirmed pos1=y rule strength?

**Priority:** medium
**Status:** resolved — inline (2026-04-11). ANSWERED. Key findings: (1) ot(E=1.52×,CONF) and ok(E=1.32×,CONF) have elevated y-opening rates consistent with their confirmed rules; (2) o-LF yo_rate=32.1%, pos1_y_E=2.17×/N=9 — NEW directional finding for o-LF pos1=y (not previously established!); (3) ch(E=0.49×) and d(E=0.78×) actively AVOID y at pos1 — their y-opening lines are "exceptional grammar" cases; (4) ol-LF has yo_rate=25%, E=1.68×/N=5 (borderline). New H_new_DY for o-LF pos1=y confirmation.
**Source:** inline H_new_DV (2026-04-11). y-opening rates: ot=22.5%, ok=19.6%, cth=15.6%, d=11.5%, ch=7.2%. ot and ok both have CONF pos1=y rules (F455, F456). d, ch, sh have no confirmed pos1=y. Hypothesis: the y-opening subtype rate is proportional to the pos1=y rule strength — LF classes with strong pos1=y rules have more y-opening lines because those grammar rules fire more often.
**Description:** For all A herbal_a LF classes with N≥20: compute (1) y-opening rate = P(pos1=y | LF=X), (2) pos1=y E-value. Check if rate and E are correlated. Also: what are qot-LF and y-LF y-opening rates? (Both may have high rates since qot has pos1=y elevated and y-LF trivially has pos1=y often.)
**Expected outcome:** If y-opening rate reflects pos1=y rule strength: ot (CONF, E=1.83×) and ok (CONF, E=1.62×) should have highest rates. cth (dir, E=3.59×/N=6) might also be elevated. d (pos1=ot CONF, not y) should have lower rate. Results would clarify whether y-opening is just "lines where the pos1=y rule happened to fire" or a distinct grammatical category.
**Cost estimate:** trivial
**Prerequisites:** none

## H_new_DT: ot→cth@pen in "non-y-opening" ot-LF lines — conditional CONF test

**Priority:** high
**Status:** resolved — inline (2026-04-11). POSITIVE: non-y-opening ot-LF (pos1≠y, N=31): pen=cth E=4.19×/N=8 (dir). Stronger than aggregate E=3.66×. Standard-opener ot-LF template: ?[pos1≠y]→...→cth[pen]→ot[LF]. F500 added. pen=ch DEPLETED (E=0.72×/N=6). The y-opening and standard-opening subtypes are confirmed as having distinct pen grammar: ot-self vs cth.
**Source:** inline (2026-04-11) — ot-LF pen dissection reveals cth@pen is concentrated in "neither" subtype (non-y-opening, non-k-routing, N=27): E=3.61×/N=6 (dir). Combined with k-routing (N=4): 8/9 total cth@pen cases come from non-y-opening lines. The non-y-opening ot-LF template: ?[pos1, not y] → ...→ cth[pen] → ot[LF]. This is a conditional rule that may reach CONF with all non-y-opening ot-LF lines.
**Description:** For A herbal_a ot-LF lines where pos1≠y (N=31): compute E for pen=cth using section-wide baseline. Expected: 8/31 = 25.8% vs baseline ~6.1% → E≈4.2×/N=8 → should be dir and possibly approaching CONF. Check if this subtype's pen=cth is confirmed at higher N than the aggregate.
**Expected outcome:** E≈4× with N=8 in non-y-opening subtype. Not CONF (needs N≥10) but strong dir. The conditional finding would establish that the ot→cth@pen exp_506 signal is specifically the "standard-opener" ot-LF grammar.
**Cost estimate:** trivial
**Prerequisites:** none

## H_new_DU: ot→cth@pen signal in other A-dialect sections (scope test)

**Priority:** medium
**Status:** resolved — inline (2026-04-11). A herbal_a-SPECIFIC: A cosmo ot-LF pen=cth obs=0 (E=0.00×); A stars ot-LF pen=cth obs=0 (E=0.00×). Section-specific ot-LF pen grammar: A herbal_a→cth+ot, A cosmo→ch dominant, A stars→qok+ok+ch. Consistent with overall finding that positional grammar is section-specific even within A dialect.
**Source:** F499/inline — A herbal_a ot-LF pen=cth: E=3.66×/N=9 overall (dir). Does this extend to A cosmo ot-LF or other A sections? If universal across A dialect, it may be a fundamental A-dialect ot-LF grammar rule. If A herbal_a-specific, it's section-specific.
**Description:** For A cosmo and A stars ot-LF lines (len≥3): compute E for pen=cth. Compare with A herbal_a result. Expected small N in other sections (ot-LF is ~5% in A cosmo; A cosmo has 296 lines → ~15 ot-LF lines).
**Expected outcome:** A cosmo ot-LF pen=cth may show similar direction if rule is A-dialect-wide. But N~8-10 in A cosmo may be insufficient for confirmation.
**Cost estimate:** trivial
**Prerequisites:** none

## H_new_DS: ot-LF y-opening subtype pen=ot template: test at CONF level in all A herbal_a ot-LF lines

**Priority:** high
**Status:** resolved — inline (2026-04-11). POSITIVE: All ot-LF pen=ot: E=3.27×/N=6 (dir). Within y-opening subtype: E=7.27×/N=3 ((dir) conditional). 50% of all ot-LF pen=ot cases concentrated in y-opening subtype. Template: y[pos1]→...→ot[pen]→ot[LF]. Not CONF (N=6 < 10) but directional at aggregate level. F499 added.
**Source:** inline H_new_DQ (2026-04-11) — ot-LF y-opening subtype (pos1=y, N=9) has pen=ot in 3/9 lines (E=7.3× within subtype). The exp_506 aggregate ot-LF ot-self@pen (E=3.51×/N=8, dir) appears to be driven by this subtype. Hypothesis: within ot-LF lines where pos1=y, pen=ot is CONF-level enrichment. This is a conditional finding (requires pos1=y) that has not been explicitly tested at CONF methodology.
**Description:** For A herbal_a ot-LF lines with pos1=y (N=9): compute exact E for pen=ot using the section-wide pen baseline (not the ot-LF-specific baseline). Is E≥2.5×/N≥3 — meeting the (dir) threshold? Compare: ot-LF overall pen=ot vs ot-LF-with-pos1=y pen=ot. This tests whether the y-opening subtype is a genuine grammatical formula y[pos1]→...→ot[pen]→ot[LF].
**Expected outcome:** 3/9 = 33% pen=ot in y-opening subtype vs ~6% baseline = E≈5.5×/N=3. That's (dir) threshold but N=3. Could be confirmed if A herbal_b (other A-dialect herbal folios) adds more examples. Or just document as directional conditional finding.
**Cost estimate:** trivial (exact E calculation using correct pen baseline)
**Prerequisites:** none

## H_new_DR: k-LF pos2=ch near-CONF (E=1.42×/N=16) — targeted confirmation test

**Priority:** high
**Status:** resolved — inline (2026-04-11). NEGATIVE: k-LF pos2=ch E=1.42×/N=16 BELOW CONF (E<1.5×). Cannot confirm. NEW: k-LF pos2=cth E=2.34×/N=4 (below both dir and (dir) thresholds). H_new_DR CLOSED.
**Source:** inline H_new_DP (2026-04-11) — k-LF pos2=ch: E=1.42×/N=16 in A herbal_a. This is just below CONF (E≥1.5×) but N=16 provides good power. The direction is OPPOSITE to ot-LF (ch depleted for ot, elevated for k). If E hits 1.5× in a targeted test with the full A herbal_a k-LF N, this is a new CONF finding.
**Description:** For A herbal_a k-LF lines (len≥3, N=33): compute exact pos2=ch E with the len≥3 A herbal_a section baseline. Check: is k-LF self-chain at pos2 present (k→k@pos2)? What are k-LF's top pos2 classes? Also check whether this is the same N=16 or higher with full section coverage.
**Expected outcome:** E=1.42× from N_elig=33 with obs=16/exp=11.3. If all A herbal_a k-LF lines are already included (N=33), E cannot be improved without more corpus data. But exact CONF threshold is 1.5× — very close. The targeted test with correct methodology will give definitive E.
**Cost estimate:** trivial
**Prerequisites:** none

## H_new_DQ: ot-LF two-subtype structure: y-opening vs k-routing — full positional profile of each subtype

**Priority:** high
**Status:** resolved — inline (2026-04-11). KEY FINDING: y-opening subtype (pos1=y, N=9) has strong ot-self@pen enrichment: 3/9 lines have pen=ot, E=7.3× — the ot-LF ot-self@pen signal from exp_506 (E=3.51×/N=8 overall) is CONCENTRATED in the y-opening subtype. Template: y[pos1]→?→ot[pen]→ot[LF]. k-routing subtype (pos2=k, N=5): cth@pen elevated (2/5, E=6.5×) but N=2. pos1 for k-routing is diverse (no clear class). "Neither" subtype (N=27): pos1 = d/o/ok dominated, pen=cth elevated (E=3.6×/N=6).
**Source:** inline H_new_DN (2026-04-11) — ot-LF splits into two independent line subtypes: y-opening (pos1=y, N=9) and k-routing (pos2=k, N=5). These don't overlap (E_cooccur=0.89×). The y-opening subtype also has elevated pos2=y (2/9 = 22% vs 3% baseline). The k-routing subtype has k specifically at pos2 (not at pos1 — or does it?). What are the FULL positional profiles of these two subtypes?
**Description:** For A herbal_a ot-LF (N_elig=40): split into (A) y-opening lines (pos1=y, N=9) and (B) k-routing lines (pos2=k, N=5) and (C) neither. For each subtype, compute: pos1 dist, pos2 dist, pen dist, LF word distribution, line length. This would characterize whether there are two ot-LF paragraph "formulas."
**Expected outcome:** y-opening subtype may show y→y (pos1→pos2) elevated, with specific pen class. k-routing subtype may show consistent pos1 class that pairs with k at pos2. If subtypes have distinct full positional profiles, ot-LF has two grammar templates (not just two independent rules).
**Cost estimate:** small (requires splitting ot-LF lines by pos1 and pos2 condition)
**Prerequisites:** none

## H_new_DP: t-LF and k-LF pos2 profile in A herbal_a — do gallows-class LF share ot's ch-depletion pattern?

**Priority:** medium
**Status:** resolved — inline (2026-04-11). NEGATIVE: ch-depletion at pos2 is ot-LF-SPECIFIC. t-LF pos2=ch: E=0.90×/N=8 (FLAT); t-LF pos2=y: E=0.00×/N=0 (DEPLETED). k-LF pos2=ch: E=1.42×/N=16 (near-threshold ELEVATED — opposite direction from ot!). The ch-depletion pattern is ot-unique. F498 note updated.
**Source:** F498 (exp_519) — ot-LF pos2 shows ch DEPLETED (E=0.80×) and k ELEVATED (E=2.07×). This may be a shared feature of gallows-class LF onsets (ot, t, k are all gallows-related in EVA). If t-LF and k-LF also avoid ch at pos2, this is a grammatical constraint on gallows-onset LF classes.
**Description:** For A herbal_a t-LF and k-LF lines (len≥3): compute full pos2 distribution. Compare ch rate at pos2 (baseline ~34%) — is it depleted? Compare y and k rates at pos2. Include also A stars (t-LF dominant section) as secondary test.
**Expected outcome:** If gallows LF classes share ch-depletion, expect t-LF pos2=ch E<0.9× and k-LF pos2=ch E<0.9×. Or they may have different pos2 profiles if the constraint is ot-specific.
**Cost estimate:** small
**Prerequisites:** none

## H_new_DO: y-opening ot-LF subtype: within-subtype pos2=y confirmation (2/9 lines)

**Priority:** medium
**Status:** resolved — inline (2026-04-11). EXPLORATORY: 2/9 y-opening lines have pos2=y: (1) y,y,s,ot and (2) y,y,ot,ot. Line 2 has ot at pen too — y[1]→y[2]→ot[pen]→ot[LF] is a specific sequence. Not confirmable (N=2). The ot-self@pen in y-opening subtype is driven by 3 lines including this one.
**Source:** inline H_new_DN (2026-04-11) — within the y-opening subtype (ot-LF, pos1=y, N=9), 2 of 9 lines have pos2=y (22% vs 3% baseline = E≈7.3×). This is the "y→y→...→ot" formula. N=2 is too small, but if the y-opening subtype is a real grammatical category, additional ot-LF lines in A herbal_a that have pos1=y should be examined with deeper analysis (line length conditioning, pen class, etc).
**Description:** The 2/9 pos2=y within pos1=y lines: record their full structure (pos1, pos2, pen, LF). Check if they have y at pen too (y→y→...→y→ot template). This is essentially asking: within the y-opening subtype, do some lines have persistent y across multiple positions?
**Expected outcome:** If 2 lines have y at pos1, pos2, and also at pen, the "y-persistent" ot-LF template is richer. But N=2 is very small. Mostly exploratory.
**Cost estimate:** trivial
**Prerequisites:** none

## H_new_DN: ot-LF pos1=y and pos2=k co-occurrence — two y-subpopulations or k-independent of y?

**Priority:** medium
**Status:** resolved — inline (2026-04-11). INDEPENDENT: BOTH pos1=y AND pos2=k: obs=1, exp=1.12, E=0.89×. y-at-pos1 and k-at-pos2 come from DIFFERENT ot-LF lines. Two distinct ot-LF line subtypes: (1) y-opening: pos1=y (N=9), pos2 diverse (ch,y,k,d,qok,ckh,cth); (2) k-routing: pos2=k (N=5), not starting with y (only 1 overlap). ot-LF grammar bifurcates into two paragraph modes.
**Source:** exp_519 (2026-04-11) — ot-LF has both pos1=y (F456, CONF, E=1.83×/N=11) and pos2=k (E=2.07×/N=5, F498, dir). Are these the same lines (ot-LF lines that have y@pos1 and k@pos2) or different lines? If y-at-pos1 and k-at-pos2 come from different ot-LF lines, there may be two distinct ot-LF paragraph types: y-opening type vs k-routing type.
**Description:** For A herbal_a ot-LF (N_elig=40, len≥3): count lines with pos1=y, pos2=k, BOTH pos1=y AND pos2=k, and NEITHER. E_cooccur = obs_both / (P(pos1=y) × P(pos2=k) × N_elig). Also check: do lines with pos2=k tend to have pos1≠y? And do lines with pos1=y tend to have pos2=y (from H_new_DA) or pos2=k?
**Expected outcome:** If y-at-pos1 and k-at-pos2 are mutually exclusive (anti-correlated), there are two ot-LF line subtypes. If independent or co-occurring, the ot-LF grammar is more complex. With N_elig=40, this is directly testable.
**Cost estimate:** trivial
**Prerequisites:** none

## H_new_DM: Gallows-class LF (t-LF, k-LF) pos2 profile — do they also avoid ch at pos2?

**Priority:** medium
**Status:** resolved — inline H_new_DP (2026-04-11). NEGATIVE: ch-depletion at pos2 is ot-LF-SPECIFIC. t-LF pos2=ch E=0.90×/N=8 (FLAT, not depleted); t-LF pos2=y E=0.00× (DEPLETED — t-LF avoids y at pos2). k-LF pos2=ch E=1.42×/N=16 (near-threshold ELEVATED — OPPOSITE direction to ot). The "avoid ch at pos2" rule is ot-LF-specific, NOT shared by gallows class. t-LF has its own distinctive constraint (y-depletion at pos2). k-LF mildly prefers ch at pos2. Each gallows subclass (ot,t,k) has a distinct pos2 profile. A stars t-LF secondary check: not done but H_new_DP resolves the core A herbal_a question.
**Source:** exp_519 — ot-LF pos2 shows ch DEPLETED (E=0.80×) and k ELEVATED (E=2.07×). ot is a gallows-related class (EVA 't' family). Do t-LF lines and k-LF lines also show ch depletion at pos2? A-dialect A stars has t-LF dominance (F446). This could test whether gallows LF classes share a "avoid ch at pos2" pattern.
**Description:** For A herbal_a t-LF and k-LF lines (len≥3): compute pos2 distribution. Focus on ch depletion and k/y elevation. Compare with ot-LF pos2 profile. A stars section (t-LF dominant) as secondary check if N_elig sufficient.
**Expected outcome:** If gallows LF classes share a ch-depletion rule at pos2, this suggests a class-level grammatical constraint (gallows onset → avoid ch at the second word). Could be related to word co-occurrence constraints in the original language.
**Cost estimate:** small (new section survey)
**Prerequisites:** none

## H_new_DL: A cosmo ch CL sender role — folio distribution of ch→ok and ch→ol

**Priority:** low
**Status:** resolved — inline (2026-04-11). DISTRIBUTED: ch→ok from 5/10 folios (N=9, f89:2,f90:2,f96:1,f101:1,f102:3); ch→ol from 4/10 folios (N=5, f88:1,f89:2,f99:1,f102:1). Both well-distributed — NOT clustering artifacts. F492 and F497 ch signals are genuine A cosmo CL grammar, not folio-specific.
**Source:** exp_518 + exp_519 — A cosmo has two CL signals where ch is the sender: ch→ok (F492, E=1.71×/N=9, directional) and ch→ol (F497, E=2.06×/N=5, dir). In A herbal_a, ch is a CL RECEIVER (qot→ch CONF). The A cosmo ch-as-sender pattern is interesting but may also be partially folio-driven. Are ch→ok and ch→ol pairs distributed across A cosmo folios, or concentrated in specific folios like the cth signals?
**Description:** Record folio distribution of ch→ok and ch→ol pairs in A cosmo. If both are distributed across ≥5 folios, the ch-as-sender role is likely a genuine A cosmo grammar feature. If concentrated in 1-3 folios, flag as potential artifact.
**Expected outcome:** ch is a much more common LF class than cth (ch=21% vs cth=~3% in A cosmo), so ch→X pairs are more likely to be distributed. ch→ok with N=9 is more likely distributed.
**Cost estimate:** trivial (instrument exp_518/519 script to record folio distribution of ch→ok and ch→ol)
**Prerequisites:** none

## H_new_DH: Folio distribution of A cosmo cth→cth CL — clustering artifact or distributed?

**Priority:** high
**Status:** resolved — exp_519 (2026-04-11). NEGATIVE: CLUSTERING ARTIFACT. All 4 cth→cth pairs from 2 of 10 folios (f87:2, f93:2). f93 also drives cth→ol (2 of 3 pairs). F497 cth→cth and cth→ol DEMOTED. Word pairs are all distinct (class-level, not lexical), but folio distribution fails the distributed-grammar criterion. f93 is simply cth-heavy in A cosmo content.
**Source:** exp_518 — A cosmo cth→cth CL shows E=7.25×/N=4. With only 10 folios and 286 pairs, N=4 could come from 1-2 folios (spatial clustering artifact). If all 4 pairs come from the same folio, the signal is a folio-specific artifact, not a grammar rule.
**Description:** For the 4 observed cth→cth consecutive pairs in A cosmo, record which folio each pair comes from. If ≥3 folios contribute, the signal is distributed (grammar-like). If 1-2 folios contribute all 4, it may be a clustering artifact. Also record the specific words involved — if it's always the same two cth-words (lexical bigram), it's a word-level collocation, not a class-level rule.
**Expected outcome:** If cth→cth is a grammar rule (class-level), expect distribution across ≥3 folios and diverse word pairs. If artifact, expect 1-2 folios contributing all 4 pairs. Results would determine whether F497 cth→cth warrants continued investigation.
**Cost estimate:** trivial (instrument exp_518 script to record folio and word-level details for cth→cth pairs)
**Prerequisites:** none

## H_new_CF: RESOLVED — exp_500 (2026-04-11). ANSWERED: A cosmo HAS confirmed pos1 rule: d-LF→y@pos1(F479,CONF,E=1.64×/N=16). Inverts A herbal_a d-LF→ot@pos1(F453). F476 scope: herbal-section-only (A cosmo ot-LF y DEPLETED). ch/y self-chain rules confirmed A-herbal_a-specific.

## H_new_CH: RESOLVED — exp_502 (2026-04-11). ANSWERED: B pharma has 2 confirmed pos1 rules: F449 (ch-self CONF, reproduced) + F480 NEW (a-LF→y@pos1,CONF,E=1.50×/N=23). Plus directionals: sh-self(dir), t-self(dir), d→l(dir), ot→t(dir).

## H_new_CI: RESOLVED — exp_503 (2026-04-11). ANSWERED: F480 is B pharma-SPECIFIC. B herbal a-LF y DEPLETED (E=0.26×); B astro below baseline; B combined E=1.43× (below CONF). B-section a-LF pos1 routing is section-specific (pharma→y, astro→d, herbal→p/ot).

## H_new_CG: RESOLVED — exp_501 (2026-04-11). ANSWERED: A stars has NO confirmed pos1 rules. d-LF d-self near threshold (E=1.67×/N=8). F476 NOT in A stars (ot-LF y@pos1 E=1.50×/N=3). A stars positional grammar (both pos1+pos2): flat/no confirmed rules.

## H_new_CE: RESOLVED — exp_504 (2026-04-11). ANSWERED: B astro pen is DRAMATICALLY stronger than pos2. THREE confirmed rules: F481(qok→sh,E=2.12×/N=20), F482(d-self,E=1.96×/N=12), F483(l→ch,E=1.89×/N=22). B astro pen/pos2 asymmetry: 3 CONF vs 0 CONF.

## H_new_CJ: RESOLVED — exp_505 (2026-04-11). ANSWERED: F481 broader(B pharma dir); F482 B astro-SPECIFIC(d-self@pen); F483 B astro-SPECIFIC(l→ch); F484 NEW CONF(B pharma l-self@pen). Pen self-chain is section-specific across B dialect.

## H_new_CS: RESOLVED — exp_511 (2026-04-11). ANSWERED: A herbal_a has 2 confirmed CL rules: F490 (qot→ch, E=2.00×/N=12, CONF) and F491 (d→qot, E=1.64×/N=13, CONF). Together suggest d→qot→ch CL chain. ok→y dir (E=2.23×/N=8), ol↔ok bidirectional dir. ch→ch CL FLAT (E=1.03×) — F438/F445 "A ch→ch" was mixed-section artifact. A herbal_a CL: qot is a "pivot" class (receives d, passes to ch). A/B CL inversion: A qot→ch vs B ch→qot (F444).

## H_new_DG: RESOLVED — exp_517 (2026-04-11). ANSWERED: F444's B pharma qok→s CL is a mixed-section baseline artifact — ZERO observations with section-specific baseline (E=0.00×). F496 NEW CONF: B pharma ol→qok CL (E=2.76×/N=10). This completes the F444 correction: ALL three F444 individual B-section CL claims (B herbal, B astro, B pharma) fail section-specific testing. Genuine B section CL rules: F495 (B astro qok→qok), F496 (B pharma ol→qok). Both use qok as a target.

## H_new_DE: RESOLVED — exp_516 (2026-04-11). ANSWERED: F444's B astro ch→qot CL is a mixed-section baseline artifact (section-specific baseline: E=1.14×/N=3, FLAT). B astro's ONLY confirmed CL rule is F495 (qok→qok, E=1.77×/N=14, NEW CONF). Directionals: d→qo(E=3.13×/N=8), ol→o(E=2.28×/N=7), qot→ch(E=1.90×/N=5, same direction as A herbal_a F490). A/B CL "inversion" for ch/qot was an artifact.

## H_new_DD: RESOLVED — exp_515 (2026-04-11). ANSWERED: B herbal has NO confirmed CL rules (258 within-folio pairs, N too small). Best dir: ot→ch (E=2.77×/N=5). d→ok near-CONF (E=1.79×/N=9). F444's B herbal CL claims (ok→y, d→sh) do NOT survive section-specific baseline — both drop below threshold. F490/F491 (d→qot, qot→ch) absent in B herbal (qot near-zero). A/B herbal CL inversion: A pivot=qot (d→qot→ch chain); B herbal leading tendency = d→ok (no qot).

## H_new_CZ: RESOLVED — exp_513+514 (2026-04-11). ANSWERED: Cross-class pos2 grammar is section-specific with no simple A/B dialect pattern. Confirmed cross-class pos2 rules: A herbal_a=F493(qot→sh,E=2.63×/N=10); B herbal=F457(d→sh,E=1.67×/N=10); B pharma=F451(l→ok)+F494(ch→o,NEW); B astro=NONE. There is NO consistent "B routes cross-class, A self-chains" pattern — A herbal_a has one cross-class CONF rule and B astro has zero. The pos2 grammar is content-section-specific: each section uses different LF-class routing targets. The d→sh pattern (F457) appears in B herbal but NOT in A herbal_a or other sections. No evidence of a universal cross-dialect pos2 routing scheme.

## H_new_DF: RESOLVED — exp_514 (2026-04-11). ANSWERED: B sections DO have confirmed cross-class pos2 rules: F457 (B herbal d→sh, E=1.67×/N=10, CONF, reproduced), F451 (B pharma l→ok, E=1.68×/N=14, CONF, reproduced), F494 NEW CONF (B pharma ch→o, E=1.54×/N=11). B astro has NO confirmed cross-class pos2 rules (ch→ok dir E=2.66×/N=9, qot→ch dir, ol→d dir — all below CONF). B pharma is richest B-section pos2 grammar (2 CONF cross-class rules). High-E directionals: B pharma d→qot (E=4.75×/N=5), B herbal ok→o (E=3.07×/N=6). A/B pos2 pattern: B astro weakest; B pharma strongest; A herbal_a's only CONF is F493 (qot→sh).

## H_new_DA: RESOLVED — inline (2026-04-11). ANSWERED: ot-LF pos1=y AND pos2=y co-occur at E=2.22×/N=3 — above baseline but below (dir) threshold (N=3, E<2.5×). Weakly elevated. The ot-LF y-at-both-early-positions tendency is real but small N prevents confirmation.

## H_new_DB: RESOLVED — inline (2026-04-11). ANSWERED: cth-LF pos2=qot AND pen=d co-occurrence: E=0.76×/N=1 — INDEPENDENT/slightly anti-correlated. Consistent with exp_493 (cth pos2+pen independent). The two rules operate on different cth-LF lines.

## H_new_DC: RESOLVED — inline (2026-04-11). ANSWERED: F493 (qot→sh@pos2) is A-herbal_a-SPECIFIC. A cosmo: N=6 too small. B herbal: N=1. B astro: E=0.73×/N=3 (DEPLETED — B astro qot-LF avoids sh@pos2). qot-LF → sh@pos2 is a herbal-A-specific rule.

## H_new_DA: A herbal_a ot-LF: do pos1=y AND pos2=y co-occur in the same lines?

**Priority:** medium
**Status:** resolved — exp_518 (2026-04-11). ot-LF N_elig=40 (corrected A-dialect filter). BOTH pos1=y AND pos2=y: obs=2, exp=0.90, E_cooccur=2.22×. Directional but N=2 too small. Individual: pos2=y E=3.60× (strong). Co-occurrence unconfirmed due to N.
**Source:** A herbal_a ot-LF has confirmed pos1=y (F456, CONF, E=1.83×/N=11) and directional pos2=y (E=3.25×/N=5, exp_513). If both positions tend to have y in the same line, the ot-LF formula is: y[pos1]→y[pos2]→...→ot[LF] — a two-position y template.
**Description:** For A herbal_a ot-LF (N_elig=48, len≥3): count lines where pos1=y AND pos2=y. E_cooccur = obs / (P_pos1 × P_pos2 × N_elig). If E≥1.5×, the two-position y template is elevated.
**Expected outcome:** y at pos1 E=1.83×/N=11; y at pos2 E=3.25×/N=5. If independent, expected co-occurrence = 11/48 × 5/48 × 48 = 1.15 lines. Likely just 0-2 observed.
**Cost estimate:** tiny
**Prerequisites:** none

## H_new_DB: A herbal_a cth-LF pos2/pen co-occurrence — qot@pos2 and d@pen in same lines?

**Priority:** medium
**Status:** resolved — exp_518 (2026-04-11). cth-LF N_elig=64 (corrected A-dialect filter). BOTH pos2=qot AND pen=d: obs=1, exp=1.41, E_cooccur=0.71×. NEGATIVE — INDEPENDENT, consistent with exp_493 (E=0.76×). Rules operate on different cth-LF lines.
**Source:** A herbal_a cth-LF has confirmed pen→d (F474, CONF, E=1.61×/N=18) and directional pos2→qot (E=2.81×/N=5, exp_513). Do these two rules operate on the same lines (forming a template) or independently? Precedent: exp_493 found cth-LF pos2+pen INDEPENDENT; exp_510 found A cosmo d-LF pos1+pen weakly correlated.
**Description:** Count cth-LF lines (N_elig=68) where pos2=qot AND pen=d. E_cooccur = obs / (p_pos2 × p_pen × N_elig). 
**Expected outcome:** Based on INDEPENDENT precedent (exp_493), likely near-baseline. With N_elig=68, even small co-occurrence numbers provide informative E values.
**Cost estimate:** tiny
**Prerequisites:** none

## H_new_DC: F493 scope — qot-LF → sh@pos2 in A cosmo and B sections

**Priority:** medium
**Status:** resolved — inline exp_513 context (2026-04-11). See RESOLVED entry at top. F493 is A-herbal_a-SPECIFIC.
**Source:** F493 (A herbal_a qot-LF → sh@pos2, CONF, E=2.63×/N=10) is the only confirmed pos2 rule in A herbal_a. Is this herbal-section-specific or broader? A cosmo has qot-LF (N=8, small); B sections have qot-LF too.
**Description:** Check qot-LF → sh@pos2 E in A cosmo (N_qot=8, small), B herbal (N=~10), B astro (N=~20). If any section shows E≥1.5×/N≥5, the rule may be broader.
**Expected outcome:** qot-LF is rare outside A herbal_a. Likely insufficient N for confirmation in other sections. But directional signals may confirm herbal-specificity or broader scope.
**Cost estimate:** tiny
**Prerequisites:** none

## H_new_CX: RESOLVED — exp_513 (2026-04-11). ANSWERED: A herbal_a pos2 grammar is cross-class routing, not self-chaining. F493 NEW CONF: qot-LF→sh@pos2(E=2.63×/N=10). Only confirmed pos2 rule in A herbal_a after corrections. qot-LF is the pos2 routing "hub": sh CONF, d dir, ch DEPLETED. Directionals: ok→o, cth→qot, ot→y, s→sh. Most LF classes below confirmation at pos2.

## H_new_CX: Does A herbal_a pos2 grammar shift from self-chain to cross-class routing?

**Priority:** medium
**Status:** resolved — exp_513 (2026-04-11). ANSWERED: see summary above.
**Source:** With F468 retracted, A herbal_a pos2 self-chain is below CONF for all classes (E=1.1-2.3×). But the pos2 tendency is still present. Are there confirmed CROSS-CLASS pos2 rules in A herbal_a (analogous to B herbal's F457 d→sh)? The exp_511 (pos2 survey) found no cross-class confirmed rules either — but only checked d-LF pos2.
**Description:** For A herbal_a: compute E for ALL onset classes at pos2, for ALL LF classes with N_elig≥20. Use correct len≥3 methodology. Focus on cross-class pairs (LF onset ≠ pos2 onset).
**Expected outcome:** May find confirmed cross-class routing (d-LF → ch@pos2? cth-LF → ok@pos2?). Or A herbal_a pos2 may be genuinely weaker than pos1/pen.
**Cost estimate:** small (single section survey)
**Prerequisites:** none

## H_new_CW: RESOLVED — inline (2026-04-11). ANSWERED: F469(B astro sh→sh@pos2) corrected to E=1.33×/N=8 (below CONF). F471(B astro ol→ol@pos2) corrected to E=1.29×/N=12 (below CONF). Both 2-word-line artifacts. No pos2 self-chain finding confirmed anywhere. Cross-class pos2 rules (F457, F477, F478) unaffected.

## H_new_CW: F469/F471 verification — are B astro sh→sh@pos2 (F469) and ol→ol@pos2 (F471) also 2-word-line artifacts?

**Priority:** high
**Status:** resolved — exp_522 (2026-04-11). RETRACTED: F469 and F471 both BELOW CONF under current methodology (E=1.33×/obs=8 and E=1.29×/obs=12 respectively). The 2-word-line correction has minimal effect (N_elig drops only 2-3); the main discrepancy with exp_490's higher N/E is different corpus parsing or baseline methodology. Both findings are below CONF regardless of the len≥2 vs len≥3 filter. F469 and F471 should be treated as RETRACTED.

## H_new_CV: RESOLVED — exp_512 (2026-04-11). ANSWERED: d→qot→ch triple: E=2.87×/N=4 (dir) — coherent with F490+F491 pairwise rules but N=4 below dir threshold. The chain is specific (d→*→ch flat at E=1.03×; qot specifically mediates). INCIDENTAL: F492 NEW CONF: A cosmo ch→ok CL(E=2.01×/N=12). CRITICAL: F461-F467 pos2 self-chain ALL corrected below CONF (2-word-line artifact). F468 RETRACTED.

## H_new_CU: RESOLVED — exp_512 (2026-04-11). ANSWERED: ok-LF pos2+pen co-occurrence: E=3.38×/N=3 (dir) — positively correlated but below CONF. INCIDENTAL: F467 reproduction showed E=1.66× vs claimed 4.53× — triggered systemic pos2 audit.

## H_new_CT: RESOLVED — exp_512 (2026-04-11). ANSWERED: F490/F491 in A cosmo: directionally consistent (d→qot E=1.86×/N=2; qot→ch E=2.20×/N=3) but N too small to confirm. B herbal: N too small (qot very rare). CL rules cannot be declared A-herbal_a-specific yet. A cosmo has own confirmed CL rule: F492 ch→ok (CONF). CL rules are section-specific.

## H_new_CV: RESOLVED — exp_517 (2026-04-11). ANSWERED: d→qot→ch triple is directional (E=2.62×/N=4, above (dir) threshold E≥2.5×/N≥3). d→*→ch (any mediator) is FLAT (E=1.03×) — qot SPECIFICALLY mediates. qot→ch→d also dir(E=2.62×/N=4) suggesting cyclic chain. Triple does not confirm (N=4 < 10) but directional confirmation of the chain structure.

## H_new_CU: RESOLVED — exp_517 (2026-04-11). ANSWERED: ok@pos2 and ok@pen CO-OCCUR at E=3.94×/N=3 (dir) — positively correlated. The ok triple ok[pos2]→...→ok[pen]→ok[LF] is directional. Contrast: cth-LF pos2+pen INDEPENDENT(E=0.76×, exp_493). ok-LF is opposite of cth-LF: co-occurring positional rules vs independent rules.

## H_new_CT: RESOLVED — exp_515 (2026-04-11). ANSWERED: F490/F491 cannot be tested in A cosmo or B herbal because qot-LF is near-absent in both sections. A cosmo: d→qot obs=1/exp=0.63; qot→ch obs=1/exp=0.81. B herbal: d→qot obs=0/exp=0.13; qot→ch obs=1/exp=0.16. N=1 is far below any threshold. F490/F491 are A-herbal_a-specific by default — qot-LF as a paragraph-pivot class is unique to A herbal_a.

## H_new_CR: RESOLVED — exp_510 (2026-04-11). ANSWERED: A cosmo d-LF y@pos1 AND ok@pen co-occur at E=1.52×/N=5 — above baseline but BELOW both CONF(N≥10) and dir(E≥2.0×/N≥5) thresholds. Three-position grammar y[pos1]→ok[pen]→d[LF] is a suggestive but unconfirmed template. Rules appear approximately independent with slight positive correlation. INCIDENTAL: F465 (A herbal_a d-LF → d-self@pos2 CONF) is a 2-word-line artifact — corrected E=1.12×/N=28 (FLAT). F465 RETRACTED.

## H_new_CQ: RESOLVED — exp_509 (2026-04-11). ANSWERED: B herbal has NO confirmed pen rules. ok→a@pen dir(E=2.66×/N=6); a-LF→ok@pen dir(E=2.85×/N=5); ot-self(dir,E=5.59×/N=3). N too small for ok→a@pen confirmation (N=6<10). B herbal stays at 0 confirmed pen rules.

## H_new_CQ: B herbal pen grammar complete survey — original content below

**Priority:** medium
**Status:** resolved
**Source:** B herbal pen is partially known: ok→a@pen (dir, E=2.73×/N=6 from F474 context); ot-self@pen (dir, E=5.43×/N=3); d-LF pen ch (E=1.47×/N=12 from exp_482, below threshold). No confirmed pen rules yet. B herbal N=272 lines; ok-LF N=40. Does a focused pen survey surface any confirmed rules? Compare with B astro (3 CONF) and B pharma (2-3 CONF).
**Description:** For B herbal: full pen survey for all LF classes with N_lf≥8.
**Expected outcome:** ok→a@pen may reach CONF with N_elig~37 (E=2.73×/N=6, need N~10 more). ot-self@pen only N=3 — won't confirm.
**Cost estimate:** small
**Prerequisites:** none

## H_new_CP: RESOLVED — exp_509 (2026-04-11). ANSWERED: A stars has ONE confirmed pen rule: F489 NEW CONF: ch-LF→ch-self@pen(E=1.89×/N=12). ch-self DEPLETED at pos2(E=0.73×) in A stars — pen/pos2 asymmetry holds. A stars: pos1=0 CONF, pos2=0 CONF, pen=1 CONF. Extends pen/pos2 asymmetry to A stars.

## H_new_CP: A stars pen grammar survey — original content below

**Priority:** medium
**Status:** resolved
**Source:** A stars (186 lines) has NO confirmed pos1 or pos2 rules (exp_498/501). Pen is completely untested. Completing the A-dialect pen survey: A herbal_a (2 CONF), A cosmo (3 CONF), A stars (unknown). A stars may show a different pattern given its different content (astronomical charts vs herbal/cosmological).
**Description:** For A stars: full pen survey for all LF classes with N_lf≥8.
**Expected outcome:** A stars may have 0-2 confirmed pen rules given small N (186 lines). The flat pos1/pos2 grammar suggests possibly weaker pen grammar too.
**Cost estimate:** small
**Prerequisites:** none

## H_new_CO: RESOLVED — exp_508 (2026-04-11). ANSWERED: A cosmo has THREE confirmed pen rules: F486(ch-LF→o@pen,CONF,E=2.05×/N=10), F487(d-LF→ok@pen,CONF,E=1.71×/N=11), F488(o-LF→ch@pen,CONF,E=2.12×/N=11). A cosmo pen rich (3 CONF) vs pos2 flat (0 CONF) — parallels B astro pen/pos2 asymmetry. d-LF bi-positional grammar: y@pos1(F479)+ok@pen(F487).

## H_new_CO: A cosmo pen grammar survey — original content below

**Priority:** high
**Status:** resolved
**Source:** A cosmo (455 lines) has confirmed pos1 rule (F479: d-LF→y@pos1, CONF). A cosmo pen is completely untested. The A-dialect pen picture is now: A herbal_a has 2 CONF rules (F474+F485) + near-CONF directionals. What does A cosmo's pen grammar look like? Does d-LF→y@pen follow from d-LF→y@pos1 (i.e., y routing carries through), or does d-LF use different routing at pen?
**Description:** For A cosmo: compute pen routing E for all LF classes with N_lf≥8 using A cosmo pen-specific baseline (len≥3). Compare with A herbal_a pen grammar.
**Expected outcome:** A cosmo may have different pen grammar from A herbal_a — d-LF might self-chain or route to y/ot at pen. Some confirmed rules likely given A cosmo N=455.
**Cost estimate:** small
**Prerequisites:** none

## H_new_CN: RESOLVED — exp_508 (2026-04-11). ANSWERED: ok→a@pen NOT manuscript-wide. DEPLETED in A cosmo (E=0.63×/N=1 from N_elig=34). Present herbal+pharma only: A herbal_a dir(E=3.18×/N=6), B herbal dir(E=2.66×/N=6), B pharma CONF(F459). ok-self@pen is A-herbal_a-SPECIFIC: B pharma E=0.93× below baseline, B herbal below threshold.

## H_new_CN: ok→a@pen cross-dialect scope — original content below

**Priority:** medium
**Status:** resolved
**Source:** F459 CONF: B-dialect ok-LF→a@pen (E=2.79×/N=19, B-dialect-wide). A herbal_a shows ok→a@pen dir (E=3.18×/N=6, exp_506). F485 also CONF for ok-self@pen in A herbal_a. The combined manuscript ok-LF pen signal: are both ok-self AND ok→a present across all sections, or is one A-specific and one B-specific?
**Description:** Combine A herbal_a + all B sections (herbal, pharma, astro) ok-LF lines. Test ok→a@pen and ok-self@pen in combined and section-by-section view. Use section-specific baselines for E, then aggregate.
**Expected outcome:** ok→a@pen may be manuscript-wide (A dir + B CONF = combined CONF). ok-self@pen may be A-herbal_a-specific (B-dialect ok-LF doesn't use self-chain).
**Cost estimate:** small (focused test, targeted analysis)
**Prerequisites:** none

## H_new_CM: RESOLVED — exp_507 (2026-04-11). ANSWERED: ot→cth@pen and ot-self@pen REMAIN DIRECTIONAL. A herbal_a has only N=51 ot-LF total — entire section used. Adding "A_herbal_b" reveals it's B-dialect-dominated (700 lines = B_astro range; cth pen rate 0.2% vs A's 5.2%). Both rules stay dir (E~3.5×/N<10). ot→cth@pen likely A-herbal_a-SPECIFIC (cth rare at pen outside A herbal_a). Cannot confirm with available A data.

## H_new_CM: A herbal_a ot-LF pen scope — original content below

**Priority:** high
**Status:** resolved
**Source:** exp_506: ot-LF → cth@pen (E=3.58×/N=9, dir, one below CONF) and ot-self@pen (E=3.51×/N=8, dir, two below CONF). Both have very high E values, just short of N=10 threshold. A focused test pulling ALL A herbal_a ot-LF lines (N=51 total, N_elig=48) may confirm these with a slightly larger/different folio sub-split, or combining with ot-LF from A herbal_b if those are counted.
**Description:** (1) Run dedicated A herbal_a ot-LF pen analysis with all 51 ot-LF lines. Show full pen distribution. (2) Check whether A herbal_b (n=57-84, A-dialect) ot-LF lines show cth@pen and ot-self@pen — if combined A herbal (a+b) confirms these, add new findings. (3) If still N<10, accept directional status.
**Expected outcome:** If the full A herbal corpus (including A herbal_b) is included, ot-LF N may increase sufficiently to confirm. Combined confirmation would establish ot→cth@pen and ot-self@pen as A herbal findings.
**Cost estimate:** small (A herbal_a ot-LF focused; A herbal_b additional)
**Prerequisites:** none

## H_new_CL: B cosmo pen grammar survey — Does B cosmo have confirmed pen routing rules?

**Priority:** medium
**Status:** RESOLVED — exp_506 (2026-04-11). ANSWERED: B cosmo has NO confirmed pen rules. Small N (N_lines=159) precludes confirmation. Directionals: ch-self (E=2.35×/N=6), ot-self (E=2.35×/N=5) consistent with B-dialect patterns but not confirmable from B cosmo alone.
**Source:** B astro pen is dramatically rich (3 CONF rules, exp_504). B cosmo pen is completely untested. B cosmo is small (N_lines≈119) so power is limited, but completing the B-dialect pen survey is worthwhile. B cosmo is adjacent in the manuscript to B astro (cosmo folios ≤102 vs astro ≤84).
**Description:** For B cosmo: compute pen routing E for all LF classes with N_lf≥8 using B cosmo pen-specific baseline (len≥3). Key classes: ch, ok, d, ot, qok, sh. Show full pen distribution for each (top 5 by E). Compare with B astro pen grammar (3 CONF rules) and B pharma pen grammar.
**Expected outcome:** B cosmo may have 0-1 confirmed pen rules (small N), but may show directional signals consistent with B astro grammar or its own pattern.
**Cost estimate:** small (B cosmo pen-specific baseline, all LF classes)
**Prerequisites:** none

## H_new_CK: RESOLVED — exp_506 (2026-04-11). ANSWERED: A herbal_a has TWO confirmed pen rules: F485 NEW (ok-self@pen, E=2.73×/N=12) + F474 reproduced (cth→d@pen, E=1.70×/N=18). Near-CONF directionals: ot→cth@pen (E=3.58×/N=9) and ot-self@pen (E=3.51×/N=8). Flat: d-LF (N=261), ch-LF (N=186). ok→a@pen dir (parallels B-dialect F459).

## H_new_CK: A herbal_a pen grammar complete survey — original content below

**Priority:** high
**Status:** resolved
**Source:** A herbal_a has only ONE confirmed pen rule (F474: cth-LF→d@pen, E=1.61×/N=18). Several directionals were noted: ok-self@pen (E=3.39×/N=7), ot-self@pen (E=3.27×/N=6), ot-LF→cth@pen (dir,E=3.70×/N=9). These near-threshold directionals may become confirmed with a focused full-class pen survey. Compare: B astro has 3 confirmed pen rules, B pharma has 2 confirmed (F460+F484). A herbal_a's pen grammar is significantly undercharacterized.
**Description:** For A herbal_a: compute pen routing E for ALL major LF classes (d, ch, ok, ot, sh, y, o, cth, qok) using A herbal_a pen-specific baseline (len≥3). Show full pen distribution per class. Key questions: (1) Does ok-self@pen reach CONF (E=3.39×/N=7, N<10 → need to recount from clean data)? (2) Does ot-LF→cth@pen reach CONF (E=3.70×/N=9)? (3) Do any other LF classes have pen routing? (4) Is the d-LF pen completely flat (sh@pen E=0.85× RETRACTED)?
**Expected outcome:** Several additional confirmed pen rules likely given the high directional E values (ok-self, ot-LF→cth). A herbal_a pen grammar may parallel B astro in richness.
**Cost estimate:** small-medium (A herbal_a full pen class survey)
**Prerequisites:** none

## H_new_CD: RESOLVED — exp_516 (2026-04-11). ANSWERED: B bio (f117+) is NOT in the ZL3b corpus. The corpus contains B-dialect folios only up to f116. H_new_CD cannot be answered from available data.

## H_new_CC: RESOLVED — exp_499 (2026-04-11). ANSWERED: A+B cosmo have NO confirmed pos2 rules. F468 scope definitively A-herbal_a-SPECIFIC (5 comparator groups all negative). A cosmo d-LF→ckh@pos2(dir) vs A herbal_a d-LF→d-self: A cosmo inversion.

## H_new_CB: RESOLVED — exp_498 (2026-04-11). ANSWERED: A stars pos2 shows NO confirmed rules; ch-self BELOW baseline (E=0.73×). F468 is A-herbal_a-SPECIFIC, not A-dialect-wide.

## H_new_CA: RESOLVED — exp_498 (2026-04-11). ANSWERED: B astro has NO confirmed pos2 routing rules. Best dir: ch→ok@pos2 (F478, E=2.66×/N=9). qok-self BELOW baseline; qot-self ZERO. B astro pos2 grammar is WEAK.

## H_new_BZ: RESOLVED — exp_496 (2026-04-11). ANSWERED: ot-LF→y@pos1 is HERBAL-REGISTER-WIDE (combined herbal CONF, E=2.05×/N=17; F476 assigned). ok-LF→y@pos1 NOT herbal-wide (combined E=1.49×, A-herbal_a-specific only).

## H_new_BZ: Combined Herbal pos1 Grammar — original content below

**Priority:** high
**Status:** resolved
**Source:** A herbal_a ot-LF→y@pos1 CONF (F456, E=1.83×/N=11); B herbal ot-LF→y@pos1 dir (F475, E=2.67×/N=6). If we combine A+B herbal ot-LF lines (N≈11+11=22), can we confirm ot-LF→y@pos1 as a herbal-register rule? Also: what about ok-LF→y@pos1 (CONF in A, flat in B) — does A-only rule hold up when checked with proper A herbal_a baseline?
**Description:** (1) Pool A herbal_a + B herbal ot-LF lines (N≈22); compute y@pos1 E using combined herbal pos1 baseline. (2) Check: is F456 (A-only herbal ot-LF→y@pos1) directionally consistent with B herbal data (F475)? (3) For ok-LF→y@pos1 (F455, CONF in A): recheck B herbal ok-LF pos1 distribution — is y@pos1 flat (E=1.13×) or genuinely depleted? (4) Compute combined herbal ok-LF→y@pos1.
**Expected outcome:** Combining A+B herbal ot-LF may push ot→y@pos1 to confirmation. ok→y@pos1 may be genuinely A-herbal_a-specific.
**Cost estimate:** small (combine two already-parsed sections, targeted pos1 test)
**Prerequisites:** none

## H_new_BY: RESOLVED — exp_496 (2026-04-11). ANSWERED: B astro has NO confirmed pos1 routing rules. Best: a-LF→d@pos1(dir,E=2.38×/N=7). ch-self=E=0.89× (near baseline). B astro ot-LF has NO y@pos1 enrichment, confirming ot→y is herbal-specific.

## H_new_BY: B astro pos1 Grammar Survey — original content below

**Priority:** medium
**Status:** resolved
**Source:** B astro has qok/qot/qo-LF dominance (F447) and its own cross-line coupling (ch→qot CL, F444). Its pos1 grammar is unknown. Contrast: A stars (t-LF dominant) has o-class at pos1 for t-LF (E=2.12×/N=5, dir, exp_477). Does B astro have confirmed pos1 rules for its major LF classes (qok/ol/sh/qot)?
**Description:** For B astro: compute pos1 routing E for all LF classes with N_lf≥8 using B astro pos1-specific baseline. Key classes: qok-LF, ol-LF, sh-LF, qot-LF. Show full pos1 distribution for each. Compare with A herbal_a and B herbal pos1 grammar.
**Expected outcome:** B astro may have different pos1 grammar than herbal sections, driven by the qok-dominant LF distribution.
**Cost estimate:** small (B astro, all LF classes, pos1-specific baseline)
**Prerequisites:** none

## H_new_BX: RESOLVED — exp_497 (2026-04-11). ANSWERED: B herbal pos2: d→sh(F457 confirmed), F458(ch→ch) FLAGGED(2-word line bug, E=1.38×/N=13 with len≥3). NEW dir: ok→o@pos2(E=3.41×/N=6,F477). B herbal pos2 NOT universal self-chaining. Q009 opened.

## H_new_BX: B herbal pos2 Full Survey — original content below

**Priority:** medium
**Status:** resolved
**Source:** B herbal pos2: only ch-LF and d-LF are confirmed (F457, F458). The pos2 distributions for ok-LF (N=39), sh-LF (N=19), a-LF (N=19), ot-LF (N=11), ol-LF (N=13) are unknown. Does B herbal have additional confirmed pos2 routing rules? Given B herbal's different LF distribution (ch>ok>d vs A herbal_a d>ch>ok), the pos2 grammar may reflect different class priorities.
**Description:** For B herbal: compute pos2 routing E for all LF classes with N_lf≥8 using B herbal pos2-specific baseline. Show full pos2 distribution for each (top 5 by E). Compare with A herbal_a universal pos2 self-chaining (F468) and known B herbal confirmed rules (F457, F458).
**Expected outcome:** Some B herbal LF classes may self-chain at pos2 (like A herbal_a); others may show cross-class routing. The pattern will contrast with A herbal_a's universal self-chaining.
**Cost estimate:** small (B herbal, all LF classes, pos2-specific baseline)
**Prerequisites:** none

## H_new_BW: RESOLVED — exp_495 (2026-04-11). ANSWERED: F468 is CLASS-LEVEL GRAMMATICAL, not bigram-driven. ch-LF: 70 self-chain cases, ALL 70 distinct word pairs (dist_ratio=1.00). d-LF: 27/23 distinct (dist_ratio=0.85). F468 magnitude context updated.

## H_new_BW: pos2 Self-Chaining Word-Level vs Class-Level — original content below

**Priority:** medium
**Status:** resolved
**Source:** F468 = A herbal_a pos2 self-chaining universal. Is this enrichment driven by recurring specific bigrams (word_A at pos2 in word_A-LF lines repeatedly) or distributed across many word pairs?
**Description:** For A herbal_a d-LF and ch-LF: (1) List all (pos2_word, LF_word) pairs. (2) Count distinct pairs vs total obs. (3) If top-3 pairs account for >50% of obs, enrichment is bigram-driven (lexical). If obs is spread across many pairs, enrichment is class-level (grammatical).
**Expected outcome:** If class-level (distributed), F468 is a grammatical rule. If bigram-driven, it may reflect formulaic phrases rather than grammar.
**Cost estimate:** small (A herbal_a only, word-pair frequency table)
**Prerequisites:** none

## H_new_BV: RESOLVED — exp_494 (2026-04-11). ANSWERED: B herbal has NO confirmed pos1 routing rules. ch-self=ZERO(N_elig=47), y-self=DEPLETED(E=0.35×). F472/F473 A-herbal_a-specific. B herbal dir: ot-LF→y@pos1(E=2.67×/N=6). F475 assigned.

## H_new_BV: B herbal pos1 Grammar Survey — Are There Confirmed pos1 Routing Rules? — original content below

**Priority:** high
**Status:** resolved
**Source:** exp_491 showed A herbal_a pos1: y-self(CONF), ch-self(CONF), d→ot(CONF), ot DEPLETED. B herbal pos1 is unknown. exp_492 showed B herbal ch-LF pos1 = y(12), s(6), qok(6), d(6) with pos1 baseline y=20.4%, d=19.0%, t=14.1%. Does B herbal have confirmed pos1 routing rules?
**Description:** For B herbal: compute pos1 routing E for all LF classes with N_lf≥8 using B herbal pos1-specific baseline. Key classes: ch-LF (N=48), ok-LF (N=39), d-LF (N=34), a-LF (N=19), sh-LF (N=19). Show full pos1 distribution for each (top 5 by E). Compare with A herbal_a pos1 findings.
**Expected outcome:** B herbal may have different pos1 routing than A herbal_a. Known: B herbal ch-LF pos1 ≠ A herbal_a ch-self (ch barely present at pos1 in B herbal). Could reveal B herbal-specific pos1 grammar.
**Cost estimate:** small (B herbal section, all LF classes, pos1-specific baseline)
**Prerequisites:** none

## H_new_BT: RESOLVED — exp_493 (2026-04-11). ANSWERED: Frame co-occurrence is NEAR BASELINE (cth@pos2+d@pen: 1/64 observed vs 0.62 expected). Formula frames = independent positional tendencies, not co-occurring structural units. d/ot/cth cycle ABSENT (d-LF cth@pen E=0.83× depleted; cth-LF ot@pos1 E=0.25× strongly depleted).

## H_new_BT: RESOLVED — original content below

**Priority:** high
**Status:** resolved (negative)
**Source:** exp_492: cth-LF → d@pen (CONF, F474) + ot-LF → cth@pen (dir, E=3.70×/N=9). Is there a systematic cth↔ot relationship at pen positions (ot-LF has cth at pen; cth-LF appears in d@pen context)? The F453 d-LF → ot@pos1 connection suggests: ot opens d-LF lines, d marks cth-LF at pen — is there a d/ot/cth triangular onset relationship?
**Description:** (1) Full A herbal_a ot-LF line structure: y[pos1](CONF) → pos2[?] → cth[pen](dir,E=3.70×/N=9) → ot[LF]. Compute co-occurrence of y@pos1 AND cth@pen within same ot-LF lines. (2) Full A herbal_a cth-LF structure: qo[pos1](dir) → cth[pos2](CONF) → d[pen](CONF) → cth[LF]. Compute co-occurrence. (3) Check: in ot-LF lines with cth at pen, what is at pos1 (is it always y)? (4) d-LF: ot at pos1 (CONF) — does d appear at pen of cth-LF specifically because cth is related to d (maybe through the d→ot opening relationship)?
**Expected outcome:** The frame co-occurrence rates (y AND cth both present in ot-LF; qo AND d both present in cth-LF) would quantify the frame coherence. Even if conditional frequencies are low, they validate the frame hypothesis.
**Cost estimate:** small (A herbal_a, line-level co-occurrence analysis for ot and cth LF classes)
**Prerequisites:** none

## H_new_BU: RESOLVED — exp_493 (2026-04-11). ANSWERED: B herbal ok-LF→a@pen dir(E=2.73×/N=6, consistent with F459); ot-LF→ot@pen (dir,E=5.43×/N=3, consistent with F460). New dir: a-LF→ok@pen(E=3.06×/N=5). No new confirmed pen findings. B-dialect-wide pen rules confirmed in B herbal at directional level.

## H_new_BU: RESOLVED — original content below

**Priority:** medium
**Status:** resolved
**Source:** A herbal_a pen survey (exp_492) found confirmed and directional pen rules. B-dialect pen rules F459/F460 came from combined B sections. Does B herbal show the same B-dialect pen rules?
**Description:** For B herbal: compute pen routing E for all LF classes with N_lf≥8 using ws[-2] as pen baseline. Primary tests: (1) B herbal ok-LF → a@pen (parallel to F452/F459); (2) B herbal ot-LF → ot@pen (parallel to F450/F460); (3) B herbal ch-LF pen routing (unknown). Secondary: d/sh/a LF classes.
**Expected outcome:** ok→a@pen and ot→ot@pen likely confirmed or directional in B herbal (consistent with B-dialect-wide F459/F460). ch-LF pen unknown — could reveal a B herbal-specific rule.
**Cost estimate:** small (B herbal section, all LF classes, ws[-2] baseline)
**Prerequisites:** none

## H_new_BR: RESOLVED — exp_492 (2026-04-11). ANSWERED: A herbal_a has confirmed pen routing (F474: cth-LF→d@pen,E=1.61×/N=18,CONF). Directional: ok→ok-self@pen(dir,3.39×/N=7), ot→cth@pen(dir,3.70×/N=9). No confirmed pen rule for d, ch, sh. cth frame: qo@pos1(dir)→d@pen(CONF)→cth@LF.

## H_new_BR: RESOLVED — original content below

**Priority:** high
**Status:** resolved
**Source:** F453/F454 were retracted due to exp_479 pen baseline bug. exp_485 confirmed pen signals are weaker. Now that pos1/pos2 are fully characterized, systematically assess pen routing with correct ws[-2] baselines for all A herbal_a LF classes.
**Description:** For all A herbal_a LF classes with N_lf≥10: compute pen routing E using ws[-2] distribution as pen baseline. Key classes: d(N=254), ch(N=183), ok(N=57), ot(N=43), sh(N=41), cth(N=74). Cross-reference with B-dialect confirmed pen rules (F459 ok→a@pen, F460 ot→ot@pen) — do any A herbal_a classes show parallel pen routing?
**Expected outcome:** Probably few confirmed signals. exp_485 showed A herbal_a has no confirmed pen rules. Directional signals possible for ot, sh, ok. The B-dialect's ok→a@pen (F459) suggests a pen position can be grammar-bearing — does A herbal_a have a pen rule for any class?
**Cost estimate:** small (A herbal_a, all LF classes, pen-specific baseline from ws[-2])
**Prerequisites:** none; must use ws[-2] as pen baseline

## H_new_BS: RESOLVED — exp_492 (2026-04-11). ANSWERED: ch@pos1 NOT cross-dialectal within herbal. B herbal flat(E=0.80×/obs=1); B astro below(E=1.18×); A cosmo below(E=0.65×). Scope: A herbal_a(F473,CONF) + B pharma(F449,CONF) only. B herbal ch-LF pos1 dominated by y/d/s/qok (different grammar). Scope is section-specific, NOT herbal-register-wide.

## H_new_BS: RESOLVED — original content below

**Priority:** medium
**Status:** resolved
**Source:** F473: A herbal_a ch-LF → ch-self@pos1 (E=1.58×/N=30, CONF). F449: B pharma ch-LF → ch@pos1 (E=1.64×/N=15, CONF). Two independent confirmations! Does ch-LF → ch@pos1 extend to B herbal, B astro, A cosmo? If so, ch-LF → ch@pos1 would be cross-dialectal and cross-sectional.
**Description:** For B herbal, B astro, A cosmo: compute ch at pos1 E for ch-LF lines with section-specific pos1 baselines. B herbal ch-LF has N=48 (reasonable). B astro ch-LF has N=85. A cosmo ch-LF has some N. If ch@pos1 is universal (like ch@pos2 within herbal), it's a major cross-section grammar rule.
**Expected outcome:** ch@pos1 likely elevated in B herbal (parallels F449 B pharma). B astro and A cosmo less certain. If confirmed in B herbal, ch-LF → ch@pos1 is broader than just one section.
**Cost estimate:** small (3 sections, ch-LF class only)
**Prerequisites:** none

## H_new_BP: RESOLVED — exp_491_pos1_selfchain_survey (2026-04-11). ANSWERED: pos1 NOT universal. F472: y-LF→y-self@pos1(CONF,E=2.13×/N=11); F473: ch-LF→ch-self@pos1(CONF,E=1.58×/N=30). ot DEPLETED(E=0.43×). Pos1 serves TWO functions: cross-class opener(d/ok/ot) vs self-chaining(ch/y/sh/qot/s).

## H_new_BP: RESOLVED — original content below

**Priority:** high
**Status:** resolved
**Source:** F468 established universal pos2 self-chaining in A herbal_a. Known pos1 routing: d-LF→ot@pos1 (F453), ok-LF→y@pos1 (F455), ot-LF→y@pos1 (F456) — these are CROSS-CLASS pos1 routings. But sh-LF → sh-self at pos1 (dir, E=2.55×/N=9) and s-LF → s-self at pos1 (dir, E=6.07×/N=7) suggest pos1 also has some self-chaining. Is pos1 self-chaining also universal (like pos2) or partial?
**Description:** For A herbal_a, compute pos1 self-chaining E for all LF classes with N_lf≥10. Use pos1-specific baseline. Key question: does d-LF → d-self at pos1 (alongside ot routing)? Does ch-LF → ch-self at pos1? Are they LOWER than pos2's self-chaining (where d E=1.56×, ch E=1.60×)? If pos1 self-chaining is absent where cross-class routing exists (d→ot, ok→y) but present where no cross-class routing is found, this supports the model that pos1 and pos2 play different roles in A herbal_a line grammar.
**Expected outcome:** Partial self-chaining at pos1 — sh and s directional, while d/ok/ot show self-chaining DEPLETED at pos1 (because cross-class routing dominates). ch may or may not self-chain at pos1.
**Cost estimate:** small (A herbal_a, all LF classes, pos1-specific baseline)
**Prerequisites:** none

## H_new_BO: RESOLVED — exp_490 (2026-04-11). REFUTED: ch@pos2 is NOT elevated in B pharma. All LF classes show E≤1.37× for ch@pos2; d-LF STRONGLY DEPLETED (E=0.33×); ot-LF E=0.75×. High raw counts were baseline artifact (25.3% ch at pos2 in B pharma). No universal ch-routing rule.

## H_new_BO: RESOLVED — original content below

**Priority:** medium
**Status:** resolved (refuted)
**Source:** exp_489: In B pharma, ch appears as the top non-self pos2 onset for virtually ALL LF classes: l-LF non-self(ch=24), ot-LF non-self(ch=15), ok-LF non-self(ch=17), a-LF non-self(ch=20). This suggests B pharma has a UNIVERSAL ch@pos2 rule regardless of LF class — the opposite of A herbal_a's self-chaining grammar.
**Description:** Formally test: is ch@pos2 elevated above baseline in B pharma for ALL or most LF classes? Use B pharma pos2 baseline. Compute ch at pos2 E for ot-LF, l-LF, ok-LF, a-LF, qok-LF, d-LF. If ch@pos2 is elevated in every class (E≥1.5×), then B pharma has the mirror-opposite grammar to A herbal_a: where A self-chains, B pharma routes everyone to ch. This would be a remarkable A/B grammar contrast at the pos2 level.
**Expected outcome:** If confirmed, ch@pos2 is universal in B pharma (≥5 LF classes). This would be a major structural finding contrasting A herbal_a's self-chaining with B pharma's ch-routing.
**Cost estimate:** small (B pharma, all LF classes, ch at pos2 enrichment)
**Prerequisites:** none

## H_new_BN: RESOLVED — exp_490 (2026-04-11). ANSWERED: B astro pos2 self-chaining is selective (not universal). ol-LF CONFIRMED (E=1.54×/N=15, F471); sh CONFIRMED (F469). qok-LF below threshold (E=1.28×/N=18); qot=ZERO. B astro ch-LF just below threshold (E=1.46×/N=19, consistent with F462 herbal-specific scope).

## H_new_BN: RESOLVED — original content below

**Priority:** medium
**Status:** resolved
**Source:** exp_487 showed sh→sh@pos2 is CONFIRMED in B astro (F469, E=1.59×/N=10). B astro has the q-bench triplet as dominant LF classes: qok(N=149), qot(N=29), qo(N=34). Does pos2 self-chaining appear for these B astro LF classes?
**Description:** For B astro: compute pos2 self-chaining E for qok-LF, qot-LF, qo-LF, s-LF, sh-LF (F469 already confirmed), d-LF. Use B astro section-specific pos2 baseline. Key tests: (1) qok-LF → qok@pos2 (N=149, largest B astro class — best chance for confirmation); (2) qot-LF → qot@pos2 (N=29); (3) qo-LF → qo@pos2 (N=34). If the q-bench self-chains at pos2, this would be B astro having its own version of the pos2 self-chaining grammar.
**Expected outcome:** qok possibly confirmed (large N=149); qot/qo directional. The B astro grammar may feature q-bench self-chaining at pos2, contrasting with the pharma ch-dominance pattern.
**Cost estimate:** small (B astro section, targeted LF classes)
**Prerequisites:** none

## H_new_BJ: RESOLVED — exp_488_f448_retraction (2026-04-11). F448 RETRACTED. ok@pos2 in y-LF lines has obs=0 (E=0.00×). exp_476 classified lines with y at pos1 (N=136) instead of y at LF (N=37). y-LF → y-SELF at pos2 (E=7.87×/N=8, dir) is the correct pattern, consistent with F468. Q008 closed.

## H_new_BJ: RESOLVED — original content below

**Priority:** critical
**Status:** resolved
**Source:** exp_476 claimed A herbal_a y-LF → ok at pos2 (E=2.25×/N=20, CONF, N_lf=124). exp_487 finds N_lf=37 for y-LF in A herbal_a and obs≤1 for ok at pos2. The 3.4× line-count discrepancy (124 vs 37) and the obs discrepancy (20 vs ≤1) both point to a classification bug in exp_476. The result.md for exp_476 explicitly notes "Unique folios: 1 (folio tracking variable bug)". Script is unavailable.
**Description:** Run a targeted script that: (1) reproduces exp_487's methodology for y-LF in A herbal_a exactly (same corpus parse, same onset priority, same section classifier), (2) outputs the exact N_lf count for y and the full pos2 distribution, (3) explicitly computes obs for ok@pos2 vs y-self@pos2, (4) also tests y-self@pos2 against confirmation thresholds (it's N=8, dir — can we upgrade?). If ok@pos2 obs≤1 is confirmed, F448 should be retracted and replaced with the y-self finding.
**Expected outcome:** ok@pos2 obs≤1, confirming exp_476 was buggy. y-self@pos2 directional (E=7.87×/N=8, same as exp_487). F448 should be formally retracted.
**Cost estimate:** minimal (extract y-LF from exp_487 methodology, one section, targeted output)
**Prerequisites:** none

## H_new_BK: RESOLVED — exp_489_b_herbal_pos2_selfchain (2026-04-11). ANSWERED: B herbal pos2 self-chaining is NOT universal. ot/ol/l show obs=0; only ch CONFIRMED (F458); sh+a directional; ok/d below threshold. F468 does NOT extend to B herbal. A/B ot-LF pos2 inversion: A→ot-self(dir); B→ZERO. F470: B herbal a-LF→a@pos2(E=3.60×/N=6,dir).

## H_new_BK: RESOLVED — original content below

**Priority:** high
**Status:** resolved
**Source:** F468 established universal pos2 self-chaining in A herbal_a. B herbal has confirmed ch-LF→ch@pos2 (F458) and d-LF→sh@pos2 (F457, cross-class). We don't know if B herbal also shows d-LF→d-SELF at pos2, or if B herbal's ok/ot/sh/y LF classes self-chain.
**Description:** For B herbal (N=269 lines): compute pos2 self-chaining E for ALL LF classes with N_lf≥5. Use B-herbal-specific pos2 baseline. Primary questions: (1) d-LF → d-self at pos2 (B has d→sh at pos2 CONF, but does d also appear above d-self baseline?); (2) ok-LF → ok-self at pos2; (3) ot-LF → ot-self at pos2; (4) sh-LF → sh-self (dir in A herbal_a, F463 scope showed dir in B herbal E=2.10×/N=7); (5) y-LF → y-self (was flat previously, but with universal rule in mind). If B herbal also shows universal pos2 self-chaining, the rule extends beyond A herbal_a dialect boundary. If not, the universal rule is A-herbal_a-specific.
**Expected outcome:** Likely partial — ch is confirmed (F458); some others directional. Key test is whether d-LF shows d-self@pos2 (would coexist with F457's d→sh; two different pos2 enrichments possible).
**Cost estimate:** small (B herbal section, all LF classes, one pass)
**Prerequisites:** none

## H_new_BL: RESOLVED — exp_489_b_herbal_pos2_selfchain (2026-04-11). ANSWERED: B pharma pos2 self-chaining absent for most classes (ch E=1.30×, l E=1.42×, qok/ok/a near baseline). Only ot(dir,E=2.19×/N=5) and sh(dir,E=2.09×/N=7) show signals — consistent with multi-section scope for ot and sh. B pharma's pos2 dominant pattern is ch appearing for ALL LF classes (not self-chaining). F468 does NOT extend to B pharma.

## H_new_BL: RESOLVED — original content below

**Priority:** medium
**Status:** resolved
**Source:** F468 universal pos2 self-chaining is established only in A herbal_a. B pharma has confirmed ch→ch at pos1 (F449), not pos2. B pharma has ot-LF (N=79), l-LF (N=~50), ok-LF (N=44), ch-LF (N=~50). Does pos2 self-chaining hold in B pharma for these major LF classes?
**Description:** For B pharma: compute pos2 self-chaining E for all LF classes with N_lf≥10. Use B-pharma-specific pos2 baseline. We already know ch→ch@pos2 is BELOW threshold in B pharma (E=1.30×, F462). Key classes to test: ot-LF→ot@pos2, l-LF→l@pos2, ok-LF→ok@pos2, d-LF→d@pos2, qok-LF→qok@pos2. If B pharma shows a different pattern from A herbal_a (e.g., no universal self-chaining), this would establish that pos2 self-chaining is a herbal-register-specific rule (parallel to the way ch@pos2 scope is herbal-specific per F462).
**Expected outcome:** Partial or absent — ch is not herbal-specific at pos2 in B pharma. Some classes may show it (ot has ot@pen as dominant rule in B pharma), others won't. If no LF class shows pos2 self-chaining in B pharma, the universal self-chaining rule (F468) is herbal-section-specific.
**Cost estimate:** small (B pharma section, all LF classes, one pass)
**Prerequisites:** none

## H_new_AV: RESOLVED (exp_481). F456 ASSIGNED. ANSWERED: A herbal_a ot-LF → y at pos1 (CONFIRMED, E=1.83×/N=11, F456). Full formula grammar matrix synthesized. y functions as line-opener for both ok-LF(F455) and ot-LF(F456) — dual o-gallows opener. sh is provisional "universal pen mediator" for d/o/s LF classes. sh-LF: no confirmed findings (N=38). qot-LF: still no confirmed findings (N=31). Directional: ot-LF cth pen(4.05×/N=9), s-LF sh pos2(2.32×/N=5), o-LF sh pen(2.02×/N=5), k-LF ok pos1(2.14×/N=5).

## H_new_AX: RESOLVED (exp_482). F457/F458 ASSIGNED. ANSWERED: B herbal d-LF→sh at pos2(CONF,F457); ch-LF→ch at pos2(CONF,F458). Cross-dialectal onset-class pairing conserved (d/sh, ch/ch) but positional placement shifts: A herbal_a places grammar-pairs at pen; B herbal places them at pos2. ot-LF→y(dir,E=2.67×/N=6). ok-LF→y FLAT. H_new_AW embedded: mixed result (ot-LF→y cross-dialectal dir; ok-LF→y A-specific).

## H_new_AX: RESOLVED — original content below for reference
**Priority:** high
**Status:** resolved
**Source:** exp_481 completed the A herbal_a formula matrix (F448/F453-F456). B herbal is the counterpart section (folios f1-72 B-dialect). B herbal LF distribution (F447): t-LF(2.34×/N=38) + y-LF(1.52×/N=55) as primary elevated classes; ch/ok/ot also present. Partial characterization exists: B herbal t-LF → qok pos1(dir,N=6), o pos2(dir,N=5), o LL(dir,N=5); y-LF → y pos1(dir,N=5), ot LL(dir,N=6). None confirmed at N≥10.
**Description:** For B herbal (B-dialect folios, folio n≤72): compute full pos1/pos2/pen routing for all LF classes with N_lf≥20 (expected: t~38, y~55, ch, ok, ot, d). Compute with B herbal section-specific baselines (not B-overall). Reproduce t-LF and y-LF directional signals with consistent implementation; check if any reach N=10 confirmation threshold. Also compute: do ok-LF and ot-LF lines start with y at pos1 (as in A herbal_a F455/F456)? If B herbal mirrors A herbal_a, y/ok and y/ot are cross-dialectal grammar pairs.
**Expected outcome:** 
- If B herbal ok-LF → y at pos1 (paralleling F455): y/ok opening is cross-dialectal. Argues for a structural grammar rule transcending dialect boundary.
- If not: F455/F456 are A-herbal_a-specific routing rules.
- t-LF likely shows qok at pos1 (from exp_472 dir finding); confirmation would elevate this to a confirmed B herbal t-LF formula rule.
**Cost estimate:** small (single script, B herbal section, ~550 lines)
**Prerequisites:** none; use B herbal baseline (not B-overall)

## H_new_BA: A/B Herbal Positional Shift — Line Length Artifact or Grammar Rule?

**Priority:** high
**Status:** RESOLVED — exp_484_ab_herbal_positional_shift (2026-04-11)
**Source:** exp_482: A herbal_a ch-LF → ch at pen (F454); B herbal ch-LF → ch at pos2 (F458). A herbal_a d-LF → sh at pen (F453); B herbal d-LF → sh at pos2 (F457). Both onset-pairs are conserved but the positional placement systematically shifts: A places them at pen, B places them at pos2. Two competing explanations: (a) Line-length artifact — B herbal lines may be shorter on average, so pen and pos2 converge for many lines; (b) Genuine grammar difference — A and B dialects have different positional schemas for the same onset-class pairings.
**Resolution:** NEITHER — the premise was wrong. exp_484 revealed that exp_479 had a baseline bug (LF-rate used instead of pen-rate as pen baseline). With correct position-specific baselines: (1) A herbal_a ch at pen = E=1.32×, below threshold — NOT confirmed; (2) A herbal_a sh at pen = E=0.85×, DEPLETED. The "A places grammar-pair onsets at pen" narrative was entirely an artifact of the bug. Real picture: BOTH A and B herbal confirm ch self-chaining at pos2 (F461: A E=1.60×/N=94; F458: B E=1.74×/N=19). d/sh at pos2 is B-herbal-specific (A herbal_a d-LF → sh is not confirmed anywhere). Also: B herbal lines are LONGER (mean 6.34) than A herbal_a (mean 4.52) — so line-length could not have explained a B-pos2 preference even if the premise were true.
**Cost estimate:** small (line-length comparison + conditional analysis)
**Prerequisites:** none

## H_new_AZ: RESOLVED (exp_483). F459/F460 ASSIGNED. ANSWERED: ot-LF→y@pos1 is HERBAL-SECTION-SPECIFIC (A+B herbal show it; B pharma/astro flat/depleted). ok→a@pen is B-DIALECT-WIDE (F459, E=2.79×/N=19, B herbal+pharma+astro all E≈2.7×). ot→ot@pen is B-DIALECT-WIDE (F460, E=2.24×/N=25, extends F450 from pharma to B-combined).

## H_new_AZ: RESOLVED — original content below for reference
**Priority:** high
**Status:** resolved
**Source:** exp_482: B herbal ot-LF → y at pos1 (dir, E=2.67×/N=6). A herbal_a ot-LF → y at pos1 (CONF, F456). If ot/y is cross-dialectal, it should also appear in B pharma and B astro. B pharma has ot-LF (N=79, F450 characterized ot at pen but not y at pos1). Also: B herbal ok-LF → a at pen (dir, E=2.73×/N=6) + B pharma ok-LF → a at pen (CONF, F452). Is ok→a pen a B-dialect rule (both herbal+pharma)?
**Description:** (1) For B pharma and B astro ot-LF lines: compute y at pos1 with section-specific baselines. If B pharma ot-LF → y at pos1 (N=79 available, confirmed possible), this strongly supports ot/y as cross-dialectal. (2) For B herbal ok-LF (N=39): directly test ok→a at pen with confirmation thresholds — is N=6 obs=6/35 pen-eligible lines sufficient to confirm? (The exp_482 script showed dir; check if N_pen=35 and obs=6 → E=2.73× meets confirmation: N=6 < 10, so directional only. Need B-dialect combined ok-LF test.)
**Expected outcome:**
- If B pharma ot-LF → y at pos1 (N=79, likely N_y≥10): F456 would get a B-dialect confirmation (separate finding)
- If ok→a at pen is confirmed in B-dialect combined (herbal+pharma ok-LF pooled): new B-dialect finding
**Cost estimate:** small (targeted query for two LF classes across B sections)
**Prerequisites:** none

## H_new_AW: RESOLVED (exp_482, embedded in H_new_AX). ANSWERED (mixed): ot-LF→y at pos1 shows cross-dialectal directional conservation (A CONF F456 + B dir E=2.67×/N=6). ok-LF→y at pos1 is A-herbal_a-specific (B herbal FLAT E=1.13×/N=9). The y/ot opener may be cross-dialectal; y/ok is A-specific.

## H_new_AW: RESOLVED — original content below for reference
**Priority:** high
**Status:** resolved
**Source:** F455 (A herbal_a ok-LF → y at pos1, E=1.62×/N=12) and F456 (A herbal_a ot-LF → y at pos1, E=1.83×/N=11). These are the most recently confirmed A herbal_a formula rules. The A/B comparison for d-LF shows A uses ot at pos1 while B uses qok/ch — a grammar inversion. Does the y/ok-opener rule also invert across dialects, or is it preserved?
**Description:** For B herbal and B pharma separately: compute pos1 onset distribution for ok-LF and ot-LF lines with section-specific baselines. Primary test: is y at pos1 elevated for ok-LF in B (as in A herbal_a F455)? Secondary: do the B section-specific ok/ot-LF pos1 distributions reveal a B-specific alternative opener (e.g., qok at pos1 for ok-LF lines, consistent with B's qok-dominance)?
**Expected outcome under competing theories:**
- A/B grammar conservation: B herbal ok-LF → y at pos1 elevated (same as A herbal_a) → y/ok is a cross-dialectal pair
- A/B grammar inversion: B herbal ok-LF → different onset at pos1 (e.g., qok or sh) → y/ok is A-dialect-specific
- Null: flat distribution → pos1 routing for ok-LF is section-specific, not grammar-level
**Cost estimate:** small (subset of B herbal + B pharma analysis, targeted two-class query)
**Prerequisites:** none

## H_new_BH: RESOLVED — exp_487_pos2_selfchain_survey (2026-04-11). ANSWERED: pos2 self-chaining is UNIVERSAL in A herbal_a. All LF classes with N_elig≥10 show self-chaining E≥1.56×: d(E=1.56×/N=44,CONF), ch(E=1.60×/N=94,CONF), cth(E=3.46×/N=14,CONF), ok(E=4.53×/N=10,CONF), sh(E=2.64×/N=12,CONF), o(E=7.03×/N=10,CONF). All smaller classes directional (ot, k, y, qot, s, qok all E≥3.7×). F465-F468 ASSIGNED. F448 FLAGGED (y-LF → ok@pos2 not reproduced).

## H_new_BH: RESOLVED — original content below

**Priority:** high
**Status:** resolved
**Source:** exp_486: ch (F461, E=1.60×), sh (F463, E=2.64×), and o (F464, E=7.03×) all show LF-class self-chaining at pos2 in A herbal_a. Three independent confirmed findings. This might be a universal A herbal_a rule: for EVERY LF class, the LF onset also appears at pos2 above baseline. Or it might be selective to ch/sh/o.
**Description:** Systematically test pos2 self-chaining for ALL A herbal_a LF classes with N_lf≥10: d, y, ok, ot, qot, sh, o, s, k. For each: compute onset-self at pos2 E with pos2-specific baseline. Key tests: (1) d-LF → d at pos2 (currently shown as 1.76×/N=4 from exp_486, directional but N too small); (2) y-LF → y at pos2 (y is a single-char onset, appears at end; check if y also appears at pos2); (3) ok-LF → ok at pos2 (F448 matrix shows ok-self pos2 directional from exp_481); (4) ot-LF → ot at pos2 (exp_481 showed k at pos2, not ot-self; but ot-self not explicitly checked). If the pattern holds for ALL classes, pos2 self-chaining is a general A herbal_a grammar axiom.
**Expected outcome:**
- Universal: every LF class shows pos2 self-chaining E≥1.5× (or directional E≥2×) — implies a strong structural constraint on line structure in herbal sections
- Selective: only ch/sh/o show it; d/y/ok do not — implies these specific onset classes have distinctive line-internal grammar
**Cost estimate:** small (A herbal_a, all LF classes, one pass)
**Prerequisites:** none; use pos2-specific A herbal_a baselines

## H_new_BI: RESOLVED — exp_487_pos2_selfchain_survey (2026-04-11). ANSWERED: sh is NOT herbal-section-specific — B astro sh-LF→sh@pos2(E=1.59×/N=10,CONF,F469); B pharma dir(E=2.09×/N=7); A cosmo E=1.88×. Contrasts with ch (herbal-specific per F462). o appears A-herbal_a-specific: B herbal flat(E=1.36×), B pharma N=4 insufficient. Pos2 self-chaining scope is onset-dependent: ch=herbal-only, sh=multi-section, o=A-herbal_a-only.

## H_new_BI: RESOLVED — original content below

**Priority:** medium
**Status:** resolved
**Source:** F462 showed ch→ch@pos2 is herbal-section-specific. F463 (sh→sh@pos2) and F464 (o→o@pos2) are currently tested only in A herbal_a. Are sh and o pos2 self-chaining also herbal-specific?
**Description:** For B pharma and A cosmo: compute sh-LF → sh at pos2 and o-LF → o at pos2 with section-specific pos2 baselines. B pharma sh-LF and o-LF should be reasonably sized. If these also show herbal-section-specificity (like ch), it strengthens the "herbal grammar register" framework. If they appear in B pharma, the pos2 self-chaining is broader than ch-specific.
**Expected outcome:**
- If sh→sh@pos2 and o→o@pos2 are herbal-specific: the entire pos2 self-chaining phenomenon is content-conditional (herbal domain) → powerful herbal grammar register
- If sh→sh@pos2 appears in B pharma: pos2 self-chaining is partial (ch is herbal-specific but sh is broader) — the rule scope is onset-dependent
**Cost estimate:** small (B pharma + A cosmo, 2 LF classes each)
**Prerequisites:** none

## H_new_BF: RESOLVED — exp_486_b_herbal_remaining_lf (2026-04-11). ANSWERED: d-LF→ot@pos1 is A-herbal_a-SPECIFIC (B herbal depleted E=0.88×). ok-LF→y@pos1 (F455) is A-herbal_a-SPECIFIC (B herbal flat E=1.13×). B herbal ok-LF → o@pos2 (E=3.36×/N=6, dir) and a@pen (E=2.73×/N=6, dir) — consistent with F459. B herbal y-LF N=15 too small.

## H_new_BF: RESOLVED — original content below

**Priority:** high
**Status:** resolved
**Source:** A herbal_a formula matrix complete (F448/F453-F456/F461). B herbal characterized for ch-LF (F458, pos2) and d-LF (F457, pos2), and ot-LF (dir, pos1). Three major B herbal LF classes not characterized: d-LF pos1 (A has ot, F453; B might differ), y-LF pos1/pos2 (A has y→ok@pos2, F448), ok-LF pos1 (A has ok→y@pos1, F455 — tested flat in B, E=1.13×/N=9, but pos2 not tested).
**Description:** For B herbal (N=269 lines): compute pos1 and pos2 routing for d-LF, y-LF, and ok-LF with B herbal section-specific baselines. Key questions: (1) B herbal d-LF → ot at pos1 (A herbal_a conserved rule)? If B herbal d-LF also starts with ot, this is cross-dialectally conserved. If B herbal d-LF starts with qok or ch (F426 formula types), it's A-herbal_a-specific. (2) B herbal y-LF → ok at pos2 (A herbal_a F448 conserved)? (3) B herbal ok-LF pos2: any elevated onset?
**Expected outcome:**
- d-LF pos1: either ot (cross-dialectal conservation of F453) or qok/ch (A-specific; B dialect routes d-LF differently)
- y-LF pos2: either ok (F448 cross-dialectal) or something different (A-specific)
- ok-LF pos2: unknown — check for B herbal signature
**Cost estimate:** small (B herbal subset, 3 LF classes)
**Prerequisites:** none

## H_new_BG: RESOLVED — exp_486_b_herbal_remaining_lf (2026-04-11). **F463** (sh-LF→sh@pos2, E=2.64×/N=12, CONF) + **F464** (o-LF→o@pos2, E=7.03×/N=10, CONF). qot-LF: directional only (qot-self@pos2 E=6.48×/N=6, sh@pos2 E=2.43×/N=9). s-LF: s-self@pos1 dir (E=6.07×/N=7). Pos2 self-chaining generalization: ch/sh/o all self-chain at pos2 in A herbal_a.

## H_new_BG: RESOLVED — original content below

**Priority:** medium
**Status:** resolved
**Source:** A herbal_a formula grammar matrix: sh-LF (N=38) and qot-LF (N=31) are the only major LF classes without confirmed routing rules. sh-LF: sh at pos1 (dir, E=1.83×); qot-LF: qot-self at pos1 (dir, E=2.31×/N=5); cth at pos2 (dir, E=2.32×/N=8). With N=38 and N=31, confirmation is marginal but possible for strong signals.
**Description:** For A herbal_a sh-LF (N=38) and qot-LF (N=31): compute complete pos1/pos2/pen routing with A herbal_a section-specific baselines. Key focus: (1) sh-LF pos1 sh self-succession: E=1.83×/N=6 — is this robust with full dataset? (2) qot-LF pos2 cth: E=2.32×/N=8 — near-threshold, check if N≥10 or if cth reaches confirmation. (3) qot-LF pos1 qot-self: E=2.31×/N=5 — marginal directional. (4) Are there pen rules for either class?
**Expected outcome:**
- sh-LF: sh at pos1 may reach directional threshold (N=6 → near-threshold); no pen rule likely
- qot-LF: cth at pos2 may reach N=10 if slightly larger dataset; qot-self at pos1 directional
- If qot-LF → cth at pos2: extends F406 (qot→ch→cth formula types) with a pos2-conditional routing rule
**Cost estimate:** small (A herbal_a subset, 2 LF classes)
**Prerequisites:** none

## H_new_BB: RESOLVED — exp_485_ch_lf_pos2_scope (2026-04-11). F462 ASSIGNED. ANSWERED: ch→ch@pos2 is HERBAL-SECTION-SPECIFIC. B pharma E=1.30× (below threshold), B astro E=1.46×, A cosmo E=1.06× (flat), B cosmo E=0.68× (depleted). Content-conditional: herbal domain activates rule, non-herbal domains do not. Parallels ot-LF→y@pos1.

## H_new_BB: RESOLVED — original content below for reference

**Priority:** high
**Status:** resolved
**Source:** F461 (A herbal_a ch-LF → ch at pos2, E=1.60×/N=94, CONFIRMED) and F458 (B herbal ch-LF → ch at pos2, E=1.74×/N=19, CONFIRMED) establish ch self-chaining at pos2 as cross-dialectally conserved in herbal sections. Is this herbal-section-specific or does it extend to pharma, astro, cosmo, stars?
**Description:** For all major sections with sufficient ch-LF N (B pharma, B astro, A stars, A cosmo, B cosmo): compute ch at pos2 in ch-LF lines using section-specific pos2 baselines. The key discriminating sections are B pharma (large corpus, ch-LF characterized in F449 for pos1 but not pos2) and B astro (moderate corpus). If ch→ch@pos2 appears in B pharma, it is B-dialect-wide (or broader). If absent in B pharma, it is herbal-section-specific (content-conditional, like ot-LF→y@pos1).
**Expected outcome under competing theories:**
- If ch→ch@pos2 extends to B pharma and B astro: ch self-chaining at pos2 is a universal (section-general) within-line grammar rule, possibly a fundamental positional constraint
- If ch→ch@pos2 is herbal-only: ch at pos2 is content-conditional (herbal context activates ch self-chaining); pharma context may deactivate it or use a different rule
- If ch→ch@pos2 is B-dialect-wide but absent in A cosmo: it's a dialect-conditional rule that crosses content boundaries within one dialect
**Cost estimate:** small (one script, 5-6 sections)
**Prerequisites:** none; use section-specific pos2 baselines (not section-general)

## H_new_BC: RESOLVED — exp_485_ch_lf_pos2_scope (2026-04-11). ANSWERED: A herbal_a d-LF pen = no confirmed signal (highest: ckh E=1.52×/N=6, below thresholds). sh depleted (E=0.85×). B pharma F450 corrected (1.94→1.75×, still CONF), F451 corrected (1.62→2.18×, CONF, stronger), F452 corrected (2.04→2.75×, CONF, stronger). New directional: A herbal_a ch-LF → ol at pen (E=2.09×/N=5, dir).

## H_new_BC: RESOLVED — original content below for reference

**Priority:** medium
**Status:** resolved
**Source:** exp_484 retracted sh at pen for A herbal_a d-LF (E=0.85×, DEPLETED). The d-LF pen profile is now uncharacterized (no confirmed signals). Also: exp_479 had a baseline bug that may have affected B pharma F450 (ot→ot@pen) and F451 (l→l@pen) E values — though the direction of bias likely deflated rather than inflated them.
**Description:** (1) For A herbal_a d-LF (N=254): compute full pen onset distribution with correct ws[-2] pen baseline. List all onsets with E≥1.3× at pen. What was actually at pen for d-LF lines? (2) For B pharma: recompute F450 (ot-LF→ot@pen) and F451 (l-LF→l@pen) with ws[-2] pen baseline. Compare to exp_479's buggy E values to confirm direction of bias and validate that F450/F451 remain confirmed with correct baselines.
**Expected outcome:**
- A herbal_a d-LF pen: likely flat (the retraction showed sh was depleted, ch was flat at 1.03×) — "no pen rule for d-LF" is the expected result with correct baselines
- B pharma F450/F451: expected to INCREASE in E value (since bug deflated them for common-LF-class onsets); both should remain confirmed
**Cost estimate:** small (A herbal_a + B pharma pen analysis, ~20 lines of focused code)
**Prerequisites:** none

## H_new_AT: RESOLVED (exp_479). F450/F451/F452 ASSIGNED. ANSWERED (multiple confirmations): B pharma ot-LF→ot at pen(CONFIRMED,F450); l-LF→ok pos2+l pen(BOTH CONFIRMED,F451); ok-LF→a at pen(CONFIRMED,F452). Pharma penultimate self-succession is a recurring pattern: ch(pos1),ot(pen),l(pen),ok(a-pen).

**Previous content:**
**Priority:** medium
**Status:** open
**Source:** exp_478: B pharma LF distribution shows ot-LF(N=79, 9.9%) and l-LF(N=92, 11.5%) as major classes with NO self-succession. Full pos1/pos2/LL routing not characterized. F423 (pharma l-chain) involves l in within-line MID positions — does l-LF show distinct routing from l at other positions?
**Description:** For B pharma (N=799): compute full pos1/pos2/LL routing for ot-LF(N=79) and l-LF(N=92) with section-specific baselines. Key questions: (1) Does ot-LF have any confirmed routing rule (N≥10, E≥1.5×) at any position? (2) Does l-LF route to d at pos1 (exp_478 d→l dir, reverse direction possible)? (3) Is ot-LF routing different from ot-class in other B sections?
**Expected outcome:** ot-LF may route to qok or ok at pos1 (pharma template routing). l-LF may route to d or qok at pos1 (consistent with d→l dir from exp_478 suggesting d-l linkage). If ot-LF has confirmed routing, this would complete the top-4 B pharma LF classes: ch(F449), l, ot, and a(11.0%, skip—a is suffix-like).
**Cost estimate:** small (subset of exp_478's full routing)
**Prerequisites:** none

## H_new_AS: RESOLVED (exp_479). F453/F454 ASSIGNED. ANSWERED (A herbal_a lacks confirmed self-succession; new confirmed LF routing rules found): A herbal_a d-LF→ot pos1(CONFIRMED,F453)+sh pen(CONFIRMED,F453); ch-LF→ch pen(CONFIRMED,F454)+k pen(CONFIRMED,F454). A herbal_a ch self-succession at pos1 NOT confirmed (1.36×/N=25). qot-self at pos1 directional(2.31×/N=5).

**Previous content:**
**Priority:** medium
**Status:** open
**Source:** F449 (exp_478): B pharma ch-LF → ch at pos1 (CONFIRMED). exp_476: A herbal_a y-LF → y at pos1 (E=2.25×/N=8, dir). Does A herbal_a have LF-class self-succession for any class analogous to B pharma? This tests whether the LF→pos1 self-succession pattern is dialect-specific or general.
**Description:** For A herbal_a (N=975 total lines): compute LF-class self-succession at pos1 for all LF classes with N_lf≥5 (d: ~137, ch: ~79, sh: ~77, o: ~77, y: ~124, qot: ~59, ok: ~45). Baseline: A herbal_a section-specific pos1 distribution. Compare each LF class self-succession E to B pharma results.
**Expected outcome:** A herbal_a ch-LF → ch at pos1 may be elevated (consistent with F158 showing A ch→ch within-line succession of 28.4%). If A herbal_a has ch self-succession at pos1 similarly to B pharma, this suggests ch self-succession is a cross-dialectal grammar feature — not pharma-specific. If A herbal_a lacks it, the pharma finding is dialect+section specific.
**Cost estimate:** small (one script, A herbal_a section, N=975)
**Prerequisites:** none

## H_new_AR: RESOLVED (exp_478). F449 ASSIGNED. ANSWERED (selective, not general): B pharma ch-LF→ch at pos1 CONFIRMED (E=1.64×/N=15). sh-LF→sh(dir,3.99×/N=6), t-LF→t(dir,8.22×/N=3). NOT general: l/ok/o/qok/d no self-succession. B herbal ch-LF→ch DEPLETED (0/47). Additional(dir): d-LF→l(4.21×/N=4), ok-LF→t(2.24×/N=4).

## H_new_AP: RESOLVED (exp_475). ANSWERED (primarily negative): A herbal_a LF→LL matrix shows NO confirmed routing rules (E≥1.5×/N≥10). d→ch(1.39×/N=35), qot→d(1.44×/N=24) — below threshold. Directional: y→o(2.10×/N=9), sh→sh(2.13×/N=6), s→ok(2.42×/N=5), ot→qok(3.17×/N=4). A herbal_a LL operates at word level (body-conditional), not LF-class routing. No finding ID.
**Source:** exp_471: A herbal_a d-LF→ch at LL(E=1.39×/N=35); qot-LF→d at LL(E=1.44×/N=24). These form a complementary pair: d opens→ch closes; qot opens→d closes. Do the other major A herbal_a LF classes (y=14.8%, ch=9.4%, sh=9.1%, o=9.1%) show complementary or structured LL routing?
**Description:** For all major A herbal_a LF classes (d, y, ch, sh, o, qot, ok, ot): compute LL routing with A herbal_a section-specific baseline. Create a LF→LL routing matrix. Test: is there a global complementary structure (each LF class has a different dominant LL class, forming a circular routing pattern)? Compare to B herbal LL routing.
**Expected outcome:** y-LF may route to d/ch at LL (consistent with A formula y→sh→ch at F406); ch-LF may route to d or sh. If a full routing matrix exists with complementary pairs, it would extend the section grammar taxonomy significantly for A.
**Priority:** medium (follows from exp_471 complementary pair; requires one focused experiment)

## H_new_AQ: RESOLVED (exp_474). ANSWERED (insufficient N): ok body-conditional N=6-7 per class, all directional. l→pos1 concentrated in edy+other-body (not aiin-body). NEW(dir): B pharma qok+edy→ch at pos1(E=2.64×/N=6) — pharma-specific deviation from F451 qok+edy→qok-self. Both ok+other and qok+other → l at pos1(~2.7-3.0×/N=5). No finding ID.
**Source:** exp_473: B pharma ok-LF top words are okeey(12)/okaiin(7)/okain(5)/okeedy(5) — edy+aiin class dominated. B qok has a body-conditional bifurcation (F451: qok+edy→qok-self 1.52×, qok+aiin→sh 1.73×). Does ok have a similar within-pharma body-conditional routing rule?
**Description:** For B pharma ok-LF lines: separate okeey/okeedy (edy-body) from okaiin/okain (aiin-body). Compute pos1 routing for each body class. Expected: ok+edy may route to ok-self or l at pos1; ok+aiin may route to sh or qok at pos1. Compare magnitudes to F451 (qok bifurcation).
**Expected outcome:** If ok+edy → ok-self and ok+aiin → sh/qok: this generalizes the body-conditional bifurcation from qok to ok. Consistent with F439 (body-conditional rules are general for template onset classes). N for ok+edy (~19) and ok+aiin (~12) may be sufficient for directional results.
**Priority:** medium (extends F451/F439 body-conditional framework to ok class; pharma-specific)

## H_new_AO: RESOLVED (exp_473). ANSWERED: B pharma ok-LF(N=44): l→pos1(2.37×/N=8,dir) + ok→pos2(2.01×/N=7,dir). ok is pharma-concentrated (B herbal N=3). ok-LF vocabulary: okeey/okaiin/okain/okeedy dominated. l at pos1 connects to F423 pharma l-chain. y→o at pos2(2.02×/N=8) confirms F430 pharma y-formula. No finding ID.
**Source:** F447 (exp_467): B pharma ok-LF elevated (E=1.47×/N=44) + o-LF elevated (E=1.53×/N=36). Neither has within-line routing characterized. With N=44, B pharma ok-LF should yield above-threshold routing results.
**Description:** For B pharma ok-LF lines (N~44): compute pos1/pos2/LL routing with B pharma section-specific baselines. Also compute B pharma o-LF routing. Compare to B pharma formula types (F430: y→o→ch is pharma-specific; F426 formula types). Does B pharma ok-LF activate the ok-class formula routings from F426 (d→qok→ol, qok→ch→ol, qok→ch→qo)?
**Expected outcome:** B pharma ok-LF may route through l or ch at pos1 (consistent with l-chain pharma concentration, F423). If ok→l→ch is a pharma-specific formula, it would extend the pharma section grammar. o-LF routing may involve or/ol at pos1.
**Priority:** high (N=44 adequate; completes F447 routing characterization; pharma l-chain connection)

## H_new_AN: RESOLVED (exp_477). ANSWERED (negative/insufficient N): A/B t-LF pos1 inversion not confirmed. A herbal_a(N=28): o-class(broad) at pos1 E=2.12×/N=5(dir), NOT specifically ot/ol. B sections: herbal(N=4), cosmo(N=5), astro(N=3) — all below directional threshold. B pharma t-LF(N=10): t-self at pos1 E=7.99×/N=3(dir) — pharma t-chains, NOT qok. Prior exp_472 evidence (B herbal N=37) could not be reproduced (dialect classifier N discrepancy). NEW(dir): B pharma t-LF → t at pos1. No finding ID.
**Source:** exp_472: B herbal t-LF→qok at pos1(2.28×/N=6,dir). A cosmo t-LF→ot(3.36×/dir)+ol(2.99×/dir) at pos1. exp_471: A herbal_a t-LF→ol(4.51×/dir) at pos1. Pattern: A dialect routes t-LF → o-gallows class (ot/ol) at pos1; B dialect routes t-LF → template class (qok) at pos1.
**Description:** Verify this A/B t-LF pos1 inversion across both dialects and available sections. Compute t-LF pos1 routing for: A herbal_a (N=31, directional individually), A cosmo (N=28), B herbal (N=37). Is ot/ol elevated at pos1 in A but not B? Is qok elevated at pos1 in B but not A?
**Expected outcome:** If the inversion is real: A t-LF→ot/ol at pos1 (E≥2× in A sections, E<1× in B); B t-LF→qok at pos1 (E≥2× in B herbal, E<1× in A). This would be a new A/B grammar discrimination finding at the LF-formula level, parallel to the pos1 distribution inversions in F408 (B qok→qok at pos1 vs A qok→ch at pos1).
**Priority:** medium (verifiable from existing experiment data; would extend A/B discrimination taxonomy)

## H_new_AM: RESOLVED (exp_472). ANSWERED (all directional): B herbal t-LF(N=37): qok→pos1(2.28×/N=6,dir), o→pos2(2.69×/N=5,dir), o→LL(2.02×/N=5,dir). B cosmo t-LF(N=16): qok→pos2(2.01×/N=5,dir). A cosmo t-LF: ot/ol→pos1(dir). B herbal y-LF: y→pos1(2.89×/N=5,dir), ot→LL(2.83×/N=6,dir). No finding ID (all directional).
**Source:** exp_468 corrected the exp_467 t→ch baseline error and found t→qok at pos1 E=2.22×(N=6,dir). But exp_468 was a correction experiment; a full formula analysis of B herbal t-LF lines (N=38 lines, 37 with ≥2 words) was not done with proper methodology. exp_468 showed pos1 routing (qok=2.22×,N=6; ch=0.80×) and LL routing (o=1.97×,N=5; ol=1.94×,N=4), but only directionally.
**Description:** For B herbal t-LF lines (N=38): compute complete pos1/pos2/LL routing with section-specific B herbal baselines for each position. Compare with B herbal y-LF (N=55) and d-LF. Also compute B cosmo t-LF (N=16) pos1/LL routing — does B cosmo t-LF have the same or different routing from B herbal t-LF? Cross-dialectal: compare A herbal_a baseline vs B herbal for each position.
**Expected outcome:** t→qok at pos1 may be confirmed above directional threshold with full analysis. B cosmo t-LF may show similar routing (t is elevated in both B herbal and B cosmo, and in A cosmo). If t-LF pos1 routing is shared between B herbal and B cosmo, this suggests a cross-section t-formula rule.
**Priority:** high (completes the t-LF grammar characterization; B cosmo t-LF is new)

## H_new_AL: RESOLVED (exp_471). ANSWERED: A herbal_a qot-LF (N=59) does NOT parallel B astro qot-LF. No pos1 routing above threshold (ch=1.10× baseline). NEW(dir): cth at pos2 E=2.32×(N=8) — consistent with F406 within-line formula qot→ch→cth at LF→pos1→pos2. d dominant at LL(E=1.44×/N=24). A herbal_a LF-class complementary pair: d-LF→ch at LL(1.39×/N=35); qot-LF→d at LL(1.44×/N=24). No finding ID (all directional).

## H_new_AJ: RESOLVED (exp_469). CONFIRMED (directional): B astro q-bench triplet has 3 distinct within-line grammar modes. qok-LF(N=149): ok→pos1(2.00×/N=11), l→LL(1.32×/N=24). qot-LF(N=29): ch→pos1(1.56×/N=7), ot→LL(3.12×/N=4,dir)+ot→pos2(2.82×/N=3,dir) — qot/ot spatial pair parallels A F378. qo-LF(N=34): ol→pos1(2.18×/N=7,dir), ch→LL(1.68×/N=7). d-LF→qot at pos2(1.99×/N=9). Co-occurrence analysis had key-ordering bug; qok+qot=114/657 reliable. No formal finding ID (all directional). The three onset classes are independently elevated (different routing profiles), not formula co-occurrence.

## H_new_AI: RESOLVED (exp_470). ANSWERED (section-composition artifact): A cth→qot CL E=1.76×/N=9 overall, but within herbal_a E=1.48×/N=9 (below threshold). cth-class is 83% herbal_a; herbal_a has elevated qot-LF base rate (7.0% vs 4.9% A-overall). The apparent elevation is inherited from section concentration, not a selective coupling. All 9 cases in 9 distinct herbal_a folios (f4r–f56r). No body-class driver. Exp_465's N=7 was slightly smaller (cph/ckh not included in cth-class). F445 NOT updated. No finding ID.

## H_new_AG: RESOLVED → F447 (exp_467). CONFIRMED: B herbal t-LF(2.34×/N=38)+y-LF(1.52×/N=55). B astro q-bench triplet: qok(1.78×)+qot(1.94×/N=29,NEW)+qo(1.60×/N=34,NEW). B pharma: ok-LF(1.47×)+o-LF(1.53×). B cosmo: t-LF(2.23×/N=16)+qot=0. Cross-dialectal: both A+B cosmo have t-LF elevated and qot~0. l-LF NOT a pharma LF marker (E=0.82×).

**Source:** F431 (exp_429) characterizes B astro qok-LF elevation. exp_466 characterizes A stars t-LF and A herbal_a qot/ch elevation. The full B herbal/pharma/cosmo/bio LF-class grammar has not been analyzed systematically (only astro was formally characterized).
**Description:** Run a B-dialect section LF grammar analysis parallel to exp_466 for A: compute section-specific E for all onset LF classes across herbal/astro/pharma/cosmo/bio sections. Key questions: Does B herbal have an elevated LF marker (parallel to A herbal_a's qot-LF 1.43×)? Does B pharma have a distinctive LF onset (l-LF has been noted in F423 as pharma-concentrated — does l appear at LF in pharma at elevated rate)? Does B cosmo show any LF-class elevation?
**Expected outcome:** B astro re-confirmed: qok-LF ~1.78×. B pharma: l-LF elevated (from F423's l-chain pharma concentration). B herbal: possibly ch-LF or d-LF elevated (paralleling A herbal_a's qot/ch LF grammar). If pharma l-LF is elevated at LF-class level, this complements the F423 cross-line finding (pharma qok→s CL, F444) and the within-line l-chain pharma concentration.
**Priority:** high (completes section LF grammar picture; symmetric to exp_466; may find B pharma l-LF analog of B astro qok-LF)

## H_new_AF: RESOLVED → F446 (exp_466). CONFIRMED: A stars t-LF E=2.12×(N=15) vs A-overall. herbal_a t-LF depleted (0.63×). Stars qot=0.16×/ot=0.19× massively depleted. B astro qok-LF elevated (F431 confirmed 1.78×); B astro t-LF depleted (0.70×). Full A/B inversion: A stars={t↑, qok↓}; B astro={qok↑, t↓}. Both "astronomical" sections use section-specific LF onset marker, different classes.

**Source:** exp_465: A stars (f57-72) has t-LF 12.0% vs herbal_a 3.7% (ratio=3.3×). qot depleted 9×, ot depleted 7×, ch depleted 2.6×.
**Description:** Compute A stars section LF-class E values using section-specific base rates (E = stars_rate / A_overall_rate, not just herbal_a rate). Cross-check with all A sections (cosmo, herbal_a, herbal_b). Compute what t-onset words are dominant at A stars LF. Compare to B astro qok-LF (F431: 19.6% vs 5.6%). Test: are A stars t-LF lines formula-typed (is there a t→pos2 routing rule)?
**Expected outcome:** A stars t-LF elevated vs full A baseline (not just herbal_a). Dominant t-words: 'taiin', 'tar', 'tor'. t-LF A stars is analogous to B astro qok-LF (F431) — a section-specific LF grammar marker, different onset class. If confirmed: F446 assigned.
**Priority:** high (strong signal 3.3×; parallels F431; would establish A/B section-grammar asymmetry at LF-class level)

## H_new_AD: RESOLVED (exp_465). ANSWERED: A stars zeros = LF grammar difference, NOT corpus size. Stars paragraphs average 13.0 lines (herbal_a=11.0). Stars has t-LF elevated 3.3×(12.0% vs 3.7%), qot depleted 9×, ot depleted 7×. Cross-line couplings tested in exp_464 involved onset classes rare in stars (ch=4%↓, qot=0.8%↓). Stars grammar uses {t,d,y,s} as dominant LF classes — completely different LF grammar from herbal_a.

## H_new_AC: RESOLVED (exp_465). CONFIRMED: cth→sh CL herbal_a-concentrated (9/12 cases, E=1.5×/N=9). Cosmo directional (N=3, 4.0×). Stars=0. Body driver: cth+o-body(E=2.31×/N=6), cth+e-body(3.60×/N=2,dir). cthy* words: baseline (1.03×). NEW: cth→qot CL E=2.07×(N=7) — cth at LL has two elevated cross-line targets: sh and qot.

## H_new_AB: RESOLVED → F445 (exp_464). CONFIRMED: A CL grammar section-specific. herbal_a: s→qot(3.2×/N=5), s→s(3.0×/N=4), sh→d(1.9×/N=8), ch→ch(1.5×/N=22), ok→y(1.7×/N=11). Cosmo: ch→ch(2.2×/N=6), ok→y(1.8×/N=5) shared with herbal_a. Stars(N=86): ALL couplings zero — no elevated cross-line coupling in A "astronomical" section. A less section-differentiated than B. NEW: cth→sh CL E=1.9×(N=12).

## H634: RESOLVED → F414 (exp_410). ANSWERED: B bracket grammar exists but differs from A. B s qok-bracket(E=2.78×/N=6); B t sh-bracket(E=3.33×/N=4,dir); B d sh-bracket ABSENT(E=1.24×, vs A=3.78×); B y y-bracket ABSENT(vs A=5.21×). A uses sh as line-framing onset (d/p/t sh-bracket); B does not — B uses qok as B-specific framing class (s→qok bracket). B p ch-correlation(E=3.38×,N=4,dir): among rare ch events in p-lines. The A/B bracket taxonomy: four confirmed differences.

## H635: RESOLVED (exp_414). DESCRIPTIVE: B s qok-bracket (N=6): f75r/12, f75r/14, f75r/15, f82r/9, f107v/9, f111r/7. MID onset distribution (N=20): ch=6(30%), sh=3(15%), qok=2(10%). ch-DOMINATED MID. All 6 lines have s→qok at pos1 (direct, NOT via sh). f107v/9 has qok-chain: s→qok→qok→qok→qok (4 consecutive qok words). 3/6 lines from f75r (bio section). B s qok-bracket = bio-section concentrated, ch-rich MID.

## H633: RESOLVED (exp_414). DESCRIPTIVE: A d sh-bracket (N=4): f1r/9(len=4), f27r/2(len=5), f58r/15(len=6), f93r/21(len=4). MID onset distribution (N=7): d=4(57%), other=1, qo=1, ch=1. d-DOMINATED MID — the d sh-bracket lines have d-onset words filling the MID. Pattern: d[LF]→sh[pos1]→[d-dominated MID]→sh[LL]. Short lines (4-6 words). Differs from A p sh-bracket (diverse MID).

## H641: RESOLVED → F423 (exp_420). ANSWERED: B l-LF is a pharma-section content class (N=63, 2.7%). l→ch→qok formula confirmed (qok=2.96×/N=5). l pos1→pos2 self-succession E=3.03× (strongest position pair). l-dense lines concentrated in pharma (3.5%) vs herbal (0.3%), bio (0.0%). All len=3-4 l-chains in f111-116 (pharma). Dominated by 'lk-' compound vocabulary.

## H644: RESOLVED → F423 (exp_420). ANSWERED: l self-succession concentrated at pos1→pos2 (E=3.03×) and pharma section (3.5% l-dense vs 0.3-1.2% elsewhere). All long l-chains (len=3-4) in pharma folios f111-116. 'lk-' compounds drive l clustering.

## H642: RESOLVED → F424 (exp_421). ANSWERED: d→qok→ol confirmed (E=2.51×/N=6). d→ch→y RETRACTED: N=3 only in standard analysis (F421 N=5 was spurious). NEW: d→ch→l=2.16×(N=12) — strongest d→ch pos2 enrichment; connects to pharma-section l-clustering (F423).

## H643: RESOLVED → F425 (exp_422). ANSWERED: y→o→ch=2.58×(N=6) confirmed. SECTION-DIFFERENTIATED: y→o→ch=pharma+bio(0 herbal); y→sh→ch=herbal+pharma. 'or' dominates y→o pos1(N=5/13). Both paths route to ch at pos2; herbal uses sh-path, pharma+bio uses o-path.

## H645: RESOLVED (exp_423). ANSWERED (negative): d→ch→l NOT pharma-specific (pharma 58% vs baseline 51%, E≈1.1×). Astro section high (33%). Pharma l-clustering is from l-LF/lk-compounds in runs (F423), not d→ch→l routing. No finding ID assigned (null result).

## H646: RESOLVED → F426 (exp_424). ANSWERED: 10 confirmed formula types at N≥5, E≥2.0. Formula-typed=2.6%(59/2265). CORRECTIONS: d→ch→l BELOW threshold(E=1.57×); p→sh→qot BORDERLINE(E=1.78×). s→sh→qok confirmed non-formula(E=1.26×/N=21). Full inventory: qok→sh→k/d→ot→ot/l→ch→qok/d→qok→ol/y→sh→ch/y→o→ch/qok→ch→qo/d→ch→y/qok→ch→ol/p→sh→ok.

## H650: RESOLVED → F430 (exp_428). CONFIRMED (directional): 3 section clusters. Astro: qok-LF formula types(E=1.7-2.5×). Herbal: d→ch→y(5.0×)/y→sh→ch(3.1×)/p→sh→ok(2.8×). Pharma+bio: y→o→ch(herbal=0×). d-LF and y-LF split between sections (same LF class, different routing). All N=4-8 directional.

## H651: RESOLVED → F431 (exp_429). ANSWERED: qok-LF rate=1.91× in astro(19.6% vs 5.6-5.9% elsewhere). All 20 astro folios contribute uniformly. pos1 routing near-uniform. Astro formula-type concentration (F430) = elevated qok-LF RATE, not section-specific routing. Astro section systematically selects qok-class LF words.

## H651: RESOLVED (duplicate) — see RESOLVED entry above (→ F431, exp_429).

## H650: RESOLVED (duplicate) — see RESOLVED entry above (→ F430, exp_428).

## H648: RESOLVED → F432 (exp_430). ANSWERED (directional): A-dialect p-LF→opch E=14.58×(N=3) — raw rate 2.31% ≈ B 2.70%. Pattern consistent with cross-dialectal p-formula self-referential structure but A N=3 is directional only. B confirmed (5.38×/N=40). A background lower (0.16% vs B 0.50%) inflates A E-value.

## H647: RESOLVED → F429 (exp_427). REFUTED (k/t), inconclusive (f). p→opch E=5.28× does NOT generalize. k-LF: okch=1.03×(N=1); t-LF: otch=1.34×(N=10, below threshold); f-LF: N=9 too small. p-LF self-referential structure (p at LF + opch MID embedding) is specific to the p-formula class — third distinguishing p-feature confirmed.

## H640: RESOLVED → F427 (exp_425). CONFIRMED: 'opch'-compounds enriched 5.28×(N=39) in B p-LF MID vs non-p-LF baseline(0.51%). o-onset MID=1.98×; ch MID=0.60×(depleted). p-gallows self-referential structure: p at LF + 'opch' (p-embedded compound) at MID. Vocabulary dominated by opchedy(13)/opchdy(7)/opchey(5) in p-LF MID. First within-word onset mirroring of the LF class confirmed in formula lines.

## H639: RESOLVED → F422 (exp_419). ANSWERED: B ot E_self=2.19×(N=145) — elevated, 2nd highest B onset. ot run-length distribution GEOMETRIC (not super-geometric). B has 23 ot-len=3 runs, 1 len=4. NEW: B l onset is MOST self-successive (E=2.35×/N=102). B s=0.33×(anti-self, consistent with formula LF routing through sh). A/B: ot B=2.19× > A=1.67×; s A=1.42× > B=0.33×.

## H632: RESOLVED → F420 (exp_417). ANSWERED: B p→o enrichment = DISTRIBUTED category preference (not closed vocabulary). pos1: 17 word types for N=21 (top: 'or'=4, 'oraiin'=2, 15 hapaxes). LL: 23 types for N=25 (top: 'opam'=2, 'opchdy'=2). MID dominated by 'op-' compounds ('opchedy'=10, 'opchdy'=6). pos2 after p→o at pos1 NEAR-MARKOVIAN (no E≥2.0 at N≥3). NEW OBSERVATION: p-gallows appears within o-onset MID words as 'op-' compounds.

## H631: RESOLVED → F415 (exp_411). ANSWERED (NEGATIVE): Formula-typed fraction (E_cond≥2.0, N≥3) is NOT a useful discrimination metric. Shuffled VMS B=10.9% > real VMS B=8.6% (CATCH 1 FLAG). Latin Caesar=10.8%, Dante=11.3%, both exceed VMS B. Under first-letter onset (comparable grain): VMS B=4.2%/A=5.1% BELOW natural language 10.8-11.3%. Metric biased by bigram strength: strong VMS bigrams inflate denominator, reducing formula-typed fraction vs shuffled/natural language. F405 9.3% narrowed: not evidence of distinctive grammar. Individual formula types (p→sh→qot, y→sh→ch, etc.) are unaffected — they remain well-replicated large-N findings.

## H637: RESOLVED → F416 (exp_412). ANSWERED: N≥5 restores genuine signal. VMS B=2.6% > shuffle=2.2% > Latin=1.9% at N≥5. N≥10: VMS B=0%, shuffle=0%, Latin=0% (Dante=2.2% due to 6.5× larger corpus). Genuine formula types survive N≥5: y→sh→ch=2.53×(N=8)/qok→sh→k=3.90×(N=5)/d→ot→ot=3.69×(N=5). Revised F405: formula-typed = 2.6% at N≥5 (not 9.3% at N≥3).

## H636: RESOLVED → F421 (exp_418). ANSWERED (partial): VMS B has MORE formula types than Latin at same corpus size (10 vs 4, N≥5, E≥2.0). Structural form (LF-conditional pos2 enrichment) identical across corpora. VMS types template-class dominated (qok/sh/ch/ot at pos1); Latin/Italian likely syntactic word-order patterns. NEW directional formula types: l→ch→qok(2.72×/N=5)/d→qok→ol(2.61×/N=6)/y→o→ch(2.45×/N=6)/d→ch→y(2.23×/N=5). p→sh→qot borderline absent from current list (E≈2.0, confirmed in exp_392).

## H630: RESOLVED → F418 (exp_415). ANSWERED: A cth at pos1 (N=75, 5.2%) is NOT a formula class. LF broadly distributed: d=1.61×(N=21)/qot=1.65×(N=6)/y=1.04×(baseline)/s=0.21×(DEPLETED)/qok=0.41×(DEPLETED). pos2 after cth-pos1 near-Markovian: qo=2.32×(N=5,highest)/ot=1.90×(N=4); NO E_cond≥2.0 at N≥3. cth is formula DESTINATION (F406: o→sh→cth=4.33×/qot→ch→cth=2.60×) but NOT formula SOURCE. A/B asymmetry: A=75 vs B=2 (37:1). High A cth-pos1 prevalence reflects A's broad distribution of cth across positions (body-class word), not a grammar rule.

## H629: RESOLVED → F408 (exp_404). ANSWERED: Four LF-class dominant pos1 inversions: s(A→ch/B→sh), sh(A→ch/B→qok), ok(A→ch/B→qok), ot(A→ch/B→qok). A ch-elevation broadly distributed; B qok-elevation from template-class LFs (ok/ot/qot→qok). B p→qok=0.00×(N=0/39) in A. Source: B has s→sh/sh→qok/ok→qok/ot→qok formula routings that A lacks.

## H629_archived: RESOLVED → F408 (answered in exp_404). "A ch elevation broadly distributed" confirmed — four dominant LF-class pos1 inversions identified (s/sh/ok/ot all A→ch but B→sh/qok). Not retested; F408 covers the question fully.

## H628: RESOLVED → F407 (exp_403). ANSWERED: Formula effects decay by pos3 (not detectable given N=4-8 per formula trigram). Robust unconditional pos2→pos3: sh→qo=2.16×(N=17)/qot→ot=2.25×(N=15)/l→l=2.16×(N=13)/y→y=3.41×(N=5). Onset gradient: sh 17%→10.8%→10.1%↓; qok 12.5%→16.9%→16.1%↑; ot 3.8%→5.9%→6.6%↑. Grammar: formula overlay (LF→pos2) + local bigram chain from pos3 onward.

## H627: RESOLVED → F406 (exp_402). ANSWERED: A formula-typed=7.6%(N=103/1360, vs B=9.3%). A pos1=ch=28.6%(vs B=19.0%); A pos1=qok=4.6%(vs B=12.3%). A formula types: sh→ch→sh=2.69×(N=8)/t→ch→sh=3.27×(N=5)/o→sh→cth=4.33×(N=4)/qok→ch→qok=3.10×(N=5). y→sh→ch NOT in A formula list (A/B inversion confirmed). B formula types y→sh→ch/p→sh→qot/qok→sh→k/s→sh→l all absent in A.

## H626: RESOLVED → F419 (exp_416). ANSWERED (directional): d-LF pos1=ot BASELINE (E=0.97×/N=13). Given d→ot pos1, pos2=ot E=6.34×(N=5) — ot self-stickiness, NOT d-specific routing. pos3 after d→ot→ot: N=5, all directional, diverse. f113v/5 extreme: 10 ot-class words in 14-word line. ch depleted after d→ot (E=0.47×). d→ot→ot is a conditional ot self-chain rule.

## H625: RESOLVED (exp_414). DESCRIPTIVE: A p sh-bracket (N=4, updated from 3): f1v/5, f3r/11, f42r/16, f102r1/3. MID diverse (N=14 tokens): other=2/t=2/ot=2/sh=2/d=1/ch=1/s=1/ol=1 — no dominant class. sh appears within MID in 2 bracket lines (f3r/11: pos2=sh; f42r/16: sh at both pos2 and within MID). Consistent with A pan-positional sh. MID not formula-constrained — brackets frame diverse content.

## H624: RESOLVED → F413 (exp_409). CONFIRMED (directional): A bracket grammar is GENERAL. Same-onset brackets: y-bracket(E=5.21×/N=3), d sh-bracket(E=3.78×/N=4), k ch-bracket(E=3.04×/N=4), p sh-bracket(E=2.06×/N=4, F404). sh-bracket shared by d AND p. Cross-class: d→other→other=4.67×/y→o→ok=5.38×(dir). A qot LL=d dominant(50%,1.91×) but no pos1 correlation. A bracket grammar = general LINE-LEVEL SYMMETRY RULE: pos1/LL onset correlation across multiple LF classes. Strongest A/B distinction: B p anti-bracket(0.44×) vs A p bracket(2.06×).

## H623: RESOLVED → F417 (exp_413). ANSWERED: B p-formula pos3 grammar. ch-avoidance extends to pos3(0.75×/N=32) — pan-positional (pos1/pos3/MID/LL all depleted). qo enriched at pos3(1.86×/N=14). pos2=sh→pos3=qo=2.55×(N=6) — OVERRIDES unconditional sh→qok bigram. p→sh→qot→pos3 near-Markovian(N=8, dir). Formula effects at pos2 only for specific path; ch-avoidance and o-class enrichment are global.

## H619: RESOLVED → F401 (exp_397). CONFIRMED: A y grammar structurally inverts B. A y→y→y=2.15×(extends) vs B y→y→y≈0(terminates). A y→sh→ok=2.47× vs B y→sh→ch=2.94×. A y→ch near-Markovian; B y→ch→ok=1.87×. A y→d→ok=4.31×(dir). B y→l=1.49×(N=20,NEW). A y="self-chain+template-routing"; B y="response-routing+truncated-chain".

## H622: RESOLVED → F404 (exp_400). PARTIAL SUPPORT: A p sh-bracket enrichment=1.80×(N=3/40 vs 1.67 expected). A p→sh at pos1=1.66×(N=10/41); A p→sh at LL=3.52×(N=7/41). B p-lines ANTI-bracket=0.44×. Three actual A bracket lines: f1/5/f3/11/f42/16. A p grammar: p[LF]→sh[pos1]→[MID]→sh[LL]. B p grammar: sh-opened, s/qo/k/o-closed.

## H621: RESOLVED (working_position.md §13.3-13.9 synthesis). Five A/B inversions confirmed: (1)y→sh→pos2 inversion(B→ch/A→ok); (2)p-formula LL routing(A sh-bracket/B anti-bracket); (3)y-chain extension(A extends/B terminates); (4)pos1 class inversion(A ch=28.2%/B=19.0%; A qok=4.6%/B=12.3%); (5)A sh↔ch interleaving formula(absent B). Additional: B formula inventory 10 types vs A different types; B section grammar (astro-qok/pharma-l/herbal-d,y,p formula split); B p self-referential opch embedding. working_position.md updated through exp_429.

## H620: RESOLVED → F409 (exp_405). ANSWERED: p-lines longer (8.6 vs 7.8 words). Global ch-avoidance: pos1=0.42×/MID=0.69×/LL=0.47×. NEW: p→o at pos1=2.24×(N=21). MID: o=1.73×/qo=1.50×/qot=1.52×/ch=0.69×. LL: o=1.73×(TOP)/qot=1.53×/r=1.41×/ch=0.47×. Global o/qo enrichment throughout. p-formula = p[LF]→sh/o[pos1]→[o/qo/qot-rich MID]→[o/qot/r LL].

## H618: RESOLVED → F405 (exp_401). ANSWERED: 90.7% of B cont lines are near-Markovian at LF-conditional pos2 level; 9.3%(N=211) formula-typed (E_cond≥2.0). Top trigrams: d→sh→qok(N=24, E=1.12×)/s→sh→qok(N=21, E=1.28×) NEAR-MARKOVIAN. All 5 prior formula types confirmed. NEW: d→ot→ot=4.13×(N=5); qok→ch→qo=2.62×(N=8); l→ch→qok=2.96×(N=5). KEY: LF primarily controls pos2 conditioning (not pos1 choice); p→sh at LF→pos1 is only 1.32×.

## H617: RESOLVED → F403 (exp_399). CONFIRMED: LF class has direct LF→LL associations. B p→ch LL=0.47×(N=15/222) strongest depletion; p-formula lines are ch-avoidant throughout. B sh→sh/qo LL enriched; B t/ot→self LL; A p→sh LL=3.60×; A qot→d LL=1.79×(N=32). Cross-dialectal: p avoids ch at LL in both dialects.

## H616: RESOLVED → F400 (exp_396). ANSWERED: A sh-pos1 grammar INVERTS B at key points. A y→sh→ch=0.62×(depleted) vs B=2.94×(enriched) — OPPOSITE. A sh-pos1 baseline: sh dominant(17.1%) vs B qok dominant(27.1%). A y→sh→ok=2.47×(NEW). A sh→sh→sh=1.72×(3-position self-chain). A k→sh→qok=2.71×. B five-type taxonomy does not map to A.

## H615: RESOLVED → F411 (exp_407). ANSWERED (dir, N=9): B f→sh DEPLETED(0.66×). f is WEAK-FORMULA gallows class. B f→k=8.90×(N=2, dir). Gallows taxonomy confirmed: STRONG-FORMULA {p(sh=1.37×)} vs WEAK {f(sh=0.66×depleted), t(F399), k(F397)}.

## H614: RESOLVED → F410 (exp_406). CONFIRMED (directional): y-chains section-specific. bio_stars=5.71/100y(N=2/35 dir) vs herbal=0.60/100y(N=2/334); pharma/cosmo=0.00. bio_stars 10× higher rate; bio_stars y%=10.1%(highest). All chains in f19(herbal)/f44(herbal)/f67r2(bio). Section-grammar property.

## H613: RESOLVED → F412 (exp_408). ANSWERED: B t=LF-DOMINANT/NON-FORMULA (LF=3.90×, MID=0.64×, LL=0.62×, pos1=0.58×). B t LF→pos1 near-Markovian(N=208). NEW: B t MID→ot=1.95×(N=22); pre_LL→ot=2.12×(N=9)/t-self=5.03×(N=4,dir). A t: LF=2.63×(weaker/broader), pos1→ot=2.82×(N=9)/ch=0.66×(depleted,confirmed F399). A/B contrast: A t pos3/LL near-baseline vs B depleted. Gallows taxonomy confirmed: STRONG-FORMULA {p(LF=6.98×,pos1=0.18×)} → WEAK {f(dir)} → NON-FORMULA/LF-ONLY {t(LF=3.90×,pos1-Markov)} → FOLIO-LEVEL {k}.

## H613b: RESOLVED → F428 (exp_426). ANSWERED: B t→ot MID adjacency E=2.15×(N=24) = DISTRIBUTED class-level sequential rule. 18 unique t-words / 15 unique ot-words; no dominant pair. 17% same-body rate (4/24) mild body-templating only. NOT compound construction. F412 1.95×/N=22 confirmed as onset-class coupling rule.

## H612: RESOLVED → F402 (exp_398). ANSWERED (directional, N=6): B raiin-pos1 lines → pos2=ch=4.67×(N=4/5). Canonical: LF(template) → raiin → ch → qok → [qok-MID] → LL. r at LL=9.46×(N=2/6, dir). raiin bridges template LF class and ch/qok body.

## H611: RESOLVED → F398 (exp_394). ANSWERED: Five B sh-pos1 grammar types: content-formula(y→sh→ch=2.94×); gallows-formula(p→sh→qot=2.11×); template-class(qok→sh→k=4.08×/NEW); formula-terminal(s→sh→l=2.06×/NEW); near-Markovian(d/t). s→sh→qot=0.00× (extends F393 s→sh→d=0.00× to dual depletion). B ch-pos1: p→ch→ot=5.28×(NEW); y→ch→ok=1.87×; qok→ch→qo=2.59×.

## H610: RESOLVED → F399 (exp_395). See H609.

## H609: RESOLVED → F399 (exp_395). ANSWERED: B t→pos1 is NEAR-BASELINE (ch=0.96×/sh=1.02×) — t is NOT a third gallows formula type. F364 {k,t}→ch is MID-specific and does not extend to LF→pos1. B t trigram grammar near-Markovian throughout (mildly distributed effects, no dominant path). A t: ch depleted(0.66×)/ot elevated(2.77×)/ol elevated(2.20×). A t→ch→sh=3.28×(N=5). Gallows LF taxonomy: STRONG-FORMULA {p(5.90×), f(1.69×)} vs WEAK/ABSENT-FORMULA {t(1.02×), k(folio-level)}.

## H604: RESOLVED → F392 (exp_388). ANSWERED: INVARIANT_LF+ {p(3.53/5.85), t(2.43/3.58), f(2.69/1.67), s(2.22/4.73), y(2.28/3.52)}; INVARIANT_LF- {ch(0.39/0.25), ol(0.64/0.58), r(0.27/0.30)}; A>B INVERSION only: qot(A=1.65×/B=0.51×); B>A CONTRAST: cth(0.13/1.16) and d(1.15/2.29); template classes more LF-depleted in B; k NOT LF-enriched unlike p/t/f.

## H608: RESOLVED → F395 (exp_391). CONFIRMED: A y chains are super-geometric. Length-4=2(exp.0.12, ~17×); length-3=4(exp.1.8, 2.2×). B has ZERO length-4 chains; only 2 length-3 chains. A has 3 LF-starting length-3 y-runs vs B=0. Specific A length-4 runs: [f19/13] "ytor ytar ytchor ytaiin" and [f67r2/72] "ypair ykoaiin ydoly ytalchos".

## H607: RESOLVED → F396 (exp_392). ANSWERED: B p→sh→qot=2.11×(N=8/51) — gallows-formula routing; p→sh→ch≈0(0.18×/N=1) confirmed; p→sh→qok=0.58×(depleted). Two B sh-pos1 grammar types: content-formula (y→sh→ch=2.94×) vs gallows-formula (p→sh→qot=2.11×). Cross-LF pos2=ch rate after sh: p=0.18× to y=2.94× (16× span). p→sh LL distribution diffuse (no dominant terminal class).

## H606: RESOLVED → F397 (exp_393). ANSWERED: k is a FOLIO-LEVEL formula class, not a LINE-LEVEL formula class. k LF-enriched in opener lines (A=4.32×/B=3.88×) but position-general in cont lines (A=0.79×/B=0.66×). p/t remain LF-enriched in BOTH line types. k shows 5.5-5.9× LF drop from opener to cont vs p/t only 1.2-1.7×. B cont k = MID-dominant (54%). Resolves F392 k anomaly.

## H603: RESOLVED → F393 (exp_389). ANSWERED: Grammar NOT strictly bigram-Markovian. Key findings: B p→sh→ch≈0(0.18×/N=1/51) strongest effect; B y→sh→ch=2.94×(N=8); A y→y→y=2.15×(N=3 dir) — y chain extends 3+ in A; B y→y→y=0 (terminates at pos1 in B); B (s,sh)→d=0.00×; most common paths (d,sh/d,ch/s,sh N≥60) near-bigram-Markovian. LF-conditioning confined to specific depletion/enrichment exceptions.

## H602: RESOLVED → F394 (exp_390). ANSWERED: raiin=40%(N=6/15) dominates B pos1 r; qok(3.19×/N=5)/qot(3.22×/N=1)/y(2.32×/N=4)/ol(2.16×/N=1) produce r at pos1; ch/sh/ok/ot/k=0 categorical. B pos1 r vocabulary ≠ B LL r vocabulary (LL: ram/ry/ror dominant; pos1: raiin dominant). raiin position-polymorphic. qok-word → raiin → ch/qok continuation is the canonical B pos1-r formula.

## H601: RESOLVED → F391 (exp_387). PARTIALLY REFUTED: A r is NOT LL-exclusive. LL=2.95×(10/21=48%), MID_inner=1.09×=BASELINE(8/21=38%), pos1=0 categorical in cont lines, LF=0.27×. A r is bimodal: LL-enriched via ch→r rule + scattered MID hapax words. 21 tokens/17 types/81% hapax; raiin=19% only (no dominant LL r word). A r is grammatically marginal but not LL-exclusive.

## H600: RESOLVED → F390 (exp_386). ANSWERED with partial falsification: LF-formula classes do NOT strongly route to ch/sh at pos1. A dialect: d/s/y→ch/sh all near-baseline (0.76-1.22×). A pos1 r=0 categorical (r never at pos1 in A). B d→sh=1.40×/s→sh=1.42× (mild); B y AVOIDS sh (0.57×), routes to y(2.13×)/r(2.30×). Template self-routing: qot→qot(A=3.0×/B=2.0×)/qok→qok(A=2.17×/B=1.27×). B template classes at LF → r at pos1 (qot/qok→r E=3.2×). ch/sh dominance at pos1 is their own positional property, not driven by LF-formula routing.

## H599: RESOLVED → F389 (exp_385). ANSWERED: Complete pre_LL→LL routing matrices. A: d→d(N=69/E=1.38×)/ok→ok(E=2.52×)/ot→ot(E=2.04×)/cth→ot(E=2.33×)/ch→r(E=2.18×)/ol→ok(E=2.78×). B: sh→qok(E=2.73×)/d→d(E=2.10×)/s→ol(E=2.98×)/y→y(E=6.18×)/qot→r(E=2.27×)/r→sh(E=2.19×, NEW). A sh pre_LL: no single dominant route in LL-conditional framing.

## H598: RESOLVED → F388 (exp_384). ANSWERED: cth A-DOMINANT (A=4.0%; B=0.3% — 13× more in A). A cth LF=0.13× (most LF-depleted of all characterized classes); "mid-to-end" class (no strong non-LF concentration). A cth→ot pre_LL=3.03× (new A LL routing). A cth→r=0.00× (categorical). B cth→d=0.00×. Vocabulary: A cthy(25%)/cthol(13.5%)/cthor(9.4%); B cthedy/cthey/cthdy.

## H597: RESOLVED → F387 (exp_383). ANSWERED: y is a LF-FORMULA CLASS (A LF=2.28×/pos1=0.51×; B LF=3.52×/pos1=0.66×). B LF-formula ranking: s(4.73×) > y(3.52×) > d(2.29×). y LL-DEPLETED (A=0.61×, B=0.64×) unlike d. y self-succession strongest of all characterized classes (A=2.06×/MID=3.15×; B=2.71×/pre_LL=6.37×[N=5]). A y→r=0.00× (categorical). y→d pre_LL (A=2.12×/B=2.44×). B y→ot LF=0.32× depleted. Vocabulary: gallows-compound, A=kaiin/taiin/keey, B=keey/teedy/keedy.

## H596: RESOLVED → F386 (exp_382). ANSWERED: s is a PURE LF-FORMULA CLASS — B s LF=4.73× (strongest LF-enrichment of any characterized class); A s LF=2.22×; pos1/MID depleted in both dialects. B s→sh LF=2.47× (confirms F376); B s→ol pan-positional (LF=1.58×/MID=1.65×/pre_LL=4.47×); B s→cth=0.00× (categorical); B s→d LF=0.29× (LF-formula avoidance); B self-succession suppressed (MID/pre_LL=0.00×); B s pre_LL → ol LL=2.98×; saiin/ain/ar body dominant.

## H595: RESOLVED → F385 (exp_381). ANSWERED: d LF-ENRICHED/LL-ENRICHED/pos1-DEPLETED cross-dialectally (A: LF=1.15×/LL=1.68×/pos1=0.58×; B: LF=2.29×/LL=1.37×/pos1=0.46×) — OPPOSITE to ch/sh. B d LF=2.29× strongest LF-enrichment of any characterized class. Self-succession pre_LL-concentrated (A=2.40×/B=3.63×). A d→cth pan-positional (E=1.61×). B d→sh LF=2.44× (strongest B d outgoing). B d pre_LL → d LL E=2.10× (new B LL routing). A d→r=0.38×. A daiin-dominant (31.1%); B more distributed (daiin=21.5%/ar=11.5%).

## H594: RESOLVED → F384 (exp_380). ANSWERED: sh pos1-ENRICHED/LL-DEPLETED cross-dialectally (A: pos1=1.64×/LL=0.52×; B: pos1=1.84×/LL=0.45×). Both ch and sh are "second-position response classes." A sh pan-positional self-succession (LF=1.64×/MID=1.49×); B sh LF-chain only (1.48×). A sh→qok MID=1.90× (MID-specific); B sh pre_LL → qok LL=2.73× (new); cross-dialect sh→s pre_LL (A=3.58×/B=3.12×). B sh→ch=0.57× depletion.

## H593: RESOLVED → F383 (exp_379). ANSWERED: ch LF-DEPLETED/pos1-ENRICHED cross-dialectally (A: LF=0.39×/pos1=1.43×; B: LF=0.25×/pos1=1.23×). B ch self-succession flat (0.94× all positions). A ch self-succession LF=1.61×/MID=1.29×/pre_LL=0.86×. A ch→d pre_LL=1.95×; A ch→r pre_LL=6.39× (directional). B ch→d pre_LL=2.01×; B ch→qok MID=1.21×; B ch→sh=0.60×. B ch pre_LL → ol depleted (0.63×). A=ol/or body; B=edy body.

## H592: RESOLVED → F382 (exp_378). ANSWERED: r LL-enriched cross-dialectally (A: LL=2.95×; B: LL=2.48×). A r grammar-marginal (21 tokens, 88% hapax, self-succ=0.00×). B raiin dominant (18.4%). B r MID-self-succession (1.96×, LF-flat). B pre_LL→r: qot=2.27×/qok=1.31×; ok/ot/sh depleted. B r→ch MID=1.65×; B r→s=0.00×. B r pre_LL → d(2.01×)/ol(1.93×). B LL 3-tier hierarchy established.

## H591: RESOLVED → F381 (exp_377). ANSWERED: ol LL-enriched cross-dialectally (A: LL=1.43×, LF=0.64×; B: LL=1.59×, LF=0.58×). B ol=8.4% of LL positions. Bare 'ol' dominates vocabulary (A=32.6%, B=27.7%). A ol self-succession pan-positional (LF=2.88×/MID=1.59×/pre_LL=2.32× — all elevated, unique). B ol self-succession LL-concentrated (pre_LL=2.55×, LF-flat=1.02×). B ol→ch LF→pos1=1.98×; B ol→d LF→pos1=0.00×. A ol→ok bi-positional (LF=2.49×/pre_LL=2.51×). B ol→r pre_LL=2.41× (extends B pre_LL→r rule). B predecessors of ol at LL: s=2.98×, qok=1.25×, ok=1.33×; ch=0.63× depleted.

## H590: RESOLVED → F380 (exp_376). ANSWERED: qok MID-enriched, LL-DEPLETED (A: MID=1.34×, LL=0.53× — strongest LL depletion of all template classes; B: MID=1.16×, LL=0.59×). A four-class spatial grammar confirmed: qot(LF)/qok+ok(MID)/ot(LL). A qok→d pre_LL=2.31× (generalizes {qot,qok,ok,ot}→daiin pre_LL). A qok→ok MID=1.73× (bidirectional MID coupling). A qok→sh pre_LL=0.00×. B qok→r pre_LL=3.01× (generalizes B {qot,qok}→r). B qok→ch/sh LF+MID elevated (1.21-1.44×). B qok highly concentrated (top3=34.9%).

## H589: RESOLVED → F379 (exp_375). ANSWERED: No qok/ok spatial pair. ok is MID-enriched. A ok→qok MID=1.68×; B {ok,ot} pre_LL→ol/d rule; A ok→ot depleted (0.62×) — separate succession chains.

## H589_archived: ok-Onset Full Characterization — Does ok Form a qok/ok Spatial Pair Analogous to qot/ot?
**Priority:** high
**Status:** RESOLVED → F539/F540 (exp_536, 2026-04-11). ANSWERED NEGATIVE: No qok/ok spatial pair. Full template hierarchy: qot=CONF opener (E=1.79×)>qok=near-CONF (E=1.47×)>ot=neutral (E=1.29×)>ok=neutral (E=1.10×) at pos1. The pattern is a qo-prefix gradient, not a discrete pair. B ok pos1 DEPL (E=0.49×); B qok near-baseline (E=0.88×). ok vocabulary DIVERGES from ot/qot (aiin-dominated, not ch-dominated). B ok-LF pos1=t CONF (F540, NEW).
**Source:** F378 (A qot/ot = mirror-image spatial pair: qot=LF cluster, ot=LL cluster); F363 (ok→ok A=1.93×, B=1.32×, A LL-biased); F326/F366 (A qok↔ok bidirectional coupling 2.03/1.68×). If ok parallels ot (LL-enriched) and qok parallels qot (LF-enriched), qok/ok would form a second spatial pair in A-dialect.
**Description:** Same as exp_374 but for ok-onset: vocabulary, positional distribution, self-succession positional, outgoing bigram rules.
**Expected outcome:** If pattern holds: ok is LL-enriched (like ot) and qok is LF-enriched (like qot) in A-dialect. B-dialect: both ok and qok are MID-enriched. ok→ol pre_LL terminal (parallel to ot→ol). Self-succession peaks at pre_LL→LL in A (like ot). qok/ok body-parallel templating.
**Cost estimate:** small — reuse exp_374 script with TARGET='ok', ONSET_LEN=2

## H588: RESOLVED → F378 (exp_374). ANSWERED: ot MID/LL-enriched (B LF=0.33×); A ot/qot MIRROR-IMAGE spatial pair; A self-succession pre_LL=2.65× vs qot pre_LL=0.00×; B ot closed ot/qot clusters; cross-dialect ot→ol pre_LL terminal (A=2.40×, B=1.68×); ot/qot share body vocabulary.

## H588_archived: ot-Onset Full Characterization — Vocabulary, Positional Grammar, Bigram Rules
**Priority:** high
**Status:** RESOLVED → F536/F537/F538 (exp_535, 2026-04-11). ANSWERED: A ot NEUTRAL at pos1 (E=1.29×/obs=53, sub-CONF — NOT a line opener unlike A qot); B ot STRONGLY DEPLETED at pos1 (E=0.34×/obs=42, stronger than B qot E=0.60×). ot→ot CONF cross-dialectal (A: E=1.79×/obs=11; B: E=2.12×/obs=124). A ot→qo dir (E=2.24×/obs=7). ot→ch DEPLETED within-line both dialects (vs qot→ch BASELINE). ot/qot vocabulary parallel: same A=ch-mediated/B=edy-dominated architecture.
**Source:** F369: ot self-succession cross-dialectally stable (A=1.94×, B=1.93×) — the most consistent self-succession finding. exp_373: B qot→ot MID E=1.72× (body-parallel templating). ot is a template class like qot with ZeroMid≥66% (sparse midfix), but has no prior positional characterization.
**Description:** For both dialects: (1) ot word inventory (top-20); (2) positional distribution; (3) ot→ot self-succession positional decomposition; (4) ot outgoing bigram rules (ot→d, ot→ch, ot→qot, etc.); (5) ot body structure; (6) full ot successor distribution.
**Expected outcome:** ot is likely a MID/LF class (template classes tend to be MID-dominant). ot→ot cross-dialectally stable suggests class-level memory rule. ot body may be 'eedy'-suffix heavy in B (like qot) and ch-compound in A (like qot).
**Cost estimate:** small — direct reuse of exp_373 script with onset='ot'

## H587: RESOLVED → F377 (exp_373). ANSWERED: A qot LF-enriched (E=1.65×), B qot LF-depleted (E=0.51×, MID/pre_LL enriched) — complete positional inversion. A self-succession: LF→pos1 E=3.34×, MID E=3.00×, pre_LL→LL ABSENT (0/36). A qot→y MID E=2.86×, A qot→qok MID E=2.29×, A qot→daiin pre_LL E=2.28×. B qot→r pre_LL E=5.18×, B qot→d pre_LL E=2.53×, B qot→ot MID E=1.72×. Cross-dialect: LF→ch at pos1 E=1.77×/1.72×. Vocabulary: A=qotchy dominant, B=qotedy/qoteedy.

## H587_archived: qot-Onset Full Characterization — Vocabulary, Position Grammar, and Bigram Rules
**Priority:** high
**Status:** RESOLVED → F533/F534/F535 (exp_534, 2026-04-11). ANSWERED: A herbal_a qot pos1 CONF (E=1.79×/obs=59, LINE OPENER); A qotchy dominant (20.7%); A qot→qot CONF (2.74×/obs=12); A qot-LF self-opens dir (E=3.17×/obs=7). B qot pos1 DEPL (E=0.60×, MID class); B qotedy+qoteedy dominant (22.2%); B qot→ot CONF (1.58×/obs=52), qot→qot CONF (1.93×/obs=33), qot→r CONF (1.78×/obs=12). KEY: qot→ch is INTER-LINE only (F490/F491) — within-line qot→ch is baseline (A: E=1.06×; B: E=1.20×).
**Source:** F369 (A qot self-succession E=2.60×, highest of all template classes); F368 (A qot LF-enriched); F366 (A qot→daiin pre_LL E=2.52×); exp_367 matrix (A qot→y E=1.75×, N=17; B qot→r E=2.00×, N=20; B qot→qot E=2.06×). qot is the only template class without a comprehensive characterization (vocabulary, position profile, bigram rules).
**Description:** For both dialects: (1) qot word inventory (top-20 qot words by frequency); (2) positional distribution (LF/MID/LL enrichment); (3) qot→qot self-succession positional decomposition; (4) qot→daiin (A, E=2.52×) and qot→y (A, E=1.75×) positional characterization; (5) qot→r (B, E=2.00×) positional characterization; (6) qot body structure (midfix distribution — qot is a sparse-midfix class per F288/Phase 6, ZeroMid≥66%).
**Expected outcome:** qot is a line-opening cluster class (LF-enriched, self-succession=2.60×) that transitions to daiin or y at line-end (pre_LL→LL). qot vocabulary likely has ~30-50 word types with a few dominant forms (qotar, qotol, qoteey, qotchy) similar to ok/ot classes.
**Cost estimate:** medium — multi-component characterization

## H586: RESOLVED → F376 (exp_372). CONFIRMED: A sh→qot position-general (LF→pos1=1.83×, MID=1.58×, pre_LL=1.70×, all=1.63×, N=29). sh-class-general, no dominant pairs. Also: A sh→t position-general pre_LL peak (E=2.56×, N=30); B s→sh LF-position-specific (LF→pos1=2.47×, N=62; MID near-baseline; pre_LL depleted); B s→ol pre_LL-concentrated (E=4.46×, N=6); 'she-' body sh = TRIPLE HUB.

## H585: RESOLVED → F376 (exp_372). CONFIRMED: B s→sh LF-POSITION-SPECIFIC (LF→pos1=2.47×, N=62/260; MID=1.15×; pre_LL=0.43× depleted). 83% of hits at LF→pos1. sh successors = 'she-' body sh words. s-class-general (all s-words 15-33% sh rate). B s→ol pre_LL-concentrated (E=4.46×).

## H578: RESOLVED → F367 (exp_365). ANSWERED: A-dialect {aiin→ol} shift = qok-onset primary driver (herbal=0.85→pharma=6.60); qokaiin near-disappears (8.04%→0.98%); ok also shifts (0.65→2.38); ch/sh already ol-biased in herbal (barely shift); d non-shifting confirmed; mechanism = aiin-word DROPOUT.

## H570: RESOLVED → F363 (exp_361). ANSWERED: ok→ok is class-level memory (84-86% DIFFERENT ok words). A cont E=1.93×, B E=1.32×. No dominant word-pair. A LL-biased (15.5%). B okedy/okar sub-words elevated.

## H570: RESOLVED (exp_433). ANSWERED: ok→ok=CLASS-LEVEL MEMORY (84-87% different words; 26-30 unique types; no dominant pair >N=5). Mild word-level clustering: 13-16% same-word rate; okaiin has 38% self-succession in B (N=5). E=1.86×(A)/1.36×(B), consistent F363. Confirms F363 class-level mechanism.

## H569: RESOLVED → F361 (exp_359). REFUTED: y→d in continuation lines A=0.96×, B=1.08×; F326 value is likely cross-register artifact. B y→daiin weakly elevated (N=9). ch-onset dominant predecessor of daiin at LL in A (34.5%).

## H571: RESOLVED → F362 (exp_360). CONFIRMED: ch→daiin E=1.30×/1.45× cross-dialect; strongest pre-LL→LL (A 1.69×, B 2.02×); chol→daiin dominant A pair; chedy→daiin dominant B; A qot pre-daiin E=2.50×.

## H571: RESOLVED → F362 (exp_360, confirmed exp_432). [DUPLICATE ENTRY REMOVED]

## H569: RESOLVED (duplicate) — see line 254 (→ F361, exp_359). exp_441 confirms: within-line y→d=0.93-0.96× (near baseline). daiin=44% of y→d at LF→pos1. A y→d rank=#2 (13.2%); B rank=#7 (5.1%).

## H568: RESOLVED → F364 (exp_362). CONFIRMED: A-dialect split persists at MID_inner (pf ch/sh=0.50, kt=2.35). B-dialect collapses (all ch-biased at MID). A k is sh-biased at LF→pos1 due to gallows→sh E=1.72× overwhelming k's ch-bias.

## H568: RESOLVED (duplicate) — see RESOLVED entry at line 268 (→ F364, exp_362). Open entry here refers to a slightly different framing (MID_inner specifically) but F364 answers it directly.

## H567: RESOLVED → F360 (exp_358). A-dialect gallows→sh multi-position (E=1.42-1.72×); B-dialect LF→pos1 specific only (E=1.22→0.78× reversal at pos1→pos2). A pre-LL anti-sh (E=0.28×). {p,f}→sh vs {k,t}→ch internal split.

## H565: RESOLVED → F365 (exp_363). ANSWERED: no folio-opener two-word formula — all LF+pos1 pairs unique (N=1). Grammar is purely onset-class level. A pos1=sh-dominant (shey/shor/sheol). B opener LF=p-dominant (34%). A closer ycheor(3) only repeated LF word.

## H565: RESOLVED (duplicate) — see RESOLVED entry at line 280 (→ F365, exp_363).

## H563: RESOLVED by F358 (exp_356) — B folio-closer pos1 sh depleted (E=0.49×); folio-opener t=0% at pos1 in both dialects; B also excludes p and k at folio-opener pos1. Both H563 entries answered by F358. [DUPLICATES CLEANED UP]

## H562: RESOLVED → F357 (exp_355). ANSWERED: A folio-closer ch elevation at pos1 is GENERAL (not y-specific). ALL LF onset types show elevated ch at pos1: y-LF→ch=36.8%, d-LF→ch=43.8%, s-LF→ch=45.5%, o-LF→ch=60%, k-LF→ch=67%. Anti-sh at pos1: E=0.16× (double-position anti-sh). General folio-closer rule, not y→ch bigram-specific.

## H561: RESOLVED → F356 (exp_354). ANSWERED: B folio-closer LL sh words (shckhdy, shckhar, shdy, shckhy) are all 100% hapax (no formula word). Folio-closer LL placement of sh+ckhy compounds is a grammar exception to their MID-restriction in continuation — short folio-closing lines (4-5 words) use MID-class vocabulary at LL. No specific sh+ckhy formula word identified.

## H541: RESOLVED → F433 (exp_431). CONFIRMED: A daiin=LL-enriched(1.30×/N=87)/LF-baseline(1.03×). A/B INVERSION: B daiin=LF-enriched(2.62×)/LL-depleted(0.70×). A d-onset LL=1.64×(consistent F385).

## H546: RESOLVED → F433 (exp_431). ANSWERED: B daiin LF NOT uniform across sections. Pharma=3.57×(N=45)/bio=3.22×/herbal=2.00×/astro=1.60×(weakest). Pharma+bio drive global B daiin LF enrichment. Astro distinct: daiin LL=1.00×(baseline, not depleted) — astro qok-LF dominance suppresses daiin LF.

## H522: RESOLVED → F372 (exp_370). ANSWERED + Q004 CLOSED: sh→qok = 'she-' body sh subclass → qok-class uniform successor. shedy/shey/sheedy drive B-dialect; qok distribution after sh is baseline-proportional. Architecture: body-conditional rule (sh+e-body → elevated qok successor).

## H522_archived: RESOLVED (exp_450). High-N confirmation of F372: she-body sh-words E=1.78-3.21× vs non-she-body at baseline. A-dialect fully class-level (97.7% unique pairs); B-dialect 62.4% unique (frequency-driven concentration). qok successor distributed across types (class-level). [ARCHIVED ENTRY CLEANED UP]

## H498: RESOLVED → F434 (exp_434). ANSWERED: A-qok ch-midfix forms (qokchy=8.2%/qokchol=3.0%/qokchor=1.7%) = 13% of A qok tokens vs B=2.4% (5.4× rate difference). B dominated by edy-class zero-midfix forms (qokeedy/ain/eey/edy/aiin = 57.5%). A qok-ol terminal = 19.3% vs B=1.7%. Structural vocabulary divergence (not morphological rule): A has 3 moderately-frequent ch-midfix types; B concentrates in zero-midfix edy-class. A zero-midfix=49.4% vs B=83.4%.

## H_new_A: RESOLVED → directional/inconclusive (exp_442). E=1.41× (13.8% vs 9.8%) but N=4 bracket tokens — too small to confirm. Dominant bracket type is ch→ch (70 lines), not F413's specific d→sh/y→y types. No new finding ID.

## H_new_B: RESOLVED (duplicate) — see resolved entry below (exp_437). Answered by F436.

---

## H497: RESOLVED (exp_437). ANSWERED (negative): Suffix entropy NOT correlated with hapax rate (Spearman=0.071(A)/0.242(B), no significance). A: SufH/type-token rho=0.554 (moderate). B: SufH/type-token rho=-0.035. H_new_B: B-qok edy fraction=40.4% unremarkable (sh=45.8% higher). Structural split: template onsets (sh/qok/ch) prefer edy 36-46%; content onsets (d/s) anti-edy (4-5%). F436 added.

## H_new_B: RESOLVED (exp_437). ANSWERED: B-qok edy fraction=40.4% not unusual. sh=45.8% highest; d=4.3% lowest. Template/content onset split in suffix preference confirmed. See F436.

---

## H496: RESOLVED (exp_440). ANSWERED (descriptive): 60-67% of MID tokens are identical to LF words (word reuse dominates MID). 57-58% of LL tokens are same-onset-diff-word (LL grammar selects within onset class). Diff-onset words = 0.1% (trivially zero — all onsets appear at all positions). daiin is primary cross-position bridge. No new finding ID.

---

## H495: RESOLVED → F435 (exp_435). ANSWERED: Hapaxes structurally abnormal. Hapax midfix 6-8× longer than frequent (A: 2.73 vs 0.43; B: 2.79 vs 0.36). Hapax mean word len 1.4-1.8 chars longer. Hapax 'no-suffix' = 20-22% vs freq = 9-11%. Hapax onset distribution more uniform (higher entropy). NOT consistent with single productive morphological system — requires separate pathways or bimodal register.

## H_new_C: RESOLVED (exp_439). ANSWERED (opposite): B astro has FEWEST hapaxes (E=0.70×, 9.4% vs global 13.5%). Herbal/bio/pharma all E=1.14-1.22×. Astro repetitive (qok-formula), not vocabulary-diverse. F435 structural anomaly is general.

## H_new_D: RESOLVED (exp_439). ANSWERED (null): No-suffix hapaxes NOT concentrated in 'other'-onset. A: other-onset=21.0% vs recog-onset=19.5% (same). B: other=11.7% vs recog=17.1% (recog HIGHER). Not transcription noise. Genuine morphological property.

## H_new_E: RESOLVED (exp_436). ANSWERED: Latin hapax/freq ratio=1.79×, Italian=1.92× — LARGER than VMS (A=1.42×, B=1.33×). Hapax-longer gradient is universal in natural language and STRONGER than VMS. F435 word-length claim revised: not VMS-distinctive. Midfix-layer claim (6-8×) is VMS-specific (no direct NL equivalent). No new finding ID.

---

## H494: RESOLVED → diagnostic (exp_443). ANSWERED: Suffix is dominant length component (A=43%/B=48% of word length). 50-60% of words have zero-midfix — midfix CANNOT cause overproduction (more midfix in sim would shorten words). 22% excess likely from suffix overselection (too many 4-char suffixes: aiin/eedy/chol = 20% of A words). A VMS: onset=1.76+midfix=1.12+suffix=2.14=5.02. B: onset=1.89+midfix=0.88+suffix=2.61=5.38. No new finding ID.

---

## H_new_F: RESOLVED → directional (exp_444). B cross-line y→d E=1.54×(N=11) confirms F326's B y→d=1.49× as cross-line effect. A cross-line y→d E=0.61×(N=4) inconclusive — F326's A y→d=1.37× unexplained. daiin NOT specific driver. B sh(LL)→d(LF) E=1.58×(N=19): strongest confirmed cross-line coupling.

## H_new_G: RESOLVED → F438 (exp_445). ANSWERED: Cross-line grammar exists. Self-succession cross-line: s→s(A=2.57×/B=2.20×), ok→y(A=1.52×/B=1.64×), ch→ch(A=1.57×), y→y(B=1.62×). Inversion: within-depleted → cross-enriched (B sh→d: CL=1.58× vs pLL→LL=0.61×). B d→sh(1.79×), l→sh(1.63×), d→qok(1.56×). Cross-line grammar is structurally DIFFERENT from within-line (inversion pattern).

## H_new_H: RESOLVED (exp_446). ANSWERED: Suffix positional grammar WEAK. B 'dy' LF E=1.86×(N=60); A 'iin' LL E=2.23×(N=17). Suffix class effects E=0.82-1.52× (vs onset-level E=3-7×). Suffix selection primarily by onset class (F436), not position. No new finding ID.

## H_new_I: RESOLVED (exp_447). ANSWERED: ok→y CLASS-LEVEL — all 16 A and 21 B pairs are unique word combinations. A ok→y(22.5%) > A ot→y(10.9%) — A-specific ok enrichment. B ok≈ot (20-21%). No word-type specificity.

## H_new_J: RESOLVED (exp_447). ANSWERED: B qok→s section-specific (astro=52%/pharma=42%). Not a formula-cycle rule. Astro's high qok density explains majority. s-words at LF after qok-LL are common content words (saiin/sain/sar). qok-words at LL have uniform 20-40% s-conversion rate (class-level).

## H_new_K: REFUTED (exp_448). rho(within_E, CL_E)=0.000(A)/−0.042(B) — no systematic inversion. Within-depleted pairs mean CL=0.94-1.01× (same as non-depleted). Individual inversions (B sh→d/d→qok/ch→ol/ok→y) are real independent coupling rules, not instances of a general mechanism. Cross-line enrichment = LF/LL positional preferences, not inversion of within-line avoidance.

## H_new_L: RESOLVED → NEGATIVE (exp_449). A cth→sh cross-line (75% herbal) matches A-dialect 74% baseline herbal proportion — NOT section-specific. Class-level, diverse word pairs. No new finding.

## H492: RESOLVED → F437 (exp_438, exploratory). ANSWERED: y-onset requires midfix (8.9-12.9% zero-midfix vs 40-83% for other classes). B-qok skeleton class (83.4% zero-midfix). d+aiin=35%(A)/24%(B) most suffix-concentrated. Onset structural taxonomy: skeleton+aiin=d/qot(B); skeleton+edy=qok(B); complex+diverse=y. No control corpus comparison (exploratory).

---

## H_new_M: RESOLVED → F439 (exp_451). CONFIRMED: Body-conditional rules general. B qok aiin-body→sh (E=1.73×/N=94) + qok edy-body→qok (E=1.52×/N=165). Complete within-class inversion. ol/ok body splits also confirmed. A: e-body→qo rule. Two-level VMS grammar: onset class (primary) + suffix body (secondary). F439 added.

## H_new_M_was: Body-Conditional Succession Rules Beyond sh→qok
**Priority:** high — directly extends F372 (she-body→qok rule)
**Status:** archived (resolved above)
**Source:** exp_450 confirms F372: 'she-' body sh-words (first body char='e') have elevated qok succession E=1.78-3.21×; non-she-body (shol/shcthy/sho) at or below baseline. Is this a specific feature of sh→qok, or is body-class-conditional succession a general VMS grammatical principle?
**Description:** For each of the 6 most common onset classes (sh, ch, d, y, ol, ok) in B-dialect MID bigrams, group words by the first body character after the onset (the character immediately following the onset string). For each (onset_class, first_body_char) group with ≥20 tokens, compute the successor onset class distribution and compare to the baseline successor distribution from that onset class. Flag cases where E≥1.5× at N≥10 (e.g., d+e-body → elevated X succession?). Cross-validate in A-dialect.
**Expected outcome:** If she-body→qok is general: we expect to find other (onset, body_char) groups with specific successor onset preferences at E≥1.5×. If it's unique to sh→qok: other onset classes will not show body-conditional bifurcation. The she-body distinction (sh+e vs sh+o) is the only known body-conditional bigram rule.
**Cost estimate:** small — corpus bigram analysis, MID positions only

## H_new_N: RESOLVED → F440 (exp_452). CONFIRMED (dialectal): f≥20 words 100%/82.6% shared; hapaxes 20.8%/13.8%. l/r/p near-B-exclusive. B-specific vocab edy-dominated. All 64 high-freq A words appear in B. Dialectal variant pattern confirmed. F440 added.

## H_new_N_was: A/B Shared Word-Type Vocabulary Overlap
**Priority:** medium
**Status:** archived (resolved above)
**Source:** F434 (A-qok vs B-qok vocabulary divergence 5.4×). The global A/B word-type overlap has never been measured. Are A and B dialectal variants (substantial overlap), different phases (partial overlap), or near-independent systems?
**Description:** Extract all unique word types in A-dialect folios and B-dialect folios. Compute: (1) fraction of A word types that also appear in B; (2) fraction of B word types also in A; (3) by onset class — which onset classes show most/least cross-dialect word sharing?; (4) by frequency tier — are common words shared across dialects (core vocabulary) while hapaxes are dialect-specific?
**Expected outcome:** If dialectal variants: top-100 most frequent words substantially overlap (60%+). Hapaxes are dialect-specific. If distinct systems: even common words are largely non-overlapping (20-40% shared). Onset class analysis: skeleton classes (qok/qot with simple zero-midfix vocabulary) may overlap more than complex classes (y, cth).
**Cost estimate:** small — word type comparison, no bigram analysis needed

## H_new_O: RESOLVED (exp_453). B qok run-length GEOMETRIC (L≥3: E=1.04×). edy-body words dominate chains (E=1.50×; edy+edy consecutive=49.6% vs 18.5% expected). F439 mechanism confirmed in chain membership. A y super-geometric not confirmed (N=1 at L=4). No new finding ID.

## H_new_O_was: B qok Chain Run-Length Distribution
**Status:** archived (resolved above)
**Source:** F439: B qok+edy-body → qok self-succession E=1.52×/N=165. This body-conditional self-replication (edy-body qok words preferentially followed by more qok words) could produce super-geometric run-length distributions if edy-body qok words cluster in chains. F419 (exp_419) showed B ot and B l run-length distributions are geometric. A y is super-geometric (F410).
**Description:** For B-dialect continuation lines, extract all qok-onset word runs (consecutive qok-class words). Count run lengths (1, 2, 3, ...). Fit geometric distribution and compare to observed. If edy-body self-replication drives runaway chains, the observed distribution should have a heavier tail than geometric (super-geometric). Also: for qok runs of length ≥2, what fraction are edy-body consecutive pairs vs aiin-body?
**Expected outcome:** If edy-body self-replication → super-geometric: geometric would underpredict len≥3 qok chains. If the body-conditional rule is within-class modulation only: geometric distribution with E_self≈1.52× (no excess tail). Compare to A qok run-length as a cross-dialectal check.
**Cost estimate:** small — run-length analysis reusing exp_419 framework

## H_new_P: RESOLVED (exp_454). CONFIRMED (dir): A e-body→qo across 4-5 onset classes (sh/ch/ok/qok/cth, E=1.66-3.68×). qo+e-body→qo self-succession E=3.26×(N=4,dir). A qo=B qok functional analog: same positional profile (MID-enriched, LL-depleted), 35% stem overlap, parallel e-body rule. Cross-dialectal body-conditional grammar principle confirmed.

## H_new_P_was: A-dialect e-Body → qo Rule
**Status:** archived (resolved above)
**Source:** F439 (A): sh+'e'→qo (E=1.66×/N=13) and ch+'e'→qo (E=1.83×/N=10). In B, e-body → qok elevated. In A, e-body → qo elevated. Hypothesis: qo in A plays the same "successor to e-body words" role that qok plays in B. This would mean the A/B structural difference at this level is the qo→qok substitution (qo is A's "light" template class where B has qok).
**Description:** For A-dialect: (1) compute qo-onset successor distribution by predecessor body-char (is qo elevated after e-body words across ALL onset classes, not just sh and ch?); (2) compare qo self-succession in A vs qok self-succession in B (using the F439 body-conditional framework); (3) check whether A qo+e-body → qo self-succession (parallel to B qok+e-body → qok); (4) compute A qo vs B qok Jaccard index for vocabulary types.
**Expected outcome:** A qo-after-e-body rule generalizes beyond sh and ch. A qo may have a qo+e-body self-replication rule parallel to B qok+e-body. A/B vocabulary comparison: A qo types overlap substantially with B qok types (they're functional analogs).
**Cost estimate:** small — extend exp_451 framework for qo onset

## H_new_S: RESOLVED (exp_456). ANSWERED: d+a-body→sh cross-line (F441) is CLASS-LEVEL. B daiin→sh specifically (E=2.42×/N=18) but dar/dal/dain also route sh+qok+ch (different sub-profiles). B daiin: s DEPLETED (0.39×), qok near-baseline (0.87×) — B daiin is "pure sh bridge". A daiin: sh E=1.54×(N=63) + s E=1.75× — broader routing (sh+s). A/B cross-dialectal difference in daiin cross-line routing. F441 confirmed class-level. No new finding ID.

## H_new_T: RESOLVED (exp_457). ANSWERED (NEGATIVE for prediction 1): shedy at LL → d CL (E=1.54×/N=11), NOT qok. Within-line shedy→qok does NOT extend cross-line. shedy DRIVES the sh→d CL coupling (58% of sh→d pairs are shedy). NEW(dir): ch+edy at LL → qot CL E=2.23×(N=7). ok→y CL driven by both aiin(1.98×/N=13) and edy(1.58×/N=7). H_new_U partially confirmed. No new finding ID.

## H_new_T_was: B sh-onset Body-Conditional Cross-Line Routing
**Priority:** high — direct test of F441 mechanism for sh onset
**Status:** archived (resolved above)
**Source:** F438: B sh→d CL=1.58×(N=19). F439: shedy (she-body, e-body) → qok within-line (E≈1.96×). F441: d+aiin→sh cross-line. Prediction: the sh→d CL coupling is driven by bare-sh or aiin-body sh words (shain/shal/shaiin), while shedy at LL routes to qok (continuing within-line rule). If edy-body sh words at LL route to qok (cross-line), then the edy-body routing extends cross-line for sh (unlike qok+edy, which showed no cross-line self-replication).
**Description:** For B-dialect continuation lines: decompose sh-onset LL words by first body character ('e'=shedy/sheedy/shey, 'a'=shain/shaiin, 'o'=shol/shom, bare='_'). For each body group, compute cross-line routing enrichments (→d, →qok, →sh, →s). Key question: does shedy at LL → qok (E≥1.3×)? Does non-shedy sh at LL → d specifically (matching/exceeding F438 aggregate)? Expected outcome: PREDICTION 1 (edy-body extends cross-line): shedy at LL → qok E≥1.3×; bare/aiin sh at LL → d E≥2.0×. PREDICTION 2 (edy-body within-line only): shedy at LL → d same as aggregate; bare sh → d. NEGATIVE: both sub-groups route identically to the aggregate.
**Cost estimate:** small — extend exp_455 framework with sh onset focus

## H_new_U: PARTIALLY ANSWERED (exp_457). edy-body CL targets differ from within-line across sh/qok/ok: sh+edy within=qok, cross-line=d(1.54×); qok+edy within=qok-self, cross-line=d(weak,1.37×); ok+edy within=l(F439), cross-line=y(1.58×). edy-body within-line self-succession does NOT extend cross-line. aiin-body is the reliable cross-line bridge predictor (d+aiin, qok+aiin, s+aiin). NEW directional: ch+edy at LL → qot CL E=2.23×(N=7) — warrants follow-up. H_new_W added for ch+edy→qot confirmation.

## H_new_U_was: Cross-Line edy-Body vs aiin-Body Routing Asymmetry
**Priority:** medium
**Status:** archived (partially resolved above)

## H_new_W: RESOLVED → F442 (exp_458). CONFIRMED: B ch+edy CL → qot (E=2.36×/N=7); within-line B ch+edy FLAT (1.05×) — CL rule has no within-line precedent. A ch+edy CL → ch (E=2.96×/N=13; F441 strengthened). A/B inversion: same body class, opposite CL routing. B ch+aiin→d CL(1.88×/N=6); A ch+aiin→sh CL(3.73×/N=4,dir). F442 added.

## H_new_W_was: ch+edy Cross-Line → qot Confirmation and ch MID Body-Conditional
**Priority:** high
**Status:** archived (resolved above)
**Source:** exp_457: B ch+edy at LL → qot at next LF: E=2.23×(N=7). This is unexpected — no prior within-line rule predicts ch→qot. Does the ch+edy at LL specifically route to qot, or is this a sampling artifact?
**Description:** Verify B ch+edy CL → qot (E=2.23×/N=7). Also: test the within-line body-conditional bigrams for ch-onset — does chedy within-line show elevated qot succession (which would explain the CL finding as an extension of within-line)? Run ch-onset body-conditional within-line bigram analysis (parallel to exp_451 for ch). Key: ch+e-body within-line successor distribution vs ch+a-body within-line successor distribution.
**Expected outcome:** If ch+edy CL→qot is real: within-line chedy→qot may also be elevated (body-conditional chain extending cross-line). If within-line chedy→qot is NOT elevated: the cross-line coupling is a separate grammatical rule (ch+edy marks paragraph-level qot association without within-line precedent).
**Cost estimate:** small — extend exp_451 for ch onset + re-examine exp_455/457 CL data for ch+edy

## H_new_X: RESOLVED (exp_459). REFUTED (B qot→ch CL=0.85×): no ch↔qot alternating pair. B qot→qot CL=2.61×(dir). B ch is a cross-line pivot: received by d/qok/ok(E=1.52× each), routes to qot(F442). A qot→ch CL=1.74×(N=5, dir) — A but NOT B. A s→qot CL=2.77×(N=5, dir) — new. A ch→ch triple: E=0.40× (NEGATIVE). No new finding ID. H_new_Y added for A s→qot.

## H_new_X_was: B ch↔qot Cross-Line Alternation and qot Body-Conditional CL
**Priority:** high
**Status:** archived (resolved above)
**Source:** F442: B ch+edy at LL → qot CL (E=2.36×/N=7); B overall ch→qot CL E=1.65×. If ch-terminal lines predict qot-opening lines in B, then qot-terminal lines should predict ch-opening lines (alternating pair). Also: what body class of qot at LL drives the qot→ch CL coupling (if present)?
**Description:** For B-dialect: (1) compute qot at LL → next LF onset (is qot→ch CL elevated?); (2) qot-onset body-conditional cross-line (qot+e-body, qot+a-body at LL); (3) For A-dialect: does A ch→ch CL chain extend (does A have ch→ch→ch across 3 lines, consistent with F441+F442)? Test A ch at LF → next line ch at LL (is there a double-line ch association)?
**Expected outcome:** B qot→ch CL elevated (E≥1.3×): would establish ch↔qot as a B-specific cross-line complementary pair. qot+edy-body at LL might specifically drive →ch (parallel to ch+edy→qot). A ch→ch chain: unlikely to extend to 3 lines due to N constraints but worth checking.
**Cost estimate:** small — extend exp_457/458 framework for qot onset

## H_new_Y: RESOLVED → F443 (exp_460). CONFIRMED: A s→qot CL E=2.82×(N=6), 6 folios, 5 unique pairs — class-level. A s dual targets: {qot(2.82×), s(2.58×)}. B s dual targets: {s(2.15×), qok(1.48×)}. A/B s secondary CL inversion: A→qot, B→qok. s+aiin→A s-self E=3.64×(N=5). F443 added.

## H_new_Y_was: A-Dialect s→qot Cross-Line Coupling and A s Cross-Line Profile
**Priority:** high
**Status:** archived (resolved above)
**Source:** exp_459: A s at LL → qot at next LF: E=2.77×(N=5). Also A s→s CL=2.57×(N=?). A-dialect s onset generates both s-continuation and qot-opening cross-line (dual target). F438 has A s→s=2.57×/N=8 confirmed; the A s→qot is new and directional.
**Description:** For A-dialect: (1) Confirm A s→qot CL (E=2.77×/N=5) — extract all A s-LL → qot-LF cases, verify word diversity and folio distribution; (2) Compute A s-onset body-conditional CL breakdown (is s+aiin → qot, or a different body class?); (3) Compare A s→qot vs B s→qot CL (B s→qok CL=1.46×, but B s→qot?); (4) Does A s-LL → qot imply the next line often opens with a qot-formula (A qot→ch at LF)?
**Expected outcome:** If confirmed: A s is the most "routing-rich" onset cross-line (s→s + s→qot both elevated). Body-conditional: s+aiin likely drives qot-routing (parallel to B s+aiin→s). A/B comparison: B s routes to self-succession (F438, 2.20×); A s routes to BOTH self-succession and qot — A s cross-line is broader.
**Cost estimate:** small — focused A-dialect cross-line analysis

## H_new_V: RESOLVED (exp_461). ANSWERED: A ok→y CL is body-class-DISTRIBUTED (c-body 3.75×/N=5, edy 1.45×/N=3, aiin 1.41×/N=5 — all elevated). A d+aiin FLAT (N=160, E=0.7-1.2×) — B d+aiin→sh CL is B-specific. A sh+edy→qok CL(dir, 3.45×/N=4) vs B sh+edy→d: A/B sh+edy CL inversion. A d+y-body→y(1.59×/N=8)+ch(1.97×/N=6). edy-body CL routing is dialect-specific (different targets A vs B for every onset tested). No new finding ID.

## H_new_V_was: A-Dialect Cross-Line Body-Conditional Rules Beyond ch+edy
**Status:** archived (resolved above)

## H_new_R: RESOLVED → F441 (exp_455). CONFIRMED: Body-conditional CL rules extend F438. B d+aiin→sh(E=1.99×/N=14), qok+aiin→s(1.76×/N=17), s+aiin→s(2.60×/N=7). A ch+edy→ch(2.79×/N=13). Within-vs-cross routing differs: qok+a-body→sh within-line but →s cross-line. aiin-body=bridge words, edy-body=self-replication. F441 added.

## H_new_Z: RESOLVED (exp_462). CONFIRMED: B CL grammar section-specific. Astro: ch→qot CL (E=1.9×/N=6, 6/9 overall cases). Herbal: ok→y(2.1×/N=10)/d→sh(2.3×/N=5). Pharma: qok→s(1.7×/N=13). F442's ch→qot is primarily an ASTRO phenomenon. CL section taxonomy parallels F430 within-line section grammar. No new finding ID.

## H_new_Z_was: Section-Specificity of B Cross-Line Grammar (F442/F443)
**Priority:** medium
**Status:** archived (resolved above)
**Source:** F430 (exp_428): within-line formula types are section-specific (astro=qok-LF, herbal=d/y/p, pharma=l). F442: B ch+edy→qot CL (E=2.36×/N=7). F443: B s→qok CL (E=1.48×/N=6). Are these cross-line couplings section-specific? Given astro has elevated qok-LF (F431), the B s→qok CL might be astro-driven (s at LL in non-astro → random; s at LL in astro → qok because astro opens with qok). Similarly, B ch→qot CL might be concentrated in a specific section.
**Description:** For B-dialect: decompose cross-line couplings (ch→qot, s→qok, d→sh, d→qok, ok→y) by section (herbal/astro/pharma/bio). Compute section-specific E values for each coupling. Compare to within-line section grammar (F430).
**Expected outcome:** ch→qot CL concentrated in astro (where qot-LF is elevated per F431-area) or in herbal (where ch is common). s→qok CL concentrated in astro (qok-LF enriched). If cross-line grammar is section-specific, it extends F430's section-grammar model to the paragraph level.
**Cost estimate:** small — extend exp_445 framework with section tagging

## H_new_AA: RESOLVED (exp_463). NEGATIVE (corpus size): [d/qok/ok→ch→ch→qot] 3-line chain N=1 (exp=0.10) — directional only. Corpus has 1293 B 3-line triples, too small for 3-onset chain confirmation. NEW directional: ok→y CL → y→d CL (E=1.96×/N=5). No finding ID. Paragraph-level chains beyond 2-step require larger corpus.

## H_new_AA_was: Paragraph-Level Cross-Line Chain in B
**Status:** archived (resolved above)
**Source:** exp_459: B ch at LL → qot CL (F442: E=1.56×); B d/qok/ok → ch CL (E=1.52× each). If these are part of a paragraph-level sequence, then [d/qok/ok-terminal lines] should be followed by [ch-LF lines] which then become [ch-terminal lines] followed by [qot-LF lines]. The 2-step chain would appear as a 3-line pattern.
**Description:** For B-dialect: (1) identify 3-consecutive-line patterns where line1-LL=d/qok/ok, line2-LF=ch, line2-LL=ch, line3-LF=qot; (2) count observed vs expected (if independent); (3) compare to: line1-LL=d/qok/ok → line2-LF=sh → line2-LL=sh → line3-LF=qok (alternative path). Also test: line1-LL=s → line2-LF=qok → ... (B s→qok chain).
**Expected outcome:** If chain exists: observed B [d/qok/ok → ch → qot] 3-line pattern > expected from independence. If chains are independent: no excess. Expected N ~3-5 for any specific 3-onset chain given corpus size constraints.
**Cost estimate:** small-medium — 3-consecutive-line sequence counting

