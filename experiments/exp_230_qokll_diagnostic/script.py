"""
exp_230: H430 — qok_ll Diagnostic

Motivation:
  exp_229 (Mode B, 14/18) produces qok_ll=0.764 (128.4% of VMS 0.595 — FAIL).
  The simulation uses VMS MID onset distribution (qok=14.19%) for MID words and
  VMS LL onset distribution (qok=7.62%) for LL words. The theoretical prediction:
  qok_ll = LL_qok / MID_qok = 7.62/14.19 = 0.537. But observed qok_ll=0.764.

  Discrepancy = 0.764 - 0.537 = 0.227 (42% of VMS qok_ll).

  This experiment adds detailed diagnostics to identify the root cause:
  (1) Measure actual MID qok rate in simulation output vs VMS MID onset (14.19%)
  (2) Measure actual LL qok rate vs VMS LL onset (7.62%)
  (3) Compute qok_ll from raw rates (not the ratio of enrichment ratios)
  (4) Test contribution of each mechanism (edy fresh-fallback, qok→ch Markov, stutter)
      by toggling them OFF individually to isolate which one causes the discrepancy

  Mechanism tests:
  - A: full exp_229 (all mechanisms active: p_qokch=0.12, p_stutter=0.009)
  - B: no Markov bias (p_qokch=0.00), all else same
  - C: no stutter (p_stutter=0.000), all else same
  - D: no edy fresh-fallback (return unchanged instead of fresh word), all else same
  - E: bare Mode B (no qok/stutter/edy mechanisms — like exp_221 baseline)

  N=20 each for mechanism isolation; N=30 for full diagnostic at best configuration.
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_DIAG  = 20
TARGET_LINES = 2447
WINDOW       = 20
SEED         = 230000
P_BLIND  = 0.30
P_LF     = 1.0
CP       = 0.55
MP       = 0.90

EVA_CHARS = list('acdehiklmnoqrsty')

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

def get_onset_len(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return len(prefix)
    return 0

def get_edy_suffix_len(w):
    if w.endswith('eedy'): return 4
    if w.endswith('edy'):  return 3
    return 0

def folio_base(folio):
    return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

def parse_vms_corpus():
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
            dialect = folio_dialect.get(fb, 'unknown')
            if dialect != 'B': continue
            lc_stripped = locus_code.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words: b_lines.append(words)
    return b_lines

def compute_vms_distributions(b_lines):
    all_words = [w for l in b_lines for w in l]
    lf_words  = [l[0]  for l in b_lines if l]
    ll_words  = [l[-1] for l in b_lines if len(l) > 1]
    mid_words = [w for l in b_lines for w in l[1:-1] if len(l) > 2]
    n = len(all_words)
    n_mid = len(mid_words)

    oc_all = Counter(get_onset(w) for w in all_words)
    oc_lf  = Counter(get_onset(w) for w in lf_words)
    oc_ll  = Counter(get_onset(w) for w in ll_words)
    oc_mid = Counter(get_onset(w) for w in mid_words)

    onset_global = {o: cnt/n for o, cnt in oc_all.items()}
    onset_lf     = {o: cnt/len(lf_words) for o, cnt in oc_lf.items()}
    onset_ll     = {o: cnt/len(ll_words) for o, cnt in oc_ll.items()}
    onset_mid    = {o: cnt/n_mid for o, cnt in oc_mid.items()} if n_mid else {}

    SUFFIX_PATTERNS = ['eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy']
    suf_ctr = Counter()
    for w in all_words:
        matched = False
        for suf in SUFFIX_PATTERNS:
            if w.endswith(suf):
                suf_ctr[suf] += 1; matched = True; break
        if not matched: suf_ctr['other'] += 1
    suffix_global = {suf: cnt/n for suf, cnt in suf_ctr.items()}

    am_r  = sum(1 for w in all_words if w.endswith('am')) / n
    ll_am = sum(1 for w in ll_words if w.endswith('am')) / len(ll_words)
    d_r   = oc_all.get('d', 0) / n
    ll_d  = oc_ll.get('d', 0) / len(ll_words)

    return {
        'onset_global': onset_global,
        'onset_lf': onset_lf,
        'onset_ll': onset_ll,
        'onset_mid': onset_mid,
        'suffix_global': suffix_global,
        'am_r': am_r, 'am_ll_target': ll_am/am_r,
        'd_r': d_r, 'd_ll_target': ll_d/d_r if d_r else 0,
        'n': n, 'n_lf': len(lf_words), 'n_ll': len(ll_words),
    }

def build_ll_onsets(onset_ll_vms, d_boost_weight):
    remaining_weight = 1.0 - d_boost_weight
    base = {o: v for o, v in onset_ll_vms.items() if o not in ('d', 'qok')}
    base_total = sum(base.values())
    if base_total > 0:
        normalized = {o: v/base_total * remaining_weight for o, v in base.items()}
    else:
        normalized = {}
    normalized['d'] = d_boost_weight
    return normalized

def make_word_sim(onset, suffix, rng):
    connector = rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei'])
    return onset + connector + suffix

def random_eva_word(onset_weights, suffix_weights, rng):
    onset  = rng.choices(list(onset_weights.keys()),  weights=list(onset_weights.values()))[0]
    suffix = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
    return make_word_sim(onset, suffix, rng)

def cipher_ll_blind(onset_weights, suffix_weights, ll_onsets, p_blind, rng):
    if rng.random() < p_blind:
        onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return make_word_sim(onset, 'am', rng)
    return random_eva_word(onset_weights, suffix_weights, rng)

def cipher_lf_vms(onset_weights, suffix_weights, onset_lf_vms, p_lf, rng):
    if rng.random() < p_lf:
        onset = rng.choices(list(onset_lf_vms.keys()), weights=list(onset_lf_vms.values()))[0]
        suffix = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
        return make_word_sim(onset, suffix, rng)
    return random_eva_word(onset_weights, suffix_weights, rng)

def timm_modify_edy_preserving_fresh_fallback(word, onset_weights, suffix_weights, rng):
    if not word: return word
    onset_len = get_onset_len(word)
    edy_len   = get_edy_suffix_len(word)
    mod_start = onset_len
    mod_end   = len(word) - edy_len
    if mod_start >= mod_end:
        return random_eva_word(onset_weights, suffix_weights, rng)
    op = rng.choice(['replace', 'insert', 'delete'])
    if op == 'replace':
        pos = rng.randint(mod_start, mod_end - 1)
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos+1:]
    elif op == 'insert':
        pos = rng.randint(mod_start, mod_end)
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos:]
    else:
        if mod_end - mod_start <= 1:
            pos = mod_start
            return word[:pos] + rng.choice(EVA_CHARS) + word[pos+1:]
        pos = rng.randint(mod_start, mod_end - 1)
        return word[:pos] + word[pos+1:]

def timm_modify_unchanged_fallback(word, rng):
    """edy-preserving modification with unchanged fallback (no fresh word)."""
    if not word: return word
    onset_len = get_onset_len(word)
    edy_len   = get_edy_suffix_len(word)
    mod_start = onset_len
    mod_end   = len(word) - edy_len
    if mod_start >= mod_end:
        return word  # unchanged — no fresh word
    op = rng.choice(['replace', 'insert', 'delete'])
    if op == 'replace':
        pos = rng.randint(mod_start, mod_end - 1)
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos+1:]
    elif op == 'insert':
        pos = rng.randint(mod_start, mod_end)
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos:]
    else:
        if mod_end - mod_start <= 1:
            pos = mod_start
            return word[:pos] + rng.choice(EVA_CHARS) + word[pos+1:]
        pos = rng.randint(mod_start, mod_end - 1)
        return word[:pos] + word[pos+1:]

def timm_modify_no_edy(word, onset_weights, suffix_weights, rng):
    """Onset-preserving only (no edy protection) — exp_221 baseline."""
    if not word: return word
    onset_len = get_onset_len(word)
    mod_start = onset_len
    mod_end   = len(word)
    if mod_start >= mod_end:
        return random_eva_word(onset_weights, suffix_weights, rng)
    op = rng.choice(['replace', 'insert', 'delete'])
    if op == 'replace':
        pos = rng.randint(mod_start, mod_end - 1)
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos+1:]
    elif op == 'insert':
        pos = rng.randint(mod_start, mod_end)
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos:]
    else:
        if mod_end - mod_start <= 1:
            pos = mod_start
            return word[:pos] + rng.choice(EVA_CHARS) + word[pos+1:]
        pos = rng.randint(mod_start, mod_end - 1)
        return word[:pos] + word[pos+1:]

def draw_from_buffer(buf, prev_onset, p_qokch, rng):
    buf_list = list(buf)
    if prev_onset == 'qok' and p_qokch > 0 and rng.random() < p_qokch:
        ch_words = [w for w in buf_list if get_onset(w) == 'ch']
        if ch_words:
            return rng.choice(ch_words)
    return rng.choice(buf_list)

def run_sim(latin_words, onset_weights, suffix_weights, ll_onsets, onset_lf_vms,
            cp, mp, p_qokch, p_stutter,
            use_edy_fresh=True, use_edy_at_all=True,
            rng=None):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    prev_onset = None
    prev_word  = None

    # Detailed diagnostic counters
    mid_qok_count = 0; mid_total = 0
    ll_qok_count  = 0; ll_total  = 0
    lf_qok_count  = 0; lf_total  = 0

    while len(lines) < TARGET_LINES and pos < len(w)-2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                ew = cipher_lf_vms(onset_weights, suffix_weights, onset_lf_vms, P_LF, rng)
                lf_qok_count += (get_onset(ew) == 'qok'); lf_total += 1
            elif i == len(chunk)-1:
                ew = cipher_ll_blind(onset_weights, suffix_weights, ll_onsets, P_BLIND, rng)
                ll_qok_count += (get_onset(ew) == 'qok'); ll_total += 1
            else:
                if prev_word is not None and p_stutter > 0 and rng.random() < p_stutter:
                    ew = prev_word
                elif buf and rng.random() < cp:
                    src = draw_from_buffer(buf, prev_onset, p_qokch, rng)
                    if rng.random() < mp:
                        if use_edy_at_all:
                            if use_edy_fresh:
                                ew = timm_modify_edy_preserving_fresh_fallback(src, onset_weights, suffix_weights, rng)
                            else:
                                ew = timm_modify_unchanged_fallback(src, rng)
                        else:
                            ew = timm_modify_no_edy(src, onset_weights, suffix_weights, rng)
                    else:
                        ew = src
                else:
                    ew = random_eva_word(onset_weights, suffix_weights, rng)
                buf.append(ew)
                mid_qok_count += (get_onset(ew) == 'qok'); mid_total += 1
            prev_onset = get_onset(ew)
            prev_word  = ew
            line.append(ew)
        lines.append(line); pos += n

    diag = {
        'mid_qok': mid_qok_count / mid_total if mid_total else 0,
        'll_qok':  ll_qok_count  / ll_total  if ll_total  else 0,
        'lf_qok':  lf_qok_count  / lf_total  if lf_total  else 0,
    }
    return lines[:TARGET_LINES], diag

def compute_qok_ll(lines):
    aw  = [w for l in lines for w in l]
    n   = len(aw)
    lf  = [l[0]  for l in lines if l]
    ll  = [l[-1] for l in lines if len(l) > 1]
    oc_all = Counter(get_onset(w) for w in aw)
    oc_ll  = Counter(get_onset(w) for w in ll)
    n_ll = len(ll)
    def enr(onset, ctr_slot, n_slot, ctr_all, n_all):
        s = ctr_slot.get(onset, 0)/n_slot if n_slot else 0
        g = ctr_all.get(onset, 0)/n_all if n_all else 0
        return s/g if g>0 else 0
    return enr('qok', oc_ll, n_ll, oc_all, n), oc_all.get('qok',0)/n

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

# ─── Main ─────────────────────────────────────────────────────────────────────

print("Parsing VMS B-dialect corpus...")
vms_b_lines = parse_vms_corpus()
vms = compute_vms_distributions(vms_b_lines)
print(f"  VMS B: {len(vms_b_lines)} lines, {vms['n']} words")

d_global    = vms['onset_global'].get('d', 0)
d_ll_target = vms['d_ll_target']
d_boost     = d_global * (d_ll_target - (1-P_BLIND)) / P_BLIND
ll_onsets   = build_ll_onsets(vms['onset_ll'], d_boost)
onset_lf_vms = dict(vms['onset_lf'])
suffix_weights = dict(vms['suffix_global'])
onset_weights_mid = dict(vms['onset_mid'])

# Reference values
vms_mid_qok = vms['onset_mid'].get('qok', 0)
vms_ll_qok  = vms['onset_ll'].get('qok', 0)
vms_global_qok = vms['onset_global'].get('qok', 0)
pred_qok_ll = vms_ll_qok / vms_mid_qok if vms_mid_qok else 0
vms_qok_ll_actual = vms['onset_ll'].get('qok',0) / vms['onset_global'].get('qok',0.001)

print(f"\nVMS qok rates:")
print(f"  VMS MID qok = {vms_mid_qok*100:.2f}%")
print(f"  VMS LL  qok = {vms_ll_qok*100:.2f}%")
print(f"  VMS global qok = {vms_global_qok*100:.2f}%")
print(f"  Theoretical qok_ll (LL/MID) = {pred_qok_ll:.3f}")
print(f"  Actual VMS qok_ll (LL/global) = {vms_qok_ll_actual:.3f}")
print(f"  NOTE: metric qok_ll = LL_qok_rate / GLOBAL_qok_rate (not LL/MID)")
print()

print("Loading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} Latin words loaded.")
print()

# ─── Mechanism Isolation Tests ─────────────────────────────────────────────────

configs = [
    ('A: Full exp_229 (all mechanisms)',    dict(p_qokch=0.12, p_stutter=0.009, use_edy_fresh=True,  use_edy_at_all=True)),
    ('B: No Markov (p_qokch=0.00)',         dict(p_qokch=0.00, p_stutter=0.009, use_edy_fresh=True,  use_edy_at_all=True)),
    ('C: No Stutter (p_stutter=0.000)',     dict(p_qokch=0.12, p_stutter=0.000, use_edy_fresh=True,  use_edy_at_all=True)),
    ('D: No edy fresh (unchanged fallback)',dict(p_qokch=0.12, p_stutter=0.009, use_edy_fresh=False, use_edy_at_all=True)),
    ('E: No edy at all (exp_221 baseline)', dict(p_qokch=0.00, p_stutter=0.000, use_edy_fresh=True,  use_edy_at_all=False)),
]

print(f"{'='*105}")
print(f"MECHANISM ISOLATION: qok_ll and qok rates in MID vs LL, N={N_DIAG} each")
print(f"VMS reference: qok_ll=0.595, VMS global qok={vms_global_qok*100:.2f}%")
print(f"               VMS LL qok={vms_ll_qok*100:.2f}%,  VMS MID qok={vms_mid_qok*100:.2f}%")
print(f"Theoretical qok_ll = LL_rate / global_rate = {vms_ll_qok:.4f}/{vms_global_qok:.4f} = {vms_ll_qok/vms_global_qok:.3f}")
print(f"{'='*105}")
print(f"  {'Config':<40} {'qok_ll':>8} {'%VMS':>7} {'MID_qok':>9} {'LL_qok':>8} {'Global_qok':>11} {'Pred_qokll':>11}")
print(f"  {'-'*98}")

for name, cfg in configs:
    qokll_vals = []; mid_qok_vals = []; ll_qok_vals = []; global_qok_vals = []
    for i in range(N_DIAG):
        rng = random.Random(SEED + i)
        lines, diag = run_sim(latin, onset_weights_mid, suffix_weights, ll_onsets, onset_lf_vms,
                              CP, MP, cfg['p_qokch'], cfg['p_stutter'],
                              cfg['use_edy_fresh'], cfg['use_edy_at_all'], rng)
        qokll, gqok = compute_qok_ll(lines)
        qokll_vals.append(qokll)
        mid_qok_vals.append(diag['mid_qok'])
        ll_qok_vals.append(diag['ll_qok'])
        global_qok_vals.append(gqok)

    qokll_m = sum(qokll_vals)/len(qokll_vals)
    mid_m   = sum(mid_qok_vals)/len(mid_qok_vals)
    ll_m    = sum(ll_qok_vals)/len(ll_qok_vals)
    glob_m  = sum(global_qok_vals)/len(global_qok_vals)
    pred    = ll_m / glob_m if glob_m else 0
    pct     = qokll_m/0.595*100
    print(f"  {name:<40} {qokll_m:>8.3f} {pct:>6.1f}%  {mid_m*100:>7.2f}%  {ll_m*100:>6.2f}%  {glob_m*100:>9.2f}%  {pred:>11.3f}")

print()
print("Key: qok_ll = LL_qok_rate / GLOBAL_qok_rate; Pred_qokll = LL_qok / Global_qok (should match qok_ll)")
print("     MID_qok: actual qok rate in MID output; LL_qok: actual qok rate in LL output")
print()
print(f"VMS targets: qok_ll=0.595, global_qok={vms_global_qok*100:.2f}%")
print(f"             LL_qok={vms_ll_qok*100:.2f}%, MID_qok={vms_mid_qok*100:.2f}%")
print()
print("Diagnostic conclusion:")
print("  If Global_qok in sim >> VMS global_qok: qok is overproduced globally → qok_ll inflated (LL=VMS, global too high)")
print("  If LL_qok in sim >> VMS LL_qok: qok overproduced at LL → qok_ll inflated")
print("  If MID_qok in sim << VMS MID_qok: qok underproduced at MID → global_qok lower → qok_ll inflated")
