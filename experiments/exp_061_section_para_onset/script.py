"""
exp_061: Paragraph Structure by Section (H071) + k vs t Onset Classes (H070)
H071: Is single-paragraph structure herbal-specific, or does it extend to all sections?
H070: Do k-initial and t-initial words (the 'other' onset class) have different suffix preferences?
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict
import math

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

            records.append({
                'folio': folio_id,
                'currier': current_currier,
                'section': current_section,
                'line_type': line_type,
                'words': tokens,
            })

    return records

def analyze_paragraph_structure_by_section(records):
    """H071: Number of para-starts per folio by section."""
    print("="*70)
    print("H071: PARAGRAPH STRUCTURE BY SECTION")
    print("="*70)

    # Group by section × folio
    folio_ps = defaultdict(lambda: {'para_starts': 0, 'total_lines': 0, 'section': None})
    for r in records:
        key = (r['section'], r['folio'])
        folio_ps[key]['para_starts'] += (1 if r['line_type'] == 'para_start' else 0)
        folio_ps[key]['total_lines'] += 1
        folio_ps[key]['section'] = r['section']

    # By section
    section_data = defaultdict(list)
    for (section, folio), data in folio_ps.items():
        if data['total_lines'] >= 5:
            section_data[section].append({
                'folio': folio,
                'para_starts': data['para_starts'],
                'total_lines': data['total_lines'],
            })

    print(f"\n{'Section':>10} {'Folios':>7} {'AvgPS':>7} {'SinglePara%':>12} {'MultiPara%':>11} {'MaxPS':>6}")
    section_order = ['H', 'B', 'P', 'S', 'A', 'C', 'T']
    for section in section_order:
        folios = section_data.get(section, [])
        if not folios:
            continue
        n = len(folios)
        avg_ps = sum(f['para_starts'] for f in folios) / n
        single = sum(1 for f in folios if f['para_starts'] <= 1)
        multi = sum(1 for f in folios if f['para_starts'] > 1)
        max_ps = max(f['para_starts'] for f in folios)
        print(f"{section:>10} {n:>7} {avg_ps:>7.2f} {100*single/n:>11.1f}% {100*multi/n:>10.1f}% {max_ps:>6}")

    print(f"\n--- MULTI-PARAGRAPH FOLIOS (>1 para-start, >=10 lines) ---")
    for section in section_order:
        folios = [f for f in section_data.get(section, []) if f['para_starts'] > 1 and f['total_lines'] >= 10]
        if folios:
            print(f"\n{section}: {len(folios)} multi-para folios")
            for f in sorted(folios, key=lambda x: -x['para_starts'])[:10]:
                print(f"  {f['folio']}: {f['para_starts']} para-starts, {f['total_lines']} lines")

def analyze_onset_suffix_disaggregated(records):
    """H070: Disaggregate 'other' onset class into k/t/f/p/s/r subtypes."""
    print("\n" + "="*70)
    print("H070: k vs t ONSET CLASS SUFFIX DISTRIBUTIONS (Currier B)")
    print("="*70)

    def detailed_onset(word):
        """More detailed onset classification."""
        if word.startswith('qo') and len(word) > 2: return 'qo'
        if word.startswith('ch') and len(word) > 2: return 'ch'
        if word.startswith('sh') and len(word) > 2: return 'sh'
        if word.startswith('cth') and len(word) > 3: return 'cth'
        if word.startswith('o') and len(word) > 1: return 'o'
        if word.startswith('d') and len(word) > 1: return 'd'
        if word.startswith('y') and len(word) > 1: return 'y'
        # Disaggregate 'other'
        if word.startswith('k') and len(word) > 1: return 'k'
        if word.startswith('t') and len(word) > 1: return 't'
        if word.startswith('f') and len(word) > 1: return 'f'
        if word.startswith('p') and len(word) > 1: return 'p'
        if word.startswith('s') and len(word) > 1: return 's'
        if word.startswith('r') and len(word) > 1: return 'r'
        return 'other_misc'

    # Currier B words
    b_words = []
    for r in records:
        if r['currier'] == 'B':
            b_words.extend(r['words'])

    print(f"Currier B total: {len(b_words)} tokens")

    onset_suffix = defaultdict(Counter)
    onset_counts = Counter()
    suffix_counts = Counter()

    for w in b_words:
        onset = detailed_onset(w)
        suf = suffix_group(w) or '(none)'
        onset_suffix[onset][suf] += 1
        onset_counts[onset] += 1
        suffix_counts[suf] += 1

    n_total = len(b_words)

    # Focus on k and t vs other onsets
    top_suffixes = [s for s, _ in suffix_counts.most_common(12) if s != '(none)']

    print(f"\nOnset distribution (top 12 onset classes):")
    for onset, count in onset_counts.most_common(15):
        print(f"  {onset:<12} {count:>6} ({100*count/n_total:.1f}%)")

    print(f"\n--- SUFFIX DISTRIBUTION: k vs t vs qo vs ch vs sh (Currier B) ---")
    print(f"{'Suffix':<8}", end='')
    for onset in ['k', 't', 'f', 'p', 's', 'qo', 'ch', 'sh', 'd']:
        print(f"{onset:>8}", end='')
    print(f"  {'marginal':>8}")

    for suf in top_suffixes[:12]:
        print(f"{'-'+suf:<8}", end='')
        for onset in ['k', 't', 'f', 'p', 's', 'qo', 'ch', 'sh', 'd']:
            n_onset = onset_counts[onset]
            if n_onset > 0:
                p = onset_suffix[onset].get(suf, 0) / n_onset
                print(f"{100*p:>7.1f}%", end='')
            else:
                print(f"{'N/A':>8}", end='')
        marginal = suffix_counts[suf] / n_total
        print(f"  {100*marginal:>7.1f}%")

    # KL divergence between onset classes
    print(f"\n--- KL DIVERGENCE BETWEEN ONSET CLASSES (Currier B) ---")
    print(f"{'Onset pair':<20} {'KL bits':>8} {'n_onset1':>10} {'n_onset2':>10}")

    def kl_div(onset1, onset2):
        n1 = onset_counts[onset1]
        n2 = onset_counts[onset2]
        if n1 < 10 or n2 < 10:
            return float('nan')
        kl = 0.0
        for suf in list(suffix_counts.keys()):
            p = onset_suffix[onset1].get(suf, 0) / max(n1, 1)
            q = onset_suffix[onset2].get(suf, 0) / max(n2, 1)
            if p > 1e-9 and q > 1e-9:
                kl += p * math.log2(p / q)
        return kl

    onset_pairs = [
        ('k', 't'), ('k', 'qo'), ('k', 'ch'), ('k', 'sh'), ('k', 'd'),
        ('t', 'qo'), ('t', 'ch'), ('t', 'sh'), ('t', 'd'),
        ('f', 'k'), ('f', 't'), ('p', 'k'), ('p', 't'),
        ('s', 'k'), ('s', 't'), ('ch', 'qo'), ('sh', 'ch'),
    ]
    for o1, o2 in onset_pairs:
        kl = kl_div(o1, o2)
        if kl == kl:
            print(f"{o1+' vs '+o2:<20} {kl:>8.3f} {onset_counts[o1]:>10} {onset_counts[o2]:>10}")

    # k vs t specific comparison
    print(f"\n--- TOP k-INITIAL WORDS in B ---")
    k_words = Counter()
    for r in records:
        if r['currier'] == 'B':
            for w in r['words']:
                if w.startswith('k') and not w.startswith('qo'):
                    k_words[w] += 1
    print(Counter(k_words).most_common(15))

    print(f"\n--- TOP t-INITIAL WORDS in B ---")
    t_words = Counter()
    for r in records:
        if r['currier'] == 'B':
            for w in r['words']:
                if w.startswith('t'):
                    t_words[w] += 1
    print(Counter(t_words).most_common(15))

if __name__ == '__main__':
    records = parse_corpus(DATA_PATH)
    analyze_paragraph_structure_by_section(records)
    analyze_onset_suffix_disaggregated(records)
