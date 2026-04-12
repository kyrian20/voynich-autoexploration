"""
exp_196: Positional Grammar Structure Tests

H161: y+ch vs d+ch opener contexts — are they complementary or interchangeable?
      (y+ch vs d+ch at para-start vs within-para lines)

H171: Gallows hierarchy — is p > f > t > k consistently across sections and
      dialects for para-start rate?

H176: k-onset cross-dialect positional class — A line-distributed vs B concentrated?

H179: f+ch cross-dialect asymmetry — why does B f+ch have 0% PS?

H193: Section vs length effect on grammar strictness — within herbal A,
      do shorter paragraphs follow positional grammar less strictly?
"""

import re
from collections import Counter, defaultdict

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


def get_second_char(word):
    """Return the second character onset component (for +ch detection)."""
    w = word.lower()
    # Check if it starts with a single-char prefix followed by ch/sh/k/t
    for prefix in ['y', 'd', 'f', 'p', 't', 'k', 's', 'l', 'r']:
        if w.startswith(prefix + 'ch'):
            return (prefix, 'ch')
        if w.startswith(prefix + 'sh'):
            return (prefix, 'sh')
    return None


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


def h161_ych_dch_contexts(paragraphs):
    """H161: y+ch vs d+ch opener contexts."""
    print("=" * 70)
    print("H161: y+ch vs d+ch Opener Contexts")
    print("=" * 70)

    a_paras = {pid: p for pid, p in paragraphs.items() if p['dialect'] == 'A'}

    # Count y+ch and d+ch at PS vs within-para line-first positions
    ych_at_ps = ych_at_wp = 0
    dch_at_ps = dch_at_wp = 0
    total_ps = total_wp = 0

    # Para-start successor analysis
    ych_ps_successors = []  # onset of line 2 opener after y+ch PS
    dch_ps_successors = []  # onset of line 2 opener after d+ch PS

    # Within-para y+ch and d+ch: what follows (line-next first word)
    ych_wp_nexts = []
    dch_wp_nexts = []

    for pid, p in sorted(a_paras.items()):
        lines = p['lines']
        for i, line in enumerate(lines):
            if not line:
                continue
            first_word = line[0]
            onset = get_onset(first_word)
            prefix_ch = get_second_char(first_word)

            is_ych = (first_word.startswith('y') and len(first_word) >= 3 and
                      (first_word[1:3] == 'ch' or first_word[1:3] == 'sh'))
            is_dch = (first_word.startswith('d') and len(first_word) >= 3 and
                      (first_word[1:3] == 'ch' or first_word[1:3] == 'sh'))

            if i == 0:
                total_ps += 1
                if is_ych:
                    ych_at_ps += 1
                    if len(lines) > 1 and lines[1]:
                        ych_ps_successors.append(get_onset(lines[1][0]))
                if is_dch:
                    dch_at_ps += 1
                    if len(lines) > 1 and lines[1]:
                        dch_ps_successors.append(get_onset(lines[1][0]))
            else:
                total_wp += 1
                if is_ych:
                    ych_at_wp += 1
                    if i + 1 < len(lines) and lines[i+1]:
                        ych_wp_nexts.append(get_onset(lines[i+1][0]))
                if is_dch:
                    dch_at_wp += 1
                    if i + 1 < len(lines) and lines[i+1]:
                        dch_wp_nexts.append(get_onset(lines[i+1][0]))

    print(f"\nA-dialect: total_ps={total_ps}, total_wp={total_wp}")
    print(f"\ny+ch at para-start: {ych_at_ps}/{total_ps} = {ych_at_ps/total_ps:.2%}")
    print(f"y+ch at within-para LF: {ych_at_wp}/{total_wp} = {ych_at_wp/total_wp:.2%}")
    if total_wp and ych_at_wp > 0:
        print(f"  PS enrichment for y+ch: {(ych_at_ps/total_ps)/(ych_at_wp/total_wp):.2f}×")

    print(f"\nd+ch at para-start: {dch_at_ps}/{total_ps} = {dch_at_ps/total_ps:.2%}")
    print(f"d+ch at within-para LF: {dch_at_wp}/{total_wp} = {dch_at_wp/total_wp:.2%}")
    if total_wp and dch_at_wp > 0:
        print(f"  PS enrichment for d+ch: {(dch_at_ps/total_ps)/(dch_at_wp/total_wp):.2f}×")

    # What FOLLOWS y+ch vs d+ch at PS (line 2 opener)
    print(f"\nLine 2 onset after y+ch para-starts (n={len(ych_ps_successors)}):")
    for onset, cnt in Counter(ych_ps_successors).most_common(8):
        print(f"  {onset}: {cnt} ({cnt/len(ych_ps_successors):.1%})")

    print(f"\nLine 2 onset after d+ch para-starts (n={len(dch_ps_successors)}):")
    for onset, cnt in Counter(dch_ps_successors).most_common(8):
        print(f"  {onset}: {cnt} ({cnt/len(dch_ps_successors):.1%})")

    # Within-para: what follows y+ch vs d+ch line-openers (next line's first word)
    baseline_wp = []
    for pid, p in sorted(a_paras.items()):
        lines = p['lines']
        for i in range(len(lines) - 1):
            if lines[i] and lines[i+1]:
                baseline_wp.append(get_onset(lines[i+1][0]))
    total_base = len(baseline_wp)

    print(f"\nWithin-para: next-line onset after y+ch lines (n={len(ych_wp_nexts)}) vs baseline (n={total_base}):")
    baseline_counts = Counter(baseline_wp)
    for onset in ['y', 'd', 'ch', 'sh', 'ok', 'o', 'p', 'k', 't']:
        ych_rate = ych_wp_nexts.count(onset) / len(ych_wp_nexts) if ych_wp_nexts else 0
        dch_rate = dch_wp_nexts.count(onset) / len(dch_wp_nexts) if dch_wp_nexts else 0
        base_rate = baseline_counts.get(onset, 0) / total_base
        print(f"  {onset:<4}: after y+ch={ych_rate:.1%} ({(ych_rate/base_rate):.2f}×base), "
              f"after d+ch={dch_rate:.1%} ({(dch_rate/base_rate):.2f}×base), base={base_rate:.1%}")

    # Complementarity test: same paragraph, do y+ch and d+ch alternate?
    print("\nWithin same paragraph: y+ch and d+ch co-occurrence:")
    both_in_same = same_y_only = same_d_only = neither = 0
    for pid, p in sorted(a_paras.items()):
        has_ych = any(line and line[0].startswith('y') and len(line[0]) >= 3
                      and line[0][1:3] in ('ch', 'sh')
                      for line in p['lines'])
        has_dch = any(line and line[0].startswith('d') and len(line[0]) >= 3
                      and line[0][1:3] in ('ch', 'sh')
                      for line in p['lines'])
        if has_ych and has_dch:
            both_in_same += 1
        elif has_ych:
            same_y_only += 1
        elif has_dch:
            same_d_only += 1
        else:
            neither += 1

    total_paras = len(a_paras)
    print(f"  Both y+ch and d+ch: {both_in_same}/{total_paras} = {both_in_same/total_paras:.1%}")
    print(f"  y+ch only: {same_y_only}/{total_paras} = {same_y_only/total_paras:.1%}")
    print(f"  d+ch only: {same_d_only}/{total_paras} = {same_d_only/total_paras:.1%}")
    print(f"  Neither: {neither}/{total_paras} = {neither/total_paras:.1%}")


