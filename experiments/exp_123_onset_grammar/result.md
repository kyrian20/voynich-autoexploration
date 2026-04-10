# Experiment exp_123: Onset Grammar Matrix (H244) + Stars "Other" Class (H242)
Date: 2026-04-09

## H244: CONFIRMED (PARTIAL) — cth→cth=4.78× Is the ONLY Mandatory Transition (ALL); NO Forbidden Pairs; Grammar Is Probabilistic Not Deterministic; cth→d=2.18×, d→cth=2.21× (cth↔d Cycle); sh→qok=1.99×, sh→qo=1.95× (B-Paradigm); s-Onset = Most Constrained (Lowest H=-0.169 bits); B-cth→cth=8.79× (Extreme, n=47)

### Full Onset Transition Matrix (All corpus)

| from\to | s | d | ch | sh | cth | ok | ot | qok | qot | qo | ol | H(next) |
|---------|---|---|----|----|-----|----|----|-----|-----|----|----|---------|
| **s** | 1.18 | 0.77 | 1.10 | **1.82×** | 0.83 | 0.87 | 0.60 | 0.56 | 0.33 | 0.66 | **1.52×** | **2.951** |
| **d** | 0.92 | **1.52×** | 1.12 | 1.31 | **2.21×** | 0.83 | 0.76 | 0.67 | 0.68 | 0.92 | 0.94 | 3.120 |
| **ch** | 1.38 | **1.24×** | 1.06 | 0.64 | **1.40×** | 0.96 | 0.89 | 0.99 | 1.05 | 0.96 | 0.83 | 3.100 |
| **sh** | 0.90 | 0.74 | 0.61 | 1.08 | 0.98 | 0.74 | 0.87 | **1.99×** | **1.71×** | **1.95×** | 0.79 | 3.164 |
| **cth** | 1.09 | **2.18×** | 1.11 | 0.67 | **4.78×** | 1.22 | 1.29 | 0.59 | 0.50 | 0.87 | 0.41 | 3.149 |
| **ok** | 0.60 | 1.01 | 1.10 | 0.94 | 0.86 | **1.53×** | 1.10 | 1.11 | 0.63 | 0.79 | 1.03 | 3.107 |
| **ot** | 1.04 | 0.91 | 0.83 | 0.81 | 0.59 | 1.06 | **1.95×** | 0.84 | **1.42×** | 0.78 | 1.11 | 3.134 |
| **qok** | 1.05 | 0.96 | 1.16 | 1.11 | 0.25 | 1.26 | 1.01 | 1.41 | 1.11 | 0.84 | 1.16 | 3.162 |
| **qot** | 0.99 | 1.09 | 1.15 | 0.82 | 0.80 | 0.60 | **1.48×** | 1.00 | **2.34×** | 0.73 | 0.74 | 3.134 |
| **qo** | 1.31 | 0.70 | 1.03 | 1.01 | 0.90 | 0.79 | 0.83 | 1.04 | 1.00 | **1.78×** | 1.08 | 3.114 |
| **ol** | 0.75 | 0.75 | 1.03 | 1.08 | 0.21 | 0.96 | 0.87 | 0.89 | 0.68 | 1.07 | **1.78×** | 3.025 |

**cth→cth=4.78× is the ONLY mandatory pair** (above 3× with n≥5). No pairs are truly forbidden (<0.15). The grammar is **probabilistic, not rule-based**.

### Key Findings

**The grammar cycle that emerges:**
- **cth → d = 2.18×** AND **d → cth = 2.21×** — cth and d are mutually attracted. The "cth↔d" cycle (mean 2.20× per step) is the strongest 2-gram structural pattern: cth-nouns are systematically followed by d-function words, and d-function words precede cth-nouns.
- **cth → cth = 4.78×** — cth-onset words self-cluster! A cth-onset word is likely followed by ANOTHER cth-onset word. This suggests multi-cth nominal sequences (e.g., "compound cth-noun phrases" or coordinations).
- **sh → qok = 1.99×, sh → qo = 1.95×** — sh-onset words are followed by qok/qo-onset words (B-paradigm pattern, confirmed from prior experiments).
- **d → sh = 1.31×** — d-onset also precedes sh (supporting the A→B transition when code-switching).
- **ot → ot = 1.95×** — ot-onset self-clusters (confirmed from exp_121: ot-run length analysis).
- **qot → qot = 2.34×** — qot-onset strongly self-clusters.
- **s → sh = 1.82×, s → ol = 1.52×** — s-onset (para-opener) is followed by sh and ol.

