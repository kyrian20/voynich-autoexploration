"""
exp_130: d-Onset Grammar (H203) + o-Prefix Body Words (H202)
==============================================================
H203: Is d-onset a unified line-boundary morpheme class?
      Classify bare_d (dal/dam/daiin/dy) vs d+gallows (dch-/dsh- = LINE_OPEN tier).
      LF/LL positions for each d-word. d-chain: what follows d-closer at line-end?

H202: ok/ot-onset body words — are they a naming vocabulary parallel to labels?
      Section distribution, vocab overlap with ok-labels, positional behavior.
"""

import re
from collections import defaultdict, Counter

SUFFIXES = ['eeedy','eeey','eedy','edy','eey','aiin','ain','air','am',
            'ol','or','ar','al','ey','dy','y']

def get_suffix(word):
    for s in SUFFIXES:
        if word.endswith(s) and len(word) > len(s):
            return s
    return 'other'

def get_onset(word):
    for pat in ['qok','qot','qo','cth','ch','sh','ok','ot','ol','olk','d','s']:
        if word.startswith(pat):
            return pat
    if len(word) >= 1 and word[0] in 'yklrtpf':
        return word[0]
    return 'other'

SECTION_MAP = {}
for f in range(1,   58): SECTION_MAP[f] = 'herbal'
for f in range(67,  74): SECTION_MAP[f] = 'astro'
for f in range(75,  85): SECTION_MAP[f] = 'cosmo'
for f in range(87, 103): SECTION_MAP[f] = 'pharma'
for f in range(103,117): SECTION_MAP[f] = 'stars'

def get_section(fn): return SECTION_MAP.get(fn, 'other')
def parse_folio_num(locus):
    m = re.match(r'f(\d+)', locus)
    return int(m.group(1)) if m else None

def is_d_gallows(word):
    """d followed by a gallows character (k/t/p/f as next char after d)."""
    if not word.startswith('d'):
        return False
    rest = word[1:]
    return bool(rest) and rest[0] in 'ktpf'

def parse_corpus_with_labels(path):
    """Parse body text AND label text separately."""
    body_lines = []
    label_lines = []
    folio_word_counts = defaultdict(Counter)

    with open(path, encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^>]+)>(.*)', line)
            if not m:
                continue
            locus_raw, text_raw = m.group(1), m.group(2)
            parts = locus_raw.split(',')
            locus = parts[0]
            locus_type_raw = parts[1] if len(parts) > 1 else ''
            locus_type = locus_type_raw.lstrip('@+*=~&')
            folio_num = parse_folio_num(locus)
            if folio_num is None:
                continue
            text = re.sub(r'<[^>]*>', '', text_raw)
            text = re.sub(r'\[[^\]]*\]', ' ', text)
            text = re.sub(r'![\w.;@]*', '', text)
            text = re.sub(r'[*@&~=+$#{}?]', '', text)
            words = [w for w in re.split(r'[-.\s,]+', text)
                     if re.match(r'^[a-z]{2,}$', w)]
            if not words:
                continue

            if re.match(r'P', locus_type):
                body_lines.append((locus, folio_num, words))
                for w in words:
                    folio_word_counts[folio_num][w] += 1
            elif re.match(r'L', locus_type):
                label_lines.append((locus, folio_num, words))

    dialect_b = {}
    for fnum, cnt in folio_word_counts.items():
        total = sum(cnt.values())
        edy_count = sum(v for w, v in cnt.items() if w.endswith('edy') or w.endswith('eedy'))
        dialect_b[fnum] = (edy_count / total >= 0.05) if total > 0 else False

    records = []
    for locus, folio_num, words in body_lines:
        dialect = 'B' if dialect_b.get(folio_num, False) else 'A'
        section = get_section(folio_num)
        records.append({
            'locus': locus, 'folio_num': folio_num,
            'dialect': dialect, 'section': section, 'words': words, 'type': 'body'
        })

    label_records = []
    for locus, folio_num, words in label_lines:
        section = get_section(folio_num)
        label_records.append({
            'locus': locus, 'folio_num': folio_num,
            'section': section, 'words': words, 'type': 'label'
        })

    return records, label_records

