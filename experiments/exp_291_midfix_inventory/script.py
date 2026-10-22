"""
exp_291: Midfix Character Inventory
Exploratory: What characters appear in VMS midfixes vs onsets vs suffixes?
Are midfixes dominated by vowel-like chars, or do they use the full EVA alphabet?

This directly characterizes the internal zone structure of VMS words at the
character level — the question exp_008 (Stolfi crust stripping) couldn't answer.

Data: eva_zl3b.txt (ZL3b transcription)
"""
from pathlib import Path as _RepositoryPath

import os, re
import numpy as np
from collections import Counter, defaultdict
from math import log2

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

def parse_both_dialects(path, min_len=3, max_len=15):
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

    words_A, words_B = [], []
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
            target = words_A if dial == 'A' else words_B
            target.extend(words)
    return words_A, words_B

def zone_chars(words):
    """Extract characters per zone: onset, midfix, suffix."""
    onset_chars = Counter()
    midfix_chars = Counter()
    suffix_chars = Counter()
    midfix_seqs  = Counter()  # common midfix subsequences
    zero_mid_count = 0
    has_mid_count  = 0

    for w in words:
        olen = get_onset_len(w)
        body = w[olen:]
        suf  = get_suffix(w)
        slen = len(suf)
        if slen > 0 and w.endswith(suf):
            midfix = w[olen:-slen]
        else:
            midfix = body

        # Count onset chars
        for c in w[:olen]:
            onset_chars[c] += 1
        # Count suffix chars
        for c in suf:
            suffix_chars[c] += 1
        # Count midfix chars
        if midfix:
            has_mid_count += 1
            for c in midfix:
                midfix_chars[c] += 1
            midfix_seqs[midfix] += 1
        else:
            zero_mid_count += 1

    return onset_chars, midfix_chars, suffix_chars, midfix_seqs, zero_mid_count, has_mid_count

def show_char_inventory(label, onset_c, midfix_c, suffix_c):
    """Show which characters appear in each zone and at what rate."""
    all_chars = sorted(set(onset_c) | set(midfix_c) | set(suffix_c))
    onset_tot  = sum(onset_c.values())
    midfix_tot = sum(midfix_c.values())
    suffix_tot = sum(suffix_c.values())

    print(f"\n=== {label}: Character Inventory by Zone ===")
    print(f"  Zone totals: onset={onset_tot}, midfix={midfix_tot}, suffix={suffix_tot}")
    print(f"\n  {'Char':<5} {'Onset%':>7} {'Midfix%':>8} {'Suffix%':>8} | {'Midfix':>7} dom | notes")
    print('  ' + '-'*65)

    # Sort by midfix rate
    for c in sorted(all_chars, key=lambda x: -midfix_c.get(x,0)/max(midfix_tot,1)):
        op = onset_c.get(c,0)/max(onset_tot,1)
        mp = midfix_c.get(c,0)/max(midfix_tot,1)
        sp = suffix_c.get(c,0)/max(suffix_tot,1)
        if op + mp + sp < 0.001: continue  # skip rare chars

        # Determine dominant zone
        dom = 'onset' if op > mp and op > sp else 'midfix' if mp > op and mp > sp else 'suffix'
        note = ''
        if mp > 0.15 and op < 0.01: note = 'MIDFIX-ONLY'
        elif mp > 0.10 and sp < 0.01: note = 'MID+ONSET'
        elif sp > 0.15 and mp < 0.01: note = 'SUFFIX-ONLY'
        print(f"  '{c}'   {op:>7.2%} {mp:>8.2%} {sp:>8.2%} | {dom:>7} | {note}")

def char_entropy_by_zone(label, onset_c, midfix_c, suffix_c):
    """Entropy of character distribution per zone."""
    h_onset  = entropy(onset_c)
    h_midfix = entropy(midfix_c)
    h_suffix = entropy(suffix_c)
    print(f"\n  {label}: H(onset)={h_onset:.3f}, H(midfix)={h_midfix:.3f}, H(suffix)={h_suffix:.3f} bits (max=4.00)")

