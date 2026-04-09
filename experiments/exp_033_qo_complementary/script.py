#!/usr/bin/env python3
"""
Experiment exp_033: qo-Word Complementary Distribution Test (H032)
52.6% of qo-stems appear as free words (e.g., qokeedy AND keedy exist).
Test whether qo-form and bare-form appear in complementary distribution
by: (a) position-in-line (initial/medial/final), (b) Currier A/B, (c) section.
"""

import re
from collections import Counter, defaultdict

ZL3B = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

def parse_tokens_with_position(path):
    """Extract tokens with line position, section, Currier dialect."""
    tokens = []
    current_folio = None
    current_lang = 'unknown'
    current_section = 'unknown'

    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            # Folio header
            if re.match(r'^<f\w+>', line) and '$' in line:
                m_folio = re.match(r'^<(f\w+)>', line)
                if m_folio:
                    current_folio = m_folio.group(1)
                m_lang = re.search(r'\$L=([AB])', line)
                current_lang = m_lang.group(1) if m_lang else 'unknown'
                m_sec = re.search(r'\$I=([A-Z])', line)
                current_section = m_sec.group(1) if m_sec else 'unknown'
                continue

            # Body text loci only
            m = re.match(r'^<[^>]+,([^>]+)>\s+(.*)', line)
            if not m:
                continue
            locus = m.group(1).strip()
            if not re.match(r'^[+*@=/~&]?P[0-9]$', locus):
                continue

            content = m.group(2)
            # Clean markup
            content = re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*', '', content)

            # Extract word sequence for this line
            raw_tokens = []
            for segment in re.split(r',', content):
                for token in re.split(r'\.', segment):
                    token = token.strip()
                    if token and re.match(r'^[a-zA-Z\']+$', token):
                        raw_tokens.append(token.lower())

            n = len(raw_tokens)
            for i, token in enumerate(raw_tokens):
                if n == 1:
                    pos = 'solo'
                elif i == 0:
                    pos = 'initial'
                elif i == n - 1:
                    pos = 'final'
                else:
                    pos = 'medial'

                tokens.append({
                    'word': token,
                    'line_pos': pos,
                    'currier': current_lang,
                    'section': current_section,
                    'folio': current_folio,
                })
    return tokens

def section_name(code):
    mapping = {'H': 'herbal', 'P': 'pharma', 'A': 'astro', 'B': 'bio',
               'Z': 'zodiac', 'C': 'cosmo', 'T': 'text', 'unknown': 'unknown'}
    return mapping.get(code, code)

def compare_distributions(qo_entries, stem_entries, label):
    """Compare two entry lists across dimensions."""
    if not qo_entries or not stem_entries:
        print(f"  {label}: insufficient data")
        return

    # Position in line
    qo_pos = Counter(e['line_pos'] for e in qo_entries)
    stem_pos = Counter(e['line_pos'] for e in stem_entries)
    print(f"\n  {label} — Position in line:")
    positions = ['initial', 'medial', 'final', 'solo']
    qo_total = sum(qo_pos.values())
    stem_total = sum(stem_pos.values())
    for pos in positions:
        qo_pct = 100 * qo_pos.get(pos, 0) / qo_total if qo_total > 0 else 0
        stem_pct = 100 * stem_pos.get(pos, 0) / stem_total if stem_total > 0 else 0
        diff = qo_pct - stem_pct
        print(f"    {pos:>8}: qo={qo_pct:5.1f}%  bare={stem_pct:5.1f}%  diff={diff:+5.1f}%")

    # Currier A/B
    qo_cur = Counter(e['currier'] for e in qo_entries)
    stem_cur = Counter(e['currier'] for e in stem_entries)
    print(f"  {label} — Currier dialect:")
    for cur in ['A', 'B', 'unknown']:
        qo_pct = 100 * qo_cur.get(cur, 0) / qo_total if qo_total > 0 else 0
        stem_pct = 100 * stem_cur.get(cur, 0) / stem_total if stem_total > 0 else 0
        diff = qo_pct - stem_pct
        print(f"    {cur}: qo={qo_pct:5.1f}%  bare={stem_pct:5.1f}%  diff={diff:+5.1f}%")