# ── H203: d-onset grammar ─────────────────────────────────────────────────────

def analyze_d_onset_grammar(records):
    print("=" * 70)
    print("H203: d-ONSET GRAMMAR — LINE-BOUNDARY MORPHEME CLASS?")
    print("=" * 70)

    # Collect all d-onset words with position info
    d_words = defaultdict(lambda: {'n':0, 'A':0, 'B':0, 'LF':0, 'LL':0, 'MID':0,
                                    'section': Counter(), 'gallows': False})
    # Line positions: LF = line-first, LL = line-last, MID = middle

    for rec in records:
        words = rec['words']
        n = len(words)
        for i, w in enumerate(words):
            if not w.startswith('d'):
                continue
            d = d_words[w]
            d['n'] += 1
            d[rec['dialect']] += 1
            d['section'][rec['section']] += 1
            d['gallows'] = is_d_gallows(w)
            if i == 0:
                d['LF'] += 1
            elif i == n - 1:
                d['LL'] += 1
            else:
                d['MID'] += 1

    # Classify d-words
    # Bare d: short words starting with d (no gallows following)
    # d+gallows: d followed by k/t/p/f
    bare_d = {w: d for w, d in d_words.items() if not is_d_gallows(w)}
    d_gall  = {w: d for w, d in d_words.items() if is_d_gallows(w)}

    print(f"\nTotal d-onset words: {sum(d['n'] for d in d_words.values()):,} tokens, {len(d_words)} types")
    print(f"  bare_d (no gallows): {sum(d['n'] for d in bare_d.values()):,} tokens, {len(bare_d)} types")
    print(f"  d+gallows: {sum(d['n'] for d in d_gall.values()):,} tokens, {len(d_gall)} types")

    # Top bare_d words with LF/LL rates
    print(f"\nTop bare_d words (LF=line-first, LL=line-last, MID=middle):")
    print(f"{'Word':<15} {'n':>6} {'LF%':>6} {'LL%':>6} {'MID%':>6} {'A/B':>6} {'Section-top':>12}")
    print("-" * 62)
    for w, d in sorted(bare_d.items(), key=lambda x: -x[1]['n'])[:30]:
        n = d['n']
        lf = d['LF']/n; ll = d['LL']/n; mid = d['MID']/n
        ab = d['A']/d['B'] if d['B'] else float('inf')
        top_sec = d['section'].most_common(1)[0][0] if d['section'] else '—'
        print(f"{w:<15} {n:>6} {lf:>5.1%} {ll:>5.1%} {mid:>5.1%} {ab:>5.2f} {top_sec:>12}")

    print(f"\nTop d+gallows words:")
    print(f"{'Word':<15} {'n':>6} {'LF%':>6} {'LL%':>6} {'MID%':>6} {'A/B':>6}")
    print("-" * 48)
    for w, d in sorted(d_gall.items(), key=lambda x: -x[1]['n'])[:15]:
        n = d['n']
        lf = d['LF']/n; ll = d['LL']/n; mid = d['MID']/n
        ab = d['A']/d['B'] if d['B'] else float('inf')
        print(f"{w:<15} {n:>6} {lf:>5.1%} {ll:>5.1%} {mid:>5.1%} {ab:>5.2f}")

    # d-CHAIN: when a line ends with a d-word, what does the NEXT LINE start with?
    print(f"\nd-CHAIN ANALYSIS: d-word at line-end → next line's first word onset")
    # Pair consecutive records: if record[i] last word is d-onset and record[i+1] is consecutive
    # (same folio, consecutive line = approximate; check by locus numbering)
    line_endings_d = []  # (closing d-word, next_line_first_onset, next_line_first_word)
    line_endings_nond = []  # (non-d closing, next_line_first_onset)

    for i in range(len(records) - 1):
        rec = records[i]
        next_rec = records[i+1]
        # Same folio check (approximate consecutive lines)
        if rec['folio_num'] != next_rec['folio_num']:
            continue
        if not rec['words'] or not next_rec['words']:
            continue
        last_w = rec['words'][-1]
        next_first = next_rec['words'][0]
        if last_w.startswith('d'):
            line_endings_d.append((last_w, get_onset(next_first), next_first))
        else:
            line_endings_nond.append((last_w, get_onset(next_first)))

    d_chain_next_onset = Counter(o for _, o, _ in line_endings_d)
    nond_chain_next_onset = Counter(o for _, o in line_endings_nond)
    total_d_end = len(line_endings_d)
    total_nond_end = len(line_endings_nond)

    print(f"  Lines ending with d-onset word: {total_d_end}")
    print(f"  Lines ending with non-d word: {total_nond_end}")
    print(f"\n  Next-line first-word onset when current line ENDS WITH d:")
    print(f"  {'Onset':<8} {'Count':>6} {'%':>6} {'Enrich':>8}")
    for o, cnt in d_chain_next_onset.most_common(10):
        d_rate = cnt / total_d_end
        nd_cnt = nond_chain_next_onset.get(o, 0)
        nd_rate = nd_cnt / total_nond_end if total_nond_end else 0
        enrich = d_rate / nd_rate if nd_rate > 0 else float('inf')
        print(f"  {o:<8} {cnt:>6} {d_rate:>5.1%} {enrich:>7.2f}×")

    # d-openers vs d-closers: are there clear positional sub-classes?
    print(f"\nd-onset POSITIONAL SUB-CLASSES:")
    closers = [(w, d) for w, d in bare_d.items() if d['n'] >= 5 and d['LL']/d['n'] >= 0.3]
    openers = [(w, d) for w, d in bare_d.items() if d['n'] >= 5 and d['LF']/d['n'] >= 0.3]
    balanced = [(w, d) for w, d in bare_d.items() if d['n'] >= 5 and d['LF']/d['n'] < 0.3 and d['LL']/d['n'] < 0.3]

    print(f"  Closers (LL≥30%): {[w for w,_ in sorted(closers, key=lambda x:-x[1]['n'])[:10]]}")
    print(f"  Openers (LF≥30%): {[w for w,_ in sorted(openers, key=lambda x:-x[1]['n'])[:10]]}")
    print(f"  Balanced: {[w for w,_ in sorted(balanced, key=lambda x:-x[1]['n'])[:10]]}")

