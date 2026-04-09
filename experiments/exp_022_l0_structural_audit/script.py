"""
Experiment: exp_022_l0_structural_audit
Hypothesis: H021
Goal: Classify all ZL3b L0 locus entries into structural types:
  Type 1 (TRUE_LABEL): standalone L0 entry not adjacent to P0 (object label)
  Type 2 (LINE_MARKER): L0 entry immediately preceding a P0 entry (margin marker)
  Type 3 (LIST_ENTRY): multiple consecutive L0 entries without P0 (list/table)
Also: identify any other folios with line-marker or list structures not yet known.
"""

import re
import json
from pathlib import Path
from collections import Counter, defaultdict

BASE = Path(__file__).resolve().parents[2]
CORPUS = BASE / 'data/transcriptions/eva_zl3b.txt'


def parse_l0_lines(path):
    """Parse all L0 locus entries with their folio, line number, content, and
    the locus of the immediately following line."""
    entries = []
    lines_by_folio = defaultdict(list)

    with open(path, encoding='latin-1') as f:
        all_lines = [l.strip() for l in f if l.strip()]

    # Parse each line
    parsed = []
    for raw in all_lines:
        m = re.match(r'^<(f\d+[rv]\d*)\.([\d]+),([^>]+)>\s*(.*)', raw)
        if m:
            folio = m.group(1)
            linenum = int(m.group(2))
            locus = m.group(3)
            text = m.group(4)
            parsed.append({
                'folio': folio,
                'linenum': linenum,
                'locus': locus,
                'text': text,
                'raw': raw,
            })

    # Find L0 entries and classify by context
    for i, entry in enumerate(parsed):
        # Match any prefixed L0 locus: L0, +L0, *L0, @L0, =L0, /L0, ~L0, &L0, etc.
        if not re.match(r'^[+*@=/~&]?L0$', entry['locus']):
            continue

        folio = entry['folio']
        linenum = entry['linenum']

        # Look at surrounding entries on same folio
        prev_entry = parsed[i-1] if i > 0 and parsed[i-1]['folio'] == folio else None
        next_entry = parsed[i+1] if i < len(parsed)-1 and parsed[i+1]['folio'] == folio else None

        prev_locus = prev_entry['locus'] if prev_entry else None
        next_locus = next_entry['locus'] if next_entry else None

        def is_p0(locus):
            return locus is not None and re.match(r'^[+*@=/~&]?P0$', locus) is not None

        def is_l0(locus):
            return locus is not None and re.match(r'^[+*@=/~&]?L0$', locus) is not None

        # Classification
        # Type 2 (LINE_MARKER): this L0 is immediately followed by a P0 on same folio
        if is_p0(next_locus):
            classification = 'LINE_MARKER'
        # Type 3 (LIST_ENTRY): adjacent to other L0 entries (not between L0 and P0 on either side)
        elif is_l0(prev_locus) or is_l0(next_locus):
            classification = 'LIST_ENTRY'
        # Type 1 (TRUE_LABEL): standalone
        else:
            classification = 'TRUE_LABEL'

        # Extract token content (strip metadata)
        text = re.sub(r'<!.*?>', '', entry['text'])
        text = re.sub(r'<[^>]+>', '', text)
        text = text.strip()
        tokens = [t for t in text.replace(' ', '.').split('.') if t]

        entries.append({
            'folio': folio,
            'linenum': linenum,
            'locus': entry['locus'],
            'classification': classification,
            'text': text,
            'tokens': tokens,
            'prev_locus': prev_locus,
            'next_locus': next_locus,
            'raw': entry['raw'][:120],
        })

    return entries, parsed


def get_section(folio):
    """Map folio to manuscript section (approximate)."""
    # Folio ranges per standard Voynich section assignments
    fnum = int(re.sub(r'[rv].*', '', folio[1:]))
    side = 'r' if 'r' in folio else 'v'

    if fnum <= 25:
        return 'herbal_A'
    elif fnum <= 57:
        if fnum in (33, 34, 35, 36, 37, 38, 39, 40):
            return 'herbal_B'
        elif fnum in (41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57):
            return 'astro'
        else:
            return 'herbal_B'
    elif fnum <= 66:
        return 'astro'
    elif fnum <= 73:
        return 'cosmo'
    elif fnum <= 84:
        return 'bio'
    elif fnum <= 102:
        return 'pharma'
    else:
        return 'recipes'


