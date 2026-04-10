"""
exp_136: -am as Paragraph-Final Marker (H266) + Universal Core Positional Distribution (H267)
         + Cosmo-Absent Words A-dialect Distribution (H268)

H266: Is -am a SENTENCE-FINAL (paragraph-final) marker, not just a line-final marker?
H267: Does the 71-word universal core behave as functional vocabulary (balanced positional distribution)?
H268: Are the 31 cosmo-absent words (chor, sho, cthy, cthol, cheo) A-dialect specific?
"""

import re
from collections import defaultdict, Counter

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

def parse_corpus_with_locus():
    """Returns records including the raw locus type for paragraph detection.

    EVA ZL3b locus prefix codes:
      @ = paragraph start (first line)
      * = paragraph start (mid-folio)
      + = paragraph continuation
      = = paragraph tail (last line, often short)
      ~ = label line
      & = uncertain
    """
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
            # Extract the prefix character (position type within paragraph)
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
            words = [w for w in text.split('.') if re.match(r'[a-z]', w)]
            if not words:
                continue
            # folio_base strips the line number (f1r.1 → f1r)
            folio_base = folio_str.split('.')[0]
            # is_para_start: @ or * signals a new paragraph begins
            is_para_start = prefix_char in ('@', '*')
            # is_para_tail: = signals a paragraph tail (often last line of para)
            is_para_tail = prefix_char == '='
            records.append({
                'folio': folio_str,
                'folio_base': folio_base,
                'folio_num': folio_num,
                'section': section,
                'locus_type': locus_type,
                'prefix_char': prefix_char,
                'is_para_start': is_para_start,
                'is_para_tail': is_para_tail,
                'words': words
            })
    return records

def get_folio_dialect(records):
    folio_counts = defaultdict(lambda: {'edy': 0, 'eedy': 0, 'total': 0})
    for rec in records:
        fn = rec['folio_base']  # Use folio_base (without line number)
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


# ─── PARAGRAPH DETECTION ───────────────────────────────────────────────────────

def detect_paragraphs(records):
    """
    Group records into paragraphs using prefix_char.
    @ or * marks paragraph start (new paragraph begins).
    + and = are continuation and tail.
    A new paragraph is created each time is_para_start=True.
    """
    paragraphs = []
    current_para = None

    for rec in records:
        if rec['is_para_start'] or current_para is None:
            if current_para is not None and current_para['lines']:
                paragraphs.append(current_para)
            current_para = {
                'folio_base': rec['folio_base'],
                'section': rec['section'],
                'lines': [rec],
                'n_lines': 1,
            }
        else:
            # Continue current paragraph (if same folio)
            if current_para['folio_base'] == rec['folio_base']:
                current_para['lines'].append(rec)
                current_para['n_lines'] += 1
            else:
                # Different folio — save current and start new
                if current_para['lines']:
                    paragraphs.append(current_para)
                current_para = {
                    'folio_base': rec['folio_base'],
                    'section': rec['section'],
                    'lines': [rec],
                    'n_lines': 1,
                }

    if current_para is not None and current_para['lines']:
        paragraphs.append(current_para)

    return paragraphs


# ─── H266: -am AS PARAGRAPH-FINAL MARKER ─────────────────────────────────────

