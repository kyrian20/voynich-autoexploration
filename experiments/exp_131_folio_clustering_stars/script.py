"""
exp_131: Folio Vocabulary Clustering (H221) + Stars Paragraph Template (H232)
==============================================================================
H221: Do folios cluster by section based on vocabulary distribution?
      Compute cosine distance between folio onset-class profiles.
      Identify outlier folios and "transition" folios that bridge sections.

H232: Do stars section paragraphs have a repeating template?
      Stars paragraphs: line count distribution, line-position onset enrichment,
      whether specific onset patterns repeat across paragraphs.
"""
from pathlib import Path as _RepositoryPath

import re
import math
from collections import defaultdict, Counter

def get_onset(word):
    for pat in ['qok','qot','qo','cth','ch','sh','ok','ot','ol','olk','d','s']:
        if word.startswith(pat):
            return pat
    if len(word) >= 1 and word[0] in 'yklrtpf':
        return word[0]
    return 'other'

def get_suffix(word):
    suffixes = ['eeedy','eeey','eedy','edy','eey','aiin','ain','air','am',
                'ol','or','ar','al','ey','dy','y']
    for s in suffixes:
        if word.endswith(s) and len(word) > len(s):
            return s
    return 'other'

SECTION_MAP = {}
for f in range(1,   58): SECTION_MAP[f] = 'herbal'
for f in range(67,  74): SECTION_MAP[f] = 'astro'
for f in range(75,  85): SECTION_MAP[f] = 'cosmo'
for f in range(87, 103): SECTION_MAP[f] = 'pharma'
for f in range(103,117): SECTION_MAP[f] = 'stars'

def get_section(fn): return SECTION_MAP.get(fn, 'other')
def parse_folio_num(locus):
    m = re.match(r'f(\d+)', locus)
    return int(m.group(1)) if m else None

def parse_corpus(path):
    raw_lines = []
    folio_word_counts = defaultdict(Counter)
    # Also track paragraph structure for stars
    para_lines = []  # (folio_num, para_id, line_in_para, words, locus_type_prefix)

    with open(path, encoding='utf-8') as fh:
        para_counter = defaultdict(int)
        current_para = defaultdict(lambda: -1)

        for line in fh:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^>]+)>(.*)', line)
            if not m:
                continue
            locus_raw, text_raw = m.group(1), m.group(2)
            parts = locus_raw.split(',')
            locus = parts[0]
            locus_type_raw = parts[1] if len(parts) > 1 else ''
            locus_type = locus_type_raw.lstrip('@+*=~&')
            folio_num = parse_folio_num(locus)
            if folio_num is None:
                continue
            if not re.match(r'P', locus_type):
                continue
            text = re.sub(r'<[^>]*>', '', text_raw)
            text = re.sub(r'\[[^\]]*\]', ' ', text)
            text = re.sub(r'![\w.;@]*', '', text)
            text = re.sub(r'[*@&~=+$#{}?]', '', text)
            words = [w for w in re.split(r'[-.\s,]+', text)
                     if re.match(r'^[a-z]{2,}$', w)]
            if not words:
                continue

            # Detect paragraph start (original locus_type_raw contains '=' for new para)
            is_para_start = '=' in locus_type_raw
            if is_para_start or current_para[folio_num] < 0:
                current_para[folio_num] += 1

            raw_lines.append((locus, folio_num, words))
            for w in words:
                folio_word_counts[folio_num][w] += 1

    dialect_b = {}
    for fnum, cnt in folio_word_counts.items():
        total = sum(cnt.values())
        edy_count = sum(v for w, v in cnt.items() if w.endswith('edy') or w.endswith('eedy'))
        dialect_b[fnum] = (edy_count / total >= 0.05) if total > 0 else False

    records = []
    for locus, folio_num, words in raw_lines:
        dialect = 'B' if dialect_b.get(folio_num, False) else 'A'
        section = get_section(folio_num)
        records.append({
            'locus': locus, 'folio_num': folio_num,
            'dialect': dialect, 'section': section, 'words': words,
        })
    return records

# ── H221: Folio vocabulary clustering ─────────────────────────────────────────

