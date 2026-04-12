# exp_548 result — o→a coupling deep characterization (H_new_FJ)

## Audit

**Target-awareness**: None. Tests specific sub-questions generated from F563 (o→a CONF cross-dialectally).

**Feature-destroying implementation**: Same corpus parsing as exp_547. B section classification uses folio-number from folio_raw. Bigrams use MID-position baseline. Reverse coupling a→o uses same MID baseline as numerator target.

**Extrapolation**: None. Each section tested independently; B pharma is the only B section with sufficient power for formal CONF claim.

---

## Results

### Part 1: Specific a-onset words following o

**A herbal_a** (67 o→a obs):
- aiin: **29 (43.3%)** — dominant single word
- ar: 8 (11.9%)
- al: 6 (9.0%)
- aiiin: 5 (7.5%)
- ain: 3 (4.5%)
- all others: 1 each

**B all** (27 o→a obs):
- aiin: **8 (29.6%)** — still dominant
- ar: 3 (11.1%)
- all others: 1 each (alys, aly, al, aiiin, ail, etc.)

**Position of o-sender in o→a pairs:**
| Pos | A | B |
|-----|---|---|
| MID | 61.2% (41/67) | 77.8% (21/27) |
| LL | 20.9% (14/67) | 18.5% (5/27) |
| pos1 | 17.9% (12/67) | 3.7% (1/27) |

The o→a coupling is predominantly a **MID-position phenomenon** — not near LF. The primary specific coupling is **o → "aiin"** (standalone word). In A herbal_a, 43% of all o→a pairs are [o-word][aiin]; in B all, 30%. Additional targets: 'ar', 'al', 'aiiin', 'ain' — all a-class lateral/aiin words.

### Part 2: Reverse coupling a→o — MUTUAL

| | A herbal_a | B all |
|--|-----------|-------|
| a-sender bigrams | 381 | 295 |
| a→o obs | 25 | 19 |
| a→o exp | 15.8 | 7.5 |
| a→o E | **1.58×** | **2.54×** |
| flag | **CONF** | **CONF** |

**The o↔a coupling is BIDIRECTIONAL and MUTUAL**: both o→a and a→o are CONF in both dialects. o→a is the dominant direction (E=3.08–3.17×) but a→o is also CONF (A: 1.58×; B: 2.54×). This means o and a have mutual affinity — they appear adjacent to each other in either order at above-baseline rate.

### Part 3: B section scope — B-dialect-wide (directional)

| Section | N lines | o-sender | o→a obs | exp | E | flag |
|---------|---------|----------|---------|-----|---|------|
| B herbal | 162 | 36 | 4 | 1.4 | 2.92× | (dir) |
| B astro | 544 | 56 | 5 | 1.0 | **5.23×** | dir |
| B pharma | 577 | 137 | 18 | 7.3 | **2.48×** | **CONF** |

All three B sections show elevated o→a (E≥2.4× in all). B pharma provides CONF-level obs; B astro shows the highest E (5.23×) with small N; B herbal is (dir). The o→a coupling is **B-dialect-wide** — not section-specific. B pharma provides the CONF anchor but the pattern is consistent across all B sections.

### Part 4: A section scope — underpowered outside A herbal_a

| Section | N lines | o-sender | o→a obs | E | flag |
|---------|---------|----------|---------|---|------|
| A herbal_a | 2033 | 435 | 67 | 3.08× | CONF |
| A stars | 14 | 3 | 1 | 2.86× | — (underpowered) |
| A cosmo | 4 | 0 | 0 | — | — |

A stars has only 3 o-sender bigrams — underpowered. The coupling is CONF in A herbal_a; section scope cannot be determined outside A herbal_a due to size constraints.

### Part 5: a-onset bigram profile — RICH GRAMMAR

**A herbal_a** (381 a-sender bigrams):

| a→X | obs | exp | E | flag |
|-----|-----|-----|---|------|
| a→a | 60 | 19.1 | **3.15×** | **CONF** |
| a→ok | 50 | 31.3 | **1.60×** | **CONF** |
| a→ol | 30 | 15.4 | **1.95×** | **CONF** |
| a→o | 25 | 15.8 | **1.58×** | **CONF** |
| a→d | 17 | 33.4 | 0.51× | DEPL |
| a→qok | 13 | 31.2 | 0.42× | DEPL |
| a→ch | 68 | 89.1 | 0.76× | — |

