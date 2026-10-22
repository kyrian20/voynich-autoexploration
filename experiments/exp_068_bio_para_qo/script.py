"""
exp_068: Bio Paragraph Independence (H083) + qo-Onset Morphology (H084)
H083: Are paragraphs within multi-para bio folios independent vocabulary units?
H084: Do qo-onset words have a restricted morphological sub-grammar?
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')
SUFFIX_LIST = ['aiin', 'ain', 'eedy', 'edy', 'chy', 'eey', 'dy', 'ey', 'y', 'ol', 'or', 'al', 'ar', 'iin', 'in']

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

def parse_corpus_with_paragraphs(path):
    """
    Parse corpus, tracking paragraph index within each folio.
    Returns: list of records with folio, currier, section, quire, para_idx, words
    """
    records = []
    current_currier = None
    current_section = None
    current_quire = None
    # Track paragraph index per folio
    folio_para_counts = defaultdict(int)
    prev_folio = None
    current_para_idx = -1

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

            # Track paragraph index: a new para_start (@ prefix on locus) starts a new paragraph
            base_locus = locus_code.lstrip('+*=/~&')
            is_para_start = base_locus.startswith('@')

            if folio_id != prev_folio:
                current_para_idx = 0
                prev_folio = folio_id
            elif is_para_start and records and records[-1]['folio'] == folio_id:
                # New paragraph within same folio
                current_para_idx += 1

            text = line[m.end():].strip()
            text = clean_text(text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]
            if not tokens:
                continue
            records.append({
                'folio': folio_id,
                'currier': current_currier,
                'section': current_section,
                'quire': current_quire,
                'para_idx': current_para_idx,
                'is_para_start': is_para_start,
                'words': tokens
            })
    return records

def jaccard(c1, c2):
    t1, t2 = set(c1.keys()), set(c2.keys())
    return len(t1 & t2) / max(len(t1 | t2), 1)

def main():
    records = parse_corpus_with_paragraphs(DATA_PATH)

    # H083: Bio paragraph independence
    print("="*70)
    print("H083: BIO PARAGRAPH INDEPENDENCE — WITHIN-FOLIO PARAGRAPH JACCARD")
    print("="*70)

    # Find multi-para bio folios
    bio_records = [r for r in records if r['section'] == 'B' and r['currier'] == 'B']

    # Group by folio, then by para_idx
    folio_para_words = defaultdict(lambda: defaultdict(list))
    for r in bio_records:
        folio_para_words[r['folio']][r['para_idx']].extend(r['words'])

    multi_para_folios = {f: paras for f, paras in folio_para_words.items() if len(paras) > 1}
    single_para_folios = {f: paras for f, paras in folio_para_words.items() if len(paras) == 1}

    print(f"\nTotal bio folios: {len(folio_para_words)}")
    print(f"Multi-para bio folios: {len(multi_para_folios)}")
    print(f"Single-para bio folios: {len(single_para_folios)}")

    print(f"\n--- WITHIN-FOLIO INTER-PARAGRAPH JACCARD ---")
    print(f"{'Folio':<10} {'N_paras':>8} {'Para sizes':>12} {'Avg Jaccard':>12}")
    all_within_jaccards = []
    for folio in sorted(multi_para_folios.keys()):
        paras = multi_para_folios[folio]
        para_indices = sorted(paras.keys())
        n = len(para_indices)
        para_sizes = [len(paras[i]) for i in para_indices]
        # Pairwise Jaccard
        jacs = []
        for i in range(n):
            for j in range(i+1, n):
                c1 = Counter(paras[para_indices[i]])
                c2 = Counter(paras[para_indices[j]])
                jacs.append(jaccard(c1, c2))
        avg_jac = sum(jacs) / len(jacs) if jacs else 0
        all_within_jaccards.extend(jacs)
        sizes_str = '+'.join(str(s) for s in para_sizes)
        print(f"{folio:<10} {n:>8} {sizes_str:>12} {avg_jac:>11.3f}")

    if all_within_jaccards:
        print(f"\nMean within-folio inter-paragraph Jaccard: {sum(all_within_jaccards)/len(all_within_jaccards):.3f}")

    # Cross-folio Jaccard as baseline: random pairs of different folios
    print(f"\n--- CROSS-FOLIO JACCARD (random pairs, baseline) ---")
    all_bio_folios = list(folio_para_words.keys())
    cross_jacs = []
    import random
    random.seed(42)
    for _ in range(100):
        f1, f2 = random.sample(all_bio_folios, 2)
        all_w1 = []
        for ws in folio_para_words[f1].values():
            all_w1.extend(ws)
        all_w2 = []
        for ws in folio_para_words[f2].values():
            all_w2.extend(ws)
        cross_jacs.append(jaccard(Counter(all_w1), Counter(all_w2)))
    print(f"Mean cross-folio bio Jaccard: {sum(cross_jacs)/len(cross_jacs):.3f}")
    print(f"Cross-folio std: {(sum((x - sum(cross_jacs)/len(cross_jacs))**2 for x in cross_jacs)/len(cross_jacs))**0.5:.3f}")

    # Also compare consecutive vs non-consecutive paragraphs
    print(f"\n--- PARAGRAPH VOCABULARY OVERLAP DETAIL ---")
    for folio in sorted(multi_para_folios.keys())[:5]:  # detail for first 5
        paras = multi_para_folios[folio]
        para_indices = sorted(paras.keys())
        print(f"\n  {folio} ({len(para_indices)} paragraphs):")
        for idx in para_indices:
            words = paras[idx]
            top = Counter(words).most_common(5)
            print(f"    Para {idx} ({len(words)} tokens): {', '.join(f'{w}({c})' for w,c in top)}")
        # Show shared words between first and second para
        if len(para_indices) >= 2:
            c0 = Counter(paras[para_indices[0]])
            c1 = Counter(paras[para_indices[1]])
            shared = set(c0.keys()) & set(c1.keys())
            print(f"    Shared types (para 0 & 1): {len(shared)} of {len(set(c0.keys()) | set(c1.keys()))} = Jaccard {jaccard(c0,c1):.3f}")

    # H084: qo-onset morphology
    print(f"\n{'='*70}")
    print("H084: qo-ONSET MORPHOLOGY AND POSITIONAL GRAMMAR IN CURRIER B")
    print(f"{'='*70}")

    b_records = [r for r in records if r['currier'] == 'B']
    b_words = []
    for r in b_records:
        b_words.extend(r['words'])

    qo_words = [w for w in b_words if w.startswith('qo') and len(w) > 2]
    non_qo_words = [w for w in b_words if not w.startswith('qo')]

    print(f"\nCurrier B total words: {len(b_words)}")
    print(f"qo-onset words: {len(qo_words)} ({100*len(qo_words)/len(b_words):.1f}%)")

    # What follows 'qo'?
    post_qo = Counter(w[2] for w in qo_words if len(w) > 2)
    print(f"\n--- CHARACTER FOLLOWING 'qo' ---")
    for char, count in post_qo.most_common(15):
        pct = 100 * count / len(qo_words)
        print(f"  qo+'{char}': {count} ({pct:.1f}%)")

    # Full qo word inventory
    qo_counts = Counter(qo_words)
    print(f"\n--- TOP qo WORDS (Currier B) ---")
    print(f"{'Word':<16} {'Count':>6} {'%':>7}")
    for w, c in qo_counts.most_common(20):
        print(f"{w:<16} {c:>6} {100*c/len(b_words):>6.2f}%")

    # qo suffix distribution vs overall B suffix distribution
    qo_suf = Counter(suffix_group(w) or '(none)' for w in qo_words)
    all_suf = Counter(suffix_group(w) or '(none)' for w in b_words)
    n_qo = len(qo_words)
    n_all = len(b_words)

    print(f"\n--- qo SUFFIX DISTRIBUTION vs ALL B ---")
    print(f"{'Suffix':<8} {'qo%':>7} {'all B%':>8} {'Ratio':>7}")
    for suf in SUFFIX_LIST + ['(none)']:
        qp = qo_suf.get(suf, 0) / max(n_qo, 1)
        ap = all_suf.get(suf, 0) / max(n_all, 1)
        if qp > 0.03 or ap > 0.03:
            ratio = qp / max(ap, 1e-10)
            print(f"{suf:<8} {100*qp:>6.1f}% {100*ap:>7.1f}% {ratio:>7.2f}×")

    # qo positional grammar: line-first%, line-last%, para-start%
    print(f"\n--- qo POSITIONAL GRAMMAR ---")
    pos_stats = defaultdict(lambda: {'total': 0, 'qo': 0, 'para_start_first': 0, 'cont_first': 0, 'last': 0, 'medial': 0})

    total_words_pos = {'para_start_first': 0, 'cont_first': 0, 'last': 0, 'medial': 0, 'total': 0}
    qo_words_pos = {'para_start_first': 0, 'cont_first': 0, 'last': 0, 'medial': 0, 'total': 0}

    for r in b_records:
        ws = r['words']
        n = len(ws)
        if n == 0:
            continue
        pos_type_first = 'para_start_first' if r['is_para_start'] else 'cont_first'
        # First word
        total_words_pos[pos_type_first] += 1
        total_words_pos['total'] += 1
        if ws[0].startswith('qo') and len(ws[0]) > 2:
            qo_words_pos[pos_type_first] += 1
            qo_words_pos['total'] += 1
        # Last word (only if n > 1)
        if n > 1:
            total_words_pos['last'] += 1
            total_words_pos['total'] += 1
            if ws[-1].startswith('qo') and len(ws[-1]) > 2:
                qo_words_pos['last'] += 1
                qo_words_pos['total'] += 1
        # Medial words
        for w in ws[1:-1] if n > 2 else []:
            total_words_pos['medial'] += 1
            total_words_pos['total'] += 1
            if w.startswith('qo') and len(w) > 2:
                qo_words_pos['medial'] += 1
                qo_words_pos['total'] += 1

    overall_qo_rate = qo_words_pos['total'] / max(total_words_pos['total'], 1)
    print(f"\nOverall qo rate in B (positional sample): {100*overall_qo_rate:.2f}%")
    print(f"{'Position':<20} {'All words':>10} {'qo words':>10} {'qo%':>7} {'Enrichment':>11}")
    for pos in ['para_start_first', 'cont_first', 'medial', 'last']:
        n_tot = total_words_pos[pos]
        n_qo = qo_words_pos[pos]
        if n_tot == 0:
            continue
        qo_pct = n_qo / n_tot
        enrichment = qo_pct / max(overall_qo_rate, 1e-10)
        print(f"{pos:<20} {n_tot:>10} {n_qo:>10} {100*qo_pct:>6.2f}% {enrichment:>10.2f}×")

    # qo words by section
    print(f"\n--- qo RATE BY SECTION (Currier B) ---")
    section_data = defaultdict(lambda: {'total': 0, 'qo': 0})
    for r in b_records:
        sec = r['section'] or '?'
        for w in r['words']:
            section_data[sec]['total'] += 1
            if w.startswith('qo') and len(w) > 2:
                section_data[sec]['qo'] += 1

    print(f"{'Section':>10} {'Total':>7} {'qo':>5} {'qo%':>7}")
    for sec in sorted(section_data.keys()):
        d = section_data[sec]
        n = d['total']
        q = d['qo']
        print(f"{sec:>10} {n:>7} {q:>5} {100*q/max(n,1):>6.2f}%")

if __name__ == '__main__':
    main()
