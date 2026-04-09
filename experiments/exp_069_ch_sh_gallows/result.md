# Experiment exp_069: ch vs sh Discrimination (H085) + Gallows Positional Grammar (H086)
Date: 2026-04-09

## H085: ch vs sh Discrimination

### Currier A

ch: 1945 (68.4%), sh: 898 (31.6%)

**Positional difference:**
| Position | ch% | sh% |
|----------|-----|-----|
| first | 3.9% | **11.2%** |
| medial | 82.4% | 80.0% |
| last | **13.7%** | 8.8% |

sh is ~3× more line-initial than ch in A. ch is ~1.6× more line-final.

**Suffix differences (A):** ch prefers -ar (1.63×), -y (1.23×); sh prefers -(none) bare forms (21.7% vs 15.3%).

**Left-context:** ch follows ch (1.52×) and qo (1.39×). sh follows sh (2×) and follows p (2.27×). Both show **self-following**: ch is more likely to follow another ch word; sh more likely to follow sh.

**Section:** A Text section: sh=55.2% of ch+sh (reverses the usual ch majority). A Herbal: sh=31.3%.

### Currier B

ch: 3247 (63.2%), sh: 1891 (36.8%)

**Positional difference:**
| Position | ch% | sh% |
|----------|-----|-----|
| first | 2.1% | **5.0%** |
| medial | 87.3% | 90.0% |
| last | **10.6%** | 5.0% |

sh again more line-initial (5.0% vs 2.1%); ch more line-final (10.6% vs 5.0%).

**Suffix differences (B):**
| Suffix | ch% | sh% | sh/ch |
|--------|-----|-----|-------|
| -eedy | 2.3% | 4.4% | **1.93×** for sh |
| -edy | 16.0% | 21.0% | **1.31×** for sh |
| -aiin | 5.7% | 3.1% | **1.87×** for ch |
| -ain | 3.6% | 2.1% | **1.69×** for ch |
| -al | 4.9% | 3.0% | **1.66×** for ch |
| -ar | 5.8% | 3.7% | **1.56×** for ch |

ch+short suffix (aiin/ain/al/ar); sh+extended suffix (edy/eedy). This is a real morphological discriminant.

**Left-context in B:** sh is 4.1× more likely than ch to appear after p-onset words (sh after p: 4.1%, ch after p: 1.0%). Since p-onset marks para-starts, sh preferentially appears as the SECOND word in a p-onset paragraph opener. ch follows ch (1.63×) and qo (1.09×); sh follows d (10.1% vs ch 7.3% = 1.38×) and s (5.1% vs 2.9%).

**Section (B):** Bio section: sh=48%; Special=30.7%; Herbal B=31.3%; Text B=45.3%. Bio and Text sections have elevated sh proportion.

**Mean word length:** ch=5.88, sh=5.53 (ch slightly longer).

### H085 Verdict: SUPPORTED — ch and sh have distinct positional and morphological niches

ch and sh are NOT interchangeable free variants. They differ consistently:
1. **sh is more line-initial** (A: 11.2% vs 3.9%; B: 5.0% vs 2.1%)
2. **ch is more line-final** (A: 13.7% vs 8.8%; B: 10.6% vs 5.0%)
3. **sh prefers extended suffixes** (-edy, -eedy in B); **ch prefers short suffixes** (-aiin, -ain, -al, -ar in B)
4. **Self-following tendency**: both show same-onset repetition (ch→ch, sh→sh)
5. **sh follows p-onset** more than ch (4.1× in B) — sh is the secondary line-opener after the p-onset para-start word
6. **Section sensitivity**: Bio (B) and Text sections show elevated sh proportion

Despite KL divergence of only 0.062 bits in the suffix profiles (F068), ch and sh have systematically different distributional signatures. They may encode a morphophonological distinction (voiced vs voiceless? determinate vs indeterminate?) that operates in a positional and contextual frame.

---

## H086: Gallows Letters Individual Positional Grammar

Currier B baseline: first=11.9%, medial=76.3%, last=11.8%, para_first=0.60%

| Gallows | Count | %all | first% | enr_first | para_first% | enr_para |
|---------|-------|------|--------|-----------|-------------|----------|
| k | 511 | 2.4% | 7.8% | **0.66×** | 2.94% | **4.88×** |
| t | 544 | 2.5% | 45.4% | **3.82×** | 4.60% | **7.64×** |
| f | 62 | 0.3% | 22.6% | **1.90×** | 4.84% | **8.04×** |
| p | 393 | 1.8% | 75.3% | **6.34×** | 10.69% | **17.76×** |

