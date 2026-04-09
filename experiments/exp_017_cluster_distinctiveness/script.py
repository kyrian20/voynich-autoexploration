"""
Experiment: exp_017_cluster_distinctiveness
Goal: Test whether cluster folios (f49v, f57v, f66r, f76r) share distinctive
statistical properties compared to each other and to non-cluster folios.
Metrics: character frequency (KL divergence), word frequency (KL divergence),
word length distributions (KS test), type-token ratios.
"""

import re
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
CORPUS = BASE / 'data/transcriptions/eva_zl3b.txt'

CLUSTER_FOLIOS = {'f49v', 'f57v', 'f66r', 'f76r'}

# Control folios: 10 non-cluster folios from same sections
# herbal A: f1r, f2v, f3r, f4r, f5r (Hand 1)
# biological: f76v, f77r, f78r, f79r (Hand 2)
# pharmaceutical: f99r, f102r (Hand 3)
CONTROL_FOLIOS = {'f1r', 'f2v', 'f3r', 'f4r', 'f5r', 'f76v', 'f77r', 'f78r', 'f99r', 'f102r'}


def parse_folio_text(path, folio_str, locus_prefix='P'):
    """Parse all body text tokens from a folio (default: P0 locus = body text)."""
    words = []
    chars = []
    in_folio = False
    with open(path, encoding='latin-1') as f:
        for raw_line in f:
            line = raw_line.strip()
            if f'<{folio_str}>' in line:
                in_folio = True
                continue
            if in_folio:
                if re.match(r'^<f\d+', line) and f'<{folio_str}.' not in line:
                    break
                if not line or line.startswith('#'):
                    continue
                m = re.match(rf'^<{re.escape(folio_str)}\.(\d+),([^>]+)>\s*(.*)', line)
                if not m:
                    continue
                locus_raw = m.group(2)
                # Strip prefix chars to get base locus
                locus_base = re.sub(r'^[*@!=+]', '', locus_raw)
                if not locus_base.startswith(locus_prefix):
                    continue
                text = m.group(3).strip()
                # Clean
                text = re.sub(r'<!.*?>', '', text)
                text = re.sub(r'<[^>]+>', '', text)
                text = text.replace('<%>', '').replace('<$>', '').replace('%', '')
                text = re.sub(r'\[([^:\]]+):[^\]]*\]', r'\1', text)
                text = re.sub(r'\{[^}]*\}', '', text)
                text = re.sub(r'@\d+;?', '', text)
                for w in re.split(r'[.\s,]+', text):
                    if w and re.match(r'^[a-zA-Z]+$', w):
                        words.append(w)
                        chars.extend(w)
    return words, chars


def parse_folio_all_text(path, folio_str):
    """Parse all text (all locus types) from a folio."""
    words = []
    chars = []
    in_folio = False
    with open(path, encoding='latin-1') as f:
        for raw_line in f:
            line = raw_line.strip()
            if f'<{folio_str}>' in line:
                in_folio = True
                continue
            if in_folio:
                if re.match(r'^<f\d+', line) and f'<{folio_str}.' not in line:
                    break
                if not line or line.startswith('#'):
                    continue
                m = re.match(rf'^<{re.escape(folio_str)}\.(\d+),([^>]+)>\s*(.*)', line)
                if not m:
                    continue
                text = m.group(3).strip()
                text = re.sub(r'<!.*?>', '', text)
                text = re.sub(r'<[^>]+>', '', text)
                text = text.replace('<%>', '').replace('<$>', '').replace('%', '')
                text = re.sub(r'\[([^:\]]+):[^\]]*\]', r'\1', text)
                text = re.sub(r'\{[^}]*\}', '', text)
                text = re.sub(r'@\d+;?', '', text)
                for w in re.split(r'[.\s,]+', text):
                    if w and re.match(r'^[a-zA-Z]+$', w):
                        words.append(w)
                        chars.extend(w)
    return words, chars


def kl_divergence(p_counts, q_counts):
    """KL divergence D(P||Q) between two frequency distributions."""
    all_keys = set(p_counts.keys()) | set(q_counts.keys())
    total_p = sum(p_counts.values())
    total_q = sum(q_counts.values())
    if total_p == 0 or total_q == 0:
        return float('inf')
    # Add epsilon smoothing for zero counts
    eps = 1e-10
    kl = 0.0
    for k in all_keys:
        p = (p_counts.get(k, 0) + eps) / (total_p + eps * len(all_keys))
        q = (q_counts.get(k, 0) + eps) / (total_q + eps * len(all_keys))
        kl += p * math.log2(p / q)
    return kl


