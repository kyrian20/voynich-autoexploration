"""
exp_087: daiin in Currier B as Line-Opener (H148), -am/-ol Complementary Distribution (H149)

H148: daiin in B is a LINE-OPENER (LFirst=34%) — opposite role from A (line-closer).
  Investigate: what follows daiin at line-start in B? Which B section? What precedes it?
H149: -am words and oly/oldy are grammatical synonyms — do they alternate on different lines
  (complementary distribution as line-closers)?

Also: s-onset and y-onset as true B line-openers (H150 preliminary).
"""
from pathlib import Path as _RepositoryPath

import re
from collections import defaultdict, Counter

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

AIIN_DOM_FOLIOS = {
    'f1r','f1v','f2r','f2v','f3r','f3v','f4r','f4v','f5r','f5v',
    'f6r','f6v','f7r','f7v','f8r','f8v','f13r','f13v','f14r','f14v',
    'f15r','f15v','f16r','f16v'
}

def folio_base(folio):
    return folio.split('.')[0]

def is_para_start(locus_code):
    return locus_code.lstrip('+*=/~&').startswith('@')

def is_body(locus_code):
    return locus_code.lstrip('+*@=/~&').startswith('P')

def get_onset(word):
    if word.startswith('qo'): return 'qo'
    if word.startswith('ch'): return 'ch'
    if word.startswith('sh'): return 'sh'
    if word and word[0] == 'p': return 'p'
    if word and word[0] == 't': return 't'
    if word and word[0] == 'k': return 'k'
    if word and word[0] == 'd': return 'd'
    if word and word[0] == 's': return 's'
    if word and word[0] == 'y': return 'y'
    if word and word[0] == 'o': return 'o'
    return 'other'

def classify_section(folio):
    m = re.match(r'f(\d+)([rv])', folio)
    if not m: return 'unknown'
    n = int(m.group(1))
    if n <= 57: return 'herbal'
    if 67 <= n <= 73: return 'astro'
    if 75 <= n <= 84: return 'cosmo'
    if 87 <= n <= 102: return 'pharma'
    if 103 <= n <= 116: return 'stars'
    return 'other'

def parse_voynich(path):
    records = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'^<([^>]+)>', line)
            if not m:
                continue
            locus_raw = m.group(1)
            text = line[m.end():].strip()
            parts = locus_raw.split(',')
            if len(parts) < 2:
                continue
            folio_raw = parts[0]
            locus_code = parts[1]
            folio = folio_raw.lstrip('+*=&~')
            if not is_body(locus_code):
                continue
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words:
                continue
            fb = folio_base(folio)
            records.append({
                'folio': fb,
                'locus': locus_code,
                'words': words,
                'is_para_start': is_para_start(locus_code),
                'section': classify_section(fb),
            })
    return records

def compute_edy_rates(records):
    folio_words = defaultdict(list)
    for rec in records:
        folio_words[rec['folio']].extend(rec['words'])
    return {f: sum(1 for w in ws if w.endswith('edy') or w.endswith('eedy')) / len(ws)
            for f, ws in folio_words.items() if ws}

def assign_dialects(records, edy_map):
    for rec in records:
        rec['is_b'] = edy_map.get(rec['folio'], 0) >= 0.05
    return records

def classify_para_boundary(records):
    for i, rec in enumerate(records):
        rec['is_para_final'] = (i + 1 < len(records)) and records[i+1]['is_para_start']
    return records


