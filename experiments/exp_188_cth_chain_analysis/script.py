"""
exp_188: cth-Word Chain Analysis — H351 (chol/daiin bigram), H352 (cthedy successors), H353 (cthol→cthy)

Motivation:
  F176 (exp_169): [ch][daiin]→cth=5.89×; [cth-MID][cthy@LL]=4.67×; cthol successor cth=2.41×;
  cthedy successor l=5.79×, ot=5.07×.

  H351: Is [chol][daiin] a stable bigram unit preceding cth? chol (3×) and chor (2×) were
    the most common ch-words in the [ch][daiin]→cth trigram (F176). Does [chol][daiin] itself
    reliably precede cth-words? Is daiin a necessary bridge between chol and cth?

  H352: What specific words follow cthedy? The l-onset (5.79×) and ot-onset (5.07×) enrichments
    for cthedy successors suggest specific bigram formulas. Are the successor words consistent?

  H353: The 4 cases of [cthol][cth-successor] — are these specifically [cthol][cthy]?
    Does daiin also mediate: [cthol][daiin][cthy]?

Pre-registration:
  H351: [chol][daiin][cth*] trigram likely has ≥3 cases (already known from exp_169).
    [chol]→cth directly (without daiin): expected at lower rate. daiin enriches the trigram.
  H352: cthedy successors likely diverse (3 cases each of l-onset and ot-onset = small n).
    Specific l-words may converge if [cthedy][ol] or [cthedy][ol] is a formula.
  H353: cthol→cthy likely but n=4 cases too small for specific claim. [cthol][daiin][cthy]
    may exist as a variant with daiin as mediator.
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

CORPUS = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

def get_onset(word):
    w = word.lower()
    if w.startswith('qok'): return 'qok'
    if w.startswith('qot'): return 'qot'
    if w.startswith('qo'): return 'qo'
    if w.startswith('cth'): return 'cth'
    if w.startswith('ch'): return 'ch'
    if w.startswith('sh'): return 'sh'
    if w.startswith('ok'): return 'ok'
    if w.startswith('ot'): return 'ot'
    if w.startswith('ol'): return 'ol'
    if w.startswith('d'): return 'd'
    if w.startswith('s'): return 's'
    if w.startswith('y'): return 'y'
    if w.startswith('k'): return 'k'
    if w.startswith('t'): return 't'
    if w.startswith('l'): return 'l'
    if w.startswith('r'): return 'r'
    return 'other'

def parse_locus(locus_raw):
    locus_parts = locus_raw.split(',')
    if len(locus_parts) < 2:
        return None, None
    folio_str = locus_parts[0]
    folio_base = folio_str.split('.')[0].lstrip('<')
    m = re.match(r'f(\d+)', folio_base)
    if not m:
        return None, None
    folio_num = int(m.group(1))
    lt_raw = locus_parts[1].rstrip('>')
    lt = lt_raw.lstrip('@+*=~&')
    return folio_num, lt

folio_words = defaultdict(list)
raw_lines = []
with open(CORPUS) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'): continue
        parts = line.split(None, 1)
        if len(parts) < 2: continue
        locus_raw, text = parts
        folio_num, lt = parse_locus(locus_raw)
        if folio_num is None: continue
        if not lt.startswith('P'): continue
        words = [w for w in text.split('.') if w and re.match(r'[a-z]', w) and not w.startswith('<')]
        if not words: continue
        folio_words[folio_num].extend(words)
        raw_lines.append((folio_num, words))

# Infer dialect from edy rate (same as exp_169)
folio_dialect = {}
for fn, wds in folio_words.items():
    if len(wds) < 10: continue
    edy_count = sum(1 for w in wds if 'edy' in w or 'eedy' in w)
    folio_dialect[fn] = 'B' if edy_count/len(wds) >= 0.05 else 'A'

lines_data = [(fn, folio_dialect.get(fn, 'unknown'), wds) for fn, wds in raw_lines]
a_lines = [(fn, wds) for fn, dial, wds in lines_data if dial == 'A']
b_lines = [(fn, wds) for fn, dial, wds in lines_data if dial == 'B']

A_words = [w for fn, wds in a_lines for w in wds]
B_words = [w for fn, wds in b_lines for w in wds]
print(f"Parsed: {len(a_lines)} A-lines ({len(A_words)} words), {len(b_lines)} B-lines ({len(B_words)} words)")
print()

def is_cth(w): return w.startswith('cth')
def is_daiin(w): return w == 'daiin'

# =====================================================================
# H351: [chol][daiin] bigram stability and cth succession
# =====================================================================
print("="*60)
print("H351: [chol][daiin] bigram stability and cth succession")
print("="*60)

for dialect_name, dlines, dwords in [('A', a_lines, A_words), ('B', b_lines, B_words)]:
    n = len(dwords)
    ch_daiin_cth = []
    chol_chor_daiin = []
    chol_chor_next = []

    for fn, wds in dlines:
        for i in range(len(wds)-2):
            w0, w1, w2 = wds[i], wds[i+1], wds[i+2]
            if w0.startswith('ch') and is_daiin(w1) and is_cth(w2):
                ch_daiin_cth.append((w0, w1, w2))
            if w0 in ('chol','chor') and is_daiin(w1):
                chol_chor_daiin.append((w0, w1, w2))
        for i in range(len(wds)-1):
            if wds[i] in ('chol','chor'):
                chol_chor_next.append((wds[i], wds[i+1]))

    cth_rate = sum(1 for w in dwords if is_cth(w)) / n if n else 0
    daiin_rate = sum(1 for w in dwords if is_daiin(w)) / n if n else 0

    print(f"\n--- {dialect_name}-dialect ({n} tokens) ---")
    print(f"  cth-word rate: {cth_rate:.4f} | daiin rate: {daiin_rate:.4f}")

    print(f"\n  [ch-word][daiin][cth-word] trigrams: {len(ch_daiin_cth)}")
    if ch_daiin_cth:
        c = Counter(ch_daiin_cth)
        for trig, cnt in c.most_common(10):
            print(f"    {trig} × {cnt}")
        ch_before = Counter(a for a,b,c2 in ch_daiin_cth)
        cth_after = Counter(c2 for a,b,c2 in ch_daiin_cth)
        print(f"  ch-words in trigram: {dict(ch_before.most_common(8))}")
        print(f"  cth-words in trigram: {dict(cth_after.most_common(8))}")

    print(f"\n  [chol/chor][daiin][?] trigrams: {len(chol_chor_daiin)}")
    if chol_chor_daiin:
        c = Counter((a,c2) for a,b,c2 in chol_chor_daiin)
        for (a,c2), cnt in c.most_common(10):
            print(f"    [{a}][daiin][{c2}] × {cnt}")
        cth_count = sum(1 for a,b,c2 in chol_chor_daiin if is_cth(c2))
        print(f"  [chol/chor][daiin]→cth: {cth_count}/{len(chol_chor_daiin)} "
              f"({100*cth_count/len(chol_chor_daiin):.0f}%)")
        chol_daiin_cth_rate = cth_count / len(chol_chor_daiin)
        enrich = chol_daiin_cth_rate / cth_rate if cth_rate else 0
        print(f"  Enrichment vs base cth rate: {chol_daiin_cth_rate:.3f}/{cth_rate:.3f} = {enrich:.2f}×")

    print(f"\n  [chol/chor]→ALL successors: {len(chol_chor_next)}")
    if chol_chor_next:
        chol_cth = [(a,b) for a,b in chol_chor_next if is_cth(b)]
        chol_daiin = [(a,b) for a,b in chol_chor_next if is_daiin(b)]
        chol_other = [(a,b) for a,b in chol_chor_next if not is_cth(b) and not is_daiin(b)]
        print(f"    → cth-word (direct): {len(chol_cth)} ({Counter(chol_cth).most_common(5)})")
        print(f"    → daiin: {len(chol_daiin)}")
        print(f"    → other: {len(chol_other)} (top 5: {Counter(b for a,b in chol_other).most_common(5)})")
        # Enrichments
        for onset, count in [('cth', len(chol_cth)), ('d', sum(1 for a,b in chol_chor_next if get_onset(b)=='d'))]:
            base = sum(1 for w in dwords if get_onset(w)==onset) / n
            succ_rate = count / len(chol_chor_next)
            print(f"    chol/chor → {onset}: {succ_rate:.3f}/{base:.3f} = {succ_rate/base:.2f}×")

# =====================================================================
# H352: cthedy successor specificity (B-dialect)
# =====================================================================
print()
print("="*60)
print("H352: cthedy successor specificity (B-dialect)")
print("="*60)

for dialect_name, dwords in [('B', B_words), ('A', A_words)]:
    n = len(dwords)
    cthedy_count = dwords.count('cthedy')
    cthedy_succ = []
    for i in range(n-1):
        if dwords[i] == 'cthedy':
            cthedy_succ.append(dwords[i+1])

    onset_counts = Counter(get_onset(w) for w in dwords)

    print(f"\n--- {dialect_name}-dialect ---")
    print(f"  cthedy total: {cthedy_count}")
    print(f"  cthedy with successors: {len(cthedy_succ)}")
    if cthedy_succ:
        succ_c = Counter(cthedy_succ)
        print(f"  All successor words:")
        for word, cnt in succ_c.most_common():
            onset = get_onset(word)
            base = onset_counts[onset] / n
            succ_r = cnt / len(cthedy_succ)
            enrich = succ_r / base if base else 0
            print(f"    [{word}] onset={onset} ×{cnt} ({succ_r:.3f}/{base:.3f}={enrich:.2f}×)")

# =====================================================================
# H353: [cthol][cth-successor] specificity
# =====================================================================
print()
print("="*60)
print("H353: [cthol][cth-successor] — specifically [cthol][cthy]?")
print("="*60)

for dialect_name, dlines, dwords in [('A', a_lines, A_words), ('B', b_lines, B_words)]:
    n = len(dwords)
    cthol_succ = []
    cthol_daiin_next = []
    cthol_count = dwords.count('cthol')

    for fn, wds in dlines:
        for i in range(len(wds)-1):
            if wds[i] == 'cthol':
                cthol_succ.append(wds[i+1])
        for i in range(len(wds)-2):
            if wds[i] == 'cthol' and is_daiin(wds[i+1]):
                cthol_daiin_next.append(wds[i+2])

    onset_counts = Counter(get_onset(w) for w in dwords)
    print(f"\n--- {dialect_name}-dialect ---")
    print(f"  cthol occurrences: {cthol_count}")
    print(f"  cthol successors: {len(cthol_succ)}")
    if cthol_succ:
        succ_c = Counter(cthol_succ)
        print(f"  Top successors:")
        for word, cnt in succ_c.most_common(12):
            onset = get_onset(word)
            base = onset_counts[onset] / n
            succ_r = cnt / len(cthol_succ)
            enrich = succ_r / base if base else 0
            print(f"    [{word}] onset={onset} ×{cnt} ({succ_r:.3f}/{base:.3f}={enrich:.2f}×)")
        cth_succ = [w for w in cthol_succ if is_cth(w)]
        print(f"  cthol → cth-word: {len(cth_succ)}/{len(cthol_succ)} cases: {Counter(cth_succ).most_common(5)}")

    print(f"  [cthol][daiin][?] trigrams: {len(cthol_daiin_next)}")
    if cthol_daiin_next:
        c2 = Counter(cthol_daiin_next)
        for w, cnt in c2.most_common(8):
            print(f"    [cthol][daiin][{w}] ×{cnt}")
        cth_via_daiin = sum(1 for w in cthol_daiin_next if is_cth(w))
        print(f"  [cthol][daiin]→cth: {cth_via_daiin}/{len(cthol_daiin_next)}")
