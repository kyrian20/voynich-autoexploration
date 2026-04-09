# Working Model — Voynich Manuscript Cryptanalysis
**Last updated:** 2026-04-09 (after exp_091)
**Purpose:** Continuously-updated structured summary of current beliefs about Voynichese.
**Discipline:** Characterization, not interpretation. Claims require experimental warrant.

---

## Tier 1 — High Confidence (Multiple Independent Experiments)

These findings have been replicated across independent analyses or confirmed by direct data inspection.

### 1.1 Morphological Structure

**qo- is a Currier B morphological prefix on k/t-initial stems (F037, F040, F041)**
- qo-stripped stems have H_initial = 1.931 bits (1.095 bits LOWER than non-qo words) — the prefix selects a constrained stem class
- qo-stems are dominated by 'k' (60.5%) and 't' (21.2%), sharply distinct from free-word onsets (o=25%, c=23%)
- qo-forms appear 88% in Currier B vs 11.6% in A; qo-normalization does NOT bridge A/B gap (Jaccard 0.152→0.153)
- qo is NOT a grammatical article (no complementary distribution with bare stems; no positional separability)
- 11/15 top B-exclusive qo-stems are absent from A vocabulary entirely

**'o' and 'qo' are parallel prefix morphemes on the SAME k/t-initial stem class (F043, F044, F055)**
- 58.4% of object labels (Lf/Ls/Ln/Lt) begin with 'o' vs 20.5% of body text
- 64.3% of o-initial labels have o-stripped stem in body vocabulary (otar→tar, otol→tol)
- Section-invariant 2.5–3.3× elevation in o-initial rate: rules out section vocabulary bias
- 10/13 (76.9%) of frequent o-stems also appear as qo-stems in Currier B body
- Onset distributions parallel: o-labels=66.5% k/t-initial; qo-body=82.5% k/t-initial
- Stem-in-free-vocab rate identical: o-stems 43.1%, qo-stems 42.0%
- Register distinction: qo- = body-text form; o- = label form (qo-words essentially absent from labels)
- Three-prefix system confirmed: (1) qo- [B body, k/t stems], (2) o- [labels, k/t stems], (3) cth- [A body, o/y/e stems]

**{y,n,l,r} cover 88.8% of all word endings (F042)**
- Top-4 word-final chars: y=41.1%, n=17.0%, l=15.7%, r=14.9%
- Top word-final bigrams: ...dy=18.6%, ...in=16.7%, ...ey=11.0%, ...ol=9.7% (top-7 cover 74.2%)
- Word-final H = 2.460 bits vs shuffled 3.86 bits (bias=1.48) — most constrained position in manuscript
- Directly matches Stolfi suffix template predictions

**Currier A and B share the same productive stems but select opposite suffix paradigms (F047, exp_040)**
- A has 349 multi-suffix stems; B has 639 — same structure, different scale
- SAME stems (ch, sh, ot, ok, qok, d, s) appear in BOTH dialects — but with near-inverted suffix preferences
- Stem 'ch': A prefers -ol/-or (225+146); B prefers -edy/-ey (430+208)
- Stem 'sh': A prefers -ol/-or (99+56); B prefers -edy/-ey (367+173)
- A's dominant suffixes: -ol (17.0%), -or (12.1%), -chy (5.1%)
- B's dominant suffixes: -edy (15.1%), -eedy (6.3%), -ain (7.0%)
- -edy is 75× more common in B than A; -ol is 2.8× more common in A than B
- cth- in A is a prefix morpheme structurally parallel to qo- in B: H_initial drops from 3.061 to 1.966 after stripping (nearly identical to qo-'s 1.931/3.027); selects o/y/e-initial stems (vs qo-'s k/t-initial stems)
- This reframes the A/B split: they share a morphological system but differ in which suffix dominates the paradigm

**The suffix paradigm is PRODUCTIVE in both A and B — log-linear r=0.83-0.89 (F048, exp_041)**
- Stem frequency (log scale) explains 69-79% of variance in paradigm completeness
- Singletons are sparse samples from a productive paradigm, not lexically fixed forms
- KL from marginal = 0.2-1.1 bits: "partially productive" consistent with natural language inflection
- 'd' in A is an outlier (KL=1.077, dominated by -aiin = daiin) — like an irregular high-frequency verb

