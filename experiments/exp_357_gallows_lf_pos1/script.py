"""
exp_357: Gallows-Onset LF → pos1 Distribution (H566)

Background:
- F358 (exp_356): A folio-opener pos1 = ch+sh balanced (25.6%+25.6%).
  Continuation pos1 = ch=27.8%, sh=15.0% (ch dominant, sh lower).
  Question: is the sh elevation at folio-opener pos1 a general rule where
  gallows-LF words (p/k/t/f) produce elevated sh at pos1, or is it
  register-specific to folio-opener lines?

- If gallows-LF → elevated sh at pos1 in ALL lines (including continuation):
  The folio-opener pos1 balance is explained by the fact that folio-opener
  LF is ~74% gallows, and gallows always produces sh elevation at pos1.

- If gallows-LF → sh elevation is FOLIO-OPENER-SPECIFIC:
  Something about the folio-opener register specifically causes sh to
  appear at pos1 after a gallows onset.

Plan:
1. Collect A-dialect continuation lines only
2. Group by LF onset (gallows vs non-gallows)
3. Compare pos1 sh% for gallows-LF vs non-gallows-LF continuation lines
4. If gallows-LF continuation lines also have elevated sh at pos1,
   the folio-opener pattern is explained by the onset-class bigram.
5. Also compute for B-dialect continuation lines.
"""

import os, re
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser('~/voynich-cryptanalyst')
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

def folio_base(folio):
    return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    return 'B' if (stats['edy'] + stats['eedy']) / total >= 0.05 else 'A'

ONSET_ORDER = [
    ('qok','qok'),('qot','qot'),('qo','qo'),('cth','cth'),
    ('ch','ch'),('sh','sh'),('ok','ok'),('ot','ot'),('ol','ol'),
    ('d','d'),('s','s'),('y','y'),('k','k'),('t','t'),
    ('l','l'),('r','r'),('p','p'),('f','f'),('o','o')
]

GALLOWS = {'k', 't', 'p', 'f'}

def get_onset(word):
    for label, prefix in ONSET_ORDER:
        if word.startswith(prefix):
            return label
    return 'other'

def is_gallows(word):
    return get_onset(word) in GALLOWS

# Pass 1: classify folios
folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
with open(DATA_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'): continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
        if not m: continue
        folio = m.group(1).lstrip('+*=&~')
        fb = folio_base(folio)
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        for w in words:
            folio_word_stats[fb]['total'] += 1
            if w.endswith('eedy'): folio_word_stats[fb]['eedy'] += 1
            elif w.endswith('edy'): folio_word_stats[fb]['edy'] += 1

folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}

# Pass 2: collect lines, classify into registers
folio_lines = defaultdict(list)

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'): continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
        if not m: continue
        folio = m.group(1).lstrip('+*=&~')
        line_num = int(m.group(2))
        locus_code = m.group(3)
        fb = folio_base(folio)
        dialect = folio_dialect.get(fb, 'unknown')
        if dialect not in ('A', 'B'): continue
        lc = locus_code.lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'): continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if len(words) < 2: continue
        folio_lines[fb].append((line_num, words, dialect))

# Separate registers
register_lines = defaultdict(lambda: defaultdict(list))  # dialect -> register -> list of words

for fb, lines_list in folio_lines.items():
    if not lines_list: continue
    dialect = lines_list[0][2]
    line_nums = [ln for ln, _, _ in lines_list]
    min_ln = min(line_nums)
    max_ln = max(line_nums)
    for ln, words, d in lines_list:
        if ln == min_ln:
            register_lines[dialect]['opener'].append(words)
        elif ln == max_ln:
            register_lines[dialect]['closer'].append(words)
        else:
            register_lines[dialect]['cont'].append(words)

# Core analysis: for continuation lines, conditional P(pos1_onset | LF_gallows_class)
print("=" * 70)
print("P(pos1_onset | LF_onset_class) IN CONTINUATION LINES")
print("=" * 70)

KEY_ONSETS_POS1 = ['ch', 'sh', 'd', 'qok', 'ok', 'y', 's', 'o', 'cth', 'ot', 'ol', 'l', 'k', 't', 'p', 'f', 'other']

