"""
exp_322: y+Gallows Compound Structure Confirmation (H523)

Background:
- exp_321 found y-onset B0 = 80% gallows characters (k=44%, t=36%, p=7%, c=5%)
- This implies y-onset words are y+gallows compounds: y(onset)+gallows(B0)+body
- H523: confirm this at word-type level; identify which gallows classes occur;
  check if 'c' at B0 = 'ch'; cross-dialect comparison; full y-onset word inventory

Measurement:
1. Top-30 y-onset MID word types for B and A dialects
2. Parse each word to identify body[0] character (is it gallows?)
3. y+gallows sub-inventory by gallows type (yk-, yt-, yp-, yf-, ych-, bare-c)
4. Cross-dialect overlap: which y-word types are shared A/B?
5. y-onset word structure: what follows the gallows? (the full compound form)
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

GALLOWS_CHARS={'k','t','p','f'}
GALLOWS_COMPOUNDS={'ch','ck','cth','cf','cp'}  # compound forms starting with c

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label
    return 'other'
def get_onset_len(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return len(prefix)
    return 0
def folio_base(folio): return re.sub(r'[rv]$', '', folio)
def classify_dialect(stats):
    total=stats['total']
    if total==0: return 'unknown'
    return 'B' if (stats['edy']+stats['eedy'])/total>=0.05 else 'A'

def get_gallows_class(body):
    """Given a body string (post-y), determine the gallows class."""
    if not body: return 'empty'
    if body[0] in GALLOWS_CHARS: return body[0]  # bare gallows k/t/p/f
    if body.startswith('ch'): return 'ch'
    if body.startswith('ck'): return 'ck'
    if body.startswith('cth'): return 'cth'
    if body.startswith('cf'): return 'cf'
    if body[0] == 'c': return 'c_bare'  # bare c
    return f"other({body[0]})"

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

    mid_by_dialect={'A':[],'B':[]}
    all_by_dialect={'A':[],'B':[]}  # all positions, not just MID
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
            text=re.sub(r'<[^>]+>','',line)
            words=[w for w in re.split(r'[-.\s]',text) if re.match(r'^[a-z]+$',w) and len(w)>=2]
            for w in words:
                if get_onset(w) == 'y':
                    all_by_dialect[dialect].append(w)
            lc_stripped=locus_code.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            if len(words)>=3:
                for w in words[1:-1]:
                    if get_onset(w) == 'y':
                        mid_by_dialect[dialect].append(w)
    return mid_by_dialect, all_by_dialect

def analyze_y_onset(words, label, pos_label):
    print(f"\n{'='*60}")
    print(f"y-onset words — {label} ({pos_label}): N={len(words)}")
    print(f"{'='*60}")

    type_counts = Counter(words)
    total = len(words)
    types = len(type_counts)

    print(f"\nTotal tokens: {total}, Types: {types}")

    # Classify body[0] gallows
    gallows_class_counts = Counter()
    for w,cnt in type_counts.items():
        body = w[1:]  # strip y onset
        gc = get_gallows_class(body)
        gallows_class_counts[gc] += cnt

    print(f"\nGallows class at body[0] (post-y):")
    for cls,cnt in gallows_class_counts.most_common():
        print(f"  {cls:<10}: {cnt:>4} ({cnt/total:.1%})")

    # Total bare gallows
    bare_gallows = sum(gallows_class_counts.get(g,0) for g in ['k','t','p','f'])
    compound_gallows = sum(gallows_class_counts.get(g,0) for g in ['ch','ck','cth','cf'])
    c_bare = gallows_class_counts.get('c_bare',0)
    other = sum(v for k,v in gallows_class_counts.items() if k.startswith('other'))
    empty = gallows_class_counts.get('empty',0)
    print(f"\n  Bare gallows (k/t/p/f): {bare_gallows} ({bare_gallows/total:.1%})")
    print(f"  Compound gallows (ch/ck/cth/cf): {compound_gallows} ({compound_gallows/total:.1%})")
    print(f"  Bare 'c': {c_bare} ({c_bare/total:.1%})")
    print(f"  Other onset at B0: {other} ({other/total:.1%})")

    # Top-30 word types
    print(f"\nTop-30 y-onset word types:")
    print(f"{'Rank':<5} {'Word':<15} {'N':>5} {'%':>7}  {'Body Class':<15} {'Body'}")
    print("-"*65)
    for rank, (w,cnt) in enumerate(type_counts.most_common(30), 1):
        body = w[1:]
        gc = get_gallows_class(body)
        pct = cnt/total
        body_short = body[:10]+'...' if len(body)>10 else body
        print(f"{rank:<5} {w:<15} {cnt:>5} {pct:>7.1%}  {gc:<15} {body_short}")

    # Sub-inventory by gallows class
    print(f"\nSub-inventory by gallows class (top-5 per class):")
    by_class = defaultdict(Counter)
    for w,cnt in type_counts.items():
        body = w[1:]
        gc = get_gallows_class(body)
        by_class[gc][w] += cnt

    for gc in ['k','t','p','f','ch','ck','cth']:
        if gc not in by_class: continue
        class_words = by_class[gc]
        class_total = sum(class_words.values())
        if class_total < 3: continue
        top5 = class_words.most_common(5)
        top5_str = ', '.join(f"{w}({n})" for w,n in top5)
        print(f"  y+{gc:<4}: N={class_total:>3} ({class_total/total:.1%}) — {top5_str}")

def main():
    print("Loading VMS data...")
    mid_by_dialect, all_by_dialect = parse_vms()

    # 1. B-dialect MID y-onset
    analyze_y_onset(mid_by_dialect['B'], 'B-dialect', 'MID only')

    # 2. A-dialect MID y-onset
    analyze_y_onset(mid_by_dialect['A'], 'A-dialect', 'MID only')

    # 3. Cross-dialect word type overlap
    print(f"\n{'='*60}")
    print("Cross-dialect y-onset type overlap (MID words)")
    print(f"{'='*60}")
    b_types = set(Counter(mid_by_dialect['B']).keys())
    a_types = set(Counter(mid_by_dialect['A']).keys())
    shared = b_types & a_types
    b_only = b_types - a_types
    a_only = a_types - b_types
    print(f"B types: {len(b_types)}, A types: {len(a_types)}, Shared: {len(shared)}")
    print(f"Jaccard: {len(shared)/(len(b_types|a_types)):.3f}")

    # Top shared by B frequency
    b_cntr = Counter(mid_by_dialect['B'])
    a_cntr = Counter(mid_by_dialect['A'])
    shared_sorted = sorted(shared, key=lambda x: b_cntr[x], reverse=True)[:15]
    print(f"\nTop-15 shared types (by B frequency):")
    print(f"{'Word':<15} {'B_N':>6} {'A_N':>6}  B+A_pct")
    b_total = sum(b_cntr.values())
    a_total = sum(a_cntr.values())
    for w in shared_sorted:
        bn, an = b_cntr[w], a_cntr[w]
        print(f"{w:<15} {bn:>6} {an:>6}  B={bn/b_total:.1%} A={an/a_total:.1%}")

    print(f"\nTop-10 B-only types:")
    b_only_sorted = sorted(b_only, key=lambda x: b_cntr[x], reverse=True)[:10]
    for w in b_only_sorted:
        body=w[1:]; gc=get_gallows_class(body)
        print(f"  {w:<15} B_N={b_cntr[w]:>4} ({b_cntr[w]/b_total:.1%})  class={gc}")

    print(f"\nTop-10 A-only types:")
    a_only_sorted = sorted(a_only, key=lambda x: a_cntr[x], reverse=True)[:10]
    for w in a_only_sorted:
        body=w[1:]; gc=get_gallows_class(body)
        print(f"  {w:<15} A_N={a_cntr[w]:>4} ({a_cntr[w]/a_total:.1%})  class={gc}")

    # 4. y-onset all positions for reference
    print(f"\n{'='*60}")
    print("y-onset ALL positions (LF+MID+LL) — B-dialect")
    print(f"{'='*60}")
    all_b = Counter(all_by_dialect['B'])
    all_b_total = sum(all_b.values())
    print(f"Total y-onset tokens (all positions): {all_b_total}")
    gallows_all = Counter()
    for w,cnt in all_b.items():
        gc = get_gallows_class(w[1:])
        gallows_all[gc] += cnt
    print("Gallows class distribution (all positions):")
    for gc,cnt in gallows_all.most_common():
        print(f"  {gc:<10}: {cnt:>4} ({cnt/all_b_total:.1%})")

    print("\nDone.")

if __name__=='__main__':
    main()
