#!/usr/bin/env python3
"""
Experiment exp_030: f49v Numeral Investigation (H029)
ZL3b comment on f49v: "In the left margin there is a vertical sequence 1 2 3 4 5
aligned with the 1st paragraph, starting from line 2."
Questions:
 1. Which L0 markers encode the numerals 1-5? (lines 2-6)
 2. Do @NNN codes (@140, @192, @164) follow a counting pattern across the folio?
 3. Are there recurring glyphs at regular intervals suggesting a continued counting system?
"""

import re

ZL3B = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

def extract_f49v(path):
    """Extract all f49v lines with comments."""
    lines = []
    in_folio = False
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('<f49v>'):
                in_folio = True
            elif in_folio and re.match(r'^<f\w+>', line) and not line.startswith('<f49v'):
                break
            if in_folio:
                lines.append(line)
    return lines

def parse_locus_entries(raw_lines):
    """Extract locus-coded entries from f49v."""
    entries = []
    for raw in raw_lines:
        m = re.match(r'^<f49v\.(\d+),([^>]+)>\s+(.*)', raw)
        if m:
            line_num = int(m.group(1))
            locus = m.group(2).strip()
            content = m.group(3).strip()
            entries.append({'line_num': line_num, 'locus': locus, 'content': content, 'raw': raw})
    return entries

def is_l0(locus):
    return bool(re.match(r'^[+*@=/~&]?L0$', locus))

def is_p0(locus):
    return bool(re.match(r'^[+*@=/~&]?P0$', locus))

