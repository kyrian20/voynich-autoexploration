"""
exp_107: Universal A/B Suffix Paradigm (H205) + s-Onset Grammar (H206)

H205: Does the A:-ol/-or vs B:-edy/-eedy paradigm split apply to ALL onset classes?
H206: Is s-onset a distinct grammatical class parallel to d-onset?
      Are saiin/sain true line-openers in the s-onset system?
"""

import re
import math
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

            for pos, w in enumerate(words):
                records.append({
                    'dialect': dialect,
                    'section': section,
                    'folio': fb,
                    'word': w,
                    'is_para_start': is_para_start and pos == 0,
                    'is_line_first': pos == 0,
                    'is_line_last': pos == len(words) - 1,
                    'pos': pos,
                })

    return records


def get_suffix(word):
    """Extract suffix from word for paradigm analysis."""
    for suf in ['eedy', 'edy', 'eey', 'aiin', 'ain', 'ey', 'ol', 'or', 'dy', 'al', 'ar', 'y', 'n', 'r', 'l']:
        if word.endswith(suf) and len(word) > len(suf):
            return suf
    return 'other'


def get_onset_class(word):
    """Classify word onset into major classes."""
    if word.startswith('pch') or word.startswith('psh'):
        return 'p+gallows'
    if word.startswith('fch') or word.startswith('fsh'):
        return 'f+gallows'
    if word.startswith('tch') or word.startswith('tsh'):
        return 'tk+gallows (weak)'
    if word.startswith('kch') or word.startswith('ksh'):
        return 'tk+gallows (weak)'
    if word.startswith('dch') or word.startswith('dsh'):
        return 'd+gallows'
    if word.startswith('ych') or word.startswith('ysh'):
        return 'y+gallows'
    if word.startswith('yk') or word.startswith('yt'):
        return 'y+gallows'
    if word.startswith('p') and len(word) >= 3:
        return 'bare_p'
    if word.startswith('f') and len(word) >= 3:
        return 'bare_f'
    if word.startswith('k') and len(word) >= 2:
        return 'bare_k'
    if word.startswith('t') and len(word) >= 2:
        return 'bare_t'
    if word.startswith('ch') and len(word) >= 3:
        return 'bare_ch'
    if word.startswith('sh') and len(word) >= 3:
        return 'bare_sh'
    if word.startswith('qo') and len(word) >= 4:
        return 'qo+stem'
    if word.startswith('ok'):
        return 'o+k'
    if word.startswith('ot'):
        return 'o+t'
    if word.startswith('ol') and len(word) >= 3:
        return 'o+l'
    if word.startswith('d') and len(word) >= 2:
        return 'bare_d'
    if word.startswith('s') and len(word) >= 2:
        return 'bare_s'
    if word.startswith('o') and len(word) >= 3:
        return 'o+other'
    return 'other'


