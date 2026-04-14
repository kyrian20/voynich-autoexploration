#!/usr/bin/env python3
"""
exp_582: Battery Correlation Matrix for 19-Metric Battery

Generates N=200 independent simulation runs of the 21-mechanism architecture
at exp_314 parameters (beta_scale=1.8). Computes 19×19 Pearson correlation
matrix, PCA effective dimension, and clustering analysis.

Question: What is the effective number of independent constraints measured
by the 19-metric battery?

Methods:
1. N=200 simulation trials at exp_314/21-mechanism parameters
2. Each trial: 2411 lines → 19 metric values
3. 19×19 Pearson correlation matrix
4. PCA: components needed for 95% variance explained
5. Clustering at |r|≥0.7 (count clusters+singletons)
6. Also report |r|≥0.5 cluster structure
"""

import os, re, random, math, csv
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser('~/voynich-cryptanalyst')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

# ─── 21-mechanism architecture parameters (exp_314, beta_scale=1.8) ───────────
P_SHORT=0.060; P_LONG=0.180; THRESH_SHORT=5; THRESH_LONG=10; MEAN_N=8.4
P_LF=1.0; CP=0.55; MP=0.90; P_QOKCH=0.12; P_CHQOK=0.12; P_STUTTER=0.006
R_LF=0.12; R_MID=0.20; MU_LEN=8.4; SIGMA_LEN=3.0; P_MF=0.20; P_LF_MF=0.50; P_LL_MF=0.00
GAMMA=0.30; ALPHA=0.20
BETA_BASE=0.50; BETA_SCALE=1.8  # 21st mechanism: scale_1.8
IDX_THRESH=2; SHORT_THRESH=2; TARGET_LINES=2411; WINDOW=20
SEED=582000; N_TRIALS=200
MAX_RETRY=10

# LL word-len filter parameters (19th mechanism)
LL_BASE=8; LL_SLOPE=0.30; LL_N_REF=5; LL_MIN_CAP=3

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

BATTERY_19=['am_ll','d_ll','y_lf','ss_mean','adj_rate','qok_lf','d_lf','s_lf',
            'ch_ll','ok_ll','qok_ll','ss_d','ss_y','am_lf_enr','am_mid_enr',
            'edy_rate','word_len_mean','qok_ch','global_am_rate']

# ─── Utility functions ─────────────────────────────────────────────────────────
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

def classify_dialect(stats):
    total=stats['total']
    if total==0: return 'unknown'
    return 'B' if (stats['edy']+stats['eedy'])/total>=0.05 else 'A'

# ─── Corpus parsing ────────────────────────────────────────────────────────────
def parse_vms_b():
    folio_word_stats=defaultdict(lambda:{'total':0,'edy':0,'eedy':0})
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
    b_lines=[]
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
            if words: b_lines.append(words)
    return b_lines

# ─── Distribution building ─────────────────────────────────────────────────────
def build_midfix_dist(words):
    midfix_cnt=Counter()
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
    ll_d=Counter(get_onset(w) for w in ll_words).get('d',0)/len(ll_words)
    d_ll_target=ll_d/d_global if d_global else 0
    d_ll_non_blind_enr=onset_ll.get('d',0)/d_global if d_global else 0
    d_boost=d_global*(d_ll_target-(1-0.115)*d_ll_non_blind_enr)/0.115
    d_boost=max(0.0,min(d_boost,1.0))
    remaining=1.0-d_boost
    base={o:v for o,v in onset_ll.items() if o!='d'}
    base_total=sum(base.values())
    ll_onsets={o:v/base_total*remaining for o,v in base.items()} if base_total else {}
    ll_onsets['d']=d_boost
    return {'onset_lf':onset_lf,'onset_ll':onset_ll,'onset_mid':onset_mid,
            'suffix_global':suffix_global,'mid_nemed':mid_nemed,'lf_nemed':lf_nemed,
            'll_nemed':ll_nemed,'ll_onsets':ll_onsets,'mid_words':mid_words,'d_boost':d_boost}

