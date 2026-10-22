"""
exp_365: A-Dialect {aiin→ol} Shift — Word-Level Vocabulary (H578)
F342 (exp_340): A-dialect {aiin→ol} shift section-specific: pharma=17.88×, herbal=3.98×.
F340 (exp_338): universal shift in ALL template onsets; d-onset unchanged.
Question: What are the specific words involved? In pharma, what specific aiin-body words
are ABSENT while ol-body words are PRESENT? Is it chaiin→chol, qokaiin→qokol, etc.?
"""
from pathlib import Path as _RepositoryPath

import os, re
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

def folio_base(folio):
    return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    return 'B' if (stats['edy'] + stats['eedy']) / total >= 0.05 else 'A'

def section_for_folio(fb):
    m = re.match(r'f(\d+)', fb)
    if not m: return 'unknown'
    n = int(m.group(1))
    if 1 <= n <= 66: return 'herbal'
    elif 67 <= n <= 73: return 'astro'
    elif 74 <= n <= 84: return 'bio'
    elif 85 <= n <= 86: return 'cosmo'
    elif 87 <= n <= 102: return 'pharma'
    else: return 'text'

ONSET_ORDER = [
    ('qok','qok'),('qot','qot'),('qo','qo'),('cth','cth'),
    ('ch','ch'),('sh','sh'),('ok','ok'),('ot','ot'),('ol','ol'),
    ('d','d'),('s','s'),('y','y'),('k','k'),('t','t'),
    ('l','l'),('r','r'),('p','p'),('f','f'),('o','o')
]

def get_onset(word):
    for label, prefix in ONSET_ORDER:
        if word.startswith(prefix):
            return label
    return 'other'

def has_aiin_body(word):
    # Check for aiin or ain body
    return 'aiin' in word or 'ain' in word

def has_ol_body(word):
    # Check for ol or or body (ol-class)
    for onset, prefix in ONSET_ORDER:
        if word.startswith(prefix):
            body = word[len(prefix):]
            if body.startswith('ol') or body.startswith('or'):
                return True
            return False
    return False

# Pass 1: classify folios
folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
with open(DATA_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'): continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
        if not m: continue
        folio = m.group(1).lstrip('+*=&~')
        fb = folio_base(folio)
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        for w in words:
            folio_word_stats[fb]['total'] += 1
            if w.endswith('eedy'): folio_word_stats[fb]['eedy'] += 1
            elif w.endswith('edy'): folio_word_stats[fb]['edy'] += 1

folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}

# Collect A-dialect words by section and onset class
section_onset_words = defaultdict(lambda: defaultdict(Counter))  # section -> onset -> words
section_totals = defaultdict(int)

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'): continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
        if not m: continue
        folio = m.group(1).lstrip('+*=&~')
        fb = folio_base(folio)
        dialect = folio_dialect.get(fb, 'unknown')
        if dialect != 'A': continue
        locus_code = m.group(3)
        lc = locus_code.lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'): continue
        section = section_for_folio(fb)
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        for w in words:
            onset = get_onset(w)
            section_onset_words[section][onset][w] += 1
            section_totals[section] += 1

print("=" * 70)
print("A-DIALECT {aiin→ol} SHIFT: WORD-LEVEL VOCABULARY (H578)")
print("=" * 70)

# For each template onset class, compare aiin-body vs ol-body words across sections
TEMPLATE_ONSETS = ['ch', 'sh', 'qok', 'ok', 'ot', 'qot']

