"""
exp_092: y+ch vs d+ch Contextual Differentiation in A Dialect (H161, H162, H163)

H161: y+ch and d+ch are NOT interchangeable — they have different contextual environments:
      (1) Different para-start rates
      (2) Different following-word distributions
      (3) Different section/folio distributions

H162: sh-stem positional paradigm in A — does bare sh / d+sh / y+sh follow same 3-tier pattern?
      If yes: the prefix-encoded positional grammar is a UNIVERSAL Voynichese feature.

H163: A inter-line continuation — do y+ch and d+ch openers appear at different rates
      depending on the PRECEDING line's closing word onset?
"""

import re
import os
from collections import defaultdict, Counter

DATA_PATH = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'


def folio_base(folio):
    """Strip .N suffix: f1r.1 -> f1r"""
    return re.sub(r'\.\d+$', '', folio)


def classify_dialect(folio_stats):
    """edy/eedy rate >= 5% -> B, else A"""
    total = folio_stats.get('total', 0)
    if total == 0:
        return 'unknown'
    rate = (folio_stats.get('edy', 0) + folio_stats.get('eedy', 0)) / total
    return 'B' if rate >= 0.05 else 'A'


def is_y_compound(word):
    if not word.startswith('y') or len(word) < 4:
        return False
    rest = word[1:]
    return rest[0] in ('c', 's', 'k', 't') and len(rest) >= 2


def is_y_ch_compound(word):
    return word.startswith('ych') and len(word) >= 4


def is_d_ch_compound(word):
    return word.startswith('dch') and len(word) >= 4


def is_y_sh_compound(word):
    return word.startswith('ysh') and len(word) >= 4


def is_d_sh_compound(word):
    return word.startswith('dsh') and len(word) >= 4


def get_onset(word):
    for prefix in ['qo', 'ch', 'sh']:
        if word.startswith(prefix):
            return prefix
    if word[0] in 'ptk':
        return word[0]
    if word[0] in 'dsyo':
        return word[0]
    return 'other'


def parse_voynich():
    """Parse EVA ZL3b transcription into line records."""
    # First pass: compute folio-level edy/eedy stats for dialect assignment
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m:
                continue
            folio_raw, _, _ = m.group(1), m.group(2), m.group(3)
            folio = folio_raw.lstrip('+*=&~')
            fb = folio_base(folio)
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            for w in words:
                folio_word_stats[fb]['total'] += 1
                if w.endswith('eedy'):
                    folio_word_stats[fb]['eedy'] += 1
                elif w.endswith('edy'):
                    folio_word_stats[fb]['edy'] += 1

    folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}

    # Second pass: parse line records
    records = []

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m:
                continue
            folio_raw = m.group(1)
            locus_code = m.group(3)

            folio = folio_raw.lstrip('+*=&~')
            fb = folio_base(folio)
            dialect = folio_dialect.get(fb, 'unknown')

            lc_stripped = locus_code.lstrip('+*=/~&')
            is_para_start = lc_stripped.startswith('@')
            is_body = lc_stripped.lstrip('@').startswith('P')

            if not is_body:
                continue

            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]

            if not words:
                continue

            records.append({
                'folio': fb,
                'dialect': dialect,
                'is_para_start': is_para_start,
                'words': words,
                'n_words': len(words),
                'first_word': words[0],
                'last_word': words[-1],
                'first_onset': get_onset(words[0]),
            })

    return records


