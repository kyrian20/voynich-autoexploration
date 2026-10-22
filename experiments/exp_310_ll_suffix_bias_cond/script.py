"""
exp_310: Line-Length-Conditional LL Suffix Bias (H512)

exp_309 showed that non-am LL_wl decreases −1.244 chars as line length increases
(n=2-4: 5.671 → n=11-15: 4.426). The 18th mechanism (cond_mild p_blind) captures
the -am rate component but NOT this non-am word length component.

DIAGNOSTIC: What suffix types do VMS non-am LL words use in short vs long lines?
  - Hypothesis: long lines use shorter suffixes (ey/ol/dy/ar) more than short lines
  - Measure VMS non-am LL suffix distribution by line length bucket

MECHANISM: Line-length-conditional suffix length bias for LL non-blind path
  - beta_ll_eff(n) = beta_ll_base * n / MEAN_N (scales with line length)
  - At n=2-4 (short lines): beta_ll_eff ≈ 0.3-0.5 * beta_ll_base (mild bias)
  - At n=11-15 (long lines): beta_ll_eff ≈ 1.3-1.8 * beta_ll_base (strong bias)
  - This biases non-blind LL word generation toward shorter suffixes in longer lines

19th mechanism candidate: line-length-conditional LL suffix bias.
Architecture baseline: 18-mechanism (cond_mild p_blind, exp_309).
"""
from pathlib import Path as _RepositoryPath

import os, re, random, math
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

# 18-mechanism architecture (exp_309: cond_mild p_blind)
P_SHORT=0.060; P_LONG=0.180; THRESH_SHORT=5; THRESH_LONG=10; MEAN_N=8.4
P_LF=1.0; CP=0.55; MP=0.90; P_QOKCH=0.12; P_CHQOK=0.12; P_STUTTER=0.006
R_LF=0.12; R_MID=0.20; MU_LEN=8.4; SIGMA_LEN=3.0; P_MF=0.20; P_LF_MF=0.50; P_LL_MF=0.00
GAMMA=0.30; ALPHA=0.20; BETA=0.50
IDX_THRESH=2; SHORT_THRESH=2; TARGET_LINES=2411; WINDOW=20; SEED=310000

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
    d_boost=d_global*(d_ll_target-(1-0.115)*d_ll_non_blind_enr)/0.115  # use baseline p_blind for d_boost
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

def apply_suffix_length_bias(suf_w, beta):
    """Apply suffix-length bias (no word_idx gate — for LL path)."""
    if beta==0.0: return suf_w
    new_w={}
    for suf,w in suf_w.items():
        suf_len=len(suf) if suf!='other' else 5
        penalty=max(0,suf_len-SHORT_THRESH)
        new_w[suf]=w*math.exp(-beta*penalty)
    total=sum(new_w.values())
    return {s:v/total for s,v in new_w.items()} if total>0 else suf_w

def apply_suffix_length_bias_mid(suf_w, word_idx, beta):
    """Apply suffix-length bias for MID path (gates on word_idx)."""
    if beta==0.0 or word_idx<IDX_THRESH: return suf_w
    return apply_suffix_length_bias(suf_w, beta)

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
    """18th mechanism: line-length-conditional p_blind (cond_mild from exp_309)."""
    if n <= THRESH_SHORT: return P_SHORT
    if n >= THRESH_LONG: return P_LONG
    frac=(n-THRESH_SHORT)/(THRESH_LONG-THRESH_SHORT)
    return P_SHORT+frac*(P_LONG-P_SHORT)

def get_beta_ll_eff(n, beta_ll_base):
    """19th mechanism candidate: line-length-conditional LL suffix bias.
    Scales beta_ll linearly with n/MEAN_N, so long lines get stronger suffix-length penalty."""
    return beta_ll_base * n / MEAN_N

# ---------------------------------------------------------------------------
# DIAGNOSTIC: VMS non-am LL suffix distribution by line length bucket
# ---------------------------------------------------------------------------

LINE_LEN_BUCKETS = [(2,4,'n=2-4'), (5,6,'n=5-6'), (7,8,'n=7-8'), (9,10,'n=9-10'), (11,20,'n=11-15')]

