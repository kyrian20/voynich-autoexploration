"""
exp_318: Length-Biased VMS Lexicon Selection for sh/ch/d (H520)

Problem identified in exp_317: vocabulary clamping for sh/ch/d (CP90 closure)
and the beta Menzerath mechanism are incompatible because:
  - sh+ch = 73% of MID tokens
  - clamping to fixed lexicons destroys line-length-conditional word-length variability
  - result: menz_r drops from 104% → 73-86% with sh/ch clamping

Solution concept: "type-reuse + length-bias"
  - Keep closed type set (VMS lexicon for sh/ch/d)
  - Weight type selection by proximity to beta-target word length
  - target_len(n) decreases with line length n
  - weight(w) = exp(-DELTA × (len(w) - target_len(n))^2)

Implementation: modify clamp_to_lexicon() to accept (n, DELTA, target_fn) parameters.
When n is provided, use length-biased selection; otherwise uniform (for qok/ok/ot/qot).

Architecture base: 21-mechanism with clamp_sh+ch+d (closes CP90 for all three).

Sweep: DELTA ∈ {0.5, 1.0, 2.0} × TARGET_SLOPE ∈ {0.10, 0.20}
Plus: baseline_clamp_shchd (uniform clamp, no length bias) for comparison.

Target: CP90 near-VMS for sh/ch/d AND menz_r ≥ 95% AND 19/19 PASS.
"""
from pathlib import Path as _RepositoryPath

import os, re, random, math
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

# 21-mechanism architecture parameters
P_SHORT=0.060; P_LONG=0.180; THRESH_SHORT=5; THRESH_LONG=10; MEAN_N=8.4
P_LF=1.0; CP=0.55; MP=0.90; P_QOKCH=0.12; P_CHQOK=0.12; P_STUTTER=0.006
R_LF=0.12; R_MID=0.20; MU_LEN=8.4; SIGMA_LEN=3.0; P_MF=0.20; P_LF_MF=0.50; P_LL_MF=0.00
GAMMA=0.30; ALPHA=0.20
BETA_BASE=0.50; BETA_SCALE=1.8; IDX_THRESH=2
SHORT_THRESH=2; TARGET_LINES=2411; WINDOW=20; SEED=318000
MAX_RETRY=10; N_TRIALS=30

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
EXTRA_CLAMP_ONSETS={'sh','ch','d'}   # additional onsets to clamp in all conditions
ALL_CLAMP_ONSETS=SPARSE_ONSETS|EXTRA_CLAMP_ONSETS

MAJOR_ONSETS=['qok','ok','ot','qot','sh','ch','d']
VMS_CP90={'qok':31,'ok':54,'ot':57,'qot':36,'sh':129,'ch':223,'d':83}

BATTERY_19=['am_ll','d_ll','y_lf','ss_mean','adj_rate','qok_lf','d_lf','s_lf',
            'ch_ll','ok_ll','qok_ll','ss_d','ss_y','am_lf_enr','am_mid_enr',
            'edy_rate','word_len_mean','qok_ch','global_am_rate']
PASS_TOL=0.20
VMS_REF={'am_ll':6.5498,'d_ll':1.3625,'y_lf':3.1837,'ss_mean':1.1640,
         'adj_rate':0.0090,'qok_lf':0.7450,'d_lf':2.1178,'s_lf':4.4422,
         'ch_ll':0.9653,'ok_ll':1.0028,'qok_ll':0.6121,'ss_d':1.5850,
         'ss_y':1.9550,'am_lf_enr':0.1225,'am_mid_enr':0.1954,
         'edy_rate':0.1940,'word_len_mean':5.4000,'qok_ch':1.2670,
         'global_am_rate':0.0203}

# Length-biased selection target: target_len(n) = TARGET_BASE - TARGET_SLOPE * max(0, n - TARGET_N_REF)
TARGET_BASE=5.4    # mean VMS word length
TARGET_N_REF=8.4   # mean line length (= MEAN_N)

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label
    return 'other'
