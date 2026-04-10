#!/usr/bin/env python3
"""
exp_118: Extended Suffix List (-am/-air) (H230) + daiin Characterization (H231)
H230: Re-analyze with -am and -air as recognized suffixes
H231: Positional profile, bigram context, and section distribution of daiin
"""

import re
import math
from collections import defaultdict, Counter

DATA = 'data/transcriptions/eva_zl3b.txt'

SECTION_MAP = {}
for f in range(1, 58): SECTION_MAP[f] = 'herbal'
for f in range(67, 74): SECTION_MAP[f] = 'astro'
for f in range(75, 85): SECTION_MAP[f] = 'cosmo'
for f in range(87, 103): SECTION_MAP[f] = 'pharma'
for f in range(103, 117): SECTION_MAP[f] = 'stars'


def get_suffix_v1(word):
    """Original suffix list"""
    for suf in ['eeedy','eeey','eedy','edy','eey','aiin','ain','ol','or','ar','al','ey','dy','y']:
        if word.endswith(suf) and len(word) > len(suf):
            return suf
    return 'other'


def get_suffix_v2(word):
    """Extended suffix list: adds -am, -air, -am, -om, -eo, -o"""
    for suf in ['eeedy','eeey','eedy','edy','eey','aiin','ain','air','am','ol','or','ar','al','ey','dy','y']:
        if word.endswith(suf) and len(word) > len(suf):
            return suf
    return 'other'


def get_onset_class(word):
    w = word
    if w.startswith('qok'): return 'qok'
    if w.startswith('qot'): return 'qot'
    if w.startswith('qo'): return 'qo'
    if w.startswith('cth'): return 'cth'
    if w.startswith('ch'): return 'ch'
    if w.startswith('sh'): return 'sh'
    if w.startswith('ok'): return 'ok'
    if w.startswith('ot'): return 'ot'
    if w.startswith('ol'): return 'ol'
    if w.startswith('olk'): return 'olk'
    if w.startswith('d'): return 'd'
    if w.startswith('s'): return 's'
    return 'other'


def shannon_entropy(counts):
    total = sum(counts.values())
    if total == 0: return 0.0
    return -sum((c/total)*math.log2(c/total) for c in counts.values() if c > 0)