def h171_gallows_hierarchy(paragraphs):
    """H171: Gallows hierarchy consistency across sections."""
    print("\n" + "=" * 70)
    print("H171: Gallows Hierarchy (p > f > t > k) Across Sections")
    print("=" * 70)

    gallows = ['p', 'f', 't', 'k']
    sections = ['herbal', 'pharma', 'cosmo', 'stars', 'astro']

    for dialect in ['A', 'B']:
        print(f"\n--- Dialect {dialect} ---")
        d_paras = {pid: p for pid, p in paragraphs.items() if p['dialect'] == dialect}

        print(f"{'Section':<10} {'n_PS':>6}", end='')
        for g in gallows:
            print(f" {'bare_'+g:>10}", end='')
        print()
        print('-' * 55)

        # Overall
        all_ps_words = []
        all_wp_words = []
        for pid, p in d_paras.items():
            lines = p['lines']
            if lines and lines[0]:
                all_ps_words.append(lines[0][0])
            for i in range(1, len(lines)):
                if lines[i]:
                    all_wp_words.append(lines[i][0])

        n_ps = len(all_ps_words)
        print(f"{'OVERALL':<10} {n_ps:>6}", end='')
        for g in gallows:
            bare_g_count = sum(1 for w in all_ps_words if w == g)
            rate = bare_g_count / n_ps if n_ps else 0
            print(f" {rate:>10.2%}", end='')
        print()

        for section in sections:
            sec_paras = {pid: p for pid, p in d_paras.items() if p['section'] == section}
            ps_words = []
            for pid, p in sec_paras.items():
                if p['lines'] and p['lines'][0]:
                    ps_words.append(p['lines'][0][0])

            n = len(ps_words)
            if n < 5:
                continue

            print(f"{section:<10} {n:>6}", end='')
            for g in gallows:
                bare_g_count = sum(1 for w in ps_words if w == g)
                rate = bare_g_count / n if n else 0
                print(f" {rate:>10.2%}", end='')
            print()

    # Also test: gallows+ch at para-starts
    print("\n--- Gallows+ch at para-starts (overall) ---")
    for dialect in ['A', 'B']:
        d_paras = {pid: p for pid, p in paragraphs.items() if p['dialect'] == dialect}
        ps_words = []
        for pid, p in d_paras.items():
            if p['lines'] and p['lines'][0]:
                ps_words.append(p['lines'][0][0])

        n_ps = len(ps_words)
        print(f"\nDialect {dialect} (n_PS={n_ps}):")
        for g in gallows:
            gch_count = sum(1 for w in ps_words if w.startswith(g + 'ch') or w.startswith(g + 'sh'))
            bare_count = sum(1 for w in ps_words if w == g)
            print(f"  {g}+ch: {gch_count}/{n_ps} = {gch_count/n_ps:.2%}; bare_{g}: {bare_count}/{n_ps} = {bare_count/n_ps:.2%}")


