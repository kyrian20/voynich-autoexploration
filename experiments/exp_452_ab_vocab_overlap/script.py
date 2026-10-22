"""
exp_452: A/B Shared Word-Type Vocabulary Overlap (H_new_N)
Q: What fraction of A word types also appear in B, and vice versa?
   Which onset classes show most/least cross-dialect sharing?
   Are common words shared while hapaxes are dialect-specific?

Method: Extract all unique word types from A and B folios separately.
Compute overlap fractions by onset class and by frequency tier.
"""
from pathlib import Path as _RepositoryPath
import re
from collections import defaultdict, Counter

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

ONSETS = ['qok','qot','qo','cth','ch','sh','ok','ot','ol','d','s','y','k','t','l','r','p','f','o']

def get_onset(word):
    for on in ONSETS:
        if word.startswith(on):
            return on
    return 'other'

def parse_corpus():
    pattern = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
    folios = defaultdict(list)
    with open(ZL3B, encoding='utf-8') as f:
        for line in f:
            for m in pattern.finditer(line):
                folio = m.group(1).lstrip('+*=&~')
                lc = m.group(3).lstrip('+*=/~&')
                if not lc.lstrip('@').startswith('P'):
                    continue
                text = m.group(4).strip()
                words = [w for w in re.split(r'[-.\s]', text)
                         if re.match(r'^[a-z]+$', w) and len(w) >= 2]
                if words:
                    folios[folio].append(words)
    return folios

