# Hypothesis Backlog
# Cryptanalyst — Voynich Manuscript Investigation
# Format: see skills/generate_hypotheses.md for the entry template.
# Ordering within a priority tier is not significant; re-order as priorities shift.

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

## H020: f49v and f76r "Key-Like" Line-Marker System — Nature and Cross-Manuscript Scope
**Priority:** medium
**Status:** SUBSTANTIALLY RESOLVED by accumulated experiments (exp_012-014, 022, 026, 030): (a) image-based hand comparison still required; (b) sequences don't correspond to adjacent body text (exp_013, <5% match vs 6% chance); (c) f75v/f76r confirmed as third/second line-marker folio pair (exp_026). f49v's L0 positions 2-6 are later-hand numerals (exp_030), not original markers — "key-like" applies to the structural pattern, not a cipher key. Sub-question (a) requires manuscript image access and is blocked.
**Source:** exp_011_single_char_validation → exp_011_f66r_wordlist
**Description:** Two text-only folios (f49v: Scribe 1/Currier A/herbal; f76r: Scribe 2/Currier B/biological) have a "key-like" single-character L0 marker before body text lines. ZL3b transcribers already named f76r's sequence "key-like." Both scribes independently use this structure. Three sub-questions: (a) Are the marker characters in the same hand as the body text? (b) Do the marker sequences (f49v: f,o,r,y,e,k,s,p,...; f76r: s,d,q,s,o,l) correspond to anything — a cipher key, a cross-reference system, an abbreviated alphabet? (c) Are there other "text only" folios with similar marker systems not yet detected? The f76r chars (s,d,q,s,o,l) vs f49v chars (f,o,r,y,e,k,s,p,...) show some overlap (s, o) but are not identical.
**Expected outcome:** If the two sequences are related or decipherable, this is among the most structurally interesting finds in the project. If they're unrelated scribal quirks, they can be set aside.
**Cost estimate:** small — raw transcription inspection for other text-only folios; image comparison for handwriting
**Prerequisites:** H021 (L0 audit) — already partially run in exp_011
**Priority:** medium
**Status:** open
**Source:** exp_011_single_char_validation
**Description:** f49v has a perfectly alternating L0/P0 structure where every body text line is preceded by a single-character L0 marker (f, o, r, y, e, k, s, p, o, y, e, p, o, y, e, d, y, e, k, y). Some L0 slots contain @NNN; special characters (unrepresented glyphs). These are real manuscript features, not transcription artifacts. Three sub-questions: (a) Are the marker characters in the same scribal hand as the body text, or a different hand? (paleographic test per Davis 2020 — Scribe 1 writes f49v Currier A). (b) Does the marker sequence (f,o,r,y,e,k,s,p...) correspond to anything elsewhere in the manuscript — another folio's marker sequence, a body-text word, or a cipher key? (c) Do similar one-per-line marker systems exist on other folios that the L0 overloading issue caused us to miss?
**Expected outcome:** If markers are in the same hand as body text, they were written by the same scribe and are intentional annotations. If they're a different hand, they're a secondary annotation layer. If the sequence matches something elsewhere in the manuscript, it may be a cross-reference system.
**Cost estimate:** small — requires raw ZL3b inspection and image comparison
**Prerequisites:** H021 (L0 audit) should run first to identify all folios with line-marker L0 patterns

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

## H031: The f49v Numeral "1-5" Annotation Is by the Same Hand as Other Known Later Annotations (e.g., f116v)
**Priority:** low
**Status:** open
**Source:** exp_030_f49v_numerals
**Description:** The f49v numeral annotation (1-5 in the margin, later hand) is one of several non-Voynich additions to the manuscript. Known later annotations include: f116v "michitonese" text (post-15th century), zodiac month names (Romance language), "Jacobus ex libris" owner inscription, and Dee/Kelley marginalia theories. H031 asks whether the f49v numeral hand matches any of these known annotators.
**Expected outcome:** If the numerals match the f116v annotation hand (same ink, script style), this narrows the annotation date. If they match the zodiac month names, it suggests a single reader who studied the manuscript systematically.
**Cost estimate:** small — image comparison, prior work literature search
**Prerequisites:** exp_030 (done)

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
**Status:** open
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
**Status:** open
**Source:** F063 (exp_056): the 'other' onset class (25.6% of B tokens) is heterogeneous; KL=0.033 bits (very low). Disaggregating k-initial vs t-initial words (the two main stem classes identified in qo-stripping, exp_040) may reveal onset-specific suffix preferences invisible in the lumped 'other' category.
**Description:** exp_040 showed that qo-stems are dominated by 'k' (60.5%) and 't' (21.2%) initial stems. The free-word corpus contains many k-initial (keedy, kaiin, kal) and t-initial (taiin, tol, tcheey) words. If k-initial and t-initial words have the same suffix preferences, they're the same morphological class. If they differ (e.g., k-initial prefers -edy while t-initial prefers -aiin), they're distinct classes. This would extend the 3-slot template (exp_056) to include root-class specificity.
**Expected outcome:** If k and t are the same class: overlapping suffix distributions. If different: different suffix preferences that were averaged out in the 'other' category.
**Cost estimate:** small (extend exp_056 by disaggregating the 'other' onset category)
**Prerequisites:** exp_056 (done)

---

## H071: Multi-Paragraph Structure Is NOT Herbal-Specific — Bio and Pharma Folios Have Multiple Paragraphs
**Priority:** medium
**Status:** open
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
**Status:** open
**Source:** F064 (exp_057): B para-start words cluster around p/t-onset forms (pchedar, tchedy, pchedal) that are rare in the general B corpus (0.4-0.9%). These look morphologically distinctive with 'pc-' and 'tc-' onset clusters.
**Description:** In Currier B, the most common para-start opener words are pchedar (×3), tchedy (×3), pchedal (×2). These start with the consonant clusters 'pch' and 'tch' — which are unusual onset combinations not found in the main onset classes (qo-, o-, ch-, sh-, d-, y-). Test: (a) What is the full frequency of 'pch' and 'tch' onset words in the B corpus? (b) Do these words concentrate at para-starts and line-starts, or are they evenly distributed? (c) Are 'pch' and 'tch' words absent from labels? (d) Do they take a distinct suffix distribution (e.g., prefer -ar/-al over -edy/-aiin)?
**Expected outcome:** If they are a dedicated structural vocabulary: concentration at para-starts, distinctive suffix distribution, label absence. If random coincidence: evenly distributed, no suffix specialization.
**Cost estimate:** small
**Prerequisites:** exp_057 (done)