# ─── Simulation utilities ──────────────────────────────────────────────────────
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

def draw_buf(buf, prev_onset, rng, word_idx):
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

def make_suppressed_suffix(sg, r_am):
    am_w=sg.get('am',0); new_am=am_w*r_am; delta=am_w-new_am; non_am=1.0-am_w
    return {suf:(new_am if suf=='am' else w+(w/non_am)*delta if non_am>0 else w)
            for suf,w in sg.items()}

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

def get_p_blind_n(n):
    if n<=THRESH_SHORT: return P_SHORT
    if n>=THRESH_LONG: return P_LONG
    frac=(n-THRESH_SHORT)/(THRESH_LONG-THRESH_SHORT)
    return P_SHORT+frac*(P_LONG-P_SHORT)

def get_max_ll_len(n):
    return max(LL_MIN_CAP, round(LL_BASE - LL_SLOPE * max(0, n - LL_N_REF)))

def generate_ll_word(rng, vms_d, suffix_global, max_ll):
    candidates=[]
    for _ in range(MAX_RETRY+1):
        onset=weighted_choice(rng,vms_d['onset_ll'])
        suf=weighted_choice(rng,suffix_global)
        ew=make_word_sim(onset,suf,rng,vms_d['ll_nemed'],P_LL_MF)
        if len(ew)<=max_ll: return ew
        candidates.append(ew)
    return min(candidates,key=len)

# ─── Core simulation ───────────────────────────────────────────────────────────
def run_sim(latin_words, vms_d, rng, suffix_lf_sup, suffix_mid_sup, lexicons):
    """Run N_TRIALS simulation trials; return list of (N_TRIALS * TARGET_LINES) lines."""
    all_lines=[]
    for trial_idx in range(N_TRIALS):
        if trial_idx % 20 == 0:
            print(f"  Trial {trial_idx}/{N_TRIALS}...")
        w=list(latin_words); rng.shuffle(w)
        lines=[]; buf=deque(maxlen=WINDOW); pos=0
        prev_onset=None; prev_word=None
        while len(lines)<TARGET_LINES and pos<len(w)-2:
            n=max(2,min(20,round(rng.gauss(MU_LEN,SIGMA_LEN))))
            chunk=w[pos:pos+n]
            if len(chunk)<2: pos+=len(chunk); continue
            line=[]; word_idx=0
            p_blind_n=get_p_blind_n(n)
            max_ll=get_max_ll_len(n)
            beta_eff=BETA_BASE*BETA_SCALE*(n/MEAN_N)
            for i,word in enumerate(chunk):
                if i==0:
                    if rng.random()<P_LF:
                        onset=weighted_choice(rng,vms_d['onset_lf'])
                        suf=weighted_choice(rng,suffix_lf_sup)
                        ew=make_word_sim(onset,suf,rng,vms_d['lf_nemed'],P_LF_MF)
                    else:
                        onset=weighted_choice(rng,vms_d['onset_mid'])
                        suf=weighted_choice(rng,suffix_lf_sup)
                        ew=make_word_sim(onset,suf,rng,{},0.0)
                elif i==len(chunk)-1:
                    if rng.random()<p_blind_n:
                        onset=weighted_choice(rng,vms_d['ll_onsets'])
                        ew=onset+'am'
                    else:
                        ew=generate_ll_word(rng,vms_d,vms_d['suffix_global'],max_ll)
                else:
                    if prev_word is not None and rng.random()<P_STUTTER:
                        ew=prev_word
                    elif buf and rng.random()<CP:
                        src=draw_buf(buf,prev_onset,rng,word_idx)
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
                        biased_suf=apply_suffix_length_bias(suffix_mid_sup,word_idx,beta_eff)
                        suf=weighted_choice(rng,biased_suf)
                        ew=make_word_sim(onset,suf,rng,vms_d['mid_nemed'],P_MF)
                        ew=clamp_to_lexicon(ew,lexicons,rng)
                    buf.append(ew); word_idx+=1
                prev_onset=get_onset(ew); prev_word=ew; line.append(ew)
            lines.append(line); pos+=n
        # Pad if needed (shouldn't happen with large enough corpus)
        all_lines.extend(lines[:TARGET_LINES])
    return all_lines

