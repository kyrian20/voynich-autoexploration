"""
exp_248: H453 — qok→ch→qok Return Pattern Analysis

exp_247 found: qok→ch→qok 2nd_order = 1.483 (N=69) in VMS but Sim_2nd = 0.320.
Simulation depletes this pattern below first-order prediction while VMS enriches it.

Diagnostic questions:
1. Is ch→qok itself enriched in MID context? (If E2(ch→qok) > 1, explains trigram)
2. Is qok→ch→qok section-concentrated? (Section clustering explanation)
3. Lexical: is qok→ch→qok driven by specific word triples?
4. Simulation sweep: does adding p_chqok parameter fix qok→ch→qok without regression?

Uses exp_236 simulation architecture with added p_chqok parameter in draw_buf.
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, defaultdict, deque

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')
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

# ── Section mapping by folio number ────────────────────────────────────────────
def get_section(fb):
    try:
        n = int(fb)
        if n <= 100: return 'herbal'
        if n <= 111: return 'astro'
        if n <= 165: return 'cosmo'
        if n <= 170: return 'bio'
        return 'other'
    except:
        return 'other'

# ── Parser (same as exp_247) ────────────────────────────────────────────────────
def parse_vms_b():
    """Parse VMS B-dialect lines (edy_rate >= 5% threshold by folio)."""
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

    def classify_dialect(stats):
        total = stats['total']
        if total == 0: return 'unknown'
        rate = (stats['edy'] + stats['eedy']) / total
        return 'B' if rate >= 0.05 else 'A'

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
            if words: b_lines.append((fb, words))
    return b_lines

# ── VMS Analysis ─────────────────────────────────────────────────────────────

print("Parsing VMS B-dialect...")
b_lines_with_folio = parse_vms_b()
b_lines = [words for fb, words in b_lines_with_folio]
print(f"  {len(b_lines)} lines")

# MID unigrams
mid_onset_counts = Counter()
total_mid = 0
for words in b_lines:
    n = len(words)
    if n < 3: continue
    for i in range(1, n - 1):
        mid_onset_counts[get_onset(words[i])] += 1
        total_mid += 1

rates_mid = {o: mid_onset_counts[o] / total_mid for o in mid_onset_counts}

# MID bigrams
mid_bg = Counter()
mid_bg_n = 0
for words in b_lines:
    n = len(words)
    if n < 4: continue
    for i in range(1, n - 2):
        mid_bg[(get_onset(words[i]), get_onset(words[i+1]))] += 1
        mid_bg_n += 1

# MID trigrams
mid_tg = Counter()
mid_tg_n = 0
for words in b_lines:
    n = len(words)
    if n < 5: continue
    for i in range(1, n - 3):
        mid_tg[(get_onset(words[i]), get_onset(words[i+1]), get_onset(words[i+2]))] += 1
        mid_tg_n += 1

def E2(x, y):
    pxy = mid_bg.get((x, y), 0) / mid_bg_n if mid_bg_n > 0 else 0
    px = rates_mid.get(x, 0); py = rates_mid.get(y, 0)
    return pxy / (px * py) if px * py > 0 else 0

def E3(x, y, z):
    pxyz = mid_tg.get((x, y, z), 0) / mid_tg_n if mid_tg_n > 0 else 0
    px = rates_mid.get(x, 0); py = rates_mid.get(y, 0); pz = rates_mid.get(z, 0)
    return pxyz / (px * py * pz) if px * py * pz > 0 else 0

print(f"  Total MID bigrams: {mid_bg_n}, MID trigrams: {mid_tg_n}")

# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 80)
print("PART 1: ch→X AND X→ch BINARY MID BIGRAMS (what follows ch? what precedes ch?)")
print("=" * 80)

print(f"\n  ch→X (MID bigrams, what follows ch?):")
print(f"  {'X onset':<12}  {'N':>5}  {'E2':>7}  {'rate(X)':>8}")
print(f"  {'-'*12}  {'---':>5}  {'---':>7}  {'---':>8}")
ch_follows = []
for onset in sorted(rates_mid):
    n = mid_bg.get(('ch', onset), 0)
    e = E2('ch', onset)
    if n >= 3:
        ch_follows.append((e, n, onset))
for e, n, onset in sorted(ch_follows, reverse=True):
    print(f"  {onset:<12}  {n:>5}  {e:>7.3f}  {rates_mid.get(onset,0):>8.4f}")

print(f"\n  X→ch (MID bigrams, what precedes ch?):")
print(f"  {'X onset':<12}  {'N':>5}  {'E2':>7}  {'rate(X)':>8}")
print(f"  {'-'*12}  {'---':>5}  {'---':>7}  {'---':>8}")
precedes_ch = []
for onset in sorted(rates_mid):
    n = mid_bg.get((onset, 'ch'), 0)
    e = E2(onset, 'ch')
    if n >= 3:
        precedes_ch.append((e, n, onset))
for e, n, onset in sorted(precedes_ch, reverse=True):
    print(f"  {onset:<12}  {n:>5}  {e:>7.3f}  {rates_mid.get(onset,0):>8.4f}")

e_chqok = E2('ch', 'qok'); n_chqok = mid_bg.get(('ch', 'qok'), 0)
e_qokch = E2('qok', 'ch'); n_qokch = mid_bg.get(('qok', 'ch'), 0)
print(f"\n  KEY SUMMARY:")
print(f"    ch→qok: E2={e_chqok:.3f}, N={n_chqok}, rate_qok={rates_mid.get('qok',0):.4f}")
print(f"    qok→ch: E2={e_qokch:.3f}, N={n_qokch}, rate_ch={rates_mid.get('ch',0):.4f}")
e3_qckq = E3('qok', 'ch', 'qok'); n_qckq = mid_tg.get(('qok','ch','qok'), 0)
e3_pred_qckq = E2('qok','ch') * E2('ch','qok')
so_qckq = e3_qckq / e3_pred_qckq if e3_pred_qckq > 0 else 0
print(f"    qok→ch→qok: E3={e3_qckq:.3f}, E3_pred={e3_pred_qckq:.3f}, "
      f"2nd_order={so_qckq:.3f}, N={n_qckq}")
print(f"  NOTE: exp_247 2nd_order used E2(qok→ch)×E2(ch→ch_next) where 'next'=qok from RATES")
print(f"  Verify: E2(qok→ch)={e_qokch:.3f}, E2(ch→qok)={e_chqok:.3f}")
print(f"  E3_pred = {e_qokch:.3f} × {e_chqok:.3f} = {e_qokch * e_chqok:.3f}  (should match {e3_pred_qckq:.3f})")

# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 80)
print("PART 2: SECTION DISTRIBUTION OF qok→ch→qok TRIGRAMS")
print("=" * 80)

section_tg_total = Counter()
section_tg_qckq = Counter()
section_bg_qokch = Counter()
section_mid_total = Counter()
section_mid_qok = Counter()
section_mid_ch = Counter()

for fb, words in b_lines_with_folio:
    sec = get_section(fb)
    n = len(words)
    for i in range(1, n - 1):
        section_mid_total[sec] += 1
        o = get_onset(words[i])
        if o == 'qok': section_mid_qok[sec] += 1
        if o == 'ch': section_mid_ch[sec] += 1
    if n >= 4:
        for i in range(1, n - 2):
            o1, o2 = get_onset(words[i]), get_onset(words[i+1])
            if o1 == 'qok' and o2 == 'ch':
                section_bg_qokch[sec] += 1
    if n >= 5:
        for i in range(1, n - 3):
            section_tg_total[sec] += 1
            o1, o2, o3 = get_onset(words[i]), get_onset(words[i+1]), get_onset(words[i+2])
            if o1 == 'qok' and o2 == 'ch' and o3 == 'qok':
                section_tg_qckq[sec] += 1

print(f"\n  {'Section':<10}  {'qok→ch→qok':>10}  {'Total trig':>10}  {'Per 1000':>9}  "
      f"{'qok→ch':>7}  {'Ret.rate':>9}  {'qok%MID':>8}  {'ch%MID':>7}")
print(f"  {'-'*80}")
total_qokch = 0; total_qckq = 0; total_tg = 0
for sec in ['herbal', 'astro', 'cosmo', 'bio', 'other']:
    n_qckq = section_tg_qckq[sec]
    n_tg = section_tg_total[sec]
    n_qokch = section_bg_qokch[sec]
    rate = 1000 * n_qckq / n_tg if n_tg > 0 else 0
    ret = n_qckq / n_qokch if n_qokch > 0 else 0
    n_mid_sec = section_mid_total[sec]
    qok_pct = 100 * section_mid_qok[sec] / n_mid_sec if n_mid_sec > 0 else 0
    ch_pct = 100 * section_mid_ch[sec] / n_mid_sec if n_mid_sec > 0 else 0
    print(f"  {sec:<10}  {n_qckq:>10}  {n_tg:>10}  {rate:>9.2f}  "
          f"{n_qokch:>7}  {ret:>9.3f}  {qok_pct:>8.2f}%  {ch_pct:>6.2f}%")
    total_qckq += n_qckq; total_qokch += n_qokch; total_tg += n_tg

print(f"\n  GLOBAL: {total_qckq} qok→ch→qok, {total_qokch} qok→ch, "
      f"ret_rate={total_qckq/total_qokch:.3f} vs expected_qok_rate={rates_mid.get('qok',0):.3f}")
print(f"  Return enrichment: {(total_qckq/total_qokch) / rates_mid.get('qok',0):.3f}×")

# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 80)
print("PART 3: LEXICAL ANALYSIS — IS qok→ch→qok SPECIFIC WORD TRIPLES?")
print("=" * 80)

word_triple_counts = Counter()
word_pair_chqok = Counter()

for words in b_lines:
    n = len(words)
    if n >= 5:
        for i in range(1, n - 3):
            o1 = get_onset(words[i]); o2 = get_onset(words[i+1]); o3 = get_onset(words[i+2])
            if o1 == 'qok' and o2 == 'ch' and o3 == 'qok':
                word_triple_counts[(words[i], words[i+1], words[i+2])] += 1
    if n >= 4:
        for i in range(1, n - 2):
            o1 = get_onset(words[i]); o2 = get_onset(words[i+1])
            if o1 == 'ch' and o2 == 'qok':
                word_pair_chqok[(words[i], words[i+1])] += 1

total_triples = sum(word_triple_counts.values())
n_unique_triples = len(word_triple_counts)
print(f"\n  qok→ch→qok word triples: {total_triples} total, {n_unique_triples} unique")
hhi_tri = sum((c/total_triples)**2 for c in word_triple_counts.values()) if total_triples > 0 else 0
hhi_null_tri = 1 / n_unique_triples if n_unique_triples > 0 else 0
print(f"  HHI: {hhi_tri:.6f}, HHI_null: {hhi_null_tri:.6f}, HHI/null: "
      f"{hhi_tri/hhi_null_tri:.2f}×" if hhi_null_tri > 0 else "")

top5_count = sum(c for _, c in word_triple_counts.most_common(5))
print(f"  Top-5 coverage: {top5_count}/{total_triples} = {100*top5_count/total_triples:.1f}%")
print(f"\n  Top 10 qok→ch→qok word triples:")
for (w1, w2, w3), count in word_triple_counts.most_common(10):
    print(f"    {w1}→{w2}→{w3}: {count} ({100*count/total_triples:.1f}%)")

total_chqok = sum(word_pair_chqok.values())
n_unique_chqok = len(word_pair_chqok)
hhi_chqok = sum((c/total_chqok)**2 for c in word_pair_chqok.values()) if total_chqok > 0 else 0
hhi_null_chqok = 1 / n_unique_chqok if n_unique_chqok > 0 else 0
print(f"\n  ch→qok binary pairs: {total_chqok} total, {n_unique_chqok} unique")
print(f"  HHI: {hhi_chqok:.6f}, HHI/null: {hhi_chqok/hhi_null_chqok:.2f}×" if hhi_null_chqok > 0 else "")
top5_chqok = sum(c for _, c in word_pair_chqok.most_common(5))
print(f"  Top-5 coverage: {100*top5_chqok/total_chqok:.1f}%" if total_chqok > 0 else "")
print(f"  Top 5 ch→qok pairs:")
for (w1, w2), count in word_pair_chqok.most_common(5):
    print(f"    {w1}→{w2}: {count} ({100*count/total_chqok:.1f}%)")

# ─────────────────────────────────────────────────────────────────────────────
# Simulation with p_chqok parameter sweep
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 80)
print("PART 4: SIMULATION — p_chqok SWEEP (exp_236 ARCHITECTURE + ch→qok MARKOV)")
print("=" * 80)

TARGET_LINES = 2447; WINDOW = 20; SEED = 248000
P_BLIND = 0.115; P_LF = 1.0; CP = 0.55; MP = 0.90; P_QOKCH = 0.12; P_STUTTER = 0.006
R_LF = 0.12; R_MID = 0.25; MU_LEN = 8.4
EVA_CHARS = list('acdehiklmnoqrsty')

all_vms = [w for line in b_lines for w in line]
n_vms = len(all_vms)
SUFFIX_PATTERNS = ['eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy']
suf_ctr = Counter()
for w in all_vms:
    matched = False
    for suf in SUFFIX_PATTERNS:
        if w.endswith(suf): suf_ctr[suf] += 1; matched = True; break
    if not matched: suf_ctr['other'] += 1
suffix_global = {suf: c/n_vms for suf, c in suf_ctr.items()}

lf_vms = [line[0] for line in b_lines if line]
ll_vms = [line[-1] for line in b_lines if len(line) > 1]
oc_lf = Counter(get_onset(w) for w in lf_vms)
oc_ll = Counter(get_onset(w) for w in ll_vms)
onset_lf_vms = {o: c/len(lf_vms) for o, c in oc_lf.items()}
onset_ll_vms = {o: c/len(ll_vms) for o, c in oc_ll.items()}
onset_weights_mid = dict(rates_mid)

d_global = Counter(get_onset(w) for w in all_vms).get('d', 0) / n_vms
oc_ll_d = oc_ll.get('d', 0); n_ll = len(ll_vms)
d_ll_target = (oc_ll_d / n_ll) / d_global if d_global else 0
vms_ll_d_enr = onset_ll_vms.get('d', 0) / d_global if d_global else 0
d_boost = d_global * (d_ll_target - (1 - P_BLIND) * vms_ll_d_enr) / P_BLIND

def build_ll_onsets(onset_ll_vms, d_boost):
    rem = 1.0 - d_boost
    base = {o: v for o, v in onset_ll_vms.items() if o != 'd'}
    bt = sum(base.values())
    n = {o: v / bt * rem for o, v in base.items()} if bt > 0 else {}
    n['d'] = d_boost; return n

ll_onsets = build_ll_onsets(onset_ll_vms, d_boost)

def make_sup(sg, r):
    am = sg.get('am', 0); new_am = am * r; delta = am - new_am; non_am = 1 - am
    return {s: (new_am if s == 'am' else w + w / non_am * delta)
            for s, w in sg.items()} if non_am > 0 else dict(sg)

suf_lf = make_sup(suffix_global, R_LF)
suf_mid = make_sup(suffix_global, R_MID)

def make_word(onset, suffix, rng):
    if suffix.endswith('edy') or suffix.endswith('eedy'):
        return onset + rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei']) + suffix
    return onset + suffix

def rand_word(ow, sw, rng):
    o = rng.choices(list(ow), weights=list(ow.values()))[0]
    s = rng.choices(list(sw), weights=list(sw.values()))[0]
    return make_word(o, s, rng)

def cipher_lf(rng):
    o = rng.choices(list(onset_lf_vms), weights=list(onset_lf_vms.values()))[0]
    s = rng.choices(list(suf_lf), weights=list(suf_lf.values()))[0]
    return make_word(o, s, rng)

def cipher_ll(rng):
    if rng.random() < P_BLIND:
        o = rng.choices(list(ll_onsets), weights=list(ll_onsets.values()))[0]
        return o + 'am'
    o = rng.choices(list(onset_ll_vms), weights=list(onset_ll_vms.values()))[0]
    s = rng.choices(list(suffix_global), weights=list(suffix_global.values()))[0]
    return make_word(o, s, rng)

def timm_modify(word, rng):
    ol = get_onset_len(word); el = get_edy_suffix_len(word)
    ms = ol; me = len(word) - el
    if ms >= me: return rand_word(onset_weights_mid, suf_mid, rng)
    op = rng.choice(['replace', 'insert', 'delete'])
    if op == 'replace':
        pos = rng.randint(ms, me - 1); return word[:pos] + rng.choice(EVA_CHARS) + word[pos+1:]
    elif op == 'insert':
        pos = rng.randint(ms, me); return word[:pos] + rng.choice(EVA_CHARS) + word[pos:]
    else:
        if me - ms <= 1: return word[:ms] + rng.choice(EVA_CHARS) + word[ms+1:]
        pos = rng.randint(ms, me - 1); return word[:pos] + word[pos+1:]

def draw_buf(buf, prev_onset, p_chqok_val, rng):
    bl = list(buf)
    if not bl: return None
    if prev_onset == 'qok' and rng.random() < P_QOKCH:
        cw = [w for w in bl if get_onset(w) == 'ch']
        if cw: return rng.choice(cw)
    if prev_onset == 'ch' and p_chqok_val > 0 and rng.random() < p_chqok_val:
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
        if sum(1 for w in ws if w.lower() in ENGLISH_SW) / len(ws) < 0.08:
            words.extend(ws)
    return words

def run_sim_trial(latin_words, p_chqok_val, seed):
    rng = random.Random(seed)
    w = list(latin_words); rng.shuffle(w)
    lines = []; buf = deque(maxlen=WINDOW); pos = 0
    prev_onset = None; prev_word = None
    while len(lines) < TARGET_LINES and pos < len(w) - 2:
        n = max(2, min(20, round(rng.gauss(MU_LEN, 3.0))))
        chunk = w[pos:pos + n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, _ in enumerate(chunk):
            if i == 0: ew = cipher_lf(rng)
            elif i == len(chunk) - 1: ew = cipher_ll(rng)
            else:
                if prev_word and P_STUTTER > 0 and rng.random() < P_STUTTER:
                    ew = prev_word
                elif buf and rng.random() < CP:
                    src = draw_buf(buf, prev_onset, p_chqok_val, rng)
                    if src is None: src = rand_word(onset_weights_mid, suf_mid, rng)
                    ew = timm_modify(src, rng) if rng.random() < MP else src
                else:
                    ew = rand_word(onset_weights_mid, suf_mid, rng)
                buf.append(ew)
            prev_onset = get_onset(ew); prev_word = ew; line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

def sim_bigrams_trigrams(lines):
    mid_words = [line[i] for line in lines for i in range(1, len(line)-1) if len(line) >= 4]
    n_mid = len(mid_words)
    oc = Counter(get_onset(w) for w in mid_words)
    r = {o: c/n_mid for o, c in oc.items()}
    bg = Counter(); bg_n = 0
    for line in lines:
        nn = len(line)
        if nn < 4: continue
        for i in range(1, nn-2):
            bg[(get_onset(line[i]), get_onset(line[i+1]))] += 1; bg_n += 1
    tg = Counter(); tg_n = 0
    for line in lines:
        nn = len(line)
        if nn < 5: continue
        for i in range(1, nn-3):
            tg[(get_onset(line[i]), get_onset(line[i+1]), get_onset(line[i+2]))] += 1; tg_n += 1
    def sE2(x, y):
        pxy = bg.get((x,y),0)/bg_n if bg_n>0 else 0
        px=r.get(x,0); py=r.get(y,0)
        return pxy/(px*py) if px*py>0 else 0
    def sE3(x, y, z):
        pxyz = tg.get((x,y,z),0)/tg_n if tg_n>0 else 0
        px=r.get(x,0); py=r.get(y,0); pz=r.get(z,0)
        return pxyz/(px*py*pz) if px*py*pz>0 else 0
    return sE2, sE3, bg.get(('qok','ch'),0), bg.get(('ch','qok'),0), tg.get(('qok','ch','qok'),0)

print("\nLoading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
N_TRIALS = 10

SWEEP = [0.00, 0.05, 0.10, 0.15, 0.20]

# Also collect ss_qok for regression check (ss_qok is the qok→qok self-succession)
print(f"\n  Sweep p_chqok ∈ {SWEEP}, N={N_TRIALS} trials each")
print(f"\n  {'p_chqok':>8}  {'ch→qok E2':>10}  {'qok→ch E2':>10}  "
      f"{'qok→ch→qok E3':>14}  {'E3_pred':>8}  {'2nd_ord':>9}  {'qok→qok E2':>11}")
print(f"  {'---':>8}  {'---':>10}  {'---':>10}  {'---':>14}  {'---':>8}  {'---':>9}  {'---':>11}")

for p_chqok_val in SWEEP:
    trials_chqok = []; trials_qokch = []; trials_e3 = []; trials_e2_xy = []; trials_e2_yz = []
    trials_qokqok = []
    for trial in range(N_TRIALS):
        lines = run_sim_trial(latin, p_chqok_val, seed=SEED + trial * 100)
        sE2, sE3, n_qokch_sim, n_chqok_sim, n_qckq_sim = sim_bigrams_trigrams(lines)
        trials_chqok.append(sE2('ch', 'qok'))
        trials_qokch.append(sE2('qok', 'ch'))
        trials_qokqok.append(sE2('qok', 'qok'))
        e3 = sE3('qok', 'ch', 'qok')
        e2_xy = sE2('qok', 'ch'); e2_yz = sE2('ch', 'qok')
        trials_e3.append(e3)
        trials_e2_xy.append(e2_xy); trials_e2_yz.append(e2_yz)

    avg = lambda lst: sum(lst)/len(lst) if lst else 0
    e2_chqok = avg(trials_chqok)
    e2_qokch = avg(trials_qokch)
    e2_qokqok = avg(trials_qokqok)
    e3_val = avg(trials_e3)
    e3_pred = avg(trials_e2_xy) * avg(trials_e2_yz)
    so = e3_val / e3_pred if e3_pred > 0 else 0
    print(f"  {p_chqok_val:>8.2f}  {e2_chqok:>10.3f}  {e2_qokch:>10.3f}  "
          f"{e3_val:>14.3f}  {e3_pred:>8.3f}  {so:>9.3f}  {e2_qokqok:>11.3f}")

print(f"\n  VMS reference:")
e3_vms_qckq = E3('qok','ch','qok')
e3_pred_vms = E2('qok','ch') * E2('ch','qok')
so_vms = e3_vms_qckq / e3_pred_vms if e3_pred_vms > 0 else 0
print(f"    ch→qok: E2={E2('ch','qok'):.3f} (N={mid_bg.get(('ch','qok'),0)})")
print(f"    qok→ch: E2={E2('qok','ch'):.3f} (N={mid_bg.get(('qok','ch'),0)})")
print(f"    qok→ch→qok: E3={e3_vms_qckq:.3f}, E3_pred={e3_pred_vms:.3f}, 2nd_order={so_vms:.3f} (N={mid_tg.get(('qok','ch','qok'),0)})")
print(f"    qok→qok: E2={E2('qok','qok'):.3f} (N={mid_bg.get(('qok','qok'),0)})")

print("\n  INTERPRETATION: Does adding p_chqok fix the 2nd_order gap?")
print(f"  Target 2nd_order: VMS={so_vms:.3f}; Baseline (p=0): ? (from table above)")
print(f"  If sim 2nd_order rises toward {so_vms:.3f} with p_chqok > 0 → mechanism viable")
print(f"  If sim qok→ch E2 drops significantly → regression risk")
print(f"  VMS ss_qok (qok→qok E2): {E2('qok','qok'):.3f} — check for regression in this")

print("\nDone.")
