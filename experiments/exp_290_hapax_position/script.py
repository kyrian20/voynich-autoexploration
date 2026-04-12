"""
exp_290: Hapax Words by Line Position — Are Long-Midfix Hapaxes at LF/LL or MID?
Hypothesis: If template words (frequent, short) are MID copy-buffer products, they should
concentrate at MID positions. If vocabulary-rich words (hapax, long midfix) are generated
by the cipher component, they should be enriched at LF/LL positions.

This tests a key architectural prediction: Mode B architecture predicts:
- MID: copy-buffer words → frequent, short, same onset repeated
- LF/LL: cipher words → potentially more varied, could be longer

Data: eva_zl3b.txt (ZL3b transcription, IVTFF format)
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

def parse_with_position(path, min_len=3, max_len=15):
    """Parse ZL3b with line position: LF=first word, LL=last word, MID=others.
    Also capture word index within line."""
    eva_ok = re.compile(r'^[a-z]+$')

    # Pass 1: classify dialects
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

    folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_stats.items()}

    # Pass 2: extract with position
    tokens = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio = m.group(1).lstrip('+*=&~')
            locus_code = m.group(3)
            fb = folio_base(folio)
            dial = folio_dialect.get(fb, 'unknown')
            if dial not in ('A', 'B'): continue
            lc = locus_code.lstrip('+*=/~&@')
            if not lc.startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s,]', text)
                     if eva_ok.match(w) and min_len <= len(w) <= max_len]
            if not words: continue
            n = len(words)
            for idx, w in enumerate(words):
                if n == 1:
                    pos = 'LL'  # single-word line
                elif idx == 0:
                    pos = 'LF'
                elif idx == n - 1:
                    pos = 'LL'
                else:
                    pos = 'MID'
                tokens.append((w, dial, pos, idx))

    return tokens

def decompose(w):
    onset = get_onset(w)
    olen  = get_onset_len(w)
    suffix = get_suffix(w)
    slen  = len(suffix)
    if slen > 0 and w.endswith(suffix):
        midfix = w[olen:-slen]
    else:
        midfix = w[olen:]
    return {
        'onset': onset, 'suffix': suffix, 'midfix': midfix,
        'wlen': len(w), 'mlen': len(midfix), 'slen': slen,
        'zero_mid': len(midfix) == 0,
    }

def frequency_tier(freq):
    if freq == 1: return 'hapax'
    if freq <= 4: return 'rare'
    if freq <= 19: return 'moderate'
    return 'frequent'


if __name__ == '__main__':
    print("=" * 70)
    print("exp_290: Hapax Words by Line Position")
    print("=" * 70)

    tokens = parse_with_position(ZL3B_PATH)
    print(f"\nTotal tokens: {len(tokens)}")

    # Global word frequency
    global_freq = Counter(w for w, d, p, i in tokens)

    # Build records
    recs = []
    for w, dial, pos, idx in tokens:
        freq = global_freq[w]
        tier = frequency_tier(freq)
        dec  = decompose(w)
        recs.append({'word': w, 'dial': dial, 'pos': pos, 'idx': idx,
                     'freq': freq, 'tier': tier, **dec})

    # 1. Position distribution of hapax vs frequent
    print(f"\n=== Word Position Distribution by Frequency Tier ===")
    print(f"{'Tier':<12} {'N_LF':>7} {'N_MID':>7} {'N_LL':>7} | {'%LF':>5} {'%MID':>5} {'%LL':>5}")
    print('-' * 60)
    for tier in ['hapax', 'rare', 'moderate', 'frequent']:
        recs_t = [r for r in recs if r['tier'] == tier]
        if not recs_t: continue
        n = len(recs_t)
        n_lf  = sum(1 for r in recs_t if r['pos'] == 'LF')
        n_mid = sum(1 for r in recs_t if r['pos'] == 'MID')
        n_ll  = sum(1 for r in recs_t if r['pos'] == 'LL')
        print(f"{tier:<12} {n_lf:>7} {n_mid:>7} {n_ll:>7} | {n_lf/n:>5.1%} {n_mid/n:>5.1%} {n_ll/n:>5.1%}")

    # 2. Midfix length by position
    print(f"\n=== Midfix Length by Position (all words) ===")
    for pos in ['LF', 'MID', 'LL']:
        recs_p = [r for r in recs if r['pos'] == pos]
        wl = np.mean([r['wlen'] for r in recs_p])
        ml = np.mean([r['mlen'] for r in recs_p])
        zm = np.mean([r['zero_mid'] for r in recs_p])
        hapax_rate = sum(1 for r in recs_p if r['tier'] == 'hapax') / len(recs_p)
        print(f"  {pos}: N={len(recs_p):5d}, WLen={wl:.2f}, MLen={ml:.2f}, ZeroMid={zm:.3f}, Hapax%={hapax_rate:.1%}")

    # 3. Midfix length by position AND tier
    print(f"\n=== Midfix Length by Position AND Frequency Tier ===")
    print(f"{'Pos':<5} {'Tier':<12} {'N':>5} {'WLen':>6} {'MLen':>6} {'ZeroMid':>8}")
    print('-' * 50)
    for pos in ['LF', 'MID', 'LL']:
        for tier in ['hapax', 'rare', 'moderate', 'frequent']:
            recs_pt = [r for r in recs if r['pos'] == pos and r['tier'] == tier]
            if len(recs_pt) < 10: continue
            wl = np.mean([r['wlen'] for r in recs_pt])
            ml = np.mean([r['mlen'] for r in recs_pt])
            zm = np.mean([r['zero_mid'] for r in recs_pt])
            print(f"{pos:<5} {tier:<12} {len(recs_pt):>5} {wl:>6.2f} {ml:>6.2f} {zm:>8.3f}")

    # 4. Per dialect
    print(f"\n=== By Dialect: Midfix Length and Hapax Rate per Position ===")
    for dial in ['A', 'B']:
        print(f"\n{dial}-dialect:")
        print(f"  {'Pos':<5} {'WLen':>6} {'MLen':>6} {'ZeroMid':>8} {'Hapax%':>7}")
        for pos in ['LF', 'MID', 'LL']:
            recs_dp = [r for r in recs if r['dial'] == dial and r['pos'] == pos]
            if not recs_dp: continue
            wl = np.mean([r['wlen'] for r in recs_dp])
            ml = np.mean([r['mlen'] for r in recs_dp])
            zm = np.mean([r['zero_mid'] for r in recs_dp])
            hr = sum(1 for r in recs_dp if r['tier'] == 'hapax') / len(recs_dp)
            print(f"  {pos:<5} {wl:>6.2f} {ml:>6.2f} {zm:>8.3f} {hr:>7.1%}")

    # 5. Onset class distribution by position (for detecting if positional grammar
    #    is driven by template words vs hapax words)
    print(f"\n=== Onset Class Distribution: MID vs LF/LL (B-dialect) ===")
    recs_B = [r for r in recs if r['dial'] == 'B']
    top_onsets = ['ch', 'qok', 'sh', 'ok', 'd', 'ot', 'l', 'y', 'o']
    print(f"  {'Onset':<7}", end='')
    for pos in ['LF', 'MID', 'LL']:
        print(f"  {pos:>8}", end='')
    print()
    for onset in top_onsets:
        print(f"  {onset:<7}", end='')
        for pos in ['LF', 'MID', 'LL']:
            recs_p = [r for r in recs_B if r['pos'] == pos]
            n_onset = sum(1 for r in recs_p if r['onset'] == onset)
            rate = n_onset / len(recs_p) if recs_p else 0
            print(f"  {rate:>8.1%}", end='')
        print()

    # 6. Are LF/LL words more hapax-like or frequent-like STRUCTURALLY?
    print(f"\n=== Template Words (ZeroMid) vs Vocabulary Words by Position ===")
    for dial in ['A', 'B']:
        print(f"\n{dial}-dialect:")
        for pos in ['LF', 'MID', 'LL']:
            recs_dp = [r for r in recs if r['dial'] == dial and r['pos'] == pos]
            if len(recs_dp) < 20: continue
            # Split into zero-midfix (template) and has-midfix (vocabulary)
            template = [r for r in recs_dp if r['zero_mid']]
            vocab    = [r for r in recs_dp if not r['zero_mid']]
            frac_templ = len(template)/len(recs_dp)
            templ_hapax = sum(1 for r in template if r['tier'] == 'hapax') / max(1, len(template))
            vocab_hapax  = sum(1 for r in vocab   if r['tier'] == 'hapax') / max(1, len(vocab))
            print(f"  {pos}: template={frac_templ:.1%} (hapax={templ_hapax:.1%}), vocabulary={1-frac_templ:.1%} (hapax={vocab_hapax:.1%})")

    # 7. Key metric: does MID have FEWER hapaxes AND fewer long-midfix words vs LF/LL?
    print(f"\n=== KEY TEST: Hapax Rate and MLen Rate per Position (B-dialect) ===")
    recs_B = [r for r in recs if r['dial'] == 'B']
    for pos in ['LF', 'MID', 'LL']:
        recs_p = [r for r in recs_B if r['pos'] == pos]
        n = len(recs_p)
        hapax_r = sum(1 for r in recs_p if r['tier'] == 'hapax') / n
        long_r  = sum(1 for r in recs_p if r['mlen'] >= 3) / n
        zero_r  = sum(1 for r in recs_p if r['zero_mid']) / n
        wlen    = np.mean([r['wlen'] for r in recs_p])
        mlen    = np.mean([r['mlen'] for r in recs_p])
        print(f"  B-{pos}: N={n:4d}, Hapax={hapax_r:.1%}, MLen>2={long_r:.1%}, ZeroMid={zero_r:.1%}, WLen={wlen:.2f}, MLen={mlen:.2f}")

    print(f"\n=== KEY TEST: Hapax Rate and MLen Rate per Position (A-dialect) ===")
    recs_A = [r for r in recs if r['dial'] == 'A']
    for pos in ['LF', 'MID', 'LL']:
        recs_p = [r for r in recs_A if r['pos'] == pos]
        n = len(recs_p)
        hapax_r = sum(1 for r in recs_p if r['tier'] == 'hapax') / n
        long_r  = sum(1 for r in recs_p if r['mlen'] >= 3) / n
        zero_r  = sum(1 for r in recs_p if r['zero_mid']) / n
        wlen    = np.mean([r['wlen'] for r in recs_p])
        mlen    = np.mean([r['mlen'] for r in recs_p])
        print(f"  A-{pos}: N={n:4d}, Hapax={hapax_r:.1%}, MLen>2={long_r:.1%}, ZeroMid={zero_r:.1%}, WLen={wlen:.2f}, MLen={mlen:.2f}")

    # 8. Are mode B's grammar positions (LF/LL) where the unique words appear?
    print(f"\n=== Fraction of Hapax Tokens by Position vs Expected ===")
    n_total = len(recs)
    for pos in ['LF', 'MID', 'LL']:
        n_pos = sum(1 for r in recs if r['pos'] == pos)
        n_hapax_pos = sum(1 for r in recs if r['pos'] == pos and r['tier'] == 'hapax')
        n_hapax_total = sum(1 for r in recs if r['tier'] == 'hapax')
        print(f"  {pos}: {n_hapax_pos}/{n_pos} hapax tokens = {n_hapax_pos/n_pos:.1%} of {pos} tokens")
        print(f"       ({n_hapax_pos}/{n_hapax_total} = {n_hapax_pos/n_hapax_total:.1%} of all hapax tokens)")