def h205_universal_paradigm(records):
    """H205: Is A:-ol/-or vs B:-edy/-eedy paradigm universal across all onset classes?"""
    print("=" * 70)
    print("H205: Universal A/B Suffix Paradigm Analysis")
    print("=" * 70)

    a_records = [r for r in records if r['dialect'] == 'A']
    b_records = [r for r in records if r['dialect'] == 'B']
    n_a = len(a_records)
    n_b = len(b_records)

    # For each onset class, compute suffix distribution in A and B
    onset_classes = [
        'bare_ch', 'bare_sh', 'qo+stem', 'o+k', 'o+t', 'o+l',
        'bare_p', 'bare_f', 'bare_k', 'bare_t',
        'p+gallows', 'f+gallows', 'd+gallows', 'y+gallows',
        'bare_d', 'bare_s', 'o+other'
    ]

    # Key suffix groups
    a_suffixes = ['ol', 'or', 'y', 'aiin']   # A-paradigm suffixes
    b_suffixes = ['edy', 'eedy', 'eey']       # B-paradigm suffixes

    print(f"\n{'Onset':<18} {'N_A':>6} {'N_B':>6} | A-type (ol+or+y)% | B-type (edy+eedy+eey)% | Paradigm ratio B/A")
    print(f"{'':18} {'':6} {'':6} | {'A_A%':>8} {'B_A%':>8} | {'A_B%':>9} {'B_B%':>9} | {'A_ratio':>9} {'B_ratio':>9}")
    print("-" * 100)

    results = {}
    for oc in onset_classes:
        a_oc = [r for r in a_records if get_onset_class(r['word']) == oc]
        b_oc = [r for r in b_records if get_onset_class(r['word']) == oc]
        na = len(a_oc)
        nb = len(b_oc)
        if na < 20 and nb < 20:
            continue

        def suffix_group_rate(recs, suffixes):
            n = len(recs)
            if n == 0:
                return 0
            return sum(1 for r in recs if get_suffix(r['word']) in suffixes) / n

        a_a_rate = suffix_group_rate(a_oc, a_suffixes)  # A-type suffixes in A dialect
        b_a_rate = suffix_group_rate(b_oc, a_suffixes)  # A-type suffixes in B dialect
        a_b_rate = suffix_group_rate(a_oc, b_suffixes)  # B-type suffixes in A dialect
        b_b_rate = suffix_group_rate(b_oc, b_suffixes)  # B-type suffixes in B dialect

        # Paradigm ratio: how much more B-type in B vs A
        a_ratio = a_a_rate / max(b_a_rate, 0.001)  # A-type: ratio A/B (how many more in A)
        b_ratio = b_b_rate / max(a_b_rate, 0.001)  # B-type: ratio B/A (how many more in B)

        results[oc] = {
            'na': na, 'nb': nb,
            'a_a': a_a_rate, 'b_a': b_a_rate,
            'a_b': a_b_rate, 'b_b': b_b_rate,
            'a_ratio': a_ratio, 'b_ratio': b_ratio
        }

        # Print paradigm indicator
        if a_ratio > 2 and b_ratio > 2:
            indicator = "STRONG SPLIT"
        elif (a_ratio > 1.5 or b_ratio > 1.5):
            indicator = "moderate split"
        elif na + nb < 50:
            indicator = "(small n)"
        else:
            indicator = "FLAT (no split)"

        print(f"  {oc:<18} {na:>6} {nb:>6} | "
              f"{a_a_rate*100:>7.1f}% {b_a_rate*100:>7.1f}% | "
              f"{a_b_rate*100:>8.1f}% {b_b_rate*100:>8.1f}% | "
              f"{a_ratio:>8.2f}× {b_ratio:>8.2f}×  {indicator}")

    # Detailed breakdown for key classes
    print(f"\n--- Detailed suffix distribution by onset class and dialect ---")
    key_classes = ['bare_ch', 'bare_sh', 'qo+stem', 'o+k', 'o+t', 'bare_d', 'bare_s', 'bare_p', 'bare_k']
    key_suffixes = ['edy', 'eedy', 'eey', 'ol', 'or', 'y', 'ey', 'aiin', 'ain', 'al', 'ar', 'other']

    for oc in key_classes:
        a_oc = [r for r in a_records if get_onset_class(r['word']) == oc]
        b_oc = [r for r in b_records if get_onset_class(r['word']) == oc]
        na = len(a_oc)
        nb = len(b_oc)
        if na < 10 and nb < 10:
            continue

        print(f"\n  {oc} (A={na}, B={nb}):")
        print(f"  {'Suffix':<10} {'A_n':>6} {'A%':>7} {'B_n':>6} {'B%':>7} {'B/A':>7}")
        a_suf = Counter(get_suffix(r['word']) for r in a_oc)
        b_suf = Counter(get_suffix(r['word']) for r in b_oc)
        for suf in key_suffixes:
            a_n = a_suf.get(suf, 0)
            b_n = b_suf.get(suf, 0)
            a_rate = a_n / na if na > 0 else 0
            b_rate = b_n / nb if nb > 0 else 0
            ratio = b_rate / a_rate if a_rate > 0 else float('inf')
            ratio_s = f"{ratio:.2f}×" if ratio != float('inf') else "∞"
            if a_n + b_n < 3:
                continue
            print(f"    {suf:<10} {a_n:>6} {a_rate*100:>6.1f}% {b_n:>6} {b_rate*100:>6.1f}% {ratio_s:>7}")


