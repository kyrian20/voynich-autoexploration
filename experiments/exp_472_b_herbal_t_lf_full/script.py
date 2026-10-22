#!/usr/bin/env python3
"""
exp_472: B herbal t-LF and B cosmo t-LF Full Formula Analysis (H_new_AM)

t-LF is elevated in B herbal (E=2.34×/N=38, F447) and B cosmo (E=2.23×/N=16, F447).
exp_468 corrected a baseline error and found:
  - B herbal t-LF pos1: qok=2.22×(N=6,dir), ch=0.80× (baseline)
  - B herbal t-LF LL: o=1.97×(N=5), ol=1.94×(N=4)
But exp_468 was inline (no script). This experiment does the full formal analysis.

Questions:
1. B herbal t-LF: complete pos1/pos2/LL routing with B herbal section-specific baselines
2. B cosmo t-LF: same analysis — does B cosmo t-LF routing match B herbal t-LF?
3. A cosmo t-LF (F447: E=1.63×/N=30): routing comparison
4. Also check B herbal y-LF (N=55) for comparison (the second elevated LF class in B herbal)
5. Word-level inventory for B herbal and B cosmo t-LF lines
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

def analyze_lf_class(section_lines, lf_onset, min_len=3, label=''):
    """
    section_lines: dict{folio: [words_list, ...]}
    Returns routing analysis for lines with LF=lf_onset.
    """
    all_lines = []
    target_lines = []

    for folio, line_list in section_lines.items():
        for words in line_list:
            if len(words) < min_len:
                continue
            all_lines.append(words)
            if get_onset(words[0]) == lf_onset:
                target_lines.append((folio, words))

    n_all = len(all_lines)
    n_target = len(target_lines)

    # Baseline distributions
    pos1_base = Counter(get_onset(ws[1]) for ws in all_lines if len(ws) >= 2)
    pos2_base = Counter(get_onset(ws[2]) for ws in all_lines if len(ws) >= 3)
    ll_base   = Counter(get_onset(ws[-1]) for ws in all_lines)
    n_p1b = sum(pos1_base.values())
    n_p2b = sum(pos2_base.values())
    n_llb = sum(ll_base.values())

    # Target distributions
    pos1_obs = Counter()
    pos2_obs = Counter()
    ll_obs   = Counter()
    for folio, words in target_lines:
        if len(words) >= 2:
            pos1_obs[get_onset(words[1])] += 1
        if len(words) >= 3:
            pos2_obs[get_onset(words[2])] += 1
        ll_obs[get_onset(words[-1])] += 1

    n_p1o = sum(pos1_obs.values())
    n_p2o = sum(pos2_obs.values())
    n_llo = sum(ll_obs.values())

    print(f"\n=== {label} (N={n_target}, all_section={n_all}) ===")
    for pos_name, obs, base, n_obs, n_base in [
        ('pos1', pos1_obs, pos1_base, n_p1o, n_p1b),
        ('pos2', pos2_obs, pos2_base, n_p2o, n_p2b),
        ('LL',   ll_obs,  ll_base,  n_llo, n_llb),
    ]:
        print(f"\n  {pos_name} (N_obs={n_obs}, N_base={n_base}):")
        rows = []
        for onset, cnt in obs.items():
            base_rate = base[onset] / n_base if n_base > 0 else 0
            exp = base_rate * n_obs
            e = cnt / exp if exp > 0 else float('inf')
            rows.append((onset, cnt, exp, e))
        for onset, cnt, exp, e in sorted(rows, key=lambda x: -x[3])[:8]:
            tag = ' (dir)' if 0 < cnt < 5 else ''
            print(f"    {onset:<8} obs={cnt:>3} exp={exp:>5.2f} E={e:>5.2f}x{tag}")

    # Word inventory
    lf_types = Counter(ws[0] for f, ws in target_lines)
    pos1_types = Counter(ws[1] for f, ws in target_lines if len(ws) >= 2)
    ll_types = Counter(ws[-1] for f, ws in target_lines)
    folios_seen = sorted(set(f for f, ws in target_lines))
    print(f"\n  Folios ({len(folios_seen)}): {', '.join(folios_seen[:10])}{'...' if len(folios_seen)>10 else ''}")
    print(f"  LF top: " + ', '.join(f"{w}({c})" for w,c in lf_types.most_common(6)))
    print(f"  pos1 top: " + ', '.join(f"{w}({c})" for w,c in pos1_types.most_common(6)))
    print(f"  LL top: " + ', '.join(f"{w}({c})" for w,c in ll_types.most_common(6)))

    return target_lines

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)

    # Organize
    a_by_section = defaultdict(lambda: defaultdict(list))
    b_by_section = defaultdict(lambda: defaultdict(list))
    for folio, lines in folios.items():
        d = dialect_map.get(folio)
        if d == 'A':
            a_by_section[get_section_a(folio)][folio].extend(lines)
        elif d == 'B':
            b_by_section[get_section_b(folio)][folio].extend(lines)

    # Section LF distributions for context
    print("=== Section LF distributions ===")
    for dialect_name, by_sec, sections in [
        ('B', b_by_section, ['herbal','cosmo','astro','pharma']),
        ('A', a_by_section, ['herbal_a','cosmo']),
    ]:
        for sec in sections:
            total = 0
            t_count = 0
            for folio, line_list in by_sec[sec].items():
                for ws in line_list:
                    if len(ws) >= 3:
                        total += 1
                        if get_onset(ws[0]) == 't':
                            t_count += 1
            rate = t_count/total*100 if total > 0 else 0
            print(f"  {dialect_name} {sec}: N={total}, t-LF={t_count}({rate:.1f}%)")

    # --- Main analyses ---
    analyze_lf_class(b_by_section['herbal'], 't', label='B herbal t-LF')
    analyze_lf_class(b_by_section['cosmo'],  't', label='B cosmo t-LF')
    analyze_lf_class(a_by_section['cosmo'],  't', label='A cosmo t-LF')
    analyze_lf_class(b_by_section['herbal'], 'y', label='B herbal y-LF (comparison)')

    # Extra: B herbal t-LF vs cosmo t-LF comparison summary
    print("\n\n=== B herbal vs B cosmo t-LF routing comparison ===")
    print("(See section outputs above — does pos1 qok elevation appear in both?)")

    # B herbal overall t-LF rate vs other B sections for context
    print("\n=== B-dialect t-LF rate by section ===")
    b_overall_total = 0
    b_overall_t = 0
    for sec in b_by_section:
        sec_total = 0
        sec_t = 0
        for folio, line_list in b_by_section[sec].items():
            for ws in line_list:
                if len(ws) >= 3:
                    sec_total += 1
                    if get_onset(ws[0]) == 't':
                        sec_t += 1
        b_overall_total += sec_total
        b_overall_t += sec_t
        if sec_total > 0:
            print(f"  B {sec}: {sec_t}/{sec_total} = {sec_t/sec_total*100:.1f}%")
    if b_overall_total > 0:
        print(f"  B overall: {b_overall_t}/{b_overall_total} = {b_overall_t/b_overall_total*100:.1f}%")

if __name__ == '__main__':
    main()
