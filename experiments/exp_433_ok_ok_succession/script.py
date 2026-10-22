"""
exp_433: ok→ok self-succession driven by specific ok word types? (H570)
B: ok→ok=1.32×, A: ok→ok=1.93× (from F363/earlier findings)
Is this class-level memory or word-level clustering?
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

ONSET_ORDER = ['qok','qot','qo','cth','ch','sh','ok','ot','ol',
               'd','s','y','k','t','l','r','p','f','o']

def get_onset(w):
    for o in ONSET_ORDER:
        if w.startswith(o):
            return o
    return 'other'

def folio_base(folio):
    return re.sub(r'[rv]\d*$', '', folio)

def parse_and_classify():
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0})
    raw_lines = []
    with open(ZL3B, encoding='utf-8') as f:
        for raw in f:
            raw = raw.strip()
            if not raw or raw.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', raw)
            if not m: continue
            folio = m.group(1).lstrip('+*=&~')
            ln = int(m.group(2))
            lc = m.group(3).lstrip('+*=/~&')
            if not lc.lstrip('@').startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', raw)
            words = [w for w in re.split(r'[-.\s]', text)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words:
                raw_lines.append((folio, ln, words))
                fb = folio_base(folio)
                for w in words:
                    folio_word_stats[fb]['total'] += 1
                    if w.endswith('edy') or w.endswith('eedy'):
                        folio_word_stats[fb]['edy'] += 1

    dialect = {}
    for fb, stats in folio_word_stats.items():
        if stats['total'] >= 20:
            rate = stats['edy'] / stats['total']
            dialect[fb] = 'B' if rate >= 0.05 else 'A'

    folio_groups = defaultdict(list)
    for folio, ln, words in raw_lines:
        fb = folio_base(folio)
        if fb in dialect:
            folio_groups[(folio, dialect[fb])].append((ln, words))

    cont_by_dialect = {'A': [], 'B': []}
    for (folio, d), flines in folio_groups.items():
        lns = [fl[0] for fl in flines]
        min_ln, max_ln = min(lns), max(lns)
        for ln, words in flines:
            if ln != min_ln and ln != max_ln:
                cont_by_dialect[d].append((folio, ln, words))

    return cont_by_dialect

def analyze_ok_ok(lines, dialect):
    print(f"\n=== {dialect}-dialect ok→ok analysis ===")
    print(f"Lines: {len(lines)}")

    ok_ok_pairs = []       # (w1, w2) for all ok→ok pairs
    ok_pairs_all = Counter()  # (w1, w2) counts
    ok_succ_all = Counter()   # distribution after ok
    ok_vocab = Counter()      # all ok-onset words

    total_pairs = 0
    ok_ok_count = 0
    total_ok = 0

    for folio, ln, words in lines:
        for i, w in enumerate(words):
            if get_onset(w) == 'ok':
                ok_vocab[w] += 1
                total_ok += 1
        for i in range(len(words)-1):
            total_pairs += 1
            w1, w2 = words[i], words[i+1]
            if get_onset(w1) == 'ok':
                ok_succ_all[get_onset(w2)] += 1
                if get_onset(w2) == 'ok':
                    ok_ok_count += 1
                    ok_ok_pairs.append((w1, w2))
                    ok_pairs_all[(w1, w2)] += 1

    ok_rate = total_ok / sum(len(words) for f,l,words in lines)
    total_ok_as_pred = sum(ok_succ_all.values())
    expected_ok_ok = total_ok_as_pred * ok_rate
    e_ok_ok = ok_ok_count / expected_ok_ok if expected_ok_ok > 0 else 0

    print(f"\nok total tokens: {total_ok}, ok rate: {ok_rate:.4f}")
    print(f"ok→ok pairs: {ok_ok_count}, expected: {expected_ok_ok:.1f}, E={e_ok_ok:.2f}×")

    # Same vs different word analysis
    same_word = sum(1 for w1, w2 in ok_ok_pairs if w1 == w2)
    diff_word = ok_ok_count - same_word
    print(f"\nSame word (w1=w2): {same_word}/{ok_ok_count} = {same_word/ok_ok_count:.3f}" if ok_ok_count > 0 else "no pairs")
    print(f"Different word: {diff_word}/{ok_ok_count} = {diff_word/ok_ok_count:.3f}" if ok_ok_count > 0 else "")

    # Top ok-onset words
    print(f"\nTop ok-onset words (top 15):")
    for w, n in ok_vocab.most_common(15):
        print(f"  {w}: {n}")

    # Top ok→ok word pairs
    print(f"\nTop ok→ok word pairs ({ok_ok_count} total):")
    for (w1, w2), n in ok_pairs_all.most_common(15):
        same_tag = "(same)" if w1 == w2 else ""
        print(f"  {w1} → {w2}: {n} {same_tag}")

    # Type diversity in ok→ok pairs
    unique_w1 = len(set(w1 for w1, w2 in ok_ok_pairs))
    unique_w2 = len(set(w2 for w1, w2 in ok_ok_pairs))
    print(f"\nUnique w1 types in ok→ok: {unique_w1}/{len(ok_vocab)}")
    print(f"Unique w2 types in ok→ok: {unique_w2}/{len(ok_vocab)}")

    # Check: for top ok words, what is their ok→ok self-succession rate?
    print(f"\nTop ok words self-succession analysis:")
    for w, total_count in ok_vocab.most_common(8):
        # How often does w appear as w2 after w as w1?
        self_succ = ok_pairs_all.get((w, w), 0)
        # How often does w appear as w1 in any ok→ok pair?
        w_as_w1 = sum(cnt for (w1,w2), cnt in ok_pairs_all.items() if w1 == w)
        frac = self_succ / w_as_w1 if w_as_w1 > 0 else 0
        print(f"  {w}: total={total_count}, ok→ok as w1={w_as_w1}, self→self={self_succ}, self_rate={frac:.3f}")

def main():
    cont = parse_and_classify()
    for d in ['A', 'B']:
        analyze_ok_ok(cont[d], d)

if __name__ == '__main__':
    main()
