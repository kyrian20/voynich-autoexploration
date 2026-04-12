"""
exp_430: A-dialect p-LF → opch MID embedding check (H648)
Cross-dialectal test: does A also show opch enrichment in p-LF MID?
"""

import re
from collections import Counter, defaultdict

ZL3B = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

ONSET_ORDER = ['qok','qot','qo','cth','ch','sh','ok','ot','ol',
               'd','s','y','k','t','l','r','p','f','o']

def get_onset(w):
    for o in ONSET_ORDER:
        if w.startswith(o):
            return o
    return 'other'

def folio_base(folio):
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
    a_folios_base = set()
    for fb, stats in folio_word_stats.items():
        if stats['total'] >= 20:
            rate = stats['edy'] / stats['total']
            if rate >= 0.05:
                b_folios_base.add(fb)
            else:
                a_folios_base.add(fb)

    # Group by folio, separate A and B
    a_folio_groups = defaultdict(list)
    b_folio_groups = defaultdict(list)
    for folio, ln, words in raw_lines:
        fb = folio_base(folio)
        if fb in a_folios_base:
            a_folio_groups[folio].append((ln, words))
        elif fb in b_folios_base:
            b_folio_groups[folio].append((ln, words))

    def get_cont_lines(folio_groups):
        cont = []
        for folio, flines in folio_groups.items():
            lns = [fl[0] for fl in flines]
            min_ln, max_ln = min(lns), max(lns)
            for ln, words in flines:
                if ln != min_ln and ln != max_ln:
                    cont.append((folio, ln, words))
        return cont

    a_cont = get_cont_lines(a_folio_groups)
    b_cont = get_cont_lines(b_folio_groups)
    return a_cont, b_cont, len(a_folios_base), len(b_folios_base)

def analyze_opch(cont_lines, dialect):
    p_lf_lines = [words for folio, ln, words in cont_lines if get_onset(words[0]) == 'p']
    non_p_lines = [words for folio, ln, words in cont_lines if get_onset(words[0]) != 'p']

    def count_mid(lines, prefix):
        total = 0
        count = 0
        vocab = Counter()
        for words in lines:
            mid = words[1:-1]
            total += len(mid)
            for w in mid:
                if w.startswith(prefix):
                    count += 1
                    vocab[w] += 1
        rate = count / total if total > 0 else 0
        return total, count, rate, vocab

    print(f"\n=== {dialect}-dialect: opch MID enrichment in p-LF lines ===")
    print(f"p-LF lines: {len(p_lf_lines)}")
    print(f"non-p-LF lines: {len(non_p_lines)}")

    for prefix in ['opch', 'op']:
        p_mid, p_cnt, p_rate, p_vocab = count_mid(p_lf_lines, prefix)
        np_mid, np_cnt, np_rate, np_vocab = count_mid(non_p_lines, prefix)
        e = p_rate / np_rate if np_rate > 0 else float('inf')
        print(f"\n  prefix='{prefix}':")
        print(f"    p-LF: {p_cnt}/{p_mid}={p_rate:.4f} ({p_rate*100:.2f}%)")
        print(f"    non-p-LF: {np_cnt}/{np_mid}={np_rate:.4f} ({np_rate*100:.2f}%)")
        print(f"    E={e:.2f}× (N_p={p_cnt})")
        if p_vocab:
            print(f"    p-LF {prefix} vocab: {p_vocab.most_common(8)}")

    # Also check o-onset enrichment broadly
    def count_mid_onset(lines, onset):
        total = 0
        count = 0
        for words in lines:
            mid = words[1:-1]
            total += len(mid)
            for w in mid:
                if get_onset(w) == onset:
                    count += 1
        rate = count / total if total > 0 else 0
        return total, count, rate

    p_mid, p_o, p_o_rate = count_mid_onset(p_lf_lines, 'o')
    np_mid, np_o, np_o_rate = count_mid_onset(non_p_lines, 'o')
    e_o = p_o_rate / np_o_rate if np_o_rate > 0 else float('inf')
    print(f"\n  o-onset MID: p-LF={p_o}/{p_mid}={p_o_rate:.4f}, non-p={np_o}/{np_mid}={np_o_rate:.4f}, E={e_o:.2f}×")

def main():
    a_cont, b_cont, n_a_folios, n_b_folios = parse_and_classify()
    print(f"A-dialect: {n_a_folios} folios, {len(a_cont)} cont lines")
    print(f"B-dialect: {n_b_folios} folios, {len(b_cont)} cont lines")

    analyze_opch(b_cont, 'B')
    analyze_opch(a_cont, 'A')

if __name__ == '__main__':
    main()
