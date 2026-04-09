"""
Experiment: exp_008_stolfi_slot_entropy
Hypothesis: H006 — Stolfi prefix-midfix-suffix decomposition with per-slot entropy.
If stripping template slots leaves residual content with h2 ~3.0-3.5, the template
is adding redundancy to an underlying natural language.

Stolfi's classification (simplified from his 1997/2000 grammar):
- Crust: d, l, r, s, n, q (at word start only), m (at word end only), y, i, g, x, v, u, j
- Bench/Mantle: ch, sh, ee, e (context-dependent)
- Core: t, k, p, f (simple gallows) and their bench variants (cth, ckh, cph, cfh)
- Circle letters: a, o, y (appear in multiple positions)

Our approach: instead of implementing the full grammar, use the empirical per-position
character class analysis to identify "crust" positions (high constraint, outer layer)
and "core" positions (lower constraint, inner layer) based on exp_002 results.

Then compute:
1. Per-slot entropy: H for characters at each word position (already done in exp_002)
2. Entropy of the "core" characters only (stripping crust and bench chars from each word)
3. H2 of a corpus made only of the core-slot characters
"""
import re, math, random
from collections import Counter, defaultdict
from pathlib import Path

random.seed(42)
BASE = Path(__file__).resolve().parents[2]

# ── EVA character classes from Stolfi/Zattera ─────────────────────────────────
# In EVA notation within a processed word string:
# Crust (dealer) characters: d l r s n y g x (also q at word start, m at word end)
CRUST_CHARS = set('dlrsnyigxvujb')  # note: 'y' is also crust in Stolfi

# Bench (mantle) characters: sequences 'ch', 'sh', 'ee', lone 'e' in some positions
# In our processed words, these appear as individual chars 'c', 'h', 'e' in context
# We can't cleanly separate bench from non-bench without the full grammar.
# Instead, use a simplified approach: identify the "core" as the inner-most characters.

# Simple gallows (core): t k p f
CORE_SIMPLE = set('tkpf')
# Bench chars that precede/follow gallows:
BENCH_CHARS = set('che')  # simplified

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

def bigram_h2(chars):
    if len(chars) < 2: return 0.0
    bigrams = [(chars[i], chars[i+1]) for i in range(len(chars)-1)]
    return shannon_entropy(bigrams) - shannon_entropy(chars)


def extract_core_chars(word):
    """
    Extract the "core" characters from a word by:
    1. Strip leading crust characters (d, l, r, s, q, y, n at start)
    2. Strip trailing crust characters (y, n, m, d, l, r at end)
    3. What remains is the mantle+core region
    
    This is a simplified version of Stolfi's decomposition.
    """
    # Leading crust: characters that are dealers (d,l,r,s,n,y,q) at the start
    leading_crust = set('dlrsnygq')
    trailing_crust = set('ynmdlrs')
    
    start = 0
    while start < len(word) and word[start] in leading_crust:
        start += 1
    
    end = len(word)
    while end > start and word[end-1] in trailing_crust:
        end -= 1
    
    return word[start:end]  # mantle + core region


def extract_inner_core(word, min_len=4):
    """
    Extract what Stolfi calls the 'core' (gallows characters and their immediate context).
    Strategy: find the first gallows char within the word, take a window of ±1 around it.
    Returns the character at the gallows position and its immediate neighbors.
    """
    if len(word) < min_len:
        return None
    for i, c in enumerate(word):
        if c in CORE_SIMPLE:
            # Return the gallows + preceding + following char as context
            context = word[max(0,i-1):i+2]
            return context
    return None  # no gallows found


