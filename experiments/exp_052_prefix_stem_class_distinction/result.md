# Experiment exp_052: Three-Prefix System Stem-Class Distinction
Date: 2026-04-09

## Question (H058)
Do the k/t-initial stems (selected by qo- and o-) have different suffix distributions from the o/y/e-initial stems (selected by cth-), within their respective dialects? If so, these stem classes encode different grammatical categories.

## Results

### Suffix Distributions by Stem Class

**Currier B classes:**

| Suffix | qo-words(B) | kt-bare(B) | other(B) | all-B |
|--------|-------------|-----------|---------|-------|
| -edy | 14.6% | 14.8% | 15.3% | 15.1% |
| -eedy | **11.8%** | 6.5% | 4.8% | 6.3% |
| -aiin | 11.0% | 10.3% | 11.5% | 11.3% |
| -ain | **10.4%** | 6.1% | 6.2% | 7.0% |
| -eey | **9.8%** | 5.3% | 6.5% | 7.1% |
| -dy | 6.0% | **12.7%** | 7.8% | 7.6% |
| -ar | 6.9% | **12.6%** | 8.1% | 8.1% |
| -y | 6.5% | 6.6% | **11.8%** | 10.5% |

**Currier A classes:**

| Suffix | cth-words(A) | oye-bare(A) | other(A) | all-A |
|--------|-------------|-----------|---------|-------|
| -y | **29.8%** | 14.9% | 15.8% | 16.1% |
| -ol | **20.0%** | 16.1% | 17.2% | 17.1% |
| -or | **13.8%** | 11.8% | 12.2% | 12.2% |
| -aiin | 5.5% | **13.6%** | **15.6%** | 14.7% |
| -edy | 0.3% | 0.1% | 0.2% | 0.2% |
| -chy | 0.9% | **5.9%** | 5.1% | 5.1% |

### KL Divergences

| Comparison | KL (bits) | Interpretation |
|-----------|-----------|----------------|
| KL(qo-words \|\| cth-words) | **4.726** | Enormous — stem classes differ by 4.7 bits |
| KL(all-A \|\| all-B) | 0.586 | Overall A/B dialect divergence |
| KL(qo-words \|\| kt-bare) | 0.154 | Small — qo- vs bare k/t in same dialect |
| KL(cth-words \|\| oye-bare) | 0.241 | Moderate — cth- differs from bare o/y/e in A |
| KL(qo-words \|\| all-B) | 0.089 | qo- is very typical of B |
| KL(cth-words \|\| all-A) | 0.202 | cth- differs somewhat from A average |

### Key Finding: Stem-Class Distinction Is Between-Dialect, Not Within-Dialect

The massive KL(qo||cth) = 4.726 bits occurs because:
- qo-words are in Currier B → use B-type suffixes (-edy, -eedy, -ain)
- cth-words are in Currier A → use A-type suffixes (-y, -ol, -or)

**Within Currier B**: qo-stems, bare k/t-initial words, and all other B-words have similar suffix distributions (KL ≈ 0.15 bits). All three use B-type suffixes at similar rates. qo-stems ARE somewhat different — more -eedy, -ain, -eey and less -dy, -ar than bare k/t words — suggesting qo- selects a specific subset within the k/t stem class, but this is modest.

**Within Currier A**: cth-words differ more substantially from bare o/y/e-words (KL = 0.241) and from other A-words. The cth-stem dramatically favors -y (29.8% vs 14.9% for bare o/y/e) and -ol (20.0%) while suppressing -aiin (5.5% vs 13.6%) and -chy (0.9% vs 5.9%).

### The cth- "Stem" Takes Suffixes Directly

The cth- words structure:
- cthy (84, 22%): cth + y
- cthol (49, 13%): cth + ol
- cthor (35, 9%): cth + or
- cthey (29, 8%): cth + ey
- cthody (13): cth + o + dy
- ctheey (11): cth + e + ey

**cth- IS the stem** — it takes suffixes directly (sometimes with a one-character connector). This means 'cth' is a single morphological root that takes the full A-type suffix paradigm. It is NOT a prefix on another stem; it's the root itself.

### Most Distinctive Suffixes: qo-class vs cth-class

| Suffix | qo-words(B) | cth-words(A) | Diff |
|--------|-------------|-------------|------|
| -y | 6.5% | **29.8%** | -23.3% |
| -edy | **14.6%** | 0.3% | +14.3% |
| -ol | 6.2% | **20.0%** | -13.8% |
| -or | 1.9% | **13.8%** | -12.0% |
| -eedy | **11.8%** | 0.0% | +11.8% |
| -ain | **10.4%** | 1.8% | +8.6% |

The suffix split between the two stem classes is IDENTICAL to the A/B dialect split. This is because:
1. The k/t-initial stems (qo-class) are essentially all in Currier B
2. The o/y/e-initial stems (cth-class) are essentially all in Currier A

## Finding (F059)
The three-prefix system (qo-, o-, cth-) operates on stem classes with radically different suffix distributions: KL(qo-class || cth-class) = 4.726 bits — 8× larger than the overall A/B dialect divergence (0.586 bits). The cth-stem class (o/y/e-initial, A-dialect) strongly prefers -y (29.8%), -ol (20.0%), -or (13.8%); the qo-stem class (k/t-initial, B-dialect) strongly prefers -edy (14.6%), -eedy (11.8%), -ain (10.4%), -eey (9.8%). However, within each dialect, the stem-class distinction is smaller (KL ≈ 0.15-0.24 bits): the dominant suffix type in B (B-type) applies to ALL B words regardless of stem initial; the dominant suffix type in A (A-type) applies to all A words. The stem-class distinction is primarily a DIALECT-LEVEL feature, not a within-dialect grammatical category distinction. Key structural insight: 'cth' is itself a stem root (not a prefix) that takes A-type suffixes directly: cth+y, cth+ol, cth+or, cth+ey. This means the "cth-prefix" terminology is slightly misleading — 'cth' is one of the paradigm-taking stems in Currier A, alongside ch, sh, ot, ok (which were found to switch suffix preferences between A and B in exp_040).

## H058 Verdict: NOT SUPPORTED (as originally stated)
The k/t and o/y/e stem classes DO have different suffix distributions — but this difference is primarily a between-dialect effect, not a within-dialect grammatical category distinction. Within Currier B, qo-stems and other k/t-stems both use B-type suffixes. The 4.726-bit divergence between qo-class and cth-class reflects the A/B dialect split, not an independent stem-class grammar. The correct interpretation: dialect membership (A vs B) determines suffix paradigm selection; the stem-initial class (k/t vs o/y/e) is strongly correlated with dialect membership but does not independently govern suffix choice.
