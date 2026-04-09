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

## H078: Bio Section Has Multiple Paragraphs Per Folio Because Pool Folios Have Multiple "Scenes"
**Priority:** medium
**Status:** open
**Source:** F068 (exp_061): Bio multi-para folios are f83r (4 PS), f84v (4 PS), f75v (3 PS), f75r, f82r, f83v, f84r — mostly pool/bathing folios. Do multi-paragraph bio folios have more words/lines per paragraph (longer scenes) or more paragraphs (more scenes)?
**Description:** In the bio section, some folios have 1 paragraph (single-scene bio illustrations) and some have 2-4 paragraphs (pool folios with multiple bathing scenes). Test: (a) Do multi-paragraph bio folios have the same word-per-paragraph count as single-paragraph bio folios, or longer paragraphs? (b) Are the paragraph texts in multi-para bio folios independent vocabulary (each scene described separately) or do they repeat the same words? (c) Does the text within each bio-folio paragraph use the same vocabulary as other bio paragraphs on the same folio?
**Expected outcome:** If each paragraph = independent scene description: different vocabulary per paragraph on the same folio.
**Cost estimate:** small
**Prerequisites:** exp_061 (done)

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

## H101: The Line-Final Onset Distribution Is Preserved Within Paragraphs vs Paragraph-Final Lines
**Priority:** medium
**Status:** open
**Source:** F081 (exp_074): B last-word onsets are non-random (o=1.25×, d=1.50×, qo=0.61×, sh=0.42×). F064 (exp_057): para-start words have a distinct onset class. Is there a difference between line-final words on para-INTERIOR lines vs the line-FINAL of a paragraph?
**Description:** For B body text, classify lines as: (1) within-paragraph continuation lines, (2) last line of a paragraph. For each group, compute last-word onset distribution and enrichment. If the para-final last word has a different onset class than within-para last words, this would show paragraph-level boundary marking at the last word.
**Expected outcome:** If boundary marking: para-final last words have different onset distribution than mid-para last words (e.g., para-final avoids qo, prefers o or d). If no distinction: the line-final grammar is purely line-level, not paragraph-level.
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

## H126: The B Paragraph Tripartite Structure (p-onset START → -am LINE-ENDs → o-onset PARA-END) Can Be Used to Parse Paragraph Structure Automatically
**Priority:** medium
**Status:** open
**Source:** F087 (exp_080): B shows a tripartite positional grammar: p-onset marks para-starts; -am suffix marks within-para line-ends; o-onset marks para-ends. If this structure is consistent, it should be possible to use these markers to PREDICT where paragraph boundaries are — i.e., to parse paragraph structure from word features alone (without the locus codes). How accurately does the tripartite grammar predict the observed locus-code paragraph structure?
**Description:** (1) For each B line, compute: is the first word p-onset? is the last word -am? is the last word o-onset? (2) Train a simple classifier: predict is_para_start from previous-line's last word features (is it o-onset? is it -am?). (3) Evaluate precision/recall of -am words for identifying within-para line-ends vs para-final line-ends. (4) How often does the tripartite grammar break down (p-onset mid-paragraph, o-onset within-para, -am at para-end)?
**Expected outcome:** If parseable: -am predicts within-para line-end with high precision (>70%); o-onset last word predicts para-final with >50% precision; p-onset first word predicts para-start with >60% precision. If inconsistent: the grammar is more approximate than suggested.
**Cost estimate:** small
**Prerequisites:** exp_080 (done)

---

## H127: The d-Onset Words (dam, chdam) Forming Line-Closers in Both Dialects Are a Cross-Dialect Function Word Subclass
**Priority:** medium
**Status:** open
**Source:** F086/F087 (exp_079/exp_080): dam is the only word appearing as a line-closer in BOTH A (62.5%) and B (77.4%). chdam is a B line-closer (60%). Both end in -am. Are there other d-onset words that bridge A and B in their positional behavior? d-onset is enriched at line-finals in BOTH dialects (A: d→1.73×, B: d→1.51×) — a cross-dialect positional grammar feature. Is d-onset the "cross-dialect bridge" onset class, appearing at line-finals in both systems?
**Description:** (1) Compute d-onset line-final rate for ALL d-onset words in both A and B. (2) Are there d-onset words that appear in both dialects with similar positional behavior? (3) Compare: dam in A vs B (line-final rate, what precedes it, what follows). (4) Does dam in A have the same positional role as dam in B, or are they the same orthographic form serving different grammatical functions?
**Expected outcome:** If cross-dialect bridge: d-onset words (especially dam and chdam) have similar line-final rates in both dialects, suggesting d-onset grammatical words are dialect-stable (unlike the sh→qo vs d→qo opposition). If dialect-specific: dam in A and dam in B have different distributional profiles despite the same form.
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

