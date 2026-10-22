"""
exp_100: Extended Positional Classifier (H188) and B Para-Final Vocabulary (H189)

H188: Add bare_k and bare_t to PARA tier; test coverage improvement.
      Extended PARA = {p,f}+stem + bare_k + bare_t

H189: B para-final closing words (okeey, orol, shedy) — are they a coherent class?

H190 (bonus): Astro section anomalous para-starts.
"""
from pathlib import Path as _RepositoryPath

import re
from collections import defaultdict, Counter

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')


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


def classify_tier_v1(word):
    """Original classifier (PARA = p/f+stem only)."""
    if (word.startswith('pch') or word.startswith('psh') or
            (word.startswith('p') and len(word) >= 3)):
        return 'PARA'
    if (word.startswith('fch') or word.startswith('fsh') or
            (word.startswith('f') and len(word) >= 3)):
        return 'PARA'
    if word.startswith('ych') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('dch') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('ysh') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('dsh') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('yk') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('yt') and len(word) >= 4:
        return 'LINE_OPEN'
    if (word.startswith('tch') or word.startswith('tsh')) and len(word) >= 4:
        return 'WEAK_PARA'
    if (word.startswith('kch') or word.startswith('ksh')) and len(word) >= 4:
        return 'WEAK_PARA'
    if word.startswith('ch') and len(word) >= 3:
        return 'MID'
    if word.startswith('sh') and len(word) >= 3:
        return 'MID'
    if word.startswith('qo') and len(word) >= 4:
        return 'MID'
    return 'OTHER'


def classify_tier_v2(word):
    """Extended classifier: PARA includes bare_k, bare_t, bare_p, bare_f."""
    # PARA tier: p/f prefix OR bare gallows (k, t)
    if (word.startswith('pch') or word.startswith('psh') or
            (word.startswith('p') and len(word) >= 3)):
        return 'PARA'
    if (word.startswith('fch') or word.startswith('fsh') or
            (word.startswith('f') and len(word) >= 3)):
        return 'PARA'
    # Bare k and t gallows (but NOT y+k, qo+k, etc.)
    if (word.startswith('k') and not word.startswith('kch') and
            not word.startswith('ksh') and len(word) >= 2):
        return 'PARA'
    if (word.startswith('t') and not word.startswith('tch') and
            not word.startswith('tsh') and len(word) >= 2):
        return 'PARA'
    # LINE_OPEN tier
    if word.startswith('ych') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('dch') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('ysh') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('dsh') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('yk') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('yt') and len(word) >= 4:
        return 'LINE_OPEN'
    # WEAK_PARA: t/k + ch/sh (compound)
    if (word.startswith('tch') or word.startswith('tsh')) and len(word) >= 4:
        return 'WEAK_PARA'
    if (word.startswith('kch') or word.startswith('ksh')) and len(word) >= 4:
        return 'WEAK_PARA'
    # MID tier
    if word.startswith('ch') and len(word) >= 3:
        return 'MID'
    if word.startswith('sh') and len(word) >= 3:
        return 'MID'
    if word.startswith('qo') and len(word) >= 4:
        return 'MID'
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

    paragraphs = {}
    current_para = None
    para_count = 0

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

            if is_para_start:
                para_count += 1
                current_para = para_count
                paragraphs[current_para] = {
                    'dialect': dialect,
                    'section': section,
                    'folio': fb,
                    'lines': []
                }
            if current_para is not None:
                paragraphs[current_para]['lines'].append(words)

    return paragraphs


