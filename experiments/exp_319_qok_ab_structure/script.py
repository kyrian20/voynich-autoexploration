"""
exp_319: qok A vs B Internal Structure Analysis (H498)

Background:
- exp_288 (F288): A-qok MLen=1.34 vs B-qok MLen=0.52 (2.6× midfix asymmetry)
- exp_294 (F295): B-qok dominated by edy/eedy/ain/aiin/eey suffixes (59.2% from 5 suffixes)
  with 78.4% ZeroMid; A-qok has richer midfix (ch/e/eo midfixes)
- Question (H498): What drives the A-qok midfix richness?
  Is it one or two high-frequency forms (e.g., qokaiin with 3-char midfix) dominating A?
  Or is the midfix uniformly longer across all A-qok forms?

Measurements:
1. Top-20 qok word types in A vs B by frequency
2. Midfix distribution per dialect: length and content
3. Suffix distribution for qok in each dialect
4. Cross-dialect: which qok types appear in both A and B?
5. Are A-qok long-midfix forms concentrated in specific folios/sections?
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
SUFFIX_PATTERNS=['eedy','edy','aiin','ain','am','ey','ol','or','al','ar','dy']

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label
    return 'other'
def get_onset_len(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return len(prefix)
    return len(w)
def get_suffix(w):
    for s in SUFFIX_PATTERNS:
        if w.endswith(s): return s
    return 'other'
def get_edy_suffix_len(w):
    if w.endswith('eedy'): return 4
    if w.endswith('edy'):  return 3
    return 0
def folio_base(folio): return re.sub(r'[rv]$', '', folio)
def classify_dialect(stats):
    total=stats['total']
    if total==0: return 'unknown'
    return 'B' if (stats['edy']+stats['eedy'])/total>=0.05 else 'A'

def get_midfix(w):
    """Extract midfix: characters between onset and suffix (with edy adjustment)."""
    onset_len=get_onset_len(w)
    suf=get_suffix(w)
    if suf=='other': return None  # skip words with unrecognized suffix
    suf_len=len(suf)
    edy_len=get_edy_suffix_len(w)
    if edy_len>0:
        mid_end=len(w)-edy_len
        midfix=w[onset_len:mid_end]
        if len(midfix)>=1: midfix=midfix[:-1]  # strip edy connector char
    else:
        midfix=w[onset_len:len(w)-suf_len]
    return midfix

def section_from_folio(fb):
    """Rough section classification from folio base."""
    try:
        num=int(''.join(c for c in fb if c.isdigit()))
    except: return 'other'
    if num<=66: return 'herbal'
    elif num<=73: return 'astro'
    elif num<=84: return 'cosmo'
    elif num<=102: return 'bio'
    elif num<=116: return 'pharma'
    else: return 'stars'

def parse_vms():
    """Parse VMS with folio-based dialect classification."""
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

    # Collect MID words by dialect
    mid_by_dialect={'A':[],'B':[]}
    folio_qok_mid={'A':defaultdict(list),'B':defaultdict(list)}
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
            if not words: continue
            # MID words = all except first and last (if line has ≥3 words)
            if len(words)>=3:
                for w in words[1:-1]:
                    mid_by_dialect[dialect].append(w)
                    if get_onset(w)=='qok':
                        folio_qok_mid[dialect][fb].append(w)
    return mid_by_dialect, folio_dialect, folio_qok_mid

def analyze_qok(mid_words, label):
    """Analyze qok word structure in a dialect's MID words."""
    qok_words=[w for w in mid_words if get_onset(w)=='qok']
    if not qok_words:
        print(f"No qok words in {label}")
        return {}
    print(f"\n{'='*60}")
    print(f"qok analysis — {label} dialect ({len(qok_words)} tokens, {len(set(qok_words))} types)")
    print(f"{'='*60}")

    # Top-20 types by frequency
    cnt=Counter(qok_words)
    print(f"\nTop-20 qok word types (of {len(cnt)}):")
    print(f"{'Rank':<5} {'Word':<20} {'Count':>7} {'%Tokens':>8} {'MidLen':>7} {'Suffix':<8} {'Midfix':<15}")
    print("-"*75)
    cum_pct=0.0
    for i,(w,c) in enumerate(cnt.most_common(20), 1):
        pct=c/len(qok_words)*100; cum_pct+=pct
        mf=get_midfix(w); suf=get_suffix(w)
        mf_display=mf if mf is not None else '?'
        print(f"{i:<5} {w:<20} {c:>7} {pct:>7.2f}% {len(mf_display):>7} {suf:<8} {mf_display:<15}")

    # CP90
    from math import inf
    threshold=0.90*len(qok_words); cumulative=0
    cp90=len(cnt)
    for i,(w,c) in enumerate(cnt.most_common(),1):
        cumulative+=c
        if cumulative>=threshold: cp90=i; break
    print(f"\nCP90: {cp90} types cover 90% of {len(qok_words)} tokens")
    print(f"CP90%: {cp90/len(cnt)*100:.1f}% of {len(cnt)} types")

    # Midfix analysis
    midfix_lens=[]; midfixes=[]; zero_mid=0
    valid_qok=[w for w in qok_words if get_suffix(w)!='other']
    for w in valid_qok:
        mf=get_midfix(w)
        if mf is None: continue
        midfix_lens.append(len(mf)); midfixes.append(mf)
        if len(mf)==0: zero_mid+=1
    mean_mlen=sum(midfix_lens)/len(midfix_lens) if midfix_lens else 0
    zero_pct=zero_mid/len(valid_qok)*100 if valid_qok else 0
    print(f"\nMidfix stats (on {len(valid_qok)} words with known suffix):")
    print(f"  Mean midfix length: {mean_mlen:.3f} chars (cf. A expected ~1.34, B expected ~0.52)")
    print(f"  Zero-midfix rate: {zero_pct:.1f}%")
    mf_cnt=Counter(midfixes)
    print(f"  Top-10 non-empty midfixes:")
    non_empty_mf=[(mf,c) for mf,c in mf_cnt.most_common() if mf!=''][:10]
    for mf,c in non_empty_mf:
        print(f"    '{mf}': {c} ({c/len(valid_qok)*100:.1f}%)")

    # Suffix analysis
    print(f"\nSuffix distribution:")
    suf_cnt=Counter(get_suffix(w) for w in qok_words)
    total=sum(suf_cnt.values())
    for suf,c in suf_cnt.most_common():
        print(f"  {suf}: {c} ({c/total*100:.1f}%)")

    # Length distribution
    lens=Counter(len(w) for w in qok_words)
    print(f"\nWord length distribution:")
    for l in sorted(lens.keys()):
        print(f"  len={l}: {lens[l]} ({lens[l]/len(qok_words)*100:.1f}%)")

    return {'cnt': cnt, 'qok_words': qok_words}

