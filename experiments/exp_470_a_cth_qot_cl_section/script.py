#!/usr/bin/env python3
"""
exp_470: A cth→qot CL Section-Specificity and Body-Conditional Driver

H_new_AI: A cth at LL has two elevated cross-line targets: sh(1.93×/N=12, exp_465)
AND qot(2.07×/N=7, exp_465). This experiment tests:
1. Section specificity: is cth→qot CL concentrated in herbal_a (like cth→sh)?
2. Body-class driver: which cth+body class predicts qot at next LF?
3. Word-level verification: diversity check (folio spread, word pairs)
4. Also: complete A cth LL profile (all CL targets) for context
"""

import re
from collections import defaultdict

CORPUS_PATH = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

ONSET_PRIORITY = [
    'cth','ckh','cph',        # cth-class (before ch/c)
    'qok','qot','qo',         # q-bench
    'ok','ot','ol',           # o+gallows
    'sh','ch',                # sh/ch digraphs
    'sch','skh','sph',        # s+gallows
    's','d','y','l','r',
    'p','k','t','f',
    'n','m',
    'o','e','a','i',
]

BODY_CLASSES = {
    'aiin': lambda w: 'aiin' in w,
    'edy':  lambda w: w.endswith('edy') or w.endswith('eedy'),
    'she':  lambda w: 'she' in w,
    'ol':   lambda w: w.endswith('ol') or w.endswith('al'),
    'iin':  lambda w: w.endswith('iin') and 'aiin' not in w,
}

def get_onset(w):
    for o in ONSET_PRIORITY:
        if w.startswith(o):
            return o
    return w[0] if w else '?'

def get_body(w):
    for name, fn in BODY_CLASSES.items():
        if fn(w):
            return name
    return 'other'

def get_section_a(folio):
    num = ''
    for c in folio:
        if c.isdigit():
            num += c
        elif num:
            break
    if not num:
        return 'other'
    n = int(num)
    if n <= 56:   return 'herbal_a'
    elif n <= 72: return 'stars'
    elif n <= 84: return 'herbal_b'
    elif n <= 102: return 'cosmo'
    else:         return 'other_a'

def parse_corpus():
    lines_by_folio = defaultdict(list)
    pat = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
    with open(CORPUS_PATH) as f:
        for raw in f:
            raw = raw.strip()
            for m in pat.finditer(raw):
                folio_raw, page_num, locus, text = m.groups()
                folio = folio_raw.lstrip('+*=&~')
                lc = locus.lstrip('+*=/~&')
                if not lc.lstrip('@').startswith('P'):
                    continue
                words = [w for w in re.split(r'[-.\s]', text)
                         if re.match(r'^[a-z]+$', w) and len(w) >= 2]
                if not words:
                    continue
                lines_by_folio[folio].append((lc, words))
    return lines_by_folio

def classify_dialects(lines_by_folio):
    a_folios = set()
    b_folios = set()
    for folio, lines in lines_by_folio.items():
        all_words = [w for _, wds in lines for w in wds]
        total = len(all_words)
        if total == 0:
            continue
        edy_count = sum(1 for w in all_words
                        if w.endswith('edy') or w.endswith('eedy'))
        rate = edy_count / total
        if rate >= 0.05:
            b_folios.add(folio)
        else:
            a_folios.add(folio)
    return a_folios, b_folios

def build_cl_pairs(lines_by_folio, target_folios):
    """Build (folio, ll_word, lf_word) cross-line pairs within continuation lines."""
    pairs = []
    for folio in sorted(target_folios):
        folio_lines = lines_by_folio.get(folio, [])
        for i in range(len(folio_lines) - 1):
            lc_cur, words_cur = folio_lines[i]
            lc_nxt, words_nxt = folio_lines[i + 1]
            if not words_cur or not words_nxt:
                continue
            ll_word = words_cur[-1]
            lf_word = words_nxt[0]
            pairs.append((folio, ll_word, lf_word))
    return pairs

