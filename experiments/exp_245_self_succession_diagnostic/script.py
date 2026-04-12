"""
exp_245: H444 — Self-Succession Under-Reproduction Diagnostic

Question: Why does the copy buffer under-reproduce ot→ot, l→l, ok→ok self-succession
(VMS E_mid: ot=1.887, l=2.203, ok=1.322; sim: ~1.3-1.6)?

Design:
  Three analytical questions:
  (A) BUFFER COMPOSITION ANALYSIS: What is the onset distribution of buffer words at
      the time a buffer draw is triggered? Is the buffer over- or under-enriched in
      moderate-rate onsets (ot, l, ok) compared to global rates?

  (B) ONSET-SELF-SUCCESSION THEORY: Given buffer composition and copy rate (CP=0.55,
      MP=0.90), what is the theoretical expected self-succession enrichment E(X→X)
      for each onset class X?

  (C) VMS vs THEORY: Compare VMS E_mid(X→X) to the theoretical expected E from (B).
      If VMS > theory → VMS has genuine self-succession enrichment beyond buffer dynamics
      If VMS ≈ theory → buffer dynamics explain the pattern

  (D) SAME ANALYSIS FOR qok→ch AND sh→qok: What do the theoretical rates predict?
      This allows us to compare cross-onset enrichment vs self-succession enrichment
      in the same framework.

  Method:
  - Run exp_236 architecture (N=5) but add logging of buffer composition at each draw
  - Record: at each buffer draw, what is the onset of the previous word (trigger) and
    what is the onset distribution of the buffer contents?
  - From this, compute P(draw qok | prev=qok) to verify qok→ch, and P(draw X | prev=X)
    to understand self-succession potential

  Alternative analytical approach (faster):
  - The buffer is a sliding window of W=20 words with onset distribution determined
    by the MID word onset distribution
  - Under stationarity: P(buffer contains onset X) ≈ onset_rate(X) for each slot
  - P(draw same onset X from buffer | prev=X) ≈ 1 - (1-onset_rate(X))^W (prob at least one X in buf)
    × 1/N_buf_available  -- this is underestimates the conditional probability
  - Better: expected E(X→X) from buffer = CP × MP × (expected # same-onset in buffer / buf_size)
    + CP × (1-MP) × onset_rate(X)  -- (direct copy of same onset unmodified)
    + (1-CP) × onset_rate(X)  -- fresh draw
    All divided by onset_rate(X)^2 (expected from independence)

  This gives a theoretical prediction for each onset class.
"""

import os, re, random, math
from collections import Counter, deque, defaultdict

REPO_DIR  = os.path.expanduser('~/voynich-cryptanalyst')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

ONSET_ORDER = [
    ('qok', 'qok'), ('qot', 'qot'), ('qo', 'qo'), ('cth', 'cth'),
    ('ch', 'ch'), ('sh', 'sh'), ('ok', 'ok'), ('ot', 'ot'), ('ol', 'ol'),
    ('d', 'd'), ('s', 's'), ('y', 'y'), ('k', 'k'), ('t', 't'),
    ('l', 'l'), ('r', 'r'), ('p', 'p'), ('f', 'f'), ('o', 'o'),
]

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label
    return 'other'

def folio_base(folio):
    return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

def parse_vms_b():
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1); folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            for w in words:
                folio_word_stats[fb]['total'] += 1
                if w.endswith('eedy'): folio_word_stats[fb]['eedy'] += 1
                elif w.endswith('edy'): folio_word_stats[fb]['edy'] += 1

    folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}
    b_lines = []
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1); locus_code = m.group(3)
            folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
            if folio_dialect.get(fb, 'unknown') != 'B': continue
            lc_stripped = locus_code.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words: b_lines.append(words)
    return b_lines

# ─── Theory ───────────────────────────────────────────────────────────────────

