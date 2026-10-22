"""
exp_223: H409 — Corpus Split Stability Check

Motivation:
  exp_221's Mode B architecture (cp=0.55, mp=0.90, p_blind=0.30) achieves 11/18 PASS
  on the full VMS B-dialect corpus. But the parameters were selected by reference to
  VMS target metrics computed from the FULL B-dialect corpus. This raises the question:
  are these metrics (am_ll=6.550, y_lf=3.324, ss_mean=1.164, etc.) stable properties
  of the VMS B-dialect system, or corpus-level variance that happens to match the model?

H409 question (adapted to 18-metric battery):
  Split B-dialect corpus into two halves by folio number:
    - Half A: odd-numbered folios (f1, f3, f5, ...)
    - Half B: even-numbered folios (f2, f4, f6, ...)
  For each half:
    (1) Compute VMS target metrics from that half only
    (2) Run exp_221's fixed configuration (cp=0.55, mp=0.90, p_blind=0.30) with that
        half's VMS distributions (onset_mid, onset_lf, onset_ll, suffix_global, etc.)
    (3) Evaluate the 18-metric battery against that half's VMS targets

  Expected outcome:
    - STABLE: VMS target metrics agree across halves (within ±10% each); same or similar
      pass counts in each half. The Mode B architecture is capturing corpus-level structure.
    - UNSTABLE: VMS target metrics diverge significantly across halves; pass counts differ.
      The 11/18 result may be overfitting to full-corpus averaging.

  Additional check: parameter sensitivity
    - At the full-corpus calibration (cp=0.55, mp=0.90), what is the pass count when
      evaluated against each HALF's VMS targets (not full-corpus targets)?
    - This tests whether the architecture's pass count depends on which corpus half
      is used as the evaluation target.

Architecture: identical to exp_221 (Mode B best config)
  - p_blind=0.30, p_lf=1.0, cp=0.55, mp=0.90
  - onset_weights = HALF-specific VMS MID onset distribution
  - VMS LF, LL onset distributions from that half
  - All suffix distributions: VMS GLOBAL (same as exp_221)
  - N=20 sims per configuration (adequate for stability check)
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SIMS       = 20
TARGET_LINES = 2447
WINDOW       = 20
SEED         = 223000
P_BLIND = 0.30
P_LF    = 1.0
CP      = 0.55
MP      = 0.90

EVA_CHARS = list('acdehiklmnoqrsty')
SUFFIX_PATTERNS = ['eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy']

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

def folio_base(folio):
    return re.sub(r'[rv]$', '', folio)

def folio_number(fb):
    """Extract numeric part of folio base (e.g., 'f1' -> 1, 'f10' -> 10)."""
    m = re.match(r'[a-zA-Z]*(\d+)', fb)
    return int(m.group(1)) if m else 0

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

    all_b_lines = []
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
            if words:
                fn = folio_number(fb)
                all_b_lines.append((fn, words))

    return all_b_lines

def compute_vms_distributions(b_lines_with_folio, split_name='ALL'):
    """b_lines_with_folio is list of (folio_num, words_list)."""
    b_lines = [words for _, words in b_lines_with_folio]
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

    # Compute VMS reference values for this split
    vms_am_lf_enr = (sum(1 for w in lf_words if w.endswith('am'))/len(lf_words)) / am_r if am_r else 0
    vms_am_mid_enr = (sum(1 for w in mid_words if w.endswith('am'))/n_mid) / am_r if (n_mid and am_r) else 0
    vms_edy_rate = sum(suf_ctr.get(s, 0) for s in ['edy','eedy']) / n

    # Compute ss_mean from VMS corpus
    bg_all = Counter()
    all_seq = [get_onset(w) for l in b_lines for w in l]
    for i in range(len(all_seq)-1): bg_all[(all_seq[i], all_seq[i+1])] += 1
    tb = len(all_seq)-1
    def vms_ss(o):
        b = oc_all.get(o, 0)/n
        return bg_all.get((o,o),0)/(tb*b*b) if b>0 else 1.0
    vms_ss_mean = (vms_ss('qok')+vms_ss('ok')+vms_ss('ch'))/3
    vms_adj = sum(1 for i in range(tb) if all_seq[i] == all_seq[i+1] and
                  [w for l in b_lines for w in l][i] == [w for l in b_lines for w in l][i+1]) / tb

    # Compute qok_ch
    qok_r = oc_all.get('qok', 0)/n
    ch_r = oc_all.get('ch', 0)/n
    vms_qok_ch = bg_all.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r else 0

    # word len
    vms_word_len = sum(len(w) for w in all_words)/n

    print(f"  [{split_name}] {len(b_lines)} lines, {n} words, {len(set(fn for fn, _ in b_lines_with_folio))} folios")
    print(f"    am_ll_target={ll_am/am_r:.3f}, y_lf={onset_lf.get('y',0)/onset_global.get('y',0.001):.3f}, "
          f"ss_mean={vms_ss_mean:.3f}, am_lf_enr={vms_am_lf_enr:.3f}, edy_rate={vms_edy_rate:.3f}")
    print(f"    d_ll_target={ll_d/d_r:.3f} (d_r={d_r*100:.2f}%)")

    return {
        'onset_global': onset_global, 'onset_lf': onset_lf, 'onset_ll': onset_ll, 'onset_mid': onset_mid,
        'suffix_global': suffix_global,
        'am_r': am_r, 'am_ll_target': ll_am/am_r,
        'd_r': d_r, 'd_ll_target': ll_d/d_r if d_r else 0,
        'n': n, 'n_lf': len(lf_words), 'n_ll': len(ll_words),
        'vms_am_lf_enr': vms_am_lf_enr, 'vms_am_mid_enr': vms_am_mid_enr,
        'vms_edy_rate': vms_edy_rate, 'vms_ss_mean': vms_ss_mean,
        'vms_adj': vms_adj, 'vms_qok_ch': vms_qok_ch, 'vms_word_len': vms_word_len,
        'b_lines': b_lines,
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

def timm_modify_onset_preserving(word, rng):
    if not word: return word
    onset_len = get_onset_len(word)
    suffix_start = onset_len
    if suffix_start >= len(word): return word
    op = rng.choice(['replace', 'insert', 'delete'])
    if op == 'replace':
        pos = rng.randint(suffix_start, len(word) - 1)
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos+1:]
    elif op == 'insert':
        pos = rng.randint(suffix_start, len(word))
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos:]
    else:
        if len(word) <= suffix_start + 1:
            if suffix_start < len(word):
                return word[:suffix_start] + rng.choice(EVA_CHARS) + word[suffix_start+1:]
            return word
        pos = rng.randint(suffix_start, len(word) - 1)
        return word[:pos] + word[pos+1:]

def run_sim(latin_words, onset_weights, suffix_weights, ll_onsets, onset_lf_vms, cp, mp, rng):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    while len(lines) < TARGET_LINES and pos < len(w)-2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                ew = cipher_lf_vms(onset_weights, suffix_weights, onset_lf_vms, P_LF, rng)
            elif i == len(chunk)-1:
                ew = cipher_ll_blind(onset_weights, suffix_weights, ll_onsets, P_BLIND, rng)
            else:
                if buf and rng.random() < cp:
                    ew = timm_modify_onset_preserving(rng.choice(list(buf)), rng) if rng.random() < mp else rng.choice(list(buf))
                else:
                    ew = random_eva_word(onset_weights, suffix_weights, rng)
                buf.append(ew)
            line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

def compute_metrics(lines):
    aw  = [w for l in lines for w in l]
    n   = len(aw)
    if n < 100: return None
    lf  = [l[0]  for l in lines if l]
    ll  = [l[-1] for l in lines if len(l) > 1]
    mid = [w for l in lines for w in l[1:-1] if len(l) > 2]
    oc_all = Counter(get_onset(w) for w in aw)
    oc_lf  = Counter(get_onset(w) for w in lf)
    oc_ll  = Counter(get_onset(w) for w in ll)
    n_lf, n_ll, n_mid = len(lf), len(ll), len(mid)

    def enr(onset, ctr_slot, n_slot, ctr_all, n_all):
        s = ctr_slot.get(onset, 0)/n_slot if n_slot else 0
        g = ctr_all.get(onset, 0)/n_all if n_all else 0
        return s/g if g>0 else 0

    am_r   = sum(1 for w in aw if w.endswith('am')) / n
    ll_am  = sum(1 for w in ll if w.endswith('am')) / n_ll if n_ll else 0
    am_ll  = ll_am / am_r if am_r else 0
    d_ll   = enr('d', oc_ll, n_ll, oc_all, n)
    y_lf   = enr('y', oc_lf, n_lf, oc_all, n)

    tb = n-1
    bg = Counter((get_onset(aw[i]), get_onset(aw[i+1])) for i in range(tb))
    def ss(o):
        b = oc_all.get(o, 0)/n
        return bg.get((o,o),0)/(tb*b*b) if b>0 else 1.0
    ss_mean = (ss('qok')+ss('ok')+ss('ch'))/3
    adj = sum(1 for i in range(tb) if aw[i]==aw[i+1])/max(1,tb)

    qok_lf = enr('qok', oc_lf, n_lf, oc_all, n)
    d_lf   = enr('d',   oc_lf, n_lf, oc_all, n)
    s_lf   = enr('s',   oc_lf, n_lf, oc_all, n)
    ch_ll  = enr('ch',  oc_ll, n_ll, oc_all, n)
    ok_ll  = enr('ok',  oc_ll, n_ll, oc_all, n)
    qok_ll = enr('qok', oc_ll, n_ll, oc_all, n)
    ss_d   = ss('d');  ss_y = ss('y')
    am_lf_enr  = (sum(1 for w in lf if w.endswith('am'))/n_lf) / am_r if am_r else 0
    am_mid_enr = (sum(1 for w in mid if w.endswith('am'))/n_mid / am_r) if (n_mid and am_r) else 0
    edy_rate   = sum(1 for w in aw if w.endswith('edy'))/n
    word_len   = sum(len(w) for w in aw)/n
    qok_r  = oc_all.get('qok', 0)/n
    ch_r   = oc_all.get('ch', 0)/n
    qok_ch = bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r else 0

    return dict(am_ll=am_ll, d_ll=d_ll, y_lf=y_lf, ss_mean=ss_mean, adj_rate=adj,
                qok_lf=qok_lf, d_lf=d_lf, s_lf=s_lf, ch_ll=ch_ll, ok_ll=ok_ll,
                qok_ll=qok_ll, ss_d=ss_d, ss_y=ss_y, am_lf_enr=am_lf_enr,
                am_mid_enr=am_mid_enr, edy_rate=edy_rate, word_len_mean=word_len,
                qok_ch=qok_ch)

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

# ─── Main ────────────────────────────────────────────────────────────────────

print("Parsing VMS B-dialect corpus with folio numbers...")
all_b_lines = parse_vms_corpus()
print(f"  Total B-dialect lines: {len(all_b_lines)}")

# Split by folio parity
odd_lines  = [(fn, words) for fn, words in all_b_lines if fn % 2 == 1]
even_lines = [(fn, words) for fn, words in all_b_lines if fn % 2 == 0]

print(f"\n  Split: {len(odd_lines)} lines in odd-folio half, {len(even_lines)} lines in even-folio half")
print()

print("Computing VMS distributions for each split:")
vms_full = compute_vms_distributions(all_b_lines, 'FULL')
vms_odd  = compute_vms_distributions(odd_lines, 'ODD-FOLIO')
vms_even = compute_vms_distributions(even_lines, 'EVEN-FOLIO')

print()
print("VMS target metric comparison across splits:")
print(f"  {'Metric':<20} {'FULL':>8} {'ODD':>8} {'EVEN':>8}  {'ODD/FULL':>9}  {'EVEN/FULL':>9}")
print(f"  {'-'*75}")
key_metrics = [
    ('am_ll_target', 'am_ll'),
    ('d_ll_target', 'd_ll'),
]
# Print some key metrics
for key, label in key_metrics:
    f_val = vms_full.get(key, 0)
    o_val = vms_odd.get(key, 0)
    e_val = vms_even.get(key, 0)
    print(f"  {label:<20} {f_val:>8.3f} {o_val:>8.3f} {e_val:>8.3f}  {o_val/f_val:>8.1%}  {e_val/f_val:>8.1%}")

for onset_name in ['y', 'd', 's', 'qok', 'ch', 'ok']:
    label = f'y_lf_enr ({onset_name})' if onset_name == 'y' else f'{onset_name}_lf' if onset_name in ['d','s','qok'] else f'{onset_name}_ll'
    if onset_name in ['y', 'd', 's', 'qok']:
        # LF enrichment
        f_val = vms_full['onset_lf'].get(onset_name,0) / vms_full['onset_global'].get(onset_name,0.001)
        o_val = vms_odd['onset_lf'].get(onset_name,0) / vms_odd['onset_global'].get(onset_name,0.001)
        e_val = vms_even['onset_lf'].get(onset_name,0) / vms_even['onset_global'].get(onset_name,0.001)
    else:
        # LL enrichment
        f_val = vms_full['onset_ll'].get(onset_name,0) / vms_full['onset_global'].get(onset_name,0.001)
        o_val = vms_odd['onset_ll'].get(onset_name,0) / vms_odd['onset_global'].get(onset_name,0.001)
        e_val = vms_even['onset_ll'].get(onset_name,0) / vms_even['onset_global'].get(onset_name,0.001)
    print(f"  {label:<20} {f_val:>8.3f} {o_val:>8.3f} {e_val:>8.3f}  {o_val/f_val:>8.1%}  {e_val/f_val:>8.1%}")

for key, label in [('vms_ss_mean','ss_mean'), ('vms_edy_rate','edy_rate'), ('vms_am_lf_enr','am_lf_enr'), ('vms_word_len','word_len')]:
    f_val = vms_full.get(key, 0)
    o_val = vms_odd.get(key, 0)
    e_val = vms_even.get(key, 0)
    print(f"  {label:<20} {f_val:>8.3f} {o_val:>8.3f} {e_val:>8.3f}  {o_val/f_val:>8.1%}  {e_val/f_val:>8.1%}")
print()

print("Loading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} Latin words loaded.")
print()

def run_split_eval(vms, split_name, seed_offset):
    """Run Mode B simulation and evaluate against this split's VMS targets."""
    d_global    = vms['onset_global'].get('d', 0)
    d_ll_target = vms['d_ll_target']
    d_boost     = d_global * (d_ll_target - (1-P_BLIND)) / P_BLIND
    ll_onsets   = build_ll_onsets(vms['onset_ll'], d_boost)
    onset_lf_vms = dict(vms['onset_lf'])
    onset_weights = dict(vms['onset_mid'])
    suffix_weights = dict(vms['suffix_global'])

    VMS_REF = {
        'am_ll':       vms['am_ll_target'],
        'd_ll':        vms['d_ll_target'],
        'y_lf':        vms['onset_lf'].get('y',0) / vms['onset_global'].get('y',0.001),
        'ss_mean':     vms.get('vms_ss_mean', 1.164),
        'adj_rate':    0.009,
        'qok_lf':      vms['onset_lf'].get('qok',0) / vms['onset_global'].get('qok',0.001),
        'd_lf':        vms['onset_lf'].get('d',0) / vms['onset_global'].get('d',0.001),
        's_lf':        vms['onset_lf'].get('s',0) / vms['onset_global'].get('s',0.001),
        'ch_ll':       vms['onset_ll'].get('ch',0) / vms['onset_global'].get('ch',0.001),
        'ok_ll':       vms['onset_ll'].get('ok',0) / vms['onset_global'].get('ok',0.001),
        'qok_ll':      vms['onset_ll'].get('qok',0) / vms['onset_global'].get('qok',0.001),
        'ss_d':        1.291, 'ss_y': 1.955,
        'am_lf_enr':   vms.get('vms_am_lf_enr', 0.122),
        'am_mid_enr':  vms.get('vms_am_mid_enr', 0.195),
        'edy_rate':    vms.get('vms_edy_rate', 0.194),
        'word_len_mean': vms.get('vms_word_len', 5.400),
        'qok_ch':      vms.get('vms_qok_ch', 1.267),
    }

    all_metrics = []
    for i in range(N_SIMS):
        rng = random.Random(SEED + seed_offset + i)
        lines = run_sim(latin, onset_weights, suffix_weights, ll_onsets, onset_lf_vms, CP, MP, rng)
        m = compute_metrics(lines)
        if m: all_metrics.append(m)

    def agg(key):
        vals = sorted(x[key] for x in all_metrics)
        mean = sum(vals)/len(vals)
        return mean

    PASS_TOL = 0.20
    pass_count = 0; total = 0
    results = {}
    for key in VMS_REF:
        vms_val = VMS_REF[key]
        sim_mean = agg(key)
        pct = sim_mean/vms_val*100 if abs(vms_val)>1e-6 else float('inf')
        pass_f = abs(sim_mean-vms_val)/abs(vms_val) <= PASS_TOL if abs(vms_val)>1e-6 else abs(sim_mean)<0.002
        results[key] = (vms_val, sim_mean, pct, pass_f)
        total += 1
        if pass_f: pass_count += 1

    return results, pass_count, total, VMS_REF

