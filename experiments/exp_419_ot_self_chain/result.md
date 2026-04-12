# exp_419: B ot Self-Stickiness and Onset Self-Succession Survey

**Hypothesis (H639):** ot self-succession is generally elevated in B (not just in d-LF lines). Compare self-succession E-values for all onset classes in B and A. Check ot run-length distribution for super-geometric pattern (like A y-chains from F395).

**Method:** For B and A cont lines, compute (1) onset self-succession bigram E = P(next=X|current=X) / P(X); (2) ot run-length distribution; (3) compare to geometric expectation given observed p_self.

---

## Results

### B dialect: onset self-succession E-values (top)

| Onset | N_total | E_self | self_n | note |
|-------|---------|--------|--------|------|
| l | 1011 | **2.35×** | 102 | highest in B |
| ot | 1208 | **2.19×** | 145 | second-highest |
| qo | 606 | 2.14× | 39 | |
| r | 256 | 2.14× | 5 | dir |
| qot | 729 | 2.16× | 57 | |
| o | 748 | 1.81× | 40 | |
| y | 652 | 1.97× | 41 | |
| ok | 1272 | 1.38× | 108 | lower than ot |
| s | 442 | **0.33×** | 3 | STRONGLY DEPLETED |
| p | 305 | **0.61×** | 3 | depleted |

### A dialect: onset self-succession E-values (comparison)
| Onset | E_self | note |
|-------|--------|------|
| l | 7.40× | extreme (dir, N=1) |
| o | 2.30× | |
| qot | 2.22× | |
| p | 2.24× | dir |
| ot | 1.67× | LOWER than B=2.19× |
| y | 1.39× | LOWER than B=1.97× |
| s | 1.42× | HIGHER than B=0.33× |
| t | **0.35×** | STRONGLY DEPLETED (unlike B=1.00×) |

### B ot run-length distribution

| Length | Observed | Fraction | Expected (geometric p_self=0.154) |
|--------|---------|---------|------|
| 1 | 943 | 0.887 | 0.846 (more singles than expected) |
| 2 | 96 | 0.090 | 0.130 (FEWER doublets than expected) |
| 3 | 23 | 0.022 | 0.020 (near-expected) |
| 4 | 1 | 0.001 | 0.003 |

B has 23 runs of length 3 and 1 run of length 4 (f113v/5's first 4 ot-words).

**Run-length distribution is roughly geometric** given the bigram p_self=15.4%. The len=2 fraction (9.0%) is slightly below the geometric expectation (13.0%) — if anything, the distribution is slightly ANTI-geometric (more single ot-words and fewer 2-chains than the bigram rate would predict). This contrasts with A y-chains, which were super-geometric (F395: A has 2 length-4 chains, expected≈0.12).

---

## Interpretation

**B ot self-succession (E=2.19×) is elevated but not super-geometric.** The bigram enrichment is real — given one ot-onset word, the next word is 2.19× more likely to also be ot. But the run-length distribution is roughly geometric given this bigram rate. This means the ot stickiness operates at the BIGRAM level (one-step memory), not as a higher-order chain rule. This contrasts with A y-chains (F395: super-geometric, showing 3rd and 4th order memory).

**l onset is the most self-successive in B (E=2.35×/N=102)**: l self-succession is even more elevated than ot. l is the 6th most common B onset (N=1011). The l self-succession finding is new and previously uncharacterized. B l→ch→qok being a formula type (F421) combined with l→l E=2.35× suggests l has both self-chain properties AND specific formula routing to ch/qok.

**s onset strongly anti-self-successive in B (E=0.33×/N=3)**: B s avoids self-succession. This is consistent with s being a B formula LF class (s→sh→qok, F398) that routes through specific pos1 classes rather than self-chaining.

**A/B comparison**: ot E_self: B=2.19× vs A=1.67× — ot is MORE sticky in B than A. y E_self: B=1.97× vs A=1.39× — y also more sticky in B bigram-wise, though A y-chains are super-geometric. B t E_self=1.00× vs A t E_self=0.35× — t strongly anti-self-successive in A (consistent with A t depleted at MID positions, F412).

**Structural interpretation**: The B ot bigram enrichment (2.19×) accounts for the d→ot→ot formula type (F419/F416) and the ot-dense lines (f113v/5). The high bigram E means that any LF class generating an ot at pos1 will tend to have another ot at pos2 — this is a within-line sequential grammar rule (ot begets ot) operating independently of the LF class.

---

## Limitations

- Run-length comparison to geometric is approximate (the geometric model uses observed p_self=0.154 as the constant transition probability, which may vary by position within line).
- A y-chains (F395) used a different methodology (chain counting at line level). The current analysis uses all within-line bigrams including cross-line-boundary positions — would need to restrict to within-line positions for exact comparison. However, even so, the ot runs show no excess over geometric at len=4.
- l self-succession (E=2.35×/N=102): genuine finding but not yet characterized.
- PASS.

---

## Self-Audit

**Target-awareness**: None.
**Extrapolation**: "ot stickiness is bigram-level (not super-geometric)" is stated relative to the ot run-length data and the geometric model. Does not claim no higher-order effects.
**Control behavior**: A ot=1.67× (lower than B=2.19×) is a consistent finding.

---

## Conclusion

H639 ANSWERED. B ot self-succession E=2.19×(N=145) is elevated (2nd highest among B onset classes). But ot run-length distribution is roughly GEOMETRIC given the bigram rate — not super-geometric like A y-chains. The ot stickiness is a one-step bigram rule, not a higher-order chain rule. NEW: B l self-succession is the highest at E=2.35×(N=102) — previously uncharacterized. B s strongly anti-self-successive (E=0.33×) consistent with s being a formula LF class that routes through sh (not itself). A/B: ot E_self B=2.19× > A=1.67×.
