"""
exp_450: sh→qok Bigram Word-Level Analysis (H522)
Q: Is the sh→qok enrichment (E=1.97× B-dialect MID) driven by:
   (a) class-level grammar (all sh-words → all qok-words uniformly),
   (b) specific sh-words driving the enrichment (sh-word type selection), or
   (c) specific sh×qok word-type pairs (lexical co-occurrence)?

Method: Extract all sh→qok adjacent bigrams in B continuation lines (both MID).
   - Top sh-word types that precede qok-words
   - Top qok-word types that follow sh-words
   - For each top-5 sh-word: qok succession rate vs its baseline rate
   - Cross-dialect: same analysis for A-dialect
   - Concentration metric: fraction of sh→qok hits accounted for by top-3 sh-words
"""
from pathlib import Path as _RepositoryPath
import re
from collections import defaultdict, Counter

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

ONSETS = ['qok','qot','qo','cth','ch','sh','ok','ot','ol','d','s','y','k','t','l','r','p','f','o']

def get_onset(word):
    for on in ONSETS:
        if word.startswith(on):
            return on
    return 'other'

def parse_corpus():
    pattern = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
    folios = defaultdict(list)
    with open(ZL3B, encoding='utf-8') as f:
        for line in f:
            for m in pattern.finditer(line):
                folio = m.group(1).lstrip('+*=&~')
                lc = m.group(3).lstrip('+*=/~&')
                if not lc.lstrip('@').startswith('P'):
                    continue
                text = m.group(4).strip()
                words = [w for w in re.split(r'[-.\s]', text)
                         if re.match(r'^[a-z]+$', w) and len(w) >= 2]
                if words:
                    folios[folio].append(words)
    return folios

def classify_dialects(folios):
    dialect = {}
    for folio, lines in folios.items():
        total = sum(len(ws) for ws in lines)
        if total == 0: continue
        edy = sum(1 for ws in lines for w in ws
                  if w.endswith('edy') or w.endswith('eedy'))
        dialect[folio] = 'B' if edy / total >= 0.05 else 'A'
    return dialect

