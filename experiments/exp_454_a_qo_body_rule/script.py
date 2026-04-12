"""
exp_454: A-dialect e-body → qo Rule: Parallel to B's e-body → qok (H_new_P)
Q: In A-dialect, does the e-body conditional routing generalize?
   Specifically: (1) does e-body → qo elevated hold across ALL onset classes (not just sh/ch)?
   (2) Is there an A qo+e-body self-succession rule parallel to B qok+e-body → qok?
   (3) How similar are A qo vocabulary and B qok vocabulary (functional analog test)?

Method: A-dialect MID bigrams. For each onset class with N≥15 predecessor tokens,
compute successor distribution by body-char, focusing on qo as successor.
"""
import re
from collections import defaultdict, Counter

ZL3B = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

ONSETS = ['qok','qot','qo','cth','ch','sh','ok','ot','ol','d','s','y','k','t','l','r','p','f','o']

def get_onset(word):
    for on in ONSETS:
        if word.startswith(on):
            return on
    return 'other'

def get_first_body_char(word, onset):
    body = word[len(onset):]
    return body[0] if body else '_'

def parse_corpus():
    pattern = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
    folios = defaultdict(list)
    with open(ZL3B, encoding='utf-8') as f:
        for line in f:
            for m in pattern.finditer(line):
                folio = m.group(1).lstrip('+*=&~')
                lc = m.group(3).lstrip('+*=/~&')
                if not lc.lstrip('@').startswith('P'):
                    continue
                text = m.group(4).strip()
                words = [w for w in re.split(r'[-.\s]', text)
                         if re.match(r'^[a-z]+$', w) and len(w) >= 2]
                if words:
                    folios[folio].append(words)
    return folios

def classify_dialects(folios):
    dialect = {}
    for folio, lines in folios.items():
        total = sum(len(ws) for ws in lines)
        if total == 0: continue
        edy = sum(1 for ws in lines for w in ws
                  if w.endswith('edy') or w.endswith('eedy'))
        dialect[folio] = 'B' if edy / total >= 0.05 else 'A'
    return dialect

