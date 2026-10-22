"""
exp_414: Bracket Line Content Analysis (H625, H633, H635)

Extract and analyze the actual word sequences in:
1. A p sh-bracket lines (H625): A cont lines with p at LF AND sh at pos1 AND sh at LL
2. A d sh-bracket lines (H633): A cont lines with d at LF AND sh at pos1 AND sh at LL
3. B s qok-bracket lines (H635): B cont lines with s at LF AND qok at pos1 AND qok at LL

For each set: print full word sequences, onset sequences, line lengths,
and MID onset composition.
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

# Pass 2: collect lines with folio IDs
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
        folio_lines[fb].append((ln, folio, words))

# Separate cont lines by dialect
a_cont = []
b_cont = []
for fb, entries in folio_lines.items():
    dialect = folio_dialect.get(fb, 'A')
    lns = [e[0] for e in entries]
    min_ln, max_ln = min(lns), max(lns)
    for ln, folio, words in entries:
        if ln != min_ln and ln != max_ln and len(words) >= 4:
            if dialect == 'A':
                a_cont.append((folio, ln, words))
            else:
                b_cont.append((folio, ln, words))

def analyze_bracket_lines(lines, lf_class, frame_onset, label):
    """Find and analyze lines with lf_class at LF AND frame_onset at pos1 AND LL."""
    bracket_lines = []
    for folio, ln, words in lines:
        onsets = [get_onset(w) for w in words]
        if onsets[0] == lf_class and onsets[1] == frame_onset and onsets[-1] == frame_onset:
            bracket_lines.append((folio, ln, words, onsets))

    print(f"\n=== {label}: LF={lf_class}, pos1=LL={frame_onset} (N={len(bracket_lines)}) ===")
    for folio, ln, words, onsets in bracket_lines:
        n = len(words)
        mid_onsets = onsets[2:-1] if n >= 4 else []
        print(f"  [{folio}/line{ln}] (len={n})")
        print(f"    Words: {' '.join(words)}")
        print(f"    Onsets: {' '.join(onsets)}")
        if mid_onsets:
            print(f"    MID onsets: {mid_onsets}")

    if not bracket_lines:
        print("  No lines found.")
        return

    # MID onset composition (positions 2..n-2)
    all_mid_onsets = []
    for folio, ln, words, onsets in bracket_lines:
        all_mid_onsets.extend(onsets[2:-1])
    if all_mid_onsets:
        mid_counter = Counter(all_mid_onsets)
        total_mid = len(all_mid_onsets)
        print(f"\n  MID onset distribution (N_mid={total_mid}):")
        for onset, cnt in mid_counter.most_common(8):
            print(f"    {onset}: n={cnt} ({cnt/total_mid:.1%})")

# Analyze the three bracket sets
analyze_bracket_lines(a_cont, 'p', 'sh', 'A p sh-bracket')
analyze_bracket_lines(a_cont, 'd', 'sh', 'A d sh-bracket')
analyze_bracket_lines(b_cont, 's', 'qok', 'B s qok-bracket')

# Additional: B s-LF lines where pos1=sh AND LL=qok (cross-class bracket check)
print("\n=== B s-LF lines: pos1=sh, LL=qok (cross-class, N?) ===")
for folio, ln, words in b_cont:
    onsets = [get_onset(w) for w in words]
    if onsets[0] == 's' and onsets[1] == 'sh' and onsets[-1] == 'qok':
        print(f"  [{folio}/line{ln}]: {' '.join(words)}")
        print(f"    Onsets: {' '.join(onsets)}")

print("\n=== Done ===")