METRIC_ORDER = [
    'am_ll', 'd_ll', 'y_lf', 'ss_mean', 'adj_rate',
    'qok_lf', 'd_lf', 's_lf', 'ch_ll', 'ok_ll', 'qok_ll',
    'ss_d', 'ss_y', 'am_lf_enr', 'am_mid_enr', 'edy_rate', 'word_len_mean', 'qok_ch'
]

print("=" * 110)
print("Running Mode B simulation on each corpus split...")
print(f"  Config: cp={CP}, mp={MP}, p_blind={P_BLIND}, N={N_SIMS} per split")
print("=" * 110)

# Full corpus
print("\nFULL corpus simulation...")
res_full, pc_full, tot_full, _ = run_split_eval(vms_full, 'FULL', 0)

# Odd-folio corpus
print("ODD-folio corpus simulation...")
res_odd, pc_odd, tot_odd, _ = run_split_eval(vms_odd, 'ODD', 1000)

# Even-folio corpus
print("EVEN-folio corpus simulation...")
res_even, pc_even, tot_even, _ = run_split_eval(vms_even, 'EVEN', 2000)

print(f"\nCompleted all three splits.")
print()
print("=" * 110)
print(f"RESULTS: 18-METRIC BATTERY BY CORPUS SPLIT (Mode B, cp={CP}, mp={MP})")
print("=" * 110)
print(f"  {'Metric':<16} {'VMS_F':>7} {'SIM_F':>7} {'%_F':>6} {'P?':>3}  |  {'VMS_O':>7} {'SIM_O':>7} {'%_O':>6} {'P?':>3}  |  {'VMS_E':>7} {'SIM_E':>7} {'%_E':>6} {'P?':>3}")
print(f"  {'-'*105}")

