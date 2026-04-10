#!/usr/bin/env python3
"""
exp_133: Cosmo vs Stars Differentiation (H261) + Astro Section Characterization (H260)

H261: What onset classes, suffixes, and positional patterns distinguish cosmo from stars?
H260: Why is astro the least cohesive section and why does f87 (pharma) best-match astro?
"""

import re
import math
from collections import defaultdict, Counter

CORPUS_PATH = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

ONSET_CLASSES = [
    'qok', 'qot', 'qo',
    'cth', 'ch', 'sh',
    'ok', 'ot', 'ol',
    'd', 's', 'y', 'k', 't', 'l', 'r', 'p', 'f',
    'other'
]

SUFFIX_LIST = ['eeedy', 'eeey', 'eedy', 'edy', 'eey', 'aiin', 'ain', 'air',
               'am', 'ol', 'or', 'ar', 'al', 'ey', 'dy', 'y']

def folio_to_section(f):
    if 1 <= f <= 57:    return 'herbal'
    elif 67 <= f <= 73: return 'astro'
    elif 75 <= f <= 84: return 'cosmo'
    elif 87 <= f <= 102: return 'pharma'
    elif 103 <= f <= 116: return 'stars'
    return None

def get_onset(word):
    w = word.lower()
    for cls in ONSET_CLASSES[:-1]:
        if w.startswith(cls):
            return cls
    return 'other'

def get_suffix(word):
    w = word.lower()
    for s in SUFFIX_LIST:
        if w.endswith(s) and len(w) > len(s):
            return s
    return 'other'

def parse_corpus(path):
    records = []
    folio_word_counts = defaultdict(lambda: defaultdict(int))

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^>]+)>(.*)', line)
            if not m:
                continue
            locus_code, text_raw = m.group(1), m.group(2)
            parts = locus_code.split(',')
            if len(parts) < 2:
                continue
            locus_type_raw = parts[1]
            locus_type = locus_type_raw.lstrip('@+*=~&')
            if not re.match(r'P', locus_type):
                continue

            folio_str = parts[0]
            fm = re.search(r'(\d+)', folio_str)
            if not fm:
                continue
            folio_num = int(fm.group(1))
            section = folio_to_section(folio_num)
            if not section:
                continue

            text = re.sub(r'<[^>]*>', '', text_raw)
            text = re.sub(r'\[[^\]]*\]', ' ', text)
            text = re.sub(r'[*@&~=+$#{}?!]', '', text)
            text = text.replace('-', ' ').replace('.', ' ').replace(',', ' ')
            words = [w for w in text.lower().split() if re.match(r'^[a-z]{2,}$', w)]
            if not words:
                continue

            for w in words:
                folio_word_counts[folio_num][w] += 1

            records.append({
                'folio': folio_num,
                'section': section,
                'words': words,
            })

    # Dialect assignment
    folio_dialect = {}
    for folio, wc in folio_word_counts.items():
        total = sum(wc.values())
        edy = sum(v for w, v in wc.items() if w.endswith('edy') or w.endswith('eedy'))
        folio_dialect[folio] = 'B' if total > 0 and edy / total >= 0.05 else 'A'

    for r in records:
        r['dialect'] = folio_dialect.get(r['folio'], 'A')

    return records, folio_dialect


def section_onset_profile(records, target_section):
    """Return onset-class frequency dict for a section."""
    words = [w for r in records if r['section'] == target_section for w in r['words']]
    total = len(words)
    counts = Counter(get_onset(w) for w in words)
    return {cls: counts.get(cls, 0) / total for cls in ONSET_CLASSES}, total


def section_suffix_profile(records, target_section):
    """Return suffix frequency dict for a section."""
    words = [w for r in records if r['section'] == target_section for w in r['words']]
    total = len(words)
    counts = Counter(get_suffix(w) for w in words)
    return {s: counts.get(s, 0) / total for s in SUFFIX_LIST + ['other']}, total


def compute_vocab(records, section):
    wc = Counter()
    for r in records:
        if r['section'] == section:
            for w in r['words']:
                wc[w] += 1
    return wc


def jaccard(set1, set2):
    inter = len(set1 & set2)
    union = len(set1 | set2)
    return inter / union if union > 0 else 0.0


