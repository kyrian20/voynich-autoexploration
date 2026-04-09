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

## F018: Gallows Characters Concentrate at Word Position 1 (22.9%) — Bench-Layer Fingerprint
**Experiment:** exp_006_gallows_grouping
**Date:** 2026-04-09
**Finding:** Simple gallows chars (t, k, p, f) appear in 22.9% of position-1 character slots (vs 6.9% at position 0, 17.4% at position 2, 6.5% at position 3, and 2-3% at positions 4-7). This spike at position 1 reflects the c+gallows pattern (ct-, ck-, cp-, cf-) that is the characteristic signature of the Stolfi bench layer. Gallows are followed most often by 'e' (30%) and 'a' (25.2%).
**Limitation:** Position 1 spike conflates simple gallows (k, t after non-c chars) with compound gallows (ct, ck after initial c). A cleaner analysis would separately count c-preceded gallows from other-preceded gallows.

## F019: Adjacent-Pair Pairing of Fixed-Filler Verbose Cipher Recovers Source Language h2 Exactly
**Experiment:** exp_007_verbose_cipher_control
**Date:** 2026-04-09
**Finding:** Italian with every character doubled by a fixed 'x' filler has baseline h2 = 2.014. After adjacent-pair grouping, paired h2 = 3.411 — exactly equal to the original Italian h2 (3.411). This validates adjacent-pair grouping as a detector for fixed-filler verbose ciphers: paired h2 = source language h2 is the expected signature.
**Limitation:** Only fixed-filler case tested. Variable-filler ciphers produce dramatically different results (paired h2 = 6.13 for random filler).

## F020: Voynich Paired h2 (3.836) Does Not Match Italian (3.411) or Latin (3.509) — Fixed-Filler Verbose Cipher Ruled Out
**Experiment:** exp_007_verbose_cipher_control
**Date:** 2026-04-09
**Finding:** If Voynich were a fixed-filler adjacent-pair verbose cipher on Italian or Latin, its paired h2 should equal Italian h2 (3.411) or Latin h2 (3.509). Observed Voynich paired h2 = 3.836 — exceeds both by 0.33-0.43 bits. The fixed-filler adjacent-pair verbose cipher on Latin or Italian is ruled out. The source language would need h2 ≈ 3.836, which exceeds both Latin and Italian.
**Limitation:** Other natural languages (German, Arabic, Hebrew) not yet tested. Variable-filler or non-adjacent-pair groupings remain open.

## F025: f66r Contains a Two-Column Word/Character List with 67% Hapax Words
**Experiment:** exp_011_f66r_wordlist
**Date:** 2026-04-09
**Finding:** f66r (Quire H, Scribe 5, Currier B, text-only folio) has a two-column L0 structure: Column 1 is a 15-word list (all unique; lengths 3-6 chars); Column 2 is a 31-entry list of mostly single characters, followed by standard Currier B body text. Of Column 1's 15 words, 6 are hapax legomena (never appear elsewhere in manuscript) and 4 more appear only 3 times each — 67% of the word list is rare or unique. Column 2 over-represents rare gallows characters: 'f' (4/10 total occurrences = 40%), 'x' (3/10 = 30%), 'p' (1/7 = 14%). The ZL3b transcription comment explicitly notes "Now individual characters in next column," confirming the two-column structure was recognized by transcribers. Adjacent folios (f65r-f66v) are structurally normal; f66r's structure is isolated.
**Limitation:** Physical manuscript inspection needed to confirm visual column separation. 6 hapax words could theoretically appear in damaged/untranscribed sections.

## F026: ZL3b L0 "Key-Like" Line Markers Found on f49v (Scribe 1) and f76r (Scribe 2)
**Experiment:** exp_011_f66r_wordlist
**Date:** 2026-04-09
**Finding:** Full L0 structural audit reveals exactly 2 folios with a perfectly alternating L0/P0 pattern (one single-char L0 marker per body text line): f49v (Quire G, Scribe 1/Hand 1, Currier A, herbal section) and f76r (Quire M, Scribe 2/Hand 2, Currier B, biological section). ZL3b transcription comment on f76r explicitly reads: "has 'key-like' sequence, here transcribed as L0 labels" — the expert transcribers themselves recognized this structural type as distinctive. Both f49v and f76r are text-only folios (`$I=T`). Two different scribes (1 and 2) use this structure in two different sections (herbal and biological), suggesting it is a deliberate manuscript feature.
**Limitation:** The ZL3b $H= field (hand number) may not exactly correspond to Davis (2020) scribe numbering. Visual confirmation of f76r's key-like sequence against manuscript images not yet performed.

## F023: ot-/ok- Label Words Are Elevated in Non-Herbal Labels (32-41%) vs Body Text (10-15%)
**Experiment:** exp_010_label_word_sections (corrected after exp_011 L0 validation)
**Date:** 2026-04-09
**Finding:** In non-herbal illustrated sections, ot-/ok- initial words account for 40.9% of astro labels (N=499), 39.2% of bio labels (N=125), and 32.4% of pharma labels (N=358). In body text, ot-/ok- appears uniformly at 10-15% across all sections. The herbal section original figure (3.7%) was inflated by L0 misclassification; corrected genuine herbal labels yield only 14 tokens across 6 folios (3/14 = 21.4% ot-/ok-, but N is too small to compare). Core validated finding: ot-/ok- is systematically elevated in labels for non-herbal illustrated content (astro, bio, pharma) compared to body text, making it a labeling-register convention for depicted objects, not a body-text word class.
**Limitation:** Herbal genuine label count (14 tokens) is too small for reliable rate comparison. L0 overloading in ZL3b affects herbal label analysis — see Q002.

## F024: [RETRACTED] "Herbal_A single-char labels" — Analytical Misclassification
**Experiment:** exp_010_label_word_sections → exp_011_single_char_validation
**Date:** 2026-04-09
**Original claim retracted:** F024 claimed herbal_A labels are dominated by single characters (y, o, f, d, e, s, p, x). Raw transcription inspection reveals two completely different phenomena — neither represents plant labels.
**Phenomenon 1 — f49v line markers:** f49v has a perfectly alternating L0/P0 structure: every odd line is an L0 single-character margin marker (f, o, r, y, e, k, s, p, ...), every even line is a P0 body text line. This is a systematic line annotation feature of this specific folio, NOT plant part labels. The 20 single chars on f49v all come from this alternating sequence.
**Phenomenon 2 — f66r column entries:** f66r is a "text only" folio (no plant illustration, Currier B) at the herbal/astro boundary. It has two columns: short words (rary, rals, qor, dary, ykeol, ...) followed by single characters (y, o, s, y, d, o, f, x, ...). The ZL3b transcription comment explicitly notes "Now individual characters in next column." This is a list/table structure, not a herbal plant label page.
**Why retracted:** All 48 herbal "single-char labels" come from exactly two folios (f49v: 20, f66r: 28) with structurally different, non-label content. The ZL3b L0 locus code covers multiple content types, not just object labels.
**Limitation:** The L0 locus code overloading is a recurring analytical hazard in this corpus — future experiments must inspect raw transcription lines rather than relying on locus code alone.
**Experiment:** exp_010_label_word_sections
**Date:** 2026-04-09
**Finding:** Herbal_A has 81 label tokens, TTR=0.556, top "words": y, o, f, d, e, s, p, x — all single characters. This contrasts sharply with astro (TTR=0.828, ot-/ok- multi-word names), bio (TTR=0.864), and pharma (TTR=0.911, near-unique names). The herbal section uses a qualitatively different single-character annotation system. Each section has near-zero vocabulary overlap with other sections (herbal ∩ pharma = 3 shared types).
**Limitation:** Single-character herbal labels need verification against facsimile images — some may be parsing artifacts from damaged or uncertain text.

## F022: No Tested Natural Language Has h2 ≥ 3.836 — Verbose Cipher Hypothesis Further Constrained
**Experiment:** exp_009_source_language_h2
**Date:** 2026-04-09
**Finding:** German (Goethe Faust, 163k chars) h2=3.535, Arabic consonantal (UDHR, 6k chars) h2=3.673, Hebrew consonantal (UDHR, 6k chars) h2=3.723. All are below the Voynich paired h2 target of 3.836 established in exp_007. Hebrew is the closest at 3.723 (-0.112 bits gap). Across five tested languages spanning European alphabets and Semitic abjads (Italian 3.411, Latin 3.509, German 3.535, Arabic 3.673, Hebrew 3.723), no language reaches the Voynich paired h2 target. The trend is monotonic: higher consonant-to-vowel ratio → higher h2, but even consonantal abjads fall short.
**Limitation:** Arabic and Hebrew samples are small (~6k chars from UDHR). Turkish and Finnish (agglutinative languages) not yet tested. Test applies only to fixed-filler adjacent-pair grouping scheme.

## F030: f57v Contains a Repeating 17-Token Sequence with a Compound @169;v Glyph and 3 Additional @Glyphs
**Experiment:** exp_015_f57v_characterization (corrected by exp_019)
**Date:** 2026-04-09
**Finding:** f57v (Quire H, Hand 1, cosmological wheel diagram) contains a circular text band (L03, +Cc locus) with a 17-token sequence repeated exactly 4 times: `o l d r v x k m f/p @169;v t r @170 @171 y I/c @172`. The cycle has 15 invariant positions and 2 variant positions: position 9 (f in cycles 1-2, p in cycles 3-4) and position 16 (I in cycle 1, c in cycles 2-4). `@169;v` is a COMPOUND GLYPH — a single ZL3b token bounded by dots on both sides, not two separate characters. This makes the 4-@glyph cluster at positions 10, 13, 14, 17 consist of: @169;v (compound, always invariant), @170 (invariant), @171 (invariant), @172 (invariant). @169;v appears only inside this repeating sequence. @170, @171, @172 each appear once additionally in other circular bands. Voynich.nu counts this as "4×17 characters" — confirmed correct by IVTFF dot-based tokenization of ZL3b (total tokens = 68 = 4×17). The outer circular band (L02, @Cc) reads as ordinary Voynich prose with no @glyphs. The folio contains a cosmological illustration inside the innermost ring, 5 labels (@L0), 4 riders (@Ro), and a Saturn symbol (@255;) in the lower right corner.
**Correction (exp_019):** exp_015 incorrectly stated "18-character sequence" — the correct count is 17 tokens per cycle because `@169;v` is a single compound token.
**Limitation:** Hand attribution uncertain (ZL3b inline comment says "hand 2 (???) " but $H=1 header says Hand 1). The I vs c at position 16 may reflect transcription uncertainty.

## F027: f66r Column 2 Is NOT a Comprehensive EVA Alphabet Inventory (44% Single-Char Coverage)
**Experiment:** exp_012_f66r_alphabet_test
**Date:** 2026-04-09
**Finding:** f66r column 2 (34 entries, 16 unique) covers only 11/25 EVA single characters (44%) and 1/12 common compound forms (sh only, 8.3%). The 8 absent common characters include the top 5 most frequent EVA characters: e(10.45%), h(9.42%), a(7.44%), i(6.34%), k(5.74%). The characters PRESENT in column 2 (o, y, d, c, l, r, s, t, f, p, x plus sh, @specials) are predominantly characters that stand alone without forming common compound clusters. The characters ABSENT (e, h, a, i, k, n, q) are precisely the characters that fuse into compound forms (ee, ch, sh, aiin, ck, etc.). Also present: 3 non-standard EVA glyphs (@169, @172, @195) and 'air' (a compound form with zero body occurrences). Column 2 may be listing graphically "atomic" or compound-resistant glyph units rather than a full alphabet.
**Limitation:** Column 2 entries were manually enumerated from raw ZL3b transcription. The 'air' entry (zero body occurrences) may be a transcription of a rare glyph or ligature. The @NNN; glyph identities depend on ZL3b transcriber conventions.

