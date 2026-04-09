"""
exp_046: Per-Folio Label-Body Vocabulary Correlation
H053: Do label words on a folio predict the body word distribution on the same folio?
Tests if labels are folio-specific (naming what's illustrated) vs. formulaic (standard label templates).
"""

import re
import math
from collections import defaultdict, Counter

DATA_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"

# True label loci (from exp_032: Lf/Lz/Ls/Lc/Ln/Lt are clean label loci)
LABEL_LOCI = {'Lf', 'Lz', 'Ls', 'Lc', 'Ln', 'Lt', 'La', 'Lp', 'Lx'}


def is_label_locus(locus_code):
    base = locus_code.lstrip('+*@=/~&')
    return any(base.startswith(lc) for lc in LABEL_LOCI)


def is_body_locus(locus_code):
    base = locus_code.lstrip('+*@=/~&')
    return base.startswith('P')


def parse_folio_label_body(path):
    """Parse per-folio label and body text words."""
    folio_labels = defaultdict(list)
    folio_body = defaultdict(list)
    folio_section = {}
    current_folio = None
    current_section = None

    with open(path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            m_sec = re.search(r'\$I=([A-Z]+)', line)
            if m_sec:
                current_section = m_sec.group(1)

            m2 = re.match(r'^<([^>]+)>', line)
            if not m2:
                continue
            locus_raw = m2.group(1)
            parts = locus_raw.split(',')
            if len(parts) < 2:
                continue
            folio_part = parts[0].strip()
            locus_code = parts[1].strip()

            folio_m = re.match(r'^(f\d+[rv]\d*)', folio_part)
            if folio_m:
                current_folio = folio_m.group(1)
                if current_section and current_folio not in folio_section:
                    folio_section[current_folio] = current_section

            if current_folio is None:
                continue

            text = line[m2.end():].strip()
            text = re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]

            if is_label_locus(locus_code):
                folio_labels[current_folio].extend(tokens)
            elif is_body_locus(locus_code):
                folio_body[current_folio].extend(tokens)

    return folio_labels, folio_body, folio_section


def jaccard(set_a, set_b):
    inter = len(set_a & set_b)
    union = len(set_a | set_b)
    return inter / union if union else 0.0


def expected_jaccard(n_label_types, n_body_types, total_vocab):
    """Expected Jaccard under random sampling."""
    # Simple hypergeometric expectation (approximate)
    # E[|A∩B|] ≈ n_label * n_body / total_vocab (without replacement: n_label * n_body / N)
    # E[|A∪B|] ≈ n_label + n_body - E[|A∩B|]
    exp_inter = n_label_types * n_body_types / max(total_vocab, 1)
    exp_union = n_label_types + n_body_types - exp_inter
    return exp_inter / max(exp_union, 1)


if __name__ == '__main__':
    print("Loading ZL3b corpus...")
    folio_labels, folio_body, folio_section = parse_folio_label_body(DATA_PATH)

    # Find folios with both labels and body text
    folios_with_both = [f for f in folio_labels
                        if len(folio_labels[f]) >= 3 and len(folio_body[f]) >= 30]
    print(f"Folios with ≥3 label tokens AND ≥30 body tokens: {len(folios_with_both)}")

    # Build manuscript-wide vocabulary for null model
    all_words = []
    for words in folio_body.values():
        all_words.extend(words)
    all_words_labels = []
    for words in folio_labels.values():
        all_words_labels.extend(words)
    total_vocab = len(set(all_words) | set(all_words_labels))
    print(f"Total vocabulary size: {total_vocab}")

    # Per-folio Jaccard: label types vs body types
    results = []
    for folio in folios_with_both:
        label_types = set(folio_labels[folio])
        body_types = set(folio_body[folio])
        j_actual = jaccard(label_types, body_types)
        j_expected = expected_jaccard(len(label_types), len(body_types), total_vocab)
        ratio = j_actual / j_expected if j_expected > 0 else 0
        n_shared = len(label_types & body_types)
        section = folio_section.get(folio, '?')
        results.append((folio, section, len(folio_labels[folio]), len(folio_body[folio]),
                        len(label_types), len(body_types), n_shared, j_actual, j_expected, ratio))

    results.sort(key=lambda x: -x[9])  # Sort by ratio

    print(f"\n{'='*70}")
    print(f"PER-FOLIO LABEL-BODY VOCABULARY CORRELATION")
    print(f"{'Folio':<10} {'Sect':>6} {'L-tok':>7} {'B-tok':>7} {'L-typ':>7} "
          f"{'B-typ':>7} {'Shared':>7} {'J_obs':>7} {'J_exp':>7} {'Ratio':>7}")
    print('-' * 70)
    for (folio, section, l_tok, b_tok, l_typ, b_typ, n_shared,
         j_actual, j_expected, ratio) in results[:30]:
        print(f"{folio:<10} {section:>6} {l_tok:>7} {b_tok:>7} {l_typ:>7} "
              f"{b_typ:>7} {n_shared:>7} {j_actual:>7.3f} {j_expected:>7.3f} {ratio:>7.2f}")

    # Section-level summary
    print(f"\n{'='*70}")
    print(f"SECTION-LEVEL SUMMARY")
    from collections import defaultdict as dd
    section_results = dd(list)
    for (folio, section, l_tok, b_tok, l_typ, b_typ, n_shared,
         j_actual, j_expected, ratio) in results:
        section_results[section].append(ratio)

    print(f"\n{'Section':>12} {'N folios':>10} {'Mean ratio':>12} {'Median ratio':>14}")
    for section, ratios in sorted(section_results.items(), key=lambda x: -sum(x[1])/max(len(x[1]),1)):
        if ratios:
            mean = sum(ratios) / len(ratios)
            sorted_r = sorted(ratios)
            mid = len(sorted_r) // 2
            median = sorted_r[mid]
            print(f"{section:>12} {len(ratios):>10} {mean:>12.2f} {median:>14.2f}")

    # Overall statistics
    all_ratios = [r[9] for r in results]
    mean_ratio = sum(all_ratios) / len(all_ratios) if all_ratios else 0
    above1 = sum(1 for r in all_ratios if r > 1.0)
    print(f"\nOverall:")
    print(f"  Mean label-body Jaccard ratio (observed/expected): {mean_ratio:.2f}")
    print(f"  Folios with ratio > 1.0 (label predicts body better than chance): {above1}/{len(all_ratios)}")
    print(f"  Interpretation: ratio > 1 → labels are folio-specific")
    print(f"                  ratio ≈ 1 → labels are formulaic (same across folios)")
    print(f"                  ratio < 1 → labels and body have LESS overlap than expected")

    # Show specific high-overlap folios
    print(f"\nTop 10 folios where label vocab most strongly predicts body vocab:")
    for (folio, section, l_tok, b_tok, l_typ, b_typ, n_shared,
         j_actual, j_expected, ratio) in results[:10]:
        shared_words = set(folio_labels[folio]) & set(folio_body[folio])
        if shared_words:
            print(f"  {folio} ({section}): ratio={ratio:.2f}, "
                  f"shared words: {', '.join(list(shared_words)[:5])}")
