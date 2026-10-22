"""
exp_273: H474 — B-Dialect 12-Mechanism Corpus-Split Stability

Question: Does the 12-mechanism B-dialect architecture (exp_257: filter_other + p_chqok=0.12)
remain corpus-split stable when run on odd and even folio halves?

Background:
- exp_223: B-dialect 11-mechanism split stable (17/19 odd, 17/19 even)
  Two failures: am_lf_enr (small edy N, Poisson noise) and adj_rate (both near-zero)
- exp_249: p_chqok=0.12 added (12th mechanism) — ch↔qok bidirectional coupling
- exp_257: filter_other applied to all onset distributions — renormalization ~6%
- Neither change has been tested in split context
- Risk: p_chqok adds a ch→qok rule; if ch-onset words cluster in specific folios,
  the rule may be over-fitted to the full corpus

Design:
- Parameters FROZEN at full-corpus exp_257 values:
  P_BLIND=0.115, R_LF=0.12, R_MID=0.25, P_STUTTER=0.006, MU_LEN=8.4, SIGMA_LEN=3.0
  CP=0.55, MP=0.90, P_QOKCH=0.12, P_CHQOK=0.12, P_LF=1.0
- Corpus-derived per-half: onset distributions, suffix distributions, d_boost (derived), VMS reference
- Folio parity: odd folios (folio number odd) vs even folios (even)
- N=30 per half (matching exp_223 and exp_264)
- Acceptable: ≥17/19 for each half
- Key metrics to watch: qok_ch (ch↔qok coupling), ss_d, am_lf_enr (known Poisson-noisy)
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_FULL = 30; WINDOW = 20; SEED = 273000

# B-dialect 12-mechanism parameters (frozen at exp_257 values)
P_BLIND   = 0.115; P_LF    = 1.0;   CP       = 0.55; MP       = 0.90
P_QOKCH   = 0.12;  P_CHQOK = 0.12;  P_STUTTER = 0.006
R_LF      = 0.12;  R_MID   = 0.25;  MU_LEN   = 8.4;  SIGMA_LEN = 3.0

EVA_CHARS = list('acdehiklmnoqrsty')
ONSET_ORDER = [
    ('qok', 'qok'), ('qot', 'qot'), ('qo', 'qo'), ('cth', 'cth'),
    ('ch', 'ch'), ('sh', 'sh'), ('ok', 'ok'), ('ot', 'ot'), ('ol', 'ol'),
    ('d', 'd'), ('s', 's'), ('y', 'y'), ('k', 'k'), ('t', 't'),
    ('l', 'l'), ('r', 'r'), ('p', 'p'), ('f', 'f'), ('o', 'o'),
]
SUFFIX_PATTERNS = ['eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy']

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
    return 'B' if (stats['edy'] + stats['eedy']) / total >= 0.05 else 'A'

def folio_number(folio_tag):
    base = re.sub(r'[rv]$', '', folio_tag)
    try: return int(re.sub(r'[a-z]', '', base))
    except: return -1

def filter_other(dist):
    filtered = {k: v for k, v in dist.items() if k != 'other'}
    total = sum(filtered.values())
    return {k: v/total for k, v in filtered.items()} if total > 0 else filtered

def parse_vms_b(split=None):
    """Parse B-dialect lines. split: None=full, 'odd'=odd folios, 'even'=even folios."""
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
            if split is not None:
                fnum = folio_number(folio)
                if split == 'odd'  and fnum % 2 == 0: continue
                if split == 'even' and fnum % 2 == 1: continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words: b_lines.append(words)
    return b_lines

def build_suffix(words):
    n = max(1, len(words)); suf_ctr = Counter()
    for w in words:
        for suf in SUFFIX_PATTERNS:
            if w.endswith(suf): suf_ctr[suf] += 1; break
        else: suf_ctr['other'] += 1
    return {suf: cnt/n for suf, cnt in suf_ctr.items()}

def build_onset_dist(words):
    n = max(1, len(words))
    return {o: cnt/n for o, cnt in Counter(get_onset(w) for w in words).items()}

def make_suppressed_suffix(suffix_global, r_am):
    am_w = suffix_global.get('am', 0.0); new_am = am_w * r_am; delta = am_w - new_am
    non_am = 1.0 - am_w
    return {s: (new_am if s=='am' else w + w/non_am*delta) for s, w in suffix_global.items()} \
           if non_am > 0 else dict(suffix_global)

def compute_d_boost(d_global, d_ll_target, d_ll_non_blind_enr, p_blind):
    """d_ll_non_blind_enr = onset_ll['d'] / d_global (enrichment ratio)."""
    return d_global * (d_ll_target - (1-p_blind) * d_ll_non_blind_enr) / p_blind

def build_ll_onsets(onset_ll, d_boost_weight):
    rem = 1.0 - d_boost_weight
    base = {o: v for o, v in onset_ll.items() if o != 'd'}
    bt = sum(base.values())
    norm = {o: v/bt*rem for o, v in base.items()} if bt > 0 else {}
    norm['d'] = d_boost_weight; return norm

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

def draw_buf(buf, prev_onset, rng):
    bl = list(buf)
    if not bl: return None
    if prev_onset == 'qok' and P_QOKCH > 0 and rng.random() < P_QOKCH:
        cw = [w for w in bl if get_onset(w) == 'ch']
        if cw: return rng.choice(cw)
    if prev_onset == 'ch' and P_CHQOK > 0 and rng.random() < P_CHQOK:
        qw = [w for w in bl if get_onset(w) == 'qok']
        if qw: return rng.choice(qw)
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
            ll_onsets, onset_lf, onset_ll, p_blind, target_lines, rng):
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
                    src = draw_buf(buf, prev_onset, rng)
                    if src is None: src = random_eva_word(onset_mid, suffix_mid_sup, rng)
                    ew = timm_modify(src, onset_mid, suffix_mid_sup, rng) if rng.random() < MP else src
                else: ew = random_eva_word(onset_mid, suffix_mid_sup, rng)
                buf.append(ew)
            prev_onset = get_onset(ew); prev_word = ew; line.append(ew)
        lines.append(line); pos += n_words
    return lines[:target_lines]

def build_vms_ref(b_lines):
    """Build VMS reference metrics from a set of B-dialect lines."""
    all_words = [w for l in b_lines for w in l]
    mid_words = [w for l in b_lines for w in l[1:-1] if len(l)>2]
    lf_words  = [l[0] for l in b_lines if l]
    ll_words  = [l[-1] for l in b_lines if len(l)>1]
    n = len(all_words); n_lf = len(lf_words); n_ll = len(ll_words); n_mid = len(mid_words)

    oc_all = Counter(get_onset(w) for w in all_words)
    oc_lf  = Counter(get_onset(w) for w in lf_words)
    oc_ll  = Counter(get_onset(w) for w in ll_words)

    am_r = sum(1 for w in all_words if w.endswith('am'))/n
    ll_am = sum(1 for w in ll_words if w.endswith('am'))/n_ll if n_ll>0 else 0
    lf_am = sum(1 for w in lf_words if w.endswith('am'))/n_lf if n_lf>0 else 0
    mid_am = sum(1 for w in mid_words if w.endswith('am'))/n_mid if n_mid>0 else 0

    def enr(o, ctr_s, ns):
        return (ctr_s.get(o,0)/ns) / (oc_all.get(o,0)/n) if ns>0 and oc_all.get(o,0)>0 else 0

    tb = n-1
    bg = Counter((get_onset(all_words[i]), get_onset(all_words[i+1])) for i in range(tb))
    def ss(o):
        b = oc_all.get(o,0)/n
        return bg.get((o,o),0)/(tb*b*b) if b>0 else 1.0
    qok_r = oc_all.get('qok',0)/n; ch_r = oc_all.get('ch',0)/n

    return {
        'am_ll':         ll_am/am_r if am_r>0 else 0,
        'd_ll':          enr('d', oc_ll, n_ll),
        'y_lf':          enr('y', oc_lf, n_lf),
        'ss_mean':       (ss('qok')+ss('ok')+ss('ch'))/3,
        'adj_rate':      sum(1 for i in range(tb) if all_words[i]==all_words[i+1])/max(1,tb),
        'qok_lf':        enr('qok', oc_lf, n_lf),
        'd_lf':          enr('d', oc_lf, n_lf),
        's_lf':          enr('s', oc_lf, n_lf),
        'ch_ll':         enr('ch', oc_ll, n_ll),
        'ok_ll':         enr('ok', oc_ll, n_ll),
        'qok_ll':        enr('qok', oc_ll, n_ll),
        'ss_d':          ss('d'),
        'ss_y':          ss('y'),
        'am_lf_enr':     lf_am/am_r if am_r>0 else 0,
        'am_mid_enr':    mid_am/am_r if am_r>0 else 0,
        'edy_rate':      sum(1 for w in all_words if w.endswith('edy'))/n,
        'word_len_mean': sum(len(w) for w in all_words)/n,
        'qok_ch':        bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r else 0,
        'global_am_rate': am_r,
    }

def compute_metrics(lines):
    aw = [w for l in lines for w in l]; n = len(aw)
    lf = [l[0] for l in lines if l]; ll = [l[-1] for l in lines if len(l)>1]
    mid = [w for l in lines for w in l[1:-1] if len(l)>2]
    oc_all = Counter(get_onset(w) for w in aw)
    oc_lf  = Counter(get_onset(w) for w in lf)
    oc_ll  = Counter(get_onset(w) for w in ll)
    n_lf, n_ll, n_mid = len(lf), len(ll), len(mid)
    def enr(o, ctr_s, ns):
        s = ctr_s.get(o,0)/ns if ns>0 else 0
        g = oc_all.get(o,0)/n if n>0 else 0
        return s/g if g>0 else 0
    am_r  = sum(1 for w in aw if w.endswith('am'))/n
    ll_am = sum(1 for w in ll if w.endswith('am'))/n_ll if n_ll>0 else 0
    am_ll = ll_am/am_r if am_r>0 else 0
    d_ll  = enr('d', oc_ll, n_ll); y_lf = enr('y', oc_lf, n_lf)
    tb = n-1
    bg = Counter((get_onset(aw[i]), get_onset(aw[i+1])) for i in range(tb))
    def ss(o):
        b = oc_all.get(o,0)/n
        return bg.get((o,o),0)/(tb*b*b) if b>0 else 1.0
    ss_mean = (ss('qok')+ss('ok')+ss('ch'))/3
    adj = sum(1 for i in range(tb) if aw[i]==aw[i+1])/max(1,tb)
    qok_lf=enr('qok',oc_lf,n_lf); d_lf=enr('d',oc_lf,n_lf); s_lf=enr('s',oc_lf,n_lf)
    ch_ll=enr('ch',oc_ll,n_ll); ok_ll=enr('ok',oc_ll,n_ll); qok_ll=enr('qok',oc_ll,n_ll)
    ss_d=ss('d'); ss_y=ss('y')
    lf_am=sum(1 for w in lf if w.endswith('am'))/n_lf if n_lf>0 else 0
    mid_am=sum(1 for w in mid if w.endswith('am'))/len(mid) if mid else 0
    am_lf_enr=lf_am/am_r if am_r>0 else 0
    am_mid_enr=mid_am/am_r if am_r>0 else 0
    edy_rate=sum(1 for w in aw if w.endswith('edy'))/n
    word_len=sum(len(w) for w in aw)/n
    qok_r=oc_all.get('qok',0)/n; ch_r=oc_all.get('ch',0)/n
    qok_ch=bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r else 0
    return dict(am_ll=am_ll, d_ll=d_ll, y_lf=y_lf, ss_mean=ss_mean, adj_rate=adj,
                qok_lf=qok_lf, d_lf=d_lf, s_lf=s_lf, ch_ll=ch_ll, ok_ll=ok_ll,
                qok_ll=qok_ll, ss_d=ss_d, ss_y=ss_y, am_lf_enr=am_lf_enr,
                am_mid_enr=am_mid_enr, edy_rate=edy_rate, word_len_mean=word_len,
                qok_ch=qok_ch, global_am_rate=am_r)

BATTERY_KEYS = ['am_ll','d_ll','y_lf','ss_mean','adj_rate','qok_lf','d_lf','s_lf',
                'ch_ll','ok_ll','qok_ll','ss_d','ss_y','am_lf_enr','am_mid_enr',
                'edy_rate','word_len_mean','qok_ch','global_am_rate']
PASS_TOL = 0.20

def run_condition(name, b_lines, latin, seed_offset):
    print(f"\n{'='*70}")
    print(f"CONDITION: {name} corpus ({len(b_lines)} lines, "
          f"{sum(len(l) for l in b_lines)} words)")
    print(f"{'='*70}")

    all_words = [w for l in b_lines for w in l]
    lf_words  = [l[0] for l in b_lines if l]
    ll_words  = [l[-1] for l in b_lines if len(l)>1]
    mid_words = [w for l in b_lines for w in l[1:-1] if len(l)>2]
    n = len(all_words)

    # VMS reference from THIS corpus half
    vms_ref = build_vms_ref(b_lines)
    print(f"  VMS ref: am_ll={vms_ref['am_ll']:.3f}  am_lf_enr={vms_ref['am_lf_enr']:.3f}  "
          f"edy_rate={vms_ref['edy_rate']:.4f}  ss_mean={vms_ref['ss_mean']:.4f}")

    # Build onset/suffix distributions from THIS corpus half
    suffix_global = build_suffix(all_words)
    onset_mid = filter_other(build_onset_dist(mid_words))
    onset_lf  = filter_other(build_onset_dist(lf_words))
    onset_ll  = filter_other(build_onset_dist(ll_words))

    # d_boost: derived from corpus (consistent with exp_257 formula)
    oc_all = Counter(get_onset(w) for w in all_words)
    oc_ll  = Counter(get_onset(w) for w in ll_words)
    d_global = oc_all.get('d',0)/n
    d_ll_rate = oc_ll.get('d',0)/len(ll_words) if ll_words else 0
    d_ll_target = d_ll_rate/d_global if d_global>0 else 1.0
    d_ll_non_blind_enr = onset_ll.get('d',0) / d_global if d_global>0 else 0
    d_boost = compute_d_boost(d_global, d_ll_target, d_ll_non_blind_enr, P_BLIND)
    d_boost_clamped = max(0.0, min(0.5, d_boost))  # safety clamp
    ll_onsets = build_ll_onsets(onset_ll, d_boost_clamped)

    suffix_lf_sup  = make_suppressed_suffix(suffix_global, R_LF)
    suffix_mid_sup = make_suppressed_suffix(suffix_global, R_MID)
    target_lines = len(b_lines)

    print(f"  d_boost={d_boost_clamped:.4f}  d_ll_target(enr)={d_ll_target:.3f}")

    # Run N=30 simulations
    all_metrics = []
    for trial in range(N_FULL):
        rng = random.Random(SEED + trial*100 + seed_offset)
        lines = run_sim(latin, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                        ll_onsets, onset_lf, onset_ll, P_BLIND, target_lines, rng)
        all_metrics.append(compute_metrics(lines))
        if (trial+1) % 10 == 0: print(f"  Trial {trial+1}/{N_FULL} done")

    avg = {k: sum(x[k] for x in all_metrics)/N_FULL for k in all_metrics[0]}

    passes = 0
    print(f"\n  {'Metric':<18} {'VMS':>8} {'Sim':>8} {'%VMS':>7} {'PASS':>5}")
    print(f"  {'-'*55}")
    for k in BATTERY_KEYS:
        v = avg[k]; t = vms_ref[k]
        pct = 100*v/t if t>0 else 0
        ok = 'PASS' if t>0 and abs(v/t-1)<=PASS_TOL else 'FAIL'
        if ok=='PASS': passes+=1
        flag = ' *' if ok=='FAIL' else ''
        print(f"  {k:<18} {t:>8.4f} {v:>8.4f} {pct:>7.1f}% {ok:>5}{flag}")
    print(f"\n  TOTAL: {passes}/{len(BATTERY_KEYS)} PASS")
    return passes, avg, vms_ref

# ─── Main ────────────────────────────────────────────────────────────────────

print("Loading Latin corpus...")
latin = load_latin(LATIN_CORPUS)

print("\nParsing B-dialect corpus (3 conditions: full, odd, even)...")
full_lines = parse_vms_b(split=None)
odd_lines  = parse_vms_b(split='odd')
even_lines = parse_vms_b(split='even')
print(f"  Full: {len(full_lines)} lines  Odd: {len(odd_lines)} lines  Even: {len(even_lines)} lines")
print(f"  Full words: {sum(len(l) for l in full_lines)}  "
      f"Odd: {sum(len(l) for l in odd_lines)}  Even: {sum(len(l) for l in even_lines)}")

full_passes, full_avg, full_ref = run_condition('Full',  full_lines, latin, seed_offset=0)
odd_passes,  odd_avg,  odd_ref  = run_condition('Odd',   odd_lines,  latin, seed_offset=1)
even_passes, even_avg, even_ref = run_condition('Even',  even_lines, latin, seed_offset=2)

print(f"\n{'='*70}")
print("SPLIT STABILITY SUMMARY")
print(f"{'='*70}")
print(f"  Full:  {full_passes}/19 PASS")
print(f"  Odd:   {odd_passes}/19 PASS")
print(f"  Even:  {even_passes}/19 PASS")
print()
print(f"  {'Metric':<18} {'Full_VMS':>10} {'Full_Sim':>10} {'Odd_VMS':>10} {'Odd_Sim':>10} {'Even_VMS':>10} {'Even_Sim':>10}")
for k in BATTERY_KEYS:
    fv=full_ref[k]; fs=full_avg[k]; ov=odd_ref[k]; os_=odd_avg[k]; ev=even_ref[k]; es=even_avg[k]
    f_ok = '✓' if fv>0 and abs(fs/fv-1)<=PASS_TOL else '✗'
    o_ok = '✓' if ov>0 and abs(os_/ov-1)<=PASS_TOL else '✗'
    e_ok = '✓' if ev>0 and abs(es/ev-1)<=PASS_TOL else '✗'
    print(f"  {k:<18} {fv:>10.4f} {fs:>10.4f}{f_ok} {ov:>10.4f} {os_:>10.4f}{o_ok} {ev:>10.4f} {es:>10.4f}{e_ok}")
print()
print("Stability verdict: STABLE if Odd≥17/19 and Even≥17/19")
if odd_passes >= 17 and even_passes >= 17:
    print("  STABLE — B-dialect 12-mechanism architecture split-stable.")
else:
    print("  UNSTABLE — Check which metrics fail and which are VMS target instability vs simulation failure.")
