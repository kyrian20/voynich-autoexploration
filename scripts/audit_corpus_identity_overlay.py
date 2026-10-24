#!/usr/bin/env python3
"""Fail closed when the historical corpus-identity exclusion overlay drifts.

This is a provenance guard, not a language classifier or reproduction of
historical experiments. Frozen corpus bytes and existing decisions stay intact.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.check_corpus_integrity import linked_path, unique_keys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path('research/CORPUS_INPUT_MANIFEST.json')
OVERLAY = Path('research/CORPUS_IDENTITY_REVIEW.json')
EXCLUDED = 'PENDING_SCOPE_AUDIT_NOT_AUTOMATICALLY_RETRACTED'
EXPECTED_ISSUES = {
    'data/reference_corpora/arabic/quran_arabic.txt': 'WRONG_LANGUAGE_AND_WORK',
    'data/reference_corpora/english/kjv_bible.txt': 'WRONG_WORK_SAME_LANGUAGE',
    'data/reference_corpora/latin/caesar_gallic_wars.txt': 'WRONG_LANGUAGE_FOR_LATIN',
    'data/reference_corpora/latin/cicero_caesar_latin.txt': 'BLOCKED_EMPTY',
    'data/reference_corpora/latin/cicero_de_officiis_latin.txt': 'BILINGUAL_REQUIRES_FILTER_AUDIT',
    'data/reference_corpora/latin/vulgate.txt': 'WRONG_LANGUAGE_FOR_LATIN',
}
# Recorded work identities are historical adjudications, not inferred by this audit.
# Keep them explicit so a plausible but incorrect nonempty work label cannot drift.
EXPECTED_WORKS = {
    'data/reference_corpora/arabic/quran_arabic.txt': 'Drum-Taps #8801',
    'data/reference_corpora/english/kjv_bible.txt': 'The Book of Mormon #17',
    'data/reference_corpora/latin/caesar_gallic_wars.txt': 'De Bello Gallico and Other Commentaries, English translation',
    'data/reference_corpora/latin/cicero_caesar_latin.txt': 'empty',
    'data/reference_corpora/latin/cicero_de_officiis_latin.txt': 'De Officiis #47001',
    'data/reference_corpora/latin/vulgate.txt': 'The Bible, Douay-Rheims, Complete',
}
ISSUES = set(EXPECTED_ISSUES.values())


def audit(root, manifest, overlay):
    """Return precise errors; do not change either file or infer a language."""
    errors = []
    if not isinstance(manifest, dict) or not isinstance(manifest.get('files'), list):
        return ['Invalid corpus manifest schema']
    if not isinstance(overlay, dict) or not isinstance(overlay.get('excluded_from_new_language_baselines'), list):
        return ['Invalid corpus identity overlay schema']
    if overlay.get('historical_results') != EXCLUDED:
        errors.append('Historical-result scope changed without adjudication')
    rows = overlay['excluded_from_new_language_baselines']
    if not rows:
        errors.append('Corpus exclusion overlay unexpectedly empty')
    frozen = {}
    for row in manifest['files']:
        if not isinstance(row, dict) or not isinstance(row.get('path'), str):
            return ['Invalid corpus manifest entry']
        if row['path'] in frozen:
            errors.append(f'Duplicate corpus manifest path: {row["path"]}')
        frozen[row['path']] = row
    seen = set()
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f'Overlay row {i} is not an object')
            continue
        name = row.get('path')
        if not isinstance(name, str) or not re.fullmatch(r'data/reference_corpora/[^\\]+\.txt', name) or '..' in Path(name).parts:
            errors.append(f'Invalid overlay path: {name}')
            continue
        if name in seen:
            errors.append(f'Duplicate overlay path: {name}')
            continue
        seen.add(name)
        if name not in frozen:
            errors.append(f'Overlay corpus missing from frozen manifest: {name}')
            continue
        entry = frozen[name]
        if row.get('sha256') != entry.get('sha256') or type(row.get('bytes')) is not int or row['bytes'] != entry.get('bytes'):
            errors.append(f'Overlay hash/size disagrees with frozen manifest: {name}')
            continue
        if row.get('issue') not in ISSUES:
            errors.append(f'Unknown corpus identity issue: {name}')
        if name in EXPECTED_ISSUES and row.get('issue') != EXPECTED_ISSUES[name]:
            errors.append(f'Historical exclusion issue changed: {name}')
        if not isinstance(row.get('adjudicated_language'), str) or not row['adjudicated_language'].strip():
            errors.append(f'Missing adjudicated language: {name}')
        if not isinstance(row.get('adjudicated_work'), str) or not row['adjudicated_work'].strip():
            errors.append(f'Missing adjudicated work: {name}')
        elif name in EXPECTED_WORKS and row['adjudicated_work'] != EXPECTED_WORKS[name]:
            errors.append(f'Historical adjudicated work changed: {name}')
        if linked_path(root, name):
            errors.append(f'Symlink forbidden in corpus identity audit: {name}')
            continue
        path = root / name
        if not path.is_file():
            errors.append(f'Overlay corpus missing: {name}')
            continue
        raw = path.read_bytes()
        if len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
            errors.append(f'Overlay corpus bytes changed: {name}')
            continue
        if row['issue'] == 'BLOCKED_EMPTY':
            if raw or entry.get('status') != 'BLOCKED_EMPTY_DO_NOT_USE':
                errors.append(f'Empty corpus quarantine inconsistent: {name}')
            if any(row.get(key) for key in ('header_title', 'header_language', 'evidence')):
                errors.append(f'Empty corpus has fabricated textual evidence: {name}')
            if row.get('adjudicated_language') != 'none':
                errors.append(f'Empty corpus adjudication changed: {name}')
            continue
        if not raw:
            errors.append(f'Nonempty identity evidence has empty corpus: {name}')
            continue
        text = raw.decode('utf-8-sig', errors='replace')
        header = {line.strip() for line in text.splitlines()[:120]}
        for key in ('header_title', 'header_language', 'evidence'):
            claims = row.get(key)
            if not isinstance(claims, list) or (key == 'evidence' and not claims):
                errors.append(f'Invalid {key} evidence list: {name}')
                continue
            for claim in claims:
                if not isinstance(claim, str) or not claim.strip():
                    errors.append(f'Empty/nontext {key} evidence: {name}')
                elif key.startswith('header_') and claim not in header:
                    errors.append(f'Header claim absent from first 120 lines ({key}): {name}')
                elif key == 'evidence' and claim not in text:
                    errors.append(f'Textual evidence not found ({claim[:45]}): {name}')
        if row['issue'] in ('WRONG_LANGUAGE_AND_WORK', 'WRONG_LANGUAGE_FOR_LATIN', 'WRONG_WORK_SAME_LANGUAGE'):
            if 'Language: English' not in row.get('header_language', []):
                errors.append(f'English header evidence required for this issue: {name}')
            if row.get('adjudicated_language') != 'English':
                errors.append(f'Adjudicated English language changed: {name}')
        if row['issue'] == 'BILINGUAL_REQUIRES_FILTER_AUDIT' and row.get('adjudicated_language') != 'Latin and English':
            errors.append(f'Bilingual adjudication changed: {name}')
    for missing in sorted(set(EXPECTED_ISSUES) - seen):
        errors.append(f'Historical exclusion silently removed: {missing}')
    return errors


def main():
    manifest = json.loads((ROOT / MANIFEST).read_text(encoding='utf-8'), object_pairs_hook=unique_keys)
    overlay = json.loads((ROOT / OVERLAY).read_text(encoding='utf-8'), object_pairs_hook=unique_keys)
    errors = audit(ROOT, manifest, overlay)
    print(json.dumps({'overlay_rows': len(overlay['excluded_from_new_language_baselines']),
                      'errors': errors,
                      'scope': 'Identity overlay vs frozen bytes and recorded textual evidence only; not historical reproduction or independent language identification.'},
                     ensure_ascii=False, indent=2))
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