def h188_extended_classifier(paragraphs):
    """H188: Test extended classifier with bare_k and bare_t in PARA tier."""
    print("=" * 70)
    print("H188: Extended Positional Classifier (v2) — bare_k + bare_t in PARA Tier")
    print("=" * 70)

    for dialect in ['A', 'B']:
        d_paras = {pid: p for pid, p in paragraphs.items()
                   if p['dialect'] == dialect and p['lines']}
        print(f"\n{'='*50}")
        print(f"Dialect {dialect} — n_paragraphs={len(d_paras)}")

        # Collect PS and WP first words
        ps_words = []
        wp_words = []

        for pid, para in d_paras.items():
            lines = para['lines']
            if not lines or not lines[0]:
                continue
            ps_words.append(lines[0][0])
            for li in range(1, len(lines)):
                if lines[li]:
                    wp_words.append(lines[li][0])

        n_ps = len(ps_words)
        n_wp = len(wp_words)

        # Compare v1 vs v2 classifier
        for version, classify_fn in [('v1 (original)', classify_tier_v1),
                                      ('v2 (extended)', classify_tier_v2)]:
            ps_tiers = [classify_fn(w) for w in ps_words]
            wp_tiers = [classify_fn(w) for w in wp_words]

            ps_counter = Counter(ps_tiers)
            wp_counter = Counter(wp_tiers)

            para_ps = ps_counter.get('PARA', 0)
            para_wp = wp_counter.get('PARA', 0)
            lo_ps = ps_counter.get('LINE_OPEN', 0)
            lo_wp = wp_counter.get('LINE_OPEN', 0)
            other_ps = ps_counter.get('OTHER', 0)

            para_ps_rate = para_ps / n_ps if n_ps > 0 else 0
            para_wp_rate = para_wp / n_wp if n_wp > 0 else 0
            enrich = para_ps_rate / para_wp_rate if para_wp_rate > 0 else float('inf')

            lo_precision = lo_wp / (lo_ps + lo_wp) if (lo_ps + lo_wp) > 0 else 0

            print(f"\n  Classifier {version}:")
            print(f"  PARA at PS: {para_ps}/{n_ps} ({para_ps_rate*100:.1f}%), WP: {para_wp}/{n_wp} ({para_wp_rate*100:.1f}%), enrichment={enrich:.2f}×")
            print(f"  LINE_OPEN at PS: {lo_ps}/{n_ps} ({lo_ps/n_ps*100:.1f}%), WP precision={lo_precision*100:.1f}%")
            print(f"  OTHER at PS: {other_ps}/{n_ps} ({other_ps/n_ps*100:.1f}%)")

            # Tier breakdown
            print(f"  Full tier distribution at PS:")
            for tier in ['PARA', 'LINE_OPEN', 'WEAK_PARA', 'MID', 'OTHER']:
                ps_cnt = ps_counter.get(tier, 0)
                wp_cnt = wp_counter.get(tier, 0)
                ps_rate = ps_cnt / n_ps
                wp_rate = wp_cnt / n_wp if n_wp > 0 else 0
                enr = ps_rate / wp_rate if wp_rate > 0 else float('inf')
                print(f"    {tier:<12}: PS={ps_cnt:3d} ({ps_rate*100:5.1f}%), WP={wp_cnt:4d} ({wp_rate*100:5.1f}%), enrich={enr:.2f}×")

        # What are the remaining OTHER words after v2?
        remaining_other = [w for w in ps_words if classify_tier_v2(w) == 'OTHER']
        print(f"\n  Remaining OTHER after v2 (n={len(remaining_other)}):")
        other_counter = Counter(remaining_other)
        for w, cnt in other_counter.most_common(20):
            print(f"    {w}: {cnt}")

        # Onset of remaining OTHER
        other_onsets = Counter(w[0] for w in remaining_other if w)
        print(f"\n  Remaining OTHER onset distribution: {other_onsets.most_common(10)}")

        # Precision/recall for v2 PARA as para-start predictor
        true_pos = sum(1 for w in ps_words if classify_tier_v2(w) == 'PARA')
        false_pos = sum(1 for w in wp_words if classify_tier_v2(w) == 'PARA')
        false_neg = n_ps - true_pos
        precision = true_pos / (true_pos + false_pos) if (true_pos + false_pos) > 0 else 0
        recall = true_pos / n_ps if n_ps > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        print(f"\n  v2 PARA Classifier Performance (para-start prediction):")
        print(f"  Precision: {precision:.3f}, Recall: {recall:.3f}, F1: {f1:.3f}")
        print(f"  Baseline: {n_ps/(n_ps+n_wp):.3f}")


