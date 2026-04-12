"""
exp_335: ch/sh Body-Class MID Position Split — Do ch+'a'-Body Words Appear Later Than ch+'e'-Body Words? (H538)

Background:
- F331 (exp_329): ot+'a'-body words significantly later than ot+'e'-body words (z=2.67σ, 0.619 vs 0.558)
- ok+'a'-body vs ok+'e'-body NOT significantly different (z=0.75)
- ch has bimodal body structure: 'e'-body dominant (chedy/cheedy/cheey) + minority 'a'-body (chol/char/chor)
- F335: ch 'a'-body B=6.2%, A=28.0% — ch is template-dominant but participates in 'a'-body

Questions:
1. Do ch+'e'-body words (chedy, cheedy, cheey, chey) appear at EARLIER MID positions than ch+'a'-body words (chol, char, chor, chaiin)?
2. Same question for sh-onset (shedy/sheedy/sheey vs shol/shar/shor/shaiin)
3. Generalize: for ALL onset classes, does 'a'-body appear later than 'e'-body?
4. Compare z-scores: ot (z=2.67) vs ch vs sh vs ok (z=0.75) vs qok
"""

import os, re
from collections import Counter, defaultdict
import statistics

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

def get_b0(w, onset_label):
    onset_len = {'qok':3,'qot':3,'qo':2,'cth':3,'ch':2,'sh':2,'ok':2,'ot':2,'ol':2,
                 'd':1,'s':1,'y':1,'k':1,'t':1,'l':1,'r':1,'p':1,'f':1,'o':1}.get(onset_label, 1)
    body = w[onset_len:]
    return body[0] if body else ''

def folio_base(folio): return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total=stats['total']
    if total==0: return 'unknown'
    return 'B' if (stats['edy']+stats['eedy'])/total>=0.05 else 'A'

def parse_vms_with_positions():
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

    # (word, onset, b0, norm_pos, dialect)
    records = []
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
            mid = words[1:-1]
            span = len(mid)
            for idx, w in enumerate(mid):
                npos = idx / (span - 1) if span > 1 else 0.5
                onset = get_onset(w)
                b0 = get_b0(w, onset)
                records.append((w, onset, b0, npos, dialect))
    return records

print("Loading corpus...")
records = parse_vms_with_positions()

def body_class(w, onset_label):
    """Classify word body as 'e'-body or 'a'-body based on body[0]"""
    onset_len = {'qok':3,'qot':3,'qo':2,'cth':3,'ch':2,'sh':2,'ok':2,'ot':2,'ol':2,
                 'd':1,'s':1,'y':1,'k':1,'t':1,'l':1,'r':1,'p':1,'f':1,'o':1}.get(onset_label, 1)
    body = w[onset_len:]
    if not body: return 'other'
    if body[0] == 'e': return 'e-body'
    if body[0] == 'a': return 'a-body'
    if body[0] == 'o': return 'o-body'
    return 'other'

def z_test_means(pos_a, pos_b):
    """Two-sample z-test for difference in means"""
    if len(pos_a) < 5 or len(pos_b) < 5:
        return float('nan'), float('nan'), float('nan')
    mean_a = statistics.mean(pos_a)
    mean_b = statistics.mean(pos_b)
    var_a = statistics.variance(pos_a)
    var_b = statistics.variance(pos_b)
    se = (var_a/len(pos_a) + var_b/len(pos_b)) ** 0.5
    if se == 0: return mean_a - mean_b, 0, 0
    z = (mean_a - mean_b) / se
    return mean_a - mean_b, z, se

