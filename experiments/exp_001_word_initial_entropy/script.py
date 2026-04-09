"""
Experiment: exp_001_word_initial_entropy
Hypothesis tested: H003 — Word-initial character entropy
Data: data/transcriptions/eva_zl3b.txt, data/reference_corpora/latin/vulgate.txt,
      data/reference_corpora/italian/dante_divina_commedia.txt
Dependencies: numpy (standard)
"""

import re
import math
import random
from collections import Counter
from pathlib import Path

random.seed(42)
BASE = Path(__file__).resolve().parents[2]

# ── EVA corpus parser ──────────────────────────────────────────────────────────

def parse_eva_zl3b(path):
    """
    Parse IVTFF EVA file into lists of clean word tokens.
    Returns (words, initial_chars, labels) where labels mark line type.
    Line locus codes: P0/P1/P2 = paragraph body, Pt = paragraph end,
    La/Lb = labels (short annotations next to illustrations), etc.
    """
    words_body = []    # body paragraph text
    words_label = []   # label text (La, Lb, Lc locus codes)

    with open(path, encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Match locus header: <fN.linenum,locus>  text
            m = re.match(r'^<[^>]+,([^>]+)>\s+(.*)', line)
            if not m:
                continue
            locus, text = m.group(1), m.group(2)

            # Strip comments within the text line
            text = re.sub(r'<!.*?>', '', text)
            text = re.sub(r'<[^>]+>', '', text)
            # Remove paragraph markers
            text = text.replace('<%>', '').replace('<$>', '').replace('%', '')
            # Resolve uncertainty markers: [a:b] → keep first option
            text = re.sub(r'\[([^:\]]+):[^\]]*\]', r'\1', text)
            # Remove remaining uncertain readings {xx}
            text = re.sub(r'\{[^}]*\}', '', text)
            # Remove @NNN glyph codes
            text = re.sub(r'@\d+;?', '', text)
            # Split on word separators (. and space)
            raw_words = re.split(r'[.\s]+', text)
            # Filter: only keep words with purely alphabetic EVA characters
            clean_words = [w for w in raw_words
                          if w and re.match(r'^[a-zA-Z]+$', w)]

            is_label = locus.startswith('L')  # La, Lb, Lc etc.
            if is_label:
                words_label.extend(clean_words)
            else:
                words_body.extend(clean_words)

    return words_body, words_label


def parse_natural_language(path, strip_gutenberg=True):
    """
    Parse a plain-text corpus into word tokens.
    Strips non-alphabetic characters, lowercases.
    """
    text = Path(path).read_text(encoding='utf-8', errors='replace')
    if strip_gutenberg:
        # Remove Gutenberg header/footer heuristically
        start = re.search(r'\*\*\* START OF', text)
        end = re.search(r'\*\*\* END OF', text)
        if start:
            text = text[start.end():]
        if end:
            text = text[:end.start()]
    words = re.findall(r'[a-zA-Z]+', text.lower())
    return words


# ── Entropy computation ────────────────────────────────────────────────────────

def shannon_entropy(items):
    """Shannon entropy in bits of a sequence of items."""
    c = Counter(items)
    total = sum(c.values())
    if total == 0:
        return 0.0
    return -sum((v/total) * math.log2(v/total) for v in c.values())


def bigram_conditional_entropy(chars):
    """
    h2 = H(char | prev_char) = H(bigram) - H(unigram).
    Computed from a flat sequence of characters (one per item in chars).
    """
    bigrams = [(chars[i], chars[i+1]) for i in range(len(chars)-1)]
    h_bigram = shannon_entropy(bigrams)
    h_unigram = shannon_entropy(chars)
    return h_bigram - h_unigram


def word_chars(words):
    """Flatten words into a single character sequence (no word-boundary markers)."""
    return list(''.join(words))


def word_initial_chars(words):
    return [w[0] for w in words if w]


# ── Shuffled control ───────────────────────────────────────────────────────────

def shuffle_within_words(words):
    """Shuffle characters within each word (preserving word lengths)."""
    result = []
    for w in words:
        chars = list(w)
        random.shuffle(chars)
        result.append(''.join(chars))
    return result


# ── Main ───────────────────────────────────────────────────────────────────────

def report(name, words, label=""):
    if not words:
        print(f"  {name}: NO DATA")
        return {}
    chars = word_chars(words)
    initials = word_initial_chars(words)
    shuffled = shuffle_within_words(words)
    shuffled_initials = word_initial_chars(shuffled)

    h1 = shannon_entropy(chars)
    h2 = bigram_conditional_entropy(chars)
    h_init = shannon_entropy(initials)
    h_init_shuffled = shannon_entropy(shuffled_initials)

    print(f"\n{'='*55}")
    print(f"  {name}{' ['+label+']' if label else ''}")
    print(f"{'='*55}")
    print(f"  Words:               {len(words):,}")
    print(f"  Characters:          {len(chars):,}")
    print(f"  Unique word-initial: {len(set(initials))}")
    print(f"  H1 (unigram):        {h1:.4f} bits")
    print(f"  H2 (conditional):    {h2:.4f} bits")
    print(f"  H_initial (actual):  {h_init:.4f} bits")
    print(f"  H_initial (shuffled):{h_init_shuffled:.4f} bits")
    print(f"  Initial vs H2 gap:   {h_init - h2:+.4f} bits")

    # Top 10 word-initial characters and their frequencies
    init_freq = Counter(initials)
    total = sum(init_freq.values())
    top = init_freq.most_common(10)
    print(f"\n  Top word-initial characters:")
    for ch, cnt in top:
        print(f"    '{ch}': {cnt:5d}  ({100*cnt/total:.1f}%)")

    return {
        "words": len(words),
        "h1": h1,
        "h2": h2,
        "h_initial": h_init,
        "h_initial_shuffled": h_init_shuffled,
        "unique_initials": len(set(initials)),
        "top_initials": {ch: cnt for ch, cnt in top}
    }


if __name__ == "__main__":
    print("Experiment exp_001: Word-Initial Character Entropy")
    print("Date: 2026-04-09\n")

    # ── Voynich ──
    voynich_body, voynich_label = parse_eva_zl3b(
        BASE / 'data/transcriptions/eva_zl3b.txt'
    )
    voynich_all = voynich_body + voynich_label

    r_voynich_all   = report("Voynich (all)",    voynich_all)
    r_voynich_body  = report("Voynich (body)",   voynich_body,  "body paragraphs")
    r_voynich_label = report("Voynich (labels)", voynich_label, "label text only")

    # ── Latin ──
    latin_words = parse_natural_language(
        BASE / 'data/reference_corpora/latin/vulgate.txt'
    )
    r_latin = report("Latin (Vulgate)", latin_words)

    # ── Italian ──
    italian_words = parse_natural_language(
        BASE / 'data/reference_corpora/italian/dante_divina_commedia.txt'
    )
    r_italian = report("Italian (Dante)", italian_words)

    # ── Summary table ──
    print(f"\n\n{'='*55}")
    print("  SUMMARY TABLE")
    print(f"{'='*55}")
    fmt = "{:<28} {:>7} {:>7} {:>7} {:>8}"
    print(fmt.format("Corpus", "H1", "H2", "H_init", "init-H2"))
    print("-" * 55)
    for name, r in [
        ("Voynich all",    r_voynich_all),
        ("Voynich body",   r_voynich_body),
        ("Voynich labels", r_voynich_label),
        ("Latin Vulgate",  r_latin),
        ("Italian Dante",  r_italian),
    ]:
        if r:
            print(fmt.format(
                name,
                f"{r['h1']:.3f}",
                f"{r['h2']:.3f}",
                f"{r['h_initial']:.3f}",
                f"{r['h_initial']-r['h2']:+.3f}"
            ))

    print("\nDone.")
