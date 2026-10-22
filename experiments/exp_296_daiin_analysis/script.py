"""
exp_296: daiin Structural Dominance Analysis (H500)
daiin accounts for 21-33% of all d-onset tokens in both A and B dialects.
No other word type dominates its onset class this strongly.
This experiment investigates: section distribution, positional behavior,
quire/hand stability, structural properties, and comparison to other
high-frequency words.

Data: eva_zl3b.txt
"""
from pathlib import Path as _RepositoryPath

import os, re
import numpy as np
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
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

def folio_base(folio):
    return re.sub(r'[rv][12]?$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

def folio_to_section(folio):
    """Rough section classification by folio number."""
    fb = folio_base(folio)
    # Extract numeric part
    m = re.match(r'f(\d+)', fb)
    if not m: return 'other'
    n = int(m.group(1))
    # Standard Voynich section mapping
    if n <= 66: return 'herbal_astro'   # f1-f66 herbal + astro
    if n <= 84: return 'herbal_bio'     # f67-f84 bio + herbal B
    if n <= 102: return 'text'          # f85-f102 text (recipe-like)
    if n <= 116: return 'pharma_text'   # f103-f116 pharma + text
    return 'other'

def parse_with_full_context(path, min_len=3, max_len=15):
    """Parse with: dialect, position, folio, section, line context."""
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
            section = folio_to_section(folio)
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
                tokens.append({
                    'word': w, 'dial': dial, 'pos': pos,
                    'folio': fb, 'section': section, 'idx': idx, 'n': n,
                })
    return tokens


def analyze_word(tokens, target_word, onset_class, label):
    """Comprehensive analysis of a single high-frequency word vs its onset class peers."""
    toks_all = tokens
    toks_target = [t for t in toks_all if t['word'] == target_word]
    toks_onset  = [t for t in toks_all if get_onset(t['word']) == onset_class]
    n_target = len(toks_target)
    n_onset  = len(toks_onset)

    print(f"\n{'='*60}")
    print(f"  {label}: '{target_word}' (onset={onset_class})")
    print(f"{'='*60}")
    print(f"\n  Total tokens: target={n_target}, onset class={n_onset} ({n_target/n_onset:.1%} of class)")

    # Positional distribution
    pos_target = Counter(t['pos'] for t in toks_target)
    pos_onset  = Counter(t['pos'] for t in toks_onset)
    pos_total  = Counter(t['pos'] for t in toks_all)

    print(f"\n  Positional distribution:")
    print(f"  {'Pos':<6} {'Target_N':>10} {'Target%':>8} {'Onset_rate':>11} {'All_rate':>10} {'Enr(T/onset)':>14}")
    for pos in ['LF', 'MID', 'LL']:
        tc = pos_target.get(pos, 0)
        oc = pos_onset.get(pos, 0)
        ac = pos_total.get(pos, 0)
        t_rate = tc/n_target if n_target > 0 else 0
        o_rate = oc/n_onset if n_onset > 0 else 0
        a_rate = ac/len(toks_all) if toks_all else 0
        enr = t_rate/o_rate if o_rate > 0 else float('inf')
        print(f"  {pos:<6} {tc:>10} {t_rate:>8.1%} {o_rate:>11.1%} {a_rate:>10.1%} {enr:>14.2f}×")

    # Dialect distribution
    dial_target = Counter(t['dial'] for t in toks_target)
    dial_onset  = Counter(t['dial'] for t in toks_onset)
    print(f"\n  Dialect: A={dial_target['A']} ({dial_target['A']/n_target:.1%}), "
          f"B={dial_target['B']} ({dial_target['B']/n_target:.1%})")
    print(f"  Onset class: A={dial_onset['A']} ({dial_onset['A']/n_onset:.1%}), "
          f"B={dial_onset['B']} ({dial_onset['B']/n_onset:.1%})")

    # Section distribution
    section_target = Counter(t['section'] for t in toks_target)
    section_onset  = Counter(t['section'] for t in toks_onset)
    print(f"\n  Section distribution:")
    all_sections = set(section_target.keys()) | set(section_onset.keys())
    for sec in sorted(all_sections):
        tc = section_target.get(sec, 0)
        oc = section_onset.get(sec, 0)
        t_rate = tc/n_target if n_target > 0 else 0
        o_rate = oc/n_onset if n_onset > 0 else 0
        enr = t_rate/o_rate if o_rate > 0 else float('inf')
        print(f"    {sec:<18} target={tc:3d}({t_rate:.1%}) onset={oc:3d}({o_rate:.1%}) enr={enr:.2f}×")

    # Folio diversity: how many folios does target appear in?
    folios_target = Counter(t['folio'] for t in toks_target)
    folios_onset  = Counter(t['folio'] for t in toks_onset)
    print(f"\n  Folio diversity: target in {len(folios_target)} folios, "
          f"onset class in {len(folios_onset)} folios")
    print(f"  Target top folios: {folios_target.most_common(5)}")

    # Contextual neighbors: what word comes BEFORE and AFTER target?
    # Need to reconstruct line context
    # We'll use the token stream — look for same-line adjacency
    # This requires re-parsing with line context; skip for now

    return {'n_target': n_target, 'n_onset': n_onset,
            'pos_target': pos_target, 'dial_target': dial_target,
            'section_target': section_target}


def compare_top_words(tokens, onset_class, label, top_n=10):
    """Compare positional and section behavior of top N words in an onset class."""
    toks_onset = [t for t in tokens if get_onset(t['word']) == onset_class]
    n_onset = len(toks_onset)
    word_counts = Counter(t['word'] for t in toks_onset)
    top_words = [w for w, c in word_counts.most_common(top_n)]

    pos_counts = Counter(t['pos'] for t in toks_onset)

    print(f"\n{'='*70}")
    print(f"  {label}: Top {top_n} Words in {onset_class}-onset Class Positional Behavior")
    print('='*70)
    print(f"\n  {'Word':<14} {'N':>5} {'%class':>7} | {'LF%':>6} {'MID%':>6} {'LL%':>6} | {'LF/MID':>7} {'LL/MID':>7}")
    print('  ' + '-'*70)

    # Global position rates for reference
    lf_rate  = pos_counts.get('LF', 0)  / n_onset
    mid_rate = pos_counts.get('MID', 0) / n_onset
    ll_rate  = pos_counts.get('LL', 0)  / n_onset

    for w in top_words:
        w_toks = [t for t in toks_onset if t['word'] == w]
        n_w = len(w_toks)
        w_pos = Counter(t['pos'] for t in w_toks)
        lf  = w_pos.get('LF', 0)/n_w
        mid = w_pos.get('MID', 0)/n_w
        ll  = w_pos.get('LL', 0)/n_w
        lf_enr  = (lf/mid_rate)/(lf_rate/mid_rate) if mid > 0 and lf_rate > 0 else 0
        ll_enr  = (ll/mid_rate)/(ll_rate/mid_rate) if mid > 0 and ll_rate > 0 else 0
        lf_enr2 = lf / mid if mid > 0 else float('inf')
        ll_enr2 = ll / mid if mid > 0 else float('inf')
        print(f"  {w:<14} {n_w:>5} {n_w/n_onset:>7.1%} | {lf:>6.1%} {mid:>6.1%} {ll:>6.1%} | {lf_enr2:>7.2f}× {ll_enr2:>7.2f}×")

    # Reference: class average
    print(f"  {'[class avg]':<14} {n_onset:>5} {'100%':>7} | {lf_rate:>6.1%} {mid_rate:>6.1%} {ll_rate:>6.1%} | {'1.00':>7} {'1.00':>7}")


if __name__ == '__main__':
    print("=" * 70)
    print("exp_296: daiin Structural Dominance Analysis (H500)")
    print("=" * 70)

    tokens = parse_with_full_context(ZL3B_PATH)
    print(f"\nTotal tokens: {len(tokens)}")

    # Analyze daiin
    analyze_word(tokens, 'daiin', 'd', 'Full corpus')

    # Compare top words in d-onset: does daiin have unique positional behavior?
    for dial in ['A', 'B']:
        toks_d = [t for t in tokens if t['dial'] == dial]
        compare_top_words(toks_d, 'd', f'{dial}-dialect', top_n=10)

    # Also compare: what are the other most-concentrated words across ALL onset classes?
    print(f"\n{'='*70}")
    print("TOP CONCENTRATED WORDS: Fraction of Onset Class Tokens (All Dialects)")
    print("=" * 70)
    print(f"\n  {'Word':<14} {'Onset':>7} {'N':>5} {'%class':>8} {'Hapax_globe':>12}")
    global_freq = Counter(t['word'] for t in tokens)
    for onset in [o for _, o in ONSET_ORDER]:
        toks_onset = [t for t in tokens if get_onset(t['word']) == onset]
        n_onset = len(toks_onset)
        if n_onset < 50: continue
        word_counts = Counter(t['word'] for t in toks_onset)
        top1 = word_counts.most_common(1)
        if top1:
            w, c = top1[0]
            frac = c/n_onset
            is_hapax = 'hapax' if global_freq[w] == 1 else f'freq={global_freq[w]}'
            print(f"  {w:<14} {onset:>7} {c:>5} {frac:>8.1%} {is_hapax:>12}")

    # How does the concentration of daiin compare to top words in other high-freq onset classes?
    print(f"\n  For reference: daiin={global_freq['daiin']} total occurrences")
    print(f"  Other top-concentrated words (A+B combined):")
    all_word_counts = Counter(t['word'] for t in tokens)
    for onset in ['ch', 'sh', 'qok', 'ok', 'ot', 'd']:
        toks_o = [t for t in tokens if get_onset(t['word']) == onset]
        n_o = len(toks_o)
        wc = Counter(t['word'] for t in toks_o)
        top3 = wc.most_common(3)
        print(f"\n  {onset}-onset (N={n_o}):")
        for w, c in top3:
            print(f"    {w:<14} {c:5} ({c/n_o:.1%}) global_freq={all_word_counts[w]}")
