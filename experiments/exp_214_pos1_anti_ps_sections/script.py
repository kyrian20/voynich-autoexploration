"""
exp_214: H405 — B pos=1 Anti-PS Constraint — Section-Level Stability

Motivation:
  exp_213 (F213): B pos=1 has 0/98 words from p+t+k onset (67% of PS). Two-slot B first-line
  formula established: [PS: p/t/k] → [pos=1: sh/qok/ch].

  H405: Is this constraint stable across B sections (herbal/stars/cosmo/pharma)?
  If stable across sections, it is a grammar rule. If driven by one section, it's a
  scribe convention or section-specific vocabulary.

  Also: Full A-dialect pos=1 onset analysis for complete A/B comparison.

Test:
  (1) B pos=1 p+t+k rate by section
  (2) B PS onset distribution by section (to confirm PS formula stability)
  (3) A pos=1 onset distribution by section
  (4) Both dialects: gallows vs anti-gallows at pos=0 and pos=1 by section
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

GALLOWS = {'p', 't', 'k', 'f'}

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix):
            return label
    return 'other'

def is_gallows(onset):
    return onset in GALLOWS

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

for dialect_label in ['B', 'A']:
    paras = [p for p in paragraphs if p['dialect'] == dialect_label and len(p['lines']) >= 2]
    print(f"\n{'='*60}")
    print(f"{dialect_label}-DIALECT ANALYSIS (n={len(paras)} paragraphs ≥2 lines)")

    # Collect by section: PS (pos=0) and pos=1 onset × section
    # section → [list of (pos0_onset, pos1_onset) or None if line has <2 words]
    section_ps = defaultdict(Counter)
    section_p1 = defaultdict(Counter)
    section_counts = defaultdict(lambda: {'ps': 0, 'p1': 0})
    section_gallows_ps = defaultdict(int)
    section_gallows_p1 = defaultdict(int)
    section_ptk_ps = defaultdict(int)    # p+t+k (not f)
    section_ptk_p1 = defaultdict(int)

    all_sections = set()
    for para in paras:
        sec = para['section']
        all_sections.add(sec)
        fl = para['lines'][0]
        if len(fl) >= 1:
            ps_onset = get_onset(fl[0])
            section_ps[sec][ps_onset] += 1
            section_counts[sec]['ps'] += 1
            if is_gallows(ps_onset):
                section_gallows_ps[sec] += 1
            if ps_onset in ('p', 't', 'k'):
                section_ptk_ps[sec] += 1
        if len(fl) >= 2:
            p1_onset = get_onset(fl[1])
            section_p1[sec][p1_onset] += 1
            section_counts[sec]['p1'] += 1
            if is_gallows(p1_onset):
                section_gallows_p1[sec] += 1
            if p1_onset in ('p', 't', 'k'):
                section_ptk_p1[sec] += 1

    print(f"\n  Section-level PS and pos=1 gallows rates:")
    print(f"  {'Section':<12} {'n_ps':<8} {'gal_PS%':<10} {'ptk_PS%':<10} {'n_p1':<8} {'gal_P1%':<10} {'ptk_P1%':<10} {'ptk_P1=0?'}")
    for sec in sorted(all_sections):
        n_ps = section_counts[sec]['ps']
        n_p1 = section_counts[sec]['p1']
        g_ps = section_gallows_ps[sec] / n_ps * 100 if n_ps > 0 else 0
        g_p1 = section_gallows_p1[sec] / n_p1 * 100 if n_p1 > 0 else 0
        ptk_ps = section_ptk_ps[sec] / n_ps * 100 if n_ps > 0 else 0
        ptk_p1 = section_ptk_p1[sec] / n_p1 * 100 if n_p1 > 0 else 0
        zero = "YES (0/n)" if section_ptk_p1[sec] == 0 else f"NO (n={section_ptk_p1[sec]})"
        print(f"  {sec:<12} {n_ps:<8} {g_ps:<10.1f} {ptk_ps:<10.1f} {n_p1:<8} {g_p1:<10.1f} {ptk_p1:<10.1f} {zero}")

    print(f"\n  Totals: PS p+t+k = {sum(section_ptk_ps.values())} ({sum(section_ptk_ps.values())/sum(section_counts[s]['ps'] for s in all_sections)*100:.1f}%)")
    print(f"          pos=1 p+t+k = {sum(section_ptk_p1.values())} ({sum(section_ptk_p1.values())/max(1,sum(section_counts[s]['p1'] for s in all_sections))*100:.1f}%)")
    print(f"          pos=1 gallows = {sum(section_gallows_p1.values())} ({sum(section_gallows_p1.values())/max(1,sum(section_counts[s]['p1'] for s in all_sections))*100:.1f}%)")

    print(f"\n  B pos=1 onset distribution detail (all sections combined):")
    p1_all = Counter()
    p1_total = 0
    ps_all = Counter()
    ps_total = 0
    for sec in all_sections:
        p1_all += section_p1[sec]
        p1_total += section_counts[sec]['p1']
        ps_all += section_ps[sec]
        ps_total += section_counts[sec]['ps']

    print(f"  {'Onset':<8} {'PS n':<8} {'PS%':<8} {'pos=1 n':<10} {'pos=1%':<10}")
    for onset, _ in ONSET_ORDER:
        ps_n = ps_all.get(onset, 0)
        p1_n = p1_all.get(onset, 0)
        ps_r = ps_n / ps_total * 100 if ps_total > 0 else 0
        p1_r = p1_n / p1_total * 100 if p1_total > 0 else 0
        if ps_n > 0 or p1_n > 0:
            flag = " ← HARD EXCLUSION" if ps_n > 3 and p1_n == 0 else ""
            print(f"  {onset:<8} {ps_n:<8} {ps_r:<8.1f} {p1_n:<10} {p1_r:<10.1f}{flag}")
