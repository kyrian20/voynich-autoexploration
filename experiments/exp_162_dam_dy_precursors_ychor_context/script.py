#!/usr/bin/env python3
"""
exp_162: What precedes dam@LL and dy@LL (H321); [ychor cthy...] full context (H323)
H321: dam and dy are strong LL-closers (3.98×, 3.02×). What is the penultimate word?
  Is [X][dam@LL] or [X][dy@LL] a specific bigram construction?
H323: [ychor][cthy@second] appears 2 times. What follows cthy at position 2? What folios?
"""
from pathlib import Path as _RepositoryPath
import re
from collections import Counter, defaultdict

CORPUS = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

ONSET_ORDER = ['qok','qot','qo','cth','ch_e','ch','sh','ok','ot','ol','d','s','y','k','t','l','r','p','f']

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
    """Return (folio_num, line_type) or (None, None) on failure."""
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

# First pass: folio word lists for dialect detection
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

print(f"Total P-type lines parsed: {len(raw_lines)}")
print(f"Total folios: {len(folio_words)}")

# Dialect assignment
folio_dialect = {}
for fn, wds in folio_words.items():
    if len(wds) < 10: continue
    edy_count = sum(1 for w in wds if 'edy' in w or 'eedy' in w)
    folio_dialect[fn] = 'B' if edy_count / len(wds) >= 0.05 else 'A'

# Annotate lines with dialect and section
lines_data = []
for folio_num, words in raw_lines:
    dialect = folio_dialect.get(folio_num, 'unknown')
    section = folio_to_section.get(folio_num, 'other')
    lines_data.append((folio_num, section, dialect, words))

a_lines = [(fn, sec, dial, wds) for fn, sec, dial, wds in lines_data if dial == 'A']
print(f"A-dialect lines: {len(a_lines)}")

# Baseline: all word tokens in A-dialect
baseline_words = Counter()
baseline_onset = Counter()
for fn, sec, dial, wds in a_lines:
    for w in wds:
        baseline_words[w] += 1
        baseline_onset[get_onset(w)] += 1
total_a_tokens = sum(baseline_words.values())
print(f"A-dialect total word tokens: {total_a_tokens}")

# --- H321: What precedes dam@LL and dy@LL? ---
print("\n=== H321: PRECURSORS OF dam@LL AND dy@LL (A-dialect) ===\n")

dam_lines = [(fn, sec, dial, wds) for fn, sec, dial, wds in a_lines if len(wds) >= 2 and wds[-1] == 'dam']
dy_lines = [(fn, sec, dial, wds) for fn, sec, dial, wds in a_lines if len(wds) >= 2 and wds[-1] == 'dy']
print(f"A-dialect lines ending in dam@LL: {len(dam_lines)}")
print(f"A-dialect lines ending in dy@LL: {len(dy_lines)}")

def analyze_penultimate(target_lines, label):
    print(f"\n--- {label} (n={len(target_lines)}) ---")
    pen_words = Counter()
    pen_onsets = Counter()
    for fn, sec, dial, wds in target_lines:
        pen = wds[-2]
        pen_words[pen] += 1
        pen_onsets[get_onset(pen)] += 1
    total_pen = sum(pen_words.values())
    if total_pen == 0:
        print("  (no data)")
        return

    print(f"Top penultimate words (n={total_pen}):")
    print(f"  {'Word':<15} {'n':>4} {'rate':>7} {'word_baseline':>14} {'word_enrich':>12}")
    for w, cnt in pen_words.most_common(15):
        rate = cnt / total_pen
        wb = baseline_words.get(w, 0) / total_a_tokens
        enrich = rate / wb if wb > 0 else float('inf')
        print(f"  {w:<15} {cnt:>4} {rate:>7.3f} {wb:>14.4f} {enrich:>12.2f}×")

    print(f"\nPenultimate onset class distribution (n={total_pen}):")
    print(f"  {'Onset':<10} {'n':>4} {'rate':>7} {'baseline':>10} {'enrich':>8}")
    for onset in ONSET_ORDER + ['other']:
        cnt = pen_onsets.get(onset, 0)
        if cnt == 0: continue
        rate = cnt / total_pen
        bl = baseline_onset.get(onset, 0) / total_a_tokens
        enrich = rate / bl if bl > 0 else float('inf')
        print(f"  {onset:<10} {cnt:>4} {rate:>7.3f} {bl:>10.4f} {enrich:>8.2f}×")

    print(f"\nFull lines ({label}):")
    for fn, sec, dial, wds in target_lines:
        print(f"  f{fn} [{sec}/{dial}]: {' '.join(wds)}")

analyze_penultimate(dam_lines, "dam@LL penultimate")
analyze_penultimate(dy_lines, "dy@LL penultimate")

# Are cth-words in penultimate position before dam/dy?
for tgt_lines, label in [(dam_lines, 'dam'), (dy_lines, 'dy')]:
    cth_pen = [(fn, sec, dial, wds) for fn, sec, dial, wds in tgt_lines if get_onset(wds[-2]) == 'cth']
    print(f"\n[cth-word][{label}@LL]: {len(cth_pen)} cases:")
    for fn, sec, dial, wds in cth_pen:
        print(f"  f{fn}: {' '.join(wds)}")

