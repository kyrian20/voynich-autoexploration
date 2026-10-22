#!/usr/bin/env python3
"""Read-only exact-byte inventory and frozen EXP607 full-line overlap sensitivity."""
from __future__ import annotations
import collections
import hashlib
import json
import io
import tarfile
from pathlib import Path
import re
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_token_policy_sensitivity import read_records
from scripts.audit_exp607_reader_sensitivity import reconstruct_native_words, native
from scripts.audit_exp607_scope_sensitivity import is_test, evaluate
from scripts.ivtff_lossless import tokens
PROTOCOL = 'research/maintenance/2026-10-22-duplicate-control/PROTOCOL.md'


def partition(rows, words, ids, scope):
    train, test = [], []
    for key in sorted(ids, key=lambda k: rows[k]['source_line']):
        row = rows[key]
        if scope == 'P0' and row['locus'] != 'P0':
            continue
        (test if is_test(row['folio']) else train).append(
            (key, row['folio'], tuple(words[key])))
    if {r[1] for r in train} & {r[1] for r in test}:
        raise ValueError('Folio leakage')
    return train, test


def exclude_shared(train, test):
    train_words = {r[2] for r in train}
    removed = [r for r in test if r[2] in train_words]
    kept = [r for r in test if r[2] not in train_words]
    return kept, removed


def grouped(rows):
    groups = collections.defaultdict(list)
    for _, folio, words in rows:
        groups[folio].append(list(words))
    return sorted(groups.items())


def summarize(rows):
    return {'lines': len(rows), 'tokens': sum(len(r[2]) for r in rows),
            'folios': sorted({r[1] for r in rows}),
            'id_set_sha256': hashlib.sha256(('\n'.join(sorted(r[0] for r in rows))+'\n').encode()).hexdigest()}


def inventory():
    archive = subprocess.check_output(['git', 'archive', 'HEAD'], cwd=ROOT)
    snapshot = tarfile.open(fileobj=io.BytesIO(archive))
    files, hashes, empty = [], collections.defaultdict(list), []
    for member in sorted((m for m in snapshot.getmembers() if m.isfile()), key=lambda m: m.name):
        name = member.name
        raw = snapshot.extractfile(member).read()
        digest = hashlib.sha256(raw).hexdigest()
        files.append({'path': name, 'bytes': len(raw), 'sha256': digest})
        (hashes[digest] if raw else empty).append(name)
    return {'scope': 'Exact git archive HEAD bytes; all working changes excluded',
            'file_count': len(files), 'files': files, 'empty_files': empty,
            'nonempty_exact_duplicate_groups': [
                {'sha256': h, 'paths': p} for h,p in sorted(hashes.items()) if len(p)>1]}


def audit(label, relative):
    raw, source_rows = read_records(ROOT / relative)
    source_rows = [r for r in source_rows if re.fullmatch(r'f\d+[rv]', r['folio'])]
    records = {r['id']: r for r in source_rows}
    if len(records) != len(source_rows):
        raise ValueError('Duplicate physical IDs')
    profiles = {'native_607': {}, 'candidate_conservative_ascii': {}}
    for row in source_rows:
        old = reconstruct_native_words(row['body'])
        new = [w for w in tokens([row['payload']]) if re.fullmatch('[a-z]{2,}', w)]
        for profile, words in zip(profiles.values(), (old, new)):
            if len(words)>=2:
                profile[row['id']] = words
    ids = set.intersection(*(set(p) for p in profiles.values()))
    result = {}
    for name, words in profiles.items():
        result[name] = {}
        for scope in ('mixed', 'P0'):
            train, test = partition(records, words, ids, scope)
            kept, removed = exclude_shared(train, test)
            result[name][scope] = {
                'train': summarize(train), 'test_before': summarize(test),
                'test_after': summarize(kept),
                'excluded': [{'id': key, 'folio': folio, 'tokens': list(ws)} for key,folio,ws in removed],
                'before': evaluate(grouped(train), grouped(test)),
                'after': evaluate(grouped(train), grouped(kept))}
    return {'source':relative, 'transcription':label,
            'source_sha256':hashlib.sha256(raw).hexdigest(),
            'common_records':len(ids), 'profiles':result}


def main():
    if (native.ALPHA, native.BIGRAM_WEIGHT, native.TEST_MOD) != (.1,.5,5):
        raise ValueError('Model drift')
    print(json.dumps({'audit':'exact_duplicates_and_EXP607_full_line_overlap',
        'status':'exploratory', 'source_commit':subprocess.check_output(
            ['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'protocol':PROTOCOL, 'protocol_sha256':hashlib.sha256((ROOT/PROTOCOL).read_bytes()).hexdigest(),
        'inventory':inventory(), 'files':[audit(*src) for src in native.FILES],
        'limits':['Exact byte duplicates are candidates for review, not errors.',
                  'Repeated full token sequences may be authentic manuscript text.',
                  'No partial-overlap, model-selection or independent-transcription validation.']},
        indent=2,ensure_ascii=False))
if __name__=='__main__':
    main()
