#!/usr/bin/env python3
"""
exp_111: olk-Cluster as B-Structural Counterpart to cth- (H218)
          + Suffix Co-Occurrence Matrix Within Content Stems (H216)
          + Standalone dy/y as Free Morphemes (H219)
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
    raw_lines = []

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
            is_para_start = locus_type.startswith('@') or locus_type.startswith('*')

            pm = re.match(r'P(\w+)', lt)
            para_id = pm.group(1) if pm else 'unknown'
            try: para_num = int(para_id)
            except: para_num = -1

            if not (is_body or is_label): continue

            # Clean text
            text_clean = re.sub(r'<[^>]*>', '', text)
            text_clean = re.sub(r'\[[^\]]*\]', lambda m: m.group(0)[1:-1].split(':')[0], text_clean)
            text_clean = re.sub(r'\{[^}]*\}', '', text_clean)
            text_clean = re.sub(r'@\d+;?', '', text_clean)
            text_clean = re.sub(r'<%>', '', text_clean)
            text_clean = re.sub(r'<!.*?>', '', text_clean)
            text_clean = re.sub(r'<\$>', '', text_clean)

            words = [w for w in re.split(r'[-.\s,]', text_clean)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words: continue

            section = section_map.get(folio_num, 'other')
            for w in words:
                if 'edy' in w or 'eedy' in w:
                    edy_counts[folio_num] += 1
                total_counts[folio_num] += 1

            raw_lines.append({
                'folio': folio_num, 'folio_line': folio_line,
                'line_in_folio': line_in_folio, 'locus_type': locus_type,
                'section': section, 'is_body': is_body, 'is_label': is_label,
                'is_para_start': is_para_start, 'para_num': para_num,
                'words': words, 'n_words': len(words),
            })

    dialect_map = {fnum: ('B' if edy_counts[fnum]/max(1,total_counts[fnum]) >= 0.05 else 'A')
                   for fnum in total_counts}

    records = []
    for lr in raw_lines:
        words = lr['words']
        n = len(words)
        d = dialect_map.get(lr['folio'], 'A')
        for i, w in enumerate(words):
            records.append({
                'word': w, 'folio': lr['folio'], 'section': lr['section'],
                'dialect': d, 'is_body': lr['is_body'], 'is_label': lr['is_label'],
                'is_para_start': lr['is_para_start'] and (i == 0),
                'line_first': (i == 0), 'line_last': (i == n-1),
                'pos_in_line': i,
            })

    return records, raw_lines, dialect_map


def extract_suffix(word):
    """Extract suffix from word (longest matching suffix from known list)."""
    for suf in ['eedy','edy','eey','aiin','ain','ol','or','ar','al','ey','dy','y','r','n']:
        if word.endswith(suf) and len(word) > len(suf):
            return suf, word[:-len(suf)]
    return 'other', word


def h218_olk_cluster(records):
    """H218: Is olk- the B-structural counterpart to cth-?"""
    print("=" * 70)
    print("H218: olk-Cluster Analysis (B-Structural Counterpart to cth-?)")
    print("=" * 70)

    body = [r for r in records if r['is_body']]
    a_total = sum(1 for r in body if r['dialect'] == 'A')
    b_total = sum(1 for r in body if r['dialect'] == 'B')
    print(f"\nTotal body tokens: {len(body)} (A={a_total}, B={b_total})")

    # cth- reference stats from F116
    cth_words = [r for r in body if r['word'].startswith('cth')]
    olk_words = [r for r in body if r['word'].startswith('olk')]

    print(f"\ncth- tokens: {len(cth_words)} (A={sum(1 for r in cth_words if r['dialect']=='A')}, B={sum(1 for r in cth_words if r['dialect']=='B')})")
    print(f"olk- tokens: {len(olk_words)} (A={sum(1 for r in olk_words if r['dialect']=='A')}, B={sum(1 for r in olk_words if r['dialect']=='B')})")

    # Comparison table
    print("\n--- cth- vs olk-: Dialect Polarity Comparison ---")
    for prefix, words in [('cth-', cth_words), ('olk-', olk_words)]:
        n = len(words)
        if n == 0: continue
        a = sum(1 for r in words if r['dialect'] == 'A')
        b = sum(1 for r in words if r['dialect'] == 'B')
        a_rate = a / a_total * 1000
        b_rate = b / b_total * 1000
        lf = sum(1 for r in words if r['line_first']) / n * 100
        ll = sum(1 for r in words if r['line_last']) / n * 100
        ps = sum(1 for r in words if r['is_para_start']) / n * 100
        ab_ratio = a_rate / max(0.001, b_rate)
        ba_ratio = b_rate / max(0.001, a_rate)
        print(f"\n  {prefix}: n={n}, A={a} ({a_rate:.2f}‰), B={b} ({b_rate:.2f}‰)")
        print(f"    A/B ratio={ab_ratio:.2f}×, B/A ratio={ba_ratio:.2f}×")
        print(f"    LFirst={lf:.1f}%, LLast={ll:.1f}%, PS={ps:.2f}%")

    # olk- sub-classes
    print("\n--- olk- Sub-Class Analysis ---")
    subclasses = {
        'olk (bare)': [r for r in body if r['word'].startswith('olk') and not r['word'].startswith('olka') and not r['word'].startswith('olke')],
        'olka-': [r for r in body if r['word'].startswith('olka')],
        'olke-': [r for r in body if r['word'].startswith('olke')],
        'olkee': [r for r in body if r['word'].startswith('olkee')],
    }

    print(f"{'Subclass':<14} {'n':<8} {'A':<8} {'B':<8} {'A_rate‰':<12} {'B_rate‰':<12} {'B/A':<8} {'LFirst%':<10} {'LLast%':<10} {'PS%'}")
    for name, words in subclasses.items():
        n = len(words)
        if n < 5: continue
        a = sum(1 for r in words if r['dialect'] == 'A')
        b = sum(1 for r in words if r['dialect'] == 'B')
        a_rate = a / a_total * 1000
        b_rate = b / b_total * 1000
        ba = b_rate / max(0.001, a_rate)
        lf = sum(1 for r in words if r['line_first']) / n * 100
        ll = sum(1 for r in words if r['line_last']) / n * 100
        ps = sum(1 for r in words if r['is_para_start']) / n * 100
        print(f"{name:<14} {n:<8} {a:<8} {b:<8} {a_rate:<12.3f} {b_rate:<12.3f} {ba:<8.2f} {lf:<10.1f} {ll:<10.1f} {ps:.2f}")

    # olk- top words
    print("\n--- Top olk- words ---")
    olk_word_counts = Counter()
    olk_a_counts = Counter()
    olk_b_counts = Counter()
    for r in olk_words:
        olk_word_counts[r['word']] += 1
        if r['dialect'] == 'A': olk_a_counts[r['word']] += 1
        else: olk_b_counts[r['word']] += 1

    print(f"{'Word':<20} {'Total':<8} {'A':<8} {'B':<8} {'A_rate‰':<12} {'B_rate‰':<12} {'A/B':<8}")
    for word, total in olk_word_counts.most_common(20):
        a = olk_a_counts[word]
        b = olk_b_counts[word]
        a_rate = a / a_total * 1000
        b_rate = b / b_total * 1000
        ratio = a_rate / max(0.001, b_rate)
        print(f"{word:<20} {total:<8} {a:<8} {b:<8} {a_rate:<12.3f} {b_rate:<12.3f} {ratio:.2f}×")

    # olk- section distribution
    print("\n--- olk- section distribution ---")
    sections = ['herbal', 'pharma', 'cosmo', 'stars', 'astro']
    sect_totals = Counter(r['section'] for r in body)
    olk_sect = Counter(r['section'] for r in olk_words)
    cth_sect = Counter(r['section'] for r in cth_words)

    print(f"{'Section':<12} {'Total':<10} {'olk_n':<8} {'olk_rate‰':<12} {'cth_n':<8} {'cth_rate‰':<12}")
    for s in sections:
        total = sect_totals[s]
        ok = olk_sect[s]
        ct = cth_sect[s]
        print(f"{s:<12} {total:<10} {ok:<8} {1000*ok/max(1,total):<12.2f} {ct:<8} {1000*ct/max(1,total):.2f}")

    # olk- suffix distribution vs cth-
    print("\n--- olk- suffix distribution vs cth- vs all ---")
    all_suf_counts = Counter()
    olk_suf_counts = Counter()
    cth_suf_counts = Counter()
    for r in body:
        w = r['word']
        suf, _ = extract_suffix(w)
        all_suf_counts[suf] += 1
        if w.startswith('olk'): olk_suf_counts[suf] += 1
        if w.startswith('cth'): cth_suf_counts[suf] += 1

    total_all = sum(all_suf_counts.values())
    total_olk = sum(olk_suf_counts.values())
    total_cth = sum(cth_suf_counts.values())

    all_sufs = set(list(olk_suf_counts.keys()) + list(cth_suf_counts.keys()))
    print(f"{'Suffix':<10} {'all%':<10} {'olk%':<10} {'olk_enrich':<14} {'cth%':<10} {'cth_enrich':<14}")
    for suf in sorted(all_sufs, key=lambda x: -olk_suf_counts.get(x, 0)):
        if all_suf_counts.get(suf, 0) < 10: continue
        all_pct = 100 * all_suf_counts.get(suf, 0) / total_all
        olk_pct = 100 * olk_suf_counts.get(suf, 0) / max(1, total_olk)
        cth_pct = 100 * cth_suf_counts.get(suf, 0) / max(1, total_cth)
        olk_e = olk_pct / all_pct if all_pct > 0 else float('inf')
        cth_e = cth_pct / all_pct if all_pct > 0 else float('inf')
        if max(abs(olk_e - 1), abs(cth_e - 1)) > 0.3:
            print(f"{suf:<10} {all_pct:<10.1f} {olk_pct:<10.1f} {olk_e:<14.2f} {cth_pct:<10.1f} {cth_e:.2f}")

    # olk- stem analysis (strip olk, compare stems)
    print("\n--- olk- stem analysis (strip 'olk') ---")
    olk_stems = Counter()
    for r in olk_words:
        stem = r['word'][3:]  # strip 'olk'
        if stem: olk_stems[stem] += 1

    all_words_counter = Counter(r['word'] for r in body)
    qo_words_counter = Counter(r['word'][2:] for r in body if r['word'].startswith('qo'))
    cth_stems_counter = Counter(r['word'][3:] for r in body if r['word'].startswith('cth'))

    print(f"{'Stem':<12} {'olk+stem':<10} {'free_word':<12} {'qo+stem':<10} {'cth+stem':<10}")
    for stem, cnt in olk_stems.most_common(15):
        free = all_words_counter.get(stem, 0)
        qo_match = qo_words_counter.get(stem, 0)
        cth_match = cth_stems_counter.get(stem, 0)
        print(f"{stem:<12} {cnt:<10} {free:<12} {qo_match:<10} {cth_match}")


def h216_suffix_cooccurrence_matrix(records):
    """H216: Do content stems systematically prefer specific suffixes?"""
    print("\n" + "=" * 70)
    print("H216: Suffix Specialization Within Content Stems")
    print("=" * 70)

    body = [r for r in records if r['is_body']]

    # Focus on top content stems: ch, sh, qok, ok, ot, qot, qo(bare)
    # Group words by stem (onset class) → suffix
    stem_suffix_counts = defaultdict(Counter)

    # Define stem extraction for each onset class
    def get_onset_class_and_stem(word):
        w = word
        if w.startswith('qok'): return 'qok', w[3:]
        if w.startswith('qot'): return 'qot', w[3:]
        if w.startswith('qo'): return 'qo', w[2:]
        if w.startswith('ch'): return 'ch', w[2:]
        if w.startswith('sh'): return 'sh', w[2:]
        if w.startswith('ok'): return 'ok', w[2:]
        if w.startswith('ot'): return 'ot', w[2:]
        if w.startswith('ol'): return 'ol', w[2:]
        if w.startswith('olk'): return 'olk', w[3:]
        return None, None

    # For B-paradigm suffixes, check within-stem specialization
    b_suffixes = ['edy', 'eedy', 'eey']
    a_suffixes = ['ol', 'or', 'y', 'aiin']

    # Per onset class: compute edy vs eedy vs eey distribution
    print("\n--- B-paradigm suffix specialization by onset class (B-dialect only) ---")
    print("Does ch prefer -edy while qok prefers -eedy?")

    b_body = [r for r in body if r['dialect'] == 'B']

    onset_b_suf = defaultdict(Counter)
    for r in b_body:
        w = r['word']
        cls, _ = get_onset_class_and_stem(w)
        if cls:
            suf, stem = extract_suffix(w)
            if suf in b_suffixes + a_suffixes:
                onset_b_suf[cls][suf] += 1

    classes = ['ch', 'sh', 'qok', 'qot', 'ok', 'ot', 'qo', 'olk']
    print(f"\n{'Onset':<8} {'n_B':<8} " + "".join(f"{'%-'+suf:<12}" for suf in b_suffixes + a_suffixes[:3]))
    for cls in classes:
        suf_counts = onset_b_suf[cls]
        n = sum(suf_counts.values())
        if n < 20: continue
        row = f"{cls:<8} {n:<8} "
        for suf in b_suffixes + a_suffixes[:3]:
            pct = 100 * suf_counts.get(suf, 0) / n
            row += f"{suf_counts.get(suf,0):3}({pct:4.1f}%)  "
        print(row)

    # Compute entropy of B-suffix usage per onset class
    print("\n--- B-suffix entropy per onset class in B-dialect ---")
    print(f"{'Onset':<8} {'n':<8} {'H_edy bits':<14} {'edy_dom%':<12} {'eedy_dom%':<12} {'eey_dom%':<12}")
    for cls in classes:
        suf_counts = onset_b_suf[cls]
        # Only B-paradigm suffixes
        b_only = {s: suf_counts.get(s, 0) for s in b_suffixes}
        total = sum(b_only.values())
        if total < 10: continue
        H = -sum((c/total)*math.log2(c/total) for c in b_only.values() if c > 0)
        edy_pct = 100 * b_only.get('edy', 0) / total
        eedy_pct = 100 * b_only.get('eedy', 0) / total
        eey_pct = 100 * b_only.get('eey', 0) / total
        print(f"{cls:<8} {total:<8} {H:<14.3f} {edy_pct:<12.1f} {eedy_pct:<12.1f} {eey_pct:.1f}")

    # Cross-dialect: same stem class, different suffix in A vs B
    print("\n--- A-dialect suffix distribution by onset class ---")
    a_body = [r for r in body if r['dialect'] == 'A']
    onset_a_suf = defaultdict(Counter)
    for r in a_body:
        w = r['word']
        cls, _ = get_onset_class_and_stem(w)
        if cls:
            suf, stem = extract_suffix(w)
            if suf in b_suffixes + a_suffixes:
                onset_a_suf[cls][suf] += 1

    print(f"\n{'Onset':<8} {'n_A':<8} " + "".join(f"{'%-'+suf:<12}" for suf in a_suffixes + b_suffixes[:2]))
    for cls in classes:
        suf_counts = onset_a_suf[cls]
        n = sum(suf_counts.values())
        if n < 10: continue
        row = f"{cls:<8} {n:<8} "
        for suf in a_suffixes + b_suffixes[:2]:
            pct = 100 * suf_counts.get(suf, 0) / n
            row += f"{suf_counts.get(suf,0):3}({pct:4.1f}%)  "
        print(row)

    # Stem-level suffix specialization within B-dialect ch-stem
    print("\n--- Within-ch suffix specialization (B-dialect): do specific ch-stems prefer edy vs eedy? ---")
    ch_b = [r for r in b_body if r['word'].startswith('ch')]
    stem_suf_b = defaultdict(Counter)
    for r in ch_b:
        suf, stem = extract_suffix(r['word'])
        if suf in b_suffixes and len(stem) >= 2:
            stem_suf_b[stem][suf] += 1

    print(f"{'Stem':<12} {'n_b_suf':<10} {'edy%':<10} {'eedy%':<10} {'eey%':<10} {'Dominant'}")
    for stem, counts in sorted(stem_suf_b.items(), key=lambda x: -sum(x[1].values())):
        n = sum(counts.values())
        if n < 5: continue
        edy_pct = 100 * counts.get('edy', 0) / n
        eedy_pct = 100 * counts.get('eedy', 0) / n
        eey_pct = 100 * counts.get('eey', 0) / n
        dominant = max(b_suffixes, key=lambda s: counts.get(s, 0))
        print(f"ch+{stem:<9} {n:<10} {edy_pct:<10.1f} {eedy_pct:<10.1f} {eey_pct:<10.1f} {dominant}")

    # Section-level B-suffix variation: does cosmo use different B-suffixes than stars?
    print("\n--- B-suffix by section (B-dialect only) ---")
    b_section_suf = defaultdict(lambda: defaultdict(Counter))
    for r in b_body:
        w = r['word']
        cls, _ = get_onset_class_and_stem(w)
        if cls:
            suf, _ = extract_suffix(w)
            if suf in b_suffixes:
                b_section_suf[cls][r['section']][suf] += 1

    for cls in ['ch', 'sh', 'qok']:
        print(f"\n  Onset class: {cls}")
        for section in ['herbal', 'cosmo', 'stars']:
            suf_counts = b_section_suf[cls].get(section, Counter())
            n = sum(suf_counts.values())
            if n < 5: continue
            edy = 100 * suf_counts.get('edy', 0) / n
            eedy = 100 * suf_counts.get('eedy', 0) / n
            eey = 100 * suf_counts.get('eey', 0) / n
            print(f"    {section}: n={n}, edy={edy:.0f}%, eedy={eedy:.0f}%, eey={eey:.0f}%")


def h219_standalone_free_morphemes(records):
    """H219: Are dy/y free morphemes that grammaticalized into suffixes?"""
    print("\n" + "=" * 70)
    print("H219: Standalone dy/y/edy as Free Morphemes")
    print("=" * 70)

    body = [r for r in records if r['is_body']]
    all_body = Counter(r['word'] for r in body)
    a_body_cnt = Counter(r['word'] for r in body if r['dialect'] == 'A')
    b_body_cnt = Counter(r['word'] for r in body if r['dialect'] == 'B')
    a_total = sum(1 for r in body if r['dialect'] == 'A')
    b_total = sum(1 for r in body if r['dialect'] == 'B')

    candidates = ['dy', 'y', 'edy', 'eedy', 'eey', 'ol', 'or', 'ar', 'al', 'aiin', 'ain']

    print(f"\n--- Standalone potential-suffix words: frequency and distribution ---")
    print(f"{'Word':<10} {'Total':<8} {'A_n':<8} {'B_n':<8} {'A_rate‰':<12} {'B_rate‰':<12} {'B/A':<8}")
    for w in candidates:
        total = all_body.get(w, 0)
        a = a_body_cnt.get(w, 0)
        b = b_body_cnt.get(w, 0)
        a_rate = a / a_total * 1000
        b_rate = b / b_total * 1000
        ba = b_rate / max(0.001, a_rate)
        print(f"{w:<10} {total:<8} {a:<8} {b:<8} {a_rate:<12.3f} {b_rate:<12.3f} {ba:.2f}×")

    # Positional profile of standalone dy, y
    print("\n--- Positional profile of standalone dy, y vs as suffix ---")
    for target in ['dy', 'y']:
        standalone = [r for r in body if r['word'] == target]
        as_suffix = [r for r in body if r['word'].endswith(target) and r['word'] != target and len(r['word']) > len(target)]
        n_s = len(standalone)
        n_sf = len(as_suffix)
        if n_s == 0: continue
        s_lf = sum(1 for r in standalone if r['line_first']) / n_s * 100
        s_ll = sum(1 for r in standalone if r['line_last']) / n_s * 100
        sf_lf = sum(1 for r in as_suffix if r['line_first']) / max(1,n_sf) * 100
        sf_ll = sum(1 for r in as_suffix if r['line_last']) / max(1,n_sf) * 100
        print(f"\n  '{target}' standalone (n={n_s}): LFirst={s_lf:.1f}%, LLast={s_ll:.1f}%")
        print(f"  '-{target}' as suffix (n={n_sf}): LFirst={sf_lf:.1f}%, LLast={sf_ll:.1f}%")

        # Section/dialect distribution
        s_a = sum(1 for r in standalone if r['dialect'] == 'A')
        s_b = sum(1 for r in standalone if r['dialect'] == 'B')
        print(f"  Standalone dialect: A={s_a} ({1000*s_a/a_total:.1f}‰), B={s_b} ({1000*s_b/b_total:.1f}‰)")

    # Compare standalone 'dy' section distribution vs -dy suffix
    print("\n--- Section distribution: standalone vs suffix ---")
    sections = ['herbal', 'pharma', 'cosmo', 'stars', 'astro']
    sect_totals = Counter(r['section'] for r in body)

    for target in ['dy', 'y']:
        standalone_sect = Counter(r['section'] for r in body if r['word'] == target)
        suffix_sect = Counter(r['section'] for r in body
                               if r['word'].endswith(target) and r['word'] != target
                               and len(r['word']) > len(target))

        print(f"\n  '{target}' standalone vs '-{target}' suffix by section:")
        print(f"  {'Section':<12} {'total':<8} {'standalone':<12} {'standalone‰':<14} {'as_suffix':<12} {'suffix‰':<12}")
        for s in sections:
            t = sect_totals[s]
            sa = standalone_sect[s]
            sf = suffix_sect[s]
            print(f"  {s:<12} {t:<8} {sa:<12} {1000*sa/max(1,t):<14.2f} {sf:<12} {1000*sf/max(1,t):.2f}")

    # Is 'edy' also standalone?
    print("\n--- 'edy' as standalone word ---")
    edy_standalone = [r for r in body if r['word'] == 'edy']
    print(f"  'edy' standalone: n={len(edy_standalone)}")
    if edy_standalone:
        for r in edy_standalone[:10]:
            print(f"    folio={r['folio']}, section={r['section']}, dialect={r['dialect']}, LFirst={r['line_first']}, LLast={r['line_last']}")


def main():
    print("Loading data...")
    records, line_records, dialect_map = parse_eva(DATA)
    body_recs = [r for r in records if r['is_body']]
    print(f"Total body tokens: {len(body_recs)}")

    h218_olk_cluster(records)
    h216_suffix_cooccurrence_matrix(records)
    h219_standalone_free_morphemes(records)


if __name__ == '__main__':
    main()
