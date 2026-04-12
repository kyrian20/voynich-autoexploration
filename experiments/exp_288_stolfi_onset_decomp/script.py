"""
exp_288: Stolfi Decomposition by Onset Class
Hypothesis: H492 — Different onset classes have different suffix inventories,
midfix lengths, and internal entropy profiles.

Exploratory analysis — characterizes word-internal structure per onset class.

Data: eva_zl3b.txt (ZL3b transcription, IVTFF format)
Dependencies: numpy (standard in project venv)
"""

import os, re
import numpy as np
from collections import Counter, defaultdict
from math import log2

REPO_DIR  = os.path.expanduser('~/voynich-cryptanalyst')
ZL3B_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')
LATIN_PATH = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')

# Onset order (longest-match first, from exp_257)
ONSET_ORDER = [
    ('qok', 'qok'), ('qot', 'qot'), ('qo', 'qo'), ('cth', 'cth'),
    ('ch', 'ch'), ('sh', 'sh'), ('ok', 'ok'), ('ot', 'ot'), ('ol', 'ol'),
    ('d', 'd'), ('s', 's'), ('y', 'y'), ('k', 'k'), ('t', 't'),
    ('l', 'l'), ('r', 'r'), ('p', 'p'), ('f', 'f'), ('o', 'o'),
]

# Suffix list: longest-match first (canonical VMS suffixes)
SUFFIX_LIST_RAW = [
    'eedy', 'eey',   # B-paradigm extended
    'edy',            # B-paradigm standard
    'aiin',           # A-paradigm extended
    'oldy', 'oly', 'ory',  # A-paradigm compound
    'ain',
    'ol', 'or', 'al', 'ar',  # A-paradigm base
    'ey', 'dy', 'ay',         # 2-char common
    'am', 'an', 'in',         # 2-char consonant-final
    'y', 'n', 'l', 'r',       # 1-char final
]
# Deduplicate
seen = set()
SUFFIX_LIST = []
for s in SUFFIX_LIST_RAW:
    if s not in seen:
        seen.add(s)
        SUFFIX_LIST.append(s)

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label
    return 'other'

def get_onset_len(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return len(prefix)
    return 0

def get_suffix(w):
    """Extract longest-match suffix from full word, min 1 char before suffix."""
    for s in SUFFIX_LIST:
        if w.endswith(s) and len(w) > len(s):
            return s
    return ''  # no recognized suffix

def entropy(counts):
    total = sum(counts.values())
    if total == 0: return 0.0
    return -sum((c/total)*log2(c/total) for c in counts.values() if c > 0)

def folio_base(folio):
    return re.sub(r'[rv][12]?$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

def parse_zl3b_both(path, min_len=3, max_len=15):
    """Parse ZL3b EVA transcription for both A and B dialect words.
    Two-pass: first classify dialect per folio (by edy rate), then extract words.
    """
    eva_ok = re.compile(r'^[a-z]+$')

    # Pass 1: classify dialects by folio edy-rate
    folio_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1)
            folio = folio_raw.lstrip('+*=&~')
            fb = folio_base(folio)
            text = re.sub(r'<[^>]+>', '', line)  # remove special tokens
            words = [w for w in re.split(r'[-.\s,]', text)
                     if eva_ok.match(w) and min_len <= len(w) <= max_len]
            for w in words:
                folio_stats[fb]['total'] += 1
                if w.endswith('eedy'): folio_stats[fb]['eedy'] += 1
                elif w.endswith('edy'): folio_stats[fb]['edy'] += 1

    folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_stats.items()}
    n_A = sum(1 for v in folio_dialect.values() if v == 'A')
    n_B = sum(1 for v in folio_dialect.values() if v == 'B')
    print(f"Dialect classification: {n_A} A-folios, {n_B} B-folios")

    # Pass 2: extract words per dialect, body text only (P* loci)
    words_A, words_B = [], []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1)
            locus_code = m.group(3)
            folio = folio_raw.lstrip('+*=&~')
            fb = folio_base(folio)
            dial = folio_dialect.get(fb, 'unknown')
            if dial not in ('A', 'B'): continue
            # Body text only: locus must be P-type
            lc = locus_code.lstrip('+*=/~&@')
            if not lc.startswith('P'): continue
            # Extract words
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s,]', text)
                     if eva_ok.match(w) and min_len <= len(w) <= max_len]
            if dial == 'A':
                words_A.extend(words)
            else:
                words_B.extend(words)

    return words_A, words_B

