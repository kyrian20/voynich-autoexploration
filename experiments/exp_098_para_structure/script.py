"""
exp_098: Paragraph Internal Structure (H182), Positional Grammar Classifier (H181)

H181: Can morphological form predict word position with >70% accuracy?
      Build prefix-based position classifier and compute accuracy.

H182: Do Voynichese paragraphs have consistent internal line-type sequence?
      Track opener type at line 1, 2, 3... of each paragraph.
"""

import re
from collections import defaultdict, Counter

DATA_PATH = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'


def folio_base(folio):
    return re.sub(r'\.\d+$', '', folio)


def classify_dialect(folio_stats):
    total = folio_stats.get('total', 0)
    if total == 0:
        return 'unknown'
    rate = (folio_stats.get('edy', 0) + folio_stats.get('eedy', 0)) / total
    return 'B' if rate >= 0.05 else 'A'


def classify_section(folio):
    m = re.match(r'f(\d+)([rv])', folio)
    if not m:
        return 'unknown'
    n = int(m.group(1))
    if n <= 57:
        return 'herbal'
    if 67 <= n <= 73:
        return 'astro'
    if 75 <= n <= 84:
        return 'cosmo'
    if 87 <= n <= 102:
        return 'pharma'
    if 103 <= n <= 116:
        return 'stars'
    return 'other'


def classify_positional_tier(word):
    """Predict positional tier from morphological form."""
    # Para-level: p or f prefix on any stem, bare p or f
    if word.startswith('pch') or word.startswith('psh') or (word.startswith('p') and len(word) >= 3 and not word.startswith('pch') and not word.startswith('psh')):
        return 'PARA'
    if word.startswith('fch') or word.startswith('fsh') or (word.startswith('f') and len(word) >= 3 and not word.startswith('fch') and not word.startswith('fsh')):
        return 'PARA'
    # Line-opener: y or d prefix on ch/sh stems
    if word.startswith('ych') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('dch') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('ysh') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('dsh') and len(word) >= 4:
        return 'LINE_OPEN'
    # Also y+k/t in B
    if word.startswith('yk') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('yt') and len(word) >= 4:
        return 'LINE_OPEN'
    # t or k prefix on ch/sh → intermediate (weak para)
    if (word.startswith('tch') or word.startswith('tsh')) and len(word) >= 4:
        return 'WEAK_PARA'
    if (word.startswith('kch') or word.startswith('ksh')) and len(word) >= 4:
        return 'WEAK_PARA'
    # Mid-line: bare ch/sh, qo+k/t
    if word.startswith('ch') and len(word) >= 3:
        return 'MID'
    if word.startswith('sh') and len(word) >= 3:
        return 'MID'
    if word.startswith('qo') and len(word) >= 4:
        return 'MID'
    # Everything else
    return 'OTHER'


def parse_voynich():
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m:
                continue
            folio_raw = m.group(1)
            folio = folio_raw.lstrip('+*=&~')
            fb = folio_base(folio)
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            for w in words:
                folio_word_stats[fb]['total'] += 1
                if w.endswith('eedy'):
                    folio_word_stats[fb]['eedy'] += 1
                elif w.endswith('edy'):
                    folio_word_stats[fb]['edy'] += 1

    folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}

    # Parse into paragraphs
    paragraphs = []  # list of paragraph dicts
    current_para = None

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m:
                continue
            folio_raw = m.group(1)
            locus_code = m.group(3)

            folio = folio_raw.lstrip('+*=&~')
            fb = folio_base(folio)
            dialect = folio_dialect.get(fb, 'unknown')
            section = classify_section(fb)

            lc_stripped = locus_code.lstrip('+*=/~&')
            is_para_start = lc_stripped.startswith('@')
            is_body = lc_stripped.lstrip('@').startswith('P')

            if not is_body:
                continue

            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]

            if not words:
                continue

            line_record = {
                'folio': fb,
                'dialect': dialect,
                'section': section,
                'words': words,
                'first_word': words[0],
                'last_word': words[-1],
                'n_words': len(words),
                'opener_tier': classify_positional_tier(words[0]),
            }

            if is_para_start or current_para is None or current_para['folio'] != fb:
                # Start a new paragraph
                if current_para is not None:
                    paragraphs.append(current_para)
                current_para = {
                    'folio': fb,
                    'dialect': dialect,
                    'section': section,
                    'lines': [line_record],
                }
            else:
                current_para['lines'].append(line_record)

    if current_para is not None:
        paragraphs.append(current_para)

    return paragraphs


