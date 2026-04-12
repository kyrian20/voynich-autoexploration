"""
exp_293: Onset Class Positional Grammar — Do Sparse-Midfix Classes Show Stronger Positional Enrichment?
H499: Sparse-template onset classes (qok, ok, ot, cth — ZeroMid 67-78%) should show weaker
positional enrichment because they are template-like (copy-buffer output). Rich-midfix classes
(y, o, l — ZeroMid 1-12%) should show stronger positional enrichment because they are
grammar-word classes driven by the cipher component.

This operationalizes the Mode B architectural prediction: copy-buffer outputs (sparse/template)
are position-agnostic, while cipher outputs (rich/grammar) are position-specific.

Also tests H493: formal positional entropy conditioned on onset class.

Data: eva_zl3b.txt
"""

import os, re
import numpy as np
from collections import Counter, defaultdict
from math import log2

REPO_DIR  = os.path.expanduser('~/voynich-cryptanalyst')
ZL3B_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

ONSET_ORDER = [
    ('qok', 'qok'), ('qot', 'qot'), ('qo', 'qo'), ('cth', 'cth'),
    ('ch', 'ch'), ('sh', 'sh'), ('ok', 'ok'), ('ot', 'ot'), ('ol', 'ol'),
    ('d', 'd'), ('s', 's'), ('y', 'y'), ('k', 'k'), ('t', 't'),
    ('l', 'l'), ('r', 'r'), ('p', 'p'), ('f', 'f'), ('o', 'o'),
]
SUFFIX_LIST = [
    'eedy', 'eey', 'edy', 'aiin', 'oldy', 'oly', 'ory',
    'ain', 'ol', 'or', 'al', 'ar', 'ey', 'dy', 'ay',
    'am', 'an', 'in', 'y', 'n', 'l', 'r',
]

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label
    return 'other'

def get_onset_len(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return len(prefix)
    return 0

def get_suffix(w):
    for s in SUFFIX_LIST:
        if w.endswith(s) and len(w) > len(s):
            return s
    return ''

def folio_base(folio):
    return re.sub(r'[rv][12]?$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

def entropy(counts):
    total = sum(counts.values())
    if total == 0: return 0.0
    return -sum((c/total)*log2(c/total) for c in counts.values() if c > 0)

def parse_with_position(path, min_len=3, max_len=15):
    """Two-pass: classify dialects, then extract tokens with position."""
    eva_ok = re.compile(r'^[a-z]+$')
    folio_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio = m.group(1).lstrip('+*=&~')
            fb = folio_base(folio)
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s,]', text)
                     if eva_ok.match(w) and min_len <= len(w) <= max_len]
            for w in words:
                folio_stats[fb]['total'] += 1
                if w.endswith('eedy'): folio_stats[fb]['eedy'] += 1
                elif w.endswith('edy'): folio_stats[fb]['edy'] += 1
    folio_dialect = {fb: classify_dialect(s) for fb, s in folio_stats.items()}

    tokens = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio = m.group(1).lstrip('+*=&~')
            lc = m.group(3).lstrip('+*=/~&@')
            if not lc.startswith('P'): continue
            fb = folio_base(folio)
            dial = folio_dialect.get(fb, 'unknown')
            if dial not in ('A', 'B'): continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s,]', text)
                     if eva_ok.match(w) and min_len <= len(w) <= max_len]
            if not words: continue
            n = len(words)
            for idx, w in enumerate(words):
                if n == 1: pos = 'LL'
                elif idx == 0: pos = 'LF'
                elif idx == n - 1: pos = 'LL'
                else: pos = 'MID'
                olen = get_onset_len(w)
                suf  = get_suffix(w)
                slen = len(suf)
                mfix = w[olen:-slen] if slen > 0 else w[olen:]
                tokens.append({
                    'word': w, 'dial': dial, 'pos': pos,
                    'onset': get_onset(w),
                    'mlen': len(mfix),
                    'zero_mid': len(mfix) == 0,
                    'suffix': suf,
                })
    return tokens

