"""
Experiment: exp_002_positional_entropy
Hypothesis tested: H001 — positional entropy analysis (h2 conditioned on position within word)
Also covers: H010 (q-initial removal), H011 (positional bias index)
Data: data/transcriptions/eva_zl3b.txt, data/reference_corpora/latin/virgil_aeneid_latin.txt,
      data/reference_corpora/italian/dante_divina_commedia.txt
Dependencies: numpy, matplotlib (optional, for visualisation stub)
"""

import re
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

random.seed(42)
BASE = Path(__file__).resolve().parents[2]


# ── Corpus parsers (reuse from exp_001) ───────────────────────────────────────

def parse_eva_zl3b(path):
    words_body, words_label = [], []
    with open(path, encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'^<[^>]+,([^>]+)>\s+(.*)', line)
            if not m:
                continue
            locus, text = m.group(1), m.group(2)
            # Strip locus prefix chars (=, *, +, @, &, -, dy) to get pure code
            locus_clean = re.sub(r'^[^A-Za-z]+', '', locus)
            # Clean text
            text = re.sub(r'<!.*?>', '', text)
            text = re.sub(r'<[^>]+>', '', text)
            text = text.replace('<%>', '').replace('<$>', '').replace('%', '')
            text = re.sub(r'\[([^:\]]+):[^\]]*\]', r'\1', text)
            text = re.sub(r'\{[^}]*\}', '', text)
            text = re.sub(r'@\d+;?', '', text)
            raw_words = re.split(r'[.\s]+', text)
            clean_words = [w for w in raw_words if w and re.match(r'^[a-zA-Z]+$', w)]
            is_label = locus_clean.startswith('L')
            if is_label:
                words_label.extend(clean_words)
            else:
                words_body.extend(clean_words)
    return words_body, words_label


def parse_natural_language(path):
    text = Path(path).read_text(encoding='utf-8', errors='replace')
    start = re.search(r'\*\*\* START OF', text)
    end = re.search(r'\*\*\* END OF', text)
    if start:
        text = text[start.end():]
    if end:
        text = text[:end.start()]
    return re.findall(r'[a-zA-Z]+', text.lower())


# ── Entropy utilities ──────────────────────────────────────────────────────────

def shannon_entropy(items):
    c = Counter(items)
    total = sum(c.values())
    if total == 0:
        return 0.0, 0
    return -sum((v/total)*math.log2(v/total) for v in c.values()), total


def bigram_conditional_entropy(chars):
    bigrams = [(chars[i], chars[i+1]) for i in range(len(chars)-1)]
    h_bi, _ = shannon_entropy(bigrams)
    h_uni, _ = shannon_entropy(chars)
    return h_bi - h_uni


# ── Positional entropy ────────────────────────────────────────────────────────

def positional_entropy_from_start(words, max_pos=10, min_words=50):
    """
    For each position i from word start (0 = first char, 1 = second, ...),
    collect all characters that appear at position i (across words of length > i).
    Return list of (position, entropy, count).
    """
    results = []
    for pos in range(max_pos):
        chars_at_pos = [w[pos] for w in words if len(w) > pos]
        if len(chars_at_pos) < min_words:
            break
        h, n = shannon_entropy(chars_at_pos)
        results.append((pos, h, n))
    return results


def positional_entropy_from_end(words, max_pos=10, min_words=50):
    """
    For each position i from word end (-1 = last char, -2 = second-to-last, ...).
    Returned as positive index: 0 = last, 1 = penultimate, etc.
    """
    results = []
    for pos in range(1, max_pos+1):
        chars_at_pos = [w[-pos] for w in words if len(w) >= pos]
        if len(chars_at_pos) < min_words:
            break
        h, n = shannon_entropy(chars_at_pos)
        results.append((pos, h, n))
    return results


def positional_bias_index(words, max_pos=10, min_words=50):
    """
    Positional bias: for each position, compute (shuffled H) - (actual H).
    Shuffled: shuffle characters within each word, then measure same position.
    High bias = position is more constrained than a random draw from the pool.
    """
    shuffled_words = []
    for w in words:
        chars = list(w)
        random.shuffle(chars)
        shuffled_words.append(''.join(chars))

    actual = positional_entropy_from_start(words, max_pos, min_words)
    shuffled = positional_entropy_from_start(shuffled_words, max_pos, min_words)

    results = []
    for (pos, h_actual, n), (_, h_shuffled, _) in zip(actual, shuffled):
        results.append((pos, h_actual, h_shuffled, h_shuffled - h_actual))
    return results


def entropy_by_word_length(words, min_count=50):
    """
    H2 computed separately for words of each length.
    Returns list of (length, h2, word_count).
    """
    by_length = defaultdict(list)
    for w in words:
        by_length[len(w)].append(w)

    results = []
    for length in sorted(by_length.keys()):
        wlist = by_length[length]
        if len(wlist) < min_count:
            continue
        # Flatten all characters from words of this length
        chars = list(''.join(wlist))
        h2 = bigram_conditional_entropy(chars)
        results.append((length, h2, len(wlist)))
    return results


# ── Q-initial analysis ────────────────────────────────────────────────────────

def q_initial_analysis(words):
    q_words = [w for w in words if w.startswith('q')]
    non_q_words = [w for w in words if not w.startswith('q')]

    # What follows q?
    q_followers = Counter(w[1] if len(w) > 1 else '<end>' for w in q_words)

    h_all, _ = shannon_entropy([w[0] for w in words])
    h_nonq, _ = shannon_entropy([w[0] for w in non_q_words])

    return {
        'q_count': len(q_words),
        'q_pct': 100 * len(q_words) / max(len(words), 1),
        'q_followers': q_followers.most_common(5),
        'H_initial_all': h_all,
        'H_initial_nonq': h_nonq,
    }


