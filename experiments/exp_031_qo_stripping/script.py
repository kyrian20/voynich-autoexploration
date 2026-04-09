#!/usr/bin/env python3
"""
Experiment exp_031: qo-Stripping Analysis (H013)
Q followed by 'o' in 97.7% of word onsets. If "qo" is a grammatical prefix/article,
stripping it should reveal higher-entropy word stems.
Tests:
 1. H_initial before and after qo-stripping
 2. H2 of qo-words vs non-qo words (parallel corpora)
 3. Vocabulary diversity of qo-stripped vs full corpus
"""

import re
import math
from collections import Counter

ZL3B = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'
LATIN = '/Users/asash/voynich-cryptanalyst/data/reference_corpora/latin_vulgate.txt'

def parse_words(path, body_only=True):
    """Extract word tokens from IVTFF file."""
    words = []
    in_valid = True
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or line.startswith('<!'):
                continue
            if not re.match(r'^<f', line):
                continue
            # Extract locus and content
            m = re.match(r'^<[^>]+,([^>]+)>\s+(.*)', line)
            if not m:
                continue
            locus = m.group(1).strip()
            content = m.group(2).strip()

            if body_only:
                # Only body text loci (P0, etc.) — not labels, not markers
                if not re.match(r'^[+*@=/~&]?P[0-9]$', locus):
                    continue

            # Clean IVTFF markup
            content = re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]', '', content)
            content = re.sub(r'@\d+;[a-z]*', '', content)  # remove @NNN glyphs

            for token in content.split('.'):
                token = token.strip().strip(',').strip()
                if token and not token.startswith('@') and len(token) >= 1:
                    # Only pure EVA characters
                    if re.match(r'^[a-zA-Z\']+$', token):
                        words.append(token.lower())
    return words

def entropy(counter):
    """Shannon entropy from a Counter."""
    total = sum(counter.values())
    if total == 0: return 0.0
    return -sum((v/total) * math.log2(v/total) for v in counter.values() if v > 0)

def h2(word_list):
    """Bigram conditional entropy."""
    bigrams = Counter()
    unigrams = Counter()
    for w in word_list:
        for i in range(len(w)-1):
            bigrams[(w[i], w[i+1])] += 1
            unigrams[w[i]] += 1
    if not bigrams: return 0.0
    total = sum(bigrams.values())
    # H(next | current) = -sum p(a,b) log p(b|a)
    h = 0.0
    for (a, b), cnt in bigrams.items():
        p_ab = cnt / total
        p_b_given_a = cnt / unigrams[a]
        h -= p_ab * math.log2(p_b_given_a)
    return h

