"""
Experiment: exp_016_at_glyph_census
Goal: Manuscript-wide census of all @NNN glyph occurrences in ZL3b.
- Which @glyphs exist, which folios contain them, how many instances
- Cross-reference with Davis scribal hand assignments ($H field)
- Identify @glyphs appearing on multiple folios
- Compute fraction of total manuscript text that is @glyph-marked
Output: data.json with full census; console report
"""

import re
import json
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
CORPUS = BASE / 'data/transcriptions/eva_zl3b.txt'


def parse_all_folios(path):
    """
    Parse full ZL3b for @NNN occurrences across all folios.
    Returns list of {folio, linenum, locus, hand, at_glyph, context} dicts.
    """
    records = []
    current_folio = None
    current_hand = None
    total_chars = 0
    total_words = 0
    folio_headers = {}

    with open(path, encoding='latin-1') as f:
        for raw_line in f:
            line = raw_line.strip()

            # Detect folio header
            m_folio = re.match(r'^<(f\d+[rv](?:\d*)?)>\s*(.*)', line)
            if m_folio:
                current_folio = m_folio.group(1)
                header_rest = m_folio.group(2)
                # Parse $H= field
                h_match = re.search(r'\$H=(\d+)', header_rest)
                current_hand = int(h_match.group(1)) if h_match else None
                folio_headers[current_folio] = {
                    'hand': current_hand,
                    'header': line,
                }
                continue

            if not current_folio:
                continue
            if not line or line.startswith('#'):
                continue

            # Parse a locus line
            m_line = re.match(rf'^<{re.escape(current_folio)}\.(\d+),([^>]+)>\s*(.*)', line)
            if not m_line:
                continue

            linenum = int(m_line.group(1))
            locus_raw = m_line.group(2)
            text = m_line.group(3).strip()

            # Clean text
            clean = text
            clean = re.sub(r'<!.*?>', '', clean)
            clean = re.sub(r'<[^>]+>', '', clean)
            clean = clean.replace('<%>', '').replace('<$>', '').replace('%', '')
            clean = re.sub(r'\[([^:\]]+):[^\]]*\]', r'\1', clean)
            clean = re.sub(r'\{[^}]*\}', '', clean)

            # Count words (for ratio computation)
            words = [w for w in re.split(r'[.\s,]+', clean)
                     if w and re.match(r'^[a-zA-Z@]+', w)]
            total_words += len(words)
            total_chars += sum(len(w) for w in words
                               if not w.startswith('@'))

            # Find @NNN occurrences
            at_matches = list(re.finditer(r'@(\d+);?', clean))
            for match in at_matches:
                glyph_id = int(match.group(1))
                glyph_key = f'@{glyph_id}'
                # Get surrounding context (up to 10 chars each side)
                start = max(0, match.start() - 20)
                end = min(len(clean), match.end() + 20)
                ctx = clean[start:end]

                records.append({
                    'folio': current_folio,
                    'linenum': linenum,
                    'locus': locus_raw,
                    'hand': current_hand,
                    'glyph': glyph_key,
                    'glyph_id': glyph_id,
                    'context': ctx,
                })

    return records, folio_headers, total_words, total_chars


