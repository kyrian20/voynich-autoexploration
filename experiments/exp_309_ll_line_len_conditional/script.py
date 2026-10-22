"""
exp_309: Line-Length-Conditional LL Mechanism (H511)

exp_308 showed VMS r_ll = −0.219 vs simulation r_ll = −0.016 (gap: 0.203).
VMS LL_wl drops 1.31 chars as line length increases from 2-4 to 11-15 words.

DIAGNOSTIC PHASE: Before implementing the mechanism, check whether the LL word
length vs line length relationship in VMS is explained by:
  (A) p_blind(n) already being line-length conditional: -am LL words more frequent
      in long lines → drives shorter LL_wl
  (B) Non-am LL word length decreasing with line length (separate mechanism)

If (A): implementing line-length-conditional p_blind in simulation is the fix.
If (B): need a different mechanism (e.g., line-length-conditional suffix distribution
         for non-blind LL words, or a different word class for LL in long lines).

MECHANISM PHASE: Test line-length-conditional p_blind:
  p_blind_n = f(n) where mean p_blind = 0.115 (current global calibration)
  Test step function: p_blind_short (n≤5) = 0.04, p_blind_long (n≥10) = {0.20, 0.30, 0.40}
  Check: does r_ll improve? Does 19/19 battery maintain?
"""
from pathlib import Path as _RepositoryPath

import os, re, random, math
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

# exp_306 architecture (beta=0.50, 17 mechanisms)
P_BLIND_BASE = 0.115  # baseline; will be overridden by n-conditional version
P_LF=1.0; CP=0.55; MP=0.90; P_QOKCH=0.12; P_CHQOK=0.12; P_STUTTER=0.006
R_LF=0.12; R_MID=0.20; MU_LEN=8.4; SIGMA_LEN=3.0; P_MF=0.20; P_LF_MF=0.50; P_LL_MF=0.00
GAMMA=0.30; ALPHA=0.20; BETA=0.50
IDX_THRESH=2; SHORT_THRESH=2; TARGET_LINES=2411; WINDOW=20; SEED=309000

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
PASS_TOL=0.20
VMS_REF={'am_ll':6.5498,'d_ll':1.3625,'y_lf':3.1837,'ss_mean':1.1640,
         'adj_rate':0.0090,'qok_lf':0.7450,'d_lf':2.1178,'s_lf':4.4422,
         'ch_ll':0.9653,'ok_ll':1.0028,'qok_ll':0.6121,'ss_d':1.5850,
         'ss_y':1.9550,'am_lf_enr':0.1225,'am_mid_enr':0.1954,
         'edy_rate':0.1940,'word_len_mean':5.4000,'qok_ch':1.2670,
         'global_am_rate':0.0203}

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
    d_boost=d_global*(d_ll_target-(1-P_BLIND_BASE)*d_ll_non_blind_enr)/P_BLIND_BASE
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

def get_p_blind_n(n, p_short, p_base, p_long, thresh_short=5, thresh_long=10):
    """Line-length-conditional p_blind."""
    if n <= thresh_short: return p_short
    if n >= thresh_long: return p_long
    # Linear interpolation for middle range
    frac = (n - thresh_short) / (thresh_long - thresh_short)
    return p_short + frac * (p_long - p_short)

