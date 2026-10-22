#!/usr/bin/env python3
"""Smoke test for the EXP-573 repository-relative corpus path."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments/exp_573_c007_reconciliation/script.py"
spec = importlib.util.spec_from_file_location("exp573_reconciliation", SCRIPT)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

assert module.ROOT == ROOT.resolve(), module.ROOT
assert module.CORPUS == ROOT.resolve() / "data/transcriptions/eva_zl3b.txt", module.CORPUS
assert module.CORPUS.is_file(), f"Missing EXP-573 corpus: {module.CORPUS}"
assert not str(module.CORPUS).startswith("/Users/"), module.CORPUS
print("EXP-573 repository-relative corpus path smoke test passed.")
