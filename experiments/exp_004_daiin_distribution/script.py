"""
Experiment: exp_004_daiin_distribution
Hypothesis tested: H014 — daiin distribution across text categories and manuscript sections
Also: H012 full analysis (inner-slot character inventory)
Data: data/transcriptions/eva_zl3b.txt
"""

import re
from collections import Counter, defaultdict
from pathlib import Path
import math

BASE = Path(__file__).resolve().parents[2]

LOCUS_CATEGORIES = {
    'P': 'body', 'L': 'label', 'R': 'rider', 'C': 'circular',
}

# Voynich manuscript section folio ranges (approximate, from standard references)
# Herbal A: f1r–f66r (many gaps); Herbal B: some folios; Pharma: f87r–f102v2;
# Stars/Astro: f67r1–f73v; Cosmo: f68r1–f68v3; Bio/Balneo: f75r–f84v;
# Recipes: f103r–f116v; Zodiac: f70v2–f73v
# Using simplified folio number ranges:
def classify_section(folio_str):
    """Classify a folio reference (like 'f1r', 'f67r1') into a section."""
    m = re.match(r'f(\d+)', folio_str)
    if not m:
        return 'unknown'
    n = int(m.group(1))
    if n <= 66:
        return 'herbal_A'
    elif 67 <= n <= 73:
        return 'astro'
    elif 74 <= n <= 84:
        return 'bio'
    elif 85 <= n <= 102:
        return 'pharma'
    elif 103 <= n <= 116:
        return 'recipes'
    else:
        return 'misc'


def parse_eva_with_context(path):
    """
    Parse ZL3b returning list of (folio, section, currier_lang, locus_cat, word) tuples.
    """
    records = []
    current_folio = 'unknown'
    current_currier = 'unknown'
    current_section = 'unknown'

    with open(path, encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Folio header: <f1r> ... $L=A/B ...
            if re.match(r'^<f\w+>', line) and '<f' in line and '$' in line:
                fmatch = re.match(r'^<(f\w+)>', line)
                if fmatch:
                    current_folio = fmatch.group(1)
                    current_section = classify_section(current_folio)
                lmatch = re.search(r'\$L=([AB])', line)
                if lmatch:
                    current_currier = lmatch.group(1)
                continue
            if line.startswith('#'):
                continue

            # Text line
            m = re.match(r'^<[^>]+,([^>]+)>\s+(.*)', line)
            if not m:
                continue
            locus, text = m.group(1), m.group(2)
            locus_clean = re.sub(r'^[^A-Za-z]+', '', locus)
            cat_char = locus_clean[0].upper() if locus_clean else '?'
            category = LOCUS_CATEGORIES.get(cat_char, 'other')

            # Clean text
            text = re.sub(r'<!.*?>', '', text)
            text = re.sub(r'<[^>]+>', '', text)
            text = text.replace('<%>', '').replace('<$>', '').replace('%', '')
            text = re.sub(r'\[([^:\]]+):[^\]]*\]', r'\1', text)
            text = re.sub(r'\{[^}]*\}', '', text)
            text = re.sub(r'@\d+;?', '', text)
            raw_words = re.split(r'[.\s]+', text)
            for w in raw_words:
                if w and re.match(r'^[a-zA-Z]+$', w):
                    records.append({
                        'folio': current_folio,
                        'section': current_section,
                        'currier': current_currier,
                        'locus': category,
                        'word': w,
                    })

    return records


def shannon_entropy(items):
    c = Counter(items)
    total = sum(c.values())
    if total == 0:
        return 0.0
    return -sum((v/total)*math.log2(v/total) for v in c.values())


if __name__ == "__main__":
    print("Experiment exp_004: daiin Distribution / Section Analysis / H012")
    print("Date: 2026-04-09\n")

    records = parse_eva_with_context(BASE / 'data/transcriptions/eva_zl3b.txt')
    print(f"Total records: {len(records):,}")

    # ── daiin distribution ──
    print("\n" + "="*60)
    print("DAIIN: DISTRIBUTION ACROSS LOCUS CATEGORIES")
    print("="*60)
    by_locus = defaultdict(list)
    for r in records:
        by_locus[r['locus']].append(r['word'])

    for cat, words in sorted(by_locus.items()):
        daiin_count = words.count('daiin')
        total = len(words)
        pct = 100 * daiin_count / max(total, 1)
        print(f"  {cat:12s}: {total:6,} words, daiin={daiin_count:4d} ({pct:.2f}%)")

    # ── daiin by manuscript section ──
    print("\n" + "="*60)
    print("DAIIN: DISTRIBUTION ACROSS MANUSCRIPT SECTIONS (body text only)")
    print("="*60)
    by_section = defaultdict(list)
    for r in records:
        if r['locus'] == 'body':
            by_section[r['section']].append(r['word'])

    for sec, words in sorted(by_section.items()):
        daiin_count = words.count('daiin')
        total = len(words)
        pct = 100 * daiin_count / max(total, 1)
        top = Counter(words).most_common(5)
        print(f"  {sec:15s}: {total:6,} words, daiin={daiin_count:4d} ({pct:.2f}%), top: {[f'{w}({c})' for w,c in top]}")

    # ── daiin by Currier language ──
    print("\n" + "="*60)
    print("DAIIN: DISTRIBUTION ACROSS CURRIER A/B (body text only)")
    print("="*60)
    by_currier = defaultdict(list)
    for r in records:
        if r['locus'] == 'body':
            by_currier[r['currier']].append(r['word'])

    for lang, words in sorted(by_currier.items()):
        daiin_count = words.count('daiin')
        total = len(words)
        pct = 100 * daiin_count / max(total, 1)
        top = Counter(words).most_common(8)
        h2_chars = list(''.join(words))
        h2 = 0.0
        if len(h2_chars) > 2:
            from collections import Counter as C2
            bigrams = [(h2_chars[i], h2_chars[i+1]) for i in range(len(h2_chars)-1)]
            h_bi = shannon_entropy(bigrams)
            h_uni = shannon_entropy(h2_chars)
            h2 = h_bi - h_uni
        print(f"  Currier {lang}: {total:6,} words, daiin={daiin_count:4d} ({pct:.2f}%), h2={h2:.3f}")
        print(f"    Top: {[f'{w}({c})' for w,c in top]}")

    # ── H012: Inner-slot character distribution by Currier ──
    print("\n" + "="*60)
    print("H012: INNER-SLOT CHARS (pos 3-4, words ≥6) BY CURRIER LANGUAGE")
    print("="*60)
    for lang in ['A', 'B']:
        body_words = [r['word'] for r in records if r['locus'] == 'body' and r['currier'] == lang]
        inner = []
        for w in body_words:
            if len(w) >= 6:
                inner.extend(w[3:5])
        h = shannon_entropy(inner)
        freq = Counter(inner)
        total_inner = sum(freq.values())
        print(f"\n  Currier {lang}: H(inner)={h:.4f}, N={total_inner:,}")
        top_inner = [(c, v, 100*v/total_inner) for c, v in freq.most_common(10)]
        for c, cnt, pct in top_inner:
            print(f"    '{c}': {cnt:5d} ({pct:.1f}%)")

    # ── Section-level word distributions ──
    print("\n" + "="*60)
    print("TOP 8 WORDS BY SECTION (body text)")
    print("="*60)
    for sec in ['herbal_A', 'astro', 'bio', 'pharma', 'recipes']:
        words = by_section.get(sec, [])
        if not words:
            continue
        top = Counter(words).most_common(8)
        print(f"  {sec:15s} ({len(words):,} words): {[f'{w}({c})' for w,c in top]}")

    print("\nDone.")