def ttr(words):
    if not words:
        return 0.0
    return len(set(words)) / len(words)


def mean_word_length(words):
    if not words:
        return 0.0
    return sum(len(w) for w in words) / len(words)


def ks_statistic(lengths1, lengths2):
    """Simple KS statistic for word length distributions."""
    if not lengths1 or not lengths2:
        return float('nan'), float('nan')
    all_lengths = sorted(set(lengths1) | set(lengths2))
    n1, n2 = len(lengths1), len(lengths2)
    c1 = Counter(lengths1)
    c2 = Counter(lengths2)
    cum1 = cum2 = 0
    max_diff = 0
    for l in all_lengths:
        cum1 += c1.get(l, 0) / n1
        cum2 += c2.get(l, 0) / n2
        max_diff = max(max_diff, abs(cum1 - cum2))
    # Approximate p-value via KS critical value
    n = (n1 * n2) / (n1 + n2)
    critical_05 = 1.36 / math.sqrt(n)
    p_approx = 'p<0.05' if max_diff > critical_05 else 'p≥0.05'
    return max_diff, p_approx


# Manuscript-wide reference distribution
def get_manuscript_char_freq(path):
    char_freq = Counter()
    word_freq = Counter()
    with open(path, encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'^<[^>]+,([^>]+)>\s+(.*)', line)
            if not m:
                continue
            locus = re.sub(r'^[*@!=+]', '', m.group(1))
            if not locus.startswith('P'):
                continue
            text = m.group(2)
            text = re.sub(r'<!.*?>', '', text)
            text = re.sub(r'<[^>]+>', '', text)
            text = text.replace('<%>', '').replace('<$>', '').replace('%', '')
            text = re.sub(r'\[([^:\]]+):[^\]]*\]', r'\1', text)
            text = re.sub(r'\{[^}]*\}', '', text)
            text = re.sub(r'@\d+;?', '', text)
            for w in re.split(r'[.\s,]+', text):
                if w and re.match(r'^[a-zA-Z]+$', w):
                    word_freq[w] += 1
                    char_freq.update(w)
    return char_freq, word_freq


