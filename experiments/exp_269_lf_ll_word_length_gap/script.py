"""
exp_269: H478 — LF/LL Word Length Gap Diagnosis
Why are simulation LF/LL words 0.6–0.9 chars shorter than VMS?

exp_268 showed: simulation LF mean ~4.7-4.9 chars vs VMS LF mean ~5.4-5.7 chars.
Simulation MID matches well (Δ ≈ 0.0-0.1 chars).

Hypotheses for the gap:
1. Onset-suffix co-variation: VMS LF words show specific onset-suffix pairings
   (e.g., y-onset → long suffixes like 'aiin'; d-onset → short suffixes like 'am');
   simulation samples onset and suffix independently, breaking these associations.
2. Midfix region: VMS LF/LL words have intermediate characters between onset and suffix
   not captured by the SUFFIX_PATTERNS. Simulation misses these.
3. Suffix distribution mismatch: simulation uses suffix_GLOBAL for cipher_lf/cipher_ll,
   but VMS LF/LL have different (longer) suffix distributions than global.

This experiment:
1. Measures onset-conditioned suffix length for LF/MID/LL in VMS.
2. Computes expected word length under independent vs joint onset-suffix sampling.
3. Identifies the top (onset, suffix) pairs by position.
4. Checks if using position-specific suffix distribution (vs global) would close the gap.
5. Analyzes midfix region: characters between onset and matched suffix.
"""
from pathlib import Path as _RepositoryPath

import os, re
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

ONSET_ORDER = [
    ('qok', 'qok'), ('qot', 'qot'), ('qo', 'qo'), ('cth', 'cth'),
    ('ch', 'ch'), ('sh', 'sh'), ('ok', 'ok'), ('ot', 'ot'), ('ol', 'ol'),
    ('d', 'd'), ('s', 's'), ('y', 'y'), ('k', 'k'), ('t', 't'),
    ('l', 'l'), ('r', 'r'), ('p', 'p'), ('f', 'f'), ('o', 'o'),
]
SUFFIX_PATTERNS = ['eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy']
# Note: 'other' means none of the above match

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label, len(prefix)
    return 'other', 0

def get_suffix(w):
    for suf in SUFFIX_PATTERNS:
        if w.endswith(suf): return suf
    return 'other'

def get_midfix(w):
    """Return the portion between onset and suffix."""
    label, onset_len = get_onset(w)
    suf = get_suffix(w)
    if suf == 'other':
        return w[onset_len:]  # everything after onset (no recognizable suffix)
    return w[onset_len:-len(suf)]  # middle region

def folio_base(folio): return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    return 'B' if (stats['edy'] + stats['eedy']) / total >= 0.05 else 'A'

def parse_vms():
    """Parse VMS into (dialect, position, word) records."""
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
            dialect = folio_dialect.get(fb, 'unknown')
            if dialect not in ('A', 'B'): continue
            lc_stripped = locus_code.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words: continue
            for i, w in enumerate(words):
                if i == 0: pos = 'LF'
                elif i == len(words)-1: pos = 'LL'
                else: pos = 'MID'
                records.append((dialect, pos, w))

    return records

def mean(lst):
    return sum(lst)/len(lst) if lst else 0.0