if __name__ == "__main__":
    print("Experiment exp_008: Stolfi Slot Entropy Analysis")
    print("Date: 2026-04-09\n")
    
    words = parse_eva_zl3b(BASE / 'data/transcriptions/eva_zl3b.txt')
    print(f"Total words: {len(words):,}")
    
    # ── Crust stripping ──────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("CRUST STRIPPING: MANTLE+CORE RESIDUAL ANALYSIS")
    print("="*60)
    
    core_regions = [extract_core_chars(w) for w in words]
    nonempty_cores = [c for c in core_regions if c]
    empty_count = sum(1 for c in core_regions if not c)
    single_count = sum(1 for c in core_regions if len(c) == 1)
    
    print(f"\n  Words processed: {len(words):,}")
    print(f"  Empty core (all crust): {empty_count:,} ({100*empty_count/len(words):.1f}%)")
    print(f"  Core length = 1: {single_count:,} ({100*single_count/len(words):.1f}%)")
    print(f"  Core length >= 2: {len(nonempty_cores)-single_count:,} ({100*(len(nonempty_cores)-single_count)/len(words):.1f}%)")
    
    # Length distribution of core regions
    core_lengths = Counter(len(c) for c in core_regions if c)
    print(f"\n  Core region length distribution:")
    for l in sorted(core_lengths.keys()):
        print(f"    len {l}: {core_lengths[l]:,} ({100*core_lengths[l]/len(words):.1f}%)")
    
    # Entropy of the core regions
    core_chars_flat = list(''.join(nonempty_cores))
    h1_core = shannon_entropy(core_chars_flat)
    h2_core = bigram_h2(core_chars_flat)
    
    # Entropy of the FULL words vs stripped words
    all_chars_flat = list(''.join(words))
    h2_full = bigram_h2(all_chars_flat)
    
    print(f"\n  Full corpus h2: {h2_full:.4f} bits")
    print(f"  Core-region h2: {h2_core:.4f} bits")
    print(f"  Core-region H1: {h1_core:.4f} bits")
    print(f"  Core unique chars: {len(set(core_chars_flat))}")
    
    # Core region top characters
    core_freq = Counter(core_chars_flat)
    total_core = sum(core_freq.values())
    print(f"\n  Core region character distribution (top 15):")
    for c, cnt in core_freq.most_common(15):
        print(f"    '{c}': {cnt:5d} ({100*cnt/total_core:.1f}%)")
    
    # ── Gallows contexts ─────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("GALLOWS CORE EXTRACTION (gallows + context window)")
    print("="*60)
    
    gallows_contexts = [extract_inner_core(w) for w in words]
    found_gallows = [c for c in gallows_contexts if c]
    print(f"\n  Words with gallows: {len(found_gallows):,} ({100*len(found_gallows)/len(words):.1f}%)")
    
    gallows_flat = list(''.join(found_gallows))
    h2_gallows = bigram_h2(gallows_flat)
    h1_gallows = shannon_entropy(gallows_flat)
    
    print(f"  Gallows context h2: {h2_gallows:.4f} bits")
    print(f"  Gallows context H1: {h1_gallows:.4f} bits")
    print(f"  Gallows context top chars: {Counter(gallows_flat).most_common(10)}")
    
    # ── Entropy by crust-stripping degree ───────────────────────────────────
    print("\n" + "="*60)
    print("ENTROPY LADDER: FULL → CRUST-STRIPPED → CORE-ONLY")
    print("="*60)
    
    # Full words
    full = list(''.join(words))
    
    # Strip only word-final y/n/m (most constrained final slot)
    strip_final = []
    for w in words:
        stripped = w.rstrip('ynm')
        if stripped:
            strip_final.append(stripped)
    stripped_flat = list(''.join(strip_final))
    
    # Strip leading q (qo-word onset)
    strip_q = [w[1:] if w.startswith('q') and len(w) > 1 else w for w in words]
    strip_q_flat = list(''.join(w for w in strip_q if w))
    
    # Core regions only (both ends stripped)
    core_only = list(''.join(nonempty_cores))
    
    for name, chars in [
        ("Full corpus", full),
        ("Strip final y/n/m", stripped_flat),
        ("Strip leading q", strip_q_flat),
        ("Core region (both ends stripped)", core_only),
    ]:
        h2 = bigram_h2(chars)
        h1 = shannon_entropy(chars)
        print(f"  {name:<35}: H1={h1:.4f}  H2={h2:.4f}")
    
    print(f"\n  Reference: Natural language h2 ≈ 3.4-3.5 bits")
    print("\nDone.")
