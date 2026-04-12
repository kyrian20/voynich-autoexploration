"""
exp_300: A-Dialect Onset Class Characterization — Parallel to B-Dialect Phase 6

Phase 6 (exp_288–298) characterized B-dialect word-internal structure thoroughly.
This experiment applies the same analysis to A-dialect to identify:
1. Three-tier midfix structure in A-dialect (expected: same taxonomy but longer midfixes)
2. Per-onset-class hapax rate, closed paradigm size, suffix entropy
3. Onset-position mutual information I(onset;pos) in A-dialect
4. Cross-dialect parallel: do A/B share the same onset class taxonomy?

Focus questions:
- Does A-dialect have the same three-category onset taxonomy (template-copying /
  grammar-word LF / line-terminal)?
- What are A-dialect closed paradigm sizes (90% coverage threshold)?
- A-dialect has 0.45% edy-words vs B 19.4% — does this change the onset class ordering?
- F296 found B-dialect l-onset has 78% hapax rate (surprising). What is A-dialect l?

Data: eva_zl3b.txt (A-dialect folios, P-locus lines)
"""

import os, re
import numpy as np
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser('~/voynich-cryptanalyst')
ZL3B_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

ONSET_ORDER = [
    ('qok', 'qok'), ('qot', 'qot'), ('qo', 'qo'), ('cth', 'cth'),
    ('ch', 'ch'), ('sh', 'sh'), ('ok', 'ok'), ('ot', 'ot'), ('ol', 'ol'),
    ('d', 'd'), ('s', 's'), ('y', 'y'), ('k', 'k'), ('t', 't'),
    ('l', 'l'), ('r', 'r'), ('p', 'p'), ('f', 'f'), ('o', 'o'),
]

SUFFIX_LIST = ['eedy','eey','edy','aiin','oldy','oly','ory','ain','ol','or','al','ar',
               'ey','dy','ay','am','an','in','y','n','l','r']

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label
    return 'other'

def get_suffix(w):
    for s in SUFFIX_LIST:
        if w.endswith(s): return s
    return ''

def get_midfix(w):
    onset = None
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix):
            onset = prefix; break
    if onset is None: return None
    suf = get_suffix(w)
    if suf == '': return w[len(onset):]
    body = w[len(onset):]
    if not body.endswith(suf): return body
    return body[:-len(suf)]

def folio_base(folio):
    return re.sub(r'[rv][12]?$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

def parse_dialect_tokens(path, target_dial, min_len=3, max_len=15):
    """Parse tokens for given dialect with position info."""
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

    lines_out = []
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
            if folio_dialect.get(fb, 'unknown') != target_dial: continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s,]', text)
                     if eva_ok.match(w) and min_len <= len(w) <= max_len]
            if words: lines_out.append(words)
    return lines_out


def analyze_onset_class(all_words, lf_words, ll_words, mid_words, onset_label, label, top_n=25):
    """Full characterization of an onset class."""
    aw_o   = [w for w in all_words if get_onset(w) == onset_label]
    lf_o   = [w for w in lf_words if get_onset(w) == onset_label]
    ll_o   = [w for w in ll_words if get_onset(w) == onset_label]
    mid_o  = [w for w in mid_words if get_onset(w) == onset_label]

    n_total = len(aw_o)
    if n_total < 20: return None

    # ZeroMid rate
    midfixes = [get_midfix(w) for w in aw_o if get_midfix(w) is not None]
    zero_mid = sum(1 for m in midfixes if m == '') / len(midfixes) if midfixes else 0
    mean_mlen = np.mean([len(m) for m in midfixes]) if midfixes else 0

    # Suffix distribution
    suffix_counts = Counter(get_suffix(w) for w in aw_o)
    total_suf = sum(suffix_counts.values())
    top1_suf = suffix_counts.most_common(1)[0] if suffix_counts else ('', 0)
    top3_cov = sum(c for _, c in suffix_counts.most_common(3)) / total_suf if total_suf else 0
    suf_h = -sum((c/total_suf)*np.log2(c/total_suf) for _, c in suffix_counts.most_common()
                 if c > 0) if total_suf > 0 else 0

    # Word type stats
    type_counts = Counter(aw_o)
    n_types = len(type_counts)
    n_hapax = sum(1 for w, c in type_counts.items() if c == 1)
    hapax_rate = n_hapax / n_types if n_types else 0
    ttr = n_types / n_total if n_total else 0

    # Closed paradigm: how many types cover 90% of tokens?
    cumsum = 0; n90 = 0
    for w, c in type_counts.most_common():
        cumsum += c; n90 += 1
        if cumsum / n_total >= 0.90: break
    cp90_frac = n90 / n_types if n_types else 0

    # Positional enrichment
    n_all = len(all_words); n_lf = len(lf_words); n_ll = len(ll_words); n_mid = len(mid_words)
    base_rate = n_total / n_all if n_all else 0
    lf_enr = (len(lf_o)/n_lf / base_rate) if n_lf and base_rate else 0
    ll_enr = (len(ll_o)/n_ll / base_rate) if n_ll and base_rate else 0
    mid_enr = (len(mid_o)/n_mid / base_rate) if n_mid and base_rate else 0

    return {
        'onset': onset_label, 'n_total': n_total, 'n_types': n_types,
        'zero_mid': zero_mid, 'mean_mlen': mean_mlen,
        'top1_suf': top1_suf[0], 'top1_suf_frac': top1_suf[1]/total_suf if total_suf else 0,
        'top3_cov': top3_cov, 'suf_h': suf_h,
        'hapax_rate': hapax_rate, 'ttr': ttr,
        'n90_types': n90, 'cp90_frac': cp90_frac,
        'lf_enr': lf_enr, 'll_enr': ll_enr, 'mid_enr': mid_enr,
    }