def top_midfixes(midfix_seqs, label, top_n=30):
    """Show most common midfix sequences."""
    print(f"\n=== {label}: Top {top_n} Midfix Sequences ===")
    total = sum(midfix_seqs.values())
    print(f"  Total midfix instances: {total}, unique sequences: {len(midfix_seqs)}")
    print(f"  {'Midfix':<10} {'Count':>7} {'Rate%':>7}")
    for mf, cnt in midfix_seqs.most_common(top_n):
        if not mf: continue
        print(f"  '{mf}'     {cnt:>7}  {cnt/total:>7.2%}")

def midfix_length_by_char_type(words, label):
    """Analyze midfix character composition: how many 'vowel-like' vs 'consonant-like'."""
    # In EVA, vowel-like (appear in middle typically): a, e, i, o
    # Consonant-like: c, d, h, k, l, m, n, q, r, s, t, y
    # Special in midfix: often 'e', 'i', 'a' combinations
    vowel_like = set('aeio')

    vowel_midfix = Counter()
    total_midfix = 0
    mixed_midfix = 0
    pure_vowel   = 0
    pure_cons    = 0

    for w in words:
        olen = get_onset_len(w)
        suf  = get_suffix(w)
        slen = len(suf)
        if slen > 0 and w.endswith(suf):
            midfix = w[olen:-slen]
        else:
            midfix = w[olen:]

        if not midfix: continue
        total_midfix += 1
        chars = set(midfix)
        n_vowel = sum(1 for c in midfix if c in vowel_like)
        n_cons  = len(midfix) - n_vowel
        vowel_frac = n_vowel / len(midfix)
        if vowel_frac > 0.8: pure_vowel += 1
        elif vowel_frac < 0.2: pure_cons += 1
        else: mixed_midfix += 1

    if total_midfix > 0:
        print(f"\n  {label}: Midfix vowel content ({total_midfix} midfixes):")
        print(f"    >80% vowel-like: {pure_vowel/total_midfix:.1%}")
        print(f"    20-80% mixed:    {mixed_midfix/total_midfix:.1%}")
        print(f"    <20% vowel-like: {pure_cons/total_midfix:.1%}")

def bigram_entropy_by_zone(words, label):
    """Character bigram entropy per zone — is midfix more or less predictable than onset/suffix?"""
    onset_bigrams  = Counter()
    midfix_bigrams = Counter()
    suffix_bigrams = Counter()

    for w in words:
        olen = get_onset_len(w)
        onset_str = w[:olen]
        suf  = get_suffix(w)
        slen = len(suf)
        midfix_str = w[olen:-slen] if slen > 0 else w[olen:]

        for i in range(len(onset_str)-1):
            onset_bigrams[onset_str[i:i+2]] += 1
        for i in range(len(midfix_str)-1):
            midfix_bigrams[midfix_str[i:i+2]] += 1
        for i in range(len(suf)-1):
            suffix_bigrams[suf[i:i+2]] += 1

    h_ob = entropy(onset_bigrams)
    h_mb = entropy(midfix_bigrams)
    h_sb = entropy(suffix_bigrams)
    print(f"\n  {label}: Bigram H: onset={h_ob:.3f}, midfix={h_mb:.3f}, suffix={h_sb:.3f}")