def analyze_am_marker(records, paragraphs):
    print("=" * 70)
    print("H266: -am AS PARAGRAPH-FINAL MARKER")
    print("=" * 70)

    # Baseline: all line-final positions
    all_line_final_suf = Counter()
    all_line_final_total = 0

    # Para-final lines (last line of each paragraph)
    para_final_suf = Counter()
    para_final_total = 0

    # Non-para-final line-finals
    non_para_final_suf = Counter()
    non_para_final_total = 0

    # Para-final LAST WORD specifically
    para_final_last_word_suf = Counter()
    para_first_last_word_suf = Counter()
    para_first_total = 0

    # Filter out single-line paragraphs for para-final analysis (ambiguous)
    multi_line_paras = [p for p in paragraphs if p['n_lines'] >= 2]
    single_line_paras = [p for p in paragraphs if p['n_lines'] == 1]
    print(f"\nTotal paragraphs: {len(paragraphs)}")
    print(f"Multi-line paragraphs (≥2 lines): {len(multi_line_paras)}")
    print(f"Single-line paragraphs: {len(single_line_paras)}")
    print(f"Total lines: {len(records)}")

    # Identify para-final lines
    para_final_rec_ids = set()
    para_first_rec_ids = set()
    for para in multi_line_paras:
        last_line = para['lines'][-1]
        first_line = para['lines'][0]
        para_final_rec_ids.add(id(last_line))
        para_first_rec_ids.add(id(first_line))

    for rec in records:
        words = rec['words']
        if not words:
            continue
        last_word = words[-1]
        suf = get_suffix(last_word)
        all_line_final_suf[suf] += 1
        all_line_final_total += 1

        is_pf = id(rec) in para_final_rec_ids
        is_pfs = id(rec) in para_first_rec_ids
        if is_pf:
            para_final_suf[suf] += 1
            para_final_total += 1
            para_final_last_word_suf[suf] += 1
        if is_pfs:
            para_first_last_word_suf[suf] += 1
            para_first_total += 1
        if not is_pf and not is_pfs:
            non_para_final_suf[suf] += 1
            non_para_final_total += 1

    print(f"\nPara-final lines (multi-line paras): {para_final_total}")
    print(f"Para-first lines: {para_first_total}")
    print(f"Non-para-boundary line-finals: {non_para_final_total}")

    print("\n--- SUFFIX DISTRIBUTION AT DIFFERENT LINE POSITIONS ---")
    print(f"\n{'Suffix':<10} {'All LL':>10} {'Para-Final':>12} {'Non-PF':>10} {'PF/all enrich':>15}")
    all_suf = sorted(SUFFIXES + ["other"])
    for suf in sorted(all_suf, key=lambda s: -para_final_suf.get(s, 0) / max(para_final_total, 1)):
        all_rate = all_line_final_suf.get(suf, 0) / max(all_line_final_total, 1)
        pf_rate = para_final_suf.get(suf, 0) / max(para_final_total, 1)
        npf_rate = non_para_final_suf.get(suf, 0) / max(non_para_final_total, 1)
        ratio = pf_rate / all_rate if all_rate > 0 else 0
        pf_cnt = para_final_suf.get(suf, 0)
        all_cnt = all_line_final_suf.get(suf, 0)
        if all_cnt > 0 or pf_cnt > 0:
            print(f"-{suf:<9} {all_cnt:>4} ({100*all_rate:.1f}%)  {pf_cnt:>4} ({100*pf_rate:.1f}%)  {non_para_final_suf.get(suf,0):>4} ({100*npf_rate:.1f}%)  {ratio:.2f}×")

    # By section
    print("\n--- -am AT PARA-FINAL vs ALL LINE-FINAL BY SECTION ---")
    print(f"{'Section':<10} {'Para-Final -am%':>16} {'All LL -am%':>14} {'Enrichment':>12}")
    for sec in ["herbal", "astro", "cosmo", "pharma", "stars"]:
        sec_recs = [r for r in records if r['section'] == sec]
        sec_all_am = sum(1 for r in sec_recs if r['words'] and get_suffix(r['words'][-1]) == 'am')
        sec_all_total = sum(1 for r in sec_recs if r['words'])

        sec_pf_recs = [r for r in sec_recs if id(r) in para_final_rec_ids]
        sec_pf_am = sum(1 for r in sec_pf_recs if r['words'] and get_suffix(r['words'][-1]) == 'am')
        sec_pf_total = len(sec_pf_recs)

        all_rate = sec_all_am / max(sec_all_total, 1)
        pf_rate = sec_pf_am / max(sec_pf_total, 1)
        ratio = pf_rate / all_rate if all_rate > 0 else 0
        print(f"{sec:<10} {sec_pf_am:>3}/{sec_pf_total:>4} ({100*pf_rate:.1f}%)  {sec_all_am:>3}/{sec_all_total:>4} ({100*all_rate:.1f}%)  {ratio:.2f}×")

    # -am words at para-final positions
    print("\n--- TOP -am WORDS AT PARA-FINAL LAST POSITIONS ---")
    pf_am_words = Counter()
    for rec in records:
        if id(rec) in para_final_rec_ids and rec['words']:
            lw = rec['words'][-1]
            if get_suffix(lw) == 'am':
                pf_am_words[lw] += 1
    for w, c in pf_am_words.most_common(15):
        print(f"  {w:20s}: {c:4d}  onset={get_onset(w)}")

    # Compare -am word-final position within para-final lines
    print("\n--- -am WORDS ANYWHERE IN PARA-FINAL LINES (not just last position) ---")
    pf_internal_am = Counter()
    for rec in records:
        if id(rec) in para_final_rec_ids:
            for w in rec['words']:
                if get_suffix(w) == 'am':
                    pf_internal_am[w] += 1
    # Compare to baseline
    all_am = Counter()
    for rec in records:
        for w in rec['words']:
            if get_suffix(w) == 'am':
                all_am[w] += 1
    total_pf_words = sum(len(r['words']) for r in records if id(r) in para_final_rec_ids)
    total_all_words = sum(len(r['words']) for r in records)
    pf_am_total = sum(pf_internal_am.values())
    all_am_total = sum(all_am.values())
    pf_am_rate = pf_am_total / max(total_pf_words, 1)
    all_am_rate = all_am_total / max(total_all_words, 1)
    print(f"  -am words in para-final lines: {pf_am_total}/{total_pf_words} = {100*pf_am_rate:.2f}%")
    print(f"  -am words in ALL lines: {all_am_total}/{total_all_words} = {100*all_am_rate:.2f}%")
    print(f"  Para-final internal -am enrichment: {pf_am_rate/all_am_rate:.2f}×")

    # -am concentration at SECOND-TO-LAST position in para-final lines
    print("\n--- SUFFIX ENRICHMENT AT PARA-FINAL LINES (all positions) ---")
    pf_all_suf = Counter()
    pf_all_total = 0
    baseline_all_suf = Counter()
    baseline_all_total = 0
    for rec in records:
        for w in rec['words']:
            suf = get_suffix(w)
            baseline_all_suf[suf] += 1
            baseline_all_total += 1
            if id(rec) in para_final_rec_ids:
                pf_all_suf[suf] += 1
                pf_all_total += 1
    print(f"  Total words in para-final lines: {pf_all_total}")
    for suf in sorted(SUFFIXES, key=lambda s: -(pf_all_suf.get(s,0)/max(pf_all_total,1))/(baseline_all_suf.get(s,0)/max(baseline_all_total,1)) if baseline_all_suf.get(s,0)>0 else 0):
        base_rate = baseline_all_suf.get(suf, 0) / max(baseline_all_total, 1)
        pf_rate2 = pf_all_suf.get(suf, 0) / max(pf_all_total, 1)
        ratio = pf_rate2 / base_rate if base_rate > 0 else 0
        if ratio > 1.2 or ratio < 0.8:
            cnt = pf_all_suf.get(suf, 0)
            print(f"  -{suf:<9}: {cnt:4d} ({100*pf_rate2:.1f}%)  enrichment vs corpus: {ratio:.2f}×")


