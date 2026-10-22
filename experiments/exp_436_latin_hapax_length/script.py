"""
exp_436: Hapax/Frequent Length Gradient in Latin vs VMS (H_new_E)

Q: Does Latin show the same hapax-longer/midfix-longer gradient as VMS (F435)?
   If yes: this is a universal statistical property, not VMS-specific.
   If no: VMS hapax structural anomaly is distinctive.

Method:
- Load Caesar's Gallic Wars (Latin), tokenize to words
- Compute word frequency
- Split into hapax/mid/frequent
- Measure word length by frequency class
- Compare ratio to VMS F435 ratios
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter
import math

LATIN_CORPUS = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/reference_corpora/latin/caesar_de_bello_gallico_latin.txt')

def tokenize_latin(text):
    """Extract Latin words (alpha only, lowercase, min 2 chars)."""
    words = re.findall(r'[a-zA-Z]+', text)
    return [w.lower() for w in words if len(w) >= 2]

def entropy(counts):
    total = sum(counts.values())
    if total == 0: return 0.0
    return -sum((c/total)*math.log2(c/total) for c in counts.values() if c > 0)

def analyze_freq_class(word_list, freq_class_name, word_counts):
    total = len(word_list)
    if total == 0:
        return
    # Word lengths
    lens = [len(w) for w in word_list]
    mean_len = sum(lens) / len(lens)
    
    # Latin "onset" = first 1-2 consonants; we'll just use word length as proxy
    # Also measure initial bigram distribution
    initials = Counter(w[:2] for w in word_list)
    init_H = entropy(initials)
    
    print(f"  [{freq_class_name}] N={total}")
    print(f"    Mean word length: {mean_len:.2f}")
    print(f"    Initial bigram entropy: {init_H:.2f} bits")
    
def main():
    with open(LATIN_CORPUS, encoding='utf-8', errors='ignore') as f:
        text = f.read()
    
    words = tokenize_latin(text)
    word_counts = Counter(words)
    
    total = len(words)
    n_types = len(word_counts)
    n_hapax = sum(1 for c in word_counts.values() if c == 1)
    print(f"Latin (Caesar): {total} tokens, {n_types} types, {n_hapax} hapax ({n_hapax/n_types:.1%} of types)")
    
    # Build frequency class lists
    hapax_list = [w for w in words if word_counts[w] == 1]
    mid_list   = [w for w in words if 2 <= word_counts[w] <= 4]
    freq_list  = [w for w in words if word_counts[w] >= 5]
    
    print(f"\n  hapax(f=1): N={len(hapax_list)} tokens")
    print(f"  mid(f=2-4): N={len(mid_list)} tokens")
    print(f"  freq(f>=5): N={len(freq_list)} tokens")
    
    for name, lst in [('hapax', hapax_list), ('mid(2-4)', mid_list), ('freq(>=5)', freq_list)]:
        if not lst:
            continue
        lens = [len(w) for w in lst]
        mean_len = sum(lens) / len(lens)
        initials = Counter(w[:2] for w in lst)
        init_H = entropy(initials)
        len_gt6 = sum(1 for l in lens if l > 6)
        len_le3 = sum(1 for l in lens if l <= 3)
        print(f"\n  [{name}] N={len(lst)}")
        print(f"    Mean word length: {mean_len:.2f}")
        print(f"    Initial bigram H: {init_H:.2f} bits")
        print(f"    Words >6 chars: {len_gt6/len(lst):.1%}")
        print(f"    Words ≤3 chars: {len_le3/len(lst):.1%}")
    
    # Hapax/freq length ratio
    hapax_len = sum(len(w) for w in hapax_list) / len(hapax_list) if hapax_list else 0
    freq_len = sum(len(w) for w in freq_list) / len(freq_list) if freq_list else 0
    print(f"\n  Hapax/freq mean length ratio: {hapax_len:.2f} / {freq_len:.2f} = {hapax_len/freq_len:.2f}×")
    print(f"  (VMS A: 6.33/4.47 = {6.33/4.47:.2f}×; VMS B: 6.59/4.96 = {6.59/4.96:.2f}×)")
    
    # Also check Italian for comparison
    import os
    italian_files = [
        str(_RepositoryPath(__file__).resolve().parents[2] / 'data/reference_corpora/italian/dante_divine_comedy_italian.txt')
    ]
    for fpath in italian_files:
        if os.path.exists(fpath):
            with open(fpath, encoding='utf-8', errors='ignore') as f:
                it_text = f.read()
            it_words = tokenize_latin(it_text)
            it_counts = Counter(it_words)
            it_total = len(it_words)
            it_types = len(it_counts)
            it_hapax_n = sum(1 for c in it_counts.values() if c == 1)
            print(f"\n=== Italian (Dante): {it_total} tokens, {it_types} types, {it_hapax_n} hapax ({it_hapax_n/it_types:.1%})")
            it_hapax = [w for w in it_words if it_counts[w] == 1]
            it_freq  = [w for w in it_words if it_counts[w] >= 5]
            it_h_len = sum(len(w) for w in it_hapax) / len(it_hapax) if it_hapax else 0
            it_f_len = sum(len(w) for w in it_freq) / len(it_freq) if it_freq else 0
            print(f"  Hapax mean len: {it_h_len:.2f}, Freq mean len: {it_f_len:.2f}, ratio: {it_h_len/it_f_len:.2f}×")

if __name__ == '__main__':
    main()
