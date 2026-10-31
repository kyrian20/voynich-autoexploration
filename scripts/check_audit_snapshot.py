#!/usr/bin/env python3
"""Compare deterministic audit JSON with exact counts and tolerant finite floats."""
import json
import math
import sys


def reject_duplicate_keys(pairs):
    """Do not allow a snapshot member to be silently overwritten by json.load."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate audit snapshot JSON key: {key}')
        result[key] = value
    return result


def reject_nonstandard_constant(value):
    """NaN and Infinity are not valid JSON, even before float comparison."""
    raise ValueError(f'Non-standard audit snapshot JSON constant: {value}')


def load_snapshot(path):
    with open(path, encoding='utf-8') as file:
        return json.load(file, object_pairs_hook=reject_duplicate_keys,
                         parse_constant=reject_nonstandard_constant)


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
    expected = load_snapshot(sys.argv[1])
    actual = load_snapshot(sys.argv[2])
    compare(expected, actual)
    print('Audit snapshot reproduced: exact structure/counts, finite floats within 1e-12.')


if __name__ == '__main__':
    main()
