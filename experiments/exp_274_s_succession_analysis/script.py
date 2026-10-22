"""
exp_274: H475 — s→s Anti-Self-Succession Analysis

Problem: VMS s→s E2=0.887 (DEPLETED, below 1.0) while simulation produces 4-7× VMS
(exp_261: sim values 4.470-7.203). The 19-metric battery doesn't track s→s.

Questions:
1. Is s→s depletion uniform across sections (grammatical rule) or section-specific (lexical)?
2. What is HHI/null for s→s pairs — random (grammatical) or concentrated (lexical)?
3. Is s→s depletion consistent across A and B dialects?
4. What does the simulation produce for s→s at the MID position level?
5. Is there an onset alternation pattern (s followed by non-s, then s again)?

Analysis:
- Section-stratified s→s E2: stars/herbal/bio/cosmo/pharma/recipes
- HHI for s→s word pairs (top-N coverage, HHI/null ratio)
- s→s E2 by position (MID only vs global)
- Lag analysis for s-onset: E(s|prev=s, lag=1,2,3) — does depletion persist?
- Anti-self-succession check: s→X distribution — what onsets follow s?
- Simulation s→s for both dialects
"""
from pathlib import Path as _RepositoryPath

import os, re, math
from collections import Counter, deque, defaultdict

REPO_DIR   = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
DATA_PATH  = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

ONSET_ORDER = [
    ('qok', 'qok'), ('qot', 'qot'), ('qo', 'qo'), ('cth', 'cth'),
    ('ch', 'ch'), ('sh', 'sh'), ('ok', 'ok'), ('ot', 'ot'), ('ol', 'ol'),
    ('d', 'd'), ('s', 's'), ('y', 'y'), ('k', 'k'), ('t', 't'),
    ('l', 'l'), ('r', 'r'), ('p', 'p'), ('f', 'f'), ('o', 'o'),
]

SECTION_MAP = {
    'herbal': range(1, 66),
    'astro':  list(range(66, 75)) + list(range(103, 117)),
    'cosmo':  range(82, 103),
    'bio':    range(75, 83),
    'recipes': range(103, 117),  # overlaps with astro intentionally skipped
    'stars':  list(range(100, 103)) + list(range(116, 120)),
}

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label
    return 'other'

def folio_base(folio): return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    return 'B' if (stats['edy'] + stats['eedy']) / total >= 0.05 else 'A'

def folio_number(folio_tag):
    base = re.sub(r'[rv]$', '', folio_tag)
    try: return int(re.sub(r'[a-z]', '', base))
    except: return -1

def get_section(fb):
    fnum = folio_number(fb)
    if 1 <= fnum <= 65: return 'herbal'
    if 66 <= fnum <= 74: return 'astro'
    if 75 <= fnum <= 81: return 'bio'
    if 82 <= fnum <= 102: return 'cosmo'
    if 103 <= fnum <= 116: return 'recipes'
    if 116 <= fnum <= 120: return 'stars'
    return 'other'

def parse_vms():
    """Parse all VMS lines with dialect and section labels."""
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1); folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            for w in words:
                folio_word_stats[fb]['total'] += 1
                if w.endswith('eedy'): folio_word_stats[fb]['eedy'] += 1
                elif w.endswith('edy'): folio_word_stats[fb]['edy'] += 1
    folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}

    records = []
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1); locus_code = m.group(3)
            folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
            lc_stripped = locus_code.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words:
                dialect = folio_dialect.get(fb, 'unknown')
                section = get_section(fb)
                records.append({'dialect': dialect, 'section': section, 'fb': fb, 'words': words})
    return records

def compute_bigram_e2(words, x, y):
    """E2(x→y) = P(XY) / (P(X)*P(Y)) across global word sequence."""
    n = len(words)
    if n < 2: return float('nan'), 0
    occ_x = sum(1 for w in words if get_onset(w) == x)
    occ_y = sum(1 for w in words if get_onset(w) == y)
    tb = n - 1
    occ_xy = sum(1 for i in range(tb) if get_onset(words[i])==x and get_onset(words[i+1])==y)
    px = occ_x/n; py = occ_y/n
    pxy = occ_xy/tb if tb>0 else 0
    e2 = pxy/(px*py) if px*py>0 else float('nan')
    return e2, occ_xy

def compute_mid_bigram_e2(lines, x, y):
    """E2(x→y) restricted to MID positions (not LF→MID-first or MID-last→LL)."""
    mid_words = []; mid_pairs = []
    for line in lines:
        mid = line[1:-1] if len(line) > 2 else []
        mid_words.extend(mid)
        for i in range(len(mid)-1):
            mid_pairs.append((get_onset(mid[i]), get_onset(mid[i+1])))
    n = len(mid_words)
    if n < 2: return float('nan'), 0
    occ_x = sum(1 for w in mid_words if get_onset(w)==x)
    occ_y = sum(1 for w in mid_words if get_onset(w)==y)
    occ_xy = sum(1 for (a,b) in mid_pairs if a==x and b==y)
    tb = len(mid_pairs)
    px = occ_x/n; py = occ_y/n
    pxy = occ_xy/tb if tb>0 else 0
    e2 = pxy/(px*py) if px*py>0 else float('nan')
    return e2, occ_xy

