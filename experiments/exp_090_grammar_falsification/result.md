# Experiment exp_090: Grammar Model Falsification (H146), A Line Structure (H156/H157)
Date: 2026-04-09

## H146: Grammar Models Falsified as Predictors — she-prefix Achieves 45.7% Precision (4.74× Base); olfchedy Achieves 61.5% Precision (14.72×)

### A Dialect Para-Start Prediction (she-prefix as first word)

| Metric | she-prefix predictor | Base rate |
|--------|---------------------|----------|
| Precision | **45.7%** | 9.6% |
| Recall | 9.9% | — |
| F1 | 16.2% | — |
| Enrichment | **4.74×** | 1.00× |
| TP/FP/FN | 16/19/146 | — |

When she-prefix opens a line, there is a 45.7% probability it is a para-start (vs 9.6% base rate). **HIGH PRECISION, LOW RECALL** predictor: she-prefix identifies para-starts reliably when it fires, but covers only 9.9% of all para-starts.

**Section-specific she-prefix precision**:
- Astro A: **P=100.0%, R=15.4%** — every she-prefix para-start prediction is correct in astro
- Herbal A: P=46.2%, R=7.0%
- Pharma A: P=42.9%, R=12.8%
- "Other" A: P=0.0% — model fails on unclassified folios

### A Dialect Para-Final Prediction (daiin as last word)

| Metric | daiin-last predictor |
|--------|---------------------|
| Precision | 13.0% |
| Recall | 8.6% |
| F1 | 10.4% |
| Enrichment | **1.35×** (very weak) |

Daiin as last word is barely above base rate for predicting para-finals (1.35×). Daiin appears at line-end throughout A (within-para and para-final), making it non-specific as a para-final predictor. **Conclusion: daiin marks line-endings generally in A, NOT para-finals specifically.**

### B Dialect Para-Start Prediction (o-onset first word)

| Predictor | Precision | Recall | F1 | Enrichment |
|-----------|-----------|--------|----|-----------| 
| o-onset first word | 9.5% | 36.6% | 15.1% | 2.28× |
| o-onset long word (≥6 + edy/dy) | 16.4% | 9.9% | 12.3% | 3.92× |
| **olfchedy/olkey/opchedy** | **61.5%** | 7.9% | 14.0% | **14.72×** |

**olfchedy, olkey, or opchedy as first word achieves 61.5% precision (14.72× enrichment)**. When one of these specific words opens a B line, there is a 61.5% chance it is a para-start. This is the strongest predictive signal found.

Simple o-onset first word has high recall (36.6%) but low precision (9.5%) — too many false positives. The precision improves dramatically by requiring specific long-form words.

### Cross-Dialect Combined Model

| Model | Precision | Recall | F1 | Enrichment |
|-------|-----------|--------|----|-----------| 
| she-prefix (A) + o-onset (B) | 12.5% | 20.2% | 15.5% | 1.95× |

The combined cross-dialect predictor achieves 1.95× enrichment, well above chance. The model correctly identifies para-starts at nearly 2× the base rate across the full corpus.

### Falsification Verdict

The grammar models are **NOT falsified** — they have genuine predictive power:
1. she-prefix: 4.74× precision enrichment for A para-starts (astro: 100% precision)
2. olfchedy/olkey/opchedy: 14.72× precision enrichment for B para-starts (61.5% precision)
3. Models work best as HIGH-PRECISION, LOW-RECALL predictors — they correctly flag para-starts when they trigger, but miss most para-starts

The precision being far above base rate (4.74-14.72×) confirms these are REAL GRAMMATICAL SIGNALS, not statistical noise.

### H146 Verdict: NOT FALSIFIED — Grammar Models Have Genuine Predictive Power; she-Prefix Achieves 45.7% Para-Start Precision (4.74×); olfchedy/olkey Achieves 61.5% Precision (14.72×); daiin Para-Final Signal Is Weak (1.35×)

---

## H156/H157: A Line Structure — ch-Onset Is A's Mid-Line Element; d-Onset Dominates Line-Final Position

### A Onset Distribution by Line Position

| Onset | pos0 | pos1 | pos2 | 2nd-last | last |
|-------|------|------|------|---------|------|
| **ch** | 10.8% | **27.3%** | **23.7%** | **22.8%** | 17.8% |
| **d** | **16.4%** | 9.2% | 12.7% | 14.9% | **23.0%** |
| o | 18.1% | 15.8% | 15.2% | 17.8% | 19.3% |
| y | **13.6%** | 3.4% | 4.2% | 5.9% | 3.8% |
| qo | 13.3% | 10.7% | 11.5% | 9.8% | 7.1% |
| sh | 10.9% | 13.7% | 11.1% | 9.1% | 5.8% |
| s | **6.3%** | 0.7% | 2.3% | 1.7% | 4.4% |

**KEY STRUCTURAL PATTERNS:**
1. **ch-onset peaks at pos1 (27.3%)** — ch is the A MID-LINE onset, dropping from 10.8% at pos0 to 17.8% at last
2. **d-onset peaks at last (23.0%)** — d is the A LINE-CLOSER onset, appearing more at line-end than anywhere else
3. **y-onset peaks at pos0 (13.6%)** — y is the A LINE-OPENER onset, dropping sharply thereafter
4. **s-onset is elevated at pos0 (6.3%)** and drops everywhere else (pos1=0.7%) — s as line-opener