# ─── Metric computation ────────────────────────────────────────────────────────
def pearson_r(xs, ys):
    n=len(xs)
    if n<3: return float('nan')
    mx=sum(xs)/n; my=sum(ys)/n
    cov=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/n
    sx=(sum((x-mx)**2 for x in xs)/n)**0.5
    sy=(sum((y-my)**2 for y in ys)/n)**0.5
    if sx*sy==0: return float('nan')
    return cov/(sx*sy)

def compute_metrics_per_trial(all_lines):
    """Compute 19 metrics per trial; return list of dicts (one per trial)."""
    trial_metrics=[]
    for t in range(N_TRIALS):
        lines=all_lines[t*TARGET_LINES:(t+1)*TARGET_LINES]
        aw=[w for l in lines for w in l]; n_aw=len(aw)
        if n_aw<100: continue
        lf=[l[0] for l in lines if l]
        ll=[l[-1] for l in lines if len(l)>1]
        mid=[w for l in lines for w in l[1:-1] if len(l)>2]
        oc_all=Counter(get_onset(w) for w in aw)
        oc_lf=Counter(get_onset(w) for w in lf)
        oc_ll=Counter(get_onset(w) for w in ll)
        n_lf=len(lf); n_ll=len(ll); n_mid=len(mid)

        def enr(onset,ctr,ns):
            s=ctr.get(onset,0)/ns if ns else 0
            g=oc_all.get(onset,0)/n_aw if n_aw else 0
            return s/g if g>0 else 0

        am_r=sum(1 for w in aw if w.endswith('am'))/n_aw
        ll_am=sum(1 for w in ll if w.endswith('am'))/n_ll if n_ll else 0
        am_ll=ll_am/am_r if am_r else 0
        d_ll=enr('d',oc_ll,n_ll); y_lf=enr('y',oc_lf,n_lf)

        tb=n_aw-1
        bg=Counter((get_onset(aw[i]),get_onset(aw[i+1])) for i in range(tb))
        def ss(o):
            b=oc_all.get(o,0)/n_aw
            return bg.get((o,o),0)/(tb*b*b) if b>0 and tb>0 else 1.0

        ss_mean=(ss('qok')+ss('ok')+ss('ch'))/3
        adj=sum(1 for i in range(tb) if aw[i]==aw[i+1])/max(1,tb)
        qok_lf=enr('qok',oc_lf,n_lf); d_lf=enr('d',oc_lf,n_lf)
        s_lf=enr('s',oc_lf,n_lf); ch_ll=enr('ch',oc_ll,n_ll)
        ok_ll=enr('ok',oc_ll,n_ll); qok_ll=enr('qok',oc_ll,n_ll)
        ss_d=ss('d'); ss_y=ss('y')
        lf_am_rate=sum(1 for w in lf if w.endswith('am'))/n_lf if n_lf else 0
        mid_am_rate=sum(1 for w in mid if w.endswith('am'))/n_mid if n_mid else 0
        am_lf_enr=lf_am_rate/am_r if am_r else 0
        am_mid_enr=mid_am_rate/am_r if am_r else 0
        edy_rate=sum(1 for w in aw if w.endswith('edy') or w.endswith('eedy'))/n_aw
        word_len=sum(len(w) for w in aw)/n_aw
        qok_r=oc_all.get('qok',0)/n_aw; ch_r=oc_all.get('ch',0)/n_aw
        qok_ch=bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r and tb>0 else 0

        metrics={'am_ll':am_ll,'d_ll':d_ll,'y_lf':y_lf,'ss_mean':ss_mean,'adj_rate':adj,
                 'qok_lf':qok_lf,'d_lf':d_lf,'s_lf':s_lf,'ch_ll':ch_ll,'ok_ll':ok_ll,
                 'qok_ll':qok_ll,'ss_d':ss_d,'ss_y':ss_y,'am_lf_enr':am_lf_enr,
                 'am_mid_enr':am_mid_enr,'edy_rate':edy_rate,'word_len_mean':word_len,
                 'qok_ch':qok_ch,'global_am_rate':am_r}
        trial_metrics.append(metrics)
    return trial_metrics

