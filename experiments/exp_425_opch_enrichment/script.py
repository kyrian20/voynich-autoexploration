"""
exp_425: B 'opch'-compound enrichment in p-LF vs non-p-LF MID positions
H640: Is 'opchedy'/'opchdy' enrichment specific to p-formula lines?
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

ONSET_ORDER = ['qok','qot','qo','cth','ch','sh','ok','ot','ol',
               'd','s','y','k','t','l','r','p','f','o']

def get_onset(w):
    for o in ONSET_ORDER:
        if w.startswith(o):
            return o
    return 'other'

def is_b_folio(folio):
    return folio  # will filter by edy rate at corpus level

def parse_lines():
    """Parse ZL3B into (folio, locus, words) triples."""
    lines = []
    with open(ZL3B, encoding='utf-8') as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', raw)
            if not m:
                continue
            folio, ln_str, lc = m.group(1), m.group(2), m.group(3)
            lc = lc.lstrip('+*=/~&')
            if not lc.lstrip('@').startswith('P'):
                continue
            text = re.sub(r'<[^>]+>', '', raw)
            words = [w for w in re.split(r'[-.\s]', text)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words:
                lines.append((folio, int(ln_str), lc, words))
    return lines

def classify_dialect(lines):
    """Classify each folio as A or B by edy+eedy rate."""
    folio_counts = {}
    for folio, ln, lc, words in lines:
        if folio not in folio_counts:
            folio_counts[folio] = {'total': 0, 'edy': 0}
        for w in words:
            folio_counts[folio]['total'] += 1
            if w.endswith('edy') or w.endswith('eedy'):
                folio_counts[folio]['edy'] += 1
    b_folios = set()
    for folio, counts in folio_counts.items():
        if counts['total'] >= 20:
            rate = counts['edy'] / counts['total']
            if rate >= 0.05:
                b_folios.add(folio)
    return b_folios

def get_continuation_lines(lines, b_folios):
    """Get B-dialect continuation lines (not first/last line of folio)."""
    # Group by folio
    folio_lines = {}
    for folio, ln, lc, words in lines:
        if folio not in b_folios:
            continue
        if folio not in folio_lines:
            folio_lines[folio] = []
        folio_lines[folio].append((ln, lc, words))

    cont_lines = []
    for folio, flines in folio_lines.items():
        lns = [fl[0] for fl in flines]
        min_ln, max_ln = min(lns), max(lns)
        for ln, lc, words in flines:
            if ln != min_ln and ln != max_ln:
                cont_lines.append((folio, ln, words))
    return cont_lines

def get_mid_words(words):
    """Return MID words (not LF=words[0], not LL=words[-1])."""
    if len(words) <= 2:
        return []
    return words[1:-1]

def is_opch(word):
    """Check if word starts with 'opch'."""
    return word.startswith('opch')

def main():
    raw_lines = parse_lines()
    b_folios = classify_dialect(raw_lines)
    print(f"B-dialect folios: {len(b_folios)}")

    cont_lines = get_continuation_lines(raw_lines, b_folios)
    print(f"B continuation lines: {len(cont_lines)}")

    # Separate into p-LF and non-p-LF
    p_lf_lines = []
    non_p_lf_lines = []
    for folio, ln, words in cont_lines:
        lf_onset = get_onset(words[0])
        if lf_onset == 'p':
            p_lf_lines.append(words)
        else:
            non_p_lf_lines.append(words)

    print(f"\nB p-LF lines: {len(p_lf_lines)}")
    print(f"B non-p-LF lines: {len(non_p_lf_lines)}")

    # Count opch words in MID positions for each group
    def count_mid_opch(line_set):
        total_mid = 0
        opch_mid = 0
        opch_words = Counter()
        for words in line_set:
            mid = get_mid_words(words)
            total_mid += len(mid)
            for w in mid:
                if is_opch(w):
                    opch_mid += 1
                    opch_words[w] += 1
        return total_mid, opch_mid, opch_words

    p_total_mid, p_opch_mid, p_opch_words = count_mid_opch(p_lf_lines)
    np_total_mid, np_opch_mid, np_opch_words = count_mid_opch(non_p_lf_lines)

    p_rate = p_opch_mid / p_total_mid if p_total_mid > 0 else 0
    np_rate = np_opch_mid / np_total_mid if np_total_mid > 0 else 0

    print("\n=== opch-prefix words at MID positions ===")
    print(f"\np-LF lines:")
    print(f"  MID tokens: {p_total_mid}")
    print(f"  opch-MID count: {p_opch_mid}")
    print(f"  opch-MID rate: {p_opch_mid}/{p_total_mid} = {p_rate:.4f} ({p_rate*100:.2f}%)")
    print(f"  opch word distribution: {p_opch_words.most_common(10)}")

    print(f"\nnon-p-LF lines:")
    print(f"  MID tokens: {np_total_mid}")
    print(f"  opch-MID count: {np_opch_mid}")
    print(f"  opch-MID rate: {np_opch_mid}/{np_total_mid} = {np_rate:.4f} ({np_rate*100:.2f}%)")
    print(f"  opch word distribution: {np_opch_words.most_common(10)}")

    if np_rate > 0:
        enrichment = p_rate / np_rate
        print(f"\nEnrichment (p-LF vs non-p-LF): {enrichment:.2f}×")
    else:
        print("\nEnrichment: undefined (np_rate=0)")

    # Also check: are opch words generally o-onset class?
    print("\n=== opch vocabulary confirmation ===")
    all_opch = p_opch_words + np_opch_words
    print(f"All opch words (p-LF + non-p-LF): {all_opch.most_common(15)}")

    # Also check: how common is o-onset class in MID for p-LF vs non-p-LF?
    def count_mid_o(line_set):
        total_mid = 0
        o_mid = 0
        for words in line_set:
            mid = get_mid_words(words)
            total_mid += len(mid)
            for w in mid:
                if get_onset(w) == 'o':
                    o_mid += 1
        return total_mid, o_mid

    p_mid_total, p_o_mid = count_mid_o(p_lf_lines)
    np_mid_total, np_o_mid = count_mid_o(non_p_lf_lines)

    p_o_rate = p_o_mid / p_mid_total if p_mid_total > 0 else 0
    np_o_rate = np_o_mid / np_mid_total if np_mid_total > 0 else 0

    print(f"\n=== o-onset class MID enrichment ===")
    print(f"p-LF: o-onset MID = {p_o_mid}/{p_mid_total} = {p_o_rate:.4f} ({p_o_rate*100:.2f}%)")
    print(f"non-p-LF: o-onset MID = {np_o_mid}/{np_mid_total} = {np_o_rate:.4f} ({np_o_rate*100:.2f}%)")
    if np_o_rate > 0:
        o_enrichment = p_o_rate / np_o_rate
        print(f"o-onset MID enrichment (p-LF vs non-p-LF): {o_enrichment:.2f}×")

    # Also: show all MID tokens to get context
    print("\n=== p-LF MID onset distribution ===")
    p_mid_onsets = Counter()
    np_mid_onsets = Counter()
    for words in p_lf_lines:
        for w in get_mid_words(words):
            p_mid_onsets[get_onset(w)] += 1
    for words in non_p_lf_lines:
        for w in get_mid_words(words):
            np_mid_onsets[get_onset(w)] += 1

    # Compute enrichment for each onset
    p_total = sum(p_mid_onsets.values())
    np_total = sum(np_mid_onsets.values())
    print(f"p-LF total MID tokens: {p_total}")
    print(f"non-p-LF total MID tokens: {np_total}")
    print("\nOnset | p-LF rate | non-p-LF rate | E")
    print("-"*50)
    for onset in ['o', 'ch', 'sh', 'qok', 'qo', 'qot', 'd', 's', 'y', 'other']:
        p_r = p_mid_onsets.get(onset, 0) / p_total if p_total else 0
        np_r = np_mid_onsets.get(onset, 0) / np_total if np_total else 0
        e = p_r / np_r if np_r > 0 else float('inf')
        print(f"{onset:<8} | {p_r:.4f} ({p_mid_onsets.get(onset,0):4d}) | "
              f"{np_r:.4f} ({np_mid_onsets.get(onset,0):6d}) | {e:.2f}×")

if __name__ == '__main__':
    main()
