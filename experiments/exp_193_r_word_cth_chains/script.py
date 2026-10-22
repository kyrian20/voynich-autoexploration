"""
exp_193: 'r' Word Profile + cth Chain Length + [oty][l@LL] B-Stars

H354: Is 'r' a function word? Full positional and bigram profile.
H355: [oty][l@LL] in B-Stars — is l-word specifically at LL after oty?
+ cth chain length: what is the longest cth-word run in a single line?
+ cthey→ch cycle: does [cthey][ch-word] return to cthey?
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

CORPUS = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

def get_onset(word):
    w = word.lower()
    if w.startswith('qok'): return 'qok'
    if w.startswith('qot'): return 'qot'
    if w.startswith('qo'): return 'qo'
    if w.startswith('cth'): return 'cth'
    if w.startswith('ch'): return 'ch'
    if w.startswith('sh'): return 'sh'
    if w.startswith('ok'): return 'ok'
    if w.startswith('ot'): return 'ot'
    if w.startswith('ol'): return 'ol'
    if w.startswith('d'): return 'd'
    if w.startswith('s'): return 's'
    if w.startswith('y'): return 'y'
    if w.startswith('k'): return 'k'
    if w.startswith('t'): return 't'
    if w.startswith('l'): return 'l'
    if w.startswith('r'): return 'r'
    if w.startswith('p'): return 'p'
    if w.startswith('f'): return 'f'
    return 'other'

def is_ch_e(word):
    w = word.lower()
    return w.startswith('che') or w.startswith('chi')

def parse_locus(locus_raw):
    locus_parts = locus_raw.split(',')
    if len(locus_parts) < 2: return None, None, None
    folio_str = locus_parts[0]
    folio_base = folio_str.split('.')[0].lstrip('<')
    m = re.match(r'f(\d+)', folio_base)
    folio_num = int(m.group(1)) if m else None
    lt_raw = locus_parts[1].rstrip('>')
    lt = lt_raw.lstrip('@+*=~&')
    line_m = re.search(r'\.(\d+),', locus_raw)
    line_num = int(line_m.group(1)) if line_m else None
    return folio_num, lt, line_num

folio_words = defaultdict(list)
raw_lines = []
with open(CORPUS) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'): continue
        parts = line.split(None, 1)
        if len(parts) < 2: continue
        locus_raw, text = parts
        folio_num, lt, line_num = parse_locus(locus_raw)
        if folio_num is None: continue
        if not lt.startswith('P'): continue
        words = [w for w in text.split('.') if w and re.match(r'[a-z]', w) and not w.startswith('<')]
        if not words: continue
        folio_words[folio_num].extend(words)
        raw_lines.append((folio_num, line_num, words))

folio_dialect = {}
for fn, wds in folio_words.items():
    if len(wds) < 10: continue
    edy_count = sum(1 for w in wds if 'edy' in w or 'eedy' in w)
    folio_dialect[fn] = 'B' if edy_count/len(wds) >= 0.05 else 'A'

lines_data = [(fn, ln, folio_dialect.get(fn, 'unknown'), wds) for fn, ln, wds in raw_lines]
a_lines = [(fn, ln, wds) for fn, ln, dial, wds in lines_data if dial == 'A']
b_lines = [(fn, ln, wds) for fn, ln, dial, wds in lines_data if dial == 'B']

A_words = [w for fn, ln, wds in a_lines for w in wds]
B_words = [w for fn, ln, wds in b_lines for w in wds]
A_onset = Counter(get_onset(w) for w in A_words)
B_onset = Counter(get_onset(w) for w in B_words)
A_total, B_total = len(A_words), len(B_words)

print(f"A: {len(a_lines)} lines ({A_total} words) | B: {len(b_lines)} lines ({B_total} words)")

# ---- H354: 'r' word profile ----
print("\n" + "="*60)
print("H354: 'r' as function word — positional profile and bigrams")
print("="*60)

# r-words in A
r_words_all = [w for w in A_words if get_onset(w) == 'r']
r_bare = [w for w in r_words_all if w == 'r']
print(f"\nAll r-onset words in A (n={len(r_words_all)}):")
print(f"r-word frequency: {Counter(r_words_all).most_common(15)}")
print(f"Bare 'r' count: {len(r_bare)} / {len(r_words_all)} = {len(r_bare)/len(r_words_all):.1%}")

# r in B
r_words_b = [w for w in B_words if get_onset(w) == 'r']
print(f"\nr-onset in B: {len(r_words_b)} words")
print(f"B r-words: {Counter(r_words_b).most_common(10)}")

# Positional profile of 'r' in A+B
r_positions_a = []
for fn, ln, wds in a_lines:
    for i, w in enumerate(wds):
        if get_onset(w) == 'r':
            pos = 'LF' if i == 0 else ('LL' if i == len(wds)-1 else 'MID')
            is_bare = (w == 'r')
            r_positions_a.append({'pos': pos, 'word': w, 'is_bare': is_bare, 'folio': fn, 'line': ln})

pos_all = Counter(d['pos'] for d in r_positions_a)
pos_bare = Counter(d['pos'] for d in r_positions_a if d['is_bare'])
pos_non_bare = Counter(d['pos'] for d in r_positions_a if not d['is_bare'])
n_r = len(r_positions_a)
n_bare = sum(1 for d in r_positions_a if d['is_bare'])
n_non_bare = n_r - n_bare

# A baselines
a_pos_total = Counter()
for fn, ln, wds in a_lines:
    for i, w in enumerate(wds):
        pos = 'LF' if i == 0 else ('LL' if i == len(wds)-1 else 'MID')
        a_pos_total[pos] += 1
a_pos_base = {k: v/sum(a_pos_total.values()) for k, v in a_pos_total.items()}

print(f"\nA-dialect r-word positions (n={n_r}):")
for p in ['LF', 'MID', 'LL']:
    cnt = pos_all[p]
    base = a_pos_base.get(p, 0)
    rate = cnt/n_r
    print(f"  {p}: {cnt} ({rate:.3f} vs base {base:.3f} = {rate/base:.2f}×)")

print(f"\nBare 'r' positions (n={n_bare}):")
for p in ['LF', 'MID', 'LL']:
    cnt = pos_bare[p]
    rate = cnt/n_bare if n_bare else 0
    base = a_pos_base.get(p, 0)
    print(f"  {p}: {cnt} ({rate:.3f} vs base {base:.3f} = {rate/base:.2f}× if n>0)")

print(f"\nNon-bare r-words positions (n={n_non_bare}):")
for p in ['LF', 'MID', 'LL']:
    cnt = pos_non_bare[p]
    rate = cnt/n_non_bare if n_non_bare else 0
    base = a_pos_base.get(p, 0)
    print(f"  {p}: {cnt} ({rate:.3f} vs base {base:.3f})")

# Folio distribution of r-onset words
r_folio = Counter(d['folio'] for d in r_positions_a)
print(f"\nFolio distribution of r-onset words in A:")
print(f"  {dict(sorted(r_folio.items()))}")

# Bigrams: what precedes r?
r_precedes = []
r_follows = []
for fn, ln, wds in a_lines:
    for i, w in enumerate(wds):
        if get_onset(w) == 'r':
            if i > 0:
                r_precedes.append((wds[i-1], w))
            if i < len(wds)-1:
                r_follows.append((w, wds[i+1]))

print(f"\nOnsets preceding r-word (n={len(r_precedes)}):")
prec_onset = Counter(get_onset(a) for a,b in r_precedes)
for onset, cnt in prec_onset.most_common():
    base = A_onset[onset]/A_total
    rate = cnt/len(r_precedes)
    print(f"  {onset}: {cnt} ({rate:.3f}, base={base:.3f}, {rate/base:.2f}×)")

print(f"\nOnsets following r-word (n={len(r_follows)}):")
foll_onset = Counter(get_onset(b) for a,b in r_follows)
for onset, cnt in foll_onset.most_common():
    base = A_onset[onset]/A_total
    rate = cnt/len(r_follows)
    print(f"  {onset}: {cnt} ({rate:.3f}, base={base:.3f}, {rate/base:.2f}×)")

# ch_e specifically
che_pre_r = sum(1 for a,b in r_precedes if is_ch_e(a))
che_post_r = sum(1 for a,b in r_follows if is_ch_e(b))
print(f"\nch_e specifically: {che_pre_r}/{len(r_precedes)} precede r; {che_post_r}/{len(r_follows)} follow r")

# Full list of lines containing r-onset
r_containing_lines_a = [(fn, ln, wds) for fn, ln, wds in a_lines if any(get_onset(w) == 'r' for w in wds)]
print(f"\nLines in A containing r-onset words (n={len(r_containing_lines_a)}):")
for fn, ln, wds in r_containing_lines_a[:20]:
    print(f"  f{fn}.{ln}: {' '.join(wds)}")

# ---- H355: [oty][l@LL] in B-Stars ----
print("\n" + "="*60)
print("H355: [oty][l@LL] in B-Stars — penultimate oty with l-word at LL")
print("="*60)

# All B lines ending in l-onset
b_l_ll_lines = [(fn, ln, wds) for fn, ln, wds in b_lines if wds and get_onset(wds[-1]) == 'l']
print(f"\nB lines ending in l-onset (l@LL): {len(b_l_ll_lines)}")
# Among these, how many have oty as penultimate?
b_oty_l_ll = [(fn, ln, wds) for fn, ln, wds in b_l_ll_lines if len(wds) >= 2 and wds[-2] == 'oty']
print(f"B l@LL lines with oty as penultimate: {len(b_oty_l_ll)}/{len(b_l_ll_lines)}")
for fn, ln, wds in b_oty_l_ll:
    section = 'bio(≤84)' if fn <= 84 else ('pharma(85-102)' if fn <= 102 else 'stars(≥103)')
    print(f"  f{fn}.{ln} [{section}]: {' '.join(wds)}")

# Among B oty@penultimate lines, how many end in l?
b_oty_penult = [(fn, ln, wds) for fn, ln, wds in b_lines if len(wds) >= 2 and wds[-2] == 'oty']
b_oty_penult_l = [(fn, ln, wds) for fn, ln, wds in b_oty_penult if get_onset(wds[-1]) == 'l']
print(f"\nB oty@penultimate lines: {len(b_oty_penult)}")
print(f"B oty@penultimate → l@LL: {len(b_oty_penult_l)} ({len(b_oty_penult_l)/len(b_oty_penult) if b_oty_penult else 0:.1%})")

# Base rate: among ALL B lines with ≥2 words, how often does LL have l-onset?
b_all_ll = [wds[-1] for fn, ln, wds in b_lines if wds]
b_l_ll_rate = sum(1 for w in b_all_ll if get_onset(w)=='l') / len(b_all_ll)
print(f"B baseline l@LL rate: {b_l_ll_rate:.3f}")
print(f"[oty][l@LL] enrichment: {len(b_oty_penult_l)/len(b_oty_penult)/b_l_ll_rate:.2f}× (vs base)")

# Stars section specifically
b_stars_oty_penult = [(fn, ln, wds) for fn, ln, wds in b_oty_penult if fn >= 103]
b_stars_oty_penult_l = [(fn, ln, wds) for fn, ln, wds in b_stars_oty_penult if get_onset(wds[-1]) == 'l']
print(f"\nB-stars (f103+) oty@penultimate: {len(b_stars_oty_penult)}")
print(f"B-stars oty@penultimate → l@LL: {len(b_stars_oty_penult_l)}")
for fn, ln, wds in b_stars_oty_penult_l:
    print(f"  f{fn}.{ln}: {' '.join(wds)}")

# ---- cth chain length analysis ----
print("\n" + "="*60)
print("cth CHAIN LENGTH: Longest consecutive cth-word runs")
print("="*60)

all_chains = []
for fn, ln, wds in a_lines:
    current_chain = []
    for i, w in enumerate(wds):
        if get_onset(w) == 'cth':
            current_chain.append((i, w))
        else:
            if len(current_chain) >= 2:
                all_chains.append((fn, ln, current_chain, wds))
            current_chain = []
    if len(current_chain) >= 2:
        all_chains.append((fn, ln, current_chain, wds))

print(f"\nAll A-dialect cth-chains of length ≥2:")
chain_lengths = Counter(len(c) for fn,ln,c,wds in all_chains)
print(f"Length distribution: {dict(sorted(chain_lengths.items()))}")
print(f"\nChains with 3+ consecutive cth-words:")
for fn, ln, c, wds in all_chains:
    if len(c) >= 3:
        chain_str = ' '.join(w for i,w in c)
        positions = [i for i,w in c]
        print(f"  f{fn}.{ln}: positions {positions}: [{chain_str}] in line: {' '.join(wds)}")

# Also longest cth chain in B
all_chains_b = []
for fn, ln, wds in b_lines:
    current_chain = []
    for i, w in enumerate(wds):
        if get_onset(w) == 'cth':
            current_chain.append((i, w))
        else:
            if len(current_chain) >= 2:
                all_chains_b.append((fn, ln, current_chain, wds))
            current_chain = []
    if len(current_chain) >= 2:
        all_chains_b.append((fn, ln, current_chain, wds))

print(f"\nB-dialect cth-chains of length ≥2:")
chain_lengths_b = Counter(len(c) for fn,ln,c,wds in all_chains_b)
print(f"Length distribution: {dict(sorted(chain_lengths_b.items()))}")
for fn, ln, c, wds in all_chains_b:
    chain_str = ' '.join(w for i,w in c)
    print(f"  f{fn}.{ln}: [{chain_str}]")

# ---- cthey→ch cycle ----
print("\n" + "="*60)
print("cthey→ch CYCLE: Does [cthey][ch-word] return to cthey?")
print("="*60)

# B-dialect: all cthey → ch-word bigrams
cthey_ch_b = []
for fn, ln, wds in b_lines:
    for i in range(len(wds)-1):
        if wds[i] == 'cthey' and get_onset(wds[i+1]) == 'ch':
            # Check if ch-word is followed by cthey
            third = wds[i+2] if i+2 < len(wds) else None
            cthey_ch_b.append((fn, ln, wds[i], wds[i+1], third))

print(f"\nB-dialect [cthey][ch-word] bigrams (n={len(cthey_ch_b)}):")
for fn, ln, a, b, third in cthey_ch_b:
    third_s = f"→{third}" if third else "(end)"
    print(f"  f{fn}.{ln}: [{a}][{b}]{third_s}")

# Is [cthey][ch-word][cthey] a trigram?
cthey_ch_cthey = [(fn,ln,a,b,c) for fn,ln,a,b,c in cthey_ch_b if c == 'cthey']
print(f"\n[cthey][ch-word][cthey] trigrams: {len(cthey_ch_cthey)}")
for fn,ln,a,b,c in cthey_ch_cthey:
    print(f"  f{fn}.{ln}: [{a}][{b}][{c}]")

# Broader: cthey appears in lines that also have ch-words
cthey_lines_b = [(fn, ln, wds) for fn, ln, wds in b_lines if 'cthey' in wds]
print(f"\nLines in B with cthey (n={len(cthey_lines_b)}):")
for fn, ln, wds in cthey_lines_b:
    print(f"  f{fn}.{ln}: {' '.join(wds)}")

# ---- Additional: 'r' in B-dialect ----
print("\n" + "="*60)
print("'r' in B-dialect — is it present?")
print("="*60)

r_b_lines = [(fn, ln, wds) for fn, ln, wds in b_lines if any(get_onset(w)=='r' for w in wds)]
print(f"\nB-dialect lines with r-onset words (n={len(r_b_lines)}):")
for fn, ln, wds in r_b_lines[:10]:
    print(f"  f{fn}.{ln}: {' '.join(wds)}")
b_r_words = [w for w in B_words if get_onset(w) == 'r']
print(f"\nB r-onset words: n={len(b_r_words)}, rate={len(b_r_words)/B_total:.4f} vs A rate={A_onset['r']/A_total:.4f}")
print(f"B r-words: {Counter(b_r_words).most_common()}")