def h189_b_para_final_vocabulary(paragraphs):
    """H189: B para-final closing words — coherent class?"""
    print("\n" + "=" * 70)
    print("H189: B Para-Final Closing Vocabulary Analysis")
    print("=" * 70)

    b_paras = {pid: p for pid, p in paragraphs.items()
               if p['dialect'] == 'B' and len(p['lines']) >= 2}
    print(f"B dialect paragraphs with ≥2 lines: {len(b_paras)}")

    # Collect para-final last words and within-para line-last words
    para_final = []  # (word, section)
    within_para = []  # (word, section)

    for pid, para in b_paras.items():
        lines = para['lines']
        section = para['section']
        n = len(lines)
        if lines[-1]:
            para_final.append((lines[-1][-1], section))
        for li in range(1, n - 1):
            if lines[li]:
                within_para.append((lines[li][-1], section))

    pf_words = [w for w, s in para_final]
    wp_words = [w for w, s in within_para]
    n_pf = len(pf_words)
    n_wp = len(wp_words)

    # Compute per-word enrichment
    pf_counter = Counter(pf_words)
    wp_counter = Counter(wp_words)

    print(f"\nPara-final words: {n_pf}, Within-para line-last: {n_wp}")
    print(f"\n--- B Para-Final Closing Words (enriched ≥2×, n_pf≥2) ---")
    print(f"{'Word':<18} {'PF_n':>5} {'PF%':>7} {'WP_n':>5} {'WP%':>7} {'Enrich':>8} {'Suffix'}")
    closing_words = []
    for word, pf_n in pf_counter.most_common():
        pf_rate = pf_n / n_pf
        wp_n = wp_counter.get(word, 0)
        wp_rate = wp_n / n_wp if n_wp > 0 else 0
        enrich = pf_rate / wp_rate if wp_rate > 0 else float('inf')
        if pf_n >= 2 and enrich >= 2.0:
            closing_words.append((word, pf_n, pf_rate, wp_n, wp_rate, enrich))

    closing_words.sort(key=lambda x: -x[5])
    for word, pf_n, pf_rate, wp_n, wp_rate, enrich in closing_words:
        # Classify suffix
        if word.endswith('eey') or word.endswith('eeey'):
            suffix = '-eey/-eeey'
        elif word.endswith('edy') or word.endswith('eedy'):
            suffix = '-edy/-eedy'
        elif word.endswith('ey'):
            suffix = '-ey'
        elif word.endswith('ol') or word.endswith('or'):
            suffix = '-ol/-or'
        elif word.endswith('am'):
            suffix = '-am'
        elif word.endswith('ain') or word.endswith('aiin'):
            suffix = '-ain/-aiin'
        else:
            suffix = '-?'
        print(f"  {word:<18} {pf_n:>5} {pf_rate*100:>6.1f}% {wp_n:>5} {wp_rate*100:>6.1f}% {enrich:>7.2f}× {suffix}")

    # Group by onset and suffix
    print(f"\n--- Para-Final Word Clusters by Onset+Suffix ---")
    onset_suffix_groups = defaultdict(list)
    for word, pf_n, pf_rate, wp_n, wp_rate, enrich in closing_words:
        onset = word[:2] if len(word) >= 2 else word[0]
        if word.endswith('eey') or word.endswith('eeey'):
            suffix_class = 'eey'
        elif word.endswith('edy') or word.endswith('eedy'):
            suffix_class = 'edy'
        elif word.endswith('ey'):
            suffix_class = 'ey'
        elif word.endswith('am'):
            suffix_class = 'am'
        elif word.endswith('ol') or word.endswith('or'):
            suffix_class = 'ol/or'
        else:
            suffix_class = 'other'
        onset_suffix_groups[f"{onset}...{suffix_class}"].append((word, pf_n, enrich))

    for group, words in sorted(onset_suffix_groups.items(), key=lambda x: -sum(n for _, n, _ in x[1])):
        total_n = sum(n for _, n, _ in words)
        mean_enrich = sum(e for _, _, e in words) / len(words)
        word_list = ', '.join(f"{w}({n})" for w, n, e in words[:5])
        print(f"  {group:<20} n={total_n:3d}, mean_enrich={mean_enrich:.1f}×: {word_list}")

    # Section distribution of para-final words
    print(f"\n--- Para-Final Last Words by B Section ---")
    section_pf = defaultdict(list)
    for word, section in para_final:
        section_pf[section].append(word)

    for section, words in sorted(section_pf.items()):
        top = Counter(words).most_common(8)
        top_str = ', '.join(f"{w}({n})" for w, n in top)
        print(f"  {section}: n={len(words)}, top: {top_str}")

    # Are the closing words consistent across sections?
    print(f"\n--- Key Closing Words Across B Sections ---")
    for word in ['okeey', 'orol', 'shedy', 'cheam', 'okeeey', 'okeedy', 'olol']:
        section_counts = Counter(s for w, s in para_final if w == word)
        wp_section_counts = Counter(s for w, s in within_para if w == word)
        total_pf = sum(section_counts.values())
        total_wp = sum(wp_section_counts.values())
        if total_pf > 0:
            print(f"  {word}: PF={total_pf} by section {dict(section_counts)}, WP={total_wp}")

    # All-sections test: what fraction of B para-final words are from our closing class?
    closing_set = {w for w, pf_n, pf_rate, wp_n, wp_rate, enrich in closing_words}
    pf_covered = sum(1 for w in pf_words if w in closing_set)
    print(f"\n  Closing class covers {pf_covered}/{n_pf} ({pf_covered/n_pf*100:.1f}%) of B para-final words")


