"""
exp_426: B t MID→ot adjacency — compound construction or independent pairing?
H613b: When t-onset word appears in MID followed by ot-onset word, are specific
       tokens involved (compound) or distributed (independent sequential pairing)?
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
    """Parse ZL3B, classify folios, return B cont lines."""
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

    # Group by folio, find continuation lines
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

    return cont_lines, b_folios

def main():
    cont_lines, b_folios = parse_and_classify()
    print(f"B-dialect folios: {len(b_folios)}")
    print(f"B continuation lines: {len(cont_lines)}")

    # Collect all MID word pairs (adjacent words in MID positions)
    # MID = words[1:-1] (not LF, not LL)
    # For each consecutive pair in MID, record (w_i, w_i+1)
    t_ot_pairs = []   # (t-word, ot-word) pairs
    ot_after_t = Counter()  # ot-onset words following t-onset in MID
    t_before_ot = Counter()  # t-onset words preceding ot-onset in MID

    # Also baseline: all ot-onset words in MID
    all_ot_mid = Counter()
    all_t_mid = Counter()
    total_mid_pairs = 0
    t_ot_count = 0

    for folio, ln, words in cont_lines:
        mid = words[1:-1]  # MID words
        if len(mid) < 2:
            continue
        for i in range(len(mid)):
            w = mid[i]
            onset = get_onset(w)
            if onset == 'ot':
                all_ot_mid[w] += 1
            if onset == 't':
                all_t_mid[w] += 1
        for i in range(len(mid) - 1):
            w1, w2 = mid[i], mid[i+1]
            total_mid_pairs += 1
            o1, o2 = get_onset(w1), get_onset(w2)
            if o1 == 't' and o2 == 'ot':
                t_ot_count += 1
                t_ot_pairs.append((w1, w2, folio, ln))
                ot_after_t[w2] += 1
                t_before_ot[w1] += 1

    print(f"\n=== t→ot adjacency in B MID ===")
    print(f"Total MID consecutive pairs: {total_mid_pairs}")
    print(f"t→ot MID pairs: {t_ot_count}")

    # Baseline rates
    all_mid_tokens = sum(all_ot_mid.values()) + sum(all_t_mid.values())
    # More precisely: count all MID tokens
    total_mid_tokens = 0
    ot_mid_count = 0
    for folio, ln, words in cont_lines:
        mid = words[1:-1]
        total_mid_tokens += len(mid)
        for w in mid:
            if get_onset(w) == 'ot':
                ot_mid_count += 1

    t_mid_count = sum(all_t_mid.values())
    print(f"Total MID tokens: {total_mid_tokens}")
    print(f"ot-onset MID tokens: {ot_mid_count} ({ot_mid_count/total_mid_tokens:.3f})")
    print(f"t-onset MID tokens: {t_mid_count} ({t_mid_count/total_mid_tokens:.3f})")

    # Expected t→ot pairs under independence
    # P(w2=ot | w1=t) vs P(ot globally)
    t_mid_pairs = sum(1 for folio, ln, words in cont_lines
                      for i in range(len(words[1:-1])-1)
                      if get_onset(words[1:-1][i]) == 't')
    expected_ot_after_t = t_mid_pairs * (ot_mid_count / total_mid_tokens) if total_mid_tokens > 0 else 0
    print(f"\nt-onset leading MID pairs: {t_mid_pairs}")
    print(f"Expected t→ot pairs (independence): {expected_ot_after_t:.1f}")
    print(f"Observed t→ot pairs: {t_ot_count}")
    if expected_ot_after_t > 0:
        print(f"Enrichment E: {t_ot_count/expected_ot_after_t:.2f}×")

    print(f"\n=== ot-onset words following t in MID (top) ===")
    for w, n in ot_after_t.most_common(15):
        print(f"  {w}: {n}")

    print(f"\n=== t-onset words preceding ot in MID (top) ===")
    for w, n in t_before_ot.most_common(15):
        print(f"  {w}: {n}")

    print(f"\n=== ot-onset vocabulary in all B MID positions (top) ===")
    for w, n in all_ot_mid.most_common(15):
        print(f"  {w}: {n}")

    print(f"\n=== t-onset vocabulary in all B MID positions (top) ===")
    for w, n in all_t_mid.most_common(15):
        print(f"  {w}: {n}")

    print(f"\n=== All t→ot MID pairs ({len(t_ot_pairs)} total) ===")
    pair_counts = Counter((w1, w2) for w1, w2, f, l in t_ot_pairs)
    for (w1, w2), n in pair_counts.most_common(20):
        print(f"  {w1} → {w2}: {n}")

    # Check type diversity: how many unique t-words and ot-words appear in pairs?
    unique_t = len(set(w1 for w1, w2, f, l in t_ot_pairs))
    unique_ot = len(set(w2 for w1, w2, f, l in t_ot_pairs))
    print(f"\nUnique t-words in pairs: {unique_t}/{len(all_t_mid)} (total t-MID types)")
    print(f"Unique ot-words in pairs: {unique_ot}/{len(all_ot_mid)} (total ot-MID types)")

    # Top pair is same word vs different?
    same_pair = sum(1 for w1, w2, f, l in t_ot_pairs if w1[1:] == w2 or w1 == w2)
    print(f"Same-word pairs (t→ot where body matches): {same_pair}/{len(t_ot_pairs)}")

if __name__ == '__main__':
    main()
