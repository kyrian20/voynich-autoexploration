#!/usr/bin/env python3
"""
Experiment exp_038: -edy/-ain Paradigm in Currier B (H034)
Top B words: chedy, shedy, qokeedy, qokain, qokedy, etc.
Test whether -edy/-ain/-aiin are in complementary distribution
(different syntactic positions) or freely alternating.
Also test: do words of the form X-edy, X-ain, X-aiin share the same stems X?
"""

import re, math
from collections import Counter, defaultdict

ZL3B = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

def parse_tokens_with_position(path):
    tokens = []
    current_folio = None
    current_lang = 'unknown'
    current_section = 'unknown'

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            if re.match(r'^<f\w+>', line) and '$' in line:
                mf = re.match(r'^<(f\w+)>', line)
                current_folio = mf.group(1) if mf else current_folio
                ml = re.search(r'\$L=([AB])', line)
                current_lang = ml.group(1) if ml else 'unknown'
                ms = re.search(r'\$I=([A-Z])', line)
                current_section = ms.group(1) if ms else 'unknown'
                continue
            m = re.match(r'^<[^>]+,([^>]+)>\s+(.*)', line)
            if not m: continue
            locus = m.group(1).strip()
            if not re.match(r'^[+*@=/~&]?P[0-9]$', locus): continue
            content = m.group(2)
            content = re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*', '', content)

            raw_tokens = []
            for seg in re.split(r',', content):
                for t in re.split(r'\.', seg):
                    t = t.strip()
                    if t and re.match(r'^[a-z\']+$', t):
                        raw_tokens.append(t.lower())

            n = len(raw_tokens)
            for i, t in enumerate(raw_tokens):
                pos = 'solo' if n == 1 else ('initial' if i == 0 else ('final' if i == n-1 else 'medial'))
                tokens.append({'word': t, 'pos': pos, 'currier': current_lang,
                               'section': current_section, 'folio': current_folio})
    return tokens

def suffix_group(word):
    """Identify suffix paradigm."""
    if word.endswith('aiin'): return 'aiin', word[:-4]
    if word.endswith('ain'): return 'ain', word[:-3]
    if word.endswith('eedy'): return 'eedy', word[:-4]
    if word.endswith('edy'): return 'edy', word[:-3]
    if word.endswith('dy'): return 'dy', word[:-2]
    if word.endswith('chy'): return 'chy', word[:-3]
    if word.endswith('eey'): return 'eey', word[:-3]
    if word.endswith('ey'): return 'ey', word[:-2]
    if word.endswith('y'): return 'y', word[:-1]
    return None, None

