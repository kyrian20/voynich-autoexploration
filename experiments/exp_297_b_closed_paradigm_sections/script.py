"""
exp_297: B-Dialect Closed Paradigm Section Stability (H501)
exp_295 found that B-dialect qok/ok/ot/ch/sh onset classes have very small closed
paradigms (18-43% of types cover 90% of tokens). This experiment asks: are these
paradigms stable across sections within B-dialect?

If the same ~32 qok types dominate across all B-dialect sections, the paradigm is
a universal template-word class. If the paradigm shifts by section, sections have
different functional vocabularies.

Also: What is the cross-section overlap for the 90%-coverage type sets?

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

# Precise section mapping based on ZL3b/VMS standard section assignments
SECTION_MAP = {
    # Herbal A (Currier A folios)
    **{f'f{n}': 'herbal_A' for n in range(1, 25)},
    **{f'f{n}': 'herbal_A' for n in range(33, 37)},
    **{f'f{n}': 'herbal_A' for n in range(40, 45)},
    **{f'f{n}': 'herbal_A' for n in range(46, 51)},
    **{f'f{n}': 'herbal_A' for n in range(93, 97)},
    # Herbal B (Currier B herbal folios)
    **{f'f{n}': 'herbal_B' for n in [25, 26, 27, 28, 29, 30, 31, 32, 37, 38, 39]},
    **{f'f{n}': 'herbal_B' for n in range(56, 66)},
    # Astronomical/Astrological
    **{f'f{n}': 'astro' for n in range(66, 74)},
    **{f'f{n}': 'astro' for n in [29, 30, 31, 32]},  # overlap with herbal_B above
    # Cosmological
    **{f'f{n}': 'cosmo' for n in [68, 69, 70, 71, 72, 73]},
    # Bio (balneological)
    **{f'f{n}': 'bio' for n in range(74, 85)},
    # Pharma
    **{f'f{n}': 'pharma' for n in [88, 89, 90, 96, 97, 98, 99, 100, 101, 102]},
    # Text/recipes
    **{f'f{n}': 'text' for n in range(103, 117)},
}

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

def folio_to_section(fb):
    """Section classification."""
    if fb in SECTION_MAP: return SECTION_MAP[fb]
    m = re.match(r'f(\d+)', fb)
    if not m: return 'other'
    n = int(m.group(1))
    if 75 <= n <= 84: return 'bio'
    if 103 <= n <= 116: return 'text'
    if 85 <= n <= 102: return 'pharma'
    if 66 <= n <= 73: return 'astro'
    return 'other'

def parse_b_with_section(path, min_len=3, max_len=15):
    """Parse B-dialect tokens with section assignment."""
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
            if dial != 'B': continue
            section = folio_to_section(fb)
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s,]', text)
                     if eva_ok.match(w) and min_len <= len(w) <= max_len]
            for w in words:
                tokens.append({'word': w, 'section': section, 'folio': fb,
                                'onset': get_onset(w)})
    return tokens


def closed_paradigm_by_section(tokens, onset_class, target_coverage=0.90):
    """
    For each section with enough B-dialect tokens of this onset class:
    - Compute the 90%-coverage word set
    - Report set size and membership
    Returns section-level closed paradigm sets for cross-section overlap analysis.
    """
    toks_onset = [t for t in tokens if t['onset'] == onset_class]
    n_total = len(toks_onset)

    # Group by section
    section_counts = defaultdict(Counter)
    for t in toks_onset:
        section_counts[t['section']][t['word']] += 1

    print(f"\n{'='*65}")
    print(f"  B-dialect {onset_class}-onset: Closed Paradigm by Section")
    print('='*65)
    print(f"  Total B-dialect {onset_class}-onset tokens: {n_total}")

    # Global 90%-coverage set for reference
    global_counts = Counter(t['word'] for t in toks_onset)
    sorted_types = global_counts.most_common()
    cumsum = 0; n90_global = 0
    for w, c in sorted_types:
        cumsum += c; n90_global += 1
        if cumsum / n_total >= target_coverage: break
    global_90_set = {w for w, c in sorted_types[:n90_global]}

    print(f"\n  Global 90%-coverage set: {n90_global} types ({n90_global/len(global_counts):.1%} of {len(global_counts)} total)")
    print(f"  Top 10 global types:")
    for w, c in sorted_types[:10]:
        print(f"    {w:<15} {c:4d} ({c/n_total:.1%})")

    # Per-section analysis
    section_90_sets = {}
    for section, counts in sorted(section_counts.items(), key=lambda x: -sum(x[1].values())):
        n_sec = sum(counts.values())
        if n_sec < 30: continue  # skip tiny sections
        n_types_sec = len(counts)
        sorted_sec = counts.most_common()
        cumsum = 0; n90_sec = 0
        for w, c in sorted_sec:
            cumsum += c; n90_sec += 1
            if cumsum / n_sec >= target_coverage: break
        sec_90_set = {w for w, c in sorted_sec[:n90_sec]}
        section_90_sets[section] = sec_90_set

        # Overlap with global
        overlap = len(sec_90_set & global_90_set)
        frac_in_global = overlap / len(sec_90_set) if sec_90_set else 0

        print(f"\n  Section: {section} (N={n_sec}, {n_types_sec} types)")
        print(f"    90%-coverage set: {n90_sec} types ({n90_sec/n_types_sec:.1%})")
        print(f"    Overlap with global 90% set: {overlap}/{n90_sec} ({frac_in_global:.1%})")
        print(f"    Top 5: {[(w,c) for w,c in sorted_sec[:5]]}")

    # Cross-section overlap: pairwise Jaccard between section 90%-sets
    if len(section_90_sets) >= 2:
        print(f"\n  Pairwise Jaccard of section 90%-coverage sets:")
        sections = list(section_90_sets.keys())
        for i, s1 in enumerate(sections):
            for s2 in sections[i+1:]:
                set1 = section_90_sets[s1]
                set2 = section_90_sets[s2]
                j = len(set1 & set2) / len(set1 | set2) if set1 | set2 else 0
                print(f"    {s1} ∩ {s2}: Jaccard={j:.3f} "
                      f"(shared={len(set1&set2)}, |s1|={len(set1)}, |s2|={len(set2)})")

    return section_90_sets, global_90_set


if __name__ == '__main__':
    print("=" * 70)
    print("exp_297: B-Dialect Closed Paradigm Section Stability (H501)")
    print("=" * 70)

    tokens = parse_b_with_section(ZL3B_PATH)
    print(f"\nTotal B-dialect tokens: {len(tokens)}")

    # Section summary
    section_totals = Counter(t['section'] for t in tokens)
    print(f"\n  Section distribution:")
    for sec, n in sorted(section_totals.items(), key=lambda x: -x[1]):
        print(f"    {sec:<15} {n:6d}")

    # Analyze qok, ch, sh, ok, ot onset classes
    for onset in ['qok', 'ch', 'sh', 'ok', 'ot']:
        s90_sets, global_90 = closed_paradigm_by_section(tokens, onset)

    # Summary: how stable are the paradigms?
    print(f"\n{'='*70}")
    print("STABILITY SUMMARY")
    print("=" * 70)
    print("""
  A paradigm is STABLE if the same word types dominate across sections.
  Metric: what fraction of each section's 90%-coverage set is in the GLOBAL 90%-set?
  If >75%: section is using the same core vocabulary as the global paradigm (stable).
  If <50%: section uses different vocabulary (section-specific paradigm).
""")
