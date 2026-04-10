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
**Status:** TESTED (exp_090) — NOT FALSIFIED: she-prefix precision=45.7% (4.74×), astro A=100%. olfchedy/olkey/opchedy B precision=61.5% (14.72×). Cross-dialect combined: 1.95×. Daiin para-final weak (1.35×). Models are high-precision, low-recall on full corpus.
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

## H161: The A Line-Initial y+ch System and the A Line-Initial d+ch System Have Different Preceding/Following Contexts — They Are Not Interchangeable
**Priority:** medium
**Status:** open
**Source:** F098 (exp_091): A has both y+ch (85.9% LFirst) and d+ch (59.6% LFirst) as line-initial prefix systems. But y+ch has HIGHER LFirst% than d+ch. Are they truly synonymous openers? Or do they appear in different contexts (e.g., y+ch at para-starts, d+ch at within-para line-starts)?
**Description:** (1) Compare y+ch vs d+ch: do they appear at para-start lines at different rates? (2) What FOLLOWS y+ch at pos1 vs what follows d+ch at pos1? (3) Are y+ch and d+ch in complementary distribution within paragraphs (e.g., y+ch opens first line, d+ch opens subsequent lines)? (4) Do y+ch words appear only in specific folio sections while d+ch appears in others?
**Expected outcome:** If distinct functions: y+ch opens para-start lines while d+ch opens within-para lines — the difference in LFirst% (85.9% vs 59.6%) reflects different para-level positions. If synonymous: both appear at similar para-position rates.
**Cost estimate:** small
**Prerequisites:** F098 (exp_091)

---

## H162: The Cross-Dialect Positional Grammar Paradigm Has a Universal Structure — Position-Encoding Prefix System Is Voynichese-Level, Not Dialect-Specific
**Priority:** high
**Status:** open
**Source:** F095-F098 (exp_088-091): Both A and B implement: [PREFIXED LINE-OPENER] → [MID-LINE CONTENT] → [LINE-CLOSER]. B: y+k/t opener; qo+k/t mid; -am/oly closer. A: y+ch or d+ch opener; bare ch mid; d+suffix closer. The prefix-encoded positional paradigm is present in BOTH dialects. Hypothesis: this is a universal Voynichese grammatical property, not dialect-specific.
**Description:** (1) Test if the A positional paradigm extends to other stem classes (not just ch): do y+sh, d+sh compounds exist in A and show similar LFirst enrichment? (2) Do the A d+ch openers appear on the same lines as the B y+k/t openers in mixed-dialect sections? (3) Is there a universal line-grammar rule that applies across all Voynichese text?
**Expected outcome:** If universal: the same three-position line grammar should appear in all sections regardless of dialect assignment. This would be the strongest possible evidence for Voynichese as a rule-governed linguistic system.
**Cost estimate:** medium
**Prerequisites:** F095-F098 (exp_088-091)

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

## H164: A Para-Start p-Onset Words Are a Specific Closed Class — Identify Them and Their PSFirst Enrichment
**Priority:** high
**Status:** open
**Source:** F099 (exp_092): p-onset words dominate A para-starts at 12.41× enrichment (28.8% of PS openers). This is the STRONGEST para-start signal found in A (stronger than she-prefix at 4.74×). Need to identify which specific p-onset words are the para-starters.
**Description:** (1) List all p-onset words in A by frequency. (2) Compute PSFirst%, LFirst%, LLast% for each p-onset word with n≥3. (3) Are para-start p-onset words a specific closed class (like she-prefix, olfchedy)? (4) Are they concentrated in specific sections (astro, herbal, pharma)? (5) What FOLLOWS the p-onset para-starters at pos1?
**Expected outcome:** A small number of specific p-onset words (like "pchedy", "pchor", "pcho") will have very high PSFirst% (>50%) — they are the A paragraph markers analogous to B's olfchedy/olkey/opchedy (61.5% precision). This would complete the A para-start grammar.
**Cost estimate:** small
**Prerequisites:** F099 (exp_092)

---