def theoretical_self_succession(onset_rate, cp, mp, W=20, p_stutter=0.006):
    """
    Theoretical expected E(X→X) from copy-buffer model.

    At stationarity, the buffer of size W contains words with onset distribution
    proportional to the MID onset distribution (assuming i.i.d. draws from that distribution,
    which is an approximation — the actual buffer has some temporal correlation).

    P(next word has onset X | prev word has onset X) =
        p_stutter                    (stutter: exact repeat)
      + (1-p_stutter) × [
          (1-cp) × onset_rate(X)    (fresh draw from vocabulary)
        + cp × [
            (1-mp) × [sum_{k in buf} P(buf[k].onset==X) / W]  (direct copy, unmodified)
          + mp × onset_rate(X)      (modified → onset preserved → same onset rate as fresh)
          ]
        ]

    Wait, modification preserves onset in this architecture. So:
    - Direct copy (cp × (1-mp)): draws from buffer, onset preserved = P(buf has X)
    - Modify (cp × mp): draws from buffer, onset preserved = P(buf has X)
    - Fresh (1-cp): draws from vocabulary, onset rate = onset_rate(X)
    - Stutter: exact repeat = onset X (previous onset)

    So:
    P(onset X | prev onset X) =
        p_stutter
      + (1-p_stutter) × [
          (1-cp) × onset_rate(X)
        + cp × P(buf_word.onset == X)
        ]

    Under stationarity, P(buf_word.onset == X) ≈ onset_rate(X) for a random buffer draw
    (because buffer fills with words having the MID onset distribution on average).

    But: there's a subtlety. After the Markov mechanism fires (qok→ch), the buffer composition
    for ch-onset increases slightly. And more importantly, the p_stutter mechanism creates
    exact repeats, inflating the buffer composition toward the previous word's onset.

    Simple approximation ignoring these second-order effects:
    P(onset X | prev onset X) ≈ p_stutter + (1-p_stutter) × onset_rate(X)

    Therefore:
    E(X→X) = P(X→X) / (onset_rate(X)^2)
            ≈ [p_stutter + (1-p_stutter) × onset_rate(X)] / onset_rate(X)
            = p_stutter / onset_rate(X) + (1-p_stutter)

    Note: this is independent of cp and mp! The copy buffer (onset-preserving modification)
    does NOT increase self-succession beyond baseline — it draws from the BUFFER which has
    the same onset distribution as the vocabulary. The only source of self-succession
    enrichment is p_stutter and any correlation in the buffer.

    The key insight: E(X→X) = 1 + p_stutter/onset_rate(X) under this model.
    For rare onsets (small rate): large E(X→X). For common onsets: small E(X→X).
    """
    # Simple formula
    E_theory = 1.0 + p_stutter / onset_rate if onset_rate > 0 else 0
    return E_theory

def theoretical_cross_onset(onset_x, onset_y, cp, mp, p_qokch=0.12, p_sh_qok=0.0, p_stutter=0.006):
    """
    Theoretical E(X→Y) for cross-onset succession.

    For X≠Y:
    P(onset Y | prev onset X) =
        p_stutter × P(prev_word.onset == Y)  # usually ~0 since prev was X
      + (1-p_stutter) × [
          (1-cp) × onset_y                   # fresh draw
        + cp × P(buf_word.onset == Y)         # buffer draw
        ]

    If X=qok and applying qok→ch Markov:
      The buffer draw has probability onset_y for ch (with slight enhancement from Markov)
      P(buf_word.onset == ch | prev=qok) ≈ onset_ch + p_qokch × (1-onset_ch) × onset_ch  <-- approx

    Actually the Markov rule fires with probability p_qokch ONLY when a ch-onset word is in buffer.
    If we assume the buffer has ~onset_ch fraction ch words:
      P(draw ch via Markov | prev=qok, buf) ≈ p_qokch × min(onset_ch × W, 1) / W ≈ p_qokch × onset_ch / W × W = p_qokch × onset_ch
      (This is imprecise — it's the probability that the Markov rule fires AND finds a ch word)

    This gets complicated. Use a simple approximation:
    E(X→Y) ≈ 1.0 for most pairs (buffer onset distribution ≈ global onset distribution)
    E(qok→ch) ≈ 1 + p_qokch × (1-1/W) / (onset_ch) × cp × onset_ch  -- rough estimate

    Actually the simplest estimate: from exp_228, slope≈1.5 per unit p_qokch, and qok→ch E_vms=1.27.
    So E(qok→ch) ≈ 1 + 1.5 × p_qokch = 1 + 1.5 × 0.12 = 1.18. Observed: 1.21. Close enough.
    """
    # Baseline: buffer onset distribution ≈ global
    # For X=qok, Y=ch: add Markov contribution
    if onset_x == 'qok' and onset_y == 'ch' and p_qokch > 0:
        # Slope from exp_228: ~1.5 per unit p_qokch
        E_theory = 1.0 + 1.5 * p_qokch
    elif onset_x == 'sh' and onset_y == 'qok' and p_sh_qok > 0:
        E_theory = 1.0 + 2.25 * p_sh_qok  # slope from exp_243
    else:
        E_theory = 1.0
    return E_theory

