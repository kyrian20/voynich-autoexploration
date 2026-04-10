#!/usr/bin/env python3
"""
exp_167: [daiin cthol cthy] trigram (H344), B-dialect cthedy positional profile (H342),
         qok→l specific pairs (H343), general 3-word chain survey
H344: Does [daiin][cthol][cthy] appear as a consecutive trigram?
H342: B-dialect cthedy vs chedy/shedy positional profiles
H343: qok→l specific word pairs
BONUS: Survey enriched trigrams involving cth-words in A-dialect
"""
import re
from collections import Counter, defaultdict

CORPUS = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

def get_onset(word):
    w = word.lower()
    if w.startswith('qok'): return 'qok'
    if w.startswith('qot'): return 'qot'
    if w.startswith('qo'): return 'qo'
    if w.startswith('cth'): return 'cth'
    if w.startswith('che') or w.startswith('chi'): return 'ch_e'
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
    return 'other'

def get_slot(i, n):
    if n == 1: return 'only'
    if i == 0: return 'LF'
    if i == n-1: return 'LL'
    if i == 1: return 'second'
    return 'MID'

SECTION_RANGES = {
    'herbal': list(range(1, 67)),
    'astro': list(range(67, 85)),
    'pharma': list(range(88, 103)),
    'cosmo': list(range(85, 88)),
    'stars': list(range(103, 117)),
    'bio': list(range(75, 85)) + list(range(116, 118)),
}
folio_to_section = {}
for sec, folios in SECTION_RANGES.items():
    for fn in folios:
        folio_to_section[fn] = sec

def parse_locus(locus_raw):
    locus_parts = locus_raw.split(',')
    if len(locus_parts) < 2:
        return None, None
    folio_str = locus_parts[0]
    folio_base = folio_str.split('.')[0].lstrip('<')
    m = re.match(r'f(\d+)', folio_base)
    if not m:
        return None, None
    folio_num = int(m.group(1))
    lt_raw = locus_parts[1].rstrip('>')
    lt = lt_raw.lstrip('@+*=~&')
    return folio_num, lt

folio_words = defaultdict(list)
raw_lines = []
with open(CORPUS) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'): continue
        parts = line.split(None, 1)
        if len(parts) < 2: continue
        locus_raw, text = parts
        folio_num, lt = parse_locus(locus_raw)
        if folio_num is None: continue
        if not lt.startswith('P'): continue
        words = [w for w in text.split('.') if w and re.match(r'[a-z]', w) and not w.startswith('<')]
        if not words: continue
        folio_words[folio_num].extend(words)
        raw_lines.append((folio_num, words))

folio_dialect = {}
folio_edy_rate = {}
for fn, wds in folio_words.items():
    if len(wds) < 10: continue
    edy_count = sum(1 for w in wds if 'edy' in w or 'eedy' in w)
    rate = edy_count / len(wds)
    folio_edy_rate[fn] = rate
    folio_dialect[fn] = 'B' if rate >= 0.05 else 'A'

lines_data = []
for folio_num, words in raw_lines:
    dialect = folio_dialect.get(folio_num, 'unknown')
    section = folio_to_section.get(folio_num, 'other')
    lines_data.append((folio_num, section, dialect, words))

a_lines = [(fn, sec, dial, wds) for fn, sec, dial, wds in lines_data if dial == 'A']
b_lines = [(fn, sec, dial, wds) for fn, sec, dial, wds in lines_data if dial == 'B']

# Baseline onset counts
a_onset = Counter()
for fn, sec, dial, wds in a_lines:
    for w in wds:
        a_onset[get_onset(w)] += 1
a_total = sum(a_onset.values())
a_total_bigrams = sum(len(wds)-1 for fn, sec, dial, wds in a_lines)
a_total_trigrams = sum(max(0, len(wds)-2) for fn, sec, dial, wds in a_lines)

print(f"A-dialect: {len(a_lines)} lines, {a_total} words, {a_total_bigrams} bigrams, {a_total_trigrams} trigrams")
print(f"B-dialect: {len(b_lines)} lines")

# --- H344: [daiin][cthol][cthy] and related trigrams ---
print("\n=== H344: [daiin][cthol][cthy] TRIGRAM AND RELATED 3-WORD CHAINS ===\n")

