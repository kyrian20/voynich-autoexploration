"""
exp_429: Astro-section qok-LF grammar — is qok-LF more common in astro,
         or only the specific formula-type routing?
H651
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

ONSET_ORDER = ['qok','qot','qo','cth','ch','sh','ok','ot','ol',
               'd','s','y','k','t','l','r','p','f','o']

def get_onset(w):
    for o in ONSET_ORDER:
        if w.startswith(o):
            return o
    return 'other'

def folio_base(folio):
    return re.sub(r'[rv]\d*$', '', folio)

def get_section(folio):
    m = re.match(r'f(\d+)', folio)
    if not m:
        return 'other'
    n = int(m.group(1))
    if n <= 72: return 'herbal'
    elif n <= 84: return 'astro'
    elif n <= 102: return 'bio'
    elif n <= 116: return 'pharma'
    return 'other'

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

def main():
    cont_lines = parse_and_classify()
    print(f"B continuation lines: {len(cont_lines)}")

    sections = ['herbal', 'astro', 'bio', 'pharma']

    # Section totals
    sec_total = Counter()
    for folio, ln, words in cont_lines:
        sec = get_section(folio)
        sec_total[sec] += 1

    # qok-LF rate by section
    sec_qok_lf = Counter()
    for folio, ln, words in cont_lines:
        sec = get_section(folio)
        if get_onset(words[0]) == 'qok':
            sec_qok_lf[sec] += 1

    print("\n=== qok-LF rate by section ===")
    total_qok = sum(sec_qok_lf.values())
    print(f"Total qok-LF lines: {total_qok}")
    for sec in sections:
        n = sec_qok_lf[sec]
        total = sec_total[sec]
        rate = n / total if total > 0 else 0
        baseline = sec_total[sec] / sum(sec_total.values())
        # overall qok-LF rate
        global_rate = total_qok / sum(sec_total.values())
        e = rate / global_rate if global_rate > 0 else 0
        print(f"  {sec}: qok-LF={n}/{total}={rate:.3f} vs global={global_rate:.3f}, E={e:.2f}×")

    # For qok-LF lines: pos1 distribution by section
    print("\n=== qok-LF pos1 distribution by section ===")
    sec_pos1 = defaultdict(Counter)
    for folio, ln, words in cont_lines:
        if len(words) < 2:
            continue
        if get_onset(words[0]) != 'qok':
            continue
        sec = get_section(folio)
        pos1 = get_onset(words[1])
        sec_pos1[sec][pos1] += 1

    # Key pos1 classes: sh, ch, qok
    key_onsets = ['sh', 'ch', 'qok', 'qo', 'qot', 'd', 'o', 'other']
    print(f"{'Onset':8}", end='')
    for sec in sections:
        total = sum(sec_pos1[sec].values())
        print(f" | {sec}(N={total})", end='')
    print()
    print("-"*80)
    for onset in key_onsets:
        print(f"{onset:8}", end='')
        for sec in sections:
            total = sum(sec_pos1[sec].values())
            n = sec_pos1[sec].get(onset, 0)
            rate = n / total if total > 0 else 0
            print(f" | {n:3d}({rate:.3f})", end='')
        print()

    # Compute E for key pos1 onsets by section vs global qok-LF pos1 baseline
    all_pos1 = Counter()
    for sec in sections:
        for onset, cnt in sec_pos1[sec].items():
            all_pos1[onset] += cnt
    total_all = sum(all_pos1.values())

    print("\n=== E(pos1 | qok-LF, section) vs global qok-LF pos1 baseline ===")
    for onset in ['sh', 'ch', 'k', 'qo', 'qot']:
        global_rate = all_pos1.get(onset, 0) / total_all if total_all > 0 else 0
        print(f"\n  {onset} (global={global_rate:.3f}):")
        for sec in sections:
            n = sec_pos1[sec].get(onset, 0)
            total = sum(sec_pos1[sec].values())
            rate = n / total if total > 0 else 0
            e = rate / global_rate if global_rate > 0 else float('inf')
            print(f"    {sec}: E={e:.2f}×(N={n})")

    # Also: which folios contribute to astro qok-LF formula types?
    print("\n=== Astro folios with qok-LF lines ===")
    astro_qok_folios = Counter()
    for folio, ln, words in cont_lines:
        if get_section(folio) == 'astro' and get_onset(words[0]) == 'qok':
            astro_qok_folios[folio] += 1
    for folio, n in sorted(astro_qok_folios.items()):
        print(f"  {folio}: {n} qok-LF lines")

if __name__ == '__main__':
    main()
