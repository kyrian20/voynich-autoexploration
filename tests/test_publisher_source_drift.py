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
                # Separate target paths permit both mutations in one repo
                # without overwriting or altering the baseline.
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
