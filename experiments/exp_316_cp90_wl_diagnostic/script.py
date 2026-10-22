"""
exp_316: CP90 Ratios and Word-Length Component Diagnostic with 21-Mechanism Architecture (H519)

Two measurements:
(A) CP90 ratios for all 7 major onset classes (qok, ok, ot, qot, sh, ch, d):
    VMS B-dialect MID words vs 21-mechanism simulation (N=30 aggregate).
    Last measurement (exp_302) used 16-mechanism architecture.
    Since then: vocabulary clamping for qok/ok/ot/qot (17th mech) and beta_scale=1.8 (21st mech).

(B) Word-length component analysis per onset class:
    VMS vs simulation: mean onset_len, midfix_len, suffix_len, total word_len.
    H494 (never run): which component drives the 22% word-length overproduction?

Architecture: 21-mechanism (exp_314 baseline: beta_scale=1.8, all prior mechanisms).
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
SHORT_THRESH=2; TARGET_LINES=2411; WINDOW=20; SEED=316000
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

# Onset classes to measure in detail
MAJOR_ONSETS=['qok','ok','ot','qot','sh','ch','d']

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label
    return 'other'
def get_onset_len(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return len(prefix)
    return len(w)  # fallback: full word
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
    """Return number of types needed to cover 90% of tokens."""
    cnt=Counter(word_list)
    total=sum(cnt.values())
    if total==0: return 0
    threshold=0.90*total
    cumulative=0
    for i,(w,c) in enumerate(cnt.most_common(),1):
        cumulative+=c
        if cumulative>=threshold: return i
    return len(cnt)

def compute_wl_components(word_list):
    """Compute mean onset_len, midfix_len, suffix_len, total_len per word."""
    onset_lens=[]; midfix_lens=[]; suffix_lens=[]; total_lens=[]
    for w in word_list:
        total_lens.append(len(w))
        ol=get_onset_len(w)
        onset_lens.append(ol)
        suf=get_suffix(w)
        if suf=='other':
            suffix_lens.append(0)
            midfix_lens.append(max(0, len(w)-ol))
        else:
            sl=len(suf)
            suffix_lens.append(sl)
            edy_len=get_edy_suffix_len(w)
            if edy_len>0:
                mid_end=len(w)-edy_len
                midfix=w[ol:mid_end]
                # strip edy connector char
                midfix=midfix[:-1] if len(midfix)>=1 else midfix
                midfix_lens.append(len(midfix))
            else:
                midfix_lens.append(max(0, len(w)-ol-sl))
    def mean(lst): return sum(lst)/len(lst) if lst else 0.0
    return {'onset_len':mean(onset_lens), 'midfix_len':mean(midfix_lens),
            'suffix_len':mean(suffix_lens), 'total_len':mean(total_lens), 'n':len(word_list)}

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

def run_sim(latin_words, vms_d, rng, n_trials, suffix_lf_sup, suffix_mid_sup, lexicons):
    """Run 21-mechanism simulation, return (all_lines, mid_words_by_onset)."""
    all_lines=[]
    mid_words_by_onset=defaultdict(list)
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
                    onset_label=get_onset(ew)
                    mid_words_by_onset[onset_label].append(ew)
                    buf.append(ew); word_idx+=1
                prev_onset=get_onset(ew); prev_word=ew; line.append(ew)
            lines.append(line); pos+=n
        all_lines.extend(lines[:TARGET_LINES])
    return all_lines, dict(mid_words_by_onset)

def measure_cp90_and_wl(words_by_onset):
    """For each onset class, compute CP90 and word-length components."""
    results={}
    for onset in MAJOR_ONSETS:
        wl=words_by_onset.get(onset,[])
        if not wl:
            results[onset]={'cp90':0, 'n_tokens':0, 'n_types':0}
            continue
        cp90=compute_cp90(wl)
        components=compute_wl_components(wl)
        results[onset]={'cp90':cp90,'n_tokens':len(wl),'n_types':len(set(wl)),**components}
    return results

def main():
    rng=random.Random(SEED)
    print("Loading data...")
    b_lines=parse_vms_b()
    print(f"B-dialect lines: {len(b_lines)} (words: {sum(len(l) for l in b_lines)})")

    # VMS MID words by onset
    vms_mid_words=[w for l in b_lines for w in l[1:-1] if len(l)>2]
    vms_mid_by_onset=defaultdict(list)
    for w in vms_mid_words: vms_mid_by_onset[get_onset(w)].append(w)

    # VMS CP90 and WL components
    print("\n--- VMS B-dialect MID words ---")
    vms_results=measure_cp90_and_wl(dict(vms_mid_by_onset))

    print(f"\n{'Onset':<6} {'Tokens':>7} {'Types':>7} {'CP90':>6} {'Onset_L':>8} {'Mid_L':>7} {'Suf_L':>7} {'Total_L':>8}")
    print("-"*60)
    for onset in MAJOR_ONSETS:
        r=vms_results.get(onset,{})
        print(f"{onset:<6} {r.get('n_tokens',0):>7} {r.get('n_types',0):>7} {r.get('cp90',0):>6} "
              f"{r.get('onset_len',0.0):>8.3f} {r.get('midfix_len',0.0):>7.3f} "
              f"{r.get('suffix_len',0.0):>7.3f} {r.get('total_len',0.0):>8.3f}")

    # Also compute overall VMS MID word-length components
    vms_overall=compute_wl_components(vms_mid_words)
    print(f"\nVMS overall MID: onset={vms_overall['onset_len']:.3f}, midfix={vms_overall['midfix_len']:.3f}, "
          f"suffix={vms_overall['suffix_len']:.3f}, total={vms_overall['total_len']:.3f}")

    # Run simulation
    print("\n--- 21-mechanism simulation (N=30 trials) ---")
    latin_words=load_latin(LATIN_CORPUS)
    vms_d=compute_vms_dists(b_lines)
    lexicons=build_full_vms_lexicons(vms_d['mid_words'],SPARSE_ONSETS)
    suffix_global=vms_d['suffix_global']
    suffix_lf_sup=make_suppressed_suffix(suffix_global,R_LF)
    suffix_mid_sup=make_suppressed_suffix(suffix_global,R_MID)

    rng2=random.Random(SEED+99999)
    all_lines, sim_mid_by_onset=run_sim(latin_words, vms_d, rng2, N_TRIALS,
                                         suffix_lf_sup, suffix_mid_sup, lexicons)
    sim_results=measure_cp90_and_wl(sim_mid_by_onset)

    # Also compute overall sim MID word-length components
    sim_mid_words=[]
    for onset in MAJOR_ONSETS:
        sim_mid_words.extend(sim_mid_by_onset.get(onset,[]))
    # Add 'other' onset words too for overall total
    all_sim_mid=[w for onset_wl in sim_mid_by_onset.values() for w in onset_wl]
    sim_overall=compute_wl_components(all_sim_mid)

    print(f"\n{'Onset':<6} {'Tokens':>7} {'Types':>7} {'CP90':>6} {'Onset_L':>8} {'Mid_L':>7} {'Suf_L':>7} {'Total_L':>8}")
    print("-"*60)
    for onset in MAJOR_ONSETS:
        r=sim_results.get(onset,{})
        print(f"{onset:<6} {r.get('n_tokens',0):>7} {r.get('n_types',0):>7} {r.get('cp90',0):>6} "
              f"{r.get('onset_len',0.0):>8.3f} {r.get('midfix_len',0.0):>7.3f} "
              f"{r.get('suffix_len',0.0):>7.3f} {r.get('total_len',0.0):>8.3f}")

    print(f"\nSim overall MID: onset={sim_overall['onset_len']:.3f}, midfix={sim_overall['midfix_len']:.3f}, "
          f"suffix={sim_overall['suffix_len']:.3f}, total={sim_overall['total_len']:.3f}")

    # CP90 ratio table
    print("\n--- CP90 Ratio Table (sim / VMS) ---")
    print(f"{'Onset':<6} {'VMS_CP90':>9} {'Sim_CP90':>9} {'Ratio':>7} {'VMS_Types':>10} {'Sim_Types':>10}")
    print("-"*55)
    for onset in MAJOR_ONSETS:
        vr=vms_results.get(onset,{})
        sr=sim_results.get(onset,{})
        vcp=vr.get('cp90',0); scp=sr.get('cp90',0)
        ratio=scp/vcp if vcp>0 else float('nan')
        vt=vr.get('n_types',0); st=sr.get('n_types',0)
        print(f"{onset:<6} {vcp:>9} {scp:>9} {ratio:>7.2f}x {vt:>10} {st:>10}")

    # Word-length component comparison
    print("\n--- Word-Length Component Comparison ---")
    print(f"{'Onset':<6} {'Component':<12} {'VMS':>7} {'Sim':>7} {'Sim/VMS':>8}")
    print("-"*45)
    for onset in MAJOR_ONSETS:
        vr=vms_results.get(onset,{})
        sr=sim_results.get(onset,{})
        for comp in ['onset_len','midfix_len','suffix_len','total_len']:
            vv=vr.get(comp,0); sv=sr.get(comp,0)
            ratio=sv/vv if vv>0 else float('nan')
            print(f"{onset:<6} {comp:<12} {vv:>7.3f} {sv:>7.3f} {ratio:>8.3f}x")
        print()

    # Overall word-length comparison
    print("--- Overall MID Word-Length Component Comparison ---")
    for comp in ['onset_len','midfix_len','suffix_len','total_len']:
        vv=vms_overall.get(comp,0); sv=sim_overall.get(comp,0)
        ratio=sv/vv if vv>0 else float('nan')
        print(f"  {comp:<12}: VMS={vv:.3f}  Sim={sv:.3f}  Ratio={ratio:.3f}x")

    print("\nDone.")

if __name__=='__main__':
    main()