def main():
    words = parse_words(ZL3B, body_only=True)
    print(f"Total word tokens: {len(words)}")

    # Partition: qo-words vs non-qo words
    qo_words = [w for w in words if w.startswith('qo')]
    non_qo_words = [w for w in words if not w.startswith('qo')]
    qo_stripped = [w[2:] for w in qo_words if len(w) > 2]  # strip "qo" prefix
    qo_stripped_nonempty = [w for w in qo_stripped if len(w) >= 1]

    print(f"\nqo-words: {len(qo_words)} ({100*len(qo_words)/len(words):.1f}%)")
    print(f"non-qo words: {len(non_qo_words)} ({100*len(non_qo_words)/len(words):.1f}%)")
    print(f"qo-stripped stems: {len(qo_stripped_nonempty)} non-empty")

    # 1. Initial entropy
    def initial_entropy(word_list):
        first_chars = Counter(w[0] for w in word_list if w)
        return entropy(first_chars)

    h_init_full = initial_entropy(words)
    h_init_non_qo = initial_entropy(non_qo_words)
    h_init_qo_stems = initial_entropy(qo_stripped_nonempty)

    print(f"\n=== INITIAL CHARACTER ENTROPY ===")
    print(f"Full corpus H_initial: {h_init_full:.3f} bits")
    print(f"Non-qo words H_initial: {h_init_non_qo:.3f} bits")
    print(f"qo-stripped stems H_initial: {h_init_qo_stems:.3f} bits")
    print(f"  (qo-stems vs non-qo: delta = {h_init_qo_stems - h_init_non_qo:+.3f} bits)")

    # 2. Combined corpus with qo stripped
    hybrid_words = non_qo_words + qo_stripped_nonempty
    h_init_hybrid = initial_entropy(hybrid_words)
    print(f"Hybrid corpus (non-qo + qo-stripped) H_initial: {h_init_hybrid:.3f} bits")
    print(f"  Delta from original full corpus: {h_init_hybrid - h_init_full:+.3f} bits")

    # 3. Top initial chars in qo-stripped stems
    qo_stem_first = Counter(w[0] for w in qo_stripped_nonempty if w)
    total_stem = sum(qo_stem_first.values())
    print(f"\n=== TOP INITIAL CHARS OF qo-STRIPPED STEMS ===")
    print(f"{'Char':>6} | {'Count':>6} | {'Pct':>7}")
    print("-" * 30)
    for ch, cnt in qo_stem_first.most_common(15):
        print(f"  '{ch}' | {cnt:>6} | {100*cnt/total_stem:>6.1f}%")

    # 4. Top initial chars of non-qo words (for comparison)
    non_qo_first = Counter(w[0] for w in non_qo_words if w)
    total_nq = sum(non_qo_first.values())
    print(f"\n=== TOP INITIAL CHARS OF NON-qo WORDS (comparison) ===")
    for ch, cnt in non_qo_first.most_common(10):
        print(f"  '{ch}' | {cnt:>6} | {100*cnt/total_nq:>6.1f}%")

    # 5. Bigram entropy comparison
    print(f"\n=== BIGRAM ENTROPY (H2) ===")
    h2_full = h2(words)
    h2_non_qo = h2(non_qo_words)
    h2_stems = h2(qo_stripped_nonempty)
    h2_hybrid = h2(hybrid_words)
    print(f"Full corpus H2: {h2_full:.3f} bits")
    print(f"Non-qo words H2: {h2_non_qo:.3f} bits")
    print(f"qo-stripped stems H2: {h2_stems:.3f} bits")
    print(f"Hybrid corpus H2: {h2_hybrid:.3f} bits")

    # 6. Vocabulary analysis
    full_vocab = set(words)
    non_qo_vocab = set(non_qo_words)
    qo_stem_vocab = set(qo_stripped_nonempty)
    print(f"\n=== VOCABULARY DIVERSITY ===")
    print(f"Full vocab types: {len(full_vocab)}")
    print(f"Non-qo vocab types: {len(non_qo_vocab)}")
    print(f"qo-stripped stems vocab types: {len(qo_stem_vocab)}")
    print(f"qo-stems overlap with non-qo vocab: {len(qo_stem_vocab & non_qo_vocab)} types")
    overlap_pct = 100 * len(qo_stem_vocab & non_qo_vocab) / len(qo_stem_vocab) if qo_stem_vocab else 0
    print(f"  = {overlap_pct:.1f}% of qo-stems also appear as free words")

    # 7. Top qo-words and their stripped forms
    qo_word_freq = Counter(w for w in words if w.startswith('qo'))
    print(f"\n=== TOP 15 qo-WORDS AND THEIR STRIPPED FORMS ===")
    print(f"{'qo-word':>15} | {'Count':>6} | {'Stripped':>15} | {'Free word?'}")
    print("-" * 60)
    for w, cnt in qo_word_freq.most_common(15):
        stem = w[2:] if len(w) > 2 else '(empty)'
        is_free = stem in non_qo_vocab if stem != '(empty)' else False
        print(f"  {w:>13} | {cnt:>6} | {stem:>15} | {'YES' if is_free else 'no'}")

    # 8. KL divergence: qo-stem first-char vs non-qo first-char distribution
    all_chars = sorted(set(list(qo_stem_first.keys()) + list(non_qo_first.keys())))
    total_stem_v = sum(qo_stem_first.values())
    total_nq_v = sum(non_qo_first.values())
    kl = 0.0
    for ch in all_chars:
        p = qo_stem_first.get(ch, 0) / total_stem_v if total_stem_v > 0 else 0
        q = non_qo_first.get(ch, 0) / total_nq_v if total_nq_v > 0 else 0
        if p > 0 and q > 0:
            kl += p * math.log2(p/q)
    print(f"\n=== KL DIVERGENCE ===")
    print(f"KL(qo-stems || non-qo words) initial char distribution: {kl:.4f} bits")
    print("(0 = identical distributions, large = very different)")

    # 9. qo as article/particle: check if qo-words concentrate in certain sections
    print(f"\n=== qo-WORDS BY CURRIER SECTION ===")
    section_counts = {'A': Counter(), 'B': Counter(), 'unknown': Counter()}
    current_lang = 'unknown'
    with open(ZL3B, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if re.match(r'^<f\w+>', line) and '$L=' in line:
                lm = re.search(r'\$L=([AB])', line)
                current_lang = lm.group(1) if lm else 'unknown'
                continue
            if line.startswith('#') or line.startswith('<!'):
                continue
            m = re.match(r'^<[^>]+,([^>]+)>\s+(.*)', line)
            if not m: continue
            locus = m.group(1).strip()
            if not re.match(r'^[+*@=/~&]?P[0-9]$', locus): continue
            content = m.group(2)
            content = re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*', '', content)
            for token in content.split('.'):
                token = token.strip().strip(',').strip().lower()
                if token and re.match(r'^[a-z\']+$', token):
                    section_counts[current_lang][token] += 1

    for lang in ['A', 'B']:
        total_lang = sum(section_counts[lang].values())
        qo_lang = sum(v for k, v in section_counts[lang].items() if k.startswith('qo'))
        print(f"  Currier {lang}: {qo_lang}/{total_lang} = {100*qo_lang/total_lang:.1f}% qo-words")
        top_qo = [(k,v) for k,v in section_counts[lang].items() if k.startswith('qo')]
        top_qo.sort(key=lambda x: -x[1])
        for w, cnt in top_qo[:8]:
            print(f"    {w}: {cnt}")

if __name__ == '__main__':
    main()
