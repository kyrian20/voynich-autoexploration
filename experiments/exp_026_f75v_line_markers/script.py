"""
Experiment: exp_026_f75v_line_markers
Goal: Characterize f75v's line-marker sequence and compare to f49v and f76r.

Key prior finding (exp_022): f75v has 5+ L0 line markers. Hand 2, Currier B, biological.
ZL3b note: "last character in first 5 lines aligned vertically reading slors"
f76r is ALSO Hand 2, Currier B, biological — same scribe!

Questions:
1. What is the complete marker sequence on f75v?
2. Is f75v's sequence related to f76r's sequence (same hand)?
3. What are marker-to-body correspondences?
4. What is the ZL3b metadata for f75v vs f75r vs f76r?
"""

import re
import json
from pathlib import Path
from collections import Counter

BASE = Path(__file__).resolve().parents[2]
CORPUS = BASE / 'data/transcriptions/eva_zl3b.txt'


def extract_folio_full(path, folio_str):
    """Extract all lines from a folio including the header."""
    header = None
    lines = []
    comments = []
    in_folio = False

    with open(path, encoding='latin-1') as f:
        for raw in f:
            s = raw.strip()
            if not s:
                continue
            if re.match(rf'^<{re.escape(folio_str)}>', s) and '$' in s:
                header = s
                in_folio = True
                continue
            if in_folio:
                if re.match(r'^<f\d+', s) and f'<{folio_str}.' not in s:
                    break
                if s.startswith('#'):
                    comments.append(s)
                else:
                    lines.append(s)
    return header, comments, lines


def is_l0(locus):
    return locus is not None and re.match(r'^[+*@=/~&]?L0$', locus) is not None

def is_p0(locus):
    return locus is not None and re.match(r'^[+*@=/~&]?P\d', locus) is not None


def parse_lines(folio_lines):
    """Parse folio lines into structured entries."""
    parsed = []
    for raw in folio_lines:
        m = re.match(r'^<[^.]+\.(\d+),([^>]+)>\s*(.*)', raw)
        if m:
            linenum = int(m.group(1))
            locus = m.group(2)
            text = m.group(3)
            text_clean = re.sub(r'<!.*?>', '', text)
            text_clean = re.sub(r'<[^>]+>', '', text_clean)
            text_clean = re.sub(r'\{[^}]*\}', '', text_clean)
            text_clean = text_clean.strip()
            parsed.append({
                'linenum': linenum,
                'locus': locus,
                'text': text_clean,
                'raw': raw[:120]
            })
    return parsed


def find_marker_pairs(parsed):
    """Find L0/P0 pairs (line marker → body text)."""
    pairs = []
    for i, entry in enumerate(parsed):
        if is_l0(entry['locus']):
            # Find the immediately following P0
            next_p0 = None
            for j in range(i+1, min(i+3, len(parsed))):
                if is_p0(parsed[j]['locus']):
                    next_p0 = parsed[j]
                    break
            pairs.append({
                'marker_line': entry['linenum'],
                'marker_text': entry['text'],
                'marker_locus': entry['locus'],
                'body_line': next_p0['linenum'] if next_p0 else None,
                'body_text': next_p0['text'] if next_p0 else None,
                'body_first_char': next_p0['text'][0].lower() if next_p0 and next_p0['text'] else None,
            })
    return pairs


def corpus_char_freq(path):
    """Get corpus-wide character frequency at word position 0."""
    word_initials = Counter()
    with open(path, encoding='latin-1') as f:
        for line in f:
            m = re.match(r'^<[^>]+,[^>]*P\d>\s*(.*)', line.strip())
            if not m:
                continue
            text = re.sub(r'<!.*?>', '', m.group(1))
            text = re.sub(r'\{[^}]*\}', '', text)
            for word in re.split(r'[.\s,]+', text):
                word = re.sub(r'\[[^\]]+\]', 'X', word).strip()
                if word and re.match(r'^[a-z]', word):
                    word_initials[word[0]] += 1
    total = sum(word_initials.values())
    return {ch: cnt/total for ch, cnt in word_initials.items()}


