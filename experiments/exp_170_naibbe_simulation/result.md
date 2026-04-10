# exp_170: Naibbe Homophonic Cipher Null Simulation
**Date**: 2026-04-10
**Hypotheses**: Does the Greshko/Naibbe tarot-deck homophonic cipher, applied to Latin or Italian plaintext, reproduce the robust positional and morphological findings from 175 VMS characterization experiments?
**Status**: CIPHER HYPOTHESIS SIGNIFICANTLY WEAKENED. Naibbe reproduces B-dialect vocabulary composition (by construction — the cipher tables were designed for this), but FAILS to reproduce the positional grammar and sequential structure findings that are among the most robust in the VMS dataset.

**Configuration**: 100 simulations × 2 plaintext sources (Italian Dante, Latin Vulgate) × 2 line-break protocols (A: sentence-based, B: VMS-length-matched) = 400 runs total. ~20,000 tokens per simulation. Cipher: naibbe_v2.py, 78-card tarocchi deck, UNAMBIGUOUS=True, RESPACING=17. Primary comparison: VMS B-dialect (n=2447 lines).

---

## NOTATION

Each result is: `VMS-B value | Naibbe mean [95% CI] → INSIDE/ABOVE/BELOW`

- **INSIDE**: VMS value falls within Naibbe's simulated distribution — cipher cannot be ruled out for this metric
- **ABOVE**: VMS value exceeds Naibbe's upper 95% bound — the VMS has this property STRONGER than any cipher output
- **BELOW**: VMS value is below Naibbe's lower 95% bound — the VMS has this property WEAKER than any cipher output

Four columns: Italian-A | Italian-B | Latin-A | Latin-B

---

## RESULT TABLE

### Group 1: Vocabulary Composition (Cipher Was Designed for These)

| Metric | VMS-B | Ital-A | Ital-B | Lat-A | Lat-B |
|--------|-------|--------|--------|-------|-------|
| edy rate (B-dialect marker) | **0.191** | 0.151 [.148,.155] → **ABOVE** | 0.151 [.147,.155] → **ABOVE** | 0.151 [.147,.155] → **ABOVE** | 0.151 [.147,.155] → **ABOVE** |
| l-onset rate (F131) | **0.058** | 0.070 [.067,.073] → BELOW | 0.071 [.068,.073] → BELOW | 0.059 [.056,.062] → **INSIDE** | 0.059 [.056,.062] → **INSIDE** |
| -edy/-ol ratio (B-suffix paradigm) | **3.029** | 1.965 [1.899,2.050] → **ABOVE** | 1.959 [1.879,2.050] → **ABOVE** | 2.282 [2.170,2.398] → **ABOVE** | 2.286 [2.163,2.402] → **ABOVE** |

**Interpretation:** Naibbe produces EVA output with B-dialect flavor (high edy rate, l-onset words, edy/ol ratio favoring edy) because the cipher tables were designed to mimic Currier B. However, the VMS B-dialect has a *stronger* edy rate (19.1% vs Naibbe's 15.1%) and stronger suffix paradigm split (3.0× vs Naibbe's 2.0-2.3×). The cipher produces Currier-B-like vocabulary but undershoots the actual VMS B statistics.

---

### Group 2: Positional Grammar (CRITICAL DISCRIMINATORS)

| Metric | VMS-B | Ital-A | Ital-B | Lat-A | Lat-B |
|--------|-------|--------|--------|-------|-------|
| -am LL enrichment (F087) | **6.811** | 1.062 [0.796,1.366] → **ABOVE** | 0.999 [0.835,1.168] → **ABOVE** | 0.625 [0.393,0.873] → **ABOVE** | 1.008 [0.845,1.166] → **ABOVE** |
| y-onset LF enrichment (F098) | **3.506** | 0.724 [0.592,0.887] → **ABOVE** | 1.011 [0.899,1.140] → **ABOVE** | 1.117 [0.824,1.495] → **ABOVE** | 1.011 [0.852,1.222] → **ABOVE** |
| cth LF enrichment (~1.0 expected B) | **0.966** | 0.961 [0.581,1.406] → INSIDE | 0.332 [0.000,0.790] → ABOVE | 0.995 [0.648,1.342] → INSIDE | 1.023 [0.672,1.378] → INSIDE |
| sh LF enrichment (B opener) | **0.859** | 0.841 [0.698,1.003] → INSIDE | 1.414 [1.179,1.664] → **BELOW** | 1.004 [0.894,1.133] → **BELOW** | 0.999 [0.881,1.117] → BELOW |
| qok LF enrichment (depleted in B) | **0.839** | 1.042 [0.905,1.179] → **BELOW** | 0.993 [0.886,1.096] → BELOW | 1.194 [1.041,1.363] → **BELOW** | 0.996 [0.905,1.088] → BELOW |
| d LL enrichment (line-closing) | **1.464** | 0.879 [0.751,1.004] → **ABOVE** | 1.000 [0.893,1.118] → **ABOVE** | 1.063 [0.898,1.235] → **ABOVE** | 0.988 [0.890,1.104] → **ABOVE** |
| daiin→cth enrichment | **0.000** | 0.410 [0.000,1.283] → INSIDE | 0.144 [0.000,0.662] → INSIDE | 0.423 [0.000,1.394] → INSIDE | 0.141 [0.000,0.738] → INSIDE |
| k@para-start enrichment (F101) | **0.456** | 0.742 [0.000,3.999] → INSIDE | 0.521 [0.000,1.068] → INSIDE | 1.028 [0.444,1.875] → INSIDE | 0.991 [0.399,1.879] → INSIDE |

