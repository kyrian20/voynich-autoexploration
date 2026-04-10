#!/usr/bin/env python3
"""
exp_139: A-herbal cth decline — smooth gradient or breakpoint? (H275)
        A-herbal l-gradient — B-vocabulary contamination or A-content shift? (H276)
"""

import re
import sys
from collections import Counter, defaultdict

CORPUS = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

SECTION_MAP = {}
for f in range(1, 58):    SECTION_MAP[f] = 'herbal'
for f in range(67, 74):   SECTION_MAP[f] = 'astro'
for f in range(75, 85):   SECTION_MAP[f] = 'cosmo'
for f in range(87, 103):  SECTION_MAP[f] = 'pharma'
for f in range(103, 117): SECTION_MAP[f] = 'stars'

# Known B-herbal folios (from F145/exp_138)
B_HERBAL_FOLIOS = {'f26r','f26v','f31r','f31v','f33r','f33v','f34r','f34v',
                   'f39r','f39v','f40r','f40v','f41r','f41v','f43r','f43v',
                   'f46r','f46v','f48r','f48v','f50r','f50v','f57r','f57v'}

import re as _re
ONSET_CLASSES = {
    "qok": _re.compile(r'^qok'),
    "qot": _re.compile(r'^qot'),
    "qo":  _re.compile(r'^qo(?![kt])'),
    "cth": _re.compile(r'^cth'),
    "ch":  _re.compile(r'^ch(?!e)'),
    "ch_e":_re.compile(r'^che'),
    "sh":  _re.compile(r'^sh'),
    "ok":  _re.compile(r'^ok'),
    "ot":  _re.compile(r'^ot'),
    "ol":  _re.compile(r'^ol'),
    "d":   _re.compile(r'^d'),
    "s":   _re.compile(r'^s'),
    "y":   _re.compile(r'^y'),
    "k":   _re.compile(r'^k'),
    "t":   _re.compile(r'^t'),
    "l":   _re.compile(r'^l'),
    "r":   _re.compile(r'^r'),
    "p":   _re.compile(r'^p'),
    "f":   _re.compile(r'^f'),
}

# B-dialect suffix markers: -edy, -eedy, -eey, -eeedy
B_SUFFIXES = {'edy','eedy','eey','eeedy','ain','aiin'}
# A-dialect suffix markers: -ol, -or, -al, -ar, -y (but not -edy)
A_SUFFIXES = {'ol','or','al','ar','y','dy'}


def parse_corpus():
    records = []
    with open(CORPUS, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^>]+)>(.*)', line)
            if not m:
                continue
            locus_raw, text = m.group(1), m.group(2).strip()
            parts = locus_raw.split(',')
            if len(parts) < 2:
                continue
            folio_str = parts[0]
            locus_type_raw = parts[1]
            # Strip prefix characters from locus_type
            locus_type = locus_type_raw.lstrip('@+*=~&')
            if not re.match(r'P', locus_type):
                continue
            folio_base = folio_str.split('.')[0]
            # Extract folio number
            m2 = re.match(r'f(\d+)', folio_base)
            if not m2:
                continue
            folio_num = int(m2.group(1))
            words = [w for w in text.split('.') if re.match(r'[a-z]', w)]
            if not words:
                continue
            records.append({
                'folio_base': folio_base,
                'folio_num': folio_num,
                'words': words,
            })
    return records


def get_onset(word):
    for name, pat in ONSET_CLASSES.items():
        if pat.match(word):
            return name
    return 'other'


def get_suffix(word):
    suffixes = ['eeedy','eeey','eedy','edy','eey','aiin','ain','air','am','ol','or','ar','al','ey','dy','y']
    for s in suffixes:
        if word.endswith(s) and len(word) > len(s):
            return s
    return 'other'


