"""
exp_448: Cross-Line Inversion Correlation (H_new_K)
Q: Does within-line depletion at pLL→LL predict cross-line enrichment at LL→LF?
   Is the inversion pattern (CL enriched ↔ within-line depleted) systematic or specific?

Method: Compute full 19×19 within-line (pLL→LL) and cross-line (LL→LF) bigram
matrices. Spearman correlation between pLL→LL E and CL E across all pairs with
expected N≥2. Also: direct test of whether E_within < 0.8 predicts E_CL > 1.2.
"""
import re
import math
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

def spearman(x, y):
    n = len(x)
    if n < 3:
        return 0, n
    def rank(lst):
        sorted_lst = sorted(enumerate(lst), key=lambda t: t[1])
        ranks = [0] * n
        for rank_i, (orig_i, _) in enumerate(sorted_lst):
            ranks[orig_i] = rank_i + 1
        return ranks
    rx = rank(x)
    ry = rank(y)
    d2 = sum((a - b)**2 for a, b in zip(rx, ry))
    rho = 1 - 6 * d2 / (n * (n**2 - 1))
    return rho, n

def compute_bigram_matrices(folios, dialect_map):
    """Returns (cl_matrix, within_pll_ll_matrix) for each dialect.
    cl_matrix[d][(ll_on, lf_on)] = (obs, exp, E)
    within_matrix[d][(pll_on, ll_on)] = (obs, exp, E)
    """
    # Cross-line bigrams
    cl_pairs = {d: Counter() for d in ['A','B']}
    ll_marg = {d: Counter() for d in ['A','B']}
    lf_marg = {d: Counter() for d in ['A','B']}
    total_cl = {d: 0 for d in ['A','B']}

    # Within-line pLL→LL bigrams
    pll_ll_pairs = {d: Counter() for d in ['A','B']}
    pll_marg = {d: Counter() for d in ['A','B']}
    ll_marg_within = {d: Counter() for d in ['A','B']}
    total_pll_ll = {d: 0 for d in ['A','B']}

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
            # pLL→LL within-line
            if len(line_words) >= 2:
                pll_on = get_onset(line_words[-2])
                ll_on = get_onset(line_words[-1])
                if pll_on != 'other' and ll_on != 'other':
                    pll_ll_pairs[d][(pll_on, ll_on)] += 1
                    pll_marg[d][pll_on] += 1
                    ll_marg_within[d][ll_on] += 1
                    total_pll_ll[d] += 1

        # Cross-line LL→LF
        for ci in range(cn - 1):
            line_a = cont_lines[ci]
            line_b = cont_lines[ci + 1]
            ll_on = get_onset(line_a[-1])
            lf_on = get_onset(line_b[0])
            if ll_on != 'other' and lf_on != 'other':
                cl_pairs[d][(ll_on, lf_on)] += 1
                ll_marg[d][ll_on] += 1
                lf_marg[d][lf_on] += 1
                total_cl[d] += 1

    # Compute E for all pairs
    def make_enrichment_dict(pairs, marg_a, marg_b, total):
        result = {}
        tot_a = sum(marg_a.values())
        tot_b = sum(marg_b.values())
        for on_a in ONSETS:
            for on_b in ONSETS:
                p_a = marg_a[on_a] / tot_a if tot_a > 0 else 0
                p_b = marg_b[on_b] / tot_b if tot_b > 0 else 0
                exp = p_a * p_b * total
                obs = pairs[(on_a, on_b)]
                E = obs / exp if exp > 0 else 0
                result[(on_a, on_b)] = (obs, exp, E)
        return result

    cl_enrich = {d: make_enrichment_dict(cl_pairs[d], ll_marg[d], lf_marg[d], total_cl[d])
                 for d in ['A','B']}
    within_enrich = {d: make_enrichment_dict(pll_ll_pairs[d], pll_marg[d], ll_marg_within[d], total_pll_ll[d])
                     for d in ['A','B']}

    return cl_enrich, within_enrich

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)
    cl_enrich, within_enrich = compute_bigram_matrices(folios, dialect_map)

    # For each dialect, compute Spearman correlation between within E and CL E
    # Use pairs where EITHER within OR CL expected N >= 2
    print("=== Spearman correlation: within-line (pLL→LL) E vs cross-line (LL→LF) E ===\n")
    for d in ['A','B']:
        x_vals = []  # within-line E
        y_vals = []  # cross-line E
        pair_list = []

        for on_a in ONSETS:
            for on_b in ONSETS:
                w_obs, w_exp, w_E = within_enrich[d][(on_a, on_b)]
                c_obs, c_exp, c_E = cl_enrich[d][(on_a, on_b)]
                # Include if expected N >= 2 in either
                if w_exp >= 2 or c_exp >= 2:
                    x_vals.append(w_E)
                    y_vals.append(c_E)
                    pair_list.append((on_a, on_b, w_obs, w_E, c_obs, c_E))

        rho, n = spearman(x_vals, y_vals)
        print(f"{d}-dialect: Spearman rho(within_E, CL_E) = {rho:.3f}  (N={n} pairs)")

    # Show the matrix of within-E vs CL-E for major onsets
    print("\n=== within-E vs CL-E comparison matrix (pairs with CL_exp≥2 or within_exp≥2) ===\n")
    for d in ['A','B']:
        print(f"{d}-dialect:")
        # Sort by CL_E descending
        pairs_sorted = []
        for on_a in ONSETS:
            for on_b in ONSETS:
                w_obs, w_exp, w_E = within_enrich[d][(on_a, on_b)]
                c_obs, c_exp, c_E = cl_enrich[d][(on_a, on_b)]
                if (w_exp >= 3 or c_exp >= 3) and (w_obs > 0 or c_obs > 0):
                    inversion = c_E > 1.3 and w_E < 0.85
                    same_dir = c_E > 1.3 and w_E > 1.3
                    pairs_sorted.append((on_a, on_b, w_obs, w_E, c_obs, c_E, inversion, same_dir))

        pairs_sorted.sort(key=lambda x: -x[5])  # sort by CL_E

        print(f"  {'Pair':<12}  {'W obs':>6}  {'W E':>6}  {'CL obs':>7}  {'CL E':>7}  {'Pattern'}")
        for (on_a, on_b, w_obs, w_E, c_obs, c_E, inv, same) in pairs_sorted[:30]:
            pattern = 'INVERT' if inv else ('SAME-DIR' if same else '')
            if c_E > 1.3 or w_E > 1.3 or c_E < 0.6 or w_E < 0.6:
                print(f"  {on_a}→{on_b:<10}  {w_obs:>6}  {w_E:>6.2f}×  {c_obs:>7}  {c_E:>7.2f}×  {pattern}")
        print()

    # Direct test: pairs with within E < 0.8 — what is their CL E distribution?
    print("=== Direct test: within E<0.8 → CL E distribution ===\n")
    for d in ['A','B']:
        depleted_cl = []
        not_depleted_cl = []
        for on_a in ONSETS:
            for on_b in ONSETS:
                w_obs, w_exp, w_E = within_enrich[d][(on_a, on_b)]
                c_obs, c_exp, c_E = cl_enrich[d][(on_a, on_b)]
                if w_exp < 3 and c_exp < 3:
                    continue
                if w_E < 0.8:
                    depleted_cl.append((c_E, on_a, on_b, w_obs, w_E, c_obs, c_E))
                else:
                    not_depleted_cl.append(c_E)

        depleted_cl.sort(key=lambda x: -x[0])
        mean_dep = sum(x[0] for x in depleted_cl) / len(depleted_cl) if depleted_cl else 0
        mean_non = sum(not_depleted_cl) / len(not_depleted_cl) if not_depleted_cl else 0
        print(f"{d}: N(within<0.8) = {len(depleted_cl)}, mean CL E = {mean_dep:.2f}×")
        print(f"   N(within≥0.8) = {len(not_depleted_cl)}, mean CL E = {mean_non:.2f}×")
        print(f"   Depleted pairs with CL E > 1.3:")
        for (c_E, on_a, on_b, w_obs, w_E, c_obs, _) in depleted_cl:
            if c_E > 1.3:
                print(f"     {on_a}→{on_b}: within={w_E:.2f}×(N={w_obs}) → CL={c_E:.2f}×(N={c_obs})")
        print()

    # Summary: inversion count
    print("=== Inversion count summary ===\n")
    for d in ['A','B']:
        inversion_count = 0
        same_dir_count = 0
        total_strong = 0
        for on_a in ONSETS:
            for on_b in ONSETS:
                w_obs, w_exp, w_E = within_enrich[d][(on_a, on_b)]
                c_obs, c_exp, c_E = cl_enrich[d][(on_a, on_b)]
                if w_exp < 3 and c_exp < 3:
                    continue
                if c_E > 1.3 or w_E > 1.3:
                    total_strong += 1
                    if c_E > 1.3 and w_E < 0.85:
                        inversion_count += 1
                    elif c_E > 1.3 and w_E > 1.3:
                        same_dir_count += 1
        print(f"{d}: {inversion_count} inversion pairs (CL>1.3/within<0.85) out of {total_strong} strong pairs")
        print(f"   {same_dir_count} same-direction pairs (both CL>1.3 AND within>1.3)")

if __name__ == '__main__':
    main()