# ── H202: ok/ot body words ────────────────────────────────────────────────────

def analyze_ok_ot_body(records, label_records):
    print()
    print("=" * 70)
    print("H202: ok/ot-ONSET BODY WORDS vs LABELS — PARALLEL NAMING VOCABULARY?")
    print("=" * 70)

    # Collect ok/ot body words
    ok_body = defaultdict(lambda: {'n':0, 'A':0, 'B':0, 'section': Counter(),
                                    'LF':0, 'LL':0, 'MID':0})
    ot_body = defaultdict(lambda: {'n':0, 'A':0, 'B':0, 'section': Counter(),
                                    'LF':0, 'LL':0, 'MID':0})
    ol_body = defaultdict(lambda: {'n':0, 'A':0, 'B':0, 'section': Counter(),
                                    'LF':0, 'LL':0, 'MID':0})

    for rec in records:
        words = rec['words']
        n = len(words)
        for i, w in enumerate(words):
            o = get_onset(w)
            pos = 'LF' if i==0 else ('LL' if i==n-1 else 'MID')
            target = None
            if o == 'ok':
                target = ok_body[w]
            elif o == 'ot':
                target = ot_body[w]
            elif o == 'ol':
                target = ol_body[w]
            if target is not None:
                target['n'] += 1
                target[rec['dialect']] += 1
                target['section'][rec['section']] += 1
                target[pos] += 1

    # Collect ok/ot label words
    ok_labels = Counter()
    ot_labels = Counter()
    ol_labels = Counter()
    for rec in label_records:
        for w in rec['words']:
            o = get_onset(w)
            if o == 'ok': ok_labels[w] += 1
            elif o == 'ot': ot_labels[w] += 1
            elif o == 'ol': ol_labels[w] += 1

    # Compare vocabularies
    for name, body_dict, label_cnt in [('ok', ok_body, ok_labels),
                                         ('ot', ot_body, ot_labels),
                                         ('ol', ol_body, ol_labels)]:
        body_vocab = set(body_dict.keys())
        label_vocab = set(label_cnt.keys())
        shared = body_vocab & label_vocab
        j = len(shared) / len(body_vocab | label_vocab) if (body_vocab | label_vocab) else 0
        total_body = sum(d['n'] for d in body_dict.values())
        total_labels = sum(label_cnt.values())

        print(f"\n{name.upper()}-onset:")
        print(f"  Body: {total_body:,} tokens, {len(body_vocab)} types")
        print(f"  Labels: {total_labels:,} tokens, {len(label_vocab)} types")
        print(f"  Shared types: {len(shared)} / Jaccard={j:.3f}")
        print(f"  Shared words: {sorted(shared)[:10]}")
        print(f"  Top body {name}-words:")
        for w, d in sorted(body_dict.items(), key=lambda x: -x[1]['n'])[:10]:
            n = d['n']
            lf = d['LF']/n; ll = d['LL']/n; mid = d['MID']/n
            b_frac = d['B']/n if n else 0
            top_sec = d['section'].most_common(1)[0][0]
            in_label = '✓' if w in label_vocab else '✗'
            print(f"    {w:<15} {n:>5} {b_frac:>5.1%}B {lf:>5.1%}LF {mid:>5.1%}MID {ll:>5.1%}LL {in_label} {top_sec}")

    # Section distribution of ok/ot body words
    sections = ['herbal', 'astro', 'cosmo', 'pharma', 'stars']
    print(f"\nSection distribution of ok/ot/ol body words:")
    for name, body_dict in [('ok', ok_body), ('ot', ot_body), ('ol', ol_body)]:
        total = sum(d['n'] for d in body_dict.values())
        if total == 0:
            continue
        sec_cnt = Counter()
        for d in body_dict.values():
            for s, c in d['section'].items():
                sec_cnt[s] += c
        dist = " ".join(f"{s[:5]}={sec_cnt[s]/total:.1%}" for s in sections)
        print(f"  {name}: {dist}")

    # Position distribution
    print(f"\nPosition distribution of ok/ot/ol body words (LF/MID/LL):")
    for name, body_dict in [('ok', ok_body), ('ot', ot_body), ('ol', ol_body)]:
        total = sum(d['n'] for d in body_dict.values())
        if total == 0:
            continue
        lf = sum(d['LF'] for d in body_dict.values())
        ll = sum(d['LL'] for d in body_dict.values())
        mid = sum(d['MID'] for d in body_dict.values())
        print(f"  {name}: LF={lf/total:.1%}, MID={mid/total:.1%}, LL={ll/total:.1%}")


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    corpus_path = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'
    print("Loading corpus...")
    records, label_records = parse_corpus_with_labels(corpus_path)
    total_words = sum(len(r['words']) for r in records)
    total_labels = sum(len(r['words']) for r in label_records)
    print(f"Loaded {len(records)} body lines ({total_words:,} words), {len(label_records)} label lines ({total_labels:,} words)")

    analyze_d_onset_grammar(records)
    analyze_ok_ot_body(records, label_records)
