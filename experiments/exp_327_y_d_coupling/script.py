"""
exp_327: y→d Coupling Bigram Analysis (H526)

Question: Is y→d onset-class bigram enrichment (1.37×/1.38× cross-dialect, from exp_324)
explained by class-level grammar or specific word-type pairs?

exp_322: y-onset = y+gallows compound class (94% gallows at B0; yk-words, yt-words dominant)
exp_325: d-onset = daiin-dominated paradigm (daiin=22.6% B, 35.0% A)
exp_324: y→d enriched 1.37×/1.38× in both dialects (cross-dialect invariant)

Measurement:
1. Extract all y→d adjacent MID bigrams for B and A dialects
2. Per-y-word P(→d): which y-words show highest probability of preceding d-onset words?
3. Per-d-word: which d-words most commonly follow y-onset words?
4. Cross-dialect pair overlap: are the same y×d pairs enriched in both dialects?
5. Compare to sh→qok mechanism: is y→d analogous (class-level) or more concentrated (word-type)?
"""
from pathlib import Path as _RepositoryPath

import os, re
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
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
print(f"B MID words: {len(words_by_d['B'])}, A MID words: {len(words_by_d['A'])}")
print(f"B MID bigrams: {len(bigrams_by_d['B'])}, A MID bigrams: {len(bigrams_by_d['A'])}")

# ---- Main analysis function ----

def analyze_y_d_coupling(bigrams, words, dialect):
    print(f"\n{'='*70}")
    print(f"DIALECT: {dialect}")
    print(f"{'='*70}")

    # Overall onset frequencies
    onset_counts = Counter(get_onset(w) for w in words)
    total = len(words)
    total_bigrams = len(bigrams)

    # y and d onset frequencies
    y_count = onset_counts.get('y', 0)
    d_count = onset_counts.get('d', 0)
    print(f"\nOnset frequencies:")
    print(f"  y-onset: {y_count} ({100*y_count/total:.2f}%)")
    print(f"  d-onset: {d_count} ({100*d_count/total:.2f}%)")

    # Expected y→d under independence
    p_y = y_count / total
    p_d = d_count / total
    exp_y_d = p_y * p_d * total_bigrams
    obs_y_d = sum(1 for w1,w2 in bigrams if get_onset(w1)=='y' and get_onset(w2)=='d')
    print(f"\ny→d bigram: obs={obs_y_d}, exp={exp_y_d:.1f}, E={obs_y_d/exp_y_d:.3f}×")

    # For comparison: y→other onset transitions
    print(f"\ny→X bigram enrichments (for comparison):")
    for o2 in ['qok','ch','sh','ok','d','y','s','other']:
        obs = sum(1 for w1,w2 in bigrams if get_onset(w1)=='y' and get_onset(w2)==o2)
        p_o2 = onset_counts.get(o2, 0) / total
        exp = p_y * p_o2 * total_bigrams
        enr = obs/exp if exp > 0 else float('nan')
        print(f"  y→{o2}: obs={obs}, exp={exp:.1f}, E={enr:.3f}×")

    # ---- Per-y-word P(→d) analysis ----
    print(f"\n--- Per-y-word P(→d) analysis ---")
    y_word_total = Counter()  # y-word type → total count as 1st in bigram
    y_word_d = Counter()     # y-word type → count of transitions to d-onset

    for w1, w2 in bigrams:
        if get_onset(w1) == 'y':
            y_word_total[w1] += 1
            if get_onset(w2) == 'd':
                y_word_d[w1] += 1

    # Class-level rate
    class_rate_y_d = obs_y_d / sum(y_word_total.values()) if y_word_total else 0
    print(f"Class-level P(y→d) = {class_rate_y_d:.4f}")

    # Top y-words with most d-transitions
    print(f"\nTop y-words by P(→d) (min 5 total transitions):")
    print(f"{'y_word':<20} {'total':>6} {'→d':>5} {'P(→d)':>7} {'vs_class':>9}")
    print("-"*55)
    y_words_sorted = sorted(y_word_total.keys(),
                            key=lambda w: y_word_d.get(w,0)/y_word_total[w] if y_word_total[w]>=5 else -1,
                            reverse=True)
    shown = 0
    for w in y_words_sorted:
        tot = y_word_total[w]
        if tot < 3: continue
        nd = y_word_d.get(w, 0)
        p = nd / tot
        ratio = p / class_rate_y_d if class_rate_y_d > 0 else float('nan')
        print(f"{w:<20} {tot:>6} {nd:>5} {p:>7.4f} {ratio:>9.2f}×")
        shown += 1
        if shown >= 20: break

    # ---- Which d-words follow y-onset words? ----
    print(f"\n--- d-words that follow y-onset words ---")
    d_word_after_y = Counter()
    d_word_total_mid = Counter(w for w in words if get_onset(w)=='d')

    for w1, w2 in bigrams:
        if get_onset(w1) == 'y' and get_onset(w2) == 'd':
            d_word_after_y[w2] += 1

    total_y_d_bigrams = sum(d_word_after_y.values())
    total_d_tokens = sum(d_word_total_mid.values())
    print(f"Total y→d bigrams: {total_y_d_bigrams}")
    print(f"\n{'d_word':<20} {'after_y':>8} {'%after_y':>9} {'total_mid':>10} {'%mid':>7} {'enr':>7}")
    print("-"*65)
    for w, cnt in d_word_after_y.most_common(15):
        d_total = d_word_total_mid.get(w, 0)
        p_after_y = cnt / total_y_d_bigrams if total_y_d_bigrams > 0 else 0
        p_mid = d_total / total_d_tokens if total_d_tokens > 0 else 0
        enr = p_after_y / p_mid if p_mid > 0 else float('nan')
        print(f"{w:<20} {cnt:>8} {p_after_y*100:>9.1f}% {d_total:>10} {p_mid*100:>7.1f}% {enr:>7.2f}×")

    # ---- Specific y×d word pairs ----
    print(f"\n--- Top y×d word-type pairs ---")
    yd_pairs = Counter()
    for w1, w2 in bigrams:
        if get_onset(w1) == 'y' and get_onset(w2) == 'd':
            yd_pairs[(w1, w2)] += 1

    total_yd = sum(yd_pairs.values())
    n_pairs = len(yd_pairs)
    # CP50: how many pairs for 50% of bigrams?
    cp50 = 0; cumsum = 0
    for (w1, w2), cnt in yd_pairs.most_common():
        cumsum += cnt
        cp50 += 1
        if cumsum >= 0.5 * total_yd: break

    print(f"Total y→d bigrams: {total_yd}, Unique pairs: {n_pairs}")
    print(f"CP50 (pairs for 50%): {cp50}")
    print(f"\nTop y×d pairs:")
    print(f"{'y_word':<18} {'d_word':<18} {'count':>6} {'%':>6}")
    for (w1, w2), cnt in yd_pairs.most_common(15):
        print(f"{w1:<18} {w2:<18} {cnt:>6} {100*cnt/total_yd:>6.1f}%")

    return yd_pairs, y_word_d, y_word_total, d_word_after_y