# Are ot-words in penultimate position before dam/dy?
for tgt_lines, label in [(dam_lines, 'dam'), (dy_lines, 'dy')]:
    ot_pen = [(fn, sec, dial, wds) for fn, sec, dial, wds in tgt_lines if get_onset(wds[-2]) == 'ot']
    print(f"\n[ot-word][{label}@LL]: {len(ot_pen)} cases:")
    for fn, sec, dial, wds in ot_pen:
        print(f"  f{fn}: {' '.join(wds)}")

# --- H323: [ychor cthy...] full context ---
print("\n\n=== H323: [ychor][cthy@second] FULL CONTEXT ===\n")

all_ychor_lines = [(fn, sec, dial, wds) for fn, sec, dial, wds in lines_data if wds and wds[0] == 'ychor']
print(f"Total ychor@LF lines: {len(all_ychor_lines)}")

ychor_cthy_lines = [(fn, sec, dial, wds) for fn, sec, dial, wds in all_ychor_lines
                     if len(wds) >= 2 and wds[1] == 'cthy']
print(f"[ychor cthy@second] lines: {len(ychor_cthy_lines)}")
for fn, sec, dial, wds in ychor_cthy_lines:
    print(f"  f{fn} [{sec}/{dial}]: {' '.join(wds)}")

print(f"\nAll ychor@LF lines with full context:")
for fn, sec, dial, wds in all_ychor_lines:
    marker = " <-- HAS cthy@second" if len(wds) >= 2 and wds[1] == 'cthy' else ""
    print(f"  f{fn} [{sec}/{dial}]: {' '.join(wds)}{marker}")

# Third-word distribution in [ychor cthy ...] lines
if ychor_cthy_lines:
    print(f"\nThird word in [ychor cthy X ...] lines:")
    for fn, sec, dial, wds in ychor_cthy_lines:
        third = wds[2] if len(wds) > 2 else '(end)'
        print(f"  f{fn}: third={third}, line={' '.join(wds)}")

# Second-word onset distribution for all ychor lines
print(f"\nSecond-word distribution for all ychor lines:")
second_words = Counter()
second_onsets = Counter()
for fn, sec, dial, wds in all_ychor_lines:
    if len(wds) >= 2:
        second_words[wds[1]] += 1
        second_onsets[get_onset(wds[1])] += 1
for w, cnt in second_words.most_common(15):
    print(f"  {w}: {cnt}")

# ychor→ot anywhere in line
print(f"\nLines with ychor where any ot-word appears in line:")
for fn, sec, dial, wds in all_ychor_lines:
    ot_positions = [i for i, w in enumerate(wds) if get_onset(w) == 'ot']
    if ot_positions:
        print(f"  f{fn}: {' '.join(wds)} [ot at positions {ot_positions}]")

# --- H324 bonus: d@LF → cth@second decomposition ---
print("\n\n=== H324 BONUS: d@LF → cth@second DECOMPOSITION ===\n")

d_lf_lines = [(fn, sec, dial, wds) for fn, sec, dial, wds in a_lines if wds and get_onset(wds[0]) == 'd']
print(f"A-dialect d@LF lines: {len(d_lf_lines)}")

d_lf_cth_second = [(fn, sec, dial, wds) for fn, sec, dial, wds in d_lf_lines
                    if len(wds) >= 2 and get_onset(wds[1]) == 'cth']
print(f"d@LF → cth@second: {len(d_lf_cth_second)} cases")

# Decompose by specific d LF word
lf_word_counts = Counter()
lf_word_cth_counts = Counter()
for fn, sec, dial, wds in d_lf_lines:
    lf_word_counts[wds[0]] += 1
for fn, sec, dial, wds in d_lf_cth_second:
    lf_word_cth_counts[wds[0]] += 1

print(f"\nd@LF word decomposition:")
print(f"  {'LF-word':<12} {'all_d_LF':>10} {'cth@second':>12} {'rate':>8} {'baseline_rate':>14} {'enrich':>8}")
total_d_lf = sum(lf_word_counts.values())
baseline_second_cth_rate = sum(1 for fn, sec, dial, wds in a_lines if len(wds) >= 2 and get_onset(wds[1]) == 'cth') / len(a_lines)
print(f"  (baseline cth@second rate: {baseline_second_cth_rate:.4f})")
for w, cnt in lf_word_counts.most_common(20):
    cth_cnt = lf_word_cth_counts.get(w, 0)
    rate = cth_cnt / cnt if cnt > 0 else 0
    enrich = rate / baseline_second_cth_rate if baseline_second_cth_rate > 0 else float('inf')
    if cth_cnt > 0 or cnt >= 5:
        print(f"  {w:<12} {cnt:>10} {cth_cnt:>12} {rate:>8.3f} {baseline_second_cth_rate:>14.4f} {enrich:>8.2f}×")

print(f"\nFull lines d@LF → cth@second:")
for fn, sec, dial, wds in d_lf_cth_second:
    print(f"  f{fn} [{sec}]: {' '.join(wds)}")