def run_diagnostic(b_lines):
    print("="*70)
    print("DIAGNOSTIC: VMS non-am LL suffix distribution by line length bucket")
    print("="*70)
    # Collect non-am LL words by line length bucket
    bucket_data = {label: {'words':[], 'suffix_cnt':Counter(), 'am_cnt':0}
                   for _,_,label in LINE_LEN_BUCKETS}
    bucket_all_ll = {label: [] for _,_,label in LINE_LEN_BUCKETS}
    for line in b_lines:
        n = len(line)
        if n < 2: continue
        ll_word = line[-1]
        for lo,hi,label in LINE_LEN_BUCKETS:
            if lo <= n <= hi:
                bucket_all_ll[label].append(ll_word)
                if ll_word.endswith('am'):
                    bucket_data[label]['am_cnt'] += 1
                else:
                    bucket_data[label]['words'].append(ll_word)
                    suf = get_suffix(ll_word)
                    bucket_data[label]['suffix_cnt'][suf] += 1
                break

    # Summarize suffix lengths
    print(f"\n{'Bucket':<12} {'N_lines':>8} {'am_rate':>8} {'nonam_N':>8} "
          f"{'nonam_wl':>9} {'mean_suf_len':>13} "
          f"short_suf% long_suf%")
    print("-"*90)
    # Short suffixes: ey, ol, or, al, ar, dy, am (len<=2)
    # Long suffixes: eedy, edy, aiin, ain (len>=3)
    all_suffix_types = SUFFIX_PATTERNS + ['other']
    for lo,hi,label in LINE_LEN_BUCKETS:
        d = bucket_data[label]
        all_ll = bucket_all_ll[label]
        N_lines = len(all_ll)
        am_cnt = d['am_cnt']
        am_rate = am_cnt/N_lines if N_lines else 0
        non_am_words = d['words']
        nonam_n = len(non_am_words)
        nonam_wl = sum(len(w) for w in non_am_words)/nonam_n if nonam_n else 0
        sc = d['suffix_cnt']
        total_sc = sum(sc.values())
        if total_sc > 0:
            mean_suf_len = sum(len(s if s!='other' else '????')*c for s,c in sc.items()) / total_sc
            short_pct = sum(c for s,c in sc.items() if len(s)<=2)/total_sc*100  # ey,ol,or,al,ar,dy
            long_pct = sum(c for s,c in sc.items() if len(s)>=3)/total_sc*100   # eedy,edy,aiin,ain
        else:
            mean_suf_len = 0; short_pct = 0; long_pct = 0
        print(f"{label:<12} {N_lines:>8} {am_rate:>8.3f} {nonam_n:>8} "
              f"{nonam_wl:>9.3f} {mean_suf_len:>13.3f} "
              f"{short_pct:>9.1f}% {long_pct:>9.1f}%")

    print("\nTop suffix types per bucket (non-am LL words):")
    for lo,hi,label in LINE_LEN_BUCKETS:
        sc = bucket_data[label]['suffix_cnt']
        total_sc = sum(sc.values())
        if total_sc == 0: continue
        top = sorted(sc.items(), key=lambda x:-x[1])[:5]
        top_str = ', '.join(f'{s}:{c/total_sc:.1%}' for s,c in top)
        print(f"  {label}: {top_str}")

    # Compute Pearson r between line length and non-am LL_wl
    ll_lens = []
    nonam_wls = []
    for line in b_lines:
        n = len(line)
        if n < 2: continue
        ll_word = line[-1]
        if not ll_word.endswith('am'):
            ll_lens.append(n)
            nonam_wls.append(len(ll_word))
    r = pearson_r(ll_lens, nonam_wls)
    print(f"\nPearson r(line_len, non_am_LL_wl) = {r:.4f} (N={len(ll_lens)} non-am LL words)")

    # Compute total LL_wl vs line_len
    all_ll_lens = []; all_ll_wls = []
    for line in b_lines:
        if len(line) < 2: continue
        all_ll_lens.append(len(line)); all_ll_wls.append(len(line[-1]))
    r_total = pearson_r(all_ll_lens, all_ll_wls)
    print(f"Pearson r(line_len, total_LL_wl) = {r_total:.4f} (N={len(all_ll_lens)} LL words)")
    print()

