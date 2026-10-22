"""
exp_101: o-Onset Para-Start Analysis (H191) and Grammar vs Para Length (H192)

H191: Which specific o-onset words are para-enriched?
      The remaining classifier OTHER is 52-63% o-onset.
      Identify which o-onset words are para-starters vs within-para.

H192: Is there a correlation between paragraph length and positional grammar strictness?
      Hypothesis: longer paragraphs follow the grammar more strictly.
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


def classify_tier_v2(word):
    """Extended classifier: PARA includes bare_k, bare_t, bare_p, bare_f."""
    if (word.startswith('pch') or word.startswith('psh') or
            (word.startswith('p') and len(word) >= 3)):
        return 'PARA'
    if (word.startswith('fch') or word.startswith('fsh') or
            (word.startswith('f') and len(word) >= 3)):
        return 'PARA'
    if (word.startswith('k') and not word.startswith('kch') and
            not word.startswith('ksh') and len(word) >= 2):
        return 'PARA'
    if (word.startswith('t') and not word.startswith('tch') and
            not word.startswith('tsh') and len(word) >= 2):
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


def h191_o_onset_para_starters(paragraphs):
    """H191: Which o-onset words are para-enriched?"""
    print("=" * 70)
    print("H191: o-Onset Para-Start Word Analysis")
    print("=" * 70)

    for dialect in ['A', 'B']:
        d_paras = {pid: p for pid, p in paragraphs.items()
                   if p['dialect'] == dialect and p['lines']}
        print(f"\n{'='*50}")
        print(f"Dialect {dialect}")

        # Collect o-onset words at PS and WP positions
        ps_o_words = []
        wp_o_words = []

        # Also collect ALL first words for enrichment calculation
        ps_all = []
        wp_all = []

        for pid, para in d_paras.items():
            lines = para['lines']
            if not lines or not lines[0]:
                continue
            first_word = lines[0][0]
            ps_all.append(first_word)
            if first_word.startswith('o'):
                ps_o_words.append(first_word)

            for li in range(1, len(lines)):
                if lines[li]:
                    wp_word = lines[li][0]
                    wp_all.append(wp_word)
                    if wp_word.startswith('o'):
                        wp_o_words.append(wp_word)

        n_ps = len(ps_all)
        n_wp = len(wp_all)
        n_ps_o = len(ps_o_words)
        n_wp_o = len(wp_o_words)

        print(f"\no-onset at PS: {n_ps_o}/{n_ps} ({n_ps_o/n_ps*100:.1f}%)")
        print(f"o-onset at WP: {n_wp_o}/{n_wp} ({n_wp_o/n_wp*100:.1f}%)")
        print(f"Overall o-onset enrichment at PS: {(n_ps_o/n_ps)/(n_wp_o/n_wp):.2f}×")

        # Per-word enrichment for o-onset words
        ps_o_counter = Counter(ps_o_words)
        wp_o_counter = Counter(wp_o_words)

        print(f"\n--- o-Onset Words: PS Enrichment (PS rate / WP rate) ---")
        print(f"{'Word':<20} {'PS_n':>5} {'PS%':>7} {'WP_n':>5} {'WP%':>7} {'Enrich':>8} {'Sub-onset'}")
        word_enrichments = []
        all_o_words = set(list(ps_o_counter.keys()) + list(wp_o_counter.keys()))
        for word in all_o_words:
            ps_n = ps_o_counter.get(word, 0)
            wp_n = wp_o_counter.get(word, 0)
            ps_rate = ps_n / n_ps
            wp_rate = wp_n / n_wp if n_wp > 0 else 0
            enrich = ps_rate / wp_rate if wp_rate > 0 else float('inf')
            total = ps_n + wp_n
            if total >= 2:  # At least 2 total tokens
                word_enrichments.append((word, ps_n, ps_rate, wp_n, wp_rate, enrich))

        word_enrichments.sort(key=lambda x: -x[5])

        # Show all strongly enriched
        print("\nPara-enriched o-onset words (enrich ≥ 2×):")
        para_enriched = [(w, ps_n, ps_rate, wp_n, wp_rate, enrich)
                         for w, ps_n, ps_rate, wp_n, wp_rate, enrich in word_enrichments
                         if enrich >= 2.0 and ps_n >= 1]
        for word, ps_n, ps_rate, wp_n, wp_rate, enrich in para_enriched[:30]:
            sub = word[:2] if len(word) >= 2 else word[0]
            enr_str = f"{enrich:.1f}×" if enrich != float('inf') else "∞"
            print(f"  {word:<20} {ps_n:>5} {ps_rate*100:>6.1f}% {wp_n:>5} {wp_rate*100:>6.1f}% {enr_str:>8} {sub}")

        print("\nPara-suppressed o-onset words (enrich < 0.5×, n_wp ≥ 5):")
        para_suppressed = [(w, ps_n, ps_rate, wp_n, wp_rate, enrich)
                           for w, ps_n, ps_rate, wp_n, wp_rate, enrich in word_enrichments
                           if enrich < 0.5 and wp_n >= 5]
        for word, ps_n, ps_rate, wp_n, wp_rate, enrich in para_suppressed[:15]:
            sub = word[:2] if len(word) >= 2 else word[0]
            print(f"  {word:<20} {ps_n:>5} {ps_rate*100:>6.1f}% {wp_n:>5} {wp_rate*100:>6.1f}% {enrich:.2f}× {sub}")

        # Sub-onset analysis for o-words: ol vs ok vs ot vs or vs o+gallows
        print(f"\n--- o-Onset Sub-Class Analysis (2-char) ---")
        sub_ps = Counter(w[:2] for w in ps_o_words if len(w) >= 2)
        sub_wp = Counter(w[:2] for w in wp_o_words if len(w) >= 2)
        all_subs = set(list(sub_ps.keys()) + list(sub_wp.keys()))
        sub_enrichments = []
        for sub in all_subs:
            ps_n = sub_ps.get(sub, 0)
            wp_n = sub_wp.get(sub, 0)
            ps_rate = ps_n / n_ps
            wp_rate = wp_n / n_wp if n_wp > 0 else 0
            enrich = ps_rate / wp_rate if wp_rate > 0 else float('inf')
            total = ps_n + wp_n
            if total >= 3:
                sub_enrichments.append((sub, ps_n, ps_rate, wp_n, wp_rate, enrich))
        sub_enrichments.sort(key=lambda x: -x[5])
        print(f"{'Sub':>5} {'PS_n':>5} {'PS%':>7} {'WP_n':>5} {'WP%':>7} {'Enrich':>8}")
        for sub, ps_n, ps_rate, wp_n, wp_rate, enrich in sub_enrichments:
            enr_str = f"{enrich:.2f}×" if enrich != float('inf') else "∞"
            print(f"  {sub:>5} {ps_n:>5} {ps_rate*100:>6.1f}% {wp_n:>5} {wp_rate*100:>6.1f}% {enr_str:>8}")

        # What fraction of o-PS words are Para-enriched?
        print(f"\n--- Coverage: para-enriched o-onset words ---")
        enriched_words = {w for w, ps_n, ps_rate, wp_n, wp_rate, enrich in word_enrichments
                          if enrich >= 2.0 and ps_n >= 1}
        covered = sum(1 for w in ps_o_words if w in enriched_words)
        print(f"Para-enriched o-onset words cover {covered}/{n_ps_o} ({covered/n_ps_o*100:.1f}%) of PS o-onset tokens")

        # What specific o-onset PREFIX patterns are enriched?
        print(f"\n--- Top 3-char o-onset patterns at PS ---")
        ps_3char = Counter(w[:3] for w in ps_o_words if len(w) >= 3)
        wp_3char = Counter(w[:3] for w in wp_o_words if len(w) >= 3)
        patterns = []
        for pat in set(list(ps_3char.keys()) + list(wp_3char.keys())):
            ps_n = ps_3char.get(pat, 0)
            wp_n = wp_3char.get(pat, 0)
            ps_rate = ps_n / n_ps
            wp_rate = wp_n / n_wp if n_wp > 0 else 0
            enrich = ps_rate / wp_rate if wp_rate > 0 else float('inf')
            if ps_n >= 2:
                patterns.append((pat, ps_n, ps_rate, wp_n, wp_rate, enrich))
        patterns.sort(key=lambda x: -x[5])
        print(f"{'Pat':>5} {'PS_n':>5} {'PS%':>7} {'WP_n':>5} {'WP%':>7} {'Enrich':>8}")
        for pat, ps_n, ps_rate, wp_n, wp_rate, enrich in patterns[:15]:
            enr_str = f"{enrich:.2f}×" if enrich != float('inf') else "∞"
            print(f"  {pat:>5} {ps_n:>5} {ps_rate*100:>6.1f}% {wp_n:>5} {wp_rate*100:>6.1f}% {enr_str:>8}")


def h192_grammar_vs_para_length(paragraphs):
    """H192: Does grammatical strictness correlate with paragraph length?"""
    print("\n" + "=" * 70)
    print("H192: Positional Grammar Strength vs Paragraph Length")
    print("=" * 70)

    # Bin paragraphs by length
    length_bins = [(2, 4, 'short(2-4)'), (5, 9, 'medium(5-9)'),
                   (10, 15, 'long(10-15)'), (16, 999, 'very_long(16+)')]

    for dialect in ['A', 'B']:
        d_paras = {pid: p for pid, p in paragraphs.items()
                   if p['dialect'] == dialect and p['lines']}
        print(f"\n--- Dialect {dialect} ---")
        print(f"{'Bin':<18} {'n_paras':>8} {'PARA%':>7} {'LO%':>7} {'OTHER%':>7} {'LO_at_PS%':>10} {'PARA_enrich':>12}")

        for lo, hi, label in length_bins:
            bin_paras = {pid: p for pid, p in d_paras.items()
                         if lo <= len(p['lines']) <= hi}
            if not bin_paras:
                continue

            ps_words = [p['lines'][0][0] for p in bin_paras.values()
                        if p['lines'] and p['lines'][0]]
            wp_words = [lines[0] for p in bin_paras.values()
                        for lines in p['lines'][1:] if lines]

            n_ps = len(ps_words)
            n_wp = len(wp_words)

            if n_ps == 0:
                continue

            ps_para = sum(1 for w in ps_words if classify_tier_v2(w) == 'PARA')
            ps_lo = sum(1 for w in ps_words if classify_tier_v2(w) == 'LINE_OPEN')
            ps_other = sum(1 for w in ps_words if classify_tier_v2(w) == 'OTHER')

            wp_para = sum(1 for w in wp_words if classify_tier_v2(w) == 'PARA')
            wp_lo = sum(1 for w in wp_words if classify_tier_v2(w) == 'LINE_OPEN')

            para_ps_rate = ps_para / n_ps if n_ps > 0 else 0
            para_wp_rate = wp_para / n_wp if n_wp > 0 else 0
            enrich = para_ps_rate / para_wp_rate if para_wp_rate > 0 else float('inf')

            lo_ps_rate = ps_lo / n_ps

            print(f"  {label:<18} {len(bin_paras):>8} {para_ps_rate*100:>6.1f}% {lo_ps_rate*100:>6.1f}% {ps_other/n_ps*100:>6.1f}% {lo_ps_rate*100:>9.1f}% {enrich:>11.2f}×")

        # Section contribution to length
        print(f"\n  Length distribution by section:")
        section_lengths = defaultdict(list)
        for pid, p in d_paras.items():
            section_lengths[p['section']].append(len(p['lines']))
        for section, lengths in sorted(section_lengths.items()):
            mean_len = sum(lengths) / len(lengths)
            print(f"    {section}: n={len(lengths)}, mean={mean_len:.1f} lines")


def h191_o_onset_classifier_extension(paragraphs):
    """Build extended v3 classifier with o-onset para-starters."""
    print("\n" + "=" * 70)
    print("H191 Extension: Can We Build an o-Onset Para-Start Sub-Classifier?")
    print("=" * 70)

    # Known from exp_090: olfchedy (87.6×), olkey (58.4×), opchedy strong
    # From exp_099 OTHER: olfchedy, okar, opchedy in B OTHER list
    # From exp_100 PARA in B: olfchedy classified as PARA? No, it starts with 'ol'
    # Let me check: what 2-char o-subclasses are enriched?

    for dialect in ['A', 'B']:
        d_paras = {pid: p for pid, p in paragraphs.items()
                   if p['dialect'] == dialect and p['lines']}

        ps_words = [p['lines'][0][0] for p in d_paras.values()
                    if p['lines'] and p['lines'][0]]
        wp_words = [lines[0] for p in d_paras.values()
                    for lines in p['lines'][1:] if lines]

        n_ps = len(ps_words)
        n_wp = len(wp_words)

        # Test v3: add ol- + gallows content words as PARA-level
        # ol+f/ol+ch = olfch, olkey (ol+k), etc.
        def classify_tier_v3(word):
            """v3: add specific o-onset forms."""
            # All existing v2 rules
            tier_v2 = classify_tier_v2(word)
            if tier_v2 != 'OTHER':
                return tier_v2
            # Additional: o-prefix + known para-start sub-patterns
            # From data: ok-onset (8.77× A, 38.12× B), of-onset, olf-
            if word.startswith('olf') and len(word) >= 4:
                return 'PARA'  # olfchedy, olfchey
            if word.startswith('olke') and len(word) >= 5:
                return 'PARA'  # olkey
            if word.startswith('op') and len(word) >= 3:
                return 'PARA'  # opchedy, oparchy
            # ok-onset (o+k gallows): ko in 2-char = 38.12× B
            # but ok is k+stem form, starts with o then k
            # From data: okar=PS enriched (appears in OTHER PS B)
            # Actually from 2-char analysis: "ok" sub-class was NOT in the sub enrichment
            # Let me just test what the raw o-sub-class data says
            return 'OTHER'

        ps_tiers_v3 = [classify_tier_v3(w) for w in ps_words]
        wp_tiers_v3 = [classify_tier_v3(w) for w in wp_words]

        from collections import Counter
        ps_counter_v3 = Counter(ps_tiers_v3)
        wp_counter_v3 = Counter(wp_tiers_v3)

        para_ps = ps_counter_v3.get('PARA', 0)
        para_wp = wp_counter_v3.get('PARA', 0)
        other_ps = ps_counter_v3.get('OTHER', 0)

        para_enrich = (para_ps/n_ps) / (para_wp/n_wp) if para_wp > 0 else float('inf')
        print(f"\n  Dialect {dialect} v3 (+ olf/olke/op):")
        print(f"  PARA: PS={para_ps} ({para_ps/n_ps*100:.1f}%), WP={para_wp} ({para_wp/n_wp*100:.1f}%), enrich={para_enrich:.2f}×")
        print(f"  OTHER: PS={other_ps} ({other_ps/n_ps*100:.1f}%)")

        # What are the remaining OTHER words?
        remaining = [w for w in ps_words if classify_tier_v3(w) == 'OTHER']
        print(f"  Remaining OTHER (n={len(remaining)}): {Counter(remaining).most_common(15)}")


def main():
    print("Loading data...")
    paragraphs = parse_voynich()
    n_a = sum(1 for p in paragraphs.values() if p['dialect'] == 'A')
    n_b = sum(1 for p in paragraphs.values() if p['dialect'] == 'B')
    print(f"Total paragraphs: {len(paragraphs)} (A={n_a}, B={n_b})")

    h191_o_onset_para_starters(paragraphs)
    h191_o_onset_classifier_extension(paragraphs)
    h192_grammar_vs_para_length(paragraphs)


if __name__ == '__main__':
    main()