### Four Distinct Positional Niches

**p (17.76× para-start)**: Almost exclusively line-first (75.3%!), strongly para-start enriched. Near-never medial (22.6%), near-never last (2.0%). The para-start marker. Top words: pchedy(29), pol(13), pchedar(10), polchedy(7).

**t (7.64× para-start, 3.82× line-first)**: Line-first biased (45.4%), also para-start enriched. Medial=48.3% (below baseline 76.3%). t is a secondary para-start marker — it frequently opens lines and disproportionately opens paragraphs. Top words: tedy(33), tchedy(28), tar(26), taiin(22).

**f (8.04× para-start, 1.90× line-first)**: Rare (only 62 tokens, 0.3% of B). Para-first enrichment as strong as t (8.04×), moderate line-first bias (1.90×). Top words: fchedy(10), fcheey(4), fchdy(3). f may be a marked/emphatic variant of t in the para-start function.

**k (4.88× para-start, 0.66× line-first)**: Predominantly medial (80.2%). k AVOIDS line-starts in general (0.66×) but when it does appear at a line-start, it's disproportionately at paragraph openings (para_first 4.88×). This creates an unusual pattern: k is the "medial gallows" that occasionally marks special paragraph-initial positions with a very different word form. Top words: keedy(34), kar(34), kaiin(32), kedy(30).

### Suffix Distributions by Gallows

| Suffix | k% | t% | f% | p% | all B% |
|--------|----|----|----|----|--------|
| -dy | **13.9%** | 8.5% | 14.5% | 10.9% | 6.5% |
| -ar | **11.0%** | **11.0%** | 6.5% | **14.5%** | 6.9% |
| -edy | 11.0% | **14.7%** | **19.4%** | 12.2% | 12.8% |
| -aiin | 8.0% | 9.9% | 6.5% | 9.4% | 9.6% |

**k** is distinguished by -dy preference (13.9% = 2.14× baseline). **p** is distinguished by -ar (14.5% = 2.10× baseline) and p-compound words like pchedar. **f** and **t** both prefer -edy.

### Section Distribution (Currier B)

| Section | k% | t% | f% | p% |
|---------|----|----|----|----|
| Herbal | 4.3% | 4.1% | 0.5% | 1.7% |
| Bio | 1.3% | 2.1% | 0.1% | 1.4% |
| Special | 2.5% | 2.3% | 0.4% | 2.2% |
| Text | 2.0% | 2.1% | 0.2% | 1.8% |

Herbal B has elevated k (4.3%) and t (4.1%) rates vs other sections. p is relatively consistent across sections (1.4–2.2%).

### H086 Verdict: STRONGLY SUPPORTED — Four gallows have distinct positional niches

The 4-class {k/t/p} onset taxonomy from F068 (based on suffix profiles) is **WRONG for positional grammar**. The four gallows have dramatically different positional roles:
- **p**: primary para-start marker (17.76×), avoids medial
- **t**: secondary para-start / line-opener (7.64× para-start, 3.82× line-first)
- **f**: tertiary/marked para-start (8.04× para-start), rare
- **k**: medial gallows (1.05× medial), but occasionally marks special para-starts (4.88×); marked by -dy suffix preference

The {k/t/p} suffix class grouping reflects MORPHOLOGICAL similarity but hides POSITIONAL specialization. This is consistent with the hypothesis that Voynichese has a grammatical category "gallows" that takes a shared suffix system but is split into positional sub-classes by initial consonant identity.

---

## Combined Finding (F076)

**H085 SUPPORTED**: ch and sh are morphologically distinct in Voynichese — NOT free variants. sh is more line-initial (A: 11.2% vs 3.9%; B: 5.0% vs 2.1%), ch is more line-final (A: 13.7% vs 8.8%; B: 10.6% vs 5.0%). In B, ch takes short suffixes (-aiin, -ain, -al, -ar: all ~1.6-1.9×) while sh takes extended suffixes (-edy, -eedy: ~1.3-1.9×). sh follows p-onset words at 4.1× the rate of ch — sh is the secondary opener after the p-onset para-start. Both show self-following repetition (ch→ch, sh→sh). **H086 STRONGLY SUPPORTED**: The 4 Currier B gallows letters have distinct positional niches despite sharing the same suffix class: p is the primary para-start marker (17.76×); t is the secondary line-opener (7.64×); f is a rare tertiary marker (8.04×); k is the medial gallows (1.05× medial, 0.66× line-first) with a -dy suffix preference (2.14×). The {k/t/p} suffix class from F068 correctly groups morphological similarity but incorrectly implies positional equivalence.
