"""
Experiment: exp_014_prior_work_check
Goal: Review prior work on f66r, f49v, f76r, and f57v.
- Query KB summaries and folio entries
- Check for existing analysis of line markers, key-like sequences, or alphabet inventory
- Document what is and is not covered in prior literature
Data: ~/voynich-kb/summaries/, ~/voynich-kb/folios/
"""

import os
import re
from pathlib import Path

KB = Path(os.path.expanduser('~/voynich-kb'))
SUMMARIES = KB / 'summaries'
FOLIOS = KB / 'folios'

TARGET_FOLIOS = ['f49v', 'f57v', 'f66r', 'f76r']
SEARCH_TERMS = [
    'key-like', 'key like', 'line marker', 'margin marker', 'marginal notation',
    'f49v', 'f57v', 'f66r', 'f76r', 'alphabet inventory', 'cipher key',
    '@169', '@172', '@195', 'special glyph'
]


def search_file(path, terms):
    """Return list of (term, line_number, line) for each term found."""
    results = []
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
        lines = text.splitlines()
        for i, line in enumerate(lines, 1):
            for term in terms:
                if term.lower() in line.lower():
                    results.append((term, i, line.strip()))
    except Exception:
        pass
    return results


if __name__ == "__main__":
    print("Experiment exp_014: Prior Work Check")
    print("Date: 2026-04-09\n")

    # 1. KB folio pages for target folios
    print("=" * 60)
    print("KB FOLIO ENTRIES")
    print("=" * 60)
    for folio in TARGET_FOLIOS:
        p = FOLIOS / f'{folio}.md'
        if p.exists():
            text = p.read_text(encoding='utf-8', errors='ignore')
            print(f"\n{folio}: EXISTS ({len(text)} bytes)")
            # Print anomalies and visual_anomaly_notes
            for line in text.splitlines():
                if any(k in line for k in ['anomal', 'section:', 'primary_subject:']):
                    print(f"  {line.strip()}")
        else:
            print(f"\n{folio}: NOT FOUND in KB folios")

    # 2. Search all summaries for target terms
    print("\n" + "=" * 60)
    print("SUMMARY SEARCH RESULTS")
    print("=" * 60)
    summary_hits = {}
    for p in sorted(SUMMARIES.glob('*.md')):
        hits = search_file(p, SEARCH_TERMS)
        if hits:
            summary_hits[p.name] = hits

    for fname, hits in sorted(summary_hits.items()):
        print(f"\n{fname}:")
        seen = set()
        for term, lineno, line in hits:
            key = (lineno, line[:80])
            if key not in seen:
                seen.add(key)
                print(f"  L{lineno}: {line[:100]}")

    print(f"\nTotal summaries with hits: {len(summary_hits)}")
    print("Done.")
