#!/usr/bin/env python3
"""
exp_166: B-dialect cth vocabulary analysis (H338, H341), cth self-succession pairs (H340),
         qok depletion before cth (H339)
H338: Is B-dialect cthedy/cthdy genuine B-vocabulary? Check bigram context.
H339: qok→cth depletion: structural or frequency artifact?
H340: cth→cth self-succession specific pairs
H341: f46 dialect analysis vs neighboring folios
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
folio_lines = defaultdict(list)
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
        folio_lines[folio_num].append(words)
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

# Baseline A-dialect onset counts
a_onset = Counter()
for fn, sec, dial, wds in a_lines:
    for w in wds:
        a_onset[get_onset(w)] += 1
a_total = sum(a_onset.values())

# --- H341: f46 folio analysis ---
print("=== H341: f46 (B-HERBAL) FOLIO ANALYSIS ===\n")

# edy rates for f43-f50 range
print("Folio edy rates (f40-f55 range):")
for fn in range(40, 56):
    if fn in folio_edy_rate:
        dial = folio_dialect.get(fn, '?')
        total_words = len(folio_words.get(fn, []))
        cth_count = sum(1 for w in folio_words.get(fn, []) if get_onset(w) == 'cth')
        cth_rate = cth_count / total_words if total_words > 0 else 0
        print(f"  f{fn} [{folio_to_section.get(fn,'?')}/{dial}]: edy_rate={folio_edy_rate[fn]:.3f}, total_words={total_words}, cth={cth_count} ({cth_rate:.3f})")

print("\nFolio f46 lines:")
for wds in folio_lines.get(46, []):
    cth_words = [w for w in wds if get_onset(w) == 'cth']
    marker = f" *** CTH: {cth_words}" if cth_words else ""
    print(f"  {' '.join(wds)}{marker}")

# --- H340: cth self-succession pairs ---
print("\n\n=== H340: cth SELF-SUCCESSION PAIRS IN A-DIALECT ===\n")
cth_cth_pairs = Counter()
cth_cth_examples = []
for fn, sec, dial, wds in a_lines:
    for i in range(len(wds)-1):
        if get_onset(wds[i]) == 'cth' and get_onset(wds[i+1]) == 'cth':
            pair = (wds[i], wds[i+1])
            cth_cth_pairs[pair] += 1
            cth_cth_examples.append((fn, sec, dial, wds, i))

total_cth_cth = sum(cth_cth_pairs.values())
print(f"Total cth→cth consecutive pairs in A: {total_cth_cth}")
print(f"\nSpecific pairs:")
for (c1, c2), cnt in cth_cth_pairs.most_common(20):
    onset1 = get_onset(c1)
    print(f"  {c1} → {c2}: {cnt}×")

print(f"\nFull lines with cth→cth:")
for fn, sec, dial, wds, i in cth_cth_examples[:25]:
    print(f"  f{fn} [{sec}/{dial}]: {' '.join(wds)}  [{wds[i]}→{wds[i+1]} at i={i}]")

# --- H339: qok→cth depletion ---
print("\n\n=== H339: qok→cth DEPLETION ANALYSIS (A-dialect) ===\n")
# qok baseline in A
qok_total_a = a_onset.get('qok', 0)
cth_total_a = a_onset.get('cth', 0)
print(f"qok tokens in A: {qok_total_a} ({qok_total_a/a_total:.4f})")
print(f"cth tokens in A: {cth_total_a} ({cth_total_a/a_total:.4f})")

# Count qok→cth bigrams
qok_cth_count = 0
qok_total_bigrams = 0
for fn, sec, dial, wds in a_lines:
    for i in range(len(wds)-1):
        if get_onset(wds[i]) == 'qok':
            qok_total_bigrams += 1
            if get_onset(wds[i+1]) == 'cth':
                qok_cth_count += 1

expected_qok_cth = qok_total_bigrams * (cth_total_a / a_total)
enrich = qok_cth_count / expected_qok_cth if expected_qok_cth > 0 else 0
print(f"\nqok bigrams in A: {qok_total_bigrams}")
print(f"qok→cth observed: {qok_cth_count}")
print(f"qok→cth expected: {expected_qok_cth:.1f}")
print(f"qok→cth enrichment: {enrich:.2f}×")

# What does qok→ lead to in A?
qok_successors = Counter()
for fn, sec, dial, wds in a_lines:
    for i in range(len(wds)-1):
        if get_onset(wds[i]) == 'qok':
            qok_successors[get_onset(wds[i+1])] += 1
print(f"\nqok successor onset distribution in A:")
for onset, cnt in qok_successors.most_common():
    rate = cnt / qok_total_bigrams if qok_total_bigrams > 0 else 0
    bl = a_onset.get(onset, 0) / a_total
    enr = rate / bl if bl > 0 else float('inf')
    print(f"  qok → {onset}: {cnt} ({rate:.3f}) vs baseline {bl:.3f} = {enr:.2f}×")

# --- H338: B-dialect cthedy/cthdy bigram context analysis ---
print("\n\n=== H338: B-DIALECT cthedy/cthdy BIGRAM CONTEXT ANALYSIS ===\n")

# Find all B-dialect lines with cthedy, cthdy, cthey
b_cth_forms = ['cthedy', 'cthdy', 'cthey', 'cthy', 'cthar', 'cthol', 'cthor', 'ctheey']

for target_word in ['cthedy', 'cthdy', 'cthey']:
    occurrences = []
    for fn, sec, dial, wds in b_lines:
        for i, w in enumerate(wds):
            if target_word in w and get_onset(w) == 'cth':
                occurrences.append((fn, sec, dial, wds, i))

    print(f"\n--- B-dialect '{target_word}' occurrences (n={len(occurrences)}) ---")
    if not occurrences:
        print("  (none found)")
        continue

    # Predecessor onset distribution
    pred_onsets = Counter()
    succ_onsets = Counter()
    for fn, sec, dial, wds, i in occurrences:
        if i > 0:
            pred_onsets[get_onset(wds[i-1])] += 1
        if i < len(wds)-1:
            succ_onsets[get_onset(wds[i+1])] += 1

    print(f"  Predecessor onsets:")
    for onset, cnt in pred_onsets.most_common():
        print(f"    {onset}: {cnt}")
    print(f"  Successor onsets:")
    for onset, cnt in succ_onsets.most_common():
        print(f"    {onset}: {cnt}")

    # Check sections
    sec_counts = Counter()
    for fn, sec, dial, wds, i in occurrences:
        sec_counts[sec] += 1
    print(f"  Sections: {dict(sec_counts)}")

    # Are these lines high-edy-rate?
    edy_rates = [folio_edy_rate.get(fn, 0) for fn, sec, dial, wds, i in occurrences]
    avg_edy = sum(edy_rates) / len(edy_rates) if edy_rates else 0
    print(f"  Avg folio edy-rate of lines containing {target_word}: {avg_edy:.3f}")

    print(f"  Full lines:")
    for fn, sec, dial, wds, i in occurrences:
        print(f"    f{fn} [{sec}/{dial}] (edy_rate={folio_edy_rate.get(fn,0):.3f}): {' '.join(wds)}")

# --- B-dialect cth-word positional analysis ---
print("\n\n=== B-DIALECT cth-WORD POSITIONAL PROFILE ===\n")
b_cth_slots = Counter()
for fn, sec, dial, wds in b_lines:
    for i, w in enumerate(wds):
        if get_onset(w) == 'cth':
            b_cth_slots[get_slot(i, len(wds))] += 1

b_cth_total = sum(b_cth_slots.values())
# B-dialect baseline slots
b_slot_baseline = Counter()
for fn, sec, dial, wds in b_lines:
    n = len(wds)
    for i in range(n):
        b_slot_baseline[get_slot(i, n)] += 1
b_slot_total = sum(b_slot_baseline.values())

print(f"B-dialect cth positional distribution (n={b_cth_total}):")
for slot in ['LF','second','MID','LL','only']:
    cnt = b_cth_slots.get(slot, 0)
    rate = cnt / b_cth_total if b_cth_total > 0 else 0
    bl = b_slot_baseline.get(slot, 0) / b_slot_total
    enr = rate / bl if bl > 0 else float('inf')
    print(f"  cth@{slot}: {cnt} ({rate:.3f} vs baseline {bl:.3f}) = {enr:.2f}×")

# Compare to A-dialect cth positional distribution
a_cth_slots = Counter()
a_slot_baseline = Counter()
for fn, sec, dial, wds in a_lines:
    n = len(wds)
    for i in range(n):
        a_slot_baseline[get_slot(i, n)] += 1
        if get_onset(wds[i]) == 'cth':
            a_cth_slots[get_slot(i, len(wds))] += 1
a_cth_total = sum(a_cth_slots.values())
a_slot_total = sum(a_slot_baseline.values())

print(f"\nA-dialect cth positional distribution (n={a_cth_total}) for comparison:")
for slot in ['LF','second','MID','LL','only']:
    cnt = a_cth_slots.get(slot, 0)
    rate = cnt / a_cth_total if a_cth_total > 0 else 0
    bl = a_slot_baseline.get(slot, 0) / a_slot_total
    enr = rate / bl if bl > 0 else float('inf')
    print(f"  cth@{slot}: {cnt} ({rate:.3f} vs baseline {bl:.3f}) = {enr:.2f}×")