def h148_daiin_b_line_opener(b_recs, a_recs):
    """
    H148: daiin in B is LINE-OPENER. Investigate:
    1. By line position: what fraction of B daiin tokens are at position 0, 1, 2, mid?
    2. Following-word distribution: what follows daiin in B?
    3. Section breakdown: which sections drive the daiin-B line-opener effect?
    4. Para-start context: is daiin more often at first-line-of-para or mid-para in B?
    5. Compare A: daiin is line-closer (LLast=25.9%); what follows daiin in A?
    """
    print("=== H148: daiin in Currier B as Line-Opener ===\n")

    for dialect_name, recs in [('B', b_recs), ('A', a_recs)]:
        print(f"--- Currier {dialect_name}: daiin positional analysis ---")
        daiin_tokens = []
        total_daiin = 0
        pos0, pos_mid, pos_last = 0, 0, 0
        following = Counter()
        preceding = Counter()
        para_start_daiin = 0
        para_mid_daiin = 0
        section_daiin = Counter()

        for rec in recs:
            words = rec['words']
            n = len(words)
            ps = rec['is_para_start']
            pf = rec['is_para_final']
            for i, w in enumerate(words):
                if w == 'daiin':
                    total_daiin += 1
                    if i == 0: pos0 += 1
                    elif i == n - 1: pos_last += 1
                    else: pos_mid += 1
                    if i < n - 1: following[words[i+1]] += 1
                    if i > 0: preceding[words[i-1]] += 1
                    if ps: para_start_daiin += 1
                    else: para_mid_daiin += 1
                    section_daiin[rec['section']] += 1

        if total_daiin == 0:
            print(f"  No daiin tokens found.")
            continue

        print(f"  Total daiin tokens: {total_daiin}")
        print(f"  Position 0 (line-first): {pos0} ({100*pos0/total_daiin:.1f}%)")
        print(f"  Position mid: {pos_mid} ({100*pos_mid/total_daiin:.1f}%)")
        print(f"  Position last (line-last): {pos_last} ({100*pos_last/total_daiin:.1f}%)")
        print(f"  On para-start lines: {para_start_daiin} ({100*para_start_daiin/total_daiin:.1f}%)")
        print(f"  On non-para-start lines: {para_mid_daiin} ({100*para_mid_daiin/total_daiin:.1f}%)")

        print(f"\n  Top following words after daiin:")
        for w, c in following.most_common(15):
            print(f"    {w}: {c} ({100*c/total_daiin:.1f}%)")

        print(f"\n  Top preceding words before daiin:")
        for w, c in preceding.most_common(15):
            print(f"    {w}: {c} ({100*c/total_daiin:.1f}%)")

        print(f"\n  Section breakdown:")
        for sect, n in section_daiin.most_common():
            print(f"    {sect}: {n} ({100*n/total_daiin:.1f}%)")

        # For B: daiin at position 0 — what comes next?
        if dialect_name == 'B':
            print(f"\n  --- daiin at position 0 (line-first): following-word analysis ---")
            pos0_following = Counter()
            for rec in recs:
                words = rec['words']
                if words and words[0] == 'daiin' and len(words) > 1:
                    pos0_following[words[1]] += 1
            print(f"  daiin[0] followed by (top 15):")
            for w, c in pos0_following.most_common(15):
                print(f"    {w}: {c}")
            print(f"  daiin[0] followed by onset class:")
            onset_counts = Counter()
            for w, c in pos0_following.items():
                onset_counts[get_onset(w)] += c
            for onset, c in onset_counts.most_common():
                print(f"    {onset}: {c} ({100*c/sum(pos0_following.values()):.1f}%)")
        print()

    # Cross-dialect daiin line-position comparison
    print("--- Cross-dialect daiin line-position summary ---")
    for dialect_name, recs in [('A', a_recs), ('B', b_recs)]:
        daiin_line_positions = []
        for rec in recs:
            words = rec['words']
            n = len(words)
            for i, w in enumerate(words):
                if w == 'daiin':
                    # Position as fraction 0=first, 1=last
                    frac = i / (n-1) if n > 1 else 0.5
                    daiin_line_positions.append(frac)
        if daiin_line_positions:
            avg = sum(daiin_line_positions) / len(daiin_line_positions)
            at_first = sum(1 for p in daiin_line_positions if p == 0)
            at_last = sum(1 for p in daiin_line_positions if p == 1.0)
            print(f"  {dialect_name}: avg_position={avg:.3f}, at_first={at_first}/{len(daiin_line_positions)} ({100*at_first/len(daiin_line_positions):.1f}%), at_last={at_last}/{len(daiin_line_positions)} ({100*at_last/len(daiin_line_positions):.1f}%)")
    print()


