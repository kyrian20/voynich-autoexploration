"""
exp_047: Quire Structure vs Section Labels for Morphological Feature Clustering
H051: Does quire membership predict morphological features better than section labels?
Computes qo-rate, -edy rate, -aiin rate per quire vs per section.
"""

import re
import math
from collections import defaultdict, Counter

DATA_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"

SUFFIXES = ['aiin', 'ain', 'eedy', 'edy', 'chy', 'eey', 'dy', 'ey', 'y',
            'ol', 'or', 'al', 'ar', 'iin', 'in']
seen = set(); SUFFIXES_DEDUP = []
for s in SUFFIXES:
    if s not in seen: seen.add(s); SUFFIXES_DEDUP.append(s)
SUFFIXES = SUFFIXES_DEDUP


def suffix_group(word):
    for sfx in SUFFIXES:
        if word.endswith(sfx) and len(word) > len(sfx):
            return sfx, word[:-len(sfx)]
    return None, word


def parse_by_quire_section(path):
    """Parse body text tokens per folio with quire and section metadata."""
    folio_data = {}
    current_folio = None
    current_quire = None
    current_section = None
    current_currier = None

    with open(path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            m_q = re.search(r'\$Q=(\w+)', line)
            if m_q: current_quire = m_q.group(1)
            m_s = re.search(r'\$I=([A-Z]+)', line)
            if m_s: current_section = m_s.group(1)
            m_c = re.search(r'\$L=([AB?])', line)
            if m_c: current_currier = m_c.group(1)

            m2 = re.match(r'^<([^>]+)>', line)
            if not m2: continue
            parts = m2.group(1).split(',')
            if len(parts) < 2: continue
            folio_m = re.match(r'^(f\d+[rv]\d*)', parts[0].strip())
            if folio_m:
                current_folio = folio_m.group(1)
                if current_folio not in folio_data:
                    folio_data[current_folio] = {
                        'quire': current_quire,
                        'section': current_section,
                        'currier': current_currier,
                        'words': []
                    }

            if current_folio is None: continue
            locus_base = parts[1].strip().lstrip('+*@=/~&')
            if not locus_base.startswith('P'): continue

            text = line[m2.end():].strip()
            text = re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]
            folio_data[current_folio]['words'].extend(tokens)

    return folio_data


def morpho_stats(words):
    """Compute qo-rate, suffix rates for key suffixes."""
    if not words:
        return {}
    n = len(words)
    qo_rate = sum(1 for w in words if w.startswith('qo')) / n
    sfx_count = Counter()
    for w in words:
        sfx, _ = suffix_group(w)
        if sfx: sfx_count[sfx] += 1
    total_sfx = sum(sfx_count.values()) or 1
    return {
        'n': n,
        'qo': qo_rate,
        'edy': sfx_count.get('edy', 0) / n,
        'ol': sfx_count.get('ol', 0) / n,
        'aiin': sfx_count.get('aiin', 0) / n,
        'ain': sfx_count.get('ain', 0) / n,
    }


def variance(values):
    """Compute variance of a list."""
    if len(values) < 2: return 0.0
    mean = sum(values) / len(values)
    return sum((v - mean)**2 for v in values) / (len(values) - 1)


def between_within_ratio(groups, feature):
    """Compute between-group vs within-group variance ratio (F-statistic analog)."""
    all_vals = []
    group_means = []
    for g_vals in groups:
        if len(g_vals) >= 2:
            vals = [v[feature] for v in g_vals if feature in v]
            if vals:
                all_vals.extend(vals)
                group_means.append(sum(vals)/len(vals))

    if not group_means or not all_vals:
        return 0.0, 0.0

    overall_mean = sum(all_vals) / len(all_vals)
    between_var = sum((gm - overall_mean)**2 for gm in group_means) / max(len(group_means)-1, 1)
    within_var_list = []
    for g_vals in groups:
        vals = [v[feature] for v in g_vals if feature in v]
        if len(vals) >= 2:
            gm = sum(vals)/len(vals)
            within_var_list.append(sum((v-gm)**2 for v in vals) / (len(vals)-1))
    within_var = sum(within_var_list) / max(len(within_var_list), 1)

    ratio = between_var / max(within_var, 1e-10)
    return between_var, within_var, ratio


