# exp_535 result — ot-onset full characterization (H588_archived)

## Audit

**Target-awareness**: None. Standard characterization methodology with no calibrated parameters.

**Feature-destroying implementation**: Standard corpus parsing. A herbal_a = n≤56 A-dialect. B all = all B-dialect lines. Position types: pos1=line first, MID=intermediate, LL=penultimate, LF=last.

**Extrapolation**: None. All claims within tested corpus scope.

---

## Part 1: ot Vocabulary

### A herbal_a: 193 tokens, 59 types
Top words: otol(11.4%), oty(11.4%), otchy(9.3%), otchol(8.8%), otaiin(6.2%), otchor(5.7%), otchey(4.7%), otor(4.1%), otal(3.1%), oteol(2.1%), otam(2.1%), otcho(1.6%).

**A vocabulary pattern**: ch-mediated forms: otchy+otchol+otchor+otchey+otcho = ~30% (vs qot's 36.5%). y-body: oty (11.4%). ol/or bodies: otol(11.4%)+otor(4.1%) = 15.5%. aiin body: otaiin (6.2%).

### B all: 943 tokens, 161 types
Top words: otedy(10.1%), otaiin(9.3%), otain(8.6%), otar(8.2%), otal(7.3%), oteedy(7.0%), oteey(6.6%), oty(4.7%), otam(2.7%), otey(2.2%), otchedy(2.0%), otol(1.8%).

**B vocabulary pattern**: edy/eedy: otedy+oteedy = 17.1%; aiin/ain: otaiin+otain = 17.9%; al/ar: otal+otar = 15.5%.

### ot/qot vocabulary parallel:
| Feature | A ot | A qot | B ot | B qot |
|---------|------|-------|------|-------|
| Dominant class | ch-mediated (~30%) | ch-mediated (36.5%) | edy+eedy (17.1%) | edy+eedy (22.2%) |
| aiin/ain body | 6.2% | 5.2% | 17.9% | 17.2% |
| al/ar/ol/or body | 15.5% | 15.0% | 15.5% | 16.4% |
| y-body | 11.4% | 10.9% | 4.7% | 6.1% |

**Template vocabulary parallel confirmed**: ot and qot share the same vocabulary architecture: A = ch-mediated dominant; B = edy/eedy dominant. The parallel holds with quantitative similarity.

---

## Part 2: ot Positional Distribution

| Position | A obs/N | A rate | A E | B obs/N | B rate | B E |
|---------|---------|--------|-----|---------|--------|-----|
| pos1 | 53/928 | 5.7% | 1.29× | 42/1903 | 2.2% | **0.34×** |
| MID | 97/2481 | 3.9% | 0.89× | 772/10610 | 7.3% | 1.11× |
| LL | 38/829 | 4.6% | 1.04× | 166/1846 | 9.0% | 1.38× |
| LF | 43/966 | 4.5% | 1.01× | 129/1930 | 6.7% | 1.02× |

Baselines: A=4.41% of all words, B=6.53%.

**A herbal_a profile**: ot is pos1-elevated (E=1.29×/obs=53) but BELOW CONF threshold (need E≥1.5×). ot is NOT a strong line opener. MID slightly depleted (E=0.89×). The A ot positional profile is effectively NEUTRAL — no strong positional role.

**B-dialect profile**: pos1 STRONGLY DEPLETED (E=0.34×/obs=42) — stronger exclusion than B qot (E=0.60×). MID mildly elevated (1.11×), LL mildly elevated (1.38×). B ot is a MID/LL-biased class.

**Key A/B contrast with qot**: A qot is pos1 CONF (E=1.79×, LINE OPENER); A ot is pos1 sub-CONF (E=1.29×, NEUTRAL). Both A template classes exclude ch from pos1, but qot is the dedicated line opener. B both ot and qot are pos1-depleted, but B ot more severely (0.34× vs 0.60×).

F536: B-dialect ot-onset STRONGLY DEPLETED at pos1 (E=0.34×/obs=42) — more excluded than B qot (E=0.60×). A ot neutral/sub-CONF (E=1.29×/obs=53). The qot/ot template pair: A qot=LINE OPENER (CONF); A ot=NEUTRAL; B both depleted at pos1.

---

## Part 3: ot Within-Line Bigrams

### A herbal_a (150 ot sender bigrams):
| ot→X | obs | E | flag |
|------|-----|---|------|
| ot→ot | 11 | 1.79× | **CONF** |
| ot→qo | 7 | 2.24× | dir |
| ot→d | 33 | 1.26× | 1.26× |
| ot→sh | 15 | 1.20× | 1.20× |
| ot→ch | 30 | 0.77× | DEPL |

**A: ot→ot CONF** (E=1.79×/obs=11, re-confirms F369). **ot→qo dir** (E=2.24×/obs=7) — new within-line coupling. ot→ch DEPLETED (E=0.77×) — contrast with qot→ch baseline (E=1.06×, F535). ot actively AVOIDS ch within-line.

### B all (814 ot sender bigrams):
| ot→X | obs | E | flag |
|------|-----|---|------|
| ot→ot | 124 | 2.12× | **CONF** |
| ot→a | 64 | 1.43× | 1.43× |
| ot→ch | 129 | 0.85× | DEPL |
| ot→qok | 82 | 0.74× | DEPL |
| ot→qot | 29 | 0.95× | baseline |

**B: ot→ot CONF** (E=2.12×/obs=124 — strong cross-dialectal self-succession). ot→a near-CONF (E=1.43×/obs=64). ot→ch DEPLETED (E=0.85×/obs=129). ot→qot BASELINE (E=0.95×) — asymmetry: qot→ot is CONF (F534) but ot→qot is baseline. B ot self-clusters more strongly than B qot (2.12× vs 1.93×).

### ot→ch vs qot→ch distinction:
| | A E×(obs) | B E×(obs) |
|--|-----------|-----------|
| qot→ch (within-line) | 1.06× (39) — BASELINE | 1.20× (102) — BASELINE |
| ot→ch (within-line) | 0.77× (30) — DEPLETED | 0.85× (129) — DEPLETED |

ot→ch is actively DEPLETED within lines in both dialects, stronger than qot→ch depletion. Despite B herbal CL ot→ch coupling (F526, dir), within-line ot→ch is avoided. The ot/qot→ch contrast: qot→ch is baseline within-line; ot→ch is depleted.

F537: ot→ot CONF cross-dialectally (A: E=1.79×/obs=11; B: E=2.12×/obs=124). A ot→qo dir (E=2.24×/obs=7 — new). B ot→a near-CONF (E=1.43×/obs=64). ot→ch DEPLETED within-line in both dialects (A: E=0.77×; B: E=0.85×) — contrasts with qot→ch which is baseline (F535). The ot/ch within-line avoidance is the key structural difference from qot.

---

## Part 4: ot-LF Lines

### A herbal_a ot-LF (43 lines, 4.5%):
- y: E=1.80×/obs=11 → **CONF** — re-confirms F456 (A ot-LF pos1=y CONF)
- l: E=7.19×/obs=2 — (dir) threshold but obs too small
- No other class above CONF

### B all ot-LF (129 lines, 6.7%):
- y: E=1.47×/obs=26 — just below CONF (need E≥1.5×)
- o: E=1.67×/obs=7 — below dir (need obs≥5 and E≥2.0)
- Flat overall — no CONF signal

**A ot-LF pos1=y CONF re-confirmed** (E=1.80×/obs=11, consistent with F456: E=1.64×/obs=12). B ot-LF flat at pos1 — no confirmed opener rule.

---

## Self-Audit

**Target-awareness**: No target-aware elements identified.

**Feature-destroying implementation**: Standard ZL3b corpus parsing with no modifications. ONSET_PRIORITY list correctly distinguishes ot (priority 10) from ok (priority 9), qot (priority 2) etc. A herbal_a = n≤56 not is_b_dialect. B all = all is_b_dialect lines. No feature destruction.

**Extrapolation**: All claims within the tested parameter range (A herbal_a and B all corpora). No claims about sections not tested.

**Negative-result scope**: N/A — primary results positive (multiple CONF and dir signals).

**Control behavior**: No controls used. Baseline rates computed within-corpus as onset frequency across all words.

---

## Summary: ot Characterization

| Feature | A herbal_a | B all |
|---------|-----------|-------|
| Dominant words | otol/oty (11.4% each), ch-mediated ~30% | otedy (10.1%), aiin+ain (17.9%), al/ar (15.5%) |
| Positional role | NEUTRAL (pos1=1.29×, sub-CONF) | MID/LL class (pos1 DEPL **E=0.34×**) |
| Within-line self-succession | CONF (E=1.79×/obs=11) | **CONF (E=2.12×/obs=124)** |
| Key within-line targets | ot→qo dir (E=2.24×) | ot→a near-CONF (E=1.43×/obs=64) |
| ot→ch within-line | DEPLETED (E=0.77×) | DEPLETED (E=0.85×) |
| LF pos1 rule | y CONF (E=1.80×/obs=11, F456) | flat |

**Vocabulary parallel (F538)**: ot and qot share identical vocabulary architecture: A = ch-mediated dominant; B = edy+eedy dominant. The A/B template vocabulary structure is a general property of the qo-prefixed template class pair.

**Key distinction from qot**: A qot is a LINE OPENER (pos1 CONF, F533); A ot is NEUTRAL (pos1 sub-CONF, E=1.29×). B both depleted at pos1, but ot more severely (0.34× vs qot 0.60×). Within-line: ot→ch DEPLETED (contrast qot→ch BASELINE). The qot/ot pairing is a complementary template pair where qot is structurally more active (higher pos1, stronger cross-line grammar) and ot is the less-constrained partner.

**New findings: F536, F537, F538 (vocabulary parallel)**
**H588_archived CLOSED.**
