# exp_598 — Results: two-token successor-pair test (diagnostic only)

**Execution date:** 2026-10-19  
**Workflow:** https://github.com/kyrian20/voynich-autoexploration/actions/runs/39258767759  
**Machine output:** `results.json`

## Outcome and protocol diagnostic

The run completed successfully, but the predeclared rare-pair collapse rule was too aggressive to provide a useful inferential test in this corpus. In Currier-B P0:

| Starter | Lines | Unique raw two-token pairs | Fraction of lines collapsed to `<RARE_PAIR>` |
|---|---:|---:|---:|
| `daiin` | 89 | 89 | 100.0% |
| `dain` | 34 | 34 | 97.1% |
| `saiin` | 46 | 46 | 97.8% |

After collapse, the entire `daiin` pair distribution consists of a single catch-all category (entropy 0 bits). Consequently, the very small post-collapse JSD values (0.0004–0.0149 bits) and nonsignificant permutation outcomes (Holm-adjusted p 0.83–1.00) **must not be interpreted as evidence that the two-token contexts are the same**. The collapse removed nearly all of the sequence information being studied.

The same collapse pattern appears in ZL3a because these files have the same counts for the three starter groups and very similar token data. This does not turn the uninformative result into independent confirmation.

## Research decision

**Mark the joint-pair inferential part of exp_598 as uninformative due to sparsity. Preserve it as a failed sensitivity rather than claiming a null finding about context equivalence.** This is a method result: exact two-token pairs are too sparse at these sample sizes for the chosen pooled-frequency threshold.

## Corrective follow-up

Exp_599 will analyze the first successor (token offset +1) and second successor (offset +2) as separate marginal distributions, rather than treating the ordered two-token pair as one rare category. It will retain all observed tokens, use the same JSD/permutation framework, adjust across three starter-group comparisons at each offset within each transcription, and report raw support counts. This preserves information at both positions without converting nearly every context into a catch-all bucket.

No semantic interpretation is claimed.
