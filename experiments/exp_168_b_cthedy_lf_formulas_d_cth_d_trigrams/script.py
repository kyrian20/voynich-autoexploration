#!/usr/bin/env python3
"""
exp_168: B-cthedy LF-opening formulas (H345), [d][cth][d] specific trigrams (H346),
         B-cthdy LL cases (H347)
H345: B-cthedy/cthey@LF — what second word follows? Any line-opening formula?
H346: [d][cth][d]=16 onset-trigrams — are these literally [daiin][cth-word][daiin]?
H347: B-cthdy LL cases — all 7 occurrences, are they at LL?
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

# Baseline A-dialect onset counts for enrichment calculations
a_onset = Counter()
for fn, sec, dial, wds in a_lines:
    for w in wds:
        a_onset[get_onset(w)] += 1
a_total = sum(a_onset.values())

# Baseline B-dialect onset counts
b_onset = Counter()
for fn, sec, dial, wds in b_lines:
    for w in wds:
        b_onset[get_onset(w)] += 1
b_total = sum(b_onset.values())

# B baseline slot counts
b_slot_baseline = Counter()
for fn, sec, dial, wds in b_lines:
    n = len(wds)
    for i in range(n):
        b_slot_baseline[get_slot(i, n)] += 1
b_slot_total = sum(b_slot_baseline.values())

# =====================================================================
# H345: B-dialect cthedy/cthey at LF — second word analysis
# =====================================================================
print("=== H345: B-dialect cthedy/cthey@LF — LINE-OPENING FORMULAS ===\n")

for target in ['cthedy', 'cthey']:
    lf_occurrences = []
    all_occurrences = []
    for fn, sec, dial, wds in b_lines:
        for i, w in enumerate(wds):
            if w == target or (get_onset(w) == 'cth' and target in w):
                slot = get_slot(i, len(wds))
                all_occurrences.append((fn, sec, wds, i, slot))
                if slot == 'LF':
                    lf_occurrences.append((fn, sec, wds, i))

    print(f"--- B-dialect '{target}' (n={len(all_occurrences)} total, {len(lf_occurrences)} at LF) ---")

    # Positional distribution
    slot_counts = Counter()
    for fn, sec, wds, i, slot in all_occurrences:
        slot_counts[slot] += 1
    n_total = len(all_occurrences)
    for slot in ['LF', 'second', 'MID', 'LL', 'only']:
        cnt = slot_counts.get(slot, 0)
        rate = cnt / n_total if n_total > 0 else 0
        bl = b_slot_baseline.get(slot, 0) / b_slot_total
        enr = rate / bl if bl > 0 else float('inf')
        print(f"  @{slot}: {cnt}/{n_total} ({rate:.3f} vs baseline {bl:.3f} = {enr:.2f}×)")

    if lf_occurrences:
        print(f"\n  Lines where {target} is at LF:")
        second_words = []
        for fn, sec, wds, i in lf_occurrences:
            second = wds[i+1] if i+1 < len(wds) else '(EOL)'
            second_words.append(second)
            print(f"    f{fn} [{sec}]: {' '.join(wds)}")
            print(f"      → second word = '{second}' (onset={get_onset(second)})")

        second_onset_counts = Counter(get_onset(w) for w in second_words if w != '(EOL)')
        print(f"\n  Second-word onset distribution when {target}@LF:")
        for onset, cnt in second_onset_counts.most_common():
            print(f"    {onset}: {cnt}")
    print()

# Check all B cthedy/cthey lines (not just LF) for positional context
print("\n--- ALL B-dialect cthedy occurrences (lines) ---")
for fn, sec, dial, wds in b_lines:
    for i, w in enumerate(wds):
        if w == 'cthedy':
            slot = get_slot(i, len(wds))
            pred = wds[i-1] if i > 0 else '(SOL)'
            succ = wds[i+1] if i+1 < len(wds) else '(EOL)'
            print(f"  f{fn} [{sec}] @{slot}: {' '.join(wds)}")
            print(f"    pred={pred} (onset={get_onset(pred)}), succ={succ} (onset={get_onset(succ)})")

print("\n--- ALL B-dialect cthey occurrences (lines) ---")
for fn, sec, dial, wds in b_lines:
    for i, w in enumerate(wds):
        if w == 'cthey':
            slot = get_slot(i, len(wds))
            pred = wds[i-1] if i > 0 else '(SOL)'
            succ = wds[i+1] if i+1 < len(wds) else '(EOL)'
            print(f"  f{fn} [{sec}] @{slot}: {' '.join(wds)}")
            print(f"    pred={pred} (onset={get_onset(pred)}), succ={succ} (onset={get_onset(succ)})")

# =====================================================================
# H346: [d][cth][d] onset-trigrams — specific words
# =====================================================================
print("\n\n=== H346: [d][cth][d] ONSET-TRIGRAMS — SPECIFIC WORDS ===\n")

d_cth_d_cases = []
for fn, sec, dial, wds in a_lines:
    for i in range(len(wds)-2):
        if (get_onset(wds[i]) == 'd' and
            get_onset(wds[i+1]) == 'cth' and
            get_onset(wds[i+2]) == 'd'):
            d_cth_d_cases.append((fn, sec, dial, wds, i))

print(f"Total [d][cth][d] onset-trigrams in A: {len(d_cth_d_cases)}")

# Tally specific words
d_before = Counter()
cth_word = Counter()
d_after = Counter()
for fn, sec, dial, wds, i in d_cth_d_cases:
    d_before[wds[i]] += 1
    cth_word[wds[i+1]] += 1
    d_after[wds[i+2]] += 1

print(f"\nD-words BEFORE cth:")
for w, cnt in d_before.most_common():
    print(f"  {w}: {cnt}")
print(f"\ncth-words IN MIDDLE:")
for w, cnt in cth_word.most_common():
    print(f"  {w}: {cnt}")
print(f"\nD-words AFTER cth:")
for w, cnt in d_after.most_common():
    print(f"  {w}: {cnt}")

# How many are literally [daiin][cth-word][daiin]?
daiin_both = sum(1 for fn, sec, dial, wds, i in d_cth_d_cases
                 if wds[i] == 'daiin' and wds[i+2] == 'daiin')
daiin_before = sum(1 for fn, sec, dial, wds, i in d_cth_d_cases if wds[i] == 'daiin')
daiin_after = sum(1 for fn, sec, dial, wds, i in d_cth_d_cases if wds[i+2] == 'daiin')
print(f"\n[daiin][cth][daiin] specifically: {daiin_both}/{len(d_cth_d_cases)}")
print(f"[daiin][cth][d] (daiin before): {daiin_before}/{len(d_cth_d_cases)}")
print(f"[d][cth][daiin] (daiin after): {daiin_after}/{len(d_cth_d_cases)}")

print(f"\nAll [d][cth][d] trigrams:")
for fn, sec, dial, wds, i in d_cth_d_cases:
    slot_of_cth = get_slot(i+1, len(wds))
    print(f"  f{fn} [{sec}] cth@{slot_of_cth}: [{wds[i]}][{wds[i+1]}][{wds[i+2]}]  | full: {' '.join(wds)}")

# Also check if [ch][d][cth]=17 (the highest) — what d-words appear between ch and cth?
print(f"\n\n--- [ch][d][cth] onset-trigrams (A, highest=17) — specific words ---")
ch_d_cth_cases = []
for fn, sec, dial, wds in a_lines:
    for i in range(len(wds)-2):
        if (get_onset(wds[i]) == 'ch' and
            get_onset(wds[i+1]) == 'd' and
            get_onset(wds[i+2]) == 'cth'):
            ch_d_cth_cases.append((fn, sec, dial, wds, i))

print(f"Total [ch][d][cth] trigrams in A: {len(ch_d_cth_cases)}")
d_between = Counter(wds[i+1] for fn, sec, dial, wds, i in ch_d_cth_cases)
print("D-word between ch and cth:")
for w, cnt in d_between.most_common():
    print(f"  {w}: {cnt}")
cth_in_ch_d_cth = Counter(wds[i+2] for fn, sec, dial, wds, i in ch_d_cth_cases)
print("cth-word at end:")
for w, cnt in cth_in_ch_d_cth.most_common():
    print(f"  {w}: {cnt}")

# =====================================================================
# H347: B-cthdy LL cases — all 7 occurrences
# =====================================================================
print("\n\n=== H347: B-dialect cthdy — ALL OCCURRENCES AND POSITIONAL ANALYSIS ===\n")

cthdy_cases = []
for fn, sec, dial, wds in b_lines:
    for i, w in enumerate(wds):
        if w == 'cthdy':
            slot = get_slot(i, len(wds))
            pred = wds[i-1] if i > 0 else '(SOL)'
            succ = wds[i+1] if i+1 < len(wds) else '(EOL)'
            cthdy_cases.append((fn, sec, wds, i, slot, pred, succ))

print(f"Total B-dialect cthdy occurrences: {len(cthdy_cases)}")
slot_dist = Counter(slot for fn, sec, wds, i, slot, pred, succ in cthdy_cases)
for slot in ['LF', 'second', 'MID', 'LL', 'only']:
    cnt = slot_dist.get(slot, 0)
    rate = cnt / len(cthdy_cases) if cthdy_cases else 0
    bl = b_slot_baseline.get(slot, 0) / b_slot_total
    enr = rate / bl if bl > 0 else float('inf')
    print(f"  @{slot}: {cnt} ({rate:.3f} vs baseline {bl:.3f} = {enr:.2f}×)")

print(f"\nAll B-dialect cthdy occurrences:")
for fn, sec, wds, i, slot, pred, succ in cthdy_cases:
    print(f"  f{fn} [{sec}] @{slot}: {' '.join(wds)}")
    print(f"    pred='{pred}', succ='{succ}'")

# Compare to A-dialect cthy LL-enrichment (for parallel)
print(f"\n--- A-dialect cthy positional profile (for comparison) ---")
cthy_slots = Counter()
for fn, sec, dial, wds in a_lines:
    n = len(wds)
    for i, w in enumerate(wds):
        if w == 'cthy':
            cthy_slots[get_slot(i, n)] += 1
cthy_total = sum(cthy_slots.values())

a_slot_baseline = Counter()
for fn, sec, dial, wds in a_lines:
    n = len(wds)
    for i in range(n):
        a_slot_baseline[get_slot(i, n)] += 1
a_slot_total = sum(a_slot_baseline.values())

print(f"A-dialect cthy (n={cthy_total}):")
for slot in ['LF', 'second', 'MID', 'LL', 'only']:
    cnt = cthy_slots.get(slot, 0)
    rate = cnt / cthy_total if cthy_total > 0 else 0
    bl = a_slot_baseline.get(slot, 0) / a_slot_total
    enr = rate / bl if bl > 0 else float('inf')
    print(f"  @{slot}: {cnt}/{cthy_total} ({rate:.3f} vs baseline {bl:.3f} = {enr:.2f}×)")

# Also: compare cthdy with other B-edy-suffix line-closers
print(f"\n--- B-dialect LL-enrichment for various -dy forms ---")
for target_word in ['cthdy', 'chedy', 'shedy', 'qokedy', 'qokeedy']:
    ll_count = 0
    total = 0
    for fn, sec, dial, wds in b_lines:
        n = len(wds)
        for i, w in enumerate(wds):
            if w == target_word:
                total += 1
                if get_slot(i, n) == 'LL':
                    ll_count += 1
    bl_ll = b_slot_baseline.get('LL', 0) / b_slot_total
    ll_rate = ll_count / total if total > 0 else 0
    enr = ll_rate / bl_ll if bl_ll > 0 else 0
    print(f"  {target_word}: LL={ll_count}/{total} ({ll_rate:.3f} vs baseline {bl_ll:.3f} = {enr:.2f}×)")
