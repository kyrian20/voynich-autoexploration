#!/usr/bin/env python3
"""
exp_113: Triple-Vowel Extended Forms (H222) + A-Dialect Suffix Section Variation (H223)
"""

import re
import math
from collections import defaultdict, Counter

DATA = 'data/transcriptions/eva_zl3b.txt'

def parse_eva(path):
    section_map = {}
    for f in range(1, 58): section_map[f] = 'herbal'
    for f in range(67, 74): section_map[f] = 'astro'
    for f in range(75, 85): section_map[f] = 'cosmo'
    for f in range(87, 103): section_map[f] = 'pharma'
    for f in range(103, 117): section_map[f] = 'stars'

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

            prefix = ''.join(c for c in locus_type if c in '@+*=~&')
            lt = locus_type[len(prefix):]
            is_body = bool(re.match(r'P', lt))
            is_label = bool(re.match(r'L', lt))
            if not (is_body or is_label): continue

            text_clean = re.sub(r'<[^>]*>', '', text)
            text_clean = re.sub(r'\[[^\]]*\]', lambda m: m.group(0)[1:-1].split(':')[0], text_clean)
            text_clean = re.sub(r'\{[^}]*\}', '', text_clean)
            text_clean = re.sub(r'@\d+;?|<%>|<!.*?>|<\$>', '', text_clean)

            words = [w for w in re.split(r'[-.\s,]', text_clean)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words: continue

            section = section_map.get(folio_num, 'other')
            for w in words:
                if 'edy' in w or 'eedy' in w:
                    edy_counts[folio_num] += 1
                total_counts[folio_num] += 1

            n = len(words)
            for i, w in enumerate(words):
                records.append({
                    'word': w, 'folio': folio_num, 'section': section,
                    'is_body': is_body, 'is_label': is_label,
                    'line_first': (i == 0), 'line_last': (i == n-1),
                })

    dialect_map = {fnum: ('B' if edy_counts[fnum]/max(1,total_counts[fnum]) >= 0.05 else 'A')
                   for fnum in total_counts}
    for r in records:
        r['dialect'] = dialect_map.get(r['folio'], 'A')
    return records, dialect_map


def get_suffix(word):
    for suf in ['eedy', 'edy', 'eey', 'aiin', 'ain', 'ol', 'or', 'ar', 'al', 'ey', 'dy', 'y']:
        if word.endswith(suf) and len(word) > len(suf):
            return suf
    return 'other'


def get_onset_class(word):
    w = word
    if w.startswith('qok'): return 'qok'
    if w.startswith('qot'): return 'qot'
    if w.startswith('qo'): return 'qo'
    if w.startswith('ch'): return 'ch'
    if w.startswith('sh'): return 'sh'
    if w.startswith('ok'): return 'ok'
    if w.startswith('ot'): return 'ot'
    if w.startswith('ol'): return 'ol'
    return 'other'


def h222_triple_vowel(records):
    print("=" * 70)
    print("H222: Triple-Vowel Extended Forms (eee-words)")
    print("=" * 70)

    body = [r for r in records if r['is_body']]

    # Words with 3+ consecutive 'e' (eee, eeee)
    triple_e_words = [r for r in body if re.search(r'eee', r['word'])]
    double_e_words = [r for r in body if re.search(r'ee', r['word']) and not re.search(r'eee', r['word'])]
    single_e_words = [r for r in body if 'e' in r['word'] and not re.search(r'ee', r['word'])]

    sections = ['herbal', 'pharma', 'cosmo', 'stars', 'astro']
    sect_totals = Counter(r['section'] for r in body)

    print(f"\nTotal body tokens: {len(body)}")
    print(f"Words with eee (3+e): {len(triple_e_words)}")
    print(f"Words with ee (2e, not 3+): {len(double_e_words)}")

    print(f"\n--- Section distribution of eee words ---")
    triple_sect = Counter(r['section'] for r in triple_e_words)
    double_sect = Counter(r['section'] for r in double_e_words)

    print(f"{'Section':<12} {'total':<8} {'eee_n':<8} {'eee‰':<10} {'ee_n':<8} {'ee‰':<10}")
    for s in sections:
        t = sect_totals[s]
        te = triple_sect[s]
        de = double_sect[s]
        print(f"{s:<12} {t:<8} {te:<8} {1000*te/max(1,t):<10.2f} {de:<8} {1000*de/max(1,t):.2f}")

    print(f"\n--- Top eee words by frequency ---")
    triple_word_counts = Counter(r['word'] for r in triple_e_words)
    triple_sect_by_word = defaultdict(Counter)
    for r in triple_e_words:
        triple_sect_by_word[r['word']][r['section']] += 1

    print(f"{'Word':<20} {'Total':<8} {'herbal':<8} {'cosmo':<8} {'stars':<8} {'astro':<8} {'Stars_dom'}")
    for word, total in triple_word_counts.most_common(30):
        h = triple_sect_by_word[word]['herbal']
        c = triple_sect_by_word[word]['cosmo']
        s = triple_sect_by_word[word]['stars']
        a = triple_sect_by_word[word]['astro']
        is_stars = s >= total * 0.5
        print(f"{word:<20} {total:<8} {h:<8} {c:<8} {s:<8} {a:<8} {'*stars' if is_stars else ''}")

    print(f"\n--- Vowel length gradient: single-e vs ee vs eee suffix forms ---")
    print("(Is eee an extension of ee which is an extension of e?)")

    # Compare suffix patterns
    for base_suf, ext1_suf, ext2_suf in [('edy', 'eedy', 'eeedy'), ('ey', 'eey', 'eeey'), ('y', 'ey', 'eey')]:
        base_words = [r for r in body if get_suffix(r['word']) == base_suf]
        ext1_words = [r for r in body if r['word'].endswith(ext1_suf) and len(r['word']) > len(ext1_suf)]
        ext2_words = [r for r in body if r['word'].endswith(ext2_suf) and len(r['word']) > len(ext2_suf)]

        print(f"\n  -{base_suf} → -{ext1_suf} → -{ext2_suf}:")
        for label, word_list in [(f'-{base_suf}', base_words), (f'-{ext1_suf}', ext1_words), (f'-{ext2_suf}', ext2_words)]:
            n = len(word_list)
            if n == 0: continue
            sect_dist = Counter(r['section'] for r in word_list)
            dialect_dist = Counter(r['dialect'] for r in word_list)
            print(f"    {label}: n={n}, A={dialect_dist['A']}, B={dialect_dist['B']}", end="")
            for s in ['herbal', 'cosmo', 'stars']:
                pct = 100 * sect_dist[s] / max(1, n)
                print(f", {s}={pct:.0f}%", end="")
            print()

    # Onset class distribution of eee words
    print(f"\n--- Onset class distribution of eee words ---")
    onset_eee = Counter(get_onset_class(r['word']) for r in triple_e_words)
    onset_total = Counter(get_onset_class(r['word']) for r in body)

    print(f"{'Onset':<10} {'eee_n':<8} {'eee%':<10} {'all%':<10} {'Enrich'}")
    for cls, cnt in onset_eee.most_common():
        all_cnt = onset_total[cls]
        eee_pct = 100 * cnt / len(triple_e_words)
        all_pct = 100 * all_cnt / len(body)
        enrich = eee_pct / all_pct if all_pct > 0 else float('inf')
        if cnt >= 3:
            print(f"{cls:<10} {cnt:<8} {eee_pct:<10.1f} {all_pct:<10.1f} {enrich:.2f}×")


def h223_a_suffix_sections(records):
    print("\n" + "=" * 70)
    print("H223: A-Dialect Suffix Section Variation")
    print("=" * 70)

    body = [r for r in records if r['is_body']]
    a_body = [r for r in body if r['dialect'] == 'A']

    a_sections = ['herbal', 'pharma', 'astro']
    onset_classes = ['ch', 'sh', 'qok', 'qot', 'ok', 'ot', 'qo']
    a_suffixes = ['ol', 'or', 'y', 'aiin', 'ain', 'ar', 'al', 'ey', 'dy']

    # A-suffix matrix by onset class and section
    matrix = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for r in a_body:
        cls = get_onset_class(r['word'])
        suf = get_suffix(r['word'])
        matrix[cls][r['section']][suf] += 1

    print(f"\n--- A-paradigm suffix distribution by onset class and section ---")
    for cls in onset_classes:
        valid_sects = []
        for s in a_sections:
            suf_counts = matrix[cls][s]
            a_total = sum(suf_counts.get(sf, 0) for sf in a_suffixes)
            if a_total >= 10:
                valid_sects.append((s, suf_counts, a_total))

        if len(valid_sects) < 2: continue

        print(f"\n  Onset class: {cls}")
        for s, suf_counts, a_total in valid_sects:
            top_sufs = sorted(a_suffixes, key=lambda sf: -suf_counts.get(sf, 0))[:4]
            suf_str = ", ".join(f"-{sf}={suf_counts.get(sf,0)}({100*suf_counts.get(sf,0)/a_total:.0f}%)"
                                for sf in top_sufs if suf_counts.get(sf, 0) > 0)
            print(f"    {s}: n={a_total}, {suf_str}")

    # Statistical summary: does any A-section systematically differ?
    print(f"\n--- Does pharma-A differ from herbal-A in suffix rates? ---")
    print(f"Comparing herbal vs pharma for A-dialect onset classes:")

    print(f"\n{'Onset':<8} {'herbal_ol%':<14} {'herbal_or%':<14} {'herbal_y%':<13} {'pharma_ol%':<14} {'pharma_or%':<14} {'pharma_y%':<12}")
    for cls in onset_classes:
        h_counts = matrix[cls].get('herbal', Counter())
        p_counts = matrix[cls].get('pharma', Counter())
        h_total = sum(h_counts.get(sf, 0) for sf in a_suffixes)
        p_total = sum(p_counts.get(sf, 0) for sf in a_suffixes)

        if h_total < 10 or p_total < 10: continue

        h_ol = 100 * h_counts.get('ol', 0) / h_total
        h_or = 100 * h_counts.get('or', 0) / h_total
        h_y = 100 * h_counts.get('y', 0) / h_total
        p_ol = 100 * p_counts.get('ol', 0) / p_total
        p_or = 100 * p_counts.get('or', 0) / p_total
        p_y = 100 * p_counts.get('y', 0) / p_total

        print(f"{cls:<8} {h_ol:<14.1f} {h_or:<14.1f} {h_y:<13.1f} {p_ol:<14.1f} {p_or:<14.1f} {p_y:.1f}")

    # Absolute comparison test: entropy of A-suffix by section
    print(f"\n--- A-suffix entropy by section (for ch-onset in A) ---")
    for cls in ['ch', 'sh', 'qok']:
        print(f"\n  {cls}:")
        for s in a_sections:
            suf_counts = matrix[cls].get(s, Counter())
            a_total = sum(suf_counts.get(sf, 0) for sf in a_suffixes)
            if a_total < 5: continue
            H = -sum((suf_counts.get(sf,0)/a_total)*math.log2(suf_counts.get(sf,0)/a_total)
                     for sf in a_suffixes if suf_counts.get(sf,0) > 0)
            dominant = max(a_suffixes, key=lambda sf: suf_counts.get(sf, 0))
            print(f"    {s}: n={a_total}, H={H:.3f} bits, dominant=-{dominant}({suf_counts.get(dominant,0)})")

    # Overall conclusion: is A uniform?
    print(f"\n--- Summary: Is A-dialect suffix paradigm uniform across sections? ---")
    print("Testing if herbal-A and pharma-A have same suffix profile:")

    total_diff = 0
    n_tests = 0
    for cls in ['ch', 'sh', 'qok']:
        h_counts = matrix[cls].get('herbal', Counter())
        p_counts = matrix[cls].get('pharma', Counter())
        h_total = sum(h_counts.get(sf, 0) for sf in a_suffixes)
        p_total = sum(p_counts.get(sf, 0) for sf in a_suffixes)
        if h_total < 10 or p_total < 10: continue

        for sf in ['ol', 'or', 'y', 'aiin']:
            h_rate = h_counts.get(sf, 0) / h_total
            p_rate = p_counts.get(sf, 0) / p_total
            diff = abs(h_rate - p_rate)
            total_diff += diff
            n_tests += 1

    avg_diff = total_diff / n_tests if n_tests > 0 else 0
    print(f"  Average absolute difference in A-suffix rates (herbal vs pharma): {100*avg_diff:.1f}%")
    print(f"  (Compare: B-section gradient for -eey: herbal~12% vs stars~43% = 31% difference)")
    print(f"  Conclusion: {'A has SIGNIFICANT section variation' if avg_diff > 0.15 else 'A is largely UNIFORM (no major section variation)'}")


def main():
    print("Loading data...")
    records, dialect_map = parse_eva(DATA)
    body_recs = [r for r in records if r['is_body']]
    print(f"Total body tokens: {len(body_recs)}")
    h222_triple_vowel(records)
    h223_a_suffix_sections(records)


if __name__ == '__main__':
    main()
