"""
exp_324: Full Onset-Class MID Bigram Succession Matrix (H525)

Background:
- exp_323 discovered sh→ch is DEPLETED (0.555×) in both dialects — unexpected
- Also: sh→qok enriched (1.97×); qok↔ch enriched (~1.15-1.20×) from prior work
- H525: compute full 7×7 (or 8×8) onset-class bigram enrichment matrix for both dialects
- Identify systematic elevated/depleted pairs; find all structural invariants

Measurement:
1. For each onset-class pair (onset1, onset2), compute obs/exp enrichment for B and A MID bigrams
2. "exp" = P(onset1) × P(onset2) × N_bigrams (independence null model)
3. Generate enrichment matrices for B and A dialects
4. Report cross-dialect consistent patterns (|enr_B - enr_A| < 0.3, both >1.2 or both <0.8)
5. Focus on template classes (qok, ch, sh, ok, d, y, s) and mutual avoidance/attraction
"""
from pathlib import Path as _RepositoryPath

import os, re, math
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

ONSET_ORDER=[
    ('qok','qok'),('qot','qot'),('qo','qo'),('cth','cth'),
    ('ch','ch'),('sh','sh'),('ok','ok'),('ot','ot'),('ol','ol'),
    ('d','d'),('s','s'),('y','y'),('k','k'),('t','t'),
    ('l','l'),('r','r'),('p','p'),('f','f'),('o','o'),
]

MAJOR_ONSETS = ['qok','ch','sh','ok','d','y','s']

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

def compute_bigram_matrix(bigrams, words, onsets):
    n_bigrams = len(bigrams)
    onset_counts = Counter(get_onset(w) for w in words)
    total = sum(onset_counts.values())

    # Count observed bigrams
    obs = defaultdict(int)
    for w1,w2 in bigrams:
        o1, o2 = get_onset(w1), get_onset(w2)
        if o1 in onsets and o2 in onsets:
            obs[(o1,o2)] += 1

    # Compute expected and enrichment
    matrix = {}
    for o1 in onsets:
        for o2 in onsets:
            p1 = onset_counts[o1]/total
            p2 = onset_counts[o2]/total
            exp = p1 * p2 * n_bigrams
            observed = obs.get((o1,o2),0)
            enr = observed / exp if exp > 0 else 0
            matrix[(o1,o2)] = (observed, exp, enr)
    return matrix, onset_counts

def print_matrix(matrix, onsets, dialect, label='enrichment'):
    print(f"\n--- {label} ({dialect}-dialect) ---")
    # Header
    print(f"{'':>6}", end='')
    for o2 in onsets: print(f" {o2:>7}", end='')
    print()
    print("-"*(8+8*len(onsets)))
    for o1 in onsets:
        print(f"{o1:>6}", end='')
        for o2 in onsets:
            obs,exp,enr = matrix.get((o1,o2),(0,0,0))
            if exp < 3: marker='   ---'
            elif enr >= 1.5: marker=f'{enr:>7.2f}▲'
            elif enr <= 0.65: marker=f'{enr:>7.2f}▼'
            else: marker=f'{enr:>7.2f} '
            print(f" {marker}", end='')
        print()

def print_counts_matrix(matrix, onsets, dialect):
    print(f"\n--- Observed counts ({dialect}-dialect) ---")
    print(f"{'':>6}", end='')
    for o2 in onsets: print(f" {o2:>7}", end='')
    print()
    for o1 in onsets:
        print(f"{o1:>6}", end='')
        for o2 in onsets:
            obs,exp,enr = matrix.get((o1,o2),(0,0,0))
            print(f" {obs:>7}", end='')
        print()

