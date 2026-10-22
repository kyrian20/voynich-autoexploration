"""
exp_207: H390 A para-opening vocabulary (first-line words); H391 A first-line grammar sequence;
         H392 B para-terminal formula (what is enriched at B pf_ll?)
"""
from pathlib import Path as _RepositoryPath
import re
from collections import defaultdict, Counter

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

ONSET_ORDER = [
    ('qok', 'qok'), ('qot', 'qot'), ('qo', 'qo'), ('cth', 'cth'),
    ('ch', 'ch'), ('sh', 'sh'), ('ok', 'ok'), ('ot', 'ot'), ('ol', 'ol'),
    ('d', 'd'), ('s', 's'), ('y', 'y'), ('k', 'k'), ('t', 't'),
    ('l', 'l'), ('r', 'r'), ('p', 'p'), ('f', 'f'), ('o', 'o'),
]

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix):
            return label
    return 'other'

def folio_base(folio):
    return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0:
        return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

def classify_section(folio):
    m = re.match(r'f(\d+)([rv])', folio)
    if not m:
        return 'other'
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
    if 117 <= n <= 202:
        return 'cosmo'
    return 'other'

def parse_corpus():
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
            words = [w for w in re.split(r'[-.\s]', text)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            for w in words:
                folio_word_stats[fb]['total'] += 1
                if w.endswith('eedy'):
                    folio_word_stats[fb]['eedy'] += 1
                elif w.endswith('edy'):
                    folio_word_stats[fb]['edy'] += 1

    folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}

    paragraphs = []
    current_para = None
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
            dialect = folio_dialect.get(fb, 'unknown')
            section = classify_section(fb)

            lc_stripped = locus_code.lstrip('+*=/~&')
            is_para_start = lc_stripped.startswith('@')
            is_body = lc_stripped.lstrip('@').startswith('P')
            if not is_body:
                continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words:
                continue
            if is_para_start:
                current_para = {'dialect': dialect, 'section': section,
                                'folio': fb, 'lines': []}
                paragraphs.append(current_para)
            if current_para is not None:
                current_para['lines'].append(words)
    return paragraphs, folio_dialect

