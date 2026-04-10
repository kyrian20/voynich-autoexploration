#!/usr/bin/env python3
"""
exp_146: B-Dialect sh/ch_e Positional Parallel to A-Dialect cth
H289: Does sh/ch_e in B show same positional profile as cth in A?
H290: What B-particle (if any) precedes l-onset at elevated enrichment?

Checks:
1. Positional distribution (LF/second/MID/LL/only) of sh and ch_e in B vs A-cth
2. d-onset enrichment before sh/ch_e in B (parallel to d before cthol=1.51× in A)
3. Self-succession: sh→sh and ch_e→ch_e enrichment in B
4. B-particle → l-onset transition matrix
"""

import re
from collections import defaultdict

CORPUS_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"

ONSET_CLASSES = [
    ('qok', re.compile(r'^qok')),
    ('qot', re.compile(r'^qot')),
    ('qo',  re.compile(r'^qo')),
    ('cth', re.compile(r'^cth')),
    ('ch_e',re.compile(r'^che')),
    ('ch',  re.compile(r'^ch')),
    ('sh',  re.compile(r'^sh')),
    ('ok',  re.compile(r'^ok')),
    ('ot',  re.compile(r'^ot')),
    ('ol',  re.compile(r'^ol')),
    ('d',   re.compile(r'^d')),
    ('s',   re.compile(r'^s')),
    ('y',   re.compile(r'^y')),
    ('k',   re.compile(r'^k')),
    ('t',   re.compile(r'^t')),
    ('l',   re.compile(r'^l')),
    ('r',   re.compile(r'^r')),
    ('p',   re.compile(r'^p')),
    ('f',   re.compile(r'^f')),
    ('other', re.compile(r'.')),
]

def get_onset(word):
    for cls, pat in ONSET_CLASSES:
        if pat.match(word):
            return cls
    return 'other'

def get_folio_dialect(folio_base, folio_words):
    if len(folio_words) < 10:
        return 'unknown'
    b_count = sum(1 for w in folio_words if w.endswith('edy') or w.endswith('eedy'))
    return 'B' if b_count / len(folio_words) >= 0.05 else 'A'

def positional_slot(i, n):
    if n == 1:
        return 'only'
    if i == 0:
        return 'LF'
    if i == n - 1:
        return 'LL'
    if i == 1 and n > 2:
        return 'second'
    return 'MID'

