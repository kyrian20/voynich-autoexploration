#!/usr/bin/env python3
"""
exp_164: Self-succession and cross-onset bigram details
H330: qot→qot and qot→l specific pairs
H331: ok→ok specific pairs
H332: l→l cases (n=3) in A-dialect
H333: ch_e↔r bidirectional pairs
BONUS: B-dialect onset self-succession survey (compare to A)
BONUS2: Full onset bigram matrix heatmap for A-dialect
"""
import re
from collections import Counter, defaultdict

CORPUS = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

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

def compute_bigrams(target_lines):
    onset_counts = Counter()
    bigram_counts = Counter()
    word_bigram_counts = Counter()
    total_bigrams = 0
    for fn, sec, dial, wds in target_lines:
        for w in wds:
            onset_counts[get_onset(w)] += 1
        for i in range(len(wds)-1):
            o1 = get_onset(wds[i])
            o2 = get_onset(wds[i+1])
            bigram_counts[(o1, o2)] += 1
            word_bigram_counts[(wds[i], wds[i+1])] += 1
            total_bigrams += 1
    return onset_counts, bigram_counts, word_bigram_counts, total_bigrams

a_lines = [(fn, sec, dial, wds) for fn, sec, dial, wds in lines_data if dial == 'A']
b_lines = [(fn, sec, dial, wds) for fn, sec, dial, wds in lines_data if dial == 'B']

a_onset, a_bigram, a_word_bigram, a_total = compute_bigrams(a_lines)
b_onset, b_bigram, b_word_bigram, b_total = compute_bigrams(b_lines)
a_total_words = sum(a_onset.values())
b_total_words = sum(b_onset.values())

print(f"A-dialect: {len(a_lines)} lines, {a_total_words} words, {a_total} bigrams")
print(f"B-dialect: {len(b_lines)} lines, {b_total_words} words, {b_total} bigrams")

def show_specific_pairs(onset1, onset2, bigram_counts, word_bigram_counts, total, onset_counts, total_words, lines_data, dialect, label):
    obs = bigram_counts.get((onset1, onset2), 0)
    r1 = onset_counts.get(onset1, 0) / total_words
    r2 = onset_counts.get(onset2, 0) / total_words
    exp = total * r1 * r2
    enrich = obs / exp if exp > 0 else float('inf')
    print(f"\n{label}: [{onset1}][{onset2}] obs={obs}, exp={exp:.1f}, enrich={enrich:.2f}×")
    # Top word pairs
    pairs = [(w1, w2, cnt) for (w1, w2), cnt in word_bigram_counts.items()
             if get_onset(w1) == onset1 and get_onset(w2) == onset2]
    pairs.sort(key=lambda x: -x[2])
    for w1, w2, cnt in pairs[:15]:
        print(f"  {w1} → {w2}: {cnt}×")
    # Show examples from lines
    print(f"  Examples:")
    shown = 0
    for fn, sec, dial, wds in lines_data:
        if dial != dialect: continue
        for i in range(len(wds)-1):
            if get_onset(wds[i]) == onset1 and get_onset(wds[i+1]) == onset2:
                print(f"    f{fn} [{sec}]: ...{wds[max(0,i-1)]} [{wds[i]}][{wds[i+1]}] {wds[i+2] if i+2<len(wds) else '(end)'}...")
                shown += 1
                if shown >= 10: break
        if shown >= 10: break

# --- H330: qot→qot and qot→l ---
print("\n=== H330: qot→qot AND qot→l SPECIFIC PAIRS (A-dialect) ===")
show_specific_pairs('qot', 'qot', a_bigram, a_word_bigram, a_total, a_onset, a_total_words, lines_data, 'A', "qot→qot")
show_specific_pairs('qot', 'l', a_bigram, a_word_bigram, a_total, a_onset, a_total_words, lines_data, 'A', "qot→l")
show_specific_pairs('qok', 'l', a_bigram, a_word_bigram, a_total, a_onset, a_total_words, lines_data, 'A', "qok→l")

# --- H331: ok→ok ---
print("\n=== H331: ok→ok SPECIFIC PAIRS (A-dialect) ===")
show_specific_pairs('ok', 'ok', a_bigram, a_word_bigram, a_total, a_onset, a_total_words, lines_data, 'A', "ok→ok")

# --- H332: l→l in A-dialect ---
print("\n=== H332: l→l IN A-DIALECT (n=3) ===")
l_l_pairs = [(fn, sec, dial, wds, i) for fn, sec, dial, wds in lines_data if dial == 'A'
              for i in range(len(wds)-1) if get_onset(wds[i]) == 'l' and get_onset(wds[i+1]) == 'l']