def positional_enrichment(tokens, dial, label):
    """
    For each onset class, compute:
    1. Zero-midfix rate (template-ness)
    2. LF enrichment (LF_rate / MID_rate)
    3. LL enrichment (LL_rate / MID_rate)
    4. Positional specificity: how concentrated is this class in its preferred position?
    5. Within-onset positional entropy: how uniformly spread across LF/MID/LL?
    """
    toks = [t for t in tokens if t['dial'] == dial]

    # Onset class zero-midfix rates
    onset_zm = defaultdict(lambda: {'zm': 0, 'total': 0})
    pos_onset = defaultdict(lambda: Counter())
    pos_total = Counter()

    for t in toks:
        onset = t['onset']
        pos = t['pos']
        onset_zm[onset]['total'] += 1
        if t['zero_mid']: onset_zm[onset]['zm'] += 1
        pos_onset[pos][onset] += 1
        pos_total[pos] += 1

    # Compute enrichment ratios
    print(f"\n=== {label}: Onset Class Positional Grammar ===")
    print(f"  Total tokens: LF={pos_total['LF']}, MID={pos_total['MID']}, LL={pos_total['LL']}")
    print(f"\n  {'Onset':<7} {'ZeroMid%':>9} {'Tier':>8} | {'LF_rate':>8} {'MID_rate':>9} {'LL_rate':>9} | {'LF/MID':>7} {'LL/MID':>7} | {'PosH':>6}")
    print('  ' + '-'*85)

    # Sort by zero-midfix rate descending (sparse → rich)
    onset_list = sorted(onset_zm.keys(),
                        key=lambda x: -onset_zm[x]['zm']/max(onset_zm[x]['total'],1))

    results = {}
    for onset in onset_list:
        if onset_zm[onset]['total'] < 30: continue
        zm_rate = onset_zm[onset]['zm'] / onset_zm[onset]['total']

        # Tier classification (from exp_288)
        if zm_rate >= 0.60: tier = 'sparse'
        elif zm_rate >= 0.35: tier = 'moderate'
        else: tier = 'rich'

        lf_r  = pos_onset['LF'][onset]  / pos_total['LF']
        mid_r = pos_onset['MID'][onset] / pos_total['MID']
        ll_r  = pos_onset['LL'][onset]  / pos_total['LL']

        lf_enr = lf_r / mid_r if mid_r > 0 else float('inf')
        ll_enr = ll_r / mid_r if mid_r > 0 else float('inf')

        # Within-onset positional entropy: how uniformly spread is THIS onset class?
        # P(pos | onset) distribution
        onset_total = pos_onset['LF'][onset] + pos_onset['MID'][onset] + pos_onset['LL'][onset]
        if onset_total > 0:
            p_lf  = pos_onset['LF'][onset]  / onset_total
            p_mid = pos_onset['MID'][onset] / onset_total
            p_ll  = pos_onset['LL'][onset]  / onset_total
            pos_h = -sum(p*log2(p) for p in [p_lf, p_mid, p_ll] if p > 0)
        else:
            pos_h = 0.0

        # Overall position distribution for reference
        n_total = pos_total['LF'] + pos_total['MID'] + pos_total['LL']
        p_lf_base  = pos_total['LF']  / n_total
        p_mid_base = pos_total['MID'] / n_total
        p_ll_base  = pos_total['LL']  / n_total
        base_h = -sum(p*log2(p) for p in [p_lf_base, p_mid_base, p_ll_base] if p > 0)

        print(f"  {onset:<7} {zm_rate:>9.1%} {tier:>8} | {lf_r:>8.2%} {mid_r:>9.2%} {ll_r:>9.2%} | {lf_enr:>7.2f}× {ll_enr:>7.2f}× | {pos_h:>6.3f}")
        results[onset] = {
            'zm_rate': zm_rate, 'tier': tier,
            'lf_r': lf_r, 'mid_r': mid_r, 'll_r': ll_r,
            'lf_enr': lf_enr, 'll_enr': ll_enr, 'pos_h': pos_h,
        }

    print(f"\n  (Reference: base position H if all onsets uniformly distributed = {base_h:.3f})")

    # Summary: sparse vs rich tier comparison
    sparse = [r for o, r in results.items() if r['tier'] == 'sparse']
    moderate = [r for o, r in results.items() if r['tier'] == 'moderate']
    rich = [r for o, r in results.items() if r['tier'] == 'rich']

    print(f"\n  === Tier Summary: Max Enrichment and Mean Positional H ===")
    print(f"  {'Tier':<10} {'N':>3} {'MeanPosH':>10} {'MeanMaxEnr':>12} {'MeanZeroMid':>12}")
    for tier_name, tier_list in [('sparse', sparse), ('moderate', moderate), ('rich', rich)]:
        if not tier_list: continue
        mean_h  = np.mean([r['pos_h'] for r in tier_list])
        mean_enr = np.mean([max(r['lf_enr'], r['ll_enr']) for r in tier_list
                            if r['lf_enr'] != float('inf') and r['ll_enr'] != float('inf')])
        mean_zm = np.mean([r['zm_rate'] for r in tier_list])
        print(f"  {tier_name:<10} {len(tier_list):>3} {mean_h:>10.3f} {mean_enr:>12.2f}× {mean_zm:>12.1%}")

    return results, base_h


