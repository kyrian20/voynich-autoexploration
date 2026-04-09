"""
Experiment: exp_011_f66r_wordlist
Goal: Characterize f66r content (15-word column, 28 single-char column, body text paragraphs).
Also: run L0 structural audit across full ZL3b; check adjacent folios (f65v, f66v, f67r).
Data: data/transcriptions/eva_zl3b.txt
Dependencies: standard library only
"""

import re
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

# ── Full ZL3b parser with line-type structure ──────────────────────────────────

def parse_full_structure(path):
    """
    Parse ZL3b into a structured list.
    Each entry: {folio, folio_num, line_num, locus_type, locus_code, raw_text, tokens}
    """
    entries = []
    with open(path, encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'^<f(\d+)([rv])\.(\d+),([^>]+)>\s*(.*)', line)
            if not m:
                continue
            folio_num = int(m.group(1))
            folio_str = f"f{m.group(1)}{m.group(2)}"
            line_num = int(m.group(3))
            locus_raw = m.group(4)
            locus_code = re.sub(r'^[^A-Za-z]+', '', locus_raw)
            raw_text = m.group(5).strip()
            ltype = {'P': 'body', 'L': 'label', 'R': 'rider', 'C': 'circular'}.get(
                locus_code[0] if locus_code else '?', 'other')

            # Clean text
            text = re.sub(r'<!.*?>', '', raw_text)
            text = re.sub(r'<[^>]+>', '', text)
            text = text.replace('<%>', '').replace('<$>', '').replace('%', '')
            text = re.sub(r'\[([^:\]]+):[^\]]*\]', r'\1', text)
            text = re.sub(r'\{[^}]*\}', '', text)
            text = re.sub(r'@\d+;?', '', text)
            tokens = [t for t in re.split(r'[.\s,]+', text) if t and re.match(r'^[a-zA-Z]+$', t)]

            entries.append({
                'folio': folio_str,
                'folio_num': folio_num,
                'line_num': line_num,
                'locus_type': ltype,
                'locus_code': locus_code,
                'raw_text': raw_text,
                'tokens': tokens,
            })
    return entries


def h2_from_tokens(tokens):
    if len(tokens) < 2:
        return 0.0
    unigrams = Counter(tokens)
    bigrams = Counter(zip(tokens[:-1], tokens[1:]))
    tu = sum(unigrams.values())
    tb = sum(bigrams.values())
    hu = -sum((v/tu)*math.log2(v/tu) for v in unigrams.values())
    hb = -sum((v/tb)*math.log2(v/tb) for v in bigrams.values())
    return hb - hu


# ── L0 Structural Audit ───────────────────────────────────────────────────────

def classify_l0_structure(entries):
    """
    Classify each folio's L0 entries as:
    - 'line_marker': L0 entries alternate perfectly with P0 entries (one L0 per P0 line)
    - 'standalone_list': Multiple consecutive L0 entries with no interleaved P0
    - 'mixed': L0 entries among P0 entries but not perfectly alternating
    - 'single_label': A small number of L0 entries on a folio with mostly non-L0 content
    """
    folio_structure = {}
    by_folio = defaultdict(list)
    for e in entries:
        by_folio[e['folio']].append(e)

    for folio, folio_entries in by_folio.items():
        l0_lines = [e for e in folio_entries if e['locus_type'] == 'label']
        p0_lines = [e for e in folio_entries if e['locus_type'] == 'body']

        if not l0_lines:
            continue

        n_l0 = len(l0_lines)
        n_p0 = len(p0_lines)

        # Check for alternating pattern: each L0 line immediately precedes a P0 line
        l0_line_nums = set(e['line_num'] for e in l0_lines)
        p0_line_nums = set(e['line_num'] for e in p0_lines)

        # Count L0 entries where next line is P0
        alternating_count = sum(1 for ln in l0_line_nums if (ln + 1) in p0_line_nums)
        alternating_ratio = alternating_count / n_l0 if n_l0 > 0 else 0

        # Check for consecutive L0 (list structure): L0 entries consecutive with no P0 between
        l0_sorted = sorted(l0_lines, key=lambda x: x['line_num'])
        consecutive_runs = 0
        run_len = 1
        max_run = 1
        for i in range(1, len(l0_sorted)):
            if l0_sorted[i]['line_num'] == l0_sorted[i-1]['line_num'] + 1:
                run_len += 1
                max_run = max(max_run, run_len)
            else:
                if run_len >= 3:
                    consecutive_runs += 1
                run_len = 1

        # Classify
        if alternating_ratio >= 0.8 and n_l0 >= 5:
            classification = 'line_marker'
        elif max_run >= 5 and (n_p0 == 0 or max_run >= n_l0 * 0.5):
            classification = 'standalone_list'
        elif n_l0 <= 3:
            classification = 'single_label'
        else:
            classification = 'mixed'

        folio_structure[folio] = {
            'n_l0': n_l0,
            'n_p0': n_p0,
            'alternating_ratio': round(alternating_ratio, 3),
            'max_consecutive_l0_run': max_run,
            'classification': classification,
            'l0_tokens': [t for e in l0_lines for t in e['tokens']],
            'single_char_count': sum(1 for e in l0_lines for t in e['tokens'] if len(t) == 1),
        }

    return folio_structure