def decompose_words(words):
    """Decompose each word into onset, body, suffix, midfix."""
    records = []
    for w in words:
        onset = get_onset(w)
        olen  = get_onset_len(w)
        body  = w[olen:]    # post-onset
        suffix = get_suffix(w)  # match from full word
        slen  = len(suffix)
        # midfix = body without suffix
        if slen > 0 and w.endswith(suffix):
            stem = w[olen:-slen]  # between onset and suffix
        else:
            stem = body  # no recognized suffix — all is stem
        midfix = stem
        records.append({
            'word': w, 'onset': onset, 'body': body,
            'suffix': suffix, 'midfix': midfix,
            'wlen': len(w), 'blen': len(body),
            'mlen': len(midfix), 'slen': slen,
            'zero_mid': len(midfix) == 0,
        })
    return records

def suffix_coverage(records, label):
    """Report suffix extraction coverage."""
    n = len(records)
    if n == 0:
        print(f"\n{label}: 0 records")
        return
    n_suff = sum(1 for r in records if r['suffix'] != '')
    print(f"\n{label} suffix coverage: {n_suff}/{n} = {n_suff/n:.3f}")

def onset_stats_table(records, label='corpus'):
    """Compute and print per-onset statistics."""
    by_onset = defaultdict(list)
    for r in records:
        by_onset[r['onset']].append(r)

    print(f"\n=== {label}: Per-Onset Summary ===")
    print(f"{'Onset':<7} {'N':>6} {'WLen':>6} {'MLen':>6} {'SLen':>6} {'ZroMd':>6} {'SH':>6} {'NSuff':>6}")
    print('-'*58)

    summary = {}
    for onset in sorted(by_onset.keys(), key=lambda x: -len(by_onset[x])):
        recs = by_onset[onset]
        if len(recs) < 20: continue
        n = len(recs)
        wl = np.mean([r['wlen'] for r in recs])
        ml = np.mean([r['mlen'] for r in recs])
        sl = np.mean([r['slen'] for r in recs])
        zm = sum(r['zero_mid'] for r in recs) / n
        sc = Counter(r['suffix'] for r in recs)
        sh = entropy(sc)
        ns = len(sc)
        print(f"{onset:<7} {n:>6} {wl:>6.2f} {ml:>6.2f} {sl:>6.2f} {zm:>6.3f} {sh:>6.3f} {ns:>6}")
        summary[onset] = {
            'n': n, 'wlen': wl, 'mlen': ml, 'slen': sl,
            'zero_mid': zm, 'suff_h': sh, 'n_suff': ns,
            'suff_dist': dict(sc.most_common(8)),
        }
    return summary

def suffix_top_by_onset(records, top_onsets, label):
    """Show top suffix distribution for each onset class."""
    by_onset = defaultdict(list)
    for r in records:
        by_onset[r['onset']].append(r)

    print(f"\n=== {label}: Top Suffix Distributions by Onset ===")
    for onset in top_onsets:
        recs = by_onset.get(onset, [])
        if len(recs) < 10: continue
        sc = Counter(r['suffix'] for r in recs)
        total = len(recs)
        top = sc.most_common(6)
        top_str = ', '.join(f"'{s}'={c/total:.1%}" for s,c in top)
        print(f"  {onset:<6} (N={total:4d}): {top_str}")

def midfix_length_by_onset(records, top_onsets, label):
    """Show midfix length distribution per onset class."""
    by_onset = defaultdict(list)
    for r in records:
        by_onset[r['onset']].append(r)

    print(f"\n=== {label}: Midfix Length Distribution by Onset ===")
    for onset in top_onsets:
        recs = by_onset.get(onset, [])
        if len(recs) < 10: continue
        mlens = [r['mlen'] for r in recs]
        mc = Counter(mlens)
        total = len(recs)
        dist = ', '.join(f"{k}:{v/total:.1%}" for k,v in sorted(mc.items())[:7])
        print(f"  {onset:<6} (N={total:4d}): mean={np.mean(mlens):.2f} std={np.std(mlens):.2f} [{dist}]")