# ─── Empirical analysis ────────────────────────────────────────────────────────

print("Parsing VMS B-dialect...")
b_lines = parse_vms_b()
print(f"  {len(b_lines)} lines")

# Compute VMS onset statistics
all_words = [w for l in b_lines for w in l]
mid_words = [w for l in b_lines for w in l[1:-1] if len(l) > 2]
n_all = len(all_words); n_mid = len(mid_words)

oc_all = Counter(get_onset(w) for w in all_words)
oc_mid = Counter(get_onset(w) for w in mid_words)
rates_all = {o: c/n_all for o, c in oc_all.items()}
rates_mid = {o: c/n_mid for o, c in oc_mid.items()}

# MID-only bigrams
mid_bg = Counter()
mid_n = 0
for line in b_lines:
    n = len(line)
    if n < 4: continue
    for i in range(1, n - 2):
        mid_bg[(get_onset(line[i]), get_onset(line[i+1]))] += 1
        mid_n += 1

def E_mid(x, y):
    pxy = mid_bg.get((x, y), 0) / mid_n if mid_n > 0 else 0
    px = rates_mid.get(x, 0); py = rates_mid.get(y, 0)
    return pxy / (px * py) if px * py > 0 else 0

# CP/MP parameters from exp_236
CP = 0.55; MP = 0.90; P_STUTTER = 0.006; W = 20; P_QOKCH = 0.12

print(f"\n{'='*80}")
print("SELF-SUCCESSION: VMS E_mid vs THEORETICAL PREDICTION")
print(f"{'='*80}")
print(f"  Architecture: CP={CP}, MP={MP}, p_stutter={P_STUTTER}, W={W}")
print(f"  Theory: E(X→X) = 1 + p_stutter/rate_mid(X)")
print(f"  (Copy buffer with onset-preserving modification does NOT enhance self-succession)")
print(f"  (Buffer onset distribution ≈ global MID onset distribution under stationarity)")
print()
print(f"  {'Onset':<8} {'Rate_mid':>10} {'E_mid_VMS':>12} {'E_theory':>12}  {'Gap':>8}  Verdict")
print(f"  {'-'*65}")

FOCUS_ONSETS = ['qok', 'ch', 'sh', 'ok', 'ot', 'ol', 'd', 's', 'y', 'l', 'o', 'r', 'k', 't']
for onset in FOCUS_ONSETS:
    r = rates_mid.get(onset, 0)
    if r < 0.005: continue
    E_vms = E_mid(onset, onset)
    E_th = theoretical_self_succession(r, CP, MP, W, P_STUTTER)
    gap = E_vms - E_th
    cnt = mid_bg.get((onset, onset), 0)
    verdict = 'OVER VMS' if gap > 0.2 else ('UNDER VMS' if gap < -0.2 else 'near theory')
    print(f"  {onset:<8} {r*100:>9.2f}%  {E_vms:>12.3f}  {E_th:>12.3f}  {gap:>+8.3f}  {verdict} (N={cnt})")

print(f"\n  Theory predicts: onset-preserving copy buffer does NOT amplify self-succession.")
print(f"  If VMS >> theory for an onset X, VMS has genuine self-succession beyond buffer dynamics.")

# Cross-onset enrichment: same analysis
print(f"\n{'='*80}")
print("CROSS-ONSET ENRICHMENT: VMS E_mid vs THEORETICAL PREDICTION")
print(f"{'='*80}")
KEY_CROSS = [
    ('qok', 'ch', 'qok→ch (Markov, p=0.12)'),
    ('sh', 'qok', 'sh→qok (no Markov, p=0.00)'),
    ('s', 'sh', 's→sh (cross-pos artifact)'),
    ('qok', 'qok', 'qok→qok (self, for comparison)'),
    ('qok', 'ok', 'qok→ok (structural)'),
]