**Currier B has a systematic 9-form suffix paradigm on ~10 productive stems (F045, F058)**
- 384 stems take 2+ suffix variants; 311 have edy/ain/aiin variants
- Top stem 'qok' generates 1,559 tokens in 9 suffix forms: {-eedy,-ain,-edy,-eey,-aiin,-y,-ey,-chy,-dy}
- Other highly productive stems: ch(1041 tokens), sh(870), ok(704), ot(604)
- Suffix positional bias: -aiin most line-initial (14.2%), -ain most line-final (8.0%, chi²=5.8 vs -edy's 6%), -edy most medial (85%)
- Section-level paradigm specialization: pharma→-eol/-ol (19.7%; -eol variant 4–28× pharma-enriched), bio→-edy (20.6%), special→-aiin dominant, herbal→balanced
- `-eol` is a pharma-specific suffix variant extending the paradigm beyond the original 9-form list
- Pharma labels do NOT prefer -ol (7.8% label vs 19.7% body): -ol is NOT a naming morpheme

### 1.2 Currier A/B Dialect Split

**Currier A and B are structurally incompatible as dialects of one system (F013, F017, F035)**
- Vocabulary Jaccard = 0.148; context-vector alignment 2% (vs 21% null)
- Frequency-rank Spearman ρ = 0.337 (dialects would show ρ > 0.8)
- A-exclusive: cth- cluster (cthy, cthol, cthor, qotchy ~250 tokens)
- B-exclusive: -edy/-ain paradigm (chedy=431, shedy=367, qokeedy=298, qokain=270)
- Shared ~21 function/template words: or, ol, ar, chey, daiin, aiin, dar...

### 1.3 Label Corpus

**The clean label corpus is 732 entries in Lf/Lz/Ls/Lc/Ln/Lt (F038, F039)**
- Zero single-char entries (no LINE_MARKER contamination); 100% section-specific per locus
- TTR extremely high: Lc=1.000, Ls=0.988, Lf=0.956, Ln=0.962, Lt=0.957, Lz=0.821 — near-unique
- H2 gradient: L0/Ls=2.27-2.31 (most diverse) > Lf=2.153 > body=2.071 > Lz/Ln/Lc/Lt=1.74-1.85 (most constrained)
- Labels systematically avoid qo-type and ch-type onset words; concentrate on o-initial vocabulary

**ZL3b L0 is overloaded — conflates three structurally different content types (X007, F034)**
- L0 audit: 9 TRUE_LABEL (5.6%), 43 LINE_MARKER (26.9%), 108 LIST_ENTRY (67.5%)
- Any analysis treating L0 as homogeneous "labels" is likely contaminated

### 1.4 Structural Anomalies

**Three "line-marker" folios exist (F026, F033)**
- f49v (Hand 1, Currier A, herbal) — 26 L0/P0 pairs; positions 2-6 are later-hand Arabic numerals @140=numeral "5" (F036)
- f75v (Hand 2, Currier B, bio) — 6 L0/P0 pairs; f75v|f76r are inner bifolium opening
- f76r (Hand 2, Currier B, bio) — 9 L0/P0 pairs; ZL3b transcribers explicitly note "key-like sequence"
- Sequences are independent (0 shared 2-grams), non-periodic, don't correspond to adjacent body text

**f57v contains a 4×17-token repeating sequence with 4 @NNN glyphs (F030)**
- Cycle: `o l d r v x k m f/p @169;v t r @170 @171 y I/c @172`
- @169;v is a compound glyph; f→@169 adjacency echoed in f66r column 2 (F028, F032)
- @169 and @172 are the ONLY @glyphs shared between Hand 1 (f57v) and Hand 5 (f66r) — widest cross-hand sharing

**f57v circular text and f66r column 2 share a statistically significant character inventory (p=0.003) (F032)**
- Jaccard=0.667; 10/25 EVA chars shared (3.84 above random expectation)
- f→@169 adjacency appears in both folios; but no positional ordering correspondence

### 1.5 Verbose Cipher Refutations

**Fixed-filler adjacent-pair verbose cipher on any tested language is ruled out (F020, F022)**
- Voynich paired h2 = 3.836 bits; Italian=3.411, Latin=3.509, German=3.535, Arabic=3.673, Hebrew=3.723
- No tested language reaches the target; the fixed-filler model requires an unknown source language
- Adjacent-pair grouping overshoots NL range for Voynich (3.836 bits > any tested natural language)

**Simple gallows grouping (+0.17 bits) and crust stripping (+0.048 bits) don't approach natural language h2 (X003, X005)**
- Target is ~3.4–3.5 bits; neither approach gets within 1 bit

### 1.6 Positional Entropy Structure

**Voynich shows a U-shaped positional entropy profile (F003, F004)**
- Onset (pos 0): 3.137 bits; Middle (pos 3-4): 3.606-3.612 bits; Final (-1): 2.456 bits
- Directly contradicts natural languages: Latin/Italian have HIGHER entropy at onset (pos 0) than interior
- Matches Stolfi slot grammar prediction (constrained outer crust, freer inner core)

**Word-final positions are the most constrained in the text (F004)**
- H(-1) = 2.456 bits — lower than even overall h2 = 2.341 bits
- Compare: Latin H(-1)=3.248, Italian H(-1)=3.062

---

## Tier 2 — Provisional (Single Well-Executed Experiment, No Major Confound)

### 2.1 Vocabulary Distribution

**daiin concentrates in Currier A / Herbal A (4.11-4.58% vs 1.28-1.41%) (F012)**
- Most frequent single word in Herbal A; appears only once in labels
- Not a universal function word; Currier A / Herbal A specific

**Currier A has a three-tier positional grammar (F057, F060, F061, F064, F066, exp_050, exp_053, exp_054, exp_057, exp_059)**
- **Paragraph-start slot**: -dy words (3.36× enriched), y-initial words ABSENT from A para-starts (0/134 = 0.0×)
- **Within-paragraph line-start slot**: y-initial words (16.4% of continuation first-words); -or suffix (1.66×); 30% of lines open with [or-word][ol-word] pair
- **Paragraph-end slot**: -aiin words (19.5% of A para-end last words = 1.35×; B: 10.5% = 1.30×)
- **Line-final slot**: -dy (1.59×), -al (1.35×), -ain (1.45×), '-am' words (dam=3.92×, dan/dom=6.27×)
- **Medial slot**: -ol (80.7% medial), -ey (80.8%), -eey (80.0%) — strictly avoid both edges
- 'y-' prefix = LINE-CONTINUATION PARTICLE (marks lines within a paragraph, not sentence-openers)
- **Two-register system in Herbal A (intra-A, NOT B-dialect)**: y-dominant vs aiin-dominant; vocabulary Jaccard = 0.138 (cf. A vs B = 0.120). y-dominant: 9.3% y-initial words globally (enriched 'or' 4.04×, odaiin 7.02×, o-onset 1.59×). Aiin-dominant: y-initial globally suppressed (0.21×), d-onset enriched (1.61×), chaiin (11.75×), daiin (2.01×); 2× higher daiin rate. Both registers use A suffix profile (-ol=14.2%, -or=9-12%, -edy<0.2%) — confirmed not B-dialect (exp_065). Aiin-dominant cluster in Quires D (50%) and F (62%); Quires B/O/Q exclusively y-dominant. This is an intra-A scribal convention difference (two ways of encoding same A grammar).
- **Currier B paragraph grammar**: p-onset is the dominant B paragraph-START marker (17-18× enriched at para-starts; pch 17.19×, p_other 18.21×); tch: 10.81×. B para-start words are almost exclusively line-initial and absent from labels (0/781). Most common B para-start forms: pchedy, tchedy (both pch/tch + -edy). -y initial suppressed at B para-starts (0.28×, not complete as in A)
- A vs B para-start grammar: A marks para-starts with SUFFIX class (-dy: 3.36×); B marks them with ONSET class (p-onset: 17-18×). Same structural function, different morphological slot.

**Bio section vocabulary is dominated by qo-words; Herbal A by short words (F015)**
- Bio top words: shedy, chedy, qokain, qokedy, ol, qokeedy, qokal, qokaiin
- Herbal A top words: daiin, chol, chor, shol, dar, or, chy, cthy

**Currier B suffix template is more constrained than A's at positions 5-8 (F016)**
- B suffix positional entropy 3.029-3.217 bits vs A's 3.557-3.690 at positions 5-8
- B H_final = 2.260 vs A H_final = 2.644

### 2.2 Section Vocabulary

**Section-level vocabulary is strongly section-specific (F023, F010)**
- Each section (herbal/astro/bio/pharma/cosmo) has near-zero label vocab overlap with others
- ot-/ok- initial words are 32-41% of non-herbal labels vs 10-15% in body text (section-invariant)

**Bio section is 30-85× more formulaic than herbal at phrase level; bio↔special most cross-section connected (F050, exp_043)**
- Only 0.24% of all trigrams (73/30,910) appear on 2+ folios — manuscript is overwhelmingly unique at phrase level
- Bio: 6.0 shared bigrams/folio-pair; herbal: 0.2 (30× difference)
- bio↔special shares most bigrams (1,404) and trigrams (17) of any cross-section pair — consistent with exp_038's suffix-paradigm section distribution (-aiin→S, -edy→bio)
- Most widespread bigram: "chol daiin" on 24 folios (herbal+pharma)
- Low cross-folio phrase repetition (0.24% trigrams) is inconsistent with template-generated text

**Word formation is probabilistic [ONSET × SUFFIX]: template preferences are real but modest (F063, F068, exp_056, exp_061)**
- Onset × suffix KL from independence: 0.01-0.32 bits (modest, not categorical)
- d+aiin is most templated: 2.69× over-represented in A, 2.16× in B
- qo+eedy: 2.05× in B; no categorical exclusions exist
- Top 6 onset × 6 suffix classes account for 48-54% of each dialect
- The template is probabilistic (onset-sensitive suffix preferences), not rigid slot-filling
- **Currier B effective onset taxonomy — MORPHOLOGICAL classes (F068, exp_061)**: {ch/sh} (high -y/-edy; KL=0.062); {k/t/p} (balanced; KL=0.082-0.111); {d/s} (aiin-dominant; d: 20.8%, s: 20.6% -aiin); {qo} (extended -eedy/-eey dominant)
- **POSITIONAL taxonomy (F076, exp_069) DIFFERS from morphological taxonomy**: {p} (primary para-start: 17.76×, 75.3% first); {t/f} (secondary line-opener: t=7.64× para-start, 3.82× first; f=8.04× para-start, 1.90× first, rare); {k} (medial gallows: 1.05× medial, 0.66× first; -dy suffix preference 2.14×); {ch/sh} (medial-dominant: ch 87.3% medial in B); {qo+gallows} (medial 1.12×, para-start suppressed 0.12×). Morphological and positional classifications are orthogonal — {k/t/p} share suffix profiles but have radically different positional niches.
- **ch and sh are morphologically distinct** (F076, exp_069): sh more line-initial (B: 5.0% vs ch 2.1%); ch more line-final (B: 10.6% vs sh 5.0%). In B: ch prefers short suffixes (-aiin 1.87×, -ain 1.69×, -al 1.66×, -ar 1.56×); sh prefers extended suffixes (-edy 1.31×, -eedy 1.93×). sh follows p-onset words at 4.1×.
- **B sequential word-order rule** (F077, exp_070): qo+gallows→ch/sh is the dominant medial sequence. qokain→ch (86), qokaiin→ch (78), more than daiin→ch (74). Full B sequence: [p-onset para-start] → [qo+gallows medial] → [ch/sh medial] → [closing word].
- **qo prefix attaches to gallows in 86.5% of cases** (F075, exp_068): qo+k=62.6%, qo+t=19.9%, qo+p=3.3%, qo+f=0.7%. Section-sensitive: Bio=26%, Astro=6.5%. Confirms Tier 1 qo→k/t-initial stem selectivity.
- **A ch-ch self-following** (F077, exp_070): Currier A ch-ch repetition 1.34× enriched; dominant pair "chol chol" (20 tokens). B near-random (1.09×).
- **B sequential hinge: sh→qo coupling** (F079, exp_072): sh→qo is ~2× enriched in ALL B sections (1.44-2.20×, universal). Top construction: shedy/shey → qok+suffix. sh is the STRONGEST predictor of qo-following (1.97×); d SUPPRESSES qo-following (0.76×). Combined with ch→qo (1.16×), creates B medial alternation: ...sh → qo → ch → qo → sh...
- **A vs B sequential grammar** (F079, exp_072): B uses qo as a sequential hinge (sh→qo=1.97×); A has FLAT transitions (max ch→ch: 1.34×). A lacks the qo-hinge function. A/B distinction extends to word-ordering grammar, not just morphology. Both have weak sh→qo coupling (A: 1.56×, B: 1.97×) — a cross-dialect feature.
- **d and sh are perfect sequential complements** (F080, exp_073): sh→ch 0.64× and sh→qo 1.97×; d→ch 1.27× and d→qo 0.76×. s→qo also suppressed (0.57×). Two paths to ch in B medial: (1) sh → qo → ch; (2) d → ch (direct bypass). After qo+ch, next word is again qo (29.7%), confirming alternation loop.
- **B medial grammar operates at onset-class level, lexically free** (F080, exp_073): Medial trigrams (qo+ch+X) are 99.4% unique (667 tokens, 663 types). Sequential grammar constrains onset classes, not specific words. This is structurally consistent with natural language.
- **Complete B sequential grammar**: [p-onset para-start] → [o/sh transition (p→o=29.6%, p→sh=19.0%)] → [qo↔ch/sh alternation (sh→qo: 1.97×, qo→ch: 1.31×) OR d→ch direct (d→ch: 1.27×)] → [closing word].
- The s-initial class is aiin-dominant like d — a new finding suggesting s-words encode a similar role to d-words
- **A has weaker d/sh complementarity; s-onset plays the "d role" in A** (F081, exp_074): A sh→qo=1.58× (vs B 1.97×), d→ch=1.09× (vs B 1.27×), d→qo=0.93× (vs B 0.76×). In A, s→ch=1.36× and s→qo=0.63× — s is the stronger complement of sh in A. The A {sh vs s} complementary structure parallels B's {sh vs d} structure.
- **B's sequential grammar is quantifiably stronger than A's** (F081, exp_074): Bigram onset-class model reduces perplexity by 13.3% in B (0.207 bits/bigram) vs 9.1% in A (0.138 bits/bigram). B's sequential grammar is 35% stronger by this measure.
- **B line-final words are non-random; A line-finals dominated by d-onset** (F081, exp_074): B: qo (0.61×) and sh (0.42×) suppressed at line-ends; o (1.25×) and d (1.50×) enriched. sh-penult → qo-last: 28.0% (sh→qo coupling extends to line boundary). A: d-onset is 1.73× enriched at line-ends (25.4%), consistent with -aiin/-daiin line-end marker pattern.
- **A sequential grammar is section-sensitive: Pharma A has B-strength sh→qo coupling** (F082, exp_075): Pharma A sh→qo=2.44× (exceeds B's 1.97×!), sh→ch=0.36×, s→ch=1.64×. Herbal A is much weaker (sh→qo=1.27×). Global A "weakness" (1.58×) reflects Herbal A's corpus dominance masking Pharma A's B-like structure.
- **A dominant onset-class trigram is ch→ch→ch (2.05×, 107 tokens)** (F082, exp_075): B's dominant enriched trigrams are sh→qo→ch (3.35×) and ?→sh→qo (3.43-6.14×). A=ch-repetition grammar; B=sh→qo oscillation. A sh→qo→* chains (2.42-3.00×) don't cycle back to ch as B does.
- **Aiin-dominant Herbal A has stronger sequential grammar than y-dominant** (F082, exp_075): Aiin-dom bigram PPL reduction=12.7% (approaching B's 13.3%); y-dom=10.2%. Key distinction: aiin-dom uses qo→ch (1.72×) and s→ch (1.76×) pathways; y-dom uses sh→qo (1.29×). Critical: aiin-dom d→qo=1.55× (OPPOSITE to B's d→qo=0.76×) — d leads TO qo in aiin-dominant Herbal A.
- **B line-final suppression of qo and sh is universal across all sections** (F082, exp_075): qo and sh suppressed at line-ends in all 6 B sections; o enriched in all sections; d enriched in 5/6 (exception: Special section, where "other" onset dominates at 2.03×).
- **Pharma A sequential grammar dissociated from morphology** (F083, exp_076): Pharma A has B-strength sh→qo=2.44× but pure A-type vocabulary (Jaccard with B=0.070, LOWER than Herbal A's 0.100; -edy=0.2%, -ol=18.2%). The sh→qo sequential grammar and morphological dialect are independent properties.
- **daiin→qo coupling is register-specific in Herbal A** (F083, exp_076): In aiin-dominant Herbal A, daiin→qo=2.38×; other d-words only 1.24×. In y-dominant Herbal A, daiin→qo=0.81× (suppressed). The two A registers have OPPOSITE daiin-qo coupling — daiin predicts qo in aiin-dom, avoids qo in y-dom.
- **Para-boundary marking: B closes paragraphs with o-onset; A closes with daiin** (F083/F084, exp_076/exp_077): B para-final last word: o=40.0% (1.72×) vs within-para line-final 28.2% (1.22×); qo suppressed to 0.17× at B para-final. A para-final: daiin is the dominant closer (9.0%, 2.08×) — only common enriched word; ch-onset para-finals are distributed. B para-boundary is class-level (o-onset); A para-boundary is word-specific (daiin). Both dialects suppress qo at para-final (B: 0.17×, A: 0.21×).
- **daiin is A's primary grammatical particle with hierarchical boundary-marking function** (F084/F085/F097, exp_077/078/090): accumulates 4+ grammatical roles: (1) line-final marker (1.41×); (2) para-final marker (2.08× in Pharma A; 1.35× overall — weak); (3) qo-predictor in aiin-dom Herbal A (2.38×); (4) qo-avoider in y-dom Herbal A (0.81×). Rate rises from para-first (2.44%) to para-last (6.87%) — hierarchical boundary marker. daiin marks GENERAL LINE-ENDINGS in A (not specifically para-finals: para-final precision only 1.35×). In B: LINE-OPENER (LFirst=34%) not line-closer.
- **she- prefix is a cross-dialect qo-predictor** (F085, exp_078): she- prefix sh-words (sheol, sheey, sheor, shey) precede qo at 2.19-2.91× across ALL contexts — Herbal A (1.52×), Pharma A (2.91×), Currier B (2.19×). sh-other forms (shol, sho, shor) precede qo at only 1.18-1.45×. The she-/sh-other morphological distinction predicts sequential behavior in both dialects.
- **e-vowel infix is a universal morphological qo-coupling marker** (F086, exp_079): e-vowel after ANY onset class (she-, che-, ke-, oe-, qoe-) predicts higher qo-following rate in both dialects across all 5 tested onset classes. B shows stronger e-infix effect than A (che-=1.36×, ke-=1.40×, oe-=1.54× vs A's weaker effects). The e-infix IS the key morphological distinction — it encodes "this word tends to precede qo" within the word itself.
- **Complete positional grammar models for A and B; -am is cross-dialect within-para marker** (F086-F097, exp_079-090): CROSS-DIALECT: -am suppressed at para-final in B (2.0% vs 12.6%) AND A (1.9% vs 6.4%). COMPLETE B POSITIONAL MODEL: [o/sh-onset + long + -edy/-dy PARA-START (2.42×/1.72×; top words: olfchedy=87.6×, olkey=58.4×)] → [-am line-ends 12.6%] → [o+medium+eedy/-aiin PARA-END (32.7%)]. B ol-prefix splits: ol-line-closers (oly=88.6% line-last) vs ol-para-starters (olkey=33.3% PSFirst). COMPLETE A POSITIONAL MODEL: [she-prefix PARA-START (4.74×; shey/sheol dominant); daiin SUPPRESSED at para-start 0.13×] → [-am line-ends 6.4%] → [daiin PARA-END (8.6%) + ch-onset]. she-DUAL FUNCTION RESOLVED (F092): she-→qo coupling intrinsic to she-lexemes, independent of para-start context. -AM CORE VOCABULARY (F093): {otam, qokam, dam, okam, cham, ram} = closed class of within-para line-closers (LLast%=50-100%, WithinPara%=90-100%, PSFirst%=0%). Functionally synonymous with oly/oldy. DAIIN CROSS-DIALECT REVERSAL (F093): daiin in B is LINE-OPENER (LFirst=34%, LLast=9.5%); daiin in A is LINE-CLOSER (LFirst=19.4%, LLast=25.9%). GRAMMAR MODEL UNIVERSALITY (F093/F097): she-para-start holds across herbal A (10.25×) and pharma A (5.03×); B o-onset para-start holds across all B sections (1.56-3.96×). PREDICTIVE PRECISION (F097): she-prefix predictor = 45.7% precision (4.74×); olfchedy/olkey/opchedy = 61.5% precision (14.72×). A LINE STRUCTURE (F097/F098): [opener: y+ch or d+ch] → [bare ch MID-LINE (27.3% at pos1; ch→ch self-continuing 28.4%)] → [d-onset CLOSER (23.0% at last; dam/dy/dal)]. A ch PARADIGM (F098): bare ch (9.7% LFirst) << d+ch (59.6%, 6.17×) ≤ y+ch (85.9%, 8.86×). A has TWO line-initial ch-prefix classes (y and d), unlike B's single y-prefix. CROSS-DIALECT POSITIONAL GRAMMAR (F097/F098): B=[y+k/t opener → qo mid → -am/oly closer]; A=[y+ch or d+ch opener → bare ch mid → d-closer]. Both implement PREFIX-ENCODED POSITIONAL GRAMMAR with same 3-slot template. B: explicit mid-line prefix (qo); A: no explicit mid-line prefix (bare ch = mid-line by position). DAIIN CROSS-DIALECT CONNECTOR/CLOSER DISTINCTION (F094): daiin-B = LINE-INITIAL CONNECTOR preceding sh/ch words (73.5% daiin[0]→ch/sh); daiin-A = LINE-TERMINAL MARKER. -AM AND OLY/OLDY ARE PERFECT SYNONYMS (F094): zero co-occurrence on same line (complementary distribution); section-level preference: -am in herbal B/stars B; oly/oldy in cosmo B. s-ONSET AND y-ONSET AS DISTINCT OPENERS (F094/F095): s-words → sh/ch following; y-compound words (y+ch/k/sh/t) → qo/aiin following. Y-COMPOUND LINE-INITIAL SYSTEM (F095/F096): y+[k/t] = 3.75× LFirst enrichment in B (47.3%); qo-prefix = mid-line (LFirst=11.3% ≈ background). THREE-LEVEL k/t STEM POSITIONAL PARADIGM (F096): bare (8.9% LFirst) < qo-prefix (11.6%) < y-prefix (36.2%); y/qo ratio=3.12× across 81 shared stems in B. PREFIX ENCODES POSITION: y+stem = LINE-INITIAL; qo+stem = MID-LINE; bare = UNMARKED. B LINE GRAMMAR IS MODULAR (F096): qo-mid pervasive (65.4%); opener (20.8%) and closer (5.6%) are independent optional modifiers; no rigid template sequence. -AM/OLY SELECTIONAL CONSTRAINT (F095): oly/oldy preceded by s/d/sh-onset (6.88×/3.06×/2.29×); -am preceded by ch/qo-onset.
- **e-infix is a VOCABULARY PARTITION, not productive morphology; the e-suffix co-occurrence is driven by minimal words** (F087/F088, exp_080/exp_081): B she-forms take -edy more than sh-other forms, but this is driven by MINIMAL WORDS (shedy = onset+e+suffix with no intervening stem). When the same stem appears with both e-infix (she+stem) and non-e (sh+stem), the suffix distributions are IDENTICAL — e-infix does NOT condition suffix selection. 70-98% of stems appear exclusively in e-infix OR non-e contexts, not both. The e-infix marks a DISTINCT LEXICAL CLASS (different vocabulary), not a morphological operation on shared stems.
- **Pharma A is B-convergent in qo-vocabulary and sh→qo grammar; DISSOCIATED not transitional** (F086/F087, exp_079/exp_080): Pharma A qo-words (qokeol, qokeey, qokeody) resemble B (qokeedy, qokedy) more than Herbal A (qotchy, qokchy). Pharma A sequential grammar (bigram PPL=12.9%≈B; sh→qo=2.44×>B; she-→qo=2.91×>B) EQUALS OR EXCEEDS B, while its vocabulary is FARTHER from B than Herbal A (Jaccard=0.070 < 0.100). This is NOT interpolation — sequential grammar and morphological paradigm are independently varying dimensions in Voynichese.
- **Grammar-morphology dissociation is GENERAL in Voynichese, not a Pharma A anomaly** (F088/F089, exp_081/082): Within Herbal A, aiin-dom has STRONGER sequential grammar (bigram PPL=5.8% vs y-dom 4.0%) but FEWER e-infix words (7.54% vs 12.59%) and SUPPRESSES she-→qo (0.41× vs y-dom 2.23×). Aiin-dom uses d→qo (1.90×); y-dom uses she→qo (2.23×). Suffix paradigm split: LIQUID-FINAL (-ol/-or combined 25.8%) dominates aiin-dom; GLIDE-FINAL (-ey/-eey combined 10.3%) dominates y-dom. The same ch/sh/cth stems appear with -ol/-or in aiin-dom and with -ey/-eey in y-dom (complementary substitution). The she-prefix morphological marker is INERT for sequential grammar in aiin-dom: aiin-dom she-words (shey=12, sheey=5, sheol=3) are minimal suffix forms with no qo-anticipatory function — neutrally following base rates except qo-suppression.
- **B o-onset line-closers (oly, otam, okam, oldy, olkam) form a functional sub-class** (F085, exp_078): 65-85% line-final, never line-initial, preceded by o/ch onset. They terminate o-onset word chains: o→o→oly/otam/okam. These are B grammatical line-closing words (analogous to grammatical particles).
- **A two-register grammar strategies are qualitatively different** (F085, exp_078): y-dominant Herbal A uses sh→qo coupling (she-→qo: 1.59×); aiin-dominant Herbal A uses qo→ch (1.72×) and s→ch (1.76×) and daiin→qo (2.38×) pathways instead (she-→qo: only 1.18×). Two distinct sequential grammar strategies co-exist in Herbal A.
- **Pharma A she- prefix forms drive B-strength sh→qo coupling** (F084, exp_077): Pharma A sh-words are she- prefix forms (sheol, sheey, sheor — 10-10% each) vs Herbal A short sh- forms (shol, sho, shor). Pharma A sh→qo=32.3% vs Herbal A sh→qo=12.9%. The she- forms specifically tend to precede qo-onset words — morphological distinction partially explains the sequential grammar difference.

**Section is the primary organizer of morphological variance; quire structure is secondary (F054, exp_047)**
- Section F-ratios > Quire F-ratios for all 4 features (qo-rate, -edy, -ol, -aiin)
- Pharma section (P) has -ol=18.5% (highest of any section) + -edy=0.3% — distinct pharma morphological signature
- Within-quire variance (std≈0.05 for qo) is high: quires are morphologically heterogeneous
- Quire M outlier (qo=25.8%, -edy=20.5%) maps almost entirely to bio section — quire signal is section signal

**Folio diversity (TTR) splits cleanly by section (F046)**
- Herbal: mean TTR=0.835 (most diverse), f48r/f96v = TTR=1.000 (all unique)
- Bio: mean TTR=0.552 (most repetitive)
- f76r (line-marker folio): TTR=0.466 — lowest in manuscript (z=-1.7 for Text section)
- f19r: most repetitive herbal folio (TTR=0.653, z=-2.6)

### 2.3 Labels vs Body Text

**Labels have substantially higher h2 (+0.273 bits) and 55.3% exclusive vocabulary (F007)**
- Label h2 = 2.575 bits vs body text h2 = 2.302 bits
- Labels also have dramatically higher TTR (0.746 vs 0.229)
- 439/794 label word types never appear in body text

**daiin (most common body word) is essentially absent from labels (F009)**
- 710 body occurrences; appears only once in labels
- Top body words (chedy, shedy, qokeedy) absent from label top-10

### 2.4 Structural Features

**f66r column 2 may list compound-initiating and standalone EVA chars, not a full alphabet (F027, H022)**
- Covers 11/25 EVA single chars (44%); absent: e, h, a, i, k, n, q (compound-forming chars)
- Experiment H022 shows marginal support (p=0.063): compound-avoiding chars tend to appear in col2

**f57v cycle and f66r column 2 share @169/@172 and character inventory (p=0.003) but not ordering (F032)**
- The connection is non-trivial but mechanism is unclear

---

## Tier 3 — Suggestive (Patterns Seen, Not Yet Tested Directly)

### 3.1 Morphological Model Extensions

**The {y,n,l,r} ending + 9-form paradigm together suggest a complete agglutinative suffix system**
- The most productive stems (qok, ch, sh, ok, ot) × 9 suffix forms produce the bulk of Currier B
- If -ain marks line-final position (syntactic "end" marker) and -aiin marks line-initial (subject marker), this could be a case system
- The section distribution of suffixes (-aiin → S section, -edy → bio) suggests discourse-level function

**The o-label morpheme and qo-prefix both involve adding a prefix to a shared stem vocabulary**
- Both are prefix operations: qo+stem = Currier B body-text form; o+stem = label form
- cth- is now a CONFIRMED third prefix morpheme (A-dialect; see F047)

**cth- in Currier A is the stem root 'cth', NOT a prefix morpheme (F047 revised, F059, exp_052)**
- H_initial drops from 3.061 to 1.966 after stripping — previously interpreted as prefix, now: 'cth' IS the stem
- cth+y=cthy, cth+ol=cthol, cth+or=cthor, cth+ey=cthey: 'cth' takes suffixes directly, sometimes with 1-char connector
- cth-suffix paradigm: -y=29.8%, -ol=20.0%, -or=13.8%, -ey=8.9% — strongly A-type
- cth dramatically suppresses -aiin (5.5% vs 14.7% all-A) — unlike all other A stems
- KL(cth || all-A) = 0.202 bits: moderately different from A baseline within Currier A
- Dialect determines suffix paradigm (A-type vs B-type) — stem-initial class does not independently govern suffix choice within a dialect

### 3.2 Scribal Structure

**The three line-marker folios (f49v, f75v, f76r) may reflect a scribal organizational practice**
- Two different hands (1 and 2) independently use the same structure in different sections
- The practice may be manuscript-wide, with other folios not yet identified

**f75v and f76r are a bifolium — their marker sequences may have a layout relationship**
- f75v (6 markers) and f76r (9 markers) share char set ({l,o,r,s} ⊂ {d,k,l,o,q,r,s})
- Physical adjacency (bifolium) has not been exploited analytically

### 3.3 Vocabulary Organization

**Labels are a formulaic distinct register from body text — NOT content annotations (F053, exp_046)**
- 60% of folios with labels have ZERO label-body vocabulary overlap
- The 40% with overlap share 'o'-prefix words (morphological relationship, not content naming)
- Pharma labels (Lf, 15 folios): median ratio=0.00 — completely formulaic regardless of folio body
- Labels are NOT "naming what's illustrated in body text" — they are a separate linguistic layer

**The label corpus TTR ≈ 1.0 across all sections suggests labels are primarily names (hapax phrases)**
- Near-unique labels suggest each labeled object gets a unique identifier
- But label vocabulary is NOT derived from same-folio body text

**The section-suffix correlation (-aiin→S, -edy→bio) may reflect pragmatic register rather than grammar**
- If the suffix paradigm marks aspect/tense/case, section differences suggest the manuscript sections have different modal registers (statements vs descriptions vs commands)

---

## Constraints — From Failed Approaches (X001–X009)

These are definitively ruled out by experiment:

- **X001/X002**: Q-initial stripping does NOT raise H_initial; qo stripping has negligible effect on entropy
- **X003/X004**: Gallows grouping raises h2 by only +0.17 bits; adjacent-pair grouping overshoots NL range
- **X005**: Stolfi crust stripping gives only +0.048 bits h2 gain — no natural-language-level content in core
- **X006/X007**: ZL3b L0 as homogeneous "label" category is analytically invalid (83% non-label contamination)
- **X008**: Statistical clustering (KL/KS methods) cannot detect the @glyph-cluster folios as a group
- **X009**: f68r2 @231-@234 is NOT a second structured @glyph cluster (single concatenated terminus token)
- **General**: No tested natural language has h2 ≥ 3.836 bits (the fixed-filler verbose cipher target)

**Key constraint**: Any model must explain why:
1. Currier A and B share only 14.8% vocabulary but both exhibit morphological templates
2. The label corpus and body corpus share 44.7% vocabulary but have different onset distributions
3. The 9-form suffix paradigm exists in B; A has a parallel system using -y/-ol/-or/-edy-suppressed paradigm on stems like ch, sh, ot, ok, cth
4. qo-prefixed forms coexist with bare stems in the same B folios (not complementary, not dialect-only)
5. Dialect membership (A vs B) determines suffix paradigm selection; the stem-initial class correlates with dialect but does not independently govern suffix choice (F059)

---

## Open Questions

**Q001: What is the Currier A structural parallel to B's qo-prefix and -edy/-ain paradigm?**
- A has cth- cluster and daiin-dominance; neither has been analyzed as a morphological paradigm
- Generating H040+ synthesis tests is the next step

**Q002: Can the 9-form paradigm predict suffix distribution for new/unseen stems?**
- If the paradigm is productive (not lexically listed), any new stem should take all 9 forms at some rate
- Predictive test: what fraction of stems with 1 observed suffix have their "missing" suffix forms at very low count (suggesting the paradigm is productive but evidence sparse)?

**Astro/Cosmo section (Hand 4) is A-adjacent in morphology despite Currier B character set (F051, F052)**
- qo-rate=0.059 (below even A=0.110, far below B=0.190)
- -edy=0.7% (near A=0.2%, far below B=18.5%); -ol=13.8% (intermediate)
- Currier B designation may reflect character-set similarity, not morphological similarity
- -ey (15.2%) and -eey (11.3%) anomalously high — possible circular ring text format effect
- Hand 3 (Special section): -aiin=11.4%, corroborating exp_038's aiin→Special concentration

**Q004: Is there cross-folio repetition beyond the 9-form paradigm?**
- How often does the exact same word sequence appear on two different folios?
- Are there "parallel passages" suggesting formulaic construction?

**Q005: [ANSWERED — exp_047/F054] Section explains morphological variance better than quire for all features.** Quire is not an independent predictor of morphology. Pharma section has a distinctive -ol=18.5% signature (highest of any section) not previously noted at the section level.

**Q006: What is the H028 glyph identity question?**
- Jim Reeds X1-X128 document: @169, @172, @195 physical identity unknown
- Alternative route: visual inspection of f57v manuscript images

**Q007: Do the line-marker sequences (f49v, f75v, f76r) encode cross-references, alphabets, or something else?**
- Sequences are non-periodic, don't correlate with adjacent body text first chars
- Gallows overrepresentation in f49v markers unexplained

**Q008: Are there parallel passages across sections that suggest the sections translate each other?**
- Currier A and B share a small function-word vocabulary; if body text sections repeat identical passages, this would be a major finding

---

*Update protocol: add experiment citation and date to relevant claim after each experiment. Add new findings to appropriate tier. Downgrade claims if subsequent experiments contradict them. Never delete — mark as [SUPERSEDED] with note.*
