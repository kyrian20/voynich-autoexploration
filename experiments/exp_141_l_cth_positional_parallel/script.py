#!/usr/bin/env python3
"""
exp_141: l-onset (B-dialect) vs cth-onset (A-dialect) — positional parallel? (H280)
         Are lch-words medially concentrated like cth-words?
         Do they appear in similar positional/bigram contexts?
"""

import re
from collections import Counter, defaultdict

CORPUS = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

SECTION_MAP = {}
for f in range(1, 58):    SECTION_MAP[f] = 'herbal'
for f in range(67, 74):   SECTION_MAP[f] = 'astro'
for f in range(75, 85):   SECTION_MAP[f] = 'cosmo'
for f in range(87, 103):  SECTION_MAP[f] = 'pharma'
for f in range(103, 117): SECTION_MAP[f] = 'stars'

ONSET_CLASSES = {
    "qok": re.compile(r'^qok'),
    "qot": re.compile(r'^qot'),
    "qo":  re.compile(r'^qo(?![kt])'),
    "cth": re.compile(r'^cth'),
    "ch":  re.compile(r'^ch(?!e)'),
    "ch_e":re.compile(r'^che'),
    "sh":  re.compile(r'^sh'),
    "ok":  re.compile(r'^ok'),
    "ot":  re.compile(r'^ot'),
    "ol":  re.compile(r'^ol'),
    "d":   re.compile(r'^d'),
    "s":   re.compile(r'^s'),
    "y":   re.compile(r'^y'),
    "k":   re.compile(r'^k'),
    "t":   re.compile(r'^t'),
    "l":   re.compile(r'^l'),
    "r":   re.compile(r'^r'),
    "p":   re.compile(r'^p'),
    "f":   re.compile(r'^f'),
}

SUFFIXES = ["eeedy", "eeey", "eedy", "edy", "eey", "aiin", "ain", "air",
            "am", "ol", "or", "ar", "al", "ey", "dy", "y"]


def get_onset(word):
    for name, pat in ONSET_CLASSES.items():
        if pat.match(word):
            return name
    return 'other'


def parse_corpus():
    """Parse into lines with positional info."""
    lines = []
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
            locus_type = locus_type_raw.lstrip('@+*=~&')
            if not re.match(r'P', locus_type):
                continue
            folio_base = folio_str.split('.')[0]
            m2 = re.match(r'f(\d+)', folio_base)
            if not m2:
                continue
            folio_num = int(m2.group(1))
            section = SECTION_MAP.get(folio_num)
            if section is None:
                continue
            words = [w for w in text.split('.') if re.match(r'[a-z]', w)]
            if not words:
                continue
            lines.append({
                'folio_base': folio_base,
                'folio_num': folio_num,
                'section': section,
                'words': words,
            })
    return lines


def get_folio_dialect(lines):
    folio_counts = defaultdict(lambda: {'edy': 0, 'eedy': 0, 'total': 0})
    for rec in lines:
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


def positional_slot(i, n):
    """Return positional slot for word at index i in line of n words."""
    if n == 1:
        return 'only'
    if i == 0:
        return 'LF'
    if i == n - 1:
        return 'LL'
    if n > 2 and i == 1:
        return 'second'
    return 'MID'


