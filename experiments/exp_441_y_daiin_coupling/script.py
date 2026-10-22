"""
exp_441: y→d Coupling Word-Level Analysis (H569)

Q: Is F326's y→d bigram (B=1.49×, A=1.37×) driven by y→daiin specifically,
   or by y→(any d-onset word)? Which position pair drives the effect?

Method:
- B and A continuation lines
- For each adjacent word pair (w1, w2), record: onset(w1), onset(w2), w2 word
- When onset(w1)=y: what fraction of w2 is 'daiin' vs other d-onset words?
- Decompose by position pair: LF→pos1, pos1→pos2, MID_inner, pre-LL→LL
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

ONSETS = ['qok', 'qot', 'qo', 'cth', 'ch', 'sh', 'ok', 'ot', 'ol',
          'd', 's', 'y', 'k', 't', 'l', 'r', 'p', 'f', 'o']

def get_onset(word):
    for on in ONSETS:
        if word.startswith(on):
            return on
    return 'other'

def get_position_pair(i, n):
    """Return position-pair label for adjacent (i, i+1) in a line of length n."""
    if i == 0:
        return 'LF→pos1'
    elif i == 1:
        return 'pos1→pos2'
    elif i == n - 2:
        return 'pre-LL→LL'
    else:
        return 'MID_inner'

def parse_corpus():
    pattern = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
    folios = defaultdict(list)
    with open(ZL3B, encoding='utf-8') as f:
        for line in f:
            for m in pattern.finditer(line):
                folio = m.group(1).lstrip('+*=&~')
                lc = m.group(3).lstrip('+*=/~&')
                if not lc.lstrip('@').startswith('P'):
                    continue
                text = m.group(4).strip()
                words = [w for w in re.split(r'[-.\s]', text)
                         if re.match(r'^[a-z]+$', w) and len(w) >= 2]
                if words:
                    folios[folio].append(words)
    return folios

def classify_dialects(folios):
    dialect = {}
    for folio, lines in folios.items():
        total = sum(len(ws) for ws in lines)
        if total == 0: continue
        edy = sum(1 for ws in lines for w in ws
                  if w.endswith('edy') or w.endswith('eedy'))
        dialect[folio] = 'B' if edy / total >= 0.05 else 'A'
    return dialect

def analyze(folios, dialect_map, target_dial):
    # For y→next bigrams: count by position pair and w2 identity
    y_to_d = {'LF→pos1': Counter(), 'pos1→pos2': Counter(),
               'MID_inner': Counter(), 'pre-LL→LL': Counter()}
    all_bigrams = Counter()  # (onset1, onset2) counts
    y_bigrams = Counter()  # (onset2) counts given onset1=y
    
    for folio, lines in folios.items():
        if dialect_map.get(folio) != target_dial: continue
        for ws in lines:
            n = len(ws)
            if n < 2: continue
            for i in range(n - 1):
                w1, w2 = ws[i], ws[i+1]
                o1, o2 = get_onset(w1), get_onset(w2)
                all_bigrams[(o1, o2)] += 1
                pp = get_position_pair(i, n)
                if o1 == 'y':
                    y_bigrams[o2] += 1
                    if o2 == 'd':
                        y_to_d[pp][w2] += 1
    
    # Overall y→d enrichment
    total_pairs = sum(all_bigrams.values())
    y_total = sum(all_bigrams[(o, 'x')] for o in [] + [o for o, o2 in all_bigrams if o == 'y'])
    y_total_correct = sum(v for (o1, o2), v in all_bigrams.items() if o1 == 'y')
    d_total = sum(v for (o1, o2), v in all_bigrams.items() if o2 == 'd')
    y_d_obs = all_bigrams.get(('y', 'd'), 0)
    y_d_exp = y_total_correct * d_total / total_pairs if total_pairs > 0 else 0
    E_y_d = y_d_obs / y_d_exp if y_d_exp > 0 else 0
    
    print(f"\n{'='*60}")
    print(f"Dialect {target_dial}")
    print(f"{'='*60}")
    print(f"  Total bigram pairs: {total_pairs}")
    print(f"  y-onset leading: {y_total_correct} pairs")
    print(f"  y→d observed: {y_d_obs}, expected: {y_d_exp:.1f}, E={E_y_d:.2f}×")
    
    # Word-level decomposition of y→d
    print(f"\n  y→d word decomposition:")
    total_yd = sum(y_to_d[pp][w] for pp in y_to_d for w in y_to_d[pp])
    daiin_n = sum(y_to_d[pp].get('daiin', 0) for pp in y_to_d)
    print(f"  Total y→d bigrams: {total_yd}")
    print(f"  y→daiin specifically: {daiin_n} = {daiin_n/total_yd:.1%} of y→d")
    
    # Position-pair decomposition
    print(f"\n  y→d by position pair:")
    for pp in ['LF→pos1', 'pos1→pos2', 'MID_inner', 'pre-LL→LL']:
        ctr = y_to_d[pp]
        n_total = sum(ctr.values())
        if n_total == 0:
            print(f"    {pp}: 0")
            continue
        n_daiin = ctr.get('daiin', 0)
        top_words = [(w, c) for w, c in ctr.most_common(5)]
        print(f"    {pp}: N={n_total}, daiin={n_daiin}({n_daiin/n_total:.0%}), top: {top_words}")
    
    # y-onset next-word distribution (for reference)
    print(f"\n  y→? onset distribution (top 5):")
    for on, count in sorted(y_bigrams.items(), key=lambda x: -x[1])[:8]:
        rate = count / y_total_correct
        print(f"    y→{on}: {count} ({rate:.1%})")
    
    # Also: what fraction of y→d is driven by y-onset words (which y word leads to d)?
    # Already have the position-pair decomposition; let's just note the daiin fraction

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)
    analyze(folios, dialect_map, 'A')
    analyze(folios, dialect_map, 'B')

if __name__ == '__main__':
    main()
