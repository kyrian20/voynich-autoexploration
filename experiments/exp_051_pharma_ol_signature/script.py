"""
exp_051: Pharma Section -ol Signature Analysis (H057)
The pharma section has the highest -ol rate of any section (18.5%).
Is this driven by a small set of frequent words, or distributed across stems?
Do pharma LABELS also prefer -ol endings?
What stems carry the pharma -ol signal?
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

LABEL_LOCI = {'Lf', 'Ls', 'Lz', 'Lc', 'Ln', 'Lt', 'La', 'Lp', 'Lx'}
SUFFIX_LIST = ['aiin', 'ain', 'eedy', 'edy', 'chy', 'eey', 'dy', 'ey', 'y', 'ol', 'or', 'al', 'ar', 'iin', 'in']

def is_label_locus(locus_code):
    base = locus_code.lstrip('+*@=/~&')
    return any(base.startswith(lc) for lc in LABEL_LOCI)

def is_body_locus(locus_code):
    base = locus_code.lstrip('+*@=/~&')
    return base.startswith('P')

def clean_text(text):
    text = re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)
    return text

def suffix_group(word):
    for suf in SUFFIX_LIST:
        if word.endswith(suf) and len(word) > len(suf):
            return suf
    return None

def strip_suffix(word):
    for suf in SUFFIX_LIST:
        if word.endswith(suf) and len(word) > len(suf):
            return word[:-len(suf)], suf
    return word, None

def parse_corpus(path):
    """Parse by section. Returns dict: section -> {'body': [words], 'labels': [words]}."""
    sections = defaultdict(lambda: {'body': [], 'labels': []})
    current_section = None

    with open(path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue

            m_sec = re.search(r'\$I=([A-Z]+)', line)
            if m_sec:
                current_section = m_sec.group(1)

            m = re.match(r'^<([^>]+)>', line)
            if not m:
                continue
            locus_raw = m.group(1)
            parts = locus_raw.split(',')
            if len(parts) < 2:
                continue
            locus_code = parts[1].strip()

            text = line[m.end():].strip()
            text = clean_text(text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]

            if not tokens or current_section is None:
                continue

            if is_label_locus(locus_code):
                sections[current_section]['labels'].extend(tokens)
            elif is_body_locus(locus_code):
                sections[current_section]['body'].extend(tokens)

    return sections

def suffix_rates(words, target_suffix):
    """Fraction of words that end with target_suffix."""
    if not words:
        return 0.0
    return sum(1 for w in words if w.endswith(target_suffix)) / len(words)

def full_suffix_distribution(words):
    """Return distribution over suffix groups."""
    counts = Counter()
    for w in words:
        sg = suffix_group(w)
        if sg:
            counts[sg] += 1
        else:
            counts['(none)'] += 1
    total = sum(counts.values())
    return {k: v/total for k, v in counts.items()}, total

def main():
    sections = parse_corpus(DATA_PATH)
    print("Section sizes:")
    for sec in sorted(sections.keys()):
        print(f"  {sec}: {len(sections[sec]['body'])} body, {len(sections[sec]['labels'])} labels")

    # Focus on pharma section
    pharma_body = sections.get('P', {}).get('body', [])
    herbal_body = sections.get('H', {}).get('body', [])
    bio_body = sections.get('B', {}).get('body', [])
    astro_body = sections.get('A', {}).get('body', [])

    pharma_labels = sections.get('P', {}).get('labels', [])
    herbal_labels = sections.get('H', {}).get('labels', [])

    print(f"\nPharma body: {len(pharma_body)} tokens")
    print(f"Pharma labels: {len(pharma_labels)} tokens")

    # === 1. -ol rate comparison by section ===
    print(f"\n{'='*60}")
    print("-ol AND -or SUFFIX RATES BY SECTION (body text)")
    print(f"{'='*60}")
    print(f"{'Section':<10} {'N':>8} {'-ol rate':>10} {'-or rate':>10} {'-ol+or':>10}")
    for sec in ['P', 'H', 'B', 'A', 'S', 'C', 'T']:
        body = sections.get(sec, {}).get('body', [])
        if not body:
            continue
        ol_rate = suffix_rates(body, 'ol')
        or_rate = suffix_rates(body, 'or')
        print(f"{sec:<10} {len(body):>8} {100*ol_rate:>9.1f}% {100*or_rate:>9.1f}% {100*(ol_rate+or_rate):>9.1f}%")

    # === 2. What -ol words appear in pharma body? ===
    print(f"\n{'='*60}")
    print("TOP -ol WORDS IN PHARMA BODY (with stem analysis)")
    print(f"{'='*60}")
    pharma_ol = [w for w in pharma_body if w.endswith('ol')]
    pharma_ol_counts = Counter(pharma_ol)
    print(f"Total -ol tokens in pharma body: {len(pharma_ol)} ({100*len(pharma_ol)/max(1,len(pharma_body)):.1f}%)")
    print(f"Unique -ol types in pharma: {len(pharma_ol_counts)}")

    # Same for herbal
    herbal_ol = [w for w in herbal_body if w.endswith('ol')]
    herbal_ol_counts = Counter(herbal_ol)

    print(f"\nTop 20 pharma -ol words:")
    for w, c in pharma_ol_counts.most_common(20):
        stem, suf = strip_suffix(w)
        herbal_rate = herbal_ol_counts.get(w, 0) / max(1, len(herbal_body))
        pharma_rate = c / max(1, len(pharma_body))
        print(f"  {w:<15} (stem='{stem}'): pharma={c} ({100*pharma_rate:.2f}%), herbal={100*herbal_rate:.3f}%")

    # === 3. Is pharma -ol driven by a few words or distributed? ===
    print(f"\n{'='*60}")
    print("CONCENTRATION ANALYSIS: Is pharma -ol driven by a few words?")
    print(f"{'='*60}")
    top5_ol = sum(c for w, c in pharma_ol_counts.most_common(5))
    top10_ol = sum(c for w, c in pharma_ol_counts.most_common(10))
    print(f"Top-5 -ol words account for: {100*top5_ol/max(1,len(pharma_ol)):.1f}% of pharma -ol tokens")
    print(f"Top-10 -ol words account for: {100*top10_ol/max(1,len(pharma_ol)):.1f}% of pharma -ol tokens")
    print(f"Number of -ol types: {len(pharma_ol_counts)} (types; high = distributed)")

    # Compare with herbal -ol concentration
    top5_h = sum(c for w, c in herbal_ol_counts.most_common(5))
    print(f"\nHerbal: top-5 -ol words = {100*top5_h/max(1,len(herbal_ol)):.1f}% of herbal -ol tokens")
    print(f"Herbal: {len(herbal_ol_counts)} unique -ol types")

    # === 4. Are pharma LABELS also -ol elevated? ===
    print(f"\n{'='*60}")
    print("PHARMA LABELS: Suffix distribution")
    print(f"{'='*60}")
    if pharma_labels:
        pharma_label_dist, pharma_label_n = full_suffix_distribution(pharma_labels)
        herbal_label_dist, herbal_label_n = full_suffix_distribution(herbal_labels) if herbal_labels else ({}, 0)

        print(f"Pharma labels n={pharma_label_n}")
        print(f"{'Suffix':<10} {'Pharma labels':>15} {'Pharma body':>14} {'Herbal labels':>15} {'Herbal body':>13}")
        for suf in ['-ol', '-or', '-al', '-ar', '-y', '-ey', '-edy', '-chy', '-aiin', '-ain', '(none)']:
            suf_key = suf.lstrip('-')
            pharma_lab_rate = pharma_label_dist.get(suf_key, 0.0)
            pharma_body_rate = suffix_rates(pharma_body, suf_key) if suf_key != '(none)' else 0.0
            herbal_lab_rate = herbal_label_dist.get(suf_key, 0.0) if herbal_label_dist else 0.0
            herbal_body_rate = suffix_rates(herbal_body, suf_key) if suf_key != '(none)' else 0.0
            print(f"{suf:<10} {100*pharma_lab_rate:>14.1f}% {100*pharma_body_rate:>13.1f}% {100*herbal_lab_rate:>14.1f}% {100*herbal_body_rate:>12.1f}%")

    # === 5. Stem diversity: how many different stems take -ol in pharma? ===
    print(f"\n{'='*60}")
    print("STEM DIVERSITY: Which stems drive pharma -ol?")
    print(f"{'='*60}")
    pharma_ol_stems = Counter()
    for w in pharma_ol:
        stem, _ = strip_suffix(w)
        pharma_ol_stems[stem] += 1

    herbal_ol_stems = Counter()
    for w in herbal_ol:
        stem, _ = strip_suffix(w)
        herbal_ol_stems[stem] += 1

    print(f"Pharma -ol unique stems: {len(pharma_ol_stems)}")
    print(f"Herbal -ol unique stems: {len(herbal_ol_stems)}")
    print(f"\nTop pharma -ol stems (vs herbal):")
    for stem, c in pharma_ol_stems.most_common(15):
        h_c = herbal_ol_stems.get(stem, 0)
        print(f"  stem='{stem}': pharma={c}, herbal={h_c}")

    # === 6. Pharma-specific -ol words (high in pharma, rare in herbal) ===
    print(f"\n{'='*60}")
    print("PHARMA-SPECIFIC -ol WORDS (enriched in pharma vs herbal)")
    print(f"{'='*60}")
    pharma_enriched = []
    for w, pc in pharma_ol_counts.items():
        p_rate = pc / max(1, len(pharma_body))
        h_rate = herbal_ol_counts.get(w, 0) / max(1, len(herbal_body))
        if p_rate > 0 and (h_rate == 0 or p_rate / h_rate > 3):
            pharma_enriched.append((w, pc, p_rate, h_rate, p_rate / max(h_rate, 1e-6)))

    pharma_enriched.sort(key=lambda x: -x[2])
    print(f"{'Word':<15} {'Pharma n':>8} {'Pharma%':>9} {'Herbal%':>9} {'Ratio':>7}")
    for w, pc, p_rate, h_rate, ratio in pharma_enriched[:20]:
        print(f"{w:<15} {pc:>8} {100*p_rate:>8.2f}% {100*h_rate:>8.3f}% {ratio:>6.1f}×")

if __name__ == '__main__':
    main()