## H131: The Two Herbal A Registers (Aiin-Dom vs Y-Dom) Are Written by Different Scribes or Represent Different Sections of the Herbal Content
**Priority:** medium
**Status:** open
**Source:** F088 (exp_081): Aiin-dom and y-dom Herbal A show: (1) different suffix paradigms (-ol/-or vs -ey/-eey); (2) opposite she-→qo coupling; (3) different bigram grammar strength; (4) different e-infix word rates. These differences are as large as the A vs B dialect difference for some features. The AIIN_DOM_FOLIOS set (f1r-f16v) may correspond to a specific quire or scribe section in the physical manuscript.
**Description:** (1) Map the aiin-dom and y-dom folios to their physical quires in the manuscript. Do they fall into distinct quires? (2) Do the aiin-dom folios have different illustration styles (herbal A plant drawings vs y-dom plant drawings)? (3) Is the aiin-dom/y-dom split purely folio-based or does it appear within single folios? (4) Is the AIIN_DOM_FOLIOS set (f1r-f16v, 24 folios) physically contiguous in the manuscript?
**Expected outcome:** If scribe split: aiin-dom folios are all from one or two quires (suggesting different hands). If section split: aiin-dom represents a specific content subsection of Herbal A with different language register.
**Cost estimate:** small (reference-based)
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

## H134: The Aiin-Dom Register Corresponds to Specific Early Quires (f1-f16 = Quires 1-3), Suggesting a Scribal or Section Break in Herbal A
**Priority:** medium
**Status:** open
**Source:** F089 (exp_082): The AIIN_DOM_FOLIOS set (f1r-f16v) was identified by their high daiin/y-suppression rates in exp_059. These folios are f1-f16, which correspond to early quires of the Voynich manuscript. The large morphological difference between aiin-dom and y-dom (different suffix paradigms, opposite she-→qo coupling) may reflect a physical manuscript break — either different scribes or different content sections. Are f1-f16 physically contiguous (early quires), and does this align with known codicological breaks?
**Description:** (1) Map f1r-f16v to quire numbers using standard Voynich MS codicology. (2) Do f1-f16 form complete quires (quires 1-3 of the manuscript)? (3) Are there known hand-changes at these folio boundaries? (4) Check the Beinecke MS 408 catalog for quire structure information. (5) Are there other register differences at the f16/f17 boundary beyond suffix paradigm?
**Expected outcome:** If quire break: f1-f16 = quires 1-2 or 1-3, with a clear physical demarcation from f17+. This would suggest the aiin-dom register corresponds to a scribal section or quire. If not: folios are from mixed quires and the register split is content-based, not physical.
**Cost estimate:** small (reference-based)
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

## H139: The A and B Positional Grammar Models Predict a Consistent Sentence/Phrase Structure (Subject/Verb/Object Analogues)
**Priority:** medium
**Status:** open
**Source:** F090 (exp_083): A model: [sh/ch PARA-START] → [-am line-ends] → [daiin PARA-END]. B model: [o/sh+long+edy PARA-START] → [-am line-ends] → [o+med+eedy PARA-END]. The positional grammar has a clear tripartite structure in both dialects. If Voynichese is a natural language (or encodes one), these positional markers might correspond to syntactic roles: para-start = topic/subject; para-final = predicate/conclusion; -am line-ends = continuation. Does this match any known typological pattern?
**Description:** (1) Are there any natural language typologies where sentence-initial and sentence-final particles differ this systematically? (2) Do the positional markers (para-start words, para-final words) co-occur in specific ways — e.g., is there a fixed topic-comment order at the paragraph level? (3) Can paragraph content between sh/ch-onset start and daiin-final end be decoded as a consistent syntactic unit? This is more interpretive than computational.
**Expected outcome:** The positional grammar suggests Voynichese paragraphs have consistent internal structure: an opening formula (sh/ch in A; o/sh+long in B) followed by content lines ending in -am, concluding with a closing formula (daiin in A; o+medium in B).
**Cost estimate:** zero (synthesis from existing data)
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
**Status:** open
**Source:** F090/F091/F092 (exp_083/084/085): We have two full positional grammar models: A=[she-para-start → -am within-para → daiin/ch para-end]; B=[o/sh+long+edy para-start → -am within-para → o+med+eedy para-end]. Can these models PREDICT paragraph structure in new folios not used for model building?
**Description:** (1) Hold out a subset of folios (e.g., Pharma A, Astro B). (2) Use the positional grammar model to predict: which lines are para-starts, which are para-finals? (3) Evaluate precision/recall against the actual locus-code para-start markers. (4) What is the best predictor combination? Is it above chance?
**Expected outcome:** If grammar models are real: precision/recall for para-start prediction should exceed 30%/30% (far above the ~10% base rate). If over-fit to training data: prediction on held-out sections falls to chance.
**Cost estimate:** medium
**Prerequisites:** F090/F091 (exp_083/084)

---