def main():
    lines_by_folio = parse_corpus()
    a_folios, b_folios = classify_dialects(lines_by_folio)

    # Build A-dialect CL pairs
    a_pairs = build_cl_pairs(lines_by_folio, a_folios)

    # --- Part 1: Complete A cth-LL profile ---
    # All CL pairs where LL onset = cth-class
    cth_class = {'cth', 'ckh', 'cph'}
    cth_ll_pairs = [(f, ll, lf) for f, ll, lf in a_pairs
                    if get_onset(ll) in cth_class]

    print(f"A-dialect total CL pairs: {len(a_pairs)}")
    print(f"A-dialect cth-LL pairs: {len(cth_ll_pairs)}")

    # LF onset distribution for cth-LL pairs
    lf_onset_counts = defaultdict(int)
    for f, ll, lf in cth_ll_pairs:
        lf_onset_counts[get_onset(lf)] += 1

    # Overall A-dialect LF onset distribution (baseline)
    a_lf_counts = defaultdict(int)
    for f, ll, lf in a_pairs:
        a_lf_counts[get_onset(lf)] += 1
    a_total = len(a_pairs)

    print("\n=== A cth-LL → next LF onset profile ===")
    print(f"{'onset':<8} {'obs':>5} {'exp':>7} {'E':>6}")
    cth_total = len(cth_ll_pairs)
    for onset, cnt in sorted(lf_onset_counts.items(), key=lambda x: -x[1]):
        base_rate = a_lf_counts[onset] / a_total
        exp = base_rate * cth_total
        e = cnt / exp if exp > 0 else float('inf')
        print(f"{onset:<8} {cnt:>5} {exp:>7.2f} {e:>6.2f}x")

    # --- Part 2: cth→qot CL section specificity ---
    cth_qot_pairs = [(f, ll, lf) for f, ll, lf in cth_ll_pairs
                     if get_onset(lf) == 'qot']
    cth_sh_pairs  = [(f, ll, lf) for f, ll, lf in cth_ll_pairs
                     if get_onset(lf) == 'sh']

    print(f"\n=== cth→qot CL section breakdown (N={len(cth_qot_pairs)}) ===")
    # Section-specific baseline for qot-LF
    sec_cth_total = defaultdict(int)
    sec_cth_qot   = defaultdict(int)
    sec_a_total   = defaultdict(int)
    sec_a_qot     = defaultdict(int)

    for f, ll, lf in cth_ll_pairs:
        sec = get_section_a(f)
        sec_cth_total[sec] += 1
        if get_onset(lf) == 'qot':
            sec_cth_qot[sec] += 1

    for f, ll, lf in a_pairs:
        sec = get_section_a(f)
        sec_a_total[sec] += 1
        if get_onset(lf) == 'qot':
            sec_a_qot[sec] += 1

    print(f"{'section':<12} {'cth_N':>6} {'cth→qot':>8} {'a_qot%':>8} {'E':>6}")
    for sec in ['herbal_a', 'cosmo', 'stars', 'herbal_b', 'other_a']:
        n_cth = sec_cth_total[sec]
        n_cth_qot = sec_cth_qot[sec]
        if sec_a_total[sec] > 0:
            base = sec_a_qot[sec] / sec_a_total[sec]
        else:
            base = 0
        exp = base * n_cth
        e = n_cth_qot / exp if exp > 0 else float('inf') if n_cth_qot > 0 else 0
        tag = ' (dir)' if 0 < n_cth_qot < 5 else ''
        print(f"{sec:<12} {n_cth:>6} {n_cth_qot:>8} {base*100:>7.1f}% {e:>6.2f}x{tag}")

    print(f"\n=== cth→qot CL word inventory ===")
    for f, ll, lf in cth_qot_pairs:
        sec = get_section_a(f)
        print(f"  {f:<8} {sec:<12} LL={ll:<12} LF={lf}")

    # --- Part 3: cth→qot body-class breakdown ---
    print(f"\n=== cth→qot CL body-class driver ===")
    body_total = defaultdict(int)
    body_qot   = defaultdict(int)

    for f, ll, lf in cth_ll_pairs:
        b = get_body(ll)
        body_total[b] += 1
        if get_onset(lf) == 'qot':
            body_qot[b] += 1

    # Baseline: body distribution among all A cth-LL → all LF
    # E = (body_qot/body_total) / (total_qot/cth_total)
    overall_qot_rate = lf_onset_counts.get('qot', 0) / cth_total

    print(f"Overall A cth-LL → qot rate: {overall_qot_rate*100:.1f}% (N={lf_onset_counts.get('qot',0)}/{cth_total})")
    print(f"{'body':<8} {'total':>6} {'→qot':>6} {'rate':>7} {'E':>6}")
    for b in sorted(body_total.keys()):
        n = body_total[b]
        nq = body_qot[b]
        rate = nq / n if n > 0 else 0
        e = rate / overall_qot_rate if overall_qot_rate > 0 else 0
        tag = ' (dir)' if 0 < nq < 5 else ''
        print(f"{b:<8} {n:>6} {nq:>6} {rate*100:>6.1f}% {e:>6.2f}x{tag}")

    # --- Part 4: Compare cth→sh vs cth→qot by section ---
    print(f"\n=== cth→sh CL section breakdown (N={len(cth_sh_pairs)}) ===")
    sec_cth_sh  = defaultdict(int)
    sec_a_sh    = defaultdict(int)
    for f, ll, lf in cth_ll_pairs:
        if get_onset(lf) == 'sh':
            sec_cth_sh[get_section_a(f)] += 1
    for f, ll, lf in a_pairs:
        if get_onset(lf) == 'sh':
            sec_a_sh[get_section_a(f)] += 1

    print(f"{'section':<12} {'cth_N':>6} {'→sh':>5} {'a_sh%':>7} {'E':>6}")
    for sec in ['herbal_a', 'cosmo', 'stars', 'herbal_b', 'other_a']:
        n_cth = sec_cth_total[sec]
        n_sh  = sec_cth_sh[sec]
        base = sec_a_sh[sec] / sec_a_total[sec] if sec_a_total[sec] > 0 else 0
        exp = base * n_cth
        e = n_sh / exp if exp > 0 else float('inf') if n_sh > 0 else 0
        tag = ' (dir)' if 0 < n_sh < 5 else ''
        print(f"{sec:<12} {n_cth:>6} {n_sh:>5} {base*100:>6.1f}% {e:>6.2f}x{tag}")

    # --- Part 5: Folio and word diversity for cth→qot ---
    print(f"\n=== cth→qot diversity check ===")
    folios = set(f for f, ll, lf in cth_qot_pairs)
    pairs_set = set((ll, lf) for f, ll, lf in cth_qot_pairs)
    print(f"N={len(cth_qot_pairs)}, unique folios={len(folios)}, unique word pairs={len(pairs_set)}")
    print(f"Folios: {', '.join(sorted(folios))}")
    print(f"Unique ll words: {set(ll for f,ll,lf in cth_qot_pairs)}")
    print(f"Unique lf words: {set(lf for f,ll,lf in cth_qot_pairs)}")

if __name__ == '__main__':
    main()