## F028: f57v Circular Text Shares Special Glyphs (@169, @172) with f66r Column 2
**Experiment:** exp_012_f66r_alphabet_test (raw ZL3b inspection), exp_014_prior_work_check
**Date:** 2026-04-09
**Finding:** f57v (astronomical/cosmological folio, Scribe 1/Hand 1, ZL3b header: "has 'key-like' sequences") contains a circular text (Cc locus) with a sequence `o.l.[d:j].r.v.x.k.m.f.@169;v.t.r.@170;.@171;.y.I.@172;` repeated 3–4 times. This sequence contains @169; and @172; — the SAME special glyphs that appear in f66r column 2. ZL3b transcribers cross-referenced the two folios explicitly via a "cf f57v?" comment on f66r line L38. The two folios were written by different scribes (Hand 1 vs Hand 5) in different sections (astronomical vs pharmaceutical), yet share the same unusual non-EVA glyphs. This creates a three-way cluster of folios with "key-like" designations in ZL3b: f49v (line markers with @SPECIAL), f57v (circular text, explicitly "key-like"), and f76r (paragraph markers, explicitly "key-like"). The f66r column 2 connects to this cluster via the @NNN; shared glyphs.
**Limitation:** The @169 and @172 glyph identities are assigned by the ZL3b transcribers; the actual manuscript glyphs need visual confirmation to verify they are the same characters in both folios.

## F029: f49v and f76r Line-Marker Sequences Are Independent, Non-Periodic, and Don't Correspond to Adjacent Body Text
**Experiment:** exp_013_line_marker_structure
**Date:** 2026-04-09
**Finding:** f49v has 26 L0/P0 marker pairs; f76r has 9. Neither sequence shows periodic structure (period 1–8, no period achieves ≥50% match). No systematic correspondence to adjacent body text: marker == body first char at 4% (f49v) and 11% (f76r), both at or below the expected-by-chance level (~6%). The two sequences share some characters {d, k, o, r, s} but zero 2-grams or 3-grams, and neither is a subsequence of the other — consistent with independent composition by different scribes. f49v markers show gallows overrepresentation (f: 16.5x, p: 9.1x the corpus rate) and include 6/26 @SPECIAL glyphs (23% of markers are non-EVA). f76r markers show 's' overrepresentation (8.9x) and only 1 @glyph (@174, unique to f76r). The markers do NOT function as running first-char catchwords or content indices into their adjacent lines.
**Correction (exp_016):** The f49v @SPECIAL glyphs are @140(×3), @164(×1), @192(×2), @243(×1) — DIFFERENT glyph IDs from f57v's @169-@172 and f66r's @169/@172/@195. The f49v cluster connection is structural (line-marker designation), not via shared @glyph IDs. F028's "three-way @NNN link" overstated: the @NNN connection is specifically f57v↔f66r only.
**Limitation:** With N=26 and N=9, statistical power for correspondence tests is low.

## F031: Manuscript-Wide @Glyph Census — 114 Occurrences, 63 Types, 0.3% of Words; f57v Is Densest
**Experiment:** exp_016_at_glyph_census
**Date:** 2026-04-09
**Finding:** The full ZL3b corpus contains 114 @glyph occurrences of 63 distinct types across 64 folios (0.303% of ~37,676 words). Most are hapaxes: 44/63 types (70%) appear on only one folio. f57v is the most @glyph-dense folio (19 occurrences), followed by f49v (7). @169 and @172 are the ONLY @glyphs shared between a Hand 1 folio (f57v) and a Hand 5 folio (f66r) — the widest cross-hand sharing of any @glyph in the manuscript. Hand 1 accounts for 55% of all @glyph occurrences and 37 distinct types. Hand 5 (f66r only) has just 3 @glyph tokens, all on f66r, all matching or related to f57v (@169, @172, @195). f68r2 (astronomical, Hand 4) has 4 consecutive unique @glyphs (@231-@234) — a possible second "structured @glyph sequence" in the manuscript. @170 and @171 appear exclusively on f57v and nowhere else.
**Correction to F029/F028:** f49v's @SPECIAL glyphs (@140, @164, @192, @243) are DIFFERENT from f57v's (@169-@172) — no @glyph IDs are shared between f49v and f57v/f66r.
**Limitation:** The @NNN numbering scheme is ZL3b-specific; it may not correspond directly to any external glyph catalog. @glyph IDs encode the transcribers' enumeration order, not necessarily glyph relationship.

## F021: Stolfi Crust Stripping Does Not Recover Natural-Language h2 — Core Region h2=2.389
**Experiment:** exp_008_stolfi_slot_entropy
**Date:** 2026-04-09
**Finding:** Stripping Voynich words of their outer crust characters (leading: d,l,r,s,n,y,g,q; trailing: y,n,m,d,l,r,s) raises h2 from 2.341 to only 2.389 — a gain of 0.048 bits. The core region remains far below natural-language h2 (~3.4-3.5 bits). Core region top characters are o(19.4%), e(15.6%), h(13.4%), a(10.9%), c(10.0%) — the same characters that dominate the full corpus. Stripping terminal y/n/m alone gains +0.121 bits (to 2.462). Stripping leading q alone LOSES 0.003 bits (to 2.338). Words containing gallows characters (51.9% of words) have LOWER h2 (2.271) than the full corpus average — gallows-containing words are more constrained, not less.
**Limitation:** Crust-stripping algorithm is a character-class approximation of the Stolfi grammar, not the full slot grammar. A proper Stolfi parser might find different core residuals. Position-conditional strip (specific chars in specific slots) not yet tested.

## F035: Currier A and B Vocabularies Are Structurally Incompatible as Dialects (Jaccard=0.148, Alignment 2%)
**Experiment:** exp_023_currier_ab_alignment
**Date:** 2026-04-09
**Finding:** Currier A (10,255 tokens, 3,356 types) and Currier B (22,178 tokens, 4,876 types) share only 14.8% of their combined vocabulary (Jaccard = 0.148). Context-vector alignment of top-100 words from each dialect produces only 2/100 identical matched pairs (2%) — far below the 21% null expectation from vocabulary overlap. Frequency rank Spearman ρ = 0.337 for 94 shared words in each top-200 (dialects would show ρ > 0.8). A-exclusive high-frequency words are cth-cluster (cthy, cthol, cthor, qotchy: ~250 total tokens) absent from B's top vocabulary. B-exclusive high-frequency words are -edy/-ain paradigm (chedy=478, shedy=411, qokeedy=299, qokain=273 — absent from A's top vocabulary). Shared vocabulary (~21 top-50 words: or, ol, ar, chey, daiin, aiin, dar, etc.) consists of short, structurally neutral function/template words.
**Limitation:** Context vectors were built on just top-100 words per dialect; alignment is greedy (not optimal). The token parsing normalizes uncertainty brackets. A larger alignment (top-300) could reveal additional shared function words.

## F033: f75v Is a Third Line-Marker Folio — Hand 2, Bio Section; Marker Set ⊆ f76r's Marker Set
**Experiment:** exp_022_l0_structural_audit + exp_026_f75v_line_markers
**Date:** 2026-04-09
**Finding:** f75v (biological section, Hand 2, Currier B) has 6 L0 markers in alternating L0/P0 structure: sequence s,l,l,o,r,s. ZL3b transcribers noted this explicitly: "last character in first 5 lines aligned vertically reading slors" (counting L8='o' and L9='r' as a compound 4th-position marker 'or'). f75v is Hand 2 — THE SAME HAND as f76r (also Hand 2, Currier B, bio). Combined with f49v (Hand 1/Currier A/herbal, 26 pairs), this makes three confirmed line-marker folios. Crucially, f75v's character set {l,o,r,s} is a proper subset of f76r's character set {d,k,l,o,q,r,s}: all 4 f75v chars appear in f76r, and f76r has 3 additional chars {d,k,q}.
**Limitation:** Image inspection needed to confirm markers are in the same scribal hand as the body text (or a different layer).

## F034: ZL3b L0 Contains Only 9 True Object Labels Out of 160 Entries (5.6%); Cosmo Section Has 53 L0 List Entries
**Experiment:** exp_022_l0_structural_audit
**Date:** 2026-04-09
**Finding:** Full L0 audit (all prefix variants: L0, *L0, +L0, @L0, =L0, &L0, /L0, ~L0) finds 160 total entries classified as: 9 TRUE_LABEL (5.6%), 43 LINE_MARKER (26.9%), 108 LIST_ENTRY (67.5%). Herbal_A has only 1 TRUE_LABEL (f2r: 'ios an on' = 3 tokens) after excluding f49v. Cosmo section folios f67r2 (19 entries), f67v1 (12 entries), and f69r (22 entries) account for 53 L0 list entries — cosmo zodiac/ring diagram labels in list format. The majority of Voynich "label" content is in other L* locus codes (Lf ≈193, Lz ≈299, Ls ≈75, Lc ≈40) not yet audited.
**Limitation:** This audit covers L0 only. The locus codes Lf, Ls, Lz, Lc, Ln, Lt need separate auditing to fully characterize the label corpus. The exp_003 "label corpus" of 1065 tokens was likely drawn from multiple L* codes combined.

## F032: f57v Cycle and f66r Column 2 Share a Statistically Significant Character Inventory (p=0.003)
**Experiment:** exp_021_f57v_f66r_overlap
**Date:** 2026-04-09
**Finding:** The character sets of f57v's 17-token repeating cycle and f66r column 2 overlap significantly (Jaccard=0.667, p=0.003 vs hypergeometric null). Of 25 EVA single chars, f57v uses 14 and f66r col2 uses 11; the intersection is 10 — 3.84 chars above random expectation. Both sets converge on: {c, d, f, l, o, p, r, t, x, y}. The only char in f66r but not f57v is 's'; only in f57v are I, k, m, v. Additionally, the f→@169 adjacency appears in both: f57v pos 9-10 is f then @169;v; f66r col2 entries 8-9 are 'f' then '@169'. The character ORDER in f66r col2 does NOT correspond to f57v cycle positions (Spearman ρ ≈ -0.09), ruling out f66r as a simple linearization of f57v's cycle.
**Limitation:** The shared char set heavily overlaps with H022's "non-compound-forming chars" category, so the overlap may partially reflect both lists independently avoiding compound-forming chars rather than a direct relationship. These two explanations are not mutually exclusive.

## F046: Bio Section Is Most Repetitive (TTR=0.552); f76r Is Most Repetitive Folio (TTR=0.466)
**Experiment:** exp_039_folio_diversity
**Date:** 2026-04-09
**Finding:** Section mean TTR: herbal=0.835 (most diverse, 122 folios), pharma=0.771, special=0.646, text=0.645, bio=0.552 (most repetitive, 19 folios). Folio outliers: f48r and f96v (herbal) have TTR=1.000 — every token unique. f76r (text/T section, the "key-like sequence" folio) has TTR=0.466 — LOWEST in the manuscript, z=-1.7 for its section. f84v (bio, TTR=0.478) and f116r (special, TTR=0.505) also extremely low. All high-TTR outliers are herbal; all low-TTR outliers are Currier B (bio/text/special). f19r (herbal) is the most repetitive herbal folio (TTR=0.653, z=-2.6).
**Limitation:** TTR is inversely correlated with token count; folios with more tokens naturally have lower TTR. High-TTR herbal outliers (TTR=1.0) have only 50-74 tokens each — this is partly a small-sample effect.