def analyze_positional_parallel(lines, folio_dialect):
    """Compare positional distribution of cth-words (A-dialect) vs lch-words (B-dialect)."""
    print("="*60)
    print("H280: l/cth POSITIONAL PARALLEL ANALYSIS")
    print("="*60)

    # Target word groups
    # cth-words in A-dialect sections
    # lch-words in B-dialect sections
    # Also: lk-words in B, standalone 'l' in B

    pos_counts = {
        'cth_A': Counter(),     # cth-onset in A-dialect folios
        'lch_B': Counter(),     # lch-onset in B-dialect folios
        'lk_B': Counter(),      # lk-onset in B-dialect folios
        'l_all_B': Counter(),   # all l-onset in B-dialect folios
        # Baseline: all words in respective dialect
        'all_A': Counter(),
        'all_B': Counter(),
    }

    # Word-level analysis
    word_pos = {
        'cth_A': defaultdict(Counter),   # word -> positional slot counts
        'lch_B': defaultdict(Counter),
    }

    # Bigram context
    before_cth = Counter()  # onset of word BEFORE cth-word (in A)
    after_cth = Counter()   # onset of word AFTER cth-word (in A)
    before_lch = Counter()  # onset of word BEFORE lch-word (in B)
    after_lch = Counter()   # onset of word AFTER lch-word (in B)

    total_tokens = {'cth_A': 0, 'lch_B': 0, 'lk_B': 0, 'l_all_B': 0,
                    'all_A': 0, 'all_B': 0}

    for rec in lines:
        fb = rec['folio_base']
        d = folio_dialect.get(fb, 'unknown')
        words = rec['words']
        n = len(words)

        for i, w in enumerate(words):
            slot = positional_slot(i, n)
            onset = get_onset(w)

            if d == 'A':
                pos_counts['all_A'][slot] += 1
                total_tokens['all_A'] += 1
                if onset == 'cth':
                    pos_counts['cth_A'][slot] += 1
                    total_tokens['cth_A'] += 1
                    word_pos['cth_A'][w][slot] += 1
                    if i > 0:
                        before_cth[get_onset(words[i-1])] += 1
                    if i < n-1:
                        after_cth[get_onset(words[i+1])] += 1

            elif d == 'B':
                pos_counts['all_B'][slot] += 1
                total_tokens['all_B'] += 1
                if onset == 'l':
                    pos_counts['l_all_B'][slot] += 1
                    total_tokens['l_all_B'] += 1
                    if w.startswith('lch') or w.startswith('lsh'):
                        pos_counts['lch_B'][slot] += 1
                        total_tokens['lch_B'] += 1
                        word_pos['lch_B'][w][slot] += 1
                        if i > 0:
                            before_lch[get_onset(words[i-1])] += 1
                        if i < n-1:
                            after_lch[get_onset(words[i+1])] += 1
                    elif w.startswith('lk'):
                        pos_counts['lk_B'][slot] += 1
                        total_tokens['lk_B'] += 1

    # Print positional distributions
    slots = ['LF', 'second', 'MID', 'LL', 'only']

    print(f"\n--- Positional distribution comparison ---")
    print(f"{'Slot':10s}  {'cth_A':8s}  {'lch_B':8s}  {'lk_B':8s}  {'l_all_B':8s}  {'all_A':8s}  {'all_B':8s}")

    for slot in slots:
        def pct(grp, s):
            t = total_tokens[grp]
            return f"{pos_counts[grp].get(s,0)/t:.1%}" if t > 0 else "N/A"
        print(f"  {slot:10s}  {pct('cth_A',slot):8s}  {pct('lch_B',slot):8s}  {pct('lk_B',slot):8s}  {pct('l_all_B',slot):8s}  {pct('all_A',slot):8s}  {pct('all_B',slot):8s}")

    print(f"\nTotal tokens: cth_A={total_tokens['cth_A']}, lch_B={total_tokens['lch_B']}, lk_B={total_tokens['lk_B']}, l_all_B={total_tokens['l_all_B']}, all_A={total_tokens['all_A']}, all_B={total_tokens['all_B']}")

    # Enrichment ratios vs baseline
    print(f"\n--- Enrichment vs dialect baseline ---")
    print(f"{'Slot':10s}  {'cth/A_base':12s}  {'lch/B_base':12s}  {'lk/B_base':12s}  {'l_all/B_base':14s}")
    for slot in slots:
        def enr(grp, baseline, s):
            t_g = total_tokens[grp]; t_b = total_tokens[baseline]
            if t_g == 0 or t_b == 0: return "N/A"
            r_g = pos_counts[grp].get(s, 0) / t_g
            r_b = pos_counts[baseline].get(s, 0) / t_b
            return f"{r_g/r_b:.2f}×" if r_b > 0 else "inf"
        print(f"  {slot:10s}  {enr('cth_A','all_A',slot):12s}  {enr('lch_B','all_B',slot):12s}  {enr('lk_B','all_B',slot):12s}  {enr('l_all_B','all_B',slot):14s}")

    # Per-word positional analysis for cth and lch
    print(f"\n--- Top cth-words: positional breakdown (A-dialect) ---")
    top_cth = sorted(word_pos['cth_A'].items(), key=lambda x: -sum(x[1].values()))[:10]
    print(f"{'Word':20s}  n     LF%     MID%    LL%")
    for w, cnt in top_cth:
        total = sum(cnt.values())
        lf = (cnt.get('LF',0)+cnt.get('second',0)) / total
        mid = cnt.get('MID',0) / total
        ll = cnt.get('LL',0) / total
        print(f"  {w:20s}  {total:4d}  {lf:.1%}   {mid:.1%}   {ll:.1%}")

    print(f"\n--- Top lch-words: positional breakdown (B-dialect) ---")
    top_lch = sorted(word_pos['lch_B'].items(), key=lambda x: -sum(x[1].values()))[:10]
    print(f"{'Word':20s}  n     LF%     MID%    LL%")
    for w, cnt in top_lch:
        total = sum(cnt.values())
        lf = (cnt.get('LF',0)+cnt.get('second',0)) / total
        mid = cnt.get('MID',0) / total
        ll = cnt.get('LL',0) / total
        print(f"  {w:20s}  {total:4d}  {lf:.1%}   {mid:.1%}   {ll:.1%}")

    # Bigram context comparison
    print(f"\n--- Bigram context: what onset PRECEDES cth-words (A) vs lch-words (B)? ---")
    print(f"{'Onset':10s}  {'before_cth':12s}  {'before_lch':12s}")
    all_onsets = set(list(before_cth.keys()) + list(before_lch.keys()))
    t_bcth = sum(before_cth.values()); t_blch = sum(before_lch.values())
    for onset in sorted(all_onsets,
                        key=lambda o: -(before_cth.get(o,0)/t_bcth if t_bcth>0 else 0)):
        if before_cth.get(onset,0) < 2 and before_lch.get(onset,0) < 2:
            continue
        r_cth = f"{before_cth.get(onset,0)/t_bcth:.1%}" if t_bcth > 0 else "N/A"
        r_lch = f"{before_lch.get(onset,0)/t_blch:.1%}" if t_blch > 0 else "N/A"
        print(f"  {onset:10s}  {r_cth:12s}  {r_lch:12s}")

    print(f"\n--- Bigram context: what onset FOLLOWS cth-words (A) vs lch-words (B)? ---")
    print(f"{'Onset':10s}  {'after_cth':12s}  {'after_lch':12s}")
    t_acth = sum(after_cth.values()); t_alch = sum(after_lch.values())
    all_onsets_after = set(list(after_cth.keys()) + list(after_lch.keys()))
    for onset in sorted(all_onsets_after,
                        key=lambda o: -(after_cth.get(o,0)/t_acth if t_acth>0 else 0)):
        if after_cth.get(onset,0) < 2 and after_lch.get(onset,0) < 2:
            continue
        r_cth = f"{after_cth.get(onset,0)/t_acth:.1%}" if t_acth > 0 else "N/A"
        r_lch = f"{after_lch.get(onset,0)/t_alch:.1%}" if t_alch > 0 else "N/A"
        print(f"  {onset:10s}  {r_cth:12s}  {r_lch:12s}")

    # Summary statistics: MID% and LF/LL ratio comparison
    print(f"\n--- Summary: MID% and line-final position comparison ---")
    for grp, base in [('cth_A','all_A'), ('lch_B','all_B'), ('lk_B','all_B'), ('l_all_B','all_B')]:
        t_g = total_tokens[grp]; t_b = total_tokens[base]
        if t_g == 0: continue
        mid_g = pos_counts[grp].get('MID',0) / t_g
        lf_g = (pos_counts[grp].get('LF',0) + pos_counts[grp].get('second',0)) / t_g
        ll_g = pos_counts[grp].get('LL',0) / t_g
        mid_b = pos_counts[base].get('MID',0) / t_b
        lf_b = (pos_counts[base].get('LF',0) + pos_counts[base].get('second',0)) / t_b
        ll_b = pos_counts[base].get('LL',0) / t_b
        print(f"  {grp:10s}: MID={mid_g:.1%} ({mid_g/mid_b:.2f}× base), LF={lf_g:.1%} ({lf_g/lf_b:.2f}×), LL={ll_g:.1%} ({ll_g/ll_b:.2f}×) [n={t_g}]")


if __name__ == '__main__':
    print("Loading corpus...")
    lines = parse_corpus()
    print(f"Loaded {len(lines)} lines")
    folio_dialect = get_folio_dialect(lines)
    n_a = sum(1 for d in folio_dialect.values() if d == 'A')
    n_b = sum(1 for d in folio_dialect.values() if d == 'B')
    print(f"Dialect: {n_a} A-folios, {n_b} B-folios")

    analyze_positional_parallel(lines, folio_dialect)
