"""
exp_103: ch-Stem Section Classifier (H195) and Cross-Dialect ch-Stem Comparison (H196)

H195: Can ch-stem vocabulary predict which section a paragraph comes from?
      If ch-stems are section-specific content words, they should predict section.

H196: Cross-dialect ch-stem comparison.
      Do A and B share ch-stems or have distinct vocabularies?
"""

import re
import math
from collections import defaultdict, Counter

DATA_PATH = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'


def folio_base(folio):
    return re.sub(r'\.\d+$', '', folio)


def classify_dialect(folio_stats):
    total = folio_stats.get('total', 0)
    if total == 0:
        return 'unknown'
    rate = (folio_stats.get('edy', 0) + folio_stats.get('eedy', 0)) / total
    return 'B' if rate >= 0.05 else 'A'


def classify_section(folio):
    m = re.match(r'f(\d+)([rv])', folio)
    if not m:
        return 'unknown'
    n = int(m.group(1))
    if n <= 57:
        return 'herbal'
    if 67 <= n <= 73:
        return 'astro'
    if 75 <= n <= 84:
        return 'cosmo'
    if 87 <= n <= 102:
        return 'pharma'
    if 103 <= n <= 116:
        return 'stars'
    return 'other'


def parse_voynich():
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m:
                continue
            folio_raw = m.group(1)
            folio = folio_raw.lstrip('+*=&~')
            fb = folio_base(folio)
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            for w in words:
                folio_word_stats[fb]['total'] += 1
                if w.endswith('eedy'):
                    folio_word_stats[fb]['eedy'] += 1
                elif w.endswith('edy'):
                    folio_word_stats[fb]['edy'] += 1

    folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}

    # Parse paragraph-level data
    paragraphs = {}
    current_para = None
    para_count = 0

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m:
                continue
            folio_raw = m.group(1)
            locus_code = m.group(3)
            folio = folio_raw.lstrip('+*=&~')
            fb = folio_base(folio)
            dialect = folio_dialect.get(fb, 'unknown')
            section = classify_section(fb)

            lc_stripped = locus_code.lstrip('+*=/~&')
            is_para_start = lc_stripped.startswith('@')
            is_body = lc_stripped.lstrip('@').startswith('P')
            if not is_body:
                continue

            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words:
                continue

            if is_para_start:
                para_count += 1
                current_para = para_count
                paragraphs[current_para] = {
                    'dialect': dialect,
                    'section': section,
                    'folio': fb,
                    'words': []
                }
            if current_para is not None:
                paragraphs[current_para]['words'].extend(words)

    return paragraphs