if __name__ == '__main__':
    print("=" * 70)
    print("exp_291: Midfix Character Inventory")
    print("=" * 70)

    words_A, words_B = parse_both_dialects(ZL3B_PATH)
    print(f"\nLoaded: A={len(words_A)}, B={len(words_B)} words")

    # Zone character analysis
    onset_A, midfix_A, suffix_A, midfix_seqs_A, zm_A, hm_A = zone_chars(words_A)
    onset_B, midfix_B, suffix_B, midfix_seqs_B, zm_B, hm_B = zone_chars(words_B)

    print(f"\nA-dialect: {zm_A} zero-midfix ({zm_A/(zm_A+hm_A):.1%}), {hm_A} has-midfix")
    print(f"B-dialect: {zm_B} zero-midfix ({zm_B/(zm_B+hm_B):.1%}), {hm_B} has-midfix")

    # Character entropy by zone
    print(f"\n=== Character Entropy by Zone ===")
    char_entropy_by_zone('A-dialect', onset_A, midfix_A, suffix_A)
    char_entropy_by_zone('B-dialect', onset_B, midfix_B, suffix_B)

    # Character inventory tables
    show_char_inventory('A-dialect', onset_A, midfix_A, suffix_A)
    show_char_inventory('B-dialect', onset_B, midfix_B, suffix_B)

    # Top midfix sequences
    top_midfixes(midfix_seqs_A, 'A-dialect', top_n=25)
    top_midfixes(midfix_seqs_B, 'B-dialect', top_n=25)

    # Vowel content analysis
    print(f"\n=== Midfix Vowel Content Analysis ===")
    midfix_length_by_char_type(words_A, 'A-dialect')
    midfix_length_by_char_type(words_B, 'B-dialect')

    # Bigram entropy
    print(f"\n=== Character Bigram Entropy by Zone ===")
    bigram_entropy_by_zone(words_A, 'A-dialect')
    bigram_entropy_by_zone(words_B, 'B-dialect')

    # Summary: which chars are MIDFIX-DOMINANT?
    print(f"\n=== SUMMARY: Midfix-Dominant Characters (midfix > 2× onset AND > 2× suffix) ===")
    all_chars = sorted(set(onset_B) | set(midfix_B) | set(suffix_B))
    mt_B = sum(midfix_B.values())
    ot_B = sum(onset_B.values())
    st_B = sum(suffix_B.values())
    print(f"\nB-dialect midfix-dominant chars:")
    for c in all_chars:
        mp = midfix_B.get(c,0)/mt_B if mt_B > 0 else 0
        op = onset_B.get(c,0)/ot_B if ot_B > 0 else 0
        sp = suffix_B.get(c,0)/st_B if st_B > 0 else 0
        if mp > 0.02 and mp > 2*op and mp > 2*sp:
            print(f"  '{c}': midfix={mp:.2%}, onset={op:.2%}, suffix={sp:.2%}")

    mt_A = sum(midfix_A.values())
    ot_A = sum(onset_A.values())
    st_A = sum(suffix_A.values())
    print(f"\nA-dialect midfix-dominant chars:")
    for c in sorted(set(onset_A) | set(midfix_A) | set(suffix_A)):
        mp = midfix_A.get(c,0)/mt_A if mt_A > 0 else 0
        op = onset_A.get(c,0)/ot_A if ot_A > 0 else 0
        sp = suffix_A.get(c,0)/st_A if st_A > 0 else 0
        if mp > 0.02 and mp > 2*op and mp > 2*sp:
            print(f"  '{c}': midfix={mp:.2%}, onset={op:.2%}, suffix={sp:.2%}")

    # Find onset-exclusive chars
    print(f"\nOnset-exclusive chars (onset > 5× midfix AND onset > 5× suffix):")
    for c in sorted(all_chars):
        mp = midfix_B.get(c,0)/mt_B if mt_B > 0 else 0
        op = onset_B.get(c,0)/ot_B if ot_B > 0 else 0
        sp = suffix_B.get(c,0)/st_B if st_B > 0 else 0
        if op > 0.02 and op > 5*mp and op > 5*sp:
            print(f"  '{c}': onset={op:.2%}, midfix={mp:.2%}, suffix={sp:.2%}")

    # Find suffix-exclusive chars
    print(f"\nSuffix-exclusive chars (suffix > 5× midfix AND suffix > 5× onset):")
    for c in sorted(all_chars):
        mp = midfix_B.get(c,0)/mt_B if mt_B > 0 else 0
        op = onset_B.get(c,0)/ot_B if ot_B > 0 else 0
        sp = suffix_B.get(c,0)/st_B if st_B > 0 else 0
        if sp > 0.02 and sp > 5*mp and sp > 5*op:
            print(f"  '{c}': suffix={sp:.2%}, midfix={mp:.2%}, onset={op:.2%}")
