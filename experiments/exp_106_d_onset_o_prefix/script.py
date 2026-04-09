"""
exp_106: d-Onset Line-Boundary Grammar (H203) + o-Prefix Body Words vs Labels (H202)

H203: Is d-onset a unified LINE-BOUNDARY MORPHEME class?
      Are bare_d-closers vs bare_d-openers morphologically distinct?
      Does the d-chain (d-closer → d+ch-opener) extend to bare_d-openers?

H202: Do ok/ot body words relate to label vocabulary?
      Section distribution and positional profile of o-prefix words.
"""

import re
import math
from collections import defaultdict, Counter

DATA_PATH = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'


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


def parse_voynich():
    """Parse all body text records with line-level context."""
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

    # Second pass: collect records with line info for d-chain analysis
    records = []
    lines_by_para = []  # list of paragraphs, each is list of lines
    current_para_lines = []

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for raw_line in f:
            raw_line = raw_line.strip()
            if not raw_line or raw_line.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', raw_line)
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

            text = re.sub(r'<[^>]+>', '', raw_line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words:
                continue

            line_record = {
                'dialect': dialect,
                'section': section,
                'folio': fb,
                'words': words,
                'is_para_start': is_para_start,
                'first_word': words[0],
                'last_word': words[-1],
                'first_onset': words[0][:2],
                'last_onset': words[-1][:2],
            }
            lines_by_para.append(line_record)

            for pos, w in enumerate(words):
                records.append({
                    'dialect': dialect,
                    'section': section,
                    'folio': fb,
                    'word': w,
                    'is_para_start': is_para_start and pos == 0,
                    'is_line_first': pos == 0,
                    'is_line_last': pos == len(words) - 1,
                    'pos': pos,
                    'line_idx': len(lines_by_para) - 1,
                })

    return records, lines_by_para


def h203_d_onset_grammar(records, lines):
    """H203: d-onset as unified line-boundary morpheme class."""
    print("=" * 70)
    print("H203: d-Onset Line-Boundary Grammar Analysis")
    print("=" * 70)

    # All d-onset records
    d_records = [r for r in records if r['word'].startswith('d') and
                 not r['word'].startswith('dch') and not r['word'].startswith('dsh')]
    d_ch_records = [r for r in records if r['word'].startswith('dch')]
    d_sh_records = [r for r in records if r['word'].startswith('dsh')]
    all_records = records

    n_total = len(all_records)
    n_d = len(d_records)
    n_dch = len(d_ch_records)
    n_dsh = len(d_sh_records)

    print(f"\nTotal body tokens: {n_total}")
    print(f"d-onset bare (not dch/dsh): {n_d} ({n_d/n_total*100:.1f}%)")
    print(f"d+ch (LINE_OPEN tier): {n_dch} ({n_dch/n_total*100:.1f}%)")
    print(f"d+sh (LINE_OPEN tier): {n_dsh} ({n_dsh/n_total*100:.1f}%)")

    # Suffix distribution of bare_d words
    print(f"\n--- Bare d-onset: suffix distribution ---")
    def get_suffix(word):
        for suf in ['eedy', 'edy', 'aiin', 'ain', 'eey', 'ey', 'al', 'ar', 'ol', 'or', 'dy', 'y', 'n', 'r', 'l']:
            if word.endswith(suf) and len(word) > len(suf):
                return '-' + suf
        return '-other'

    d_suffixes = Counter(get_suffix(r['word']) for r in d_records)
    all_suffixes = Counter(get_suffix(r['word']) for r in all_records)
    suffix_enrich = []
    for suf, cnt in d_suffixes.most_common():
        d_rate = cnt / n_d
        all_rate = all_suffixes.get(suf, 0) / n_total
        enrich = d_rate / all_rate if all_rate > 0 else float('inf')
        suffix_enrich.append((suf, cnt, d_rate, all_rate, enrich))
    print(f"{'Suffix':<10} {'d_n':>6} {'d%':>7} {'all%':>7} {'Enrich':>8}")
    for suf, cnt, dr, ar, enr in sorted(suffix_enrich, key=lambda x: -x[4])[:15]:
        enr_s = f"{enr:.2f}×" if enr != float('inf') else "∞"
        print(f"  {suf:<10} {cnt:>6} {dr*100:>6.1f}% {ar*100:>6.1f}% {enr_s:>8}")

    # LFirst/LLast profile of bare_d words
    print(f"\n--- Bare d-onset: positional profile (overall vs A vs B) ---")
    def pos_profile(recs, label):
        n = len(recs)
        if n == 0:
            return
        lf = sum(1 for r in recs if r['is_line_first']) / n
        ll = sum(1 for r in recs if r['is_line_last']) / n
        ps = sum(1 for r in recs if r['is_para_start']) / n
        print(f"  {label}: n={n}, PS={ps*100:.1f}%, LFirst={lf*100:.1f}%, LLast={ll*100:.1f}%")

    pos_profile(d_records, "All bare_d")
    pos_profile([r for r in d_records if r['dialect'] == 'A'], "A bare_d")
    pos_profile([r for r in d_records if r['dialect'] == 'B'], "B bare_d")
    pos_profile(d_ch_records, "d+ch (LINE_OPEN)")
    pos_profile(d_sh_records, "d+sh (LINE_OPEN)")

    # Top d words by positional role
    print(f"\n--- Top bare_d words by positional bias ---")
    d_word_data = defaultdict(lambda: {'n': 0, 'lf': 0, 'll': 0, 'ps': 0})
    for r in d_records:
        w = r['word']
        d_word_data[w]['n'] += 1
        if r['is_line_first']:
            d_word_data[w]['lf'] += 1
        if r['is_line_last']:
            d_word_data[w]['ll'] += 1
        if r['is_para_start']:
            d_word_data[w]['ps'] += 1

    # Separate closers (LL dominant) vs openers (LF dominant)
    closers = []
    openers = []
    for w, d in d_word_data.items():
        n = d['n']
        if n < 5:
            continue
        lf = d['lf'] / n
        ll = d['ll'] / n
        if ll > 0.25:
            closers.append((w, n, lf, ll))
        elif lf > 0.20:
            openers.append((w, n, lf, ll))

    print(f"\nLine-CLOSERS (LL > 25%):")
    print(f"{'Word':<12} {'n':>5} {'LF%':>7} {'LL%':>7} {'suffix':>8}")
    for w, n, lf, ll in sorted(closers, key=lambda x: -x[3]):
        print(f"  {w:<12} {n:>5} {lf*100:>6.1f}% {ll*100:>6.1f}% {get_suffix(w):>8}")

    print(f"\nLine-OPENERS (LF > 20%):")
    print(f"{'Word':<12} {'n':>5} {'LF%':>7} {'LL%':>7} {'suffix':>8}")
    for w, n, lf, ll in sorted(openers, key=lambda x: -x[2]):
        print(f"  {w:<12} {n:>5} {lf*100:>6.1f}% {ll*100:>6.1f}% {get_suffix(w):>8}")

    # D-chain analysis: does d-closer → d-opener or d+ch on next line?
    print(f"\n--- D-chain analysis: what follows a d-ending line? ---")
    # Find consecutive line pairs where line N ends with d-onset word
    d_closer_words = set(w for w, n, lf, ll in closers)
    d_closer_words.update(['dal', 'dam', 'dy', 'dar', 'dol', 'dor', 'ain', 'aiin'])  # known closers

    next_line_onsets_after_d = Counter()
    next_line_onsets_all = Counter()
    n_d_ending = 0

    for i in range(len(lines) - 1):
        line = lines[i]
        next_line = lines[i + 1]
        # Only count within same dialect
        if line['dialect'] != next_line['dialect']:
            continue
        if next_line['is_para_start']:
            continue  # skip para-boundary transitions

        next_onset = next_line['first_word'][:2]
        next_line_onsets_all[next_onset] += 1

        if line['last_word'].startswith('d'):
            next_line_onsets_after_d[next_onset] += 1
            n_d_ending += 1

    print(f"\nLines ending with d-onset last word: {n_d_ending}")
    print(f"Next-line first-word onset distribution (after d-ending line vs all):")
    print(f"{'Next onset':<12} {'after_d_n':>10} {'after_d%':>10} {'all%':>8} {'Enrich':>8}")
    n_all = sum(next_line_onsets_all.values())
    for onset, cnt in sorted(next_line_onsets_after_d.items(),
                              key=lambda x: -(x[1] / n_d_ending) / (next_line_onsets_all.get(x[0], 1) / n_all)):
        if cnt < 5:
            continue
        after_d_rate = cnt / n_d_ending
        all_rate = next_line_onsets_all.get(onset, 0) / n_all
        enrich = after_d_rate / all_rate if all_rate > 0 else float('inf')
        enr_s = f"{enrich:.2f}×"
        print(f"  {onset:<12} {cnt:>10} {after_d_rate*100:>9.1f}% {all_rate*100:>7.1f}% {enr_s:>8}")

    # Compare d+ch onset (LINE_OPEN) vs bare_d opener
    print(f"\n--- How do d-openers follow d-closers? ---")
    # Count specifically: does d-ending line → dch (LINE_OPEN) vs → bare_d ?
    after_d_specific = Counter()
    for i in range(len(lines) - 1):
        line = lines[i]
        next_line = lines[i + 1]
        if line['dialect'] != next_line['dialect']:
            continue
        if next_line['is_para_start']:
            continue
        if line['last_word'].startswith('d'):
            next_w = next_line['first_word']
            if next_w.startswith('dch') or next_w.startswith('dsh'):
                after_d_specific['d+gallows'] += 1
            elif next_w.startswith('d'):
                after_d_specific['bare_d'] += 1
            else:
                after_d_specific['other'] += 1

    total_after_d = sum(after_d_specific.values())
    for cat, cnt in sorted(after_d_specific.items(), key=lambda x: -x[1]):
        print(f"  After d-ending line → {cat}: {cnt} ({cnt/total_after_d*100:.1f}%)")

    # By dialect
    print(f"\n--- D-chain by dialect ---")
    for dialect in ['A', 'B']:
        after_d_d = Counter()
        n_d_dial = 0
        for i in range(len(lines) - 1):
            line = lines[i]
            next_line = lines[i + 1]
            if line['dialect'] != dialect or next_line['dialect'] != dialect:
                continue
            if next_line['is_para_start']:
                continue
            if line['last_word'].startswith('d'):
                n_d_dial += 1
                next_w = next_line['first_word']
                if next_w.startswith('dch') or next_w.startswith('dsh'):
                    after_d_d['d+gallows'] += 1
                elif next_w.startswith('d'):
                    after_d_d['bare_d'] += 1
                else:
                    after_d_d['other'] += 1

        print(f"\n  Dialect {dialect}: {n_d_dial} d-ending lines")
        for cat, cnt in sorted(after_d_d.items(), key=lambda x: -x[1]):
            print(f"    → {cat}: {cnt} ({cnt/n_d_dial*100:.1f}%)")


def h202_o_prefix_body_vs_labels(records):
    """H202: o-prefix body words — section distribution and label connection."""
    print("\n" + "=" * 70)
    print("H202: o-Prefix Body Words vs Label System")
    print("=" * 70)

    # Parse label words separately
    label_records = []
    label_folio_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})

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
            section = classify_section(fb)

            lc_stripped = locus_code.lstrip('+*=/~&')
            # Label loci: Lf, Lz, Ls, Lc, Ln, Lt
            locus_clean = lc_stripped.lstrip('@')
            is_label = (locus_clean.startswith('Lf') or locus_clean.startswith('Lz') or
                        locus_clean.startswith('Ls') or locus_clean.startswith('Ln') or
                        locus_clean.startswith('Lc') or locus_clean.startswith('Lt'))
            if not is_label:
                continue

            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            for w in words:
                label_records.append({'word': w, 'section': section, 'folio': fb})

    # o-prefix body words: ok+, ot+, ol+, or+, od+
    o_prefix_body = [r for r in records if r['word'].startswith('o') and len(r['word']) >= 3]
    o_prefix_labels = [r for r in label_records if r['word'].startswith('o') and len(r['word']) >= 3]
    qo_body = [r for r in records if r['word'].startswith('qo') and len(r['word']) >= 4]

    print(f"\nTotal body tokens: {len(records)}")
    print(f"o-prefix body words (len>=3): {len(o_prefix_body)} ({len(o_prefix_body)/len(records)*100:.1f}%)")
    print(f"o-prefix label words: {len(o_prefix_labels)}")
    print(f"qo-body words: {len(qo_body)}")

    # Vocabulary overlap: o-body vs o-labels
    o_body_vocab = set(r['word'] for r in o_prefix_body)
    o_label_vocab = set(r['word'] for r in o_prefix_labels)
    qo_vocab = set(r['word'] for r in qo_body)

    shared_body_label = o_body_vocab & o_label_vocab
    body_only = o_body_vocab - o_label_vocab
    label_only = o_label_vocab - o_body_vocab

    print(f"\nVocabulary overlap (o-prefix):")
    print(f"  o-body unique words: {len(o_body_vocab)}")
    print(f"  o-label unique words: {len(o_label_vocab)}")
    print(f"  Shared (body∩label): {len(shared_body_label)} ({len(shared_body_label)/len(o_body_vocab|o_label_vocab)*100:.1f}% of union)")
    print(f"  Body-only: {len(body_only)}")
    print(f"  Label-only: {len(label_only)}")

    # Strip 'o' and compare stems to qo-stems
    o_stems = set(w[1:] for w in o_body_vocab)
    qo_stems = set(w[2:] for w in qo_vocab)
    shared_stems = o_stems & qo_stems
    print(f"\n  Stem overlap (strip prefix): o-body stems ∩ qo-stems = {len(shared_stems)}/{len(o_stems)} ({len(shared_stems)/len(o_stems)*100:.1f}%)")
    print(f"  Top shared stems (o-body + qo-body):")
    o_stem_freq = Counter()
    for r in o_prefix_body:
        o_stem_freq[r['word'][1:]] += 1
    qo_stem_freq = Counter()
    for r in qo_body:
        qo_stem_freq[r['word'][2:]] += 1
    for stem in sorted(shared_stems, key=lambda s: -(o_stem_freq.get(s, 0) + qo_stem_freq.get(s, 0)))[:20]:
        o_cnt = o_stem_freq.get(stem, 0)
        qo_cnt = qo_stem_freq.get(stem, 0)
        print(f"    stem='{stem}': o-body={o_cnt} ('{('o'+stem)[:12]}'), qo-body={qo_cnt} ('{('qo'+stem)[:12]}')")

    # Section distribution of o-prefix body words
    print(f"\n--- o-prefix body words: section distribution ---")
    section_totals = Counter(r['section'] for r in records)
    o_section = Counter(r['section'] for r in o_prefix_body)
    print(f"{'Section':<15} {'o_count':>8} {'section_total':>14} {'o_rate%':>9}")
    for sect, cnt in sorted(o_section.items(), key=lambda x: -x[1]):
        tot = section_totals.get(sect, 0)
        rate = cnt / tot if tot > 0 else 0
        print(f"  {sect:<15} {cnt:>8} {tot:>14} {rate*100:>8.1f}%")

    # Positional profile of o-prefix body sub-classes
    print(f"\n--- o-prefix sub-class positional profiles ---")
    sub_classes = {
        'o+k (okaiin, okain, okal...)': [r for r in o_prefix_body if r['word'].startswith('ok')],
        'o+t (otedy, otaiin, otal...)': [r for r in o_prefix_body if r['word'].startswith('ot')],
        'o+l (ol, olkey, olkar...)': [r for r in o_prefix_body if r['word'].startswith('ol')],
        'o+r (or, orol, oredy...)': [r for r in o_prefix_body if r['word'].startswith('or')],
        'o+key/oke (okeey, okedy...)': [r for r in o_prefix_body if r['word'].startswith('oke')],
    }
    for name, recs in sub_classes.items():
        n = len(recs)
        if n == 0:
            continue
        lf = sum(1 for r in recs if r['is_line_first']) / n
        ll = sum(1 for r in recs if r['is_line_last']) / n
        ps = sum(1 for r in recs if r['is_para_start']) / n
        print(f"  {name}: n={n}, PS={ps*100:.1f}%, LF={lf*100:.1f}%, LL={ll*100:.1f}%")

    # Compare o-body vs o-label top words
    print(f"\n--- o-prefix: Top body words vs top label words ---")
    o_body_freq = Counter(r['word'] for r in o_prefix_body)
    o_label_freq = Counter(r['word'] for r in o_prefix_labels)

    print(f"\nTop 20 o-prefix BODY words:")
    for word, cnt in o_body_freq.most_common(20):
        in_label = o_label_freq.get(word, 0)
        in_qo = qo_stem_freq.get(word[1:], 0)  # does the stem appear as qo-word?
        print(f"  {word:<15} body={cnt:>5}, label={in_label:>3}, qo-equiv('{('qo'+word[1:])[:12]}')={in_qo:>3}")

    print(f"\nTop 20 o-prefix LABEL words:")
    for word, cnt in o_label_freq.most_common(20):
        in_body = o_body_freq.get(word, 0)
        in_qo = qo_stem_freq.get(word[1:], 0)
        print(f"  {word:<15} label={cnt:>5}, body={in_body:>3}, qo-equiv('{('qo'+word[1:])[:12]}')={in_qo:>3}")

    # Are there o-body words that appear ONLY in one dialect?
    print(f"\n--- o-prefix body words: dialect distribution ---")
    a_o_body = Counter(r['word'] for r in o_prefix_body if r['dialect'] == 'A')
    b_o_body = Counter(r['word'] for r in o_prefix_body if r['dialect'] == 'B')
    n_a = sum(1 for r in records if r['dialect'] == 'A')
    n_b = sum(1 for r in records if r['dialect'] == 'B')

    print(f"A o-prefix rate: {sum(a_o_body.values())/n_a*100:.1f}%")
    print(f"B o-prefix rate: {sum(b_o_body.values())/n_b*100:.1f}%")

    # Words with strong A or B preference
    print(f"\nTop A-dominant o-words (ratio A_rate/B_rate):")
    for word in sorted(set(a_o_body.keys()) | set(b_o_body.keys()),
                       key=lambda w: -(a_o_body.get(w, 0)/n_a) / max(b_o_body.get(w, 0.001)/n_b, 0.0001))[:15]:
        if a_o_body.get(word, 0) + b_o_body.get(word, 0) < 5:
            continue
        ar = a_o_body.get(word, 0) / n_a * 1000
        br = b_o_body.get(word, 0) / n_b * 1000
        ratio = ar / br if br > 0 else float('inf')
        print(f"  {word:<15}: A={ar:.2f}‰ B={br:.2f}‰ A/B={ratio:.1f}×")

    print(f"\nTop B-dominant o-words (ratio B_rate/A_rate):")
    for word in sorted(set(a_o_body.keys()) | set(b_o_body.keys()),
                       key=lambda w: -(b_o_body.get(w, 0)/n_b) / max(a_o_body.get(w, 0.001)/n_a, 0.0001))[:15]:
        if a_o_body.get(word, 0) + b_o_body.get(word, 0) < 5:
            continue
        ar = a_o_body.get(word, 0) / n_a * 1000
        br = b_o_body.get(word, 0) / n_b * 1000
        ratio = br / ar if ar > 0 else float('inf')
        print(f"  {word:<15}: A={ar:.2f}‰ B={br:.2f}‰ B/A={ratio:.1f}×")


def main():
    print("Loading data...")
    records, lines = parse_voynich()
    print(f"Total body word tokens: {len(records)}")
    print(f"Total body lines: {len(lines)}")

    h203_d_onset_grammar(records, lines)
    h202_o_prefix_body_vs_labels(records)


if __name__ == '__main__':
    main()
