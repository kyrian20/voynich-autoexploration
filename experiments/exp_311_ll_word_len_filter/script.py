"""
exp_311: Line-Length-Conditional LL Word-Length Filter (H513)

exp_310 showed VMS non-am LL_wl gradient is driven by "other"-suffix (unrecognized
ending) words increasing 22.5% → 42.6% in long lines. The correct mechanism is
word-length conditioning: in long lines, VMS uses shorter LL words overall (not shorter
recognized suffixes). The onset+suffix generation currently produces words of fixed
length distribution regardless of line length.

DIAGNOSTIC PHASE:
  What are the actual word lengths of VMS LL words by line length bucket?
  What onset classes do short LL words use? (Are shorter LL words also onset-class-shifted?)

MECHANISM:
  Line-length-conditional word-length filter for LL non-blind path:
  max_ll_len(n) = max(MIN_CAP, base_len - slope * max(0, n - n_ref))
  After generating LL word (onset + suffix), if len(word) > max_ll_len(n):
    - Redraw up to MAX_RETRY times
    - If all draws fail, use the shortest of {all draws, original}

  This directly generates shorter words in longer lines, reproducing the "other"
  category increase (shorter words often fall outside recognized suffix patterns).

19th mechanism candidate.
Architecture baseline: 18-mechanism (cond_mild p_blind, exp_309/310).
"""

import os, re, random, math
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser('~/voynich-cryptanalyst')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

# 18-mechanism architecture (exp_309: cond_mild p_blind)
P_SHORT=0.060; P_LONG=0.180; THRESH_SHORT=5; THRESH_LONG=10; MEAN_N=8.4
P_LF=1.0; CP=0.55; MP=0.90; P_QOKCH=0.12; P_CHQOK=0.12; P_STUTTER=0.006
R_LF=0.12; R_MID=0.20; MU_LEN=8.4; SIGMA_LEN=3.0; P_MF=0.20; P_LF_MF=0.50; P_LL_MF=0.00
GAMMA=0.30; ALPHA=0.20; BETA=0.50
IDX_THRESH=2; SHORT_THRESH=2; TARGET_LINES=2411; WINDOW=20; SEED=311000
MAX_RETRY=10  # max redraws when word exceeds max_ll_len

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
    """18th mechanism: line-length-conditional p_blind (cond_mild from exp_309)."""
    if n <= THRESH_SHORT: return P_SHORT
    if n >= THRESH_LONG: return P_LONG
    frac=(n-THRESH_SHORT)/(THRESH_LONG-THRESH_SHORT)
    return P_SHORT+frac*(P_LONG-P_SHORT)

def get_max_ll_len(n, base_len, slope, n_ref, min_cap=3):
    """19th mechanism: line-length-conditional max LL word length."""
    return max(min_cap, round(base_len - slope * max(0, n - n_ref)))

LINE_LEN_BUCKETS = [(2,4,'n=2-4'), (5,6,'n=5-6'), (7,8,'n=7-8'), (9,10,'n=9-10'), (11,20,'n=11-15')]

# ---------------------------------------------------------------------------
# DIAGNOSTIC: VMS LL word length distribution by bucket
# ---------------------------------------------------------------------------