def hhi_null_ratio(word_pairs):
    """HHI(observed) / HHI(null)."""
    if not word_pairs: return float('nan')
    n = len(word_pairs)
    pair_ctr = Counter(word_pairs)
    # Observed HHI
    hhi_obs = sum((cnt/n)**2 for cnt in pair_ctr.values())
    # Null HHI: independent draws, P(xy)=P(x)*P(y)
    x_words = [a for a,b in word_pairs]; y_words = [b for a,b in word_pairs]
    x_ctr = Counter(x_words); y_ctr = Counter(y_words)
    n_x = len(x_words); n_y = len(y_words)
    hhi_null = sum((x_ctr[xw]/n_x)**2 for xw in x_ctr) * sum((y_ctr[yw]/n_y)**2 for yw in y_ctr)
    return hhi_obs/hhi_null if hhi_null>0 else float('nan')

def lag_enrichment(words, target_onset, lag):
    """E(target at position i+lag | target at position i)."""
    n = len(words)
    count_x = sum(1 for w in words if get_onset(w)==target_onset)
    count_xy = sum(1 for i in range(n-lag) if get_onset(words[i])==target_onset and get_onset(words[i+lag])==target_onset)
    px = count_x/n if n>0 else 0
    p_xy = count_xy/(n-lag) if n-lag>0 else 0
    e = p_xy/px if px>0 else float('nan')
    return e, count_xy

def analyze_onset(records, dialect, onset_label):
    """Full analysis for a given onset and dialect."""
    print(f"\n{'='*70}")
    print(f"ONSET: {onset_label}  DIALECT: {dialect}")
    print(f"{'='*70}")

    # Filter to dialect
    d_lines = [r['words'] for r in records if r['dialect']==dialect]
    all_words = [w for line in d_lines for w in line]
    n = len(all_words)

    onset_cnt = sum(1 for w in all_words if get_onset(w)==onset_label)
    print(f"  Total words: {n}  {onset_label}-onset: {onset_cnt} ({100*onset_cnt/n:.1f}%)")

    # Section 1: Global E2(s→s)
    e2_global, n_ss = compute_bigram_e2(all_words, onset_label, onset_label)
    print(f"\n  Section 1: Global E2({onset_label}→{onset_label}) = {e2_global:.4f}  (N_pairs={n_ss})")
    if e2_global < 1.0:
        print(f"  DEPLETED (E<1): {onset_label}-onset is followed by non-{onset_label} more than expected")
    else:
        print(f"  ENRICHED (E>1): {onset_label}-onset self-succession higher than expected")

    # Section 2: MID-only E2
    e2_mid, n_ss_mid = compute_mid_bigram_e2(d_lines, onset_label, onset_label)
    print(f"\n  Section 2: MID-only E2({onset_label}→{onset_label}) = {e2_mid:.4f}  (N_mid_pairs={n_ss_mid})")

    # Section 3: Section-stratified E2
    print(f"\n  Section 3: Section-stratified E2({onset_label}→{onset_label})")
    section_records = defaultdict(list)
    for r in records:
        if r['dialect']==dialect:
            section_records[r['section']].extend(r['words'])
    for sec in ['herbal','astro','bio','cosmo','recipes','stars']:
        sec_words = section_records[sec]
        if len(sec_words) < 20: continue
        e2, nxy = compute_bigram_e2(sec_words, onset_label, onset_label)
        s_cnt = sum(1 for w in sec_words if get_onset(w)==onset_label)
        tb = max(1, len(sec_words)-1)
        print(f"    {sec:>10}: E2={e2:.3f}  N={nxy}  n_words={len(sec_words)}  "
              f"s_rate={100*s_cnt/len(sec_words):.1f}%")

    # Section 4: Lag analysis
    print(f"\n  Section 4: Lag enrichment E(lag-1,2,3) for {onset_label}→{onset_label}")
    for lag in [1, 2, 3]:
        e, nxy = lag_enrichment(all_words, onset_label, lag)
        print(f"    Lag-{lag}: E={e:.4f}  N={nxy}")

    # Section 5: HHI/null for s→s pairs
    print(f"\n  Section 5: HHI/null for {onset_label}→{onset_label} word pairs")
    tb = len(all_words)-1
    ss_pairs = [(all_words[i], all_words[i+1]) for i in range(tb)
                if get_onset(all_words[i])==onset_label and get_onset(all_words[i+1])==onset_label]
    if ss_pairs:
        hhi_ratio = hhi_null_ratio(ss_pairs)
        pair_ctr = Counter(ss_pairs)
        top5 = pair_ctr.most_common(5)
        top5_cov = sum(cnt for _,cnt in top5)/len(ss_pairs)
        print(f"    N_pairs={len(ss_pairs)}  HHI/null={hhi_ratio:.3f}  top5_coverage={top5_cov:.3f}")
        print(f"    Top 5 pairs: {top5[:5]}")
        if hhi_ratio < 1.5:
            print(f"    GRAMMATICAL (near-random pairings, HHI/null~1)")
        else:
            print(f"    LEXICAL (concentrated in specific word pairs)")
    else:
        print(f"    No {onset_label}→{onset_label} pairs found")

    # Section 6: What follows s-onset? (s→X distribution)
    print(f"\n  Section 6: {onset_label}→X transition distribution (what follows {onset_label}?)")
    after_s = Counter()
    for i in range(tb):
        if get_onset(all_words[i])==onset_label:
            after_s[get_onset(all_words[i+1])] += 1
    total_after = sum(after_s.values())
    onset_counts = Counter(get_onset(w) for w in all_words)
    if total_after > 0:
        rows = []
        for o, cnt in sorted(after_s.items(), key=lambda x: -x[1])[:8]:
            expected = onset_counts.get(o,0)/n if n>0 else 0
            actual = cnt/total_after
            enr = actual/expected if expected>0 else float('inf')
            rows.append((o, cnt, actual, expected, enr))
        print(f"    {'Onset':>8} {'Count':>6} {'Actual':>8} {'Expected':>9} {'E':>6}")
        for o, cnt, act, exp, enr in rows:
            marker = '*' if enr < 0.5 else ('+' if enr > 1.5 else ' ')
            print(f"    {o:>8} {cnt:>6} {act:>8.3f} {exp:>9.3f} {enr:>6.3f}{marker}")

