"""
exp_275: H476 — ch→ch and sh→sh Depletion in MID Position

Problem from exp_246: VMS MID shows ch→ch and sh→sh DEPLETED (E<1) while
simulation over-produces them. The battery doesn't track these.

Questions:
1. Confirm MID-only E2(ch→ch) and E2(sh→sh) for both dialects (F246 data)
2. Is this depletion section-specific (lexical) or uniform (grammatical)?
3. HHI/null for ch→ch and sh→sh pairs — random (grammatical) or concentrated?
4. What follows ch-onset words? (ch→X distribution)
5. Simulation MID-only E2 for ch→ch and sh→sh (compare to VMS)
6. Compare to other high-frequency onsets: does depletion correlate with onset frequency?

Note: ch and sh are the two highest-frequency onsets in both dialects (~15-25% each).
High-frequency onsets would be EXPECTED to self-succeed more by chance (buffer cycling),
yet VMS shows depletion. This is a genuine anti-self-succession pattern.
"""
from pathlib import Path as _RepositoryPath

import os, re, random, math
from collections import Counter, deque, defaultdict

REPO_DIR   = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
DATA_PATH  = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')

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

def folio_base(folio): return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    return 'B' if (stats['edy'] + stats['eedy']) / total >= .05 else 'A'

def folio_number(folio_tag):
    base = re.sub(r'[rv]$', '', folio_tag)
    try: return int(re.sub(r'[a-z]', '', base))
    except: return -1

def get_section(fb):
    fnum = folio_number(fb)
    if 1 <= fnum <= 65: return 'herbal'
    if 66 <= fnum <= 74: return 'astro'
    if 75 <= fnum <= 81: return 'bio'
    if 82 <= fnum <= 102: return 'cosmo'
    if 103 <= fnum <= 116: return 'recipes'
    if 116 <= fnum <= 120: return 'stars'
    return 'other'

def parse_vms(target_dialect=None):
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1); folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w)>=2]
            for w in words:
                folio_word_stats[fb]['total'] += 1
                if w.endswith('eedy'): folio_word_stats[fb]['eedy'] += 1
                elif w.endswith('edy'): folio_word_stats[fb]['edy'] += 1
    folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}

    lines_by_dialect = defaultdict(list)
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1); locus_code = m.group(3)
            folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
            d = folio_dialect.get(fb, 'unknown')
            if target_dialect and d != target_dialect: continue
            lc_stripped = locus_code.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w)>=2]
            if words:
                lines_by_dialect[d].append({'fb': fb, 'section': get_section(fb), 'words': words})
    return lines_by_dialect

def mid_bigrams(lines):
    """Get all MID→MID adjacent word pairs (within a line, excluding LF and LL)."""
    pairs = []
    mid_words = []
    for rec in lines:
        ws = rec['words']
        mid = ws[1:-1] if len(ws) > 2 else []
        mid_words.extend(mid)
        for i in range(len(mid)-1):
            pairs.append((get_onset(mid[i]), get_onset(mid[i+1]), mid[i], mid[i+1]))
    return mid_words, pairs

def e2_mid(mid_words, pairs, x, y):
    """E2(x→y) in MID-only bigrams."""
    n = len(mid_words); tb = len(pairs)
    if n < 2 or tb == 0: return float('nan'), 0
    px = sum(1 for w in mid_words if get_onset(w)==x)/n
    py = sum(1 for w in mid_words if get_onset(w)==y)/n
    pxy = sum(1 for (a,b,_,__) in pairs if a==x and b==y)/tb
    e2 = pxy/(px*py) if px*py>0 else float('nan')
    nxy = sum(1 for (a,b,_,__) in pairs if a==x and b==y)
    return e2, nxy

def hhi_null_ratio(word_pairs):
    if not word_pairs: return float('nan')
    n = len(word_pairs)
    pair_ctr = Counter(word_pairs)
    hhi_obs = sum((cnt/n)**2 for cnt in pair_ctr.values())
    x_words = [a for a,b in word_pairs]; y_words = [b for a,b in word_pairs]
    x_ctr = Counter(x_words); y_ctr = Counter(y_words)
    n_x = len(x_words); n_y = len(y_words)
    hhi_null = sum((v/n_x)**2 for v in x_ctr.values()) * sum((v/n_y)**2 for v in y_ctr.values())
    return hhi_obs/hhi_null if hhi_null>0 else float('nan')

