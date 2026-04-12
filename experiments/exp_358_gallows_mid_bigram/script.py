"""
exp_358: Gallows→sh Bigram in MID Positions (H567)

Background:
- F359 (exp_357): gallows→sh E=1.72× (A) / 1.22× (B) at LF→pos1 position
- Question: Is this a general within-line bigram rule (all adjacent pairs where
  first word is gallows-onset) or positional (LF→pos1 only)?

Plan:
1. Collect ALL adjacent word pairs from continuation lines
2. Split by position: LF→pos1 (i=0→1), pos1→pos2 (i=1→2), MID pairs (i≥2), LL-adjacent (last two words)
3. For each position pair, compute P(sh | gallows_prev) vs P(sh | non-gallows_prev)
4. Compare across positions to see if gallows→sh is position-dependent
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

# Pass 2: collect lines
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

# Get continuation lines only
cont_lines = defaultdict(list)
for fb, lines_list in folio_lines.items():
    if not lines_list: continue
    dialect = lines_list[0][2]
    line_nums = [ln for ln, _, _ in lines_list]
    min_ln = min(line_nums)
    max_ln = max(line_nums)
    for ln, words, d in lines_list:
        if ln != min_ln and ln != max_ln:
            cont_lines[dialect].append(words)

print("=" * 70)
print("GALLOWS→sh BIGRAM BY POSITION IN CONTINUATION LINES")
print("=" * 70)

for dialect in ['A', 'B']:
    lines = cont_lines[dialect]
    print(f"\n{'='*70}")
    print(f"{dialect}-DIALECT (N_lines={len(lines)})")
    print(f"{'='*70}")

    # Collect bigrams by position category
    # pos_key: 'LF_pos1' (i=0→1), 'pos1_pos2' (i=1→2), 'MID_inner' (i=2→N-3), 'pre_LL' (last-two)
    bigrams_by_pos = defaultdict(list)
    for words in lines:
        n = len(words)
        for i in range(n - 1):
            o1 = get_onset(words[i])
            o2 = get_onset(words[i+1])
            gallows1 = is_gallows(words[i])
            if i == 0:
                pos_key = 'LF→pos1'
            elif i == 1:
                pos_key = 'pos1→pos2'
            elif i == n - 2:
                pos_key = 'pre-LL→LL'
            else:
                pos_key = 'MID_inner'
            bigrams_by_pos[pos_key].append((o1, o2, gallows1))

    # For each position, compute P(sh | gallows_prev) and P(sh | non_gallows_prev)
    print(f"\n{'Position':<15} {'N_gall':>8} {'sh_gall%':>10} {'N_nongall':>10} {'sh_nongall%':>12} {'E':>8} | {'ch_gall%':>10} {'ch_nongall%':>12} {'E_ch':>8}")
    
    for pos_key in ['LF→pos1', 'pos1→pos2', 'MID_inner', 'pre-LL→LL']:
        bigrams = bigrams_by_pos.get(pos_key, [])
        if not bigrams: continue
        
        gallows_next = [o2 for o1, o2, g in bigrams if g]
        nongall_next = [o2 for o1, o2, g in bigrams if not g]
        
        n_g = len(gallows_next)
        n_n = len(nongall_next)
        
        sh_g = sum(1 for o in gallows_next if o == 'sh')
        sh_n = sum(1 for o in nongall_next if o == 'sh')
        ch_g = sum(1 for o in gallows_next if o == 'ch')
        ch_n = sum(1 for o in nongall_next if o == 'ch')
        
        pg_sh = sh_g / n_g if n_g > 0 else 0
        pn_sh = sh_n / n_n if n_n > 0 else 0
        e_sh = pg_sh / pn_sh if pn_sh > 0 else float('inf')
        
        pg_ch = ch_g / n_g if n_g > 0 else 0
        pn_ch = ch_n / n_n if n_n > 0 else 0
        e_ch = pg_ch / pn_ch if pn_ch > 0 else float('inf')
        
        e_sh_s = f"{e_sh:.2f}×"
        e_ch_s = f"{e_ch:.2f}×"
        
        print(f"  {pos_key:<15} {n_g:>8} {100*pg_sh:>9.1f}%  {n_n:>10} {100*pn_sh:>11.1f}%  {e_sh_s:>8} | {100*pg_ch:>9.1f}%  {100*pn_ch:>11.1f}%  {e_ch_s:>8}")
    
    # Also compute OVERALL (all positions combined)
    all_bg = sum(bigrams_by_pos.values(), [])
    gallows_all = [o2 for o1, o2, g in all_bg if g]
    nongall_all = [o2 for o1, o2, g in all_bg if not g]
    n_ga = len(gallows_all)
    n_na = len(nongall_all)
    sh_ga = sum(1 for o in gallows_all if o == 'sh')
    sh_na = sum(1 for o in nongall_all if o == 'sh')
    ch_ga = sum(1 for o in gallows_all if o == 'ch')
    ch_na = sum(1 for o in nongall_all if o == 'ch')
    pg_sh = sh_ga / n_ga if n_ga > 0 else 0
    pn_sh = sh_na / n_na if n_na > 0 else 0
    e_sh = pg_sh / pn_sh if pn_sh > 0 else 0
    pg_ch = ch_ga / n_ga if n_ga > 0 else 0
    pn_ch = ch_na / n_na if n_na > 0 else 0
    e_ch = pg_ch / pn_ch if pn_ch > 0 else 0
    print(f"  {'ALL_POSITIONS':<15} {n_ga:>8} {100*pg_sh:>9.1f}%  {n_na:>10} {100*pn_sh:>11.1f}%  {e_sh:.2f}× | {100*pg_ch:>9.1f}%  {100*pn_ch:>11.1f}%  {e_ch:.2f}×")

    # Per-gallows-onset breakdown for ALL positions
    print(f"\n{dialect} Per-gallows-onset sh/ch rates at next position (all positions combined):")
    all_by_o1 = defaultdict(list)
    for o1, o2, g in all_bg:
        all_by_o1[o1].append(o2)
    
    print(f"  {'LF_onset':<10} {'N':>6} {'sh%':>8} {'ch%':>8} {'ch/sh':>8}")
    for lf_onset in ['p', 'k', 't', 'f', 'ch', 'sh', 'd', 'y', 's', 'qok', 'ok']:
        nexts = all_by_o1.get(lf_onset, [])
        n = len(nexts)
        if n < 10: continue
        nc = Counter(nexts)
        sh_pct = 100 * nc.get('sh', 0) / n
        ch_pct = 100 * nc.get('ch', 0) / n
        ratio = ch_pct / sh_pct if sh_pct > 0 else float('inf')
        rs = f"{ratio:.2f}" if ratio != float('inf') else "inf"
        print(f"  {lf_onset:<10} {n:>6} {sh_pct:>7.1f}%  {ch_pct:>7.1f}%  {rs:>8}")

