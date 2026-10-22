#!/usr/bin/env python3
"""
exp_163: [ot-word][ot-word] bigram enrichment (H327), [dchor][cthor] construction (H328),
         [daiin][dam] line structure (H329), onset self-succession enrichment survey
H327: Is [ot][ot] bigram enriched? (sparked by f17: otor oteol consecutive)
H328: Two [dchor@LF][cth@second] lines — is the cth-word cthor both times? [dchor][cthor]?
H329: Three [daiin ... dam] lines — are [daiin][dam] immediate bigrams?
BONUS: Survey all onset class self-succession enrichments to find systematic same-class chaining.
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
print(f"A-dialect lines: {len(a_lines)}")

# Baseline: bigram counts in A-dialect
onset_counts = Counter()
bigram_counts = Counter()
total_bigrams = 0
for fn, sec, dial, wds in a_lines:
    for i, w in enumerate(wds):
        onset_counts[get_onset(w)] += 1
    for i in range(len(wds)-1):
        o1 = get_onset(wds[i])
        o2 = get_onset(wds[i+1])
        bigram_counts[(o1, o2)] += 1
        total_bigrams += 1

total_words = sum(onset_counts.values())
print(f"A-dialect total bigrams: {total_bigrams}")

# Onset rates
onset_rates = {o: onset_counts[o] / total_words for o in onset_counts}

# --- H327: [ot][ot] bigram enrichment ---
print("\n=== H327: ONSET SELF-SUCCESSION ENRICHMENT (A-dialect) ===\n")
print("Self-succession = onset X followed immediately by onset X")
print(f"\n{'Onset':<10} {'observed':>10} {'expected':>10} {'enrich':>8} {'obs_n':>8}")
for onset in ONSET_ORDER + ['other']:
    oc = onset_counts.get(onset, 0)
    if oc < 5: continue
    baseline_rate = oc / total_words
    # Expected bigrams = total_bigrams * P(onset1=X) * P(onset2=X)
    expected = total_bigrams * baseline_rate * baseline_rate
    observed = bigram_counts.get((onset, onset), 0)
    enrich = observed / expected if expected > 0 else float('inf')
    print(f"  {onset:<10} {observed:>10} {expected:>10.2f} {enrich:>8.2f}× {observed:>8}")

# Specifically [ot][ot]
ot_rate = onset_counts.get('ot', 0) / total_words
ot_ot_obs = bigram_counts.get(('ot','ot'), 0)
ot_ot_exp = total_bigrams * ot_rate * ot_rate
print(f"\n[ot][ot] specifically: observed={ot_ot_obs}, expected={ot_ot_exp:.2f}, enrichment={ot_ot_obs/ot_ot_exp:.2f}×")

# Show all [ot][ot] examples
print(f"\n[ot-word][ot-word] consecutive pairs in A-dialect:")
ot_ot_pairs = Counter()
ot_ot_examples = []
for fn, sec, dial, wds in a_lines:
    for i in range(len(wds)-1):
        if get_onset(wds[i]) == 'ot' and get_onset(wds[i+1]) == 'ot':
            pair = (wds[i], wds[i+1])
            ot_ot_pairs[pair] += 1
            ot_ot_examples.append((fn, sec, wds, i))
print(f"Total [ot][ot] pairs: {ot_ot_obs}")
for pair, cnt in ot_ot_pairs.most_common(15):
    print(f"  {pair[0]} → {pair[1]}: {cnt}×")
print(f"\nExamples (up to 20):")
for fn, sec, wds, i in ot_ot_examples[:20]:
    print(f"  f{fn} [{sec}]: {' '.join(wds)} [pair at positions {i},{i+1}]")

# --- H328: [dchor@LF][cth@second] full lines ---
print("\n\n=== H328: [dchor@LF][cth@second] FULL LINES ===\n")
dchor_lf_cth_second = [(fn, sec, dial, wds) for fn, sec, dial, wds in a_lines
                        if wds and wds[0] == 'dchor' and len(wds) >= 2 and get_onset(wds[1]) == 'cth']
print(f"[dchor@LF][cth@second] lines: {len(dchor_lf_cth_second)}")
for fn, sec, dial, wds in dchor_lf_cth_second:
    print(f"  f{fn} [{sec}/{dial}]: {' '.join(wds)}")
    print(f"    LF-word={wds[0]}, second-word={wds[1]}, onset2={get_onset(wds[1])}")

# Check: is second word cthor specifically?
for fn, sec, dial, wds in dchor_lf_cth_second:
    print(f"  --> second word is: '{wds[1]}' (is cthor: {wds[1]=='cthor'})")

# All d-ch-prefix LF → cthor@second
print(f"\nAll d-ch-prefix@LF → cthor@second lines:")
for fn, sec, dial, wds in a_lines:
    if wds and wds[0].startswith('dch') and len(wds) >= 2 and wds[1] == 'cthor':
        print(f"  f{fn} [{sec}]: {' '.join(wds)}")

# --- H329: [daiin ... dam@LL] line structure ---
print("\n\n=== H329: [daiin...dam@LL] LINE STRUCTURE ===\n")
dam_lines = [(fn, sec, dial, wds) for fn, sec, dial, wds in a_lines if wds and wds[-1] == 'dam']
daiin_dam_lines = [(fn, sec, dial, wds) for fn, sec, dial, wds in dam_lines if 'daiin' in wds[:-1]]
print(f"Lines ending in dam with daiin anywhere: {len(daiin_dam_lines)}")
daiin_pen_dam = [(fn, sec, dial, wds) for fn, sec, dial, wds in dam_lines if len(wds) >= 2 and wds[-2] == 'daiin']
print(f"Lines with daiin immediately before dam: {len(daiin_pen_dam)}")
for fn, sec, dial, wds in daiin_pen_dam:
    print(f"  f{fn} [{sec}]: {' '.join(wds)} (len={len(wds)})")

# Immediate [daiin][dam] bigrams
daiin_dam_immediate = [(fn, sec, dial, wds) for fn, sec, dial, wds in a_lines
                        if any(wds[i]=='daiin' and i+1<len(wds) and wds[i+1]=='dam' for i in range(len(wds)))]
print(f"\nImmediate [daiin][dam] bigrams in A: {len(daiin_dam_immediate)}")
for fn, sec, dial, wds in daiin_dam_immediate:
    print(f"  f{fn} [{sec}]: {' '.join(wds)}")

# --- BONUS: Cross-onset bigram enrichment heatmap for key transitions ---
print("\n\n=== BONUS: KEY CROSS-ONSET BIGRAM ENRICHMENTS (A-dialect) ===\n")
print("Top-10 most enriched bigrams (min 3 observed):")

bigram_enrichments = []
for (o1, o2), obs in bigram_counts.items():
    if obs < 3: continue
    r1 = onset_counts.get(o1, 0) / total_words
    r2 = onset_counts.get(o2, 0) / total_words
    exp = total_bigrams * r1 * r2
    if exp < 0.5: continue
    enrich = obs / exp
    bigram_enrichments.append((enrich, obs, o1, o2))

bigram_enrichments.sort(reverse=True)
print(f"{'o1':>8} {'o2':>8} {'obs':>6} {'exp':>8} {'enrich':>8}")
for enrich, obs, o1, o2 in bigram_enrichments[:20]:
    r1 = onset_counts.get(o1, 0) / total_words
    r2 = onset_counts.get(o2, 0) / total_words
    exp = total_bigrams * r1 * r2
    print(f"  {o1:>8} → {o2:>8}: {obs:>6} {exp:>8.1f} {enrich:>8.2f}×")