def main():
    raw = extract_f49v(ZL3B)

    print("=== RAW f49v CONTENT (with comments) ===")
    for line in raw:
        print(line)
    print()

    entries = parse_locus_entries(raw)

    # Extract L0 markers in order
    l0_entries = [(e['line_num'], e['locus'], e['content']) for e in entries if is_l0(e['locus'])]
    p0_entries = [(e['line_num'], e['locus'], e['content']) for e in entries if is_p0(e['locus'])]

    print("=== L0 MARKER SEQUENCE (all 26) ===")
    print(f"{'Pos':>3} | {'ZL3b line':>9} | {'Marker':>12} | {'Type'}")
    print("-" * 55)

    # Pair L0 with its position (1-indexed among L0 markers)
    for i, (lnum, locus, content) in enumerate(l0_entries, 1):
        marker_type = 'STANDARD'
        if content.startswith('@'):
            marker_type = 'AT-GLYPH'

        # Identify the numeral zone (lines 2-6 = positions 2-6 in the folio, L0 positions 2-6)
        # The comment says starting from line 2, so L0[0] (line 1) has no numeral
        # L0[1]..L0[5] = "1 2 3 4 5"
        numeral_label = ''
        if i == 2: numeral_label = '← "1"'
        elif i == 3: numeral_label = '← "2"'
        elif i == 4: numeral_label = '← "3"'
        elif i == 5: numeral_label = '← "4"'
        elif i == 6: numeral_label = '← "5"'

        print(f"{i:>3} | f49v.{lnum:<5} | {content:>12} | {marker_type} {numeral_label}")

    print()
    print("=== @NNN GLYPH ANALYSIS ===")
    at_markers = [(i+1, l0_entries[i]) for i in range(len(l0_entries)) if l0_entries[i][2].startswith('@')]
    print(f"{'Position':>8} | {'ZL3b line':>9} | {'Glyph':>10} | Notes")
    print("-" * 60)

    # Map position to paragraph and line-within-paragraph
    # Paragraph boundary: after L0 pos 13 (f49v.25 is last L0 before para break)
    # Para2 starts at L0 pos 14 (f49v.27)
    para_boundary = 13  # first 13 L0s = paragraph 1

    for pos, (lnum, locus, content) in at_markers:
        para = 1 if pos <= para_boundary else 2
        pos_in_para = pos if pos <= para_boundary else pos - para_boundary
        note = f"Para {para}, line {pos_in_para}"

        if pos == 6: note += " | CONFIRMED = numeral '5'"
        elif content == '@192;':
            note += f" | spacing from @140: {pos - [p for p,_ in at_markers if _[2]=='@140;' and p < pos][-1] if [p for p,_ in at_markers if _[2]=='@140;' and p < pos] else '?'} positions"

        print(f"{pos:>8} | f49v.{lnum:<5} | {content:>10} | {note}")

    print()
    print("=== SPACING ANALYSIS: @140 OCCURRENCES ===")
    at140_positions = [i+1 for i, (lnum, locus, content) in enumerate(l0_entries) if content == '@140;']
    print(f"@140 appears at L0 positions: {at140_positions}")
    gaps = [at140_positions[i+1] - at140_positions[i] for i in range(len(at140_positions)-1)]
    print(f"Gaps between @140 occurrences: {gaps}")

    print()
    at192_positions = [i+1 for i, (lnum, locus, content) in enumerate(l0_entries) if content == '@192;']
    print(f"@192 appears at L0 positions: {at192_positions}")
    at164_positions = [i+1 for i, (lnum, locus, content) in enumerate(l0_entries) if content == '@164;']
    print(f"@164 appears at L0 positions: {at164_positions}")

    print()
    print("=== COUNTING SYSTEM TEST ===")
    print("If @140=5, @192=10, @164=? — do @NNN appear at multiples of 5?")
    at_positions_sorted = sorted([(i+1, l0_entries[i][2]) for i in range(len(l0_entries)) if l0_entries[i][2].startswith('@')])
    for pos, glyph in at_positions_sorted:
        mod5 = pos % 5
        print(f"  L0-pos {pos:>2} ({glyph:>8}): pos mod 5 = {mod5} {'<-- MULTIPLE OF 5' if mod5==0 else ''}")

    print()
    print("=== FULL SEQUENCE WITH NUMERAL HYPOTHESIS ===")
    print("Assuming: o=1, r=2, y=3, e=4, @140=5 in first 5-count")
    print("Do these chars recur in counting pattern?")

    # Count all chars in L0 sequence
    from collections import Counter
    char_counts = Counter(e[2] for e in l0_entries)
    print("\nL0 marker character frequency:")
    for char, count in sorted(char_counts.items(), key=lambda x: -x[1]):
        print(f"  '{char}': {count}x")

    # Check if positions 2-6 chars (o,r,y,e,@140) recur at positions 7+
    numeral_chars = {'o', 'r', 'y', 'e', '@140;'}
    post6 = [(i+1, e[2]) for i, e in enumerate(l0_entries) if i >= 6]
    print(f"\nL0 markers at positions 7+ that match '1-5' char set {numeral_chars}:")
    for pos, char in post6:
        if char in numeral_chars:
            print(f"  Position {pos}: '{char}'")

    print()
    print("=== PARAGRAPH-LEVEL PATTERN ===")
    print("Para 1 (L0 pos 1-13):")
    for i, (lnum, locus, content) in enumerate(l0_entries[:13], 1):
        print(f"  [{i:>2}] {content}")
    print("\nPara 2 (L0 pos 14-26):")
    for i, (lnum, locus, content) in enumerate(l0_entries[13:], 14):
        print(f"  [{i:>2}] {content}")

    print()
    print("=== CROSS-PARAGRAPH ALIGNMENT ===")
    print("Same position in each paragraph:")
    for i in range(13):
        p1_char = l0_entries[i][2] if i < len(l0_entries) else '?'
        p2_char = l0_entries[i+13][2] if i+13 < len(l0_entries) else '?'
        match = '==' if p1_char == p2_char else '  '
        print(f"  Line {i+1:>2}: P1='{p1_char:>8}' | P2='{p2_char:>8}' {match}")

    # Count matches
    matches = sum(1 for i in range(13) if i < len(l0_entries) and i+13 < len(l0_entries)
                  and l0_entries[i][2] == l0_entries[i+13][2])
    print(f"\nMatches across paragraphs: {matches}/13")

if __name__ == '__main__':
    main()
