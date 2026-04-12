"""
exp_333: ch/sh Body Vocabulary — Do ch and sh Participate in the 7-Onset × 7-Body Doublet System? (H536)

Background:
- F333 (exp_331): Complete 5-onset × 7-body doublet system confirmed for {qok,ok,ot,d,s}
- Quick check showed: char(B=28,A=27), chol(B=65,A=209), shaiin(B=3,A=14), shol(B=40,A=84)
- ch and sh DO have aiin-body forms — potentially extending the system to 7 onsets

Questions:
1. Complete 7-onset × 7-body table (adding ch and sh to the 5-onset table from F333)
2. Which bodies are shared vs exclusive to specific onsets?
3. A/B dialect differences in which onset-body combinations are populated
4. How do ch/sh 'a'-body rates compare to their overall B0 distributions?
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
            for w in words[1:-1]:
                mid_words_by_dialect[dialect].append(w)
    return mid_words_by_dialect

print("Loading corpus...")
words_by_d = parse_vms()

# Complete 7-onset × 7-body doublet table
ALL_ONSETS_7 = ['qok', 'ok', 'ot', 'd', 's', 'ch', 'sh']
CORE_BODIES = ['aiin', 'ain', 'ar', 'al', 'ol', 'air', 'or', 'am']

ONSET_LENS = {'qok':3,'ok':2,'ot':2,'d':1,'s':1,'ch':2,'sh':2}

def build_onset_words(words, onsets):
    return {o: Counter(w for w in words if get_onset(w) == o) for o in onsets}

def analyze_7onset_table(words, dialect):
    print(f"\n{'='*70}")
    print(f"COMPLETE 7-ONSET × 8-BODY DOUBLET TABLE — {dialect}")
    print(f"{'='*70}")
    
    onset_words = build_onset_words(words, ALL_ONSETS_7)
    onset_totals = {o: sum(onset_words[o].values()) for o in ALL_ONSETS_7}
    
    print(f"\nOnset token counts: " + ", ".join(f"{o}={onset_totals[o]}" for o in ALL_ONSETS_7))
    
    print(f"\n{'Body':<8}", end='')
    for o in ALL_ONSETS_7:
        print(f" {o:>10}", end='')
    print(f"  {'coverage':>10}")
    print("-"*90)
    
    body_coverage = {}
    for body in CORE_BODIES:
        row = {}
        for o in ALL_ONSETS_7:
            word = o + body
            row[o] = onset_words[o].get(word, 0)
        
        n_present = sum(1 for c in row.values() if c > 0)
        body_coverage[body] = n_present
        
        print(f"{body:<8}", end='')
        for o in ALL_ONSETS_7:
            c = row[o]
            s = f"{c}" if c > 0 else '-'
            print(f" {s:>10}", end='')
        print(f"  {'*'*n_present} ({n_present}/7)")
    
    # Check e-body table too (template forms)
    print(f"\n{'='*40}")
    print(f"'e'-body template forms (same pattern):")
    print(f"{'e-body':<10}", end='')
    for o in ALL_ONSETS_7:
        print(f" {o:>10}", end='')
    print()
    
    for ebody in ['edy', 'eedy', 'eey', 'ey', 'eol', 'eol', 'eor']:
        row = {}
        for o in ALL_ONSETS_7:
            word = o + ebody
            row[o] = onset_words[o].get(word, 0)
        
        n_present = sum(1 for c in row.values() if c > 0)
        if max(row.values()) < 1: continue
        print(f"{ebody:<10}", end='')
        for o in ALL_ONSETS_7:
            c = row[o]
            s = f"{c}" if c > 0 else '-'
            print(f" {s:>10}", end='')
        print(f"  ({n_present}/7)")
    
    # ch/sh 'a'-body fraction vs overall B0
    print(f"\n--- ch/sh 'a'-body participation rates ---")
    for o in ['ch', 'sh']:
        total = onset_totals[o]
        a_body_count = sum(onset_words[o][o+body] for body in CORE_BODIES)
        if total > 0:
            print(f"  {o}: total={total}, 'a'-body count (8 core)={a_body_count} ({100*a_body_count/total:.1f}%)")
    
    print(f"\n  Compare: d 'a'-body fraction = {100*sum(onset_words['d']['d'+body] for body in CORE_BODIES)/onset_totals['d']:.1f}%" if onset_totals['d']>0 else '')
    print(f"  Compare: qok 'a'-body fraction = {100*sum(onset_words['qok']['qok'+body] for body in CORE_BODIES)/onset_totals['qok']:.1f}%" if onset_totals['qok']>0 else '')
    
    return body_coverage

b_coverage = analyze_7onset_table(words_by_d['B'], 'B')
a_coverage = analyze_7onset_table(words_by_d['A'], 'A')

# Cross-dialect comparison: for each body, which onset coverage matches/differs?
print(f"\n{'='*70}")
print(f"CROSS-DIALECT CONSISTENCY")
print(f"{'='*70}")
print(f"\n{'Body':<8} {'B_coverage':>12} {'A_coverage':>12} {'consistent?'}")
for body in CORE_BODIES:
    bc = b_coverage[body]
    ac = a_coverage[body]
    mark = '✓' if abs(bc - ac) <= 1 else '✗'
    print(f"{body:<8} {bc:>12}/7 {ac:>12}/7 {mark}")