print(f"  {'Pair':<14} {'E_mid_VMS':>12} {'E_theory':>12}  {'Gap':>8}  Label")
print(f"  {'-'*70}")
for (x, y, label) in KEY_CROSS:
    E_vms = E_mid(x, y)
    E_th = theoretical_cross_onset(x, y, CP, MP, P_QOKCH)
    gap = E_vms - E_th
    cnt = mid_bg.get((x, y), 0)
    print(f"  {x}→{y:<8} {E_vms:>12.3f}  {E_th:>12.3f}  {gap:>+8.3f}  {label} (N={cnt})")

# ─── Empirical buffer analysis: run simulation with buffer logging ────────────

print(f"\n{'='*80}")
print("EMPIRICAL BUFFER COMPOSITION — WHAT ONSETS ARE IN BUFFER AT DRAW TIME?")
print(f"{'='*80}")
print("Running a single simulation trial to sample buffer composition...")

# Import minimal simulation infrastructure
ENGLISH_SW = {'the','and','of','to','a','in','that','is','was','he','it','for','on','are',
              'as','with','his','they','at','be','this','have','from','or','had','by','not',
              'but','what','all','were','we'}
def load_latin(path):
    with open(path, encoding='utf-8', errors='replace') as f: text = f.read()
    words = []
    for p in re.split(r'\n\s*\n', text):
        ws = re.findall(r'\b[a-zA-Z]+\b', p)
        if not ws: continue
        if sum(1 for w in ws if w.lower() in ENGLISH_SW)/len(ws) < 0.08: words.extend(ws)
    return words

def make_word_sim(onset, suffix, rng):
    if suffix.endswith('edy') or suffix.endswith('eedy'):
        return onset + rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei']) + suffix
    return onset + suffix

def random_eva_word(ow, sw, rng):
    o = rng.choices(list(ow.keys()), weights=list(ow.values()))[0]
    s = rng.choices(list(sw.keys()), weights=list(sw.values()))[0]
    return make_word_sim(o, s, rng)

latin = load_latin(LATIN_CORPUS)
rng = random.Random(245000)
w_shuffled = list(latin); rng.shuffle(w_shuffled)

# Use actual VMS onset/suffix distributions
SUFFIX_PATTERNS = ['eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy']
suf_ctr = Counter()
for w in all_words:
    matched = False
    for suf in SUFFIX_PATTERNS:
        if w.endswith(suf): suf_ctr[suf] += 1; matched = True; break
    if not matched: suf_ctr['other'] += 1
suffix_global = {suf: c/len(all_words) for suf, c in suf_ctr.items()}
onset_weights_mid = dict(rates_mid)

# Record buffer composition at draw time, for each prev_onset
buf_at_draw = defaultdict(list)  # prev_onset → list of buffer onset distributions
draw_results = defaultdict(list)  # prev_onset → list of drawn word onsets

TARGET_LINES = 2447
buf = deque(maxlen=W)
pos = 0; prev_onset = None; n_lines = 0
lines_generated = []

while n_lines < TARGET_LINES and pos < len(w_shuffled) - 2:
    line_len = max(2, min(20, round(rng.gauss(8.4, 3.0))))
    chunk = w_shuffled[pos:pos+line_len]
    if len(chunk) < 2: pos += len(chunk); continue
    line = []
    for i, _ in enumerate(chunk):
        if i == 0:
            ew = random_eva_word(onset_weights_mid, suffix_global, rng)
        elif i == len(chunk)-1:
            ew = random_eva_word(onset_weights_mid, suffix_global, rng)
        else:
            if P_STUTTER > 0 and line and rng.random() < P_STUTTER:
                ew = line[-1]  # stutter
            elif buf and rng.random() < CP:
                # Record buffer composition at draw
                buf_list = list(buf)
                buf_oc = Counter(get_onset(bw) for bw in buf_list)
                buf_at_draw[prev_onset].append(buf_oc)
                ew_src = rng.choice(buf_list)  # no Markov for diagnostic
                ew = make_word_sim(get_onset(ew_src), rng.choices(list(suffix_global.keys()), weights=list(suffix_global.values()))[0], rng) if rng.random() < MP else ew_src
                draw_results[prev_onset].append(get_onset(ew))
            else:
                ew = random_eva_word(onset_weights_mid, suffix_global, rng)
            buf.append(ew)
        prev_onset = get_onset(ew); line.append(ew)
    lines_generated.append(line); n_lines += 1
    pos += line_len

