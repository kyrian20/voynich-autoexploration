"""Regression for concurrent changes to historical evidence under output root."""
from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

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

    def test_new_known_dated_output_is_safe(self):
        self.write("research/experiments/2026-10-30-exp590-corrected-L-metadata.json", '{"value": 2}\n')
        head = self.commit("another publisher updated an output")
        self.assertEqual(changed_source_paths(self.root, self.base, head), [])
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



    def test_new_known_exp622_output_is_safe(self):
        self.write("research/experiments/exp_622_ch_sh_specificity_interaction/results.json", "{}\n")
        head = self.commit("publisher added new exp622 output")
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
