"""
exp_066: Word Length by Line Position (H081) + Register Entropy (H079)
H081: Does Voynichese use word LENGTH as a positional signal?
H079: Does the aiin-dominant register have higher or lower entropy than y-dominant?
"""

import re
from collections import Counter, defaultdict
import math

DATA_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"
SUFFIX_LIST = ['aiin', 'ain', 'eedy', 'edy', 'chy', 'eey', 'dy', 'ey', 'y', 'ol', 'or', 'al', 'ar', 'iin', 'in']

AIIN_DOMINANT = {'f20r', 'f22r', 'f30v', 'f32r', 'f32v', 'f35r', 'f42r', 'f42v',
                 'f45r', 'f47r', 'f47v', 'f49r', 'f4r', 'f8v'}
Y_DOMINANT = {'f16v', 'f17r', 'f17v', 'f18r', 'f19v', 'f24r', 'f24v', 'f36v',
              'f37r', 'f3r', 'f3v', 'f44r', 'f44v', 'f51r', 'f52v', 'f53v',
              'f6r', 'f6v', 'f87v', 'f93r', 'f96v', 'f9v'}

def clean_text(text):
    return re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)

def is_body_locus(locus_code):
    base = locus_code.lstrip('+*@=/~&')
    return base.startswith('P')

def parse_corpus(path):
    records = []
    current_currier = None
    current_section = None
    with open(path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue
            m_c = re.search(r'\$L=([AB])', line)
            if m_c:
                current_currier = m_c.group(1)
            m_s = re.search(r'\$I=([A-Z]+)', line)
            if m_s:
                current_section = m_s.group(1)
            m = re.match(r'^<([^>]+)>', line)
            if not m:
                continue
            locus_raw = m.group(1)
            parts = locus_raw.split(',')
            if len(parts) < 2:
                continue
            folio_raw = parts[0].strip()
            locus_code = parts[1].strip()
            folio_id = folio_raw.split('.')[0] if '.' in folio_raw else folio_raw
            if not is_body_locus(locus_code):
                continue
            line_type = 'para_start' if locus_code.startswith('@') else ('continuation' if locus_code.startswith('+') else 'other')
            text = line[m.end():].strip()
            text = clean_text(text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]
            if not tokens:
                continue
            records.append({'folio': folio_id, 'currier': current_currier, 'section': current_section,
                            'line_type': line_type, 'words': tokens})
    return records

def entropy(counter):
    n = sum(counter.values())
    if n == 0:
        return 0.0
    return -sum((c/n) * math.log2(c/n) for c in counter.values() if c > 0)

def main():
    records = parse_corpus(DATA_PATH)

    # H081: Word length by line position
    print("="*70)
    print("H081: WORD LENGTH BY LINE POSITION")
    print("="*70)

    for dialect in ['A', 'B']:
        lines = [r for r in records if r['currier'] == dialect]
        ps_lines = [r for r in lines if r['line_type'] == 'para_start']
        cont_lines = [r for r in lines if r['line_type'] == 'continuation']

        # Collect lengths by position
        pos_lengths = {
            'para_start_first': [],
            'cont_first': [],
            'medial': [],
            'last': [],
            'all': [],
        }

        for l in lines:
            words = l['words']
            n = len(words)
            if n == 0:
                continue
            pos_lengths['last'].append(len(words[-1]))
            pos_lengths['all'].extend(len(w) for w in words)
            if l['line_type'] == 'para_start':
                pos_lengths['para_start_first'].append(len(words[0]))
            else:
                pos_lengths['cont_first'].append(len(words[0]))
            for w in words[1:-1]:
                pos_lengths['medial'].append(len(w))

        print(f"\nCurrier {dialect}:")
        print(f"{'Position':<22} {'Count':>7} {'Mean_len':>9} {'Median':>8}")
        for pos_name, lengths in pos_lengths.items():
            if not lengths:
                continue
            mean_l = sum(lengths) / len(lengths)
            sorted_l = sorted(lengths)
            median_l = sorted_l[len(sorted_l)//2]
            print(f"{pos_name:<22} {len(lengths):>7} {mean_l:>8.2f} {median_l:>8}")

        # Length distribution for key positions
        print(f"\n  Length distribution (para_start_first vs cont_first vs last):")
        for pos in ['para_start_first', 'cont_first', 'last', 'all']:
            lengths = pos_lengths[pos]
            dist = Counter(lengths)
            n = len(lengths)
            print(f"  {pos}: ", end='')
            for l in sorted(dist.keys())[:15]:
                print(f"{l}:{100*dist[l]/n:.0f}%", end=' ')
            print()

    # H079: Entropy comparison: aiin-dominant vs y-dominant herbal A
    print(f"\n{'='*70}")
    print("H079: ENTROPY COMPARISON — HERBAL A REGISTERS")
    print(f"{'='*70}")

    aiin_words = []
    y_words = []
    for r in records:
        if r['currier'] == 'A' and r['section'] == 'H':
            if r['folio'] in AIIN_DOMINANT:
                aiin_words.extend(r['words'])
            elif r['folio'] in Y_DOMINANT:
                y_words.extend(r['words'])

    aiin_c = Counter(aiin_words)
    y_c = Counter(y_words)
    n_aiin = len(aiin_words)
    n_y = len(y_words)

    # Unigram entropy
    h1_aiin = entropy(aiin_c)
    h1_y = entropy(y_c)

    # TTR
    ttr_aiin = len(aiin_c) / max(n_aiin, 1)
    ttr_y = len(y_c) / max(n_y, 1)

    # Bigram entropy
    def bigram_h(words):
        bigrams = Counter(zip(words[:-1], words[1:]))
        unigrams = Counter(words)
        h_cond = 0.0
        n = sum(unigrams.values())
        for (w1, w2), count in bigrams.items():
            p_joint = count / max(n, 1)
            p_w1 = unigrams[w1] / max(n, 1)
            if p_joint > 0 and p_w1 > 0:
                h_cond -= p_joint * math.log2(p_joint / p_w1)
        return h_cond

    h2_aiin = bigram_h(aiin_words)
    h2_y = bigram_h(y_words)

    # Mean word length
    mwl_aiin = sum(len(w) for w in aiin_words) / max(n_aiin, 1)
    mwl_y = sum(len(w) for w in y_words) / max(n_y, 1)

    print(f"\n{'Metric':<25} {'Aiin-dom A':>12} {'y-dom A':>12}")
    print(f"{'Tokens':<25} {n_aiin:>12} {n_y:>12}")
    print(f"{'Types':<25} {len(aiin_c):>12} {len(y_c):>12}")
    print(f"{'TTR':<25} {ttr_aiin:>11.3f} {ttr_y:>11.3f}")
    print(f"{'h1 (unigram entropy)':<25} {h1_aiin:>11.3f} {h1_y:>11.3f}")
    print(f"{'h2 (bigram cond H)':<25} {h2_aiin:>11.3f} {h2_y:>11.3f}")
    print(f"{'Mean word length':<25} {mwl_aiin:>11.2f} {mwl_y:>11.2f}")

    # Word length comparison between registers
    print(f"\nWord length distribution:")
    aiin_len = Counter(len(w) for w in aiin_words)
    y_len = Counter(len(w) for w in y_words)
    print(f"{'Length':<8} {'Aiin%':>7} {'y%':>7}")
    for l in range(2, 15):
        ap = aiin_len.get(l, 0) / n_aiin
        yp = y_len.get(l, 0) / n_y
        if ap > 0.01 or yp > 0.01:
            print(f"{l:<8} {100*ap:>6.1f}% {100*yp:>6.1f}%")

if __name__ == '__main__':
    main()
