"""Regression for concurrent changes to historical evidence under output root."""
from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

from scripts.check_publisher_source_drift import (
    assert_no_source_drift, changed_source_paths,
)


class PublisherSourceDriftContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "user.name", "CI test")
        self.git("config", "user.email", "ci@example.invalid")
        self.write("scripts/analyse.py", "print('old source')\n")
        self.write("data/transcriptions/input.txt", "original corpus\n")
        self.write("research/experiments/2026-10-20-exp590-erratum.md", "frozen correction\n")
        self.write("research/experiments/2026-10-20-exp590.json", '{"value": 1}\n')
        self.write("research/experiments/2026-10-29-exp590-corrected-L-metadata.json", '{"value": 1}\n')
        self.commit("baseline")
        self.base = self.git("rev-parse", "HEAD").strip()

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True,
                              capture_output=True, text=True).stdout

    def write(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-qm", message)
        return self.git("rev-parse", "HEAD").strip()


    @staticmethod
    def sample_output(exp):
        # Real, frozen publisher output is a stronger positive control than
        # an invented JSON fixture with an accidentally permissive schema.
        paths = {
            590: "2026-11-02-exp590-corrected-L-metadata.json",
            593: "2026-11-02-exp593-corrected-L-metadata.json",
            622: "exp_622_ch_sh_specificity_interaction/results.json",
            623: "exp_623_it2a_ch_sh_specificity_replication/results.json",
        }
        return json.loads((ROOT / "research/experiments" / paths[exp]).read_text(encoding="utf-8"))

    def test_new_known_dated_output_is_safe(self):
        self.write("research/experiments/2026-10-30-exp590-corrected-L-metadata.json",
                   json.dumps(self.sample_output(590)))
        head = self.commit("another publisher updated an output")
        self.assertEqual(changed_source_paths(self.root, self.base, head), [])
        assert_no_source_drift(self.root, self.base, head)

    def test_new_allowed_symlink_is_not_safe_generated_output(self):
        # Before the fix, status A + an allowlisted pathname was sufficient,
        # even when the committed entry was a symlink rather than a JSON blob.
        target = self.root / "research/experiments/2026-10-30-exp590-corrected-L-metadata.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(self.root / "scripts/analyse.py")
        head = self.commit("add symlink with permitted output name")
        with self.assertRaisesRegex(RuntimeError, "unsafe Git mode/type.*120000"):
            assert_no_source_drift(self.root, self.base, head)

    def test_new_allowed_executable_file_is_not_safe_generated_output(self):
        target = "research/experiments/2026-10-30-exp590-corrected-L-metadata.json"
        self.write(target, '{"value": 2}\\n')
        (self.root / target).chmod(0o755)
        head = self.commit("add executable with permitted output name")
        with self.assertRaisesRegex(RuntimeError, "unsafe Git mode/type.*100755"):
            assert_no_source_drift(self.root, self.base, head)

    def test_script_change_blocks_stale_publication(self):
        self.write("scripts/analyse.py", "print('new source')\n")
        head = self.commit("concurrent script update")
        with self.assertRaisesRegex(RuntimeError, "scripts/analyse.py"):
            assert_no_source_drift(self.root, self.base, head)

    def test_transcription_change_blocks_stale_publication(self):
        self.write("data/transcriptions/input.txt", "changed corpus\n")
        head = self.commit("concurrent corpus update")
        with self.assertRaisesRegex(RuntimeError, "data/transcriptions/input.txt"):
            assert_no_source_drift(self.root, self.base, head)

    def test_rebase_race_after_output_update_is_still_blocked(self):
        self.write("research/experiments/2026-10-30-exp590-corrected-L-metadata.json", '{"value": 2}\n')
        self.commit("output-only concurrent update")
        self.write("scripts/analyse.py", "print('new source')\n")
        head = self.commit("source changed after output update")
        with self.assertRaisesRegex(RuntimeError, "scripts/analyse.py"):
            assert_no_source_drift(self.root, self.base, head)

    def test_unknown_ref_fails_closed(self):
        with self.assertRaisesRegex(RuntimeError, "Cannot verify source drift"):
            assert_no_source_drift(self.root, self.base, "missing-ref")

    def test_empty_baseline_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "required"):
            assert_no_source_drift(self.root, "", "HEAD")

    def test_workflow_checks_after_fetch_before_rebase(self):
        workflow = (Path(__file__).resolve().parents[1] / ".github" / "workflows" /
                    "voynich-agent.yml").read_text(encoding="utf-8")
        fetch = workflow.index("git fetch --no-tags origin master")
        check = workflow.index("python scripts/check_publisher_source_drift.py")
        rebase = workflow.index("git rebase origin/master")
        self.assertLess(fetch, check)
        self.assertLess(check, rebase)
        self.assertIn('--base "$GITHUB_SHA"', workflow)




    def test_new_allowlisted_empty_json_blocks_publication(self):
        self.write("research/experiments/2026-11-02-exp590-corrected-L-metadata.json", "")
        head = self.commit("concurrent empty generated JSON")
        with self.assertRaisesRegex(RuntimeError, "empty or whitespace-only output"):
            assert_no_source_drift(self.root, self.base, head)

    def test_new_allowlisted_invalid_json_blocks_publication(self):
        self.write("research/experiments/2026-11-02-exp593-corrected-L-metadata.json", '{"unfinished":')
        head = self.commit("concurrent malformed generated JSON")
        with self.assertRaisesRegex(RuntimeError, "invalid or ambiguous JSON"):
            assert_no_source_drift(self.root, self.base, head)

    def test_new_allowlisted_nested_duplicate_json_keys_blocks_publication(self):
        self.write("research/experiments/2026-11-02-exp590-corrected-L-metadata.json",
                   '{"metrics": {"n": 1, "n": 2}}')
        head = self.commit("concurrent ambiguous generated JSON")
        with self.assertRaisesRegex(RuntimeError, "duplicate JSON key"):
            assert_no_source_drift(self.root, self.base, head)

    def test_new_allowlisted_nonfinite_json_blocks_publication(self):
        self.write("research/experiments/2026-11-02-exp590-corrected-L-metadata.json",
                   '{"statistic": NaN}')
        head = self.commit("concurrent non-finite generated JSON")
        with self.assertRaisesRegex(RuntimeError, "non-finite JSON constant"):
            assert_no_source_drift(self.root, self.base, head)

    def test_new_allowlisted_overflow_json_blocks_publication(self):
        # Python's json.loads turns a legal 1e999 token into float('inf').
        self.write("research/experiments/2026-11-02-exp590-corrected-L-metadata.json",
                   '{"nested": [{"statistic": 1e999}]}')
        head = self.commit("concurrent overflowed generated JSON")
        with self.assertRaisesRegex(RuntimeError, "non-finite JSON number"):
            assert_no_source_drift(self.root, self.base, head)

    def test_new_allowlisted_array_json_blocks_publication(self):
        self.write("research/experiments/2026-11-02-exp590-corrected-L-metadata.json",
                   '[{"metric": 1}]')
        head = self.commit("concurrent wrong-root generated JSON")
        with self.assertRaisesRegex(RuntimeError, "JSON root must be an object"):
            assert_no_source_drift(self.root, self.base, head)

    def test_new_allowlisted_blank_markdown_blocks_publication(self):
        self.write("research/experiments/2026-11-02-exp590-corrected-L-metadata.md",
                   "  \n  ")
        head = self.commit("concurrent blank generated report")
        with self.assertRaisesRegex(RuntimeError, "empty or whitespace-only output"):
            assert_no_source_drift(self.root, self.base, head)

    def test_new_allowlisted_non_utf8_json_blocks_publication(self):
        target = self.root / "research/experiments/2026-11-02-exp590-corrected-L-metadata.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b'{"invalid": "\\xff"}' + b'\xff')
        head = self.commit("concurrent non-UTF8 generated JSON")
        with self.assertRaisesRegex(RuntimeError, "non-UTF-8 output"):
            assert_no_source_drift(self.root, self.base, head)

    def test_new_allowlisted_valid_markdown_remains_safe(self):
        self.write("research/experiments/2026-11-02-exp590-corrected-L-metadata.md",
                   "# Resultados\n\nDiagnóstico sin afirmación semántica.\n")
        head = self.commit("concurrent valid generated report")
        assert_no_source_drift(self.root, self.base, head)

    def test_new_known_exp622_output_is_safe(self):
        self.write("research/experiments/exp_622_ch_sh_specificity_interaction/results.json",
                   json.dumps(self.sample_output(622)))
        head = self.commit("publisher added new exp622 output")
        assert_no_source_drift(self.root, self.base, head)


    def test_all_four_published_json_schemas_are_accepted(self):
        outputs = {
            590: "2026-11-02-exp590-corrected-L-metadata.json",
            593: "2026-11-02-exp593-corrected-L-metadata.json",
            622: "exp_622_ch_sh_specificity_interaction/results.json",
            623: "exp_623_it2a_ch_sh_specificity_replication/results.json",
        }
        for exp, name in outputs.items():
            self.write("research/experiments/" + name,
                       json.dumps(self.sample_output(exp)))
        head = self.commit("four valid publisher artifacts")
        self.assertEqual(changed_source_paths(self.root, self.base, head), [])

    def test_empty_json_object_is_not_safe_generated_output(self):
        # Formerly a root object, including {}, passed the drift exemption.
        self.write("research/experiments/2026-11-02-exp590-corrected-L-metadata.json", "{}")
        head = self.commit("empty JSON object")
        with self.assertRaisesRegex(RuntimeError, "wrong or missing experiment identity"):
            assert_no_source_drift(self.root, self.base, head)

    def test_wrong_experiment_identity_is_rejected(self):
        data = self.sample_output(590)
        data["experiment"] = "EXP-593"
        self.write("research/experiments/2026-11-02-exp590-corrected-L-metadata.json",
                   json.dumps(data))
        head = self.commit("wrong experiment identity")
        with self.assertRaisesRegex(RuntimeError, "wrong or missing experiment identity"):
            assert_no_source_drift(self.root, self.base, head)

    def test_wrong_source_hash_is_rejected(self):
        data = self.sample_output(593)
        data["source_sha256"] = "0" * 64
        self.write("research/experiments/2026-11-02-exp593-corrected-L-metadata.json",
                   json.dumps(data))
        head = self.commit("wrong source hash")
        with self.assertRaisesRegex(RuntimeError, "pinned corpus provenance"):
            assert_no_source_drift(self.root, self.base, head)

    def test_boolean_and_negative_counts_are_rejected(self):
        for suffix, value in (("bool", True), ("negative", -1)):
            with self.subTest(value=value):
                # Each candidate is compared with the unchanged baseline;
                # the prior invalid candidate also remains unsafe.
                data = self.sample_output(590)
                data["metrics"]["tokens"] = value
                path = "research/experiments/2026-11-02-exp590-corrected-L-metadata.json"
                self.write(path, json.dumps(data))
                head = self.commit("invalid " + suffix + " token count")
                with self.assertRaisesRegex(RuntimeError, "invalid EXP-590 count fields"):
                    assert_no_source_drift(self.root, self.base, head)

    def test_exp593_missing_variant_result_is_rejected(self):
        data = self.sample_output(593)
        del data["tests"]["dain"]
        self.write("research/experiments/2026-11-02-exp593-corrected-L-metadata.json",
                   json.dumps(data))
        head = self.commit("missing variant result")
        with self.assertRaisesRegex(RuntimeError, "variant/test coverage"):
            assert_no_source_drift(self.root, self.base, head)

    def test_exp622_out_of_range_p_is_rejected(self):
        data = self.sample_output(622)
        data["two_sided_permutation_p"] = 1.5
        self.write("research/experiments/exp_622_ch_sh_specificity_interaction/results.json",
                   json.dumps(data))
        head = self.commit("impossible p value")
        with self.assertRaisesRegex(RuntimeError, "invalid EXP-622/623 result fields"):
            assert_no_source_drift(self.root, self.base, head)

    def test_exp623_missing_counts_is_rejected(self):
        data = self.sample_output(623)
        del data["matched_strata"]
        self.write("research/experiments/exp_623_it2a_ch_sh_specificity_replication/results.json",
                   json.dumps(data))
        head = self.commit("missing count")
        with self.assertRaisesRegex(RuntimeError, "invalid EXP-622/623 result fields"):
            assert_no_source_drift(self.root, self.base, head)

    def test_exp590_aggregate_target_exceeds_token_count_is_rejected(self):
        data = self.sample_output(590)
        data["metrics"]["target_occurrences"] = data["metrics"]["tokens"] + 1
        self.write("research/experiments/2026-11-02-exp590-corrected-L-metadata.json",
                   json.dumps(data))
        head = self.commit("impossible EXP-590 aggregate")
        with self.assertRaisesRegex(RuntimeError, "inconsistent EXP-590 aggregate counts"):
            assert_no_source_drift(self.root, self.base, head)

    def test_exp590_initial_count_exceeds_line_count_is_rejected(self):
        data = self.sample_output(590)
        data["metrics"]["line_initial_occurrences"] = data["metrics"]["lines"] + 1
        self.write("research/experiments/2026-11-02-exp590-corrected-L-metadata.json",
                   json.dumps(data))
        head = self.commit("impossible EXP-590 line-initial count")
        with self.assertRaisesRegex(RuntimeError, "inconsistent EXP-590 aggregate counts"):
            assert_no_source_drift(self.root, self.base, head)

    def test_exp590_currier_partition_must_be_complete(self):
        data = self.sample_output(590)
        del data["metrics"]["currier"]["unknown"]
        self.write("research/experiments/2026-11-02-exp590-corrected-L-metadata.json",
                   json.dumps(data))
        head = self.commit("missing EXP-590 Currier class")
        with self.assertRaisesRegex(RuntimeError, "invalid EXP-590 Currier partition"):
            assert_no_source_drift(self.root, self.base, head)

    def test_exp590_currier_subgroup_cannot_exceed_its_lines(self):
        data = self.sample_output(590)
        data["metrics"]["currier"]["A"]["line_initial_lines"] = 2000
        self.write("research/experiments/2026-11-02-exp590-corrected-L-metadata.json",
                   json.dumps(data))
        head = self.commit("impossible EXP-590 subgroup")
        with self.assertRaisesRegex(RuntimeError, "inconsistent EXP-590 Currier subgroup counts"):
            assert_no_source_drift(self.root, self.base, head)

    def test_exp590_currier_partition_sum_must_match_aggregate(self):
        data = self.sample_output(590)
        data["metrics"]["currier"]["B"]["target_occurrences"] += 1
        self.write("research/experiments/2026-11-02-exp590-corrected-L-metadata.json",
                   json.dumps(data))
        head = self.commit("EXP-590 subgroup totals differ from aggregate")
        with self.assertRaisesRegex(RuntimeError, "inconsistent EXP-590 Currier partition totals"):
            assert_no_source_drift(self.root, self.base, head)

    def test_exp590_currier_partition_rejects_boolean_subgroup_count(self):
        data = self.sample_output(590)
        data["metrics"]["currier"]["unknown"]["lines"] = True
        self.write("research/experiments/2026-11-02-exp590-corrected-L-metadata.json",
                   json.dumps(data))
        head = self.commit("boolean EXP-590 Currier subgroup count")
        with self.assertRaisesRegex(RuntimeError, "invalid EXP-590 Currier partition"):
            assert_no_source_drift(self.root, self.base, head)

    def assert_exp590_concurrent_output_rejected(self, data, error):
        path = "research/experiments/2026-11-02-exp590-corrected-L-metadata.json"
        self.write(path, json.dumps(data))
        head = self.commit("synthetic contradictory EXP-590 generated output")
        with self.assertRaisesRegex(RuntimeError, error):
            assert_no_source_drift(self.root, self.base, head)

    def test_exp590_initial_rate_must_match_counts(self):
        data = self.sample_output(590)
        data["metrics"]["initial_rate_per_target_occurrence"] = 0.5
        self.assert_exp590_concurrent_output_rejected(
            data, "inconsistent EXP-590 positional rates")

    def test_exp590_final_rate_boolean_is_invalid(self):
        data = self.sample_output(590)
        data["metrics"]["final_rate_per_target_occurrence"] = True
        self.assert_exp590_concurrent_output_rejected(
            data, "inconsistent EXP-590 positional rates")

    def test_exp590_missing_null_exceedances_is_invalid(self):
        data = self.sample_output(590)
        del data["permutation_test"]["null_ge_observed"]
        self.assert_exp590_concurrent_output_rejected(
            data, "invalid EXP-590 null distribution fields")

    def test_exp590_exceedances_cannot_exceed_replicates(self):
        data = self.sample_output(590)
        data["permutation_test"]["null_ge_observed"] = (
            data["permutation_test"]["permutations"] + 1)
        self.assert_exp590_concurrent_output_rejected(
            data, "invalid EXP-590 null distribution fields")

    def test_exp590_negative_null_sd_is_invalid(self):
        data = self.sample_output(590)
        data["permutation_test"]["null_sd_initial_lines"] = -0.01
        self.assert_exp590_concurrent_output_rejected(
            data, "invalid EXP-590 null distribution fields")

    def test_exp590_null_mean_cannot_exceed_lines(self):
        data = self.sample_output(590)
        data["permutation_test"]["null_mean_initial_lines"] = data["metrics"]["lines"] + 1
        self.assert_exp590_concurrent_output_rejected(
            data, "invalid EXP-590 null distribution fields")

    def test_exp590_null_mean_cannot_exceed_target_occurrences(self):
        # A draw can put at most one daiin at each line start; it cannot
        # create more initial daiin lines than daiin tokens in the corpus.
        data = self.sample_output(590)
        data["permutation_test"]["null_mean_initial_lines"] = (
            data["metrics"]["target_occurrences"] + 1)
        self.assert_exp590_concurrent_output_rejected(
            data, "invalid EXP-590 null distribution fields")

    def test_exp590_null_sd_cannot_exceed_bounded_variance(self):
        # This value was accepted before the variance support guard.
        data = self.sample_output(590)
        data["permutation_test"]["null_sd_initial_lines"] = 10000.0
        self.assert_exp590_concurrent_output_rejected(
            data, "invalid EXP-590 null distribution fields")

    def test_exp590_p_value_must_match_exceedances(self):
        data = self.sample_output(590)
        data["permutation_test"]["empirical_one_sided_p"] = 0.5
        self.assert_exp590_concurrent_output_rejected(
            data, "inconsistent EXP-590 permutation p-value")

    def assert_exp593_concurrent_output_rejected(self, data, error):
        path = "research/experiments/2026-11-02-exp593-corrected-L-metadata.json"
        self.write(path, json.dumps(data))
        head = self.commit("synthetic contradictory EXP-593 generated output")
        with self.assertRaisesRegex(RuntimeError, error):
            assert_no_source_drift(self.root, self.base, head)

    def test_exp593_occurrences_cannot_exceed_total_tokens(self):
        data = self.sample_output(593)
        data["observed"]["daiin"]["occurrences"] = data["tokens"] + 1
        self.assert_exp593_concurrent_output_rejected(
            data, "inconsistent EXP-593 observed counts")

    def test_exp593_line_initial_cannot_exceed_total_lines(self):
        data = self.sample_output(593)
        data["observed"]["daiin"]["line_initial"] = data["lines"] + 1
        self.assert_exp593_concurrent_output_rejected(
            data, "inconsistent EXP-593 observed counts")

    def test_exp593_currier_partition_requires_unknown_class(self):
        data = self.sample_output(593)
        del data["observed"]["daiin"]["by_currier"]["unknown"]
        self.assert_exp593_concurrent_output_rejected(
            data, "invalid EXP-593 Currier partition")

    def test_exp593_currier_subtotals_must_match_variant(self):
        data = self.sample_output(593)
        data["observed"]["daiin"]["by_currier"]["B"]["occurrences"] += 1
        self.assert_exp593_concurrent_output_rejected(
            data, "inconsistent EXP-593 Currier partition totals")

    def test_exp593_currier_initial_cannot_exceed_subgroup_occurrences(self):
        data = self.sample_output(593)
        data["observed"]["daiin"]["by_currier"]["A"]["line_initial"] = 441
        self.assert_exp593_concurrent_output_rejected(
            data, "inconsistent EXP-593 Currier subgroup counts")

    def test_exp593_boolean_currier_count_is_not_integer(self):
        data = self.sample_output(593)
        data["observed"]["daiin"]["by_currier"]["unknown"]["occurrences"] = True
        self.assert_exp593_concurrent_output_rejected(
            data, "invalid EXP-593 Currier partition")

    def test_exp593_initial_fraction_must_match_counts(self):
        data = self.sample_output(593)
        data["observed"]["daiin"]["initial_fraction"] = 0.1
        self.assert_exp593_concurrent_output_rejected(
            data, "inconsistent EXP-593 initial fraction")

    def test_exp593_negative_null_sd_is_invalid(self):
        data = self.sample_output(593)
        data["tests"]["daiin"]["null_sd_initial"] = -1.0
        self.assert_exp593_concurrent_output_rejected(
            data, "invalid EXP-593 null moments/statistic")

    def test_exp593_null_mean_cannot_exceed_lines(self):
        data = self.sample_output(593)
        data["tests"]["dain"]["null_mean_initial"] = data["lines"] + 1
        self.assert_exp593_concurrent_output_rejected(
            data, "invalid EXP-593 null moments/statistic")

    def test_exp593_null_sd_cannot_exceed_bounded_variance(self):
        data = self.sample_output(593)
        data["tests"]["daiiin"]["null_sd_initial"] = data["lines"]
        self.assert_exp593_concurrent_output_rejected(
            data, "invalid EXP-593 null moments/statistic")

    def test_exp593_rare_variant_null_mean_cannot_exceed_occurrences(self):
        # This was previously accepted: 20 <= 4,188 lines, but only 19
        # daiiin tokens exist, so no shuffle can put 20 at line starts.
        data = self.sample_output(593)
        row = data["observed"]["daiiin"]
        test = data["tests"]["daiiin"]
        test["null_mean_initial"] = row["occurrences"] + 1.0
        test["null_sd_initial"] = 1.0
        test["observed_standardized_statistic"] = (
            row["line_initial"] - test["null_mean_initial"]
        ) / test["null_sd_initial"]
        self.assert_exp593_concurrent_output_rejected(
            data, "invalid EXP-593 null moments/statistic")

    def test_exp593_rare_variant_null_sd_respects_occurrence_bound(self):
        # At mean 10, the maximum feasible variance with 19 occurrences
        # is 10 * (19 - 10) = 90, not 10 * (4188 - 10).
        data = self.sample_output(593)
        row = data["observed"]["daiiin"]
        test = data["tests"]["daiiin"]
        test["null_mean_initial"] = 10.0
        test["null_sd_initial"] = 20.0
        test["observed_standardized_statistic"] = (
            row["line_initial"] - test["null_mean_initial"]
        ) / test["null_sd_initial"]
        self.assert_exp593_concurrent_output_rejected(
            data, "invalid EXP-593 null moments/statistic")

    def test_exp593_observed_standardized_statistic_must_match(self):
        data = self.sample_output(593)
        data["tests"]["daiin"]["observed_standardized_statistic"] += 0.5
        self.assert_exp593_concurrent_output_rejected(
            data, "inconsistent EXP-593 standardized statistic")

    def test_exp593_boolean_null_statistic_is_invalid(self):
        data = self.sample_output(593)
        data["tests"]["dain"]["observed_standardized_statistic"] = True
        self.assert_exp593_concurrent_output_rejected(
            data, "invalid EXP-593 null moments/statistic")

    def test_exp593_empirical_p_must_use_plus_one_grid(self):
        data = self.sample_output(593)
        data["tests"]["daiin"]["empirical_p"] = 0.5
        self.assert_exp593_concurrent_output_rejected(
            data, "inconsistent EXP-593 permutation p-value grid")

    def test_exp593_max_t_p_must_use_plus_one_grid(self):
        data = self.sample_output(593)
        data["tests"]["daiin"]["max_stat_adjusted_p"] = 0.5
        self.assert_exp593_concurrent_output_rejected(
            data, "inconsistent EXP-593 permutation p-value grid")

    def test_exp593_adjusted_p_cannot_be_below_empirical_p(self):
        data = self.sample_output(593)
        data["tests"]["daiiin"]["max_stat_adjusted_p"] = (
            1 / (data["permutations"] + 1))
        self.assert_exp593_concurrent_output_rejected(
            data, "inconsistent EXP-593 max-T adjustment")

    def assert_exp622_623_concurrent_output_rejected(self, exp, data, error):
        paths = {
            622: "exp_622_ch_sh_specificity_interaction/results.json",
            623: "exp_623_it2a_ch_sh_specificity_replication/results.json",
        }
        self.write("research/experiments/" + paths[exp], json.dumps(data))
        head = self.commit("synthetic contradictory EXP-622/623 generated output")
        with self.assertRaisesRegex(RuntimeError, error):
            assert_no_source_drift(self.root, self.base, head)

    def test_exp622_matched_strata_need_two_occurrences_each(self):
        data = self.sample_output(622)
        data["matched_strata"] = data["occurrences_with_two_neighbors"] // 2 + 1
        self.assert_exp622_623_concurrent_output_rejected(
            622, data, "inconsistent EXP-622/623 matched population")

    def test_exp623_folios_cannot_exceed_matched_strata(self):
        data = self.sample_output(623)
        data["folios_in_matched_strata"] = data["matched_strata"] + 1
        self.assert_exp622_623_concurrent_output_rejected(
            623, data, "inconsistent EXP-622/623 matched population")

    def test_exp622_next_rate_difference_must_be_bounded(self):
        data = self.sample_output(622)
        data["mean_matched_stratum_next_sh_minus_ch"] = 1.01
        self.assert_exp622_623_concurrent_output_rejected(
            622, data, "invalid EXP-622/623 matched rate contrast")

    def test_exp623_prev_rate_difference_must_be_bounded(self):
        data = self.sample_output(623)
        data["mean_matched_stratum_prev_sh_minus_ch"] = -1.01
        self.assert_exp622_623_concurrent_output_rejected(
            623, data, "invalid EXP-622/623 matched rate contrast")

    def test_exp622_boolean_rate_difference_is_invalid(self):
        data = self.sample_output(622)
        data["mean_matched_stratum_next_sh_minus_ch"] = True
        self.assert_exp622_623_concurrent_output_rejected(
            622, data, "invalid EXP-622/623 matched rate contrast")

    def test_exp623_interaction_must_equal_next_minus_prev(self):
        data = self.sample_output(623)
        data["interaction_next_minus_prev"] += 0.1
        self.assert_exp622_623_concurrent_output_rejected(
            623, data, "inconsistent EXP-622/623 interaction components")

    def test_exp622_p_value_must_match_exceedances(self):
        data = self.sample_output(622)
        data["two_sided_permutation_p"] = 0.5
        self.assert_exp622_623_concurrent_output_rejected(
            622, data, "inconsistent EXP-622/623 permutation p-value")

    def test_exp623_p_value_must_match_exceedances(self):
        data = self.sample_output(623)
        data["permutation_exceedances"] -= 1
        self.assert_exp622_623_concurrent_output_rejected(
            623, data, "inconsistent EXP-622/623 permutation p-value")

    def test_historical_erratum_edit_blocks(self):
        self.write("research/experiments/2026-10-20-exp590-erratum.md", "rewritten correction\n")
        head = self.commit("concurrent historical correction")
        with self.assertRaisesRegex(RuntimeError, "exp590-erratum.md"):
            assert_no_source_drift(self.root, self.base, head)

    def test_historical_json_edit_blocks(self):
        self.write("research/experiments/2026-10-20-exp590.json", '{"value": 99}\n')
        head = self.commit("concurrent historical result rewrite")
        with self.assertRaisesRegex(RuntimeError, "exp590.json"):
            assert_no_source_drift(self.root, self.base, head)

    def test_existing_dated_output_edit_blocks(self):
        self.write("research/experiments/2026-10-29-exp590-corrected-L-metadata.json", '{"value": 2}\n')
        head = self.commit("concurrent rewrite of prior generated result")
        with self.assertRaisesRegex(RuntimeError, "2026-10-29-exp590"):
            assert_no_source_drift(self.root, self.base, head)

    def test_unknown_new_file_under_output_root_blocks(self):
        self.write("research/experiments/archive/new-analysis.md", "unexpected input\n")
        head = self.commit("new historical analysis")
        with self.assertRaisesRegex(RuntimeError, "archive/new-analysis.md"):
            assert_no_source_drift(self.root, self.base, head)

    def test_misnamed_output_blocks(self):
        self.write("research/experiments/2026-10-30-exp590-corrected-L-metadata.json.bak", "{}\n")
        head = self.commit("unexpected output suffix")
        with self.assertRaisesRegex(RuntimeError, "json.bak"):
            assert_no_source_drift(self.root, self.base, head)

    def test_deleted_generated_output_blocks(self):
        (self.root / "research/experiments/2026-10-29-exp590-corrected-L-metadata.json").unlink()
        head = self.commit("concurrent output deletion")
        with self.assertRaisesRegex(RuntimeError, "2026-10-29-exp590"):
            assert_no_source_drift(self.root, self.base, head)

    def test_divergent_identical_trees_block_publication(self):
        # A rewritten master can have the same files but a different history.
        self.git("checkout", "-qb", "replacement", self.base)
        self.git("commit", "--allow-empty", "-qm", "replacement history")
        replacement = self.git("rev-parse", "HEAD").strip()
        self.git("checkout", "-qb", "generator", self.base)
        self.git("commit", "--allow-empty", "-qm", "generating history")
        generating = self.git("rev-parse", "HEAD").strip()
        self.assertNotEqual(generating, replacement)
        self.assertEqual(self.git("diff", "--name-only", generating, replacement), "")
        with self.assertRaisesRegex(RuntimeError, "not a descendant"):
            assert_no_source_drift(self.root, generating, replacement)

    def test_older_candidate_blocks_publication_even_with_same_tree(self):
        self.git("commit", "--allow-empty", "-qm", "generating commit")
        generating = self.git("rev-parse", "HEAD").strip()
        with self.assertRaisesRegex(RuntimeError, "not a descendant"):
            assert_no_source_drift(self.root, generating, self.base)

    def test_same_tree_descendant_remains_allowed(self):
        self.git("commit", "--allow-empty", "-qm", "new descendant")
        descendant = self.git("rev-parse", "HEAD").strip()
        assert_no_source_drift(self.root, self.base, self.base)
        assert_no_source_drift(self.root, self.base, descendant)


if __name__ == "__main__":
    unittest.main()