def analyze_folio_clustering(records):
    print("=" * 70)
    print("H221: FOLIO VOCABULARY CLUSTERING BY ONSET-CLASS PROFILE")
    print("=" * 70)

    # Build folio onset-class profile
    folio_onsets = defaultdict(Counter)
    folio_total = Counter()
    folio_section = {}
    folio_dialect = {}

    for rec in records:
        fn = rec['folio_num']
        folio_section[fn] = rec['section']
        folio_dialect[fn] = rec['dialect']
        for w in rec['words']:
            o = get_onset(w)
            folio_onsets[fn][o] += 1
            folio_total[fn] += 1

    # Onset classes to use for profiles
    onset_classes = ['qok','qot','qo','cth','ch','sh','ok','ot','ol','d','s',
                     'y','p','r','k','t','l','f','other']

    # Compute normalized onset vectors per folio (folios with ≥30 words)
    folio_vectors = {}
    for fn, total in folio_total.items():
        if total < 30:
            continue
        vec = [folio_onsets[fn].get(o, 0) / total for o in onset_classes]
        folio_vectors[fn] = vec

    def cosine_sim(v1, v2):
        dot = sum(a*b for a,b in zip(v1,v2))
        n1 = math.sqrt(sum(a*a for a in v1))
        n2 = math.sqrt(sum(b*b for b in v2))
        return dot/(n1*n2) if n1*n2 > 0 else 0

    # For each folio, compute mean similarity to each section
    # First, compute centroid per section
    sections = ['herbal', 'astro', 'cosmo', 'pharma', 'stars']
    section_folios = defaultdict(list)
    for fn, vec in folio_vectors.items():
        s = folio_section.get(fn, 'other')
        if s in sections:
            section_folios[s].append((fn, vec))

    section_centroids = {}
    for s, fvs in section_folios.items():
        if not fvs:
            continue
        centroid = [sum(vec[i] for _, vec in fvs)/len(fvs) for i in range(len(onset_classes))]
        section_centroids[s] = centroid

    # For each folio, compute similarity to each section centroid
    print(f"\nFolio-to-section similarity (cosine; top/bottom by assigned section fit):")
    print(f"{'Folio':<8} {'Sec':>6} {'D':>2} {'Self-sim':>9} {'Best-sec':>9} {'Mismatch':>9}")
    print("-" * 50)

    folio_sims = {}
    for fn, vec in sorted(folio_vectors.items()):
        s = folio_section.get(fn, 'other')
        if s not in section_centroids:
            continue
        self_sim = cosine_sim(vec, section_centroids[s])
        # Best section
        best_s = max(sections, key=lambda x: cosine_sim(vec, section_centroids.get(x, [0]*len(onset_classes))))
        best_sim = cosine_sim(vec, section_centroids[best_s])
        folio_sims[fn] = {
            'section': s, 'dialect': folio_dialect.get(fn,'?'),
            'self_sim': self_sim, 'best_sec': best_s, 'best_sim': best_sim,
            'mismatch': s != best_s
        }

    # Sort by self_sim (ascending = outliers first)
    sorted_folios = sorted(folio_sims.items(), key=lambda x: x[1]['self_sim'])

    print("\nLOWEST self-similarity to assigned section (potential outlier folios):")
    for fn, d in sorted_folios[:20]:
        mark = '***' if d['mismatch'] else ''
        print(f"  f{fn:<5} {d['section']:<8} {d['dialect']:<1} self={d['self_sim']:.3f} best={d['best_sec']:<8} ({d['best_sim']:.3f}) {mark}")

    print("\nHIGHEST self-similarity to assigned section (most typical folios):")
    for fn, d in sorted_folios[-15:]:
        print(f"  f{fn:<5} {d['section']:<8} {d['dialect']:<1} self={d['self_sim']:.3f}")

    # Mismatched folios (best section ≠ assigned section)
    mismatched = [(fn, d) for fn, d in folio_sims.items() if d['mismatch']]
    print(f"\nFolios where best-match section ≠ assigned section ({len(mismatched)} folios):")
    for fn, d in sorted(mismatched, key=lambda x: -abs(x[1]['best_sim']-x[1]['self_sim'])):
        print(f"  f{fn}: assigned={d['section']}, best-match={d['best_sec']} (self={d['self_sim']:.3f}, best={d['best_sim']:.3f})")

    # Show section-level mean self-similarity
    print(f"\nMean self-similarity by section:")
    for s in sections:
        sims = [d['self_sim'] for fn, d in folio_sims.items() if d['section'] == s]
        if sims:
            print(f"  {s:<10}: mean={sum(sims)/len(sims):.3f} (n={len(sims)})")

    # Key finding: which folios most resemble another section?
    print(f"\nFolios most similar to a different section (top cross-section affinities):")
    cross_sec = [(fn, d) for fn, d in folio_sims.items() if d['mismatch']]
    for fn, d in sorted(cross_sec, key=lambda x: -x[1]['best_sim'])[:10]:
        print(f"  f{fn} ({d['section']}, {d['dialect']}) → best={d['best_sec']} ({d['best_sim']:.3f}) vs self={d['self_sim']:.3f}")