## F045: Currier B Has a Systematic 9-Form Suffix Paradigm: 384 Stems with 2+ Suffix Variants
**Experiment:** exp_038_edy_ain_paradigm
**Date:** 2026-04-09
**Finding:** In Currier B, 384 stems take 2+ distinct suffix variants; 311 stems have edy/ain/aiin variants. The stem 'qok' generates 1,559 tokens in 9 suffix forms (-eedy/-ain/-edy/-eey/-aiin/-y/-ey/-chy/-dy). Top stems: ch(1041), sh(870), ok(704), ot(604). Suffix positional distribution: -aiin most line-initial (14.2%), -ain most line-final (8.0%, chi²=5.8 vs -edy's 6%), -edy most medial (85%). Section: -aiin concentrates in 'S' (57%), -edy in bio (42%), -ain in 'S' (54%). All types absent from pharma. The suffix system is structurally consistent with grammatical inflection (case/aspect marking) on a ~10-stem core vocabulary.
**Limitation:** Position-in-line is a crude syntactic proxy; true grammatical role assignment would require sentence-level structure, which Voynich text structure doesn't clearly expose.

## F044: 'o' Functions as a Label-Form Prefix — 64.3% of o-Initial Labels Are o+Body-Word
**Experiment:** exp_037_label_o_prefix
**Date:** 2026-04-09
**Finding:** 101/157 (64.3%) o-initial label tokens have their body (word-minus-'o') in the body-text vocabulary (otar→tar, otol→tol, ockhy→ckhy, octhey→cthey, etc.). Labels show 2.5-3.3× higher o-initial rate than body text in the same sections (astro: 60.5% label vs 18.2% body; bio: 60.2% vs 21.4%; pharma: 54.4% vs 21.6%). The section-invariant elevation rules out section vocabulary bias. KL divergence of o-initial bigrams (label vs body) = 0.154 bits — stems after 'o' follow body-text patterns. 'o' is a label-form morpheme structurally parallel to the 'qo' prefix in Currier B: both add a prefix to transform body-text vocabulary items into a labeled/grammatical form. ot-/ok- concentration: 64.3% of o-labels start ot- or ok-.
**Limitation:** 35.7% of o-labels do not have body-text stems — these may be label-unique vocabulary items or the stem analysis is too aggressive (e.g., okodar≠o+kodar if kodar is uncommon). Sample size 157 o-labels is small.

## F043: Labels Are 'o'-Initial Dominated (58.4%) and 'q'-Initial Absent (1.9% vs 16.3% in Body)
**Experiment:** inline analysis (Lf+Ls+Ln+Lt label corpus vs body text)
**Date:** 2026-04-09
**Finding:** The clean label corpus (Lf+Ls+Ln+Lt, 269 tokens) shows dramatic initial-char differences from body text: 'o'-initial = 58.4% of labels vs 20.5% of body (+37.9%); 'q'-initial = 1.9% of labels vs 16.3% of body (-14.4%); 'c'-initial = 8.9% labels vs 18.9% body (-10.0%); 'd'-initial = 14.5% labels vs 9.4% body (+5.1%). Final char: 'l' more common in labels (21.6% vs 15.9%), 'n' much rarer (8.2% vs 16.9% — daiin/aiin/kain type words underrepresented). Mean label length = 5.64 vs body 5.18. Label vocabulary contains many tokens absent from body top-500 (otolor, darol, ytodal, ytchodly). Labels avoid qo-type and ch-type onset words, concentrating instead on o-initial vocabulary.
**Limitation:** Only 269 label tokens in this corpus (Lf/Ls/Ln/Lt); Lz (299 entries) and Lf already studied. The 'o'-initial dominance may reflect section bias (pharma section has ot-/ok- type labels from exp_010).

## F042: Word-Final Inventory: {y,n,l,r} Cover 88.8% of Endings; ...dy/...in/...ey/...ol Are Top Bigrams
**Experiment:** exp_036_word_final_inventory
**Date:** 2026-04-09
**Finding:** Word-final character distribution: 'y'=41.1%, 'n'=17.0%, 'l'=15.7%, 'r'=14.9% (together = 88.8%). Top 5 covers 91.8%. Final H = 2.460 bits (vs shuffled 3.86 bits, bias=1.48). Top word-final bigrams: ...dy=18.6%, ...in=16.7%, ...ey=11.0%, ...ol=9.7%, ...ar=7.1%, ...hy=5.8%, ...al=5.4% — top 7 cover 74.2% of all word endings. Currier B has 'y' dominant (45.5% vs A's 31.8%); B final H = 2.324 bits vs A's 2.682 bits (B more constrained). Bio section most y-heavy (54%); pharma most l-heavy (24%). These patterns directly match Stolfi's suffix template predictions.
**Limitation:** Analysis uses word tokens; compound treatments (EVA ch=one char vs two) affect count slightly.

## F041: qo-Prefix Does Not Bridge A/B Gap — qo-Stripped B Stems Are Mostly B-Exclusive
**Experiment:** exp_035_ab_qo_normalization
**Date:** 2026-04-09
**Finding:** Stripping "qo" from Currier B vocabulary barely changes A/B divergence: Jaccard 0.152→0.153 (both normalized), Spearman ρ 0.348→0.387. Of top-15 B-exclusive qo-words, 11/15 stripped stems are NOT in A vocabulary (qokeedy→keedy, qotedy→tedy, etc. all B-exclusive). qo-stripped stems are B-specific vocabulary items, not A-vocabulary with a prefix. 397/3766 B-exclusive types are qo-words (10.5%). The A/B divergence is NOT explained by the qo morphological prefix — the vocabularies are fundamentally different independent of morphological conventions.
**Limitation:** Analysis uses simple type overlap (Jaccard) and rank correlation; word2vec embedding alignment (as originally proposed in H004) could reveal deeper structural similarities.

## F040: qo-Prefix Is a Currier B/Bio-Section Dialectal Marker for k-Initial Vocabulary
**Experiment:** exp_033_qo_complementary
**Date:** 2026-04-09
**Finding:** Comparing top-20 qo/bare-stem pairs (e.g., qokeedy/keedy, qokain/kain): qo-forms appear 88.0% in Currier B vs 11.6% in A; bare stems appear 72.7% in B vs 26.6% in A (15-point A/B gap). Section distribution: qo-forms 39.3% bio vs 14.1% herbal; bare stems 18.2% bio vs 37.2% herbal (23-point reversal). Line position shows minimal differences (<3%). The distribution is NOT complementary — both forms appear in both dialects — but a strong dialectal bias: bare k-initial stems dominate A/herbal, qo-prefixed forms dominate B/bio. Within B, both forms coexist, suggesting qo marks a grammatical subtype rather than pure dialect feature. qokeedy vs keedy shows the strongest positional signal (1% vs 10% line-final, chi²=13.5).
**Limitation:** Analysis covers top-20 pairs only. The qo-morphology may vary across different stem types (k-initial vs t-initial stems not separately analyzed).

## F038: Non-L0 Label Loci (Lf/Lz/Ls/Lc/Ln/Lt) Are Uncontaminated — 732 True Labels, 100% Section-Specific
**Experiment:** exp_032_label_locus_audit
**Date:** 2026-04-09
**Finding:** All non-L0 label loci have zero single-char entries (no LINE_MARKER contamination). Each locus is 100% section-specific: Lf→pharma (194), Lz→zodiac (299), Ls→astrological (76), Lc→cosmo-pharma (40), Ln→bio (63), Lt→bio (47), plus La/Lp/Lx (13). Total clean true-label corpus: ~732 entries. Type-token ratios are extremely high across all label types: Lc=1.000 (all hapax), Ls=0.988, Lf=0.956, Ln=0.962, Lt=0.957, Lz=0.821 — near-unique labels throughout. Pharma labels (Lf) concentrated in f88-f102 range. Bio labels (Ln/Lt) concentrated in f75v-f84r range; f75v alone contributes 27 label entries (Ln+Lt) confirming its LINE_MARKER L0 entries are structural, not labels.
**Limitation:** Lz "month name" (Romance language) entries were not detected by regex — the zodiac month labels may be in a non-standard format or separate locus within ZL3b.

## F039: Label H2 Shows Section Gradient: L0/Ls > Lf > Body > Lz > Ln > Lc > Lt (1.74–2.31 bits)
**Experiment:** exp_032_label_locus_audit
**Date:** 2026-04-09
**Finding:** H2 values by label type: L0=2.312, Ls=2.265, Lf=2.153, body=2.071, Lz=1.851, Ln=1.833, Lc=1.780, Lt=1.739 bits. Biological section labels (Ln, Lt) have the LOWEST H2 — more internally constrained than even body text. Astrological labels (L0, Ls) have the HIGHEST — more diverse than body text. This inverts the section body-text entropy relationship (Currier A herbal tends to be lower H2 than B biological in body text). Near-unique vocabulary (TTR 0.82-1.00) across all label types.
**Limitation:** Token counts for individual label types are small (20-299 tokens); H2 estimates may be noisy.

## F037: qo Is a Morphological Prefix Selecting k/t-Initial Stems — Not a Grammatical Article
**Experiment:** exp_031_qo_stripping
**Date:** 2026-04-09
**Finding:** After stripping the "qo" prefix from qo-initial words (16.8% of corpus), the resulting stems have H_initial = 1.931 bits — 1.095 bits LOWER than non-qo words (3.027 bits). KL divergence between qo-stem initials and non-qo word initials = 2.96 bits. qo-stems are dominated by 'k' (60.5%) and 't' (21.2%), whereas free words are dominated by 'o' (25.1%), 'c' (23.0%), 's' (14.6%). qo-stripped stem H2 = 1.818 bits (lower than corpus average 2.060). 52.6% of qo-stripped stem types appear as independent free words. qo-words are nearly twice as frequent in Currier B (19.4%) vs A (11.1%); B's top qo-words all have k-initial stems (qokeedy, qokain, qokedy).
**Limitation:** The stem identification relies on simple prefix-stripping; morphological analysis doesn't account for possible elision or phonological conditioning. Complementary distribution test (H032) still needed to confirm grammatical alternant status.

## F036: f49v Margin Numerals 1-5 Are Later-Hand Annotations; @140 = Numeral "5"
**Experiment:** exp_030_f49v_numerals
**Date:** 2026-04-09
**Finding:** ZL3b comment on f49v explicitly identifies "a vertical sequence 1 2 3 4 5 aligned with the 1st paragraph, starting from line 2." The L0 entries for f49v lines 2-6 are: o=1, r=2, y=3, e=4, @140=5. These are the ZL3b transcription of Arabic numerals visible in the manuscript margin — a later-hand annotation by a non-Voynich reader/owner numbering the first 5 body lines. @140 is the non-EVA glyph representing "5" (its shape was too non-standard for EVA approximation). The remaining 21 L0 markers (positions 1, 7-26) are original Voynich margin glyphs. The @NNN codes (@140, @192, @164) do NOT form a counting system: gaps between @140 occurrences are 8 and 7 positions (not 5), and modular analysis shows @NNN positions are not multiples of 5. Cross-paragraph alignment is 0/13 — the two f49v paragraphs' L0 sequences are completely independent.
**Limitation:** Image inspection required to confirm the annotation layer identity (ink color, script style) and whether the "1-5" numerals are Arabic digits or another numeral system.

## F002: Pure Glossographic Model (Uniform Template Across All Positions) is Contradicted
**Experiment:** exp_001_word_initial_entropy
**Date:** 2026-04-09
**Finding:** The substantial elevation of word-initial entropy (+0.796 bits) above within-word conditional entropy in Voynichese is incompatible with a text-generation process that constrains all character positions equivalently (pure phonological template / glossolalia model). Under such a model, H_initial ≈ H2; instead H_initial > H2 by a margin larger than seen in natural languages.
**Limitation:** This rules out the uniform-template variant of the glossographic hypothesis only. A model with a specifically constrained onset slot (low H_initial) and constrained continuation positions (low H2) could still produce a structured text without a real lexicon.

## F047: Currier A Has a Suffix Paradigm Parallel to B's — Same Stems, Opposite Suffix Preferences
**Experiment:** exp_040_currier_a_suffix_paradigm
**Date:** 2026-04-09
**Finding:** Currier A has 349 multi-suffix stems (vs B's 639) with the same morphological paradigm structure. Critically, the SAME core stems appear in both dialects but with near-opposite suffix distributions: stem 'ch' takes -ol(225)/-or(146) in A but -edy(430)/-ey(208) in B; stem 'sh' takes -ol(99)/-or(56) in A but -edy(367)/-ey(173) in B. A's top suffixes are -ol (17.0%) and -or (12.1%); B's are -edy (15.1%) and -eedy (6.3%). -edy is 75× more common in B than A; -ol is 2.8× more common in A than B. Additionally, cth- in A functions as a morphological prefix parallel to qo- in B: cth-stripped stems have H_initial=1.966 bits vs 3.061 for free words (nearly identical to qo-'s 1.931 vs 3.027), KL=2.281 bits, selecting o/y/e-initial stems (while qo- selects k/t-initial stems). 37.3% of cth-stripped stems appear in A free vocabulary.
**Limitation:** The suffix frequency analysis uses the same priority-list suffix_group() function as exp_038; the suffix boundaries may occasionally be ambiguous for short words. cth- rate (3.9% of A) is lower than qo- in B (16.8%), so sample sizes for cth- analysis are smaller.

## F048: Voynich Suffix Paradigm Is Productive — Log-Linear r=0.83-0.89 Between Stem Frequency and Paradigm Completeness
**Experiment:** exp_041_paradigm_productivity
**Date:** 2026-04-09
**Finding:** In both Currier B and A, stem frequency (log scale) predicts number of suffix variants with Pearson r=0.830 (B) and r=0.891 (A). Under a fixed lexical list, paradigm completeness is stem-specific and uncorrelated with frequency; the observed high correlation is the signature of a productive generative morphological system. KL divergence from the marginal suffix distribution is 0.2-1.1 bits across top stems — "partially productive" regime: stems have preferences but sample from the full paradigm, consistent with natural language inflection. The single outlier is 'd' in A (KL=1.077 bits), driven by daiin being overwhelmingly dominant — analogous to an irregular high-frequency verb form. Singletons (1762 in B, 1339 in A) are most likely sparse samples from the productive paradigm rather than lexically fixed mono-suffix forms.
**Limitation:** Pearson r includes noise from suffix boundary parsing; the analysis uses the same priority-order suffix_group() function as exp_038/040, which may occasionally assign wrong suffix boundaries for short words. The KL analysis uses a single marginal distribution as baseline, not a per-stem prior.

## F049: f76r Body Text Is Structurally Normal Bio Text; "Key-Like" Label Refers to L0 Line Markers Only
**Experiment:** exp_042_f76r_autocorrelation
**Date:** 2026-04-09
**Finding:** f76r body text (514 tokens) shows no significant word-level autocorrelation (max ACF ratio=1.85, threshold=2.0). Its lowest-manuscript TTR=0.466 is due to high frequency of standard Currier B vocabulary (shedy=4.9%, chedy=3.7%, chey=2.1%) rather than periodic structure. The "key-like sequence" ZL3b designation refers exclusively to the L0 line marker layer (already analyzed in exp_013/exp_026), not the P0 body prose. For comparison, f84v and f75v (bio section) both show significant autocorrelation at lag=13 (ratios 2.30 and 2.22 respectively) — a possible bio-section structural feature. Consecutive-line Jaccard similarity: f76r mean=0.045, comparable to other bio folios (range 0.030-0.060).
**Limitation:** Autocorrelation at lag=13 in f84v and f75v may be a sampling artifact (9-10 matches in 305-319 comparisons). A manuscript-wide lag=13 test would be needed to assess whether this is a systematic bio-section feature.

## F050: Bio Section Is 30-85x More Formulaic Than Herbal; bio↔special Is the Most Cross-Section Connected Pair
**Experiment:** exp_043_parallel_passages
**Date:** 2026-04-09
**Finding:** Only 5.7% of word bigram types (1,594/27,926) appear on 2+ folios; only 0.24% of trigram types (73/30,910) appear on 2+ folios — the manuscript is overwhelmingly unique at the phrase level beyond bigrams. Within-section cross-folio bigram sharing: bio=6.0/pair, special=2.9/pair, herbal=0.2/pair (bio is 30× more formulaic). Trigram sharing: bio=0.17/pair vs herbal=0.002/pair (85× more formulaic). Most widespread bigram: "chol daiin" on 24 folios (herbal+pharma). Most widespread trigram: "ol shedy qokedy" on 4 bio folios. Cross-section connections: bio↔special shares the most bigrams (1,404) AND trigrams (17) of any section pair — consistent with exp_038's finding that these sections share the -aiin/-edy suffix paradigm distribution. Herbal is least formulaic at all levels.
**Limitation:** Cross-folio bigram/trigram rate is sensitive to section size (bio has 20 folios with many token-rich pages; herbal has 116 folios with sparser labels). Normalized by pairs, but pair count doesn't fully account for token count differences. The "parallel passages" threshold (2+ folios) is the minimum; true literary "parallel passages" would require 4+ word sequences.

## F051: Hand 4 (Astro/Cosmo Section) Has A-Like Morphology Despite Currier B Designation
**Experiment:** exp_044_hand_qo_variation
**Date:** 2026-04-09
**Finding:** Scribal hand comparison: Hand 1 (Currier A) qo=10.7%; Hand 2 (B, bio+herbal) qo=20.6%; Hand 3 (B, special) qo=17.9%; Hand 4 (B, astro/cosmo) qo=5.9%; Hand 5 (B, herbal) qo=12.2%. Hand 4 is an outlier: its -edy rate is 0.4% (vs 16.4% for Hand 2, 9.9% for Hand 3) and -ol rate is 8.3% (highest of any B hand, close to Currier A). Hand 4's suffix profile resembles Currier A more than other Currier B hands. Hand 3 (Special section) is -aiin dominant (11.4%) — corroborating exp_038's finding that -aiin concentrates in Special section (57%). Within Hand 2 (bio section), qo-rate varies enormously across folios (0.000 to 0.368, std=0.090), suggesting qo-rate is primarily content-driven rather than scribe-driven.
**Limitation:** Hand 4 has only 9 folios (471 tokens) — a small sample. The astro/cosmo section also has circular text structures that constrain vocabulary differently from prose, which may partly explain the anomalous suffix profile. Section and hand identity are strongly confounded throughout (each hand writes specific sections).

## F052: Astro/Cosmo Section (Hand 4) Is A-Adjacent in Morphology Despite Currier B Designation
**Experiment:** exp_045_astro_third_dialect
**Date:** 2026-04-09
**Finding:** Hand 4 astro/cosmo section (9 folios, 471 tokens) has a morphological profile closer to Currier A than to B: qo-rate=0.059 (below even A=0.110, far below B=0.190); -edy=0.7% (near A=0.2%, far below B=18.5%); -ol=13.8% (intermediate: A=19.6%, B=7.2%). Vocabulary Jaccard: A↔Astro=0.046 > B↔Astro=0.033. However, -ey=15.2% and -eey=11.3% are anomalously above B levels (possibly a circular ring text format effect). Of 11 suffixes tested, 5 are intermediate between A and B, 3 are above B, 2 are at A level or below. The astro/cosmo section appears to be a distinct morphological register with strong A-adjacency, consistent with Hand 4 being a scribe with A-dialect morphological habits writing in the Currier B character set.
**Limitation:** 471 tokens is a small sample — all statistics have high variance. Hand 4 also writes circular ring text, which constrains word selection by spatial fit and may inflate -ey/-eey (short, space-efficient suffix). Jaccard distances are affected by type count and sample size.

## F053: Labels Are Formulaic (Distinct Register), Not Folio-Specific Content Annotations
**Experiment:** exp_046_label_body_correlation
**Date:** 2026-04-09
**Finding:** Of 30 folios with ≥3 label tokens AND ≥30 body tokens, 18 (60%) have zero vocabulary overlap between their label layer and body text layer. The 12 with above-chance overlap (40%) are primarily bio (mean ratio=7.10) and astro (6.04), and the shared words are exclusively 'o'-prefix forms (okaiin, okain, oteedy, olkeedy, etc.) — a morphological relationship (the 'o' label morpheme from F044), not a content relationship. Pharma labels (15 folios, Lf locus) have median ratio=0.00 — completely formulaic across the section. This means labels are NOT naming the illustrated objects in the same terms used in body text; they are a distinct linguistic register with its own vocabulary. The label-body register separation extends the finding from F007 (labels have higher h2 and 55.3% exclusive vocabulary) and F009 (daiin absent from labels) to the within-folio level.
**Limitation:** Only 30 folios have both sufficient labels and body text. The Lz (zodiac, 299 entries) locus was only partially parsed — zodiac month name entries may be in non-standard format. The threshold (≥3 label tokens, ≥30 body tokens) excludes most herbal folios (too few labels after L0 contamination correction).

## F054: Section Explains Morphological Variance Better Than Quire; Pharma Has Distinctive -ol Signature
**Experiment:** exp_047_quire_morphology
**Date:** 2026-04-09
**Finding:** For all four morphological features tested (qo-rate, -edy, -ol, -aiin), section assignment explains more between-group variance than quire assignment (Section F-ratios: qo=1.35, -edy=2.07, -ol=0.86, -aiin=0.40; Quire F-ratios uniformly lower). The apparent quire signal largely reflects that some quires (especially quire M, n=20 folios) correspond closely to a single section (bio). Within-quire variance is high (std≈0.05 for qo-rate), confirming quires are morphologically heterogeneous. Notable section-level finding: the pharma section (P) has -ol=18.5% — the highest of any section — while its -edy=0.3%, establishing a distinct pharma morphological signature (high -ol, near-zero -edy) not previously isolated. Bio continues to show extreme B-type markers (qo=26.1%, -edy=20.6%).
**Limitation:** The $Q= field in IVTFF encodes quire letters (A–T), but the mapping from these letters to physical quire numbers in the manuscript is not verified. Some quire letters may span non-contiguous physical quires. Variance decomposition is a simple F-ratio analog (no ANOVA), so statistical significance is not computed.

## F055: 'o'-Label and 'qo'-Body Morphemes Are Parallel Prefixes on the Same k/t-Initial Stem Class
**Experiment:** exp_048_o_label_qo_stem_overlap
**Date:** 2026-04-09
**Finding:** 10/13 (76.9%) of frequent o-initial label stems also appear as qo-stems in Currier B body text. Both morphemes select from the same k/t-initial stem class: o-labels 66.5% k/t-initial, qo-body 82.5% k/t-initial. The stem-in-free-vocabulary rate is ~43% for both morphemes (o-stems: 43.1%; qo-stems: 42.0%), confirming both draw from the same underlying vocabulary pool. qo- and o- are in complementary functional distribution: qo- marks body-text register (4 qo-words in 807 label tokens — essentially absent from labels), while o- marks label register. Combined with cth- (F047: selects o/y/e-initial stems in Currier A), the morphological system has at least three confirmed prefix morphemes: (1) qo- [Currier B body, k/t stems], (2) o- [labels, k/t stems], (3) cth- [Currier A, o/y/e stems]. The qo-≈o- symmetry on identical stems suggests the prefix encodes register (body vs label), not semantic content — the same k/t-initial stem can appear free, as qo+stem (body), or as o+stem (label).
**Limitation:** The o-stem freq≥2 set is only 13 items (label corpus is small: 807 tokens, high TTR). The stem overlap result is robust but directional — most frequent o-stems appear in qo-stems; whether most frequent qo-stems appear in o-stems cannot be established from the data.

## F056: Lag=13 Word Autocorrelation Is Folio-Specific (f75v, f82v, f84v), Not Section-Wide in Bio
**Experiment:** exp_049_bio_lag13_autocorr
**Date:** 2026-04-09
**Finding:** Of 19 bio-section folios with ≥50 tokens, 3 (f75v=2.22, f82v=2.17, f84v=2.30) have lag=13 word autocorrelation ratio >2.0; the bio section mean is 1.00 (at baseline); 9/19 bio folios have ratio <1.0. The effect is not systematic across bio but is concentrated in the "bathing pool" folio subset (f75v–f84v range). Herbal section: max lag=13 ratio = 1.38, 0/28 above 2.0. The bio vs herbal comparison shows bio has more variance and higher maximum, but the mean lag-13 ratio is not elevated in bio as a whole. The three folios with high lag=13 ratios may share vocabulary structure from the pool scene content, creating local repetition patterns at 13-word intervals.
**Limitation:** Testing 20 lags × 19 folios = 380 comparisons with no multiple-testing correction. The 3/19 rate at lag=13 specifically is consistent with chance in a high-dimensional test. Without a specific a priori prediction for lag=13 (the finding emerged from exp_042), the evidence is suggestive rather than conclusive.

## F057: Currier A 'd'-Stem Words Are Line-Final Markers; -ol/-or Words Are Excluded from Line Endings
**Experiment:** exp_050_daiin_positional
**Date:** 2026-04-09
**Finding:** In Currier A, the 'd' stem paradigm dominates line-final positions: dam=62.5% line-final (3.92× above baseline), dy=49.2% (3.09×), dal=35.5% (2.23×), daiin=22.5% (1.41×), with the entire -aiin suffix class at 20.2% line-final (1.27×). In contrast, -ol/-or words (chol=0.9% final, shol=1.0% final, chor=4.1% final) are almost entirely excluded from line endings — a factor of 4–18× below baseline. The 'd' stem collectively functions as a line-terminating element in Currier A, while chol/shol/chor/shor are strictly mid-sentence or line-medial. This creates a strong positional complementary distribution: 'd'-stem words at line endings, -ol/-or words avoiding them. This parallels the Currier B positional biases from exp_038 (-aiin line-initial, -edy medial) but using a different structural mechanism (stem identity in A vs suffix class in B). Note: B's -ain words are NOT line-final elevated (8.5% last, below baseline), so daiin and -ain are not functional parallels — the parallel is between d-stem positional role in A and suffix-class positional roles in B.
**Limitation:** Line-final position in IVTFF may include paragraph-final (=Pt) and mid-paragraph line endings. These were not distinguished. The positional analysis treats all P0/Pt lines uniformly.

## F058: Pharma -ol Dominance Is Driven by a `-eol` Suffix Variant; Sections Have Paradigm-Level Specialization
**Experiment:** exp_051_pharma_ol_signature
**Date:** 2026-04-09
**Finding:** The pharma section's -ol+or rate of 30.1% (vs herbal 20%, bio 13.3%, special 8.6%) is primarily driven by a pharma-specific `-eol` suffix variant: cheol (5.7× herbal rate), okeol (13.6×), qokeol (15.4×), sheol (4.0×), qockhol (28.1×), sheeol/qokeeol/qoeol (pharma-exclusive). These are known stems (ch, ok, qok, sh) with `-eol` rather than plain `-ol`. The `-eol` suffix variant is NOT in the original 9-form paradigm list — it represents an additional pharma-specific paradigm slot. The -ol elevation is broadly distributed (122 unique -ol types; top-5 account for 36.4%, similar to herbal's 39.1%). Pharma LABELS do not show -ol preference (7.8% vs 19.7% body) — ruling out -ol as an ingredient-naming morpheme. Labels have 32.2% no-suffix words (vs 0% in body). Completing the paradigm section map: pharma→-eol/-ol, bio→-edy, special→-aiin, herbal→balanced. Different sections preferentially use different suffix paradigm slots from a shared underlying system.
**Limitation:** The `-eol` pattern is observed but not explicitly tested as a suffix — it's parsed as stem+`e`+`-ol`. A dedicated `-eol` suffix test with KL analysis would confirm whether this is a true suffix unit or a stem-level phenomenon.

## F059: Stem-Class Suffix Distinction Is Between-Dialect, Not Within-Dialect; cth- Is a Stem, Not a Prefix
**Experiment:** exp_052_prefix_stem_class_distinction
**Date:** 2026-04-09
**Finding:** KL(qo-class || cth-class) = 4.726 bits — 8× the overall A/B dialect divergence (0.586 bits). The k/t-initial stems (qo-selected, B) strongly prefer -edy/-eedy/-ain/-aiin; the o/y/e-initial stems (cth, A) strongly prefer -y/-ol/-or/-ey. However, this is a between-dialect effect: within Currier B, all stem classes (qo-stems, bare k/t, other words) use B-type suffixes with similar distributions (KL ≈ 0.15 bits between stem groups). The dialect (A vs B) determines suffix paradigm, not the stem-initial class independently. Structural finding: 'cth' IS the stem root itself (not a prefix) — it takes A-type suffixes directly: cth+y, cth+ol, cth+or, cth+ey. 'cth' is one of the paradigm-taking stems in Currier A alongside ch, sh (which, per exp_040, use A-type suffixes in A and B-type suffixes in B). The cth-stem strongly favors -y (29.8% vs 14.9% for bare o/y/e words) and suppresses -aiin (5.5% vs 13.6%) within Currier A, showing it has a distinctive within-A profile.
**Limitation:** The "qo-" prefix analysis treats qo-words as a class; the distinction between qo-words and bare k/t words within B may reflect different registers rather than a stem-class grammatical distinction.

## F060: Currier A Has a Partial Line Grammar: y-Initial Words and -or as Line-Initial Markers; -dy/-al as Line-Final
**Experiment:** exp_053_a_line_structure
**Date:** 2026-04-09
**Finding:** Currier A positional grammar: (1) -or suffix is line-initial dominant (1.66×, 26.4% first); 'y-'+ch words (ychor=5.83×, ycheor=5.49×, ychol=5.38×, ycheey=6.27×) are the strongest line-initial markers — 'y' appears to function as a line-initial particle. (2) 30% of A lines open with [or-word][ol-word] as the first two words. (3) Line-final slot: -dy (1.59×), -al (1.35×), -ain (1.45×), and '-am' words (dan/dom/sam at 6.27×, dam at 3.92×). (4) -ol and -ey/-eey are strictly medial (~80%+). (5) -ain has above-baseline rates at BOTH edges (1.30 first, 1.45 last), unlike other suffixes — possibly a sentence-boundary marker. Currier B contrast: both -or (1.84) and -ol (1.46) are line-initial in B; -aiin is line-initial in B (1.50) but line-final in A (1.27); -dy avoids both edges in B (0.83/0.70) but is line-final in A (1.59). The A/B positional grammar is structurally different: A has a clearer slot structure while B has more uniform suffix distribution across positions.
**Limitation:** Line-initial in IVTFF includes both paragraph-start (@P0) and continuation (+P0) lines — paragraph-start vs regular line effects are not separated. The 'y-' initial enrichment analysis has small counts (6-13 per word); pooled 'y+ch' analysis would strengthen the finding.

## F061: 'y-' Is a Line-Continuation Particle; -dy Marks Paragraph Starts; -aiin Marks Paragraph Ends
**Experiment:** exp_054_y_prefix_paragraph
**Date:** 2026-04-09
**Finding:** The 'y-' prefix is a line-CONTINUATION marker, not a paragraph-start marker: 0/134 Currier A paragraph starts begin with a y-initial word (vs 16.3% of continuation lines); in B, 3.8% para-starts vs 14.2% continuations. Paragraph-start markers in Currier A: -dy suffix words appear 4.39× more at paragraph-start first positions than at continuation-line first positions; -y words appear 1.76× more at para-starts than continuations. Paragraph-end markers: -aiin words appear at 19.5% of A paragraph-end last positions (vs 14.4% overall = 1.35× enriched); same effect in B (10.5% para-end vs 8.1% overall = 1.30×). -ain words strongly avoid paragraph starts (A: 0.25× enrichment, B: 0.30× enrichment). This establishes a three-tier positional grammar in Currier A: (1) paragraph-start → -dy or -y suffix words; (2) within-paragraph line-start → y-initial, -or suffix words (the line-continuation slot); (3) paragraph-end → -aiin suffix words. The 'y-' line-continuation function also appears in Currier B, suggesting this is a manuscript-wide feature, not A-specific.
**Limitation:** "Para-start" (@P0) and "para-end" (=Pt or <$> marker) counts are small (A: 134 para-starts, 236 para-ends). The -dy paragraph-start enrichment (12.7% vs 2.9%) rests on only 17 -dy words at para-starts. The result is strong directionally but would benefit from larger-sample confirmation.

## F062: Lag=13 in Pool Folios Is Statistical; y-Initial Rate Varies by Section (Astro=23.2%, Bio=7.5%)
**Experiment:** exp_055_bathing_pool_phrases
**Date:** 2026-04-09
**Finding:** H059 NOT SUPPORTED: The lag=13 signal in f75v, f82v, f84v is from high-frequency bio words (qokain, ol, shedy, qokedy) repeating by chance; cross-folio bigram sharing (2-8 bigrams per pair) is indistinguishable from other bio pairs. No distinctive shared phrase template. H063 PARTIALLY SUPPORTED: y-initial first-word rates vary by section: astro=23.2%, pharma=17.9%, special=16.6%, herbal=14.7%, text=14.6%, bio=7.5%, cosmo=7.5%. Since y-initial marks line-continuation position (F061), sections with higher y-initial rates have longer paragraphs; bio's low rate (7.5%) is consistent with bio having short formulaic paragraphs (also consistent with bio being the most phrase-repetitive section: exp_043). Per-folio outliers: f6v (38.1% y-initial, extreme continuation structure), f49r (0% y-initial, 0 continuation markers). The inverse correlation between bio formulaicity (highest: exp_043) and y-initial rate (lowest: exp_055) is the strongest evidence that bio text is organized as short repeated units rather than long flowing prose.
**Limitation:** Astro section has only 56 lines (small sample). The y-initial section correlation reflects the combination of Currier (A vs B) and section effects — astro folios are mostly Currier B despite their A-like morphology (exp_045), which may affect y-initial usage.

## F063: Voynichese Word Template Is Probabilistic: Onset × Suffix Preferences Are Modest (KL 0.01–0.32 Bits)
**Experiment:** exp_056_word_template
**Date:** 2026-04-09
**Finding:** Cross-tabulation of onset class × suffix class shows non-independent but modest deviations from independence (KL=0.01–0.32 bits). The 'd' stem is most strongly templated (KL=0.324 bits in A, 0.254 in B), primarily from d+aiin being 2.69×/2.16× over-represented. qo+eedy is 2.05× over-represented in B (qo- words prefer extended -eedy). No categorical onset-suffix exclusions exist. Top 6 onset-classes × top 6 suffix-classes account for 48-54% of the corpus; top 20 combos account for 46-51%. The word template is probabilistic (onset-sensitive suffix preferences) not categorical (rigid slot-filling). Most onset classes have KL 0.01–0.09 bits from independence — the template constraint is weak at this level of analysis. The system is consistent with a productive morphological grammar (F048: log-linear stem-frequency vs paradigm completeness r=0.83-0.89) with mild onset-driven suffix preferences.
**Limitation:** The 'other' onset category (25.6% of B tokens) is heterogeneous — it mixes words starting with t, k, f, p, s, r, etc. Disaggregating 'other' might reveal additional template structure. The analysis treats each token independently (no context window).

## F064: Currier A and B Share Paragraph-Grammar System but Use Different Marker Morphemes
**Experiment:** exp_057_b_para_start_markers
**Date:** 2026-04-09
**Finding:** H064 PARTIALLY SUPPORTED. Both dialects mark paragraph starts, suppress y-initial words at those positions, and use -dy as a (weak) para-start indicator — but with different strength and different primary markers. Currier A: -dy is the dominant para-start marker (3.36×); y-initial is completely absent at A para-starts (0/134, 0.00×). Currier B: -dy is only weakly enriched at para-starts (1.53×); stronger B para-start markers are -chy (2.94×) and -ar (2.11×). y-initial is strongly but not completely suppressed in B para-starts (5/130 = 3.8% vs 13.6% baseline = 0.28×). B-specific para-start suppressions: -aiin (0.37×) and -ain (0.31×) are strongly avoided at B para-starts — a feature absent in A (where -aiin is at baseline 0.96× at para-starts). B para-start words are more formulaic than A, clustering around p-/t-onset forms (pchedar ×3, tchedy ×3, pchedal ×2). These p/t-onset formulaic words are rare in the general B corpus (0.4-0.9% overall vs 1.5-2.3% at para-starts = 3-7× enrichment). The two dialects share a paragraph-grammar type (position-sensitive morphological marking) but implement it through different specific morphemes. This is consistent with a shared underlying grammar with dialect-specific lexical encodings.
**Limitation:** Para-start sample sizes are small (A: 134, B: 130). The -dy enrichment in A rests on 17 tokens; B on 10. The -chy and -ar B findings (7 and 23 tokens respectively) are more robust. The locus parsing of @P0 as para-start may miss some para-starts that use different locus notation.

## F065: All Currier A Herbal Folios Are Single-Paragraph; y-Initial Rate Variation Is Folio-Level, Not Paragraph-Length-Driven
**Experiment:** exp_058_f6v_paragraph_structure
**Date:** 2026-04-09
**Finding:** H065 NOT SUPPORTED. Every Currier A herbal folio (75/75 with ≥10 lines) has exactly 1 paragraph (1 para-start per folio). Since paragraph length = folio length for all herbal A folios, the y-initial rate variation (0% to 38.5%) cannot be explained by paragraph structure. f6v (38.1%, rank #2) is within the normal range of high-y herbal folios; f53v is higher (38.5%). The distribution appears bimodal: ~30 folios in a high-y cluster (20-38%) and ~12 folios with 0% y-initial (f49r, f8v, f32r, f32v, f35r, f42v, f45r, f47r, f47v, f13r, f20r, f22r, f30v, f4r, f7r). The zero-y-initial group spans different quires and positions, suggesting this is a scribal-hand or content-sub-category property rather than a positional artifact. The bimodal distribution is inconsistent with a single uniform scribal convention applied to all herbal A text.
**Limitation:** Para-start detection relies on @P0 locus prefix; if some folios use a different locus notation for paragraph boundaries, their para counts would be underreported. The herbal A folio population in this analysis includes both main herbal (H) and any mislabeled folios — section tagging was from the $I= field which may not be 100% consistent. Zero-y-initial folios may overlap with folios that are shorter or have unusual line counts.

## F066: Two-Register System within Currier A Herbal: y-initial vs aiin-dominant Folios
**Experiment:** exp_059_a_grammar_violations
**Date:** 2026-04-09
**Finding:** H066 SUPPORTED. Six Currier A herbal folios violate the canonical line grammar by having near-zero y-initial continuation rates: f49r (0%), f32r (0%), f8v (0%), f42v (0%), f35r (0%), f42r (4.5%). All violations are in the Herbal section — Special, Pharma, and Text sections show no violations. The violating folios show compensatory elevated -aiin rates at line endings: f35r (53.3%), f8v (35.3%), f42v (25.0%), f32r (21.1%), f49r (19.0%) — compared to the herbal mean of ~15%. This negative correlation (low y@cont, high aiin-last) suggests a two-register system within herbal A: a y-initial-dominant register (f6v=40%, f24v=33%, f51r=36% y@cont with low aiin-last) and an aiin-dominant register (f49r, f32r, f8v, f42v, f35r: 0% y@cont with elevated aiin-last). The two registers may correspond to different scribal hands or different herbal content categories. f6v is the only high outlier (y@cont=40%, mean+2sd threshold). f35r is the most extreme bidirectional violator (0% y@cont AND 53.3% aiin-last). The grammar is internally consistent within each folio — violations are folio-level, not line-level noise.
**Limitation:** Per-folio sample sizes are small (15-23 lines). The two-register identification is based on the tail of the distribution; the 6 violators may simply be the low end of a continuous distribution rather than a discrete register. No scribal hand data was consulted — the hypothesis that this reflects different scribal hands requires external validation.

## F067: daiin and y-Initial Are Competing Line-Continuation Strategies; Aiin-Dominant Herbal A Folios Cluster in Quires D and F
**Experiment:** exp_060_daiin_yinit_quire
**Date:** 2026-04-09
**Finding:** H069 PARTIALLY SUPPORTED: daiin rate is negatively correlated with y-initial rate across herbal A folios (r = -0.297). Aiin-dominant herbal folios have mean daiin = 6.88% vs y-dominant folios = 3.50% (2× higher). This suggests daiin and y-initial are competing line-continuation encoding strategies: the aiin-dominant register uses -aiin endings (including the specific word daiin = d+aiin) where the y-dominant register uses y-initial words. H072 PARTIALLY SUPPORTED: Aiin-dominant folios cluster in Quires D (3/6 = 50%) and F (5/8 = 62%), while Quires B, O, Q have zero aiin-dominant folios. This quire-level clustering is consistent with a scribal-hand hypothesis (different scribes for different quires using different grammatical conventions). However, within Quire F, f44r and f44v are y-dominant exceptions, suggesting the hand boundary is not perfectly quire-aligned. The two-register system (aiin-dominant vs y-dominant) likely reflects scribal hand variation overlaid with content variation. Both the grammatical (competing continuation strategies) and structural (quire clustering) evidence point toward the same conclusion: the herbal section was written by multiple scribes with different positional grammar conventions.
**Limitation:** The quire assignments come from the $Q= header field in ZL3b, which may not perfectly reflect physical quire boundaries. The r=-0.297 correlation, while real, is not strong — other factors drive y-initial rate variation. The "competing strategies" interpretation is structural; it doesn't directly address which strategy maps to which linguistic function.

## F068: Paragraph Count Mirrors Content Organization; Currier B Has 4 Onset Classes, Not 8
**Experiment:** exp_061_section_para_onset
**Date:** 2026-04-09
**Finding:** H071 SUPPORTED: Single-paragraph structure is NOT herbal-specific — it characterizes ALL content-organized sections: Herbal (100%), Special (100%), Text (100%). Multi-paragraph structure characterizes technical/reference sections: Pharma (75%), Cosmo (71%), Astro (50%), Bio (37%). Bio's multi-paragraph folios are specifically the bathing pool sub-section (f75v, f82r, f83r, f83v, f84r, f84v — pool scenes with multiple illustrated figures per page). Pharma multi-para folios (f99r, f99v, f88r etc.) are consistent with recipe-book organization. Astro f67r2 has 13 para-starts in 35 lines — the most structurally complex folio in the manuscript. Paragraph count is a direct indicator of page content complexity. H070 SUPPORTED: k-initial and t-initial words in Currier B have KL=0.082 bits (nearly identical suffix distributions), confirming they are the same onset class. sh and ch are also one class (KL=0.062 bits). Currier B's effective onset taxonomy collapses to 4 classes: (1) {ch/sh}: high -y/-edy/-ey; (2) {k/t/p}: balanced distribution, moderate -dy; (3) {d/s}: aiin-dominant (s: 20.6% -aiin, d: 20.8%); (4) {qo}: extended-form dominant (-eedy=10.9%, -eey=9.1%, -ain=9.6%). This 4-class taxonomy is consistent with all prior onset analysis (qo- selects {k/t} class; cth- in A selects {o/y/e} class). The `s`-initial class being aiin-dominant alongside d is a new finding — s-words may encode a similar grammatical role to d-words in Currier B.
**Limitation:** The 4-class taxonomy is based on suffix KL in Currier B only; Currier A onset structure was not separately analyzed. The `other_misc` category (12.2% of B) contains mixed characters that were not disaggregated. The para-start counts per folio may undercount multi-paragraph structure if some folios use alternative locus notation for paragraph boundaries.

## F069: Two Herbal A Sub-Dialects with Vocabulary Jaccard = 0.138 (Near A/B Inter-Dialect Gap)
**Experiment:** exp_062_two_register_vocab
**Date:** 2026-04-09
**Finding:** H068 STRONGLY SUPPORTED. The aiin-dominant herbal A folios (Quires D/F cluster) are lexically distinct from y-dominant folios at near-dialect level: vocabulary Jaccard = 0.138 (cf. A/B Jaccard = 0.148, F013). Key differences: (1) y-initial words are globally suppressed in aiin-dominant (2.0% vs 9.3% overall = 0.21×) — not just at line-starts. (2) d-onset words are 1.61× enriched in aiin-dominant; ch/sh onsets 1.50-1.52× enriched. (3) o-onset words are 0.63× in aiin-dominant. (4) chaiin is 11.75× over-represented in aiin-dominant; daiin 2.01×, dain 3.58×. (5) y-dominant exclusive: ychor (3964×), ykchy (3398×), odaiin (7.02×), or (4.04×). (6) 447 aiin-exclusive types, 781 y-exclusive types. The vocabulary difference extends beyond positional grammar to the entire word inventory. Combined with quire clustering (Quires D/F aiin-dominant) and competing continuation strategies (y-initial vs -aiin), this constitutes near-evidence of a distinct scribal tradition within Currier A Herbal — possibly a different scribe with an alternative morphological convention for encoding the same underlying grammatical categories.
**Limitation:** The Jaccard comparison is between two sub-corpora within the same dialect/section; it's possible the low Jaccard reflects sample size effects rather than genuine lexical divergence. The aiin-dominant corpus (1127 tokens) is smaller than the y-dominant corpus (1766 tokens), which could inflate the exclusive-type counts. However, the specific vocabulary patterns (y-onset 0.21× globally, chaiin 11.75×, 'or' 4.04×) are consistent and directionally strong.

## F070: Currier B Marks Paragraph-Starts with p-Onset Class (17-18×); Currier A Marks Them with -dy Suffix (3.36×)
**Experiment:** exp_063_pch_tch_onset
**Date:** 2026-04-09
**Finding:** H073 SUPPORTED. pch-initial words in Currier B are 17.19× enriched at paragraph-starts (18/130 B para-starts). tch-initial: 10.81×. The broader p_other (non-pch p-onset) is even more enriched (18.21×). All pch/tch words are almost exclusively line-initial (4.4%/3.0% line-first; 0.1% line-last) and completely absent from labels (0/781). Most common forms: pchedy (29 tokens), tchedy (28) — both pch/tch + -edy. These words show a distinctive suffix preference for -edy (pch: 19.0%, tch: 25.2% vs B marginal 12.8%). The p-onset class in Currier B functions as the paragraph-opening structural marker. Structural comparison: Currier A marks paragraph-starts with -dy suffix (3.36×) while Currier B marks them with p-onset (17-18×). The dialectal difference in positional grammar is: A uses suffix-class marking, B uses onset-class marking for the same structural function. This directly confirms and extends F064 (B para-start -chy and -ar enrichment were weaker signals from the same system; p-onset is the dominant marker). The complete label absence confirms p-onset is a structural/positional marker, not a content vocabulary item.
**Limitation:** The 130 B para-starts sample is small. The 17× enrichment is computed over para-start first-words, which may be partially explained by rare overall frequency (pch=0.81% of all B words). The baseline rate (all-corpus word frequency) is the correct denominator for position enrichment, so the 17× figure stands. However, the interpretation "B marks para-starts with onset class" should be verified with a larger para-start sample if available.

## F071: Complete Currier B Onset Positional Grammar; p-Onset Is Cross-Dialect Para-Start Marker
**Experiment:** exp_064_s_d_positional
**Date:** 2026-04-09
**Finding:** H075 PARTIALLY SUPPORTED: p-onset enrichment at para-starts is cross-dialect (A: 7.38×, B: 2.80× overall). y-initial suppression at para-starts is also cross-dialect (A: 0.00×, B: 0.28×). The "B-specific two-marker system" is a pan-Voynichese feature. H074 NOT SUPPORTED: s-initial and d-initial have the same suffix profile (both aiin-dominant: ~20.7% -aiin) but DIFFERENT positional grammar — s is 4.61× line-first biased (exclusively), while d is biased at BOTH edges (2.43× first, 1.42× last). H076 (partially) SUPPORTED via the same data: Currier B onset classes have a complete positional grammar: p (6.34× line-first = para-start); s/y/t (3-5× line-first = continuation/opener class); d (2.43× first AND 1.42× last = edge-adjacent, appears at both line edges); ch/sh (0.17-0.42× first = medial, strongly avoid line openings); qo (0.64× first = slightly medial); o (1.24× last = slightly line-final biased); k (baseline). Top s-words in B: saiin (80), sain (53), sar (40), sol (30), sal (25), sor (24) — all s+simple-suffix forms, occurring at line openings. The 4-class onset taxonomy from F068 ({ch/sh}, {k/t/p}, {d/s}, {qo}) does NOT map cleanly onto positional grammar — s and p are in the same suffix class ({k/t/p}) but have very different positional roles (s=4.61× line-first, p=6.34× line-first, k=0.66× below baseline line-first).
**Limitation:** The positional analysis treats all continuation lines as equivalent, but line-FIRST and line-LAST are both "first/last words per line" which includes very short lines (2-word lines have the same word as first and last). This inflates positional enrichment for rare words. The correction would require filtering to lines with ≥4 words for reliable first vs last distinction.

## F072: Herbal A Two-Register System Is Intra-A Variation, Not B-Dialect Intrusion
**Experiment:** exp_065_aiin_dom_b_proximity
**Date:** 2026-04-09
**Finding:** H077 NOT SUPPORTED. The aiin-dominant herbal A sub-dialect is NOT closer to Currier B than to standard Currier A. Vocabulary Jaccard: aiin-dom A vs y-dom A = 0.138; aiin-dom A vs all B = 0.046; aiin-dom A vs herbal B = 0.087. Both A registers share the A suffix profile: -ol=14.2%, -or=9-12%, -edy<0.2% (cf. B: -edy=12.8%). The two herbal A registers are in the same Currier A morphological system, just with different emphasis on -aiin vs y-initial as continuation markers. The near-identical Jaccard values between (aiin-dom A vs y-dom A=0.138) and (all A vs all B=0.120) are coincidental — the within-A split reflects a vocabulary partition driven by which positional markers are used, not cross-dialect contamination. Both A registers have the characteristic A suffixes (-ol, -or, -chy) and lack the B-specific forms (-edy dominant, qo- prefix system). Only 2 words in aiin-dom A are absent from all of B (cthaiin, qotchol), confirming that the aiin-dom vocabulary is A-type (present in both dialects individually but without B-specific frequency pattern). The quire-clustered two-register system represents an intra-A scribal convention difference, not a dialect boundary.
**Limitation:** The Jaccard comparison is sensitive to corpus size. aiin-dom A has 643 types from 1127 tokens — a small corpus where many types are hapax. Expanding the aiin-dom corpus by including borderline folios might increase the Jaccard. The "herbal B" corpus is also relatively small (1435 types, 3064 tokens). The comparison would benefit from larger samples.

## F073: Word Length Is a Positional Signal (Para-Start=Longest, Last=Shortest); Registers Differ in Lexical Entropy Not Syntactic
**Experiment:** exp_066_word_length_position
**Date:** 2026-04-09
**Finding:** H081 STRONGLY SUPPORTED: Para-start first words are the longest in both dialects (A: mean=6.55, B: mean=7.15 chars); line-last words are shortest especially in B (mean=5.43); medial words are shortest overall (A:5.43, B:5.56). A gradient exists in B: para_start (7.15) > cont_first (6.09) > medial (5.56) > last (5.43). This is a THIRD type of positional encoding beyond onset class and suffix class — word LENGTH itself encodes position. The long para-start words correspond to the pch/tch compound onset forms (pchedar=7 chars, tchedy=6) while line-final words include short forms (ol=2, or=2, aiin=4, chy=3). H079 SUPPORTED (opposite direction): y-dominant herbal A has HIGHER unigram entropy (h1=9.180) than aiin-dominant (h1=8.488) because y-dominant spreads frequency more uniformly across more word types. Aiin-dominant is concentrated around daiin (6.48%), chol, shol. Both registers have nearly identical bigram conditional entropy (h2: 1.577 vs 1.566) — same sequential word-ordering grammar, different lexical frequency profiles. The difference between registers is LEXICAL (which words dominate), not SYNTACTIC (how words combine).
**Limitation:** Word length in EVA transcription may not equal true Voynichese grapheme count (some EVA digraphs like 'ch', 'sh' represent single glyphs). The positional analysis treats EVA char length as a proxy for glyph complexity, which introduces measurement noise. The comparison would be more precise with glyph-level counts. The entropy comparison is on small corpora (1127 vs 1766 tokens) — the h1 difference (0.692 bits) may partly reflect sample size effects.

## F074: Bio Pool/Non-Pool Is Organizational, Not Linguistic; pch/tch Is a Universal B Positional Marker
**Experiment:** exp_067_bio_pool_quire
**Date:** 2026-04-09
**Finding:** H082 NOT SUPPORTED: Bio pool folios (f83r, f84v, f75v, f75r, f82r, f83v, f84r) vs non-pool folios show Jaccard=0.201 — substantially HIGHER than the herbal A intra-register split (0.138). Suffix profiles are nearly identical (no suffix class differs by >1.5×): pool -edy=22.9% vs non-pool -edy=18.6%; qo-rates 26.8% vs 25.7%. Word-level differences are in low-frequency hapax-like forms. The multi-paragraph structure of pool folios is an organizational feature (grouped bathing scenes), not a linguistic register boundary — unlike the herbal A two-register split which reflects a deep morphological convention difference. H080 NOT SUPPORTED: pch/tch onset words are distributed across all Currier B quires without dramatic clustering. Combined pch+tch rates range 0.58% (Quire I) to 2.36% (Quire D) — only ~4× variation, far below the aiin-dominant A clustering (62% of Quire F folios). pch/tch is a manuscript-wide B positional grammar convention, not a quire-specific scribal feature. Per-quire pch vs tch split shows some variation (Quire Q: tch=1.86% vs pch=0.41%; Quire D: pch=1.77% vs tch=0.59%) that may reflect individual scribes using pch or tch as their preferred para-start opener within the shared p-onset class.
**Limitation:** Small quire counts for D (339 tokens), G (374), I (346), J (125) make per-quire percentages noisy. The D quire pch/tch rate (2.36%) may be elevated due to sampling variance. The pool/non-pool vocabulary comparison is done within the Bio section — comparing across sections might show stronger differentiation.

## F075: Bio Paragraphs Share Structural Vocabulary; qo is a Gallows-Prefix Class Complementary to p-Onset
**Experiment:** exp_068_bio_para_qo
**Date:** 2026-04-09
**Finding:** H083 PARTIALLY SUPPORTED: Within-folio bio paragraph Jaccard for non-trivial paragraph pairs (≥50 tokens each) is 0.075–0.156 — comparable to the cross-folio baseline of 0.155 (std=0.018). Paragraphs within the same multi-para bio folio share the same high-frequency Currier B structural vocabulary (qokain, qokedy, shedy, chedy). Some multi-para folios (f83r, f84v) have one large main paragraph + tiny marginal annotations (4–16 tokens) that drive the mean down to 0.060. Bio paragraphs do not represent sharply distinct vocabulary domains. H084 STRONGLY SUPPORTED: qo is a PREFIX class that attaches to gallows letters (k: 62.6%, t: 19.9%, p: 3.3%, f: 0.7%) in 86.5% of cases. The qo+gallows+suffix construction (top words: qokeedy, qokain, qokedy, qokeey, qokaiin) represents 18.6% of all Currier B words. Morphological properties: (1) suppressed at para-starts (0.12× — directly opposite p-onset's 17-18×); (2) medially biased (1.12× enriched); (3) prefers extended suffixes (-eedy: 2.05×, -ain: 1.61×, -eey: 1.50×); (4) avoids suffix-free forms (0.51×); (5) is section-sensitive: Bio=26%, Astro=6.5%. The qo and p-onset classes occupy complementary positional niches: p-onset marks paragraph openings, qo+gallows marks medial position.
**Limitation:** The paragraph-start detection relies on '@' prefix in locus codes; tiny "paragraphs" of 4-16 tokens may be marginal annotations, not true paragraph breaks. The qo section distribution analysis treats all B records equally regardless of transcription quality variation by section.

## F076: ch/sh Morphologically Distinct; Gallows k/t/f/p Have Four Distinct Positional Niches
**Experiment:** exp_069_ch_sh_gallows
**Date:** 2026-04-09
**Finding:** H085 SUPPORTED: ch and sh are NOT interchangeable. sh is more line-initial (A: 11.2% vs ch 3.9%; B: 5.0% vs 2.1%); ch is more line-final (A: 13.7% vs 8.8%; B: 10.6% vs 5.0%). In B, ch takes short suffixes (-aiin: 1.87×, -ain: 1.69×, -al: 1.66×, -ar: 1.56×) while sh takes extended suffixes (-edy: 1.31×, -eedy: 1.93×). sh follows p-onset words at 4.1× the rate of ch — sh is the secondary opener in p-onset paragraphs. Both show self-following repetition (ch after ch: 1.52-1.63×; sh after sh: 2×). Section variation: B Bio section has sh=48% of ch+sh (vs Special=30.7%). Mean length: ch=5.88, sh=5.53 in B. H086 STRONGLY SUPPORTED: The 4 Currier B gallows letters occupy distinct positional niches: p=primary para-start marker (17.76×, 75.3% first), t=secondary line-opener (7.64× para-start, 3.82× line-first), f=rare tertiary marker (8.04× para-start, 1.90× line-first, only 62 tokens), k=medial gallows (1.05× medial, 0.66× line-first) with -dy suffix preference (13.9% = 2.14× baseline). The {k/t/p} suffix class taxonomy from F068 correctly groups morphological similarity but incorrectly implies positional equivalence. Key refinement to the working model: k is a MEDIAL gallows (not a line-first gallows like t and p); the 4-class onset taxonomy needs splitting into 5 classes: {ch/sh} (medial), {p} (para-start), {t/f} (line-opener), {k} (medial-gallows), {d/s} (continuation-class).
**Limitation:** f only has 62 tokens in B — the para-start enrichment (8.04×) may be noise from small sample. The k para-start enrichment (4.88×) is surprising and may reflect a different phenomenon: k words appearing in the first word of very short paragraphs. The left-context analysis for ch/sh is limited to words on the same line; cross-line context is not tracked.

## F077: A Has ch-ch Bi-Word Constructions; B Reveals qo+Gallows→ch Sequential Rule
**Experiment:** exp_070_kedy_particle_ch_bigrams
**Date:** 2026-04-09
**Finding:** H087 WEAKLY SUPPORTED: k-dy words (top forms: kchdy, keody — morphologically k+ch/sh+dy compounds) are slightly more line-final (1.43× vs k-other 0.95×) and follow gallows words (k: 2.79×, t: 2.63×). Not a strong grammatical particle. H088 SUPPORTED for A, NOT for B: Currier A ch-ch self-following is 1.34× enriched; "chol chol" (20 tokens) is the dominant bi-word construction; sh-sh is 1.46× enriched. In B, self-following is near-random (1.04-1.09×). New serendipitous finding: In Currier B, qo+gallows words (qokain=86, qokaiin=78) are the most common words BEFORE ch-onset words — more common than even daiin (74). Similarly, qo+gallows precedes sh-onset words at high rates (qokain=45, qokaiin=39). This establishes a sequential word-order rule in Currier B: qo+gallows (medial) → ch/sh (medial) → suffix closing, creating a three-part medial construction. The full B positional grammar is: [p-onset para-start word] → [qo+gallows medial] → [ch/sh medial] → [line-closing word].
**Limitation:** The sequential analysis treats all bigrams equally; cross-line bigrams are excluded (bigrams within a single transcription line only). The "chol chol" A repetition (20 tokens) is concentrated in specific Currier A Herbal folios — it may be a scribal habit of a specific scribe rather than a grammatical construction. The B sequential rule (qo+gallows → ch) is based on frequency counts, not conditional probability controlling for overall ch frequency.

## F078: 5-Class Positional Taxonomy Stable Across B Sections; sh→qo (36.6%) Is Dominant B Transition
**Experiment:** exp_071_onset_taxonomy_sections
**Date:** 2026-04-09
**Finding:** H089 STRONGLY SUPPORTED: 5-class positional taxonomy is stable across all B sections. ch/sh: ALWAYS 0.00% para-first (all sections confirmed). p: 19-55× para-start enrichment in all sections (universally stable). qo: 0.00% para-first in all sections except Bio (0.37×). Section-specific amplifications: (1) Bio section uses k at para-starts at 12.00× vs Herbal 3.77× — k may be an additional Bio para-start marker. (2) Special section amplifies d/s/y line-first biases (s=6.26×, y=5.03×). H090 WEAKLY SUPPORTED: qo→ch enrichment is 1.13-1.70× across sections; strongest in Bio (1.63×) and Cosmo (1.70×); weak in Herbal/Special/Text (1.13-1.16×). The rule is section-sensitive, not universal grammar. Serendipitous: B-wide onset transition matrix reveals sh→qo=36.6% — the LARGEST single transition in the entire matrix (vs next: qo→qo=22.0%, qo→ch=19.6%). The sh↔qo coupling is tighter than qo→ch. Full B structural grammar prototype: [p (para-start)] → [o/sh (transition)] → [qo↔ch/sh alternation loop] → [closing]. Within the medial zone, qo and ch alternate (ch→qo=21.6%, qo→ch=19.6%); sh is sandwiched between qo words (sh→qo=36.6%).
**Limitation:** The transition matrix treats all word-pair adjacencies equally regardless of section or folio context. Cross-line transitions (last word of one line, first word of next) are included since lines are transcribed as single records. This could inflate some transitions if para-start markers (p-onset) tend to appear after specific line-ending words in the previous paragraph.

## F079: sh→qo Is a Universal B Grammar Coupling (~2×); A Has Flat Sequential Grammar with Weak sh→qo
**Experiment:** exp_072_sh_qo_coupling
**Date:** 2026-04-09
**Finding:** H092 STRONGLY SUPPORTED: sh→qo enrichment is 1.44-2.20× across ALL Currier B sections (1.81× Bio, 1.97× Herbal, 2.01× Special, 2.05× Text, 1.44× Cosmo, 2.20× Astro). The construction is: shedy/shey → qok+{aiin/ain/edy/eedy/eey} (top pair: "shedy qokedy" 18 tokens). sh is the strongest qo-predictor (36.6%, 1.97×); d suppresses qo-following (14.2%, 0.76×). This creates the B medial alternation: sh → qo → ch → qo → sh... H091/H093 SUPPORTED: Currier A has NO dominant predecessor class for ch. A's transition matrix is flat (max enrichment ch→ch: 1.34×). A has weak sh→qo coupling (1.56× vs B's 1.97×). Key A/B distinction: B uses qo as a sequential hinge (sh→qo→ch); A lacks this qo-hinge and has flat transitions. The ONLY A sequential structure is ch→ch self-following (1.34×), corresponding to the "chol chol" bi-word construction (F077). sh→ch is suppressed in A (0.80×), opposite to B where d→ch is suppressed (0.76×). Cross-dialect shared feature: both A and B have some sh→qo coupling, but at very different strengths.
**Limitation:** The transition matrix includes cross-line bigrams (last word of line i, first word of line i+1) since each record is one transcribed line. Cross-line transitions (which would include para-start words following the end of previous paragraphs) may inflate some transitions. The sh→qo analysis uses onset classes, not specific words — the actual coupling may be even stronger at the word level (shedy specifically → qok-forms specifically).

## F080: d/sh Are Complementary Sequential Classes; Medial Trigrams Are Near-Unique (Grammar Is Onset-Level, Not Word-Level)
**Experiment:** exp_073_medial_trigrams
**Date:** 2026-04-09
**Finding:** H094 STRONGLY SUPPORTED: d and sh are perfect sequential complements in B. sh→ch suppressed (0.64×), sh→qo enriched (1.97×). d→ch enriched (1.27×), d→qo suppressed (0.76×). s-onset also suppresses qo (0.57×). Two paths to ch in B medial grammar: (1) sh → qo → ch (indirect, via qo hinge); (2) d → ch (direct). After qo+ch, the next word is most often qo again (29.7%), confirming the qo↔ch alternation loop. After d: o(274), ch(231), sh(181), qo(172). H095 REFUTED AT WORD LEVEL: qo+ch trigrams are 99.4% unique (667 tokens, 663 types); qo+sh trigrams 98.6% unique. The sequential grammar operates at ONSET-CLASS level only — within each class, word choice is essentially free. This is structurally consistent with natural language: grammatical structure at category level, lexical freedom within categories. H096 NOT SUPPORTED: daiin specifically is not enriched as ch-predecessor (1.06× vs 19.8% baseline); the d→ch enrichment (~1.09-1.27×) is a class property uniformly distributed across all d-words.
**Limitation:** The near-uniqueness of trigrams (99.4%) may partly reflect the large vocabulary and small corpus size (21,605 B tokens). A larger corpus might show more repeated trigrams. The "two paths to ch" interpretation assumes d→ch and sh→qo→ch are independent pathways; they may co-occur in overlapping sequences.

## F081: A Has Weaker d/sh Complementarity (sh Complement Is s, Not d); B's Sequential Grammar Is Quantifiably Stronger; Line-Final Words Are Non-Random
**Experiment:** exp_074_grammar_model
**Date:** 2026-04-09
**Finding:** H097 SUPPORTED: d/sh complementarity is cross-dialect but weaker in A. A sh→qo=1.58× (vs B 1.97×), sh→ch=0.80× (vs B 0.64×), d→ch=1.09× (vs B 1.27×), d→qo=0.93× (vs B 0.76×). Critical A finding: in A, **s-onset plays the "d role"** — s→ch=1.36×, s→qo=0.63×. The complement of sh in A is s, not d. The A complementary structure is {sh vs s}: sh avoids ch (0.80×) and weakly prefers qo (1.58×); s prefers ch (1.36×) and avoids qo (0.63×). The d/sh and s/sh complementarity reflect the same underlying mechanism at different strengths across dialects. H098 SUPPORTED: A Laplace-smoothed bigram onset-class model reduces perplexity by 13.3% over unigram in B (PPL 8.092→7.012, 0.207 bits/bigram reduction) vs only 9.1% in A (PPL 8.758→7.957, 0.138 bits/bigram reduction). B's sequential grammar is quantifiably 35% stronger than A's. The ~3 bits/onset-token entropy is consistent with ~8 effective onset classes. H099 SUPPORTED: B line-final words are non-random: qo (0.61×) and sh (0.42×) are strongly suppressed at line-ends; o (1.25×) and d (1.50×) are enriched. The sh→qo coupling extends to line boundaries: sh as penultimate word predicts qo as last word (28.0%). d as penultimate word predicts o as last (30.4%). In A, d-onset strongly dominates line-finals (25.4%, 1.73×), consistent with the -aiin/-daiin line-end marker pattern.
**Limitation:** The line-final analysis uses the last word of each transcribed line, which may not correspond to sentence-final positions in the source text. The A s→ch enrichment (1.36×) is weaker than B's d→ch (1.27× in B) and may partially reflect A's overall flat transition matrix rather than a specific s-onset role. The bigram perplexity comparison is confounded by A having a smaller corpus than B, which affects smoothing constants.