def get_folio_dialect(records):
    """Compute dialect per folio_base using edy/eedy rate >= 5%."""
    folio_counts = defaultdict(lambda: {'edy': 0, 'eedy': 0, 'total': 0})
    for rec in records:
        fb = rec['folio_base']
        for w in rec['words']:
            folio_counts[fb]['total'] += 1
            if w.endswith('eedy'):
                folio_counts[fb]['eedy'] += 1
            elif w.endswith('edy'):
                folio_counts[fb]['edy'] += 1
    dialect = {}
    for fb, cnts in folio_counts.items():
        if cnts['total'] < 10:
            dialect[fb] = 'unknown'
        else:
            rate = (cnts['edy'] + cnts['eedy']) / cnts['total']
            dialect[fb] = 'B' if rate >= 0.05 else 'A'
    return dialect


def build_folio_profiles(records):
    folio_onset = defaultdict(Counter)
    folio_words_all = defaultdict(list)
    folio_total = defaultdict(int)
    for rec in records:
        fb = rec['folio_base']
        for w in rec['words']:
            folio_onset[fb][get_onset(w)] += 1
            folio_words_all[fb].append(w)
            folio_total[fb] += 1
    return folio_onset, folio_words_all, folio_total


def spearman_rho(xs, ys):
    n = len(xs)
    if n < 3:
        return float('nan')
    rank_x = sorted(range(n), key=lambda i: xs[i])
    rank_y = sorted(range(n), key=lambda i: ys[i])
    rx = [0]*n; ry = [0]*n
    for r, i in enumerate(rank_x): rx[i] = r
    for r, i in enumerate(rank_y): ry[i] = r
    d2 = sum((rx[i]-ry[i])**2 for i in range(n))
    return 1 - 6*d2 / (n*(n*n-1))


