#!/usr/bin/env python3
"""
exp_114: Conditional Entropy as Naturalness Test (H224)
Computes H(suffix | onset_class, section, dialect) vs H(suffix) marginal
Tests whether the four-level hierarchy (F120) reduces suffix prediction uncertainty.
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
            if not is_body: continue

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
            records.extend((w, folio_num, section) for w in words)

    dialect_map = {fnum: ('B' if edy_counts[fnum]/max(1,total_counts[fnum]) >= 0.05 else 'A')
                   for fnum in total_counts}

    final_records = []
    for w, folio, section in records:
        final_records.append((w, folio, section, dialect_map.get(folio, 'A')))
    return final_records


def get_suffix(word):
    for suf in ['eeedy','eeey','eedy','edy','eey','aiin','ain','ol','or','ar','al','ey','dy','y']:
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
    if w.startswith('olk'): return 'olk'
    if w.startswith('ok'): return 'ok'
    if w.startswith('ot'): return 'ot'
    if w.startswith('ol'): return 'ol'
    if w.startswith('d'): return 'd'
    if w.startswith('s'): return 's'
    if w.startswith('y'): return 'y_onset'
    return 'other'


def shannon_entropy(counts):
    total = sum(counts.values())
    if total == 0: return 0.0
    return -sum((c/total)*math.log2(c/total) for c in counts.values() if c > 0)


def conditional_entropy(records, conditions):
    """
    Compute H(suffix | conditions) where conditions is a list of keys.
    conditions = list of (condition_name, condition_value) tuples.
    """
    # Group records by condition values
    groups = defaultdict(list)
    for w, folio, section, dialect in records:
        key = tuple(c(w, section, dialect) for c in conditions)
        suf = get_suffix(w)
        groups[key].append(suf)

    total = sum(len(g) for g in groups.values())
    H_cond = 0.0
    for key, sufs in groups.items():
        suf_counts = Counter(sufs)
        n = len(sufs)
        H_g = shannon_entropy(suf_counts)
        H_cond += (n / total) * H_g
    return H_cond, total


def h224_conditional_entropy(records):
    print("=" * 70)
    print("H224: Conditional Entropy as Naturalness Test")
    print("=" * 70)

    # Marginal suffix distribution
    all_suffixes = Counter(get_suffix(w) for w, _, _, _ in records)
    H_marginal = shannon_entropy(all_suffixes)
    n_total = sum(all_suffixes.values())

    print(f"\nTotal body tokens: {n_total}")
    print(f"H(suffix) marginal = {H_marginal:.4f} bits")
    print(f"\nMarginal suffix distribution:")
    for suf, cnt in sorted(all_suffixes.items(), key=lambda x: -x[1])[:15]:
        print(f"  -{suf}: {cnt} ({100*cnt/n_total:.1f}%)")

    print(f"\n--- Conditional entropy at each level of the four-level hierarchy ---")

    # Level 1: Dialect
    def cond_dialect(w, section, dialect): return dialect
    H_d, _ = conditional_entropy(records, [cond_dialect])
    print(f"\nLevel 1: H(suffix | dialect) = {H_d:.4f} bits (reduction: {H_marginal - H_d:.4f} bits = {100*(H_marginal-H_d)/H_marginal:.1f}%)")

    # Level 2: Dialect + onset class
    def cond_onset(w, section, dialect): return get_onset_class(w)
    H_do, _ = conditional_entropy(records, [cond_dialect, cond_onset])
    print(f"Level 2: H(suffix | dialect, onset) = {H_do:.4f} bits (reduction vs marginal: {H_marginal - H_do:.4f} bits = {100*(H_marginal-H_do)/H_marginal:.1f}%)")
    print(f"         Additional reduction from level 1: {H_d - H_do:.4f} bits")

    # Level 3: Dialect + onset + section
    def cond_section(w, section, dialect): return section
    H_dos, _ = conditional_entropy(records, [cond_dialect, cond_onset, cond_section])
    print(f"Level 3: H(suffix | dialect, onset, section) = {H_dos:.4f} bits (reduction vs marginal: {H_marginal - H_dos:.4f} bits = {100*(H_marginal-H_dos)/H_marginal:.1f}%)")
    print(f"         Additional reduction from level 2: {H_do - H_dos:.4f} bits")

    # Level 4: Dialect + onset + section + vowel-length group
    def vowel_length(w, section, dialect):
        if re.search(r'eee', w): return 'triple_e'
        if re.search(r'ee', w): return 'double_e'
        return 'single'
    H_dosv, _ = conditional_entropy(records, [cond_dialect, cond_onset, cond_section, vowel_length])
    print(f"Level 4: H(suffix | dialect, onset, section, vowel_len) = {H_dosv:.4f} bits (reduction vs marginal: {H_marginal - H_dosv:.4f} bits = {100*(H_marginal-H_dosv)/H_marginal:.1f}%)")
    print(f"         Additional reduction from level 3: {H_dos - H_dosv:.4f} bits")

    # Individual onset class entropy decomposition
    print(f"\n--- Per-onset-class suffix entropy by dialect ---")
    onset_classes = ['ch', 'sh', 'qok', 'qot', 'ok', 'ot', 'qo', 'olk', 'cth', 'd', 's', 'ol']
    sections = ['herbal', 'cosmo', 'stars', 'pharma']

    print(f"\n{'Onset':<10} {'n':<8} {'H_all':<10} {'H_A':<10} {'H_B':<10} {'Info_from_dialect'}")
    for cls in onset_classes:
        cls_recs = [(w, sec, d) for w, _, sec, d in records if get_onset_class(w) == cls]
        n = len(cls_recs)
        if n < 20: continue

        suf_all = Counter(get_suffix(w) for w, _, _ in cls_recs)
        suf_a = Counter(get_suffix(w) for w, _, d in cls_recs if d == 'A')
        suf_b = Counter(get_suffix(w) for w, _, d in cls_recs if d == 'B')

        H_all = shannon_entropy(suf_all)
        H_a = shannon_entropy(suf_a) if sum(suf_a.values()) > 0 else float('nan')
        H_b = shannon_entropy(suf_b) if sum(suf_b.values()) > 0 else float('nan')

        n_a = sum(suf_a.values())
        n_b = sum(suf_b.values())
        H_cond = (n_a/n)*H_a + (n_b/n)*H_b if n > 0 else 0
        info_gain = H_all - H_cond

        print(f"{cls:<10} {n:<8} {H_all:<10.3f} {H_a:<10.3f} {H_b:<10.3f} {info_gain:.3f}")

    # Section-level conditional entropy for B-dialect
    print(f"\n--- B-dialect suffix entropy by section (per onset class) ---")
    print(f"{'Onset':<8} {'H_all_B':<12} {'H_cond_sect':<14} {'Info_from_section'}")
    for cls in ['ch', 'sh', 'qok', 'ok', 'ot']:
        b_recs = [(w, sec) for w, _, sec, d in records
                  if get_onset_class(w) == cls and d == 'B' and sec in sections]
        n = len(b_recs)
        if n < 20: continue

        suf_all_b = Counter(get_suffix(w) for w, _ in b_recs)
        H_all_b = shannon_entropy(suf_all_b)

        # Conditional on section
        groups = defaultdict(list)
        for w, sec in b_recs:
            groups[sec].append(get_suffix(w))
        H_cond_sect = sum((len(g)/n)*shannon_entropy(Counter(g)) for g in groups.values())
        info_gain_sect = H_all_b - H_cond_sect

        print(f"{cls:<8} {H_all_b:<12.3f} {H_cond_sect:<14.3f} {info_gain_sect:.3f}")

    # Comparison with shuffled null model
    import random
    random.seed(42)
    print(f"\n--- Null model: shuffled suffix labels ---")
    print("(If hierarchy is real, shuffled data should show NO entropy reduction)")

    all_recs_list = list(records)
    shuffled_suffs = [get_suffix(w) for w, _, _, _ in all_recs_list]
    random.shuffle(shuffled_suffs)

    shuffled_records = [(s, folio, section, dialect)
                        for (_, folio, section, dialect), s in zip(all_recs_list, shuffled_suffs)]

    # Marginal of shuffled
    shuf_counts = Counter(shuffled_suffs)
    H_shuf_marg = shannon_entropy(shuf_counts)

    def shuf_get_suffix(w, sec, d): return w  # w is already the suffix for shuffled
    H_shuf_d, _ = conditional_entropy(
        [(s, f, sec, d) for s, f, sec, d in shuffled_records],
        [lambda s, sec, d: d]
    )
    print(f"Shuffled H(suffix) = {H_shuf_marg:.4f} bits")
    print(f"Shuffled H(suffix | dialect) = {H_shuf_d:.4f} bits (reduction: {H_shuf_marg - H_shuf_d:.4f} bits)")
    print(f"Actual reduction from dialect: {H_marginal - H_d:.4f} bits")
    print(f"Signal/noise ratio: {(H_marginal - H_d)/(max(0.001, H_shuf_marg - H_shuf_d)):.1f}×")

    # Summary table
    print(f"\n--- Summary: Information Hierarchy ---")
    print(f"{'Level':<40} {'H(bits)':<12} {'Reduction':<12} {'% of marginal'}")
    print(f"{'H(suffix) marginal':<40} {H_marginal:<12.4f} {'—':<12} {'100%'}")
    print(f"{'H(suffix | dialect)':<40} {H_d:<12.4f} {H_marginal-H_d:<12.4f} {100*(H_marginal-H_d)/H_marginal:.1f}%")
    print(f"{'H(suffix | +onset_class)':<40} {H_do:<12.4f} {H_marginal-H_do:<12.4f} {100*(H_marginal-H_do)/H_marginal:.1f}%")
    print(f"{'H(suffix | +section)':<40} {H_dos:<12.4f} {H_marginal-H_dos:<12.4f} {100*(H_marginal-H_dos)/H_marginal:.1f}%")
    print(f"{'H(suffix | +vowel_length)':<40} {H_dosv:<12.4f} {H_marginal-H_dosv:<12.4f} {100*(H_marginal-H_dosv)/H_marginal:.1f}%")


def main():
    print("Loading data...")
    records = parse_eva(DATA)
    print(f"Total body tokens: {len(records)}")
    h224_conditional_entropy(records)


if __name__ == '__main__':
    main()
