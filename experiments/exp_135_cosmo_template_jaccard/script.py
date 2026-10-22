"""
exp_135: Cosmo Line-Element Template (H264) + Cross-Section Vocabulary Jaccard Matrix (H265)
H264: Does Cosmo have a formal line-template analogous to Stars' [OPENER][sh-2nd][-am LAST]?
H265: What is the full pairwise Jaccard similarity between all 5 sections?
"""
from pathlib import Path as _RepositoryPath

import re
from collections import defaultdict, Counter

CORPUS_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

SECTION_MAP = {}
for f in range(1, 58):
    SECTION_MAP[f] = "herbal"
for f in range(67, 74):
    SECTION_MAP[f] = "astro"
for f in range(75, 85):
    SECTION_MAP[f] = "cosmo"
for f in range(87, 103):
    SECTION_MAP[f] = "pharma"
for f in range(103, 117):
    SECTION_MAP[f] = "stars"

SUFFIXES = ["eeedy", "eeey", "eedy", "edy", "eey", "aiin", "ain", "air",
            "am", "ol", "or", "ar", "al", "ey", "dy", "y"]

ONSET_CLASSES = {
    "qok": re.compile(r'^qok'),
    "qot": re.compile(r'^qot'),
    "qo":  re.compile(r'^qo(?![kt])'),
    "cth": re.compile(r'^cth'),
    "ch":  re.compile(r'^ch(?!e)'),
    "ch_e":re.compile(r'^che'),
    "sh":  re.compile(r'^sh'),
    "ok":  re.compile(r'^ok'),
    "ot":  re.compile(r'^ot'),
    "ol":  re.compile(r'^ol'),
    "d":   re.compile(r'^d'),
    "s":   re.compile(r'^s'),
    "y":   re.compile(r'^y'),
    "k":   re.compile(r'^k'),
    "t":   re.compile(r'^t'),
    "l":   re.compile(r'^l'),
    "r":   re.compile(r'^r'),
    "p":   re.compile(r'^p'),
    "f":   re.compile(r'^f'),
}

def get_onset(word):
    for name, pat in ONSET_CLASSES.items():
        if pat.match(word):
            return name
    return "other"

def get_suffix(word):
    for s in SUFFIXES:
        if word.endswith(s):
            return s
    return "other"

def get_folio_num(folio_str):
    m = re.match(r'f(\d+)', folio_str)
    return int(m.group(1)) if m else None

def parse_corpus():
    records = []
    with open(CORPUS_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^>]+)>(.*)', line)
            if not m:
                continue
            locus_raw, text = m.group(1), m.group(2).strip()
            parts = locus_raw.split(',')
            if len(parts) < 2:
                continue
            folio_str = parts[0]
            locus_type = parts[1].lstrip('@+*=~&')
            if not re.match(r'P', locus_type):
                continue
            folio_num = get_folio_num(folio_str)
            if folio_num is None:
                continue
            section = SECTION_MAP.get(folio_num)
            if section is None:
                continue
            words = [w for w in text.split('.') if re.match(r'[a-z]', w)]
            if not words:
                continue
            records.append({
                'folio': folio_str,
                'folio_num': folio_num,
                'section': section,
                'locus_type': locus_type,
                'words': words
            })
    return records

def get_folio_dialect(records):
    folio_counts = defaultdict(lambda: {'edy': 0, 'eedy': 0, 'total': 0})
    for rec in records:
        fn = rec['folio']
        for w in rec['words']:
            folio_counts[fn]['total'] += 1
            if w.endswith('eedy'):
                folio_counts[fn]['eedy'] += 1
            elif w.endswith('edy'):
                folio_counts[fn]['edy'] += 1
    dialect = {}
    for fn, cnts in folio_counts.items():
        if cnts['total'] < 10:
            dialect[fn] = 'unknown'
        else:
            rate = (cnts['edy'] + cnts['eedy']) / cnts['total']
            dialect[fn] = 'B' if rate >= 0.05 else 'A'
    return dialect

# ─── LINE-POSITION UTILITIES ───────────────────────────────────────────────────

def positional_slots(words):
    """Return list of (word, slot) where slot in {first,second,mid,last}"""
    n = len(words)
    result = []
    for i, w in enumerate(words):
        if n == 1:
            slot = "first"  # single-word line → treat as first
        elif i == 0:
            slot = "first"
        elif i == 1:
            slot = "second"
        elif i == n - 1:
            slot = "last"
        else:
            slot = "mid"
    result = []
    for i, w in enumerate(words):
        if n == 1:
            slot = "first"
        elif i == 0:
            slot = "first"
        elif i == 1:
            slot = "second"
        elif i == n - 1:
            slot = "last"
        else:
            slot = "mid"
        result.append((w, slot))
    return result

