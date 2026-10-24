"""Synthetic fail-closed regression tests for corpus identity exclusions."""
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.audit_corpus_identity_overlay import audit, EXPECTED_ISSUES, EXPECTED_WORKS


class IdentityOverlayTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.name = 'data/reference_corpora/latin/vulgate.txt'
        self.manifest = {'files': []}
        self.overlay = {'historical_results': 'PENDING_SCOPE_AUDIT_NOT_AUTOMATICALLY_RETRACTED',
                        'excluded_from_new_language_baselines': []}
        for name, issue in EXPECTED_ISSUES.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            raw = (b'' if issue == 'BLOCKED_EMPTY' else
                   b'Title: English translation\nLanguage: English\nEvidence of translation\n')
            path.write_bytes(raw)
            row = {
                'path': name, 'sha256': hashlib.sha256(raw).hexdigest(),
                'bytes': len(raw), 'header_title': [] if issue in ('BLOCKED_EMPTY', 'BILINGUAL_REQUIRES_FILTER_AUDIT') else ['Title: English translation'],
                'header_language': [] if issue in ('BLOCKED_EMPTY', 'BILINGUAL_REQUIRES_FILTER_AUDIT') else ['Language: English'],
                'issue': issue,
                'adjudicated_language': ('none' if issue == 'BLOCKED_EMPTY' else
                                        'Latin and English' if issue == 'BILINGUAL_REQUIRES_FILTER_AUDIT' else 'English'),
                'adjudicated_work': EXPECTED_WORKS[name],
                'evidence': [] if issue == 'BLOCKED_EMPTY' else ['Evidence of translation'],
            }
            self.overlay['excluded_from_new_language_baselines'].append(row)
            self.manifest['files'].append(dict(path=name, bytes=len(raw),
                 sha256=row['sha256'], status=('BLOCKED_EMPTY_DO_NOT_USE' if issue == 'BLOCKED_EMPTY'
                                              else 'FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED')))
        self.row = next(x for x in self.overlay['excluded_from_new_language_baselines'] if x['path'] == self.name)

    def check(self):
        return audit(self.root, self.manifest, self.overlay)

    def test_valid_overlay(self):
        self.assertEqual(self.check(), [])

    def test_hash_or_size_mismatch(self):
        self.row['sha256'] = '0' * 64
        self.assertTrue(any('hash/size' in x for x in self.check()))

    def test_duplicate_overlay_row(self):
        self.overlay['excluded_from_new_language_baselines'].append(dict(self.row))
        self.assertTrue(any('Duplicate overlay' in x for x in self.check()))

    def test_fabricated_header_and_evidence(self):
        self.row['header_language'] = ['Language: Latin']
        self.row['evidence'] = ['Invented textual claim']
        errors = self.check()
        self.assertTrue(any('Header claim absent' in x for x in errors))
        self.assertTrue(any('Textual evidence not found' in x for x in errors))

    def test_drift_in_historical_scope(self):
        self.overlay['historical_results'] = 'VALIDATED'
        self.assertTrue(any('Historical-result scope' in x for x in self.check()))

    def test_unlisted_corpus_or_path_escape(self):
        self.row['path'] = 'data/reference_corpora/latin/../vulgate.txt'
        self.assertTrue(any('Invalid overlay path' in x for x in self.check()))
        self.row['path'] = 'data/reference_corpora/latin/unknown.txt'
        self.assertTrue(any('missing from frozen manifest' in x for x in self.check()))

    def test_unreviewed_manifest_backed_exclusion_is_rejected(self):
        # This is a syntactically valid, hash-consistent seventh corpus.
        # Before the guard, the audit returned [] for this fixture.
        name = 'data/reference_corpora/latin/virgil_aeneid_latin.txt'
        raw = b'Title: English translation\\nLanguage: English\\nEvidence of translation\\n'
        # Interpret the literal escapes to make the test data explicit.
        raw = raw.replace(b'\\\\n', b'\\n')
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        digest = hashlib.sha256(raw).hexdigest()
        self.manifest['files'].append({
            'path': name, 'sha256': digest, 'bytes': len(raw),
            'status': 'FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED',
        })
        self.overlay['excluded_from_new_language_baselines'].append({
            'path': name, 'sha256': digest, 'bytes': len(raw),
            'header_title': ['Title: English translation'],
            'header_language': ['Language: English'],
            'issue': 'WRONG_LANGUAGE_FOR_LATIN',
            'adjudicated_language': 'English',
            'adjudicated_work': 'Unreviewed work',
            'evidence': ['Evidence of translation'],
        })
        self.assertTrue(any('Unreviewed corpus exclusion' in error
                            for error in self.check()))

    def test_quarantined_empty_input(self):
        row = next(x for x in self.overlay['excluded_from_new_language_baselines'] if x['issue'] == 'BLOCKED_EMPTY')
        self.assertEqual(self.check(), [])
        row['evidence'] = ['invented']
        self.assertTrue(any('fabricated' in x for x in self.check()))

    def test_untrusted_symlink(self):
        outside = self.root / 'outside.txt'
        outside.write_bytes((self.root / self.name).read_bytes())
        (self.root / self.name).unlink()
        (self.root / self.name).symlink_to(outside)
        self.assertTrue(any('Symlink forbidden' in x for x in self.check()))

    def test_missing_historical_exclusion(self):
        self.overlay['excluded_from_new_language_baselines'].remove(self.row)
        self.assertTrue(any('silently removed' in x for x in self.check()))

    def test_changed_adjudicated_work_rejected_even_if_nonempty(self):
        # The old guard only required a nonempty work label. A fabricated
        # label therefore passed while the original corpus bytes were intact.
        self.row['adjudicated_work'] = 'Invented work'
        self.assertTrue(any('Historical adjudicated work changed' in x
                            for x in self.check()))
        # Even another historically documented work must not silently replace
        # this file's recorded identity.
        self.row['adjudicated_work'] = 'The Book of Mormon #17'
        self.assertTrue(any('Historical adjudicated work changed' in x
                            for x in self.check()))

    def test_changed_identity_classification(self):
        self.row['issue'] = 'WRONG_WORK_SAME_LANGUAGE'
        self.assertTrue(any('Historical exclusion issue changed' in x for x in self.check()))
        self.row['issue'] = 'WRONG_LANGUAGE_FOR_LATIN'
        self.row['adjudicated_language'] = 'Latin'
        self.assertTrue(any('Adjudicated English language changed' in x for x in self.check()))


if __name__ == '__main__':
    unittest.main()
