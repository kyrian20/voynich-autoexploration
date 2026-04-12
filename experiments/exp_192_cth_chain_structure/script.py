"""
exp_192: cth Chain Structure — H339/H340/H341/H342/H343/H344/H345/H346/H347/H348/H349/H350

H339: qok depletes before cth (0.51×) in A — is this qok rarity in A or systematic avoidance?
H340: cth self-succession (1.62×, n=23) — which [cth1][cth2] pairs dominate?
H341: f46 B-herbal has anomalous cth concentration — is it a transition folio?
H342: B-cthedy positional profile vs other B-edy words (chedy, shedy)
H343: qok→l=2.44× in A — which qok-words? which folios?
H344: Is [cthol][cthy] part of a [daiin][cthol][cthy] 3-word chain?
H345: B-cthedy/cthey LF-enriched — what are their line-opening second-word formulas?
H346: [d][cth][d]=16 trigrams — are all literally [daiin][cth-word][daiin]?
H347: B-cthdy LL-enriched (2.41×) — are all 7 cases at LL position?
H348: [ch][daiin][cth]=12/17 — which ch-words? is [ch][daiin] a compound unit?
H349: cthol in [d][cth][d] — asymmetric d-word preferences (daiin left, varied right)?
H350: cthey@LF → ch_e second word (2/2 cases) — is this genuine or noise?
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

def is_ch_e(word):
    w = word.lower()
    return w.startswith('che') or w.startswith('chi')

def parse_locus(locus_raw):
    locus_parts = locus_raw.split(',')
    if len(locus_parts) < 2: return None, None, None
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
A_onset = Counter(get_onset(w) for w in A_words)
B_onset = Counter(get_onset(w) for w in B_words)
A_total, B_total = len(A_words), len(B_words)

print(f"A: {len(a_lines)} lines ({A_total} words) | B: {len(b_lines)} lines ({B_total} words)")

# ---- H339: qok→cth depletion in A ----
print("\n" + "="*60)
print("H339: qok→cth=0.51× — qok rarity in A or systematic avoidance?")
print("="*60)

qok_bigrams_a = []
qok_total_a = 0
for fn, ln, wds in a_lines:
    for i in range(len(wds)-1):
        if get_onset(wds[i]) == 'qok':
            qok_total_a += 1
            qok_bigrams_a.append((wds[i], wds[i+1], get_onset(wds[i+1]), fn))

qok_cth_a = [(a,b,fn) for a,b,o,fn in qok_bigrams_a if o == 'cth']
base_cth = A_onset['cth'] / A_total
expected_qok_cth = qok_total_a * base_cth
print(f"\nA-dialect qok total: {sum(1 for w in A_words if get_onset(w)=='qok')} words")
print(f"A-dialect qok bigrams (qok at position i): {qok_total_a}")
print(f"A-dialect qok→cth: {len(qok_cth_a)} observed vs {expected_qok_cth:.1f} expected")
print(f"Enrichment: {len(qok_cth_a)/expected_qok_cth:.2f}× (base cth={base_cth:.4f})")
print(f"\nqok→[all onsets] in A:")
for onset, cnt in Counter(o for a,b,o,fn in qok_bigrams_a).most_common():
    base = A_onset[onset] / A_total
    rate = cnt / qok_total_a if qok_total_a else 0
    print(f"  {onset}: {cnt} ({rate:.3f}, base={base:.3f}, {rate/base:.2f}×)")

# B-dialect qok→cth for comparison
qok_b_total = 0
qok_cth_b = 0
for fn, ln, wds in b_lines:
    for i in range(len(wds)-1):
        if get_onset(wds[i]) == 'qok':
            qok_b_total += 1
            if get_onset(wds[i+1]) == 'cth':
                qok_cth_b += 1
b_base_cth = B_onset['cth'] / B_total if B_total else 0
print(f"\nB-dialect qok→cth: {qok_cth_b}/{qok_b_total} (base cth={b_base_cth:.4f}, enrichment={qok_cth_b/(qok_b_total*b_base_cth) if qok_b_total*b_base_cth else 0:.2f}×)")

# ---- H340: cth self-succession pairs ----
print("\n" + "="*60)
print("H340: cth self-succession (1.62×, n=23) — which [cth1][cth2] pairs?")
print("="*60)

cth_cth_a = []
for fn, ln, wds in a_lines:
    for i in range(len(wds)-1):
        if get_onset(wds[i]) == 'cth' and get_onset(wds[i+1]) == 'cth':
            cth_cth_a.append((fn, ln, wds[i], wds[i+1], i, len(wds)))

print(f"\nA-dialect [cth][cth] bigrams: {len(cth_cth_a)}")
pair_counts = Counter((a,b) for fn,ln,a,b,i,n in cth_cth_a)
print(f"Specific pairs: {pair_counts.most_common()}")
print(f"\nFull list:")
for fn, ln, a, b, i, n in cth_cth_a:
    pos_a = 'LF' if i == 0 else ('LL' if i == n-2 else 'MID')
    pos_b = 'LF' if i+1 == 0 else ('LL' if i+1 == n-1 else 'MID')
    print(f"  f{fn}.{ln}: [{a}@{pos_a}][{b}@{pos_b}]  (line_len={n})")

# Most common cth1 words in succession
cth1_words = Counter(a for fn,ln,a,b,i,n in cth_cth_a)
cth2_words = Counter(b for fn,ln,a,b,i,n in cth_cth_a)
print(f"\ncth1 words: {cth1_words.most_common()}")
print(f"cth2 words: {cth2_words.most_common()}")

# ---- H341: f46 anomalous cth ----
print("\n" + "="*60)
print("H341: f46 anomalous cth concentration — transition folio?")
print("="*60)

for folio in [44, 45, 46, 47, 48]:
    fn_words = folio_words[folio]
    if not fn_words:
        print(f"  f{folio}: no words")
        continue
    dialect = folio_dialect.get(folio, 'unknown')
    edy_count = sum(1 for w in fn_words if 'edy' in w or 'eedy' in w)
    edy_rate = edy_count / len(fn_words)
    cth_words_in_folio = [w for w in fn_words if w.startswith('cth')]
    cth_rate = len(cth_words_in_folio) / len(fn_words)
    print(f"  f{folio} ({dialect}): {len(fn_words)} words, edy_rate={edy_rate:.3f}, cth_rate={cth_rate:.4f} (n={len(cth_words_in_folio)})")
    if cth_words_in_folio:
        print(f"    cth words: {Counter(cth_words_in_folio).most_common()}")

print(f"\nOverall B-dialect cth rate: {B_onset['cth']/B_total:.4f}")
print(f"Overall A-dialect cth rate: {A_onset['cth']/A_total:.4f}")

# ---- H342: B cthedy positional profile vs chedy, shedy ----
print("\n" + "="*60)
print("H342: B-cthedy positional profile vs chedy, shedy, qokedy")
print("="*60)

target_words = ['cthedy', 'cthey', 'cthdy', 'chedy', 'shedy', 'qokedy']
for word in target_words:
    positions = []
    for fn, ln, wds in b_lines:
        for i, w in enumerate(wds):
            if w == word:
                pos = 'LF' if i == 0 else ('LL' if i == len(wds)-1 else 'second' if i == 1 else 'MID')
                positions.append(pos)
    if not positions:
        print(f"  {word}: not found in B")
        continue
    n = len(positions)
    pos_count = Counter(positions)
    lf = pos_count['LF'] / n
    ll = pos_count['LL'] / n
    mid = pos_count['MID'] / n
    base_lf = len(a_lines) / A_total  # approximation
    print(f"  {word}: n={n} | LF={pos_count['LF']}({lf:.3f}) | second={pos_count.get('second',0)} | MID={pos_count['MID']}({mid:.3f}) | LL={pos_count['LL']}({ll:.3f})")

# B baseline positional rates
b_all_positions = []
for fn, ln, wds in b_lines:
    for i, w in enumerate(wds):
        pos = 'LF' if i == 0 else ('LL' if i == len(wds)-1 else 'MID')
        b_all_positions.append(pos)
b_pos_base = Counter(b_all_positions)
b_pos_total = sum(b_pos_base.values())
print(f"\nB baseline: LF={b_pos_base['LF']/b_pos_total:.3f}, MID={b_pos_base['MID']/b_pos_total:.3f}, LL={b_pos_base['LL']/b_pos_total:.3f}")

# ---- H343: qok→l in A ----
print("\n" + "="*60)
print("H343: qok→l=2.44× in A — which qok-words? which folios?")
print("="*60)

qok_l_a = []
for fn, ln, wds in a_lines:
    for i in range(len(wds)-1):
        if get_onset(wds[i]) == 'qok' and get_onset(wds[i+1]) == 'l':
            qok_l_a.append((fn, ln, wds[i], wds[i+1]))

print(f"\nA-dialect qok→l bigrams (n={len(qok_l_a)}):")
for fn, ln, a, b in qok_l_a:
    print(f"  f{fn}.{ln}: [{a}][{b}]")
qok_l_pairs = Counter((a,b) for fn,ln,a,b in qok_l_a)
print(f"\nqok-words in qok→l: {Counter(a for fn,ln,a,b in qok_l_a).most_common()}")
print(f"l-words after qok: {Counter(b for fn,ln,a,b in qok_l_a).most_common()}")
print(f"Folio distribution: {Counter(fn for fn,ln,a,b in qok_l_a).most_common()}")

# Enrichment confirmation
base_l = A_onset['l'] / A_total
qok_total_all = sum(1 for w in A_words if get_onset(w)=='qok')
n_qok_bigrams_all = sum(1 for fn,ln,wds in a_lines for i in range(len(wds)-1) if get_onset(wds[i])=='qok')
print(f"\nqok→l enrichment: {len(qok_l_a)}/{n_qok_bigrams_all} = {len(qok_l_a)/n_qok_bigrams_all:.4f} vs base l={base_l:.4f} → {(len(qok_l_a)/n_qok_bigrams_all)/base_l:.2f}×")

# ---- H344: [daiin][cthol][cthy] 3-word chain ----
print("\n" + "="*60)
print("H344: [daiin][cthol][cthy] 3-word chain — how many cases?")
print("="*60)

daiin_cthol_cthy = []
daiin_cthol = []
cthol_cthy = []
for fn, ln, wds in a_lines:
    for i in range(len(wds)-1):
        if wds[i] == 'daiin' and wds[i+1] == 'cthol':
            daiin_cthol.append((fn, ln, i, wds))
            if i+2 < len(wds) and wds[i+2] == 'cthy':
                daiin_cthol_cthy.append((fn, ln, i, wds))
        if wds[i] == 'cthol' and wds[i+1] == 'cthy':
            cthol_cthy.append((fn, ln, i, wds))

print(f"\n[daiin][cthol] bigrams: {len(daiin_cthol)}")
print(f"[cthol][cthy] bigrams: {len(cthol_cthy)}")
print(f"[daiin][cthol][cthy] trigrams: {len(daiin_cthol_cthy)}")
for fn, ln, i, wds in daiin_cthol_cthy:
    print(f"  f{fn}.{ln}: {' '.join(wds)}")
for fn, ln, i, wds in cthol_cthy:
    print(f"  [cthol][cthy]: f{fn}.{ln}: ...{' '.join(wds[max(0,i-1):i+3])}...")

# All [daiin][cthol] cases and what follows cthol
print(f"\n[daiin][cthol] + what follows:")
for fn, ln, i, wds in daiin_cthol:
    next_w = wds[i+2] if i+2 < len(wds) else '(end)'
    print(f"  f{fn}.{ln}: daiin cthol {next_w}")

# ---- H345: B-cthedy/cthey LF-enriched — second words ----
print("\n" + "="*60)
print("H345: B-cthedy/cthey LF lines — what second words?")
print("="*60)

for target in ['cthedy', 'cthey']:
    lf_lines = [(fn, ln, wds) for fn, ln, wds in b_lines if wds and wds[0] == target]
    print(f"\n{target}@LF lines (n={len(lf_lines)}):")
    for fn, ln, wds in lf_lines:
        second = wds[1] if len(wds) > 1 else '(end)'
        print(f"  f{fn}.{ln}: {' '.join(wds[:4])}...")

# Also non-LF positions of cthedy/cthey to check successor diversity
for target in ['cthedy', 'cthey']:
    non_lf = [(fn, ln, i, wds) for fn, ln, wds in b_lines
              for i, w in enumerate(wds) if w == target and i > 0]
    successors_non_lf = Counter(wds[i+1] if i+1 < len(wds) else '(end)' for fn,ln,i,wds in non_lf)
    print(f"\n{target}@non-LF successor words: {successors_non_lf.most_common(5)}")

# ---- H346: [d][cth][d] = 16 trigrams — are they [daiin][cth][daiin]? ----
print("\n" + "="*60)
print("H346: [d][cth][d]=16 onset-trigrams — specific d-words flanking cth")
print("="*60)

d_cth_d = []
for fn, ln, wds in a_lines:
    for i in range(len(wds)-2):
        if get_onset(wds[i]) == 'd' and get_onset(wds[i+1]) == 'cth' and get_onset(wds[i+2]) == 'd':
            d_cth_d.append((fn, ln, wds[i], wds[i+1], wds[i+2]))

print(f"\nA-dialect [d][cth][d] trigrams: {len(d_cth_d)}")
daiin_cth_daiin = sum(1 for fn,ln,a,b,c in d_cth_d if a=='daiin' and c=='daiin')
daiin_left = sum(1 for fn,ln,a,b,c in d_cth_d if a=='daiin')
daiin_right = sum(1 for fn,ln,a,b,c in d_cth_d if c=='daiin')
print(f"[daiin][cth][daiin]: {daiin_cth_daiin}/{len(d_cth_d)} = {daiin_cth_daiin/len(d_cth_d):.1%}")
print(f"[daiin][cth][?]: {daiin_left}/{len(d_cth_d)} (daiin left)")
print(f"[?][cth][daiin]: {daiin_right}/{len(d_cth_d)} (daiin right)")
print(f"\nLeft d-words: {Counter(a for fn,ln,a,b,c in d_cth_d).most_common()}")
print(f"cth-words: {Counter(b for fn,ln,a,b,c in d_cth_d).most_common()}")
print(f"Right d-words: {Counter(c for fn,ln,a,b,c in d_cth_d).most_common()}")
print(f"\nFull list:")
for fn, ln, a, b, c in d_cth_d:
    print(f"  f{fn}.{ln}: [{a}][{b}][{c}]")

# ---- H347: B-cthdy LL position ----
print("\n" + "="*60)
print("H347: B-cthdy LL-enriched — are all 7 cases at LL position?")
print("="*60)

cthdy_positions = []
for fn, ln, wds in b_lines:
    for i, w in enumerate(wds):
        if w == 'cthdy':
            pos = 'LL' if i == len(wds)-1 else ('LF' if i == 0 else 'MID')
            cthdy_positions.append((fn, ln, i, len(wds), pos, wds))

print(f"\nB-dialect cthdy occurrences (n={len(cthdy_positions)}):")
for fn, ln, i, n, pos, wds in cthdy_positions:
    print(f"  f{fn}.{ln}: position={i}@{pos}, line_len={n}: ...{' '.join(wds[max(0,i-1):i+2])}...")
print(f"\ncthdy position summary: {Counter(pos for fn,ln,i,n,pos,wds in cthdy_positions)}")

# ---- H348: [ch][daiin][cth] specific pairs ----
print("\n" + "="*60)
print("H348: [ch][daiin][cth]=12/17 trigrams — which ch-words?")
print("="*60)

ch_daiin_cth = []
for fn, ln, wds in a_lines:
    for i in range(len(wds)-2):
        if get_onset(wds[i]) == 'ch' and wds[i+1] == 'daiin' and get_onset(wds[i+2]) == 'cth':
            ch_daiin_cth.append((fn, ln, wds[i], wds[i+1], wds[i+2]))

print(f"\n[ch][daiin][cth] trigrams (n={len(ch_daiin_cth)}):")
ch_words_in = Counter(a for fn,ln,a,b,c in ch_daiin_cth)
cth_words_out = Counter(c for fn,ln,a,b,c in ch_daiin_cth)
print(f"ch-words: {ch_words_in.most_common()}")
print(f"cth-words: {cth_words_out.most_common()}")
print(f"\nFull list:")
for fn, ln, a, b, c in ch_daiin_cth:
    print(f"  f{fn}.{ln}: [{a}][{b}][{c}]")

# Also: full [ch][d][cth] (any d-word)
ch_d_cth = [(fn, ln, wds[i], wds[i+1], wds[i+2])
            for fn, ln, wds in a_lines
            for i in range(len(wds)-2)
            if get_onset(wds[i]) == 'ch' and get_onset(wds[i+1]) == 'd' and get_onset(wds[i+2]) == 'cth']
print(f"\nAll [ch][d-word][cth] trigrams (any d-word): {len(ch_d_cth)}")
d_words_between = Counter(b for fn,ln,a,b,c in ch_d_cth)
print(f"d-words between ch and cth: {d_words_between.most_common()}")

# ---- H349: cthol d-word asymmetry ----
print("\n" + "="*60)
print("H349: cthol d-word asymmetry — daiin preferentially left, varied right?")
print("="*60)

# All [d][cthol] bigrams — daiin specifically
d_cthol = []
cthol_d = []
for fn, ln, wds in a_lines:
    for i in range(len(wds)-1):
        if get_onset(wds[i]) == 'd' and wds[i+1] == 'cthol':
            d_cthol.append((fn, ln, wds[i], 'cthol'))
        if wds[i] == 'cthol' and get_onset(wds[i+1]) == 'd':
            cthol_d.append((fn, ln, 'cthol', wds[i+1]))

print(f"\n[d][cthol] bigrams: {len(d_cthol)}")
d_left = Counter(a for fn,ln,a,b in d_cthol)
print(f"d-words LEFT of cthol: {d_left.most_common()}")
daiin_left_cthol = d_left['daiin']
print(f"  daiin LEFT: {daiin_left_cthol}/{len(d_cthol)} = {daiin_left_cthol/len(d_cthol):.1%} (vs daiin base rate in A: {sum(1 for w in A_words if w=='daiin')/A_total:.4f})")

print(f"\n[cthol][d] bigrams: {len(cthol_d)}")
d_right = Counter(b for fn,ln,a,b in cthol_d)
print(f"d-words RIGHT of cthol: {d_right.most_common()}")
daiin_right_cthol = d_right.get('daiin', 0)
print(f"  daiin RIGHT: {daiin_right_cthol}/{len(cthol_d)} = {daiin_right_cthol/len(cthol_d) if cthol_d else 0:.1%}")

# Compare daiin rate left vs right
if d_cthol and cthol_d:
    print(f"\nAsymmetry: daiin appears {daiin_left_cthol/len(d_cthol):.3f} left vs {daiin_right_cthol/len(cthol_d):.3f} right")

# ---- H350: cthey@LF → ch_e second word ----
print("\n" + "="*60)
print("H350: cthey@LF → ch_e second word — genuine or noise?")
print("="*60)

# B-dialect cthey@LF
cthey_lf_b = [(fn, ln, wds) for fn, ln, wds in b_lines if wds and wds[0] == 'cthey']
print(f"\nB-dialect cthey@LF (n={len(cthey_lf_b)}):")
for fn, ln, wds in cthey_lf_b:
    second = wds[1] if len(wds) > 1 else '(end)'
    is_che = is_ch_e(second) if len(wds) > 1 else False
    print(f"  f{fn}.{ln}: cthey → {second} {'[ch_e]' if is_che else ''}")

# All cthey successor distribution (any position)
cthey_successors_b = [(wds[i+1], get_onset(wds[i+1])) for fn,ln,wds in b_lines
                      for i in range(len(wds)-1) if wds[i] == 'cthey']
print(f"\ncthey → all successors in B (n={len(cthey_successors_b)}):")
succ_onset = Counter(o for w,o in cthey_successors_b)
for onset, cnt in succ_onset.most_common():
    base = B_onset.get(onset, 0) / B_total
    rate = cnt / len(cthey_successors_b)
    print(f"  {onset}: {cnt} ({rate:.3f}, base={base:.3f}, {rate/base:.2f}× if base>0)")

che_after_cthey = sum(1 for w,o in cthey_successors_b if is_ch_e(w))
print(f"\nch_e successors after cthey (any position): {che_after_cthey}/{len(cthey_successors_b)}")

# cthedy successor distribution for comparison
cthedy_successors_b = [(wds[i+1], get_onset(wds[i+1])) for fn,ln,wds in b_lines
                       for i in range(len(wds)-1) if wds[i] == 'cthedy']
print(f"\ncthedy → all successors in B (n={len(cthedy_successors_b)}):")
succ_onset_edy = Counter(o for w,o in cthedy_successors_b)
for onset, cnt in succ_onset_edy.most_common():
    base = B_onset.get(onset, 0) / B_total
    rate = cnt / len(cthedy_successors_b)
    print(f"  {onset}: {cnt} ({rate:.3f}, base={base:.3f}, {rate/base:.2f}× if base>0)")