def analyze_cosmo_vs_stars(records):
    """H261: Differentiate cosmo and stars sections."""
    print("=" * 70)
    print("H261: COSMO vs STARS SECTION DIFFERENTIATION")
    print("=" * 70)

    cosmo_records = [r for r in records if r['section'] == 'cosmo']
    stars_records = [r for r in records if r['section'] == 'stars']

    # Corpus baseline
    all_words = [w for r in records for w in r['words']]
    total_all = len(all_words)
    corpus_onset = Counter(get_onset(w) for w in all_words)
    corpus_onset_frac = {cls: corpus_onset[cls] / total_all for cls in ONSET_CLASSES}

    cosmo_profile, cosmo_total = section_onset_profile(records, 'cosmo')
    stars_profile, stars_total = section_onset_profile(records, 'stars')

    print(f"\nCorpus totals: cosmo={cosmo_total} words ({len(cosmo_records)} lines), stars={stars_total} words ({len(stars_records)} lines)")
    print(f"Cosmo folios (f75-f84): n=10; Stars folios (f103-f116): n=12")

    # Onset-class comparison
    print("\n### Onset-Class Profile: Cosmo vs Stars (with corpus baseline)")
    print(f"{'Class':<8} {'Cosmo':>8} {'Stars':>8} {'Corpus':>8} {'C/S ratio':>10} {'C/base':>10} {'S/base':>10}")
    cosmo_stars_diff = []
    for cls in ONSET_CLASSES:
        c = cosmo_profile[cls]
        s = stars_profile[cls]
        b = corpus_onset_frac[cls]
        ratio = c / s if s > 0 else float('inf')
        c_enrich = c / b if b > 0 else 0
        s_enrich = s / b if b > 0 else 0
        cosmo_stars_diff.append((cls, c, s, b, ratio, c_enrich, s_enrich))
        print(f"{cls:<8} {c:>7.4f}  {s:>7.4f}  {b:>7.4f}  {ratio:>9.2f}×  {c_enrich:>9.2f}×  {s_enrich:>9.2f}×")

    # Most cosmo-enriched vs stars
    print("\n### Most Cosmo-Enriched Onset Classes (cosmo/stars ratio > 1.2×)")
    for cls, c, s, b, ratio, c_enrich, s_enrich in sorted(cosmo_stars_diff, key=lambda x: -x[4]):
        if ratio > 1.2 and c > 0.005:
            print(f"  {cls:<8} cosmo={c:.4f} stars={s:.4f} ratio={ratio:.2f}×  (cosmo/base={c_enrich:.2f}×, stars/base={s_enrich:.2f}×)")

    print("\n### Most Stars-Enriched Onset Classes (stars/cosmo ratio > 1.2×)")
    for cls, c, s, b, ratio, c_enrich, s_enrich in sorted(cosmo_stars_diff, key=lambda x: x[4]):
        if ratio < 0.83 and s > 0.005:
            print(f"  {cls:<8} cosmo={c:.4f} stars={s:.4f} ratio={ratio:.2f}× (stars/cosmo={1/ratio:.2f}×)  (cosmo/base={c_enrich:.2f}×, stars/base={s_enrich:.2f}×)")

    # Suffix profile comparison
    cosmo_suf, _ = section_suffix_profile(records, 'cosmo')
    stars_suf, _ = section_suffix_profile(records, 'stars')

    print("\n### Suffix Profile: Cosmo vs Stars")
    print(f"{'Suffix':<10} {'Cosmo':>8} {'Stars':>8} {'C/S ratio':>10}")
    for s in SUFFIX_LIST + ['other']:
        c = cosmo_suf.get(s, 0)
        st = stars_suf.get(s, 0)
        ratio = c / st if st > 0 else float('inf')
        if abs(c - st) > 0.003 or s in ['eedy', 'edy', 'eey', 'aiin']:
            print(f"{s:<10} {c:>7.4f}  {st:>7.4f}  {ratio:>9.2f}×")

    # Vocabulary overlap between cosmo and stars
    cosmo_vocab = compute_vocab(records, 'cosmo')
    stars_vocab = compute_vocab(records, 'stars')
    herbal_vocab = compute_vocab(records, 'herbal')
    pharma_vocab = compute_vocab(records, 'pharma')

    cosmo_types = set(cosmo_vocab.keys())
    stars_types = set(stars_vocab.keys())

    j_cs = jaccard(cosmo_types, stars_types)
    print(f"\n### Vocabulary Jaccard Similarities (type-level)")
    print(f"  Cosmo vs Stars: {j_cs:.3f}")
    print(f"  Cosmo vs Herbal: {jaccard(cosmo_types, set(herbal_vocab.keys())):.3f}")
    print(f"  Cosmo vs Pharma: {jaccard(cosmo_types, set(pharma_vocab.keys())):.3f}")
    print(f"  Stars vs Herbal: {jaccard(stars_types, set(herbal_vocab.keys())):.3f}")
    print(f"  Stars vs Pharma: {jaccard(stars_types, set(pharma_vocab.keys())):.3f}")

    # Cosmo-exclusive and stars-exclusive top words
    cosmo_only = {w: cosmo_vocab[w] for w in cosmo_vocab if w not in stars_vocab}
    stars_only = {w: stars_vocab[w] for w in stars_vocab if w not in cosmo_vocab}
    shared = {w: (cosmo_vocab[w], stars_vocab[w]) for w in cosmo_vocab if w in stars_vocab}

    print(f"\n### Vocabulary Exclusivity")
    print(f"  Cosmo-exclusive types: {len(cosmo_only)} ({100*len(cosmo_only)/len(cosmo_types):.1f}%)")
    print(f"  Stars-exclusive types: {len(stars_only)} ({100*len(stars_only)/len(stars_types):.1f}%)")
    print(f"  Shared types: {len(shared)}")
    print(f"\nTop cosmo-exclusive words (by frequency):")
    for w, n in sorted(cosmo_only.items(), key=lambda x: -x[1])[:15]:
        print(f"  {w:<16} n={n:>4}  onset={get_onset(w):<8} suffix={get_suffix(w)}")
    print(f"\nTop stars-exclusive words (by frequency):")
    for w, n in sorted(stars_only.items(), key=lambda x: -x[1])[:15]:
        print(f"  {w:<16} n={n:>4}  onset={get_onset(w):<8} suffix={get_suffix(w)}")

    # Per-folio onset profiles for cosmo
    print("\n### Per-Folio Onset Profile: Cosmo Folios (f75-f84)")
    cosmo_folio_words = defaultdict(list)
    for r in records:
        if r['section'] == 'cosmo':
            cosmo_folio_words[r['folio']].extend(r['words'])
    key_classes = ['s', 'd', 'sh', 'ch', 'ok', 'qok', 'ot', 'ol', 'other']
    header = f"{'Folio':<7} {'n':>5} " + " ".join(f"{c:<6}" for c in key_classes)
    print(header)
    for f in sorted(cosmo_folio_words.keys()):
        ws = cosmo_folio_words[f]
        profile = Counter(get_onset(w) for w in ws)
        total = len(ws)
        row = f"f{f:<6} {total:>5} " + " ".join(f"{profile.get(c,0)/total:.3f} " for c in key_classes)
        print(row)

    # Per-folio onset profiles for stars
    print("\n### Per-Folio Onset Profile: Stars Folios (f103-f116)")
    stars_folio_words = defaultdict(list)
    for r in records:
        if r['section'] == 'stars':
            stars_folio_words[r['folio']].extend(r['words'])
    print(header)
    for f in sorted(stars_folio_words.keys()):
        ws = stars_folio_words[f]
        profile = Counter(get_onset(w) for w in ws)
        total = len(ws)
        row = f"f{f:<6} {total:>5} " + " ".join(f"{profile.get(c,0)/total:.3f} " for c in key_classes)
        print(row)

    # Positional comparison
    print("\n### Line-Positional Grammar: Cosmo vs Stars")
    for section_name, section_recs in [('cosmo', cosmo_records), ('stars', stars_records)]:
        lf_counts = Counter()
        ll_counts = Counter()
        mid_counts = Counter()
        total_lf = total_ll = total_mid = 0
        for r in section_recs:
            ws = r['words']
            n = len(ws)
            for i, w in enumerate(ws):
                onset = get_onset(w)
                if i == 0:
                    lf_counts[onset] += 1
                    total_lf += 1
                elif i == n - 1:
                    ll_counts[onset] += 1
                    total_ll += 1
                else:
                    mid_counts[onset] += 1
                    total_mid += 1
        print(f"\n{section_name.upper()} line-first top onset classes:")
        for cls, n in lf_counts.most_common(8):
            print(f"  {cls:<8} {n:>5} ({100*n/total_lf:.1f}%)")
        print(f"{section_name.upper()} line-last suffix analysis:")
        ll_suffixes = Counter()
        for r in section_recs:
            ws = r['words']
            if ws:
                ll_suffixes[get_suffix(ws[-1])] += 1
        for s, n in ll_suffixes.most_common(8):
            print(f"  {s:<10} {n:>5} ({100*n/total_ll:.1f}%)")


