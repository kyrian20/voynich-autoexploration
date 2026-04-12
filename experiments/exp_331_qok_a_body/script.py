"""
exp_331: qok 'a'-Body Analysis — Are qok+'a'-Body Words Part of the aiin-Body Paradigm? (H531)

Background:
- F330 (exp_328): ok+'a'-body = d-onset doublets (okaiin/daiin, okain/dain, etc.)
- F323 (exp_321): qok B0: 'e'=48%, 'a'=36%
- Top qok 'a'-body words: qokain(221), qokaiin(197), qokal(128), qokar(105) — 4 of top 7 qok words

Question: Do qok+'a'-body words form onset-substitution doublets with d-onset words?
If qokain body = 'ain' = dain body = 'ain', then qok and d share the same body vocabulary.
"""

import os, re
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser('~/voynich-cryptanalyst')
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

ONSET_ORDER=[
    ('qok','qok'),('qot','qot'),('qo','qo'),('cth','cth'),
    ('ch','ch'),('sh','sh'),('ok','ok'),('ot','ot'),('ol','ol'),
    ('d','d'),('s','s'),('y','y'),('k','k'),('t','t'),
    ('l','l'),('r','r'),('p','p'),('f','f'),('o','o'),
]

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label
    return 'other'

def folio_base(folio): return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total=stats['total']
    if total==0: return 'unknown'
    return 'B' if (stats['edy']+stats['eedy'])/total>=0.05 else 'A'

def parse_vms():
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
    mid_words_by_dialect={'A':[],'B':[]}
    with open(DATA_PATH,'r',encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line or line.startswith('#'): continue
            m=re.match(r'<([^.]+)\.(\d+),([^>]+)>',line)
            if not m: continue
            folio_raw=m.group(1); locus_code=m.group(3)
            folio=folio_raw.lstrip('+*=&~'); fb=folio_base(folio)
            dialect=folio_dialect.get(fb,'unknown')
            if dialect not in ('A','B'): continue
            lc_stripped=locus_code.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            text=re.sub(r'<[^>]+>','',line)
            words=[w for w in re.split(r'[-.\s]',text) if re.match(r'^[a-z]+$',w) and len(w)>=2]
            if len(words)<3: continue
            mid=words[1:-1]
            for w in mid:
                mid_words_by_dialect[dialect].append(w)
    return mid_words_by_dialect

print("Loading corpus...")
words_by_d = parse_vms()

# Onset lengths
ONSET_LEN = {'qok':3,'qot':3,'qo':2,'cth':3,'ch':2,'sh':2,'ok':2,'ot':2,'ol':2,
             'd':1,'s':1,'y':1,'k':1,'t':1,'l':1,'r':1,'p':1,'f':1,'o':1}

def get_body(w, onset_label):
    l = ONSET_LEN.get(onset_label, 1)
    return w[l:] if len(w) > l else ''

def analyze_qok_body(words, dialect):
    print(f"\n{'='*70}")
    print(f"qok-ONSET BODY STRUCTURE ({dialect})")
    print(f"{'='*70}")
    
    qok_words = [w for w in words if get_onset(w) == 'qok']
    total = len(qok_words)
    
    # B0 distribution
    b0_counts = Counter()
    for w in qok_words:
        body = get_body(w, 'qok')
        b0 = body[0] if body else ''
        b0_counts[b0] += 1
    
    print(f"\nTotal qok MID tokens: {total}")
    print("\nB0 distribution:")
    for c, n in b0_counts.most_common(8):
        print(f"  '{c}': {n} ({100*n/total:.1f}%)")
    
    # Top 30 qok words
    qok_type_counts = Counter(qok_words)
    e_words = Counter(w for w in qok_words if get_body(w,'qok')[:1] == 'e')
    a_words = Counter(w for w in qok_words if get_body(w,'qok')[:1] == 'a')
    
    n_e = sum(e_words.values())
    n_a = sum(a_words.values())
    print(f"\nPartition: 'e'-body={n_e} ({100*n_e/total:.1f}%), 'a'-body={n_a} ({100*n_a/total:.1f}%)")
    
    # Build doublet table: qok+'a' vs d-onset
    d_words = Counter(w for w in words if get_onset(w) == 'd')
    d_total = sum(d_words.values())
    
    print(f"\nTop qok 'a'-body words vs d-onset doublets:")
    print(f"{'qok_word':<20} {'qok_N':>7} {'d_analogue':<20} {'d_N':>7} {'doublet?'}")
    print("-"*65)
    for w, cnt in a_words.most_common(15):
        body = get_body(w, 'qok')
        d_analogue = 'd' + body
        d_cnt = d_words.get(d_analogue, 0)
        doublet = '✓' if d_cnt > 0 else '✗'
        print(f"{w:<20} {cnt:>7} {d_analogue:<20} {d_cnt:>7} {doublet}")
    
    print(f"\nTop qok 'e'-body words vs ok/'e' analogues:")
    print(f"{'qok_word':<20} {'qok_N':>7} {'ok_analogue':<20} {'ok_N':>7}")
    ok_words = Counter(w for w in words if get_onset(w) == 'ok')
    print("-"*60)
    for w, cnt in e_words.most_common(10):
        body = get_body(w, 'qok')
        ok_analogue = 'ok' + body
        ok_cnt = ok_words.get(ok_analogue, 0)
        print(f"{w:<20} {cnt:>7} {ok_analogue:<20} {ok_cnt:>7}")
    
    # Summary: how many aiin-body vocabulary words exist in all 5 onset classes?
    print(f"\n--- COMPLETE aiin-BODY DOUBLET TABLE ---")
    print(f"Body vocabulary that appears in ALL onset classes (qok/ok/ot/d/s):")
    
    onset_words = {
        'qok': Counter(w for w in words if get_onset(w) == 'qok'),
        'ok':  Counter(w for w in words if get_onset(w) == 'ok'),
        'ot':  Counter(w for w in words if get_onset(w) == 'ot'),
        'd':   Counter(w for w in words if get_onset(w) == 'd'),
        's':   Counter(w for w in words if get_onset(w) == 's'),
    }
    
    core_bodies = ['aiin', 'ain', 'ar', 'al', 'ol', 'air', 'or', 'am']
    
    print(f"\n{'body':<8}", end='')
    for o in ['qok','ok','ot','d','s']:
        print(f" {o:>8}", end='')
    print(f"  {'in_n_classes':>12}")
    print("-"*60)
    
    for body in core_bodies:
        counts = {}
        for o in ['qok','ok','ot','d','s']:
            word = o + body
            counts[o] = onset_words[o].get(word, 0)
        n_present = sum(1 for c in counts.values() if c > 0)
        print(f"{body:<8}", end='')
        for o in ['qok','ok','ot','d','s']:
            c = counts[o]
            mark = f"{c:>8}" if c > 0 else "        -"
            print(f" {mark}", end='')
        print(f"  {'*'*n_present} ({n_present}/5)")

analyze_qok_body(words_by_d['B'], 'B')
analyze_qok_body(words_by_d['A'], 'A')
