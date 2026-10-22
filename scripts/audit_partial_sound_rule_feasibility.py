#!/usr/bin/env python3
"""Limited, set-valued operationalization of published approximate sound rules.

This is not a decoder, a full implementation of Bax, or a semantic validator.
Unknown units and unresolved sounds are never silently completed.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = 'research/decipherment/2026-10-22-f41v-feasibility/PROTOCOL.md'
# IPA values are approximate proposals from Bax (2014), Appendix 1.
# R_PLUS_UNSPECIFIED_VOWEL and R_CONTEXT_UNRESOLVED are unresolved markers.
RULES = {
    'k': ['k'], 'y': ['n'], 'd': ['t', 'd', 'θ', 'ð'],
    'r': ['r', 'R_PLUS_UNSPECIFIED_VOWEL'],
    'm': ['R_CONTEXT_UNRESOLVED'],
    'n': ['r', 'R_PLUS_UNSPECIFIED_VOWEL'],
    'sh': ['kʰ', 'x', 'tʃ'], 's': ['s'],
    'o': ['a'], 'a': ['ə', 'u', 'wa'],
    'in': ['ir'], 'iin': ['ur'], 'e': ['o']}
TARGETS = ('ytoail','keeredal','keerodal','otaim','dam','alam',
           'otaimdam','kydainy','kydain')
KEYS = sorted(RULES, key=lambda key: (-len(key), key))


def inspect_word(word):
    units = []
    offset = 0
    while offset < len(word):
        match = next((key for key in KEYS if word.startswith(key, offset)), None)
        if match is None:
            units.append({'raw': word[offset], 'start': offset, 'end': offset+1,
                          'kind': 'unmapped', 'proposed_sounds': []})
            offset += 1
        else:
            units.append({'raw': match, 'start': offset, 'end': offset+len(match),
                          'kind': 'mapped_approximate', 'proposed_sounds': RULES[match]})
            offset += len(match)
    return {
        'token': word, 'units': units,
        'unmapped_characters': sorted({u['raw'] for u in units if u['kind']=='unmapped'}),
        'positions_with_multiple_proposals': [u['start'] for u in units if len(u['proposed_sounds'])>1],
        'unresolved_context_positions': [
            u['start'] for u in units if any('UNRESOLVED' in s or 'UNSPECIFIED' in s
                                            for s in u['proposed_sounds'])],
        'repeated_e_duration_not_decided': 'ee' in word,
        'plaintext': None,
        'status': 'UNVALIDATED_PARTIAL_SOUND_PROJECTION'}


def main():
    out = {
        'audit': 'limited_published_sound_rule_feasibility', 'version': 1,
        'source': {'author': 'Stephen Bax', 'year': 2014,
                   'url': 'https://stephenbax.net/wp-content/uploads/2014/01/Voynich-a-provisional-partial-decoding-BAX.pdf',
                   'locator': 'Appendix 1, pp. 56–57; f41v pp. 22–25',
                   'access': 'Web full-text extraction; direct local PDF download returned 403; no local PDF rendering completed.'},
        'protocol': PROTOCOL,
        'protocol_sha256': hashlib.sha256((ROOT/PROTOCOL).read_bytes()).hexdigest(),
        'rules': RULES,
        'implementation_choices': [
            'Longest available key first, including in/iin/sh; no glyph insertion/deletion.',
            'Repeated e kept as separate units; duration/coalescence unimplemented.',
            'Unknown symbols retained at exact offsets; no analogy-based gallows mappings.',
            'Sound alternatives and undefined contexts remain unresolved.',
            'No lexicon search, language model ranking or name fitting.'],
        'targets': [inspect_word(word) for word in TARGETS],
        'limitations': [
            'This subset is not the full author proposal; failure is conditional on this operationalization.',
            'The plant identity and exact historical name are not verified.',
            'Sound coverage or apparent pronounceability does not establish plaintext.',
            'No held-out semantic prediction or independent decipherment test is performed.']}
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()

