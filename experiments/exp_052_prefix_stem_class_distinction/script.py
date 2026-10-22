"""
exp_052: Three-Prefix System Stem-Class Distinction (H058)
qo- and o- both select k/t-initial stems (F055).
cth- selects o/y/e-initial stems (F047).
H058: Do these stem classes have different suffix distributions,
suggesting different grammatical categories?
If yes: k/t-initial stems and o/y/e-initial stems are distinct grammatical classes
in Voynichese morphology.
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

SUFFIX_LIST = ['aiin', 'ain', 'eedy', 'edy', 'chy', 'eey', 'dy', 'ey', 'y', 'ol', 'or', 'al', 'ar', 'iin', 'in']

def is_body_locus(locus_code):
    base = locus_code.lstrip('+*@=/~&')
    return base.startswith('P')

def clean_text(text):
    text = re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)
    return text

def suffix_group(word):
    for suf in SUFFIX_LIST:
        if word.endswith(suf) and len(word) > len(suf):
            return suf
    return None

def strip_suffix(word):
    for suf in SUFFIX_LIST:
        if word.endswith(suf) and len(word) > len(suf):
            return word[:-len(suf)], suf
    return word, None

def parse_corpus(path):
    """Parse body text words per Currier dialect."""
    words_a = []
    words_b = []
    current_currier = None

    with open(path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue

            m_c = re.search(r'\$L=([AB])', line)
            if m_c:
                current_currier = m_c.group(1)

            m = re.match(r'^<([^>]+)>', line)
            if not m:
                continue
            locus_raw = m.group(1)
            parts = locus_raw.split(',')
            if len(parts) < 2:
                continue
            locus_code = parts[1].strip()

            if not is_body_locus(locus_code):
                continue

            text = line[m.end():].strip()
            text = clean_text(text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]

            if current_currier == 'A':
                words_a.extend(tokens)
            elif current_currier == 'B':
                words_b.extend(tokens)

    return words_a, words_b

def suffix_distribution(words):
    """Return normalized suffix distribution."""
    counts = Counter()
    for w in words:
        sg = suffix_group(w)
        if sg:
            counts[sg] += 1
    total = sum(counts.values())
    return {k: v/total for k, v in counts.items()}, total

def kl_divergence(p_dist, q_dist, vocab):
    """KL(P||Q) over shared vocabulary."""
    kl = 0.0
    for k in vocab:
        p = p_dist.get(k, 0.0)
        q = q_dist.get(k, 0.0)
        if p > 0 and q > 0:
            kl += p * (p / q)  # Note: KL uses log; this is wrong
    # Actually implement correctly:
    kl = 0.0
    import math
    for k in vocab:
        p = p_dist.get(k, 1e-10)
        q = q_dist.get(k, 1e-10)
        if p > 1e-9:
            kl += p * math.log2(p / q)
    return kl

def print_suffix_comparison(name1, dist1, n1, name2, dist2, n2, suffixes=None):
    if suffixes is None:
        suffixes = sorted(set(dist1) | set(dist2), key=lambda s: -(dist1.get(s,0)+dist2.get(s,0)))
    print(f"\n{'Suffix':<10} {name1:>15} {name2:>15}")
    for suf in suffixes:
        r1 = dist1.get(suf, 0.0)
        r2 = dist2.get(suf, 0.0)
        print(f"{'-'+suf:<10} {100*r1:>14.1f}% {100*r2:>14.1f}%")
    print(f"{'(N)':>10} {n1:>15} {n2:>15}")

def main():
    words_a, words_b = parse_corpus(DATA_PATH)
    print(f"Currier A: {len(words_a)} tokens, Currier B: {len(words_b)} tokens")

    # === Define the three stem classes ===
    # Class 1: qo-stripped stems (k/t-initial) from Currier B — the "qo-class"
    # Class 2: cth-stripped stems (o/y/e-initial) from Currier A — the "cth-class"
    # Class 3: bare k/t-initial words (not prefixed) in Currier B — baseline for class 1
    # Class 4: bare o/y/e-initial words (not prefixed) in Currier A — baseline for class 2

    # qo-class: stem words after stripping qo-
    qo_stems_words = []  # the qo+stem form (full word)
    for w in words_b:
        if w.startswith('qo') and len(w) > 2:
            qo_stems_words.append(w)  # keep full word for suffix analysis

    # cth-class: full words starting with cth
    cth_words = [w for w in words_a if w.startswith('cth') and len(w) > 3]

    # Bare k/t-initial words in B (not qo-prefixed)
    kt_bare_b = [w for w in words_b if not w.startswith('qo') and w[0] in 'kt']
    # Bare o/y/e-initial words in A (not cth-prefixed)
    oye_bare_a = [w for w in words_a if not w.startswith('cth') and w[0] in 'oye']
    # All other words in B (not qo-prefixed, not k/t-initial)
    other_b = [w for w in words_b if not w.startswith('qo') and w[0] not in 'kt']
    # All other words in A (not cth-prefixed, not o/y/e-initial)
    other_a = [w for w in words_a if not w.startswith('cth') and w[0] not in 'oye']

    print(f"\nClass sizes:")
    print(f"  qo-prefix words (B): {len(qo_stems_words)}")
    print(f"  cth-prefix words (A): {len(cth_words)}")
    print(f"  bare k/t-initial words (B, no qo): {len(kt_bare_b)}")
    print(f"  bare o/y/e-initial words (A, no cth): {len(oye_bare_a)}")
    print(f"  other words (B, no qo, no k/t): {len(other_b)}")
    print(f"  other words (A, no cth, no o/y/e): {len(other_a)}")

    # === Suffix distributions for each class ===
    suffixes_to_show = ['aiin', 'ain', 'eedy', 'edy', 'eey', 'ey', 'y', 'dy', 'ol', 'or', 'chy', 'al', 'ar', 'iin', 'in']

    qo_dist, qo_n = suffix_distribution(qo_stems_words)
    cth_dist, cth_n = suffix_distribution(cth_words)
    kt_bare_dist, kt_bare_n = suffix_distribution(kt_bare_b)
    oye_bare_dist, oye_bare_n = suffix_distribution(oye_bare_a)
    other_b_dist, other_b_n = suffix_distribution(other_b)
    other_a_dist, other_a_n = suffix_distribution(other_a)
    all_b_dist, all_b_n = suffix_distribution(words_b)
    all_a_dist, all_a_n = suffix_distribution(words_a)

    print(f"\n{'='*80}")
    print("SUFFIX DISTRIBUTIONS BY STEM CLASS")
    print(f"{'='*80}")
    print(f"\n{'Suffix':<10} {'qo-words(B)':>12} {'kt-bare(B)':>12} {'other(B)':>12} {'all-B':>10}")
    for suf in suffixes_to_show:
        r_qo = qo_dist.get(suf, 0.0)
        r_kt = kt_bare_dist.get(suf, 0.0)
        r_oth = other_b_dist.get(suf, 0.0)
        r_all = all_b_dist.get(suf, 0.0)
        print(f"-{suf:<9} {100*r_qo:>11.1f}% {100*r_kt:>11.1f}% {100*r_oth:>11.1f}% {100*r_all:>9.1f}%")
    print(f"{'N':>10} {qo_n:>12} {kt_bare_n:>12} {other_b_n:>12} {all_b_n:>10}")

    print(f"\n{'Suffix':<10} {'cth-words(A)':>12} {'oye-bare(A)':>12} {'other(A)':>12} {'all-A':>10}")
    for suf in suffixes_to_show:
        r_cth = cth_dist.get(suf, 0.0)
        r_oye = oye_bare_dist.get(suf, 0.0)
        r_oth = other_a_dist.get(suf, 0.0)
        r_all = all_a_dist.get(suf, 0.0)
        print(f"-{suf:<9} {100*r_cth:>11.1f}% {100*r_oye:>11.1f}% {100*r_oth:>11.1f}% {100*r_all:>9.1f}%")
    print(f"{'N':>10} {cth_n:>12} {oye_bare_n:>12} {other_a_n:>12} {all_a_n:>10}")

    # === KL divergence between stem classes ===
    import math
    all_suffixes = set(suffixes_to_show)
    print(f"\n{'='*60}")
    print("KL DIVERGENCES (bits) BETWEEN STEM CLASSES")
    print(f"{'='*60}")

    def kl(p, q):
        kl_val = 0.0
        for k in all_suffixes:
            pv = p.get(k, 1e-10)
            qv = q.get(k, 1e-10)
            if pv > 1e-9:
                kl_val += pv * math.log2(pv / qv)
        return kl_val

    print(f"KL(qo-words || all-B):           {kl(qo_dist, all_b_dist):.3f} bits")
    print(f"KL(cth-words || all-A):           {kl(cth_dist, all_a_dist):.3f} bits")
    print(f"KL(qo-words || cth-words):        {kl(qo_dist, cth_dist):.3f} bits")
    print(f"KL(kt-bare || qo-words):          {kl(kt_bare_dist, qo_dist):.3f} bits")
    print(f"KL(oye-bare || cth-words):        {kl(oye_bare_dist, cth_dist):.3f} bits")
    print(f"KL(qo-words || kt-bare):          {kl(qo_dist, kt_bare_dist):.3f} bits")
    print(f"KL(cth-words || oye-bare):        {kl(cth_dist, oye_bare_dist):.3f} bits")
    print(f"KL(all-A || all-B):               {kl(all_a_dist, all_b_dist):.3f} bits")

    # === Which suffixes distinguish qo- from cth-? ===
    print(f"\n{'='*60}")
    print("MOST DISTINCTIVE SUFFIXES: qo-words (B) vs cth-words (A)")
    print(f"{'='*60}")
    diffs = []
    for suf in suffixes_to_show:
        r_qo = qo_dist.get(suf, 0.0)
        r_cth = cth_dist.get(suf, 0.0)
        diffs.append((suf, r_qo, r_cth, r_qo - r_cth))
    diffs.sort(key=lambda x: -abs(x[3]))
    print(f"{'Suffix':<10} {'qo-words(B)':>12} {'cth-words(A)':>12} {'diff':>10}")
    for suf, rq, rc, diff in diffs:
        print(f"-{suf:<9} {100*rq:>11.1f}% {100*rc:>11.1f}% {100*diff:>+9.1f}%")

    # === Cross-class comparison: k/t-initial words in B have qo- preference ===
    print(f"\n{'='*60}")
    print("CROSS-CLASS COMPARISON: How distinctive is qo-prefix within k/t-stems?")
    print(f"{'='*60}")
    # How many k-initial words in B start with qo-? (vs bare k/t)
    k_initial_b = [w for w in words_b if w[0] == 'k']
    t_initial_b = [w for w in words_b if w[0] == 't']
    qok_words = [w for w in words_b if w.startswith('qok')]
    qot_words = [w for w in words_b if w.startswith('qot')]

    print(f"k-initial words in B: {len(k_initial_b)}")
    print(f"  qok- prefixed: {len(qok_words)} ({100*len(qok_words)/max(1,len(k_initial_b)):.1f}%)")
    print(f"  bare k-initial: {len(k_initial_b)-len(qok_words)} ({100*(1-len(qok_words)/max(1,len(k_initial_b))):.1f}%)")
    print(f"t-initial words in B: {len(t_initial_b)}")
    print(f"  qot- prefixed: {len(qot_words)} ({100*len(qot_words)/max(1,len(t_initial_b)):.1f}%)")
    print(f"  bare t-initial: {len(t_initial_b)-len(qot_words)} ({100*(1-len(qot_words)/max(1,len(t_initial_b))):.1f}%)")

    # Top bare k-initial words in B (without qo-)
    bare_k_b_counts = Counter(w for w in words_b if w[0] == 'k' and not w.startswith('qo'))
    print(f"\nTop bare k-initial words in B (without qo-):")
    for w, c in bare_k_b_counts.most_common(10):
        sg = suffix_group(w)
        print(f"  {w}: {c} (suf={sg})")

    # Top cth- words in A
    cth_counts = Counter(cth_words)
    print(f"\nTop cth-words in A:")
    for w, c in cth_counts.most_common(10):
        sg = suffix_group(w)
        stem, suf = strip_suffix(w[3:] if w.startswith('cth') else w)  # strip 'cth'
        print(f"  {w}: {c} (stripped_stem='{stem}', suf='{sg}')")

    # === Summary ===
    print(f"\n{'='*60}")
    print("SUMMARY: Do qo- and cth- stem classes have different suffix distributions?")
    print(f"{'='*60}")
    print(f"qo-words (k/t-initial B): dominant suffixes:")
    for suf, rate in sorted(qo_dist.items(), key=lambda x: -x[1])[:5]:
        print(f"  -{suf}: {100*rate:.1f}%")
    print(f"cth-words (o/y/e-initial A): dominant suffixes:")
    for suf, rate in sorted(cth_dist.items(), key=lambda x: -x[1])[:5]:
        print(f"  -{suf}: {100*rate:.1f}%")
    print(f"KL(qo || cth) = {kl(qo_dist, cth_dist):.3f} bits (how different the suffix paradigms are)")
    print(f"KL(all-A || all-B) = {kl(all_a_dist, all_b_dist):.3f} bits (A/B overall divergence)")

if __name__ == '__main__':
    main()
