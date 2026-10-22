"""
exp_137: Paragraph Tail Lines (H269) + Folio-Level Onset Gradient (new H271)

H269: Is "other=97.6%" at para-final a transcription artifact of =Pt tail lines?
      What vocabulary do paragraph tail lines actually contain?
H271: Is there a folio-level onset gradient across the manuscript?
      (Systematic change in onset-class rates as folio number increases)
"""
from pathlib import Path as _RepositoryPath

import re
from collections import defaultdict, Counter
import math

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
    """Parse with prefix_char for line-type info."""
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
            locus_type_raw = parts[1]
            prefix_m = re.match(r'([@+*=~&]+)', locus_type_raw)
            prefix_char = prefix_m.group(1)[0] if prefix_m else ''
            locus_type = locus_type_raw.lstrip('@+*=~&')
            if not re.match(r'P', locus_type):
                continue
            folio_num = get_folio_num(folio_str)
            if folio_num is None:
                continue
            section = SECTION_MAP.get(folio_num)
            if section is None:
                continue
            folio_base = folio_str.split('.')[0]
            # Extract line number within folio
            line_num_m = re.search(r'\.(\d+)$', folio_str)
            line_num = int(line_num_m.group(1)) if line_num_m else 0
            # Raw text (before word parsing)
            raw_text = text
            words = [w for w in text.split('.') if re.match(r'[a-z]', w)]
            records.append({
                'folio': folio_str,
                'folio_base': folio_base,
                'folio_num': folio_num,
                'line_num': line_num,
                'section': section,
                'locus_type': locus_type,
                'prefix_char': prefix_char,
                'raw_text': raw_text,
                'words': words
            })
    return records

def get_folio_dialect(records):
    folio_counts = defaultdict(lambda: {'edy': 0, 'eedy': 0, 'total': 0})
    for rec in records:
        fn = rec['folio_base']
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


# ─── H269: PARAGRAPH TAIL LINES ───────────────────────────────────────────────