if __name__ == "__main__":
    print("Experiment exp_016: Manuscript-Wide @Glyph Census")
    print("Date: 2026-04-09\n")

    records, folio_headers, total_words, total_chars = parse_all_folios(CORPUS)

    print(f"Total manuscript words: {total_words:,}")
    print(f"Total @glyph occurrences: {len(records)}")
    print(f"@glyph fraction: {100*len(records)/total_words:.3f}% of words\n")

    # Overall frequency
    glyph_freq = Counter(r['glyph'] for r in records)
    print(f"--- Distinct @glyphs ({len(glyph_freq)}) by frequency ---")
    for g, cnt in sorted(glyph_freq.items(), key=lambda x: -x[1]):
        print(f"  {g}: ×{cnt}")

    # Per-folio breakdown
    folio_glyphs = defaultdict(list)
    for r in records:
        folio_glyphs[r['folio']].append(r)

    print(f"\n--- Folios with @glyphs ({len(folio_glyphs)} folios) ---")
    for folio in sorted(folio_glyphs.keys()):
        recs = folio_glyphs[folio]
        hand = recs[0]['hand'] if recs else None
        glyph_list = Counter(r['glyph'] for r in recs)
        print(f"  {folio} (Hand {hand}): {sum(glyph_list.values())} total — "
              f"{dict(sorted(glyph_list.items()))}")

    # @glyphs appearing on multiple folios
    print(f"\n--- @glyphs by folio presence ---")
    glyph_folios = defaultdict(set)
    for r in records:
        glyph_folios[r['glyph']].add(r['folio'])

    multi_folio = {g: fs for g, fs in glyph_folios.items() if len(fs) > 1}
    single_folio = {g: fs for g, fs in glyph_folios.items() if len(fs) == 1}

    print(f"\nMulti-folio @glyphs ({len(multi_folio)}):")
    for g, fs in sorted(multi_folio.items()):
        hands = set()
        for r in records:
            if r['glyph'] == g:
                hands.add(r['hand'])
        print(f"  {g}: {sorted(fs)} (hands: {sorted(h for h in hands if h)})")

    print(f"\nSingle-folio @glyphs ({len(single_folio)}):")
    for g, fs in sorted(single_folio.items()):
        f_only = list(fs)[0]
        hand = folio_headers.get(f_only, {}).get('hand', '?')
        cnt = glyph_freq[g]
        print(f"  {g}: ×{cnt} on {f_only} (Hand {hand})")

    # Hand distribution
    print(f"\n--- @glyph occurrences by scribal hand ---")
    hand_counts = Counter(r['hand'] for r in records)
    total_at = len(records)
    for hand in sorted(hand_counts.keys(), key=lambda x: x or 999):
        cnt = hand_counts[hand]
        glyphs = Counter(r['glyph'] for r in records if r['hand'] == hand)
        print(f"  Hand {hand}: {cnt} @glyphs ({100*cnt/total_at:.1f}%) — "
              f"types: {sorted(glyphs.keys())}")

    # Cluster folios specifically
    cluster_folios = {'f49v', 'f57v', 'f66r', 'f76r'}
    print(f"\n--- Cluster folio @glyph breakdown ---")
    for folio in sorted(cluster_folios):
        recs = folio_glyphs.get(folio, [])
        if recs:
            glyph_list = Counter(r['glyph'] for r in recs)
            hand = recs[0]['hand']
            print(f"  {folio} (Hand {hand}): {dict(sorted(glyph_list.items()))}")
        else:
            hand = folio_headers.get(folio, {}).get('hand', '?')
            print(f"  {folio} (Hand {hand}): NO @glyphs")

    # Save data.json
    output_path = Path(__file__).parent / 'data.json'
    output = {
        'total_words': total_words,
        'total_at_glyph_occurrences': len(records),
        'at_glyph_fraction': len(records) / total_words,
        'glyph_frequency': dict(glyph_freq),
        'folios_with_at_glyphs': len(folio_glyphs),
        'multi_folio_glyphs': {g: sorted(fs) for g, fs in multi_folio.items()},
        'single_folio_glyphs': {g: sorted(fs)[0] for g, fs in single_folio.items()},
        'per_folio': {
            folio: {
                'hand': recs[0]['hand'],
                'total': len(recs),
                'glyphs': dict(Counter(r['glyph'] for r in recs)),
                'records': recs,
            }
            for folio, recs in folio_glyphs.items()
        },
    }
    with open(output_path, 'w') as fout:
        json.dump(output, fout, indent=2)
    print(f"\nSaved data to {output_path}")
    print("\nDone.")
