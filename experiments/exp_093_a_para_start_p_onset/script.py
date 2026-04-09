"""
exp_093: A Para-Start p/k/t-Onset Words (H164), d-Chain Pattern (H165), Cross-Dialect Para-Start Comparison (H166)

H164: A para-starts are dominated by specific p-onset words — identify the closed class.
H165: d-closer → d+ch opener is statistically significant (d-chain pattern).
H166: A p-onset para-start words = B's pchedy/tchedy para-starters — both dialects use p/t-onset for para-starts.
"""

import re
import os
from collections import defaultdict, Counter

DATA_PATH = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'


def folio_base(folio):
    return re.sub(r'\.\d+$', '', folio)


def classify_dialect(folio_stats):
    total = folio_stats.get('total', 0)
    if total == 0:
        return 'unknown'
    rate = (folio_stats.get('edy', 0) + folio_stats.get('eedy', 0)) / total
    return 'B' if rate >= 0.05 else 'A'


def classify_section(folio):
    m = re.match(r'f(\d+)([rv])', folio)
    if not m:
        return 'unknown'
    n = int(m.group(1))
    if n <= 57:
        return 'herbal'
    if 67 <= n <= 73:
        return 'astro'
    if 75 <= n <= 84:
        return 'cosmo'
    if 87 <= n <= 102:
        return 'pharma'
    if 103 <= n <= 116:
        return 'stars'
    return 'other'


def get_onset(word):
    for prefix in ['qo', 'ch', 'sh']:
        if word.startswith(prefix):
            return prefix
    if word[0] in 'ptk':
        return word[0]
    if word[0] in 'dsyo':
        return word[0]
    return 'other'


def is_y_ch_compound(word):
    return word.startswith('ych') and len(word) >= 4


def is_d_ch_compound(word):
    return word.startswith('dch') and len(word) >= 4


def parse_voynich():
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m:
                continue
            folio_raw = m.group(1)
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
            section = classify_section(fb)

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
                'section': section,
                'is_para_start': is_para_start,
                'words': words,
                'n_words': len(words),
                'first_word': words[0],
                'last_word': words[-1],
            })

    return records


def h164_a_para_start_p_onset(records):
    """H164: Identify the specific p/k/t-onset A para-start words."""
    print("=" * 70)
    print("H164: A Para-Start p/k/t-Onset Words — Identification")
    print("=" * 70)

    a_records = [r for r in records if r['dialect'] == 'A']
    a_ps = [r for r in a_records if r['is_para_start']]
    a_wp = [r for r in a_records if not r['is_para_start']]

    total_ps = len(a_ps)
    total_wp = len(a_wp)
    total = len(a_records)

    print(f"\nA total lines: {total}, para-start: {total_ps}, within-para: {total_wp}")
    print(f"Base para-start rate: {total_ps/total:.3f}")

    # Word-level analysis for all words
    word_ps_count = Counter()
    word_wp_count = Counter()

    for r in a_ps:
        word_ps_count[r['first_word']] += 1
    for r in a_wp:
        word_wp_count[r['first_word']] += 1

    # Compute PSFirst enrichment for all words
    results = []
    all_words = set(word_ps_count.keys()) | set(word_wp_count.keys())
    for word in all_words:
        ps = word_ps_count.get(word, 0)
        wp = word_wp_count.get(word, 0)
        total_w = ps + wp
        if total_w < 3:
            continue
        ps_rate = ps / total_ps if total_ps > 0 else 0
        wp_rate = wp / total_wp if total_wp > 0 else 0
        ps_frac = ps / total_w  # PSFirst% = this word appears at PS as % of all its occurrences
        enr = (ps / total_ps) / (wp / total_wp) if wp > 0 and wp_rate > 0 else float('inf')
        results.append({
            'word': word,
            'onset': get_onset(word),
            'ps_count': ps,
            'wp_count': wp,
            'total': total_w,
            'ps_frac': ps_frac,
            'enrichment': enr,
        })

    results.sort(key=lambda x: -x['enrichment'])

    print(f"\n--- Top Para-Start Enriched Words in A (n>=3, sorted by enrichment) ---")
    print(f"{'Word':<16} {'onset':<8} {'PS_n':<8} {'WP_n':<8} {'Total':<8} {'PSFirst%':<10} {'Enrichment':<12}")
    for r in results[:30]:
        print(f"  {r['word']:<14} {r['onset']:<8} {r['ps_count']:<8} {r['wp_count']:<8} {r['total']:<8} {r['ps_frac']*100:>6.1f}%    {r['enrichment']:>8.2f}×")

    # p-onset specifically
    print(f"\n--- All p-onset A Words (n>=2) ---")
    print(f"{'Word':<16} {'PS_n':<8} {'WP_n':<8} {'Total':<8} {'PSFirst%':<10} {'Enrichment':<12}")
    p_results = sorted([r for r in results if r['onset'] == 'p'], key=lambda x: -x['enrichment'])
    for r in p_results:
        print(f"  {r['word']:<14} {r['ps_count']:<8} {r['wp_count']:<8} {r['total']:<8} {r['ps_frac']*100:>6.1f}%    {r['enrichment']:>8.2f}×")

    # Also low-count p-onset
    print(f"\n--- p-onset words with n=1 or 2 (all of them) ---")
    p_low = [(w, word_ps_count.get(w,0), word_wp_count.get(w,0))
             for w in all_words if get_onset(w) == 'p' and
             word_ps_count.get(w,0) + word_wp_count.get(w,0) < 3]
    print(f"  {sorted(p_low, key=lambda x: -(x[1]+x[2]))[:20]}")

    # Section distribution of p-onset para-starters
    print(f"\n--- p-onset Para-Start by Section ---")
    p_ps_section = Counter()
    for r in a_ps:
        if get_onset(r['first_word']) == 'p':
            p_ps_section[r['section']] += 1
    total_ps_p = sum(p_ps_section.values())
    for sect, cnt in sorted(p_ps_section.items(), key=lambda x: -x[1]):
        print(f"  {sect}: {cnt} ({cnt/total_ps_p*100:.1f}%)")

    # What follows p-onset para-starters
    print(f"\n--- What Follows p-onset Para-Start Words (pos1 onset) ---")
    p_ps_following = Counter()
    for r in a_ps:
        if get_onset(r['first_word']) == 'p' and len(r['words']) >= 2:
            p_ps_following[get_onset(r['words'][1])] += 1
    total_follow = sum(p_ps_following.values())
    for onset, cnt in sorted(p_ps_following.items(), key=lambda x: -x[1]):
        print(f"  {onset}: {cnt} ({cnt/total_follow*100:.1f}%)")


