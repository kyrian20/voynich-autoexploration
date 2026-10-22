#!/usr/bin/env python3
"""
exp_140: A-herbal cth vocabulary shift (H277)
         Which specific cth-words disappear in late A-herbal vs early?
         Uniform proportional reduction (scribal drift) or selective disappearance (content shift)?
         Also H278: B-dialect l-vocabulary profile for comparison.
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict
import math

CORPUS = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

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


def get_suffix(word):
    for s in SUFFIXES:
        if word.endswith(s):
            return s
    return 'other'


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
            records.append({
                'folio_base': folio_base,
                'folio_num': folio_num,
                'section': section,
                'words': words,
            })
    return records


def get_folio_dialect(records):
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


def analyze_cth_vocabulary_shift(records, folio_dialect):
    """H277: Which cth-words disappear in late A-herbal vs early?"""
    print("="*60)
    print("H277: cth VOCABULARY SHIFT — EARLY vs LATE A-HERBAL")
    print("="*60)

    # Define three periods for A-herbal
    # T1 = f1-f18, T2 = f19-f37, T3 = f38-f57 (approximate tertiles)
    cth_words = {'T1': Counter(), 'T2': Counter(), 'T3': Counter()}
    period_totals = {'T1': 0, 'T2': 0, 'T3': 0}

    for rec in records:
        fn = rec['folio_num']
        fb = rec['folio_base']
        if rec['section'] != 'herbal':
            continue
        if folio_dialect.get(fb) != 'A':
            continue
        if fn <= 18:
            period = 'T1'
        elif fn <= 37:
            period = 'T2'
        else:
            period = 'T3'
        for w in rec['words']:
            period_totals[period] += 1
            if get_onset(w) == 'cth':
                cth_words[period][w] += 1

    print(f"\nA-herbal period totals:")
    for p, tot in period_totals.items():
        cth_n = sum(cth_words[p].values())
        print(f"  {p}: {tot} words, {cth_n} cth tokens ({cth_n/tot:.3%})")

    # Get all cth-word types across all periods
    all_cth_types = set(cth_words['T1'].keys()) | set(cth_words['T2'].keys()) | set(cth_words['T3'].keys())
    print(f"\nTotal cth types across all periods: {len(all_cth_types)}")

    # Normalize to per-thousand words for fair comparison
    def rate(period, word):
        tot = period_totals[period]
        return (cth_words[period].get(word, 0) / tot * 1000) if tot > 0 else 0

    # Sort by total frequency
    all_cth_sorted = sorted(all_cth_types,
        key=lambda w: sum(cth_words[p].get(w,0) for p in ['T1','T2','T3']),
        reverse=True)

    print(f"\n--- cth-word rates per 1000 words (A-herbal only) ---")
    print(f"{'Word':20s}  {'T1(‰)':8s}  {'T2(‰)':8s}  {'T3(‰)':8s}  {'T3/T1':6s}  {'Pattern'}")
    for w in all_cth_sorted[:30]:
        r1, r2, r3 = rate('T1', w), rate('T2', w), rate('T3', w)
        ratio = (r3/r1) if r1 > 0 else float('inf') if r3 > 0 else 1.0
        # Classify pattern
        if r1 > 0 and r3 == 0:
            pattern = 'DISAPPEARS'
        elif r1 == 0 and r3 > 0:
            pattern = 'EMERGES'
        elif r3 < r1 * 0.5:
            pattern = 'DECLINES'
        elif r3 > r1 * 1.5:
            pattern = 'INCREASES'
        else:
            pattern = 'STABLE'
        print(f"  {w:20s}  {r1:8.3f}  {r2:8.3f}  {r3:8.3f}  {ratio:6.2f}  {pattern}")

    # Words absent from T3 but present in T1 (true disappearances)
    print(f"\n--- cth-words in T1 but ABSENT from T3 (complete disappearance) ---")
    disappear = [(w, cth_words['T1'][w]) for w in cth_words['T1'] if cth_words['T3'].get(w, 0) == 0]
    disappear.sort(key=lambda x: -x[1])
    for w, n in disappear:
        r1 = rate('T1', w)
        r2 = rate('T2', w)
        print(f"  {w:20s}  T1_n={n:3d}({r1:.3f}‰)  T2_n={cth_words['T2'].get(w,0):3d}({r2:.3f}‰)  T3=0")

    # Words stable from T1 to T3
    print(f"\n--- cth-words STABLE from T1 to T3 (T3/T1 ratio 0.5-2.0) ---")
    stable = []
    for w in all_cth_types:
        r1, r3 = rate('T1', w), rate('T3', w)
        if r1 > 0.1 and r3 > 0:
            ratio = r3/r1
            if 0.5 <= ratio <= 2.0:
                stable.append((w, r1, r3, ratio))
    stable.sort(key=lambda x: -x[1])
    for w, r1, r3, ratio in stable:
        print(f"  {w:20s}  T1={r1:.3f}‰  T3={r3:.3f}‰  ratio={ratio:.2f}")

    # Test for proportional vs selective: do common cth-words decline proportionally?
    print(f"\n--- Proportionality test: do ALL cth-words decline at same rate? ---")
    expected_ratio = period_totals['T1'] and period_totals['T3'] and (
        sum(cth_words['T3'].values()) / period_totals['T3']) / (
        sum(cth_words['T1'].values()) / period_totals['T1'])
    print(f"  Overall cth rate T3/T1 = {expected_ratio:.3f}×")
    print(f"  (If proportional reduction: each word should decline by this factor)")
    major_words = [w for w in all_cth_sorted if cth_words['T1'].get(w, 0) >= 3]
    for w in major_words[:10]:
        r1, r3 = rate('T1', w), rate('T3', w)
        obs_ratio = r3/r1 if r1 > 0 else float('nan')
        deviation = obs_ratio / expected_ratio if expected_ratio > 0 else float('nan')
        print(f"  {w:20s}: T3/T1={obs_ratio:.2f} (expected {expected_ratio:.2f}, dev={deviation:.2f}×)")


def analyze_b_l_vocabulary(records, folio_dialect):
    """H278: B-dialect l-vocabulary profile across all B sections."""
    print("\n" + "="*60)
    print("H278: B-DIALECT l-VOCABULARY PROFILE")
    print("="*60)

    # Collect l-words by dialect and section
    b_l_by_section = defaultdict(Counter)
    a_l_words = Counter()
    all_l_words = Counter()

    for rec in records:
        fb = rec['folio_base']
        d = folio_dialect.get(fb, 'unknown')
        sec = rec['section']
        for w in rec['words']:
            if get_onset(w) == 'l':
                all_l_words[w] += 1
                if d == 'A':
                    a_l_words[w] += 1
                elif d == 'B':
                    b_l_by_section[sec][w] += 1

    # Total B l-words per section
    print(f"\nB-dialect l-words by section:")
    for sec in ['herbal', 'cosmo', 'stars', 'pharma', 'astro']:
        n = sum(b_l_by_section[sec].values())
        n_types = len(b_l_by_section[sec])
        print(f"  {sec:10s}: {n:4d} tokens, {n_types:3d} types")

    # All B l-words combined
    b_l_all = Counter()
    for sec_cnt in b_l_by_section.values():
        b_l_all.update(sec_cnt)

    print(f"\nTotal B-dialect l-words: {sum(b_l_all.values())} tokens, {len(b_l_all)} types")
    print(f"Total A-dialect l-words: {sum(a_l_words.values())} tokens, {len(a_l_words)} types")

    # Top B l-words with suffix profile
    print(f"\n--- Top B-dialect l-words ---")
    print(f"{'Word':20s}  {'n':5s}  {'suffix':8s}  {'A_cnt':6s}  {'B%':5s}")
    for w, n in b_l_all.most_common(20):
        suf = get_suffix(w)
        a_cnt = a_l_words.get(w, 0)
        total = a_cnt + n
        b_pct = n / total if total > 0 else 0
        print(f"  {w:20s}  {n:5d}  {suf:8s}  {a_cnt:6d}  {b_pct:.1%}")

    # Suffix paradigm split: A-dialect vs B-dialect l-words
    def suffix_split(word_counter):
        b_suf = {'edy','eedy','eey','eeedy','ain','aiin'}
        a_suf = {'ol','or','al','ar','y','dy'}
        a_cnt = b_cnt = other = 0
        for w, c in word_counter.items():
            s = get_suffix(w)
            if s in b_suf: b_cnt += c
            elif s in a_suf: a_cnt += c
            else: other += c
        return a_cnt, b_cnt, other

    aa, ab, ao = suffix_split(a_l_words)
    ba, bb, bo = suffix_split(b_l_all)
    at = aa+ab+ao; bt = ba+bb+bo
    print(f"\n--- Suffix paradigm split (l-onset words) ---")
    print(f"          A-suffix%   B-suffix%   other%")
    print(f"  A-dial:  {aa/at:.1%}      {ab/at:.1%}      {ao/at:.1%}  (n={at})")
    print(f"  B-dial:  {ba/bt:.1%}      {bb/bt:.1%}      {bo/bt:.1%}  (n={bt})")

    # B-exclusive l-words (not in A at all)
    b_exclusive = {w for w in b_l_all if a_l_words.get(w, 0) == 0}
    print(f"\nB-exclusive l-words (not in any A-folio): {len(b_exclusive)} types")
    for w in sorted(b_exclusive, key=lambda w: -b_l_all[w])[:15]:
        n = b_l_all[w]
        suf = get_suffix(w)
        print(f"  {w:20s}  n={n:4d}  suffix=-{suf}")

    # A-exclusive l-words
    a_exclusive = {w for w in a_l_words if b_l_all.get(w, 0) == 0}
    print(f"\nA-exclusive l-words (not in any B-folio): {len(a_exclusive)} types")
    for w in sorted(a_exclusive, key=lambda w: -a_l_words[w])[:15]:
        suf = get_suffix(w)
        print(f"  {w:20s}  n={a_l_words[w]:4d}  suffix=-{suf}")

    # lk-prefix forms specifically
    lk_forms = {w for w in all_l_words if w.startswith('lk')}
    print(f"\n--- lk-prefixed l-words (expected B-dialect markers) ---")
    for w in sorted(lk_forms, key=lambda w: -all_l_words[w])[:10]:
        a_cnt = a_l_words.get(w, 0)
        b_cnt = b_l_all.get(w, 0)
        suf = get_suffix(w)
        print(f"  {w:20s}  A={a_cnt:3d}  B={b_cnt:3d}  suffix=-{suf}")

    # Check the 3 late A-herbal clean B-forms from exp_139
    print(f"\n--- Late A-herbal clean B-form l-words (lkeedy, lkeey, loldaiin) corpus-wide ---")
    for w in ['lkeedy', 'lkeey', 'loldaiin', 'lor', 'lo', 'lchor']:
        a_cnt = a_l_words.get(w, 0)
        b_cnt = b_l_all.get(w, 0)
        suf = get_suffix(w)
        total = a_cnt + b_cnt
        b_pct = b_cnt/total if total > 0 else 0
        print(f"  {w:20s}  A={a_cnt:3d}  B={b_cnt:3d}  B%={b_pct:.1%}  suffix=-{suf}")


if __name__ == '__main__':
    print("Loading corpus...")
    records = parse_corpus()
    print(f"Loaded {len(records)} lines")
    folio_dialect = get_folio_dialect(records)

    n_a = sum(1 for d in folio_dialect.values() if d == 'A')
    n_b = sum(1 for d in folio_dialect.values() if d == 'B')
    print(f"Dialect: {n_a} A-folios, {n_b} B-folios")

    analyze_cth_vocabulary_shift(records, folio_dialect)
    analyze_b_l_vocabulary(records, folio_dialect)
