#!/usr/bin/env python3
"""
Experiment exp_032: Complete Label Locus Audit (H021 completion)
Audits all non-L0 label loci: Lz, Lf, Ls, Lc, Ln, Lt, La, Lp, Lx
Questions:
 1. How many entries per locus type?
 2. Are there LINE_MARKER or LIST_ENTRY contamination patterns?
 3. What is the vocabulary and entropy of each label type?
"""

import re
import math
from collections import Counter, defaultdict

ZL3B = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

def parse_all_entries(path):
    """Parse all locus-coded entries from ZL3b."""
    entries = []
    current_folio = None
    current_lang = 'unknown'
    current_hand = 'unknown'
    current_section = 'unknown'

    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            # Folio header
            if re.match(r'^<f\w+>', line) and '$' in line:
                m_folio = re.match(r'^<(f\w+)>', line)
                if m_folio:
                    current_folio = m_folio.group(1)
                m_lang = re.search(r'\$L=([AB])', line)
                current_lang = m_lang.group(1) if m_lang else 'unknown'
                m_hand = re.search(r'\$H=(\d+)', line)
                current_hand = m_hand.group(1) if m_hand else 'unknown'
                m_sec = re.search(r'\$I=([A-Z])', line)
                current_section = m_sec.group(1) if m_sec else 'unknown'
                continue
            # Regular locus entry
            m = re.match(r'^<[^>]+\.(\d+),([^>]+)>\s+(.*)', line)
            if m:
                line_num = int(m.group(1))
                locus = m.group(2).strip()
                content = m.group(3).strip()
                entries.append({
                    'folio': current_folio,
                    'line_num': line_num,
                    'locus': locus,
                    'content': content,
                    'lang': current_lang,
                    'hand': current_hand,
                    'section': current_section,
                })
    return entries

def locus_base(locus):
    """Return base locus code (without prefix character)."""
    return re.sub(r'^[+*@=/~&]', '', locus)

def clean_content(content):
    """Clean IVTFF markup from content."""
    content = re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]', '', content)
    content = re.sub(r'@\d+;[a-z]*', 'SPECIAL', content)
    return content.strip()

def tokenize(content):
    """Extract word tokens from cleaned content."""
    content = clean_content(content)
    tokens = []
    for part in re.split(r'[.,\s]+', content):
        part = part.strip().strip(',').strip()
        if part and part != 'SPECIAL' and len(part) >= 1:
            if re.match(r'^[a-zA-Z\']+$', part):
                tokens.append(part.lower())
    return tokens

def entropy(counter):
    total = sum(counter.values())
    if total == 0: return 0.0
    return -sum((v/total)*math.log2(v/total) for v in counter.values() if v > 0)

def h2_from_words(word_list):
    """Bigram conditional entropy."""
    bigrams = Counter()
    unigrams = Counter()
    for w in word_list:
        for i in range(len(w)-1):
            bigrams[(w[i], w[i+1])] += 1
            unigrams[w[i]] += 1
    if not bigrams: return 0.0
    total = sum(bigrams.values())
    h = 0.0
    for (a, b), cnt in bigrams.items():
        p_ab = cnt / total
        p_b_given_a = cnt / unigrams[a]
        h -= p_ab * math.log2(p_b_given_a)
    return h