# ============================================================
# H390: A Para-Opening Formula — First-Line Word Distribution
# ============================================================
def h390_a_para_opening(paragraphs):
    print("=== H390: A Para-Opening Vocabulary (First Paragraph Line) ===")

    # Overall A word distribution
    a_word_count = Counter()
    a_onset_count = Counter()
    a_total = 0

    # First-line word distribution
    a_fl_word = Counter()
    a_fl_onset = Counter()
    a_fl_total = 0

    # Non-first-line for comparison
    a_nfl_onset = Counter()
    a_nfl_total = 0

    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        lines = para['lines']
        for line_idx, line in enumerate(lines):
            for pos, word in enumerate(line):
                a_word_count[word] += 1
                a_onset_count[get_onset(word)] += 1
                a_total += 1
                if line_idx == 0:
                    a_fl_word[word] += 1
                    a_fl_onset[get_onset(word)] += 1
                    a_fl_total += 1
                else:
                    a_nfl_onset[get_onset(word)] += 1
                    a_nfl_total += 1

    print(f"\nA first-line total words: {a_fl_total}; all-A: {a_total}; non-first: {a_nfl_total}")

    print("\nA first-line onset distribution vs all-A baseline:")
    print(f"{'Onset':<8} {'fl_n':>5} {'fl%':>7} {'base%':>7} {'Enr':>6}")
    for onset in sorted(a_onset_count, key=lambda o: -a_fl_onset.get(o, 0)):
        n = a_fl_onset.get(onset, 0)
        if n < 2:
            continue
        fl_pct = n / a_fl_total
        base_pct = a_onset_count[onset] / a_total
        enr = fl_pct / base_pct if base_pct > 0 else 0
        print(f"{onset:<8} {n:>5} {fl_pct*100:>6.2f}% {base_pct*100:>6.2f}% {enr:>6.2f}×")

    print("\nTop 25 A first-line words:")
    for word, n in a_fl_word.most_common(25):
        total_in_a = a_word_count[word]
        fl_rate = n / a_fl_total
        base_rate = total_in_a / a_total
        enr = fl_rate / base_rate if base_rate > 0 else 0
        print(f"  {word}: fl={n}, total={total_in_a}, fl%={fl_rate*100:.2f}%, base%={base_rate*100:.2f}%, {enr:.2f}×")

    # PS word (pos=0, line_idx=0) vs rest of first line (pos>=1, line_idx=0)
    print("\nA first-line position breakdown:")
    a_ps_onset = Counter()  # pos=0, line_idx=0
    a_fl_body_onset = Counter()  # pos>=1, line_idx=0
    a_ps_total = 0
    a_fl_body_total = 0
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        if not para['lines']:
            continue
        first_line = para['lines'][0]
        for pos, word in enumerate(first_line):
            onset = get_onset(word)
            if pos == 0:
                a_ps_onset[onset] += 1
                a_ps_total += 1
            else:
                a_fl_body_onset[onset] += 1
                a_fl_body_total += 1

    print(f"\nA PS (pos=0, line_idx=0): n={a_ps_total}")
    print(f"{'Onset':<8} {'ps_n':>5} {'ps%':>7} {'base%':>7} {'Enr':>6}")
    for onset in sorted(a_onset_count, key=lambda o: -a_ps_onset.get(o, 0)):
        n = a_ps_onset.get(onset, 0)
        if n < 2:
            continue
        ps_pct = n / a_ps_total
        base_pct = a_onset_count[onset] / a_total
        enr = ps_pct / base_pct if base_pct > 0 else 0
        print(f"{onset:<8} {n:>5} {ps_pct*100:>6.2f}% {base_pct*100:>6.2f}% {enr:>6.2f}×")

    print(f"\nA first-line non-PS body (pos>=1, line_idx=0): n={a_fl_body_total}")
    print(f"{'Onset':<8} {'flb_n':>5} {'flb%':>7} {'base%':>7} {'Enr':>6}")
    for onset in sorted(a_onset_count, key=lambda o: -a_fl_body_onset.get(o, 0)):
        n = a_fl_body_onset.get(onset, 0)
        if n < 2:
            continue
        flb_pct = n / a_fl_body_total
        base_pct = a_onset_count[onset] / a_total
        enr = flb_pct / base_pct if base_pct > 0 else 0
        print(f"{onset:<8} {n:>5} {flb_pct*100:>6.2f}% {base_pct*100:>6.2f}% {enr:>6.2f}×")

