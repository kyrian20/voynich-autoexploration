"""
exp_438: Stolfi Decomposition by Onset Class (H492)

Q: Do different onset classes have different internal structures 
   (midfix length, suffix diversity)? This is exploratory — comparing
   onset vs suffix independence across onset classes.

Method:
- Strip onset from each word; extract suffix (longest-match)
- Compute midfix = remaining body
- Per onset class: zero-midfix fraction, mean midfix length, top suffixes
- Compare across onset classes within each dialect
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict
import math

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

ONSETS = ['qok', 'qot', 'qo', 'cth', 'ch', 'sh', 'ok', 'ot', 'ol',
          'd', 's', 'y', 'k', 't', 'l', 'r', 'p', 'f', 'o']

SUFFIXES = [
    'aiin', 'aiir', 'ain', 'air', 'aii',
    'eedy', 'edy', 'eey', 'ey',
    'ckhy', 'ckh', 'cthy', 'cth',
    'chedy', 'chey', 'chol', 'cheol', 'cheor', 'chor', 'cho', 'ch',
    'shedy', 'shey', 'shol', 'shor', 'sho', 'sh',
    'dy', 'y',
    'ar', 'or', 'ol', 'al',
    'am', 'om',
    'iin', 'iir', 'in',
    'l', 'r', 'n',
]
SUFFIXES.sort(key=lambda x: -len(x))

def get_onset(word):
    for on in ONSETS:
        if word.startswith(on):
            return on
    return 'other'

def strip_suffix(body):
    for s in SUFFIXES:
        if body.endswith(s) and len(body) > len(s):
            return body[:-len(s)], s
        elif body == s:
            return '', s
    return body, ''

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

def entropy(counts):
    total = sum(counts.values())
    if total == 0: return 0.0
    return -sum((c/total)*math.log2(c/total) for c in counts.values() if c > 0)

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)
    
    for target_dial in ['A', 'B']:
        # Collect word-level data by onset class
        onset_stats = defaultdict(lambda: {
            'tokens': 0,
            'mf_lens': [],
            'suffixes': Counter(),
            'zero_mf': 0,
        })
        
        for folio, lines in folios.items():
            if dialect_map.get(folio) != target_dial:
                continue
            for ws in lines:
                for w in ws:
                    on = get_onset(w)
                    if on == 'other':
                        continue
                    body = w[len(on):]
                    mf, sf = strip_suffix(body)
                    onset_stats[on]['tokens'] += 1
                    onset_stats[on]['mf_lens'].append(len(mf))
                    onset_stats[on]['suffixes'][sf] += 1
                    if mf == '':
                        onset_stats[on]['zero_mf'] += 1
        
        print(f"\n{'='*75}")
        print(f"Dialect {target_dial} — Stolfi decomposition by onset class (EXPLORATORY)")
        print(f"{'='*75}")
        print(f"{'Onset':<6} {'Tokens':>7} {'ZeroMF%':>8} {'MeanMF':>7} {'MaxMF':>6} {'SufH':>6} {'Top suffix':>12}")
        
        onset_rows = []
        for on in ONSETS:
            if on not in onset_stats or onset_stats[on]['tokens'] < 20:
                continue
            st = onset_stats[on]
            total = st['tokens']
            mf_lens = st['mf_lens']
            mean_mf = sum(mf_lens) / len(mf_lens)
            max_mf = max(mf_lens)
            zero_mf_pct = st['zero_mf'] / total
            suf_H = entropy(st['suffixes'])
            top_sf, top_sf_n = st['suffixes'].most_common(1)[0]
            top_sf_pct = top_sf_n / total
            
            print(f"{on:<6} {total:>7} {zero_mf_pct:>8.1%} {mean_mf:>7.2f} {max_mf:>6} {suf_H:>6.2f} {top_sf!r:>10}={top_sf_pct:.0%}")
            onset_rows.append((on, total, zero_mf_pct, mean_mf, suf_H))
        
        # Highlight key structural splits
        print(f"\n  Key structural groups:")
        print(f"  HIGH zero-midfix (template skeletons):")
        for on, total, zmf, mmf, sufH in sorted(onset_rows, key=lambda x: -x[2]):
            if zmf >= 0.70 and total >= 50:
                print(f"    {on}: {zmf:.1%} zero-midfix, MeanMF={mmf:.2f}")
        print(f"  LOW zero-midfix (complex interior structure):")
        for on, total, zmf, mmf, sufH in sorted(onset_rows, key=lambda x: x[2]):
            if zmf <= 0.45 and total >= 50:
                print(f"    {on}: {zmf:.1%} zero-midfix, MeanMF={mmf:.2f}")
        
        # Top suffix by onset (with concentration)
        print(f"\n  Top suffix concentration:")
        for on in ['ch', 'sh', 'qok', 'd', 'y', 'ok', 'ot']:
            if on not in onset_stats or onset_stats[on]['tokens'] < 50:
                continue
            st = onset_stats[on]
            total = st['tokens']
            top3 = st['suffixes'].most_common(3)
            top3_str = ', '.join(f"{sf!r}={n/total:.0%}" for sf, n in top3)
            print(f"    {on}: {top3_str}")

if __name__ == '__main__':
    main()