def h195_section_classifier(paragraphs):
    """H195: Can ch-stem vocabulary predict section?"""
    print("=" * 70)
    print("H195: ch-Stem Section Classifier")
    print("=" * 70)

    # Focus on A dialect with 4 sections (herbal, pharma, astro) and B dialect (herbal, stars, cosmo)
    for dialect, sections in [('A', ['herbal', 'pharma', 'astro']),
                               ('B', ['herbal', 'stars', 'cosmo'])]:
        d_paras = {pid: p for pid, p in paragraphs.items()
                   if p['dialect'] == dialect and p['section'] in sections}

        print(f"\n{'='*50}")
        print(f"Dialect {dialect} — {len(d_paras)} paragraphs in {sections}")

        # Get ch-words per paragraph
        para_section = {}
        para_ch = {}
        for pid, para in d_paras.items():
            section = para['section']
            ch_words = [w for w in para['words'] if w.startswith('ch') and len(w) >= 3]
            if len(ch_words) >= 3:  # Only paragraphs with enough ch-words
                para_section[pid] = section
                para_ch[pid] = Counter(ch_words)

        print(f"Paragraphs with ≥3 ch-words: {len(para_ch)}")

        # Build naive Bayes classifier using ch-word frequencies
        # Training on ALL data (leave-one-out cross-validation would be ideal but expensive)
        # Instead: train on first 80%, test on last 20%
        pids = list(para_ch.keys())
        n = len(pids)
        train_n = int(n * 0.8)
        train_pids = pids[:train_n]
        test_pids = pids[train_n:]

        # Compute per-section ch-word log probabilities (training data)
        section_word_counts = defaultdict(Counter)
        section_total = defaultdict(int)
        for pid in train_pids:
            section = para_section[pid]
            for word, count in para_ch[pid].items():
                section_word_counts[section][word] += count
                section_total[section] += count

        # Section priors (uniform for simplicity)
        n_sections = len(sections)
        log_prior = -math.log(n_sections)

        # Vocabulary for Laplace smoothing
        all_ch_vocab = set()
        for counter in section_word_counts.values():
            all_ch_vocab.update(counter.keys())
        V = len(all_ch_vocab)

        # Evaluate on test set
        correct = 0
        total_test = 0
        confusion = defaultdict(Counter)

        for pid in test_pids:
            true_section = para_section[pid]
            ch_words = para_ch[pid]

            # Score each section
            scores = {}
            for sect in sections:
                total = section_total.get(sect, 0) + V  # Laplace smoothed total
                log_prob = log_prior
                for word, count in ch_words.items():
                    word_count = section_word_counts[sect].get(word, 0) + 1  # Laplace
                    log_prob += count * math.log(word_count / total)
                scores[sect] = log_prob

            predicted = max(scores, key=scores.get)
            confusion[true_section][predicted] += 1
            if predicted == true_section:
                correct += 1
            total_test += 1

        accuracy = correct / total_test if total_test > 0 else 0
        baseline = 1 / n_sections

        print(f"\nNaive Bayes classifier accuracy: {correct}/{total_test} = {accuracy:.3f}")
        print(f"Baseline (random): {baseline:.3f}")
        print(f"Improvement: {accuracy/baseline:.2f}× baseline")

        print(f"\nConfusion matrix (true → predicted):")
        all_sects = sorted(set(list(confusion.keys()) + [s for v in confusion.values() for s in v.keys()]))
        print(f"  {'True\\Pred':<12}", end='')
        for s in all_sects:
            print(f"  {s[:8]:>8}", end='')
        print()
        for true_s in all_sects:
            row_total = sum(confusion[true_s].values())
            print(f"  {true_s:<12}", end='')
            for pred_s in all_sects:
                cnt = confusion[true_s].get(pred_s, 0)
                print(f"  {cnt:>8}", end='')
            print(f"  (n={row_total})")

        # Most informative features (ch-words with highest per-section log-odds)
        print(f"\nMost informative ch-words by section:")
        for sect in sections:
            total_this = section_total.get(sect, 0) + V
            total_other = sum(section_total[s] for s in sections if s != sect) + V * (n_sections - 1)
            log_odds = []
            for word in all_ch_vocab:
                count_this = section_word_counts[sect].get(word, 0) + 1
                count_other = sum(section_word_counts[s].get(word, 0) for s in sections if s != sect) + (n_sections - 1)
                p_this = count_this / total_this
                p_other = count_other / total_other
                lo = math.log(p_this / p_other)
                total_count = sum(section_word_counts[s].get(word, 0) for s in sections)
                if total_count >= 3:
                    log_odds.append((word, lo, total_count))
            log_odds.sort(key=lambda x: -x[1])
            top = log_odds[:8]
            top_str = ', '.join(f"{w}({lo:.1f})" for w, lo, n in top)
            print(f"  {sect}: {top_str}")

        # Also test with ALL words (not just ch)
        para_all_words = {}
        for pid, para in d_paras.items():
            words = [w for w in para['words'] if len(w) >= 2]
            if len(words) >= 10:
                para_all_words[pid] = Counter(words)

        pids_all = list(para_all_words.keys())
        n_all = len(pids_all)
        train_n_all = int(n_all * 0.8)
        train_all = pids_all[:train_n_all]
        test_all = pids_all[train_n_all:]

        sect_word_counts_all = defaultdict(Counter)
        sect_total_all = defaultdict(int)
        for pid in train_all:
            sect = para_section.get(pid)
            if sect is None:
                # Look it up
                sect = d_paras[pid]['section']
            for word, count in para_all_words[pid].items():
                sect_word_counts_all[sect][word] += count
                sect_total_all[sect] += count

        V_all = len(set(w for c in sect_word_counts_all.values() for w in c.keys()))

        correct_all = 0
        total_test_all = 0
        for pid in test_all:
            true_sect = d_paras[pid]['section']
            if true_sect not in sections:
                continue
            words_pid = para_all_words[pid]
            scores = {}
            for sect in sections:
                total = sect_total_all.get(sect, 0) + V_all
                log_prob = log_prior
                for word, count in words_pid.items():
                    wc = sect_word_counts_all[sect].get(word, 0) + 1
                    log_prob += count * math.log(wc / total)
                scores[sect] = log_prob
            predicted = max(scores, key=scores.get)
            if predicted == true_sect:
                correct_all += 1
            total_test_all += 1

        acc_all = correct_all / total_test_all if total_test_all > 0 else 0
        print(f"\nAll-word classifier accuracy: {correct_all}/{total_test_all} = {acc_all:.3f}")
        print(f"ch-word classifier accuracy: {accuracy:.3f} ({accuracy/acc_all*100:.0f}% of all-word performance)")


