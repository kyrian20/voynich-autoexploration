#!/usr/bin/env python3
"""Compare deterministic audit JSON with exact counts and tolerant finite floats."""
import json
import math
import sys


def compare(expected, actual, path='$'):
    if type(expected) is not type(actual):
        raise ValueError(f'{path}: types differ')
    if isinstance(expected, dict):
        if expected.keys() != actual.keys():
            raise ValueError(f'{path}: keys differ')
        for key in expected:
            compare(expected[key], actual[key], f'{path}.{key}')
    elif isinstance(expected, list):
        if len(expected) != len(actual):
            raise ValueError(f'{path}: lengths differ')
        for index, (a, b) in enumerate(zip(expected, actual)):
            compare(a, b, f'{path}[{index}]')
    elif isinstance(expected, float):
        if not math.isfinite(expected) or not math.isfinite(actual) or not math.isclose(expected, actual, rel_tol=1e-12, abs_tol=1e-12):
            raise ValueError(f'{path}: floating value differs')
    elif expected != actual:
        raise ValueError(f'{path}: value differs')


def main():
    if len(sys.argv) != 3:
        raise SystemExit('Usage: python scripts/check_audit_snapshot.py EXPECTED.json ACTUAL.json')
    with open(sys.argv[1], encoding='utf-8') as file:
        expected = json.load(file)
    with open(sys.argv[2], encoding='utf-8') as file:
        actual = json.load(file)
    compare(expected, actual)
    print('Audit snapshot reproduced: exact structure/counts, finite floats within 1e-12.')


if __name__ == '__main__':
    main()
