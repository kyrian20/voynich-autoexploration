"""
exp_458: ch-onset Body-Conditional Within-Line and Cross-Line Analysis (H_new_W)
Q: (1) Is ch+edy at LL → qot CL (E=2.23×/N=7, exp_457) reproducible?
   (2) Does chedy within-line → qot (would explain the CL finding)?
   (3) What is the full ch-onset body-conditional bigram profile within-line?

Method:
  Part A — Within-line body-conditional bigrams for ch-onset (MID positions).
  Part B — Cross-line CL for ch-onset (LL → next LF), with body breakdown.
  Parallel for both B-dialect and A-dialect.
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

def analyze_within_line_ch(folios, dialect_map, target_dialect):
    """Body-conditional bigrams for ch-onset within MID positions."""
    body_bigrams = defaultdict(Counter)   # (body_char) -> Counter(succ_onset)
    body_total = Counter()                 # body_char -> total
    succ_total = Counter()                 # succ_onset -> total across all ch words
    ch_total = 0

    for folio, lines in folios.items():
        if folio not in dialect_map or dialect_map[folio] != target_dialect:
            continue
        for line in lines:
            if len(line) < 3: continue
            # MID positions: indices 1..len-2
            for i in range(1, len(line) - 1):
                w1 = line[i]
                w2 = line[i+1]
                on1 = get_onset(w1)
                on2 = get_onset(w2)
                if on1 != 'ch' or on2 == 'other': continue
                bc1 = get_first_body_char(w1, on1)
                body_bigrams[bc1][on2] += 1
                body_total[bc1] += 1
                succ_total[on2] += 1
                ch_total += 1

    return body_bigrams, body_total, succ_total, ch_total

def analyze_crossline_ch(folios, dialect_map, target_dialect):
    """Cross-line analysis for ch-onset LL words → next LF onset."""
    cl_body = defaultdict(Counter)
    body_total = Counter()
    lf_total = Counter()
    total_cl = 0

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
            if ll_on != 'ch': continue
            ll_bc = get_first_body_char(ll_word, ll_on)
            cl_body[ll_bc][lf_on] += 1
            body_total[ll_bc] += 1

    return cl_body, body_total, lf_total, total_cl

def print_body_bigram_table(body_bigrams, body_total, succ_total, ch_total,
                             top_succ=None, dialect='', context='within-line'):
    total_bc = sum(body_total.values())
    if not top_succ:
        all_succ = Counter()
        for bc_data in body_bigrams.values():
            all_succ.update(bc_data)
        top_succ = [s for s, _ in all_succ.most_common(7)]

    print(f"\n  {dialect} ch-onset {context} bigrams (total ch words: {ch_total})")
    header = f"  {'body':>6}  {'N':>6}"
    for s in top_succ:
        header += f"  {'→'+s:>12}"
    print(header)

    # Sort by frequency
    body_keys = sorted(body_total.keys(), key=lambda bc: -body_total[bc])
    for bc in body_keys:
        n = body_total[bc]
        if n < 5: continue
        row = f"  '{bc}':  {n:>6}"
        for s in top_succ:
            obs = body_bigrams[bc][s]
            base_p = succ_total[s] / ch_total if ch_total > 0 else 0
            exp = n * base_p
            if exp >= 1.0:
                E = obs / exp
                mk = '↑' if E >= 1.4 else ('↓' if E <= 0.6 else ' ')
                row += f"  {E:.2f}×{mk}(N={obs:2d})"
            else:
                row += f"  {'--':>12}"
        print(row)

    # Special focus: edy vs aiin contrast
    print(f"\n  KEY CONTRAST — edy vs aiin body ({dialect} {context}):")
    for bc_label, bc in [('edy(e)', 'e'), ('aiin(a)', 'a')]:
        n = body_total.get(bc, 0)
        if n < 3:
            print(f"    {bc_label}: N={n} (insufficient)")
            continue
        row = f"    {bc_label}: N={n}  "
        for s in top_succ:
            obs = body_bigrams[bc][s]
            base_p = succ_total[s] / ch_total if ch_total > 0 else 0
            exp = n * base_p
            if exp >= 1.0:
                E = obs / exp
                mk = '↑' if E >= 1.4 else ('↓' if E <= 0.6 else ' ')
                row += f"→{s}={E:.2f}×{mk}(N={obs}) "
            elif exp >= 0.3:
                row += f"→{s}=dir(N={obs}) "
        print(row)

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)

    print("="*65)
    print("  EXP_458: ch-onset Body-Conditional Analysis (H_new_W)")
    print("="*65)

    for dialect in ['B', 'A']:
        print(f"\n{'='*65}")
        print(f"  {dialect}-DIALECT")
        print(f"{'='*65}")

        # Part A: Within-line ch body-conditional bigrams
        wl_bb, wl_bt, wl_st, wl_total = analyze_within_line_ch(folios, dialect_map, dialect)
        top_succ_wl = ['qok', 'qot', 'sh', 'd', 'ok', 'ch', 'y']
        print_body_bigram_table(wl_bb, wl_bt, wl_st, wl_total,
                                 top_succ=top_succ_wl, dialect=dialect, context='within-line MID')

        # Part B: Cross-line ch body-conditional
        cl_body, cl_bt, cl_lf_total, cl_total = analyze_crossline_ch(folios, dialect_map, dialect)
        top_succ_cl = ['qot', 'd', 's', 'ch', 'sh', 'qok', 'y']
        print(f"\n  {dialect} ch-onset CROSS-LINE (LL → next LF):")
        print(f"  Total CL pairs: {cl_total}")
        ch_ll_total = sum(cl_bt.values())
        if ch_ll_total > 0:
            print(f"  Total ch at LL: {ch_ll_total}")
            header = f"  {'body':>6}  {'N':>6}"
            for s in top_succ_cl:
                header += f"  {'→'+s:>12}"
            print(header)

            body_keys = sorted(cl_bt.keys(), key=lambda bc: -cl_bt[bc])
            for bc in body_keys:
                n = cl_bt[bc]
                if n < 5: continue
                row = f"  '{bc}':  {n:>6}"
                for s in top_succ_cl:
                    obs = cl_body[bc][s]
                    base_p = cl_lf_total[s] / cl_total if cl_total > 0 else 0
                    exp = n * base_p
                    if exp >= 0.8:
                        E = obs / exp
                        mk = '↑' if E >= 1.4 else ('↓' if E <= 0.6 else ' ')
                        row += f"  {E:.2f}×{mk}(N={obs:2d})"
                    else:
                        row += f"  {'--':>12}"
                print(row)

            # Overall ch CL
            print(f"\n  Overall ch CL (all body classes):")
            all_ch_cl = Counter()
            for bc_data in cl_body.values():
                all_ch_cl.update(bc_data)
            for s in top_succ_cl:
                obs = all_ch_cl[s]
                base_p = cl_lf_total[s] / cl_total if cl_total > 0 else 0
                exp = ch_ll_total * base_p
                if exp >= 1.0:
                    E = obs / exp
                    print(f"    →{s}: E={E:.2f}×(N={obs})", end='  ')
            print()

            # edy vs aiin special focus
            print(f"\n  KEY CL edy vs aiin contrast ({dialect}):")
            for bc_label, bc in [('edy(e)', 'e'), ('aiin(a)', 'a')]:
                n = cl_bt.get(bc, 0)
                if n < 3:
                    print(f"    {bc_label}: N={n} (insufficient)")
                    continue
                row = f"    {bc_label}: N={n}  "
                for s in ['qot', 'd', 'ch', 'sh', 'qok', 's', 'y']:
                    obs = cl_body.get(bc, Counter())[s]
                    base_p = cl_lf_total[s] / cl_total if cl_total > 0 else 0
                    exp = n * base_p
                    if exp >= 0.5:
                        E = obs / exp
                        mk = '↑' if E >= 1.4 else ('↓' if E <= 0.6 else ' ')
                        row += f"→{s}={E:.2f}×{mk}(N={obs}) "
                    elif exp >= 0.2:
                        row += f"→{s}=dir(N={obs}) "
                print(row)

if __name__ == '__main__':
    main()