def parse_corpus():
    """Return per-folio word lists and per-line word lists."""
    folio_words = defaultdict(list)
    lines_by_dialect = defaultdict(list)  # 'A' or 'B' -> list of (words_in_line, folio_base)

    # First pass: get folio words for dialect assignment
    raw_lines = []
    with open(CORPUS_PATH, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split(' ', 1)
            if len(parts) < 2:
                continue
            locus_raw = parts[0]
            text = parts[1]
            locus_parts = locus_raw.split(',')
            if len(locus_parts) < 2:
                continue
            folio_str = locus_parts[0]
            locus_type_raw = locus_parts[1]
            locus_type = locus_type_raw.lstrip('@+*=~&')
            folio_base = folio_str.split('.')[0]
            words = [w for w in text.split('.') if re.match(r'[a-z]', w)]
            if not words:
                continue
            folio_words[folio_base].extend(words)
            raw_lines.append((folio_base, locus_type, words))

    # Assign dialects
    dialect_map = {}
    for fb, words in folio_words.items():
        dialect_map[fb] = get_folio_dialect(fb, words)

    # Organize lines by dialect
    for folio_base, locus_type, words in raw_lines:
        d = dialect_map.get(folio_base, 'unknown')
        if d in ('A', 'B') and locus_type.startswith('P'):
            lines_by_dialect[d].append(words)

    return folio_words, lines_by_dialect, dialect_map

def analyze_positional(lines, target_onsets, label):
    """Compute positional distribution for target onset classes."""
    slot_counts = defaultdict(lambda: defaultdict(int))
    total_by_slot = defaultdict(int)

    for words in lines:
        n = len(words)
        for i, w in enumerate(words):
            onset = get_onset(w)
            slot = positional_slot(i, n)
            total_by_slot[slot] += 1
            if onset in target_onsets:
                slot_counts[onset][slot] += 1

    print(f"\n{label}")
    print(f"{'Word class':<10} {'n':>6} {'LF%':>7} {'2nd%':>7} {'MID%':>7} {'LL%':>7} {'only%':>7}")
    print("-" * 55)

    slot_order = ['LF', 'second', 'MID', 'LL', 'only']
    baseline = {s: total_by_slot[s] / sum(total_by_slot.values()) for s in slot_order}

    # Print baseline
    total = sum(total_by_slot.values())
    print(f"{'BASELINE':<10} {total:>6} " + " ".join(f"{baseline[s]*100:>6.1f}%" for s in slot_order))

    for onset in target_onsets:
        cnts = slot_counts[onset]
        n_onset = sum(cnts.values())
        if n_onset == 0:
            continue
        rates = {s: cnts.get(s, 0) / n_onset for s in slot_order}
        enrichments = {s: rates[s] / baseline[s] if baseline[s] > 0 else 0 for s in slot_order}
        rate_str = " ".join(f"{rates[s]*100:>6.1f}%" for s in slot_order)
        print(f"{onset:<10} {n_onset:>6} {rate_str}")
        enr_str = " ".join(f"({enrichments[s]:.2f}×)" for s in slot_order)
        print(f"{'':10} {'enrich':>6} {enr_str}")

    return slot_counts, total_by_slot

def analyze_before_context(lines, target_onset, label):
    """Enrichment of each onset class BEFORE target_onset words."""
    before_counts = defaultdict(int)
    total_bigrams = 0
    onset_baseline = defaultdict(int)
    total_words = 0

    for words in lines:
        n = len(words)
        for i, w in enumerate(words):
            onset_baseline[get_onset(w)] += 1
            total_words += 1
            if i > 0 and get_onset(w) == target_onset:
                before_counts[get_onset(words[i-1])] += 1
                total_bigrams += 1

    print(f"\n{label} (before-context, n_target={total_bigrams})")
    print(f"{'Before onset':<12} {'n':>5} {'obs%':>7} {'base%':>7} {'enrich':>8}")
    print("-" * 45)

    for onset_cls, _ in ONSET_CLASSES[:15]:  # top 15 classes
        obs = before_counts[onset_cls]
        obs_rate = obs / total_bigrams if total_bigrams > 0 else 0
        base_rate = onset_baseline[onset_cls] / total_words if total_words > 0 else 0
        enrich = obs_rate / base_rate if base_rate > 0 else 0
        if obs > 0 or base_rate > 0.02:
            print(f"{onset_cls:<12} {obs:>5} {obs_rate*100:>6.1f}% {base_rate*100:>6.1f}% {enrich:>7.2f}×")

def analyze_self_succession(lines, target_onset, label):
    """Self-succession enrichment for target onset class."""
    self_bigrams = 0
    total_after = 0
    baseline_onset = 0
    total_words = 0

    for words in lines:
        for i, w in enumerate(words):
            onset = get_onset(w)
            total_words += 1
            if onset == target_onset:
                baseline_onset += 1
            if i > 0 and get_onset(words[i-1]) == target_onset:
                total_after += 1
                if onset == target_onset:
                    self_bigrams += 1

    baseline_rate = baseline_onset / total_words if total_words > 0 else 0
    obs_rate = self_bigrams / total_after if total_after > 0 else 0
    enrichment = obs_rate / baseline_rate if baseline_rate > 0 else 0

    print(f"\n{label} self-succession: {self_bigrams}/{total_after} = {obs_rate*100:.1f}% (baseline={baseline_rate*100:.1f}%, enrichment={enrichment:.2f}×)")

def analyze_l_onset_determiners(lines, label):
    """For B-dialect: which particles precede l-onset words most?"""
    before_l = defaultdict(int)
    before_l_specific = defaultdict(lambda: defaultdict(int))  # particle → l-word
    total_l_bigrams = 0
    onset_counts = defaultdict(int)
    total_words = 0
    particle_total = defaultdict(int)

    for words in lines:
        n = len(words)
        for i, w in enumerate(words):
            onset_counts[get_onset(w)] += 1
            total_words += 1
            if i > 0:
                particle_total[words[i-1]] += 1
            if get_onset(w) == 'l' and i > 0:
                prev = words[i-1]
                prev_onset = get_onset(prev)
                before_l[prev_onset] += 1
                before_l_specific[prev][w] += 1
                total_l_bigrams += 1

    l_baseline = onset_counts['l'] / total_words if total_words > 0 else 0

    print(f"\n{label} — Onset classes before l-onset words (n_l={total_l_bigrams}, baseline={l_baseline*100:.1f}%)")
    print(f"{'Before onset':<12} {'n':>5} {'obs%':>7} {'base%':>7} {'enrich':>8}")
    print("-" * 45)
    for onset_cls, _ in ONSET_CLASSES[:15]:
        obs = before_l[onset_cls]
        obs_rate = obs / total_l_bigrams if total_l_bigrams > 0 else 0
        base_rate = onset_counts[onset_cls] / total_words if total_words > 0 else 0
        enrich = obs_rate / base_rate if base_rate > 0 else 0
        if obs > 0 or base_rate > 0.02:
            print(f"{onset_cls:<12} {obs:>5} {obs_rate*100:>6.1f}% {base_rate*100:>6.1f}% {enrich:>7.2f}×")

    print(f"\nTop SPECIFIC particles before l-onset words:")
    # Sort specific particles by frequency
    particle_l_counts = {p: sum(ws.values()) for p, ws in before_l_specific.items()}
    for particle, cnt in sorted(particle_l_counts.items(), key=lambda x: -x[1])[:15]:
        pt = particle_total.get(particle, 0)
        rate = cnt / pt if pt > 0 else 0
        base = l_baseline
        enrich = rate / base if base > 0 else 0
        top_lwords = sorted(before_l_specific[particle].items(), key=lambda x: -x[1])[:3]
        top_str = ", ".join(f"{w}({n})" for w,n in top_lwords)
        print(f"  {particle:<12} n={cnt:>4}, rate={rate*100:.1f}% ({enrich:.2f}×), top l-words: {top_str}")

def main():
    print("Loading corpus...")
    folio_words, lines_by_dialect, dialect_map = parse_corpus()

    a_lines = lines_by_dialect['A']
    b_lines = lines_by_dialect['B']

    print(f"A-dialect lines: {len(a_lines)}")
    print(f"B-dialect lines: {len(b_lines)}")

    # H289: Positional profile of sh/ch_e in B vs cth in A
    print("\n" + "="*70)
    print("H289: POSITIONAL PROFILE COMPARISON")
    print("="*70)

    analyze_positional(a_lines, ['cth'], "A-DIALECT: cth POSITIONAL DISTRIBUTION")
    analyze_positional(b_lines, ['sh', 'ch_e', 'ch'], "B-DIALECT: sh / ch_e / ch POSITIONAL DISTRIBUTION")

    # Before-context enrichment
    print("\n" + "="*70)
    print("H289: BEFORE-CONTEXT ENRICHMENT")
    print("="*70)

    analyze_before_context(a_lines, 'cth', "A-DIALECT before cth-onset words")
    analyze_before_context(b_lines, 'sh', "B-DIALECT before sh-onset words")
    analyze_before_context(b_lines, 'ch_e', "B-DIALECT before ch_e-onset words")

    # Self-succession
    print("\n" + "="*70)
    print("H289: SELF-SUCCESSION")
    print("="*70)

    analyze_self_succession(a_lines, 'cth', "A-cth")
    analyze_self_succession(b_lines, 'sh', "B-sh")
    analyze_self_succession(b_lines, 'ch_e', "B-ch_e")
    analyze_self_succession(b_lines, 'ch', "B-ch (control)")

    # H290: B-particle → l-onset determiner analysis
    print("\n" + "="*70)
    print("H290: B-DIALECT PARTICLE → l-ONSET ANALYSIS")
    print("="*70)

    analyze_l_onset_determiners(b_lines, "B-DIALECT")

    # Also: daiin→l in A for comparison
    print("\n--- A-DIALECT daiin→onset (for l-onset comparison) ---")
    analyze_before_context(a_lines, 'l', "A-DIALECT before l-onset words")

if __name__ == '__main__':
    main()