# ─── H267: UNIVERSAL CORE POSITIONAL DISTRIBUTION ─────────────────────────────

def analyze_universal_core(records):
    print("\n" + "=" * 70)
    print("H267: UNIVERSAL CORE POSITIONAL DISTRIBUTION")
    print("=" * 70)

    sections = ["herbal", "astro", "cosmo", "pharma", "stars"]

    # Get section vocabularies
    section_vocab = defaultdict(set)
    section_word_counts = defaultdict(Counter)
    for rec in records:
        sec = rec['section']
        for w in rec['words']:
            section_vocab[sec].add(w)
            section_word_counts[sec][w] += 1

    # Universal core (all 5 sections)
    universal = section_vocab['herbal']
    for sec in sections[1:]:
        universal = universal & section_vocab[sec]
    print(f"\nUniversal core size: {len(universal)} types")
    print(f"Top universal words by total frequency:")
    shared_freq = sorted([(w, sum(section_word_counts[s][w] for s in sections)) for w in universal],
                         key=lambda x: -x[1])
    for w, total_c in shared_freq[:25]:
        print(f"  {w:20s}: {total_c:5d}  onset={get_onset(w)} suffix={get_suffix(w)}")

    # Compare positional distribution: universal core vs section-exclusive words
    print("\n--- POSITIONAL DISTRIBUTION: UNIVERSAL CORE vs SECTION-EXCLUSIVE ---")

    # Build section-exclusive sets
    section_exclusive = {}
    for sec in sections:
        others = set()
        for other in sections:
            if other != sec:
                others |= section_vocab[other]
        section_exclusive[sec] = section_vocab[sec] - others

    # Compute positional profiles
    def get_positional_profile(word_filter_fn):
        """Compute LF/MID/LL rates for words matching filter."""
        lf = mid = ll = total = 0
        for rec in records:
            words = rec['words']
            n = len(words)
            for i, w in enumerate(words):
                if not word_filter_fn(w):
                    continue
                total += 1
                if n == 1 or i == 0:
                    lf += 1
                elif i == n - 1:
                    ll += 1
                else:
                    mid += 1
        return lf, mid, ll, total

    universal_set = set(universal)
    non_universal_recs = set()
    for sec in sections:
        non_universal_recs |= section_exclusive[sec]

    lf_u, mid_u, ll_u, tot_u = get_positional_profile(lambda w: w in universal_set)
    lf_e, mid_e, ll_e, tot_e = get_positional_profile(lambda w: w in non_universal_recs)

    print(f"\n  {'':25s} {'LF%':>8} {'MID%':>8} {'LL%':>8} {'n':>8}")
    print(f"  {'Universal core (71 types)':25s} {100*lf_u/max(tot_u,1):>8.1f} {100*mid_u/max(tot_u,1):>8.1f} {100*ll_u/max(tot_u,1):>8.1f} {tot_u:>8}")
    print(f"  {'Section-exclusive':25s} {100*lf_e/max(tot_e,1):>8.1f} {100*mid_e/max(tot_e,1):>8.1f} {100*ll_e/max(tot_e,1):>8.1f} {tot_e:>8}")

    # Positional profile per individual universal word
    print("\n--- PER-WORD POSITIONAL PROFILE (UNIVERSAL CORE, top 30 by frequency) ---")
    print(f"  {'Word':<20} {'Total':>6} {'LF%':>6} {'MID%':>6} {'LL%':>6} {'Onset':<8} {'Suffix'}")
    for w, total_c in shared_freq[:30]:
        lf_w, mid_w, ll_w, tot_w = get_positional_profile(lambda x, word=w: x == word)
        print(f"  {w:<20} {tot_w:>6} {100*lf_w/max(tot_w,1):>6.1f} {100*mid_w/max(tot_w,1):>6.1f} {100*ll_w/max(tot_w,1):>6.1f} {get_onset(w):<8} {get_suffix(w)}")

    # Onset profile of universal core
    print("\n--- ONSET PROFILE COMPARISON: UNIVERSAL CORE vs SECTION-EXCLUSIVE vs ALL ---")
    all_onsets_list = list(ONSET_CLASSES.keys()) + ["other"]
    univ_onset = Counter(get_onset(w) for w in universal_set)
    excl_onset = Counter()
    for sec in sections:
        for w in section_exclusive[sec]:
            excl_onset[get_onset(w)] += 1
    all_onset = Counter(get_onset(w) for sec in sections for w in section_vocab[sec])
    print(f"\n  {'Onset':<10} {'Universal%':>12} {'Exclusive%':>12} {'All%':>8}")
    for onset in all_onsets_list:
        u_pct = 100 * univ_onset.get(onset, 0) / max(len(universal_set), 1)
        e_pct = 100 * excl_onset.get(onset, 0) / max(sum(excl_onset.values()), 1)
        a_pct = 100 * all_onset.get(onset, 0) / max(sum(all_onset.values()), 1)
        if max(u_pct, e_pct) > 1:
            print(f"  {onset:<10} {u_pct:>12.1f} {e_pct:>12.1f} {a_pct:>8.1f}")

    # Bigram context of universal core words
    print("\n--- BIGRAM CONTEXT OF UNIVERSAL CORE WORDS ---")
    print("What onset class FOLLOWS a universal core word?")
    follow_onset_u = Counter()  # what follows universal words
    follow_onset_e = Counter()  # what follows section-exclusive words
    follow_total_u = follow_total_e = 0

    for rec in records:
        words = rec['words']
        for i, w in enumerate(words[:-1]):
            next_w = words[i + 1]
            next_onset = get_onset(next_w)
            if w in universal_set:
                follow_onset_u[next_onset] += 1
                follow_total_u += 1
            elif w in non_universal_recs:
                follow_onset_e[next_onset] += 1
                follow_total_e += 1

    print(f"\n  {'Onset':<10} {'After-Universal%':>17} {'After-Exclusive%':>17}")
    for onset in sorted(all_onsets_list, key=lambda o: -follow_onset_u.get(o,0)/max(follow_total_u,1)):
        u_rate = follow_onset_u.get(onset, 0) / max(follow_total_u, 1)
        e_rate = follow_onset_e.get(onset, 0) / max(follow_total_e, 1)
        if u_rate > 0.02 or e_rate > 0.02:
            print(f"  {onset:<10} {100*u_rate:>17.1f}% {100*e_rate:>17.1f}%")