def h206_s_onset_grammar(records):
    """H206: s-onset as grammatical class — parallel to d-onset?"""
    print("\n" + "=" * 70)
    print("H206: s-Onset Grammar Analysis")
    print("=" * 70)

    s_records = [r for r in records if r['word'].startswith('s') and len(r['word']) >= 2]
    d_records = [r for r in records if r['word'].startswith('d') and
                 not r['word'].startswith('dch') and not r['word'].startswith('dsh')
                 and len(r['word']) >= 2]
    all_records = records

    n_s = len(s_records)
    n_d = len(d_records)
    n_total = len(all_records)

    print(f"\nTotal body tokens: {n_total}")
    print(f"s-onset words: {n_s} ({n_s/n_total*100:.1f}%)")
    print(f"d-onset words (bare): {n_d} ({n_d/n_total*100:.1f}%)")

    # Overall positional profile comparison
    def pos_profile(recs, label):
        n = len(recs)
        if n == 0:
            return
        ps = sum(1 for r in recs if r['is_para_start']) / n
        lf = sum(1 for r in recs if r['is_line_first']) / n
        ll = sum(1 for r in recs if r['is_line_last']) / n
        return ps, lf, ll, n

    print(f"\n--- Positional profiles: s-onset vs d-onset vs all ---")
    for recs, label in [
        (s_records, "s-onset ALL"),
        ([r for r in s_records if r['dialect'] == 'A'], "s-onset A"),
        ([r for r in s_records if r['dialect'] == 'B'], "s-onset B"),
        (d_records, "d-onset ALL"),
        ([r for r in d_records if r['dialect'] == 'A'], "d-onset A"),
        ([r for r in d_records if r['dialect'] == 'B'], "d-onset B"),
        (all_records, "ALL words"),
    ]:
        r = pos_profile(recs, label)
        if r:
            ps, lf, ll, n = r
            print(f"  {label:<16}: n={n:>5}, PS={ps*100:.1f}%, LFirst={lf*100:.1f}%, LLast={ll*100:.1f}%")

    # Top s-onset words by positional role
    print(f"\n--- s-onset top words by positional role ---")
    s_word_data = defaultdict(lambda: {'n': 0, 'lf': 0, 'll': 0, 'ps': 0, 'a': 0, 'b': 0})
    for r in s_records:
        w = r['word']
        s_word_data[w]['n'] += 1
        if r['is_line_first']:
            s_word_data[w]['lf'] += 1
        if r['is_line_last']:
            s_word_data[w]['ll'] += 1
        if r['is_para_start']:
            s_word_data[w]['ps'] += 1
        if r['dialect'] == 'A':
            s_word_data[w]['a'] += 1
        else:
            s_word_data[w]['b'] += 1

    print(f"{'Word':<14} {'n':>5} {'PS%':>5} {'LF%':>6} {'LL%':>6} {'A':>5} {'B':>5} {'suf':<8}")
    for w, d in sorted(s_word_data.items(), key=lambda x: -x[1]['n'])[:30]:
        n = d['n']
        if n < 5:
            continue
        print(f"  {w:<14} {n:>5} {d['ps']/n*100:>4.0f}% {d['lf']/n*100:>5.0f}% {d['ll']/n*100:>5.0f}% "
              f"{d['a']:>5} {d['b']:>5} {get_suffix(w):<8}")

    # Compare s-openers vs d-openers
    print(f"\n--- s-openers vs d-openers comparison ---")
    # Line-openers: LFirst > 25%
    s_openers = [(w, d) for w, d in s_word_data.items() if d['n'] >= 5 and d['lf']/d['n'] > 0.25]
    d_word_data = defaultdict(lambda: {'n': 0, 'lf': 0, 'll': 0, 'ps': 0, 'a': 0, 'b': 0})
    for r in d_records:
        w = r['word']
        d_word_data[w]['n'] += 1
        if r['is_line_first']:
            d_word_data[w]['lf'] += 1
        if r['is_line_last']:
            d_word_data[w]['ll'] += 1
        if r['dialect'] == 'A':
            d_word_data[w]['a'] += 1
        else:
            d_word_data[w]['b'] += 1

    d_openers = [(w, d) for w, d in d_word_data.items() if d['n'] >= 5 and d['lf']/d['n'] > 0.25]

    print(f"\ns-openers (LFirst>25%):")
    for w, d in sorted(s_openers, key=lambda x: -x[1]['lf']/x[1]['n'])[:10]:
        n = d['n']
        print(f"  {w}({n}): LF={d['lf']/n*100:.0f}%, LL={d['ll']/n*100:.0f}%, A={d['a']}, B={d['b']}, suffix={get_suffix(w)}")

    print(f"\nd-openers (LFirst>25%):")
    for w, d in sorted(d_openers, key=lambda x: -x[1]['lf']/x[1]['n'])[:10]:
        n = d['n']
        print(f"  {w}({n}): LF={d['lf']/n*100:.0f}%, LL={d['ll']/n*100:.0f}%, A={d['a']}, B={d['b']}, suffix={get_suffix(w)}")

    # Next-word onset after s-openers vs d-openers
    print(f"\n--- What follows s-openers vs d-openers (next word onset)? ---")
    # Group by line position: words at position 0, find next word (position 1)
    # Build pos-0 → pos-1 pairs from records (sorted by line)
    line_groups = defaultdict(list)
    for r in records:
        key = (r['folio'], r.get('line_idx', 0))
        line_groups[key].append(r)

    s_next_onsets = Counter()
    d_next_onsets = Counter()

    for key, line_recs in line_groups.items():
        sorted_recs = sorted(line_recs, key=lambda x: x['pos'])
        for i, r in enumerate(sorted_recs[:-1]):
            next_word = sorted_recs[i + 1]['word']
            if r['pos'] == 0 and r['word'].startswith('s'):
                s_next_onsets[next_word[:2]] += 1
            if r['pos'] == 0 and r['word'].startswith('d') and not r['word'].startswith('dch'):
                d_next_onsets[next_word[:2]] += 1

    n_s_next = sum(s_next_onsets.values())
    n_d_next = sum(d_next_onsets.values())
    all_first_onsets = Counter(r['word'][:2] for r in records if r['is_line_first'] and r['pos'] > 0)
    # actually compute next-onset baseline from all position-1 words
    pos1_onsets = Counter()
    for key, line_recs in line_groups.items():
        sorted_recs = sorted(line_recs, key=lambda x: x['pos'])
        if len(sorted_recs) > 1:
            pos1_onsets[sorted_recs[1]['word'][:2]] += 1

    n_pos1 = sum(pos1_onsets.values())
    print(f"\nAfter s-onset position-0 word (n={n_s_next}), next onset distribution:")
    for onset, cnt in sorted(s_next_onsets.items(),
                              key=lambda x: -(x[1]/n_s_next)/(pos1_onsets.get(x[0],1)/n_pos1))[:15]:
        if cnt < 5:
            continue
        s_rate = cnt / n_s_next
        baseline = pos1_onsets.get(onset, 0) / n_pos1
        enrich = s_rate / baseline if baseline > 0 else float('inf')
        print(f"  {onset}: {cnt} ({s_rate*100:.1f}%), baseline={baseline*100:.1f}%, enrich={enrich:.2f}×")

    print(f"\nAfter d-onset position-0 word (n={n_d_next}), next onset distribution:")
    for onset, cnt in sorted(d_next_onsets.items(),
                              key=lambda x: -(x[1]/n_d_next)/(pos1_onsets.get(x[0],1)/n_pos1))[:15]:
        if cnt < 5:
            continue
        d_rate = cnt / n_d_next
        baseline = pos1_onsets.get(onset, 0) / n_pos1
        enrich = d_rate / baseline if baseline > 0 else float('inf')
        print(f"  {onset}: {cnt} ({d_rate*100:.1f}%), baseline={baseline*100:.1f}%, enrich={enrich:.2f}×")

    # Suffix distribution of s-onset
    print(f"\n--- s-onset suffix distribution (vs d-onset) ---")
    s_suffixes = Counter(get_suffix(r['word']) for r in s_records)
    d_suffixes = Counter(get_suffix(r['word']) for r in d_records)
    all_suffixes = Counter(get_suffix(r['word']) for r in all_records)

    key_suf_list = ['edy', 'eedy', 'eey', 'ol', 'or', 'y', 'ey', 'aiin', 'ain', 'al', 'ar', 'other']
    print(f"{'Suffix':<10} {'s_n':>5} {'s%':>7} {'d_n':>5} {'d%':>7} {'all%':>7} | s-enrich d-enrich")
    for suf in key_suf_list:
        sn = s_suffixes.get(suf, 0)
        dn = d_suffixes.get(suf, 0)
        an = all_suffixes.get(suf, 0)
        sr = sn / n_s if n_s > 0 else 0
        dr = dn / n_d if n_d > 0 else 0
        ar = an / n_total if n_total > 0 else 0
        s_enr = sr / ar if ar > 0 else float('inf')
        d_enr = dr / ar if ar > 0 else float('inf')
        s_enr_s = f"{s_enr:.2f}×"
        d_enr_s = f"{d_enr:.2f}×"
        print(f"  {suf:<10} {sn:>5} {sr*100:>6.1f}% {dn:>5} {dr*100:>6.1f}% {ar*100:>6.1f}% | {s_enr_s:>8} {d_enr_s:>8}")

    # Dialect distribution of s-onset
    print(f"\n--- s-onset dialect and section distribution ---")
    s_a = [r for r in s_records if r['dialect'] == 'A']
    s_b = [r for r in s_records if r['dialect'] == 'B']
    n_a = sum(1 for r in records if r['dialect'] == 'A')
    n_b = sum(1 for r in records if r['dialect'] == 'B')
    print(f"  A s-onset rate: {len(s_a)/n_a*100:.1f}% (n={len(s_a)})")
    print(f"  B s-onset rate: {len(s_b)/n_b*100:.1f}% (n={len(s_b)})")

    s_sections = Counter(r['section'] for r in s_records)
    section_totals = Counter(r['section'] for r in records)
    print(f"\n  s-onset by section:")
    for sect, cnt in sorted(s_sections.items(), key=lambda x: -x[1]):
        tot = section_totals.get(sect, 0)
        print(f"    {sect}: {cnt}/{tot} ({cnt/tot*100:.1f}%)")


def main():
    print("Loading data...")
    records = parse_voynich()
    print(f"Total body tokens: {len(records)}")

    h205_universal_paradigm(records)
    h206_s_onset_grammar(records)


if __name__ == '__main__':
    main()
