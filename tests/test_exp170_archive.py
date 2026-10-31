#!/usr/bin/env python3
import importlib.util
import json
import math
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('audit', ROOT/'scripts/audit_exp170_archive.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class ArchiveAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (ROOT/audit.EXP/'script.py').read_text()
        cls.ns, _ = audit.historical_namespace("raise RuntimeError('module executed')\n"+cls.source)
        cls.result = audit.audit()

    def test_extraction_has_no_cipher_or_module_side_effects(self):
        self.assertNotIn('encrypt_naibbe', self.ns)
        self.assertNotIn('os', self.ns)
        self.assertNotIn('load_plaintext', self.ns)

    def test_all_metrics_against_hand_counted_corpus(self):
        lines = [['y', 'qokam', 'ch', 'dam'], ['qok', 'okam', 'ok', 'dy'],
                 ['cth', 'daiin', 'cth', 'kam'], ['sh', 'ch', 'chol', 'dam']]
        expected = dict(edy_rate=0, l_onset_rate=0, am_ll_enrichment=2.4,
            daiin_cth_enrichment=8, k_para_start_enrichment=0, y_lf_enrichment=4,
            cth_lf_enrichment=2, qok_ch_enrichment=8/3, qok_self_succ=0,
            ok_self_succ=4, d_self_succ=0, ch_self_succ=16/9, qo_self_succ=0,
            sh_self_succ=0, edy_ol_ratio=0, d_ll_enrichment=3,
            sh_lf_enrichment=4, qok_lf_enrichment=2)
        actual = self.ns['compute_metrics'](lines, {0, 2})
        self.assertEqual(set(actual), set(expected))
        for key, value in expected.items():
            with self.subTest(metric=key):
                self.assertAlmostEqual(actual[key], value)

    def test_classifier_and_line_boundaries(self):
        f = self.ns['get_onset']
        self.assertEqual([f(x) for x in ['qok', 'qot', 'qo', 'cth', 'che', 'chi', 'ch']],
                         ['qok', 'qot', 'qo', 'cth', 'ch_e', 'ch_e', 'ch'])
        # No transition is permitted across lines; ch_e is not ch self-succession.
        metric = self.ns['compute_metrics']([['qok'], ['ch', 'che']])
        self.assertEqual(metric['qok_ch_enrichment'], 0)
        self.assertEqual(metric['ch_self_succ'], 0)
        self.assertIsNone(metric['k_para_start_enrichment'])
        self.assertEqual(self.ns['compute_metrics']([]), {})

    def test_legacy_percentiles_and_population_sd(self):
        values = list(range(100))
        s = self.ns['summarize_distribution'](values+[None])
        self.assertEqual(s['n'], 100)
        self.assertEqual((s['p5'], s['p95']), (5, 95))
        self.assertAlmostEqual(s['mean'], 49.5)
        self.assertAlmostEqual(s['std'], math.sqrt(833.25))
        self.assertAlmostEqual(audit.quantile(values, .05), 4.95)
        self.assertAlmostEqual(audit.quantile(values, .975), 96.525)
        self.assertEqual(audit.summarize([])['n'], 0)
        self.assertEqual(self.ns['inside_interval'](5, s), 'INSIDE')
        self.assertEqual(self.ns['inside_interval'](95, s), 'INSIDE')
        self.assertEqual(self.ns['inside_interval'](None, s), 'N/A')

    def test_archive_snapshot_and_confirmed_errata(self):
        saved = json.loads((ROOT/'research/maintenance/2026-10-22-exp170-audit/results.json').read_text())
        self.assertEqual(self.result, saved)
        self.assertEqual(self.result['baseline_mismatches'], [])
        self.assertEqual(self.result['baseline_lines'], 2447)
        self.assertEqual(self.result['baseline_paragraph_starts'], 2307)
        self.assertEqual(len(self.result['numeric_mismatches']), 50)
        self.assertEqual(len({(x['metric'], x['condition']) for x in self.result['numeric_mismatches']}), 18)
        self.assertEqual(len(self.result['status_mismatches']), 2)
        self.assertEqual([self.result['recomputed_counts'][c]['INSIDE'] for c in audit.CONDITIONS], [4,4,4,5])
        for key in ['am_ll_enrichment', 'y_lf_enrichment']:
            for cell in self.result['metrics'][key]['conditions'].values():
                self.assertEqual(cell['upper_tail_exceedances'], 0)
                self.assertAlmostEqual(cell['upper_tail_plus_one'], 1/101)
                self.assertEqual(cell['status_central95'], 'ABOVE')
        self.assertGreater(self.result['metrics']['am_ll_enrichment']['conditions']['italian_A']['max'], 1.5)

    def test_corrected_table_is_generated_from_archive(self):
        saved = (ROOT/'research/maintenance/2026-10-22-exp170-audit/TABLE.md').read_text()
        self.assertEqual(audit.render_table(self.result), saved)

    def test_malformed_report_fails_closed(self):
        with self.assertRaises(ValueError):
            audit.report_tables('| Metric | Missing |')

    def test_duplicate_historical_metric_row_fails_closed(self):
        report = (ROOT/audit.EXP/'result.md').read_text()
        row = next(line for line in report.splitlines()
                   if line.startswith('| edy rate (B-dialect marker) |'))
        with self.assertRaisesRegex(ValueError, 'Duplicate historical metric row'):
            audit.report_tables(report + '\n' + row + '\n')

    def test_duplicate_historical_count_row_fails_closed(self):
        report = (ROOT/audit.EXP/'result.md').read_text()
        row = next(line for line in report.splitlines()
                   if line.startswith('| INSIDE (cipher consistent) |'))
        with self.assertRaisesRegex(ValueError, 'Duplicate historical count row'):
            audit.report_tables(report + '\n' + row + '\n')

    def test_truncated_historical_count_row_fails_closed(self):
        report = (ROOT/audit.EXP/'result.md').read_text()
        row = next(line for line in report.splitlines()
                   if line.startswith('| INSIDE (cipher consistent) |'))
        cells = row.strip('|').split('|')
        shortened = '| ' + ' | '.join(cells[:-1]).strip() + ' |'
        with self.assertRaisesRegex(ValueError, 'Malformed historical count row'):
            audit.report_tables(report.replace(row, shortened, 1))

    def test_duplicate_archive_json_keys_fail_at_any_depth(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate EXP-170 archive JSON key'):
            audit.parse_archive('{"italian_A": [], "italian_A": []}')
        with self.assertRaisesRegex(ValueError, 'Duplicate EXP-170 archive JSON key'):
            audit.parse_archive('{"italian_A": [{"edy_rate": 1, "edy_rate": 2}]}')

    def test_archive_metric_boolean_is_not_a_number(self):
        # bool is a subclass of int; an archived true/false must not pass as 1/0.
        for value in (True, False):
            with self.subTest(value=value):
                archive = {c: [{'metric': 1.0} for _ in range(100)]
                           for c in audit.CONDITIONS}
                archive['italian_A'][0]['metric'] = value
                with self.assertRaisesRegex(ValueError, 'Non-finite or non-numeric metric'):
                    audit.validate_archive(archive, {'metric'})

    def test_null_only_allowed_for_paragraph_start_metric(self):
        # A nonempty compute_metrics() result always has numeric edy_rate.
        # A missing paragraph-start rate is the one legitimate nullable field.
        row = {"edy_rate": 0.0, "k_para_start_enrichment": None}
        archive = {c: [dict(row) for _ in range(100)] for c in audit.CONDITIONS}
        audit.validate_archive(archive, set(row))
        for bad_key in ("edy_rate",):
            with self.subTest(metric=bad_key):
                archive["italian_A"][0][bad_key] = None
                with self.assertRaisesRegex(ValueError, "Unexpected null"):
                    audit.validate_archive(archive, set(row))
                archive["italian_A"][0][bad_key] = 0.0

    def test_legacy_summary_mismatch_fails_in_optimized_mode(self):
        original = audit.historical_namespace

        def altered_namespace(source):
            ns, tree = original(source)
            summarize = ns['summarize_distribution']

            def altered_summary(values):
                summary = summarize(values)
                if summary['mean'] is not None:
                    summary['mean'] += 0.5
                return summary

            ns['summarize_distribution'] = altered_summary
            return ns, tree

        with patch.object(audit, 'historical_namespace', side_effect=altered_namespace):
            with self.assertRaisesRegex(ValueError, 'EXP-170 legacy summary mismatch'):
                audit.audit()

    def test_legacy_status_mismatch_fails_in_optimized_mode(self):
        original = audit.historical_namespace

        def altered_namespace(source):
            ns, tree = original(source)
            ns['inside_interval'] = lambda *_: 'N/A'
            return ns, tree

        with patch.object(audit, 'historical_namespace', side_effect=altered_namespace):
            with self.assertRaisesRegex(ValueError, 'EXP-170 legacy status mismatch'):
                audit.audit()

    def test_frozen_inputs_match_independent_sha256_lock(self):
        # The lock is not reconstructed from a mutable audit snapshot.
        audit.verify_frozen_inputs(ROOT)
        saved = json.loads((ROOT/'research/maintenance/2026-10-22-exp170-audit/results.json').read_text())
        self.assertEqual(audit.FROZEN_INPUT_SHA256, saved['sha256'])

    def test_frozen_input_tampering_fails_before_historical_ast_execution(self):
        # Copy, never modify, the real historical inputs. Exercise each file.
        with tempfile.TemporaryDirectory() as temp:
            copy_root = Path(temp)
            for relative in audit.FROZEN_INPUT_SHA256:
                dest = copy_root / relative
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / relative, dest)
            audit.verify_frozen_inputs(copy_root)
            for relative in audit.FROZEN_INPUT_SHA256:
                with self.subTest(path=relative):
                    dest = copy_root / relative
                    original = dest.read_bytes()
                    try:
                        dest.write_bytes(original + b'\\n# unexpected mutation')
                        with patch.object(audit, 'historical_namespace',
                                          side_effect=AssertionError('historical AST executed')):
                            with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
                                audit.audit(root=copy_root)
                    finally:
                        dest.write_bytes(original)
            audit.verify_frozen_inputs(copy_root)

    def test_frozen_input_symlink_is_rejected_before_execution(self):
        with tempfile.TemporaryDirectory() as temp:
            copy_root = Path(temp)
            relative = next(iter(audit.FROZEN_INPUT_SHA256))
            dest = copy_root / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            try:
                dest.symlink_to(ROOT / relative)
            except (OSError, NotImplementedError):
                self.skipTest('Symlinks unavailable')
            with patch.object(audit, 'historical_namespace',
                              side_effect=AssertionError('historical AST executed')):
                with self.assertRaisesRegex(ValueError, 'symlinked'):
                    audit.audit(root=copy_root)

    def test_original_archive_passes_strict_json_parser(self):
        raw = (ROOT/audit.EXP/'data/simulation_results.json').read_text()
        self.assertEqual(audit.parse_archive(raw), json.loads(raw))

if __name__ == '__main__':
    unittest.main()