## H165: d-Chain Pattern in A — d-Closer → d+ch Opener Sequence Is Systematically Above Chance
**Priority:** medium
**Status:** open
**Source:** F099 (exp_092): When a line ends with a d-onset word (d-closer), the NEXT line opens with d+ch at 35.7% vs y+ch at 16.2% (ratio 2.20×). This suggests a d-chain continuity pattern: d-onset LINE-CLOSER triggers a d-onset LINE-OPENER on the following line. Test if this is statistically significant and if it creates multi-line d-chain runs.
**Description:** (1) Measure: P(d+ch opener | prev d-closer) vs P(d+ch opener | prev non-d-closer). (2) Is the 35.7% rate significantly above expected? (3) Do d-chains (d-closer → d+ch → d-closer → d+ch → ...) extend for 3+ lines? (4) Is there a complementary o-chain (o-ending → y+ch opener → o-ending)?
**Expected outcome:** d-chains appear at significantly above chance. This would establish a INTER-LINE CONTINUITY GRAMMAR: d-onset words create runs across consecutive lines.
**Cost estimate:** small
**Prerequisites:** F099 (exp_092)

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

## H167: k-Onset A Para-Start Words — Identify the Specific k-Onset Para-Start Vocabulary
**Priority:** high
**Status:** open
**Source:** F100 (exp_093): k-onset words are para-start enriched in A (4.32×) and VERY strongly in B (9.91×!). k-onset is the SECOND strongest gallows-initial para-start class. Need to identify which specific k-onset words (kol, kor, kaiin, kedy, etc.) drive the para-start enrichment.
**Description:** (1) List all k-onset A words by frequency. (2) Compute PSFirst% for k-onset A words with n≥3. (3) Compare: are k-onset A PS words the same structural forms as p-onset A PS words? (4) Check B k-onset PS words (9.91× — even stronger than p-onset!) — what specific B k-onset words open paragraphs? (5) Is there a "gallows-initial" closed class for k/p/t/f that marks discourse-level positions?
**Expected outcome:** A specific subset of k-onset words (like kol, kor — the same stems as ch-stems but with k-initial gallows) will show high PSFirst%. The gallows character (k gallows ≡ t/p gallows) systematically marks para-starts.
**Cost estimate:** small
**Prerequisites:** F100 (exp_093)

---

## H168: The Four-Level Positional Grammar Is Encode in the Gallows Character System — p/k = Para-Level; Non-Gallows = Line-Level
**Priority:** high
**Status:** open
**Source:** F100 (exp_093): p/k/t-onset (gallows characters) = para-starters; y/d/qo (non-gallows) = line-level. In EVA, k and t are the "regular gallows"; p and f are the "platform gallows". All four gallows characters should show para-start enrichment.
**Description:** (1) Check f-onset words — do f-onset words also show para-start enrichment? (2) Within gallows class: is p-gallows enrichment > k-gallows > t-gallows > f-gallows? (3) Are qo-prefix + gallows words (qok, qot) showing para-start SUPPRESSION? (4) Does the y-initial line-opener system ever use gallows stems (y+k, y+t)? This would explain y+k/t compounds in B as a way to "recruit" gallows stems into the WITHIN-LINE position.
**Expected outcome:** f-onset words are also para-start enriched. The four gallows characters (p/k/t/f) collectively mark paragraph-level positions; prefixes (y/d/q) recruit the same gallows stems for within-line positions.
**Cost estimate:** small
**Prerequisites:** F100 (exp_093)

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

## H171: Is the Gallows Hierarchy Consistent for ALL Gallows Characters Individually? (bare_p > bare_t > bare_k?)
**Priority:** medium
**Status:** open
**Source:** F101 (exp_094): bare_p is strongest (A=40.2% PS, B=10.7%); bare_t next (A=10.2%, B=3.9%); bare_k weakest (A=5.7%, B=3.0%). Is there a consistent internal hierarchy within the gallows class: p > f > t > k? And is this hierarchy consistent across sections?
**Description:** (1) Section-specific analysis: does herbal A show same gallows hierarchy as pharma A? (2) Does bare_t appear at para-starts more than bare_k in all sections? (3) What is the functional difference between bare_k and qo+k — if they have same LFirst% (~10%) but different PS rates (3% vs 0.1%), they may differ in discourse function but not line position. (4) Is p > f > t > k a consistent hierarchy across sections and dialects?
**Cost estimate:** small
**Prerequisites:** F101 (exp_094)