if __name__ == "__main__":
    print("Experiment exp_017: Cluster Distinctiveness Analysis")
    print("Date: 2026-04-09\n")

    path = CORPUS

    # Get manuscript-wide reference
    print("Computing manuscript-wide reference distributions...")
    ms_char_freq, ms_word_freq = get_manuscript_char_freq(path)

    # Parse each folio — use ALL text (not just P0, since f57v has mostly Cc)
    folio_data = {}
    all_folios = CLUSTER_FOLIOS | CONTROL_FOLIOS
    for folio in sorted(all_folios):
        words, chars = parse_folio_all_text(path, folio)
        folio_data[folio] = {
            'words': words,
            'chars': chars,
            'char_freq': Counter(chars),
            'word_freq': Counter(words),
            'word_lengths': [len(w) for w in words],
            'n_words': len(words),
            'n_unique_words': len(set(words)),
            'ttr': ttr(words),
            'mean_length': mean_word_length(words),
        }

    # Print basic stats
    print(f"\n{'Folio':<8} {'N_words':>8} {'N_unique':>9} {'TTR':>7} {'MeanLen':>8} {'Type':>12}")
    print("-" * 60)
    for folio in sorted(folio_data.keys()):
        d = folio_data[folio]
        ftype = "CLUSTER" if folio in CLUSTER_FOLIOS else "control"
        print(f"{folio:<8} {d['n_words']:>8} {d['n_unique_words']:>9} "
              f"{d['ttr']:>7.3f} {d['mean_length']:>8.2f} {ftype:>12}")

    # KL divergence: each folio vs manuscript-wide char distribution
    print(f"\n--- KL divergence vs manuscript-wide (char) ---")
    cluster_kl_chars = []
    control_kl_chars = []
    for folio in sorted(folio_data.keys()):
        d = folio_data[folio]
        kl = kl_divergence(d['char_freq'], ms_char_freq)
        ftype = "CLUSTER" if folio in CLUSTER_FOLIOS else "control"
        print(f"  {folio}: KL(char)={kl:.4f} [{ftype}]")
        if folio in CLUSTER_FOLIOS:
            cluster_kl_chars.append((folio, kl))
        else:
            control_kl_chars.append((folio, kl))

    avg_cluster = sum(k for _, k in cluster_kl_chars) / len(cluster_kl_chars)
    avg_control = sum(k for _, k in control_kl_chars) / len(control_kl_chars)
    print(f"\n  Cluster avg KL(char): {avg_cluster:.4f}")
    print(f"  Control avg KL(char): {avg_control:.4f}")

    # KL divergence vs manuscript-wide word distribution
    print(f"\n--- KL divergence vs manuscript-wide (word, top-500) ---")
    # Use top 500 words for tractability
    top_words = set(w for w, _ in ms_word_freq.most_common(500))
    ms_top_word_freq = {w: ms_word_freq[w] for w in top_words}
    cluster_kl_words = []
    control_kl_words = []
    for folio in sorted(folio_data.keys()):
        d = folio_data[folio]
        folio_top = {w: d['word_freq'].get(w, 0) for w in top_words}
        kl = kl_divergence(folio_top, ms_top_word_freq)
        ftype = "CLUSTER" if folio in CLUSTER_FOLIOS else "control"
        print(f"  {folio}: KL(word)={kl:.4f} [{ftype}]")
        if folio in CLUSTER_FOLIOS:
            cluster_kl_words.append((folio, kl))
        else:
            control_kl_words.append((folio, kl))

    avg_cluster_w = sum(k for _, k in cluster_kl_words) / len(cluster_kl_words)
    avg_control_w = sum(k for _, k in control_kl_words) / len(control_kl_words)
    print(f"\n  Cluster avg KL(word): {avg_cluster_w:.4f}")
    print(f"  Control avg KL(word): {avg_control_w:.4f}")

    # Word length KS tests: each cluster folio vs pooled controls
    print(f"\n--- Word length KS test: cluster vs pooled controls ---")
    control_lengths = []
    for folio in CONTROL_FOLIOS:
        control_lengths.extend(folio_data[folio]['word_lengths'])

    for folio in sorted(CLUSTER_FOLIOS):
        d = folio_data[folio]
        ks, p = ks_statistic(d['word_lengths'], control_lengths)
        print(f"  {folio}: KS={ks:.4f} ({p}), mean_len={d['mean_length']:.2f} "
              f"vs controls_mean={mean_word_length([folio_data[f]['words'] for f in CONTROL_FOLIOS][0]):.2f}")

    # Control mean length
    all_control_words = []
    for f in CONTROL_FOLIOS:
        all_control_words.extend(folio_data[f]['words'])
    print(f"\n  Pooled control mean word length: {mean_word_length(all_control_words):.2f}")
    print(f"  Pooled control TTR: {ttr(all_control_words):.3f}")

    # Cross-cluster KL divergences (char): are cluster folios similar to each other?
    print(f"\n--- Cross-cluster KL divergences (char) ---")
    cluster_list = sorted(CLUSTER_FOLIOS)
    for i, f1 in enumerate(cluster_list):
        for f2 in cluster_list[i+1:]:
            kl12 = kl_divergence(folio_data[f1]['char_freq'], folio_data[f2]['char_freq'])
            kl21 = kl_divergence(folio_data[f2]['char_freq'], folio_data[f1]['char_freq'])
            print(f"  KL({f1}||{f2})={kl12:.4f}, KL({f2}||{f1})={kl21:.4f}")

    # Cross-control for comparison
    print(f"\n--- Sample cross-control KL divergences (char) ---")
    ctrl_list = sorted(CONTROL_FOLIOS)[:5]
    for i, f1 in enumerate(ctrl_list):
        for f2 in ctrl_list[i+1:]:
            kl12 = kl_divergence(folio_data[f1]['char_freq'], folio_data[f2]['char_freq'])
            print(f"  KL({f1}||{f2})={kl12:.4f}")

    # Top words per cluster folio
    print(f"\n--- Top 10 words per cluster folio ---")
    for folio in sorted(CLUSTER_FOLIOS):
        d = folio_data[folio]
        top = d['word_freq'].most_common(10)
        print(f"  {folio}: {top}")

    # Save data
    output_path = Path(__file__).parent / 'data.json'
    save_data = {}
    for folio, d in folio_data.items():
        save_data[folio] = {
            'n_words': d['n_words'],
            'n_unique_words': d['n_unique_words'],
            'ttr': d['ttr'],
            'mean_length': d['mean_length'],
            'is_cluster': folio in CLUSTER_FOLIOS,
            'top_words': d['word_freq'].most_common(20),
            'char_freq': dict(d['char_freq'].most_common()),
        }
    with open(output_path, 'w') as fout:
        json.dump(save_data, fout, indent=2)
    print(f"\nSaved data to {output_path}")
    print("\nDone.")
