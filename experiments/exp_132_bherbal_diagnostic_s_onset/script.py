#!/usr/bin/env python3
"""
exp_132: B-Herbal Onset Profile Diagnostic (H258) + s-Onset Characterization (H259)

H258: What specific onset classes make B-herbal folios (f26/f31/f40/f48/f50) cluster
      with pharma/stars rather than herbal?
H259: Characterize s-onset words — are they a grammatical opener class with
      sub-types?
"""

import re
import math
from collections import defaultdict, Counter

CORPUS_PATH = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

# Section map (folio number → section)
def folio_to_section(f):
    if 1 <= f <= 57:
        return 'herbal'
    elif 67 <= f <= 73:
        return 'astro'
    elif 75 <= f <= 84:
        return 'cosmo'
    elif 87 <= f <= 102:
        return 'pharma'
    elif 103 <= f <= 116:
        return 'stars'
    return None

# Onset classification
ONSET_CLASSES = [
    'qok', 'qot', 'qo',
    'cth', 'ch', 'sh',
    'ok', 'ot', 'ol',
    'd', 's', 'y', 'k', 't', 'l', 'r', 'p', 'f',
    'other'
]

def get_onset(word):
    w = word.lower()
    for cls in ONSET_CLASSES[:-1]:
        if w.startswith(cls):
            return cls
    return 'other'

def parse_corpus(path):
    """Parse EVA ZL3b corpus. Returns list of records."""
    records = []
    folio_word_counts = defaultdict(lambda: defaultdict(int))

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^>]+)>(.*)', line)
            if not m:
                continue
            locus_code, text_raw = m.group(1), m.group(2)
            parts = locus_code.split(',')
            if len(parts) < 2:
                continue
            locus_type_raw = parts[1]
            locus_type = locus_type_raw.lstrip('@+*=~&')
            if not re.match(r'P', locus_type):
                continue

            # Extract folio number
            folio_str = parts[0]
            fm = re.search(r'(\d+)', folio_str)
            if not fm:
                continue
            folio_num = int(fm.group(1))
            section = folio_to_section(folio_num)
            if not section:
                continue

            # Is this a paragraph start?
            is_para_start = '=' in locus_type_raw

            # Clean text
            text = re.sub(r'<[^>]*>', '', text_raw)
            text = re.sub(r'\[[^\]]*\]', ' ', text)
            text = re.sub(r'[*@&~=+$#{}?!]', '', text)
            text = text.replace('-', ' ').replace('.', ' ').replace(',', ' ')

            words = [w for w in text.lower().split() if re.match(r'^[a-z]{2,}$', w)]
            if not words:
                continue

            # Dialect: folio-level edy/eedy rate
            for w in words:
                folio_word_counts[folio_num][w] += 1

            records.append({
                'folio': folio_num,
                'section': section,
                'words': words,
                'is_para_start': is_para_start,
            })

    # Assign dialect per folio
    folio_dialect = {}
    for folio, wc in folio_word_counts.items():
        total = sum(wc.values())
        edy_count = sum(v for w, v in wc.items() if w.endswith('edy') or w.endswith('eedy'))
        folio_dialect[folio] = 'B' if total > 0 and edy_count / total >= 0.05 else 'A'

    for r in records:
        r['dialect'] = folio_dialect.get(r['folio'], 'A')

    return records, folio_dialect


def compute_onset_profile(words):
    """Return normalized onset-class count vector."""
    counts = Counter(get_onset(w) for w in words)
    total = sum(counts.values())
    if total == 0:
        return {cls: 0.0 for cls in ONSET_CLASSES}
    return {cls: counts.get(cls, 0) / total for cls in ONSET_CLASSES}


def cosine_sim(v1, v2):
    dot = sum(v1[k] * v2[k] for k in ONSET_CLASSES)
    n1 = math.sqrt(sum(v ** 2 for v in v1.values()))
    n2 = math.sqrt(sum(v ** 2 for v in v2.values()))
    if n1 == 0 or n2 == 0:
        return 0.0
    return dot / (n1 * n2)


