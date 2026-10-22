"""
exp_444: Cross-Line y→d Bigram (H_new_F)
Q: Is F326's y→d enrichment (1.37-1.49×) driven by cross-line bigrams
   (y-onset word at LL of line N → d-onset word at LF of line N+1)
   rather than within-line adjacency?

exp_441 showed within-line y→d E=0.93-0.96× (not enriched).
This experiment tests the cross-line hypothesis directly.
"""
from pathlib import Path as _RepositoryPath
import re
from collections import defaultdict, Counter

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

ONSETS = ['qok','qot','qo','cth','ch','sh','ok','ot','ol','d','s','y','k','t','l','r','p','f','o']

def get_onset(word):
    for on in ONSETS:
        if word.startswith(on):
            return on
    return 'other'

def parse_corpus():
    """Returns {folio: [line_words_list, ...]} in line order (P-loci only)."""
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

    # For cross-line bigrams:
    # Consider consecutive continuation lines (cont_lines[i] → cont_lines[i+1])
    # LL of line i = last word of cont_lines[i]
    # LF of line i+1 = first word of cont_lines[i+1]
    # Cross-line bigram: (LL_onset, LF_onset)

    # Store cross-line onset pair counts and marginals
    cl_pairs = {d: Counter() for d in ['A','B']}  # (LL_onset, LF_onset) counts
    ll_marginal = {d: Counter() for d in ['A','B']}  # LL onset counts
    lf_marginal = {d: Counter() for d in ['A','B']}  # LF onset counts
    total_cl = {d: 0 for d in ['A','B']}

    # Also track all words at LL and LF for overall onset rates
    all_words_by_pos = {d: {'LL': Counter(), 'LF': Counter()} for d in ['A','B']}

    for folio, lines in folios.items():
        if folio not in dialect_map:
            continue
        d = dialect_map[folio]
        n = len(lines)
        if n < 3:
            continue

        cont_lines = lines[1:-1]
        cn = len(cont_lines)
        if cn < 2:
            continue

        for ci, line_words in enumerate(cont_lines):
            # LF = first word, LL = last word
            lf_word = line_words[0]
            ll_word = line_words[-1]
            lf_on = get_onset(lf_word)
            ll_on = get_onset(ll_word)
            if lf_on != 'other':
                all_words_by_pos[d]['LF'][lf_on] += 1
            if ll_on != 'other':
                all_words_by_pos[d]['LL'][ll_on] += 1

        for ci in range(cn - 1):
            line_a = cont_lines[ci]
            line_b = cont_lines[ci + 1]
            ll_word = line_a[-1]
            lf_word = line_b[0]
            ll_on = get_onset(ll_word)
            lf_on = get_onset(lf_word)
            if ll_on == 'other' or lf_on == 'other':
                continue
            cl_pairs[d][(ll_on, lf_on)] += 1
            ll_marginal[d][ll_on] += 1
            lf_marginal[d][lf_on] += 1
            total_cl[d] += 1

    # Compute cross-line enrichment for y→d
    print("=== Cross-line onset bigrams (LL of line N → LF of line N+1) ===\n")
    for d in ['A','B']:
        tcl = total_cl[d]
        print(f"{d}-dialect: N cross-line pairs = {tcl}")
        # y→d
        ll_on, lf_on = 'y', 'd'
        obs = cl_pairs[d][(ll_on, lf_on)]
        p_ll = ll_marginal[d][ll_on] / sum(ll_marginal[d].values())
        p_lf = lf_marginal[d][lf_on] / sum(lf_marginal[d].values())
        exp = p_ll * p_lf * tcl
        E = obs / exp if exp > 0 else 0
        print(f"  y(LL)→d(LF): obs={obs}, exp={exp:.1f}, E={E:.2f}×")
        # breakdown: what d-onset words appear at LF after y-LL?
        all_yd = [(k, v) for k, v in cl_pairs[d].items() if k[0]=='y' and k[1]=='d']
        print(f"  y→d total: {obs}")
        # daiin fraction at LF after y-LL
        # We need word-level data for this

    # Also compute full y-successor cross-line bigram table
    print("\n=== y(LL) → * (LF of next line) ===")
    for d in ['A','B']:
        y_total = ll_marginal[d]['y']
        if y_total == 0:
            continue
        print(f"\n{d}-dialect (y at LL: N={y_total} cases):")
        print(f"  {'LF onset':<10}  {'obs':>5}  {'exp':>7}  {'E':>6}")
        lf_total = sum(lf_marginal[d].values())
        for on in ONSETS[:10]:  # top 10 onsets
            obs = cl_pairs[d][('y', on)]
            if obs == 0 and lf_marginal[d][on] == 0:
                continue
            p_lf = lf_marginal[d][on] / lf_total if lf_total > 0 else 0
            exp = p_lf * y_total
            E = obs / exp if exp > 0 else 0
            mark = ' **' if E > 1.5 and obs >= 3 else ''
            print(f"  {on:<10}  {obs:>5}  {exp:>7.1f}  {E:>6.2f}×{mark}")

    # Compute d(LF) ← * (LL of previous line)
    print("\n=== *(LL) → d (LF of next line) ===")
    for d in ['A','B']:
        d_total = lf_marginal[d]['d']
        if d_total == 0:
            continue
        print(f"\n{d}-dialect (d at LF: N={d_total} cases):")
        print(f"  {'LL onset':<10}  {'obs':>5}  {'exp':>7}  {'E':>6}")
        ll_total = sum(ll_marginal[d].values())
        for on in ONSETS[:10]:
            obs = cl_pairs[d][(on, 'd')]
            if obs == 0 and ll_marginal[d][on] == 0:
                continue
            p_ll = ll_marginal[d][on] / ll_total if ll_total > 0 else 0
            exp = p_ll * d_total
            E = obs / exp if exp > 0 else 0
            mark = ' **' if E > 1.5 and obs >= 3 else ''
            print(f"  {on:<10}  {obs:>5}  {exp:>7.1f}  {E:>6.2f}×{mark}")

    # Word-level cross-line bigrams: redo with words to get y→daiin
    print("\n=== Cross-line word bigram: y-onset(LL) → d-onset(LF): top d-words ===")
    cl_word_pairs = {d: Counter() for d in ['A','B']}
    yd_pairs = {d: Counter() for d in ['A','B']}

    for folio, lines in folios.items():
        if folio not in dialect_map:
            continue
        d = dialect_map[folio]
        n = len(lines)
        if n < 3:
            continue
        cont_lines = lines[1:-1]
        cn = len(cont_lines)
        for ci in range(cn - 1):
            line_a = cont_lines[ci]
            line_b = cont_lines[ci + 1]
            ll_word = line_a[-1]
            lf_word = line_b[0]
            ll_on = get_onset(ll_word)
            lf_on = get_onset(lf_word)
            if ll_on == 'y' and lf_on == 'd':
                yd_pairs[d][lf_word] += 1

    for d in ['A','B']:
        total_yd = sum(yd_pairs[d].values())
        print(f"\n{d}-dialect: y(LL)→d-onset(LF) pairs N={total_yd}")
        print("  Top d-words at LF after y-LL:")
        for word, cnt in yd_pairs[d].most_common(10):
            print(f"    {word}: {cnt}")

    # Also: compare to baseline d-word distribution at LF
    print("\n=== Baseline: all d-onset words at LF ===")
    for folio, lines in folios.items():
        if folio not in dialect_map:
            continue
        d = dialect_map[folio]
        n = len(lines)
        if n < 3:
            continue
        cont_lines = lines[1:-1]
        cn = len(cont_lines)
        for ci, line_words in enumerate(cont_lines):
            lf_word = line_words[0]
            if get_onset(lf_word) == 'd':
                all_words_by_pos[d]['LF'][lf_word] = all_words_by_pos[d]['LF'].get(lf_word, 0) + 1

    # This is a bit redundant, let me just recompute d-LF words
    d_lf_words = {d: Counter() for d in ['A','B']}
    for folio, lines in folios.items():
        if folio not in dialect_map:
            continue
        d = dialect_map[folio]
        n = len(lines)
        if n < 3:
            continue
        cont_lines = lines[1:-1]
        cn = len(cont_lines)
        for ci, line_words in enumerate(cont_lines):
            lf_word = line_words[0]
            if get_onset(lf_word) == 'd':
                d_lf_words[d][lf_word] += 1

    for d in ['A','B']:
        total_d_lf = sum(d_lf_words[d].values())
        print(f"\n{d}-dialect: all d-onset LF words (N={total_d_lf})")
        daiin_cnt = d_lf_words[d].get('daiin', 0)
        print(f"  daiin: {daiin_cnt} ({daiin_cnt/total_d_lf*100:.1f}% of d-LF)")
        for word, cnt in d_lf_words[d].most_common(5):
            print(f"  {word}: {cnt} ({cnt/total_d_lf*100:.1f}%)")

    # Key enrichment: is daiin enriched at LF AFTER y-LL compared to baseline?
    print("\n=== daiin enrichment at LF after y-LL vs baseline d-LF ===")
    for d in ['A','B']:
        total_yd = sum(yd_pairs[d].values())
        total_d_lf = sum(d_lf_words[d].values())
        if total_yd == 0 or total_d_lf == 0:
            continue
        daiin_after_y = yd_pairs[d].get('daiin', 0)
        daiin_baseline = d_lf_words[d].get('daiin', 0)
        daiin_baseline_rate = daiin_baseline / total_d_lf
        daiin_after_y_rate = daiin_after_y / total_yd if total_yd > 0 else 0
        E = daiin_after_y_rate / daiin_baseline_rate if daiin_baseline_rate > 0 else 0
        print(f"{d}: daiin after y-LL = {daiin_after_y}/{total_yd} "
              f"({daiin_after_y_rate*100:.1f}%) vs baseline {daiin_baseline_rate*100:.1f}%  "
              f"E={E:.2f}×")

if __name__ == '__main__':
    main()