---

## H172: The Prefix-Demoted Gallows Grammar Applies to A's ch-Stems Analogously — p+ch = Para-Starter, y+ch/d+ch = Line-Opener, bare ch = Mid-Line
**Priority:** high
**Status:** open  
**Source:** F101 (exp_094): A's ch-stem system: bare_ch(7.1% LFirst) < d+ch(59.6%)/y+ch(85.9%) line-openers < p+ch(para-starters). This is exactly the gallows-demotion hierarchy! p+ch would be the "recruited gallows for ch-stem para-start". Test: (1) p+ch words in A — what are their PSFirst% rates? (2) If p+ch = para-starters and d+ch/y+ch = line-openers, this extends the gallows-demotion model to ch-stems in A. (3) Does A have p+sh, p+s, p+d forms as para-starters for sh-stems?
**Expected outcome:** p+ch words have high PSFirst% (para-starters), extending the gallows-demotion model to A's ch-stem paradigm. This would unify A's positional grammar with B's under a single framework: para-starters use gallows-initial prefix; line-openers use y/d-prefix; mid-line = bare.
**Cost estimate:** small
**Prerequisites:** F101 (exp_094)

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

## H175: Does the B Dialect Show the Same Gallows+Stem Para-Start Hierarchy? (pch/fch/tch in B)
**Priority:** high
**Status:** open
**Source:** F102 (exp_095): In A, p+ch and f+ch are para-starters, y+ch/d+ch are line-openers. In B, the ch-stem system is used differently (ch is mid-line in B; B uses k/t stems not ch). But B also has gallows words at para-starts. Does B show p+ch = para-starter? Or p+t/p+k? Test the B-equivalent of the A gallows+stem hierarchy.
**Expected outcome:** In B, p+ch should also show elevated PS rate; but B's primary para-starters may be p+t or p+k (gallows+gallows compounds). The B answer will tell us if the A gallows-demotion model is universal.
**Cost estimate:** small
**Prerequisites:** F102 (exp_095)

---

## H176: The k-onset Words in A Are a DIFFERENT Positional Class Than k-onset in B — A's k-onset Is Line-Distributed; B's k-onset Is More Para-Concentrated
**Priority:** medium
**Status:** open
**Source:** F101-F102: In A, k+ch=3.5% PS (very weak); bare_k=5.7% PS (weak). In B, bare_k=3.0% PS but total B k-onset=9.91× — the B k enrichment is driven by k at line-first generally, not just para-starts. Test: is B k-onset concentrated at ANY line-first position (not just para-starts) more than A k-onset?
**Cost estimate:** small
**Prerequisites:** F101, F102

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

## H178: The Prefix Determines Position; Does the STEM AFFECT MEANING (Content vs Function Words)?
**Priority:** high
**Status:** open
**Source:** F103 (exp_096): Prefix determines position; stem determines content. But are some stems FUNCTION words (abstract) while others are CONTENT words (concrete)? Test: (1) Do para-start p+ch words use the SAME ch-stems as within-para y+ch and d+ch? (2) Are there "exclusive" stems that only appear with one prefix type? (3) If stem = content and prefix = position, then the same stem should appear with p-, y-, d-, and bare forms depending on context. Test this.
**Expected outcome:** The same ch-stems (chor, chol, chey) appear with all three prefixes (p+ch, y+ch, d+ch) — the stem is semantically stable and the prefix shifts position. If TRUE: Voynichese is a positional morphology system. If FALSE (stems are prefix-exclusive): the stem+prefix combination = lexical item with no stem reuse.
**Cost estimate:** small
**Prerequisites:** F103 (exp_096)

---

