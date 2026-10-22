#!/usr/bin/env python3
"""
exp_169: [ch][daiin][cth] compound analysis (H348), cthol d-word asymmetry (H349),
         cthey → ch_e affinity (H350)
H348: Is [ch-word][daiin] a stable compound precursor to cth-words?
H349: Does cthol have asymmetric d-word preferences (daiin left, non-daiin right)?
H350: Does cthey specifically attract ch_e-type successor words (beyond LF)?
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

# Baseline B-dialect onset counts
b_onset = Counter()
for fn, sec, dial, wds in b_lines:
    for w in wds:
        b_onset[get_onset(w)] += 1
b_total = sum(b_onset.values())

# =====================================================================
# H348: [ch][daiin][cth] compound — specific ch-words and cth-words
# =====================================================================
print("=== H348: [ch][daiin][cth] TRIGRAMS — SPECIFIC WORDS ===\n")

ch_daiin_cth_cases = []
for fn, sec, dial, wds in a_lines:
    for i in range(len(wds)-2):
        if (get_onset(wds[i]) == 'ch' and
            wds[i+1] == 'daiin' and
            get_onset(wds[i+2]) == 'cth'):
            ch_daiin_cth_cases.append((fn, sec, wds, i))

print(f"[ch][daiin][cth] (with daiin literally): {len(ch_daiin_cth_cases)}")

ch_words_before = Counter()
cth_words_after = Counter()
for fn, sec, wds, i in ch_daiin_cth_cases:
    ch_words_before[wds[i]] += 1
    cth_words_after[wds[i+2]] += 1

print(f"\nch-words BEFORE daiin-cth:")
for w, cnt in ch_words_before.most_common():
    print(f"  {w}: {cnt}")
print(f"\ncth-words AFTER daiin:")
for w, cnt in cth_words_after.most_common():
    print(f"  {w}: {cnt}")

print(f"\nAll [ch][daiin][cth] trigrams:")
for fn, sec, wds, i in ch_daiin_cth_cases:
    slot_daiin = get_slot(i+1, len(wds))
    print(f"  f{fn} [{sec}] daiin@{slot_daiin}: [{wds[i]}][daiin][{wds[i+2]}]  | full: {' '.join(wds)}")

# Now check: is [ch][daiin] in general a bigram that precedes cth?
# Compare [ch][daiin] → cth vs all [ch][daiin] bigrams
print(f"\n\n--- [ch][daiin] bigram enrichment analysis ---")
ch_daiin_total = 0
ch_daiin_then_cth = 0
ch_daiin_successors = Counter()
for fn, sec, dial, wds in a_lines:
    for i in range(len(wds)-2):
        if get_onset(wds[i]) == 'ch' and wds[i+1] == 'daiin':
            ch_daiin_total += 1
            if i+2 < len(wds):
                ch_daiin_successors[get_onset(wds[i+2])] += 1
                if get_onset(wds[i+2]) == 'cth':
                    ch_daiin_then_cth += 1

print(f"Total [ch][daiin] bigrams in A: {ch_daiin_total}")
print(f"[ch][daiin] → cth: {ch_daiin_then_cth}/{ch_daiin_total}")
cth_base = a_onset.get('cth', 0) / a_total
expected_cth = ch_daiin_total * cth_base
print(f"Expected [ch][daiin] → cth (baseline): {expected_cth:.1f}")
print(f"Enrichment: {ch_daiin_then_cth/expected_cth:.2f}× (if > 0)")

print(f"\n[ch][daiin] successor onset distribution:")
for onset, cnt in ch_daiin_successors.most_common(12):
    rate = cnt / ch_daiin_total if ch_daiin_total > 0 else 0
    bl = a_onset.get(onset, 0) / a_total
    enr = rate / bl if bl > 0 else float('inf')
    print(f"  {onset}: {cnt} ({rate:.3f} vs {bl:.3f}) = {enr:.2f}×")

# Compare to [daiin] alone → cth enrichment
daiin_total = sum(1 for fn, sec, dial, wds in a_lines for w in wds if w == 'daiin')
daiin_bigrams = 0
daiin_then_cth = 0
for fn, sec, dial, wds in a_lines:
    for i in range(len(wds)-1):
        if wds[i] == 'daiin':
            daiin_bigrams += 1
            if get_onset(wds[i+1]) == 'cth':
                daiin_then_cth += 1

daiin_cth_rate = daiin_then_cth / daiin_bigrams if daiin_bigrams > 0 else 0
print(f"\n[daiin] → cth bigram rate: {daiin_then_cth}/{daiin_bigrams} = {daiin_cth_rate:.4f}")
print(f"Expected from baseline: {cth_base:.4f}")
print(f"[daiin] → cth enrichment: {daiin_cth_rate/cth_base:.2f}×")

# Is [ch][daiin] enriched as a bigram overall vs [ch] alone → daiin?
# ch → daiin rate
ch_bigrams = 0
ch_then_daiin = 0
for fn, sec, dial, wds in a_lines:
    for i in range(len(wds)-1):
        if get_onset(wds[i]) == 'ch':
            ch_bigrams += 1
            if wds[i+1] == 'daiin':
                ch_then_daiin += 1

ch_daiin_rate = ch_then_daiin / ch_bigrams if ch_bigrams > 0 else 0
daiin_base = daiin_total / a_total
print(f"\n[ch] → daiin rate: {ch_then_daiin}/{ch_bigrams} = {ch_daiin_rate:.4f}")
print(f"Expected from baseline: {daiin_base:.4f}")
print(f"[ch] → daiin enrichment: {ch_daiin_rate/daiin_base:.2f}×")

# =====================================================================
# H349: cthol d-word asymmetry — daiin left vs non-daiin right
# =====================================================================
print("\n\n=== H349: cthol D-WORD ASYMMETRY (daiin LEFT vs diverse RIGHT) ===\n")

# All [d][cthol] bigrams in A
d_before_cthol = Counter()
daiin_before_cthol = 0
d_before_cthol_total = 0
for fn, sec, dial, wds in a_lines:
    for i in range(len(wds)-1):
        if wds[i+1] == 'cthol' and get_onset(wds[i]) == 'd':
            d_before_cthol[wds[i]] += 1
            d_before_cthol_total += 1
            if wds[i] == 'daiin':
                daiin_before_cthol += 1

print(f"All [d][cthol] bigrams in A (n={d_before_cthol_total}):")
for w, cnt in d_before_cthol.most_common():
    print(f"  {w}: {cnt}")
print(f"daiin specifically before cthol: {daiin_before_cthol}/{d_before_cthol_total} = {daiin_before_cthol/d_before_cthol_total:.3f}")

# All [cthol][d] bigrams in A
d_after_cthol = Counter()
daiin_after_cthol = 0
d_after_cthol_total = 0
for fn, sec, dial, wds in a_lines:
    for i in range(len(wds)-1):
        if wds[i] == 'cthol' and get_onset(wds[i+1]) == 'd':
            d_after_cthol[wds[i+1]] += 1
            d_after_cthol_total += 1
            if wds[i+1] == 'daiin':
                daiin_after_cthol += 1

print(f"\nAll [cthol][d] bigrams in A (n={d_after_cthol_total}):")
for w, cnt in d_after_cthol.most_common():
    print(f"  {w}: {cnt}")
print(f"daiin specifically after cthol: {daiin_after_cthol}/{d_after_cthol_total} = {daiin_after_cthol/d_after_cthol_total:.3f}" if d_after_cthol_total > 0 else "daiin after cthol: 0/0")

# Full cthol predecessor/successor distribution (all onsets, not just d)
cthol_pred = Counter()
cthol_succ = Counter()
cthol_total = 0
for fn, sec, dial, wds in a_lines:
    for i, w in enumerate(wds):
        if w == 'cthol':
            cthol_total += 1
            if i > 0: cthol_pred[get_onset(wds[i-1])] += 1
            if i < len(wds)-1: cthol_succ[get_onset(wds[i+1])] += 1

print(f"\nTotal cthol in A: {cthol_total}")
print(f"\ncthol PREDECESSOR onset distribution:")
for onset, cnt in cthol_pred.most_common(10):
    rate = cnt / sum(cthol_pred.values())
    bl = a_onset.get(onset, 0) / a_total
    enr = rate / bl if bl > 0 else float('inf')
    print(f"  {onset}: {cnt} ({rate:.3f} vs {bl:.3f}) = {enr:.2f}×")

print(f"\ncthol SUCCESSOR onset distribution:")
for onset, cnt in cthol_succ.most_common(10):
    rate = cnt / sum(cthol_succ.values())
    bl = a_onset.get(onset, 0) / a_total
    enr = rate / bl if bl > 0 else float('inf')
    print(f"  {onset}: {cnt} ({rate:.3f} vs {bl:.3f}) = {enr:.2f}×")

# Also check: what specifically follows cthol (top specific words)
cthol_succ_words = Counter()
for fn, sec, dial, wds in a_lines:
    for i, w in enumerate(wds):
        if w == 'cthol' and i < len(wds)-1:
            cthol_succ_words[wds[i+1]] += 1
print(f"\ncthol successor WORDS (top 15):")
for w, cnt in cthol_succ_words.most_common(15):
    print(f"  {w}: {cnt}")

# =====================================================================
# H350: cthey → ch_e affinity (all positions)
# =====================================================================
print("\n\n=== H350: cthey SUCCESSOR ONSET DISTRIBUTION (ALL B-DIALECT POSITIONS) ===\n")

cthey_succ = Counter()
cthey_total_with_succ = 0
for fn, sec, dial, wds in b_lines:
    for i, w in enumerate(wds):
        if w == 'cthey' and i < len(wds)-1:
            cthey_succ[get_onset(wds[i+1])] += 1
            cthey_total_with_succ += 1

print(f"cthey total with successor: {cthey_total_with_succ}")
print(f"\ncthey SUCCESSOR onset distribution:")
for onset, cnt in cthey_succ.most_common():
    rate = cnt / cthey_total_with_succ if cthey_total_with_succ > 0 else 0
    bl = b_onset.get(onset, 0) / b_total
    enr = rate / bl if bl > 0 else float('inf')
    print(f"  {onset}: {cnt} ({rate:.3f} vs baseline {bl:.3f}) = {enr:.2f}×")

# What about cthey predecessor distribution?
cthey_pred = Counter()
for fn, sec, dial, wds in b_lines:
    for i, w in enumerate(wds):
        if w == 'cthey' and i > 0:
            cthey_pred[get_onset(wds[i-1])] += 1

print(f"\ncthey PREDECESSOR onset distribution:")
for onset, cnt in cthey_pred.most_common():
    rate = cnt / sum(cthey_pred.values())
    bl = b_onset.get(onset, 0) / b_total
    enr = rate / bl if bl > 0 else float('inf')
    print(f"  {onset}: {cnt} ({rate:.3f} vs baseline {bl:.3f}) = {enr:.2f}×")

# Compare: cthedy successor onset distribution
print(f"\n\n--- cthedy SUCCESSOR onset distribution (for comparison) ---")
cthedy_succ = Counter()
cthedy_total_with_succ = 0
for fn, sec, dial, wds in b_lines:
    for i, w in enumerate(wds):
        if w == 'cthedy' and i < len(wds)-1:
            cthedy_succ[get_onset(wds[i+1])] += 1
            cthedy_total_with_succ += 1

print(f"cthedy total with successor: {cthedy_total_with_succ}")
for onset, cnt in cthedy_succ.most_common():
    rate = cnt / cthedy_total_with_succ if cthedy_total_with_succ > 0 else 0
    bl = b_onset.get(onset, 0) / b_total
    enr = rate / bl if bl > 0 else float('inf')
    print(f"  {onset}: {cnt} ({rate:.3f} vs baseline {bl:.3f}) = {enr:.2f}×")

# Also: compare cthey@LF vs cthey@non-LF successor patterns
print(f"\n--- cthey successor onset by position ---")
for target_slot in ['LF', 'second', 'MID']:
    succ_by_slot = Counter()
    for fn, sec, dial, wds in b_lines:
        n = len(wds)
        for i, w in enumerate(wds):
            if w == 'cthey' and get_slot(i, n) == target_slot and i < n-1:
                succ_by_slot[get_onset(wds[i+1])] += 1
    total_slot = sum(succ_by_slot.values())
    if total_slot > 0:
        print(f"  cthey@{target_slot} successors (n={total_slot}): {dict(succ_by_slot.most_common(5))}")

# Bonus: survey ALL B-dialect cth-words' successor onset distributions
print(f"\n\n=== BONUS: B-dialect cth-words SUCCESSOR ONSET DISTRIBUTIONS ===\n")
for target_word in ['cthedy', 'cthey', 'cthdy']:
    succ = Counter()
    for fn, sec, dial, wds in b_lines:
        for i, w in enumerate(wds):
            if w == target_word and i < len(wds)-1:
                succ[get_onset(wds[i+1])] += 1
    total = sum(succ.values())
    print(f"{target_word} (n={total} with succ): top successors")
    for onset, cnt in succ.most_common(6):
        rate = cnt / total if total > 0 else 0
        bl = b_onset.get(onset, 0) / b_total
        enr = rate / bl if bl > 0 else float('inf')
        print(f"  → {onset}: {cnt} ({rate:.3f} vs {bl:.3f}) = {enr:.2f}×")
    print()
