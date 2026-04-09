"""
Experiment: exp_010_label_word_sections
Hypothesis tested: H015 — ot-/ok- initial label words cluster in specific manuscript sections
Also tests: whether label vocabulary generally differs across sections (herbal, astro, bio, pharma)
Data: data/transcriptions/eva_zl3b.txt
Dependencies: collections, re (standard library only)
"""

import re
import math
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

# ── Section definitions (folio number ranges per standard classification) ────────
SECTIONS = {
    'herbal_A':    (1, 66),
    'astro':       (67, 73),
    'bio':         (74, 84),
    'pharma':      (85, 102),
    'recipes':     (103, 116),
}

def folio_to_section(folio_num):
    for name, (lo, hi) in SECTIONS.items():
        if lo <= folio_num <= hi:
            return name
    return 'other'

def folio_num_from_locus_line(line):
    """Extract folio number from lines like <f1r.1,La> or <f100v.2,Lb>."""
    m = re.match(r'^<f(\d+)[rv]', line)
    if m:
        return int(m.group(1))
    return None

# ── Parser ────────────────────────────────────────────────────────────────────

def parse_with_section_and_locus(path):
    """
    Returns list of (word, locus_type, section, folio_num) tuples.
    locus_type: 'body', 'label', 'rider', 'circular'
    """
    results = []
    current_folio = None
    current_section = 'other'
    current_currier = None

    LOCUS_MAP = {'P': 'body', 'L': 'label', 'R': 'rider', 'C': 'circular'}

    with open(path, encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Folio header comment
            if line.startswith('#'):
                # Check for Currier language marker: $L=A or $L=B
                m_currier = re.search(r'\$L=([AB])', line)
                if m_currier:
                    current_currier = m_currier.group(1)
                continue

            # Data line
            m = re.match(r'^<([^>]+)>\s+(.*)', line)
            if not m:
                continue
            locus_full = m.group(1)
            text = m.group(2)

            # Extract folio number from locus
            fn = folio_num_from_locus_line('<' + locus_full + '>')
            if fn is not None:
                current_folio = fn
                current_section = folio_to_section(fn)

            # Extract locus type from second part (after comma)
            locus_parts = locus_full.split(',')
            if len(locus_parts) < 2:
                continue
            locus_code = re.sub(r'^[^A-Za-z]+', '', locus_parts[1].strip())
            if not locus_code:
                continue
            locus_type = LOCUS_MAP.get(locus_code[0], 'other')

            # Clean text
            text = re.sub(r'<!.*?>', '', text)
            text = re.sub(r'<[^>]+>', '', text)
            text = text.replace('<%>', '').replace('<$>', '').replace('%', '')
            text = re.sub(r'\[([^:\]]+):[^\]]*\]', r'\1', text)
            text = re.sub(r'\{[^}]*\}', '', text)
            text = re.sub(r'@\d+;?', '', text)
            raw_words = re.split(r'[.\s]+', text)
            for w in raw_words:
                if w and re.match(r'^[a-zA-Z]+$', w):
                    results.append((w, locus_type, current_section, current_folio, current_currier))

    return results


# ── Analysis ──────────────────────────────────────────────────────────────────

def entropy(dist):
    total = sum(dist.values())
    if total == 0:
        return 0.0
    return -sum((v/total) * math.log2(v/total) for v in dist.values() if v > 0)


if __name__ == "__main__":
    print("Experiment exp_010: Label Word Section Distribution")
    print("Date: 2026-04-09\n")

    data = parse_with_section_and_locus(BASE / 'data/transcriptions/eva_zl3b.txt')
    print(f"Total tokens: {len(data):,}")

    # Separate by locus type
    labels = [(w, sec, folio, cur) for w, ltype, sec, folio, cur in data if ltype == 'label']
    body = [(w, sec, folio, cur) for w, ltype, sec, folio, cur in data if ltype == 'body']

    print(f"Label tokens: {len(labels):,}")
    print(f"Body tokens: {len(body):,}")

    # ── 1. ot-/ok- words in labels: which sections? ───────────────────────────
    print(f"\n{'='*60}")
    print("H015: ot-/ok- LABEL WORDS BY SECTION")
    print(f"{'='*60}")

    otok_labels = [(w, sec) for w, sec, folio, cur in labels if w.startswith(('ot', 'ok'))]
    print(f"\nTotal ot-/ok- label tokens: {len(otok_labels):,}")

    otok_by_section = Counter(sec for _, sec in otok_labels)
    total_by_section = Counter(sec for _, sec, folio, cur in labels)

    print(f"\n  {'Section':<15} {'ot/ok count':>12} {'label total':>12} {'% ot/ok':>10}")
    print(f"  {'-'*50}")
    for sec in list(SECTIONS.keys()) + ['other']:
        n_otok = otok_by_section.get(sec, 0)
        n_total = total_by_section.get(sec, 0)
        pct = 100 * n_otok / n_total if n_total > 0 else 0
        print(f"  {sec:<15} {n_otok:>12} {n_total:>12} {pct:>9.1f}%")

    # Specific ot-/ok- words in each section
    print("\n  Top ot-/ok- label words overall:")
    for w, count in Counter(w for w, sec in otok_labels).most_common(15):
        print(f"    {w}: {count}")

    print("\n  ot-/ok- words per section (top 5 each):")
    for sec in SECTIONS.keys():
        sec_words = Counter(w for w, s in otok_labels if s == sec)
        if sec_words:
            print(f"  {sec}: {sec_words.most_common(5)}")
        else:
            print(f"  {sec}: (none)")

    # ── 2. Full label vocabulary comparison by section ───────────────────────
    print(f"\n{'='*60}")
    print("LABEL VOCABULARY BY SECTION")
    print(f"{'='*60}")

    for sec in list(SECTIONS.keys()) + ['other']:
        sec_labels = [w for w, s, folio, cur in labels if s == sec]
        if len(sec_labels) < 5:
            continue
        types = len(set(sec_labels))
        tokens = len(sec_labels)
        top = Counter(sec_labels).most_common(8)
        print(f"\n  {sec}: {tokens} tokens, {types} types (TTR={types/tokens:.3f})")
        print(f"    Top: {[w for w,_ in top]}")

    # ── 3. Comparison: body vs label ot-/ok- frequency per section ───────────
    print(f"\n{'='*60}")
    print("ot-/ok- WORDS IN BODY TEXT BY SECTION")
    print(f"{'='*60}")

    otok_body = [(w, sec) for w, sec, folio, cur in body if w.startswith(('ot', 'ok'))]
    body_by_section = Counter(sec for _, sec, folio, cur in body)
    otok_body_by_section = Counter(sec for _, sec in otok_body)

    print(f"\n  {'Section':<15} {'ot/ok count':>12} {'body total':>12} {'% ot/ok':>10}")
    print(f"  {'-'*50}")
    for sec in list(SECTIONS.keys()) + ['other']:
        n_otok = otok_body_by_section.get(sec, 0)
        n_total = body_by_section.get(sec, 0)
        pct = 100 * n_otok / n_total if n_total > 0 else 0
        print(f"  {sec:<15} {n_otok:>12} {n_total:>12} {pct:>9.1f}%")

    # ── 4. Label word overlap between sections ────────────────────────────────
    print(f"\n{'='*60}")
    print("LABEL VOCABULARY OVERLAP BETWEEN SECTIONS")
    print(f"{'='*60}")

    section_vocab = {}
    for sec in SECTIONS.keys():
        sec_labels = [w for w, s, folio, cur in labels if s == sec]
        section_vocab[sec] = set(sec_labels)

    print("\n  Shared types between pairs of sections:")
    secs = list(SECTIONS.keys())
    for i in range(len(secs)):
        for j in range(i+1, len(secs)):
            a, b = secs[i], secs[j]
            shared = section_vocab.get(a, set()) & section_vocab.get(b, set())
            sa = len(section_vocab.get(a, set()))
            sb = len(section_vocab.get(b, set()))
            print(f"  {a} ∩ {b}: {len(shared)} shared ({100*len(shared)/max(sa,1):.0f}% of {a}, {100*len(shared)/max(sb,1):.0f}% of {b})")

    print("\nDone.")