## H179: f+ch Cross-Dialect Asymmetry — Why Is f+ch Para-Level in A (21% PS) But Mid-Line in B (0% PS)?
**Priority:** medium
**Status:** open
**Source:** F103 (exp_096): f+ch appears at para-starts 21.4% in A but 0% in B (n=34). This is the one major exception to the unified grammar model. Test: (1) In B, where do f+ch words appear? Are they truly mid-line? (2) Is the B f+ch distribution section-specific (only in specific B folios)? (3) Could the n=34 sample in B be too small? (4) Does B use other gallows+ch forms for para-starts instead of f+ch?
**Expected outcome:** The B f+ch distribution may be section-specific or folio-specific. Alternatively, B uses different gallows (k+sh=9% in B, which is stronger than k+sh in A) to compensate for f+ch's mid-line role. The exception may be real: A uses both p and f as para-starters; B uses primarily p (and less f).
**Cost estimate:** small
**Prerequisites:** F103 (exp_096)

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

## H181: Voynichese Positional Grammar Completeness Test — Can We Predict Line Position From Prefix With >80% Accuracy?
**Priority:** high
**Status:** open
**Source:** F101-F104 (exp_093-097): We now have a complete positional grammar model: {p,f}+stem=para; {y,d}+stem=line-opener; {qo}+gallows=mid-line; bare_ch=mid-line. Test: given a word's morphological form (prefix + stem class), can we predict whether it's at (1) para-start, (2) within-para line-first, (3) mid-line, or (4) line-last with >80% accuracy?
**Description:** (1) Build a classifier: word → predict positional tier. (2) Use prefix type and stem class as features. (3) Compute confusion matrix: how often does the predicted tier match the actual position? (4) What are the most common misclassifications? (5) Does accuracy differ by section or dialect?
**Expected outcome:** High accuracy (>70%) for classifying words into positional tiers based on morphology alone. This would confirm the MORPHOLOGY-TO-POSITION MAPPING is the dominant grammatical rule in Voynichese. Misclassifications would identify edge cases.
**Cost estimate:** medium
**Prerequisites:** F101-F104 (exp_093-097)

---

## H182: Do Voynichese Paragraphs Have Consistent Internal Structure? (Para-Level Template Test)
**Priority:** high
**Status:** open
**Source:** F100-F104: We know individual words have strong positional grammar. But do paragraphs have consistent internal structure? Test: (1) What is the typical A/B paragraph length (in lines)? (2) Is there a consistent pattern within paragraphs: gallows-word first line, then multiple y/d+ch openers, then final d-onset closer? (3) Is the "paragraph" a coherent unit with observable internal structure?
**Description:** (1) Compute paragraph lengths (number of lines per paragraph) for A and B. (2) For each paragraph, track the sequence of line-opener types: para-start line (gallows opener), then line 2 (y/d+ch?), line 3... (3) Is there a modal paragraph template? (4) Do para-start gallows words always appear at line 1, or also mid-paragraph?
**Expected outcome:** Paragraphs have consistent structure with gallows word at line 1, followed by y/d+ch-type openers for internal lines, and possibly d+ch or d-onset words at para-final line. This would complete the multi-level grammar characterization.
**Cost estimate:** medium
**Prerequisites:** F100-F104

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

## H184: What Are the "OTHER" Para-Start Words? — Coverage Gap Investigation
**Priority:** high
**Status:** open
**Source:** F105 (exp_098): ~54% of para-starts begin with "OTHER" words not captured by the PARA/LINE_OPEN/MID/WEAK_PARA classifier. This is the largest single category at para-starts. What onset classes do these words use? Are they: (1) o-onset words, (2) words beginning with specific vowel-onset patterns, (3) word-forms with specific suffixes, (4) section-specific vocabulary?
**Description:** Extract all para-start words classified as "OTHER" in A and B. Compute onset distribution (o, a, e, s, c, etc.). Compare to within-para OTHER words. Identify if specific word forms are para-start-enriched within the OTHER category.
**Expected outcome:** Likely find that o-onset words (like ol, or, or similar) are para-start enriched. These would be a FOURTH positional class beyond the gallows system — an "o-prefix para-start" class to complement p/k/t/f para-starters.
**Cost estimate:** small
**Prerequisites:** F105 (exp_098)

