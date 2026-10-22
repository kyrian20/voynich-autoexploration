"""
exp_387: A-Dialect r-Onset Positional Census (H601)

Tests whether A-dialect r is approximately LL-exclusive.
Counts r-onset tokens at each position (LF, pos1, MID_inner, pre_LL, LL).
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
    return re.sub(r'[rv]$', '', folio)

# Pass 1: dialect classification
folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
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
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        for w in words:
            folio_word_stats[fb]['total'] += 1
            if w.endswith('eedy'):
                folio_word_stats[fb]['eedy'] += 1
            elif w.endswith('edy'):
                folio_word_stats[fb]['edy'] += 1

def classify_dialect(stats):
    total = stats['total']
    if total == 0:
        return 'unknown'
    return 'B' if (stats['edy'] + stats['eedy']) / total >= 0.05 else 'A'

folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}

# Pass 2: collect all lines
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
        line_num = int(m.group(2))
        locus_code = m.group(3)
        fb = folio_base(folio)
        dialect = folio_dialect.get(fb, 'unknown')
        if dialect not in ('A', 'B'):
            continue
        lc = locus_code.lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'):
            continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if len(words) < 1:
            continue
        folio_lines[fb].append((line_num, words, dialect))

def pos_category(idx, n):
    if idx == 0:
        return "LF"
    if idx == 1:
        return "pos1"
    if idx == n - 1:
        return "LL"
    if n >= 4 and idx == n - 2:
        return "pre_LL"
    return "MID_inner"

# Collect r-onset positions for A dialect (all lines: opener, continuation, closer)
# Also collect baseline for normalization

for include_all_lines in [False, True]:
    scope = "ALL LINES" if include_all_lines else "CONTINUATION LINES ONLY"
    print(f"\n{'='*70}")
    print(f"A-DIALECT r-ONSET POSITIONAL CENSUS — {scope}")
    print(f"{'='*70}")

    pos_counts = Counter()  # r onset by position
    total_pos_counts = Counter()  # all words by position

    r_tokens = []  # (word, position_label, folio, line_num)

    for fb, lines_list in folio_lines.items():
        if not lines_list:
            continue
        dialect = lines_list[0][2]
        if dialect != 'A':
            continue

        line_nums = [ln for ln, _, _ in lines_list]
        min_ln, max_ln = min(line_nums), max(line_nums)

        for ln, words, d in lines_list:
            is_continuation = (ln != min_ln and ln != max_ln)
            if not include_all_lines and not is_continuation:
                continue

            n = len(words)
            for idx, w in enumerate(words):
                pos = pos_category(idx, n)
                total_pos_counts[pos] += 1
                if get_onset(w) == 'r':
                    pos_counts[pos] += 1
                    r_tokens.append((w, pos, fb, ln))

    total_r = sum(pos_counts.values())
    total_words = sum(total_pos_counts.values())
    print(f"\nTotal A r-onset tokens: {total_r}")
    print(f"Total A words in scope: {total_words}")
    print(f"Overall r rate: {total_r/total_words*100:.3f}%\n")

    POSITIONS = ['LF', 'pos1', 'MID_inner', 'pre_LL', 'LL']
    print(f"{'Position':<12} {'r_count':>8} {'pos_total':>10} {'r_rate%':>8} {'baseline_r%':>12} {'E':>6}")
    print("-" * 60)
    overall_r_rate = total_r / total_words if total_words > 0 else 0
    for pos in POSITIONS:
        r_n = pos_counts.get(pos, 0)
        pos_n = total_pos_counts.get(pos, 0)
        if pos_n == 0:
            print(f"{pos:<12} {'---':>8} {'---':>10}")
            continue
        r_rate = r_n / pos_n
        e = r_rate / overall_r_rate if overall_r_rate > 0 else float('nan')
        print(f"{pos:<12} {r_n:>8} {pos_n:>10} {r_rate*100:>8.3f}% {overall_r_rate*100:>11.3f}% {e:>6.2f}×")

    print(f"\nAll A r-onset words (continuation lines):")
    if not include_all_lines:
        cont_r = [(w, pos) for w, pos, fb, ln in r_tokens]
        r_word_counts = Counter(w for w, pos in cont_r)
        for word, count in sorted(r_word_counts.items(), key=lambda x: -x[1]):
            positions_of_word = [pos for w, pos in cont_r if w == word]
            pos_summary = Counter(positions_of_word)
            print(f"  {word}: {count} total — {dict(pos_summary)}")

    # Only print position-sorted list for continuation
    if not include_all_lines:
        print(f"\nA r-onset by position (cont lines):")
        for pos in POSITIONS:
            examples = [(w, fb) for w, p, fb, ln in r_tokens if p == pos]
            if examples:
                example_words = Counter(w for w, fb in examples)
                print(f"  {pos} (N={pos_counts.get(pos,0)}): {dict(example_words.most_common(5))}")