# Search for daiin-cthol-cthy trigram
target_trigrams = [
    ('daiin', 'cthol', 'cthy'),
    ('daiin', 'cthor', 'cthy'),
    ('daiin', 'cthol', 'cthol'),
    ('daiin', 'cthor', 'chol'),
    ('chol', 'cthol', 'cthy'),
    ('chor', 'cthol', 'cthy'),
    ('chol', 'cthor', 'cthy'),
]

print("Searching for specific 3-word chains (A-dialect):")
for w1, w2, w3 in target_trigrams:
    matches = []
    for fn, sec, dial, wds in a_lines:
        for i in range(len(wds)-2):
            if wds[i] == w1 and wds[i+1] == w2 and wds[i+2] == w3:
                matches.append((fn, sec, wds, i))
    print(f"\n  [{w1}][{w2}][{w3}]: {len(matches)} occurrences")
    for fn, sec, wds, i in matches:
        print(f"    f{fn} [{sec}]: {' '.join(wds)}")

# Search for onset-level trigrams involving cth
print("\n\nOnset trigrams involving cth as middle or last word (A-dialect):")
cth_trigram_counts = Counter()
for fn, sec, dial, wds in a_lines:
    for i in range(len(wds)-2):
        if get_onset(wds[i+1]) == 'cth' or get_onset(wds[i+2]) == 'cth':
            key = (get_onset(wds[i]), get_onset(wds[i+1]), get_onset(wds[i+2]))
            cth_trigram_counts[key] += 1

# Expected count for random trigram with cth
cth_rate = a_onset.get('cth', 0) / a_total
total_onset_combos = sum(cth_trigram_counts.values())

# Sort by count
print("\nTop onset trigrams involving cth (obs ≥5):")
print(f"{'o1':>8} {'o2':>8} {'o3':>8} {'obs':>6}")
for key, cnt in sorted(cth_trigram_counts.items(), key=lambda x: -x[1]):
    if cnt >= 5:
        print(f"  {key[0]:>8} {key[1]:>8} {key[2]:>8} {cnt:>6}")

# Specific daiin chains
print("\n\nAll A-dialect lines with daiin immediately before cthol:")
daiin_cthol_lines = [(fn, sec, dial, wds, i) for fn, sec, dial, wds in a_lines
                      for i in range(len(wds)-1) if wds[i] == 'daiin' and wds[i+1] == 'cthol']
print(f"[daiin][cthol] bigrams: {len(daiin_cthol_lines)}")
for fn, sec, dial, wds, i in daiin_cthol_lines:
    next_word = wds[i+2] if i+2 < len(wds) else '(end)'
    print(f"  f{fn} [{sec}]: {' '.join(wds)}  [next after cthol: {next_word}]")

print("\n\nAll A-dialect lines with cthol immediately before cthy:")
cthol_cthy_lines = [(fn, sec, dial, wds, i) for fn, sec, dial, wds in a_lines
                     for i in range(len(wds)-1) if wds[i] == 'cthol' and wds[i+1] == 'cthy']
print(f"[cthol][cthy] bigrams: {len(cthol_cthy_lines)}")
for fn, sec, dial, wds, i in cthol_cthy_lines:
    prev_word = wds[i-1] if i > 0 else '(start)'
    print(f"  f{fn} [{sec}]: {' '.join(wds)}  [prev before cthol: {prev_word}]")

# --- H343: qok→l specific pairs (A-dialect) ---
print("\n\n=== H343: qok→l SPECIFIC PAIRS IN A-DIALECT ===\n")
qok_l_pairs = Counter()
qok_l_examples = []
for fn, sec, dial, wds in a_lines:
    for i in range(len(wds)-1):
        if get_onset(wds[i]) == 'qok' and get_onset(wds[i+1]) == 'l':
            qok_l_pairs[(wds[i], wds[i+1])] += 1
            qok_l_examples.append((fn, sec, dial, wds, i))
total_qok_l = sum(qok_l_pairs.values())
print(f"Total qok→l pairs in A: {total_qok_l}")
print(f"Specific pairs:")
for (w1, w2), cnt in qok_l_pairs.most_common():
    print(f"  {w1} → {w2}: {cnt}×")