def analyze_bherbal_diagnostic(records, folio_dialect):
    """H258: Characterize what onset classes make B-herbal folios mismatch."""
    print("=" * 70)
    print("H258: B-HERBAL FOLIO ONSET PROFILE DIAGNOSTIC")
    print("=" * 70)

    # Build per-folio word lists
    folio_words = defaultdict(list)
    for r in records:
        folio_words[r['folio']].extend(r['words'])

    # Build section centroids (average onset-class profiles)
    section_words = defaultdict(list)
    for r in records:
        section_words[r['section']].extend(r['words'])

    section_centroids = {s: compute_onset_profile(ws) for s, ws in section_words.items()}

    # B-herbal folios
    b_herbal = [f for f in folio_words if folio_to_section(f) == 'herbal' and folio_dialect.get(f) == 'B']
    b_herbal.sort()
    # A-herbal folios for baseline
    a_herbal = [f for f in folio_words if folio_to_section(f) == 'herbal' and folio_dialect.get(f) == 'A']

    print(f"\nB-herbal folios identified: {b_herbal}")
    print(f"A-herbal folios (n={len(a_herbal)}): {sorted(a_herbal)[:10]}...")

    # Compute profiles for each B-herbal folio
    print("\n### Per-Folio Cosine Similarity to Each Section Centroid")
    sections = ['herbal', 'pharma', 'stars', 'cosmo', 'astro']
    header = f"{'Folio':<8} {'Tokens':<8} " + " ".join(f"{s:<8}" for s in sections) + " Best"
    print(header)

    folio_profiles = {}
    for f in sorted(b_herbal):
        ws = folio_words[f]
        profile = compute_onset_profile(ws)
        folio_profiles[f] = profile
        sims = {s: cosine_sim(profile, section_centroids[s]) for s in sections}
        best = max(sims, key=sims.get)
        row = f"f{f:<7} {len(ws):<8} " + " ".join(f"{sims[s]:.3f}   " for s in sections) + f" {best}"
        print(row)

    # A-herbal centroid for comparison
    a_herbal_words = [w for f in a_herbal for w in folio_words[f]]
    a_herbal_centroid = compute_onset_profile(a_herbal_words)

    print("\n### Onset-Class Profile: B-Herbal Folios vs Section Centroids")
    print("(+) = over-represented vs A-herbal centroid; (-) = under-represented")
    print()

    # Show deviations: B-herbal folio profile - A-herbal centroid
    # Focus on classes with large deviations
    print(f"{'Class':<8} {'A-Herb':<8} {'Stars':<8} {'Pharma':<8} " + " ".join(f"f{f:<6}" for f in sorted(b_herbal)))
    for cls in ONSET_CLASSES:
        a_val = a_herbal_centroid[cls]
        stars_val = section_centroids['stars'][cls]
        pharma_val = section_centroids['pharma'][cls]
        folio_vals = [folio_profiles[f][cls] for f in sorted(b_herbal)]
        # Only show classes with meaningful variation
        all_vals = [a_val, stars_val, pharma_val] + folio_vals
        if max(all_vals) - min(all_vals) < 0.005:
            continue
        row = f"{cls:<8} {a_val:.4f}  {stars_val:.4f}  {pharma_val:.4f}  "
        row += " ".join(f"{v:.4f}  " for v in folio_vals)
        print(row)

    # For each B-herbal folio: show top 5 most deviant onset classes vs A-herbal centroid
    print("\n### Top Deviant Onset Classes: B-Herbal vs A-Herbal Centroid")
    for f in sorted(b_herbal):
        profile = folio_profiles[f]
        deviations = {cls: profile[cls] - a_herbal_centroid[cls] for cls in ONSET_CLASSES}
        sorted_dev = sorted(deviations.items(), key=lambda x: abs(x[1]), reverse=True)[:6]
        best_section = max(section_centroids.keys(), key=lambda s: cosine_sim(profile, section_centroids[s]))
        print(f"\nf{f} (best={best_section}, n={len(folio_words[f])} tokens):")
        for cls, dev in sorted_dev:
            direction = "↑" if dev > 0 else "↓"
            a_val = a_herbal_centroid[cls]
            f_val = profile[cls]
            best_s_val = section_centroids[best_section][cls]
            print(f"  {cls:<8} {direction}{abs(dev):.4f}  folio={f_val:.4f}  A-herbal={a_val:.4f}  {best_section}={best_s_val:.4f}")

    # Summary: which onset classes consistently deviate across all B-herbal folios?
    print("\n### Consistent Deviations Across ALL B-Herbal Folios vs A-Herbal")
    for cls in ONSET_CLASSES:
        devs = [folio_profiles[f][cls] - a_herbal_centroid[cls] for f in b_herbal]
        if all(d > 0.002 for d in devs):
            mean_dev = sum(devs) / len(devs)
            print(f"  ELEVATED: {cls:<8} mean_dev=+{mean_dev:.4f} (A-herbal={a_herbal_centroid[cls]:.4f})")
        elif all(d < -0.002 for d in devs):
            mean_dev = sum(devs) / len(devs)
            print(f"  DEPLETED: {cls:<8} mean_dev={mean_dev:.4f} (A-herbal={a_herbal_centroid[cls]:.4f})")


