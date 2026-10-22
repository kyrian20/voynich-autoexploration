"""
exp_195: Stars Entry Markers + dam Cross-Dialect + she- Profile + d-Chains

H356: Stars PARA-tier words as zodiacal entry markers — specific word analysis,
      spacing distribution, closed vs open vocabulary.

H357: Full PARA-tier (k/t/f/p) exclusion from para-final — are all gallows
      excluded from para-final positions?

H358: d-chain vocabulary — in runs of 3-5 consecutive d-final lines, are
      the d-words identical (formulaic) or diverse (grammatical)?

H127: d-onset cross-dialect bridge — dam/d-onset positional comparison A vs B.

H147: she- word following profile — what words/onsets follow she-prefix words?
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')


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
    if w.startswith('o'): return 'o'
    return 'other'


def is_para_tier(word):
    """v2 classifier: p/k/t/f-onset = PARA tier."""
    return word and get_onset(word) in ('p', 'k', 't', 'f')


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

    paragraphs = {}
    current_para = None
    para_count = 0

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

            if is_para_start:
                para_count += 1
                current_para = para_count
                paragraphs[current_para] = {
                    'dialect': dialect,
                    'section': section,
                    'folio': fb,
                    'lines': []
                }

            if current_para is not None:
                paragraphs[current_para]['lines'].append(words)

    return paragraphs, folio_dialect


def h356_stars_entry_markers(paragraphs):
    """H356: Stars PARA-tier words as zodiacal entry markers."""
    print("=" * 70)
    print("H356: Stars B PARA-Tier Words as Entry Markers")
    print("=" * 70)

    stars_paras = {pid: p for pid, p in paragraphs.items()
                   if p['section'] == 'stars' and p['dialect'] == 'B'}

    # Collect ALL non-PS PARA-tier words in stars paragraphs
    para_marker_words = []  # (word, position_in_para, para_id, folio)
    all_marker_positions = []  # positions of PARA-tier at lines 3+

    for pid, p in sorted(stars_paras.items()):
        lines = p['lines']
        n = len(lines)
        for i in range(1, n):  # skip line 0 (para-start)
            if lines[i] and is_para_tier(lines[i][0]):
                para_marker_words.append((lines[i][0], i, pid, p['folio']))
                all_marker_positions.append(i)

    print(f"\nTotal non-PS PARA-tier words in stars paras: {len(para_marker_words)}")

    # Word frequency
    word_counts = Counter(w for w, pos, pid, fb in para_marker_words)
    print(f"\nTop 30 PARA-tier marker words (non-PS positions):")
    for word, cnt in word_counts.most_common(30):
        print(f"  {word}: {cnt}")

    print(f"\nTotal unique PARA-tier marker words: {len(word_counts)}")
    print(f"Top-10 words cover {sum(c for _, c in word_counts.most_common(10))}/{len(para_marker_words)} "
          f"= {sum(c for _, c in word_counts.most_common(10))/len(para_marker_words):.1%}")

    # Onset distribution of marker words
    print(f"\nOnset distribution of PARA-tier markers:")
    onset_counts = Counter(get_onset(w) for w, _, _, _ in para_marker_words)
    for onset, cnt in sorted(onset_counts.items(), key=lambda x: -x[1]):
        print(f"  {onset}: {cnt} ({cnt/len(para_marker_words):.1%})")

    # Position distribution
    print(f"\nPosition of PARA-tier markers within stars paragraphs:")
    pos_counts = Counter(all_marker_positions)
    for pos in sorted(pos_counts.keys()):
        n_paras_at_pos = sum(1 for p in stars_paras.values() if pos < len(p['lines']))
        rate = pos_counts[pos] / n_paras_at_pos if n_paras_at_pos else 0
        bar = '█' * pos_counts[pos]
        print(f"  Line {pos:2d} (n={pos_counts[pos]:2d}, rate={rate:.2f}): {bar}")

    # Spacing between consecutive PARA-tier markers within same paragraph
    spacings = []
    for pid, p in sorted(stars_paras.items()):
        lines = p['lines']
        marker_positions = [i for i in range(1, len(lines))
                           if lines[i] and is_para_tier(lines[i][0])]
        for j in range(1, len(marker_positions)):
            spacings.append(marker_positions[j] - marker_positions[j-1])

    if spacings:
        from statistics import mean, median
        print(f"\nSpacing between consecutive PARA-tier markers (n={len(spacings)}):")
        print(f"  mean={mean(spacings):.1f}, median={median(spacings):.1f}")
        spacing_dist = Counter(spacings)
        for s in sorted(spacing_dist.keys()):
            print(f"  spacing={s}: {spacing_dist[s]}")

    # Are the same words reused across paragraphs?
    print(f"\nWords appearing in 5+ paragraphs:")
    for word, cnt in word_counts.most_common(20):
        para_ids = set(pid for w, pos, pid, fb in para_marker_words if w == word)
        if len(para_ids) >= 5:
            print(f"  {word}: {cnt} tokens, {len(para_ids)} distinct paragraphs")

    # First PARA-tier marker position in each paragraph
    first_marker_positions = []
    for pid, p in sorted(stars_paras.items()):
        lines = p['lines']
        for i in range(1, len(lines)):
            if lines[i] and is_para_tier(lines[i][0]):
                first_marker_positions.append(i)
                break

    if first_marker_positions:
        print(f"\nFirst PARA-tier marker position in each stars paragraph:")
        pos_dist = Counter(first_marker_positions)
        for pos in sorted(pos_dist.keys()):
            print(f"  Position {pos}: {pos_dist[pos]} paragraphs")


def h357_full_gallows_para_final(paragraphs):
    """H357: Full PARA-tier exclusion from para-final."""
    print("\n" + "=" * 70)
    print("H357: Full Gallows Exclusion from Para-Final")
    print("=" * 70)

    gallows = ['p', 'k', 't', 'f']

    for dialect in ['A', 'B']:
        d_paras = {pid: p for pid, p in paragraphs.items()
                   if p['dialect'] == dialect and len(p['lines']) >= 2}

        para_final_onsets = []
        within_para_onsets = []

        for pid, p in d_paras.items():
            lines = p['lines']
            for i, line in enumerate(lines):
                if not line:
                    continue
                last_word = line[-1]
                onset = get_onset(last_word)
                if i == len(lines) - 1:
                    para_final_onsets.append(onset)
                else:
                    within_para_onsets.append(onset)

        total_pf = len(para_final_onsets)
        total_wp = len(within_para_onsets)

        print(f"\nDialect {dialect} — para-final n={total_pf}, within-para n={total_wp}")
        print(f"{'Onset':<6} {'PF%':>7} {'WP%':>7} {'Enrich':>8} {'PF_n':>6}")
        print("-" * 40)

        # All gallows individually
        for onset in gallows:
            pf_n = para_final_onsets.count(onset)
            wp_n = within_para_onsets.count(onset)
            pf_rate = pf_n / total_pf if total_pf else 0
            wp_rate = wp_n / total_wp if total_wp else 0
            enrich = pf_rate / wp_rate if wp_rate > 0.001 else (float('inf') if pf_n > 0 else 0.00)
            print(f"{onset:<6} {pf_rate:>7.2%} {wp_rate:>7.2%} {enrich:>8.2f}×  {pf_n:>5}")

        # All non-gallows for comparison
        print("\n  (comparison: key non-gallows)")
        for onset in ['d', 'ch', 'o', 'ok', 'sh']:
            pf_n = para_final_onsets.count(onset)
            wp_n = within_para_onsets.count(onset)
            pf_rate = pf_n / total_pf if total_pf else 0
            wp_rate = wp_n / total_wp if total_wp else 0
            enrich = pf_rate / wp_rate if wp_rate > 0.001 else float('inf')
            print(f"  {onset:<6} {pf_rate:>7.2%} {wp_rate:>7.2%} {enrich:>8.2f}×  {pf_n:>5}")


def h358_d_chain_vocabulary(paragraphs):
    """H358: d-chain vocabulary analysis."""
    print("\n" + "=" * 70)
    print("H358: d-Chain Vocabulary Analysis (A Dialect)")
    print("=" * 70)

    a_paras = {pid: p for pid, p in paragraphs.items()
               if p['dialect'] == 'A' and len(p['lines']) >= 3}

    # Find runs of 3+ consecutive d-final lines
    d_runs = []
    for pid, p in sorted(a_paras.items()):
        lines = p['lines']
        current_run = []
        for i, line in enumerate(lines):
            if not line:
                continue
            last_word = line[-1]
            if get_onset(last_word) == 'd':
                current_run.append((i, last_word))
            else:
                if len(current_run) >= 3:
                    d_runs.append({'para': pid, 'folio': p['folio'], 'run': current_run})
                current_run = []
        if len(current_run) >= 3:
            d_runs.append({'para': pid, 'folio': p['folio'], 'run': current_run})

    print(f"\nRuns of 3+ consecutive d-final lines: {len(d_runs)}")

    # Analyze vocabulary in each run
    identical_runs = 0
    same_stem_runs = 0
    diverse_runs = 0

    for run_data in d_runs:
        words = [w for _, w in run_data['run']]
        unique_words = set(words)
        if len(unique_words) == 1:
            identical_runs += 1
        elif len(unique_words) <= 2:
            same_stem_runs += 1
        else:
            diverse_runs += 1

    print(f"\nRun vocabulary diversity:")
    print(f"  All identical words: {identical_runs}")
    print(f"  1-2 distinct words: {same_stem_runs}")
    print(f"  3+ distinct words (diverse): {diverse_runs}")

    print(f"\nDetailed d-runs of length 3+:")
    for run_data in d_runs[:20]:  # show first 20
        words = [w for _, w in run_data['run']]
        positions = [pos for pos, _ in run_data['run']]
        unique_words = set(words)
        diversity = 'IDENTICAL' if len(unique_words) == 1 else ('SIMILAR' if len(unique_words) == 2 else 'DIVERSE')
        print(f"  Para {run_data['para']} (folio {run_data['folio']}): "
              f"lines {positions} = {words} [{diversity}]")

    # Word frequency in d-runs
    all_run_words = [w for rd in d_runs for _, w in rd['run']]
    print(f"\nMost common d-final words in runs:")
    for word, cnt in Counter(all_run_words).most_common(15):
        print(f"  {word}: {cnt}")


def h127_dam_cross_dialect(paragraphs, folio_dialect):
    """H127: dam cross-dialect bridge analysis."""
    print("\n" + "=" * 70)
    print("H127: dam/d-Onset Cross-Dialect Bridge Analysis")
    print("=" * 70)

    # Collect all d-onset word positional data
    for dialect in ['A', 'B']:
        d_paras = {pid: p for pid, p in paragraphs.items()
                   if p['dialect'] == dialect}

        d_words_lf = []   # d-onset words at LF
        d_words_ll = []   # d-onset words at LL
        d_words_mid = []  # d-onset words at MID

        for pid, p in d_paras.items():
            for line in p['lines']:
                if not line:
                    continue
                for i, w in enumerate(line):
                    if get_onset(w) == 'd':
                        if i == 0:
                            d_words_lf.append(w)
                        elif i == len(line) - 1:
                            d_words_ll.append(w)
                        else:
                            d_words_mid.append(w)

        total_d = len(d_words_lf) + len(d_words_ll) + len(d_words_mid)

        print(f"\nDialect {dialect} d-onset words (n={total_d}):")
        print(f"  LF: {len(d_words_lf)} ({len(d_words_lf)/total_d:.1%})")
        print(f"  LL: {len(d_words_ll)} ({len(d_words_ll)/total_d:.1%})")
        print(f"  MID: {len(d_words_mid)} ({len(d_words_mid)/total_d:.1%})")

        print(f"\n  Top d-onset words at LL:")
        for word, cnt in Counter(d_words_ll).most_common(10):
            ll_rate = d_words_ll.count(word) / (d_words_ll.count(word) + d_words_lf.count(word) + d_words_mid.count(word))
            print(f"    {word}: {cnt} at LL ({ll_rate:.1%} of all positions)")

        print(f"\n  Top d-onset words at LF:")
        for word, cnt in Counter(d_words_lf).most_common(10):
            print(f"    {word}: {cnt}")

    # Specific dam comparison
    print("\n--- dam cross-dialect comparison ---")
    for dialect in ['A', 'B']:
        d_paras = {pid: p for pid, p in paragraphs.items()
                   if p['dialect'] == dialect}

        dam_lf = dam_ll = dam_mid = 0
        for pid, p in d_paras.items():
            for line in p['lines']:
                if not line:
                    continue
                for i, w in enumerate(line):
                    if w == 'dam':
                        if i == 0: dam_lf += 1
                        elif i == len(line) - 1: dam_ll += 1
                        else: dam_mid += 1

        dam_total = dam_lf + dam_ll + dam_mid
        if dam_total > 0:
            print(f"  {dialect}: dam total={dam_total}, LF={dam_lf}({dam_lf/dam_total:.1%}), "
                  f"LL={dam_ll}({dam_ll/dam_total:.1%}), MID={dam_mid}({dam_mid/dam_total:.1%})")

    # Preceding words before dam@LL in both dialects
    print("\n  Words preceding dam@LL:")
    for dialect in ['A', 'B']:
        d_paras = {pid: p for pid, p in paragraphs.items()
                   if p['dialect'] == dialect}

        precede_dam = []
        for pid, p in d_paras.items():
            for line in p['lines']:
                if not line:
                    continue
                if line[-1] == 'dam' and len(line) >= 2:
                    precede_dam.append(line[-2])

        print(f"  {dialect}: {Counter(precede_dam).most_common(10)}")


def h147_she_following_profile(paragraphs):
    """H147: she- word following-word profile."""
    print("\n" + "=" * 70)
    print("H147: she- Word Following-Word Profile (A Dialect)")
    print("=" * 70)

    # Collect all she-prefix words and their successors in A
    she_bigrams = []  # (she_word, next_word, para_pos)
    all_bigrams_a = []  # all bigrams in A for baseline

    a_paras = {pid: p for pid, p in paragraphs.items()
               if p['dialect'] == 'A'}

    for pid, p in a_paras.items():
        for line in p['lines']:
            if len(line) < 2:
                continue
            for i in range(len(line) - 1):
                w1, w2 = line[i], line[i+1]
                all_bigrams_a.append((w1, w2))
                if w1.startswith('she') and len(w1) >= 4:
                    she_bigrams.append((w1, w2, 'within_line'))

    # Successors of she- words
    print(f"\nA-dialect she-prefix words: {len(she_bigrams)} within-line successors")

    # she- word frequency
    she_words = Counter(w1 for w1, w2, pos in she_bigrams)
    print(f"\nTop she- words:")
    for word, cnt in she_words.most_common(10):
        print(f"  {word}: {cnt}")

    # Successor onset distribution
    succ_onsets = Counter(get_onset(w2) for w1, w2, pos in she_bigrams)
    total_she = len(she_bigrams)

    # Baseline: overall onset distribution in A (from all successors)
    baseline_onsets = Counter(get_onset(w2) for w1, w2 in all_bigrams_a)
    total_baseline = len(all_bigrams_a)

    print(f"\nSuccessor onset distribution after she- words vs baseline:")
    print(f"{'Onset':<8} {'she%':>7} {'base%':>7} {'Enrich':>8} {'n':>5}")
    print("-" * 40)

    for onset in sorted(set(succ_onsets) | set(baseline_onsets),
                         key=lambda x: -succ_onsets.get(x, 0)):
        she_rate = succ_onsets.get(onset, 0) / total_she
        base_rate = baseline_onsets.get(onset, 0) / total_baseline
        enrich = she_rate / base_rate if base_rate > 0.001 else float('inf')
        n = succ_onsets.get(onset, 0)
        if n >= 3 or base_rate > 0.02:
            print(f"{onset:<8} {she_rate:>7.2%} {base_rate:>7.2%} {enrich:>8.2f}×  {n:>5}")

    # Top specific successor words
    succ_words = Counter(w2 for w1, w2, pos in she_bigrams)
    print(f"\nTop 15 successor words after she- words:")
    for word, cnt in succ_words.most_common(15):
        base_word_rate = sum(1 for w1, w2 in all_bigrams_a if w2 == word) / total_baseline
        she_word_rate = cnt / total_she
        enrich = she_word_rate / base_word_rate if base_word_rate > 0.0001 else float('inf')
        print(f"  {word}: {cnt} ({enrich:.1f}×)")

    # she-para-start lines vs she-non-para-start lines
    print("\nShe- words at para-start vs non-para-start lines:")
    she_at_ps = 0   # she-word at line-first in para-start lines
    she_at_wp = 0   # she-word at line-first in within-para lines

    for pid, p in a_paras.items():
        lines = p['lines']
        for i, line in enumerate(lines):
            if line and line[0].startswith('she') and len(line[0]) >= 4:
                if i == 0:
                    she_at_ps += 1
                else:
                    she_at_wp += 1

    total_ps = sum(1 for p in a_paras.values() if p['lines'])
    total_wp = sum(len(p['lines']) - 1 for p in a_paras.values() if len(p['lines']) > 1)

    print(f"  she-words at para-start (LF of line 0): {she_at_ps}/{total_ps} = {she_at_ps/total_ps:.2%}")
    print(f"  she-words at within-para LF: {she_at_wp}/{total_wp} = {she_at_wp/total_wp:.2%}")
    if total_wp > 0 and she_at_wp > 0:
        print(f"  PS enrichment: {(she_at_ps/total_ps)/(she_at_wp/total_wp):.2f}×")


def main():
    print("Loading corpus...")
    paragraphs, folio_dialect = parse_voynich()

    total_paras = len(paragraphs)
    a_paras = sum(1 for p in paragraphs.values() if p['dialect'] == 'A')
    b_paras = sum(1 for p in paragraphs.values() if p['dialect'] == 'B')
    print(f"Total paragraphs: {total_paras} (A={a_paras}, B={b_paras})")

    h356_stars_entry_markers(paragraphs)
    h357_full_gallows_para_final(paragraphs)
    h358_d_chain_vocabulary(paragraphs)
    h127_dam_cross_dialect(paragraphs, folio_dialect)
    h147_she_following_profile(paragraphs)


if __name__ == '__main__':
    main()
