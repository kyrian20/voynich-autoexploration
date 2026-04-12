"""
exp_308: Menzerath r Component Decomposition — LF/LL vs MID Contribution (H510)

exp_307 showed bio section MID slope already matched (106%) but Menzerath r is 2×
simulation (−0.208 vs −0.109). This means Menzerath r has components beyond MID slope.

H510: LF/LL word length scales with line length in VMS (long lines have longer
LF words or shorter LL words), creating additional Menzerath r that the simulation
misses because cipher_lf/cipher_ll don't condition on line length.

This experiment:
  1. Decomposes VMS Menzerath r into LF, MID, LL components
  2. Computes r(line_len, LF_word_len) and r(line_len, LL_word_len) by section
  3. Compares to simulation (exp_306 architecture, beta=0.50) output
  4. Multiple regression: what fraction of VMS Menzerath r is explained by each component?
  5. Tests whether LF word length increases or LL word length decreases with line length
"""

import os, re, random, math
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser('~/voynich-cryptanalyst')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

# Simulation architecture (exp_306, beta=0.50, 17 mechanisms)
P_BLIND=0.115; P_LF=1.0; CP=0.55; MP=0.90; P_QOKCH=0.12; P_CHQOK=0.12; P_STUTTER=0.006
R_LF=0.12; R_MID=0.20; MU_LEN=8.4; SIGMA_LEN=3.0; P_MF=0.20; P_LF_MF=0.50; P_LL_MF=0.00
GAMMA=0.30; ALPHA=0.20; BETA=0.50
IDX_THRESH=2; SHORT_THRESH=2; TARGET_LINES=2411; WINDOW=20; SEED=308000

L_BASE=5.40; L_SLOPE=-0.053
SHORT_ONSETS={'d','s','y','k','t','l','r','p','f','o'}
EVA_CHARS=list('acdehiklmnoqrsty')

ONSET_ORDER=[
    ('qok','qok'),('qot','qot'),('qo','qo'),('cth','cth'),
    ('ch','ch'),('sh','sh'),('ok','ok'),('ot','ot'),('ol','ol'),
    ('d','d'),('s','s'),('y','y'),('k','k'),('t','t'),
    ('l','l'),('r','r'),('p','p'),('f','f'),('o','o'),
]
SUFFIX_PATTERNS=['eedy','edy','aiin','ain','am','ey','ol','or','al','ar','dy']
SPARSE_ONSETS={'qok','ok','ot','qot'}

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label
    return 'other'
