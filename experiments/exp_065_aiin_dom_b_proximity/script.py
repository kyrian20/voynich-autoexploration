"""
exp_065: Is the Aiin-Dominant Herbal A Sub-Dialect Closer to Currier B? (H077)
Compare aiin-dominant herbal A folios to:
1. y-dominant herbal A folios
2. Currier B herbal folios
3. Currier B overall
Measure vocabulary Jaccard and frequency-rank Spearman correlation.
"""

import re
from collections import Counter, defaultdict
import math

DATA_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"

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
            text = line[m.end():].strip()
            text = clean_text(text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]
            if not tokens:
                continue
            records.append({'folio': folio_id, 'currier': current_currier, 'section': current_section, 'words': tokens})
    return records

def jaccard(c1, c2):
    t1, t2 = set(c1.keys()), set(c2.keys())
    return len(t1 & t2) / max(len(t1 | t2), 1)

def spearman(c1, c2, top_n=100):
    """Compute Spearman rank correlation of top_n words shared by both."""
    shared = set(c1.keys()) & set(c2.keys())
    if len(shared) < 10:
        return float('nan')

    # Get top-N overall combined
    combined = Counter()
    for w in shared:
        combined[w] = c1[w] + c2[w]
    top_words = [w for w, _ in combined.most_common(top_n)]

    r1 = {w: rank for rank, w in enumerate(sorted(top_words, key=lambda x: -c1.get(x, 0)))}
    r2 = {w: rank for rank, w in enumerate(sorted(top_words, key=lambda x: -c2.get(x, 0)))}

    n = len(top_words)
    mean_r = (n - 1) / 2
    d2 = sum((r1[w] - r2[w])**2 for w in top_words)
    rho = 1 - 6 * d2 / (n * (n**2 - 1))
    return rho

def main():
    records = parse_corpus(DATA_PATH)

    # Build corpora
    corpora = {
        'aiin_dom_A': Counter(),
        'y_dom_A': Counter(),
        'herbal_B': Counter(),
        'all_B': Counter(),
        'all_A': Counter(),
    }

    for r in records:
        folio = r['folio']
        currier = r['currier']
        section = r['section']
        for w in r['words']:
            if currier == 'A' and section == 'H':
                if folio in AIIN_DOMINANT:
                    corpora['aiin_dom_A'][w] += 1
                elif folio in Y_DOMINANT:
                    corpora['y_dom_A'][w] += 1
            if currier == 'B':
                corpora['all_B'][w] += 1
                if section == 'H':
                    corpora['herbal_B'][w] += 1
            if currier == 'A':
                corpora['all_A'][w] += 1

    for name, c in corpora.items():
        print(f"{name}: {sum(c.values())} tokens, {len(c)} types")

    print(f"\n{'='*60}")
    print("VOCABULARY JACCARD OVERLAPS")
    print(f"{'='*60}")

    comparisons = [
        ('aiin_dom_A', 'y_dom_A', 'aiin-dom A vs y-dom A'),
        ('aiin_dom_A', 'all_B', 'aiin-dom A vs all B'),
        ('aiin_dom_A', 'herbal_B', 'aiin-dom A vs herbal B'),
        ('y_dom_A', 'all_B', 'y-dom A vs all B'),
        ('y_dom_A', 'herbal_B', 'y-dom A vs herbal B'),
        ('all_A', 'all_B', 'all A vs all B (baseline)'),
    ]

    for c1_name, c2_name, label in comparisons:
        j = jaccard(corpora[c1_name], corpora[c2_name])
        rho = spearman(corpora[c1_name], corpora[c2_name], top_n=50)
        n1 = len(corpora[c1_name])
        n2 = len(corpora[c2_name])
        shared = len(set(corpora[c1_name].keys()) & set(corpora[c2_name].keys()))
        print(f"\n{label}:")
        print(f"  Types: {n1} vs {n2}, shared={shared}, Jaccard={j:.3f}")
        print(f"  Spearman rho (top 50 shared): {rho:.3f}")

    # Top shared words: aiin-dom A and all B
    print(f"\n{'='*60}")
    print("TOP SHARED WORDS: aiin-dom A and all B")
    print(f"{'='*60}")
    aiin_c = corpora['aiin_dom_A']
    b_c = corpora['all_B']
    n_a = sum(aiin_c.values())
    n_b = sum(b_c.values())
    shared_words = [(w, aiin_c[w], b_c[w]) for w in set(aiin_c.keys()) & set(b_c.keys()) if aiin_c[w] >= 3]
    shared_words.sort(key=lambda x: -x[1])
    print(f"{'Word':<16} {'AiinA':>7} {'AiinA%':>8} {'B':>7} {'B%':>7}")
    for w, ac, bc in shared_words[:20]:
        print(f"{w:<16} {ac:>7} {100*ac/n_a:>7.2f}% {bc:>7} {100*bc/n_b:>7.2f}%")

    # Words exclusive to aiin-dom A (not in B at all)
    print(f"\n{'='*60}")
    print("WORDS IN aiin-dom A BUT NOT IN Currier B")
    print(f"{'='*60}")
    aiin_excl = [(w, c) for w, c in aiin_c.items() if w not in b_c and c >= 3]
    aiin_excl.sort(key=lambda x: -x[1])
    print(f"Count: {len(aiin_excl)}")
    for w, c in aiin_excl[:15]:
        print(f"  {w}: {c} ({100*c/n_a:.2f}%)")

    # Words in B but not aiin-dom A
    print(f"\n{'='*60}")
    print("WORDS IN ALL B BUT NOT aiin-dom A (top by B freq)")
    print(f"{'='*60}")
    b_excl = [(w, c) for w, c in b_c.items() if w not in aiin_c and c >= 10]
    b_excl.sort(key=lambda x: -x[1])
    print(f"Count: {len(b_excl)}")
    for w, c in b_excl[:15]:
        print(f"  {w}: {c} ({100*c/n_b:.2f}%)")

    # Suffix distribution comparison
    print(f"\n{'='*60}")
    print("SUFFIX DISTRIBUTION: aiin-dom A vs all B vs y-dom A")
    print(f"{'='*60}")
    SUFFIX_LIST = ['aiin', 'ain', 'eedy', 'edy', 'chy', 'eey', 'dy', 'ey', 'y', 'ol', 'or', 'al', 'ar', 'iin', 'in']
    def suffix_dist(counter):
        def suf(w):
            for s in SUFFIX_LIST:
                if w.endswith(s) and len(w) > len(s):
                    return s
            return '(none)'
        d = Counter(suf(w) for w, c in counter.items() for _ in range(c))
        n = sum(d.values())
        return {k: v/n for k, v in d.items()}

    aiin_suf = suffix_dist(aiin_c)
    b_suf = suffix_dist(b_c)
    y_suf = suffix_dist(corpora['y_dom_A'])
    print(f"{'Suffix':<8} {'AiinA%':>8} {'y-domA%':>9} {'AllB%':>8}")
    for suf in SUFFIX_LIST + ['(none)']:
        ap = aiin_suf.get(suf, 0)
        yp = y_suf.get(suf, 0)
        bp = b_suf.get(suf, 0)
        if ap > 0.02 or yp > 0.02 or bp > 0.02:
            print(f"{suf:<8} {100*ap:>7.1f}% {100*yp:>8.1f}% {100*bp:>7.1f}%")

if __name__ == '__main__':
    main()