def body_entropy_by_onset(records, top_onsets, label):
    """Entropy of body characters at each position (relative to onset end), by onset class."""
    by_onset = defaultdict(list)
    for r in records:
        by_onset[r['onset']].append(r)

    print(f"\n=== {label}: Body Position Entropy by Onset (pos 0=char after onset) ===")
    header = f"{'Onset':<7} {'N':>5}"
    for p in range(6):
        header += f"  p{p}"
    print(header)

    for onset in top_onsets:
        recs = by_onset.get(onset, [])
        if len(recs) < 10: continue
        pos_chars = defaultdict(list)
        for r in recs:
            for i, c in enumerate(r['body'][:8]):
                pos_chars[i].append(c)
        row = f"{onset:<7} {len(recs):>5}"
        for p in range(6):
            if len(pos_chars[p]) < 5:
                row += "   ---"
            else:
                h = entropy(Counter(pos_chars[p]))
                row += f"  {h:.2f}"
        print(row)

def midfix_entropy_by_onset(records, top_onsets, label):
    """Entropy of midfix characters at each position, by onset class."""
    by_onset = defaultdict(list)
    for r in records:
        by_onset[r['onset']].append(r)

    print(f"\n=== {label}: Midfix Position Entropy by Onset ===")
    header = f"{'Onset':<7} {'N_mf':>5}"
    for p in range(5):
        header += f"  m{p}"
    print(header)

    for onset in top_onsets:
        recs = by_onset.get(onset, [])
        recs_with_mf = [r for r in recs if r['mlen'] > 0]
        if len(recs_with_mf) < 10: continue
        pos_chars = defaultdict(list)
        for r in recs_with_mf:
            for i, c in enumerate(r['midfix'][:6]):
                pos_chars[i].append(c)
        row = f"{onset:<7} {len(recs_with_mf):>5}"
        for p in range(5):
            if len(pos_chars[p]) < 5:
                row += "   ---"
            else:
                h = entropy(Counter(pos_chars[p]))
                row += f"  {h:.2f}"
        print(row)

