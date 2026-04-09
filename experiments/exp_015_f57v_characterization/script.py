"""
Experiment: exp_015_f57v_characterization
Goal: Complete characterization of f57v transcription and @glyph structure.
- Extract full f57v transcription from ZL3b
- Characterize all locus types (P0, L0, Cc, etc.)
- Map @glyph positions within circular text
- Compare f57v @glyphs to f66r column 2 @glyphs in immediate context
Data: data/transcriptions/eva_zl3b.txt
Output: data.json with full transcription and structured @glyph data
"""

import re
import json
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
CORPUS = BASE / 'data/transcriptions/eva_zl3b.txt'

# F66r column 2 @glyphs for comparison (from exp_012)
F66R_SPECIALS = {'@169', '@172', '@195'}

# All known @glyphs across manuscript cluster
CLUSTER_SPECIALS = {'@169', '@170', '@171', '@172', '@195'}


def extract_folio_raw(path, folio_str):
    """Extract all raw lines from a folio."""
    lines = []
    in_folio = False
    header = None
    with open(path, encoding='latin-1') as f:
        for raw_line in f:
            stripped = raw_line.strip()
            if f'<{folio_str}>' in stripped:
                in_folio = True
                header = stripped
                continue
            if in_folio:
                if re.match(r'^<f\d+', stripped) and f'<{folio_str}.' not in stripped:
                    break
                if not stripped or stripped.startswith('#'):
                    if stripped.startswith('#'):
                        lines.append({'type': 'comment', 'raw': stripped})
                    continue
                m = re.match(rf'^<{re.escape(folio_str)}\.(\d+),([^>]+)>\s*(.*)', stripped)
                if m:
                    linenum = int(m.group(1))
                    locus_raw = m.group(2)
                    text = m.group(3).strip()
                    lines.append({
                        'linenum': linenum,
                        'locus_raw': locus_raw,
                        'text': text,
                        'raw': stripped,
                    })
    return header, lines


def parse_locus(locus_raw):
    """Parse locus code: extract prefix (*, @, =, !) and base (P0, L0, Cc, etc.)"""
    m = re.match(r'^([*@!=]?)(.+)$', locus_raw)
    if m:
        return m.group(1), m.group(2)
    return '', locus_raw


def extract_at_glyphs_from_text(text):
    """Extract all @NNN occurrences with positions."""
    # Pattern: @NNN or @NNN;
    return re.findall(r'@\d+;?', text)


def clean_text_for_analysis(text):
    """Remove markup, keep EVA chars and @glyphs."""
    text = re.sub(r'<!.*?>', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('<%>', '').replace('<$>', '').replace('%', '')
    text = re.sub(r'\[([^:\]]+):[^\]]*\]', r'\1', text)
    text = re.sub(r'\{[^}]*\}', '', text)
    return text


def get_context(text, at_glyph, window=3):
    """Get characters before and after an @glyph occurrence."""
    # Tokenize by dots/spaces
    tokens = re.split(r'[.\s]+', text)
    contexts = []
    for i, tok in enumerate(tokens):
        normalized = re.sub(r';$', '', tok)
        if normalized == at_glyph or tok.startswith(at_glyph.rstrip(';')):
            before = tokens[max(0, i-window):i]
            after = tokens[i+1:i+1+window]
            contexts.append({'before': before, 'glyph': tok, 'after': after, 'pos': i})
    return contexts


if __name__ == "__main__":
    print("Experiment exp_015: f57v Characterization")
    print("Date: 2026-04-09\n")

    header, lines = extract_folio_raw(CORPUS, 'f57v')
    print(f"ZL3b header: {header}")
    print(f"Total lines: {len(lines)}\n")

    # Categorize by locus
    locus_counts = defaultdict(list)
    all_at_glyphs = []
    all_at_glyph_contexts = defaultdict(list)

    data_entries = []
    for entry in lines:
        if entry.get('type') == 'comment':
            data_entries.append(entry)
            continue
        prefix, base = parse_locus(entry['locus_raw'])
        locus_counts[base].append(entry)
        clean = clean_text_for_analysis(entry['text'])
        at_glyphs = extract_at_glyphs_from_text(clean)
        normalized_glyphs = [re.sub(r';$', '', g) for g in at_glyphs]
        all_at_glyphs.extend(normalized_glyphs)
        for g in normalized_glyphs:
            ctx = get_context(clean, g)
            all_at_glyph_contexts[g].extend(ctx)

        data_entries.append({
            **entry,
            'locus_prefix': prefix,
            'locus_base': base,
            'clean_text': clean,
            'at_glyphs': normalized_glyphs,
        })

    # Print locus summary
    print("--- Locus type summary ---")
    for base, elist in sorted(locus_counts.items()):
        print(f"  {base}: {len(elist)} lines")

    # Print all entries
    print("\n--- Full transcription ---")
    for e in data_entries:
        if e.get('type') == 'comment':
            print(f"  {e['raw']}")
        else:
            at_note = f" [@GLYPHS: {e['at_glyphs']}]" if e['at_glyphs'] else ""
            print(f"  L{e['linenum']:02d} [{e['locus_raw']}]: {e['text']}{at_note}")

    # @glyph summary
    print(f"\n--- @glyph occurrences in f57v ---")
    at_freq = Counter(all_at_glyphs)
    print(f"Total @glyph tokens: {len(all_at_glyphs)}")
    print(f"Distinct @glyphs: {sorted(at_freq.keys())}")
    for g, cnt in sorted(at_freq.items()):
        print(f"  {g}: ×{cnt}")

    # Context for each @glyph
    print(f"\n--- @glyph immediate contexts (within circular text) ---")
    for g in sorted(all_at_glyph_contexts.keys()):
        ctxs = all_at_glyph_contexts[g]
        print(f"\n  {g} (×{len(ctxs)} occurrences):")
        for ctx in ctxs:
            before_str = '.'.join(ctx['before'][-3:]) if ctx['before'] else '(start)'
            after_str = '.'.join(ctx['after'][:3]) if ctx['after'] else '(end)'
            print(f"    ...{before_str} → [{g}] → {after_str}...")

    # f66r comparison
    print(f"\n--- f66r vs f57v @glyph comparison ---")
    f57v_glyphs = set(at_freq.keys())
    print(f"f57v @glyphs: {sorted(f57v_glyphs)}")
    print(f"f66r @glyphs: {sorted(F66R_SPECIALS)}")
    shared = f57v_glyphs & F66R_SPECIALS
    only_57v = f57v_glyphs - F66R_SPECIALS
    only_66r = F66R_SPECIALS - f57v_glyphs
    print(f"Shared: {sorted(shared)}")
    print(f"Only in f57v: {sorted(only_57v)}")
    print(f"Only in f66r: {sorted(only_66r)}")

    # Save data.json
    output_path = Path(__file__).parent / 'data.json'
    output = {
        'folio': 'f57v',
        'header': header,
        'entries': data_entries,
        'locus_summary': {k: len(v) for k, v in locus_counts.items()},
        'at_glyph_frequency': dict(at_freq),
        'at_glyph_contexts': {k: v for k, v in all_at_glyph_contexts.items()},
        'f66r_comparison': {
            'f57v_glyphs': sorted(f57v_glyphs),
            'f66r_glyphs': sorted(F66R_SPECIALS),
            'shared': sorted(shared),
            'only_57v': sorted(only_57v),
            'only_66r': sorted(only_66r),
        }
    }
    with open(output_path, 'w') as fout:
        json.dump(output, fout, indent=2)
    print(f"\nSaved data to {output_path}")
    print("\nDone.")