def analyze_depletion(lines, onset_label, label=''):
    """Full analysis of onset self-succession in MID position."""
    mid_words, pairs = mid_bigrams(lines)
    n_mid = len(mid_words); n_pairs = len(pairs)
    onset_cnt = sum(1 for w in mid_words if get_onset(w)==onset_label)
    rate = onset_cnt/n_mid if n_mid>0 else 0

    e2, nxy = e2_mid(mid_words, pairs, onset_label, onset_label)
    print(f"\n  {label}: {onset_label}→{onset_label}")
    print(f"    N_mid_words={n_mid}  {onset_label}_rate={100*rate:.1f}%  "
          f"N_mid_pairs={n_pairs}  N_{onset_label}{onset_label}={nxy}")
    print(f"    E2_mid = {e2:.4f}  {'DEPLETED' if e2<1 else 'ENRICHED'}")

    # Section stratification
    section_lines = defaultdict(list)
    for rec in lines:
        section_lines[rec['section']].append(rec)
    print(f"    Section breakdown:")
    for sec in ['herbal','astro','bio','cosmo','recipes','stars']:
        sl = section_lines[sec]
        sw, sp = mid_bigrams(sl)
        if len(sw) < 20: continue
        se2, snxy = e2_mid(sw, sp, onset_label, onset_label)
        sr = sum(1 for w in sw if get_onset(w)==onset_label)/len(sw)
        print(f"      {sec:>10}: E2={se2:.3f}  N={snxy}  n_mid={len(sw)}  rate={100*sr:.1f}%")

    # HHI/null for self-pairs
    self_word_pairs = [(w1, w2) for (a,b,w1,w2) in pairs if a==onset_label and b==onset_label]
    if self_word_pairs:
        hhi = hhi_null_ratio(self_word_pairs)
        pair_ctr = Counter(self_word_pairs)
        top5 = pair_ctr.most_common(5)
        top5_cov = sum(c for _,c in top5)/len(self_word_pairs)
        print(f"    HHI/null={hhi:.3f}  top5_cov={top5_cov:.3f}  N_pairs={len(self_word_pairs)}")
        if hhi < 1.5:
            print(f"    → GRAMMATICAL (near-random)")
        else:
            print(f"    → LEXICAL or small-N artifact (concentrated pairs)")

    # ch→X MID transition distribution
    print(f"    {onset_label}→X in MID:")
    after_onset = Counter((b, w2) for (a,b,w1,w2) in pairs if a==onset_label)
    by_onset = Counter(b for (b, w2) in after_onset.elements())
    total_after = sum(by_onset.values())
    onset_rate_in_mid = Counter(get_onset(w) for w in mid_words)
    if total_after > 0:
        rows = []
        for o, cnt in sorted(by_onset.items(), key=lambda x: -x[1])[:8]:
            exp_rate = onset_rate_in_mid.get(o,0)/n_mid if n_mid>0 else 0
            act_rate = cnt/total_after
            enr = act_rate/exp_rate if exp_rate>0 else float('inf')
            rows.append((o, cnt, act_rate, exp_rate, enr))
        print(f"    {'Onset':>8} {'Count':>6} {'Actual':>8} {'Expected':>9} {'E':>6}")
        for o, cnt, act, exp, enr in rows[:6]:
            marker = '*' if enr < 0.5 else ('+' if enr > 1.5 else ' ')
            print(f"    {o:>8} {cnt:>6} {act:>8.3f} {exp:>9.3f} {enr:>6.3f}{marker}")

    return e2, nxy, rate

# ─── Simulation ───────────────────────────────────────────────────────────────

SUFFIX_PATTERNS = ['eedy','edy','aiin','ain','am','ey','ol','or','al','ar','dy']
EVA_CHARS = list('acdehiklmnoqrsty')

A_PARAMS = dict(p_blind=0.0505, d_boost=0.2430, r_lf=0.266, r_mid=0.87,
                p_stutter=0.002, mu_len=5.64, sigma_len=2.5,
                cp=0.55, mp=0.90, p_qokch=0.12, p_chqok=0.00, p_lf=1.0,
                p_y_y=0.10, p_o_o=0.10, p_sh_qok=0.10, window=20)