def h161_y_ch_vs_d_ch_context(records):
    """H161: y+ch and d+ch have different contextual environments in A."""
    print("=" * 70)
    print("H161: y+ch vs d+ch Contextual Differentiation (A Dialect)")
    print("=" * 70)

    a_records = [r for r in records if r['dialect'] == 'A']

    # Para-start rates
    y_ch_lines = [r for r in a_records if is_y_ch_compound(r['first_word'])]
    d_ch_lines = [r for r in a_records if is_d_ch_compound(r['first_word'])]
    all_a_lines = a_records

    base_ps_rate = sum(1 for r in all_a_lines if r['is_para_start']) / len(all_a_lines) if all_a_lines else 0
    y_ch_ps_rate = sum(1 for r in y_ch_lines if r['is_para_start']) / len(y_ch_lines) if y_ch_lines else 0
    d_ch_ps_rate = sum(1 for r in d_ch_lines if r['is_para_start']) / len(d_ch_lines) if d_ch_lines else 0

    print(f"\nTotal A lines: {len(all_a_lines)}")
    print(f"Lines opening with y+ch: {len(y_ch_lines)}")
    print(f"Lines opening with d+ch: {len(d_ch_lines)}")
    print(f"\n--- Para-Start Rate Comparison ---")
    print(f"{'Type':<20} {'n_lines':<10} {'PS_rate':<12} {'Enrichment':<12}")
    print(f"{'Background':<20} {len(all_a_lines):<10} {base_ps_rate:.3f}        1.00×")
    print(f"{'y+ch openers':<20} {len(y_ch_lines):<10} {y_ch_ps_rate:.3f}        {y_ch_ps_rate/base_ps_rate:.2f}×")
    print(f"{'d+ch openers':<20} {len(d_ch_lines):<10} {d_ch_ps_rate:.3f}        {d_ch_ps_rate/base_ps_rate:.2f}×")

    # Following word distribution (pos1 onset)
    print(f"\n--- Following Word (pos1) Onset Distribution ---")
    y_ch_following = Counter()
    d_ch_following = Counter()

    for r in y_ch_lines:
        if len(r['words']) >= 2:
            y_ch_following[get_onset(r['words'][1])] += 1
    for r in d_ch_lines:
        if len(r['words']) >= 2:
            d_ch_following[get_onset(r['words'][1])] += 1

    y_total = sum(y_ch_following.values())
    d_total = sum(d_ch_following.values())

    all_onsets = sorted(set(list(y_ch_following.keys()) + list(d_ch_following.keys())))
    print(f"{'Onset':<10} {'y+ch %':<12} {'d+ch %':<12} {'Ratio (y/d)':<12}")
    for onset in sorted(all_onsets, key=lambda x: -(y_ch_following.get(x,0)/y_total if y_total else 0)):
        yp = y_ch_following.get(onset, 0) / y_total if y_total else 0
        dp = d_ch_following.get(onset, 0) / d_total if d_total else 0
        ratio = yp/dp if dp > 0 else float('inf')
        print(f"  {onset:<8} {yp*100:>6.1f}%    {dp*100:>6.1f}%    {ratio:.2f}×")

    # Top following words
    print(f"\n--- Top Following Words ---")
    y_following_words = Counter()
    d_following_words = Counter()
    for r in y_ch_lines:
        if len(r['words']) >= 2:
            y_following_words[r['words'][1]] += 1
    for r in d_ch_lines:
        if len(r['words']) >= 2:
            d_following_words[r['words'][1]] += 1

    print(f"After y+ch:  {y_following_words.most_common(8)}")
    print(f"After d+ch:  {d_following_words.most_common(8)}")

    # Stem identity overlap
    print(f"\n--- Shared Stem Analysis (ch-stem) ---")
    y_stems = Counter()
    d_stems = Counter()
    for r in y_ch_lines:
        w = r['first_word']
        if w.startswith('ych'):
            y_stems[w[1:]] += 1  # strip y- to get ch-stem
    for r in d_ch_lines:
        w = r['first_word']
        if w.startswith('dch'):
            d_stems[w[1:]] += 1  # strip d- to get ch-stem

    print(f"Top y+ch opener stems (ch-form): {y_stems.most_common(8)}")
    print(f"Top d+ch opener stems (ch-form): {d_stems.most_common(8)}")

    shared_stems = set(y_stems.keys()) & set(d_stems.keys())
    print(f"Shared stems (appear in both): {len(shared_stems)}")
    print(f"Shared stems: {sorted(shared_stems)}")

    # Are they interchangeable per paragraph?
    # Check if same paragraph has both y+ch and d+ch openers
    print(f"\n--- Co-occurrence within Paragraphs ---")
    # Track by (folio, para_index)
    para_opener_types = defaultdict(set)
    para_idx = 0
    prev_para_start = True
    for r in a_records:
        if r['is_para_start']:
            para_idx += 1
        key = (r['folio'], para_idx)
        if is_y_ch_compound(r['first_word']):
            para_opener_types[key].add('y_ch')
        if is_d_ch_compound(r['first_word']):
            para_opener_types[key].add('d_ch')

    paras_y_only = sum(1 for v in para_opener_types.values() if v == {'y_ch'})
    paras_d_only = sum(1 for v in para_opener_types.values() if v == {'d_ch'})
    paras_both = sum(1 for v in para_opener_types.values() if 'y_ch' in v and 'd_ch' in v)
    paras_with_opener = sum(1 for v in para_opener_types.values() if v)

    print(f"Paras with y+ch only: {paras_y_only}")
    print(f"Paras with d+ch only: {paras_d_only}")
    print(f"Paras with BOTH y+ch and d+ch: {paras_both}")
    print(f"Total paras with at least one: {paras_with_opener}")

    return y_ch_ps_rate, d_ch_ps_rate, base_ps_rate