def h176_k_onset_crossdialect(paragraphs):
    """H176: k-onset positional class A vs B."""
    print("\n" + "=" * 70)
    print("H176: k-onset Positional Profile A vs B")
    print("=" * 70)

    for dialect in ['A', 'B']:
        d_paras = {pid: p for pid, p in paragraphs.items() if p['dialect'] == dialect}

        k_at_lf = k_at_ll = k_at_mid = 0
        k_at_ps = k_at_wp = 0
        total_k = 0
        total_ps = total_wp_lf = 0

        for pid, p in d_paras.items():
            lines = p['lines']
            for i, line in enumerate(lines):
                if not line:
                    continue
                if i == 0:
                    total_ps += 1
                else:
                    total_wp_lf += 1

                # First word (LF)
                if get_onset(line[0]) == 'k':
                    k_at_lf += 1
                    total_k += 1
                    if i == 0:
                        k_at_ps += 1
                    else:
                        k_at_wp += 1

                # LL
                if len(line) >= 2 and get_onset(line[-1]) == 'k':
                    k_at_ll += 1
                    total_k += 1

                # MID
                for j in range(1, len(line) - 1):
                    if get_onset(line[j]) == 'k':
                        k_at_mid += 1
                        total_k += 1

        if total_k > 0:
            print(f"\nDialect {dialect}: total k-onset words = {total_k}")
            print(f"  LF: {k_at_lf} ({k_at_lf/total_k:.1%})")
            print(f"  LL: {k_at_ll} ({k_at_ll/total_k:.1%})")
            print(f"  MID: {k_at_mid} ({k_at_mid/total_k:.1%})")
            print(f"  LF at PS (para-start): {k_at_ps}/{total_ps} = {k_at_ps/total_ps:.2%}")
            print(f"  LF at within-para: {k_at_wp}/{total_wp_lf} = {k_at_wp/total_wp_lf:.2%}")
            if total_wp_lf > 0 and k_at_wp > 0:
                print(f"  PS enrichment: {(k_at_ps/total_ps)/(k_at_wp/total_wp_lf):.2f}×")

        # k-word breakdown
        k_words_lf = []
        for pid, p in d_paras.items():
            for line in p['lines']:
                if line and get_onset(line[0]) == 'k':
                    k_words_lf.append(line[0])

        print(f"  Top k-onset words at LF:")
        for word, cnt in Counter(k_words_lf).most_common(8):
            print(f"    {word}: {cnt}")