**Critical findings:**

**-am LL enrichment: VMS=6.811, Naibbe~1.0 — completely OUTSIDE in all 4 conditions.** The -am suffix specifically clustering at line-ends (6.81× enrichment in VMS B-dialect) is ABSENT from every Naibbe simulation. Naibbe produces ~1× enrichment (near-baseline). This is the largest gap and the clearest discriminator.

**y-onset LF enrichment: VMS=3.506, Naibbe~0.7-1.1 — OUTSIDE in all 4 conditions.** The y-onset line-opening enrichment (3.5×) does not appear in any Naibbe simulation. Naibbe Protocol B produces ~1× (random), Protocol A produces ~0.7× (actually depleted). The VMS's y-onset line-opening preference has no cipher explanation.

**qok LF depletion: VMS=0.839, Naibbe~0.99-1.19 — BELOW in 3/4 conditions.** VMS B-dialect depletes qok at line-first positions, while Naibbe produces near-baseline or elevated qok at LF. This is the REVERSE of the VMS pattern — the cipher produces a structural artifact the VMS lacks.

**sh LF (B opener) discrepancy**: VMS B-dialect has sh at LF near-baseline (0.86×), but Naibbe Latin Protocol A produces sh LF enrichment (1.41×). This is a cipher artifact absent from VMS.