def h190_astro_para_starts(paragraphs):
    """H190: Astro section anomalous para-start grammar."""
    print("\n" + "=" * 70)
    print("H190: Astro Section Para-Start Grammar (A dialect)")
    print("=" * 70)

    astro_paras = {pid: p for pid, p in paragraphs.items()
                   if p['dialect'] == 'A' and p['section'] == 'astro' and p['lines']}
    herbal_paras = {pid: p for pid, p in paragraphs.items()
                    if p['dialect'] == 'A' and p['section'] == 'herbal' and p['lines']}

    print(f"\nAstro A paragraphs: {len(astro_paras)}")
    print(f"Herbal A paragraphs: {len(herbal_paras)}")

    def analyze_ps(paras, label):
        ps_words = [p['lines'][0][0] for p in paras.values()
                    if p['lines'] and p['lines'][0]]
        print(f"\n--- {label} Para-Start Words (n={len(ps_words)}) ---")

        # Tier classification
        v2_tiers = Counter(classify_tier_v2(w) for w in ps_words)
        print("  v2 tier distribution:")
        for tier, cnt in sorted(v2_tiers.items(), key=lambda x: -x[1]):
            print(f"    {tier}: {cnt} ({cnt/len(ps_words)*100:.1f}%)")

        # Top words
        print("  Top para-start words:")
        for w, cnt in Counter(ps_words).most_common(15):
            print(f"    {w}: {cnt} (tier={classify_tier_v2(w)})")

        # Onset distribution
        onset_counter = Counter(w[0] for w in ps_words if w)
        print(f"  1-char onset distribution: {onset_counter.most_common(10)}")

    analyze_ps(astro_paras, "Astro A")
    analyze_ps(herbal_paras, "Herbal A")


def main():
    print("Loading data...")
    paragraphs = parse_voynich()
    n_a = sum(1 for p in paragraphs.values() if p['dialect'] == 'A')
    n_b = sum(1 for p in paragraphs.values() if p['dialect'] == 'B')
    print(f"Total paragraphs: {len(paragraphs)} (A={n_a}, B={n_b})")

    h188_extended_classifier(paragraphs)
    h189_b_para_final_vocabulary(paragraphs)
    h190_astro_para_starts(paragraphs)


if __name__ == '__main__':
    main()