def main():
    entries = parse_all_entries(ZL3B)
    print(f"Total entries parsed: {len(entries)}")

    # Group by base locus
    by_base = defaultdict(list)
    for e in entries:
        base = locus_base(e['locus'])
        by_base[base].append(e)

    # Summary of all label-type loci
    label_bases = ['L0', 'Lf', 'Lz', 'Ls', 'Lc', 'Ln', 'Lt', 'La', 'Lp', 'Lx']

    print("\n=== LOCUS TYPE SUMMARY ===")
    print(f"{'Locus':>5} | {'Count':>6} | {'Folios':>7} | {'Sections':>20} | {'Notes'}")
    print("-" * 80)
    for base in label_bases:
        elist = by_base.get(base, [])
        if not elist: continue
        folio_set = set(e['folio'] for e in elist)
        section_counts = Counter(e['section'] for e in elist)
        top_sections = '/'.join(f"{k}:{v}" for k,v in section_counts.most_common(3))
        print(f"  {base:>5} | {len(elist):>6} | {len(folio_set):>7} | {top_sections:>20}")

    # Detailed audit of each major label type
    for base in ['Lf', 'Lz', 'Ls', 'Lc', 'Ln', 'Lt']:
        elist = by_base.get(base, [])
        if not elist: continue

        print(f"\n{'='*60}")
        print(f"=== {base} LABEL AUDIT ({len(elist)} entries) ===")

        # Check for LINE_MARKER pattern: Lx entry adjacent to Px entry
        # In general, line markers are single-char entries in alternating L/P loci
        # Count single-char entries
        single_char = [e for e in elist if len(clean_content(e['content'])) == 1
                        and re.match(r'^[a-zA-Z@]', clean_content(e['content']))]
        multi_word = [e for e in elist if len(tokenize(e['content'])) >= 2]
        empty_or_special = [e for e in elist if not clean_content(e['content'])
                             or clean_content(e['content']) in ('SPECIAL', '')]

        print(f"  Single-char entries: {len(single_char)} ({100*len(single_char)/len(elist):.1f}%)")
        print(f"  Multi-word entries:  {len(multi_word)} ({100*len(multi_word)/len(elist):.1f}%)")

        # Vocabulary
        all_tokens = []
        for e in elist:
            all_tokens.extend(tokenize(e['content']))

        vocab = set(all_tokens)
        token_counter = Counter(all_tokens)
        hapax = sum(1 for v in token_counter.values() if v == 1)
        ttr = len(vocab) / len(all_tokens) if all_tokens else 0

        print(f"  Total tokens: {len(all_tokens)}, types: {len(vocab)}, hapax: {hapax}")
        print(f"  TTR: {ttr:.3f}, hapax rate: {100*hapax/len(vocab):.1f}%")
        if all_tokens:
            h2_val = h2_from_words(all_tokens)
            print(f"  H2: {h2_val:.3f} bits")

        # Top words
        print(f"  Top 10 words:")
        for w, cnt in token_counter.most_common(10):
            print(f"    '{w}': {cnt}x")

        # Section distribution
        section_counts = Counter(e['section'] for e in elist)
        print(f"  Section distribution:")
        for sec, cnt in section_counts.most_common():
            print(f"    {sec}: {cnt} ({100*cnt/len(elist):.1f}%)")

        # Folio distribution (top 10)
        folio_counts = Counter(e['folio'] for e in elist)
        print(f"  Top 10 folios:")
        for f, cnt in folio_counts.most_common(10):
            print(f"    {f}: {cnt}")

        # Sample entries
        print(f"  Sample entries (first 8):")
        for e in elist[:8]:
            print(f"    [{e['folio']} {e['locus']}] {e['content'][:80]}")

    # Lz special: zodiac month names
    print(f"\n{'='*60}")
    print("=== Lz SPECIAL ANALYSIS (zodiac labels) ===")
    lz_entries = by_base.get('Lz', [])
    # The zodiac month names are non-Voynich — check content patterns
    non_voynich = [e for e in lz_entries if re.search(r'[A-Z][a-z]{2,}|[a-z]{4,}[aeiou]s$', e['content'])]
    voynich_like = [e for e in lz_entries if not re.search(r'[A-Z]', e['content'])
                    and re.search(r'[a-z]', e['content'])]
    print(f"  Entries with month-name patterns (Romance language): {len(non_voynich)}")
    print(f"  Voynich-like entries: {len(voynich_like)}")
    print("  Sample non-Voynich Lz content:")
    for e in non_voynich[:8]:
        print(f"    [{e['folio']}] '{e['content']}'")
    print("  Sample Voynich Lz content:")
    for e in voynich_like[:8]:
        print(f"    [{e['folio']}] '{e['content']}'")

    # Cross-comparison: h2 across label types vs body text
    print(f"\n{'='*60}")
    print("=== H2 COMPARISON ACROSS LABEL TYPES ===")
    print("(Reference: body text H2 ≈ 2.06, labels L0 TRUE_LABEL ≈ 2.5)")

    # Body text
    body_tokens = []
    for e in entries:
        if re.match(r'^[+*@=/~&]?P[0-9]$', e['locus']):
            body_tokens.extend(tokenize(e['content']))
    print(f"  Body text (P0): H2 = {h2_from_words(body_tokens):.3f} bits ({len(body_tokens)} tokens)")

    for base in label_bases:
        elist = by_base.get(base, [])
        if not elist: continue
        tokens = []
        for e in elist:
            tokens.extend(tokenize(e['content']))
        if len(tokens) < 20: continue
        h2_val = h2_from_words(tokens)
        print(f"  {base}: H2 = {h2_val:.3f} bits ({len(tokens)} tokens)")

if __name__ == '__main__':
    main()
