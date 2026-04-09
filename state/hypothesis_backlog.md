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
**Status:** partially tested (exp_012, exp_013, exp_014)
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
**Status:** open
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
**Status:** open
**Source:** exp_031_qo_stripping
**Description:** 52.6% of qo-stripped stem types appear as independent free words (e.g., both "qokeedy" and "keedy" exist). If qo marks a grammatical inflection (case, number, aspect), the qo-form and the bare form should appear in different syntactic positions (e.g., qo-form is line-medial, bare form is line-final) or in different sections. If they're randomly distributed, qo may be a cipher artifact or phonotactically determined variant rather than a grammatical marker.
**Expected outcome:**
- Grammatical inflection: complementary positional/sectional distribution
- Phonotactic conditioning: no distribution difference, qo-form appears wherever stem-form appears (cipher artifact possibility)
- Dialectal: one form dominates in A, other in B
**Test:** For the top 20 qo/bare stem pairs (e.g., qokeedy/keedy), compute: (a) position-in-line distribution (word-initial, medial, final), (b) Currier A/B frequency, (c) section (herbal/bio/pharma/astro/cosmo) frequency.
**Cost estimate:** medium — requires parsing positional data per token
**Prerequisites:** exp_031 (done)
