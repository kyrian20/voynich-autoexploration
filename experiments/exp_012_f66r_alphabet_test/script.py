"""
Experiment: exp_012_f66r_alphabet_test
Goal: Test whether f66r column 2 is an alphabet inventory of the Voynich writing system.
Compare column 2 entries (including @NNN; special glyphs) against the full EVA character
inventory from the body corpus.
Data: data/transcriptions/eva_zl3b.txt
"""

import re
import math
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

# ── f66r column 2 raw entries (manually enumerated from raw transcription) ─────
# Lines 16-49 of f66r, preserving @NNN; special chars
F66R_COL2_RAW = [
    ('L16', 'y'),
    ('L17', 'o'),
    ('L18', 's'),
    ('L19', 'sh'),
    ('L20', 'y'),
    ('L21', 'd'),
    ('L22', 'o'),
    ('L23', 'f'),
    ('L24', '@169'),   # special glyph
    ('L25', 'x'),
    ('L26', 'air'),
    ('L27', 'd'),
    ('L28', 'sh'),
    ('L29', 'y'),
    ('L30', 'f'),
    ('L31', 'f'),
    ('L32', 'y'),
    ('L33', 'o'),
    ('L34', 'd'),
    ('L35', 's'),
    ('L36', 'f'),
    ('L37', 'c'),      # comment stripped from 'c<!cf f57v seq.>'
    ('L38', '@172'),   # special glyph, comment stripped
    ('L39', 'x'),
    ('L40', 't'),
    ('L41', 'o'),
    ('L42', '@195'),   # special glyph
    ('L43', 'l'),
    ('L44', 'r'),
    ('L45', 't'),
    ('L46', 'o'),
    ('L47', 'x'),
    ('L48', 'p'),
    ('L49', 'd'),
]

# Unique entries in column 2
COL2_ENTRIES = [v for _, v in F66R_COL2_RAW]
COL2_UNIQUE = set(COL2_ENTRIES)
COL2_FREQ = Counter(COL2_ENTRIES)

# ── Extract EVA character inventory from body corpus ──────────────────────────
# Strategy: tokenize at single-character level AND extract common compound forms.
# Compound forms recognized in EVA as single glyphs:
# - ch, sh (most common digraphs)
# - ck, ct, cp, cf  (compound gallows = bench variants)
# - cth, ckh, cph, cfh (doubly compound gallows)
# - ee, eee, eeee (multiple minims)
# - ii, iii (multiple i's)
# - aiin, ain, aiiin (common word-end sequences)
# - qo (near-invariant word-onset bigram)
# We treat these as possible "glyph units" to check if column 2 lists them as units.

COMPOUND_GLYPHS = [
    'cth', 'ckh', 'cph', 'cfh',  # doubly compound (order matters: longer first)
    'ch', 'sh', 'ck', 'ct', 'cp', 'cf',  # compound digraphs
    'eee', 'ee',  # repeated e (longer first)
    'iii', 'ii',  # repeated i
    'aiin', 'ain',  # common endings
    'qo',  # near-invariant onset
]

def tokenize_with_compounds(word, compound_list):
    """Tokenize a word into compound and simple units."""
    tokens = []
    i = 0
    while i < len(word):
        matched = False
        for cg in compound_list:
            if word[i:i+len(cg)] == cg:
                tokens.append(cg)
                i += len(cg)
                matched = True
                break
        if not matched:
            tokens.append(word[i])
            i += 1
    return tokens


def parse_body_words(path):
    words = []
    with open(path, encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'^<[^>]+,([^>]+)>\s+(.*)', line)
            if not m:
                continue
            locus = re.sub(r'^[^A-Za-z]+', '', m.group(1))
            if not locus.startswith('P'):  # body text only
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
                    words.append(w)
    return words


