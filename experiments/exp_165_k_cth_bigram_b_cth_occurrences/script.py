#!/usr/bin/env python3
"""
exp_165: k→cth bigram in A (H335), B-dialect cth occurrences and ch→cth bigrams (H337),
         ch→r specifics (H336), t→ot specifics (H334)
H335: Which k-words precede cth in A? New 6th cth-introduction construction?
H337: 8 B-dialect ch→cth bigrams — which sections? What cth-words?
H336: 15 A-dialect ch→r pairs — which words?
H334: 16 A-dialect t→ot pairs — which words?
"""
from pathlib import Path as _RepositoryPath
import re
from collections import Counter, defaultdict

CORPUS = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

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
for fn, wds in folio_words.items():
    if len(wds) < 10: continue
    edy_count = sum(1 for w in wds if 'edy' in w or 'eedy' in w)
    folio_dialect[fn] = 'B' if edy_count / len(wds) >= 0.05 else 'A'

lines_data = []
for folio_num, words in raw_lines:
    dialect = folio_dialect.get(folio_num, 'unknown')
    section = folio_to_section.get(folio_num, 'other')
    lines_data.append((folio_num, section, dialect, words))

a_lines = [(fn, sec, dial, wds) for fn, sec, dial, wds in lines_data if dial == 'A']
b_lines = [(fn, sec, dial, wds) for fn, sec, dial, wds in lines_data if dial == 'B']

# Baseline counts
a_onset = Counter()
for fn, sec, dial, wds in a_lines:
    for w in wds:
        a_onset[get_onset(w)] += 1
a_total = sum(a_onset.values())

def find_bigrams(target_lines, o1, o2, label):
    """Find all [o1-word][o2-word] consecutive pairs."""
    pairs = Counter()
    examples = []
    for fn, sec, dial, wds in target_lines:
        for i in range(len(wds)-1):
            if get_onset(wds[i]) == o1 and get_onset(wds[i+1]) == o2:
                pairs[(wds[i], wds[i+1])] += 1
                examples.append((fn, sec, dial, wds, i))
    total = sum(pairs.values())
    print(f"\n{label}: [{o1}][{o2}] total={total}")
    print(f"Specific word pairs:")
    for (w1, w2), cnt in pairs.most_common(20):
        slot1 = None
        for fn, sec, dial, wds, i in examples:
            if wds[i] == w1 and wds[i+1] == w2:
                slot1 = get_slot(i, len(wds))
                break
        print(f"  {w1}({slot1}) → {w2}: {cnt}×")
    print(f"Examples (full lines):")
    for fn, sec, dial, wds, i in examples[:20]:
        print(f"  f{fn} [{sec}/{dial}]: {' '.join(wds)}  [{wds[i]} → {wds[i+1]} at i={i}]")
    return pairs, examples

# --- H335: k→cth in A-dialect ---
print("=== H335: k→cth BIGRAMS IN A-DIALECT (n=18) ===")
k_cth_pairs, k_cth_ex = find_bigrams(a_lines, 'k', 'cth', "k→cth in A")

# Breakdown by positional slot of k-word
print(f"\nPositional slot of k-word in k→cth bigrams:")
slot_counts = Counter()
for fn, sec, dial, wds, i in k_cth_ex:
    slot_counts[get_slot(i, len(wds))] += 1
for slot, cnt in slot_counts.most_common():
    print(f"  k@{slot}: {cnt}")

# --- H336: ch→r in A-dialect ---
print("\n\n=== H336: ch→r BIGRAMS IN A-DIALECT (n=15) ===")
ch_r_pairs, ch_r_ex = find_bigrams(a_lines, 'ch', 'r', "ch→r in A")

# Also r→ch
print("\n=== r→ch BIGRAMS IN A-DIALECT ===")
r_ch_pairs, r_ch_ex = find_bigrams(a_lines, 'r', 'ch', "r→ch in A")

# --- H334: t→ot in A-dialect ---
print("\n\n=== H334: t→ot BIGRAMS IN A-DIALECT (n=16) ===")
t_ot_pairs, t_ot_ex = find_bigrams(a_lines, 't', 'ot', "t→ot in A")