# ─── PCA (pure Python) ────────────────────────────────────────────────────────
def compute_pca(data_matrix):
    """
    data_matrix: list of lists, shape (N, 19)
    Returns: eigenvalues (sorted descending), cumulative variance explained
    """
    n = len(data_matrix)
    p = len(data_matrix[0])
    # Compute mean and std
    means = [sum(row[j] for row in data_matrix)/n for j in range(p)]
    stds = []
    for j in range(p):
        var = sum((row[j]-means[j])**2 for row in data_matrix)/n
        stds.append(var**0.5 if var>0 else 1e-10)
    # Standardize
    std_data = [[(row[j]-means[j])/stds[j] for j in range(p)] for row in data_matrix]
    # Compute correlation matrix
    corr = [[0.0]*p for _ in range(p)]
    for i in range(p):
        for j in range(p):
            cov = sum(std_data[k][i]*std_data[k][j] for k in range(n))/n
            corr[i][j] = cov
    # Power iteration to get eigenvalues (simple approach for small p=19)
    # Use Jacobi method approximation: just compute eigenvalues of correlation matrix
    # For simplicity, use numpy if available
    try:
        import numpy as np
        corr_np = np.array(corr)
        eigenvalues = np.linalg.eigvalsh(corr_np)
        eigenvalues = sorted(eigenvalues, reverse=True)
        cum_var = []
        total = sum(eigenvalues)
        cum = 0
        for ev in eigenvalues:
            cum += ev/total
            cum_var.append(cum)
        return eigenvalues, cum_var, corr
    except ImportError:
        # Fallback: trace gives sum of eigenvalues = p
        # Estimate via correlation matrix structure
        print("Warning: numpy not available, using simplified eigenvalue estimate")
        return None, None, corr

def find_clusters(corr_matrix, metrics, threshold=0.7):
    """Union-find clustering at |r| >= threshold."""
    n = len(metrics)
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(x, y):
        parent[find(x)] = find(y)
    for i in range(n):
        for j in range(i+1, n):
            if abs(corr_matrix[i][j]) >= threshold:
                union(i, j)
    clusters = defaultdict(list)
    for i in range(n):
        clusters[find(i)].append(metrics[i])
    return sorted(clusters.values(), key=len, reverse=True)