def h149_am_ol_complementary_distribution(b_recs):
    """
    H149: -am words and oly/oldy are in complementary distribution as line-closers.
    Test: on lines ending with -am, how often do oly/oldy appear? And vice versa?
    Also: are -am line-endings and oly/oldy line-endings enriched in different sections?
    """
    print("=== H149: -am Words and oly/oldy Complementary Distribution ===\n")

    AM_CORE = {'dam', 'otam', 'okam', 'qokam', 'cham', 'ram', 'qotam'}
    OL_CLOSERS = {'oly', 'oldy'}

    # Count B lines ending with -am vs oly/oldy vs other
    am_lines = []  # lines ending with am-core word
    ol_lines = []  # lines ending with oly/oldy
    other_lines = []

    for rec in b_recs:
        words = rec['words']
        if not words: continue
        last = words[-1]
        if last in AM_CORE:
            am_lines.append(rec)
        elif last in OL_CLOSERS:
            ol_lines.append(rec)
        else:
            other_lines.append(rec)

    print(f"B lines ending with -am core: {len(am_lines)} ({100*len(am_lines)/len(b_recs):.1f}%)")
    print(f"B lines ending with oly/oldy: {len(ol_lines)} ({100*len(ol_lines)/len(b_recs):.1f}%)")
    print(f"B lines ending with other: {len(other_lines)} ({100*len(other_lines)/len(b_recs):.1f}%)")
    print()

    # For -am lines: does oly/oldy appear anywhere on the same line?
    am_also_ol = sum(1 for rec in am_lines if any(w in OL_CLOSERS for w in rec['words']))
    ol_also_am = sum(1 for rec in ol_lines if any(w in AM_CORE for w in rec['words']))
    print(f"Lines ending with -am that also contain oly/oldy: {am_also_ol}/{len(am_lines)} ({100*am_also_ol/max(len(am_lines),1):.1f}%)")
    print(f"Lines ending with oly/oldy that also contain -am core: {ol_also_am}/{len(ol_lines)} ({100*ol_also_am/max(len(ol_lines),1):.1f}%)")
    print()

    # Section preferences
    print("Section preference: -am endings vs oly/oldy endings")
    am_sect = Counter(r['section'] for r in am_lines)
    ol_sect = Counter(r['section'] for r in ol_lines)
    all_sect = Counter(r['section'] for r in b_recs)
    for sect in sorted(all_sect.keys()):
        n_total = all_sect[sect]
        n_am = am_sect.get(sect, 0)
        n_ol = ol_sect.get(sect, 0)
        am_rate = 100 * n_am / n_total if n_total else 0
        ol_rate = 100 * n_ol / n_total if n_total else 0
        print(f"  {sect}: total={n_total}, -am={n_am}({am_rate:.1f}%), oly/oldy={n_ol}({ol_rate:.1f}%)")
    print()

    # Is the -am-ending distribution consistent across sections or section-specific?
    # Para-start lines: do they prefer oly/oldy vs -am endings?
    ps_lines = [r for r in b_recs if r['is_para_start']]
    non_ps = [r for r in b_recs if not r['is_para_start']]
    def rate_last(recs, target_set):
        if not recs: return 0.0
        return sum(1 for r in recs if r['words'] and r['words'][-1] in target_set) / len(recs)
    print("Para-start vs non-para-start: line-ending preference")
    print(f"  Para-start lines (n={len(ps_lines)}): -am={100*rate_last(ps_lines, AM_CORE):.1f}%, oly/oldy={100*rate_last(ps_lines, OL_CLOSERS):.1f}%")
    print(f"  Non-para-start lines (n={len(non_ps)}): -am={100*rate_last(non_ps, AM_CORE):.1f}%, oly/oldy={100*rate_last(non_ps, OL_CLOSERS):.1f}%")
    print()

    # Paragraph-position: do -am endings and oly/oldy endings prefer different positions within paragraphs?
    # Group into paragraphs
    paras = []
    current = []
    for rec in b_recs:
        if rec['is_para_start'] and current:
            paras.append(current)
            current = []
        current.append(rec)
    if current:
        paras.append(current)

    # For each line in each paragraph, compute relative position (0=first, 1=last)
    am_positions = []
    ol_positions = []
    for para in paras:
        n = len(para)
        for i, rec in enumerate(para):
            words = rec['words']
            if not words: continue
            last = words[-1]
            frac = i / (n-1) if n > 1 else 0.5
            if last in AM_CORE:
                am_positions.append(frac)
            elif last in OL_CLOSERS:
                ol_positions.append(frac)

    if am_positions:
        print(f"Para-position of -am line-endings (n={len(am_positions)}): avg={sum(am_positions)/len(am_positions):.3f}")
        bins = [0, 0, 0, 0, 0]
        for p in am_positions:
            bins[min(int(p*5), 4)] += 1
        print(f"  Distribution: [0-0.2]={bins[0]}, [0.2-0.4]={bins[1]}, [0.4-0.6]={bins[2]}, [0.6-0.8]={bins[3]}, [0.8-1.0]={bins[4]}")

    if ol_positions:
        print(f"Para-position of oly/oldy line-endings (n={len(ol_positions)}): avg={sum(ol_positions)/len(ol_positions):.3f}")
        bins = [0, 0, 0, 0, 0]
        for p in ol_positions:
            bins[min(int(p*5), 4)] += 1
        print(f"  Distribution: [0-0.2]={bins[0]}, [0.2-0.4]={bins[1]}, [0.4-0.6]={bins[2]}, [0.6-0.8]={bins[3]}, [0.8-1.0]={bins[4]}")
    print()


