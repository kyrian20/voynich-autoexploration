"""
exp_432: ch→daiin sequential rule (H571)
Is ch the dominant predecessor of daiin in both dialects?
Decompose by position pair (LF→pos1, pos1→pos2, MID_inner, pre_LL→LL).
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

ONSET_ORDER = ['qok','qot','qo','cth','ch','sh','ok','ot','ol',
               'd','s','y','k','t','l','r','p','f','o']

def get_onset(w):
    for o in ONSET_ORDER:
        if w.startswith(o):
            return o
    return 'other'

def folio_base(folio):
    return re.sub(r'[rv]\d*$', '', folio)

def parse_and_classify():
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0})
    raw_lines = []
    with open(ZL3B, encoding='utf-8') as f:
        for raw in f:
            raw = raw.strip()
            if not raw or raw.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', raw)
            if not m: continue
            folio = m.group(1).lstrip('+*=&~')
            ln = int(m.group(2))
            lc = m.group(3).lstrip('+*=/~&')
            if not lc.lstrip('@').startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', raw)
            words = [w for w in re.split(r'[-.\s]', text)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words:
                raw_lines.append((folio, ln, words))
                fb = folio_base(folio)
                for w in words:
                    folio_word_stats[fb]['total'] += 1
                    if w.endswith('edy') or w.endswith('eedy'):
                        folio_word_stats[fb]['edy'] += 1

    dialect = {}
    for fb, stats in folio_word_stats.items():
        if stats['total'] >= 20:
            rate = stats['edy'] / stats['total']
            dialect[fb] = 'B' if rate >= 0.05 else 'A'

    folio_groups = defaultdict(list)
    for folio, ln, words in raw_lines:
        fb = folio_base(folio)
        if fb in dialect:
            folio_groups[(folio, dialect[fb])].append((ln, words))

    cont_by_dialect = {'A': [], 'B': []}
    for (folio, d), flines in folio_groups.items():
        lns = [fl[0] for fl in flines]
        min_ln, max_ln = min(lns), max(lns)
        for ln, words in flines:
            if ln != min_ln and ln != max_ln:
                cont_by_dialect[d].append((folio, ln, words))

    return cont_by_dialect

def get_position_type(i, n):
    """Return position type for word at index i in line of length n."""
    if i == 0: return 'LF'
    if i == 1: return 'pos1'
    if i == n-1: return 'LL'
    if i == n-2: return 'pre_LL'
    return 'MID_inner'

def analyze_ch_daiin(lines, dialect):
    """Analyze ch→daiin coupling with position decomposition."""
    print(f"\n=== {dialect}-dialect ch→daiin analysis ===")
    print(f"Lines: {len(lines)}")

    # Collect all consecutive pairs with position types
    # Position types for pair (w_i, w_{i+1}): type = f(i, i+1, n)
    
    # For daiin at each position: what is the predecessor onset?
    daiin_preds = defaultdict(Counter)  # pos_type → Counter of predecessor onsets
    daiin_counts_by_pos = Counter()  # pos_type → count of daiin occurrences
    
    # Also: for ch-onset at each position, how often is successor = daiin?
    ch_succ = defaultdict(Counter)  # pos_type → Counter of successors
    
    # Overall bigram counting
    pair_counts = Counter()  # (onset1, is_daiin_2) → count
    all_pairs = Counter()  # (onset1, onset2) → count

    for folio, ln, words in lines:
        n = len(words)
        for i in range(n):
            if words[i] == 'daiin':
                pos_type = get_position_type(i, n)
                daiin_counts_by_pos[pos_type] += 1
                if i > 0:
                    pred_onset = get_onset(words[i-1])
                    # Position type for the pair
                    if i == 1: pair_pos = 'LF→pos1'
                    elif i == n-1: pair_pos = 'pre_LL→LL'
                    elif i == 2: pair_pos = 'pos1→pos2'
                    else: pair_pos = 'MID_inner'
                    daiin_preds[pair_pos][pred_onset] += 1

        for i in range(n-1):
            if get_onset(words[i]) == 'ch':
                if i == 0: pair_pos = 'LF→pos1'
                elif i == n-2: pair_pos = 'pre_LL→LL'
                elif i == 1: pair_pos = 'pos1→pos2'
                else: pair_pos = 'MID_inner'
                ch_succ[pair_pos][words[i+1]] += 1

    # Global rates
    total_pairs_global = sum(len(words)-1 for f,l,words in lines)
    total_daiin = sum(1 for f,l,words in lines for w in words if w == 'daiin')
    total_ch = sum(1 for f,l,words in lines for w in words if get_onset(w) == 'ch')
    daiin_rate = total_daiin / sum(len(words) for f,l,words in lines)
    ch_rate = total_ch / sum(len(words) for f,l,words in lines)
    
    print(f"\ndaiin total: {total_daiin}, daiin rate: {daiin_rate:.4f}")
    print(f"ch total: {total_ch}, ch rate: {ch_rate:.4f}")

    # ch→daiin overall
    ch_daiin_pairs = sum(daiin_preds[pp].get('ch', 0) for pp in daiin_preds)
    total_ch_as_pred = sum(1 for f,l,words in lines for i in range(len(words)-1)
                           if get_onset(words[i]) == 'ch')
    expected_ch_daiin = total_ch_as_pred * daiin_rate
    e_ch_daiin = ch_daiin_pairs / expected_ch_daiin if expected_ch_daiin > 0 else 0
    print(f"\nch→daiin overall: N={ch_daiin_pairs}, expected={expected_ch_daiin:.1f}, E={e_ch_daiin:.2f}×")

    # By position pair
    print(f"\nch→daiin by position pair:")
    for pair_pos in ['LF→pos1', 'pos1→pos2', 'MID_inner', 'pre_LL→LL']:
        n_ch_daiin = daiin_preds[pair_pos].get('ch', 0)
        total_daiin_pos = sum(daiin_preds[pair_pos].values())
        n_ch_total_pos = sum(ch_succ[pair_pos].values())
        total_pairs_pos = sum(len(words)-1 for f,l,words in lines)  # approximate
        n_daiin_pos = daiin_counts_by_pos.get(pair_pos.split('→')[1] if '→' in pair_pos else pair_pos, 0)
        frac_ch = n_ch_daiin / total_daiin_pos if total_daiin_pos > 0 else 0
        n_succ_daiin = ch_succ[pair_pos].get('daiin', 0)
        frac_daiin_after_ch = n_succ_daiin / n_ch_total_pos if n_ch_total_pos > 0 else 0
        print(f"  {pair_pos}: ch precedes daiin N={n_ch_daiin}/{total_daiin_pos}={frac_ch:.3f}; "
              f"ch→daiin N={n_succ_daiin}/{n_ch_total_pos}={frac_daiin_after_ch:.3f}")

    # Pre-LL→LL pair is most relevant for A-dialect (A daiin LL-enriched)
    print(f"\nTop predecessors of daiin at pre_LL→LL position:")
    for onset, cnt in daiin_preds['pre_LL→LL'].most_common(8):
        print(f"  {onset}: {cnt}")
    total_preLLLL = sum(daiin_preds['pre_LL→LL'].values())
    ch_count = daiin_preds['pre_LL→LL'].get('ch', 0)
    print(f"  ch fraction: {ch_count}/{total_preLLLL}={ch_count/total_preLLLL:.3f}" if total_preLLLL > 0 else "  no data")

    print(f"\nTop predecessors of daiin at LF→pos1 position:")
    for onset, cnt in daiin_preds['LF→pos1'].most_common(8):
        print(f"  {onset}: {cnt}")
    total_LFpos1 = sum(daiin_preds['LF→pos1'].values())
    ch_count_lf = daiin_preds['LF→pos1'].get('ch', 0)
    print(f"  ch fraction: {ch_count_lf}/{total_LFpos1}={ch_count_lf/total_LFpos1:.3f}" if total_LFpos1 > 0 else "  no data")

    # ch→daiin at pre_LL→LL in detail
    print(f"\nch successor distribution at pre_LL→LL:")
    total_ch_preLLLL = sum(ch_succ['pre_LL→LL'].values())
    for word, cnt in Counter(ch_succ['pre_LL→LL']).most_common(5):
        print(f"  {word}: {cnt}/{total_ch_preLLLL}={cnt/total_ch_preLLLL:.3f}" if total_ch_preLLLL > 0 else "  no data")

def main():
    cont = parse_and_classify()
    for d in ['A', 'B']:
        analyze_ch_daiin(cont[d], d)

if __name__ == '__main__':
    main()