def collect_bigrams(folios, dialect_map, target_dialect):
    """Collect adjacent bigrams in MID positions of continuation lines."""
    # sh_qok_pairs: list of (sh_word, qok_word) pairs
    sh_qok_pairs = []
    # sh_all: all sh-word occurrences as predecessor in MID bigrams
    sh_next = defaultdict(Counter)  # sh_word -> next_word counts
    # overall MID bigrams for baseline
    total_mid_bigrams = 0
    sh_total = 0  # total sh predecessors in MID bigrams
    qok_as_successor = Counter()  # qok word frequencies as successor to anything
    sh_freq = Counter()  # sh word frequencies overall in MID
    qok_freq = Counter()  # qok word frequencies overall in MID

    for folio, lines in folios.items():
        if folio not in dialect_map or dialect_map[folio] != target_dialect:
            continue
        n = len(lines)
        if n < 3:
            continue
        cont_lines = lines[1:-1]
        cn = len(cont_lines)

        for ci, line_words in enumerate(cont_lines):
            # MID words: positions 1..n-2 (0-indexed: positions 1 to len-2)
            # For the within-line bigrams, check all adjacent pairs in MID
            # Position 0 = LF (first word), last = LL
            # MID = everything between LF and LL
            lw = len(line_words)
            if lw < 4:
                continue  # Need at least 2 MID words for MID bigrams

            # MID positions: index 1 through lw-2 (inclusive)
            mid_words = line_words[1:lw-1]
            for i, w in enumerate(mid_words):
                if get_onset(w) == 'sh':
                    sh_freq[w] += 1
                if get_onset(w) == 'qok':
                    qok_freq[w] += 1

            for i in range(len(mid_words) - 1):
                w1 = mid_words[i]
                w2 = mid_words[i+1]
                on1 = get_onset(w1)
                on2 = get_onset(w2)
                total_mid_bigrams += 1
                if on1 == 'sh':
                    sh_next[w1][w2] += 1
                    sh_total += 1
                    if on2 == 'qok':
                        sh_qok_pairs.append((w1, w2))
                if on2 == 'qok':
                    qok_as_successor[w2] += 1

    return sh_qok_pairs, sh_next, sh_total, total_mid_bigrams, qok_as_successor, sh_freq, qok_freq

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)

    for dialect in ['B', 'A']:
        print(f"\n{'='*60}")
        print(f"  {dialect}-DIALECT: sh→qok word-level analysis")
        print(f"{'='*60}")

        sh_qok_pairs, sh_next, sh_total, total_mid_bigrams, qok_as_successor, sh_freq, qok_freq = \
            collect_bigrams(folios, dialect_map, dialect)

        n_pairs = len(sh_qok_pairs)
        print(f"\nTotal sh→qok pairs (MID bigrams): N={n_pairs}")
        print(f"Total sh predecessor events: N={sh_total}")
        print(f"Total MID bigrams: N={total_mid_bigrams}")

        if sh_total == 0 or total_mid_bigrams == 0:
            print("  Insufficient data.")
            continue

        # Baseline P(qok_successor) = qok_as_successor.total / total_mid_bigrams
        total_qok_succ = sum(qok_as_successor.values())
        p_qok_succ = total_qok_succ / total_mid_bigrams
        expected_sh_qok = sh_total * p_qok_succ
        E_overall = n_pairs / expected_sh_qok if expected_sh_qok > 0 else 0
        print(f"P(qok successor | any) = {p_qok_succ:.3f}")
        print(f"Expected sh→qok under independence: {expected_sh_qok:.1f}")
        print(f"Observed/Expected E = {E_overall:.2f}×  (overall confirmation)")

        # Top sh-word types by frequency among sh→qok predecessors
        sh_qok_by_pred = Counter(w1 for w1, w2 in sh_qok_pairs)
        print(f"\nTop sh-word types as sh→qok predecessors:")
        print(f"  {'sh-word':<15} {'n(sh→qok)':>10} {'n(sh→any)':>10} {'qok_rate':>9} {'baseline':>9} {'E':>6}")
        sh_word_total_in_pairs = sum(sh_qok_by_pred.values())
        cumulative = 0
        for sh_word, count in sh_qok_by_pred.most_common(10):
            sh_total_w = sum(sh_next[sh_word].values())
            qok_rate = count / sh_total_w if sh_total_w > 0 else 0
            E_w = qok_rate / p_qok_succ if p_qok_succ > 0 else 0
            cumulative += count
            print(f"  {sh_word:<15} {count:>10} {sh_total_w:>10} {qok_rate:>9.3f} {p_qok_succ:>9.3f} {E_w:>6.2f}×")
        print(f"  Top-3 account for {sum(c for _, c in sh_qok_by_pred.most_common(3))}/{n_pairs} = "
              f"{sum(c for _, c in sh_qok_by_pred.most_common(3))/n_pairs:.1%} of sh→qok pairs")

        # Top qok-word types as successors to sh
        sh_qok_by_succ = Counter(w2 for w1, w2 in sh_qok_pairs)
        print(f"\nTop qok-word types as successors after sh:")
        print(f"  {'qok-word':<15} {'n(sh→qok-w)':>12} {'frac_of_sh→qok':>15}")
        for qok_word, count in sh_qok_by_succ.most_common(10):
            print(f"  {qok_word:<15} {count:>12} {count/n_pairs:>15.1%}")

        # Concentration test: for each top-5 sh-word, qok rate vs baseline
        print(f"\nConcentration test: specific sh-words' qok successor rate")
        top5_sh = [w for w, _ in sh_qok_by_pred.most_common(5)]
        # Also check top sh-words NOT in sh→qok list
        # Get top sh-words by overall frequency
        top_sh_by_freq = sh_freq.most_common(10)
        print(f"\n  Top sh-words by MID frequency:")
        print(f"  {'sh-word':<15} {'MID_freq':>9} {'n(→qok)':>8} {'qok_rate':>9} {'E_vs_base':>10}")
        for sh_word, freq in top_sh_by_freq:
            n_qok = sh_qok_by_pred.get(sh_word, 0)
            sh_tot = sum(sh_next[sh_word].values())
            rate = n_qok / sh_tot if sh_tot > 0 else 0
            E_w = rate / p_qok_succ if p_qok_succ > 0 else 0
            print(f"  {sh_word:<15} {freq:>9} {n_qok:>8} {rate:>9.3f} {E_w:>10.2f}×")

        # Top qok-words by frequency in MID — how often do they appear after sh vs non-sh?
        print(f"\nTop qok-words: frequency after sh vs. baseline")
        print(f"  {'qok-word':<15} {'sh→qok-w':>9} {'total_as_succ':>14} {'sh_rate':>9} {'base_rate':>10} {'E':>6}")
        for qok_word, total_s in qok_as_successor.most_common(10):
            after_sh = sh_qok_by_succ.get(qok_word, 0)
            sh_rate = after_sh / sh_total if sh_total > 0 else 0
            base_rate = total_s / total_mid_bigrams
            E_w = sh_rate / (base_rate if base_rate > 0 else 1)
            print(f"  {qok_word:<15} {after_sh:>9} {total_s:>14} {sh_rate:>9.4f} {base_rate:>10.4f} {E_w:>6.2f}×")

        # Specific pair analysis: most common (sh_word, qok_word) pairs
        pair_counts = Counter(sh_qok_pairs)
        print(f"\nMost common specific sh→qok pairs:")
        for (w1, w2), count in pair_counts.most_common(10):
            print(f"  {w1}→{w2}: N={count}")
        unique_pairs = len(pair_counts)
        print(f"Unique (sh, qok) pairs: {unique_pairs} / {n_pairs} total = "
              f"{unique_pairs/n_pairs:.1%} unique (class-level if >80%)")

if __name__ == '__main__':
    main()