### Entropy Analysis

**s-onset has the LOWEST next-onset entropy (H=2.951; Δ=-0.169 bits from baseline)** — confirming s-onset as a grammatically constrained class (para-opener with specific collocational behavior).

**sh and qok have HIGHEST next-onset entropy (H≈3.16)** — sh and qok are the most "context-free" content classes; their successors are nearly as unpredictable as random.

### A-Dialect vs B-Dialect Differences

**B-dialect cth→cth=8.79×** (n=47, all corpus cth→cth=4.78×) — B-dialect has very few cth words (15× less than A), and when cth appears in B-text, it self-clusters extremely strongly.

**B-dialect sh→qok=2.08×** (vs mixed corpus 1.99×): slightly stronger in pure B.
**A-dialect: d→cth=1.52×** (vs 2.21× in mixed corpus — the mixed corpus inflates this due to B-cth rarity pushing A-A bigrams to dominate the mixed count).

### Grammar Cycle Analysis

| Chain | Mean enrichment |
|-------|----------------|
| cth→d→cth | 2.20× |
| sh→qok→ch | 1.58× |
| ch→d→cth | 1.72× |
| s→ch→cth | 1.25× |
| qok→sh→qok | 1.55× (B-cycle) |

**cth→d→cth=2.20×** is the strongest cycle. **sh→qok→ch and qok→sh→qok** (mean 1.55-1.58×) are B-paradigm cycles. No strong directed "main cycle" spanning s→d→ch→cth is found — mean enrichment only 1.10×.

### H244 Verdict: CONFIRMED (PARTIAL) — The onset transition matrix is probabilistic (no forbidden pairs, one mandatory: cth→cth=4.78×); the cth↔d mutual attraction (2.18-2.21×) is the dominant grammar cycle; sh→qok/qo (1.95-1.99×) is the B-paradigm B-cycle; ot→ot=1.95× confirms ot-self-clustering; s-onset is the most constrained next-onset predictor (H=-0.169 bits); B-dialect cth→cth=8.79× (extreme: very few cth words in B cluster together); NO true forbidden transitions (no zeroes with sufficient n); grammar is probabilistic, not deterministic

---

## H242: CONFIRMED — Stars "Other"-Onset Class Is: (1) Standalone Particles (aiin/ar/al/or, 33% of other); (2) l-/k-Prefixed B-Dialect Words (lchedy, lkaiin, keedy: NEW ONSET CLASS?); (3) y-/p-Prefixed Line-Starters (ycheey, yshey, polaiin); Stars Line-End "Other" = am-Suffix Particles; lkaiin=81% Stars-Concentrated; l-/k-Onset Is Stars-Exclusive B-Dialect Class

### Stars "Other"-Onset Composition

Stars has 3,554 "other"-onset tokens (33.7% of all stars words). The top words reveal THREE distinct word groups:

**Group 1: Standalone particles (no recognized suffix or onset)**
- aiin (207), ar (147), al (138), or (71), ain (56), air (34), am (28)
- These are the same A-paradigm free morphemes seen in exp_117 — but they appear in B-dialect stars!
- aiin is 45% stars-concentrated; al is 65% stars-concentrated; ar is 44%

**Group 2: l-initial compound words** ← NEW FINDING
- lchedy (52), lkaiin (39), lkeedy (30), lkain (28), lkar (22), lkeey (34), lkedy (17), lshedy (14)
- **lkaiin = 81% stars-concentrated** (39 of 48 total appearances are in stars!) ← extreme
- lchedy = 45% stars-concentrated; lkeedy, lkain similar
- These words start with 'l' — a prefix not in the recognized onset taxonomy
- Pattern: l + [ch/sh/k + suffix] — l-prefixed B-paradigm words

**Group 3: k-initial words**
- kaiin (36), keedy (34), keey (21), kain (20), kedy (14)
- kaiin = 47% stars-concentrated; keedy = 55% stars-concentrated
- Pattern: k + [B-paradigm suffix] — k-onset words

