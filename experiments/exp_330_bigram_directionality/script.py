"""
exp_330: Bigram Directionality — Does the Onset-Class MID Position Gradient Predict Bigram Enrichment Direction? (H534)

Background:
- F331 (exp_329): MID position gradient: sh(0.42) < y/ch/qok(0.48) < ok(0.50) < d(0.56) < ot(0.59)
- F326 (exp_324): Bigram enrichment matrix shows structured couplings
- Question: Are enriched bigrams directionally consistent with the gradient?
  - "Forward" = lower gradient position → higher (e.g., sh→qok = early→mid)
  - "Backward" = higher → lower
  - If grammar is directional, forward E > backward E consistently

Measurements:
1. Use bigram enrichment data from corpus (re-run from corpus data)
2. Compute E(o1→o2) and E(o2→o1) for all major onset-class pairs
3. Assign gradient positions from F331
4. Test: are E values higher for forward transitions?
5. Report: which bigrams violate gradient directionality?
"""

import os, re, math
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
            mid=words[1:-1]
            for w in mid:
                mid_words_by_dialect[dialect].append(w)
            for i in range(len(mid)-1):
                mid_bigrams_by_dialect[dialect].append((mid[i],mid[i+1]))
    return mid_bigrams_by_dialect, mid_words_by_dialect

print("Loading corpus...")
bigrams_by_d, words_by_d = parse_vms()

# MID position gradient from F331
GRADIENT_B = {
    'sh': 0.420,
    'y': 0.484,
    'ch': 0.487,
    'qok': 0.491,
    'ok': 0.503,
    's': 0.532,
    'd': 0.560,
    'ot': 0.588,
}
GRADIENT_A = {
    'sh': 0.410,
    'ch': 0.471,
    'qok': 0.501,
    'ok': 0.521,
    'y': 0.544,
    'ot': 0.574,
    'd': 0.596,
    's': 0.617,
}

MAJOR_ONSETS = ['qok','ch','sh','ok','ot','d','y','s']

def compute_enrichment_matrix(bigrams, words, onsets):
    """Compute obs/exp enrichment for all onset pairs."""
    onset_counts = Counter(get_onset(w) for w in words)
    total = len(words)
    n_bigrams = len(bigrams)

    # Observed bigram counts
    obs = defaultdict(int)
    for w1, w2 in bigrams:
        o1, o2 = get_onset(w1), get_onset(w2)
        if o1 in onsets and o2 in onsets:
            obs[(o1, o2)] += 1

    # Expected under independence
    matrix = {}
    for o1 in onsets:
        for o2 in onsets:
            p1 = onset_counts[o1] / total
            p2 = onset_counts[o2] / total
            exp = p1 * p2 * n_bigrams
            if exp > 0:
                enr = obs[(o1, o2)] / exp
            else:
                enr = float('nan')
            matrix[(o1, o2)] = (obs[(o1, o2)], exp, enr)
    return matrix