def mutual_information_onset_pos(all_words, lf_words, ll_words, mid_words, n_shuffle=200):
    """I(onset; position) with null model shuffle."""
    tokens = (
        [(w, 'LF') for w in lf_words] +
        [(w, 'MID') for w in mid_words] +
        [(w, 'LL') for w in ll_words]
    )
    if len(tokens) < 100: return 0, 0, 0

    # Position distribution
    pos_counts = Counter(p for _, p in tokens)
    total = len(tokens)
    h_pos = -sum((c/total)*np.log2(c/total) for c in pos_counts.values() if c > 0)

    # Joint onset-position distribution
    joint = Counter((get_onset(w), p) for w, p in tokens)
    onset_counts = Counter(get_onset(w) for w, _ in tokens)

    def compute_mi(joint, onset_counts, pos_counts, total):
        mi = 0
        for (o, p), count in joint.items():
            if count == 0: continue
            p_joint = count / total
            p_o = onset_counts[o] / total
            p_p = pos_counts[p] / total
            if p_o > 0 and p_p > 0:
                mi += p_joint * np.log2(p_joint / (p_o * p_p))
        return mi

    obs_mi = compute_mi(joint, onset_counts, pos_counts, total)

    # Null model: shuffle positions
    shuffle_mis = []
    words = [w for w, _ in tokens]
    positions = [p for _, p in tokens]
    rng = np.random.default_rng(300000)
    for _ in range(n_shuffle):
        shuf_pos = list(positions); rng.shuffle(shuf_pos)
        shuf_tokens = list(zip(words, shuf_pos))
        shuf_joint = Counter((get_onset(w), p) for w, p in shuf_tokens)
        shuffle_mis.append(compute_mi(shuf_joint, onset_counts, pos_counts, total))

    null_mean = np.mean(shuffle_mis)
    null_std  = np.std(shuffle_mis)
    z_score = (obs_mi - null_mean) / null_std if null_std > 0 else 0
    pct_h_pos = obs_mi / h_pos * 100 if h_pos > 0 else 0
    return obs_mi, z_score, pct_h_pos