def analyze_para_tail(records):
    print("=" * 70)
    print("H269: PARAGRAPH TAIL LINES (=Pt) ANALYSIS")
    print("=" * 70)

    # Classify lines by prefix_char
    lines_by_prefix = defaultdict(list)
    for rec in records:
        lines_by_prefix[rec['prefix_char']].append(rec)

    print("\nLine prefix distribution:")
    for pc in sorted(lines_by_prefix.keys()):
        cnt = len(lines_by_prefix[pc])
        print(f"  '{pc}': {cnt:5d} lines ({100*cnt/len(records):.1f}%)")

    # Focus on = (paragraph tail) vs + (continuation) vs @ (para-start) vs * (para-start-mid)
    tail_recs = lines_by_prefix.get('=', [])
    cont_recs = lines_by_prefix.get('+', [])
    start_recs = lines_by_prefix.get('@', []) + lines_by_prefix.get('*', [])

    print(f"\nTail lines (=): {len(tail_recs)}")
    print(f"Continuation lines (+): {len(cont_recs)}")
    print(f"Para-start lines (@/*): {len(start_recs)}")

    # Word count distribution
    print("\n--- WORD COUNT BY LINE TYPE ---")
    for ltype, recs, label in [
        ('=', tail_recs, "Tail (=)"),
        ('+', cont_recs, "Continuation (+)"),
        ('@/*', start_recs, "Para-start (@/*)"),
    ]:
        if not recs:
            continue
        word_counts = [len(r['words']) for r in recs]
        avg = sum(word_counts) / len(word_counts)
        wc_dist = Counter(word_counts)
        print(f"\n  {label}: mean={avg:.1f} words, n={len(recs)}")
        for wc in sorted(wc_dist.keys())[:8]:
            print(f"    {wc} words: {wc_dist[wc]:4d} lines ({100*wc_dist[wc]/len(recs):.1f}%)")

    # Check for <$> markers in tail lines
    print("\n--- TRANSCRIPTION MARKER ANALYSIS ---")
    for label, recs in [("Tail (=)", tail_recs), ("Continuation (+)", cont_recs)]:
        dollar_end = sum(1 for r in recs if '<$>' in r['raw_text'])
        total = len(recs)
        print(f"\n  {label}: {dollar_end}/{total} ({100*dollar_end/max(total,1):.1f}%) contain <$>")
        # What tokens appear at end of tail lines?
        end_tokens = Counter()
        for r in recs:
            if r['raw_text']:
                # Last space-separated token
                last_token = r['raw_text'].split()[-1] if r['raw_text'].split() else ''
                end_tokens[last_token] += 1
        print(f"  Top ending tokens:")
        for tok, cnt in end_tokens.most_common(10):
            print(f"    {tok:25s}: {cnt:4d}")

    # Suffix distribution: tail vs continuation
    print("\n--- SUFFIX DISTRIBUTION: TAIL vs CONTINUATION ---")
    def compute_suffix_profile(recs):
        suf_counts = Counter()
        total = 0
        for rec in recs:
            for w in rec['words']:
                suf_counts[get_suffix(w)] += 1
                total += 1
        return suf_counts, total

    tail_suf, tail_total = compute_suffix_profile(tail_recs)
    cont_suf, cont_total = compute_suffix_profile(cont_recs)

    print(f"\n{'Suffix':<12} {'Tail%':>8} {'Cont%':>8} {'Ratio':>8}")
    for suf in sorted(SUFFIXES + ['other'], key=lambda s: -(tail_suf.get(s,0)/max(tail_total,1))):
        t_pct = 100 * tail_suf.get(suf, 0) / max(tail_total, 1)
        c_pct = 100 * cont_suf.get(suf, 0) / max(cont_total, 1)
        ratio = t_pct / c_pct if c_pct > 0 else 0
        if t_pct > 0.5 or c_pct > 0.5:
            print(f"-{suf:<11} {t_pct:>8.1f}% {c_pct:>8.1f}% {ratio:>8.2f}×")

    # Onset distribution: tail vs continuation
    print("\n--- ONSET DISTRIBUTION: TAIL vs CONTINUATION ---")
    def compute_onset_profile(recs):
        onset_counts = Counter()
        total = 0
        for rec in recs:
            for w in rec['words']:
                onset_counts[get_onset(w)] += 1
                total += 1
        return onset_counts, total

    tail_onset, tail_ototal = compute_onset_profile(tail_recs)
    cont_onset, cont_ototal = compute_onset_profile(cont_recs)

    print(f"\n{'Onset':<10} {'Tail%':>8} {'Cont%':>8} {'Ratio':>8}")
    for onset in sorted(list(ONSET_CLASSES.keys()) + ['other'],
                        key=lambda o: -(tail_onset.get(o,0)/max(tail_ototal,1))):
        t_pct = 100 * tail_onset.get(onset, 0) / max(tail_ototal, 1)
        c_pct = 100 * cont_onset.get(onset, 0) / max(cont_ototal, 1)
        ratio = t_pct / c_pct if c_pct > 0 else 0
        print(f"{onset:<10} {t_pct:>8.1f}% {c_pct:>8.1f}% {ratio:>8.2f}×")

    # LINE-FINAL suffix for tail lines (excluding <$>-terminated)
    print("\n--- TAIL LINE LAST-WORD SUFFIX (EXCL. <$>-TERMINAL) ---")
    tail_no_dollar = [r for r in tail_recs if '<$>' not in r['raw_text']]
    print(f"  Tail lines without <$>: {len(tail_no_dollar)}/{len(tail_recs)}")
    last_word_suf = Counter()
    last_word_words = Counter()
    for rec in tail_no_dollar:
        if rec['words']:
            lw = rec['words'][-1]
            last_word_suf[get_suffix(lw)] += 1
            last_word_words[lw] += 1
    total_nodollar = len(tail_no_dollar)
    print(f"\n  Last-word suffix profile (excl <$>):")
    for suf, cnt in sorted(last_word_suf.items(), key=lambda x: -x[1]):
        print(f"    -{suf:<10}: {cnt:4d} ({100*cnt/max(total_nodollar,1):.1f}%)")
    print(f"\n  Top last words in non-<$> tail lines:")
    for w, c in last_word_words.most_common(15):
        print(f"    {w:20s}: {c:4d}  onset={get_onset(w)} suffix={get_suffix(w)}")

    # Section distribution of tail lines
    print("\n--- SECTION DISTRIBUTION OF TAIL LINES ---")
    section_tail = Counter(r['section'] for r in tail_recs)
    section_cont = Counter(r['section'] for r in cont_recs)
    section_start = Counter(r['section'] for r in start_recs)
    for sec in ["herbal", "astro", "cosmo", "pharma", "stars"]:
        t = section_tail.get(sec, 0)
        c = section_cont.get(sec, 0)
        s = section_start.get(sec, 0)
        total_sec = t + c + s
        print(f"  {sec:8s}: tail={t:4d} ({100*t/max(total_sec,1):.1f}%)  cont={c:4d} ({100*c/max(total_sec,1):.1f}%)  start={s:4d} ({100*s/max(total_sec,1):.1f}%)")


