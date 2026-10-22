#!/usr/bin/env python3
"""Verify the path-only migration without importing or executing old experiments."""
from __future__ import annotations

import ast
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'research/maintenance/2026-10-22-intensive/path-migration.json'
OLD_ROOTS = ('/Users/asash/voynich-cryptanalyst', '~/voynich-cryptanalyst')
BASE = ast.dump(ast.parse('_RepositoryPath(__file__).resolve().parents[2]', mode='eval').body)


class NormalizePaths(ast.NodeTransformer):
    def visit_ImportFrom(self, node):
        if node.module == 'pathlib' and len(node.names) == 1 and node.names[0].asname == '_RepositoryPath':
            return None
        return node

    def visit_Constant(self, node):
        if isinstance(node.value, str):
            for root in OLD_ROOTS:
                if node.value == root or node.value.startswith(root + '/'):
                    return ast.Constant('@REPOSITORY@' + node.value[len(root):])
        return node

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == 'str' and len(node.args) == 1 and not node.keywords:
            value = node.args[0]
            suffix = ''
            if isinstance(value, ast.BinOp) and isinstance(value.op, ast.Div) and isinstance(value.right, ast.Constant) and isinstance(value.right.value, str):
                suffix = '/' + value.right.value
                value = value.left
            if ast.dump(value) == BASE:
                return ast.Constant('@REPOSITORY@' + suffix)
        return self.generic_visit(node)


def algorithm_digest(text: str) -> str:
    tree = NormalizePaths().visit(ast.parse(text))
    return hashlib.sha256(ast.dump(tree, include_attributes=False).encode()).hexdigest()


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    blocked = []
    for entry in manifest['files']:
        path = ROOT / entry['path']
        text = path.read_text()
        if algorithm_digest(text) != entry['algorithm_ast_sha256']:
            raise ValueError(f'Algorithm changed outside the path-only migration: {entry["path"]}')
        for node in ast.walk(ast.parse(text)):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if any(node.value == old or node.value.startswith(old + '/') for old in OLD_ROOTS):
                    raise ValueError(f'Legacy machine path remains: {path}')
            if isinstance(node, ast.Call):
                normalized = NormalizePaths().visit(copy.deepcopy(node))
                if isinstance(normalized, ast.Constant) and isinstance(normalized.value, str) and normalized.value.startswith('@REPOSITORY@'):
                    suffix = normalized.value[len('@REPOSITORY@'):].lstrip('/')
                    resolved = eval(compile(ast.Expression(node), str(path), 'eval'),
                                    {'__builtins__': {'str': str}, '_RepositoryPath': Path, '__file__': str(path)})
                    if resolved != str(ROOT / suffix):
                        raise ValueError(f'Runtime path expression does not resolve to this checkout: {path}')
        for target in entry['targets']:
            if not (ROOT / target['relative_path']).exists():
                blocked.append({'script': entry['path'], 'missing_target': target['relative_path']})
    print(json.dumps({'path_only_files_verified': len(manifest['files']), 'algorithm_ast_checks': 'pass',
                      'missing_inputs': blocked,
                      'scope': 'Static semantic preservation, not execution or scientific validation of every historical experiment.'}, indent=2))


if __name__ == '__main__':
    main()