def h179_fch_asymmetry(paragraphs):
    """H179: f+ch cross-dialect asymmetry."""
    print("\n" + "=" * 70)
    print("H179: f+ch Cross-Dialect Asymmetry")
    print("=" * 70)

    for dialect in ['A', 'B']:
        d_paras = {pid: p for pid, p in paragraphs.items() if p['dialect'] == dialect}

        fch_at_ps = 0
        fch_at_wp = 0
        total_ps = 0
        total_wp = 0
        fch_positions = []  # (word, position: 'LF'/'LL'/'MID', is_ps)
        fch_section_counts = Counter()

        for pid, p in d_paras.items():
            lines = p['lines']
            for i, line in enumerate(lines):
                if not line:
                    continue
                if i == 0:
                    total_ps += 1
                else:
                    total_wp += 1

                for j, w in enumerate(line):
                    if w.startswith('f') and len(w) >= 3 and (w[1:3] == 'ch' or w[1:3] == 'sh'):
                        if j == 0:
                            pos = 'LF'
                            if i == 0:
                                fch_at_ps += 1
                            else:
                                fch_at_wp += 1
                        elif j == len(line) - 1:
                            pos = 'LL'
                        else:
                            pos = 'MID'
                        fch_positions.append((w, pos, i == 0, p['section']))
                        fch_section_counts[p['section']] += 1

        total_fch = len(fch_positions)
        lf_count = sum(1 for _, pos, _, _ in fch_positions if pos == 'LF')
        ll_count = sum(1 for _, pos, _, _ in fch_positions if pos == 'LL')
        mid_count = sum(1 for _, pos, _, _ in fch_positions if pos == 'MID')

        print(f"\nDialect {dialect}: total f+ch words = {total_fch}")
        if total_fch > 0:
            print(f"  LF: {lf_count} ({lf_count/total_fch:.1%})")
            print(f"  LL: {ll_count} ({ll_count/total_fch:.1%})")
            print(f"  MID: {mid_count} ({mid_count/total_fch:.1%})")
            print(f"  LF at PS: {fch_at_ps}/{total_ps} = {fch_at_ps/total_ps:.2%}")
            print(f"  LF at within-para: {fch_at_wp}/{total_wp} = {fch_at_wp/total_wp:.2%}")

            print(f"  Section distribution:")
            for sect, cnt in fch_section_counts.most_common():
                print(f"    {sect}: {cnt}")

            print(f"  Top f+ch words:")
            word_counts = Counter(w for w, _, _, _ in fch_positions)
            for word, cnt in word_counts.most_common(10):
                print(f"    {word}: {cnt}")