if __name__ == "__main__":
    print("Experiment exp_022: ZL3b L0 Structural Audit")
    print("Hypothesis: H021")
    print("Date: 2026-04-09\n")

    entries, parsed = parse_l0_lines(CORPUS)

    print(f"Total L0 entries found: {len(entries)}")

    # Overall classification breakdown
    by_class = Counter(e['classification'] for e in entries)
    print(f"\n=== Classification Breakdown ===")
    for cls, cnt in by_class.most_common():
        pct = 100 * cnt / len(entries)
        print(f"  {cls}: {cnt} ({pct:.1f}%)")

    # Per-folio breakdown — identify all folios with line markers or list entries
    print(f"\n=== Folios by Classification ===")
    folio_counts = defaultdict(Counter)
    for e in entries:
        folio_counts[e['folio']][e['classification']] += 1

    # Show folios with LINE_MARKER or LIST_ENTRY
    marker_folios = {f: c for f, c in folio_counts.items()
                     if c.get('LINE_MARKER', 0) + c.get('LIST_ENTRY', 0) > 0}

    print(f"\nFolios with LINE_MARKER or LIST_ENTRY entries ({len(marker_folios)} folios):")
    for folio in sorted(marker_folios.keys()):
        c = folio_counts[folio]
        section = get_section(folio)
        print(f"  {folio} ({section}): LINE_MARKER={c.get('LINE_MARKER',0)}, "
              f"LIST_ENTRY={c.get('LIST_ENTRY',0)}, TRUE_LABEL={c.get('TRUE_LABEL',0)}")

    # Detailed look at LINE_MARKER folios (sorted by count)
    print(f"\n=== Detailed LINE_MARKER Folios ===")
    line_marker_folios = {f: c for f, c in folio_counts.items()
                          if c.get('LINE_MARKER', 0) > 0}
    for folio in sorted(line_marker_folios.keys(), key=lambda f: -folio_counts[f].get('LINE_MARKER', 0)):
        c = folio_counts[folio]
        markers = [e for e in entries if e['folio'] == folio and e['classification'] == 'LINE_MARKER']
        section = get_section(folio)
        print(f"\n  {folio} ({section}) — {c.get('LINE_MARKER',0)} LINE_MARKERs:")
        for m in markers[:10]:  # first 10
            print(f"    L{m['linenum']}: '{m['text']}' | next={m['next_locus']}")

    # Detailed look at LIST_ENTRY folios
    print(f"\n=== Detailed LIST_ENTRY Folios ===")
    list_folios = {f: c for f, c in folio_counts.items()
                   if c.get('LIST_ENTRY', 0) > 0}
    for folio in sorted(list_folios.keys(), key=lambda f: -folio_counts[f].get('LIST_ENTRY', 0)):
        c = folio_counts[folio]
        lists = [e for e in entries if e['folio'] == folio and e['classification'] == 'LIST_ENTRY']
        section = get_section(folio)
        print(f"\n  {folio} ({section}) — {c.get('LIST_ENTRY',0)} LIST_ENTRYs:")
        for le in lists[:10]:
            print(f"    L{le['linenum']}: '{le['text']}'")

    # Section-level analysis of TRUE_LABEL entries
    print(f"\n=== TRUE_LABEL Entries by Section ===")
    true_labels = [e for e in entries if e['classification'] == 'TRUE_LABEL']
    by_section = Counter(get_section(e['folio']) for e in true_labels)
    for sec, cnt in by_section.most_common():
        print(f"  {sec}: {cnt}")

    # Token analysis for TRUE_LABEL
    print(f"\n=== TRUE_LABEL Token Frequency ===")
    label_tokens = []
    for e in true_labels:
        label_tokens.extend(e['tokens'])
    label_token_freq = Counter(label_tokens)
    print(f"  Total TRUE_LABEL tokens: {len(label_tokens)}")
    print(f"  Unique types: {len(label_token_freq)}")
    print(f"  TTR: {len(label_token_freq)/len(label_tokens):.3f}" if label_tokens else "  No tokens")
    print(f"  Top 20 tokens:")
    for tok, cnt in label_token_freq.most_common(20):
        print(f"    '{tok}': {cnt}")

    # Specifically check herbal_A TRUE_LABELS after removing f49v and f66r
    herbal_a_labels = [e for e in true_labels
                       if get_section(e['folio']) == 'herbal_A'
                       and e['folio'] not in ('f49v', 'f66r')]
    print(f"\n  Herbal A TRUE_LABELs (excl. f49v/f66r): {len(herbal_a_labels)}")
    for e in herbal_a_labels:
        print(f"    {e['folio']}: '{e['text']}'")

    # Previously known special folios — verify our prior findings
    print(f"\n=== Verification of Known Cases ===")
    f49v_entries = [e for e in entries if e['folio'] == 'f49v']
    f66r_entries = [e for e in entries if e['folio'] == 'f66r']
    f76r_entries = [e for e in entries if e['folio'] == 'f76r']
    print(f"  f49v: total={len(f49v_entries)}, "
          f"LINE_MARKER={sum(1 for e in f49v_entries if e['classification']=='LINE_MARKER')}, "
          f"LIST_ENTRY={sum(1 for e in f49v_entries if e['classification']=='LIST_ENTRY')}, "
          f"TRUE_LABEL={sum(1 for e in f49v_entries if e['classification']=='TRUE_LABEL')}")
    print(f"  f66r: total={len(f66r_entries)}, "
          f"LINE_MARKER={sum(1 for e in f66r_entries if e['classification']=='LINE_MARKER')}, "
          f"LIST_ENTRY={sum(1 for e in f66r_entries if e['classification']=='LIST_ENTRY')}, "
          f"TRUE_LABEL={sum(1 for e in f66r_entries if e['classification']=='TRUE_LABEL')}")
    print(f"  f76r: total={len(f76r_entries)}, "
          f"LINE_MARKER={sum(1 for e in f76r_entries if e['classification']=='LINE_MARKER')}, "
          f"LIST_ENTRY={sum(1 for e in f76r_entries if e['classification']=='LIST_ENTRY')}, "
          f"TRUE_LABEL={sum(1 for e in f76r_entries if e['classification']=='TRUE_LABEL')}")

    # Save results
    output = {
        'total_l0': len(entries),
        'by_class': dict(by_class),
        'marker_folios': {f: dict(c) for f, c in marker_folios.items()},
        'true_label_count': len(true_labels),
        'true_label_by_section': dict(by_section),
        'true_label_top20_tokens': label_token_freq.most_common(20),
        'herbal_a_true_labels_excl_f49v_f66r': len(herbal_a_labels),
        'all_entries': entries,  # full record for downstream analysis
    }

    out_path = Path(__file__).parent / 'data.json'
    # Omit 'all_entries' from JSON (too large) — save summary
    output_slim = {k: v for k, v in output.items() if k != 'all_entries'}
    with open(out_path, 'w') as f:
        json.dump(output_slim, f, indent=2)
    print(f"\nSaved summary to {out_path}")
    print("Done.")
