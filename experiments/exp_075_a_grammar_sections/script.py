"""
exp_075: Currier A Grammar — Section-Sensitive Complementarity (H100), Trigram Structure (H102),
         Register-Sensitive Sequential Grammar (H103), Line-Final by Section (H104)

H100: Does A's {sh vs s} complementarity vary by section (Herbal A vs Pharma A)?
H102: Does A have a dominant onset-class trigram structure analogous to B's qo→ch→qo?
H103: Does the sequential grammar differ between A's y-dominant and aiin-dominant registers?
H104: Does B's line-final onset distribution differ by section?
"""
from pathlib import Path as _RepositoryPath

import re
import math
from collections import Counter, defaultdict

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

# Aiin-dominant Herbal A folios (from exp_059/exp_062)
AIIN_DOM_FOLIOS = {'f6r', 'f6v', 'f7r', 'f7v', 'f8r', 'f8v', 'f9r', 'f9v',
                   'f10r', 'f10v', 'f11r', 'f11v', 'f13r', 'f13v', 'f14r', 'f14v',
                   'f15r', 'f15v', 'f16r', 'f16v', 'f17r', 'f17v', 'f96r', 'f96v'}

def clean_text(text):
    return re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)

def is_body_locus(locus_code):
    base = locus_code.lstrip('+*@=/~&')
    return base.startswith('P')

def onset_class(word):
    if word.startswith('qo') and len(word) > 2:
        return 'qo'
    if word.startswith('ch') and len(word) > 2:
        return 'ch'
    if word.startswith('sh') and len(word) > 2:
        return 'sh'
    if word.startswith('p') and len(word) > 1:
        return 'p'
    if word.startswith('t') and len(word) > 1:
        return 't'
    if word.startswith('k') and len(word) > 1:
        return 'k'
    if word.startswith('d') and len(word) > 1:
        return 'd'
    if word.startswith('s') and not word.startswith('sh') and len(word) > 1:
        return 's'
    if word.startswith('y') and len(word) > 1:
        return 'y'
    if word.startswith('o') and len(word) > 1:
        return 'o'
    return 'other'

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
            base_locus = locus_code.lstrip('+*=/~&')
            is_para_start = base_locus.startswith('@')
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
                'is_para_start': is_para_start,
                'words': tokens
            })
    return records

def complementarity_stats(recs, label=""):
    """Compute P(ch|X) and P(qo|X) for key onset classes."""
    d_words = [w for r in recs for w in r['words']]
    if not d_words:
        return
    base_ch = sum(1 for w in d_words if onset_class(w) == 'ch') / len(d_words)
    base_qo = sum(1 for w in d_words if onset_class(w) == 'qo') / len(d_words)

    transitions = defaultdict(Counter)
    totals = Counter()
    for r in recs:
        ws = r['words']
        for i in range(len(ws) - 1):
            oc1 = onset_class(ws[i])
            oc2 = onset_class(ws[i+1])
            transitions[oc1][oc2] += 1
            totals[oc1] += 1

    print(f"\n{label}: baseline ch={100*base_ch:.1f}%, qo={100*base_qo:.1f}%")
    print(f"  {'Onset':<8} {'n':>6} {'→ch':>8} {'enr_ch':>8} {'→qo':>8} {'enr_qo':>8}")
    for oc in ['sh', 's', 'd', 'ch', 'y', 'o', 'qo', 'k']:
        n = totals[oc]
        if n < 20:
            continue
        p_ch = transitions[oc].get('ch', 0) / max(n, 1)
        p_qo = transitions[oc].get('qo', 0) / max(n, 1)
        print(f"  {oc+'→':<8} {n:>6} {100*p_ch:>7.1f}% {p_ch/max(base_ch,1e-10):>7.2f}× {100*p_qo:>7.1f}% {p_qo/max(base_qo,1e-10):>7.2f}×")

    return transitions, totals, base_ch, base_qo

def bigram_ppl_reduction(recs, alpha=0.1):
    """Return bigram PPL reduction vs unigram for the given records."""
    unigram = Counter()
    bigram = defaultdict(Counter)
    for r in recs:
        ws = r['words']
        for w in ws:
            unigram[onset_class(w)] += 1
        for i in range(len(ws) - 1):
            bigram[onset_class(ws[i])][onset_class(ws[i+1])] += 1

    total = sum(unigram.values())
    n_types = len(unigram)

    log_uni = 0.0
    log_bi = 0.0
    n_tok = 0
    n_big = 0

    for r in recs:
        ws = r['words']
        ocs = [onset_class(w) for w in ws]
        for oc in ocs:
            p = (unigram[oc] + alpha) / (total + alpha * n_types)
            log_uni += math.log2(p)
            n_tok += 1
        for i in range(len(ocs) - 1):
            oc1, oc2 = ocs[i], ocs[i+1]
            n1 = sum(bigram[oc1].values())
            p_bi = (bigram[oc1][oc2] + alpha) / (n1 + alpha * n_types)
            log_bi += math.log2(p_bi)
            n_big += 1

    ppl_uni = 2 ** (-log_uni / max(n_tok, 1))
    ppl_bi = 2 ** (-log_bi / max(n_big, 1))
    reduction_pct = 100 * (ppl_uni - ppl_bi) / max(ppl_uni, 1)
    return ppl_uni, ppl_bi, reduction_pct, n_tok

