#!/usr/bin/env python3
"""
Experiment exp_037: Label 'o'-Initial Morpheme Analysis (H033)
58.4% of object labels begin with 'o'. Is this a label-marker prefix,
or does it reflect section-specific vocabulary?
"""
from pathlib import Path as _RepositoryPath

import re, math
from collections import Counter, defaultdict

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

def parse_all(path):
    label_entries = []
    body_entries = []
    current_folio = None
    current_lang = 'unknown'
    current_section = 'unknown'

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            if re.match(r'^<f\w+>', line) and '$' in line:
                mf = re.match(r'^<(f\w+)>', line)
                current_folio = mf.group(1) if mf else current_folio
                ml = re.search(r'\$L=([AB])', line)
                current_lang = ml.group(1) if ml else 'unknown'
                ms = re.search(r'\$I=([A-Z])', line)
                current_section = ms.group(1) if ms else 'unknown'
                continue
            m = re.match(r'^<[^>]+,([^>]+)>\s+(.*)', line)
            if not m: continue
            locus, content = m.group(1).strip(), m.group(2)
            content = re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*', '', content)
            tokens = [t.strip() for t in re.split(r'[., ]+', content)
                      if re.match(r'^[a-z]+$', t.strip()) and len(t.strip()) >= 2]
            base = re.sub(r'^[+*@=/~&]', '', locus)
            info = {'folio': current_folio, 'lang': current_lang, 'section': current_section}
            if base in ('Lf', 'Ls', 'Ln', 'Lt'):
                for t in tokens:
                    label_entries.append({'word': t, **info})
            elif re.match(r'^P[0-9]$', base):
                for t in tokens:
                    body_entries.append({'word': t, **info})
    return label_entries, body_entries

def section_name(c):
    return {'H': 'herbal', 'P': 'pharma', 'A': 'astro', 'B': 'bio', 'Z': 'zodiac'}.get(c, c)

def main():
    labels, body = parse_all(ZL3B)
    print(f"Label tokens: {len(labels)}, body tokens: {len(body)}")

    # 1. Label o-initial bigrams
    o_labels = [e['word'] for e in labels if e['word'].startswith('o')]
    non_o_labels = [e['word'] for e in labels if not e['word'].startswith('o')]

    print(f"\n=== LABEL o-INITIAL BIGRAMS (n={len(o_labels)}) ===")
    o_bigrams = Counter(w[:2] for w in o_labels if len(w) >= 2)
    total_o = len(o_labels)
    print(f"{'Bigram':>8} | {'Count':>6} | {'Pct':>7}")
    for bg, cnt in o_bigrams.most_common(15):
        print(f"  '{bg}' | {cnt:>6} | {100*cnt/total_o:>6.1f}%")

    # 2. Compare body text o-initial bigrams
    o_body = [e['word'] for e in body if e['word'].startswith('o')]
    o_body_bigrams = Counter(w[:2] for w in o_body if len(w) >= 2)
    total_ob = len(o_body)
    print(f"\n=== BODY TEXT o-INITIAL BIGRAMS (n={total_ob}) ===")
    for bg, cnt in o_body_bigrams.most_common(10):
        print(f"  '{bg}' | {cnt:>6} | {100*cnt/total_ob:>6.1f}%")

    # 3. KL divergence label vs body for o-initial bigrams
    all_bgs = sorted(set(list(o_bigrams.keys()) + list(o_body_bigrams.keys())))
    kl = 0.0
    for bg in all_bgs:
        p = o_bigrams.get(bg, 0) / total_o if total_o > 0 else 0
        q = o_body_bigrams.get(bg, 0) / total_ob if total_ob > 0 else 0
        if p > 0 and q > 0:
            kl += p * math.log2(p/q)
    print(f"\nKL(label-o-bigrams || body-o-bigrams) = {kl:.4f} bits")
    print("(0 = identical distributions)")

    # 4. Is o-initial rate section-specific in body?
    print(f"\n=== o-INITIAL RATE BY SECTION (body text) ===")
    section_body = defaultdict(list)
    for e in body:
        section_body[e['section']].append(e['word'])
    for sec in sorted(section_body.keys()):
        words = section_body[sec]
        if len(words) < 50: continue
        o_rate = sum(1 for w in words if w.startswith('o')) / len(words)
        print(f"  {section_name(sec):>8}: {100*o_rate:.1f}% o-initial ({len(words)} words)")

    # 5. Is o-initial rate section-specific in labels?
    print(f"\n=== o-INITIAL RATE BY SECTION (labels) ===")
    section_labels = defaultdict(list)
    for e in labels:
        section_labels[e['section']].append(e['word'])
    for sec in sorted(section_labels.keys()):
        words = section_labels[sec]
        if not words: continue
        o_rate = sum(1 for w in words if w.startswith('o')) / len(words)
        print(f"  {section_name(sec):>8}: {100*o_rate:.1f}% o-initial ({len(words)} label tokens)")

    # 6. Check if o-labels are simply ot-/ok-: break down the bigrams
    print(f"\n=== LABEL o-SECOND-CHAR BREAKDOWN ===")
    o_second = Counter(w[1] for w in o_labels if len(w) >= 2)
    for ch, cnt in o_second.most_common(10):
        print(f"  o+'{ch}': {cnt}x ({100*cnt/total_o:.1f}%)")

    # 7. If 'o' is stripped from labels, what does the distribution look like?
    stripped_o = [w[1:] for w in o_labels if len(w) >= 2]
    stripped_o_init = Counter(w[0] for w in stripped_o if w)
    total_so = len(stripped_o)
    print(f"\n=== LABELS WITH 'o' STRIPPED: NEXT-CHAR DISTRIBUTION ===")
    for ch, cnt in stripped_o_init.most_common(10):
        print(f"  '{ch}': {cnt}x ({100*cnt/total_so:.1f}%)")

    # 8. Do o-stripped label stems appear in body text?
    body_vocab = set(e['word'] for e in body)
    stripped_in_body = [(w, w[1:] in body_vocab) for w in o_labels if len(w) > 1]
    in_body_count = sum(1 for _, b in stripped_in_body if b)
    print(f"\n=== o-STRIPPED LABEL STEMS IN BODY TEXT ===")
    print(f"  {in_body_count}/{len(stripped_in_body)} ({100*in_body_count/len(stripped_in_body):.1f}%) o-stripped stems appear in body vocabulary")

    # Examples
    print("  Examples:")
    for w, b in stripped_in_body[:20]:
        stem = w[1:]
        freq = sum(1 for e in body if e['word'] == stem)
        print(f"    {w} → '{stem}': in body={'YES' if b else 'no'}, body_freq={freq}")

if __name__ == '__main__':
    main()
