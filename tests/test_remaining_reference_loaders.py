#!/usr/bin/env python3
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('remaining', ROOT/'scripts/audit_remaining_reference_loaders.py')
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

class RemainingReaderTests(unittest.TestCase):
    def fixture(self, experiment, text):
        source=(ROOT/'experiments'/experiment/'script.py').read_text()
        # A module-level exception proves that importing the experiment is forbidden.
        with tempfile.TemporaryDirectory() as directory:
            directory=Path(directory)
            path=directory/'script.py'
            corpus=directory/'fixture.txt'
            path.write_text("raise RuntimeError('whole module executed')\n"+source)
            corpus.write_text(text)
            original=audit.ROOT
            try:
                audit.ROOT=directory
                return audit.replay(experiment,path,corpus)
            finally:
                audit.ROOT=original

    def test_inline_minimum_two_preserves_case_and_english(self):
        r=self.fixture('exp_267_word_length_position','I am Latin. The book. Arma virumque.')
        self.assertEqual(r['selected_units'],6)
        self.assertEqual(r['first_units'],['am','Latin','The','book','Arma'])

    def test_inline_onset_loop_matches_and_keeps_english(self):
        r=self.fixture('exp_288_stolfi_onset_decomp','I am arma. The book. rhythm.')
        self.assertEqual(r['selected_units'],4)
        self.assertEqual(r['first_units'][0],{'onset':'rm','wlen':4,'blen':1,'mlen':0})
        self.assertEqual(r['last_units'][-1]['blen'],0)

    def test_line_filter_counts_unicode_letters_and_retains_headers(self):
        r=self.fixture('exp_170_naibbe_simulation','12\nab\nABC\nééé\nThe book\n')
        self.assertEqual(r['first_units'],['ABC','ééé','The book'])

    def test_gutenberg_coordinate_bug_exposed(self):
        r=self.fixture('exp_001_word_initial_entropy','header\n*** START OF title ***\narma cano\n*** END OF title ***\nenglish footer retained')
        c=r['gutenberg_coordinate_check']
        self.assertGreater(c['token_delta'],0)
        self.assertGreater(c['historical_selected_characters'],c['coordinate_corrected_characters'])

    def test_no_markers_plain_ascii(self):
        r=self.fixture('exp_001_word_initial_entropy','Arma virumque cano')
        self.assertEqual(r['first_units'],['arma','virumque','cano'])
        self.assertEqual(r['gutenberg_coordinate_check']['token_delta'],0)

    def test_missing_reader_fails(self):
        with self.assertRaises(ValueError):
            audit.select(ast.parse('x=1'), 'exp_267_word_length_position')


class RemainingReaderProvenanceTests(unittest.TestCase):
    """Adversarial metadata inputs; no historical script or corpus is rewritten."""

    def setUp(self):
        from scripts.audit_corpus_identity_overlay import (EXPECTED_ISSUES, EXPECTED_WORKS,
                                                          EXPECTED_EVIDENCE, EXPECTED_SOURCE_COMMIT)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.manifest = {'files': []}
        self.overlay = {
            'source_commit': EXPECTED_SOURCE_COMMIT,
            'historical_results': 'PENDING_SCOPE_AUDIT_NOT_AUTOMATICALLY_RETRACTED',
            'excluded_from_new_language_baselines': [],
        }
        for name, issue in EXPECTED_ISSUES.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            recorded = EXPECTED_EVIDENCE[name]
            evidence_lines = list(dict.fromkeys(recorded['header_title'] +
                                                recorded['header_language'] +
                                                recorded['evidence']))
            raw = (b'' if issue == 'BLOCKED_EMPTY' else
                   ('\n'.join(evidence_lines) + '\n').encode('utf-8'))
            path.write_bytes(raw)
            digest = hashlib.sha256(raw).hexdigest()
            self.manifest['files'].append({
                'path': name, 'bytes': len(raw), 'sha256': digest,
                'status': ('BLOCKED_EMPTY_DO_NOT_USE' if issue == 'BLOCKED_EMPTY'
                           else 'FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED'),
            })
            self.overlay['excluded_from_new_language_baselines'].append({
                'path': name, 'bytes': len(raw), 'sha256': digest,
                'issue': issue, 'adjudicated_work': EXPECTED_WORKS[name],
                'adjudicated_language': ('none' if issue == 'BLOCKED_EMPTY' else
                    'Latin and English' if issue == 'BILINGUAL_REQUIRES_FILTER_AUDIT'
                    else 'English'),
                'header_title': list(recorded['header_title']),
                'header_language': list(recorded['header_language']),
                'evidence': list(recorded['evidence']),
            })

    def load(self):
        for name, obj in (
            ('research/CORPUS_INPUT_MANIFEST.json', self.manifest),
            ('research/CORPUS_IDENTITY_REVIEW.json', self.overlay),
        ):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(obj), encoding='utf-8')
        return audit.load_verified_reference_metadata(self.root)

    def test_valid_metadata_preserves_six_recorded_exclusions(self):
        from scripts.audit_corpus_identity_overlay import EXPECTED_ISSUES
        self.assertEqual(set(self.load()), set(EXPECTED_ISSUES))

    def test_duplicate_overlay_path_fails_before_reader_execution(self):
        rows = self.overlay['excluded_from_new_language_baselines']
        rows.append(dict(rows[0], adjudicated_language='Latin'))
        with self.assertRaisesRegex(ValueError, 'Duplicate overlay path'):
            self.load()

    def test_plausible_identity_change_cannot_silently_relabel_control(self):
        row = next(r for r in self.overlay['excluded_from_new_language_baselines']
                   if r['path'] == 'data/reference_corpora/latin/vulgate.txt')
        row['issue'] = 'WRONG_WORK_SAME_LANGUAGE'
        with self.assertRaisesRegex(ValueError, 'Historical exclusion issue changed'):
            self.load()

    def test_manifest_digest_drift_fails_before_reader_execution(self):
        row = next(r for r in self.manifest['files']
                   if r['path'] == 'data/reference_corpora/latin/vulgate.txt')
        row['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Overlay hash/size disagrees'):
            self.load()

    def test_duplicate_json_members_rejected_at_any_depth(self):
        self.load()
        path = self.root / 'research/CORPUS_IDENTITY_REVIEW.json'
        path.write_text('{"historical_results":"bad",'
                        '"historical_results":"PENDING_SCOPE_AUDIT_NOT_AUTOMATICALLY_RETRACTED",'
                        '"excluded_from_new_language_baselines":[]}', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Duplicate JSON key'):
            audit.load_verified_reference_metadata(self.root)


if __name__=='__main__': unittest.main()
