"""
exp_439: Hapax Section Distribution (H_new_C) and No-Suffix Hapax Analysis (H_new_D)

H_new_C: Are hapax words section-specific? Does B astro/pharma have higher hapax rate?
H_new_D: Are 'no-suffix' hapaxes (20-22%) concentrated in 'other'-onset words?
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

ONSETS = ['qok', 'qot', 'qo', 'cth', 'ch', 'sh', 'ok', 'ot', 'ol',
          'd', 's', 'y', 'k', 't', 'l', 'r', 'p', 'f', 'o']

SUFFIXES = [
    'aiin', 'aiir', 'ain', 'air', 'aii',
    'eedy', 'edy', 'eey', 'ey',
    'ckhy', 'ckh', 'cthy', 'cth',
    'chedy', 'chey', 'chol', 'cheol', 'cheor', 'chor', 'cho', 'ch',
    'shedy', 'shey', 'shol', 'shor', 'sho', 'sh',
    'dy', 'y',
    'ar', 'or', 'ol', 'al',
    'am', 'om',
    'iin', 'iir', 'in',
    'l', 'r', 'n',
]
SUFFIXES.sort(key=lambda x: -len(x))

def get_onset(word):
    for on in ONSETS:
        if word.startswith(on):
            return on
    return 'other'

def strip_suffix(body):
    for s in SUFFIXES:
        if body.endswith(s) and len(body) > len(s):
            return body[:-len(s)], s
        elif body == s:
            return '', s
    return body, ''

def get_section(folio):
    m = re.match(r'f(\d+)', folio)
    if not m: return 'other'
    n = int(m.group(1))
    if n <= 72: return 'herbal'
    elif n <= 84: return 'astro'
    elif n <= 102: return 'bio'
    elif n <= 116: return 'pharma'
    return 'other'

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

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)
    
    # Build global word frequency per dialect
    word_counts = {'A': Counter(), 'B': Counter()}
    for folio, lines in folios.items():
        d = dialect_map.get(folio)
        if d not in ('A', 'B'): continue
        for ws in lines:
            for w in ws:
                word_counts[d][w] += 1
    
    # H_new_C: B-dialect hapax rate by section
    print("=== H_new_C: B-dialect hapax rate by section ===")
    section_counts = defaultdict(lambda: [0, 0])  # [total_tokens, hapax_tokens]
    for folio, lines in folios.items():
        if dialect_map.get(folio) != 'B': continue
        sec = get_section(folio)
        for ws in lines:
            for w in ws:
                section_counts[sec][0] += 1
                if word_counts['B'][w] == 1:
                    section_counts[sec][1] += 1
    
    total_B = sum(v[0] for v in section_counts.values())
    hapax_B = sum(v[1] for v in section_counts.values())
    global_hapax_rate = hapax_B / total_B if total_B else 0
    print(f"  B overall: {hapax_B}/{total_B} = {global_hapax_rate:.1%} hapax tokens")
    
    for sec in ['herbal', 'astro', 'bio', 'pharma']:
        total, hapax = section_counts[sec]
        if total == 0: continue
        rate = hapax / total
        E = rate / global_hapax_rate if global_hapax_rate > 0 else 0
        print(f"  {sec:<8}: {hapax}/{total} = {rate:.1%} (E={E:.2f}×)")
    
    # H_new_D: Are no-suffix hapaxes concentrated in 'other'-onset words?
    print("\n=== H_new_D: No-suffix hapax analysis (both dialects) ===")
    for target_dial in ['A', 'B']:
        hapax_words = [w for w, c in word_counts[target_dial].items() if c == 1]
        
        # Classify by onset and suffix
        other_onset_nosuf = 0
        other_onset_total = 0
        recog_onset_nosuf = 0
        recog_onset_total = 0
        
        for w in hapax_words:
            on = get_onset(w)
            body = w[len(on) if on != 'other' else 0:]
            if on == 'other':
                body = w
            _, sf = strip_suffix(body)
            
            if on == 'other':
                other_onset_total += 1
                if sf == '':
                    other_onset_nosuf += 1
            else:
                recog_onset_total += 1
                if sf == '':
                    recog_onset_nosuf += 1
        
        total_hapax = len(hapax_words)
        total_nosuf = other_onset_nosuf + recog_onset_nosuf
        
        print(f"\n  Dialect {target_dial}: {total_hapax} hapax types")
        print(f"  'other'-onset: {other_onset_total} ({other_onset_total/total_hapax:.1%} of hapaxes)")
        if other_onset_total > 0:
            print(f"    - no-suffix: {other_onset_nosuf}/{other_onset_total} = {other_onset_nosuf/other_onset_total:.1%}")
        print(f"  recognized-onset: {recog_onset_total} ({recog_onset_total/total_hapax:.1%} of hapaxes)")
        if recog_onset_total > 0:
            print(f"    - no-suffix: {recog_onset_nosuf}/{recog_onset_total} = {recog_onset_nosuf/recog_onset_total:.1%}")
        print(f"  Overall no-suffix hapax rate: {total_nosuf}/{total_hapax} = {total_nosuf/total_hapax:.1%}")

if __name__ == '__main__':
    main()
