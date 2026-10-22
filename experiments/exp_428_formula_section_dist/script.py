"""
exp_428: Section distribution of 10 confirmed B formula types (H650)
Check if any formula types are section-concentrated like y→o→ch (pharma+bio, F425).
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

ONSET_ORDER = ['qok','qot','qo','cth','ch','sh','ok','ot','ol',
               'd','s','y','k','t','l','r','p','f','o']

# Confirmed formula types (LF, pos1, pos2)
FORMULA_TYPES = [
    ('qok', 'sh', 'k', 'qok→sh→k'),
    ('d', 'ot', 'ot', 'd→ot→ot'),
    ('l', 'ch', 'qok', 'l→ch→qok'),
    ('d', 'qok', 'ol', 'd→qok→ol'),
    ('y', 'sh', 'ch', 'y→sh→ch'),
    ('y', 'o', 'ch', 'y→o→ch'),
    ('qok', 'ch', 'qo', 'qok→ch→qo'),
    ('d', 'ch', 'y', 'd→ch→y'),
    ('qok', 'ch', 'ol', 'qok→ch→ol'),
    ('p', 'sh', 'ok', 'p→sh→ok'),
]

# Section boundaries (approximate folio number ranges)
# Based on prior findings (F410, F414, F423 etc.)
def get_section(folio):
    """Classify folio into section based on folio number/letter."""
    # Extract folio number
    m = re.match(r'f(\d+)', folio)
    if not m:
        return 'other'
    n = int(m.group(1))
    if n <= 72:
        return 'herbal'
    elif n <= 84:
        return 'astro'
    elif n <= 102:
        return 'bio'
    elif n <= 116:
        return 'pharma'
    else:
        return 'other'

def get_onset(w):
    for o in ONSET_ORDER:
        if w.startswith(o):
            return o
    return 'other'

def folio_base(folio):
    # strip trailing letters (f1r → f1, f1v → f1)
    return re.sub(r'[rv]\d*$', '', folio)

def parse_and_classify():
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0})
    raw_lines = []

    with open(ZL3B, encoding='utf-8') as f:
        for raw in f:
            raw = raw.strip()
            if not raw or raw.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', raw)
            if not m:
                continue
            folio = m.group(1).lstrip('+*=&~')
            ln = int(m.group(2))
            lc = m.group(3).lstrip('+*=/~&')
            if not lc.lstrip('@').startswith('P'):
                continue
            text = re.sub(r'<[^>]+>', '', raw)
            words = [w for w in re.split(r'[-.\s]', text)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words:
                raw_lines.append((folio, ln, words))
                fb = folio_base(folio)
                for w in words:
                    folio_word_stats[fb]['total'] += 1
                    if w.endswith('edy') or w.endswith('eedy'):
                        folio_word_stats[fb]['edy'] += 1

    b_folios_base = set()
    for fb, stats in folio_word_stats.items():
        if stats['total'] >= 20 and stats['edy'] / stats['total'] >= 0.05:
            b_folios_base.add(fb)

    folio_groups = defaultdict(list)
    for folio, ln, words in raw_lines:
        fb = folio_base(folio)
        if fb in b_folios_base:
            folio_groups[folio].append((ln, words))

    cont_lines = []
    for folio, flines in folio_groups.items():
        lns = [fl[0] for fl in flines]
        min_ln, max_ln = min(lns), max(lns)
        for ln, words in flines:
            if ln != min_ln and ln != max_ln:
                cont_lines.append((folio, ln, words))

    return cont_lines

def get_onsets_filtered(words):
    """Get onset sequence with 'other' filtering (consistent with exp_424)."""
    onsets = []
    for w in words:
        o = get_onset(w)
        if o != 'other':
            onsets.append(o)
    return onsets

def main():
    cont_lines = parse_and_classify()
    print(f"B continuation lines: {len(cont_lines)}")

    # Count cont lines by section for baseline
    section_counts = Counter()
    for folio, ln, words in cont_lines:
        sec = get_section(folio)
        section_counts[sec] += 1
    total_cont = sum(section_counts.values())
    print(f"\nSection distribution (baseline B cont lines):")
    for sec in ['herbal', 'astro', 'bio', 'pharma', 'other']:
        n = section_counts[sec]
        print(f"  {sec}: {n} ({n/total_cont*100:.1f}%)")

    # For each formula type, count occurrences by section
    formula_section = defaultdict(lambda: Counter())
    formula_total = Counter()

    for folio, ln, words in cont_lines:
        if len(words) < 3:
            continue
        onsets = get_onsets_filtered(words)
        if len(onsets) < 3:
            continue
        lf, p1, p2 = onsets[0], onsets[1], onsets[2]
        sec = get_section(folio)
        for (ft_lf, ft_p1, ft_p2, ft_name) in FORMULA_TYPES:
            if lf == ft_lf and p1 == ft_p1 and p2 == ft_p2:
                formula_section[ft_name][sec] += 1
                formula_total[ft_name] += 1

    print(f"\n=== Formula type section distribution ===")
    print(f"{'Formula type':20} | N | herbal | astro | bio | pharma | other | Max E(section)")
    print("-"*90)
    for (ft_lf, ft_p1, ft_p2, ft_name) in FORMULA_TYPES:
        n = formula_total[ft_name]
        sec_dist = formula_section[ft_name]
        row = f"{ft_name:20} | {n:2d}"
        max_e = 0
        max_sec = ''
        for sec in ['herbal', 'astro', 'bio', 'pharma', 'other']:
            cnt = sec_dist[sec]
            baseline_frac = section_counts[sec] / total_cont if total_cont > 0 else 0
            obs_frac = cnt / n if n > 0 else 0
            e = obs_frac / baseline_frac if baseline_frac > 0 else 0
            row += f" | {cnt:2d}({e:.1f}×)"
            if e > max_e and cnt > 0:
                max_e = e
                max_sec = sec
        row += f" | {max_sec}({max_e:.1f}×)"
        print(row)

    # Detailed section comparison for notable cases
    print(f"\n=== Detailed: l→ch→qok (expected pharma-concentrated) ===")
    name = 'l→ch→qok'
    for sec in ['herbal', 'astro', 'bio', 'pharma', 'other']:
        n_formula = formula_section[name][sec]
        n_baseline = section_counts[sec]
        frac_f = n_formula / formula_total[name] if formula_total[name] > 0 else 0
        frac_b = n_baseline / total_cont
        e = frac_f / frac_b if frac_b > 0 else 0
        print(f"  {sec}: {n_formula}/{formula_total[name]} = {frac_f:.3f} vs baseline {frac_b:.3f}, E={e:.2f}×")

    print(f"\n=== Detailed: y→o→ch (expected pharma+bio, no herbal) ===")
    name = 'y→o→ch'
    for sec in ['herbal', 'astro', 'bio', 'pharma', 'other']:
        n_formula = formula_section[name][sec]
        n_baseline = section_counts[sec]
        frac_f = n_formula / formula_total[name] if formula_total[name] > 0 else 0
        frac_b = n_baseline / total_cont
        e = frac_f / frac_b if frac_b > 0 else 0
        print(f"  {sec}: {n_formula}/{formula_total[name]} = {frac_f:.3f} vs baseline {frac_b:.3f}, E={e:.2f}×")

if __name__ == '__main__':
    main()
