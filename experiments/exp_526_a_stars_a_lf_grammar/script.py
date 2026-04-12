"""
exp_526: A stars a-LF grammar (H_new_ER)

A stars (57-72, A-dialect) has a-LF as 11% of LF (3rd rank after d=18.4%, ch=16.9%).
a-LF has no confirmed within-line grammar rules anywhere.
In A herbal_a, a-LF is rare (~1.4%), making A stars the best location to study a-LF grammar.

This experiment:
1. Full pos1/pos2/pen positional grammar for a-LF in A stars
2. Cross-section comparison: a-LF grammar in A herbal_a and B herbal (F470 context)
3. A stars full LF class positional survey (d, ch, a, o, sh, ok, ot — all N_elig≥5 classes)
4. Also: investigate Q011 — examine what exp_466 found for t-LF (if we can determine discrepancy source)
"""

import re
from collections import defaultdict, Counter

CORPUS = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

ONSET_PRIORITY = [
    'qok','qot','qo','cth','ckh','cph','ch','sh','ok','ot','ol','sch','skh','sph',
    'd','s','y','k','t','l','r','p','f','o','e','a','n','m'
]

def get_onset(word):
    for onset in ONSET_PRIORITY:
        if word.startswith(onset):
            return onset
    return 'other'

def folio_num(folio):
    m = re.search(r'f(\d+)', folio)
    return int(m.group(1)) if m else None

