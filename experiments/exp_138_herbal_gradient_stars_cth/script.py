"""
exp_138: Within-Herbal cth Gradient Analysis (H272) + Stars cth Anomaly (H273) + f47 Profile (H274)

H272: Is the within-herbal cth gradient (ρ=-0.486) due to B-insertions or A-herbal scribal shift?
H273: Why does cth INCREASE within stars (ρ=+0.469)? Which folios drive it?
H274: What is the full profile of f47 (most deviant A-herbal folio, ch:+20%)?
"""

import re
from collections import defaultdict, Counter
import math

CORPUS_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"

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
            locus_type_raw = parts[1]
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
            words = [w for w in text.split('.') if re.match(r'[a-z]', w)]
            records.append({
                'folio': folio_str,
                'folio_base': folio_base,
                'folio_num': folio_num,
                'section': section,
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

def spearman_rho(xs, ys):
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

def build_folio_profiles(records):
    """Build per-folio onset/suffix/word counts."""
    folio_onset = defaultdict(Counter)
    folio_suffix = defaultdict(Counter)
    folio_words = defaultdict(Counter)
    folio_total = Counter()

    for rec in records:
        fn = rec['folio_num']
        for w in rec['words']:
            folio_onset[fn][get_onset(w)] += 1
            folio_suffix[fn][get_suffix(w)] += 1
            folio_words[fn][w] += 1
            folio_total[fn] += 1

    return folio_onset, folio_suffix, folio_words, folio_total


# ─── H272: WITHIN-HERBAL cth GRADIENT ─────────────────────────────────────────

def analyze_herbal_gradient(records, folio_dialect):
    print("=" * 70)
    print("H272: WITHIN-HERBAL cth GRADIENT (B-insertion artifact vs scribal shift?)")
    print("=" * 70)

    folio_onset, folio_suffix, folio_words, folio_total = build_folio_profiles(records)

    herbal_folios = sorted([fn for fn in folio_total if SECTION_MAP.get(fn) == 'herbal' and folio_total[fn] >= 50])

    # Classify herbal folios by dialect
    def get_folio_dialect_key(fn):
        # Try f{n}r first, then f{n}v
        for suffix in ['r', 'v']:
            key = f"f{fn}{suffix}"
            if key in folio_dialect:
                return folio_dialect[key]
        return 'unknown'

    a_herbal = [fn for fn in herbal_folios if get_folio_dialect_key(fn) == 'A']
    b_herbal = [fn for fn in herbal_folios if get_folio_dialect_key(fn) == 'B']

    print(f"\nHerbal folios with ≥50 words: {len(herbal_folios)}")
    print(f"  A-dialect: {len(a_herbal)} folios: {a_herbal}")
    print(f"  B-dialect: {len(b_herbal)} folios: {b_herbal}")

    # Compute cth rate per folio
    print("\n--- Cth RATE BY FOLIO (HERBAL) ---")
    print(f"{'Folio':>6} {'D':>3} {'Total':>6} {'cth%':>7} {'ch%':>7} {'d%':>7} {'qok%':>7} {'l%':>7}")
    for fn in herbal_folios:
        d = get_folio_dialect_key(fn)
        total = folio_total[fn]
        cth = 100 * folio_onset[fn].get('cth', 0) / total
        ch = 100 * folio_onset[fn].get('ch', 0) / total
        d_rate = 100 * folio_onset[fn].get('d', 0) / total
        qok = 100 * folio_onset[fn].get('qok', 0) / total
        l = 100 * folio_onset[fn].get('l', 0) / total
        marker = " ←B" if d == 'B' else ""
        print(f"{fn:>6} {d:>3} {total:>6} {cth:>7.1f} {ch:>7.1f} {d_rate:>7.1f} {qok:>7.1f} {l:>7.1f}{marker}")

    # Gradient analysis: all herbal vs A-herbal-only vs B-herbal-only
    print("\n--- SPEARMAN ρ WITH FOLIO NUMBER ---")
    for label, folios in [
        ("ALL herbal", herbal_folios),
        ("A-herbal only", a_herbal),
        ("B-herbal only", b_herbal),
    ]:
        if len(folios) < 4:
            print(f"  {label}: too few folios ({len(folios)})")
            continue
        folio_rank = list(range(len(folios)))
        for onset in ['cth', 'ch', 'd', 'qok', 'l', 'ok']:
            rates = [folio_onset[fn].get(onset, 0) / folio_total[fn] for fn in folios]
            rho = spearman_rho(folio_rank, rates)
            if abs(rho) > 0.2:
                print(f"  {label} {onset}: ρ={rho:+.3f}")

    # Early vs late herbal comparison (by folio number, within each dialect)
    print("\n--- EARLY (f1-f28) vs LATE (f29-f57) HERBAL RATES ---")
    early_cutoff = 28
    for d_label, d_folios in [("A-herbal", a_herbal), ("B-herbal", b_herbal), ("All herbal", herbal_folios)]:
        early = [fn for fn in d_folios if fn <= early_cutoff]
        late = [fn for fn in d_folios if fn > early_cutoff]
        if not early or not late:
            continue
        print(f"\n  {d_label}: early n={len(early)}, late n={len(late)}")
        for onset in ['cth', 'ch', 'd', 'qok', 'l']:
            early_rate = sum(folio_onset[fn].get(onset, 0) for fn in early) / max(sum(folio_total[fn] for fn in early), 1)
            late_rate = sum(folio_onset[fn].get(onset, 0) for fn in late) / max(sum(folio_total[fn] for fn in late), 1)
            ratio = late_rate / early_rate if early_rate > 0 else 0
            print(f"    {onset:4s}: early={100*early_rate:.1f}%  late={100*late_rate:.1f}%  ratio={ratio:.2f}×")

    # Top cth words by herbal folio range
    print("\n--- TOP cth WORDS IN EARLY vs LATE HERBAL ---")
    early_cth_words = Counter()
    late_cth_words = Counter()
    for rec in records:
        if rec['section'] != 'herbal':
            continue
        fn = rec['folio_num']
        for w in rec['words']:
            if get_onset(w) == 'cth':
                if fn <= early_cutoff:
                    early_cth_words[w] += 1
                else:
                    late_cth_words[w] += 1

    print("  Early herbal (f1-28) top cth words:")
    for w, c in early_cth_words.most_common(10):
        print(f"    {w:20s}: {c:4d}")
    print("  Late herbal (f29-57) top cth words:")
    for w, c in late_cth_words.most_common(10):
        print(f"    {w:20s}: {c:4d}")


# ─── H273: STARS cth ANOMALY ──────────────────────────────────────────────────

def analyze_stars_cth(records, folio_dialect):
    print("\n" + "=" * 70)
    print("H273: STARS cth ANOMALY — Per-Folio Analysis")
    print("=" * 70)

    folio_onset, folio_suffix, folio_words, folio_total = build_folio_profiles(records)

    stars_folios = sorted([fn for fn in folio_total if SECTION_MAP.get(fn) == 'stars' and folio_total[fn] >= 50])

    print("\n--- PER-FOLIO Cth/CH RATES IN STARS ---")
    print(f"{'Folio':>6} {'Total':>6} {'cth%':>7} {'ch%':>7} {'ch_e%':>7} {'cth tokens':>12}")
    cth_word_totals = Counter()
    for fn in stars_folios:
        total = folio_total[fn]
        cth_pct = 100 * folio_onset[fn].get('cth', 0) / total
        ch_pct = 100 * folio_onset[fn].get('ch', 0) / total
        ch_e_pct = 100 * folio_onset[fn].get('ch_e', 0) / total
        cth_tokens = folio_onset[fn].get('cth', 0)
        print(f"{fn:>6} {total:>6} {cth_pct:>7.2f} {ch_pct:>7.1f} {ch_e_pct:>7.1f} {cth_tokens:>12}")
        # Accumulate cth words
        for w, c in folio_words[fn].items():
            if get_onset(w) == 'cth':
                cth_word_totals[w] += c

    # Gradient within stars
    print("\n--- GRADIENT WITHIN STARS ---")
    folio_rank = list(range(len(stars_folios)))
    for onset in ['cth', 'ch', 'ch_e', 'd', 'l', 'ok', 'qok']:
        rates = [folio_onset[fn].get(onset, 0) / folio_total[fn] for fn in stars_folios]
        rho = spearman_rho(folio_rank, rates)
        print(f"  {onset:6s}: ρ={rho:+.3f}")

    # What cth words appear in stars?
    print("\n--- Cth WORDS IN STARS ---")
    print(f"Total cth tokens in stars: {sum(cth_word_totals.values())}")
    for w, c in cth_word_totals.most_common(20):
        # Check dialect of this word
        print(f"  {w:20s}: {c:4d}")

    # Are these B-cth hybrid forms (cthedy/cthdy from F132)?
    print("\n--- Cth WORD SUFFIX ANALYSIS IN STARS ---")
    suf_counts = Counter()
    for w, c in cth_word_totals.items():
        suf_counts[get_suffix(w)] += c
    for suf, c in sorted(suf_counts.items(), key=lambda x: -x[1]):
        print(f"  -{suf}: {c}")

    # Which specific later stars folios drive the increase?
    print("\n--- EARLY (f103-109) vs LATE (f110-116) STARS cth RATES ---")
    early_stars = [fn for fn in stars_folios if fn <= 109]
    late_stars = [fn for fn in stars_folios if fn > 109]

    def section_rate(folios, onset):
        total_cnt = sum(folio_total[fn] for fn in folios)
        onset_cnt = sum(folio_onset[fn].get(onset, 0) for fn in folios)
        return onset_cnt / max(total_cnt, 1)

    print(f"  Early stars (f103-109, n={len(early_stars)}): cth={100*section_rate(early_stars,'cth'):.2f}%  ch={100*section_rate(early_stars,'ch'):.1f}%")
    print(f"  Late stars  (f110-116, n={len(late_stars)}): cth={100*section_rate(late_stars,'cth'):.2f}%  ch={100*section_rate(late_stars,'ch'):.1f}%")

    # Check if late stars folios' cth words are B-cth forms
    late_cth_words = Counter()
    for fn in late_stars:
        for w, c in folio_words[fn].items():
            if get_onset(w) == 'cth':
                late_cth_words[w] += c
    print(f"\n  CthWords in late stars: {sum(late_cth_words.values())} tokens")
    for w, c in late_cth_words.most_common(15):
        print(f"    {w:20s}: {c}  suf={get_suffix(w)}")


# ─── H274: f47 PROFILE ────────────────────────────────────────────────────────

def analyze_f47(records, folio_dialect):
    print("\n" + "=" * 70)
    print("H274: f47 FULL PROFILE (Most Deviant A-Herbal Folio)")
    print("=" * 70)

    folio_onset, folio_suffix, folio_words, folio_total = build_folio_profiles(records)

    # f47 profile
    fn47 = 47
    total = folio_total[fn47]
    print(f"\nf47: {total} words")

    print("\n--- ONSET PROFILE ---")
    print(f"{'Onset':>8} {'f47%':>8} {'A-her%':>10} {'Ratio':>8}")

    # Compute A-herbal centroid
    def get_folio_dialect_key2(fn):
        for suffix in ['r', 'v']:
            key = f"f{fn}{suffix}"
            if key in folio_dialect:
                return folio_dialect[key]
        return 'unknown'

    a_herbal_folios = [fn for fn in folio_total if SECTION_MAP.get(fn) == 'herbal' and get_folio_dialect_key2(fn) == 'A' and fn != 47]
    a_total = sum(folio_total[fn] for fn in a_herbal_folios)
    a_onset_sum = Counter()
    for fn in a_herbal_folios:
        for onset, cnt in folio_onset[fn].items():
            a_onset_sum[onset] += cnt

    all_onsets = sorted(list(ONSET_CLASSES.keys()) + ['other'])
    for onset in sorted(all_onsets, key=lambda o: -folio_onset[fn47].get(o, 0)/max(total,1)):
        f47_pct = 100 * folio_onset[fn47].get(onset, 0) / max(total, 1)
        a_pct = 100 * a_onset_sum.get(onset, 0) / max(a_total, 1)
        ratio = f47_pct / a_pct if a_pct > 0 else 0
        if f47_pct > 1 or a_pct > 1:
            print(f"{onset:>8} {f47_pct:>8.1f}% {a_pct:>10.1f}% {ratio:>8.2f}×")

    # Top words in f47
    print("\n--- TOP WORDS IN f47 ---")
    for w, c in folio_words[fn47].most_common(25):
        onset = get_onset(w)
        suf = get_suffix(w)
        print(f"  {w:20s}: {c:4d}  onset={onset} suf={suf}")

    # Top ch-onset words in f47 (the anomaly)
    print("\n--- CH-ONSET WORDS IN f47 (the anomaly, ch:+20%) ---")
    ch_words_f47 = Counter()
    a_ch_words = Counter()
    for w, c in folio_words[fn47].items():
        if get_onset(w) == 'ch':
            ch_words_f47[w] += c
    for fn in a_herbal_folios:
        for w, c in folio_words[fn].items():
            if get_onset(w) == 'ch':
                a_ch_words[w] += c

    total_ch_f47 = sum(ch_words_f47.values())
    total_ch_a = sum(a_ch_words.values())
    print(f"  f47 ch-words: {total_ch_f47} tokens ({100*total_ch_f47/max(total,1):.1f}% of f47)")
    print(f"  A-herbal ch-words: {total_ch_a} tokens ({100*total_ch_a/max(a_total,1):.1f}% of A-herbal)")
    print("\n  Top ch-words in f47 vs A-herbal rate:")
    for w, c in ch_words_f47.most_common(15):
        f47_rate = c / max(total, 1)
        a_rate = a_ch_words.get(w, 0) / max(a_total, 1)
        ratio = f47_rate / a_rate if a_rate > 0 else float('inf')
        print(f"    {w:20s}: f47={c} ({100*f47_rate:.2f}‰)  A-her={a_ch_words.get(w,0)} ({100*a_rate:.2f}‰)  {ratio:.1f}×")

    # Section comparison: which section centroid is f47 closest to?
    print("\n--- SECTION CENTROID SIMILARITY (cosine) ---")
    def cosine_sim(v1, v2, keys):
        dot = sum(v1.get(k, 0) * v2.get(k, 0) for k in keys)
        mag1 = math.sqrt(sum(v1.get(k, 0)**2 for k in keys))
        mag2 = math.sqrt(sum(v2.get(k, 0)**2 for k in keys))
        return dot / (mag1 * mag2) if mag1 * mag2 > 0 else 0

    all_onsets_list = list(ONSET_CLASSES.keys()) + ['other']
    f47_vec = {onset: folio_onset[fn47].get(onset, 0) / max(total, 1) for onset in all_onsets_list}

    for sec_name in ["herbal", "pharma", "stars", "cosmo", "astro"]:
        sec_folios = [fn for fn in folio_total if SECTION_MAP.get(fn) == sec_name and fn != 47]
        if not sec_folios:
            continue
        sec_total = sum(folio_total[fn] for fn in sec_folios)
        sec_onset_sum = Counter()
        for fn in sec_folios:
            for onset, cnt in folio_onset[fn].items():
                sec_onset_sum[onset] += cnt
        sec_vec = {onset: sec_onset_sum.get(onset, 0) / max(sec_total, 1) for onset in all_onsets_list}
        sim = cosine_sim(f47_vec, sec_vec, all_onsets_list)
        print(f"  f47 vs {sec_name:8s}: {sim:.4f}")


# ─── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Parsing corpus...")
    records = parse_corpus()
    folio_dialect = get_folio_dialect(records)
    print(f"Loaded {len(records)} body-text lines")

    analyze_herbal_gradient(records, folio_dialect)
    analyze_stars_cth(records, folio_dialect)
    analyze_f47(records, folio_dialect)

    print("\nDone.")
