"""
exp_189: Line-Terminal Construction Analysis — H321 (dam@LL precursors), H323 ([ychor][cthy@second])

H321: What precedes dam@LL and dy@LL in A-dialect?
  F166: dam=3.98× LL-closer, dy=3.02× LL-closer in A.
  Extract all A-dialect lines ending in dam or dy. Tabulate penultimate word onset class.
  Expected: specific onset class enrichment (cth-words or ot-words as penultimate).

H323: The [ychor][cthy@second] construction
  F167: [ychor][cthy@second]=2 cases. cthy normally LL-enriched but appears at position-2 (second)
    after ychor — atypical position. What follows in these lines? Same folio cluster?
  Extract all ychor lines in A-dialect. Identify the 2 [ychor][cthy...] lines. Tabulate positions 3+.

Pre-registration:
  H321: penultimate onset before dam@LL: cth-words expected enriched (3-5× relative to baseline).
    Alternatively, d-onset or daiin-class might precede. Not known.
  H323: [ychor][cthy...] lines likely have a specific third-word onset or cluster in same folio range.
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
    return 'other'

def parse_locus(locus_raw):
    locus_parts = locus_raw.split(',')
    if len(locus_parts) < 2:
        return None, None, None
    folio_str = locus_parts[0]
    folio_base = folio_str.split('.')[0].lstrip('<')
    m = re.match(r'f(\d+)', folio_base)
    folio_num = int(m.group(1)) if m else None
    lt_raw = locus_parts[1].rstrip('>')
    lt = lt_raw.lstrip('@+*=~&')
    line_m = re.search(r'\.(\d+),', locus_raw)
    line_num = int(line_m.group(1)) if line_m else None
    return folio_num, lt, line_num

folio_words = defaultdict(list)
raw_lines = []
with open(CORPUS) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'): continue
        parts = line.split(None, 1)
        if len(parts) < 2: continue
        locus_raw, text = parts
        folio_num, lt, line_num = parse_locus(locus_raw)
        if folio_num is None: continue
        if not lt.startswith('P'): continue
        words = [w for w in text.split('.') if w and re.match(r'[a-z]', w) and not w.startswith('<')]
        if not words: continue
        folio_words[folio_num].extend(words)
        raw_lines.append((folio_num, line_num, words))

folio_dialect = {}
for fn, wds in folio_words.items():
    if len(wds) < 10: continue
    edy_count = sum(1 for w in wds if 'edy' in w or 'eedy' in w)
    folio_dialect[fn] = 'B' if edy_count/len(wds) >= 0.05 else 'A'

lines_data = [(fn, ln, folio_dialect.get(fn, 'unknown'), wds) for fn, ln, wds in raw_lines]
a_lines = [(fn, ln, wds) for fn, ln, dial, wds in lines_data if dial == 'A']
b_lines = [(fn, ln, wds) for fn, ln, dial, wds in lines_data if dial == 'B']
A_words = [w for fn, ln, wds in a_lines for w in wds]
B_words = [w for fn, ln, wds in b_lines for w in wds]

print(f"A-dialect: {len(a_lines)} lines, {len(A_words)} words")
print(f"B-dialect: {len(b_lines)} lines, {len(B_words)} words")

A_onset = Counter(get_onset(w) for w in A_words)
A_total = len(A_words)

# =====================================================================
# H321: What precedes dam@LL and dy@LL?
# =====================================================================
print()
print("="*60)
print("H321: Penultimate words before dam@LL and dy@LL (A-dialect)")
print("="*60)

dam_ll_lines = []
dy_ll_lines = []
am_ll_lines = []  # lines ending in -am suffix (general)

for fn, ln, wds in a_lines:
    if len(wds) < 2: continue
    last = wds[-1]
    penult = wds[-2]
    if last == 'dam':
        dam_ll_lines.append((fn, ln, wds, penult))
    elif last.endswith('dy') and len(last) <= 4:  # short dy-suffix words
        dy_ll_lines.append((fn, ln, wds, penult))
    if last.endswith('am'):
        am_ll_lines.append((fn, ln, wds, penult))

print(f"\nLines ending in 'dam' (exact): {len(dam_ll_lines)}")
print(f"Lines ending in short -dy words: {len(dy_ll_lines)}")
print(f"Lines ending in -am words (all): {len(am_ll_lines)}")

for target_name, target_lines in [('dam@LL', dam_ll_lines), ('dy@LL (short)', dy_ll_lines), ('*am@LL', am_ll_lines)]:
    if not target_lines: continue
    penult_onsets = Counter(get_onset(p) for fn,ln,wds,p in target_lines)
    penult_words = Counter(p for fn,ln,wds,p in target_lines)

    print(f"\n--- {target_name} (n={len(target_lines)}) ---")
    print(f"  Penultimate onset distribution (enrichment vs A-dialect baseline):")
    for onset in ['cth','ch','sh','d','ok','ot','qok','y','s','l','other']:
        base = A_onset[onset] / A_total
        count = penult_onsets[onset]
        rate = count / len(target_lines)
        enrich = rate / base if base > 0 else 0
        if count > 0:
            print(f"    {onset:6s}: {count:3d}/{len(target_lines)} = {rate:.3f} (base={base:.3f}, enrich={enrich:.2f}×)")

    print(f"  Top penultimate words: {dict(penult_words.most_common(8))}")

    # Show specific line examples
    print(f"  Example lines ending in {target_name.split('@')[0]}:")
    for fn, ln, wds, p in target_lines[:6]:
        print(f"    f{fn}.{ln}: {' '.join(wds[-5:])}")

# =====================================================================
# H323: [ychor][cthy@second] construction
# =====================================================================
print()
print("="*60)
print("H323: [ychor][cthy@second] construction — full context")
print("="*60)

ychor_lines_a = [(fn, ln, wds) for fn, ln, wds in a_lines if wds and wds[0] == 'ychor']
ychor_lines_b = [(fn, ln, wds) for fn, ln, wds in b_lines if wds and wds[0] == 'ychor']

for dialect_name, ychor_lines in [('A', ychor_lines_a), ('B', ychor_lines_b)]:
    print(f"\n--- {dialect_name}-dialect ychor-opening lines (n={len(ychor_lines)}) ---")
    if not ychor_lines:
        print("  (no ychor lines)")
        continue

    # Second word analysis
    second_words = [wds[1] if len(wds) > 1 else None for fn, ln, wds in ychor_lines]
    second_onsets = Counter(get_onset(w) for w in second_words if w)
    print(f"  Second word onset distribution:")
    onset_total = sum(second_onsets.values())
    for onset, cnt in second_onsets.most_common():
        base = A_onset[onset] / A_total if dialect_name == 'A' else Counter(get_onset(w) for w in B_words)[onset]/len(B_words)
        rate = cnt / onset_total
        enrich = rate / base if base else 0
        print(f"    {onset:6s}: {cnt} ({rate:.2f} vs base {base:.3f} = {enrich:.1f}×)")

    # Identify [ychor][cthy...] lines specifically
    ychor_cthy = [(fn, ln, wds) for fn, ln, wds in ychor_lines if len(wds) > 1 and wds[1].startswith('cth')]
    print(f"\n  [ychor][cth-word@second] lines (n={len(ychor_cthy)}):")
    for fn, ln, wds in ychor_cthy:
        print(f"    f{fn}.{ln}: {' '.join(wds)}")

    # Full context of all ychor lines
    print(f"\n  All {len(ychor_lines)} ychor-opening lines:")
    for fn, ln, wds in sorted(ychor_lines, key=lambda x: (x[0], x[1])):
        second = wds[1] if len(wds) > 1 else '--'
        third = wds[2] if len(wds) > 2 else '--'
        last = wds[-1] if wds else '--'
        marker = ' *** [ychor][cth]' if second.startswith('cth') else ''
        print(f"    f{fn}.{ln}: ychor {second} {third} ... {last}{marker}")

    # Folio clustering
    if ychor_cthy:
        print(f"\n  Folio numbers for [ychor][cth@second] cases: {[fn for fn, ln, wds in ychor_cthy]}")
        print(f"  Folio numbers for all ychor lines: {[fn for fn, ln, wds in ychor_lines]}")

# =====================================================================
# Supplement: All A-dialect lines ending in dam or dy — full listing
# =====================================================================
print()
print("="*60)
print("SUPPLEMENT: Full inventory of dam@LL lines (A-dialect)")
print("="*60)
print(f"All {len(dam_ll_lines)} dam-final lines:")
for fn, ln, wds, p in dam_ll_lines:
    print(f"  f{fn}.{ln}: {' '.join(wds)}")