def h165_d_chain_pattern(records):
    """H165: d-closer → d+ch opener (d-chain) — statistical test."""
    print("\n" + "=" * 70)
    print("H165: d-Chain Pattern — d-Closer Triggers d+ch Opener")
    print("=" * 70)

    a_records = [r for r in records if r['dialect'] == 'A']

    # Build consecutive-line pairs (same folio only)
    d_closer_then_dch = 0
    d_closer_then_ych = 0
    d_closer_then_other = 0
    non_d_closer_then_dch = 0
    non_d_closer_then_ych = 0
    non_d_closer_then_other = 0

    d_chain_runs = []
    current_run = 0

    for i in range(1, len(a_records)):
        curr = a_records[i]
        prev = a_records[i-1]

        if curr['folio'] != prev['folio']:
            if current_run > 0:
                d_chain_runs.append(current_run)
            current_run = 0
            continue

        prev_last_is_d = get_onset(prev['last_word']) == 'd'
        curr_opens_with_dch = is_d_ch_compound(curr['first_word'])
        curr_opens_with_ych = is_y_ch_compound(curr['first_word'])

        if prev_last_is_d:
            if curr_opens_with_dch:
                d_closer_then_dch += 1
                current_run += 1
            elif curr_opens_with_ych:
                d_closer_then_ych += 1
                if current_run > 0:
                    d_chain_runs.append(current_run)
                current_run = 0
            else:
                d_closer_then_other += 1
                if current_run > 0:
                    d_chain_runs.append(current_run)
                current_run = 0
        else:
            if curr_opens_with_dch:
                non_d_closer_then_dch += 1
            elif curr_opens_with_ych:
                non_d_closer_then_ych += 1
            else:
                non_d_closer_then_other += 1
            if current_run > 0:
                d_chain_runs.append(current_run)
            current_run = 0

    # Statistical test
    total_d_closer = d_closer_then_dch + d_closer_then_ych + d_closer_then_other
    total_non_d = non_d_closer_then_dch + non_d_closer_then_ych + non_d_closer_then_other

    p_dch_given_d = d_closer_then_dch / total_d_closer if total_d_closer > 0 else 0
    p_dch_given_nond = non_d_closer_then_dch / total_non_d if total_non_d > 0 else 0
    enrichment = p_dch_given_d / p_dch_given_nond if p_dch_given_nond > 0 else float('inf')

    p_ych_given_d = d_closer_then_ych / total_d_closer if total_d_closer > 0 else 0
    p_ych_given_nond = non_d_closer_then_ych / total_non_d if total_non_d > 0 else 0
    ych_enrichment = p_ych_given_d / p_ych_given_nond if p_ych_given_nond > 0 else float('inf')

    print(f"\nAfter d-closing line:")
    print(f"  d+ch next: {d_closer_then_dch}/{total_d_closer} = {p_dch_given_d*100:.1f}%")
    print(f"  y+ch next: {d_closer_then_ych}/{total_d_closer} = {p_ych_given_d*100:.1f}%")
    print(f"  other next: {d_closer_then_other}/{total_d_closer} = {d_closer_then_other/total_d_closer*100:.1f}%")

    print(f"\nAfter NON-d-closing line:")
    print(f"  d+ch next: {non_d_closer_then_dch}/{total_non_d} = {p_dch_given_nond*100:.1f}%")
    print(f"  y+ch next: {non_d_closer_then_ych}/{total_non_d} = {p_ych_given_nond*100:.1f}%")

    print(f"\nEnrichment:")
    print(f"  d+ch after d-closer: {enrichment:.2f}× (P={p_dch_given_d:.3f} vs baseline={p_dch_given_nond:.3f})")
    print(f"  y+ch after d-closer: {ych_enrichment:.2f}× (P={p_ych_given_d:.3f} vs baseline={p_ych_given_nond:.3f})")

    # Chi-square test equivalent (simple ratio test)
    if total_d_closer > 0 and total_non_d > 0:
        # Fisher-like: compare proportions
        expected_dch = total_d_closer * p_dch_given_nond
        print(f"\n  Expected d+ch after d-closer (if no effect): {expected_dch:.1f}")
        print(f"  Observed d+ch after d-closer: {d_closer_then_dch}")
        if expected_dch > 0:
            print(f"  Observed/Expected = {d_closer_then_dch/expected_dch:.2f}×")

    # Chain run distribution
    if d_chain_runs:
        run_counter = Counter(d_chain_runs)
        print(f"\nD-chain run lengths (consecutive d+ch openers after d-closer):")
        for length, cnt in sorted(run_counter.items()):
            print(f"  length={length}: {cnt} runs")

    # Also test the o-chain pattern
    print(f"\n--- o-ending → y+ch vs d+ch ---")
    o_then_ych = 0
    o_then_dch = 0
    nono_then_ych = 0
    nono_then_dch = 0
    total_o = 0
    total_nono = 0

    for i in range(1, len(a_records)):
        curr = a_records[i]
        prev = a_records[i-1]
        if curr['folio'] != prev['folio']:
            continue
        prev_last_onset = get_onset(prev['last_word'])
        is_o = prev_last_onset == 'o'
        if is_o:
            total_o += 1
            if is_y_ch_compound(curr['first_word']):
                o_then_ych += 1
            elif is_d_ch_compound(curr['first_word']):
                o_then_dch += 1
        else:
            total_nono += 1
            if is_y_ch_compound(curr['first_word']):
                nono_then_ych += 1
            elif is_d_ch_compound(curr['first_word']):
                nono_then_dch += 1

    if total_o > 0 and total_nono > 0:
        p_ych_o = o_then_ych / total_o
        p_ych_nono = nono_then_ych / total_nono
        p_dch_o = o_then_dch / total_o
        p_dch_nono = nono_then_dch / total_nono
        print(f"After o-ending line:  y+ch={o_then_ych}/{total_o} ({p_ych_o*100:.1f}%)  d+ch={o_then_dch}/{total_o} ({p_dch_o*100:.1f}%)")
        print(f"After non-o line:     y+ch={nono_then_ych}/{total_nono} ({p_ych_nono*100:.1f}%)  d+ch={nono_then_dch}/{total_nono} ({p_dch_nono*100:.1f}%)")
        print(f"y+ch enrichment after o: {p_ych_o/p_ych_nono:.2f}× vs baseline")
        print(f"d+ch enrichment after o: {p_dch_o/p_dch_nono:.2f}× vs baseline")


