"""
exp_126: cth-Onset Vocabulary (H245) + Within-Line Suffix Grammar (H246)
=========================================================================
H245: Is cth a closed class (small vocab, high hapax) or open class (large vocab, productive)?
      Compare cth to ch, sh, qok, ok in: type count, hapax rate, section specialization,
      top-word coverage, and per-section vocabulary diversity.

H246: Within-line suffix grammar — does suffix sequence within a line show systematic order?
      Test: -ol before -aiin; suffix bigrams within lines; suffix positional enrichment by
      line-fraction; entropy by fractional position. Compare A and B dialect.
"""
from pathlib import Path as _RepositoryPath

import re
import sys
from collections import defaultdict, Counter

# ── parser (canonical EVA ZL3b IVTFF format) ────────────────────────────────

SUFFIXES = ['eeedy','eeey','eedy','edy','eey','aiin','ain','air','am',
            'ol','or','ar','al','ey','dy','y']

def get_suffix(word):
    for s in SUFFIXES:
        if word.endswith(s) and len(word) > len(s):
            return s
    return 'other'

SECTION_MAP = {}
for f in range(1,   58): SECTION_MAP[f] = 'herbal'
for f in range(67,  74): SECTION_MAP[f] = 'astro'
for f in range(75,  85): SECTION_MAP[f] = 'cosmo'
for f in range(87, 103): SECTION_MAP[f] = 'pharma'
for f in range(103,117): SECTION_MAP[f] = 'stars'

def get_section(folio_num):
    return SECTION_MAP.get(folio_num, 'other')

def parse_folio_num(locus):
    m = re.match(r'f(\d+)', locus)
    return int(m.group(1)) if m else None

def is_dialect_b(folio_num, dialect_cache):
    return dialect_cache.get(folio_num, False)

def get_onset(word):
    for pat in ['qok','qot','qo','cth','ch','sh','ok','ot','ol','olk','d','s']:
        if word.startswith(pat):
            return pat
    if len(word) >= 1 and word[0] in 'yklrtpf':
        return word[0]
    return 'other'

def parse_corpus(path):
    """Returns list of line_records: each is a dict with folio_num, section, line_id,
    words (in order), dialect (set after first pass)."""
    raw_lines = []
    folio_word_counts = defaultdict(lambda: Counter())

    with open(path, encoding='utf-8') as fh:
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
                continue  # body text only
            # Clean text: remove inline markup, special chars, annotations
            text = re.sub(r'<[^>]*>', '', text_raw)     # remove <...> tags
            text = re.sub(r'\[[^\]]*\]', ' ', text)     # remove [...]
            text = re.sub(r'![\w.;@]*', '', text)       # remove !... annotations
            text = re.sub(r'<%[^>]*>', '', text)        # remove <% markers
            text = re.sub(r'[*@&~=+$#{}?]', '', text)  # strip special chars
            words = [w for w in re.split(r'[-.\s,]+', text)
                     if re.match(r'^[a-z]{2,}$', w)]
            if words:
                raw_lines.append((locus, folio_num, words))
                for w in words:
                    # track edy/eedy rate per folio for dialect detection
                    folio_word_counts[folio_num][w] += 1

    # dialect detection: folio-level edy/eedy rate >= 5% → B
    dialect_b = {}
    for fnum, cnt in folio_word_counts.items():
        total = sum(cnt.values())
        edy_count = sum(v for w, v in cnt.items() if w.endswith('edy') or w.endswith('eedy'))
        dialect_b[fnum] = (edy_count / total >= 0.05) if total > 0 else False

    # build records
    records = []
    for locus, folio_num, words in raw_lines:
        dialect = 'B' if dialect_b.get(folio_num, False) else 'A'
        section = get_section(folio_num)
        records.append({
            'locus': locus,
            'folio_num': folio_num,
            'dialect': dialect,
            'section': section,
            'words': words,
        })
    return records

# ── H245: cth-Onset Vocabulary Analysis ─────────────────────────────────────

