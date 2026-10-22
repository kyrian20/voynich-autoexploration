"""
exp_197: ch-Stem Section Classifier + Cross-Dialect Comparison + Zipf's Law

H195: Section-specific ch-stem vocabulary — can ch-stems identify section?
H196: Cross-dialect ch-stem — do A-herbal and B-stars share ch-stems?
H199: Zipf's law — does Voynich word frequency follow f(r) ∝ r^(-α)?
"""
from pathlib import Path as _RepositoryPath

import re
import math
from collections import Counter, defaultdict

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')


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


def is_ch_stem(word):
    w = word.lower()
    return w.startswith('ch') or w.startswith('cth') or w.startswith('sh')


def parse_corpus():
    """Parse corpus; return paragraph list and folio-level word stats."""
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

    paragraphs = []
    current_para = None

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
                current_para = {
                    'dialect': dialect,
                    'section': section,
                    'folio': fb,
                    'words': []
                }
                paragraphs.append(current_para)

            if current_para is not None:
                current_para['words'].extend(words)

    return paragraphs, folio_dialect


def h195_ch_stem_classifier(paragraphs):
    """H195: ch-stem section classifier."""
    print("=" * 70)
    print("H195: ch-Stem Section Classifier")
    print("=" * 70)

    # Focus on 4 sections with sufficient data
    target_sections = ['herbal', 'pharma', 'stars', 'cosmo']
    sections_paras = {s: [p for p in paragraphs if p['section'] == s] for s in target_sections}

    for s in target_sections:
        n = len(sections_paras[s])
        print(f"  {s}: {n} paragraphs")

    # Build section ch-stem vocabulary
    section_ch_counts = {}
    section_total_ch = {}
    section_total_words = {}
    for sect in target_sections:
        ch_words = Counter()
        total_ch = 0
        total_words = 0
        for p in sections_paras[sect]:
            for w in p['words']:
                total_words += 1
                if is_ch_stem(w):
                    ch_words[w] += 1
                    total_ch += 1
        section_ch_counts[sect] = ch_words
        section_total_ch[sect] = total_ch
        section_total_words[sect] = total_words

    print(f"\nch-stem words by section:")
    for sect in target_sections:
        print(f"  {sect}: {section_total_ch[sect]} ch-words, {len(section_ch_counts[sect])} unique, "
              f"rate={section_total_ch[sect]/section_total_words[sect]:.1%}")

    # Find most discriminative ch-stem words (PMI-like: log(p(w|s) / p(w|overall)))
    all_ch = Counter()
    total_all = 0
    for sect in target_sections:
        for w, cnt in section_ch_counts[sect].items():
            all_ch[w] += cnt
            total_all += cnt

    print(f"\nTop discriminative ch-stem words by section:")
    for sect in target_sections:
        sect_total = section_total_ch[sect]
        discriminative = []
        for w, cnt in section_ch_counts[sect].most_common(50):
            p_w_sect = cnt / sect_total
            p_w_all = all_ch[w] / total_all
            pmi = math.log2(p_w_sect / p_w_all) if p_w_all > 0 else 0
            if cnt >= 3:  # min count threshold
                discriminative.append((w, cnt, pmi))

        discriminative.sort(key=lambda x: -x[2])
        print(f"\n  {sect} (top discriminative ch-words):")
        for w, cnt, pmi in discriminative[:8]:
            print(f"    {w}: {cnt} occurrences, PMI={pmi:.2f}")

    # Simple classifier: Naive Bayes using ch-stem words
    # Leave-one-out cross-validation on paragraphs
    print(f"\n--- Naive Bayes Classifier (leave-one-out, ch-stems only) ---")
    print("(Only paragraphs with ≥ 3 ch-stem words are classified)")

    # Precompute log prior and log likelihoods
    n_per_sect = {s: len(sections_paras[s]) for s in target_sections}
    total_paras = sum(n_per_sect.values())

    correct = 0
    total_classified = 0
    confusion = defaultdict(Counter)

    # Global smoothed word probabilities (add-1 smoothing)
    vocab_size = len(all_ch)

    for true_sect in target_sections:
        for p in sections_paras[true_sect]:
            ch_words_in_p = [w for w in p['words'] if is_ch_stem(w)]
            if len(ch_words_in_p) < 3:
                continue

            total_classified += 1
            scores = {}
            for sect in target_sections:
                # log P(sect)
                log_prior = math.log(n_per_sect[sect] / total_paras)
                # log P(w | sect) for each ch-word (Laplace smoothing)
                log_lik = 0
                sect_total = section_total_ch[sect]
                for w in ch_words_in_p:
                    p_w_given_sect = (section_ch_counts[sect].get(w, 0) + 1) / (sect_total + vocab_size)
                    log_lik += math.log(p_w_given_sect)
                scores[sect] = log_prior + log_lik

            predicted = max(scores, key=lambda s: scores[s])
            confusion[true_sect][predicted] += 1
            if predicted == true_sect:
                correct += 1

    accuracy = correct / total_classified if total_classified else 0
    baseline = 1 / len(target_sections)
    print(f"\nTotal classified: {total_classified}, Correct: {correct}")
    print(f"Accuracy: {accuracy:.1%} (baseline: {baseline:.1%})")

    print(f"\nConfusion matrix:")
    header = f"{'True\\Pred':<10}" + ''.join(f"{s[:6]:>8}" for s in target_sections)
    print(header)
    for true_sect in target_sections:
        row = f"{true_sect:<10}"
        for pred_sect in target_sections:
            row += f"{confusion[true_sect].get(pred_sect, 0):>8}"
        total_row = sum(confusion[true_sect].values())
        acc_row = confusion[true_sect].get(true_sect, 0) / total_row if total_row else 0
        print(row + f"  (acc={acc_row:.0%})")

    # Section-specific accuracy
    print(f"\nPer-section accuracy:")
    for sect in target_sections:
        n_classified = sum(confusion[sect].values())
        n_correct = confusion[sect].get(sect, 0)
        acc = n_correct / n_classified if n_classified else 0
        print(f"  {sect}: {n_correct}/{n_classified} = {acc:.1%}")