def trigram_analysis(recs, label="", top_n=20):
    """Compute onset-class trigrams and compare to unigram baseline."""
    d_words = [w for r in recs for w in r['words']]
    if not d_words:
        return
    unigram = Counter(onset_class(w) for w in d_words)
    total = len(d_words)

    trigrams = Counter()
    for r in recs:
        ws = r['words']
        for i in range(len(ws) - 2):
            t = (onset_class(ws[i]), onset_class(ws[i+1]), onset_class(ws[i+2]))
            trigrams[t] += 1

    total_tri = sum(trigrams.values())
    print(f"\n{label}: {total_tri} trigrams total")
    print(f"  {'Trigram':<25} {'Count':>6} {'Expected':>9} {'Enrichment':>11}")

    for tri, cnt in trigrams.most_common(top_n):
        oc1, oc2, oc3 = tri
        p1 = unigram.get(oc1, 0) / total
        p2 = unigram.get(oc2, 0) / total
        p3 = unigram.get(oc3, 0) / total
        expected = p1 * p2 * p3 * total_tri
        enrichment = cnt / max(expected, 0.001)
        label_str = f"{oc1}→{oc2}→{oc3}"
        print(f"  {label_str:<25} {cnt:>6} {expected:>9.1f} {enrichment:>10.2f}×")

    # Also show top enriched trigrams with count >= 20
    print(f"\n  Top enriched trigrams (count ≥ 20):")
    enriched = []
    for tri, cnt in trigrams.items():
        if cnt < 20:
            continue
        oc1, oc2, oc3 = tri
        p1 = unigram.get(oc1, 0) / total
        p2 = unigram.get(oc2, 0) / total
        p3 = unigram.get(oc3, 0) / total
        expected = p1 * p2 * p3 * total_tri
        enrichment = cnt / max(expected, 0.001)
        enriched.append((enrichment, cnt, f"{oc1}→{oc2}→{oc3}"))
    enriched.sort(reverse=True)
    print(f"  {'Trigram':<25} {'Count':>6} {'Enrichment':>11}")
    for enr, cnt, label_str in enriched[:15]:
        print(f"  {label_str:<25} {cnt:>6} {enr:>10.2f}×")

def line_final_by_section(recs, label=""):
    """Compute last-word onset distribution by section."""
    all_words = [w for r in recs for w in r['words']]
    base_onset = Counter(onset_class(w) for w in all_words)
    n_total = len(all_words)

    # Group by section
    section_last = defaultdict(Counter)
    section_total = Counter()
    for r in recs:
        ws = r['words']
        if not ws:
            continue
        last_oc = onset_class(ws[-1])
        sec = r['section'] or 'UNK'
        section_last[sec][last_oc] += 1
        section_total[sec] += 1

    print(f"\n{label}: last-word onset by section")
    print(f"  {'Section':<10} {'n':>5} {'qo':>8} {'sh':>8} {'o':>8} {'d':>8} {'ch':>8} {'other':>8}")
    for sec in sorted(section_total, key=lambda s: -section_total[s]):
        n = section_total[sec]
        if n < 30:
            continue
        row = f"  {sec:<10} {n:>5}"
        for oc in ['qo', 'sh', 'o', 'd', 'ch', 'other']:
            cnt = section_last[sec].get(oc, 0)
            base_p = base_onset.get(oc, 0) / max(n_total, 1)
            p = cnt / max(n, 1)
            enr = p / max(base_p, 1e-10)
            row += f" {enr:>6.2f}×"
        print(row)

