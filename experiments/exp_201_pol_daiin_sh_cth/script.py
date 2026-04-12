#!/usr/bin/env python3
"""
exp_201: POL-Prefix Profile, daiin Predecessor/Successor, sh→cth, cosmo shedy

H366: pol-prefix words — full positional profile in A and B
H367: daiin predecessor (A LL) and successor (B LF)
H368: non-she sh-prefix → cth bigrams — which specific words?
H369: cosmo B para-final shedy/chedy — spread or concentrated?
"""

import re
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


def parse_corpus():
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
            words = [w for w in re.split(r'[-.\s]', text)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            for w in words:
                folio_word_stats[fb]['total'] += 1
                if w.endswith('eedy'):
                    folio_word_stats[fb]['eedy'] += 1
                elif w.endswith('edy'):
                    folio_word_stats[fb]['edy'] += 1

    folio_dialect = {fb: classify_dialect(stats)
                     for fb, stats in folio_word_stats.items()}

    paragraphs = []
    current_para = None

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
            words = [w for w in re.split(r'[-.\s]', text)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words:
                continue

            if is_para_start:
                current_para = {
                    'dialect': dialect,
                    'section': section,
                    'folio': fb,
                    'lines': []
                }
                paragraphs.append(current_para)

            if current_para is not None:
                current_para['lines'].append(words)

    return paragraphs, folio_dialect


def h366_pol_prefix_profile(paragraphs):
    """H366: pol-prefix words — full positional profile in A and B."""
    print("=" * 70)
    print("H366: POL-Prefix Word Positional Profile")
    print("=" * 70)

    # pol-prefix: starts with 'pol' (not 'p' alone — needs at least 3 chars)
    # Compare to pch-prefix: starts with 'pch' or 'psh'

    pol_words = defaultdict(lambda: defaultdict(lambda: {'lf': 0, 'mid': 0, 'll': 0, 'total': 0}))
    pch_words = defaultdict(lambda: defaultdict(lambda: {'lf': 0, 'mid': 0, 'll': 0, 'total': 0}))
    all_words = defaultdict(lambda: defaultdict(lambda: {'lf': 0, 'mid': 0, 'll': 0, 'total': 0}))

    # Track pol-prefix occurrences with section info
    pol_section_pos = defaultdict(lambda: defaultdict(int))  # word -> section -> pos_count
    pol_word_n = Counter()

    for para in paragraphs:
        dialect = para['dialect']
        section = para['section']
        if dialect not in ('A', 'B'):
            continue
        for line in para['lines']:
            n = len(line)
            for pos, word in enumerate(line):
                if pos == 0:
                    pos_cat = 'lf'
                elif pos == n - 1 and n > 1:
                    pos_cat = 'll'
                else:
                    pos_cat = 'mid'

                is_pol = word.startswith('pol') and len(word) >= 3
                is_pch = (word.startswith('pch') or word.startswith('psh')) and len(word) >= 3

                if is_pol:
                    pol_words[dialect][word][pos_cat] += 1
                    pol_words[dialect][word]['total'] += 1
                    pol_section_pos[word][f"{section}:{pos_cat}"] += 1
                    pol_word_n[f"{dialect}:{word}"] += 1
                if is_pch:
                    pch_words[dialect][word][pos_cat] += 1
                    pch_words[dialect][word]['total'] += 1

                all_words[dialect][word][pos_cat] += 1
                all_words[dialect][word]['total'] += 1

    # Aggregate pol-prefix by dialect
    print("\n--- pol-prefix aggregate positional distribution by dialect ---")
    for dialect in ['A', 'B']:
        pol_agg = {'lf': 0, 'mid': 0, 'll': 0, 'total': 0}
        for word, v in pol_words[dialect].items():
            for k in ['lf', 'mid', 'll', 'total']:
                pol_agg[k] += v[k]
        total = pol_agg['total']
        print(f"\n  {dialect}-dialect pol-prefix: total={total}")
        if total > 0:
            print(f"    LF: {pol_agg['lf']}/{total} = {pol_agg['lf']/total:.3f}")
            print(f"    MID: {pol_agg['mid']}/{total} = {pol_agg['mid']/total:.3f}")
            print(f"    LL: {pol_agg['ll']}/{total} = {pol_agg['ll']/total:.3f}")

        # Top pol words in this dialect
        top_pol = sorted(pol_words[dialect].items(), key=lambda x: -x[1]['total'])[:15]
        if top_pol:
            print(f"\n  Top pol-words in {dialect}:")
            print(f"  {'Word':<18} {'n':<6} {'LF%':<8} {'MID%':<8} {'LL%'}")
            for word, v in top_pol:
                t = v['total']
                print(f"    {word:<18} {t:<6} {v['lf']/t:.3f}{'':<4} {v['mid']/t:.3f}{'':<4} {v['ll']/t:.3f}")

    # Compare to pch-prefix
    print("\n--- pch-prefix aggregate positional distribution by dialect ---")
    for dialect in ['A', 'B']:
        pch_agg = {'lf': 0, 'mid': 0, 'll': 0, 'total': 0}
        for word, v in pch_words[dialect].items():
            for k in ['lf', 'mid', 'll', 'total']:
                pch_agg[k] += v[k]
        total = pch_agg['total']
        print(f"\n  {dialect}-dialect pch-prefix: total={total}")
        if total > 0:
            print(f"    LF: {pch_agg['lf']}/{total} = {pch_agg['lf']/total:.3f}")
            print(f"    MID: {pch_agg['mid']}/{total} = {pch_agg['mid']/total:.3f}")
            print(f"    LL: {pch_agg['ll']}/{total} = {pch_agg['ll']/total:.3f}")

    # pol-prefix section distribution (B only)
    print("\n--- B pol-prefix section distribution ---")
    b_pol_section = Counter()
    b_pol_total = 0
    for para in paragraphs:
        if para['dialect'] != 'B':
            continue
        for line_idx, line in enumerate(para['lines']):
            n = len(line)
            for pos, word in enumerate(line):
                if word.startswith('pol') and len(word) >= 3:
                    b_pol_section[para['section']] += 1
                    b_pol_total += 1

    for section, cnt in b_pol_section.most_common():
        print(f"  {section:<12} {cnt} ({cnt/b_pol_total*100:.1f}%)" if b_pol_total > 0 else f"  {section}: {cnt}")


def h367_daiin_pred_succ(paragraphs):
    """H367: daiin predecessor (A LL) and successor (B LF)."""
    print("\n" + "=" * 70)
    print("H367: daiin Predecessor@LL (A) and Successor@LF (B)")
    print("=" * 70)

    # A: penultimate onset before daiin@LL
    a_penult_onsets = Counter()
    a_daiin_ll_total = 0
    baseline_penult = Counter()
    baseline_penult_total = 0

    # B: second word after daiin@LF
    b_second_onsets = Counter()
    b_daiin_lf_total = 0
    baseline_second = Counter()
    baseline_second_total = 0

    for para in paragraphs:
        dialect = para['dialect']
        if dialect not in ('A', 'B'):
            continue

        for line in para['lines']:
            n = len(line)
            if n < 2:
                continue

            # A: daiin at LL
            if dialect == 'A':
                last_word = line[-1]
                if n >= 2:
                    penult = line[-2]
                    penult_onset = get_onset(penult)
                    baseline_penult[penult_onset] += 1
                    baseline_penult_total += 1
                    if last_word == 'daiin':
                        a_penult_onsets[penult_onset] += 1
                        a_daiin_ll_total += 1

            # B: daiin at LF (first word)
            if dialect == 'B':
                first_word = line[0]
                if n >= 2:
                    second = line[1]
                    second_onset = get_onset(second)
                    baseline_second[second_onset] += 1
                    baseline_second_total += 1
                    if first_word == 'daiin':
                        b_second_onsets[second_onset] += 1
                        b_daiin_lf_total += 1

    print(f"\nA-dialect daiin@LL cases: n={a_daiin_ll_total}")
    print(f"B-dialect daiin@LF cases: n={b_daiin_lf_total}")

    print("\n--- A: Penultimate onset BEFORE daiin@LL ---")
    print(f"{'Onset':<10} {'daiin@LL n':<12} {'daiin@LL%':<12} {'base%':<12} {'Enrichment'}")
    penult_data = []
    all_onsets = set(list(a_penult_onsets.keys()) + list(baseline_penult.keys()))
    for onset in all_onsets:
        cnt = a_penult_onsets.get(onset, 0)
        rate = cnt / a_daiin_ll_total if a_daiin_ll_total > 0 else 0
        base_cnt = baseline_penult.get(onset, 0)
        base_rate = base_cnt / baseline_penult_total if baseline_penult_total > 0 else 0
        enr = rate / base_rate if base_rate > 0 else float('inf')
        penult_data.append((onset, cnt, rate, base_rate, enr))
    penult_data.sort(key=lambda x: -x[4])
    for onset, cnt, rate, base_rate, enr in penult_data:
        if rate < 0.02 and base_rate < 0.02:
            continue
        enr_str = f"{enr:.2f}×" if enr != float('inf') else "∞"
        print(f"  {onset:<10} {cnt:<12} {rate*100:.2f}%{'':<6} {base_rate*100:.2f}%{'':<6} {enr_str}")

    # Specific penultimate words before daiin@LL in A
    a_penult_words = Counter()
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            n = len(line)
            if n >= 2 and line[-1] == 'daiin':
                a_penult_words[line[-2]] += 1

    print(f"\n  Top 10 specific penultimate words before A daiin@LL:")
    for word, cnt in a_penult_words.most_common(10):
        print(f"    {word}: {cnt}")

    print("\n--- B: Second-word onset AFTER daiin@LF ---")
    print(f"{'Onset':<10} {'daiin@LF n':<12} {'daiin@LF%':<12} {'base%':<12} {'Enrichment'}")
    second_data = []
    all_onsets2 = set(list(b_second_onsets.keys()) + list(baseline_second.keys()))
    for onset in all_onsets2:
        cnt = b_second_onsets.get(onset, 0)
        rate = cnt / b_daiin_lf_total if b_daiin_lf_total > 0 else 0
        base_cnt = baseline_second.get(onset, 0)
        base_rate = base_cnt / baseline_second_total if baseline_second_total > 0 else 0
        enr = rate / base_rate if base_rate > 0 else float('inf')
        second_data.append((onset, cnt, rate, base_rate, enr))
    second_data.sort(key=lambda x: -x[4])
    for onset, cnt, rate, base_rate, enr in second_data:
        if rate < 0.02 and base_rate < 0.02:
            continue
        enr_str = f"{enr:.2f}×" if enr != float('inf') else "∞"
        print(f"  {onset:<10} {cnt:<12} {rate*100:.2f}%{'':<6} {base_rate*100:.2f}%{'':<6} {enr_str}")

    # Specific second words after daiin@LF in B
    b_second_words = Counter()
    for para in paragraphs:
        if para['dialect'] != 'B':
            continue
        for line in para['lines']:
            n = len(line)
            if n >= 2 and line[0] == 'daiin':
                b_second_words[line[1]] += 1

    print(f"\n  Top 10 specific second words after B daiin@LF:")
    for word, cnt in b_second_words.most_common(10):
        print(f"    {word}: {cnt}")


def h368_sh_cth_bigrams(paragraphs):
    """H368: non-she sh-prefix → cth bigrams."""
    print("\n" + "=" * 70)
    print("H368: Non-she sh-prefix → cth Bigrams")
    print("=" * 70)

    sh_cth_pairs = Counter()  # (sh_word, cth_word) -> count
    sh_cth_section = []

    for para in paragraphs:
        if para['dialect'] not in ('A', 'B'):
            continue
        section = para['section']
        for line in para['lines']:
            n = len(line)
            for pos, word in enumerate(line):
                onset = get_onset(word)
                if onset == 'sh' and not (word.startswith('she') or word.startswith('shee')):
                    # non-she sh-word
                    if pos < n - 1:
                        next_word = line[pos + 1]
                        next_onset = get_onset(next_word)
                        if next_onset == 'cth':
                            sh_cth_pairs[(word, next_word)] += 1
                            sh_cth_section.append({
                                'sh_word': word,
                                'cth_word': next_word,
                                'section': section,
                                'dialect': para['dialect'],
                                'folio': para['folio']
                            })

    total_bigrams = sum(sh_cth_pairs.values())
    print(f"\nTotal non-she sh → cth bigrams: {total_bigrams}")

    print("\n--- All non-she sh → cth bigram pairs ---")
    print(f"{'sh-word':<12} {'cth-word':<12} {'n'}")
    for (sh_w, cth_w), cnt in sh_cth_pairs.most_common():
        print(f"  {sh_w:<12} {cth_w:<12} {cnt}")

    print("\n--- Section/dialect breakdown ---")
    sect_dial = Counter()
    for entry in sh_cth_section:
        sect_dial[f"{entry['dialect']}-{entry['section']}"] += 1
    for key, cnt in sect_dial.most_common():
        print(f"  {key}: {cnt}")

    print("\n--- Folio distribution ---")
    folio_count = Counter()
    for entry in sh_cth_section:
        folio_count[entry['folio']] += 1
    for folio, cnt in folio_count.most_common():
        print(f"  {folio}: {cnt}")

    # Also compute sh→cth enrichment in A vs baseline
    she_cth = 0
    nonsh_cth = 0
    she_total = 0
    nonsh_total = 0

    for para in paragraphs:
        for line in para['lines']:
            n = len(line)
            for pos, word in enumerate(line):
                onset = get_onset(word)
                if onset == 'sh' and pos < n - 1:
                    next_onset = get_onset(line[pos + 1])
                    is_she = word.startswith('she') or word.startswith('shee')
                    if is_she:
                        she_total += 1
                        if next_onset == 'cth':
                            she_cth += 1
                    else:
                        nonsh_total += 1
                        if next_onset == 'cth':
                            nonsh_cth += 1

    print(f"\n--- she- vs non-she sh → cth rate ---")
    if she_total > 0:
        print(f"  she→cth: {she_cth}/{she_total} = {she_cth/she_total:.4f} ({she_cth/she_total*100:.2f}%)")
    if nonsh_total > 0:
        print(f"  non-she-sh→cth: {nonsh_cth}/{nonsh_total} = {nonsh_cth/nonsh_total:.4f} ({nonsh_cth/nonsh_total*100:.2f}%)")
    if she_total > 0 and nonsh_total > 0:
        ratio = (nonsh_cth/nonsh_total) / (she_cth/she_total) if she_cth > 0 else float('inf')
        print(f"  non-she/she ratio: {ratio:.2f}×")


def h369_cosmo_shedy(paragraphs):
    """H369: cosmo B para-final shedy/chedy — spread or concentrated?"""
    print("\n" + "=" * 70)
    print("H369: cosmo B Para-Final shedy/chedy — Distribution")
    print("=" * 70)

    cosmo_b_paras = [p for p in paragraphs
                     if p['dialect'] == 'B' and p['section'] == 'cosmo']
    print(f"\nCosmo B paragraphs: {len(cosmo_b_paras)}")

    # Extract para-final and within-para LL words for cosmo B
    pf_words = []
    wp_ll_words = []

    for para in cosmo_b_paras:
        lines = para['lines']
        n_lines = len(lines)
        for line_idx, line in enumerate(lines):
            if len(line) < 2:
                continue
            last_word = line[-1]
            if line_idx == n_lines - 1:
                pf_words.append((last_word, para['folio']))
            else:
                wp_ll_words.append(last_word)

    pf_total = len(pf_words)
    wp_total = len(wp_ll_words)
    print(f"Cosmo B PF-LL total: {pf_total}")
    print(f"Cosmo B WP-LL total: {wp_total}")

    # Para-final word distribution
    pf_counter = Counter(w for w, _ in pf_words)
    wp_counter = Counter(wp_ll_words)

    print("\n--- All cosmo B para-final last words ---")
    print(f"{'Word':<18} {'PF-n':<6} {'PF%':<8} {'WP-n':<6} {'WP%':<8} {'Enrichment'}")
    pf_enr = []
    for word, pf_cnt in pf_counter.most_common():
        pf_rate = pf_cnt / pf_total
        wp_cnt = wp_counter.get(word, 0)
        wp_rate = wp_cnt / wp_total if wp_total > 0 else 0
        enr = pf_rate / wp_rate if wp_rate > 0 else float('inf')
        pf_enr.append((word, pf_cnt, pf_rate, wp_cnt, wp_rate, enr))
    pf_enr.sort(key=lambda x: -x[5])
    for word, pf_n, pf_r, wp_n, wp_r, enr in pf_enr:
        enr_str = f"{enr:.2f}×" if enr != float('inf') else "∞"
        print(f"  {word:<18} {pf_n:<6} {pf_r*100:.2f}%{'':<3} {wp_n:<6} {wp_r*100:.2f}%{'':<3} {enr_str}")

    # Which specific paras end with shedy or chedy?
    print("\n--- Cosmo B paras ending with shedy or chedy ---")
    for word, folio in pf_words:
        if word in ('shedy', 'chedy', 'sheedy', 'cheeddy'):
            print(f"  para in folio {folio}: ends with '{word}'")

    # Paragraph-level breakdown
    print("\n--- All cosmo B para-final words with folio ---")
    for word, folio in pf_words:
        print(f"  {folio:<8} → '{word}'")

    # WP-LL rate for shedy/chedy in cosmo B
    for target in ['shedy', 'chedy']:
        pf_cnt = pf_counter.get(target, 0)
        wp_cnt = wp_counter.get(target, 0)
        pf_rate = pf_cnt / pf_total if pf_total > 0 else 0
        wp_rate = wp_cnt / wp_total if wp_total > 0 else 0
        enr = pf_rate / wp_rate if wp_rate > 0 else float('inf')
        enr_str = f"{enr:.2f}×" if enr != float('inf') else "∞"
        print(f"\n{target}: PF={pf_cnt}/{pf_total}={pf_rate:.3f} vs WP-LL={wp_cnt}/{wp_total}={wp_rate:.3f} → enrichment={enr_str}")


def main():
    print("Loading ZL3b corpus...")
    paragraphs, folio_dialect = parse_corpus()

    a_paras = [p for p in paragraphs if p['dialect'] == 'A']
    b_paras = [p for p in paragraphs if p['dialect'] == 'B']
    print(f"Parsed {len(paragraphs)} paragraphs: A={len(a_paras)}, B={len(b_paras)}")

    h366_pol_prefix_profile(paragraphs)
    h367_daiin_pred_succ(paragraphs)
    h368_sh_cth_bigrams(paragraphs)
    h369_cosmo_shedy(paragraphs)


if __name__ == '__main__':
    main()