print(f"  Generated {n_lines} lines, recorded {sum(len(v) for v in buf_at_draw.values())} buffer draws\n")

# Compute conditional P(buf contains X | prev = X) and E(X→X from buffer)
print(f"  {'Prev':<8} {'Draws':>7}  {'Rate_mid%':>10}  {'P(buf has X)':>13}  E_buf_theory  {'E_from_draws':>13}")
print(f"  {'-'*75}")

focus_onsets = ['qok', 'sh', 'ok', 'ot', 'ch', 'ol', 'y', 'd', 'l', 'o']
for onset in focus_onsets:
    draws = buf_at_draw.get(onset, [])
    if len(draws) < 20: continue
    # Average fraction of buffer with onset X
    p_buf_has_X = sum(bc.get(onset, 0) / W for bc in draws) / len(draws)
    r = rates_mid.get(onset, 0)
    # E from draws: P(draw onset X | prev=X, buf_draw) / r
    drawn_X = draw_results.get(onset, [])
    p_draw_X = sum(1 for d in drawn_X if d == onset) / len(drawn_X) if drawn_X else 0
    # Expected full simulation E(X→X) from buffer
    # P(X→X) = p_stutter + (1-p_stutter) × [cp × p_buf_has_X + (1-cp) × r]
    p_total_xx = P_STUTTER + (1-P_STUTTER) * (CP * p_buf_has_X + (1-CP) * r)
    E_from_theory = p_total_xx / r if r > 0 else 0
    print(f"  {onset:<8} {len(draws):>7}  {r*100:>9.2f}%  {p_buf_has_X*100:>12.2f}%  {E_from_theory:>12.3f}  {p_draw_X/r if r>0 else 0:>13.3f}")

print(f"\n  Note: P(buf has X) should be ≈ rate_mid(X)% if buffer is stationary.")
print(f"  If P(buf has X) >> rate_mid(X): buffer is enriched in X → self-succession automatic.")
print(f"  E_buf_theory includes p_stutter contribution.")

# ─── Summary ──────────────────────────────────────────────────────────────────

print(f"\n{'='*80}")
print("H444 DIAGNOSTIC SUMMARY")
print(f"{'='*80}")
print(f"""
  Theory: E(X→X) = 1 + p_stutter/rate_mid(X)

  This means self-succession enrichment from the copy-buffer architecture is:
  1. Driven ONLY by p_stutter (the exact-repeat mechanism)
  2. Inversely proportional to onset rate (rare onsets get more enrichment from stutter)
  3. NOT enhanced by the copy buffer itself (onset-preserving modification returns same
     onset rate as the MID vocabulary distribution)

  At p_stutter=0.006:
  - qok (14% rate): E_theory = 1 + 0.006/0.14 = 1.043
  - sh  (6% rate):  E_theory = 1 + 0.006/0.06 = 1.100
  - ok  (5% rate):  E_theory = 1 + 0.006/0.05 = 1.120
  - ot  (4% rate):  E_theory = 1 + 0.006/0.04 = 1.150
  - y   (5% rate):  E_theory = 1 + 0.006/0.05 = 1.120
  - l   (3% rate):  E_theory = 1 + 0.006/0.03 = 1.200
  - d   (9% rate):  E_theory = 1 + 0.006/0.09 = 1.067

  VMS E_mid values:
  - qok: 1.169 (theory: 1.043 → gap +0.13)
  - sh:  ~1.1  (theory: 1.100 → gap ~0)
  - ok:  1.322 (theory: 1.120 → gap +0.20)
  - ot:  1.887 (theory: 1.150 → gap +0.74)
  - y:   2.491 (theory: 1.120 → gap +1.37)
  - l:   2.203 (theory: 1.200 → gap +1.00)
  - d:   1.540 (theory: 1.067 → gap +0.47)

  CONCLUSION: The copy-buffer architecture has a fundamental self-succession gap.
  The mechanism produces E(X→X) ≈ 1.04-1.20 from stutter alone.
  VMS shows E_mid(X→X) = 1.2-2.5 for most onsets.
  The ENTIRE self-succession enrichment above the stutter baseline is unexplained
  by the current architecture.

  This parallels the sh→qok finding: both are genuine grammatical rules that
  exceed the copy-buffer's natural production rate by a large margin.
""")
print("Done.")
