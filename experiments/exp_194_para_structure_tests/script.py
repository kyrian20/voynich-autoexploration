"""
exp_194: Paragraph Structure Tests — H078, H101, H126, H165, H186, H187

H078: Bio multi-para structure — do multi-paragraph bio folios have longer/shorter
      paragraphs than single-para bio folios? Independent vocabulary per para?

H101: Line-final onset within-para vs para-final — is the onset distribution of
      the last word different for para-final lines vs within-para line-last lines?

H126: B para tripartite structure parsing — p-onset para-start → -am line-ends →
      o-onset para-end. How well does this model predict actual paragraph boundaries?

H165: d-chain pattern in A — does a d-onset line-closer predict a d+ch opener on
      the next line? Does this create multi-line d-chain runs?

H186: Stars B paragraph internal structure — do 47-line star paragraphs have
      sub-structure? Internal PARA-tier markers? N-line cycles?

H187: OTHER para-start → line-2 bigrams — do specific OTHER para-start words
      predict specific tier patterns on line 2?
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

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


def get_onset(word):
    w = word.lower()
    if w.startswith('qok'): return 'qok'
    if w.startswith('qot'): return 'qot'
    if w.startswith('qo'): return 'qo'
    if w.startswith('cth'): return 'cth'
    if w.startswith('ch'): return 'ch'
    if w.startswith('sh'): return 'sh'
    if w.startswith('ok'): return 'ok'
    if w.startswith('ot'): return 'ot'
    if w.startswith('ol'): return 'ol'
    if w.startswith('d'): return 'd'
    if w.startswith('s'): return 's'
    if w.startswith('y'): return 'y'
    if w.startswith('k'): return 'k'
    if w.startswith('t'): return 't'
    if w.startswith('l'): return 'l'
    if w.startswith('r'): return 'r'
    if w.startswith('p'): return 'p'
    if w.startswith('f'): return 'f'
    if w.startswith('o'): return 'o'
    return 'other'


def classify_positional_tier(word):
    """Assign morphological tier based on word onset (v2 classifier)."""
    # PARA tier: gallows initial (p/f/k/t)
    if word.startswith('p') and len(word) >= 2:
        return 'PARA'
    if word.startswith('f') and len(word) >= 2:
        return 'PARA'
    if word.startswith('k') and len(word) >= 2:
        return 'PARA'
    if word.startswith('t') and len(word) >= 2:
        return 'PARA'
    # LINE_OPEN tier
    if (word.startswith('ych') or word.startswith('dch') or
            word.startswith('ysh') or word.startswith('dsh') or
            word.startswith('yk') or word.startswith('yt')) and len(word) >= 3:
        return 'LINE_OPEN'
    # MID tier
    if (word.startswith('ch') or word.startswith('sh') or
            word.startswith('qo')) and len(word) >= 3:
        return 'MID'
    return 'OTHER'


def parse_voynich():
    """Parse ZL3b into paragraph records with dialect and section."""
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

    return paragraphs, folio_dialect


def h078_bio_multi_para(paragraphs):
    """H078: Bio multi-paragraph structure."""
    print("=" * 70)
    print("H078: Bio Multi-Paragraph Structure")
    print("=" * 70)

    # Group paragraphs by folio
    folio_paras = defaultdict(list)
    for pid, p in paragraphs.items():
        if p['section'] == 'cosmo' and 75 <= int(re.search(r'f(\d+)', p['folio']).group(1)) <= 84:
            folio_paras[p['folio']].append(p)

    # Actually, bio section = f75-f84 in ZL3b
    folio_paras_bio = defaultdict(list)
    for pid, p in paragraphs.items():
        m = re.search(r'f(\d+)', p['folio'])
        if m and 75 <= int(m.group(1)) <= 84:
            folio_paras_bio[p['folio']].append(p)

    print(f"\nBio folios with paragraphs: {sorted(folio_paras_bio.keys())}")

    single_para_folios = {fb: ps for fb, ps in folio_paras_bio.items() if len(ps) == 1}
    multi_para_folios = {fb: ps for fb, ps in folio_paras_bio.items() if len(ps) >= 2}

    print(f"\nSingle-para bio folios (n={len(single_para_folios)}): {sorted(single_para_folios.keys())}")
    print(f"Multi-para bio folios (n={len(multi_para_folios)}): {sorted(multi_para_folios.keys())}")

    # Paragraph lengths
    single_lengths = [len(p['lines']) for ps in single_para_folios.values() for p in ps]
    multi_lengths = [len(p['lines']) for ps in multi_para_folios.values() for p in ps]

    if single_lengths:
        print(f"\nSingle-para folio paragraph lengths: mean={sum(single_lengths)/len(single_lengths):.1f}, "
              f"total={sum(single_lengths)}, n_paras={len(single_lengths)}")
    if multi_lengths:
        print(f"Multi-para folio paragraph lengths: mean={sum(multi_lengths)/len(multi_lengths):.1f}, "
              f"total={sum(multi_lengths)}, n_paras={len(multi_lengths)}")

    # Detailed breakdown
    print("\nMulti-para bio folios:")
    for fb, ps in sorted(multi_para_folios.items()):
        lengths = [len(p['lines']) for p in ps]
        print(f"  {fb}: {len(ps)} paragraphs, lengths={lengths}, total_lines={sum(lengths)}")

    # Vocabulary overlap between paragraphs within same multi-para folio
    print("\nVocabulary overlap between paragraphs in same bio folio:")
    for fb, ps in sorted(multi_para_folios.items()):
        if len(ps) < 2:
            continue
        para_vocabs = [set(w for line in p['lines'] for w in line) for p in ps]
        if len(para_vocabs) >= 2:
            # Pairwise Jaccard
            jaccards = []
            for i in range(len(para_vocabs)):
                for j in range(i+1, len(para_vocabs)):
                    inter = len(para_vocabs[i] & para_vocabs[j])
                    union = len(para_vocabs[i] | para_vocabs[j])
                    jaccards.append(inter/union if union else 0)
            print(f"  {fb}: mean pairwise Jaccard={sum(jaccards)/len(jaccards):.3f} (n_pairs={len(jaccards)})")


def h101_line_final_onset_para_vs_within(paragraphs):
    """H101: Line-final onset within-para vs para-final."""
    print("\n" + "=" * 70)
    print("H101: Line-Final Onset — Para-Final vs Within-Para")
    print("=" * 70)

    for dialect in ['A', 'B']:
        d_paras = {pid: p for pid, p in paragraphs.items()
                   if p['dialect'] == dialect and len(p['lines']) >= 2}

        para_final_onsets = []   # last word of last line in paragraph
        within_para_onsets = []  # last word of non-last lines in paragraph

        for pid, p in d_paras.items():
            lines = p['lines']
            for i, line in enumerate(lines):
                if not line:
                    continue
                last_word = line[-1]
                onset = get_onset(last_word)
                if i == len(lines) - 1:
                    para_final_onsets.append(onset)
                else:
                    within_para_onsets.append(onset)

        total_pf = len(para_final_onsets)
        total_wp = len(within_para_onsets)

        print(f"\nDialect {dialect} — para-final n={total_pf}, within-para n={total_wp}")

        all_onsets = ['o', 'd', 'ch', 'sh', 'qo', 'qok', 'qot', 'y', 's', 'p', 'k', 't', 'cth', 'l', 'ol', 'ot', 'ok']
        print(f"{'Onset':<8} {'PF%':>7} {'WP%':>7} {'Enrich':>8}")
        print("-" * 35)
        for onset in all_onsets:
            pf_n = para_final_onsets.count(onset)
            wp_n = within_para_onsets.count(onset)
            pf_rate = pf_n / total_pf if total_pf else 0
            wp_rate = wp_n / total_wp if total_wp else 0
            enrich = pf_rate / wp_rate if wp_rate > 0.001 else float('inf')
            if pf_n >= 2 or wp_n >= 5:
                print(f"{onset:<8} {pf_rate:>7.1%} {wp_rate:>7.1%} {enrich:>8.2f}×  (pf_n={pf_n})")


def h126_b_tripartite_parser(paragraphs):
    """H126: B para tripartite structure parsing."""
    print("\n" + "=" * 70)
    print("H126: B Para Tripartite Structure — Parsing Test")
    print("=" * 70)

    b_paras = {pid: p for pid, p in paragraphs.items()
               if p['dialect'] == 'B' and len(p['lines']) >= 3}

    print(f"B paragraphs with ≥3 lines: {len(b_paras)}")

    # Rule 1: para-start line = has p/k/t/f onset opener (PARA tier)
    # Rule 2: within-para continuation = last word ends in -am
    # Rule 3: para-final = last word is o-onset

    # Measure rates of each signal
    ps_para_tier = []    # does PS line have PARA-tier opener?
    wp_am_rate = []      # does within-para line end in -am?
    pf_o_rate = []       # does para-final line end in o-onset?

    for pid, p in b_paras.items():
        lines = p['lines']
        n = len(lines)

        # Para-start line opener
        if lines[0]:
            tier = classify_positional_tier(lines[0][0])
            ps_para_tier.append(tier == 'PARA')

        # Within-para line endings (-am suffix)
        for i in range(1, n-1):
            if lines[i]:
                last_w = lines[i][-1]
                wp_am_rate.append(last_w.endswith('am'))

        # Para-final line last word
        if lines[-1]:
            last_w = lines[-1][-1]
            pf_o_rate.append(get_onset(last_w) == 'o')

    print(f"\nPS line has PARA-tier opener: {sum(ps_para_tier)}/{len(ps_para_tier)} = {sum(ps_para_tier)/len(ps_para_tier):.1%}")
    print(f"Within-para line ends in -am: {sum(wp_am_rate)}/{len(wp_am_rate)} = {sum(wp_am_rate)/len(wp_am_rate):.1%}")
    print(f"Para-final line ends in o-onset: {sum(pf_o_rate)}/{len(pf_o_rate)} = {sum(pf_o_rate)/len(pf_o_rate):.1%}")

    # Classifier: predict next-line is para-boundary from current-line features
    # Signal: does o-onset at line-end predict NEXT line is PS?
    # Collect (current_line_last_onset, is_next_line_para_start)
    print("\nPrecision of para-final signals as para-boundary predictors:")

    o_final_total = 0
    o_final_correct = 0
    am_final_total = 0
    am_final_correct = 0

    for pid, p in b_paras.items():
        lines = p['lines']
        n = len(lines)

        for i in range(n - 1):
            if not lines[i]:
                continue
            last_w = lines[i][-1]
            # Does this being the last line of paragraph signal correctly?
            # (We know it IS the last if i == n-1)
            # Instead, let's just measure: conditional on o-final, is next line a different para?
            # We can't do inter-paragraph since we only have intra-para...
            # Let's measure: at para boundaries, what's the last word onset of the final line?
            pass

    # Instead: measure how often para-final line (last line of para) ends with o-onset
    # vs non-para-final line
    print("(See H101 for para-final vs within-para onset rates — same data)")

    # Tripartite completeness: fraction of paragraphs with ALL three signals
    complete = 0
    for pid, p in b_paras.items():
        lines = p['lines']
        n = len(lines)
        has_para_open = classify_positional_tier(lines[0][0]) == 'PARA' if lines[0] else False
        has_am = any(lines[i][-1].endswith('am') for i in range(1, n-1) if lines[i]) if n >= 3 else False
        has_o_close = get_onset(lines[-1][-1]) == 'o' if lines[-1] else False
        if has_para_open and has_am and has_o_close:
            complete += 1

    print(f"Paragraphs with all 3 tripartite signals: {complete}/{len(b_paras)} = {complete/len(b_paras):.1%}")

    # By section
    print("\nParas by section:")
    sec_counts = Counter(p['section'] for p in b_paras.values())
    for sec, n in sorted(sec_counts.items()):
        print(f"  {sec}: {n}")


def h165_d_chain_pattern(paragraphs):
    """H165: d-chain pattern in A — d-closer → d+ch opener on next line."""
    print("\n" + "=" * 70)
    print("H165: d-Chain Pattern in A Dialect")
    print("=" * 70)

    # Collect consecutive line pairs within A paragraphs
    a_paras = {pid: p for pid, p in paragraphs.items()
               if p['dialect'] == 'A' and len(p['lines']) >= 2}

    # Consecutive line pairs: (prev_line_last_onset, next_line_first_onset)
    pairs = []
    for pid, p in a_paras.items():
        lines = p['lines']
        for i in range(len(lines) - 1):
            if not lines[i] or not lines[i+1]:
                continue
            prev_last = get_onset(lines[i][-1])
            next_first = lines[i+1][0]
            next_first_onset = get_onset(next_first)
            # Is next line opener a d+ch compound?
            is_dch_opener = next_first.startswith('dch') and len(next_first) >= 4
            is_ych_opener = next_first.startswith('ych') and len(next_first) >= 4
            pairs.append({
                'prev_last_onset': prev_last,
                'next_first_onset': next_first_onset,
                'is_dch_opener': is_dch_opener,
                'is_ych_opener': is_ych_opener,
                'next_first_word': next_first,
            })

    total_pairs = len(pairs)
    print(f"\nTotal consecutive line pairs in A paragraphs: {total_pairs}")

    # Base rates
    base_dch = sum(1 for p in pairs if p['is_dch_opener']) / total_pairs
    base_ych = sum(1 for p in pairs if p['is_ych_opener']) / total_pairs
    print(f"Base rate d+ch opener: {base_dch:.3f} ({sum(1 for p in pairs if p['is_dch_opener'])}/{total_pairs})")
    print(f"Base rate y+ch opener: {base_ych:.3f} ({sum(1 for p in pairs if p['is_ych_opener'])}/{total_pairs})")

    # Conditional on prev line ending in d-onset
    d_final_pairs = [p for p in pairs if p['prev_last_onset'] == 'd']
    non_d_final_pairs = [p for p in pairs if p['prev_last_onset'] != 'd']

    if d_final_pairs:
        dch_after_d = sum(1 for p in d_final_pairs if p['is_dch_opener']) / len(d_final_pairs)
        ych_after_d = sum(1 for p in d_final_pairs if p['is_ych_opener']) / len(d_final_pairs)
        print(f"\nAfter d-final line (n={len(d_final_pairs)}):")
        print(f"  d+ch opener: {dch_after_d:.3f} (enrich={dch_after_d/base_dch:.2f}×)")
        print(f"  y+ch opener: {ych_after_d:.3f} (enrich={ych_after_d/base_ych:.2f}×)")

    if non_d_final_pairs:
        dch_after_nond = sum(1 for p in non_d_final_pairs if p['is_dch_opener']) / len(non_d_final_pairs)
        print(f"\nAfter non-d-final line (n={len(non_d_final_pairs)}):")
        print(f"  d+ch opener: {dch_after_nond:.3f}")

    # Look for d-chain runs (d-closer → d+ch opener → d-closer → ...)
    print("\nLooking for multi-line d-chains:")
    chain_counts = Counter()
    for pid, p in a_paras.items():
        lines = p['lines']
        chain_len = 1
        for i in range(len(lines)):
            if not lines[i]:
                continue
            last_word = lines[i][-1]
            is_d_closer = get_onset(last_word) == 'd'
            if is_d_closer:
                chain_len += 1
            else:
                if chain_len >= 2:
                    chain_counts[chain_len] += 1
                chain_len = 1
    for ln, cnt in sorted(chain_counts.items()):
        print(f"  d-closer run of length {ln}: {cnt} cases")

    # Complementary o-chain: o-final → y+ch opener → o-final?
    o_final_pairs = [p for p in pairs if p['prev_last_onset'] == 'o']
    if o_final_pairs:
        ych_after_o = sum(1 for p in o_final_pairs if p['is_ych_opener']) / len(o_final_pairs)
        dch_after_o = sum(1 for p in o_final_pairs if p['is_dch_opener']) / len(o_final_pairs)
        print(f"\nAfter o-final line (n={len(o_final_pairs)}):")
        print(f"  y+ch opener: {ych_after_o:.3f} (enrich={ych_after_o/base_ych:.2f}×)")
        print(f"  d+ch opener: {dch_after_o:.3f} (enrich={dch_after_o/base_dch:.2f}×)")


def h186_stars_internal_structure(paragraphs):
    """H186: Stars B paragraph internal structure."""
    print("\n" + "=" * 70)
    print("H186: Stars B Paragraph Internal Structure")
    print("=" * 70)

    stars_paras = {pid: p for pid, p in paragraphs.items()
                   if p['section'] == 'stars' and p['dialect'] == 'B'}

    print(f"Stars B paragraphs: {len(stars_paras)}")
    lengths = [len(p['lines']) for p in stars_paras.values()]
    if lengths:
        print(f"Paragraph lengths: mean={sum(lengths)/len(lengths):.1f}, "
              f"min={min(lengths)}, max={max(lengths)}, "
              f"range={sorted(lengths)}")

    # Check for PARA-tier markers appearing mid-paragraph
    print("\nPARA-tier opener appearances at non-PS positions:")
    for pid, p in sorted(stars_paras.items()):
        lines = p['lines']
        n = len(lines)
        para_mid = []
        for i in range(1, n):  # skip first line (para-start)
            if lines[i] and classify_positional_tier(lines[i][0]) == 'PARA':
                para_mid.append((i, lines[i][0]))
        if para_mid:
            print(f"  Para {pid} (folio {p['folio']}, {n} lines): PARA at lines {para_mid}")

    # Check for N-line cycles (look at first-word onset pattern)
    print("\nLine-opener onset patterns in stars paragraphs (first 5 para):")
    for pid, p in list(sorted(stars_paras.items()))[:5]:
        lines = p['lines']
        pattern = [get_onset(line[0]) if line else '?' for line in lines[:20]]
        print(f"  Para {pid} ({len(lines)} lines): {pattern}")

    # Compute PARA-tier fraction by line position within paragraph
    max_line = 60
    line_para_counts = [0] * max_line
    line_totals = [0] * max_line

    for pid, p in stars_paras.items():
        lines = p['lines']
        for i, line in enumerate(lines):
            if i >= max_line:
                break
            if line:
                line_totals[i] += 1
                if classify_positional_tier(line[0]) == 'PARA':
                    line_para_counts[i] += 1

    print("\nPARA-tier rate by line position within stars paragraphs (positions 0-20):")
    for i in range(min(21, max_line)):
        if line_totals[i] > 0:
            rate = line_para_counts[i] / line_totals[i]
            bar = '█' * int(rate * 20)
            print(f"  Line {i:2d} (n={line_totals[i]:3d}): {rate:.2f} {bar}")

    # Check if ~47 = some structure
    print(f"\nAstronomical number check for stars para lengths:")
    for ln in sorted(set(lengths)):
        n_paras = lengths.count(ln)
        print(f"  {ln} lines: {n_paras} paragraph(s) — {ln}/12={ln/12:.1f}, {ln}/36={ln/36:.2f}")


def h187_other_ps_line2_bigrams(paragraphs):
    """H187: OTHER para-start words → line-2 bigrams."""
    print("\n" + "=" * 70)
    print("H187: OTHER Para-Start → Line-2 Bigrams")
    print("=" * 70)

    for dialect in ['A', 'B']:
        d_paras = {pid: p for pid, p in paragraphs.items()
                   if p['dialect'] == dialect and len(p['lines']) >= 2}

        print(f"\nDialect {dialect} — {len(d_paras)} paragraphs with ≥2 lines")

        # Collect: PS_tier → line2_tier transitions
        transitions = []
        for pid, p in d_paras.items():
            lines = p['lines']
            if not lines[0] or not lines[1]:
                continue
            ps_tier = classify_positional_tier(lines[0][0])
            line2_tier = classify_positional_tier(lines[1][0])
            transitions.append((ps_tier, line2_tier))

        # Overall PS → line2 transition matrix
        total = len(transitions)
        ps_tiers = ['PARA', 'LINE_OPEN', 'MID', 'OTHER']
        line2_tiers = ['PARA', 'LINE_OPEN', 'MID', 'OTHER']

        print(f"PS-tier → Line2-tier transition rates (n={total}):")
        print(f"{'PS\\L2':<12}" + "".join(f"{t:<10}" for t in line2_tiers))
        for ps in ps_tiers:
            ps_subset = [t for s, t in transitions if s == ps]
            n_ps = len(ps_subset)
            if n_ps == 0:
                continue
            row = f"{ps:<12}"
            for l2 in line2_tiers:
                rate = ps_subset.count(l2) / n_ps
                row += f"{rate:.2f}      "
            row += f"(n={n_ps})"
            print(row)

        # For OTHER PS words specifically: which specific words predict what line-2 tier?
        other_ps_words = []
        for pid, p in d_paras.items():
            lines = p['lines']
            if not lines[0] or not lines[1]:
                continue
            ps_word = lines[0][0]
            ps_tier = classify_positional_tier(ps_word)
            if ps_tier == 'OTHER':
                line2_tier = classify_positional_tier(lines[1][0])
                other_ps_words.append((ps_word, line2_tier, get_onset(ps_word)))

        print(f"\nOTHER PS words by onset: total={len(other_ps_words)}")
        onset_groups = defaultdict(list)
        for word, l2, onset in other_ps_words:
            onset_groups[onset].append(l2)

        for onset in sorted(onset_groups.keys(), key=lambda x: -len(onset_groups[x])):
            g = onset_groups[onset]
            n = len(g)
            line_open_rate = g.count('LINE_OPEN') / n
            para_rate = g.count('PARA') / n
            print(f"  {onset}-onset (n={n}): LINE_OPEN_rate={line_open_rate:.2f}, PARA_rate={para_rate:.2f}")


def main():
    print("Loading corpus...")
    paragraphs, folio_dialect = parse_voynich()

    total_paras = len(paragraphs)
    a_paras = sum(1 for p in paragraphs.values() if p['dialect'] == 'A')
    b_paras = sum(1 for p in paragraphs.values() if p['dialect'] == 'B')
    print(f"Total paragraphs: {total_paras} (A={a_paras}, B={b_paras})")

    h078_bio_multi_para(paragraphs)
    h101_line_final_onset_para_vs_within(paragraphs)
    h126_b_tripartite_parser(paragraphs)
    h165_d_chain_pattern(paragraphs)
    h186_stars_internal_structure(paragraphs)
    h187_other_ps_line2_bigrams(paragraphs)


if __name__ == '__main__':
    main()
