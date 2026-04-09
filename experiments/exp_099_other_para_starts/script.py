"""
exp_099: "OTHER" Para-Start Word Investigation (H184) and Para-Final o-Onset Analysis (H185)

H184: What onset classes dominate the "OTHER" para-start words?
      ~54% of para-starts begin with words not in our PARA/LINE_OPEN/WEAK_PARA/MID classifier.
      Goal: identify what these words are and whether they form a recognizable positional class.

H185: Is o-onset specifically enriched at PARA-FINAL positions?
      Para-final last words are 27-35% o-onset. Is this para-specific or general line-final behavior?

H186 (bonus): What is the onset distribution of line-2 "OTHER" words within paragraphs?
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


def classify_positional_tier(word):
    """Assign morphological tier based on word onset."""
    if (word.startswith('pch') or word.startswith('psh') or
            (word.startswith('p') and len(word) >= 3)):
        return 'PARA'
    if (word.startswith('fch') or word.startswith('fsh') or
            (word.startswith('f') and len(word) >= 3)):
        return 'PARA'
    if word.startswith('ych') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('dch') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('ysh') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('dsh') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('yk') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('yt') and len(word) >= 4:
        return 'LINE_OPEN'
    if (word.startswith('tch') or word.startswith('tsh')) and len(word) >= 4:
        return 'WEAK_PARA'
    if (word.startswith('kch') or word.startswith('ksh')) and len(word) >= 4:
        return 'WEAK_PARA'
    if word.startswith('ch') and len(word) >= 3:
        return 'MID'
    if word.startswith('sh') and len(word) >= 3:
        return 'MID'
    if word.startswith('qo') and len(word) >= 4:
        return 'MID'
    return 'OTHER'


def get_onset_class(word):
    """Get broad onset class of a word."""
    for prefix in ['qo', 'pch', 'psh', 'fch', 'fsh', 'tch', 'tsh', 'kch', 'ksh',
                   'ych', 'ysh', 'yk', 'yt', 'dch', 'dsh', 'ch', 'sh']:
        if word.startswith(prefix):
            return prefix
    # Single character onset
    if word:
        return word[0]
    return 'other'


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

    # Parse into paragraph records
    paragraphs = {}  # para_id -> list of lines; each line = list of words
    current_para = None
    current_para_folio = None
    current_para_dialect = None
    current_para_section = None
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

    return paragraphs


def h184_other_para_start_investigation(paragraphs):
    """H184: What onset classes dominate OTHER para-start words?"""
    print("=" * 70)
    print("H184: 'OTHER' Para-Start Word Investigation")
    print("=" * 70)

    for dialect in ['A', 'B']:
        d_paras = {pid: p for pid, p in paragraphs.items() if p['dialect'] == dialect and p['lines']}
        print(f"\n{'='*50}")
        print(f"Dialect {dialect} — n_paragraphs={len(d_paras)}")

        # Collect para-start first words classified as OTHER
        other_ps_words = []
        para_words = []

        for pid, para in d_paras.items():
            if not para['lines']:
                continue
            first_line = para['lines'][0]
            if not first_line:
                continue
            first_word = first_line[0]
            tier = classify_positional_tier(first_word)
            para_words.append((first_word, tier, 'PS'))

            # Within-para first words
            for li, words in enumerate(para['lines'][1:], 1):
                if words:
                    wp_word = words[0]
                    wp_tier = classify_positional_tier(wp_word)
                    para_words.append((wp_word, wp_tier, 'WP'))

        ps_other = [(w, t) for w, t, pos in para_words if pos == 'PS' and t == 'OTHER']
        ps_all = [(w, t) for w, t, pos in para_words if pos == 'PS']
        wp_other = [(w, t) for w, t, pos in para_words if pos == 'WP' and t == 'OTHER']
        wp_all = [(w, t) for w, t, pos in para_words if pos == 'WP']

        print(f"\nPara-start words: {len(ps_all)}")
        print(f"  OTHER at PS: {len(ps_other)} ({len(ps_other)/len(ps_all)*100:.1f}%)")
        print(f"Within-para first words: {len(wp_all)}")
        print(f"  OTHER at WP: {len(wp_other)} ({len(wp_other)/len(wp_all)*100:.1f}%)")

        # Onset distribution for PS-OTHER words
        ps_other_onsets = Counter(get_onset_class(w) for w, t in ps_other)
        wp_other_onsets = Counter(get_onset_class(w) for w, t in wp_other)
        ps_total_onsets = Counter(get_onset_class(w) for w, t in ps_all)
        wp_total_onsets = Counter(get_onset_class(w) for w, t in wp_all)

        print(f"\n--- Onset distribution of PS-OTHER words (n={len(ps_other)}) ---")
        for onset, cnt in ps_other_onsets.most_common(15):
            ps_rate = cnt / len(ps_other)
            wp_cnt = wp_other_onsets.get(onset, 0)
            wp_rate = wp_cnt / len(wp_other) if wp_other else 0
            enrichment = ps_rate / wp_rate if wp_rate > 0 else float('inf')
            print(f"  {onset:<8} PS={cnt:4d} ({ps_rate*100:5.1f}%)  WP={wp_cnt:4d} ({wp_rate*100:5.1f}%)  enrich={enrichment:.2f}×")

        # Top PS-OTHER words
        ps_other_words = Counter(w for w, t in ps_other)
        print(f"\n--- Top PS-OTHER words (n unique={len(ps_other_words)}) ---")
        for word, cnt in ps_other_words.most_common(20):
            print(f"  {word}: {cnt}")

        # Compare PS vs WP onset distributions (all words, not just OTHER)
        print(f"\n--- ALL word onset distributions: PS vs WP enrichment ---")
        all_onsets = set(list(ps_total_onsets.keys()) + list(wp_total_onsets.keys()))
        ps_n = len(ps_all)
        wp_n = len(wp_all)
        enrichments = []
        for onset in all_onsets:
            ps_cnt = ps_total_onsets.get(onset, 0)
            wp_cnt = wp_total_onsets.get(onset, 0)
            ps_rate = ps_cnt / ps_n if ps_n > 0 else 0
            wp_rate = wp_cnt / wp_n if wp_n > 0 else 0
            enrich = ps_rate / wp_rate if wp_rate > 0 else float('inf')
            total = ps_cnt + wp_cnt
            if total >= 5:
                enrichments.append((onset, ps_cnt, ps_rate, wp_cnt, wp_rate, enrich))

        enrichments.sort(key=lambda x: -x[5])
        print(f"  {'Onset':<10} {'PS n':>6} {'PS%':>7} {'WP n':>6} {'WP%':>7} {'Enrich':>8}")
        for onset, ps_cnt, ps_rate, wp_cnt, wp_rate, enrich in enrichments[:20]:
            print(f"  {onset:<10} {ps_cnt:>6} {ps_rate*100:>6.1f}% {wp_cnt:>6} {wp_rate*100:>6.1f}% {enrich:>7.2f}×")

        # Specific investigation of o-onset at PS
        o_ps = [(w, t) for w, t, pos in para_words if pos == 'PS' and w.startswith('o')]
        o_wp = [(w, t) for w, t, pos in para_words if pos == 'WP' and w.startswith('o')]
        print(f"\n--- o-onset words at PS (n={len(o_ps)}) ---")
        o_ps_words = Counter(w for w, t in o_ps)
        for word, cnt in o_ps_words.most_common(15):
            tier = classify_positional_tier(word)
            print(f"  {word}: {cnt} (tier={tier})")
        print(f"\n--- Top o-onset words at WP (n={len(o_wp)}) ---")
        o_wp_words = Counter(w for w, t in o_wp)
        for word, cnt in o_wp_words.most_common(10):
            print(f"  {word}: {cnt}")


def h185_para_final_o_onset(paragraphs):
    """H185: Is o-onset enriched specifically at PARA-FINAL lines vs within-para line-last?"""
    print("\n" + "=" * 70)
    print("H185: Para-Final o-Onset Analysis — Paragraph-Closer Specialization?")
    print("=" * 70)

    for dialect in ['A', 'B']:
        d_paras = {pid: p for pid, p in paragraphs.items()
                   if p['dialect'] == dialect and len(p['lines']) >= 2}
        print(f"\n--- Dialect {dialect} (n_paras={len(d_paras)}) ---")

        para_final_last = []  # last word of the para-final line
        within_para_last = []  # last words of within-para lines (not para-start, not para-final)

        for pid, para in d_paras.items():
            lines = para['lines']
            n = len(lines)
            # Para-final line = last line
            if lines[-1]:
                para_final_last.append(lines[-1][-1])
            # Within-para: lines 1 to n-2 (skip line 0 = para-start, skip line n-1 = para-final)
            for li in range(1, n - 1):
                if lines[li]:
                    within_para_last.append(lines[li][-1])

        def onset_rate(words, prefix):
            if not words:
                return 0, 0
            n = sum(1 for w in words if w.startswith(prefix))
            return n, n / len(words)

        print(f"\n  Para-final last words: {len(para_final_last)}")
        print(f"  Within-para line-last words: {len(within_para_last)}")

        # Compare o-onset, d-onset, ch-onset, qo-onset rates
        print(f"\n  {'Prefix':<10} {'PF_n':>6} {'PF%':>7} {'WP_n':>6} {'WP%':>7} {'Enrich':>8}")
        for prefix in ['o', 'd', 'ch', 'sh', 'qo', 'y', 'p', 'k', 't', 'a', 's']:
            pf_n, pf_rate = onset_rate(para_final_last, prefix)
            wp_n, wp_rate = onset_rate(within_para_last, prefix)
            enrich = pf_rate / wp_rate if wp_rate > 0 else float('inf')
            if pf_n + wp_n >= 5:
                print(f"  {prefix:<10} {pf_n:>6} {pf_rate*100:>6.1f}% {wp_n:>6} {wp_rate*100:>6.1f}% {enrich:>7.2f}×")

        # Top para-final last words
        pf_counter = Counter(para_final_last)
        print(f"\n  Top para-final last words:")
        for w, cnt in pf_counter.most_common(15):
            wp_cnt = sum(1 for x in within_para_last if x == w)
            wp_rate = wp_cnt / len(within_para_last) if within_para_last else 0
            pf_rate = cnt / len(para_final_last) if para_final_last else 0
            enrich = pf_rate / wp_rate if wp_rate > 0 else float('inf')
            print(f"    {w}: PF={cnt} ({pf_rate*100:.1f}%), WP={wp_cnt} ({wp_rate*100:.1f}%), enrich={enrich:.2f}×")


def h186_other_para_start_by_section(paragraphs):
    """H186: Are OTHER para-starts section-specific?"""
    print("\n" + "=" * 70)
    print("H186: 'OTHER' Para-Start Words by Section")
    print("=" * 70)

    # For each section, what fraction of PS words are OTHER? What are the top OTHER PS words?
    section_ps_other = defaultdict(list)
    section_ps_all = defaultdict(list)

    for pid, para in paragraphs.items():
        if not para['lines']:
            continue
        first_line = para['lines'][0]
        if not first_line:
            continue
        section = para['section']
        dialect = para['dialect']
        first_word = first_line[0]
        tier = classify_positional_tier(first_word)
        key = f"{dialect}_{section}"
        section_ps_all[key].append((first_word, tier))
        if tier == 'OTHER':
            section_ps_other[key].append(first_word)

    print(f"\n{'Section':<20} {'n_PS':>6} {'OTHER%':>8} {'Top OTHER words'}")
    for key in sorted(section_ps_all.keys()):
        all_words = section_ps_all[key]
        other_words = section_ps_other.get(key, [])
        other_pct = len(other_words) / len(all_words) * 100 if all_words else 0
        top = Counter(other_words).most_common(5)
        top_str = ', '.join(f"{w}({n})" for w, n in top)
        print(f"  {key:<18} {len(all_words):>6} {other_pct:>7.1f}%  {top_str}")


def h184_extended_onset_analysis(paragraphs):
    """Extended: compute enrichment for ALL onset patterns at PS vs WP."""
    print("\n" + "=" * 70)
    print("H184 Extended: Para-Start Onset Enrichment for ALL Patterns")
    print("=" * 70)

    for dialect in ['A', 'B']:
        d_paras = {pid: p for pid, p in paragraphs.items() if p['dialect'] == dialect and p['lines']}
        print(f"\n--- Dialect {dialect} ---")

        ps_words = []
        wp_words = []

        for pid, para in d_paras.items():
            lines = para['lines']
            if not lines:
                continue
            # Para-start first word
            if lines[0]:
                ps_words.append(lines[0][0])
            # Within-para first words
            for li in range(1, len(lines)):
                if lines[li]:
                    wp_words.append(lines[li][0])

        # Two-character onset enrichment
        ps_2char = Counter(w[:2] for w in ps_words if len(w) >= 2)
        wp_2char = Counter(w[:2] for w in wp_words if len(w) >= 2)

        print(f"\n  Top 2-char onset enrichments at PS vs WP (min 3 PS occurrences):")
        print(f"  {'Onset':<8} {'PS_n':>5} {'PS%':>7} {'WP_n':>5} {'WP%':>7} {'Enrich':>8}")
        enrichments = []
        ps_n = len(ps_words)
        wp_n = len(wp_words)
        for onset in set(list(ps_2char.keys()) + list(wp_2char.keys())):
            ps_cnt = ps_2char.get(onset, 0)
            wp_cnt = wp_2char.get(onset, 0)
            if ps_cnt < 3:
                continue
            ps_rate = ps_cnt / ps_n
            wp_rate = wp_cnt / wp_n if wp_n > 0 else 0
            enrich = ps_rate / wp_rate if wp_rate > 0 else float('inf')
            enrichments.append((onset, ps_cnt, ps_rate, wp_cnt, wp_rate, enrich))

        enrichments.sort(key=lambda x: -x[5])
        for onset, ps_cnt, ps_rate, wp_cnt, wp_rate, enrich in enrichments[:25]:
            print(f"  {onset:<8} {ps_cnt:>5} {ps_rate*100:>6.1f}% {wp_cnt:>5} {wp_rate*100:>6.1f}% {enrich:>7.2f}×")

        # Also single-char enrichment for completeness
        ps_1char = Counter(w[0] for w in ps_words if len(w) >= 1)
        wp_1char = Counter(w[0] for w in wp_words if len(w) >= 1)
        print(f"\n  1-char onset enrichments:")
        print(f"  {'Onset':<8} {'PS_n':>5} {'PS%':>7} {'WP_n':>5} {'WP%':>7} {'Enrich':>8}")
        enrich_1 = []
        for onset in set(list(ps_1char.keys()) + list(wp_1char.keys())):
            ps_cnt = ps_1char.get(onset, 0)
            wp_cnt = wp_1char.get(onset, 0)
            if ps_cnt < 2:
                continue
            ps_rate = ps_cnt / ps_n
            wp_rate = wp_cnt / wp_n if wp_n > 0 else 0
            enrich = ps_rate / wp_rate if wp_rate > 0 else float('inf')
            enrich_1.append((onset, ps_cnt, ps_rate, wp_cnt, wp_rate, enrich))
        enrich_1.sort(key=lambda x: -x[5])
        for onset, ps_cnt, ps_rate, wp_cnt, wp_rate, enrich in enrich_1:
            print(f"  {onset:<8} {ps_cnt:>5} {ps_rate*100:>6.1f}% {wp_cnt:>5} {wp_rate*100:>6.1f}% {enrich:>7.2f}×")


def main():
    print("Loading data...")
    paragraphs = parse_voynich()
    n_a = sum(1 for p in paragraphs.values() if p['dialect'] == 'A')
    n_b = sum(1 for p in paragraphs.values() if p['dialect'] == 'B')
    print(f"Total paragraphs: {len(paragraphs)} (A={n_a}, B={n_b})")

    h184_other_para_start_investigation(paragraphs)
    h184_extended_onset_analysis(paragraphs)
    h185_para_final_o_onset(paragraphs)
    h186_other_para_start_by_section(paragraphs)


if __name__ == '__main__':
    main()