# ── Reporting ─────────────────────────────────────────────────────────────────

def print_positional(name, words, max_pos=10):
    print(f"\n── {name}: Positional entropy from word START ──")
    print(f"  {'Pos':>4}  {'H(char|pos)':>11}  {'N tokens':>9}  {'Top chars'}")
    from_start = positional_entropy_from_start(words, max_pos)
    for pos, h, n in from_start:
        chars_at = Counter(w[pos] for w in words if len(w) > pos)
        top = ', '.join(f"{c}({chars_at[c]/n*100:.0f}%)" for c,_ in chars_at.most_common(4))
        print(f"  {pos:>4}  {h:>11.4f}  {n:>9,}  {top}")

    print(f"\n── {name}: Positional entropy from word END ──")
    print(f"  {'End':>4}  {'H(char|pos)':>11}  {'N tokens':>9}")
    from_end = positional_entropy_from_end(words, max_pos)
    for pos, h, n in from_end:
        print(f"  {-pos:>4}  {h:>11.4f}  {n:>9,}")

    return from_start, from_end


def print_bias(name, words, max_pos=10):
    print(f"\n── {name}: Positional bias index (shuffled H - actual H) ──")
    print(f"  {'Pos':>4}  {'H_actual':>9}  {'H_shuffled':>10}  {'Bias':>7}")
    bias = positional_bias_index(words, max_pos)
    for pos, h_act, h_shuf, b in bias:
        print(f"  {pos:>4}  {h_act:>9.4f}  {h_shuf:>10.4f}  {b:>7.4f}")
    return bias


def print_length_entropy(name, words):
    print(f"\n── {name}: H2 by word length ──")
    print(f"  {'Length':>7}  {'H2':>7}  {'Words':>7}")
    by_len = entropy_by_word_length(words)
    for length, h2, n in by_len:
        print(f"  {length:>7}  {h2:>7.4f}  {n:>7,}")
    return by_len


# ── Main ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Experiment exp_002: Positional Entropy Analysis")
    print("Date: 2026-04-09\n")

    # Load corpora
    voynich_body, voynich_label = parse_eva_zl3b(BASE / 'data/transcriptions/eva_zl3b.txt')
    voynich_all = voynich_body + voynich_label
    print(f"Voynich: {len(voynich_all):,} words ({len(voynich_label):,} labels)")

    latin_words = parse_natural_language(BASE / 'data/reference_corpora/latin/virgil_aeneid_latin.txt')
    print(f"Latin (Virgil): {len(latin_words):,} words")

    # Supplement Latin with Caesar
    latin_caesar = parse_natural_language(BASE / 'data/reference_corpora/latin/caesar_de_bello_gallico_latin.txt')
    latin_combined = latin_words + latin_caesar
    print(f"Latin (Virgil+Caesar): {len(latin_combined):,} words")

    italian_words = parse_natural_language(BASE / 'data/reference_corpora/italian/dante_divina_commedia.txt')
    print(f"Italian (Dante): {len(italian_words):,} words")

    # ── Q-initial analysis ──
    print("\n" + "="*60)
    print("Q-INITIAL ANALYSIS (Voynich)")
    print("="*60)
    qa = q_initial_analysis(voynich_all)
    print(f"  q-initial words: {qa['q_count']:,} ({qa['q_pct']:.1f}%)")
    print(f"  q-followers: {qa['q_followers']}")
    print(f"  H_initial (all words):    {qa['H_initial_all']:.4f}")
    print(f"  H_initial (no-q words):   {qa['H_initial_nonq']:.4f}")

    # ── Positional entropy from start and end ──
    print("\n" + "="*60)
    print("POSITIONAL ENTROPY — FROM START AND END")
    print("="*60)
    voy_start, voy_end = print_positional("Voynich", voynich_all, max_pos=10)
    lat_start, lat_end = print_positional("Latin (Virgil+Caesar)", latin_combined, max_pos=10)
    ita_start, ita_end = print_positional("Italian (Dante)", italian_words, max_pos=10)

    # ── Positional bias ──
    print("\n" + "="*60)
    print("POSITIONAL BIAS INDEX (shuffled_H - actual_H)")
    print("="*60)
    voy_bias  = print_bias("Voynich", voynich_all)
    lat_bias  = print_bias("Latin", latin_combined)
    ita_bias  = print_bias("Italian", italian_words)

    # ── Length-conditioned entropy (H002) ──
    print("\n" + "="*60)
    print("H2 BY WORD LENGTH (testing H002)")
    print("="*60)
    voy_len = print_length_entropy("Voynich", voynich_all)
    lat_len = print_length_entropy("Latin", latin_combined)
    ita_len = print_length_entropy("Italian", italian_words)

    # ── Summary comparison table ──
    print("\n" + "="*60)
    print("SUMMARY: Positional H vs position (from start)")
    print("="*60)
    fmt = "{:<6} {:>10} {:>10} {:>10}"
    print(fmt.format("Pos", "Voynich", "Latin", "Italian"))
    print("-"*40)
    for i, (pos, h_v, _) in enumerate(voy_start[:8]):
        h_l = lat_start[i][1] if i < len(lat_start) else float('nan')
        h_i = ita_start[i][1] if i < len(ita_start) else float('nan')
        print(fmt.format(pos, f"{h_v:.3f}", f"{h_l:.3f}", f"{h_i:.3f}"))

    print("\nDone.")
