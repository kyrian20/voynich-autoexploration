# Experiment exp_132: B-Herbal Onset Profile Diagnostic (H258) + s-Onset Characterization (H259)
Date: 2026-04-09

## H258: CONFIRMED — B-Herbal Folios Are Depleted in cth (A-Nominal) and d (A-Function Words) ACROSS ALL 12 B-Herbal Folios; Elevated in ok/qok/other (B-Content Classes); f40→stars Because ok=16.1% (vs A-herbal=4.3%); f26/f31/f50→pharma Because ok+qok Elevated and d/cth Depleted; Two UNIVERSAL Deviations from A-Herbal Centroid Confirm B-Herbal Is Genuinely Different Register

### Per-Folio Cosine Similarity (Onset-Class Profile Vectors)

| Folio | Tokens | Herbal | Pharma | Stars | Cosmo | Astro | Best |
|-------|--------|--------|--------|-------|-------|-------|------|
| **f26** | 152 | 0.922 | **0.961** | 0.907 | 0.804 | 0.950 | pharma |
| **f31** | 202 | 0.933 | **0.965** | 0.921 | 0.783 | 0.912 | pharma |
| f33 | 163 | 0.929 | 0.939 | 0.864 | 0.729 | **0.945** | astro |
| f34 | 233 | 0.924 | **0.944** | 0.919 | 0.809 | 0.845 | pharma |
| f39 | 285 | 0.929 | 0.956 | 0.891 | 0.768 | **0.975** | astro |
| **f40** | 186 | 0.779 | 0.867 | **0.870** | 0.743 | 0.833 | stars |
| f41 | 145 | 0.904 | **0.929** | 0.888 | 0.885 | 0.828 | pharma |
| f43 | 301 | **0.964** | 0.945 | 0.889 | 0.758 | 0.938 | herbal |
| f46 | 262 | **0.953** | 0.938 | 0.861 | 0.821 | 0.888 | herbal |
| **f48** | 194 | 0.848 | 0.849 | 0.868 | 0.681 | **0.870** | astro |
| **f50** | 185 | 0.849 | **0.902** | 0.885 | 0.797 | 0.856 | pharma |
| f57 | 83 | 0.951 | **0.956** | 0.867 | 0.766 | 0.936 | pharma |

**Key**: Bolded rows are B-herbal folios identified in F123 as bifolio insertions. Note: exp_131 identified 5 mismatching B-herbal folios; this experiment with full B-dialect identification identifies 12 B-herbal folios total, 10 of which mismatch. f43 and f46 are B-dialect (edy/eedy ≥5%) but best-match herbal — they are less extreme B-herbal folios.

### Universal Deviations: cth↓ and d↓ Across ALL B-Herbal Folios

Two onset classes are CONSISTENTLY depleted across ALL 12 B-herbal folios vs A-herbal centroid:
- **cth: mean_dev = -0.0366** (A-herbal=0.0447; B-herbal mean≈0.008) — B-herbal is nearly CTHLESS. cth-onset words (A-dialect plant-name nominals) are systematically absent from B-herbal text.
- **d: mean_dev = -0.0617** (A-herbal=0.1677; B-herbal mean≈0.106) — B-herbal has 37% fewer d-onset words (A-function words: daiin, dy, dam, dshedy). The A-dialect function word class is underrepresented in B-herbal.

### Folio-Specific Deviations Explain Best-Match Section

**f40 → STARS** (self=0.779, stars=0.870): Most extreme mismatch
- ok↑+0.119 (folio=0.161, A-herbal=0.043, stars=0.070)
- qok↑+0.062 (folio=0.097, A-herbal=0.035, stars=0.104)
- other↑+0.105, d↓-0.103, ch↓-0.086
- **MECHANISM**: f40 has extreme ok-onset inflation (16.1% of words vs A-herbal 4.3%). ok is a B-content class concentrated in stars. Combined with d/ch depletion, this makes f40 look more like stars than any other section.

**f26 → pharma** (pharma=0.961): 
- other↑+0.078, d↓-0.076, qok↑+0.051, s↑+0.044
- cth↓ (folio=0.020 vs A-herbal=0.045)