print(f"l→l in A-dialect: {len(l_l_pairs)} cases")
for fn, sec, dial, wds, i in l_l_pairs:
    print(f"  f{fn} [{sec}/{dial}]: {' '.join(wds)} [l→l at positions {i},{i+1}: {wds[i]}→{wds[i+1]}]")

# Also check B-dialect
l_l_b = [(fn, sec, dial, wds, i) for fn, sec, dial, wds in lines_data if dial == 'B'
          for i in range(len(wds)-1) if get_onset(wds[i]) == 'l' and get_onset(wds[i+1]) == 'l']
print(f"\nl→l in B-dialect: {len(l_l_b)} cases")
for fn, sec, dial, wds, i in l_l_b[:20]:
    print(f"  f{fn} [{sec}/{dial}]: {' '.join(wds)} [l→l at positions {i},{i+1}: {wds[i]}→{wds[i+1]}]")

# l onset self-succession enrichment in B
l_obs_b = b_bigram.get(('l','l'), 0)
r_l_b = b_onset.get('l', 0) / b_total_words
exp_l_b = b_total * r_l_b * r_l_b
print(f"\nB-dialect l→l: obs={l_obs_b}, exp={exp_l_b:.2f}, enrich={l_obs_b/exp_l_b:.2f}×")

# --- H333: ch_e↔r bidirectional ---
print("\n=== H333: ch_e↔r BIDIRECTIONAL PAIRS (A-dialect) ===")
show_specific_pairs('ch_e', 'r', a_bigram, a_word_bigram, a_total, a_onset, a_total_words, lines_data, 'A', "ch_e→r")
show_specific_pairs('r', 'ch_e', a_bigram, a_word_bigram, a_total, a_onset, a_total_words, lines_data, 'A', "r→ch_e")

# --- BONUS: B-dialect onset self-succession survey ---
print("\n=== B-DIALECT ONSET SELF-SUCCESSION SURVEY ===\n")
print(f"{'Onset':<10} {'observed':>10} {'expected':>10} {'enrich':>8}")
for onset in ONSET_ORDER + ['other']:
    oc = b_onset.get(onset, 0)
    if oc < 5: continue
    baseline_rate = oc / b_total_words
    expected = b_total * baseline_rate * baseline_rate
    observed = b_bigram.get((onset, onset), 0)
    enrich = observed / expected if expected > 0 else float('inf')
    print(f"  {onset:<10} {observed:>10} {expected:>10.2f} {enrich:>8.2f}×")

# --- BONUS2: Top enriched bigrams in B that differ from A ---
print("\n\n=== B-DIALECT TOP ENRICHED BIGRAMS ===\n")
b_enrichments = []
for (o1, o2), obs in b_bigram.items():
    if obs < 5: continue
    r1 = b_onset.get(o1, 0) / b_total_words
    r2 = b_onset.get(o2, 0) / b_total_words
    exp = b_total * r1 * r2
    if exp < 1: continue
    enrich = obs / exp
    b_enrichments.append((enrich, obs, o1, o2))
b_enrichments.sort(reverse=True)
print(f"{'o1':>10} {'o2':>10} {'obs':>6} {'exp':>8} {'enrich':>8}")
for enrich, obs, o1, o2 in b_enrichments[:20]:
    r1 = b_onset.get(o1, 0) / b_total_words
    r2 = b_onset.get(o2, 0) / b_total_words
    exp = b_total * r1 * r2
    print(f"  {o1:>10} → {o2:>10}: {obs:>6} {exp:>8.1f} {enrich:>8.2f}×")

# --- Full onset bigram matrix (A-dialect, top enriched) ---
print("\n\n=== A-DIALECT FULL BIGRAM MATRIX (enrichments ≥1.5× with obs≥5) ===\n")
a_enrichments = []
for (o1, o2), obs in a_bigram.items():
    if obs < 5: continue
    r1 = a_onset.get(o1, 0) / a_total_words
    r2 = a_onset.get(o2, 0) / a_total_words
    exp = a_total * r1 * r2
    if exp < 1: continue
    enrich = obs / exp
    if enrich >= 1.5:
        a_enrichments.append((enrich, obs, o1, o2))
a_enrichments.sort(reverse=True)
for enrich, obs, o1, o2 in a_enrichments:
    r1 = a_onset.get(o1, 0) / a_total_words
    r2 = a_onset.get(o2, 0) / a_total_words
    exp = a_total * r1 * r2
    print(f"  {o1:>10} → {o2:>10}: {obs:>6} {exp:>8.1f} {enrich:>8.2f}×")
