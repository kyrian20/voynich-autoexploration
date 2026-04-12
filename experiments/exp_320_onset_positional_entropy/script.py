"""
exp_320: Positional Character Entropy Conditioned on Onset Class (H493)

Background:
- exp_259 measured overall positional character entropy across all VMS words
- H493: do different onset classes have DIFFERENT entropy profiles at positions
  within the word body (post-onset)?
- If profiles diverge: onset class predicts internal structure (morphological system)
- If profiles converge: onset is interchangeable with body (glossographic/template)

Measurement:
1. For each major onset class, strip onset prefix
2. Compute h(c_i) at each position i within the word body (relative to onset end)
3. Compare entropy profiles: h(body[0]), h(body[1]), h(body[2]), h(body[3]) by onset class
4. Also compare absolute positions h(word[0]), h(word[1]), ... (overall word)

Do both dialects. Focus on MID words (most diverse position).

Test for two outcomes:
  - Convergence: all onset classes have ~same body entropy profile (body is independent of onset)
  - Divergence: different onset classes have different body entropy profiles (onset predicts body)
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

MAJOR_ONSETS_FOCUS=['qok','ch','sh','d','y','ok','s']

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

def entropy(char_list):
    """Shannon entropy in bits of a character sequence."""
    if not char_list: return 0.0
    cnt=Counter(char_list); n=len(char_list)
    return -sum((c/n)*math.log2(c/n) for c in cnt.values() if c>0)

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
                    if onset in MAJOR_ONSETS_FOCUS: mid_by_dialect[dialect][onset].append(w)
    return mid_by_dialect

def compute_body_entropy(words, max_body_pos=8, min_count=5):
    """Compute entropy at each relative position within the word body (post-onset)."""
    body_chars_by_pos=defaultdict(list)
    for w in words:
        ol=get_onset_len(w)
        body=w[ol:]
        for i, c in enumerate(body):
            if i>=max_body_pos: break
            body_chars_by_pos[i].append(c)
    entropies={}
    counts={}
    for pos in range(max_body_pos):
        chars=body_chars_by_pos.get(pos,[])
        if len(chars)>=min_count:
            entropies[pos]=entropy(chars)
            counts[pos]=len(chars)
    return entropies, counts

def compute_absolute_entropy(words, max_abs_pos=12, min_count=5):
    """Compute entropy at each absolute position within the full word."""
    abs_chars_by_pos=defaultdict(list)
    for w in words:
        for i,c in enumerate(w):
            if i>=max_abs_pos: break
            abs_chars_by_pos[i].append(c)
    entropies={}
    for pos in range(max_abs_pos):
        chars=abs_chars_by_pos.get(pos,[])
        if len(chars)>=min_count:
            entropies[pos]=entropy(chars)
    return entropies

def main():
    print("Loading VMS data...")
    mid_by_dialect=parse_vms()

    for dialect in ['B','A']:
        print(f"\n{'='*70}")
        print(f"{'='*70}")
        print(f"DIALECT {dialect}")
        print(f"{'='*70}")

        onset_data=mid_by_dialect[dialect]

        # 1. Body entropy profiles by onset class
        print(f"\n--- Body entropy (post-onset positions 0-7) by onset class ---")
        print(f"Body position: relative to end of onset prefix")
        print(f"{'Onset':<6} {'N':>6} ", end='')
        for i in range(8): print(f" B{i}:h  ", end='')
        print()
        print("-"*80)

        # Also collect all onset body chars for comparison
        all_body=defaultdict(list)

        onset_entropies={}
        for onset in MAJOR_ONSETS_FOCUS:
            words=onset_data.get(onset,[])
            if not words: continue
            entropies, counts=compute_body_entropy(words)
            onset_entropies[onset]=entropies
            n=len(words)
            ol=get_onset_len(onset)  # onset length for this class
            print(f"{onset:<6} {n:>6} ", end='')
            for i in range(8):
                if i in entropies: print(f"{entropies[i]:6.3f} ", end='')
                else: print(f"   --- ", end='')
            print(f"  (onset_len={ol})")
            # Collect all bodies
            for w in words:
                body=w[get_onset_len(w):]
                for i,c in enumerate(body):
                    if i<8: all_body[i].append(c)

        # Overall body entropy (all onsets combined)
        print(f"\n{'ALL':<6} {sum(len(v) for v in onset_data.values()):>6} ", end='')
        for i in range(8):
            chars=all_body.get(i,[])
            if len(chars)>=5: print(f"{entropy(chars):6.3f} ", end='')
            else: print(f"   --- ", end='')
        print(" (all onsets combined)")

        # 2. Divergence analysis: compute pairwise entropy difference at each body position
        print(f"\n--- Onset-class divergence: max - min entropy at each body position ---")
        print(f"High divergence = onset class predicts character at that position")
        print(f"{'Pos':<4} {'MaxH':>7} {'MinH':>7} {'Range':>7} {'MaxOnset':<8} {'MinOnset':<8}")
        print("-"*45)
        for pos in range(6):
            vals=[(onset, ent[pos]) for onset, ent in onset_entropies.items() if pos in ent]
            if len(vals)<2: continue
            vals.sort(key=lambda x: x[1], reverse=True)
            max_onset, max_h = vals[0]
            min_onset, min_h = vals[-1]
            range_h=max_h-min_h
            print(f"B{pos:<3} {max_h:>7.3f} {min_h:>7.3f} {range_h:>7.3f} {max_onset:<8} {min_onset:<8}")

        # 3. Absolute position entropy
        print(f"\n--- Absolute position entropy (word positions 0-10, all onsets) ---")
        print(f"{'Onset':<6} ", end='')
        for i in range(10): print(f" P{i}:h  ", end='')
        print()
        print("-"*80)
        for onset in MAJOR_ONSETS_FOCUS:
            words=onset_data.get(onset,[])
            if not words: continue
            abs_ent=compute_absolute_entropy(words)
            print(f"{onset:<6} ", end='')
            for i in range(10):
                if i in abs_ent: print(f"{abs_ent[i]:6.3f} ", end='')
                else: print(f"   --- ", end='')
            print()

        # 4. Summary: entropy at position 0 of body (first post-onset character)
        print(f"\n--- Body position 0 entropy summary (first character after onset) ---")
        print(f"This is the key discriminator: if onset predicts body[0], onset is morphological")
        print(f"{'Onset':<6} {'N':>6} {'h(body[0])':>12} {'h(body[1])':>12}")
        print("-"*40)
        for onset in MAJOR_ONSETS_FOCUS:
            words=onset_data.get(onset,[])
            if not words: continue
            ent,cnt=compute_body_entropy(words)
            h0=ent.get(0,'---'); h1=ent.get(1,'---')
            h0_s=f"{h0:12.3f}" if isinstance(h0,float) else f"{'---':>12}"
            h1_s=f"{h1:12.3f}" if isinstance(h1,float) else f"{'---':>12}"
            print(f"{onset:<6} {len(words):>6} {h0_s} {h1_s}")

    print("\nDone.")

if __name__=='__main__':
    main()
