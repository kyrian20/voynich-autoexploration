"""Regression for a scheduled publisher rebase that could mislabel inputs."""
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
        self.write("research/experiments/output.json", '{"value": 1}\n')
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

    def test_output_only_update_is_safe(self):
        self.write("research/experiments/output.json", '{"value": 2}\n')
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
        self.write("research/experiments/output.json", '{"value": 2}\n')
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


if __name__ == "__main__":
    unittest.main()