def parse_corpus(path):
    folio_lines = defaultdict(list)
    pat = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
    with open(path, encoding='utf-8') as f:
        raw = f.read()
    for m in pat.finditer(raw):
        folio_raw, _, locus_raw, text = m.groups()
        folio = folio_raw.lstrip('+*=&~')
        lc = locus_raw.lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'):
            continue
        words = [w for w in re.split(r'[-.\s]', text)
                 if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if not words:
            continue
        n = folio_num(folio)
        if n is None:
            continue
        folio_lines[n].append(words)
    return folio_lines

def is_b_dialect(lines):
    words = [w for ln in lines for w in ln]
    if not words:
        return False
    edy = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
    return edy / len(words) >= 0.05

folio_lines = parse_corpus(CORPUS)

# Section definitions
a_stars = {n: ls for n, ls in folio_lines.items() if 57 <= n <= 72 and not is_b_dialect(ls)}
a_herbal_a = {n: ls for n, ls in folio_lines.items() if n <= 56 and not is_b_dialect(ls)}
b_herbal = {n: ls for n, ls in folio_lines.items() if n <= 72 and is_b_dialect(ls)}

a_stars_lines = [ln for ls in a_stars.values() for ln in ls]
a_ha_lines = [ln for ls in a_herbal_a.values() for ln in ls]
b_herbal_lines = [ln for ls in b_herbal.values() for ln in ls]

print(f"A stars: {len(a_stars)} folios, {len(a_stars_lines)} lines")
print(f"A herbal_a: {len(a_herbal_a)} folios, {len(a_ha_lines)} lines")
print(f"B herbal: {len(b_herbal)} folios, {len(b_herbal_lines)} lines")

def flag(obs, E):
    if obs >= 10 and E >= 1.5:
        return 'CONF'
    elif obs >= 5 and E >= 2.0:
        return 'dir'
    elif obs >= 3 and E >= 2.5:
        return '(dir)'
    elif E >= 1.0:
        return f'{E:.2f}×'
    else:
        return f'DEPL {E:.2f}×'

def compute_baselines(lines):
    """pos1: len>=2; pos2/pen: len>=3"""
    pos1 = Counter(get_onset(ln[0]) for ln in lines if len(ln) >= 2)
    pos2 = Counter(get_onset(ln[1]) for ln in lines if len(ln) >= 3)
    pen = Counter(get_onset(ln[-2]) for ln in lines if len(ln) >= 3)
    return {
        'pos1': (pos1, sum(pos1.values())),
        'pos2': (pos2, sum(pos2.values())),
        'pen': (pen, sum(pen.values())),
    }

def positional_profile(lines, lf_class, baselines, section_label, top_n=12):
    lf_lines = [ln for ln in lines if get_onset(ln[-1]) == lf_class]
    N_lf = len(lf_lines)
    print(f"\n{'='*60}")
    print(f"  {section_label} {lf_class}-LF (N_lines={N_lf})")
    print(f"{'='*60}")

    if N_lf == 0:
        print("  (no lines)")
        return

    for pos_name, pos_idx, min_len in [('pos1', 0, 2), ('pos2', 1, 3), ('pen', -2, 3)]:
        elig = [ln for ln in lf_lines if len(ln) >= min_len]
        counts = Counter(get_onset(ln[pos_idx]) for ln in elig)
        base_counts, base_total = baselines[pos_name]
        N_elig = len(elig)
        print(f"\n  {pos_name} (N_elig={N_elig}):")
        if N_elig == 0:
            print("    (no eligible lines)")
            continue

        # Chain-relevant classes to always show
        chain = {'d','qot','ch','o','sh','ok','ot','y','cth','s','k','t','a', lf_class}
        rows = []
        for cls, obs in counts.most_common(top_n):
            exp = (base_counts.get(cls, 0) / base_total) * N_elig if base_total > 0 else 0
            E = obs / exp if exp > 0 else float('inf')
            rows.append((cls, obs, exp, E))
        shown = {cls for cls, _, _, _ in rows}
        for cls in chain - shown:
            obs = counts.get(cls, 0)
            exp = (base_counts.get(cls, 0) / base_total) * N_elig if base_total > 0 else 0
            E = obs / exp if exp > 0 else (float('inf') if obs > 0 else 0.0)
            rows.append((cls, obs, exp, E))
        rows.sort(key=lambda x: -x[3])

        print(f"  {'cls':8} {'obs':>5} {'exp':>6} {'E':>7}  flag")
        seen = set()
        for cls, obs, exp, E in rows:
            if cls in seen:
                continue
            seen.add(cls)
            E_str = f'{E:.2f}' if E != float('inf') else 'inf'
            print(f"  {cls:8} {obs:>5} {exp:>6.1f} {E_str:>7}x  {flag(obs, E)}")

# ─────────────────────────────────────────────────────────────────────────────
# PART 1: A stars a-LF full positional profile (H_new_ER)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 1: A STARS a-LF POSITIONAL GRAMMAR (H_new_ER)")
print("="*70)

a_stars_baselines = compute_baselines(a_stars_lines)

# Show A stars LF distribution for context
lf_dist = Counter(get_onset(ln[-1]) for ln in a_stars_lines)
total = len(a_stars_lines)
print(f"\nA stars LF distribution (N={total}):")
for cls, cnt in lf_dist.most_common(12):
    print(f"  {cls}: {cnt} ({100*cnt/total:.1f}%)")

positional_profile(a_stars_lines, 'a', a_stars_baselines, 'A stars')

# ─────────────────────────────────────────────────────────────────────────────
# PART 2: Cross-section a-LF comparison — A herbal_a and B herbal
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 2: CROSS-SECTION a-LF COMPARISON")
print("="*70)

a_ha_baselines = compute_baselines(a_ha_lines)
b_herbal_baselines = compute_baselines(b_herbal_lines)

positional_profile(a_ha_lines, 'a', a_ha_baselines, 'A herbal_a')
positional_profile(b_herbal_lines, 'a', b_herbal_baselines, 'B herbal')

# ─────────────────────────────────────────────────────────────────────────────
# PART 3: A stars full grammar survey — all LF classes with N_elig>=5
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 3: A STARS FULL LF CLASS GRAMMAR SURVEY")
print("="*70)

lf_classes_to_survey = [cls for cls, cnt in lf_dist.most_common() if cnt >= 5]
print(f"\nClasses with N_lf>=5: {lf_classes_to_survey}")

for cls in lf_classes_to_survey:
    positional_profile(a_stars_lines, cls, a_stars_baselines, 'A stars')

# ─────────────────────────────────────────────────────────────────────────────
# PART 4: Q011 investigation — t-LF in A stars detailed
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 4: Q011 — t-LF IN A STARS (DETAILED)")
print("="*70)

# Show every t-LF line in A stars for inspection
t_lf_lines = [ln for ln in a_stars_lines if get_onset(ln[-1]) == 't']
print(f"\nAll t-LF lines in A stars (N={len(t_lf_lines)}):")
for i, ln in enumerate(t_lf_lines):
    print(f"  {i+1}: {' '.join(ln)}")

# Show full LF onset breakdown including t
print(f"\nA stars t-LF raw count: {lf_dist.get('t', 0)} / {total} = {100*lf_dist.get('t',0)/total:.2f}%")
a_ha_lf_dist = Counter(get_onset(ln[-1]) for ln in a_ha_lines)
print(f"A herbal_a t-LF raw count: {a_ha_lf_dist.get('t', 0)} / {len(a_ha_lines)} = {100*a_ha_lf_dist.get('t',0)/len(a_ha_lines):.2f}%")
E_t = (lf_dist.get('t',0)/total) / (a_ha_lf_dist.get('t',0)/len(a_ha_lines))
print(f"E(t-LF A stars vs A herbal_a) = {E_t:.3f}×")

# What would N=15 require?
print(f"\nFor F446's N=15 t-LF in A stars:")
print(f"  Current A stars: {total} lines, {lf_dist.get('t',0)} t-LF lines")
print(f"  F446 claimed N=15: would require {15/total*100:.1f}% t-LF rate")
print(f"  Possible explanation: exp_466 used A stars = 57-84? or 57-102?")

# Test different A stars definitions for t-LF
for lo, hi in [(57,72),(57,84),(57,102),(57,116)]:
    section = {n: ls for n, ls in folio_lines.items() if lo <= n <= hi and not is_b_dialect(ls)}
    sec_lines = [ln for ls in section.values() for ln in ls]
    t_n = sum(1 for ln in sec_lines if get_onset(ln[-1]) == 't')
    print(f"  A stars {lo}-{hi}: {len(sec_lines)} lines, t-LF N={t_n} ({100*t_n/len(sec_lines):.1f}%)" if sec_lines else f"  A stars {lo}-{hi}: empty")
