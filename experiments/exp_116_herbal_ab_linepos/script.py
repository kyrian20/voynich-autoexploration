#!/usr/bin/env python3
"""
exp_116: Herbal A/B Interleave Periodicity (H226) + Line-Position Suffix Effect (H227)
H226: Is the herbal A/B folio alternation regular (quire-aligned)?
H227: Do first/last words of a line use different suffixes than mid-line words?
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

# Approximate quire boundaries for herbal section (based on Voynich quire structure)
# Q1: f1-8, Q2: f9-16, Q3: f17-24, Q4: f25-32, Q5: f33-40, Q6: f41-48, Q7: f49-57
HERBAL_QUIRES = {
    1: list(range(1, 9)),
    2: list(range(9, 17)),
    3: list(range(17, 25)),
    4: list(range(25, 33)),
    5: list(range(33, 41)),
    6: list(range(41, 49)),
    7: list(range(49, 58)),
}


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
                    'pos': i, 'n_in_line': n,
                    'is_line_first': (i == 0),
                    'is_line_last': (i == n - 1),
                    'is_line_mid': (i > 0 and i < n - 1),
                    'section': SECTION_MAP.get(folio_num, 'other'),
                })

    dialect_map = {fnum: ('B' if edy_counts[fnum]/max(1,total_counts[fnum]) >= 0.05 else 'A')
                   for fnum in total_counts}
    for r in records:
        r['dialect'] = dialect_map.get(r['folio'], 'A')

    return records, dialect_map


def h226_herbal_interleave(records, dialect_map):
    print("=" * 70)
    print("H226: Herbal A/B Interleave Periodicity")
    print("=" * 70)

    herbal_folios = sorted([f for f, s in SECTION_MAP.items() if s == 'herbal'
                            and f in dialect_map])

    print(f"\n--- Herbal folio dialect sequence ---")
    print(f"{'Folio':<8} {'Dialect':<10} {'edy_rate%':<12} {'Quire'}")
    folio_dialect_seq = []
    for f in herbal_folios:
        edy_r = dialect_map.get(f, 'A')
        # Get token counts for this folio
        quire = None
        for q, qfolios in HERBAL_QUIRES.items():
            if f in qfolios:
                quire = q
                break
        folio_dialect_seq.append((f, edy_r, quire))
        print(f"{f:<8} {edy_r:<10} {'—':<12} {quire or '?'}")

    # Binary sequence: 1=B, 0=A
    print(f"\n--- Binary A/B sequence (1=B, 0=A) ---")
    binary = [1 if d == 'B' else 0 for _, d, _ in folio_dialect_seq]
    folio_nums = [f for f, _, _ in folio_dialect_seq]
    seq_str = ''.join(str(b) for b in binary)
    print(f"Sequence: {seq_str}")
    print(f"B-folios: {sum(binary)}/{len(binary)} ({100*sum(binary)/len(binary):.1f}%)")

    # Runs analysis
    print(f"\n--- Runs analysis ---")
    runs = []
    current_val = binary[0]
    current_run = 1
    for b in binary[1:]:
        if b == current_val:
            current_run += 1
        else:
            runs.append((current_val, current_run))
            current_val = b
            current_run = 1
    runs.append((current_val, current_run))

    a_runs = [r for v, r in runs if v == 0]
    b_runs = [r for v, r in runs if v == 1]
    print(f"Total runs: {len(runs)}")
    print(f"A-runs (n={len(a_runs)}): lengths = {sorted(a_runs)}")
    print(f"B-runs (n={len(b_runs)}): lengths = {sorted(b_runs)}")
    print(f"Mean A-run length: {sum(a_runs)/max(1,len(a_runs)):.2f}")
    print(f"Mean B-run length: {sum(b_runs)/max(1,len(b_runs)):.2f}")

    # Quire-level analysis
    print(f"\n--- Quire-level B-folio distribution ---")
    print(f"{'Quire':<8} {'Folios':<20} {'B_folios':<15} {'B_positions':<20} {'B_at_boundary?'}")
    for q, qfolios in HERBAL_QUIRES.items():
        valid_qfolios = [f for f in qfolios if f in dialect_map]
        if not valid_qfolios: continue
        b_in_quire = [f for f in valid_qfolios if dialect_map[f] == 'B']
        # Positions within quire (1-indexed from start of quire)
        b_positions = [valid_qfolios.index(f)+1 for f in b_in_quire]
        quire_len = len(valid_qfolios)
        # Boundary = position 1, 2, last-1, last (within quire)
        boundary_positions = {1, 2, quire_len-1, quire_len}
        at_boundary = any(p in boundary_positions for p in b_positions)
        print(f"{q:<8} {str(valid_qfolios):<20} {str(b_in_quire):<15} {str(b_positions):<20} {'YES' if at_boundary else 'NO'}")

    # Autocorrelation of the binary sequence
    print(f"\n--- Autocorrelation of A/B binary sequence ---")
    n = len(binary)
    mean = sum(binary) / n
    variance = sum((b - mean)**2 for b in binary) / n
    if variance > 0:
        for lag in range(1, min(15, n//2)):
            cov = sum((binary[i] - mean) * (binary[i+lag] - mean) for i in range(n-lag)) / (n-lag)
            autocorr = cov / variance
            bar = '|' + '#' * int(abs(autocorr) * 20) + (' (neg)' if autocorr < 0 else '')
            print(f"  Lag {lag:2d}: autocorr = {autocorr:+.3f}  {bar}")
    else:
        print("  Variance is zero (all same dialect)")

    # Expected runs under random model
    p_b = sum(binary) / len(binary)
    p_a = 1 - p_b
    expected_runs = 1 + 2 * (n - 1) * p_a * p_b
    print(f"\nExpected runs (random): {expected_runs:.1f}")
    print(f"Actual runs: {len(runs)}")
    print(f"More runs than expected: {'YES (alternating)' if len(runs) > expected_runs else 'NO (clustering)'}")


def h227_linepos_suffix(records):
    print("\n" + "=" * 70)
    print("H227: Line-Position Effect on Suffix Distribution")
    print("=" * 70)

    body = [r for r in records if r['section'] != 'other']

    # Position categories: line-first, line-last, mid-line
    # Only use lines with ≥3 words to get meaningful mid-line tokens
    long_lines = [r for r in body if r['n_in_line'] >= 3]
    short_body = [r for r in body if r['n_in_line'] < 3]

    pos_classes = ['first', 'last', 'mid']

    def get_pos_class(r):
        if r['is_line_first']: return 'first'
        if r['is_line_last']: return 'last'
        return 'mid'

    # Global suffix by position
    print(f"\n--- Suffix distribution by line position (all sections, lines ≥3 words) ---")
    pos_suffix = defaultdict(Counter)
    for r in long_lines:
        pc = get_pos_class(r)
        pos_suffix[pc][get_suffix(r['word'])] += 1

    # Key suffixes to track
    key_suffs = ['edy','eedy','eey','y','ol','or','aiin','dy','ar']
    totals = {pc: sum(pos_suffix[pc].values()) for pc in pos_classes}
    print(f"\n{'Suffix':<8} {'first%':<10} {'last%':<10} {'mid%':<10} {'first/mid':<12} {'last/mid':<12}")
    for suf in key_suffs:
        pcts = {pc: 100*pos_suffix[pc].get(suf,0)/max(1,totals[pc]) for pc in pos_classes}
        mid_rate = pcts['mid']
        first_ratio = pcts['first']/mid_rate if mid_rate > 0 else float('nan')
        last_ratio = pcts['last']/mid_rate if mid_rate > 0 else float('nan')
        print(f"{suf:<8} {pcts['first']:<10.2f} {pcts['last']:<10.2f} {pcts['mid']:<10.2f} "
              f"{first_ratio:<12.2f} {last_ratio:<12.2f}")

    print(f"\nTokens: first={totals['first']}, last={totals['last']}, mid={totals['mid']}")

    # Shannon entropy by position
    print(f"\n{'Position':<12} {'H(suffix)':<12} {'n'}")
    for pc in pos_classes:
        H = shannon_entropy(pos_suffix[pc])
        print(f"{pc:<12} {H:<12.3f} {totals[pc]}")

    # By dialect
    print(f"\n--- Suffix by line position, A vs B dialect ---")
    for dialect in ['A', 'B']:
        d_recs = [r for r in long_lines if r['dialect'] == dialect]
        print(f"\n  Dialect {dialect}:")
        d_pos_suffix = defaultdict(Counter)
        for r in d_recs:
            pc = get_pos_class(r)
            d_pos_suffix[pc][get_suffix(r['word'])] += 1
        d_totals = {pc: sum(d_pos_suffix[pc].values()) for pc in pos_classes}
        print(f"  {'Suffix':<8} {'first%':<10} {'last%':<10} {'mid%':<10} {'first/mid':<12} {'last/mid'}")
        for suf in key_suffs:
            pcts = {pc: 100*d_pos_suffix[pc].get(suf,0)/max(1,d_totals[pc]) for pc in pos_classes}
            mid_rate = pcts['mid']
            if mid_rate == 0: continue
            fr = pcts['first']/mid_rate
            lr = pcts['last']/mid_rate
            if abs(fr-1.0) < 0.1 and abs(lr-1.0) < 0.1: continue  # Skip near-uniform
            print(f"  {suf:<8} {pcts['first']:<10.2f} {pcts['last']:<10.2f} {pcts['mid']:<10.2f} "
                  f"{fr:<12.2f} {lr:.2f}")

    # By onset class and position for B-dialect
    print(f"\n--- B-dialect: Suffix by onset class and position ---")
    b_recs = [r for r in long_lines if r['dialect'] == 'B']
    onset_classes = ['ch', 'sh', 'qok', 'ok']
    b_suffs = ['edy', 'eedy', 'eey']
    print(f"\n{'Onset':<8} {'Position':<10} {'n':<6} {'edy%':<8} {'eedy%':<8} {'eey%':<8} {'dominant'}")
    for cls in onset_classes:
        cls_recs = [r for r in b_recs if get_onset_class(r['word']) == cls]
        for pc in pos_classes:
            pc_recs = [r for r in cls_recs if get_pos_class(r) == pc]
            if len(pc_recs) < 10: continue
            suf_counts = Counter(get_suffix(r['word']) for r in pc_recs)
            b_total = sum(suf_counts.get(s,0) for s in b_suffs)
            if b_total < 5: continue
            edy_r = 100*suf_counts.get('edy',0)/b_total
            eedy_r = 100*suf_counts.get('eedy',0)/b_total
            eey_r = 100*suf_counts.get('eey',0)/b_total
            dom = max(b_suffs, key=lambda s: suf_counts.get(s,0))
            print(f"{cls:<8} {pc:<10} {len(pc_recs):<6} {edy_r:<8.1f} {eedy_r:<8.1f} {eey_r:<8.1f} {dom}")

    # A-dialect: ol/or/y by position
    print(f"\n--- A-dialect: A-suffix (ol/or/y/aiin) by position ---")
    a_recs = [r for r in long_lines if r['dialect'] == 'A']
    a_suffs = ['ol', 'or', 'y', 'aiin']
    onset_classes_a = ['ch', 'sh', 'qok', 'ok', 'cth']
    print(f"\n{'Onset':<8} {'Position':<10} {'n':<6} {'ol%':<8} {'or%':<8} {'y%':<8} {'aiin%':<8}")
    for cls in onset_classes_a:
        cls_recs = [r for r in a_recs if get_onset_class(r['word']) == cls]
        for pc in pos_classes:
            pc_recs = [r for r in cls_recs if get_pos_class(r) == pc]
            if len(pc_recs) < 10: continue
            suf_counts = Counter(get_suffix(r['word']) for r in pc_recs)
            a_total = sum(suf_counts.get(s,0) for s in a_suffs)
            if a_total < 5: continue
            rates = {s: 100*suf_counts.get(s,0)/a_total for s in a_suffs}
            print(f"{cls:<8} {pc:<10} {len(pc_recs):<6} {rates['ol']:<8.1f} {rates['or']:<8.1f} "
                  f"{rates['y']:<8.1f} {rates['aiin']:<8.1f}")

    # Free-morpheme positional check: standalone ol/or/aiin enriched at line-last?
    print(f"\n--- Conditional entropy of suffix given position (all dialects) ---")
    all_suffix = Counter(get_suffix(r['word']) for r in long_lines)
    H_marg = shannon_entropy(all_suffix)

    groups = defaultdict(list)
    for r in long_lines:
        groups[get_pos_class(r)].append(get_suffix(r['word']))
    n_total = len(long_lines)
    H_cond = sum((len(g)/n_total)*shannon_entropy(Counter(g)) for g in groups.values())
    print(f"\nH(suffix) marginal = {H_marg:.4f} bits")
    print(f"H(suffix | position) = {H_cond:.4f} bits")
    print(f"Information from position = {H_marg - H_cond:.4f} bits ({100*(H_marg-H_cond)/H_marg:.1f}%)")


def main():
    print("Loading data...")
    records, dialect_map = parse_eva(DATA)
    print(f"Total body tokens: {len(records)}")

    h226_herbal_interleave(records, dialect_map)
    h227_linepos_suffix(records)


if __name__ == '__main__':
    main()