## H147: The she- Lexical Class Has a Consistent Semantic Register — she-Words Appear With Specific Content Words That Suggest a Grammatical Function (Aspect/Topic Marker)
**Priority:** medium
**Status:** open
**Source:** F091/F092 (exp_084/085): she-prefix is 4.74× enriched at para-starts, AND predicts qo-following (27.5% she-→qo vs 11.4% base). The she- function appears to be inherent to she-lexemes (not context-driven). What follows she-words? Do specific content words co-occur with she-words more than expected?
**Description:** (1) For each A record containing she-prefix words: what are the most over-represented following-words? (2) Is there a recurring {she-word} → {X} pattern where X is a specific content or function word? (3) Do she-words appear in specific topic/content contexts (e.g., only in Herbal sections, not Pharma)? (4) Compare she-para-start lines vs she-non-para-start lines: do they have different following-word profiles?
**Expected outcome:** If she- is a grammatical marker: the following-word distribution after she-words would be drawn from a restricted class (qo-onset words plus a few other common words). The co-occurrence pattern may reveal what grammatical role she- encodes.
**Cost estimate:** small
**Prerequisites:** F091/F092 (exp_084/085)

---

## H148: daiin in Currier B Is a LINE-OPENER (34.0% LFirst, 9.5% LLast) — Completely Different Grammatical Role Than A (Where daiin Is a Line-Closer)
**Priority:** high
**Status:** open
**Source:** F093 (exp_086): In Currier B, daiin has LFirst%=34.0%, LLast%=9.5% — it functions as a LINE-OPENER, not a line-closer. In Currier A, daiin has LFirst%=19.4%, LLast%=25.9% — a line-closer/para-boundary marker. This is a fundamental cross-dialect reversal in daiin's grammatical role.
**Description:** (1) Verify the daiin-B line-opener finding: what words FOLLOW daiin on the same line in B? (2) What words PRECEDE daiin on the same line in B? (3) Is daiin predominantly the FIRST WORD of B lines (34% LFirst), or does it appear both first and mid-line? (4) Is the daiin-B line-opener consistent across all B sections, or concentrated in one section? (5) Can daiin's B role be described as a "line-initial discourse particle" (like how daiin marks line-endings in A)?
**Expected outcome:** If daiin is a B line-opener: most B daiin tokens should appear at line position 0 or 1 (first or second word), with specific following words. This would be a major grammatical discovery — the same word encoding opposite boundaries in two dialects.
**Cost estimate:** small
**Prerequisites:** F093 (exp_086)

---

## H149: The -am Function Words (otam, qokam, dam, okam) and the ol-Line-Closers (oly, oldy) Are Grammatical Synonyms — They Occupy the Same Syntactic Slot
**Priority:** medium
**Status:** open
**Source:** F093 (exp_086): Both -am core words and oly/oldy have LLast%=50-100%, WithinPara%=90-100%, PSFirst%=0%, PFLast%≈0%. They appear to be functionally synonymous. Do they occupy the same syntactic slot — i.e., are they in complementary distribution with each other ON THE SAME LINE?
**Description:** (1) On B lines that end with -am words: what other line-closing words appear? Do -am endings and oly/oldy endings alternate on different lines? (2) Are -am word endings and oly/oldy endings enriched in the same folio regions or different regions? (3) Do -am words and oly/oldy words share preceding contexts (same onset classes precede them)? (4) What is the overlap in preceding-word distributions?
**Expected outcome:** If synonymous slots: -am words and oly/oldy should be in near-perfect complementary distribution — any given line ends with EITHER an -am word OR oly/oldy, not both. If parallel: they might appear in different folio regions (section preference) while serving the same syntactic role.
**Cost estimate:** small
**Prerequisites:** F093 (exp_086)

---

## H150: The s-Onset and y-Onset (True Line-Openers by LFirst%) Have Complementary Grammatical Functions — s Marks One Line-Type, y Another
**Priority:** medium
**Status:** open
**Source:** F093 (exp_086): s-onset has LFirst%=45.9% (A) / 61.3% (B); y-onset has LFirst%=40.7% (A) / 44.4% (B). Both are strongly line-initial. But they have different LLast% and onset distributions. Are they grammatically distinct (s=topic opener, y=continuation/list) or synonymous?
**Description:** (1) Compare s-onset and y-onset positional profiles more finely: what words FOLLOW s-onset line-openers vs y-onset line-openers? (2) Do s-onset line-openers appear in different folio sections or paragraph positions than y-onset? (3) Are s-words and y-words in complementary distribution as LINE-OPENERS (one preferred over the other by section/position)? (4) What are the most common s-onset and y-onset line-first words?
**Expected outcome:** If complementary: s-onset and y-onset mark different line-types (e.g., s=standalone statement, y=continuation). If synonymous: they are interchangeable line-openers with no structural difference.
**Cost estimate:** small
**Prerequisites:** F093 (exp_086)
