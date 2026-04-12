#!/usr/bin/env python3
"""
exp_200: Cross-Dialect Word Profiles and Successor Patterns

H362: daiin cross-dialect positional profile — does daiin show LL stability like dam?
H363: B para-final closing vocabulary — which specific words close B paragraphs?
H364: p-onset WP-LF vocabulary in B — which p-onset words flood B's WP-LF?
H365: sh-prefix successor profile — is she-qo affinity specific to she- or all sh-prefix?
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
    """Parse ZL3b corpus into paragraph list using folio-level dialect assignment."""
    # First pass: compute folio dialect
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

    # Second pass: parse paragraphs
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


def h362_daiin_cross_dialect(paragraphs):
    """H362: daiin cross-dialect positional profile — does daiin show LL stability like dam?"""
    print("=" * 70)
    print("H362: daiin/dam/d-onset cross-dialect positional profiles")
    print("=" * 70)

    # For each dialect: collect positional stats per word and per onset class
    # Positions: LF (line-first), second (pos 1 in lines len>=3), LL (line-last), MID (else)
    dial_word_pos = defaultdict(lambda: defaultdict(lambda: {'lf': 0, 'mid': 0, 'll': 0, 'total': 0}))
    dial_onset_pos = defaultdict(lambda: defaultdict(lambda: {'lf': 0, 'mid': 0, 'll': 0, 'total': 0}))

    for para in paragraphs:
        dialect = para['dialect']
        if dialect not in ('A', 'B'):
            continue
        for line in para['lines']:
            n = len(line)
            if n == 0:
                continue
            for pos, word in enumerate(line):
                onset = get_onset(word)
                if pos == 0:
                    pos_cat = 'lf'
                elif pos == n - 1 and n > 1:
                    pos_cat = 'll'
                else:
                    pos_cat = 'mid'

                dial_word_pos[dialect][word][pos_cat] += 1
                dial_word_pos[dialect][word]['total'] += 1
                dial_onset_pos[dialect][onset][pos_cat] += 1
                dial_onset_pos[dialect][onset]['total'] += 1

    # Report d-onset class
    print("\n--- d-onset class positional distribution by dialect ---")
    print(f"{'Position':<10} {'A%':<12} {'A-n':<8} {'B%':<12} {'B-n'}")
    for pos_cat in ['lf', 'mid', 'll']:
        a = dial_onset_pos['A']['d']
        b = dial_onset_pos['B']['d']
        a_r = a[pos_cat] / a['total'] if a['total'] > 0 else 0
        b_r = b[pos_cat] / b['total'] if b['total'] > 0 else 0
        print(f"  {pos_cat:<10} {a_r:.3f}{'':<6} {a[pos_cat]:<8} {b_r:.3f}{'':<6} {b[pos_cat]}")

    # Report specific d-onset words
    target_words = ['daiin', 'dam', 'dy', 'dol', 'dain', 'daiin', 'dairn', 'dor', 'ds']
    seen = set()
    print("\n--- Specific d-onset word positional profiles ---")
    print(f"{'Word':<12} {'Dial':<6} {'n':<6} {'LF%':<8} {'MID%':<8} {'LL%'}")

    # Also identify top d-onset words in each dialect
    for dialect in ['A', 'B']:
        top_d = [(w, v['total']) for w, v in dial_word_pos[dialect].items()
                 if get_onset(w) == 'd']
        top_d.sort(key=lambda x: -x[1])
        for word, total in top_d[:12]:
            v = dial_word_pos[dialect][word]
            lf = v['lf'] / total
            ll = v['ll'] / total
            mid = v['mid'] / total
            key = f"{word}_{dialect}"
            if key not in seen:
                seen.add(key)
                print(f"  {word:<12} {dialect:<6} {total:<6} {lf:.3f}{'':<4} {mid:.3f}{'':<4} {ll:.3f}")

    # Cross-dialect comparison for shared d-onset words
    print("\n--- Cross-dialect comparison: d-onset words appearing in both A and B (n>=5 in each) ---")
    a_d_words = {w for w, v in dial_word_pos['A'].items()
                 if get_onset(w) == 'd' and v['total'] >= 5}
    b_d_words = {w for w, v in dial_word_pos['B'].items()
                 if get_onset(w) == 'd' and v['total'] >= 5}
    shared_d = a_d_words & b_d_words

    print(f"{'Word':<12} {'A-n':<6} {'A-LF%':<8} {'A-LL%':<8} {'B-n':<6} {'B-LF%':<8} {'B-LL%'}")
    for word in sorted(shared_d):
        a = dial_word_pos['A'][word]
        b = dial_word_pos['B'][word]
        a_lf = a['lf'] / a['total']
        a_ll = a['ll'] / a['total']
        b_lf = b['lf'] / b['total']
        b_ll = b['ll'] / b['total']
        print(f"  {word:<12} {a['total']:<6} {a_lf:.3f}{'':<4} {a_ll:.3f}{'':<4} "
              f"{b['total']:<6} {b_lf:.3f}{'':<4} {b_ll:.3f}")


def h363_b_para_final_vocab(paragraphs):
    """H363: B para-final closing vocabulary."""
    print("\n" + "=" * 70)
    print("H363: B Para-Final Closing Vocabulary")
    print("=" * 70)

    pf_ll_words = Counter()   # B para-final last words
    wp_ll_words = Counter()   # B within-para last words

    b_paras = [p for p in paragraphs if p['dialect'] == 'B']
    total_pf = 0
    total_wp = 0

    for para in b_paras:
        lines = para['lines']
        n_lines = len(lines)
        for line_idx, line in enumerate(lines):
            if len(line) < 2:
                continue
            last_word = line[-1]
            if line_idx == n_lines - 1:
                pf_ll_words[last_word] += 1
                total_pf += 1
            else:
                wp_ll_words[last_word] += 1
                total_wp += 1

    print(f"\nB para-final LL: n={total_pf}")
    print(f"B within-para LL: n={total_wp}")

    # Compute per-word enrichment
    print("\n--- Top B para-final last words (sorted by enrichment, n>=1 at PF) ---")
    print(f"{'Word':<15} {'PF-n':<6} {'PF%':<8} {'WP-n':<6} {'WP%':<8} {'Enrich'}")
    pf_enrichments = []
    for word, pf_count in pf_ll_words.items():
        pf_rate = pf_count / total_pf
        wp_count = wp_ll_words.get(word, 0)
        wp_rate = wp_count / total_wp if total_wp > 0 else 0
        enrichment = pf_rate / wp_rate if wp_rate > 0 else float('inf')
        pf_enrichments.append((word, pf_count, pf_rate, wp_count, wp_rate, enrichment))

    pf_enrichments.sort(key=lambda x: -x[5])
    for word, pf_n, pf_r, wp_n, wp_r, enr in pf_enrichments[:30]:
        enr_str = f"{enr:.2f}×" if enr != float('inf') else "∞"
        print(f"  {word:<15} {pf_n:<6} {pf_r*100:.2f}%{'':<2} {wp_n:<6} {wp_r*100:.2f}%{'':<2} {enr_str}")

    # Onset distribution at B PF-LL vs WP-LL
    print("\n--- Onset distribution at B PF-LL vs WP-LL ---")
    pf_onset = Counter()
    wp_onset = Counter()
    for word, cnt in pf_ll_words.items():
        pf_onset[get_onset(word)] += cnt
    for word, cnt in wp_ll_words.items():
        wp_onset[get_onset(word)] += cnt

    all_onsets = set(list(pf_onset.keys()) + list(wp_onset.keys()))
    onset_data = []
    for onset in all_onsets:
        pf_r = pf_onset[onset] / total_pf if total_pf > 0 else 0
        wp_r = wp_onset[onset] / total_wp if total_wp > 0 else 0
        ratio = pf_r / wp_r if wp_r > 0 else float('inf')
        onset_data.append((onset, pf_onset[onset], pf_r, wp_onset[onset], wp_r, ratio))
    onset_data.sort(key=lambda x: -x[5])
    print(f"{'Onset':<10} {'PF-n':<6} {'PF%':<10} {'WP-n':<6} {'WP%':<10} {'Ratio'}")
    for onset, pf_n, pf_r, wp_n, wp_r, ratio in onset_data:
        if pf_r < 0.005 and wp_r < 0.005:
            continue
        ratio_str = f"{ratio:.2f}×" if ratio != float('inf') else "∞"
        print(f"  {onset:<10} {pf_n:<6} {pf_r*100:.2f}%{'':<4} {wp_n:<6} {wp_r*100:.2f}%{'':<4} {ratio_str}")

    # Section breakdown of B PF-LL vocab
    print("\n--- Top B PF-LL words by section ---")
    pf_by_section = defaultdict(Counter)
    pf_section_totals = defaultdict(int)

    for para in b_paras:
        lines = para['lines']
        n_lines = len(lines)
        if n_lines == 0:
            continue
        last_line = lines[-1]
        if len(last_line) < 2:
            continue
        last_word = last_line[-1]
        section = para['section']
        pf_by_section[section][last_word] += 1
        pf_section_totals[section] += 1

    for section, total in sorted(pf_section_totals.items(), key=lambda x: -x[1]):
        top5 = pf_by_section[section].most_common(5)
        top5_str = ', '.join([f"{w}({c})" for w, c in top5])
        print(f"  {section:<10} (n={total}): {top5_str}")


def h364_p_onset_wplf_vocab_b(paragraphs):
    """H364: p-onset WP-LF vocabulary in B."""
    print("\n" + "=" * 70)
    print("H364: p-Onset WP-LF Vocabulary in B")
    print("=" * 70)

    b_ps_words = Counter()
    b_wplf_words = Counter()
    b_ps_total = 0
    b_wplf_total = 0

    b_paras = [p for p in paragraphs if p['dialect'] == 'B']

    for para in b_paras:
        for line_idx, line in enumerate(para['lines']):
            if not line:
                continue
            first_word = line[0]
            if line_idx == 0:
                b_ps_words[first_word] += 1
                b_ps_total += 1
            else:
                b_wplf_words[first_word] += 1
                b_wplf_total += 1

    print(f"\nB PS total: {b_ps_total}, B WP-LF total: {b_wplf_total}")

    p_wplf = {w: c for w, c in b_wplf_words.items() if get_onset(w) == 'p'}
    p_ps = {w: c for w, c in b_ps_words.items() if get_onset(w) == 'p'}

    total_p_wplf = sum(p_wplf.values())
    total_p_ps = sum(p_ps.values())

    print(f"p-onset at B WP-LF: {total_p_wplf}/{b_wplf_total} = {total_p_wplf/b_wplf_total:.3f} ({total_p_wplf/b_wplf_total*100:.1f}%)")
    print(f"p-onset at B PS: {total_p_ps}/{b_ps_total} = {total_p_ps/b_ps_total:.3f} ({total_p_ps/b_ps_total*100:.1f}%)")

    print("\n--- Top p-onset words at B WP-LF ---")
    print(f"{'Word':<18} {'WP-LF n':<9} {'WP-LF%':<9} {'PS n':<8} {'PS%':<8} {'WP-LF/PS ratio'}")
    p_wplf_sorted = sorted(p_wplf.items(), key=lambda x: -x[1])
    for word, wplf_cnt in p_wplf_sorted[:25]:
        wplf_rate = wplf_cnt / b_wplf_total
        ps_cnt = p_ps.get(word, 0)
        ps_rate = ps_cnt / b_ps_total
        ratio = wplf_rate / ps_rate if ps_rate > 0 else float('inf')
        ratio_str = f"{ratio:.2f}×" if ratio != float('inf') else "∞ (PS=0)"
        print(f"  {word:<18} {wplf_cnt:<9} {wplf_rate*100:.2f}%{'':<4} {ps_cnt:<8} {ps_rate*100:.2f}%{'':<4} {ratio_str}")

    print("\n--- Top p-onset words at B PS ---")
    print(f"{'Word':<18} {'PS n':<9} {'PS%':<9} {'WP-LF n':<10} {'WP-LF%':<8} {'PS/WP-LF ratio'}")
    p_ps_sorted = sorted(p_ps.items(), key=lambda x: -x[1])
    for word, ps_cnt in p_ps_sorted[:25]:
        ps_rate = ps_cnt / b_ps_total
        wplf_cnt = p_wplf.get(word, 0)
        wplf_rate = wplf_cnt / b_wplf_total
        ratio = ps_rate / wplf_rate if wplf_rate > 0 else float('inf')
        ratio_str = f"{ratio:.2f}×" if ratio != float('inf') else "∞ (WP-LF=0)"
        print(f"  {word:<18} {ps_cnt:<9} {ps_rate*100:.2f}%{'':<4} {wplf_cnt:<10} {wplf_rate*100:.2f}%{'':<4} {ratio_str}")

    # Overlap analysis
    ps_set = set(p_ps.keys())
    wplf_set = set(p_wplf.keys())
    shared = ps_set & wplf_set
    ps_only = ps_set - wplf_set
    wplf_only = wplf_set - ps_set

    print(f"\n--- p-onset vocabulary overlap (B dialect) ---")
    print(f"  Total unique p-onset words across both positions: {len(ps_set | wplf_set)}")
    print(f"  At PS only (never at WP-LF): {len(ps_only)}")
    print(f"  At WP-LF only (never at PS): {len(wplf_only)}")
    print(f"  At both PS and WP-LF: {len(shared)}")
    if shared:
        top_shared = sorted(shared,
                            key=lambda w: p_ps.get(w, 0) + p_wplf.get(w, 0), reverse=True)[:10]
        print(f"  Top shared words: {', '.join(top_shared)}")
    if ps_only:
        top_ps_only = sorted(ps_only, key=lambda w: p_ps.get(w, 0), reverse=True)[:5]
        print(f"  Most frequent PS-only words: {', '.join(top_ps_only)}")
    if wplf_only:
        top_wplf_only = sorted(wplf_only, key=lambda w: p_wplf.get(w, 0), reverse=True)[:5]
        print(f"  Most frequent WP-LF-only words: {', '.join(top_wplf_only)}")


def h365_sh_successor_profile(paragraphs):
    """H365: sh-prefix successor profile — she vs non-she sh-prefix."""
    print("\n" + "=" * 70)
    print("H365: sh-Prefix Successor Profile — she- vs non-she sh-")
    print("=" * 70)

    she_successors = Counter()
    nonsh_successors = Counter()
    baseline_successors = Counter()

    she_total = 0
    nonsh_total = 0
    baseline_total = 0

    for para in paragraphs:
        if para['dialect'] not in ('A', 'B'):
            continue
        for line in para['lines']:
            n = len(line)
            for pos, word in enumerate(line):
                onset = get_onset(word)
                if pos < n - 1:
                    succ_onset = get_onset(line[pos + 1])
                    baseline_successors[succ_onset] += 1
                    baseline_total += 1

                    if onset == 'sh':
                        # she-prefix: she*, shee*
                        if word.startswith('she') or word.startswith('shee'):
                            she_successors[succ_onset] += 1
                            she_total += 1
                        else:
                            nonsh_successors[succ_onset] += 1
                            nonsh_total += 1

    print(f"\nShe-prefix tokens with successor: n={she_total}")
    print(f"Non-she sh-prefix tokens with successor: n={nonsh_total}")
    print(f"Baseline successors: n={baseline_total}")

    all_onsets = set(list(she_successors.keys()) + list(nonsh_successors.keys())
                     + list(baseline_successors.keys()))

    # Compute enrichments
    print("\n--- she-prefix successor enrichments vs baseline ---")
    print(f"{'Onset':<10} {'she-n':<8} {'she%':<8} {'base%':<8} {'Enrichment'}")
    she_data = []
    for onset in all_onsets:
        she_cnt = she_successors.get(onset, 0)
        she_rate = she_cnt / she_total if she_total > 0 else 0
        base_cnt = baseline_successors.get(onset, 0)
        base_rate = base_cnt / baseline_total if baseline_total > 0 else 0
        enr = she_rate / base_rate if base_rate > 0 else float('inf')
        she_data.append((onset, she_cnt, she_rate, base_rate, enr))
    she_data.sort(key=lambda x: -x[4])
    for onset, cnt, rate, base_rate, enr in she_data:
        if rate < 0.01 and base_rate < 0.01:
            continue
        enr_str = f"{enr:.2f}×" if enr != float('inf') else "∞"
        print(f"  {onset:<10} {cnt:<8} {rate*100:.2f}%{'':<3} {base_rate*100:.2f}%{'':<3} {enr_str}")

    print("\n--- Non-she sh-prefix successor enrichments vs baseline ---")
    print(f"{'Onset':<10} {'nsh-n':<8} {'nsh%':<8} {'base%':<8} {'Enrichment'}")
    nsh_data = []
    for onset in all_onsets:
        nsh_cnt = nonsh_successors.get(onset, 0)
        nsh_rate = nsh_cnt / nonsh_total if nonsh_total > 0 else 0
        base_cnt = baseline_successors.get(onset, 0)
        base_rate = base_cnt / baseline_total if baseline_total > 0 else 0
        enr = nsh_rate / base_rate if base_rate > 0 else float('inf')
        nsh_data.append((onset, nsh_cnt, nsh_rate, base_rate, enr))
    nsh_data.sort(key=lambda x: -x[4])
    for onset, cnt, rate, base_rate, enr in nsh_data:
        if rate < 0.01 and base_rate < 0.01:
            continue
        enr_str = f"{enr:.2f}×" if enr != float('inf') else "∞"
        print(f"  {onset:<10} {cnt:<8} {rate*100:.2f}%{'':<3} {base_rate*100:.2f}%{'':<3} {enr_str}")

    # Direct comparison: she- vs non-she-sh
    print("\n--- Direct comparison: she- vs non-she-sh successors ---")
    print(f"{'Onset':<10} {'she-n':<8} {'she%':<8} {'nsh-n':<8} {'nsh%':<8} {'she/nsh ratio'}")
    comparison_data = []
    for onset in all_onsets:
        she_cnt = she_successors.get(onset, 0)
        she_rate = she_cnt / she_total if she_total > 0 else 0
        nsh_cnt = nonsh_successors.get(onset, 0)
        nsh_rate = nsh_cnt / nonsh_total if nonsh_total > 0 else 0
        ratio = she_rate / nsh_rate if nsh_rate > 0 else float('inf')
        comparison_data.append((onset, she_cnt, she_rate, nsh_cnt, nsh_rate, ratio))
    comparison_data.sort(key=lambda x: -x[5])
    for onset, she_cnt, she_rate, nsh_cnt, nsh_rate, ratio in comparison_data:
        if she_rate < 0.01 and nsh_rate < 0.01:
            continue
        ratio_str = f"{ratio:.2f}×" if ratio != float('inf') else "∞"
        print(f"  {onset:<10} {she_cnt:<8} {she_rate*100:.2f}%{'':<3} {nsh_cnt:<8} {nsh_rate*100:.2f}%{'':<3} {ratio_str}")

    # Word-level analysis for she-prefix
    print("\n--- Most frequent she-prefix words and top-3 successor onsets ---")
    she_word_succ = defaultdict(Counter)
    she_word_n = Counter()
    nsh_word_succ = defaultdict(Counter)
    nsh_word_n = Counter()

    for para in paragraphs:
        for line in para['lines']:
            n = len(line)
            for pos, word in enumerate(line):
                onset = get_onset(word)
                if onset == 'sh':
                    if word.startswith('she') or word.startswith('shee'):
                        she_word_n[word] += 1
                        if pos < n - 1:
                            she_word_succ[word][get_onset(line[pos + 1])] += 1
                    else:
                        nsh_word_n[word] += 1
                        if pos < n - 1:
                            nsh_word_succ[word][get_onset(line[pos + 1])] += 1

    print("  she-prefix words (n>=5):")
    for word, total in she_word_n.most_common(10):
        if total < 5:
            break
        succs = she_word_succ[word]
        succ_total = sum(succs.values())
        top3 = succs.most_common(3)
        top3_str = ', '.join([f"{o}({c/succ_total:.2f})" for o, c in top3])
        print(f"    {word} (n={total}): {top3_str}")

    print("  non-she sh-prefix words (n>=5):")
    for word, total in nsh_word_n.most_common(10):
        if total < 5:
            break
        succs = nsh_word_succ[word]
        succ_total = sum(succs.values())
        top3 = succs.most_common(3)
        top3_str = ', '.join([f"{o}({c/succ_total:.2f})" for o, c in top3])
        print(f"    {word} (n={total}): {top3_str}")


def main():
    print(f"Loading ZL3b corpus...")
    paragraphs, folio_dialect = parse_corpus()

    a_paras = [p for p in paragraphs if p['dialect'] == 'A']
    b_paras = [p for p in paragraphs if p['dialect'] == 'B']
    print(f"Parsed {len(paragraphs)} paragraphs: A={len(a_paras)}, B={len(b_paras)}")

    h362_daiin_cross_dialect(paragraphs)
    h363_b_para_final_vocab(paragraphs)
    h364_p_onset_wplf_vocab_b(paragraphs)
    h365_sh_successor_profile(paragraphs)


if __name__ == '__main__':
    main()
