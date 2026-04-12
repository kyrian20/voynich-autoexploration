"""
exp_406: A y-Chain Section Specificity (H614)

For A-dialect, compute y-chain length distribution separately for each manuscript section.
F395 showed both A length-4 y-chains are in herbal (f19) and bio (f67r2).
H614: Are y-chains (length>=3) concentrated in herbal/bio sections?

Section identification:
- Herbal: folios f1-f66 (approximately)
- Pharma: folios f99-f116
- Bio/Stars: various (f67-f86)
- Cosmo: f86v5 (cosmological rosette) + other
- Text/Recipes: f103-f116 (or other)

We'll use the folio numbering to classify sections.
"""

import os, re
from collections import Counter, defaultdict

DATA_PATH = os.path.expanduser('~/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt')

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

def folio_base(folio):
    return re.sub(r'[rv]\d*$', '', folio)

def folio_num(folio_str):
    """Extract numeric part of folio name (handles 'f19', 'f67r2', etc.)"""
    m = re.search(r'(\d+)', folio_str)
    return int(m.group(1)) if m else 999

def get_section(folio_str):
    """Classify folio into section based on number"""
    n = folio_num(folio_str)
    if n <= 66:
        return 'herbal'
    elif n <= 86:
        return 'bio_stars'
    elif n <= 98:
            return 'cosmo'
    elif n <= 116:
        return 'pharma'
    else:
        return 'text'

# Pass 1: folio dialect
folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0})
with open(DATA_PATH, 'r', encoding='utf-8') as fh:
    for line in fh:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
        if not m:
            continue
        folio = m.group(1).lstrip('+*=&~')
        fb = folio_base(folio)
        lc = m.group(3).lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'):
            continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        for w in words:
            folio_word_stats[fb]['total'] += 1
            if w.endswith('edy') or w.endswith('eedy'):
                folio_word_stats[fb]['edy'] += 1

folio_dialect = {}
for fb, stats in folio_word_stats.items():
    t = stats['total']
    folio_dialect[fb] = 'B' if t > 0 and stats['edy'] / t >= 0.05 else 'A'

# Pass 2: collect A words by folio and line, tracking y-runs
folio_lines = defaultdict(list)  # fb -> list of (ln, words)
with open(DATA_PATH, 'r', encoding='utf-8') as fh:
    for line in fh:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
        if not m:
            continue
        folio = m.group(1).lstrip('+*=&~')
        ln = int(m.group(2))
        lc = m.group(3).lstrip('+*=/~&')
        fb = folio_base(folio)
        if folio_dialect.get(fb, 'A') != 'A':
            continue
        if not lc.lstrip('@').startswith('P'):
            continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if not words:
            continue
        folio_lines[fb].append((ln, words))

# For each A folio, compute y-chains in continuation lines
# Track runs of consecutive y-onset words
section_stats = defaultdict(lambda: {'total_words': 0, 'y_words': 0, 'runs_1': 0, 'runs_2': 0, 'runs_3': 0, 'runs_4plus': 0, 'folios': set()})

def get_y_runs(word_list):
    """Get all y-onset runs from a list of words"""
    runs = []
    current_run = 0
    for w in word_list:
        if get_onset(w) == 'y':
            current_run += 1
        else:
            if current_run > 0:
                runs.append(current_run)
                current_run = 0
    if current_run > 0:
        runs.append(current_run)
    return runs

all_runs = []  # (run_length, section, folio, context)

for fb, line_list in folio_lines.items():
    section = get_section(fb)
    lns = [l[0] for l in line_list]
    min_ln, max_ln = min(lns), max(lns)

    # Collect all continuation words in sequence (respecting line order)
    line_list_sorted = sorted(line_list, key=lambda x: x[0])

    for ln, words in line_list_sorted:
        # Count words for section stats
        is_cont = (ln != min_ln and ln != max_ln)
        for w in words:
            if is_cont:
                section_stats[section]['total_words'] += 1
                section_stats[section]['folios'].add(fb)
                if get_onset(w) == 'y':
                    section_stats[section]['y_words'] += 1

        # Find y-runs within this line
        if is_cont:
            runs = get_y_runs(words)
            for r in runs:
                if r == 1:
                    section_stats[section]['runs_1'] += 1
                elif r == 2:
                    section_stats[section]['runs_2'] += 1
                elif r == 3:
                    section_stats[section]['runs_3'] += 1
                elif r >= 4:
                    section_stats[section]['runs_4plus'] += 1
                all_runs.append((r, section, fb))

# Summary
print("=== A Dialect y-Chain Section Analysis ===\n")
print(f"{'Section':<15} {'N_words':>8}  {'y%':>6}  {'runs_1':>7}  {'runs_2':>7}  {'runs_3':>7}  {'runs_4+':>7}  {'run3+ per 100y':>15}")
total_runs_3plus_all = 0
total_y_all = 0
for sect in ['herbal', 'bio_stars', 'cosmo', 'pharma', 'text']:
    s = section_stats[sect]
    n = s['total_words']
    y = s['y_words']
    r1 = s['runs_1']
    r2 = s['runs_2']
    r3 = s['runs_3']
    r4 = s['runs_4plus']
    total_y_all += y
    total_runs_3plus_all += r3 + r4
    y_pct = 100 * y / n if n > 0 else 0
    runs_per_100y = 100 * (r3 + r4) / y if y > 0 else 0
    print(f"  {sect:<13} {n:>8}  {y_pct:>5.1f}%  {r1:>7}  {r2:>7}  {r3:>7}  {r4:>7}  {runs_per_100y:>15.2f}")

print(f"\n  {'TOTAL':<13} {sum(s['total_words'] for s in section_stats.values()):>8}  "
      f"{100*total_y_all/sum(s['total_words'] for s in section_stats.values()):>5.1f}%  "
      f"  ...  "
      f"{sum(s['runs_3'] for s in section_stats.values()):>7}  "
      f"{sum(s['runs_4plus'] for s in section_stats.values()):>7}  "
      f"{100*total_runs_3plus_all/total_y_all if total_y_all > 0 else 0:>15.2f}")

# Print individual length-3+ runs with section and folio
print(f"\n=== All A y-chains length >= 3 (continuation lines) ===")
long_runs = [(r, sect, fb) for r, sect, fb in all_runs if r >= 3]
print(f"Total length>=3 y-chains: {len(long_runs)}")
for r, sect, fb in sorted(long_runs, key=lambda x: -x[0]):
    print(f"  length={r}  section={sect}  folio={fb}")

# Statistical comparison: is length-3+ y-chain rate elevated in herbal/bio vs pharma/text?
print(f"\n=== Section comparison: length-3+ y-chains per 100 y-words ===")
for sect in ['herbal', 'bio_stars']:
    s = section_stats[sect]
    r3p = s['runs_3'] + s['runs_4plus']
    y = s['y_words']
    rate = 100 * r3p / y if y > 0 else 0
    print(f"  {sect}: {r3p}/{y} (rate={rate:.2f} per 100 y-words)")

for sect in ['pharma', 'text', 'cosmo']:
    s = section_stats[sect]
    r3p = s['runs_3'] + s['runs_4plus']
    y = s['y_words']
    rate = 100 * r3p / y if y > 0 else 0
    print(f"  {sect}: {r3p}/{y} (rate={rate:.2f} per 100 y-words)")

# Also compute folio count per section
print(f"\nFolios per section:")
for sect in ['herbal', 'bio_stars', 'cosmo', 'pharma', 'text']:
    print(f"  {sect}: {len(section_stats[sect]['folios'])} folios")