---

## H185: Para-Final o-Onset Specialization — Is o-Ending a Paragraph Closer Morpheme?
**Priority:** medium
**Status:** open
**Source:** F105 (exp_098): Para-final last words are 27.4% (A) / 35.3% (B) o-onset. Is this para-specialized or just a property of line-final words in general? Compare o-onset line-last rate at para-final lines vs within-para line-last positions.
**Description:** Test if o-onset words are SPECIFICALLY enriched at para-final positions vs within-para line-last positions. If para-final o-onset > within-para line-last o-onset, then o-onset is a paragraph-closer signal.
**Expected outcome:** o-onset words are somewhat enriched at para-final line-last positions but not dramatically so — the 27-35% rate may simply reflect the general distribution of line-final words ending in o-onset forms.
**Cost estimate:** small
**Prerequisites:** F105 (exp_098)

---

## H186: Stars (B) Paragraph Internal Structure — Are 47-Line Paragraphs Internally Structured Into Sub-Sections?
**Priority:** medium
**Status:** open
**Source:** F105/H183: Stars (B) paragraphs have mean 47 lines (range 37-54). These are massive structural units. Do they have sub-structure? Test: (1) Within-stars paragraphs, do PARA-tier markers appear mid-paragraph (creating internal "sub-paragraphs")? (2) Is there a repeating N-line cycle within stars paragraphs? (3) Do the ~47-line stars paragraphs correspond to known astronomical sub-structures (12 zodiac signs × 4 lines? 36 decans?)?
**Description:** Extract stars-section B paragraphs. Look at line position × opener-tier to find any mid-paragraph structure. Check if paragraph length = some astronomically meaningful number.
**Expected outcome:** Stars paragraphs may have internal structure corresponding to astronomical catalog format. The ~47-line length in stars may be 47 = some combination like 12+12+12+11 (seasonal months) or 36+N (decans).
**Cost estimate:** small
**Prerequisites:** F105/H183 (exp_098)

---

## H187: "OTHER" Para-Start Words — Do They Form Positional Bigrams With Line-2 Words?
**Priority:** medium
**Status:** open
**Source:** F105: 23.2% of A paragraphs start with "OTHER→OTHER" 2-line sequence. If OTHER para-start words have positional grammar, it should appear in their transition probabilities. Do specific OTHER para-starters predict specific line-2 continuations?
**Description:** Extract OTHER para-start words. For each, compute what tier appears on line 2. Does OTHER→LINE_OPEN rate differ by specific OTHER word type? Are some "OTHER" para-starters actually predictive of line-2 structure?
**Expected outcome:** Some OTHER para-start words behave like PARA-tier words (followed by LINE_OPEN at line 2). These would extend the PARA tier class.
**Cost estimate:** small
**Prerequisites:** F105 (exp_098)

---

## H184: "OTHER" Para-Start Investigation
**Priority:** high
**Status:** TESTED (exp_099) — CONFIRMED: "OTHER" PS words dominated by bare_k (9-12× enriched) and bare_t (3.25× A). These are bare gallows para-starters missing from classifier. Extended PARA tier = {p,f}+stem + bare_k + bare_t covers ~65-70% of para-starts.

---

## H185: Para-Final o-Onset Specialization
**Priority:** medium
**Status:** TESTED (exp_099) — PARTIALLY CONFIRMED: o-onset mildly enriched (A=1.52×, B=1.25×). B has stronger para-final specialization: sh-onset (2.88×) and words okeey (16.4×), orol (21.9×), shedy (6.25×). P-onset perfectly excluded from para-finals (0.00×).

---

