#!/usr/bin/env python3
"""Bounded, reproducible reading attempt; never emits invented plaintext."""
import hashlib
import json
import random
import re
from pathlib import Path
from audit_token_policy_sensitivity import read_records, project, FULL
from audit_partial_sound_rule_feasibility import inspect_word

ROOT = Path(__file__).resolve().parents[1]
SEED = 20261023

def run():
    path = ROOT/'data/transcriptions/eva_zl3b.txt'
    candidates = []
    for line in path.read_text().splitlines():
        m = re.match(r'^<([^>]+)>\s+(.*)',line)
        if m and re.search(r',.P0$',m[1]):
            candidates.append((m[1],m[2]))
    index = random.Random(SEED).randrange(len(candidates))
    selected, body = candidates[index]
    locus = selected.split(',')[0]
    sources = []
    targets = ('dshor','ytchol','shy','o','qotchy','otchy','dar')
    for name in ('eva_zl3b.txt','eva_it2a.txt','zl3a.txt'):
        raw, rows = read_records(ROOT/'data/transcriptions'/name)
        row = next(r for r in rows if r['id'] == locus)
        views = {policy: project(row['payload'],FULL,join_commas=policy=='join') for policy in ('split','join')}
        concordances = {}
        for policy in ('split','join'):
            records = [(r,project(r['payload'],FULL,join_commas=policy=='join')) for r in rows if r['locus']=='P0']
            concordances[policy] = {
                target: {'occurrences':sum(words.count(target) for _,words in records),
                         'folio_count':len({r['folio'] for r,words in records if target in words}),
                         'contexts':[{'id':r['id'],'tokens':words} for r,words in records if target in words][:8]}
                for target in targets}
            concordances[policy]['qotchy_otchy_pair'] = [r['id'] for r,words in records
                if any(a=='qotchy' and b=='otchy' for a,b in zip(words,words[1:]))]
        sources.append({'path':name,'sha256':hashlib.sha256(raw).hexdigest(),
                        'raw_body':row['body'],'views':views,'concordances':concordances})
    return {'status':'NO_JUSTIFIED_TRANSLATION','selection':{'seed':SEED,'candidate_count':len(candidates),
            'zero_based_index':index,'selected':selected,'raw_body':body},'sources':sources,
            'limited_prior_sound_projection':[inspect_word(t) for t in targets],
            'image':{'url':'https://collections.library.yale.edu/iiif/2/1006160/full/full/0/default.jpg',
                     'folio':'44r','inspection':'Plant drawing and three text blocks observed; no botanical identification or definitive glyph adjudication.'},
            'plaintext':None,'limits':['P0 records only; the selection is not uniform over sentences or folios.',
              'Fixed seed chosen by analyst; repeatable pseudorandom draw, not cryptographic randomness.',
              'Full projection preserves high-ASCII markers, with primary alternatives/expanded ligatures; not paleographic adjudication.',
              'The inherited sound rules are a limited unvalidated subset, not a full implementation of Bax.',
              'Character similarity and distributional counts establish no word meanings.']}

if __name__ == '__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2))