# --- H337: B-dialect cth occurrences ---
print("\n\n=== H337: B-DIALECT cth OCCURRENCES ===\n")

# All cth-words in B-dialect
b_cth_words = Counter()
b_cth_contexts = []
for fn, sec, dial, wds in b_lines:
    for i, w in enumerate(wds):
        if get_onset(w) == 'cth':
            b_cth_words[w] += 1
            b_cth_contexts.append((fn, sec, dial, wds, i))

print(f"Total B-dialect cth-word occurrences: {sum(b_cth_words.values())}")
print(f"B-dialect cth-word types: {len(b_cth_words)}")
print(f"\nTop B-dialect cth-words:")
for w, cnt in b_cth_words.most_common(20):
    print(f"  {w}: {cnt}")

# B-dialect ch→cth bigrams
print(f"\nB-dialect ch→cth bigrams (n=8):")
ch_cth_b, ch_cth_b_ex = find_bigrams(b_lines, 'ch', 'cth', "ch→cth in B")

# Section distribution of all B cth occurrences
print(f"\nSection distribution of B cth occurrences:")
sec_counts = Counter()
for fn, sec, dial, wds, i in b_cth_contexts:
    sec_counts[sec] += 1
for sec, cnt in sec_counts.most_common():
    print(f"  {sec}: {cnt}")

# Full lines of B ch→cth
print(f"\nFull lines with B ch→cth bigrams:")
for fn, sec, dial, wds, i in ch_cth_b_ex:
    print(f"  f{fn} [{sec}/{dial}]: {' '.join(wds)}  [ch→cth: {wds[i]}→{wds[i+1]}]")

# Also check ALL B cth-occurrence lines (not just ch→cth)
print(f"\nAll lines where B-dialect has a cth-word (unique lines, up to 30):")
seen = set()
for fn, sec, dial, wds, i in b_cth_contexts:
    key = (fn, ' '.join(wds))
    if key not in seen:
        seen.add(key)
        cth_positions = [j for j, w in enumerate(wds) if get_onset(w) == 'cth']
        print(f"  f{fn} [{sec}/{dial}]: {' '.join(wds)}  [cth at positions {cth_positions}: {[wds[j] for j in cth_positions]}]")

# --- BONUS: Expanded cth introduction grammar model ---
print("\n\n=== EXPANDED cth INTRODUCTION GRAMMAR MODEL (A-dialect) ===\n")
print("All onset classes that precede cth in A-dialect (bigram level):")

a_bigram_pre_cth = Counter()
a_bigram_pre_cth_words = Counter()
for fn, sec, dial, wds in a_lines:
    for i in range(1, len(wds)):
        if get_onset(wds[i]) == 'cth':
            a_bigram_pre_cth[get_onset(wds[i-1])] += 1
            a_bigram_pre_cth_words[(wds[i-1], wds[i])] += 1

total_pre_cth = sum(a_bigram_pre_cth.values())
print(f"Total A-dialect cth-word occurrences with a predecessor: {total_pre_cth}")
print(f"\nPredecessor onset distribution:")
print(f"{'Onset':<10} {'n':>5} {'rate':>8} {'baseline':>10} {'enrich':>8}")
for onset in ['ch','ch_e','d','y','sh','ok','ot','cth','k','qok','qot','qo','s','t','l','r','other']:
    cnt = a_bigram_pre_cth.get(onset, 0)
    if cnt == 0: continue
    rate = cnt / total_pre_cth
    bl = a_onset.get(onset, 0) / a_total
    enrich = rate / bl if bl > 0 else float('inf')
    print(f"  {onset:<10} {cnt:>5} {rate:>8.3f} {bl:>10.4f} {enrich:>8.2f}×")

print(f"\nTop specific predecessor words before cth:")
for (pre, cth_w), cnt in a_bigram_pre_cth_words.most_common(20):
    print(f"  {pre} → {cth_w}: {cnt}×")
