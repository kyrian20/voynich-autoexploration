"""
exp_567: ok-onset full characterization (H_new_GE)
ok = words starting with "ok" (after qok in ONSET_PRIORITY)
Parts:
1. Vocabulary (top-20 ok words, A and B)
2. Positional distribution (pos1/MID/LL/LF vs baseline)
3. ok within-line bigrams (outgoing and incoming)
4. ok-LF pos1 profile
"""

import re
from collections import Counter

CORPUS = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'
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

print("\n=== PART 1: ok vocabulary ===")
for words, label in [(all_A_words, "A herbal_a"), (all_B_words, "B all")]:
    total = len(words)
    ok_words = [w for w in words if get_onset(w) == 'ok']
    print(f"\n{label}: {len(ok_words)} ok tokens ({100*len(ok_words)/total:.2f}% of {total})")
    wc = Counter(ok_words)
    print(f"  Unique types: {len(wc)}")
    print(f"  Top-15: {', '.join(f'{w}:{c}({100*c/len(ok_words):.1f}%)' for w,c in wc.most_common(15))}")

print("\n=== PART 2: ok positional ===")
for lines, label in [(lines_A, "A herbal_a"), (lines_B, "B all")]:
    pc = {'pos1':0,'MID':0,'LL':0,'LF':0}
    tc = {'pos1':0,'MID':0,'LL':0,'LF':0}
    for fo, ws in lines:
        L = len(ws); onsets = [get_onset(w) for w in ws]
        tc['pos1']+=1
        if onsets[0]=='ok': pc['pos1']+=1
        if L>=2:
            tc['LF']+=1; tc['LL']+=1
            if onsets[-1]=='ok': pc['LF']+=1
            if onsets[-2]=='ok': pc['LL']+=1
        for i in range(1,L-1):
            tc['MID']+=1
            if onsets[i]=='ok': pc['MID']+=1
    mr = pc['MID']/tc['MID'] if tc['MID']>0 else 0
    print(f"\n{label} MID={pc['MID']}/{tc['MID']}={mr:.4f}:")
    for pos in ['pos1','LL','LF']:
        obs=pc[pos]; tot=tc[pos]; exp=mr*tot
        e=(obs/tot)/mr if mr>0 and tot>0 else 0
        flag='CONF' if e>=1.5 and obs>=10 else ('dir' if e>=2.0 and obs>=5 else ('(dir)' if e>=2.5 and obs>=3 else ('DEPL' if e<0.7 and obs>=3 else '')))
        print(f"  {pos}: obs={obs}/{tot}, exp={exp:.1f}, E={e:.2f}× {flag}")

print("\n=== PART 3: ok bigrams ===")
for lines, all_words, label in [(lines_A, all_A_words, "A herbal_a"), (lines_B, all_B_words, "B all")]:
    mid_counts = Counter()
    total_mid = 0
    for fo, ws in lines:
        for i in range(1, len(ws)-1):
            mid_counts[get_onset(ws[i])] += 1; total_mid += 1
    outgoing = Counter(); n_sender = 0
    for fo, ws in lines:
        for i in range(len(ws)-1):
            if get_onset(ws[i])=='ok':
                outgoing[get_onset(ws[i+1])]+=1; n_sender+=1
    incoming = Counter(); n_receiver = 0
    for fo, ws in lines:
        for i in range(1,len(ws)):
            if get_onset(ws[i])=='ok':
                incoming[get_onset(ws[i-1])]+=1; n_receiver+=1
    overall = Counter(get_onset(w) for w in all_words)
    total_overall = len(all_words)
    print(f"\n{label} (sender={n_sender}, receiver={n_receiver}):")
    print("  Outgoing ok→X (top 12):")
    for cls,obs in outgoing.most_common(12):
        exp=(mid_counts[cls]/total_mid)*n_sender if total_mid>0 else 0
        e=obs/exp if exp>0 else 0
        flag='CONF' if e>=1.5 and obs>=10 else ('dir' if e>=2.0 and obs>=5 else ('(dir)' if e>=2.5 and obs>=3 else ('DEPL' if e<0.7 and obs>=3 else '')))
        print(f"    ok→{cls}: obs={obs}, exp={exp:.1f}, E={e:.2f}× {flag}")
    print("  Incoming X→ok (top 12):")
    for cls,obs in incoming.most_common(12):
        exp=(overall[cls]/total_overall)*n_receiver if total_overall>0 else 0
        e=obs/exp if exp>0 else 0
        flag='CONF' if e>=1.5 and obs>=10 else ('dir' if e>=2.0 and obs>=5 else ('(dir)' if e>=2.5 and obs>=3 else ('DEPL' if e<0.7 and obs>=3 else '')))
        print(f"    {cls}→ok: obs={obs}, exp={exp:.1f}, E={e:.2f}× {flag}")

print("\n=== PART 4: ok-LF pos1 ===")
for lines, label in [(lines_A, "A herbal_a"), (lines_B, "B all")]:
    ok_lf = [(fo,ws) for fo,ws in lines if len(ws)>=2 and get_onset(ws[-1])=='ok']
    print(f"\n{label}: ok-LF lines: {len(ok_lf)}")
    if len(ok_lf)<5: print("  Underpowered."); continue
    pos1_counts = Counter(get_onset(ws[0]) for fo,ws in ok_lf)
    a_pos1 = Counter(get_onset(ws[0]) for fo,ws in lines if len(ws)>=2)
    total_base=sum(a_pos1.values()); total_ok_lf=sum(pos1_counts.values())
    print("  Pos1 distribution (top 10):")
    for cls,obs in pos1_counts.most_common(10):
        base=a_pos1[cls]/total_base if total_base>0 else 0
        e=(obs/total_ok_lf)/base if base>0 else 0
        flag='CONF' if e>=1.5 and obs>=10 else ('dir' if e>=2.0 and obs>=5 else ('(dir)' if e>=2.5 and obs>=3 else ('DEPL' if e<0.7 and obs>=3 else '')))
        print(f"    {cls}@pos1: {obs} (E={e:.2f}×) {flag}")