## H188: Extended Positional Classifier — Add bare_k and bare_t to PARA Tier; Test Coverage Improvement
**Priority:** high
**Status:** open
**Source:** F106 (exp_099): bare_k and bare_t are para-starters (F101, 4-10× enriched) but were missing from the PARA-tier classifier. Adding them should improve classifier coverage from ~38-39% to ~65-70% of para-starts.
**Description:** Rebuild the classifier with bare_k and bare_t in PARA tier. Re-evaluate: (1) new precision/recall for PARA tier; (2) what fraction of para-starts are still "OTHER"? (3) Does adding bare_k/bare_t create false positives (within-para k/t words)?
**Expected outcome:** Coverage increases to ~65-70%, precision may decrease slightly (bare_k/bare_t appear within-para too), but enrichment should still be strong (4-12×).
**Cost estimate:** small
**Prerequisites:** F106 (exp_099)

---

## H189: B Para-Final Closing Words — okeey, orol, shedy, cheam as a Specialized Para-Closing Class
**Priority:** medium
**Status:** open
**Source:** F106 (exp_099): B has para-final words okeey (16.4×), orol (21.9×), shedy (6.25×), cheam (10.9×). Do these form a coherent lexical class? Test: (1) Are they systematically distributed across all B sections or section-specific? (2) Do they share morphological features (all o-onset + -ey/-eey, or sh- + -edy)? (3) Is the para-final closing signal consistent within individual B folios?
**Description:** Extract all para-final last words in B. Cluster by onset class and suffix. Identify the core B para-closing vocabulary. Compare to B line-final words (which are separate from para-final).
**Expected outcome:** B para-closing words = {o-onset + -ey/-eey} + {sh-onset + -edy} — a closed class of 10-15 words that systematically end paragraphs in B. This would be the B equivalent of A's daiin para-closing function.
**Cost estimate:** small
**Prerequisites:** F106 (exp_099)

---

## H190: Astro Section Anomalous Para-Start Grammar — 69% OTHER — What Words Actually Start A Astro Paragraphs?
**Priority:** medium
**Status:** open
**Source:** F106/H186: A_astro has 69.2% OTHER para-starts — highest of any section. These are short captions/labels (~3.4 lines each). What vocabulary do they use? Are they using a completely different para-start system (perhaps image-specific labels)?
**Description:** Extract all astro-section A para-start words. Compute onset distribution. Identify top 20 para-start words. Compare to herbal A para-start vocabulary.
**Expected outcome:** Astro A para-starts use a diverse open-class vocabulary, possibly with more d-onset or o-onset words than other sections, reflecting the label-like nature of astro captions.
**Cost estimate:** very small
**Prerequisites:** F106 (exp_099)

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

## H191: o-Onset Para-Start Words — Which Specific o-Onset Words Are Para-Enriched?
**Priority:** high
**Status:** open
**Source:** F107 (exp_100): Remaining OTHER (52-63% o-onset) is the biggest gap in the classifier. But o-onset words are NOT uniformly enriched at para-starts (overall o-onset: A=0.52×, B=1.28×). ONLY SPECIFIC o-onset words are para-enriched. Need to identify which ones.
**Description:** Extract all o-onset words at para-starts and within-para positions. Compute per-word enrichment at para-start. Identify the specific o-onset words that are para-enriched (≥2×). Are they: (1) olfchedy/olkey-type (established from exp_090 as 87.6× para-starters); (2) o+gallows (ok-, ot-) prefix forms; (3) o+ch (och-onset)?
**Expected outcome:** A small set of specific o-onset words (olfchedy, olkey, opchedy, okar, oty, etc.) are strongly para-enriched, while the majority of o-onset words (otol, okaiin, or, etc.) are within-para. This will identify the "o-onset para-starter" class as a closed set of 10-20 specific words.
**Cost estimate:** small
**Prerequisites:** F107 (exp_100)

---

## H192: Positional Grammar Strength vs Paragraph Length — Short Paragraphs Have Relaxed Grammar?
**Priority:** medium
**Status:** open
**Source:** F107: Astro A (3.4 lines) has relaxed grammar; herbal A (12-13 lines) has strict grammar. Is there a systematic relationship between paragraph length and grammatical strictness?
**Description:** Bin all paragraphs by length (2-4 lines, 5-9 lines, 10-15 lines, 16+ lines). For each bin, compute PARA% and LINE_OPEN% at para-start and within-para. Test whether short paragraphs have lower PARA% and higher LINE_OPEN% at para-starts.
**Expected outcome:** There is a positive correlation between paragraph length and PARA% at para-start. Very short paragraphs (2-4 lines) have lower grammatical constraint.
**Cost estimate:** small
**Prerequisites:** F107 (exp_100)

