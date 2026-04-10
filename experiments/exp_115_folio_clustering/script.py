#!/usr/bin/env python3
"""
exp_115: Folio-Level Vocabulary Distance Clustering (H225)
Tests: Do folios cluster by section based on word frequency vectors?
Do suffix pattern profiles (eey vs eedy vs edy rates) cluster independently?
Are there transition folios or outliers?
"""

import re
import math
from collections import defaultdict, Counter

DATA = 'data/transcriptions/eva_zl3b.txt'

SECTION_MAP = {}
for f in range(1, 58): SECTION_MAP[f] = 'herbal'
for f in range(67, 74): SECTION_MAP[f] = 'astro'
for f in range(75, 85): SECTION_MAP[f] = 'cosmo'
for f in range(87, 103): SECTION_MAP[f] = 'pharma'
for f in range(103, 117): SECTION_MAP[f] = 'stars'


def parse_eva(path):
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

            prefix = ''.join(c for c in locus_type if c in '@+*=~&')
            lt = locus_type[len(prefix):]
            is_body = bool(re.match(r'P', lt))
            if not is_body: continue

            text_clean = re.sub(r'<[^>]*>', '', text)
            text_clean = re.sub(r'\[[^\]]*\]', lambda m: m.group(0)[1:-1].split(':')[0], text_clean)
            text_clean = re.sub(r'\{[^}]*\}', '', text_clean)
            text_clean = re.sub(r'@\d+;?', '', text_clean)
            text_clean = re.sub(r'<%>|<!.*?>|<\$>', '', text_clean)

            words = [w for w in re.split(r'[-.\s,]', text_clean)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words: continue

            for w in words:
                if 'edy' in w or 'eedy' in w:
                    edy_counts[folio_num] += 1
                total_counts[folio_num] += 1
                records.append({'word': w, 'folio': folio_num})

    dialect_map = {fnum: ('B' if edy_counts[fnum]/max(1,total_counts[fnum]) >= 0.05 else 'A')
                   for fnum in total_counts}
    for r in records:
        r['dialect'] = dialect_map.get(r['folio'], 'A')
        r['section'] = SECTION_MAP.get(r['folio'], 'other')

    return records, dialect_map


def get_suffix(word):
    for suf in ['eeedy','eeey','eedy','edy','eey','aiin','ain','ol','or','ar','al','ey','dy','y']:
        if word.endswith(suf) and len(word) > len(suf):
            return suf
    return 'other'


def cosine_similarity(v1, v2, vocab):
    dot = sum(v1.get(w,0) * v2.get(w,0) for w in vocab)
    n1 = math.sqrt(sum(x*x for x in v1.values()))
    n2 = math.sqrt(sum(x*x for x in v2.values()))
    if n1 == 0 or n2 == 0: return 0.0
    return dot / (n1 * n2)


def build_folio_profiles(records):
    """Build per-folio word frequency vectors and suffix profile vectors."""
    folio_words = defaultdict(Counter)
    folio_suffix = defaultdict(Counter)
    folio_total = defaultdict(int)
    folio_section = {}
    folio_dialect = {}

    for r in records:
        f = r['folio']
        w = r['word']
        folio_words[f][w] += 1
        folio_suffix[f][get_suffix(w)] += 1
        folio_total[f] += 1
        folio_section[f] = r['section']
        folio_dialect[f] = r['dialect']

    return folio_words, folio_suffix, folio_total, folio_section, folio_dialect


def suffix_profile_vector(suffix_counts, total):
    """Normalized suffix rate vector for a folio."""
    suffixes = ['edy','eedy','eey','eeey','eeedy','y','ol','or','aiin','dy','ar','al']
    return {suf: suffix_counts.get(suf, 0) / max(1, total) for suf in suffixes}


def cosine_suffix(sf1, sf2):
    keys = set(sf1) | set(sf2)
    dot = sum(sf1.get(k,0) * sf2.get(k,0) for k in keys)
    n1 = math.sqrt(sum(x*x for x in sf1.values()))
    n2 = math.sqrt(sum(x*x for x in sf2.values()))
    if n1 == 0 or n2 == 0: return 0.0
    return dot / (n1 * n2)


def h225_folio_clustering(records):
    print("=" * 70)
    print("H225: Folio-Level Vocabulary Distance Clustering")
    print("=" * 70)

    folio_words, folio_suffix, folio_total, folio_section, folio_dialect = build_folio_profiles(records)

    # Only use folios with enough tokens
    valid_folios = [f for f, n in folio_total.items() if n >= 50 and folio_section[f] != 'other']
    valid_folios.sort()

    print(f"\n{len(valid_folios)} valid folios (≥50 tokens, known section)")

    # === PART 1: Suffix Profile Similarity ===
    print("\n--- Part 1: Folio suffix profile vectors ---")
    folio_sfvec = {f: suffix_profile_vector(folio_suffix[f], folio_total[f])
                   for f in valid_folios}

    print(f"\n{'Folio':<8} {'Sect':<8} {'D':<3} {'n':<6} {'edy%':<7} {'eedy%':<7} {'eey%':<7} {'y%':<6} {'ol%':<6} {'aiin%':<7}")
    for f in valid_folios:
        sv = folio_sfvec[f]
        s = folio_section[f]
        d = folio_dialect[f]
        n = folio_total[f]
        print(f"{f:<8} {s:<8} {d:<3} {n:<6} "
              f"{100*sv['edy']:<7.1f} {100*sv['eedy']:<7.1f} {100*sv['eey']:<7.1f} "
              f"{100*sv['y']:<6.1f} {100*sv['ol']:<6.1f} {100*sv['aiin']:<7.1f}")

    # === PART 2: Within-section vs across-section suffix similarity ===
    print("\n--- Part 2: Within-section vs cross-section suffix similarity ---")

    sections = ['herbal','cosmo','stars','pharma','astro']
    within_sims = defaultdict(list)
    cross_sims = []

    for i, f1 in enumerate(valid_folios):
        for f2 in valid_folios[i+1:]:
            sim = cosine_suffix(folio_sfvec[f1], folio_sfvec[f2])
            s1 = folio_section[f1]
            s2 = folio_section[f2]
            if s1 == s2:
                within_sims[s1].append(sim)
            else:
                cross_sims.append(sim)

    print(f"\n{'Section':<12} {'Within_mean':<14} {'Within_min':<12} {'Within_max':<12} {'n_pairs'}")
    for s in sections:
        sims = within_sims[s]
        if not sims: continue
        print(f"{s:<12} {sum(sims)/len(sims):<14.3f} {min(sims):<12.3f} {max(sims):<12.3f} {len(sims)}")

    cross_mean = sum(cross_sims)/len(cross_sims) if cross_sims else 0
    print(f"\nCross-section mean similarity: {cross_mean:.3f} (n={len(cross_sims)} pairs)")

    # === PART 3: Nearest-neighbor section assignment ===
    print("\n--- Part 3: Section-centroid suffix similarity ---")

    # Compute per-section centroid suffix vectors
    section_centroids = {}
    for s in sections:
        s_folios = [f for f in valid_folios if folio_section[f] == s]
        if not s_folios: continue
        centroid = defaultdict(float)
        for f in s_folios:
            for suf, rate in folio_sfvec[f].items():
                centroid[suf] += rate / len(s_folios)
        section_centroids[s] = dict(centroid)

    # For each folio, find closest section centroid
    print(f"\n{'Folio':<8} {'True':<10} {'Nearest':<10} {'Sim':<8} {'2nd':<10} {'Correct?'}")
    correct = 0
    total_tested = 0
    for f in valid_folios:
        true_sect = folio_section[f]
        sims_to_centroids = {s: cosine_suffix(folio_sfvec[f], centroid)
                             for s, centroid in section_centroids.items()}
        sorted_sects = sorted(sims_to_centroids.items(), key=lambda x: -x[1])
        nearest = sorted_sects[0][0]
        nearest_sim = sorted_sects[0][1]
        second = sorted_sects[1][0] if len(sorted_sects) > 1 else '—'
        is_correct = (nearest == true_sect)
        if is_correct: correct += 1
        total_tested += 1
        mark = '✓' if is_correct else '✗'
        print(f"{f:<8} {true_sect:<10} {nearest:<10} {nearest_sim:<8.3f} {second:<10} {mark}")

    print(f"\nSection assignment accuracy: {correct}/{total_tested} ({100*correct/total_tested:.1f}%)")

    # === PART 4: Vocabulary-based folio similarity (top-N words) ===
    print("\n--- Part 4: Vocabulary overlap (Jaccard) between section groups ---")

    # Build per-section vocabulary (words occurring ≥3 times in section)
    section_vocab = defaultdict(Counter)
    for r in records:
        s = r['section']
        if s == 'other': continue
        section_vocab[s][r['word']] += 1

    section_sets = {s: {w for w, c in vc.items() if c >= 3}
                    for s, vc in section_vocab.items()}

    print(f"\n{'Pair':<20} {'Jaccard':<10} {'|A|':<8} {'|B|':<8} {'|A∩B|':<8}")
    for i, s1 in enumerate(sections):
        if s1 not in section_sets: continue
        for s2 in sections[i+1:]:
            if s2 not in section_sets: continue
            a = section_sets[s1]
            b = section_sets[s2]
            inter = len(a & b)
            union = len(a | b)
            j = inter / union if union > 0 else 0
            print(f"{s1+'-'+s2:<20} {j:<10.3f} {len(a):<8} {len(b):<8} {inter:<8}")

    # === PART 5: Transition folios — detect boundary folios ===
    print("\n--- Part 5: Folio-by-folio suffix similarity with neighbors ---")
    print("(Looking for sharp transitions and outlier folios)")

    folio_seq = sorted(valid_folios)
    print(f"\n{'Folio':<8} {'Sect':<8} {'Sim_prev':<12} {'Sim_next':<12} {'Transition?'}")
    threshold = 0.15  # similarity drop threshold for transition

    for i, f in enumerate(folio_seq):
        prev_f = folio_seq[i-1] if i > 0 else None
        next_f = folio_seq[i+1] if i < len(folio_seq)-1 else None

        sim_prev = cosine_suffix(folio_sfvec[f], folio_sfvec[prev_f]) if prev_f else float('nan')
        sim_next = cosine_suffix(folio_sfvec[f], folio_sfvec[next_f]) if next_f else float('nan')

        is_transition = False
        if prev_f and next_f:
            prev_same = folio_section[prev_f] == folio_section[f]
            next_same = folio_section[next_f] == folio_section[f]
            is_transition = not prev_same or not next_same

        sp = f"{sim_prev:.3f}" if not math.isnan(sim_prev) else '—'
        sn = f"{sim_next:.3f}" if not math.isnan(sim_next) else '—'
        mark = '◄ BOUNDARY' if is_transition else ''
        print(f"{f:<8} {folio_section[f]:<8} {sp:<12} {sn:<12} {mark}")

    # === PART 6: B-suffix section clustering quality ===
    print("\n--- Part 6: B-suffix (edy/eedy/eey) rates per folio (B-dialect only) ---")

    b_folios = [f for f in valid_folios if folio_dialect[f] == 'B']
    print(f"\n{'Folio':<8} {'Sect':<8} {'n':<6} {'edy%':<8} {'eedy%':<8} {'eey%':<8} {'Dominant'}")
    for f in b_folios:
        sf = folio_suffix[f]
        b_suf_total = sf.get('edy',0) + sf.get('eedy',0) + sf.get('eey',0)
        if b_suf_total < 5: continue
        edy_r = 100*sf.get('edy',0)/b_suf_total
        eedy_r = 100*sf.get('eedy',0)/b_suf_total
        eey_r = 100*sf.get('eey',0)/b_suf_total
        dom = max(['edy','eedy','eey'], key=lambda x: sf.get(x,0))
        print(f"{f:<8} {folio_section[f]:<8} {b_suf_total:<6} {edy_r:<8.1f} {eedy_r:<8.1f} {eey_r:<8.1f} {dom}")


def main():
    print("Loading data...")
    records, dialect_map = parse_eva(DATA)
    print(f"Total body tokens: {len(records)}")
    h225_folio_clustering(records)


if __name__ == '__main__':
    main()