# ── Main ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Experiment exp_011: f66r Word List Investigation + L0 Structural Audit")
    print("Date: 2026-04-09\n")

    entries = parse_full_structure(BASE / 'data/transcriptions/eva_zl3b.txt')
    print(f"Total transcription lines parsed: {len(entries):,}")

    # ── Part 1: f66r detailed content ─────────────────────────────────────────
    print(f"\n{'='*60}")
    print("PART 1: f66r CONTENT ANALYSIS")
    print(f"{'='*60}")

    f66r_entries = [e for e in entries if e['folio'] == 'f66r']
    f66r_labels = [e for e in f66r_entries if e['locus_type'] == 'label']
    f66r_body = [e for e in f66r_entries if e['locus_type'] == 'body']

    print(f"\nf66r total lines: {len(f66r_entries)}")
    print(f"  Label (L0) lines: {len(f66r_labels)}")
    print(f"  Body (P0) lines: {len(f66r_body)}")

    # Split label content into the two columns based on line numbers
    # Lines 1-15: word column; Lines 16-49: single-char column
    word_col = [e for e in f66r_labels if e['line_num'] <= 15]
    char_col = [e for e in f66r_labels if 16 <= e['line_num'] <= 49]

    word_col_tokens = [t for e in word_col for t in e['tokens']]
    char_col_tokens = [t for e in char_col for t in e['tokens']]

    print(f"\nColumn 1 (word list, lines 1-15): {len(word_col)} entries, {len(word_col_tokens)} tokens")
    print(f"  Words: {word_col_tokens}")
    print(f"  Length distribution: {sorted(Counter(len(w) for w in word_col_tokens).items())}")
    print(f"  Types: {len(set(word_col_tokens))} (all unique: {len(set(word_col_tokens)) == len(word_col_tokens)})")

    print(f"\nColumn 2 (char list, lines 16-49): {len(char_col)} entries, {len(char_col_tokens)} tokens")
    print(f"  Chars: {char_col_tokens}")
    print(f"  Single-char count: {sum(1 for t in char_col_tokens if len(t) == 1)}")
    print(f"  Multi-char (len>=2): {[t for t in char_col_tokens if len(t) >= 2]}")
    print(f"  Char frequency: {Counter(char_col_tokens).most_common()}")

    # Body text paragraphs on f66r
    body_tokens = [t for e in f66r_body for t in e['tokens']]
    print(f"\nBody text paragraphs (lines 50+): {len(f66r_body)} lines, {len(body_tokens)} tokens")
    print(f"  Top words: {Counter(body_tokens).most_common(10)}")

    # ── Check if word-list tokens appear elsewhere in manuscript ──────────────
    print(f"\n{'='*60}")
    print("WORD LIST TOKENS: MANUSCRIPT-WIDE OCCURRENCE")
    print(f"{'='*60}")

    # Build full token index (excluding f66r)
    all_tokens_ex_f66r = [t for e in entries if e['folio'] != 'f66r' for t in e['tokens']]
    global_freq = Counter(all_tokens_ex_f66r)
    global_total = len(all_tokens_ex_f66r)

    print(f"\nColumn 1 words — frequency in rest of manuscript:")
    for w in word_col_tokens:
        freq = global_freq.get(w, 0)
        pct = 100 * freq / global_total if global_total > 0 else 0
        print(f"  '{w}': {freq} times ({pct:.3f}%)")

    print(f"\nColumn 2 single-char tokens — rare or common elsewhere?")
    char_freq = Counter(char_col_tokens)
    for char, count in sorted(char_freq.items(), key=lambda x: -x[1]):
        global_count = global_freq.get(char, 0)
        pct = 100 * global_count / global_total if global_total > 0 else 0
        print(f"  '{char}' (appears {count}x in f66r col2): {global_count} times globally ({pct:.3f}%)")

    # ── Adjacent folios ────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("ADJACENT FOLIOS: f65r, f65v, f66v, f67r")
    print(f"{'='*60}")

    for folio in ['f65r', 'f65v', 'f66v', 'f67r']:
        folio_entries = [e for e in entries if e['folio'] == folio]
        l0 = [e for e in folio_entries if e['locus_type'] == 'label']
        p0 = [e for e in folio_entries if e['locus_type'] == 'body']
        if not folio_entries:
            print(f"  {folio}: not found")
            continue
        l0_tokens = [t for e in l0 for t in e['tokens']]
        p0_tokens = [t for e in p0 for t in e['tokens']]
        print(f"\n  {folio}: {len(l0)} label lines ({len(l0_tokens)} tokens), "
              f"{len(p0)} body lines ({len(p0_tokens)} tokens)")
        if l0_tokens:
            print(f"    Label tokens: {l0_tokens[:10]}")
        if p0_tokens:
            print(f"    Body top words: {Counter(p0_tokens).most_common(5)}")

    # ── Part 2: L0 Structural Audit ──────────────────────────────────────────
    print(f"\n{'='*60}")
    print("PART 2: L0 STRUCTURAL AUDIT — ALL FOLIOS")
    print(f"{'='*60}")

    l0_structure = classify_l0_structure(entries)

    # Summary by classification
    class_summary = Counter(v['classification'] for v in l0_structure.values())
    print(f"\nClassification summary:")
    for cls, count in class_summary.most_common():
        print(f"  {cls}: {count} folios")

    # Detail by classification
    for cls in ['line_marker', 'standalone_list', 'mixed']:
        folios_in_cls = [(f, v) for f, v in l0_structure.items() if v['classification'] == cls]
        if folios_in_cls:
            print(f"\n  {cls.upper()} folios ({len(folios_in_cls)}):")
            for f, v in sorted(folios_in_cls, key=lambda x: x[0]):
                print(f"    {f}: n_l0={v['n_l0']}, n_p0={v['n_p0']}, "
                      f"alt_ratio={v['alternating_ratio']:.2f}, max_run={v['max_consecutive_l0_run']}, "
                      f"single_char={v['single_char_count']}")

    # Count tokens by classification
    print(f"\nL0 token counts by classification:")
    for cls in ['line_marker', 'standalone_list', 'single_label', 'mixed']:
        folios = [v for v in l0_structure.values() if v['classification'] == cls]
        total_l0 = sum(v['n_l0'] for v in folios)
        print(f"  {cls}: {total_l0} label lines across {len(folios)} folios")

    # ── Save structured data ─────────────────────────────────────────────────
    data_out = {
        'f66r_word_column': word_col_tokens,
        'f66r_char_column': char_col_tokens,
        'f66r_body_top_words': dict(Counter(body_tokens).most_common(20)),
        'word_col_global_freq': {w: global_freq.get(w, 0) for w in word_col_tokens},
        'l0_audit': {f: {k: v for k, v in info.items() if k != 'l0_tokens'}
                    for f, info in l0_structure.items()},
    }
    out_path = Path(__file__).parent / 'data.json'
    with open(out_path, 'w') as fp:
        json.dump(data_out, fp, indent=2, ensure_ascii=False)
    print(f"\nData saved to {out_path}")
    print("\nDone.")