def run_sim(latin_words, vms_d, rng, n_trials, p_short, p_base, p_long,
            suffix_lf_sup, suffix_mid_sup, lexicons):
    """Run simulation with line-length-conditional p_blind."""
    all_lines = []
    for _ in range(n_trials):
        w=list(latin_words); rng.shuffle(w)
        lines=[]; buf=deque(maxlen=WINDOW); pos=0
        prev_onset=None; prev_word=None
        while len(lines)<TARGET_LINES and pos<len(w)-2:
            n=max(2,min(20,round(rng.gauss(MU_LEN,SIGMA_LEN))))
            chunk=w[pos:pos+n]
            if len(chunk)<2: pos+=len(chunk); continue
            line=[]; word_idx=0
            # Determine line-length-conditional p_blind for this line
            p_blind_n = get_p_blind_n(n, p_short, p_base, p_long)
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
                    # LL with line-length-conditional p_blind
                    if rng.random()<p_blind_n:
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
                        biased_suf=apply_suffix_length_bias(suffix_mid_sup,word_idx,BETA)
                        suf=weighted_choice(rng,biased_suf)
                        ew=make_word_sim(onset,suf,rng,vms_d['mid_nemed'],P_MF)
                        ew=clamp_to_lexicon(ew,lexicons,rng)
                    buf.append(ew); word_idx+=1
                prev_onset=get_onset(ew); prev_word=ew; line.append(ew)
            lines.append(line); pos+=n
        all_lines.extend(lines[:TARGET_LINES])
    return all_lines

def compute_metrics(all_lines, n_trials):
    """Compute battery metrics + Menzerath components from pooled lines."""
    # For battery: average over trials
    trial_size = TARGET_LINES
    all_metrics = []
    for t in range(n_trials):
        lines = all_lines[t*trial_size:(t+1)*trial_size]
        aw=[w for l in lines for w in l]; n=len(aw)
        if n<100: continue
        lf=[l[0] for l in lines if l]
        ll=[l[-1] for l in lines if len(l)>1]
        mid=[w for l in lines for w in l[1:-1] if len(l)>2]
        oc_all=Counter(get_onset(w) for w in aw)
        oc_lf=Counter(get_onset(w) for w in lf)
        oc_ll=Counter(get_onset(w) for w in ll)
        n_lf,n_ll,n_mid=len(lf),len(ll),len(mid)
        def enr(onset,ctr,ns):
            s=ctr.get(onset,0)/ns if ns else 0
            g=oc_all.get(onset,0)/n if n else 0
            return s/g if g>0 else 0
        am_r=sum(1 for w in aw if w.endswith('am'))/n
        ll_am=sum(1 for w in ll if w.endswith('am'))/n_ll if n_ll else 0
        am_ll=ll_am/am_r if am_r else 0
        d_ll=enr('d',oc_ll,n_ll); y_lf=enr('y',oc_lf,n_lf)
        tb=n-1
        bg=Counter((get_onset(aw[i]),get_onset(aw[i+1])) for i in range(tb))
        def ss(o):
            b=oc_all.get(o,0)/n
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
        edy_rate=sum(1 for w in aw if w.endswith('edy') or w.endswith('eedy'))/n
        word_len=sum(len(w) for w in aw)/n
        qok_r=oc_all.get('qok',0)/n; ch_r=oc_all.get('ch',0)/n
        qok_ch=bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r and tb>0 else 0
        # Menzerath
        line_lens=[len(l) for l in lines if len(l)>=3]
        line_mean_wl=[sum(len(w) for w in l)/len(l) for l in lines if len(l)>=3]
        ll_wls=[len(l[-1]) for l in lines if len(l)>=3]
        if len(line_lens)>10:
            mn_ll=sum(line_lens)/len(line_lens); mn_wl=sum(line_mean_wl)/len(line_mean_wl)
            cov=sum((x-mn_ll)*(y-mn_wl) for x,y in zip(line_lens,line_mean_wl))/len(line_lens)
            var_ll=sum((x-mn_ll)**2 for x in line_lens)/len(line_lens)
            var_wl=sum((y-mn_wl)**2 for y in line_mean_wl)/len(line_mean_wl)
            menz_r=cov/(var_ll**0.5*var_wl**0.5) if var_ll>0 and var_wl>0 else 0
            # r_ll component
            mn_ll2=sum(line_lens)/len(line_lens); mn_llwl=sum(ll_wls)/len(ll_wls)
            cov_ll=sum((x-mn_ll2)*(y-mn_llwl) for x,y in zip(line_lens,ll_wls))/len(line_lens)
            var_ll2=sum((x-mn_ll2)**2 for x in line_lens)/len(line_lens)
            var_llwl=sum((y-mn_llwl)**2 for y in ll_wls)/len(ll_wls)
            r_ll=cov_ll/(var_ll2**0.5*var_llwl**0.5) if var_ll2>0 and var_llwl>0 else 0
        else:
            menz_r=0.0; r_ll=0.0
        idx_lens=[]
        for l in lines:
            if len(l)<4: continue
            for j,w in enumerate(l[1:-1]): idx_lens.append((j,len(w)))
        if len(idx_lens)>100:
            n_il=len(idx_lens); mean_idx=sum(x for x,y in idx_lens)/n_il
            mean_len=sum(y for x,y in idx_lens)/n_il
            cov_il=sum((x-mean_idx)*(y-mean_len) for x,y in idx_lens)/n_il
            var_il=sum((x-mean_idx)**2 for x,y in idx_lens)/n_il
            mid_slope=cov_il/var_il if var_il>0 else 0
        else:
            mid_slope=0.0
        all_metrics.append(dict(am_ll=am_ll,d_ll=d_ll,y_lf=y_lf,ss_mean=ss_mean,adj_rate=adj,
                                qok_lf=qok_lf,d_lf=d_lf,s_lf=s_lf,ch_ll=ch_ll,ok_ll=ok_ll,
                                qok_ll=qok_ll,ss_d=ss_d,ss_y=ss_y,am_lf_enr=am_lf_enr,
                                am_mid_enr=am_mid_enr,edy_rate=edy_rate,word_len_mean=word_len,
                                qok_ch=qok_ch,global_am_rate=am_r,menz_r=menz_r,
                                mid_slope=mid_slope,r_ll=r_ll))
    return all_metrics