def main():
    print("Loading VMS data...")
    mid_by_dialect, folio_dialect, folio_qok_mid = parse_vms()

    for dialect in ('A','B'):
        print(f"\nTotal MID words in {dialect}: {len(mid_by_dialect[dialect])}")

    result_A = analyze_qok(mid_by_dialect['A'], 'A')
    result_B = analyze_qok(mid_by_dialect['B'], 'B')

    # Cross-dialect overlap
    if result_A and result_B:
        a_types = set(result_A['cnt'].keys())
        b_types = set(result_B['cnt'].keys())
        shared = a_types & b_types
        print(f"\n{'='*60}")
        print(f"Cross-dialect qok type overlap")
        print(f"{'='*60}")
        print(f"A types: {len(a_types)}, B types: {len(b_types)}, Shared: {len(shared)}")
        print(f"Shared as % of A: {len(shared)/len(a_types)*100:.1f}%")
        print(f"Shared as % of B: {len(shared)/len(b_types)*100:.1f}%")
        print(f"\nTop-20 shared types (by A+B frequency):")
        shared_sorted=sorted(shared, key=lambda w: result_A['cnt'][w]+result_B['cnt'][w], reverse=True)
        print(f"{'Word':<20} {'A_cnt':>7} {'B_cnt':>7} {'Midfix':<15} {'Suffix':<8}")
        print("-"*60)
        for w in shared_sorted[:20]:
            mf=get_midfix(w); suf=get_suffix(w)
            mf_display=mf if mf is not None else '?'
            print(f"{w:<20} {result_A['cnt'][w]:>7} {result_B['cnt'][w]:>7} {mf_display:<15} {suf:<8}")

        # A-only forms (high midfix length)
        a_only=a_types - b_types
        print(f"\nA-only types: {len(a_only)} (unique to A dialect)")
        a_only_sorted=sorted(a_only, key=lambda w: result_A['cnt'][w], reverse=True)
        print(f"Top-10 A-only types:")
        for w in a_only_sorted[:10]:
            mf=get_midfix(w); suf=get_suffix(w)
            mf_display=mf if mf is not None else '?'
            print(f"  {w} (freq={result_A['cnt'][w]}, midfix='{mf_display}', suf={suf})")

        # A-only long-midfix forms
        a_long_mf=[w for w in a_types if (get_midfix(w) or '') and len(get_midfix(w) or '')>=2]
        print(f"\nA types with midfix ≥ 2 chars: {len(a_long_mf)}")
        b_long_mf=[w for w in b_types if (get_midfix(w) or '') and len(get_midfix(w) or '')>=2]
        print(f"B types with midfix ≥ 2 chars: {len(b_long_mf)}")

        # Common A long-midfix forms
        if a_long_mf:
            a_long_sorted=sorted(a_long_mf, key=lambda w: result_A['cnt'][w], reverse=True)
            print(f"\nTop-10 A long-midfix qok types (≥2 char midfix):")
            for w in a_long_sorted[:10]:
                mf=get_midfix(w)
                print(f"  {w} (freq={result_A['cnt'][w]}, midfix='{mf}' len={len(mf or '')})")

    # Folio distribution of A-qok midfix length
    print(f"\n{'='*60}")
    print(f"A-dialect: qok folio distribution (is long-midfix concentrated in specific folios?)")
    print(f"{'='*60}")
    folio_stats_A={}
    for fb, words in folio_qok_mid['A'].items():
        valid=[w for w in words if get_suffix(w)!='other']
        if not valid: continue
        mf_lens=[len(get_midfix(w) or '') for w in valid]
        mean_mlen=sum(mf_lens)/len(mf_lens)
        folio_stats_A[fb]={'n':len(valid), 'mean_mlen':mean_mlen, 'section':section_from_folio(fb)}

    # Sort by mean_mlen descending
    print(f"Folios with highest mean qok midfix length:")
    sorted_folios=sorted(folio_stats_A.items(), key=lambda x: x[1]['mean_mlen'], reverse=True)
    print(f"{'Folio':<10} {'Section':<10} {'N':>5} {'MeanMLen':>9}")
    for fb,(stats) in sorted_folios[:15]:
        print(f"{fb:<10} {stats['section']:<10} {stats['n']:>5} {stats['mean_mlen']:>9.3f}")

    print(f"\nDone.")

if __name__=='__main__':
    main()
