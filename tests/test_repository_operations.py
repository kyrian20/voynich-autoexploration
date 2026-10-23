#!/usr/bin/env python3
"""Exercise publication guard against additional writers and force-pushes."""
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_repository_operations import audit_workflows, reconcile_records


def must_reject(directory):
    try:
        audit_workflows(directory)
    except ValueError:
        return
    raise AssertionError('Unsafe publication configuration accepted')


def main():
    audit_workflows(ROOT / '.github/workflows')
    with tempfile.TemporaryDirectory() as temporary:
        directory = Path(temporary) / 'workflows'
        shutil.copytree(ROOT / '.github/workflows', directory)
        reader = directory / 'voynich-exp604.yml'
        original = reader.read_text()
        reader.write_text(original.replace('contents: read', 'contents: write'))
        must_reject(directory)
        reader.write_text(original)
        reader.write_text(original.replace('          persist-credentials: false', '          persist-credentials: false\n        with:\n          persist-credentials: true'))
        must_reject(directory)
        reader.write_text(original)
        # Previously accepted: a nominal reader with another write permission.
        reader.write_text(original.replace('permissions:\n  contents: read',
                                           'permissions:\n  contents: read\n  actions: write', 1))
        must_reject(directory)
        reader.write_text(original)
        # Previously accepted: a job-level writer for a scope other than contents.
        reader.write_text(original.replace('  exp604:\n',
                                           '  exp604:\n    permissions:\n      pull-requests: write\n', 1))
        must_reject(directory)
        reader.write_text(original)
        publisher = directory / 'voynich-agent.yml'
        publisher_original = publisher.read_text()
        publisher.write_text(publisher_original.replace('permissions:\n  contents: write',
                                                        'permissions:\n  contents: write\n  issues: write', 1))
        must_reject(directory)
        publisher.write_text(publisher_original.replace('git push origin', 'git push --force origin'))
        must_reject(directory)
    records = reconcile_records()
    assert records['nonempty_raw_records'] - records['nonempty_token_records'] == len(records['excluded_after_token_filter'])
    print('Publication guards and exact record-ID reconciliation passed.')


if __name__ == '__main__':
    main()