# ---------------------------------------------------------------------------
# SIMULATION
# ---------------------------------------------------------------------------

def run_sim(latin_words, vms_d, rng, n_trials, beta_ll_base,
            suffix_lf_sup, suffix_mid_sup, lexicons):
    """Run simulation with 18-mechanism architecture + beta_ll_base for LL suffix bias."""
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
            p_blind_n = get_p_blind_n(n)
            beta_ll_eff = get_beta_ll_eff(n, beta_ll_base)
            # Pre-compute biased LL suffix distribution for this line length
            biased_ll_suf = apply_suffix_length_bias(suffix_mid_sup, beta_ll_eff)
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
                    # LL: 18th mechanism p_blind + 19th mechanism beta_ll
                    if rng.random()<p_blind_n:
                        onset=weighted_choice(rng,vms_d['ll_onsets'])
                        ew=onset+'am'
                    else:
                        onset=weighted_choice(rng,vms_d['onset_ll'])
                        suf=weighted_choice(rng,biased_ll_suf)
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
                        biased_suf=apply_suffix_length_bias_mid(suffix_mid_sup,word_idx,BETA)
                        suf=weighted_choice(rng,biased_suf)
                        ew=make_word_sim(onset,suf,rng,vms_d['mid_nemed'],P_MF)
                        ew=clamp_to_lexicon(ew,lexicons,rng)
                    buf.append(ew); word_idx+=1
                prev_onset=get_onset(ew); prev_word=ew; line.append(ew)
            lines.append(line); pos+=n
        all_lines.extend(lines[:TARGET_LINES])
    return all_lines

def compute_metrics(all_lines, n_trials):
    trial_size=TARGET_LINES
    trial_metrics=[]
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
        # Menzerath components
        line_lens=[len(l) for l in lines if len(l)>=3]
        line_mean_wl=[sum(len(w) for w in l)/len(l) for l in lines if len(l)>=3]
        ll_wls=[len(l[-1]) for l in lines if len(l)>=3]
        lf_wls=[len(l[0]) for l in lines if len(l)>=3]
        menz_r=pearson_r(line_lens,line_mean_wl)
        r_ll=pearson_r(line_lens,ll_wls)
        # MID slope
        mid_word_indices=[]; mid_word_lens=[]
        for l in lines:
            for idx,w in enumerate(l[1:-1],1):
                mid_word_indices.append(idx); mid_word_lens.append(len(w))
        mid_slope = 0.0
        if len(mid_word_indices) > 2:
            mx=sum(mid_word_indices)/len(mid_word_indices)
            my=sum(mid_word_lens)/len(mid_word_lens)
            num=sum((x-mx)*(y-my) for x,y in zip(mid_word_indices,mid_word_lens))
            denom=sum((x-mx)**2 for x in mid_word_indices)
            mid_slope=num/denom if denom else 0
        # Non-am LL word length by line length bucket (for r_ll decomposition)
        nonam_ll_wl_short=[]  # n<=5
        nonam_ll_wl_long=[]   # n>=10
        for l in lines:
            n=len(l)
            if n<2: continue
            ll_w=l[-1]
            if not ll_w.endswith('am'):
                if n<=5: nonam_ll_wl_short.append(len(ll_w))
                if n>=10: nonam_ll_wl_long.append(len(ll_w))
        nonam_delta = (sum(nonam_ll_wl_long)/len(nonam_ll_wl_long) -
                       sum(nonam_ll_wl_short)/len(nonam_ll_wl_short)) if nonam_ll_wl_short and nonam_ll_wl_long else 0
        metrics={'am_ll':am_ll,'d_ll':d_ll,'y_lf':y_lf,'ss_mean':ss_mean,'adj_rate':adj,
                 'qok_lf':qok_lf,'d_lf':d_lf,'s_lf':s_lf,'ch_ll':ch_ll,'ok_ll':ok_ll,
                 'qok_ll':qok_ll,'ss_d':ss_d,'ss_y':ss_y,'am_lf_enr':am_lf_enr,
                 'am_mid_enr':am_mid_enr,'edy_rate':edy_rate,'word_len_mean':word_len,
                 'qok_ch':qok_ch,'global_am_rate':am_r,
                 'menz_r':menz_r,'r_ll':r_ll,'mid_slope':mid_slope,'nonam_delta':nonam_delta}
        trial_metrics.append(metrics)
    return trial_metrics

