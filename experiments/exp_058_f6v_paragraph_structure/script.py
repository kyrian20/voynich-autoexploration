"""
exp_058: f6v Paragraph Structure Analysis (H065)
f6v has 38.1% y-initial lines — far above the herbal A mean (~15%).
Tests whether this is due to: (a) very long paragraphs, (b) unusual text layout,
or (c) scribal preference. Compares f6v paragraph lengths to other herbal A folios.
"""

import re
from collections import Counter, defaultdict

DATA_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"

def clean_text(text):
    return re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)

def is_body_locus(locus_code):
    base = locus_code.lstrip('+*@=/~&')
    return base.startswith('P')

def parse_folio_lines(path):
    """Parse lines keeping track of folio, currier, section, and line type."""
    lines = []
    current_currier = None
    current_section = None
    current_folio = None

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

            # Extract folio ID (e.g., f6v from f6v.P1 or similar)
            folio_id = folio_raw.split('.')[0] if '.' in folio_raw else folio_raw

            if not is_body_locus(locus_code):
                continue

            # Determine line type
            base_locus = locus_code.lstrip('+*@=/~&')
            raw_prefix = locus_code[0] if locus_code else ''
            if raw_prefix == '@':
                line_type = 'para_start'
            elif raw_prefix == '+':
                line_type = 'continuation'
            else:
                line_type = 'other'

            text = line[m.end():].strip()
            text = clean_text(text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]

            if not tokens:
                continue

            lines.append({
                'folio': folio_id,
                'currier': current_currier,
                'section': current_section,
                'line_type': line_type,
                'words': tokens,
            })

    return lines

def paragraph_stats(folio_lines):
    """
    Compute paragraphs and their lengths.
    A new paragraph starts at each para_start line.
    """
    paragraphs = []
    current_para = []
    for l in folio_lines:
        if l['line_type'] == 'para_start':
            if current_para:
                paragraphs.append(current_para)
            current_para = [l]
        else:
            current_para.append(l)
    if current_para:
        paragraphs.append(current_para)

    para_lengths = [len(p) for p in paragraphs]
    return paragraphs, para_lengths

def analyze_folio(folio_id, folio_lines):
    """
    Compute:
    - Total lines, y-initial lines, y-initial%
    - Number of paragraphs
    - Mean/max paragraph length in lines
    - Whether there are any para_start lines
    """
    n = len(folio_lines)
    y_initial = sum(1 for l in folio_lines if l['words'][0].startswith('y'))
    para_starts = sum(1 for l in folio_lines if l['line_type'] == 'para_start')
    paragraphs, para_lengths = paragraph_stats(folio_lines)
    n_paras = len(paragraphs)
    mean_para_len = sum(para_lengths) / max(n_paras, 1)
    max_para_len = max(para_lengths) if para_lengths else 0

    return {
        'folio': folio_id,
        'n_lines': n,
        'y_initial': y_initial,
        'y_rate': y_initial / max(n, 1),
        'n_paras': n_paras,
        'mean_para_len': mean_para_len,
        'max_para_len': max_para_len,
        'para_starts': para_starts,
    }

def main():
    lines = parse_folio_lines(DATA_PATH)
    print(f"Total lines: {len(lines)}")

    # Group lines by folio
    folio_lines = defaultdict(list)
    for l in lines:
        if l['currier'] == 'A':
            folio_lines[l['folio']].append(l)

    # Analyze f6v specifically
    f6v_lines = folio_lines.get('f6v', [])
    print(f"\nf6v: {len(f6v_lines)} Currier A body lines")
    if not f6v_lines:
        print("f6v not found in corpus!")
        return

    f6v_stats = analyze_folio('f6v', f6v_lines)
    print(f"  y-initial: {f6v_stats['y_initial']}/{f6v_stats['n_lines']} = {100*f6v_stats['y_rate']:.1f}%")
    print(f"  Para-starts: {f6v_stats['para_starts']}")
    print(f"  Paragraphs: {f6v_stats['n_paras']}")
    print(f"  Mean para length: {f6v_stats['mean_para_len']:.1f} lines")
    print(f"  Max para length: {f6v_stats['max_para_len']} lines")

    # Show each paragraph in f6v
    paragraphs, para_lengths = paragraph_stats(f6v_lines)
    print(f"\n  f6v paragraph breakdown:")
    for i, (para, length) in enumerate(zip(paragraphs, para_lengths), 1):
        y_count = sum(1 for l in para if l['words'][0].startswith('y'))
        first_words = [l['words'][0] for l in para[:3]]
        print(f"    Para {i}: {length} lines, {y_count} y-initial ({100*y_count/max(length,1):.0f}%), starts: {first_words}")

    # Compare to all Currier A herbal folios (section H)
    print(f"\n{'='*70}")
    print("COMPARISON: All Currier A Herbal folios (≥10 lines)")
    print(f"{'='*70}")
    print(f"{'Folio':<8} {'Lines':>6} {'y%':>5} {'Paras':>6} {'MeanLen':>8} {'MaxLen':>7}")

    herbal_stats = []
    for folio_id, flines in sorted(folio_lines.items()):
        # Filter to herbal section
        herbal_lines = [l for l in flines if l.get('section') == 'H']
        if len(herbal_lines) >= 10:
            stats = analyze_folio(folio_id, herbal_lines)
            herbal_stats.append(stats)

    herbal_stats.sort(key=lambda x: -x['y_rate'])
    for s in herbal_stats:
        marker = ' <-- f6v' if s['folio'] == 'f6v' else ''
        print(f"{s['folio']:<8} {s['n_lines']:>6} {100*s['y_rate']:>4.1f}% {s['n_paras']:>6} {s['mean_para_len']:>8.1f} {s['max_para_len']:>7}{marker}")

    # Compute correlation: y_rate vs mean_para_len
    herbal_subset = [s for s in herbal_stats if s['n_paras'] >= 2]
    if len(herbal_subset) >= 5:
        y_rates = [s['y_rate'] for s in herbal_subset]
        para_lens = [s['mean_para_len'] for s in herbal_subset]
        n = len(herbal_subset)
        mean_y = sum(y_rates) / n
        mean_p = sum(para_lens) / n
        num = sum((y - mean_y) * (p - mean_p) for y, p in zip(y_rates, para_lens))
        den_y = (sum((y - mean_y)**2 for y in y_rates)) ** 0.5
        den_p = (sum((p - mean_p)**2 for p in para_lens)) ** 0.5
        r = num / max(den_y * den_p, 1e-10)
        print(f"\nCorrelation y-rate vs mean paragraph length (herbal A folios): r = {r:.3f}")

    # Compare to all sections
    print(f"\n{'='*70}")
    print("f6v vs ALL Currier A folios (≥10 lines): where does f6v rank?")
    print(f"{'='*70}")
    all_stats = []
    for folio_id, flines in sorted(folio_lines.items()):
        if len(flines) >= 10:
            stats = analyze_folio(folio_id, flines)
            all_stats.append(stats)
    all_stats.sort(key=lambda x: -x['y_rate'])
    for rank, s in enumerate(all_stats[:20], 1):
        marker = ' <-- f6v' if s['folio'] == 'f6v' else ''
        print(f"  #{rank:<3} {s['folio']:<8} y={100*s['y_rate']:.1f}% paras={s['n_paras']} meanLen={s['mean_para_len']:.1f}{marker}")

if __name__ == '__main__':
    main()