def analyze_cth_breakpoint(records, folio_dialect):
    """H275: Is A-herbal cth decline smooth gradient or step-change?"""
    print("="*60)
    print("H275: A-HERBAL cth BREAKPOINT ANALYSIS")
    print("="*60)

    # Get A-herbal folios with cth rates
    folio_onset, _, folio_total = build_folio_profiles(records)
    herbal_a_folios = []
    for fb, total in sorted(folio_total.items(), key=lambda x: int(re.match(r'f(\d+)', x[0]).group(1))):
        m = re.match(r'f(\d+)', fb)
        if not m:
            continue
        fn = int(m.group(1))
        if SECTION_MAP.get(fn) != 'herbal':
            continue
        if folio_dialect.get(fb) != 'A':
            continue
        cth_rate = folio_onset[fb]['cth'] / total if total > 0 else 0
        l_rate = folio_onset[fb]['l'] / total if total > 0 else 0
        herbal_a_folios.append((fn, fb, cth_rate, l_rate, total))

    # Tertile analysis
    n = len(herbal_a_folios)
    t1 = herbal_a_folios[:n//3]
    t2 = herbal_a_folios[n//3:2*n//3]
    t3 = herbal_a_folios[2*n//3:]

    print(f"\nA-herbal folios: {n} total")
    print(f"Tertile 1: f{t1[0][0]}-f{t1[-1][0]} ({len(t1)} folios)")
    print(f"Tertile 2: f{t2[0][0]}-f{t2[-1][0]} ({len(t2)} folios)")
    print(f"Tertile 3: f{t3[0][0]}-f{t3[-1][0]} ({len(t3)} folios)")

    for label, tert in [('T1 (early)', t1), ('T2 (mid)', t2), ('T3 (late)', t3)]:
        total_words = sum(x[4] for x in tert)
        cth_words = sum(folio_onset[x[1]]['cth'] for x in tert)
        l_words = sum(folio_onset[x[1]]['l'] for x in tert)
        cth_rate = cth_words / total_words if total_words > 0 else 0
        l_rate = l_words / total_words if total_words > 0 else 0
        folio_range = f"f{tert[0][0]}-f{tert[-1][0]}"
        print(f"  {label} [{folio_range}]: n={total_words} words, cth={cth_rate:.3%}, l={l_rate:.3%}")

    # Change-point scan: find the folio that maximizes between-group difference
    print("\n--- Change-point scan (breakpoint maximizing |mean_cth_before - mean_cth_after|) ---")
    all_cth = [(x[0], x[2]) for x in herbal_a_folios]  # (folio_num, cth_rate)
    best_bp = None
    best_diff = 0
    for i in range(2, len(all_cth)-2):
        before = [x[1] for x in all_cth[:i]]
        after = [x[1] for x in all_cth[i:]]
        diff = abs(sum(before)/len(before) - sum(after)/len(after))
        if diff > best_diff:
            best_diff = diff
            best_bp = all_cth[i][0]
    print(f"  Best breakpoint: f{best_bp} (diff={best_diff:.4f})")

    # Show cth rate by window of 5 folios
    print("\n--- cth rate in 5-folio windows ---")
    print(f"{'Folios':20s}  cth%    l%")
    for i in range(0, len(herbal_a_folios), 5):
        window = herbal_a_folios[i:i+5]
        total_w = sum(x[4] for x in window)
        cth_w = sum(folio_onset[x[1]]['cth'] for x in window)
        l_w = sum(folio_onset[x[1]]['l'] for x in window)
        fn_range = f"f{window[0][0]}-f{window[-1][0]}"
        print(f"  {fn_range:20s}  {cth_w/total_w:.3%}  {l_w/total_w:.3%}")

    # Per-folio table
    print("\n--- Per-A-herbal-folio cth and l rates ---")
    print(f"{'Folio':8s}  {'Words':6s}  {'cth%':7s}  {'l%':6s}")
    for fn, fb, cth_r, l_r, total in herbal_a_folios:
        print(f"  f{fn:<6d}  {total:6d}  {cth_r:.3%}  {l_r:.3%}")

    # Overall Spearman
    folio_nums = [x[0] for x in herbal_a_folios]
    cth_rates = [x[2] for x in herbal_a_folios]
    l_rates = [x[3] for x in herbal_a_folios]
    rho_cth = spearman_rho(folio_nums, cth_rates)
    rho_l = spearman_rho(folio_nums, l_rates)
    print(f"\nOverall A-herbal Spearman: cth ρ={rho_cth:.3f}, l ρ={rho_l:.3f}")


def analyze_l_gradient(records, folio_dialect):
    """H276: A-herbal l-gradient — A-vocab l-forms or B-vocab l-forms?"""
    print("\n" + "="*60)
    print("H276: A-HERBAL l-GRADIENT — B-VOCABULARY CONTAMINATION?")
    print("="*60)

    folio_onset, folio_words_all, folio_total = build_folio_profiles(records)

    # Collect l-onset words from early A-herbal (f1-f28) vs late A-herbal (f29-f57)
    early_l_words = Counter()
    late_l_words = Counter()

    for rec in records:
        fb = rec['folio_base']
        fn = rec['folio_num']
        if SECTION_MAP.get(fn) != 'herbal':
            continue
        if folio_dialect.get(fb) != 'A':
            continue
        for w in rec['words']:
            if get_onset(w) == 'l':
                if fn <= 28:
                    early_l_words[w] += 1
                else:
                    late_l_words[w] += 1

    print(f"\nEarly A-herbal (f1-f28) l-words: {sum(early_l_words.values())} tokens, {len(early_l_words)} types")
    print(f"Late A-herbal (f29-f57) l-words: {sum(late_l_words.values())} tokens, {len(late_l_words)} types")

    print("\n--- Top l-words in early A-herbal ---")
    for w, c in early_l_words.most_common(15):
        suf = get_suffix(w)
        suf_class = 'B-suf' if suf in B_SUFFIXES else ('A-suf' if suf in A_SUFFIXES else 'other')
        print(f"  {w:20s}  n={c:3d}  suffix=-{suf}  [{suf_class}]")

    print("\n--- Top l-words in late A-herbal ---")
    for w, c in late_l_words.most_common(15):
        suf = get_suffix(w)
        suf_class = 'B-suf' if suf in B_SUFFIXES else ('A-suf' if suf in A_SUFFIXES else 'other')
        print(f"  {w:20s}  n={c:3d}  suffix=-{suf}  [{suf_class}]")

    # Suffix paradigm split: A-suffix vs B-suffix in early vs late l-words
    def suffix_split(word_counter):
        a_count = 0; b_count = 0; other_count = 0
        for w, c in word_counter.items():
            suf = get_suffix(w)
            if suf in B_SUFFIXES:
                b_count += c
            elif suf in A_SUFFIXES:
                a_count += c
            else:
                other_count += c
        return a_count, b_count, other_count

    ea, eb, eo = suffix_split(early_l_words)
    la, lb, lo = suffix_split(late_l_words)
    et = ea+eb+eo; lt = la+lb+lo
    print(f"\n--- Suffix paradigm split (l-onset words) ---")
    print(f"Period     A-suffix%   B-suffix%   other%")
    print(f"  Early:   {ea/et:.1%}      {eb/et:.1%}      {eo/et:.1%}  (n={et})")
    print(f"  Late:    {la/lt:.1%}      {lb/lt:.1%}      {lo/lt:.1%}  (n={lt})")

    # Check for specific B-l forms (lkeedy, lkedy etc.)
    b_l_forms = ['lkeedy','lkedy','lkeey','lkain','lkaiin','lkedy','lkam']
    print("\n--- B-dialect l-forms (lk-prefixed) in A-herbal ---")
    for form in b_l_forms:
        e_cnt = early_l_words.get(form, 0)
        l_cnt = late_l_words.get(form, 0)
        if e_cnt > 0 or l_cnt > 0:
            print(f"  {form}: early={e_cnt}, late={l_cnt}")
    # Also check for any l-words that are predominantly B-dialect corpus-wide
    print("\n--- l-words with B-type suffixes in late A-herbal ---")
    late_b_l = [(w, c) for w, c in late_l_words.items() if get_suffix(w) in B_SUFFIXES]
    late_b_l.sort(key=lambda x: -x[1])
    if late_b_l:
        for w, c in late_b_l[:10]:
            print(f"  {w:20s}  n={c}")
    else:
        print("  (none)")

    # Are late A-herbal l-words found in B-dialect sections?
    # Cross-reference with corpus-wide l-word dialect distribution
    print("\n--- Corpus-wide dialect distribution of top late A-herbal l-words ---")
    # Build corpus-wide per-word dialect counts
    word_dialect_count = defaultdict(Counter)
    for rec in records:
        fb = rec['folio_base']
        d = folio_dialect.get(fb, 'A')
        for w in rec['words']:
            if get_onset(w) == 'l':
                word_dialect_count[w][d] += 1

    print(f"{'Word':20s}  {'A_total':8s}  {'B_total':8s}  {'B%':6s}  {'Late_A_herbal':12s}")
    for w, c in late_l_words.most_common(15):
        a_cnt = word_dialect_count[w].get('A', 0)
        b_cnt = word_dialect_count[w].get('B', 0)
        total = a_cnt + b_cnt
        b_pct = b_cnt / total if total > 0 else 0
        print(f"  {w:20s}  {a_cnt:8d}  {b_cnt:8d}  {b_pct:.1%}  {c:12d}")


if __name__ == '__main__':
    print("Loading corpus...")
    records = parse_corpus()
    print(f"Loaded {len(records)} lines")
    folio_dialect = get_folio_dialect(records)

    n_a = sum(1 for fb, d in folio_dialect.items() if d == 'A')
    n_b = sum(1 for fb, d in folio_dialect.items() if d == 'B')
    print(f"Dialect: {n_a} A-folios, {n_b} B-folios")

    analyze_cth_breakpoint(records, folio_dialect)
    analyze_l_gradient(records, folio_dialect)
