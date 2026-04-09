"""
exp_060: daiin × y-initial Correlation + Quire Clustering of Aiin-Dominant Folios (H069, H072)
Tests two small hypotheses from the recent findings:
H069: Is daiin frequency negatively correlated with y-initial rate across herbal A folios?
H072: Do the aiin-dominant herbal A folios cluster in specific quires?
"""

import re
from collections import Counter, defaultdict

DATA_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"
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
                'quire': current_quire,
                'line_type': line_type,
                'words': tokens,
            })

    return records

def main():
    records = parse_corpus(DATA_PATH)

    # Group by folio, keep only herbal A body text
    folio_data = defaultdict(lambda: {'lines': [], 'quire': None})
    for r in records:
        if r['currier'] == 'A' and r['section'] == 'H':
            folio_data[r['folio']]['lines'].append(r)
            if r['quire']:
                folio_data[r['folio']]['quire'] = r['quire']

    # Compute per-folio statistics
    folio_stats = []
    for folio_id, data in sorted(folio_data.items()):
        lines = data['lines']
        quire = data['quire']
        if len(lines) < 10:
            continue

        all_words = [w for l in lines for w in l['words']]
        n_words = len(all_words)
        n_lines = len(lines)
        cont_lines = [l for l in lines if l['line_type'] == 'continuation']
        n_cont = len(cont_lines)

        daiin_rate = sum(1 for w in all_words if w == 'daiin') / max(n_words, 1)
        y_initial_rate = sum(1 for l in lines if l['words'][0].startswith('y')) / max(n_lines, 1)
        y_cont_rate = sum(1 for l in cont_lines if l['words'][0].startswith('y')) / max(n_cont, 1) if n_cont > 0 else float('nan')
        aiin_last_rate = sum(1 for l in lines if suffix_group(l['words'][-1]) == 'aiin') / max(n_lines, 1)

        folio_stats.append({
            'folio': folio_id,
            'quire': quire,
            'n_lines': n_lines,
            'n_words': n_words,
            'n_cont': n_cont,
            'daiin_rate': daiin_rate,
            'y_initial_rate': y_initial_rate,
            'y_cont_rate': y_cont_rate,
            'aiin_last_rate': aiin_last_rate,
        })

    print(f"Herbal A folios with >=10 lines: {len(folio_stats)}")

    # H069: daiin × y-initial correlation
    print(f"\n{'='*70}")
    print("H069: daiin rate vs y-initial rate (herbal A folios, >=10 lines)")
    print(f"{'='*70}")
    print(f"{'Folio':<10} {'Quire':>8} {'Lines':>6} {'daiin%':>7} {'y_init%':>8} {'y_cont%':>8} {'aiin_last%':>11}")

    # Sort by daiin rate
    for s in sorted(folio_stats, key=lambda x: -x['daiin_rate'])[:30]:
        y_cont = f"{100*s['y_cont_rate']:.1f}%" if s['y_cont_rate']==s['y_cont_rate'] else "N/A"
        print(f"{s['folio']:<10} {str(s['quire']):>8} {s['n_lines']:>6} {100*s['daiin_rate']:>6.2f}% {100*s['y_initial_rate']:>7.1f}% {y_cont:>8} {100*s['aiin_last_rate']:>10.1f}%")

    # Compute correlation
    valid = [(s['daiin_rate'], s['y_initial_rate']) for s in folio_stats]
    n = len(valid)
    mean_d = sum(x[0] for x in valid) / n
    mean_y = sum(x[1] for x in valid) / n
    num = sum((x[0]-mean_d)*(x[1]-mean_y) for x in valid)
    den_d = (sum((x[0]-mean_d)**2 for x in valid))**0.5
    den_y = (sum((x[1]-mean_y)**2 for x in valid))**0.5
    r = num / max(den_d * den_y, 1e-10)
    print(f"\nCorrelation daiin_rate vs y_initial_rate (n={n}): r = {r:.3f}")

    valid2 = [(s['daiin_rate'], s['y_cont_rate']) for s in folio_stats if s['y_cont_rate']==s['y_cont_rate']]
    n2 = len(valid2)
    mean_d2 = sum(x[0] for x in valid2) / n2
    mean_y2 = sum(x[1] for x in valid2) / n2
    num2 = sum((x[0]-mean_d2)*(x[1]-mean_y2) for x in valid2)
    den_d2 = (sum((x[0]-mean_d2)**2 for x in valid2))**0.5
    den_y2 = (sum((x[1]-mean_y2)**2 for x in valid2))**0.5
    r2 = num2 / max(den_d2 * den_y2, 1e-10)
    print(f"Correlation daiin_rate vs y_cont_rate (n={n2}): r = {r2:.3f}")

    # H072: Quire clustering of aiin-dominant folios
    print(f"\n{'='*70}")
    print("H072: Quire assignment of aiin-dominant vs y-dominant herbal A folios")
    print(f"{'='*70}")

    # Identify aiin-dominant (y@cont < 5%, n_cont >= 10)
    aiin_dom = [s for s in folio_stats if s['y_cont_rate']==s['y_cont_rate'] and s['y_cont_rate'] < 0.05 and s['n_cont'] >= 10]
    y_dom = [s for s in folio_stats if s['y_cont_rate']==s['y_cont_rate'] and s['y_cont_rate'] > 0.20 and s['n_cont'] >= 10]

    print(f"\nAiin-dominant folios (y@cont < 5%, n_cont >= 10): {len(aiin_dom)}")
    for s in sorted(aiin_dom, key=lambda x: x['folio']):
        print(f"  {s['folio']:<10} quire={s['quire']}, y@cont={100*s['y_cont_rate']:.1f}%, aiin_last={100*s['aiin_last_rate']:.1f}%, daiin={100*s['daiin_rate']:.2f}%")

    print(f"\ny-dominant folios (y@cont > 20%, n_cont >= 10): {len(y_dom)}")
    for s in sorted(y_dom, key=lambda x: x['folio']):
        print(f"  {s['folio']:<10} quire={s['quire']}, y@cont={100*s['y_cont_rate']:.1f}%, aiin_last={100*s['aiin_last_rate']:.1f}%, daiin={100*s['daiin_rate']:.2f}%")

    # Quire distribution
    aiin_quires = Counter(s['quire'] for s in aiin_dom)
    y_quires = Counter(s['quire'] for s in y_dom)
    all_quires = Counter(s['quire'] for s in folio_stats)
    print(f"\nQuire distribution:")
    print(f"{'Quire':>10} {'All':>5} {'Aiin-dom':>10} {'y-dom':>7}")
    for q in sorted(all_quires.keys()):
        print(f"{str(q):>10} {all_quires[q]:>5} {aiin_quires.get(q,0):>10} {y_quires.get(q,0):>7}")

if __name__ == '__main__':
    main()