def analyze_astro_section(records, folio_dialect):
    """H260: Characterize the astro section."""
    print("\n\n" + "=" * 70)
    print("H260: ASTRO SECTION CHARACTERIZATION")
    print("=" * 70)

    astro_records = [r for r in records if r['section'] == 'astro']
    astro_folios = sorted(set(r['folio'] for r in astro_records))

    print(f"\nAstro folios: {astro_folios}")
    print(f"Total astro lines: {len(astro_records)}")
    total_astro = sum(len(r['words']) for r in astro_records)
    print(f"Total astro words: {total_astro}")
    print(f"Astro dialect distribution:")
    for f in astro_folios:
        d = folio_dialect.get(f, '?')
        n = sum(len(r['words']) for r in astro_records if r['folio'] == f)
        print(f"  f{f}: dialect={d}, words={n}")

    # Build onset profiles for each astro folio
    astro_folio_words = defaultdict(list)
    for r in astro_records:
        astro_folio_words[r['folio']].extend(r['words'])

    # Section centroids for comparison
    section_profiles = {}
    for sec in ['herbal', 'pharma', 'stars', 'cosmo', 'astro']:
        words = [w for r in records if r['section'] == sec for w in r['words']]
        if words:
            total = len(words)
            counts = Counter(get_onset(w) for w in words)
            section_profiles[sec] = {cls: counts.get(cls, 0) / total for cls in ONSET_CLASSES}

    def cosine_sim(v1, v2):
        dot = sum(v1.get(k, 0) * v2.get(k, 0) for k in ONSET_CLASSES)
        n1 = math.sqrt(sum(v ** 2 for v in v1.values()))
        n2 = math.sqrt(sum(v ** 2 for v in v2.values()))
        if n1 == 0 or n2 == 0:
            return 0.0
        return dot / (n1 * n2)

    # Cosine similarity for each astro folio to all sections
    print("\n### Per-Folio Cosine Similarity to Section Centroids")
    secs = ['herbal', 'pharma', 'stars', 'cosmo', 'astro']
    header = f"{'Folio':<8} {'n':>5} " + " ".join(f"{s:<8}" for s in secs) + " Best"
    print(header)
    for f in astro_folios:
        ws = astro_folio_words[f]
        total = len(ws)
        if total == 0:
            continue
        counts = Counter(get_onset(w) for w in ws)
        profile = {cls: counts.get(cls, 0) / total for cls in ONSET_CLASSES}
        sims = {s: cosine_sim(profile, section_profiles[s]) for s in secs}
        best = max(sims, key=sims.get)
        row = f"f{f:<7} {total:>5} " + " ".join(f"{sims[s]:.3f}   " for s in secs) + f" {best}"
        print(row)

    # Pairwise similarity between astro folios
    print("\n### Pairwise Cosine Similarity Between Astro Folios")
    astro_profiles = {}
    for f in astro_folios:
        ws = astro_folio_words[f]
        if ws:
            counts = Counter(get_onset(w) for w in ws)
            total = len(ws)
            astro_profiles[f] = {cls: counts.get(cls, 0) / total for cls in ONSET_CLASSES}

    for i, f1 in enumerate(astro_folios):
        for f2 in astro_folios[i+1:]:
            if f1 in astro_profiles and f2 in astro_profiles:
                sim = cosine_sim(astro_profiles[f1], astro_profiles[f2])
                print(f"  f{f1} vs f{f2}: {sim:.4f}")

    # Astro onset profile vs other sections
    print("\n### Astro Onset Profile vs Other Sections")
    astro_profile = section_profiles.get('astro', {})
    print(f"{'Class':<8} {'Astro':>8} {'Herbal':>8} {'Pharma':>8} {'Stars':>8} {'Cosmo':>8}")
    for cls in ONSET_CLASSES:
        a = astro_profile.get(cls, 0)
        h = section_profiles['herbal'].get(cls, 0)
        ph = section_profiles['pharma'].get(cls, 0)
        st = section_profiles['stars'].get(cls, 0)
        co = section_profiles['cosmo'].get(cls, 0)
        all_vals = [a, h, ph, st, co]
        if max(all_vals) - min(all_vals) > 0.005:
            print(f"{cls:<8} {a:>7.4f}  {h:>7.4f}  {ph:>7.4f}  {st:>7.4f}  {co:>7.4f}")

    # What makes astro distinctive?
    print("\n### Astro-Distinctive Onset Classes (astro/corpus enrichment)")
    all_words = [w for r in records for w in r['words']]
    corpus_total = len(all_words)
    corpus_onset = Counter(get_onset(w) for w in all_words)
    astro_words = [w for r in astro_records for w in r['words']]
    astro_onset = Counter(get_onset(w) for w in astro_words)
    for cls in sorted(ONSET_CLASSES, key=lambda c: -(astro_onset.get(c, 0)/total_astro) / (corpus_onset.get(c, 0)/corpus_total) if corpus_onset.get(c, 0) > 0 else 0):
        a_rate = astro_onset.get(cls, 0) / total_astro
        c_rate = corpus_onset.get(cls, 0) / corpus_total
        if c_rate > 0 and astro_onset.get(cls, 0) >= 3:
            enrich = a_rate / c_rate
            if abs(enrich - 1) > 0.1:
                print(f"  {cls:<8} astro={a_rate:.4f}  corpus={c_rate:.4f}  enrichment={enrich:.2f}×")

    # Top astro words
    print("\n### Top Astro Words (with onset/suffix)")
    astro_vocab = compute_vocab(records, 'astro')
    print(f"{'Word':<16} {'n':>5} {'onset':<8} {'suffix'}")
    for w, n in astro_vocab.most_common(25):
        print(f"{w:<16} {n:>5} {get_onset(w):<8} {get_suffix(w)}")

    # Astro vocabulary vs all other sections
    astro_types = set(astro_vocab.keys())
    for sec in ['herbal', 'pharma', 'stars', 'cosmo']:
        sec_vocab = compute_vocab(records, sec)
        sec_types = set(sec_vocab.keys())
        j = jaccard(astro_types, sec_types)
        print(f"\nAstro vs {sec:<8} Jaccard={j:.3f}  shared={len(astro_types & sec_types)}  astro-only={len(astro_types - sec_types)}")

    # f87 pharma: why does it best-match astro?
    print("\n### f87 (Pharma) vs Astro Centroid")
    f87_words = [w for r in records if r['folio'] == 87 for w in r['words']]
    if f87_words:
        f87_total = len(f87_words)
        f87_counts = Counter(get_onset(w) for w in f87_words)
        f87_profile = {cls: f87_counts.get(cls, 0) / f87_total for cls in ONSET_CLASSES}
        pharma_profile = section_profiles.get('pharma', {})

        sim_to_astro = cosine_sim(f87_profile, astro_profile)
        sim_to_pharma = cosine_sim(f87_profile, pharma_profile)
        print(f"f87 cosine similarity: astro={sim_to_astro:.4f}, pharma={sim_to_pharma:.4f}")
        print(f"\nf87 vs Pharma centroid deviation (onset classes with |dev|>0.01):")
        for cls in ONSET_CLASSES:
            dev = f87_profile.get(cls, 0) - pharma_profile.get(cls, 0)
            if abs(dev) > 0.01:
                direction = "↑" if dev > 0 else "↓"
                print(f"  {cls:<8} {direction}{abs(dev):.4f}  f87={f87_profile.get(cls,0):.4f}  pharma_centroid={pharma_profile.get(cls,0):.4f}  astro={astro_profile.get(cls,0):.4f}")


def main():
    print("Loading corpus...")
    records, folio_dialect = parse_corpus(CORPUS_PATH)
    total_words = sum(len(r['words']) for r in records)
    print(f"Loaded {len(records)} body-text lines, {total_words} words, {len(set(r['folio'] for r in records))} folios")

    analyze_cosmo_vs_stars(records)
    analyze_astro_section(records, folio_dialect)

    print("\nDone.")


if __name__ == '__main__':
    main()
