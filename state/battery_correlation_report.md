# Battery Correlation Report — exp_582

**Generated:** 2026-04-12  
**N trials:** 200  
**Architecture:** 21-mechanism, exp_314 parameters (beta_scale=1.8)  

---

## PCA Results

Eigenvalue decomposition of the 19×19 Pearson correlation matrix (N=200 trials).

| Component | Eigenvalue | Var% | CumVar% |
|-----------|-----------|------|---------|
| PC1 | 2.1928 | 11.5% | 11.5% |
| PC2 | 1.7871 | 9.4% | 20.9% |
| PC3 | 1.5660 | 8.2% | 29.2% |
| PC4 | 1.4145 | 7.4% | 36.6% |
| PC5 | 1.3526 | 7.1% | 43.8% |
| PC6 | 1.2140 | 6.4% | 50.1% |
| PC7 | 1.1627 | 6.1% | 56.3% |
| PC8 | 1.0572 | 5.6% | 61.8% |
| PC9 | 1.0431 | 5.5% | 67.3% |
| PC10 | 0.9619 | 5.1% | 72.4% |
| PC11 | 0.8771 | 4.6% | 77.0% |
| PC12 | 0.8349 | 4.4% | 81.4% |
| PC13 | 0.7346 | 3.9% | 85.3% |
| PC14 | 0.6868 | 3.6% | 88.9% |
| PC15 | 0.6581 | 3.5% | 92.3% |
| PC16 | 0.5372 | 2.8% | **95.2%** ← 95% threshold |
| PC17 | 0.4681 | 2.5% | 97.6% |
| PC18 | 0.4221 | 2.2% | 99.8% |
| PC19 | 0.0292 | 0.2% | 100.0% |

**Components for 95% variance: 16**  
**Components for 99% variance: 18**

---

## Effective Dimension

- **PCA (95% variance):** 16 components
- **Clustering |r|≥0.7:** 18 independent groups (17 singletons + 1 pair)
- **Clustering |r|≥0.5:** 18 independent groups (same structure)
- **Conservative estimate (min of PCA and |r|≥0.7):** **16**

---

## Cluster Structure at |r| ≥ 0.7

Total clusters/singletons: **18**

| Group | Metrics | Size | Interpretation |
|-------|---------|------|----------------|
| Cluster 1 | am_ll, am_mid_enr | 2 | Conservation constraint: blind LL pushes -am to LL at expense of MID position |
| Singleton | d_ll | 1 | — |
| Singleton | y_lf | 1 | — |
| Singleton | ss_mean | 1 | — |
| Singleton | adj_rate | 1 | — |
| Singleton | qok_lf | 1 | — |
| Singleton | d_lf | 1 | — |
| Singleton | s_lf | 1 | — |
| Singleton | ch_ll | 1 | — |
| Singleton | ok_ll | 1 | — |
| Singleton | qok_ll | 1 | — |
| Singleton | ss_d | 1 | — |
| Singleton | ss_y | 1 | — |
| Singleton | am_lf_enr | 1 | — |
| Singleton | edy_rate | 1 | — |
| Singleton | word_len_mean | 1 | — |
| Singleton | qok_ch | 1 | — |
| Singleton | global_am_rate | 1 | — |

---

## High-Correlation Pairs

### |r| ≥ 0.5 (strong correlations)

| Metric 1 | Metric 2 | r | Mechanism |
|----------|----------|---|-----------|
| am_ll | am_mid_enr | −0.9361 | Conservation: blind LL mechanism allocates -am across positions |

### |r| ≥ 0.3 (moderate correlations)

| Metric 1 | Metric 2 | r | Mechanism |
|----------|----------|---|-----------|
| am_ll | am_mid_enr | −0.9361 | Same as above |
| y_lf | ss_y | −0.3709 | y-onset is concentrated at LF; when more y tokens fall at LF, less available for y→y succession in MID |
| edy_rate | word_len_mean | +0.3550 | edy-suffix words are typically longer; higher edy_rate → slightly longer mean word length |

---

## Key Finding: High Independence of Battery Metrics

The correlation structure is nearly diagonal. Of 171 pairwise correlations:
- Only 1 pair exceeds |r|=0.5 (am_ll / am_mid_enr at −0.94)
- Only 2 additional pairs exceed |r|=0.3
- The remaining 168 pairs are near zero

**This means the 19 metrics are measuring approximately 16–18 genuinely independent aspects of simulation behavior.**

Expected mechanistic clusters that do NOT appear:
- ss_mean, ss_d, ss_y are all independent of each other despite all being driven by the copy-buffer
- qok_lf, qok_ll, qok_ch are all independent despite all being qok-related
- am_lf_enr, global_am_rate, am_mid_enr cluster only partially (am_lf_enr is independent)
- adj_rate is independent of ss_mean/ss_d/ss_y despite both being copy-buffer effects

Mechanistic explanation: although these metrics share common drivers, they sample different onset-class pools or different stochastic sub-processes, so trial-to-trial variation is uncorrelated.

---

## Methodological Notes

1. Each trial is an independent simulation run (2,411 lines) at exp_314 parameters. No parameter varies across trials — all variation is stochastic.
2. The correlation matrix measures how metrics co-vary across simulation runs due to internal randomness, not VMS corpus variation.
3. The conservation effect (am_ll/am_mid_enr at r=−0.94) is mechanistically expected: the blind LL mechanism commits -am to LL position with probability p_blind_n per line; when more lines trigger this, both am_ll and global_am_rate rise slightly but am_mid_enr falls because fewer -am tokens remain for MID positions.
4. PC19 eigenvalue = 0.029 corresponds to the linear combination am_ll + am_mid_enr, which is near-constant (the "conservation axis"). This single near-degenerate direction reduces effective PCA dimension from 19 to 18.
5. The PCA threshold (95%) requires 16 components because eigenvalues are distributed nearly uniformly across metrics — no single PC dominates. This "flat" spectrum is characteristic of high-dimensional independence.
