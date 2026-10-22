"""
exp_256: H459 — B-Dialect ot→ot Recheck After 'Other' Onset Bug Fix

Question: Does the B-dialect ot→ot gap (Δ=-0.477 from exp_246, VMS=1.887 vs Sim=1.410)
persist after fixing the 'other' onset bug? B-dialect has 5.99% 'other' contamination
in onset_mid — same bug as A-dialect (6.48%), where fixing eliminated the gap entirely.

Design:
- Use exp_249 12-mechanism B-dialect architecture (WITHOUT p_ot_ot — testing baseline gap)
- Apply filter_other fix: remove 'other' from onset_mid, onset_lf, onset_ll, renormalize
- Run N=15 simulations
- Report: ot→ot MID E2 (VMS=1.887), ot onset rate (VMS MID ~7.21% from exp_245), 19-metric battery
- Compare to contaminated baseline: if gap disappears → p_ot_ot=0.10 was artifact correction
- Also test WITH p_ot_ot=0.10 to see if it now over-produces ot→ot

Base architecture: exp_249 params (p_qokch=0.12, p_chqok=0.12)
Without p_ot_ot (testing gap magnitude)
With p_ot_ot=0.10 (testing if it now over-produces)
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SIM = 15; WINDOW = 20; SEED = 256000

# exp_249 B-dialect parameters (12 mechanisms)
P_BLIND = 0.115; P_LF = 1.0; CP = 0.55; MP = 0.90
P_QOKCH = 0.12; P_CHQOK = 0.12; P_STUTTER = 0.006
R_LF = 0.12; R_MID = 0.25; MU_LEN = 8.4; SIGMA_LEN = 3.0

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
def folio_base(folio): return re.sub(r'[rv]$', '', folio)
def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

def filter_other(dist):
    """Remove 'other' key and renormalize."""
    filtered = {k: v for k, v in dist.items() if k != 'other'}
    total = sum(filtered.values())
    return {k: v/total for k, v in filtered.items()} if total > 0 else filtered

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

SUFFIX_PATTERNS = ['eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy']

def build_suffix(words):
    n = len(words); suf_ctr = Counter()
    for w in words:
        matched = False
        for suf in SUFFIX_PATTERNS:
            if w.endswith(suf): suf_ctr[suf] += 1; matched = True; break
        if not matched: suf_ctr['other'] += 1
    return {suf: cnt/n for suf, cnt in suf_ctr.items()}

def build_onset_dist(words):
    n = max(1, len(words))
    return {o: cnt/n for o, cnt in Counter(get_onset(w) for w in words).items()}

def make_suppressed_suffix(suffix_global, r_am):
    am_w = suffix_global.get('am', 0.0); new_am = am_w * r_am; delta = am_w - new_am
    non_am = 1.0 - am_w
    return {s: (new_am if s=='am' else w + w/non_am*delta) for s, w in suffix_global.items()} \
           if non_am > 0 else dict(suffix_global)

def build_ll_onsets(onset_ll, d_boost_weight):
    rem = 1.0 - d_boost_weight
    base = {o: v for o, v in onset_ll.items() if o != 'd'}
    bt = sum(base.values())
    norm = {o: v/bt*rem for o, v in base.items()} if bt > 0 else {}
    norm['d'] = d_boost_weight; return norm

def compute_d_boost(d_global, d_ll_target, d_ll_non_blind, p_blind):
    return d_global * (d_ll_target - (1-p_blind) * d_ll_non_blind) / p_blind

def make_word_sim(onset, suffix, rng):
    if suffix.endswith('edy') or suffix.endswith('eedy'):
        return onset + rng.choice(['a','ai','o','oi','e','ei']) + suffix
    return onset + suffix

def random_eva_word(onset_w, suffix_w, rng):
    o = rng.choices(list(onset_w.keys()), weights=list(onset_w.values()))[0]
    s = rng.choices(list(suffix_w.keys()), weights=list(suffix_w.values()))[0]
    return make_word_sim(o, s, rng)

def cipher_ll(onset_w, suffix_g, ll_onsets, onset_ll, p_blind, rng):
    if rng.random() < p_blind:
        o = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return o + 'am'
    o = rng.choices(list(onset_ll.keys()), weights=list(onset_ll.values()))[0]
    s = rng.choices(list(suffix_g.keys()), weights=list(suffix_g.values()))[0]
    return make_word_sim(o, s, rng)

def cipher_lf(onset_w, suffix_lf, onset_lf, p_lf, rng):
    if rng.random() < p_lf:
        o = rng.choices(list(onset_lf.keys()), weights=list(onset_lf.values()))[0]
        s = rng.choices(list(suffix_lf.keys()), weights=list(suffix_lf.values()))[0]
        return make_word_sim(o, s, rng)
    return random_eva_word(onset_w, suffix_lf, rng)

def timm_modify(word, onset_w, suffix_mid, rng):
    if not word: return word
    ol = get_onset_len(word); el = get_edy_suffix_len(word)
    ms = ol; me = len(word) - el
    if ms >= me: return random_eva_word(onset_w, suffix_mid, rng)
    op = rng.choice(['replace','insert','delete'])
    if op == 'replace':
        pos = rng.randint(ms, me-1); return word[:pos]+rng.choice(EVA_CHARS)+word[pos+1:]
    elif op == 'insert':
        pos = rng.randint(ms, me); return word[:pos]+rng.choice(EVA_CHARS)+word[pos:]
    else:
        if me-ms<=1: return word[:ms]+rng.choice(EVA_CHARS)+word[ms+1:]
        pos = rng.randint(ms, me-1); return word[:pos]+word[pos+1:]

def draw_buf(buf, prev_onset, p_ot_ot, rng):
    bl = list(buf)
    if not bl: return None
    if prev_onset == 'qok' and P_QOKCH > 0 and rng.random() < P_QOKCH:
        cw = [w for w in bl if get_onset(w) == 'ch']
        if cw: return rng.choice(cw)
    if prev_onset == 'ch' and P_CHQOK > 0 and rng.random() < P_CHQOK:
        qw = [w for w in bl if get_onset(w) == 'qok']
        if qw: return rng.choice(qw)
    if prev_onset == 'ot' and p_ot_ot > 0 and rng.random() < p_ot_ot:
        ow = [w for w in bl if get_onset(w) == 'ot']
        if ow: return rng.choice(ow)
    return rng.choice(bl)

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

def run_sim(latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
            ll_onsets, onset_lf, onset_ll, p_blind, target_lines, p_ot_ot, rng):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    prev_onset = None; prev_word = None
    while len(lines) < target_lines and pos < len(w)-2:
        n_words = max(2, min(20, round(rng.gauss(MU_LEN, SIGMA_LEN))))
        chunk = w[pos:pos+n_words]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0: ew = cipher_lf(onset_mid, suffix_lf_sup, onset_lf, P_LF, rng)
            elif i == len(chunk)-1: ew = cipher_ll(onset_mid, suffix_global, ll_onsets, onset_ll, p_blind, rng)
            else:
                if prev_word is not None and P_STUTTER > 0 and rng.random() < P_STUTTER: ew = prev_word
                elif buf and rng.random() < CP:
                    src = draw_buf(buf, prev_onset, p_ot_ot, rng)
                    if src is None: src = random_eva_word(onset_mid, suffix_mid_sup, rng)
                    ew = timm_modify(src, onset_mid, suffix_mid_sup, rng) if rng.random() < MP else src
                else: ew = random_eva_word(onset_mid, suffix_mid_sup, rng)
                buf.append(ew)
            prev_onset = get_onset(ew); prev_word = ew; line.append(ew)
        lines.append(line); pos += n_words
    return lines[:target_lines]

def compute_ot_ot_mid(lines):
    mid_words = [w for l in lines for w in l[1:-1] if len(l)>2]
    n_mid = max(1, len(mid_words))
    oc_mid = Counter(get_onset(w) for w in mid_words)
    mid_bg = Counter(); mid_bg_n = 0
    for line in lines:
        nn = len(line)
        if nn < 4: continue
        for i in range(1, nn-2):
            mid_bg[(get_onset(line[i]), get_onset(line[i+1]))] += 1; mid_bg_n += 1
    def E2_mid(x, y):
        px = oc_mid.get(x,0)/n_mid; py = oc_mid.get(y,0)/n_mid
        pxy = mid_bg.get((x,y),0)/mid_bg_n if mid_bg_n>0 else 0
        return pxy/(px*py) if px*py>0 else float('nan')
    ot_mid_rate = oc_mid.get('ot',0)/n_mid
    return E2_mid('ot','ot'), ot_mid_rate, mid_bg.get(('ot','ot'),0)

# ─── Main ──────────────────────────────────────────────────────────────────────

print("Parsing VMS B-dialect corpus...")
b_lines = parse_vms_b()
print(f"  B-dialect: {len(b_lines)} lines")

# VMS ot→ot MID measurement
vms_mid = [w for l in b_lines for w in l[1:-1] if len(l)>2]
vms_ot_mid_rate = Counter(get_onset(w) for w in vms_mid).get('ot',0) / max(1,len(vms_mid))
vms_ot_ot_e2, _, vms_ot_ot_n = compute_ot_ot_mid(b_lines)
print(f"  VMS B-dialect MID ot rate: {vms_ot_mid_rate:.4f}")
print(f"  VMS B-dialect ot→ot E_mid: {vms_ot_ot_e2:.3f} (N={vms_ot_ot_n})")

# Check 'other' contamination before fix
all_words_b = [w for l in b_lines for w in l]
other_mid_rate = Counter(get_onset(w) for w in vms_mid).get('other',0) / max(1,len(vms_mid))
print(f"  Pre-fix B-dialect MID 'other' rate: {other_mid_rate:.4f} ({other_mid_rate*100:.2f}%)")

# Build distributions WITH fix
suffix_global = build_suffix(all_words_b)
onset_mid_raw = build_onset_dist(vms_mid)
onset_mid = filter_other(onset_mid_raw)  # FIX
onset_lf_raw = build_onset_dist([l[0] for l in b_lines if l])
onset_lf = filter_other(onset_lf_raw)
onset_ll_raw = build_onset_dist([l[-1] for l in b_lines if len(l)>1])
onset_ll = filter_other(onset_ll_raw)

# Compute d_boost for B-dialect
d_global = Counter(get_onset(w) for w in all_words_b).get('d',0)/len(all_words_b)
ll_words_b = [l[-1] for l in b_lines if len(l)>1]
d_ll_rate = Counter(get_onset(w) for w in ll_words_b).get('d',0)/len(ll_words_b)
d_ll_target = d_ll_rate/d_global if d_global>0 else 1.0
d_ll_non_blind = onset_ll.get('d',0)
d_boost = compute_d_boost(d_global, d_ll_target, d_ll_non_blind, P_BLIND)
ll_onsets = build_ll_onsets(onset_ll, d_boost)
suffix_lf_sup = make_suppressed_suffix(suffix_global, R_LF)
suffix_mid_sup = make_suppressed_suffix(suffix_global, R_MID)
target_lines = len(b_lines)

print(f"\nPost-fix onset_mid['ot'] = {onset_mid.get('ot',0):.4f} (VMS MID ot = {vms_ot_mid_rate:.4f})")
print(f"Post-fix onset_mid sum   = {sum(onset_mid.values()):.4f}")

print("\nLoading Latin corpus...")
latin = load_latin(LATIN_CORPUS)

# ─── Run both conditions ───────────────────────────────────────────────────────

for p_ot_ot, label in [(0.00, 'NO p_ot_ot (baseline)'), (0.10, 'p_ot_ot=0.10')]:
    print(f"\nRunning N={N_SIM} simulations: {label}...")
    sim_all_lines = []
    for trial in range(N_SIM):
        rng = random.Random(SEED + trial*100 + int(p_ot_ot*1000))
        lines = run_sim(latin, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                        ll_onsets, onset_lf, onset_ll, P_BLIND, target_lines, p_ot_ot, rng)
        sim_all_lines.extend(lines)
        if (trial+1) % 5 == 0: print(f"  Trial {trial+1}/{N_SIM} done")

    e2, ot_rate, n_ot = compute_ot_ot_mid(sim_all_lines)
    delta = e2 - vms_ot_ot_e2
    print(f"\n  [{label}]")
    print(f"  Sim MID ot rate: {ot_rate:.4f} (VMS: {vms_ot_mid_rate:.4f}, ratio: {ot_rate/vms_ot_mid_rate:.2f}x)")
    print(f"  ot→ot E_mid: Sim={e2:.3f}, VMS={vms_ot_ot_e2:.3f}, Δ={delta:+.3f} (N_sim={n_ot})")
    if abs(delta) < 0.15:
        print(f"  STATUS: MATCH (gap eliminated or minimal)")
    elif delta < -0.15:
        print(f"  STATUS: GAP PERSISTS (Sim under-produces)")
    else:
        print(f"  STATUS: OVER-PRODUCED (Sim exceeds VMS)")

print(f"\nDone.")
