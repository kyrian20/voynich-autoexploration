"""
Experiment: exp_013_line_marker_structure
Goal: Structural analysis of f49v and f76r line-marker sequences.
- Repeating subsequences / periodicity
- Character frequency vs. manuscript distribution
- Correspondence between marker and adjacent body text line
- Cross-sequence comparison
Data: data/transcriptions/eva_zl3b.txt
"""

import re
import math
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

# ── Known sequences (from raw transcription inspection) ───────────────────────
# f49v: L0 markers for each body text line (26 marker/body pairs)
# f76r: L0 markers for selected paragraphs (9 markers), not every line

# We need to pair each marker with its following body text content.

def parse_folio_lines(path, folio_str):
    """Parse all lines from a folio, preserving order."""
    entries = []
    in_folio = False
    with open(path, encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if f'<{folio_str}>' in line:
                in_folio = True
                continue
            if in_folio:
                # Stop at next folio
                if re.match(r'^<f\d+', line) and f'<{folio_str}.' not in line:
                    break
                if not line or line.startswith('#'):
                    continue
                m = re.match(rf'^<{re.escape(folio_str)}\.(\d+),([^>]+)>\s*(.*)', line)
                if not m:
                    continue
                linenum = int(m.group(1))
                locus = re.sub(r'^[^A-Za-z]+', '', m.group(2))
                raw = m.group(3).strip()
                # Clean text for tokens
                text = re.sub(r'<!.*?>', '', raw)
                text = re.sub(r'<[^>]+>', '', text)
                text = text.replace('<%>', '').replace('<$>', '').replace('%', '')
                text = re.sub(r'\[([^:\]]+):[^\]]*\]', r'\1', text)
                text = re.sub(r'\{[^}]*\}', '', text)
                text = re.sub(r'@\d+;?', '@SPECIAL', text)
                tokens = [t for t in re.split(r'[.\s,<>]+', text)
                         if t and (re.match(r'^[a-zA-Z]+$', t) or t == '@SPECIAL')]
                ltype = {'P': 'body', 'L': 'label'}.get(locus[0] if locus else '?', 'other')
                entries.append({
                    'line': linenum, 'ltype': ltype,
                    'locus': locus, 'raw': raw, 'tokens': tokens
                })
    return entries


def get_marker_body_pairs(entries):
    """
    For each L0 marker entry, find the immediately following P0 body text entry.
    Returns list of (marker_token, body_tokens, body_first_char, body_last_char).
    """
    pairs = []
    by_line = {e['line']: e for e in entries}
    for e in entries:
        if e['ltype'] != 'label':
            continue
        marker_tokens = e['tokens']
        if not marker_tokens:
            # Could be @SPECIAL glyph
            if '@SPECIAL' in e['raw'] or '@' in e['raw']:
                marker_tokens = ['@SPECIAL']
            else:
                continue
        marker = marker_tokens[0] if marker_tokens else '@EMPTY'
        # Find next entry (label or body)
        next_line = e['line'] + 1
        while next_line <= e['line'] + 3:
            if next_line in by_line:
                nxt = by_line[next_line]
                if nxt['ltype'] == 'body' and nxt['tokens']:
                    body = nxt['tokens']
                    pairs.append({
                        'marker': marker,
                        'body_first_char': body[0][0] if body[0] else '',
                        'body_last_char': body[-1][-1] if body[-1] else '',
                        'body_first_word': body[0] if body else '',
                        'body_last_word': body[-1] if body else '',
                        'body_length': sum(len(t) for t in body),
                        'body_tokens': body,
                        'marker_line': e['line'],
                        'body_line': next_line,
                    })
                    break
            next_line += 1
    return pairs


def char_freq_from_body(path):
    """Get character frequency from all body text."""
    chars = []
    with open(path, encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'^<[^>]+,([^>]+)>\s+(.*)', line)
            if not m:
                continue
            locus = re.sub(r'^[^A-Za-z]+', '', m.group(1))
            if not locus.startswith('P'):
                continue
            text = m.group(2)
            text = re.sub(r'<!.*?>', '', text)
            text = re.sub(r'<[^>]+>', '', text)
            text = text.replace('<%>', '').replace('<$>', '').replace('%', '')
            text = re.sub(r'\[([^:\]]+):[^\]]*\]', r'\1', text)
            text = re.sub(r'\{[^}]*\}', '', text)
            text = re.sub(r'@\d+;?', '', text)
            for w in re.split(r'[.\s,]+', text):
                if w and re.match(r'^[a-zA-Z]+$', w):
                    chars.extend(w)
    return Counter(chars)


def check_periodicity(seq, max_period=10):
    """Check if a sequence has periodic structure."""
    n = len(seq)
    results = []
    for period in range(1, min(max_period + 1, n)):
        mismatches = 0
        for i in range(n):
            if seq[i] != seq[i % period]:
                mismatches += 1
        match_rate = (n - mismatches) / n
        results.append((period, match_rate, mismatches))
    return results


if __name__ == "__main__":
    print("Experiment exp_013: Line Marker Structure Analysis")
    print("Date: 2026-04-09\n")

    path = BASE / 'data/transcriptions/eva_zl3b.txt'
    global_char_freq = char_freq_from_body(path)
    total_chars = sum(global_char_freq.values())

    for folio_str in ['f49v', 'f76r']:
        print(f"\n{'='*60}")
        print(f"FOLIO {folio_str}")
        print(f"{'='*60}")

        entries = parse_folio_lines(path, folio_str)
        pairs = get_marker_body_pairs(entries)
        markers = [p['marker'] for p in pairs]

        print(f"\nTotal marker/body pairs: {len(pairs)}")
        print(f"Marker sequence: {markers}")
        marker_freq = Counter(markers)
        print(f"Marker frequency: {marker_freq.most_common()}")

        # Repeating analysis
        print(f"\n--- Periodicity check (period 1-{min(8, len(markers)//2)}) ---")
        if len(markers) >= 4:
            periodic = check_periodicity(markers, max_period=min(8, len(markers)//2))
            for period, match_rate, mismatches in periodic:
                if match_rate >= 0.5:
                    print(f"  Period {period}: {match_rate:.0%} match ({mismatches} mismatches)")
                    if period <= 6:
                        print(f"    Pattern: {markers[:period]}")
        else:
            print(f"  Sequence too short for periodicity analysis")

        # Character frequency comparison to manuscript
        print(f"\n--- Marker chars vs. manuscript frequency ---")
        for c, cnt in marker_freq.most_common():
            if c.startswith('@'):
                print(f"  '{c}': ×{cnt} in markers — special glyph")
                continue
            global_cnt = global_char_freq.get(c, 0)
            global_pct = 100 * global_cnt / total_chars if total_chars else 0
            marker_pct = 100 * cnt / len(markers)
            ratio = (marker_pct / global_pct) if global_pct > 0 else float('inf')
            direction = "↑ over" if ratio > 2 else ("↓ under" if ratio < 0.5 else "≈ normal")
            print(f"  '{c}': ×{cnt} ({marker_pct:.0f}%) in markers, "
                  f"{global_pct:.2f}% in corpus — {direction}represented (ratio {ratio:.1f}x)")

        # Body text correspondence analysis
        print(f"\n--- Marker vs body text correspondence ---")
        # Check multiple possible correspondences
        first_char_match = sum(1 for p in pairs if p['marker'] == p['body_first_char'])
        last_char_match = sum(1 for p in pairs if p['marker'] == p['body_last_char'])
        first_word_first = sum(1 for p in pairs if p['body_first_word'].startswith(p['marker']))
        last_word_last = sum(1 for p in pairs if p['body_last_word'].endswith(p['marker']))

        print(f"  Marker == body line first char: {first_char_match}/{len(pairs)} "
              f"({100*first_char_match/len(pairs):.0f}%)")
        print(f"  Marker == body line last char: {last_char_match}/{len(pairs)} "
              f"({100*last_char_match/len(pairs):.0f}%)")
        print(f"  Body first word starts with marker: {first_word_first}/{len(pairs)} "
              f"({100*first_word_first/len(pairs):.0f}%)")
        print(f"  Body last word ends with marker: {last_word_last}/{len(pairs)} "
              f"({100*last_word_last/len(pairs):.0f}%)")

        # Expected by chance
        if len(pairs) > 0:
            # For first char: chance = (freq of marker in corpus) / total chars
            expected_first = sum(
                global_char_freq.get(p['marker'], 0) / total_chars
                for p in pairs if not p['marker'].startswith('@')
            ) / len(pairs)
            print(f"  Expected first-char match by chance: {100*expected_first:.1f}%")

        # Show first N pairs
        print(f"\n  First 10 marker → body pairs:")
        for p in pairs[:10]:
            print(f"    '{p['marker']}' → first_char='{p['body_first_char']}' "
                  f"last_char='{p['body_last_char']}' "
                  f"first_word='{p['body_first_word'][:10]}' "
                  f"(len={p['body_length']})")

    # ── Cross-sequence comparison ──────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("CROSS-SEQUENCE COMPARISON")
    print(f"{'='*60}")

    f49v_entries = parse_folio_lines(path, 'f49v')
    f76r_entries = parse_folio_lines(path, 'f76r')
    f49v_pairs = get_marker_body_pairs(f49v_entries)
    f76r_pairs = get_marker_body_pairs(f76r_entries)
    seq_49v = [p['marker'] for p in f49v_pairs]
    seq_76r = [p['marker'] for p in f76r_pairs]

    print(f"\nf49v sequence ({len(seq_49v)}): {seq_49v}")
    print(f"f76r sequence ({len(seq_76r)}): {seq_76r}")

    shared = set(seq_49v) & set(seq_76r)
    only_49v = set(seq_49v) - set(seq_76r)
    only_76r = set(seq_76r) - set(seq_49v)
    print(f"\nShared markers: {sorted(shared)}")
    print(f"Only in f49v: {sorted(only_49v)}")
    print(f"Only in f76r: {sorted(only_76r)}")

    # Check if either is a subsequence of the other
    def is_subsequence(short, long):
        it = iter(long)
        return all(c in it for c in short)

    print(f"\nIs f76r a subsequence of f49v? {is_subsequence(seq_76r, seq_49v)}")
    print(f"Is f49v a subsequence of f76r? {is_subsequence(seq_49v, seq_76r)}")

    # Check for shared n-grams
    for n in [2, 3]:
        ngrams_49v = set(tuple(seq_49v[i:i+n]) for i in range(len(seq_49v)-n+1))
        ngrams_76r = set(tuple(seq_76r[i:i+n]) for i in range(len(seq_76r)-n+1))
        shared_ng = ngrams_49v & ngrams_76r
        print(f"Shared {n}-grams: {len(shared_ng)} — {list(shared_ng)[:5]}")

    print("\nDone.")