if __name__ == '__main__':
    print("=" * 70)
    print("exp_300: A-Dialect Onset Class Characterization")
    print("=" * 70)

    # Parse both dialects
    a_lines = parse_dialect_tokens(ZL3B_PATH, 'A')
    b_lines = parse_dialect_tokens(ZL3B_PATH, 'B')

    print(f"\nA-dialect: {len(a_lines)} lines")
    print(f"B-dialect: {len(b_lines)} lines")

    for dial_label, lines in [('A', a_lines), ('B', b_lines)]:
        print(f"\n{'='*70}")
        print(f"  {dial_label}-DIALECT ONSET CLASS CHARACTERIZATION")
        print('='*70)

        all_words = [w for l in lines for w in l]
        lf_words  = [l[0]  for l in lines if l]
        ll_words  = [l[-1] for l in lines if len(l) > 1]
        mid_words = [w for l in lines for w in l[1:-1] if len(l) > 2]

        print(f"  Total: {len(all_words)} words | LF: {len(lf_words)} | MID: {len(mid_words)} | LL: {len(ll_words)}")

        # Mutual information
        print(f"\n  I(onset; position) analysis ({dial_label}):")
        mi, z, pct = mutual_information_onset_pos(all_words, lf_words, ll_words, mid_words)
        print(f"    I(onset;pos) = {mi:.4f} bits  Z={z:.0f}  ({pct:.1f}% of H(pos))")

        # Per-onset analysis
        results = []
        for prefix, label in ONSET_ORDER:
            r = analyze_onset_class(all_words, lf_words, ll_words, mid_words, label, dial_label)
            if r: results.append(r)

        print(f"\n  {'Onset':<5}  {'N':>5}  {'Types':>5}  {'ZeroMid':>7}  {'MLen':>5}  {'SufH':>5}  "
              f"{'Hapax':>5}  {'CP90':>5}  {'LF×':>5}  {'MID×':>5}  {'LL×':>5}  Top1Suf")
        for r in sorted(results, key=lambda x: -x['n_total']):
            print(f"  {r['onset']:<5}  {r['n_total']:>5}  {r['n_types']:>5}  "
                  f"{r['zero_mid']:>7.1%}  {r['mean_mlen']:>5.2f}  {r['suf_h']:>5.2f}  "
                  f"{r['hapax_rate']:>5.1%}  {r['cp90_frac']:>5.1%}  "
                  f"{r['lf_enr']:>5.2f}  {r['mid_enr']:>5.2f}  {r['ll_enr']:>5.2f}  "
                  f"{r['top1_suf']}/{r['top1_suf_frac']:.1%}")

        # Three-category summary
        template_onsets = [r for r in results if r['mid_enr'] > 1.0 and r['hapax_rate'] < 0.25]
        lf_onsets = [r for r in results if r['lf_enr'] > 2.0]
        ll_onsets = [r for r in results if r['ll_enr'] > 1.5]

        print(f"\n  THREE-CATEGORY TAXONOMY ({dial_label}):")
        print(f"  Template-copying (MID>1× + hapax<25%): {[r['onset'] for r in sorted(template_onsets, key=lambda x: -x['mid_enr'])]}")
        print(f"  Grammar-word LF (LF>2×): {[r['onset'] for r in sorted(lf_onsets, key=lambda x: -x['lf_enr'])]}")
        print(f"  Line-terminal LL (LL>1.5×): {[r['onset'] for r in sorted(ll_onsets, key=lambda x: -x['ll_enr'])]}")

        # Closed paradigm sizes
        print(f"\n  CLOSED PARADIGM SIZES ({dial_label}) — types needed for 90% token coverage:")
        for r in sorted(results, key=lambda x: x['cp90_frac'])[:10]:
            print(f"    {r['onset']:<5}: {r['n90_types']:3d} types ({r['cp90_frac']:5.1%} of {r['n_types']} total)  "
                  f"[hapax={r['hapax_rate']:.1%}]")

    print(f"\n{'='*70}")
    print("CROSS-DIALECT COMPARISON")
    print('='*70)
    print("  Comparing closed paradigm sizes and onset taxonomy across dialects...")
    a_res = {}; b_res = {}
    for dial_label, lines, store in [('A', a_lines, a_res), ('B', b_lines, b_res)]:
        all_words = [w for l in lines for w in l]
        lf_words  = [l[0]  for l in lines if l]
        ll_words  = [l[-1] for l in lines if len(l) > 1]
        mid_words = [w for l in lines for w in l[1:-1] if len(l) > 2]
        for prefix, label in ONSET_ORDER:
            r = analyze_onset_class(all_words, lf_words, ll_words, mid_words, label, dial_label)
            if r: store[label] = r
    print(f"\n  {'Onset':<5}  {'A ZeroMid':>9}  {'B ZeroMid':>9}  {'A CP90%':>7}  {'B CP90%':>7}  {'A Hapax':>7}  {'B Hapax':>7}")
    for prefix, label in ONSET_ORDER:
        ar = a_res.get(label); br = b_res.get(label)
        if ar and br:
            print(f"  {label:<5}  {ar['zero_mid']:>9.1%}  {br['zero_mid']:>9.1%}  "
                  f"{ar['cp90_frac']:>7.1%}  {br['cp90_frac']:>7.1%}  "
                  f"{ar['hapax_rate']:>7.1%}  {br['hapax_rate']:>7.1%}")