def main():
    tokens = parse_tokens_with_position(ZL3B)
    print(f"Total tokens: {len(tokens)}")

    # Focus on Currier B
    b_tokens = [t for t in tokens if t['currier'] == 'B']
    print(f"Currier B tokens: {len(b_tokens)}")

    # Find major suffix paradigms: stems that appear with multiple suffixes
    stem_suffixes = defaultdict(lambda: defaultdict(int))
    for t in b_tokens:
        suf, stem = suffix_group(t['word'])
        if suf and stem and len(stem) >= 2:
            stem_suffixes[stem][suf] += 1

    # Find stems with multiple suffix forms
    multi_suffix = {stem: suf_dict for stem, suf_dict in stem_suffixes.items()
                    if len(suf_dict) >= 2}
    print(f"\nStems with 2+ suffix variants in Currier B: {len(multi_suffix)}")

    # Sort by total frequency
    multi_by_freq = sorted(multi_suffix.items(),
                           key=lambda x: -sum(x[1].values()))
    print("\n=== TOP 20 MULTI-SUFFIX STEM PARADIGMS ===")
    print(f"{'Stem':>12} | {'Total':>6} | {'Suffixes (count)'}")
    print("-" * 60)
    for stem, suf_dict in multi_by_freq[:20]:
        total = sum(suf_dict.values())
        suf_str = ', '.join(f"-{s}({c})" for s, c in sorted(suf_dict.items(), key=lambda x: -x[1]))
        print(f"  {stem:>10} | {total:>6} | {suf_str}")

    # Focus on the -edy/-ain/-aiin paradigm specifically
    print(f"\n=== -edy/-ain/-aiin PARADIGM ANALYSIS ===")
    edy_ain_stems = {stem: suf_dict for stem, suf_dict in multi_suffix.items()
                     if any(s in suf_dict for s in ('edy', 'ain', 'aiin', 'eedy'))}
    print(f"Stems with edy/ain/aiin variants: {len(edy_ain_stems)}")

    # Top stems in this paradigm
    top_ea = sorted(edy_ain_stems.items(), key=lambda x: -sum(x[1].values()))[:20]
    for stem, suf_dict in top_ea:
        total = sum(suf_dict.values())
        relevant = {k: v for k, v in suf_dict.items() if k in ('edy', 'eedy', 'ain', 'aiin', 'dy', 'ey', 'eey')}
        if not relevant: continue
        suf_str = ', '.join(f"-{s}:{c}" for s, c in sorted(relevant.items()))
        print(f"  {stem}: {suf_str} (total={total})")

    # Positional distribution for the core -edy vs -ain/-aiin pairs
    print(f"\n=== POSITIONAL DISTRIBUTION: -edy vs -ain vs -aiin ===")
    edy_tokens = [t for t in b_tokens if t['word'].endswith('edy') and not t['word'].endswith('eedy')]
    eedy_tokens = [t for t in b_tokens if t['word'].endswith('eedy')]
    ain_tokens = [t for t in b_tokens if t['word'].endswith('ain') and not t['word'].endswith('aiin')]
    aiin_tokens = [t for t in b_tokens if t['word'].endswith('aiin')]

    groups = [('-edy', edy_tokens), ('-eedy', eedy_tokens), ('-ain', ain_tokens), ('-aiin', aiin_tokens)]
    print(f"\n{'Suffix':>8} | {'n':>5} | {'init%':>6} | {'med%':>6} | {'fin%':>6} | {'solo%':>6}")
    print("-" * 55)
    for name, grp in groups:
        if not grp: continue
        pos_c = Counter(t['pos'] for t in grp)
        n = len(grp)
        pi = 100*pos_c.get('initial',0)/n
        pm = 100*pos_c.get('medial',0)/n
        pf = 100*pos_c.get('final',0)/n
        ps = 100*pos_c.get('solo',0)/n
        print(f"  {name:>6} | {n:>5} | {pi:>5.1f}% | {pm:>5.1f}% | {pf:>5.1f}% | {ps:>5.1f}%")

    # Chi-square: -edy vs -ain final position
    import math
    print(f"\n=== CHI-SQUARE: FINAL vs NON-FINAL ===")
    for (n1, g1), (n2, g2) in [('-edy', edy_tokens), ('-ain', ain_tokens)], [('-edy', edy_tokens), ('-aiin', aiin_tokens)]:
        pass  # reconstructed below

    pairs_to_test = [('-edy', edy_tokens, '-ain', ain_tokens),
                     ('-edy', edy_tokens, '-aiin', aiin_tokens),
                     ('-ain', ain_tokens, '-aiin', aiin_tokens)]
    for n1, g1, n2, g2 in pairs_to_test:
        if not g1 or not g2: continue
        a = sum(1 for t in g1 if t['pos']=='final')
        b = len(g1) - a
        c = sum(1 for t in g2 if t['pos']=='final')
        d = len(g2) - c
        n = a+b+c+d
        e11 = (a+b)*(a+c)/n; e12 = (a+b)*(b+d)/n
        e21 = (c+d)*(a+c)/n; e22 = (c+d)*(b+d)/n
        chi2 = sum((obs-exp)**2/exp for obs, exp in [(a,e11),(b,e12),(c,e21),(d,e22)] if exp>0)
        or_val = (a*d)/(b*c) if b*c > 0 else float('inf')
        fin1 = 100*a/len(g1) if g1 else 0
        fin2 = 100*c/len(g2) if g2 else 0
        print(f"  {n1}(fin={fin1:.0f}%) vs {n2}(fin={fin2:.0f}%): OR={or_val:.2f}, chi2={chi2:.1f}")

    # Section/currier distribution
    print(f"\n=== SUFFIX PARADIGM BY SECTION (Currier B) ===")
    sections_b = {'H', 'P', 'B', 'A', 'Z', 'T', 'S', 'C'}
    section_totals = Counter(t['section'] for t in b_tokens)
    for name, grp in groups:
        if not grp: continue
        sec_c = Counter(t['section'] for t in grp)
        n = len(grp)
        print(f"  {name}: n={n}", end='')
        for sec in ['H', 'P', 'B', 'A', 'S']:
            rate = 100*sec_c.get(sec,0)/n if n > 0 else 0
            print(f" | {sec}={rate:.0f}%", end='')
        print()

    # Top words per suffix
    print(f"\n=== TOP 10 WORDS PER SUFFIX ===")
    for name, grp in groups:
        if not grp: continue
        top = Counter(t['word'] for t in grp).most_common(10)
        print(f"  {name}: {', '.join(f'{w}({c})' for w,c in top)}")

if __name__ == '__main__':
    main()