def get_onset_len(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return len(prefix)
    return 0
def get_suffix(w):
    for s in SUFFIX_PATTERNS:
        if w.endswith(s): return s
    return 'other'
def get_edy_suffix_len(w):
    if w.endswith('eedy'): return 4
    if w.endswith('edy'):  return 3
    return 0
def folio_base(folio): return re.sub(r'[rv]$', '', folio)
def folio_num(fb):
    try: return int(re.sub(r'[^0-9]', '', fb))
    except: return 0
def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    return 'B' if (stats['edy']+stats['eedy'])/total >= 0.05 else 'A'

def pearson_r(xs, ys):
    n = len(xs)
    if n < 3: return float('nan')
    mx = sum(xs)/n; my = sum(ys)/n
    cov = sum((x-mx)*(y-my) for x,y in zip(xs,ys))/n
    sx = (sum((x-mx)**2 for x in xs)/n)**0.5
    sy = (sum((y-my)**2 for y in ys)/n)**0.5
    if sx*sy == 0: return float('nan')
    return cov/(sx*sy)

def assign_section(fn):
    if fn<=57: return 'herbal'
    elif fn<=73: return 'astro'
    elif fn<=84: return 'bio'
    elif fn<=87: return 'cosmo'
    elif fn<=102: return 'pharma'
    elif fn<=116: return 'stars'
    else: return 'text'

def parse_vms_b():
    folio_word_stats = defaultdict(lambda: {'total':0,'edy':0,'eedy':0})
    with open(DATA_PATH,'r',encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line or line.startswith('#'): continue
            m=re.match(r'<([^.]+)\.(\d+),([^>]+)>',line)
            if not m: continue
            folio=m.group(1).lstrip('+*=&~'); fb=folio_base(folio)
            text=re.sub(r'<[^>]+>','',line)
            words=[w for w in re.split(r'[-.\s]',text) if re.match(r'^[a-z]+$',w) and len(w)>=2]
            for w in words:
                folio_word_stats[fb]['total']+=1
                if w.endswith('eedy'): folio_word_stats[fb]['eedy']+=1
                elif w.endswith('edy'): folio_word_stats[fb]['edy']+=1
    folio_dialect={fb:classify_dialect(stats) for fb,stats in folio_word_stats.items()}
    b_lines=[]; section_lines=defaultdict(list)
    with open(DATA_PATH,'r',encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line or line.startswith('#'): continue
            m=re.match(r'<([^.]+)\.(\d+),([^>]+)>',line)
            if not m: continue
            folio_raw=m.group(1); locus_code=m.group(3)
            folio=folio_raw.lstrip('+*=&~'); fb=folio_base(folio)
            if folio_dialect.get(fb,'unknown')!='B': continue
            lc_stripped=locus_code.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            text=re.sub(r'<[^>]+>','',line)
            words=[w for w in re.split(r'[-.\s]',text) if re.match(r'^[a-z]+$',w) and len(w)>=2]
            if not words: continue
            fn=folio_num(fb); section=assign_section(fn)
            b_lines.append(words); section_lines[section].append(words)
    return b_lines, section_lines

def compute_component_correlations(lines, min_len=3):
    """Compute r(line_len, LF_wl), r(line_len, mean_MID_wl), r(line_len, LL_wl) for a set of lines."""
    data = []
    for l in lines:
        if len(l) < min_len: continue
        ll_n = len(l)
        lf_wl = len(l[0])
        ll_wl = len(l[-1])
        mid_words = l[1:-1] if len(l) > 2 else []
        mid_wl = sum(len(w) for w in mid_words)/len(mid_words) if mid_words else float('nan')
        mean_wl = sum(len(w) for w in l)/ll_n
        data.append((ll_n, lf_wl, mid_wl, ll_wl, mean_wl))
    if len(data) < 5:
        return {'n': len(data), 'r_total': float('nan'), 'r_lf': float('nan'),
                'r_mid': float('nan'), 'r_ll': float('nan'),
                'mean_lf_wl': float('nan'), 'mean_mid_wl': float('nan'), 'mean_ll_wl': float('nan'),
                'mid_slope': float('nan')}
    xs = [d[0] for d in data]
    lf_wls = [d[1] for d in data]
    mid_wls = [d[2] for d in data if not math.isnan(d[2])]
    mid_xs = [d[0] for d in data if not math.isnan(d[2])]
    ll_wls = [d[3] for d in data]
    mean_wls = [d[4] for d in data]
    r_total = pearson_r(xs, mean_wls)
    r_lf = pearson_r(xs, lf_wls)
    r_mid = pearson_r(mid_xs, mid_wls) if len(mid_wls) >= 3 else float('nan')
    r_ll = pearson_r(xs, ll_wls)
    # MID slope (word_len vs position within line)
    idx_lens = []
    for l in lines:
        if len(l) < 4: continue
        for j, w in enumerate(l[1:-1]): idx_lens.append((j, len(w)))
    if len(idx_lens) > 50:
        n_il = len(idx_lens)
        mean_idx = sum(x for x,y in idx_lens)/n_il
        mean_len = sum(y for x,y in idx_lens)/n_il
        cov_il = sum((x-mean_idx)*(y-mean_len) for x,y in idx_lens)/n_il
        var_il = sum((x-mean_idx)**2 for x,y in idx_lens)/n_il
        mid_slope = cov_il/var_il if var_il > 0 else 0
    else:
        mid_slope = float('nan')
    return {
        'n': len(data),
        'r_total': r_total, 'r_lf': r_lf, 'r_mid': r_mid, 'r_ll': r_ll,
        'mean_lf_wl': sum(lf_wls)/len(lf_wls),
        'mean_mid_wl': sum(mid_wls)/len(mid_wls) if mid_wls else float('nan'),
        'mean_ll_wl': sum(ll_wls)/len(ll_wls),
        'mid_slope': mid_slope,
    }

# ─── VMS analysis ───────────────────────────────────────────────────────────────
print("exp_308: Menzerath r Component Decomposition — LF/LL vs MID Contribution (H510)")
print("=" * 70)

print("\nParsing VMS B-dialect...")
all_b_lines, section_lines = parse_vms_b()
print(f"  Total: {len(all_b_lines)} lines")

print(f"\n{'='*70}")
print("VMS Component Correlations: r(line_len, [LF|MID|LL]_word_len)")
print(f"{'='*70}")
print(f"\n{'Section':10s}  {'N':6s}  {'r_total':8s}  {'r_lf':8s}  {'r_mid':8s}  {'r_ll':8s}  {'MID_slope':10s}")
print("-" * 75)

section_comp = {}
for section in ['overall', 'stars', 'bio', 'herbal', 'astro', 'pharma', 'text']:
    lines = all_b_lines if section == 'overall' else section_lines.get(section, [])
    if not lines: continue
    comp = compute_component_correlations(lines)
    section_comp[section] = comp
    rt = comp['r_total']; rlf = comp['r_lf']; rm = comp['r_mid']; rll = comp['r_ll']
    ms = comp['mid_slope']
    print(f"{section:10s}  {comp['n']:6d}  {rt:+8.4f}  {rlf:+8.4f}  {rm:+8.4f}  {rll:+8.4f}  {ms:+10.4f}")

# ─── Mean word length by position-class and line length bucket ───────────────
print(f"\n{'='*70}")
print("Mean LF/MID/LL Word Length by Line Length Bucket (VMS overall)")
print(f"{'='*70}")
# Bucket lines by length
bucket_data = defaultdict(lambda: {'lf': [], 'mid': [], 'll': []})
for l in all_b_lines:
    if len(l) < 3: continue
    ln = len(l)
    bucket = (ln // 3) * 3  # 3-5, 6-8, 9-11, 12-14, 15+
    bucket_data[bucket]['lf'].append(len(l[0]))
    if len(l) > 2: bucket_data[bucket]['mid'].extend(len(w) for w in l[1:-1])
    bucket_data[bucket]['ll'].append(len(l[-1]))

print(f"\n{'Bucket':10s}  {'N_lines':8s}  {'LF_wl':7s}  {'MID_wl':7s}  {'LL_wl':7s}  {'Mean_wl':8s}")
print("-" * 55)
all_lines_by_len = []
for l in all_b_lines:
    if len(l) >= 3:
        mean_wl = sum(len(w) for w in l)/len(l)
        all_lines_by_len.append((len(l), len(l[0]),
                                  sum(len(w) for w in l[1:-1])/len(l[1:-1]) if len(l)>2 else float('nan'),
                                  len(l[-1]), mean_wl))

# Create line-length buckets
buckets = [(2,4), (5,6), (7,8), (9,10), (11,15), (16,25)]
for lo, hi in buckets:
    subset = [x for x in all_lines_by_len if lo <= x[0] <= hi]
    if not subset: continue
    n = len(subset)
    lf_wl = sum(x[1] for x in subset)/n
    mid_wls = [x[2] for x in subset if not math.isnan(x[2])]
    mid_wl = sum(mid_wls)/len(mid_wls) if mid_wls else float('nan')
    ll_wl = sum(x[3] for x in subset)/n
    mean_wl = sum(x[4] for x in subset)/n
    label = f"LL={lo}-{hi}"
    print(f"{label:10s}  {n:8d}  {lf_wl:7.3f}  {mid_wl:7.3f}  {ll_wl:7.3f}  {mean_wl:8.3f}")

# ─── Run simulation for comparison ──────────────────────────────────────────────
print(f"\n{'='*70}")
print(f"Simulation Component Correlations (exp_306 architecture, N=30, SEED={SEED})")
print(f"{'='*70}")

# Simplified simulation run (import key functions inline)
def build_midfix_dist(words):
    midfix_cnt = Counter()
    for w in words:
        onset=get_onset(w); suf=get_suffix(w)
        if onset=='other' or suf=='other': continue
        onset_len=get_onset_len(w); suf_len=len(suf)
        if (edy_len:=get_edy_suffix_len(w)):
            mid_end=len(w)-edy_len; midfix=w[onset_len:mid_end]
            if len(midfix)>=1: midfix=midfix[:-1]
        else:
            midfix=w[onset_len:len(w)-suf_len]
        midfix_cnt[midfix]+=1
    total=sum(midfix_cnt.values())
    if total==0: return {},0.0
    p_non_empty=sum(v for k,v in midfix_cnt.items() if k!='')/total
    non_empty_raw={mf:v for mf,v in midfix_cnt.items() if mf!=''}
    non_empty_total=sum(non_empty_raw.values())
    return {mf:v/non_empty_total for mf,v in non_empty_raw.items()} if non_empty_total else {},p_non_empty

def weighted_choice(rng, dist):
    r=rng.random(); cum=0.0
    for k,v in dist.items():
        cum+=v
        if r<cum: return k
    return list(dist.keys())[-1]

def make_word_sim(onset, suffix, rng, nemed, p_mf):
    midfix=''
    if nemed and rng.random()<p_mf: midfix=weighted_choice(rng,nemed)
    if suffix.endswith('edy') or suffix.endswith('eedy'):
        return onset+midfix+rng.choice(['a','ai','o','oi','e','ei'])+suffix
    return onset+midfix+suffix

def apply_suffix_length_bias(suf_w, word_idx, beta):
    if beta==0.0 or word_idx<IDX_THRESH: return suf_w
    new_w={}
    for suf,w in suf_w.items():
        suf_len=len(suf) if suf!='other' else 5
        penalty=max(0,suf_len-SHORT_THRESH)
        new_w[suf]=w*math.exp(-beta*penalty)
    total=sum(new_w.values())
    return {s:v/total for s,v in new_w.items()} if total>0 else suf_w

def timm_modify(word, onset_mid, suffix_mid, rng):
    if not word: return word
    onset_len=get_onset_len(word); edy_len=get_edy_suffix_len(word)
    mod_start=onset_len; mod_end=len(word)-edy_len
    if mod_start>=mod_end:
        return make_word_sim(weighted_choice(rng,onset_mid),weighted_choice(rng,suffix_mid),rng,{},0.0)
    op=rng.choice(['replace','insert','delete'])
    if op=='replace':
        pos=rng.randint(mod_start,mod_end-1)
        return word[:pos]+rng.choice(EVA_CHARS)+word[pos+1:]
    elif op=='insert':
        pos=rng.randint(mod_start,mod_end)
        return word[:pos]+rng.choice(EVA_CHARS)+word[pos:]
    else:
        if mod_end-mod_start<=1:
            return word[:mod_start]+rng.choice(EVA_CHARS)+word[mod_start+1:]
        pos=rng.randint(mod_start,mod_end-1)
        return word[:pos]+word[pos+1:]

def clamp_to_lexicon(word, lexicons, rng):
    onset=get_onset(word)
    if onset in lexicons and lexicons[onset]: return rng.choice(lexicons[onset])
    return word

def draw_buf_length_biased(buf, prev_onset, rng, word_idx):
    buf_list=list(buf)
    if not buf_list: return None
    preferred=None
    if prev_onset=='qok' and rng.random()<P_QOKCH:
        ch_words=[w for w in buf_list if get_onset(w)=='ch']
        if ch_words: preferred=ch_words
    elif prev_onset=='ch' and rng.random()<P_CHQOK:
        qok_words=[w for w in buf_list if get_onset(w)=='qok']
        if qok_words: preferred=qok_words
    candidates=preferred if preferred else buf_list
    if GAMMA==0.0: return rng.choice(candidates)
    L_target=L_BASE+L_SLOPE*word_idx
    weights=[math.exp(-GAMMA*(len(w)-L_target)**2) for w in candidates]
    total=sum(weights)
    if total==0: return rng.choice(candidates)
    r=rng.random()*total; cum=0.0
    for w,wt in zip(candidates,weights):
        cum+=wt
        if r<cum: return w
    return candidates[-1]

ENGLISH_SW={'the','and','of','to','a','in','that','is','was','he','it','for','on','are',
            'as','with','his','they','at','be','this','have','from','or','had','by','not',
            'but','what','all','were','we'}
def load_latin(path):
    with open(path,encoding='utf-8',errors='replace') as f: text=f.read()
    words=[]
    for p in re.split(r'\n\s*\n',text):
        ws=re.findall(r'\b[a-zA-Z]+\b',p)
        if not ws: continue
        if sum(1 for w in ws if w.lower() in ENGLISH_SW)/len(ws)<0.08: words.extend(ws)
    return words

def make_suppressed_suffix(suffix_global, r_am):
    am_w=suffix_global.get('am',0); new_am=am_w*r_am
    delta=am_w-new_am; non_am=1.0-am_w
    return {suf:(new_am if suf=='am' else w+(w/non_am)*delta if non_am>0 else w)
            for suf,w in suffix_global.items()}

def build_full_vms_lexicons(mid_words, onset_classes):
    lexicons={}; per_onset_counts=defaultdict(Counter)
    for w in mid_words:
        onset=get_onset(w)
        if onset in onset_classes: per_onset_counts[onset][w]+=1
    for onset in onset_classes:
        counts=per_onset_counts[onset]; lex_list=[]
        for w,c in counts.items(): lex_list.extend([w]*c)
        lexicons[onset]=lex_list
    return lexicons

def compute_vms_dists(b_lines):
    all_words=[w for l in b_lines for w in l]
    lf_words=[l[0] for l in b_lines if l]
    ll_words=[l[-1] for l in b_lines if len(l)>1]
    mid_words=[w for l in b_lines for w in l[1:-1] if len(l)>2]
    def build_onset(words):
        cnt=Counter(get_onset(w) for w in words); cnt.pop('other',None)
        total=sum(cnt.values())
        return {k:v/total for k,v in cnt.items()} if total else {}
    def build_suffix(words):
        cnt=Counter(get_suffix(w) for w in words); total=sum(cnt.values())
        return {k:v/total for k,v in cnt.items()} if total else {}
    onset_lf=build_onset(lf_words); onset_ll=build_onset(ll_words); onset_mid=build_onset(mid_words)
    suffix_global=build_suffix(all_words)
    mid_nemed,mid_p=build_midfix_dist(mid_words)
    lf_nemed,lf_p=build_midfix_dist(lf_words)
    ll_nemed,ll_p=build_midfix_dist(ll_words)
    d_global=Counter(get_onset(w) for w in all_words).get('d',0)/len(all_words)
    d_r=d_global
    ll_d=Counter(get_onset(w) for w in ll_words).get('d',0)/len(ll_words)
    d_ll_target=ll_d/d_r if d_r else 0
    d_ll_non_blind_enr=onset_ll.get('d',0)/d_r if d_r else 0
    d_boost_weight=d_r*(d_ll_target-(1-P_BLIND)*d_ll_non_blind_enr)/P_BLIND
    d_boost_weight=max(0.0,min(d_boost_weight,1.0))
    remaining=1.0-d_boost_weight
    base={o:v for o,v in onset_ll.items() if o!='d'}
    base_total=sum(base.values())
    ll_onsets={o:v/base_total*remaining for o,v in base.items()} if base_total else {}
    ll_onsets['d']=d_boost_weight
    return {'onset_lf':onset_lf,'onset_ll':onset_ll,'onset_mid':onset_mid,
            'suffix_global':suffix_global,'mid_nemed':mid_nemed,'lf_nemed':lf_nemed,
            'll_nemed':ll_nemed,'ll_onsets':ll_onsets,'mid_words':mid_words}

print("\nBuilding simulation distributions...")
vms_d=compute_vms_dists(all_b_lines)
latin_words=load_latin(LATIN_CORPUS)
print(f"  {len(latin_words)} Latin words loaded")

suffix_lf_sup=make_suppressed_suffix(vms_d['suffix_global'],R_LF)
suffix_mid_sup=make_suppressed_suffix(vms_d['suffix_global'],R_MID)
lexicons=build_full_vms_lexicons(vms_d['mid_words'],SPARSE_ONSETS)

def run_sim_lines(latin_words, vms_d, rng, n_trials=10):
    """Run simulation and collect all lines from all trials."""
    all_lines=[]
    for _ in range(n_trials):
        w=list(latin_words); rng.shuffle(w)
        lines=[]; buf=deque(maxlen=WINDOW); pos=0
        prev_onset=None; prev_word=None
        while len(lines)<TARGET_LINES and pos<len(w)-2:
            n=max(2,min(20,round(rng.gauss(MU_LEN,SIGMA_LEN))))
            chunk=w[pos:pos+n]
            if len(chunk)<2: pos+=len(chunk); continue
            line=[]; word_idx=0
            for i,word in enumerate(chunk):
                if i==0:
                    # LF
                    if rng.random()<P_LF:
                        onset=weighted_choice(rng,vms_d['onset_lf'])
                        suf=weighted_choice(rng,suffix_lf_sup)
                        ew=make_word_sim(onset,suf,rng,vms_d['lf_nemed'],P_LF_MF)
                    else:
                        onset=weighted_choice(rng,vms_d['onset_mid'])
                        suf=weighted_choice(rng,suffix_lf_sup)
                        ew=make_word_sim(onset,suf,rng,{},0.0)
                elif i==len(chunk)-1:
                    # LL
                    if rng.random()<P_BLIND:
                        onset=weighted_choice(rng,vms_d['ll_onsets'])
                        ew=onset+'am'
                    else:
                        onset=weighted_choice(rng,vms_d['onset_ll'])
                        suf=weighted_choice(rng,vms_d['suffix_global'])
                        ew=make_word_sim(onset,suf,rng,vms_d['ll_nemed'],P_LL_MF)
                else:
                    if prev_word is not None and rng.random()<P_STUTTER:
                        ew=prev_word
                    elif buf and rng.random()<CP:
                        src=draw_buf_length_biased(buf,prev_onset,rng,word_idx)
                        if src is None: src=rng.choice(list(buf))
                        if rng.random()<MP:
                            ew=timm_modify(src,vms_d['onset_mid'],suffix_mid_sup,rng)
                            ew=clamp_to_lexicon(ew,lexicons,rng)
                        else:
                            ew=src
                    else:
                        new_ow={o:v*(1+ALPHA*word_idx) if o in SHORT_ONSETS else v
                                for o,v in vms_d['onset_mid'].items()}
                        tot=sum(new_ow.values())
                        norm={o:v/tot for o,v in new_ow.items()} if tot else vms_d['onset_mid']
                        onset=weighted_choice(rng,norm)
                        biased_suf=apply_suffix_length_bias(suffix_mid_sup,word_idx,BETA)
                        suf=weighted_choice(rng,biased_suf)
                        ew=make_word_sim(onset,suf,rng,vms_d['mid_nemed'],P_MF)
                        ew=clamp_to_lexicon(ew,lexicons,rng)
                    buf.append(ew); word_idx+=1
                prev_onset=get_onset(ew); prev_word=ew; line.append(ew)
            lines.append(line); pos+=n
        all_lines.extend(lines[:TARGET_LINES])
    return all_lines

rng=random.Random(SEED)
print(f"Running simulation (N=10 trials)...")
sim_lines=run_sim_lines(latin_words,vms_d,rng,n_trials=10)
print(f"  {len(sim_lines)} total simulated lines")

sim_comp=compute_component_correlations(sim_lines)
print(f"\nSimulation component correlations (pooled N=10 trials):")
print(f"  r_total: {sim_comp['r_total']:+.4f}  (VMS overall: {section_comp.get('overall',{}).get('r_total',float('nan')):+.4f})")
print(f"  r_lf:    {sim_comp['r_lf']:+.4f}  (VMS overall: {section_comp.get('overall',{}).get('r_lf',float('nan')):+.4f})")
print(f"  r_mid:   {sim_comp['r_mid']:+.4f}  (VMS overall: {section_comp.get('overall',{}).get('r_mid',float('nan')):+.4f})")
print(f"  r_ll:    {sim_comp['r_ll']:+.4f}  (VMS overall: {section_comp.get('overall',{}).get('r_ll',float('nan')):+.4f})")
print(f"  MID_slope: {sim_comp['mid_slope']:+.4f}  (VMS: {section_comp.get('overall',{}).get('mid_slope',float('nan')):+.4f})")

# Mean word lengths by position class
print(f"\nMean word lengths by position class:")
print(f"  {'':10s}  {'LF_wl':7s}  {'MID_wl':7s}  {'LL_wl':7s}")
print(f"  {'VMS':10s}  {section_comp.get('overall',{}).get('mean_lf_wl',0):7.3f}  "
      f"{section_comp.get('overall',{}).get('mean_mid_wl',0):7.3f}  "
      f"{section_comp.get('overall',{}).get('mean_ll_wl',0):7.3f}")
print(f"  {'Sim':10s}  {sim_comp.get('mean_lf_wl',0):7.3f}  "
      f"{sim_comp.get('mean_mid_wl',0):7.3f}  "
      f"{sim_comp.get('mean_ll_wl',0):7.3f}")

# Sim line-length vs word-length bucket
print(f"\nSimulation word lengths by line length bucket:")
sim_by_len=[]
for l in sim_lines:
    if len(l)>=3:
        sim_by_len.append((len(l), len(l[0]),
                           sum(len(w) for w in l[1:-1])/len(l[1:-1]) if len(l)>2 else float('nan'),
                           len(l[-1]), sum(len(w) for w in l)/len(l)))

print(f"\n{'Bucket':10s}  {'N_lines':8s}  {'LF_wl':7s}  {'MID_wl':7s}  {'LL_wl':7s}  {'Mean_wl':8s}")
print("-" * 55)
for lo,hi in [(2,4),(5,6),(7,8),(9,10),(11,15),(16,25)]:
    subset=[x for x in sim_by_len if lo<=x[0]<=hi]
    if not subset: continue
    n=len(subset)
    lf_wl=sum(x[1] for x in subset)/n
    mid_wls=[x[2] for x in subset if not math.isnan(x[2])]
    mid_wl=sum(mid_wls)/len(mid_wls) if mid_wls else float('nan')
    ll_wl=sum(x[3] for x in subset)/n
    mean_wl=sum(x[4] for x in subset)/n
    label=f"LL={lo}-{hi}"
    print(f"{label:10s}  {n:8d}  {lf_wl:7.3f}  {mid_wl:7.3f}  {ll_wl:7.3f}  {mean_wl:8.3f}")

print("\nDone.")