# ============================================================
# H391: A First-Line Grammar Sequence — Positions after PS
# ============================================================
def h391_a_first_line_sequence(paragraphs):
    print("\n=== H391: A First-Line Grammar Sequence (Positions 0,1,2,3,4+) ===")

    # For each within-first-line position, compute onset distribution
    a_fl_pos_onset = defaultdict(Counter)  # {pos: {onset: count}}
    a_fl_pos_total = Counter()
    a_total_onset = Counter()
    a_total = 0

    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        if not para['lines']:
            continue
        first_line = para['lines'][0]
        for pos, word in enumerate(first_line):
            onset = get_onset(word)
            p = min(pos, 5)  # cap at 5+
            a_fl_pos_onset[str(p)][onset] += 1
            a_fl_pos_total[str(p)] += 1
        for line in para['lines']:
            for word in line:
                a_total_onset[get_onset(word)] += 1
                a_total += 1

    print("\nA first-line onset profile by within-line position:")
    # Focus on sh, ch, cth, d, daiin
    key_onsets = ['p', 'sh', 'ch', 'cth', 'd', 'qok', 'other']
    header = f"{'Pos':<6}" + "".join(f"{o:>8}" for o in key_onsets)
    print(header)
    for p_label in sorted(a_fl_pos_total.keys(), key=lambda x: int(x)):
        total = a_fl_pos_total[p_label]
        row = f"{p_label+'+'if p_label=='5' else p_label:<6}"
        for onset in key_onsets:
            n = a_fl_pos_onset[p_label].get(onset, 0)
            pct = n / total if total > 0 else 0
            row += f"{pct*100:>7.1f}%"
        print(row + f"  (n={total})")

    # Also: is sh enriched at positions 1+ of first line (not just pos 0)?
    print("\nSh-onset enrichment at first-line positions (vs all-A baseline):")
    sh_base = a_total_onset.get('sh', 0) / a_total if a_total > 0 else 0
    print(f"  All-A sh baseline: {sh_base*100:.2f}%")
    for p_label in sorted(a_fl_pos_total.keys(), key=lambda x: int(x)):
        total = a_fl_pos_total[p_label]
        n = a_fl_pos_onset[p_label].get('sh', 0)
        pct = n / total if total > 0 else 0
        enr = pct / sh_base if sh_base > 0 else 0
        print(f"  pos={p_label}: sh={n}/{total} = {pct*100:.2f}% ({enr:.2f}×)")

    # Most common words at first-line positions 1 and 2
    print("\nTop words at first-line positions:")
    for pos_label in ['1', '2']:
        top = a_fl_pos_onset[pos_label].most_common(5) if False else None
        word_at_pos = Counter()
        for para in paragraphs:
            if para['dialect'] != 'A' or not para['lines']:
                continue
            first_line = para['lines'][0]
            p = int(pos_label)
            if len(first_line) > p:
                word_at_pos[first_line[p]] += 1
        print(f"  Position {pos_label}: {word_at_pos.most_common(8)}")

    # After PS, what's the very next word? (pos=1, line_idx=0)
    print("\nA PS→next word transition (first-line pos=0→pos=1):")
    ps_to_next_onset = Counter()
    ps_to_next_word = Counter()
    for para in paragraphs:
        if para['dialect'] != 'A' or not para['lines']:
            continue
        first_line = para['lines'][0]
        if len(first_line) >= 2:
            ps_to_next_onset[get_onset(first_line[1])] += 1
            ps_to_next_word[first_line[1]] += 1
    total_next = sum(ps_to_next_onset.values())
    print(f"  n={total_next} transitions")
    for onset in sorted(a_total_onset, key=lambda o: -ps_to_next_onset.get(o, 0)):
        n = ps_to_next_onset.get(onset, 0)
        if n < 2:
            continue
        pct = n / total_next
        base = a_total_onset.get(onset, 0) / a_total if a_total > 0 else 0
        enr = pct / base if base > 0 else 0
        print(f"  {onset}: {n} ({pct*100:.1f}%, base {base*100:.1f}%, {enr:.2f}×)")
    print(f"\n  Top PS→next words: {ps_to_next_word.most_common(10)}")