**f31 → pharma** (pharma=0.965):
- ok↑+0.096, d↓-0.069, other↑+0.054, cth↓-0.035

**f48 → astro** (astro=0.870):
- d↓-0.106, ot↑+0.082, ch↓-0.071, t↑+0.058, y↑+0.054
- f48 has high ot (0.124) and t (0.093) — unusual for herbal; matches astro better than pharma

**f50 → pharma** (pharma=0.902):
- ch↓-0.102, ok↑+0.093, d↓-0.081, qok↑+0.051

**f33, f39 → astro**: elevated "other" (0.196, 0.221 vs A-herbal=0.100); depleted ch and cth

### MECHANISM Summary

B-herbal folios cluster with pharma/stars/astro because:
1. **cth depletion** (universal): No A-dialect plant-name nominals → no herbal-type vocabulary
2. **d depletion** (universal): Reduced A-function word class → different functional grammar
3. **ok/qok elevation** (most folios): B-content nouns dominate → similar to B-dialect sections (pharma-B has elevated qok too)
4. **other elevation** (most folios): B-words not in the 18-class taxonomy inflate the "other" category
5. **ch depletion** (some folios): Less A-paradigm content → lower similarity to A-herbal centroid

Pharma is the most common best-match because pharma ALSO has elevated qok (0.075) and reduced cth (0.025) vs A-herbal — pharma is the nearest A-section with partial B-vocabulary mixing. Stars is f40's match because stars has the highest ok+qok in the manuscript.

### H258 Verdict: CONFIRMED — ALL B-herbal folios are universally depleted in cth (A-nominals, mean_dev=-0.037) and d (A-function words, mean_dev=-0.062). Most B-herbal folios are elevated in ok/qok/other (B-content classes). f40 (ok=16.1% vs A-herbal=4.3%) best-matches stars because stars has the highest ok+qok concentration. f26/f31/f50 best-match pharma because pharma also has elevated qok and reduced A-paradigm vocabulary. The mechanism is dialect-level onset class composition: B-herbal has B-dialect content vocabulary (ok/qok) and lacks A-dialect grammar words (cth, d), making it structurally more similar to B-dialect sections (pharma, stars, astro) than to A-dialect herbal.

---

## H259: CONFIRMED — s-Onset Is a LINE-OPENING Grammatical Class (LF=48.9%); Two Sub-Classes: s-OPENERS (LF=50-100%; saiin/sain/sar/sol/sor) and s-CLOSERS (LL=28-89%; sy/sam/sal); Post-s sh=1.92× (s-Openers Followed by sh-Content); s Is COSMO/ASTRO-Concentrated (1.52×/2.15×), NOT Stars; Parallel to d-Onset But Purer Positional Specialization

### Global s-Onset Statistics

- Total tokens: 791, types: 262, hapax: 201 (76.7%)
- **Line-first (LF): 387/791 = 48.9%** — s is predominantly a LINE-OPENING onset class
- Mid-line (MID): 286/791 = 36.2%
- Line-last (LL): 123/791 = 15.5%

Comparison to d-onset (3-sub-class system from F137):
- d-onset: LF=20.5%, MID=56.5%, LL=23.2% — primarily MEDIAL function word
- s-onset: LF=48.9%, MID=36.2%, LL=15.5% — primarily LINE-OPENER

**s-onset is structurally different from d-onset**: s is a line-OPENING class (48.9% LF vs d=20.5% LF), while d is a balanced function/medial class with higher line-last rate.

### Section and Dialect Distribution

| Section | n | s% | corpus% | enrichment |
|---------|---|----|---------:|----------:|
| **astro** | 27 | 3.4% | 1.6% | **2.15×** |
| **cosmo** | 262 | 33.1% | 21.7% | **1.52×** |
| **pharma** | 128 | 16.2% | 11.4% | **1.42×** |
| herbal | 188 | 23.8% | 30.4% | 0.78× |
| stars | 186 | 23.5% | 34.9% | **0.67×** |

