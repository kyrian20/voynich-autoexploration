"""
exp_048: o-label morpheme vs qo-prefix stem overlap (H042)
Do 'o' (label morpheme) and 'qo' (body-text B prefix) attach to the same stems?
If yes: they are parallel morphemes on a shared stem class.
If no: they select different vocabulary registers.
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

def strip_suffix(word):
    for suf in SUFFIX_LIST:
        if word.endswith(suf) and len(word) > len(suf):
            return word[:-len(suf)]
    return None

def parse_corpus(path):
    label_words = []
    body_b_words = []
    body_a_words = []
    current_currier = None

    with open(path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue

            m_currier = re.search(r'\$L=([AB])', line)
            if m_currier:
                current_currier = m_currier.group(1)

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

            if is_label_locus(locus_code):
                label_words.extend(tokens)
            elif is_body_locus(locus_code):
                if current_currier == 'B':
                    body_b_words.extend(tokens)
                elif current_currier == 'A':
                    body_a_words.extend(tokens)

    return label_words, body_b_words, body_a_words

def main():
    label_words, body_b, body_a = parse_corpus(DATA_PATH)
    print(f"Corpus loaded: {len(label_words)} label words, {len(body_b)} Currier B body, {len(body_a)} Currier A body")

    # === 1. Extract qo-prefix stems from Currier B body ===
    qo_stems = []
    for w in body_b:
        if w.startswith('qo') and len(w) > 2:
            qo_stems.append(w[2:])
    qo_stem_counts = Counter(qo_stems)
    qo_stem_set = set(s for s, c in qo_stem_counts.items() if c >= 2)

    print(f"\nqo-prefix stems (Currier B body): {len(qo_stems)} instances, {len(qo_stem_counts)} unique")
    print(f"qo-stems with freq>=2: {len(qo_stem_set)}")
    print("Top 20 qo-stems:")
    for stem, count in qo_stem_counts.most_common(20):
        print(f"  qo+{stem}: {count}")

    # === 2. Extract o-initial words from labels ===
    o_labels = [w for w in label_words if w.startswith('o') and len(w) >= 3]
    o_stems_raw = [w[1:] for w in o_labels]
    o_stem_counts = Counter(o_stems_raw)
    o_stem_set = set(s for s, c in o_stem_counts.items() if c >= 2)

    print(f"\no-initial label words: {len(o_labels)} instances, {len(o_stem_counts)} unique o-stems")
    print(f"o-stems with freq>=2: {len(o_stem_set)}")
    print("Top 20 o-stems (after stripping 'o'):")
    for stem, count in o_stem_counts.most_common(20):
        print(f"  o+{stem}: {count}")

    # === 3. Exact stem overlap ===
    overlap_exact = qo_stem_set & o_stem_set
    union_exact = qo_stem_set | o_stem_set
    jaccard_exact = len(overlap_exact) / len(union_exact) if union_exact else 0.0

    print(f"\n=== EXACT STEM OVERLAP (qo+X in body B vs o+X in labels) ===")
    print(f"qo-stem set (freq>=2): {len(qo_stem_set)}")
    print(f"o-stem set (freq>=2): {len(o_stem_set)}")
    print(f"Exact overlap: {len(overlap_exact)}")
    print(f"Jaccard: {jaccard_exact:.3f}")
    if overlap_exact:
        print("Shared stems:")
        for stem in sorted(overlap_exact, key=lambda s: -qo_stem_counts[s]):
            print(f"  '{stem}': qo+stem={qo_stem_counts[stem]}, o+stem={o_stem_counts[stem]}")

    # === 4. Root-level overlap (strip suffix from both) ===
    def to_root(stem):
        root = strip_suffix(stem)
        return root if root else stem

    o_roots = Counter()
    for w in o_labels:
        stem = w[1:]
        root = to_root(stem)
        if len(root) >= 2:
            o_roots[root] += 1

    qo_roots = Counter()
    for w in body_b:
        if w.startswith('qo') and len(w) > 2:
            stem = w[2:]
            root = to_root(stem)
            if len(root) >= 2:
                qo_roots[root] += 1

    o_root_set = set(r for r, c in o_roots.items() if c >= 2)
    qo_root_set = set(r for r, c in qo_roots.items() if c >= 2)
    root_overlap = o_root_set & qo_root_set
    root_union = o_root_set | qo_root_set
    root_jaccard = len(root_overlap) / len(root_union) if root_union else 0.0

    print(f"\n=== ROOT-LEVEL OVERLAP (after suffix stripping) ===")
    print(f"o-label roots (freq>=2): {len(o_root_set)}")
    print(f"qo-body roots (freq>=2): {len(qo_root_set)}")
    print(f"Root overlap: {len(root_overlap)}")
    print(f"Root Jaccard: {root_jaccard:.3f}")
    print("Top shared roots:")
    for root in sorted(root_overlap, key=lambda r: -(o_roots[r] + qo_roots[r]))[:15]:
        print(f"  '{root}': o-labels={o_roots[root]}, qo-body={qo_roots[root]}")

    # === 5. o-stem in free B body vocab ===
    body_b_vocab = Counter(body_b)
    body_b_types = set(body_b_vocab.keys())

    o_stems_in_body = {s for s in o_stem_counts if s in body_b_types}
    qo_stems_in_body = {s for s in qo_stem_counts if s in body_b_types}

    print(f"\n=== STEM vs FREE CURRIER B VOCABULARY ===")
    print(f"o-stems in free B body: {len(o_stems_in_body)}/{len(o_stem_counts)} ({100*len(o_stems_in_body)/max(1,len(o_stem_counts)):.1f}%)")
    print(f"qo-stems in free B body: {len(qo_stems_in_body)}/{len(qo_stem_counts)} ({100*len(qo_stems_in_body)/max(1,len(qo_stem_counts)):.1f}%)")

    print("\nTop o-stems present as free words in Currier B body:")
    for stem in sorted(o_stems_in_body, key=lambda s: -body_b_vocab.get(s, 0))[:15]:
        print(f"  '{stem}': o+{o_stem_counts[stem]} labels, free={body_b_vocab.get(stem,0)}")

    # === 6. Onset character analysis ===
    print(f"\n=== ONSET ANALYSIS ===")
    # Second char after 'o' in o-initial labels
    o_second = Counter()
    for w in o_labels:
        if len(w) >= 2:
            o_second[w[1]] += 1
    print("Second char after 'o' in o-initial labels:")
    for char, cnt in o_second.most_common(10):
        pct = 100 * cnt / len(o_labels)
        print(f"  o{char}...: {cnt} ({pct:.1f}%)")

    # Third char after 'q' in qo- words in body B (= first char of stem)
    qo_third = Counter()
    for w in body_b:
        if w.startswith('qo') and len(w) >= 3:
            qo_third[w[2]] += 1
    print("\nFirst char of qo-stem in Currier B body:")
    for char, cnt in qo_third.most_common(10):
        pct = 100 * cnt / sum(qo_third.values())
        print(f"  qo+{char}...: {cnt} ({pct:.1f}%)")

    # === 7. Are qo-words absent from labels? ===
    qo_in_labels = [w for w in label_words if w.startswith('qo')]
    print(f"\n=== qo-WORDS IN LABELS ===")
    print(f"qo-initial words in label corpus: {len(qo_in_labels)}")
    if qo_in_labels:
        print("Examples:", Counter(qo_in_labels).most_common(10))

    # === Summary ===
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"qo-stems (body B, freq>=2): {len(qo_stem_set)}")
    print(f"o-stems (labels, freq>=2): {len(o_stem_set)}")
    print(f"Exact stem overlap: {len(overlap_exact)} ({jaccard_exact:.3f} Jaccard)")
    print(f"Root overlap (suffix-stripped): {len(root_overlap)} ({root_jaccard:.3f} Jaccard)")
    print(f"o-stems in free B vocab: {len(o_stems_in_body)}/{len(o_stem_counts)} ({100*len(o_stems_in_body)/max(1,len(o_stem_counts)):.1f}%)")
    print(f"qo-stems in free B vocab: {len(qo_stems_in_body)}/{len(qo_stem_counts)} ({100*len(qo_stems_in_body)/max(1,len(qo_stem_counts)):.1f}%)")
    print(f"qo-words appearing in labels: {len(qo_in_labels)}")

if __name__ == '__main__':
    main()