def h150_s_y_onset_openers(b_recs, a_recs):
    """
    H150 preliminary: s-onset and y-onset as true line-openers.
    What are the most common s-onset and y-onset line-first words?
    Do they show different following-word distributions?
    """
    print("=== H150: s-Onset and y-Onset as True Line-Openers ===\n")

    for dialect_name, recs in [('A', a_recs), ('B', b_recs)]:
        print(f"--- Currier {dialect_name}: s/y-onset line-first analysis ---")
        s_line_first = Counter()
        y_line_first = Counter()
        s_following = Counter()
        y_following = Counter()

        for rec in recs:
            words = rec['words']
            if not words: continue
            first = words[0]
            if get_onset(first) == 's':
                s_line_first[first] += 1
                if len(words) > 1:
                    s_following[words[1]] += 1
            elif get_onset(first) == 'y':
                y_line_first[first] += 1
                if len(words) > 1:
                    y_following[words[1]] += 1

        print(f"  Top s-onset line-first words: {s_line_first.most_common(10)}")
        print(f"  Top s-onset following words: {s_following.most_common(10)}")
        print(f"  Total s-onset line-first: {sum(s_line_first.values())}")
        print()
        print(f"  Top y-onset line-first words: {y_line_first.most_common(10)}")
        print(f"  Top y-onset following words: {y_following.most_common(10)}")
        print(f"  Total y-onset line-first: {sum(y_line_first.values())}")
        print()


def main():
    print("Loading data...")
    records = parse_voynich(DATA_PATH)
    edy_map = compute_edy_rates(records)
    records = assign_dialects(records, edy_map)
    records = classify_para_boundary(records)
    a_recs = [r for r in records if not r['is_b']]
    b_recs = [r for r in records if r['is_b']]
    print(f"Total body records: {len(records)}")
    print(f"A: {len(a_recs)}, B: {len(b_recs)}\n")

    h148_daiin_b_line_opener(b_recs, a_recs)
    h149_am_ol_complementary_distribution(b_recs)
    h150_s_y_onset_openers(b_recs, a_recs)

if __name__ == '__main__':
    main()