def h196_cross_dialect_ch_stems(paragraphs):
    """H196: Cross-dialect ch-stem comparison."""
    print("\n" + "=" * 70)
    print("H196: Cross-Dialect ch-Stem Vocabulary")
    print("=" * 70)

    herbal_a = Counter()
    stars_b = Counter()
    herbal_b = Counter()
    pharma_a = Counter()

    for p in paragraphs:
        sect = p['section']
        dial = p['dialect']
        ch_words = [w for w in p['words'] if is_ch_stem(w)]
        if sect == 'herbal' and dial == 'A':
            herbal_a.update(ch_words)
        elif sect == 'stars' and dial == 'B':
            stars_b.update(ch_words)
        elif sect == 'herbal' and dial == 'B':
            herbal_b.update(ch_words)
        elif sect == 'pharma' and dial == 'A':
            pharma_a.update(ch_words)

    print(f"\nHerbal A: {sum(herbal_a.values())} ch-words, {len(herbal_a)} unique")
    print(f"Stars B:  {sum(stars_b.values())} ch-words, {len(stars_b)} unique")
    print(f"Herbal B: {sum(herbal_b.values())} ch-words, {len(herbal_b)} unique")
    print(f"Pharma A: {sum(pharma_a.values())} ch-words, {len(pharma_a)} unique")

    # Vocabulary overlap
    ha_set = set(w for w, c in herbal_a.items() if c >= 2)
    sb_set = set(w for w, c in stars_b.items() if c >= 2)

    shared = ha_set & sb_set
    ha_only = ha_set - sb_set
    sb_only = sb_set - ha_set

    print(f"\nHerbal A (≥2) vs Stars B (≥2) vocabulary:")
    print(f"  Herbal A unique ≥2: {len(ha_set)}")
    print(f"  Stars B unique ≥2: {len(sb_set)}")
    print(f"  Shared: {len(shared)} ({len(shared)/max(len(ha_set),len(sb_set)):.1%})")
    print(f"  Herbal A only: {len(ha_only)}")
    print(f"  Stars B only: {len(sb_only)}")

    print(f"\n  Top shared ch-words (Herbal A & Stars B):")
    for w in sorted(shared, key=lambda x: -(herbal_a[x]+stars_b[x]))[:15]:
        print(f"    {w}: HA={herbal_a[w]}, SB={stars_b[w]}")

    print(f"\n  Top Stars B exclusive ch-words:")
    for w in sorted(sb_only, key=lambda x: -stars_b[x])[:12]:
        print(f"    {w}: SB={stars_b[w]}, HA={herbal_a.get(w, 0)}")

    print(f"\n  Top Herbal A exclusive ch-words:")
    for w in sorted(ha_only, key=lambda x: -herbal_a[x])[:12]:
        print(f"    {w}: HA={herbal_a[w]}, SB={stars_b.get(w, 0)}")

    # Common ch-words across all four groups
    common_all = set(herbal_a.keys()) & set(stars_b.keys()) & set(herbal_b.keys()) & set(pharma_a.keys())
    print(f"\n  ch-words appearing in ALL 4 groups (herbal_A, stars_B, herbal_B, pharma_A): {len(common_all)}")
    for w in sorted(common_all, key=lambda x: -herbal_a[x])[:10]:
        print(f"    {w}: HA={herbal_a[w]}, SB={stars_b[w]}, HB={herbal_b[w]}, PA={pharma_a[w]}")