def parse_eva(path):
    edy_counts = defaultdict(int)
    total_counts = defaultdict(int)
    records = []

    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or not line.startswith('<'):
                continue
            m = re.match(r'<([^>]+)>(.*)', line)
            if not m: continue
            locus_code = m.group(1)
            text = m.group(2).strip()

            comma_idx = locus_code.find(',')
            if comma_idx < 0: continue
            folio_line = locus_code[:comma_idx]
            locus_type = locus_code[comma_idx+1:]

            fm = re.match(r'f(\d+)', folio_line)
            if not fm: continue
            folio_num = int(fm.group(1))

            lm = re.match(r'f\w+\.(\d+)', folio_line)
            line_in_folio = int(lm.group(1)) if lm else 0

            prefix = ''.join(c for c in locus_type if c in '@+*=~&')
            lt = locus_type[len(prefix):]
            is_body = bool(re.match(r'P', lt))
            if not is_body: continue

            text_clean = re.sub(r'<[^>]*>', '', text)
            text_clean = re.sub(r'\[[^\]]*\]', lambda m: m.group(0)[1:-1].split(':')[0], text_clean)
            text_clean = re.sub(r'\{[^}]*\}', '', text_clean)
            text_clean = re.sub(r'@\d+;?', '', text_clean)
            text_clean = re.sub(r'<%>|<!.*?>|<\$>', '', text_clean)

            words = [w for w in re.split(r'[-.\s,]', text_clean)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words: continue

            n = len(words)
            for i, w in enumerate(words):
                for suf_check in ['edy', 'eedy']:
                    if w.endswith(suf_check):
                        edy_counts[folio_num] += 1
                total_counts[folio_num] += 1
                records.append({
                    'word': w, 'folio': folio_num,
                    'line_in_folio': line_in_folio,
                    'line_key': (folio_num, line_in_folio),
                    'pos_in_line': i,
                    'n_in_line': n,
                    'is_line_first': (i == 0),
                    'is_line_last': (i == n-1),
                    'section': SECTION_MAP.get(folio_num, 'other'),
                    'prev_word': words[i-1] if i > 0 else None,
                    'next_word': words[i+1] if i < n-1 else None,
                })

    dialect_map = {fnum: ('B' if edy_counts[fnum]/max(1,total_counts[fnum]) >= 0.05 else 'A')
                   for fnum in total_counts}
    for r in records:
        r['dialect'] = dialect_map.get(r['folio'], 'A')

    return records, dialect_map


def h230_extended_suffix(records):
    print("=" * 70)
    print("H230: Extended Suffix List Analysis (-am and -air)")
    print("=" * 70)

    body = [r for r in records if r['section'] != 'other']

    # Compare v1 vs v2 suffix coverage
    v1_counts = Counter(get_suffix_v1(r['word']) for r in body)
    v2_counts = Counter(get_suffix_v2(r['word']) for r in body)
    n_total = len(body)

    print(f"\nTotal body tokens: {n_total}")
    print(f"\n--- Coverage comparison: v1 (original) vs v2 (extended) ---")
    print(f"\n{'Suffix':<10} {'v1_n':<8} {'v1%':<8} {'v2_n':<8} {'v2%'}")

    all_suffs = sorted(set(v1_counts) | set(v2_counts),
                       key=lambda x: -max(v1_counts.get(x,0), v2_counts.get(x,0)))
    for suf in all_suffs[:20]:
        v1_n = v1_counts.get(suf, 0)
        v2_n = v2_counts.get(suf, 0)
        print(f"{suf:<10} {v1_n:<8} {100*v1_n/n_total:<8.2f} {v2_n:<8} {100*v2_n/n_total:.2f}")

    print(f"\n'other' reduced from {v1_counts['other']} ({100*v1_counts['other']/n_total:.1f}%) "
          f"to {v2_counts['other']} ({100*v2_counts['other']/n_total:.1f}%)")

    # Entropy comparison
    H_v1 = shannon_entropy(v1_counts)
    H_v2 = shannon_entropy(v2_counts)
    print(f"\nH(suffix_v1) = {H_v1:.4f} bits")
    print(f"H(suffix_v2) = {H_v2:.4f} bits")

    # Characterize -am words (using v2)
    print(f"\n--- -am suffix characterization ---")
    am_words = [(r['word'], r['section'], r['dialect']) for r in body
                if get_suffix_v2(r['word']) == 'am']
    am_count = Counter(w for w, _, _ in am_words)
    am_dialect = Counter(d for _, _, d in am_words)
    am_section = Counter(s for _, s, _ in am_words)

    print(f"Total -am tokens: {len(am_words)}")
    print(f"Dialect split: A={am_dialect.get('A',0)}, B={am_dialect.get('B',0)} "
          f"(A/B ratio={am_dialect.get('A',0)/max(1,am_dialect.get('B',0)):.2f})")
    print(f"\nSection distribution:")
    all_section = Counter(r['section'] for r in body)
    for s in ['herbal','cosmo','stars','pharma','astro']:
        s_n = am_section.get(s,0)
        total_s = all_section.get(s,0)
        print(f"  {s}: {s_n} ({100*s_n/max(1,total_s):.1f}‰ of section tokens)")

    print(f"\nTop -am words (by frequency):")
    for w, c in am_count.most_common(15):
        print(f"  {w}: {c} (onset={get_onset_class(w)})")

    print(f"\nOnset class distribution of -am words:")
    am_onset = Counter(get_onset_class(w) for w, _, _ in am_words)
    am_total = len(am_words)
    all_onset_total = len(body)
    all_onset_counts = Counter(get_onset_class(r['word']) for r in body)
    for cls, cnt in am_onset.most_common(10):
        am_pct = 100*cnt/am_total
        all_pct = 100*all_onset_counts.get(cls,0)/all_onset_total
        enrichment = am_pct/all_pct if all_pct > 0 else float('inf')
        print(f"  {cls}: {cnt} ({am_pct:.1f}% of am-words vs {all_pct:.1f}% overall; {enrichment:.2f}×)")

    # Characterize -air words
    print(f"\n--- -air suffix characterization ---")
    air_words = [(r['word'], r['section'], r['dialect']) for r in body
                 if get_suffix_v2(r['word']) == 'air']
    air_count = Counter(w for w, _, _ in air_words)
    air_dialect = Counter(d for _, _, d in air_words)
    air_section = Counter(s for _, s, _ in air_words)

    print(f"Total -air tokens: {len(air_words)}")
    print(f"Dialect split: A={air_dialect.get('A',0)}, B={air_dialect.get('B',0)} "
          f"(A/B ratio={air_dialect.get('A',0)/max(1,air_dialect.get('B',0)):.2f})")
    print(f"\nSection distribution:")
    for s in ['herbal','cosmo','stars','pharma','astro']:
        s_n = air_section.get(s,0)
        total_s = all_section.get(s,0)
        print(f"  {s}: {s_n} ({100*s_n/max(1,total_s):.1f}‰ of section tokens)")

    print(f"\nTop -air words:")
    for w, c in air_count.most_common(12):
        print(f"  {w}: {c} (onset={get_onset_class(w)})")

    # A-dialect -am vs -air vs -ol/-or comparison
    print(f"\n--- A-dialect suffix comparison: -am vs -air vs -ol vs -or ---")
    a_body = [r for r in body if r['dialect'] == 'A']
    a_suffs_v2 = Counter(get_suffix_v2(r['word']) for r in a_body)
    a_total = len(a_body)
    for suf in ['ol', 'or', 'ar', 'al', 'am', 'air', 'y', 'aiin']:
        n = a_suffs_v2.get(suf, 0)
        print(f"  A-dialect -{suf}: {n} ({100*n/a_total:.2f}%)")


def h231_daiin(records):
    print("\n" + "=" * 70)
    print("H231: daiin Characterization — Positional Profile and Bigram Context")
    print("=" * 70)

    body = [r for r in records if r['section'] != 'other']
    daiin_recs = [r for r in body if r['word'] == 'daiin']
    non_daiin = [r for r in body if r['word'] != 'daiin']

    print(f"\nTotal body tokens: {len(body)}")
    print(f"daiin tokens: {len(daiin_recs)} ({100*len(daiin_recs)/len(body):.2f}%)")

    # Positional profile
    print(f"\n--- daiin positional profile vs all words ---")
    daiin_first = sum(1 for r in daiin_recs if r['is_line_first'])
    daiin_last = sum(1 for r in daiin_recs if r['is_line_last'])
    daiin_mid = len(daiin_recs) - daiin_first - daiin_last

    all_first = sum(1 for r in body if r['is_line_first'])
    all_last = sum(1 for r in body if r['is_line_last'])
    n = len(body)

    print(f"\n{'Position':<12} {'daiin%':<12} {'all%':<12} {'ratio'}")
    for label, d_n, a_n in [('first', daiin_first, all_first),
                              ('last', daiin_last, all_last),
                              ('mid', daiin_mid, n-all_first-all_last)]:
        d_pct = 100*d_n/max(1,len(daiin_recs))
        a_pct = 100*a_n/max(1,n)
        ratio = d_pct/a_pct if a_pct > 0 else float('inf')
        print(f"{label:<12} {d_pct:<12.1f} {a_pct:<12.1f} {ratio:.2f}×")

    # Section distribution
    print(f"\n--- daiin section distribution ---")
    daiin_section = Counter(r['section'] for r in daiin_recs)
    all_section = Counter(r['section'] for r in body)
    print(f"\n{'Section':<10} {'daiin_n':<10} {'all_n':<10} {'daiin_rate‰'}")
    for s in ['herbal','cosmo','stars','pharma','astro']:
        d_n = daiin_section.get(s, 0)
        a_n = all_section.get(s, 0)
        rate = 1000*d_n/max(1,a_n)
        print(f"{s:<10} {d_n:<10} {a_n:<10} {rate:.2f}‰")

    # Bigram context: what comes before and after daiin?
    print(f"\n--- daiin bigram context ---")
    prev_words = Counter(r['prev_word'] for r in daiin_recs if r['prev_word'])
    next_words = Counter(r['next_word'] for r in daiin_recs if r['next_word'])

    print(f"\nWords BEFORE daiin (prev_word, n={sum(prev_words.values())}):")
    for w, c in prev_words.most_common(15):
        print(f"  {w}: {c}")

    print(f"\nWords AFTER daiin (next_word, n={sum(next_words.values())}):")
    for w, c in next_words.most_common(15):
        print(f"  {w}: {c}")

    # What onset class appears most after daiin?
    print(f"\nOnset class AFTER daiin:")
    after_onset = Counter(get_onset_class(w) for w in next_words.elements())
    after_total = sum(after_onset.values())
    all_onset = Counter(get_onset_class(r['word']) for r in body)
    all_total = len(body)
    for cls, cnt in after_onset.most_common(8):
        after_pct = 100*cnt/after_total
        all_pct = 100*all_onset.get(cls,0)/all_total
        ratio = after_pct/all_pct if all_pct > 0 else float('inf')
        print(f"  {cls}: {cnt} ({after_pct:.1f}% vs {all_pct:.1f}% overall; {ratio:.2f}×)")

    # What onset class appears most before daiin?
    print(f"\nOnset class BEFORE daiin:")
    before_onset = Counter(get_onset_class(w) for w in prev_words.elements())
    before_total = sum(before_onset.values())
    for cls, cnt in before_onset.most_common(8):
        before_pct = 100*cnt/before_total
        all_pct = 100*all_onset.get(cls,0)/all_total
        ratio = before_pct/all_pct if all_pct > 0 else float('inf')
        print(f"  {cls}: {cnt} ({before_pct:.1f}% vs {all_pct:.1f}% overall; {ratio:.2f}×)")

    # Co-occurrence on same line
    print(f"\n--- Words co-occurring on SAME LINE as daiin ---")
    daiin_lines = set(r['line_key'] for r in daiin_recs)
    same_line_words = [r['word'] for r in body
                       if r['line_key'] in daiin_lines and r['word'] != 'daiin']
    same_line_counts = Counter(same_line_words)
    same_line_total = len(same_line_words)

    # Compare to baseline: all body word frequencies
    all_word_counts = Counter(r['word'] for r in body)
    all_total_tokens = len(body)

    print(f"\n{'Word':<12} {'co-occ_n':<12} {'co-occ%':<12} {'base%':<10} {'ratio'}")
    for w, cnt in same_line_counts.most_common(20):
        co_pct = 100*cnt/max(1,same_line_total)
        base_pct = 100*all_word_counts.get(w,0)/all_total_tokens
        ratio = co_pct/base_pct if base_pct > 0 else float('inf')
        print(f"{w:<12} {cnt:<12} {co_pct:<12.2f} {base_pct:<10.2f} {ratio:.2f}×")

    # Compare to other high-frequency function words
    print(f"\n--- daiin vs other d-onset words ---")
    d_words = [r for r in body if get_onset_class(r['word']) == 'd']
    d_freq = Counter(r['word'] for r in d_words)
    d_first_rate = Counter(r['word'] for r in d_words if r['is_line_first'])
    print(f"\n{'Word':<12} {'n':<8} {'first%':<10} {'last%':<10}")
    for w, cnt in d_freq.most_common(10):
        w_recs = [r for r in d_words if r['word'] == w]
        first_n = sum(1 for r in w_recs if r['is_line_first'])
        last_n = sum(1 for r in w_recs if r['is_line_last'])
        print(f"{w:<12} {cnt:<8} {100*first_n/cnt:<10.1f} {100*last_n/cnt:.1f}")

    # Line length context: are daiin-lines shorter or longer?
    print(f"\n--- Line length when daiin is present vs absent ---")
    daiin_line_len = [r['n_in_line'] for r in daiin_recs]
    other_line_len = [r['n_in_line'] for r in non_daiin]
    print(f"Mean line length WITH daiin: {sum(daiin_line_len)/max(1,len(daiin_line_len)):.2f}")
    print(f"Mean line length WITHOUT daiin: {sum(other_line_len)/max(1,len(other_line_len)):.2f}")

    # Dialect
    daiin_dialect = Counter(r['dialect'] for r in daiin_recs)
    print(f"\ndaiin dialect: A={daiin_dialect.get('A',0)}, B={daiin_dialect.get('B',0)}")
    total_a = sum(1 for r in body if r['dialect'] == 'A')
    total_b = sum(1 for r in body if r['dialect'] == 'B')
    print(f"daiin rate in A: {1000*daiin_dialect.get('A',0)/max(1,total_a):.2f}‰")
    print(f"daiin rate in B: {1000*daiin_dialect.get('B',0)/max(1,total_b):.2f}‰")


def main():
    print("Loading data...")
    records, dialect_map = parse_eva(DATA)
    print(f"Total body tokens: {len(records)}")

    h230_extended_suffix(records)
    h231_daiin(records)


if __name__ == '__main__':
    main()