def positional_entropy_by_onset(tokens, dial, label):
    """
    H493: Formal positional entropy test.
    For each onset class, compute H(position | onset_class).
    Compare to marginal H(position).
    Mutual information I(onset; position).
    """
    toks = [t for t in tokens if t['dial'] == dial]

    # Build joint distribution P(onset, pos)
    joint = Counter()
    onset_marginal = Counter()
    pos_marginal = Counter()
    n = 0

    for t in toks:
        joint[(t['onset'], t['pos'])] += 1
        onset_marginal[t['onset']] += 1
        pos_marginal[t['pos']] += 1
        n += 1

    # Mutual information I(onset; position)
    mi = 0.0
    for (onset, pos), count in joint.items():
        p_joint = count / n
        p_onset = onset_marginal[onset] / n
        p_pos   = pos_marginal[pos] / n
        if p_joint > 0 and p_onset > 0 and p_pos > 0:
            mi += p_joint * log2(p_joint / (p_onset * p_pos))

    h_pos = entropy(pos_marginal)
    h_onset = entropy(onset_marginal)

    # H(pos | onset): conditional entropy
    h_pos_given_onset = h_pos - mi

    # Fraction of positional entropy explained by onset class
    frac_explained = mi / h_pos if h_pos > 0 else 0

    print(f"\n  {label}: Positional Entropy Analysis")
    print(f"    H(position) = {h_pos:.4f} bits")
    print(f"    H(onset)    = {h_onset:.4f} bits")
    print(f"    I(onset;pos)= {mi:.4f} bits ({frac_explained:.1%} of H(position))")
    print(f"    H(pos|onset)= {h_pos_given_onset:.4f} bits")

    # Null model: shuffle onset assignments, measure MI
    np.random.seed(293)
    onsets_arr = [t['onset'] for t in toks]
    pos_arr    = [t['pos']   for t in toks]
    null_mis = []
    for _ in range(200):
        shuffled = np.random.permutation(onsets_arr)
        j = Counter(zip(shuffled, pos_arr))
        m_null = Counter(shuffled)
        mi_null = 0.0
        for (onset, pos), count in j.items():
            p_joint = count / n
            p_o = m_null[onset] / n
            p_p = pos_marginal[pos] / n
            if p_joint > 0 and p_o > 0 and p_p > 0:
                mi_null += p_joint * log2(p_joint / (p_o * p_p))
        null_mis.append(mi_null)
    null_mean = np.mean(null_mis)
    null_std  = np.std(null_mis)
    z = (mi - null_mean) / null_std if null_std > 0 else 0
    print(f"    Null model MI: {null_mean:.4f} ± {null_std:.4f}  Z = {z:.1f}")

    return mi, h_pos, frac_explained


