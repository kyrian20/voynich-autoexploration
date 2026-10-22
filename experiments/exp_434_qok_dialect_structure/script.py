"""
exp_434: qok Vocabulary A vs B Internal Structure (H498)

Q: What drives A-qok MLen=1.34 vs B-qok MLen=0.52 (from F288)?
   Is the A midfix length difference driven by a few high-frequency qok forms,
   or is it uniformly distributed across qok word types?

Method:
- Parse ZL3B corpus; classify A/B dialects
- For all qok-onset words in each dialect, compute:
  (a) Top-20 word types by frequency
  (b) Mean character length of full word
  (c) Midfix length (onset stripped, suffix stripped from defined suffix list)
  (d) Suffix distribution
  (e) Type-token structure
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

# Suffix list for stripping (longest-match approach)
SUFFIXES = [
    'aiin', 'aiir', 'ain', 'air', 'aii',
    'eedy', 'edy', 'eey', 'ey',
    'ckhy', 'ckh', 'cthy', 'cth',
    'dy', 'y',
    'ar', 'or', 'ol', 'al',
    'am', 'om',
    'iin', 'iir', 'in',
    'cheol', 'cheor', 'chedy', 'chey', 'cho', 'ch',
    'shedy', 'shey', 'sho', 'sh',
    'l', 'r', 'n',
]
SUFFIXES.sort(key=lambda x: -len(x))  # longest first

def strip_suffix(word_body):
    """Strip longest known suffix from word body. Returns (midfix, suffix)."""
    for s in SUFFIXES:
        if word_body.endswith(s) and len(word_body) > len(s):
            return word_body[:-len(s)], s
        elif word_body == s:
            return '', s
    return word_body, ''  # no recognized suffix

QOK_ONSET = 'qok'
QOK_LEN = len(QOK_ONSET)  # 3

def parse_corpus():
    """Parse ZL3B, return dict: folio -> list of (locus, [words])"""
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
                    folios[folio].append((lc, words))
    return folios

def classify_dialects(folios):
    """Classify each folio as A or B by edy/eedy rate ≥5%."""
    dialect = {}
    for folio, lines in folios.items():
        total = sum(len(ws) for _, ws in lines)
        if total == 0:
            continue
        edy = sum(1 for _, ws in lines for w in ws
                  if w.endswith('edy') or w.endswith('eedy'))
        dialect[folio] = 'B' if edy / total >= 0.05 else 'A'
    return dialect

def get_onset(word):
    """Return onset priority, consistent with project conventions."""
    ONSETS = ['qok', 'qot', 'qo', 'cth', 'ch', 'sh', 'ok', 'ot', 'ol',
              'd', 's', 'y', 'k', 't', 'l', 'r', 'p', 'f', 'o']
    for on in ONSETS:
        if word.startswith(on):
            return on
    return 'other'

def analyze_qok_words(folios, dialect_map, target_dialect):
    """Collect all qok-onset words and analyze structure."""
    words_all = []
    for folio, lines in folios.items():
        if dialect_map.get(folio) != target_dialect:
            continue
        for _, ws in lines:
            for w in ws:
                if get_onset(w) == 'qok':
                    words_all.append(w)
    return words_all

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)

    n_a = sum(1 for d in dialect_map.values() if d == 'A')
    n_b = sum(1 for d in dialect_map.values() if d == 'B')
    print(f"Folios: A={n_a}, B={n_b}")

    for dial in ['A', 'B']:
        words = analyze_qok_words(folios, dialect_map, dial)
        if not words:
            print(f"\n{dial}: No qok words found")
            continue

        counter = Counter(words)
        total = len(words)
        n_types = len(counter)
        hapax = sum(1 for c in counter.values() if c == 1)

        print(f"\n{'='*60}")
        print(f"DIALECT {dial} — qok-onset words")
        print(f"Total tokens: {total}, Unique types: {n_types}, Hapax: {hapax} ({hapax/n_types:.1%})")

        # Word length distribution
        word_lens = [len(w) for w in words]
        mean_len = sum(word_lens) / len(word_lens)
        print(f"Mean word length (chars): {mean_len:.2f}")

        # Midfix analysis: strip 'qok' onset, then strip suffix
        midfixes = []
        suffixes_found = []
        for w in words:
            body = w[QOK_LEN:]  # strip 'qok'
            mf, sf = strip_suffix(body)
            midfixes.append(mf)
            suffixes_found.append(sf)

        mf_lens = [len(mf) for mf in midfixes]
        mean_mf_len = sum(mf_lens) / len(mf_lens)
        zero_mf = sum(1 for mf in midfixes if mf == '')
        print(f"Mean midfix length: {mean_mf_len:.2f} (vs F288: A=1.34, B=0.52)")
        print(f"Zero-midfix fraction: {zero_mf}/{total} = {zero_mf/total:.1%}")

        # Top midfixes
        mf_counter = Counter(midfixes)
        print(f"Top midfix forms: {mf_counter.most_common(10)}")

        # Top suffixes
        sf_counter = Counter(suffixes_found)
        print(f"Top suffixes: {sf_counter.most_common(10)}")

        # Top word types
        print(f"\nTop 20 qok-onset word types:")
        for word, count in counter.most_common(20):
            body = word[QOK_LEN:]
            mf, sf = strip_suffix(body)
            print(f"  {word}: {count} ({count/total:.1%}) | midfix='{mf}' suffix='{sf}'")

        # Midfix length distribution
        mf_len_dist = Counter(mf_lens)
        print(f"\nMidfix length distribution:")
        for mf_l in sorted(mf_len_dist.keys()):
            print(f"  len={mf_l}: {mf_len_dist[mf_l]} ({mf_len_dist[mf_l]/total:.1%})")

        # Key question: are the long midfixes in A concentrated in a few types?
        # High-midfix words: mf_len >= 2
        long_mf = [(w, mf, c) for (w, c), mf in zip(counter.most_common(),
                   [strip_suffix(w[QOK_LEN:])[0] for w in counter.keys()])
                   if len(mf) >= 2]
        print(f"\nWords with midfix len≥2 (top 10):")
        for w, mf, c in sorted(long_mf, key=lambda x: -x[2])[:10]:
            print(f"  {w}: N={c}, midfix='{mf}'")

if __name__ == '__main__':
    main()