# ── H232: Stars paragraph template ───────────────────────────────────────────

def analyze_stars_paragraphs(records):
    print()
    print("=" * 70)
    print("H232: STARS SECTION PARAGRAPH TEMPLATE")
    print("=" * 70)

    # Extract stars records
    stars_records = [r for r in records if r['section'] == 'stars']
    total_words = sum(len(r['words']) for r in stars_records)
    print(f"\nStars records: {len(stars_records)} lines, {total_words:,} words")

    # Build paragraph structure using locus numbering
    # Locus format: f103r.1, f103r.2 etc. Within same folio, group by paragraph
    # Approximate: lines with same folio number are grouped; use position within folio

    # Group stars lines by folio
    folio_lines = defaultdict(list)
    for rec in stars_records:
        folio_lines[rec['folio_num']].append(rec)

    # Within each folio, treat consecutive lines as a unit
    # Compute per-folio statistics: words per line, onset distributions by line position
    folio_stats = {}
    for fn, lines in sorted(folio_lines.items()):
        if not lines:
            continue
        # Line length distribution
        lengths = [len(r['words']) for r in lines]
        # Onset distribution at each line position
        # Use relative position (first/last/middle)
        first_words = [r['words'][0] for r in lines if r['words']]
        last_words = [r['words'][-1] for r in lines if r['words']]
        folio_stats[fn] = {
            'n_lines': len(lines),
            'mean_len': sum(lengths)/len(lengths),
            'first_onsets': Counter(get_onset(w) for w in first_words),
            'last_onsets': Counter(get_onset(w) for w in last_words),
        }

    # Aggregate across all stars folios
    all_first = Counter()
    all_last = Counter()
    all_mid = Counter()
    all_second = Counter()
    for rec in stars_records:
        words = rec['words']
        n = len(words)
        if words:
            all_first[get_onset(words[0])] += 1
        if len(words) >= 2:
            all_last[get_onset(words[-1])] += 1
            all_second[get_onset(words[1])] += 1
        for w in words[1:-1]:
            all_mid[get_onset(w)] += 1

    total_first = sum(all_first.values())
    total_last = sum(all_last.values())
    total_mid = sum(all_mid.values())

    # Compute baseline (overall onset distribution in stars)
    baseline = Counter()
    for rec in stars_records:
        for w in rec['words']:
            baseline[get_onset(w)] += 1
    total_baseline = sum(baseline.values())

    print(f"\nLine-position onset enrichment in stars (obs/baseline):")
    print(f"{'Onset':<8} {'First-enr':>10} {'Second-enr':>11} {'Mid-enr':>9} {'Last-enr':>9}")
    print("-" * 48)
    key_onsets = ['qok','qot','qo','ch','sh','ok','ot','ol','d','s','y','p','r','k','t','other']
    for o in key_onsets:
        base = baseline.get(o, 0) / total_baseline if total_baseline > 0 else 0
        if base == 0:
            continue
        f_enr = (all_first.get(o,0)/total_first) / base if total_first > 0 else 0
        s_enr = (all_second.get(o,0)/sum(all_second.values())) / base if sum(all_second.values()) > 0 else 0
        m_enr = (all_mid.get(o,0)/total_mid) / base if total_mid > 0 else 0
        l_enr = (all_last.get(o,0)/total_last) / base if total_last > 0 else 0
        if max(f_enr, s_enr, m_enr, l_enr) > 1.5 or min(f_enr, s_enr, m_enr, l_enr) < 0.5:
            print(f"{o:<8} {f_enr:>9.2f}× {s_enr:>10.2f}× {m_enr:>8.2f}× {l_enr:>8.2f}×")

    # Stars folio overview
    print(f"\nStars folio overview:")
    print(f"{'Folio':>7} {'Lines':>6} {'Words':>6} {'MeanLen':>8} {'Top-first':>12} {'Top-last':>12}")
    print("-" * 60)
    for fn in sorted(folio_stats.keys()):
        d = folio_stats[fn]
        tf = d['first_onsets'].most_common(1)[0][0] if d['first_onsets'] else '—'
        tl = d['last_onsets'].most_common(1)[0][0] if d['last_onsets'] else '—'
        n_words = sum(len(r['words']) for r in folio_lines[fn])
        print(f"  f{fn:<5} {d['n_lines']:>5} {n_words:>6} {d['mean_len']:>8.1f} {tf:>12} {tl:>12}")

    # Suffix distribution in stars (line-position enrichment)
    print(f"\nStars suffix distribution by line position:")
    stars_suf_first = Counter()
    stars_suf_last = Counter()
    stars_suf_mid = Counter()
    for rec in stars_records:
        words = rec['words']
        n = len(words)
        for i, w in enumerate(words):
            s = get_suffix(w)
            if i == 0:
                stars_suf_first[s] += 1
            elif i == n - 1:
                stars_suf_last[s] += 1
            else:
                stars_suf_mid[s] += 1

    suf_baseline = Counter()
    for rec in stars_records:
        for w in rec['words']:
            suf_baseline[get_suffix(w)] += 1
    suf_total = sum(suf_baseline.values())
    sf_total = sum(stars_suf_first.values())
    sl_total = sum(stars_suf_last.values())
    sm_total = sum(stars_suf_mid.values())

    print(f"{'Suffix':<8} {'First-enr':>10} {'Mid-enr':>9} {'Last-enr':>9}")
    print("-" * 33)
    key_suffs = ['aiin','ain','edy','eedy','ol','or','ar','al','am','dy','ey','y','other']
    for s in key_suffs:
        base = suf_baseline.get(s,0)/suf_total if suf_total > 0 else 0
        if base == 0:
            continue
        f = (stars_suf_first.get(s,0)/sf_total) / base if sf_total > 0 else 0
        mid = (stars_suf_mid.get(s,0)/sm_total) / base if sm_total > 0 else 0
        l = (stars_suf_last.get(s,0)/sl_total) / base if sl_total > 0 else 0
        if max(f, mid, l) > 1.3 or min(f, mid, l) < 0.7:
            print(f"{s:<8} {f:>9.2f}× {mid:>8.2f}× {l:>8.2f}×")

    # Check for repeating line-type sequences across stars paragraphs
    # Top first-words across stars lines
    print(f"\nTop 20 line-initial words in stars:")
    stars_first_words = Counter(r['words'][0] for r in stars_records if r['words'])
    for w, cnt in stars_first_words.most_common(20):
        print(f"  {w:<15} n={cnt} onset={get_onset(w)}")

    # Stars section: are there paragraphs of similar length (catalog entries)?
    stars_line_counts = []
    for fn, lines in folio_lines.items():
        stars_line_counts.append(len(lines))
    print(f"\nLines per folio in stars: min={min(stars_line_counts)}, max={max(stars_line_counts)}, mean={sum(stars_line_counts)/len(stars_line_counts):.1f}")


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    corpus_path = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')
    print("Loading corpus...")
    records = parse_corpus(corpus_path)
    total_words = sum(len(r['words']) for r in records)
    print(f"Loaded {len(records)} lines, {total_words:,} word tokens")

    analyze_folio_clustering(records)
    analyze_stars_paragraphs(records)