def h193_section_vs_length(paragraphs):
    """H193: Section vs length effect on grammar strictness."""
    print("\n" + "=" * 70)
    print("H193: Section vs Length Effect on Grammar Strictness")
    print("=" * 70)

    a_paras = {pid: p for pid, p in paragraphs.items() if p['dialect'] == 'A'}

    # Grammar strictness = PARA-tier rate at PS
    # (first word of para being p/k/t/f-onset)
    def is_para_tier(word):
        return get_onset(word) in ('p', 'k', 't', 'f')

    # Overall per-section analysis
    print("\nPARA-tier rate at PS by section (A-dialect):")
    print(f"{'Section':<12} {'n_PS':>6} {'PARA%':>8} {'long%':>8} {'short%':>8}")
    print('-' * 45)

    sections = ['herbal', 'pharma', 'cosmo', 'stars', 'astro']
    for section in sections:
        sec_paras = {pid: p for pid, p in a_paras.items() if p['section'] == section}
        n_ps = len(sec_paras)
        if n_ps < 3:
            continue

        para_tier_ps = sum(1 for p in sec_paras.values()
                          if p['lines'] and p['lines'][0] and is_para_tier(p['lines'][0][0]))
        rate = para_tier_ps / n_ps if n_ps else 0

        # Length split within section
        lengths = [len(p['lines']) for p in sec_paras.values()]
        median_len = sorted(lengths)[len(lengths)//2]
        long_ps = sum(1 for p in sec_paras.values() if len(p['lines']) >= median_len
                     and p['lines'] and p['lines'][0] and is_para_tier(p['lines'][0][0]))
        long_n = sum(1 for p in sec_paras.values() if len(p['lines']) >= median_len)
        short_ps = sum(1 for p in sec_paras.values() if len(p['lines']) < median_len
                      and p['lines'] and p['lines'][0] and is_para_tier(p['lines'][0][0]))
        short_n = sum(1 for p in sec_paras.values() if len(p['lines']) < median_len)

        long_rate = long_ps / long_n if long_n else 0
        short_rate = short_ps / short_n if short_n else 0

        print(f"{section:<12} {n_ps:>6} {rate:>8.1%} {long_rate:>8.1%} {short_rate:>8.1%}")

    # Within herbal A: fine-grained length vs PS grammar
    print(f"\nHerbal A: para length vs PARA-tier at PS:")
    herbal_paras = {pid: p for pid, p in a_paras.items() if p['section'] == 'herbal'}
    length_groups = Counter()
    para_tier_in_group = Counter()
    for pid, p in herbal_paras.items():
        n_lines = len(p['lines'])
        if n_lines <= 5:
            group = 'short(≤5)'
        elif n_lines <= 10:
            group = 'medium(6-10)'
        elif n_lines <= 20:
            group = 'long(11-20)'
        else:
            group = 'very_long(21+)'

        length_groups[group] += 1
        if p['lines'] and p['lines'][0] and is_para_tier(p['lines'][0][0]):
            para_tier_in_group[group] += 1

    for group in ['short(≤5)', 'medium(6-10)', 'long(11-20)', 'very_long(21+)']:
        n = length_groups[group]
        pt = para_tier_in_group[group]
        rate = pt / n if n else 0
        print(f"  {group:<20}: {n:>4} paras, PARA% at PS = {rate:.2%}")

    # Pharma A comparison
    print(f"\nPharma A: para length vs PARA-tier at PS:")
    pharma_paras = {pid: p for pid, p in a_paras.items() if p['section'] == 'pharma'}
    pharma_length_groups = Counter()
    pharma_pt = Counter()
    for pid, p in pharma_paras.items():
        n_lines = len(p['lines'])
        if n_lines <= 5:
            group = 'short(≤5)'
        elif n_lines <= 10:
            group = 'medium(6-10)'
        elif n_lines <= 20:
            group = 'long(11-20)'
        else:
            group = 'very_long(21+)'
        pharma_length_groups[group] += 1
        if p['lines'] and p['lines'][0] and is_para_tier(p['lines'][0][0]):
            pharma_pt[group] += 1

    for group in ['short(≤5)', 'medium(6-10)', 'long(11-20)', 'very_long(21+)']:
        n = pharma_length_groups[group]
        pt = pharma_pt[group]
        rate = pt / n if n else 0
        print(f"  {group:<20}: {n:>4} paras, PARA% at PS = {rate:.2%}")


def main():
    print("Loading corpus...")
    paragraphs, folio_dialect = parse_voynich()
    total = len(paragraphs)
    a = sum(1 for p in paragraphs.values() if p['dialect'] == 'A')
    b = sum(1 for p in paragraphs.values() if p['dialect'] == 'B')
    print(f"Total paragraphs: {total} (A={a}, B={b})")

    h161_ych_dch_contexts(paragraphs)
    h171_gallows_hierarchy(paragraphs)
    h176_k_onset_crossdialect(paragraphs)
    h179_fch_asymmetry(paragraphs)
    h193_section_vs_length(paragraphs)


if __name__ == '__main__':
    main()