def analyze_onset_vocab(records):
    """For each onset class, compute: total tokens, types, hapax rate, section distribution,
    top-N word coverage, per-section type count."""
    onset_tokens   = defaultdict(list)  # onset → [word, ...]
    onset_section  = defaultdict(lambda: Counter())

    for rec in records:
        for w in rec['words']:
            o = get_onset(w)
            onset_tokens[o].append(w)
            onset_section[o][rec['section']] += 1

    focal_onsets = ['cth', 'ch', 'sh', 'qok', 'ok', 'ot', 'qot', 'd']
    sections = ['herbal', 'astro', 'cosmo', 'pharma', 'stars']

    print("=" * 70)
    print("H245: cth-ONSET VOCABULARY — CLOSED vs OPEN CLASS")
    print("=" * 70)

    header = f"{'Onset':<8} {'Tokens':>7} {'Types':>6} {'Hapax%':>7} {'Top10%':>7} {'Top5%':>7}"
    print(header)
    print("-" * 50)

    results = {}
    for o in focal_onsets:
        tokens = onset_tokens[o]
        if not tokens:
            continue
        n = len(tokens)
        cnt = Counter(tokens)
        types = len(cnt)
        hapax = sum(1 for v in cnt.values() if v == 1)
        hapax_rate = hapax / types if types > 0 else 0
        top5 = sum(v for _, v in cnt.most_common(5))
        top10 = sum(v for _, v in cnt.most_common(10))
        results[o] = {'n': n, 'types': types, 'hapax_rate': hapax_rate,
                      'top5_frac': top5/n, 'top10_frac': top10/n, 'cnt': cnt}
        print(f"{o:<8} {n:>7,} {types:>6,} {hapax_rate:>6.1%} {top10/n:>6.1%} {top5/n:>6.1%}")

    print()
    print("Section distribution (% of onset tokens in section):")
    print(f"{'Onset':<8} " + " ".join(f"{s[:7]:>7}" for s in sections))
    print("-" * 50)
    for o in focal_onsets:
        if o not in results:
            continue
        n = results[o]['n']
        row = " ".join(f"{onset_section[o].get(s,0)/n:>6.1%}" for s in sections)
        print(f"{o:<8} {row}")

    print()
    print("Top 15 cth-onset words:")
    cth_cnt = results.get('cth', {}).get('cnt', Counter())
    for w, c in cth_cnt.most_common(15):
        print(f"  {w:<20} {c:>5}")

    print()
    print("cth per-section vocabulary (types, tokens):")
    cth_section_vocab = defaultdict(Counter)
    for rec in records:
        for w in rec['words']:
            if get_onset(w) == 'cth':
                cth_section_vocab[rec['section']][w] += 1
    for sec in sections:
        cnt = cth_section_vocab[sec]
        total = sum(cnt.values())
        types = len(cnt)
        if total > 0:
            hapax = sum(1 for v in cnt.values() if v == 1)
            print(f"  {sec:<10}: {types:>4} types, {total:>5} tokens, "
                  f"hapax={hapax/types:.1%}, "
                  f"top5={sum(v for _,v in cnt.most_common(5))/total:.1%}")

    print()
    print("cth vocabulary by dialect (A vs B types):")
    cth_dial_vocab = defaultdict(Counter)
    for rec in records:
        for w in rec['words']:
            if get_onset(w) == 'cth':
                cth_dial_vocab[rec['dialect']][w] += 1
    for d in ['A', 'B']:
        cnt = cth_dial_vocab[d]
        n = sum(cnt.values())
        types = len(cnt)
        shared_with_other = d  # placeholder
        print(f"  Dialect {d}: {types} types, {n} tokens, top: "
              + ", ".join(f"{w}({c})" for w, c in cnt.most_common(5)))

    # Jaccard between A and B cth vocabularies
    a_types = set(cth_dial_vocab['A'].keys())
    b_types = set(cth_dial_vocab['B'].keys())
    j = len(a_types & b_types) / len(a_types | b_types) if (a_types | b_types) else 0
    print(f"  A∩B cth Jaccard = {j:.3f} ({len(a_types & b_types)} shared types)")
    print(f"  A-exclusive cth types: {sorted(a_types - b_types)[:15]}")
    print(f"  B-exclusive cth types: {sorted(b_types - a_types)[:15]}")

    return results

# ── H246: Within-Line Suffix Grammar ─────────────────────────────────────────

