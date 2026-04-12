"""
exp_460: A-Dialect s→qot Cross-Line Coupling Confirmation (H_new_Y)
Q: Is A s at LL → qot at next LF (E=2.77×/N=5) a genuine finding?
   What body class drives it? How does A s cross-line compare to B s?

Method:
  (1) A-dialect s at LL cross-line analysis with body-conditional breakdown
  (2) Verify folio/word diversity (class-level, not word-specific?)
  (3) A s → qot: check what onset class appears after qot-LF lines (A qot routing)
  (4) B s cross-line for comparison
"""
import re
from collections import defaultdict, Counter

ZL3B = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'
ONSETS = ['qok','qot','qo','cth','ch','sh','ok','ot','ol','d','s','y','k','t','l','r','p','f','o']

def get_onset(word):
    for on in ONSETS:
        if word.startswith(on):
            return on
    return 'other'

def get_first_body_char(word, onset):
    body = word[len(onset):]
    return body[0] if body else '_'

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

def analyze_s_crossline(folios, dialect_map, target_dialect):
    """s-onset at LL cross-line analysis."""
    cl_body = defaultdict(Counter)   # body_char -> Counter(lf_onset)
    body_total = Counter()
    lf_total = Counter()
    total_cl = 0

    s_qot_cases = []  # detailed cases for s→qot

    for folio, lines in folios.items():
        if folio not in dialect_map or dialect_map[folio] != target_dialect:
            continue
        n = len(lines)
        if n < 3: continue
        cont_lines = lines[1:-1]
        cn = len(cont_lines)

        for ci in range(cn - 1):
            ll_word = cont_lines[ci][-1]
            lf_word = cont_lines[ci+1][0]
            ll_on = get_onset(ll_word)
            lf_on = get_onset(lf_word)
            if lf_on == 'other': continue
            lf_total[lf_on] += 1
            total_cl += 1
            if ll_on != 's': continue
            ll_bc = get_first_body_char(ll_word, ll_on)
            cl_body[ll_bc][lf_on] += 1
            body_total[ll_bc] += 1
            if lf_on == 'qot':
                s_qot_cases.append((folio, ll_word, lf_word))

    s_total = sum(body_total.values())
    return cl_body, body_total, lf_total, total_cl, s_total, s_qot_cases

def print_s_analysis(cl_body, body_total, lf_total, total_cl, s_total, s_qot_cases, dialect):
    top_lf = ['s', 'qot', 'qok', 'sh', 'd', 'ch', 'y']
    print(f"\n{'='*60}")
    print(f"  {dialect}-DIALECT: s at LL cross-line analysis (total s-LL: {s_total})")
    print(f"  Total CL pairs: {total_cl}")
    print(f"{'='*60}")

    # Overall s CL distribution
    all_s_cl = Counter()
    for bc_data in cl_body.values():
        all_s_cl.update(bc_data)
    print(f"\n  Overall s at LL → next LF enrichments:")
    for lf in top_lf:
        obs = all_s_cl[lf]
        base_p = lf_total[lf] / total_cl
        exp = s_total * base_p
        if exp >= 1:
            E = obs / exp
            mk = '↑' if E >= 1.4 else ('↓' if E <= 0.6 else ' ')
            print(f"    →{lf}: E={E:.2f}×{mk}(N={obs}, exp={exp:.1f})", end='  ')
    print()

    # Body-conditional breakdown
    print(f"\n  Body-conditional breakdown:")
    header = f"  {'body':>7}  {'N':>5}"
    for lf in top_lf:
        header += f"  {'→'+lf:>10}"
    print(header)

    body_keys = sorted(body_total.keys(), key=lambda bc: -body_total[bc])
    for bc in body_keys:
        n = body_total[bc]
        if n < 5: continue
        row = f"  '{bc}':  {n:>5}"
        for lf in top_lf:
            obs = cl_body[bc][lf]
            base_p = lf_total[lf] / total_cl
            exp = n * base_p
            if exp >= 0.8:
                E = obs / exp
                mk = '↑' if E >= 1.4 else ('↓' if E <= 0.6 else ' ')
                row += f"  {E:.2f}×{mk}(N={obs:2d})"
            else:
                row += f"  dir({obs}){' ':>5}"
        print(row)

    # s→qot detailed cases
    if s_qot_cases:
        print(f"\n  s→qot cross-line cases (N={len(s_qot_cases)}):")
        word_types = Counter((case[1], case[2]) for case in s_qot_cases)
        folios_involved = set(case[0] for case in s_qot_cases)
        ll_words = Counter(case[1] for case in s_qot_cases)
        lf_words = Counter(case[2] for case in s_qot_cases)
        print(f"    Folios: {sorted(folios_involved)}")
        print(f"    Unique LL words: {len(ll_words)} = {dict(ll_words.most_common(8))}")
        print(f"    Unique LF words: {len(lf_words)} = {dict(lf_words.most_common(8))}")
        print(f"    Unique pairs: {len(word_types)}/{len(s_qot_cases)}")
        same_pair = [pair for pair, cnt in word_types.items() if cnt > 1]
        if same_pair:
            print(f"    Repeated pairs: {same_pair}")

    # s→s detailed cases for comparison
    s_s_cases = sum(cl_body[bc]['s'] for bc in cl_body)
    s_s_obs = all_s_cl['s']
    base_p_s = lf_total['s'] / total_cl
    exp_s_s = s_total * base_p_s
    E_s_s = s_s_obs / exp_s_s if exp_s_s > 0 else 0
    print(f"\n  s→s cross-line: N={s_s_obs}, E={E_s_s:.2f}×, exp={exp_s_s:.1f}")
    print(f"  s→qot cross-line: N={all_s_cl['qot']}, E={all_s_cl['qot']/((lf_total['qot']/total_cl)*s_total):.2f}×" if lf_total['qot'] > 0 else "")

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)

    for dialect in ['A', 'B']:
        cl_body, body_total, lf_total, total_cl, s_total, s_qot_cases = \
            analyze_s_crossline(folios, dialect_map, dialect)
        print_s_analysis(cl_body, body_total, lf_total, total_cl, s_total, s_qot_cases, dialect)

if __name__ == '__main__':
    main()
