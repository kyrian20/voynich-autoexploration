"""
exp_440: Cross-Position Word Identity vs Onset-Class Overlap (H496)

Q: What fraction of cross-position token overlap is from identical word types
   vs same onset class (different word)? If onset class alone explains the overlap,
   positional grammar selects onset class first, then picks different words per position.

Method:
- For each word token in LF/MID/LL positions, record: word, onset class, position
- Compute: P(word appears in other positions) vs P(onset class appears in other positions)
- Measure type-level overlap vs onset-class-level overlap
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

ONSETS = ['qok', 'qot', 'qo', 'cth', 'ch', 'sh', 'ok', 'ot', 'ol',
          'd', 's', 'y', 'k', 't', 'l', 'r', 'p', 'f', 'o']

def get_onset(word):
    for on in ONSETS:
        if word.startswith(on):
            return on
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

def analyze(folios, dialect_map, target_dial):
    # Collect: for each position (LF, MID, LL), set of word types and onset classes
    pos_words = {'LF': Counter(), 'MID': Counter(), 'LL': Counter()}
    pos_onsets = {'LF': Counter(), 'MID': Counter(), 'LL': Counter()}
    
    for folio, lines in folios.items():
        if dialect_map.get(folio) != target_dial: continue
        for ws in lines:
            n = len(ws)
            if n < 2: continue
            # LF
            w = ws[0]
            pos_words['LF'][w] += 1
            pos_onsets['LF'][get_onset(w)] += 1
            # LL
            w = ws[-1]
            pos_words['LL'][w] += 1
            pos_onsets['LL'][get_onset(w)] += 1
            # MID
            for w in ws[1:-1]:
                pos_words['MID'][w] += 1
                pos_onsets['MID'][get_onset(w)] += 1
    
    print(f"\n{'='*60}")
    print(f"Dialect {target_dial}")
    print(f"{'='*60}")
    
    pos_pairs = [('LF', 'MID'), ('MID', 'LL'), ('LF', 'LL')]
    
    for p1, p2 in pos_pairs:
        # Type-level analysis
        types1 = set(pos_words[p1].keys())
        types2 = set(pos_words[p2].keys())
        overlap_types = types1 & types2
        
        # Token-level: fraction of p1 tokens whose word also appears in p2
        tokens_p1 = sum(pos_words[p1].values())
        tokens_in_p2 = sum(pos_words[p1][w] for w in types1 if w in types2)
        
        # Onset-level: fraction of p1 onset classes also in p2
        onsets1 = set(pos_onsets[p1].keys())
        onsets2 = set(pos_onsets[p2].keys())
        overlap_onsets = onsets1 & onsets2
        
        # Decompose: for p1 tokens in p2, break into identical-word vs same-onset-different-word vs different-onset
        # Check each p2 token: does it appear in p1 as identical? as same onset?
        tokens_p2 = sum(pos_words[p2].values())
        tokens_p2_identical = sum(pos_words[p2][w] for w in types2 if w in types1)
        tokens_p2_same_onset_diff_word = sum(
            sum(pos_words[p2][w] for w in types2 if get_onset(w) == on and w not in types1)
            for on in onsets1
        )
        tokens_p2_diff_onset = tokens_p2 - tokens_p2_identical - tokens_p2_same_onset_diff_word
        
        # Null model: if p2 tokens drawn from p2's word distribution independently of p1
        # Expected overlap = sum over p1 types w: P(w in p2) × tokens_p1(w)
        # Actually simpler: just report the observed fractions
        
        print(f"\n  {p1} ↔ {p2}:")
        print(f"    Types: |{p1}|={len(types1)}, |{p2}|={len(types2)}, |overlap|={len(overlap_types)}")
        print(f"    Type overlap rate: {len(overlap_types)/len(types1):.1%} of {p1} types also in {p2}")
        print(f"    Token overlap: {tokens_in_p2}/{tokens_p1} = {tokens_in_p2/tokens_p1:.1%} of {p1} tokens use words also in {p2}")
        
        print(f"    {p2} token decomposition ({tokens_p2} total):")
        print(f"      identical word (in {p1}): {tokens_p2_identical}/{tokens_p2} = {tokens_p2_identical/tokens_p2:.1%}")
        print(f"      same-onset diff word: {tokens_p2_same_onset_diff_word}/{tokens_p2} = {tokens_p2_same_onset_diff_word/tokens_p2:.1%}")
        print(f"      diff-onset word: {tokens_p2_diff_onset}/{tokens_p2} = {tokens_p2_diff_onset/tokens_p2:.1%}")
        
        # Top shared word types
        top_shared = sorted(overlap_types, key=lambda w: -(pos_words[p1][w] + pos_words[p2][w]))[:5]
        print(f"    Top shared types: {[(w, pos_words[p1][w], pos_words[p2][w]) for w in top_shared]}")
    
    # Top words by position (for reference)
    print(f"\n  Top LF words: {pos_words['LF'].most_common(5)}")
    print(f"  Top MID words: {pos_words['MID'].most_common(5)}")
    print(f"  Top LL words: {pos_words['LL'].most_common(5)}")

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)
    analyze(folios, dialect_map, 'A')
    analyze(folios, dialect_map, 'B')

if __name__ == '__main__':
    main()
