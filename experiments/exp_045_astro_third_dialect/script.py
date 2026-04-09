"""
exp_045: Is the Astro/Cosmo Section a Morphologically Intermediate Third Dialect?
H056: Hand 4 (astro/cosmo) is intermediate between Currier A and B.
Test: vocabulary Jaccard, suffix distances, character distributions.
"""

import re
import math
from collections import defaultdict, Counter

DATA_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"

SUFFIXES = ['aiin', 'ain', 'eedy', 'edy', 'chy', 'eey', 'dy', 'ey', 'y',
            'ol', 'or', 'al', 'ar', 'iin', 'in']
seen = set(); SUFFIXES_DEDUP = []
for s in SUFFIXES:
    if s not in seen: seen.add(s); SUFFIXES_DEDUP.append(s)
SUFFIXES = SUFFIXES_DEDUP

HAND4_FOLIOS = {'f67r1','f67r2','f67v2','f68r1','f68r2','f68v2','f68v3','f69r','f70r2'}


def suffix_group(word):
    for sfx in SUFFIXES:
        if word.endswith(sfx) and len(word) > len(sfx):
            return sfx, word[:-len(sfx)]
    return None, word


def parse_corpus(path):
    folio_data = {}
    current_folio = None
    current_hand = None
    current_currier = None

    with open(path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m_hand = re.search(r'\$H=(\d+)', line)
            if m_hand: current_hand = m_hand.group(1)
            m_cur = re.search(r'\$L=([AB?])', line)
            if m_cur: current_currier = m_cur.group(1)

            m2 = re.match(r'^<([^>]+)>', line)
            if not m2: continue
            parts = m2.group(1).split(',')
            if len(parts) < 2: continue
            folio_m = re.match(r'^(f\d+[rv]\d*)', parts[0].strip())
            if folio_m:
                current_folio = folio_m.group(1)
                if current_folio not in folio_data:
                    folio_data[current_folio] = {'hand': current_hand, 'currier': current_currier, 'words': []}

            if current_folio is None: continue
            locus_base = parts[1].strip().lstrip('+*@=/~&')
            if not locus_base.startswith('P'): continue

            text = line[m2.end():].strip()
            text = re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]
            folio_data[current_folio]['words'].extend(tokens)

    return folio_data


def vocab_stats(words):
    freq = Counter(words)
    types = set(words)
    sfx_count = Counter()
    for w in words:
        sfx, _ = suffix_group(w)
        if sfx: sfx_count[sfx] += 1
    qo_rate = sum(1 for w in words if w.startswith('qo')) / max(len(words), 1)
    return freq, types, sfx_count, qo_rate


def jaccard(set_a, set_b):
    inter = len(set_a & set_b)
    union = len(set_a | set_b)
    return inter / union if union else 0.0


def kl_divergence(p_dist, q_dist, vocab):
    total_p = sum(p_dist.get(w, 0) for w in vocab) or 1
    total_q = sum(q_dist.get(w, 0) for w in vocab) or 1
    kl = 0.0
    for w in vocab:
        p = p_dist.get(w, 0) / total_p
        q = q_dist.get(w, 0) / total_q
        if p > 0 and q > 0:
            kl += p * math.log2(p / q)
    return kl


