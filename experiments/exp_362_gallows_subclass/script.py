"""
exp_362: Gallows Subclass Split at MID Positions (H568)
F360: all-positions combined shows {p,f}→sh-biased, {k,t}→ch-biased.
Question: Does this split persist in MID_inner positions where
A-dialect gallows→sh E=1.42× (multi-position) and B-dialect E=1.00× (neutral)?
"""
from pathlib import Path as _RepositoryPath

import os, re
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
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

def get_onset(word):
    for label, prefix in ONSET_ORDER:
        if word.startswith(prefix):
            return label
    return 'other'

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

# Register classification
register_lines = defaultdict(lambda: defaultdict(list))
for fb, lines_list in folio_lines.items():
    if not lines_list: continue
    dialect = lines_list[0][2]
    line_nums = [ln for ln, _, _ in lines_list]
    min_ln = min(line_nums)
    max_ln = max(line_nums)
    for ln, words, d in lines_list:
        if ln == min_ln: reg = 'opener'
        elif ln == max_ln: reg = 'closer'
        else: reg = 'cont'
        register_lines[dialect][reg].append(words)

print("=" * 70)
print("GALLOWS SUBCLASS SPLIT: {p,f}→sh vs {k,t}→ch BY POSITION (H568)")
print("=" * 70)

for dialect in ['A', 'B']:
    cont_lines = register_lines[dialect]['cont']
    print(f"\n{'='*70}")
    print(f"{dialect}-DIALECT")
    print(f"{'='*70}")

    # Collect pairs with position category
    def pos_cat(i, n):
        if i == 0: return 'LF'
        elif i == 1: return 'pos1'
        elif i == n-1: return 'LL'
        else: return 'MID'

    # For each position category, collect (prev_gallows_onset, next_onset)
    pos_pairs = defaultdict(list)  # cat -> [(prev_o, next_o)]
    for wlist in cont_lines:
        n = len(wlist)
        for i in range(n-1):
            prev = wlist[i]
            nxt = wlist[i+1]
            prev_o = get_onset(prev)
            next_o = get_onset(nxt)
            pp = pos_cat(i, n)
            np_ = pos_cat(i+1, n)
            
            # Classify pair position
            if np_ == 'LL':
                cat = 'pre-LL→LL'
            elif pp == 'LF':
                cat = 'LF→pos1'
            elif pp == 'pos1':
                cat = 'pos1→next'
            else:
                cat = 'MID_inner'
            
            if prev_o in ('p','f','k','t','ch','sh','d','y','qok','ok','s','cth','ot','ol'):
                pos_pairs[cat].append((prev_o, next_o))

    print(f"\n--- sh and ch rates after each gallows onset by position ---")
    gallows_onsets = ['p', 'f', 'k', 't']
    non_gallows_ref = ['ch', 'sh', 'd', 'y', 'qok']
    
    for cat in ['LF→pos1', 'pos1→next', 'MID_inner', 'pre-LL→LL']:
        pairs = pos_pairs[cat]
        total_by_onset = defaultdict(int)
        sh_by_onset = defaultdict(int)
        ch_by_onset = defaultdict(int)
        for po, no in pairs:
            total_by_onset[po] += 1
            if no == 'sh': sh_by_onset[po] += 1
            if no == 'ch': ch_by_onset[po] += 1
        
        print(f"\n  Position: {cat}")
        print(f"  {'Onset':<8} {'N':>6} {'sh%':>7} {'ch%':>7} {'ch/sh':>8}")
        for onset in ['p','f','k','t']:
            n = total_by_onset[onset]
            if n < 3: 
                print(f"  {onset:<8} {n:>6} (N too small)")
                continue
            sh_p = 100*sh_by_onset[onset]/n
            ch_p = 100*ch_by_onset[onset]/n
            ratio = ch_p/sh_p if sh_p > 0 else float('inf')
            print(f"  {onset:<8} {n:>6} {sh_p:>6.1f}% {ch_p:>6.1f}% {ratio:>7.2f}")
        
        # Non-gallows reference
        for onset in ['ch','sh','d','y']:
            n = total_by_onset[onset]
            if n < 10: continue
            sh_p = 100*sh_by_onset[onset]/n
            ch_p = 100*ch_by_onset[onset]/n
            ratio = ch_p/sh_p if sh_p > 0 else float('inf')
            print(f"  {onset:<8} {n:>6} {sh_p:>6.1f}% {ch_p:>6.1f}% {ratio:>7.2f}  [ref]")
    
    # Summary table: MID_inner specifically
    print(f"\n--- SUMMARY: MID_inner position only ---")
    mid_pairs = pos_pairs['MID_inner']
    total_mid = defaultdict(int)
    sh_mid = defaultdict(int)
    ch_mid = defaultdict(int)
    for po, no in mid_pairs:
        total_mid[po] += 1
        if no == 'sh': sh_mid[po] += 1
        if no == 'ch': ch_mid[po] += 1
    
    print(f"  {'Onset':<8} {'N_MID':>8} {'sh%':>7} {'ch%':>7} {'ch/sh':>8} {'group':>10}")
    for onset, group in [('p','pf-sh'), ('f','pf-sh'), ('k','kt-ch'), ('t','kt-ch'), 
                          ('ch','ref'), ('sh','ref'), ('d','ref'), ('y','ref')]:
        n = total_mid[onset]
        if n < 3:
            print(f"  {onset:<8} {n:>8} (N too small) [{group}]")
            continue
        sh_p = 100*sh_mid[onset]/n
        ch_p = 100*ch_mid[onset]/n
        ratio = ch_p/sh_p if sh_p > 0 else float('inf')
        print(f"  {onset:<8} {n:>8} {sh_p:>6.1f}% {ch_p:>6.1f}% {ratio:>7.2f}  [{group}]")
    
    # Aggregate p+f vs k+t at each position
    print(f"\n--- Aggregate {{p,f}} vs {{k,t}} by position ---")
    print(f"  {'Position':<15} {'pf_sh%':>8} {'pf_ch%':>8} {'kt_sh%':>8} {'kt_ch%':>8} {'pf_ch/sh':>10} {'kt_ch/sh':>10}")
    for cat in ['LF→pos1', 'pos1→next', 'MID_inner', 'pre-LL→LL']:
        pairs = pos_pairs[cat]
        pf_total = sum(1 for po,no in pairs if po in ('p','f'))
        kt_total = sum(1 for po,no in pairs if po in ('k','t'))
        pf_sh = sum(1 for po,no in pairs if po in ('p','f') and no == 'sh')
        pf_ch = sum(1 for po,no in pairs if po in ('p','f') and no == 'ch')
        kt_sh = sum(1 for po,no in pairs if po in ('k','t') and no == 'sh')
        kt_ch = sum(1 for po,no in pairs if po in ('k','t') and no == 'ch')
        if pf_total == 0 or kt_total == 0: continue
        pf_sh_p = 100*pf_sh/pf_total
        pf_ch_p = 100*pf_ch/pf_total
        kt_sh_p = 100*kt_sh/kt_total
        kt_ch_p = 100*kt_ch/kt_total
        pf_ratio = pf_ch_p/pf_sh_p if pf_sh_p > 0 else float('inf')
        kt_ratio = kt_ch_p/kt_sh_p if kt_sh_p > 0 else float('inf')
        print(f"  {cat:<15} {pf_sh_p:>7.1f}% {pf_ch_p:>7.1f}% {kt_sh_p:>7.1f}% {kt_ch_p:>7.1f}% {pf_ratio:>9.2f} {kt_ratio:>9.2f}")