def analyze_body_position_split(records, dialect, onset_label):
    """For a given onset class and dialect, compare 'e'-body vs 'a'-body MID positions."""
    recs = [(w, b0, npos) for w, onset, b0, npos, d in records
            if onset == onset_label and d == dialect]
    if not recs:
        return

    e_pos = [npos for w, b0, npos in recs if b0 == 'e']
    a_pos = [npos for w, b0, npos in recs if b0 == 'a']
    o_pos = [npos for w, b0, npos in recs if b0 == 'o']
    all_pos = [npos for w, b0, npos in recs]

    diff, z, se = z_test_means(a_pos, e_pos)  # a_mean - e_mean (positive = a is later)

    print(f"\n  {onset_label} ({dialect}): N={len(recs)}, all_mean={statistics.mean(all_pos):.3f}")
    print(f"    e-body: N={len(e_pos)}, mean={statistics.mean(e_pos):.3f}" if e_pos else f"    e-body: N=0")
    print(f"    a-body: N={len(a_pos)}, mean={statistics.mean(a_pos):.3f}" if a_pos else f"    a-body: N=0")
    if o_pos:
        print(f"    o-body: N={len(o_pos)}, mean={statistics.mean(o_pos):.3f}")
    if e_pos and a_pos:
        print(f"    a_mean - e_mean = {diff:+.3f}, z = {z:+.2f} (positive = 'a' later than 'e')")
        significance = '✓ SIGNIFICANT (z>2)' if abs(z) > 2 else '○ not significant'
        print(f"    → {significance}")

print("\n" + "="*70)
print("BODY-CLASS MID POSITION SPLIT BY ONSET CLASS AND DIALECT")
print("="*70)

ONSET_CLASSES = ['qok', 'ok', 'ot', 'ch', 'sh', 'd', 's', 'y']

for dialect in ['B', 'A']:
    print(f"\n{'─'*60}")
    print(f"DIALECT {dialect}")
    print(f"{'─'*60}")
    for onset in ONSET_CLASSES:
        analyze_body_position_split(records, dialect, onset)

# Summary table
print("\n" + "="*70)
print("SUMMARY: 'a'-body mean position vs 'e'-body mean position")
print(f"{'Onset':<6} {'Dialect':<8} {'e_mean':>7} {'a_mean':>7} {'diff':>7} {'z':>8} {'sig'}")
print("="*70)

for dialect in ['B', 'A']:
    for onset in ONSET_CLASSES:
        recs = [(w, b0, npos) for w, on, b0, npos, d in records if on == onset and d == dialect]
        e_pos = [npos for w, b0, npos in recs if b0 == 'e']
        a_pos = [npos for w, b0, npos in recs if b0 == 'a']
        if not e_pos or not a_pos:
            continue
        e_mean = statistics.mean(e_pos)
        a_mean = statistics.mean(a_pos)
        diff, z, se = z_test_means(a_pos, e_pos)
        sig = '✓' if abs(z) > 2 else ' '
        print(f"  {onset:<4} {dialect:<7} {e_mean:>7.3f} {a_mean:>7.3f} {diff:>+7.3f} {z:>+8.2f} {sig}")

# Specific analysis for ch and sh top word types
print("\n" + "="*70)
print("TOP WORD TYPES BY BODY CLASS — ch and sh ONSET")
print("="*70)

for dialect in ['B', 'A']:
    for onset in ['ch', 'sh']:
        recs = [(w, body_class(w, onset), npos) for w, on, b0, npos, d in records
                if on == onset and d == dialect]
        e_words = [(w, npos) for w, bc, npos in recs if bc == 'e-body']
        a_words = [(w, npos) for w, bc, npos in recs if bc == 'a-body']
        o_words = [(w, npos) for w, bc, npos in recs if bc == 'o-body']

        print(f"\n  {onset} ({dialect}) — top e-body words and their positions:")
        e_type_pos = defaultdict(list)
        for w, npos in e_words:
            e_type_pos[w].append(npos)
        for w, positions in sorted(e_type_pos.items(), key=lambda x: -len(x[1]))[:8]:
            print(f"    {w:<15} N={len(positions):>4}, mean_pos={statistics.mean(positions):.3f}")

        print(f"  {onset} ({dialect}) — top a-body words and their positions:")
        a_type_pos = defaultdict(list)
        for w, npos in a_words:
            a_type_pos[w].append(npos)
        for w, positions in sorted(a_type_pos.items(), key=lambda x: -len(x[1]))[:8]:
            print(f"    {w:<15} N={len(positions):>4}, mean_pos={statistics.mean(positions):.3f}")
