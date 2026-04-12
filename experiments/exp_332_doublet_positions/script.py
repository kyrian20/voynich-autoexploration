"""
exp_332: MID Position of Doublet Pairs — Do Onset-Substitution Doublets Appear at Different MID Positions? (H535)

Background:
- F333 (exp_331): 5-onset × 7-body doublet system confirmed
- F331 (exp_329): MID position gradient: sh < y/ch/qok < ok < d/ot
- Prediction: words sharing the same body but different onset should appear at MID positions
  consistent with their onset class position in the gradient
  e.g., qokaiin (qok pos≈0.49) should appear earlier than daiin (d pos≈0.56)
  and okaiin (ok pos≈0.50) should be intermediate

Test: for each of the 5 onset classes × core bodies, compute mean MID position of each doublet
word and compare to: (1) expected class position from F331, (2) whether body-sharing words
differ in position.
"""

import os, re, statistics
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

def parse_vms_positions():
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

    word_positions = defaultdict(lambda: defaultdict(list))  # dialect -> word -> [npos list]
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
                npos = idx / (span-1) if span > 1 else 0.5
                word_positions[dialect][w].append(npos)
    return word_positions

print("Loading corpus with positions...")
word_positions = parse_vms_positions()
print(f"B unique MID word types: {len(word_positions['B'])}")
print(f"A unique MID word types: {len(word_positions['A'])}")

# Gradient positions from F331
GRADIENT_B = {'qok':0.491, 'ok':0.503, 'ot':0.588, 'd':0.560, 's':0.532}
GRADIENT_A = {'qok':0.501, 'ok':0.521, 'ot':0.574, 'd':0.596, 's':0.617}

CORE_BODIES = ['aiin', 'ain', 'ar', 'al', 'ol', 'air', 'or']
AIIN_ONSETS = ['qok', 'ok', 'ot', 'd', 's']

def analyze_doublet_positions(word_positions_d, gradient, dialect):
    print(f"\n{'='*70}")
    print(f"DOUBLET MID POSITIONS — {dialect}")
    print(f"{'='*70}")
    
    # For each core body, show positions of each onset variant
    print(f"\n{'Body':<8}", end='')
    for o in AIIN_ONSETS:
        print(f" {o:>12}", end='')
    print(f"  {'range':>8}  {'expected_range':>14}")
    print("-"*80)
    
    expected_range = max(GRADIENT_B.values()) - min(GRADIENT_B.values())
    
    for body in CORE_BODIES:
        positions = {}
        for o in AIIN_ONSETS:
            word = o + body
            pos_list = word_positions_d.get(word, [])
            if len(pos_list) >= 3:
                positions[o] = (statistics.mean(pos_list), len(pos_list))
            else:
                positions[o] = (None, len(pos_list))
        
        # Print line
        print(f"{body:<8}", end='')
        available = [(o, m, n) for o, (m, n) in positions.items() if m is not None]
        means = [m for o, m, n in available]
        
        for o in AIIN_ONSETS:
            m, n = positions[o]
            if m is None:
                print(f" {'N='+str(n):>12}", end='')
            else:
                print(f" {m:.3f}(N={n})", end='')
        
        if len(means) >= 2:
            obs_range = max(means) - min(means)
            # Expected range: gradient diff between highest and lowest onset pos
            exp_r = expected_range
            print(f"  {obs_range:>8.3f}  {exp_r:>14.3f}")
        else:
            print(f"  {'?':>8}  {expected_range:>14.3f}")
    
    # Check if ordering matches gradient
    print(f"\n--- Ordering check: does mean pos follow gradient? ---")
    print(f"Expected gradient order (from F331): {' < '.join(sorted(GRADIENT_B.keys(), key=lambda o: GRADIENT_B[o]))}")
    print(f"\n{'Body':<8} {'observed_order':<40} {'matches_gradient?'}")
    print("-"*60)
    
    gradient_matches = 0
    gradient_total = 0
    
    for body in CORE_BODIES:
        positions = {}
        for o in AIIN_ONSETS:
            word = o + body
            pos_list = word_positions_d.get(word, [])
            if len(pos_list) >= 3:
                positions[o] = statistics.mean(pos_list)
        
        if len(positions) < 3: continue
        
        # Sort by observed position
        obs_order = sorted(positions.keys(), key=lambda o: positions[o])
        obs_str = ' < '.join(obs_order)
        
        # Check: does each adjacent pair in obs_order match gradient direction?
        correct_pairs = 0
        total_pairs = 0
        exp_order = sorted(positions.keys(), key=lambda o: gradient.get(o, 0.5))
        
        for i in range(len(exp_order)-1):
            o1, o2 = exp_order[i], exp_order[i+1]
            if o1 in positions and o2 in positions:
                total_pairs += 1
                if positions[o1] < positions[o2]:  # Expected o1 < o2
                    correct_pairs += 1
        
        match = f"{correct_pairs}/{total_pairs}" if total_pairs > 0 else "N/A"
        print(f"{body:<8} {obs_str:<40} {match}")
        gradient_matches += correct_pairs
        gradient_total += total_pairs
    
    if gradient_total > 0:
        print(f"\nOverall: {gradient_matches}/{gradient_total} gradient-consistent pairs ({100*gradient_matches/gradient_total:.1f}%)")

analyze_doublet_positions(word_positions['B'], GRADIENT_B, 'B')
analyze_doublet_positions(word_positions['A'], GRADIENT_A, 'A')

# Also compute specific doublet position comparisons for the main bodies
print(f"\n{'='*70}")
print("SPECIFIC DOUBLET COMPARISON: 'aiin'-body across 5 onsets")
print(f"{'='*70}")

for dialect in ['B', 'A']:
    print(f"\n{dialect}-dialect:")
    for o in AIIN_ONSETS:
        word = o + 'aiin'
        pos_list = word_positions[dialect].get(word, [])
        if pos_list:
            m = statistics.mean(pos_list)
            expected = GRADIENT_B[o] if dialect == 'B' else GRADIENT_A[o]
            print(f"  {word:<12}: mean_pos={m:.4f} (expected class pos={expected:.4f}, diff={m-expected:+.4f}), N={len(pos_list)}")