for key in METRIC_ORDER:
    vf, sf, pctf, passf = res_full.get(key, (0,0,0,False))
    vo, so, pcto, passo = res_odd.get(key, (0,0,0,False))
    ve, se, pcte, passe = res_even.get(key, (0,0,0,False))
    pf = 'P' if passf else 'F'
    po = 'P' if passo else 'F'
    pe = 'P' if passe else 'F'
    print(f"  {key:<16} {vf:>7.3f} {sf:>7.3f} {pctf:>5.1f}% {pf:>3}  |  {vo:>7.3f} {so:>7.3f} {pcto:>5.1f}% {po:>3}  |  {ve:>7.3f} {se:>7.3f} {pcte:>5.1f}% {pe:>3}")

print()
print(f"  Pass count: FULL={pc_full}/{tot_full}  |  ODD={pc_odd}/{tot_odd}  |  EVEN={pc_even}/{tot_even}")
print()

# VMS target metric stability summary
print("=" * 110)
print("VMS TARGET METRIC STABILITY ACROSS SPLITS")
print("=" * 110)
print(f"  {'Metric':<20} {'FULL':>8} {'ODD':>8} {'EVEN':>8}  {'Stable?'}")
print(f"  {'-'*65}")
stability_metrics = [
    ('am_ll', res_full['am_ll'][0], res_odd['am_ll'][0], res_even['am_ll'][0]),
    ('y_lf', res_full['y_lf'][0], res_odd['y_lf'][0], res_even['y_lf'][0]),
    ('d_ll', res_full['d_ll'][0], res_odd['d_ll'][0], res_even['d_ll'][0]),
    ('ss_mean', res_full['ss_mean'][0], res_odd['ss_mean'][0], res_even['ss_mean'][0]),
    ('qok_lf', res_full['qok_lf'][0], res_odd['qok_lf'][0], res_even['qok_lf'][0]),
    ('d_lf', res_full['d_lf'][0], res_odd['d_lf'][0], res_even['d_lf'][0]),
    ('s_lf', res_full['s_lf'][0], res_odd['s_lf'][0], res_even['s_lf'][0]),
    ('ch_ll', res_full['ch_ll'][0], res_odd['ch_ll'][0], res_even['ch_ll'][0]),
    ('ok_ll', res_full['ok_ll'][0], res_odd['ok_ll'][0], res_even['ok_ll'][0]),
    ('qok_ll', res_full['qok_ll'][0], res_odd['qok_ll'][0], res_even['qok_ll'][0]),
    ('edy_rate', res_full['edy_rate'][0], res_odd['edy_rate'][0], res_even['edy_rate'][0]),
    ('am_lf_enr', res_full['am_lf_enr'][0], res_odd['am_lf_enr'][0], res_even['am_lf_enr'][0]),
]
for metric, fv, ov, ev in stability_metrics:
    stable = (abs(ov-fv)/max(abs(fv),1e-6) <= 0.20 and abs(ev-fv)/max(abs(fv),1e-6) <= 0.20)
    stable_str = "STABLE" if stable else "UNSTABLE!"
    print(f"  {metric:<20} {fv:>8.3f} {ov:>8.3f} {ev:>8.3f}  {stable_str}")
print()
print(f"  Note: 'STABLE' means both halves within ±20% of full corpus VMS target value")
