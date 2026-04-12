"""
exp_334: ch→qok Enrichment and Full Template-Class→qok Rule Analysis (H539)

Background:
- F326 (exp_324): sh→qok elevated (B=1.97×, A=1.74×) — strong cross-dialect rule
- ch is also a template-onset class; is ch→qok also elevated?
- If ch→qok elevated ≈ sh→qok, one "TEMPLATE→qok" rule explains both
- Also re-examine ch→sh and sh→ch (F328: B bidirectional, A unidirectional sh→ch)
- Plus: check if ch→ok, sh→ok are elevated (template→ok bigrams)

Questions:
1. ch→qok enrichment in B and A dialects
2. ch→ok enrichment (parallel to sh→qok)
3. Full template-class bigram profile: which qok/ok transitions are enriched from ch/sh?
4. Compare sh→qok vs ch→qok — same rule or different?
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
    mid_bigrams_by_dialect={'A':[],'B':[]}
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
            mid = words[1:-1]
            mid_words_by_dialect[dialect].extend(mid)
            for i in range(len(mid)-1):
                mid_bigrams_by_dialect[dialect].append((mid[i], mid[i+1]))
    return mid_words_by_dialect, mid_bigrams_by_dialect

print("Loading corpus...")
words_by_d, bigrams_by_d = parse_vms()

FOCUS_ONSETS = ['qok', 'ok', 'ot', 'ch', 'sh', 'd', 'y', 's']

def analyze_template_bigrams(words, bigrams, dialect):
    print(f"\n{'='*70}")
    print(f"TEMPLATE-CLASS BIGRAM ANALYSIS — {dialect}")
    print(f"{'='*70}")

    # Onset frequencies
    onset_counts = Counter(get_onset(w) for w in words)
    total_words = len(words)
    N_bigrams = len(bigrams)

    print(f"\nOnset frequencies (N_words={total_words}, N_bigrams={N_bigrams}):")
    for o in FOCUS_ONSETS:
        print(f"  {o}: {onset_counts[o]} ({100*onset_counts[o]/total_words:.1f}%)")

    # Bigram matrix for focus onsets
    bigram_counts = Counter((get_onset(w1), get_onset(w2)) for w1, w2 in bigrams)

    print(f"\n{'Pair':<15} {'obs':>6} {'exp':>8} {'E':>8} {'interpretation'}")
    print("-"*60)

    # Focus pairs: template onsets → qok, ok, and also sh/ch mutual
    focus_pairs = [
        ('sh', 'qok'), ('ch', 'qok'),  # template→qok
        ('sh', 'ok'),  ('ch', 'ok'),   # template→ok
        ('sh', 'ch'),  ('ch', 'sh'),   # mutual avoidance
        ('sh', 'sh'),  ('ch', 'ch'),   # self-succession
        ('sh', 'y'),   ('ch', 'y'),    # template→y
        ('sh', 'd'),   ('ch', 'd'),    # template→content
        ('qok', 'sh'), ('qok', 'ch'),  # qok→template (reverse)
        ('ok', 'qok'), ('qok', 'ok'),  # qok↔ok coupling
        ('ok', 'ok'),                  # ok self-succession
    ]

    for o1, o2 in focus_pairs:
        obs = bigram_counts.get((o1, o2), 0)
        p1 = onset_counts[o1] / total_words
        p2 = onset_counts[o2] / total_words
        exp = p1 * p2 * N_bigrams
        E = obs / exp if exp > 0 else 0

        flag = ''
        if E > 1.3: flag = '↑ elevated'
        elif E < 0.7: flag = '↓ depleted'
        print(f"  {o1}→{o2:<10} {obs:>6} {exp:>8.1f} {E:>8.3f}  {flag}")

    # Direct comparison: sh→qok vs ch→qok
    print(f"\n--- DIRECT COMPARISON: sh→qok vs ch→qok ---")
    for pair in [('sh','qok'), ('ch','qok')]:
        o1, o2 = pair
        obs = bigram_counts.get(pair, 0)
        exp = (onset_counts[o1]/total_words) * (onset_counts[o2]/total_words) * N_bigrams
        E = obs/exp if exp>0 else 0
        print(f"  {o1}→{o2}: obs={obs}, exp={exp:.1f}, E={E:.3f}×")

    sh_qok_E = bigram_counts.get(('sh','qok'), 0) / ((onset_counts['sh']/total_words) * (onset_counts['qok']/total_words) * N_bigrams)
    ch_qok_E = bigram_counts.get(('ch','qok'), 0) / ((onset_counts['ch']/total_words) * (onset_counts['qok']/total_words) * N_bigrams)

    if sh_qok_E > 0:
        print(f"\n  ch→qok / sh→qok ratio: {ch_qok_E/sh_qok_E:.3f}× (1.0 = identical enrichment)")

    # Also check template→qok combined
    print(f"\n--- TEMPLATE-CLASS → qok COMBINED (ch+sh pooled) ---")
    template_obs = sum(bigram_counts.get((o, 'qok'), 0) for o in ['ch', 'sh'])
    template_rate = sum(onset_counts[o] for o in ['ch', 'sh']) / total_words
    qok_rate = onset_counts['qok'] / total_words
    template_exp = template_rate * qok_rate * N_bigrams
    template_E = template_obs / template_exp if template_exp > 0 else 0
    print(f"  (ch+sh)→qok: obs={template_obs}, exp={template_exp:.1f}, E={template_E:.3f}×")
    print(f"  sh→qok: {bigram_counts.get(('sh','qok'),0)} obs")
    print(f"  ch→qok: {bigram_counts.get(('ch','qok'),0)} obs")

    # Compare to non-template→qok
    print(f"\n--- NON-TEMPLATE ONSETS → qok for comparison ---")
    for o1 in ['d', 'y', 'ok', 's']:
        obs = bigram_counts.get((o1, 'qok'), 0)
        exp = (onset_counts[o1]/total_words) * (onset_counts['qok']/total_words) * N_bigrams
        E = obs/exp if exp>0 else 0
        print(f"  {o1}→qok: obs={obs}, exp={exp:.1f}, E={E:.3f}×")

for d in ['B', 'A']:
    analyze_template_bigrams(words_by_d[d], bigrams_by_d[d], d)
