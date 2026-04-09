"""
Experiment: exp_003_label_body_entropy
Hypothesis tested: H009 — Entropy comparison between label text and running body text
Also covers: H012 (inner-slot character distribution), H013 (qo-as-token)
Data: data/transcriptions/eva_zl3b.txt
"""

import re
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

random.seed(42)
BASE = Path(__file__).resolve().parents[2]


# ── Shared utilities ──────────────────────────────────────────────────────────

def shannon_entropy(items):
    c = Counter(items)
    total = sum(c.values())
    if total == 0:
        return 0.0, 0
    return -sum((v/total)*math.log2(v/total) for v in c.values()), total

def bigram_conditional_entropy(chars):
    if len(chars) < 2:
        return 0.0
    bigrams = [(chars[i], chars[i+1]) for i in range(len(chars)-1)]
    h_bi, _ = shannon_entropy(bigrams)
    h_uni, _ = shannon_entropy(chars)
    return h_bi - h_uni

def word_type_entropy(words):
    """Entropy of the word-type distribution (lexical entropy)."""
    h, _ = shannon_entropy(words)
    return h

def type_token_ratio(words):
    return len(set(words)) / max(len(words), 1)


# ── EVA parser — returning locus categories ────────────────────────────────────

LOCUS_CATEGORIES = {
    'P': 'body',     # P0, P1, P2, Pt, Pb, Pc, Pr — paragraph text
    'L': 'label',    # La, Lb, Lc, Lf, Ln, Ls, Lt, Lx, Lz, L0 — labels
    'R': 'rider',    # Ri, Ro — rider text (marginal annotations)
    'C': 'circular', # Cc — circular text (ring labels, zodiac)
    'd': 'unknown',  # dy or similar
}

def parse_eva_with_locus(path):
    """
    Parse ZL3b returning a dict of locus_category → list of words.
    """
    by_locus = defaultdict(list)

    with open(path, encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'^<[^>]+,([^>]+)>\s+(.*)', line)
            if not m:
                continue
            locus, text = m.group(1), m.group(2)
            locus_clean = re.sub(r'^[^A-Za-z]+', '', locus)
            cat_char = locus_clean[0].upper() if locus_clean else '?'
            category = LOCUS_CATEGORIES.get(cat_char, 'other')

            # Clean text
            text = re.sub(r'<!.*?>', '', text)
            text = re.sub(r'<[^>]+>', '', text)
            text = text.replace('<%>', '').replace('<$>', '').replace('%', '')
            text = re.sub(r'\[([^:\]]+):[^\]]*\]', r'\1', text)
            text = re.sub(r'\{[^}]*\}', '', text)
            text = re.sub(r'@\d+;?', '', text)
            raw_words = re.split(r'[.\s]+', text)
            clean = [w for w in raw_words if w and re.match(r'^[a-zA-Z]+$', w)]
            by_locus[category].extend(clean)

    return by_locus


# ── Detailed entropy profile for a word list ──────────────────────────────────

def full_profile(name, words, reference_words=None):
    print(f"\n{'='*55}")
    print(f"  {name}")
    print(f"{'='*55}")
    if not words:
        print("  NO DATA")
        return {}

    chars = list(''.join(words))
    h1, _ = shannon_entropy(chars)
    h2 = bigram_conditional_entropy(chars)
    h_init, _ = shannon_entropy([w[0] for w in words])
    h_final, _ = shannon_entropy([w[-1] for w in words])
    h_lex = word_type_entropy(words)
    ttr = type_token_ratio(words)

    avg_len = sum(len(w) for w in words) / max(len(words), 1)
    len_dist = Counter(len(w) for w in words)

    # Top 5 words by frequency
    top_words = Counter(words).most_common(10)

    print(f"  Words (tokens):     {len(words):,}")
    print(f"  Words (types):      {len(set(words)):,}")
    print(f"  Type/Token ratio:   {ttr:.4f}")
    print(f"  Avg word length:    {avg_len:.2f}")
    print(f"  H1 (unigram):       {h1:.4f} bits")
    print(f"  H2 (conditional):   {h2:.4f} bits")
    print(f"  H_initial:          {h_init:.4f} bits")
    print(f"  H_final:            {h_final:.4f} bits")
    print(f"  H_lexical (word):   {h_lex:.4f} bits")

    print(f"\n  Word length distribution:")
    for length in sorted(len_dist.keys()):
        bar = '#' * int(len_dist[length] / max(len_dist.values()) * 30)
        print(f"    {length:>2}: {len_dist[length]:>5}  {bar}")

    print(f"\n  Top 10 words: {[f'{w}({c})' for w, c in top_words[:10]]}")

    # Most common initial chars
    init_c = Counter(w[0] for w in words)
    print(f"  Top initial chars: {init_c.most_common(6)}")

    # Most common final chars
    final_c = Counter(w[-1] for w in words)
    print(f"  Top final chars:   {final_c.most_common(6)}")

    return {
        'tokens': len(words),
        'types': len(set(words)),
        'ttr': ttr,
        'avg_len': avg_len,
        'h1': h1,
        'h2': h2,
        'h_initial': h_init,
        'h_final': h_final,
        'h_lexical': h_lex,
        'top_words': top_words,
        'top_initial': init_c.most_common(6),
        'top_final': final_c.most_common(6),
    }


# ── H012: Inner-slot character distribution ────────────────────────────────────