def classify_dialects(folios):
    dialect = {}
    for folio, lines in folios.items():
        total = sum(len(ws) for ws in lines)
        if total == 0: continue
        edy = sum(1 for ws in lines for w in ws
                  if w.endswith('edy') or w.endswith('eedy'))
        dialect[folio] = 'B' if edy / total >= 0.05 else 'A'
    return dialect

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)

    # Collect word frequencies for each dialect
    a_freq = Counter()
    b_freq = Counter()
    for folio, lines in folios.items():
        if folio not in dialect_map:
            continue
        d = dialect_map[folio]
        for line_words in lines:
            for w in line_words:
                if d == 'A':
                    a_freq[w] += 1
                else:
                    b_freq[w] += 1

    a_types = set(a_freq.keys())
    b_types = set(b_freq.keys())
    shared = a_types & b_types
    a_only = a_types - b_types
    b_only = b_types - a_types

    print(f"=== A/B Vocabulary Overlap ===\n")
    print(f"A word types: {len(a_types):,}")
    print(f"B word types: {len(b_types):,}")
    print(f"Shared word types: {len(shared):,}")
    print(f"A-only: {len(a_only):,}")
    print(f"B-only: {len(b_only):,}")
    print(f"\nFraction of A types also in B: {len(shared)/len(a_types):.1%}")
    print(f"Fraction of B types also in A: {len(shared)/len(b_types):.1%}")

    # Total tokens in shared vs dialect-specific types
    a_shared_tokens = sum(a_freq[w] for w in shared)
    b_shared_tokens = sum(b_freq[w] for w in shared)
    a_total_tokens = sum(a_freq.values())
    b_total_tokens = sum(b_freq.values())
    print(f"\nToken coverage by shared types:")
    print(f"  A: {a_shared_tokens:,}/{a_total_tokens:,} = {a_shared_tokens/a_total_tokens:.1%} tokens are shared-type words")
    print(f"  B: {b_shared_tokens:,}/{b_total_tokens:,} = {b_shared_tokens/b_total_tokens:.1%} tokens are shared-type words")

    # Frequency tier analysis
    print(f"\n=== Overlap by frequency tier ===\n")
    tiers = [
        ('hapax (f=1)', lambda f, w: f[w] == 1),
        ('rare (f=2-4)', lambda f, w: 2 <= f[w] <= 4),
        ('medium (f=5-19)', lambda f, w: 5 <= f[w] <= 19),
        ('frequent (f≥20)', lambda f, w: f[w] >= 20),
        ('very frequent (f≥100)', lambda f, w: f[w] >= 100),
    ]
    print(f"{'Tier':<25} {'A types':>8} {'A in B':>7} {'A overlap':>10} | {'B types':>8} {'B in A':>7} {'B overlap':>10}")
    for tier_name, filter_fn in tiers:
        a_tier = {w for w in a_types if filter_fn(a_freq, w)}
        b_tier = {w for w in b_types if filter_fn(b_freq, w)}
        a_in_b = a_tier & b_types  # A-tier words that appear in B (at any freq)
        b_in_a = b_tier & a_types
        print(f"{tier_name:<25} {len(a_tier):>8} {len(a_in_b):>7} {len(a_in_b)/len(a_tier) if a_tier else 0:>10.1%} | "
              f"{len(b_tier):>8} {len(b_in_a):>7} {len(b_in_a)/len(b_tier) if b_tier else 0:>10.1%}")

    # Onset class analysis
    print(f"\n=== Overlap by onset class ===\n")
    print(f"{'Onset':<8} {'A types':>8} {'B types':>8} {'Shared':>8} {'A→B':>7} {'B→A':>7} {'Jaccard':>8}")
    onset_results = []
    for onset in ONSETS:
        a_o = {w for w in a_types if get_onset(w) == onset}
        b_o = {w for w in b_types if get_onset(w) == onset}
        shared_o = a_o & b_o
        union_o = a_o | b_o
        jaccard = len(shared_o) / len(union_o) if union_o else 0
        a_to_b = len(shared_o) / len(a_o) if a_o else 0
        b_to_a = len(shared_o) / len(b_o) if b_o else 0
        onset_results.append((onset, len(a_o), len(b_o), len(shared_o), a_to_b, b_to_a, jaccard))

    onset_results.sort(key=lambda x: -x[6])  # sort by Jaccard
    for (onset, na, nb, ns, atob, btoa, jacc) in onset_results:
        if na >= 5 or nb >= 5:
            print(f"{onset:<8} {na:>8} {nb:>8} {ns:>8} {atob:>7.1%} {btoa:>7.1%} {jacc:>8.3f}")

    # Top shared words (sorted by combined A+B frequency)
    print(f"\n=== Top 30 shared words (by combined A+B frequency) ===\n")
    shared_combined = [(w, a_freq[w] + b_freq[w], a_freq[w], b_freq[w]) for w in shared]
    shared_combined.sort(key=lambda x: -x[1])
    print(f"{'word':<15} {'A_freq':>8} {'B_freq':>8} {'combined':>10}")
    for w, combined, af, bf in shared_combined[:30]:
        print(f"{w:<15} {af:>8} {bf:>8} {combined:>10}")

    # Top A-only words (high freq in A, absent from B)
    print(f"\n=== Top A-only words (≥10 occurrences in A, absent from B) ===\n")
    a_only_highfreq = [(w, a_freq[w]) for w in a_only if a_freq[w] >= 10]
    a_only_highfreq.sort(key=lambda x: -x[1])
    print(f"{'word':<15} {'A_freq':>8}  onset")
    for w, f in a_only_highfreq[:20]:
        print(f"{w:<15} {f:>8}  {get_onset(w)}")

    # Top B-only words (high freq in B, absent from A)
    print(f"\n=== Top B-only words (≥10 occurrences in B, absent from A) ===\n")
    b_only_highfreq = [(w, b_freq[w]) for w in b_only if b_freq[w] >= 10]
    b_only_highfreq.sort(key=lambda x: -x[1])
    print(f"{'word':<15} {'B_freq':>8}  onset")
    for w, f in b_only_highfreq[:20]:
        print(f"{w:<15} {f:>8}  {get_onset(w)}")

    # For high-frequency shared words: A/B frequency ratio
    print(f"\n=== High-frequency shared words: A/B usage ratio ===\n")
    print(f"{'word':<15} {'A_freq':>8} {'B_freq':>8} {'A/B_ratio':>10} onset")
    high_shared = [(w, a_freq[w], b_freq[w]) for w in shared
                   if a_freq[w] >= 20 or b_freq[w] >= 20]
    high_shared.sort(key=lambda x: x[2]/x[1] if x[1] > 0 else 999)
    for w, af, bf in high_shared[:20]:
        ratio = af / bf if bf > 0 else float('inf')
        print(f"{w:<15} {af:>8} {bf:>8} {ratio:>10.2f} {get_onset(w)}")

if __name__ == '__main__':
    main()