def compute_enrichment(slot_onset_counts, baseline_onset_counts, slot_total, baseline_total):
    """Compute enrichment ratios for each onset class in a slot vs baseline."""
    enrichment = {}
    for onset in list(ONSET_CLASSES.keys()) + ["other"]:
        slot_rate = slot_onset_counts.get(onset, 0) / max(slot_total, 1)
        base_rate = baseline_onset_counts.get(onset, 0) / max(baseline_total, 1)
        if base_rate > 0:
            enrichment[onset] = slot_rate / base_rate
        else:
            enrichment[onset] = 0.0
    return enrichment

# ─── H264: COSMO LINE-ELEMENT TEMPLATE ────────────────────────────────────────

def analyze_cosmo_template(records):
    print("=" * 70)
    print("H264: COSMO LINE-ELEMENT TEMPLATE")
    print("=" * 70)

    # Get cosmo and stars records for comparison
    cosmo_recs = [r for r in records if r['section'] == 'cosmo']
    stars_recs = [r for r in records if r['section'] == 'stars']

    print(f"\nCosmo lines: {len(cosmo_recs)}")
    print(f"Stars lines (reference): {len(stars_recs)}")

    for section_name, section_recs in [("COSMO", cosmo_recs), ("STARS", stars_recs)]:
        print(f"\n{'─'*60}")
        print(f"{section_name} LINE-POSITION ANALYSIS")
        print(f"{'─'*60}")

        # Aggregate by position
        slot_onset = defaultdict(Counter)  # slot → onset → count
        slot_suffix = defaultdict(Counter)  # slot → suffix → count
        slot_total = Counter()
        baseline_onset = Counter()
        baseline_total = 0

        for rec in section_recs:
            words = rec['words']
            slots = positional_slots(words)
            for w, slot in slots:
                onset = get_onset(w)
                suffix = get_suffix(w)
                slot_onset[slot][onset] += 1
                slot_suffix[slot][suffix] += 1
                slot_total[slot] += 1
                baseline_onset[onset] += 1
                baseline_total += 1

        print(f"\nBaseline onset distribution (all positions):")
        for onset, cnt in sorted(baseline_onset.items(), key=lambda x: -x[1])[:12]:
            print(f"  {onset:8s}: {cnt:5d}  ({100*cnt/baseline_total:.1f}%)")

        for slot in ["first", "second", "mid", "last"]:
            total = slot_total[slot]
            if total == 0:
                continue
            enrichment = compute_enrichment(slot_onset[slot], baseline_onset, total, baseline_total)
            print(f"\n  [{slot.upper()}] n={total}")
            # Top enriched onsets
            top = sorted(enrichment.items(), key=lambda x: -x[1])[:8]
            for onset, ratio in top:
                cnt = slot_onset[slot].get(onset, 0)
                pct = 100 * cnt / total
                print(f"    {onset:8s}: {pct:5.1f}%  enrichment={ratio:.2f}×")

        # Suffix enrichment at last position
        print(f"\n  SUFFIX ENRICHMENT AT LAST POSITION:")
        last_total = slot_total['last']
        all_suffixes = list(SUFFIXES) + ["other"]
        suf_enrichments = []
        baseline_suf = Counter()
        for rec in section_recs:
            for w in rec['words']:
                baseline_suf[get_suffix(w)] += 1
        for suf in all_suffixes:
            last_rate = slot_suffix['last'].get(suf, 0) / max(last_total, 1)
            base_rate = baseline_suf.get(suf, 0) / max(baseline_total, 1)
            ratio = last_rate / base_rate if base_rate > 0 else 0
            cnt = slot_suffix['last'].get(suf, 0)
            suf_enrichments.append((suf, cnt, 100*cnt/max(last_total,1), ratio))
        for suf, cnt, pct, ratio in sorted(suf_enrichments, key=lambda x: -x[3])[:10]:
            print(f"    -{suf:8s}: {cnt:4d} ({pct:.1f}%)  enrichment={ratio:.2f}×")

        # Suffix enrichment at first position
        print(f"\n  SUFFIX ENRICHMENT AT FIRST POSITION:")
        first_total = slot_total['first']
        suf_enrichments_first = []
        for suf in all_suffixes:
            first_rate = slot_suffix['first'].get(suf, 0) / max(first_total, 1)
            base_rate = baseline_suf.get(suf, 0) / max(baseline_total, 1)
            ratio = first_rate / base_rate if base_rate > 0 else 0
            cnt = slot_suffix['first'].get(suf, 0)
            suf_enrichments_first.append((suf, cnt, 100*cnt/max(first_total,1), ratio))
        for suf, cnt, pct, ratio in sorted(suf_enrichments_first, key=lambda x: -x[3])[:8]:
            print(f"    -{suf:8s}: {cnt:4d} ({pct:.1f}%)  enrichment={ratio:.2f}×")

        # Top words by position
        for slot in ["first", "last"]:
            slot_words = Counter()
            for rec in section_recs:
                slots = positional_slots(rec['words'])
                for w, s in slots:
                    if s == slot:
                        slot_words[w] += 1
            print(f"\n  TOP {slot.upper()} WORDS:")
            for w, c in slot_words.most_common(15):
                onset = get_onset(w)
                suffix = get_suffix(w)
                print(f"    {w:20s}: {c:4d}  onset={onset} suffix={suffix}")

    # Compare cosmo vs stars line-opening/closing enrichment directly
    print(f"\n{'─'*60}")
    print("COSMO vs STARS POSITION ENRICHMENT COMPARISON")
    print(f"{'─'*60}")

    print(f"\n{'Onset':<10} {'Cosmo-FIRST':>14} {'Stars-FIRST':>14} {'Cosmo-LAST':>14} {'Stars-LAST':>14}")
    print("-" * 66)

    # Recompute slot data for both
    def get_slot_data(recs):
        slot_onset = defaultdict(Counter)
        slot_total = Counter()
        baseline_onset = Counter()
        baseline_total = 0
        for rec in recs:
            for w, slot in positional_slots(rec['words']):
                onset = get_onset(w)
                slot_onset[slot][onset] += 1
                slot_total[slot] += 1
                baseline_onset[onset] += 1
                baseline_total += 1
        return slot_onset, slot_total, baseline_onset, baseline_total

    c_so, c_st, c_bo, c_bt = get_slot_data(cosmo_recs)
    s_so, s_st, s_bo, s_bt = get_slot_data(stars_recs)

    for onset in list(ONSET_CLASSES.keys()) + ["other"]:
        c_first = c_so['first'].get(onset, 0) / max(c_st['first'], 1) / (c_bo.get(onset, 0) / max(c_bt, 1)) if c_bo.get(onset, 0) else 0
        s_first = s_so['first'].get(onset, 0) / max(s_st['first'], 1) / (s_bo.get(onset, 0) / max(s_bt, 1)) if s_bo.get(onset, 0) else 0
        c_last  = c_so['last'].get(onset, 0) / max(c_st['last'], 1) / (c_bo.get(onset, 0) / max(c_bt, 1)) if c_bo.get(onset, 0) else 0
        s_last  = s_so['last'].get(onset, 0) / max(s_st['last'], 1) / (s_bo.get(onset, 0) / max(s_bt, 1)) if s_bo.get(onset, 0) else 0
        if max(c_first, s_first, c_last, s_last) > 1.3 or min(c_first, s_first, c_last, s_last) < 0.7:
            print(f"{onset:<10} {c_first:>14.2f}× {s_first:>14.2f}× {c_last:>14.2f}× {s_last:>14.2f}×")