def main():
    print("Loading VMS data...")
    mid_bigrams_by_dialect, mid_words_by_dialect = parse_vms()

    results = {}
    for dialect in ['B','A']:
        bigrams = mid_bigrams_by_dialect[dialect]
        words = mid_words_by_dialect[dialect]
        matrix, onset_counts = compute_bigram_matrix(bigrams, words, MAJOR_ONSETS)
        results[dialect] = (matrix, onset_counts)

        total = sum(onset_counts.values())
        print(f"\n{'='*65}")
        print(f"DIALECT {dialect}: {len(bigrams)} MID bigrams, {len(words)} MID words")
        print(f"{'='*65}")
        print(f"\nOnset frequencies (MID):")
        for o in MAJOR_ONSETS:
            cnt = onset_counts[o]
            print(f"  {o:<6}: {cnt:>5} ({cnt/total:.2%})")

        print_matrix(matrix, MAJOR_ONSETS, dialect, label='Enrichment (obs/exp)')
        print_counts_matrix(matrix, MAJOR_ONSETS, dialect)

    # Cross-dialect comparison
    print(f"\n{'='*65}")
    print("CROSS-DIALECT INVARIANTS (consistent elevated/depleted in both B and A)")
    print(f"{'='*65}")

    b_matrix = results['B'][0]
    a_matrix = results['A'][0]

    elevated_both = []
    depleted_both = []
    discordant = []

    for o1 in MAJOR_ONSETS:
        for o2 in MAJOR_ONSETS:
            obs_b, exp_b, enr_b = b_matrix.get((o1,o2),(0,0,0))
            obs_a, exp_a, enr_a = a_matrix.get((o1,o2),(0,0,0))
            if exp_b < 3 or exp_a < 3: continue
            if enr_b >= 1.3 and enr_a >= 1.3:
                elevated_both.append((o1,o2,enr_b,enr_a,obs_b,obs_a))
            elif enr_b <= 0.70 and enr_a <= 0.70:
                depleted_both.append((o1,o2,enr_b,enr_a,obs_b,obs_a))
            elif abs(enr_b-enr_a) > 0.5 and (enr_b>1.3 or enr_b<0.7 or enr_a>1.3 or enr_a<0.7):
                discordant.append((o1,o2,enr_b,enr_a,obs_b,obs_a))

    print(f"\nELEVATED in both dialects (E>1.3× in B AND A):")
    print(f"{'Pair':<12} {'Enr_B':>8} {'Enr_A':>8} {'Obs_B':>8} {'Obs_A':>8}")
    elevated_both.sort(key=lambda x: -(x[2]+x[3])/2)
    for o1,o2,eb,ea,ob,oa in elevated_both:
        print(f"{o1}→{o2:<6} {eb:>8.3f} {ea:>8.3f} {ob:>8} {oa:>8}")

    print(f"\nDEPLETED in both dialects (E<0.70× in B AND A):")
    print(f"{'Pair':<12} {'Enr_B':>8} {'Enr_A':>8} {'Obs_B':>8} {'Obs_A':>8}")
    depleted_both.sort(key=lambda x: (x[2]+x[3])/2)
    for o1,o2,eb,ea,ob,oa in depleted_both:
        print(f"{o1}→{o2:<6} {eb:>8.3f} {ea:>8.3f} {ob:>8} {oa:>8}")

    print(f"\nDISCORDANT (significant in B but not A or vice versa):")
    print(f"{'Pair':<12} {'Enr_B':>8} {'Enr_A':>8} {'Obs_B':>8} {'Obs_A':>8}")
    discordant.sort(key=lambda x: -abs(x[2]-x[3]))
    for o1,o2,eb,ea,ob,oa in discordant:
        print(f"{o1}→{o2:<6} {eb:>8.3f} {ea:>8.3f} {ob:>8} {oa:>8}")

    # Self-succession rates
    print(f"\n{'='*65}")
    print("SELF-SUCCESSION RATES (onset→same onset)")
    print(f"{'='*65}")
    print(f"{'Onset':<6} {'Enr_B':>8} {'Obs_B':>8} {'Enr_A':>8} {'Obs_A':>8}")
    for o in MAJOR_ONSETS:
        obs_b,exp_b,enr_b = b_matrix.get((o,o),(0,0,0))
        obs_a,exp_a,enr_a = a_matrix.get((o,o),(0,0,0))
        flag_b = '▲' if enr_b>1.3 else ('▼' if enr_b<0.7 else ' ')
        flag_a = '▲' if enr_a>1.3 else ('▼' if enr_a<0.7 else ' ')
        print(f"{o:<6} {enr_b:>8.3f}{flag_b} {obs_b:>8} {enr_a:>8.3f}{flag_a} {obs_a:>8}")

    print("\nDone.")

if __name__=='__main__':
    main()