def agg(ml, key):
    vals=[x[key] for x in ml if key in x]
    return sum(vals)/len(vals) if vals else 0
def passes(sv, vv): return (1-PASS_TOL)<=sv/vv<=(1+PASS_TOL) if vv else True

# ─── Parse VMS ─────────────────────────────────────────────────────────────────
print("exp_309: Line-Length-Conditional LL Mechanism (H511)")
print("=" * 70)

print("\nParsing VMS B-dialect...")
b_lines=parse_vms_b()
print(f"  Total: {len(b_lines)} lines")

# ─── DIAGNOSTIC: VMS -am rate and non-am LL_wl by line length bucket ──────────
print(f"\n{'='*70}")
print("DIAGNOSTIC: VMS LL Word Length Decomposition by Line Length")
print(f"{'='*70}")
print("\nIs the VMS LL gradient driven by -am rate increase (p_blind effect) or by")
print("non-am LL word length decrease?")
print()

buckets_vms = [(2,4),(5,6),(7,8),(9,10),(11,15)]
print(f"{'Bucket':10s}  {'N':6s}  {'LL_wl':7s}  {'am_rate':8s}  {'nonam_wl':9s}  {'am_wl':7s}  {'implied_p':10s}")
print("-" * 70)
vms_ll_data = []
for lo,hi in buckets_vms:
    ll_words_bucket = [l[-1] for l in b_lines if lo<=len(l)<=hi and len(l)>=2]
    if not ll_words_bucket: continue
    n=len(ll_words_bucket)
    am_words=[w for w in ll_words_bucket if w.endswith('am')]
    nonam_words=[w for w in ll_words_bucket if not w.endswith('am')]
    am_rate=len(am_words)/n
    am_wl=sum(len(w) for w in am_words)/len(am_words) if am_words else 0
    nonam_wl=sum(len(w) for w in nonam_words)/len(nonam_words) if nonam_words else 0
    ll_wl=sum(len(w) for w in ll_words_bucket)/n
    # From: ll_wl = am_rate × am_wl + (1-am_rate) × nonam_wl
    # In sim: am_rate = p_blind × p_blind_word_is_am + (1-p_blind) × global_am_rate_ll
    # For diagnostic, am_rate ≈ p_blind (since -am words in non-blind path are rare)
    implied_p = am_rate  # approximation
    label=f"LL={lo}-{hi}"
    print(f"{label:10s}  {n:6d}  {ll_wl:7.3f}  {am_rate:8.4f}  {nonam_wl:9.3f}  {am_wl:7.3f}  {implied_p:10.4f}")
    vms_ll_data.append((lo,hi,n,ll_wl,am_rate,nonam_wl,am_wl))