for dialect in ['A', 'B']:
    cont_lines = register_lines[dialect]['cont']
    opener_lines = register_lines[dialect]['opener']
    closer_lines = register_lines[dialect]['closer']
    print(f"\n{'='*70}")
    print(f"{dialect}-DIALECT ANALYSIS")
    print(f"{'='*70}")

    # Group continuation lines by LF gallows class
    gallows_lf_lines = [words for words in cont_lines if is_gallows(words[0])]
    non_gallows_lf_lines = [words for words in cont_lines if not is_gallows(words[0])]

    n_gallows = len(gallows_lf_lines)
    n_non_gallows = len(non_gallows_lf_lines)

    print(f"\nContinuation lines with gallows LF: N={n_gallows}")
    print(f"Continuation lines with non-gallows LF: N={n_non_gallows}")

    # pos1 onset distribution for each group
    gallows_pos1 = [get_onset(words[1]) for words in gallows_lf_lines if len(words) >= 2]
    non_gallows_pos1 = [get_onset(words[1]) for words in non_gallows_lf_lines if len(words) >= 2]

    gall_c = Counter(gallows_pos1)
    non_gall_c = Counter(non_gallows_pos1)
    n_gall_pos1 = len(gallows_pos1)
    n_non_gall_pos1 = len(non_gallows_pos1)

    print(f"\n{dialect} Continuation lines: pos1 by LF gallows class:")
    print(f"{'Onset':<10} {'Gallows_LF%':>13} {'NonGallows_LF%':>16} {'Opener_pos1%':>14} {'E(Gallows/NonGallows)':>22}")

    # Opener pos1 for reference
    opener_pos1_words = [get_onset(words[1]) for words in opener_lines if len(words) >= 2]
    opener_pos1_c = Counter(opener_pos1_words)
    n_opener_pos1 = len(opener_pos1_words)

    for onset in KEY_ONSETS_POS1:
        pg = gall_c.get(onset, 0) / n_gall_pos1 if n_gall_pos1 > 0 else 0
        pn = non_gall_c.get(onset, 0) / n_non_gall_pos1 if n_non_gall_pos1 > 0 else 0
        po = opener_pos1_c.get(onset, 0) / n_opener_pos1 if n_opener_pos1 > 0 else 0
        e = pg / pn if pn > 0 else (float('inf') if pg > 0 else 1.0)
        if max(pg, pn, po) >= 0.02:
            es = f"{e:.2f}×" if e != float('inf') else "inf"
            print(f"  {onset:<10} {100*pg:>12.1f}%  {100*pn:>15.1f}%  {100*po:>13.1f}%  {es:>22}")

    # Summary: sh and ch specifically
    g_sh = 100 * gall_c.get('sh', 0) / n_gall_pos1
    n_sh = 100 * non_gall_c.get('sh', 0) / n_non_gall_pos1
    g_ch = 100 * gall_c.get('ch', 0) / n_gall_pos1
    n_ch = 100 * non_gall_c.get('ch', 0) / n_non_gall_pos1
    o_sh = 100 * opener_pos1_c.get('sh', 0) / n_opener_pos1
    o_ch = 100 * opener_pos1_c.get('ch', 0) / n_opener_pos1
    print(f"\n  SUMMARY: sh at pos1:")
    print(f"    Gallows-LF cont: {g_sh:.1f}%")
    print(f"    Non-gallows-LF cont: {n_sh:.1f}%")
    print(f"    Folio-opener: {o_sh:.1f}%")
    print(f"  ch at pos1:")
    print(f"    Gallows-LF cont: {g_ch:.1f}%")
    print(f"    Non-gallows-LF cont: {n_ch:.1f}%")
    print(f"    Folio-opener: {o_ch:.1f}%")

    # Refined: P(pos1_sh | LF_onset) for each specific onset in continuation
    print(f"\n{dialect} Continuation P(sh at pos1 | LF onset):")
    lf_onset_groups = defaultdict(list)
    for words in cont_lines:
        if len(words) >= 2:
            lf_onset_groups[get_onset(words[0])].append(get_onset(words[1]))

    print(f"  {'LF_onset':<10} {'N':>6} {'sh%':>8} {'ch%':>8} {'ch/sh_ratio':>12}")
    for lf_onset in ['p', 'k', 't', 'f', 'ch', 'sh', 'd', 'y', 's', 'qok', 'ok']:
        pos1_list = lf_onset_groups.get(lf_onset, [])
        n = len(pos1_list)
        if n < 3: continue
        pos1_c = Counter(pos1_list)
        sh_pct = 100 * pos1_c.get('sh', 0) / n
        ch_pct = 100 * pos1_c.get('ch', 0) / n
        ratio = ch_pct / sh_pct if sh_pct > 0 else float('inf')
        rs = f"{ratio:.2f}" if ratio != float('inf') else "inf"
        print(f"  {lf_onset:<10} {n:>6} {sh_pct:>7.1f}%  {ch_pct:>7.1f}%  {rs:>12}")

# Cross-register comparison for specific onset classes
print("\n" + "=" * 70)
print("CROSS-REGISTER sh% AT pos1: DOES GALLOWS-LF EXPLAIN OPENER sh?")
print("=" * 70)

for dialect in ['A', 'B']:
    opener = register_lines[dialect]['opener']
    cont = register_lines[dialect]['cont']

    # Opener breakdown: gallows vs non-gallows LF at opener
    opener_gallows = [words for words in opener if is_gallows(words[0])]
    opener_non_gall = [words for words in opener if not is_gallows(words[0])]

    # Continuation breakdown
    cont_gallows = [words for words in cont if is_gallows(words[0])]
    cont_non_gall = [words for words in cont if not is_gallows(words[0])]

    def pos1_sh(lines):
        pos1 = [get_onset(words[1]) for words in lines if len(words) >= 2]
        if not pos1: return 0, 0
        return sum(1 for o in pos1 if o == 'sh'), len(pos1)

    og_sh, og_n = pos1_sh(opener_gallows)
    on_sh, on_n = pos1_sh(opener_non_gall)
    cg_sh, cg_n = pos1_sh(cont_gallows)
    cn_sh, cn_n = pos1_sh(cont_non_gall)

    print(f"\n{dialect}-dialect sh at pos1:")
    print(f"  Opener gallows-LF:     {og_sh}/{og_n} = {100*og_sh/og_n:.1f}%" if og_n else "  Opener gallows-LF: N=0")
    print(f"  Opener non-gall-LF:    {on_sh}/{on_n} = {100*on_sh/on_n:.1f}%" if on_n else "  Opener non-gall-LF: N=0")
    print(f"  Cont gallows-LF:       {cg_sh}/{cg_n} = {100*cg_sh/cg_n:.1f}%")
    print(f"  Cont non-gall-LF:      {cn_sh}/{cn_n} = {100*cn_sh/cn_n:.1f}%")
    print(f"  → Does gallows-LF explain opener sh level? {'YES' if abs(100*og_sh/og_n - 100*cg_sh/cg_n) < 5 else 'NO'}")