if __name__ == '__main__':
    print("Loading corpus...")
    folio_data = parse_corpus(DATA_PATH)

    # Build three corpora
    words_a, words_b, words_astro = [], [], []
    for folio, data in folio_data.items():
        if not data['words']: continue
        if folio in HAND4_FOLIOS:
            words_astro.extend(data['words'])
        elif data['currier'] == 'A':
            words_a.extend(data['words'])
        elif data['currier'] == 'B':
            words_b.extend(data['words'])

    print(f"Currier A: {len(words_a)} tokens")
    print(f"Currier B: {len(words_b)} tokens")
    print(f"Astro/Cosmo (Hand 4): {len(words_astro)} tokens")

    freq_a, types_a, sfx_a, qo_a = vocab_stats(words_a)
    freq_b, types_b, sfx_b, qo_b = vocab_stats(words_b)
    freq_astro, types_astro, sfx_astro, qo_astro = vocab_stats(words_astro)

    print(f"\n{'='*55}")
    print(f"VOCABULARY JACCARD DISTANCES")
    j_ab = jaccard(types_a, types_b)
    j_a_astro = jaccard(types_a, types_astro)
    j_b_astro = jaccard(types_b, types_astro)
    print(f"A ↔ B:     Jaccard = {j_ab:.3f}")
    print(f"A ↔ Astro: Jaccard = {j_a_astro:.3f}")
    print(f"B ↔ Astro: Jaccard = {j_b_astro:.3f}")
    print(f"\nIf Astro is intermediate: J(A,Astro) > J(A,B) and J(B,Astro) > J(A,B)")
    print(f"If Astro is closer to A: J(A,Astro) > J(B,Astro)")
    print(f"If Astro is closer to B: J(B,Astro) > J(A,Astro)")

    print(f"\n{'='*55}")
    print(f"SUFFIX DISTRIBUTION COMPARISON")
    core_sfx = ['edy', 'ol', 'ain', 'aiin', 'eedy', 'eey', 'dy', 'ey', 'y', 'or', 'chy']
    total_a_sfx = sum(sfx_a.get(s, 0) for s in core_sfx) or 1
    total_b_sfx = sum(sfx_b.get(s, 0) for s in core_sfx) or 1
    total_astro_sfx = sum(sfx_astro.get(s, 0) for s in core_sfx) or 1

    print(f"\n{'Suffix':<8} {'A%':>7} {'B%':>7} {'Astro%':>9}")
    print('-' * 35)
    for sfx in core_sfx:
        pa = 100 * sfx_a.get(sfx, 0) / total_a_sfx
        pb = 100 * sfx_b.get(sfx, 0) / total_b_sfx
        pastro = 100 * sfx_astro.get(sfx, 0) / total_astro_sfx
        # Is astro between A and B?
        between = (min(pa, pb) <= pastro <= max(pa, pb))
        flag = " <-mid" if between else ""
        print(f"-{sfx:<7} {pa:>7.1f} {pb:>7.1f} {pastro:>9.1f}{flag}")

    print(f"\nqo-rate: A={qo_a:.3f}, B={qo_b:.3f}, Astro={qo_astro:.3f}")
    astro_between_qo = min(qo_a, qo_b) <= qo_astro <= max(qo_a, qo_b)
    print(f"Astro qo-rate between A and B: {astro_between_qo}")

    print(f"\n{'='*55}")
    print(f"CHARACTER DISTRIBUTION COMPARISON")
    def char_dist(words):
        c = Counter()
        for w in words:
            for ch in w:
                c[ch] += 1
        total = sum(c.values())
        return {ch: n/total for ch, n in c.items()}

    chars_a = char_dist(words_a)
    chars_b = char_dist(words_b)
    chars_astro = char_dist(words_astro)
    all_chars = set(chars_a) | set(chars_b) | set(chars_astro)

    kl_a_b = kl_divergence(Counter(words_a), Counter(words_b), set(words_a)|set(words_b))
    kl_a_astro = kl_divergence(Counter(words_a), Counter(words_astro), set(words_a)|set(words_astro))
    kl_b_astro = kl_divergence(Counter(words_b), Counter(words_astro), set(words_b)|set(words_astro))

    print(f"\nWord-level KL divergences:")
    print(f"  KL(A || B) = {kl_a_b:.3f} bits")
    print(f"  KL(A || Astro) = {kl_a_astro:.3f} bits")
    print(f"  KL(B || Astro) = {kl_b_astro:.3f} bits")
    print(f"  If Astro is intermediate: KL(A||Astro) < KL(A||B) and KL(B||Astro) < KL(A||B)")

    print(f"\n{'='*55}")
    print(f"TOP WORDS SHARED BETWEEN GROUPS")
    print(f"\nTop 15 words in Astro/Cosmo:")
    for word, cnt in Counter(words_astro).most_common(15):
        in_a = freq_a.get(word, 0)
        in_b = freq_b.get(word, 0)
        print(f"  {word}: {cnt} (A:{in_a}, B:{in_b})")

    # Words unique to Astro
    astro_unique = types_astro - types_a - types_b
    print(f"\nWords unique to Astro (not in A or B): {len(astro_unique)}")
    print(f"Astro words also in A only: {len(types_astro & types_a - types_b)}")
    print(f"Astro words also in B only: {len(types_astro & types_b - types_a)}")
    print(f"Astro words in both A and B: {len(types_astro & types_a & types_b)}")
