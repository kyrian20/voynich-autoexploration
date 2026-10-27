#!/usr/bin/env python3
"""Replay four explicitly selected input readers without importing experiments."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import sys

# CLI execution from scripts/ and direct test imports must use the same guard.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.audit_corpus_identity_overlay import audit as audit_identity_overlay
from scripts.check_corpus_integrity import unique_keys

ROOT = Path(__file__).resolve().parents[1]
BASE = 'aa9ec5399e7a5cdf8d1b2890fa657f1358825b41'
CICERO = 'data/reference_corpora/latin/cicero_de_officiis_latin.txt'
VULGATE = 'data/reference_corpora/latin/vulgate.txt'
CASES = [('exp_267_word_length_position', CICERO),
         ('exp_288_stolfi_onset_decomp', CICERO),
         ('exp_001_word_initial_entropy', VULGATE),
         ('exp_170_naibbe_simulation', VULGATE)]

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def select(tree, experiment):
    if experiment.startswith(('exp_001', 'exp_170')):
        name = 'parse_natural_language' if experiment.startswith('exp_001') else 'load_plaintext'
        nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
        if len(nodes) != 1:
            raise ValueError('Reader selection changed')
        return nodes, name
    container = tree.body
    variable = 'LATIN_CORPUS'
    if experiment.startswith('exp_288'):
        guards = [n for n in tree.body if isinstance(n, ast.If) and ast.unparse(n.test) == "__name__ == '__main__'"]
        if len(guards) != 1:
            raise ValueError('Main guard changed')
        tries = [n for n in guards[0].body if isinstance(n, ast.Try)]
        if len(tries) != 1:
            raise ValueError('Reader try block changed')
        container = tries[0].body
        variable = 'LATIN_PATH'
    starts = [i for i,n in enumerate(container) if isinstance(n, ast.With) and variable in ast.unparse(n)]
    if len(starts) != 1:
        raise ValueError('Inline reader changed')
    # Explicit fixed slices: file read + tokenizer, or read + tokenizer + records + loop.
    nodes = container[starts[0]:starts[0]+(4 if experiment.startswith('exp_288') else 2)]
    if len(nodes) != (4 if experiment.startswith('exp_288') else 2):
        raise ValueError('Truncated reader')
    return nodes, None

def replay(experiment, path, corpus):
    source = path.read_bytes()
    nodes, function = select(ast.parse(source.decode('utf-8')), experiment)
    # Read-only execution environment; only the extracted historical reader executes.
    def readonly_open(candidate, *args, **kwargs):
        if Path(candidate).resolve() != corpus.resolve():
            raise ValueError('Unexpected input')
        if (args[0] if args else kwargs.get('mode', 'r')) != 'r':
            raise ValueError('Unexpected write mode')
        return open(candidate, *args, **kwargs)
    class ReadPath:
        def __init__(self, candidate):
            if Path(candidate).resolve() != corpus.resolve():
                raise ValueError('Unexpected Path input')
        def read_text(self, **kwargs):
            return corpus.read_text(**kwargs)
    ns = {'re': re, 'Path': ReadPath, 'open': readonly_open,
          'LATIN_CORPUS': str(corpus), 'LATIN_PATH': str(corpus)}
    exec(compile(ast.Module(body=nodes,type_ignores=[]), str(path), 'exec'), ns)
    text = corpus.read_text(encoding='utf-8')
    if function:
        actual = ns[function](str(corpus))
    elif experiment.startswith('exp_267'):
        actual = ns['latin_words']
    else:
        actual = ns['lat_recs']
    # Independent reconstruction uses token spans/line predicates, not the original function.
    if experiment.startswith('exp_267'):
        expected = [m.group() for m in re.finditer(r'\b[A-Za-z]{2,}\b', text)]
    elif experiment.startswith('exp_288'):
        expected = []
        for m in re.finditer('[A-Za-z]+',text):
            word = m.group().lower()
            if len(word) < 3:
                continue
            vowel_run = re.match('[aeiou]*',word).end()
            consonant_run = re.match('[^aeiou]*',word[vowel_run:]).end()
            end = vowel_run + consonant_run
            body = word[end:] if end else word
            expected.append({'onset':word[vowel_run:end] if consonant_run else 'V',
                             'wlen':len(word), 'blen':len(body), 'mlen':max(0,len(body)-2)})
    elif experiment.startswith('exp_170'):
        expected = [line.strip() for line in text.splitlines()
                    if sum(ch.isalpha() for ch in line.strip()) >= 3]
    else:
        # Reconstruct the historical coordinate bug literally, then compare to a corrected crop.
        start = re.search(r'\*\*\* START OF', text)
        end = re.search(r'\*\*\* END OF', text)
        begin = start.end() if start else 0
        historical_text = text[begin:]
        if end:
            historical_text = historical_text[:end.start()]
        expected = re.findall('[A-Za-z]+',historical_text.lower())
    if actual != expected:
        raise ValueError('Independent reader mismatch: '+experiment)
    row = {'experiment_path':path.relative_to(ROOT).as_posix(),
           'script_sha256':sha(source), 'reader_ast_sha256':sha(ast.dump(ast.Module(body=nodes,type_ignores=[]),include_attributes=False).encode()),
           'corpus':corpus.relative_to(ROOT).as_posix(), 'corpus_sha256':sha(corpus.read_bytes()),
           'status':'ISOLATED_READER_REPLAY_MATCHED', 'selected_units':len(actual),
           'unit':'lines' if experiment.startswith('exp_170') else ('onset_records' if experiment.startswith('exp_288') else 'tokens'),
           'sequence_sha256':sha(json.dumps(actual,ensure_ascii=False,separators=(',',':')).encode()),
           'first_units':actual[:5], 'last_units':actual[-5:]}
    if experiment.startswith('exp_001'):
        corrected_text = text[begin:end.start() if end else len(text)]
        corrected = re.findall('[A-Za-z]+',corrected_text.lower())
        row['gutenberg_coordinate_check'] = {'start_marker_end':begin,'end_marker_start':end.start() if end else None,
             'historical_selected_characters':len(historical_text), 'coordinate_corrected_characters':len(corrected_text),
             'coordinate_corrected_tokens':len(corrected),'token_delta':len(actual)-len(corrected),
             'note':'Coordinate correction only; the remainder of the START title line is still retained. No clean-body claim.'}
    return row

def load_verified_reference_metadata(root):
    """Validate both frozen manifest and identity overlay before replay.

    The old dictionary comprehension silently accepted duplicate paths and
    unreviewed identity changes when this CLI was used outside the full CI.
    Do not reclassify a corpus or replace any historical input here.
    """
    manifest = json.loads((root/'research/CORPUS_INPUT_MANIFEST.json').read_text(encoding='utf-8'),
                          object_pairs_hook=unique_keys)
    review = json.loads((root/'research/CORPUS_IDENTITY_REVIEW.json').read_text(encoding='utf-8'),
                        object_pairs_hook=unique_keys)
    errors = audit_identity_overlay(root, manifest, review)
    if errors:
        raise ValueError('Frozen reference provenance failed: ' + '; '.join(errors))
    return {row['path']: row for row in review['excluded_from_new_language_baselines']}


def compute():
    metadata = load_verified_reference_metadata(ROOT)
    for corpus in {c for e,c in CASES}:
        if sha((ROOT/corpus).read_bytes()) != metadata[corpus]['sha256']:
            raise ValueError('Frozen corpus changed: '+corpus)
    rows = [replay(e,ROOT/'experiments'/e/'script.py',ROOT/c) for e,c in CASES]
    for row in rows:
        row['adjudicated_language'] = metadata[row['corpus']]['adjudicated_language']
        row['identity_issue'] = metadata[row['corpus']]['issue']
    return {'source_commit':BASE, 'cases':rows,
            'scope':'Input readers only; no manuscript parser, metrics, simulations or historical conclusions revalidated. Cicero remains bilingual and excluded from monolingual baselines. Vulgate identity remains subject to the corpus review.'}

def main():
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--out',type=Path)
    group.add_argument('--check',type=Path)
    args=parser.parse_args()
    result=compute()
    if args.check:
        if result != json.loads(args.check.read_text()):
            raise SystemExit('Remaining-reader diagnostic changed')
    else:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'matched':len(result['cases']), 'units':[(r['experiment_path'],r['selected_units']) for r in result['cases']]}))

if __name__=='__main__':
    main()