**Group 4: Stars line-start "other" words (y- and p-prefixed)**
- ycheey (8), yshey (6), ycheo (5), ykeey (3), ycheedy (2): y-prefixed ch/sh/k-suffix words
- polaiin (5), pcheor (3), pchedal (3), pchodain (3), pchedy: p-prefixed words
- These appear to be y-prefix (like y+ch+ey = ycheey) and p-prefix variants

### Stars Line-Start vs Line-End "Other" Words

| Position | Top words | Pattern |
|----------|-----------|---------|
| **Line-start** | ycheey(8), yshey(6), ycheo(5), polaiin(5), pol(4), tchedy(4) | **y- and p-prefixed** (B-content) |
| **Line-end** | am(16), al(9), lchedy(6), ar(5), ram(4), ary(4) | **-am particles and l-compounds** |

Stars line-START "other" = predominantly y-/p-/t-prefixed B-content words (not the particles).
Stars line-END "other" = predominantly am-suffix particles (am=16!) and short free morphemes (al, ar).

**Overlap between top-20 start and top-20 end "other" words: only 'ar'** — almost no shared words! The "other"-onset class at line-start vs line-end is completely different.

### Stars Folio Variation

f104 and f105 have the highest "other" at line-start (60-68%); f108 and f116 have the lowest (25-28%). This folio variation suggests different content types across the stars section.

### l-/k-Onset: A NEW ONSET CLASS?

The l-initial words (lchedy, lkaiin, lkeedy, lkeey, lkain) and k-initial words (kaiin, keedy, keey, kain) suggest TWO unrecognized onset classes in B-dialect:
- **l-onset**: lch, lsh, lk — combinations of l + standard onset
- **k-onset**: k + B-paradigm suffix (keedy, kedy, keey, kaiin, kain)

These may be additional prefix classes (analogous to 'o-', 'qo-', 'cth-') that are B-dialect exclusive and stars-concentrated.

### H242 Verdict: CONFIRMED — Stars "other"-onset comprises: (1) standalone A-paradigm particles (aiin/ar/al/or/ain/am = 33% of other); (2) l-onset compounds (lchedy/lkaiin/lkeedy: stars-concentrated 45-81%, suggest new 'l-' prefix class); (3) k-onset words (kaiin/keedy/keey: 47-55% stars); (4) y-/p-/t-prefixed line-starters (ycheey, yshey, polaiin = formula openers); stars line-END other = am-particles (am=16 at last position); lkaiin=81% stars-concentrated is the most section-specific word found; l-/k-onset suggests unrecognized B-dialect prefix classes that are stars-exclusive

---

## Combined Finding (F130)

**H244 CONFIRMED PARTIAL (F130)**: The Voynich onset transition grammar is probabilistic — no forbidden transitions (no pairs with enrichment<0.15 at sufficient n). The dominant structural patterns are: (1) **cth→cth=4.78×** (the ONE mandatory transition — cth self-clusters, suggesting compound nominal phrases or lists); (2) **cth↔d mutual attraction** (cth→d=2.18×, d→cth=2.21×, mean cycle=2.20×) — the strongest sustained structural cycle; (3) **sh→qok=1.99×, sh→qo=1.95×** (B-paradigm sh→qok pattern); (4) **ot→ot=1.95×, qot→qot=2.34×** (ot/qot self-clustering); (5) **s-onset most constrained** (H=-0.169 bits). B-dialect shows cth→cth=8.79× (extreme: the rare B-cth words cluster together). No directed "grammatical cycle" spanning all onset classes exists — the grammar is local and probabilistic, not a global sequence rule.

**H242 CONFIRMED (F130)**: Stars "other"-onset class reveals two previously unrecognized B-dialect onset categories: (1) **l-onset** (lchedy, lkaiin, lkeedy — l-prefix on standard B-onset stems; lkaiin=81% stars-concentrated = the most section-specific token in the manuscript); (2) **k-onset** (kaiin, keedy, keey — k-initial B-paradigm words; 47-55% stars-concentrated). Stars line-start "other" = y-/p-/t-prefixed B-content words (formula openers for catalog entries); stars line-end "other" = am-suffix particles (am=16 at final positions). The standalone particles (aiin/ar/al/or/am) account for 33% of "other" in stars — these are discourse-level free morphemes appearing within B-dialect catalog entries. **New hypotheses generated**: H247 (l-onset prefix class characterization), H248 (k-onset characterization).
