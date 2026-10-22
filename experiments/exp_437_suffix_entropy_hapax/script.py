"""
exp_437: Suffix Entropy vs Hapax Rate per Onset Class (H497)

Q: Is onset-class suffix entropy correlated with hapax rate?
   If yes: morphological diversity (many suffix forms) generates lexical diversity.
   Under a random model: no correlation expected.

Method: per onset class, compute suffix entropy and hapax rate. Spearman correlation.
Also: B-qok edy-class suffix concentration test (H_new_B).
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

EDY_SUFFIXES = {'eedy', 'edy', 'eey', 'ey'}

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

def get_suffix(word):
    on = get_onset(word)
    body = word[len(on):]
    _, sf = strip_suffix(body)
    return sf

def entropy(counts):
    total = sum(counts.values())
    if total == 0: return 0.0
    return -sum((c/total)*math.log2(c/total) for c in counts.values() if c > 0)

def spearman(xs, ys):
    n = len(xs)
    if n < 3: return float('nan')
    def rank(arr):
        sorted_arr = sorted(enumerate(arr), key=lambda x: x[1])
        ranks = [0]*n
        for rank_val, (idx, _) in enumerate(sorted_arr):
            ranks[idx] = rank_val + 1
        return ranks
    rx = rank(xs); ry = rank(ys)
    d2 = sum((a-b)**2 for a,b in zip(rx,ry))
    return 1 - 6*d2/(n*(n*n-1))

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

def analyze_dialect(folios, dialect_map, target_dial):
    # Global word frequency
    word_counts = Counter()
    for folio, lines in folios.items():
        if dialect_map.get(folio) != target_dial:
            continue
        for ws in lines:
            for w in ws:
                word_counts[w] += 1
    
    # Per onset class: suffix entropy and hapax rate
    onset_data = defaultdict(lambda: {'suffixes': Counter(), 'types': Counter()})
    for word, count in word_counts.items():
        on = get_onset(word)
        sf = get_suffix(word)
        onset_data[on]['suffixes'][sf] += count
        onset_data[on]['types'][word] += count
    
    print(f"\n{'='*60}")
    print(f"Dialect {target_dial}")
    print(f"{'='*60}")
    print(f"{'Onset':<8} {'Tokens':>7} {'Types':>6} {'Hapax':>6} {'Hapax%':>7} {'SufH':>6} {'Type/Tok':>8}")
    
    rows = []
    for on in ONSETS:
        if on not in onset_data: continue
        types = onset_data[on]['types']
        suffixes = onset_data[on]['suffixes']
        total_tokens = sum(types.values())
        total_types = len(types)
        hapax = sum(1 for c in types.values() if c == 1)
        hapax_rate = hapax / total_types if total_types > 0 else 0
        suf_H = entropy(suffixes)
        type_tok = total_types / total_tokens if total_tokens > 0 else 0
        
        if total_tokens < 10:
            continue
        
        print(f"{on:<8} {total_tokens:>7} {total_types:>6} {hapax:>6} {hapax_rate:>7.1%} {suf_H:>6.2f} {type_tok:>8.3f}")
        rows.append((on, total_tokens, total_types, hapax, hapax_rate, suf_H, type_tok))
    
    # Spearman correlation: suffix entropy vs hapax rate
    if len(rows) >= 5:
        suf_Hs = [r[5] for r in rows]
        hapax_rates = [r[4] for r in rows]
        type_toks = [r[6] for r in rows]
        rho_hapax = spearman(suf_Hs, hapax_rates)
        rho_tt = spearman(suf_Hs, type_toks)
        print(f"\n  Spearman(suf_entropy, hapax_rate) = {rho_hapax:.3f}")
        print(f"  Spearman(suf_entropy, type/token)  = {rho_tt:.3f}")
    
    # H_new_B: B-qok edy-class suffix concentration
    if target_dial == 'B' and 'qok' in onset_data:
        qok_sf = onset_data['qok']['suffixes']
        qok_total = sum(qok_sf.values())
        edy_total = sum(qok_sf.get(sf, 0) for sf in EDY_SUFFIXES)
        print(f"\n  B-qok edy-class suffix fraction: {edy_total}/{qok_total} = {edy_total/qok_total:.1%}")
        
        # Compare to other onset classes
        print(f"  edy-class fraction by onset (B):")
        for on in ['qok', 'ch', 'sh', 'd', 'y', 'ok', 'ot', 'ol', 's']:
            if on not in onset_data: continue
            sf_ctr = onset_data[on]['suffixes']
            tot = sum(sf_ctr.values())
            if tot < 20: continue
            edy_n = sum(sf_ctr.get(sf, 0) for sf in EDY_SUFFIXES)
            print(f"    {on:<6}: {edy_n}/{tot} = {edy_n/tot:.1%}")

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)
    analyze_dialect(folios, dialect_map, 'A')
    analyze_dialect(folios, dialect_map, 'B')

if __name__ == '__main__':
    main()
