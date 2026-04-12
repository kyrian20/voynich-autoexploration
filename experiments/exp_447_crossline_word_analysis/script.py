"""
exp_447: Cross-Line Coupling Word-Level Analysis (H_new_I + H_new_J)
Q1 (H_new_I): ok(LL)→y(LF) — class-level or word-type specific?
Q2 (H_new_J): B qok(LL)→s(LF) E=1.51× — is this the s→sh→qok formula cycle?

Method: ZL3B continuation lines. Enumerate word-level cross-line pairs for
specific onset combinations. Classify as class-level vs word-pair specific.
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

def parse_corpus():
    pattern = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
    folios = defaultdict(list)
    folio_order = []
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
                    if folio not in folios:
                        folio_order.append(folio)
                    folios[folio].append(words)
    return folios, folio_order

def classify_dialects(folios):
    dialect = {}
    for folio, lines in folios.items():
        total = sum(len(ws) for ws in lines)
        if total == 0: continue
        edy = sum(1 for ws in lines for w in ws
                  if w.endswith('edy') or w.endswith('eedy'))
        dialect[folio] = 'B' if edy / total >= 0.05 else 'A'
    return dialect

def get_section(folio):
    """Simple section classifier."""
    digits = re.sub(r'[^0-9]', '', folio)
    if not digits:
        return 'unknown'
    f = int(digits[:3]) if len(digits) >= 3 else int(digits)
    if f <= 72:
        return 'herbal'
    elif f <= 84:
        return 'astro'
    elif f <= 102:
        return 'bio'
    elif f <= 116:
        return 'pharma'
    else:
        return 'other'

def main():
    folios, folio_order = parse_corpus()
    dialect_map = classify_dialects(folios)

    # Collect all cross-line pairs with word-level info
    # cl_data: list of (dialect, folio, section, ll_word, lf_word, ll_on, lf_on)
    cl_data = []

    for folio in folio_order:
        lines = folios[folio]
        if folio not in dialect_map:
            continue
        d = dialect_map[folio]
        n = len(lines)
        if n < 3:
            continue
        cont_lines = lines[1:-1]
        cn = len(cont_lines)
        section = get_section(folio)

        for ci in range(cn - 1):
            line_a = cont_lines[ci]
            line_b = cont_lines[ci + 1]
            ll_word = line_a[-1]
            lf_word = line_b[0]
            ll_on = get_onset(ll_word)
            lf_on = get_onset(lf_word)
            if ll_on != 'other' and lf_on != 'other':
                cl_data.append((d, folio, section, ll_word, lf_word, ll_on, lf_on))

    # Also collect baselines: ok-words at LL, y-words at LF (general)
    ok_at_ll = {d: Counter() for d in ['A','B']}
    y_at_lf = {d: Counter() for d in ['A','B']}
    qok_at_ll = {d: Counter() for d in ['A','B']}
    s_at_lf = {d: Counter() for d in ['A','B']}

    for folio in folio_order:
        lines = folios[folio]
        if folio not in dialect_map:
            continue
        d = dialect_map[folio]
        n = len(lines)
        if n < 3:
            continue
        cont_lines = lines[1:-1]
        cn = len(cont_lines)
        for ci, line_words in enumerate(cont_lines):
            ll_word = line_words[-1]
            lf_word = line_words[0]
            ll_on = get_onset(ll_word)
            lf_on = get_onset(lf_word)
            if ll_on == 'ok':
                ok_at_ll[d][ll_word] += 1
            if ll_on == 'qok':
                qok_at_ll[d][ll_word] += 1
            if lf_on == 'y':
                y_at_lf[d][lf_word] += 1
            if lf_on == 's':
                s_at_lf[d][lf_word] += 1

    # H_new_I: ok→y cross-line word pairs
    print("=== H_new_I: ok(LL)→y(LF) cross-line word pairs ===\n")
    for d in ['A','B']:
        ok_y_pairs = [(r[3], r[4]) for r in cl_data if r[0]==d and r[5]=='ok' and r[6]=='y']
        print(f"{d}-dialect: N(ok→y) = {len(ok_y_pairs)}")

        # Word-pair distribution
        pair_counter = Counter(ok_y_pairs)
        print("  Top word pairs (ok-word, y-word):")
        for (ll_w, lf_w), cnt in pair_counter.most_common(10):
            print(f"    {ll_w} → {lf_w}: {cnt}")

        # ok-word types at LL in these pairs
        ok_ll_in_pairs = Counter(r[3] for r in cl_data if r[0]==d and r[5]=='ok' and r[6]=='y')
        print(f"\n  ok-words at LL (in ok→y pairs):")
        for w, cnt in ok_ll_in_pairs.most_common(8):
            total_ok_ll = ok_at_ll[d][w]
            print(f"    {w}: {cnt} (total ok-LL: {total_ok_ll})")

        # y-word types at LF in these pairs
        y_lf_in_pairs = Counter(r[4] for r in cl_data if r[0]==d and r[5]=='ok' and r[6]=='y')
        print(f"\n  y-words at LF (after ok-LL):")
        for w, cnt in y_lf_in_pairs.most_common(8):
            total_y_lf = y_at_lf[d][w]
            print(f"    {w}: {cnt} (total y-LF: {total_y_lf})")

        # Class-level test: is the ok→y ratio similar across ok-word types?
        total_ok_ll_n = sum(ok_at_ll[d].values())
        total_pairs = sum(1 for r in cl_data if r[0]==d and r[5]=='ok')
        total_ok_y = len(ok_y_pairs)
        global_ok_y_rate = total_ok_y / total_pairs if total_pairs > 0 else 0
        print(f"\n  Global ok→y rate: {total_ok_y}/{total_pairs} = {global_ok_y_rate*100:.1f}%")
        print(f"  (If class-level: all ok-words should have similar y-LF rate)")
        print()

    # H_new_J: B qok→s cross-line
    print("=== H_new_J: B qok(LL)→s(LF) cross-line pairs ===\n")
    d = 'B'
    qok_s_pairs = [(r[2], r[3], r[4]) for r in cl_data if r[0]==d and r[5]=='qok' and r[6]=='s']
    print(f"B-dialect: N(qok→s) = {len(qok_s_pairs)}")

    # Section distribution
    section_counts = Counter(r[0] for r in qok_s_pairs)
    print("  Section distribution:")
    for sec, cnt in section_counts.most_common():
        print(f"    {sec}: {cnt}")

    # qok-words at LL
    qok_ll_words = Counter(r[1] for r in qok_s_pairs)
    print("\n  qok-words at LL (in qok→s pairs):")
    for w, cnt in qok_ll_words.most_common(10):
        total_qok_ll = qok_at_ll[d][w]
        rate = cnt/total_qok_ll*100 if total_qok_ll > 0 else 0
        print(f"    {w}: {cnt}/{total_qok_ll} ({rate:.1f}% of all {w} at LL cross into s)")

    # s-words at LF
    s_lf_words = Counter(r[2] for r in qok_s_pairs)
    print("\n  s-words at LF (after qok-LL):")
    for w, cnt in s_lf_words.most_common(10):
        total_s_lf = s_at_lf[d][w]
        print(f"    {w}: {cnt} (total s-LF: {total_s_lf})")

    # Compare to baseline: what follows qok at LL in general?
    qok_ll_all = Counter(r[4] for r in cl_data if r[0]==d and r[5]=='qok')
    total_qok_cl = sum(qok_ll_all.values())
    print(f"\n  qok-LL total cross-line pairs: {total_qok_cl}")
    print("  LF onset distribution after qok-LL:")
    for on in ['s','sh','d','ch','qok','y','ok','ot','ol']:
        cnt = qok_ll_all.get(on, 0)
        if cnt > 0 or True:
            print(f"    {on}: {cnt} ({cnt/total_qok_cl*100:.1f}%)")

    # Also: A qok→s and A s→s for comparison
    print("\n\n=== A-dialect s→s cross-line pairs ===")
    d = 'A'
    s_s_pairs = [(r[2], r[3], r[4]) for r in cl_data if r[0]==d and r[5]=='s' and r[6]=='s']
    print(f"A s→s cross-line N={len(s_s_pairs)}")
    print("  Specific (s-word LL, s-word LF) pairs:")
    pair_c = Counter((r[1], r[2]) for r in s_s_pairs)
    for (ll_w, lf_w), cnt in pair_c.most_common(8):
        print(f"    {ll_w} → {lf_w}: {cnt}")

    print("\n=== B-dialect s→s cross-line pairs ===")
    d = 'B'
    s_s_pairs_b = [(r[2], r[3], r[4]) for r in cl_data if r[0]==d and r[5]=='s' and r[6]=='s']
    print(f"B s→s cross-line N={len(s_s_pairs_b)}")
    pair_c = Counter((r[1], r[2]) for r in s_s_pairs_b)
    for (ll_w, lf_w), cnt in pair_c.most_common(8):
        print(f"    {ll_w} → {lf_w}: {cnt}")

    # Word uniqueness test for s→s: are these same s-word repeats or different s-words?
    for d in ['A','B']:
        s_s = [(r[3], r[4]) for r in cl_data if r[0]==d and r[5]=='s' and r[6]=='s']
        same_word = sum(1 for (a,b) in s_s if a == b)
        print(f"\n{d} s→s: {same_word}/{len(s_s)} = {same_word/len(s_s)*100:.0f}% same exact s-word")

    # ok→y: ot→y comparison
    print("\n\n=== Cross-line ot(LL)→y(LF) vs ok→y ===")
    for d in ['A','B']:
        ot_y = [(r[3], r[4]) for r in cl_data if r[0]==d and r[5]=='ot' and r[6]=='y']
        ok_y = [(r[3], r[4]) for r in cl_data if r[0]==d and r[5]=='ok' and r[6]=='y']
        ot_total = sum(1 for r in cl_data if r[0]==d and r[5]=='ot')
        ok_total = sum(1 for r in cl_data if r[0]==d and r[5]=='ok')
        print(f"{d}: ot→y = {len(ot_y)}/{ot_total} ({len(ot_y)/ot_total*100:.1f}%)  "
              f"ok→y = {len(ok_y)}/{ok_total} ({len(ok_y)/ok_total*100:.1f}%)")

if __name__ == '__main__':
    main()