def run_diagnostic(b_lines):
    print("="*70)
    print("DIAGNOSTIC: VMS LL word length by line length bucket")
    print("="*70)
    bucket_data = {label: {'all_wl':[], 'nonam_wl':[], 'am_cnt':0, 'onset_cnt':Counter()}
                   for _,_,label in LINE_LEN_BUCKETS}
    for line in b_lines:
        n = len(line)
        if n < 2: continue
        ll_word = line[-1]
        for lo,hi,label in LINE_LEN_BUCKETS:
            if lo <= n <= hi:
                bucket_data[label]['all_wl'].append(len(ll_word))
                if ll_word.endswith('am'):
                    bucket_data[label]['am_cnt'] += 1
                else:
                    bucket_data[label]['nonam_wl'].append(len(ll_word))
                    bucket_data[label]['onset_cnt'][get_onset(ll_word)] += 1
                break

    print(f"\n{'Bucket':<12} {'N':>6} {'all_wl':>7} {'nonam_wl':>9} {'am_rate':>8} {'wl<=4%':>8} {'wl<=5%':>8}")
    print("-"*65)
    for lo,hi,label in LINE_LEN_BUCKETS:
        d = bucket_data[label]
        N = len(d['all_wl'])
        all_wl = sum(d['all_wl'])/N if N else 0
        nonam_n = len(d['nonam_wl'])
        nonam_wl = sum(d['nonam_wl'])/nonam_n if nonam_n else 0
        am_rate = d['am_cnt']/N if N else 0
        wl4_pct = sum(1 for w in d['nonam_wl'] if w<=4)/nonam_n*100 if nonam_n else 0
        wl5_pct = sum(1 for w in d['nonam_wl'] if w<=5)/nonam_n*100 if nonam_n else 0
        print(f"{label:<12} {N:>6} {all_wl:>7.3f} {nonam_wl:>9.3f} {am_rate:>8.3f} {wl4_pct:>7.1f}% {wl5_pct:>7.1f}%")

    print("\nTop onset classes for non-am LL words by bucket:")
    for lo,hi,label in LINE_LEN_BUCKETS:
        oc = bucket_data[label]['onset_cnt']
        total = sum(oc.values())
        if total == 0: continue
        top = sorted(oc.items(), key=lambda x:-x[1])[:5]
        top_str = ', '.join(f'{o}:{c/total:.1%}' for o,c in top)
        print(f"  {label}: {top_str}")

    # Short LL word analysis (len<=4) in long lines
    print("\nShort LL word details (len<=4, n>=9 lines):")
    short_ll = []
    for line in b_lines:
        if len(line) < 9: continue
        ll_w = line[-1]
        if not ll_w.endswith('am') and len(ll_w) <= 4:
            short_ll.append(ll_w)
    if short_ll:
        cnt = Counter(short_ll)
        top20 = sorted(cnt.items(), key=lambda x:-x[1])[:20]
        for w,c in top20:
            print(f"  {w}: {c} ({c/len(short_ll):.1%}), onset={get_onset(w)}, suf={get_suffix(w)}")
    print(f"Total short LL words (len<=4, n>=9): {len(short_ll)}")

    # Implied max_ll_len targets
    print("\nImplied max_ll_len targets (95th percentile of nonam_wl per bucket):")
    for lo,hi,label in LINE_LEN_BUCKETS:
        d = bucket_data[label]
        if d['nonam_wl']:
            sorted_wl = sorted(d['nonam_wl'])
            p95 = sorted_wl[int(0.90 * len(sorted_wl))]
            print(f"  {label}: 90th pctile nonam_wl = {p95}")
    print()

# ---------------------------------------------------------------------------
# SIMULATION
# ---------------------------------------------------------------------------

def generate_ll_word(rng, vms_d, suffix_global, n, max_ll_len_val):
    """Generate a non-blind LL word, with length filter."""
    # Try to generate a word within max_ll_len
    candidates = []
    for _ in range(MAX_RETRY + 1):
        onset = weighted_choice(rng, vms_d['onset_ll'])
        suf = weighted_choice(rng, suffix_global)
        ew = make_word_sim(onset, suf, rng, vms_d['ll_nemed'], P_LL_MF)
        if len(ew) <= max_ll_len_val:
            return ew
        candidates.append(ew)
    # Fallback: return shortest of all candidates
    return min(candidates, key=len)

