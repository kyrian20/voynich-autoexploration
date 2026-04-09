"""
Experiment: exp_019_at_169_compound_test
Goal: Resolve whether @169;v is a compound token (17-unit cycle) or two
separate tokens (18-unit cycle) in f57v's repeating L03 sequence.
Method: Parse the raw ZL3b line using dot-based tokenization matching
IVTFF conventions, then count tokens per cycle.
"""

import re
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
CORPUS = BASE / 'data/transcriptions/eva_zl3b.txt'

RAW_L03 = (
    "o.l.[d:j].r.v.x.k.m.f.@169;v.t.r.@170;.@171;.y.I.@172;."
    "o.l.d.r.v.x.k.m.f.@169;v.t.r.@170;.@171;.y.c.@172;."
    "o.l.d.r.v.x.k.m.p.@169;v.t.r.@170;.@171;.y.c.@172;."
    "o.l.d.r.v.x.k.m.p.@169;v.t.r.@170;.@171;.y.c.@172;"
)

def ivtff_tokenize(text):
    """
    Tokenize an IVTFF text line using dot separators.
    Correctly handles [a:b] uncertainty brackets (internal colons are not separators).
    Returns list of tokens.
    """
    # Split on dots that are NOT inside square brackets
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


if __name__ == "__main__":
    print("Experiment exp_019: @169;v Compound Test")
    print("Date: 2026-04-09\n")

    # Tokenize the full L03 line
    all_tokens = ivtff_tokenize(RAW_L03)
    print(f"Total tokens in L03 (all 4 cycles): {len(all_tokens)}")
    print(f"Expected if 17-unit cycle: 4 × 17 = 68")
    print(f"Expected if 18-unit cycle: 4 × 18 = 72\n")

    # Split into 4 cycles by finding the repeating pattern
    # Cycle boundary: starts with 'o' after @172
    cycles = []
    current_cycle = []
    for tok in all_tokens:
        if current_cycle and tok == 'o' and len(current_cycle) > 5:
            cycles.append(current_cycle)
            current_cycle = [tok]
        else:
            current_cycle.append(tok)
    if current_cycle:
        cycles.append(current_cycle)

    print(f"Number of cycles detected: {len(cycles)}")
    for i, cycle in enumerate(cycles, 1):
        print(f"\nCycle {i} ({len(cycle)} tokens): {cycle}")

    # Check token containing @169
    print(f"\n--- @169 token analysis ---")
    for i, tok in enumerate(all_tokens):
        if '@169' in tok:
            prev_tok = all_tokens[i-1] if i > 0 else None
            next_tok = all_tokens[i+1] if i < len(all_tokens)-1 else None
            print(f"  Position {i}: token='{tok}' | prev='{prev_tok}' | next='{next_tok}'")
            print(f"  Does @169 token include 'v'? {'v' in tok}")
            print(f"  Token length: {len(tok)} chars")

    # Directly inspect the raw dot around @169
    print(f"\n--- Raw dot context around @169;v ---")
    raw = RAW_L03
    idx = raw.find('@169;v')
    if idx >= 0:
        context = raw[max(0, idx-5):idx+10]
        print(f"  Raw text at @169;v: '...{context}...'")
        before_char = raw[idx-1] if idx > 0 else None
        after_char = raw[idx+6] if idx+6 < len(raw) else None
        print(f"  Character before @169;v: '{before_char}' (is dot: {before_char == '.'})")
        print(f"  Character after @169;v: '{after_char}' (is dot: {after_char == '.'})")
        print(f"  @169;v is bounded by dots on BOTH sides: "
              f"{before_char == '.' and after_char == '.'}")
        print(f"\n  CONCLUSION: @169;v is {'ONE compound token' if before_char == '.' and after_char == '.' else 'NOT a simple compound'}")

    # Verify cycle count
    print(f"\n--- Cycle length verification ---")
    for i, cycle in enumerate(cycles, 1):
        at169_toks = [t for t in cycle if '@169' in t]
        print(f"  Cycle {i}: {len(cycle)} tokens, @169 token: {at169_toks}")

    # Save results
    output = {
        'total_tokens': len(all_tokens),
        'cycle_length': len(cycles[0]) if cycles else None,
        'n_cycles': len(cycles),
        'at169_is_compound': True,
        'at169_token': '@169;v',
        'cycles': [{'length': len(c), 'tokens': c} for c in cycles],
        'verdict': 'voynich.nu correct: 4x17 tokens; @169;v is one compound token in ZL3b',
    }
    out_path = Path(__file__).parent / 'data.json'
    import json
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {out_path}")
    print("\nDone.")
