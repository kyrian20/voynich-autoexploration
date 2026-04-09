"""
Experiment: exp_007_verbose_cipher_control
Purpose: Control test for exp_006 adjacent-pair grouping.
Apply the same grouping to Latin and Italian corpora to check:
1. Does pairing natural language text ALSO overshoot h2 above NL range?
2. What is the characteristic "paired" h2 for natural language vs. Voynich?
3. Apply pairing to a KNOWN verbose cipher control (English with every other char replaced
   by a dummy) to calibrate what a true verbose cipher "looks like" after pairing.
"""
import re, math, random
from collections import Counter
from pathlib import Path

random.seed(42)
BASE = Path(__file__).resolve().parents[2]

def parse_natural_language(path):
    text = Path(path).read_text(encoding='utf-8', errors='replace')
    start = re.search(r'\*\*\* START OF', text)
    end   = re.search(r'\*\*\* END OF', text)
    if start: text = text[start.end():]
    if end:   text = text[:end.start()]
    return re.findall(r'[a-zA-Z]+', text.lower())

def parse_eva_zl3b(path):
    words = []
    with open(path, encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'^<[^>]+,([^>]+)>\s+(.*)', line)
            if not m: continue
            text = m.group(2)
            text = re.sub(r'<!.*?>', '', text)
            text = re.sub(r'<[^>]+>', '', text)
            text = text.replace('<%>','').replace('<$>','').replace('%','')
            text = re.sub(r'\[([^:\]]+):[^\]]*\]', r'\1', text)
            text = re.sub(r'\{[^}]*\}', '', text)
            text = re.sub(r'@\d+;?', '', text)
            words.extend(w for w in re.split(r'[.\s]+', text) if w and re.match(r'^[a-zA-Z]+$', w))
    return words

def shannon_entropy(items):
    c = Counter(items)
    total = sum(c.values())
    if total == 0: return 0.0
    return -sum((v/total)*math.log2(v/total) for v in c.values())

def bigram_h2(tokens):
    if len(tokens) < 2: return 0.0
    bigrams = [(tokens[i], tokens[i+1]) for i in range(len(tokens)-1)]
    return shannon_entropy(bigrams) - shannon_entropy(tokens)

def apply_pair_grouping(words):
    all_tokens = []
    for w in words:
        i = 0
        while i < len(w) - 1:
            all_tokens.append(w[i:i+2])
            i += 2
        if i < len(w):
            all_tokens.append(w[i])
    return all_tokens

def make_verbose_cipher(words, filler='x'):
    """
    Simulate a simple verbose cipher: every plaintext char is followed by a fixed filler.
    E.g., 'cat' -> 'cxaxtx'
    Returns words with doubled length.
    """
    return [re.sub(r'(.)', r'\1' + filler, w) for w in words]

def make_random_verbose_cipher(words):
    """Simulate verbose cipher with random filler characters."""
    fillers = 'aeioubc'  # restricted filler set
    result = []
    for w in words:
        out = ''
        for c in w:
            out += c + random.choice(fillers)
        result.append(out)
    return result

def profile(name, words):
    chars = list(''.join(words))
    h2_base = bigram_h2(chars)
    paired_tokens = apply_pair_grouping(words)
    h2_paired = bigram_h2(paired_tokens)
    n_unique_base = len(set(chars))
    n_unique_paired = len(set(paired_tokens))
    top_pairs = Counter(paired_tokens).most_common(8)
    print(f"\n  {name}:")
    print(f"    Words: {len(words):,}  Chars: {len(chars):,}")
    print(f"    Baseline h2: {h2_base:.4f}  Unique chars: {n_unique_base}")
    print(f"    Paired h2:   {h2_paired:.4f}  Unique pairs: {n_unique_paired}  (gain: {h2_paired-h2_base:+.4f})")
    print(f"    Top pairs: {top_pairs}")
    return h2_base, h2_paired

if __name__ == "__main__":
    print("Experiment exp_007: Verbose Cipher Control Test")
    print("Date: 2026-04-09\n")

    voynich_words = parse_eva_zl3b(BASE / 'data/transcriptions/eva_zl3b.txt')
    latin_words   = parse_natural_language(BASE / 'data/reference_corpora/latin/virgil_aeneid_latin.txt')
    latin_words  += parse_natural_language(BASE / 'data/reference_corpora/latin/caesar_de_bello_gallico_latin.txt')
    italian_words = parse_natural_language(BASE / 'data/reference_corpora/italian/dante_divina_commedia.txt')

    # Verbose cipher simulations on Italian
    italian_verbose_fixed   = make_verbose_cipher(italian_words, filler='x')
    italian_verbose_random  = make_random_verbose_cipher(italian_words)

    print("="*60)
    print("ADJACENT-PAIR GROUPING: Natural Language vs Voynich vs Simulated Verbose Cipher")
    print("="*60)

    results = {}
    for name, words in [
        ("Voynich (EVA)",            voynich_words),
        ("Latin (Virgil+Caesar)",    latin_words[:len(voynich_words)]),
        ("Italian (Dante)",          italian_words[:len(voynich_words)]),
        ("Italian verbose-x (sim)",  italian_verbose_fixed[:len(voynich_words)]),
        ("Italian verbose-rand(sim)",italian_verbose_random[:len(voynich_words)]),
    ]:
        h2b, h2p = profile(name, words)
        results[name] = (h2b, h2p)

    print("\n" + "="*60)
    print("SUMMARY TABLE")
    print("="*60)
    fmt = "{:<32} {:>8} {:>8} {:>8}"
    print(fmt.format("Corpus", "H2_base", "H2_pair", "Gain"))
    print("-"*60)
    for name, (h2b, h2p) in results.items():
        print(fmt.format(name, f"{h2b:.4f}", f"{h2p:.4f}", f"{h2p-h2b:+.4f}"))

    print("\n  Key question: Does pairing ALWAYS overshoot NL h2, or is Voynich special?")
    print("Done.")
