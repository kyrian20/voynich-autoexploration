#!/usr/bin/env python3
"""
exp_471: A herbal_a qot-LF Within-Line Formula Analysis

H_new_AL: A herbal_a has qot elevated at LF (7.1% vs 4.9% A-overall, E=1.45×).
This parallels B astro qok-LF (F431: E=1.78×) and B astro qot-LF (exp_469: E=1.94×/N=29).
Exp_469 found B astro qot-LF routing: ch at pos1 E=1.56×(N=7), ot at LL E=3.12×(N=4,dir).

Questions:
1. What is the A herbal_a qot-LF → pos1, pos2, LL routing?
2. Compare to B astro qot-LF routing (exp_469 results)
3. Also: A cosmo qot-LF routing (qot depleted in A cosmo, E~0, but check)
4. Compare A herbal_a qot-LF to A herbal_a d-LF (most common LF class)
5. Cross: does A herbal_a have a qot-LF formula type (parallel to B astro formula types)?
"""
from pathlib import Path as _RepositoryPath

import re
from collections import defaultdict, Counter

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')
ONSETS = ['qok','qot','qo','cth','ckh','cph','ch','sh','ok','ot','ol',
          'sch','skh','sph','d','s','y','k','t','l','r','p','f','o','e','a','n','m']

def get_onset(word):
    for on in ONSETS:
        if word.startswith(on): return on
    return word[0] if word else '?'

def get_section_a(folio):
    num = ''
    for c in folio:
        if c.isdigit(): num += c
        elif num: break
    if not num: return 'other'
    n = int(num)
    if n <= 56: return 'herbal_a'
    elif n <= 72: return 'stars'
    elif n <= 84: return 'herbal_b'
    elif n <= 102: return 'cosmo'
    else: return 'other_a'

def get_section_b(folio):
    num = ''
    for c in folio:
        if c.isdigit(): num += c
        elif num: break
    if not num: return 'other'
    n = int(num)
    if n <= 72: return 'herbal'
    elif n <= 84: return 'astro'
    elif n <= 102: return 'cosmo'
    elif n <= 116: return 'pharma'
    elif n <= 170: return 'bio'
    else: return 'text'

def parse_corpus():
    pattern = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
    folios = defaultdict(list)
    with open(ZL3B, encoding='utf-8') as f:
        for line in f:
            for m in pattern.finditer(line):
                folio = m.group(1).lstrip('+*=&~')
                lc = m.group(3).lstrip('+*=/~&')
                if not lc.lstrip('@').startswith('P'): continue
                text = m.group(4).strip()
                words = [w for w in re.split(r'[-.\s]', text)
                         if re.match(r'^[a-z]+$', w) and len(w) >= 2]
                if words: folios[folio].append(words)
    return folios

def classify_dialects(folios):
    dialect = {}
    for folio, lines in folios.items():
        total = sum(len(ws) for ws in lines)
        if total == 0: continue
        edy = sum(1 for ws in lines for w in ws if w.endswith('edy') or w.endswith('eedy'))
        dialect[folio] = 'B' if edy / total >= 0.05 else 'A'
    return dialect

def compute_lf_routing(lines_by_section, target_section, lf_onset_class, min_len=3):
    """
    For lines in target_section with LF word matching lf_onset_class,
    compute pos1/pos2/LL routing distributions.
    Also compute section-specific baselines for pos1/pos2/LL from ALL lines in section.
    """
    target_lines = []   # (lf_word, words) for lines with target LF onset
    all_lines = []      # all lines in section with min_len

    for folio, line_list in lines_by_section[target_section].items():
        for words in line_list:
            if len(words) < min_len:
                continue
            all_lines.append(words)
            lf_on = get_onset(words[0])
            if lf_on == lf_onset_class:
                target_lines.append((folio, words))

    if not all_lines:
        return None

    # Compute position-specific baselines from all lines
    pos1_baseline = Counter()
    pos2_baseline = Counter()
    ll_baseline   = Counter()
    for words in all_lines:
        if len(words) >= 2:
            pos1_baseline[get_onset(words[1])] += 1
        if len(words) >= 3:
            pos2_baseline[get_onset(words[2])] += 1
        ll_baseline[get_onset(words[-1])] += 1

    n_pos1_base = sum(pos1_baseline.values())
    n_pos2_base = sum(pos2_baseline.values())
    n_ll_base   = sum(ll_baseline.values())

    # Compute routing from target LF lines
    pos1_obs = Counter()
    pos2_obs = Counter()
    ll_obs   = Counter()
    details  = []  # (folio, words) for word-level inspection

    for folio, words in target_lines:
        if len(words) >= 2:
            pos1_obs[get_onset(words[1])] += 1
        if len(words) >= 3:
            pos2_obs[get_onset(words[2])] += 1
        ll_obs[get_onset(words[-1])] += 1
        details.append((folio, words))

    n_target = len(target_lines)
    n_pos1   = sum(pos1_obs.values())
    n_pos2   = sum(pos2_obs.values())
    n_ll     = sum(ll_obs.values())

    return {
        'target_lines': details,
        'n_total': n_target,
        'pos1': (pos1_obs, pos1_baseline, n_pos1_base, n_pos1),
        'pos2': (pos2_obs, pos2_baseline, n_pos2_base, n_pos2),
        'll':   (ll_obs, ll_baseline, n_ll_base, n_ll),
    }

