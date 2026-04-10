# Working Model — Voynich Manuscript Cryptanalysis
**Last updated:** 2026-04-10 (after exp_156)
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
- **Complete positional grammar models for A and B; -am is cross-dialect within-para marker** (F086-F097, exp_079-090): CROSS-DIALECT: -am suppressed at para-final in B (2.0% vs 12.6%) AND A (1.9% vs 6.4%). COMPLETE B POSITIONAL MODEL: [o/sh-onset + long + -edy/-dy PARA-START (2.42×/1.72×; top words: olfchedy=87.6×, olkey=58.4×)] → [-am line-ends 12.6%] → [o+medium+eedy/-aiin PARA-END (32.7%)]. B ol-prefix splits: ol-line-closers (oly=88.6% line-last) vs ol-para-starters (olkey=33.3% PSFirst). COMPLETE A POSITIONAL MODEL: [she-prefix PARA-START (4.74×; shey/sheol dominant); daiin SUPPRESSED at para-start 0.13×] → [-am line-ends 6.4%] → [daiin PARA-END (8.6%) + ch-onset]. she-DUAL FUNCTION RESOLVED (F092): she-→qo coupling intrinsic to she-lexemes, independent of para-start context. -AM CORE VOCABULARY (F093): {otam, qokam, dam, okam, cham, ram} = closed class of within-para line-closers (LLast%=50-100%, WithinPara%=90-100%, PSFirst%=0%). Functionally synonymous with oly/oldy. DAIIN CROSS-DIALECT REVERSAL (F093): daiin in B is LINE-OPENER (LFirst=34%, LLast=9.5%); daiin in A is LINE-CLOSER (LFirst=19.4%, LLast=25.9%). GRAMMAR MODEL UNIVERSALITY (F093/F097): she-para-start holds across herbal A (10.25×) and pharma A (5.03×); B o-onset para-start holds across all B sections (1.56-3.96×). PREDICTIVE PRECISION (F097): she-prefix predictor = 45.7% precision (4.74×); olfchedy/olkey/opchedy = 61.5% precision (14.72×). A LINE STRUCTURE (F097/F098): [opener: y+ch or d+ch] → [bare ch MID-LINE (27.3% at pos1; ch→ch self-continuing 28.4%)] → [d-onset CLOSER (23.0% at last; dam/dy/dal)]. A ch PARADIGM (F098): bare ch (9.7% LFirst) << d+ch (59.6%, 6.17×) ≤ y+ch (85.9%, 8.86×). A has TWO line-initial ch-prefix classes (y and d), unlike B's single y-prefix. CROSS-DIALECT POSITIONAL GRAMMAR (F097/F098): B=[y+k/t opener → qo mid → -am/oly closer]; A=[y+ch or d+ch opener → bare ch mid → d-closer]. Both implement PREFIX-ENCODED POSITIONAL GRAMMAR with same 3-slot template. B: explicit mid-line prefix (qo); A: no explicit mid-line prefix (bare ch = mid-line by position). REVISED A GRAMMAR — FOUR TIERS (F099): (1) PARA-START markers: p-onset words (12.41× enrichment, 28.8% of PS openers!); also k-onset (4.32×), t-onset (2.72×); (2) WITHIN-PARA LINE-OPENERS: y+ch (85.9% LFirst, 0% PS rate) and d+ch (59.6%, 0% PS) and y+sh (85.7%) and d+sh (68.8%) — prefix-encoded line-starting morphemes, NOT para-starters; (3) MID-LINE: bare ch (9.7%) and bare sh (13.2%) — background LFirst rate; (4) LINE-CLOSER: d-onset words (dam/dy/dal/dar, 33-63% LLast). Y+CH vs D+CH DISTINCTION (F099): both at 0% PS rate; y+ch follows o-ending lines (23%), d+ch follows d-ending lines (35.7%); y+ch→o-onset at pos1 (24.3%, 8.15× over d+ch); d+ch→qo-onset at pos1 (16.4%), ch-onset (35.8%). D-CHAIN PATTERN (F099): d-closer on line N → d+ch opener on line N+1 (35.7% of d+ch openers follow d-ending lines). SH-STEM PARADIGM UNIVERSAL (F099): bare sh (13.2%) << d+sh (68.8%, 5.21×) ≤ y+sh (85.7%, 6.49×) — same structure as ch-stems; positional grammar applies to ALL A consonantal stem classes. UNIVERSAL VOYNICHESE POSITIONAL GRAMMAR (F100/F101): ALL FOUR GALLOWS CHARACTERS (p/k/t/f) mark PARAGRAPH BOUNDARIES in BOTH dialects: A=p(12.41×),k(4.32×),t(2.72×),f(9.50×); B=p(3.71×),k(9.91×),t(2.05×),f(7.62×). NON-GALLOWS onsets (y/d/qo/sh/s/ch) ALL SUPPRESSED at para-starts in BOTH dialects. MASTER FINDING (F101/F102): THE VOYNICHESE POSITIONAL GRAMMAR IS A PREFIX-DEMOTED GALLOWS HIERARCHY: (1) BARE GALLOWS (p/k/t/f) = PARAGRAPH-LEVEL markers: bare_p strongest (A=40.2% PS rate!, B=10.7%); bare_f second (A=24.2%, B=5.6%); bare_t next (A=10.2%, B=3.9%); bare_k weakest (A=5.7%, B=3.0%). (2) PREFIX + GALLOWS = LINE-LEVEL (prefix DEMOTES): y+gallows=WITHIN-PARA LINE-OPENER (LFirst≈30%, PS=0%); qo+gallows=MID-LINE (LFirst≈10%, PS≈0%); d+ch in A=within-para LINE-OPENER (LFirst=59-86%). (3) BARE NON-GALLOWS (ch/sh) = MID-LINE/CLOSING (LFirst=3-13%). MORPHOLOGICAL OPERATION: adding y- or qo- prefix to gallows character eliminates its para-start function; proof: qo+k(0.27-0.32× PS suppressed); y+gallows(0.08-0.40× PS suppressed). The SAME gallows stem (k, t) appears at three positional levels: bare=para, y-prefixed=line-opener, qo-prefixed=mid-line. COMPLETE 4-LEVEL GRAMMAR: LEVEL4=Para-Opener(bare gallows p/k/t/f) → LEVEL3=Line-Opener(y+gallows or d+ch in A, 0% PS rate) → LEVEL2=Mid-Line(qo+gallows in B, bare ch in A) → LEVEL1=Line-Closer(d+suffix in A, -am/oly in B). D-CHAIN (F099/F100): d-closer → d+ch opener 1.76× (modest but real). EXTENDED MASTER MODEL (F102): TWO-DIMENSION PREFIX SYSTEM: Gallows type (p/f/t/k) determines PS strength; prefix (y/d vs qo vs none) determines line-level position. PLATFORM GALLOWS (p,f) STRONGER para-starters than REGULAR GALLOWS (t,k): p+ch=26.9% PS; f+ch=21.4%; t+ch=4.1%; k+ch=3.5%. Same for sh-stems: p+sh=33.3%; t+sh=28.6%. y+ch/d+ch=0% PS (line-openers). THREE COMPLETE POSITIONAL TIERS in A: (1) Para-level: bare_p/bare_f (40-24% PS), p+ch/p+sh/f+ch (21-33% PS); (2) Line-opener: y+ch/d+ch/y+sh/d+sh (0% PS, 56-86% LFirst); (3) Mid-line: bare_ch/bare_sh/qo+k/qo+t (0-1% PS, 7-27% LFirst). UNIFIED GRAMMAR MODEL (F103): SAME morphological class has SAME positional role in BOTH A and B: p+ch=para-level in A(27% PS) AND B(12% PS); y+ch/d+ch=line-opener in A AND B (0% PS, 75-84% LFirst); bare_ch=mid-line in both (0.1-0.3% PS). PREFIX TYPE = POSITIONAL MORPHEME universally: {p,f}+any_stem=para; {y,d}+any_stem=line-opener; {qo}+gallows/bare_ch=mid-line. Stem=content; prefix=position. Single exception: f+ch is para-level in A (21%) but mid-line in B (0%). DAIIN CROSS-DIALECT CONNECTOR/CLOSER DISTINCTION (F094): daiin-B = LINE-INITIAL CONNECTOR preceding sh/ch words (73.5% daiin[0]→ch/sh); daiin-A = LINE-TERMINAL MARKER. -AM AND OLY/OLDY ARE PERFECT SYNONYMS (F094): zero co-occurrence on same line (complementary distribution); section-level preference: -am in herbal B/stars B; oly/oldy in cosmo B. s-ONSET AND y-ONSET AS DISTINCT OPENERS (F094/F095): s-words → sh/ch following; y-compound words (y+ch/k/sh/t) → qo/aiin following. Y-COMPOUND LINE-INITIAL SYSTEM (F095/F096): y+[k/t] = 3.75× LFirst enrichment in B (47.3%); qo-prefix = mid-line (LFirst=11.3% ≈ background). THREE-LEVEL k/t STEM POSITIONAL PARADIGM (F096): bare (8.9% LFirst) < qo-prefix (11.6%) < y-prefix (36.2%); y/qo ratio=3.12× across 81 shared stems in B. PREFIX ENCODES POSITION: y+stem = LINE-INITIAL; qo+stem = MID-LINE; bare = UNMARKED. B LINE GRAMMAR IS MODULAR (F096): qo-mid pervasive (65.4%); opener (20.8%) and closer (5.6%) are independent optional modifiers; no rigid template sequence. -AM/OLY SELECTIONAL CONSTRAINT (F095): oly/oldy preceded by s/d/sh-onset (6.88×/3.06×/2.29×); -am preceded by ch/qo-onset.
- **Stem × prefix combinatorics is PRODUCTIVE (not fixed lexicon); positional classifier validates three-tier model (F104/F105, exp_097/098):** PRODUCTIVE MORPHOLOGY: Core ch-stems (chol, chor, cheey) appear with ALL 7 prefix classes (p/y/d/bare/t/k/f). 87.8% stem exclusivity is a FREQUENCY ARTIFACT (rare stems don't have enough tokens to appear in all positional contexts). Zipfian stem distribution: 3 fully-productive stems account for large token fractions; ~16 productive stems=47% of all ch-stem tokens. f+ch DIALECT ASYMMETRY (F104): A uses f+ch in herbal section (21% PS rate); B uses f+ch in stars (0% PS, B-type -edy suffixes) — genuine dialectal difference in f-gallows function. POSITIONAL CLASSIFIER VALIDATION (F105): LINE_OPEN tier is CATEGORICALLY EXCLUDED from para-starts (B=100% clean, A=98.6% clean — only 1 false positive). PARA tier is 11.8× enriched in A and 3.94× in B. COVERAGE GAP: ~54% of para-starts use "OTHER" words not in the gallows/compound system — para-starting vocabulary extends beyond the gallows morphology. PARA BOUNDARY IS SHARPEST MORPHOLOGICAL TRANSITION: PARA markers drop 33%→0.6% from line 1 to line 2 (55× drop); LINE_OPEN markers jump 2.4%→29% (12× rise). Canonical paragraph sequence: PARA-tier opener at line 1 → LINE_OPEN or OTHER at lines 2+. WITHIN-PARA structure is uniform (no distinct middle or closing morphology). PARA-FINAL LAST WORDS: o-onset (27.4% A, 35.3% B) and d-onset (23.8% A) dominant — but no specialized closing morphological class. PARA LENGTH IS SECTION-DETERMINED: stars(B)=47 lines, cosmo(B)=25 lines, herbal(A/B)=12-13 lines, pharma(A)=7.7 lines, astro(A)=3.4 lines. REVISED PARA TIER CLASSIFIER (F106, exp_099): "OTHER" para-start words are dominated by bare_k (A=9.12×, B=11.92×) and bare_t (A=3.25×, B=1.77×) gallows words — these were the missing piece in the classifier. o-onset, d-onset, s-onset are SUPPRESSED even within OTHER. COMPLETE PARA TIER = {p,f}+stem + bare_k + bare_t (should cover ~65-70% of para-starts). Most discriminative 2-char para-start onsets: A="po-" (22.17×!), B="ko-" (38.12×!). B PARA-CLOSING VOCABULARY (F106): B has specialized para-final words: okeey (16.4×), orol (21.9×), shedy (6.25×), cheam (10.9×) — sh-onset (2.88×) and specific o+ey forms dominate B paragraph endings. A para-final is weaker: daiin (1.27×). Para-starters (p-onset) are perfectly EXCLUDED from para-final positions (0.00×) — clean complementary distribution. Astro section A has 69.2% OTHER para-starts — most anomalous section for para-start vocabulary. EXTENDED CLASSIFIER v2 (F107, exp_100): Adding bare_k + bare_t to PARA tier improves PS coverage from 34%→54% (A) and 39%→54% (B). OTHER shrinks to 18-24%. Remaining OTHER is 52-63% o-onset (oty, okoy, olfchedy, okar). Full PARA tier = {p,f,k,t}+anything + specific o-onset forms. ASTRO EXCEPTION CONFIRMED: Astro A (3.4-line captions) allows LINE_OPEN at para-starts (11.5% vs 0% herbal) — positional grammar is REGISTER-SPECIFIC, strict in long paragraphs, relaxed in short captions. HERBAL A COVERAGE: v2 classifier achieves 60.9% PARA, 8% OTHER in herbal A — near-complete coverage of herbal para-starts. B PARA-FINAL WEAK ORGANIZATION: okeey/okeeey (∞ enrich), orol (21.9×), shedy (6.25× cosmo-only) are B para-final markers but cover only 22.8% of B para-finals. Most paragraphs end with hapax/section-specific words. Cosmo B has most formulaic closing vocabulary. o-ONSET PARA-START CLASS (F108, exp_101): o-onset is NOT a coherent para-start class (0.52× A suppressed). Only "op-" sub-onset (9.5×) is enriched via internal p-gallows; olfchedy-type words enriched via internal f+ch morphology. Remaining ~17-20% OTHER para-starts are genuinely diverse hapax/section-specific words — the positional grammar is essentially complete at v3. GRAMMAR STRENGTH VS PARAGRAPH LENGTH (F108): Para-start grammar strictness scales with paragraph length. A 10-15 line paragraphs (herbal): 70.7% PARA, 0% LINE_OPEN — strictest grammar in manuscript. A 2-4 line (astro captions): 31% PARA, 8.6% LINE_OPEN allowed. B monotonically increasing (22%→65% PARA with length), never violates LINE_OPEN exclusion. The positional grammar is a REGISTER-SPECIFIC rule: strictest in canonical herbal (~13-line) paragraphs, progressively relaxed in shorter caption-like text.
- **e-infix is a VOCABULARY PARTITION, not productive morphology; the e-suffix co-occurrence is driven by minimal words** (F087/F088, exp_080/exp_081): B she-forms take -edy more than sh-other forms, but this is driven by MINIMAL WORDS (shedy = onset+e+suffix with no intervening stem). When the same stem appears with both e-infix (she+stem) and non-e (sh+stem), the suffix distributions are IDENTICAL — e-infix does NOT condition suffix selection. 70-98% of stems appear exclusively in e-infix OR non-e contexts, not both. The e-infix marks a DISTINCT LEXICAL CLASS (different vocabulary), not a morphological operation on shared stems.
- **Pharma A is B-convergent in qo-vocabulary and sh→qo grammar; DISSOCIATED not transitional** (F086/F087, exp_079/exp_080): Pharma A qo-words (qokeol, qokeey, qokeody) resemble B (qokeedy, qokedy) more than Herbal A (qotchy, qokchy). Pharma A sequential grammar (bigram PPL=12.9%≈B; sh→qo=2.44×>B; she-→qo=2.91×>B) EQUALS OR EXCEEDS B, while its vocabulary is FARTHER from B than Herbal A (Jaccard=0.070 < 0.100). This is NOT interpolation — sequential grammar and morphological paradigm are independently varying dimensions in Voynichese.
- **Grammar-morphology dissociation is GENERAL in Voynichese, not a Pharma A anomaly** (F088/F089, exp_081/082): Within Herbal A, aiin-dom has STRONGER sequential grammar (bigram PPL=5.8% vs y-dom 4.0%) but FEWER e-infix words (7.54% vs 12.59%) and SUPPRESSES she-→qo (0.41× vs y-dom 2.23×). Aiin-dom uses d→qo (1.90×); y-dom uses she→qo (2.23×). Suffix paradigm split: LIQUID-FINAL (-ol/-or combined 25.8%) dominates aiin-dom; GLIDE-FINAL (-ey/-eey combined 10.3%) dominates y-dom. The same ch/sh/cth stems appear with -ol/-or in aiin-dom and with -ey/-eey in y-dom (complementary substitution). The she-prefix morphological marker is INERT for sequential grammar in aiin-dom: aiin-dom she-words (shey=12, sheey=5, sheol=3) are minimal suffix forms with no qo-anticipatory function — neutrally following base rates except qo-suppression.
- **B o-onset line-closers (oly, otam, okam, oldy, olkam) form a functional sub-class** (F085, exp_078): 65-85% line-final, never line-initial, preceded by o/ch onset. They terminate o-onset word chains: o→o→oly/otam/okam. These are B grammatical line-closing words (analogous to grammatical particles).
- **A two-register grammar strategies are qualitatively different** (F085, exp_078): y-dominant Herbal A uses sh→qo coupling (she-→qo: 1.59×); aiin-dominant Herbal A uses qo→ch (1.72×) and s→ch (1.76×) and daiin→qo (2.38×) pathways instead (she-→qo: only 1.18×). Two distinct sequential grammar strategies co-exist in Herbal A.
- **Pharma A she- prefix forms drive B-strength sh→qo coupling** (F084, exp_077): Pharma A sh-words are she- prefix forms (sheol, sheey, sheor — 10-10% each) vs Herbal A short sh- forms (shol, sho, shor). Pharma A sh→qo=32.3% vs Herbal A sh→qo=12.9%. The she- forms specifically tend to precede qo-onset words — morphological distinction partially explains the sequential grammar difference.

**ch-Stem vocabulary classifies sections at 73% of full-vocabulary performance; A/B ch-vocabularies are MORE DISTINCT than random (F110, exp_103)**
- Naive Bayes on ch-words: 2.11× baseline (A), 1.60× (B); ch-words capture 73% of full-vocabulary section-discriminating power
- Most informative section markers: herbal A = chaiin, char; pharma A = cheom, cheodal; stars B = cheeo, chokaiin; cosmo B = checthy, cheeky
- A/B ch-vocabulary Jaccard = 0.181 (BELOW independence expectation of 0.62×!) — dialects are anti-correlated in ch-vocabulary
- B-exclusive ch-words: chedar(25), chdaiin(17), chdal(16), chdar(15) — "ch+d" cluster pattern unique to B
- A-exclusive: chom, choiin, chory, chotchy — "cho+" onset + A-suffix forms
- chedy (B=22.74‰, A=0.52‰, 43.9× more common in B) is the single most diagnostic A/B differentiator in ch-vocabulary
- The shared 18% ch-vocabulary is dominated by extreme rate contrasts (same word form, very different frequency), suggesting accidental homography rather than shared semantic content

**Section is the primary organizer of morphological variance; quire structure is secondary (F054, exp_047)**
- Section F-ratios > Quire F-ratios for all 4 features (qo-rate, -edy, -ol, -aiin)
- Pharma section (P) has -ol=18.5% (highest of any section) + -edy=0.3% — distinct pharma morphological signature
- Within-quire variance (std≈0.05 for qo) is high: quires are morphologically heterogeneous
- Quire M outlier (qo=25.8%, -edy=20.5%) maps almost entirely to bio section — quire signal is section signal
- **Section-specific CONTENT WORD vocabulary confirmed (F109, exp_102)**: bare_ch content words show strong section-specialization. Herbal A: chol/chor + EXCLUSIVE words (chain, chocthy, choiin, chan, chokchy). Pharma A: cheol (6.1×!), cheeor (10.4×!), cheom (14.8×!) enriched. Stars B: cho/cheo/cheeo/cheodaiin EXCLUSIVE; Stars B also has chain (6.1×), chaiin (6.1×), cheeody (6.1×). Cosmo B: chcthy (2.3×), checthy (4.9×), cheeky (5.1×). Herbal B: cheky (3.5×), chekaiin (10×!). Each section has a distinctive ch-stem morphological signature beyond the shared core (chol/chor in A; chedy/chey in B). TIER COMPOSITION (F109): PARA+LO+WEAK tiers = only 10-20% of all word tokens; ~80% are content words (MID tier = 31-49% bare_ch/sh/qo; OTHER = 41-52%). The positional grammar labels a minority of words — most words in the manuscript are content words that show section-level semantic specialization. GRAMMAR STRICTNESS (F108/F109): Grammar strictness is PRIMARILY section-determined. Within cosmo B, length also has genuine effect. Within herbal A, grammar strictness is REVERSED with length (shorter herbal paras = higher PARA%). The positional grammar is most strict in the canonical herbal text register (10-15 line paragraphs, 70.7% PARA at PS, 0% LINE_OPEN).

**Suffix System Has FOUR-LEVEL Hierarchy: Dialect → Stem Class → Section → Vowel-Length; Stars-Triple-Vowel (eeedy=63%; eeey=59%); A-Herbal=-y; A-Pharma=-ol (F120, exp_113)**
- eee (triple-vowel) words: stars=17.25‰, cosmo=4.40‰ (suppressed). Vowel-length gradient monotonically stars-concentrated (edy→eedy→eeedy: 36%→48%→63%). eee enriched in ok/ol/qo (1.7-1.9×), suppressed in ch/sh (0.37-0.46×).
- A-dialect section variation: herbal-A=-y dominant (qok=37%, ch=29%); pharma-A=-ol dominant (qok=41%, ok=40%); 8.9% avg diff (3.5× weaker than B's 31%).
- FOUR-LEVEL suffix hierarchy: Dialect (A/B) → Stem class (Simple-B/Complex-B; A-y/-ol) → Section (B: stars/cosmo/herbal; A: herbal/pharma) → Vowel length (stars triple-vowel extension). Strong evidence for natural language morphology.

**CORRECTED cth POSITIONAL PARADIGM: cthor=SECOND (2.16×); cthol=MID (1.33×); cthy=LL (1.63×); ALL cth AVOID LF (0.00-0.38×); cthor=97% IN A-HERBAL; daiin→cthy SELECTS LL (2.12×); [daiin][cthy] SPECIFIC PHRASE (F161, exp_154; F160, exp_153)**
- CORRECTION: F158 claimed cthor=LF-opener (1.76×) — RETRACTED. Exp_151/152 had swapped LF/second labels. Correct: cthor=SECOND-enriched (2.16×), LF-depleted (0.38×). cthor appears at i=1 (second word), not i=0 (first word).
- Corrected paradigm: cthor=second (2.16×); cthol=MID (1.33×); cthody/ctheody=MID (1.33-1.53×); cthy=LL (1.63×); cthom=LL (2.49×). All cth-words avoid LF.
- cthor: 97% concentrated in A-herbal (32/33 tokens). A-pharma n=1; astro/cosmo n=0.
- [daiin][cthy]: daiin→cthy bigrams (n=9): cthy at LL=55.6% (2.12×), never at LF/second. daiin is an LL-specific selector for cthy.
- [daiin][cthy] specificity confirmed (H304/F160): daiin=3.57× as penultimate before cthy@LL, 0× before all other cth@LL.
- Section bug fixed (H305): folio_base kept leading '<' (e.g., '<f1r'); .lstrip('<') fixes regex match.

**4-WAY cth POSITIONAL PARADIGM: cthor=LF-OPENER (1.76×); cthol=SECOND (1.94×); cthody/ctheody=MID (1.29-1.68×); cthy=LL-CLOSER (1.39×); daiin→cthy=LINE-CLOSER + daiin→cthol=MEDIAL; chol@LF→cth@SECOND=3.11× (F158, exp_151)**
- cthor=LF-enriched (LF=31.2%, 1.76×), LL-depleted (0.35×). cthol=second-enriched (31.2%, 1.94×), LL-depleted (0.59×). cthody/ctheody=MID-enriched (1.29-1.68×). cthy=LL-enriched (24.7%, 1.39×), second-depleted (0.58×).
- daiin→cthy→LL (n=5, dominant line-closer): daiin introduces cthy to close the line.
- daiin→cthol→MID/second (n=6, dominant medial): daiin introduces cthol as medial nominal.
- chol at LF → cth at second=14.1% (3.11×); 31.2% of chol-lines contain a cth-word.

**chol=SECOND-ENRICHED (1.87×), LF-DEPLETED (0.30×); chol→cth BIGRAMS FROM SECOND/MID (NOT LF); VERIFIED chol→cth=2.35×, chor→cth=2.22×; F157 POSITIONAL FRAMING RETRACTED (F163, exp_156)**
- chol: second=1.87×, MID=1.25×, LF=0.30× (NOT a line-opener). chor: second=2.33×, LF=0.64×.
- chol→cth bigrams (n=20): 55% from chol@second, 45% from chol@MID, 0% from chol@LF. Corrected construction: [LF-word][chol@second][cth@subsequent].
- chol@LF (n=11): second-pos is ch-onset 54.5% (~8× enriched) — [chol@LF][ch@second] pattern, never cth at second.
- Verified bigram enrichments: chol→cth=2.35×, chor→cth=2.22× (real).
- daiin→cth bigram real (3.08×). Daiin→cth positional context still to verify (H314).
- dy→sh real within-line construction. HELD.

**NO A-PARTICLE INTRODUCES sh/ch_e AT 3×+; sh=SELF-INTRODUCED (1.68×); ch_e=SELF-INTRODUCED (1.98×); cth-ENRICHED PARTICLE CLUSTER (daiin/chol/chor/cthol→cth AT 2.1-3.1×) DEPLETES sh/ch_e; aiin/ol→cth=0.00× BUT →ch_e=1.4-2.0× (F156, exp_149)**
- sh before-context: self-succession=1.68×; d=0.77×, cth=0.64× (depleted). No particle >2.5×.
- ch_e before-context: self-succession=1.98×; ok=1.56×, qok=1.50×; d=0.62×, sh=0.56× (depleted).
- cth-enriched particles (daiin/chol/chor/cthol) all avoid sh/ch_e. aiin/ol/ar→cth=0.00× but →ch_e=1.4-2.0×.
- A grammar has onset-class self-succession but no dedicated particle-gatekeeper for sh/ch_e — daiin→cth=3.08× is uniquely categorical.

**B-daiin→d=2.85× TRUE (NOT SELF-SUCCESSION); A-daiin DEPLETES sh (0.64×) AND ch_e (0.42×); B-daiin→ch_e=1.77×; A/B REVERSAL: A-daiin=[cth-introducer]; B-daiin=[d/ch_e-introducer] (F155, exp_148)**
- A-daiin P-type: cth=3.08× (confirmed); d=1.40×; sh=0.64× (depleted); ch_e=0.42× (strongly depleted).
- B-daiin P-type: d=2.85× (non-self, n=21); ch_e=1.77×; sh=1.19× (near baseline); cth=0.00×.
- A/B REVERSAL: A-daiin avoids sh/ch_e; B-daiin seeks ch_e. A-daiin is cth-specific gatekeeper; B-daiin is d/ch_e introducer.

**B-COMPOUND-ch (chdy/chckhy/chcthy) ARE B "MEDIAL NOMINALS" (MID=1.10-1.28×, LF-DEPLETED); d DEPLETED BEFORE B-ch (0.79×, OPPOSITE A-cth 1.30×); ch SELF-SUCCESSION=1.57×; exp_145 B-daiin→sh REVISED to 1.19× (P-TYPE); B-daiin→d=2.70× DOMINANT (F154, exp_147)**
- Compound ch-words (chdy=103, chckhy=102, chcthy=52, chody=37) are MID-enriched (1.10-1.28×), LF-depleted (0.52-0.68×) — B's "medial nominal" class. chol in B is a LINE-OPENER (LF=1.42×).
- Before B-ch: ch-self-succession (1.54×) and k-class (1.40×) dominant; d=0.79× DEPLETED. Opposite of A-cth where d=1.30× enriched.
- ch self-succession=1.57× is the closest B-ch parallel to A-cth self-succession (1.84×). B-sh/ch_e have no self-succession.
- CORRECTION to F152: exp_145 daiin→sh=2.33× was inflated by non-P locus types. P-type body text only: daiin→sh=1.19×; daiin→d=2.70× (dominant). B-daiin is primarily a d-predecessor, not sh-determiner.

**B-sh IS B LINE-OPENER (LF=1.90×), NOT MEDIAL NOMINAL; daiin→sh≠daiin→cth ANALOGY DISPROVEN; -eey WORDS PRECEDE B l-ONSET AT 2.7-3.4× (MORPHOLOGICAL, NOT SINGLE DETERMINER); A l-ONSET FOLLOWS qo-ENVIRONMENT (qot=3.99×) (F153, exp_146)**
- sh in B: LF=24.8% (1.90×), LL=5.2% (0.40×) — LINE-OPENER. cth in A: LF=16.6% (0.94×), LL=21.3% (1.20×) — near-baseline/mildly LL. Profiles opposite.
- Before sh in B: qok=1.42× (not d); before cth in A: d=1.30×, qok-suppressed. Self-succession: A-cth=1.84×; B-sh=0.93× (absent); B-ch_e=0.87×. B-ch shows 1.57× — closer to A-cth.
- daiin→sh (2.33×) reflects B sequential grammar: daiin (LFirst=34%) + sh (LF=1.90×) are both LF-enriched. Not determiner-nominal — two line-initial class words.
- l-onset in B preceded by -eey suffix words (okeey=3.37×, qokey=2.96×, chey=2.94×); ch_e=1.42×, ch=1.27× at onset-class level; d=0.42× depleted. No single B-particle parallels daiin's cth-determiner role.
- A l-onset (n=59 rare) follows qo-environment (qot=3.99×, qok=2.40×) — may be specialized qo-following vocab, not equivalent to B l-class.

**daiin=UNIQUE cth-DETERMINER IN A-DIALECT (3.19×); NO OTHER PARTICLE PRECEDES cth (0.00×); B-DIALECT daiin SHIFTS TO sh/ch_e INTRODUCTION (2.33×/2.11×); OTHER B-PARTICLES DEPLETED BEFORE sh/ch_e (F152, exp_145)**
- daiin→cth in A: 43 cases, 12.9% observed vs 4.0% baseline = 3.19× enrichment. All other tested particles (aiin/ar/ol/chol/dain/qokeey/saiin) precede cth at 0.00× — categorical distinction.
- daiin→cth in B: 0.0% (consistent with B's cth depletion). In B: daiin→sh=2.33× (46 cases) and daiin→ch_e=2.11× (44 cases) are uniquely enriched.
- Other B particles (aiin/ar/ol/chol) are DEPLETED before sh/ch_e (0.31×–0.45×) — exact opposite of daiin. daiin is the unique sh/ch_e introducer in B, mirroring its A role as unique cth introducer.
- Structural parallel: daiin = category-specific determiner in both dialects. In A: [daiin → cth-nominal]; in B: [daiin → sh/ch_e-nominal]. Role preserved cross-dialect; target onset class shifts.

**cthor→chol DOMINANT (37.5%); [qo/ok][daiin][cthor][ot-word] EXTENDED FORMULA; daiin=UNIVERSAL cth-PRECEDER (43 cases); ot=A/B PARADIGM SPLIT (1.67× B-biased) (F151, exp_144)**
- cthor→chol 3× (f9/f15/f19); "daiin cthor chol" 2×. cthor completable by chol or ot-word.
- Extended construction: [qo/ok][daiin][cthor][ot-word] — all 3 "daiin cthor ot*" preceded by qo/ok-word.
- daiin: universal cth-preceder (43× in A). daiin→cthy=9, daiin→cthol=6, daiin→cthor=6.
- ot-onset: A rate=3.9% (otol/oty dominant), B rate=6.5% (otedy/oteedy dominant). A/B paradigm split matches all other onset classes.

**cthor→ot REAL (21.9%) NOT EARLY-HERBAL-SPECIFIC; "daiin cthor ot*" TRIPLE RECURRENT (3×); cth-RUNS RARE (93.2% ISOLATED, ALL BIGRAMS HAPAX) (F150, exp_143)**
- cthor→ot: 21.9% of cthor usages, varied ot-words, spread f9-f52. "daiin cthor ot*" triple appears 3×. cthor decline not due to cthor→ot disappearing (present in late folios).
- cth-runs: 93.2% isolated, 6.8% in 2+ runs. All consecutive cth-bigrams are hapax — no dominant cth-cluster formula. Confirmed cth-words are mostly isolated content words.

**cthor=SECOND-POSITION WORD (corrects F148 LF=39.4% artifact); cthor→ot 6.18×; d before cthol=1.51× = d before lchedy=1.45× (PARALLEL CONFIRMED); SELF-SUCCESSION ~2.2× in each dialect (F149, exp_142)**
- cthor true LF=6.1% (not 39.4%); cthor is a second-position word (~33% at position i=1) with ot-succession (6.18×). cthor not preceded by cth (0.00×) unlike cthol (1.55×).
- d-enrichment before cthol (1.51×) = d-enrichment before lchedy (1.45×) — grammatical parallel confirmed across dialects. Self-succession: cth before cthol=1.55×, l before lchedy=2.10×.
- After-patterns dialect-specific but same enrichment magnitude (~2×). Structural parallel confirmed at d-predecessor and self-succession levels.

**lchedy↔cthol POSITIONAL EQUIVALENCE (MID~67-69%, LF~20-22%, LL~11-12%); cth LF=0.14× DEPLETED/LL=1.38× ENRICHED; lk-MOST MEDIAL (74.5%); BIGRAM CONTEXTS COMPLETELY DIFFERENT; cthor LF=39.4% RETRACTED BY F149 (F148, exp_141)**
- lchedy (dominant B l-word) and cthol (dominant A cth-word): nearly identical positional profiles. Structural parallel of A's cth-prefix and B's l-prefix confirmed at word level.
- cth-words strongly LF-depleted (0.14×) and LL-enriched (1.38×). lch-words moderately LF-depleted (0.81×) and LL-enriched (1.27×).
- lk-words most purely medial (MID=74.5%, 1.15×, LF=0.33×, LL=0.87×) — different from lch and cth.
- Bigram contexts completely different: cth surrounded by d/ch (A-grammar); lch surrounded by qok/l (B-grammar).
- cthor LF=39.4% (anomalously high for cth-word): cthor marks line-opening constructions; may explain cthor-specific decline in late A-herbal (F147).

**A-HERBAL cth VOCABULARY DECLINE MIXED (cthor 0.24×, cthaiin STABLE; l=B-MORPHOLOGICAL PARALLEL to cth: lchedy(102,100%B) DOMINANT; 1120 B vs 59 A l-tokens; loldaiin=A-EXCLUSIVE (exp_139 correction) (F147, exp_140)**
- cth vocabulary shift: cthor disproportionately declines (T3/T1=0.24 vs overall 0.60). cthaiin completely stable (1.03×). Most cth-words decline proportionally (~0.46). Mechanism: general cth density reduction + cthor-specific botanical content shift.
- B-dialect l-vocabulary: 1120 B vs 59 A l-tokens (19× ratio). Top B l-words: lchedy(102,100%B), lkaiin(37,100%B), lkeey(33,97%B), lkeedy(32,97%B). lk-forms are 100% B-exclusive.
- l is B's morphological parallel to A's cth: both are prefix morphemes on distinct stem classes. lchedy (l+ch+edy) parallels cthol (cth+ol).
- CORRECTION: loldaiin (exp_139 "B-form") is A-exclusive (A=1, B=0). Only lkeedy(1) and lkeey(1) are genuine B-dialect l-intrusions in late A-herbal.

**A-HERBAL cth DECLINE = SMOOTH GRADIENT (T1=5.96%→T2=4.82%→T3=3.66%, −1.1pp/tertile); l-GRADIENT STRONGER (ρ=+0.627) THAN cth-GRADIENT (ρ=-0.269); A-HERBAL l-WORDS TOO SPARSE (37 tokens) FOR B-CONTAMINATION ANALYSIS (F146, exp_139)**
- A-herbal cth tertile decline is equal-interval (−1.14pp, −1.15pp per step) — smooth gradient, not step-change. Rules out single scribal hand-change at a specific folio.
- l-gradient ρ=+0.627 STRONGER than cth-gradient ρ=-0.269 in A-herbal. Later A-herbal shifts more consistently toward l-onset words than it depletes cth.
- l-words in A-herbal: only 37 total tokens (16 early, 21 late). Clean B-form late l-words: lkeedy(1), lkeey(1), loldaiin(1). Sample too small for B-vocabulary contamination conclusion.
- Spawned: H277 (cth decline = content gradient? Identify which cth-words disappear), H278 (B-dialect l-vocabulary as reference for A-herbal comparison).

**A-HERBAL cth GRADIENT IS REAL IN A-ONLY (ρ=-0.353; early=5.4% → late=3.7%=0.69×); l-GRADIENT ALSO REAL (ρ=+0.457); STARS cth ρ=+0.469 = NOISE (19 tokens, F144 claim RETRACTED); f47 = SAMPLING ARTIFACT (n=134) (F145, exp_138)**
- A-herbal-only cth ρ=-0.353 (44 folios): genuine A-herbal cth decline, not solely B-insertion artifact. B-insertions amplify (full-herbal ρ=-0.486 → A-only ρ=-0.353).
- Early A-herbal (f1-f28): cth=5.4%, l=0.4%; late A-herbal (f29-f57): cth=3.7% (0.69×), l=0.8% (1.84×). l-gradient (ρ=+0.457) in A-herbal is a B-dialect marker increase.
- Stars cth total = 19 tokens / 7748 words (0.25%). The F144 ρ=+0.469 was driven by f113 (7 tokens) + f116 (4 tokens) — sampling noise with unreliable Spearman ρ. F144's stars-cth claim RETRACTED.
- f47 (n=134 words, A-herbal): ch=35.1% (2.06×) = sampling artifact. chol=11 by chance, y/qo=0% consistent with n=134. Cosine similarity=0.8473 (correctly identified herbal). No scribal anomaly.
- Spawned: H275 (A-herbal cth breakpoint vs smooth gradient), H276 (late A-herbal l-words: B-vocabulary contamination or A-content shift?).

**PARA-TAIL LINES (=Pt) = ch-DOMINANT (2.15×), y-DEPLETED (0.28×), 80% HERBAL; PARA-TAIL CLOSER = -y (27.3%); FOLIO GRADIENT: d/cth DECREASE (ρ≈-0.64), l/qok INCREASE (ρ≈+0.64) ACROSS MANUSCRIPT; WITHIN-HERBAL cth ρ=-0.486; STARS cth ρ=+0.469 (RETRACTED BY F145) (F144, exp_137)**
- Para-tail (=Pt): 46 lines, mean=5.3 words (vs continuation 7.5). ch=2.15×, d=1.61×, y=0.28×. Last-word: -y=27.3%, -am=6.1%. 80% herbal, 20% cosmo; zero stars/pharma/astro tail lines.
- Para-tail is closing vocabulary (ch/d-dominant, y-depleted) — complementary to para-start (y/p/k-dominant).
- Six onset classes show global folio gradient (|ρ|>0.5): d/cth/ch decrease; l/qok/ol increase — traces A→B dialect transition.
- sh/s: ρ≈0 (no folio gradient — section-concentrated but non-monotonic).
- Within-herbal cth gradient (ρ=-0.486): cth 6-10% at early herbal → ~0% at late herbal (B-insertions concentrated in later herbal folios).
- Stars cth ρ=+0.469 (unexpected increase in later stars folios).
- Most deviant: f40(dev=0.2407), f47(dev=0.2375), f67(dev=0.2229). Most typical: f106(dev=0.0575), f80(dev=0.0624).

**-am = WITHIN-PARAGRAPH LINE-FINAL MARKER ONLY (0 para-final occurrences); UNIVERSAL CORE (71 WORDS) = 78.9% MEDIAL; l/p/cth ABSENT FROM UNIVERSAL CORE; COSMO-ABSENT SET = 55% A-DIALECT (cth=10.90×); ol/s/l = COSMO-POSITIVE FEATURES (F143, exp_136)**
- -am at para-final line-ends: 0/255 (0.00×) across all 260 paragraphs all sections. REVERSED: -am is NOT sentence-final, it is strictly within-paragraph. Confirms and extends F086/F094 (-am suppressed at para-final in both A and B).
- Para-final lines end with "other" suffix (97.6%) — paragraph tail (=Pt) lines with transcription markers; NOT a closing formula.
- Universal core (71 types, 6708 tokens): LF=11.6%, MID=78.9%, LL=9.5% vs section-exclusive LF=16.1%, MID=60.2%, LL=23.8%. Core contains openers (saiin=53.5%LF), closers (dy=41.9%LL), and medials (chey=95.7%MID).
- l/p/cth ABSENT from 71 universal types. s(9.9%), ot(8.5%), ok(7%), sh(9.9%) overrepresented. After-universal bigram context = baseline.
- 73 high-freq cosmo-absent words: 55% A-dominated (cth onset = 10.90× in cosmo-absent set). cthy=96.6%A, cthol=96.1%A. ol/s/l = 0.00× in cosmo-absent (these are cosmo's exclusive features).

**COSMO LINE TEMPLATE = [s/y/p/t/d OPENER (2.6-4.7×)][sh 2nd (1.75×)][l/r/ol CLOSER][-am(7.87×)/-y/-dy SUFFIX CLOSER]; -am IS PAN-B-SECTION CLOSER (COSMO=7.87×, STARS=7.48×); COSMO-STARS=CLOSEST SECTION PAIR (Jaccard=0.1371); 71-WORD UNIVERSAL CORE (daiin/ol/chol dominant); HERBAL=VOCABULARY SUPERSET (F142, exp_135)**
- Cosmo template: FIRST: p(4.67×), s(4.10×), y(3.78×), t(2.59×), d(1.81×); DEPLETED: ch_e(0.23×), sh(0.47×). SECOND: sh(1.75×). LAST onset: r(2.19×), l(2.16×), ol(1.69×). LAST suffix: -am(7.87×), -dy(2.22×), -y(2.04×).
- -am CLOSER is pan-B-section: cosmo=7.87×, stars=7.48× (REVISES F138 which implied stars-concentration). -am is a SENTENCE-FINAL MARKER across both major B sections.
- 5×5 Jaccard matrix: cosmo-stars=0.1371 (highest pair), herbal-pharma=0.1209, herbal-stars=0.1199. Astro=most isolated (astro-stars=0.0434, astro-herbal=0.0461). All pairwise J<0.15 — sections are highly distinct vocabulary communities.
- Exclusive vocabulary: herbal=2488 types (70.7%), stars=2350 (67.9%), cosmo=1015 (56.7%), pharma=845 (54.4%), astro=132 (38.7%). Astro's low exclusive fraction confirms heterogeneous composition (F140).
- 71 universal words in all 5 sections: daiin(641), ol(318), chol(290), qokeey(276), chey(258). d-onset and ol dominate the universal core.
- Herbal=vocabulary superset: 0 words absent from herbal when present in all other 4 sections. Stars nearly a superset (only 5 absent).
- Absent from cosmo: 31 types including chor, sho, cthy, cthol — all cth/ch forms, consistent with B-dialect cth depletion (F139).
- B-dialect Jaccard confirms: cosmo-stars=0.1523 (highest B pair), herbal-cosmo=0.1512. B-cosmo vocabulary bridges B-herbal and stars.
- cth absent from cosmo FIRST position (0.23×) vs stars cth=1.89× at FIRST — same cth depletion in B-cosmo at grammatical level.

**ol-ONSET = MEDIAL PARTICLE/MODIFIER (MID=74.6%, LF=7.7%); ol SELF-CHAINS (pre-ol=ol 1.68×, post-ol=ol 1.89×); STANDALONE "ol"(n=474) + ol+k-stem B-COSMO COMPOUND WORDS; ol = o+l DOUBLE-PREFIX; ch+eo VOWEL-GRADIENT: ch+o=27%STARS→ch+eo=40%→ch+eeo=55%→ch+eeeo=100%; e-VOWEL EXTENSION = STARS MARKER AT ALL STRUCTURAL LEVELS (F141, exp_134)**
- ol-onset: 1333 tokens, MID=74.6%, LF=7.7% — never a line-opener. Cosmo=2.06×. B=81.5%.
- Standalone "ol" (n=474, 84%MID, cosmo=49%) = the -ol suffix as free morpheme. ol+k-stem compound words (olkain=76.5%cosmo, olkedy=80%cosmo — all 100%B) = double-prefixed cosmo content.
- ol-closers: oly=81.8%LL, oldy=66.7%LL, olam=100%LL. ol self-chains: post-ol=ol 1.89×.
- Morphological: olkeedy(36) ↔ lkeedy(36) = same frequency → ol = o-prefix + l-stem word.
- ch+eo vowel gradient: ch+o(2692 tokens)=27% stars → ch+eo(591)=40% → ch+eeo(73)=55% → ch+eeeo(1)=100%. EXACT PARALLEL to suffix gradient edy→eedy→eeedy (36%→48%→63% from F120).
- e-vowel extension is stars-specific at: (1) word-internal ch level, (2) suffix level (edy→eedy), (3) standalone suffix words (triple-vowel F120). Universal stars morphological signal.

**COSMO=ol-DOMINANT (2.06×), qok-DOMINANT (1.75×), s-LINE-OPENER (17.7%), -y LINE-CLOSER (25.5%); STARS=ch-DOMINANT (BASELINE), ot-ELEVATED (1.43×), -am LINE-CLOSER (17.0%), ch+eo EXCLUSIVE; ASTRO=HETEROGENEOUS (f67=TRUE ASTRO: y-s-ELEVATED/qok-DEPLETED; f68/f70=A-HERBAL-LIKE) (F140, exp_133)**
- Cosmo onset: ol=2.06×, qok=1.75×, qo=1.40×, sh=1.27×, s=1.52× vs corpus baseline. Stars onset: ot=1.43×, l=1.72×, ok=1.16×, other=1.20×; ch near-baseline (0.98×).
- Suffix: cosmo -edy=19.23% (2.01× stars); stars -am=2.11% (3.1× cosmo, confirms -am=8.06× line-end from F138); cosmo -y=11.55% (1.49× stars).
- Vocabulary Jaccard=0.178 (distinct sections). Stars-exclusive: ch+eo words (cheo/cheody/cheeo); cosmo-exclusive: qol-prefix forms (qolchedy/qoly).
- Line-first: cosmo=s(17.7%)+qok(16.9%); stars=d(16.3%)+p(14.7%)+y(14.2%). Line-last: cosmo=-y; stars=-am.
- Astro=heterogeneous: f67 (y=2.36×, s=2.15×, other=1.87×, qok=0.33×) vs f68/f70 (A-herbal-like, pairwise sim=0.953). f67 vs f68 sim=0.558 explains low cohesion=0.886.

**B-HERBAL FOLIOS UNIVERSALLY DEPLETED IN cth (A-NOMINALS, mean_dev=-0.037) AND d (A-FUNCTION WORDS, mean_dev=-0.062); f40 ok=16.1% (3.8× A-HERBAL) → STARS BEST-MATCH; s-ONSET = LINE-OPENER (LF=48.9%); s-OPENERS (saiin/sol=50-72%LF) + s-CLOSERS (sy=85%LL, sam=89%LL); Post-s sh=1.92× (s→sh RULE); FOUR LINE-OPENER CLASSES: y/p/d+ch-sh/s (F139, exp_132)**
- B-herbal (12 folios by dialect): universal cth depletion (B-herbal nearly CTHLESS, A-herbal=4.5%) and d depletion (37% fewer d-words). Elevated ok/qok/other (B-content classes).
- f40→stars mechanism: ok=16.1% (3.8× A-herbal rate, close to stars=7.0%). f26/f31/f50→pharma (pharma also has elevated qok vs A-herbal). f48→astro (elevated ot/t).
- s-onset: LF=48.9% (pure line-opener, vs d=20.5%LF). Two sub-classes: s-OPENERS (saiin 50%LF, sol 64%, soiin 72%, sshedy 100%LF) and s-CLOSERS (sy=85%LL, sam=89%LL — parallel to dy/dam).
- Post-s sh=1.92× (s→sh opener-to-content rule, same as stars line template [opener][sh-2nd]).
- s is COSMO/ASTRO-concentrated (1.52×/2.15×), NOT stars-concentrated (stars=0.67×). Stars s-words are rare but 67.2% LF in stars context.
- FOUR LINE-OPENER CLASSES: y (k/t stems, both dialects, 39.6%LF), p (B+ch/sh, 71.1%LF), d+ch/sh compounds (A+B, dialect-split), s (various stems, cosmo/pharma, 48.9%LF overall).

**27% of FOLIOS BEST-MATCH ≠ ASSIGNED SECTION; B-HERBAL BIFOLIO INSERTIONS (f26/f31/f40/f48/f50) CLUSTER with Pharma/Stars; HERBAL=LEAST COHESIVE (0.914), COSMO=MOST (0.965); STARS LINE TEMPLATE: [p/s/y/d/t OPENER (5-7×)][sh 2nd (2.25×)][mid content][-am LAST (8.06×=STRONGEST POSITIONAL SUFFIX IN MANUSCRIPT)] (F138, exp_131)**
- Cosine similarity on folio onset-class profile vectors: 25/94 folios (27%) best-match a different section. Section cohesion: cosmo=0.965 > stars=0.954 > pharma=0.940 > herbal=0.914 > astro=0.886.
- B-herbal bifolio insertions (f26/f31/f40/f48/f50) all mismatch: f40→stars(0.860 vs self=0.755), f48→astro(0.890), f50→pharma(0.893), f26→pharma(0.966), f31→pharma(0.959). Confirms bifolio insertion hypothesis from F123.
- f103 (first stars folio) best-matches cosmo (transitional folio). A-herbal folios f3/f17/f24/f34 best-match pharma (herbal-pharma onset continuum).
- Stars line-element template: [p/s/y/d/t OPENER at position-1: p=6.84×, s=6.56×, y=5.10×, t=3.75×, d=3.56×][sh-word at position-2: 2.25×][B-content middle][r-closer(2.55×) OR -am LAST(8.06×)].
- -am=8.06× at line-end = strongest positional suffix enrichment in the entire manuscript. Stars is most line-opener constrained section.
- Per-folio: lines=50-105, words/line=8.7-10.9. Dominant opener varies by folio (f112=s, f107/f113=p, f104/f106/f114=y, most=d).

**d-ONSET = THREE SUB-CLASSES: d+ch/sh OPENERS (dshedy=90.9%LF/B; dchor=59.1%LF/A), d-CLOSERS (dan=100%LL, dam=67.9%LL, dy=40.3%LL), MEDIAL FUNCTION WORDS (daiin=61.5%MID); ok/ot BODY = B-Dialect Content Nouns (81-82%MID, Stars/Cosmo 38-45%) (F137, exp_130)**
- d-grammar: three positional sub-classes. d+ch/sh openers dialect-split (dshedy/dchedy=B; dchor/dchol=A). d-closers: short words with -am/-an/-y/-al suffix (dan=100%LL, dam=67.9%LL). Medial: daiin/dol/dar (60-80%MID). d+gallows (dk/dt) = rare (23 tokens). d-chain weak.
- ok/ot/ol body words: B-dialect medial content nouns (81-82%MID). stars/cosmo 38-45%. Low label overlap (Jaccard=0.197/0.139/0.062). ok/ot body = B-dialect nominal class parallel to A-dialect cth-nouns. Line-closers: oly=81.2%LL, otam=62.8%LL.

**p+r NOT Mandatory Bracket (1.29×); raiin=B-Stars Medial Particle (pre-s=3.25×, post-ot=2.36×); raiin≠daiin (No post-raiin cth) (F136, exp_129)**
- p+r co-occurrence in B-dialect lines = 1.29× enriched vs independence (13 vs 10.1 expected). p and r are INDEPENDENT positional markers, not a mandatory line-bracket.
- raiin (n=61, 93.4% B, 63.9% stars): preceded by s-onset=3.25× (topic openers), ch=1.68×; NOT preceded by "other" (0.13×). Followed by ot=2.36×, sh=1.81×. NOT a daiin equivalent (no post-raiin cth enrichment).
- raiin = B-stars medial particle with context [s-opener][content][raiin][ot/sh]; aiin = more general medial particle (pre-other=2.21×, post-ok=2.70×).

**POSITIONAL PREFIX SYSTEM: p=LINE-OPENER (ch/sh-stems, 71.1% line-start, B-dominant); r=LINE-CLOSER (PARTICLE STEMS, 28.7% line-end, 8.3×B); p/r BRACKET B-dialect Lines; r Creates "Prefixed Particles" raiin/rain/rar/ral/ror/ram (F135, exp_128)**
- p-prefix: 523 tokens, 285 types; A/B=0.31 (3.3×B); line-start=71.1% (5.72×); stars=43.4%, cosmo=16.8%. Stem: ch=45.5%, ol=16.8%, sh=8.6% — DISTINCT from y/qo/o (which select k/t). pchedy=35 (100%B).
- r-prefix: 341 tokens, 117 types; A/B=0.12 (8.3×B); line-end=28.7%; stars=51.6%, cosmo=32.6%. Attaches to PARTICLE STEMS (64.5%: aiin/ain/ar/al/or/am). Creates raiin(61), rain(21), rar(17), ral(15), ror(14), ram(11).
- COMPLETE POSITIONAL PREFIX SYSTEM: y/p=OPENERS (y=both+k/t; p=B+ch/sh); qo/l/o=CONTENT MODIFIERS; r=CLOSER (B+particles). y and p are STEM-CLASS SPECIFIC openers. r is the only prefix that selects PARTICLE stems.

**y-PREFIX = GRAMMATICAL LINE-CONTINUATION OPENER; Splits A-y (y+A-paradigm, B%≤25%) vs B-y (y+B-paradigm, B%=100%); y Selects k/t-Stems (65.4%) = Same as qo-/o-; A/B Jaccard=0.174; 4-gram Template Enriched 4.92×; aiin→am=Distributional Not Fixed Phrase (F134, exp_127)**
- y-prefix: 1,372 tokens, 488 types; A/B ratio=0.81 (balanced); line-start=39.6% (grammatical position opener).
- A-y sub-type: y+A-paradigm (ycheor/ydaiin/ytchy, B%≤25%, herbal 60-88%) — A-dialect continuation particle.
- B-y sub-type: y+B-paradigm (yteedy/ykeedy/ykedy, B%=100%) — B-dialect formula opener.
- Both sub-types select k/t-stems (65.4%) = same selectivity as qo-/o-. A/B Jaccard=0.174 (near-distinct vocabularies).
- Extended k/t-stem prefix paradigm: bare=A-herbal, y=both+line-initial(grammatical), o=labels, qo=B-body, l=B-stars/cosmo.
- 4-gram [-ol/-or][aiin][cth][-am/-dy/-al] enriched 4.92× (3 observed/0.6 expected; all A-herbal); 3-gram has 23 matches.
- aiin→am=4.62× is distributional (67 bigrams/57 pairs; NOT fixed phrase). -am is universal line-closer; aiin→am is co-occurrence in same line.

**cth = SEMI-CLOSED NOMINAL CLASS (Top5=55.4%, Herbal+Pharma=90%); Within-Line A-DIALECT SUFFIX GRAMMAR: -or(FIRST) → -ol → -aiin(MIDDLE) → -dy/-al → -am(LAST); aiin→am=4.62×; B Flatter (F133, exp_126)**
- cth top5 concentration=55.4% (vs ch=28.1%, sh=36.8%) — 2× more concentrated; marks specialized herbal/pharma nominal vocabulary (plant names, preparations). NOT a productive prefix.
- cth section distribution: herbal=71.0% + pharma=18.9% = 90% of tokens — most section-specialized onset class. Essentially absent from cosmo/stars (B-sections).
- A-cth has 85 types, 398 tokens (71.6% hapax in herbal); B-cth has 20 types, 57 tokens (hybrid forms: cthedy/cthdy). A/B Jaccard=0.117 (distinct vocabularies).
- Within-line suffix positional order (A-dialect): -or(0.371) < -ol(0.441) < -ey/-aiin(0.45-0.53) < -dy/-al(0.584-0.586) < -am(0.799). Full line grammar = NP template extended: [-or/-ol modifier] → [-aiin determiner] → [cth-noun] → [-dy/-al/-am closer].
- -or enriched at 0-20%(1.51×); -dy/-al enriched at 80-100%(1.51×/1.50×); aiin→am=4.62× (strongest suffix bigram).
- -am = universal line-final closer: A mean=0.799, B mean=0.925. B-dialect less positionally structured (same directionality, flatter gradients).

**SEVEN-PREFIX SYSTEM: o-/qo-/l-/r-/p-/y-/cth-; ok-/ot-/qok-/qot-Onset = PREFIXED DERIVED FORMS (NOT Primitive Stems); qo-Prefix k/t-Selective (Not ch/sh); B-cth=Hybrid Words cthedy/cthdy (B_frac=0.917/1.000); B-cth→cth=n=1 Only (F132, exp_125)**
- ok-onset (okaiin=201) = o-prefix on k-stem; ot-onset (otaiin=137) = o-prefix on t-stem; qok-onset (qokaiin=265) = qo-prefix on k-stem; qot-onset = qo-prefix on t-stem. These are NOT independent onset classes.
- qo-prefix is EXCLUSIVELY k/t-stem selective: qochedy=1 (absent), ochedy=8 (rare). ch/sh-stems take ONLY l-prefix (lchedy=116). Resolves why qo-stripping finds k/t-initial stems.
- New prefix classes: r- (346 tokens, 87.0% stem recovery, 8.4× B, stars 51%); p- (528 tokens, 76.1%, 3.4× B, stars 43%); y- (1374 tokens, 85.6%, balanced A/B).
- B-dialect cth (n=55): cthedy (B_frac=0.917) and cthdy (B_frac=1.000) are hybrid morphological forms — B-paradigm suffixes (-edy/-dy) applied to cth-onset. Concentrated in B-herbal folios f26/f48 (~20‰) and stars f113/f116.
- exp_123's B-cth→cth=8.79× was a single-token artifact; actual B-cth self-clustering = n=1 only.
- Primitive stem classes (revised): ch / sh / k / t / r. Prefixes: o- / qo- / l- / r- / p- / y- / cth-.

**FOUR-PREFIX SYSTEM: o-/qo-/cth-/l-; k-Stems Generate (bare-k/qo+k/l+k) Paradigm; l Is B-Dialect Prefix (91.3% Stem Recovery, 10.3× B-Dominant); lk=80% Stars; kaiin Folios=Herbal vs lkaiin Folios=Stars/Cosmo (Disjoint) (F131, exp_124)**
- 'l' is a B-dialect morphological prefix with 91.3% stem recovery (qo=54.8%, o=50.4%) — most transparent prefix. l is 10.3× B-dominant (50.66‰ B vs 4.93‰ A).
- l-words: stars-enriched (1.83×), cosmo (1.42×); herbal/pharma depleted (0.22×); astro absent. l-suffix: -edy=2.32× (B-paradigm); -y depleted (0.50×). lk-subclass = 80% stars, n=415.
- k is a stem-initial segment generating THREE-PREFIX paradigm: bare-k (A-herbal, folios 1-56), qo+k (B-body), l+k (B-stars/cosmo, folios 75-116). kaiin folios=[1-56] ≠ lkaiin folios=[75-116] (section-disjoint).
- **FOUR prefixes confirmed**: o- [labels, k/t stems]; qo- [B body, k/t stems]; cth- [A body, o/y/e stems]; l- [B stars/cosmo, ch/sh/k/d stems]. The prefix system encodes BOTH register (label vs body) AND section/dialect.
- H249 CONFIRMED (F132): Paradigm generalizes — ok/ot/qok/qot are all derived; qo-prefix k/t-selective; ch/sh take l-only. New H251: Full characterization of y-prefix class (1374 tokens, balanced dialect).

**Onset Grammar Probabilistic; cth→cth=4.78×=Only Mandatory; cth↔d Cycle=2.20×; Stars l-/k-Onset = NEW B-Dialect Prefix Classes; lkaiin=81% Stars; Stars Line-Start=y-/p-Openers; Line-End=am-Particles (F130, exp_123)**
- Onset transition grammar is probabilistic — no forbidden transitions found. One mandatory pair: cth→cth=4.78× (cth-noun self-clustering).
- cth↔d mutual cycle (cth→d=2.18×, d→cth=2.21×, mean 2.20×) is dominant syntactic pattern. sh→qok=1.99× (B-paradigm). ot→ot=1.95×, qot→qot=2.34× (self-clusters). s-onset = most constrained predictor (H=-0.169 bits).
- Stars "other"-onset = (1) standalone particles (aiin/ar/al/or/am = 33%); (2) **l-onset** (lchedy, lkaiin=81% stars, lkeedy — new unrecognized prefix class); (3) **k-onset** (kaiin, keedy, keey — 47-55% stars); (4) y-/p-prefixed formula openers (ycheey, yshey, polaiin) at line-start; am-particles at line-end.
- lkaiin = most stars-concentrated token in manuscript (81% of all lkaiin appear in stars). l-/k-onset likely constitute unrecognized B-dialect prefix classes.

**-ol=Pre-Determiner (d-Onset 1.44-1.66×); -or=Pre-Nominal (cth 2.15×, sh 1.57×); B-otaiin→ot=4.00× MIRRORS A-daiin→cth=2.77×; Dialectal NP Complementarity: A=[ch-ol/or][daiin][cth]; B=[ot/ok][otaiin][ot] (F129, exp_122)**
- -ol suffix = pre-determiner position: chol→d=1.66× (chol → daiin → cth-noun is 3-word A-NP template via determiner)
- -or suffix = pre-nominal position: chor→cth=2.15× (chor → cth-noun is 2-word direct A-NP)
- shor→sh=2.84× (same-class sequencer); full suffix matrix: aiin=2.24× cth; ey/dy/eey=pre-qok (1.57-2.48×); al=pre-d (1.47×, depletes cth 0.43×); ar=pre-sh (1.45×)
- B-otaiin→ot=4.00× exactly mirrors A-daiin→cth=2.77×. B-NP: [ot/ok-modifier][otaiin][ot-noun]. A-NP: [ch-ol/or][daiin?][cth-noun].
- Pre-otaiin top word = okaiin (4×) — -aiin chain: okaiin→otaiin→ot-noun. Pre-shedy: qok→shedy→qok=1.79× (B-paradigm self-reinforcing qok sequence).

**A-Dialect NP Template: [chol/shol/chor][daiin][cth-noun]; d-Depleted Before daiin (0.60×); Stars=All-B (12/12), No Fixed Line Template, ot-Enriched in 2nd Half (1.75×), s-Onset Line-Start Only (F128, exp_121)**
- A-dialect 3-word NP template: [W1][daiin][cth-noun] where W1 is ch-onset (1.94×) with -ol suffix (2.48×). Top W1 words: chol, shol, chor. W0 (4-gram) shows no pattern — phrase is exactly 3 words.
- General pre-daiin pattern: ch-onset=1.33×; d-onset DEPLETED (0.60×) — d-words don't precede daiin. Top pre-daiin: chol (31), shol (9), chor (9), daiin→daiin chains (8).
- Stars = 100% B-dialect (all 12 present folios). No repeating line template (all 580 lines unique). Positional structure: pos-0 highly constrained (H=-0.532; 48% "other", 16% d, 13% s); mid-line near-baseline; ot-onset enriched in 2nd half (1.75×), s-onset depleted in 2nd half (0.28×). Template: [d/s-opener][B-content][ot-nominal][other-closer].
- otaiin→ot=3.99× in stars (n=53) — confirmed ot-determiner in B-dialect star entries.

**Bigram Split by Dialect: A-daiin/chol/shol→cth; B-chor=19.04×→cth; cth=15× More A; chedy→qok=23.31× in A-Only; otaiin→ot=4.27×; aiin→ok=2.5× (F127, exp_120)**
- Pre-cth is A-dialect rule: daiin/chol/shol appear before cth only in A-dialect (zero in B). cth = 39.29‰ A vs 2.57‰ B (15× ratio). In B-dialect, chor→cth=19.04× (rare B-text cth occurrences).
- Pre-qok: shedy→qok B-ONLY; chedy→qok=23.31× in A-text only (B-words in A-context). daiin is top A-dialect precursor of BOTH cth (2.64×) AND qok (5.2% of cases).
- otaiin = ot-class determiner (4.27×, stars-dominated 7.30‰, B-dominant). aiin→ok=2.5×. -aiin words form chains.

**Bigram Syntax: [A-Suffix]→cth (chor=4.73×), [B-Suffix]→qok (shedy=3.75×); d-Onset = Function Class (H_pos=1.424 vs ch=0.699); s=Para-Start; or/ar/al Most Constrained (F126, exp_119)**
- Pre-cth cluster: chor→cth=4.73×, daiin→4.38×, chol→3.40× — A-paradigm words systematically precede cth-onset nouns. Structural rule: [A-suffix] → [cth-noun].
- Pre-qok cluster: shedy→qok=3.75×, chedy→2.69× — B-paradigm words precede qok. Structural rule: [B-suffix] → [qok-word].
- d-onset function class: H(position)=1.424 (ch=0.699, sh=0.675). Roles: dshedy=93.1% first (topic), daiin balanced (determiner), dam=68.6% last (closer). s-onset: 48.5% first (para-opener).
- 'or'/'ar'/'al' most collocationally constrained (H=1.98-2.23 vs baseline 3.13).
- Structural model: s=para-start → d=function → ch/sh=content → cth=A-noun → qok=B-cluster.

**daiin = Pre-Nominal Determiner: A-Dominant (3.5×), After-daiin cth 4.89×; -am/-air Are B-Dominant (NOT A-Paradigm); 'Other' Reduced to 17.9% (F125, exp_118)**
- daiin: 2.39% of body, 45.87‰ A vs 13.05‰ B (3.5× A-enriched). After-daiin cth-onset = 4.89× enriched — strongest bigram association in manuscript. daiin = pre-nominal determiner before cth-nouns. Lines with daiin are 0.64 words shorter.
- -am (519 tok) and -air (293 tok) are B-DOMINANT (A/B=0.44 and 0.32) — NOT A-paradigm as expected. Both stars-concentrated, cosmo-depleted. Adding them reduces 'other' from 20.6% to 17.9%.
- d-onset word roles: dshedy=93.1% line-first (topic marker), dam=68.6% line-last (closer), dy=43.1% last, daiin=20.2% first/17.5% last (balanced determiner).

**'Other' 20.6% = Free A-Morphemes + Unrecognized -am/-air + Short Forms; Adjacent Paras Share 1.85× Non-Adjacent Vocab; daiin in 41% of Paras (F124, exp_117)**
- 'Other' top words: ol (476), aiin (394), or (300) — standalone free A-morphemes (confirms F118 free-morpheme asymmetry). Unrecognized suffixes -am (~570 tok) and -air (~450 tok) account for 16% of 'other'.
- Adjacent paragraphs have 1.85× higher vocabulary overlap than non-adjacent (0.084 vs 0.045 Jaccard) — genuine discourse cohesion. daiin appears 3+ times in 41% of all paragraphs.
- Stars highest within-para repetition rate (0.476; star catalog structure). Astro lowest (0.062).

**Herbal B-Folios Absent in Q1-Q3; Cluster at Quire Boundaries in Q4-Q7 (Bifolio Insertion); Lag-7 Autocorr=+0.580; Line-FIRST ch/ok Reverses to eey (58%); Line-LAST = -y Closure (F123, exp_116)**
- Herbal quires 1-3 (f1-24): pure A-dialect. B-folios appear only Q4-Q7, at quire boundary positions (1-2, 7-8 of each 8-folio quire). Consistent with bifolio insertion as outer sheets.
- Line-LAST enriches -y (1.83×), -dy (1.55×), suppresses all B-suffixes. Line-FIRST enriches -or (2.05×). B-dialect ch/ok at line-first: eey=58% (vs 20% mid). A-dialect at line-last: y=49-66%.
- Five-level hierarchy: Dialect=0.11b + Onset=0.16b + Section=0.10b + Vowel-length=0.35b + Line-pos=0.037b = 0.75 bits resolved (21.2% of marginal H).

**Folio Suffix Profiles Cluster by Section (73.1%); Herbal A/B ALTERNATES Every 3-5 Folios; cosmo-pharma Sharpest Boundary; f107 Only eey-Dominant Folio (F122, exp_115)**
- Cosine similarity on suffix rate vectors: cosmo=0.923 within (most coherent); herbal=0.779 (most heterogeneous — A/B dialect folios interleaved)
- Herbal B-dialect folios alternate with A-dialect every 3-5 folios (f26/31/33-34/39-41/43/46/48/50/57): regular pattern → two-source manuscript compilation hypothesis.
- cosmo→pharma boundary: sharpest in manuscript (f84→f87 similarity drop to 0.479). astro vocabulary-isolated (Jaccard=0.04-0.10).
- f107: ONLY folio in manuscript where eey > edy (44% eey). f79 (cosmo): outlier with 34.5% eey (nearly stars-level).
- cosmo-stars highest Jaccard overlap (0.391); both B-dialect sections share vocabulary more than any other pair.

**Four-Level Hierarchy Quantified: 20.1% Entropy Reduction (0.71/3.54 bits); Vowel Length Contributes MOST (0.35 bits); Residual 2.83 bits (F121, exp_114)**
- Marginal suffix entropy H = 3.54 bits. Full four-level conditioning reduces to 2.83 bits (20.1% reduction; 0.71 bits resolved).
- Per-level contributions: dialect=0.11b, onset=0.16b, section=0.10b, vowel_length=0.35b. Vowel length (L4) > Levels 1–3 combined per-level.
- A-dialect consistently has lower within-class entropy than B (e.g., qot-A=2.94 bits vs qot-B=3.59). A is more morphologically regular.
- Per-onset dialect information: qot=0.207b (highest polarity); ol=0.035b (lowest — ol is both suffix and onset class).
- 20% reduction comparable to agglutinative natural language morphological conditioning (15–30% typical range).

**B-Paradigm Suffix Is a THREE-TIER Register System: Dialect (B-paradigm) → Stem Class (Simple-B/Complex-B) → Section (stars→eey; cosmo→eedy; herbal→baseline) (F119, exp_112)**
- Stars B universally elevates -eey (highest rate across ALL onset classes; monotonic gradient stars>cosmo>herbal). Cosmo B elevates -eedy for qo-prefix stems (qok=35%, ok=38% eedy) but NOT ch/sh. -edy dominance erodes herbal→cosmo→stars.
- Same vocabulary across sections (qokedy/qokeedy/qokeey all present everywhere), different proportions. Stars-exclusive: triple-vowel forms (oteeey=7, cheeey=6, lkeeey=7).
- THREE-TIER B-SUFFIX REGISTER: (1) Dialect: B vs A; (2) Stem class: ch/sh→-edy; qok/ok→balanced; (3) Section: stars→-eey (universal), cosmo→-eedy (qo-prefix only). B-words encode dialect+stem class+section simultaneously.

**Three-Layer A/B Morphological Asymmetry: Onset Markers, Suffix Origins, Secondary Suffix Structure — A Is Older/Conservative; B Is Newer/Innovative (F118, exp_111)**
- olk-: B-dominant (9.5× B/A), B-exclusive top words, section-complement to cth- (olk-=cosmo/stars; cth-=herbal/pharma), suffix-complement (olk-enriches eedy/eey; cth-enriches or/ol/y). BUT olk- is MID-LINE (LLast=11.7%), not a closer like cth- (LLast=20.2%). No B-exclusive onset-based CLOSER exists.
- Secondary B-suffix split: ch/sh = Simple-B (-edy dominant, 68-69%, H=1.16-1.21 bits); qok/ok = Complex-B (balanced edy/eedy/eey, H=1.57-1.58 bits). Stars B→-eey; Cosmo B→-eedy; Herbal B→-edy. A-dialect: NO secondary suffix split.
- Free-morpheme asymmetry: A-paradigm suffixes are GRAMMATICALIZED FREE WORDS (ol=523, or=356, aiin=458 standalone); B-paradigm suffixes are NON-FREE (edy=2, eedy=5 standalone). standalone dy = A-closer (LLast=42.9%); y=ZERO standalone.
- KEY ASYMMETRY: A-dialect=morphologically OLDER (onset extensions + grammaticalized free-morpheme suffixes); B-dialect=NEWER (non-free -edy/-eedy/-eey innovation + secondary stem-level suffix specialization).

**Para-Internal Grammar Is STEP FUNCTION (Lines 1-2 Grammar-Heavy → Content Throughout → -am Last 3-5 Lines); Dialect Polarity ASYMMETRY: A=Onset-Encoded; B=Suffix-Encoded (F117, exp_110)**
- Paragraph-internal grammar is a two-zone STEP FUNCTION: Grammar Zone (lines 1-2: PARA tier at 5.0%/3.7%, 3.5× average) → Content Zone (lines 3+: PARA tier drops to 0.2-1.9%). Transition is SHARP at line 3, not a smooth arc.
- -am closing markers appear in last 3-5 lines (1.3-2.05%, absent from lines 1-2). Para-final words: A-paradigm content forms (chor=3.0×, ain=3.6×, chol=2.1×). Para-first words: MID-tier content (shey=2.9×, oty=4.1×). B has stronger grammar zone (6.0% at line+1 vs 4.1% in A).
- Dialect polarity axis is ASYMMETRIC: A-extreme = ONSET-encoded (cth-=14×, ctho=60.8×, ckho=45.3×); B-extreme = SUFFIX-encoded (-edy on any onset class). No B-exclusive onset MORPHEME paralleling cth- exists. olk-cluster is closest B-structural class (B/A=9.5×, stars/cosmo).
- KEY ASYMMETRY (F117): A-dialect encodes dialect identity through ONSET morphemes (cth-); B-dialect encodes it through SUFFIX choices (-edy). B added -edy paradigm onto existing onset classes; A retained onset-extended morphology.

**-am Class Dialect-NEUTRAL Overall but Dialect-SPLIT Within; No 4-gram Cross-Folio Repetition; cth- Is Most A-Exclusive Onset Class (14× A/B), Gallows-Extended A-Dialect Closer (F116, exp_109)**
- -am class is dialect-neutral at class level (A/B=1.00×) but SPLIT within: A-onset-prefixed -am words (dam=3.1×, cham=3.5×, sam=11.6×) are A-dominant; qo/o-onset-prefixed -am words (qokam=0.3×, ram=0.2×) are B-dominant. Onset, not -am suffix, determines dialect identity. All -am words are LINE-CLOSERS (LL=60-100%). cosmo B suppresses -am (6.83‰ vs 22-41‰).
- 4-gram cross-folio repetition: only 1/16,210 unique 4-grams repeats (0.006%). 5-grams: 0 cross-folio. Voynichese generates compositionally unique word sequences per folio. Consistent with Heaps' β=0.66-0.74 and 72-79% section-specific vocabulary.
- cth- onset: most A-exclusive onset class (14× A/B), line-closer (LLast=25-26% in A), A-paradigm suffix dominant (enriches -y=2.16×, -or=2.24×, -ol=1.96×; suppresses -edy=0.33×, -eedy=0.06×). Concentrated in herbal/pharma (24-38‰), nearly absent in stars/cosmo (~2‰). Low stem overlap with qo/o (17-24%) — NOT a parallel prefix system.
- DIALECT POLARITY AXIS (F116): Onset classes encode dialect polarity on a gradient: cth- (extreme A, 14×) → d-onset (moderate A, closer) → ch/sh/qo (paradigm base) → s-onset (B-shifted, opener). A/B paradigm is graded, not binary.

**s/d-Onset Are Frequency-Complementary (Not Strictly Complementary); Grammar/Content Split Is at STEM Level With 3+ Bit Entropy Gap (F115, exp_108)**
- s/d co-occurrence = 0.97× (near independence): NOT in strict complementary distribution. s-opener lines suppress d (0.67×), but d-openers do not suppress s. B-dialect uses s-openers 1.78× more; cosmo B strongly prefers s-openers (s/d=2.98×); pharma A slightly prefers d-openers.
- Grammar/content distinction is at the STEM level, not onset-class level. All onset classes have narrow 3.25-3.79 bit entropy range (0.55 bits total). Grammar particles (-am closed class: cham, otam, dam, okam, ram): H=0.0-0.3 bits — FIXED FORMS, no suffix variation. Content stems (ch, sh, qok, ok, ot): H=2.9-3.4 bits — 6-8 productive suffix types.
- TWO-TIER VOCABULARY with 3+ bit entropy gap: (1) CLOSED GRAMMAR CLASS (H≈0): -am/-oly words = invariant particles; (2) OPEN CONTENT CLASS (H≈3 bits): ch, sh, qok, ok = paradigmatic stems. This is a sharp, natural-language-like grammar/content boundary.

**A/B Suffix Paradigm Is UNIVERSAL Across All Onset Classes; s/d-Onset Are Complementary Line-Openers With Opposite Suffix Alignment (F114, exp_107)**
- Universal paradigm (H205): All 16 onset classes show same A/B split direction. A-type (-ol/-or/-y) more common in A; B-type (-edy/-eedy) more common in B. Magnitude: bare_t=12.6× B-ratio (strongest), d+gallows=9.3×, bare_ch/sh=5.4-5.7×, bare_d/bare_s=5.2-5.7×. d/s-onset in A-dialect: ZERO -edy/-eedy (absolute suppression). The paradigm is a SINGLE DEEP GRAMMATICAL RULE governing all onset classes.
- s-onset (11.8% of tokens) is a LINE-OPENER class (LFirst=18.7%, LLast=9.9% — unidirectional opener). s+vowel = strong opener (saiin=51%LF, sain=60%LF, sor=66%LF, sol=63%LF). Same vowel/consonant split as d-onset.
- s-onset and d-onset are SUFFIX OPPOSITES: s enriches -edy (1.40×) + -ey (1.52×), suppresses -aiin (0.73×). d enriches -aiin (3.08×), suppresses -edy (0.16×). s=B-paradigm aligned; d=A-paradigm aligned.
- Both s/d-openers are followed by qo at 2.16-2.48× enrichment — SAME grammatical function despite opposite suffix alignment.
- TWO LINE-OPENER CLASSES: (1) s-onset = B-paradigm, unidirectional opener, -edy/-ey rich; (2) d-onset = A-paradigm, bidirectional opener+closer, -aiin rich. Both lead to qo mid-line.

**d-Onset has VOWEL/CONSONANT split (line-opener vs closer); o-Prefix body words (19%) obey A/B suffix paradigm universally (F113, exp_106)**
- d-onset (8.2% of tokens) VOWEL/CONSONANT split: d+vowel (daiin, dain, dair, dor) = LINE-OPENERs (24-37% LFirst); d+consonant (dal, dam, dy, daly) = LINE-CLOSERs (30-70% LLast). d+gallows (LINE_OPEN tier) = strongest line-openers (64-79% LFirst).
- d-onset suppresses B-type suffixes in BOTH dialects: -edy=0.16×, -ey=0.15×, -eey=0.13× (d-onset words are morphologically A-aligned regardless of dialect context).
- A bare_d: more closing (LLast=31.5%); B bare_d: more opening (LFirst=20.7%). D-chain: 18% of lines after d-closer start d-onset (A=19.6%, B=14.2% — weak but real).
- o-prefix body words = 19.0% of all tokens (5,384 tokens). Low label overlap (10.8%) but 28.3% stem overlap with qo-body (shared stems = k/t-initial, F043 confirmed). Sub-class positional roles: or-onset = strong closer (LL=40.6%); ol-onset = moderate closer (LL=24%); ok/ot = mid-line content (LL=14-16%).
- UNIVERSAL A/B PARADIGM: o-prefix obeys SAME A/B suffix split as ch-stems: A-dominant o-forms use -ol/-or (otchol=44.4×A; okol=5.8×A); B-dominant use -edy/-eedy (otedy=69.3×B; okedy=∞B; okeedy=49.2×B). The suffix paradigm governs ALL onset classes — it is a GRAMMATICAL property of the dialect, not lexical.

**"OTHER" tier (43.8% of tokens) has clear sub-structure; Zipf α=1.050; 44 universal words = 21-28% of each section's tokens (F112, exp_105)**
- OTHER tier sub-structure: (1) o-prefix content words (ok/ot/ol+anything = 37% of OTHER) — body-text object vocabulary linked to label system; (2) d-onset line-boundary words (19%): dal=30% LL, dam=70% LL, dy=46% LL (closers); dain=30% LF (opener); (3) aiin/ain particles (9%); (4) s-onset openers (saiin=51% LF, sain=60% LF = 6%). OTHER skewed SHORT (2-char 2.25×; 7-char 0.57×). qo-onset 0.08× suppressed in OTHER.
- Zipf's law: α=1.050 overall (NL range 1.0-1.5). By section: B cosmo=1.105, B stars=0.979, A herbal=0.876, A pharma=0.819. Heaps-Zipf deviation (observed α=1.05 vs predicted 1.34 from β=0.744) indicates Zipf-Mandelbrot pattern — no single dominant "the"-equivalent. daiin (rank 1) = only 2.5% of corpus. Section-specific function words dilute corpus-wide rank.
- Universal vocabulary: 44 words appear in ALL 5 large sections at ≥3 tokens. Universal tokens = 21-28% of each section (consistent). Universal tier composition: OTHER (57%: daiin, ol, aiin, or, dar) + MID (41%: chol, qokeey, chey, shey). No PARA-tier words are universal. Remaining 72-79% of each section = section-specific content.
- Section-exclusive words: B_stars=215 (most diverse; consistent with highest Heaps' β=0.735); A_herbal=144 (cth-cluster exclusives: cthor, dchor, kchy, dchy); B_herbal=12 (fewest, shares most with other B sections).
- THREE-LAYER VOCABULARY MODEL: (1) Universal function-word core (21-28% tokens): 44 words crossing all sections; (2) Section-specific content (72-79%): section-restricted vocabulary; (3) OTHER tier = o-prefix body-objects + d-boundary + particles (43.8% all tokens).

**Voynichese follows Heaps' law; section-level β=0.661-0.744 (upper end of NL range); "chd" is NOT a B morphological unit (F111, exp_104)**
- Heaps' law: V=K×N^β confirmed at section level. B cosmo=0.674 (most repetitive); A/B herbal=0.744; B stars=0.735; A pharma=0.661 (also within NL range 0.5-0.7). All within natural language range (English prose β≈0.55-0.65); Voynichese slightly higher — consistent with morphologically complex languages.
- Overall A/B β=0.84 is an artifact of cross-section vocabulary divergence; within any section, β is in NL range. This is strong evidence against random/substitution cipher models (which would have anomalous β).
- "chd cluster" (B-exclusive words from F110: chedar, chdaiin, chdal, chdar) is NOT a morphological unit — these are ch-onset words with B-type -edy/-dy suffixes. The 'd' belongs to the suffix. Positional profile of ch+d forms (PS=0.1%, LFirst=1.8%, LLast=11.8%) is identical to all bare_ch in B (PS=0.0%, LFirst=3.7%, LLast=12.1%). chedy (424 tokens) = ch + -edy; chdaiin = ch + -daiin.
- The B ch+d pattern from F110 explained: B's -edy suffix (2.97× enriched in ch+d forms; -y/-ey suppressed 0.06×) applied to ch-stems naturally produces forms that LOOK like ch+d clusters but are morphologically ch-onset + B-suffix.

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