**B all** (295 a-sender bigrams):

| a→X | obs | exp | E | flag |
|-----|-----|-----|---|------|
| a→a | 44 | 11.0 | **4.01×** | **CONF** |
| a→ok | 34 | 21.3 | **1.60×** | **CONF** |
| a→ol | 29 | 15.3 | **1.89×** | **CONF** |
| a→o | 19 | 7.5 | **2.54×** | **CONF** |
| a→y | 15 | 6.1 | **2.45×** | **CONF** |
| a→k | 10 | 6.3 | **1.59×** | **CONF** |
| a→d | 6 | 14.5 | 0.41× | DEPL |
| a→qok | 9 | 48.7 | 0.18× | DEPL |
| a→l | 9 | 17.0 | 0.53× | DEPL |

**a→a CONF cross-dialectally** (A: E=3.15×/obs=60; B: E=4.01×/obs=44) — very strong a self-succession. a→ok CONF both (A: 1.60×/50; B: 1.60×/34). a→ol CONF A (1.95×/30), near-CONF B (1.89×/29). DEPL: a→d (A: 0.51×; B: 0.41×); a→qok (A: 0.42×; B: 0.18×). B-specific: a→y CONF (2.45×/15); a→k CONF (1.59×/10). The a-class has a **rich, cross-dialectally stable bigram grammar** that makes it a highly structured onset class.

---

## New Findings

**F565: o→a coupling is primarily [o-word][aiin]** — in A herbal_a, 43% of o→a pairs (29/67) have 'aiin' as the specific target; in B, 30% (8/27). Secondary targets: 'ar', 'al', 'aiiin'. The coupling predominantly occurs at MID positions (A: 61%; B: 78%) — not near LF. The phrase pattern [o-word][aiin] is the dominant specific realization of the o→a coupling.

**F566: o↔a MUTUAL CONF coupling** — both directions CONF in both dialects. o→a CONF (F563: E≈3.1×); a→o CONF (A: E=1.58×/obs=25; B: E=2.54×/obs=19). o→a is the dominant direction (~2× stronger). The o-a dyad forms a bidirectional affinity cluster within VMS lines, predominantly at MID positions. Coupled with a→a CONF (F567), the a-class forms extended a-clusters potentially preceded by an o-word.

**F567: o→a B-dialect-wide** — all B sections show elevated o→a (B astro: E=5.23×/dir; B herbal: E=2.92×/(dir); B pharma: E=2.48×/CONF). Not section-specific. The coupling is B-dialect-wide, with B pharma providing CONF anchor.

**F568: a-onset bigram grammar CONF cross-dialectally** — a→a CONF (A: E=3.15×/obs=60; B: E=4.01×/obs=44 — one of the strongest bigram signals); a→ok CONF both (A/B: 1.60×); a→ol CONF A (1.95×/30); a→o CONF both (reverse of F563). DEPL: a→d (A: 0.51×; B: 0.41×); a→qok (A: 0.42×; B: 0.18×). B-specific additions: a→y CONF (2.45×/15); a→k CONF (1.59×/10). The a-class has one of the richest characterized bigram grammars — dominated by a-class self-succession and ok/ol affinities, while strongly avoiding d and q-class onsets.

---

## Summary

- **H_new_FJ CLOSED**: o→a coupling characterized. The coupling is primarily [o-word][aiin] (43% of A obs), occurs at MID positions, is mutual (a→o also CONF), and is B-dialect-wide (all B sections show (dir)+).
- **F565**: o→a primarily [o-word][aiin]; MID-position dominant
- **F566**: o↔a mutual CONF coupling (both directions; o→a stronger)
- **F567**: o→a B-dialect-wide (consistent across all B sections)
- **F568 KEY**: a-onset bigram grammar: a→a CONF cross-dialectally (3.15×A/4.01×B); a→ok CONF both; a→ol CONF A; a→o CONF both; DEPL: d, qok; B additions: a→y CONF, a→k CONF
- **New hypothesis**: a-onset full characterization (positional + vocabulary + LF pos1) — a has a rich bigram grammar but no characterized positional profile