def h181_positional_classifier(paragraphs):
    """H181: Can morphological form predict position with >70% accuracy?"""
    print("=" * 70)
    print("H181: Positional Grammar Classifier Accuracy")
    print("=" * 70)

    # For each word in the corpus, compute:
    # actual position (para_start, line_first, mid, line_last)
    # predicted tier (PARA, LINE_OPEN, WEAK_PARA, MID, OTHER)
    # and check if they match

    # Simplified: at the LINE level, check if the opener tier matches
    # the actual line type (para-start vs within-para line-start vs other)

    for dialect in ['A', 'B']:
        d_paras = [p for p in paragraphs if p['dialect'] == dialect]

        # Line-level records
        para_line_tiers = []  # (line_type, opener_tier)
        wp_line_tiers = []

        for para in d_paras:
            for line_idx, line in enumerate(para['lines']):
                is_ps = (line_idx == 0)
                tier = line['opener_tier']
                if is_ps:
                    para_line_tiers.append(tier)
                else:
                    wp_line_tiers.append(tier)

        total_ps = len(para_line_tiers)
        total_wp = len(wp_line_tiers)

        print(f"\n{'='*50}")
        print(f"Dialect {dialect} (PS={total_ps}, WP={total_wp})")

        # How often does a PARA-tier word appear at para-start vs within-para?
        para_tier_at_ps = sum(1 for t in para_line_tiers if t == 'PARA')
        para_tier_at_wp = sum(1 for t in wp_line_tiers if t == 'PARA')

        line_open_at_ps = sum(1 for t in para_line_tiers if t == 'LINE_OPEN')
        line_open_at_wp = sum(1 for t in wp_line_tiers if t == 'LINE_OPEN')

        mid_at_ps = sum(1 for t in para_line_tiers if t == 'MID')
        mid_at_wp = sum(1 for t in wp_line_tiers if t == 'MID')

        other_at_ps = sum(1 for t in para_line_tiers if t in ('OTHER', 'WEAK_PARA'))
        other_at_wp = sum(1 for t in wp_line_tiers if t in ('OTHER', 'WEAK_PARA'))

        print(f"\n--- Tier Distribution at Para-Start vs Within-Para Lines ---")
        print(f"{'Predicted Tier':<16} {'PS count':<12} {'PS%':<10} {'WP count':<12} {'WP%':<10} {'PS enrichment'}")
        for tier_label, ps_n, wp_n in [
            ('PARA', para_tier_at_ps, para_tier_at_wp),
            ('LINE_OPEN', line_open_at_ps, line_open_at_wp),
            ('WEAK_PARA', sum(1 for t in para_line_tiers if t=='WEAK_PARA'), sum(1 for t in wp_line_tiers if t=='WEAK_PARA')),
            ('MID', mid_at_ps, mid_at_wp),
            ('OTHER', other_at_ps, other_at_wp),
        ]:
            ps_pct = ps_n / total_ps if total_ps else 0
            wp_pct = wp_n / total_wp if total_wp else 0
            enr = ps_pct / wp_pct if wp_pct > 0 else float('inf')
            enr_str = f"{enr:.2f}×" if enr != float('inf') else "inf×"
            print(f"  {tier_label:<14} {ps_n:<12} {ps_pct*100:>6.1f}%    {wp_n:<12} {wp_pct*100:>6.1f}%    {enr_str}")

        # Classification accuracy: if PARA tier → predict para-start; else predict WP
        # Evaluate: what's the F1 for PARA-tier as para-start predictor?
        total_para_tier = para_tier_at_ps + para_tier_at_wp
        precision = para_tier_at_ps / total_para_tier if total_para_tier > 0 else 0
        recall = para_tier_at_ps / total_ps if total_ps > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        baseline_precision = total_ps / (total_ps + total_wp)

        print(f"\n--- PARA-Tier as Para-Start Predictor ---")
        print(f"  Precision: {precision:.3f} ({precision/baseline_precision:.2f}× baseline={baseline_precision:.3f})")
        print(f"  Recall: {recall:.3f}")
        print(f"  F1: {f1:.3f}")

        # LINE_OPEN tier: should be WP line-first (low PS)
        total_lo = line_open_at_ps + line_open_at_wp
        lo_wp_precision = line_open_at_wp / total_lo if total_lo else 0
        print(f"\n--- LINE_OPEN-Tier as Within-Para Line-Opener Predictor ---")
        print(f"  Predicted WP-first precision: {lo_wp_precision:.3f} (n={total_lo})")
        print(f"  (PS contamination: {line_open_at_ps/total_lo*100:.1f}%)")