def main():
    records = parse_corpus(DATA_PATH)
    a_records = [r for r in records if r['currier'] == 'A']
    b_records = [r for r in records if r['currier'] == 'B']

    # Split A by section
    herbal_a = [r for r in a_records if r['section'] in ('H', 'HER')]
    pharma_a = [r for r in a_records if r['section'] in ('P', 'PHA')]

    # Split Herbal A by register (aiin-dom vs y-dom)
    aiin_dom_a = [r for r in a_records if r['folio'] in AIIN_DOM_FOLIOS]
    y_dom_a = [r for r in a_records
               if r['folio'] not in AIIN_DOM_FOLIOS
               and r['section'] in ('H', 'HER')]

    # ================================================================
    print("="*70)
    print("H100: A {sh vs s} COMPLEMENTARITY BY SECTION")
    print("="*70)

    # First show global A for reference
    complementarity_stats(a_records, "A GLOBAL")

    # Check section names
    section_counts = Counter(r['section'] for r in a_records)
    print(f"\nA section distribution: {dict(section_counts.most_common(10))}")

    for label, recs in [('Herbal A', herbal_a), ('Pharma A', pharma_a)]:
        if len(recs) > 50:
            complementarity_stats(recs, label)

    # ================================================================
    print(f"\n{'='*70}")
    print("H103: REGISTER-SENSITIVE SEQUENTIAL GRAMMAR (aiin-dom vs y-dom Herbal A)")
    print(f"{'='*70}")

    print(f"\naiin-dom folios: {len(aiin_dom_a)} records; y-dom folios: {len(y_dom_a)} records")
    for label, recs in [('Aiin-dominant Herbal A', aiin_dom_a), ('Y-dominant Herbal A', y_dom_a)]:
        if len(recs) > 50:
            complementarity_stats(recs, label)

    # Bigram PPL by register
    print(f"\nBigram PPL reduction by A register:")
    for label, recs in [('A global', a_records), ('Aiin-dom A', aiin_dom_a), ('Y-dom A', y_dom_a)]:
        if len(recs) > 50:
            ppl_uni, ppl_bi, pct, n_tok = bigram_ppl_reduction(recs)
            print(f"  {label:<22}: {n_tok} tokens | unigram PPL={ppl_uni:.3f} | bigram PPL={ppl_bi:.3f} | reduction={pct:.1f}%")

    # ================================================================
    print(f"\n{'='*70}")
    print("H102: A ONSET-CLASS TRIGRAM STRUCTURE")
    print(f"{'='*70}")

    trigram_analysis(a_records, "Currier A", top_n=20)
    trigram_analysis(b_records, "Currier B (for comparison)", top_n=15)

    # ================================================================
    print(f"\n{'='*70}")
    print("H104: B LINE-FINAL ONSET DISTRIBUTION BY SECTION")
    print(f"{'='*70}")

    line_final_by_section(b_records, "Currier B")

    # Also check A by section for completeness
    line_final_by_section(a_records, "Currier A")

    # ================================================================
    # Additional: Cross-check sh→qo by A section
    print(f"\n{'='*70}")
    print("CROSS-CHECK: sh→qo and s→ch enrichment by A section")
    print(f"{'='*70}")

    a_sections_map = defaultdict(list)
    for r in a_records:
        a_sections_map[r['section'] or 'UNK'].append(r)

    for sec, recs in sorted(a_sections_map.items(), key=lambda x: -len(x[1])):
        if len(recs) < 50:
            continue
        d_words = [w for r in recs for w in r['words']]
        base_ch = sum(1 for w in d_words if onset_class(w) == 'ch') / max(len(d_words), 1)
        base_qo = sum(1 for w in d_words if onset_class(w) == 'qo') / max(len(d_words), 1)
        transitions = defaultdict(Counter)
        totals = Counter()
        for r in recs:
            ws = r['words']
            for i in range(len(ws) - 1):
                oc1, oc2 = onset_class(ws[i]), onset_class(ws[i+1])
                transitions[oc1][oc2] += 1
                totals[oc1] += 1

        sh_ch = transitions['sh'].get('ch', 0) / max(totals['sh'], 1) if totals['sh'] > 10 else float('nan')
        sh_qo = transitions['sh'].get('qo', 0) / max(totals['sh'], 1) if totals['sh'] > 10 else float('nan')
        s_ch = transitions['s'].get('ch', 0) / max(totals['s'], 1) if totals['s'] > 10 else float('nan')
        s_qo = transitions['s'].get('qo', 0) / max(totals['s'], 1) if totals['s'] > 10 else float('nan')

        n_words = len(d_words)
        print(f"\nA {sec} ({n_words} words, base ch={100*base_ch:.1f}%, qo={100*base_qo:.1f}%):")
        print(f"  sh→ch={100*sh_ch:.1f}% ({sh_ch/max(base_ch,1e-10):.2f}×)  sh→qo={100*sh_qo:.1f}% ({sh_qo/max(base_qo,1e-10):.2f}×)  n(sh)={totals['sh']}")
        print(f"  s→ch={100*s_ch:.1f}% ({s_ch/max(base_ch,1e-10):.2f}×)   s→qo={100*s_qo:.1f}% ({s_qo/max(base_qo,1e-10):.2f}×)   n(s)={totals['s']}")

if __name__ == '__main__':
    main()
