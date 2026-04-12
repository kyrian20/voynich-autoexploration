#!/usr/bin/env python3
"""
exp_495: pos2 Self-Chaining: Word-Level vs Class-Level
H_new_BW: Is F468 (A herbal_a universal pos2 self-chaining) driven by recurring bigrams
or distributed across many word pairs?
Tests d-LF and ch-LF as representative large classes.
"""

import re
from collections import defaultdict

ZL3B = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

ONSET_PRIORITY = ['qok','qot','qo','cth','ckh','cph','ch','sh','ok','ot','ol',
                  'sch','skh','sph','d','s','y','k','t','l','r','p','f','o','e','a','n','m']

def get_onset(word):
    for o in ONSET_PRIORITY:
        if word.startswith(o):
            return o
    return word[0] if word else ''

def folio_num(folio):
    m = re.match(r'f(\d+)', folio)
    return int(m.group(1)) if m else 999

def is_b_dialect(words):
    return sum(1 for w in words if w.endswith('edy') or w.endswith('eedy')) / max(len(words),1) >= 0.05

def get_section_a(folio):
    n = folio_num(folio)
    if n <= 56: return 'herbal_a'
    if n <= 72: return 'stars'
    if n <= 84: return 'herbal_b'
    if n <= 102: return 'cosmo'
    return 'other'

# Parse corpus
folios = defaultdict(list)
with open(ZL3B) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)', line)
        if not m:
            continue
        folio_raw, _, locus, text = m.group(1), m.group(2), m.group(3), m.group(4)
        folio = folio_raw.lstrip('+*=&~')
        lc = locus.lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'):
            continue
        words = [w for w in re.split(r'[-.\s]', text)
                 if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if words:
            folios[folio].append(words)

sections = defaultdict(list)
for folio, lines in folios.items():
    all_words = [w for line in lines for w in line]
    if not is_b_dialect(all_words):
        sec = 'A_' + get_section_a(folio)
        for line in lines:
            sections[sec].append((folio, line))

a_herbal = sections['A_herbal_a']
print(f"A herbal_a lines: {len(a_herbal)}")

def analyze_pos2_selfchain_wordlevel(section_lines, lf_onset, label):
    """For a given LF onset class, show word-pair distribution for pos2-self-chain cases."""
    lf_lines = [(fo, ws) for fo, ws in section_lines if get_onset(ws[-1]) == lf_onset]
    # pos2 eligible: len>=3
    elig = [(fo, ws) for fo, ws in lf_lines if len(ws) >= 3]
    n_elig = len(elig)

    print(f"\n--- {lf_onset}-LF pos2 word-level analysis (N_lf={len(lf_lines)}, N_elig={n_elig}) ---")

    # All (pos2_word, LF_word) pairs
    all_pairs = [(ws[1], ws[-1]) for fo, ws in elig]

    # Self-chain cases: pos2 same onset as LF
    self_chain = [(pos2, lf) for pos2, lf in all_pairs if get_onset(pos2) == lf_onset]
    n_self = len(self_chain)

    print(f"Total self-chain cases (pos2_onset==LF_onset): {n_self}/{n_elig} = {n_self/n_elig*100:.1f}%")

    # Count distinct pairs
    pair_counts = defaultdict(int)
    for p in self_chain:
        pair_counts[p] += 1

    n_distinct = len(pair_counts)
    print(f"Distinct (pos2_word, LF_word) pairs among self-chain cases: {n_distinct}")

    # Distribution: top pairs
    top_pairs = sorted(pair_counts.items(), key=lambda x: -x[1])
    cumulative = 0
    print(f"\nTop pairs (pos2_word → LF_word):")
    for i, ((pos2w, lfw), cnt) in enumerate(top_pairs[:15]):
        cumulative += cnt
        pct_of_self = cnt / n_self * 100 if n_self > 0 else 0
        cumulative_pct = cumulative / n_self * 100 if n_self > 0 else 0
        print(f"  {pos2w:12s} → {lfw:12s}: N={cnt} ({pct_of_self:.1f}% of self-chain; cumulative {cumulative_pct:.1f}%)")

    if n_distinct > 15:
        remaining = n_self - cumulative
        print(f"  ... {n_distinct - 15} more pairs, N={remaining} ({remaining/n_self*100:.1f}%)")

    # Concentration: what fraction of self-chain obs is in top-3 pairs?
    top3_count = sum(cnt for _, cnt in top_pairs[:3])
    top5_count = sum(cnt for _, cnt in top_pairs[:5])
    if n_self > 0:
        print(f"\nConcentration: top-3 pairs = {top3_count}/{n_self} = {top3_count/n_self*100:.1f}% of self-chain obs")
        print(f"Concentration: top-5 pairs = {top5_count}/{n_self} = {top5_count/n_self*100:.1f}% of self-chain obs")

    # For comparison: non-self-chain pos2 pair distribution
    non_self = [(pos2, lf) for pos2, lf in all_pairs if get_onset(pos2) != lf_onset]
    non_pair_counts = defaultdict(int)
    for p in non_self:
        non_pair_counts[p] += 1
    print(f"\nNon-self-chain pos2 words (top 5): N_non_self={len(non_self)}")
    top_pos2 = defaultdict(int)
    for pos2, lf in non_self:
        top_pos2[pos2] += 1
    for w, cnt in sorted(top_pos2.items(), key=lambda x: -x[1])[:5]:
        print(f"  pos2={w}: {cnt}")

    return n_self, n_distinct, n_elig

# Test d-LF and ch-LF (largest classes)
print("\n=== Word-level analysis of pos2 self-chaining in A herbal_a ===")
print("Question: Is F468 enrichment driven by recurring bigrams or distributed?")
print("Hypothesis: If top-3 pairs >50% of self-chain obs → bigram/lexical driven")
print("            If top-3 pairs <30% of self-chain obs → grammatical/class-level pattern")

results = {}
for lf_onset in ['d', 'ch', 'ok', 'cth', 'sh', 'o']:
    n_self, n_distinct, n_elig = analyze_pos2_selfchain_wordlevel(a_herbal, lf_onset, 'A herbal_a')
    results[lf_onset] = (n_self, n_distinct, n_elig)

print("\n=== Summary ===")
print(f"{'LF':8s} {'N_self':7s} {'N_elig':7s} {'%self':7s} {'N_distinct':10s} {'dist_ratio':10s}")
for lf_onset, (n_self, n_distinct, n_elig) in results.items():
    pct = n_self/n_elig*100 if n_elig > 0 else 0
    dist_ratio = n_distinct/n_self if n_self > 0 else 0
    print(f"{lf_onset:8s} {n_self:7d} {n_elig:7d} {pct:7.1f} {n_distinct:10d} {dist_ratio:10.2f}")
print("(dist_ratio = distinct_pairs / n_self; ratio near 1.0 means many unique pairs = distributed/grammatical)")
print("(dist_ratio near 0.0-0.3 means few recurring pairs = bigram/lexical driven)")