B_PARAMS = dict(p_blind=0.115, r_lf=0.12, r_mid=0.25,
                p_stutter=0.006, mu_len=8.4, sigma_len=3.0,
                cp=0.55, mp=0.90, p_qokch=0.12, p_chqok=0.12, p_lf=1.0,
                p_y_y=0.00, p_o_o=0.00, p_sh_qok=0.00, window=20)

def get_onset_len(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return len(prefix)
    return 0

def get_edy_suf_len(w):
    if w.endswith('eedy'): return 4
    if w.endswith('edy'): return 3
    return 0

def build_onset_dist(words):
    n = max(1, len(words))
    return {o: cnt/n for o, cnt in Counter(get_onset(w) for w in words).items()}

def build_suffix(words):
    n = max(1, len(words)); suf = Counter()
    for w in words:
        for s in SUFFIX_PATTERNS:
            if w.endswith(s): suf[s]+=1; break
        else: suf['other']+=1
    return {s: c/n for s, c in suf.items()}

def filter_other(d):
    fd = {k: v for k, v in d.items() if k != 'other'}
    t = sum(fd.values())
    return {k: v/t for k, v in fd.items()} if t > 0 else fd

def make_sup_suffix(suf_g, r):
    am = suf_g.get('am', 0); new_am = am*r; delta = am - new_am
    non_am = 1 - am
    return {s: (new_am if s=='am' else w + w/non_am*delta) for s, w in suf_g.items()} if non_am>0 else dict(suf_g)

def build_ll_onsets(onset_ll, d_boost_w):
    rem = 1-d_boost_w; base = {o: v for o, v in onset_ll.items() if o!='d'}
    bt = sum(base.values())
    n = {o: v/bt*rem for o, v in base.items()} if bt>0 else {}
    n['d'] = d_boost_w; return n

def make_word(o, s, rng):
    if s.endswith('edy') or s.endswith('eedy'): return o+rng.choice(['a','ai','o','oi','e','ei'])+s
    return o+s

def random_word(onset_w, suf_w, rng):
    o = rng.choices(list(onset_w.keys()), weights=list(onset_w.values()))[0]
    s = rng.choices(list(suf_w.keys()), weights=list(suf_w.values()))[0]
    return make_word(o, s, rng)

def cipher_lf(onset_lf, suf_lf, p_lf, onset_mid, rng):
    if rng.random() < p_lf:
        o = rng.choices(list(onset_lf.keys()), weights=list(onset_lf.values()))[0]
        s = rng.choices(list(suf_lf.keys()), weights=list(suf_lf.values()))[0]
        return make_word(o, s, rng)
    return random_word(onset_mid, suf_lf, rng)

def cipher_ll(onset_mid, suf_g, ll_onsets, onset_ll, p_blind, rng):
    if rng.random() < p_blind:
        o = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return o + 'am'
    o = rng.choices(list(onset_ll.keys()), weights=list(onset_ll.values()))[0]
    s = rng.choices(list(suf_g.keys()), weights=list(suf_g.values()))[0]
    return make_word(o, s, rng)

def timm(w, onset_mid, suf_mid, rng):
    if not w: return w
    ol = get_onset_len(w); el = get_edy_suf_len(w)
    ms = ol; me = len(w)-el
    if ms >= me: return random_word(onset_mid, suf_mid, rng)
    op = rng.choice(['replace','insert','delete'])
    if op == 'replace':
        p = rng.randint(ms,me-1); return w[:p]+rng.choice(EVA_CHARS)+w[p+1:]
    elif op == 'insert':
        p = rng.randint(ms,me); return w[:p]+rng.choice(EVA_CHARS)+w[p:]
    else:
        if me-ms<=1: return w[:ms]+rng.choice(EVA_CHARS)+w[ms+1:]
        p = rng.randint(ms,me-1); return w[:p]+w[p+1:]

def draw_buf(buf, prev, p):
    bl = list(buf)
    if not bl: return None
    if prev=='qok' and p.get('p_qokch',0)>0 and r()<p['p_qokch']:
        cw=[w for w in bl if get_onset(w)=='ch']
        if cw: return r.choice(cw)
    return r.choice(bl)

ENGLISH_SW = {'the','and','of','to','a','in','that','is','was','he','it','for','on','are',
              'as','with','his','they','at','be','this','have','from','or','had','by','not',
              'but','what','all','were','we'}

def load_latin(path):
    with open(path,encoding='utf-8',errors='replace') as f: text = f.read()
    words = []
    for p in re.split(r'\n\s*\n', text):
        ws = re.findall(r'\b[a-zA-Z]+\b', p)
        if not ws: continue
        if sum(1 for w in ws if w.lower() in ENGLISH_SW)/len(ws) < 0.08: words.extend(ws)
    return words

def draw_buf_full(buf, prev_onset, params, rng):
    bl = list(buf)
    if not bl: return None
    if prev_onset=='qok' and params.get('p_qokch',0)>0 and rng.random()<params['p_qokch']:
        cw=[w for w in bl if get_onset(w)=='ch']
        if cw: return rng.choice(cw)
    if prev_onset=='ch' and params.get('p_chqok',0)>0 and rng.random()<params['p_chqok']:
        qw=[w for w in bl if get_onset(w)=='qok']
        if qw: return rng.choice(qw)
    if prev_onset=='y' and params.get('p_y_y',0)>0 and rng.random()<params['p_y_y']:
        yw=[w for w in bl if get_onset(w)=='y']
        if yw: return rng.choice(yw)
    if prev_onset=='o' and params.get('p_o_o',0)>0 and rng.random()<params['p_o_o']:
        ow=[w for w in bl if get_onset(w)=='o']
        if ow: return rng.choice(ow)
    if prev_onset=='sh' and params.get('p_sh_qok',0)>0 and rng.random()<params['p_sh_qok']:
        qw=[w for w in bl if get_onset(w)=='qok']
        if qw: return rng.choice(qw)
    return rng.choice(bl)

def run_sim(latin_words, onset_mid, suf_g, suf_lf, suf_mid, ll_onsets, onset_lf, onset_ll, params, target, rng):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=params['window']), 0
    prev_onset = None; prev_word = None
    while len(lines)<target and pos<len(w)-2:
        n_words = max(2, min(20, round(rng.gauss(params['mu_len'], params['sigma_len']))))
        chunk = w[pos:pos+n_words]
        if len(chunk)<2: pos+=len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i==0: ew=cipher_lf(onset_lf,suf_lf,params['p_lf'],onset_mid,rng)
            elif i==len(chunk)-1: ew=cipher_ll(onset_mid,suf_g,ll_onsets,onset_ll,params['p_blind'],rng)
            else:
                if prev_word and params['p_stutter']>0 and rng.random()<params['p_stutter']: ew=prev_word
                elif buf and rng.random()<params['cp']:
                    src=draw_buf_full(buf,prev_onset,params,rng)
                    if src is None: src=random_word(onset_mid,suf_mid,rng)
                    ew=timm(src,onset_mid,suf_mid,rng) if rng.random()<params['mp'] else src
                else: ew=random_word(onset_mid,suf_mid,rng)
                buf.append(ew)
            prev_onset=get_onset(ew); prev_word=ew; line.append(ew)
        lines.append(line); pos+=n_words
    return lines[:target]