def h166_cross_dialect_para_start(records):
    """H166: Cross-dialect comparison of para-start onset patterns."""
    print("\n" + "=" * 70)
    print("H166: Cross-Dialect Para-Start Onset Comparison (A vs B)")
    print("=" * 70)

    for dialect in ['A', 'B']:
        d_records = [r for r in records if r['dialect'] == dialect]
        d_ps = [r for r in d_records if r['is_para_start']]
        d_wp = [r for r in d_records if not r['is_para_start']]
        total_ps = len(d_ps)
        total_wp = len(d_wp)

        if not d_ps:
            continue

        onset_ps = Counter()
        onset_wp = Counter()
        for r in d_ps:
            onset_ps[get_onset(r['first_word'])] += 1
        for r in d_wp:
            onset_wp[get_onset(r['first_word'])] += 1

        print(f"\n{'='*50}")
        print(f"Dialect {dialect} (PS={total_ps}, WP={total_wp})")
        print(f"{'Onset':<10} {'PS%':<10} {'WP%':<10} {'Enrichment':<12}")
        all_onsets = sorted(set(list(onset_ps.keys()) + list(onset_wp.keys())),
                            key=lambda x: -(onset_ps.get(x,0)/total_ps if total_ps else 0))
        for onset in all_onsets:
            pp = onset_ps.get(onset, 0) / total_ps if total_ps else 0
            wp = onset_wp.get(onset, 0) / total_wp if total_wp else 0
            enr = pp/wp if wp > 0 else float('inf')
            print(f"  {onset:<8} {pp*100:>6.1f}%    {wp*100:>6.1f}%    {enr:.2f}×")

    # Word-level comparison: top para-start words by enrichment in each dialect
    print(f"\n--- Top Para-Start Words by Enrichment ---")
    for dialect in ['A', 'B']:
        d_records = [r for r in records if r['dialect'] == dialect]
        d_ps = [r for r in d_records if r['is_para_start']]
        d_wp = [r for r in d_records if not r['is_para_start']]
        total_ps = len(d_ps)
        total_wp = len(d_wp)

        word_ps = Counter(r['first_word'] for r in d_ps)
        word_wp = Counter(r['first_word'] for r in d_wp)

        scored = []
        for word in set(list(word_ps.keys()) + list(word_wp.keys())):
            ps = word_ps.get(word, 0)
            wp = word_wp.get(word, 0)
            if ps + wp < 3:
                continue
            ps_rate = ps / total_ps if total_ps else 0
            wp_rate = wp / total_wp if total_wp else 0
            enr = ps_rate / wp_rate if wp_rate > 0 else float('inf')
            scored.append((word, ps, wp, enr, get_onset(word)))

        scored.sort(key=lambda x: -x[3])
        print(f"\nDialect {dialect} top para-start words:")
        print(f"  {'Word':<16} {'onset':<8} {'PS_n':<8} {'WP_n':<8} {'Enrichment':<12}")
        for word, ps, wp, enr, onset in scored[:15]:
            print(f"  {word:<16} {onset:<8} {ps:<8} {wp:<8} {enr:.2f}×")

    # Are A p-onset para-starters the same as A section's "pch" words in earlier exp?
    print(f"\n--- A p-onset Para-Start Specific Words ---")
    a_ps = [r for r in records if r['dialect'] == 'A' and r['is_para_start']]
    a_wp = [r for r in records if r['dialect'] == 'A' and not r['is_para_start']]
    p_ps_words = Counter(r['first_word'] for r in a_ps if get_onset(r['first_word']) == 'p')
    p_wp_words = Counter(r['first_word'] for r in a_wp if get_onset(r['first_word']) == 'p')
    print(f"All p-onset A para-start opener words:")
    for word, cnt in sorted(p_ps_words.items(), key=lambda x: -x[1]):
        wp_cnt = p_wp_words.get(word, 0)
        total = cnt + wp_cnt
        ps_frac = cnt / total if total > 0 else 0
        print(f"  {word}: PS={cnt}, WP={wp_cnt}, PSFirst%={ps_frac*100:.1f}%")


def main():
    print("Loading data...")
    records = parse_voynich()
    print(f"Total line records: {len(records)}")

    a_count = sum(1 for r in records if r['dialect'] == 'A')
    b_count = sum(1 for r in records if r['dialect'] == 'B')
    print(f"A dialect lines: {a_count}, B dialect lines: {b_count}")

    print()
    h164_a_para_start_p_onset(records)
    h165_d_chain_pattern(records)
    h166_cross_dialect_para_start(records)


if __name__ == '__main__':
    main()
