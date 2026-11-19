"""Regression: lag pair guard must execute with and without Python assertions.

Extract only pure helpers from the historical runner; importing the runner
would launch its expensive scientific analysis. No corpus is loaded or changed.
"""
import ast
from pathlib import Path
import subprocess
import sys
import unittest

RUNNER = Path(__file__).resolve().parents[1] / "research/analysis/2026-10-23-lag-screen/run.py"

CHECK = r'''
import ast
from collections import Counter
from pathlib import Path
source = Path(__import__("sys").argv[1]).read_text(encoding="utf-8")
tree = ast.parse(source)
selected = [node for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name in {"chains", "verify"}]
if len(selected) != 2 or {node.name for node in selected} != {"chains", "verify"}:
    raise RuntimeError("Expected exactly one chains and one verify helper")
namespace = {"Counter": Counter}
exec(compile(ast.Module(body=selected, type_ignores=[]), "<lag-helpers>", "exec"), namespace)
namespace["verify"]()  # positive control
def broken_chains(rows, distance):
    return [{"tokens": ["wrong", "wrong"]}]
namespace["chains"] = broken_chains
try:
    namespace["verify"]()
except ValueError as exc:
    if "Lag pair construction mismatch" not in str(exc):
        raise
else:
    raise RuntimeError("Broken lag pair construction escaped validation")
'''

class LagGuardOptimizedRegression(unittest.TestCase):
    def test_guard_rejects_broken_pairs_normal_and_optimized(self):
        for flag in ([], ["-O"]):
            with self.subTest(python_flags=flag):
                completed = subprocess.run(
                    [sys.executable, *flag, "-c", CHECK, str(RUNNER)],
                    capture_output=True, text=True, timeout=15, check=False)
                self.assertEqual(completed.returncode, 0, completed.stderr)

if __name__ == "__main__":
    unittest.main()