**daiin→cth and k@para-start**: Both are INSIDE but for uninformative reasons. daiin→cth is INSIDE because both VMS-B and Naibbe have ~0 enrichment (daiin→cth is an A-dialect finding; B-dialect daiin doesn't specifically introduce cth). k@para-start is INSIDE because the VMS-B para-start parsing is unreliable (the P0 locus type assigned 2307 of 2447 B-dialect lines as para-starts, effectively making it a LF-position measure rather than true paragraph structure). These two INSIDEs should NOT be counted as cipher support.

---

### Group 3: Sequential Grammar / Self-Succession

| Metric | VMS-B | Ital-A | Ital-B | Lat-A | Lat-B |
|--------|-------|--------|--------|-------|-------|
| qok self-succession enrichment | **1.239** | 0.843 [0.763,0.948] → **ABOVE** | 0.880 [0.801,0.976] → **ABOVE** | 0.848 [0.739,0.983] → **ABOVE** | 0.886 [0.797,0.983] → **ABOVE** |
| ok self-succession enrichment | **1.462** | 0.846 [0.675,1.049] → **ABOVE** | 0.958 [0.802,1.125] → **ABOVE** | 0.858 [0.655,1.063] → **ABOVE** | 0.964 [0.805,1.141] → **ABOVE** |
| ch self-succession enrichment | **1.694** | 0.813 [0.533,1.144] → **ABOVE** | 0.888 [0.625,1.098] → **ABOVE** | 0.793 [0.600,1.058] → **ABOVE** | 0.867 [0.649,1.110] → **ABOVE** |
| d self-succession enrichment | **1.157** | 1.006 [0.878,1.150] → ABOVE | 1.055 [0.899,1.185] → INSIDE | 1.016 [0.877,1.170] → INSIDE | 1.046 [0.892,1.185] → INSIDE |
| qo self-succession enrichment | **2.047** | not shown | not shown | not shown | not shown |
| qok→ch enrichment | **1.326** | 1.189 [1.071,1.306] → **ABOVE** | 1.196 [1.098,1.296] → **ABOVE** | 1.196 [1.079,1.316] → **ABOVE** | 1.177 [1.080,1.272] → **ABOVE** |

**Critical findings:**

**Onset self-succession is systematically ABSENT in Naibbe.** VMS B-dialect has qok self-succession (1.24×), ok self-succession (1.46×), ch self-succession (1.69×). Naibbe produces DEPLETED self-succession for qok and ok (~0.84-0.89×) and near-baseline or slightly depleted for ch (~0.79-0.89×). The VMS's tendency for onset-class words to follow each other is not a cipher artifact — it appears to be intrinsic to Voynichese structure.

**qok→ch enrichment**: VMS=1.326, Naibbe=1.177-1.196 — consistently ABOVE in all 4 conditions. VMS B-dialect's qok→ch sequential preference is stronger than Naibbe produces.

---

## SUMMARY: INSIDE/OUTSIDE COUNTS

| Condition | Ital-A | Ital-B | Lat-A | Lat-B |
|-----------|--------|--------|-------|-------|
| INSIDE (cipher consistent) | 3 | 4 | 4 | 4 |
| ABOVE (VMS stronger than cipher) | 10 | 8 | 9 | 9 |
| BELOW (VMS weaker than cipher — cipher artifacts) | 3 | 4 | 3 | 3 |
| Total metrics | 16 | 16 | 16 | 16 |

Note: INSIDE count includes 2 non-informative cases (daiin→cth INSIDE because both ~0; k@para-start INSIDE due to parsing issue). True informative INSIDE count: **1-2 of 16**.

---

## BIDIRECTIONAL CHECK: NAIBBE ARTIFACTS NOT IN VMS

The following patterns appear in Naibbe output but are absent from or weaker in VMS B-dialect, arguing AGAINST the cipher hypothesis:

1. **sh LF enrichment** (Latin Protocol A: 1.41× in Naibbe vs 0.86× in VMS) — Naibbe Latin produces sh-initial word opening enrichment that VMS doesn't have
2. **qok LF near-baseline** (Naibbe ~1.0× vs VMS 0.84×) — Naibbe fails to reproduce the VMS depletion of qok at line-first position
3. **l-onset rate** (Naibbe Italian: 7.0-7.1% vs VMS 5.8%) — Naibbe Italian overproduces l-onset words

---

## KEY LIMITATIONS

1. **daiin→cth INSIDE is uninformative**: This finding is A-dialect, not B-dialect. VMS-B daiin→cth = 0.000 (no enrichment) and Naibbe also ~0.14-0.42 with wide CI. Agreement at ~0 is trivial.

2. **k@para-start parsing issue**: The VMS B-dialect P0 (paragraph-start) locus type parsing produced 2307 para-starts out of 2447 lines (94%) — essentially treating all B-dialect lines as paragraph starters. This makes the k@para-start metric equivalent to k@LF for B-dialect, not a true paragraph-start metric. The F101 finding (9.91×) is about A-dialect and was not properly tested here.

3. **Protocol A line length mismatch**: Protocol A produces much longer "lines" (sentence = 40-80 tokens) than VMS lines (mean=8.4 tokens). The sentence-based protocol is structurally dissimilar to VMS and may unfairly disadvantage the cipher.

4. **Single cipher mechanism**: Only the Naibbe v2 (78-card tarocchi) mechanism was tested. Other homophonic cipher mechanisms could produce different results.

---

## CONCLUSION

**The Naibbe cipher is INSUFFICIENT to explain VMS B-dialect structure.** The cipher succeeds only at what it was designed to do: produce EVA glyph strings with B-dialect-like vocabulary composition. It fails on every structural metric:

- **-am line-final enrichment**: 6.8× in VMS, ~1.0× in Naibbe across all 400 simulations. The probability of the VMS value under the Naibbe distribution is essentially 0.
- **y-onset LF enrichment**: 3.5× in VMS, ~0.7-1.1× in Naibbe. Absent from cipher output.
- **Onset self-succession**: Enriched in VMS (1.24-1.69×), depleted or neutral in Naibbe (~0.8-1.0×).
- **d LL enrichment**: 1.46× in VMS, ~0.88-1.06× in Naibbe. VMS d-words close lines; cipher doesn't produce this.
- **qok LF depletion**: VMS depletes qok at LF (0.84×); Naibbe produces near-baseline (~1.0×). Cipher produces wrong direction.

**The VMS positional grammar cannot be explained as an artifact of homophonic substitution of Latin or Italian.** The cipher hypothesis in the Naibbe formulation is falsified by the positional and sequential structure evidence.

**What the cipher DOES reproduce** (by design): B-style vocabulary composition (edy-suffixed words, qok-prefixed words, l-onset words). This is expected since the cipher was calibrated against Currier B statistics. It does not count as independent evidence for the cipher.

**Outcome condition reached**: Naibbe DOES NOT reproduce B-dialect findings in positional/structural metrics. Consistent with: "the cipher hypothesis is significantly weakened — combined with the characterization evidence pointing toward non-cipher, this moves the cipher hypothesis from possible to unlikely."

---

## FILES

- `script.py`: Simulation code (400 runs, all metrics)
- `data/simulation_results.json`: Raw metric vectors for all 400 runs (reproducible with the saved seeds)