def h182_para_internal_structure(paragraphs):
    """H182: Paragraph internal line-opener sequence analysis."""
    print("\n" + "=" * 70)
    print("H182: Paragraph Internal Structure — Line-Opener Sequence")
    print("=" * 70)

    for dialect in ['A', 'B']:
        d_paras = [p for p in paragraphs if p['dialect'] == dialect and len(p['lines']) >= 2]

        print(f"\n{'='*50}")
        print(f"Dialect {dialect} — {len(d_paras)} paragraphs with ≥2 lines")

        # Paragraph length distribution
        lengths = Counter(len(p['lines']) for p in d_paras)
        print(f"\nParagraph length distribution:")
        for length in sorted(lengths.keys()):
            count = lengths[length]
            print(f"  {length} lines: {count} paras ({count/len(d_paras)*100:.1f}%)")

        # For each line position within a paragraph, what tier is the opener?
        max_pos = min(10, max(len(p['lines']) for p in d_paras))
        print(f"\n--- Opener Tier by Line Position Within Paragraph ---")
        print(f"{'Position':<12} {'PARA%':<10} {'LINE_OPEN%':<14} {'WEAK_PARA%':<14} {'MID%':<10} {'OTHER%':<10} {'n'}")

        for pos in range(max_pos):
            tiers = [p['lines'][pos]['opener_tier'] for p in d_paras if len(p['lines']) > pos]
            n = len(tiers)
            tier_counts = Counter(tiers)
            para_pct = tier_counts.get('PARA', 0) / n
            lo_pct = tier_counts.get('LINE_OPEN', 0) / n
            wp_pct = tier_counts.get('WEAK_PARA', 0) / n
            mid_pct = tier_counts.get('MID', 0) / n
            other_pct = (tier_counts.get('OTHER', 0)) / n
            pos_label = f"line {pos+1}" if pos > 0 else "line 1 (PS)"
            print(f"  {pos_label:<12} {para_pct*100:>6.1f}%    {lo_pct*100:>6.1f}%          {wp_pct*100:>6.1f}%          {mid_pct*100:>6.1f}%    {other_pct*100:>6.1f}%    {n}")

        # Para-final line: what tier?
        print(f"\n--- Para-Final Line Opener Tier ---")
        para_final_tiers = Counter(p['lines'][-1]['opener_tier'] for p in d_paras)
        n_total = len(d_paras)
        for tier, cnt in sorted(para_final_tiers.items(), key=lambda x: -x[1]):
            print(f"  {tier}: {cnt} ({cnt/n_total*100:.1f}%)")

        # Para-final last word onset
        print(f"\n--- Para-Final Line Last Word Onset ---")
        def get_onset(word):
            if word.startswith('qo'):
                return 'qo'
            if word.startswith('ch'):
                return 'ch'
            if word.startswith('sh'):
                return 'sh'
            return word[0] if word else 'other'

        para_final_closers = Counter(get_onset(p['lines'][-1]['last_word']) for p in d_paras)
        for onset, cnt in sorted(para_final_closers.items(), key=lambda x: -x[1])[:8]:
            print(f"  {onset}: {cnt} ({cnt/n_total*100:.1f}%)")

        # Most common 2-line opener sequence (para line 1 → line 2)
        print(f"\n--- 2-Line Opener Sequence (Line 1 → Line 2) ---")
        two_seqs = Counter()
        for p in d_paras:
            if len(p['lines']) >= 2:
                seq = (p['lines'][0]['opener_tier'], p['lines'][1]['opener_tier'])
                two_seqs[seq] += 1
        for seq, cnt in two_seqs.most_common(10):
            print(f"  {seq[0]} → {seq[1]}: {cnt} ({cnt/len(d_paras)*100:.1f}%)")


def h183_paragraph_length_grammar(paragraphs):
    """H183: Are paragraph lengths consistent and section-specific?"""
    print("\n" + "=" * 70)
    print("H183: Paragraph Length by Section and Dialect")
    print("=" * 70)

    for dialect in ['A', 'B']:
        d_paras = [p for p in paragraphs if p['dialect'] == dialect]
        print(f"\nDialect {dialect}:")
        sections = sorted(set(p['section'] for p in d_paras))
        for sect in sections:
            s_paras = [p for p in d_paras if p['section'] == sect]
            if len(s_paras) < 3:
                continue
            lengths = [len(p['lines']) for p in s_paras]
            mean_len = sum(lengths) / len(lengths)
            median_len = sorted(lengths)[len(lengths)//2]
            print(f"  {sect}: n={len(s_paras)}, mean={mean_len:.1f} lines, median={median_len}, max={max(lengths)}, min={min(lengths)}")


def main():
    print("Loading data...")
    paragraphs = parse_voynich()
    print(f"Total paragraphs: {len(paragraphs)}")

    a_paras = sum(1 for p in paragraphs if p['dialect'] == 'A')
    b_paras = sum(1 for p in paragraphs if p['dialect'] == 'B')
    print(f"A dialect paragraphs: {a_paras}, B dialect: {b_paras}")

    print()
    h181_positional_classifier(paragraphs)
    h182_para_internal_structure(paragraphs)
    h183_paragraph_length_grammar(paragraphs)


if __name__ == '__main__':
    main()