def main():
    print("Parsing VMS corpus...")
    records = parse_vms()
    total_lines = len(records)
    print(f"  Total lines: {total_lines}")

    # Analyze s→s for both dialects
    for dialect in ['A', 'B']:
        analyze_onset(records, dialect, 's')

    # Also check l→l, p→p, f→f for comparison (are these also depleted or normal?)
    print(f"\n{'='*70}")
    print("COMPARISON: E2 for other potentially-depleted onsets (A-dialect)")
    print(f"{'='*70}")
    a_lines = [r['words'] for r in records if r['dialect']=='A']
    a_words = [w for l in a_lines for w in l]
    for onset_label in ['s', 'l', 'p', 'f', 'k', 't', 'r']:
        e2, nxy = compute_bigram_e2(a_words, onset_label, onset_label)
        cnt = sum(1 for w in a_words if get_onset(w)==onset_label)
        n = len(a_words)
        rate = 100*cnt/n if n>0 else 0
        print(f"  A-dialect {onset_label:>4}: E2={e2:.4f}  N={nxy}  rate={rate:.1f}%  "
              f"{'DEPLETED' if e2<1.0 else 'enriched'}")

    print(f"\n{'='*70}")
    print("COMPARISON: E2 for potentially-depleted onsets (B-dialect)")
    print(f"{'='*70}")
    b_lines = [r['words'] for r in records if r['dialect']=='B']
    b_words = [w for l in b_lines for w in l]
    for onset_label in ['s', 'l', 'p', 'f', 'k', 't', 'r']:
        e2, nxy = compute_bigram_e2(b_words, onset_label, onset_label)
        cnt = sum(1 for w in b_words if get_onset(w)==onset_label)
        n = len(b_words)
        rate = 100*cnt/n if n>0 else 0
        print(f"  B-dialect {onset_label:>4}: E2={e2:.4f}  N={nxy}  rate={rate:.1f}%  "
              f"{'DEPLETED' if e2<1.0 else 'enriched'}")

    # s→X and X→s enrichment for both dialects (what does s tend to follow/precede?)
    print(f"\n{'='*70}")
    print("CROSS-ONSET: What does s tend to follow? (X→s enrichment, A-dialect)")
    print(f"{'='*70}")
    n_a = len(a_words); tb_a = n_a-1
    s_onset_count_a = sum(1 for w in a_words if get_onset(w)=='s')
    px_s_a = s_onset_count_a/n_a if n_a>0 else 0
    before_s = Counter(get_onset(a_words[i]) for i in range(tb_a) if get_onset(a_words[i+1])=='s')
    total_before = sum(before_s.values())
    onset_counts_a = Counter(get_onset(w) for w in a_words)
    print(f"  s-onset frequency: {s_onset_count_a}/{n_a} ({100*px_s_a:.1f}%)")
    print(f"  {'Onset':>8} {'Count':>6} {'X→s_actual':>12} {'X→s_expected':>14} {'E(X→s)':>10}")
    for o, cnt in sorted(before_s.items(), key=lambda x: -x[1])[:8]:
        px_o = onset_counts_a.get(o,0)/n_a
        p_xs = cnt/tb_a
        p_x = px_o
        p_s = px_s_a
        e_xs = p_xs/(p_x*p_s) if p_x*p_s>0 else float('inf')
        print(f"  {o:>8} {cnt:>6} {p_xs:>12.4f} {p_x*p_s:>14.4f} {e_xs:>10.3f}")

if __name__ == '__main__':
    main()
