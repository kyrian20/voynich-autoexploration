#!/usr/bin/env python3
"""
exp_110: Paragraph-Internal Line Grammar Arc (H215) + Extreme B-Pole Onset Classes (H214)
Tests:
  H215: Do lines within a paragraph follow a predictable sequential positional grammar arc?
  H214: Does the dialect polarity axis have a B-extreme counterpart to cth- (14× A)?
"""

import re
import math
from collections import defaultdict, Counter

DATA = 'data/transcriptions/eva_zl3b.txt'

def parse_eva(path):
    """Parse EVA ZL3b IVTFF. Returns (records, line_records, dialect_map)."""
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
            if not m:
                continue
            locus_code = m.group(1)
            text = m.group(2).strip()

            # Split locus into folio.line and locus_type
            comma_idx = locus_code.find(',')
            if comma_idx < 0:
                continue
            folio_line = locus_code[:comma_idx]   # e.g. 'f1r.1'
            locus_type = locus_code[comma_idx+1:] # e.g. '@P0', '+P0', '*P0', '@Lp'

            # Extract folio number
            fm = re.match(r'f(\d+)', folio_line)
            if not fm:
                continue
            folio_num = int(fm.group(1))

            # Extract line in folio
            lm = re.match(r'f\w+\.(\d+)', folio_line)
            line_in_folio = int(lm.group(1)) if lm else 0

            # Locus type: strip prefix chars to get body/label id
            prefix = ''
            lt = locus_type
            for c in locus_type:
                if c in '@+*=~&':
                    prefix += c
                else:
                    break
            lt = locus_type[len(prefix):]

            is_body = bool(re.match(r'P', lt))
            is_label = bool(re.match(r'L', lt))
            is_para_start = locus_type.startswith('@') or locus_type.startswith('*')

            # Para id (P0, P1, Pt, Pa, ...)
            pm = re.match(r'P(\w+)', lt)
            para_id = pm.group(1) if pm else 'unknown'
            try:
                para_num = int(para_id)
            except:
                para_num = -1

            if not (is_body or is_label):
                continue

            # Clean text: remove special markers
            text_clean = re.sub(r'<[^>]*>', '', text)
            text_clean = re.sub(r'\[[^\]]*\]', lambda m: m.group(0).replace('[','').replace(']','').split(':')[0], text_clean)
            text_clean = re.sub(r'\{[^}]*\}', '', text_clean)
            text_clean = re.sub(r'@\d+;?', '', text_clean)
            text_clean = re.sub(r'<%>', '', text_clean)
            text_clean = re.sub(r'<!.*?>', '', text_clean)
            text_clean = re.sub(r'<\$>', '', text_clean)

            words = [w for w in re.split(r'[-.\s,]', text_clean)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]

            if not words:
                continue

            section = section_map.get(folio_num, 'other')

            for w in words:
                if 'edy' in w or 'eedy' in w:
                    edy_counts[folio_num] += 1
                total_counts[folio_num] += 1

            raw_lines.append({
                'folio': folio_num,
                'folio_str': folio_line,
                'line_in_folio': line_in_folio,
                'locus_type': locus_type,
                'section': section,
                'is_body': is_body,
                'is_label': is_label,
                'is_para_start': is_para_start,
                'para_num': para_num,
                'para_id': para_id,
                'words': words,
                'n_words': len(words),
            })

    # Assign dialect
    dialect_map = {}
    for fnum in total_counts:
        rate = edy_counts[fnum] / total_counts[fnum] if total_counts[fnum] > 0 else 0
        dialect_map[fnum] = 'B' if rate >= 0.05 else 'A'

    # Assign line_in_para: within each (folio, para_num) group
    para_groups = defaultdict(list)
    for lr in raw_lines:
        if lr['is_body'] and lr['para_num'] >= 0:
            key = (lr['folio'], lr['para_num'])
            para_groups[key].append(lr)

    for key, group in para_groups.items():
        group.sort(key=lambda x: x['line_in_folio'])
        for i, lr in enumerate(group):
            lr['line_in_para'] = i + 1  # 1-indexed

    # For lines without line_in_para (labels or non-numeric para)
    for lr in raw_lines:
        if 'line_in_para' not in lr:
            lr['line_in_para'] = 0
        lr['dialect'] = dialect_map.get(lr['folio'], 'A')

    # Build word-level records
    records = []
    for lr in raw_lines:
        words = lr['words']
        n = len(words)
        for i, w in enumerate(words):
            records.append({
                'word': w,
                'folio': lr['folio'],
                'section': lr['section'],
                'dialect': lr['dialect'],
                'is_para_start': lr['is_para_start'] and (i == 0),
                'is_body': lr['is_body'],
                'is_label': lr['is_label'],
                'line_first': (i == 0),
                'line_last': (i == n - 1),
                'para_num': lr['para_num'],
                'line_in_para': lr['line_in_para'],
                'pos_in_line': i,
            })

    return records, raw_lines, dialect_map


