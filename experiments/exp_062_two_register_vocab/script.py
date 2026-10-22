"""
exp_062: Vocabulary Differences in Two-Register Herbal A Folios (H068)
Tests whether aiin-dominant herbal A folios (f49r, f32r, f8v, f42v, f35r, f20r, f22r, f30v, f32v, f45r, f47r, f47v, f42r, f4r)
differ in vocabulary from y-dominant folios (f6v, f17r, f17v, f19v, f24v, f51r, f53v, etc.)
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

SUFFIX_LIST = ['aiin', 'ain', 'eedy', 'edy', 'chy', 'eey', 'dy', 'ey', 'y', 'ol', 'or', 'al', 'ar', 'iin', 'in']

# From exp_060: y@cont < 5%, n_cont >= 10
AIIN_DOMINANT = {'f20r', 'f22r', 'f30v', 'f32r', 'f32v', 'f35r', 'f42r', 'f42v',
                 'f45r', 'f47r', 'f47v', 'f49r', 'f4r', 'f8v'}

# From exp_060: y@cont > 20%, n_cont >= 10
Y_DOMINANT = {'f16v', 'f17r', 'f17v', 'f18r', 'f19v', 'f24r', 'f24v', 'f36v',
              'f37r', 'f3r', 'f3v', 'f44r', 'f44v', 'f51r', 'f52v', 'f53v',
              'f6r', 'f6v', 'f87v', 'f93r', 'f96v', 'f9v'}

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
            text = line[m.end():].strip()
            text = clean_text(text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]
            if not tokens:
                continue
            records.append({'folio': folio_id, 'currier': current_currier, 'section': current_section, 'words': tokens})
    return records

def main():
    records = parse_corpus(DATA_PATH)

    # Separate into two groups
    aiin_words = []
    y_words = []

    for r in records:
        if r['currier'] == 'A' and r['section'] == 'H':
            if r['folio'] in AIIN_DOMINANT:
                aiin_words.extend(r['words'])
            elif r['folio'] in Y_DOMINANT:
                y_words.extend(r['words'])

    print(f"Aiin-dominant group: {len(aiin_words)} tokens from {len(AIIN_DOMINANT)} folios")
    print(f"y-dominant group: {len(y_words)} tokens from {len(Y_DOMINANT)} folios")

    aiin_counter = Counter(aiin_words)
    y_counter = Counter(y_words)
    n_aiin = len(aiin_words)
    n_y = len(y_words)

    # Vocabulary overlap
    aiin_types = set(aiin_counter.keys())
    y_types = set(y_counter.keys())
    shared = aiin_types & y_types
    jaccard = len(shared) / len(aiin_types | y_types)
    print(f"\nVocabulary overlap:")
    print(f"  Aiin-dominant types: {len(aiin_types)}")
    print(f"  y-dominant types: {len(y_types)}")
    print(f"  Shared types: {len(shared)}")
    print(f"  Jaccard: {jaccard:.3f}")
    print(f"  Aiin-exclusive types: {len(aiin_types - y_types)}")
    print(f"  y-exclusive types: {len(y_types - aiin_types)}")

    # Top words in each group
    print(f"\n--- TOP 20 WORDS IN AIIN-DOMINANT FOLIOS ---")
    print(f"{'Word':<16} {'Aiin_count':>10} {'Aiin%':>7} {'y_count':>10} {'y%':>7} {'Ratio':>7}")
    for word, count in aiin_counter.most_common(20):
        aiin_p = count / n_aiin
        y_p = y_counter.get(word, 0) / n_y
        ratio = aiin_p / max(y_p, 1e-10)
        print(f"{word:<16} {count:>10} {100*aiin_p:>6.2f}% {y_counter.get(word, 0):>10} {100*y_p:>6.2f}% {ratio:>7.2f}×")

    print(f"\n--- TOP 20 WORDS IN y-DOMINANT FOLIOS ---")
    print(f"{'Word':<16} {'y_count':>10} {'y%':>7} {'Aiin_count':>10} {'Aiin%':>7} {'Ratio':>7}")
    for word, count in y_counter.most_common(20):
        y_p = count / n_y
        aiin_p = aiin_counter.get(word, 0) / n_aiin
        ratio = y_p / max(aiin_p, 1e-10)
        print(f"{word:<16} {count:>10} {100*y_p:>6.2f}% {aiin_counter.get(word, 0):>10} {100*aiin_p:>6.2f}% {ratio:>7.2f}×")

    # Most over-represented in aiin-dominant (ratio aiin/y > 2.0)
    print(f"\n--- WORDS OVER-REPRESENTED IN AIIN-DOMINANT (ratio > 2.0, min 5 occurrences) ---")
    print(f"{'Word':<16} {'Aiin':>6} {'Aiin%':>7} {'y':>6} {'y%':>7} {'Ratio':>7}")
    over_rep_aiin = []
    for word, count in aiin_counter.items():
        if count < 5:
            continue
        aiin_p = count / n_aiin
        y_p = y_counter.get(word, 0) / n_y
        ratio = aiin_p / max(y_p, 1e-6)
        if ratio > 2.0:
            over_rep_aiin.append((word, count, aiin_p, y_counter.get(word,0), y_p, ratio))
    over_rep_aiin.sort(key=lambda x: -x[5])
    for word, count, aiin_p, y_cnt, y_p, ratio in over_rep_aiin[:20]:
        print(f"{word:<16} {count:>6} {100*aiin_p:>6.2f}% {y_cnt:>6} {100*y_p:>6.2f}% {ratio:>7.2f}×")

    # Most over-represented in y-dominant
    print(f"\n--- WORDS OVER-REPRESENTED IN y-DOMINANT (ratio > 2.0, min 5 occurrences) ---")
    print(f"{'Word':<16} {'y':>6} {'y%':>7} {'Aiin':>6} {'Aiin%':>7} {'Ratio':>7}")
    over_rep_y = []
    for word, count in y_counter.items():
        if count < 5:
            continue
        y_p = count / n_y
        aiin_p = aiin_counter.get(word, 0) / n_aiin
        ratio = y_p / max(aiin_p, 1e-6)
        if ratio > 2.0:
            over_rep_y.append((word, count, y_p, aiin_counter.get(word,0), aiin_p, ratio))
    over_rep_y.sort(key=lambda x: -x[5])
    for word, count, y_p, aiin_cnt, aiin_p, ratio in over_rep_y[:20]:
        print(f"{word:<16} {count:>6} {100*y_p:>6.2f}% {aiin_cnt:>6} {100*aiin_p:>6.2f}% {ratio:>7.2f}×")

    # Suffix distribution comparison
    print(f"\n--- SUFFIX DISTRIBUTION COMPARISON ---")
    aiin_suf = Counter(suffix_group(w) or '(none)' for w in aiin_words)
    y_suf = Counter(suffix_group(w) or '(none)' for w in y_words)
    print(f"{'Suffix':<8} {'Aiin%':>7} {'y%':>7} {'Ratio':>7}")
    for suf in SUFFIX_LIST + ['(none)']:
        ap = aiin_suf.get(suf, 0) / n_aiin
        yp = y_suf.get(suf, 0) / n_y
        ratio = ap / max(yp, 1e-10)
        if ap > 0.005 or yp > 0.005:
            print(f"{suf:<8} {100*ap:>6.1f}% {100*yp:>6.1f}% {ratio:>7.2f}×")

    # Onset distribution comparison
    print(f"\n--- ONSET DISTRIBUTION COMPARISON ---")
    def classify_onset(word):
        if word.startswith('qo') and len(word) > 2: return 'qo'
        if word.startswith('ch') and len(word) > 2: return 'ch'
        if word.startswith('sh') and len(word) > 2: return 'sh'
        if word.startswith('cth') and len(word) > 3: return 'cth'
        if word.startswith('o') and len(word) > 1: return 'o'
        if word.startswith('d') and len(word) > 1: return 'd'
        if word.startswith('y') and len(word) > 1: return 'y'
        if word.startswith('k') and len(word) > 1: return 'k'
        if word.startswith('t') and len(word) > 1: return 't'
        if word.startswith('s') and len(word) > 1: return 's'
        return 'other'

    aiin_onset = Counter(classify_onset(w) for w in aiin_words)
    y_onset = Counter(classify_onset(w) for w in y_words)
    print(f"{'Onset':<8} {'Aiin%':>7} {'y%':>7} {'Ratio':>7}")
    for onset in ['qo', 'ch', 'sh', 'cth', 'o', 'd', 'y', 'k', 't', 's', 'other']:
        ap = aiin_onset.get(onset, 0) / n_aiin
        yp = y_onset.get(onset, 0) / n_y
        ratio = ap / max(yp, 1e-10)
        print(f"{onset:<8} {100*ap:>6.1f}% {100*yp:>6.1f}% {ratio:>7.2f}×")

if __name__ == '__main__':
    main()