def avg_metrics(trial_metrics):
    if not trial_metrics: return {}
    keys=list(trial_metrics[0].keys())
    return {k:sum(m[k] for m in trial_metrics)/len(trial_metrics) for k in keys}

def count_pass(trial_metrics):
    passes=0
    for m in trial_metrics:
        all_pass=True
        for k in BATTERY_19:
            ref=VMS_REF[k]; val=m[k]
            if not (ref*(1-PASS_TOL) <= val <= ref*(1+PASS_TOL)):
                all_pass=False; break
        if all_pass: passes+=1
    return passes

def print_battery(avg, n_trials, pass_count, label):
    print(f"\n{'='*60}")
    print(f"Battery: {label}  [{pass_count}/{n_trials} PASS]")
    print(f"{'='*60}")
    print(f"{'Metric':<18} {'VMS':>8} {'Sim':>8} {'%VMS':>7} {'Status'}")
    print("-"*50)
    for k in BATTERY_19:
        ref=VMS_REF[k]; val=avg.get(k,0)
        pct=val/ref*100 if ref else 0
        status='PASS' if ref*(1-PASS_TOL)<=val<=ref*(1+PASS_TOL) else 'FAIL'
        print(f"{k:<18} {ref:>8.4f} {val:>8.4f} {pct:>6.1f}% {status}")
    print(f"\nMenzerath r: {avg.get('menz_r',0):.4f} ({avg.get('menz_r',0)/(-0.225)*100:.1f}% of VMS -0.225)")
    print(f"r_ll:        {avg.get('r_ll',0):.4f} ({avg.get('r_ll',0)/(-0.219)*100:.1f}% of VMS -0.219)")
    print(f"MID slope:   {avg.get('mid_slope',0):.4f} ({avg.get('mid_slope',0)/(-0.058)*100:.1f}% of VMS -0.058)")
    print(f"nonam_LL_delta (long−short): {avg.get('nonam_delta',0):.3f} chars (VMS: −1.244)")