def h162_sh_stem_paradigm(records):
    """H162: sh-stem positional paradigm in A — does bare sh / d+sh / y+sh follow 3-tier pattern?"""
    print("\n" + "=" * 70)
    print("H162: sh-Stem Positional Paradigm in A Dialect")
    print("=" * 70)

    a_records = [r for r in records if r['dialect'] == 'A']
    total_a = len(a_records)
    background_lfirst = sum(1 for r in a_records if r['first_word'] == r['words'][0] and
                            r.get('is_line_first_pos', True)) / total_a if total_a else 0

    # Count by position (which line position the word appears at)
    # For each word in each line, track position
    bare_sh_lfirst = 0
    bare_sh_total = 0
    y_sh_lfirst = 0
    y_sh_total = 0
    d_sh_lfirst = 0
    d_sh_total = 0

    for r in a_records:
        words = r['words']
        for pos, w in enumerate(words):
            if is_y_sh_compound(w):
                y_sh_total += 1
                if pos == 0:
                    y_sh_lfirst += 1
            elif is_d_sh_compound(w):
                d_sh_total += 1
                if pos == 0:
                    d_sh_lfirst += 1
            elif w.startswith('sh') and len(w) >= 3 and not is_y_sh_compound(w):
                bare_sh_total += 1
                if pos == 0:
                    bare_sh_lfirst += 1

    print(f"\n--- sh-Stem Positional Distribution (A Dialect) ---")
    print(f"{'Type':<20} {'n_tokens':<12} {'LFirst%':<12} {'vs bare ratio':<12}")

    bare_rate = bare_sh_lfirst / bare_sh_total if bare_sh_total else 0
    y_rate = y_sh_lfirst / y_sh_total if y_sh_total else 0
    d_rate = d_sh_lfirst / d_sh_total if d_sh_total else 0

    print(f"{'bare sh':<20} {bare_sh_total:<12} {bare_rate*100:.1f}%       1.00× (baseline)")
    print(f"{'d+sh':<20} {d_sh_total:<12} {d_rate*100:.1f}%       {d_rate/bare_rate:.2f}×" if bare_rate > 0 else f"{'d+sh':<20} {d_sh_total:<12} {d_rate*100:.1f}%       N/A")
    print(f"{'y+sh':<20} {y_sh_total:<12} {y_rate*100:.1f}%       {y_rate/bare_rate:.2f}×" if bare_rate > 0 else f"{'y+sh':<20} {y_sh_total:<12} {y_rate*100:.1f}%       N/A")

    # Top y+sh and d+sh forms
    y_sh_forms = Counter()
    d_sh_forms = Counter()
    for r in a_records:
        for w in r['words']:
            if is_y_sh_compound(w):
                y_sh_forms[w] += 1
            elif is_d_sh_compound(w):
                d_sh_forms[w] += 1

    print(f"\nTop y+sh forms: {y_sh_forms.most_common(8)}")
    print(f"Top d+sh forms: {d_sh_forms.most_common(8)}")

    # Compare to ch-stem paradigm ratios from exp_091
    print(f"\n--- Paradigm Comparison: sh-stems vs ch-stems (A Dialect) ---")
    print(f"{'Stem class':<20} {'bare LFirst':<14} {'d+stem LFirst':<16} {'y+stem LFirst':<16} {'d/bare':<10} {'y/bare':<10}")
    print(f"{'ch-stems (exp091)':<20} {'9.7%':<14} {'59.6%':<16} {'85.9%':<16} {'6.17×':<10} {'8.86×':<10}")
    d_ratio = d_rate/bare_rate if bare_rate > 0 else 0
    y_ratio = y_rate/bare_rate if bare_rate > 0 else 0
    print(f"{'sh-stems (this exp)':<20} {bare_rate*100:.1f}%{'':<8} {d_rate*100:.1f}%{'':<10} {y_rate*100:.1f}%{'':<10} {d_ratio:.2f}×{'':<4} {y_ratio:.2f}×")

    return bare_rate, d_rate, y_rate, d_sh_total, y_sh_total


