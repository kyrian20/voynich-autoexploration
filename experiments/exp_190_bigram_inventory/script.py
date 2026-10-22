"""
exp_190: Bigram Inventory — H324/H325/H326/H327/H329/H330/H331/H332

H324: Decompose d@LF→cth@second: how much is driven by daiin@LF vs other d-LF words?
H325: Are [cthor→ot-word] bigrams concentrated in specific herbal folios or spread?
H326: Ordering constraint — is [oty@LL][cth-word] ever observed? (should be 0)
H327: Is [ot-word][ot-word] bigram enriched in A? (sparked by otor/oteol in ychor line)
H329: Are [daiin ... dam@LL] lines short? Is [daiin][dam] an immediate bigram?
H330: qot→qot=2.22×, qot→l=2.84× — which qot-words self-chain or precede l-onset?
H331: ok→ok=1.96× (54 cases) — which ok-words chain?
H332: l→l=10.21× (n=3) — what are the three l→l cases in A-dialect?
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

# ---- H324: d@LF → cth@second — which d-LF words drive it? ----
print("\n" + "="*60)
print("H324: d@LF → cth@second — decompose by specific d-LF word")
print("="*60)

d_lf_cth_second = []
d_lf_total = []
for fn, ln, wds in a_lines:
    if len(wds) < 2: continue
    if get_onset(wds[0]) == 'd':
        d_lf_total.append((wds[0], wds[1] if len(wds)>1 else None, fn))
        if get_onset(wds[1]) == 'cth' if len(wds)>1 else False:
            d_lf_cth_second.append((wds[0], wds[1], fn))

print(f"\nTotal d@LF lines: {len(d_lf_total)}")
print(f"d@LF → cth@second: {len(d_lf_cth_second)} ({100*len(d_lf_cth_second)/len(d_lf_total):.1f}%)")

d_lf_word_counts = Counter(w for w,s,fn in d_lf_total)
d_lf_cth_by_word = Counter(w for w,s,fn in d_lf_cth_second)
print(f"\nSpecific d-LF words and their cth@second rate:")
for word, total in d_lf_word_counts.most_common(10):
    cth_count = d_lf_cth_by_word[word]
    rate = cth_count / total
    base_cth = A_onset['cth'] / A_total
    enrich = rate / base_cth if base_cth else 0
    print(f"  {word}: {cth_count}/{total} = {rate:.3f} (base={base_cth:.3f}, {enrich:.2f}×)")

print(f"\nFull [d-LF-word][cth@second] cases:")
for w0, w1, fn in d_lf_cth_second:
    print(f"  f{fn}: [{w0}][{w1}]")

# ---- H325: cthor→ot bigrams — folio distribution ----
print("\n" + "="*60)
print("H325: cthor→ot bigrams — folio distribution")
print("="*60)

cthor_ot_cases = []
cthor_total = []
for fn, ln, wds in a_lines:
    for i in range(len(wds)-1):
        if wds[i] == 'cthor':
            cthor_total.append((fn, wds[i], wds[i+1]))
            if get_onset(wds[i+1]) == 'ot':
                cthor_ot_cases.append((fn, wds[i], wds[i+1]))

cthor_total_b = []
cthor_ot_b = []
for fn, ln, wds in b_lines:
    for i in range(len(wds)-1):
        if wds[i] == 'cthor':
            cthor_total_b.append((fn, wds[i], wds[i+1]))
            if get_onset(wds[i+1]) == 'ot':
                cthor_ot_b.append((fn, wds[i], wds[i+1]))

print(f"\nA-dialect cthor→ot cases: {len(cthor_ot_cases)}/{len(cthor_total)} cthor bigrams")
print(f"Folios: {Counter(fn for fn,a,b in cthor_ot_cases).most_common()}")
print("Specific pairs:")
for fn, a, b in cthor_ot_cases:
    print(f"  f{fn}: [{a}][{b}]")
print(f"\nB-dialect cthor→ot cases: {len(cthor_ot_b)}/{len(cthor_total_b)}")

# ---- H326: Does [oty@LL][cth-word] ever occur? ----
print("\n" + "="*60)
print("H326: [oty@LL][cth-word@start-of-next-line] — is this 0?")
print("="*60)

# oty@LL followed by cth-word on next line (across line boundaries)
oty_ll_to_cth = []
for fn, ln, wds in a_lines:
    if wds and wds[-1] == 'oty':  # oty-final lines
        # Find the next line from same folio
        pass  # Need line-adjacent lookup

# Also check within-line: oty immediately followed by cth-word
oty_bigrams_within = []
for fn, ln, wds in a_lines + b_lines:
    for i in range(len(wds)-1):
        if wds[i] == 'oty':
            oty_bigrams_within.append((fn, wds[i], wds[i+1], get_onset(wds[i+1])))

print(f"\nA+B: all oty→[word] bigrams within lines (n={len(oty_bigrams_within)})")
onset_after_oty = Counter(o for fn,a,b,o in oty_bigrams_within)
total_oty_bigrams = len(oty_bigrams_within)
print(f"onset distribution after oty:")
for onset, cnt in onset_after_oty.most_common():
    base = A_onset[onset]/A_total
    rate = cnt/total_oty_bigrams
    print(f"  {onset}: {cnt} ({rate:.3f}, base={base:.3f}, {rate/base:.2f}×)")

cth_after_oty = [(fn,a,b,o) for fn,a,b,o in oty_bigrams_within if o == 'cth']
print(f"\n[oty][cth-word] within-line cases: {len(cth_after_oty)}")
for case in cth_after_oty:
    print(f"  f{case[0]}: [{case[1]}][{case[2]}]")

# ---- H327: [ot-word][ot-word] bigram enriched? ----
print("\n" + "="*60)
print("H327: [ot-word][ot-word] bigram enrichment in A-dialect")
print("="*60)

ot_ot_bigrams = []
for fn, ln, wds in a_lines:
    for i in range(len(wds)-1):
        if get_onset(wds[i]) == 'ot' and get_onset(wds[i+1]) == 'ot':
            ot_ot_bigrams.append((fn, ln, wds[i], wds[i+1]))

total_ot_bigrams = sum(1 for fn, ln, wds in a_lines for i in range(len(wds)-1) if get_onset(wds[i]) == 'ot')
base_ot_rate = A_onset['ot'] / A_total
total_bigrams_a = sum(len(wds)-1 for fn,ln,wds in a_lines)
expected_ot_ot = total_bigrams_a * base_ot_rate * base_ot_rate

print(f"\nA-dialect ot→ot bigrams: {len(ot_ot_bigrams)}")
print(f"Expected under independence: {expected_ot_ot:.1f} ({base_ot_rate:.4f}^2 × {total_bigrams_a})")
if expected_ot_ot > 0:
    print(f"Enrichment: {len(ot_ot_bigrams)/expected_ot_ot:.2f}×")

print(f"\nSpecific [ot-word][ot-word] pairs (top 10):")
pair_counts = Counter((a,b) for fn,ln,a,b in ot_ot_bigrams)
for pair, cnt in pair_counts.most_common(10):
    print(f"  {pair} × {cnt}")

# The specific f17 case: otor oteol
print(f"\nContains [otor][oteol]: {sum(1 for fn,ln,a,b in ot_ot_bigrams if a=='otor' and b=='oteol')}")
print(f"All otor→ot cases: {[(b,fn) for fn,ln,a,b in ot_ot_bigrams if a=='otor']}")

# ---- H329: [daiin][dam@LL] — are these immediate bigrams? Are lines short? ----
print("\n" + "="*60)
print("H329: [daiin ... dam@LL] — distance and line length")
print("="*60)

dam_lines = [(fn, ln, wds) for fn, ln, wds in a_lines if wds and wds[-1] == 'dam']
print(f"\nAll dam@LL lines: {len(dam_lines)}")
print(f"Lengths: {sorted(len(wds) for fn,ln,wds in dam_lines)}")
print(f"Mean length: {sum(len(wds) for fn,ln,wds in dam_lines)/len(dam_lines):.1f}")
print(f"A-dialect mean line length: {A_total/len(a_lines):.1f}")

daiin_dam_lines = []
for fn, ln, wds in dam_lines:
    if 'daiin' in wds:
        daiin_pos = [i for i, w in enumerate(wds) if w == 'daiin']
        dam_pos = len(wds) - 1
        for dp in daiin_pos:
            dist = dam_pos - dp
            daiin_dam_lines.append((fn, ln, wds, dp, dist))

print(f"\nLines with both daiin and dam@LL: {len(set(fn for fn,ln,wds,dp,dist in daiin_dam_lines))}")
print(f"[daiin][dam] immediate bigram (distance=1): {sum(1 for fn,ln,wds,dp,d in daiin_dam_lines if d==1)}")
print(f"[daiin][X][dam] (distance=2): {sum(1 for fn,ln,wds,dp,d in daiin_dam_lines if d==2)}")
print(f"[daiin ... dam] (distance≥3): {sum(1 for fn,ln,wds,dp,d in daiin_dam_lines if d>=3)}")
print(f"\nSpecific cases:")
for fn, ln, wds, dp, dist in daiin_dam_lines:
    print(f"  f{fn}.{ln} (len={len(wds)}, dist={dist}): {' '.join(wds)}")

# ---- H330: qot→qot and qot→l ----
print("\n" + "="*60)
print("H330: qot→qot (2.22×) and qot→l (2.84×) — specific words")
print("="*60)

qot_bigrams_a = []
for fn, ln, wds in a_lines:
    for i in range(len(wds)-1):
        if get_onset(wds[i]) == 'qot':
            qot_bigrams_a.append((wds[i], wds[i+1], get_onset(wds[i+1])))

qot_qot = [(a,b) for a,b,o in qot_bigrams_a if o=='qot']
qot_l = [(a,b) for a,b,o in qot_bigrams_a if o=='l']
print(f"\nA-dialect qot→qot: {len(qot_qot)} cases: {Counter(qot_qot).most_common(8)}")
print(f"A-dialect qot→l: {len(qot_l)} cases: {Counter(qot_l).most_common(8)}")

# ---- H331: ok→ok (54 cases) ----
print("\n" + "="*60)
print("H331: ok→ok (54 cases) — which ok-words chain?")
print("="*60)

ok_ok_a = []
for fn, ln, wds in a_lines:
    for i in range(len(wds)-1):
        if get_onset(wds[i]) == 'ok' and get_onset(wds[i+1]) == 'ok':
            ok_ok_a.append((wds[i], wds[i+1]))

print(f"\nA-dialect ok→ok bigrams: {len(ok_ok_a)}")
print(f"Top pairs: {Counter(ok_ok_a).most_common(10)}")
print(f"ok-word self-chaining (same word): {sum(1 for a,b in ok_ok_a if a==b)}")
all_ok_a = [w for fn,ln,wds in a_lines for w in wds if get_onset(w)=='ok']
print(f"Top individual ok words: {Counter(all_ok_a).most_common(8)}")

# ---- H332: l→l (n=3) ----
print("\n" + "="*60)
print("H332: l→l bigrams in A-dialect (extremely rare)")
print("="*60)

l_l_a = []
for fn, ln, wds in a_lines:
    for i in range(len(wds)-1):
        if get_onset(wds[i]) == 'l' and get_onset(wds[i+1]) == 'l':
            l_l_a.append((fn, ln, wds[i], wds[i+1]))

print(f"\nA-dialect l→l bigrams: {len(l_l_a)}")
for fn, ln, a, b in l_l_a:
    print(f"  f{fn}.{ln}: [{a}][{b}]")

all_l_a = [w for fn,ln,wds in a_lines for w in wds if get_onset(w)=='l']
print(f"Total l-words in A: {len(all_l_a)}")
base_l = len(all_l_a)/A_total
total_bg_a = sum(len(wds)-1 for fn,ln,wds in a_lines)
expected_l_l = total_bg_a * base_l * base_l
print(f"Expected l→l under independence: {expected_l_l:.2f}")
print(f"Enrichment: {len(l_l_a)/expected_l_l:.2f}×")