---

## H191: o-Onset Para-Start Words
**Priority:** high
**Status:** TESTED (exp_101) — CONFIRMED (negative): o-onset is NOT a coherent para-start class (0.52× A suppressed, 1.28× B neutral). Only "op-" sub-onset (9.5×) is para-enriched — via internal p-gallows. olfchedy/olfchey are enriched via internal f+ch morphology. ~17-20% OTHER after v3 is genuinely diverse vocabulary beyond the grammar system.

---

## H192: Grammar Strength vs Paragraph Length
**Priority:** medium
**Status:** TESTED (exp_101) — STRONGLY CONFIRMED: Para-start grammar strictness scales with paragraph length. A long (10-15 lines): 70.7% PARA, 0% LINE_OPEN — strictest in manuscript. A short (2-4 lines): 31% PARA, 8.6% LINE_OPEN allowed. B monotonically increasing (22%→65%), never violates LINE_OPEN exclusion.

---

## H193: Section vs Length Separation — Is Grammar Strictness Driven by Section or Length?
**Priority:** medium
**Status:** open
**Source:** F108: H192 finding conflates section (short=astro, long=herbal, very_long=cosmo+stars) with length. Need within-section analysis: within herbal A, do shorter paragraphs follow grammar less strictly than longer herbal paragraphs?
**Description:** Within each major section (herbal A, pharma A), split paragraphs by length and compute PARA% at PS. If within-section length still predicts grammar strictness, it's a genuine length effect, not a section effect.
**Expected outcome:** Within herbal A, there may be modest length effects (longer herbal paras have higher PARA%), but the main effect is section-level. The "very long" paragraphs in "other" (mean=39.7 lines) may have lower PARA% due to content differences.
**Cost estimate:** small
**Prerequisites:** F108 (exp_101)

---

## H194: Cross-Sectional Positional Grammar Summary — What Is the Final Model?
**Priority:** high
**Status:** open
**Source:** F101-F108: We now have a comprehensive positional grammar model. Time to synthesize into a unified, quantitative summary of the complete Voynichese positional grammar.
**Description:** Build a comprehensive table: For each morphological class × position combination, report the attested rates. Final classifier performance with v3. Summary of what fraction of the manuscript is "explained" by the positional grammar.
**Expected outcome:** A complete, coherent positional grammar model for Voynichese: PARA tier covers ~55% of para-starts in main text, LINE_OPEN tier is perfectly excluded from para-starts, the model correctly classifies ~70-75% of main-text (herbal/pharma/stars) para-start words.
**Cost estimate:** medium
**Prerequisites:** F101-F108

---

## H193: Section vs Length Grammar Separation
**Priority:** medium
**Status:** TESTED (exp_102) — PARTIALLY CONFIRMED: Grammar strictness is primarily section-driven. Within herbal A, shorter paras have HIGHER PARA% (reversed from H192). Within cosmo B, length has genuine positive effect. H192 cross-section gradient = section composition artifact.

---

## H194: Content Word Analysis
**Priority:** high
**Status:** TESTED (exp_102) — CONFIRMED: ch-stem content words show strong section-specific vocabulary. Herbal A: chain, chocthy, choiin exclusive; Pharma A: cheol (6.1×), cheeor (10.4×) enriched; Stars B: cho/cheo/cheeo exclusive; Cosmo B: chcthy/checthy enriched. Each section has distinctive ch-stem morphological signature. PARA+LO+WEAK tiers = only 10-20% of all tokens; ~80% are content words (MID+OTHER).

---

