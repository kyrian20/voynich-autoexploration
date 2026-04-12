"""
exp_363: Folio-Opener Two-Word Formula (H565)
What are the specific word pairs at folio-opener LF+pos1 in both dialects?
This completes the three-register grammar characterization.
"""

import os, re
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser('~/voynich-cryptanalyst')
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

def folio_base(folio):
    return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    return 'B' if (stats['edy'] + stats['eedy']) / total >= 0.05 else 'A'

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

# Pass 1: classify folios
folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
with open(DATA_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'): continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
        if not m: continue
        folio = m.group(1).lstrip('+*=&~')
        fb = folio_base(folio)
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        for w in words:
            folio_word_stats[fb]['total'] += 1
            if w.endswith('eedy'): folio_word_stats[fb]['eedy'] += 1
            elif w.endswith('edy'): folio_word_stats[fb]['edy'] += 1

folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}

# Pass 2: collect opener/closer lines
folio_lines = defaultdict(list)
with open(DATA_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'): continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
        if not m: continue
        folio = m.group(1).lstrip('+*=&~')
        line_num = int(m.group(2))
        locus_code = m.group(3)
        fb = folio_base(folio)
        dialect = folio_dialect.get(fb, 'unknown')
        if dialect not in ('A', 'B'): continue
        lc = locus_code.lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'): continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if len(words) < 2: continue
        folio_lines[fb].append((line_num, words, dialect))

# Extract opener and closer lines
opener_lines = defaultdict(list)  # dialect -> list of word lists
closer_lines = defaultdict(list)
for fb, lines_list in folio_lines.items():
    if not lines_list: continue
    dialect = lines_list[0][2]
    line_nums = [ln for ln, _, _ in lines_list]
    min_ln = min(line_nums)
    max_ln = max(line_nums)
    for ln, words, d in lines_list:
        if ln == min_ln:
            opener_lines[dialect].append(words)
        elif ln == max_ln:
            closer_lines[dialect].append(words)

print("=" * 70)
print("FOLIO-OPENER AND FOLIO-CLOSER WORD FORMULAS (H565)")
print("=" * 70)

for dialect in ['A', 'B']:
    print(f"\n{'='*70}")
    print(f"{dialect}-DIALECT")
    print(f"{'='*70}")

    openers = opener_lines[dialect]
    closers = closer_lines[dialect]
    print(f"Folio-opener lines: N={len(openers)}")
    print(f"Folio-closer lines: N={len(closers)}")

    # Opener: LF word frequencies and LF+pos1 pairs
    print(f"\n--- Folio-opener LF word frequencies ---")
    opener_lf = Counter(w[0] for w in openers)
    opener_pos1 = Counter(w[1] for w in openers if len(w) >= 2)
    opener_pairs = Counter((w[0], w[1]) for w in openers if len(w) >= 2)

    total_opener = len(openers)
    print(f"{'Word':<18} {'Count':>6} {'%':>6} {'onset':>8}")
    for word, cnt in opener_lf.most_common(20):
        pct = 100*cnt/total_opener
        onset = get_onset(word)
        print(f"  {word:<18} {cnt:>6} {pct:>5.1f}%  {onset}")

    print(f"\n--- Folio-opener pos1 word frequencies ---")
    for word, cnt in opener_pos1.most_common(15):
        pct = 100*cnt/total_opener
        onset = get_onset(word)
        print(f"  {word:<18} {cnt:>6} {pct:>5.1f}%  {onset}")

    print(f"\n--- Folio-opener TOP LF+pos1 PAIRS ---")
    pair_total = sum(opener_pairs.values())
    print(f"Total LF+pos1 pairs: {pair_total}")
    for (lf, p1), cnt in opener_pairs.most_common(20):
        lf_onset = get_onset(lf)
        p1_onset = get_onset(p1)
        print(f"  {lf:<15} + {p1:<15}: N={cnt}  [{lf_onset}→{p1_onset}]")

    # Opener hapax rate for LF words
    lf_hapax = sum(1 for w,cnt in opener_lf.items() if cnt == 1)
    print(f"\nOpener LF hapax rate: {lf_hapax}/{len(opener_lf)} types = {100*lf_hapax/max(len(opener_lf),1):.0f}% types ({100*lf_hapax/max(total_opener,1):.0f}% tokens)")

    # Now closer: LF word frequencies and LF+pos1 pairs
    print(f"\n--- Folio-closer LF word frequencies ---")
    closer_lf = Counter(w[0] for w in closers)
    closer_pos1 = Counter(w[1] for w in closers if len(w) >= 2)
    closer_ll = Counter(w[-1] for w in closers)
    closer_pairs = Counter((w[0], w[1]) for w in closers if len(w) >= 2)

    total_closer = len(closers)
    print(f"{'Word':<18} {'Count':>6} {'%':>6} {'onset':>8}")
    for word, cnt in closer_lf.most_common(15):
        pct = 100*cnt/total_closer
        onset = get_onset(word)
        print(f"  {word:<18} {cnt:>6} {pct:>5.1f}%  {onset}")

    print(f"\n--- Folio-closer pos1 word frequencies ---")
    for word, cnt in closer_pos1.most_common(10):
        pct = 100*cnt/total_closer
        onset = get_onset(word)
        print(f"  {word:<18} {cnt:>6} {pct:>5.1f}%  {onset}")

    print(f"\n--- Folio-closer LL word frequencies ---")
    for word, cnt in closer_ll.most_common(10):
        pct = 100*cnt/total_closer
        onset = get_onset(word)
        print(f"  {word:<18} {cnt:>6} {pct:>5.1f}%  {onset}")

    print(f"\n--- Folio-closer TOP LF+pos1 PAIRS ---")
    for (lf, p1), cnt in closer_pairs.most_common(15):
        lf_onset = get_onset(lf)
        p1_onset = get_onset(p1)
        print(f"  {lf:<15} + {p1:<15}: N={cnt}  [{lf_onset}→{p1_onset}]")

    # Line length distribution for opener/closer
    print(f"\n--- Line length distribution ---")
    opener_lens = [len(w) for w in openers]
    closer_lens = [len(w) for w in closers]
    from collections import Counter as Ctr
    olen = Counter(opener_lens)
    clen = Counter(closer_lens)
    print(f"Opener: mean={sum(opener_lens)/max(len(opener_lens),1):.1f} words")
    print(f"  length dist: {sorted(olen.items())}")
    print(f"Closer: mean={sum(closer_lens)/max(len(closer_lens),1):.1f} words")
    print(f"  length dist: {sorted(clen.items())}")

