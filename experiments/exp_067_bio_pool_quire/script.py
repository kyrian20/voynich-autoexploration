"""
exp_067: Bio Pool vs Non-Pool Two-Register Test (H082) + pch/tch Quire Distribution (H080)
H082: Do pool folios (multi-paragraph bio) differ in vocabulary/grammar from non-pool bio folios?
H080: Are pch/tch onset words concentrated in specific Currier B quires?
"""

import re
from collections import Counter, defaultdict

DATA_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"
SUFFIX_LIST = ['aiin', 'ain', 'eedy', 'edy', 'chy', 'eey', 'dy', 'ey', 'y', 'ol', 'or', 'al', 'ar', 'iin', 'in']

# Bio pool folios (multi-paragraph bio): from exp_061
POOL_FOLIOS = {'f83r', 'f84v', 'f75v', 'f75r', 'f82r', 'f83v', 'f84r'}

def suffix_group(word):
    for suf in SUFFIX_LIST:
        if word.endswith(suf) and len(word) > len(suf):
            return suf
    return None

def clean_text(text):
    return re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)

def is_body_locus(locus_code):
    base = locus_code.lstrip('+*@=/~&')
    return base.startswith('P')

def parse_corpus(path):
    records = []
    current_currier = None
    current_section = None
    current_quire = None
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
            m_q = re.search(r'\$Q=([^\s,]+)', line)
            if m_q:
                current_quire = m_q.group(1)
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
            records.append({'folio': folio_id, 'currier': current_currier, 'section': current_section,
                            'quire': current_quire, 'words': tokens})
    return records

def jaccard(c1, c2):
    t1, t2 = set(c1.keys()), set(c2.keys())
    return len(t1 & t2) / max(len(t1 | t2), 1)

def main():
    records = parse_corpus(DATA_PATH)

    # H082: Bio pool vs non-pool vocabulary comparison
    print("="*70)
    print("H082: BIO POOL vs NON-POOL FOLIO VOCABULARY COMPARISON")
    print("="*70)

    pool_words = []
    nonpool_words = []

    for r in records:
        if r['currier'] == 'B' and r['section'] == 'B':  # Bio section
            if r['folio'] in POOL_FOLIOS:
                pool_words.extend(r['words'])
            else:
                nonpool_words.extend(r['words'])

    pool_c = Counter(pool_words)
    nonpool_c = Counter(nonpool_words)
    n_pool = len(pool_words)
    n_nonpool = len(nonpool_words)

    print(f"\nPool folios: {n_pool} tokens, {len(pool_c)} types")
    print(f"Non-pool folios: {n_nonpool} tokens, {len(nonpool_c)} types")
    print(f"Jaccard: {jaccard(pool_c, nonpool_c):.3f}")

    # Suffix distribution
    pool_suf = Counter(suffix_group(w) or '(none)' for w in pool_words)
    nonpool_suf = Counter(suffix_group(w) or '(none)' for w in nonpool_words)

    print(f"\n--- SUFFIX DISTRIBUTION ---")
    print(f"{'Suffix':<8} {'Pool%':>7} {'NonPool%':>9} {'Ratio':>7}")
    for suf in SUFFIX_LIST[:12] + ['(none)']:
        pp = pool_suf.get(suf, 0) / max(n_pool, 1)
        np = nonpool_suf.get(suf, 0) / max(n_nonpool, 1)
        ratio = pp / max(np, 1e-10)
        if pp > 0.02 or np > 0.02:
            print(f"{suf:<8} {100*pp:>6.1f}% {100*np:>8.1f}% {ratio:>7.2f}×")

    # Top words in pool vs non-pool
    print(f"\n--- TOP POOL WORDS (over-represented vs non-pool) ---")
    print(f"{'Word':<16} {'Pool':>6} {'Pool%':>7} {'NonPool':>8} {'NonPool%':>9} {'Ratio':>7}")
    over = [(w, c, pool_c[w], nonpool_c.get(w,0)) for w, c in pool_c.items()
            if c >= 5 and c/n_pool > (nonpool_c.get(w,0)/max(n_nonpool,1)) * 2.0]
    over.sort(key=lambda x: -(x[1]/n_pool) / max(nonpool_c.get(x[0],0)/max(n_nonpool,1), 1e-10))
    for w, _, pc, npc in over[:15]:
        pp = pc/n_pool
        np = npc/max(n_nonpool,1)
        ratio = pp/max(np, 1e-10)
        print(f"{w:<16} {pc:>6} {100*pp:>6.2f}% {npc:>8} {100*np:>8.2f}% {ratio:>7.2f}×")

    print(f"\n--- TOP NON-POOL WORDS (over-represented vs pool) ---")
    over2 = [(w, c) for w, c in nonpool_c.items()
             if c >= 10 and c/n_nonpool > (pool_c.get(w,0)/max(n_pool,1)) * 2.0]
    over2.sort(key=lambda x: -(x[1]/n_nonpool) / max(pool_c.get(x[0],0)/max(n_pool,1), 1e-10))
    for w, npc in over2[:15]:
        pc = pool_c.get(w, 0)
        np = npc/n_nonpool
        pp = pc/max(n_pool,1)
        ratio = np/max(pp, 1e-10)
        print(f"{w:<16} {npc:>6} {100*np:>6.2f}% {pc:>8} {100*pp:>8.2f}% {ratio:>7.2f}×")

    # qo-rate comparison
    print(f"\n--- qo-RATE AND ONSET DISTRIBUTION ---")
    def qo_rate(words):
        return sum(1 for w in words if w.startswith('qo')) / max(len(words), 1)
    print(f"  Pool qo-rate: {100*qo_rate(pool_words):.1f}%")
    print(f"  Non-pool qo-rate: {100*qo_rate(nonpool_words):.1f}%")

    # H080: pch/tch quire distribution in B
    print(f"\n{'='*70}")
    print("H080: pch/tch ONSET QUIRE DISTRIBUTION IN CURRIER B")
    print(f"{'='*70}")

    quire_data = defaultdict(lambda: {'total': 0, 'pch': 0, 'tch': 0, 'p_other': 0})
    for r in records:
        if r['currier'] == 'B':
            q = r['quire'] or '?'
            for w in r['words']:
                quire_data[q]['total'] += 1
                if w.startswith('pch'):
                    quire_data[q]['pch'] += 1
                elif w.startswith('tch'):
                    quire_data[q]['tch'] += 1
                elif w.startswith('p') and not w.startswith('pch'):
                    quire_data[q]['p_other'] += 1

    print(f"\n{'Quire':>8} {'Total':>7} {'pch':>5} {'pch%':>7} {'tch':>5} {'tch%':>7} {'p_other':>8} {'p_other%':>9}")
    for q in sorted(quire_data.keys()):
        d = quire_data[q]
        n = d['total']
        pch_p = d['pch'] / max(n, 1)
        tch_p = d['tch'] / max(n, 1)
        po_p = d['p_other'] / max(n, 1)
        print(f"{q:>8} {n:>7} {d['pch']:>5} {100*pch_p:>6.2f}% {d['tch']:>5} {100*tch_p:>6.2f}% {d['p_other']:>8} {100*po_p:>8.2f}%")

if __name__ == '__main__':
    main()
