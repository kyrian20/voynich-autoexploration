"""Regression: registered experiment paths must not redirect through symlinks."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import audit_repository_operations as audit


class ExperimentRegistrySymlinkTests(unittest.TestCase):
    def test_symlinked_experiment_directory_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "research").mkdir()
            (root / "experiments").mkdir()
            outside = root / "outside"
            outside.mkdir()
            (root / "experiments" / "exp_999_external").symlink_to(
                outside, target_is_directory=True
            )
            (root / "research" / "EXPERIMENT_PATH_REGISTRY.json").write_text(
                json.dumps({"entries": [], "numeric_collisions": {}})
            )
            with patch.object(audit, "ROOT", root):
                with self.assertRaisesRegex(ValueError, "Symlink in experiments tree"):
                    audit.audit_experiment_paths()

    def test_symlinked_experiments_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root / "outside"
            outside.mkdir()
            (root / "experiments").symlink_to(outside, target_is_directory=True)
            with patch.object(audit, "ROOT", root):
                with self.assertRaisesRegex(ValueError, "Experiment root must not be a symlink"):
                    audit.audit_experiment_paths()

    def test_empty_regular_registry_is_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "research").mkdir()
            (root / "experiments").mkdir()
            (root / "research" / "EXPERIMENT_PATH_REGISTRY.json").write_text(
                json.dumps({"entries": [], "numeric_collisions": {}})
            )
            with patch.object(audit, "ROOT", root):
                result = audit.audit_experiment_paths()
            self.assertEqual(result["unique_path_ids"], 0)


if __name__ == "__main__":
    unittest.main()