# ============================================================
# H392: B Para-Terminal Formula — What Is Enriched at B PF-LL?
# ============================================================
def h392_b_para_terminal(paragraphs):
    print("\n=== H392: B Para-Terminal Formula (pf_ll position) ===")

    b_pf_word = Counter()
    b_pf_onset = Counter()
    b_pf_total = 0

    b_all_word = Counter()
    b_all_onset = Counter()
    b_all_total = 0

    b_pf_by_section = defaultdict(Counter)

    # Also: A pf_ll for comparison
    a_pf_word = Counter()
    a_pf_onset = Counter()
    a_pf_total = 0
    a_all_onset = Counter()
    a_all_total = 0

    for para in paragraphs:
        lines = para['lines']
        if not lines:
            continue
        n_lines = len(lines)
        last_line = lines[-1]
        if not last_line:
            continue
        pf_word = last_line[-1] if len(last_line) > 1 else last_line[0]
        # But we want the actual LL word of the last line
        # In the positional framework, pf_ll = pos=n-1, line_idx=n_lines-1

        if para['dialect'] == 'B':
            for line in lines:
                for w in line:
                    b_all_word[w] += 1
                    b_all_onset[get_onset(w)] += 1
                    b_all_total += 1
            # pf_ll: last word of last line
            if len(last_line) > 1:
                pf_w = last_line[-1]
                b_pf_word[pf_w] += 1
                b_pf_onset[get_onset(pf_w)] += 1
                b_pf_total += 1
                b_pf_by_section[para['section']][pf_w] += 1
        elif para['dialect'] == 'A':
            for line in lines:
                for w in line:
                    a_all_onset[get_onset(w)] += 1
                    a_all_total += 1
            if len(last_line) > 1:
                pf_w = last_line[-1]
                a_pf_word[pf_w] += 1
                a_pf_onset[get_onset(pf_w)] += 1
                a_pf_total += 1

    print(f"\nB pf_ll total: {b_pf_total} (out of 101 B paragraphs)")
    print(f"A pf_ll total: {a_pf_total} (out of 163 A paragraphs)")

    print("\nB pf_ll onset distribution vs all-B baseline:")
    print(f"{'Onset':<8} {'pf_n':>5} {'pf%':>7} {'base%':>7} {'Enr':>6}")
    for onset in sorted(b_all_onset, key=lambda o: -b_pf_onset.get(o, 0)):
        n = b_pf_onset.get(onset, 0)
        if n < 1:
            continue
        pf_pct = n / b_pf_total
        base_pct = b_all_onset[onset] / b_all_total
        enr = pf_pct / base_pct if base_pct > 0 else 0
        print(f"{onset:<8} {n:>5} {pf_pct*100:>6.2f}% {base_pct*100:>6.2f}% {enr:>6.2f}×")

    print("\nTop 20 B pf_ll words:")
    for word, n in b_pf_word.most_common(20):
        total_in_b = b_all_word[word]
        pf_rate = n / b_pf_total
        base_rate = total_in_b / b_all_total
        enr = pf_rate / base_rate if base_rate > 0 else 0
        print(f"  {word}: pf={n}, total_b={total_in_b}, pf%={pf_rate*100:.2f}%, base%={base_rate*100:.2f}%, {enr:.2f}×")

    print("\nA pf_ll onset distribution vs all-A baseline:")
    print(f"{'Onset':<8} {'pf_n':>5} {'pf%':>7} {'base%':>7} {'Enr':>6}")
    for onset in sorted(a_all_onset, key=lambda o: -a_pf_onset.get(o, 0)):
        n = a_pf_onset.get(onset, 0)
        if n < 1:
            continue
        pf_pct = n / a_pf_total
        base_pct = a_all_onset[onset] / a_all_total
        enr = pf_pct / base_pct if base_pct > 0 else 0
        print(f"{onset:<8} {n:>5} {pf_pct*100:>6.2f}% {base_pct*100:>6.2f}% {enr:>6.2f}×")

    print("\nTop 20 A pf_ll words:")
    a_pf_word_full = Counter()
    a_all_word = Counter()
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        lines = para['lines']
        if not lines:
            continue
        last_line = lines[-1]
        for w in [w for line in lines for w in line]:
            a_all_word[w] += 1
        if len(last_line) > 1:
            a_pf_word_full[last_line[-1]] += 1
    for word, n in a_pf_word_full.most_common(20):
        total = a_all_word.get(word, 0)
        pf_rate = n / a_pf_total if a_pf_total > 0 else 0
        base = total / a_all_total if a_all_total > 0 else 0
        enr = pf_rate / base if base > 0 else 0
        print(f"  {word}: pf={n}, total_a={total}, pf%={pf_rate*100:.2f}%, base%={base*100:.2f}%, {enr:.2f}×")

    print("\nB pf_ll by section:")
    for section, words in sorted(b_pf_by_section.items()):
        total_sec = sum(words.values())
        print(f"  {section}: n={total_sec} — top words: {words.most_common(5)}")

def main():
    print("Parsing corpus...")
    paragraphs, folio_dialect = parse_corpus()
    A_count = sum(1 for p in paragraphs if p['dialect'] == 'A')
    B_count = sum(1 for p in paragraphs if p['dialect'] == 'B')
    print(f"Paragraphs: A={A_count}, B={B_count}, total={len(paragraphs)}")

    h390_a_para_opening(paragraphs)
    h391_a_first_line_sequence(paragraphs)
    h392_b_para_terminal(paragraphs)

if __name__ == '__main__':
    main()