def analyze_suffix_grammar(records):
    """Test within-line suffix ordering: -ol before -aiin, suffix bigrams, positional enrichment."""
    print()
    print("=" * 70)
    print("H246: WITHIN-LINE SUFFIX GRAMMAR")
    print("=" * 70)

    suffixes_of_interest = ['ol','or','aiin','ain','edy','eedy','ey','dy','al','ar','am','y','other']

    # 1. Suffix bigrams within lines (what suffix follows what suffix?)
    suf_bigrams = defaultdict(Counter)
    suf_counts  = Counter()

    # 2. Within-line -ol before -aiin test
    ol_before_aiin = 0
    aiin_before_ol = 0
    lines_with_both = 0

    # 3. Positional enrichment by line fraction (split into 5 bins: 0-0.2, 0.2-0.4, ..., 0.8-1.0)
    N_BINS = 5
    suf_pos_A = [Counter() for _ in range(N_BINS)]
    suf_pos_B = [Counter() for _ in range(N_BINS)]

    # 4. Suffix sequence by dialect
    for rec in records:
        words = rec['words']
        n = len(words)
        if n < 2:
            continue
        suffs = [get_suffix(w) for w in words]
        d = rec['dialect']

        # bigrams
        for i in range(len(suffs) - 1):
            suf_bigrams[suffs[i]][suffs[i+1]] += 1
            suf_counts[suffs[i]] += 1

        # -ol before -aiin
        has_ol   = 'ol' in suffs
        has_aiin = 'aiin' in suffs
        if has_ol and has_aiin:
            lines_with_both += 1
            first_ol   = suffs.index('ol')
            first_aiin = suffs.index('aiin')
            if first_ol < first_aiin:
                ol_before_aiin += 1
            else:
                aiin_before_ol += 1

        # positional enrichment
        for i, s in enumerate(suffs):
            frac = i / n
            b = min(int(frac * N_BINS), N_BINS - 1)
            if d == 'A':
                suf_pos_A[b][s] += 1
            else:
                suf_pos_B[b][s] += 1

    # Print suffix bigrams (top pairs, enrichment)
    print("\nSuffix bigram enrichment within lines (obs/baseline, n≥50):")
    total_suf_tokens = sum(suf_counts.values())
    suf_base = {s: suf_counts[s] / total_suf_tokens for s in suf_counts}
    print(f"{'From\\To':<8} " + " ".join(f"{s[:5]:>6}" for s in suffixes_of_interest))
    for s1 in ['ol','or','aiin','ain','edy','ey','dy','y','other']:
        row_total = sum(suf_bigrams[s1].values())
        if row_total < 20:
            continue
        vals = []
        for s2 in suffixes_of_interest:
            obs = suf_bigrams[s1].get(s2, 0)
            base = suf_base.get(s2, 0)
            if base > 0 and row_total >= 20:
                enrich = (obs / row_total) / base
                vals.append(f"{enrich:>6.2f}")
            else:
                vals.append("    —")
        print(f"{s1:<8} " + " ".join(vals))

    print(f"\n-ol BEFORE -aiin test (lines with both -ol and -aiin words):")
    print(f"  Lines with both: {lines_with_both}")
    if lines_with_both > 0:
        print(f"  ol before aiin: {ol_before_aiin} ({ol_before_aiin/lines_with_both:.1%})")
        print(f"  aiin before ol: {aiin_before_ol} ({aiin_before_ol/lines_with_both:.1%})")

    # Positional enrichment table
    bin_labels = ['0-20%', '20-40%', '40-60%', '60-80%', '80-100%']
    for dialect, pos_data in [('A', suf_pos_A), ('B', suf_pos_B)]:
        print(f"\nSuffix positional enrichment within line (dialect {dialect}):")
        bin_totals = [sum(b.values()) for b in pos_data]
        total_all = sum(bin_totals)
        if total_all == 0:
            continue
        # baseline: overall suffix rate across all positions in this dialect
        overall_suf = Counter()
        for b in pos_data:
            overall_suf.update(b)
        overall_total = sum(overall_suf.values())
        suf_baseline = {s: overall_suf[s] / overall_total for s in overall_suf}

        focal_suffs = ['ol','or','aiin','ain','edy','ey','dy','y','al','ar']
        print(f"  {'Suffix':<8} " + " ".join(f"{bl:>7}" for bl in bin_labels))
        for s in focal_suffs:
            row = []
            for i, b in enumerate(pos_data):
                bt = bin_totals[i]
                obs = b.get(s, 0)
                base = suf_baseline.get(s, 0)
                if bt > 0 and base > 0:
                    enrich = (obs / bt) / base
                    row.append(f"{enrich:>7.2f}")
                else:
                    row.append("      —")
            print(f"  {s:<8} " + " ".join(row))

    # Suffix sequence order test: rank suffixes by mean position within line
    print(f"\nMean within-line position of suffix class (0=first, 1=last):")
    suf_positions_A = defaultdict(list)
    suf_positions_B = defaultdict(list)
    for rec in records:
        words = rec['words']
        n = len(words)
        if n < 2:
            continue
        for i, w in enumerate(words):
            s = get_suffix(w)
            frac = i / (n - 1) if n > 1 else 0.5
            if rec['dialect'] == 'A':
                suf_positions_A[s].append(frac)
            else:
                suf_positions_B[s].append(frac)

    print(f"  {'Suffix':<8} {'A mean':>8} {'A n':>6} {'B mean':>8} {'B n':>6}")
    for s in ['ol','or','aiin','ain','edy','eedy','ey','dy','al','ar','am','y','other']:
        a_pos = suf_positions_A.get(s, [])
        b_pos = suf_positions_B.get(s, [])
        a_mean = sum(a_pos) / len(a_pos) if a_pos else float('nan')
        b_mean = sum(b_pos) / len(b_pos) if b_pos else float('nan')
        print(f"  {s:<8} {a_mean:>8.3f} {len(a_pos):>6,} {b_mean:>8.3f} {len(b_pos):>6,}")


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    corpus_path = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

    print(f"Loading corpus from {corpus_path}...")
    records = parse_corpus(corpus_path)
    total_words = sum(len(r['words']) for r in records)
    print(f"Loaded {len(records)} lines, {total_words:,} word tokens")

    analyze_onset_vocab(records)
    analyze_suffix_grammar(records)
