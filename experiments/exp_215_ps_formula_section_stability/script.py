"""
exp_215: H400 — Shared PS Formula Stability Across Sections

Motivation:
  F198/F208: A and B share the same PS onset class (p/t/k/f enriched; y/d excluded).
  F214: A and B share [PS=gallows → pos=1=anti-gallows] skeleton.

  H400: Is the PS formula stable across sections within each dialect?
  If stable → grammar rule / shared syntactic template
  If varies strongly by section → scribal convention

Test:
  For each dialect × section combination with sufficient n (n≥5 paragraphs):
  (1) p-onset enrichment at PS (p_PS / p_base)
  (2) t-onset enrichment at PS
  (3) k-onset enrichment at PS
  (4) f-onset enrichment at PS
  (5) Combined gallows enrichment at PS
  (6) y-onset enrichment at PS (should be low)
  (7) d-onset enrichment at PS (should be low)

  Compare across sections within each dialect.
"""
import re
from collections import defaultdict, Counter

DATA_PATH = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

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
    folio_section = {}
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
            folio_section[fb] = classify_section(fb)
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


paragraphs, folio_dialect = parse_corpus()

print("=== PS Formula Stability by Section × Dialect ===")
print("  [H400: Is the shared A/B PS formula (p/t/k/f enriched; y/d depleted) stable across sections?]")
print()

for dialect_label in ['A', 'B']:
    paras = [p for p in paragraphs if p['dialect'] == dialect_label and len(p['lines']) >= 1]
    print(f"\n--- {dialect_label}-DIALECT ({len(paras)} total paragraphs) ---")

    # Overall base rates (across all positions in all first lines)
    all_onsets = Counter()
    all_n = 0
    for para in paras:
        for line in para['lines']:
            for word in line:
                all_onsets[get_onset(word)] += 1
                all_n += 1

    # Section breakdown
    section_ps = defaultdict(Counter)
    section_ps_n = defaultdict(int)
    section_para_n = defaultdict(int)

    for para in paras:
        sec = para['section']
        section_para_n[sec] += 1
        fl = para['lines'][0]
        if fl:
            ps_word = fl[0]
            ps_onset = get_onset(ps_word)
            section_ps[sec][ps_onset] += 1
            section_ps_n[sec] += 1

    # Report for each section with sufficient n
    key_onsets = ['p', 't', 'k', 'f', 'y', 'd', 'ch', 'sh']
    print(f"  {'Section':<10} {'n_para':<8} {'p_enr':<8} {'t_enr':<8} {'k_enr':<8} {'f_enr':<8} {'gal%':<8} {'y_enr':<8} {'d_enr':<8}")

    for sec in sorted(section_para_n.keys()):
        n_ps = section_ps_n[sec]
        n_para = section_para_n[sec]
        if n_ps < 5:
            print(f"  {sec:<10} {n_para:<8} (n<5 — skipped)")
            continue

        # Base rates vs section PS rates
        enr = {}
        for onset in key_onsets:
            b_r = all_onsets.get(onset, 0) / all_n if all_n > 0 else 0
            ps_r = section_ps[sec].get(onset, 0) / n_ps
            enr[onset] = ps_r / b_r if b_r > 0 else 0

        gal_pct = (section_ps[sec].get('p',0) + section_ps[sec].get('t',0) +
                   section_ps[sec].get('k',0) + section_ps[sec].get('f',0)) / n_ps * 100

        print(f"  {sec:<10} {n_para:<8} {enr['p']:.2f}×  {enr['t']:.2f}×  {enr['k']:.2f}×  {enr['f']:.2f}×  "
              f"{gal_pct:.0f}%    {enr['y']:.2f}×  {enr['d']:.2f}×")

    # Overall
    total_ps = Counter()
    total_n = 0
    for para in paras:
        fl = para['lines'][0]
        if fl:
            total_ps[get_onset(fl[0])] += 1
            total_n += 1

    gal_pct_total = (total_ps.get('p',0)+total_ps.get('t',0)+total_ps.get('k',0)+total_ps.get('f',0)) / total_n * 100
    enr = {}
    for onset in key_onsets:
        b_r = all_onsets.get(onset, 0) / all_n if all_n > 0 else 0
        ps_r = total_ps.get(onset, 0) / total_n
        enr[onset] = ps_r / b_r if b_r > 0 else 0

    print(f"  {'TOTAL':<10} {len(paras):<8} {enr['p']:.2f}×  {enr['t']:.2f}×  {enr['k']:.2f}×  {enr['f']:.2f}×  "
          f"{gal_pct_total:.0f}%    {enr['y']:.2f}×  {enr['d']:.2f}×")

    print(f"\n  Top PS words for {dialect_label} by section:")
    for sec in sorted(section_para_n.keys()):
        n_para = section_para_n[sec]
        if n_para < 5:
            continue
        # Collect all PS words in this section
        ps_words = Counter()
        for para in paras:
            if para['section'] == sec:
                fl = para['lines'][0]
                if fl:
                    ps_words[fl[0]] += 1
        top = ', '.join(f"{w}({c})" for w, c in ps_words.most_common(5))
        print(f"    {sec:<10} (n={n_para}): {top}")
