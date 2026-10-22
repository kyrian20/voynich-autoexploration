"""
exp_053: Currier A Line Structure — Full Positional Analysis
F057 showed: 'd'-stem words are line-final markers; -ol/-or words avoid line endings.
Hypothesis: -ol/-or words are LINE-INITIAL markers in Currier A.
If the full positional structure maps out as:
  [line-initial: chol/shol/chor/shor] → [medial: free] → [line-final: dy/dal/daiin]
Then Currier A has a rigid slot-based line grammar.

Also test Currier B line structure for comparison.
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

SUFFIX_LIST = ['aiin', 'ain', 'eedy', 'edy', 'chy', 'eey', 'dy', 'ey', 'y', 'ol', 'or', 'al', 'ar', 'iin', 'in']

def is_body_locus(locus_code):
    base = locus_code.lstrip('+*@=/~&')
    return base.startswith('P')

def clean_text(text):
    return re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)

def suffix_group(word):
    for suf in SUFFIX_LIST:
        if word.endswith(suf) and len(word) > len(suf):
            return suf
    return None

def parse_lines(path):
    """Parse all body text lines, tracking position within each line."""
    lines_a = []  # each item = list of words in a Currier A body line
    lines_b = []
    current_currier = None

    with open(path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue

            m_c = re.search(r'\$L=([AB])', line)
            if m_c:
                current_currier = m_c.group(1)

            m = re.match(r'^<([^>]+)>', line)
            if not m:
                continue
            locus_raw = m.group(1)
            parts = locus_raw.split(',')
            if len(parts) < 2:
                continue
            locus_code = parts[1].strip()

            if not is_body_locus(locus_code):
                continue

            text = line[m.end():].strip()
            text = clean_text(text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]

            if not tokens:
                continue

            if current_currier == 'A':
                lines_a.append(tokens)
            elif current_currier == 'B':
                lines_b.append(tokens)

    return lines_a, lines_b

def positional_rates(lines, words_of_interest):
    """
    For a set of target words, compute:
    - rate at position 0 (first word in line)
    - rate at position -1 (last word in line)
    - rate at other positions (medial)

    Returns: dict with word -> (n, frac_first, frac_last, frac_medial)
    """
    counts = {w: [0, 0, 0, 0] for w in words_of_interest}  # total, first, last, medial
    total_first = 0
    total_last = 0
    total_medial = 0

    for line in lines:
        n = len(line)
        if n == 0:
            continue
        total_first += 1
        total_last += 1
        total_medial += max(0, n - 2)

        for i, w in enumerate(line):
            if w in counts:
                counts[w][0] += 1  # total
                if i == 0:
                    counts[w][1] += 1  # first
                elif i == n - 1:
                    counts[w][2] += 1  # last
                else:
                    counts[w][3] += 1  # medial

    baseline_first = total_first / max(1, sum(len(l) for l in lines))
    baseline_last = total_last / max(1, sum(len(l) for l in lines))

    result = {}
    for w, (total, first, last, medial) in counts.items():
        if total == 0:
            continue
        result[w] = {
            'n': total,
            'frac_first': first / total,
            'frac_last': last / total,
            'frac_medial': medial / total,
            'baseline_first': baseline_first,
            'baseline_last': baseline_last,
        }
    return result

def suffix_positional_profile(lines, suffix):
    """Compute positional distribution for all words with a given suffix."""
    first_count = 0
    last_count = 0
    medial_count = 0
    total = 0
    total_first_slots = 0
    total_last_slots = 0

    for line in lines:
        n = len(line)
        if n == 0:
            continue
        total_first_slots += 1
        total_last_slots += 1
        for i, w in enumerate(line):
            if w.endswith(suffix) and (suffix == '' or len(w) > len(suffix)):
                total += 1
                if i == 0:
                    first_count += 1
                elif i == n - 1:
                    last_count += 1
                else:
                    medial_count += 1

    if total == 0:
        return None

    return {
        'n': total,
        'frac_first': first_count / total,
        'frac_last': last_count / total,
        'frac_medial': medial_count / total,
        'rate_first': first_count / max(1, total_first_slots),
        'rate_last': last_count / max(1, total_last_slots),
    }

def main():
    lines_a, lines_b = parse_lines(DATA_PATH)
    print(f"Currier A lines: {len(lines_a)}, Currier B lines: {len(lines_b)}")

    n_tokens_a = sum(len(l) for l in lines_a)
    n_tokens_b = sum(len(l) for l in lines_b)
    baseline_first_a = len(lines_a) / n_tokens_a
    baseline_last_a = len(lines_a) / n_tokens_a
    print(f"A baseline rate per position: {100*baseline_first_a:.1f}% (each of first/last slots = 1/{100/baseline_first_a:.0f} tokens)")

    # === 1. Full suffix-level positional profiles in Currier A ===
    print(f"\n{'='*70}")
    print("CURRIER A: SUFFIX POSITIONAL PROFILES")
    print(f"{'='*70}")
    print(f"{'Suffix':<10} {'N':>7} {'First%':>8} {'Last%':>8} {'Medial%':>8} {'First/base':>11} {'Last/base':>10}")

    suffixes_to_test = ['y', 'dy', 'ey', 'ol', 'or', 'al', 'ar', 'aiin', 'ain', 'chy', 'eey', 'edy', 'eedy', 'in', 'iin']
    for suf in sorted(suffixes_to_test):
        res = suffix_positional_profile(lines_a, suf)
        if res and res['n'] > 20:
            ratio_first = res['frac_first'] / baseline_first_a if baseline_first_a > 0 else 0
            ratio_last = res['frac_last'] / baseline_last_a if baseline_last_a > 0 else 0
            flag_f = "***" if ratio_first > 2.0 else ("**" if ratio_first > 1.5 else ("*" if ratio_first > 1.2 else ""))
            flag_l = "***" if ratio_last > 2.0 else ("**" if ratio_last > 1.5 else ("*" if ratio_last > 1.2 else ""))
            print(f"-{suf:<9} {res['n']:>7} {100*res['frac_first']:>7.1f}% {100*res['frac_last']:>7.1f}% {100*res['frac_medial']:>7.1f}% {ratio_first:>9.2f}{flag_f} {ratio_last:>8.2f}{flag_l}")

    # === 2. Full suffix-level positional profiles in Currier B ===
    print(f"\n{'='*70}")
    print("CURRIER B: SUFFIX POSITIONAL PROFILES")
    print(f"{'='*70}")
    baseline_b = len(lines_b) / max(1, n_tokens_b)
    print(f"B baseline: {100*baseline_b:.1f}%")
    print(f"{'Suffix':<10} {'N':>7} {'First%':>8} {'Last%':>8} {'Medial%':>8} {'First/base':>11} {'Last/base':>10}")

    for suf in sorted(suffixes_to_test):
        res = suffix_positional_profile(lines_b, suf)
        if res and res['n'] > 20:
            ratio_first = res['frac_first'] / baseline_b if baseline_b > 0 else 0
            ratio_last = res['frac_last'] / baseline_b if baseline_b > 0 else 0
            flag_f = "***" if ratio_first > 2.0 else ("**" if ratio_first > 1.5 else ("*" if ratio_first > 1.2 else ""))
            flag_l = "***" if ratio_last > 2.0 else ("**" if ratio_last > 1.5 else ("*" if ratio_last > 1.2 else ""))
            print(f"-{suf:<9} {res['n']:>7} {100*res['frac_first']:>7.1f}% {100*res['frac_last']:>7.1f}% {100*res['frac_medial']:>7.1f}% {ratio_first:>9.2f}{flag_f} {ratio_last:>8.2f}{flag_l}")

    # === 3. Word-level positional profiles for key Currier A words ===
    key_words_a = ['chol', 'shol', 'chor', 'shor', 'ol', 'or', 'cthol', 'cthor',
                   'daiin', 'dy', 'dal', 'dam', 'dar', 'dain', 'dol', 'dy',
                   'cthy', 'aiin', 'or', 'ar']
    stats = positional_rates(lines_a, key_words_a)

    print(f"\n{'='*70}")
    print("CURRIER A: KEY WORD POSITIONAL PROFILES")
    print(f"{'='*70}")
    print(f"{'Word':<12} {'N':>5} {'First%':>8} {'Last%':>8} {'Medial%':>8} {'First/base':>11} {'Last/base':>10}")
    for w in sorted(stats.keys(), key=lambda x: -stats[x]['frac_first']):
        r = stats[w]
        if r['n'] < 5:
            continue
        rf = r['frac_first'] / r['baseline_first']
        rl = r['frac_last'] / r['baseline_last']
        flag_f = "***" if rf > 2.5 else ("**" if rf > 2.0 else ("*" if rf > 1.5 else ""))
        flag_l = "***" if rl > 2.5 else ("**" if rl > 2.0 else ("*" if rl > 1.5 else ""))
        print(f"{w:<12} {r['n']:>5} {100*r['frac_first']:>7.1f}% {100*r['frac_last']:>7.1f}% {100*r['frac_medial']:>7.1f}% {rf:>9.2f}{flag_f} {rl:>8.2f}{flag_l}")

    # === 4. Mutual information: line position and word identity ===
    # For each of (first, last) slot: what are the most over/under-represented words?
    print(f"\n{'='*70}")
    print("CURRIER A: MOST OVER-REPRESENTED WORDS AT LINE-INITIAL POSITION")
    print(f"{'='*70}")
    all_a_words = Counter(w for line in lines_a for w in line)
    first_words = Counter(line[0] for line in lines_a if line)
    last_words = Counter(line[-1] for line in lines_a if line)
    n_lines = len(lines_a)
    n_total = sum(all_a_words.values())

    # Over-representation = P(word | first) / P(word | any)
    overrep_first = []
    for w, fc in first_words.most_common(50):
        p_first = fc / n_lines
        p_any = all_a_words.get(w, 0) / n_total
        if p_any > 0:
            overrep_first.append((w, fc, p_first, p_any, p_first/p_any))
    overrep_first.sort(key=lambda x: -x[4])

    print(f"{'Word':<12} {'First-count':>12} {'P(word|first)':>14} {'P(word)':>9} {'Ratio':>7}")
    for w, fc, pf, pa, ratio in overrep_first[:15]:
        print(f"{w:<12} {fc:>12} {100*pf:>13.1f}% {100*pa:>8.2f}% {ratio:>6.2f}×")

    print(f"\n{'='*70}")
    print("CURRIER A: MOST OVER-REPRESENTED WORDS AT LINE-FINAL POSITION")
    print(f"{'='*70}")
    overrep_last = []
    for w, lc in last_words.most_common(50):
        p_last = lc / n_lines
        p_any = all_a_words.get(w, 0) / n_total
        if p_any > 0:
            overrep_last.append((w, lc, p_last, p_any, p_last/p_any))
    overrep_last.sort(key=lambda x: -x[4])

    print(f"{'Word':<12} {'Last-count':>11} {'P(word|last)':>13} {'P(word)':>9} {'Ratio':>7}")
    for w, lc, pl, pa, ratio in overrep_last[:15]:
        print(f"{w:<12} {lc:>11} {100*pl:>12.1f}% {100*pa:>8.2f}% {ratio:>6.2f}×")

    # === 5. Consecutive pair structure: what follows line-initial words? ===
    print(f"\n{'='*70}")
    print("CURRIER A: WHAT FOLLOWS LINE-INITIAL -ol/-or WORDS?")
    print(f"{'='*70}")
    ol_or_initial_lines = [l for l in lines_a if l and (l[0].endswith('ol') or l[0].endswith('or'))]
    print(f"Lines starting with -ol/-or words: {len(ol_or_initial_lines)}/{len(lines_a)} ({100*len(ol_or_initial_lines)/max(1,len(lines_a)):.1f}%)")
    if ol_or_initial_lines:
        second_words = Counter(l[1] for l in ol_or_initial_lines if len(l) >= 2)
        print("Top second words after -ol/-or line-starters:")
        for w, c in second_words.most_common(10):
            print(f"  {w}: {c}")

    # What precedes line-final -d/-dy words?
    print(f"\nWhat precedes line-final -dy/-dal/-dam words?")
    d_final_lines = [l for l in lines_a if l and (l[-1].endswith('dy') or l[-1] in ('dal', 'dam', 'dar'))]
    print(f"Lines ending with -dy/dal/dam words: {len(d_final_lines)}/{len(lines_a)} ({100*len(d_final_lines)/max(1,len(lines_a)):.1f}%)")
    if d_final_lines:
        prev_words = Counter(l[-2] for l in d_final_lines if len(l) >= 2)
        print("Top penultimate words before -dy/dal/dam finals:")
        for w, c in prev_words.most_common(10):
            print(f"  {w}: {c}")

if __name__ == '__main__':
    main()