**CRITICAL**: s-onset is DEPLETED in stars (0.67×) and herbal (0.78×), and ELEVATED in cosmo (1.52×), pharma (1.42×), and astro (2.15×). This is OPPOSITE to what was expected from F138 (where s=6.56× at stars line-start). The resolution: s-words are RARE in stars (0.67× overall) but those that do appear in stars are overwhelmingly LINE-OPENERS (67.2% LF in stars-s subset). Stars s-words are concentrated at line-start; cosmo has more s-words overall.

Dialect: A=37.8%, B=62.2% (slightly B-dominant, matching corpus baseline of 34/66%).

### Top s-Onset Words

| Word | n | LF% | MID% | LL% | Stars% | B% |
|------|---|-----|------|-----|--------|-----|
| saiin | 106 | 50.0% | 40.6% | 9.4% | 32.1% | 71.7% |
| sar | 59 | 49.2% | 33.9% | 16.9% | 35.6% | 78.0% |
| sain | 59 | 57.6% | 30.5% | 11.9% | 40.7% | 89.8% |
| sol | 55 | 63.6% | 32.7% | 3.6% | 10.9% | 76.4% |
| sor | 44 | 65.9% | 29.5% | 4.5% | 15.9% | 56.8% |
| sal | 40 | 30.0% | 42.5% | 27.5% | 17.5% | 65.0% |
| **sy** | 20 | 5.0% | 10.0% | **85.0%** | 10.0% | 35.0% |
| sair | 20 | 45.0% | 50.0% | 5.0% | 45.0% | 75.0% |
| soiin | 18 | 72.2% | 27.8% | 0.0% | 22.2% | 44.4% |
| **sam** | 9 | 11.1% | 0.0% | **88.9%** | 22.2% | 33.3% |

Top s-words are dominated by two groups:
1. **s-openers**: saiin, sain, sar, sol, sor, soiin (50-72% LF) — open lines
2. **s-closers**: sy (85%LL), sam (89%LL) — close lines (parallel to d-closers dy/dam)

### s-Onset Sub-Classes

**s-OPENERS (LF≥40%, n≥3): 26 types**
- schedy(86%LF, 100%B), sshedy(100%LF, 100%B), sshey(100%LF) — s+ch/sh compounds parallel to d+ch/sh openers
- solchedy(83%LF, 100%B), solkeey(100%LF), solkeedy(100%LF) — s+ol+ch compound openers
- soiin(72%LF, 44%A), sodaiin(75%LF, 25%A) — s+A-paradigm openers
- sol(64%LF), sor(66%LF) — frequent line-opening particles

**s-CLOSERS (LL≥25%, LF<40%, n≥3): 7 types**
- sam(89%LL, 33%B) — s+am closer (parallel to dam=67.9%LL)
- sy(85%LL, 35%B) — s+y closer (parallel to dy=40.3%LL)
- sos(67%LL), saldy(67%LL), sairy(67%LL) — longer s-closers

**s-MEDIALS (MID≥60%, n≥3): only 4 types** (sol, sols, sody, san) — s is NOT a medial class

### Bigram Context: Post-s = sh (1.92×) Strongest

**What follows s-onset words:**
- sh: **1.92×** (strongest enrichment — s-words precede sh-content)
- ol: 1.60×
- other: 1.53×
- d: 0.63× (s-words do NOT precede d-words)
- qok: 0.56× (s-words do NOT precede qok — unusual for B-paradigm)

**What precedes s-onset words:**
- No strong enrichment (k=1.40×, qo=1.37×, ch=1.31×) — s-words can follow almost anything

The post-s sh=1.92× enrichment directly parallels the stars line-template from F138: [s-opener][sh-content 2nd word]. In cosmo also, s-words precede sh-onset content. This is a **s→sh opener-to-content rule** parallel to the d+ch/sh compound opener class (where d-words that start with d+ch are openers — d connects directly to ch).

### Stars-Specific s-Onset

