"""
exp_417: B p-formula o-class preference detail (H632)

F409: p→o at pos1=2.24×(N=21); p→o at LL=1.73×(N=25).
What specific o-onset words appear at pos1 and LL in B p-LF lines?
Is the o-class a closed vocabulary (few formula words) or distributed?
Does p→o at pos1 have specific pos2 routing?
"""
from pathlib import Path as _RepositoryPath

import os, re
from collections import Counter, defaultdict

DATA_PATH = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt'))

ONSET_ORDER = [
    ('qok','qok'),('qot','qot'),('qo','qo'),('cth','cth'),
    ('ch','ch'),('sh','sh'),('ok','ok'),('ot','ot'),('ol','ol'),
    ('d','d'),('s','s'),('y','y'),('k','k'),('t','t'),
    ('l','l'),('r','r'),('p','p'),('f','f'),('o','o')
]

def get_onset(word):
    for label, prefix in ONSET_ORDER:
        if word.startswith(prefix):
            return label
    return 'other'

def folio_base(folio):
    return re.sub(r'[rv]\d*$', '', folio)

# Pass 1: folio dialect
folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0})
with open(DATA_PATH, 'r', encoding='utf-8') as fh:
    for line in fh:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
        if not m:
            continue
        folio = m.group(1).lstrip('+*=&~')
        fb = folio_base(folio)
        lc = m.group(3).lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'):
            continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        for w in words:
            folio_word_stats[fb]['total'] += 1
            if w.endswith('edy') or w.endswith('eedy'):
                folio_word_stats[fb]['edy'] += 1

folio_dialect = {}
for fb, stats in folio_word_stats.items():
    t = stats['total']
    folio_dialect[fb] = 'B' if t > 0 and stats['edy'] / t >= 0.05 else 'A'

# Pass 2: collect cont lines
folio_lines = defaultdict(list)
with open(DATA_PATH, 'r', encoding='utf-8') as fh:
    for line in fh:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
        if not m:
            continue
        folio = m.group(1).lstrip('+*=&~')
        ln = int(m.group(2))
        lc = m.group(3).lstrip('+*=/~&')
        fb = folio_base(folio)
        if not lc.lstrip('@').startswith('P'):
            continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if not words:
            continue
        folio_lines[fb].append((ln, words))

cont_lines_b = []
for fb, entries in folio_lines.items():
    dialect = folio_dialect.get(fb, 'A')
    if dialect != 'B':
        continue
    lns = [e[0] for e in entries]
    min_ln, max_ln = min(lns), max(lns)
    for ln, words in entries:
        if ln != min_ln and ln != max_ln:
            cont_lines_b.append(words)

# B p-LF lines
b_p_lines = [words for words in cont_lines_b if len(words) >= 2 and get_onset(words[0]) == 'p']
print(f"B p-LF cont lines: {len(b_p_lines)}")

# p→o at pos1: word tokens
p_o_pos1 = [words for words in b_p_lines if get_onset(words[1]) == 'o']
print(f"\nB p→o at pos1 (N={len(p_o_pos1)}):")
o_pos1_tokens = Counter(words[1] for words in p_o_pos1)
print("  o-class word types at pos1:")
for word, cnt in sorted(o_pos1_tokens.items(), key=lambda x: -x[1]):
    print(f"    '{word}': n={cnt}")

# pos2 distribution after p→o at pos1
print(f"\np→o at pos1 → pos2 distribution (N_len3={sum(1 for w in p_o_pos1 if len(w)>=3)}):")
pos2_p_o = Counter(get_onset(words[2]) for words in p_o_pos1 if len(words) >= 3)
# Baseline: B p-LF pos2 distribution
pos2_p_base = Counter(get_onset(words[2]) for words in b_p_lines if len(words) >= 3)
total_p_p2 = sum(pos2_p_base.values())
total_p_o_p2 = sum(pos2_p_o.values())
for onset, cnt in sorted(pos2_p_o.items(), key=lambda x: -x[1]):
    base = pos2_p_base[onset] / total_p_p2 if total_p_p2 > 0 else 0
    rate = cnt / total_p_o_p2 if total_p_o_p2 > 0 else 0
    E = rate / base if base > 0 else float('inf')
    print(f"  {onset:6s}: n={cnt:3d}  rate={rate:.3f}  base={base:.3f}  E={E:.2f}×")

# p→o at LL: word tokens
p_o_ll = [words for words in b_p_lines if get_onset(words[-1]) == 'o']
print(f"\nB p→o at LL (N={len(p_o_ll)}):")
o_ll_tokens = Counter(words[-1] for words in p_o_ll)
print("  o-class word types at LL:")
for word, cnt in sorted(o_ll_tokens.items(), key=lambda x: -x[1]):
    print(f"    '{word}': n={cnt}")

# Compare o vocabulary at pos1 vs LL vs MID in p-lines
print("\nB p-LF lines: o-class word types across positions:")
o_mid_tokens = Counter()
for words in b_p_lines:
    if len(words) >= 5:
        for w in words[2:-2]:  # MID = idx 2..n-3
            if get_onset(w) == 'o':
                o_mid_tokens[w] += 1

print(f"  pos1 o-types: {len(o_pos1_tokens)} types (N={sum(o_pos1_tokens.values())})")
print(f"  LL o-types: {len(o_ll_tokens)} types (N={sum(o_ll_tokens.values())})")
print(f"  MID o-types: {len(o_mid_tokens)} types (N={sum(o_mid_tokens.values())})")
print(f"\n  Top MID o-class words in p-lines:")
for word, cnt in sorted(o_mid_tokens.items(), key=lambda x: -x[1])[:10]:
    print(f"    '{word}': n={cnt}")

# Check if pos1 o vocabulary overlaps with LL o vocabulary
pos1_set = set(o_pos1_tokens.keys())
ll_set = set(o_ll_tokens.keys())
mid_set = set(o_mid_tokens.keys())
print(f"\n  pos1 ∩ LL: {sorted(pos1_set & ll_set)}")
print(f"  pos1 ∩ MID: {len(pos1_set & mid_set)} types")
print(f"  LL ∩ MID: {len(ll_set & mid_set)} types")
print(f"  All three: {sorted(pos1_set & ll_set & mid_set)}")

# Full p→o lines at pos1 (show full sequences)
print(f"\nAll p→o pos1 lines:")
for words in p_o_pos1:
    onsets = [get_onset(w) for w in words]
    print(f"  {words} → {onsets}")

print("\n=== Done ===")