def main():
    rng=random.Random(SEED)
    print("Loading data...")
    b_lines=parse_vms_b()
    print(f"B-dialect lines: {len(b_lines)} (total words: {sum(len(l) for l in b_lines)})")

    # DIAGNOSTIC
    run_diagnostic(b_lines)

    # Build distributions
    vms_d=compute_vms_dists(b_lines)
    latin_words=load_latin(LATIN_CORPUS)
    print(f"Latin words loaded: {len(latin_words)}")

    sg=vms_d['suffix_global']
    suffix_lf_sup=make_suppressed_suffix(sg,R_LF)
    suffix_mid_sup=make_suppressed_suffix(sg,R_MID)
    lexicons=build_full_vms_lexicons(vms_d['mid_words'],SPARSE_ONSETS)

    # SWEEP: beta_ll_base values
    sweep_conditions = [
        ('baseline', 0.00),
        ('mild',     0.20),
        ('moderate', 0.40),
        ('strong',   0.60),
        ('vstrong',  0.80),
        ('extreme',  1.20),
    ]

    N_SWEEP=10
    sweep_results=[]
    print(f"\n{'='*70}")
    print(f"SWEEP: beta_ll_base values (N={N_SWEEP} each)")
    print(f"{'='*70}")
    print(f"{'Condition':<14} {'Pass':>6} {'menz_r':>8} {'r_ll':>8} {'%rll':>7} "
          f"{'nonam_d':>8} {'am_ll%':>8}")

    for cond_name, beta_ll_base in sweep_conditions:
        rng_cond=random.Random(SEED+hash(cond_name)%100000)
        all_lines=run_sim(latin_words,vms_d,rng_cond,N_SWEEP,beta_ll_base,
                          suffix_lf_sup,suffix_mid_sup,lexicons)
        tms=compute_metrics(all_lines,N_SWEEP)
        passes=count_pass(tms)
        avg=avg_metrics(tms)
        sweep_results.append((cond_name,beta_ll_base,passes,avg))
        am_ll_pct=avg['am_ll']/VMS_REF['am_ll']*100
        rll_pct=avg['r_ll']/(-0.219)*100 if avg['r_ll']!=0 else 0
        print(f"{cond_name:<14} {passes:>4}/{N_SWEEP} {avg['menz_r']:>8.4f} "
              f"{avg['r_ll']:>8.4f} {rll_pct:>6.1f}% "
              f"{avg['nonam_delta']:>8.3f} {am_ll_pct:>7.1f}%")

    # Identify best 19/19-stable condition
    best_cond=None; best_r_ll=-99
    for cond_name,beta_ll_base,passes,avg in sweep_results:
        if passes>=N_SWEEP-1 and avg['r_ll']<best_r_ll:  # more negative = better
            best_r_ll=avg['r_ll']; best_cond=(cond_name,beta_ll_base)
    # If nothing 19/19, take best 18/19
    if best_cond is None:
        for cond_name,beta_ll_base,passes,avg in sweep_results:
            if passes>=N_SWEEP-2 and avg['r_ll']<best_r_ll:
                best_r_ll=avg['r_ll']; best_cond=(cond_name,beta_ll_base)
    if best_cond is None:
        best_cond=('mild',0.20)  # fallback

    print(f"\nBest stable condition: {best_cond[0]} (beta_ll_base={best_cond[1]})")

    # Full N=30 battery on best condition
    N_FULL=30
    print(f"\nRunning full N={N_FULL} battery on {best_cond[0]} (beta_ll_base={best_cond[1]})...")
    rng_full=random.Random(SEED+9999)
    all_lines_full=run_sim(latin_words,vms_d,rng_full,N_FULL,best_cond[1],
                           suffix_lf_sup,suffix_mid_sup,lexicons)
    tms_full=compute_metrics(all_lines_full,N_FULL)
    pass_full=count_pass(tms_full)
    avg_full=avg_metrics(tms_full)
    print_battery(avg_full, N_FULL, pass_full, f"{best_cond[0]} (beta_ll_base={best_cond[1]})")

    # Also run baseline full N=30 for comparison
    print(f"\nRunning baseline N=30 (beta_ll_base=0.00) for comparison...")
    rng_base=random.Random(SEED+8888)
    all_lines_base=run_sim(latin_words,vms_d,rng_base,N_FULL,0.00,
                           suffix_lf_sup,suffix_mid_sup,lexicons)
    tms_base=compute_metrics(all_lines_base,N_FULL)
    pass_base=count_pass(tms_base)
    avg_base=avg_metrics(tms_base)
    print_battery(avg_base, N_FULL, pass_base, "baseline (beta_ll_base=0.00)")

    # Non-am LL_wl bucket analysis for best condition
    print(f"\n{'='*70}")
    print(f"Non-am LL_wl by line-length bucket: best condition vs VMS")
    print(f"{'='*70}")
    bucket_labels=[label for _,_,label in LINE_LEN_BUCKETS]
    vms_nonam_wl=[5.671, 5.404, 5.226, 4.659, 4.426]  # from exp_309 diagnostic
    # Measure sim non-am LL_wl per bucket
    sim_bucket_nonam = {label:[] for label in bucket_labels}
    for l in all_lines_full:
        n=len(l)
        if n<2: continue
        ll_w=l[-1]
        if ll_w.endswith('am'): continue
        for lo,hi,label in LINE_LEN_BUCKETS:
            if lo<=n<=hi: sim_bucket_nonam[label].append(len(ll_w)); break
    print(f"{'Bucket':<12} {'VMS_nonam_wl':>14} {'Sim_nonam_wl':>14} {'N_sim':>8}")
    for (lo,hi,label),vms_wl in zip(LINE_LEN_BUCKETS,vms_nonam_wl):
        sim_wl=sum(sim_bucket_nonam[label])/len(sim_bucket_nonam[label]) if sim_bucket_nonam[label] else 0
        print(f"{label:<12} {vms_wl:>14.3f} {sim_wl:>14.3f} {len(sim_bucket_nonam[label]):>8}")

    print("\nDone.")

if __name__=='__main__':
    main()
