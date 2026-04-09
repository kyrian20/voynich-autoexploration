"""
exp_074: Grammar Model (H097, H098, H099)
H097: Does Currier A also have d/sh complementarity?
H098: Does a bigram onset model outperform unigram? Is B's grammar stronger than A's?
H099: Are line-final words determined by the preceding onset class?
"""

import re
import math
from collections import Counter, defaultdict

DATA_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"

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

def build_transition_model(recs):
    """Build unigram and bigram onset-class models."""
    unigram = Counter()
    bigram = defaultdict(Counter)
    for r in recs:
        ws = r['words']
        for w in ws:
            unigram[onset_class(w)] += 1
        for i in range(len(ws) - 1):
            oc1 = onset_class(ws[i])
            oc2 = onset_class(ws[i+1])
            bigram[oc1][oc2] += 1
    return unigram, bigram

def compute_perplexity(recs, unigram, bigram, alpha=0.1):
    """Compute perplexity of unigram and bigram models over onset sequences."""
    total = sum(unigram.values())
    n_types = len(unigram)

    # Unigram model: smoothed
    log_prob_unigram = 0.0
    log_prob_bigram = 0.0
    n_tokens = 0
    n_bigrams = 0

    for r in recs:
        ws = r['words']
        ocs = [onset_class(w) for w in ws]
        n = len(ocs)
        for i, oc in enumerate(ocs):
            # Laplace-smoothed unigram
            p = (unigram[oc] + alpha) / (total + alpha * n_types)
            log_prob_unigram += math.log2(p)
            n_tokens += 1
        # Bigram
        for i in range(n - 1):
            oc1, oc2 = ocs[i], ocs[i+1]
            n1 = sum(bigram[oc1].values())
            p_bi = (bigram[oc1][oc2] + alpha) / (n1 + alpha * n_types)
            log_prob_bigram += math.log2(p_bi)
            n_bigrams += 1

    ppl_uni = 2 ** (-log_prob_unigram / max(n_tokens, 1))
    ppl_bi = 2 ** (-log_prob_bigram / max(n_bigrams, 1))
    bits_uni = -log_prob_unigram / max(n_tokens, 1)
    bits_bi = -log_prob_bigram / max(n_bigrams, 1)
    return ppl_uni, ppl_bi, bits_uni, bits_bi, n_tokens, n_bigrams

