"""
exp_325: s-Onset Internal Structure (H524)

Background:
- exp_321 found s-onset B0='a'=62.8% (B), 37.1% (A) — similar to d-onset 'a'=73.0%/70.2%
- exp_321 B1='i'=40.1% (B), 28.7% (A); B2='i'=33.0% (B); B3='n'=40.5% (B)
  -- This matches d-onset body sequence a+i+i+n (daiin template)
- H524: Is s-onset saiin-dominated like d-onset is daiin-dominated?
- exp_324: s-onset bigram behavior -- d→d enriched (1.54×, self-succession); s→d enriched (1.62×)
  -- s→d coupling in B-dialect (1.62×) is similar to y→d (1.37×)

Measurement:
1. Top-30 s-onset word types for B and A dialects (MID and ALL positions)
2. s-onset vs d-onset word-type comparison: how much overlap?
3. Confirm body character sequence a+i+i+n for s-onset
4. Section distribution of s-onset
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

    mid_by_dialect={'A':defaultdict(list),'B':defaultdict(list)}
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
            if len(words)>=3:
                for w in words[1:-1]:
                    onset=get_onset(w)
                    if onset in ('s','d'):
                        mid_by_dialect[dialect][onset].append(w)
    return mid_by_dialect

def analyze_onset(words, onset_label, dialect):
    n = len(words)
    type_counts = Counter(words)
    types = len(type_counts)
    print(f"\n{onset_label}-onset ({dialect}-dialect): N={n} tokens, {types} types")
    print(f"Top-30 word types:")
    print(f"{'Rank':<5} {'Word':<15} {'N':>5} {'%':>7}  Body_sequence")
    total = n
    for rank,(w,cnt) in enumerate(type_counts.most_common(30), 1):
        body = w[len(onset_label):]  # strip onset
        pct = cnt/total
        print(f"{rank:<5} {w:<15} {cnt:>5} {pct:>7.1%}  {body}")

def compare_s_d(s_words, d_words, dialect):
    """Compare s-onset and d-onset word types."""
    s_cntr = Counter(s_words)
    d_cntr = Counter(d_words)
    s_total = sum(s_cntr.values())
    d_total = sum(d_cntr.values())

    # For each s-word, find analogous d-word (replace leading 's' with 'd')
    print(f"\n--- s vs d structural analogues ({dialect}-dialect) ---")
    print(f"s-onset N={s_total}, d-onset N={d_total}")
    print(f"\nTop-20 s-onset words and their 'd'-analogues:")
    print(f"{'s_word':<15} {'s_N':>5} {'s_%':>6}  {'d_analogue':<15} {'d_N':>5} {'d_%':>6}")
    print("-"*65)
    for w,cnt in s_cntr.most_common(20):
        d_analogue = 'd' + w[1:]  # replace 's' onset with 'd'
        d_cnt = d_cntr.get(d_analogue, 0)
        s_pct = cnt/s_total
        d_pct = d_cnt/d_total if d_total>0 else 0
        print(f"{w:<15} {cnt:>5} {s_pct:>6.1%}  {d_analogue:<15} {d_cnt:>5} {d_pct:>6.1%}")

    # How many top-20 s-words have a d-analogue in top-20 d-words?
    top20_s = {w for w,_ in s_cntr.most_common(20)}
    top20_d = {w for w,_ in d_cntr.most_common(20)}
    s_to_d_analogues = {w: 'd'+w[1:] for w in top20_s}
    shared_analogues = {w for w,dw in s_to_d_analogues.items() if dw in top20_d}
    print(f"\n{len(shared_analogues)}/20 top s-words have top-20 d-analogues")

    # s-specific forms (not a simple d-analogue)
    s_specific = [(w,cnt) for w,cnt in s_cntr.most_common(20) if d_cntr.get('d'+w[1:], 0) == 0]
    print(f"s-specific forms (no d-analogue):")
    for w,cnt in s_specific[:10]:
        print(f"  {w} (N={cnt})")

def main():
    print("Loading VMS data...")
    mid_by_dialect = parse_vms()

    # B-dialect
    for dialect in ['B','A']:
        print(f"\n{'='*65}")
        print(f"DIALECT {dialect}")
        print(f"{'='*65}")

        s_words = mid_by_dialect[dialect].get('s',[])
        d_words = mid_by_dialect[dialect].get('d',[])

        analyze_onset(s_words, 's', dialect)
        analyze_onset(d_words, 'd', dialect)
        compare_s_d(s_words, d_words, dialect)

    # Cross-dialect comparison for s-onset
    print(f"\n{'='*65}")
    print("s-onset cross-dialect comparison (B vs A)")
    print(f"{'='*65}")
    b_s = Counter(mid_by_dialect['B'].get('s',[]))
    a_s = Counter(mid_by_dialect['A'].get('s',[]))
    b_total = sum(b_s.values())
    a_total = sum(a_s.values())
    shared = set(b_s.keys()) & set(a_s.keys())
    print(f"B types: {len(b_s)}, A types: {len(a_s)}, Shared: {len(shared)}")
    print(f"Jaccard: {len(shared)/(len(b_s|a_s)):.3f}")
    print(f"\nTop-15 by B frequency:")
    print(f"{'Word':<15} {'B_N':>5} {'B_%':>6}  {'A_N':>5} {'A_%':>6}")
    for w,cnt in b_s.most_common(15):
        a_cnt = a_s.get(w,0)
        print(f"{w:<15} {cnt:>5} {cnt/b_total:>6.1%}  {a_cnt:>5} {a_cnt/a_total if a_total else 0:>6.1%}")

    print("\nDone.")

if __name__=='__main__':
    main()