if __name__ == "__main__":
    print("Experiment exp_026: f75v Line Marker Analysis")
    print("Date: 2026-04-09\n")

    # Extract f75v, f76r, f49v
    folios = ['f75v', 'f76r', 'f49v']
    folio_data = {}
    for folio in folios:
        header, comments, lines = extract_folio_full(CORPUS, folio)
        parsed = parse_lines(lines)
        pairs = find_marker_pairs(parsed)
        folio_data[folio] = {
            'header': header, 'comments': comments,
            'parsed': parsed, 'pairs': pairs
        }

    # Print f75v details
    print(f"=== f75v Header and Metadata ===")
    print(f"  Header: {folio_data['f75v']['header']}")
    print(f"  ZL3b comments:")
    for c in folio_data['f75v']['comments']:
        print(f"    {c}")

    print(f"\n=== f75v All Lines (first 20) ===")
    for entry in folio_data['f75v']['parsed'][:20]:
        marker = "← MARKER" if is_l0(entry['locus']) else ""
        print(f"  L{entry['linenum']:02d} [{entry['locus']:5s}]: '{entry['text'][:60]}' {marker}")

    print(f"\n=== f75v Marker Sequence ===")
    f75v_pairs = folio_data['f75v']['pairs']
    print(f"  Total L0 entries: {len(f75v_pairs)}")
    print(f"  Marker sequence: {[p['marker_text'] for p in f75v_pairs]}")
    for p in f75v_pairs:
        bc = p['body_first_char'] or '?'
        print(f"  Marker '{p['marker_text']}' (L{p['marker_line']}) → body L{p['body_line']}: first_char='{bc}' | "
              f"'{(p['body_text'] or '')[:40]}'")

    # Compare with f76r
    print(f"\n=== f76r Marker Sequence (same hand) ===")
    f76r_pairs = folio_data['f76r']['pairs']
    print(f"  Total: {len(f76r_pairs)}")
    print(f"  Marker sequence: {[p['marker_text'] for p in f76r_pairs]}")

    # Compare with f49v
    print(f"\n=== f49v Marker Sequence (different hand) ===")
    f49v_pairs = folio_data['f49v']['pairs']
    print(f"  Total: {len(f49v_pairs)}")
    print(f"  Marker sequence (first 15): {[p['marker_text'] for p in f49v_pairs[:15]]}")

    # Character set overlap
    f75v_seq = [p['marker_text'] for p in f75v_pairs]
    f76r_seq = [p['marker_text'] for p in f76r_pairs]
    f49v_seq = [p['marker_text'] for p in f49v_pairs]

    print(f"\n=== Sequence Analysis ===")
    print(f"  f75v chars: {sorted(set(f75v_seq))}")
    print(f"  f76r chars: {sorted(set(f76r_seq))}")
    print(f"  f49v chars: {sorted(set(f49v_seq))}")

    shared_75_76 = set(f75v_seq) & set(f76r_seq)
    shared_75_49 = set(f75v_seq) & set(f49v_seq)
    shared_all = set(f75v_seq) & set(f76r_seq) & set(f49v_seq)
    print(f"  f75v ∩ f76r: {sorted(shared_75_76)}")
    print(f"  f75v ∩ f49v: {sorted(shared_75_49)}")
    print(f"  All three share: {sorted(shared_all)}")

    # Is f75v a subsequence/subset of f76r?
    f75v_set = set(f75v_seq)
    f76r_set = set(f76r_seq)
    print(f"  f75v char set ⊆ f76r char set? {f75v_set.issubset(f76r_set)}")
    print(f"  Chars in f75v but not f76r: {f75v_set - f76r_set}")
    print(f"  Chars in f76r but not f75v: {f76r_set - f75v_set}")

    # Body text correspondence test
    print(f"\n=== Body Text First-Char Correspondence (f75v) ===")
    matches = sum(1 for p in f75v_pairs
                  if p['marker_text'] and p['body_first_char']
                  and p['marker_text'][0] == p['body_first_char'])
    total = sum(1 for p in f75v_pairs if p['marker_text'] and p['body_first_char'])
    print(f"  Marker == body first char: {matches}/{total} = {100*matches/total:.1f}%")

    # Corpus rate for body first char = marker char
    char_freq = corpus_char_freq(CORPUS)
    expected = sum(char_freq.get(p['marker_text'][0], 0)
                   for p in f75v_pairs if p['marker_text'] and p['body_first_char'])
    print(f"  Expected by chance (corpus rate): {100*expected/total:.1f}%")

    # f75v metadata
    header_str = folio_data['f75v']['header'] or ''
    hand_m = re.search(r'\$H=(\d)', header_str)
    lang_m = re.search(r'\$L=([AB])', header_str)
    section_m = re.search(r'\$I=([A-Z])', header_str)
    print(f"\n=== f75v Metadata ===")
    print(f"  Hand: {hand_m.group(1) if hand_m else '?'}")
    print(f"  Currier: {lang_m.group(1) if lang_m else '?'}")
    print(f"  Section code: {section_m.group(1) if section_m else '?'}")

    f76r_header = folio_data['f76r']['header'] or ''
    hand_m76 = re.search(r'\$H=(\d)', f76r_header)
    lang_m76 = re.search(r'\$L=([AB])', f76r_header)
    print(f"  f76r Hand: {hand_m76.group(1) if hand_m76 else '?'} Currier: {lang_m76.group(1) if lang_m76 else '?'}")

    # Save
    output = {
        'f75v_markers': f75v_seq,
        'f76r_markers': f76r_seq,
        'f49v_markers': [p['marker_text'] for p in f49v_pairs],
        'f75v_char_set': sorted(f75v_set),
        'f76r_char_set': sorted(f76r_set),
        'shared_75_76': sorted(shared_75_76),
        'f75v_subset_of_f76r': f75v_set.issubset(f76r_set),
        'body_match_rate': round(matches/total, 3) if total else None,
        'expected_chance': round(expected/total, 3) if total else None,
        'zl3b_comment': [c for c in folio_data['f75v']['comments']],
    }
    out_path = Path(__file__).parent / 'data.json'
    with open(out_path, 'w') as fj:
        json.dump(output, fj, indent=2)
    print(f"\nSaved to {out_path}")
    print("Done.")
