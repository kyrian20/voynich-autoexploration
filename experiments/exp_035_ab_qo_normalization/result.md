# Experiment exp_035: A/B Divergence After qo-Normalization
Date: 2026-04-09

## Hypothesis Tested
Does removing qo-prefix from Currier B words bridge the A/B vocabulary gap? If qo is a B-dialect marker for A's bare k/t-initial stems, stripping qo from B should increase Jaccard and Spearman rho toward A-B alignment.

## Results

| Condition | Jaccard | Spearman ρ | Change |
|-----------|---------|------------|--------|
| Baseline | 0.152 | 0.348 | — |
| B qo-normalized | 0.139 | 0.386 | Jac -0.012, ρ +0.038 |
| Both A+B normalized | 0.153 | 0.387 | Jac +0.001, ρ +0.039 |

## Key Findings

### 1. qo-Normalization Barely Changes A/B Divergence
Stripping "qo" from B vocabulary DECREASES Jaccard slightly (-0.012) when only B is normalized. When both are normalized, Jaccard essentially doesn't change (+0.001). Spearman ρ improves only marginally (+0.038-0.039). The A/B divergence is nearly unaffected by qo removal.

### 2. Most qo-Stripped Stems Are NOT in A Vocabulary
Of the top-15 B-exclusive qo-words, 11/15 stripped stems do NOT appear in A vocabulary:
- qokeedy → keedy: **NOT in A**
- qotedy → tedy: **NOT in A**
- qoteedy → teedy: **NOT in A**
- qopchedy → pchedy: **NOT in A**

Only 4/15 stripped stems appear in A (qokchdy→kchdy, qopchdy→pchdy, qolchedy→lchedy, qolchey→lchey). The qo-words' stems are B-specific vocabulary items, not A-vocabulary with a prefix attached.

### 3. B-Exclusive qo-Words = 10.5% of B-Exclusive Vocabulary
397 out of 3766 B-exclusive vocab types are qo-words (10.5%). Stripping qo reduces B's total vocab from 4843 to 4554 types — the qo-prefix merges some previously distinct forms, reducing B's vocabulary diversity.

### 4. B H2 Changes Marginally
B original H2 = 1.928 bits; B normalized H2 = 1.988 bits (+0.060). The slight H2 increase after qo removal is consistent with removing the predictable qo→k bigram transition.

## Verdict

**qo normalization does NOT bridge the A/B gap.** The premise — that qo-B words are simply A-vocabulary with a "qo" prefix — is FALSE. The qo-stripped stems are B-specific items not found in A. The A/B divergence measured in exp_023 (Jaccard=0.148, ρ=0.337) is fundamentally driven by genuinely different vocabulary between the two dialects, not by the qo morphological prefix.

This REINFORCES exp_023's conclusion: A and B are NOT dialects of the same system. They have largely non-overlapping vocabularies that cannot be reconciled by prefix removal.

**Implication:** The exp_033 finding (qo is a B/bio dialectal marker) should be reinterpreted: qo is NOT a prefix that marks "B versions" of A words. Rather, qo is a prefix that appears on B-specific k-initial vocabulary items that have no A equivalents. The qo-paradigm (qo+k-stem) is a B-internal morphological system, not a B-vs-A substitution rule.
