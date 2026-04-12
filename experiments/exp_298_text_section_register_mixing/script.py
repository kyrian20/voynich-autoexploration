"""
exp_298: Text-Section Paradigm Expansion — Register Mixing vs Genuine Lexical Diversity (H502)

exp_297 found: text section needs 39 qok types for 90% token coverage (vs bio=15),
with 74% overlap with the global 90%-set. H502: is this because the text section
(f103-f116) mixes multiple sub-registers (zodiac, recipes, circular text)?

Method: split f103-f116 into sub-groups by folio characteristics:
- Zodiac (f103-f116 based on VMS folio assignments — text/recipe section)
  Note: the "text" section in ZL3b is folios 103-116 (Currier B late section)
  f103-f116 contains:
    - f103r: starts with "por" paragraph
    - f107-f116: late B-dialect text

  We'll split by folio range:
    - Early text: f103-f108 (first 6 folios)
    - Late text: f109-f116 (last 8 folios)

  Also compare to: paragraph-position stratification (P1 = first line, P-rest)
  and within-folio diversity (TTR per folio in text section).

The key question: if text sub-sections individually have bio-sized paradigms (~15 types),
expansion = register mixing. If each individually needs 30+ types, it's genuine diversity.

Also: measure folio-level TTR for qok-onset words in text vs bio section.

Data: eva_zl3b.txt
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

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label
    return 'other'

def folio_base(folio):
    return re.sub(r'[rv][12]?$', '', folio)

def folio_num(fb):
    m = re.match(r'f(\d+)', fb)
    return int(m.group(1)) if m else -1

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

def parse_b_with_folio(path, min_len=3, max_len=15):
    """Parse B-dialect tokens with folio and locus info."""
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
            n = folio_num(fb)
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s,]', text)
                     if eva_ok.match(w) and min_len <= len(w) <= max_len]
            for w in words:
                tokens.append({'word': w, 'folio': fb, 'n': n, 'onset': get_onset(w)})
    return tokens


def closed_paradigm_size(counts, target_coverage=0.90):
    """How many types cover target_coverage fraction of tokens?"""
    total = sum(counts.values())
    if total == 0: return 0, 0
    cumsum = 0; n90 = 0
    for w, c in counts.most_common():
        cumsum += c; n90 += 1
        if cumsum / total >= target_coverage: break
    return n90, len(counts)


def analyze_sub_sections(tokens, onset_class, section_name, sub_def, min_n=30):
    """
    sub_def: dict {label: set of folio_nums}
    Compute 90%-coverage set for each sub-group and cross-group Jaccard.
    """
    toks = [t for t in tokens if t['onset'] == onset_class]

    print(f"\n{'='*65}")
    print(f"  {section_name} — {onset_class}-onset sub-section analysis")
    print('='*65)

    sub_sets = {}
    for label, folio_nums in sorted(sub_def.items()):
        sub_toks = [t for t in toks if t['n'] in folio_nums]
        if not sub_toks:
            continue
        counts = Counter(t['word'] for t in sub_toks)
        n90, n_types = closed_paradigm_size(counts)
        n_total = sum(counts.values())
        if n_total < min_n:
            print(f"  {label}: N={n_total} (too small, skip)")
            continue
        sub_sets[label] = {w for w, _ in counts.most_common(n90)}
        top5 = counts.most_common(5)
        print(f"\n  {label} (N={n_total}, {n_types} types):")
        print(f"    90%-coverage: {n90} types ({n90/n_types:.1%})")
        print(f"    Top 5: {[(w,c) for w,c in top5]}")

    if len(sub_sets) >= 2:
        print(f"\n  Pairwise Jaccard:")
        labels = list(sub_sets.keys())
        for i, l1 in enumerate(labels):
            for l2 in labels[i+1:]:
                s1, s2 = sub_sets[l1], sub_sets[l2]
                j = len(s1 & s2) / len(s1 | s2) if s1 | s2 else 0
                print(f"    {l1} ∩ {l2}: J={j:.3f} (shared={len(s1&s2)}, |{l1}|={len(s1)}, |{l2}|={len(s2)})")

    return sub_sets


def folio_level_ttr(tokens, onset_class, section_folio_nums):
    """Per-folio TTR for onset_class within the given folio set."""
    toks = [t for t in tokens if t['onset'] == onset_class and t['n'] in section_folio_nums]
    by_folio = defaultdict(Counter)
    for t in toks:
        by_folio[t['folio']][t['word']] += 1

    ttrs = []
    for fb, counts in by_folio.items():
        total = sum(counts.values())
        if total >= 5:
            ttrs.append((fb, total, len(counts), len(counts)/total))
    ttrs.sort(key=lambda x: x[0])
    return ttrs


if __name__ == '__main__':
    print("=" * 70)
    print("exp_298: Text-Section Paradigm Expansion — Register Mixing vs Diversity (H502)")
    print("=" * 70)

    tokens = parse_b_with_folio(ZL3B_PATH)

    # Section definitions
    text_folios = set(range(103, 117))   # f103-f116
    bio_folios = set(range(74, 85))      # f74-f84

    # Text sub-sections
    text_early = set(range(103, 110))    # f103-f109 (6 folios)
    text_late  = set(range(110, 117))    # f110-f116 (7 folios)

    # Bio sub-sections
    bio_early = set(range(74, 80))       # f74-f79
    bio_late  = set(range(80, 85))       # f80-f84

    # Overall token count by section
    text_toks = [t for t in tokens if t['n'] in text_folios]
    bio_toks  = [t for t in tokens if t['n'] in bio_folios]

    print(f"\nTotal B-dialect tokens: {len(tokens)}")
    print(f"Text section (f103-f116): {len(text_toks)} tokens")
    print(f"Bio section (f74-f84): {len(bio_toks)} tokens")

    # Folio distribution
    print(f"\nText folio sizes (all onsets):")
    text_folio_counts = Counter(t['folio'] for t in text_toks)
    for fb, n in sorted(text_folio_counts.items()):
        print(f"  {fb}: {n}")

    print(f"\nBio folio sizes (all onsets):")
    bio_folio_counts = Counter(t['folio'] for t in bio_toks)
    for fb, n in sorted(bio_folio_counts.items()):
        print(f"  {fb}: {n}")

    for onset in ['qok', 'ok', 'ot', 'ch', 'sh']:
        print(f"\n{'#'*70}")
        print(f"# ONSET CLASS: {onset}")
        print('#'*70)

        # Text sub-sections
        analyze_sub_sections(
            tokens, onset,
            "Text section",
            {'text_early_f103-109': text_early, 'text_late_f110-116': text_late}
        )

        # Bio sub-sections (for comparison)
        analyze_sub_sections(
            tokens, onset,
            "Bio section",
            {'bio_early_f74-79': bio_early, 'bio_late_f80-84': bio_late}
        )

        # Per-folio TTR in text vs bio
        print(f"\n  Per-folio TTR ({onset}-onset):")
        print(f"  Text folios:")
        text_ttrs = folio_level_ttr(tokens, onset, text_folios)
        for fb, total, types, ttr in text_ttrs:
            print(f"    {fb}: N={total}, types={types}, TTR={ttr:.3f}")

        print(f"  Bio folios:")
        bio_ttrs = folio_level_ttr(tokens, onset, bio_folios)
        for fb, total, types, ttr in bio_ttrs:
            print(f"    {fb}: N={total}, types={types}, TTR={ttr:.3f}")

        # Summary: mean TTR
        if text_ttrs and bio_ttrs:
            mean_text_ttr = np.mean([x[3] for x in text_ttrs])
            mean_bio_ttr  = np.mean([x[3] for x in bio_ttrs])
            print(f"\n  Mean per-folio TTR: text={mean_text_ttr:.3f}, bio={mean_bio_ttr:.3f}")

    print(f"\n{'='*70}")
    print("SUMMARY")
    print('='*70)
    print("""
  If text_early and text_late each have bio-sized paradigms (15-20 types for qok):
    → Text expansion = register mixing across folios
  If text_early/late individually need 30+ types:
    → Text genuinely has more diverse vocabulary within folios
  Per-folio TTR: if text TTR > bio TTR per folio, diversity is within-folio.
    """)