# ─── H265: CROSS-SECTION VOCABULARY JACCARD MATRIX ───────────────────────────

def analyze_jaccard_matrix(records, folio_dialect):
    print("\n" + "=" * 70)
    print("H265: CROSS-SECTION VOCABULARY JACCARD MATRIX")
    print("=" * 70)

    sections = ["herbal", "astro", "cosmo", "pharma", "stars"]

    # Build vocabulary sets per section
    section_vocab = defaultdict(set)
    section_word_counts = defaultdict(Counter)

    for rec in records:
        sec = rec['section']
        for w in rec['words']:
            section_vocab[sec].add(w)
            section_word_counts[sec][w] += 1

    print("\nSection vocabulary sizes:")
    for sec in sections:
        print(f"  {sec:8s}: {len(section_vocab[sec]):5d} types")

    # Pairwise Jaccard matrix
    print("\n5×5 PAIRWISE JACCARD SIMILARITY MATRIX (type-level):")
    print(f"{'':10s}", end="")
    for sec in sections:
        print(f"  {sec[:6]:>8s}", end="")
    print()

    jaccard_matrix = {}
    for s1 in sections:
        print(f"{s1[:10]:10s}", end="")
        for s2 in sections:
            v1 = section_vocab[s1]
            v2 = section_vocab[s2]
            intersection = len(v1 & v2)
            union = len(v1 | v2)
            j = intersection / union if union > 0 else 0
            jaccard_matrix[(s1, s2)] = j
            print(f"  {j:>8.4f}", end="")
        print()

    # Shared and exclusive vocabulary
    print("\n\nPAIRWISE SHARED VOCABULARY (intersection sizes):")
    print(f"{'':10s}", end="")
    for sec in sections:
        print(f"  {sec[:6]:>8s}", end="")
    print()
    for s1 in sections:
        print(f"{s1[:10]:10s}", end="")
        for s2 in sections:
            v1 = section_vocab[s1]
            v2 = section_vocab[s2]
            print(f"  {len(v1 & v2):>8d}", end="")
        print()

    # Exclusive vocabulary per section
    print("\nEXCLUSIVE VOCABULARY (types unique to each section):")
    for sec in sections:
        others = set()
        for other in sections:
            if other != sec:
                others |= section_vocab[other]
        exclusive = section_vocab[sec] - others
        print(f"  {sec:8s}: {len(exclusive):4d} exclusive types")
        # Top exclusive by frequency
        top_excl = sorted([(w, section_word_counts[sec][w]) for w in exclusive],
                          key=lambda x: -x[1])[:10]
        for w, c in top_excl:
            print(f"    {w:20s}: {c:4d}  onset={get_onset(w)} suffix={get_suffix(w)}")

    # Cross-dialect analysis
    print("\nDIALECT-SPLIT JACCARD (A-folios vs B-folios):")
    dialect_sec_vocab = defaultdict(lambda: defaultdict(set))
    for rec in records:
        d = folio_dialect.get(rec['folio'], 'unknown')
        if d in ('A', 'B'):
            sec = rec['section']
            for w in rec['words']:
                dialect_sec_vocab[d][sec].add(w)

    for d in ['A', 'B']:
        print(f"\n  Dialect {d}:")
        d_secs = [s for s in sections if dialect_sec_vocab[d][s]]
        for i, s1 in enumerate(d_secs):
            for s2 in d_secs[i+1:]:
                v1 = dialect_sec_vocab[d][s1]
                v2 = dialect_sec_vocab[d][s2]
                intersection = len(v1 & v2)
                union = len(v1 | v2)
                j = intersection / union if union > 0 else 0
                print(f"    {s1:8s} ∩ {s2:8s}: J={j:.4f}  |∩|={intersection}  |v1|={len(v1)}  |v2|={len(v2)}")

    # Onset-class profile of exclusive vocabulary
    print("\nONSET PROFILE OF EXCLUSIVE VOCABULARY:")
    print(f"{'Onset':<10}", end="")
    for sec in sections:
        print(f"  {sec[:6]:>8s}", end="")
    print()

    all_onsets = list(ONSET_CLASSES.keys()) + ["other"]
    for onset in all_onsets:
        row_vals = []
        for sec in sections:
            others = set()
            for other in sections:
                if other != sec:
                    others |= section_vocab[other]
            exclusive = section_vocab[sec] - others
            if len(exclusive) == 0:
                row_vals.append(0.0)
            else:
                cnt = sum(1 for w in exclusive if get_onset(w) == onset)
                row_vals.append(100 * cnt / len(exclusive))
        if max(row_vals) > 5:
            print(f"{onset:<10}", end="")
            for v in row_vals:
                print(f"  {v:>8.1f}%", end="")
            print()

    # Top high-frequency cross-section shared words
    print("\nMOST SHARED WORDS (appear in all 5 sections):")
    all_shared = section_vocab['herbal']
    for sec in sections[1:]:
        all_shared = all_shared & section_vocab[sec]
    print(f"  Types appearing in all 5 sections: {len(all_shared)}")
    # Sort by total frequency across sections
    shared_freq = [(w, sum(section_word_counts[s][w] for s in sections)) for w in all_shared]
    for w, total_c in sorted(shared_freq, key=lambda x: -x[1])[:20]:
        per_sec = "  ".join(f"{s[:3]}={section_word_counts[s][w]}" for s in sections)
        print(f"  {w:20s}: total={total_c:5d}  [{per_sec}]  onset={get_onset(w)}")

    # 4-of-5 shared words (all except one)
    print("\nWORDS ABSENT FROM EXACTLY ONE SECTION (4/5 shared):")
    for absent_sec in sections:
        others_secs = [s for s in sections if s != absent_sec]
        shared_4 = section_vocab[others_secs[0]]
        for s in others_secs[1:]:
            shared_4 = shared_4 & section_vocab[s]
        shared_4 = shared_4 - section_vocab[absent_sec]
        print(f"  Absent from {absent_sec}: {len(shared_4)} types")
        top4 = sorted([(w, sum(section_word_counts[s][w] for s in others_secs)) for w in shared_4],
                      key=lambda x: -x[1])[:5]
        for w, c in top4:
            print(f"    {w:20s}: freq={c}  onset={get_onset(w)}")


# ─── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Parsing corpus...")
    records = parse_corpus()
    folio_dialect = get_folio_dialect(records)
    print(f"Loaded {len(records)} body-text lines")

    section_counts = Counter(r['section'] for r in records)
    for sec, cnt in sorted(section_counts.items()):
        print(f"  {sec:8s}: {cnt:4d} lines")

    analyze_cosmo_template(records)
    analyze_jaccard_matrix(records, folio_dialect)

    print("\nDone.")