def main():
    print("Parsing tokens with position data...")
    tokens = parse_tokens_with_position(ZL3B)
    print(f"Total body-text tokens: {len(tokens)}")

    # Build index: word → entries
    word_index = defaultdict(list)
    for t in tokens:
        word_index[t['word']].append(t)

    # Find qo-stems that exist as free words
    qo_words = set(t['word'] for t in tokens if t['word'].startswith('qo'))
    qo_stem_pairs = {}
    for qw in qo_words:
        stem = qw[2:]
        if len(stem) >= 2 and stem in word_index:
            qo_stem_pairs[qw] = stem

    # Sort by qo-word frequency (descending)
    qo_freq = Counter(t['word'] for t in tokens if t['word'].startswith('qo'))
    top_pairs = sorted(qo_stem_pairs.items(), key=lambda x: -qo_freq[x[0]])[:20]

    print(f"\nTop 20 qo/bare-stem pairs (by qo-word frequency):")
    print(f"{'qo-word':>15} | {'qo freq':>7} | {'bare stem':>12} | {'stem freq':>9}")
    print("-" * 55)
    for qw, stem in top_pairs:
        print(f"  {qw:>13} | {qo_freq[qw]:>7} | {stem:>12} | {len(word_index[stem]):>9}")

    # Aggregate analysis across all pairs
    print(f"\n=== AGGREGATE POSITION DISTRIBUTION (all {len(top_pairs)} pairs) ===")
    all_qo = []
    all_stems = []
    for qw, stem in top_pairs:
        all_qo.extend(word_index[qw])
        all_stems.extend(word_index[stem])

    qo_pos = Counter(e['line_pos'] for e in all_qo)
    stem_pos = Counter(e['line_pos'] for e in all_stems)
    qo_total = sum(qo_pos.values())
    stem_total = sum(stem_pos.values())

    print(f"{'Position':>10} | {'qo-form %':>10} | {'bare-form %':>12} | {'Diff':>8}")
    print("-" * 48)
    for pos in ['initial', 'medial', 'final', 'solo']:
        qp = 100 * qo_pos.get(pos, 0) / qo_total if qo_total > 0 else 0
        sp = 100 * stem_pos.get(pos, 0) / stem_total if stem_total > 0 else 0
        print(f"  {pos:>8} | {qp:>10.1f} | {sp:>12.1f} | {qp-sp:>+8.1f}")

    # Currier A/B
    qo_cur = Counter(e['currier'] for e in all_qo)
    stem_cur = Counter(e['currier'] for e in all_stems)
    print(f"\n=== CURRIER DIALECT DISTRIBUTION ===")
    print(f"{'Dialect':>8} | {'qo-form':>10} | {'bare-form':>12} | {'Diff':>8}")
    print("-" * 48)
    for cur in ['A', 'B']:
        qp = 100 * qo_cur.get(cur, 0) / qo_total if qo_total > 0 else 0
        sp = 100 * stem_cur.get(cur, 0) / stem_total if stem_total > 0 else 0
        print(f"  {cur:>6} | {qp:>10.1f} | {sp:>12.1f} | {qp-sp:>+8.1f}")

    # Section
    qo_sec = Counter(e['section'] for e in all_qo)
    stem_sec = Counter(e['section'] for e in all_stems)
    print(f"\n=== SECTION DISTRIBUTION ===")
    print(f"{'Section':>8} | {'qo-form':>10} | {'bare-form':>12} | {'Diff':>8}")
    print("-" * 48)
    all_sections = sorted(set(list(qo_sec.keys()) + list(stem_sec.keys())))
    for sec in all_sections:
        qp = 100 * qo_sec.get(sec, 0) / qo_total if qo_total > 0 else 0
        sp = 100 * stem_sec.get(sec, 0) / stem_total if stem_total > 0 else 0
        print(f"  {section_name(sec):>8} | {qp:>10.1f} | {sp:>12.1f} | {qp-sp:>+8.1f}")

    # Individual pair analysis for the top 10
    print(f"\n=== TOP 10 PAIR INDIVIDUAL ANALYSIS ===")
    for qw, stem in top_pairs[:10]:
        qe = word_index[qw]
        se = word_index[stem]
        qp = Counter(e['line_pos'] for e in qe)
        sp = Counter(e['line_pos'] for e in se)
        qt = sum(qp.values())
        st = sum(sp.values())
        qf = 100 * qp.get('final', 0) / qt if qt > 0 else 0
        sf = 100 * sp.get('final', 0) / st if st > 0 else 0
        qi = 100 * qp.get('initial', 0) / qt if qt > 0 else 0
        si = 100 * sp.get('initial', 0) / st if st > 0 else 0
        qa = Counter(e['currier'] for e in qe)
        sa = Counter(e['currier'] for e in se)
        qb_frac = 100 * qa.get('B', 0) / qt if qt > 0 else 0
        sb_frac = 100 * sa.get('B', 0) / st if st > 0 else 0
        print(f"  {qw}({qt}) vs {stem}({st}): final={qf:.0f}%/{sf:.0f}%, init={qi:.0f}%/{si:.0f}%, B%={qb_frac:.0f}%/{sb_frac:.0f}%")

    # Chi-square test for line position (initial vs final)
    print(f"\n=== STATISTICAL TEST: FINAL vs NON-FINAL POSITION ===")
    import math
    for qw, stem in top_pairs[:10]:
        qe = word_index[qw]
        se = word_index[stem]
        n_qf = sum(1 for e in qe if e['line_pos'] == 'final')
        n_q = len(qe)
        n_sf = sum(1 for e in se if e['line_pos'] == 'final')
        n_s = len(se)
        if n_q < 5 or n_s < 5: continue
        # 2x2 contingency table
        a = n_qf; b = n_q - n_qf
        c = n_sf; d = n_s - n_sf
        n = a + b + c + d
        if a*d == 0 or b*c == 0: continue
        # Fisher's OR
        or_val = (a*d) / (b*c)
        # Chi-square (with continuity)
        e11 = (a+b)*(a+c)/n; e12 = (a+b)*(b+d)/n
        e21 = (c+d)*(a+c)/n; e22 = (c+d)*(b+d)/n
        chi2 = (a-e11)**2/e11 + (b-e12)**2/e12 + (c-e21)**2/e21 + (d-e22)**2/e22
        # p-value approximation (chi2 with 1 df)
        p_approx = math.exp(-chi2/2) if chi2 < 20 else 0.0001  # rough
        print(f"  {qw} vs {stem}: final_rate={100*n_qf/n_q:.0f}%/{100*n_sf/n_s:.0f}%, OR={or_val:.2f}, chi2={chi2:.2f}")

if __name__ == '__main__':
    main()
