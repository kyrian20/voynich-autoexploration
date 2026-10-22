"""
exp_191: Bigram Specifics — H328/H333/H334/H335/H336/H337/H338 + [oty][l-onset] B-dialect

H328: What are the two [dchor@LF][cth@second] full lines? Is [dchor][cthor] reduplication?
H333: ch_e↔r bidirectional enrichment (2.55×, n=6 each) — what are the specific pairs?
H334: t→ot=1.85× (n=16) — which t-words precede ot-words?
H335: k→cth=1.60× (n=18) — which k-words precede cth-words?
H336: ch→r=2.34× (n=15) — which ch-words precede r-onset?
H337: B-dialect ch→cth=2.75× (n=8) — what are these 8 B ch→cth bigrams?
H338: Is B-dialect cthedy/cthdy genuine B-vocabulary or transcription artifacts?
+ [oty][l-onset]: 15.78× in B Stars/Bio — characterize the 6 cases and section distribution
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
    if w.startswith('p'): return 'p'
    if w.startswith('f'): return 'f'
    return 'other'

def is_ch_e(word):
    """Is this word a ch_e form (che-, chi- forms)?"""
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
locus_map = {}  # (folio_num, line_num) -> locus_raw for full context
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
        raw_lines.append((folio_num, line_num, words, locus_raw))

folio_dialect = {}
for fn, wds in folio_words.items():
    if len(wds) < 10: continue
    edy_count = sum(1 for w in wds if 'edy' in w or 'eedy' in w)
    folio_dialect[fn] = 'B' if edy_count/len(wds) >= 0.05 else 'A'

lines_data = [(fn, ln, folio_dialect.get(fn, 'unknown'), wds, locus) for fn, ln, wds, locus in raw_lines]
a_lines = [(fn, ln, wds, locus) for fn, ln, dial, wds, locus in lines_data if dial == 'A']
b_lines = [(fn, ln, wds, locus) for fn, ln, dial, wds, locus in lines_data if dial == 'B']

A_words = [w for fn, ln, wds, locus in a_lines for w in wds]
B_words = [w for fn, ln, wds, locus in b_lines for w in wds]
A_onset = Counter(get_onset(w) for w in A_words)
B_onset = Counter(get_onset(w) for w in B_words)
A_total, B_total = len(A_words), len(B_words)

print(f"A: {len(a_lines)} lines ({A_total} words) | B: {len(b_lines)} lines ({B_total} words)")

# ---- H328: [dchor@LF][cth@second] — the two full lines ----
print("\n" + "="*60)
print("H328: [dchor@LF][cth@second] full lines and [dchor][cthor] reduplication")
print("="*60)

dchor_lf_lines = []
for fn, ln, wds, locus in a_lines:
    if wds and wds[0] == 'dchor':
        dchor_lf_lines.append((fn, ln, wds, locus))

print(f"\nAll dchor@LF lines in A (n={len(dchor_lf_lines)}):")
dchor_cth_second = []
for fn, ln, wds, locus in dchor_lf_lines:
    second_word = wds[1] if len(wds) > 1 else None
    second_onset = get_onset(second_word) if second_word else None
    marker = "*** cth@second" if second_onset == 'cth' else ""
    print(f"  f{fn}.{ln}: {' '.join(wds)} {marker}")
    if second_onset == 'cth':
        dchor_cth_second.append((fn, ln, wds, second_word))

print(f"\n[dchor@LF][cth@second] cases: {len(dchor_cth_second)}")
print(f"cth words at second position:")
for fn, ln, wds, second in dchor_cth_second:
    print(f"  f{fn}.{ln}: dchor → {second} → {wds[2] if len(wds)>2 else '(end)'}")

# Is [dchor][cthor] specifically enriched?
dchor_cthor = sum(1 for fn,ln,wds,locus in a_lines
                  for i in range(len(wds)-1)
                  if wds[i] == 'dchor' and wds[i+1] == 'cthor')
dchor_any = sum(1 for fn,ln,wds,locus in a_lines
                for i in range(len(wds)-1)
                if wds[i] == 'dchor')
cthor_base_rate = sum(1 for w in A_words if w == 'cthor') / A_total
rate_str = f"{dchor_cthor/dchor_any:.3f}" if dchor_any else "N/A"
print(f"\n[dchor][cthor] within all A bigrams: {dchor_cthor}/{dchor_any} dchor bigrams = {rate_str}")
print(f"Base cthor rate in A: {cthor_base_rate:.4f}")
if dchor_any and cthor_base_rate > 0:
    print(f"Enrichment: {(dchor_cthor/dchor_any)/cthor_base_rate:.2f}×")

# Also check dchor@LF: is cthor specifically selected?
print(f"\ndchor@LF → all second-word onsets:")
dchor_lf_second = Counter(get_onset(wds[1]) if len(wds)>1 else 'END' for fn,ln,wds,locus in dchor_lf_lines)
for onset, cnt in dchor_lf_second.most_common():
    base = A_onset[onset]/A_total
    rate = cnt/len(dchor_lf_lines)
    print(f"  {onset}: {cnt} ({rate:.3f}, base={base:.3f}, {rate/base:.2f}× if base>0)")
print(f"\ndchor@LF → cthor specifically:")
dchor_lf_cthor = sum(1 for fn,ln,wds,locus in dchor_lf_lines if len(wds)>1 and wds[1]=='cthor')
print(f"  {dchor_lf_cthor}/{len(dchor_lf_lines)} = {dchor_lf_cthor/len(dchor_lf_lines):.3f}")

# ---- H333: ch_e↔r bidirectional enrichment ----
print("\n" + "="*60)
print("H333: ch_e↔r bidirectional enrichment — specific pairs")
print("="*60)

che_to_r = []
r_to_che = []
for fn, ln, wds, locus in a_lines:
    for i in range(len(wds)-1):
        if is_ch_e(wds[i]) and get_onset(wds[i+1]) == 'r':
            che_to_r.append((fn, ln, wds[i], wds[i+1]))
        if get_onset(wds[i]) == 'r' and is_ch_e(wds[i+1]):
            r_to_che.append((fn, ln, wds[i], wds[i+1]))

print(f"\nA-dialect [ch_e→r] pairs (n={len(che_to_r)}):")
for fn, ln, a, b in che_to_r:
    print(f"  f{fn}.{ln}: [{a}][{b}]")
print(f"\nA-dialect [r→ch_e] pairs (n={len(r_to_che)}):")
for fn, ln, a, b in r_to_che:
    print(f"  f{fn}.{ln}: [{a}][{b}]")

# Compute enrichment
all_che_words = [w for w in A_words if is_ch_e(w)]
n_che = len(all_che_words)
n_r = A_onset['r']
n_bigrams_a = sum(len(wds)-1 for fn,ln,wds,locus in a_lines)
base_r = n_r / A_total
base_che = n_che / A_total
print(f"\nBase rates: ch_e={base_che:.4f} ({n_che} words), r={base_r:.4f} ({n_r} words)")
print(f"Expected [ch_e→r] under independence: {n_bigrams_a * base_che * base_r:.2f}")
print(f"Expected [r→ch_e] under independence: {n_bigrams_a * base_r * base_che:.2f}")
print(f"Enrichment [ch_e→r]: {len(che_to_r) / (n_bigrams_a * base_che * base_r):.2f}×")
print(f"Enrichment [r→ch_e]: {len(r_to_che) / (n_bigrams_a * base_r * base_che):.2f}×")

# Most common ch_e words
print(f"\nTop ch_e words in A: {Counter(all_che_words).most_common(8)}")
# r words
r_words_a = [w for w in A_words if get_onset(w) == 'r']
print(f"Top r-onset words in A: {Counter(r_words_a).most_common(8)}")

# ---- H334: t→ot=1.85× (n=16) ----
print("\n" + "="*60)
print("H334: t→ot=1.85× (n=16) — which t-words precede ot-words?")
print("="*60)

t_ot_bigrams = []
for fn, ln, wds, locus in a_lines:
    for i in range(len(wds)-1):
        if get_onset(wds[i]) == 't' and get_onset(wds[i+1]) == 'ot':
            t_ot_bigrams.append((fn, ln, wds[i], wds[i+1]))

print(f"\nA-dialect t→ot bigrams (n={len(t_ot_bigrams)}):")
t_ot_pairs = Counter((a,b) for fn,ln,a,b in t_ot_bigrams)
print(f"Specific pairs: {t_ot_pairs.most_common()}")
print(f"\nFull list:")
for fn, ln, a, b in t_ot_bigrams:
    print(f"  f{fn}.{ln}: [{a}][{b}]")

# t-word breakdown
t_lf_in_t_ot = Counter(a for fn,ln,a,b in t_ot_bigrams)
all_t_words = Counter(w for w in A_words if get_onset(w)=='t')
print(f"\nt-words in t→ot (n unique t-words={len(t_lf_in_t_ot)}): {t_lf_in_t_ot.most_common()}")
print(f"All t-words in A: {all_t_words.most_common(8)}")

base_ot_rate = A_onset['ot'] / A_total
t_total_bigrams = sum(1 for fn,ln,wds,locus in a_lines for i in range(len(wds)-1) if get_onset(wds[i])=='t')
print(f"Enrichment: {len(t_ot_bigrams)/t_total_bigrams:.3f} vs base {base_ot_rate:.3f} = {(len(t_ot_bigrams)/t_total_bigrams)/base_ot_rate:.2f}×")

# ---- H335: k→cth=1.60× (n=18) ----
print("\n" + "="*60)
print("H335: k→cth=1.60× (n=18) — which k-words precede cth-words?")
print("="*60)

k_cth_bigrams = []
for fn, ln, wds, locus in a_lines:
    for i in range(len(wds)-1):
        if get_onset(wds[i]) == 'k' and get_onset(wds[i+1]) == 'cth':
            k_cth_bigrams.append((fn, ln, wds[i], wds[i+1]))

print(f"\nA-dialect k→cth bigrams (n={len(k_cth_bigrams)}):")
k_cth_pairs = Counter((a,b) for fn,ln,a,b in k_cth_bigrams)
print(f"Specific pairs: {k_cth_pairs.most_common()}")
print(f"\nFull list:")
for fn, ln, a, b in k_cth_bigrams:
    print(f"  f{fn}.{ln}: [{a}][{b}]")

all_k_words = Counter(w for w in A_words if get_onset(w)=='k')
k_lf_in_k_cth = Counter(a for fn,ln,a,b in k_cth_bigrams)
print(f"\nk-words driving k→cth: {k_lf_in_k_cth.most_common()}")
print(f"Top k-words in A: {all_k_words.most_common(8)}")

k_total_bigrams = sum(1 for fn,ln,wds,locus in a_lines for i in range(len(wds)-1) if get_onset(wds[i])=='k')
base_cth_rate = A_onset['cth'] / A_total
print(f"\nEnrichment: {len(k_cth_bigrams)/k_total_bigrams:.4f} vs base {base_cth_rate:.4f} = {(len(k_cth_bigrams)/k_total_bigrams)/base_cth_rate:.2f}×")

# Also: what cth-words specifically follow k-words?
cth_after_k = Counter(b for fn,ln,a,b in k_cth_bigrams)
print(f"cth-words following k: {cth_after_k.most_common()}")

# ---- H336: ch→r=2.34× (n=15) ----
print("\n" + "="*60)
print("H336: ch→r=2.34× (n=15) — which ch-words precede r-onset?")
print("="*60)

ch_r_bigrams = []
for fn, ln, wds, locus in a_lines:
    for i in range(len(wds)-1):
        if get_onset(wds[i]) == 'ch' and get_onset(wds[i+1]) == 'r':
            ch_r_bigrams.append((fn, ln, wds[i], wds[i+1]))

print(f"\nA-dialect ch→r bigrams (n={len(ch_r_bigrams)}):")
ch_r_pairs = Counter((a,b) for fn,ln,a,b in ch_r_bigrams)
print(f"Top specific pairs: {ch_r_pairs.most_common(10)}")
print(f"\nFull list:")
for fn, ln, a, b in ch_r_bigrams:
    che_marker = " [ch_e]" if is_ch_e(a) else ""
    print(f"  f{fn}.{ln}: [{a}]{che_marker}[{b}]")

ch_in_ch_r = Counter(a for fn,ln,a,b in ch_r_bigrams)
print(f"\nch-words driving ch→r: {ch_in_ch_r.most_common()}")
print(f"ch_e words in ch→r: {sum(1 for fn,ln,a,b in ch_r_bigrams if is_ch_e(a))}/{len(ch_r_bigrams)}")

# Verify overlap with H333
print(f"\nOverlap with H333 [ch_e→r]: {len(che_to_r)} cases are a subset of {len(ch_r_bigrams)} ch→r cases")

# ---- H337: B-dialect ch→cth=2.75× (n=8) ----
print("\n" + "="*60)
print("H337: B-dialect ch→cth=2.75× (n=8) — characterize these 8 bigrams")
print("="*60)

b_ch_cth_bigrams = []
for fn, ln, wds, locus in b_lines:
    for i in range(len(wds)-1):
        if get_onset(wds[i]) == 'ch' and get_onset(wds[i+1]) == 'cth':
            b_ch_cth_bigrams.append((fn, ln, wds[i], wds[i+1]))

print(f"\nB-dialect ch→cth bigrams (n={len(b_ch_cth_bigrams)}):")
for fn, ln, a, b in b_ch_cth_bigrams:
    print(f"  f{fn}.{ln}: [{a}][{b}]")

b_ch_cth_pairs = Counter((a,b) for fn,ln,a,b in b_ch_cth_bigrams)
print(f"\nSpecific pairs: {b_ch_cth_pairs.most_common()}")
print(f"ch-words: {Counter(a for fn,ln,a,b in b_ch_cth_bigrams).most_common()}")
print(f"cth-words: {Counter(b for fn,ln,a,b in b_ch_cth_bigrams).most_common()}")

# Folio breakdown
folio_dist = Counter(fn for fn,ln,a,b in b_ch_cth_bigrams)
print(f"Folio distribution: {dict(sorted(folio_dist.items()))}")

# B-dialect ch→cth enrichment confirmation
b_ch_total_bigrams = sum(1 for fn,ln,wds,locus in b_lines for i in range(len(wds)-1) if get_onset(wds[i])=='ch')
b_cth_rate = B_onset['cth'] / B_total if B_total else 0
print(f"\nB base cth rate: {b_cth_rate:.4f}")
print(f"B ch→cth rate: {len(b_ch_cth_bigrams)}/{b_ch_total_bigrams} = {len(b_ch_cth_bigrams)/b_ch_total_bigrams:.4f}")
if b_cth_rate > 0:
    print(f"Enrichment: {(len(b_ch_cth_bigrams)/b_ch_total_bigrams)/b_cth_rate:.2f}×")

# Compare A ch→cth
a_ch_cth_bigrams = [(fn,ln,wds[i],wds[i+1]) for fn,ln,wds,locus in a_lines
                    for i in range(len(wds)-1)
                    if get_onset(wds[i])=='ch' and get_onset(wds[i+1])=='cth']
a_ch_total_bigrams = sum(1 for fn,ln,wds,locus in a_lines for i in range(len(wds)-1) if get_onset(wds[i])=='ch')
a_cth_rate = A_onset['cth'] / A_total
print(f"\nFor reference — A-dialect ch→cth: {len(a_ch_cth_bigrams)}/{a_ch_total_bigrams} = {len(a_ch_cth_bigrams)/a_ch_total_bigrams:.4f} vs base {a_cth_rate:.4f} = {(len(a_ch_cth_bigrams)/a_ch_total_bigrams)/a_cth_rate:.2f}×")

# ---- H338: B-dialect cthedy/cthdy genuineness ----
print("\n" + "="*60)
print("H338: B-dialect cthedy/cthdy — genuine B-vocabulary or artifacts?")
print("="*60)

# Identify all B-dialect cth- words
b_cth_words_all = [w for fn,ln,wds,locus in b_lines for w in wds if w.startswith('cth')]
b_cth_counter = Counter(b_cth_words_all)
print(f"\nAll B-dialect cth-words (n={len(b_cth_words_all)} total, {len(b_cth_counter)} unique):")
print(f"Top 20: {b_cth_counter.most_common(20)}")

# Artifact markers: do any contain '<', ',', '-'?
b_cth_artifacts = [w for w in b_cth_words_all if any(c in w for c in '<,->')]
print(f"\nB cth-words with artifact characters (<,>,-): {b_cth_artifacts}")

# Focus: cthedy and cthdy specifically
cthedy_b = [w for w in b_cth_words_all if w in ('cthedy', 'cthdy', 'cthey')]
print(f"\ncthedy: {b_cth_counter.get('cthedy',0)}, cthdy: {b_cth_counter.get('cthdy',0)}, cthey: {b_cth_counter.get('cthey',0)}")

# Folio distribution of cthedy in B
cthedy_folio_b = defaultdict(list)
for fn, ln, wds, locus in b_lines:
    for w in wds:
        if w in ('cthedy', 'cthdy', 'cthey'):
            cthedy_folio_b[w].append(fn)

for word, folios in cthedy_folio_b.items():
    print(f"  {word}: {len(folios)} cases, folios: {sorted(set(folios))}")

# Section inference: Pharmaceutical section is f99-f117 (B-Stars/Bio) vs f1-f57 (A-herbal) vs f57-f84 (B-bio)
# Based on folio numbers: f75-f84 is B-bio, f99-f117 is B-pharma/stars
# Compare cthedy distribution by folio range
for word, folios in cthedy_folio_b.items():
    bio_count = sum(1 for f in folios if f <= 84)
    pharma_count = sum(1 for f in folios if 85 <= f <= 102)
    stars_count = sum(1 for f in folios if f >= 103)
    print(f"  {word} section distribution: bio(≤84)={bio_count}, pharma(85-102)={pharma_count}, stars(≥103)={stars_count}")

# Compare with A-dialect cthedy
a_cthedy_words = [w for fn,ln,wds,locus in a_lines for w in wds if w.startswith('cthedy') or w == 'cthdy']
print(f"\nA-dialect cthedy/cthdy occurrences: {len(a_cthedy_words)} — {Counter(a_cthedy_words).most_common()}")

# ---- [oty][l-onset] B-dialect characterization ----
print("\n" + "="*60)
print("[oty][l-onset] B-dialect Stars/Bio — characterize the 6 cases")
print("="*60)

oty_l_b = []
for fn, ln, wds, locus in b_lines:
    for i in range(len(wds)-1):
        if wds[i] == 'oty' and get_onset(wds[i+1]) == 'l':
            oty_l_b.append((fn, ln, wds[i], wds[i+1], locus))

print(f"\nB-dialect [oty][l-word] cases (n={len(oty_l_b)}):")
for fn, ln, a, b, locus in oty_l_b:
    section = 'bio(≤84)' if fn <= 84 else ('pharma(85-102)' if fn <= 102 else 'stars(≥103)')
    print(f"  f{fn}.{ln} [{section}]: [{a}][{b}]")

# Also check A-dialect [oty][l-word]
oty_l_a = [(fn,ln,wds[i],wds[i+1]) for fn,ln,wds,locus in a_lines
           for i in range(len(wds)-1)
           if wds[i]=='oty' and get_onset(wds[i+1])=='l']
print(f"\nA-dialect [oty][l-word] cases (n={len(oty_l_a)}): {[(a,b) for fn,ln,a,b in oty_l_a]}")

# All B oty bigrams (for enrichment reference)
oty_bigrams_b = [(wds[i], wds[i+1], get_onset(wds[i+1]), fn)
                 for fn,ln,wds,locus in b_lines
                 for i in range(len(wds)-1) if wds[i]=='oty']
print(f"\nAll B [oty][X] bigrams (n={len(oty_bigrams_b)}) by onset:")
b_oty_onset = Counter(o for a,b,o,fn in oty_bigrams_b)
for onset, cnt in b_oty_onset.most_common():
    b_base = B_onset.get(onset, 0) / B_total if B_total else 0
    rate = cnt / len(oty_bigrams_b) if oty_bigrams_b else 0
    print(f"  {onset}: {cnt} ({rate:.3f}, base={b_base:.3f}, {rate/b_base:.2f}× if base>0)")

# l-words specifically
l_words_after_oty_b = Counter(b for a,b,o,fn in oty_bigrams_b if o=='l')
print(f"\nl-words specifically after oty in B: {l_words_after_oty_b}")

# Check: is [oty][l] a line-position-specific construction?
oty_l_positions = []
for fn, ln, wds, locus in b_lines:
    for i in range(len(wds)-1):
        if wds[i] == 'oty' and get_onset(wds[i+1]) == 'l':
            oty_l_positions.append({'folio': fn, 'line': ln, 'oty_pos': i, 'line_len': len(wds),
                                    'oty_word': wds[i], 'l_word': wds[i+1]})
print(f"\n[oty][l-word] position analysis:")
for case in oty_l_positions:
    pos_from_end = case['line_len'] - 1 - case['oty_pos']
    print(f"  f{case['folio']}.{case['line']}: oty at pos {case['oty_pos']} (from-end={pos_from_end}), line_len={case['line_len']}, l-word={case['l_word']}")