def h199_zipfs_law(paragraphs):
    """H199: Zipf's law for Voynich word frequencies."""
    print("\n" + "=" * 70)
    print("H199: Zipf's Law Analysis")
    print("=" * 70)

    # Overall word frequency
    overall_freq = Counter()
    section_freq = defaultdict(Counter)

    for p in paragraphs:
        for w in p['words']:
            overall_freq[w] += 1
            section_freq[p['section']][w] += 1

    total_words = sum(overall_freq.values())
    vocab_size = len(overall_freq)

    print(f"\nTotal corpus: {total_words} words, {vocab_size} unique types")

    # Rank-frequency analysis
    ranked = sorted(overall_freq.values(), reverse=True)

    print(f"\nTop 30 words by frequency:")
    for word, cnt in overall_freq.most_common(30):
        rank = list(overall_freq.most_common()).index((word, cnt)) + 1
        print(f"  rank {rank:3d}: {word} = {cnt} ({cnt/total_words:.2%})")

    # Fit power law using log-log regression on ranks 1-500
    print(f"\nPower law fit (Zipf: log f = C - α × log r):")
    import statistics

    def fit_power_law(ranks, freqs):
        """Simple log-log linear regression."""
        log_r = [math.log(r) for r in ranks]
        log_f = [math.log(f) for f in freqs]
        n = len(ranks)
        mean_lr = statistics.mean(log_r)
        mean_lf = statistics.mean(log_f)
        cov = sum((lr - mean_lr) * (lf - mean_lf) for lr, lf in zip(log_r, log_f)) / n
        var_r = sum((lr - mean_lr) ** 2 for lr in log_r) / n
        alpha = -cov / var_r
        C = math.exp(mean_lf + alpha * mean_lr)
        return alpha, C

    # Overall
    for max_rank in [100, 500, 1000]:
        ranks_to_use = list(range(1, min(max_rank + 1, len(ranked) + 1)))
        freqs_to_use = ranked[:len(ranks_to_use)]
        alpha, C = fit_power_law(ranks_to_use, freqs_to_use)
        print(f"  Ranks 1-{max_rank}: α = {alpha:.3f} (Zipf exponent), C = {C:.1f}")

    # Expected: α ≈ 1/β where β is Heaps' law exponent
    # F111: Heaps' β ≈ 0.66-0.74 → expected α ≈ 1.35-1.52
    print(f"\n  Expected α from Heaps' β≈0.66-0.74: α ≈ {1/0.74:.2f}–{1/0.66:.2f}")

    # Section-specific Zipf
    print(f"\nSection-specific Zipf (ranks 1-100):")
    for sect in ['herbal', 'pharma', 'stars', 'cosmo']:
        sect_ranked = sorted(section_freq[sect].values(), reverse=True)
        if len(sect_ranked) < 50:
            continue
        n_words = sum(sect_ranked)
        n_types = len(sect_ranked)
        ranks = list(range(1, min(101, len(sect_ranked) + 1)))
        freqs = sect_ranked[:len(ranks)]
        try:
            alpha, C = fit_power_law(ranks, freqs)
            print(f"  {sect}: {n_words} words, {n_types} types, α={alpha:.3f}")
        except:
            print(f"  {sect}: fit failed")

    # Top words by section
    print(f"\nTop 10 words by section:")
    for sect in ['herbal', 'pharma', 'stars', 'cosmo']:
        top10 = section_freq[sect].most_common(10)
        print(f"\n  {sect}:")
        for w, cnt in top10:
            print(f"    {w}: {cnt}")

    # Word frequency distribution statistics
    print(f"\nWord frequency distribution:")
    hapaxes = sum(1 for _, c in overall_freq.items() if c == 1)
    dis = sum(1 for _, c in overall_freq.items() if c == 2)
    tris = sum(1 for _, c in overall_freq.items() if c == 3)
    print(f"  Hapax legomena (freq=1): {hapaxes} = {hapaxes/vocab_size:.1%} of vocabulary")
    print(f"  Dis legomena (freq=2): {dis} = {dis/vocab_size:.1%}")
    print(f"  Tris legomena (freq=3): {tris} = {tris/vocab_size:.1%}")
    print(f"  Top 100 words cover: {sum(ranked[:100])/total_words:.1%} of corpus")
    print(f"  Top 1000 words cover: {sum(ranked[:1000])/total_words:.1%} of corpus")


def main():
    print("Loading corpus...")
    paragraphs, folio_dialect = parse_corpus()

    total = len(paragraphs)
    a = sum(1 for p in paragraphs if p['dialect'] == 'A')
    b = sum(1 for p in paragraphs if p['dialect'] == 'B')
    total_words = sum(len(p['words']) for p in paragraphs)
    print(f"Total paragraphs: {total} (A={a}, B={b}), {total_words} words")

    h195_ch_stem_classifier(paragraphs)
    h196_cross_dialect_ch_stems(paragraphs)
    h199_zipfs_law(paragraphs)


if __name__ == '__main__':
    main()