if __name__ == '__main__':
    print("Loading corpus...")
    folio_data = parse_by_quire_section(DATA_PATH)

    # Aggregate per quire
    quire_stats = defaultdict(list)
    section_stats = defaultdict(list)

    for folio, data in folio_data.items():
        if len(data['words']) < 30:
            continue
        stats = morpho_stats(data['words'])
        if not stats:
            continue
        if data['quire']:
            quire_stats[data['quire']].append(stats)
        if data['section']:
            section_stats[data['section']].append(stats)

    # Quire-level summary
    print(f"\n{'='*65}")
    print(f"QUIRE-LEVEL MORPHOLOGICAL STATISTICS")
    print(f"{'Quire':<8} {'Folios':>8} {'Tokens':>8} {'qo%':>8} "
          f"{'-edy%':>8} {'-ol%':>8} {'-aiin%':>8}")
    print('-' * 60)

    quire_order = sorted(quire_stats.keys())
    for quire in quire_order:
        g_stats = quire_stats[quire]
        if not g_stats: continue
        n_folios = len(g_stats)
        total_n = sum(s['n'] for s in g_stats)
        mean_qo = sum(s['qo'] for s in g_stats) / n_folios
        mean_edy = sum(s['edy'] for s in g_stats) / n_folios
        mean_ol = sum(s['ol'] for s in g_stats) / n_folios
        mean_aiin = sum(s['aiin'] for s in g_stats) / n_folios
        print(f"  {quire:<6} {n_folios:>8} {total_n:>8} {100*mean_qo:>7.1f}% "
              f"{100*mean_edy:>7.1f}% {100*mean_ol:>7.1f}% {100*mean_aiin:>7.1f}%")

    # Section-level summary
    print(f"\n{'='*65}")
    print(f"SECTION-LEVEL MORPHOLOGICAL STATISTICS")
    print(f"{'Section':<10} {'Folios':>8} {'Tokens':>8} {'qo%':>8} "
          f"{'-edy%':>8} {'-ol%':>8} {'-aiin%':>8}")
    print('-' * 65)

    for section in sorted(section_stats.keys()):
        g_stats = section_stats[section]
        if not g_stats: continue
        n_folios = len(g_stats)
        total_n = sum(s['n'] for s in g_stats)
        mean_qo = sum(s['qo'] for s in g_stats) / n_folios
        mean_edy = sum(s['edy'] for s in g_stats) / n_folios
        mean_ol = sum(s['ol'] for s in g_stats) / n_folios
        mean_aiin = sum(s['aiin'] for s in g_stats) / n_folios
        print(f"  {section:<8} {n_folios:>8} {total_n:>8} {100*mean_qo:>7.1f}% "
              f"{100*mean_edy:>7.1f}% {100*mean_ol:>7.1f}% {100*mean_aiin:>7.1f}%")

    # Variance analysis: quire vs section
    print(f"\n{'='*65}")
    print(f"VARIANCE DECOMPOSITION: Which grouping explains more variance?")
    print(f"(Between-group variance / Within-group variance ratio)")
    print(f"Higher F-ratio → grouping explains more of the morphological variation")
    print()

    for feature in ['qo', 'edy', 'ol', 'aiin']:
        quire_groups = list(quire_stats.values())
        section_groups = list(section_stats.values())

        try:
            q_bv, q_wv, q_f = between_within_ratio(quire_groups, feature)
            s_bv, s_wv, s_f = between_within_ratio(section_groups, feature)
            winner = "QUIRE" if q_f > s_f else "SECTION"
            print(f"  Feature '{feature}': Quire F={q_f:.2f}, Section F={s_f:.2f} → {winner} explains more")
        except Exception as e:
            print(f"  Feature '{feature}': Error — {e}")

    # Quire-level variance for qo-rate
    print(f"\nQuire-level qo-rate variance (within each quire):")
    for quire in sorted(quire_stats.keys()):
        g_stats = quire_stats[quire]
        if len(g_stats) < 3: continue
        vals = [s['qo'] for s in g_stats]
        v = variance(vals)
        mean = sum(vals) / len(vals)
        std = v**0.5
        print(f"  Quire {quire}: n={len(vals)}, mean_qo={mean:.3f}, std={std:.3f}")