def h196_cross_dialect_ch_stems(paragraphs):
    """H196: Cross-dialect ch-stem comparison."""
    print("\n" + "=" * 70)
    print("H196: Cross-Dialect ch-Stem Comparison")
    print("=" * 70)

    # Get all ch-words by dialect
    a_ch = Counter()
    b_ch = Counter()
    a_total = 0
    b_total = 0

    for pid, para in paragraphs.items():
        words = para['words']
        if para['dialect'] == 'A':
            for w in words:
                if w.startswith('ch') and len(w) >= 3:
                    a_ch[w] += 1
                a_total += 1
        elif para['dialect'] == 'B':
            for w in words:
                if w.startswith('ch') and len(w) >= 3:
                    b_ch[w] += 1
                b_total += 1

    # Shared vs exclusive
    a_vocab = set(a_ch.keys())
    b_vocab = set(b_ch.keys())
    shared = a_vocab & b_vocab
    a_only = a_vocab - b_vocab
    b_only = b_vocab - a_vocab

    print(f"\nA dialect ch-vocabulary: {len(a_vocab)} unique ch-words ({sum(a_ch.values())} tokens)")
    print(f"B dialect ch-vocabulary: {len(b_vocab)} unique ch-words ({sum(b_ch.values())} tokens)")
    print(f"Shared: {len(shared)} words ({len(shared)/len(a_vocab|b_vocab)*100:.1f}% of union)")
    print(f"A-exclusive: {len(a_only)} words")
    print(f"B-exclusive: {len(b_only)} words")

    # Top shared ch-words and their relative rates
    print(f"\n--- Shared ch-Words: A vs B Rate Comparison ---")
    shared_list = [(w, a_ch[w], b_ch[w]) for w in shared]
    shared_list.sort(key=lambda x: -(x[1]+x[2]))

    print(f"{'Word':<18} {'A_n':>5} {'A%':>7} {'B_n':>5} {'B%':>7} {'A/B_ratio':>10}")
    for word, a_n, b_n in shared_list[:20]:
        a_rate = a_n / a_total * 1000  # per 1000 words
        b_rate = b_n / b_total * 1000
        ratio = a_rate / b_rate if b_rate > 0 else float('inf')
        print(f"  {word:<18} {a_n:>5} {a_rate:>6.2f}‰ {b_n:>5} {b_rate:>6.2f}‰ {ratio:>9.2f}×")

    # A-dominant shared words (present in A at higher rate)
    print(f"\n--- A-Dominant Shared ch-Words (A rate > 2× B rate) ---")
    a_dominant = [(w, a_ch[w], b_ch[w]) for w in shared
                  if a_ch[w]/a_total > 2 * b_ch[w]/b_total and a_ch[w] >= 5]
    a_dominant.sort(key=lambda x: -x[1])
    for word, a_n, b_n in a_dominant[:15]:
        a_rate = a_n / a_total * 1000
        b_rate = b_n / b_total * 1000
        ratio = a_rate / b_rate if b_rate > 0 else float('inf')
        print(f"  {word}: A={a_n}({a_rate:.2f}‰) B={b_n}({b_rate:.2f}‰) ratio={ratio:.1f}×")

    print(f"\n--- B-Dominant Shared ch-Words (B rate > 2× A rate) ---")
    b_dominant = [(w, a_ch[w], b_ch[w]) for w in shared
                  if b_ch[w]/b_total > 2 * a_ch[w]/a_total and b_ch[w] >= 5]
    b_dominant.sort(key=lambda x: -x[2])
    for word, a_n, b_n in b_dominant[:15]:
        a_rate = a_n / a_total * 1000
        b_rate = b_n / b_total * 1000
        ratio = b_rate / a_rate if a_rate > 0 else float('inf')
        print(f"  {word}: B={b_n}({b_rate:.2f}‰) A={a_n}({a_rate:.2f}‰) ratio={ratio:.1f}×")

    # High-frequency A-exclusive and B-exclusive
    print(f"\n--- Top A-Exclusive ch-Words (not in B) ---")
    a_exclusive_sorted = sorted([(w, n) for w, n in a_ch.items() if w in a_only], key=lambda x: -x[1])
    for w, n in a_exclusive_sorted[:15]:
        print(f"  {w}: {n} tokens in A")

    print(f"\n--- Top B-Exclusive ch-Words (not in A) ---")
    b_exclusive_sorted = sorted([(w, n) for w, n in b_ch.items() if w in b_only], key=lambda x: -x[1])
    for w, n in b_exclusive_sorted[:15]:
        print(f"  {w}: {n} tokens in B")

    # Jaccard similarity
    jaccard = len(shared) / len(a_vocab | b_vocab)
    print(f"\nJaccard similarity (ch-stems A vs B): {jaccard:.3f}")

    # Compare to random baseline (what fraction would be shared if vocabulary were random?)
    # Under hypergeometric model: expected shared ≈ |A| * |B| / |A ∪ B|
    expected_shared = len(a_vocab) * len(b_vocab) / (len(a_vocab) + len(b_vocab))
    print(f"Expected shared (under independence): ~{expected_shared:.0f}")
    print(f"Observed shared: {len(shared)} (ratio to expected: {len(shared)/expected_shared:.2f}×)")


def main():
    print("Loading data...")
    paragraphs = parse_voynich()
    n_a = sum(1 for p in paragraphs.values() if p['dialect'] == 'A')
    n_b = sum(1 for p in paragraphs.values() if p['dialect'] == 'B')
    print(f"Total paragraphs: {len(paragraphs)} (A={n_a}, B={n_b})")

    h195_section_classifier(paragraphs)
    h196_cross_dialect_ch_stems(paragraphs)


if __name__ == '__main__':
    main()
