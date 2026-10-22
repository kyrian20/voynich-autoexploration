#!/usr/bin/env python3
"""Fail closed on repository automation regressions; never rewrite research data.

Requires PyYAML 6.0.3. Run from any directory. This checks operational contracts,
not scientific validity or full IVTFF conformance.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate YAML keys, which GitHub rejects but safe_load ignores."""


def unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f'Duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}')
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def audit_workflows(directory: Path) -> dict:
    errors, writers, readers = [], [], []
    paths = sorted([*directory.glob('*.yml'), *directory.glob('*.yaml')])
    if not paths:
        raise ValueError('No workflows found')
    for path in paths:
        text = path.read_text(encoding='utf-8')
        data = yaml.load(text, Loader=UniqueKeyLoader)
        if not isinstance(data, dict) or not data.get('jobs'):
            errors.append(f'{path.name}: missing jobs')
            continue
        permissions = data.get('permissions', {})
        writer = isinstance(permissions, dict) and permissions.get('contents') == 'write'
        (writers if writer else readers).append(path.name)
        if not isinstance(permissions, dict) or permissions.get('contents') not in {'read', 'write'}:
            errors.append(f'{path.name}: contents permission must be explicit')
        for job in data['jobs'].values():
            if job.get('permissions', {}).get('contents') == 'write' and not writer:
                errors.append(f'{path.name}: hidden job-level writer')
            for step in job.get('steps', []):
                run = step.get('run', '')
                if not writer and re.search(r'\bgit\s+(?:push|commit)\b', run):
                    errors.append(f'{path.name}: reader contains publication command')
                if re.search(r'\bgit\s+push[^\n]*(?:--force|\s-f\b)', run):
                    errors.append(f'{path.name}: force-push forbidden')
        if path.name not in {'voynich-check.yml'}:
            if 'actions/upload-artifact@' not in text:
                errors.append(f'{path.name}: missing result artifact')
        if writer:
            concurrency = data.get('concurrency', {})
            if not concurrency.get('group') or concurrency.get('cancel-in-progress') is not False:
                errors.append(f'{path.name}: publisher concurrency must preserve active run')
            if 'fetch-depth: 0' not in text or 'git rebase --abort' not in text:
                errors.append(f'{path.name}: publisher lacks full history/conflict abort')
            # PyYAML uses YAML 1.1, where the key "on" is parsed as True.
            triggers = data.get('on', data.get(True, {}))
            if triggers.get('push', {}).get('branches') != ['master']:
                errors.append(f'{path.name}: publisher push must be limited to master')
            if "github.ref == 'refs/heads/master'" not in text:
                errors.append(f'{path.name}: dispatch must also be limited to master')
    if writers != ['voynich-agent.yml']:
        errors.append(f'Expected one publisher, found {writers}')
    if errors:
        raise ValueError('\n'.join(errors))
    return {'workflow_count': len(paths), 'publishers': writers, 'artifact_or_check_readers': readers}


def reconcile_records() -> dict:
    # These imports expose existing production and audit views; no new tokenizer.
    from scripts.exp590_daiin_position import TEXT_LINE, load_lines
    from scripts.audit_ivtff_ligature_views import TEXT_LINE as BROAD_LINE, tokenize_views

    path = ROOT / 'data/transcriptions/eva_zl3b.txt'
    raw, parsed = load_lines(path)
    rows, excluded = [], []
    for source_line, row in enumerate(raw.decode('utf-8-sig').splitlines(), 1):
        broad = BROAD_LINE.match(row)
        if not broad or not broad.group(3).strip():
            continue
        match = TEXT_LINE.match(row)
        if not match:
            raise ValueError(f'Broad record missed by production pattern: source line {source_line}')
        folio, number, body = match.groups()
        key = (folio, int(number))
        rows.append(key)
        if not tokenize_views(body)['historical']:
            excluded.append({'id': f'{folio}.{number}', 'source_line': source_line, 'raw_body': body})
    parsed_ids = [(x['folio'], x['line']) for x in parsed]
    if len(rows) != len(set(rows)) or len(parsed_ids) != len(set(parsed_ids)):
        raise ValueError('Duplicate record IDs; refusing set-only reconciliation')
    excluded_ids = {x['id'] for x in excluded}
    expected = {k for k in rows if f'{k[0]}.{k[1]}' not in excluded_ids}
    if expected != set(parsed_ids):
        raise ValueError('Production IDs disagree with broad coverage after identical token filter')
    return {
        'source': str(path.relative_to(ROOT)), 'source_sha256': hashlib.sha256(raw).hexdigest(),
        'nonempty_raw_records': len(rows), 'nonempty_token_records': len(parsed_ids),
        'excluded_after_token_filter': excluded,
        'interpretation': 'Exact ID-set reconciliation under the historical exclusion of tags, braces and square annotations; no scientific claim.',
    }


def audit_experiment_paths() -> dict:
    registry = json.loads((ROOT / 'research/EXPERIMENT_PATH_REGISTRY.json').read_text())
    expected = []
    for path in sorted((ROOT / 'experiments').iterdir()):
        match = re.fullmatch(r'exp_(\d+)_(.+)', path.name)
        if path.is_dir() and match:
            relative = path.relative_to(ROOT).as_posix()
            expected.append({'canonical_id': 'GH:' + relative,
                             'legacy_numeric_id': int(match[1]), 'path': relative})
    if registry['entries'] != expected:
        raise ValueError('Experiment path registry differs from actual directories; reconcile explicitly')
    if len({x['canonical_id'] for x in expected}) != len(expected):
        raise ValueError('Canonical experiment IDs are not unique')
    collisions = {}
    for entry in expected:
        collisions.setdefault(str(entry['legacy_numeric_id']), []).append(entry['canonical_id'])
    collisions = {key: values for key, values in collisions.items() if len(values) > 1}
    if registry['numeric_collisions'] != collisions:
        raise ValueError('Legacy numeric alias collisions are not fully registered')
    return {'unique_path_ids': len(expected), 'legacy_numeric_collision_groups': len(collisions),
            'scientific_validation': False}


def main() -> None:
    print(json.dumps({'audit': 'repository_operations', 'workflows': audit_workflows(ROOT / '.github/workflows'),
                      'experiment_paths': audit_experiment_paths(),
                      'record_reconciliation': reconcile_records()}, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    import sys
    sys.path.insert(0, str(ROOT))
    main()
