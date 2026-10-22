"""
exp_442: A-qok ch-Midfix Connection to Bracket Grammar (H_new_A)

Q: Are A-dialect ch-midfix qok forms (qokchy/qokchol/qokchor) concentrated
   in bracket lines (lines where pos1 and LL share an onset class)?

Method:
- A-dialect continuation lines
- Identify bracket lines: pos1 and LL have same onset class (d sh-bracket, y y-bracket, k ch-bracket)
- Compare qok-onset MID word distribution in bracket vs non-bracket lines
- Specifically: ch-midfix qok forms (qokchy/qokchol/qokchor) rate in bracket vs non-bracket MID
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

ONSETS = ['qok', 'qot', 'qo', 'cth', 'ch', 'sh', 'ok', 'ot', 'ol',
          'd', 's', 'y', 'k', 't', 'l', 'r', 'p', 'f', 'o']

CH_MIDFIX_QOK = {'qokchy', 'qokchol', 'qokchor', 'qokcho', 'qokchedy', 'qokchey', 'qokchd', 'qokchod'}

def get_onset(word):
    for on in ONSETS:
        if word.startswith(on):
            return on
    return 'other'

def parse_corpus():
    pattern = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
    folios = defaultdict(list)
    with open(ZL3B, encoding='utf-8') as f:
        for line in f:
            for m in pattern.finditer(line):
                folio = m.group(1).lstrip('+*=&~')
                lc = m.group(3).lstrip('+*=/~&')
                if not lc.lstrip('@').startswith('P'):
                    continue
                text = m.group(4).strip()
                words = [w for w in re.split(r'[-.\s]', text)
                         if re.match(r'^[a-z]+$', w) and len(w) >= 2]
                if words:
                    folios[folio].append(words)
    return folios

def classify_dialects(folios):
    dialect = {}
    for folio, lines in folios.items():
        total = sum(len(ws) for ws in lines)
        if total == 0: continue
        edy = sum(1 for ws in lines for w in ws
                  if w.endswith('edy') or w.endswith('eedy'))
        dialect[folio] = 'B' if edy / total >= 0.05 else 'A'
    return dialect

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)
    
    # A-dialect continuation lines (not folio-first or folio-last)
    bracket_mid_qok = Counter()   # qok words in MID of bracket lines
    nonbracket_mid_qok = Counter() # qok words in MID of non-bracket lines
    
    bracket_count = 0
    nonbracket_count = 0
    
    # Track by bracket type
    bracket_types = Counter()  # (pos1_onset, ll_onset) -> line count
    
    for folio, lines in folios.items():
        if dialect_map.get(folio) != 'A':
            continue
        n_lines = len(lines)
        for idx, ws in enumerate(lines):
            n = len(ws)
            if n < 3:
                continue
            # Skip folio-first (idx=0) and folio-last (idx=n_lines-1)
            if idx == 0 or idx == n_lines - 1:
                continue
            
            lf = ws[0]
            pos1 = ws[1]
            ll = ws[-1]
            mid_words = ws[2:-1]  # MID = from pos2 to pre-LL
            
            on_pos1 = get_onset(pos1)
            on_ll = get_onset(ll)
            
            # Is this a bracket line? (same onset at pos1 and LL)
            is_bracket = (on_pos1 == on_ll) and on_pos1 != 'other'
            
            if is_bracket:
                bracket_types[(on_pos1, on_ll)] += 1
                bracket_count += 1
                for w in mid_words:
                    if get_onset(w) == 'qok':
                        bracket_mid_qok[w] += 1
            else:
                nonbracket_count += 1
                for w in mid_words:
                    if get_onset(w) == 'qok':
                        nonbracket_mid_qok[w] += 1
    
    print(f"A-dialect cont lines: bracket={bracket_count}, non-bracket={nonbracket_count}")
    print(f"Bracket types (top): {bracket_types.most_common(8)}")
    
    b_total_qok = sum(bracket_mid_qok.values())
    nb_total_qok = sum(nonbracket_mid_qok.values())
    
    print(f"\nBracket MID: {b_total_qok} qok tokens across {bracket_count} lines")
    print(f"Non-bracket MID: {nb_total_qok} qok tokens across {nonbracket_count} lines")
    
    # ch-midfix qok rate
    b_ch_mf = sum(bracket_mid_qok.get(w, 0) for w in CH_MIDFIX_QOK)
    nb_ch_mf = sum(nonbracket_mid_qok.get(w, 0) for w in CH_MIDFIX_QOK)
    
    # Rate per line (normalize by line count to avoid MID length confound)
    b_qok_per_line = b_total_qok / bracket_count if bracket_count else 0
    nb_qok_per_line = nb_total_qok / nonbracket_count if nonbracket_count else 0
    
    b_chmf_per_line = b_ch_mf / bracket_count if bracket_count else 0
    nb_chmf_per_line = nb_ch_mf / nonbracket_count if nonbracket_count else 0
    
    # Rate per qok token
    b_chmf_rate = b_ch_mf / b_total_qok if b_total_qok else 0
    nb_chmf_rate = nb_ch_mf / nb_total_qok if nb_total_qok else 0
    E_chmf = b_chmf_rate / nb_chmf_rate if nb_chmf_rate else float('inf')
    
    print(f"\nqok-onset MID rate: bracket={b_qok_per_line:.3f}/line, non-bracket={nb_qok_per_line:.3f}/line")
    print(f"ch-midfix qok: bracket N={b_ch_mf}, non-bracket N={nb_ch_mf}")
    print(f"ch-midfix rate (per qok token): bracket={b_chmf_rate:.1%}, non-bracket={nb_chmf_rate:.1%}")
    print(f"Enrichment E={E_chmf:.2f}×")
    
    print(f"\nBracket top MID qok words: {bracket_mid_qok.most_common(10)}")
    print(f"Non-bracket top MID qok words: {nonbracket_mid_qok.most_common(10)}")
    
    # Also check specific bracket types (d→sh bracket, y→y bracket, k→ch bracket)
    print(f"\nBracket line breakdown:")
    for bt, n in bracket_types.most_common(10):
        print(f"  {bt[0]}→...→{bt[1]}: {n} lines")

if __name__ == '__main__':
    main()