def analyze_directionality(bigrams, words, dialect, gradient):
    print(f"\n{'='*70}")
    print(f"BIGRAM DIRECTIONALITY ANALYSIS — {dialect}")
    print(f"{'='*70}")

    matrix = compute_enrichment_matrix(bigrams, words, MAJOR_ONSETS)

    # For each pair (o1, o2) with o1 ≠ o2, compare forward vs backward enrichment
    print(f"\nDirectionality table: forward = o1 has LOWER gradient position than o2")
    print(f"(If 'forward' consistently has higher E, gradient predicts bigram direction)")
    print(f"\n{'Pair':<15} {'pos_diff':>9} {'E(o1→o2)':>10} {'E(o2→o1)':>10} {'dir_ratio':>10} {'direction':>10}")
    print("-"*70)

    directional_pairs = []  # (o1, o2, pos_diff, e_fwd, e_bkwd)
    for o1 in MAJOR_ONSETS:
        for o2 in MAJOR_ONSETS:
            if o1 >= o2: continue  # Only process each pair once
            if o1 not in gradient or o2 not in gradient: continue
            pos1 = gradient[o1]
            pos2 = gradient[o2]
            pos_diff = pos2 - pos1  # positive = o1 is earlier = o1→o2 is forward

            e_fwd = matrix[(o1, o2)][2]  # E(o1→o2)
            e_bkwd = matrix[(o2, o1)][2]  # E(o2→o1)

            if math.isnan(e_fwd) or math.isnan(e_bkwd): continue

            dir_ratio = e_fwd / e_bkwd if e_bkwd > 0 else float('nan')

            # Direction label
            if abs(pos_diff) < 0.02:
                dir_label = 'symmetric'
            elif pos_diff > 0 and e_fwd > e_bkwd:
                dir_label = '✓ gradient'
            elif pos_diff > 0 and e_fwd < e_bkwd:
                dir_label = '✗ anti-grad'
            elif pos_diff < 0 and e_fwd < e_bkwd:
                dir_label = '✓ gradient'
            else:
                dir_label = '✗ anti-grad'

            pair_str = f"{o1}→{o2}"
            print(f"{pair_str:<15} {pos_diff:>+9.3f} {e_fwd:>10.3f} {e_bkwd:>10.3f} {dir_ratio:>10.3f} {dir_label:>10}")
            directional_pairs.append((o1, o2, pos_diff, e_fwd, e_bkwd, dir_label))

    # Summary counts
    gradient_consistent = sum(1 for _, _, _, _, _, d in directional_pairs if d == '✓ gradient')
    anti_gradient = sum(1 for _, _, _, _, _, d in directional_pairs if d == '✗ anti-grad')
    total_pairs = gradient_consistent + anti_gradient

    print(f"\nDirectionality summary:")
    print(f"  Gradient-consistent (forward > backward): {gradient_consistent}/{total_pairs}")
    print(f"  Anti-gradient (backward > forward): {anti_gradient}/{total_pairs}")
    print(f"  Expected by chance: {total_pairs//2}/{total_pairs}")

    # Focus on strongly asymmetric pairs
    print(f"\nStrongly asymmetric pairs (dir_ratio > 1.5× or < 0.67×):")
    for o1, o2, pos_diff, e_fwd, e_bkwd, dir_label in directional_pairs:
        dir_ratio = e_fwd / e_bkwd if e_bkwd > 0 else float('nan')
        if abs(math.log(dir_ratio)) > math.log(1.5):  # ratio > 1.5 or < 0.67
            pair_str = f"{o1}→{o2}"
            print(f"  {pair_str:<15} pos_diff={pos_diff:+.3f} E_fwd={e_fwd:.3f} E_bkwd={e_bkwd:.3f} ratio={dir_ratio:.2f}×  {dir_label}")

    # Directional self-succession (self-transitions — not directional by definition)
    print(f"\nSelf-succession enrichment (directionality N/A):")
    for o in MAJOR_ONSETS:
        e_self = matrix[(o, o)][2]
        pos = gradient.get(o, float('nan'))
        print(f"  {o:<8} pos={pos:.3f}  E_self={e_self:.3f}×")

    return matrix, directional_pairs

b_matrix, b_pairs = analyze_directionality(bigrams_by_d['B'], words_by_d['B'], 'B', GRADIENT_B)
a_matrix, a_pairs = analyze_directionality(bigrams_by_d['A'], words_by_d['A'], 'A', GRADIENT_A)

# ---- Cross-dialect directionality consistency ----
print(f"\n{'='*70}")
print(f"CROSS-DIALECT DIRECTIONALITY CONSISTENCY")
print(f"{'='*70}")

# Compare direction labels between B and A for same pairs
b_dir = {(o1,o2): d for o1,o2,_,_,_,d in b_pairs}
a_dir = {(o1,o2): d for o1,o2,_,_,_,d in a_pairs}
shared_pairs = set(b_dir.keys()) & set(a_dir.keys())

print(f"\n{'Pair':<15} {'B_dir':<12} {'A_dir':<12} {'consistent?'}")
print("-"*50)
both_consistent = 0
discordant = 0
for o1, o2 in sorted(shared_pairs):
    bd = b_dir[(o1,o2)]
    ad = a_dir[(o1,o2)]
    consistent = (bd == ad) or (bd == 'symmetric' or ad == 'symmetric')
    mark = '✓' if consistent else '✗'
    if 'gradient' in bd and 'gradient' in ad: both_consistent += 1
    if bd != ad and 'symmetric' not in bd and 'symmetric' not in ad: discordant += 1
    print(f"{o1+'→'+o2:<15} {bd:<12} {ad:<12} {mark}")

print(f"\nBoth gradient-consistent: {both_consistent}")
print(f"Discordant (different directions): {discordant}")