if __name__ == "__main__":
    print("Experiment exp_012: f66r Column 2 Alphabet Inventory Test")
    print("Date: 2026-04-09\n")

    # ── Column 2 summary ──────────────────────────────────────────────────────
    print(f"Column 2 entries: {len(COL2_ENTRIES)} total, {len(COL2_UNIQUE)} unique")
    print(f"  All entries: {COL2_ENTRIES}")
    print(f"  Unique: {sorted(COL2_UNIQUE)}")
    print(f"  Frequency: {COL2_FREQ.most_common()}")
    special = [e for e in COL2_UNIQUE if e.startswith('@')]
    compounds = [e for e in COL2_UNIQUE if len(e) > 1 and not e.startswith('@')]
    singles = [e for e in COL2_UNIQUE if len(e) == 1]
    print(f"\n  Special glyphs (@NNN;): {special}")
    print(f"  Compound entries (multi-char EVA): {compounds}")
    print(f"  Single-char EVA: {sorted(singles)}")

    # ── Body corpus character inventory ───────────────────────────────────────
    words = parse_body_words(BASE / 'data/transcriptions/eva_zl3b.txt')
    total_chars = sum(len(w) for w in words)
    print(f"\nBody corpus: {len(words):,} words, {total_chars:,} characters")

    # Single-char inventory
    all_chars = list(''.join(words))
    char_freq = Counter(all_chars)
    print(f"\nSingle-char EVA inventory ({len(char_freq)} distinct chars):")
    print(f"  All chars: {sorted(char_freq.keys())}")
    print(f"  By frequency:")
    for c, cnt in char_freq.most_common():
        pct = 100 * cnt / len(all_chars)
        in_col2 = c in COL2_UNIQUE
        flag = " ← IN COL2" if in_col2 else ""
        print(f"    '{c}': {cnt:6,} ({pct:5.2f}%){flag}")

    # Compound glyph inventory
    compound_tokens = []
    for w in words:
        compound_tokens.extend(tokenize_with_compounds(w, COMPOUND_GLYPHS))
    compound_freq = Counter(t for t in compound_tokens if len(t) > 1)
    print(f"\nCommon compound EVA forms (top 20, sorted by frequency):")
    for cg, cnt in compound_freq.most_common(20):
        pct = 100 * cnt / len(compound_tokens)
        in_col2 = cg in COL2_UNIQUE
        flag = " ← IN COL2" if in_col2 else ""
        print(f"    '{cg}': {cnt:6,} ({pct:4.2f}%){flag}")

    # ── Coverage analysis ─────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("COVERAGE ANALYSIS")
    print(f"{'='*60}")

    # (a) Characters in BOTH column 2 and body (at appropriate frequencies)
    in_both_single = [c for c in COL2_UNIQUE if len(c) == 1 and c in char_freq]
    in_both_compound = [c for c in COL2_UNIQUE if len(c) > 1 and not c.startswith('@') and c in compound_freq]
    print(f"\n(a) In both column 2 AND body corpus:")
    print(f"  Single chars ({len(in_both_single)}): {sorted(in_both_single)}")
    print(f"  Compound forms ({len(in_both_compound)}): {sorted(in_both_compound)}")
    for c in sorted(in_both_single):
        cnt = char_freq[c]
        pct = 100 * cnt / len(all_chars)
        col2_cnt = COL2_FREQ[c]
        print(f"    '{c}': body {cnt:,} ({pct:.2f}%), col2 ×{col2_cnt}")

    # (b) In column 2 but RARE or ABSENT in body
    rare_thresh = 0.001  # <0.1% of chars
    print(f"\n(b) In column 2 but rare in body (< {rare_thresh*100:.1f}% of chars):")
    for c in sorted(COL2_UNIQUE):
        if c.startswith('@'):
            print(f"  '{c}' (special glyph — no body equivalent)")
            continue
        freq_in_body = char_freq.get(c, compound_freq.get(c, 0))
        total = len(all_chars) if len(c) == 1 else len(compound_tokens)
        pct = freq_in_body / total if total > 0 else 0
        if pct < rare_thresh:
            print(f"  '{c}': body {freq_in_body} ({pct*100:.4f}%), col2 ×{COL2_FREQ[c]}")

    # (c) In body but ABSENT from column 2 — the "missed" characters
    print(f"\n(c) In body (>100 occurrences) but NOT in column 2:")
    absent_common = []
    for c, cnt in char_freq.most_common():
        if c not in COL2_UNIQUE:
            pct = 100 * cnt / len(all_chars)
            absent_common.append((c, cnt, pct))
    for c, cnt, pct in absent_common:
        print(f"  '{c}': {cnt:6,} ({pct:.2f}%) ← ABSENT from column 2")

    # Coverage statistics
    print(f"\n{'='*60}")
    print("COVERAGE STATISTICS")
    print(f"{'='*60}")
    n_single_in_body = len(char_freq)
    n_single_in_col2 = len(in_both_single)
    n_compound_in_body = len([k for k, v in compound_freq.items() if v >= 100])
    n_compound_in_col2 = len(in_both_compound)

    print(f"\nSingle-char coverage: {n_single_in_col2}/{n_single_in_body} = "
          f"{100*n_single_in_col2/n_single_in_body:.1f}%")
    print(f"Common compound coverage: {n_compound_in_col2}/{n_compound_in_body} = "
          f"{100*n_compound_in_col2/n_compound_in_body:.1f}%")
    print(f"Column 2 includes {len(special)} special (@NNN;) glyphs not in EVA standard")

    # Key verdict
    print(f"\n{'='*60}")
    print("VERDICT")
    print(f"{'='*60}")
    if n_single_in_col2 / n_single_in_body >= 0.7:
        verdict = "HIGH coverage — supports alphabet inventory hypothesis"
    elif n_single_in_col2 / n_single_in_body >= 0.4:
        verdict = "MODERATE coverage — partial inventory or specialized subset"
    else:
        verdict = "LOW coverage — column 2 is NOT a comprehensive alphabet inventory"
    print(f"\n{verdict}")
    print(f"Key absences from column 2: "
          f"{[c for c,_,_ in absent_common if char_freq[c] > 500]}")
    print("\nDone.")