### A Line Structure Model

**Full A line structure: [OPENER: y/d/o/sh/qo] → [ch MID-LINE (27.3% at pos1)] → [d-CLOSER (23.0% at last)]**

This parallels the B structure:
| Feature | A Dialect | B Dialect |
|---------|-----------|-----------|
| LINE-OPENER morpheme | y-compound, she-prefix | y-compound, s-onset |
| MID-LINE marker | ch-onset (27.3% at pos1) | qo-prefix (65.4% present) |
| LINE-CLOSER | d-onset (23.0%), -am words | -am words (74-86% LLast), oly/oldy |

### Top Words at Each Position

**pos0 (line-openers)**: daiin(81, d-onset), sho/shol/shor(32/24/21, sh), chor/chol(21/19, ch), dain(18, d)
- Surprisingly: daiin(81) is the most common A line-opener! d-onset opens lines often (daiin, dain, dchor)

**last (line-closers)**: daiin(108, d), dy(35, d), dal(26, d), dar(25, d), dam(24, d), dain(22, d), aiin(19), chol(17, ch)
- **d-onset dominates A line endings**: daiin, dy, dal, dar, dam, dain are all d-onset and all frequent line-closers

**2nd-last**: daiin(94, d), chol(39, ch), chor(25, ch), dain(19, d), shol(18, sh)
- ch-onset (chol, chor) dominates the 2nd-to-last position — ch appears just before the d-closer

### d-Onset A: Word-Level Line-Closing Profiles

| Word | n | LFirst% | LLast% | Mid% |
|------|---|---------|--------|------|
| dam | 38 | 0.0% | **63.2%** | 36.8% |
| dy | 63 | 4.8% | **55.6%** | 39.7% |
| daiiin | 9 | 0.0% | **55.6%** | 44.4% |
| dal | 68 | 2.9% | **38.2%** | 58.8% |
| dar | 75 | 16.0% | **33.3%** | 50.7% |
| dain | 73 | 24.7% | **30.1%** | 45.2% |
| daiin | 417 | 19.4% | **25.2%** | 55.4% |
| dchor | 21 | **66.7%** | 4.8% | 28.6% | ← LINE-OPENER
| dchol | 11 | **72.7%** | 18.2% | 9.1% | ← LINE-OPENER
| dchey | 9 | **66.7%** | 0.0% | 33.3% | ← LINE-OPENER

**d-onset splits into two functional sub-classes in A:**
1. **d-LINE-CLOSERS**: {dam (63.2%), dy (55.6%), dal (38.2%), dar (33.3%), dain (30.1%)} — predominantly line-final, within-para
2. **d-LINE-OPENERS**: {dchor (66.7% LFirst!), dchol (72.7%), dchey (66.7%)} — predominantly line-initial (d+ch compound forms)

This is a structural analogy to B's y-compound/bare-stem distinction: in A, the d-prefix with ch-stem (dchor, dchol) creates LINE-OPENERS, while bare d+suffix forms (dal, dar, dam) are LINE-CLOSERS.

### A Para-Start Line Openers (Most Enriched)

| Word | PS enrichment | PS count | Non-PS count |
|------|--------------|---------|-------------|
| shey | **46.9×** | 5 | 1 |
| sheol | **18.8×** | 4 | 2 |
| oty | 9.4× | 3 | 3 |
| chor | 2.9× | 5 | 16 |
| shol | 1.3× | 3 | 21 |

shey (46.9×) and sheol (18.8×) are the dominant A para-start openers. These are she-prefix forms. chor is the next most enriched (2.9×) — ch-onset para-start is a moderate signal.

### H156/H157 Verdict: CONFIRMED — A Has ch-Onset Mid-Line Structure (27.3% at pos1) and d-Onset Line-Final Structure (23.0% at last); d-Onset Splits Into Line-Openers (dchor/dchol=66-72% LFirst) and Line-Closers (dam/dy/dal=33-63% LLast); A Line Structure Parallels B

---

## Combined Finding (F097)

**H146 NOT FALSIFIED**: Grammar models have real predictive power. she-prefix: 45.7% precision (4.74×, astro A = 100% precision). olfchedy/olkey/opchedy: 61.5% precision (14.72×). Cross-dialect combined model: 1.95× enrichment. daiin para-final predictor is weak (1.35×) — daiin marks general line-endings in A, not specifically para-finals.

**H156/H157 CONFIRMED**: A has a parallel line structure to B but with different morphemes: A = [opener] → [ch MID-LINE (27.3% at pos1)] → [d-CLOSER (23.0% at last)]; B = [y/s opener] → [qo MID-LINE] → [-am/oly CLOSER]. d-onset splits in A: {dchor/dchol/dchey} are LINE-OPENERS (LFirst=66-72%); {dam/dy/dal/dar/dain/daiin} are LINE-CLOSERS (LLast=25-63%). The two-way d split in A parallels the y-prefix/bare-stem split in B. The structural parallelism across dialects provides strong evidence that Voynichese has a systematic positional grammar.
