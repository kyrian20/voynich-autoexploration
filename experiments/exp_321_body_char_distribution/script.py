"""
exp_321: Body Character Distribution by Onset Class (H521)

Background:
- exp_320 showed d-onset has lowest body entropy at B0-B3 in both dialects
  (B: d-B0=1.451, d-B1=2.342; A: d-B3=2.183 — lowest at that position)
- LOW ENTROPY = CONCENTRATION IN FEW CHARACTERS
- exp_320 measured entropy but not WHICH characters concentrate
- H521: what specific characters appear at d-onset B0-B3?
  - d→-aiin constraint (F289) predicts d-onset body[0] = 'a'
  - y-onset B1 has compressed entropy in B (2.216 bits, lowest at B1)
  - ch-onset has highest entropy at B1-B3 — is it truly flat?

Measurement:
1. For each major onset class, compute P(char | onset, Bi) at positions B0-B3
2. Show top-5 characters by frequency at each position
3. Identify characters that appear EXCLUSIVELY in one onset class's body (cross-onset character gating)
4. Compare A vs B dialect for d-onset (A has more constrained body per exp_320)
5. Also: cross-onset character overlap — Jaccard index between onset class body[0] char sets
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

MAJOR_ONSETS=['qok','ch','sh','d','y','ok','s']

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
                    if onset in MAJOR_ONSETS: mid_by_dialect[dialect][onset].append(w)
    return mid_by_dialect

def body_char_dist(words, max_body_pos=4, min_count=3):
    """For each body position, return Counter of characters."""
    pos_chars=defaultdict(Counter)
    for w in words:
        ol=get_onset_len(w)
        body=w[ol:]
        for i,c in enumerate(body):
            if i>=max_body_pos: break
            pos_chars[i][c]+=1
    return pos_chars

def top_chars(counter, k=6):
    total=sum(counter.values())
    if total==0: return []
    return [(c, cnt, cnt/total) for c,cnt in counter.most_common(k)]

def entropy(counter):
    total=sum(counter.values())
    if total==0: return 0.0
    return -sum((c/total)*math.log2(c/total) for c in counter.values() if c>0)

def print_body_dist(onset, words, dialect):
    n=len(words)
    pos_chars=body_char_dist(words)
    ol=get_onset_len(onset) if onset != 'other' else 0
    print(f"\n  {onset}-onset ({n} words, onset_len={ol}):")
    for pos in range(4):
        cntr=pos_chars.get(pos, Counter())
        if sum(cntr.values()) < 5:
            print(f"    B{pos}: (insufficient data)")
            continue
        total=sum(cntr.values())
        h=entropy(cntr)
        top=top_chars(cntr)
        top_str=', '.join(f"{c}={pct:.1%}" for c,cnt,pct in top[:5])
        top_char,top_cnt,top_pct=top[0] if top else ('?',0,0)
        print(f"    B{pos}: h={h:.3f}  N={total}  top_char='{top_char}' ({top_pct:.1%})  [{top_str}]")

def main():
    print("Loading VMS data...")
    mid_by_dialect=parse_vms()

    for dialect in ['B','A']:
        print(f"\n{'='*70}")
        print(f"DIALECT {dialect}: Body Character Distributions (H521)")
        print(f"{'='*70}")

        onset_data=mid_by_dialect[dialect]

        # 1. Per-onset body character distributions
        print("\n--- Body character frequency distributions by onset class ---")
        for onset in MAJOR_ONSETS:
            words=onset_data.get(onset,[])
            if not words: continue
            print_body_dist(onset, words, dialect)

        # 2. Cross-onset character overlap at B0 and B1
        print(f"\n--- Cross-onset character overlap at B0 (first body char) ---")
        onset_b0_chars={}
        for onset in MAJOR_ONSETS:
            words=onset_data.get(onset,[])
            if not words: continue
            pos_chars=body_char_dist(words)
            cntr=pos_chars.get(0, Counter())
            total=sum(cntr.values())
            if total < 10: continue
            onset_b0_chars[onset]={c: cnt/total for c,cnt in cntr.items()}

        # Print top-3 B0 chars per onset
        print(f"{'Onset':<6} {'N':>6}  Top-3 characters at B0")
        print("-"*60)
        for onset in MAJOR_ONSETS:
            words=onset_data.get(onset,[])
            if not words: continue
            pos_chars=body_char_dist(words)
            cntr=pos_chars.get(0, Counter())
            total=sum(cntr.values())
            if total < 10: continue
            top3=top_chars(cntr, k=3)
            top_str=', '.join(f"'{c}'={pct:.1%}" for c,cnt,pct in top3)
            print(f"{onset:<6} {total:>6}  {top_str}")

        # 3. Which characters appear ONLY in d-onset body (B0-B1) vs other onsets
        print(f"\n--- d-onset vs others: exclusive vs shared characters at B0-B1 ---")
        d_words=onset_data.get('d',[])
        if d_words:
            d_pos=body_char_dist(d_words)
            all_others_pos=defaultdict(Counter)
            for onset in MAJOR_ONSETS:
                if onset == 'd': continue
                words=onset_data.get(onset,[])
                if not words: continue
                pos=body_char_dist(words)
                for p in range(4):
                    for c,cnt in pos[p].items():
                        all_others_pos[p][c]+=cnt
            for bp in [0,1,2]:
                d_chars=set(c for c,cnt in d_pos.get(bp,Counter()).items() if cnt>=3)
                other_chars=set(c for c,cnt in all_others_pos.get(bp,Counter()).items() if cnt>=3)
                d_only=d_chars-other_chars
                others_only=other_chars-d_chars
                shared=d_chars&other_chars
                d_total=sum(d_pos.get(bp,Counter()).values())
                d_only_pct=sum(d_pos.get(bp,Counter()).get(c,0) for c in d_only)/max(d_total,1)
                print(f"  B{bp}: d-only={sorted(d_only)} ({d_only_pct:.1%} of d-B{bp} tokens)")
                print(f"       shared={sorted(shared)}")
                if others_only: print(f"       others-only={sorted(others_only)}")

        # 4. y-onset B1 concentration (y-B1 had lowest entropy at B1 in B-dialect)
        if dialect == 'B':
            print(f"\n--- y-onset B1 character concentration (B-dialect, exp_320: y-B1=2.216 bits) ---")
            y_words=onset_data.get('y',[])
            if y_words:
                y_pos=body_char_dist(y_words)
                cntr=y_pos.get(1, Counter())
                total=sum(cntr.values())
                h=entropy(cntr)
                top=top_chars(cntr, k=8)
                print(f"  y-onset B1: N={total}, h={h:.3f} bits")
                print(f"  Full distribution: {', '.join(f'{c}={pct:.1%}' for c,cnt,pct in top)}")
                # Also show B0
                cntr0=y_pos.get(0, Counter())
                total0=sum(cntr0.values())
                h0=entropy(cntr0)
                top0=top_chars(cntr0, k=8)
                print(f"  y-onset B0: N={total0}, h={h0:.3f} bits")
                print(f"  Full distribution: {', '.join(f'{c}={pct:.1%}' for c,cnt,pct in top0)}")

        # 5. ch-onset body distribution (highest entropy — what's the spread?)
        print(f"\n--- ch-onset body distribution (highest entropy at B1-B3) ---")
        ch_words=onset_data.get('ch',[])
        if ch_words:
            ch_pos=body_char_dist(ch_words, max_body_pos=4)
            for bp in range(4):
                cntr=ch_pos.get(bp, Counter())
                total=sum(cntr.values())
                if total < 5: continue
                h=entropy(cntr)
                top=top_chars(cntr, k=6)
                top_str=', '.join(f"'{c}'={pct:.1%}" for c,cnt,pct in top)
                print(f"  ch B{bp}: N={total}, h={h:.3f}  [{top_str}]")

        # 6. Cross-onset character matrix at B0: who uses what
        print(f"\n--- Cross-onset B0 character matrix (pct of each onset's B0 tokens) ---")
        # Collect all B0 chars
        all_b0_chars=set()
        onset_b0_counts={}
        for onset in MAJOR_ONSETS:
            words=onset_data.get(onset,[])
            if not words: continue
            pos=body_char_dist(words)
            cntr=pos.get(0, Counter())
            if sum(cntr.values()) < 10: continue
            onset_b0_counts[onset]=cntr
            all_b0_chars.update(cntr.keys())
        # Find chars that appear in B0 of at least one onset at >5%
        dominant_chars=set()
        for onset, cntr in onset_b0_counts.items():
            total=sum(cntr.values())
            for c,cnt in cntr.items():
                if cnt/total >= 0.05: dominant_chars.add(c)
        dominant_chars=sorted(dominant_chars)
        # Print matrix
        header='  '+' '.join(f"{c:>5}" for c in dominant_chars)
        print(header)
        for onset in MAJOR_ONSETS:
            if onset not in onset_b0_counts: continue
            cntr=onset_b0_counts[onset]
            total=sum(cntr.values())
            row=f"{onset:<6}"
            for c in dominant_chars:
                pct=cntr.get(c,0)/total
                row+=f" {pct:5.1%}"
            print(row)

    print("\nDone.")

if __name__=='__main__':
    main()
