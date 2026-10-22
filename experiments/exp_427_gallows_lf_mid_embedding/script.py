"""
exp_427: Gallows-class generalization of LF-onset MID embedding
H647: Does f/t/k-LF show gallows-embedded compound enrichment at MID,
      analogous to p-LF→opch enrichment (F427)?
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
                for w in words:
                    folio_word_stats[folio]['total'] += 1
                    if w.endswith('edy') or w.endswith('eedy'):
                        folio_word_stats[folio]['edy'] += 1

    b_folios = set()
    for folio, stats in folio_word_stats.items():
        if stats['total'] >= 20 and stats['edy'] / stats['total'] >= 0.05:
            b_folios.add(folio)

    folio_groups = defaultdict(list)
    for folio, ln, words in raw_lines:
        if folio in b_folios:
            folio_groups[folio].append((ln, words))

    cont_lines = []
    for folio, flines in folio_groups.items():
        lns = [fl[0] for fl in flines]
        min_ln, max_ln = min(lns), max(lns)
        for ln, words in flines:
            if ln != min_ln and ln != max_ln:
                cont_lines.append((folio, ln, words))

    return cont_lines

def analyze_gallows_embedding(cont_lines, lf_gallows, embed_prefix):
    """
    For lines where LF class = lf_gallows, check if MID words starting
    with embed_prefix are enriched vs non-lf_gallows lines.
    """
    lf_lines = []
    non_lf_lines = []
    for folio, ln, words in cont_lines:
        if get_onset(words[0]) == lf_gallows:
            lf_lines.append(words)
        else:
            non_lf_lines.append(words)

    def count_mid_prefix(line_set, prefix):
        total_mid = 0
        prefix_count = 0
        vocab = Counter()
        for words in line_set:
            mid = words[1:-1]
            total_mid += len(mid)
            for w in mid:
                if w.startswith(prefix):
                    prefix_count += 1
                    vocab[w] += 1
        rate = prefix_count / total_mid if total_mid > 0 else 0
        return total_mid, prefix_count, rate, vocab

    lf_mid, lf_cnt, lf_rate, lf_vocab = count_mid_prefix(lf_lines, embed_prefix)
    nlf_mid, nlf_cnt, nlf_rate, nlf_vocab = count_mid_prefix(non_lf_lines, embed_prefix)
    e = lf_rate / nlf_rate if nlf_rate > 0 else float('inf')

    return {
        'lf_gallows': lf_gallows,
        'embed_prefix': embed_prefix,
        'n_lf_lines': len(lf_lines),
        'n_nlf_lines': len(non_lf_lines),
        'lf_mid': lf_mid,
        'lf_cnt': lf_cnt,
        'lf_rate': lf_rate,
        'nlf_mid': nlf_mid,
        'nlf_cnt': nlf_cnt,
        'nlf_rate': nlf_rate,
        'E': e,
        'lf_vocab': lf_vocab,
    }

def main():
    cont_lines = parse_and_classify()
    print(f"B continuation lines: {len(cont_lines)}")

    # Define gallows → embedded prefix mapping
    # p → opch (p in o-onset compound via 'op' prefix + ch)
    # f → ofch (f in o-onset compound)
    # t → tch?? or ot prefix?? Let's think:
    #   p-gallows embedded as 'op' = o + p; then ch body: 'opch'
    #   f-gallows: 'of' = o + f; then ch body: 'ofch'
    #   k-gallows: 'ok' is a onset class; 'okch'?
    #   t-gallows: 'ot' is an onset class; 'otch'?
    # Also check: what are general gallows-embedded prefixes?
    # Look at all words starting with 'o' + gallows letter
    # p: op, f: of, k: ok (but ok is also an onset class!), t: ot (also onset class!)

    gallows_tests = [
        ('p', 'opch'),   # confirmed in F427
        ('f', 'ofch'),   # hypothesis H647
        ('k', 'okch'),   # k-embedded ch compound
        ('t', 'otch'),   # t-embedded ch compound (distinct from ot-onset class)
        # Also check broader embedding: 'op' prefix (any f body), 'of' prefix
        ('p', 'op'),     # any o+p compound
        ('f', 'of'),     # any o+f compound
        ('k', 'ok'),     # any o+k compound (but ok is onset class)
        ('t', 'ot'),     # any o+t compound (but ot is onset class)
    ]

    print("\n=== Gallows LF embedding analysis ===")
    print(f"{'LF':4} | {'prefix':8} | {'N_lf_lines':10} | {'LF cnt':7} | {'LF rate':9} | {'NLF rate':9} | {'E':7} | top vocab")
    print("-"*90)
    for lf_gall, prefix in gallows_tests:
        result = analyze_gallows_embedding(cont_lines, lf_gall, prefix)
        top_v = result['lf_vocab'].most_common(3)
        top_str = ', '.join(f"{w}({n})" for w, n in top_v)
        print(f"{lf_gall:4} | {prefix:8} | {result['n_lf_lines']:10d} | {result['lf_cnt']:7d} | "
              f"{result['lf_rate']:9.4f} | {result['nlf_rate']:9.4f} | {result['E']:7.2f}× | {top_str}")

    # Detailed breakdown for top results
    print("\n=== Detailed: p→opch (baseline from F427) ===")
    r = analyze_gallows_embedding(cont_lines, 'p', 'opch')
    print(f"p-LF lines: {r['n_lf_lines']}, opch MID: {r['lf_cnt']}/{r['lf_mid']}={r['lf_rate']:.4f}")
    print(f"non-p-LF: {r['nlf_cnt']}/{r['nlf_mid']}={r['nlf_rate']:.4f}")
    print(f"E={r['E']:.2f}×")

    print("\n=== Detailed: f→ofch ===")
    r = analyze_gallows_embedding(cont_lines, 'f', 'ofch')
    print(f"f-LF lines: {r['n_lf_lines']}, ofch MID: {r['lf_cnt']}/{r['lf_mid']}={r['lf_rate']:.4f}")
    print(f"non-f-LF: {r['nlf_cnt']}/{r['nlf_mid']}={r['nlf_rate']:.4f}")
    print(f"E={r['E']:.2f}×")
    print(f"ofch vocab in f-LF MID: {r['lf_vocab'].most_common(10)}")

    # Also find all words with gallows-embedded structure in general
    print("\n=== Survey: 'ofch' words in full B corpus ===")
    all_ofch = Counter()
    all_opch_base = Counter()
    for folio, ln, words in cont_lines:
        for w in words:
            if w.startswith('ofch'):
                all_ofch[w] += 1
            if w.startswith('opch'):
                all_opch_base[w] += 1
    print(f"All 'ofch' words: {all_ofch.most_common(10)} (total={sum(all_ofch.values())})")
    print(f"All 'opch' words (baseline): {all_opch_base.most_common(5)} (total={sum(all_opch_base.values())})")

if __name__ == '__main__':
    main()