if __name__ == '__main__':
    print("=" * 70)
    print("exp_288: Stolfi Decomposition by Onset Class")
    print("=" * 70)

    # Load VMS corpus
    words_A, words_B = parse_zl3b_both(ZL3B_PATH)
    print(f"\nCorpus loaded: A={len(words_A)} words, B={len(words_B)} words")

    # Decompose
    recs_A = decompose_words(words_A)
    recs_B = decompose_words(words_B)

    # Suffix coverage check
    suffix_coverage(recs_A, 'A-dialect')
    suffix_coverage(recs_B, 'B-dialect')

    # Overall stats
    print(f"\nOverall word length:   A={np.mean([r['wlen'] for r in recs_A]):.2f}, B={np.mean([r['wlen'] for r in recs_B]):.2f}")
    print(f"Overall midfix length: A={np.mean([r['mlen'] for r in recs_A]):.2f}, B={np.mean([r['mlen'] for r in recs_B]):.2f}")
    print(f"Overall suffix length: A={np.mean([r['slen'] for r in recs_A]):.2f}, B={np.mean([r['slen'] for r in recs_B]):.2f}")
    print(f"Overall zero-midfix:   A={np.mean([r['zero_mid'] for r in recs_A]):.3f}, B={np.mean([r['zero_mid'] for r in recs_B]):.3f}")

    # Per-onset summary tables
    sum_A = onset_stats_table(recs_A, 'A-dialect')
    sum_B = onset_stats_table(recs_B, 'B-dialect')

    # Top onset classes (by count) for detailed analysis
    top_A = sorted(sum_A.keys(), key=lambda x: -sum_A[x]['n'])[:10]
    top_B = sorted(sum_B.keys(), key=lambda x: -sum_B[x]['n'])[:10]

    # Top suffix distributions
    suffix_top_by_onset(recs_A, top_A, 'A-dialect')
    suffix_top_by_onset(recs_B, top_B, 'B-dialect')

    # Midfix length distributions
    midfix_length_by_onset(recs_A, top_A, 'A-dialect')
    midfix_length_by_onset(recs_B, top_B, 'B-dialect')

    # Body positional entropy
    body_entropy_by_onset(recs_A, top_A, 'A-dialect')
    body_entropy_by_onset(recs_B, top_B, 'B-dialect')

    # Midfix entropy
    midfix_entropy_by_onset(recs_A, top_A, 'A-dialect')
    midfix_entropy_by_onset(recs_B, top_B, 'B-dialect')

    # Cross-dialect comparison
    shared = [o for o in sum_A if o in sum_B and sum_A[o]['n'] >= 50 and sum_B[o]['n'] >= 50]
    print(f"\n=== A vs B Comparison (shared onsets, N>=50 each) ===")
    print(f"{'Onset':<7} {'N_A':>5} {'N_B':>5} {'ML_A':>6} {'ML_B':>6} {'SL_A':>6} {'SL_B':>6} {'SH_A':>6} {'SH_B':>6}")
    print('-'*65)
    for o in sorted(shared, key=lambda x: -(sum_A[x]['n']+sum_B[x]['n'])):
        a, b = sum_A[o], sum_B[o]
        print(f"{o:<7} {a['n']:>5} {b['n']:>5} {a['mlen']:>6.2f} {b['mlen']:>6.2f} {a['slen']:>6.2f} {b['slen']:>6.2f} {a['suff_h']:>6.3f} {b['suff_h']:>6.3f}")

    # Suffix entropy range across onset classes
    print(f"\n=== Suffix Entropy Range Across Onset Classes ===")
    print(f"A-dialect: min={min(v['suff_h'] for v in sum_A.values()):.3f}, "
          f"max={max(v['suff_h'] for v in sum_A.values()):.3f}, "
          f"range={max(v['suff_h'] for v in sum_A.values())-min(v['suff_h'] for v in sum_A.values()):.3f}")
    print(f"B-dialect: min={min(v['suff_h'] for v in sum_B.values()):.3f}, "
          f"max={max(v['suff_h'] for v in sum_B.values()):.3f}, "
          f"range={max(v['suff_h'] for v in sum_B.values())-min(v['suff_h'] for v in sum_B.values()):.3f}")

    # Latin control: initial consonant cluster decomposition
    print("\n=== Latin Cicero Control (initial consonant cluster = onset) ===")
    try:
        with open(LATIN_PATH, encoding='utf-8', errors='ignore') as f:
            text = f.read()
        lat_words = re.findall(r'[a-zA-Z]+', text)
        lat_recs = []
        for w in lat_words:
            w = w.lower()
            if len(w) < 3: continue
            # Onset = initial consonant cluster
            i = 0
            while i < len(w) and w[i] in 'aeiou': i += 1  # skip initial vowels
            j = i
            while j < len(w) and w[j] not in 'aeiou': j += 1  # find first vowel
            onset = w[i:j] if j > i else 'V'  # consonant cluster or vowel-initial
            body = w[j:] if j > 0 else w
            lat_recs.append({'onset': onset, 'wlen': len(w), 'blen': len(body), 'mlen': max(0, len(body)-2)})
        print(f"Latin words: {len(lat_recs)}")
        lat_by_onset = defaultdict(list)
        for r in lat_recs: lat_by_onset[r['onset']].append(r)
        print(f"{'Onset':12} {'N':>6} {'WLen':>6} {'BLen':>6}")
        print('-'*35)
        for o, recs in sorted(lat_by_onset.items(), key=lambda x: -len(x[1]))[:10]:
            if len(recs) < 20: continue
            wl = np.mean([r['wlen'] for r in recs])
            bl = np.mean([r['blen'] for r in recs])
            print(f"{o:12} {len(recs):>6} {wl:>6.2f} {bl:>6.2f}")
    except FileNotFoundError:
        print(f"Latin corpus not found at {LATIN_PATH}")

    # === FINAL SUMMARY ===
    print("\n" + "=" * 70)
    print("FINAL SUMMARY: Onset-Class Structural Profiles")
    print("=" * 70)
    print("\nB-dialect (top onsets by frequency):")
    for o in top_B:
        if o not in sum_B: continue
        v = sum_B[o]
        top2 = sorted(v['suff_dist'].items(), key=lambda x: -x[1])[:3]
        top_str = ', '.join(f"'{s}'={c}" for s,c in top2)
        print(f"  {o:<7} N={v['n']:4d}: WLen={v['wlen']:.2f}, MLen={v['mlen']:.2f}, SLen={v['slen']:.2f}, SH={v['suff_h']:.3f}, ZeroMid={v['zero_mid']:.3f} | top_suff=[{top_str}]")

    print("\nA-dialect (top onsets by frequency):")
    for o in top_A:
        if o not in sum_A: continue
        v = sum_A[o]
        top2 = sorted(v['suff_dist'].items(), key=lambda x: -x[1])[:3]
        top_str = ', '.join(f"'{s}'={c}" for s,c in top2)
        print(f"  {o:<7} N={v['n']:4d}: WLen={v['wlen']:.2f}, MLen={v['mlen']:.2f}, SLen={v['slen']:.2f}, SH={v['suff_h']:.3f}, ZeroMid={v['zero_mid']:.3f} | top_suff=[{top_str}]")