def top_lf_ll_words_by_onset(tokens, dial, label):
    """Show the top LF and LL words per onset class — what specifically drives the enrichment?"""
    toks = [t for t in tokens if t['dial'] == dial]

    lf_counts = defaultdict(Counter)  # onset -> {word: count}
    mid_counts = defaultdict(Counter)
    ll_counts  = defaultdict(Counter)

    for t in toks:
        if t['pos'] == 'LF':  lf_counts[t['onset']][t['word']] += 1
        elif t['pos'] == 'MID': mid_counts[t['onset']][t['word']] += 1
        elif t['pos'] == 'LL':  ll_counts[t['onset']][t['word']] += 1

    print(f"\n=== {label}: Top LF/LL Words by Onset Class (LF-enriched onsets) ===")
    # Focus on LF-enriched onset classes
    lf_enriched_onsets = ['p', 's', 't', 'y', 'd']
    for onset in lf_enriched_onsets:
        n_lf  = sum(lf_counts[onset].values())
        n_mid = sum(mid_counts[onset].values())
        n_ll  = sum(ll_counts[onset].values())
        if n_lf < 5: continue
        print(f"\n  {onset}-onset (LF={n_lf}, MID={n_mid}, LL={n_ll}):")
        # Top LF words
        top_lf = lf_counts[onset].most_common(5)
        for w, c in top_lf:
            mid_c = mid_counts[onset].get(w, 0)
            ll_c  = ll_counts[onset].get(w, 0)
            print(f"    LF-top: {w:12} LF={c:3d} MID={mid_c:3d} LL={ll_c:3d}")

    print(f"\n=== {label}: Top MID Words by Onset Class (MID-enriched onsets) ===")
    mid_enriched_onsets = ['ch', 'sh', 'ok', 'ot', 'qok']
    for onset in mid_enriched_onsets:
        n_lf  = sum(lf_counts[onset].values())
        n_mid = sum(mid_counts[onset].values())
        n_ll  = sum(ll_counts[onset].values())
        if n_mid < 5: continue
        print(f"\n  {onset}-onset (LF={n_lf}, MID={n_mid}, LL={n_ll}):")
        top_mid = mid_counts[onset].most_common(5)
        for w, c in top_mid:
            lf_c = lf_counts[onset].get(w, 0)
            ll_c = ll_counts[onset].get(w, 0)
            print(f"    MID-top: {w:12} LF={lf_c:3d} MID={c:3d} LL={ll_c:3d}")


if __name__ == '__main__':
    print("=" * 70)
    print("exp_293: Onset Class Positional Grammar (H499 + H493)")
    print("=" * 70)

    tokens = parse_with_position(ZL3B_PATH)
    print(f"\nTotal tokens: {len(tokens)}")

    # Main analysis per dialect
    for dial in ['A', 'B']:
        label = f"{dial}-dialect"
        results, base_h = positional_enrichment(tokens, dial, label)
        positional_entropy_by_onset(tokens, dial, label)
        top_lf_ll_words_by_onset(tokens, dial, label)

    # Cross-dialect comparison: does positional grammar DIFFER between A and B?
    print(f"\n{'='*70}")
    print("CROSS-DIALECT ONSET ENRICHMENT COMPARISON")
    print("=" * 70)
    print(f"\n  {'Onset':<7} {'A_LF/MID':>10} {'B_LF/MID':>10} | {'A_LL/MID':>10} {'B_LL/MID':>10}")
    print('  ' + '-'*55)

    toks_A = [t for t in tokens if t['dial'] == 'A']
    toks_B = [t for t in tokens if t['dial'] == 'B']

    def enrichment_by_onset(toks):
        pos_onset = defaultdict(Counter)
        pos_total = Counter()
        for t in toks:
            pos_onset[t['pos']][t['onset']] += 1
            pos_total[t['pos']] += 1
        enr = {}
        all_onsets = set(pos_onset['LF'].keys()) | set(pos_onset['MID'].keys()) | set(pos_onset['LL'].keys())
        for onset in all_onsets:
            lf  = pos_onset['LF'][onset]  / pos_total['LF']
            mid = pos_onset['MID'][onset] / pos_total['MID']
            ll  = pos_onset['LL'][onset]  / pos_total['LL']
            enr[onset] = {'lf': lf/mid if mid>0 else float('inf'), 'll': ll/mid if mid>0 else float('inf')}
        return enr

    enr_A = enrichment_by_onset(toks_A)
    enr_B = enrichment_by_onset(toks_B)

    all_onsets = set(enr_A.keys()) | set(enr_B.keys())
    # Sort by B LF enrichment
    sorted_onsets = sorted(all_onsets,
        key=lambda x: -enr_B.get(x, {}).get('lf', 0)
        if enr_B.get(x, {}).get('lf', float('inf')) != float('inf') else 0)

    for onset in sorted_onsets:
        a_lf = enr_A.get(onset, {}).get('lf', 0)
        b_lf = enr_B.get(onset, {}).get('lf', 0)
        a_ll = enr_A.get(onset, {}).get('ll', 0)
        b_ll = enr_B.get(onset, {}).get('ll', 0)
        if max(a_lf, b_lf) < 0.1: continue  # skip very rare
        if a_lf == float('inf') or b_lf == float('inf'): continue
        print(f"  {onset:<7} {a_lf:>10.2f}× {b_lf:>10.2f}× | {a_ll:>10.2f}× {b_ll:>10.2f}×")
