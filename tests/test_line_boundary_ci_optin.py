#!/usr/bin/env python3
"""Guard against automatic scientific replay on every PR/push.

This test inspects workflow configuration only; it never imports or runs
the line-boundary predictor and does not access held-out labels.
"""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/voynich-check.yml"
RUN_CMD = (
    "python research/analysis/2026-10-28-line-boundary-reproduction/"
    "line_boundary_replication.py"
)
GUARD = (
    "${{ github.event_name == 'workflow_dispatch' && "
    "inputs.run_line_boundary_replication == true }}"
)


class LineBoundaryCIOptInTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # BaseLoader preserves YAML's literal 'on' and boolean-like scalars.
        cls.workflow = yaml.load(WORKFLOW.read_text(encoding="utf-8"),
                                 Loader=yaml.BaseLoader)
        cls.steps = cls.workflow["jobs"]["check"]["steps"]

    def test_dispatch_is_explicit_boolean_default_false(self):
        dispatch = self.workflow["on"]["workflow_dispatch"]
        option = dispatch["inputs"]["run_line_boundary_replication"]
        self.assertEqual(option["type"], "boolean")
        self.assertEqual(option["required"], "false")
        self.assertEqual(option["default"], "false")
        self.assertIn("pull_request", self.workflow["on"])
        self.assertIn("push", self.workflow["on"])

    def test_only_predictor_invocation_requires_manual_opt_in(self):
        executing = [step for step in self.steps if RUN_CMD in step.get("run", "")]
        self.assertEqual(len(executing), 1)
        self.assertEqual(executing[0]["name"],
                         "Recalcular réplica corregida de límites de línea")
        self.assertEqual(executing[0]["if"], GUARD)

    def test_scientific_artifact_upload_has_same_guard(self):
        uploads = [step for step in self.steps if
                   "line-boundary-replication-${{ github.run_id }}"
                   in step.get("with", {}).get("name", "")]
        self.assertEqual(len(uploads), 1)
        self.assertEqual(uploads[0]["if"], GUARD)
        self.assertEqual(uploads[0]["with"]["if-no-files-found"], "error")

    def test_regression_runs_without_predictor(self):
        checks = [step for step in self.steps if
                  "test_line_boundary_ci_optin.py" in step.get("run", "")]
        self.assertEqual(len(checks), 1)
        self.assertNotIn(RUN_CMD, checks[0]["run"])
        self.assertIn("python -O", checks[0]["run"])


if __name__ == "__main__":
    unittest.main()
