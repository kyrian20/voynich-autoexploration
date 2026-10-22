"""
exp_445: Cross-Line Onset Bigram Full Matrix (H_new_G)
Q: Which LL→LF cross-line onset couplings are systematic (E≥1.5, N≥5)?
   Is cross-line grammar similar to within-line grammar or structurally different?

Method: ZL3B continuation lines. For consecutive pairs of continuation lines in
same folio, compute (LL onset, LF onset) bigrams. Compare to within-line bigrams.
"""
from pathlib import Path as _RepositoryPath
import re
from collections import defaultdict, Counter
import math

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

ONSETS = ['qok','qot','qo','cth','ch','sh','ok','ot','ol','d','s','y','k','t','l','r','p','f','o']
# Compact list for matrix display
TOP_ONSETS = ['qok','qot','qo','ch','sh','ok','ot','ol','d','s','y','k','t','l','o']

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

def compute_enrichments(pairs, ll_marg, lf_marg, total):
    """Return dict of (ll_on, lf_on) -> E for all pairs."""
    results = {}
    ll_total = sum(ll_marg.values())
    lf_total = sum(lf_marg.values())
    for pair, obs in pairs.items():
        ll_on, lf_on = pair
        p_ll = ll_marg[ll_on] / ll_total if ll_total > 0 else 0
        p_lf = lf_marg[lf_on] / lf_total if lf_total > 0 else 0
        exp = p_ll * p_lf * total
        E = obs / exp if exp > 0 else 0
        results[pair] = (obs, exp, E)
    return results

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)

    # Cross-line bigrams
    cl_pairs = {d: Counter() for d in ['A','B']}
    ll_marg = {d: Counter() for d in ['A','B']}
    lf_marg = {d: Counter() for d in ['A','B']}
    total_cl = {d: 0 for d in ['A','B']}

    # Within-line last→first (pre_LL→LF pattern within same line) for comparison
    # Actually, let's do within-line: last word → second word of same line (as proxy)
    # Better: within-line (pre-LL onset → LL onset) bigrams for comparison

    # Pre_LL → LL within-line bigrams
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
        if cn < 2:
            continue

        for ci, line_words in enumerate(cont_lines):
            # Within-line: pre-LL → LL
            if len(line_words) >= 2:
                pll_word = line_words[-2]
                ll_word = line_words[-1]
                pll_on = get_onset(pll_word)
                ll_on = get_onset(ll_word)
                if pll_on != 'other' and ll_on != 'other':
                    pll_ll_pairs[d][(pll_on, ll_on)] += 1
                    pll_marg[d][pll_on] += 1
                    ll_marg_within[d][ll_on] += 1
                    total_pll_ll[d] += 1

        # Cross-line bigrams
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
            ll_marg[d][ll_on] += 1
            lf_marg[d][lf_on] += 1
            total_cl[d] += 1

    # Compute enrichments
    cl_enrich = {d: compute_enrichments(cl_pairs[d], ll_marg[d], lf_marg[d], total_cl[d])
                 for d in ['A','B']}

    # Print top cross-line couplings
    print("=== Top cross-line onset couplings (E≥1.4, N≥3) ===\n")
    for d in ['A','B']:
        print(f"{d}-dialect (N cross-line pairs = {total_cl[d]}):")
        print(f"  {'LL→LF':<15}  {'obs':>5}  {'exp':>7}  {'E':>6}")
        results = sorted(cl_enrich[d].items(), key=lambda x: -x[1][2])
        for (ll_on, lf_on), (obs, exp, E) in results:
            if E >= 1.4 and obs >= 3:
                print(f"  {ll_on}→{lf_on:<12}  {obs:>5}  {exp:>7.1f}  {E:>6.2f}×")
        print()

    # Print notable DEPLETED cross-line couplings
    print("=== Notable cross-line DEPLETION (E≤0.5, N_expected≥5) ===\n")
    for d in ['A','B']:
        print(f"{d}-dialect:")
        results = sorted(cl_enrich[d].items(), key=lambda x: x[1][2])
        for (ll_on, lf_on), (obs, exp, E) in results:
            if E <= 0.5 and exp >= 5:
                print(f"  {ll_on}→{lf_on:<12}  obs={obs:>4}  exp={exp:>7.1f}  E={E:.2f}×")
        print()

    # Compare cross-line vs within-line (pre_LL→LL) for key pairs
    pll_ll_enrich = {d: compute_enrichments(pll_ll_pairs[d], pll_marg[d], ll_marg_within[d], total_pll_ll[d])
                     for d in ['A','B']}

    print("=== Cross-line vs within-line (pre_LL→LL) comparison for selected pairs ===\n")
    # Key pairs from exp_444 and discovery
    check_pairs = [('y','d'),('sh','d'),('ol','d'),('ch','d'),('d','d'),
                   ('y','ch'),('d','ch'),('ch','ch'),('sh','ch'),
                   ('qok','ch'),('d','qok'),('ch','qok')]
    for d in ['A','B']:
        print(f"{d}-dialect:")
        print(f"  {'Pair':<12}  {'CL obs':>6}  {'CL E':>7}  {'pLL→LL E':>10}")
        for pair in check_pairs:
            cl_r = cl_enrich[d].get(pair, (0, 0, 0))
            wl_r = pll_ll_enrich[d].get(pair, (0, 0, 0))
            cl_obs, cl_exp, cl_E = cl_r
            wl_obs, wl_exp, wl_E = wl_r
            if max(cl_obs, wl_obs) >= 3 or max(cl_exp, wl_exp) >= 3:
                print(f"  {pair[0]}→{pair[1]:<10}  {cl_obs:>6}  {cl_E:>7.2f}×  {wl_E:>9.2f}×")
        print()

    # Summary: LL onset distribution (what comes at LL most often?)
    print("=== LL onset distribution (cross-line: what words are at LL?) ===")
    for d in ['A','B']:
        total = sum(ll_marg[d].values())
        print(f"\n{d}-dialect (total LL words with recognized onset): {total}")
        for on in TOP_ONSETS:
            cnt = ll_marg[d][on]
            if cnt >= 5:
                print(f"  {on:<6}: {cnt:>4} ({cnt/total*100:.1f}%)")

    print("\n=== LF onset distribution (cross-line: what words are at LF?) ===")
    for d in ['A','B']:
        total = sum(lf_marg[d].values())
        print(f"\n{d}-dialect (total LF words with recognized onset): {total}")
        for on in TOP_ONSETS:
            cnt = lf_marg[d][on]
            if cnt >= 5:
                print(f"  {on:<6}: {cnt:>4} ({cnt/total*100:.1f}%)")

if __name__ == '__main__':
    main()