# ─── H271: FOLIO-LEVEL ONSET GRADIENT ─────────────────────────────────────────

def analyze_folio_gradient(records, folio_dialect):
    print("\n" + "=" * 70)
    print("H271: FOLIO-LEVEL ONSET GRADIENT")
    print("=" * 70)

    # Build per-folio onset profiles
    folio_onset_counts = defaultdict(Counter)
    folio_word_totals = Counter()

    for rec in records:
        fn = rec['folio_num']
        for w in rec['words']:
            folio_onset_counts[fn][get_onset(w)] += 1
            folio_word_totals[fn] += 1

    # Compute per-folio rates for key onset classes
    # Only folios with ≥50 words
    valid_folios = sorted([fn for fn in folio_word_totals if folio_word_totals[fn] >= 50])
    print(f"\nValid folios (≥50 words): {len(valid_folios)}")

    # Compute rates for key onset classes
    key_onsets = ['qok', 'cth', 'd', 'sh', 'ol', 's', 'l', 'ot', 'ch', 'ok']

    # Print folio-by-folio table for key onsets
    print(f"\n{'Folio':>6} {'Section':>8} {'D':>5} {'N':>5}", end="")
    for onset in key_onsets:
        print(f" {onset:>6}", end="")
    print()

    folio_rates = {}
    for fn in valid_folios:
        total = folio_word_totals[fn]
        folio_base = f"f{fn}r"  # approximate
        d = folio_dialect.get(f"f{fn}r", folio_dialect.get(f"f{fn}v", '?'))
        sec = SECTION_MAP.get(fn, '?')[:3]
        rates = {}
        for onset in key_onsets:
            rates[onset] = folio_onset_counts[fn].get(onset, 0) / total
        folio_rates[fn] = rates
        row = f"{fn:>6} {sec:>8} {d:>5} {total:>5}"
        for onset in key_onsets:
            row += f" {100*rates[onset]:>5.1f}"
        print(row)

    # Compute correlations with folio number for each onset class
    print("\n\n--- CORRELATION OF ONSET RATE WITH FOLIO NUMBER ---")
    print("(Spearman rank correlation, pooled across all sections)")

    def spearman_rho(xs, ys):
        """Spearman rank correlation."""
        n = len(xs)
        if n < 3:
            return 0
        ranked_x = sorted(range(n), key=lambda i: xs[i])
        ranked_y = sorted(range(n), key=lambda i: ys[i])
        rank_x = [0] * n
        rank_y = [0] * n
        for rank, i in enumerate(ranked_x):
            rank_x[i] = rank
        for rank, i in enumerate(ranked_y):
            rank_y[i] = rank
        d_sq = sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n))
        rho = 1 - 6 * d_sq / (n * (n * n - 1))
        return rho

    folio_nums = valid_folios
    for onset in key_onsets:
        rates = [folio_rates[fn][onset] for fn in folio_nums]
        rho = spearman_rho(list(range(len(folio_nums))), rates)
        print(f"  {onset:6s}: ρ={rho:+.3f}")

    # Separate by section to control for section effect
    print("\n--- WITHIN-SECTION FOLIO GRADIENT ---")
    for sec_name, fn_range in [
        ("herbal", range(1, 58)),
        ("cosmo", range(75, 85)),
        ("pharma", range(87, 103)),
        ("stars", range(103, 117)),
    ]:
        sec_folios = [fn for fn in fn_range if fn in folio_rates]
        if len(sec_folios) < 4:
            continue
        print(f"\n  {sec_name.upper()} (n={len(sec_folios)} folios):")
        for onset in key_onsets:
            rates = [folio_rates[fn][onset] for fn in sec_folios]
            rho = spearman_rho(list(range(len(sec_folios))), rates)
            if abs(rho) > 0.3:
                print(f"    {onset:6s}: ρ={rho:+.3f} (NOTABLE)")

    # Moving window analysis: 10-folio running average for most interesting onsets
    print("\n--- 10-FOLIO RUNNING MEAN FOR KEY ONSETS ---")
    print(f"{'Folio range':>15}", end="")
    running_onsets = ['cth', 'ol', 'l', 'qok', 'd']
    for onset in running_onsets:
        print(f"  {onset:>6}", end="")
    print()

    window = 10
    for i in range(len(valid_folios) - window + 1):
        window_folios = valid_folios[i:i+window]
        folio_range = f"{window_folios[0]}-{window_folios[-1]}"
        # Aggregate rates across window
        window_totals = sum(folio_word_totals[fn] for fn in window_folios)
        window_onset_counts = Counter()
        for fn in window_folios:
            for onset in running_onsets:
                window_onset_counts[onset] += folio_onset_counts[fn].get(onset, 0)
        row = f"{folio_range:>15}"
        for onset in running_onsets:
            rate = 100 * window_onset_counts[onset] / max(window_totals, 1)
            row += f"  {rate:>5.1f}"
        print(row)

    # Folio-level "section mismatch" analysis: which folios have the most unusual onset profiles?
    print("\n--- FOLIO-LEVEL ONSET DEVIATION FROM SECTION CENTROID ---")
    # Compute section centroids
    section_onset_counts = defaultdict(Counter)
    section_word_totals = Counter()
    for rec in records:
        sec = rec['section']
        for w in rec['words']:
            section_onset_counts[sec][get_onset(w)] += 1
            section_word_totals[sec] += 1

    section_centroids = {}
    for sec in section_onset_counts:
        total = section_word_totals[sec]
        section_centroids[sec] = {onset: section_onset_counts[sec].get(onset, 0) / total
                                   for onset in list(ONSET_CLASSES.keys()) + ['other']}

    # Compute per-folio deviation from its section centroid
    all_onsets = list(ONSET_CLASSES.keys()) + ['other']
    folio_deviations = {}
    for fn in valid_folios:
        sec = SECTION_MAP.get(fn)
        if sec is None:
            continue
        centroid = section_centroids.get(sec, {})
        total = folio_word_totals[fn]
        folio_vec = {onset: folio_onset_counts[fn].get(onset, 0) / total for onset in all_onsets}
        # Euclidean distance from centroid
        deviation = math.sqrt(sum((folio_vec.get(o, 0) - centroid.get(o, 0)) ** 2 for o in all_onsets))
        folio_deviations[fn] = deviation

    print("\nTop 15 most deviant folios from their section centroid:")
    for fn, dev in sorted(folio_deviations.items(), key=lambda x: -x[1])[:15]:
        sec = SECTION_MAP.get(fn, '?')
        folio_base_approx = f"f{fn}"
        d = folio_dialect.get(f"f{fn}r", folio_dialect.get(f"f{fn}v", '?'))
        total = folio_word_totals[fn]
        # Most deviant onset classes
        centroid = section_centroids.get(sec, {})
        total_fn = folio_word_totals[fn]
        folio_vec = {onset: folio_onset_counts[fn].get(onset, 0) / total_fn for onset in all_onsets}
        devs = sorted([(o, folio_vec.get(o, 0) - centroid.get(o, 0)) for o in all_onsets],
                      key=lambda x: -abs(x[1]))
        top_devs = ", ".join(f"{o}:{100*d:+.1f}%" for o, d in devs[:3])
        print(f"  f{fn:>3} ({sec:6s}, {d}): dev={dev:.4f}  n={total}  [{top_devs}]")

    print("\nMost TYPICAL folios (lowest deviation from section centroid):")
    for fn, dev in sorted(folio_deviations.items(), key=lambda x: x[1])[:10]:
        sec = SECTION_MAP.get(fn, '?')
        d = folio_dialect.get(f"f{fn}r", folio_dialect.get(f"f{fn}v", '?'))
        print(f"  f{fn:>3} ({sec:6s}, {d}): dev={dev:.4f}  n={folio_word_totals[fn]}")


# ─── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Parsing corpus...")
    records = parse_corpus()
    folio_dialect = get_folio_dialect(records)
    print(f"Loaded {len(records)} body-text lines")

    analyze_para_tail(records)
    analyze_folio_gradient(records, folio_dialect)

    print("\nDone.")