def analyze_s_onset(records):
    """H259: Characterize s-onset words — sub-classes, positional profile, section/dialect, bigrams."""
    print("\n\n" + "=" * 70)
    print("H259: s-ONSET CHARACTERIZATION")
    print("=" * 70)

    # Collect s-onset words with positional metadata
    s_words = []  # (word, position_in_line, line_length, folio, section, dialect)
    all_words = []  # (word, onset, folio, section, dialect) for bigram context

    for r in records:
        words = r['words']
        n = len(words)
        for i, w in enumerate(words):
            onset = get_onset(w)
            all_words.append((w, onset, i, n, r['folio'], r['section'], r['dialect']))
            if onset == 's':
                is_lf = (i == 0)
                is_ll = (i == n - 1)
                is_mid = not is_lf and not is_ll
                s_words.append({
                    'word': w,
                    'pos': i,
                    'n': n,
                    'frac': i / max(n - 1, 1),
                    'is_lf': is_lf,
                    'is_ll': is_ll,
                    'is_mid': is_mid,
                    'folio': r['folio'],
                    'section': r['section'],
                    'dialect': r['dialect'],
                    'line_idx': len(s_words),
                })

    # Basic stats
    total_tokens = len(s_words)
    word_counter = Counter(sw['word'] for sw in s_words)
    total_types = len(word_counter)
    hapax = sum(1 for w, c in word_counter.items() if c == 1)

    lf = sum(1 for sw in s_words if sw['is_lf'])
    ll = sum(1 for sw in s_words if sw['is_ll'])
    mid = sum(1 for sw in s_words if sw['is_mid'])

    # Section distribution
    section_counts = Counter(sw['section'] for sw in s_words)
    all_section_counts = Counter(w[5] for w in all_words)
    # Dialect distribution
    dialect_counts = Counter(sw['dialect'] for sw in s_words)
    all_dialect_counts = Counter(w[6] for w in all_words)

    print(f"\nTotal s-onset tokens: {total_tokens}")
    print(f"Total s-onset types: {total_types}")
    print(f"Hapax legomena: {hapax} ({100*hapax/total_types:.1f}%)")
    print(f"\nPositional profile:")
    print(f"  Line-first (LF): {lf} ({100*lf/total_tokens:.1f}%)")
    print(f"  Mid-line (MID):  {mid} ({100*mid/total_tokens:.1f}%)")
    print(f"  Line-last (LL):  {ll} ({100*ll/total_tokens:.1f}%)")

    print(f"\nSection distribution (with enrichment vs corpus baseline):")
    total_all = len(all_words)
    for s in ['herbal', 'pharma', 'stars', 'cosmo', 'astro']:
        n_s = section_counts.get(s, 0)
        n_all = all_section_counts.get(s, 0)
        enrichment = (n_s / total_tokens) / (n_all / total_all) if n_all > 0 else 0
        print(f"  {s:<8}: {n_s:4d} ({100*n_s/total_tokens:.1f}%)  base={100*n_all/total_all:.1f}%  enrich={enrichment:.2f}×")

    print(f"\nDialect distribution:")
    for d in ['A', 'B']:
        n_d = dialect_counts.get(d, 0)
        n_all_d = all_dialect_counts.get(d, 0)
        enrichment = (n_d / total_tokens) / (n_all_d / total_all) if n_all_d > 0 else 0
        print(f"  {d}: {n_d} ({100*n_d/total_tokens:.1f}%)  corpus={100*n_all_d/total_all:.1f}%  A/B ratio effect={enrichment:.2f}×")

    # Top s-words with individual profiles
    print(f"\n### Top s-Onset Words (top 25)")
    print(f"{'Word':<14} {'n':>5} {'LF%':>6} {'MID%':>6} {'LL%':>6} {'Stars%':>8} {'B%':>6}")
    for word, count in word_counter.most_common(25):
        ws = [sw for sw in s_words if sw['word'] == word]
        lf_r = sum(1 for w in ws if w['is_lf']) / len(ws)
        ll_r = sum(1 for w in ws if w['is_ll']) / len(ws)
        mid_r = sum(1 for w in ws if w['is_mid']) / len(ws)
        stars_r = sum(1 for w in ws if w['section'] == 'stars') / len(ws)
        b_r = sum(1 for w in ws if w['dialect'] == 'B') / len(ws)
        print(f"{word:<14} {count:>5} {100*lf_r:>5.1f}% {100*mid_r:>5.1f}% {100*ll_r:>5.1f}% {100*stars_r:>7.1f}% {100*b_r:>5.1f}%")

    # Sub-class analysis
    print(f"\n### s-Onset Sub-Classes by Positional Role")
    # Build word-level LF/MID/LL
    word_profile = {}
    for word, count in word_counter.items():
        if count < 3:
            continue
        ws = [sw for sw in s_words if sw['word'] == word]
        lf_r = sum(1 for w in ws if w['is_lf']) / len(ws)
        ll_r = sum(1 for w in ws if w['is_ll']) / len(ws)
        mid_r = sum(1 for w in ws if w['is_mid']) / len(ws)
        word_profile[word] = (count, lf_r, mid_r, ll_r)

    openers = [(w, c, lf, mid, ll) for w, (c, lf, mid, ll) in word_profile.items() if lf >= 0.40]
    closers = [(w, c, lf, mid, ll) for w, (c, lf, mid, ll) in word_profile.items() if ll >= 0.25 and lf < 0.40]
    medials = [(w, c, lf, mid, ll) for w, (c, lf, mid, ll) in word_profile.items()
               if mid >= 0.60 and lf < 0.40 and ll < 0.25]

    print(f"\ns-OPENERS (LF≥40%, n≥3): {len(openers)} types")
    for w, c, lf, mid, ll in sorted(openers, key=lambda x: -x[2])[:10]:
        print(f"  {w:<14} n={c:>4}  LF={100*lf:.0f}%  MID={100*mid:.0f}%  LL={100*ll:.0f}%")

    print(f"\ns-CLOSERS (LL≥25%, LF<40%, n≥3): {len(closers)} types")
    for w, c, lf, mid, ll in sorted(closers, key=lambda x: -x[4])[:10]:
        print(f"  {w:<14} n={c:>4}  LF={100*lf:.0f}%  MID={100*mid:.0f}%  LL={100*ll:.0f}%")

    print(f"\ns-MEDIALS (MID≥60%, n≥3): {len(medials)} types")
    for w, c, lf, mid, ll in sorted(medials, key=lambda x: -x[2])[:10]:
        print(f"  {w:<14} n={c:>4}  LF={100*lf:.0f}%  MID={100*mid:.0f}%  LL={100*ll:.0f}%")

    # Bigram context: what comes before and after s-onset words
    print(f"\n### Bigram Context: What Precedes and Follows s-Onset Words?")
    # Build list of (prev_onset, s_word, next_onset)
    pre_s = Counter()
    post_s = Counter()
    total_pre = 0
    total_post = 0

    for r in records:
        words = r['words']
        onsets = [get_onset(w) for w in words]
        for i, (w, onset) in enumerate(zip(words, onsets)):
            if onset != 's':
                continue
            if i > 0:
                pre_s[onsets[i - 1]] += 1
                total_pre += 1
            if i < len(words) - 1:
                post_s[onsets[i + 1]] += 1
                total_post += 1

    # Compute corpus baseline onset distribution
    corpus_onset_counts = Counter()
    for r in records:
        for w in r['words']:
            corpus_onset_counts[get_onset(w)] += 1
    corpus_total = sum(corpus_onset_counts.values())
    corpus_onset_frac = {cls: corpus_onset_counts[cls] / corpus_total for cls in ONSET_CLASSES}

    print("\nPre-s onset enrichment (what appears before s-words):")
    print(f"{'Onset':<10} {'n':>5} {'obs%':>8} {'base%':>8} {'enrich':>8}")
    for cls, n in pre_s.most_common(12):
        obs = n / total_pre
        base = corpus_onset_frac.get(cls, 0)
        enrich = obs / base if base > 0 else 0
        print(f"{cls:<10} {n:>5} {100*obs:>7.2f}% {100*base:>7.2f}% {enrich:>7.2f}×")

    print("\nPost-s onset enrichment (what follows s-words):")
    print(f"{'Onset':<10} {'n':>5} {'obs%':>8} {'base%':>8} {'enrich':>8}")
    for cls, n in post_s.most_common(12):
        obs = n / total_post
        base = corpus_onset_frac.get(cls, 0)
        enrich = obs / base if base > 0 else 0
        print(f"{cls:<10} {n:>5} {100*obs:>7.2f}% {100*base:>7.2f}% {enrich:>7.2f}×")

    # Stars-specific s-onset analysis
    print(f"\n### Stars-Specific s-Onset Analysis")
    stars_s = [sw for sw in s_words if sw['section'] == 'stars']
    if stars_s:
        stars_s_counter = Counter(sw['word'] for sw in stars_s)
        stars_lf = sum(1 for sw in stars_s if sw['is_lf'])
        stars_total = len(stars_s)
        print(f"Stars s-onset tokens: {stars_total} (LF={100*stars_lf/stars_total:.1f}%)")
        print("Top stars s-words:")
        for word, count in stars_s_counter.most_common(10):
            all_count = word_counter.get(word, 0)
            stars_pct = 100 * count / all_count if all_count > 0 else 0
            ws_list = [sw for sw in s_words if sw['word'] == word]
            lf_r = sum(1 for w in ws_list if w['is_lf']) / len(ws_list)
            print(f"  {word:<14} n={count:>4} ({stars_pct:.0f}% of all {word})  LF={100*lf_r:.0f}%")

    # Comparison to d-onset (for structural contrast)
    print(f"\n### s-Onset vs d-Onset Structural Comparison")
    d_words_data = []
    for r in records:
        words = r['words']
        n = len(words)
        for i, w in enumerate(words):
            if get_onset(w) == 'd':
                d_words_data.append({
                    'word': w,
                    'is_lf': (i == 0),
                    'is_ll': (i == n - 1),
                    'is_mid': (0 < i < n - 1),
                })
    d_total = len(d_words_data)
    d_lf = sum(1 for w in d_words_data if w['is_lf'])
    d_ll = sum(1 for w in d_words_data if w['is_ll'])
    d_mid = sum(1 for w in d_words_data if w['is_mid'])
    print(f"d-onset: n={d_total}, LF={100*d_lf/d_total:.1f}%, MID={100*d_mid/d_total:.1f}%, LL={100*d_ll/d_total:.1f}%")
    print(f"s-onset: n={total_tokens}, LF={100*lf/total_tokens:.1f}%, MID={100*mid/total_tokens:.1f}%, LL={100*ll/total_tokens:.1f}%")
    print(f"s/d LF ratio: {(lf/total_tokens)/(d_lf/d_total):.2f}× (s more/less line-first than d)")

    # Para-start s-onset rate
    para_start_records = [r for r in records if r['is_para_start']]
    para_start_s = 0
    para_start_total = 0
    for r in para_start_records:
        if r['words']:
            para_start_total += 1
            if get_onset(r['words'][0]) == 's':
                para_start_s += 1
    all_first_words = sum(1 for r in records if r['words'])
    all_first_s = sum(1 for r in records if r['words'] and get_onset(r['words'][0]) == 's')
    if para_start_total > 0 and all_first_words > 0:
        print(f"\nPara-start first-word = s: {para_start_s}/{para_start_total} ({100*para_start_s/para_start_total:.1f}%)")
        print(f"All-line first-word = s: {all_first_s}/{all_first_words} ({100*all_first_s/all_first_words:.1f}%)")
        if all_first_s > 0 and all_first_words > 0:
            enrich = (para_start_s / para_start_total) / (all_first_s / all_first_words)
            print(f"Para-start s enrichment: {enrich:.2f}×")


def main():
    print("Loading corpus...")
    records, folio_dialect = parse_corpus(CORPUS_PATH)
    print(f"Loaded {len(records)} body-text lines from {len(set(r['folio'] for r in records))} folios")
    total_words = sum(len(r['words']) for r in records)
    print(f"Total body-text words: {total_words}")

    analyze_bherbal_diagnostic(records, folio_dialect)
    analyze_s_onset(records)

    print("\n\nDone.")


if __name__ == '__main__':
    main()