print(f"\nFull lines:")
for fn, sec, dial, wds, i in qok_l_examples:
    print(f"  f{fn} [{sec}]: {' '.join(wds)}")

# --- H342: B-dialect cthedy positional profile vs chedy/shedy ---
print("\n\n=== H342: B-DIALECT cthedy/cthdy vs chedy/shedy POSITIONAL PROFILES ===\n")

b_slot_baseline = Counter()
for fn, sec, dial, wds in b_lines:
    n = len(wds)
    for i in range(n):
        b_slot_baseline[get_slot(i, n)] += 1
b_slot_total = sum(b_slot_baseline.values())

def get_positional_profile(target_lines, target_word_pattern, label):
    """Get LF/second/MID/LL enrichment for a target word (exact match or onset match)."""
    slots = Counter()
    total = 0
    for fn, sec, dial, wds in target_lines:
        n = len(wds)
        for i, w in enumerate(wds):
            if target_word_pattern in w and (get_onset(w) == get_onset(target_word_pattern) or w == target_word_pattern):
                slots[get_slot(i, n)] += 1
                total += 1
    if total == 0:
        print(f"  {label}: no occurrences")
        return
    print(f"\n  {label} (n={total}):")
    for slot in ['LF','second','MID','LL']:
        cnt = slots.get(slot, 0)
        rate = cnt / total
        bl = b_slot_baseline.get(slot, 0) / b_slot_total
        enr = rate / bl if bl > 0 else float('inf')
        print(f"    {slot}: {cnt}/{total} = {rate:.3f} vs baseline {bl:.3f} = {enr:.2f}×")

print("Positional profiles of B-suffix words in B-dialect:")
for target in ['cthedy', 'cthdy', 'cthey', 'chedy', 'shedy', 'qokedy', 'qokeedy']:
    slots = Counter()
    total = 0
    for fn, sec, dial, wds in b_lines:
        n = len(wds)
        for i, w in enumerate(wds):
            if target in w and w.startswith(target[:3]):
                slots[get_slot(i, n)] += 1
                total += 1
    if total == 0:
        continue
    lf = slots.get('LF', 0) / total
    sec = slots.get('second', 0) / total
    mid = slots.get('MID', 0) / total
    ll = slots.get('LL', 0) / total
    lf_enr = lf / (b_slot_baseline.get('LF', 0) / b_slot_total)
    ll_enr = ll / (b_slot_baseline.get('LL', 0) / b_slot_total)
    mid_enr = mid / (b_slot_baseline.get('MID', 0) / b_slot_total)
    print(f"  {target:<12} n={total:>4}: LF={lf:.2f}({lf_enr:.2f}×) sec={sec:.2f} MID={mid:.2f}({mid_enr:.2f}×) LL={ll:.2f}({ll_enr:.2f}×)")

# Compare with A-dialect suffix words
print("\nA-dialect cth-word positional profiles for comparison:")
a_slot_baseline = Counter()
for fn, sec, dial, wds in a_lines:
    n = len(wds)
    for i in range(n):
        a_slot_baseline[get_slot(i, n)] += 1
a_slot_total = sum(a_slot_baseline.values())

for target in ['cthol', 'cthor', 'cthy', 'chol', 'shor']:
    slots = Counter()
    total = 0
    for fn, sec, dial, wds in a_lines:
        n = len(wds)
        for i, w in enumerate(wds):
            if w == target or w.startswith(target + ',') or w.startswith(target + '<'):
                slots[get_slot(i, n)] += 1
                total += 1
    if total == 0:
        continue
    lf = slots.get('LF', 0) / total
    sec_r = slots.get('second', 0) / total
    mid = slots.get('MID', 0) / total
    ll = slots.get('LL', 0) / total
    lf_enr = lf / (a_slot_baseline.get('LF', 0) / a_slot_total)
    ll_enr = ll / (a_slot_baseline.get('LL', 0) / a_slot_total)
    mid_enr = mid / (a_slot_baseline.get('MID', 0) / a_slot_total)
    print(f"  {target:<12} n={total:>4}: LF={lf:.2f}({lf_enr:.2f}×) sec={sec_r:.2f} MID={mid:.2f}({mid_enr:.2f}×) LL={ll:.2f}({ll_enr:.2f}×)")
