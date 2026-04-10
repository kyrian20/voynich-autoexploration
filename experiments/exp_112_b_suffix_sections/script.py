#!/usr/bin/env python3
"""
exp_112: Secondary B-Suffix Section Partition (H220)
Tests: Is -eey a stars-specific B-paradigm marker and -eedy a cosmo-specific marker?
Is there a systematic three-way B-suffix grammar: herbal-B=-edy; cosmo-B=-eedy; stars-B=-eey?
"""

import re
import math
from collections import defaultdict, Counter

DATA = 'data/transcriptions/eva_zl3b.txt'

def parse_eva(path):
    section_map = {}
    for f in range(1, 58): section_map[f] = 'herbal'
    for f in range(67, 74): section_map[f] = 'astro'
    for f in range(75, 85): section_map[f] = 'cosmo'
    for f in range(87, 103): section_map[f] = 'pharma'
    for f in range(103, 117): section_map[f] = 'stars'

    edy_counts = defaultdict(int)
    total_counts = defaultdict(int)
    records = []

    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or not line.startswith('<'):
                continue
            m = re.match(r'<([^>]+)>(.*)', line)
            if not m: continue
            locus_code = m.group(1)
            text = m.group(2).strip()

            comma_idx = locus_code.find(',')
            if comma_idx < 0: continue
            folio_line = locus_code[:comma_idx]
            locus_type = locus_code[comma_idx+1:]

            fm = re.match(r'f(\d+)', folio_line)
            if not fm: continue
            folio_num = int(fm.group(1))

            lm = re.match(r'f\w+\.(\d+)', folio_line)
            line_in_folio = int(lm.group(1)) if lm else 0

            prefix = ''.join(c for c in locus_type if c in '@+*=~&')
            lt = locus_type[len(prefix):]
            is_body = bool(re.match(r'P', lt))
            is_label = bool(re.match(r'L', lt))

            if not (is_body or is_label): continue

            text_clean = re.sub(r'<[^>]*>', '', text)
            text_clean = re.sub(r'\[[^\]]*\]', lambda m: m.group(0)[1:-1].split(':')[0], text_clean)
            text_clean = re.sub(r'\{[^}]*\}', '', text_clean)
            text_clean = re.sub(r'@\d+;?', '', text_clean)
            text_clean = re.sub(r'<%>|<!.*?>|<\$>', '', text_clean)

            words = [w for w in re.split(r'[-.\s,]', text_clean)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words: continue

            section = section_map.get(folio_num, 'other')
            is_para_start = locus_type.startswith('@') or locus_type.startswith('*')

            for w in words:
                if 'edy' in w or 'eedy' in w:
                    edy_counts[folio_num] += 1
                total_counts[folio_num] += 1

            n = len(words)
            for i, w in enumerate(words):
                records.append({
                    'word': w, 'folio': folio_num, 'section': section,
                    'is_body': is_body, 'is_label': is_label,
                    'is_para_start': is_para_start and (i == 0),
                    'line_first': (i == 0), 'line_last': (i == n-1),
                    'pos_in_line': i,
                })

    dialect_map = {fnum: ('B' if edy_counts[fnum]/max(1,total_counts[fnum]) >= 0.05 else 'A')
                   for fnum in total_counts}
    for r in records:
        r['dialect'] = dialect_map.get(r['folio'], 'A')

    return records, dialect_map


def get_onset_class(word):
    w = word
    if w.startswith('qok'): return 'qok'
    if w.startswith('qot'): return 'qot'
    if w.startswith('qo'): return 'qo'
    if w.startswith('ch'): return 'ch'
    if w.startswith('sh'): return 'sh'
    if w.startswith('ok'): return 'ok'
    if w.startswith('ot'): return 'ot'
    if w.startswith('ol'): return 'ol'
    if w.startswith('olk'): return 'olk'
    if w.startswith('d'): return 'd'
    if w.startswith('s'): return 's'
    return 'other'


def h220_b_suffix_section_partition(records):
    """H220: Is there a systematic three-way B-suffix section partition?"""
    print("=" * 70)
    print("H220: Secondary B-Suffix Section Partition")
    print("=" * 70)

    body = [r for r in records if r['is_body']]
    b_body = [r for r in body if r['dialect'] == 'B']

    b_sections = ['herbal', 'cosmo', 'stars']
    onset_classes = ['ch', 'sh', 'qok', 'qot', 'ok', 'ot', 'qo', 'ol', 'olk', 's']
    b_suffixes = ['edy', 'eedy', 'eey']
    a_suffixes = ['ol', 'or', 'y', 'aiin']

    # Extract suffix
    def get_suffix(word):
        for suf in ['eedy', 'edy', 'eey', 'aiin', 'ol', 'or', 'ar', 'al', 'ey', 'ain', 'dy', 'y']:
            if word.endswith(suf) and len(word) > len(suf):
                return suf
        return 'other'

    # Build (onset, section, suffix) matrix for B-dialect
    matrix = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    section_totals = defaultdict(int)

    for r in b_body:
        cls = get_onset_class(r['word'])
        suf = get_suffix(r['word'])
        section = r['section']
        matrix[cls][section][suf] += 1
        section_totals[section] += 1

    # Print B-suffix breakdown by section for each onset class
    print(f"\n--- B-suffix distribution by onset class and section (B-dialect only) ---")
    print("(Three-way test: herbal-B→-edy, cosmo-B→-eedy, stars-B→-eey?)")

    for cls in onset_classes:
        sect_data = {}
        for s in b_sections:
            suf_counts = matrix[cls][s]
            b_total = sum(suf_counts.get(sf, 0) for sf in b_suffixes)
            if b_total < 10:
                sect_data[s] = None
                continue
            edy = 100 * suf_counts.get('edy', 0) / b_total
            eedy = 100 * suf_counts.get('eedy', 0) / b_total
            eey = 100 * suf_counts.get('eey', 0) / b_total
            dominant = max(b_suffixes, key=lambda sf: suf_counts.get(sf, 0))
            sect_data[s] = (b_total, edy, eedy, eey, dominant)

        # Only print if at least 2 sections have enough data
        valid = [(s, d) for s, d in sect_data.items() if d is not None]
        if len(valid) < 2:
            continue

        print(f"\n  Onset class: {cls}")
        for s, data in valid:
            b_total, edy, eedy, eey, dominant = data
            print(f"    {s:<12}: n={b_total:4}, edy={edy:5.1f}%, eedy={eedy:5.1f}%, eey={eey:5.1f}% → dominant={dominant}")

    # Systematic test: for each onset class, does the 3-way partition hold?
    print("\n--- Systematic test of 3-way partition ---")
    print("Prediction: herbal→edy_dom, cosmo→eedy_dom, stars→eey_dom")
    print(f"{'Onset':<8} {'herbal_dom':<14} {'cosmo_dom':<14} {'stars_dom':<14} {'Matches?'}")

    for cls in onset_classes:
        results = {}
        for s in b_sections:
            suf_counts = matrix[cls][s]
            b_total = sum(suf_counts.get(sf, 0) for sf in b_suffixes)
            if b_total < 10:
                results[s] = '?'
                continue
            dominant = max(b_suffixes, key=lambda sf: suf_counts.get(sf, 0))
            results[s] = dominant

        if all(results.get(s, '?') == '?' for s in b_sections):
            continue

        herbal_dom = results.get('herbal', '?')
        cosmo_dom = results.get('cosmo', '?')
        stars_dom = results.get('stars', '?')

        matches = (herbal_dom == 'edy' or herbal_dom == '?') and \
                  (cosmo_dom == 'eedy' or cosmo_dom == '?') and \
                  (stars_dom == 'eey' or stars_dom == '?')

        print(f"{cls:<8} {herbal_dom:<14} {cosmo_dom:<14} {stars_dom:<14} {'YES' if matches else 'NO'}")

    # Word-level analysis: do sections share stems with different B-suffixes?
    print("\n--- Stem sharing across B-sections with different suffixes ---")
    print("(Do qok+edy=herbal, qok+eedy=cosmo, qok+eey=stars with SAME or DIFFERENT stems?)")

    # For qok onset: collect stem → {section: suffix_set}
    qok_stem_analysis = defaultdict(lambda: defaultdict(Counter))

    for r in b_body:
        w = r['word']
        if not w.startswith('qok'): continue
        suf = get_suffix(w)
        if suf not in b_suffixes: continue
        stem = w[3:-len(suf)] if len(w) > 3 + len(suf) else w[3:]
        qok_stem_analysis[stem][r['section']][suf] += 1

    # Find stems appearing in multiple sections
    print(f"\n  qok-stems appearing in multiple B-sections:")
    print(f"  {'Stem':<12} {'herbal_suf':<20} {'cosmo_suf':<20} {'stars_suf':<20}")
    for stem, section_suf in sorted(qok_stem_analysis.items()):
        sections_with_data = [s for s in b_sections if sum(section_suf[s].values()) >= 3]
        if len(sections_with_data) < 2: continue

        herbal_str = str(dict(section_suf.get('herbal', {}))) if section_suf.get('herbal') else '-'
        cosmo_str = str(dict(section_suf.get('cosmo', {}))) if section_suf.get('cosmo') else '-'
        stars_str = str(dict(section_suf.get('stars', {}))) if section_suf.get('stars') else '-'

        print(f"  {stem:<12} {herbal_str:<20} {cosmo_str:<20} {stars_str:<20}")

    # Cross-section vocabulary test: unique B-suffix words per section
    print("\n--- B-suffix word uniqueness by section ---")
    b_suf_words = defaultdict(lambda: defaultdict(set))  # section → suf → set of words

    for r in b_body:
        suf = get_suffix(r['word'])
        if suf in b_suffixes:
            b_suf_words[r['section']][suf].add(r['word'])

    for suf in b_suffixes:
        print(f"\n  -{suf} words:")
        for s in b_sections:
            words = b_suf_words[s][suf]
            print(f"    {s}: {len(words)} unique words")

        # Overlap between sections
        herbal_set = b_suf_words['herbal'][suf]
        cosmo_set = b_suf_words['cosmo'][suf]
        stars_set = b_suf_words['stars'][suf]

        if herbal_set and cosmo_set:
            overlap_hc = len(herbal_set & cosmo_set)
            print(f"    herbal∩cosmo: {overlap_hc} ({100*overlap_hc/max(1,len(herbal_set|cosmo_set)):.0f}%)")
        if herbal_set and stars_set:
            overlap_hs = len(herbal_set & stars_set)
            print(f"    herbal∩stars: {overlap_hs} ({100*overlap_hs/max(1,len(herbal_set|stars_set)):.0f}%)")
        if cosmo_set and stars_set:
            overlap_cs = len(cosmo_set & stars_set)
            print(f"    cosmo∩stars: {overlap_cs} ({100*overlap_cs/max(1,len(cosmo_set|stars_set)):.0f}%)")

    # Top words per B-section by B-suffix
    print("\n--- Top section-exclusive B-suffix words ---")
    for s in b_sections:
        print(f"\n  {s} B-dialect top -edy/-eedy/-eey words:")
        for suf in b_suffixes:
            # Words exclusive to this section (or at least dominant)
            words_here = Counter(r['word'] for r in b_body
                                 if r['section'] == s and get_suffix(r['word']) == suf)
            words_other = Counter(r['word'] for r in b_body
                                  if r['section'] != s and get_suffix(r['word']) == suf)

            exclusive = {w: c for w, c in words_here.items()
                         if words_other.get(w, 0) == 0 and c >= 3}
            print(f"    -{suf} exclusive to {s} (n≥3): {len(exclusive)} words")
            for w, c in sorted(exclusive.items(), key=lambda x: -x[1])[:8]:
                print(f"      {w}: {c}")

    # Per-folio B-suffix rates
    print("\n--- Per-folio B-suffix distribution (qok-onset, B-dialect folios) ---")
    folio_suf = defaultdict(Counter)
    folio_section = {}
    for r in b_body:
        if not r['word'].startswith('qok'): continue
        suf = get_suffix(r['word'])
        if suf in b_suffixes:
            folio_suf[r['folio']][suf] += 1
            folio_section[r['folio']] = r['section']

    print(f"  {'Folio':<8} {'Section':<12} {'n':<6} {'edy%':<8} {'eedy%':<8} {'eey%':<8}")
    for folio in sorted(folio_suf.keys()):
        counts = folio_suf[folio]
        n = sum(counts.values())
        if n < 5: continue
        s = folio_section[folio]
        edy = 100 * counts.get('edy', 0) / n
        eedy = 100 * counts.get('eedy', 0) / n
        eey = 100 * counts.get('eey', 0) / n
        print(f"  {folio:<8} {s:<12} {n:<6} {edy:<8.0f} {eedy:<8.0f} {eey:<8.0f}")

    # Statistical test: is the section partition significant?
    print("\n--- Statistical summary: B-suffix rates by section ---")
    print("(Rate = tokens of given suffix / total B-suffix tokens for onset class)")

    all_classes_summary = []
    for cls in ['ch', 'sh', 'qok', 'ok', 'ot', 'ol']:
        row = {'class': cls}
        for s in b_sections:
            suf_counts = matrix[cls][s]
            total = sum(suf_counts.get(sf, 0) for sf in b_suffixes)
            if total < 5:
                row[s] = None
                continue
            row[s] = {sf: suf_counts.get(sf, 0)/total for sf in b_suffixes}
        all_classes_summary.append(row)

    # Does the partition direction hold across ALL onset classes?
    print(f"\n  For EACH onset class, does stars have highest -eey rate? cosmo highest -eedy?")
    for row in all_classes_summary:
        cls = row['class']
        valid = {s: row[s] for s in b_sections if row[s] is not None}
        if len(valid) < 2: continue

        eey_order = sorted(valid.keys(), key=lambda s: valid[s].get('eey', 0), reverse=True)
        eedy_order = sorted(valid.keys(), key=lambda s: valid[s].get('eedy', 0), reverse=True)

        eey_str = ' > '.join(f"{s}({100*valid[s]['eey']:.0f}%)" for s in eey_order)
        eedy_str = ' > '.join(f"{s}({100*valid[s]['eedy']:.0f}%)" for s in eedy_order)
        print(f"  {cls}: -eey: {eey_str}")
        print(f"        -eedy: {eedy_str}")


def main():
    print("Loading data...")
    records, dialect_map = parse_eva(DATA)

    body_recs = [r for r in records if r['is_body']]
    b_body = [r for r in body_recs if r['dialect'] == 'B']

    print(f"Total body tokens: {len(body_recs)}")
    print(f"B-dialect body tokens: {len(b_body)}")

    h220_b_suffix_section_partition(records)


if __name__ == '__main__':
    main()
