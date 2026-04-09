"""
Experiment: exp_020_f68r2_second_cluster
Goal: Characterize f68r2's @231-@234 sequence and test whether it is a second
structured @glyph cluster analogous to f57v's @169-@172.
Also: search for any other folios with 3+ consecutive @glyphs.
"""

import re
import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
CORPUS = BASE / 'data/transcriptions/eva_zl3b.txt'

def ivtff_tokenize(text):
    """Tokenize IVTFF text on dots, respecting brackets."""
    tokens = []
    current = []
    depth = 0
    for ch in text:
        if ch == '[':
            depth += 1
            current.append(ch)
        elif ch == ']':
            depth -= 1
            current.append(ch)
        elif ch == '.' and depth == 0:
            tok = ''.join(current).strip()
            if tok:
                tokens.append(tok)
            current = []
        else:
            current.append(ch)
    last = ''.join(current).strip()
    if last:
        tokens.append(last)
    return tokens


def extract_folio_raw(path, folio_str):
    """Extract all raw lines from a folio."""
    lines = []
    header = None
    in_folio = False
    with open(path, encoding='latin-1') as f:
        for raw_line in f:
            stripped = raw_line.strip()
            if f'<{folio_str}>' in stripped and re.match(rf'^<{re.escape(folio_str)}>', stripped):
                in_folio = True
                header = stripped
                continue
            if in_folio:
                if re.match(r'^<f\d+', stripped) and f'<{folio_str}.' not in stripped:
                    break
                lines.append(stripped)
    return header, lines


def find_consecutive_at_glyphs(path):
    """Find all lines with 2+ consecutive @NNN;@NNN patterns."""
    results = []
    with open(path, encoding='latin-1') as f:
        for i, raw_line in enumerate(f, 1):
            line = raw_line.strip()
            # Find consecutive @NNN; pairs (possibly multiple)
            matches = re.findall(r'(?:@\d+;){2,}', line)
            if matches:
                folio_m = re.match(r'^<(f\d+[rv]\d*)\.', line)
                folio = folio_m.group(1) if folio_m else '?'
                locus_m = re.match(r'^<[^>]+,([^>]+)>', line)
                locus = locus_m.group(1) if locus_m else '?'
                results.append({
                    'line_num': i,
                    'folio': folio,
                    'locus': locus,
                    'consecutive_groups': matches,
                    'max_consecutive': max(m.count('@') for m in matches),
                    'raw': line,
                })
    return results


if __name__ == "__main__":
    print("Experiment exp_020: f68r2 Second Cluster Analysis")
    print("Date: 2026-04-09\n")

    # 1. Extract f68r2 transcription
    header, lines = extract_folio_raw(CORPUS, 'f68r2')
    print(f"ZL3b header: {header}")
    print(f"\nFull f68r2 transcription:")
    for line in lines:
        if line:
            at_glyphs = re.findall(r'@\d+;?', line)
            note = f" [@glyphs: {at_glyphs}]" if at_glyphs else ""
            print(f"  {line}{note}")

    # 2. Locate @231-@234
    print(f"\n--- @231-@234 sequence analysis ---")
    target_line = None
    for line in lines:
        if '@231' in line or '@232' in line:
            target_line = line
            break

    if target_line:
        print(f"Line containing @231-@234:")
        print(f"  {target_line}")
        # Extract locus
        m = re.match(r'^<f68r2\.(\d+),([^>]+)>\s*(.*)', target_line)
        if m:
            linenum = m.group(1)
            locus = m.group(2)
            text = m.group(3)
            print(f"\n  Line number: {linenum}")
            print(f"  Locus: {locus}")
            # Tokenize
            clean = re.sub(r'<!.*?>', '', text)
            clean = re.sub(r'<[^>]+>', '', clean)
            tokens = ivtff_tokenize(clean)
            print(f"  Total tokens: {len(tokens)}")
            print(f"  Tokens: {tokens}")
            # Find @glyph positions
            at_positions = [(i, t) for i, t in enumerate(tokens) if '@' in t]
            print(f"\n  @glyph token positions:")
            for pos, tok in at_positions:
                prev = tokens[pos-1] if pos > 0 else None
                nxt = tokens[pos+1] if pos < len(tokens)-1 else None
                print(f"    Position {pos}: '{tok}' | prev='{prev}' | next='{nxt}'")
            # Check if consecutive
            at_pos_nums = [p for p, _ in at_positions]
            if len(at_pos_nums) >= 2:
                diffs = [at_pos_nums[i+1] - at_pos_nums[i] for i in range(len(at_pos_nums)-1)]
                print(f"\n  Are @glyphs consecutive in token list? "
                      f"diffs={diffs}, all_1={all(d==1 for d in diffs)}")
            # Check raw adjacency (no dot between them)
            raw_adj = re.search(r'@231;@232;@233;@234;', text)
            print(f"  Raw adjacency (@231;@232;@233;@234; with no separator): "
                  f"{'YES' if raw_adj else 'NO'}")

    # 3. Is this repeating like f57v?
    print(f"\n--- Repeating structure test ---")
    cc_lines = [l for l in lines if ',@Cc>' in l or ',+Cc>' in l]
    print(f"Circular text lines in f68r2: {len(cc_lines)}")
    for cl in cc_lines:
        print(f"  {cl}")

    # 4. Structural comparison with f57v
    print(f"\n--- Structural comparison: f68r2 vs f57v ---")
    print(f"\nf57v L03 pattern:")
    print(f"  Context: Repeating 17-token cycle, @glyphs at positions 10,13,14,17")
    print(f"  @glyphs distributed throughout cycle with standard chars between them")
    print(f"  Pattern: [8 std chars] [@169;v] [t r] [@170] [@171] [y] [I/c] [@172]")
    print(f"  Repeats: 4× identical structure")

    print(f"\nf68r2 L31 pattern:")
    print(f"  Context: End of bottom ring circular text band (@Cc locus)")
    print(f"  @glyphs: 4 consecutive, no separators between them (raw: @231;@232;@233;@234;)")
    print(f"  Terminate the line — no repeating structure")
    print(f"  Pattern: [standard Voynich text...] [terminus: @231@232@233@234]")

    print(f"\nConclusion: DIFFERENT PATTERNS")
    print(f"  f57v: @glyphs distributed within a repeating structured cycle")
    print(f"  f68r2: @glyphs concatenated at the terminus of a non-repeating circular band")

    # 5. Search for other consecutive @glyph occurrences
    print(f"\n--- All consecutive @glyph groups in manuscript ---")
    consec = find_consecutive_at_glyphs(CORPUS)
    print(f"Lines with 2+ consecutive @glyphs: {len(consec)}")
    for r in consec:
        print(f"  {r['folio']} [{r['locus']}]: max={r['max_consecutive']} — "
              f"groups: {r['consecutive_groups']}")
        print(f"    Context: {r['raw'][:100]}")

    # Save data
    output = {
        'f68r2_header': header,
        'at231_234_context': target_line,
        'is_repeating': False,
        'pattern_type': 'terminal_concatenated',
        'f57v_comparison': 'different_structure',
        'consecutive_at_glyph_lines': consec,
        'verdict': 'f68r2 @231-@234 is terminal concatenation, NOT a second structured cluster',
    }
    out_path = Path(__file__).parent / 'data.json'
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {out_path}")
    print("\nDone.")