def main():
    rng = random.Random(SEED)
    print("="*70)
    print("exp_582: Battery Correlation Matrix (N=200 trials)")
    print("="*70)

    print("\nLoading corpus and building distributions...")
    b_lines = parse_vms_b()
    print(f"B-dialect lines: {len(b_lines)} (words: {sum(len(l) for l in b_lines)})")
    latin_words = load_latin(LATIN_CORPUS)
    print(f"Latin words: {len(latin_words)}")

    vms_d = compute_vms_dists(b_lines)
    lexicons = build_full_vms_lexicons(vms_d['mid_words'], SPARSE_ONSETS)
    suffix_global = vms_d['suffix_global']
    suffix_lf_sup = make_suppressed_suffix(suffix_global, R_LF)
    suffix_mid_sup = make_suppressed_suffix(suffix_global, R_MID)

    print(f"\nRunning N={N_TRIALS} simulation trials (beta_scale={BETA_SCALE})...")
    all_lines = run_sim(latin_words, vms_d, rng, suffix_lf_sup, suffix_mid_sup, lexicons)
    print(f"Total lines generated: {len(all_lines)}")

    print("\nComputing per-trial metrics...")
    trial_metrics = compute_metrics_per_trial(all_lines)
    print(f"Trials with metrics: {len(trial_metrics)}")

    # Build 200×19 data matrix
    data_matrix = [[tm[k] for k in BATTERY_19] for tm in trial_metrics]

    # Report per-metric means and stds
    print("\n--- Per-metric statistics across 200 trials ---")
    print(f"{'Metric':<18} {'Mean':>10} {'Std':>10} {'CV%':>8}")
    print("-"*48)
    for j, k in enumerate(BATTERY_19):
        vals = [row[j] for row in data_matrix]
        mn = sum(vals)/len(vals)
        std = (sum((v-mn)**2 for v in vals)/len(vals))**0.5
        cv = std/mn*100 if mn != 0 else 0
        print(f"{k:<18} {mn:>10.4f} {std:>10.4f} {cv:>7.1f}%")

    # Compute correlation matrix and PCA
    print("\nComputing correlation matrix and PCA...")
    eigenvalues, cum_var, corr_matrix = compute_pca(data_matrix)

    # PCA results
    n_for_95 = None
    if cum_var:
        for i, cv in enumerate(cum_var):
            if cv >= 0.95:
                n_for_95 = i + 1
                break
        if n_for_95 is None:
            n_for_95 = len(cum_var)

        print(f"\n--- PCA Results ---")
        print(f"{'Component':<12} {'Eigenvalue':>12} {'Var%':>8} {'CumVar%':>10}")
        print("-"*44)
        total_ev = sum(eigenvalues)
        for i, (ev, cv) in enumerate(zip(eigenvalues, cum_var)):
            marker = " <-- 95%" if i+1 == n_for_95 else ""
            print(f"PC{i+1:<10} {ev:>12.4f} {ev/total_ev*100:>7.1f}% {cv*100:>9.1f}%{marker}")
            if cv >= 0.99: break
        print(f"\nComponents for 95% variance: {n_for_95}")

    # Clustering at |r|>=0.7
    print("\n--- Clustering at |r| >= 0.7 ---")
    clusters_07 = find_clusters(corr_matrix, BATTERY_19, threshold=0.7)
    n_eff_07 = len(clusters_07)
    print(f"Effective independent constraints (clusters + singletons): {n_eff_07}")
    for i, cl in enumerate(clusters_07):
        print(f"  Cluster {i+1} ({len(cl)} metrics): {', '.join(cl)}")

    # Also clustering at |r|>=0.5
    print("\n--- Clustering at |r| >= 0.5 ---")
    clusters_05 = find_clusters(corr_matrix, BATTERY_19, threshold=0.5)
    n_eff_05 = len(clusters_05)
    print(f"Effective independent constraints at 0.5: {n_eff_05}")
    for i, cl in enumerate(clusters_05):
        print(f"  Cluster {i+1} ({len(cl)} metrics): {', '.join(cl)}")

    # Print full correlation matrix (abbreviated)
    print("\n--- Correlation Matrix Highlights (|r| >= 0.5 pairs) ---")
    high_pairs = []
    for i in range(len(BATTERY_19)):
        for j in range(i+1, len(BATTERY_19)):
            r = corr_matrix[i][j]
            if abs(r) >= 0.5:
                high_pairs.append((abs(r), r, BATTERY_19[i], BATTERY_19[j]))
    high_pairs.sort(reverse=True)
    print(f"{'Metric 1':<18} {'Metric 2':<18} {'r':>8}")
    print("-"*46)
    for abs_r, r, m1, m2 in high_pairs:
        print(f"{m1:<18} {m2:<18} {r:>+8.4f}")

    # Save correlation matrix CSV
    out_dir = '/Users/asash/voynich-cryptanalyst/state'
    csv_path = os.path.join(out_dir, 'battery_correlation_matrix.csv')
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['metric'] + BATTERY_19)
        for i, m in enumerate(BATTERY_19):
            writer.writerow([m] + [f"{corr_matrix[i][j]:.6f}" for j in range(len(BATTERY_19))])
    print(f"\nCorrelation matrix saved to: {csv_path}")

    # Save report
    report_path = os.path.join(out_dir, 'battery_correlation_report.md')
    with open(report_path, 'w') as f:
        f.write("# Battery Correlation Report — exp_582\n\n")
        f.write(f"**Generated:** 2026-04-12  \n")
        f.write(f"**N trials:** {N_TRIALS}  \n")
        f.write(f"**Architecture:** 21-mechanism, exp_314 parameters (beta_scale={BETA_SCALE})  \n\n")

        f.write("## PCA Results\n\n")
        if cum_var and eigenvalues:
            f.write(f"Components needed to explain 95% of variance: **{n_for_95}**\n\n")
            f.write(f"| Component | Eigenvalue | Var% | CumVar% |\n")
            f.write(f"|-----------|-----------|------|---------|\n")
            total_ev = sum(eigenvalues)
            for i, (ev, cv) in enumerate(zip(eigenvalues, cum_var)):
                f.write(f"| PC{i+1} | {ev:.4f} | {ev/total_ev*100:.1f}% | {cv*100:.1f}% |\n")
                if cv >= 0.99: break
            f.write("\n")

        f.write(f"## Effective Dimension\n\n")
        f.write(f"- **PCA (95% variance):** {n_for_95} components\n")
        f.write(f"- **Clustering |r|≥0.7:** {n_eff_07} independent groups\n")
        f.write(f"- **Clustering |r|≥0.5:** {n_eff_05} independent groups\n\n")
        f.write(f"**Conservative estimate (min of PCA and |r|≥0.7 clustering):** {min(n_for_95 or 99, n_eff_07)}\n\n")

        f.write("## Cluster Structure at |r| ≥ 0.7\n\n")
        f.write(f"Total clusters/singletons: {n_eff_07}\n\n")
        for i, cl in enumerate(clusters_07):
            cluster_name = f"Cluster {i+1}" if len(cl) > 1 else "Singleton"
            f.write(f"**{cluster_name}** ({len(cl)} metrics): {', '.join(cl)}\n\n")

        f.write("## Cluster Structure at |r| ≥ 0.5\n\n")
        for i, cl in enumerate(clusters_05):
            cluster_name = f"Cluster {i+1}" if len(cl) > 1 else "Singleton"
            f.write(f"**{cluster_name}** ({len(cl)} metrics): {', '.join(cl)}\n\n")

        f.write("## High-Correlation Pairs (|r| ≥ 0.5)\n\n")
        f.write(f"| Metric 1 | Metric 2 | r |\n")
        f.write(f"|----------|----------|---|\n")
        for abs_r, r, m1, m2 in high_pairs:
            f.write(f"| {m1} | {m2} | {r:+.4f} |\n")
        f.write("\n")

        f.write("## Methodological Notes\n\n")
        f.write("1. Each trial is an independent simulation run at exp_314 parameters.\n")
        f.write("2. Trial-to-trial variation reflects stochastic variability of the generative model, not VMS corpus noise.\n")
        f.write("3. The correlation matrix measures how metrics co-vary across simulation runs, not across VMS sections.\n")
        f.write("4. High correlations reflect shared mechanistic drivers (e.g., the blind LL mechanism affects am_ll AND am_lf_enr indirectly via global_am_rate).\n")
        f.write("5. The effective dimension estimate is conservative: PCA may split correlated clusters differently than simple clustering.\n")

    print(f"Report saved to: {report_path}")

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"N trials completed: {len(trial_metrics)}")
    if n_for_95:
        print(f"PCA: {n_for_95} components explain 95% of variance")
    print(f"Clustering |r|>=0.7: {n_eff_07} independent constraints")
    print(f"Clustering |r|>=0.5: {n_eff_05} independent constraints")
    print(f"Conservative estimate: {min(n_for_95 or 99, n_eff_07)}")

if __name__ == '__main__':
    main()