def inner_slot_analysis(words, pos_start=3, pos_end=5, min_len=6):
    """
    Collect characters at inner positions (default 3-4) from words of length >= min_len.
    """
    inner_chars = []
    for w in words:
        if len(w) >= min_len:
            inner_chars.extend(w[pos_start:pos_end])
    h, n = shannon_entropy(inner_chars)
    freq = Counter(inner_chars)
    total = sum(freq.values())
    return h, n, [(c, v, 100*v/total) for c, v in freq.most_common(15)]


# ── H013: qo-as-token analysis ────────────────────────────────────────────────

def qo_token_analysis(words):
    """
    Treat 'qo' at word start as a single prefix token. Strip it, analyse remainder.
    """
    stripped = []
    for w in words:
        if w.startswith('qo') and len(w) > 2:
            stripped.append(w[2:])  # remainder after qo
        elif w.startswith('q') and not w.startswith('qo'):
            stripped.append(w[1:])  # strip single q
        else:
            stripped.append(w)
    stripped = [w for w in stripped if w]  # remove empty

    h_init_orig, _ = shannon_entropy([w[0] for w in words])
    h_init_stripped, _ = shannon_entropy([w[0] for w in stripped if w])
    h2_orig = bigram_conditional_entropy(list(''.join(words)))
    h2_stripped = bigram_conditional_entropy(list(''.join(stripped)))

    return {
        'original_tokens': len(words),
        'stripped_tokens': len(stripped),
        'H_initial_original': h_init_orig,
        'H_initial_stripped': h_init_stripped,
        'H2_original': h2_orig,
        'H2_stripped': h2_stripped,
    }


# ── Vocabulary overlap between label and body ──────────────────────────────────

def vocabulary_overlap(words_a, words_b, name_a='A', name_b='B'):
    set_a = set(words_a)
    set_b = set(words_b)
    overlap = set_a & set_b
    print(f"\n  Vocabulary overlap ({name_a} vs {name_b}):")
    print(f"    Types in {name_a}: {len(set_a)}")
    print(f"    Types in {name_b}: {len(set_b)}")
    print(f"    Shared types:    {len(overlap)} ({100*len(overlap)/max(len(set_a),1):.1f}% of {name_a})")
    # Top shared words
    freq_a = Counter(words_a)
    shared_by_freq = sorted(overlap, key=lambda w: freq_a[w], reverse=True)[:10]
    print(f"    Top shared (by body freq): {shared_by_freq}")
    # Words exclusive to labels
    label_only = set_a - set_b
    body_only = set_b - set_a
    print(f"    Label-exclusive types: {len(label_only)}")
    print(f"    Body-exclusive types:  {len(body_only)}")
    return {'shared': len(overlap), 'label_only': len(label_only), 'body_only': len(body_only)}


# ── Main ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Experiment exp_003: Label vs Body Entropy / Inner-Slot Analysis / qo-Token")
    print("Date: 2026-04-09\n")

    by_locus = parse_eva_with_locus(BASE / 'data/transcriptions/eva_zl3b.txt')

    for cat, words in by_locus.items():
        print(f"  Category '{cat}': {len(words):,} words")

    # ── Main comparison: labels vs body ──
    label_words = by_locus.get('label', [])
    body_words  = by_locus.get('body', [])
    rider_words = by_locus.get('rider', [])
    circ_words  = by_locus.get('circular', [])
    all_words   = label_words + body_words + rider_words + circ_words

    r_body   = full_profile("BODY TEXT (paragraphs)", body_words)
    r_label  = full_profile("LABEL TEXT (annotations)", label_words)
    if rider_words:
        r_rider = full_profile("RIDER TEXT (marginal)", rider_words)
    if circ_words:
        r_circ  = full_profile("CIRCULAR TEXT", circ_words)

    # ── Vocabulary overlap ──
    print("\n" + "="*55)
    print("VOCABULARY OVERLAP ANALYSIS")
    print("="*55)
    overlap = vocabulary_overlap(label_words, body_words, 'labels', 'body')

    # ── Summary comparison table ──
    print("\n" + "="*55)
    print("SUMMARY COMPARISON")
    print("="*55)
    fmt = "{:<20} {:>8} {:>8} {:>8} {:>8} {:>8} {:>8}"
    print(fmt.format("Corpus", "Tokens", "Types", "TTR", "H1", "H2", "H_init"))
    print("-" * 70)
    for name, r in [("Body", r_body), ("Labels", r_label)]:
        if r:
            print(fmt.format(
                name,
                r['tokens'], r['types'],
                f"{r['ttr']:.3f}",
                f"{r['h1']:.3f}",
                f"{r['h2']:.3f}",
                f"{r['h_initial']:.3f}",
            ))

    # ── H012: Inner slot character distribution ──
    print("\n" + "="*55)
    print("H012: INNER SLOT CHARACTERS (positions 3-4, words ≥6)")
    print("="*55)
    for corpus_name, corpus_words in [("Body", body_words), ("Labels", label_words)]:
        h, n, freq = inner_slot_analysis(corpus_words, pos_start=3, pos_end=5, min_len=6)
        print(f"\n  {corpus_name}: H(inner)={h:.4f} bits, N={n:,} chars")
        print(f"  Character distribution at inner slots (pos 3-4):")
        for c, cnt, pct in freq[:12]:
            print(f"    '{c}': {cnt:5d}  ({pct:.1f}%)")

    # ── H013: qo-as-token ──
    print("\n" + "="*55)
    print("H013: QO-AS-TOKEN ANALYSIS (all words)")
    print("="*55)
    qo = qo_token_analysis(all_words)
    for k, v in qo.items():
        print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")

    print("\nDone.")