def run_sim(latin_words, vms_d, rng, n_trials, base_len, slope, n_ref,
            suffix_lf_sup, suffix_mid_sup, lexicons):
    """Run simulation with 18-mechanism architecture + word-length filter for LL."""
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
            max_ll = get_max_ll_len(n, base_len, slope, n_ref)
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
                    # LL: 18th mechanism p_blind + 19th mechanism word-length filter
                    if rng.random()<p_blind_n:
                        onset=weighted_choice(rng,vms_d['ll_onsets'])
                        ew=onset+'am'
                    else:
                        ew = generate_ll_word(rng, vms_d, vms_d['suffix_global'], n, max_ll)
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
        menz_r=pearson_r(line_lens,line_mean_wl)
        r_ll=pearson_r(line_lens,ll_wls)
        mid_word_indices=[]; mid_word_lens=[]
        for l in lines:
            for idx,w in enumerate(l[1:-1],1):
                mid_word_indices.append(idx); mid_word_lens.append(len(w))
        mid_slope = 0.0
        if len(mid_word_indices) > 2:
            mx2=sum(mid_word_indices)/len(mid_word_indices)
            my2=sum(mid_word_lens)/len(mid_word_lens)
            num=sum((x-mx2)*(y-my2) for x,y in zip(mid_word_indices,mid_word_lens))
            denom=sum((x-mx2)**2 for x in mid_word_indices)
            mid_slope=num/denom if denom else 0
        # nonam LL_wl delta (long−short)
        nonam_short=[]; nonam_long=[]
        for l in lines:
            n_l=len(l)
            if n_l<2: continue
            ll_w=l[-1]
            if ll_w.endswith('am'): continue
            if n_l<=5: nonam_short.append(len(ll_w))
            elif n_l>=10: nonam_long.append(len(ll_w))
        nonam_delta=(sum(nonam_long)/len(nonam_long)-sum(nonam_short)/len(nonam_short)) if nonam_short and nonam_long else 0
        metrics={'am_ll':am_ll,'d_ll':d_ll,'y_lf':y_lf,'ss_mean':ss_mean,'adj_rate':adj,
                 'qok_lf':qok_lf,'d_lf':d_lf,'s_lf':s_lf,'ch_ll':ch_ll,'ok_ll':ok_ll,
                 'qok_ll':qok_ll,'ss_d':ss_d,'ss_y':ss_y,'am_lf_enr':am_lf_enr,
                 'am_mid_enr':am_mid_enr,'edy_rate':edy_rate,'word_len_mean':word_len,
                 'qok_ch':qok_ch,'global_am_rate':am_r,
                 'menz_r':menz_r,'r_ll':r_ll,'mid_slope':mid_slope,'nonam_delta':nonam_delta}
        trial_metrics.append(metrics)
    return trial_metrics

def agg(trial_metrics, key):
    return sum(m[key] for m in trial_metrics)/len(trial_metrics) if trial_metrics else 0

def metric_pass(trial_metrics, key):
    v=agg(trial_metrics,key); ref=VMS_REF[key]
    return ref*(1-PASS_TOL)<=v<=ref*(1+PASS_TOL)

def count_pass_metrics(trial_metrics):
    return sum(1 for k in BATTERY_19 if metric_pass(trial_metrics,k))

def print_battery_full(trial_metrics, label):
    n=len(trial_metrics); pass_count=count_pass_metrics(trial_metrics)
    print(f"\n{'='*60}")
    print(f"Battery: {label}  [{pass_count}/19 metrics PASS]")
    print(f"{'='*60}")
    print(f"{'Metric':<18} {'VMS':>8} {'Sim':>8} {'%VMS':>7} {'Status'}")
    print("-"*50)
    for k in BATTERY_19:
        ref=VMS_REF[k]; val=agg(trial_metrics,k)
        pct=val/ref*100 if ref else 0
        status='PASS' if metric_pass(trial_metrics,k) else 'FAIL'
        print(f"{k:<18} {ref:>8.4f} {val:>8.4f} {pct:>6.1f}% {status}")
    mr=agg(trial_metrics,'menz_r'); rll=agg(trial_metrics,'r_ll')
    ms=agg(trial_metrics,'mid_slope'); nd=agg(trial_metrics,'nonam_delta')
    print(f"\nMenzerath r: {mr:.4f} ({mr/(-0.225)*100:.1f}% of VMS -0.225)")
    print(f"r_ll:        {rll:.4f} ({rll/(-0.219)*100:.1f}% of VMS -0.219)")
    print(f"MID slope:   {ms:.4f} ({ms/(-0.058)*100:.1f}% of VMS -0.058)")
    print(f"nonam_delta: {nd:.3f} chars (VMS: -1.244, coverage: {nd/(-1.244)*100:.1f}%)")


