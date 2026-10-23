"""Read-only AST and hash audit of EXP-177's reproducibility constraints.

No historical experiment is imported or executed. No corpus is opened.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = (
    'experiments/exp_177_position_sensitive_cipher/script.py',
    'experiments/exp_177_verify/script.py',
    'experiments/exp_177_position_sensitive_cipher/data/cipher_results.json',
    'experiments/exp_177_verify/data/verify_results.json',
)
SOURCE_COMMIT = '75f126df8a358f9d048ec8c1065b8ede82b99c5e'


def _calls(tree, owner=None):
    if owner is not None:
        matches = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == owner]
        if len(matches) != 1:
            raise ValueError(f'Expected exactly one function {owner}')
        tree = matches[0]
    return [n for n in ast.walk(tree) if isinstance(n, ast.Call)]


def _is_call(node, base, method):
    return (isinstance(node.func, ast.Attribute) and node.func.attr == method
            and isinstance(node.func.value, ast.Name) and node.func.value.id == base)


def audit_source(source):
    tree = ast.parse(source)
    seeded_from_hash = False
    for node in _calls(tree):
        if _is_call(node, 'random', 'Random'):
            for arg in node.args:
                if any(isinstance(child, ast.Call) and isinstance(child.func, ast.Name)
                       and child.func.id == 'hash' and len(child.args) == 1
                       and isinstance(child.args[0], ast.Name) and child.args[0].id == 'cal'
                       for child in ast.walk(arg)):
                    seeded_from_hash = True
    core_uses_global_random = any(_is_call(node, 'random', 'choice')
                                  for node in _calls(tree, 'make_word'))
    plaintext_shuffled = any(_is_call(node, 'rng', 'shuffle') and len(node.args) == 1
                             and isinstance(node.args[0], ast.Name) and node.args[0].id == 'all_words'
                             for node in _calls(tree, 'generate_cipher_corpus'))
    global_seed_42 = any(_is_call(node, 'random', 'seed') and len(node.args) == 1
                         and isinstance(node.args[0], ast.Constant) and node.args[0].value == 42
                         for node in _calls(tree))
    return {
        'python_hash_used_in_simulation_seed': seeded_from_hash,
        'word_core_uses_global_random_not_local_rng': core_uses_global_random,
        'plaintext_word_order_shuffled_before_encoding': plaintext_shuffled,
        'global_random_seed_42_present': global_seed_42,
    }


def build_snapshot(root=ROOT):
    data = {}
    for path in INPUTS:
        b = (root / path).read_bytes()
        data[path] = hashlib.sha256(b).hexdigest()
    return {
        'schema_version': 1,
        'source_commit': SOURCE_COMMIT,
        'scope': 'Read-only AST audit; no historical simulation, parser, or corpus executed',
        'input_sha256': data,
        'checks': {
            'EXP-177': audit_source((root / INPUTS[0]).read_text(encoding='utf-8')),
            'EXP-177-verify': audit_source((root / INPUTS[1]).read_text(encoding='utf-8')),
        },
    }


def main():
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--check', type=Path)
    group.add_argument('--out', type=Path)
    args = ap.parse_args()
    actual = build_snapshot()
    if args.check:
        expected = json.loads(args.check.read_text(encoding='utf-8'))
        if actual != expected:
            raise SystemExit('FAIL: archived snapshot differs from current sources or AST checks')
        print('PASS: EXP-177 RNG provenance snapshot and input SHA-256')
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(actual, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'Wrote {args.out}')


if __name__ == '__main__':
    main()
