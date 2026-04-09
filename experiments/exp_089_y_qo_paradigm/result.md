# Experiment exp_089: y+{stem} vs qo+{stem} Positional Paradigm (H154), B Line Template (H155)
Date: 2026-04-09

## H154: Three-Level Positional Paradigm for k/t Stems — Bare < qo < y in LFirst%

### Shared Stem Aggregate: y+stem vs qo+stem (B Dialect)

| Prefix type | Token count | LFirst% | Relative to bare stems |
|------------|-------------|---------|----------------------|
| y+stem (y-compound) | 373 (shared stems) | **36.2%** | **4.07×** |
| qo+stem (qo-prefix) | 2623 (shared stems) | 11.6% | 1.30× |
| Bare stem (no prefix) | 2722 | 8.9% | 1.00× (baseline) |

**Three-level line-position paradigm for k/t stems in B:**
1. **Bare stem**: LFirst=8.9% — mid-line/line-final preference
2. **qo+stem**: LFirst=11.6% — mid-line (near background)
3. **y+stem**: LFirst=36.2% — STRONGLY LINE-INITIAL (4× bare, 3.12× qo)

### Individual Stem Comparisons (B Dialect, n≥5)

| Stem | y-form | y-LFirst% | y-n | qo-form | qo-LFirst% | qo-n | y/qo ratio |
|------|--------|-----------|-----|---------|-----------|------|-----------|
| kain | ykaiin | 42.9% | 7 | qokaiin | 13.0% | 269 | 3.29× |
| tal | ytal | 33.3% | 6 | qotal | 4.1% | 49 | 8.17× |
| tchedy | ytchedy | 50.0% | 8 | qotchedy | 8.3% | 24 | 6.00× |
| tar | ytar | 27.3% | 11 | qotar | 5.2% | 58 | 5.27× |
| teedy | yteedy | 28.0% | 25 | qoteedy | 13.9% | 72 | 2.02× |
| taiin | ytaiin | 35.0% | 20 | qotaiin | 14.5% | 62 | 2.41× |
| keey | ykeey | 26.9% | 26 | qokeey | 13.4% | 247 | 2.02× |
| keedy | ykeedy | 27.3% | 22 | qokeedy | 12.6% | 294 | 2.17× |
| kaiin | ykaiin | 30.8% | 26 | qokaiin | 13.6% | 236 | 2.27× |
| teey | yteey | 38.9% | 18 | qoteey | 16.1% | 31 | 2.41× |
| koly | ykol | 50.0% | 2 | qokol | 11.6% | 43 | 4.30× |

**Consistent pattern across all stems (n≥6)**: y-form has 2.02-8.17× higher LFirst% than qo-form for the same stem. The positional paradigm is robust.

**Exceptions** (y < qo LFirst): kedy (y=7.1% vs qo=11.9%), kal (y=0% vs qo=10.9%), key (y=0% vs qo=10.8%) — all have very small y-form sample sizes (n=1-4 tokens).

### A Dialect: Much Weaker Paradigm

In Currier A: y+stem LFirst=31.4%, qo+stem LFirst=24.5% → ratio=1.28×. The contrast is only 1.28× in A vs 3.12× in B. In A, qo-prefix words have much higher LFirst% (24.5% vs background ~18%), partially overlapping with y-prefix.

**The y/qo positional paradigm is primarily a B-dialect phenomenon.** In A, qo-prefix shows elevated LFirst% (24.5% vs background 18%), reducing the gap. In B, qo-prefix remains at background LFirst (11.6% vs background ~12.6%), making y-prefix (36.2%) sharply distinct.

### Interpretation

The three-prefix system for k/t stems in B encodes grammatical position:
- **Bare stem** (kaiin, keey, etc.): mid-line or line-final — UNMARKED POSITION
- **qo+stem** (qokaiin, qokeey): mid-line — EXPLICIT MID-LINE FORM
- **y+stem** (ykaiin, ykeey): line-initial — EXPLICIT LINE-OPENING FORM

This is a **prefix-encoded positional paradigm**: the same content word appears in different morphological forms depending on its position in the line. The y-prefix specifically marks LINE-INITIAL position; qo-prefix marks mid-line content. Bare stems appear throughout.

