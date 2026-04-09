"""
exp_056: Three-Slot Word Template Analysis (H067)
Tests whether Voynichese word formation follows:
  [ONSET: qo/o/y/cth/∅] + [ROOT: stem type] + [SUFFIX: paradigm class]
by measuring observed vs expected frequency of onset × suffix combinations.
Also: what fraction of the corpus is explained by the top onset × suffix combos?
"""

import re
import math
from collections import Counter, defaultdict

DATA_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"

SUFFIX_LIST = ['aiin', 'ain', 'eedy', 'edy', 'chy', 'eey', 'dy', 'ey', 'y', 'ol', 'or', 'al', 'ar', 'iin', 'in']

def is_body_locus(locus_code):
    base = locus_code.lstrip('+*@=/~&')
    return base.startswith('P')

def clean_text(text):
    return re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)

def suffix_group(word):
    for suf in SUFFIX_LIST:
        if word.endswith(suf) and len(word) > len(suf):
            return suf
    return None

def classify_onset(word):
    """Classify word by onset morpheme."""
    if word.startswith('qo') and len(word) > 2:
        return 'qo'
    elif word.startswith('o') and len(word) > 2:
        return 'o'
    elif word.startswith('y') and len(word) >= 3:
        return 'y'
    elif word.startswith('cth') and len(word) > 3:
        return 'cth'
    elif word.startswith('sh') and len(word) > 2:
        return 'sh'
    elif word.startswith('ch') and len(word) > 2:
        return 'ch'
    elif word.startswith('d') and len(word) > 1:
        return 'd'
    else:
        return 'other'