def get_onset_len(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return len(prefix)
    return len(w)
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

def pearson_r(xs, ys):
    n=len(xs)
    if n<3: return float('nan')
    mx=sum(xs)/n; my=sum(ys)/n
    cov=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/n
    sx=(sum((x-mx)**2 for x in xs)/n)**0.5
    sy=(sum((y-my)**2 for y in ys)/n)**0.5
    if sx*sy==0: return float('nan')
    return cov/(sx*sy)

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

def compute_cp90(word_list):
    cnt=Counter(word_list); total=sum(cnt.values())
    if total==0: return 0
    threshold=0.90*total; cumulative=0
    for i,(w,c) in enumerate(cnt.most_common(),1):
        cumulative+=c
        if cumulative>=threshold: return i
    return len(cnt)

def build_midfix_dist(words):
    midfix_cnt=Counter()
    for w in words:
        onset=get_onset(w); suf=get_suffix(w)
        if onset=='other' or suf=='other': continue
        onset_len=get_onset_len(w); suf_len=len(suf)
        edy_len=get_edy_suffix_len(w)
        if edy_len:
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
    mid_nemed,_=build_midfix_dist(mid_words)
    lf_nemed,_=build_midfix_dist(lf_words)
    ll_nemed,_=build_midfix_dist(ll_words)
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

def clamp_to_lexicon(word, lexicons, rng, n=None, delta=0.0, target_slope=0.0,
                     length_biased_onsets=frozenset()):
    """Clamp word to VMS lexicon. If n provided and onset in length_biased_onsets,
    use length-biased selection; otherwise uniform."""
    onset=get_onset(word)
    if onset not in lexicons or not lexicons[onset]: return word
    lex=lexicons[onset]
    if delta > 0.0 and n is not None and onset in length_biased_onsets:
        # Length-biased selection: prefer words close to target_len(n)
        target_len=TARGET_BASE - target_slope * max(0.0, n - TARGET_N_REF)
        weights=[math.exp(-delta * (len(w) - target_len)**2) for w in lex]
        total=sum(weights)
        if total > 0:
            r=rng.random()*total; cum=0.0
            for w,wt in zip(lex, weights):
                cum+=wt
                if r<cum: return w
    return rng.choice(lex)

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

def build_vms_lexicons(mid_words, onset_classes):
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

def run_sim(latin_words, vms_d, rng, n_trials, suffix_lf_sup, suffix_mid_sup,
            lexicons, delta, target_slope, length_biased_onsets):
    all_lines=[]; mid_words_by_onset=defaultdict(list)
    for _ in range(n_trials):
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
                            ew=clamp_to_lexicon(ew, lexicons, rng, n, delta, target_slope,
                                                length_biased_onsets)
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
                        ew=clamp_to_lexicon(ew, lexicons, rng, n, delta, target_slope,
                                            length_biased_onsets)
                    mid_words_by_onset[get_onset(ew)].append(ew)
                    buf.append(ew); word_idx+=1
                prev_onset=get_onset(ew); prev_word=ew; line.append(ew)
            lines.append(line); pos+=n
        all_lines.extend(lines[:TARGET_LINES])
    return all_lines, dict(mid_words_by_onset)

def compute_metrics(all_lines, n_trials):
    trial_size=TARGET_LINES; trial_metrics=[]
    for t in range(n_trials):
        lines=all_lines[t*trial_size:(t+1)*trial_size]
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
        line_lens=[len(l) for l in lines if len(l)>=3]
        line_mean_wl=[sum(len(w) for w in l)/len(l) for l in lines if len(l)>=3]
        ll_wls=[len(l[-1]) for l in lines if len(l)>=3]
        mid_wls_by_line=[sum(len(w) for w in l[1:-1])/len(l[1:-1]) for l in lines if len(l)>=4]
        line_lens_for_mid=[len(l) for l in lines if len(l)>=4]
        menz_r=pearson_r(line_lens,line_mean_wl)
        r_ll=pearson_r(line_lens,ll_wls)
        r_mid=pearson_r(line_lens_for_mid,mid_wls_by_line)
        metrics={'am_ll':am_ll,'d_ll':d_ll,'y_lf':y_lf,'ss_mean':ss_mean,'adj_rate':adj,
                 'qok_lf':qok_lf,'d_lf':d_lf,'s_lf':s_lf,'ch_ll':ch_ll,'ok_ll':ok_ll,
                 'qok_ll':qok_ll,'ss_d':ss_d,'ss_y':ss_y,'am_lf_enr':am_lf_enr,
                 'am_mid_enr':am_mid_enr,'edy_rate':edy_rate,'word_len_mean':word_len,
                 'qok_ch':qok_ch,'global_am_rate':am_r,
                 'menz_r':menz_r,'r_ll':r_ll,'r_mid':r_mid}
        trial_metrics.append(metrics)
    return trial_metrics

def agg(tms,k): return sum(m[k] for m in tms)/len(tms) if tms else 0
def metric_pass(tms,k):
    v=agg(tms,k); ref=VMS_REF[k]
    return ref*(1-PASS_TOL)<=v<=ref*(1+PASS_TOL)
def count_pass_metrics(tms): return sum(1 for k in BATTERY_19 if metric_pass(tms,k))

def print_result(tms, label, cp90_dict):
    pass_cnt=count_pass_metrics(tms)
    mr=agg(tms,'menz_r'); rll=agg(tms,'r_ll'); rmid=agg(tms,'r_mid')
    adj=agg(tms,'adj_rate'); edy=agg(tms,'edy_rate')
    fails=[k for k in BATTERY_19 if not metric_pass(tms,k)]
    fail_str=', '.join(fails) if fails else 'none'
    print(f"\n{'='*60}")
    print(f"Condition: {label}  [{pass_cnt}/19 PASS]")
    print(f"{'='*60}")
    print(f"menz_r={mr:.4f} ({mr/(-0.225)*100:.1f}%VMS)  "
          f"r_mid={rmid:.4f} ({rmid/(-0.178)*100:.1f}%VMS)  "
          f"r_ll={rll:.4f} ({rll/(-0.219)*100:.1f}%VMS)")
    print(f"adj_rate={adj:.5f} ({adj/0.009*100:.1f}%VMS)  edy_rate={edy:.4f} ({edy/0.194*100:.1f}%VMS)")
    print(f"CP90 ratios: ", end='')
    parts=[]
    for onset in ['sh','ch','d']:
        sc=cp90_dict.get(onset,0); vc=VMS_CP90.get(onset,1)
        ratio=sc/vc if vc else float('nan')
        parts.append(f"{onset}:{ratio:.2f}x")
    print(', '.join(parts))
    if fails: print(f"FAIL: {fail_str}")
    else: print("PASS: all 19")

def main():
    rng=random.Random(SEED)
    print("Loading data...")
    b_lines=parse_vms_b()
    print(f"B-dialect lines: {len(b_lines)} (words: {sum(len(l) for l in b_lines)})")

    latin_words=load_latin(LATIN_CORPUS)
    vms_d=compute_vms_dists(b_lines)
    suffix_global=vms_d['suffix_global']
    suffix_lf_sup=make_suppressed_suffix(suffix_global,R_LF)
    suffix_mid_sup=make_suppressed_suffix(suffix_global,R_MID)

    # Build lexicons: sparse (baseline) + extra for sh/ch/d
    sparse_lexicons=build_vms_lexicons(vms_d['mid_words'], SPARSE_ONSETS)
    all_clamp_lexicons=build_vms_lexicons(vms_d['mid_words'], ALL_CLAMP_ONSETS)

    # Print VMS sh/ch/d word-length distributions for context
    print("\nVMS sh/ch/d word-length ranges in MID:")
    vms_mid_by_onset=defaultdict(list)
    for w in vms_d['mid_words']: vms_mid_by_onset[get_onset(w)].append(w)
    for onset in ['sh','ch','d']:
        wls=[len(w) for w in vms_mid_by_onset[onset]]
        if wls:
            wl_cnt=Counter(wls)
            print(f"  {onset}: min={min(wls)}, max={max(wls)}, mean={sum(wls)/len(wls):.2f}, "
                  f"range={sorted(set(wls))}")

    # Conditions: baseline (no sh/ch/d clamp), then swept conditions
    conditions = [
        # (label, lexicons, delta, target_slope, length_biased_onsets)
        ('baseline_sparse_only', sparse_lexicons, 0.0, 0.0, frozenset()),
        ('clamp_shchd_uniform', all_clamp_lexicons, 0.0, 0.0, frozenset()),  # uniform clamp
        ('clamp_shchd_d0.5_s0.10', all_clamp_lexicons, 0.5, 0.10, EXTRA_CLAMP_ONSETS),
        ('clamp_shchd_d0.5_s0.20', all_clamp_lexicons, 0.5, 0.20, EXTRA_CLAMP_ONSETS),
        ('clamp_shchd_d1.0_s0.10', all_clamp_lexicons, 1.0, 0.10, EXTRA_CLAMP_ONSETS),
        ('clamp_shchd_d1.0_s0.20', all_clamp_lexicons, 1.0, 0.20, EXTRA_CLAMP_ONSETS),
        ('clamp_shchd_d2.0_s0.10', all_clamp_lexicons, 2.0, 0.10, EXTRA_CLAMP_ONSETS),
        ('clamp_shchd_d2.0_s0.20', all_clamp_lexicons, 2.0, 0.20, EXTRA_CLAMP_ONSETS),
    ]

    for label, lexicons, delta, target_slope, lb_onsets in conditions:
        rng2=random.Random(SEED+99999)
        all_lines, mid_by_onset=run_sim(latin_words, vms_d, rng2, N_TRIALS,
                                         suffix_lf_sup, suffix_mid_sup,
                                         lexicons, delta, target_slope, lb_onsets)
        tms=compute_metrics(all_lines, N_TRIALS)
        cp90_dict={onset: compute_cp90(mid_by_onset.get(onset,[])) for onset in MAJOR_ONSETS}
        print_result(tms, label, cp90_dict)

    print("\nDone.")

if __name__=='__main__':
    main()