## H195: Section-Specific ch-Stem Vocabulary — Can We Build a ch-Stem Section Classifier?
**Priority:** high
**Status:** open
**Source:** F109: ch-stem words are section-enriched. Can a ch-stem vocabulary-based classifier identify which section a fragment of text comes from? Test: given a set of ch-words from an unknown paragraph, predict its section (herbal/pharma/stars/cosmo). Baseline: random assignment. Performance: how well does ch-stem vocabulary predict section?
**Expected outcome:** The classifier achieves >50% accuracy on section prediction using only ch-stem words (vs 25% baseline for 4-way classification). The section-distinctive ch-words (chain, cheol, cheo) are the best features.
**Cost estimate:** medium

---

## H196: Cross-Dialect ch-Stem Comparison — Do the Same ch-Stems Appear in A-Herbal and B-Stars?
**Priority:** medium
**Status:** open
**Source:** F109: Stars B has exclusive ch-words (cheo, cheeo, chedam) not found in herbal B. Do these appear in herbal A? Are the "exclusive" words truly absent or just below detection threshold?
**Expected outcome:** Some ch-stems appear in herbal A but not in B dialect, and vice versa, reflecting genuine vocabulary differences between dialects.

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

## H199: Zipf's Law — Does Voynichese Word Frequency Follow a Power Law Rank-Frequency Distribution?
**Priority:** medium
**Status:** open
**Source:** F111 (Heaps' law confirmed). Heaps' law and Zipf's law are mathematically related (Heaps' β ≈ 1/Zipf's α for pure power law). Test whether Voynich word frequency rank-frequency distribution follows Zipf's law f(r) ∝ r^(-α), and whether the Zipf exponent α is consistent with the Heaps' β values found in F111.
**Description:** Compute word rank vs frequency for each section and overall. Fit f(r) = C × r^(-α) on log-log scale. Expected: Zipf's α ≈ 1.0-1.5 for natural language. Compare α to the theoretical prediction from Heaps' β (α ≈ 1/β). If α matches the Heaps' prediction, the two statistics are mutually consistent (as they should be for natural language). Also test: are the most frequent words (rank 1-10) the same across sections, or section-specific?
**Expected outcome:** α ≈ 1.3-1.5 (consistent with β≈0.66-0.74 via α≈1/β). Top-ranked words may be grammar/function words (daiin, chedy, qokeedy) universal across sections; lower-ranked words more section-specific.
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
**Source:** F156: daiin/chol/chor/cthol all precede cth at 2.1-3.1× and deplete sh/ch_e. They form a cluster of "cth-nominal introducer" particles. Do they appear in specific positional contexts (LF vs second vs MID) when they precede cth-words?
**Description:** For each of daiin/chol/chor/cthol: (1) When it precedes a cth-onset word, what slot is it in? (LF, second, MID?) (2) Is the pattern that these particles appear at line-final (LL) position and the cth-word opens the NEXT line, or within the same line? (3) Compute: when the bigram [particle→cth] occurs, what is the positional slot of the particle? This reveals whether "cth-introduction" is within-line (particle at MID; cth-word at MID+1) or cross-line (particle at LL; cth-word at LF of next line).
**Expected outcome:** daiin precedes cth within the same line (both at MID positions). If confirmed, daiin is a within-line determiner. If particle is at LL and cth is at LF, these are line-boundary bigrams — counting line-boundary bigrams should be excluded for within-line grammar analysis.
**Cost estimate:** small
**Prerequisites:** F156

---

## H298: Is dy→sh=1.96× a Within-Line Construction or a Cross-Line Bigram Artifact?
**Priority:** low
**Source:** F156: dy→sh=1.96× (n=6/32 transitions). dy is primarily a line-final short word in A; if dy appears at line-end (LL) and sh appears at LF of the next line, the bigram spans a line boundary and is not a syntactic construction.
**Description:** Check all 6 dy→sh bigrams: are they within the same parsed line (same locus P-type line) or cross-line (dy at end of line N, sh at start of line N+1)? If all 6 are within-line, dy→sh is a real construction. If most are cross-line, the enrichment is a line-boundary artifact.
**Expected outcome:** dy→sh is a cross-line artifact (dy ending one line, next line starting with sh). This would confirm that line-boundary bigrams inflate apparent enrichments for line-final words (dy) followed by line-initial onset classes (sh).
**Cost estimate:** trivial
**Prerequisites:** F156

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