def parse_corpus(path):
    """Parse body text words per Currier dialect."""
    words_a = []
    words_b = []
    current_currier = None

    with open(path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue

            m_c = re.search(r'\$L=([AB])', line)
            if m_c:
                current_currier = m_c.group(1)

            m = re.match(r'^<([^>]+)>', line)
            if not m:
                continue
            locus_raw = m.group(1)
            parts = locus_raw.split(',')
            if len(parts) < 2:
                continue
            locus_code = parts[1].strip()

            if not is_body_locus(locus_code):
                continue

            text = line[m.end():].strip()
            text = clean_text(text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]

            if current_currier == 'A':
                words_a.extend(tokens)
            elif current_currier == 'B':
                words_b.extend(tokens)

    return words_a, words_b

def onset_suffix_analysis(words, dialect_name):
    """Full cross-tabulation of onset × suffix classes."""
    print(f"\n{'='*70}")
    print(f"ONSET × SUFFIX CROSS-TABULATION: Currier {dialect_name}")
    print(f"{'='*70}")

    n = len(words)
    onset_counts = Counter()
    suffix_counts = Counter()
    cross_counts = Counter()

    for w in words:
        onset = classify_onset(w)
        suf = suffix_group(w) or '(none)'
        onset_counts[onset] += 1
        suffix_counts[suf] += 1
        cross_counts[(onset, suf)] += 1

    # Compute expected under independence
    onsets = sorted(onset_counts.keys(), key=lambda x: -onset_counts[x])
    suffixes = sorted(suffix_counts.keys(), key=lambda x: -suffix_counts[x])[:12]  # top 12 suffixes

    # Print cross-table
    print(f"\n{'Onset':<8}", end='')
    for suf in suffixes:
        print(f"{'-'+suf:>8}", end='')
    print(f"{'(none)':>8} {'TOTAL':>7}")

    for onset in onsets[:8]:
        print(f"{onset:<8}", end='')
        for suf in suffixes:
            obs = cross_counts.get((onset, suf), 0)
            print(f"{obs:>8}", end='')
        obs_none = cross_counts.get((onset, '(none)'), 0)
        print(f"{obs_none:>8} {onset_counts[onset]:>7}")

    print(f"{'TOTAL':<8}", end='')
    for suf in suffixes:
        print(f"{suffix_counts[suf]:>8}", end='')
    print(f"{suffix_counts.get('(none)',0):>8} {n:>7}")

    # Compute KL(observed || expected) for each onset class
    print(f"\nKL from independence for each onset class:")
    for onset in onsets[:8]:
        obs_dist = {}
        exp_dist = {}
        for suf in suffixes + ['(none)']:
            obs = cross_counts.get((onset, suf), 0)
            onset_total = onset_counts[onset]
            obs_p = obs / max(1, onset_total)
            exp_p = suffix_counts[suf] / n
            obs_dist[suf] = obs_p
            exp_dist[suf] = exp_p

        kl = 0.0
        for suf in obs_dist:
            p = obs_dist[suf]
            q = exp_dist.get(suf, 1e-10)
            if p > 1e-9:
                kl += p * math.log2(p / max(q, 1e-10))

        print(f"  onset={onset:<8} (n={onset_counts[onset]:>5}): KL={kl:.3f} bits (deviation from independence)")

    # Most over-represented onset-suffix combinations
    print(f"\nTop OVER-REPRESENTED onset-suffix combinations (observed/expected > 2):")
    print(f"{'Onset-Suffix':<20} {'Obs':>6} {'Exp':>6} {'Ratio':>7}")
    over_rep = []
    for (onset, suf), obs in cross_counts.items():
        exp = onset_counts[onset] * suffix_counts[suf] / n
        if exp >= 3 and obs / exp > 2.0:
            over_rep.append((onset, suf, obs, exp, obs/exp))
    over_rep.sort(key=lambda x: -x[4])
    for onset, suf, obs, exp, ratio in over_rep[:20]:
        print(f"{onset+'+'+suf:<20} {obs:>6} {exp:>6.1f} {ratio:>7.2f}×")

    print(f"\nTop UNDER-REPRESENTED onset-suffix combinations (observed/expected < 0.2):")
    print(f"{'Onset-Suffix':<20} {'Obs':>6} {'Exp':>6} {'Ratio':>7}")
    under_rep = []
    for onset in onsets[:8]:
        for suf in suffixes + ['(none)']:
            obs = cross_counts.get((onset, suf), 0)
            exp = onset_counts[onset] * suffix_counts[suf] / n
            if exp >= 5 and (obs == 0 or obs / exp < 0.2):
                under_rep.append((onset, suf, obs, exp, obs/max(exp,1e-6)))
    under_rep.sort(key=lambda x: x[4])
    for onset, suf, obs, exp, ratio in under_rep[:15]:
        print(f"{onset+'+'+suf:<20} {obs:>6} {exp:>6.1f} {ratio:>7.2f}×")

    # Coverage: what fraction of corpus is covered by top N onset-suffix combinations?
    print(f"\nTop onset-suffix combinations by frequency:")
    top_combos = cross_counts.most_common(20)
    cumulative = 0
    print(f"{'Rank':<5} {'Onset-Suffix':<20} {'Count':>7} {'%':>6} {'Cumulative%':>12}")
    for i, ((onset, suf), count) in enumerate(top_combos, 1):
        cumulative += count
        print(f"{i:<5} {onset+'+'+suf:<20} {count:>7} {100*count/n:>5.1f}% {100*cumulative/n:>11.1f}%")

    return onset_counts, suffix_counts, cross_counts

def main():
    words_a, words_b = parse_corpus(DATA_PATH)
    print(f"Currier A: {len(words_a)} tokens, Currier B: {len(words_b)} tokens")

    # Analyze Currier B (main dialect with most data)
    onset_b, suffix_b, cross_b = onset_suffix_analysis(words_b, 'B')

    # Analyze Currier A
    onset_a, suffix_a, cross_a = onset_suffix_analysis(words_a, 'A')

    # Global summary
    n_b = len(words_b)
    n_a = len(words_a)

    print("\n" + "="*70)
    print("TEMPLATE COVERAGE: What fraction of corpus uses recognized templates?")
    print("="*70)

    # Top 5 onset classes
    top_onsets_b = [k for k, v in onset_b.most_common(6)]
    top_onsets_a = [k for k, v in onset_a.most_common(6)]

    # Top 6 suffix classes
    top_suffixes_b = [k for k, v in suffix_b.most_common(7) if k != '(none)']
    top_suffixes_a = [k for k, v in suffix_a.most_common(7) if k != '(none)']

    # Coverage by template matrix
    for dialect, words, onsets, suffixes, cross, n in [
        ('B', words_b, top_onsets_b, top_suffixes_b, cross_b, n_b),
        ('A', words_a, top_onsets_a, top_suffixes_a, cross_a, n_a),
    ]:
        covered = sum(cross.get((on, suf), 0) for on in onsets for suf in suffixes)
        print(f"\nCurrier {dialect}: Top {len(onsets)} onsets × top {len(suffixes)} suffixes")
        print(f"  Coverage: {covered}/{n} = {100*covered/n:.1f}%")

        # Individual onset coverage
        print(f"  Onset-only coverage (all suffixes included):")
        for on in onsets:
            count = onset_b.get(on, 0) if dialect == 'B' else onset_a.get(on, 0)
            print(f"    onset={on}: {count} ({100*count/n:.1f}%)")

if __name__ == '__main__':
    main()
