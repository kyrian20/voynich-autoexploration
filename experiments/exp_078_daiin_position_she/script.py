"""
exp_078: daiin Paragraph Position (H113), she-/sh- Morphological Distinction (H114),
         oly/otam/okam Structural Analysis (H115), Register sh-Vocabulary (H116)

H113: Does daiin rate increase toward the end of multi-line paragraphs in Currier A?
H114: Does she- prefix predict qo-following rate across all A sections?
H115: Are oly/otam/okam morphologically distinct B within-para line-final words?
H116: Do A registers differ in she-/sh- usage patterns?
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

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

def group_into_paragraphs(recs):
    """Group records into paragraphs by is_para_start markers."""
    paragraphs = []
    current_para = []
    for r in recs:
        if r['is_para_start'] and current_para:
            paragraphs.append(current_para)
            current_para = [r]
        elif r['is_para_start']:
            current_para = [r]
        else:
            current_para.append(r)
    if current_para:
        paragraphs.append(current_para)
    return paragraphs

def main():
    records = parse_corpus(DATA_PATH)
    a_records = [r for r in records if r['currier'] == 'A']
    b_records = [r for r in records if r['currier'] == 'B']
    herbal_a = [r for r in a_records if r['section'] == 'H']
    pharma_a = [r for r in a_records if r['section'] == 'P']
    aiin_dom = [r for r in a_records if r['folio'] in AIIN_DOM_FOLIOS]
    y_dom = [r for r in a_records if r['folio'] not in AIIN_DOM_FOLIOS and r['section'] == 'H']

    # ================================================================
    print("="*70)
    print("H113: daiin PARAGRAPH POSITION IN CURRIER A")
    print("="*70)

    # Group A records into paragraphs
    a_paras = group_into_paragraphs(a_records)
    multi_line_paras = [p for p in a_paras if len(p) >= 3]
    print(f"\nTotal A paragraphs: {len(a_paras)}; multi-line (≥3): {len(multi_line_paras)}")

    # Compute daiin rate by relative line position (bucket into: line 1, line 2, ..., last, 2nd-to-last)
    # Use absolute position: 0, 1, 2, ... and also relative from end: -1, -2, -3 ...
    # For multi-line paragraphs, bin by: first, middle, last
    daiin_by_pos = {'first': Counter(), 'middle': Counter(), 'last': Counter()}  # word counts

    for para in multi_line_paras:
        n_lines = len(para)
        for line_idx, rec in enumerate(para):
            if line_idx == 0:
                pos = 'first'
            elif line_idx == n_lines - 1:
                pos = 'last'
            else:
                pos = 'middle'

            for word in rec['words']:
                daiin_by_pos[pos][word] += 1

    for pos in ['first', 'middle', 'last']:
        total = sum(daiin_by_pos[pos].values())
        daiin_cnt = daiin_by_pos[pos].get('daiin', 0)
        rate = 100 * daiin_cnt / max(total, 1)
        print(f"  {pos}: {daiin_cnt}/{total} daiin = {rate:.2f}%")

    # Also for paragraphs with 5+ lines, compute by position 0, 1, 2, ..., -2, -1
    long_paras = [p for p in a_paras if len(p) >= 5]
    print(f"\nFor long paragraphs (≥5 lines, n={len(long_paras)}): daiin rate by line position from start:")
    pos_daiin = defaultdict(lambda: Counter())
    for para in long_paras:
        n = len(para)
        for idx, rec in enumerate(para):
            for word in rec['words']:
                pos_daiin[idx][word] += 1
    # Show first 6 positions and last 3
    for idx in range(min(6, max(pos_daiin.keys()) + 1)):
        if idx not in pos_daiin:
            continue
        total = sum(pos_daiin[idx].values())
        dc = pos_daiin[idx].get('daiin', 0)
        print(f"  line {idx}: {dc}/{total} = {100*dc/max(total,1):.1f}%")

    print(f"  [...]")
    max_idx = max(pos_daiin.keys())
    for idx in range(max(0, max_idx - 2), max_idx + 1):
        if idx not in pos_daiin:
            continue
        total = sum(pos_daiin[idx].values())
        dc = pos_daiin[idx].get('daiin', 0)
        print(f"  line {idx} (from-end={max_idx - idx}): {dc}/{total} = {100*dc/max(total,1):.1f}%")

    # Also: daiin rate by token position within line (first, mid, last) across all A
    daiin_by_token_pos = {'first': Counter(), 'middle': Counter(), 'last': Counter()}
    for r in a_records:
        ws = r['words']
        n = len(ws)
        for i, w in enumerate(ws):
            if i == 0:
                tpos = 'first'
            elif i == n - 1:
                tpos = 'last'
            else:
                tpos = 'middle'
            daiin_by_token_pos[tpos][w] += 1

    print(f"\ndaiin rate by token position within line (all A):")
    for tpos in ['first', 'middle', 'last']:
        total = sum(daiin_by_token_pos[tpos].values())
        dc = daiin_by_token_pos[tpos].get('daiin', 0)
        rate = 100 * dc / max(total, 1)
        print(f"  {tpos}: {dc}/{total} = {rate:.2f}% (enrichment vs corpus: {rate/max(100*423/max(sum(sum(c.values()) for c in daiin_by_token_pos.values()),1),1e-10):.2f}×)")

    # ================================================================
    print(f"\n{'='*70}")
    print("H114: she- vs sh- MORPHOLOGICAL DISTINCTION PREDICTS qo-FOLLOWING")
    print(f"{'='*70}")

    def she_or_sh(word):
        """Classify sh-words: 'she-' if starts 'she', else 'sh-other'."""
        if word.startswith('she') and len(word) > 3:
            return 'she-'
        elif onset_class(word) == 'sh':
            return 'sh-other'
        return None

    # Global Currier A: she- vs sh-other → qo following
    print(f"\nAll Currier A: she- vs sh-other onset classes → qo following")
    for label, recs in [('All A', a_records), ('Herbal A', herbal_a), ('Pharma A', pharma_a)]:
        she_qo = 0
        she_n = 0
        sho_qo = 0
        sho_n = 0
        she_ch = 0
        sho_ch = 0
        all_words = [w for r in recs for w in r['words']]
        n_total = len(all_words)
        base_qo = sum(1 for w in all_words if onset_class(w) == 'qo') / max(n_total, 1)

        for r in recs:
            ws = r['words']
            for i in range(len(ws) - 1):
                sc = she_or_sh(ws[i])
                next_oc = onset_class(ws[i+1])
                if sc == 'she-':
                    she_n += 1
                    if next_oc == 'qo':
                        she_qo += 1
                    if next_oc == 'ch':
                        she_ch += 1
                elif sc == 'sh-other':
                    sho_n += 1
                    if next_oc == 'qo':
                        sho_qo += 1
                    if next_oc == 'ch':
                        sho_ch += 1

        she_words = Counter(w for r in recs for w in r['words'] if she_or_sh(w) == 'she-')
        sho_words = Counter(w for r in recs for w in r['words'] if she_or_sh(w) == 'sh-other')

        print(f"\n  {label} (baseline qo={100*base_qo:.1f}%):")
        print(f"    she- forms: n(transitions)={she_n}, top words: {list(she_words.most_common(5))}")
        print(f"    she-→qo: {100*she_qo/max(she_n,1):.1f}% ({(she_qo/max(she_n,1))/max(base_qo,1e-10):.2f}×), she-→ch: {100*she_ch/max(she_n,1):.1f}%")
        print(f"    sh-other forms: n={sho_n}, top words: {list(sho_words.most_common(5))}")
        print(f"    sh-other→qo: {100*sho_qo/max(sho_n,1):.1f}% ({(sho_qo/max(sho_n,1))/max(base_qo,1e-10):.2f}×), sh-other→ch: {100*sho_ch/max(sho_n,1):.1f}%")

    # Also test in Currier B
    b_all_words = [w for r in b_records for w in r['words']]
    b_base_qo = sum(1 for w in b_all_words if onset_class(w) == 'qo') / max(len(b_all_words), 1)
    she_qo_b = she_n_b = sho_qo_b = sho_n_b = 0
    for r in b_records:
        ws = r['words']
        for i in range(len(ws) - 1):
            sc = she_or_sh(ws[i])
            next_oc = onset_class(ws[i+1])
            if sc == 'she-':
                she_n_b += 1
                if next_oc == 'qo':
                    she_qo_b += 1
            elif sc == 'sh-other':
                sho_n_b += 1
                if next_oc == 'qo':
                    sho_qo_b += 1
    print(f"\n  Currier B (baseline qo={100*b_base_qo:.1f}%):")
    print(f"    she-→qo: {100*she_qo_b/max(she_n_b,1):.1f}% ({(she_qo_b/max(she_n_b,1))/max(b_base_qo,1e-10):.2f}×, n={she_n_b})")
    print(f"    sh-other→qo: {100*sho_qo_b/max(sho_n_b,1):.1f}% ({(sho_qo_b/max(sho_n_b,1))/max(b_base_qo,1e-10):.2f}×, n={sho_n_b})")

    # ================================================================
    print(f"\n{'='*70}")
    print("H115: oly/otam/okam POSITIONAL PROFILE AND PRECEDING CONTEXT IN B")
    print(f"{'='*70}")

    target_words = {'oly', 'otam', 'okam', 'oldy', 'olkam'}
    all_b_words_list = [w for r in b_records for w in r['words']]
    n_b = len(all_b_words_list)
    b_word_freq = Counter(all_b_words_list)

    for target in sorted(target_words):
        if b_word_freq.get(target, 0) < 5:
            continue
        # Positional stats
        first_cnt = mid_cnt = last_cnt = 0
        total_cnt = 0
        preceding_oc = Counter()
        following_oc = Counter()
        for r in b_records:
            ws = r['words']
            n = len(ws)
            for i, w in enumerate(ws):
                if w == target:
                    total_cnt += 1
                    if i == 0:
                        first_cnt += 1
                    elif i == n - 1:
                        last_cnt += 1
                    else:
                        mid_cnt += 1
                    if i > 0:
                        preceding_oc[onset_class(ws[i-1])] += 1
                    if i < n - 1:
                        following_oc[onset_class(ws[i+1])] += 1
        corpus_rate = b_word_freq.get(target, 0) / max(n_b, 1)
        last_rate = last_cnt / max(total_cnt, 1)
        print(f"\n  '{target}' (n={total_cnt}, corpus={100*corpus_rate:.2f}%):")
        print(f"    first={first_cnt}, middle={mid_cnt}, last={last_cnt}")
        print(f"    last rate: {100*last_rate:.1f}% (vs corpus: {100*last_cnt/max(n_b,1):.2f}%)")
        print(f"    preceding onset: {dict(preceding_oc.most_common(5))}")
        print(f"    following onset: {dict(following_oc.most_common(5))}")

    # ================================================================
    print(f"\n{'='*70}")
    print("H116: REGISTER sh-VOCABULARY — she-/sh- SPLIT IN AIIN-DOM vs Y-DOM HERBAL A")
    print(f"{'='*70}")

    for label, recs in [('Aiin-dominant', aiin_dom), ('Y-dominant', y_dom)]:
        sh_words = [w for r in recs for w in r['words'] if onset_class(w) == 'sh']
        she_words = [w for w in sh_words if w.startswith('she') and len(w) > 3]
        n_sh = len(sh_words)
        n_she = len(she_words)

        # qo following for she- vs sh-other
        she_qo_n = she_qo_cnt = sho_qo_n = sho_qo_cnt = 0
        all_words = [w for r in recs for w in r['words']]
        n_total = len(all_words)
        base_qo = sum(1 for w in all_words if onset_class(w) == 'qo') / max(n_total, 1)
        for r in recs:
            ws = r['words']
            for i in range(len(ws) - 1):
                sc = she_or_sh(ws[i])
                next_oc = onset_class(ws[i+1])
                if sc == 'she-':
                    she_qo_n += 1
                    if next_oc == 'qo':
                        she_qo_cnt += 1
                elif sc == 'sh-other':
                    sho_qo_n += 1
                    if next_oc == 'qo':
                        sho_qo_cnt += 1

        she_top = Counter(she_words).most_common(5)
        sho_top = Counter(w for w in sh_words if not (w.startswith('she') and len(w) > 3)).most_common(5)

        print(f"\n{label} Herbal A (baseline qo={100*base_qo:.1f}%):")
        print(f"  Total sh-words: {n_sh}; she- forms: {n_she} ({100*n_she/max(n_sh,1):.1f}%)")
        print(f"  Top she- words: {she_top}")
        print(f"  Top sh-other words: {sho_top}")
        print(f"  she-→qo: {100*she_qo_cnt/max(she_qo_n,1):.1f}% ({(she_qo_cnt/max(she_qo_n,1))/max(base_qo,1e-10):.2f}×, n={she_qo_n})")
        print(f"  sh-other→qo: {100*sho_qo_cnt/max(sho_qo_n,1):.1f}% ({(sho_qo_cnt/max(sho_qo_n,1))/max(base_qo,1e-10):.2f}×, n={sho_qo_n})")

if __name__ == '__main__':
    main()