for onset in TEMPLATE_ONSETS:
    print(f"\n{'='*60}")
    print(f"ONSET: {onset}")
    print(f"{'='*60}")
    
    # For herbal and pharma sections
    for section in ['herbal', 'pharma', 'text']:
        words = section_onset_words[section][onset]
        total_section = section_totals[section]
        total_onset = sum(words.values())
        if total_onset < 5: continue
        
        # Separate aiin-body vs ol-body words
        aiin_words = {w: c for w, c in words.items() if has_aiin_body(w)}
        ol_words = {w: c for w, c in words.items() if has_ol_body(w)}
        aiin_total = sum(aiin_words.values())
        ol_total = sum(ol_words.values())
        
        print(f"\n  Section: {section} (total={total_section}, {onset}_total={total_onset})")
        print(f"  aiin-body: {aiin_total}/{total_onset}={100*aiin_total/max(total_onset,1):.1f}%")
        print(f"  ol-body:   {ol_total}/{total_onset}={100*ol_total/max(total_onset,1):.1f}%")
        print(f"  ol/aiin ratio: {ol_total/max(aiin_total,1):.2f}")
        
        # Top aiin-body words
        if aiin_words:
            print(f"  Top aiin-body words:")
            for w, c in sorted(aiin_words.items(), key=lambda x: -x[1])[:5]:
                print(f"    {w}: {c}")
        
        # Top ol-body words
        if ol_words:
            print(f"  Top ol-body words:")
            for w, c in sorted(ol_words.items(), key=lambda x: -x[1])[:5]:
                print(f"    {w}: {c}")

# Cross-section comparison: ch onset specifically
print(f"\n{'='*60}")
print("SUMMARY TABLE: ol/aiin ratio per onset per section")
print(f"{'='*60}")
print(f"{'Onset':<8} {'herbal_ol/aiin':>16} {'pharma_ol/aiin':>16} {'text_ol/aiin':>14}")
for onset in TEMPLATE_ONSETS:
    ratios = {}
    for section in ['herbal', 'pharma', 'text']:
        words = section_onset_words[section][onset]
        aiin_total = sum(c for w, c in words.items() if has_aiin_body(w))
        ol_total = sum(c for w, c in words.items() if has_ol_body(w))
        total_onset = sum(words.values())
        if total_onset < 5:
            ratios[section] = 'N/A'
        else:
            ratios[section] = f"{ol_total/max(aiin_total,0.5):.2f} ({ol_total}/{max(aiin_total,0)})"
    print(f"  {onset:<8} {ratios.get('herbal','N/A'):>16} {ratios.get('pharma','N/A'):>16} {ratios.get('text','N/A'):>14}")

# d-onset (should NOT shift per F340)
print(f"\n{'='*60}")
print("d-onset comparison (should NOT shift per F340)")
print(f"{'='*60}")
for section in ['herbal', 'pharma', 'text']:
    words = section_onset_words[section]['d']
    total_onset = sum(words.values())
    if total_onset < 5: continue
    aiin_total = sum(c for w, c in words.items() if has_aiin_body(w))
    ol_total = sum(c for w, c in words.items() if has_ol_body(w))
    print(f"  {section:<10}: d-aiin={aiin_total}, d-ol={ol_total}, ol/aiin={ol_total/max(aiin_total,0.5):.2f}")
    # Top d-words
    top_d = sorted(words.items(), key=lambda x: -x[1])[:6]
    print(f"    Top: {', '.join(f'{w}({c})' for w,c in top_d)}")

# Specific word-level shift: pharma vs herbal for ch and qok
print(f"\n{'='*60}")
print("WORD-LEVEL SHIFT: ch-onset pharma vs herbal (top words)")
print(f"{'='*60}")
for onset in ['ch', 'qok', 'sh']:
    herb_words = section_onset_words['herbal'][onset]
    pharma_words = section_onset_words['pharma'][onset]
    h_total = sum(herb_words.values())
    p_total = sum(pharma_words.values())
    if h_total < 5 or p_total < 5: continue
    
    print(f"\n  Onset: {onset}")
    print(f"  {'Word':<15} {'Herbal%':>9} {'Pharma%':>9} {'P/H ratio':>11}")
    all_words = set(herb_words) | set(pharma_words)
    # Focus on words with aiin or ol body
    relevant = [(w, herb_words.get(w,0)/max(h_total,1), pharma_words.get(w,0)/max(p_total,1))
                for w in all_words
                if (has_aiin_body(w) or has_ol_body(w)) and 
                   (herb_words.get(w,0) + pharma_words.get(w,0)) >= 2]
    relevant.sort(key=lambda x: max(x[1], x[2]), reverse=True)
    for word, h_pct, p_pct in relevant[:15]:
        body_type = 'aiin' if has_aiin_body(word) else 'ol'
        ratio = p_pct / max(h_pct, 0.0001)
        print(f"  {word:<15} {100*h_pct:>8.2f}% {100*p_pct:>8.2f}% {ratio:>9.2f}× [{body_type}]")