def get_word_tier(word):
    """Classify into PARA, LINE_OPEN, WEAK_PARA, MID, OTHER tiers."""
    w = word.lower()
    if re.match(r'^(p|f)(ch|sh|k|t)', w): return 'PARA'
    if re.match(r'^(k|t)(ch|sh)', w): return 'WEAK_PARA'
    if re.match(r'^olf', w) or re.match(r'^olke', w) or re.match(r'^op[^a-z]', w): return 'PARA'
    if re.match(r'^d(ch|sh)', w) or re.match(r'^y(ch|sh)', w): return 'LINE_OPEN'
    if w.startswith('ch') or w.startswith('sh') or w.startswith('qo'): return 'MID'
    return 'OTHER'


def h215_paragraph_line_arc(records, line_records):
    """H215: Do paragraph-internal lines follow a grammar arc?"""
    print("=" * 70)
    print("H215: Paragraph-Internal Line Grammar Arc")
    print("=" * 70)

    body_lines = [lr for lr in line_records if lr['is_body'] and lr['para_num'] >= 0]
    print(f"Body lines with para_num: {len(body_lines)}")

    # Group by (folio, para_num)
    para_groups = defaultdict(list)
    for lr in body_lines:
        key = (lr['folio'], lr['para_num'])
        para_groups[key].append(lr)

    for key in para_groups:
        para_groups[key].sort(key=lambda x: x['line_in_folio'])

    # Only use paragraphs with 4+ lines
    long_paras = {k: v for k, v in para_groups.items() if len(v) >= 4}
    all_paras = para_groups

    print(f"Total paragraphs: {len(all_paras)}")
    print(f"Paragraphs with 4+ lines: {len(long_paras)}")
    print(f"Lines in long paras: {sum(len(v) for v in long_paras.values())}")

    # Bin by relative position within paragraph
    bins = [(0.0, 0.1), (0.1, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 0.9), (0.9, 1.01)]
    bin_labels = ['0-10%', '10-25%', '25-50%', '50-75%', '75-90%', '90-100%']

    tier_counts = defaultdict(lambda: defaultdict(int))
    bin_word_counts = defaultdict(int)
    am_counts = defaultdict(int)
    dal_counts = defaultdict(int)

    for key, lines in long_paras.items():
        n = len(lines)
        for idx, lr in enumerate(lines):
            rel_pos = idx / (n - 1) if n > 1 else 0.5
            bin_idx = len(bins) - 1
            for i, (lo, hi) in enumerate(bins):
                if lo <= rel_pos < hi:
                    bin_idx = i
                    break
            bl = bin_labels[bin_idx]

            for w in lr['words']:
                tier = get_word_tier(w)
                tier_counts[bl][tier] += 1
                bin_word_counts[bl] += 1
                if w.endswith('am') and len(w) >= 3:
                    am_counts[bl] += 1
                if w in ['dal', 'dam', 'dy', 'daly', 'darol', 'doldy', 'dar']:
                    dal_counts[bl] += 1

    print("\n--- Tier distribution by paragraph-relative position (4+ line paras) ---")
    print(f"{'Bin':<12} {'N_words':<10} {'PARA%':<8} {'WEAK_P%':<9} {'LN_OPEN%':<10} {'MID%':<8} {'OTHER%':<8} {'-am%':<8} {'dal%':<8}")

    for bl in bin_labels:
        n = bin_word_counts[bl]
        if n == 0:
            continue
        para_pct = 100 * tier_counts[bl]['PARA'] / n
        weak_pct = 100 * tier_counts[bl]['WEAK_PARA'] / n
        lo_pct = 100 * tier_counts[bl]['LINE_OPEN'] / n
        mid_pct = 100 * tier_counts[bl]['MID'] / n
        other_pct = 100 * tier_counts[bl]['OTHER'] / n
        am_pct = 100 * am_counts[bl] / n
        dal_pct = 100 * dal_counts[bl] / n
        print(f"{bl:<12} {n:<10} {para_pct:<8.1f} {weak_pct:<9.1f} {lo_pct:<10.1f} {mid_pct:<8.1f} {other_pct:<8.1f} {am_pct:<8.2f} {dal_pct:<8.2f}")

    # Absolute position from start and end
    print("\n--- Tier distribution by absolute line position (from para start and end) ---")
    abs_pos_tiers = defaultdict(lambda: defaultdict(int))
    abs_pos_counts = defaultdict(int)
    abs_pos_am = defaultdict(int)
    abs_pos_dal = defaultdict(int)
    abs_pos_oly = defaultdict(int)

    for key, lines in long_paras.items():
        n = len(lines)
        for idx, lr in enumerate(lines):
            from_start = idx + 1
            from_end = n - idx

            for w in lr['words']:
                tier = get_word_tier(w)
                if from_start <= 5:
                    pos = f'start_{from_start}'
                    abs_pos_tiers[pos][tier] += 1
                    abs_pos_counts[pos] += 1
                if from_end <= 5:
                    pos = f'end_{from_end}'
                    abs_pos_tiers[pos][tier] += 1
                    abs_pos_counts[pos] += 1
                    if w.endswith('am') and len(w) >= 3:
                        abs_pos_am[pos] += 1
                    if w in ['dal', 'dam', 'dy', 'daly']:
                        abs_pos_dal[pos] += 1
                    if w in ['oly', 'oldy', 'olkeedy', 'olkedy']:
                        abs_pos_oly[pos] += 1

    print(f"\n{'Position':<14} {'N_words':<10} {'PARA%':<8} {'WEAK_P%':<9} {'LN_OPEN%':<10} {'MID%':<8} {'OTHER%':<8} {'-am%':<7} {'oly%':<7}")
    for pos in [f'start_{i}' for i in range(1, 6)] + [f'end_{i}' for i in range(5, 0, -1)]:
        n = abs_pos_counts[pos]
        if n < 10:
            continue
        para_pct = 100 * abs_pos_tiers[pos]['PARA'] / n
        weak_pct = 100 * abs_pos_tiers[pos]['WEAK_PARA'] / n
        lo_pct = 100 * abs_pos_tiers[pos]['LINE_OPEN'] / n
        mid_pct = 100 * abs_pos_tiers[pos]['MID'] / n
        other_pct = 100 * abs_pos_tiers[pos]['OTHER'] / n
        am_pct = 100 * abs_pos_am.get(pos, 0) / n
        oly_pct = 100 * abs_pos_oly.get(pos, 0) / n
        lbl = pos.replace('start_', 'line+').replace('end_', 'line-')
        print(f"{lbl:<14} {n:<10} {para_pct:<8.1f} {weak_pct:<9.1f} {lo_pct:<10.1f} {mid_pct:<8.1f} {other_pct:<8.1f} {am_pct:<7.2f} {oly_pct:<7.2f}")

    # By dialect
    print("\n--- Line grammar arc by dialect ---")
    for dialect in ['A', 'B']:
        d_paras = {k: v for k, v in long_paras.items()
                   if v[0].get('dialect', 'A') == dialect}
        print(f"\n  Dialect {dialect}: {len(d_paras)} long paragraphs")

        d_tier = defaultdict(lambda: defaultdict(int))
        d_count = defaultdict(int)
        d_am = defaultdict(int)

        for key, lines in d_paras.items():
            n = len(lines)
            for idx, lr in enumerate(lines):
                from_end = n - idx
                from_start = idx + 1
                for w in lr['words']:
                    tier = get_word_tier(w)
                    for pos_key, cond in [(f'start_{from_start}', from_start <= 3),
                                          (f'end_{from_end}', from_end <= 3)]:
                        if cond:
                            d_tier[pos_key][tier] += 1
                            d_count[pos_key] += 1
                            if pos_key.startswith('end') and w.endswith('am') and len(w) >= 3:
                                d_am[pos_key] += 1

        print(f"  {'Position':<12} {'N':<8} {'PARA%':<8} {'LN_OPEN%':<10} {'MID%':<8} {'OTHER%':<9} {'-am%':<8}")
        for pos in ['start_1', 'start_2', 'start_3', 'end_3', 'end_2', 'end_1']:
            n = d_count[pos]
            if n < 5:
                continue
            para_pct = 100 * d_tier[pos]['PARA'] / n
            lo_pct = 100 * d_tier[pos]['LINE_OPEN'] / n
            mid_pct = 100 * d_tier[pos]['MID'] / n
            other_pct = 100 * (d_tier[pos]['OTHER']) / n
            am_pct = 100 * d_am.get(pos, 0) / n
            print(f"  {pos:<12} {n:<8} {para_pct:<8.1f} {lo_pct:<10.1f} {mid_pct:<8.1f} {other_pct:<9.1f} {am_pct:<8.2f}")

    # Words enriched at paragraph-LAST line
    print("\n--- Words enriched at paragraph-LAST line ---")
    last_words = Counter()
    all_body_words = Counter()

    for key, lines in long_paras.items():
        for w in lines[-1]['words']:
            last_words[w] += 1
        for lr in lines:
            for w in lr['words']:
                all_body_words[w] += 1

    total_last = sum(last_words.values())
    total_all = sum(all_body_words.values())

    print(f"{'Word':<15} {'last_n':<8} {'last%':<10} {'all%':<10} {'Enrich'}")
    candidates = [(w, c) for w, c in last_words.items() if c >= 5]
    candidates.sort(key=lambda x: -(x[1]/total_last) / max(0.00001, all_body_words[x[0]]/total_all))
    for w, c in candidates[:20]:
        all_rate = all_body_words[w] / total_all
        last_rate = c / total_last
        enrich = last_rate / all_rate if all_rate > 0 else float('inf')
        if enrich >= 1.5:
            print(f"{w:<15} {c:<8} {100*last_rate:<10.2f} {100*all_rate:<10.2f} {enrich:.2f}×")

    # Words enriched at paragraph-FIRST line
    print("\n--- Words enriched at paragraph-FIRST line ---")
    first_words = Counter()
    for key, lines in long_paras.items():
        for w in lines[0]['words']:
            first_words[w] += 1

    total_first = sum(first_words.values())
    candidates = [(w, c) for w, c in first_words.items() if c >= 5]
    candidates.sort(key=lambda x: -(x[1]/total_first) / max(0.00001, all_body_words[x[0]]/total_all))
    for w, c in candidates[:20]:
        all_rate = all_body_words[w] / total_all
        first_rate = c / total_first
        enrich = first_rate / all_rate if all_rate > 0 else float('inf')
        if enrich >= 1.5:
            print(f"{w:<15} {c:<8} {100*first_rate:<10.2f} {100*all_rate:<10.2f} {enrich:.2f}×")