def main():
    records = parse_corpus(DATA_PATH)
    b_records = [r for r in records if r['currier'] == 'B']
    a_records = [r for r in records if r['currier'] == 'A']

    # H097: d/sh complementarity in A
    print("="*70)
    print("H097: d/sh COMPLEMENTARITY IN CURRIER A vs B")
    print("="*70)

    for dialect, d_recs in [('A', a_records), ('B', b_records)]:
        d_words = [w for r in d_recs for w in r['words']]
        base_ch = sum(1 for w in d_words if onset_class(w) == 'ch') / max(len(d_words), 1)
        base_qo = sum(1 for w in d_words if onset_class(w) == 'qo') / max(len(d_words), 1)

        transitions = defaultdict(Counter)
        totals = Counter()
        for r in d_recs:
            ws = r['words']
            for i in range(len(ws) - 1):
                oc1 = onset_class(ws[i])
                oc2 = onset_class(ws[i+1])
                transitions[oc1][oc2] += 1
                totals[oc1] += 1

        print(f"\nCurrier {dialect}: baseline ch={100*base_ch:.1f}%, qo={100*base_qo:.1f}%")
        print(f"  {'Onset':<8} {'→ch':>8} {'enr_ch':>8} {'→qo':>8} {'enr_qo':>8}")
        for oc in ['d', 'sh', 's', 'ch', 'y', 'o', 'qo']:
            n = totals[oc]
            if n < 30:
                continue
            p_ch = transitions[oc].get('ch', 0) / max(n, 1)
            p_qo = transitions[oc].get('qo', 0) / max(n, 1)
            print(f"  {oc+'→':<8} {100*p_ch:>7.1f}% {p_ch/max(base_ch,1e-10):>7.2f}× {100*p_qo:>7.1f}% {p_qo/max(base_qo,1e-10):>7.2f}×")

    # H098: Bigram vs unigram perplexity
    print(f"\n{'='*70}")
    print("H098: BIGRAM vs UNIGRAM ONSET-CLASS PERPLEXITY")
    print(f"{'='*70}")

    for dialect, d_recs in [('A', a_records), ('B', b_records)]:
        unigram, bigram = build_transition_model(d_recs)
        ppl_uni, ppl_bi, bits_uni, bits_bi, n_tok, n_big = compute_perplexity(d_recs, unigram, bigram)
        print(f"\nCurrier {dialect}: {n_tok} tokens, {n_big} bigrams")
        print(f"  Unigram perplexity: {ppl_uni:.3f} ({bits_uni:.3f} bits/token)")
        print(f"  Bigram perplexity:  {ppl_bi:.3f} ({bits_bi:.3f} bits/bigram)")
        print(f"  Improvement: {ppl_uni - ppl_bi:.3f} PPL reduction ({bits_uni - bits_bi:.3f} bits reduction)")
        print(f"  Relative reduction: {100*(ppl_uni-ppl_bi)/max(ppl_uni,1):.1f}%")

    # H099: Line-final word onset class determined by second-to-last onset class
    print(f"\n{'='*70}")
    print("H099: LINE-FINAL ONSET CLASS DETERMINED BY PRECEDING ONSET CLASS")
    print(f"{'='*70}")

    for dialect, d_recs in [('A', a_records), ('B', b_records)]:
        d_words = [w for r in d_recs for w in r['words']]
        base_onset = Counter(onset_class(w) for w in d_words)
        n_total = len(d_words)

        # Collect (second-to-last onset, last onset) pairs
        penultimate_to_last = defaultdict(Counter)  # onset class of second-to-last → onset class of last
        penultimate_total = Counter()
        last_onset_overall = Counter()

        for r in d_recs:
            ws = r['words']
            n = len(ws)
            if n < 2:
                continue
            last_oc = onset_class(ws[-1])
            penult_oc = onset_class(ws[-2])
            penultimate_to_last[penult_oc][last_oc] += 1
            penultimate_total[penult_oc] += 1
            last_onset_overall[last_oc] += 1

        # Overall distribution of last-word onsets
        n_last = sum(last_onset_overall.values())
        print(f"\nCurrier {dialect}: last-word onset distribution:")
        for oc, c in last_onset_overall.most_common(8):
            print(f"  {oc}: {c} ({100*c/max(n_last,1):.1f}%)")

        # For each penultimate onset, what is the last-word onset?
        print(f"\n  Conditional: P(last onset | penultimate onset)")
        print(f"  {'Penult→':<10} {'n':>5} {'→ch':>7} {'→sh':>7} {'→qo':>7} {'→o':>7} {'→d':>7} {'→other':>8}")
        for pen_oc in ['qo', 'ch', 'sh', 'd', 'o', 'y', 'k', 'other']:
            n = penultimate_total.get(pen_oc, 0)
            if n < 10:
                continue
            row = f"  {pen_oc+'→':<10} {n:>5}"
            for last_oc in ['ch', 'sh', 'qo', 'o', 'd', 'other']:
                count = penultimate_to_last[pen_oc].get(last_oc, 0)
                pct = 100 * count / max(n, 1)
                row += f" {pct:>6.1f}%"
            print(row)

        # What onset class appears most commonly as second-to-last word?
        print(f"\n  Second-to-last word onset distribution:")
        for oc, c in penultimate_total.most_common(8):
            print(f"  {oc}: {c} ({100*c/max(n_last,1):.1f}%)")

        # Compare: is the second-to-last word onset different from random?
        print(f"\n  Enrichment of second-to-last onset vs baseline:")
        for oc in ['qo', 'ch', 'sh', 'd', 'o', 'y']:
            pen_p = penultimate_total.get(oc, 0) / max(n_last, 1)
            base_p = base_onset.get(oc, 0) / max(n_total, 1)
            print(f"  {oc}: {100*pen_p:.1f}% vs baseline {100*base_p:.1f}% = {pen_p/max(base_p,1e-10):.2f}×")

if __name__ == '__main__':
    main()