def h163_inter_line_context(records):
    """H163: Do y+ch and d+ch openers depend on the preceding line's closing onset?"""
    print("\n" + "=" * 70)
    print("H163: A Line Opener (y+ch vs d+ch) Preceded by Which Line-Closers?")
    print("=" * 70)

    a_records = [r for r in records if r['dialect'] == 'A']

    # Build consecutive-line pairs
    y_ch_prev_last_onset = Counter()
    d_ch_prev_last_onset = Counter()
    bare_ch_prev_last_onset = Counter()

    for i in range(1, len(a_records)):
        curr = a_records[i]
        prev = a_records[i-1]

        # Only within same folio (don't cross folio boundaries)
        if curr['folio'] != prev['folio']:
            continue

        prev_last_onset = get_onset(prev['last_word'])
        curr_first = curr['first_word']

        if is_y_ch_compound(curr_first):
            y_ch_prev_last_onset[prev_last_onset] += 1
        elif is_d_ch_compound(curr_first):
            d_ch_prev_last_onset[prev_last_onset] += 1
        elif curr_first.startswith('ch'):
            bare_ch_prev_last_onset[prev_last_onset] += 1

    y_total = sum(y_ch_prev_last_onset.values())
    d_total = sum(d_ch_prev_last_onset.values())
    b_total = sum(bare_ch_prev_last_onset.values())

    print(f"\nLines preceded by (prev line last word onset):")
    print(f"{'Prev onset':<12} {'y+ch %':<12} {'d+ch %':<12} {'bare ch %':<12} {'Ratio y/d':<10}")

    all_onsets = sorted(set(
        list(y_ch_prev_last_onset.keys()) +
        list(d_ch_prev_last_onset.keys()) +
        list(bare_ch_prev_last_onset.keys())
    ))

    for onset in sorted(all_onsets, key=lambda x: -(y_ch_prev_last_onset.get(x,0)/y_total if y_total else 0)):
        yp = y_ch_prev_last_onset.get(onset, 0) / y_total if y_total else 0
        dp = d_ch_prev_last_onset.get(onset, 0) / d_total if d_total else 0
        bp = bare_ch_prev_last_onset.get(onset, 0) / b_total if b_total else 0
        ratio = yp/dp if dp > 0 else float('inf')
        print(f"  {onset:<10} {yp*100:>6.1f}%    {dp*100:>6.1f}%    {bp*100:>6.1f}%    {ratio:.2f}×")

    print(f"\ny+ch n={y_total}, d+ch n={d_total}, bare_ch n={b_total}")

    # Para-start context: what OPENS first line of a para vs subsequent lines?
    print(f"\n--- Para-Start vs Within-Para Opener Distribution ---")
    ps_openers = Counter()
    wp_openers = Counter()

    for r in a_records:
        opener = r['first_word']
        if is_y_ch_compound(opener):
            label = 'y+ch'
        elif is_d_ch_compound(opener):
            label = 'd+ch'
        elif opener.startswith('ch'):
            label = 'bare_ch'
        elif opener.startswith('sh'):
            label = 'sh'
        elif opener.startswith('y'):
            label = 'y-other'
        elif opener.startswith('d'):
            label = 'd-other'
        else:
            label = get_onset(opener)

        if r['is_para_start']:
            ps_openers[label] += 1
        else:
            wp_openers[label] += 1

    ps_total = sum(ps_openers.values())
    wp_total = sum(wp_openers.values())

    print(f"{'Opener type':<14} {'PS %':<12} {'WP %':<12} {'Enrichment (PS/WP)':<20}")
    for label in sorted(set(list(ps_openers.keys()) + list(wp_openers.keys())),
                        key=lambda x: -(ps_openers.get(x,0)/ps_total if ps_total else 0)):
        pp = ps_openers.get(label, 0) / ps_total if ps_total else 0
        wp = wp_openers.get(label, 0) / wp_total if wp_total else 0
        enr = pp/wp if wp > 0 else float('inf')
        print(f"  {label:<12} {pp*100:>6.1f}%    {wp*100:>6.1f}%    {enr:.2f}×")

    print(f"\nPS total lines: {ps_total}, WP total lines: {wp_total}")


def main():
    print("Loading data...")
    records = parse_voynich()
    print(f"Total line records: {len(records)}")

    a_count = sum(1 for r in records if r['dialect'] == 'A')
    b_count = sum(1 for r in records if r['dialect'] == 'B')
    print(f"A dialect lines: {a_count}, B dialect lines: {b_count}")

    print()
    y_ch_ps, d_ch_ps, base_ps = h161_y_ch_vs_d_ch_context(records)
    h162_sh_stem_paradigm(records)
    h163_inter_line_context(records)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"H161: y+ch PS rate={y_ch_ps:.3f} ({y_ch_ps/base_ps:.2f}× base={base_ps:.3f})")
    print(f"      d+ch PS rate={d_ch_ps:.3f} ({d_ch_ps/base_ps:.2f}× base={base_ps:.3f})")
    if y_ch_ps > 0 and d_ch_ps > 0:
        print(f"      y+ch/d+ch PS ratio: {y_ch_ps/d_ch_ps:.2f}×")


if __name__ == '__main__':
    main()
