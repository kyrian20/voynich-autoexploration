"""
exp_431: daiin positional distribution by dialect and section (H541 + H546)
H541: Is A-dialect daiin LL-enriched (vs B-dialect)?
H546: Is B-dialect daiin LF enrichment uniform across sections?
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
    if not m: return 'other'
    n = int(m.group(1))
    if n <= 72: return 'herbal'
    elif n <= 84: return 'astro'
    elif n <= 102: return 'bio'
    elif n <= 116: return 'pharma'
    return 'other'

def parse_all_lines():
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0})
    raw_lines = []
    with open(ZL3B, encoding='utf-8') as f:
        for raw in f:
            raw = raw.strip()
            if not raw or raw.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', raw)
            if not m: continue
            folio = m.group(1).lstrip('+*=&~')
            ln = int(m.group(2))
            lc = m.group(3).lstrip('+*=/~&')
            if not lc.lstrip('@').startswith('P'): continue
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

    dialect = {}
    for fb, stats in folio_word_stats.items():
        if stats['total'] >= 20:
            rate = stats['edy'] / stats['total']
            dialect[fb] = 'B' if rate >= 0.05 else 'A'

    # Group by folio, get cont lines
    folio_groups = defaultdict(list)
    for folio, ln, words in raw_lines:
        fb = folio_base(folio)
        if fb in dialect:
            folio_groups[(folio, dialect[fb])].append((ln, words))

    cont_by_dialect = {'A': [], 'B': []}
    for (folio, d), flines in folio_groups.items():
        lns = [fl[0] for fl in flines]
        min_ln, max_ln = min(lns), max(lns)
        for ln, words in flines:
            if ln != min_ln and ln != max_ln:
                cont_by_dialect[d].append((folio, ln, words))

    return cont_by_dialect

def analyze_word_position(lines, word='daiin'):
    """Compute LF/MID/LL/total distribution for a specific word."""
    lf = mid = ll = total = 0
    for folio, ln, words in lines:
        for i, w in enumerate(words):
            if w == word:
                total += 1
                if i == 0: lf += 1
                elif i == len(words)-1: ll += 1
                else: mid += 1
    return {'total': total, 'LF': lf, 'MID': mid, 'LL': ll}

def baseline_position(lines):
    """Compute LF/MID/LL baseline token counts."""
    lf = mid = ll = 0
    for folio, ln, words in lines:
        lf += 1
        ll += 1
        mid += max(0, len(words) - 2)
    return {'LF': lf, 'MID': mid, 'LL': ll}

def main():
    cont = parse_all_lines()

    for d in ['A', 'B']:
        print(f"\n{'='*60}")
        print(f"DIALECT {d}: {len(cont[d])} cont lines")
        print(f"{'='*60}")

        # Overall daiin position
        pos = analyze_word_position(cont[d], 'daiin')
        base = baseline_position(cont[d])
        print(f"\ndaiin overall: total={pos['total']}")
        for position in ['LF', 'MID', 'LL']:
            n = pos[position]
            base_n = base[position]
            base_frac = base_n / (base['LF'] + base['MID'] + base['LL'])
            obs_frac = n / pos['total'] if pos['total'] > 0 else 0
            e = obs_frac / base_frac if base_frac > 0 else 0
            print(f"  {position}: {n}/{pos['total']}={obs_frac:.3f} vs baseline {base_frac:.3f}, E={e:.2f}×")

        # B-dialect: section breakdown
        if d == 'B':
            print(f"\n--- B-dialect daiin LF/MID/LL by section ---")
            for sec in ['herbal', 'astro', 'bio', 'pharma']:
                sec_lines = [(f,l,w) for f,l,w in cont[d] if get_section(f) == sec]
                pos_sec = analyze_word_position(sec_lines, 'daiin')
                base_sec = baseline_position(sec_lines)
                total_tokens = base_sec['LF'] + base_sec['MID'] + base_sec['LL']
                print(f"\n  {sec} (N={len(sec_lines)} lines, {total_tokens} tokens):")
                print(f"  daiin total: {pos_sec['total']}")
                for position in ['LF', 'MID', 'LL']:
                    n = pos_sec[position]
                    base_n = base_sec[position]
                    base_frac = base_n / total_tokens if total_tokens > 0 else 0
                    obs_frac = n / pos_sec['total'] if pos_sec['total'] > 0 else 0
                    e = obs_frac / base_frac if base_frac > 0 else 0
                    print(f"    {position}: {n}/{pos_sec['total']}={obs_frac:.3f} vs baseline {base_frac:.3f}, E={e:.2f}×")

        # Also check: d-onset words at LL in each dialect
        print(f"\n--- {d}-dialect d-onset LL enrichment ---")
        d_ll = d_total = 0
        total_ll = 0
        for folio, ln, words in cont[d]:
            total_ll += 1  # each line has one LL
            if words and get_onset(words[-1]) == 'd':
                d_ll += 1
            for w in words:
                if get_onset(w) == 'd':
                    d_total += 1
        total_tokens = sum(len(words) for folio, ln, words in cont[d])
        d_global_rate = d_total / total_tokens if total_tokens > 0 else 0
        d_ll_rate = d_ll / total_ll if total_ll > 0 else 0
        print(f"  d-onset total tokens: {d_total}/{total_tokens}={d_global_rate:.3f}")
        print(f"  d-onset at LL: {d_ll}/{total_ll}={d_ll_rate:.3f}")
        print(f"  d-onset LL enrichment: E={d_ll_rate/d_global_rate:.2f}×")

        # Also: daiin at LL vs baseline d-onset words
        daiin_ll = sum(1 for f,l,w in cont[d] if w and w[-1] == 'daiin')
        daiin_total = sum(1 for f,l,words in cont[d] for w in words if w == 'daiin')
        daiin_ll_correct = sum(1 for f,l,words in cont[d] if words[-1] == 'daiin')
        print(f"  daiin total: {daiin_total}")
        print(f"  daiin at LL: {daiin_ll_correct}")
        if daiin_total > 0:
            print(f"  daiin LL fraction: {daiin_ll_correct/daiin_total:.3f}")

if __name__ == '__main__':
    main()