def main():
    rng=random.Random(SEED)
    print("Loading data...")
    b_lines=parse_vms_b()
    print(f"B-dialect lines: {len(b_lines)} (words: {sum(len(l) for l in b_lines)})")

    # DIAGNOSTIC
    run_diagnostic(b_lines)

    # Build distributions
    vms_d=compute_vms_dists(b_lines)
    latin_words=load_latin(LATIN_CORPUS)
    print(f"Latin words: {len(latin_words)}")

    sg=vms_d['suffix_global']
    suffix_lf_sup=make_suppressed_suffix(sg,R_LF)
    suffix_mid_sup=make_suppressed_suffix(sg,R_MID)
    lexicons=build_full_vms_lexicons(vms_d['mid_words'],SPARSE_ONSETS)

    # SWEEP: (base_len, slope, n_ref) conditions
    # max_ll_len(n) = max(3, round(base_len - slope * max(0, n - n_ref)))
    # For n=3: no cap applied (n<n_ref=5 → max=base_len ≈ 8)
    # For n=12: max = base_len - slope * (12 - n_ref)
    sweep_conditions = [
        # (name, base_len, slope, n_ref)
        ('baseline',    8,  0.00, 6),   # no filter
        ('mild_s20',    8,  0.20, 5),   # n=12→max=6.6≈7; n=15→max=6
        ('mild_s30',    8,  0.30, 5),   # n=12→max=5.9≈6; n=15→max=5
        ('mod_s30',     7,  0.30, 5),   # n=12→max=4.9≈5; n=15→max=4
        ('mod_s40',     8,  0.40, 5),   # n=12→max=5.2≈5; n=15→max=4
        ('strong_s50',  8,  0.50, 5),   # n=12→max=4.5≈5; n=15→max=3
        ('strong_s40b', 7,  0.40, 5),   # n=12→max=4.2≈4; n=15→max=3
    ]

    N_SWEEP=10
    print(f"\n{'='*70}")
    print(f"SWEEP: word-length filter conditions (N={N_SWEEP} each, metric-level)")
    print(f"{'='*70}")
    print(f"  max_ll_len(n) = max(3, round(base_len - slope * max(0, n - n_ref)))")
    print(f"  Example values for selected conditions:")
    for nm,bl,sl,nr in sweep_conditions:
        n3=get_max_ll_len(3,bl,sl,nr); n8=get_max_ll_len(8,bl,sl,nr)
        n12=get_max_ll_len(12,bl,sl,nr); n15=get_max_ll_len(15,bl,sl,nr)
        print(f"    {nm:<14}: n=3→{n3}, n=8→{n8}, n=12→{n12}, n=15→{n15}")
    print()
    print(f"{'Condition':<16} {'Pass':>7} {'menz_r':>8} {'r_ll':>8} {'%rll':>7} "
          f"{'nonam_d':>8} {'wl_mean%':>9}")

    sweep_results=[]
    for nm,bl,sl,nr in sweep_conditions:
        rng_c=random.Random(SEED+hash(nm)%100000)
        all_lines=run_sim(latin_words,vms_d,rng_c,N_SWEEP,bl,sl,nr,
                          suffix_lf_sup,suffix_mid_sup,lexicons)
        tms=compute_metrics(all_lines,N_SWEEP)
        pass_cnt=count_pass_metrics(tms)
        mr=agg(tms,'menz_r'); rll=agg(tms,'r_ll')
        nd=agg(tms,'nonam_delta'); wl=agg(tms,'word_len_mean')
        rll_pct=rll/(-0.219)*100 if rll!=0 else 0
        wl_pct=wl/VMS_REF['word_len_mean']*100
        sweep_results.append((nm,bl,sl,nr,pass_cnt,mr,rll,nd,tms))
        print(f"{nm:<16} {pass_cnt:>4}/19 {mr:>8.4f} {rll:>8.4f} {rll_pct:>6.1f}% "
              f"{nd:>8.3f} {wl_pct:>8.1f}%")

    # Find best condition: maximize r_ll (most negative) subject to 18/19 or 19/19
    best_19=max((r for r in sweep_results if r[4]>=19),key=lambda r:abs(r[6]),default=None)
    best_18=max((r for r in sweep_results if r[4]>=18),key=lambda r:abs(r[6]),default=None)
    best=best_19 or best_18 or sweep_results[0]
    best_nm,best_bl,best_sl,best_nr=best[0],best[1],best[2],best[3]
    print(f"\nBest condition: {best_nm} (base_len={best_bl}, slope={best_sl}, n_ref={best_nr})")

    # Full N=30 battery on best
    N_FULL=30
    print(f"\nRunning full N={N_FULL} battery on {best_nm}...")
    rng_full=random.Random(SEED+7777)
    all_full=run_sim(latin_words,vms_d,rng_full,N_FULL,best_bl,best_sl,best_nr,
                     suffix_lf_sup,suffix_mid_sup,lexicons)
    tms_full=compute_metrics(all_full,N_FULL)
    print_battery_full(tms_full, f"{best_nm} (base={best_bl},slope={best_sl},n_ref={best_nr})")

    # nonam LL_wl bucket analysis for best condition
    print(f"\n{'='*70}")
    print(f"Non-am LL_wl by bucket: best condition vs VMS")
    print(f"{'='*70}")
    vms_nonam=[5.671,5.404,5.226,4.659,4.426]
    sim_bucket={label:[] for _,_,label in LINE_LEN_BUCKETS}
    for l in all_full:
        n_l=len(l)
        if n_l<2: continue
        ll_w=l[-1]
        if ll_w.endswith('am'): continue
        for lo,hi,label in LINE_LEN_BUCKETS:
            if lo<=n_l<=hi: sim_bucket[label].append(len(ll_w)); break
    print(f"{'Bucket':<12} {'VMS':>10} {'Sim':>10} {'Delta_VMS':>12} {'Delta_Sim':>12}")
    vms_d0=None; sim_d0=None
    for (lo,hi,label),vwl in zip(LINE_LEN_BUCKETS,vms_nonam):
        swl=sum(sim_bucket[label])/len(sim_bucket[label]) if sim_bucket[label] else 0
        if vms_d0 is None: vms_d0=vwl; sim_d0=swl
        dv=vwl-vms_d0; ds=swl-sim_d0
        print(f"{label:<12} {vwl:>10.3f} {swl:>10.3f} {dv:>+12.3f} {ds:>+12.3f}")

    # Also run full baseline for comparison (same seed)
    print(f"\nRunning baseline N={N_FULL} (no filter) with same seed...")
    rng_base=random.Random(SEED+7777)
    all_base=run_sim(latin_words,vms_d,rng_base,N_FULL,8,0.00,6,
                     suffix_lf_sup,suffix_mid_sup,lexicons)
    tms_base=compute_metrics(all_base,N_FULL)
    print_battery_full(tms_base, "baseline (no filter)")

    print("\nDone.")

if __name__=='__main__':
    main()
