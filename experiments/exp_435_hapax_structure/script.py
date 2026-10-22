"""
exp_435: Hapax Internal Structure (H495)

Q: Do hapax words (appearing only once) follow the same onset+suffix combinatorics
   as frequent words? If so: supports productive morphology.
   If not: hapaxes are structurally abnormal → constrains generation mechanism.

Method:
- Parse ZL3B corpus; classify A/B dialects
- For each word, compute: onset class, suffix, midfix length, word length
- Split into hapax (freq=1), mid-frequency (freq=2-4), frequent (freq>=5)
- Compare: onset distribution, suffix distribution, word length, midfix entropy
- Do per dialect
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
        if total == 0:
            continue
        edy = sum(1 for ws in lines for w in ws
                  if w.endswith('edy') or w.endswith('eedy'))
        dialect[folio] = 'B' if edy / total >= 0.05 else 'A'
    return dialect

def entropy(counts):
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -sum((c/total)*math.log2(c/total) for c in counts.values() if c > 0)

def analyze(words_by_freq_class, label):
    """Compare hapax vs mid-freq vs frequent words."""
    hapax = words_by_freq_class.get('hapax', [])
    mid   = words_by_freq_class.get('mid', [])
    freq  = words_by_freq_class.get('freq', [])

    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    print(f"  hapax(f=1): N={len(hapax)} tokens / {len(set(hapax))} types")
    print(f"  mid(f=2-4): N={len(mid)} tokens / {len(set(mid))} types")
    print(f"  freq(f>=5): N={len(freq)} tokens / {len(set(freq))} types")

    for name, words in [('hapax', hapax), ('mid(2-4)', mid), ('freq(>=5)', freq)]:
        if not words:
            continue
        # Onset distribution
        onsets = Counter(get_onset(w) for w in words)
        total = len(words)
        # Top onsets
        top_onsets = ', '.join(f"{on}={onsets[on]/total:.1%}" for on in ONSETS
                               if onsets[on] > 0)

        # Suffix distribution
        suffixes = Counter()
        mf_lens = []
        word_lens = [len(w) for w in words]
        for w in words:
            on = get_onset(w)
            body = w[len(on):]
            mf, sf = strip_suffix(body)
            suffixes[sf] += 1
            mf_lens.append(len(mf))

        top_suffixes = ', '.join(f"{sf}={cnt/total:.1%}"
                                  for sf, cnt in suffixes.most_common(8))
        other_rate = sum(1 for w in words if get_onset(w) == 'other') / total
        mean_len = sum(word_lens) / len(word_lens)
        mean_mf = sum(mf_lens) / len(mf_lens)
        onset_H = entropy(onsets)
        suf_H = entropy(suffixes)

        print(f"\n  [{name}] N={total}")
        print(f"    Mean word len: {mean_len:.2f}, Mean midfix: {mean_mf:.2f}")
        print(f"    Onset H: {onset_H:.2f} bits, Suffix H: {suf_H:.2f} bits")
        print(f"    'other' onset: {other_rate:.1%}")
        print(f"    Top onsets: {top_onsets}")
        print(f"    Top suffixes: {top_suffixes}")

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)

    for target_dial in ['A', 'B']:
        # Collect all words with their global frequency in this dialect
        word_counts = Counter()
        for folio, lines in folios.items():
            if dialect_map.get(folio) != target_dial:
                continue
            for ws in lines:
                for w in ws:
                    word_counts[w] += 1

        # Build frequency-class word lists (tokens, not types)
        words_by_class = {'hapax': [], 'mid': [], 'freq': []}
        for folio, lines in folios.items():
            if dialect_map.get(folio) != target_dial:
                continue
            for ws in lines:
                for w in ws:
                    f = word_counts[w]
                    if f == 1:
                        words_by_class['hapax'].append(w)
                    elif f <= 4:
                        words_by_class['mid'].append(w)
                    else:
                        words_by_class['freq'].append(w)

        analyze(words_by_class, f"Dialect {target_dial} — hapax vs frequent word structure")

        # Additional: positional hapax rate (LF vs MID vs LL)
        print(f"\n  --- Positional hapax rates (dialect {target_dial}) ---")
        pos_hapax = {'LF': [0,0], 'MID': [0,0], 'LL': [0,0]}
        for folio, lines in folios.items():
            if dialect_map.get(folio) != target_dial:
                continue
            for ws in lines:
                n = len(ws)
                if n < 2:
                    continue
                # LF
                w = ws[0]; f = word_counts[w]
                pos_hapax['LF'][0] += 1
                if f == 1: pos_hapax['LF'][1] += 1
                # LL
                w = ws[-1]; f = word_counts[w]
                pos_hapax['LL'][0] += 1
                if f == 1: pos_hapax['LL'][1] += 1
                # MID
                for w in ws[1:-1]:
                    f = word_counts[w]
                    pos_hapax['MID'][0] += 1
                    if f == 1: pos_hapax['MID'][1] += 1

        for pos, (total, n_hapax) in pos_hapax.items():
            if total > 0:
                print(f"    {pos}: {n_hapax}/{total} = {n_hapax/total:.1%} hapax")

if __name__ == '__main__':
    main()
