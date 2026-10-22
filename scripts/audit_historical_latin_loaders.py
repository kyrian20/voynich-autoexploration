#!/usr/bin/env python3
"""Replay isolated historical Cicero loaders, never experiment module bodies.

This is a diagnostic, not a language detector or a historical claim retraction.
Only explicitly selected local functions and literal stopword constants compile.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import random
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'data/reference_corpora/latin/cicero_de_officiis_latin.txt'
NAMES = {'load_latin', 'extract_latin_words', 'extract_latin_sentences', 'parse_latin'}

def digest(value):
    return hashlib.sha256(value).hexdigest()

def replay(path, corpus):
    source = path.read_text(encoding='utf-8')
    tree = ast.parse(source)
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in NAMES]
    row = {'script': path.relative_to(ROOT).as_posix(), 'script_sha256': digest(path.read_bytes())}
    if len(functions) != 1:
        return dict(row, status='NOT_REPLAYED_NO_UNIQUE_SELECTED_LOADER')
    function = functions[0]
    namespace = {'re': re, 'random': random.Random(20261022)}
    # Do not execute imports, assignments with side effects, or experiment bodies.
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in {'ENGLISH_SW', 'ENGLISH_STOPWORDS'}:
                namespace[name] = ast.literal_eval(node.value)
            elif name == 'LATIN_CLAUSE_FINAL':
                call = node.value
                if not (isinstance(call, ast.Call) and ast.unparse(call.func) == 're.compile' and len(call.args) in (1, 2)):
                    raise ValueError('Unexpected regex definition')
                flags = re.I if len(call.args) == 2 and ast.unparse(call.args[1]) == 're.I' else 0
                namespace[name] = re.compile(ast.literal_eval(call.args[0]), flags)
    def readonly_open(candidate, *args, **kwargs):
        if Path(candidate).resolve() != corpus.resolve():
            raise ValueError('Loader attempted another input')
        mode = args[0] if args else kwargs.get('mode', 'r')
        if mode != 'r':
            raise ValueError('Non-read mode')
        return open(candidate, *args, **kwargs)
    namespace['open'] = readonly_open
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(path), 'exec'), namespace)
    observed = {}
    def trace(frame, event, arg):
        if frame.f_code is not namespace[function.name].__code__:
            return None
        frame.f_trace_lines = False
        if event == 'return' and frame.f_code is namespace[function.name].__code__:
            observed.update(frame.f_locals)
        return trace
    previous = sys.gettrace()
    try:
        sys.settrace(trace)
        output = namespace[function.name](str(corpus))
    finally:
        sys.settrace(previous)
    stopwords = next((observed[n] for n in ('english_stopwords',) if n in observed), None)
    if stopwords is None:
        stopwords = namespace.get('ENGLISH_SW', namespace.get('ENGLISH_STOPWORDS'))
    unfiltered = function.name == 'parse_latin'
    if not unfiltered and not isinstance(stopwords, set):
        raise ValueError('Unknown filter')
    paragraphs = re.split(r'\n\s*\n', corpus.read_text(encoding='utf-8'))
    minimum = 5 if 'ENGLISH_STOPWORDS' in namespace else 1
    normalize = 'ENGLISH_STOPWORDS' in namespace
    retained = []
    expected = []
    offset = 0
    text = corpus.read_text(encoding='utf-8')
    for index, paragraph in enumerate(paragraphs):
        start = text.find(paragraph, offset)
        offset = start + len(paragraph)
        words = re.findall(r'[a-zA-Z]+' if unfiltered else r'\b[a-zA-Z]+\b', paragraph)
        if len(words) < minimum:
            continue
        ratio = None if unfiltered else sum(w.lower() in stopwords for w in words) / len(words)
        if unfiltered or ratio < .08:
            tokens = [w.lower() for w in words if w.isalpha() and len(w) >= 2] if normalize else words
            if unfiltered:
                minimum_word = 2 if 'len(tok) >= 2' in ast.unparse(function) else 1
                tokens = [w.lower() for w in words if len(w) >= minimum_word]
            expected.extend(tokens)
            retained.append({'paragraph_index': index, 'start_line': text.count('\n', 0, start)+1,
                             'tokens': len(tokens), 'stopword_ratio': ratio,
                             'excerpt': paragraph.strip()[:240]})
    pool = observed.get('latin_words', output)
    if isinstance(pool, tuple):
        pool = pool[0]
    if pool != expected:
        raise ValueError(f'Independent selection does not match original loader: {path}')
    if function.name == 'extract_latin_sentences':
        flattened = [word for sentence in output for word in sentence]
        if flattened != expected[:len(flattened)] or len(expected)-len(flattened) > 3:
            raise ValueError('Unexpected chunking behavior')
        chunking = {'chunks': len(output), 'returned_tokens': len(flattened), 'omitted_tail_tokens': len(expected)-len(flattened)}
    else:
        chunking = None
    return dict(row, status='ISOLATED_LOADER_REPLAY_MATCHED', function=function.name,
                function_ast_sha256=digest(ast.dump(function, include_attributes=False).encode()),
                stopwords=sorted(stopwords) if stopwords is not None else [], filter='NONE' if unfiltered else 'PARAGRAPH_ENGLISH_STOPWORDS_LT_0.08', selected_tokens=len(expected), retained_paragraphs=len(retained),
                selected_sequence_sha256=digest(json.dumps(expected, ensure_ascii=False, separators=(',', ':')).encode()),
                chunking=chunking, evidence=retained[:18]+retained[-18:])

def static_cases():
    cases = [
        ('exp_266_onset_lag_enrichment', 'LATIN_CORPUS', 'DECLARED_NO_AST_NAME_LOAD'),
        ('exp_577_q007_adjrate_decomp', 'LATIN_CORPUS', 'DECLARED_NO_AST_NAME_LOAD'),
        ('exp_267_word_length_position', 'LATIN_CORPUS', 'INLINE_READ_NO_LANGUAGE_FILTER'),
        ('exp_288_stolfi_onset_decomp', 'LATIN_PATH', 'INLINE_READ_NO_LANGUAGE_FILTER'),
        ('exp_031_qo_stripping', 'LATIN', 'DECLARED_NO_AST_NAME_LOAD_DIFFERENT_LEGACY_PATH'),
        ('exp_001_word_initial_entropy', None, 'VULGATE_PASSED_TO_GENERIC_TOKENIZER'),
        ('exp_170_naibbe_simulation', 'LATIN_CORPUS', 'VULGATE_PASSED_TO_LINE_LOADER'),
    ]
    result = []
    for experiment, identifier, status in cases:
        path = ROOT/'experiments'/experiment/'script.py'
        source = path.read_text(encoding='utf-8')
        tree = ast.parse(source)
        loads = sorted(n.lineno for n in ast.walk(tree) if isinstance(n, ast.Name)
                       and isinstance(n.ctx, ast.Load) and n.id == identifier)
        if status.startswith('DECLARED_NO_AST_NAME_LOAD') and loads:
            raise ValueError('Previously unused path now has static loads')
        result.append({'script': path.relative_to(ROOT).as_posix(),
                       'script_sha256': digest(path.read_bytes()), 'path_variable': identifier,
                       'ast_name_load_lines': loads, 'manual_source_review': status,
                       'limit': 'Static source review, not execution or transitive/dynamic use analysis.'})
    return result

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--out', type=Path)
    group.add_argument('--check', type=Path)
    args = parser.parse_args()
    corpus = ROOT / SOURCE
    rows = [replay(path, corpus) for path in sorted((ROOT/'experiments').rglob('*.py'))
            if Path(SOURCE).name in path.read_text(encoding='utf-8')]
    groups = {}
    for row in rows:
        if 'evidence' not in row:
            continue
        key = row['selected_sequence_sha256']
        group = groups.setdefault(key, {'representative_script': row['script'], 'evidence': row['evidence'], 'stopwords': row['stopwords'], 'scripts': []})
        group['scripts'].append(row['script'])
        del row['evidence'], row['stopwords']
    result = {'static_remaining_cases': static_cases(), 'selection_groups': groups, 'source_commit': '1e49032d698713dd29672fd6fbbf2107cac80cd8',
              'corpus': SOURCE, 'corpus_sha256': digest(corpus.read_bytes()),
              'seed_for_diagnostic_chunking': 20261022, 'scripts': rows,
              'limits': ['No experiment module body, simulation or historical result was executed.',
                         'Replay proves loader behavior on frozen input, not that a historical run used it.',
                         'Stopword filtering is not language adjudication. Evidence excerpts require human review.',
                         'Four scripts without a selected loader remain unresolved; transitive imports are outside scope.']}
    if args.check:
        if result != json.loads(args.check.read_text(encoding='utf-8')):
            raise SystemExit('Historical loader replay differs from archived diagnostic')
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'scripts':len(rows), 'matched':sum(r['status']=='ISOLATED_LOADER_REPLAY_MATCHED' for r in rows),
                      'distinct_selected_sequences':len({r['selected_sequence_sha256'] for r in rows if 'selected_sequence_sha256' in r})}))

if __name__ == '__main__':
    main()