b_pairs, b_y_d, b_y_tot, b_d_after = analyze_y_d_coupling(bigrams_by_d['B'], words_by_d['B'], 'B')
a_pairs, a_y_d, a_y_tot, a_d_after = analyze_y_d_coupling(bigrams_by_d['A'], words_by_d['A'], 'A')

# ---- Cross-dialect pair overlap ----
print(f"\n{'='*70}")
print("CROSS-DIALECT COMPARISON")
print(f"{'='*70}")

b_pair_set = set(b_pairs.keys())
a_pair_set = set(a_pairs.keys())
shared = b_pair_set & a_pair_set
jaccard = len(shared) / len(b_pair_set | a_pair_set) if (b_pair_set | a_pair_set) else 0

print(f"B unique y→d pairs: {len(b_pair_set)}")
print(f"A unique y→d pairs: {len(a_pair_set)}")
print(f"Shared pairs: {len(shared)}")
print(f"Jaccard: {jaccard:.3f}")

if shared:
    print(f"\nShared y×d pairs (appear in both dialects):")
    for pair in sorted(shared, key=lambda p: -(b_pairs.get(p,0)+a_pairs.get(p,0))):
        b_cnt = b_pairs.get(pair, 0)
        a_cnt = a_pairs.get(pair, 0)
        print(f"  {pair[0]:<15} → {pair[1]:<15} B={b_cnt} A={a_cnt}")

# ---- Compare to sh→qok mechanism ----
print(f"\n{'='*70}")
print("COMPARISON WITH sh→qok MECHANISM (exp_323)")
print(f"{'='*70}")
print("""
sh→qok (exp_323):
  - Class-level enrichment: E=1.97× (B), E=1.74× (A)
  - Unique sh→qok pairs (B): 103 pairs; top pair = shedy→qokedy (4.7% of bigrams)
  - Cross-dialect pair overlap: 2.4% (5/257) → CLASS-LEVEL mechanism

y→d should be compared:
  - Total y→d bigrams (much smaller N): B=?, A=?
  - N_pairs vs N for sh→qok
  - CP50 pairs (how concentrated?)
  - Cross-dialect overlap % (if >10%, more lexical; if <5%, class-level)
""")

# Quantitative comparison
print("Quantitative comparison:")
print(f"  sh→qok B: exp_323 reported 342 bigrams, 103 pairs, CP50=~5 pairs, overlap=2.4%")
b_y_d_total = sum(b_pairs.values())
a_y_d_total = sum(a_pairs.values())
if b_y_d_total > 0:
    b_cp50 = 0; cs = 0
    for (w1,w2), cnt in b_pairs.most_common():
        cs += cnt; b_cp50 += 1
        if cs >= 0.5*b_y_d_total: break
    b_jaccard_like = len(shared)/(len(b_pair_set)|len(a_pair_set)) if (b_pair_set|a_pair_set) else 0
    print(f"  y→d B: {b_y_d_total} bigrams, {len(b_pair_set)} pairs, CP50={b_cp50} pairs")
    print(f"  y→d A: {a_y_d_total} bigrams, {len(a_pair_set)} pairs")
    print(f"  y→d cross-dialect overlap: {len(shared)} shared / {len(b_pair_set|a_pair_set)} total = {100*jaccard:.1f}%")
    if jaccard < 0.05:
        print(f"  → LOW OVERLAP (<5%): CLASS-LEVEL mechanism (like sh→qok)")
    elif jaccard > 0.15:
        print(f"  → HIGH OVERLAP (>15%): LEXICAL mechanism (specific pairs recurring)")
    else:
        print(f"  → MEDIUM OVERLAP (5-15%): Mixed class-level + lexical")
