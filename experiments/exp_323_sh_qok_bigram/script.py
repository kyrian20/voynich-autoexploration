"""
exp_323: sh→qok Bigram Word-Level Analysis (H522, Q004)

Background:
- Q004 (sh→qok enrichment): E_mid=1.967× in B-dialect (F261)
- The enrichment is unexplained architecturally: is it:
  (a) all sh-words preceding all qok-words uniformly (class-level grammar)
  (b) specific sh-words preceding any qok-word (sh-word selection)
  (c) specific sh×qok word-type pairs (lexical co-occurrence)
- Mechanistic interpretation depends critically on which scenario is true
- A-dialect: p_sh_qok=0.10 Markov rule added to achieve sh→qok enrichment (F302/exp_300)

Measurement:
1. Extract all sh→qok adjacent MID bigrams (B and A dialect)
2. Frequency distribution of sh-word types that precede qok-words
3. Frequency distribution of qok-word types that follow sh-words
4. Top-20 specific sh×qok word-type pairs
5. Expected vs observed for each pair (under independence: P(sh_type)×P(qok_type)×N_sh_qok)
6. Compare sh→qok concentration vs sh→ch and sh→sh (other high-frequency transitions)
7. Cross-dialect: do A and B share the same specific pairs?
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

    # Extract MID bigrams
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
            for w in mid:
                mid_words_by_dialect[dialect].append(w)
            for i in range(len(mid)-1):
                mid_bigrams_by_dialect[dialect].append((mid[i], mid[i+1]))
    return mid_bigrams_by_dialect, mid_words_by_dialect

def analyze_sh_qok(bigrams, mid_words, dialect):
    print(f"\n{'='*65}")
    print(f"sh→qok Bigram Analysis — {dialect}-dialect")
    print(f"{'='*65}")

    n_bigrams = len(bigrams)
    word_counts = Counter(mid_words)
    onset_counts = defaultdict(int)
    for w,cnt in word_counts.items():
        onset_counts[get_onset(w)] += cnt

    # sh→qok bigrams
    sh_qok_bigrams = [(w1,w2) for w1,w2 in bigrams if get_onset(w1)=='sh' and get_onset(w2)=='qok']
    sh_any = [(w1,w2) for w1,w2 in bigrams if get_onset(w1)=='sh']
    any_qok = [(w1,w2) for w1,w2 in bigrams if get_onset(w2)=='qok']

    n_sh_qok = len(sh_qok_bigrams)
    n_sh_any = len(sh_any)
    n_any_qok = len(any_qok)

    # Expected under independence
    p_sh = onset_counts['sh'] / sum(onset_counts.values()) if sum(onset_counts.values()) > 0 else 0
    p_qok = onset_counts['qok'] / sum(onset_counts.values()) if sum(onset_counts.values()) > 0 else 0
    n_expected = p_sh * p_qok * n_bigrams
    enrichment = n_sh_qok / max(n_expected, 1)

    print(f"\nOverall: sh→qok bigrams = {n_sh_qok}/{n_bigrams} total MID bigrams")
    print(f"  sh→any: {n_sh_any}, any→qok: {n_any_qok}")
    print(f"  Expected (independence): {n_expected:.1f}")
    print(f"  Observed/Expected (enrichment): {enrichment:.3f}×")

    # Comparison bigrams
    for onset1, onset2, label in [('sh','ch','sh→ch'), ('sh','sh','sh→sh'), ('ch','qok','ch→qok'), ('qok','sh','qok→sh')]:
        n = sum(1 for w1,w2 in bigrams if get_onset(w1)==onset1 and get_onset(w2)==onset2)
        p1 = onset_counts[onset1] / sum(onset_counts.values())
        p2 = onset_counts[onset2] / sum(onset_counts.values())
        exp = p1 * p2 * n_bigrams
        enr = n / max(exp, 1)
        print(f"  {label}: obs={n}, exp={exp:.1f}, enr={enr:.3f}×")

    # sh-word type distribution preceding qok
    sh_words_before_qok = Counter(w1 for w1,w2 in sh_qok_bigrams)
    sh_total = onset_counts['sh']
    print(f"\n--- sh-word types preceding qok-words (top-15) ---")
    print(f"N total sh-tokens: {sh_total}")
    print(f"{'Word':<15} {'N_before_qok':>14} {'P(w1|sh,w1→qok)':>16}  {'Background P(w1)':>16}")
    sh_bgcount = {w:cnt for w,cnt in word_counts.items() if get_onset(w)=='sh'}
    sh_bg_total = sum(sh_bgcount.values())
    for w,cnt in sh_words_before_qok.most_common(15):
        bg = sh_bgcount.get(w,0)
        bg_pct = bg/sh_bg_total if sh_bg_total>0 else 0
        enr_this = (cnt/n_sh_qok) / bg_pct if bg_pct>0 else float('inf')
        print(f"{w:<15} {cnt:>14} {cnt/n_sh_qok:>16.1%}  {bg:>5}({bg_pct:.1%}) enr={enr_this:.2f}×")

    # qok-word type distribution following sh
    qok_words_after_sh = Counter(w2 for w1,w2 in sh_qok_bigrams)
    qok_total = onset_counts['qok']
    print(f"\n--- qok-word types following sh-words (top-15) ---")
    print(f"N total qok-tokens: {qok_total}")
    print(f"{'Word':<15} {'N_after_sh':>10} {'P(w2|sh,w2∈qok)':>16}  {'Background P(w2)':>16}")
    qok_bgcount = {w:cnt for w,cnt in word_counts.items() if get_onset(w)=='qok'}
    qok_bg_total = sum(qok_bgcount.values())
    for w,cnt in qok_words_after_sh.most_common(15):
        bg = qok_bgcount.get(w,0)
        bg_pct = bg/qok_bg_total if qok_bg_total>0 else 0
        enr_this = (cnt/n_sh_qok) / bg_pct if bg_pct>0 else float('inf')
        print(f"{w:<15} {cnt:>10} {cnt/n_sh_qok:>16.1%}  {bg:>5}({bg_pct:.1%}) enr={enr_this:.2f}×")

    # Top sh×qok word-type pairs
    print(f"\n--- Top-20 specific sh×qok word-type pairs ---")
    pair_counts = Counter(sh_qok_bigrams)
    print(f"{'sh_word':<15} {'qok_word':<15} {'N':>4}  {'Obs/Exp_pair':>12}")
    print("-"*50)
    for (w1,w2),cnt in pair_counts.most_common(20):
        p_w1 = sh_bgcount.get(w1,0) / sh_bg_total if sh_bg_total>0 else 0
        p_w2 = qok_bgcount.get(w2,0) / qok_bg_total if qok_bg_total>0 else 0
        exp_pair = p_w1 * p_w2 * n_sh_qok
        enr_pair = cnt / max(exp_pair, 0.1)
        print(f"{w1:<15} {w2:<15} {cnt:>4}  {enr_pair:>12.2f}×")

    # Coverage by top-N sh-words
    sh_word_types_ordered = [w for w,_ in sh_words_before_qok.most_common()]
    cumsum = 0
    print(f"\n--- Concentration: cumulative sh-word coverage ---")
    for i,w in enumerate(sh_word_types_ordered[:10]):
        cumsum += sh_words_before_qok[w]
        print(f"  Top-{i+1}: {cumsum}/{n_sh_qok} = {cumsum/n_sh_qok:.1%}")

    # Is the enrichment proportional (class-level) or concentrated (word-type level)?
    # If class-level: each sh-word has P(next=qok) ≈ P_class(qok)
    # If word-type level: some sh-words have much higher P(next=qok)
    print(f"\n--- Per-sh-word P(next=qok) distribution ---")
    per_word_rates = {}
    for w,bg_cnt in sorted(sh_bgcount.items(), key=lambda x: -x[1])[:15]:
        qok_count = sh_words_before_qok.get(w,0)
        # Also get sh-word followed by ANY in bigrams
        n_w_any = sum(1 for w1,w2 in bigrams if w1==w)
        if n_w_any > 0:
            rate = qok_count/n_w_any
        else:
            rate = 0
        per_word_rates[w] = (qok_count, n_w_any, rate)
    print(f"{'sh_word':<15} {'Bg':>5} {'→qok':>6} {'→any':>6} {'P(→qok)':>9}")
    for w,bg_cnt in sorted(sh_bgcount.items(), key=lambda x: -x[1])[:15]:
        qc,na,rate = per_word_rates.get(w,(0,0,0))
        # Expected rate = P(qok among MID words after sh)
        qok_rate = sum(1 for w1,w2 in bigrams if get_onset(w1)=='sh' and get_onset(w2)=='qok') / max(sum(1 for w1,w2 in bigrams if get_onset(w1)=='sh'),1)
        print(f"{w:<15} {bg_cnt:>5} {qc:>6} {na:>6} {rate:>9.3f}  (class_rate={qok_rate:.3f})")

def main():
    print("Loading VMS data...")
    mid_bigrams_by_dialect, mid_words_by_dialect = parse_vms()

    # Analyze B-dialect
    analyze_sh_qok(mid_bigrams_by_dialect['B'], mid_words_by_dialect['B'], 'B')

    # Analyze A-dialect
    analyze_sh_qok(mid_bigrams_by_dialect['A'], mid_words_by_dialect['A'], 'A')

    # Cross-dialect comparison of top sh→qok pairs
    print(f"\n{'='*65}")
    print("Cross-dialect sh→qok pair overlap")
    print(f"{'='*65}")
    b_pairs = Counter((w1,w2) for w1,w2 in mid_bigrams_by_dialect['B'] if get_onset(w1)=='sh' and get_onset(w2)=='qok')
    a_pairs = Counter((w1,w2) for w1,w2 in mid_bigrams_by_dialect['A'] if get_onset(w1)=='sh' and get_onset(w2)=='qok')
    shared_pairs = set(b_pairs.keys()) & set(a_pairs.keys())
    print(f"B unique pairs: {len(b_pairs)}, A unique pairs: {len(a_pairs)}, Shared: {len(shared_pairs)}")
    print(f"Top-10 shared pairs (by B count):")
    for (w1,w2) in sorted(shared_pairs, key=lambda x: -b_pairs[x])[:10]:
        print(f"  {w1:<15} → {w2:<15}  B={b_pairs[(w1,w2)]}, A={a_pairs[(w1,w2)]}")

    print("\nDone.")

if __name__=='__main__':
    main()