def collect_mid_bigrams(folios, dialect_map, target_dialect):
    body_bigrams = defaultdict(Counter)  # (onset, body_char) -> Counter(succ_onset)
    onset_body_total = Counter()
    baseline_succ = defaultdict(Counter)  # onset -> Counter(succ_onset)
    total_mid = 0

    for folio, lines in folios.items():
        if folio not in dialect_map or dialect_map[folio] != target_dialect:
            continue
        n = len(lines)
        if n < 3: continue
        cont_lines = lines[1:-1]
        for line_words in cont_lines:
            lw = len(line_words)
            if lw < 4: continue
            mid_words = line_words[1:lw-1]
            for i in range(len(mid_words) - 1):
                w1, w2 = mid_words[i], mid_words[i+1]
                on1 = get_onset(w1)
                on2 = get_onset(w2)
                if on1 == 'other' or on2 == 'other': continue
                bc1 = get_first_body_char(w1, on1)
                body_bigrams[(on1, bc1)][on2] += 1
                onset_body_total[(on1, bc1)] += 1
                baseline_succ[on1][on2] += 1
                total_mid += 1

    return body_bigrams, onset_body_total, baseline_succ, total_mid

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)

    a_bigrams, a_body_total, a_baseline, a_total = collect_mid_bigrams(folios, dialect_map, 'A')
    b_bigrams, b_body_total, b_baseline, b_total = collect_mid_bigrams(folios, dialect_map, 'B')

    # 1. A: e-body → qo systematic check across all onset classes
    print("=== A-dialect: e-body predecessor → qo successor enrichment ===\n")
    print(f"A baseline P(qo | any) = {sum(a_baseline[on]['qo'] for on in a_baseline)/a_total:.3f}")
    print(f"\n{'Onset+body':<15} {'N(pred)':>8} {'obs→qo':>8} {'exp→qo':>8} {'E(qo)':>7} | "
          f"{'B parallel: obs→qok':>20} {'E(qok)':>8}")
    print("-"*75)

    for onset in ['sh', 'ch', 'd', 'y', 'ol', 'ok', 'qok', 'ot', 'o', 'cth', 'qot']:
        # A e-body
        n_a_e = a_body_total.get((onset, 'e'), 0)
        if n_a_e < 5: continue
        a_base_total = sum(a_baseline[onset].values())
        if a_base_total < 10: continue
        a_p_qo = a_baseline[onset]['qo'] / a_base_total
        a_obs_qo = a_bigrams[(onset, 'e')]['qo']
        a_exp_qo = n_a_e * a_p_qo
        a_E_qo = a_obs_qo / a_exp_qo if a_exp_qo >= 1 else 0

        # B e-body → qok for comparison
        n_b_e = b_body_total.get((onset, 'e'), 0)
        b_base_total = sum(b_baseline[onset].values())
        b_p_qok = b_baseline[onset]['qok'] / b_base_total if b_base_total > 0 else 0
        b_obs_qok = b_bigrams[(onset, 'e')]['qok']
        b_exp_qok = n_b_e * b_p_qok
        b_E_qok = b_obs_qok / b_exp_qok if b_exp_qok >= 1 else 0

        marker = ' *' if a_E_qo >= 1.4 else (' DEP' if a_E_qo <= 0.6 and a_exp_qo >= 2 else '')
        print(f"{onset}+'e':{n_a_e:>9} {a_obs_qo:>8} {a_exp_qo:>8.1f} {a_E_qo:>7.2f}×{marker} | "
              f"B N={n_b_e}: {b_obs_qok}/{b_exp_qok:.1f} E={b_E_qok:.2f}×")

    # 2. A qo body-conditional: does qo+e-body self-replicate like B qok+e-body?
    print(f"\n=== A-dialect: qo onset body-conditional succession ===\n")
    qo_base = sum(a_baseline['qo'].values())
    if qo_base > 0:
        print(f"A qo baseline N={qo_base}")
        print(f"A P(qo→qo) baseline = {a_baseline['qo']['qo']/qo_base:.3f}")
        print(f"\n  body_char  N(pred)  obs→qo  E(qo→qo)  obs→qok  E(qo→qok)  obs→sh  E(qo→sh)")
        for bc in ['e', 'a', 'o', 'c', 'y', '_']:
            n = a_body_total.get(('qo', bc), 0)
            if n < 5: continue
            base_p_qo = a_baseline['qo']['qo'] / qo_base
            base_p_qok = a_baseline['qo']['qok'] / qo_base
            base_p_sh = a_baseline['qo']['sh'] / qo_base
            obs_qo = a_bigrams[('qo', bc)]['qo']
            obs_qok = a_bigrams[('qo', bc)]['qok']
            obs_sh = a_bigrams[('qo', bc)]['sh']
            exp_qo = n * base_p_qo
            exp_qok = n * base_p_qok
            exp_sh = n * base_p_sh
            E_qo = obs_qo/exp_qo if exp_qo >= 1 else 0
            E_qok = obs_qok/exp_qok if exp_qok >= 1 else 0
            E_sh = obs_sh/exp_sh if exp_sh >= 1 else 0
            print(f"  '{bc}': N={n:>5}  {obs_qo:>5}/{exp_qo:>4.1f}={E_qo:.2f}×  "
                  f"{obs_qok:>5}/{exp_qok:>4.1f}={E_qok:.2f}×  "
                  f"{obs_sh:>5}/{exp_sh:>4.1f}={E_sh:.2f}×")

    # 3. A qo vs B qok vocabulary similarity
    print(f"\n=== A qo vs B qok vocabulary comparison ===\n")
    a_qo_words = Counter()
    b_qok_words = Counter()
    for folio, lines in folios.items():
        if folio not in dialect_map: continue
        d = dialect_map[folio]
        for line_words in lines:
            for w in line_words:
                on = get_onset(w)
                if d == 'A' and on == 'qo':
                    a_qo_words[w] += 1
                elif d == 'B' and on == 'qok':
                    b_qok_words[w] += 1

    a_qo_types = set(a_qo_words.keys())
    b_qok_types = set(b_qok_words.keys())
    shared = a_qo_types & b_qok_types
    print(f"A qo word types: {len(a_qo_types)}")
    print(f"B qok word types: {len(b_qok_types)}")
    print(f"Shared (qo=A, qok=B identical string): {len(shared)}")
    print(f"Jaccard: {len(shared)/len(a_qo_types|b_qok_types):.3f}")
    print(f"(Note: qo and qok have different onset strings so exact overlap is low by construction)")

    # Check if A qo words are similar to B qok words with qo→qok onset substitution
    a_qo_stems = {w[2:]: w for w in a_qo_types}  # strip 'qo' onset
    b_qok_stems = {w[3:]: w for w in b_qok_types}  # strip 'qok' onset
    shared_stems = set(a_qo_stems.keys()) & set(b_qok_stems.keys())
    print(f"\nShared body+suffix (qo→qok substitution): {len(shared_stems)} / {min(len(a_qo_stems), len(b_qok_stems))} = "
          f"{len(shared_stems)/len(set(a_qo_stems.keys())|set(b_qok_stems.keys())):.3f}")
    print(f"\nTop shared body+suffix (appearing as A qo+X and B qok+X):")
    stem_combined = [(stem, a_qo_words.get(a_qo_stems[stem], 0), b_qok_words.get(b_qok_stems[stem], 0))
                     for stem in shared_stems]
    stem_combined.sort(key=lambda x: -(x[1]+x[2]))
    print(f"  {'stem (body+suf)':<15} {'A qo+stem':>12} {'B qok+stem':>12} {'A_word':<12} {'B_word':<12}")
    for stem, af, bf in stem_combined[:15]:
        aw = a_qo_stems[stem]
        bw = b_qok_stems[stem]
        print(f"  {stem:<15} {af:>12} {bf:>12} {aw:<12} {bw:<12}")

    # 4. Positional distribution comparison: A qo vs B qok
    print(f"\n=== Positional distribution: A qo vs B qok ===\n")
    pos_counts = defaultdict(Counter)  # (dialect, onset) -> Counter(pos)
    for folio, lines in folios.items():
        if folio not in dialect_map: continue
        d = dialect_map[folio]
        n = len(lines)
        if n < 3: continue
        cont_lines = lines[1:-1]
        cn = len(cont_lines)
        for ci, line_words in enumerate(cont_lines):
            lw = len(line_words)
            if lw < 2: continue
            for wi, w in enumerate(line_words):
                on = get_onset(w)
                if wi == 0:
                    pos = 'LF'
                elif wi == lw-1:
                    pos = 'LL'
                else:
                    pos = 'MID'
                for key in [('A', 'qo'), ('B', 'qok')]:
                    if d == key[0] and on == key[1]:
                        pos_counts[key][pos] += 1

    for key in [('A', 'qo'), ('B', 'qok')]:
        counts = pos_counts[key]
        total = sum(counts.values())
        if total > 0:
            print(f"  {key[0]} {key[1]}: LF={counts['LF']/total:.3f}  MID={counts['MID']/total:.3f}  LL={counts['LL']/total:.3f}  N={total}")

    # Overall positional baselines
    print(f"\n  A overall (for comparison):")
    a_pos_total = Counter()
    for folio, lines in folios.items():
        if folio not in dialect_map or dialect_map[folio] != 'A': continue
        for line_words in lines:
            lw = len(line_words)
            for wi, w in enumerate(line_words):
                pos = 'LF' if wi == 0 else ('LL' if wi == lw-1 else 'MID')
                a_pos_total[pos] += 1
    at = sum(a_pos_total.values())
    print(f"  LF={a_pos_total['LF']/at:.3f}  MID={a_pos_total['MID']/at:.3f}  LL={a_pos_total['LL']/at:.3f}")

if __name__ == '__main__':
    main()