def print_routing(result, label):
    if result is None:
        print(f"  {label}: no data")
        return
    n = result['n_total']
    print(f"\n--- {label} (N={n} lines) ---")
    for pos_name, (obs, base, n_base, n_obs) in [
        ('pos1', result['pos1']),
        ('pos2', result['pos2']),
        ('LL',   result['ll']),
    ]:
        print(f"\n  {pos_name} routing (vs section baseline, N_obs={n_obs}, N_base={n_base}):")
        rows = []
        for onset, cnt in sorted(obs.items(), key=lambda x: -x[1]):
            base_rate = base[onset] / n_base if n_base > 0 else 0
            exp = base_rate * n_obs
            e = cnt / exp if exp > 0 else float('inf')
            tag = ''
            if cnt < 5 and cnt > 0:
                tag = ' (dir)'
            rows.append((onset, cnt, exp, e, tag))
        for onset, cnt, exp, e, tag in sorted(rows, key=lambda x: -x[3])[:8]:
            print(f"    {onset:<8} obs={cnt:>3} exp={exp:>5.2f} E={e:>5.2f}x{tag}")

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)

    # Organize by dialect+section
    a_by_section = defaultdict(lambda: defaultdict(list))
    b_by_section = defaultdict(lambda: defaultdict(list))

    for folio, lines in folios.items():
        d = dialect_map.get(folio)
        if d == 'A':
            sec = get_section_a(folio)
            a_by_section[sec][folio].extend(lines)
        elif d == 'B':
            sec = get_section_b(folio)
            b_by_section[sec][folio].extend(lines)

    # --- Part 1: A herbal_a section LF distribution ---
    print("=== A herbal_a LF onset distribution (all lines ≥3 words) ===")
    lf_counts_ha = Counter()
    total_ha = 0
    for folio, line_list in a_by_section['herbal_a'].items():
        for words in line_list:
            if len(words) >= 3:
                lf_counts_ha[get_onset(words[0])] += 1
                total_ha += 1

    print(f"Total A herbal_a lines (≥3 words): {total_ha}")
    for onset, cnt in sorted(lf_counts_ha.items(), key=lambda x: -x[1])[:15]:
        print(f"  {onset:<8} {cnt:>4} ({cnt/total_ha*100:.1f}%)")

    # A-overall LF distribution (for cross-comparison)
    lf_a_overall = Counter()
    total_a_overall = 0
    for sec in a_by_section:
        for folio, line_list in a_by_section[sec].items():
            for words in line_list:
                if len(words) >= 3:
                    lf_a_overall[get_onset(words[0])] += 1
                    total_a_overall += 1

    print(f"\nA-overall: total={total_a_overall}")

    # --- Part 2: A herbal_a qot-LF routing ---
    print("\n\n=== A herbal_a qot-LF formula analysis ===")
    result_ha_qot = compute_lf_routing(a_by_section, 'herbal_a', 'qot')
    print_routing(result_ha_qot, 'A herbal_a qot-LF')

    # --- Part 3: A herbal_a d-LF routing (comparison baseline) ---
    print("\n\n=== A herbal_a d-LF formula analysis (comparison) ===")
    result_ha_d = compute_lf_routing(a_by_section, 'herbal_a', 'd')
    print_routing(result_ha_d, 'A herbal_a d-LF')

    # --- Part 4: A herbal_a t-LF routing (depleted, but check) ---
    print("\n\n=== A herbal_a t-LF routing ===")
    result_ha_t = compute_lf_routing(a_by_section, 'herbal_a', 't')
    print_routing(result_ha_t, 'A herbal_a t-LF')

    # --- Part 5: A cosmo qot-LF (reference) ---
    print("\n\n=== A cosmo qot-LF routing (reference — qot depleted in cosmo) ===")
    result_cosmo_qot = compute_lf_routing(a_by_section, 'cosmo', 'qot')
    print_routing(result_cosmo_qot, 'A cosmo qot-LF')

    # --- Part 6: Word-level inspection of A herbal_a qot-LF lines ---
    if result_ha_qot:
        print("\n\n=== A herbal_a qot-LF word inventory ===")
        lf_types = Counter()
        pos1_types = Counter()
        ll_types = Counter()
        folios_seen = set()
        for folio, words in result_ha_qot['target_lines']:
            folios_seen.add(folio)
            lf_types[words[0]] += 1
            if len(words) >= 2:
                pos1_types[words[1]] += 1
            ll_types[words[-1]] += 1

        print(f"Unique folios: {len(folios_seen)}: {', '.join(sorted(folios_seen))}")
        print(f"\nLF words (top): " + ', '.join(f"{w}({c})" for w,c in lf_types.most_common(10)))
        print(f"pos1 words (top): " + ', '.join(f"{w}({c})" for w,c in pos1_types.most_common(10)))
        print(f"LL words (top): " + ', '.join(f"{w}({c})" for w,c in ll_types.most_common(10)))

    # --- Part 7: A stars qot-LF (known depleted — confirm) ---
    print("\n\n=== A stars qot-LF (known depleted — verification) ===")
    result_stars_qot = compute_lf_routing(a_by_section, 'stars', 'qot')
    if result_stars_qot:
        print_routing(result_stars_qot, 'A stars qot-LF')
    else:
        print("A stars qot-LF: N=0 (confirmed depleted)")

    # --- Part 8: B astro qot-LF comparison (reproduce exp_469 briefly) ---
    print("\n\n=== B astro qot-LF routing (exp_469 comparison) ===")
    result_bastro_qot = compute_lf_routing(b_by_section, 'astro', 'qot')
    print_routing(result_bastro_qot, 'B astro qot-LF')

if __name__ == '__main__':
    main()
