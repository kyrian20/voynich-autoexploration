"""
exp_561: ckh and cph onset characterization (H_new_FX)
Compound gallows classes — are they openers like sch or terminals like cth?
Parts:
1. Vocabulary (top forms, A and B, for both ckh and cph)
2. Positional (pos1/MID/LL/LF vs baseline, both dialects)
3. Within-line bigrams (outgoing and incoming)
4. Summary: compound gallows positional classification
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter

CORPUS = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')
ONSET_PRIORITY = ['qok','qot','qo','cth','ckh','cph','ch','sh','ok','ot','ol','sch','skh','sph',
                  'd','s','y','k','t','l','r','p','f','o','e','a','n','m']

def get_onset(w):
    for o in ONSET_PRIORITY:
        if w.startswith(o):
            return o
    return w[0] if w else None

def parse_corpus(filepath):
    lines_A, lines_B = [], []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)', line)
            if not m: continue
            folio_raw, n_str, lc, text = m.group(1), m.group(2), m.group(3), m.group(4)
            lc2 = lc.lstrip('+*=/~&').lstrip('@')
            if not lc2.startswith('P'): continue
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words: continue
            try: n = int(n_str)
            except: continue
            edy_count = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
            is_b = edy_count / len(words) >= 0.05
            if is_b:
                lines_B.append((folio_raw, words))
            else:
                if n <= 56:
                    lines_A.append((folio_raw, words))
    return lines_A, lines_B

lines_A, lines_B = parse_corpus(CORPUS)
print(f"A herbal_a: {len(lines_A)} lines; B all: {len(lines_B)} lines")

all_A_words = [w for fo, ws in lines_A for w in ws]
all_B_words = [w for fo, ws in lines_B for w in ws]
print(f"A words: {len(all_A_words)}; B words: {len(all_B_words)}")

def analyze_onset(onset_class, lines_A, lines_B, all_A_words, all_B_words):
    print(f"\n{'='*60}")
    print(f"=== {onset_class.upper()} ONSET ===")
    print(f"{'='*60}")

    for lines, all_words, label in [(lines_A, all_A_words, "A herbal_a"), (lines_B, all_B_words, "B all")]:
        tokens = [w for w in all_words if get_onset(w) == onset_class]
        total = len(all_words)
        print(f"\n--- {label}: {len(tokens)} {onset_class} tokens ({100*len(tokens)/total:.3f}% of {total} words) ---")

        if len(tokens) == 0:
            print(f"  No {onset_class} tokens found.")
            continue

        # Vocabulary
        wc = Counter(tokens)
        print(f"  Unique types: {len(wc)}")
        print(f"  Top-15:")
        for w, c in wc.most_common(15):
            print(f"    {w}: {c} ({100*c/len(tokens):.1f}%)")

        # Positional
        pos_counts = {'pos1': 0, 'MID': 0, 'LL': 0, 'LF': 0}
        total_counts = {'pos1': 0, 'MID': 0, 'LL': 0, 'LF': 0}

        for fo, ws in lines:
            L = len(ws)
            if L < 1: continue
            onsets = [get_onset(w) for w in ws]

            total_counts['pos1'] += 1
            if onsets[0] == onset_class: pos_counts['pos1'] += 1

            if L >= 2:
                total_counts['LF'] += 1
                if onsets[-1] == onset_class: pos_counts['LF'] += 1
                total_counts['LL'] += 1
                if onsets[-2] == onset_class: pos_counts['LL'] += 1

            for i in range(1, L-1):
                total_counts['MID'] += 1
                if onsets[i] == onset_class: pos_counts['MID'] += 1

        mid_rate = pos_counts['MID'] / total_counts['MID'] if total_counts['MID'] > 0 else 0
        print(f"\n  Positional (MID baseline: {pos_counts['MID']}/{total_counts['MID']} = {mid_rate:.5f}):")
        for pos in ['pos1', 'LL', 'LF']:
            obs = pos_counts[pos]
            tot = total_counts[pos]
            if tot == 0: continue
            exp = mid_rate * tot
            e = (obs/tot) / mid_rate if mid_rate > 0 and obs > 0 else (0 if obs == 0 else float('inf'))
            flag = 'CONF' if e >= 1.5 and obs >= 10 else ('dir' if e >= 2.0 and obs >= 5 else ('(dir)' if e >= 2.5 and obs >= 3 else ('DEPL' if e < 0.7 and obs >= 3 else '')))
            print(f"    {pos}: obs={obs}/{tot}, exp={exp:.1f}, E={e:.2f}× {flag}")

        # Bigrams
        mid_counts = Counter()
        total_mid = 0
        for fo, ws in lines:
            L = len(ws)
            for i in range(1, L-1):
                mid_counts[get_onset(ws[i])] += 1
                total_mid += 1

        outgoing = Counter()
        n_sender = 0
        for fo, ws in lines:
            for i in range(len(ws) - 1):
                if get_onset(ws[i]) == onset_class:
                    outgoing[get_onset(ws[i+1])] += 1
                    n_sender += 1

        incoming = Counter()
        n_receiver = 0
        for fo, ws in lines:
            for i in range(1, len(ws)):
                if get_onset(ws[i]) == onset_class:
                    incoming[get_onset(ws[i-1])] += 1
                    n_receiver += 1

        overall_counts = Counter(get_onset(w) for w in all_words)
        total_overall = len(all_words)

        print(f"\n  Bigrams (sender={n_sender}, receiver={n_receiver}):")
        if n_sender > 0:
            print(f"  Outgoing {onset_class}→X (top 8):")
            for cls, obs in outgoing.most_common(8):
                exp = (mid_counts[cls] / total_mid) * n_sender if total_mid > 0 else 0
                e = obs / exp if exp > 0 else float('inf')
                flag = 'CONF' if e >= 1.5 and obs >= 10 else ('dir' if e >= 2.0 and obs >= 5 else ('(dir)' if e >= 2.5 and obs >= 3 else ('DEPL' if e < 0.7 and obs >= 3 else '')))
                print(f"    {onset_class}→{cls}: obs={obs}, exp={exp:.1f}, E={e:.2f}× {flag}")

        if n_receiver > 0:
            print(f"  Incoming X→{onset_class} (top 8):")
            for cls, obs in incoming.most_common(8):
                exp = (overall_counts[cls] / total_overall) * n_receiver if total_overall > 0 else 0
                e = obs / exp if exp > 0 else float('inf')
                flag = 'CONF' if e >= 1.5 and obs >= 10 else ('dir' if e >= 2.0 and obs >= 5 else ('(dir)' if e >= 2.5 and obs >= 3 else ('DEPL' if e < 0.7 and obs >= 3 else '')))
                print(f"    {cls}→{onset_class}: obs={obs}, exp={exp:.1f}, E={e:.2f}× {flag}")

# Analyze ckh and cph
analyze_onset('ckh', lines_A, lines_B, all_A_words, all_B_words)
analyze_onset('cph', lines_A, lines_B, all_A_words, all_B_words)

# Also check skh and sph (also in ONSET_PRIORITY) for completeness
print(f"\n\n=== ADDITIONAL: skh and sph ===")
for onset_class in ['skh', 'sph']:
    all_A_skh = [w for w in all_A_words if get_onset(w) == onset_class]
    all_B_skh = [w for w in all_B_words if get_onset(w) == onset_class]
    print(f"{onset_class}: A={len(all_A_skh)} tokens ({100*len(all_A_skh)/len(all_A_words):.3f}%); B={len(all_B_skh)} tokens ({100*len(all_B_skh)/len(all_B_words):.3f}%)")
    if all_A_skh:
        print(f"  A top-5: {Counter(all_A_skh).most_common(5)}")
    if all_B_skh:
        print(f"  B top-5: {Counter(all_B_skh).most_common(5)}")

# Summary comparison of all compound gallows
print(f"\n\n=== COMPOUND GALLOWS SUMMARY ===")
print(f"{'Class':<8} {'A tokens':<12} {'A%':<8} {'B tokens':<12} {'B%':<8} {'A pos1 KNOWN'}")
for cls in ['cth', 'ckh', 'cph', 'sch', 'skh', 'sph']:
    a_tok = [w for w in all_A_words if get_onset(w) == cls]
    b_tok = [w for w in all_B_words if get_onset(w) == cls]
    print(f"{cls:<8} {len(a_tok):<12} {100*len(a_tok)/len(all_A_words):<8.3f} {len(b_tok):<12} {100*len(b_tok)/len(all_B_words):<8.3f}")