Stars has 186 s-onset tokens (23.5% of all s-words) at LF=**67.2%** — far higher than global 48.9%. Stars s-words are almost exclusively LINE-OPENERS in stars context. Top stars s-words: saiin(34), sain(24), sar(21). These are the same words that are general openers, but in stars they are even more constrained to line-start.

### Para-Start s Enrichment (Unreliable)
Para-start detection identified only 46 paragraph-start loci (known to be incomplete). With that caveat: s appears at para-start first-word at rate 6.5% vs all-line first-word 10.2% = **0.64×**. This tentatively suggests s is NOT specifically a paragraph-opener; it's a line-opener (consistent with 48.9% LF across all lines). Prior finding in F126 that "s=48.5% para-start" may have been measurement error.

### H259 Verdict: CONFIRMED — s-onset has TWO main sub-classes: (1) s-OPENERS (LF=50-100%; saiin=50%, sain=58%, sol=64%, soiin=72%, sshedy/sshey=100%); (2) s-CLOSERS (sy=85%LL, sam=89%LL — parallel to d-closers dy/dam). s-onset is primarily a LINE-OPENER class (48.9% LF vs d=20.5% LF). s-words are COSMO/ASTRO/PHARMA-concentrated (1.52×/2.15×/1.42×) and DEPLETED in stars (0.67×) and herbal (0.78×) — s is NOT a stars-specific class despite appearing as a strong line-opener in stars. The resolution: in stars, s-words are RARE but heavily concentrated at line-start (67.2%LF); in cosmo, s-words are more numerous overall. Post-s sh=1.92× confirms s-opener→sh-content sequential rule (parallel to stars line template [opener][sh-2nd]). s-onset compounds (schedy, sshedy, solchedy = 100%B, 100%LF) parallel d+ch/sh compound openers from F137. s is the SECOND LINE-OPENER CLASS after y/p (from F135) — completing the picture of multiple opener classes: y-openers (k/t stems), p-openers (B+ch/sh), s-openers (various stems, cosmo/pharma concentrated).

---

## Combined Finding (F139)

**H258 CONFIRMED (F139)**: B-herbal folios (12 total identified by dialect) are universally depleted in cth (A-nominal class, mean_dev=-0.037) and d (A-function words, mean_dev=-0.062). Most B-herbal folios are elevated in ok/qok/other (B-content onset classes). The dialect-level mismatch operates through onset class composition: B-herbal lacks A-dialect grammar words and has B-dialect content vocabulary, making it cluster with B-dialect sections (pharma, stars, astro) rather than A-dialect herbal. f40's ok=16.1% (3.8× A-herbal rate, near stars-level) is the single most extreme diagnostic: B-herbal content vocabulary can reach stars-class concentrations of B-paradigm nouns. f43 and f46 are B-dialect (edy≥5%) but remain herbal-best-match — they have less extreme B-vocabulary and retain some herbal-like onset profiles.

**H259 CONFIRMED (F139)**: s-onset is a LINE-OPENING grammatical class (LF=48.9%) with two sub-classes: s-OPENERS (saiin/sain/sar/sol/sor, LF=50-100%) and s-CLOSERS (sy=85%LL, sam=89%LL). Post-s sh=1.92× confirms s→sh sequential rule (same as stars line template's [opener][sh-2nd-position]). s is COSMO/ASTRO-concentrated (1.52×/2.15×) and depleted in stars (0.67×) and herbal — s is NOT a stars-specific opener but a general multi-section opener. Stars s-words (67.2%LF in stars context) are maximally line-concentrated even though s is overall rare in stars. The s-onset OPENER sub-class (schedy/sshedy/solchedy = 100%B, 100%LF) is the B-dialect parallel to d+ch/sh compound openers (A-dialect: dchor/dchol; B-dialect: dshedy/dchedy from F137). Combined with p-openers (F135), y-openers (F134), d-openers (F137): the manuscript has AT LEAST FOUR DISTINCT LINE-OPENER ONSET CLASSES: y (k/t stems, both dialects), p (B+ch/sh), d+ch/sh compounds (A+B, section-split), s (various stems, cosmo/pharma).