print("\nInterpretation:")
if vms_ll_data:
    am_rates=[d[4] for d in vms_ll_data]
    nonam_wls=[d[5] for d in vms_ll_data]
    ll_wls=[d[3] for d in vms_ll_data]
    ns=[d[2] for d in vms_ll_data]
    # Does am_rate increase with line length bucket?
    am_rate_increase=am_rates[-1]-am_rates[0]
    nonam_decrease=nonam_wls[0]-nonam_wls[-1]
    print(f"  -am rate change (short→long lines): {am_rates[0]:.4f} → {am_rates[-1]:.4f} "
          f"(Δ={am_rate_increase:+.4f})")
    print(f"  Non-am LL_wl change (short→long): {nonam_wls[0]:.3f} → {nonam_wls[-1]:.3f} "
          f"(Δ={-nonam_decrease:+.3f})")
    print(f"  Overall LL_wl change: {ll_wls[0]:.3f} → {ll_wls[-1]:.3f} (Δ={ll_wls[-1]-ll_wls[0]:+.3f})")
    print(f"\n  If Δ(am_rate) >> Δ(nonam_wl): p_blind is the driver → H511 is the right fix")
    print(f"  If Δ(nonam_wl) >> Δ(am_rate): non-am distribution changes → different mechanism needed")

# ─── Setup simulation ────────────────────────────────────────────────────────────
print(f"\n{'='*70}")
print("Simulation Setup")
print(f"{'='*70}")

vms_d=compute_vms_dists(b_lines)
latin_words=load_latin(LATIN_CORPUS)
print(f"  {len(latin_words)} Latin words loaded")
suffix_lf_sup=make_suppressed_suffix(vms_d['suffix_global'],R_LF)
suffix_mid_sup=make_suppressed_suffix(vms_d['suffix_global'],R_MID)
lexicons=build_full_vms_lexicons(vms_d['mid_words'],SPARSE_ONSETS)

# Compute expected mean p_blind for each condition (must ≈ 0.115 for am_ll calibration)
# VMS line length distribution for weighting:
n_dist = Counter(len(l) for l in b_lines)
total_lines = sum(n_dist.values())
def mean_p_blind(p_short, p_long, n_dist, total_lines, thresh_short=5, thresh_long=10):
    total_p = 0
    for n, cnt in n_dist.items():
        p = get_p_blind_n(n, p_short, P_BLIND_BASE, p_long, thresh_short, thresh_long)
        total_p += p * cnt
    return total_p / total_lines

# ─── Sweep p_blind conditions ────────────────────────────────────────────────────
CONDITIONS = [
    ('baseline',          0.115, 0.115, 0.115),  # no conditioning
    ('cond_mild',         0.060, 0.115, 0.180),  # mild conditioning
    ('cond_moderate',     0.040, 0.115, 0.250),  # moderate
    ('cond_strong',       0.020, 0.115, 0.350),  # strong
    ('cond_very_strong',  0.005, 0.115, 0.500),  # very strong
]

N_SWEEP = 10

print(f"\n{'='*70}")
print(f"Sweep: Line-Length-Conditional p_blind (N={N_SWEEP} per condition)")
print(f"{'='*70}")
print(f"\nCondition parameters (p_short for n≤5, linear interp, p_long for n≥10):")
for label, p_short, p_base, p_long in CONDITIONS:
    mp = mean_p_blind(p_short, p_long, n_dist, total_lines)
    print(f"  {label:20s}: p_short={p_short:.3f}, p_long={p_long:.3f}, mean_p_blind={mp:.4f}")