def sim_mid_e2(sim_lines, x, y):
    """E2(x→y) in simulation MID words."""
    mid_words_sim = [w for l in sim_lines for w in l[1:-1] if len(l)>2]
    pairs_sim = []
    for l in sim_lines:
        mid = l[1:-1] if len(l)>2 else []
        for i in range(len(mid)-1):
            pairs_sim.append((get_onset(mid[i]),get_onset(mid[i+1])))
    n = len(mid_words_sim); tb = len(pairs_sim)
    px = sum(1 for w in mid_words_sim if get_onset(w)==x)/n if n>0 else 0
    py = sum(1 for w in mid_words_sim if get_onset(w)==y)/n if n>0 else 0
    pxy = sum(1 for (a,b) in pairs_sim if a==x and b==y)/tb if tb>0 else 0
    e2 = pxy/(px*py) if px*py>0 else float('nan')
    nxy = sum(1 for (a,b) in pairs_sim if a==x and b==y)
    return e2, nxy

def main():
    print("Parsing VMS corpus...")
    d_lines = parse_vms()

    print(f"\n{'='*70}")
    print("SECTION A: VMS CORPUS ANALYSIS")
    print(f"{'='*70}")

    for dialect in ['A', 'B']:
        print(f"\n{'─'*60}")
        print(f"DIALECT {dialect}")
        lines = d_lines.get(dialect, [])
        print(f"  Total lines: {len(lines)}")

        print(f"\n  --- MID E2 for all high-frequency onsets ---")
        mid_words, pairs = mid_bigrams(lines)
        n_mid = len(mid_words)
        # Compute E2 for all onsets, sorted by frequency
        onset_counts = Counter(get_onset(w) for w in mid_words)
        n_pairs = len(pairs)
        print(f"  N_mid_words={n_mid}  N_mid_pairs={n_pairs}")
        print(f"  {'Onset':>8} {'Rate%':>7} {'E2(self)':>10} {'N_self':>8} {'Status':>10}")
        for o, cnt in sorted(onset_counts.items(), key=lambda x: -x[1]):
            rate = cnt/n_mid if n_mid>0 else 0
            if rate < 0.01: continue  # skip very rare
            e2, nxy = e2_mid(mid_words, pairs, o, o)
            status = 'DEPLETED' if e2 < 1.0 else 'enriched'
            print(f"  {o:>8} {100*rate:>7.1f}% {e2:>10.4f} {nxy:>8d} {status:>10}")

        print(f"\n  --- Detailed analysis: ch→ch and sh→sh ---")
        for onset in ['ch', 'sh']:
            analyze_depletion(lines, onset, label=f'{dialect}-{onset}')

    print(f"\n{'='*70}")
    print("SECTION B: SIMULATION MID E2 COMPARISON")
    print(f"{'='*70}")

    print("Loading Latin corpus...")
    latin = load_latin(LATIN_CORPUS)
    N_RUNS = 5; SEED = 275000

    for dialect, params in [('A', A_PARAMS), ('B', B_PARAMS)]:
        print(f"\n{'─'*60}")
        print(f"SIMULATION DIALECT {dialect} (N={N_RUNS} runs aggregated)")
        lines = d_lines.get(dialect, [])
        all_words = [w for rec in lines for w in rec['words']]
        mid_words_vms = [w for rec in lines for w in rec['words'][1:-1] if len(rec['words'])>2]
        lf_words = [rec['words'][0] for rec in lines if rec['words']]
        ll_words = [rec['words'][-1] for rec in lines if len(rec['words'])>1]

        onset_mid = filter_other(build_onset_dist(mid_words_vms))
        onset_lf  = filter_other(build_onset_dist(lf_words))
        onset_ll  = filter_other(build_onset_dist(ll_words))
        suf_g  = build_suffix(all_words)
        suf_lf = make_sup_suffix(suf_g, params.get('r_lf', 0.12))
        suf_mid= make_sup_suffix(suf_g, params.get('r_mid', 0.25))
        d_boost_w = params.get('d_boost', 0.0)
        ll_onsets = build_ll_onsets(onset_ll, d_boost_w) if d_boost_w>0 else onset_ll.copy()

        rng = random.Random(SEED)
        all_sim_lines = []
        for _ in range(N_RUNS):
            sl = run_sim(latin, onset_mid, suf_g, suf_lf, suf_mid, ll_onsets, onset_lf, onset_ll,
                        params, len(lines), rng)
            all_sim_lines.extend(sl)

        mid_words_vms_list, pairs_vms = mid_bigrams(lines)
        onset_counts_vms = Counter(get_onset(w) for w in mid_words_vms_list)

        print(f"  {'Onset':>8} {'Rate%':>7} {'VMS_E2':>8} {'VMS_N':>7} {'Sim_E2':>8} {'Sim_N':>7} {'Gap':>8}")
        for o in ['ch', 'sh', 'qok', 'ok', 'ot', 'ol', 'd']:
            rate = onset_counts_vms.get(o,0)/len(mid_words_vms_list) if mid_words_vms_list else 0
            vms_e2, vms_n = e2_mid(mid_words_vms_list, pairs_vms, o, o)
            sim_e2, sim_n = sim_mid_e2(all_sim_lines, o, o)
            gap = sim_e2 - vms_e2 if not (math.isnan(vms_e2) or math.isnan(sim_e2)) else float('nan')
            marker = '*' if abs(gap)>0.3 else ''
            print(f"  {o:>8} {100*rate:>7.1f}% {vms_e2:>8.4f} {vms_n:>7d} {sim_e2:>8.4f} {sim_n:>7d} {gap:>8.4f}{marker}")

if __name__ == '__main__':
    main()