def main():
    print("Parsing VMS corpus...")
    records = parse_vms()
    print(f"  Total records: {len(records)}")

    for dialect in ['A', 'B']:
        print(f"\n{'='*70}")
        print(f"DIALECT: {dialect}")
        print(f"{'='*70}")
        dialect_records = [(p, w) for d, p, w in records if d == dialect]

        # Stratify by position
        by_pos = defaultdict(list)
        for pos, w in dialect_records:
            by_pos[pos].append(w)

        # ─── 1. Mean word length by position ───
        print("\n1. Mean word length by position:")
        for pos in ['LF', 'MID', 'LL']:
            ws = by_pos[pos]
            print(f"  {pos}: mean={mean([len(w) for w in ws]):.3f}  N={len(ws)}")

        # ─── 2. Onset-conditioned word length ───
        print("\n2. Onset-conditioned mean word length:")
        for pos in ['LF', 'MID', 'LL']:
            ws = by_pos[pos]
            onset_lengths = defaultdict(list)
            for w in ws:
                o, _ = get_onset(w)
                onset_lengths[o].append(len(w))
            # Filter 'other' onset and show top onsets
            top = sorted([(o, ls) for o, ls in onset_lengths.items() if o != 'other'],
                         key=lambda x: -len(x[1]))[:10]
            print(f"  {pos}:")
            for o, ls in top:
                print(f"    {o:>5}: mean={mean(ls):.3f}  N={len(ls)}")

        # ─── 3. Suffix distribution by position ───
        print("\n3. Suffix distribution by position (top suffixes):")
        for pos in ['LF', 'MID', 'LL']:
            ws = by_pos[pos]
            suf_ctr = Counter(get_suffix(w) for w in ws)
            total = len(ws)
            print(f"  {pos} (N={total}):")
            for suf, cnt in suf_ctr.most_common(8):
                print(f"    {suf:>6}: {cnt/total*100:5.1f}%  N={cnt}  mean_len_in_VMS={mean([len(w) for w in ws if get_suffix(w)==suf]):.2f}")

        # ─── 4. Expected word length: independent vs actual ───
        print("\n4. Word length decomposition: expected under independent sampling vs actual")
        print("  (Shows whether onset-suffix co-variation explains length gap)")
        for pos in ['LF', 'MID', 'LL']:
            ws = by_pos[pos]
            total = len(ws)
            # Actual mean
            actual_mean = mean([len(w) for w in ws])
            # Build onset marginal and suffix marginal
            onset_counts = Counter()
            suffix_counts = Counter()
            for w in ws:
                o, _ = get_onset(w)
                s = get_suffix(w)
                if o != 'other': onset_counts[o] += 1
                suffix_counts[s] += 1
            # Mean onset length under marginal
            onset_total = sum(onset_counts.values())
            mean_onset_len = sum(
                sum(len(prefix) for prefix, label in ONSET_ORDER if label == o) * cnt
                for o, cnt in onset_counts.items()
            ) / onset_total if onset_total > 0 else 0
            # Actually, onset label → prefix length (just use first match)
            onset_label_to_len = {label: len(prefix) for prefix, label in ONSET_ORDER}
            mean_onset_len = mean(
                [onset_label_to_len.get(o, 0) for o in onset_counts.elements()]
            )
            # Mean suffix length under marginal (treating 'other' as the typical remainder)
            # For 'other': use actual remaining length after onset
            other_remainders = []
            for w in ws:
                o, ol = get_onset(w)
                s = get_suffix(w)
                if s == 'other':
                    other_remainders.append(len(w) - ol)
            mean_other_len = mean(other_remainders) if other_remainders else 3.0
            suffix_label_to_len = {s: len(s) for s in SUFFIX_PATTERNS}
            suffix_label_to_len['other'] = mean_other_len
            mean_suffix_len = mean(
                [suffix_label_to_len.get(s, 3.0) for s in suffix_counts.elements()]
            )
            # Expected under independence: mean_onset + mean_suffix
            # (+ bridge for edy/eedy — mean bridge len ≈ 1.5 chars)
            edy_rate = (suffix_counts.get('edy', 0) + suffix_counts.get('eedy', 0)) / total
            expected_indep = mean_onset_len + mean_suffix_len + edy_rate * 1.5  # bridge for edy
            print(f"  {pos}: actual={actual_mean:.3f}  expected_indep={expected_indep:.3f}  "
                  f"gap={actual_mean-expected_indep:.3f}")
            print(f"         mean_onset_len={mean_onset_len:.3f}  mean_suffix_len={mean_suffix_len:.3f}  edy_rate={edy_rate:.3f}")

        # ─── 5. Midfix region analysis ───
        print("\n5. Midfix region (characters between onset and suffix):")
        for pos in ['LF', 'MID', 'LL']:
            ws = by_pos[pos]
            midfixes = [get_midfix(w) for w in ws]
            midfix_lens = [len(m) for m in midfixes]
            midfix_ctr = Counter(m for m in midfixes if m)
            print(f"  {pos}: mean_midfix_len={mean(midfix_lens):.3f}  "
                  f"empty_frac={sum(1 for m in midfixes if not m)/len(midfixes)*100:.1f}%")
            top_mf = midfix_ctr.most_common(10)
            if top_mf:
                print(f"    Top midfixes: {', '.join(f'{m}({n})' for m, n in top_mf[:8])}")

        # ─── 6. Top word types by position ───
        print("\n6. Top 15 word types by position (with length):")
        for pos in ['LF', 'MID', 'LL']:
            ws = by_pos[pos]
            top_words = Counter(ws).most_common(15)
            print(f"  {pos}:")
            for w, cnt in top_words:
                o, _ = get_onset(w); s = get_suffix(w); mf = get_midfix(w)
                print(f"    {w:15s} ({len(w)}) onset={o:5} suf={s:6} mid='{mf}'  freq={cnt}")

        # ─── 7. Expected word length if suffix were position-specific ───
        print("\n7. Suffix mean length: global vs LF vs LL vs MID")
        all_ws = by_pos['LF'] + by_pos['MID'] + by_pos['LL']
        suf_ctr_global = Counter(get_suffix(w) for w in all_ws)
        global_total = len(all_ws)
        # Compute mean suffix length of each suffix
        suffix_actual_lens = {}
        for suf in SUFFIX_PATTERNS + ['other']:
            words_with_suf = [w for w in all_ws if get_suffix(w) == suf]
            if words_with_suf:
                if suf == 'other':
                    lens = [len(w) - onset_label_to_len.get(get_onset(w)[0], 0) for w in words_with_suf]
                else:
                    lens = [len(suf)] * len(words_with_suf)
                suffix_actual_lens[suf] = mean(lens)
        print(f"  Suffix  | global% | LF%  | MID% | LL%  | len")
        for suf in SUFFIX_PATTERNS + ['other']:
            g_pct = suf_ctr_global.get(suf, 0) / global_total * 100
            lf_pct = Counter(get_suffix(w) for w in by_pos['LF']).get(suf, 0) / len(by_pos['LF']) * 100
            mid_pct = Counter(get_suffix(w) for w in by_pos['MID']).get(suf, 0) / len(by_pos['MID']) * 100
            ll_pct = Counter(get_suffix(w) for w in by_pos['LL']).get(suf, 0) / len(by_pos['LL']) * 100
            sl = suffix_actual_lens.get(suf, 0)
            print(f"  {suf:6} |  {g_pct:5.1f}% | {lf_pct:4.1f}% | {mid_pct:4.1f}% | {ll_pct:4.1f}% | {sl:.1f}")

        # ─── 8. Simulation-equivalent expected length using global suffix ───
        print("\n8. Why simulation produces different LF/LL lengths:")
        print("  (Using global suffix distribution + position onset distribution)")
        global_suf_dist = {s: n/global_total for s, n in suf_ctr_global.items()}
        for pos in ['LF', 'MID', 'LL']:
            ws = by_pos[pos]
            onset_counts_pos = Counter()
            for w in ws:
                o, _ = get_onset(w)
                if o != 'other': onset_counts_pos[o] += 1
            oc_total = sum(onset_counts_pos.values())
            mean_onset_pos = mean([onset_label_to_len.get(o, 0) for o in onset_counts_pos.elements()])
            # Expected word length using global suffix distribution
            global_suffix_len = sum(
                suffix_actual_lens.get(s, 3.0) * p for s, p in global_suf_dist.items()
            )
            # edy bridge
            global_edy_rate = (global_suf_dist.get('edy', 0) + global_suf_dist.get('eedy', 0))
            expected_sim = mean_onset_pos + global_suffix_len + global_edy_rate * 1.5
            actual = mean([len(w) for w in ws])
            print(f"  {pos}: actual={actual:.3f}  sim_predicted={expected_sim:.3f}  Δ={actual-expected_sim:.3f}")
            print(f"         mean_onset={mean_onset_pos:.3f}  global_suffix_mean={global_suffix_len:.3f}")

    print("\nDone.")

if __name__ == '__main__':
    main()