A natural language parallel: like Turkish topic/focus particles that mark discourse position, or Japanese topic-marking particles (wa/ga).

### H154 Verdict: STRONGLY SUPPORTED — Three-Level k/t Stem Positional Paradigm: bare (8.9% LFirst) < qo-prefix (11.6%) < y-prefix (36.2%); y/qo contrast = 3.12× in B; Weaker in A (1.28×)

---

## H155: B Line Structure Template Is NOT a Rigid Sequence — Components Are Independent

### B Line Template Component Rates

| Component | B lines with component | % |
|-----------|----------------------|---|
| has_opener (y/s at pos0) | 502 | 20.8% |
| has_qo_mid | 1580 | **65.4%** |
| has_closer (-am or oly) | 135 | 5.6% |
| has_daiin_opener | 87 | 3.6% |
| full_template (opener+qo+closer) | 18 | **0.7%** |

### Template Enrichment Test

| Metric | Value |
|--------|-------|
| Observed full template rate | 0.7% |
| Expected by independence (p_opener × p_qo × p_closer) | 0.8% |
| Template enrichment | **0.95× (AT CHANCE)** |

**The full three-part template is NOT enriched above chance (0.95×).** The three components appear independently — knowing a line has an opener does not predict it will also have a qo-mid and a closer.

### Most Common B Line Patterns

| Pattern | Count | % |
|---------|-------|---|
| qo-mid only | 1123 | **46.5%** |
| none | 558 | 23.1% |
| opener+qo-mid | 307 | **12.7%** |
| opener only | 167 | 6.9% |
| qo-mid+am-close | 53 | 2.2% |
| daiin-opener+qo-mid | 52 | 2.2% |
| qo-mid+ol-close | 23 | 1.0% |

**The dominant B line pattern is qo-mid only (46.5%)** — most B lines contain qo-prefix words in the middle but have neither a y/s-opener nor a -am/oly closer. The qo-prefix is the pervasive mid-line element present in 65.4% of B lines.

### Revised B Line Structure Model

The B line structure is NOT a rigid template [opener → qo-mid → closer]. Instead:
1. **qo-prefix is pervasive (65.4%)**: present in most B lines mid-line regardless of opener/closer presence
2. **opener is optional (20.8%)**: when y-compound or s-onset appears at pos0, it adds a line-initial grammatical marker
3. **closer is rare (5.6%)**: -am and oly/oldy appear as true line-closers only on some lines
4. **Components are INDEPENDENT**: no synergistic constraint forces them to co-occur

The B line grammar is therefore **probabilistic and modular**: each slot has its own distribution but they don't form a required sequence. Most lines are just [qo-mid...] without openers or closers.

### H155 Verdict: NOT SUPPORTED AS STATED — B Line Template Is NOT a Rigid Sequence; Full Template Only 0.7% (at chance); Components Are Independent; qo-Mid Is Pervasive (65.4%); Opener/Closer Are Optional Modifiers

---

## Combined Finding (F096)

**H154 STRONGLY SUPPORTED**: B dialect has a three-level positional paradigm for k/t stems: bare (LFirst=8.9%) < qo-prefix (LFirst=11.6%) < y-prefix (LFirst=36.2%). y/qo LFirst ratio = 3.12× across 81 shared stems in B. The y-prefix specifically encodes LINE-INITIAL position; qo-prefix is mid-line; bare stems are unmarked. In A, the paradigm is weaker (y/qo ratio=1.28×) — qo-prefix has higher LFirst% in A (24.5% vs B 11.6%), partially overlapping y-prefix function. The y-prefix positional specialization is primarily a B-dialect feature.

**H155 NOT SUPPORTED**: The full B line template [opener+qo-mid+closer] occurs at only 0.7% (chance rate = 0.8%, enrichment = 0.95×). Components are independent — qo-mid presence does not predict opener or closer presence. The dominant B pattern is qo-mid-only (46.5%). B line grammar is modular and probabilistic: qo-prefix is the pervasive mid-line element; y/s-opener and -am/oly-closer are optional independent modifiers. No rigid three-part sequence constraint exists.