# ─── H268: COSMO-ABSENT WORDS A-DIALECT DISTRIBUTION ─────────────────────────

def analyze_cosmo_absent(records, folio_dialect):
    print("\n" + "=" * 70)
    print("H268: COSMO-ABSENT WORDS — A-DIALECT DISTRIBUTION")
    print("=" * 70)

    sections = ["herbal", "astro", "cosmo", "pharma", "stars"]

    section_vocab = defaultdict(set)
    section_word_counts = defaultdict(Counter)
    folio_word_counts = defaultdict(Counter)

    for rec in records:
        sec = rec['section']
        fn = rec['folio_base']  # Use folio_base for dialect analysis
        for w in rec['words']:
            section_vocab[sec].add(w)
            section_word_counts[sec][w] += 1
            folio_word_counts[fn][w] += 1

    # Words in all other 4 sections but NOT in cosmo
    cosmo_absent = set()
    other_secs = [s for s in sections if s != 'cosmo']
    for s in other_secs:
        cosmo_absent |= section_vocab[s]
    cosmo_absent -= section_vocab['cosmo']

    # Restrict to those in ALL 4 other sections (not just one)
    in_all_4 = section_vocab[other_secs[0]]
    for s in other_secs[1:]:
        in_all_4 = in_all_4 & section_vocab[s]
    cosmo_absent_all4 = in_all_4 - section_vocab['cosmo']

    print(f"\nWords absent from cosmo (in at least 1 other section): {len(cosmo_absent)}")
    print(f"Words absent from cosmo (in ALL 4 other sections): {len(cosmo_absent_all4)}")

    # Analyze the ALL-4 set
    print("\nTop cosmo-absent-from-all-4 words by total frequency:")
    abs4_freq = sorted([(w, sum(section_word_counts[s][w] for s in other_secs)) for w in cosmo_absent_all4],
                       key=lambda x: -x[1])
    for w, c in abs4_freq[:15]:
        per_sec = "  ".join(f"{s[:3]}={section_word_counts[s][w]}" for s in sections)
        print(f"  {w:20s}: freq={c}  onset={get_onset(w)}  [{per_sec}]")

    # Analyze the broader set (any 1+ other sections)
    # Focus on high-frequency cosmo-absent words
    high_freq_absent = [(w, sum(section_word_counts[s][w] for s in other_secs))
                        for w in cosmo_absent
                        if sum(section_word_counts[s][w] for s in other_secs) >= 10]
    print(f"\nHigh-freq (≥10 total) cosmo-absent words: {len(high_freq_absent)}")

    # Dialect distribution of cosmo-absent words
    print("\n--- DIALECT DISTRIBUTION OF COSMO-ABSENT WORDS ---")
    # Build dialect-folio map
    a_folios = {fn for fn, d in folio_dialect.items() if d == 'A'}
    b_folios = {fn for fn, d in folio_dialect.items() if d == 'B'}

    def word_dialect_split(word):
        """How much of a word's usage is A vs B?"""
        a_count = sum(folio_word_counts[fn].get(word, 0) for fn in a_folios)
        b_count = sum(folio_word_counts[fn].get(word, 0) for fn in b_folios)
        total = a_count + b_count
        if total == 0:
            return 0, 0, 0
        return a_count, b_count, total

    # Top cosmo-absent words by dialect split
    print(f"\n{'Word':<20} {'Total':>6} {'A_cnt':>6} {'B_cnt':>6} {'A%':>6} {'Onset'}")
    for w, total_c in sorted(high_freq_absent, key=lambda x: -x[1])[:25]:
        a_c, b_c, tot = word_dialect_split(w)
        a_pct = 100 * a_c / max(tot, 1)
        print(f"  {w:<20} {total_c:>6} {a_c:>6} {b_c:>6} {a_pct:>6.1f}% {get_onset(w)}")

    # Onset profile of cosmo-absent high-freq words
    print("\n--- ONSET PROFILE OF COSMO-ABSENT WORDS vs COSMO WORDS ---")
    absent_onset = Counter(get_onset(w) for w, c in high_freq_absent)
    cosmo_onset = Counter(get_onset(w) for w in section_vocab['cosmo'])
    absent_total = sum(absent_onset.values())
    cosmo_total = sum(cosmo_onset.values())

    print(f"\n  {'Onset':<10} {'Absent%':>10} {'Cosmo%':>10} {'Ratio':>8}")
    for onset in sorted(list(ONSET_CLASSES.keys()) + ["other"],
                        key=lambda o: -absent_onset.get(o,0)/max(absent_total,1)):
        a_pct = 100 * absent_onset.get(onset, 0) / max(absent_total, 1)
        c_pct = 100 * cosmo_onset.get(onset, 0) / max(cosmo_total, 1)
        ratio = a_pct / c_pct if c_pct > 0 else 0
        if a_pct > 1 or c_pct > 1:
            print(f"  {onset:<10} {a_pct:>10.1f}% {c_pct:>10.1f}% {ratio:>8.2f}×")

    # Section-folio distribution of top cosmo-absent words
    print("\n--- FOLIO DISTRIBUTION OF KEY COSMO-ABSENT WORDS ---")
    key_words = ['chor', 'sho', 'cthy', 'cthol', 'cheo']
    for w in key_words:
        if w not in cosmo_absent:
            print(f"  {w}: NOT cosmo-absent (appears in cosmo!)")
            continue
        folio_dist = sorted([(fn, folio_word_counts[fn].get(w, 0))
                              for fn in folio_word_counts
                              if folio_word_counts[fn].get(w, 0) > 0],
                             key=lambda x: -x[1])
        total = sum(c for _, c in folio_dist)
        d_split = word_dialect_split(w)
        print(f"\n  {w} (total={total}, A={d_split[0]}, B={d_split[1]}, A%={100*d_split[0]/max(d_split[2],1):.1f}%):")
        print(f"  Section breakdown: ", end="")
        for sec in sections:
            cnt = section_word_counts[sec].get(w, 0)
            if cnt > 0:
                print(f"{sec}={cnt}  ", end="")
        print()
        print(f"  Top folios: ", end="")
        for fn, cnt in folio_dist[:8]:
            d = folio_dialect.get(fn, '?')
            fnum = get_folio_num(fn)
            sec = SECTION_MAP.get(fnum, '?')[:3] if fnum else '?'
            print(f"{fn}({d},{sec})={cnt}  ", end="")
        print()

    # Summary: are cosmo-absent words A-dialect specific?
    print("\n--- SUMMARY: IS COSMO ABSENCE DIALECT-DRIVEN? ---")
    a_dominated = sum(1 for w, c in high_freq_absent
                      if word_dialect_split(w)[2] > 0 and
                      100 * word_dialect_split(w)[0] / word_dialect_split(w)[2] >= 70)
    b_dominated = sum(1 for w, c in high_freq_absent
                      if word_dialect_split(w)[2] > 0 and
                      100 * word_dialect_split(w)[1] / word_dialect_split(w)[2] >= 70)
    mixed = len(high_freq_absent) - a_dominated - b_dominated
    print(f"\n  High-freq cosmo-absent ({len(high_freq_absent)} words):")
    print(f"    A-dominated (≥70% A): {a_dominated}")
    print(f"    B-dominated (≥70% B): {b_dominated}")
    print(f"    Mixed: {mixed}")


# ─── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Parsing corpus...")
    records = parse_corpus_with_locus()
    folio_dialect = get_folio_dialect(records)
    print(f"Loaded {len(records)} body-text lines")

    # Detect paragraphs
    paragraphs = detect_paragraphs(records)
    print(f"Detected {len(paragraphs)} paragraphs (by para_id grouping)")

    # Verify paragraph detection
    section_para_counts = Counter(p['section'] for p in paragraphs)
    for sec, cnt in sorted(section_para_counts.items()):
        multi = sum(1 for p in paragraphs if p['section'] == sec and p['n_lines'] >= 2)
        print(f"  {sec:8s}: {cnt:4d} paragraphs ({multi} multi-line)")

    analyze_am_marker(records, paragraphs)
    analyze_universal_core(records)
    analyze_cosmo_absent(records, folio_dialect)

    print("\nDone.")