print(f"\n{'Condition':22s}  {'Pass':6s}  {'am_ll':7s}  {'%VMS':6s}  {'menz_r':8s}  {'r_ll':7s}  {'mid_slope':10s}")
print("-" * 80)

rng = random.Random(SEED)
condition_results = {}
for label, p_short, p_base, p_long in CONDITIONS:
    all_lines = run_sim(latin_words, vms_d, rng, N_SWEEP, p_short, p_base, p_long,
                        suffix_lf_sup, suffix_mid_sup, lexicons)
    ml = compute_metrics(all_lines, N_SWEEP)
    pass_count = sum(1 for m in BATTERY_19 if passes(agg(ml,m), VMS_REF[m]))
    am_ll_v = agg(ml,'am_ll'); am_ll_pct = am_ll_v/VMS_REF['am_ll']*100
    mr = agg(ml,'menz_r'); rll = agg(ml,'r_ll'); ms = agg(ml,'mid_slope')
    print(f"{label:22s}  {pass_count:2d}/19  {am_ll_v:7.4f}  {am_ll_pct:5.1f}%  {mr:+8.4f}  {rll:+7.4f}  {ms:+10.4f}")
    condition_results[label] = {'pass': pass_count, 'am_ll': am_ll_v, 'menz_r': mr, 'r_ll': rll, 'mid_slope': ms, 'ml': ml}

# ─── Full battery for best candidate ─────────────────────────────────────────────
print(f"\n{'='*70}")
print("Selecting best condition and running full N=30 battery")
print(f"{'='*70}")

# Select: best menz_r with pass_count >= 18/19 and am_ll within 20% of VMS
candidates = [(label, r) for label, r in condition_results.items()
              if r['pass'] >= 18 and abs(r['am_ll']/VMS_REF['am_ll'] - 1) <= 0.20]
if candidates:
    best_label = max(candidates, key=lambda x: abs(x[1]['menz_r']))[0]
    best_params = next((c for c in CONDITIONS if c[0] == best_label), None)
    print(f"\nBest condition: {best_label}")
    print(f"  p_short={best_params[1]:.3f}, p_long={best_params[3]:.3f}")
    print(f"  Sweep menz_r={condition_results[best_label]['menz_r']:+.4f}, r_ll={condition_results[best_label]['r_ll']:+.4f}")

    rng2 = random.Random(SEED + 1000)
    N_FULL = 30
    all_lines_full = run_sim(latin_words, vms_d, rng2, N_FULL,
                             best_params[1], best_params[2], best_params[3],
                             suffix_lf_sup, suffix_mid_sup, lexicons)
    ml_full = compute_metrics(all_lines_full, N_FULL)
    pass_total = sum(1 for m in BATTERY_19 if passes(agg(ml_full,m), VMS_REF[m]))
    print(f"\n  Full N={N_FULL} Battery ({best_label}):")
    print(f"  {'Metric':<25} {'VMS':>8} {'Sim':>8} {'%VMS':>7}  Status")
    print(f"  {'-'*55}")
    for metric in BATTERY_19:
        vv=VMS_REF[metric]; sv=agg(ml_full,metric)
        pct=sv/vv*100 if vv else 0
        ok=passes(sv,vv); status='PASS' if ok else 'FAIL'
        print(f"  {metric:<25} {vv:8.4f} {sv:8.4f} {pct:6.1f}%  {status}")
    print(f"\n  TOTAL: {pass_total}/19")
    print(f"  Menzerath r: {agg(ml_full,'menz_r'):+.4f}  (VMS=-0.225, prev=-0.109)")
    print(f"  r_ll:        {agg(ml_full,'r_ll'):+.4f}  (VMS=-0.219, prev=-0.016)")
    print(f"  MID slope:   {agg(ml_full,'mid_slope'):+.4f}  (VMS=-0.058)")
else:
    print("No candidate satisfies constraints. See sweep results above.")
    for label, r in condition_results.items():
        print(f"  {label}: pass={r['pass']}/19, am_ll%={r['am_ll']/VMS_REF['am_ll']*100:.1f}%")

print("\nDone.")