def h214_b_pole_onset_classes(records):
    """H214: Find the extreme B-pole counterpart to cth-."""
    print("\n" + "=" * 70)
    print("H214: Extreme B-Pole Onset Classes (B/A Rate Ratio Survey)")
    print("=" * 70)

    body_records = [r for r in records if r['is_body']]

    a_total = sum(1 for r in body_records if r['dialect'] == 'A')
    b_total = sum(1 for r in body_records if r['dialect'] == 'B')
    print(f"\nTotal body tokens: {len(body_records)} (A={a_total}, B={b_total})")

    # Build onset → dialect counts for onset lengths 2, 3, 4
    onset_stats = defaultdict(lambda: {'A': 0, 'B': 0, 'n': 0, 'lf': 0, 'll': 0, 'ps': 0})

    for r in body_records:
        w = r['word']
        d = r['dialect']
        # Test 2-char, 3-char, 4-char onsets
        for length in [2, 3, 4]:
            if len(w) > length:
                onset = w[:length]
                if re.match(r'^[a-z]+$', onset) and not re.search(r'\d', onset):
                    onset_stats[onset][d] += 1
                    onset_stats[onset]['n'] += 1
                    if r['line_first']:
                        onset_stats[onset]['lf'] += 1
                    if r['line_last']:
                        onset_stats[onset]['ll'] += 1
                    if r['is_para_start']:
                        onset_stats[onset]['ps'] += 1

    # Compute B/A ratio for onset clusters with total n >= 30
    results = []
    for onset, s in onset_stats.items():
        a, b, total = s['A'], s['B'], s['n']
        if total < 30:
            continue
        a_rate = a / a_total
        b_rate = b / b_total
        ba_ratio = b_rate / a_rate if a_rate > 0 else float('inf')
        ab_ratio = a_rate / b_rate if b_rate > 0 else float('inf')
        lf_pct = 100 * s['lf'] / total
        ll_pct = 100 * s['ll'] / total
        ps_pct = 100 * s['ps'] / total
        results.append((onset, a, b, total, a_rate, b_rate, ba_ratio, ab_ratio, lf_pct, ll_pct, ps_pct))

    results.sort(key=lambda x: -x[6])  # Sort by B/A ratio

    print(f"\n--- Most B-DOMINANT onset clusters (n>=30) ---")
    print(f"{'Onset':<12} {'Total':<8} {'A_n':<8} {'B_n':<8} {'A_rate‰':<12} {'B_rate‰':<12} {'B/A':<10} {'LFirst%':<9} {'LLast%':<9} {'PS%'}")
    for row in results[:30]:
        onset, a, b, total, a_rate, b_rate, ba_ratio, ab_ratio, lf, ll, ps = row
        if ba_ratio >= 2.0:
            print(f"{onset:<12} {total:<8} {a:<8} {b:<8} {1000*a_rate:<12.2f} {1000*b_rate:<12.2f} {ba_ratio:<10.2f} {lf:<9.1f} {ll:<9.1f} {ps:.2f}")

    print(f"\n--- Most A-DOMINANT onset clusters (n>=30) ---")
    results_ab = sorted(results, key=lambda x: -x[7])
    print(f"{'Onset':<12} {'Total':<8} {'A_n':<8} {'B_n':<8} {'A_rate‰':<12} {'B_rate‰':<12} {'A/B':<10} {'LFirst%':<9} {'LLast%':<9} {'PS%'}")
    for row in results_ab[:25]:
        onset, a, b, total, a_rate, b_rate, ba_ratio, ab_ratio, lf, ll, ps = row
        if ab_ratio >= 2.0:
            print(f"{onset:<12} {total:<8} {a:<8} {b:<8} {1000*a_rate:<12.2f} {1000*b_rate:<12.2f} {ab_ratio:<10.2f} {lf:<9.1f} {ll:<9.1f} {ps:.2f}")

    # Complete dialect polarity axis (n>=50)
    print("\n--- Complete Dialect Polarity Axis (onset clusters, n>=50) ---")
    axis = [(row[0], row[2], row[1], row[3], row[4], row[5], row[6])
            for row in results if row[3] >= 50]
    axis.sort(key=lambda x: x[6])

    print(f"{'Onset':<12} {'B_n':<8} {'A_n':<8} {'Total':<8} {'A_rate‰':<12} {'B_rate‰':<12} {'B/A':<8} {'Pole'}")
    for onset, b, a, total, a_rate, b_rate, ba_ratio in axis:
        if ba_ratio < 0.1:
            pole = 'EXTREME-A'
        elif ba_ratio < 0.35:
            pole = 'A-strong'
        elif ba_ratio < 0.7:
            pole = 'A-lean'
        elif ba_ratio < 1.5:
            pole = 'neutral'
        elif ba_ratio < 3.0:
            pole = 'B-lean'
        elif ba_ratio < 8.0:
            pole = 'B-strong'
        else:
            pole = 'EXTREME-B'
        print(f"{onset:<12} {b:<8} {a:<8} {total:<8} {1000*a_rate:<12.3f} {1000*b_rate:<12.3f} {ba_ratio:<8.3f} {pole}")

    # Top B-dominant: suffix and section analysis
    b_top = [row for row in results if row[6] >= 3.0]

    print(f"\n--- Section distribution of top B-dominant onsets ---")
    section_totals = Counter(r['section'] for r in body_records)
    sections = ['herbal', 'pharma', 'cosmo', 'stars', 'astro']

    section_onset = defaultdict(lambda: defaultdict(int))
    for r in body_records:
        w = r['word']
        for row in b_top[:12]:
            onset = row[0]
            if w.startswith(onset):
                section_onset[onset][r['section']] += 1

    print(f"{'Onset':<10} {'B/A':<6} " + " ".join(f"{s:<10}" for s in sections))
    for row in b_top[:12]:
        onset = row[0]
        ba = row[6]
        sec_str = " ".join(
            f"{section_onset[onset][s]}/{section_totals[s]}({1000*section_onset[onset][s]/max(1,section_totals[s]):.0f}‰)"
            for s in sections
        )
        print(f"{onset:<10} {ba:<6.1f} {sec_str}")

    # Suffix analysis of top B-dominant
    all_suffix_counts = Counter()
    for r in body_records:
        w = r['word']
        for suf in ['eedy','edy','eey','ol','or','y','aiin','ain','ar','al','ey','dy']:
            if w.endswith(suf):
                all_suffix_counts[suf] += 1
                break
    total_suffix = sum(all_suffix_counts.values())

    print(f"\n--- Suffix enrichment of top B-dominant onsets ---")
    for row in b_top[:5]:
        onset = row[0]
        ba = row[6]
        onset_recs = [r for r in body_records if r['word'].startswith(onset)]
        n = len(onset_recs)
        suf_counts = Counter()
        for r in onset_recs:
            w = r['word']
            for suf in ['eedy','edy','eey','ol','or','y','aiin','ain','ar','al','ey','dy']:
                if w.endswith(suf):
                    suf_counts[suf] += 1
                    break
        print(f"\n  Onset '{onset}' (B/A={ba:.1f}×, n={n}):")
        for suf, cnt in sorted(suf_counts.items(), key=lambda x: -x[1])[:8]:
            all_pct = 100 * all_suffix_counts[suf] / total_suffix if total_suffix > 0 else 0
            this_pct = 100 * cnt / n
            enrich = this_pct / all_pct if all_pct > 0 else float('inf')
            print(f"    -{suf}: {cnt} ({this_pct:.1f}% vs {all_pct:.1f}% all → {enrich:.2f}×)")


def main():
    print("Loading data...")
    records, line_records, dialect_map = parse_eva(DATA)

    body_recs = [r for r in records if r['is_body']]
    print(f"Total body tokens: {len(body_recs)}")
    print(f"Total body lines: {len([lr for lr in line_records if lr['is_body']])}")

    h215_paragraph_line_arc(records, line_records)
    h214_b_pole_onset_classes(records)


if __name__ == '__main__':
    main()
